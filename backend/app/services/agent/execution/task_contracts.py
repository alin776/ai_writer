# -*- coding: utf-8 -*-
"""任务契约注册表 - 定义工具的前置条件与产出"""

from __future__ import annotations

from typing import Dict, List


class TaskContractRegistry:
    """维护工具的 requires / produces 映射"""

    def __init__(self) -> None:
        self._requires: Dict[str, List[str]] = {
            "smart_insert": ["locate_targets"],
            "smart_rewrite": ["locate_targets"],
            "operate_apply": ["locate_targets"],
        }
        self._produces: Dict[str, List[str]] = {
            "explore_content": ["locate_targets", "insert_context"],
        }

    def get_requires(self, tool_name: str) -> List[str]:
        if not tool_name:
            return []
        return list(self._requires.get(tool_name, []))

    def get_produces(self, tool_name: str) -> List[str]:
        if not tool_name:
            return []
        return list(self._produces.get(tool_name, []))

    def is_tracked_tool(self, tool_name: str) -> bool:
        if not tool_name:
            return False
        return tool_name in self._requires or tool_name in self._produces
