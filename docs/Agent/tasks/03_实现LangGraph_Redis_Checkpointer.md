# 实现LangGraph Redis Checkpointer

## 目标

创建一个自定义的Redis Checkpointer，替代LangGraph默认的MemorySaver，实现会话状态的持久化。

## 技术背景

### LangGraph Checkpointer接口

LangGraph的Checkpointer需要实现以下核心方法：

```python
from langgraph.checkpoint.base import BaseCheckpointer

class BaseCheckpointer:
    def get(self, config: RunnableConfig) -> Optional[Checkpoint]:
        """获取指定的checkpoint"""
        pass

    def put(self, config: RunnableConfig, checkpoint: Checkpoint) -> RunnableConfig:
        """保存checkpoint"""
        pass

    def list(self, config: RunnableConfig) -> Iterator[Checkpoint]:
        """列出所有checkpoint"""
        pass
```

## 实现步骤

### 步骤1：创建RedisCheckpointer类文件

**文件路径**：`ai_writer/backend/app/services/agent/memory/redis_checkpointer.py`

**完整代码实现**：

```python
"""
Redis Checkpointer for LangGraph

实现LangGraph的持久化Checkpointer，使用Redis存储会话状态。
"""

from typing import Optional, Iterator, Any, Dict
from datetime import datetime, timedelta
import json
import logging
import redis
from langgraph.checkpoint.base import BaseCheckpointer, Checkpoint
from langchain_core.runnables import RunnableConfig

logger = logging.getLogger(__name__)


class RedisCheckpointer(BaseCheckpointer):
    """
    基于Redis的LangGraph Checkpointer

    功能：
    - 持久化会话状态到Redis
    - 支持跨会话恢复
    - 自动过期清理（默认7天）
    """

    def __init__(
        self,
        redis_client: redis.Redis,
        key_prefix: str = "langgraph:checkpoint",
        ttl: int = 7 * 24 * 3600  # 7天
    ):
        """
        初始化Redis Checkpointer

        Args:
            redis_client: Redis客户端实例
            key_prefix: Redis键前缀
            ttl: 过期时间（秒），默认7天
        """
        self.redis = redis_client
        self.key_prefix = key_prefix
        self.ttl = ttl
        logger.info(f"[RedisCheckpointer] 初始化完成，TTL={ttl}秒")

    def _make_key(self, thread_id: str, checkpoint_id: str = "latest") -> str:
        """生成Redis键"""
        return f"{self.key_prefix}:{thread_id}:{checkpoint_id}"

    def _make_list_key(self, thread_id: str) -> str:
        """生成checkpoint列表键"""
        return f"{self.key_prefix}:list:{thread_id}"

    def get(self, config: RunnableConfig) -> Optional[Checkpoint]:
        """
        获取checkpoint

        Args:
            config: 运行配置，包含thread_id

        Returns:
            Checkpoint对象或None
        """
        try:
            thread_id = config.get("configurable", {}).get("thread_id")
            if not thread_id:
                logger.warning("[RedisCheckpointer] 缺少thread_id")
                return None

            key = self._make_key(thread_id)
            data = self.redis.get(key)

            if not data:
                logger.info(f"[RedisCheckpointer] 未找到checkpoint: {thread_id}")
                return None

            checkpoint_data = json.loads(data)
            logger.info(f"[RedisCheckpointer] 加载checkpoint: {thread_id}")

            # 转换为Checkpoint对象
            checkpoint = Checkpoint(
                v=checkpoint_data.get("v", 1),
                id=checkpoint_data.get("id"),
                ts=checkpoint_data.get("ts"),
                channel_values=checkpoint_data.get("channel_values", {}),
                channel_versions=checkpoint_data.get("channel_versions", {}),
                versions_seen=checkpoint_data.get("versions_seen", {})
            )

            return checkpoint

        except Exception as e:
            logger.error(f"[RedisCheckpointer] 加载失败: {e}", exc_info=True)
            return None

    def put(
        self,
        config: RunnableConfig,
        checkpoint: Checkpoint,
        metadata: Optional[Dict[str, Any]] = None
    ) -> RunnableConfig:
        """
        保存checkpoint

        Args:
            config: 运行配置
            checkpoint: 要保存的checkpoint
            metadata: 元数据（可选）

        Returns:
            更新后的配置
        """
        try:
            thread_id = config.get("configurable", {}).get("thread_id")
            if not thread_id:
                logger.warning("[RedisCheckpointer] 缺少thread_id，无法保存")
                return config

            # 序列化checkpoint
            checkpoint_data = {
                "v": checkpoint.v,
                "id": checkpoint.id,
                "ts": checkpoint.ts,
                "channel_values": checkpoint.channel_values,
                "channel_versions": checkpoint.channel_versions,
                "versions_seen": checkpoint.versions_seen,
                "metadata": metadata or {},
                "saved_at": datetime.now().isoformat()
            }

            # 保存到Redis
            key = self._make_key(thread_id)
            self.redis.setex(
                key,
                self.ttl,
                json.dumps(checkpoint_data, ensure_ascii=False)
            )

            # 添加到列表（用于list操作）
            list_key = self._make_list_key(thread_id)
            self.redis.lpush(list_key, checkpoint.id)
            self.redis.ltrim(list_key, 0, 99)  # 保留最近100个
            self.redis.expire(list_key, self.ttl)

            logger.info(f"[RedisCheckpointer] 保存成功: {thread_id}, checkpoint_id={checkpoint.id}")

            return config

        except Exception as e:
            logger.error(f"[RedisCheckpointer] 保存失败: {e}", exc_info=True)
            return config

    def list(
        self,
        config: RunnableConfig,
        limit: int = 10,
        before: Optional[str] = None
    ) -> Iterator[Checkpoint]:
        """
        列出checkpoint历史

        Args:
            config: 运行配置
            limit: 返回数量限制
            before: 在此之前的checkpoint（可选）

        Yields:
            Checkpoint对象迭代器
        """
        try:
            thread_id = config.get("configurable", {}).get("thread_id")
            if not thread_id:
                return

            list_key = self._make_list_key(thread_id)
            checkpoint_ids = self.redis.lrange(list_key, 0, limit - 1)

            for checkpoint_id in checkpoint_ids:
                checkpoint_id = checkpoint_id.decode('utf-8')

                # 跳过before之后的
                if before and checkpoint_id >= before:
                    continue

                # 尝试加载checkpoint
                key = self._make_key(thread_id, checkpoint_id)
                data = self.redis.get(key)

                if data:
                    checkpoint_data = json.loads(data)
                    yield Checkpoint(
                        v=checkpoint_data.get("v", 1),
                        id=checkpoint_data.get("id"),
                        ts=checkpoint_data.get("ts"),
                        channel_values=checkpoint_data.get("channel_values", {}),
                        channel_versions=checkpoint_data.get("channel_versions", {}),
                        versions_seen=checkpoint_data.get("versions_seen", {})
                    )

        except Exception as e:
            logger.error(f"[RedisCheckpointer] 列表查询失败: {e}", exc_info=True)

    def delete(self, thread_id: str):
        """
        删除指定会话的所有checkpoint

        Args:
            thread_id: 会话ID
        """
        try:
            # 删除主checkpoint
            key = self._make_key(thread_id)
            self.redis.delete(key)

            # 删除列表
            list_key = self._make_list_key(thread_id)
            self.redis.delete(list_key)

            logger.info(f"[RedisCheckpointer] 删除成功: {thread_id}")

        except Exception as e:
            logger.error(f"[RedisCheckpointer] 删除失败: {e}", exc_info=True)

    def get_stats(self, thread_id: str) -> Dict[str, Any]:
        """
        获取checkpoint统计信息

        Args:
            thread_id: 会话ID

        Returns:
            统计信息字典
        """
        try:
            key = self._make_key(thread_id)
            list_key = self._make_list_key(thread_id)

            exists = self.redis.exists(key)
            count = self.redis.llen(list_key)
            ttl = self.redis.ttl(key)

            return {
                "thread_id": thread_id,
                "exists": bool(exists),
                "checkpoint_count": count,
                "ttl_seconds": ttl,
                "expires_at": (datetime.now() + timedelta(seconds=ttl)).isoformat() if ttl > 0 else None
            }

        except Exception as e:
            logger.error(f"[RedisCheckpointer] 统计查询失败: {e}", exc_info=True)
            return {}
```

