# 记忆系统集成

## 文档版本
- 版本：1.1
- 日期：2025-12-19
- 更新：修正 AgentMiddleware 基类，移除 ToolRuntime 依赖

---

## 一、现有记忆系统概述

### 1.1 三层记忆架构

```
┌─────────────────────────────────────────────────────────┐
│                   现有记忆系统                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │           Short-term Memory (短期)              │   │
│  │  - 最近 10 条消息                                │   │
│  │  - 存储在 Redis                                 │   │
│  │  - TTL: 会话级                                  │   │
│  └─────────────────────────────────────────────────┘   │
│                         ↓                              │
│  ┌─────────────────────────────────────────────────┐   │
│  │           Medium-term Memory (中期)             │   │
│  │  - 最近 100 条消息摘要                          │   │
│  │  - 存储在 Redis                                 │   │
│  │  - TTL: 7 天                                    │   │
│  └─────────────────────────────────────────────────┘   │
│                         ↓                              │
│  ┌─────────────────────────────────────────────────┐   │
│  │           Long-term Memory (长期)               │   │
│  │  - 语义向量存储                                  │   │
│  │  - ChromaDB + sentence-transformers            │   │
│  │  - 支持相似性检索                               │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 1.2 相关文件

| 文件 | 功能 | 行数 |
|------|------|------|
| `memory/enhanced_memory_manager.py` | 增强记忆管理器 | ~500 |
| `memory/long_term_memory.py` | 长期记忆 | ~300 |
| `memory/long_term_store.py` | 长期存储 | ~200 |
| `memory/unified_coordinator.py` | 统一协调器 | ~400 |
| `context/vector_memory_store.py` | 向量存储 | ~350 |
| `context/manager.py` | 上下文管理器 | ~600 |

### 1.3 核心类

```python
# EnhancedMemoryManager
class EnhancedMemoryManager:
    """三层记忆管理器"""

    def __init__(self, redis_client):
        self.short_term = ShortTermMemory(redis_client)
        self.medium_term = MediumTermMemory(redis_client)
        self.long_term = LongTermMemory()

    async def remember(self, user_id, work_id, message, importance=0.5):
        """记住一条消息"""
        # 存入短期
        await self.short_term.add(user_id, work_id, message)
        # 重要消息存入中期
        if importance > 0.7:
            await self.medium_term.add(user_id, work_id, message)
        # 非常重要存入长期
        if importance > 0.9:
            await self.long_term.add(user_id, work_id, message)

    async def recall(self, user_id, work_id, query, limit=10):
        """回忆相关信息"""
        results = []
        results += await self.short_term.get_recent(user_id, work_id, 5)
        results += await self.medium_term.search(user_id, work_id, query, 3)
        results += await self.long_term.search(user_id, work_id, query, 2)
        return results[:limit]
```

---

## 二、Deep Agents 记忆系统

### 2.1 内置 Store

```python
from langgraph.store import InMemoryStore

# Deep Agents 使用 Store 进行跨线程存储
store = InMemoryStore()

# 存储数据
store.put(
    namespace=("users", "user_123", "preferences"),
    key="writing_style",
    value={"style": "幽默", "tone": "轻松"}
)

# 读取数据
data = store.get(("users", "user_123", "preferences"), "writing_style")
```

### 2.2 局限性

| 方面 | Deep Agents Store | 我们的记忆系统 |
|------|-------------------|----------------|
| 存储后端 | 内存/简单持久化 | Redis + ChromaDB |
| 检索方式 | Key-Value | 语义相似性 |
| 分层管理 | ❌ 无 | ✅ 三层 |
| 自动遗忘 | ❌ 无 | ✅ 有 |
| 重要度评分 | ❌ 无 | ✅ 有 |

---

## 三、集成方案

### 3.1 自定义 MemoryMiddleware

```python
# middleware/memory_middleware.py

from langchain.tools import tool
from app.services.agent.memory import EnhancedMemoryManager

# 伪代码：AgentMiddleware 为约定接口
class AgentMiddleware:
    pass

