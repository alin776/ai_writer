# Planning模式到Chat()模式的复用策略

## 📌 背景说明

**核心问题**：Planning模式虽然逐步被放弃，但其中包含大量优秀的设计和实现。在优化Chat()模式时，应该充分复用这些已验证的组件，避免重复开发。

**本文档目标**：系统梳理Planning模式中可复用的内容，制定清晰的复用策略。

## ⚠️ 重要提示

**本文档基于代码分析和设计推演编写，但尚未完全验证实际代码的一致性！**

在实施复用前，必须：
1. ✅ 验证文档中提到的代码位置是否准确
2. ✅ 验证各组件的实际实现是否支持文档描述的功能
3. ✅ 验证复用的可行性和工作量估算
4. ✅ 制定详细的验证清单和测试计划

**切勿盲目按照本文档实施，必须先进行代码验证！**

详细验证计划参见：`tasks/todo.md` - "Planning → Chat 模式复用策略 · 深度Review计划"

---

## 🎯 可复用内容全景图

```
┌─────────────────────────────────────────────────────────────┐
│                 100% 直接复用（无需修改）                      │
├─────────────────────────────────────────────────────────────┤
│  1. 工具系统 (tools)                                         │
│  2. Checkpointer集成                                         │
│  3. JSON解析器                                               │
│  4. 重试机制                                                 │
│  5. Prompt模板库                                             │
│  6. 模型选择器 (TaskType)                                    │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│              需要适配后复用（轻度修改）                        │
├─────────────────────────────────────────────────────────────┤
│  7. 进度回调机制                                             │
│  8. 错误处理逻辑                                             │
│  9. 上下文构建                                               │
│  10. AgentState结构                                         │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│              设计思想复用（需重新实现）                        │
├─────────────────────────────────────────────────────────────┤
│  11. 三阶段执行模式                                          │
│  12. 智能并行执行                                            │
│  13. 结果聚合策略                                            │
└─────────────────────────────────────────────────────────────┘
```

---

## ✅ 类别1：100% 直接复用（无需修改）

### 1. 工具系统 (Tools)

**位置**：`langgraph_agent.py` Line 92-193

**复用价值**：⭐⭐⭐⭐⭐（最高）

**核心内容**：
```python
# 可以直接复用的工具
- continue_writing_tool      # 续写工具
- polish_text_tool           # 润色工具
- analyze_text_tool          # 分析工具
- get_context_tool           # 获取上下文
- get_chapter_by_order_tool  # 按序号获取章节
- read_chapter_tool          # 读取章节
- search_analysis_fragments_tool  # 检索分析片段

# 辅助函数
- _generate_text_helper      # 文本生成辅助（支持task_type）
- _retry_on_failure          # 通用重试机制
```

**复用方式**：
```python
# Chat模式直接引用
from backend.app.services.agent.langgraph_agent import (
    continue_writing_tool,
    polish_text_tool,
    analyze_text_tool,
    # ... 其他工具
)

# 在Chat的Graph中使用
workflow.add_node("tools", ToolNode([
    continue_writing_tool,
    polish_text_tool,
    analyze_text_tool,
    # ...
]))
```

**注意事项**：
- ✅ 工具已支持`task_type`参数，符合模型选择机制
- ✅ 工具内部已有重试机制，稳定可靠
- ⚠️ 需要确保`_global_ai_service`已初始化

---

### 2. Checkpointer集成

**位置**：`langgraph_agent.py` Line 1986-2037

**复用价值**：⭐⭐⭐⭐⭐

**核心内容**：
```python
# Planning模式的Checkpointer使用方式
- AsyncRedisSaver 配置
- checkpoint 数据结构
- aput/aget/aget_tuple 完整使用示例
- 消息合并逻辑
```

**复用方式**：
```python
# Chat模式可以直接使用相同的checkpointer实例
class LangGraphAgent:
    def __init__(self, ...):
        # 复用同一个checkpointer
        self.checkpointer = AsyncRedisSaver(...)

        # Planning图使用
        self.planning_graph = self._build_planning_graph()

        # Chat图也使用
        self.chat_graph = self._build_chat_graph()
        # 两者共享checkpointer ✅

# 在chat_stream中使用
async def chat_stream(self, message, conversation_id):
    config = {"configurable": {"thread_id": conversation_id}}

    # LangGraph自动使用checkpointer
    async for event in self.chat_graph.astream(initial_state, config):
        yield event

    # 无需手动保存，LangGraph已自动保存 ✅
```

