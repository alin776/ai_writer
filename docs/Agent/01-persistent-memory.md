# P0-1: 持久化记忆系统

> 优先级：🔴 P0（核心功能）
>
> 工作量：2天
>
> 预期收益：会话不丢失、支持长期记忆、可回溯历史

---

## 📋 问题描述

### 当前实现

```python
# backend/app/services/agent/langgraph_agent.py:514
from langgraph.checkpoint.memory import MemorySaver

self.checkpointer = MemorySaver()
```

### 存在的问题

1. **❌ 会话易失**：服务重启后所有会话历史丢失
2. **❌ 无长期记忆**：无法记住用户的写作风格、偏好
3. **❌ 不可回溯**：无法查看历史对话和决策过程
4. **❌ 无容错能力**：Agent 执行失败无法从断点恢复

---

## 🎯 解决方案

### 方案选择

LangGraph 官方提供多种 Checkpointer 实现：

| Checkpointer | 适用场景 | 性能 | 持久化 |
|-------------|----------|------|--------|
| MemorySaver | 开发测试 | ⭐⭐⭐⭐⭐ | ❌ |
| SqliteSaver | 本地开发 | ⭐⭐⭐⭐ | ✅ |
| PostgresSaver | 生产环境 | ⭐⭐⭐⭐⭐ | ✅ |
| RedisSaver | 高并发 | ⭐⭐⭐⭐⭐ | ✅ |

**推荐**：使用 **PostgresSaver**（项目已有 PostgreSQL 数据库）

---

## 🔧 实现步骤

### Step 1: 安装依赖

```bash
# 已有依赖（无需安装）
pip install langchain langgraph psycopg
```

### Step 2: 创建 Checkpointer

```python
# backend/app/services/agent/checkpointer.py
from langgraph.checkpoint.postgres import AsyncPostgresSaver
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class CheckpointerFactory:
    """Checkpointer 工厂类"""

    _instance: Optional[AsyncPostgresSaver] = None

    @classmethod
    async def get_checkpointer(cls) -> AsyncPostgresSaver:
        """获取单例 Checkpointer"""

        if cls._instance is None:
            logger.info("[Checkpointer] 初始化 PostgreSQL Checkpointer")

            cls._instance = AsyncPostgresSaver.from_conn_string(
                conn_string=settings.DATABASE_URL
            )

            # 初始化数据库表
            await cls._instance.setup()

            logger.info("[Checkpointer] 初始化完成")

        return cls._instance

    @classmethod
    async def close(cls):
        """关闭连接"""
        if cls._instance:
            await cls._instance.close()
            cls._instance = None
```

### Step 3: 修改 Agent 初始化

```python
# backend/app/services/agent/langgraph_agent.py

class WritingAgentGraph:
    def __init__(self, ai_service: HTTPAIService, use_chatgpt: bool = False):
        self.ai_service = ai_service
        self.use_chatgpt = use_chatgpt

        # 设置全局 AI Service
        set_global_ai_service(ai_service)

        # 初始化模式
        if use_chatgpt:
            logger.info("[LangGraph] 使用 ChatOpenAI 模式")
            self._init_chatgpt_mode()
        else:
            logger.info("[LangGraph] 使用 HTTPAIService 模式")
            self.llm = None
            self.llm_with_tools = None

        # ⭐ 修改：使用异步初始化 Checkpointer
        self.checkpointer = None  # 延迟初始化

        # 构建图（不传 checkpointer）
        self._graph = self._build_graph()

    async def _ensure_checkpointer(self):
        """确保 Checkpointer 已初始化"""
        if self.checkpointer is None:
            from app.services.agent.checkpointer import CheckpointerFactory
            self.checkpointer = await CheckpointerFactory.get_checkpointer()

    async def chat(self, message: str, work_id: str, chapter_id: str,
                   conversation_id: str, context: Dict):
        """对话接口"""

        # 确保 Checkpointer 初始化
        await self._ensure_checkpointer()

        # 编译图（带 Checkpointer）
        graph = self._graph.compile(checkpointer=self.checkpointer)

        # 执行...
```

### Step 4: 使用 Thread ID 管理会话

