# P2级记忆增强功能使用指南

## 概述

P2级增强为ReAct记忆系统添加了6个高级功能模块，所有模块已集成到记忆系统中，可通过统一接口访问。

**修复完成时间**: 2025-11-22
**总代码行数**: ~3100行
**修复状态**: ✅ 全部完成 (6/6)

---

## 1. 统一接口抽象 (P2-1)

### 模块位置
`backend/app/services/agent/memory/interfaces.py`

### 核心接口

```python
from app.services.agent.memory import (
    IMemoryManager,      # 记忆管理器核心接口
    IMemoryStore,        # 存储接口
    IMemoryRetriever,    # 检索接口
    IForgetStrategy,     # 遗忘策略接口
    IImportanceEvaluator,# 重要度评估接口
    IContextBuilder,     # 上下文构建接口
    MemoryEntry,         # 统一记忆条目
    MemoryManagerFactory # 工厂模式
)
```

### 使用示例

```python
# 使用工厂模式创建记忆管理器
factory = MemoryManagerFactory()
memory_manager = factory.create_manager("enhanced", redis_client=redis)

# 使用装饰器记录操作
from app.services.agent.memory import memory_operation

@memory_operation("custom_operation")
async def my_memory_operation(user_id: str):
    # 操作会被自动记录
    pass
```

---

## 2. 动态重要度调整 (P2-2)

### 模块位置
`backend/app/services/agent/memory/importance_adjuster.py`

### 使用示例

```python
from app.services.agent.memory import (
    DynamicImportanceAdjuster,
    AdjustmentConfig,
    get_importance_adjuster
)

# 获取全局调整器实例
adjuster = get_importance_adjuster(redis_client)

# 配置调整参数
config = AdjustmentConfig(
    decay_half_life_days=7.0,     # 7天半衰期
    access_boost_factor=0.1,      # 访问提升10%
    context_boost=0.1,            # 上下文相关性提升10%
    reference_boost=0.15          # 被引用提升15%
)

# 访问时调整重要度
new_importance = await adjuster.adjust_on_access(
    user_id="user123",
    memory_id="mem456",
    current_importance=0.5,
    access_count=3,
    last_access=datetime.now()
)

# 应用时间衰减（艾宾浩斯遗忘曲线）
memories = [
    {"id": "m1", "importance": 0.8, "timestamp": "2025-11-15T10:00:00"},
    {"id": "m2", "importance": 0.6, "timestamp": "2025-11-20T10:00:00"}
]
decayed_memories = await adjuster.apply_time_decay("user123", memories)

# 根据上下文调整
adjusted = await adjuster.adjust_by_context(
    user_id="user123",
    memories=memories,
    current_query="主角的性格特点",
    keywords=["主角", "性格"]
)
```

---

## 3. 版本控制和回滚 (P2-3)

### 模块位置
`backend/app/services/agent/memory/version_control.py`

### 使用示例

```python
from app.services.agent.memory import (
    MemoryVersionControl,
    VersionType,
    get_version_control
)

# 获取版本控制实例
vc = get_version_control(redis_client)

# 创建手动版本
version_id = await vc.create_version(
    user_id="user123",
    version_type=VersionType.MANUAL,
    description="修改主角设定前的备份"
)
print(f"Created version: {version_id}")

# 列出版本历史
versions = await vc.list_versions(
    user_id="user123",
    limit=10,
    version_type=VersionType.MANUAL
)
for v in versions:
    print(f"{v['version_id']}: {v['description']} ({v['total_memories']} memories)")

# 回滚到指定版本
success = await vc.rollback_to_version(
    user_id="user123",
    version_id=version_id,
    create_backup=True  # 回滚前自动备份当前状态
)

# 比较版本差异
diff = await vc.compare_versions(
    user_id="user123",
    version_id_from="v1",
    version_id_to="v2"
)
print(f"Added: {len(diff.added_memories)}")
print(f"Removed: {len(diff.removed_memories)}")
print(f"Modified: {len(diff.modified_memories)}")
```

---

## 4. 跨会话记忆关联 (P2-4)

### 模块位置
`backend/app/services/agent/memory/cross_session_linker.py`

### 使用示例

