# 03 - 后端实现

> 模块化设计：DeepAgent 逻辑独立于 langgraph_agent.py

## 1. 设计原则

**核心原则**：`langgraph_agent.py` 已有 5000+ 行，**不再往里添加大量代码**。

### 1.1 目录结构

```
backend/app/services/agent/
├── langgraph_agent.py           # +6-8 行（导入 + 参数 + 分支）
│
└── deep_agent/                  # 新增目录
    ├── __init__.py              # 导出接口
    ├── executor.py              # DeepAgentExecutor 核心类
    ├── reflection.py            # think_tool + 反思逻辑
    └── config.py                # 配置常量

backend/app/api/v1/
└── agent.py                     # +3-5 行（传递 enable_reflection 参数）

backend/app/models/
└── chat_models.py               # +1-2 行（请求模型添加字段）
```

### 1.2 改动量

| 文件 | 类型 | 行数 | 说明 |
|------|------|------|------|
| `langgraph_agent.py` | 修改 | **+6-8 行** | 导入 + 参数 + if 分支 |
| `agent.py` | 修改 | **+3-5 行** | 传递 enable_reflection |
| `chat_models.py` | 修改 | **+1-2 行** | 添加请求字段 |
| `deep_agent/__init__.py` | 新建 | ~10 行 | 导出接口 |
| `deep_agent/config.py` | 新建 | ~20 行 | 配置常量 |
| `deep_agent/reflection.py` | 新建 | ~80 行 | think_tool |
| `deep_agent/executor.py` | 新建 | ~150 行 | DeepAgentExecutor |
| **总计后端** | | **~280 行** | |

## 2. API 层改动（agent.py）

### 2.1 请求模型添加字段

```python
# backend/app/models/chat_models.py

class AgentChatRequest(BaseModel):
    message: str
    work_id: Optional[str] = None
    chapter_id: Optional[str] = None
    context: Optional[dict] = None
    mode: Optional[ChatMode] = ChatMode.PLANNING
    enable_reflection: bool = False  # 新增：是否启用反思
```

### 2.2 传递参数到 chat_with_planning

```python
# backend/app/api/v1/agent.py

# 在 agent_chat_stream 函数中
if actual_mode == ChatMode.PLANNING:
    result = await agent_graph.chat_with_planning(
        message=request.message,
        user_id=user_id,
        work_id=request.work_id,
        chapter_id=request.chapter_id,
        conversation_id=conversation_id,
        context=context,
        on_plan=on_plan,
        on_task_start=on_task_start,
        on_task_progress=on_task_progress,
        on_task_done=on_task_done,
        on_content=on_content,
        db=db,
        enable_reflection=request.enable_reflection,  # 新增
    )
```

## 3. langgraph_agent.py 改动

### 3.1 添加导入

```python
# 在文件顶部导入区添加 1 行
from .deep_agent import DeepAgentExecutor
```

### 3.2 在 chat_with_planning 中调用

找到 `chat_with_planning` 方法（约行 3785），添加参数和分支：

```python
async def chat_with_planning(
    self,
    message: str,
    ...
    on_task_progress: Optional[callable] = None,  # 现有参数，用于发送反思
    ...
    enable_reflection: bool = False,  # 新增参数
) -> Dict[str, Any]:

    # ... 现有的 Planning 阶段代码 ...

    # ════════════════════════════════════════════
    # 新增：如果启用反思，使用 DeepAgentExecutor 包装
    # ════════════════════════════════════════════
    if enable_reflection:
        executor = DeepAgentExecutor(
            agent_graph=self,
            on_plan=on_plan,
            on_task_start=on_task_start,
            on_task_progress=on_task_progress,  # 用于发送反思内容
            on_task_done=on_task_done,
            on_content=on_content
        )
        return await executor.execute_with_reflection(plan, context)
    # ════════════════════════════════════════════

    # ... 现有的 Execution 阶段代码（不变）...
```

## 4. deep_agent/config.py

```python
# backend/app/services/agent/deep_agent/config.py

"""DeepAgent 配置常量"""


class DeepAgentConfig:
    """DeepAgent 配置"""

    # 反思限制
    MAX_REFLECTIONS = 3      # 单次请求最多反思次数
    MAX_REPLANS = 2          # 单次请求最多重规划次数

    # 超时设置
    REFLECTION_TIMEOUT = 30  # 反思超时（秒）
    REPLAN_TIMEOUT = 45      # 重规划超时（秒）

    # 反思触发条件
    REFLECT_ON_FAILURE = True           # 任务失败时反思
    REFLECT_ON_LOW_QUALITY = True       # 低质量结果时反思
    QUALITY_THRESHOLD = 0.6             # 质量阈值
    REFLECT_ON_ANALYSIS = True          # 分析类任务后反思
    REFLECT_EVERY_N_TASKS = 3           # 每 N 个任务反思一次
```

