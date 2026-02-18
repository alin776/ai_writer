"""
事件翻译器

将 LangGraph astream_events() 输出翻译为前端 FlowEvent 格式。
前端已有渲染逻辑，这里只做格式映射，保持兼容。

astream_events v2 主要事件类型：
- on_chat_model_stream: LLM 逐 token 输出
- on_tool_start: 工具调用开始
- on_tool_end: 工具调用结束
- on_chain_end: 链/Agent 结束
"""

import logging
import re
from typing import Any

from app.utils.datetime_utils import get_utc_now

logger = logging.getLogger(__name__)

# 工具图标映射
_TOOL_ICONS = {
    "read_file": "FileText",
    "write_file": "PenTool",
    "edit_file": "Edit3",
    "ls": "FolderOpen",
    "glob": "Search",
    "grep": "Search",
    "semantic_search": "Search",
    "write_todos": "ListTodo",
    "read_todos": "ListTodo",
    "task": "Users",
}

# 步骤计数器（per-session 实例，避免全局状态并发冲突）


class StepCounter:
    """每个 Agent 会话独立的步骤计数器。"""

    def __init__(self):
        self._counter = 0
        self._run_to_step: dict[str, int] = {}  # run_id → step_id 映射

    def next_id(self, run_id: str | None = None) -> int:
        self._counter += 1
        if run_id:
            self._run_to_step[run_id] = self._counter
        return self._counter

    def get_step_id(self, run_id: str | None) -> int:
        """通过 run_id 查找对应的 step_id，找不到则回退到 current。"""
        if run_id and run_id in self._run_to_step:
            return self._run_to_step.pop(run_id)
        return self._counter

    @property
    def current(self) -> int:
        return self._counter


def _now() -> str:
    return get_utc_now().isoformat()


def translate_event(event: dict[str, Any], counter: StepCounter) -> dict[str, Any] | None:
    """将 astream_events 事件翻译为前端 FlowEvent。

    Args:
        event: LangGraph astream_events v2 事件字典
        counter: 当前会话的步骤计数器

    Returns:
        FlowEvent 字典，或 None（跳过不关心的事件）
    """
    kind = event.get("event", "")
    name = event.get("name", "")
    data = event.get("data", {})
    run_id = event.get("run_id", "")

    # ─── LLM 逐 token 流式输出 ───
    if kind == "on_chat_model_stream":
        chunk = data.get("chunk")
        if chunk and hasattr(chunk, "content") and chunk.content:
            raw = chunk.content
            # 归一化：content 可能是 str 或 list[dict]（Responses API 格式）
            if isinstance(raw, list):
                text = "".join(
                    b.get("text", b.get("content", "")) if isinstance(b, dict) else str(b)
                    for b in raw
                )
            else:
                text = str(raw)
            if text:
                return {
                    "type": "text",
                    "data": {"content": text},
                    "timestamp": _now(),
                }
        return None

    # ─── 工具调用开始 ───
    if kind == "on_tool_start":
        tool_name = name
        tool_input = data.get("input", {})

        step_id = counter.next_id(run_id)  # 记录 run_id → step_id 映射

        # 生成友好的工具描述
        desc = _tool_description(tool_name, tool_input)

        return {
            "type": "step_start",
            "step_id": step_id,
            "title": desc,
            "tool_name": tool_name,
            "tool_input": tool_input,
            "status": "running",
            "timestamp": _now(),
        }

    # ─── 工具调用结束 ───
    if kind == "on_tool_end":
        tool_name = name
        icon = _TOOL_ICONS.get(tool_name, "Wrench")

        return {
            "type": "step_complete",
            "step_id": counter.get_step_id(run_id),  # 通过 run_id 找回正确的 step_id
            "description": f"{tool_name} 完成",
            "tool_name": tool_name,
            "tool_call": {"icon": icon, "name": tool_name},
            "status": "done",
            "timestamp": _now(),
        }

    # ─── 跳过不关心的事件 ───
    return None


def make_completion_event(changes: list[dict]) -> dict[str, Any]:
    """构建 Agent 完成事件。

    Args:
        changes: 待审批改动列表（来自 backend.get_changes()）

    Returns:
        completion FlowEvent
    """
    if changes:
        text = f"任务已完成，共 {len(changes)} 处改动待审批"
    else:
        text = "任务已完成"

    return {
        "type": "completion",
        "data": {"text": text, "changes": changes},
        "timestamp": _now(),
    }


def make_revision_event(op: dict) -> dict[str, Any]:
    """从缓冲区操作构建 revision 事件。

    Args:
        op: get_changes() 返回的单条操作

    Returns:
        revision FlowEvent
    """
    # 统计 diff 行数（折叠多换行 + 去头尾空行，与前端 diff 插件口径一致）
    new_s = op.get("new_string", "")
    old_s = op.get("old_string", "")
    new_norm = re.sub(r'\n{2,}', '\n', new_s).strip('\n') if new_s else ""
    old_norm = re.sub(r'\n{2,}', '\n', old_s).strip('\n') if old_s else ""
    add_lines = new_norm.count("\n") + 1 if new_norm else 0
    del_lines = old_norm.count("\n") + 1 if old_norm else 0

    return {
        "type": "revision",
        "data": {
            "revisionType": "create" if op["op_type"] == "write" else "replace",
            "path": op["path"],
            "status": "pending",
            "contentPreview": op.get("content_preview", ""),
            "oldString": op.get("old_string", ""),
            "newString": op.get("new_string", ""),
            "chapterId": op.get("chapter_id", ""),
            "chapterTitle": op.get("chapter_title", ""),
            "addLines": add_lines,
            "delLines": del_lines,
            "index": op.get("index"),
        },
        "timestamp": _now(),
    }


def _tool_description(tool_name: str, tool_input: Any) -> str:
    """生成工具调用的友好描述。"""
    if isinstance(tool_input, dict):
        if tool_name == "read_file":
            return f"读取 {tool_input.get('file_path', '文件')}"
        if tool_name == "write_file":
            return f"创建 {tool_input.get('file_path', '文件')}"
        if tool_name == "edit_file":
            return f"编辑 {tool_input.get('file_path', '文件')}"
        if tool_name == "ls":
            return f"查看目录 {tool_input.get('path', '/')}"
        if tool_name in ("grep", "glob"):
            return f"搜索 {tool_input.get('pattern', '')}"
        if tool_name == "semantic_search":
            return f"语义搜索: {str(tool_input.get('query', ''))[:50]}"
        if tool_name == "task":
            return f"子任务: {str(tool_input.get('prompt', ''))[:50]}"
    return tool_name