```python
from app.services.agent.memory import (
    CrossSessionLinker,
    EntityType,
    get_cross_session_linker
)

# 获取关联器实例
linker = get_cross_session_linker(redis_client)

# 注册实体
entity_id = await linker.register_entity(
    user_id="user123",
    entity_name="张三",
    entity_type=EntityType.CHARACTER,
    session_id="session001",
    memory_id="mem001",
    context="主角的好友，性格开朗"
)

# 自动提取并注册实体
content = "张三在北京遇到了李四，他们一起去了天安门"
extracted_ids = await linker.extract_and_register(
    user_id="user123",
    session_id="session002",
    memory_id="mem002",
    content=content
)
print(f"Extracted {len(extracted_ids)} entities")

# 按实体查找相关记忆（跨会话）
memories = await linker.find_by_entity(
    user_id="user123",
    entity_name="张三",
    limit=10
)
for mem in memories:
    print(f"Session {mem['session_id']}: {mem['context']}")

# 查找相关实体
related = await linker.find_related_entities(
    user_id="user123",
    entity_name="张三",
    limit=5
)

# 获取实体关系图谱
graph = await linker.get_entity_graph(
    user_id="user123",
    limit=50
)
print(f"Nodes: {len(graph['nodes'])}, Edges: {len(graph['edges'])}")
```

---

## 5. 高级遗忘策略 (P2-5)

### 模块位置
`backend/app/services/agent/memory/advanced_forget_strategy.py`

### 使用示例

```python
from app.services.agent.memory import (
    AdvancedForgetStrategy,
    ForgetConfig,
    ForgetStage,
    ProtectionLevel
)

# 创建策略实例
config = ForgetConfig(
    decay_half_life_days=7.0,
    critical_importance=0.9,
    fading_threshold=0.3,
    forgotten_threshold=0.85
)
strategy = AdvancedForgetStrategy(redis_client, config)

# 计算遗忘分数
memory = {
    "id": "m1",
    "content": "主角的性格设定",
    "importance": 0.8,
    "timestamp": "2025-11-15T10:00:00",
    "access_count": 5,
    "last_access": "2025-11-20T10:00:00",
    "links": 3,
    "metadata": {"protected": False}
}

score, factors = await strategy.calculate_forget_score(
    memory=memory,
    current_context="当前正在讨论配角设定"
)
print(f"Forget score: {score:.3f}")
print(f"Factors: time={factors['time']:.3f}, importance={factors['importance']:.3f}")

# 选择待遗忘记忆
memories = [...]  # 记忆列表
to_forget = await strategy.select_memories_to_forget(
    memories=memories,
    target_count=10,
    current_context="当前情节"
)

# 应用渐进式遗忘
result = await strategy.apply_gradual_forgetting(
    memories=memories,
    current_context="当前情节"
)
print(f"ACTIVE: {len(result['ACTIVE'])}")
print(f"FADING: {len(result['FADING'])}")
print(f"DORMANT: {len(result['DORMANT'])}")
print(f"ARCHIVED: {len(result['ARCHIVED'])}")
print(f"FORGOTTEN: {len(result['FORGOTTEN'])}")
```

### 保护级别说明

| 级别 | 描述 | 遗忘分数调整 |
|------|------|-------------|
| NONE | 无保护 | 0 |
| LOW | 低保护 | -0.1 |
| MEDIUM | 中等保护 | -0.2 |
| HIGH | 高保护 | -0.4 |
| PERMANENT | 永久保护 | -1.0 (永不遗忘) |

---

## 6. 记忆导入导出 (P2-6)

### 模块位置
`backend/app/services/agent/memory/import_export.py`

### 使用示例

