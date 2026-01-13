"""
Agent 工具模块 (Agent Tools)

提供:
1. 工具类型系统 (tool_types)
2. 工具行为约束 (tool_behaviors)
3. 工具注册表 (tool_registry)
4. 写作工具集 (writing_tools)
5. 分析工具集 (analysis_tools)
6. 工具监控系统 (tool_monitor)
7. 人机协同工具 (hitl)
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

# ==================== 工具行为约束 ====================
from .tool_behaviors import (
    CategoryBehavior,
    CATEGORY_BEHAVIORS,
    get_category_behavior,
    creative_output_filter,
    apply_category_filter,
    with_creative_filter,
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
    # 扩写工具
    ExpandTextInput,
    ExpandTextOutput,
    expand_text_tool
)

# ==================== 分析工具 ====================
from .analysis_tools import (
    # 内容分析工具
    AnalyzeContentInput,
    AnalyzeContentOutput,
    analyze_content_tool,
    # 质量评估工具
    EvaluateQualityInput,
    EvaluateQualityOutput,
    evaluate_quality_tool,
    # 文本分析工具（兼容 @tool 版本）
    AnalyzeTextInput,
    AnalyzeTextOutput,
    analyze_text_tool
)

# ==================== 工具监控系统 ====================
from .tool_monitor import (
    ToolMonitor,
    get_tool_monitor,
    set_tool_monitor
)

# ==================== 人机协同工具 ====================
from .hitl import (
    HITLManager,
    ApprovalRequest,
    ApprovalStatus
)

# ==================== 高级工具 ====================
from .advanced_tools import (
    book_analysis,
    novel_review,
    ai_evaluation,
    deai_rewrite,
    search_knowledge_advanced
)

# ==================== 编辑器工具 ====================
from .editor_tools import (
    apply_chapter_edit,
    smart_continue,
    smart_rewrite,
    smart_insert,
    # StandardTool 版本
    smart_rewrite_tool,
    smart_continue_tool,
    smart_insert_tool,
    apply_chapter_edit_tool
)

# ==================== 章节管理工具 ====================
from .chapter_tools import (
    create_chapter,
    update_chapter_title,
    delete_chapter,
    update_chapter_content,
    # StandardTool 版本
    create_chapter_tool,
    update_chapter_title_tool,
    delete_chapter_tool,
    update_chapter_content_tool
)

# ==================== 定位工具（2026-01-10）====================
from .locate_tools import (
    locate_content
)

# ==================== 辅助工具（2026-01-09）====================
from .consistency_checker import check_story_consistency_tool, check_story_consistency_st
from .show_dont_tell import show_emotion_tool, enhance_scene_tool
from .style_learning import learn_style_tool, get_style_guidance_tool, analyze_style_tool

# ==================== 章节工具（StandardTool版本）====================
from app.services.agent.langgraph_tools import (
    get_context_tool_st,
    read_chapter_tool_st,
    get_chapter_by_order_tool_st,
    search_content_tool_st,
    search_analysis_fragments_tool_st,
    get_worldview_summary_tool_st,
    get_writing_context_tool_st,  # 2026-01-12: 新增聚合工具
)


__all__ = [
    # ==================== 工具类型系统 ====================
    "ToolInput",
    "ToolOutput",
    "ToolCategory",
    "StandardTool",
    "InputT",
    "OutputT",

    # ==================== 工具行为约束 ====================
    "CategoryBehavior",
    "CATEGORY_BEHAVIORS",
    "get_category_behavior",
    "creative_output_filter",
    "apply_category_filter",
    "with_creative_filter",

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
    # 扩写工具
    "ExpandTextInput",
    "ExpandTextOutput",
    "expand_text_tool",

    # ==================== 分析工具 ====================
    # 内容分析工具
    "AnalyzeContentInput",
    "AnalyzeContentOutput",
    "analyze_content_tool",
    # 质量评估工具
    "EvaluateQualityInput",
    "EvaluateQualityOutput",
    "evaluate_quality_tool",
    # 文本分析工具（兼容 @tool 版本）
    "AnalyzeTextInput",
    "AnalyzeTextOutput",
    "analyze_text_tool",

    # ==================== 工具监控系统 ====================
    "ToolMonitor",
    "get_tool_monitor",
    "set_tool_monitor",

    # ==================== 人机协同工具 ====================
    "HITLManager",
    "ApprovalRequest",
    "ApprovalStatus",

    # ==================== 高级工具 ====================
    "book_analysis",
    "novel_review",
    "ai_evaluation",
    "deai_rewrite",
    "search_knowledge_advanced",

    # ==================== 编辑器工具 ====================
    "apply_chapter_edit",
    "smart_continue",
    "smart_rewrite",
    "smart_insert",
    # StandardTool 版本
    "smart_rewrite_tool",
    "smart_continue_tool",
    "smart_insert_tool",
    "apply_chapter_edit_tool",

    # ==================== 章节管理工具 ====================
    "create_chapter",
    "update_chapter_title",
    "delete_chapter",
    "update_chapter_content",
    # StandardTool 版本
    "create_chapter_tool",
    "update_chapter_title_tool",
    "delete_chapter_tool",
    "update_chapter_content_tool",

    # ==================== 定位工具（2026-01-10）====================
    "locate_content",

    # ==================== 辅助工具（2026-01-09）====================
    "check_story_consistency_tool",
    "check_story_consistency_st",
    "show_emotion_tool",
    "enhance_scene_tool",
    "learn_style_tool",
    "get_style_guidance_tool",
    "analyze_style_tool",

    # ==================== 章节工具（StandardTool版本）====================
    "get_context_tool_st",
    "read_chapter_tool_st",
    "get_chapter_by_order_tool_st",
    "search_content_tool_st",
    "search_analysis_fragments_tool_st",
    "get_worldview_summary_tool_st",
    "get_writing_context_tool_st",  # 2026-01-12: 新增聚合工具
]


# ==================== 2025-12-14: 自动注册 StandardTool 到 registry ====================
def _register_standard_tools():
    """注册所有 StandardTool 工具到 registry（模块加载时自动执行）

    这是元数据驱动架构的基础设施，确保：
    - list_tools_by_category() 能返回正确的工具
    - find_tool_by_description() 能匹配到工具
    - get_tools_info_for_prompt() 能生成工具列表
    """
    # 写作工具
    registry.register_standard_tool(expand_text_tool)

    # 分析工具
    registry.register_standard_tool(analyze_content_tool)
    registry.register_standard_tool(analyze_text_tool)  # 2025-12-14: 新增兼容版本
    registry.register_standard_tool(evaluate_quality_tool)

    # 编辑器工具（2025-12-14: 新增）
    registry.register_standard_tool(smart_rewrite_tool)
    registry.register_standard_tool(smart_continue_tool)
    registry.register_standard_tool(smart_insert_tool)
    registry.register_standard_tool(apply_chapter_edit_tool)

    # 章节工具（2025-12-14: 新增）
    registry.register_standard_tool(get_context_tool_st)
    registry.register_standard_tool(read_chapter_tool_st)
    registry.register_standard_tool(get_chapter_by_order_tool_st)
    registry.register_standard_tool(search_content_tool_st)
    registry.register_standard_tool(search_analysis_fragments_tool_st)

    # 世界观工具
    registry.register_standard_tool(get_worldview_summary_tool_st)

    # 聚合工具（2026-01-12: 新增）
    registry.register_standard_tool(get_writing_context_tool_st)

    # 辅助工具（2026-01-09: 新增）
    registry.register_standard_tool(check_story_consistency_st)

    # 章节管理工具（2026-01-10: 新增 OPERATION 类工具）
    registry.register_standard_tool(create_chapter_tool)
    registry.register_standard_tool(update_chapter_title_tool)
    registry.register_standard_tool(delete_chapter_tool)
    registry.register_standard_tool(update_chapter_content_tool)


# 模块加载时自动注册
_register_standard_tools()

