# -*- coding: utf-8 -*-
"""
Explore Artifact 持久化工具

用于保存 explore_content 的完整结果，支持 TTL 与容量上限清理。
"""

from __future__ import annotations

import json
import logging
import time
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from app.core.config import settings

logger = logging.getLogger(__name__)


# 默认策略（按需求可调）
EXPLORE_ARTIFACT_TTL_SECONDS = 7 * 24 * 60 * 60
EXPLORE_ARTIFACT_MAX_CHARS = 200000
EXPLORE_ARTIFACT_MAX_PER_WORK = 200
EXPLORE_ARTIFACT_MAX_GLOBAL = 10000
SESSION_ARTIFACT_TTL_SECONDS = EXPLORE_ARTIFACT_TTL_SECONDS
SESSION_ARTIFACT_MAX_ITEMS = 20
SESSION_ARTIFACT_KEY_PREFIX = "explore:artifact:session"
ARTIFACT_INDEX_KEY_PREFIX = "explore:artifact:index"


def _candidate_upload_roots() -> List[Path]:
    upload_dir = Path(settings.UPLOAD_DIR)
    if upload_dir.is_absolute():
        return [upload_dir]

    # 尝试定位 repo root（backend 的父目录）
    base = Path(__file__).resolve()
    repo_root = None
    backend_root = None
    for parent in base.parents:
        if parent.name == "backend":
            backend_root = parent
            repo_root = parent.parent
            break

    roots: List[Path] = []
    # 服务以 backend/ 作为工作目录时，优先使用 backend 根路径
    if backend_root:
        roots.append(backend_root / upload_dir)
    if repo_root:
        roots.append(repo_root / upload_dir)
    if not roots:
        roots.append(base.parents[5] / upload_dir)

    # 去重并规范化
    unique: List[Path] = []
    seen = set()
    for root in roots:
        resolved = root.resolve()
        if str(resolved) in seen:
            continue
        seen.add(str(resolved))
        unique.append(resolved)
    return unique


def _artifact_root() -> Path:
    roots = _candidate_upload_roots()
    root = roots[0]
    root.mkdir(parents=True, exist_ok=True)
    return root


def _work_dir(work_id: str) -> Path:
    return _artifact_root() / str(work_id)


def _session_key(session_id: str) -> str:
    return f"{SESSION_ARTIFACT_KEY_PREFIX}:{session_id}"


def _artifact_index_key(artifact_id: str) -> str:
    return f"{ARTIFACT_INDEX_KEY_PREFIX}:{artifact_id}"


def _list_artifact_files(base: Path) -> List[Tuple[Path, float]]:
    if not base.exists():
        return []
    files: List[Tuple[Path, float]] = []
    for path in base.rglob("*.json"):
        try:
            stat = path.stat()
        except OSError:
            continue
        files.append((path, stat.st_mtime))
    return files


def _safe_unlink(path: Path) -> bool:
    try:
        path.unlink()
        return True
    except OSError:
        return False


def _enforce_limit(entries: List[Tuple[Path, float]], limit: int) -> int:
    if limit <= 0:
        return 0
    if len(entries) <= limit:
        return 0
    entries.sort(key=lambda item: item[1])  # oldest first
    remove_count = len(entries) - limit
    removed = 0
    for path, _ in entries[:remove_count]:
        if _safe_unlink(path):
            removed += 1
    return removed


async def cleanup_explore_artifacts(work_id: Optional[str] = None) -> Dict[str, int]:
    """清理 Explore Artifact：TTL + 上限控制"""
    root = _artifact_root()
    now = time.time()
    removed_expired = 0
    removed_limit = 0

    # TTL 清理
    if work_id:
        scoped = _list_artifact_files(_work_dir(work_id))
    else:
        scoped = _list_artifact_files(root)

    for path, mtime in scoped:
        if now - mtime > EXPLORE_ARTIFACT_TTL_SECONDS:
            if _safe_unlink(path):
                removed_expired += 1

    # per-work 上限
    if work_id:
        remaining = _list_artifact_files(_work_dir(work_id))
        removed_limit += _enforce_limit(remaining, EXPLORE_ARTIFACT_MAX_PER_WORK)

    # 全局上限
    all_files = _list_artifact_files(root)
    removed_limit += _enforce_limit(all_files, EXPLORE_ARTIFACT_MAX_GLOBAL)

    return {
        "expired": removed_expired,
        "limit": removed_limit
    }


