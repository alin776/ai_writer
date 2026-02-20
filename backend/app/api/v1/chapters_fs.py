"""
章节文件系统 API

基于文件系统的章节 CRUD，替代 DB 章节操作。
所有章节数据存储在 data/users/{user_id}/works/{work_id}/chapters/ 目录。
"""

import asyncio
import io
import logging
import re
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.work import Work
from app.services.agent.deep_agent import DATA_ROOT
from app.services.agent.deep_agent.frontmatter import (
    build_chapter, chapter_filename, parse_chapter,
)
from app.services.worldview_knowledge_bridge import WorldviewKnowledgeBridge
from app.services.knowledge_sync_scheduler import request_worldview_sync

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


class FileNode(BaseModel):
    """文件树节点"""
    name: str
    path: str
    type: str  # "file" | "dir"
    size: int = 0
    children: list["FileNode"] = []

FileNode.model_rebuild()


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


def _to_posix_rel_path(path: str) -> str:
    """标准化相对路径为 posix 形式。"""
    rel = (path or "").strip().replace("\\", "/")
    while rel.startswith("./"):
        rel = rel[2:]
    return rel.lstrip("/")


async def _sync_worldview_cards_from_knowledge(
    db: AsyncSession,
    work_id: str,
    work_dir: Path,
    touched_paths: list[str],
) -> None:
    """Best-effort: debounced knowledge->worldview sync."""
    if not WorldviewKnowledgeBridge.has_tracked_path(touched_paths):
        return
    try:
        await request_worldview_sync(
            db=db,
            work_id=work_id,
            work_dir=work_dir,
            touched_paths=touched_paths,
            sync_mode=settings.WORLDVIEW_KNOWLEDGE_SYNC_MODE,
        )
    except Exception as exc:
        logger.warning("[chapters_fs] knowledge->worldview sync skipped: %s", exc)


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


def _renumber_chapters(chapters_dir: Path) -> None:
    """删除后重排章节文件序号，保持连续。"""
    files = _list_chapter_files(chapters_dir)
    for new_num, (old_num, fpath) in enumerate(files, start=1):
        if new_num != old_num:
            match = re.match(r"^\d+-(.+)$", fpath.name)
            if match:
                new_name = f"{new_num:02d}-{match.group(1)}"
                fpath.rename(chapters_dir / new_name)


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


# ─── 文件树 + 迁移 ───

# 兼容迁移：旧路径 → 新路径
_MIGRATION_MAP = {
    "characters.md": "knowledge/characters.md",
    "worldview.md": "knowledge/worldview.md",
    "outline.md": "knowledge/outline.md",
}


def _migrate_legacy_files(work_dir: Path) -> None:
    """将旧路径文件迁移到 knowledge/ 目录（一次性）。"""
    for old_rel, new_rel in _MIGRATION_MAP.items():
        old_path = work_dir / old_rel
        new_path = work_dir / new_rel
        if old_path.exists() and not new_path.exists():
            new_path.parent.mkdir(parents=True, exist_ok=True)
            old_path.rename(new_path)
            logger.info(f"Migrated {old_rel} → {new_rel}")


def _build_file_tree(base: Path, rel: str = "") -> list[FileNode]:
    """递归构建文件树（排除隐藏文件，只包含 .md 文件和含 .md 的目录）。"""
    current = base / rel if rel else base
    if not current.exists():
        return []

    dirs: list[FileNode] = []
    files: list[FileNode] = []

    for entry in sorted(current.iterdir(), key=lambda e: e.name):
        if entry.name.startswith(".") or entry.is_symlink():
            continue
        entry_rel = f"{rel}/{entry.name}" if rel else entry.name
        if entry.is_dir():
            children = _build_file_tree(base, entry_rel)
            if children:  # 只包含有 .md 文件的目录
                dirs.append(FileNode(
                    name=entry.name, path=entry_rel,
                    type="dir", children=children,
                ))
        elif entry.is_file() and entry.suffix == ".md":
            files.append(FileNode(
                name=entry.name, path=entry_rel,
                type="file", size=entry.stat().st_size,
            ))

    return dirs + files


