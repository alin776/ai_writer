"""
知识库API路由
"""
import json
import io
from typing import Optional, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File, Form
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.knowledge_item import KnowledgeCategory, KnowledgeItem, KnowledgeSource
from app.schemas.knowledge import (
    KnowledgeItemCreate,
    KnowledgeItemUpdate,
    KnowledgeItemResponse,
    KnowledgeItemListResponse,
    KnowledgeSearchRequest,
    KnowledgeSearchResponse,
    KnowledgeSearchResult
)
from app.services.knowledge_service import KnowledgeService

router = APIRouter()
MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5MB


@router.post("", response_model=KnowledgeItemResponse, status_code=status.HTTP_201_CREATED)
async def create_knowledge_item(
    data: KnowledgeItemCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    创建知识条目

    - **title**: 标题
    - **content**: 内容
    - **category**: 分类
    - **tags**: 标签列表
    - **source_type**: 来源类型
    - **source_reference**: 来源说明
    - **work_id**: 关联作品ID（可选）
    - **chapter_id**: 关联章节ID（可选）
    """
    service = KnowledgeService(db)
    item = await service.create_item(
        user_id=str(current_user.id),
        data=data
    )
    return item


@router.get("", response_model=KnowledgeItemListResponse)
async def get_knowledge_items(
    skip: int = Query(0, ge=0, description="跳过数量"),
    limit: int = Query(20, ge=1, le=100, description="每页大小"),
    category: Optional[KnowledgeCategory] = Query(None, description="分类过滤"),
    tags: Optional[str] = Query(None, description="标签过滤(逗号分隔)"),
    work_id: Optional[str] = Query(None, description="作品ID过滤"),
    search: Optional[str] = Query(None, description="Search keyword"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取知识条目列表

    支持分类、标签、作品、关键词过滤和分页
    """
    service = KnowledgeService(db)

    # 解析标签
    tag_list = None
    if tags:
        tag_list = [t.strip() for t in tags.split(",") if t.strip()]

    items, total = await service.get_items(
        user_id=str(current_user.id),
        skip=skip,
        limit=limit,
        category=category,
        tags=tag_list,
        work_id=work_id,
        search=search
    )

    page = skip // limit + 1

    return KnowledgeItemListResponse(
        total=total,
        page=page,
        page_size=limit,
        items=items
    )


@router.get("/tags", response_model=List[str])
async def get_knowledge_tags(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """获取当前用户的标签列表（去重）"""
    stmt = (
        select(func.distinct(func.unnest(KnowledgeItem.tags)))
        .where(KnowledgeItem.user_id == current_user.id)
    )
    result = await db.execute(stmt)
    tags = [row[0] for row in result.fetchall() if row[0]]
    return tags


@router.get("/titles", response_model=List[dict])
async def get_knowledge_titles(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """获取当前用户的知识库文档列表（id + title），用于@引用选择"""
    stmt = (
        select(KnowledgeItem.id, KnowledgeItem.title)
        .where(KnowledgeItem.user_id == current_user.id)
        .order_by(KnowledgeItem.updated_at.desc())
    )
    result = await db.execute(stmt)
    docs = [{"id": str(row[0]), "title": row[1]} for row in result.fetchall()]
    return docs


@router.get("/{item_id}", response_model=KnowledgeItemResponse)
async def get_knowledge_item(
    item_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """获取知识条目详情"""
    service = KnowledgeService(db)
    item = await service.get_item(
        item_id=item_id,
        user_id=str(current_user.id),
        increment_view=True
    )

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Knowledge item not found or access denied"
        )

    return item


@router.put("/{item_id}", response_model=KnowledgeItemResponse)
async def update_knowledge_item(
    item_id: UUID,
    data: KnowledgeItemUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """更新知识条目"""
    service = KnowledgeService(db)
    item = await service.update_item(
        item_id=item_id,
        user_id=str(current_user.id),
        data=data
    )

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Knowledge item not found or access denied"
        )

    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_knowledge_item(
    item_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """删除知识条目"""
    service = KnowledgeService(db)
    success = await service.delete_item(
        item_id=item_id,
        user_id=str(current_user.id)
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Knowledge item not found or access denied"
        )


@router.post("/search", response_model=KnowledgeSearchResponse)
async def search_knowledge(
    request: KnowledgeSearchRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    语义搜索知识库

    使用RAG向量检索技术，根据语义相似度搜索相关知识条目
    """
    service = KnowledgeService(db)

    results = await service.search_by_semantic(
        user_id=str(current_user.id),
        query=request.query,
        category=request.category,
        tags=request.tags,
        work_id=str(request.work_id) if request.work_id else None,
        top_k=request.top_k
    )

    # 转换为响应格式
    search_results = [
        KnowledgeSearchResult(
            item=result['item'],
            relevance_score=result['relevance_score'],
            highlight=result['highlight']
        )
        for result in results
    ]

    return KnowledgeSearchResponse(
        query=request.query,
        total=len(search_results),
        results=search_results
    )


@router.post("/upload", response_model=KnowledgeItemResponse, status_code=status.HTTP_201_CREATED)
async def upload_knowledge_item(
    file: UploadFile = File(..., description="知识库文件，支持 txt/markdown/pdf/docx（自动提取文本）"),
    title: str = Form(...),
    category: KnowledgeCategory = Form(...),
    tags: Optional[str] = Form(None, description="标签，逗号分隔或JSON数组"),
    source_reference: Optional[str] = Form(None, description="来源说明"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    上传文件并创建知识条目（读取文本内容存储）
    """
    try:
        content_bytes = await file.read()

        if len(content_bytes) == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="文件为空")
        if len(content_bytes) > MAX_UPLOAD_SIZE:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="文件过大，限制5MB")

        content_text = _extract_text_from_upload(file, content_bytes)

        if not content_text.strip():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="未提取到有效文本内容")

        # 解析标签
        tag_list: List[str] = []
        if tags:
            try:
                parsed = json.loads(tags)
                if isinstance(parsed, list):
                    tag_list = [str(t).strip() for t in parsed if str(t).strip()]
                else:
                    tag_list = [t.strip() for t in tags.split(",") if t.strip()]
            except json.JSONDecodeError:
                tag_list = [t.strip() for t in tags.split(",") if t.strip()]

        service = KnowledgeService(db)
        item = await service.create_item(
            user_id=str(current_user.id),
            data=KnowledgeItemCreate(
                title=title,
                content=content_text,
                category=category,
                tags=tag_list,
                source_type=KnowledgeSource.IMPORTED,
                source_reference=source_reference or file.filename,
                extra_data={
                    "filename": file.filename,
                    "content_type": file.content_type,
                    "size": len(content_bytes)
                }
            )
        )
        return item
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


def _extract_text_from_upload(file: UploadFile, content_bytes: bytes) -> str:
    """
    根据文件类型提取文本内容
    支持 txt/markdown/pdf/docx，自动检测编码
    """
    filename = file.filename or ""
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

    if ext in ["txt", "md", "markdown", ""]:
        # 尝试多种编码
        encodings = ["utf-8", "gbk", "gb2312", "gb18030", "utf-16", "big5"]
        for encoding in encodings:
            try:
                return content_bytes.decode(encoding)
            except (UnicodeDecodeError, LookupError):
                continue
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="无法识别文件编码，请转换为UTF-8后重试")

    if ext == "pdf":
        try:
            import pdfplumber
        except ImportError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="服务器未安装 pdfplumber，暂不支持 PDF 上传")
        with pdfplumber.open(io.BytesIO(content_bytes)) as pdf:
            texts = [page.extract_text() or "" for page in pdf.pages]
        return "\n".join(t for t in texts if t)

    if ext == "docx":
        try:
            from docx import Document
        except ImportError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="服务器未安装 python-docx，暂不支持 DOCX 上传")
        doc = Document(io.BytesIO(content_bytes))
        paragraphs = [p.text for p in doc.paragraphs if p.text]
        return "\n".join(paragraphs)

    # 默认尝试多种编码
    encodings = ["utf-8", "gbk", "gb2312", "gb18030", "utf-16", "big5"]
    for encoding in encodings:
        try:
            return content_bytes.decode(encoding)
        except (UnicodeDecodeError, LookupError):
            continue
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Unsupported file type or encoding"
    )


@router.post("/{item_id}/reference", status_code=status.HTTP_200_OK)
async def increment_reference_count(
    item_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    增加引用次数

    当用户在编辑器中引用该知识条目时调用
    """
    service = KnowledgeService(db)
    success = await service.increment_reference_count(
        item_id=item_id,
        user_id=str(current_user.id)
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Knowledge item not found or access denied"
        )

    return {"message": "Reference count incremented"}
