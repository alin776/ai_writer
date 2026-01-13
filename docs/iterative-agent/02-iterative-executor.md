# 02 - 迭代执行器设计

> ⚠️ 重要说明：最终实现落在 **DeepAgentExecutor 增强版**（`backend/app/services/agent/deep_agent/executor.py`），
> 本文中的 IterativeExecutor 为概念设计，不再新建 `iterative_executor.py`。

## 文件位置

`backend/app/services/agent/deep_agent/executor.py`（增强实现）

## 类设计

```python
from typing import AsyncGenerator, Dict, Any, Optional, List
from dataclasses import dataclass

@dataclass
class IterativeConfig:
    """迭代执行配置"""
    max_iterations: int = 10          # 最大迭代次数
    max_added_tasks: int = 3          # 最多动态添加任务数
    reflection_timeout: float = 10.0  # 反思超时时间


class IterativeExecutor:
    """迭代执行器

    实现类似 Claude Code 的执行模式：
    1. 初始规划 → 生成任务列表
    2. 迭代执行 → 每次执行一个任务
    3. 反思决策 → AI 总结 + 决定下一步
    4. 动态调整 → 可增删改任务
    """

    def __init__(
        self,
        plan_generator,      # 复用
        task_runner,         # 复用
        reflection_engine,   # 增强
        response_builder,    # 复用
        stream_handler,      # 复用
        config: Optional[IterativeConfig] = None
    ):
        self.plan_generator = plan_generator
        self.task_runner = task_runner
        self.reflection_engine = reflection_engine
        self.response_builder = response_builder
        self.stream_handler = stream_handler
        self.config = config or IterativeConfig()

    async def execute(
        self,
        request: Dict[str, Any],
        state: Dict[str, Any]
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """执行入口

        Args:
            request: 用户请求
            state: Agent 状态

        Yields:
            事件字典，包含 type 和 data
        """
        # 见下方详细流程
        pass
```

## 执行流程

```python
async def execute(self, request, state) -> AsyncGenerator:
    """完整执行流程"""

    # ========== 1. 初始规划 ==========
    plan_result = await self.plan_generator.generate(
        message=request["message"],
        context=state
    )

    # 创建动态计划
    dynamic_plan = DynamicPlan(plan_result["tasks"])

    # 发送计划事件
    yield {
        "type": "plan",
        "data": {
            "tasks": dynamic_plan.to_display_list(),
            "user_intent": plan_result.get("user_intent", "")
        }
    }

    # ========== 2. 迭代执行 ==========
    completed_results = []
    iteration = 0
    added_tasks_count = 0

    while dynamic_plan.has_pending():
        # 检查迭代限制
        if iteration >= self.config.max_iterations:
            yield {"type": "warning", "data": {"message": "达到最大迭代次数"}}
            break

        iteration += 1
        task = dynamic_plan.get_next()

        # 2.1 发送任务开始事件
        yield {
            "type": "task_start",
            "data": {
                "task_id": task["task_id"],
                "title": task["title"],
                "tool": task["tool"]
            }
        }

        # 2.2 执行任务
        result = await self.task_runner.execute_task(
            task=task,
            work_id=state.get("work_id"),
            chapter_id=state.get("chapter_id"),
            context=request["message"],
            state=state
        )

        completed_results.append({
            "task_id": task["task_id"],
            "tool": task["tool"],
            "result": result,
            "status": "completed"
        })

        # 2.3 发送任务完成事件
        yield {
            "type": "task_done",
            "data": {
                "task_id": task["task_id"],
                "result_preview": result[:200] if len(result) > 200 else result
            }
        }

        # 2.4 反思决策
        decision = await self.reflection_engine.reflect(
            task=task,
            result=result,
            remaining_tasks=dynamic_plan.get_remaining(),
            user_request=request["message"],
            completed_results=completed_results
        )

        # 2.5 发送思考事件
        yield {
            "type": "thinking",
            "data": {
                "summary": decision.summary,
                "next_step": decision.next_step
            }
        }

        # 2.6 根据决策调整计划
        if decision.action == "add_task" and added_tasks_count < self.config.max_added_tasks:
            dynamic_plan.insert_after_current(decision.new_task)
            added_tasks_count += 1

            yield {
                "type": "plan_update",
                "data": {
                    "action": "add",
                    "task": decision.new_task,
                    "tasks": dynamic_plan.to_display_list()
                }
            }

        elif decision.action == "skip_next":
            skipped = dynamic_plan.skip_next()
            if skipped:
                yield {
                    "type": "plan_update",
                    "data": {
                        "action": "skip",
                        "task_id": skipped["task_id"],
                        "tasks": dynamic_plan.to_display_list()
                    }
                }

        elif decision.action == "done":
            break

        # 标记当前任务完成
        dynamic_plan.mark_completed(task["task_id"])

    # ========== 3. 最终响应 ==========
    final_response = await self.response_builder.build_final_response(
        task_results=completed_results,
        message=request["message"]
    )

    yield {
        "type": "final",
        "data": {
            "content": final_response
        }
    }
```

## 错误处理

```python
async def execute(self, request, state) -> AsyncGenerator:
    try:
        # ... 主流程 ...
    except Exception as e:
        logger.error(f"[IterativeExecutor] 执行失败: {e}")
        yield {
            "type": "error",
            "data": {
                "message": f"执行过程中出现错误: {str(e)}",
                "recoverable": False
            }
        }
```

## 配置说明

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| max_iterations | 10 | 防止无限循环 |
| max_added_tasks | 3 | 限制动态添加任务数 |
| reflection_timeout | 10.0 | 反思超时时间（秒） |
