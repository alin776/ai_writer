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
    OPENAI_MODEL: str = "gpt-5"  # 默认模型，可通过环境变量修改
    OPENAI_TIMEOUT: int = 120  # AI调用超时时间（秒），默认120秒

    # LangGraph Agent 配置
    AGENT_USE_CHATGPT: bool = True  # False=HTTPAIService模式（绕过Cloudflare），True=ChatOpenAI模式（原生工具调用）

    # 评审功能专用模型配置
    REVIEW_MODEL: str = "gemini-2.5-flash"  # 评审专用模型,速度快,响应快
    REVIEW_TIMEOUT: int = 60  # 评审超时时间(秒),gemini速度快

    # 图书分析专用模型配置
    BOOK_ANALYSIS_MODEL: str = "deepseek-r1-free"  # 图书分析专用模型,默认使用免费的推理模型
    BOOK_ANALYSIS_TIMEOUT: int = 60  # 图书分析超时时间(秒),推理模型速度更快

    # AI 改写助手配置
    # 可用模型列表（可通过修改 enabled 字段启用/禁用模型）
    REWRITE_MODELS: dict = {
        "gemini-2.5-pro": {
            "name": "Gemini 2.5 Pro",
            "description": "擅长创意和细节描写",
            "enabled": True
        },
        "gpt-5": {
            "name": "GPT-5",
            "description": "平衡全能，表现稳定",
            "enabled": True
        },
        "claude-3-opus": {
            "name": "Claude 3 Opus",
            "description": "擅长深度思考和逻辑",
            "enabled": False
        },
        "gpt-4-turbo": {
            "name": "GPT-4 Turbo",
            "description": "快速高效",
            "enabled": False
        }
    }

    # 默认使用的模型列表
    REWRITE_DEFAULT_MODELS: List[str] = ["gemini-2.5-pro", "gpt-5"]

    # 最多可同时使用的模型数量
    REWRITE_MAX_MODELS: int = 4

    # 改写竞技场性能优化配置
    REWRITE_MAX_CONCURRENT: int = 3  # 最大并发API请求数（避免触发限流）
    REWRITE_TIMEOUT_PER_MODEL: int = 30  # 单个模型超时时间（秒）

    # 小说分析配置
    ANALYSIS_MAX_RETRIES: int = 3  # 单章分析失败最大重试次数
    ANALYSIS_TIMEOUT: int = 3600  # 整体分析超时时间（秒），默认1小时
    ANALYSIS_RETRY_DELAY: int = 2  # 重试延迟（秒）

    # 小说分析并发配置
    NOVEL_ANALYSIS_MAX_CONCURRENT: int = 5  # 最大并发章节数（推荐5，平衡性能与稳定性）
    NOVEL_ANALYSIS_CHAPTER_TIMEOUT: int = 120  # 单章超时时间（秒）
    NOVEL_ANALYSIS_BATCH_UPDATE_SIZE: int = 10  # 批量更新进度的间隔（章节数）
    
    # 文件上传配置
    MAX_UPLOAD_SIZE: int = 10485760  # 10MB
    UPLOAD_DIR: str = "./uploads"

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
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # 忽略额外字段 (如 VITE_* 前端变量)


settings = Settings()
