"""
Agent 系统配置管理

提供统一的配置管理，支持环境变量、配置文件和默认值。
"""

import os
from typing import Dict, Any, Optional, List
from pydantic import Field, ConfigDict
from pathlib import Path

# 尝试从 pydantic-settings 导入，如果不可用则使用 pydantic
try:
    from pydantic_settings import BaseSettings
except ImportError:
    # 降级使用 pydantic v2 兼容方式
    from pydantic import BaseModel as BaseSettings


class AgentConfig(BaseSettings):
    """
    Agent 系统配置类

    支持从环境变量、.env文件和默认值加载配置
    """

    # ==================== 模型配置 ====================

    # 默认模型
    DEFAULT_MODEL: str = Field(
        default="gemini-2.5-flash",
        description="默认使用的AI模型"
    )

    FALLBACK_MODEL: str = Field(
        default="gemini-2.5-flash-lite",
        description="降级使用的AI模型"
    )

    # 模型选择器配置
    ENABLE_MODEL_SELECTOR: bool = Field(
        default=True,
        description="是否启用智能模型选择器"
    )

    ENABLE_COST_TRACKING: bool = Field(
        default=True,
        description="是否启用成本追踪"
    )

    # ==================== 性能配置 ====================

    # 并发控制
    MAX_CONCURRENT_ACTIONS: int = Field(
        default=5,
        ge=1,
        le=20,
        description="最大并发Action数量"
    )

    MAX_CONCURRENT_TOOLS: int = Field(
        default=3,
        ge=1,
        le=10,
        description="最大并发工具调用数量"
    )

    # 超时配置
    ACTION_TIMEOUT: int = Field(
        default=300,
        ge=30,
        le=600,
        description="Action执行超时时间（秒）"
    )

    TOOL_TIMEOUT: int = Field(
        default=60,
        ge=10,
        le=300,
        description="工具调用超时时间（秒）"
    )

    LLM_TIMEOUT: int = Field(
        default=120,
        ge=30,
        le=300,
        description="LLM调用超时时间（秒）"
    )

    # ==================== 缓存配置 ====================

    # Memory系统
    MEMORY_SHORT_TERM_SIZE: int = Field(
        default=10,
        ge=5,
        le=50,
        description="短期记忆最大条数"
    )

    MEMORY_MEDIUM_TERM_SIZE: int = Field(
        default=100,
        ge=50,
        le=500,
        description="中期记忆最大条数"
    )

    MEMORY_CACHE_SIZE: int = Field(
        default=1000,
        ge=100,
        le=10000,
        description="内存缓存大小"
    )

    MEMORY_FORGET_THRESHOLD: float = Field(
        default=0.1,
        ge=0.0,
        le=1.0,
        description="记忆遗忘阈值"
    )

    # Redis配置
    REDIS_TTL: int = Field(
        default=3600,
        ge=60,
        le=86400,
        description="Redis缓存TTL（秒）"
    )

    REDIS_CONNECTION_POOL_SIZE: int = Field(
        default=20,
        ge=5,
        le=50,
        description="Redis连接池大小"
    )

    # ==================== 质量控制配置 ====================

    # 质量评估
    QUALITY_THRESHOLD: float = Field(
        default=8.0,
        ge=1.0,
        le=10.0,
        description="内容质量阈值"
    )

    MAX_QUALITY_RETRIES: int = Field(
        default=3,
        ge=1,
        le=5,
        description="质量循环最大重试次数"
    )

    ENABLE_QUALITY_CACHE: bool = Field(
        default=True,
        description="是否启用质量评估缓存"
    )

    # ==================== 错误处理配置 ====================

    # 重试配置
    DEFAULT_MAX_RETRIES: int = Field(
        default=3,
        ge=1,
        le=10,
        description="默认最大重试次数"
    )

    DEFAULT_RETRY_DELAY: float = Field(
        default=1.0,
        ge=0.1,
        le=10.0,
        description="默认重试延迟（秒）"
    )

    # 熔断器配置
    CIRCUIT_BREAKER_THRESHOLD: int = Field(
        default=5,
        ge=1,
        le=20,
        description="熔断器失败阈值"
    )

    CIRCUIT_BREAKER_TIMEOUT: float = Field(
        default=60.0,
        ge=10.0,
        le=300.0,
        description="熔断器恢复超时（秒）"
    )

    # ==================== 日志配置 ====================

    LOG_LEVEL: str = Field(
        default="INFO",
        description="日志级别"
    )

    LOG_FORMAT: str = Field(
        default="json",
        description="日志格式 (json/text)"
    )

    ENABLE_STRUCTURED_LOGGING: bool = Field(
        default=True,
        description="是否启用结构化日志"
    )

    # ==================== 监控配置 ====================

    # 性能监控
    ENABLE_PERFORMANCE_MONITORING: bool = Field(
        default=True,
        description="是否启用性能监控"
    )

    SLOW_QUERY_THRESHOLD: float = Field(
        default=10.0,
        ge=1.0,
        le=60.0,
        description="慢查询阈值（秒）"
    )

    # 成本监控
    COST_ALERT_THRESHOLD: float = Field(
        default=10.0,
        ge=1.0,
        description="成本告警阈值（美元）"
    )

    DAILY_COST_LIMIT: float = Field(
        default=50.0,
        ge=0.0,
        description="每日成本限制（美元）"
    )

    # ==================== 安全配置 ====================

    # 数据保护
    ENABLE_DATA_ENCRYPTION: bool = Field(
        default=False,
        description="是否启用数据加密"
    )

    MAX_CONTENT_LENGTH: int = Field(
        default=10000,
        ge=1000,
        le=100000,
        description="最大内容长度（字符）"
    )

    # ==================== 实验性功能 ====================

    ENABLE_EXPERIMENTAL_FEATURES: bool = Field(
        default=False,
        description="是否启用实验性功能"
    )

    ENABLE_ADVANCED_CACHING: bool = Field(
        default=False,
        description="是否启用高级缓存策略"
    )

    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=True, extra="ignore"  # 忽略额外的环境变量)
    @classmethod
    def from_env(cls, **overrides) -> "AgentConfig":
        """从环境变量创建配置"""
        return cls(**overrides)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return self.dict()

    def validate_config(self) -> List[str]:
        """
        验证配置的有效性

        Returns:
            List[str]: 验证错误列表，空列表表示验证通过
        """
        errors = []

        # 验证阈值逻辑
        if self.QUALITY_THRESHOLD < 1.0 or self.QUALITY_THRESHOLD > 10.0:
            errors.append("QUALITY_THRESHOLD 必须在 1.0-10.0 之间")

        if self.MEMORY_FORGET_THRESHOLD < 0.0 or self.MEMORY_FORGET_THRESHOLD > 1.0:
            errors.append("MEMORY_FORGET_THRESHOLD 必须在 0.0-1.0 之间")

        # 验证超时配置
        if self.TOOL_TIMEOUT >= self.ACTION_TIMEOUT:
            errors.append("TOOL_TIMEOUT 应该小于 ACTION_TIMEOUT")

        # 验证并发配置
        if self.MAX_CONCURRENT_TOOLS > self.MAX_CONCURRENT_ACTIONS:
            errors.append("MAX_CONCURRENT_TOOLS 不应该超过 MAX_CONCURRENT_ACTIONS")

        return errors

    def get_model_config(self, complexity: str = "medium") -> Dict[str, Any]:
        """
        根据复杂度获取模型配置

        Args:
            complexity: 任务复杂度 (simple/medium/complex)

        Returns:
            Dict[str, Any]: 模型配置
        """
        model_configs = {
            "simple": {
                "model": self.FALLBACK_MODEL,
                "temperature": 0.1,
                "max_tokens": 1000
            },
            "medium": {
                "model": self.DEFAULT_MODEL,
                "temperature": 0.7,
                "max_tokens": 2000
            },
            "complex": {
                "model": "gemini-2.5-pro",
                "temperature": 0.8,
                "max_tokens": 4000
            }
        }

        return model_configs.get(complexity, model_configs["medium"])

    def get_cache_config(self) -> Dict[str, Any]:
        """获取缓存配置"""
        return {
            "memory_cache_size": self.MEMORY_CACHE_SIZE,
            "redis_ttl": self.REDIS_TTL,
            "connection_pool_size": self.REDIS_CONNECTION_POOL_SIZE,
            "enable_quality_cache": self.ENABLE_QUALITY_CACHE
        }

    def get_timeout_config(self) -> Dict[str, Any]:
        """获取超时配置"""
        return {
            "action_timeout": self.ACTION_TIMEOUT,
            "tool_timeout": self.TOOL_TIMEOUT,
            "llm_timeout": self.LLM_TIMEOUT
        }

    def get_monitoring_config(self) -> Dict[str, Any]:
        """获取监控配置"""
        return {
            "enable_performance_monitoring": self.ENABLE_PERFORMANCE_MONITORING,
            "slow_query_threshold": self.SLOW_QUERY_THRESHOLD,
            "cost_alert_threshold": self.COST_ALERT_THRESHOLD,
            "daily_cost_limit": self.DAILY_COST_LIMIT
        }


# 全局配置实例
config = AgentConfig()


def get_config() -> AgentConfig:
    """获取全局配置实例"""
    return config


def reload_config(**overrides) -> AgentConfig:
    """
    重新加载配置

    Args:
        **overrides: 配置覆盖值

    Returns:
        AgentConfig: 新的配置实例
    """
    global config
    config = AgentConfig.from_env(**overrides)

    # 验证配置
    errors = config.validate_config()
    if errors:
        raise ValueError(f"配置验证失败: {', '.join(errors)}")

    return config


def load_config_from_file(config_path: Path) -> AgentConfig:
    """
    从文件加载配置

    Args:
        config_path: 配置文件路径

    Returns:
        AgentConfig: 配置实例
    """
    if not config_path.exists():
        raise FileNotFoundError(f"配置文件不存在: {config_path}")

    # 这里可以添加 YAML/JSON 配置文件解析逻辑
    # 暂时只支持环境变量

    return AgentConfig()


# 导出配置常量
DEFAULT_CONFIG = config.to_dict()
