# P0-04: Planning组件复用清单 - 详细操作指南

## 📋 文档信息

**优先级**：P0（基础工作）
**预估工作量**：贯穿整个项目周期
**前置依赖**：[P0-00-代码现状诊断.md](./P0-00-代码现状诊断.md)
**后续任务**：所有P0-P3任务都会用到

---

## 🎯 文档目标

### 主要目标
1. ✅ 提供13个Planning组件的详细复用指南
2. ✅ 明确每个组件在哪个阶段、哪个任务中复用
3. ✅ 提供具体的代码示例和操作步骤
4. ✅ 识别复用过程中的风险和注意事项

### 使用说明
- ⚠️ **本文档基于P0-00诊断结果**，如果诊断结果与文档假设不符，必须先更新本文档
- 每个阶段开始前，复查对应组件的复用清单
- 复用完成后，在清单中标记完成状态

---

## 📊 复用组件总览

### 分类统计
```
类别1: 直接复用（6个）⭐⭐⭐⭐⭐
  ├─ 工具系统
  ├─ Checkpointer
  ├─ JSON解析器
  ├─ 重试机制
  ├─ Prompt模板库
  └─ 模型选择器

类别2: 适配复用（4个）🔧
  ├─ 进度回调机制
  ├─ 错误处理逻辑
  ├─ 上下文构建
  └─ AgentState结构

类别3: 设计思想复用（3个）💡
  ├─ 三阶段执行模式
  ├─ 智能并行执行
  └─ 结果聚合策略
```

### 复用时间线
```
P0阶段（Week 2-4）：
  ✅ 工具系统
  ✅ 模型选择器
  ✅ 重试机制

P1阶段（Week 6-8）：
  ✅ Checkpointer
  ✅ Prompt模板库
  🔧 AgentState结构
  🔧 进度回调机制
  🔧 上下文构建

P2阶段（Week 9）：
  🔧 错误处理逻辑
  💡 并行执行思想
  💡 结果聚合策略

随时可用：
  ✅ JSON解析器
```

---

## 🔥 类别1：直接复用组件（6个）

这些组件可以**零改动**直接复用，是复用的重点！

---

### 1.1 工具系统 ⭐⭐⭐⭐⭐

#### 📍 复用时机
**阶段**：P0阶段
**任务**：P0-02-统一工具系统
**Week**：Week 2

#### 📦 包含内容
基于P0-00诊断结果（假设验证通过）：
- 7个完整的工具
- _generate_text_helper辅助函数
- 工具参数验证逻辑
- 错误处理机制

#### 🎯 复用方式

**步骤1：导入Planning的工具**
```python
# 在Chat模式的代码中
from backend.app.services.agent.langgraph_agent import (
    continue_writing_tool,
    polish_text_tool,
    analyze_text_tool,
    get_context_tool,
    get_chapter_by_order_tool,
    read_chapter_tool,
    search_analysis_fragments_tool,
)
```

**步骤2：在Chat图中注册工具**
```python
# 在_build_chat_graph方法中
from langgraph.prebuilt import ToolNode

# 创建工具列表
all_tools = [
    continue_writing_tool,
    polish_text_tool,
    analyze_text_tool,
    get_context_tool,
    get_chapter_by_order_tool,
    read_chapter_tool,
    search_analysis_fragments_tool,
]

# 创建工具节点
tools_node = ToolNode(all_tools)

# 添加到图中
workflow.add_node("tools", tools_node)
```

**步骤3：配置工具调用**
```python
# 在agent节点中
async def agent_node(state: AgentState):
    messages = state["messages"]

    # 调用LLM，LLM可以决定是否使用工具
    response = await llm_with_tools.ainvoke(messages)

    return {"messages": [response]}

# 添加条件边：决定是调用工具还是结束
def should_continue(state: AgentState):
    messages = state["messages"]
    last_message = messages[-1]

    # 如果LLM调用了工具
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    # 否则结束
    return END

workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        END: END
    }
)

# 工具执行后返回agent
workflow.add_edge("tools", "agent")
```

#### ✅ 验收标准
- [ ] 所有7个工具都可以在Chat中调用
- [ ] 工具调用时正确传递task_type参数
- [ ] 工具返回结果格式正确
- [ ] 通过单元测试：测试每个工具的调用

