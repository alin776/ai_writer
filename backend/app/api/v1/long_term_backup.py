"""
长期记忆备份管理API (P1-6修复)

提供长期记忆的备份、恢复和管理接口
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any, List, Optional
import logging

from app.services.agent.memory import get_long_term_store

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/metadata/{user_id}", summary="获取长期记忆元数据")
async def get_long_term_metadata(user_id: str) -> Dict[str, Any]:
    """
    获取用户的长期记忆存储元数据

    Args:
        user_id: 用户ID

    Returns:
        元数据字典，包含文件大小、压缩状态、备份版本数等信息

    示例:
        GET /api/v1/long-term-backup/metadata/user_123

        Response:
        {
            "user_id": "user_123",
            "exists": true,
            "compressed": true,
            "file_size_bytes": 12345,
            "content_size_kb": 45.2,
            "last_modified": "2025-11-22T10:00:00Z",
            "backup_versions": 3
        }
    """
    try:
        store = get_long_term_store()
        metadata = await store.get_metadata(user_id)

        if not metadata:
            raise HTTPException(status_code=404, detail=f"No metadata found for user {user_id}")

        return metadata

    except Exception as e:
        logger.error(f"Failed to get metadata for user {user_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get metadata: {str(e)}"
        )


@router.get("/backups/{user_id}", summary="列出所有备份版本")
async def list_backups(user_id: str) -> Dict[str, Any]:
    """
    列出用户的所有长期记忆备份版本

    Args:
        user_id: 用户ID

    Returns:
        包含备份列表的字典

    示例:
        GET /api/v1/long-term-backup/backups/user_123

        Response:
        {
            "user_id": "user_123",
            "total_backups": 3,
            "backups": [
                {
                    "filename": "backup_v3_20251122_100000.json.gz",
                    "version": 3,
                    "backup_time": "2025-11-22T10:00:00Z",
                    "file_size_bytes": 8192,
                    "checksum": "abc123..."
                },
                ...
            ]
        }
    """
    try:
        store = get_long_term_store()
        backups = await store.list_backups(user_id)

        return {
            "user_id": user_id,
            "total_backups": len(backups),
            "backups": backups
        }

    except Exception as e:
        logger.error(f"Failed to list backups for user {user_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to list backups: {str(e)}"
        )


@router.post("/restore/{user_id}", summary="从备份恢复长期记忆")
async def restore_from_backup(
    user_id: str,
    version: Optional[int] = Query(None, description="备份版本号（不指定则使用最新版本）")
) -> Dict[str, Any]:
    """
    从磁盘备份恢复长期记忆到Redis

    Args:
        user_id: 用户ID
        version: 备份版本号（可选）

    Returns:
        恢复结果

    示例:
        POST /api/v1/long-term-backup/restore/user_123?version=2

        Response:
        {
            "success": true,
            "user_id": "user_123",
            "restored_version": 2,
            "content_size_kb": 45.2,
            "message": "Long-term memory restored successfully"
        }
    """
    try:
        from app.services.agent.memory import EnhancedMemoryManager
        from app.core.redis_client import get_redis_client

        store = get_long_term_store()

        # 从备份恢复内容
        content = await store._restore_from_backup(user_id, version=version)

        if not content:
            raise HTTPException(
                status_code=404,
                detail=f"No backup found for user {user_id}" + (
                    f" version {version}" if version else ""
                )
            )

        # 保存到Redis
        redis_client = get_redis_client()
        key = f"memory:{user_id}:long_term"
        redis_client.set(key, content)

        content_size_kb = len(content.encode('utf-8')) / 1024

        logger.info(
            f"[LongTermBackup] Restored from backup: user={user_id}, "
            f"version={version or 'latest'}, size={content_size_kb:.2f}KB"
        )

        return {
            "success": True,
            "user_id": user_id,
            "restored_version": version or "latest",
            "content_size_kb": round(content_size_kb, 2),
            "message": "Long-term memory restored successfully"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to restore from backup for user {user_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to restore from backup: {str(e)}"
        )


@router.post("/backup/{user_id}", summary="手动触发备份")
async def manual_backup(user_id: str) -> Dict[str, Any]:
    """
    手动触发长期记忆备份到磁盘

    Args:
        user_id: 用户ID

    Returns:
        备份结果

    示例:
        POST /api/v1/long-term-backup/backup/user_123

        Response:
        {
            "success": true,
            "user_id": "user_123",
            "file_size_bytes": 12345,
            "content_size_kb": 45.2,
            "compressed": true,
            "secondary_compressed": false,
            "backup_version": 4
        }
    """
    try:
        from app.core.redis_client import get_redis_client

        redis_client = get_redis_client()
        key = f"memory:{user_id}:long_term"

        # 从Redis读取长期记忆
        content = redis_client.get(key)

        if not content:
            raise HTTPException(
                status_code=404,
                detail=f"No long-term memory found for user {user_id}"
            )

        # 兼容decode_responses配置
        if isinstance(content, bytes):
            content = content.decode('utf-8')

        # 保存到磁盘
        store = get_long_term_store()
        result = await store.save(
            user_id=user_id,
            content=content,
            auto_compress=True,
            create_backup=True
        )

        logger.info(
            f"[LongTermBackup] Manual backup completed: user={user_id}, "
            f"size={result.get('content_size_kb', 0):.2f}KB"
        )

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to backup for user {user_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to backup: {str(e)}"
        )


@router.delete("/backups/{user_id}", summary="清理旧备份")
async def cleanup_old_backups(
    user_id: str,
    keep_versions: int = Query(5, ge=1, le=20, description="保留的备份版本数")
) -> Dict[str, Any]:
    """
    清理用户的旧备份，只保留指定数量的最新版本

    Args:
        user_id: 用户ID
        keep_versions: 保留的备份版本数（默认5）

    Returns:
        清理结果

    示例:
        DELETE /api/v1/long-term-backup/backups/user_123?keep_versions=3

        Response:
        {
            "success": true,
            "user_id": "user_123",
            "deleted_count": 2,
            "remaining_count": 3,
            "message": "Old backups cleaned up successfully"
        }
    """
    try:
        store = get_long_term_store()

        # 获取当前备份列表
        backups = await store.list_backups(user_id)
        total_backups = len(backups)

        if total_backups <= keep_versions:
            return {
                "success": True,
                "user_id": user_id,
                "deleted_count": 0,
                "remaining_count": total_backups,
                "message": "No cleanup needed"
            }

        # 清理旧备份
        await store._cleanup_old_versions(user_id)

        # 重新获取备份列表
        remaining_backups = await store.list_backups(user_id)
        deleted_count = total_backups - len(remaining_backups)

        logger.info(
            f"[LongTermBackup] Cleaned up old backups: user={user_id}, "
            f"deleted={deleted_count}, remaining={len(remaining_backups)}"
        )

        return {
            "success": True,
            "user_id": user_id,
            "deleted_count": deleted_count,
            "remaining_count": len(remaining_backups),
            "message": "Old backups cleaned up successfully"
        }

    except Exception as e:
        logger.error(f"Failed to cleanup backups for user {user_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to cleanup backups: {str(e)}"
        )


@router.get("/stats", summary="获取备份系统统计")
async def get_backup_stats() -> Dict[str, Any]:
    """
    获取整个备份系统的统计信息

    Returns:
        统计信息字典

    示例:
        GET /api/v1/long-term-backup/stats

        Response:
        {
            "total_users": 10,
            "total_backups": 42,
            "total_size_mb": 5.2,
            "compression_enabled": true,
            "max_size_threshold_kb": 50
        }
    """
    try:
        import os
        from pathlib import Path

        store = get_long_term_store()
        base_dir = Path(store.base_dir)

        if not base_dir.exists():
            return {
                "total_users": 0,
                "total_backups": 0,
                "total_size_mb": 0,
                "compression_enabled": store.compression_enabled,
                "max_size_threshold_kb": store.max_size_kb
            }

        # 统计所有用户
        user_dirs = [d for d in base_dir.iterdir() if d.is_dir()]
        total_users = len(user_dirs)

        # 统计所有备份文件
        total_backups = 0
        total_size = 0

        for user_dir in user_dirs:
            backups = list(user_dir.glob("backup_v*.json.gz"))
            total_backups += len(backups)

            for backup_file in backups:
                total_size += backup_file.stat().st_size

            # 加上当前文件
            current_file = user_dir / "current.json.gz"
            if current_file.exists():
                total_size += current_file.stat().st_size
            else:
                current_file = user_dir / "current.json"
                if current_file.exists():
                    total_size += current_file.stat().st_size

        return {
            "total_users": total_users,
            "total_backups": total_backups,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "compression_enabled": store.compression_enabled,
            "max_size_threshold_kb": store.max_size_kb,
            "auto_backup_interval_seconds": store.auto_backup_interval
        }

    except Exception as e:
        logger.error(f"Failed to get backup stats: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get backup stats: {str(e)}"
        )
