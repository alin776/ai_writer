"""贴图相关 API"""
from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import Optional, List
from pydantic import BaseModel
import httpx
import uuid

from app.core.database import get_db
from app.core.config import settings
from app.models.user import User
from app.models.user_sticker import UserSticker, UserFavoriteSticker, StickerSource
from app.core.security import get_current_active_user

router = APIRouter(prefix="/stickers", tags=["贴图"])


# ==================== Pydantic 模型 ====================

class TenorSticker(BaseModel):
    """Tenor 贴图"""
    id: str
    url: str
    preview_url: str
    description: Optional[str] = None


class TenorSearchResponse(BaseModel):
    """Tenor 搜索响应"""
    stickers: List[TenorSticker]
    next: Optional[str] = None


class UserStickerResponse(BaseModel):
    """用户贴图响应"""
    id: str
    name: Optional[str]
    image_url: str
    preview_url: Optional[str]
    source: str
    created_at: str


class FavoriteStickerResponse(BaseModel):
    """收藏贴图响应"""
    id: str
    sticker_url: str
    preview_url: Optional[str]
    source: str
    tenor_id: Optional[str]
    created_at: str


class AddFavoriteRequest(BaseModel):
    """添加收藏请求"""
    sticker_url: str
    preview_url: Optional[str] = None
    source: str = "tenor"
    tenor_id: Optional[str] = None


# ==================== Tenor 搜索 API ====================

@router.get("/search", response_model=TenorSearchResponse)
async def search_stickers(
    q: str = Query(..., min_length=1, max_length=100, description="搜索关键词"),
    limit: int = Query(20, ge=1, le=50, description="返回数量"),
    pos: Optional[str] = Query(None, description="分页位置"),
    current_user: User = Depends(get_current_active_user)
):
    """
    搜索 Tenor 静态贴图
    """
    api_key = settings.TENOR_API_KEY
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Tenor API 未配置"
        )

    # 构建 Tenor API 请求
    params = {
        "key": api_key,
        "q": q,
        "limit": limit,
        "contentfilter": "medium",  # 内容过滤级别
    }

    if pos:
        params["pos"] = pos

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                "https://tenor.googleapis.com/v2/search",
                params=params
            )
            response.raise_for_status()
            data = response.json()

        # 解析响应
        stickers = []
        for result in data.get("results", []):
            media_formats = result.get("media_formats", {})

            # 按优先级尝试获取 URL
            url = None
            preview_url = None

            # 原图优先级：gif > mediumgif > tinygif > webp
            for fmt in ["gif", "mediumgif", "tinygif", "webp", "mp4"]:
                if fmt in media_formats and media_formats[fmt].get("url"):
                    url = media_formats[fmt]["url"]
                    break

            # 预览图优先级：tinygif > nanogif > gif
            for fmt in ["tinygif", "nanogif", "gif", "webp"]:
                if fmt in media_formats and media_formats[fmt].get("url"):
                    preview_url = media_formats[fmt]["url"]
                    break

            if url:
                stickers.append(TenorSticker(
                    id=result.get("id", ""),
                    url=url,
                    preview_url=preview_url or url,
                    description=result.get("content_description", "")
                ))

        return TenorSearchResponse(
            stickers=stickers,
            next=data.get("next")
        )

    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Tenor API 请求失败: {e.response.status_code}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"搜索贴图失败: {str(e)}"
        )


