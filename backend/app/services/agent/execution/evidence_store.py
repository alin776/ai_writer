# -*- coding: utf-8 -*-
"""证据仓库 - 统一存储执行期可复用证据"""

from __future__ import annotations

from typing import Any, Dict, List, Optional


class EvidenceStore:
    def __init__(self) -> None:
        self._store: Dict[str, Any] = {}

    def put(self, key: str, payload: Any) -> None:
        if not key:
            return
        if payload is None:
            return
        self._store[key] = payload

    def get(self, key: str) -> Optional[Any]:
        if not key:
            return None
        return self._store.get(key)

    def has(self, key: str) -> bool:
        value = self._store.get(key)
        if key == "locate_targets":
            if not isinstance(value, list):
                return False
            for item in value:
                if not isinstance(item, dict):
                    continue
                chapter_id = item.get("chapter_id") or ""
                if chapter_id:
                    return True
            return False
        return value is not None

    def missing(self, requires: List[str]) -> List[str]:
        missing = []
        for key in requires:
            if not self.has(key):
                missing.append(key)
        return missing

    def ingest(self, tool_name: str, raw_result: Any) -> None:
        if not tool_name or not isinstance(raw_result, dict):
            return
        if tool_name == "explore_content":
            if raw_result.get("success") is not True:
                return
            locate_targets = raw_result.get("locate_targets")
            if isinstance(locate_targets, list) and locate_targets:
                self.put("locate_targets", locate_targets)
            context_for_task = raw_result.get("context_for_task")
            if isinstance(context_for_task, str) and context_for_task.strip():
                self.put("insert_context", context_for_task.strip())
                return
            if isinstance(locate_targets, list):
                for item in locate_targets:
                    if isinstance(item, dict):
                        insert_context = item.get("insert_context")
                        if isinstance(insert_context, str) and insert_context.strip():
                            self.put("insert_context", insert_context.strip())
                            return