```python
from app.services.agent.memory import (
    MemoryExporter,
    MemoryImporter,
    MemoryMigrator,
    ExportFormat,
    export_memories,
    import_memories
)

# === 导出记忆 ===

exporter = MemoryExporter(redis_client)

# 导出为JSON
json_data = await exporter.export_json(
    user_id="user123",
    include_metadata=True,
    pretty=True
)
with open("memories.json", "w", encoding="utf-8") as f:
    f.write(json_data)

# 导出为压缩JSON（适合大数据）
compressed = await exporter.export_compressed_json(user_id="user123")
with open("memories.json.gz", "wb") as f:
    f.write(compressed)

# 导出为CSV（适合Excel）
csv_data = await exporter.export_csv(
    user_id="user123",
    include_content=True
)
with open("memories.csv", "w", encoding="utf-8") as f:
    f.write(csv_data)

# 导出为Markdown（可读性好）
md_data = await exporter.export_markdown(
    user_id="user123",
    include_stats=True
)
with open("memories.md", "w", encoding="utf-8") as f:
    f.write(md_data)

# 便捷导出函数
data = await export_memories(
    redis_client=redis_client,
    user_id="user123",
    format=ExportFormat.JSON
)

# === 导入记忆 ===

importer = MemoryImporter(redis_client)

# 从JSON导入
with open("memories.json", "r", encoding="utf-8") as f:
    json_data = f.read()

result = await importer.import_json(
    user_id="user456",
    json_data=json_data,
    merge=True,           # 合并模式
    overwrite_existing=False
)
print(f"Imported: {result.imported_count}")
print(f"Skipped: {result.skipped_count}")
print(f"Failed: {result.failed_count}")

# 从压缩JSON导入
with open("memories.json.gz", "rb") as f:
    compressed = f.read()

result = await importer.import_compressed_json(
    user_id="user456",
    compressed_data=compressed,
    merge=True
)

# 便捷导入函数
result = await import_memories(
    redis_client=redis_client,
    user_id="user456",
    data=json_data,
    merge=True
)

# === 记忆迁移 ===

migrator = MemoryMigrator(redis_client)

# 用户间迁移
result = await migrator.migrate_user(
    from_user_id="old_user",
    to_user_id="new_user",
    delete_source=False  # 保留源数据
)

# 批量克隆
result_map = await migrator.clone_memories(
    source_user_id="template_user",
    target_user_ids=["user1", "user2", "user3"]
)
for user_id, result in result_map.items():
    print(f"{user_id}: imported {result.imported_count} memories")
```

---

## 集成使用示例

将多个P2功能组合使用的完整示例：

```python
from app.services.agent.memory import (
    get_unified_coordinator,
    get_importance_adjuster,
    get_version_control,
    get_cross_session_linker,
    AdvancedForgetStrategy,
    MemoryExporter,
    VersionType,
    ExportFormat
)

async def advanced_memory_workflow(user_id: str, redis_client):
    """高级记忆管理工作流"""

    # 1. 获取统一协调器
    coordinator = get_unified_coordinator(redis_client)

    # 2. 添加记忆前创建版本快照
    vc = get_version_control(redis_client)
    backup_version = await vc.create_version(
        user_id=user_id,
        version_type=VersionType.CHECKPOINT,
        description="操作前备份"
    )

    # 3. 添加记忆并自动提取实体
    memory_id = await coordinator.add_memory(
        user_id=user_id,
        content="张三和李四在北京讨论新小说的情节",
        role="user",
        importance=0.7
    )

    linker = get_cross_session_linker(redis_client)
    await linker.extract_and_register(
        user_id=user_id,
        session_id="session001",
        memory_id=memory_id,
        content="张三和李四在北京讨论新小说的情节"
    )

    # 4. 定期调整重要度
    adjuster = get_importance_adjuster(redis_client)
    memories = await coordinator.retrieve_memories(user_id, limit=100)
    await adjuster.apply_time_decay(user_id, memories)

    # 5. 应用高级遗忘策略
    strategy = AdvancedForgetStrategy(redis_client)
    await strategy.apply_gradual_forgetting(
        memories=memories,
        current_context="当前正在编写第三章"
    )

    # 6. 导出备份
    exporter = MemoryExporter(redis_client)
    backup_data = await exporter.export_compressed_json(user_id)

    return {
        "backup_version": backup_version,
        "memory_id": memory_id,
        "backup_size": len(backup_data)
    }
```

---

## 技术特性总结

| 模块 | 核心技术 | 性能特点 |
|------|----------|----------|
| P2-1 接口抽象 | ABC抽象基类、工厂模式 | 依赖注入、易测试 |
| P2-2 重要度调整 | 艾宾浩斯遗忘曲线 | O(n)时间复杂度 |
| P2-3 版本控制 | gzip压缩、快照 | 30天TTL、最多50版本 |
| P2-4 跨会话关联 | 中文NER、实体图谱 | 60+姓氏、多种实体类型 |
| P2-5 高级遗忘 | 多维度评分、5阶段 | 6因子加权计算 |
| P2-6 导入导出 | 多格式支持、迁移 | JSON/CSV/MD/压缩 |

---

## 相关文档

- [ReAct记忆模块缺陷深度分析报告](./ReAct记忆模块缺陷深度分析报告.md)
- [P0/P1级修复文档](./P0-P1-Memory-Fixes.md)
- API文档: `backend/app/services/agent/memory/`

**修复完成**: 2025-11-22
**总体进度**: P0(8/8) + P1(7/7) + P2(6/6) = 21/23 (91%)
