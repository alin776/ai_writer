from fastapi import APIRouter, Depends, HTTPException, status, Query, Response
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import Optional, List
from datetime import datetime, timezone
import logging

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.work import Work, WorkGenre
from app.models.chapter import Chapter
from app.models.bookshelf import Bookshelf
from app.models.rating import WorkRating
from app.models.channel import Channel, ChannelType, ChannelStatus
from app.models.channel_member import ChannelMember, MemberRole
from app.schemas.work import WorkResponse
from pydantic import BaseModel
import uuid

router = APIRouter()
logger = logging.getLogger(__name__)


class PublishedChapterResponse(BaseModel):
    """已发布章节响应"""
    id: str
    title: str
    order: int
    word_count: int
    view_count: int
    published_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class LibraryWorkResponse(BaseModel):
    """图书馆作品响应"""
    id: str
    title: str
    description: Optional[str] = None
    cover_image: Optional[str] = None
    genre: str
    status: str
    total_words: int
    total_chapters: int
    view_count: int
    favorite_count: int = 0
    average_rating: float = 0.0
    published_at: Optional[datetime] = None
    author_name: str
    author_id: str
    published_chapter_count: int
    is_featured: bool = False

    class Config:
        from_attributes = True


class LibraryWorkDetailResponse(LibraryWorkResponse):
    """图书馆作品详情响应(包含章节列表)"""
    chapters: List[PublishedChapterResponse]


class LibraryListResponse(BaseModel):
    """图书馆列表响应"""
    total: int
    page: int
    page_size: int
    items: List[LibraryWorkResponse]


@router.get("/featured", response_model=List[LibraryWorkResponse])
async def get_featured_novels(
    db: AsyncSession = Depends(get_db)
):
    """
    获取推荐作品列表(最多5本,用于轮播图)
    """
    # 查询已发布且推荐的作品
    query = (
        select(Work)
        .where(Work.is_published == True, Work.is_featured == True)
        .options(selectinload(Work.author))
        .order_by(Work.published_at.desc())
        .limit(5)
    )

    result = await db.execute(query)
    works = result.scalars().all()

    # 构建响应数据
    items = []
    for work in works:
        # 统计已发布章节数
        published_chapter_count_result = await db.execute(
            select(func.count(Chapter.id)).where(
                Chapter.work_id == work.id,
                Chapter.is_published == True
            )
        )
        published_chapter_count = published_chapter_count_result.scalar() or 0

        # 计算平均评分
        avg_rating_result = await db.execute(
            select(func.avg(WorkRating.rating)).where(
                WorkRating.work_id == work.id
            )
        )
        average_rating = avg_rating_result.scalar() or 0.0

        items.append(LibraryWorkResponse(
            id=str(work.id),
            title=work.title,
            description=work.description,
            cover_image=work.cover_image,
            genre=work.genre.value,
            status=work.status.value,
            total_words=work.total_words,
            total_chapters=work.total_chapters,
            view_count=work.view_count,
            favorite_count=work.favorite_count,
            average_rating=round(average_rating, 1) if average_rating else 0.0,
            published_at=work.published_at,
            author_name=work.author.username,
            author_id=str(work.author_id),
            published_chapter_count=published_chapter_count,
            is_featured=work.is_featured
        ))

    return items


