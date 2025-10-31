# P0-2: Hierarchical Supervisor 架构

> 优先级：🔴 P0（核心功能）
>
> 工作量：3-4天
>
> 预期收益：清晰职责划分、支持复杂任务、易扩展

---

## 📋 问题描述

### 当前架构（扁平化）

```
intent_classifier
    ↓
┌───┴───┬───────┬──────────┬────────┐
│       │       │          │        │
writing planning analysis  stuck  general
```

### 存在的问题

1. **❌ 无协调者**：所有 Agent 平级，复杂任务难以协调
2. **❌ 职责不清**：每个 Agent 既要决策又要执行
3. **❌ 扩展性差**：添加新 Agent 需要修改路由逻辑
4. **❌ 错误处理弱**：失败后无法动态调整策略

---

## 🎯 解决方案：三层 Supervisor 架构

```
                    ┌──────────────────┐
                    │  Main Supervisor │  ← 顶层：总协调
                    │  (路由到团队)     │
                    └────────┬─────────┘
                             │
           ┌─────────────────┼─────────────────┐
           │                 │                 │
    ┌──────▼──────┐   ┌─────▼──────┐   ┌─────▼──────┐
    │Writing Team │   │Planning Team│   │Analysis Team│
    │  Supervisor │   │  Supervisor  │   │  Supervisor │  ← 中层：团队管理
    └──────┬──────┘   └──────┬──────┘   └──────┬──────┘
           │                 │                 │
    ┌──────┴──────┐   ┌─────┴──────┐   ┌─────┴──────┐
    │             │   │            │   │            │
 ┌──▼──┐  ┌──▼──┐ │ ┌▼───┐ ┌▼────┐│ ┌▼────┐ ┌▼────┐ │  ← 底层：执行 Agent
 │续写 │  │润色 │ │ │大纲│ │角色 ││ │评估 │ │诊断 │ │
 └─────┘  └─────┘ │ └────┘ └─────┘│ └─────┘ └─────┘ │
    │             │   │            │   │            │
 ┌──▼──┐          │ ┌▼────┐        │ ┌▼────┐        │
 │扩写 │          │ │世界观│        │ │建议 │        │
 └─────┘          │ └─────┘        │ └─────┘        │
```

---

## 🔧 实现步骤

### Step 1: 定义状态结构

```python
# backend/app/services/agent/states.py
from typing import TypedDict, Annotated, List, Dict, Any, Optional
from enum import Enum
import operator

class TeamType(str, Enum):
    """团队类型"""
    WRITING = "writing"
    PLANNING = "planning"
    ANALYSIS = "analysis"

class AgentRole(str, Enum):
    """Agent 角色"""
    # Writing Team
    CONTINUE_WRITER = "continue_writer"
    POLISHER = "polisher"
    EXPANDER = "expander"

    # Planning Team
    OUTLINER = "outliner"
    CHARACTER_CREATOR = "character_creator"
    WORLDVIEW_CREATOR = "worldview_creator"

    # Analysis Team
    EVALUATOR = "evaluator"
    DIAGNOSER = "diagnoser"
    ADVISOR = "advisor"

class SupervisorState(TypedDict):
    """Supervisor 状态"""
    # 基础信息
    messages: Annotated[List[Any], operator.add]
    user_id: str
    work_id: Optional[str]
    chapter_id: Optional[str]

    # 任务信息
    original_request: str           # 原始请求
    current_task: Optional[str]     # 当前任务描述
    task_queue: List[Dict[str, Any]]  # 任务队列

    # 团队和角色
    assigned_team: Optional[TeamType]  # 分配的团队
    assigned_agent: Optional[AgentRole]  # 分配的 Agent

    # 执行状态
    team_results: Dict[str, Any]    # 各团队的执行结果
    agent_results: Dict[str, Any]   # 各 Agent 的执行结果
    execution_history: List[Dict]   # 执行历史

    # 上下文
    context: Dict[str, Any]
    metadata: Dict[str, Any]

    # 最终响应
    final_response: Optional[str]
```

### Step 2: 实现 Main Supervisor

