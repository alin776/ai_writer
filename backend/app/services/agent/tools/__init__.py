"""
Agent 工具模块 (Agent Tools)

提供:
1. 工具类型系统 (tool_types)
2. 工具注册表 (tool_registry)
3. 写作工具集 (writing_tools)
4. 人机协同工具 (hitl)
"""

# ==================== 工具类型系统 ====================
from .tool_types import (
    ToolInput,
    ToolOutput,
    ToolCategory,
    StandardTool,
    InputT,
    OutputT
)

# ==================== 工具注册表 ====================
from .tool_registry import (
    # 标准化注册表
    StandardToolRegistry,
    registry,
    # 动态注册表(兼容)
    DynamicToolRegistry,
    global_registry,
    ToolDefinition,
    ToolParameter,
    ToolMetadata,
    register_as_tool
)

# ==================== 写作工具 ====================
from .writing_tools import (
    # AI Service 设置
    set_ai_service,
    # 续写工具
    ContinueWritingInput,
    ContinueWritingOutput,
    continue_writing_tool,
    # 润色工具
    PolishTextInput,
    PolishTextOutput,
    polish_text_tool,
    # 扩写工具
    ExpandTextInput,
    ExpandTextOutput,
    expand_text_tool
)

# ==================== 人机协同工具 ====================
from .hitl import (
    HITLManager,
    ApprovalRequest,
    ApprovalStatus
)


__all__ = [
    # ==================== 工具类型系统 ====================
    "ToolInput",
    "ToolOutput",
    "ToolCategory",
    "StandardTool",
    "InputT",
    "OutputT",

    # ==================== 工具注册表 ====================
    # 标准化注册表
    "StandardToolRegistry",
    "registry",
    # 动态注册表(兼容)
    "DynamicToolRegistry",
    "global_registry",
    "ToolDefinition",
    "ToolParameter",
    "ToolMetadata",
    "register_as_tool",

    # ==================== 写作工具 ====================
    # AI Service
    "set_ai_service",
    # 续写工具
    "ContinueWritingInput",
    "ContinueWritingOutput",
    "continue_writing_tool",
    # 润色工具
    "PolishTextInput",
    "PolishTextOutput",
    "polish_text_tool",
    # 扩写工具
    "ExpandTextInput",
    "ExpandTextOutput",
    "expand_text_tool",

    # ==================== 人机协同工具 ====================
    "HITLManager",
    "ApprovalRequest",
    "ApprovalStatus",
]