**优势**：
- ✅ Planning已验证的checkpoint数据结构可直接复用
- ✅ 两种模式共享同一个对话历史存储
- ✅ 无需重新测试Redis集成

---

### 3. JSON解析器

**位置**：`langgraph_agent.py` Line 1614-1730

**复用价值**：⭐⭐⭐⭐

**核心内容**：
```python
def _extract_json_from_text(self, text: str) -> Optional[dict]:
    """
    从文本中提取JSON对象

    支持5种解析策略：
    1. 纯JSON
    2. Markdown代码块包裹的JSON (```json ... ```)
    3. 普通代码块 (``` ... ```)
    4. 正则匹配JSON对象
    5. 逐字符扫描匹配大括号
    """
```

**复用方式**：
```python
# Chat模式中的意图识别可能也需要解析JSON
async def _classify_intent(self, state: AgentState):
    response = await llm.ainvoke(...)

    # 复用Planning的JSON解析器
    intent_data = self._extract_json_from_text(response.content)

    if intent_data:
        return {"intent": intent_data.get("intent")}
```

**优势**：
- ✅ 已经过充分测试，处理各种边界情况
- ✅ 支持多种LLM输出格式
- ✅ 健壮的错误处理

---

### 4. 重试机制

**位置**：`langgraph_agent.py` Line 61-89

**复用价值**：⭐⭐⭐⭐⭐

**核心内容**：
```python
async def _retry_on_failure(func, *args, max_retries=3, **kwargs):
    """
    通用重试包装器

    特性：
    - 指数退避 (2^retry_count)
    - 异常传播
    - 详细日志
    """
```

**复用方式**：
```python
# Chat模式的任何异步操作都可以使用
async def _call_llm_with_retry(self, messages, task_type):
    return await _retry_on_failure(
        self.ai_service.generate,
        messages=messages,
        task_type=task_type,
        max_retries=3
    )
```

**优势**：
- ✅ 通用工具函数，与模式无关
- ✅ 已验证有效
- ✅ 提升系统稳定性

---

### 5. Prompt模板库

**位置**：`backend/app/services/agent/prompt_library.py`

**复用价值**：⭐⭐⭐⭐⭐

**核心内容**：
```python
# Planning使用的各种Prompt模板
- get_content_prompt()  # 获取内容生成提示
- NovelPhase            # 小说阶段枚举
- PhaseCharacteristics  # 阶段特征
```

**复用方式**：
```python
# Chat模式的写作Agent可以直接使用
async def _writing_agent_node(self, state: AgentState):
    # 复用Planning的Prompt模板
    prompt = get_content_prompt(
        phase=NovelPhase.DEVELOPMENT,
        context=state.get("context"),
        requirements="..."
    )

    response = await llm.ainvoke(prompt)
    return {"messages": [response]}
```

---

### 6. 模型选择器 (TaskType)

**位置**：`backend/app/services/agent/model_selector.py`

**复用价值**：⭐⭐⭐⭐⭐

**核心内容**：
```python
class TaskType(str, Enum):
    CONTENT_CREATION = "content_creation"  # 内容创作 → gemini-2.5-pro
    SIMPLE_QA = "simple_qa"                # 简单问答 → gemini-2.5-flash-lite
    TEXT_POLISH = "text_polish"            # 文本润色 → gemini-2.5-flash
    DEEP_ANALYSIS = "deep_analysis"        # 深度分析 → gemini-2.5-pro
    # ...
```

**复用方式**：
```python
# Chat模式的每个节点都应该使用
async def _intent_classifier(self, state: AgentState):
    # 意图分类用简单模型
    response = await self._generate_text(
        prompt=prompt,
        task_type=TaskType.SIMPLE_QA  # ← 复用
    )

async def _writing_agent(self, state: AgentState):
    # 写作用强大模型
    response = await self._generate_text(
        prompt=prompt,
        task_type=TaskType.CONTENT_CREATION  # ← 复用
    )
```

**优势**：
- ✅ Planning已定义好各种任务类型
- ✅ 模型映射已优化
- ✅ 直接提升性能和降低成本

---

## 🔧 类别2：需要适配后复用（轻度修改）

### 7. 进度回调机制

**位置**：`langgraph_agent.py` Line 1732-2050