#### ⚠️ 注意事项
1. **工具参数验证**：确保所有必需参数都传递了
2. **异步调用**：所有工具都是异步的，使用await
3. **错误处理**：工具可能失败，需要捕获异常
4. **task_type传递**：确保工具内部的LLM调用传递了task_type

#### 🔗 相关代码位置
- 工具定义：`backend/app/services/agent/langgraph_agent.py` Line 92-193（根据诊断调整）
- 辅助函数：`_generate_text_helper`
- 使用示例：Planning的tools节点

---

### 1.2 Checkpointer ⭐⭐⭐⭐⭐

#### 📍 复用时机
**阶段**：P1阶段
**任务**：P1-01-实现chat_stream
**Week**：Week 6

#### 📦 包含内容
- AsyncRedisSaver配置
- Redis连接管理
- Checkpoint数据结构
- 自动保存机制

#### 🎯 复用方式

**步骤1：共享Checkpointer实例**
```python
class LangGraphAgent:
    def __init__(self, ai_service):
        self.ai_service = ai_service

        # 初始化Checkpointer（Planning已配置好）
        from langgraph.checkpoint.redis import AsyncRedisSaver

        # 复用Planning的Redis配置
        self.checkpointer = AsyncRedisSaver(
            redis_url="redis://localhost:6379",  # 根据实际配置调整
            # 其他配置参数...
        )

        # Planning图使用checkpointer
        self.planning_graph = self._build_planning_graph()

        # Chat图也使用同一个checkpointer ✅
        self.chat_graph = self._build_chat_graph()
```

**步骤2：在Chat图中启用Checkpointer**
```python
def _build_chat_graph(self):
    from langgraph.graph import StateGraph, END

    workflow = StateGraph(ChatAgentState)

    # 添加节点...
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tools_node)

    # 设置入口点
    workflow.set_entry_point("agent")

    # 添加边...

    # 编译图，使用共享的checkpointer ✅
    return workflow.compile(checkpointer=self.checkpointer)
```

**步骤3：在chat_stream中使用**
```python
async def chat_stream(
    self,
    message: str,
    conversation_id: str,  # 重要：用于checkpoint的thread_id
    on_progress: Optional[callable] = None
):
    """实现流式chat，支持对话历史"""

    # 配置conversation_id作为thread_id
    config = {
        "configurable": {
            "thread_id": conversation_id  # ← 关键：用于加载/保存对话历史
        }
    }

    # 构建初始状态
    initial_state = {
        "messages": [HumanMessage(content=message)],
        "work_id": None,
        "chapter_id": None,
    }

    # LangGraph自动加载历史消息，执行后自动保存 ✅
    async for event in self.chat_graph.astream(initial_state, config):
        node_name = list(event.keys())[0]
        node_data = event[node_name]

        # 处理事件...
        if on_progress:
            await on_progress(...)

    # 无需手动保存！LangGraph已自动保存到checkpointer ✅
```

#### ✅ 验收标准
- [ ] Planning和Chat可以共享对话历史
- [ ] 同一conversation_id在两种模式下看到相同历史
- [ ] Chat模式的对话历史正确保存
- [ ] Redis中的checkpoint数据结构正确

#### ⚠️ 注意事项
1. **thread_id一致性**：Planning和Chat必须使用相同的conversation_id
2. **State结构兼容**：ChatAgentState应与PlanningAgentState兼容
3. **Redis连接池**：确保Redis连接池配置合理
4. **数据迁移**：如果改变State结构，需要处理旧数据

#### 🔗 相关代码位置
- Checkpointer初始化：`langgraph_agent.py` __init__方法（根据诊断调整）
- Planning使用示例：`chat_with_planning`方法
- Redis配置：配置文件或环境变量

---

### 1.3 模型选择器 ⭐⭐⭐⭐⭐

#### 📍 复用时机
**阶段**：P0阶段
**任务**：P0-01-修复task_type传递
**Week**：Week 3

#### 📦 包含内容
- TaskType枚举定义
- 任务类型到模型的映射
- 模型选择逻辑

#### 🎯 复用方式

**步骤1：导入TaskType**
```python
# 在所有需要调用LLM的地方
from backend.app.services.agent.model_selector import TaskType
```

