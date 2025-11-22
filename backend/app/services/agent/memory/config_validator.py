"""
✅ P3-2修复: 配置验证机制

使用Pydantic进行配置验证，确保所有配置参数的合法性：
- TTL范围验证
- 容量限制验证
- 重要度阈值验证
- 性能参数验证
- 类型安全
"""
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional, Dict, Any, List
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)


class TTLConfig(BaseModel):
    """TTL配置（时间到期配置）"""

    short_term_ttl: int = Field(
        default=86400,  # 24小时
        ge=300,  # 最少5分钟
        le=86400 * 7,  # 最多7天
        description="短期记忆TTL（秒）"
    )

    medium_term_ttl: int = Field(
        default=86400 * 7,  # 7天
        ge=3600,  # 最少1小时
        le=86400 * 30,  # 最多30天
        description="中期记忆TTL（秒）"
    )

    long_term_ttl: Optional[int] = Field(
        default=None,
        ge=86400 * 7,  # 最少7天
        le=86400 * 365,  # 最多1年
        description="长期记忆TTL（秒），None表示永久"
    )

    version_ttl: int = Field(
        default=86400 * 30,  # 30天
        ge=86400,  # 最少1天
        le=86400 * 90,  # 最多90天
        description="版本快照TTL（秒）"
    )

    @field_validator('medium_term_ttl')
    @classmethod
    def medium_must_be_longer_than_short(cls, v, info):
        """中期TTL必须大于短期TTL"""
        if info.data.get('short_term_ttl') and v <= info.data['short_term_ttl']:
            raise ValueError(
                f"medium_term_ttl ({v}) must be greater than "
                f"short_term_ttl ({info.data['short_term_ttl']})"
            )
        return v

    @field_validator('long_term_ttl')
    @classmethod
    def long_must_be_longer_than_medium(cls, v, info):
        """长期TTL必须大于中期TTL（如果设置）"""
        if v is not None and info.data.get('medium_term_ttl'):
            if v <= info.data['medium_term_ttl']:
                raise ValueError(
                    f"long_term_ttl ({v}) must be greater than "
                    f"medium_term_ttl ({info.data['medium_term_ttl']})"
                )
        return v

    def to_timedelta(self) -> Dict[str, timedelta]:
        """转换为timedelta对象"""
        return {
            "short_term": timedelta(seconds=self.short_term_ttl),
            "medium_term": timedelta(seconds=self.medium_term_ttl),
            "long_term": timedelta(seconds=self.long_term_ttl) if self.long_term_ttl else None,
            "version": timedelta(seconds=self.version_ttl)
        }


class CapacityConfig(BaseModel):
    """容量限制配置"""

    short_term_size: int = Field(
        default=20,
        ge=5,
        le=100,
        description="短期记忆容量"
    )

    medium_term_size: int = Field(
        default=200,
        ge=10,
        le=1000,
        description="中期记忆容量"
    )

    long_term_size: Optional[int] = Field(
        default=None,
        ge=100,
        le=10000,
        description="长期记忆容量，None表示不限制"
    )

    max_content_length: int = Field(
        default=10000,
        ge=100,
        le=100000,
        description="单条记忆最大内容长度（字符）"
    )

    max_versions: int = Field(
        default=50,
        ge=5,
        le=200,
        description="最大版本数量"
    )

    @field_validator('medium_term_size')
    @classmethod
    def medium_must_be_larger_than_short(cls, v, info):
        """中期容量必须大于短期容量"""
        if info.data.get('short_term_size') and v <= info.data['short_term_size']:
            raise ValueError(
                f"medium_term_size ({v}) must be greater than "
                f"short_term_size ({info.data['short_term_size']})"
            )
        return v

    @field_validator('long_term_size')
    @classmethod
    def long_must_be_larger_than_medium(cls, v, info):
        """长期容量必须大于中期容量（如果设置）"""
        if v is not None and info.data.get('medium_term_size'):
            if v <= info.data['medium_term_size']:
                raise ValueError(
                    f"long_term_size ({v}) must be greater than "
                    f"medium_term_size ({info.data['medium_term_size']})"
                )
        return v


