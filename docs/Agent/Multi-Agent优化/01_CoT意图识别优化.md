# CoT 意图识别优化设计文档

## 文档信息

| 项目 | 内容 |
|------|------|
| 版本 | v1.1.0 |
| 创建日期 | 2025-12-07 |
| 更新日期 | 2025-12-07 |
| 状态 | 设计中 |
| 优先级 | P1 - 性能优化 |

---

## 1. 问题背景

### 1.1 当前架构现状

> **注意**：当前系统已实现 AI 优先的意图分类架构，本文档聚焦于"快速路径"优化。

**已实现的功能**（`langgraph_agent.py:1602-1738`）：
- ✅ 极简规则快速通道 `_classify_intent_by_rules()` - 处理空消息、纯标点、章节模式
- ✅ AI 语义分类 `_ai_classify_intent()` - 置信度 < 0.9 时触发
- ✅ 5 种意图类型：writing, planning, analysis, stuck, general
- ✅ 路由决策函数 `_route_intent()`

**尚未实现的功能**（本文档重点）：
- ❌ 快速路径：简单查询直接执行工具，跳过 Planning
- ❌ 直接响应：问候等简单请求直接回答，无需工具

### 1.2 当前流程（需优化）

```
当前流程：
用户请求: "第五章的标题是什么？"
    │
    ├── _classify_intent() (AI优先，已实现)
    │   └── 判定为 general 或 writing 意图
    │
    └── 进入对应 Agent 节点
        ├── 构建 Prompt + 调用 LLM (3-5秒)
        ├── LLM 决策是否需要工具 (可能不需要)
        └── 总计: ~5-8秒 ← 简单查询不应该这么慢!
```

### 1.3 核心问题

| 问题 | 描述 |
|------|------|
| 缺少快速路径 | 简单查询（如"标题是什么"）仍需经过完整 Agent 流程 |
| 无直接响应机制 | 问候语也需要 LLM 判断，增加不必要延迟 |
| 意图粒度不足 | 当前只区分意图类型，不区分复杂度（simple/complex） |

### 1.4 期望效果

```
优化后流程：
用户请求: "第五章的标题是什么？"
    │
    └── _classify_intent_with_cot() (1-2秒，增强版)
        ├── Layer 1: query 类型 (复用现有 AI 分类)
        ├── Layer 2: simple 复杂度 (新增判断)
        └── Layer 3: 直接调用 get_chapter_by_order_tool
            │
            └── quick_tool_execute (新节点，~0.5秒)
                └── 返回标题
                    └── 总计: ~2秒 (提升 3-4x)
```

---

## 2. 设计方案

### 2.1 核心思路：在现有架构上增加复杂度判断

> **设计原则**：复用现有的 AI 意图分类，新增复杂度判断层，实现快速路径分流。

```
用户请求
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│  增强版意图识别 _classify_intent_with_cot()                  │
│                                                             │
│  Layer 1: 请求类型分析 (复用现有 _ai_classify_intent)        │
│           → writing / query / planning / analysis / general │
│                                                             │
│  Layer 2: 复杂度判断 (新增)                                  │
│           → simple（直接执行）/ complex（需要规划）          │
│                                                             │
│  Layer 3: 执行方案 (新增)                                    │
│           → 工具名 + 参数 / 直接回答 / 交给原有 Agent        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
    │
    ├── simple + tool    → quick_tool_execute（新节点）
    ├── simple + answer  → direct_response（新节点）
    └── complex          → 进入现有 Agent 节点（writing_agent 等）
```

### 2.2 三层思维链详解

#### Layer 1: 请求类型（复用现有分类）

> 复用 `_ai_classify_intent()` 的结果，无需重复实现。

| 类型 | 描述 | 示例 |
|------|------|------|
| `writing` | 创作内容（明确的写作指令） | "续写"、"改写"、"润色" |
| `planning` | 规划设计 | "写大纲"、"设计世界观"、"规划角色" |
| `analysis` | 分析评估 | "分析这段文字"、"评估质量" |
| `stuck` | 写作卡顿 | "写不下去了"、"需要灵感" |
| `general` | 通用对话/查询 | "标题是什么"、"有多少字"、"你好" |

#### Layer 2: 复杂度判断（新增）

**判断为 `simple` 的条件**：
- 只需要 1 个工具调用
- 或者可以直接回答（不需要工具）
- 没有依赖关系
- 没有多步骤