**步骤2：在Chat节点中使用**
```python
async def intent_classifier_node(state: AgentState):
    """意图识别节点 - 使用简单模型"""

    prompt = "分析用户意图：..."

    # 使用SIMPLE_QA类型 → 自动选择flash模型 ✅
    response = await self._generate_text(
        prompt=prompt,
        task_type=TaskType.SIMPLE_QA  # ← 复用
    )

    return {"intent": response}


async def writing_agent_node(state: AgentState):
    """写作Agent节点 - 使用强大模型"""

    prompt = "根据上下文续写：..."

    # 使用CONTENT_CREATION类型 → 自动选择pro模型 ✅
    response = await self._generate_text(
        prompt=prompt,
        task_type=TaskType.CONTENT_CREATION  # ← 复用
    )

    return {"messages": [AIMessage(content=response)]}


async def polish_agent_node(state: AgentState):
    """润色Agent节点 - 使用中等模型"""

    prompt = "润色以下文本：..."

    # 使用TEXT_POLISH类型 → 自动选择flash模型 ✅
    response = await self._generate_text(
        prompt=prompt,
        task_type=TaskType.TEXT_POLISH  # ← 复用
    )

    return {"messages": [AIMessage(content=response)]}
```

**步骤3：确保_generate_text方法支持task_type**
```python
async def _generate_text(
    self,
    prompt: str,
    task_type: TaskType,  # ← 必须传递
    **kwargs
):
    """调用AI服务生成文本"""

    # 将task_type传递给ai_service
    response = await self.ai_service.generate(
        prompt=prompt,
        task_type=task_type,  # ← 传递给底层
        **kwargs
    )

    return response
```

#### ✅ 验收标准
- [ ] Chat的所有LLM调用都传递task_type
- [ ] 简单对话使用flash模型（查看日志）
- [ ] 复杂任务使用pro模型（查看日志）
- [ ] 成本降低（对比前后API调用费用）

#### ⚠️ 注意事项
1. **覆盖所有调用点**：使用grep搜索确保没有遗漏
2. **选择合适的TaskType**：根据任务特点选择
3. **性能监控**：记录每种TaskType的响应时间和成本

#### 🔗 相关代码位置
- TaskType定义：`backend/app/services/agent/model_selector.py`
- 使用示例：Planning中的各个节点
- AI服务接口：`backend/app/services/ai_service.py`

---

### 1.4 JSON解析器 ⭐⭐⭐⭐

#### 📍 复用时机
**阶段**：随时可用
**任务**：任何需要解析LLM返回JSON的地方
**Week**：任何时候

#### 📦 包含内容
- 5种JSON解析策略
- 健壮的错误处理
- 多种格式支持

#### 🎯 复用方式

**场景1：解析意图识别结果**
```python
async def _classify_intent(self, state: AgentState):
    """意图识别节点"""

    prompt = """请分析用户意图，返回JSON格式：
    {
        "intent": "writing"|"reading"|"analyzing",
        "confidence": 0.0-1.0
    }

    用户输入：{message}
    """

    response = await self._generate_text(
        prompt=prompt,
        task_type=TaskType.SIMPLE_QA
    )

    # 复用Planning的JSON解析器 ✅
    intent_data = self._extract_json_from_text(response)

    if intent_data:
        return {
            "intent": intent_data.get("intent"),
            "confidence": intent_data.get("confidence", 0.5)
        }
    else:
        # 解析失败，使用默认值
        return {"intent": "unknown", "confidence": 0.0}
```

**场景2：解析结构化输出**
```python
async def _analyze_chapter(self, chapter_content: str):
    """分析章节，返回结构化数据"""

    prompt = """分析以下章节，返回JSON：
    {
        "word_count": <数字>,
        "themes": [<主题列表>],
        "characters": [<角色列表>],
        "summary": "<摘要>"
    }

    章节内容：{chapter_content}
    """

    response = await self._generate_text(
        prompt=prompt,
        task_type=TaskType.DEEP_ANALYSIS
    )

    # 复用JSON解析器 ✅
    analysis_data = self._extract_json_from_text(response)

    return analysis_data
```

#### ✅ 验收标准
- [ ] 可以正确解析纯JSON
- [ ] 可以正确解析Markdown代码块中的JSON
- [ ] 解析失败时返回None，不抛异常
- [ ] 处理各种边界情况（空字符串、无效JSON等）

