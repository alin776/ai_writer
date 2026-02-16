"""
章节文件系统 API

基于文件系统的章节 CRUD，替代 DB 章节操作。
所有章节数据存储在 data/users/{user_id}/works/{work_id}/chapters/ 目录。
"""

import asyncio
import logging
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.work import Work
from app.services.agent.deep_agent import DATA_ROOT
from app.services.agent.deep_agent.frontmatter import (
    build_chapter, chapter_filename, parse_chapter,
)

router = APIRouter()
logger = logging.getLogger(__name__)


# ─── 请求/响应模型 ───


class ChapterResponse(BaseModel):
    """章节信息响应"""
    num: int
    title: str
    status: str
    word_count: int
    content: Optional[str] = None


class ChapterCreateRequest(BaseModel):
    """创建章节请求"""
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(default="")
    status: str = Field(default="draft")


class ChapterUpdateRequest(BaseModel):
    """更新章节请求"""
    title: Optional[str] = None
    content: Optional[str] = None
    status: Optional[str] = None


class FileContentResponse(BaseModel):
    """文件内容响应"""
    path: str
    content: str


class FileWriteRequest(BaseModel):
    """文件写入请求"""
    content: str


# ─── 工具函数 ───


def _get_work_dir(user_id: str, work_id: str) -> Path:
    """获取作品工作目录。"""
    return DATA_ROOT / user_id / "works" / work_id


def _safe_path(base: Path, user_path: str) -> Path:
    """安全路径解析：防止目录穿越。"""
    resolved = (base / user_path).resolve()
    base_resolved = base.resolve()
    try:
        resolved.relative_to(base_resolved)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Path traversal not allowed",
        )
    return resolved


async def _get_work_and_dir(
    work_id: str,
    current_user: User,
    db: AsyncSession,
) -> tuple[Work, Path]:
    """获取作品和工作目录，统一鉴权。"""
    stmt = select(Work).where(
        Work.id == work_id,
        Work.author_id == current_user.id,
    )
    result = await db.execute(stmt)
    work = result.scalar_one_or_none()
    if not work:
        raise HTTPException(status_code=404, detail="Work not found")

    work_dir = _get_work_dir(str(current_user.id), str(work.id))
    return work, work_dir


def _list_chapter_files(chapters_dir: Path) -> list[tuple[int, Path]]:
    """列出章节文件，返回 (序号, 路径) 排序列表。"""
    if not chapters_dir.exists():
        return []
    result = []
    for f in chapters_dir.iterdir():
        if f.is_file() and f.suffix == ".md":
            match = re.match(r"^(\d+)-(.+)\.md$", f.name)
            if match:
                result.append((int(match.group(1)), f))
    result.sort(key=lambda x: x[0])
    return result


def _next_chapter_num(chapters_dir: Path) -> int:
    """获取下一个可用的章节序号。"""
    existing = _list_chapter_files(chapters_dir)
    if not existing:
        return 1
    return existing[-1][0] + 1


def _resolve_chapter_path(chapters_dir: Path, num: int) -> Optional[Path]:
    """按序号 glob 匹配章节文件：02-*.md"""
    for f in chapters_dir.glob(f"{num:02d}-*.md"):
        if f.is_file():
            return f
    return None


# ─── 章节端点 ───