**Planning的实现**：
```python
# Planning模式的进度回调
async def chat_with_planning(
    self,
    message: str,
    on_plan=None,           # 计划生成回调
    on_task_start=None,     # 任务开始回调
    on_task_progress=None,  # 任务进度回调
    on_task_done=None,      # 任务完成回调
    on_content=None         # 内容流式输出回调
):
    # 调用回调
    if on_plan:
        await on_plan(plan_data)

    if on_task_start:
        await on_task_start(task_info)
```

**Chat模式的适配**：
```python
# 适配为Chat模式的事件流
async def chat_stream(
    self,
    message: str,
    on_progress=None       # ← 统一的进度回调
):
    async for event in self.graph.astream(...):
        # 将LangGraph事件转换为统一格式
        progress_event = self._convert_to_progress_event(event)

        if on_progress:
            await on_progress(progress_event)

def _convert_to_progress_event(self, graph_event):
    """
    复用Planning的事件结构，但从LangGraph事件转换
    """
    return {
        "type": self._infer_event_type(graph_event),
        "description": "...",
        "timestamp": time.time()
    }
```

**复用内容**：
- ✅ 回调函数的签名设计
- ✅ 事件数据结构（type, description, timestamp等）
- ✅ 前端已适配的事件处理逻辑

**需要修改**：
- ⚠️ 事件触发时机（从手动调用改为从astream事件推断）
- ⚠️ 事件类型映射（planning的task事件 → chat的node事件）

---

### 8. 错误处理逻辑

**Planning的实现**：
```python
# Line 1880-1920
try:
    plan_result = await self._generate_text(...)
except Exception as e:
    # 检查是否是网络相关错误
    network_related_errors = (
        httpx.ConnectTimeout,
        httpx.ReadTimeout,
        httpx.NetworkError,
        # ...
    )

    is_network_error = (
        isinstance(e, network_related_errors) or
        any(keyword in str(e).lower() for keyword in
            ["网络", "连接", "超时", "timeout", "connection", "network"])
    )

    if is_network_error:
        # 返回友好的错误提示
        return {"error": "网络连接问题，请稍后重试"}
```

**Chat模式的适配**：
```python
# 可以提取为通用的错误处理器
class ErrorHandler:
    """复用Planning的错误分类逻辑"""

    NETWORK_RELATED_ERRORS = (
        httpx.ConnectTimeout,
        httpx.ReadTimeout,
        httpx.NetworkError,
        # ...
    )

    @classmethod
    def classify_error(cls, error: Exception) -> str:
        """
        分类错误类型
        返回: "network" | "llm" | "tool" | "unknown"
        """
        if isinstance(error, cls.NETWORK_RELATED_ERRORS):
            return "network"
        # ...

    @classmethod
    def get_user_friendly_message(cls, error: Exception) -> str:
        """获取用户友好的错误消息"""
        error_type = cls.classify_error(error)

        if error_type == "network":
            return "网络连接问题，请稍后重试"
        # ...

# 在Chat模式中使用
try:
    response = await llm.ainvoke(...)
except Exception as e:
    error_msg = ErrorHandler.get_user_friendly_message(e)
    return {"error": error_msg}
```

**复用内容**：
- ✅ 错误分类逻辑
- ✅ 用户友好的错误消息
- ✅ 网络错误的特殊处理

---

### 9. 上下文构建

**Planning的实现**：
```python
# Line 1955-1972
initial_context = f"用户请求：{message}\n\n"

# 任务执行后聚合上下文
all_context = initial_context
for result in task_results:
    all_context += f"\n任务{result['task_id']}结果：\n{result['result']}\n"
```

**Chat模式的适配**：
```python
# 复用上下文构建的思路
class ContextBuilder:
    """复用Planning的上下文聚合策略"""

    @staticmethod
    def build_initial_context(message: str, work_info: dict) -> str:
        """构建初始上下文"""
        return f"""用户请求：{message}

作品信息：
- 标题：{work_info.get('title')}
- 类型：{work_info.get('genre')}

"""

    @staticmethod
    def append_tool_result(context: str, tool_name: str, result: str) -> str:
        """追加工具结果到上下文"""
        return f"""{context}
工具调用结果 ({tool_name}):
{result}

"""

# 在Chat的节点中使用
def _build_writing_context(self, state: AgentState) -> str:
    context = ContextBuilder.build_initial_context(
        message=state["messages"][0].content,
        work_info=state.get("context", {})
    )

    # 追加工具结果
    for msg in state["messages"]:
        if isinstance(msg, ToolMessage):
            context = ContextBuilder.append_tool_result(
                context, msg.name, msg.content
            )

    return context
```

