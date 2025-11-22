"""
长期记忆持久化存储 (P1-6修复)

提供长期记忆的持久化、备份和压缩功能，解决以下问题：
1. Redis故障时的数据丢失风险
2. 长期记忆无限增长的问题
3. 缺少二次压缩的问题

核心功能：
- 磁盘备份：定期将长期记忆备份到磁盘
- 二次压缩：当长期记忆超过阈值时，进行智能压缩
- 故障恢复：从磁盘恢复长期记忆
- 版本管理：保留历史备份版本
"""

import json
import os
import gzip
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Dict, List, Any
from dataclasses import dataclass, asdict
import logging

logger = logging.getLogger(__name__)


@dataclass
class BackupMetadata:
    """备份元数据"""
    user_id: str
    backup_time: datetime
    version: int
    size_bytes: int
    compressed: bool
    checksum: str  # MD5校验和


class LongTermMemoryStore:
    """
    长期记忆持久化存储器

    提供长期记忆的磁盘备份、压缩和恢复功能

    架构：
    - 数据目录: ./data/long_term_memory/
    - 用户目录: ./data/long_term_memory/{user_id}/
    - 当前版本: {user_id}/current.json (或 current.json.gz)
    - 历史版本: {user_id}/backup_v{version}_{timestamp}.json.gz
    - 元数据: {user_id}/metadata.json

    使用示例：
    ```python
    store = LongTermMemoryStore()

    # 保存长期记忆
    await store.save(user_id="user_123", content="长期记忆内容...")

    # 加载长期记忆
    content = await store.load(user_id="user_123")

    # 二次压缩（当内容过大时）
    compressed = await store.compress(user_id="user_123")
    ```
    """

    def __init__(
        self,
        base_dir: str = "./data/long_term_memory",
        max_size_kb: int = 50,  # 触发二次压缩的阈值（KB）
        compression_enabled: bool = True,
        keep_versions: int = 5,  # 保留的历史版本数
        auto_backup_interval: int = 3600  # 自动备份间隔（秒）
    ):
        """
        初始化长期记忆存储器

        Args:
            base_dir: 基础数据目录
            max_size_kb: 触发二次压缩的阈值（KB）
            compression_enabled: 是否启用压缩
            keep_versions: 保留的历史版本数
            auto_backup_interval: 自动备份间隔（秒）
        """
        self.base_dir = Path(base_dir)
        self.max_size_kb = max_size_kb
        self.compression_enabled = compression_enabled
        self.keep_versions = keep_versions
        self.auto_backup_interval = auto_backup_interval

        # 确保目录存在
        self.base_dir.mkdir(parents=True, exist_ok=True)

        # 上次备份时间跟踪（用于自动备份）
        self._last_backup: Dict[str, datetime] = {}

        logger.info(
            f"[LongTermStore] Initialized: base_dir={base_dir}, "
            f"max_size={max_size_kb}KB, compression={compression_enabled}"
        )

    def _get_user_dir(self, user_id: str) -> Path:
        """获取用户专属目录"""
        user_dir = self.base_dir / user_id
        user_dir.mkdir(parents=True, exist_ok=True)
        return user_dir

    def _calculate_checksum(self, content: str) -> str:
        """计算内容的MD5校验和"""
        import hashlib
        return hashlib.md5(content.encode('utf-8')).hexdigest()

    def _should_auto_backup(self, user_id: str) -> bool:
        """判断是否需要自动备份"""
        if user_id not in self._last_backup:
            return True

        elapsed = (datetime.now(timezone.utc) - self._last_backup[user_id]).total_seconds()
        return elapsed >= self.auto_backup_interval

    async def save(
        self,
        user_id: str,
        content: str,
        auto_compress: bool = True,
        create_backup: bool = True
    ) -> Dict[str, Any]:
        """
        保存长期记忆到磁盘

        Args:
            user_id: 用户ID
            content: 长期记忆内容
            auto_compress: 是否自动压缩（如果超过阈值）
            create_backup: 是否创建历史备份

        Returns:
            保存结果：包含文件大小、是否压缩等信息
        """
        user_dir = self._get_user_dir(user_id)

        # 检查是否需要二次压缩
        content_size_kb = len(content.encode('utf-8')) / 1024
        needs_compression = auto_compress and content_size_kb > self.max_size_kb

        if needs_compression:
            logger.info(
                f"[LongTermStore] Content size {content_size_kb:.2f}KB exceeds "
                f"threshold {self.max_size_kb}KB, triggering secondary compression"
            )
            content = await self._secondary_compress(content)
            content_size_kb = len(content.encode('utf-8')) / 1024

        # 创建历史备份（如果需要）
        backup_version = 0
        if create_backup and self._should_auto_backup(user_id):
            backup_version = await self._create_backup_version(user_id, content)

        # 保存当前版本
        current_file = user_dir / "current.json"
        compressed_file = user_dir / "current.json.gz"

        if self.compression_enabled:
            # 使用gzip压缩保存
            with gzip.open(compressed_file, 'wt', encoding='utf-8') as f:
                json.dump({
                    "user_id": user_id,
                    "content": content,
                    "saved_at": datetime.now(timezone.utc).isoformat(),
                    "size_kb": content_size_kb,
                    "checksum": self._calculate_checksum(content)
                }, f, ensure_ascii=False, indent=2)

            # 删除未压缩版本（如果存在）
            if current_file.exists():
                current_file.unlink()

            file_size = compressed_file.stat().st_size
            logger.info(
                f"[LongTermStore] Saved (compressed): user={user_id}, "
                f"size={file_size/1024:.2f}KB, content_size={content_size_kb:.2f}KB"
            )
        else:
            # 保存为未压缩JSON
            with open(current_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "user_id": user_id,
                    "content": content,
                    "saved_at": datetime.now(timezone.utc).isoformat(),
                    "size_kb": content_size_kb,
                    "checksum": self._calculate_checksum(content)
                }, f, ensure_ascii=False, indent=2)

            # 删除压缩版本（如果存在）
            if compressed_file.exists():
                compressed_file.unlink()

            file_size = current_file.stat().st_size
            logger.info(
                f"[LongTermStore] Saved (uncompressed): user={user_id}, "
                f"size={file_size/1024:.2f}KB"
            )

        # 更新备份时间
        self._last_backup[user_id] = datetime.now(timezone.utc)

        # 清理旧版本
        await self._cleanup_old_versions(user_id)

        return {
            "success": True,
            "user_id": user_id,
            "file_size_bytes": file_size,
            "content_size_kb": content_size_kb,
            "compressed": self.compression_enabled,
            "secondary_compressed": needs_compression,
            "backup_version": backup_version
        }

    async def load(
        self,
        user_id: str,
        verify_checksum: bool = True
    ) -> Optional[str]:
        """
        从磁盘加载长期记忆

        Args:
            user_id: 用户ID
            verify_checksum: 是否验证校验和

        Returns:
            长期记忆内容，如果不存在则返回None
        """
        user_dir = self._get_user_dir(user_id)
        current_file = user_dir / "current.json"
        compressed_file = user_dir / "current.json.gz"

        # 优先加载压缩版本
        if compressed_file.exists():
            try:
                with gzip.open(compressed_file, 'rt', encoding='utf-8') as f:
                    data = json.load(f)

                content = data.get("content", "")
                checksum = data.get("checksum", "")

                # 验证校验和
                if verify_checksum and checksum:
                    actual_checksum = self._calculate_checksum(content)
                    if actual_checksum != checksum:
                        logger.error(
                            f"[LongTermStore] Checksum mismatch for user={user_id}! "
                            f"Expected={checksum}, Actual={actual_checksum}"
                        )
                        # 尝试从备份恢复
                        return await self._restore_from_backup(user_id)

                logger.info(
                    f"[LongTermStore] Loaded (compressed): user={user_id}, "
                    f"size={data.get('size_kb', 0):.2f}KB"
                )
                return content

            except Exception as e:
                logger.error(f"[LongTermStore] Failed to load compressed file: {e}")
                # 尝试从备份恢复
                return await self._restore_from_backup(user_id)

        # 加载未压缩版本
        elif current_file.exists():
            try:
                with open(current_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                content = data.get("content", "")
                checksum = data.get("checksum", "")

                # 验证校验和
                if verify_checksum and checksum:
                    actual_checksum = self._calculate_checksum(content)
                    if actual_checksum != checksum:
                        logger.error(
                            f"[LongTermStore] Checksum mismatch for user={user_id}!"
                        )
                        return await self._restore_from_backup(user_id)

                logger.info(
                    f"[LongTermStore] Loaded (uncompressed): user={user_id}, "
                    f"size={data.get('size_kb', 0):.2f}KB"
                )
                return content

            except Exception as e:
                logger.error(f"[LongTermStore] Failed to load file: {e}")
                return await self._restore_from_backup(user_id)

        else:
            logger.warning(f"[LongTermStore] No data found for user={user_id}")
            return None

    async def _create_backup_version(
        self,
        user_id: str,
        content: str
    ) -> int:
        """
        创建历史备份版本

        Args:
            user_id: 用户ID
            content: 内容

        Returns:
            备份版本号
        """
        user_dir = self._get_user_dir(user_id)

        # 获取当前版本号
        existing_backups = list(user_dir.glob("backup_v*.json.gz"))
        version = len(existing_backups) + 1

        # 生成备份文件名
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        backup_file = user_dir / f"backup_v{version}_{timestamp}.json.gz"

        # 保存备份（始终压缩）
        with gzip.open(backup_file, 'wt', encoding='utf-8') as f:
            json.dump({
                "user_id": user_id,
                "content": content,
                "backup_version": version,
                "backup_time": datetime.now(timezone.utc).isoformat(),
                "checksum": self._calculate_checksum(content)
            }, f, ensure_ascii=False, indent=2)

        logger.info(
            f"[LongTermStore] Created backup version {version} for user={user_id}"
        )

        return version

    async def _restore_from_backup(
        self,
        user_id: str,
        version: Optional[int] = None
    ) -> Optional[str]:
        """
        从备份恢复长期记忆

        Args:
            user_id: 用户ID
            version: 备份版本号（如果为None则使用最新版本）

        Returns:
            恢复的内容，如果失败则返回None
        """
        user_dir = self._get_user_dir(user_id)
        backups = sorted(user_dir.glob("backup_v*.json.gz"), reverse=True)

        if not backups:
            logger.error(f"[LongTermStore] No backup found for user={user_id}")
            return None

        # 选择备份文件
        if version is not None:
            backup_file = next(
                (b for b in backups if f"backup_v{version}_" in b.name),
                None
            )
            if not backup_file:
                logger.error(
                    f"[LongTermStore] Backup version {version} not found for user={user_id}"
                )
                return None
        else:
            backup_file = backups[0]  # 最新备份

        try:
            with gzip.open(backup_file, 'rt', encoding='utf-8') as f:
                data = json.load(f)

            content = data.get("content", "")
            logger.info(
                f"[LongTermStore] Restored from backup: user={user_id}, "
                f"version={data.get('backup_version', 'unknown')}"
            )
            return content

        except Exception as e:
            logger.error(f"[LongTermStore] Failed to restore from backup: {e}")
            return None

    async def _cleanup_old_versions(self, user_id: str):
        """清理过期的备份版本"""
        user_dir = self._get_user_dir(user_id)
        backups = sorted(user_dir.glob("backup_v*.json.gz"), reverse=True)

        # 删除超出保留数量的备份
        if len(backups) > self.keep_versions:
            for old_backup in backups[self.keep_versions:]:
                try:
                    old_backup.unlink()
                    logger.info(f"[LongTermStore] Deleted old backup: {old_backup.name}")
                except Exception as e:
                    logger.error(f"[LongTermStore] Failed to delete old backup: {e}")

    async def _secondary_compress(self, content: str) -> str:
        """
        二次压缩：对长期记忆进行智能摘要压缩

        策略：
        1. 提取核心信息（用户偏好、重要决策）
        2. 移除冗余描述
        3. 合并相似主题

        Args:
            content: 原始长期记忆内容

        Returns:
            压缩后的内容
        """
        logger.info(
            f"[LongTermStore] Applying secondary compression, "
            f"original_size={len(content.encode('utf-8'))/1024:.2f}KB"
        )

        # 简单的压缩策略：提取关键句子
        lines = content.split('\n')

        # 保留包含关键词的句子
        important_keywords = [
            # 用户偏好
            "喜欢", "不喜欢", "偏好", "习惯", "风格",
            # 重要决策
            "决定", "选择", "确定", "要求", "需要",
            # 核心信息
            "设定", "角色", "大纲", "主线", "背景",
            # 创作指导
            "写法", "技巧", "注意", "避免", "强调"
        ]

        compressed_lines = []
        for line in lines:
            line = line.strip()
            if not line:
                continue

            # 保留包含关键词的行
            if any(keyword in line for keyword in important_keywords):
                compressed_lines.append(line)
            # 或者保留足够长的句子（可能包含重要信息）
            elif len(line) > 20:
                # 简单检查是否是重要信息（包含冒号、数字、引号等）
                if any(char in line for char in [':', '：', '"', '"', '《', '》', '1', '2', '3']):
                    compressed_lines.append(line)

        # 如果压缩后太少，保留更多内容
        if len(compressed_lines) < len(lines) * 0.3:  # 至少保留30%
            compressed_lines = lines[:int(len(lines) * 0.5)]  # 保留前50%

        compressed_content = '\n'.join(compressed_lines)

        logger.info(
            f"[LongTermStore] Secondary compression complete, "
            f"new_size={len(compressed_content.encode('utf-8'))/1024:.2f}KB, "
            f"reduction={100*(1-len(compressed_content)/len(content)):.1f}%"
        )

        return compressed_content

    async def get_metadata(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        获取用户的存储元数据

        Args:
            user_id: 用户ID

        Returns:
            元数据字典
        """
        user_dir = self._get_user_dir(user_id)
        current_file = user_dir / "current.json"
        compressed_file = user_dir / "current.json.gz"

        metadata = {
            "user_id": user_id,
            "exists": False,
            "compressed": False,
            "file_size_bytes": 0,
            "content_size_kb": 0,
            "last_modified": None,
            "backup_versions": 0
        }

        # 检查当前文件
        if compressed_file.exists():
            metadata["exists"] = True
            metadata["compressed"] = True
            metadata["file_size_bytes"] = compressed_file.stat().st_size
            metadata["last_modified"] = datetime.fromtimestamp(
                compressed_file.stat().st_mtime,
                tz=timezone.utc
            ).isoformat()

            try:
                with gzip.open(compressed_file, 'rt', encoding='utf-8') as f:
                    data = json.load(f)
                metadata["content_size_kb"] = data.get("size_kb", 0)
            except:
                pass

        elif current_file.exists():
            metadata["exists"] = True
            metadata["compressed"] = False
            metadata["file_size_bytes"] = current_file.stat().st_size
            metadata["last_modified"] = datetime.fromtimestamp(
                current_file.stat().st_mtime,
                tz=timezone.utc
            ).isoformat()

            try:
                with open(current_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                metadata["content_size_kb"] = data.get("size_kb", 0)
            except:
                pass

        # 统计备份版本
        backups = list(user_dir.glob("backup_v*.json.gz"))
        metadata["backup_versions"] = len(backups)

        return metadata

    async def list_backups(self, user_id: str) -> List[Dict[str, Any]]:
        """
        列出用户的所有备份版本

        Args:
            user_id: 用户ID

        Returns:
            备份信息列表
        """
        user_dir = self._get_user_dir(user_id)
        backups = sorted(user_dir.glob("backup_v*.json.gz"), reverse=True)

        backup_list = []
        for backup_file in backups:
            try:
                with gzip.open(backup_file, 'rt', encoding='utf-8') as f:
                    data = json.load(f)

                backup_list.append({
                    "filename": backup_file.name,
                    "version": data.get("backup_version", 0),
                    "backup_time": data.get("backup_time", ""),
                    "file_size_bytes": backup_file.stat().st_size,
                    "checksum": data.get("checksum", "")
                })
            except Exception as e:
                logger.error(f"[LongTermStore] Failed to read backup {backup_file.name}: {e}")

        return backup_list


# 全局单例
_default_store: Optional[LongTermMemoryStore] = None


def get_long_term_store(
    base_dir: str = "./data/long_term_memory",
    max_size_kb: int = 50,
    compression_enabled: bool = True
) -> LongTermMemoryStore:
    """
    获取全局默认的长期记忆存储器实例（单例模式）

    Args:
        base_dir: 基础数据目录
        max_size_kb: 触发二次压缩的阈值（KB）
        compression_enabled: 是否启用压缩

    Returns:
        LongTermMemoryStore实例
    """
    global _default_store
    if _default_store is None:
        _default_store = LongTermMemoryStore(
            base_dir=base_dir,
            max_size_kb=max_size_kb,
            compression_enabled=compression_enabled
        )
    return _default_store
