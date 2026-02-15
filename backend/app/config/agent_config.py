"""
Agent system configuration management.

Provides a unified configuration layer backed by env values and defaults.
"""

import os
from typing import Dict, Any, Optional, List
from pydantic import Field, ConfigDict
from pathlib import Path

try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseModel as BaseSettings


class AgentConfig(BaseSettings):
    """
    Agent configuration model.
    
    Supports loading from environment variables with default fallbacks.
    """


    DEFAULT_MODEL: str = Field(
        default="gemini-2.5-flash",
        description="Default AI model"
    )

    FALLBACK_MODEL: str = Field(
        default="gemini-2.5-flash-lite",
        description="Fallback AI model"
    )

    ENABLE_MODEL_SELECTOR: bool = Field(
        default=True,
        description="Enable intelligent model selection"
    )

    ENABLE_COST_TRACKING: bool = Field(
        default=True,
        description="Enable cost tracking"
    )


    MAX_CONCURRENT_ACTIONS: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Maximum concurrent actions"
    )

    MAX_CONCURRENT_TOOLS: int = Field(
        default=3,
        ge=1,
        le=10,
        description="Maximum concurrent tools"
    )

    ACTION_TIMEOUT: int = Field(
        default=300,
        ge=30,
        le=600,
        description="Action timeout in seconds"
    )

    TOOL_TIMEOUT: int = Field(
        default=60,
        ge=10,
        le=300,
        description="Tool call timeout in seconds"
    )

    LLM_TIMEOUT: int = Field(
        default=120,
        ge=30,
        le=300,
        description="LLM call timeout in seconds"
    )


    MEMORY_SHORT_TERM_SIZE: int = Field(
        default=10,
        ge=5,
        le=50,
        description="Max short-term memory items"
    )

    MEMORY_MEDIUM_TERM_SIZE: int = Field(
        default=100,
        ge=50,
        le=500,
        description="Max medium-term memory items"
    )

    MEMORY_CACHE_SIZE: int = Field(
        default=1000,
        ge=100,
        le=10000,
        description="In-memory cache size"
    )

    MEMORY_FORGET_THRESHOLD: float = Field(
        default=0.1,
        ge=0.0,
        le=1.0,
        description="Memory forget threshold"
    )

    REDIS_TTL: int = Field(
        default=3600,
        ge=60,
        le=86400,
        description="Redis cache TTL in seconds"
    )

    REDIS_CONNECTION_POOL_SIZE: int = Field(
        default=20,
        ge=5,
        le=50,
        description="Redis connection pool size"
    )


    QUALITY_THRESHOLD: float = Field(
        default=8.0,
        ge=1.0,
        le=10.0,
        description="Content quality threshold"
    )

    MAX_QUALITY_RETRIES: int = Field(
        default=3,
        ge=1,
        le=5,
        description="Max quality-loop retries"
    )

    ENABLE_QUALITY_CACHE: bool = Field(
        default=True,
        description="Enable quality-evaluation cache"
    )


    DEFAULT_MAX_RETRIES: int = Field(
        default=3,
        ge=1,
        le=10,
        description="Default max retries"
    )

    DEFAULT_RETRY_DELAY: float = Field(
        default=1.0,
        ge=0.1,
        le=10.0,
        description="Default retry delay in seconds"
    )

    CIRCUIT_BREAKER_THRESHOLD: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Circuit breaker failure threshold"
    )

    CIRCUIT_BREAKER_TIMEOUT: float = Field(
        default=60.0,
        ge=10.0,
        le=300.0,
        description="Circuit breaker recovery timeout in seconds"
    )


    LOG_LEVEL: str = Field(
        default="INFO",
        description="Log level"
    )

    LOG_FORMAT: str = Field(
        default="json",
        description="Log format (json/text)"
    )

    ENABLE_STRUCTURED_LOGGING: bool = Field(
        default=True,
        description="Enable structured logging"
    )


    ENABLE_PERFORMANCE_MONITORING: bool = Field(
        default=True,
        description="Enable performance monitoring"
    )

    SLOW_QUERY_THRESHOLD: float = Field(
        default=10.0,
        ge=1.0,
        le=60.0,
        description="Slow query threshold in seconds"
    )

    COST_ALERT_THRESHOLD: float = Field(
        default=10.0,
        ge=1.0,
        description="Cost alert threshold in USD"
    )

    DAILY_COST_LIMIT: float = Field(
        default=50.0,
        ge=0.0,
        description="Daily cost limit in USD"
    )


    ENABLE_DATA_ENCRYPTION: bool = Field(
        default=False,
        description="Enable data encryption"
    )

    MAX_CONTENT_LENGTH: int = Field(
        default=10000,
        ge=1000,
        le=100000,
        description="Maximum content length in characters"
    )


    ENABLE_EXPERIMENTAL_FEATURES: bool = Field(
        default=False,
        description="Enable experimental features"
    )

    ENABLE_ADVANCED_CACHING: bool = Field(
        default=False,
        description="Enable advanced caching strategy"
    )

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )
    @classmethod
    def from_env(cls, **overrides) -> "AgentConfig":
        """Create config from environment overrides."""
        return cls(**overrides)

    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return self.dict()

    def validate_config(self) -> List[str]:
        """
        Validate config consistency.
        
        Returns:
            List[str]: Validation errors; empty means valid.
        """
        errors = []

        if self.QUALITY_THRESHOLD < 1.0 or self.QUALITY_THRESHOLD > 10.0:
            errors.append("QUALITY_THRESHOLD must be in range 1.0-10.0")

        if self.MEMORY_FORGET_THRESHOLD < 0.0 or self.MEMORY_FORGET_THRESHOLD > 1.0:
            errors.append("MEMORY_FORGET_THRESHOLD must be in range 0.0-1.0")

        if self.TOOL_TIMEOUT >= self.ACTION_TIMEOUT:
            errors.append("TOOL_TIMEOUT must be less than ACTION_TIMEOUT")

        if self.MAX_CONCURRENT_TOOLS > self.MAX_CONCURRENT_ACTIONS:
            errors.append("MAX_CONCURRENT_TOOLS must not exceed MAX_CONCURRENT_ACTIONS")

        return errors

    def get_model_config(self, complexity: str = "medium") -> Dict[str, Any]:
        """
        Get model config based on task complexity.
        
        Args:
            complexity: Task complexity (simple/medium/complex).
        
        Returns:
            Dict[str, Any]: Model configuration values.
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
        """Get cache configuration."""
        return {
            "memory_cache_size": self.MEMORY_CACHE_SIZE,
            "redis_ttl": self.REDIS_TTL,
            "connection_pool_size": self.REDIS_CONNECTION_POOL_SIZE,
            "enable_quality_cache": self.ENABLE_QUALITY_CACHE
        }

    def get_timeout_config(self) -> Dict[str, Any]:
        """Get timeout configuration."""
        return {
            "action_timeout": self.ACTION_TIMEOUT,
            "tool_timeout": self.TOOL_TIMEOUT,
            "llm_timeout": self.LLM_TIMEOUT
        }

    def get_monitoring_config(self) -> Dict[str, Any]:
        """Get monitoring configuration."""
        return {
            "enable_performance_monitoring": self.ENABLE_PERFORMANCE_MONITORING,
            "slow_query_threshold": self.SLOW_QUERY_THRESHOLD,
            "cost_alert_threshold": self.COST_ALERT_THRESHOLD,
            "daily_cost_limit": self.DAILY_COST_LIMIT
        }


config = AgentConfig()


def get_config() -> AgentConfig:
    """Get the global config instance."""
    return config


def reload_config(**overrides) -> AgentConfig:
    """
    Reload configuration with optional overrides.
    
    Args:
        **overrides: Config override values.
    
    Returns:
        AgentConfig: Reloaded config instance.
    """
    global config
    config = AgentConfig.from_env(**overrides)

    errors = config.validate_config()
    if errors:
        raise ValueError(f"Config validation failed: {', '.join(errors)}")

    return config


def load_config_from_file(config_path: Path) -> AgentConfig:
    """
    Load config from file path.
    
    Args:
        config_path: Path to a config file.
    
    Returns:
        AgentConfig: Loaded config instance.
    """
    if not config_path.exists():
        raise FileNotFoundError(f"Config file does not exist: {config_path}")


    return AgentConfig()


DEFAULT_CONFIG = config.to_dict()