@router.get("/novels", response_model=LibraryListResponse)
async def get_published_novels(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    genre: Optional[WorkGenre] = None,
    search: Optional[str] = None,
    sort_by: str = Query("latest", regex="^(latest|popular|words)$"),
    db: AsyncSession = Depends(get_db)
):
    """
    获取小说广场的已发布作品列表

    - **skip**: 跳过的记录数
    - **limit**: 每页数量
    - **genre**: 作品类型筛选
    - **search**: 搜索关键词(标题或作者名)
    - **sort_by**: 排序方式 (latest=最新发布, popular=最多浏览, words=最多字数)
    """
    # 构建基础查询 - 只获取已发布的作品
    query = select(Work).where(Work.is_published == True)
    count_query = select(func.count(Work.id)).where(Work.is_published == True)

    # 类型筛选
    if genre:
        query = query.where(Work.genre == genre)
        count_query = count_query.where(Work.genre == genre)

    # 搜索功能 - 支持按作品标题或作者名搜索
    if search:
        # 需要 join users 表来搜索作者名
        from app.models.user import User
        query = query.join(Work.author).where(
            or_(
                Work.title.ilike(f"%{search}%"),
                User.username.ilike(f"%{search}%")
            )
        )
        count_query = count_query.join(Work.author).where(
            or_(
                Work.title.ilike(f"%{search}%"),
                User.username.ilike(f"%{search}%")
            )
        )

    # 获取总数
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    # 排序
    if sort_by == "latest":
        query = query.order_by(Work.published_at.desc())
    elif sort_by == "popular":
        query = query.order_by(Work.view_count.desc())
    elif sort_by == "words":
        query = query.order_by(Work.total_words.desc())

    # 分页并加载作者信息
    query = query.options(selectinload(Work.author)).offset(skip).limit(limit)
    result = await db.execute(query)
    works = result.scalars().all()

    # 构建响应数据
    items = []
    for work in works:
        # 统计已发布章节数
        published_chapter_count_result = await db.execute(
            select(func.count(Chapter.id)).where(
                Chapter.work_id == work.id,
                Chapter.is_published == True
            )
        )
        published_chapter_count = published_chapter_count_result.scalar() or 0

        # 计算平均评分
        avg_rating_result = await db.execute(
            select(func.avg(WorkRating.rating)).where(
                WorkRating.work_id == work.id
            )
        )
        average_rating = avg_rating_result.scalar() or 0.0

        items.append(LibraryWorkResponse(
            id=str(work.id),
            title=work.title,
            description=work.description,
            cover_image=work.cover_image,
            genre=work.genre.value,
            status=work.status.value,
            total_words=work.total_words,
            total_chapters=work.total_chapters,
            view_count=work.view_count,
            favorite_count=work.favorite_count,
            average_rating=round(average_rating, 1) if average_rating else 0.0,
            published_at=work.published_at,
            author_name=work.author.username,
            author_id=str(work.author_id),
            published_chapter_count=published_chapter_count,
            is_featured=work.is_featured
        ))

    page = skip // limit + 1

    return LibraryListResponse(
        total=total,
        page=page,
        page_size=limit,
        items=items
    )


@router.get("/novels/{work_id}", response_model=LibraryWorkDetailResponse)
async def get_published_novel_detail(
    work_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    获取已发布作品的详情(包含已发布章节列表)

    - **work_id**: 作品ID
    """
    # 查询作品
    result = await db.execute(
        select(Work)
        .options(selectinload(Work.author))
        .where(Work.id == work_id, Work.is_published == True)
    )
    work = result.scalar_one_or_none()

    if not work:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="作品不存在或未发布"
        )

    # 增加浏览次数
    work.view_count += 1
    await db.commit()

    # 获取已发布的章节列表
    chapters_result = await db.execute(
        select(Chapter)
        .where(
            Chapter.work_id == work_id,
            Chapter.is_published == True
        )
        .order_by(Chapter.order.asc())
    )
    chapters = chapters_result.scalars().all()

    # 统计已发布章节数
    published_chapter_count = len(chapters)

    # 计算平均评分
    avg_rating_result = await db.execute(
        select(func.avg(WorkRating.rating)).where(
            WorkRating.work_id == work_id
        )
    )
    average_rating = avg_rating_result.scalar() or 0.0

    # 构建章节响应数据
    chapter_responses = [
        PublishedChapterResponse(
            id=str(chapter.id),
            title=chapter.title,
            order=chapter.order,
            word_count=chapter.word_count,
            view_count=chapter.view_count,
            published_at=chapter.published_at
        )
        for chapter in chapters
    ]

    return LibraryWorkDetailResponse(
        id=str(work.id),
        title=work.title,
        description=work.description,
        cover_image=work.cover_image,
        genre=work.genre.value,
        status=work.status.value,
        total_words=work.total_words,
        total_chapters=work.total_chapters,
        view_count=work.view_count,
        favorite_count=work.favorite_count,
        average_rating=round(average_rating, 1) if average_rating else 0.0,
        published_at=work.published_at,
        author_name=work.author.username,
        author_id=str(work.author_id),
        published_chapter_count=published_chapter_count,
        chapters=chapter_responses
    )


@router.get("/novels/{work_id}/chapters/{chapter_id}", response_model=dict)
async def get_published_chapter_content(
    work_id: str,
    chapter_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    获取已发布章节的内容

    - **work_id**: 作品ID
    - **chapter_id**: 章节ID
    """
    # 验证作品是否已发布
    work_result = await db.execute(
        select(Work).where(Work.id == work_id, Work.is_published == True)
    )
    work = work_result.scalar_one_or_none()

    if not work:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="作品不存在或未发布"
        )

    # 查询章节
    chapter_result = await db.execute(
        select(Chapter).where(
            Chapter.id == chapter_id,
            Chapter.work_id == work_id,
            Chapter.is_published == True
        )
    )
    chapter = chapter_result.scalar_one_or_none()

    if not chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="章节不存在或未发布"
        )

    # 增加章节浏览次数
    chapter.view_count += 1
    await db.commit()

    return {
        "id": str(chapter.id),
        "work_id": str(work_id),
        "title": chapter.title,
        "content": chapter.content,
        "order": chapter.order,
        "word_count": chapter.word_count,
        "view_count": chapter.view_count,
        "published_at": chapter.published_at
    }