**判断为 `complex` 的条件**：
- 需要多个工具协作
- 有步骤依赖（先获取A，再用A做B）
- 涉及创作完整章节（触发 Multi-Agent）
- 需要分析后再行动

#### Layer 3: 执行方案（新增）

| 场景 | 方案 |
|------|------|
| simple + tool | 提供 tool_name + tool_args，进入 quick_tool_execute |
| simple + answer | 提供 direct_answer，进入 direct_response |
| complex | 留空，进入现有的 Agent 节点（writing_agent/planning_agent 等） |

---

## 3. Prompt 设计

### 3.1 复杂度判断 Prompt（新增，在意图分类后调用）

> **设计说明**：此 Prompt 在现有 `_ai_classify_intent()` 返回结果后调用，用于判断复杂度和执行方案。

```python
# 文件: backend/app/services/agent/prompt_cache.py

@cache_review(expire=3600, key_prefix="prompt")
async def get_complexity_decision_prompt() -> str:
    """复杂度判断 Prompt（在意图分类后调用）"""
    return """你是执行路径决策器。根据已识别的意图类型和用户请求，判断最优执行路径。

【输入信息】
- 意图类型: {intent} (已由意图分类器识别)
- 用户请求: {message}

【决策规则】

## 复杂度判断
问自己：这个请求需要复杂处理吗？

判断为 simple（可直接执行）的条件：
- 只需要 1 个工具调用（如获取标题、字数）
- 或者可以直接回答（如问候、简单问答）
- 没有依赖关系
- 没有多步骤

判断为 complex（需要完整流程）的条件：
- 需要多个工具协作
- 有步骤依赖（先获取A，再用A做B）
- 涉及创作完整章节
- 需要分析后再行动
- 意图类型为 writing/planning/analysis/stuck

## 执行方案
如果是 simple，给出具体方案：

工具调用时：
- tool_name: 工具名称
- tool_args: 参数
- response_hint: 返回字段提示（title/content/word_count）

直接回答时：
- direct_answer: 答案内容

【可用工具速查】

获取类（返回数据，无副作用）：
- get_chapter_by_order_tool(chapter_order: int) → {title, content, word_count}
- get_context_tool() → 作品上下文
- search_analysis_fragments_tool(query: str) → 搜索结果

【输出格式】

```json
{
  "complexity": "simple|complex",
  "reason": "判断依据（简短）",
  "action": {
    // simple + tool:
    "tool_name": "工具名",
    "tool_args": {},
    "response_hint": "title|content|word_count"

    // simple + answer:
    "direct_answer": "直接回答内容"

    // complex: 留空 {}
  }
}
```

请分析并返回 JSON："""
```

### 3.2 示例覆盖

#### 示例 1: 简单元数据查询

```
用户: "第五章的标题是什么"
已识别意图: general

复杂度判断结果:
{
  "complexity": "simple",
  "reason": "只需获取标题字段，单工具调用",
  "action": {
    "tool_name": "get_chapter_by_order_tool",
    "tool_args": {"chapter_order": 5},
    "response_hint": "title"
  }
}
```

#### 示例 2: 需要分析的查询

```
用户: "第三章讲了什么"
已识别意图: general

复杂度判断结果:
{
  "complexity": "complex",
  "reason": "需要先获取内容，再进行概括分析，多步骤依赖",
  "action": {}
}
```

#### 示例 3: 写作任务

```
用户: "续写第五章"
已识别意图: writing

复杂度判断结果:
{
  "complexity": "complex",
  "reason": "writing 意图默认为 complex，需要 Multi-Agent 流程",
  "action": {}
}
```

#### 示例 4: 简单问候

```
用户: "你好"
已识别意图: general

复杂度判断结果:
{
  "complexity": "simple",
  "reason": "简单问候，可直接回答",
  "action": {
    "direct_answer": "你好！我是 AI 写作助手，可以帮你续写章节、查看内容、分析情节。有什么可以帮你的吗？"
  }
}
```

---

## 4. 代码实现

### 4.1 增强版意图分类节点（在现有基础上扩展）

