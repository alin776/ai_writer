# Deep Agents 核心概念

## 文档版本
- 版本：1.2
- 日期：2025-12-22
- 更新：API 验证确认，补充实际导出和参数说明

---

## 〇、API 验证结果（2025-12-22）

> 以下 API 已通过实际安装 `deepagents==0.3.0` 验证：

| API | 验证结果 | 位置 |
|-----|----------|------|
| `create_deep_agent()` | ✅ 存在 | `deepagents` |
| `FilesystemMiddleware` | ✅ 存在 | `deepagents.middleware` |
| `SubAgentMiddleware` | ✅ 存在 | `deepagents.middleware` |
| `AgentMiddleware` | ✅ 存在 | `langchain.agents.middleware.types` |
| `interrupt_on` 参数 | ✅ 支持 | `create_deep_agent()` 参数 |
| `InterruptOnConfig` | ✅ 存在 | `langchain.agents.middleware.human_in_the_loop` |
| `ToolRuntime` | ✅ 存在 | `langgraph.prebuilt.tool_node` |
| `interrupt` / `Command` | ✅ 存在 | `langgraph.types` |

**实际可用的顶层导出：**
```python
from deepagents import (
    create_deep_agent,      # 创建 Agent
    FilesystemMiddleware,   # 文件系统中间件
    SubAgentMiddleware,     # 子代理中间件
    SubAgent,               # 子代理定义
    CompiledSubAgent,       # 编译后的子代理
)

from deepagents.backends import (
    BackendProtocol,        # 后端协议
    CompositeBackend,       # 组合后端
    FilesystemBackend,      # 文件系统后端
    StateBackend,           # 状态后端
    StoreBackend,           # 存储后端
)
```

---

## 一、Deep Agents 简介

### 1.1 什么是 Deep Agents

Deep Agents 是 LangChain 官方基于 LangGraph 构建的独立库，专门用于处理**复杂、多步骤任务**的智能代理。

```
Deep Agents = LangGraph + 中间件系统 + interrupt/resume + 最佳实践
```

### 1.2 核心设计理念

| 理念 | 说明 |
|------|------|
| **任务规划** | 内置 `write_todos` 工具，支持任务分解和进度跟踪 |
| **上下文管理** | 通过文件系统工具防止上下文溢出 |
| **子代理派生** | `task` 工具创建独立上下文的子代理 |
| **人机协同** | 原生 `interrupt/resume` 机制 |

### 1.3 安装

```bash
pip install deepagents tavily-python
```

> 注意：tavily-python 是可选的，用于网络搜索功能。

---

## 二、核心 API

### 2.1 create_deep_agent

最简单的使用方式：

```python
from deepagents import create_deep_agent
from langchain.chat_models import init_chat_model

# 定义自定义工具（普通 Python 函数）
def my_tool(query: str) -> str:
    """工具描述"""
    return f"处理结果: {query}"

# 创建 Agent（默认使用 claude-sonnet-4-5-20250929）
agent = create_deep_agent(
    tools=[my_tool],
    system_prompt="你是一个写作助手..."
)

# 也可以指定其他模型
model = init_chat_model("openai:gpt-4o")
agent = create_deep_agent(
    model=model,
    tools=[my_tool],
    system_prompt="你是一个写作助手..."
)

# 执行
result = agent.invoke({
    "messages": [{"role": "user", "content": "帮我写一个大纲"}]
})
```

### 2.2 自动包含的工具

创建 Agent 时，Deep Agents 自动添加以下工具：

| 工具 | 功能 |
|------|------|
| `write_todos` / `read_todos` | 更新/读取任务列表，跟踪进度 |
| `ls` | 列出文件目录 |
| `read_file` | 读取文件内容 |
| `write_file` | 创建新文件 |
| `edit_file` | 修改现有文件 |
| `glob` | 模式匹配搜索文件 |
| `grep` | 内容搜索 |
| `execute` | 执行命令（需要 SandboxBackend） |
| `task` | 派生子代理执行特定任务 |

---

## 三、中间件系统

### 3.1 内置中间件

```
┌─────────────────────────────────────────┐
│           Deep Agents Core              │
└─────────────────────────────────────────┘
                   ↓
┌─────────────┬─────────────┬─────────────┐
│ TodoList    │ Filesystem  │  SubAgent   │
│ Middleware  │ Middleware  │ Middleware  │
├─────────────┼─────────────┼─────────────┤
│Summarizaton │ HumanInThe  │             │
│ Middleware  │LoopMiddlware│             │
└─────────────┴─────────────┴─────────────┘
```

