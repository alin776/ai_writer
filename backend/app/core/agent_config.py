"""
Agent系统配置

包含Agent相关的所有配置参数
"""

from typing import Dict, List


class AgentConfig:
    """Agent配置类"""

    # ==================== 记忆系统配置 ====================
    MEMORY_TTL_DAYS = 90  # 记忆保留天数
    MAX_CONVERSATIONS = 50  # 最多保留的会话摘要数
    MAX_FEEDBACK_HISTORY = 100  # 最多保留的反馈记录数

    # ==================== HITL配置 ====================
    HITL_DEFAULT_TIMEOUT_HOURS = 2  # 默认批准超时时间（小时）
    HITL_MAX_PENDING_REQUESTS = 20  # 最多待处理请求数

    # 需要批准的操作类型
    HITL_REQUIRE_APPROVAL_FOR = [
        "create_outline",  # 生成大纲
        "create_worldview",  # 创建世界观
        "create_character",  # 创建角色
        "batch_operation",  # 批量操作
        "delete_content",  # 删除内容
    ]

    # ==================== 反思机制配置 ====================
    REFLECTION_QUALITY_THRESHOLD = 80.0  # 质量阈值（0-100）
    REFLECTION_MAX_ITERATIONS = 3  # 最大迭代次数

    # ==================== 并行执行配置 ====================
    PARALLEL_MAX_CONCURRENT = 5  # 最大并发任务数

    # ==================== 风格学习配置 ====================
    STYLE_MIN_SAMPLES = 3  # 最少样本数量
    STYLE_MIN_WORDS_PER_SAMPLE = 300  # 每个样本最少字数
    STYLE_CONFIDENCE_THRESHOLD = 60.0  # 置信度阈值

    # ==================== Planning Agent配置 ====================
    PLANNING_MAX_TASKS = 50  # 单个计划最多任务数
    PLANNING_MAX_RETRIES = 3  # 任务最大重试次数

    # ==================== Agent角色配置 ====================
    AGENT_ROLES = {
        "writing": {
            "name": "写作Agent",
            "description": "负责内容创作、续写、扩写",
            "system_prompt": """你是一位专业的小说写作助手。
你的职责是帮助用户创作高质量的小说内容。
你擅长：续写、扩写、创作新内容。
请始终保持创意性、逻辑性和可读性。"""
        },
        "editing": {
            "name": "编辑Agent",
            "description": "负责内容润色、改写、优化",
            "system_prompt": """你是一位专业的文字编辑。
你的职责是优化和改进文本质量。
你擅长：润色、改写、语言优化。
请注重文字的流畅性和表达的准确性。"""
        },
        "analysis": {
            "name": "分析Agent",
            "description": "负责内容分析、评估、诊断",
            "system_prompt": """你是一位专业的文本分析师。
你的职责是分析和评估文本质量。
你擅长：质量评估、问题诊断、改进建议。
请提供客观、具体、可操作的分析结果。"""
        },
        "planning": {
            "name": "规划Agent",
            "description": "负责大纲规划、任务分解、流程设计",
            "system_prompt": """你是一位专业的创作规划师。
你的职责是帮助用户规划创作流程。
你擅长：大纲设计、任务分解、流程规划。
请提供清晰、有序、可执行的计划。"""
        }
    }

    # ==================== 工具注册配置 ====================
    # 核心工具列表
    CORE_TOOLS = [
        "continue_writing",  # 续写
        "polish_text",  # 润色
        "expand_text",  # 扩写
        "evaluate_text",  # 评估
        "search_knowledge",  # 知识库搜索
        "get_chapter_context",  # 获取章节上下文
        "create_character",  # 创建角色
        "create_worldview",  # 创建世界观
        "check_consistency",  # 一致性检查
    ]

    # ==================== 场景配置 ====================
    # 核心场景定义
    CORE_SCENARIOS = {
        "scene_a": {
            "name": "帮我写第三章",
            "description": "续写指定章节",
            "keywords": ["写", "续写", "章节"],
            "workflow": [
                "get_chapter_context",
                "search_knowledge",
                "continue_writing",
                "evaluate_text",
                "polish_text"
            ]
        },
        "scene_b": {
            "name": "我想写玄幻小说",
            "description": "从零开始创作小说",
            "keywords": ["写", "创作", "小说", "玄幻", "都市", "言情"],
            "workflow": [
                "analyze_requirement",
                "create_worldview",
                "create_character",
                "create_outline",
                "write_chapter"
            ]
        },
        "scene_c": {
            "name": "分析这段文字",
            "description": "文本分析和改进",
            "keywords": ["分析", "评估", "诊断", "不好"],
            "workflow": [
                "evaluate_text",
                "diagnose_issue",
                "suggest_fix",
                "apply_fix"
            ]
        },
        "scene_d": {
            "name": "我卡文了",
            "description": "写作辅助和灵感建议",
            "keywords": ["卡文", "灵感", "帮助", "建议"],
            "workflow": [
                "analyze_context",
                "generate_suggestions",
                "user_select",
                "execute_suggestion"
            ]
        }
    }

    # ==================== 提示词模板 ====================
    PROMPT_TEMPLATES = {
        "continue_with_style": """请根据以下风格要求续写内容。

{style_guidance}

上文：
{context}

请继续：""",

        "analyze_quality": """请评估以下文本的质量（1-100分），并指出问题和改进建议。

文本内容：
{text}

请以JSON格式返回评估结果：
{{
    "score": 分数(0-100),
    "issues": ["问题1", "问题2"],
    "suggestions": ["建议1", "建议2"]
}}""",

        "generate_outline": """请为以下小说生成详细大纲。

小说类型：{genre}
目标章节数：{chapter_count}
主题：{theme}

要求：
1. 每章包含标题和简介
2. 情节连贯、逻辑清晰
3. 有起承转合

请生成大纲："""
    }

    # ==================== 性能配置 ====================
    # 缓存配置
    CACHE_ENABLED = True
    CACHE_TTL_SECONDS = 3600  # 缓存过期时间（秒）

    # 超时配置
    AGENT_TIMEOUT_SECONDS = 300  # Agent执行超时（5分钟）
    TOOL_TIMEOUT_SECONDS = 60  # 工具调用超时（1分钟）

    # 重试配置
    MAX_RETRY_ATTEMPTS = 3  # 最大重试次数
    RETRY_DELAY_SECONDS = 1  # 重试延迟（秒）

    # ==================== 日志配置 ====================
    LOG_AGENT_ACTIONS = True  # 是否记录Agent操作
    LOG_TOOL_CALLS = True  # 是否记录工具调用
    LOG_USER_INTERACTIONS = True  # 是否记录用户交互

    # ==================== 安全配置 ====================
    # 内容过滤
    CONTENT_FILTER_ENABLED = False  # 是否启用内容过滤
    MAX_MESSAGE_LENGTH = 10000  # 最大消息长度

    # 速率限制
    RATE_LIMIT_ENABLED = True  # 是否启用速率限制
    RATE_LIMIT_PER_MINUTE = 60  # 每分钟最大请求数
    RATE_LIMIT_PER_HOUR = 1000  # 每小时最大请求数

    @classmethod
    def get_agent_role(cls, role: str) -> Dict:
        """获取Agent角色配置"""
        return cls.AGENT_ROLES.get(role, cls.AGENT_ROLES["writing"])

    @classmethod
    def get_scenario(cls, scenario_id: str) -> Dict:
        """获取场景配置"""
        return cls.CORE_SCENARIOS.get(scenario_id, {})

    @classmethod
    def match_scenario(cls, user_message: str) -> str:
        """根据用户消息匹配场景"""
        message_lower = user_message.lower()

        for scenario_id, scenario in cls.CORE_SCENARIOS.items():
            keywords = scenario.get("keywords", [])
            if any(keyword in message_lower for keyword in keywords):
                return scenario_id

        return "scene_a"  # 默认场景

    @classmethod
    def get_prompt_template(cls, template_name: str) -> str:
        """获取提示词模板"""
        return cls.PROMPT_TEMPLATES.get(template_name, "")


# 全局配置实例
agent_config = AgentConfig()