# ========== 书架相关API ==========


class BookshelfItemResponse(LibraryWorkResponse):
    """书架项目响应"""
    last_read_chapter_id: Optional[str] = None
    last_read_chapter_title: Optional[str] = None
    last_read_chapter_order: Optional[int] = None
    last_read_position: int = 0
    last_read_at: Optional[datetime] = None
    added_at: datetime


class BookshelfListResponse(BaseModel):
    """书架列表响应"""
    total: int
    items: List[BookshelfItemResponse]


class UpdateReadingProgressRequest(BaseModel):
    """更新阅读进度请求"""
    chapter_id: str
    position: int = 0


@router.post("/bookshelf/{work_id}", response_model=dict)
async def add_to_bookshelf(
    work_id: str,
    response: Response,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    将作品加入书架（幂等操作）

    - **work_id**: 作品ID

    注意: 该接口设计为幂等操作
    - 新加入书架时返回 201 Created
    - 已在书架中时返回 200 OK
    """
    # 验证作品是否存在且已发布
    work_result = await db.execute(
        select(Work).where(Work.id == work_id, Work.is_published == True)
    )
    work = work_result.scalar_one_or_none()

    if not work:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="作品不存在或未发布"
        )

    # 检查是否已经在书架中
    bookshelf_result = await db.execute(
        select(Bookshelf).where(
            Bookshelf.user_id == current_user.id,
            Bookshelf.work_id == work_id
        )
    )
    existing = bookshelf_result.scalar_one_or_none()

    if existing:
        # 幂等设计：已在书架中时返回 200 OK
        response.status_code = status.HTTP_200_OK
        return {
            "message": "已在书架中",
            "work_id": str(work_id),
            "already_exists": True
        }

    # 添加到书架
    bookshelf_item = Bookshelf(
        user_id=current_user.id,
        work_id=work_id
    )

    db.add(bookshelf_item)

    # 增加作品的收藏数
    work.favorite_count += 1

    # 检查是否需要自动创建作品频道
    # 当收藏数达到 20 且尚未创建频道时，自动创建
    if work.favorite_count == 20:
        # 检查是否已有频道
        existing_channel_result = await db.execute(
            select(Channel).where(
                Channel.work_id == work.id,
                Channel.type == ChannelType.WORK
            )
        )
        existing_channel = existing_channel_result.scalar_one_or_none()

        if not existing_channel:
            # 创建作品频道
            channel = Channel(
                id=uuid.uuid4(),
                name=f"《{work.title}》书友圈",
                description=f"《{work.title}》的读者交流频道",
                type=ChannelType.WORK,
                status=ChannelStatus.ACTIVE,
                work_id=work.id,
                creator_id=work.author_id,  # 作者作为创建者
                is_permanent=False,  # 作品频道默认非永久
                is_pinned=False,
            )
            db.add(channel)

            # 作者自动成为频道管理员
            author_member = ChannelMember(
                id=uuid.uuid4(),
                channel_id=channel.id,
                user_id=work.author_id,
                role=MemberRole.ADMIN
            )
            db.add(author_member)
            channel.member_count = 1

            logger.info(f"Auto-created work channel for work {work.id} ({work.title}) at 20 favorites")

    await db.commit()

    # 新创建时返回 201 Created
    response.status_code = status.HTTP_201_CREATED
    return {
        "message": "已加入书架",
        "work_id": str(work_id),
        "already_exists": False
    }


@router.delete("/bookshelf/{work_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_from_bookshelf(
    work_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    从书架移除作品

    - **work_id**: 作品ID
    """
    # 查询书架项
    bookshelf_result = await db.execute(
        select(Bookshelf).where(
            Bookshelf.user_id == current_user.id,
            Bookshelf.work_id == work_id
        )
    )
    bookshelf_item = bookshelf_result.scalar_one_or_none()

    if not bookshelf_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="该作品不在书架中"
        )

    # 获取作品信息以减少收藏数
    work_result = await db.execute(
        select(Work).where(Work.id == work_id)
    )
    work = work_result.scalar_one_or_none()

    await db.delete(bookshelf_item)

    # 减少作品的收藏数
    if work and work.favorite_count > 0:
        work.favorite_count -= 1

    await db.commit()


