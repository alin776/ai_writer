# 05 - 流式事件设计

## 文件位置

`backend/app/services/agent/stream/stream_event_handler.py`（改造）

## 新增事件类型

| 事件类型 | 说明 | 数据结构 |
|----------|------|----------|
| `plan` | 初始计划 | `{tasks: [], user_intent: ""}` |
| `task_start` | 任务开始 | `{task_id, title, tool}` |
| `task_done` | 任务完成（主事件） | `{task_id, result_preview}` |
| `thinking` | AI 思考 | `{summary, next_step}` |
| `plan_update` | 计划更新 | `{action, task?, tasks}` |
| `final` | 最终响应 | `{content}` |

> ⚠️ 兼容说明：
> - 现有 SSE 链路已使用 `plan/task_start/task_progress/task_done`，新增事件需保持兼容。
> - `task_complete` 仅作为别名（必要时双发），前端以 `task_done` 为准。
> - 计划更新优先复用 `plan` + `is_update/new_task_ids`；`plan_update` 为可选扩展。
> - `thinking` 可新增，但需保留 `task_progress` 的回退显示。

## 事件数据结构

```typescript
// 前端 TypeScript 类型定义

interface PlanEvent {
  type: "plan";
  data: {
    tasks: TaskDisplay[];
    user_intent: string;
  };
}

interface TaskStartEvent {
  type: "task_start";
  data: {
    task_id: string;
    title: string;
    tool: string;
  };
}

interface TaskDoneEvent {
  type: "task_done";
  data: {
    task_id: string;
    result_preview: string;  // 结果预览（限制长度）
  };
}

interface ThinkingEvent {
  type: "thinking";
  data: {
    summary: string;    // AI 对结果的总结
    next_step: string;  // 下一步说明
  };
}

interface PlanUpdateEvent {
  type: "plan_update";
  data: {
    action: "add" | "skip" | "reorder";
    task?: TaskDisplay;      // 新增的任务
    task_id?: string;        // 被跳过的任务ID
    tasks: TaskDisplay[];    // 更新后的完整任务列表
  };
}

interface FinalEvent {
  type: "final";
  data: {
    content: string;
  };
}

interface TaskDisplay {
  task_id: string;
  title: string;
  tool: string;
  status: "pending" | "in_progress" | "completed" | "skipped" | "failed";
  is_dynamic: boolean;
}
```

## 后端发送方法

```python
# stream_event_handler.py 新增方法

class StreamEventHandler:
    """流式事件处理器"""

    async def emit_plan(self, tasks: List[Dict], user_intent: str = ""):
        """发送初始计划事件"""
        await self._emit({
            "type": "plan",
            "data": {
                "tasks": tasks,
                "user_intent": user_intent
            }
        })

    async def emit_task_start(self, task_id: str, title: str, tool: str):
        """发送任务开始事件"""
        await self._emit({
            "type": "task_start",
            "data": {
                "task_id": task_id,
                "title": title,
                "tool": tool
            }
        })

    async def emit_task_done(self, task_id: str, result_preview: str):
        """发送任务完成事件"""
        await self._emit({
            "type": "task_done",
            "data": {
                "task_id": task_id,
                "result_preview": result_preview[:200]  # 限制长度
            }
        })

    async def emit_thinking(self, summary: str, next_step: str):
        """发送 AI 思考事件"""
        await self._emit({
            "type": "thinking",
            "data": {
                "summary": summary,
                "next_step": next_step
            }
        })

    async def emit_plan_update(
        self,
        action: str,
        tasks: List[Dict],
        task: Optional[Dict] = None,
        task_id: Optional[str] = None
    ):
        """发送计划更新事件"""
        data = {
            "action": action,
            "tasks": tasks
        }
        if task:
            data["task"] = task
        if task_id:
            data["task_id"] = task_id

        await self._emit({
            "type": "plan_update",
            "data": data
        })

    async def emit_final(self, content: str):
        """发送最终响应事件"""
        await self._emit({
            "type": "final",
            "data": {
                "content": content
            }
        })
```

## SSE 格式

```
event: plan
data: {"tasks": [...], "user_intent": "续写第三章"}

event: task_start
data: {"task_id": "1", "title": "获取上下文", "tool": "get_writing_context"}

event: task_done
data: {"task_id": "1", "result_preview": "第三章内容：主角进入森林..."}

event: thinking
data: {"summary": "获取了第三章内容，共2000字", "next_step": "接下来开始续写"}

event: task_start
data: {"task_id": "2", "title": "续写章节", "tool": "smart_continue"}

event: task_done
data: {"task_id": "2", "result_preview": "续写内容：林间的雾气..."}

event: thinking
data: {"summary": "续写完成，生成了500字", "next_step": "应用到编辑器"}

event: final
data: {"content": "已为第三章续写了500字内容..."}
```

## 与现有事件的兼容

| 现有事件 | 保留/替换 | 说明 |
|----------|-----------|------|
| `task_progress` | 保留 | 兼容旧模式 |
| `summarization_start` | 保留 | 最终响应阶段 |
| `summarization_complete` | 保留 | 最终响应阶段 |
| `output_ready` | 保留 | 输出容器 |

新事件与现有事件**并存**，通过执行模式区分使用哪套事件。