```python
# backend/app/api/v1/agent.py

@router.post("/chat/stream")
async def agent_chat_stream(
    request: AgentChatRequest,
    current_user: User = Depends(get_current_active_user),
    ai_service: HTTPAIService = Depends(get_ai_service),
    memory: MemoryManager = Depends(get_memory),
    db: AsyncSession = Depends(get_db)
):
    """Agent 对话流式响应"""

    user_id = str(current_user.id)

    # ⭐ 使用 conversation_id 作为 thread_id
    thread_id = request.conversation_id or str(uuid.uuid4())

    # 创建 Agent
    agent_graph = WritingAgentGraph(ai_service, use_chatgpt=settings.AGENT_USE_CHATGPT)

    # 配置 RunnableConfig（指定 thread_id）
    config = {
        "configurable": {
            "thread_id": thread_id,  # 会话线程 ID
            "user_id": user_id       # 用户 ID（可选）
        }
    }

    async def generate():
        try:
            # 调用 Agent（会自动保存 checkpoint）
            async for event in agent_graph.stream(
                message=request.message,
                work_id=request.work_id,
                chapter_id=request.chapter_id,
                context=context,
                config=config  # ⭐ 传入配置
            ):
                yield f"data: {json.dumps(event, ensure_ascii=False)}\n\n"
        except Exception as e:
            logger.error(f"[Stream] Error: {e}")
            yield f"data: {json.dumps({'error': str(e)}, ensure_ascii=False)}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")
```

---

## 📊 数据库表结构

PostgresSaver 会自动创建以下表：

```sql
-- Checkpoints 表（保存状态快照）
CREATE TABLE IF NOT EXISTS checkpoints (
    thread_id TEXT NOT NULL,
    checkpoint_id TEXT NOT NULL,
    parent_id TEXT,
    checkpoint JSONB NOT NULL,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (thread_id, checkpoint_id)
);

-- Writes 表（保存写入操作）
CREATE TABLE IF NOT EXISTS checkpoint_writes (
    thread_id TEXT NOT NULL,
    checkpoint_id TEXT NOT NULL,
    task_id TEXT NOT NULL,
    idx INTEGER NOT NULL,
    channel TEXT NOT NULL,
    value JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (thread_id, checkpoint_id, task_id, idx)
);

-- 索引优化
CREATE INDEX idx_checkpoints_thread_id ON checkpoints(thread_id);
CREATE INDEX idx_checkpoint_writes_thread_id ON checkpoint_writes(thread_id);
```

---

## 🎨 使用示例

### 场景 1: 继续之前的对话

```python
# 用户第一次对话
response1 = await agent.chat(
    message="帮我写第三章",
    conversation_id="conv_123",  # 指定会话 ID
    ...
)

# 几天后，用户继续对话（使用相同 conversation_id）
response2 = await agent.chat(
    message="继续写下去",
    conversation_id="conv_123",  # ⭐ 相同 ID，自动加载历史
    ...
)
# Agent 会记住之前的上下文和状态
```

### 场景 2: 从失败中恢复

```python
try:
    result = await agent.chat(
        message="生成 5000 字小说大纲",
        conversation_id="conv_456",
        ...
    )
except Exception as e:
    # 如果失败，可以从最后一个 checkpoint 恢复
    logger.error(f"Agent 失败: {e}")

    # 重试（会从最后一个成功的 checkpoint 继续）
    result = await agent.chat(
        message="继续",  # 继续之前的任务
        conversation_id="conv_456",
        ...
    )
```

### 场景 3: 查看历史状态

```python
# 获取会话的所有 checkpoints
async def get_conversation_history(thread_id: str):
    checkpointer = await CheckpointerFactory.get_checkpointer()

    # 列出所有 checkpoint
    checkpoints = await checkpointer.list({"configurable": {"thread_id": thread_id}})

    for checkpoint in checkpoints:
        print(f"Checkpoint ID: {checkpoint['checkpoint_id']}")
        print(f"Parent ID: {checkpoint['parent_id']}")
        print(f"State: {checkpoint['checkpoint']}")
        print(f"Created At: {checkpoint['created_at']}")
        print("---")
```

---

## 🔍 高级特性

### 1. 自定义 Checkpoint 元数据

```python
config = {
    "configurable": {
        "thread_id": conversation_id,
        "checkpoint_metadata": {
            "user_id": user_id,
            "work_id": work_id,
            "chapter_id": chapter_id,
            "intent": "writing",
            "tags": ["novel", "chapter3"]
        }
    }
}
```

### 2. 手动保存 Checkpoint

