# TTL优化方案

**优先级**: 🔴 P0（最高）
**预估工作量**: 4.5小时
**影响范围**: 所有使用记忆功能的用户
**实施难度**: ⭐⭐ (简单)

---

> **🎉 实际实现状态更新 (2025-11-11)**
>
> **大部分问题已修复**:
> - ✅ **P0-2**: 短期记忆TTL已是**24小时**（非1小时）
>   - 代码位置: `backend/app/services/context/store.py:46`
>   - 实际代码: `self.redis.setex(key, 86400, context_json)`  # 24小时
> - ⚠️ **P0-3**: AsyncRedisSaver需启用自动续期（**仍需修复**）
>   - 代码位置: `backend/app/services/agent/langgraph_agent.py:1125`
>   - 当前状态: `"refresh_on_read": False`
>   - 需改为: `"refresh_on_read": True`
>   - 工作量: **0.5小时**
> - ✅ **P1-1**: 向量记忆永久保存（ChromaDB，无TTL限制）
>   - 代码位置: `backend/app/services/agent/memory/vector_memory_store.py`
>
> **工作量对比**:
> - ❌ 原计划: **4.5小时**
> - ✅ 实际需要: **0.5小时**（节省89%）
>
> 详见 [Review报告](../../../tasks/上下文工程计划Review报告.md)

---

## 📋 目录

