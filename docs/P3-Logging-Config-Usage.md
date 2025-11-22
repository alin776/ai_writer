# P3级功能使用指南 - 日志与配置

## 概述

P3级修复添加了增强的日志记录和配置验证功能，提升系统的可调试性和配置安全性。

**修复完成时间**: 2025-11-22
**新增代码**: ~850行
**修复状态**: ✅ 全部完成 (2/2)

---

## 1. 增强日志记录 (P3-1)

### 模块位置
`backend/app/services/agent/memory/enhanced_logging.py`

### 核心功能

#### MemoryLogger - 增强的日志记录器

```python
from app.services.agent.memory import (
    MemoryLogger,
    LogLevel,
    OperationType,
    get_memory_logger
)

# 获取全局日志实例
logger = get_memory_logger()

# 记录添加记忆操作
logger.log_memory_add(
    user_id="user123",
    memory_id="mem456",
    content_length=150,
    importance=0.8,
    layer="short_term",
    duration_ms=12.5
)

# 记录检索操作
logger.log_memory_retrieve(
    user_id="user123",
    query="主角性格",
    result_count=5,
    total_available=20,
    duration_ms=25.3,
    retrieval_method="semantic"
)

# 详细记录遗忘操作（包含遗忘原因）
logger.log_memory_forget(
    user_id="user123",
    memory_id="mem789",
    reason="time_decay",
    forget_score=0.85,
    age_days=45.2,
    importance=0.3,
    access_count=1,
    duration_ms=8.7
)
```

**输出示例**:
```
[2025-11-22 10:30:45] INFO [memory_system:156] [add_memory] ✓ user=user123 | duration=12.50ms | memory_id=mem456 | content_length=150 | importance=0.800 | layer=short_term

[2025-11-22 10:31:02] INFO [memory_system:189] [retrieve_memory] ✓ user=user123 | duration=25.30ms | query=主角性格 | result_count=5 | total_available=20 | retrieval_method=semantic | hit_rate=25.0%

[2025-11-22 10:31:15] INFO [memory_system:212] [forget_memory] ✓ user=user123 | duration=8.70ms | memory_id=mem789 | reason=time_decay | forget_score=0.850 | age_days=45.2 | importance=0.300 | access_count=1 | decision=aged(45.2d)+low_importance(0.30)+rarely_accessed(1)+high_score(0.85)
```

#### Redis操作性能监控

```python
# 记录Redis操作性能
logger.log_redis_operation(
    operation="LRANGE",
    key_pattern="memory:st:user123",
    success=True,
    duration_ms=5.2,
    metadata={"keys_count": 10}
)

# 慢操作会自动WARNING级别记录
logger.log_redis_operation(
    operation="ZRANGE",
    key_pattern="memory:mt:*",
    success=True,
    duration_ms=1200,  # > 1000ms，自动WARNING
    metadata={"keys_count": 500}
)
```

**性能分类**:
- `excellent`: < 10ms
- `good`: 10-50ms
- `acceptable`: 50-200ms
- `slow`: 200-1000ms
- `critical`: > 1000ms (自动WARNING)

#### 重要度调整日志

```python
# 记录重要度调整
logger.log_importance_adjustment(
    user_id="user123",
    memory_id="mem456",
    old_importance=0.5,
    new_importance=0.65,
    adjustment_type="access_boost",
    factors={
        "time_decay": -0.1,
        "access_boost": +0.2,
        "context_relevance": +0.05
    },
    duration_ms=3.2
)
```

**输出示例**:
```
[2025-11-22 10:32:10] INFO [memory_system:245] [adjust_importance] ✓ user=user123 | duration=3.20ms | memory_id=mem456 | old_importance=0.500 | new_importance=0.650 | delta=+0.150 | adjustment_type=access_boost | factors={"time_decay": -0.100, "access_boost": 0.200, "context_relevance": 0.050}
```

#### 使用装饰器自动记录

```python
from app.services.agent.memory import log_memory_operation, OperationType

@log_memory_operation(OperationType.ADD_MEMORY)
async def add_memory(user_id: str, content: str):
    # 函数逻辑
    # 自动记录操作时间、成功/失败状态
    pass

@log_memory_operation(OperationType.FORGET_MEMORY)
async def forget_memory(user_id: str, memory_id: str):
    # 自动记录并捕获异常
    pass
```