@router.get(
    "/works/{work_id}/tree",
    response_model=list[FileNode],
    summary="获取文件树",
)
async def get_file_tree(
    work_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """递归列出作品目录下的文件树。"""
    _, work_dir = await _get_work_and_dir(work_id, current_user, db)
    await asyncio.to_thread(_migrate_legacy_files, work_dir)
    tree = await asyncio.to_thread(_build_file_tree, work_dir)
    return tree


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

    rel_path = _to_posix_rel_path(path)
    await _sync_worldview_cards_from_knowledge(
        db=db,
        work_id=work_id,
        work_dir=work_dir,
        touched_paths=[rel_path],
    )

    return FileContentResponse(path=path, content=request.content)


# ─── 通用文件/目录操作端点 ───


class RenameRequest(BaseModel):
    """重命名请求"""
    new_name: str = Field(..., min_length=1, max_length=200)


@router.post(
    "/works/{work_id}/dirs/{path:path}",
    response_model=list[FileNode],
    status_code=status.HTTP_201_CREATED,
    summary="创建目录",
)
async def create_dir(
    work_id: str,
    path: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """在作品目录下创建文件夹，空目录自动放入占位文件。"""
    _, work_dir = await _get_work_and_dir(work_id, current_user, db)
    dir_path = _safe_path(work_dir, path)
    await asyncio.to_thread(dir_path.mkdir, parents=True, exist_ok=True)
    # 空目录不会出现在文件树中（_build_file_tree 过滤），放一个占位 .md
    if not any(p for p in dir_path.iterdir() if p.suffix == ".md"):
        placeholder = dir_path / "untitled.md"
        await asyncio.to_thread(placeholder.write_text, "", "utf-8")
    return await asyncio.to_thread(_build_file_tree, work_dir)


@router.delete(
    "/works/{work_id}/files/{path:path}",
    response_model=list[FileNode],
    summary="删除文件或文件夹",
)
async def delete_file(
    work_id: str,
    path: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """删除作品目录下的文件或文件夹，返回刷新后的文件树。"""
    _, work_dir = await _get_work_and_dir(work_id, current_user, db)
    target = _safe_path(work_dir, path)
    if not target.exists():
        raise HTTPException(status_code=404, detail="File or directory not found")
    # 禁止删除关键根目录
    if target.resolve() == (work_dir / "chapters").resolve() or \
       target.resolve() == (work_dir / "knowledge").resolve():
        raise HTTPException(status_code=400, detail="Cannot delete critical directory")
    if target.is_dir():
        await asyncio.to_thread(shutil.rmtree, target)
    else:
        await asyncio.to_thread(target.unlink)
    # 章节文件删除后自动重排序
    if path.startswith("chapters/"):
        chapters_dir = work_dir / "chapters"
        if chapters_dir.exists():
            await asyncio.to_thread(_renumber_chapters, chapters_dir)
    return await asyncio.to_thread(_build_file_tree, work_dir)


@router.patch(
    "/works/{work_id}/files/{path:path}",
    response_model=list[FileNode],
    summary="重命名文件或文件夹",
)
async def rename_file(
    work_id: str,
    path: str,
    request: RenameRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """重命名作品目录下的文件或文件夹，返回刷新后的文件树。"""
    _, work_dir = await _get_work_and_dir(work_id, current_user, db)
    target = _safe_path(work_dir, path)
    if not target.exists():
        raise HTTPException(status_code=404, detail="File or directory not found")
    # 禁止重命名关键根目录
    if target.resolve() == (work_dir / "chapters").resolve() or \
       target.resolve() == (work_dir / "knowledge").resolve():
        raise HTTPException(status_code=400, detail="Cannot rename critical directory")
    new_name = request.new_name.strip()
    if "/" in new_name or "\\" in new_name or new_name.startswith("."):
        raise HTTPException(status_code=400, detail="Invalid name")
    new_path = target.parent / new_name
    _safe_path(work_dir, str(new_path.relative_to(work_dir.resolve())))
    if new_path.exists():
        raise HTTPException(status_code=409, detail="Target already exists")
    await asyncio.to_thread(target.rename, new_path)
    return await asyncio.to_thread(_build_file_tree, work_dir)


# ─── 知识库上传 ───

_ALLOWED_EXTENSIONS = {"txt", "md", "pdf", "docx"}
_MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5 MB


def _extract_text_from_upload(file: UploadFile, content_bytes: bytes) -> str:
    """根据文件类型提取文本内容，支持 txt/md/pdf/docx。"""
    filename = file.filename or ""
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

    if ext in ("txt", "md", "markdown", ""):
        for encoding in ("utf-8", "gbk", "gb2312", "gb18030", "utf-16", "big5"):
            try:
                return content_bytes.decode(encoding)
            except (UnicodeDecodeError, LookupError):
                continue
        raise HTTPException(status_code=400, detail="无法识别文件编码，请转换为 UTF-8 后重试")

    if ext == "pdf":
        try:
            import pdfplumber
        except ImportError:
            raise HTTPException(status_code=400, detail="服务器未安装 pdfplumber，暂不支持 PDF")
        with pdfplumber.open(io.BytesIO(content_bytes)) as pdf:
            texts = [page.extract_text() or "" for page in pdf.pages]
        return "\n".join(t for t in texts if t)

    if ext == "docx":
        try:
            from docx import Document
        except ImportError:
            raise HTTPException(status_code=400, detail="服务器未安装 python-docx，暂不支持 DOCX")
        doc = Document(io.BytesIO(content_bytes))
        return "\n".join(p.text for p in doc.paragraphs if p.text)

    raise HTTPException(status_code=400, detail=f"不支持的文件类型: .{ext}")


@router.post(
    "/works/{work_id}/upload/knowledge",
    response_model=list[FileNode],
    summary="上传知识库文件",
)
async def upload_knowledge_file(
    work_id: str,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """上传文件到知识库目录，提取文本存为 .md，返回刷新后的文件树。"""
    _, work_dir = await _get_work_and_dir(work_id, current_user, db)

    # 校验文件类型
    filename = file.filename or "untitled.txt"
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext not in _ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"不支持的文件类型，允许: {', '.join(_ALLOWED_EXTENSIONS)}")

    # 读取并校验大小
    content_bytes = await file.read()
    if len(content_bytes) > _MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=400, detail="文件大小超过 5MB 限制")

    # 提取文本
    text = _extract_text_from_upload(file, content_bytes)

    # 存为 knowledge/{stem}.md
    stem = filename.rsplit(".", 1)[0] if "." in filename else filename
    knowledge_dir = work_dir / "knowledge"
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    target = knowledge_dir / f"{stem}.md"
    await asyncio.to_thread(target.write_text, text, "utf-8")

    rel_path = _to_posix_rel_path(f"knowledge/{stem}.md")
    await _sync_worldview_cards_from_knowledge(
        db=db,
        work_id=work_id,
        work_dir=work_dir,
        touched_paths=[rel_path],
    )

    return await asyncio.to_thread(_build_file_tree, work_dir)
