"""
聊天模式相关的数据模型

提供统一的数据模型支持多种聊天模式（React/Planning）
"""

from enum import Enum
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any, List
import json
from datetime import datetime


class ChatMode(str, Enum):
    """
    聊天模式枚举

    - PLANNING: Planning模式（规划+执行，适合复杂任务）
    - REACT: ReAct模式（边思考边执行，适合简单交互）
    """
    PLANNING = "planning"
    REACT = "react"

    def __str__(self):
        return self.value


class ChatRequest(BaseModel):
    """
    统一的聊天请求模型

    适用于所有聊天模式
    """
    message: str = Field(..., description="用户消息", min_length=1)
    mode: Optional[ChatMode] = Field(None, description="聊天模式（默认planning）")
    work_id: Optional[str] = Field(None, description="作品ID")
    chapter_id: Optional[str] = Field(None, description="章节ID")
    conversation_id: Optional[str] = Field(None, description="会话ID（用于继续对话）")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="额外上下文")

    model_config = ConfigDict(
        use_enum_values=True,
        json_schema_extra={
            "example": {
                "message": "帮我写一篇关于AI的文章",
                "mode": "react",
                "work_id": "work_123",
                "conversation_id": "conv_456"
            }
        }
    )


# ==================== SSE事件模型 ====================

class ReactEvent(BaseModel):
    """
    ReAct模式事件

    用于chat_stream()的实时事件
    """
    type: str = Field(..., description="事件类型：progress/tool_call/content/completed/error")
    data: Dict[str, Any] = Field(..., description="事件数据")
    timestamp: Optional[str] = Field(None, description="时间戳")
    session_id: Optional[str] = Field(None, description="会话ID")
    mode: str = Field("react", description="模式标识")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "type": "progress",
                "data": {
                    "step": "intent_analysis",
                    "description": "正在分析您的需求..."
                },
                "mode": "react"
            }
        }
    )


class PlanningEvent(BaseModel):
    """
    Planning模式事件

    用于chat_with_planning()的实时事件
    """
    type: str = Field(..., description="事件类型：plan/task_start/task_progress/task_done/content/done/error")
    data: Any = Field(..., description="事件数据")
    mode: str = Field("planning", description="模式标识")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "type": "plan",
                "data": {
                    "tasks": [
                        {"task_id": 1, "description": "收集信息"}
                    ]
                },
                "mode": "planning"
            }
        }
    )


# ==================== 格式化函数 ====================

def format_react_event_to_sse(event_type: str, event_data: Dict[str, Any], session_id: Optional[str] = None) -> str:
    """
    将ReAct事件转换为SSE格式

    Args:
        event_type: 事件类型
        event_data: 事件数据
        session_id: 会话ID

    Returns:
        SSE格式字符串
    """
    sse_data = {
        "type": event_type,
        "data": event_data,
        "timestamp": datetime.now().isoformat(),
        "mode": "react"
    }

    if session_id:
        sse_data["session_id"] = session_id

    return f"data: {json.dumps(sse_data, ensure_ascii=False)}\n\n"


def format_planning_event_to_sse(event_type: str, event_data: Any) -> str:
    """
    将Planning事件转换为SSE格式

    Args:
        event_type: 事件类型
        event_data: 事件数据

    Returns:
        SSE格式字符串
    """
    sse_data = {
        "type": event_type,
        "data": event_data,
        "mode": "planning"
    }

    return f"data: {json.dumps(sse_data, ensure_ascii=False)}\n\n"


def format_error_event(error: Exception, mode: str = "react", session_id: Optional[str] = None) -> str:
    """
    创建错误事件

    Args:
        error: 异常对象
        mode: 模式（react/planning）
        session_id: 会话ID

    Returns:
        SSE格式错误事件
    """
    error_data = {
        "type": "error",
        "data": {
            "error": str(error),
            "error_type": type(error).__name__
        },
        "mode": mode,
        "timestamp": datetime.now().isoformat()
    }

    if session_id:
        error_data["session_id"] = session_id

    return f"data: {json.dumps(error_data, ensure_ascii=False)}\n\n"