async def invalidate_explore_artifacts(work_id: str) -> int:
    """清理指定作品的所有 Explore Artifact"""
    work_id = str(work_id or "").strip()
    if not work_id:
        return 0
    work_dir = _work_dir(work_id)
    if not work_dir.exists():
        return 0
    removed = 0
    for path in work_dir.rglob("*.json"):
        if _safe_unlink(path):
            removed += 1
    try:
        if not any(work_dir.iterdir()):
            work_dir.rmdir()
    except OSError:
        pass
    return removed


async def save_explore_artifact(
    payload: Dict[str, Any],
    work_id: str,
    user_id: Optional[str],
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """保存 Explore 结果到磁盘"""
    work_id = str(work_id or "").strip()
    if not work_id:
        return {"stored": False, "reason": "missing_work_id"}

    artifact_id = uuid.uuid4().hex
    created_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    data = {
        "artifact_id": artifact_id,
        "work_id": work_id,
        "user_id": str(user_id or ""),
        "created_at": created_at,
        "meta": metadata or {},
        "payload": payload
    }

    try:
        serialized = json.dumps(data, ensure_ascii=False)
    except Exception as exc:
        return {"stored": False, "reason": f"serialize_failed:{exc}"}

    if len(serialized) > EXPLORE_ARTIFACT_MAX_CHARS:
        return {
            "stored": False,
            "reason": "size_limit",
            "size": len(serialized),
            "max_chars": EXPLORE_ARTIFACT_MAX_CHARS
        }

    work_dir = _work_dir(work_id)
    work_dir.mkdir(parents=True, exist_ok=True)
    filepath = work_dir / f"{artifact_id}.json"
    try:
        filepath.write_text(serialized, encoding="utf-8")
    except OSError as exc:
        return {"stored": False, "reason": f"write_failed:{exc}"}

    # 记录 artifact_id -> path 索引（Redis）
    try:
        from app.core.redis import RedisClient
        index_payload = {
            "path": str(filepath),
            "work_id": work_id,
            "user_id": str(user_id or "")
        }
        await RedisClient.set(
            _artifact_index_key(artifact_id),
            index_payload,
            expire=EXPLORE_ARTIFACT_TTL_SECONDS
        )
    except Exception as exc:
        logger.debug(f"[ExploreArtifact] 索引写入失败: {exc}")

    # 清理过期与超限
    try:
        await cleanup_explore_artifacts(work_id=work_id)
    except Exception as exc:
        logger.debug(f"[ExploreArtifact] 清理失败: {exc}")

    return {
        "stored": True,
        "artifact_id": artifact_id,
        "created_at": created_at,
        "path": str(filepath),
        "size": len(serialized)
    }


async def record_session_artifact(
    session_id: str,
    artifact_id: str,
    work_id: str,
    created_at: Optional[str] = None,
    preview: Optional[str] = None
) -> Dict[str, Any]:
    """将 artifact_id 记录到会话状态（Redis）"""
    session_id = str(session_id or "").strip()
    artifact_id = str(artifact_id or "").strip()
    work_id = str(work_id or "").strip()
    if not session_id or not artifact_id:
        return {"stored": False, "reason": "missing_session_or_artifact"}

    from app.core.redis import RedisClient

    key = _session_key(session_id)
    current = await RedisClient.get(key)
    items: List[Dict[str, Any]] = current if isinstance(current, list) else []
    items = [
        item for item in items
        if isinstance(item, dict) and item.get("artifact_id") != artifact_id
    ]
    items.insert(0, {
        "artifact_id": artifact_id,
        "work_id": work_id,
        "created_at": created_at or time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "preview": preview or ""
    })
    if len(items) > SESSION_ARTIFACT_MAX_ITEMS:
        items = items[:SESSION_ARTIFACT_MAX_ITEMS]

    stored = await RedisClient.set(key, items, expire=SESSION_ARTIFACT_TTL_SECONDS)
    return {
        "stored": stored,
        "count": len(items)
    }


async def get_session_artifacts(session_id: str) -> List[Dict[str, Any]]:
    """读取会话状态中的 artifact 列表"""
    session_id = str(session_id or "").strip()
    if not session_id:
        return []
    from app.core.redis import RedisClient
    data = await RedisClient.get(_session_key(session_id))
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    return []


async def load_explore_artifact(
    artifact_id: str,
    work_id: str,
    user_id: Optional[str] = None,
    mode: str = "full",
    max_chars: Optional[int] = None,
    step_reasoning: Optional[str] = None
) -> Dict[str, Any]:
    """读取 Explore Artifact（按需取回）"""
    artifact_id = str(artifact_id or "").strip()
    work_id = str(work_id or "").strip()
    if not artifact_id or not work_id:
        return {"success": False, "error": "missing_artifact_id_or_work_id"}

    filepath = _work_dir(work_id) / f"{artifact_id}.json"
    if not filepath.exists():
        # 尝试 Redis 索引回查
        try:
            from app.core.redis import RedisClient
            index_data = await RedisClient.get(_artifact_index_key(artifact_id))
        except Exception:
            index_data = None

        if isinstance(index_data, dict):
            indexed_path = Path(index_data.get("path") or "")
            indexed_work_id = str(index_data.get("work_id") or "")
            if indexed_work_id and indexed_work_id != work_id:
                return {"success": False, "error": "work_id_mismatch", "artifact_id": artifact_id}
            if indexed_path.exists():
                filepath = indexed_path
        else:
            # 兼容旧路径：尝试其他 upload 根目录
            for root in _candidate_upload_roots()[1:]:
                candidate = root / work_id / f"{artifact_id}.json"
                if candidate.exists():
                    filepath = candidate
                    break
                legacy = root / "explore_artifacts" / work_id / f"{artifact_id}.json"
                if legacy.exists():
                    filepath = legacy
                    break

    if not filepath.exists():
        logger.warning(
            "[ExploreArtifact] 未找到 artifact 文件: %s (work_id=%s)",
            artifact_id,
            work_id
        )
        return {"success": False, "error": "not_found", "artifact_id": artifact_id}

    try:
        raw = filepath.read_text(encoding="utf-8")
        data = json.loads(raw)
    except Exception as exc:
        return {"success": False, "error": f"read_failed:{exc}", "artifact_id": artifact_id}

    # 权限校验
    if str(data.get("work_id") or "") != work_id:
        return {"success": False, "error": "work_id_mismatch", "artifact_id": artifact_id}
    stored_user_id = str(data.get("user_id") or "")
    if user_id and stored_user_id and str(user_id) != stored_user_id:
        return {"success": False, "error": "user_id_mismatch", "artifact_id": artifact_id}

    payload = data.get("payload", {})
    if mode == "metadata":
        return {
            "success": True,
            "artifact_id": artifact_id,
            "work_id": work_id,
            "user_id": stored_user_id,
            "created_at": data.get("created_at"),
            "meta": data.get("meta", {})
        }

    if mode == "summary":
        summary = ""
        if isinstance(payload, dict):
            summary = payload.get("explore_summary") or payload.get("context_for_task") or ""
        return {
            "success": True,
            "artifact_id": artifact_id,
            "summary": summary
        }

    # full
    if max_chars and isinstance(max_chars, int) and max_chars > 0:
        try:
            payload_text = json.dumps(payload, ensure_ascii=False)
        except Exception:
            payload_text = str(payload)
        truncated = len(payload_text) > max_chars
        return {
            "success": True,
            "artifact_id": artifact_id,
            "payload_text": payload_text[:max_chars] + ("..." if truncated else ""),
            "truncated": truncated
        }

    return {
        "success": True,
        "artifact_id": artifact_id,
        "payload": payload
    }