```python
# backend/app/services/agent/supervisors/main_supervisor.py
from langgraph.graph import StateGraph, END
from typing import Literal
import logging

logger = logging.getLogger(__name__)

class MainSupervisor:
    """主 Supervisor - 顶层协调者"""

    def __init__(self, ai_service):
        self.ai_service = ai_service
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        """构建主 Supervisor 图"""

        workflow = StateGraph(SupervisorState)

        # 添加节点
        workflow.add_node("classify_task", self._classify_task)
        workflow.add_node("route_to_team", self._route_to_team)
        workflow.add_node("writing_team", self._invoke_writing_team)
        workflow.add_node("planning_team", self._invoke_planning_team)
        workflow.add_node("analysis_team", self._invoke_analysis_team)
        workflow.add_node("synthesize_results", self._synthesize_results)

        # 设置入口
        workflow.set_entry_point("classify_task")

        # 路由逻辑
        workflow.add_edge("classify_task", "route_to_team")

        workflow.add_conditional_edges(
            "route_to_team",
            self._decide_team,
            {
                "writing": "writing_team",
                "planning": "planning_team",
                "analysis": "analysis_team"
            }
        )

        # 各团队完成后汇总
        workflow.add_edge("writing_team", "synthesize_results")
        workflow.add_edge("planning_team", "synthesize_results")
        workflow.add_edge("analysis_team", "synthesize_results")

        workflow.add_edge("synthesize_results", END)

        return workflow

    async def _classify_task(self, state: SupervisorState) -> SupervisorState:
        """分类任务：识别用户意图和任务类型"""

        user_request = state["original_request"]

        # 使用 LLM 进行任务分类
        prompt = f"""
你是一个任务分类专家。分析用户请求，识别任务类型和所需团队。

用户请求: {user_request}

可选团队:
- writing: 内容创作（续写、润色、扩写）
- planning: 规划设计（大纲、角色、世界观）
- analysis: 分析评估（评估质量、诊断问题、提供建议）

请以 JSON 格式返回:
{{
    "team": "团队名称",
    "task_description": "任务描述",
    "subtasks": ["子任务1", "子任务2"],
    "priority": "high/medium/low"
}}
"""

        response = await self.ai_service.generate(prompt, temperature=0.3)

        # 解析响应
        import json
        task_info = json.loads(response)

        state["assigned_team"] = task_info["team"]
        state["current_task"] = task_info["task_description"]
        state["task_queue"] = [
            {"task": subtask, "status": "pending"}
            for subtask in task_info.get("subtasks", [])
        ]

        logger.info(f"[Main Supervisor] 任务分类: {task_info['team']}")

        return state

    def _decide_team(self, state: SupervisorState) -> Literal["writing", "planning", "analysis"]:
        """决定路由到哪个团队"""
        return state["assigned_team"]

    async def _invoke_writing_team(self, state: SupervisorState) -> SupervisorState:
        """调用写作团队"""

        logger.info("[Main Supervisor] 调用 Writing Team")

        # 创建写作团队 Supervisor
        from .writing_team_supervisor import WritingTeamSupervisor
        writing_team = WritingTeamSupervisor(self.ai_service)

        # 执行
        result = await writing_team.execute(state)

        # 保存结果
        state["team_results"]["writing"] = result

        return state

    async def _invoke_planning_team(self, state: SupervisorState) -> SupervisorState:
        """调用规划团队"""

        logger.info("[Main Supervisor] 调用 Planning Team")

        from .planning_team_supervisor import PlanningTeamSupervisor
        planning_team = PlanningTeamSupervisor(self.ai_service)

        result = await planning_team.execute(state)
        state["team_results"]["planning"] = result

        return state

    async def _invoke_analysis_team(self, state: SupervisorState) -> SupervisorState:
        """调用分析团队"""

        logger.info("[Main Supervisor] 调用 Analysis Team")

        from .analysis_team_supervisor import AnalysisTeamSupervisor
        analysis_team = AnalysisTeamSupervisor(self.ai_service)

        result = await analysis_team.execute(state)
        state["team_results"]["analysis"] = result

        return state

    async def _synthesize_results(self, state: SupervisorState) -> SupervisorState:
        """综合各团队结果，生成最终响应"""

        team_results = state["team_results"]

        # 使用 LLM 综合结果
        prompt = f"""
请根据以下团队的执行结果，生成最终的用户响应。

用户请求: {state['original_request']}

团队结果:
{json.dumps(team_results, ensure_ascii=False, indent=2)}

要求:
1. 简洁明了
2. 突出重点
3. 如有建议，清晰列出
"""

        final_response = await self.ai_service.generate(prompt, temperature=0.7)

        state["final_response"] = final_response

        logger.info("[Main Supervisor] 任务完成")

        return state
```

