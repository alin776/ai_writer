# -*- coding: utf-8 -*-
"""规划输出结构定义（用于校验与归一化）。"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, ConfigDict


class RefSpec(BaseModel):
    """任务结果引用：从指定 task_id 的结果中抽取字段。"""

    model_config = ConfigDict(extra="allow")

    task_id: int = Field(..., ge=1, description="被引用的任务ID")
    path: str = Field(default="", description="字段路径，如 chapters[0].content")
    default: Any = Field(default=None, description="依赖未就绪时的默认值")


class TaskSpec(BaseModel):
    """单个任务定义。"""

    model_config = ConfigDict(extra="allow")

    task_id: int = Field(..., ge=1)
    title: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    tool: str = Field(...)
    params: Dict[str, Any] = Field(default_factory=dict)
    depends_on: List[int] = Field(default_factory=list)


class PlanSchema(BaseModel):
    """规划输出结构。"""

    model_config = ConfigDict(extra="allow")

    thinking: Dict[str, Any] = Field(default_factory=dict)
    user_intent: Optional[str] = Field(default=None)
    output_title: Optional[str] = Field(default=None)
    direct_answer: Optional[str] = Field(default=None)
    response_hint: Optional[str] = Field(default=None)
    tasks: List[TaskSpec] = Field(default_factory=list)
