"""
BufferedFilesystemBackend — 带写缓冲的文件系统后端

继承 DeepAgents 的 FilesystemBackend，将 write/edit 操作缓冲到内存，
不直接落盘。用户审批后调用 flush() 写入磁盘或 discard() 丢弃。

核心思路：
- write() / edit() 不落盘，追加到 self._buffer 操作日志
- read() 先查缓冲区（通过 _replay），没有才读磁盘
- flush() 审批通过后将缓冲区全部写入磁盘
- discard() 审批拒绝丢弃全部缓冲区
"""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from deepagents.backends.filesystem import (
    EditResult,
    FilesystemBackend,
    WriteResult,
    format_content_with_line_numbers,
    perform_string_replacement,
)


@dataclass
class BufferOp:
    """单条缓冲操作"""
    op_type: str  # "write" or "edit"
    path: str     # 虚拟路径（相对于 root_dir）
    content: str | None = None      # write 时的完整内容
    old_string: str | None = None   # edit 时的旧字符串
    new_string: str | None = None   # edit 时的新字符串
    replace_all: bool = False       # edit 时是否全部替换


class BufferedFilesystemBackend(FilesystemBackend):
    """带写缓冲的文件系统后端。

    Agent 执行期间的 write/edit 操作存入内存缓冲区，
    用户审批后调用 flush() 落盘或 discard() 丢弃。
    """

    def __init__(self, root_dir: str | Path, **kwargs):
        kwargs.setdefault("virtual_mode", True)
        super().__init__(root_dir=root_dir, **kwargs)
        self._buffer: list[BufferOp] = []

    # ─── 重写写操作：缓冲不落盘 ───

    def write(self, file_path: str, content: str) -> WriteResult:
        """write 操作存入缓冲区，不落盘。"""
        # 检查磁盘上是否已存在
        resolved = self._resolve_path(file_path)
        if resolved.exists():
            return WriteResult(
                error=f"Cannot write to {file_path} because it already exists. "
                      "Read and then make an edit, or write to a new path."
            )

        # 检查缓冲区是否已 write 过同路径
        for op in self._buffer:
            if op.path == file_path and op.op_type == "write":
                return WriteResult(
                    error=f"Cannot write to {file_path} because it already exists "
                          "in the pending buffer."
                )

        self._buffer.append(BufferOp(
            op_type="write",
            path=file_path,
            content=content,
        ))
        return WriteResult(path=file_path, files_update=None)

    def edit(
        self,
        file_path: str,
        old_string: str,
        new_string: str,
        replace_all: bool = False,
    ) -> EditResult:
        """edit 操作存入缓冲区，不落盘。先验证 old_string 匹配。"""
        # 通过 _replay 获取文件当前内容（含缓冲区）
        current = self._replay(file_path)
        if current is None:
            return EditResult(error=f"Error: File '{file_path}' not found")

        # 验证 old_string 存在且可替换
        result = perform_string_replacement(current, old_string, new_string, replace_all)
        if isinstance(result, str):
            # 返回的是错误消息
            return EditResult(error=result)

        _new_content, occurrences = result

        self._buffer.append(BufferOp(
            op_type="edit",
            path=file_path,
            old_string=old_string,
            new_string=new_string,
            replace_all=replace_all,
        ))
        return EditResult(path=file_path, files_update=None, occurrences=int(occurrences))

    # ─── 重写读操作：优先读缓冲区 ───

    def read(
        self,
        file_path: str,
        offset: int = 0,
        limit: int = 2000,
    ) -> str:
        """读文件，优先查缓冲区（含 replay），没有才读磁盘。"""
        # 只有该文件在缓冲区中有操作时，才走 replay 路径
        has_buffer_ops = any(op.path == file_path for op in self._buffer)
        if has_buffer_ops:
            replayed = self._replay(file_path)
            if replayed is not None:
                lines = replayed.splitlines()
                start_idx = offset
                end_idx = min(start_idx + limit, len(lines))
                if start_idx >= len(lines):
                    return f"Error: Line offset {offset} exceeds file length ({len(lines)} lines)"
                selected = lines[start_idx:end_idx]
                return format_content_with_line_numbers(selected, start_line=start_idx + 1)

        # 缓冲区没有，走父类（读磁盘）
        return super().read(file_path, offset, limit)

    # ─── 核心重放逻辑 ───

    def _replay(self, file_path: str) -> str | None:
        """按序重放缓冲区操作，得到文件当前内容。

        三种情况：
        1. 缓冲区有 write → 从 write 的 content 开始，叠加后续 edit
        2. 缓冲区只有 edit → 先读磁盘内容，再依次 apply edit
        3. 缓冲区和磁盘都没有 → 返回 None

        Args:
            file_path: 虚拟路径

        Returns:
            重放后的文件内容，若文件既不在缓冲区也不在磁盘则返回 None
        """
        # 筛选出该文件的所有操作（保持顺序）
        ops = [op for op in self._buffer if op.path == file_path]

        # 确定初始内容
        content: str | None = None
        start_idx = 0

        for i, op in enumerate(ops):
            if op.op_type == "write":
                # 最后一次 write 作为基础（之前的 write 被覆盖）
                content = op.content or ""
                start_idx = i + 1

        # 如果缓冲区没有 write，尝试从磁盘读取
        if content is None:
            resolved = self._resolve_path(file_path)
            if not resolved.exists() or not resolved.is_file():
                return None
            try:
                content = resolved.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                return None

        # 从 start_idx 开始依次 apply edit
        for op in ops[start_idx:]:
            if op.op_type == "edit":
                result = perform_string_replacement(
                    content, op.old_string or "", op.new_string or "", op.replace_all
                )
                if not isinstance(result, str):
                    content, _ = result
                # 替换失败则跳过（不应发生，因为 edit() 已验证过）

        return content

    # ─── 审批操作 ───

    def get_changes(self) -> list[dict[str, Any]]:
        """返回待审批改动列表（JSON 可序列化）。"""
        changes = []
        for i, op in enumerate(self._buffer):
            item: dict[str, Any] = {
                "index": i,
                "op_type": op.op_type,
                "path": op.path,
            }
            if op.op_type == "write":
                item["content_preview"] = (op.content or "")[:200]
            elif op.op_type == "edit":
                item["old_string"] = op.old_string
                item["new_string"] = op.new_string
            changes.append(item)
        return changes

    def flush(self) -> list[str]:
        """审批通过：将缓冲区全部写入磁盘。返回受影响的文件路径列表。"""
        import logging
        logger = logging.getLogger(__name__)

        affected = set()
        for op in self._buffer:
            try:
                if op.op_type == "write":
                    # 用父类的 write 落盘
                    resolved = self._resolve_path(op.path)
                    resolved.parent.mkdir(parents=True, exist_ok=True)
                    flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
                    if hasattr(os, "O_NOFOLLOW"):
                        flags |= os.O_NOFOLLOW
                    fd = os.open(resolved, flags, 0o644)
                    with os.fdopen(fd, "w", encoding="utf-8") as f:
                        f.write(op.content or "")
                elif op.op_type == "edit":
                    # 读取当前磁盘内容（或之前 flush 的结果）做替换
                    resolved = self._resolve_path(op.path)
                    content = resolved.read_text(encoding="utf-8")
                    result = perform_string_replacement(
                        content, op.old_string or "", op.new_string or "", op.replace_all
                    )
                    if not isinstance(result, str):
                        new_content, _ = result
                        fd = os.open(resolved, os.O_WRONLY | os.O_TRUNC, 0o644)
                        with os.fdopen(fd, "w", encoding="utf-8") as f:
                            f.write(new_content)
                affected.add(op.path)
            except Exception as e:
                logger.error(f"[BufferedBackend] flush 操作失败: {op.op_type} {op.path}: {e}")
        self._buffer.clear()
        return list(affected)

    def flush_single(self, index: int) -> str | None:
        """单个接受：将指定索引的操作写入磁盘。返回受影响路径或 None。

        安全检查：如果该操作是 edit 且同一文件有更早的未落盘 write，
        则拒绝执行（返回 None），因为 edit 依赖 write 先落盘。
        """
        if index < 0 or index >= len(self._buffer):
            return None

        op = self._buffer[index]

        # 依赖检查：edit 不能脱离其 write 单独 flush
        if op.op_type == "edit":
            has_pending_write = any(
                self._buffer[i].path == op.path and self._buffer[i].op_type == "write"
                for i in range(index)
            )
            if has_pending_write:
                return None

        self._buffer.pop(index)
        if op.op_type == "write":
            resolved = self._resolve_path(op.path)
            resolved.parent.mkdir(parents=True, exist_ok=True)
            resolved.write_text(op.content or "", encoding="utf-8")
        elif op.op_type == "edit":
            resolved = self._resolve_path(op.path)
            content = resolved.read_text(encoding="utf-8")
            result = perform_string_replacement(
                content, op.old_string or "", op.new_string or "", op.replace_all
            )
            if not isinstance(result, str):
                new_content, _ = result
                resolved.write_text(new_content, encoding="utf-8")
        return op.path

    def discard(self) -> None:
        """审批拒绝：丢弃全部缓冲区。"""
        self._buffer.clear()

    def discard_single(self, index: int) -> bool:
        """单个拒绝：丢弃指定索引的操作。"""
        if index < 0 or index >= len(self._buffer):
            return False
        self._buffer.pop(index)
        return True
