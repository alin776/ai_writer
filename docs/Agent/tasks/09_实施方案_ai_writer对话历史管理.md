# ai_writer 对话历史管理实施方案

## 项目现状分析

### 当前架构
```
ai_writer/backend/app/
├── api/v1/agent.py           # API接口层
├── services/
│   ├── agent/
│   │   ├── langgraph_agent.py    # ❌ 问题代码在这里
│   │   ├── memory/
│   │   │   ├── memory_manager.py  # ✅ 已有记忆管理
│   │   │   ├── long_term_memory.py
│   │   │   └── user_profile.py
```

### 核心问题
**位置**：`langgraph_agent.py:1278`
```python
# ❌ 每次都只传入当前消息
initial_state = {
    "messages": [HumanMessage(content=message)],  # 只有1条！
}
```

---

## 🎯 实施方案（分3步）

### 步骤1：修复对话历史加载（核心，立即见效）

#### 1.1 修改 `langgraph_agent.py` 的 `chat` 方法

**文件位置**：`ai_writer/backend/app/services/agent/langgraph_agent.py:1254`

**完整修改代码**：

```python
async def chat(
    self,
    message: str,
    work_id: Optional[str] = None,
    chapter_id: Optional[str] = None,
    conversation_id: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    与 Agent 对话（支持上下文记忆）

    Args:
        message: 用户消息
        work_id: 作品ID
        chapter_id: 章节ID
        conversation_id: 会话ID（用于记忆）
        context: 额外上下文

    Returns:
        Dict: Agent响应
    """

    conversation_id = conversation_id or str(uuid.uuid4())
    config = {"configurable": {"thread_id": conversation_id}}

    # ========== ✅ 核心修改：加载对话历史 ==========
    logger.info(f"[LangGraph] 会话ID: {conversation_id}")

    messages = []
    try:
        # 1️⃣ 尝试从Checkpointer加载历史state
        saved_checkpoint = self.checkpointer.get(config)

        if saved_checkpoint and saved_checkpoint.channel_values:
            # 有历史对话
            saved_messages = saved_checkpoint.channel_values.get("messages", [])
            logger.info(f"[LangGraph] ✅ 加载了 {len(saved_messages)} 条历史消息")

            # 2️⃣ 将历史消息复制到新列表（避免修改原对象）
            messages = list(saved_messages)

            # 3️⃣ 追加新消息
            messages.append(HumanMessage(content=message))

            # 4️⃣ 恢复其他状态（如果之前有）
            work_id = work_id or saved_checkpoint.channel_values.get("work_id")
            chapter_id = chapter_id or saved_checkpoint.channel_values.get("chapter_id")

        else:
            # 首次对话
            logger.info(f"[LangGraph] 🆕 首次对话，创建新会话")
            messages = [HumanMessage(content=message)]

    except Exception as e:
        logger.warning(f"[LangGraph] ⚠️ 加载历史失败: {e}，创建新会话")
        messages = [HumanMessage(content=message)]

    # 5️⃣ 长度限制：避免token溢出
    MAX_MESSAGES = 50  # 最多保留50条消息
    if len(messages) > MAX_MESSAGES:
        logger.warning(f"[LangGraph] ⚠️ 消息过多({len(messages)}条)，截断为{MAX_MESSAGES}条")
        # 保留最近的消息
        messages = messages[-MAX_MESSAGES:]

    # ========== 构建state ==========
    initial_state = {
        "messages": messages,  # ✅ 包含完整对话历史
        "work_id": work_id,
        "chapter_id": chapter_id,
        "intent": None,
        "context": context or {},
        "agent_steps": [],
        "suggested_actions": [],
        "final_response": None
    }

    # ========== 运行图 ==========
    try:
        logger.info(f"[LangGraph] 📝 开始处理，总消息数: {len(messages)}")
        result = await self.graph.ainvoke(initial_state, config)

        logger.info(f"[LangGraph] ✅ 处理完成")

        return {
            "response": result["final_response"],
            "conversation_id": conversation_id,
            "agent_steps": result["agent_steps"],
            "suggested_actions": result["suggested_actions"],
            "metadata": {
                "intent": result.get("intent"),
                "message_count": len(messages),  # 返回总消息数
                "timestamp": str(datetime.now())
            }
        }

    except Exception as e:
        logger.error(f"[LangGraph] ❌ Agent执行失败: {e}", exc_info=True)
        return {
            "response": f"抱歉，处理您的请求时出错了：{str(e)}",
            "conversation_id": conversation_id,
            "agent_steps": [],
            "suggested_actions": [],
            "metadata": {"error": str(e)}
        }
```

