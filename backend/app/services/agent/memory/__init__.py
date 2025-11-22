"""
Agent记忆系统模块

提供三层记忆架构:
1. 短期记忆 (Short-term Memory): 单次会话内的对话历史
2. 长期记忆 (Long-term Memory): 跨会话的用户偏好和习惯
3. 知识库 (Knowledge Base): 作品相关的世界观、人物等设定

Agent增强功能:
- EnhancedMemoryManager: 增强的记忆管理器（三层记忆+智能遗忘）
- SmartForgetStrategy: 智能遗忘策略
- MemoryItem/MemorySnapshot: 数据类型定义

统一记忆协调器（✅ P0-1修复）:
- UnifiedMemoryCoordinator: 统一入口，协调三个记忆系统
"""

# 旧的记忆系统（保持兼容性）
from .long_term_memory import LongTermMemoryService
from .user_profile import UserProfileMemory
from .memory_manager import MemoryManager

# 新的增强记忆系统
from .types import (
    MemoryItem,
    MemoryLayer,
    MemorySnapshot,
    MemoryStats,
    ForgetDecision
)
from .memory_strategy import SmartForgetStrategy
from .enhanced_memory_manager import EnhancedMemoryManager

# ✅ P0-1修复: 统一记忆协调器
from .unified_coordinator import (
    UnifiedMemoryCoordinator,
    UnifiedMemoryConfig,
    MemorySystemStatus,
    MemorySystemHealth,
    get_unified_coordinator,
    set_unified_coordinator,
    create_unified_coordinator
)

# ✅ P1-5修复: 监控系统
from .metrics import (
    MemoryMetrics,
    get_metrics,
    HealthStatus,
    HealthReport,
    Alert
)

# ✅ P1-6修复: 长期记忆持久化
from .long_term_store import (
    LongTermMemoryStore,
    get_long_term_store,
    BackupMetadata
)

# ✅ P2-1修复: 统一接口抽象
from .interfaces import (
    IMemoryManager,
    IMemoryStore,
    IMemoryRetriever,
    IForgetStrategy,
    IImportanceEvaluator,
    IContextBuilder,
    MemoryEntry,
    RetrievalResult,
    MemoryLayerType,
    MemoryManagerFactory,
    memory_operation
)

# ✅ P2-2修复: 重要度动态调整
from .importance_adjuster import (
    DynamicImportanceAdjuster,
    AdjustmentConfig,
    AdjustmentEvent,
    get_importance_adjuster
)

# ✅ P2-3修复: 版本控制
from .version_control import (
    MemoryVersionControl,
    VersionSnapshot,
    VersionDiff,
    VersionType,
    get_version_control
)

# ✅ P2-4修复: 跨会话关联
from .cross_session_linker import (
    CrossSessionLinker,
    EntityExtractor,
    Entity,
    EntityType,
    EntityLink,
    get_cross_session_linker
)

# ✅ P2-5修复: 高级遗忘策略
from .advanced_forget_strategy import (
    AdvancedForgetStrategy,
    ForgetConfig,
    ForgetStage,
    ProtectionLevel
)

# ✅ P2-6修复: 导入导出
from .import_export import (
    MemoryExporter,
    MemoryImporter,
    MemoryMigrator,
    ExportFormat,
    ExportMetadata,
    ImportResult,
    export_memories,
    import_memories
)

# ✅ P3-1修复: 增强日志记录
from .enhanced_logging import (
    MemoryLogger,
    StructuredLogger,
    LogLevel,
    OperationType,
    get_memory_logger,
    set_memory_logger,
    log_memory_operation,
    log_memory_add,
    log_memory_forget,
    log_redis_op
)

# ✅ P3-2修复: 配置验证
from .config_validator import (
    TTLConfig,
    CapacityConfig,
    ImportanceConfig,
    ForgetConfig as ForgetValidationConfig,
    PerformanceConfig,
    MemorySystemConfig,
    ConfigTemplates,
    validate_config
)

__all__ = [
    # ✅ P0-1修复: 统一记忆协调器（推荐使用）
    "UnifiedMemoryCoordinator",
    "UnifiedMemoryConfig",
    "MemorySystemStatus",
    "MemorySystemHealth",
    "get_unified_coordinator",
    "set_unified_coordinator",
    "create_unified_coordinator",

    # ✅ P1-5修复: 监控系统
    "MemoryMetrics",
    "get_metrics",
    "HealthStatus",
    "HealthReport",
    "Alert",

    # ✅ P1-6修复: 长期记忆持久化
    "LongTermMemoryStore",
    "get_long_term_store",
    "BackupMetadata",

    # 新的增强功能
    "EnhancedMemoryManager",
    "SmartForgetStrategy",
    "MemoryItem",
    "MemoryLayer",
    "MemorySnapshot",
    "MemoryStats",
    "ForgetDecision",

    # ✅ P2-1修复: 统一接口抽象
    "IMemoryManager",
    "IMemoryStore",
    "IMemoryRetriever",
    "IForgetStrategy",
    "IImportanceEvaluator",
    "IContextBuilder",
    "MemoryEntry",
    "RetrievalResult",
    "MemoryLayerType",
    "MemoryManagerFactory",
    "memory_operation",

    # ✅ P2-2修复: 重要度动态调整
    "DynamicImportanceAdjuster",
    "AdjustmentConfig",
    "AdjustmentEvent",
    "get_importance_adjuster",

    # ✅ P2-3修复: 版本控制
    "MemoryVersionControl",
    "VersionSnapshot",
    "VersionDiff",
    "VersionType",
    "get_version_control",

    # ✅ P2-4修复: 跨会话关联
    "CrossSessionLinker",
    "EntityExtractor",
    "Entity",
    "EntityType",
    "EntityLink",
    "get_cross_session_linker",

    # ✅ P2-5修复: 高级遗忘策略
    "AdvancedForgetStrategy",
    "ForgetConfig",
    "ForgetStage",
    "ProtectionLevel",

    # ✅ P2-6修复: 导入导出
    "MemoryExporter",
    "MemoryImporter",
    "MemoryMigrator",
    "ExportFormat",
    "ExportMetadata",
    "ImportResult",
    "export_memories",
    "import_memories",

    # ✅ P3-1修复: 增强日志记录
    "MemoryLogger",
    "StructuredLogger",
    "LogLevel",
    "OperationType",
    "get_memory_logger",
    "set_memory_logger",
    "log_memory_operation",
    "log_memory_add",
    "log_memory_forget",
    "log_redis_op",

    # ✅ P3-2修复: 配置验证
    "TTLConfig",
    "CapacityConfig",
    "ImportanceConfig",
    "ForgetValidationConfig",
    "PerformanceConfig",
    "MemorySystemConfig",
    "ConfigTemplates",
    "validate_config",

    # 旧的兼容接口
    "LongTermMemoryService",
    "UserProfileMemory",
    "MemoryManager"
]
