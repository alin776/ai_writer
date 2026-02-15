"""
记忆导入导出模块 (P2-6修复)

提供记忆数据的导入导出功能：
1. 导出：将记忆导出为JSON/CSV格式
2. 导入：从文件导入记忆
3. 迁移：在不同用户/实例间迁移记忆
4. 备份恢复：完整的备份和恢复功能

支持格式：
- JSON：完整数据，支持元数据
- CSV：表格格式，便于分析
- Markdown：可读格式，便于查看

使用示例：
```python
exporter = MemoryExporter(redis_client)

# 导出为JSON
json_data = await exporter.export_json(user_id="user_123")

# 导出为CSV
csv_data = await exporter.export_csv(user_id="user_123")

# 导入
importer = MemoryImporter(redis_client)
result = await importer.import_json(user_id="user_123", json_data=json_data)
```
"""

import json
import csv
import io
import gzip
import logging
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum
from redis import Redis
from app.utils.datetime_utils import get_utc_now

logger = logging.getLogger(__name__)


class ExportFormat(Enum):
    """导出格式"""
    JSON = "json"
    CSV = "csv"
    MARKDOWN = "markdown"
    COMPRESSED_JSON = "json.gz"


@dataclass
class ExportMetadata:
    """导出元数据"""
    export_time: datetime
    user_id: str
    format: ExportFormat
    version: str = "1.0"
    total_memories: int = 0
    short_term_count: int = 0
    medium_term_count: int = 0
    has_long_term: bool = False
    source_instance: str = ""


@dataclass
class ImportResult:
    """导入结果"""
    success: bool
    imported_count: int
    skipped_count: int
    error_count: int
    errors: List[str]
    warnings: List[str]