#### 1.2 同样修改 `chat_with_planning` 方法

**文件位置**：`ai_writer/backend/app/services/agent/langgraph_agent.py:1418`

在 `chat_with_planning` 方法开头添加相同的历史加载逻辑：

```python
async def chat_with_planning(
    self,
    message: str,
    work_id: Optional[str] = None,
    chapter_id: Optional[str] = None,
    conversation_id: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None,
    on_plan: Optional[callable] = None,
    on_task_start: Optional[callable] = None,
    on_task_progress: Optional[callable] = None,
    on_task_done: Optional[callable] = None,
    on_content: Optional[callable] = None
) -> Dict[str, Any]:
    """Planning + Execution 模式（支持上下文记忆）"""

    conversation_id = conversation_id or str(uuid.uuid4())
    config = {"configurable": {"thread_id": conversation_id}}

    # ========== ✅ 加载对话历史 ==========
    conversation_history_text = ""
    try:
        saved_checkpoint = self.checkpointer.get(config)
        if saved_checkpoint and saved_checkpoint.channel_values:
            saved_messages = saved_checkpoint.channel_values.get("messages", [])
            logger.info(f"[Planning] ✅ 加载了 {len(saved_messages)} 条历史消息")

            # 将历史格式化为文本（用于planning prompt）
            history_lines = []
            for msg in saved_messages[-5:]:  # 只取最近5条
                if isinstance(msg, HumanMessage):
                    history_lines.append(f"用户: {msg.content}")
                elif isinstance(msg, AIMessage):
                    history_lines.append(f"助手: {msg.content[:100]}...")  # 截断

            if history_lines:
                conversation_history_text = f"""
【对话历史】（最近5轮）
{chr(10).join(history_lines)}

"""
        else:
            logger.info(f"[Planning] 🆕 首次对话")

    except Exception as e:
        logger.warning(f"[Planning] ⚠️ 加载历史失败: {e}")

    # 将历史加入到当前消息
    if conversation_history_text:
        message = conversation_history_text + f"【当前请求】\n{message}"

    # 继续原有的planning逻辑...
    try:
        # ========== 阶段1: 规划（Planning） ==========
        logger.info(f"[Planning] 开始规划: {message[:50]}...")
        # ...（原有代码）
```

---

### 步骤2：实现Redis Checkpointer（持久化，可选）

#### 2.1 创建 `redis_checkpointer.py`

**文件位置**：`ai_writer/backend/app/services/agent/memory/redis_checkpointer.py`

**完整代码**：