#### ⚠️ 注意事项
1. **总是检查返回值**：可能返回None
2. **提供默认值**：解析失败时的fallback逻辑
3. **Prompt优化**：明确要求LLM返回JSON格式

#### 🔗 相关代码位置
- 方法定义：`langgraph_agent.py` 的 `_extract_json_from_text`方法
- 使用示例：Planning中的多个节点

---

### 1.5 重试机制 ⭐⭐⭐⭐⭐

#### 📍 复用时机
**阶段**：P0阶段及之后
**任务**：所有异步操作
**Week**：Week 2+

#### 📦 包含内容
- 通用异步重试包装器
- 指数退避策略
- 详细日志记录

#### 🎯 复用方式

**场景1：包装LLM调用**
```python
from backend.app.services.agent.langgraph_agent import _retry_on_failure

async def _call_llm_with_retry(self, messages, task_type):
    """带重试的LLM调用"""

    return await _retry_on_failure(
        self.ai_service.generate,
        messages=messages,
        task_type=task_type,
        max_retries=3  # 最多重试3次
    )
```

**场景2：包装数据库操作**
```python
async def _get_chapter_with_retry(self, chapter_id: str):
    """带重试的数据库查询"""

    return await _retry_on_failure(
        self.db.get_chapter,
        chapter_id=chapter_id,
        max_retries=3
    )
```

**场景3：包装API调用**
```python
async def _search_fragments_with_retry(self, query: str):
    """带重试的检索API调用"""

    return await _retry_on_failure(
        self.search_service.search,
        query=query,
        top_k=5,
        max_retries=3
    )
```

#### ✅ 验收标准
- [ ] 临时性错误自动重试
- [ ] 指数退避生效（查看日志时间间隔）
- [ ] 达到最大重试次数后正确抛出异常
- [ ] 日志记录清晰

#### ⚠️ 注意事项
1. **幂等性**：只对幂等操作使用重试
2. **重试次数**：根据操作类型调整max_retries
3. **超时设置**：避免单次操作时间过长

#### 🔗 相关代码位置
- 函数定义：`langgraph_agent.py` 的 `_retry_on_failure`函数
- 使用示例：Planning的工具和节点中

---

### 1.6 Prompt模板库 ⭐⭐⭐⭐⭐

#### 📍 复用时机
**阶段**：P1阶段
**任务**：P1-05-Prompt优化
**Week**：Week 8

#### 📦 包含内容
- 已验证的Prompt模板
- NovelPhase枚举
- 阶段特征描述

#### 🎯 复用方式

**步骤1：导入Prompt模板**
```python
from backend.app.services.agent.prompt_library import (
    get_content_prompt,
    NovelPhase,
    PhaseCharacteristics,
)
```

**步骤2：在写作Agent中使用**
```python
async def writing_agent_node(state: AgentState):
    """写作Agent - 复用Planning的Prompt模板"""

    context = state.get("context", {})
    chapter_info = state.get("chapter_info", {})

    # 确定当前小说阶段
    current_phase = self._determine_phase(chapter_info)

    # 复用Planning的Prompt模板 ✅
    prompt = get_content_prompt(
        phase=current_phase,
        context=context,
        requirements="续写第三章，保持前文风格"
    )

    # 生成内容
    response = await self._generate_text(
        prompt=prompt,
        task_type=TaskType.CONTENT_CREATION
    )

    return {"messages": [AIMessage(content=response)]}


def _determine_phase(self, chapter_info: dict) -> NovelPhase:
    """根据章节信息确定小说阶段"""

    chapter_number = chapter_info.get("order", 1)
    total_chapters = chapter_info.get("total", 50)

    progress = chapter_number / total_chapters

    if progress < 0.3:
        return NovelPhase.OPENING
    elif progress < 0.7:
        return NovelPhase.DEVELOPMENT
    else:
        return NovelPhase.CLIMAX
```