---

### 10. AgentState结构

**Planning的定义**：
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

**Chat模式的复用**：
```python
# 可以直接复用大部分字段
class ChatAgentState(TypedDict):
    # 复用Planning的核心字段
    messages: Annotated[List[Any], operator.add]     # ✅ 直接复用
    work_id: Optional[str]                            # ✅ 直接复用
    chapter_id: Optional[str]                         # ✅ 直接复用
    context: Dict[str, Any]                           # ✅ 直接复用

    # Chat特有字段
    intent: Optional[str]                             # ✅ 复用但语义不同
    session_id: str                                   # ← 新增
    task_type: str                                    # ← 新增

    # 可选的Planning字段
    agent_steps: Annotated[List[Dict[str, Any]], operator.add]  # ⚠️ 按需复用
```

**优势**：
- ✅ 数据结构已验证
- ✅ work_id、chapter_id等业务字段可直接复用
- ✅ 与checkpointer兼容

---

## 💡 类别3：设计思想复用（需重新实现）

### 11. 三阶段执行模式

**Planning的设计**：
```
Planning阶段 → Execution阶段 → Response阶段
    ↓              ↓                ↓
  生成计划      执行任务          聚合结果
```

**Chat模式的借鉴**：
```
虽然Chat是ReAct模式（思考→行动→观察循环），
但可以借鉴Planning的阶段划分思想：

Phase 1: Intent Classification（意图识别）
  - 类似Planning的计划阶段
  - 确定用户意图和需要调用的工具

Phase 2: Tool Execution（工具执行）
  - 类似Planning的执行阶段
  - 调用必要的工具获取信息

Phase 3: Response Generation（响应生成）
  - 类似Planning的响应阶段
  - 基于工具结果生成最终回复
```

**借鉴价值**：⭐⭐⭐
- ✅ 清晰的执行流程
- ✅ 便于监控和调试
- ⚠️ 但Chat需要保持灵活性，不能完全固定三阶段

---

### 12. 智能并行执行

**Planning的实现**：
```python
# Line 1958-1966
task_results = await self._execute_tasks_in_parallel(
    tasks=plan_data["tasks"],
    # ...
)

# 内部使用asyncio.gather实现并行
```

**Chat模式的借鉴**：
```
Chat模式虽然是串行的ReAct循环，
但在工具执行阶段可以借鉴并行思想：

情况1：需要调用多个独立工具
  → 可以并行执行（类似Planning）

情况2：工具之间有依赖
  → 保持串行

LangGraph的Send API可以实现：
workflow.add_conditional_edges(
    "agent",
    route_to_tools,
    # 返回多个Send可以并行执行工具
)
```

**借鉴价值**：⭐⭐⭐⭐
- ✅ 提升性能
- ✅ Planning已验证有效
- ⚠️ 需要LangGraph的Send API支持

---

### 13. 结果聚合策略

**Planning的实现**：
```python
# Line 1979-1983
final_content = await self._build_final_response(
    task_results=task_results,
    message=message,
    on_content=on_content
)

# 内部逻辑：
# 1. 判断是否有内容创作任务
# 2. 如果有，直接返回创作内容
# 3. 否则，用LLM总结所有结果
```

**Chat模式的借鉴**：
```python
# Chat模式的最终响应也可以复用这个思路
def _build_chat_response(self, state: AgentState) -> str:
    """
    复用Planning的结果聚合策略
    """
    messages = state["messages"]

    # 策略1：如果最后一条是AI消息，直接返回
    if messages and isinstance(messages[-1], AIMessage):
        return messages[-1].content

    # 策略2：如果有工具结果，总结所有工具结果
    tool_results = [m for m in messages if isinstance(m, ToolMessage)]
    if tool_results:
        return self._summarize_tool_results(tool_results)

    # 策略3：默认情况
    return "抱歉，我无法处理您的请求"
```

**借鉴价值**：⭐⭐⭐⭐
- ✅ 经过验证的聚合逻辑
- ✅ 提升响应质量

---

## 🚫 不建议复用的内容

### 1. Planning阶段的Prompt
- **原因**：Planning的计划生成Prompt是专门为三阶段设计的
- **Chat替代**：使用ReAct的标准Prompt

### 2. Task执行循环
- **原因**：Planning手动编排任务，Chat由LangGraph自动编排
- **Chat替代**：依赖LangGraph的图结构