class MemoryMiddleware(AgentMiddleware):
    """将三层记忆系统集成到 Deep Agents - 继承 AgentMiddleware"""

    def __init__(self, redis_client):
        self.memory_manager = EnhancedMemoryManager(redis_client)

    def get_tools(self):
        """返回记忆相关工具"""
        return [
            self._create_remember_tool(),
            self._create_recall_tool(),
            self._create_forget_tool(),
        ]

    def _create_remember_tool(self):
        """创建记忆工具"""
        memory_manager = self.memory_manager

        def remember_tool(
            content: str,
            importance: float = 0.5,
            tags: str = ""
        ) -> str:
            """记住重要信息

            Args:
                content: 要记住的内容
                importance: 重要程度 (0-1)
                tags: 标签，逗号分隔
            """
            # 从全局上下文获取 user_id 和 work_id
            from app.core.context import get_current_context
            ctx = get_current_context()

            tag_list = [t.strip() for t in tags.split(",") if t.strip()]

            memory_manager.remember_sync(
                user_id=ctx.user_id,
                work_id=ctx.work_id,
                message=content,
                importance=importance,
                tags=tag_list
            )

            return f"已记住：{content[:50]}..."

        return remember_tool

    def _create_recall_tool(self):
        """创建回忆工具"""
        memory_manager = self.memory_manager

        def recall_tool(query: str, limit: int = 5) -> str:
            """回忆相关信息

            Args:
                query: 查询内容
                limit: 返回数量
            """
            from app.core.context import get_current_context
            ctx = get_current_context()

            memories = memory_manager.recall_sync(
                user_id=ctx.user_id,
                work_id=ctx.work_id,
                query=query,
                limit=limit
            )

            if not memories:
                return "没有找到相关记忆"

            result = "找到以下相关记忆：\n"
            for i, mem in enumerate(memories, 1):
                result += f"{i}. {mem['content'][:100]}...\n"

            return result

        return recall_tool

    def _create_forget_tool(self):
        """创建遗忘工具"""
        memory_manager = self.memory_manager

        def forget_tool(query: str) -> str:
            """遗忘特定信息

            Args:
                query: 要遗忘的内容描述
            """
            from app.core.context import get_current_context
            ctx = get_current_context()

            count = memory_manager.forget_sync(
                user_id=ctx.user_id,
                work_id=ctx.work_id,
                query=query
            )

            return f"已遗忘 {count} 条相关记忆"

        return forget_tool
```

### 3.2 Store 适配器

Deep Agents 使用 LangGraph 的 Store API，我们可以创建适配器：

```python
# middleware/store_adapter.py

from langgraph.store import BaseStore
from typing import Optional
import json

class EnhancedMemoryStore(BaseStore):
    """将 EnhancedMemoryManager 适配为 LangGraph Store 接口"""

    def __init__(self, memory_manager):
        self.memory = memory_manager

    def put(self, namespace: tuple, key: str, value: dict):
        """存储数据到记忆系统"""
        user_id, work_id = self._parse_namespace(namespace)
        importance = value.get("importance", 0.5)

        self.memory.remember_sync(
            user_id=user_id,
            work_id=work_id,
            message=json.dumps({"key": key, "value": value}),
            importance=importance
        )

    def get(self, namespace: tuple, key: str) -> Optional[dict]:
        """从记忆系统获取数据"""
        user_id, work_id = self._parse_namespace(namespace)

        memories = self.memory.recall_sync(
            user_id=user_id,
            work_id=work_id,
            query=key,
            limit=1
        )

        if memories:
            try:
                data = json.loads(memories[0]["content"])
                if data.get("key") == key:
                    return data.get("value")
            except json.JSONDecodeError:
                pass

        return None

    def search(self, namespace: tuple, query: str, limit: int = 10):
        """语义搜索记忆"""
        user_id, work_id = self._parse_namespace(namespace)

        return self.memory.recall_sync(
            user_id=user_id,
            work_id=work_id,
            query=query,
            limit=limit
        )

    def _parse_namespace(self, namespace: tuple):
        """解析 namespace 获取 user_id 和 work_id"""
        user_id = namespace[0] if len(namespace) > 0 else None
        work_id = namespace[1] if len(namespace) > 1 else None
        return user_id, work_id
```

### 3.3 消息历史同步

```python
# middleware/history_sync.py

# 伪代码：AgentMiddleware 为约定接口
class AgentMiddleware:
    pass