class ImportanceConfig(BaseModel):
    """重要度相关配置"""

    default_importance: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="默认重要度"
    )

    critical_importance: float = Field(
        default=0.9,
        ge=0.7,
        le=1.0,
        description="关键重要度阈值（高于此值不会被遗忘）"
    )

    low_importance: float = Field(
        default=0.2,
        ge=0.0,
        le=0.5,
        description="低重要度阈值（低于此值优先遗忘）"
    )

    importance_decay_rate: float = Field(
        default=0.1,
        ge=0.01,
        le=0.5,
        description="重要度衰减率"
    )

    @field_validator('critical_importance')
    @classmethod
    def critical_must_be_high(cls, v, info):
        """关键重要度必须高于默认值"""
        if info.data.get('default_importance') and v <= info.data['default_importance']:
            raise ValueError(
                f"critical_importance ({v}) must be greater than "
                f"default_importance ({info.data['default_importance']})"
            )
        return v

    @field_validator('low_importance')
    @classmethod
    def low_must_be_lower(cls, v, info):
        """低重要度必须低于默认值"""
        if info.data.get('default_importance') and v >= info.data['default_importance']:
            raise ValueError(
                f"low_importance ({v}) must be less than "
                f"default_importance ({info.data['default_importance']})"
            )
        return v


class ForgetConfig(BaseModel):
    """遗忘策略配置"""

    forget_threshold: float = Field(
        default=0.7,
        ge=0.5,
        le=0.95,
        description="遗忘分数阈值（高于此值会被遗忘）"
    )

    decay_half_life_days: float = Field(
        default=7.0,
        ge=1.0,
        le=90.0,
        description="衰减半衰期（天）"
    )

    min_access_count: int = Field(
        default=2,
        ge=0,
        le=20,
        description="最小访问次数（低于此值更容易遗忘）"
    )

    protect_recent_hours: int = Field(
        default=24,
        ge=1,
        le=168,  # 7天
        description="保护最近N小时的记忆不被遗忘"
    )


class PerformanceConfig(BaseModel):
    """性能相关配置"""

    batch_size: int = Field(
        default=100,
        ge=10,
        le=1000,
        description="批处理大小"
    )

    redis_timeout: int = Field(
        default=5000,
        ge=1000,
        le=30000,
        description="Redis操作超时（毫秒）"
    )

    max_retry_attempts: int = Field(
        default=3,
        ge=0,
        le=10,
        description="最大重试次数"
    )

    cache_ttl: int = Field(
        default=300,
        ge=60,
        le=3600,
        description="缓存TTL（秒）"
    )

    enable_compression: bool = Field(
        default=True,
        description="是否启用压缩"
    )

    compression_threshold: int = Field(
        default=1000,
        ge=100,
        le=10000,
        description="压缩阈值（字节）"
    )


