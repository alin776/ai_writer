"""
记忆版本控制系统 (P2-3修复)

实现记忆的版本管理和回滚功能：
1. 自动创建版本快照（重要操作前）
2. 手动创建版本快照
3. 版本列表查看
4. 回滚到指定版本
5. 版本对比

核心功能：
- MemoryVersionControl: 版本控制管理器
- VersionSnapshot: 版本快照数据结构
- 支持短期、中期、长期记忆的完整备份和恢复

使用示例：
```python
vc = MemoryVersionControl(redis_client)

# 创建版本
version_id = await vc.create_version(
    user_id="user_123",
    description="完成第一章创作"
)

# 列出版本
versions = await vc.list_versions(user_id="user_123")

# 回滚
await vc.rollback_to_version(user_id="user_123", version_id=version_id)

# 对比
diff = await vc.compare_versions(user_id, version_id_1, version_id_2)
```
"""

import json
import uuid
import gzip
import logging
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field, asdict
from redis import Redis
from enum import Enum

logger = logging.getLogger(__name__)


class VersionType(Enum):
    """版本类型"""
    AUTO = "auto"              # 自动创建（系统触发）
    MANUAL = "manual"          # 手动创建（用户触发）
    BEFORE_DELETE = "before_delete"  # 删除前备份
    BEFORE_FORGET = "before_forget"  # 遗忘前备份
    CHECKPOINT = "checkpoint"  # 检查点


@dataclass
class VersionSnapshot:
    """
    版本快照数据结构

    包含某一时刻所有记忆的完整状态
    """
    version_id: str
    user_id: str
    created_at: datetime
    version_type: VersionType
    description: str

    # 记忆数据
    short_term_memories: List[Dict[str, Any]]
    medium_term_memories: List[Dict[str, Any]]
    long_term_summary: str

    # 元数据
    total_memories: int
    total_tokens: int
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_json(self) -> str:
        """序列化为JSON"""
        data = {
            "version_id": self.version_id,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat(),
            "version_type": self.version_type.value,
            "description": self.description,
            "short_term_memories": self.short_term_memories,
            "medium_term_memories": self.medium_term_memories,
            "long_term_summary": self.long_term_summary,
            "total_memories": self.total_memories,
            "total_tokens": self.total_tokens,
            "metadata": self.metadata
        }
        return json.dumps(data, ensure_ascii=False)

    @classmethod
    def from_json(cls, json_str: str) -> 'VersionSnapshot':
        """从JSON反序列化"""
        data = json.loads(json_str)
        return cls(
            version_id=data["version_id"],
            user_id=data["user_id"],
            created_at=datetime.fromisoformat(data["created_at"]),
            version_type=VersionType(data["version_type"]),
            description=data["description"],
            short_term_memories=data["short_term_memories"],
            medium_term_memories=data["medium_term_memories"],
            long_term_summary=data["long_term_summary"],
            total_memories=data["total_memories"],
            total_tokens=data["total_tokens"],
            metadata=data.get("metadata", {})
        )


@dataclass
class VersionDiff:
    """
    版本差异

    两个版本之间的差异对比
    """
    version_from: str
    version_to: str

    # 差异统计
    added_count: int
    removed_count: int
    modified_count: int

    # 详细差异
    added_memories: List[Dict[str, Any]]
    removed_memories: List[Dict[str, Any]]
    modified_memories: List[Dict[str, Any]]

    # 长期记忆差异
    long_term_changed: bool
    long_term_diff: Optional[str]