```python
# 文件: backend/app/services/agent/langgraph_agent.py

async def _classify_intent_with_cot(self, state: AgentState) -> AgentState:
    """增强版意图识别 - 在现有分类基础上增加复杂度判断

    流程：
    1. 调用现有的意图分类逻辑（复用 _classify_intent_by_rules + _ai_classify_intent）
    2. 新增：判断复杂度（simple/complex）
    3. 新增：如果 simple，确定执行方案

    Returns:
        AgentState: 包含 intent, intent_decision, agent_steps
    """

    message = state["messages"][-1].content
    logger.info(f"[Intent-CoT] 开始分析: {message[:50]}...")

    # ========== 步骤1: 复用现有意图分类 ==========
    intent, confidence = self._classify_intent_by_rules(message)
    classification_method = "快速通道"

    if confidence < 0.9:
        intent, confidence = await self._ai_classify_intent(message)
        classification_method = "AI语义分类"

    logger.info(f"[Intent-CoT] 意图: {intent} ({classification_method})")

    # ========== 步骤2: 复杂度判断 ==========
    # writing/planning/analysis/stuck 意图默认为 complex
    if intent in ("writing", "planning", "analysis", "stuck"):
        logger.info(f"[Intent-CoT] {intent} 意图默认为 complex")
        return {
            "intent": intent,
            "intent_decision": {"complexity": "complex", "action": {}},
            "agent_steps": [{
                "step": "intent_cot",
                "result": f"{intent}/complex (默认)",
            }]
        }

    # general 意图需要进一步判断复杂度
    complexity_decision = await self._judge_complexity(message, intent)

    logger.info(
        f"[Intent-CoT] 决策: intent={intent}, "
        f"complexity={complexity_decision.get('complexity', 'complex')}"
    )

    return {
        "intent": intent,
        "intent_decision": complexity_decision,
        "agent_steps": [{
            "step": "intent_cot",
            "result": f"{intent}/{complexity_decision.get('complexity', 'complex')}",
        }]
    }


async def _judge_complexity(self, message: str, intent: str) -> Dict:
    """判断请求复杂度并确定执行方案

    Args:
        message: 用户消息
        intent: 已识别的意图类型

    Returns:
        Dict: {"complexity": "simple|complex", "action": {...}}
    """
    from app.services.agent.prompt_cache import get_complexity_decision_prompt

    prompt_template = await get_complexity_decision_prompt()
    prompt = prompt_template.format(intent=intent, message=message)

    try:
        result = await self.ai_service.call_ai(
            system_prompt="你是执行路径决策器，返回严格的JSON格式。",
            user_prompt=prompt,
            max_tokens=300,
            temperature=0.1,
            task_type=TaskType.TEXT_CLASSIFICATION
        )

        decision = self._extract_json_from_text(result)
        if decision and decision.get("complexity"):
            return decision

    except Exception as e:
        logger.warning(f"[Intent-CoT] 复杂度判断失败: {e}，降级为 complex")

    # 降级：默认为 complex
    return {"complexity": "complex", "action": {}}
```

### 4.2 路由函数（新增快速路径分支）

```python
# 文件: backend/app/services/agent/langgraph_agent.py

def _route_after_intent_cot(self, state: AgentState) -> str:
    """根据 CoT 结果路由到对应节点

    路由规则：
    - simple + direct_answer → direct_response 节点（新增）
    - simple + tool_name → quick_tool_execute 节点（新增）
    - complex → 原有 Agent 节点（按意图路由）

    Returns:
        str: 目标节点名称
    """

    decision = state.get("intent_decision", {})
    complexity = decision.get("complexity", "complex")
    action = decision.get("action", {})
    intent = state.get("intent", "general")

    # ========== 快速路径（新增）==========
    if complexity == "simple":
        if action.get("direct_answer"):
            logger.info("[Route] → direct_response (直接回答)")
            return "direct_response"
        elif action.get("tool_name"):
            logger.info(f"[Route] → quick_tool_execute ({action['tool_name']})")
            return "quick_tool_execute"

    # ========== 原有路径（保持不变）==========
    # 复杂请求走原有的 Agent 节点
    logger.info(f"[Route] → {intent}_agent (complex)")
    return f"{intent}_agent"  # writing_agent, planning_agent, etc.
```

### 4.3 快速执行节点（新增）