```python
"""
Redis Checkpointer for LangGraph
基于Redis实现LangGraph的持久化Checkpointer
"""

from typing import Optional, Iterator, Any, Dict
from datetime import datetime
import json
import logging
import redis
from langgraph.checkpoint.base import BaseCheckpointer, Checkpoint
from langchain_core.runnables import RunnableConfig

logger = logging.getLogger(__name__)


class RedisCheckpointer(BaseCheckpointer):
    """基于Redis的LangGraph Checkpointer"""

    def __init__(
        self,
        redis_client: redis.Redis,
        key_prefix: str = "langgraph:checkpoint",
        ttl: int = 7 * 24 * 3600  # 7天
    ):
        self.redis = redis_client
        self.key_prefix = key_prefix
        self.ttl = ttl
        logger.info(f"[RedisCheckpointer] 初始化完成，TTL={ttl}秒")

    def _make_key(self, thread_id: str) -> str:
        return f"{self.key_prefix}:{thread_id}:latest"

    def get(self, config: RunnableConfig) -> Optional[Checkpoint]:
        """获取checkpoint"""
        try:
            thread_id = config.get("configurable", {}).get("thread_id")
            if not thread_id:
                return None

            key = self._make_key(thread_id)
            data = self.redis.get(key)

            if not data:
                return None

            checkpoint_data = json.loads(data)

            checkpoint = Checkpoint(
                v=checkpoint_data.get("v", 1),
                id=checkpoint_data.get("id"),
                ts=checkpoint_data.get("ts"),
                channel_values=checkpoint_data.get("channel_values", {}),
                channel_versions=checkpoint_data.get("channel_versions", {}),
                versions_seen=checkpoint_data.get("versions_seen", {})
            )

            return checkpoint

        except Exception as e:
            logger.error(f"[RedisCheckpointer] 加载失败: {e}", exc_info=True)
            return None

    def put(
        self,
        config: RunnableConfig,
        checkpoint: Checkpoint,
        metadata: Optional[Dict[str, Any]] = None
    ) -> RunnableConfig:
        """保存checkpoint"""
        try:
            thread_id = config.get("configurable", {}).get("thread_id")
            if not thread_id:
                return config

            checkpoint_data = {
                "v": checkpoint.v,
                "id": checkpoint.id,
                "ts": checkpoint.ts,
                "channel_values": checkpoint.channel_values,
                "channel_versions": checkpoint.channel_versions,
                "versions_seen": checkpoint.versions_seen,
                "metadata": metadata or {},
                "saved_at": datetime.now().isoformat()
            }

            key = self._make_key(thread_id)
            self.redis.setex(
                key,
                self.ttl,
                json.dumps(checkpoint_data, ensure_ascii=False, default=str)
            )

            logger.info(f"[RedisCheckpointer] 保存成功: {thread_id}")
            return config

        except Exception as e:
            logger.error(f"[RedisCheckpointer] 保存失败: {e}", exc_info=True)
            return config

    def list(
        self,
        config: RunnableConfig,
        limit: int = 10,
        before: Optional[str] = None
    ) -> Iterator[Checkpoint]:
        """列出checkpoint历史（简化实现）"""
        checkpoint = self.get(config)
        if checkpoint:
            yield checkpoint
```

#### 2.2 修改 `langgraph_agent.py` 的 `__init__`

**文件位置**：`ai_writer/backend/app/services/agent/langgraph_agent.py:494`

```python
from app.services.agent.memory.redis_checkpointer import RedisCheckpointer

def __init__(
    self,
    ai_service: HTTPAIService,
    redis_client: redis.Redis = None,  # ✅ 新增参数
    use_chatgpt: bool = False
):
    self.ai_service = ai_service
    self.use_chatgpt = use_chatgpt
    set_global_ai_service(ai_service)

    if use_chatgpt:
        logger.info("[LangGraph] 使用 ChatOpenAI 模式")
        self._init_chatgpt_mode()
    else:
        logger.info("[LangGraph] 使用 HTTPAIService 模式")
        self.llm = None
        self.llm_with_tools = None

    # ✅ 使用Redis Checkpointer（如果提供）
    if redis_client:
        logger.info("[LangGraph] 使用 RedisCheckpointer（持久化）")
        self.checkpointer = RedisCheckpointer(
            redis_client=redis_client,
            key_prefix="langgraph:agent:checkpoint",
            ttl=7 * 24 * 3600
        )
    else:
        logger.warning("[LangGraph] 使用 MemorySaver（非持久化）")
        self.checkpointer = MemorySaver()

    self.graph = self._build_graph()
```

#### 2.3 修改API层传递Redis客户端

**文件位置**：`ai_writer/backend/app/api/v1/agent.py:167`

```python
@router.post("/chat", response_model=AgentChatResponse)
async def agent_chat(
    request: AgentChatRequest,
    current_user: User = Depends(get_current_active_user),
    memory: MemoryManager = Depends(get_memory_manager),
    ai_service: HTTPAIService = Depends(get_ai_service),
    db: AsyncSession = Depends(get_db)
):
    try:
        user_id = str(current_user.id)
        conversation_id = request.conversation_id or str(uuid.uuid4())

        # ✅ 获取Redis客户端
        redis_client = get_redis_client()

        # ✅ 创建Agent时传入Redis客户端
        agent_graph = WritingAgentGraph(
            ai_service,
            redis_client=redis_client,  # ✅ 传入
            use_chatgpt=settings.AGENT_USE_CHATGPT
        )

        # 调用
        result = await agent_graph.chat(
            message=request.message,
            work_id=request.work_id,
            chapter_id=request.chapter_id,
            conversation_id=conversation_id,
            context=request.context
        )

        # 记录到MemoryManager（可选）
        memory.record_user_interaction(
            user_id,
            "agent_chat",
            {
                "message": request.message,
                "intent": result["metadata"].get("intent"),
                "conversation_id": conversation_id
            }
        )

        return AgentChatResponse(
            response=result["response"],
            conversation_id=result["conversation_id"],
            agent_steps=result["agent_steps"],
            suggested_actions=result["suggested_actions"],
            metadata=result["metadata"]
        )

    except Exception as e:
        logger.error(f"[Agent API] Error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Agent对话失败: {str(e)}"
        )
```