### Step 3: 实现 Writing Team Supervisor

```python
# backend/app/services/agent/supervisors/writing_team_supervisor.py
from langgraph.graph import StateGraph, END
from typing import Literal
import logging

logger = logging.getLogger(__name__)

class WritingTeamSupervisor:
    """写作团队 Supervisor"""

    def __init__(self, ai_service):
        self.ai_service = ai_service
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        """构建写作团队图"""

        workflow = StateGraph(SupervisorState)

        # 添加节点
        workflow.add_node("assign_agent", self._assign_agent)
        workflow.add_node("continue_writer", self._execute_continue_writer)
        workflow.add_node("polisher", self._execute_polisher)
        workflow.add_node("expander", self._execute_expander)
        workflow.add_node("review_result", self._review_result)

        # 入口
        workflow.set_entry_point("assign_agent")

        # 路由
        workflow.add_conditional_edges(
            "assign_agent",
            self._decide_agent,
            {
                "continue_writer": "continue_writer",
                "polisher": "polisher",
                "expander": "expander"
            }
        )

        # 各 Agent 完成后评审
        workflow.add_edge("continue_writer", "review_result")
        workflow.add_edge("polisher", "review_result")
        workflow.add_edge("expander", "review_result")

        # 评审后决定是否需要重做
        workflow.add_conditional_edges(
            "review_result",
            self._decide_next,
            {
                "done": END,
                "retry": "assign_agent"  # 重试
            }
        )

        return workflow

    async def _assign_agent(self, state: SupervisorState) -> SupervisorState:
        """分配具体的 Agent"""

        task = state["current_task"]

        # 使用 LLM 决定使用哪个 Agent
        prompt = f"""
任务: {task}

可用 Agent:
- continue_writer: 续写内容（延续现有故事）
- polisher: 润色文本（改进语言表达）
- expander: 扩写内容（增加细节描写）

选择最合适的 Agent（只返回 Agent 名称）:
"""

        agent_name = await self.ai_service.generate(prompt, temperature=0.2, max_tokens=50)
        agent_name = agent_name.strip().lower()

        state["assigned_agent"] = agent_name

        logger.info(f"[Writing Team] 分配 Agent: {agent_name}")

        return state

    def _decide_agent(self, state: SupervisorState) -> str:
        """决定调用哪个 Agent"""
        return state["assigned_agent"]

    async def _execute_continue_writer(self, state: SupervisorState) -> SupervisorState:
        """执行续写"""

        logger.info("[Writing Team] 执行续写")

        # 调用续写工具
        from app.services.agent.tools import continue_writing_tool

        result = await continue_writing_tool(
            work_id=state["work_id"],
            chapter_id=state["chapter_id"],
            prompt=state["current_task"],
            style_requirements=""
        )

        state["agent_results"]["continue_writer"] = result

        return state

    async def _execute_polisher(self, state: SupervisorState) -> SupervisorState:
        """执行润色"""

        logger.info("[Writing Team] 执行润色")

        from app.services.agent.tools import polish_text_tool

        result = await polish_text_tool(
            text=state.get("target_text", ""),
            style="professional"
        )

        state["agent_results"]["polisher"] = result

        return state

    async def _execute_expander(self, state: SupervisorState) -> SupervisorState:
        """执行扩写"""

        logger.info("[Writing Team] 执行扩写")

        # 扩写逻辑
        # ...

        return state

    async def _review_result(self, state: SupervisorState) -> SupervisorState:
        """评审结果质量"""

        agent_name = state["assigned_agent"]
        result = state["agent_results"].get(agent_name)

        # 简单质量检查
        if not result or len(result) < 100:
            state["metadata"]["quality_check"] = "failed"
            state["metadata"]["retry_count"] = state["metadata"].get("retry_count", 0) + 1
        else:
            state["metadata"]["quality_check"] = "passed"

        return state

    def _decide_next(self, state: SupervisorState) -> Literal["done", "retry"]:
        """决定下一步"""

        quality = state["metadata"].get("quality_check")
        retry_count = state["metadata"].get("retry_count", 0)

        if quality == "passed" or retry_count >= 3:
            return "done"
        else:
            return "retry"

    async def execute(self, state: SupervisorState) -> Dict[str, Any]:
        """执行写作团队任务"""

        # 编译图
        app = self.graph.compile()

        # 执行
        result = await app.ainvoke(state)

        return {
            "team": "writing",
            "agent": result["assigned_agent"],
            "result": result["agent_results"],
            "quality": result["metadata"].get("quality_check")
        }
```