**步骤3：根据Chat场景调整（可选）**
```python
# 如果Planning的模板不完全适合，可以扩展
def get_chat_writing_prompt(
    phase: NovelPhase,
    context: dict,
    conversation_history: List[str]
) -> str:
    """Chat模式的写作Prompt - 基于Planning模板扩展"""

    # 复用Planning的基础模板
    base_prompt = get_content_prompt(phase, context)

    # 添加对话历史
    history_summary = self._summarize_conversation(conversation_history)

    enhanced_prompt = f"""{base_prompt}

对话历史：
{history_summary}

请基于以上对话历史和要求，生成内容。
"""

    return enhanced_prompt
```

#### ✅ 验收标准
- [ ] 复用了Planning的核心Prompt模板
- [ ] 根据Chat场景做了适当调整
- [ ] 生成内容质量≥Planning模式
- [ ] 不同阶段的特征明显

#### ⚠️ 注意事项
1. **理解模板意图**：先理解Planning为什么这样设计
2. **保留核心逻辑**：不要破坏已验证的部分
3. **增量调整**：如需修改，逐步测试效果

#### 🔗 相关代码位置
- 模板定义：`backend/app/services/agent/prompt_library.py`
- 使用示例：Planning的写作节点
- 阶段特征：`PhaseCharacteristics`类

---

## 🔧 类别2：适配复用组件（4个）

这些组件需要**轻度修改**才能在Chat中使用，是复用的重点之一。

---

### 2.1 进度回调机制 🔧

#### 📍 复用时机
**阶段**：P1阶段
**任务**：P1-01-实现chat_stream
**Week**：Week 6

#### 🎯 适配方案

**Planning的回调机制**：
```python
# Planning使用手动回调
await on_plan(plan_data)
await on_task_start(task_info)
await on_task_progress(progress_info)
await on_task_done(result_info)
```

**Chat的适配方案**：
```python
# Chat使用LangGraph事件转换为回调
async def chat_stream(self, message, on_progress=None):
    """将LangGraph事件转换为Planning兼容的进度格式"""

    async for event in self.graph.astream(...):
        # 转换LangGraph事件 → Planning格式 ✅
        progress_event = self._convert_to_planning_format(event)

        if progress_event and on_progress:
            await on_progress(progress_event)


def _convert_to_planning_format(self, graph_event: dict) -> dict:
    """
    复用Planning的事件结构

    Planning事件格式：
    {
        "type": "plan" | "task_start" | "task_progress" | "task_done" | "content",
        "description": str,
        "timestamp": float,
        "details": dict
    }
    """
    node_name = list(graph_event.keys())[0]
    node_data = graph_event[node_name]

    if node_name == "intent_classifier":
        return {
            "type": "task_start",  # 复用Planning的类型
            "description": "正在分析您的需求...",
            "timestamp": time.time(),
            "details": {"node": node_name}
        }

    elif node_name == "tools":
        return {
            "type": "task_progress",  # 复用Planning的类型
            "description": "正在调用工具...",
            "timestamp": time.time(),
            "details": {"tools": self._extract_tool_names(node_data)}
        }

    # ... 其他节点映射

    return None
```

#### ✅ 验收标准
- [ ] 前端接收到的事件格式与Planning一致
- [ ] 前端无需修改即可显示Chat的进度
- [ ] 事件覆盖所有关键节点

#### ⚠️ 注意事项
- 保持事件数据结构与Planning兼容
- 新增事件类型需要前端支持

---

### 2.2 错误处理逻辑 🔧

#### 📍 复用时机
**阶段**：P2阶段
**任务**：P2-02-错误处理
**Week**：Week 9

#### 🎯 适配方案

**步骤1：提取Planning的错误处理为工具类**
```python
# 创建新文件：backend/app/services/agent/common/error_handler.py

import httpx
from typing import Type, Tuple

class ErrorHandler:
    """复用Planning的错误处理逻辑"""

    # 从Planning复制网络错误类型
    NETWORK_RELATED_ERRORS = (
        httpx.ConnectTimeout,
        httpx.ReadTimeout,
        httpx.NetworkError,
        ConnectionError,
        TimeoutError,
    )

    @classmethod
    def classify_error(cls, error: Exception) -> str:
        """
        分类错误类型（复用Planning的分类逻辑）

        返回: "network" | "llm" | "tool" | "unknown"
        """
        if isinstance(error, cls.NETWORK_RELATED_ERRORS):
            return "network"

        # 检查错误消息中的关键词（从Planning复用）
        error_msg = str(error).lower()
        if any(kw in error_msg for kw in ["网络", "连接", "超时", "timeout", "connection"]):
            return "network"

        if any(kw in error_msg for kw in ["llm", "model", "api"]):
            return "llm"

        if any(kw in error_msg for kw in ["tool", "function"]):
            return "tool"

        return "unknown"

    @classmethod
    def get_user_friendly_message(cls, error: Exception) -> str:
        """获取用户友好的错误消息（复用Planning的消息）"""

        error_type = cls.classify_error(error)

        messages = {
            "network": "网络连接问题，请稍后重试",
            "llm": "AI服务暂时不可用，请稍后重试",
            "tool": "工具调用失败，请检查参数",
            "unknown": "发生未知错误，请联系管理员"
        }

        return messages.get(error_type, messages["unknown"])
```

