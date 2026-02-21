"""
Agent 智能助手 API 路由

提供 Agent 相关的 RESTful API 接口，包括：
- Agent 会话管理（Session CRUD）
- V2 Agent 对话（DeepAgents 引擎）
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import logging
import json
import re
import uuid
import yaml
import redis
from pathlib import Path, PurePosixPath
from datetime import datetime, timedelta
from app.utils.datetime_utils import get_utc_now

from sqlalchemy.orm.attributes import flag_modified

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.core.config import settings
from app.models.user import User
from app.models.agent_session import AgentSession
from app.models.agent_session_message import AgentSessionMessage

router = APIRouter()
logger = logging.getLogger(__name__)

# ==================== Skills 元数据 ====================

SKILLS_ROOT = Path(__file__).resolve().parents[2] / "services" / "agent" / "skills"

_GROUP_LABELS = {
    # 原有
    "quality": "质量检查",
    "review": "创作分析",
    "statistics": "创作分析",
    "process": "创作辅助",
    # 新增
    "chinese-novel": "中文小说",
    "core": "故事诊断",
    "character": "角色塑造",
    "structure": "结构设计",
    "craft": "写作技法",
    "worldbuilding": "世界构建",
    "application": "应用工具",
}

_GROUP_ORDER = [
    "质量检查", "创作分析", "创作辅助",
    "中文小说", "故事诊断", "角色塑造", "结构设计",
    "写作技法", "世界构建", "应用工具",
]

DEFAULT_ENABLED_SKILL_COUNT = 5


def _load_all_skills() -> list[dict]:
    """从磁盘读取所有 SKILL.md，返回 skill 字典列表（不含 enabled 字段）。"""
    if not SKILLS_ROOT.is_dir():
        return []
    skills = []
    for skill_md in SKILLS_ROOT.rglob("SKILL.md"):
        try:
            content = skill_md.read_text(encoding="utf-8")
        except OSError:
            continue
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                try:
                    meta = yaml.safe_load(parts[1]) or {}
                except yaml.YAMLError:
                    continue
                group_key = skill_md.parent.parent.name
                raw_tools = meta.get("allowed-tools", [])
                allowed_tools = list(raw_tools) if isinstance(raw_tools, list) else []
                skills.append({
                    "name": meta.get("name", ""),
                    "description": meta.get("description", ""),
                    "group": _GROUP_LABELS.get(group_key, group_key),
                    "allowed_tools": allowed_tools,
                    "content": parts[2].strip(),
                })
    return skills


def _get_default_enabled_skills(all_skills: list[dict]) -> list[str]:
    """按 _GROUP_ORDER 排序后取前 N 个 skill 名称作为默认启用列表。"""
    group_rank = {g: i for i, g in enumerate(_GROUP_ORDER)}

    def sort_key(s: dict):
        return (group_rank.get(s["group"], 999), s["name"])

    sorted_skills = sorted(all_skills, key=sort_key)
    return [s["name"] for s in sorted_skills[:DEFAULT_ENABLED_SKILL_COUNT]]


@router.get("/skills", summary="列出可用 Agent Skills")
async def list_skills(
    current_user: User = Depends(get_current_active_user),
):
    """列出所有可用的 Agent Skills（前端技能面板数据源），含 enabled 状态。"""
    all_skills = _load_all_skills()

    # 读取用户偏好中的 enabled_skills
    prefs = current_user.preferences or {}
    enabled_skills: list[str] | None = prefs.get("enabled_skills")

    if enabled_skills is None:
        enabled_skills = _get_default_enabled_skills(all_skills)

    enabled_set = set(enabled_skills)
    for skill in all_skills:
        skill["enabled"] = skill["name"] in enabled_set

    logger.info(
        "[list_skills] user=%s total=%d enabled=%d enabled_names=%s",
        current_user.id, len(all_skills), len(enabled_set), sorted(enabled_set),
    )

    return all_skills


@router.post("/skills/{skill_name}/toggle", summary="切换 Skill 启用/禁用状态")
async def toggle_skill(
    skill_name: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """切换指定 Skill 的启用/禁用状态，持久化到用户 preferences.enabled_skills。"""
    # 校验 skill_name 合法性
    all_skills = _load_all_skills()
    valid_names = {s["name"] for s in all_skills}
    if skill_name not in valid_names:
        raise HTTPException(status_code=404, detail=f"Skill '{skill_name}' not found")

    # 读取当前 enabled_skills
    prefs: dict = dict(current_user.preferences or {})
    enabled_skills: list[str] | None = prefs.get("enabled_skills")

    if enabled_skills is None:
        enabled_skills = _get_default_enabled_skills(all_skills)

    # 切换
    if skill_name in enabled_skills:
        enabled_skills = [s for s in enabled_skills if s != skill_name]
        now_enabled = False
    else:
        enabled_skills.append(skill_name)
        now_enabled = True

    # 写回 preferences（flag_modified 确保 SQLAlchemy 检测到 JSONB 变更）
    prefs["enabled_skills"] = enabled_skills
    current_user.preferences = prefs
    flag_modified(current_user, "preferences")
    db.add(current_user)
    await db.flush()
    await db.commit()
    logger.info(
        "[toggle_skill] user=%s skill=%s enabled=%s saved_skills=%s",
        current_user.id, skill_name, now_enabled, enabled_skills,
    )

    return {"skill_name": skill_name, "enabled": now_enabled}


# ==================== Redis 连接池 ====================
_redis_pool = None
SESSION_CACHE_TTL_SECONDS = 30 * 24 * 60 * 60  # 30 天缓存 TTL，用于热数据

def get_redis_client():
    """获取同步Redis客户端（使用连接池）"""
    global _redis_pool

    # 🔧 修复：使用全局连接池，避免每次都创建新连接
    if _redis_pool is None:
        _redis_pool = redis.ConnectionPool(
            host='localhost',
            port=6379,
            db=1,  # 使用db1，避免与缓存服务冲突
            decode_responses=False,
            max_connections=10,  # 最大连接数
            socket_connect_timeout=5,  # 连接超时5秒
            socket_timeout=5,  # 操作超时5秒
        )
        logger.info("[Redis] 全局连接池已创建")

    return redis.Redis(connection_pool=_redis_pool)


# ==================== Request/response models ====================


# ==================== 会话管理（新增） ====================

class AgentSessionCreateRequest(BaseModel):
    title: Optional[str] = Field(None, description="会话标题")
    work_id: Optional[str] = Field(None, description="作品ID")
    chapter_id: Optional[str] = Field(None, description="章节ID")
    conversation_id: Optional[str] = Field(None, description="关联的对话ID（可选）")
    title_locked: Optional[bool] = Field(None, description="是否锁定标题")


class AgentSessionUpdateRequest(BaseModel):
    title: Optional[str] = Field(None, description="会话标题")
    title_locked: Optional[bool] = Field(None, description="是否锁定标题")


class AgentSessionResponse(BaseModel):
    session_id: str
    title: Optional[str] = None
    conversation_id: Optional[str] = None
    work_id: Optional[str] = None
    chapter_id: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    archived_at: Optional[str] = None
    expires_at: Optional[str] = None
    title_locked: Optional[bool] = None
    message_count: Optional[int] = None
    last_message_preview: Optional[str] = None

    model_config = {"from_attributes": True}


class AgentSessionListResponse(BaseModel):
    sessions: List[AgentSessionResponse]


class AgentSessionMessageResponse(BaseModel):
    id: str
    session_id: str
    role: str
    content: str
    metadata: Optional[Dict[str, Any]] = None
    token_usage: Optional[Dict[str, Any]] = None
    created_at: Optional[str] = None


# ==================== 会话管理 ====================

def _session_to_response(
    session: AgentSession,
    message_count: Optional[int] = None,
    last_message_preview: Optional[str] = None,
) -> Dict[str, Any]:
    return {
        "session_id": str(session.id),
        "title": session.title,
        "conversation_id": session.conversation_id,
        "work_id": str(session.work_id) if session.work_id else None,
        "chapter_id": str(session.chapter_id) if session.chapter_id else None,
        "created_at": session.created_at.isoformat() if session.created_at else None,
        "updated_at": session.updated_at.isoformat() if session.updated_at else None,
        "archived_at": session.archived_at.isoformat() if getattr(session, "archived_at", None) else None,
        "expires_at": session.expires_at.isoformat() if getattr(session, "expires_at", None) else None,
        "title_locked": bool(getattr(session, "title_locked", False)),
        "message_count": message_count if message_count is not None else 0,
        "last_message_preview": last_message_preview or "",
    }


def _session_cache_key(user_id: str, work_id: Optional[str], chapter_id: Optional[str], limit: int) -> str:
    return (
        f"agent:sessions:user:{user_id}:work:{work_id or 'all'}:"
        f"chapter:{chapter_id or 'all'}:limit:{limit}"
    )


def _session_detail_cache_key(session_id: str) -> str:
    return f"agent:session:{session_id}"


def _session_title_lock_key(session_id: str) -> str:
    return f"agent:session:title_locked:{session_id}"


def _cache_sessions(redis_client, key: str, sessions: List[Dict[str, Any]]) -> None:
    try:
        payload = json.dumps({"sessions": sessions}, ensure_ascii=False)
        redis_client.setex(key, SESSION_CACHE_TTL_SECONDS, payload.encode("utf-8"))
    except Exception as e:
        logger.warning(f"[Redis] set sessions cache failed: {e}")


def _read_sessions_from_cache(redis_client, key: str) -> Optional[List[Dict[str, Any]]]:
    try:
        cached = redis_client.get(key)
        if not cached:
            return None
        data = json.loads(cached)
        return data.get("sessions")
    except Exception as e:
        logger.warning(f"[Redis] read sessions cache failed: {e}")
        return None


def _invalidate_session_caches(redis_client, user_id: str) -> None:
    try:
        pattern = f"agent:sessions:user:{user_id}:*"
        for cache_key in redis_client.scan_iter(match=pattern):
            redis_client.delete(cache_key)
    except Exception as e:
        logger.warning(f"[Redis] invalidate sessions cache failed: {e}")


def _get_title_lock(redis_client, session_id: str) -> bool:
    try:
        val = redis_client.get(_session_title_lock_key(session_id))
        return bool(val and val.decode() != "0")
    except Exception as e:
        logger.warning(f"[Redis] read title lock failed: {e}")
        return False


def _set_title_lock(redis_client, session_id: str, locked: bool) -> None:
    try:
        key = _session_title_lock_key(session_id)
        if locked:
            redis_client.setex(key, SESSION_CACHE_TTL_SECONDS, "1")
        else:
            redis_client.delete(key)
    except Exception as e:
        logger.warning(f"[Redis] set title lock failed: {e}")


def _message_to_response(message: AgentSessionMessage) -> Dict[str, Any]:
    return {
        "id": str(message.id),
        "session_id": str(message.session_id),
        "role": message.role,
        "content": message.content,
        "metadata": message.message_metadata,
        "token_usage": message.token_usage,
        "created_at": message.created_at.isoformat() if message.created_at else None,
    }


def _is_valid_uuid(val: str) -> bool:
    """检查字符串是否为合法 UUID 格式"""
    try:
        uuid.UUID(val)
        return True
    except (ValueError, AttributeError):
        return False


async def _find_session_by_conversation(db: AsyncSession, user_id: str, conversation_id: Optional[str]) -> Optional[AgentSession]:
    if not conversation_id:
        return None
    stmt = select(AgentSession).where(
        AgentSession.user_id == user_id,
        AgentSession.conversation_id == conversation_id
    ).limit(1)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def _find_session(db: AsyncSession, user_id: str, session_id: str) -> Optional[AgentSession]:
    """按 UUID 主键或 conversation_id 查找会话（自动跳过非法 UUID）"""
    session = None
    if _is_valid_uuid(session_id):
        stmt = select(AgentSession).where(
            AgentSession.id == session_id,
            AgentSession.user_id == user_id,
        )
        result = await db.execute(stmt)
        session = result.scalar_one_or_none()
    if not session:
        session = await _find_session_by_conversation(db, user_id, session_id)
    return session


async def _persist_message(
    db: AsyncSession,
    session: Optional[AgentSession],
    role: str,
    content: str,
    metadata: Optional[Dict[str, Any]] = None,
    token_usage: Optional[Dict[str, Any]] = None
) -> None:
    if not session:
        return
    user_id = str(session.user_id)
    message = AgentSessionMessage(
        session_id=session.id,
        role=role,
        content=content,
        message_metadata=metadata,
        token_usage=token_usage,
    )
    db.add(message)
    # 触发 updated_at/expires_at 更新
    session.updated_at = datetime.utcnow()
    session.expires_at = datetime.utcnow() + timedelta(days=30)
    try:
        redis_client = get_redis_client()
        redis_client.delete(_session_detail_cache_key(str(session.id)))
        _invalidate_session_caches(redis_client, user_id)
    except Exception as cache_err:
        logger.warning(f"[SessionCache] invalidate failed: {cache_err}")


@router.post("/sessions", response_model=AgentSessionResponse, summary="创建 Agent 会话")
async def create_agent_session(
    payload: AgentSessionCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    title = payload.title or "New session"
    now = datetime.utcnow()
    expires_at = now + timedelta(days=30)
    user_id = str(current_user.id)

    # 避免同一 conversation_id 重复创建会话
    if payload.conversation_id:
        existing = await _find_session_by_conversation(db, user_id, payload.conversation_id)
        if existing:
            response = _session_to_response(existing)
            if payload.title_locked:
                try:
                    redis_client = get_redis_client()
                    _set_title_lock(redis_client, str(existing.id), True)
                except Exception as e:
                    logger.warning(f"[Redis] set title lock failed: {e}")
            return response

    # 验证 chapter_id 格式（如果提供）
    validated_chapter_id = None
    if payload.chapter_id:
        try:
            from uuid import UUID as PyUUID
            PyUUID(payload.chapter_id)  # 格式校验
            validated_chapter_id = payload.chapter_id
        except ValueError:
            logger.debug(f"[create_agent_session] chapter_id {payload.chapter_id} 格式无效，已忽略")

    new_session = AgentSession(
        user_id=current_user.id,
        title=title,
        conversation_id=payload.conversation_id,
        work_id=payload.work_id,
        chapter_id=validated_chapter_id,
        expires_at=expires_at,
        title_locked=payload.title_locked if payload.title_locked is not None else False,
    )

    db.add(new_session)
    await db.commit()
    await db.refresh(new_session)

    response = _session_to_response(new_session)
    if payload.title_locked:
        try:
            redis_client = get_redis_client()
            _set_title_lock(redis_client, str(new_session.id), True)
        except Exception as e:
            logger.warning(f"[Redis] set title lock failed: {e}")

    try:
        redis_client = get_redis_client()
        redis_client.setex(
            _session_detail_cache_key(response["session_id"]),
            SESSION_CACHE_TTL_SECONDS,
            json.dumps(response, ensure_ascii=False).encode("utf-8")
        )
        _invalidate_session_caches(redis_client, str(current_user.id))
    except Exception as e:
        logger.warning(f"[Redis] cache new session failed: {e}")

    return response


@router.get("/sessions", response_model=AgentSessionListResponse, summary="获取 Agent 会话列表")
async def list_agent_sessions(
    work_id: Optional[str] = Query(None, description="Filter by work ID"),
    chapter_id: Optional[str] = Query(None, description="Filter by chapter ID"),
    limit: int = Query(50, ge=1, le=200, description="返回数量上限"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    redis_client = get_redis_client()
    cache_key = _session_cache_key(str(current_user.id), work_id, chapter_id, limit)
    cached_sessions = _read_sessions_from_cache(redis_client, cache_key)
    if cached_sessions is not None:
        return {"sessions": cached_sessions}

    stmt = select(AgentSession).where(AgentSession.user_id == current_user.id)
    if work_id:
        stmt = stmt.where(AgentSession.work_id == work_id)
    if chapter_id:
        try:
            uuid.UUID(chapter_id)
            stmt = stmt.where(AgentSession.chapter_id == chapter_id)
        except ValueError:
            pass  # fs-N 格式，跳过 chapter_id 过滤
    stmt = stmt.where((AgentSession.expires_at.is_(None)) | (AgentSession.expires_at > datetime.utcnow()))

    stmt = stmt.order_by(AgentSession.updated_at.desc()).limit(limit)
    result = await db.execute(stmt)
    sessions = result.scalars().all()

    session_ids = [str(s.id) for s in sessions]
    counts_map: Dict[str, int] = {}
    previews_map: Dict[str, str] = {}

    if session_ids:
        count_rows = await db.execute(
            select(
                AgentSessionMessage.session_id,
                func.count(AgentSessionMessage.id)
            )
            .where(AgentSessionMessage.session_id.in_(session_ids))
            .group_by(AgentSessionMessage.session_id)
        )
        counts_map = {str(row[0]): int(row[1]) for row in count_rows.all()}

        preview_rows = await db.execute(
            select(
                AgentSessionMessage.session_id,
                AgentSessionMessage.content,
                func.row_number().over(
                    partition_by=AgentSessionMessage.session_id,
                    order_by=AgentSessionMessage.created_at.desc()
                ).label("rn")
            )
            .where(AgentSessionMessage.session_id.in_(session_ids))
        )
        for session_id, content, rn in preview_rows.all():
            if rn == 1 and content:
                previews_map[str(session_id)] = content[:80]

    redis_client = get_redis_client()
    response = []
    for s in sessions:
        sid = str(s.id)
        resp = _session_to_response(
            s,
            message_count=counts_map.get(sid, 0),
            last_message_preview=previews_map.get(sid, ""),
        )
        lock_redis = _get_title_lock(redis_client, resp["session_id"])
        resp["title_locked"] = resp["title_locked"] or lock_redis
        response.append(resp)
    _cache_sessions(redis_client, cache_key, response)
    return {"sessions": response}


@router.get("/sessions/{session_id}", response_model=AgentSessionResponse, summary="获取单个 Agent 会话详情")
async def get_agent_session_detail(
    session_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    redis_client = get_redis_client()
    cache_key = _session_detail_cache_key(session_id)
    try:
        cached = redis_client.get(cache_key)
        if cached:
            return json.loads(cached)
    except Exception as e:
        logger.warning(f"[Redis] read session detail cache failed: {e}")

    session = await _find_session(db, str(current_user.id), session_id)
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")

    # 统一用真实 UUID 作为缓存 key，避免同一 session 产生多个缓存条目
    cache_key = _session_detail_cache_key(str(session.id))
    redis_client = get_redis_client()
    response = _session_to_response(session)
    lock_redis = _get_title_lock(redis_client, response["session_id"])
    response["title_locked"] = response["title_locked"] or lock_redis
    try:
        redis_client.setex(
            cache_key,
            SESSION_CACHE_TTL_SECONDS,
            json.dumps(response, ensure_ascii=False).encode("utf-8")
        )
    except Exception as e:
        logger.warning(f"[Redis] cache session detail failed: {e}")

    return response


@router.patch("/sessions/{session_id}", response_model=AgentSessionResponse, summary="更新 Agent 会话")
async def update_agent_session(
    session_id: str,
    payload: AgentSessionUpdateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    session = await _find_session(db, str(current_user.id), session_id)

    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")

    updated = False
    if payload.title is not None:
        session.title = payload.title
        updated = True
        # 设置默认锁定
        if payload.title_locked is None:
            payload.title_locked = True

    if payload.title_locked is not None:
        try:
            redis_client = get_redis_client()
            _set_title_lock(redis_client, str(session.id), payload.title_locked)
        except Exception as e:
            logger.warning(f"[Redis] set title lock failed: {e}")
        session.title_locked = payload.title_locked

    if updated:
        session.updated_at = datetime.utcnow()
        session.expires_at = datetime.utcnow() + timedelta(days=30)
        db.add(session)
        await db.commit()
        await db.refresh(session)

        try:
            redis_client = get_redis_client()
            redis_client.delete(_session_detail_cache_key(str(session.id)))
            _invalidate_session_caches(redis_client, str(current_user.id))
        except Exception as e:
            logger.warning(f"[Redis] invalidate session caches failed: {e}")

    redis_client = get_redis_client()
    resp = _session_to_response(session)
    resp["title_locked"] = _get_title_lock(redis_client, resp["session_id"])
    return resp


@router.delete("/sessions/{session_id}", status_code=status.HTTP_204_NO_CONTENT, summary="删除 Agent 会话")
async def delete_agent_session(
    session_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    session = await _find_session(db, str(current_user.id), session_id)

    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")

    real_id = str(session.id)
    await db.delete(session)
    await db.commit()

    try:
        redis_client = get_redis_client()
        redis_client.delete(_session_detail_cache_key(real_id))
        redis_client.delete(_session_title_lock_key(real_id))
        _invalidate_session_caches(redis_client, str(current_user.id))
    except Exception as e:
        logger.warning(f"[Redis] invalidate session caches failed: {e}")

    return None


@router.get("/sessions/{session_id}/messages", response_model=List[AgentSessionMessageResponse], summary="获取会话消息列表")
async def get_agent_session_messages(
    session_id: str,
    limit: int = Query(50, ge=1, le=200, description="返回数量上限"),
    offset: int = Query(0, ge=0, description="偏移量"),
    order: str = Query("asc", regex="^(asc|desc)$", description="排序 asc/desc"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    session = await _find_session(db, str(current_user.id), session_id)
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")

    # 用实际的 session.id（UUID）查询消息
    actual_session_id = str(session.id)
    order_by = AgentSessionMessage.created_at.asc() if order == "asc" else AgentSessionMessage.created_at.desc()
    stmt = (
        select(AgentSessionMessage)
        .where(AgentSessionMessage.session_id == actual_session_id)
        .order_by(order_by)
        .offset(offset)
        .limit(limit)
    )
    result = await db.execute(stmt)
    messages = result.scalars().all()
    return [_message_to_response(m) for m in messages]



# ══════════════════════════════════════════════════════════════════
# V2 端点 — DeepAgents 引擎（Strangler Fig 模式，与旧端点共存）
# ══════════════════════════════════════════════════════════════════

import asyncio as _asyncio

# 待审批 backend 缓存："{user_id}:{conversation_id}" → BufferedFilesystemBackend
_pending_backends: dict[str, Any] = {}
# 并发锁：防止同一 work 的并发写入冲突
_work_locks: dict[str, _asyncio.Lock] = {}

# 全局 Redis checkpointer（跨请求共享，按 thread_id 隔离对话状态）
_checkpointer = None

async def _get_checkpointer():
    """获取或初始化全局 Redis Checkpointer（懒加载单例）。"""
    global _checkpointer
    if _checkpointer is None:
        try:
            from langgraph.checkpoint.redis.aio import AsyncRedisSaver
            cp = AsyncRedisSaver(
                redis_url=settings.REDIS_URL,
                ttl={"default_ttl": 60 * 24 * 7},  # 7 天后自动过期（分钟）
            )
            await cp.setup()
            _checkpointer = cp
            logger.info("[Checkpointer] Redis checkpointer 初始化成功")
        except Exception as e:
            logger.warning(f"[Checkpointer] Redis 初始化失败: {e}")
            raise
    return _checkpointer


def _pending_path(user_id: str, conversation_id: str) -> Path:
    """返回持久化 JSON 文件路径：data/users/.pending/{user_id}_{conversation_id}.json"""
    from app.services.agent.deep_agent import DATA_ROOT
    return DATA_ROOT / ".pending" / f"{user_id}_{conversation_id}.json"


def _save_pending(key: str, backend) -> None:
    """将 backend 持久化到 JSON（静默失败）。"""
    user_id, conv_id = key.split(":", 1)
    try:
        backend.save_pending(_pending_path(user_id, conv_id))
    except Exception as e:
        logger.warning(f"[Pending] save failed for {key}: {e}")


def _load_pending(key: str):
    """从 JSON 恢复 backend 到内存缓存，返回 backend 或 None。"""
    from app.services.agent.deep_agent.buffered_backend import BufferedFilesystemBackend
    user_id, conv_id = key.split(":", 1)
    try:
        backend = BufferedFilesystemBackend.load_pending(_pending_path(user_id, conv_id))
        if backend:
            _pending_backends[key] = backend
        return backend
    except Exception as e:
        logger.warning(f"[Pending] load failed for {key}: {e}")
        return None


def _delete_pending(key: str) -> None:
    """删除持久化 JSON 文件（静默失败）。"""
    user_id, conv_id = key.split(":", 1)
    try:
        path = _pending_path(user_id, conv_id)
        if path.is_file():
            path.unlink()
    except Exception as e:
        logger.warning(f"[Pending] delete failed for {key}: {e}")


def _buffer_op_to_change(op, index: int) -> dict:
    """将单条 BufferOp 转换为 get_changes() 兼容的 dict，供实时 revision 使用。"""
    from app.services.agent.deep_agent.frontmatter import parse_chapter

    item: dict = {"index": index, "op_type": op.op_type, "path": op.path}
    if op.op_type == "write":
        item["content_preview"] = (op.content or "")[:200]
        parsed = parse_chapter(op.content or "")
        item["new_string"] = parsed["content"]
        if parsed["title"]:
            item["chapter_title"] = parsed["title"]
    elif op.op_type == "edit":
        item["old_string"] = op.old_string
        item["new_string"] = op.new_string
    return item


class V2ChatRequest(BaseModel):
    """V2 Agent 对话请求"""
    message: str = Field(..., min_length=1)
    work_id: str = Field(...)
    conversation_id: Optional[str] = Field(None)
    knowledge_files: Optional[List[str]] = Field(None)
    quoted_text: Optional[str] = Field(None, description="用户在编辑器中选中的引用文本")
    skill: Optional[str] = Field(
        None,
        description="用户主动选择的 Skill 名称（如 chapter-review）",
        pattern=r"^[a-z][a-z0-9\-]{0,63}$",
    )


class V2ChangesResponse(BaseModel):
    """待审批改动响应"""
    conversation_id: str
    changes: List[Dict[str, Any]]


@router.post("/v2/chat/stream", summary="V2 Agent 对话（DeepAgents 引擎）")
async def agent_v2_chat_stream(
    request: V2ChatRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """使用 DeepAgents 引擎的流式对话端点。"""
    from app.services.agent.deep_agent.agent_factory import create_writing_agent
    from app.services.agent.deep_agent.event_translator import (
        StepCounter,
        translate_event,
        make_completion_event,
        make_revision_event,
    )

    user_id = str(current_user.id)
    conversation_id = request.conversation_id or str(uuid.uuid4())

    # 查询 Work
    from app.models.work import Work
    stmt = select(Work).where(
        Work.id == request.work_id,
        Work.author_id == current_user.id,
    )
    result = await db.execute(stmt)
    work = result.scalar_one_or_none()
    if not work:
        raise HTTPException(status_code=404, detail="Work not found")

    async def event_generator():
        try:
            counter = StepCounter()

            # 获取 per-work 锁
            work_key = f"{user_id}:{request.work_id}"
            if work_key not in _work_locks:
                _work_locks[work_key] = _asyncio.Lock()

            async with _work_locks[work_key]:
                # 创建 Agent + Backend（传入 checkpointer 实现跨轮次记忆）
                checkpointer = await _get_checkpointer()
                agent, backend = create_writing_agent(work, user_id, checkpointer=checkpointer)

                # 构建输入（注入知识库引用）
                user_content = request.message
                if request.knowledge_files:
                    from app.services.agent.deep_agent import DATA_ROOT
                    work_dir = DATA_ROOT / user_id / "works" / request.work_id
                    ref_parts = []
                    for rel_path in request.knowledge_files:
                        fp = (work_dir / rel_path).resolve()
                        # 安全检查：防止目录穿越
                        if not str(fp).startswith(str(work_dir.resolve())):
                            continue
                        if fp.exists() and fp.is_file():
                            try:
                                text = fp.read_text("utf-8")
                                ref_parts.append(f"<reference path=\"{rel_path}\">\n{text}\n</reference>")
                            except Exception:
                                logger.warning(f"Failed to read knowledge file: {rel_path}")
                    if ref_parts:
                        user_content = "\n".join(ref_parts) + "\n\n" + request.message

                # 注入用户引用文本
                if request.quoted_text:
                    user_content = f"<quote>\n{request.quoted_text}\n</quote>\n\n{user_content}"

                # 注入用户主动选择的 Skill 指令
                loaded_skill_name = None
                if request.skill:
                    # 白名单校验：skill 名称必须对应实际存在的 SKILL.md
                    valid_skill = False
                    for skill_md in SKILLS_ROOT.rglob("SKILL.md"):
                        try:
                            raw = skill_md.read_text(encoding="utf-8")
                            if raw.startswith("---"):
                                parts = raw.split("---", 2)
                                if len(parts) >= 3:
                                    meta = yaml.safe_load(parts[1]) or {}
                                    if meta.get("name") == request.skill:
                                        valid_skill = True
                                        break
                        except Exception:
                            continue

                    if valid_skill:
                        loaded_skill_name = request.skill
                        # raw 已在验证循环中读取，提取正文（跳过 YAML frontmatter）
                        skill_body = raw.split("---", 2)[2].strip() if raw.startswith("---") else raw
                        user_content = (
                            f"<directive>\n"
                            f"用户选择了技能「{request.skill}」。\n"
                            f"你 **必须严格** 按照以下技能 SOP 执行任务，"
                            f"包括输出格式、评审维度、分级标准等所有细节。\n\n"
                            f"{skill_body}\n"
                            f"</directive>\n\n"
                            f"{user_content}"
                        )
                    else:
                        logger.warning("Unknown skill requested: %s", request.skill)

                input_msg = {"messages": [{"role": "user", "content": user_content}]}
                config = {
                    "configurable": {"thread_id": conversation_id},
                    "recursion_limit": 500,
                }

                # 发送 agent_header
                header = {
                    "type": "agent_header",
                    "data": {"name": "文枢AI", "badge": "v2"},
                    "timestamp": get_utc_now().isoformat(),
                }
                yield f"data: {json.dumps(header, ensure_ascii=False)}\n\n"

                # 发送 skill_loaded 事件（仅当用户选择了有效技能时）
                if loaded_skill_name:
                    skill_event = {
                        "type": "skill_loaded",
                        "skill_name": loaded_skill_name,
                        "timestamp": get_utc_now().isoformat(),
                    }
                    yield f"data: {json.dumps(skill_event, ensure_ascii=False)}\n\n"

                # 流式运行 Agent（实时发送 revision）
                _last_buffer_len = 0

                async for event in agent.astream_events(
                    input_msg, config=config, version="v2"
                ):
                    translated = translate_event(event, counter)
                    if translated:
                        yield f"data: {json.dumps(translated, ensure_ascii=False)}\n\n"

                    # 🆕 实时发送 revision：on_tool_end 后检测 buffer 新增
                    kind = event.get("event", "")
                    if kind == "on_tool_end" and len(backend._buffer) > _last_buffer_len:
                        # 从 translated step_complete 事件提取精确 step_id（防嵌套调用错位）
                        _step_id = (translated or {}).get("step_id", counter.current)
                        # 逐条发送新增的 buffer 操作
                        while _last_buffer_len < len(backend._buffer):
                            op_dict = _buffer_op_to_change(backend._buffer[_last_buffer_len], _last_buffer_len)
                            _last_buffer_len += 1
                            # 补充 chapter_id
                            m = re.search(r'chapters/(\d+)-[^/]+\.md', op_dict["path"])
                            if m:
                                op_dict["chapter_id"] = f"fs-{int(m.group(1))}"
                            else:
                                clean_path = op_dict["path"].lstrip("/")
                                op_dict["chapter_id"] = f"doc:{clean_path}"
                                if not op_dict.get("chapter_title"):
                                    op_dict["chapter_title"] = PurePosixPath(op_dict["path"]).stem
                            rev = make_revision_event(op_dict)
                            rev["step_id"] = _step_id
                            yield f"data: {json.dumps(rev, ensure_ascii=False)}\n\n"

                # Agent 完成：获取改动列表（用于 completion 统计和 pending 缓存）
                changes = backend.get_changes()

                # 发送 completion 事件
                completion = make_completion_event(changes)
                yield f"data: {json.dumps(completion, ensure_ascii=False)}\n\n"

                # 缓存 backend 待审批（绑定 user_id 隔离）
                if changes:
                    backend_key = f"{user_id}:{conversation_id}"
                    _pending_backends[backend_key] = backend
                    _save_pending(backend_key, backend)

                # 发送 done 事件
                done_event = {
                    "type": "done",
                    "conversation_id": conversation_id,
                    "has_changes": len(changes) > 0,
                }
                yield f"data: {json.dumps(done_event, ensure_ascii=False)}\n\n"

        except Exception as e:
            logger.error(f"[V2 Agent] Error: {e}", exc_info=True)
            error_event = {
                "type": "error",
                "error": str(e),
                "error_type": type(e).__name__,
            }
            yield f"data: {json.dumps(error_event, ensure_ascii=False)}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
            "X-Conversation-Id": conversation_id,
        },
    )


@router.get("/v2/changes/{conversation_id}", summary="获取待审批改动")
async def get_v2_changes(
    conversation_id: str,
    current_user: User = Depends(get_current_active_user),
):
    """获取指定对话的待审批改动列表。"""
    backend_key = f"{current_user.id}:{conversation_id}"
    backend = _pending_backends.get(backend_key) or _load_pending(backend_key)
    if not backend:
        return V2ChangesResponse(conversation_id=conversation_id, changes=[])
    return V2ChangesResponse(
        conversation_id=conversation_id,
        changes=backend.get_changes(),
    )


@router.post("/v2/changes/{conversation_id}/accept", summary="全部接受改动")
async def accept_v2_changes(
    conversation_id: str,
    current_user: User = Depends(get_current_active_user),
):
    """全部接受：将缓冲区写入磁盘。"""
    backend_key = f"{current_user.id}:{conversation_id}"
    backend = _pending_backends.pop(backend_key, None)
    if not backend:
        backend = _load_pending(backend_key)
        _pending_backends.pop(backend_key, None)
    if not backend:
        raise HTTPException(status_code=404, detail="No pending changes")

    affected = backend.flush()
    _delete_pending(backend_key)

    # flush 后更新向量索引（直接读磁盘文件，而非 backend.read()）
    from app.services.agent.deep_agent.rag_tool import update_chapter_vectors
    from app.services.agent.deep_agent.frontmatter import parse_chapter

    for path in affected:
        if "/chapters/" in path:
            try:
                disk_path = backend._resolve_path(path)
                raw = disk_path.read_text(encoding="utf-8")
                parsed = parse_chapter(raw)
                work_id = Path(str(backend.cwd)).name
                update_chapter_vectors(work_id, path, parsed["content"])
            except Exception as e:
                logger.warning(f"[V2] Failed to update vectors for {path}: {e}")

    return {"status": "accepted", "affected_paths": affected}


@router.post("/v2/changes/{conversation_id}/reject", summary="全部拒绝改动")
async def reject_v2_changes(
    conversation_id: str,
    current_user: User = Depends(get_current_active_user),
):
    """全部拒绝：丢弃缓冲区。"""
    backend_key = f"{current_user.id}:{conversation_id}"
    backend = _pending_backends.pop(backend_key, None)
    if not backend:
        backend = _load_pending(backend_key)
        _pending_backends.pop(backend_key, None)
    if not backend:
        raise HTTPException(status_code=404, detail="No pending changes")
    backend.discard()
    _delete_pending(backend_key)
    return {"status": "rejected"}


@router.post("/v2/changes/{conversation_id}/accept/{index}", summary="单个接受改动")
async def accept_v2_single_change(
    conversation_id: str,
    index: int,
    current_user: User = Depends(get_current_active_user),
):
    """单个接受：将指定操作写入磁盘。"""
    backend_key = f"{current_user.id}:{conversation_id}"
    backend = _pending_backends.get(backend_key) or _load_pending(backend_key)
    if not backend:
        raise HTTPException(status_code=404, detail="No pending changes")

    path = backend.flush_single(index)
    if path is None:
        raise HTTPException(status_code=400, detail="Invalid change index or has unresolved dependencies")

    # 缓冲区清空后移除
    if not backend.get_changes():
        _pending_backends.pop(backend_key, None)
        _delete_pending(backend_key)
    else:
        _save_pending(backend_key, backend)

    return {"status": "accepted", "path": path}


@router.post("/v2/changes/{conversation_id}/reject/{index}", summary="单个拒绝改动")
async def reject_v2_single_change(
    conversation_id: str,
    index: int,
    current_user: User = Depends(get_current_active_user),
):
    """单个拒绝：丢弃指定操作。"""
    backend_key = f"{current_user.id}:{conversation_id}"
    backend = _pending_backends.get(backend_key) or _load_pending(backend_key)
    if not backend:
        raise HTTPException(status_code=404, detail="No pending changes")

    ok = backend.discard_single(index)
    if not ok:
        raise HTTPException(status_code=400, detail="Invalid change index")

    # 缓冲区清空后移除
    if not backend.get_changes():
        _pending_backends.pop(backend_key, None)
        _delete_pending(backend_key)
    else:
        _save_pending(backend_key, backend)

    return {"status": "rejected"}