class HistorySyncMiddleware(AgentMiddleware):
    """同步消息历史到记忆系统 - 继承 AgentMiddleware"""

    def __init__(self, memory_manager):
        self.memory = memory_manager

    def on_message(self, message, state, config):
        """消息钩子 - 每条消息都同步到记忆"""
        user_id = config.get("configurable", {}).get("user_id")
        work_id = state.get("work_id")

        # 判断消息重要度
        importance = self._calculate_importance(message)

        # 存储到记忆系统
        self.memory.remember_sync(
            user_id=user_id,
            work_id=work_id,
            message=message.content if hasattr(message, 'content') else str(message),
            importance=importance,
            metadata={
                "role": getattr(message, 'role', 'unknown'),
                "timestamp": datetime.now().isoformat()
            }
        )

    def _calculate_importance(self, message) -> float:
        """计算消息重要度"""
        content = str(message.content if hasattr(message, 'content') else message).lower()

        # 包含关键决策的消息更重要
        if any(kw in content for kw in ["确定", "决定", "选择", "修改"]):
            return 0.9

        # 包含创作内容的消息较重要
        if any(kw in content for kw in ["写", "改", "续", "生成"]):
            return 0.7

        # 普通对话
        return 0.5
```

---

## 四、上下文管理集成

### 4.1 ContextMiddleware

```python
# middleware/context_middleware.py

from app.services.context import ContextManager

# 伪代码：AgentMiddleware 为约定接口
class AgentMiddleware:
    pass

class ContextMiddleware(AgentMiddleware):
    """上下文管理中间件 - 继承 AgentMiddleware"""

    def __init__(self, ai_service):
        self.context_manager = ContextManager(
            ai_service=ai_service,
            enable_long_term_memory=True,
            enable_adaptive_budget=True
        )

    def before_invoke(self, state, config):
        """调用前 - 加载上下文"""
        configurable = config.get("configurable", {})
        user_id = configurable.get("user_id")
        work_id = state.get("work_id")
        thread_id = configurable.get("thread_id")

        # 加载上下文
        context = self.context_manager.load_context_sync(
            user_id=user_id,
            work_id=work_id,
            conversation_id=thread_id
        )

        # 注入到状态
        state["loaded_context"] = context
        return state

    def after_invoke(self, state, result, config):
        """调用后 - 保存上下文"""
        configurable = config.get("configurable", {})
        user_id = configurable.get("user_id")
        work_id = state.get("work_id")
        thread_id = configurable.get("thread_id")

        # 保存上下文
        self.context_manager.save_context_sync(
            user_id=user_id,
            work_id=work_id,
            conversation_id=thread_id,
            messages=state.get("messages", [])
        )

        return result

    def get_tools(self):
        """提供上下文相关工具"""
        return [self._create_context_summary_tool()]

    def _create_context_summary_tool(self):
        """创建上下文摘要工具"""
        def get_context_summary() -> str:
            """获取当前上下文摘要"""
            from app.core.context import get_current_context
            ctx = get_current_context()

            summary = "当前上下文：\n"
            summary += f"- 作品ID: {ctx.work_id or '未设置'}\n"
            summary += f"- 章节ID: {ctx.chapter_id or '未设置'}\n"
            summary += f"- 用户ID: {ctx.user_id or '未设置'}\n"

            return summary

        return get_context_summary
```

### 4.2 Token 预算管理

```python
# middleware/budget_middleware.py

from app.services.context.adaptive_budget import AdaptiveBudget

# 伪代码：AgentMiddleware 为约定接口
class AgentMiddleware:
    pass

class BudgetMiddleware(AgentMiddleware):
    """Token 预算管理中间件 - 继承 AgentMiddleware"""

    def __init__(self, total_budget=16000):
        self.budget = AdaptiveBudget(total=total_budget)

    def before_invoke(self, state, config):
        """计算可用预算"""
        messages = state.get("messages", [])
        task_type = state.get("task_type", "general")

        # 计算已用 token
        used_tokens = self._count_tokens(messages)

        # 获取自适应预算
        available = self.budget.get_available(
            task_type=task_type,
            used=used_tokens
        )

        state["token_budget"] = available
        return state

    def _count_tokens(self, messages) -> int:
        """计算消息的 token 数"""
        total = 0
        for msg in messages:
            content = msg.content if hasattr(msg, 'content') else str(msg)
            # 简单估算：中文约 0.5 token/字，英文约 0.25 token/字
            total += len(content) * 0.5
        return int(total)
```

---

## 五、统一协调器

### 5.1 整合所有记忆组件

```python
# middleware/unified_memory.py

# 伪代码：AgentMiddleware 为约定接口
class AgentMiddleware:
    pass