class MemoryVersionControl:
    """
    记忆版本控制管理器

    提供完整的版本管理功能：
    - 创建版本快照
    - 列出历史版本
    - 回滚到指定版本
    - 版本对比
    - 自动清理过期版本
    """

    # 配置常量
    VERSION_TTL = 86400 * 30      # 版本保留时间（30天）
    MAX_VERSIONS = 50             # 每用户最大版本数
    COMPRESS_THRESHOLD = 10000    # 压缩阈值（字符数）

    def __init__(
        self,
        redis_client: Redis,
        version_ttl: int = VERSION_TTL,
        max_versions: int = MAX_VERSIONS
    ):
        """
        初始化版本控制器

        Args:
            redis_client: Redis客户端
            version_ttl: 版本保留时间（秒）
            max_versions: 每用户最大版本数
        """
        self.redis = redis_client
        self.version_ttl = version_ttl
        self.max_versions = max_versions

        logger.info(
            f"[VersionControl] Initialized: "
            f"ttl={version_ttl}s, max_versions={max_versions}"
        )

    def _generate_version_id(self) -> str:
        """生成版本ID"""
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        unique = uuid.uuid4().hex[:8]
        return f"v_{timestamp}_{unique}"

    def _get_version_key(self, user_id: str, version_id: str) -> str:
        """获取版本存储的Redis key"""
        return f"memory:version:{user_id}:{version_id}"

    def _get_version_index_key(self, user_id: str) -> str:
        """获取版本索引的Redis key"""
        return f"memory:version_index:{user_id}"

    async def create_version(
        self,
        user_id: str,
        version_type: VersionType = VersionType.MANUAL,
        description: str = "",
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        创建版本快照

        Args:
            user_id: 用户ID
            version_type: 版本类型
            description: 版本描述
            metadata: 额外元数据

        Returns:
            版本ID
        """
        version_id = self._generate_version_id()

        try:
            # 1. 获取当前所有记忆
            short_term = await self._get_short_term_memories(user_id)
            medium_term = await self._get_medium_term_memories(user_id)
            long_term = await self._get_long_term_summary(user_id)

            # 2. 计算统计
            total_memories = len(short_term) + len(medium_term)
            total_tokens = self._estimate_tokens(short_term, medium_term, long_term)

            # 3. 创建快照
            snapshot = VersionSnapshot(
                version_id=version_id,
                user_id=user_id,
                created_at=datetime.now(timezone.utc),
                version_type=version_type,
                description=description or f"Version created at {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                short_term_memories=short_term,
                medium_term_memories=medium_term,
                long_term_summary=long_term,
                total_memories=total_memories,
                total_tokens=total_tokens,
                metadata=metadata or {}
            )

            # 4. 序列化并压缩
            json_data = snapshot.to_json()
            if len(json_data) > self.COMPRESS_THRESHOLD:
                # 使用gzip压缩
                compressed = gzip.compress(json_data.encode('utf-8'))
                data_to_store = compressed
                is_compressed = True
            else:
                data_to_store = json_data.encode('utf-8')
                is_compressed = False

            # 5. 保存到Redis
            version_key = self._get_version_key(user_id, version_id)
            self.redis.set(version_key, data_to_store, ex=self.version_ttl)

            # 6. 更新版本索引
            index_key = self._get_version_index_key(user_id)
            index_entry = json.dumps({
                "version_id": version_id,
                "created_at": snapshot.created_at.isoformat(),
                "version_type": version_type.value,
                "description": description,
                "total_memories": total_memories,
                "is_compressed": is_compressed
            }, ensure_ascii=False)
            self.redis.lpush(index_key, index_entry)
            self.redis.expire(index_key, self.version_ttl)

            # 7. 清理过期版本
            await self._cleanup_old_versions(user_id)

            logger.info(
                f"[VersionControl] Created version: "
                f"user={user_id}, version={version_id}, "
                f"type={version_type.value}, memories={total_memories}"
            )

            return version_id

        except Exception as e:
            logger.error(f"[VersionControl] Failed to create version: {e}")
            raise

    async def list_versions(
        self,
        user_id: str,
        limit: int = 20,
        version_type: Optional[VersionType] = None
    ) -> List[Dict[str, Any]]:
        """
        列出用户的版本历史

        Args:
            user_id: 用户ID
            limit: 最大返回数量
            version_type: 过滤版本类型

        Returns:
            版本列表（按时间倒序）
        """
        index_key = self._get_version_index_key(user_id)

        try:
            # 获取索引列表
            entries = self.redis.lrange(index_key, 0, limit * 2)  # 获取更多以便过滤

            versions = []
            for entry in entries:
                if isinstance(entry, bytes):
                    entry = entry.decode('utf-8')

                version_info = json.loads(entry)

                # 类型过滤
                if version_type and version_info.get("version_type") != version_type.value:
                    continue

                versions.append(version_info)

                if len(versions) >= limit:
                    break

            return versions

        except Exception as e:
            logger.error(f"[VersionControl] Failed to list versions: {e}")
            return []

    async def get_version(
        self,
        user_id: str,
        version_id: str
    ) -> Optional[VersionSnapshot]:
        """
        获取指定版本的完整快照

        Args:
            user_id: 用户ID
            version_id: 版本ID

        Returns:
            版本快照，如果不存在返回None
        """
        version_key = self._get_version_key(user_id, version_id)

        try:
            data = self.redis.get(version_key)

            if not data:
                logger.warning(f"[VersionControl] Version not found: {version_id}")
                return None

            # 尝试解压缩
            try:
                json_str = gzip.decompress(data).decode('utf-8')
            except gzip.BadGzipFile:
                # 非压缩数据
                json_str = data.decode('utf-8') if isinstance(data, bytes) else data

            return VersionSnapshot.from_json(json_str)

        except Exception as e:
            logger.error(f"[VersionControl] Failed to get version: {e}")
            return None

    async def rollback_to_version(
        self,
        user_id: str,
        version_id: str,
        create_backup: bool = True
    ) -> bool:
        """
        回滚到指定版本

        Args:
            user_id: 用户ID
            version_id: 目标版本ID
            create_backup: 是否在回滚前创建当前状态的备份

        Returns:
            是否回滚成功
        """
        try:
            # 1. 获取目标版本
            snapshot = await self.get_version(user_id, version_id)
            if not snapshot:
                logger.error(f"[VersionControl] Rollback failed: version {version_id} not found")
                return False

            # 2. 创建当前状态的备份
            if create_backup:
                await self.create_version(
                    user_id=user_id,
                    version_type=VersionType.BEFORE_DELETE,
                    description=f"Backup before rollback to {version_id}"
                )

            # 3. 清空当前记忆
            await self._clear_all_memories(user_id)

            # 4. 恢复短期记忆
            short_key = f"memory:{user_id}:short_term"
            for memory in reversed(snapshot.short_term_memories):
                self.redis.rpush(short_key, json.dumps(memory, ensure_ascii=False))
            self.redis.expire(short_key, 86400)  # 24小时

            # 5. 恢复中期记忆
            medium_key = f"memory:{user_id}:medium_term"
            for memory in snapshot.medium_term_memories:
                importance = memory.get("importance", 0.5)
                self.redis.zadd(
                    medium_key,
                    {json.dumps(memory, ensure_ascii=False): importance}
                )
            self.redis.expire(medium_key, 86400 * 3)  # 3天

            # 6. 恢复长期记忆
            if snapshot.long_term_summary:
                long_key = f"memory:{user_id}:long_term"
                self.redis.set(long_key, snapshot.long_term_summary)

            logger.info(
                f"[VersionControl] Rollback successful: "
                f"user={user_id}, version={version_id}, "
                f"restored_memories={snapshot.total_memories}"
            )

            return True

        except Exception as e:
            logger.error(f"[VersionControl] Rollback failed: {e}")
            return False

    async def compare_versions(
        self,
        user_id: str,
        version_id_from: str,
        version_id_to: str
    ) -> Optional[VersionDiff]:
        """
        对比两个版本的差异

        Args:
            user_id: 用户ID
            version_id_from: 源版本ID
            version_id_to: 目标版本ID

        Returns:
            版本差异
        """
        try:
            # 获取两个版本
            version_from = await self.get_version(user_id, version_id_from)
            version_to = await self.get_version(user_id, version_id_to)

            if not version_from or not version_to:
                logger.error("[VersionControl] Compare failed: version not found")
                return None

            # 计算记忆差异
            from_ids = {m.get("id") for m in version_from.short_term_memories + version_from.medium_term_memories}
            to_ids = {m.get("id") for m in version_to.short_term_memories + version_to.medium_term_memories}

            added_ids = to_ids - from_ids
            removed_ids = from_ids - to_ids
            common_ids = from_ids & to_ids

            # 获取具体的记忆
            from_memories = {
                m.get("id"): m
                for m in version_from.short_term_memories + version_from.medium_term_memories
            }
            to_memories = {
                m.get("id"): m
                for m in version_to.short_term_memories + version_to.medium_term_memories
            }

            added_memories = [to_memories[mid] for mid in added_ids if mid in to_memories]
            removed_memories = [from_memories[mid] for mid in removed_ids if mid in from_memories]

            # 检查内容变化的记忆
            modified_memories = []
            for mid in common_ids:
                if mid in from_memories and mid in to_memories:
                    if from_memories[mid].get("content") != to_memories[mid].get("content"):
                        modified_memories.append({
                            "id": mid,
                            "from": from_memories[mid],
                            "to": to_memories[mid]
                        })

            # 长期记忆对比
            long_term_changed = version_from.long_term_summary != version_to.long_term_summary
            long_term_diff = None
            if long_term_changed:
                # 简单diff：显示长度变化
                from_len = len(version_from.long_term_summary)
                to_len = len(version_to.long_term_summary)
                long_term_diff = f"Long-term summary: {from_len} -> {to_len} chars"

            return VersionDiff(
                version_from=version_id_from,
                version_to=version_id_to,
                added_count=len(added_memories),
                removed_count=len(removed_memories),
                modified_count=len(modified_memories),
                added_memories=added_memories,
                removed_memories=removed_memories,
                modified_memories=modified_memories,
                long_term_changed=long_term_changed,
                long_term_diff=long_term_diff
            )

        except Exception as e:
            logger.error(f"[VersionControl] Compare failed: {e}")
            return None

    async def delete_version(
        self,
        user_id: str,
        version_id: str
    ) -> bool:
        """
        删除指定版本

        Args:
            user_id: 用户ID
            version_id: 版本ID

        Returns:
            是否删除成功
        """
        try:
            # 删除版本数据
            version_key = self._get_version_key(user_id, version_id)
            self.redis.delete(version_key)

            # 从索引中移除
            index_key = self._get_version_index_key(user_id)
            entries = self.redis.lrange(index_key, 0, -1)

            for i, entry in enumerate(entries):
                if isinstance(entry, bytes):
                    entry = entry.decode('utf-8')

                version_info = json.loads(entry)
                if version_info.get("version_id") == version_id:
                    self.redis.lrem(index_key, 1, entry)
                    break

            logger.info(f"[VersionControl] Deleted version: {version_id}")
            return True

        except Exception as e:
            logger.error(f"[VersionControl] Delete failed: {e}")
            return False

    async def _cleanup_old_versions(self, user_id: str):
        """清理过期版本（保留最新的max_versions个）"""
        index_key = self._get_version_index_key(user_id)

        try:
            # 获取版本总数
            total = self.redis.llen(index_key)

            if total > self.max_versions:
                # 获取要删除的版本
                to_delete = self.redis.lrange(index_key, self.max_versions, -1)

                for entry in to_delete:
                    if isinstance(entry, bytes):
                        entry = entry.decode('utf-8')

                    version_info = json.loads(entry)
                    version_id = version_info.get("version_id")

                    # 删除版本数据
                    version_key = self._get_version_key(user_id, version_id)
                    self.redis.delete(version_key)

                # 修剪索引
                self.redis.ltrim(index_key, 0, self.max_versions - 1)

                logger.info(
                    f"[VersionControl] Cleaned up {total - self.max_versions} old versions "
                    f"for user {user_id}"
                )

        except Exception as e:
            logger.error(f"[VersionControl] Cleanup failed: {e}")

    async def _get_short_term_memories(self, user_id: str) -> List[Dict[str, Any]]:
        """获取短期记忆"""
        key = f"memory:{user_id}:short_term"
        memories = self.redis.lrange(key, 0, -1)

        result = []
        for m in memories:
            if isinstance(m, bytes):
                m = m.decode('utf-8')
            try:
                result.append(json.loads(m))
            except:
                pass

        return result

    async def _get_medium_term_memories(self, user_id: str) -> List[Dict[str, Any]]:
        """获取中期记忆"""
        key = f"memory:{user_id}:medium_term"
        memories = self.redis.zrange(key, 0, -1, withscores=True)

        result = []
        for m, score in memories:
            if isinstance(m, bytes):
                m = m.decode('utf-8')
            try:
                memory = json.loads(m)
                memory["importance"] = score
                result.append(memory)
            except:
                pass

        return result

    async def _get_long_term_summary(self, user_id: str) -> str:
        """获取长期记忆摘要"""
        key = f"memory:{user_id}:long_term"
        summary = self.redis.get(key)

        if not summary:
            return ""

        return summary.decode('utf-8') if isinstance(summary, bytes) else summary

    async def _clear_all_memories(self, user_id: str):
        """清空所有记忆"""
        keys = [
            f"memory:{user_id}:short_term",
            f"memory:{user_id}:medium_term",
            f"memory:{user_id}:long_term"
        ]
        self.redis.delete(*keys)

    def _estimate_tokens(
        self,
        short_term: List[Dict],
        medium_term: List[Dict],
        long_term: str
    ) -> int:
        """估算总Token数"""
        total_chars = 0

        for m in short_term:
            total_chars += len(m.get("content", ""))

        for m in medium_term:
            total_chars += len(m.get("content", ""))

        total_chars += len(long_term)

        # 粗略估算：中文1字≈1.5 tokens，英文4字≈1 token
        return int(total_chars * 0.5)


# 全局单例
_default_version_control: Optional[MemoryVersionControl] = None


def get_version_control(redis_client: Redis) -> MemoryVersionControl:
    """
    获取全局默认的版本控制器实例

    Args:
        redis_client: Redis客户端

    Returns:
        MemoryVersionControl实例
    """
    global _default_version_control
    if _default_version_control is None:
        _default_version_control = MemoryVersionControl(redis_client)
    return _default_version_control