## 4. deep_agent/reflection.py

```python
# backend/app/services/agent/deep_agent/reflection.py

"""反思工具和逻辑"""

import json
import logging
import asyncio
from dataclasses import dataclass
from typing import Dict, Any, List, Optional

from .config import DeepAgentConfig

logger = logging.getLogger(__name__)


@dataclass
class ReflectionResult:
    """反思结果"""
    reflection: str           # 反思内容
    needs_replan: bool        # 是否需要重规划
    suggested_tasks: Optional[List[str]] = None


async def think_tool(
    task: Dict[str, Any],
    result: Dict[str, Any],
    remaining_tasks: List[Dict[str, Any]],
    context: Dict[str, Any],
    ai_service,
) -> ReflectionResult:
    """反思工具

    纯上下文工程工具，迫使 Agent 在关键节点评估进度。
    """
    prompt = _build_reflection_prompt(task, result, remaining_tasks)

    try:
        response = await asyncio.wait_for(
            ai_service.chat(prompt),
            timeout=DeepAgentConfig.REFLECTION_TIMEOUT
        )
        return _parse_reflection_response(response)
    except asyncio.TimeoutError:
        logger.warning("反思超时")
        return ReflectionResult(reflection="反思超时", needs_replan=False)
    except Exception as e:
        logger.error(f"反思失败: {e}")
        return ReflectionResult(reflection=str(e), needs_replan=False)


def _build_reflection_prompt(
    task: Dict[str, Any],
    result: Dict[str, Any],
    remaining_tasks: List[Dict[str, Any]],
) -> str:
    """构建反思 Prompt"""
    task_desc = task.get("description", "未知任务")
    task_status = result.get("status", "unknown")
    task_output = str(result.get("output", result.get("content", "")))[:300]

    remaining_str = "\n".join([
        f"  - {t.get('description', '未知')}"
        for t in remaining_tasks[:5]
    ]) if remaining_tasks else "  (无)"

    return f"""你是一个 AI Agent，刚完成了一个任务。请简短反思。

## 刚完成的任务
- 描述: {task_desc}
- 状态: {task_status}
- 输出: {task_output}...

## 剩余任务
{remaining_str}

## 请思考
1. 结果是否达到预期？
2. 是否需要补充信息？
3. 是否需要调整计划？

## 输出格式（JSON）
{{"reflection": "简短反思（<100字）", "needs_replan": true/false}}
"""


def _parse_reflection_response(response: str) -> ReflectionResult:
    """解析反思响应"""
    try:
        data = json.loads(response)
        return ReflectionResult(
            reflection=data.get("reflection", response),
            needs_replan=data.get("needs_replan", False),
        )
    except json.JSONDecodeError:
        needs_replan = any(kw in response for kw in ["需要", "补充", "调整", "不足"])
        return ReflectionResult(reflection=response, needs_replan=needs_replan)


def should_reflect(
    task: Dict[str, Any],
    result: Dict[str, Any],
    completed_count: int,
    reflection_count: int,
) -> bool:
    """判断是否需要触发反思"""
    config = DeepAgentConfig

    # 达到上限
    if reflection_count >= config.MAX_REFLECTIONS:
        return False

    # 任务失败
    if config.REFLECT_ON_FAILURE and result.get("status") == "failed":
        return True

    # 低质量
    if config.REFLECT_ON_LOW_QUALITY:
        quality = result.get("quality_score", 1.0)
        if quality < config.QUALITY_THRESHOLD:
            return True

    # 分析类任务
    if config.REFLECT_ON_ANALYSIS:
        desc = task.get("description", "").lower()
        if "分析" in desc or task.get("type") == "analysis":
            return True

    # 定期反思
    if completed_count > 0 and completed_count % config.REFLECT_EVERY_N_TASKS == 0:
        return True

    return False
```

## 5. deep_agent/executor.py

### 5.1 与 MultiAgentExecutor 的协作关系