@router.get("/trending", response_model=TenorSearchResponse)
async def get_trending_stickers(
    limit: int = Query(20, ge=1, le=50, description="返回数量"),
    pos: Optional[str] = Query(None, description="分页位置"),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取热门贴图
    """
    api_key = settings.TENOR_API_KEY
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Tenor API 未配置"
        )

    params = {
        "key": api_key,
        "limit": limit,
        "searchfilter": "sticker,static",
        "media_filter": "tinygif,gif",
        "contentfilter": "medium",
    }

    if pos:
        params["pos"] = pos

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                "https://tenor.googleapis.com/v2/featured",
                params=params
            )
            response.raise_for_status()
            data = response.json()

        stickers = []
        for result in data.get("results", []):
            media_formats = result.get("media_formats", {})
            url = None
            preview_url = None

            if "tinygif_transparent" in media_formats:
                preview_url = media_formats["tinygif_transparent"].get("url")
            elif "tinygif" in media_formats:
                preview_url = media_formats["tinygif"].get("url")

            if "gif_transparent" in media_formats:
                url = media_formats["gif_transparent"].get("url")
            elif "gif" in media_formats:
                url = media_formats["gif"].get("url")

            if url:
                stickers.append(TenorSticker(
                    id=result.get("id", ""),
                    url=url,
                    preview_url=preview_url or url,
                    description=result.get("content_description", "")
                ))

        return TenorSearchResponse(
            stickers=stickers,
            next=data.get("next")
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取热门贴图失败: {str(e)}"
        )


# ==================== 用户自定义贴图 API ====================

@router.get("/my", response_model=List[UserStickerResponse])
async def get_my_stickers(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取用户自定义贴图列表
    """
    query = (
        select(UserSticker)
        .where(UserSticker.user_id == current_user.id)
        .order_by(UserSticker.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(query)
    stickers = result.scalars().all()

    return [
        UserStickerResponse(
            id=str(s.id),
            name=s.name,
            image_url=s.image_url,
            preview_url=s.preview_url,
            source=s.source.value,
            created_at=s.created_at.isoformat()
        )
        for s in stickers
    ]


@router.post("/upload", response_model=UserStickerResponse)
async def upload_sticker(
    file: UploadFile = File(...),
    name: Optional[str] = None,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    上传自定义贴图
    """
    # 验证文件类型
    allowed_types = ["image/png", "image/jpeg", "image/gif", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不支持的文件类型，仅支持 PNG、JPEG、GIF、WebP"
        )

    # 验证文件大小 (最大 2MB)
    content = await file.read()
    if len(content) > 2 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="文件大小不能超过 2MB"
        )

    # 上传到 COS 存储服务
    from app.services.cos_service import get_cos_service

    try:
        cos_service = get_cos_service()
        file_url = await cos_service.upload_sticker(
            user_id=str(current_user.id),
            filename=file.filename or "sticker.png",
            content=content,
            content_type=file.content_type
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"上传失败: {str(e)}"
        )

    # 创建贴图记录
    sticker = UserSticker(
        user_id=current_user.id,
        name=name or file.filename,
        image_url=file_url,
        preview_url=file_url,  # 暂时使用原图作为预览
        source=StickerSource.UPLOAD
    )

    db.add(sticker)
    await db.commit()
    await db.refresh(sticker)

    return UserStickerResponse(
        id=str(sticker.id),
        name=sticker.name,
        image_url=sticker.image_url,
        preview_url=sticker.preview_url,
        source=sticker.source.value,
        created_at=sticker.created_at.isoformat()
    )


@router.delete("/my/{sticker_id}")
async def delete_my_sticker(
    sticker_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    删除自定义贴图
    """
    try:
        sticker_uuid = uuid.UUID(sticker_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无效的贴图ID"
        )

    query = select(UserSticker).where(
        UserSticker.id == sticker_uuid,
        UserSticker.user_id == current_user.id
    )
    result = await db.execute(query)
    sticker = result.scalar_one_or_none()

    if not sticker:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="贴图不存在"
        )

    await db.delete(sticker)
    await db.commit()

    return {"message": "删除成功"}


# ==================== 收藏贴图 API ====================

@router.get("/favorites", response_model=List[FavoriteStickerResponse])
async def get_favorite_stickers(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取收藏的贴图列表
    """
    query = (
        select(UserFavoriteSticker)
        .where(UserFavoriteSticker.user_id == current_user.id)
        .order_by(UserFavoriteSticker.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(query)
    favorites = result.scalars().all()

    return [
        FavoriteStickerResponse(
            id=str(f.id),
            sticker_url=f.sticker_url,
            preview_url=f.preview_url,
            source=f.source.value,
            tenor_id=f.tenor_id,
            created_at=f.created_at.isoformat()
        )
        for f in favorites
    ]


@router.post("/favorites", response_model=FavoriteStickerResponse)
async def add_favorite_sticker(
    request: AddFavoriteRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    收藏贴图
    """
    # 检查是否已收藏（通过 tenor_id 或 URL 去重）
    existing_query = select(UserFavoriteSticker).where(
        UserFavoriteSticker.user_id == current_user.id
    )

    if request.tenor_id:
        existing_query = existing_query.where(
            UserFavoriteSticker.tenor_id == request.tenor_id
        )
    else:
        existing_query = existing_query.where(
            UserFavoriteSticker.sticker_url == request.sticker_url
        )

    result = await db.execute(existing_query)
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="已收藏该贴图"
        )

    # 创建收藏记录
    source = StickerSource.TENOR if request.source == "tenor" else StickerSource.UPLOAD
    favorite = UserFavoriteSticker(
        user_id=current_user.id,
        sticker_url=request.sticker_url,
        preview_url=request.preview_url,
        source=source,
        tenor_id=request.tenor_id
    )

    db.add(favorite)
    await db.commit()
    await db.refresh(favorite)

    return FavoriteStickerResponse(
        id=str(favorite.id),
        sticker_url=favorite.sticker_url,
        preview_url=favorite.preview_url,
        source=favorite.source.value,
        tenor_id=favorite.tenor_id,
        created_at=favorite.created_at.isoformat()
    )


@router.delete("/favorites/{favorite_id}")
async def remove_favorite_sticker(
    favorite_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    取消收藏贴图
    """
    try:
        favorite_uuid = uuid.UUID(favorite_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无效的收藏ID"
        )

    query = select(UserFavoriteSticker).where(
        UserFavoriteSticker.id == favorite_uuid,
        UserFavoriteSticker.user_id == current_user.id
    )
    result = await db.execute(query)
    favorite = result.scalar_one_or_none()

    if not favorite:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="收藏不存在"
        )

    await db.delete(favorite)
    await db.commit()

    return {"message": "取消收藏成功"}