**步骤2：在Chat中使用**
```python
from backend.app.services.agent.common.error_handler import ErrorHandler

async def chat_stream(self, message, on_progress=None, on_error=None):
    """带错误处理的chat_stream"""

    try:
        async for event in self.graph.astream(...):
            # 正常处理...
            pass

    except Exception as e:
        # 复用Planning的错误处理 ✅
        error_type = ErrorHandler.classify_error(e)
        user_msg = ErrorHandler.get_user_friendly_message(e)

        if on_error:
            await on_error({
                "type": error_type,
                "message": user_msg,
                "recoverable": error_type in ["network", "llm"]
            })

        # 根据错误类型决定是否重试
        if error_type == "network":
            # 可以重试
            return await self._retry_with_backoff(message, on_progress, on_error)
        else:
            # 不可重试，抛出异常
            raise
```

#### ✅ 验收标准
- [ ] Planning和Chat使用相同的ErrorHandler
- [ ] 错误分类准确
- [ ] 用户看到友好的错误消息
- [ ] 可重试的错误自动重试

---

### 2.3 上下文构建 🔧

#### 📍 复用时机
**阶段**：P1阶段
**任务**：P1-04-上下文管理
**Week**：Week 8

#### 🎯 适配方案

**步骤1：提取Planning的上下文构建逻辑**
```python
# 创建新文件：backend/app/services/agent/common/context_builder.py

class ContextBuilder:
    """复用Planning的上下文构建策略"""

    @staticmethod
    def build_initial_context(message: str, work_info: dict) -> str:
        """
        构建初始上下文（从Planning复用）

        Planning的格式：
        用户请求：{message}

        作品信息：
        - 标题：{title}
        - 类型：{genre}
        """
        return f"""用户请求：{message}

作品信息：
- 标题：{work_info.get('title', '未设置')}
- 类型：{work_info.get('genre', '未设置')}
- 当前章节：{work_info.get('current_chapter', '未知')}

"""

    @staticmethod
    def append_tool_result(context: str, tool_name: str, result: str) -> str:
        """追加工具结果到上下文（从Planning复用）"""

        return f"""{context}
工具调用结果 ({tool_name}):
{result}

"""

    @staticmethod
    def summarize_long_context(context: str, max_length: int = 2000) -> str:
        """压缩过长的上下文（新增，Planning没有）"""

        if len(context) <= max_length:
            return context

        # 简单截断策略（后续可以用LLM总结）
        return context[:max_length] + "\n\n[上下文过长，已截断...]"
```

**步骤2：在Chat中使用**
```python
from backend.app.services.agent.common.context_builder import ContextBuilder

async def _build_writing_context(self, state: AgentState) -> str:
    """构建写作上下文 - 复用Planning的策略"""

    # 复用初始上下文构建 ✅
    context = ContextBuilder.build_initial_context(
        message=state["messages"][0].content,
        work_info=state.get("context", {})
    )

    # 追加工具结果 ✅
    for msg in state["messages"]:
        if isinstance(msg, ToolMessage):
            context = ContextBuilder.append_tool_result(
                context,
                msg.name,
                msg.content
            )

    # 压缩上下文（新功能）
    context = ContextBuilder.summarize_long_context(context)

    return context
```

#### ✅ 验收标准
- [ ] Planning和Chat的上下文格式一致
- [ ] 上下文包含所有必要信息
- [ ] 长上下文正确压缩
- [ ] 不会超出模型token限制

---

### 2.4 AgentState结构 🔧