### 3. 手动并发控制（asyncio.gather）
- **原因**：LangGraph有更优雅的并发机制
- **Chat替代**：使用LangGraph的Send API

---

## 📋 复用优先级和实施计划

### 立即复用（P0）⭐⭐⭐⭐⭐

**必须在Chat优化开始前就复用的：**

| 组件 | 复用方式 | 工作量 | 收益 |
|------|---------|--------|------|
| 工具系统 | 直接引用 | 0.5天 | 极高 |
| Checkpointer | 共享实例 | 0.5天 | 极高 |
| 模型选择器 | 直接使用TaskType | 0.5天 | 极高 |
| 重试机制 | 直接调用 | 0.5天 | 高 |

**总计**：2天，收益极高

---

### 近期复用（P1）⭐⭐⭐⭐

**在实现chat_stream时复用的：**

| 组件 | 复用方式 | 工作量 | 收益 |
|------|---------|--------|------|
| JSON解析器 | 复用方法 | 0.5天 | 中 |
| 错误处理 | 提取为ErrorHandler类 | 1天 | 高 |
| 进度回调 | 适配事件格式 | 1.5天 | 高 |
| 上下文构建 | 提取为ContextBuilder | 1天 | 中 |

**总计**：4天

---

### 中期复用（P2）⭐⭐⭐

**在完善功能时复用的：**

| 组件 | 复用方式 | 工作量 | 收益 |
|------|---------|--------|------|
| Prompt模板库 | 适配Chat场景 | 2天 | 高 |
| AgentState | 扩展字段 | 0.5天 | 中 |
| 并行执行思想 | 用Send API重新实现 | 2天 | 中 |

**总计**：4.5天

---

## 🎯 复用实施路线图

### Week 1：基础组件复用

```
Day 1-2:
  ✅ 复用工具系统
  ✅ 复用Checkpointer
  ✅ 复用模型选择器
  ✅ 复用重试机制

验证：
  - Chat模式可以调用所有Planning的工具
  - Chat和Planning共享对话历史
  - Chat的各节点正确使用TaskType
```

### Week 2-3：适配层组件复用

```
Day 3-5:
  ✅ 提取ErrorHandler工具类
  ✅ 适配进度回调机制
  ✅ 提取ContextBuilder

验证：
  - 错误处理统一且友好
  - 前端可以显示Chat的进度
  - 上下文构建合理
```

### Week 4+：设计思想复用

```
Day 6-8:
  ✅ 借鉴三阶段思想优化Chat流程
  ✅ 实现工具并行执行（Send API）
  ✅ 复用结果聚合策略

验证：
  - Chat执行流程清晰
  - 性能提升明显
  - 响应质量好
```

---

## ✅ 验收标准

### 代码复用度
- [ ] 80%以上的工具代码直接复用
- [ ] 错误处理逻辑100%复用
- [ ] Checkpointer配置100%复用

### 功能兼容性
- [ ] Chat和Planning可以共享对话历史
- [ ] 两种模式可以无缝切换
- [ ] 复用的组件没有引发新bug

### 性能表现
- [ ] Chat模式的响应时间不高于Planning
- [ ] 模型选择机制正确生效
- [ ] 并发执行提升性能

---

## 📝 关键注意事项

### ⚠️ 避免的陷阱

1. **过度复用**
   - ❌ 不要复用Planning特有的三阶段Prompt
   - ❌ 不要复用手动任务编排逻辑
   - ✅ 只复用通用的工具和基础设施

2. **复用不彻底**
   - ❌ 不要创建工具的"Chat版本"
   - ❌ 不要重新实现已有的错误处理
   - ✅ 最大化复用，避免重复开发

3. **破坏模式独立性**
   - ❌ 不要让两种模式互相依赖
   - ✅ 通过共享基础组件实现复用
   - ✅ 保持各模式的独立性

### ✅ 最佳实践

1. **提取通用组件**
   ```python
   # 好的做法：提取为独立的工具类
   from app.services.agent.common.error_handler import ErrorHandler
   from app.services.agent.common.context_builder import ContextBuilder

   # 不好的做法：在Planning和Chat中各自实现
   ```

2. **保持向后兼容**
   ```python
   # 好的做法：扩展而非修改
   class ChatAgentState(AgentState):  # 继承Planning的State
       session_id: str  # 新增字段

   # 不好的做法：修改Planning的State定义
   ```