```python
# 在关键节点手动保存
async def writing_agent_with_checkpoints(state: AgentState):
    # 执行写作
    result = await generate_content(state)

    # 更新状态
    state["generated_content"] = result

    # LangGraph 会自动在每个 superstep 后保存 checkpoint
    # 无需手动调用

    return state
```

### 3. 清理过期 Checkpoints

```python
# backend/app/tasks/cleanup_checkpoints.py
async def cleanup_old_checkpoints(days: int = 90):
    """清理 N 天前的 checkpoints"""

    async with AsyncSessionLocal() as db:
        cutoff_date = datetime.now() - timedelta(days=days)

        await db.execute(
            "DELETE FROM checkpoints WHERE created_at < :cutoff",
            {"cutoff": cutoff_date}
        )

        await db.execute(
            "DELETE FROM checkpoint_writes WHERE created_at < :cutoff",
            {"cutoff": cutoff_date}
        )

        await db.commit()
        logger.info(f"[Cleanup] 清理了 {days} 天前的 checkpoints")
```

---

## ✅ 验证测试

### 测试脚本

```python
# tests/test_persistent_memory.py
import pytest
from app.services.agent.langgraph_agent import WritingAgentGraph
from app.services.ai.http_ai_service import HTTPAIService

@pytest.mark.asyncio
async def test_persistent_memory():
    """测试持久化记忆"""

    ai_service = HTTPAIService()
    agent = WritingAgentGraph(ai_service, use_chatgpt=True)

    conversation_id = "test_conv_001"

    # 第一次对话
    result1 = await agent.chat(
        message="记住：我喜欢写玄幻小说",
        conversation_id=conversation_id,
        work_id="test_work",
        chapter_id="test_chapter",
        context={}
    )

    assert "记住" in result1["response"]

    # 重新创建 Agent（模拟服务重启）
    agent2 = WritingAgentGraph(ai_service, use_chatgpt=True)

    # 第二次对话（使用相同 conversation_id）
    result2 = await agent2.chat(
        message="我喜欢什么类型的小说？",
        conversation_id=conversation_id,
        work_id="test_work",
        chapter_id="test_chapter",
        context={}
    )

    # 验证 Agent 记住了之前的对话
    assert "玄幻" in result2["response"]
```

---

## 📈 性能优化

### 1. 连接池配置

```python
# backend/app/core/config.py
class Settings(BaseSettings):
    # PostgreSQL 连接池配置
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 10
    DATABASE_POOL_TIMEOUT: int = 30
```

### 2. Checkpoint 压缩

```python
# 对于大状态，考虑压缩
import gzip
import json

def compress_state(state: dict) -> bytes:
    json_str = json.dumps(state)
    return gzip.compress(json_str.encode())

def decompress_state(data: bytes) -> dict:
    json_str = gzip.decompress(data).decode()
    return json.loads(json_str)
```

### 3. 批量清理

```python
# 定期清理（Celery 任务）
from celery import Celery
from celery.schedules import crontab

app = Celery('tasks')

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # 每天凌晨 3 点清理
    sender.add_periodic_task(
        crontab(hour=3, minute=0),
        cleanup_old_checkpoints.s(days=90)
    )
```

---

## 🚀 部署建议

### 开发环境

```python
# 使用 SQLite（快速测试）
from langgraph.checkpoint.sqlite import AsyncSqliteSaver

checkpointer = AsyncSqliteSaver.from_conn_string("./checkpoints.db")
```

### 生产环境

```python
# 使用 PostgreSQL（高性能）
from langgraph.checkpoint.postgres import AsyncPostgresSaver

checkpointer = AsyncPostgresSaver.from_conn_string(
    settings.DATABASE_URL,
    pool_size=20,
    max_overflow=10
)
```

---

## 📚 参考资源

- **LangGraph Persistence 文档**：https://langchain-ai.github.io/langgraph/concepts/persistence/
- **PostgresSaver API**：https://langchain-ai.github.io/langgraph/reference/checkpointers/#postgresconfiguration
- **Memory Tutorial**：https://langchain-ai.github.io/langgraph/how-tos/memory/add-memory/

---

## ✅ 完成标准

- [ ] PostgresSaver 实现并测试通过
- [ ] 会话持久化验证
- [ ] 服务重启后会话恢复测试
- [ ] 性能基准测试（响应时间 < 100ms）
- [ ] 数据库索引优化
- [ ] 清理任务部署
- [ ] 文档更新

---

**下一步**：实施完成后，继续 [Hierarchical Supervisor 架构](./02-hierarchical-supervisor.md)