@router.get(
    "/works/{work_id}/chapters",
    response_model=List[ChapterResponse],
    summary="列出所有章节",
)
async def list_chapters(
    work_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """列出作品的所有章节（从文件系统读取）。"""
    _, work_dir = await _get_work_and_dir(work_id, current_user, db)
    chapters_dir = work_dir / "chapters"

    chapter_files = await asyncio.to_thread(_list_chapter_files, chapters_dir)

    result = []
    for num, path in chapter_files:
        try:
            raw = await asyncio.to_thread(path.read_text, "utf-8")
            parsed = parse_chapter(raw)
            result.append(ChapterResponse(
                num=num,
                title=parsed["title"],
                status=parsed["status"],
                word_count=parsed["word_count"],
            ))
        except Exception as e:
            logger.warning(f"Failed to parse chapter {path}: {e}")
            result.append(ChapterResponse(
                num=num,
                title=f"Chapter {num}",
                status="error",
                word_count=0,
            ))
    return result


@router.get(
    "/works/{work_id}/chapters/{num}",
    response_model=ChapterResponse,
    summary="读取章节",
)
async def get_chapter(
    work_id: str,
    num: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """读取单个章节（含正文内容）。"""
    _, work_dir = await _get_work_and_dir(work_id, current_user, db)
    chapters_dir = work_dir / "chapters"
    chapter_path = _resolve_chapter_path(chapters_dir, num)

    if chapter_path is None:
        raise HTTPException(status_code=404, detail=f"Chapter {num} not found")

    raw = await asyncio.to_thread(chapter_path.read_text, "utf-8")
    parsed = parse_chapter(raw)
    return ChapterResponse(
        num=num,
        title=parsed["title"],
        status=parsed["status"],
        word_count=parsed["word_count"],
        content=parsed["content"],
    )


@router.post(
    "/works/{work_id}/chapters",
    response_model=ChapterResponse,
    status_code=status.HTTP_201_CREATED,
    summary="创建章节",
)
async def create_chapter(
    work_id: str,
    request: ChapterCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """创建新章节（自动分配序号）。"""
    _, work_dir = await _get_work_and_dir(work_id, current_user, db)
    chapters_dir = work_dir / "chapters"
    chapters_dir.mkdir(parents=True, exist_ok=True)

    num = _next_chapter_num(chapters_dir)
    chapter_path = chapters_dir / chapter_filename(num, request.title)

    content = build_chapter(request.title, request.status, request.content)
    await asyncio.to_thread(chapter_path.write_text, content, "utf-8")

    parsed = parse_chapter(content)
    return ChapterResponse(
        num=num,
        title=parsed["title"],
        status=parsed["status"],
        word_count=parsed["word_count"],
        content=parsed["content"],
    )


@router.put(
    "/works/{work_id}/chapters/{num}",
    response_model=ChapterResponse,
    summary="更新章节",
)
async def update_chapter(
    work_id: str,
    num: int,
    request: ChapterUpdateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """更新章节（标题/内容/状态）。"""
    _, work_dir = await _get_work_and_dir(work_id, current_user, db)
    chapters_dir = work_dir / "chapters"
    chapter_path = _resolve_chapter_path(chapters_dir, num)

    if chapter_path is None:
        raise HTTPException(status_code=404, detail=f"Chapter {num} not found")

    raw = await asyncio.to_thread(chapter_path.read_text, "utf-8")
    parsed = parse_chapter(raw)

    title = request.title if request.title is not None else parsed["title"]
    content = request.content if request.content is not None else parsed["content"]
    chapter_status = request.status if request.status is not None else parsed["status"]

    new_content = build_chapter(title, chapter_status, content)
    await asyncio.to_thread(chapter_path.write_text, new_content, "utf-8")

    # 标题变更时重命名文件
    new_name = chapter_filename(num, title)
    new_path = chapters_dir / new_name
    if new_path != chapter_path:
        if new_path.exists():
            logger.warning(f"Rename target {new_path} already exists, skipping rename")
        else:
            await asyncio.to_thread(chapter_path.rename, new_path)

    new_parsed = parse_chapter(new_content)
    return ChapterResponse(
        num=num,
        title=new_parsed["title"],
        status=new_parsed["status"],
        word_count=new_parsed["word_count"],
        content=new_parsed["content"],
    )


@router.delete(
    "/works/{work_id}/chapters/{num}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="删除章节",
)
async def delete_chapter(
    work_id: str,
    num: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """删除章节文件。"""
    _, work_dir = await _get_work_and_dir(work_id, current_user, db)
    chapters_dir = work_dir / "chapters"
    chapter_path = _resolve_chapter_path(chapters_dir, num)

    if chapter_path is None:
        raise HTTPException(status_code=404, detail=f"Chapter {num} not found")

    await asyncio.to_thread(chapter_path.unlink)
    return None


# ─── 通用文件端点 ───


@router.get(
    "/works/{work_id}/files/{path:path}",
    response_model=FileContentResponse,
    summary="读取文件",
)
async def read_file(
    work_id: str,
    path: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """读取作品目录下的任意文件。"""
    _, work_dir = await _get_work_and_dir(work_id, current_user, db)
    file_path = _safe_path(work_dir, path)

    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")

    content = await asyncio.to_thread(file_path.read_text, "utf-8")
    return FileContentResponse(path=path, content=content)


@router.put(
    "/works/{work_id}/files/{path:path}",
    response_model=FileContentResponse,
    summary="写入文件",
)
async def write_file(
    work_id: str,
    path: str,
    request: FileWriteRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """写入作品目录下的任意文件（创建或覆盖）。"""
    _, work_dir = await _get_work_and_dir(work_id, current_user, db)
    file_path = _safe_path(work_dir, path)

    file_path.parent.mkdir(parents=True, exist_ok=True)
    await asyncio.to_thread(file_path.write_text, request.content, "utf-8")

    return FileContentResponse(path=path, content=request.content)