```python
# 文件: backend/app/services/agent/langgraph_agent.py

async def _quick_tool_execute(self, state: AgentState) -> AgentState:
    """快速执行单工具（新增节点，跳过完整 Agent 流程）

    用于 simple + tool 场景，直接调用工具并格式化返回。

    Returns:
        AgentState: 包含 final_response, agent_steps
    """

    decision = state.get("intent_decision", {})
    action = decision.get("action", {})

    tool_name = action.get("tool_name")
    tool_args = action.get("tool_args", {})
    response_hint = action.get("response_hint")

    logger.info(f"[QuickExecute] 执行工具: {tool_name}, 参数: {tool_args}")

    # 1. 获取工具函数
    tool_func = self._get_tool_by_name(tool_name)
    if not tool_func:
        return {
            "final_response": f"未知工具: {tool_name}",
            "agent_steps": [{"step": "quick_tool_execute", "result": "工具不存在"}]
        }

    # 2. 执行工具
    try:
        result = await tool_func(**tool_args)
    except Exception as e:
        logger.error(f"[QuickExecute] 工具执行失败: {e}")
        return {
            "final_response": f"工具执行失败: {str(e)}",
            "agent_steps": [{"step": "quick_tool_execute", "result": f"错误: {e}"}]
        }

    # 3. 根据 hint 格式化响应
    response = self._format_tool_response(result, tool_args, response_hint)

    return {
        "final_response": response,
        "agent_steps": [{
            "step": "quick_tool_execute",
            "result": f"执行 {tool_name}",
            "tool_result": result
        }]
    }


def _format_tool_response(
    self,
    result: Any,
    tool_args: Dict,
    response_hint: Optional[str]
) -> str:
    """格式化工具响应

    根据 response_hint 提取特定字段并格式化为用户友好的响应。
    """
    if not response_hint or not isinstance(result, dict):
        return str(result)

    chapter_order = tool_args.get("chapter_order", "")

    if response_hint == "title":
        title = result.get("title", "未知")
        return f"第{chapter_order}章的标题是：**{title}**"

    elif response_hint == "word_count":
        word_count = result.get("word_count", 0)
        return f"第{chapter_order}章共 **{word_count}** 字"

    elif response_hint == "content":
        return result.get("content", "")

    else:
        return str(result)
```

### 4.4 直接响应节点（新增）

```python
# 文件: backend/app/services/agent/langgraph_agent.py

async def _direct_response(self, state: AgentState) -> AgentState:
    """直接返回答案（新增节点，无需工具）

    用于 simple + direct_answer 场景。

    Returns:
        AgentState: 包含 final_response, agent_steps
    """

    decision = state.get("intent_decision", {})
    action = decision.get("action", {})
    answer = action.get("direct_answer", "")

    logger.info(f"[DirectResponse] 返回预设答案")

    return {
        "final_response": answer,
        "agent_steps": [{
            "step": "direct_response",
            "result": "直接回答"
        }]
    }
```

### 4.5 工作流扩展（在现有基础上新增节点）

```python
# 文件: backend/app/services/agent/langgraph_agent.py

def _build_workflow(self) -> CompiledStateGraph:
    """构建 LangGraph 工作流

    在现有工作流基础上新增快速路径节点。
    """
    workflow = StateGraph(AgentState)

    # ========== 新增节点 ==========

    # 增强版意图识别（替换原有的 intent_classifier）
    workflow.add_node("intent_cot", self._classify_intent_with_cot)

    # 快速执行路径（新增）
    workflow.add_node("quick_tool_execute", self._quick_tool_execute)
    workflow.add_node("direct_response", self._direct_response)

    # ========== 保留原有节点 ==========
    workflow.add_node("writing_agent", self._handle_writing)
    workflow.add_node("planning_agent", self._handle_planning)
    workflow.add_node("analysis_agent", self._handle_analysis)
    workflow.add_node("stuck_agent", self._handle_stuck)
    workflow.add_node("general_agent", self._handle_general)
    workflow.add_node("tools", self._parallel_tool_node)

    # ========== 入口点 ==========
    workflow.set_entry_point("intent_cot")

    # ========== 条件路由（扩展）==========
    workflow.add_conditional_edges(
        "intent_cot",
        self._route_after_intent_cot,
        {
            # 新增快速路径
            "quick_tool_execute": "quick_tool_execute",
            "direct_response": "direct_response",
            # 原有路径
            "writing_agent": "writing_agent",
            "planning_agent": "planning_agent",
            "analysis_agent": "analysis_agent",
            "stuck_agent": "stuck_agent",
            "general_agent": "general_agent",
        }
    )

    # ========== 终止边 ==========
    # 快速路径直接结束
    workflow.add_edge("quick_tool_execute", END)
    workflow.add_edge("direct_response", END)

    # 原有路径继续...（省略）

    return workflow.compile(checkpointer=self.memory)
```

---

## 5. 工具注册

### 5.1 工具映射表