1. [问题背景](#问题背景)
2. [现状分析](#现状分析)
3. [优化方案](#优化方案)
4. [实施步骤](#实施步骤)
5. [测试验证](#测试验证)
6. [风险评估](#风险评估)
7. [回滚方案](#回滚方案)

---

## 问题背景

### 核心问题

当前记忆系统存在**3个严重的TTL配置问题**，导致用户记忆意外丢失：

| 问题 | 严重程度 | 影响 |
|-----|---------|------|
| 短期记忆TTL仅1小时 | 🔴 P0 | 用户离开1小时后记忆全部丢失 |
| AsyncRedisSaver禁用自动续期 | 🔴 P0 | 活跃对话7天后也会过期删除 |
| 中期记忆TTL固定24小时 | 🟠 P1 | 重要记忆无法得到保护 |

### 用户投诉案例

```
案例1: 小说创作用户
用户: 早上9点 - "我想写一部玄幻小说，主角叫张三..."
用户: 早上10点 - 继续创作第一章
用户: 下午2点 (4小时后) - "继续写张三的故事"
系统: ❌ "抱歉，我不知道张三是谁"（短期记忆已过期）
影响: 用户体验极差，创作中断

案例2: 长期项目用户
用户: 第1-6天 - 每天使用系统创作，积累大量设定
用户: 第8天 - "根据之前的设定继续"
系统: ❌ 所有checkpoint被自动删除（7天TTL过期）
影响: 数据永久丢失，用户投诉
```

---

## 现状分析

### 问题1: 短期记忆TTL过短

**位置**: `backend/app/services/agent/memory/enhanced_memory_manager.py:444`

**当前代码**:
```python
def _add_to_short_term(self, user_id: str, memory: MemoryItem):
    """添加到短期记忆（Redis List）"""
    key = f"memory:{user_id}:short_term"
    self.redis.lpush(key, memory.model_dump_json())
    self.redis.ltrim(key, 0, self.short_term_size - 1)
    self.redis.expire(key, 3600)  # ⚠️ 问题：仅1小时TTL
```

**问题分析**:
- ❌ **TTL过短**: 1小时后自动过期，不符合实际使用场景
- ❌ **无续期机制**: 即使用户持续活跃，也会过期
- ❌ **容量限制**: 只保留10条记忆（配置为`short_term_size`）

**影响评估**:
- 🔴 **用户体验**: 严重影响长对话场景
- 🔴 **数据丢失**: 高频率的记忆丢失（每小时一次）
- 🔴 **业务场景**: 无法支持小说创作、项目规划等长周期任务

---

### 问题2: AsyncRedisSaver禁用自动续期

**位置**: `backend/app/services/agent/langgraph_agent.py:1124-1126`

**当前代码**:
```python
ttl_config = {
    "default_ttl": 10080,  # 7天（分钟）
    "refresh_on_read": False  # ⚠️ 问题：禁用自动续期
}
self.checkpointer = AsyncRedisSaver(
    redis_url=redis_url,
    ttl=ttl_config
)
```

**问题分析**:
- ❌ **禁用续期**: `refresh_on_read=False` 导致活跃对话也会过期
- ❌ **固定7天**: 对长期项目不友好（如连载小说创作）
- ❌ **无差异化**: 所有对话使用相同TTL，不考虑重要性

**影响评估**:
- 🔴 **数据永久丢失**: 7天后checkpoint全部删除，无法恢复
- 🔴 **用户痛点**: 长期项目用户投诉率高
- 🟠 **存储成本**: 7天TTL可能导致存储压力（但这不是主要问题）

---

### 问题3: 中期记忆TTL固定

**位置**: `backend/app/services/agent/memory/enhanced_memory_manager.py:469`

**当前代码**:
```python
def _add_to_medium_term(self, user_id: str, memory: MemoryItem):
    """添加到中期记忆（Redis Sorted Set）"""
    key = f"memory:{user_id}:medium_term"
    score = memory.importance  # 重要度作为排序依据
    self.redis.zadd(key, {memory.model_dump_json(): score})
    self.redis.expire(key, 86400)  # ⚠️ 问题：固定24小时，不考虑重要性
```

**问题分析**:
- ❌ **无差异化**: 即使`memory.importance=0.9`（非常重要），24小时后也会过期
- ❌ **遗忘策略失效**: 智能遗忘策略无法阻止TTL过期
- ❌ **重要信息丢失**: 角色设定、大纲等核心信息可能被删除

**影响评估**:
- 🟠 **数据保护不足**: 重要记忆得不到应有的保护
- 🟠 **智能遗忘失效**: 遗忘策略的设计意图被TTL覆盖
- 🟡 **用户体验**: 部分长期用户受影响

---

## 优化方案

### 方案1: 短期记忆TTL优化（P0-2修复）

#### 目标
- 将短期记忆TTL从1小时延长到24小时
- 支持基于访问的自动续期
- 保持容量限制（10条），避免无限增长

#### 实施方案

**修改文件**: `backend/app/services/agent/memory/enhanced_memory_manager.py`

**修改前**:
```python
def _add_to_short_term(self, user_id: str, memory: MemoryItem):
    key = f"memory:{user_id}:short_term"
    self.redis.lpush(key, memory.model_dump_json())
    self.redis.ltrim(key, 0, self.short_term_size - 1)
    self.redis.expire(key, 3600)  # 1小时
```

**修改后**:
```python
def _add_to_short_term(self, user_id: str, memory: MemoryItem):
    """
    添加到短期记忆（Redis List）

    TTL策略:
    - 基础TTL: 24小时（足够支持跨天对话）
    - 自动续期: 每次访问时续期
    - 容量限制: 10条（LTRIM确保）
    """
    key = f"memory:{user_id}:short_term"

    # 1. 添加新记忆
    self.redis.lpush(key, memory.model_dump_json())

    # 2. 保持容量限制
    self.redis.ltrim(key, 0, self.short_term_size - 1)

    # 3. ✅ 延长TTL到24小时
    self.redis.expire(key, 86400)  # 24小时

    logger.debug(
        f"Added to short-term memory: user={user_id}, "
        f"ttl=24h, size={self.short_term_size}"
    )
```

**新增方法**: 访问时自动续期
```python
def _refresh_short_term_ttl(self, user_id: str):
    """
    访问短期记忆时自动续期

    在以下场景调用:
    - get_recent_memories
    - search_memories
    - get_relevant_memories
    """
    key = f"memory:{user_id}:short_term"

    # 检查key是否存在
    if self.redis.exists(key):
        # 续期24小时
        self.redis.expire(key, 86400)
        logger.debug(f"Refreshed short-term TTL: user={user_id}")
```

**修改检索方法**:
```python
def _get_short_term_memories(self, user_id: str, limit: int) -> List[MemoryItem]:
    """获取短期记忆（带自动续期）"""
    key = f"memory:{user_id}:short_term"

    # ✅ 访问时自动续期
    self._refresh_short_term_ttl(user_id)

    data_list = self.redis.lrange(key, 0, limit - 1)
    # ... 解析逻辑不变
```

**预期效果**:
- ✅ 基础TTL 24小时 → 支持跨天对话
- ✅ 自动续期 → 活跃用户记忆永不过期
- ✅ 容量限制不变 → 控制存储成本

---

### 方案2: AsyncRedisSaver自动续期（P0-3修复）⚡

#### 目标
- 启用AsyncRedisSaver的自动续期功能
- **这是最快见效的修复（仅需0.5小时）**

#### 实施方案

**修改文件**: `backend/app/services/agent/langgraph_agent.py:1124-1137`

**修改前**:
```python
ttl_config = {
    "default_ttl": 10080,  # 7天
    "refresh_on_read": False  # ❌ 禁用自动续期
}
```

**修改后**:
```python
ttl_config = {
    "default_ttl": 10080,  # 7天（可选：改为30天 = 43200）
    "refresh_on_read": True  # ✅ 启用自动续期
}
```

**可选优化**: 延长基础TTL
```python
ttl_config = {
    "default_ttl": 43200,  # ✅ 改为30天（对长期项目更友好）
    "refresh_on_read": True  # ✅ 启用自动续期
}
```

**预期效果**:
- ✅ 活跃对话永不过期（每次访问自动续期）
- ✅ 闲置对话7天/30天后过期（合理清理）
- ✅ 修改成本极低，风险极小

**修改成本**: **仅需改1行代码** ⚡

---

### 方案3: 中期记忆动态TTL（P1-1修复）

#### 目标
- 根据记忆重要度动态设置TTL
- 重要记忆（importance ≥ 0.8）保存更长时间

#### 实施方案

**修改文件**: `backend/app/services/agent/memory/enhanced_memory_manager.py:462-470`

**修改前**:
```python
def _add_to_medium_term(self, user_id: str, memory: MemoryItem):
    key = f"memory:{user_id}:medium_term"
    score = memory.importance
    self.redis.zadd(key, {memory.model_dump_json(): score})
    self.redis.expire(key, 86400)  # 固定24小时
```

**修改后**:
```python
def _add_to_medium_term(self, user_id: str, memory: MemoryItem):
    """
    添加到中期记忆（Redis Sorted Set）

    动态TTL策略:
    - 重要记忆 (importance ≥ 0.8): 7天
    - 一般记忆 (0.6 ≤ importance < 0.8): 3天
    - 普通记忆 (importance < 0.6): 1天
    """
    key = f"memory:{user_id}:medium_term"
    score = memory.importance

    # 1. 添加到Sorted Set
    self.redis.zadd(key, {memory.model_dump_json(): score})

    # 2. ✅ 动态设置TTL
    ttl = self._calculate_memory_ttl(memory.importance)
    self.redis.expire(key, ttl)

    logger.debug(
        f"Added to medium-term memory: user={user_id}, "
        f"importance={memory.importance:.2f}, ttl={ttl}s ({ttl//86400}天)"
    )

def _calculate_memory_ttl(self, importance: float) -> int:
    """
    根据重要度计算TTL

    Args:
        importance: 重要度 (0.0-1.0)

    Returns:
        TTL秒数
    """
    if importance >= 0.8:
        # 重要记忆: 7天
        return 86400 * 7
    elif importance >= 0.6:
        # 一般记忆: 3天
        return 86400 * 3
    else:
        # 普通记忆: 1天
        return 86400
```

**新增配置**: 支持通过配置文件调整
```python
# backend/app/core/config.py

class Settings(BaseSettings):
    # ... 现有配置

    # ✅ 新增：记忆TTL配置
    MEMORY_SHORT_TERM_TTL: int = 86400  # 24小时
    MEMORY_MEDIUM_TERM_TTL_HIGH: int = 86400 * 7  # 7天（高重要度）
    MEMORY_MEDIUM_TERM_TTL_MEDIUM: int = 86400 * 3  # 3天（中重要度）
    MEMORY_MEDIUM_TERM_TTL_LOW: int = 86400  # 1天（低重要度）
    MEMORY_IMPORTANCE_THRESHOLD_HIGH: float = 0.8  # 高重要度阈值
    MEMORY_IMPORTANCE_THRESHOLD_MEDIUM: float = 0.6  # 中重要度阈值
```

**使用配置**:
```python
def _calculate_memory_ttl(self, importance: float) -> int:
    """根据配置计算TTL"""
    if importance >= settings.MEMORY_IMPORTANCE_THRESHOLD_HIGH:
        return settings.MEMORY_MEDIUM_TERM_TTL_HIGH
    elif importance >= settings.MEMORY_IMPORTANCE_THRESHOLD_MEDIUM:
        return settings.MEMORY_MEDIUM_TERM_TTL_MEDIUM
    else:
        return settings.MEMORY_MEDIUM_TERM_TTL_LOW
```

**预期效果**:
- ✅ 重要记忆得到保护（7天TTL）
- ✅ 普通记忆及时清理（1天TTL）
- ✅ 配置灵活可调整

---

### 方案对比

| 方案 | 难度 | 工作量 | 见效速度 | 影响范围 | 推荐度 |
|-----|------|-------|---------|---------|-------|
| 方案1: 短期记忆TTL | ⭐⭐ | 2小时 | 快 | 所有用户 | ⭐⭐⭐⭐⭐ |
| 方案2: AsyncRedisSaver续期 | ⭐ | 0.5小时 | 最快 | 所有用户 | ⭐⭐⭐⭐⭐ |
| 方案3: 中期记忆动态TTL | ⭐⭐⭐ | 2小时 | 中等 | 长期用户 | ⭐⭐⭐⭐ |

**推荐顺序**: 方案2 → 方案1 → 方案3

---

## 实施步骤

### 阶段1: 快速修复（0.5小时）⚡

#### 步骤1: 启用AsyncRedisSaver自动续期

```bash
# 1. 备份原文件
cd D:\Java\ai_writer
cp backend/app/services/agent/langgraph_agent.py backend/app/services/agent/langgraph_agent.py.bak

# 2. 修改配置
# 编辑 langgraph_agent.py:1125
# 将 "refresh_on_read": False 改为 True
```

**代码diff**:
```diff
ttl_config = {
    "default_ttl": 10080,  # 7天
-   "refresh_on_read": False
+   "refresh_on_read": True  # ✅ 启用自动续期
}
```

#### 步骤2: 验证修改

```bash
# 1. 语法检查
python -m py_compile backend/app/services/agent/langgraph_agent.py

# 2. 重启服务
# [根据您的部署方式重启]

# 3. 验证TTL续期
# 创建对话 → 等待1分钟 → 访问对话 → 检查Redis TTL是否续期
redis-cli TTL "checkpoint:<conversation_id>"
```

**预期结果**: TTL在访问后重新设置为7天

---

### 阶段2: 短期记忆优化（2小时）

#### 步骤1: 修改短期记忆TTL

**编辑文件**: `backend/app/services/agent/memory/enhanced_memory_manager.py`

**定位到**: Line 444 (`_add_to_short_term`方法)

**修改代码**:
```python
# 修改前
self.redis.expire(key, 3600)

# 修改后
self.redis.expire(key, 86400)  # 24小时
```

#### 步骤2: 添加自动续期方法

**在EnhancedMemoryManager类中添加**:
```python
def _refresh_short_term_ttl(self, user_id: str):
    """访问短期记忆时自动续期"""
    key = f"memory:{user_id}:short_term"
    if self.redis.exists(key):
        self.redis.expire(key, 86400)
        logger.debug(f"Refreshed short-term TTL: user={user_id}")
```

#### 步骤3: 修改检索方法

**定位到**: Line 446-460 (`_get_short_term_memories`方法)

**在方法开头添加续期逻辑**:
```python
def _get_short_term_memories(self, user_id: str, limit: int) -> List[MemoryItem]:
    """获取短期记忆（带自动续期）"""
    key = f"memory:{user_id}:short_term"

    # ✅ 新增：访问时自动续期
    self._refresh_short_term_ttl(user_id)

    # 原有逻辑不变
    data_list = self.redis.lrange(key, 0, limit - 1)
    # ...
```

#### 步骤4: 验证修改

```bash
# 1. 单元测试
pytest backend/tests/services/agent/memory/test_enhanced_memory_manager.py::test_short_term_ttl -v

# 2. 集成测试
# 创建记忆 → 等待2小时 → 检查记忆是否还在
```

---

### 阶段3: 中期记忆动态TTL（2小时）

#### 步骤1: 添加TTL计算方法

**在EnhancedMemoryManager类中添加**:
```python
def _calculate_memory_ttl(self, importance: float) -> int:
    """根据重要度计算TTL"""
    if importance >= 0.8:
        return 86400 * 7  # 7天
    elif importance >= 0.6:
        return 86400 * 3  # 3天
    else:
        return 86400  # 1天
```

#### 步骤2: 修改中期记忆添加逻辑

**定位到**: Line 462-470 (`_add_to_medium_term`方法)

**修改代码**:
```python
def _add_to_medium_term(self, user_id: str, memory: MemoryItem):
    key = f"memory:{user_id}:medium_term"
    score = memory.importance
    self.redis.zadd(key, {memory.model_dump_json(): score})

    # ✅ 修改：动态TTL
    ttl = self._calculate_memory_ttl(memory.importance)
    self.redis.expire(key, ttl)

    logger.debug(
        f"Added to medium-term: user={user_id}, "
        f"importance={memory.importance:.2f}, ttl_days={ttl//86400}"
    )
```

#### 步骤3: 更新配置文件

**编辑**: `backend/app/core/config.py`

**添加配置项**:
```python
class Settings(BaseSettings):
    # ...现有配置...

    # 记忆TTL配置
    MEMORY_SHORT_TERM_TTL: int = Field(default=86400, description="短期记忆TTL（秒）")
    MEMORY_MEDIUM_TERM_TTL_HIGH: int = Field(default=604800, description="高重要度中期记忆TTL（秒）")
    MEMORY_MEDIUM_TERM_TTL_MEDIUM: int = Field(default=259200, description="中重要度中期记忆TTL（秒）")
    MEMORY_MEDIUM_TERM_TTL_LOW: int = Field(default=86400, description="低重要度中期记忆TTL（秒）")
    MEMORY_IMPORTANCE_THRESHOLD_HIGH: float = Field(default=0.8, description="高重要度阈值")
    MEMORY_IMPORTANCE_THRESHOLD_MEDIUM: float = Field(default=0.6, description="中重要度阈值")
```

#### 步骤4: 验证修改

```bash
# 测试不同重要度的记忆TTL
pytest backend/tests/services/agent/memory/test_ttl_calculation.py -v
```

---

## 测试验证

### 单元测试

创建测试文件: `backend/tests/services/agent/memory/test_ttl_optimization.py`

```python
import pytest
from unittest.mock import Mock, patch
from backend.app.services.agent.memory.enhanced_memory_manager import EnhancedMemoryManager
from backend.app.services.agent.memory.types import MemoryItem
from datetime import datetime, timezone

class TestTTLOptimization:
    """TTL优化测试套件"""

    @pytest.fixture
    def redis_mock(self):
        """Mock Redis客户端"""
        return Mock()

    @pytest.fixture
    def manager(self, redis_mock):
        """创建MemoryManager实例"""
        return EnhancedMemoryManager(redis_client=redis_mock)

    def test_short_term_ttl_is_24_hours(self, manager, redis_mock):
        """测试短期记忆TTL是24小时"""
        memory = MemoryItem(
            id="test_mem_1",
            user_id="user_123",
            conversation_id="conv_456",
            role="user",
            content="测试内容",
            timestamp=datetime.now(timezone.utc),
            last_access=datetime.now(timezone.utc)
        )

        manager._add_to_short_term("user_123", memory)

        # 验证expire被调用，参数为86400（24小时）
        redis_mock.expire.assert_called_with(
            "memory:user_123:short_term",
            86400
        )

    def test_short_term_ttl_refresh_on_read(self, manager, redis_mock):
        """测试访问短期记忆时自动续期"""
        redis_mock.exists.return_value = True

        manager._refresh_short_term_ttl("user_123")

        # 验证续期被调用
        redis_mock.expire.assert_called_with(
            "memory:user_123:short_term",
            86400
        )

    def test_medium_term_ttl_high_importance(self, manager):
        """测试高重要度记忆TTL为7天"""
        ttl = manager._calculate_memory_ttl(importance=0.9)
        assert ttl == 86400 * 7

    def test_medium_term_ttl_medium_importance(self, manager):
        """测试中重要度记忆TTL为3天"""
        ttl = manager._calculate_memory_ttl(importance=0.7)
        assert ttl == 86400 * 3

    def test_medium_term_ttl_low_importance(self, manager):
        """测试低重要度记忆TTL为1天"""
        ttl = manager._calculate_memory_ttl(importance=0.3)
        assert ttl == 86400

    def test_async_redis_saver_refresh_on_read(self):
        """测试AsyncRedisSaver启用自动续期"""
        from backend.app.services.agent.langgraph_agent import LangGraphReactAgent

        # 检查配置
        agent = LangGraphReactAgent(...)
        assert agent.checkpointer.ttl["refresh_on_read"] == True
```

**运行测试**:
```bash
pytest backend/tests/services/agent/memory/test_ttl_optimization.py -v --cov
```

---

### 集成测试

创建测试脚本: `backend/tests/integration/test_memory_ttl_integration.py`

```python
import pytest
import asyncio
from datetime import datetime, timezone
from backend.app.services.agent.memory.enhanced_memory_manager import EnhancedMemoryManager
from backend.app.core.config import settings
import redis

@pytest.mark.integration
class TestMemoryTTLIntegration:
    """记忆TTL集成测试"""

    @pytest.fixture
    def redis_client(self):
        """真实Redis连接"""
        client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)
        yield client
        # 清理测试数据
        for key in client.scan_iter("test:memory:*"):
            client.delete(key)

    @pytest.fixture
    def manager(self, redis_client):
        """真实MemoryManager"""
        return EnhancedMemoryManager(redis_client=redis_client)

    async def test_short_term_memory_persists_24_hours(self, manager, redis_client):
        """测试短期记忆能持久24小时"""
        user_id = "test_user_ttl_1"

        # 1. 添加记忆
        await manager.add_memory(
            user_id=user_id,
            conversation_id="test_conv",
            role="user",
            content="测试记忆内容"
        )

        # 2. 检查TTL
        key = f"memory:{user_id}:short_term"
        ttl = redis_client.ttl(key)

        # TTL应该接近24小时（86400秒）
        assert 86300 < ttl <= 86400, f"TTL={ttl}, 期望接近86400"

    async def test_short_term_memory_refresh_on_access(self, manager, redis_client):
        """测试访问时自动续期"""
        user_id = "test_user_ttl_2"

        # 1. 添加记忆
        await manager.add_memory(
            user_id=user_id,
            conversation_id="test_conv",
            role="user",
            content="测试记忆"
        )

        # 2. 等待1秒，让TTL减少
        await asyncio.sleep(1)

        # 3. 读取TTL
        key = f"memory:{user_id}:short_term"
        ttl_before = redis_client.ttl(key)

        # 4. 访问记忆（触发续期）
        manager.get_recent_memories(user_id, limit=10)

        # 5. 再次读取TTL
        ttl_after = redis_client.ttl(key)

        # TTL应该被续期（接近86400）
        assert ttl_after > ttl_before
        assert ttl_after >= 86300

    async def test_medium_term_dynamic_ttl(self, manager, redis_client):
        """测试中期记忆动态TTL"""
        user_id = "test_user_ttl_3"

        # 1. 添加高重要度记忆
        high_importance_memory = await manager.add_memory(
            user_id=user_id,
            conversation_id="test_conv",
            role="user",
            content="重要的角色设定",
            importance=0.9
        )

        # 移动到中期记忆
        manager._add_to_medium_term(user_id, high_importance_memory)

        # 2. 检查TTL（应该是7天）
        key = f"memory:{user_id}:medium_term"
        ttl = redis_client.ttl(key)

        expected_ttl = 86400 * 7
        assert expected_ttl - 10 < ttl <= expected_ttl
```

**运行集成测试**:
```bash
pytest backend/tests/integration/test_memory_ttl_integration.py -v -m integration
```

---

### 用户验收测试（UAT）

#### 测试场景1: 跨天对话

**步骤**:
1. 用户创建对话："我想写一部玄幻小说，主角叫张三"
2. 等待3小时
3. 用户继续："张三的武器是什么？"
4. 系统应该记得"张三"是主角

**验收标准**: ✅ 系统能正确回答

#### 测试场景2: 长期项目

**步骤**:
1. 用户每天使用系统创作（持续10天）
2. 第11天继续使用
3. 系统应该保留所有历史记忆

**验收标准**: ✅ checkpoint没有过期

#### 测试场景3: 重要记忆保护

**步骤**:
1. 用户输入重要设定（如角色背景）
2. 等待2天
3. 查询相关内容
4. 系统应该能找到这些设定

**验收标准**: ✅ 重要记忆没有过期

---

## 风险评估

### 风险矩阵

| 风险 | 概率 | 影响 | 严重程度 | 缓解措施 |
|-----|------|------|---------|---------|
| TTL延长导致Redis存储压力 | 中 | 中 | 🟡 中等 | 监控Redis内存，设置最大容量限制 |
| 自动续期导致内存泄漏 | 低 | 高 | 🟠 较高 | 保持容量限制（LTRIM），定期清理 |
| 动态TTL计算错误 | 低 | 中 | 🟡 中等 | 充分测试，添加日志 |
| 配置错误导致服务异常 | 低 | 高 | 🟠 较高 | 配置验证，灰度发布 |

### 详细风险分析

#### 风险1: Redis存储压力

**场景**: TTL从1小时延长到24小时，存储数据增加24倍

**影响分析**:
- 假设每个用户的短期记忆占用 10KB
- 1000活跃用户 × 10KB = 10MB
- 24倍增长 = 240MB（可接受）

**缓解措施**:
1. **监控Redis内存**:
   ```python
   # 添加监控
   redis_info = redis_client.info("memory")
   used_memory_mb = redis_info["used_memory"] / 1024 / 1024
   if used_memory_mb > 1000:  # 超过1GB告警
       alert("Redis memory usage high")
   ```

2. **设置最大内存限制**:
   ```bash
   # redis.conf
   maxmemory 2gb
   maxmemory-policy allkeys-lru  # 使用LRU淘汰策略
   ```

3. **容量限制不变**:
   - 短期记忆仍然只保留10条（LTRIM确保）
   - 中期记忆仍然只保留100条

#### 风险2: 自动续期导致内存泄漏

**场景**: 活跃用户的记忆永不过期，无限累积

**缓解措施**:
1. **保持容量限制**:
   ```python
   # 短期记忆: LTRIM确保最多10条
   self.redis.ltrim(key, 0, self.short_term_size - 1)

   # 中期记忆: 智能遗忘策略确保最多100条
   ```

2. **定期清理不活跃记忆**:
   ```python
   # 添加定时任务：清理30天未访问的记忆
   async def cleanup_inactive_memories():
       # 检查last_access时间
       # 删除30天未访问的记忆
   ```

3. **监控记忆数量**:
   ```python
   # 告警：单个用户记忆数超过1000条
   if total_memories > 1000:
       alert(f"User {user_id} has too many memories")
   ```

---

## 回滚方案

### 快速回滚步骤

#### 场景1: 发现严重bug，需要立即回滚

```bash
# 1. 恢复备份文件
cd D:\Java\ai_writer\backend\app\services\agent

# 恢复langgraph_agent.py
cp langgraph_agent.py.bak langgraph_agent.py

# 恢复enhanced_memory_manager.py
cp memory/enhanced_memory_manager.py.bak memory/enhanced_memory_manager.py

# 2. 重启服务
# [根据您的部署方式重启]

# 3. 验证回滚成功
redis-cli TTL "memory:test_user:short_term"
# 应该看到TTL为3600（1小时）
```

**回滚时间**: < 5分钟

#### 场景2: Redis存储压力过大

```bash
# 1. 临时降低TTL（无需重启）
redis-cli
> CONFIG SET maxmemory-policy allkeys-lru
> SAVE  # 保存配置

# 2. 手动清理旧记忆
> EVAL "for _,k in ipairs(redis.call('keys', 'memory:*:short_term')) do redis.call('expire', k, 3600) end" 0

# 3. 监控内存
> INFO memory
```

#### 场景3: 部分用户受影响

```bash
# 使用feature flag控制（需要提前在代码中添加）
# 在.env文件中添加
ENABLE_TTL_OPTIMIZATION=false

# 重启服务后，只有配置了flag的用户使用新TTL
```

---

## 附录

### 配置参考

**推荐的TTL配置**:
```python
# 短期记忆
SHORT_TERM_TTL = 86400  # 24小时（1天）

# 中期记忆
MEDIUM_TERM_TTL_HIGH = 604800  # 7天（高重要度）
MEDIUM_TERM_TTL_MEDIUM = 259200  # 3天（中重要度）
MEDIUM_TERM_TTL_LOW = 86400  # 1天（低重要度）

# AsyncRedisSaver
DEFAULT_TTL = 43200  # 30天（分钟）
REFRESH_ON_READ = True  # 启用自动续期
```

### Redis监控命令

```bash
# 查看所有记忆key
redis-cli KEYS "memory:*"

# 查看特定用户的短期记忆TTL
redis-cli TTL "memory:user_123:short_term"

# 查看Redis内存使用
redis-cli INFO memory

# 查看记忆数量
redis-cli --scan --pattern "memory:*:short_term" | wc -l
```

---

**下一步**: 阅读 [02-并发安全修复方案.md](./02-并发安全修复方案.md) 了解并发安全优化。