class UnifiedMemoryMiddleware(AgentMiddleware):
    """统一记忆协调中间件 - 整合所有记忆组件"""

    def __init__(self, redis_client, ai_service, checkpointer):
        from app.services.agent.memory import EnhancedMemoryManager

        # 初始化各组件
        self.memory_manager = EnhancedMemoryManager(redis_client)
        self.checkpointer = checkpointer

        # 子中间件
        self.memory_mw = MemoryMiddleware(redis_client)
        self.context_mw = ContextMiddleware(ai_service)
        self.history_mw = HistorySyncMiddleware(self.memory_manager)
        self.budget_mw = BudgetMiddleware()

    def get_tools(self):
        """合并所有工具"""
        tools = []
        tools.extend(self.memory_mw.get_tools())
        tools.extend(self.context_mw.get_tools())
        return tools

    def before_invoke(self, state, config):
        """调用前处理"""
        state = self.context_mw.before_invoke(state, config)
        state = self.budget_mw.before_invoke(state, config)
        return state

    def after_invoke(self, state, result, config):
        """调用后处理"""
        result = self.context_mw.after_invoke(state, result, config)
        return result

    def on_message(self, message, state, config):
        """消息钩子"""
        self.history_mw.on_message(message, state, config)
```

---

## 六、使用示例

### 6.1 创建带记忆的 Agent

```python
# writing_agent.py（伪代码）
from .middleware.unified_memory import UnifiedMemoryMiddleware

def create_writing_agent(
    redis_client,
    ai_service,
    checkpointer
):
    # 创建统一记忆中间件
    memory_middleware = UnifiedMemoryMiddleware(
        redis_client=redis_client,
        ai_service=ai_service,
        checkpointer=checkpointer
    )

    return build_agent_graph(
        tools=[...],
        system_prompt="...",
        middleware=[memory_middleware],
        checkpointer=checkpointer,
        # 使用自定义 Store
        store=EnhancedMemoryStore(memory_middleware.memory_manager)
    )
```

### 6.2 工具中使用记忆

```python
def write_with_memory(prompt: str) -> str:
    """基于记忆的写作

    Args:
        prompt: 写作提示
    """
    from app.core.context import get_current_context
    from app.services.agent.memory import get_memory_manager

    # 获取当前上下文
    ctx = get_current_context()
    memory_manager = get_memory_manager()

    # 检索相关记忆
    memories = memory_manager.recall_sync(
        user_id=ctx.user_id,
        work_id=ctx.work_id,
        query=prompt,
        limit=5
    )

    # 构建上下文
    context = "相关历史信息：\n"
    for mem in memories:
        context += f"- {mem['content']}\n"

    # 生成内容
    result = generate_content(prompt, context)

    # 记住这次创作
    memory_manager.remember_sync(
        user_id=ctx.user_id,
        work_id=ctx.work_id,
        message=f"创作: {prompt[:50]}... -> {result[:100]}...",
        importance=0.7
    )

    return result
```

---

## 七、测试方案

### 7.1 单元测试

```python
@pytest.mark.asyncio
async def test_memory_middleware():
    """测试记忆中间件"""
    redis = MockRedis()
    middleware = MemoryMiddleware(redis)

    # 模拟 runtime
    runtime = Mock()
    runtime.context = {"user_id": "user_1"}
    runtime.state = {"work_id": "work_1"}

    # 测试记忆
    result = await middleware.remember_tool(
        content="测试内容",
        importance=0.8,
        runtime=runtime
    )
    assert "已记住" in result

    # 测试回忆
    result = await middleware.recall_tool(
        query="测试",
        runtime=runtime
    )
    assert "测试内容" in result or "没有找到" in result
```

### 7.2 集成测试

```python
@pytest.mark.asyncio
async def test_memory_in_agent():
    """测试记忆在 Agent 中的工作"""
    agent = create_writing_agent(...)

    # 第一次对话
    result1 = await agent.ainvoke({
        "messages": [{"role": "user", "content": "我喜欢幽默风格"}]
    }, config={"thread_id": "test"})

    # 第二次对话 - 应该记住偏好
    result2 = await agent.ainvoke({
        "messages": [{"role": "user", "content": "帮我写一段对话"}]
    }, config={"thread_id": "test"})

    # 验证记忆被使用
    assert "幽默" in result2["messages"][-1].content
```

---

## 八、迁移检查清单

- [ ] MemoryMiddleware 开发完成
- [ ] EnhancedMemoryStore 适配完成
- [ ] ContextMiddleware 开发完成
- [ ] HistorySyncMiddleware 开发完成
- [ ] BudgetMiddleware 开发完成
- [ ] UnifiedMemoryMiddleware 整合完成
- [ ] 单元测试通过
- [ ] 集成测试通过
- [ ] 性能测试通过（记忆检索 < 100ms）

---

## 九、下一步

阅读 `06-interrupt-resume.md` 了解如何实现中断恢复机制。