#### 结构化JSON日志

```python
from app.services.agent.memory import StructuredLogger

json_logger = StructuredLogger()

# 记录JSON格式日志（便于机器解析）
json_logger.log_json({
    "operation": "memory_forget",
    "user_id": "user123",
    "memory_id": "mem789",
    "forget_score": 0.85,
    "reason": "time_decay"
}, level="INFO")
```

**JSON输出**:
```json
{
  "timestamp": "2025-11-22T10:33:00Z",
  "level": "INFO",
  "operation": "memory_forget",
  "user_id": "user123",
  "memory_id": "mem789",
  "forget_score": 0.85,
  "reason": "time_decay"
}
```

#### 批量操作日志

```python
# 记录批量操作
logger.log_batch_operation(
    operation=OperationType.DEDUPLICATE,
    user_id="user123",
    total_count=100,
    success_count=95,
    failed_count=5,
    duration_ms=250.5,
    errors=["Error 1", "Error 2", "Error 3"]
)
```

#### 错误日志

```python
try:
    # 某些操作
    pass
except Exception as e:
    logger.log_error(
        operation=OperationType.RETRIEVE_MEMORY,
        user_id="user123",
        error=e,
        context={
            "query": "主角性格",
            "layer": "short_term"
        }
    )
```

---

## 2. 配置验证 (P3-2)

### 模块位置
`backend/app/services/agent/memory/config_validator.py`

### 核心配置类

#### TTLConfig - TTL配置验证

```python
from app.services.agent.memory import TTLConfig

# 创建TTL配置
ttl_config = TTLConfig(
    short_term_ttl=3600,      # 1小时（300秒-7天）
    medium_term_ttl=86400,    # 1天（1小时-30天）
    long_term_ttl=86400*30,   # 30天（7天-1年，可选）
    version_ttl=86400*14      # 14天（1天-90天）
)

# 验证：中期TTL必须 > 短期TTL
try:
    invalid_config = TTLConfig(
        short_term_ttl=86400,
        medium_term_ttl=3600  # 错误：小于short_term_ttl
    )
except ValueError as e:
    print(f"验证失败: {e}")
    # 输出: medium_term_ttl (3600) must be greater than short_term_ttl (86400)

# 转换为timedelta
timedeltas = ttl_config.to_timedelta()
# {'short_term': timedelta(seconds=3600), 'medium_term': timedelta(days=1), ...}
```

#### CapacityConfig - 容量配置验证

```python
from app.services.agent.memory import CapacityConfig

capacity_config = CapacityConfig(
    short_term_size=20,          # 5-100
    medium_term_size=200,        # 10-1000
    long_term_size=None,         # 可选（100-10000）
    max_content_length=10000,    # 100-100000
    max_versions=50              # 5-200
)

# 验证：中期容量必须 > 短期容量
try:
    invalid = CapacityConfig(
        short_term_size=100,
        medium_term_size=50  # 错误
    )
except ValueError as e:
    print(f"验证失败: {e}")
```

#### ImportanceConfig - 重要度配置验证

```python
from app.services.agent.memory import ImportanceConfig

importance_config = ImportanceConfig(
    default_importance=0.5,      # 0.0-1.0
    critical_importance=0.9,     # 0.7-1.0，必须 > default
    low_importance=0.2,          # 0.0-0.5，必须 < default
    importance_decay_rate=0.1    # 0.01-0.5
)
```

#### MemorySystemConfig - 完整系统配置

```python
from app.services.agent.memory import (
    MemorySystemConfig,
    TTLConfig,
    CapacityConfig,
    ImportanceConfig,
    ForgetValidationConfig,
    PerformanceConfig
)

# 手动创建完整配置
config = MemorySystemConfig(
    ttl=TTLConfig(
        short_term_ttl=86400,
        medium_term_ttl=86400*7,
        version_ttl=86400*30
    ),
    capacity=CapacityConfig(
        short_term_size=20,
        medium_term_size=200
    ),
    importance=ImportanceConfig(
        default_importance=0.5,
        critical_importance=0.9,
        low_importance=0.2
    ),
    forget=ForgetValidationConfig(
        forget_threshold=0.7,
        decay_half_life_days=7.0,
        min_access_count=2,
        protect_recent_hours=24
    ),
    performance=PerformanceConfig(
        batch_size=100,
        redis_timeout=5000,
        max_retry_attempts=3,
        enable_compression=True
    ),
    enable_vector_search=False,
    enable_deduplication=True,
    enable_auto_backup=True,
    backup_interval_hours=24,
    debug_mode=False
)

# 验证并获取警告
warnings = config.validate_and_log()
# 返回: ["Short term TTL is very short (3600s), may cause frequent memory loss", ...]

# 转换为字典
config_dict = config.to_dict()

# 转换为JSON
config_json = config.to_json()

# 从JSON加载
loaded_config = MemorySystemConfig.from_json(config_json)
```

