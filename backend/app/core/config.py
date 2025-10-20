from typing import List
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
    
    # 文件上传配置
    MAX_UPLOAD_SIZE: int = 10485760  # 10MB
    UPLOAD_DIR: str = "./uploads"
    
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


settings = Settings()