**内置中间件说明：**
- **TodoListMiddleware**: 提供 `write_todos`/`read_todos` 工具
- **FilesystemMiddleware**: 提供文件操作工具
- **SubAgentMiddleware**: 提供 `task` 工具
- **SummarizationMiddleware**: 在 170k tokens 时自动摘要
- **HumanInTheLoopMiddleware**: 人机协同审批

#### TodoListMiddleware

```python
# 提供 write_todos 工具
# 让 Agent 能够：
# - 分解复杂任务
# - 跟踪执行进度
# - 动态调整计划

# 示例：Agent 自动生成的 todos
{
    "todos": [
        {"id": 1, "task": "读取章节内容", "status": "completed"},
        {"id": 2, "task": "分析人物关系", "status": "in_progress"},
        {"id": 3, "task": "生成改进建议", "status": "pending"}
    ]
}
```

#### FilesystemMiddleware

```python
# 提供文件操作工具
# 解决上下文溢出问题

# 工具列表
- ls(path)           # 列出目录
- read_file(path)    # 读取文件
- write_file(path, content)  # 写入文件
- edit_file(path, edits)     # 编辑文件
- glob(pattern)      # 模式匹配
- grep(pattern)      # 内容搜索
```

#### SubAgentMiddleware

```python
# 提供 task 工具
# 支持子代理派生

# 使用示例
result = task(
    name="analysis_agent",
    description="分析章节内容",
    system_prompt="你是文本分析专家...",
    tools=[analyze_text]
)
```

### 3.2 自定义中间件

```python
from deepagents import AgentMiddleware

class MyCustomMiddleware(AgentMiddleware):
    """自定义中间件 - 继承 AgentMiddleware"""

    def get_tools(self):
        """返回此中间件提供的工具"""
        return [self.my_custom_tool]

    def my_custom_tool(self, param: str) -> str:
        """自定义工具"""
        return f"处理: {param}"

# 注册到 Agent
agent = create_deep_agent(
    tools=[...],
    middleware=[MyCustomMiddleware()]
)
```

---

## 四、interrupt/resume 机制

### 4.1 核心概念

Deep Agents 通过 `interrupt_on` 参数和 `HumanInTheLoopMiddleware` 实现人机协同：

```python
from langgraph.types import interrupt, Command

# interrupt: 暂停执行，等待外部输入
# Command(resume=...): 恢复执行，传入用户响应
```

### 4.2 使用方式

**方式一：通过 interrupt_on 参数配置（推荐）**

```python
# 配置哪些工具需要人工确认
agent = create_deep_agent(
    tools=[smart_rewrite, dangerous_operation],
    interrupt_on={
        "smart_rewrite": {
            "allowed_decisions": ["approve", "edit", "reject"]
        },
        "dangerous_operation": True  # 简单配置
    }
)

# 执行时会在指定工具前暂停
result = agent.invoke(
    {"messages": [...]},
    config={"configurable": {"thread_id": "xxx"}}
)

# 检查是否被中断
if result.get("__interrupt__"):
    # 等待用户响应后恢复
    result = agent.invoke(
        None,
        config={"configurable": {"thread_id": "xxx"}},
        command=Command(resume="approve")
    )
```

**方式二：在节点中使用 interrupt（底层机制）**

```python
from langgraph.types import interrupt

# 这是 LangGraph 原生的 interrupt，Deep Agents 内部使用
# 一般用户不需要直接调用
def my_node(state):
    response = interrupt({
        "type": "confirmation",
        "question": "是否继续？"
    })
    # 用户响应后继续执行
    return {"response": response}
```

### 4.3 恢复执行

```python
from langgraph.types import Command

# 用户提交响应后恢复执行
result = agent.invoke(
    None,  # 不需要新消息，使用 None
    config={"configurable": {"thread_id": "xxx"}},
    command=Command(resume="approve")  # 或其他响应
)
```

### 4.4 与现有 HITL 对比

| 特性 | 现有 HITL | interrupt/resume |
|------|-----------|------------------|
| 等待机制 | 轮询 Redis | 原生阻塞 |
| 延迟 | 2-5 秒 | < 100ms |
| 触发点 | 特定工具 | 任意位置 |
| 灵活性 | 低 | 高 |

---

## 五、状态管理

### 5.1 Checkpointer

```python
from langgraph.checkpoint.redis import AsyncRedisSaver

# 创建持久化检查点
checkpointer = AsyncRedisSaver(
    redis_url="redis://localhost:6379",
    ttl={"default_ttl": 10080}  # 7天
)

agent = create_deep_agent(
    tools=[...],
    checkpointer=checkpointer
)
```

### 5.2 Thread 管理