```python
# 文件: backend/app/services/agent/langgraph_agent.py

def _get_tool_by_name(self, tool_name: str) -> Optional[Callable]:
    """根据名称获取工具函数

    维护一个工具名到函数的映射表。
    """

    TOOL_REGISTRY = {
        # 获取类
        "get_chapter_by_order_tool": self._tool_get_chapter_by_order,
        "get_context_tool": self._tool_get_context,
        "search_analysis_fragments_tool": self._tool_search_fragments,

        # 分析类
        "analyze_text_tool": self._tool_analyze_text,

        # 注意：multi_agent_writing 不在此处，它需要走 Planning 流程
    }

    return TOOL_REGISTRY.get(tool_name)
```

---

## 6. 数据流图

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           用户请求                                       │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    intent_cot 节点（增强版）                             │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  步骤1: 复用现有意图分类                                           │  │
│  │  - _classify_intent_by_rules() 极简快速通道                       │  │
│  │  - _ai_classify_intent() AI 语义分类                              │  │
│  │  → 输出: intent (writing/planning/analysis/stuck/general)         │  │
│  │                                                                   │  │
│  │  步骤2: 复杂度判断（新增）                                         │  │
│  │  - writing/planning/analysis/stuck → 默认 complex                │  │
│  │  - general → 调用 _judge_complexity() 进一步判断                  │  │
│  │  → 输出: complexity (simple/complex), action                      │  │
│  └───────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
                    ┌───────────────┴───────────────┐
                    │     _route_after_intent_cot   │
                    └───────────────┬───────────────┘
                                    │
            ┌───────────────────────┼───────────────────────┐
            │                       │                       │
            ▼                       ▼                       ▼
    ┌───────────────┐       ┌───────────────┐       ┌───────────────┐
    │direct_response│       │quick_tool_exec│       │ 原有 Agent    │
    │    (新增)     │       │    (新增)     │       │(writing/plan..│
    │               │       │               │       │               │
    │ 直接返回答案  │       │ 执行单个工具  │       │ 完整 Agent    │
    │ (~1秒)        │       │ (~1.5秒)      │       │ 流程 (~5-30s) │
    └───────┬───────┘       └───────┬───────┘       └───────┬───────┘
            │                       │                       │
            ▼                       ▼                       ▼
    ┌───────────────┐       ┌───────────────┐       ┌───────────────┐
    │     END       │       │     END       │       │  继续执行...  │
    └───────────────┘       └───────────────┘       │  (工具/Multi-│
                                                    │   Agent等)   │
                                                    └───────────────┘
```

---

## 7. 性能对比

### 7.1 响应时间对比

| 场景 | 优化前 | 优化后 | 提升 |
|------|--------|--------|------|
| "第五章标题是什么" | ~5-8秒 | ~2秒 | **3-4x** |
| "你好" | ~3-5秒 | ~1.5秒 | **2-3x** |
| "第三章有多少字" | ~5-8秒 | ~2秒 | **3-4x** |
| "第三章讲了什么" | ~15-25秒 | ~15-25秒 | 无变化 (需要分析) |
| "续写第五章" | ~120-180秒 | ~120-180秒 | 无变化 (需要 Multi-Agent) |

### 7.2 LLM 调用次数

| 场景 | 优化前 | 优化后 | 说明 |
|------|--------|--------|------|
| 简单查询 | 2次 (意图+Agent) | 2次 (意图+复杂度) | 次数相同，但第二次更轻量 |
| 复杂查询 | 2-3次 | 2-3次 | 无变化 |
| 写作任务 | 6+次 | 6+次 | 无变化 |

### 7.3 关键优化点

1. **跳过 Agent 节点**：简单查询直接执行工具，不经过完整 Agent 决策
2. **直接响应**：问候等简单请求无需工具调用
3. **复用现有分类**：不重复实现意图分类，只新增复杂度判断

---

## 8. 测试用例

### 8.1 单元测试

```python
# 文件: backend/tests/test_intent_cot.py

import pytest
from app.services.agent.langgraph_agent import WritingAgentGraph

class TestIntentCoT:

    @pytest.fixture
    async def agent(self):
        return WritingAgentGraph(...)

    async def test_simple_title_query(self, agent):
        """测试简单标题查询走快速路径"""
        state = {"messages": [HumanMessage(content="第五章的标题是什么")]}
        result = await agent._classify_intent_with_cot(state)

        assert result["intent"] == "query"
        assert result["intent_decision"]["complexity"] == "simple"
        assert result["intent_decision"]["action"]["tool_name"] == "get_chapter_by_order_tool"

    async def test_complex_summary_query(self, agent):
        """测试需要分析的查询走 Planning 路径"""
        state = {"messages": [HumanMessage(content="第三章讲了什么")]}
        result = await agent._classify_intent_with_cot(state)

        assert result["intent_decision"]["complexity"] == "complex"

    async def test_greeting_direct_response(self, agent):
        """测试问候直接返回"""
        state = {"messages": [HumanMessage(content="你好")]}
        result = await agent._classify_intent_with_cot(state)

        assert result["intent_decision"]["complexity"] == "simple"
        assert "direct_answer" in result["intent_decision"]["action"]
```

### 8.2 集成测试

```python
async def test_end_to_end_simple_query(self, agent):
    """端到端测试：简单查询"""
    response = await agent.chat(
        message="第五章的标题是什么",
        work_id="xxx",
        chapter_id="xxx"
    )

    # 验证走了快速路径
    assert "quick_tool_execute" in [s["step"] for s in response["agent_steps"]]
    assert "第五章的标题是" in response["response"]
```

---

## 9. 监控指标

### 9.1 新增指标

```python
# 路由分布
increment_counter("intent_cot_route", labels={
    "route": "quick_tool_execute" | "direct_response" | "planning"
})

# 快速路径命中率
quick_path_hit_rate = quick_path_count / total_requests

# CoT 解析成功率
cot_parse_success_rate = parse_success_count / total_cot_calls
```

### 9.2 日志格式

```
[Intent-CoT] 开始分析: 第五章的标题是什么...
[Intent-CoT] Layer1=query - 用户想知道标题, Layer2=simple - 只需一个工具
[Intent-CoT] 决策: type=query, complexity=simple
[Route] → quick_tool_execute (get_chapter_by_order_tool)
[QuickExecute] 执行工具: get_chapter_by_order_tool, 参数: {'chapter_order': 5}
```

---

## 10. 回滚方案

如果 CoT 意图识别出现问题，可以快速回滚：

```python
# 配置开关
ENABLE_INTENT_COT = os.getenv("ENABLE_INTENT_COT", "true").lower() == "true"

def _build_workflow(self):
    if ENABLE_INTENT_COT:
        workflow.set_entry_point("intent_cot")
    else:
        workflow.set_entry_point("intent_classifier")  # 原有节点
```

---

## 11. 实施计划

| 阶段 | 任务 | 说明 |
|------|------|------|
| 1 | 实现复杂度判断 Prompt | 新增 `get_complexity_decision_prompt()` |
| 2 | 实现 `_judge_complexity()` | 在现有意图分类后调用 |
| 3 | 实现 `_classify_intent_with_cot()` | 整合意图分类 + 复杂度判断 |
| 4 | 实现快速执行节点 | `quick_tool_execute` + `direct_response` |
| 5 | 扩展工作流路由 | 修改 `_build_workflow()` |
| 6 | 单元测试 | 覆盖各种场景 |
| 7 | 集成测试 + 灰度发布 | 验证性能提升 |

---

## 12. 风险评估

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|----------|
| 复杂度判断失败 | 低 | 低 | 降级到原有 Agent 流程（complex） |
| 误判 simple/complex | 中 | 中 | 保守策略：不确定时默认 complex |
| 快速路径工具报错 | 低 | 低 | 捕获异常，返回友好错误信息 |
| 与现有代码冲突 | 低 | 中 | 逐步替换，支持回滚开关 |

---

## 13. 回滚方案

```python
# 配置开关（支持快速回滚）
ENABLE_QUICK_PATH = os.getenv("ENABLE_QUICK_PATH", "true").lower() == "true"

def _build_workflow(self):
    if ENABLE_QUICK_PATH:
        workflow.set_entry_point("intent_cot")  # 新版
    else:
        workflow.set_entry_point("intent_classifier")  # 原有节点
```

---

## 14. 与现有代码的关系

| 现有代码 | 本方案 | 关系 |
|---------|--------|------|
| `_classify_intent_by_rules()` | 复用 | 作为快速通道 |
| `_ai_classify_intent()` | 复用 | 作为 AI 分类 |
| `_classify_intent()` | 替换 | 被 `_classify_intent_with_cot()` 替换 |
| `_route_intent()` | 扩展 | 增加快速路径分支 |
| `writing_agent` 等 | 保留 | complex 请求继续使用 |