@router.get("/bookshelf", response_model=BookshelfListResponse)
async def get_bookshelf(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取我的书架
    """
    # 查询书架项
    bookshelf_result = await db.execute(
        select(Bookshelf)
        .where(Bookshelf.user_id == current_user.id)
        .options(
            selectinload(Bookshelf.work).selectinload(Work.author),
            selectinload(Bookshelf.last_read_chapter)
        )
        .order_by(Bookshelf.last_read_at.desc().nullslast(), Bookshelf.created_at.desc())
    )
    bookshelf_items = bookshelf_result.scalars().all()

    # 构建响应数据
    items = []
    for item in bookshelf_items:
        work = item.work

        # 统计已发布章节数
        published_chapter_count_result = await db.execute(
            select(func.count(Chapter.id)).where(
                Chapter.work_id == work.id,
                Chapter.is_published == True
            )
        )
        published_chapter_count = published_chapter_count_result.scalar() or 0

        # 计算平均评分
        avg_rating_result = await db.execute(
            select(func.avg(WorkRating.rating)).where(
                WorkRating.work_id == work.id
            )
        )
        average_rating = avg_rating_result.scalar() or 0.0

        items.append(BookshelfItemResponse(
            id=str(work.id),
            title=work.title,
            description=work.description,
            cover_image=work.cover_image,
            genre=work.genre.value,
            status=work.status.value,
            total_words=work.total_words,
            total_chapters=work.total_chapters,
            view_count=work.view_count,
            favorite_count=work.favorite_count,
            average_rating=round(average_rating, 1) if average_rating else 0.0,
            published_at=work.published_at,
            author_name=work.author.username,
            author_id=str(work.author_id),
            published_chapter_count=published_chapter_count,
            last_read_chapter_id=str(item.last_read_chapter_id) if item.last_read_chapter_id else None,
            last_read_chapter_title=item.last_read_chapter.title if item.last_read_chapter else None,
            last_read_chapter_order=item.last_read_chapter.order if item.last_read_chapter else None,
            last_read_position=item.last_read_position,
            last_read_at=item.last_read_at,
            added_at=item.created_at
        ))

    return BookshelfListResponse(
        total=len(items),
        items=items
    )


@router.put("/bookshelf/{work_id}/progress", response_model=dict)
async def update_reading_progress(
    work_id: str,
    request: UpdateReadingProgressRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    更新阅读进度

    - **work_id**: 作品ID
    - **request**: 阅读进度信息
    """
    # 查询书架项
    bookshelf_result = await db.execute(
        select(Bookshelf).where(
            Bookshelf.user_id == current_user.id,
            Bookshelf.work_id == work_id
        )
    )
    bookshelf_item = bookshelf_result.scalar_one_or_none()

    if not bookshelf_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="该作品不在书架中,请先添加到书架"
        )

    # 验证章节是否存在且已发布
    chapter_result = await db.execute(
        select(Chapter).where(
            Chapter.id == request.chapter_id,
            Chapter.work_id == work_id,
            Chapter.is_published == True
        )
    )
    chapter = chapter_result.scalar_one_or_none()

    if not chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="章节不存在或未发布"
        )

    # 更新阅读进度
    bookshelf_item.last_read_chapter_id = request.chapter_id
    bookshelf_item.last_read_position = request.position
    bookshelf_item.last_read_at = datetime.now(timezone.utc)

    await db.commit()

    return {
        "message": "阅读进度已更新",
        "chapter_id": str(request.chapter_id),
        "position": request.position
    }


@router.get("/bookshelf/check/{work_id}", response_model=dict)
async def check_in_bookshelf(
    work_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    检查作品是否在书架中

    - **work_id**: 作品ID
    """
    bookshelf_result = await db.execute(
        select(Bookshelf).where(
            Bookshelf.user_id == current_user.id,
            Bookshelf.work_id == work_id
        )
    )
    in_bookshelf = bookshelf_result.scalar_one_or_none() is not None

    return {
        "work_id": str(work_id),
        "in_bookshelf": in_bookshelf
    }