```python
# 每个对话使用唯一的 thread_id
config = {"configurable": {"thread_id": "user_123_conversation_456"}}

# 同一 thread_id 保持对话上下文
result1 = agent.invoke({"messages": [msg1]}, config=config)
result2 = agent.invoke({"messages": [msg2]}, config=config)  # 保持上下文
```

### 5.3 Store (长期记忆)

```python
from langgraph.store import InMemoryStore

# 创建存储
store = InMemoryStore()

# 跨线程存储数据
store.put(
    namespace=("users", "user_123"),
    key="preferences",
    value={"style": "幽默"}
)

# 读取数据
prefs = store.get(("users", "user_123"), "preferences")
```

---

## 六、工具定义

### 6.1 基础工具

Deep Agents 支持多种工具定义方式：

**方式一：普通 Python 函数（推荐）**

```python
def analyze_text(text: str, focus: str = "综合分析") -> str:
    """分析文本内容

    Args:
        text: 要分析的文本
        focus: 分析焦点（如"人物关系"、"情节结构"）

    Returns:
        分析结果
    """
    # 实现分析逻辑
    return f"分析 {focus}: ..."
```

**方式二：使用 @tool 装饰器**

```python
from langchain.tools import tool

@tool
def analyze_text(text: str, focus: str = "综合分析") -> str:
    """分析文本内容

    Args:
        text: 要分析的文本
        focus: 分析焦点

    Returns:
        分析结果
    """
    return f"分析 {focus}: ..."
```

### 6.2 工具上下文访问

Deep Agents 工具通过以下方式访问上下文：

**方式一：依赖注入（全局服务）**

```python
# 在模块级别定义服务
from app.services.ai import get_ai_service

def get_chapter_content(chapter_id: str) -> str:
    """读取章节内容"""
    ai_service = get_ai_service()  # 全局服务
    return ai_service.fetch_chapter(chapter_id)
```

**方式二：通过 State 访问（在自定义节点中）**

```python
def my_custom_node(state):
    """自定义节点可以访问完整 state"""
    work_id = state.get("work_id")
    messages = state.get("messages")
    # ...
    return {"result": "..."}
```

### 6.3 返回 Command 的工具

```python
from langgraph.types import Command

def update_context(new_info: str) -> Command:
    """更新上下文信息 - 返回 Command 更新状态"""
    return Command(update={
        "context": {"new_info": new_info}
    })
```

---

## 七、流式处理

### 7.1 流式模式

```python
# 五种流式模式
async for event in agent.astream(
    {"messages": [...]},
    stream_mode=["values", "updates", "custom", "messages", "debug"]
):
    # values: 每步后完整状态
    # updates: 仅状态变更
    # custom: 自定义数据
    # messages: LLM token 流
    # debug: 完整执行跟踪
    pass
```

### 7.2 流式响应处理

```python
# 推荐的流式处理方式
async for event in agent.astream(
    {"messages": [{"role": "user", "content": "..."}]},
    stream_mode="values"
):
    if "__interrupt__" in event:
        # 处理中断
        print("需要用户确认:", event["__interrupt__"])
    else:
        # 处理正常响应
        messages = event.get("messages", [])
        if messages:
            print(messages[-1].content)
```

---

## 八、与 LangGraph 的关系

```
┌─────────────────────────────────────────────────────────┐
│                    Deep Agents                          │
│  ┌─────────────────────────────────────────────────┐   │
│  │              高级抽象层                          │   │
│  │  - create_deep_agent()                          │   │
│  │  - 中间件系统                                    │   │
│  │  - 最佳实践封装                                  │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                          ↓ 基于
┌─────────────────────────────────────────────────────────┐
│                     LangGraph                           │
│  ┌─────────────────────────────────────────────────┐   │
│  │              核心框架                            │   │
│  │  - StateGraph                                    │   │
│  │  - Checkpointer                                  │   │
│  │  - interrupt/resume                              │   │
│  │  - Store                                         │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                          ↓ 基于
┌─────────────────────────────────────────────────────────┐
│                    LangChain                            │
│  - 工具定义                                             │
│  - 消息类型                                             │
│  - 模型接口                                             │
└─────────────────────────────────────────────────────────┘
```

---

## 九、适用场景

### 9.1 适合使用 Deep Agents

- ✅ 复杂多步骤任务
- ✅ 需要用户中途干预
- ✅ 长时间运行的工作流
- ✅ 需要任务规划和跟踪
- ✅ 需要子代理协作

### 9.2 不适合使用 Deep Agents

- ❌ 简单的问答对话
- ❌ 单步操作
- ❌ 不需要持久化的场景

---

## 十、下一步

阅读 `03-migration-strategy.md` 了解如何将现有代码迁移到 Deep Agents。