#### 📍 复用时机
**阶段**：P1阶段
**任务**：P1-01-实现chat_stream
**Week**：Week 6

#### 🎯 适配方案

**Planning的AgentState**：
```python
class AgentState(TypedDict):
    messages: Annotated[List[Any], operator.add]
    work_id: Optional[str]
    chapter_id: Optional[str]
    intent: Optional[str]
    context: Dict[str, Any]
    agent_steps: Annotated[List[Dict[str, Any]], operator.add]
    suggested_actions: Annotated[List[str], operator.add]
    final_response: Optional[str]
```

**Chat的AgentState（扩展）**：
```python
from typing import TypedDict, Annotated, List, Optional, Dict, Any
import operator

class ChatAgentState(TypedDict):
    # ===== 直接复用Planning的字段 ✅ =====
    messages: Annotated[List[Any], operator.add]
    work_id: Optional[str]
    chapter_id: Optional[str]
    context: Dict[str, Any]

    # ===== 复用但语义不同的字段 =====
    intent: Optional[str]  # Chat用于意图分类

    # ===== Chat特有的新字段 =====
    conversation_id: str  # 对话ID（用于checkpointer）
    task_type: Optional[str]  # 当前任务类型

    # ===== 可选的Planning字段（按需使用）=====
    # agent_steps: Annotated[List[Dict[str, Any]], operator.add]
    # suggested_actions: Annotated[List[str], operator.add]
    # final_response: Optional[str]
```

#### ✅ 验收标准
- [ ] ChatAgentState与Planning兼容
- [ ] Checkpointer可以正确序列化/反序列化
- [ ] Planning和Chat可以共享某些字段

#### ⚠️ 注意事项
- 保持核心字段与Planning一致
- 新增字段要文档化
- 考虑向后兼容性

---

## 💡 类别3：设计思想复用（3个）

这些不是直接复用代码，而是复用**设计智慧**。

---

### 3.1 三阶段执行模式 💡

#### 📍 复用时机
**阶段**：P1阶段
**任务**：整体架构设计
**Week**：Week 6

#### 🎯 借鉴思想

**Planning的三阶段**：
```
Phase 1: Planning（计划） → 生成任务列表
Phase 2: Execution（执行） → 并行执行任务
Phase 3: Response（响应） → 聚合结果返回
```

**Chat的借鉴（ReAct循环，但可以借鉴阶段划分）**：
```
虽然Chat是动态的ReAct循环（思考→行动→观察），
但可以借鉴Planning的"阶段划分"思想：

Phase 1: Intent Classification（意图识别）
  - 类似Planning的计划阶段
  - 确定用户意图和所需工具

Phase 2: Tool Execution（工具执行）
  - 类似Planning的执行阶段
  - 调用工具获取信息

Phase 3: Response Generation（响应生成）
  - 类似Planning的响应阶段
  - 基于工具结果生成回复
```

#### 💡 借鉴价值
- 清晰的执行流程，便于监控
- 阶段间职责明确
- 便于调试和优化

#### ⚠️ 注意
- Chat需要保持灵活性
- 不能完全固定三阶段（ReAct是动态的）

---

### 3.2 智能并行执行 💡

#### 📍 复用时机
**阶段**：P2阶段
**任务**：性能优化
**Week**：Week 9

#### 🎯 借鉴思想

**Planning的并行执行**：
```python
# Planning使用asyncio.gather并行执行多个任务
task_results = await asyncio.gather(*[
    self._execute_task(task1),
    self._execute_task(task2),
    self._execute_task(task3),
])
```

**Chat的借鉴（使用LangGraph的Send API）**：
```python
# 当需要并行调用多个工具时
from langgraph.constants import Send

def route_to_tools(state: AgentState):
    """决定是否并行调用工具"""

    last_message = state["messages"][-1]

    if hasattr(last_message, "tool_calls"):
        tool_calls = last_message.tool_calls

        if len(tool_calls) > 1:
            # 多个工具调用 → 并行执行 ✅（借鉴Planning的思想）
            return [
                Send("tools", {"tool_call": tc})
                for tc in tool_calls
            ]

    # 单个工具或无工具
    return "tools"  # 或 END

workflow.add_conditional_edges(
    "agent",
    route_to_tools
)
```

