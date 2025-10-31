# Memory 系统设计

> **版本**: v1.1
> **创建日期**: 2025-10-31
> **最后更新**: 2025-10-31
> **实施状态**: ✅ 已完成 (Week 1, 2025-10-28)
> **模块**: 增强的记忆管理系统

---

## 📋 目录

- [1. 设计目标](#1-设计目标)
- [2. 核心概念](#2-核心概念)
- [3. 数据模型](#3-数据模型)
- [4. 核心类设计](#4-核心类设计)
- [5. 智能遗忘策略](#5-智能遗忘策略)
- [6. 状态快照](#6-状态快照)
- [7. 存储设计](#7-存储设计)
- [8. 使用示例](#8-使用示例)

---

## 1. 设计目标

### 1.1 核心目标

- ✅ **分层记忆**: 短期/中期/长期三层记忆
- ✅ **智能遗忘**: 重要度加权，非简单FIFO
- ✅ **状态快照**: 支持快照和恢复
- ✅ **版本历史**: 追踪记忆变更
- ✅ **高性能**: 检索速度 < 100ms

### 1.2 问题分析

**当前问题**:
- 简单的 FIFO 策略，重要信息可能被遗忘
- 无法恢复历史状态
- 缺乏语义检索能力
- 长期对话性能下降

**解决方案**:
- 引入重要度计算
- 实现快照机制
- 集成向量检索
- 分层存储优化

---

## 2. 核心概念

### 2.1 三层记忆模型

```
┌──────────────────────────────────────┐
│        短期记忆 (Short-Term)         │
│    最近10条，完整保留，快速访问      │
│    Redis List, TTL: 1小时            │
└──────────────────────────────────────┘
                  ↓
┌──────────────────────────────────────┐
│        中期记忆 (Medium-Term)        │
│   最近100条，按重要度过滤，定期整理  │
│   Redis Sorted Set, TTL: 24小时     │
└──────────────────────────────────────┘
                  ↓
┌──────────────────────────────────────┐
│        长期记忆 (Long-Term)          │
│    历史所有，压缩为摘要，持久化      │
│    PostgreSQL + Redis, 永久保存      │
└──────────────────────────────────────┘
```

### 2.2 记忆重要度计算

```
重要度 = 初始重要度 × 时间衰减 × 访问频率加权

时间衰减 = e^(-decay_rate × 时间差 / 3600)
访问加权 = 1 + log(1 + access_count)
```

**示例**:
```
记忆A: 初始重要度0.8, 2小时前, 访问3次
  时间衰减 = e^(-0.1 × 2) ≈ 0.82
  访问加权 = 1 + log(1 + 3) ≈ 2.39
  重要度 = 0.8 × 0.82 × 2.39 ≈ 1.57

记忆B: 初始重要度0.5, 10小时前, 访问0次
  时间衰减 = e^(-0.1 × 10) ≈ 0.37
  访问加权 = 1
  重要度 = 0.5 × 0.37 × 1 ≈ 0.19 → 应该遗忘
```

---

## 3. 数据模型

### 3.1 MemoryItem（记忆条目）

```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, Any, Optional

class MemoryItem(BaseModel):
    """记忆条目"""

    # 基础信息
    id: str = Field(..., description="唯一标识")
    user_id: str = Field(..., description="用户ID")
    conversation_id: str = Field(..., description="会话ID")

    # 内容
    role: str = Field(..., description="角色: user/assistant/system")
    content: str = Field(..., description="记忆内容")

    # 时间信息
    timestamp: datetime = Field(..., description="创建时间")
    last_access: datetime = Field(..., description="最后访问时间")

    # 重要度相关
    importance: float = Field(0.5, ge=0, le=1, description="初始重要度")
    decay_rate: float = Field(0.1, ge=0, description="遗忘速率")
    access_count: int = Field(0, ge=0, description="访问次数")

    # 元数据
    metadata: Dict[str, Any] = Field(default_factory=dict, description="扩展元数据")

    # 向量嵌入（用于语义检索）
    embedding: Optional[List[float]] = Field(None, description="向量嵌入")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
```

### 3.2 MemoryLayer（记忆层级）

```python
from enum import Enum

class MemoryLayer(str, Enum):
    """记忆层级"""
    SHORT_TERM = "short_term"    # 短期记忆
    MEDIUM_TERM = "medium_term"  # 中期记忆
    LONG_TERM = "long_term"      # 长期记忆
```

### 3.3 MemorySnapshot（记忆快照）

```python
class MemorySnapshot(BaseModel):
    """记忆快照"""

    snapshot_id: str = Field(..., description="快照ID")
    user_id: str = Field(..., description="用户ID")
    conversation_id: str = Field(..., description="会话ID")
    created_at: datetime = Field(..., description="创建时间")

    # 快照数据
    short_term_memories: List[MemoryItem] = Field(default_factory=list)
    medium_term_memories: List[MemoryItem] = Field(default_factory=list)
    long_term_summary: str = Field("", description="长期记忆摘要")

    # 元数据
    description: str = Field("", description="快照描述")
    tags: List[str] = Field(default_factory=list, description="标签")
```

---

## 4. 核心类设计

### 4.1 EnhancedMemoryManager（增强的记忆管理器）

```python
# backend/app/services/agent/memory/enhanced_memory_manager.py

import redis
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from .memory_strategy import SmartForgetStrategy

class EnhancedMemoryManager:
    """增强的记忆管理器"""

    def __init__(self, redis_client: redis.Redis):
        """初始化"""
        self.redis = redis_client
        self.strategy = SmartForgetStrategy()

        # 配置参数
        self.short_term_size = 10
        self.medium_term_size = 100
        self.forget_threshold = 0.1

    # ==================== 记忆添加 ====================

    def add_memory(
        self,
        user_id: str,
        conversation_id: str,
        role: str,
        content: str,
        importance: float = 0.5,
        metadata: Dict = None
    ) -> MemoryItem:
        """
        添加记忆（自动分层）

        Args:
            user_id: 用户ID
            conversation_id: 会话ID
            role: 角色
            content: 内容
            importance: 初始重要度
            metadata: 元数据

        Returns:
            MemoryItem: 创建的记忆条目
        """
        # 创建记忆条目
        memory = MemoryItem(
            id=self._generate_id(),
            user_id=user_id,
            conversation_id=conversation_id,
            role=role,
            content=content,
            timestamp=datetime.now(),
            last_access=datetime.now(),
            importance=importance,
            metadata=metadata or {}
        )

        # 添加到短期记忆
        self._add_to_short_term(user_id, memory)

        # 应用遗忘策略
        self.apply_forgetting(user_id)

        return memory

    # ==================== 记忆检索 ====================

    def get_recent_memories(
        self,
        user_id: str,
        limit: int = 10,
        layer: MemoryLayer = MemoryLayer.SHORT_TERM
    ) -> List[MemoryItem]:
        """
        获取最近的记忆

        Args:
            user_id: 用户ID
            limit: 数量限制
            layer: 记忆层级

        Returns:
            List[MemoryItem]: 记忆列表
        """
        if layer == MemoryLayer.SHORT_TERM:
            return self._get_short_term_memories(user_id, limit)
        elif layer == MemoryLayer.MEDIUM_TERM:
            return self._get_medium_term_memories(user_id, limit)
        else:
            return self._get_long_term_memories(user_id, limit)

    def get_relevant_memories(
        self,
        user_id: str,
        query: str,
        top_k: int = 5,
        layer: MemoryLayer = None
    ) -> List[MemoryItem]:
        """
        获取相关记忆（基于语义相似度）

        Args:
            user_id: 用户ID
            query: 查询文本
            top_k: 返回数量
            layer: 记忆层级（None表示所有层级）

        Returns:
            List[MemoryItem]: 相关记忆列表
        """
        # 1. 生成query的嵌入
        query_embedding = self._generate_embedding(query)

        # 2. 获取候选记忆
        if layer:
            candidates = self.get_recent_memories(user_id, limit=100, layer=layer)
        else:
            # 从所有层级获取
            candidates = []
            candidates.extend(self.get_recent_memories(user_id, limit=10, layer=MemoryLayer.SHORT_TERM))
            candidates.extend(self.get_recent_memories(user_id, limit=50, layer=MemoryLayer.MEDIUM_TERM))

        # 3. 计算相似度并排序
        scored_memories = []
        for memory in candidates:
            if memory.embedding:
                similarity = self._cosine_similarity(query_embedding, memory.embedding)
                scored_memories.append((similarity, memory))

        scored_memories.sort(key=lambda x: x[0], reverse=True)

        # 4. 返回top_k
        return [memory for _, memory in scored_memories[:top_k]]

    def search_memories(
        self,
        user_id: str,
        keywords: List[str],
        limit: int = 10
    ) -> List[MemoryItem]:
        """
        关键词搜索记忆

        Args:
            user_id: 用户ID
            keywords: 关键词列表
            limit: 返回数量

        Returns:
            List[MemoryItem]: 匹配的记忆列表
        """
        # 从所有层级搜索
        all_memories = []
        all_memories.extend(self.get_recent_memories(user_id, limit=10, layer=MemoryLayer.SHORT_TERM))
        all_memories.extend(self.get_recent_memories(user_id, limit=100, layer=MemoryLayer.MEDIUM_TERM))

        # 关键词匹配
        matched = []
        for memory in all_memories:
            if any(keyword.lower() in memory.content.lower() for keyword in keywords):
                matched.append(memory)

        return matched[:limit]

    # ==================== 智能遗忘 ====================

    def apply_forgetting(self, user_id: str):
        """
        应用智能遗忘策略

        Args:
            user_id: 用户ID
        """
        # 1. 获取中期记忆
        medium_memories = self._get_medium_term_memories(user_id, limit=self.medium_term_size)

        # 2. 计算每条记忆的重要度
        current_time = datetime.now()
        for memory in medium_memories:
            importance = self.strategy.calculate_importance(memory, current_time)
            memory.metadata['current_importance'] = importance

        # 3. 筛选应该保留的记忆
        to_keep = []
        to_forget = []

        for memory in medium_memories:
            if self.strategy.should_forget(memory, self.forget_threshold):
                to_forget.append(memory)
            else:
                to_keep.append(memory)

        # 4. 更新中期记忆
        self._update_medium_term_memories(user_id, to_keep)

        # 5. 将遗忘的记忆压缩到长期记忆
        if to_forget:
            summary = self.strategy.compress_to_summary(to_forget)
            self._append_to_long_term(user_id, summary)

    # ==================== 状态快照 ====================

    def create_snapshot(
        self,
        user_id: str,
        conversation_id: str,
        description: str = ""
    ) -> str:
        """
        创建状态快照

        Args:
            user_id: 用户ID
            conversation_id: 会话ID
            description: 快照描述

        Returns:
            str: 快照ID
        """
        snapshot = MemorySnapshot(
            snapshot_id=self._generate_snapshot_id(),
            user_id=user_id,
            conversation_id=conversation_id,
            created_at=datetime.now(),
            short_term_memories=self._get_short_term_memories(user_id, limit=10),
            medium_term_memories=self._get_medium_term_memories(user_id, limit=100),
            long_term_summary=self._get_long_term_summary(user_id),
            description=description
        )

        # 保存快照到Redis
        key = f"memory:snapshot:{snapshot.snapshot_id}"
        self.redis.set(key, snapshot.json(), ex=86400 * 7)  # 保留7天

        return snapshot.snapshot_id

    def restore_snapshot(
        self,
        snapshot_id: str
    ) -> MemorySnapshot:
        """
        恢复状态快照

        Args:
            snapshot_id: 快照ID

        Returns:
            MemorySnapshot: 快照对象
        """
        key = f"memory:snapshot:{snapshot_id}"
        data = self.redis.get(key)

        if not data:
            raise ValueError(f"Snapshot {snapshot_id} not found")

        snapshot = MemorySnapshot.parse_raw(data)

        # 恢复记忆
        self._restore_memories(snapshot)

        return snapshot

    # ==================== 私有方法 ====================

    def _add_to_short_term(self, user_id: str, memory: MemoryItem):
        """添加到短期记忆"""
        key = f"memory:{user_id}:short_term"
        self.redis.lpush(key, memory.json())
        self.redis.ltrim(key, 0, self.short_term_size - 1)
        self.redis.expire(key, 3600)  # 1小时过期

    def _get_short_term_memories(self, user_id: str, limit: int) -> List[MemoryItem]:
        """获取短期记忆"""
        key = f"memory:{user_id}:short_term"
        data_list = self.redis.lrange(key, 0, limit - 1)
        return [MemoryItem.parse_raw(data) for data in data_list]

    def _get_medium_term_memories(self, user_id: str, limit: int) -> List[MemoryItem]:
        """获取中期记忆（按重要度排序）"""
        key = f"memory:{user_id}:medium_term"
        # 使用 Sorted Set，score 为重要度
        data_list = self.redis.zrevrange(key, 0, limit - 1)
        return [MemoryItem.parse_raw(data) for data in data_list]

    def _update_medium_term_memories(self, user_id: str, memories: List[MemoryItem]):
        """更新中期记忆"""
        key = f"memory:{user_id}:medium_term"
        self.redis.delete(key)

        for memory in memories:
            importance = memory.metadata.get('current_importance', 0.5)
            self.redis.zadd(key, {memory.json(): importance})

        self.redis.expire(key, 86400)  # 24小时过期

    def _get_long_term_summary(self, user_id: str) -> str:
        """获取长期记忆摘要"""
        key = f"memory:{user_id}:long_term"
        return self.redis.get(key) or ""

    def _append_to_long_term(self, user_id: str, summary: str):
        """追加到长期记忆"""
        key = f"memory:{user_id}:long_term"
        current = self.redis.get(key) or ""
        self.redis.set(key, current + "\n" + summary)

    def _generate_embedding(self, text: str) -> List[float]:
        """生成文本嵌入（使用向量模型）"""
        # TODO: 集成向量模型
        return []

    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """计算余弦相似度"""
        import numpy as np
        return float(np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))

    def _generate_id(self) -> str:
        """生成记忆ID"""
        import uuid
        return f"mem_{uuid.uuid4().hex[:12]}"

    def _generate_snapshot_id(self) -> str:
        """生成快照ID"""
        import uuid
        return f"snap_{uuid.uuid4().hex[:12]}"

    def _restore_memories(self, snapshot: MemorySnapshot):
        """从快照恢复记忆"""
        user_id = snapshot.user_id

        # 清空当前记忆
        self.redis.delete(f"memory:{user_id}:short_term")
        self.redis.delete(f"memory:{user_id}:medium_term")

        # 恢复短期记忆
        for memory in snapshot.short_term_memories:
            self._add_to_short_term(user_id, memory)

        # 恢复中期记忆
        self._update_medium_term_memories(user_id, snapshot.medium_term_memories)

        # 恢复长期记忆
        key = f"memory:{user_id}:long_term"
        self.redis.set(key, snapshot.long_term_summary)
```

---

## 5. 智能遗忘策略

### 5.1 SmartForgetStrategy（智能遗忘策略）

```python
# backend/app/services/agent/memory/memory_strategy.py

import math
from datetime import datetime
from typing import List

class SmartForgetStrategy:
    """智能遗忘策略"""

    def calculate_importance(
        self,
        memory: MemoryItem,
        current_time: datetime
    ) -> float:
        """
        计算记忆重要度

        公式：重要度 = 初始重要度 × 时间衰减 × 访问频率加权

        Args:
            memory: 记忆条目
            current_time: 当前时间

        Returns:
            float: 当前重要度
        """
        # 1. 时间衰减（指数衰减）
        time_delta = (current_time - memory.timestamp).total_seconds()
        time_decay = math.exp(-memory.decay_rate * time_delta / 3600)

        # 2. 访问频率加权
        access_weight = 1 + math.log(1 + memory.access_count)

        # 3. 综合重要度
        importance = memory.importance * time_decay * access_weight

        return importance

    def should_forget(
        self,
        memory: MemoryItem,
        threshold: float = 0.1
    ) -> bool:
        """
        判断是否应该遗忘

        Args:
            memory: 记忆条目
            threshold: 遗忘阈值

        Returns:
            bool: True表示应该遗忘
        """
        current_importance = self.calculate_importance(
            memory,
            datetime.now()
        )
        return current_importance < threshold

    def compress_to_summary(
        self,
        memories: List[MemoryItem]
    ) -> str:
        """
        将多条记忆压缩为摘要

        Args:
            memories: 记忆列表

        Returns:
            str: 摘要文本
        """
        if not memories:
            return ""

        # 简单实现：提取关键信息
        # 实际可以用 LLM 生成更好的摘要
        summaries = []
        for memory in memories:
            # 提取前50字作为摘要
            summary = memory.content[:50]
            if len(memory.content) > 50:
                summary += "..."
            summaries.append(f"- {summary}")

        return "\n".join(summaries)
```

---

## 6. 状态快照

### 6.1 快照创建流程

```
用户请求创建快照
   ↓
收集当前状态:
  ├─ 短期记忆（最近10条）
  ├─ 中期记忆（最近100条）
  └─ 长期记忆摘要
   ↓
生成快照ID
   ↓
序列化为JSON
   ↓
保存到Redis（TTL: 7天）
   ↓
返回快照ID
```

### 6.1 快照恢复流程

```
用户请求恢复快照
   ↓
根据快照ID从Redis读取
   ↓
反序列化JSON
   ↓
清空当前记忆
   ↓
恢复各层级记忆:
  ├─ 恢复短期记忆
  ├─ 恢复中期记忆
  └─ 恢复长期记忆
   ↓
返回快照对象
```

---

## 7. 存储设计

### 7.1 Redis 数据结构

```
# 短期记忆（List）
memory:{user_id}:short_term
  - [MemoryItem JSON, MemoryItem JSON, ...]
  - LPUSH 添加，LTRIM 限制大小
  - TTL: 3600秒（1小时）

# 中期记忆（Sorted Set）
memory:{user_id}:medium_term
  - {MemoryItem JSON: importance_score}
  - ZADD 添加，ZREVRANGE 读取
  - TTL: 86400秒（24小时）

# 长期记忆（String）
memory:{user_id}:long_term
  - "摘要文本..."
  - APPEND 追加
  - 永久保存

# 快照（String）
memory:snapshot:{snapshot_id}
  - MemorySnapshot JSON
  - TTL: 604800秒（7天）
```

### 7.2 PostgreSQL 数据表（可选）

```sql
-- 长期记忆持久化表
CREATE TABLE agent_long_term_memories (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    conversation_id VARCHAR(100),
    summary TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at)
);

-- 快照持久化表
CREATE TABLE agent_memory_snapshots (
    id SERIAL PRIMARY KEY,
    snapshot_id VARCHAR(50) UNIQUE NOT NULL,
    user_id INTEGER NOT NULL,
    conversation_id VARCHAR(100),
    snapshot_data JSONB NOT NULL,
    description TEXT,
    created_at TIMESTAMP NOT NULL,
    INDEX idx_snapshot_id (snapshot_id),
    INDEX idx_user_id (user_id)
);
```

---

## 8. 使用示例

### 8.1 基本使用

```python
import redis
from app.services.agent.memory import EnhancedMemoryManager

# 初始化
redis_client = redis.Redis(host='localhost', port=6379, db=1)
memory_manager = EnhancedMemoryManager(redis_client)

# 添加记忆
memory = memory_manager.add_memory(
    user_id="user_123",
    conversation_id="conv_456",
    role="user",
    content="我想写一部玄幻小说",
    importance=0.8
)

# 获取最近记忆
recent = memory_manager.get_recent_memories(
    user_id="user_123",
    limit=5
)

# 语义搜索
relevant = memory_manager.get_relevant_memories(
    user_id="user_123",
    query="玄幻小说",
    top_k=3
)

# 创建快照
snapshot_id = memory_manager.create_snapshot(
    user_id="user_123",
    conversation_id="conv_456",
    description="完成第一章创作后的状态"
)

# 恢复快照
snapshot = memory_manager.restore_snapshot(snapshot_id)
```

### 8.2 集成到Agent

```python
# 在 LangGraph Agent 中使用

class WritingAgentGraph:
    def __init__(self):
        self.memory_manager = EnhancedMemoryManager(redis_client)

    async def writing_node(self, state: AgentState):
        user_id = state["user_id"]

        # 1. 获取相关记忆作为上下文
        relevant_memories = self.memory_manager.get_relevant_memories(
            user_id=user_id,
            query=state["messages"][-1].content,
            top_k=5
        )

        # 2. 构建上下文
        context = "\n".join([m.content for m in relevant_memories])

        # 3. 生成内容
        response = await self.generate_content(context, state)

        # 4. 保存到记忆
        self.memory_manager.add_memory(
            user_id=user_id,
            conversation_id=state["conversation_id"],
            role="assistant",
            content=response,
            importance=0.7
        )

        return {"messages": [AIMessage(content=response)]}
```

---

## 9. 性能优化

### 9.1 优化策略

1. **Redis Pipeline**: 批量操作使用pipeline
2. **异步I/O**: 使用aioredis
3. **缓存**: 热数据本地缓存
4. **索引**: 中期记忆使用Sorted Set索引

### 9.2 性能目标

- ✅ 添加记忆: < 10ms
- ✅ 检索记忆: < 100ms
- ✅ 创建快照: < 200ms
- ✅ 恢复快照: < 200ms

---

## 10. 测试

### 10.1 单元测试

```python
# tests/agent/test_enhanced_memory.py

import pytest
from app.services.agent.memory import EnhancedMemoryManager

def test_add_memory(memory_manager):
    """测试添加记忆"""
    memory = memory_manager.add_memory(
        user_id="test_user",
        conversation_id="test_conv",
        role="user",
        content="测试内容"
    )
    assert memory.id is not None
    assert memory.content == "测试内容"

def test_get_recent_memories(memory_manager):
    """测试获取最近记忆"""
    # 添加多条记忆
    for i in range(15):
        memory_manager.add_memory(
            user_id="test_user",
            conversation_id="test_conv",
            role="user",
            content=f"内容{i}"
        )

    # 获取最近10条
    recent = memory_manager.get_recent_memories("test_user", limit=10)
    assert len(recent) == 10

def test_smart_forgetting(memory_manager):
    """测试智能遗忘"""
    # TODO: 实现测试
    pass

def test_create_and_restore_snapshot(memory_manager):
    """测试快照创建和恢复"""
    # 添加记忆
    memory_manager.add_memory(
        user_id="test_user",
        conversation_id="test_conv",
        role="user",
        content="快照测试"
    )

    # 创建快照
    snapshot_id = memory_manager.create_snapshot(
        user_id="test_user",
        conversation_id="test_conv"
    )
    assert snapshot_id is not None

    # 恢复快照
    snapshot = memory_manager.restore_snapshot(snapshot_id)
    assert len(snapshot.short_term_memories) > 0
```

---

**文档完成** ✅