**同样修改 `/chat/stream` 端点**（约268行）。

---

### 步骤3：添加记忆压缩（可选，优化）

当对话历史过长时，自动压缩旧消息为摘要。

#### 3.1 添加压缩方法

**文件位置**：`ai_writer/backend/app/services/agent/langgraph_agent.py`（新增方法）

```python
async def _compress_messages(
    self,
    messages: List[Any],
    keep_recent: int = 10
) -> List[Any]:
    """
    压缩消息历史

    Args:
        messages: 消息列表
        keep_recent: 保留最近N条消息不压缩

    Returns:
        压缩后的消息列表
    """
    if len(messages) <= keep_recent + 10:
        # 消息不够多，无需压缩
        return messages

    logger.info(f"[LangGraph] 开始压缩消息: {len(messages)}条 → 保留{keep_recent}条")

    # 分离：旧消息 vs 最近消息
    old_messages = messages[:-keep_recent]
    recent_messages = messages[-keep_recent:]

    # 生成摘要
    try:
        old_content = "\n".join([
            f"{'用户' if isinstance(m, HumanMessage) else 'AI'}: {m.content[:200]}"
            for m in old_messages
        ])

        summary_prompt = f"""请将以下对话历史压缩为简洁的摘要（200字以内）：

{old_content}

摘要："""

        summary_text = ""
        async for chunk, _ in self.ai_service._stream_chat(
            messages=[{"role": "user", "content": summary_prompt}],
            max_tokens=300,
            temperature=0.3
        ):
            if chunk:
                summary_text += chunk

        # 用摘要替换旧消息
        compressed = [
            SystemMessage(content=f"【对话摘要】\n{summary_text}")
        ] + recent_messages

        logger.info(f"[LangGraph] ✅ 压缩完成: {len(messages)}条 → {len(compressed)}条")
        return compressed

    except Exception as e:
        logger.error(f"[LangGraph] ❌ 压缩失败: {e}，保持原样")
        return messages
```

#### 3.2 在 `chat` 方法中使用压缩

```python
# 在 chat 方法中，长度限制之后添加：

# 5️⃣ 长度限制
MAX_MESSAGES = 50
if len(messages) > MAX_MESSAGES:
    messages = messages[-MAX_MESSAGES:]

# 6️⃣ 智能压缩（可选）
if len(messages) > 30:
    messages = await self._compress_messages(messages, keep_recent=10)
```

---

## 🧪 测试验证

### 测试1：对话连续性测试

创建测试文件：`tests/test_conversation_memory.py`

