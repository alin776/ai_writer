# -*- coding: utf-8 -*-
"""Tool execution context helpers."""

from contextvars import ContextVar
from typing import Any, Optional


_stream_event_handler: ContextVar[Optional[Any]] = ContextVar(
    "tool_stream_event_handler",
    default=None
)
_explore_step_id: ContextVar[Optional[int]] = ContextVar(
    "tool_explore_step_id",
    default=None
)


def set_stream_event_handler(handler: Any):
    return _stream_event_handler.set(handler)


def reset_stream_event_handler(token) -> None:
    _stream_event_handler.reset(token)


def get_stream_event_handler() -> Optional[Any]:
    return _stream_event_handler.get()


def set_explore_step_id(step_id: Optional[int]):
    return _explore_step_id.set(step_id)


def reset_explore_step_id(token) -> None:
    _explore_step_id.reset(token)


def get_explore_step_id() -> Optional[int]:
    return _explore_step_id.get()