class MemoryExporter:
    """
    记忆导出器

    支持多种格式的记忆导出
    """

    VERSION = "1.0"

    def __init__(self, redis_client: Redis):
        """
        初始化导出器

        Args:
            redis_client: Redis客户端
        """
        self.redis = redis_client
        logger.info("[MemoryExporter] Initialized")

    async def export_json(
        self,
        user_id: str,
        include_metadata: bool = True,
        pretty: bool = False
    ) -> str:
        """
        导出为JSON格式

        Args:
            user_id: 用户ID
            include_metadata: 是否包含元数据
            pretty: 是否美化输出

        Returns:
            JSON字符串
        """
        # 获取所有记忆
        short_term = await self._get_short_term(user_id)
        medium_term = await self._get_medium_term(user_id)
        long_term = await self._get_long_term(user_id)

        export_data = {
            "memories": {
                "short_term": short_term,
                "medium_term": medium_term,
                "long_term": long_term
            }
        }

        if include_metadata:
            export_data["metadata"] = {
                "export_time": datetime.now(timezone.utc).isoformat(),
                "user_id": user_id,
                "format": ExportFormat.JSON.value,
                "version": self.VERSION,
                "total_memories": len(short_term) + len(medium_term),
                "short_term_count": len(short_term),
                "medium_term_count": len(medium_term),
                "has_long_term": bool(long_term)
            }

        indent = 2 if pretty else None
        return json.dumps(export_data, ensure_ascii=False, indent=indent)

    async def export_compressed_json(
        self,
        user_id: str
    ) -> bytes:
        """
        导出为压缩JSON格式

        Args:
            user_id: 用户ID

        Returns:
            Gzip压缩的字节数据
        """
        json_data = await self.export_json(user_id, include_metadata=True, pretty=False)
        return gzip.compress(json_data.encode('utf-8'))

    async def export_csv(
        self,
        user_id: str,
        include_content: bool = True
    ) -> str:
        """
        导出为CSV格式

        Args:
            user_id: 用户ID
            include_content: 是否包含完整内容

        Returns:
            CSV字符串
        """
        # 获取所有记忆
        short_term = await self._get_short_term(user_id)
        medium_term = await self._get_medium_term(user_id)

        # 定义CSV列
        columns = [
            "id", "layer", "role", "importance", "created_at",
            "access_count", "content_preview"
        ]
        if include_content:
            columns.append("content")

        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=columns)
        writer.writeheader()

        # 写入短期记忆
        for memory in short_term:
            row = self._memory_to_csv_row(memory, "short_term", include_content)
            writer.writerow(row)

        # 写入中期记忆
        for memory in medium_term:
            row = self._memory_to_csv_row(memory, "medium_term", include_content)
            writer.writerow(row)

        return output.getvalue()

    async def export_markdown(
        self,
        user_id: str,
        include_stats: bool = True
    ) -> str:
        """
        导出为Markdown格式

        Args:
            user_id: 用户ID
            include_stats: 是否包含统计信息

        Returns:
            Markdown字符串
        """
        # 获取所有记忆
        short_term = await self._get_short_term(user_id)
        medium_term = await self._get_medium_term(user_id)
        long_term = await self._get_long_term(user_id)

        lines = []

        # 标题
        lines.append(f"# 记忆导出 - {user_id}")
        lines.append(f"\n导出时间: {get_utc_now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        # 统计
        if include_stats:
            lines.append("## 统计信息\n")
            lines.append(f"- 短期记忆: {len(short_term)} 条")
            lines.append(f"- 中期记忆: {len(medium_term)} 条")
            lines.append(f"- 长期记忆: {'有' if long_term else '无'}")
            lines.append("")

        # 短期记忆
        if short_term:
            lines.append("## 短期记忆\n")
            for i, memory in enumerate(short_term, 1):
                lines.append(f"### {i}. {memory.get('role', 'unknown')} ({memory.get('id', '')})")
                lines.append(f"- 重要度: {memory.get('importance', 0):.2f}")
                lines.append(f"- 时间: {memory.get('created_at', 'N/A')}")
                lines.append(f"\n```\n{memory.get('content', '')[:500]}{'...' if len(memory.get('content', '')) > 500 else ''}\n```\n")

        # 中期记忆
        if medium_term:
            lines.append("## 中期记忆\n")
            for i, memory in enumerate(medium_term, 1):
                lines.append(f"### {i}. {memory.get('role', 'unknown')} ({memory.get('id', '')})")
                lines.append(f"- 重要度: {memory.get('importance', 0):.2f}")
                lines.append(f"- 访问次数: {memory.get('access_count', 0)}")
                lines.append(f"- 时间: {memory.get('created_at', 'N/A')}")
                lines.append(f"\n```\n{memory.get('content', '')[:500]}{'...' if len(memory.get('content', '')) > 500 else ''}\n```\n")

        # 长期记忆
        if long_term:
            lines.append("## 长期记忆摘要\n")
            lines.append(f"```\n{long_term[:1000]}{'...' if len(long_term) > 1000 else ''}\n```\n")

        return "\n".join(lines)

    def _memory_to_csv_row(
        self,
        memory: Dict[str, Any],
        layer: str,
        include_content: bool
    ) -> Dict[str, Any]:
        """将记忆转换为CSV行"""
        content = memory.get("content", "")
        row = {
            "id": memory.get("id", ""),
            "layer": layer,
            "role": memory.get("role", ""),
            "importance": memory.get("importance", 0),
            "created_at": memory.get("created_at", ""),
            "access_count": memory.get("access_count", 0),
            "content_preview": content[:100] + "..." if len(content) > 100 else content
        }
        if include_content:
            row["content"] = content
        return row

    async def _get_short_term(self, user_id: str) -> List[Dict[str, Any]]:
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

    async def _get_medium_term(self, user_id: str) -> List[Dict[str, Any]]:
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

    async def _get_long_term(self, user_id: str) -> str:
        """获取长期记忆"""
        key = f"memory:{user_id}:long_term"
        summary = self.redis.get(key)

        if not summary:
            return ""

        return summary.decode('utf-8') if isinstance(summary, bytes) else summary


class MemoryImporter:
    """
    记忆导入器

    支持从多种格式导入记忆
    """

    def __init__(self, redis_client: Redis):
        """
        初始化导入器

        Args:
            redis_client: Redis客户端
        """
        self.redis = redis_client
        logger.info("[MemoryImporter] Initialized")

    async def import_json(
        self,
        user_id: str,
        json_data: Union[str, Dict[str, Any]],
        merge: bool = True,
        overwrite_existing: bool = False
    ) -> ImportResult:
        """
        从JSON导入记忆

        Args:
            user_id: 目标用户ID
            json_data: JSON数据（字符串或字典）
            merge: 是否合并到现有记忆（否则清空后导入）
            overwrite_existing: 是否覆盖同ID记忆

        Returns:
            导入结果
        """
        errors = []
        warnings = []
        imported_count = 0
        skipped_count = 0
        error_count = 0

        try:
            # 解析JSON
            if isinstance(json_data, str):
                data = json.loads(json_data)
            else:
                data = json_data

            memories = data.get("memories", {})

            # 检查版本兼容性
            metadata = data.get("metadata", {})
            version = metadata.get("version", "1.0")
            if version != "1.0":
                warnings.append(f"版本不匹配: 期望1.0, 实际{version}")

            # 如果不合并，先清空现有记忆
            if not merge:
                await self._clear_memories(user_id)
                logger.info(f"[MemoryImporter] Cleared existing memories for user {user_id}")

            # 导入短期记忆
            short_term = memories.get("short_term", [])
            for memory in short_term:
                try:
                    result = await self._import_short_term(user_id, memory, overwrite_existing)
                    if result == "imported":
                        imported_count += 1
                    elif result == "skipped":
                        skipped_count += 1
                except Exception as e:
                    error_count += 1
                    errors.append(f"短期记忆导入失败: {str(e)}")

            # 导入中期记忆
            medium_term = memories.get("medium_term", [])
            for memory in medium_term:
                try:
                    result = await self._import_medium_term(user_id, memory, overwrite_existing)
                    if result == "imported":
                        imported_count += 1
                    elif result == "skipped":
                        skipped_count += 1
                except Exception as e:
                    error_count += 1
                    errors.append(f"中期记忆导入失败: {str(e)}")

            # 导入长期记忆
            long_term = memories.get("long_term", "")
            if long_term:
                try:
                    await self._import_long_term(user_id, long_term, merge)
                    imported_count += 1
                except Exception as e:
                    error_count += 1
                    errors.append(f"长期记忆导入失败: {str(e)}")

            logger.info(
                f"[MemoryImporter] Import completed: "
                f"user={user_id}, imported={imported_count}, "
                f"skipped={skipped_count}, errors={error_count}"
            )

            return ImportResult(
                success=error_count == 0,
                imported_count=imported_count,
                skipped_count=skipped_count,
                error_count=error_count,
                errors=errors,
                warnings=warnings
            )

        except Exception as e:
            logger.error(f"[MemoryImporter] Import failed: {e}")
            return ImportResult(
                success=False,
                imported_count=0,
                skipped_count=0,
                error_count=1,
                errors=[str(e)],
                warnings=[]
            )

    async def import_compressed_json(
        self,
        user_id: str,
        compressed_data: bytes,
        merge: bool = True
    ) -> ImportResult:
        """
        从压缩JSON导入记忆

        Args:
            user_id: 目标用户ID
            compressed_data: Gzip压缩的数据
            merge: 是否合并

        Returns:
            导入结果
        """
        try:
            json_data = gzip.decompress(compressed_data).decode('utf-8')
            return await self.import_json(user_id, json_data, merge)
        except Exception as e:
            return ImportResult(
                success=False,
                imported_count=0,
                skipped_count=0,
                error_count=1,
                errors=[f"解压缩失败: {str(e)}"],
                warnings=[]
            )

    async def _clear_memories(self, user_id: str):
        """清空用户的所有记忆"""
        keys = [
            f"memory:{user_id}:short_term",
            f"memory:{user_id}:medium_term",
            f"memory:{user_id}:long_term"
        ]
        self.redis.delete(*keys)

    async def _import_short_term(
        self,
        user_id: str,
        memory: Dict[str, Any],
        overwrite: bool
    ) -> str:
        """导入短期记忆"""
        key = f"memory:{user_id}:short_term"

        # 检查是否已存在
        if not overwrite:
            existing = self.redis.lrange(key, 0, -1)
            memory_id = memory.get("id", "")
            for e in existing:
                if isinstance(e, bytes):
                    e = e.decode('utf-8')
                try:
                    existing_data = json.loads(e)
                    if existing_data.get("id") == memory_id:
                        return "skipped"
                except:
                    pass

        # 添加记忆
        self.redis.rpush(key, json.dumps(memory, ensure_ascii=False))
        self.redis.expire(key, 86400)  # 24小时

        return "imported"

    async def _import_medium_term(
        self,
        user_id: str,
        memory: Dict[str, Any],
        overwrite: bool
    ) -> str:
        """导入中期记忆"""
        key = f"memory:{user_id}:medium_term"
        importance = memory.get("importance", 0.5)

        # 检查是否已存在
        if not overwrite:
            existing = self.redis.zrange(key, 0, -1)
            memory_id = memory.get("id", "")
            for e in existing:
                if isinstance(e, bytes):
                    e = e.decode('utf-8')
                try:
                    existing_data = json.loads(e)
                    if existing_data.get("id") == memory_id:
                        return "skipped"
                except:
                    pass

        # 添加记忆
        self.redis.zadd(key, {json.dumps(memory, ensure_ascii=False): importance})
        self.redis.expire(key, 86400 * 3)  # 3天

        return "imported"

    async def _import_long_term(
        self,
        user_id: str,
        summary: str,
        merge: bool
    ):
        """导入长期记忆"""
        key = f"memory:{user_id}:long_term"

        if merge:
            # 合并到现有摘要
            existing = self.redis.get(key)
            if existing:
                if isinstance(existing, bytes):
                    existing = existing.decode('utf-8')
                summary = f"{existing}\n\n[导入的记忆]\n{summary}"

        self.redis.set(key, summary)


class MemoryMigrator:
    """
    记忆迁移器

    在不同用户/实例间迁移记忆
    """

    def __init__(self, redis_client: Redis):
        """
        初始化迁移器

        Args:
            redis_client: Redis客户端
        """
        self.redis = redis_client
        self.exporter = MemoryExporter(redis_client)
        self.importer = MemoryImporter(redis_client)

        logger.info("[MemoryMigrator] Initialized")

    async def migrate_user(
        self,
        from_user_id: str,
        to_user_id: str,
        delete_source: bool = False
    ) -> ImportResult:
        """
        迁移用户记忆

        Args:
            from_user_id: 源用户ID
            to_user_id: 目标用户ID
            delete_source: 是否删除源数据

        Returns:
            迁移结果
        """
        try:
            # 导出源用户记忆
            json_data = await self.exporter.export_json(from_user_id)

            # 导入到目标用户
            result = await self.importer.import_json(
                to_user_id,
                json_data,
                merge=True,
                overwrite_existing=False
            )

            # 删除源数据
            if delete_source and result.success:
                keys = [
                    f"memory:{from_user_id}:short_term",
                    f"memory:{from_user_id}:medium_term",
                    f"memory:{from_user_id}:long_term"
                ]
                self.redis.delete(*keys)
                logger.info(f"[MemoryMigrator] Deleted source memories: {from_user_id}")

            logger.info(
                f"[MemoryMigrator] Migration completed: "
                f"{from_user_id} -> {to_user_id}, "
                f"imported={result.imported_count}"
            )

            return result

        except Exception as e:
            logger.error(f"[MemoryMigrator] Migration failed: {e}")
            return ImportResult(
                success=False,
                imported_count=0,
                skipped_count=0,
                error_count=1,
                errors=[str(e)],
                warnings=[]
            )

    async def clone_memories(
        self,
        source_user_id: str,
        target_user_ids: List[str]
    ) -> Dict[str, ImportResult]:
        """
        克隆记忆到多个用户

        Args:
            source_user_id: 源用户ID
            target_user_ids: 目标用户ID列表

        Returns:
            各用户的导入结果
        """
        results = {}

        # 导出源用户记忆
        json_data = await self.exporter.export_json(source_user_id)

        # 导入到每个目标用户
        for target_id in target_user_ids:
            result = await self.importer.import_json(
                target_id,
                json_data,
                merge=False,
                overwrite_existing=True
            )
            results[target_id] = result

        logger.info(
            f"[MemoryMigrator] Clone completed: "
            f"source={source_user_id}, targets={len(target_user_ids)}"
        )

        return results


# 便捷函数
async def export_memories(
    redis_client: Redis,
    user_id: str,
    format: ExportFormat = ExportFormat.JSON
) -> Union[str, bytes]:
    """
    导出记忆的便捷函数

    Args:
        redis_client: Redis客户端
        user_id: 用户ID
        format: 导出格式

    Returns:
        导出数据
    """
    exporter = MemoryExporter(redis_client)

    if format == ExportFormat.JSON:
        return await exporter.export_json(user_id, pretty=True)
    elif format == ExportFormat.CSV:
        return await exporter.export_csv(user_id)
    elif format == ExportFormat.MARKDOWN:
        return await exporter.export_markdown(user_id)
    elif format == ExportFormat.COMPRESSED_JSON:
        return await exporter.export_compressed_json(user_id)
    else:
        raise ValueError(f"Unsupported format: {format}")


async def import_memories(
    redis_client: Redis,
    user_id: str,
    data: Union[str, bytes, Dict[str, Any]],
    merge: bool = True
) -> ImportResult:
    """
    导入记忆的便捷函数

    Args:
        redis_client: Redis客户端
        user_id: 用户ID
        data: 导入数据
        merge: 是否合并

    Returns:
        导入结果
    """
    importer = MemoryImporter(redis_client)

    if isinstance(data, bytes):
        return await importer.import_compressed_json(user_id, data, merge)
    else:
        return await importer.import_json(user_id, data, merge)