### 预定义配置模板

#### 开发环境配置

```python
from app.services.agent.memory import ConfigTemplates

dev_config = ConfigTemplates.development()

# 特点:
# - 短TTL（1小时/1天）
# - 小容量（10/50）
# - 调试模式开启
# - 宽松的超时设置
```

#### 生产环境配置

```python
prod_config = ConfigTemplates.production()

# 特点:
# - 标准TTL（24小时/7天）
# - 标准容量（20/200）
# - 自动备份开启
# - 调试模式关闭
```

#### 高性能配置

```python
hp_config = ConfigTemplates.high_performance()

# 特点:
# - 大容量（30/300）
# - 启用压缩
# - 启用向量检索
# - 启用去重
# - 大批量处理（200）
```

### 配置验证函数

```python
from app.services.agent.memory import validate_config

# 验证配置字典
config_dict = {
    "ttl": {
        "short_term_ttl": 3600,
        "medium_term_ttl": 86400
    },
    "capacity": {
        "short_term_size": 20,
        "medium_term_size": 200
    },
    "debug_mode": True
}

try:
    validated_config = validate_config(config_dict)
    print("配置验证通过！")
except Exception as e:
    print(f"配置验证失败: {e}")
```

### 集成示例

```python
from app.services.agent.memory import (
    get_unified_coordinator,
    ConfigTemplates,
    get_memory_logger
)

async def setup_memory_system(redis_client):
    """设置带日志和配置验证的记忆系统"""

    # 1. 加载并验证配置
    config = ConfigTemplates.production()
    warnings = config.validate_and_log()
    if warnings:
        print(f"配置警告: {len(warnings)}个")

    # 2. 设置日志记录器
    logger = get_memory_logger()

    # 3. 创建协调器
    coordinator = get_unified_coordinator(redis_client)

    # 4. 使用系统（自动记录日志）
    memory_id = await coordinator.add_memory(
        user_id="user123",
        content="测试内容",
        role="user",
        importance=0.7
    )

    # 日志自动输出:
    # [add_memory] ✓ user=user123 | duration=15.23ms | ...

    return coordinator
```

---

## 日志级别配置

### 设置日志级别

```python
import logging
from app.services.agent.memory import get_memory_logger

logger = get_memory_logger()
logger.logger.setLevel(logging.DEBUG)  # 显示所有日志

# 或者
logger.logger.setLevel(logging.WARNING)  # 只显示警告和错误
```

### 自定义日志格式

```python
import logging
from app.services.agent.memory import MemoryLogger

# 创建自定义logger
custom_logger = MemoryLogger("my_memory_system")

# 添加文件处理器
file_handler = logging.FileHandler("memory_operations.log")
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
))
custom_logger.logger.addHandler(file_handler)
```

---

## 性能建议

### 日志记录
- 生产环境：使用INFO级别，关键操作使用WARNING
- 开发环境：使用DEBUG级别，查看所有操作细节
- 性能测试：临时关闭日志或使用ERROR级别

### 配置验证
- 启动时验证一次配置，不要在运行时频繁验证
- 使用预定义模板减少配置错误
- 定期检查配置警告，优化配置参数

---

## 相关文档

- [ReAct记忆模块缺陷深度分析报告](./ReAct记忆模块缺陷深度分析报告.md)
- [ReAct修复总结报告](./ReAct-Memory-Fix-Summary.md)
- [P2功能使用指南](./P2-Memory-Enhancement-Usage.md)

**修复完成**: 2025-11-22
**功能状态**: ✅ 生产就绪