### 步骤2：在__init__.py中导出

**文件路径**：`ai_writer/backend/app/services/agent/memory/__init__.py`

**添加导出**：

```python
from .redis_checkpointer import RedisCheckpointer

__all__ = [
    "MemoryManager",
    "LongTermMemoryService",
    "UserProfileMemory",
    "RedisCheckpointer",  # 新增
]
```

### 步骤3：修改langgraph_agent.py

**文件路径**：`ai_writer/backend/app/services/agent/langgraph_agent.py`

**修改点1：导入RedisCheckpointer**

```python
# 文件顶部添加导入
from app.services.agent.memory import RedisCheckpointer
```

**修改点2：修改__init__方法**

```python
# 修改前（约第494-518行）
def __init__(self, ai_service: HTTPAIService, use_chatgpt: bool = False):
    self.ai_service = ai_service
    self.use_chatgpt = use_chatgpt
    set_global_ai_service(ai_service)

    if use_chatgpt:
        logger.info("[LangGraph] 使用 ChatOpenAI 模式")
        self._init_chatgpt_mode()
    else:
        logger.info("[LangGraph] 使用 HTTPAIService 模式")
        self.llm = None
        self.llm_with_tools = None

    # ❌ 旧代码
    self.checkpointer = MemorySaver()

    self.graph = self._build_graph()

# 修改后
def __init__(
    self,
    ai_service: HTTPAIService,
    redis_client: redis.Redis,  # 新增参数
    use_chatgpt: bool = False
):
    self.ai_service = ai_service
    self.redis_client = redis_client  # 保存redis客户端
    self.use_chatgpt = use_chatgpt
    set_global_ai_service(ai_service)

    if use_chatgpt:
        logger.info("[LangGraph] 使用 ChatOpenAI 模式")
        self._init_chatgpt_mode()
    else:
        logger.info("[LangGraph] 使用 HTTPAIService 模式")
        self.llm = None
        self.llm_with_tools = None

    # ✅ 新代码：使用Redis Checkpointer
    self.checkpointer = RedisCheckpointer(
        redis_client=redis_client,
        key_prefix="langgraph:agent:checkpoint",
        ttl=7 * 24 * 3600  # 7天过期
    )
    logger.info("[LangGraph] 使用 RedisCheckpointer 进行状态持久化")

    self.graph = self._build_graph()
```

