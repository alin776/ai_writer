"""Custom file operation tools for DeepAgent.

Expose buffered rename/delete capabilities that are not part of the
default filesystem middleware toolset.
"""

from __future__ import annotations

from typing import Annotated

from langchain_core.tools import BaseTool, StructuredTool

from app.services.agent.deep_agent.buffered_backend import BufferedFilesystemBackend


def _normalize_abs_file_path(path: str, field_name: str) -> str:
    normalized = (path or "").strip().replace("\\", "/")
    if not normalized.startswith("/"):
        raise ValueError(f"{field_name} must be an absolute path starting with '/'")
    if normalized == "/":
        raise ValueError(f"{field_name} cannot be root '/'")
    return normalized


def create_file_ops_tools(backend: BufferedFilesystemBackend) -> list[BaseTool]:
    """Create custom tools backed by BufferedFilesystemBackend."""

    def rename_file(
        old_path: Annotated[str, "Absolute source file path, e.g. /chapters/02-old.md"],
        new_path: Annotated[str, "Absolute target file path, e.g. /chapters/02-new.md"],
    ) -> str:
        """Rename an existing file path (buffered; requires user approval to apply)."""
        try:
            normalized_old = _normalize_abs_file_path(old_path, "old_path")
            normalized_new = _normalize_abs_file_path(new_path, "new_path")
        except ValueError as e:
            return f"Error: {e}"

        error = backend.rename_path(normalized_old, normalized_new)
        if error:
            return error
        return f"Success: rename queued {normalized_old} -> {normalized_new} (pending approval)"

    def delete_file(
        file_path: Annotated[str, "Absolute file path to delete, e.g. /chapters/02-old.md"],
    ) -> str:
        """Delete a file path (buffered; requires user approval to apply)."""
        try:
            normalized_path = _normalize_abs_file_path(file_path, "file_path")
        except ValueError as e:
            return f"Error: {e}"

        error = backend.delete_path(normalized_path)
        if error:
            return error
        return f"Success: delete queued {normalized_path} (pending approval)"

    return [
        StructuredTool.from_function(
            name="rename_file",
            description=(
                "Rename a file path. Use this for chapter/file renaming when path needs to change. "
                "Both old_path and new_path must be absolute."
            ),
            func=rename_file,
        ),
        StructuredTool.from_function(
            name="delete_file",
            description=(
                "Delete a file. Use this when a chapter/file should be removed. "
                "file_path must be absolute."
            ),
            func=delete_file,
        ),
    ]

