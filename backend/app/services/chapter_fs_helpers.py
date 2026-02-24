"""
章节文件系统 Helper 模块

从 library.py 提取的公共工具函数，供所有需要读取章节文件的模块使用。
章节存储路径: data/users/{author_id}/works/{work_id}/chapters/{num}-{title}.md
"""
import asyncio
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from app.services.agent.deep_agent import DATA_ROOT
from app.services.agent.deep_agent.frontmatter import parse_chapter


@dataclass
class ChapterData:
    """章节数据，兼容原 Chapter ORM 对象的常用属性访问模式。"""
    id: str           # 章节序号（字符串形式），如 "1", "2"
    title: str
    content: str
    order: int        # 章节序号（整数），等同于文件名前缀
    word_count: int
    status: str       # "draft" | "published"


def get_chapters_dir(author_id: str, work_id: str) -> Path:
    """获取章节目录 Path。"""
    return DATA_ROOT / author_id / "works" / work_id / "chapters"


def list_chapter_files(chapters_dir: Path) -> list[tuple[int, Path]]:
    """列出 [(num, path)]，按序号升序。"""
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


def resolve_chapter_path(chapters_dir: Path, num: int) -> Optional[Path]:
    """按序号找到章节文件路径，找不到返回 None。"""
    for n, p in list_chapter_files(chapters_dir):
        if n == num:
            return p
    return None


async def count_published_chapters(author_id: str, work_id: str) -> int:
    """统计已发布章节数量。"""
    chapters_dir = get_chapters_dir(author_id, work_id)
    count = 0
    for _num, path in list_chapter_files(chapters_dir):
        try:
            raw = await asyncio.to_thread(path.read_text, "utf-8")
            ch = parse_chapter(raw)
            if ch["status"] == "published":
                count += 1
        except Exception:
            continue
    return count


async def count_all_chapters(author_id: str, work_id: str) -> int:
    """统计所有章节数量（含 draft）。"""
    chapters_dir = get_chapters_dir(author_id, work_id)
    return len(list_chapter_files(chapters_dir))


async def get_all_chapters(author_id: str, work_id: str) -> list[dict]:
    """获取所有章节详情列表（含 draft），按序号升序。"""
    chapters_dir = get_chapters_dir(author_id, work_id)
    result = []
    for num, path in list_chapter_files(chapters_dir):
        try:
            raw = await asyncio.to_thread(path.read_text, "utf-8")
            ch = parse_chapter(raw)
            result.append({
                "num": num,
                "title": ch["title"],
                "word_count": ch["word_count"],
                "content": ch["content"],
                "status": ch["status"],
            })
        except Exception:
            continue
    return result


async def get_published_chapters(author_id: str, work_id: str) -> list[dict]:
    """获取所有已发布章节详情列表，按序号升序。"""
    chapters_dir = get_chapters_dir(author_id, work_id)
    result = []
    for num, path in list_chapter_files(chapters_dir):
        try:
            raw = await asyncio.to_thread(path.read_text, "utf-8")
            ch = parse_chapter(raw)
            if ch["status"] == "published":
                result.append({
                    "num": num,
                    "title": ch["title"],
                    "word_count": ch["word_count"],
                    "content": ch["content"],
                })
        except Exception:
            continue
    return result


async def read_chapter_by_num(
    author_id: str, work_id: str, num: int
) -> Optional[dict]:
    """读取单个章节，返回 dict 或 None。"""
    chapters_dir = get_chapters_dir(author_id, work_id)
    path = resolve_chapter_path(chapters_dir, num)
    if not path:
        return None
    try:
        raw = await asyncio.to_thread(path.read_text, "utf-8")
        ch = parse_chapter(raw)
        ch["num"] = num
        return ch
    except Exception:
        return None


async def get_all_chapters_data(
    author_id: str, work_id: str
) -> list[ChapterData]:
    """读取所有章节，返回 ChapterData 列表，按序号升序。"""
    chapters_dir = get_chapters_dir(author_id, work_id)
    result = []
    for num, path in list_chapter_files(chapters_dir):
        try:
            raw = await asyncio.to_thread(path.read_text, "utf-8")
            ch = parse_chapter(raw)
            result.append(ChapterData(
                id=str(num),
                title=ch["title"],
                content=ch["content"],
                order=num,
                word_count=ch["word_count"],
                status=ch["status"],
            ))
        except Exception:
            continue
    return result


async def get_chapters_by_nums(
    author_id: str, work_id: str, nums: list[int]
) -> list[ChapterData]:
    """按章节序号列表读取指定章节，返回按序号升序排列的列表。"""
    chapters_dir = get_chapters_dir(author_id, work_id)
    nums_set = set(nums)
    result = []
    for num, path in list_chapter_files(chapters_dir):
        if num not in nums_set:
            continue
        try:
            raw = await asyncio.to_thread(path.read_text, "utf-8")
            ch = parse_chapter(raw)
            result.append(ChapterData(
                id=str(num),
                title=ch["title"],
                content=ch["content"],
                order=num,
                word_count=ch["word_count"],
                status=ch["status"],
            ))
        except Exception:
            continue
    return result


async def get_chapters_by_range(
    author_id: str,
    work_id: str,
    start_chapter: int = 1,
    end_chapter: Optional[int] = None,
    limit: Optional[int] = None,
) -> list[ChapterData]:
    """按序号范围读取章节，返回按序号升序排列的列表。"""
    chapters_dir = get_chapters_dir(author_id, work_id)
    result = []
    for num, path in list_chapter_files(chapters_dir):
        if num < start_chapter:
            continue
        if end_chapter is not None and num > end_chapter:
            continue
        try:
            raw = await asyncio.to_thread(path.read_text, "utf-8")
            ch = parse_chapter(raw)
            result.append(ChapterData(
                id=str(num),
                title=ch["title"],
                content=ch["content"],
                order=num,
                word_count=ch["word_count"],
                status=ch["status"],
            ))
        except Exception:
            continue
        if limit and len(result) >= limit:
            break
    return result