### 步骤4：修改API路由传递Redis客户端

**文件路径**：`ai_writer/backend/app/api/v1/agent.py`

**修改chat接口（约第167行）**：

```python
# 修改前
agent_graph = WritingAgentGraph(ai_service, use_chatgpt=settings.AGENT_USE_CHATGPT)

# 修改后
redis_client = get_redis_client()  # 获取Redis客户端
agent_graph = WritingAgentGraph(
    ai_service,
    redis_client=redis_client,
    use_chatgpt=settings.AGENT_USE_CHATGPT
)
```

**修改chat_stream接口（约第268行）**：

```python
# 修改前
agent_graph = WritingAgentGraph(ai_service, use_chatgpt=settings.AGENT_USE_CHATGPT)

# 修改后
redis_client = get_redis_client()
agent_graph = WritingAgentGraph(
    ai_service,
    redis_client=redis_client,
    use_chatgpt=settings.AGENT_USE_CHATGPT
)
```

## 测试验证

### 单元测试

创建测试文件：`ai_writer/backend/tests/test_redis_checkpointer.py`

```python
import pytest
import redis
from app.services.agent.memory import RedisCheckpointer
from langgraph.checkpoint.base import Checkpoint

@pytest.fixture
def redis_client():
    """测试用Redis客户端"""
    client = redis.Redis(host='localhost', port=6379, db=15, decode_responses=False)
    yield client
    # 清理
    client.flushdb()

def test_put_and_get_checkpoint(redis_client):
    """测试保存和获取checkpoint"""
    checkpointer = RedisCheckpointer(redis_client, ttl=60)

    config = {"configurable": {"thread_id": "test-thread-1"}}
    checkpoint = Checkpoint(
        v=1,
        id="checkpoint-1",
        ts="2025-11-04T14:00:00",
        channel_values={"messages": []},
        channel_versions={},
        versions_seen={}
    )

    # 保存
    checkpointer.put(config, checkpoint)

    # 获取
    loaded = checkpointer.get(config)
    assert loaded is not None
    assert loaded.id == "checkpoint-1"

def test_checkpoint_ttl(redis_client):
    """测试TTL过期"""
    checkpointer = RedisCheckpointer(redis_client, ttl=1)  # 1秒过期

    config = {"configurable": {"thread_id": "test-thread-2"}}
    checkpoint = Checkpoint(v=1, id="cp-2", ts="2025-11-04", channel_values={})

    checkpointer.put(config, checkpoint)

    # 立即获取应该成功
    assert checkpointer.get(config) is not None

    # 等待过期
    import time
    time.sleep(2)

    # 过期后应该返回None
    assert checkpointer.get(config) is None
```