#### 💡 借鉴价值
- 提升性能（多个独立工具并行）
- Planning已验证有效

---

### 3.3 结果聚合策略 💡

#### 📍 复用时机
**阶段**：P1阶段
**任务**：响应生成
**Week**：Week 8

#### 🎯 借鉴思想

**Planning的聚合策略**：
```python
def _build_final_response(self, task_results):
    """Planning的结果聚合逻辑"""

    # 策略1：如果有内容创作任务，直接返回创作内容
    for result in task_results:
        if result["type"] == "content_creation":
            return result["content"]

    # 策略2：否则，用LLM总结所有结果
    summary = await self._summarize_results(task_results)
    return summary
```

**Chat的借鉴**：
```python
async def _build_chat_response(self, state: AgentState) -> str:
    """Chat的响应生成 - 借鉴Planning的聚合策略"""

    messages = state["messages"]

    # 策略1：如果最后一条是AI消息，直接返回 ✅（借鉴）
    if messages and isinstance(messages[-1], AIMessage):
        return messages[-1].content

    # 策略2：如果有工具结果，总结所有工具结果 ✅（借鉴）
    tool_results = [m for m in messages if isinstance(m, ToolMessage)]
    if tool_results:
        return await self._summarize_tool_results(tool_results)

    # 策略3：默认情况
    return "抱歉，我无法处理您的请求"
```

#### 💡 借鉴价值
- 经过验证的聚合逻辑
- 提升响应质量

---

## 📊 复用进度追踪

### 复用清单总表

| 组件 | 类别 | 阶段 | 任务 | 状态 | 完成日期 | 验证人 |
|------|------|------|------|------|----------|--------|
| 工具系统 | 直接复用 | P0 | P0-02 | ⏸️待执行 | - | - |
| Checkpointer | 直接复用 | P1 | P1-01 | ⏸️待执行 | - | - |
| JSON解析器 | 直接复用 | 随时 | - | ⏸️待执行 | - | - |
| 重试机制 | 直接复用 | P0+ | - | ⏸️待执行 | - | - |
| Prompt模板库 | 直接复用 | P1 | P1-05 | ⏸️待执行 | - | - |
| 模型选择器 | 直接复用 | P0 | P0-01 | ⏸️待执行 | - | - |
| 进度回调机制 | 适配复用 | P1 | P1-01 | ⏸️待执行 | - | - |
| 错误处理逻辑 | 适配复用 | P2 | P2-02 | ⏸️待执行 | - | - |
| 上下文构建 | 适配复用 | P1 | P1-04 | ⏸️待执行 | - | - |
| AgentState结构 | 适配复用 | P1 | P1-01 | ⏸️待执行 | - | - |
| 三阶段执行模式 | 设计复用 | P1 | 架构设计 | ⏸️待执行 | - | - |
| 智能并行执行 | 设计复用 | P2 | 性能优化 | ⏸️待执行 | - | - |
| 结果聚合策略 | 设计复用 | P1 | 响应生成 | ⏸️待执行 | - | - |

### 更新说明
- 每完成一个组件的复用，更新状态为"✅已完成"
- 记录完成日期和验证人
- 如果复用失败，记录原因和调整方案

---

## 🎯 关键成功因素

### 1. 验证先行 ⚠️
- 所有复用必须基于P0-00的诊断结果
- 验证失败立即调整策略

### 2. 渐进复用 📈
- 从简单到复杂
- 从直接复用到适配复用
- 从代码复用到设计复用

### 3. 充分测试 ✅
- 每个复用组件都要测试
- 回归测试确保不影响Planning
- 性能测试确保无回归

### 4. 文档同步 📝
- 复用过程中的调整及时更新文档
- 记录复用经验和教训
- 为团队提供参考

---

**文档版本**：v1.0
**创建时间**：2025-01-06
**维护者**：Agent开发团队
**状态**：📋 待执行（需先完成P0-00诊断）

**相关文档**：
- [P0-00-代码现状诊断.md](./P0-00-代码现状诊断.md) - 必须先完成
- [IMPLEMENTATION_PLAN.md](./IMPLEMENTATION_PLAN.md) - 总体计划
- [../Planning模式到Chat模式的复用策略.md](../Planning模式到Chat模式的复用策略.md) - 战略参考