### Step 4: 集成到现有系统

```python
# backend/app/services/agent/langgraph_agent.py

class WritingAgentGraph:
    """主 Agent 类（使用 Supervisor 架构）"""

    def __init__(self, ai_service: HTTPAIService, use_chatgpt: bool = False):
        self.ai_service = ai_service
        self.use_chatgpt = use_chatgpt

        # ⭐ 创建 Main Supervisor
        from app.services.agent.supervisors.main_supervisor import MainSupervisor
        self.main_supervisor = MainSupervisor(ai_service)

        # Checkpointer
        self.checkpointer = None

    async def chat(self, message: str, work_id: str, chapter_id: str,
                   conversation_id: str, context: Dict) -> Dict[str, Any]:
        """对话接口（使用 Supervisor）"""

        # 确保 Checkpointer
        await self._ensure_checkpointer()

        # 编译图
        app = self.main_supervisor.graph.compile(checkpointer=self.checkpointer)

        # 准备初始状态
        initial_state = {
            "messages": [],
            "user_id": context.get("user_id"),
            "work_id": work_id,
            "chapter_id": chapter_id,
            "original_request": message,
            "current_task": None,
            "task_queue": [],
            "assigned_team": None,
            "assigned_agent": None,
            "team_results": {},
            "agent_results": {},
            "execution_history": [],
            "context": context,
            "metadata": {},
            "final_response": None
        }

        # 配置
        config = {
            "configurable": {
                "thread_id": conversation_id
            }
        }

        # 执行
        result = await app.ainvoke(initial_state, config=config)

        return {
            "response": result["final_response"],
            "conversation_id": conversation_id,
            "agent_steps": result["execution_history"],
            "metadata": {
                "team": result["assigned_team"],
                "agent": result["assigned_agent"]
            }
        }
```

---

## 📊 架构优势

### 1. 清晰的职责划分

| 层级 | 职责 | 示例 |
|------|------|------|
| Main Supervisor | 任务分类、团队路由 | "这是写作任务，交给 Writing Team" |
| Team Supervisor | Agent 分配、质量把控 | "这需要续写，交给 Continue Writer" |
| Worker Agent | 具体执行 | 调用工具完成任务 |

### 2. 支持复杂任务

```
用户: "帮我完善第三章：先分析质量，再润色，最后扩写到 2000 字"

Main Supervisor: 分解为 3 个子任务
  ↓
  1. Analysis Team → Evaluator Agent → 质量分析
  2. Writing Team → Polisher Agent → 润色
  3. Writing Team → Expander Agent → 扩写到 2000 字
  ↓
Main Supervisor: 汇总结果，生成响应
```

### 3. 灵活扩展

```python
# 添加新团队：只需实现 Supervisor
class TranslationTeamSupervisor:
    """翻译团队"""
    # ...

# 在 Main Supervisor 中注册
workflow.add_node("translation_team", self._invoke_translation_team)
```

---

## 🎯 使用示例

### 简单任务（单 Agent）

```python
# 用户: "润色这段文字"
# → Main Supervisor → Writing Team → Polisher Agent
# → 一步完成
```

### 复杂任务（多 Agent 协作）

```python
# 用户: "我想写玄幻小说"
# → Main Supervisor → Planning Team
#     ├─ Worldview Creator: 创建世界观
#     ├─ Character Creator: 创建主角
#     └─ Outliner: 生成大纲
# → Main Supervisor 汇总结果
```

---

## 📚 参考资源

- **LangGraph Supervisor 库**：https://github.com/langchain-ai/langgraph-supervisor-py
- **Multi-Agent 教程**：https://github.com/langchain-ai/langgraph/blob/main/docs/docs/tutorials/multi_agent/agent_supervisor.md
- **Hierarchical Architecture**：https://github.com/Ashot72/Langgraph.js-Hierarchical-Multi-Agent-AI

---

## ✅ 完成标准

- [ ] Main Supervisor 实现
- [ ] Writing Team Supervisor 实现
- [ ] Planning Team Supervisor 实现
- [ ] Analysis Team Supervisor 实现
- [ ] 单元测试覆盖率 > 80%
- [ ] 端到端测试通过
- [ ] 性能测试（复杂任务 < 10s）

---

**下一步**：实施完成后，继续 [Reflection 反思机制](./03-reflection-pattern.md)