```
┌─────────────────────────────────────────────────────────────────┐
│                    DeepAgentExecutor                             │
│  职责：在任务执行之间插入反思检查点                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   for task in plan.tasks:                                        │
│       │                                                          │
│       ▼                                                          │
│   ┌─────────────────────────────────────────┐                   │
│   │ 调用 agent._execute_task_in_parallel    │ ← 复用现有执行逻辑  │
│   │ 或 MultiAgentExecutor（写作类任务）       │                   │
│   └─────────────────────────────────────────┘                   │
│       │                                                          │
│       ▼                                                          │
│   ┌─────────────────────────────────────────┐                   │
│   │ should_reflect() → think_tool()         │ ← 新增反思检查点   │
│   │ 通过 on_task_progress 发送反思内容       │                   │
│   └─────────────────────────────────────────┘                   │
│       │                                                          │
│       ▼                                                          │
│   ┌─────────────────────────────────────────┐                   │
│   │ 需要重规划？ → 更新 tasks 列表           │                   │
│   │ 通过 on_plan 发送更新事件                │                   │
│   └─────────────────────────────────────────┘                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 完整代码

```python
# backend/app/services/agent/deep_agent/executor.py

"""DeepAgent 执行器

包装现有的 Planning 执行流程，添加反思循环。
"""

import json
import logging
import asyncio
from datetime import datetime
from typing import Dict, Any, List, Optional, Callable

from .config import DeepAgentConfig
from .reflection import think_tool, should_reflect, ReflectionResult

logger = logging.getLogger(__name__)


