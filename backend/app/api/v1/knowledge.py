"""
鐭ヨ瘑搴揂PI璺敱
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
    鍒涘缓鐭ヨ瘑鏉＄洰

    - **title**: 鏍囬
    - **content**: 鍐呭
    - **category**: 鍒嗙被
    - **tags**: 鏍囩鍒楄〃
    - **source_type**: 鏉ユ簮绫诲瀷
    - **source_reference**: 鏉ユ簮璇存槑
    - **work_id**: 鍏宠仈浣滃搧ID锛堝彲閫夛級
    - **chapter_id**: 鍏宠仈绔犺妭ID锛堝彲閫夛級
    """
    service = KnowledgeService(db)
    item = await service.create_item(
        user_id=str(current_user.id),
        data=data
    )
    return item


@router.get("", response_model=KnowledgeItemListResponse)
async def get_knowledge_items(
    skip: int = Query(0, ge=0, description="璺宠繃鏁伴噺"),
    limit: int = Query(20, ge=1, le=100, description="姣忛〉澶у皬"),
    category: Optional[KnowledgeCategory] = Query(None, description="鍒嗙被杩囨护"),
    tags: Optional[str] = Query(None, description="鏍囩杩囨护(閫楀彿鍒嗛殧)"),
    work_id: Optional[str] = Query(None, description="浣滃搧ID杩囨护"),
    search: Optional[str] = Query(None, description="Search keyword"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    鑾峰彇鐭ヨ瘑鏉＄洰鍒楄〃

    鏀寔鍒嗙被銆佹爣绛俱€佷綔鍝併€佸叧閿瘝杩囨护鍜屽垎椤?
    """
    service = KnowledgeService(db)

    # 瑙ｆ瀽鏍囩
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
    """鑾峰彇褰撳墠鐢ㄦ埛鐨勬爣绛惧垪琛紙鍘婚噸锛?"""
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
    """鑾峰彇褰撳墠鐢ㄦ埛鐨勭煡璇嗗簱鏂囨。鍒楄〃锛坕d + title锛夛紝鐢ㄤ簬@寮曠敤閫夋嫨"""
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
    """鑾峰彇鐭ヨ瘑鏉＄洰璇︽儏"""
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
    """鏇存柊鐭ヨ瘑鏉＄洰"""
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
    """鍒犻櫎鐭ヨ瘑鏉＄洰"""
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
    璇箟鎼滅储鐭ヨ瘑搴?

    浣跨敤RAG鍚戦噺妫€绱㈡妧鏈紝鏍规嵁璇箟鐩镐技搴︽悳绱㈢浉鍏崇煡璇嗘潯鐩?
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

    # 杞崲涓哄搷搴旀牸寮?
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
    file: UploadFile = File(..., description="鐭ヨ瘑搴撴枃浠讹紝鏀寔 txt/markdown/pdf/docx锛堣嚜鍔ㄦ彁鍙栨枃鏈級"),
    title: str = Form(...),
    category: KnowledgeCategory = Form(...),
    tags: Optional[str] = Form(None, description="鏍囩锛岄€楀彿鍒嗛殧鎴?JSON 鏁扮粍"),
    source_reference: Optional[str] = Form(None, description="鏉ユ簮璇存槑"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    涓婁紶鏂囦欢骞跺垱寤虹煡璇嗘潯鐩紙璇诲彇鏂囨湰鍐呭瀛樺偍锛?
    """
    try:
        content_bytes = await file.read()

        if len(content_bytes) == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="鏂囦欢涓虹┖")
        if len(content_bytes) > MAX_UPLOAD_SIZE:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="鏂囦欢杩囧ぇ锛岄檺鍒?5MB")

        content_text = _extract_text_from_upload(file, content_bytes)
        if not content_text.strip():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="鏈彁鍙栧埌鏈夋晥鏂囨湰鍐呭")

        # 瑙ｆ瀽鏍囩
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
    鏍规嵁鏂囦欢绫诲瀷鎻愬彇鏂囨湰鍐呭
    鏀寔 txt/markdown/pdf/docx锛岄粯璁ゅ皾璇?UTF-8 瑙ｇ爜
    """
    filename = file.filename or ""
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

    if ext in ["txt", "md", "markdown", ""]:
        try:
            return content_bytes.decode("utf-8")
        except UnicodeDecodeError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="浠呮敮鎸?UTF-8 鏂囨湰鏂囦欢")

    if ext == "pdf":
        try:
            import pdfplumber
        except ImportError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="鏈嶅姟鍣ㄦ湭瀹夎 pdfplumber锛屾殏涓嶆敮鎸?PDF 涓婁紶")
        with pdfplumber.open(io.BytesIO(content_bytes)) as pdf:
            texts = [page.extract_text() or "" for page in pdf.pages]
        return "\n".join(t for t in texts if t)

    if ext == "docx":
        try:
            from docx import Document
        except ImportError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="鏈嶅姟鍣ㄦ湭瀹夎 python-docx锛屾殏涓嶆敮鎸?DOCX 涓婁紶")
        doc = Document(io.BytesIO(content_bytes))
        paragraphs = [p.text for p in doc.paragraphs if p.text]
        return "\n".join(paragraphs)

    # 榛樿灏濊瘯 UTF-8 瑙ｇ爜
    try:
        return content_bytes.decode("utf-8")
    except UnicodeDecodeError:
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
    澧炲姞寮曠敤娆℃暟

    褰撶敤鎴峰湪缂栬緫鍣ㄤ腑寮曠敤璇ョ煡璇嗘潯鐩椂璋冪敤
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