### 集成测试

```python
# 测试与LangGraph的集成
def test_langgraph_with_redis_checkpointer():
    """测试LangGraph使用Redis Checkpointer"""
    redis_client = redis.Redis(host='localhost', port=6379, db=15)
    ai_service = HTTPAIService()

    # 创建Agent
    agent = WritingAgentGraph(
        ai_service=ai_service,
        redis_client=redis_client,
        use_chatgpt=False
    )

    # 第一次对话
    result1 = await agent.chat(
        message="帮我写第一章",
        work_id="test-work",
        conversation_id="test-conv-1"
    )

    assert result1["response"] is not None

    # 第二次对话，应该能恢复上下文
    result2 = await agent.chat(
        message="继续写",
        work_id="test-work",
        conversation_id="test-conv-1"  # 相同的conversation_id
    )

    assert result2["response"] is not None
    # Agent应该能够记住之前的对话
```

## 常见问题

### Q1: Redis连接失败怎么办？

**A**: 实现降级机制：

```python
try:
    self.checkpointer = RedisCheckpointer(redis_client)
except Exception as e:
    logger.error(f"Redis Checkpointer初始化失败，降级为MemorySaver: {e}")
    self.checkpointer = MemorySaver()
```

### Q2: 如何清理过期的checkpoint？

**A**: Redis的TTL会自动清理，也可以手动清理：

```python
# 清理特定会话
checkpointer.delete(thread_id="old-conversation-id")

# 批量清理（可以写一个定时任务）
pattern = "langgraph:agent:checkpoint:*"
for key in redis_client.scan_iter(match=pattern):
    ttl = redis_client.ttl(key)
    if ttl < 0:  # 没有过期时间
        redis_client.expire(key, 7 * 24 * 3600)
```

### Q3: 性能影响如何？

**A**:
- Redis操作非常快（< 1ms）
- 异步保存不影响响应速度
- 建议监控Redis内存使用

## 下一步

完成实现后，继续查看：
- `04_优化现有记忆管理.md` - 优化MemoryManager集成
- `05_集成测试计划.md` - 完整的测试计划
