from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import validator


class Settings(BaseSettings):
    """应用配置"""
    
    # 应用配置
    APP_NAME: str = "NovelAIde"
    APP_VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = False
    SECRET_KEY: str
    
    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # 数据库配置
    DATABASE_URL: str
    DB_ECHO: bool = False
    
    # Redis 配置
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # JWT 配置
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALGORITHM: str = "HS256"
    
    # CORS 配置
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://localhost:5174"
    ]
    
    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v

    # OpenAI 配置
    OPENAI_API_KEY: str
    OPENAI_BASE_URL: str = "https://204992.xyz/v1"
    OPENAI_MODEL: str = "gemini-2.5-pro"  # 默认模型，可通过环境变量修改

    @validator("OPENAI_TIMEOUT", pre=True)
    @classmethod
    def validate_openai_timeout(cls, v):
        if isinstance(v, (int, str)):
            timeout = int(v)
            if timeout < 1 or timeout > 600:  # 1秒到10分钟
                raise ValueError("OPENAI_TIMEOUT 必须在 1-600 秒之间")
            return timeout
        raise ValueError("OPENAI_TIMEOUT 必须是数字")

    OPENAI_TIMEOUT: int = 120  # AI调用超时时间（秒），默认120秒

    @validator("OPENAI_CONNECT_TIMEOUT", pre=True)
    @classmethod
    def validate_openai_connect_timeout(cls, v):
        if isinstance(v, (int, str)):
            timeout = int(v)
            if timeout < 1 or timeout > 60:  # 1秒到1分钟
                raise ValueError("OPENAI_CONNECT_TIMEOUT 必须在 1-60 秒之间")
            return timeout
        raise ValueError("OPENAI_CONNECT_TIMEOUT 必须是数字")

    OPENAI_CONNECT_TIMEOUT: int = 30  # 连接超时时间（秒），默认30秒

    @validator("OPENAI_MAX_RETRIES", pre=True)
    @classmethod
    def validate_openai_max_retries(cls, v):
        if isinstance(v, (int, str)):
            retries = int(v)
            if retries < 0 or retries > 10:  # 0到10次
                raise ValueError("OPENAI_MAX_RETRIES 必须在 0-10 之间")
            return retries
        raise ValueError("OPENAI_MAX_RETRIES 必须是整数")

    OPENAI_MAX_RETRIES: int = 3  # 最大重试次数，默认3次

    @validator("OPENAI_RETRY_DELAY", pre=True)
    @classmethod
    def validate_openai_retry_delay(cls, v):
        if isinstance(v, (int, float, str)):
            delay = float(v)
            if delay < 0.1 or delay > 60.0:  # 0.1秒到60秒
                raise ValueError("OPENAI_RETRY_DELAY 必须在 0.1-60.0 秒之间")
            return delay
        raise ValueError("OPENAI_RETRY_DELAY 必须是数字")

    OPENAI_RETRY_DELAY: float = 2.0  # 重试延迟（秒），默认2秒

    # LangGraph Agent 配置
    AGENT_USE_CHATGPT: bool = True  # False=HTTPAIService模式（绕过Cloudflare），True=ChatOpenAI模式（原生工具调用）

    # 🆕 双Prompt架构配置
    AGENT_USE_DUAL_PROMPT: bool = False  # True=双Prompt架构（系统层+创作层），False=传统单Prompt架构

    # 评审功能专用模型配置
    REVIEW_MODEL: str = "gemini-2.5-flash"  # 评审专用模型,速度快,响应快
    REVIEW_TIMEOUT: int = 60  # 评审超时时间(秒),gemini速度快

    # 图书分析专用模型配置
    BOOK_ANALYSIS_MODEL: str = "gemini-2.5-flash-lite"  # 图书分析专用模型,快速分析
    BOOK_ANALYSIS_TIMEOUT: int = 60  # 图书分析超时时间(秒)

    # AI 改写助手配置
    # 可用模型列表（可通过修改 enabled 字段启用/禁用模型）
    REWRITE_MODELS: dict = {
        "gemini-2.5-pro": {
            "name": "Gemini 2.5 Pro",
            "description": "复杂任务专用模型，擅长创意和细节描写",
            "enabled": True
        }
    }

    # 默认使用的模型列表
    REWRITE_DEFAULT_MODELS: List[str] = ["gemini-2.5-pro"]

    # 最多可同时使用的模型数量
    REWRITE_MAX_MODELS: int = 4

    # 改写竞技场性能优化配置
    REWRITE_MAX_CONCURRENT: int = 3  # 最大并发API请求数（避免触发限流）
    REWRITE_TIMEOUT_PER_MODEL: int = 30  # 单个模型超时时间（秒）

    # 小说分析配置
    ANALYSIS_MAX_RETRIES: int = 3  # 单章分析失败最大重试次数
    ANALYSIS_TIMEOUT: int = 3600  # 整体分析超时时间（秒），默认1小时
    ANALYSIS_MIN_CONTENT_LENGTH: int = 100  # 章节最小内容长度（字符数），用于验证
    ANALYSIS_MIN_MICRO_CONTENT_LENGTH: int = 50  # 微观分析最小内容长度（字符数）

    # ==================== Agent 增强功能配置 ====================

    # 功能开关
    ENABLE_ENHANCED_MEMORY: bool = True  # 启用增强的Memory系统
    ENABLE_QUALITY_LOOP: bool = True  # 启用质量循环机制
    ENABLE_VERSION_CONTROL: bool = True  # 启用版本管理系统
    ENABLE_MODEL_SELECTION: bool = True  # 启用智能模型选择
    ENABLE_SMART_PROMPTS: bool = True  # 启用智能Prompt库

    # Memory 系统配置
    MEMORY_SHORT_TERM_SIZE: int = 10  # 短期记忆容量（最近N条）
    MEMORY_MEDIUM_TERM_SIZE: int = 100  # 中期记忆容量（最近N条）
    MEMORY_FORGET_THRESHOLD: float = 0.1  # 遗忘阈值（重要度低于此值将被遗忘）

    # 质量循环配置
    QUALITY_LOOP_MAX_ITERATIONS: int = 3  # 质量循环最大迭代次数
    QUALITY_LOOP_PASS_THRESHOLD: float = 8.0  # 质量通过阈值（0-10分）

    # 模型选择配置
    MODEL_SIMPLE_TASK: str = "gemini-2.5-flash-lite"  # 简单任务使用的模型
    MODEL_MEDIUM_TASK: str = "gemini-2.5-flash"  # 中等任务使用的模型
    MODEL_COMPLEX_TASK: str = "gemini-2.5-pro"  # 复杂任务使用的模型

    # 成本控制配置
    ENABLE_COST_TRACKING: bool = True  # 启用成本追踪

    @validator("DAILY_COST_LIMIT_PER_USER", pre=True)
    @classmethod
    def validate_daily_cost_limit(cls, v):
        if isinstance(v, (int, float, str)):
            limit = float(v)
            if limit < 0 or limit > 1000:  # 0到1000元
                raise ValueError("DAILY_COST_LIMIT_PER_USER 必须在 0-1000 元之间")
            return limit
        raise ValueError("DAILY_COST_LIMIT_PER_USER 必须是数字")

    DAILY_COST_LIMIT_PER_USER: float = 10.0  # 每用户每天成本限额（元）

    @validator("ANALYSIS_RETRY_DELAY", pre=True)
    @classmethod
    def validate_analysis_retry_delay(cls, v):
        if isinstance(v, (int, str)):
            delay = int(v)
            if delay < 1 or delay > 300:  # 1秒到5分钟
                raise ValueError("ANALYSIS_RETRY_DELAY 必须在 1-300 秒之间")
            return delay
        raise ValueError("ANALYSIS_RETRY_DELAY 必须是整数")

    ANALYSIS_RETRY_DELAY: int = 2  # 重试延迟（秒）

    @validator("NOVEL_ANALYSIS_MAX_CONCURRENT", pre=True)
    @classmethod
    def validate_novel_analysis_max_concurrent(cls, v):
        if isinstance(v, (int, str)):
            concurrent = int(v)
            if concurrent < 1 or concurrent > 20:  # 1到20个并发
                raise ValueError("NOVEL_ANALYSIS_MAX_CONCURRENT 必须在 1-20 之间")
            return concurrent
        raise ValueError("NOVEL_ANALYSIS_MAX_CONCURRENT 必须是整数")

    NOVEL_ANALYSIS_MAX_CONCURRENT: int = 5  # 最大并发章节数（推荐5，平衡性能与稳定性）

    @validator("NOVEL_ANALYSIS_CHAPTER_TIMEOUT", pre=True)
    @classmethod
    def validate_novel_analysis_chapter_timeout(cls, v):
        if isinstance(v, (int, str)):
            timeout = int(v)
            if timeout < 30 or timeout > 1800:  # 30秒到30分钟
                raise ValueError("NOVEL_ANALYSIS_CHAPTER_TIMEOUT 必须在 30-1800 秒之间")
            return timeout
        raise ValueError("NOVEL_ANALYSIS_CHAPTER_TIMEOUT 必须是整数")

    NOVEL_ANALYSIS_CHAPTER_TIMEOUT: int = 120  # 单章超时时间（秒）

    @validator("NOVEL_ANALYSIS_BATCH_UPDATE_SIZE", pre=True)
    @classmethod
    def validate_novel_analysis_batch_update_size(cls, v):
        if isinstance(v, (int, str)):
            size = int(v)
            if size < 1 or size > 100:  # 1到100个章节
                raise ValueError("NOVEL_ANALYSIS_BATCH_UPDATE_SIZE 必须在 1-100 之间")
            return size
        raise ValueError("NOVEL_ANALYSIS_BATCH_UPDATE_SIZE 必须是整数")

    NOVEL_ANALYSIS_BATCH_UPDATE_SIZE: int = 10  # 批量更新进度的间隔（章节数）
    
    # 文件上传配置
    MAX_UPLOAD_SIZE: int = 10485760  # 10MB
    UPLOAD_DIR: str = "./uploads"

    # ==================== 世界观提取配置 ====================

    # 批次处理配置
    WORLDVIEW_CHARACTER_BATCH_SIZE: int = 20  # 角色批次大小
    WORLDVIEW_LOCATION_BATCH_SIZE: int = 15  # 地点批次大小
    WORLDVIEW_SETTING_BATCH_SIZE: int = 10  # 设定批次大小

    # 重试机制配置
    WORLDVIEW_BATCH_MAX_RETRIES: int = 3  # 单批次失败最大重试次数
    WORLDVIEW_RETRY_DELAY: int = 5  # 重试延迟（秒）

    # 进度持久化配置
    WORLDVIEW_ENABLE_PROGRESS_PERSISTENCE: bool = True  # 启用进度持久化
    WORLDVIEW_PROGRESS_SAVE_INTERVAL: int = 10  # 每处理N个批次保存一次进度

    # 腾讯云 COS 配置
    COS_HOST: Optional[str] = None
    COS_SECRET_ID: Optional[str] = None
    COS_SECRET_KEY: Optional[str] = None
    COS_REGION: Optional[str] = None
    COS_BUCKET: Optional[str] = None
    COS_SCHEME: str = "https"
    COS_PREFIX: Optional[str] = "uploads"
    
    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "./logs/app.log"
    
    # Sentry 配置
    SENTRY_DSN: str = ""
    
    # 管理员配置
    ADMIN_EMAIL: str = "admin@example.com"
    ADMIN_PASSWORD: str

    # ==================== 积分系统核心配置 ====================

    # 积分系统开关
    CREDITS_ENABLED: bool = True  # 是否启用积分系统

    # 管理员积分豁免
    ADMIN_CREDITS_EXEMPT: bool = True  # 管理员使用AI功能是否豁免积分检查

    # 美元兑积分比例（基于混合使用模型：1 USD = 12,400 积分）
    CREDITS_PER_DOLLAR: int = 12400

    # 新用户赠送积分（混合写50,000字）
    NEW_USER_GIFT_CREDITS: float = 5000.00

    # 积分有效期（天），0 表示永久
    CREDITS_EXPIRE_DAYS: int = 0

    # 兑换码默认有效期（天）
    REDEEM_CODE_EXPIRE_DAYS: int = 90

    # ==================== 邀请系统配置 ====================

    # 邀请奖励积分（混合写10,000字）
    INVITATION_REWARD_CREDITS: float = 1000.00

    # 邀请码限制
    INVITATION_MAX_USES_PER_CODE: int = 10  # 每个邀请码最多使用次数
    USER_MAX_INVITATION_CODES: int = 3  # 每个用户最多持有邀请码数
    INVITATION_CODE_EXPIRE_DAYS: int = 365  # 邀请码有效期（天）
    NEW_USER_INVITE_COOLDOWN_HOURS: int = 72  # 新用户邀请冷却时间（小时）

    # 邀请激活条件
    INVITATION_ACTIVATION_MIN_CONSUME: float = 200.00  # 激活所需最小消费积分
    INVITATION_ACTIVATION_MIN_RECHARGE: float = 1.00  # 激活所需最小充值积分
    INVITATION_ACTIVATION_DEADLINE_DAYS: int = 7  # 激活期限（天）

    # ==================== 防刷机制配置 ====================

    # IP和设备限制
    SAME_IP_REGISTER_LIMIT_24H: int = 3  # 同IP 24小时内最多注册次数
    SAME_DEVICE_REGISTER_LIMIT_7D: int = 5  # 同设备7天内最多注册次数

    # ==================== 模型智能选择配置（P0优化）====================
    MODEL_SELECTION_ENABLED: bool = True  # 启用ModelSelector智能选择

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # 忽略额外字段 (如 VITE_* 前端变量)


settings = Settings()
