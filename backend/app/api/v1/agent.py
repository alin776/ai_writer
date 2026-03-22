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
import time as _time
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
    "core": "故事诊断",
    "character": "角色塑造",
    "structure": "结构设计",
    "craft": "写作技法",
    "worldbuilding": "世界构建",
    "application": "实用工具",
    "chinese-novel": "中文创作",
}

_GROUP_ORDER = [
    "故事诊断", "角色塑造", "结构设计",
    "写作技法", "世界构建", "中文创作", "实用工具",
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
                # 跳过系统级 Skill（不在前端技能面板展示）
                skill_meta = meta.get("metadata") or {}
                if isinstance(skill_meta, dict) and skill_meta.get("type") == "system":
                    continue
                group_key = skill_md.parent.parent.name
                raw_tools = meta.get("allowed-tools", "")
                if isinstance(raw_tools, str):
                    allowed_tools = [t.strip(",") for t in raw_tools.split() if t.strip(",")]
                elif isinstance(raw_tools, list):
                    allowed_tools = [str(t) for t in raw_tools]
                else:
                    allowed_tools = []
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
SESSION_CACHE_TTL_SECONDS = 2 * 24 * 60 * 60  # 2 天缓存 TTL，用于热数据

def get_redis_client():
    """获取同步Redis客户端（使用连接池）"""
    global _redis_pool

    if _redis_pool is None:
        # 从 settings.REDIS_URL 构建连接池，将 db 切换为 1 避免与缓存服务冲突
        base_url = settings.REDIS_URL.rsplit("/", 1)[0]  # 去掉尾部 /N
        pool_url = f"{base_url}/1"
        _redis_pool = redis.ConnectionPool.from_url(
            pool_url,
            decode_responses=False,
            max_connections=10,
            socket_connect_timeout=5,
            socket_timeout=5,
        )
        logger.info("[Redis] 全局连接池已创建: %s", pool_url)

    return redis.Redis(connection_pool=_redis_pool)


# ==================== SSE 事件缓存（断线重连） ====================

_SSE_CACHE_TTL = 600  # 10 分钟
_SSE_CACHE_PREFIX = "sse:events:"
# 跟踪活跃的 SSE 流（conversation_id → set[asyncio.Queue]），支持多订阅者
import asyncio as _asyncio
_active_streams: dict[str, set[_asyncio.Queue]] = {}


def _sse_cache_key(conversation_id: str) -> str:
    return f"{_SSE_CACHE_PREFIX}{conversation_id}"


_SSE_CACHE_MAX_EVENTS = 2000  # 单个会话最多缓存事件数


def _cache_sse_event(conversation_id: str, event_id: int, raw_sse: str) -> None:
    """将单条 SSE 事件缓存到 Redis List（同步，在 yield 时调用）。"""
    try:
        r = get_redis_client()
        key = _sse_cache_key(conversation_id)
        pipe = r.pipeline(transaction=False)
        pipe.rpush(key, raw_sse.encode("utf-8"))
        pipe.ltrim(key, -_SSE_CACHE_MAX_EVENTS, -1)
        pipe.expire(key, _SSE_CACHE_TTL)
        # 刷新 owner key TTL（防止长 Agent 运行超过初始 TTL 后 resume 被 403）
        pipe.expire(f"sse:owner:{conversation_id}", _SSE_CACHE_TTL)
        pipe.execute()
    except Exception:
        pass  # 缓存失败不影响主流程


def _broadcast_to_subscribers(conversation_id: str, frame: str) -> None:
    """向所有订阅者队列推送事件帧。队列满时移除该订阅者（慢客户端）。"""
    subscribers = _active_streams.get(conversation_id)
    if not subscribers:
        return
    dead: list[_asyncio.Queue] = []
    for q in list(subscribers):  # 复制迭代，防止并发修改
        try:
            q.put_nowait(frame)
        except _asyncio.QueueFull:
            dead.append(q)
    for q in dead:
        subscribers.discard(q)


def _get_cached_events(conversation_id: str, after_id: int) -> list[str]:
    """从 Redis 获取 event_id > after_id 的所有缓存事件。

    由于 LTRIM 可能截断早期事件，无法依赖 List 索引与 event_id 的简单映射。
    改为获取全部缓存事件，通过帧内 id 字段过滤。
    """
    try:
        r = get_redis_client()
        key = _sse_cache_key(conversation_id)
        raw_list = r.lrange(key, 0, -1)
        result = []
        for item in raw_list:
            frame = item.decode("utf-8") if isinstance(item, bytes) else item
            # 从帧中提取 event_id，跳过 <= after_id 的事件
            frame_id = 0
            for fline in frame.split("\n"):
                if fline.startswith("id: "):
                    try:
                        frame_id = int(fline[4:].strip())
                    except ValueError:
                        pass
                    break
            if frame_id > after_id:
                result.append(frame)
        return result
    except Exception:
        return []


def _mark_stream_done(conversation_id: str) -> None:
    """标记流已完成（在 Redis 中设置标志）。"""
    try:
        r = get_redis_client()
        r.set(f"sse:done:{conversation_id}", "1", ex=_SSE_CACHE_TTL)
    except Exception:
        pass


def _is_stream_done(conversation_id: str) -> bool:
    """检查流是否已完成。"""
    try:
        r = get_redis_client()
        return r.exists(f"sse:done:{conversation_id}") > 0
    except Exception:
        return False


def _set_stream_owner(conversation_id: str, user_id: str) -> None:
    """记录 SSE 流的所有者（用于 resume 端点鉴权）。"""
    try:
        r = get_redis_client()
        r.set(f"sse:owner:{conversation_id}", user_id, ex=_SSE_CACHE_TTL)
    except Exception:
        pass


def _check_stream_owner(conversation_id: str, user_id: str) -> bool:
    """校验当前用户是否为该 SSE 流的所有者。"""
    try:
        r = get_redis_client()
        owner = r.get(f"sse:owner:{conversation_id}")
        if owner is None:
            return False
        owner_str = owner.decode("utf-8") if isinstance(owner, bytes) else owner
        return owner_str == user_id
    except Exception:
        return False


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

# 待审批 backend 缓存："{user_id}:{conversation_id}" → BufferedFilesystemBackend
_pending_backends: dict[str, Any] = {}
_pending_access_times: dict[str, float] = {}  # key → 最后访问的 time.time() 时间戳
_PENDING_TTL = 30 * 60   # 30 分钟无访问则从内存驱逐（磁盘 JSON 保留）
_PENDING_MAX_SIZE = 50    # 内存中最多保留 50 个 backend（LRU 兜底）

# 并发锁：防止同一 work 的并发写入冲突
_work_locks: dict[str, _asyncio.Lock] = {}
_work_lock_access_times: dict[str, float] = {}  # key → 最后使用的 time.time() 时间戳
_WORK_LOCK_TTL = 60 * 60  # 1 小时无使用则清理


def _evict_stale_pending() -> None:
    """驱逐内存中过期的 pending backends（磁盘 JSON 保留），并清理闲置的 work locks。"""
    try:
        now = _time.time()

        # ── 1. TTL 驱逐：清理超过 30 分钟无访问的 pending backends ──
        expired_keys = [
            k for k, t in _pending_access_times.items()
            if now - t > _PENDING_TTL
        ]
        for k in expired_keys:
            _pending_backends.pop(k, None)
            _pending_access_times.pop(k, None)

        # ── 2. LRU 兜底：超过 max size 时淘汰最老的 ──
        overflow = len(_pending_backends) - _PENDING_MAX_SIZE
        if overflow > 0:
            sorted_keys = sorted(_pending_access_times, key=_pending_access_times.get)
            for k in sorted_keys[:overflow]:
                _pending_backends.pop(k, None)
                _pending_access_times.pop(k, None)
            expired_keys.extend(sorted_keys[:overflow])

        if expired_keys:
            logger.info("[Pending] evicted %d stale entries from memory", len(expired_keys))

        # ── 3. 顺便清理闲置的 work locks ──
        stale_locks = [
            k for k, t in _work_lock_access_times.items()
            if now - t > _WORK_LOCK_TTL
            and (k not in _work_locks or not _work_locks[k].locked())
        ]
        for k in stale_locks:
            _work_locks.pop(k, None)
            _work_lock_access_times.pop(k, None)
        if stale_locks:
            logger.info("[WorkLocks] cleaned %d stale locks", len(stale_locks))
    except Exception as e:
        logger.warning("[Eviction] cleanup failed (non-fatal): %s", e)

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
                ttl={"default_ttl": 60 * 24 * 3},  # 3 天后自动过期（分钟）
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
            _pending_access_times[key] = _time.time()
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


async def _sync_worldview_cards_from_pending(
    db: AsyncSession,
    backend: Any,
    touched_paths: list[str],
) -> dict[str, Any] | None:
    """Best-effort: debounced knowledge->worldview sync for AI-applied edits."""
    if not touched_paths:
        return None

    from app.services.worldview_knowledge_bridge import WorldviewKnowledgeBridge
    from app.services.knowledge_sync_scheduler import request_worldview_sync

    if not WorldviewKnowledgeBridge.has_tracked_path(touched_paths):
        return None

    work_dir = Path(str(getattr(backend, "cwd", "")))
    if not work_dir.name:
        return None

    work_id = work_dir.name
    return await request_worldview_sync(
        db=db,
        work_id=work_id,
        work_dir=work_dir,
        touched_paths=touched_paths,
        sync_mode=settings.WORLDVIEW_KNOWLEDGE_SYNC_MODE,
    )


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
    elif op.op_type == "rename":
        target_path = str(op.new_path or op.path)
        item["old_path"] = op.path
        item["new_path"] = target_path
        item["path"] = target_path
        item["content_preview"] = f"{op.path} -> {target_path}"
        item["old_title"] = PurePosixPath(op.path).stem
        item["new_title"] = PurePosixPath(target_path).stem
        item["chapter_title"] = item["new_title"]
        item["old_string"] = ""
        item["new_string"] = ""
    elif op.op_type == "delete":
        item["old_string"] = op.old_string or ""
        item["new_string"] = ""
        item["content_preview"] = (op.old_string or "")[:200]
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

    # ── 改动 A：积分预检（SSE 流开始之前同步返回 402） ──
    token_usage_summary: dict | None = None
    if settings.CREDITS_ENABLED and not current_user.is_admin:
        from decimal import Decimal as _Decimal
        from app.services.credits.credit_service import CreditService as _CreditSvc
        _credit_svc = _CreditSvc(db)
        _MIN_V2_CREDITS = _Decimal("500")
        _is_ok, _balance = await _credit_svc.check_sufficient(current_user.id, _MIN_V2_CREDITS)
        if not _is_ok:
            raise HTTPException(status_code=402, detail=f"积分余额不足，当前 {_balance}")

    # 在 generator 外同步设置 owner + 订阅者集合，确保即使 generator 延迟执行也能 resume
    _set_stream_owner(conversation_id, user_id)
    _active_streams.setdefault(conversation_id, set())

    async def event_generator():
        usage_cb = None
        _stream_start = None
        backend = None
        _event_id = 0  # SSE 事件编号（断线重连用）

        # 设置 Agent 计费累加器（合并内部多次 LLM 调用为 1 条记录）
        from app.core.billing_context import AgentBillingAccumulator, set_agent_billing, agent_billing_ctx
        billing_accumulator = AgentBillingAccumulator()
        _billing_token = set_agent_billing(billing_accumulator)

        def _emit_sse(data_str: str) -> str:
            """为 SSE 事件添加 id 字段并缓存到 Redis，返回完整 SSE 帧。"""
            nonlocal _event_id
            _event_id += 1
            frame = f"id: {_event_id}\ndata: {data_str}\n\n"
            _cache_sse_event(conversation_id, _event_id, frame)
            _broadcast_to_subscribers(conversation_id, frame)
            return frame
        try:
            counter = StepCounter()

            # 获取 per-work 锁
            work_key = f"{user_id}:{request.work_id}"
            if work_key not in _work_locks:
                _work_locks[work_key] = _asyncio.Lock()
            _work_lock_access_times[work_key] = _time.time()

            async with _work_locks[work_key]:
                # 创建 Agent + Backend（传入 checkpointer 实现跨轮次记忆）
                checkpointer = await _get_checkpointer()

                # ── 改动 B：注入 Token 用量收集 callback ──
                from langchain_core.callbacks.base import BaseCallbackHandler as _BCH
                from langchain_core.outputs import LLMResult as _LLMResult, ChatGeneration as _ChatGen
                from langchain_core.messages import AIMessage as _AIMsg
                import time as _time

                class _UsageCollector(_BCH):
                    """轻量 callback：按 model_name 聚合 usage_metadata（兼容 Responses API）。"""
                    def __init__(self, default_model: str):
                        super().__init__()
                        self.usage_metadata: dict = {}  # {model_name: UsageMetadata}
                        self._default_model = default_model

                    def on_llm_end(self, response: _LLMResult, **kwargs) -> None:
                        try:
                            gen = response.generations[0][0]
                        except IndexError:
                            return
                        if not isinstance(gen, _ChatGen) or not isinstance(gen.message, _AIMsg):
                            return
                        um = gen.message.usage_metadata
                        if not um:
                            return
                        name = (gen.message.response_metadata or {}).get("model_name") or self._default_model
                        if name in self.usage_metadata:
                            from langchain_core.callbacks.usage import add_usage
                            self.usage_metadata[name] = add_usage(self.usage_metadata[name], um)
                        else:
                            self.usage_metadata[name] = um

                usage_cb = _UsageCollector(default_model=settings.OPENAI_MODEL)
                agent, backend = create_writing_agent(
                    work, user_id, checkpointer=checkpointer, callbacks=[usage_cb],
                )
                _stream_start = _time.time()

                # 构建输入（知识文件由模型通过工具按需读取）
                user_content = request.message
                if request.knowledge_files:
                    from app.services.agent.deep_agent import DATA_ROOT

                    work_dir = DATA_ROOT / user_id / "works" / request.work_id
                    ref_parts: list[str] = []
                    seen_paths: set[str] = set()
                    for raw_path in request.knowledge_files:
                        rel_path = (raw_path or "").strip().replace("\\", "/")
                        while rel_path.startswith("./"):
                            rel_path = rel_path[2:]
                        rel_path = rel_path.lstrip("/")
                        if not rel_path:
                            continue
                        lower_rel = rel_path.lower()
                        if lower_rel in seen_paths:
                            continue
                        seen_paths.add(lower_rel)

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
                                        # 系统级 Skill 不能通过前端 skill 参数手动触发
                                        skill_meta = meta.get("metadata") or {}
                                        if isinstance(skill_meta, dict) and skill_meta.get("type") == "system":
                                            break
                                        valid_skill = True
                                        break
                        except Exception:
                            continue

                    if valid_skill:
                        loaded_skill_name = request.skill
                        loaded_skill_dir = skill_md.parent.name   # 目录名，用于 skill_switched 去重
                        # raw 已在验证循环中读取，提取正文（跳过 YAML frontmatter）
                        skill_body = raw.split("---", 2)[2].strip() if raw.startswith("---") else raw

                        # 检测 Skill 是否附带脚本工具，生成强制性使用指令
                        skill_scripts_dir = skill_md.parent / "scripts"
                        script_instruction = ""
                        if skill_scripts_dir.is_dir():
                            py_files = list(skill_scripts_dir.glob("*.py"))
                            if py_files:
                                script_names = ", ".join(f.name for f in py_files)
                                script_instruction = (
                                    f"\n\n**脚本工具使用规则（必须遵守）：**\n"
                                    f"此技能附带以下分析脚本：{script_names}\n"
                                    f"- 在执行诊断或分析任务时，**必须先使用 execute 工具运行相关脚本**获取量化数据\n"
                                    f"- 脚本调用方式见下方技能文档中的「可用工具」章节\n"
                                    f"- 脚本输出的量化数据应作为你分析的依据，而非仅凭 LLM 推断\n"
                                    f"- 如果脚本执行失败，在回复中说明失败原因，然后用你自己的分析能力补充\n"
                                )

                        user_content = (
                            f"<directive>\n"
                            f"用户选择了技能「{request.skill}」作为主要技能。\n"
                            f"请严格按照此技能的 SOP 执行任务，包括输出格式、评审维度、分级标准等所有细节。\n\n"
                            f"**技能路由规则：**\n"
                            f"- 如果在执行过程中，此技能的「集成」「交接」或「相关技能」部分建议切换到其他技能，"
                            f"你可以使用 read_file 读取目标技能的 SKILL.md 并遵循其 SOP\n"
                            f"- 切换前用一句话告知用户你将切换到哪个技能以及原因\n"
                            f"- 切换后，按照目标技能的 SOP 严格执行\n"
                            f"{script_instruction}\n"
                            f"{skill_body}\n"
                            f"</directive>\n\n"
                            f"{user_content}"
                        )
                    else:
                        logger.warning("Unknown skill requested: %s", request.skill)

                input_msg = {"messages": [{"role": "user", "content": user_content}]}
                config = {
                    "configurable": {"thread_id": conversation_id},
                    "recursion_limit": 150,
                }

                # 发送 agent_header（含 conversation_id，断线重连的关键：前端需尽早获得此 ID）
                header = {
                    "type": "agent_header",
                    "conversation_id": conversation_id,
                    "data": {"name": "文枢AI", "badge": "v2"},
                    "timestamp": get_utc_now().isoformat(),
                }
                yield _emit_sse(json.dumps(header, ensure_ascii=False))

                # 发送 skill_loaded 事件（仅当用户选择了有效技能时）
                if loaded_skill_name:
                    skill_event = {
                        "type": "skill_loaded",
                        "skill_name": loaded_skill_name,
                        "timestamp": get_utc_now().isoformat(),
                    }
                    yield _emit_sse(json.dumps(skill_event, ensure_ascii=False))

                # 流式运行 Agent（实时发送 revision）
                _last_buffer_len = 0
                # Skill 切换去重集合（目录名）
                emitted_skills: set[str] = set()
                if loaded_skill_name:
                    emitted_skills.add(loaded_skill_dir)

                # ── SSE 心跳保活（防 Cloudflare 100s 空闲超时） ──
                _HEARTBEAT_INTERVAL = 15  # 秒
                _SENTINEL_DONE = object()
                _SENTINEL_HEARTBEAT = object()
                _event_queue: _asyncio.Queue = _asyncio.Queue()

                async def _stream_producer():
                    """后台任务：将 Agent 事件逐个放入队列"""
                    try:
                        async for ev in agent.astream_events(
                            input_msg, config=config, version="v2"
                        ):
                            await _event_queue.put(ev)
                    except Exception as exc:
                        await _event_queue.put(exc)
                    finally:
                        await _event_queue.put(_SENTINEL_DONE)

                async def _heartbeat_producer():
                    """后台任务：每 N 秒放入心跳哨兵"""
                    try:
                        while True:
                            await _asyncio.sleep(_HEARTBEAT_INTERVAL)
                            await _event_queue.put(_SENTINEL_HEARTBEAT)
                    except _asyncio.CancelledError:
                        pass

                _producer_task = _asyncio.create_task(_stream_producer())
                _heartbeat_task = _asyncio.create_task(_heartbeat_producer())

                try:
                    while True:
                        item = await _event_queue.get()
                        if item is _SENTINEL_DONE:
                            break
                        if item is _SENTINEL_HEARTBEAT:
                            yield ": heartbeat\n\n"
                            continue
                        if isinstance(item, Exception):
                            raise item

                        event = item
                        translated = translate_event(event, counter)
                        if translated:
                            yield _emit_sse(json.dumps(translated, ensure_ascii=False))

                        # 检测 Skill 切换：Agent 读取其他 SKILL.md 时发送 skill_switched 事件
                        # 子 Agent 读取 SKILL.md 不触发 skill_switched
                        kind = event.get("event", "")
                        parent_ids = event.get("parent_ids", [])
                        is_child_event = counter.find_parent_task(parent_ids) is not None

                        if kind == "on_tool_start" and event.get("name") == "read_file":
                            if not is_child_event:  # 子 Agent 读 SKILL.md 不触发
                                _rf_path = str((event.get("data") or {}).get("input", {}).get("file_path", ""))
                                if "SKILL.md" in _rf_path:
                                    _sk_m = re.search(r'/skills/[^/]+/([^/]+)/SKILL\.md', _rf_path)
                                    if _sk_m:
                                        _switched = _sk_m.group(1)
                                        if _switched not in emitted_skills:
                                            emitted_skills.add(_switched)
                                            yield _emit_sse(json.dumps({'type': 'skill_switched', 'skill_name': _switched, 'timestamp': get_utc_now().isoformat()}, ensure_ascii=False))
                        if kind == "on_tool_end" and len(backend._buffer) > _last_buffer_len:
                            if not is_child_event:  # 子 Agent 写操作静默
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
                                    yield _emit_sse(json.dumps(rev, ensure_ascii=False))
                            else:
                                _last_buffer_len = len(backend._buffer)  # 静默推进指针
                finally:
                    _heartbeat_task.cancel()
                    if not _producer_task.done():
                        _producer_task.cancel()
                    # 等待任务真正结束，防止 aclose() 时任务泄漏
                    for _t in (_heartbeat_task, _producer_task):
                        try:
                            await _t
                        except (_asyncio.CancelledError, Exception):
                            pass

                # Agent 完成：获取改动列表（用于 completion 统计和 pending 缓存）
                changes = backend.get_changes()

                # 发送 completion 事件
                completion = make_completion_event(changes)
                yield _emit_sse(json.dumps(completion, ensure_ascii=False))

                # ── 改动 C：流结束后汇总扣费 ──
                token_usage_summary = None
                if settings.CREDITS_ENABLED:
                    try:
                        from app.utils.cost_calculator import CostCalculator
                        from app.services.credits.credit_service import CreditService
                        from app.services.credits.credit_utils import calculate_credits_from_cost
                        from app.services.ai_log_service import AILogService
                        from app.schemas.ai_call_log import AICallLogCreate
                        from app.core.database import create_db_session
                        from decimal import Decimal
                        from uuid import UUID

                        # ── Source 1: _UsageCollector（Agent 自身推理的 token）──
                        model_breakdown = {}
                        total_input = 0
                        total_output = 0
                        for cb_model, meta in usage_cb.usage_metadata.items():
                            model_name = cb_model or settings.OPENAI_MODEL
                            entry = model_breakdown.setdefault(model_name, {
                                "input_tokens": 0, "output_tokens": 0,
                                "cache_read": 0, "cache_creation": 0, "reasoning": 0,
                            })
                            inp = meta.get("input_tokens", 0)
                            out = meta.get("output_tokens", 0)
                            entry["input_tokens"] += inp
                            entry["output_tokens"] += out
                            total_input += inp
                            total_output += out

                            # 提取 token 细分
                            in_details = meta.get("input_token_details") or {}
                            out_details = meta.get("output_token_details") or {}
                            entry["cache_read"] += in_details.get("cache_read", 0) or 0
                            entry["cache_creation"] += in_details.get("cache_creation", 0) or 0
                            entry["reasoning"] += out_details.get("reasoning", 0) or 0

                        # _UsageCollector 部分的 token 小计（用于单独计算费用）
                        uc_input = total_input
                        uc_output = total_output

                        # ── Source 2: billing_accumulator（工具/技能调用的 token）──
                        for acc_model, acc_entry in billing_accumulator.model_breakdown.items():
                            entry = model_breakdown.setdefault(acc_model, {
                                "input_tokens": 0, "output_tokens": 0,
                                "cache_read": 0, "cache_creation": 0, "reasoning": 0,
                            })
                            entry["input_tokens"] += acc_entry["input_tokens"]
                            entry["output_tokens"] += acc_entry["output_tokens"]
                            entry["cache_read"] += acc_entry["cache_read"]
                            entry["cache_creation"] += acc_entry["cache_creation"]
                            entry["reasoning"] += acc_entry["reasoning"]
                            total_input += acc_entry["input_tokens"]
                            total_output += acc_entry["output_tokens"]

                        total_total = total_input + total_output

                        if total_total > 0:
                            # 聚合 token 细分
                            total_cache_read = sum(v.get("cache_read", 0) for v in model_breakdown.values())
                            total_cache_creation = sum(v.get("cache_creation", 0) for v in model_breakdown.values())
                            total_reasoning = sum(v.get("reasoning", 0) for v in model_breakdown.values())

                            # 从 DB 读取定价（带内存缓存）
                            from app.services.system_config_service import SystemConfigService
                            async with create_db_session() as pricing_db:
                                model_pricing = await SystemConfigService.get_model_pricing(pricing_db)
                                credits_per_dollar = await SystemConfigService.get_credits_per_dollar(pricing_db)

                            # _UsageCollector 部分重新计算费用（Agent 推理的 token）
                            if uc_input + uc_output > 0:
                                uc_cache_read = sum(
                                    (meta.get("input_token_details") or {}).get("cache_read", 0) or 0
                                    for meta in usage_cb.usage_metadata.values()
                                )
                                uc_cache_creation = sum(
                                    (meta.get("input_token_details") or {}).get("cache_creation", 0) or 0
                                    for meta in usage_cb.usage_metadata.values()
                                )
                                uc_reasoning = sum(
                                    (meta.get("output_token_details") or {}).get("reasoning", 0) or 0
                                    for meta in usage_cb.usage_metadata.values()
                                )
                                cost_data = CostCalculator.calculate_cost(
                                    model_name=settings.OPENAI_MODEL,
                                    prompt_tokens=uc_input,
                                    completion_tokens=uc_output,
                                    cache_read=uc_cache_read,
                                    cache_creation=uc_cache_creation,
                                    reasoning=uc_reasoning,
                                    model_pricing=model_pricing,
                                )
                                uc_cost = cost_data["total_cost"]
                            else:
                                cost_data = {"prompt_cost": 0, "completion_cost": 0, "total_cost": 0}
                                uc_cost = 0

                            # 合并费用：_UsageCollector 重算 + 累加器预算
                            combined_total_cost = uc_cost + billing_accumulator.total_cost_usd
                            combined_prompt_cost = cost_data["prompt_cost"] + billing_accumulator.prompt_cost_usd
                            combined_completion_cost = cost_data["completion_cost"] + billing_accumulator.completion_cost_usd

                            credits_to_deduct = calculate_credits_from_cost(
                                combined_total_cost, credits_per_dollar=credits_per_dollar,
                            )
                            duration_ms = int((_time.time() - _stream_start) * 1000)

                            # 独立 DB 会话（SSE 生成器内端点 db 不可用）
                            # nowait 重试：锁冲突时短暂退避后重试
                            from sqlalchemy.exc import DBAPIError as _DBErr
                            _max_retries = 3
                            for _attempt in range(_max_retries):
                                try:
                                    async with create_db_session() as billing_db:
                                        log_data = AICallLogCreate(
                                            user_id=current_user.id,
                                            model_name=settings.OPENAI_MODEL,
                                            operation_type="v2_agent_chat",
                                            prompt_tokens=total_input,
                                            completion_tokens=total_output,
                                            total_tokens=total_total,
                                            cache_read_tokens=total_cache_read,
                                            cache_creation_tokens=total_cache_creation,
                                            reasoning_tokens=total_reasoning,
                                            prompt_cost=combined_prompt_cost,
                                            completion_cost=combined_completion_cost,
                                            total_cost=combined_total_cost,
                                            duration_ms=duration_ms,
                                            is_success=True,
                                            extra_data={
                                                "conversation_id": conversation_id,
                                                "work_id": request.work_id,
                                                "model_breakdown": model_breakdown,
                                                "sub_call_count": billing_accumulator.call_count,
                                                "sub_call_log_ids": billing_accumulator.ai_call_log_ids,
                                            },
                                        )
                                        log_svc = AILogService(billing_db)
                                        ai_log = await log_svc.create_log(log_data, auto_commit=False)

                                        credit_svc = CreditService(billing_db)
                                        _raw = (request.message or "").replace("\n", " ").strip()
                                        msg_preview = _raw[:20] + "…" if len(_raw) > 20 else _raw
                                        await credit_svc.consume(
                                            user_id=current_user.id,
                                            amount=credits_to_deduct,
                                            description=f"{work.title} · {msg_preview}",
                                            related_id=ai_log.id,
                                            skip_check=current_user.is_admin,
                                            auto_commit=False,
                                            nowait=True,
                                        )
                                        await billing_db.commit()
                                    break  # 成功，退出重试
                                except (_DBErr, TimeoutError) as _lock_err:
                                    if _attempt < _max_retries - 1:
                                        logger.warning(
                                            "[V2 Billing] 锁冲突/超时，重试 %d/%d: %s",
                                            _attempt + 1, _max_retries, _lock_err,
                                        )
                                        await _asyncio.sleep(0.5 * (_attempt + 1))
                                    else:
                                        raise

                            token_usage_summary = {
                                "input_tokens": total_input,
                                "output_tokens": total_output,
                                "total_tokens": total_total,
                                "model_breakdown": model_breakdown,
                                "credits_deducted": float(credits_to_deduct),
                                "input_token_details": {"cache_read": total_cache_read, "cache_creation": total_cache_creation},
                                "output_token_details": {"reasoning": total_reasoning},
                            }
                            logger.info(
                                "[V2 Billing] user=%s conv=%s tokens=%d credits=%.2f (sub_calls=%d)",
                                user_id, conversation_id[:8], total_total,
                                float(credits_to_deduct), billing_accumulator.call_count,
                            )
                    except Exception as billing_err:
                        logger.error("[V2 Billing] 计费失败（不影响用户）: %s", billing_err, exc_info=True)

                # 缓存 backend 待审批（绑定 user_id 隔离）
                if changes:
                    backend_key = f"{user_id}:{conversation_id}"
                    _pending_backends[backend_key] = backend
                    _pending_access_times[backend_key] = _time.time()
                    _save_pending(backend_key, backend)
                    _evict_stale_pending()  # 搭车清理过期条目

                # ── 改动 D：done 事件附加 token_usage ──
                done_event = {
                    "type": "done",
                    "conversation_id": conversation_id,
                    "has_changes": len(changes) > 0,
                    "token_usage": token_usage_summary,
                }
                yield _emit_sse(json.dumps(done_event, ensure_ascii=False))
                _mark_stream_done(conversation_id)

        except Exception as e:
            logger.error(f"[V2 Agent] Error: {e}", exc_info=True)

            # ── 改动 E：错误路径也扣费（按实际用量） ──
            if settings.CREDITS_ENABLED and usage_cb is not None:
                try:
                    from app.utils.cost_calculator import CostCalculator
                    from app.services.credits.credit_service import CreditService
                    from app.services.credits.credit_utils import calculate_credits_from_cost
                    from app.services.ai_log_service import AILogService
                    from app.schemas.ai_call_log import AICallLogCreate
                    from app.core.database import create_db_session
                    from decimal import Decimal

                    err_input = sum(m.get("input_tokens", 0) for m in usage_cb.usage_metadata.values())
                    err_output = sum(m.get("output_tokens", 0) for m in usage_cb.usage_metadata.values())
                    # _UsageCollector 部分小计（用于单独计算费用）
                    uc_err_input = err_input
                    uc_err_output = err_output
                    # 合并累加器 token
                    err_input += billing_accumulator.prompt_tokens
                    err_output += billing_accumulator.completion_tokens
                    err_total = err_input + err_output

                    if err_total > 0:
                        # 聚合 token 细分
                        err_cache_read = 0
                        err_cache_creation = 0
                        err_reasoning = 0
                        for meta in usage_cb.usage_metadata.values():
                            in_d = meta.get("input_token_details") or {}
                            out_d = meta.get("output_token_details") or {}
                            err_cache_read += in_d.get("cache_read", 0) or 0
                            err_cache_creation += in_d.get("cache_creation", 0) or 0
                            err_reasoning += out_d.get("reasoning", 0) or 0
                        err_cache_read += billing_accumulator.cache_read_tokens
                        err_cache_creation += billing_accumulator.cache_creation_tokens
                        err_reasoning += billing_accumulator.reasoning_tokens

                        # 构建 per-model breakdown（与成功路径一致）
                        err_model_breakdown = {}
                        for cb_model, meta in usage_cb.usage_metadata.items():
                            model_name = cb_model or settings.OPENAI_MODEL
                            entry = err_model_breakdown.setdefault(model_name, {
                                "input_tokens": 0, "output_tokens": 0,
                                "cache_read": 0, "cache_creation": 0, "reasoning": 0,
                            })
                            entry["input_tokens"] += meta.get("input_tokens", 0)
                            entry["output_tokens"] += meta.get("output_tokens", 0)
                            in_d = meta.get("input_token_details") or {}
                            out_d = meta.get("output_token_details") or {}
                            entry["cache_read"] += in_d.get("cache_read", 0) or 0
                            entry["cache_creation"] += in_d.get("cache_creation", 0) or 0
                            entry["reasoning"] += out_d.get("reasoning", 0) or 0
                        # 合并累加器 model_breakdown
                        for acc_model, acc_entry in billing_accumulator.model_breakdown.items():
                            entry = err_model_breakdown.setdefault(acc_model, {
                                "input_tokens": 0, "output_tokens": 0,
                                "cache_read": 0, "cache_creation": 0, "reasoning": 0,
                            })
                            entry["input_tokens"] += acc_entry["input_tokens"]
                            entry["output_tokens"] += acc_entry["output_tokens"]
                            entry["cache_read"] += acc_entry["cache_read"]
                            entry["cache_creation"] += acc_entry["cache_creation"]
                            entry["reasoning"] += acc_entry["reasoning"]

                        # 从 DB 读取定价
                        from app.services.system_config_service import SystemConfigService
                        async with create_db_session() as pricing_db:
                            model_pricing = await SystemConfigService.get_model_pricing(pricing_db)
                            credits_per_dollar = await SystemConfigService.get_credits_per_dollar(pricing_db)

                        # _UsageCollector 部分费用
                        if uc_err_input + uc_err_output > 0:
                            uc_cache_read = sum(
                                (m.get("input_token_details") or {}).get("cache_read", 0) or 0
                                for m in usage_cb.usage_metadata.values()
                            )
                            uc_cache_creation = sum(
                                (m.get("input_token_details") or {}).get("cache_creation", 0) or 0
                                for m in usage_cb.usage_metadata.values()
                            )
                            uc_reasoning = sum(
                                (m.get("output_token_details") or {}).get("reasoning", 0) or 0
                                for m in usage_cb.usage_metadata.values()
                            )
                            cost_data = CostCalculator.calculate_cost(
                                settings.OPENAI_MODEL, uc_err_input, uc_err_output,
                                cache_read=uc_cache_read,
                                cache_creation=uc_cache_creation,
                                reasoning=uc_reasoning,
                                model_pricing=model_pricing,
                            )
                        else:
                            cost_data = {"prompt_cost": 0, "completion_cost": 0, "total_cost": 0}

                        # 合并费用
                        combined_total_cost = cost_data["total_cost"] + billing_accumulator.total_cost_usd
                        combined_prompt_cost = cost_data["prompt_cost"] + billing_accumulator.prompt_cost_usd
                        combined_completion_cost = cost_data["completion_cost"] + billing_accumulator.completion_cost_usd

                        credits_to_deduct = calculate_credits_from_cost(
                            combined_total_cost, credits_per_dollar=credits_per_dollar,
                        )
                        duration_ms = int((_time.time() - _stream_start) * 1000) if _stream_start else 0

                        _max_retries = 3
                        from sqlalchemy.exc import DBAPIError as _DBErr
                        for _attempt in range(_max_retries):
                            try:
                                async with create_db_session() as billing_db:
                                    log_data = AICallLogCreate(
                                        user_id=current_user.id,
                                        model_name=settings.OPENAI_MODEL,
                                        operation_type="v2_agent_chat",
                                        prompt_tokens=err_input,
                                        completion_tokens=err_output,
                                        total_tokens=err_total,
                                        cache_read_tokens=err_cache_read,
                                        cache_creation_tokens=err_cache_creation,
                                        reasoning_tokens=err_reasoning,
                                        prompt_cost=combined_prompt_cost,
                                        completion_cost=combined_completion_cost,
                                        total_cost=combined_total_cost,
                                        duration_ms=duration_ms,
                                        is_success=False,
                                        error_message=str(e)[:1000],
                                        extra_data={
                                            "conversation_id": conversation_id,
                                            "work_id": request.work_id,
                                            "model_breakdown": err_model_breakdown,
                                            "sub_call_count": billing_accumulator.call_count,
                                            "sub_call_log_ids": billing_accumulator.ai_call_log_ids,
                                        },
                                    )
                                    log_svc = AILogService(billing_db)
                                    ai_log = await log_svc.create_log(log_data, auto_commit=False)

                                    credit_svc = CreditService(billing_db)
                                    _raw = (request.message or "").replace("\n", " ").strip()
                                    msg_preview = _raw[:20] + "…" if len(_raw) > 20 else _raw
                                    await credit_svc.consume(
                                        user_id=current_user.id,
                                        amount=credits_to_deduct,
                                        description=f"{work.title} · {msg_preview}(错误)",
                                        related_id=ai_log.id,
                                        skip_check=current_user.is_admin,
                                        auto_commit=False,
                                        nowait=True,
                                    )
                                    await billing_db.commit()
                                break  # 成功，退出重试
                            except (_DBErr, TimeoutError) as _lock_err:
                                if _attempt < _max_retries - 1:
                                    logger.warning(
                                        "[V2 Billing] 错误路径锁冲突/超时，重试 %d/%d: %s",
                                        _attempt + 1, _max_retries, _lock_err,
                                    )
                                    await _asyncio.sleep(0.5 * (_attempt + 1))
                                else:
                                    raise

                        logger.info(
                            "[V2 Billing] error-path user=%s tokens=%d credits=%.2f (sub_calls=%d)",
                            user_id, err_total, float(credits_to_deduct),
                            billing_accumulator.call_count,
                        )
                except Exception as billing_err:
                    logger.error("[V2 Billing] 错误路径计费失败: %s", billing_err, exc_info=True)

            # 识别常见的 LLM API 错误，给用户更有用的提示
            error_str = str(e)
            error_hint = ""
            _err_lower = error_str.lower()
            if isinstance(e, json.JSONDecodeError) or "expecting value" in _err_lower:
                error_hint = (
                    "（可能原因：AI 服务返回了空响应或无效数据。"
                    "建议：稍后重试，若反复出现请检查 AI 服务配置或联系管理员）"
                )
                # 用更友好的消息替代原始 JSON 解析错误
                error_str = "AI 服务返回了无效响应"
            elif "help.openai.com" in _err_lower or "an error occurred while processing your request" in _err_lower:
                # OpenAI API 500 服务端错误，替换为友好消息，不暴露上游细节
                logger.error("[V2 Agent] OpenAI API 服务端错误（原始信息）: %s", error_str)
                error_str = "AI 服务暂时不可用"
                error_hint = "（AI 服务上游出现临时故障，请稍后重试）"
            elif any(kw in _err_lower for kw in [
                "rate limit", "rate_limit", "429", "too many requests",
                "quota", "insufficient_quota",
            ]):
                error_str = "AI 服务请求频率超限"
                error_hint = "（请稍等片刻后再试）"
            elif any(kw in _err_lower for kw in [
                "input stream", "context length", "too long", "max tokens",
                "maximum context", "token limit", "content too large",
            ]):
                error_hint = (
                    "（可能原因：对话上下文过长。"
                    "建议：开启新对话，减少单次任务涉及的章节数量，"
                    "或使用语义搜索代替逐章阅读）"
                )
            elif "timeout" in _err_lower or "timed out" in _err_lower:
                error_hint = "（可能原因：AI 服务响应超时，请稍后重试）"
            elif any(kw in _err_lower for kw in [
                "connection", "connect", "refused", "reset",
                "eof", "broken pipe", "network",
            ]):
                error_hint = "（可能原因：AI 服务连接异常，请稍后重试）"
            elif any(kw in _err_lower for kw in [
                "401", "unauthorized", "authentication", "invalid api key",
                "invalid_api_key", "incorrect api key",
            ]):
                logger.error("[V2 Agent] API 认证失败: %s", error_str)
                error_str = "AI 服务认证失败"
                error_hint = "（请联系管理员检查 API 配置）"
            elif any(kw in _err_lower for kw in [
                "500", "502", "503", "504", "internal server error",
                "bad gateway", "service unavailable", "server error",
            ]):
                logger.error("[V2 Agent] API 服务端错误: %s", error_str)
                error_str = "AI 服务暂时不可用"
                error_hint = "（AI 服务上游出现临时故障，请稍后重试）"

            error_event = {
                "type": "error",
                "error": error_str + error_hint,
                "error_type": type(e).__name__,
            }
            yield _emit_sse(json.dumps(error_event, ensure_ascii=False))
            _mark_stream_done(conversation_id)
        finally:
            # 清理 Agent 计费上下文
            agent_billing_ctx.reset(_billing_token)
            # 清理活跃流注册（断线重连用）
            _active_streams.pop(conversation_id, None)
            # 清理 Docker 沙盒容器（流结束后容器不再需要）
            if backend is not None and hasattr(backend, 'cleanup_sandbox'):
                try:
                    backend.cleanup_sandbox()
                except Exception as cleanup_err:
                    logger.warning("[V2 Agent] Sandbox cleanup failed: %s", cleanup_err)

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


@router.get("/v2/chat/stream/resume/{conversation_id}", summary="SSE 断线重连")
async def resume_v2_chat_stream(
    conversation_id: str,
    last_event_id: int = Query(0, alias="last_event_id", ge=0),
    current_user: User = Depends(get_current_active_user),
):
    """断线重连端点：回放缓存事件 + 转发实时事件。"""
    # 鉴权：校验当前用户是否为该流的所有者
    if not _check_stream_owner(conversation_id, str(current_user.id)):
        raise HTTPException(status_code=403, detail="Not authorized for this conversation")

    async def resume_generator():
        subscribe_q: _asyncio.Queue = _asyncio.Queue(maxsize=256)
        _RESUME_MAX_WAIT = 300  # 最长等待 5 分钟

        # 1. 先注册订阅队列（在回放之前），避免回放和订阅之间的事件间隙
        subscribers = _active_streams.get(conversation_id)
        if subscribers is not None:
            subscribers.add(subscribe_q)

        try:
            # 2. 回放 Redis 缓存中 last_event_id 之后的事件
            cached = _get_cached_events(conversation_id, after_id=last_event_id)
            # 记录已回放的最大 event_id，用于去重
            replayed_max_id = last_event_id
            for frame in cached:
                yield frame
                # 从帧中提取 event_id
                for fline in frame.split("\n"):
                    if fline.startswith("id: "):
                        try:
                            eid = int(fline[4:].strip())
                            if eid > replayed_max_id:
                                replayed_max_id = eid
                        except ValueError:
                            pass

            # 3. 如果流已完成且队列为空，直接结束
            if _is_stream_done(conversation_id) and subscribe_q.empty():
                return

            # 4. 如果主流不存在（已结束且清理了 _active_streams），直接结束
            if subscribers is None or conversation_id not in _active_streams:
                return

            # 5. 转发实时事件（去重：跳过已回放的事件）
            import time as _time
            _resume_start = _time.monotonic()
            while True:
                # 超时保护：防止无限挂起
                if _time.monotonic() - _resume_start > _RESUME_MAX_WAIT:
                    break
                try:
                    frame = await _asyncio.wait_for(subscribe_q.get(), timeout=30)
                    # 去重：提取 event_id，跳过已回放的
                    frame_id = 0
                    for fline in frame.split("\n"):
                        if fline.startswith("id: "):
                            try:
                                frame_id = int(fline[4:].strip())
                            except ValueError:
                                pass
                            break
                    if frame_id > 0 and frame_id <= replayed_max_id:
                        continue  # 已回放过，跳过

                    yield frame
                    if '"type": "done"' in frame or '"type": "error"' in frame:
                        break
                except _asyncio.TimeoutError:
                    yield ": heartbeat\n\n"
                    if _is_stream_done(conversation_id) and subscribe_q.empty():
                        break
        finally:
            # 从订阅者集合中移除自己
            subs = _active_streams.get(conversation_id)
            if subs is not None:
                subs.discard(subscribe_q)

    return StreamingResponse(
        resume_generator(),
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
    _pending_access_times[backend_key] = _time.time()
    return V2ChangesResponse(
        conversation_id=conversation_id,
        changes=backend.get_changes(),
    )


@router.post("/v2/changes/{conversation_id}/accept", summary="全部接受改动")
async def accept_v2_changes(
    conversation_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """全部接受：将缓冲区写入磁盘。"""
    backend_key = f"{current_user.id}:{conversation_id}"
    backend = _pending_backends.pop(backend_key, None)
    _pending_access_times.pop(backend_key, None)
    if not backend:
        backend = _load_pending(backend_key)
        _pending_backends.pop(backend_key, None)
        _pending_access_times.pop(backend_key, None)
    if not backend:
        raise HTTPException(status_code=404, detail="No pending changes")

    affected = backend.flush()
    _delete_pending(backend_key)

    # 清理 Docker 沙盒（如果有）
    if hasattr(backend, 'cleanup_sandbox'):
        backend.cleanup_sandbox()

    worldview_sync: dict[str, Any] | None = None
    try:
        worldview_sync = await _sync_worldview_cards_from_pending(
            db=db,
            backend=backend,
            touched_paths=affected,
        )
    except Exception as e:
        logger.warning(f"[V2] knowledge->worldview sync failed: {e}")

    # flush 后更新向量索引（直接读磁盘文件，而非 backend.read()）
    from app.services.agent.deep_agent.rag_tool import update_chapter_vectors, remove_chapter_vectors, update_knowledge_vectors
    from app.services.agent.deep_agent.frontmatter import parse_chapter

    for path in affected:
        if "/chapters/" in path:
            try:
                disk_path = backend._resolve_path(path)
                work_id = Path(str(backend.cwd)).name
                if not disk_path.exists() or not disk_path.is_file():
                    remove_chapter_vectors(work_id, path)
                    continue
                raw = disk_path.read_text(encoding="utf-8")
                parsed = parse_chapter(raw)
                update_chapter_vectors(work_id, path, parsed["content"])
            except Exception as e:
                logger.warning(f"[V2] Failed to update vectors for {path}: {e}")
        elif "/knowledge/" in path:
            try:
                disk_path = backend._resolve_path(path)
                work_id = Path(str(backend.cwd)).name
                if not disk_path.exists() or not disk_path.is_file():
                    remove_chapter_vectors(work_id, path)
                    continue
                raw = disk_path.read_text(encoding="utf-8")
                update_knowledge_vectors(work_id, path, raw)
            except Exception as e:
                logger.warning(f"[V2] Failed to update knowledge vectors for {path}: {e}")

    return {"status": "accepted", "affected_paths": affected, "worldview_sync": worldview_sync}


@router.post("/v2/changes/{conversation_id}/reject", summary="全部拒绝改动")
async def reject_v2_changes(
    conversation_id: str,
    current_user: User = Depends(get_current_active_user),
):
    """全部拒绝：丢弃缓冲区。"""
    backend_key = f"{current_user.id}:{conversation_id}"
    backend = _pending_backends.pop(backend_key, None)
    _pending_access_times.pop(backend_key, None)
    if not backend:
        backend = _load_pending(backend_key)
        _pending_backends.pop(backend_key, None)
        _pending_access_times.pop(backend_key, None)
    if not backend:
        raise HTTPException(status_code=404, detail="No pending changes")
    backend.discard()
    _delete_pending(backend_key)

    # 清理 Docker 沙盒（如果有）
    if hasattr(backend, 'cleanup_sandbox'):
        backend.cleanup_sandbox()

    return {"status": "rejected"}


@router.post("/v2/changes/{conversation_id}/accept/{index}", summary="单个接受改动")
async def accept_v2_single_change(
    conversation_id: str,
    index: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """单个接受：将指定操作写入磁盘。"""
    backend_key = f"{current_user.id}:{conversation_id}"
    backend = _pending_backends.get(backend_key) or _load_pending(backend_key)
    if not backend:
        raise HTTPException(status_code=404, detail="No pending changes")
    _pending_access_times[backend_key] = _time.time()

    # 先捕获受影响路径（尤其是 rename 需要 old/new 两个路径），再执行 flush_single
    changes = backend.get_changes()
    if index < 0 or index >= len(changes):
        raise HTTPException(status_code=400, detail="Invalid change index")

    selected = changes[index]
    touched_paths: list[str] = []
    if selected.get("op_type") == "rename":
        for candidate in (
            selected.get("old_path"),
            selected.get("new_path"),
            selected.get("path"),
        ):
            if isinstance(candidate, str) and candidate and candidate not in touched_paths:
                touched_paths.append(candidate)
    else:
        selected_path = selected.get("path")
        if isinstance(selected_path, str) and selected_path:
            touched_paths.append(selected_path)

    path = backend.flush_single(index)
    if path is None:
        raise HTTPException(status_code=400, detail="Invalid change index or has unresolved dependencies")
    if not touched_paths:
        touched_paths = [path]

    worldview_sync: dict[str, Any] | None = None
    try:
        worldview_sync = await _sync_worldview_cards_from_pending(
            db=db,
            backend=backend,
            touched_paths=touched_paths,
        )
    except Exception as e:
        logger.warning(f"[V2] knowledge->worldview sync failed: {e}")

    # 单个接受后同步章节/知识库向量索引（含 rename/delete 场景）
    try:
        from app.services.agent.deep_agent.rag_tool import (
            remove_chapter_vectors,
            update_chapter_vectors,
            update_knowledge_vectors,
        )
        from app.services.agent.deep_agent.frontmatter import parse_chapter

        work_id = Path(str(backend.cwd)).name
        for touched_path in touched_paths:
            if "/chapters/" in touched_path:
                disk_path = backend._resolve_path(touched_path)
                if not disk_path.exists() or not disk_path.is_file():
                    remove_chapter_vectors(work_id, touched_path)
                else:
                    raw = disk_path.read_text(encoding="utf-8")
                    parsed = parse_chapter(raw)
                    update_chapter_vectors(work_id, touched_path, parsed["content"])
            elif "/knowledge/" in touched_path:
                disk_path = backend._resolve_path(touched_path)
                if not disk_path.exists() or not disk_path.is_file():
                    remove_chapter_vectors(work_id, touched_path)
                else:
                    raw = disk_path.read_text(encoding="utf-8")
                    update_knowledge_vectors(work_id, touched_path, raw)
    except Exception as e:
        logger.warning(f"[V2] Failed to update vectors for single change {path}: {e}")

    # 缓冲区清空后移除
    if not backend.get_changes():
        _pending_backends.pop(backend_key, None)
        _pending_access_times.pop(backend_key, None)
        _delete_pending(backend_key)
        # 防御性清理：释放可能关联的 Docker 沙盒
        if hasattr(backend, 'cleanup_sandbox'):
            backend.cleanup_sandbox()
    else:
        _save_pending(backend_key, backend)

    return {
        "status": "accepted",
        "path": path,
        "affected_paths": touched_paths,
        "worldview_sync": worldview_sync,
    }


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
    _pending_access_times[backend_key] = _time.time()

    ok = backend.discard_single(index)
    if not ok:
        raise HTTPException(status_code=400, detail="Invalid change index")

    # 缓冲区清空后移除
    if not backend.get_changes():
        _pending_backends.pop(backend_key, None)
        _pending_access_times.pop(backend_key, None)
        _delete_pending(backend_key)
        # 防御性清理：释放可能关联的 Docker 沙盒
        if hasattr(backend, 'cleanup_sandbox'):
            backend.cleanup_sandbox()
    else:
        _save_pending(backend_key, backend)

    return {"status": "rejected"}