```python
import pytest
from app.services.agent.langgraph_agent import WritingAgentGraph
from app.services.ai.http_ai_service import HTTPAIService
import redis

@pytest.mark.asyncio
async def test_conversation_continuity():
    """测试对话连续性"""

    # 1. 创建Agent
    ai_service = HTTPAIService()
    redis_client = redis.Redis(host='localhost', port=6379, db=15, decode_responses=False)
    agent = WritingAgentGraph(ai_service, redis_client=redis_client)

    conversation_id = "test-memory-001"

    # 2. 第一轮对话
    result1 = await agent.chat(
        message="我想写一个科幻小说，背景是2150年的火星殖民地",
        conversation_id=conversation_id
    )
    print(f"\n第1轮 Agent: {result1['response'][:100]}...")
    assert result1["metadata"]["message_count"] == 1

    # 3. 第二轮对话（测试记忆）
    result2 = await agent.chat(
        message="主角应该是什么职业？",
        conversation_id=conversation_id
    )
    print(f"\n第2轮 Agent: {result2['response'][:100]}...")
    assert result2["metadata"]["message_count"] == 3  # 2轮对话=3条消息（1用户+1AI+1用户）

    # ✅ 验证：Agent应该记住"科幻"和"火星"
    response_lower = result2['response'].lower()
    assert any(keyword in response_lower for keyword in ['科幻', '火星', '2150', '殖民'])

    # 4. 第三轮对话
    result3 = await agent.chat(
        message="帮我写第一章的开头",
        conversation_id=conversation_id
    )
    print(f"\n第3轮 Agent: {result3['response'][:100]}...")
    assert result3["metadata"]["message_count"] == 5  # 3轮=5条

    print("\n✅ 测试通过：Agent能够记住完整对话历史！")


@pytest.mark.asyncio
async def test_different_conversations():
    """测试不同会话隔离"""

    ai_service = HTTPAIService()
    redis_client = redis.Redis(host='localhost', port=6379, db=15)
    agent = WritingAgentGraph(ai_service, redis_client=redis_client)

    # 会话A
    result_a1 = await agent.chat(
        message="我想写玄幻小说",
        conversation_id="test-conv-A"
    )

    # 会话B（不同conversation_id）
    result_b1 = await agent.chat(
        message="我想写科幻小说",
        conversation_id="test-conv-B"
    )

    # 继续会话A
    result_a2 = await agent.chat(
        message="主角修炼什么功法？",
        conversation_id="test-conv-A"
    )

    # ✅ 验证：会话A应该记得"玄幻"
    assert "玄幻" in result_a2['response'] or "修炼" in result_a2['response']

    print("\n✅ 测试通过：不同会话相互隔离！")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_conversation_continuity())
    asyncio.run(test_different_conversations())
```

### 运行测试

```bash
cd ai_writer/backend
pytest tests/test_conversation_memory.py -v -s
```

---

## 📋 实施检查清单

### 步骤1：修复对话历史（必须）

- [ ] 修改 `langgraph_agent.py` 的 `chat` 方法（加载历史）
- [ ] 修改 `chat_with_planning` 方法（加载历史）
- [ ] 添加长度限制（MAX_MESSAGES=50）
- [ ] 测试对话连续性

**预计时间**：2-3小时

### 步骤2：实现Redis Checkpointer（推荐）

- [ ] 创建 `redis_checkpointer.py`
- [ ] 修改 `WritingAgentGraph.__init__`
- [ ] 修改 API层传递Redis客户端
- [ ] 测试持久化（重启服务后恢复）

**预计时间**：3-4小时

### 步骤3：添加记忆压缩（可选）

- [ ] 添加 `_compress_messages` 方法
- [ ] 在 `chat` 方法中调用压缩
- [ ] 测试压缩效果

**预计时间**：2小时

---

## 🎯 预期效果

### 修改前
```
用户: "我想写科幻小说"
Agent: "好的，我来帮你..."

用户: "主角叫什么？"
Agent: "请问你想写什么类型的小说？"  # ❌ 忘了
```

### 修改后
```
用户: "我想写科幻小说，背景是2150年火星"
Agent: "好的，我来帮你规划这个火星科幻小说..."

用户: "主角叫什么？"
Agent: "既然是2150年火星殖民地的科幻背景，主角可以..."  # ✅ 记得

用户: "帮我写第一章"
Agent: "好的，让我为你的火星科幻小说写第一章..."  # ✅ 记得完整上下文
```

---

## 🚀 快速开始

### 最小化实施（只做步骤1）

如果时间紧迫，**只实施步骤1**即可立即见效：

1. 修改 `chat` 方法，加载历史messages
2. 添加长度限制
3. 测试

**代码改动**：~50行
**时间**：2-3小时
**效果**：立即解决"失忆"问题

### 完整实施（步骤1+2+3）

如果要生产就绪：

1. 步骤1：修复对话历史
2. 步骤2：Redis持久化
3. 步骤3：记忆压缩

**代码改动**：~200行
**时间**：1天
**效果**：企业级记忆管理

---

## 📞 下一步

1. **立即开始**：先实施步骤1，测试效果
2. **逐步完善**：步骤2和3可以后续添加
3. **持续优化**：根据实际使用情况调整参数

有任何问题随时问我！🎉