class DeepAgentExecutor:
    """DeepAgent 执行器

    包装 WritingAgentGraph 的执行流程，添加反思能力。
    不修改原有代码，仅在执行过程中插入反思检查点。

    与 MultiAgentExecutor 的关系：
    - DeepAgentExecutor 负责「任务间」的反思和重规划
    - MultiAgentExecutor 负责「写作类任务内部」的多 Agent 协作
    - 两者是组合关系，DeepAgentExecutor 通过 agent._execute_task_in_parallel 间接调用 MultiAgentExecutor
    """

    def __init__(
        self,
        agent_graph,  # WritingAgentGraph 实例
        on_plan: Optional[Callable] = None,
        on_task_start: Optional[Callable] = None,
        on_task_progress: Optional[Callable] = None,  # 新增：用于发送反思内容
        on_task_done: Optional[Callable] = None,
        on_content: Optional[Callable] = None,
    ):
        self.agent = agent_graph
        self.on_plan = on_plan
        self.on_task_start = on_task_start
        self.on_task_progress = on_task_progress  # 复用现有事件发送反思
        self.on_task_done = on_task_done
        self.on_content = on_content

        # 状态
        self.reflection_count = 0
        self.replan_count = 0
        self.reflections = []

    async def execute_with_reflection(
        self,
        plan: Dict[str, Any],
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """带反思的执行流程

        Args:
            plan: 初始计划（来自 Planning 阶段）
            context: 执行上下文

        Returns:
            执行结果
        """
        tasks = list(plan.get("tasks", []))
        results = {}
        completed_count = 0

        i = 0
        while i < len(tasks):
            task = tasks[i]
            task_id = task.get("task_id", i + 1)

            # 执行任务（复用现有逻辑）
            if self.on_task_start:
                await self.on_task_start(task)

            try:
                # 调用现有的任务执行方法
                # 写作类任务会自动路由到 MultiAgentExecutor
                result = await self.agent._execute_task_in_parallel(
                    task=task,
                    context=context,
                    on_task_progress=self.on_task_progress,  # 传递进度回调
                )
                results[task_id] = result
                completed_count += 1
            except Exception as e:
                result = {"status": "failed", "error": str(e)}
                results[task_id] = result
                logger.error(f"任务 {task_id} 执行失败: {e}")

            if self.on_task_done:
                await self.on_task_done(task, result)

            # ═══════════════════════════════════════
            # 反思检查点
            # ═══════════════════════════════════════
            if should_reflect(task, result, completed_count, self.reflection_count):
                reflection_result = await self._do_reflection(
                    task=task,
                    result=result,
                    remaining_tasks=tasks[i+1:],
                    context=context,
                )

                # 如果需要重规划
                if reflection_result.needs_replan and self._can_replan():
                    new_tasks = await self._do_replan(
                        reflection=reflection_result.reflection,
                        remaining_tasks=tasks[i+1:],
                    )

                    if new_tasks:
                        tasks = tasks[:i+1] + new_tasks
                        self.replan_count += 1

                        if self.on_plan:
                            await self.on_plan({
                                "tasks": [self._format_task(t, j) for j, t in enumerate(new_tasks, i+2)],
                                "is_update": True,
                                "reason": reflection_result.reflection[:100],
                            })

            i += 1

        return {
            "results": results,
            "tasks": tasks,
            "reflections": self.reflections,
            "reflection_count": self.reflection_count,
            "replan_count": self.replan_count,
        }

    async def _do_reflection(
        self,
        task: Dict[str, Any],
        result: Dict[str, Any],
        remaining_tasks: List[Dict[str, Any]],
        context: Dict[str, Any],
    ) -> ReflectionResult:
        """执行反思"""
        try:
            reflection_result = await think_tool(
                task=task,
                result=result,
                remaining_tasks=remaining_tasks,
                context=context,
                ai_service=self.agent.ai_service,
            )

            self.reflection_count += 1
            self.reflections.append({
                "task_id": task.get("task_id"),
                "reflection": reflection_result.reflection,
                "needs_replan": reflection_result.needs_replan,
                "timestamp": datetime.now().isoformat(),
            })

            # MVP方案：复用 task_progress 事件发送反思内容
            # 前端 progress_status 会自动显示，无需任何改动
            if self.on_task_progress:
                await self.on_task_progress(
                    task,
                    f"💭 反思: {reflection_result.reflection}"
                )

            return reflection_result

        except Exception as e:
            logger.error(f"反思失败: {e}")
            return ReflectionResult(reflection=str(e), needs_replan=False)

    def _can_replan(self) -> bool:
        """是否还能重规划"""
        return self.replan_count < DeepAgentConfig.MAX_REPLANS

    async def _do_replan(
        self,
        reflection: str,
        remaining_tasks: List[Dict[str, Any]],
    ) -> Optional[List[Dict[str, Any]]]:
        """重新规划"""
        try:
            prompt = f"""基于反思，调整后续任务：

反思: {reflection}

原剩余任务:
{json.dumps(remaining_tasks, ensure_ascii=False, indent=2)}

输出调整后的任务列表（JSON）:
{{"tasks": [{{"description": "任务描述"}}, ...]}}
"""
            response = await asyncio.wait_for(
                self.agent.ai_service.chat(prompt),
                timeout=DeepAgentConfig.REPLAN_TIMEOUT
            )

            data = json.loads(response)
            return data.get("tasks", remaining_tasks)

        except Exception as e:
            logger.error(f"重规划失败: {e}")
            return None

    def _format_task(self, task: Dict[str, Any], task_id: int) -> Dict[str, Any]:
        """格式化任务"""
        if isinstance(task, str):
            return {"task_id": task_id, "description": task, "status": "pending"}
        task["task_id"] = task_id
        task.setdefault("status", "pending")
        return task
```

## 6. deep_agent/__init__.py

```python
# backend/app/services/agent/deep_agent/__init__.py

"""DeepAgent 模块

提供动态反思和重规划能力。
"""

from .executor import DeepAgentExecutor
from .reflection import think_tool, should_reflect, ReflectionResult
from .config import DeepAgentConfig

__all__ = [
    "DeepAgentExecutor",
    "think_tool",
    "should_reflect",
    "ReflectionResult",
    "DeepAgentConfig",
]
```

## 7. 使用示例

### 7.1 在 langgraph_agent.py 中使用

```python
# langgraph_agent.py

from .deep_agent import DeepAgentExecutor  # 新增导入

async def chat_with_planning(
    self,
    message: str,
    ...
    enable_reflection: bool = False,  # 新增参数
):
    # Planning 阶段（不变）
    plan = await self._generate_plan(message, context)
    await on_plan(plan)

    # Execution 阶段（新增分支）
    if enable_reflection:
        # 使用 DeepAgentExecutor 包装
        executor = DeepAgentExecutor(
            self, on_plan, on_task_start, on_task_done, on_content
        )
        exec_result = await executor.execute_with_reflection(plan, context)
        # 合并结果继续后续流程...
    else:
        # 原有逻辑不变
        ...
```

### 7.2 API 调用

```python
# 启用反思
result = await agent.chat_with_planning(
    message="帮我写第三章",
    enable_reflection=True,
)

print(f"反思次数: {result.get('reflection_count', 0)}")
```

## 8. 总结

| 方面 | 说明 |
|------|------|
| **设计原则** | langgraph_agent.py 仅改 4 行 |
| **新增目录** | `deep_agent/` 包含 4 个文件 |
| **总代码量** | ~260 行（全部新建） |
| **侵入性** | 极低，通过组合而非修改 |
| **可测试性** | DeepAgentExecutor 可独立测试 |
| **可回退** | enable_reflection=False 完全跳过 |