3. **文档化复用关系**
   ```python
   # 在代码中注释复用关系
   class LangGraphAgent:
       def __init__(self):
           # 复用Planning的checkpointer实例
           self.checkpointer = AsyncRedisSaver(...)  # from Planning
   ```

---

## 🎉 总结

### 复用价值估算

**总工作量节省**：10.5天
- P0组件：2天
- P1组件：4天
- P2组件：4.5天

**质量提升**：
- ✅ 复用已验证的代码，减少bug
- ✅ 保持两种模式的一致性
- ✅ 降低维护成本

**关键成功因素**：
1. 正确识别可复用的内容
2. 适当的抽象和提取
3. 保持模式间的独立性
4. 充分的测试验证

---

---

## 🔍 代码验证清单（必须执行）

### 优先级P0：立即验证（最关键）

#### 1. 工具系统验证
```
位置：backend/app/services/agent/langgraph_agent.py Line 92-193

验证项：
[ ] 7个工具是否都存在？
    - continue_writing_tool
    - polish_text_tool
    - analyze_text_tool
    - get_context_tool
    - get_chapter_by_order_tool
    - read_chapter_tool
    - search_analysis_fragments_tool

[ ] 工具是否支持task_type参数？
[ ] _generate_text_helper是否支持task_type？
[ ] _retry_on_failure是否存在且可用？

验证方法：
1. 打开langgraph_agent.py
2. 搜索"continue_writing_tool"
3. 检查工具定义和参数
4. 运行单元测试验证
```

#### 2. Checkpointer集成验证
```
位置：backend/app/services/agent/langgraph_agent.py Line 1986-2037

验证项：
[ ] AsyncRedisSaver是否正确配置？
[ ] Planning和Chat是否可以共享同一个checkpointer实例？
[ ] checkpoint数据结构是什么？
[ ] aput/aget/aget_tuple方法是否可用？

验证方法：
1. 搜索"AsyncRedisSaver"
2. 查看初始化代码
3. 测试Planning和Chat共享对话历史
```

#### 3. 模型选择器验证
```
位置：backend/app/services/agent/model_selector.py

验证项：
[ ] TaskType枚举是否定义完整？
    - CONTENT_CREATION
    - SIMPLE_QA
    - TEXT_POLISH
    - DEEP_ANALYSIS
    等

[ ] 模型映射关系是什么？
[ ] 在Planning中是否实际使用？
[ ] 在Chat中能否直接使用？

验证方法：
1. 打开model_selector.py
2. 查看TaskType定义
3. 搜索代码中的使用情况
```

### 优先级P1：近期验证

#### 4. JSON解析器验证
```
位置：backend/app/services/agent/langgraph_agent.py Line 1614-1730

验证项：
[ ] _extract_json_from_text方法是否存在？
[ ] 5种解析策略是否都实现？
[ ] 是否可以在Chat中直接调用？
```

#### 5. 重试机制验证
```
位置：backend/app/services/agent/langgraph_agent.py Line 61-89

验证项：
[ ] _retry_on_failure函数是否存在？
[ ] 参数签名是什么？
[ ] 是否支持自定义重试次数？
```

#### 6. Prompt模板库验证
```
位置：backend/app/services/agent/prompt_library.py

验证项：
[ ] 文件是否存在？
[ ] get_content_prompt是否可用？
[ ] NovelPhase枚举是否定义？
[ ] 模板是否适合Chat场景？
```

### 验证结果记录模板

请将验证结果记录在此：

```markdown
## 验证结果（日期：____）

### 工具系统
- 验证结果：✅ 通过 / ❌ 失败 / ⚠️ 部分通过
- 实际情况：
- 与文档差异：
- 建议修改：

### Checkpointer集成
- 验证结果：✅ 通过 / ❌ 失败 / ⚠️ 部分通过
- 实际情况：
- 与文档差异：
- 建议修改：

### 模型选择器
- 验证结果：✅ 通过 / ❌ 失败 / ⚠️ 部分通过
- 实际情况：
- 与文档差异：
- 建议修改：

（其他组件...）
```

---

**文档版本**：v1.1（添加验证警告和清单）
**创建时间**：2025-01-06
**最后更新**：2025-01-06
**维护者**：Agent开发团队
**状态**：⚠️ 待验证

**相关文档**：
- [chat模式深度优化方案.md](./chat模式深度优化方案.md)
- [技术战略分析-Planning vs Chat.md](./技术战略分析-Planning%20vs%20Chat.md)
- [tasks/todo.md](../../tasks/todo.md) - 验证计划