class MemorySystemConfig(BaseModel):
    """记忆系统完整配置"""

    ttl: TTLConfig = Field(default_factory=TTLConfig)
    capacity: CapacityConfig = Field(default_factory=CapacityConfig)
    importance: ImportanceConfig = Field(default_factory=ImportanceConfig)
    forget: ForgetConfig = Field(default_factory=ForgetConfig)
    performance: PerformanceConfig = Field(default_factory=PerformanceConfig)

    enable_vector_search: bool = Field(
        default=False,
        description="是否启用向量检索"
    )

    enable_deduplication: bool = Field(
        default=True,
        description="是否启用去重"
    )

    enable_auto_backup: bool = Field(
        default=True,
        description="是否启用自动备份"
    )

    backup_interval_hours: int = Field(
        default=24,
        ge=1,
        le=168,
        description="备份间隔（小时）"
    )

    debug_mode: bool = Field(
        default=False,
        description="调试模式"
    )

    class Config:
        """Pydantic配置"""
        validate_assignment = True  # 赋值时也验证
        extra = "forbid"  # 禁止额外字段
        use_enum_values = True

    @model_validator(mode='after')
    def validate_overall_consistency(self):
        """验证整体一致性"""
        # 确保性能配置合理
        if self.enable_vector_search and not self.performance:
            logger.warning("Vector search enabled without performance config")

        return self

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return self.model_dump()

    def to_json(self) -> str:
        """转换为JSON"""
        return self.model_dump_json(indent=2)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MemorySystemConfig":
        """从字典创建配置"""
        return cls(**data)

    @classmethod
    def from_json(cls, json_str: str) -> "MemorySystemConfig":
        """从JSON创建配置"""
        return cls.model_validate_json(json_str)

    def validate_and_log(self) -> List[str]:
        """验证配置并返回警告信息"""
        warnings = []

        # 检查TTL设置
        if self.ttl.short_term_ttl < 3600:
            warnings.append(
                f"Short term TTL is very short ({self.ttl.short_term_ttl}s), "
                "may cause frequent memory loss"
            )

        # 检查容量设置
        if self.capacity.short_term_size > 50:
            warnings.append(
                f"Short term capacity is large ({self.capacity.short_term_size}), "
                "may impact performance"
            )

        # 检查重要度设置
        if self.importance.critical_importance < 0.8:
            warnings.append(
                f"Critical importance threshold is low ({self.importance.critical_importance}), "
                "important memories may be forgotten"
            )

        # 检查遗忘设置
        if self.forget.forget_threshold > 0.9:
            warnings.append(
                f"Forget threshold is very high ({self.forget.forget_threshold}), "
                "memories will be rarely forgotten"
            )

        # 检查性能设置
        if self.performance.redis_timeout < 3000:
            warnings.append(
                f"Redis timeout is short ({self.performance.redis_timeout}ms), "
                "may cause frequent timeouts"
            )

        # 记录警告
        for warning in warnings:
            logger.warning(f"[Config Validation] {warning}")

        return warnings


# 预定义配置模板
class ConfigTemplates:
    """预定义配置模板"""

    @staticmethod
    def development() -> MemorySystemConfig:
        """开发环境配置"""
        return MemorySystemConfig(
            ttl=TTLConfig(
                short_term_ttl=3600,  # 1小时
                medium_term_ttl=86400,  # 1天
                version_ttl=86400 * 7  # 7天
            ),
            capacity=CapacityConfig(
                short_term_size=10,
                medium_term_size=50,
                max_versions=20
            ),
            performance=PerformanceConfig(
                batch_size=50,
                redis_timeout=10000  # 10秒（开发环境较宽松）
            ),
            debug_mode=True
        )

    @staticmethod
    def production() -> MemorySystemConfig:
        """生产环境配置"""
        return MemorySystemConfig(
            ttl=TTLConfig(
                short_term_ttl=86400,  # 24小时
                medium_term_ttl=86400 * 7,  # 7天
                version_ttl=86400 * 30  # 30天
            ),
            capacity=CapacityConfig(
                short_term_size=20,
                medium_term_size=200,
                max_versions=50
            ),
            performance=PerformanceConfig(
                batch_size=100,
                redis_timeout=5000  # 5秒
            ),
            enable_auto_backup=True,
            debug_mode=False
        )

    @staticmethod
    def high_performance() -> MemorySystemConfig:
        """高性能配置"""
        return MemorySystemConfig(
            ttl=TTLConfig(
                short_term_ttl=86400,
                medium_term_ttl=86400 * 7,
                version_ttl=86400 * 14
            ),
            capacity=CapacityConfig(
                short_term_size=30,
                medium_term_size=300,
                max_versions=30
            ),
            performance=PerformanceConfig(
                batch_size=200,
                redis_timeout=3000,
                enable_compression=True,
                cache_ttl=600
            ),
            enable_vector_search=True,
            enable_deduplication=True
        )


def validate_config(config: Dict[str, Any]) -> MemorySystemConfig:
    """
    验证配置字典

    Args:
        config: 配置字典

    Returns:
        验证后的配置对象

    Raises:
        ValidationError: 如果配置无效
    """
    try:
        validated = MemorySystemConfig(**config)
        warnings = validated.validate_and_log()

        if warnings:
            logger.info(f"Configuration validated with {len(warnings)} warning(s)")

        return validated

    except Exception as e:
        logger.error(f"Configuration validation failed: {e}")
        raise


__all__ = [
    "TTLConfig",
    "CapacityConfig",
    "ImportanceConfig",
    "ForgetConfig",
    "PerformanceConfig",
    "MemorySystemConfig",
    "ConfigTemplates",
    "validate_config"
]
