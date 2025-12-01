"""
图书分析API路由
"""

import os
import shutil
from pathlib import Path
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Query, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.core.database import get_db
from app.core.security import get_current_user
from app.core.config import settings
from app.models.user import User
from app.models.book_analysis import BookAnalysisJob, JobStatus
from app.models.worldview_suggestion import WorldviewSuggestion, SuggestionStatus
from app.schemas.book_analysis import (
    BookAnalysisJobCreate,
    BookAnalysisJobResponse,
    BookAnalysisJobListResponse,
    BookAnalysisJobStatusResponse,
    WorldviewSuggestionListResponse,
    WorldviewSuggestionResponse,
    AdoptSuggestionRequest,
    AdoptSuggestionResponse,
    UpdateSuggestionRequest,
    CostEstimateResponse
)
from app.services.book_analysis_service import BookAnalysisService
from app.services.ai.http_ai_service import HTTPAIService
from app.services.knowledge_service import KnowledgeService
from app.core.database import create_db_session


router = APIRouter()

# 上传文件存储目录
UPLOAD_DIR = Path("uploads/books")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# 支持的文件格式
ALLOWED_EXTENSIONS = {".txt", ".epub", ".pdf"}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB


async def run_analysis_task(job_id: UUID, user_id: UUID):
    """后台分析任务包装器 - 使用独立的数据库会话"""
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"🚀 开始执行后台分析任务: job_id={job_id}, user_id={user_id}")

    async with create_db_session() as db:
        try:
            logger.info(f"✅ 数据库会话创建成功")
            # 使用图书分析专用模型和超时配置
            # 2025-12-01: 传递db和user_id以启用成本追踪
            ai_service = HTTPAIService(
                db=db,
                user_id=user_id,
                model=settings.BOOK_ANALYSIS_MODEL,
                timeout=settings.BOOK_ANALYSIS_TIMEOUT
            )
            logger.info(f"✅ AI服务初始化成功")
            knowledge_service = KnowledgeService(db)
            logger.info(f"✅ 知识库服务初始化成功")
            service = BookAnalysisService(db, ai_service, knowledge_service)
            logger.info(f"✅ 图书分析服务初始化成功,开始分析...")
            await service.analyze_book(job_id, user_id)
            logger.info(f"🎉 图书分析任务完成: job_id={job_id}")
        except Exception as e:
            logger.error(f"❌ 图书分析任务失败 {job_id}: {str(e)}", exc_info=True)


@router.post("/upload", response_model=BookAnalysisJobResponse)
async def upload_book(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    book_title: Optional[str] = None,
    strategy_id: str = "web_novel_11d",
    work_id: Optional[UUID] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    上传图书并启动分析任务

    Args:
        file: 图书文件 (.txt/.epub/.pdf)
        book_title: 图书标题 (可选,默认使用文件名)
        strategy_id: 分析策略ID
        work_id: 关联作品ID (可选)
    """
    # 验证文件类型
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, f"不支持的文件格式,仅支持: {', '.join(ALLOWED_EXTENSIONS)}")

    # 读取文件
    content = await file.read()
    file_size = len(content)

    # 验证文件大小
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(400, f"文件过大,最大支持 {MAX_FILE_SIZE // 1024 // 1024}MB")

    # 保存文件
    from uuid import uuid4
    file_path = UPLOAD_DIR / f"{uuid4()}{file_ext}"
    with open(file_path, 'wb') as f:
        f.write(content)

    # 创建分析任务
    # 使用图书分析专用模型
    # 2025-12-01: 传递db和user_id以启用成本追踪
    ai_service = HTTPAIService(
        db=db,
        user_id=str(current_user.id),
        model=settings.BOOK_ANALYSIS_MODEL,
        timeout=settings.BOOK_ANALYSIS_TIMEOUT
    )
    knowledge_service = KnowledgeService(db)
    service = BookAnalysisService(db, ai_service, knowledge_service)

    try:
        job = await service.create_job(
            file_path=str(file_path),
            original_filename=file.filename,
            file_size_bytes=file_size,
            user_id=current_user.id,
            book_title=book_title,
            strategy_id=strategy_id,
            work_id=work_id
        )

        # 启动后台分析任务 (使用独立的数据库会话)
        background_tasks.add_task(run_analysis_task, job.id, current_user.id)

        return BookAnalysisJobResponse.from_orm(job)

    except ValueError as e:
        # 删除文件
        os.remove(file_path)
        raise HTTPException(400, str(e))


@router.get("/jobs/{job_id}", response_model=BookAnalysisJobResponse)
async def get_job(
    job_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取任务详情"""
    job = await db.get(BookAnalysisJob, job_id)
    if not job:
        raise HTTPException(404, "任务不存在")

    if job.user_id != current_user.id:
        raise HTTPException(403, "无权访问该任务")

    return BookAnalysisJobResponse.from_orm(job)


@router.get("/jobs/{job_id}/status", response_model=BookAnalysisJobStatusResponse)
async def get_job_status(
    job_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取任务状态 (轻量级)"""
    job = await db.get(BookAnalysisJob, job_id)
    if not job:
        raise HTTPException(404, "任务不存在")

    if job.user_id != current_user.id:
        raise HTTPException(403, "无权访问该任务")

    return BookAnalysisJobStatusResponse(
        id=job.id,
        status=job.status,
        progress=job.progress,
        current_step=job.current_step,
        error_message=job.error_message
    )


@router.get("/jobs", response_model=BookAnalysisJobListResponse)
async def list_jobs(
    status: Optional[JobStatus] = None,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取任务列表"""
    query = select(BookAnalysisJob).where(
        BookAnalysisJob.user_id == current_user.id
    )

    if status:
        query = query.where(BookAnalysisJob.status == status)

    query = query.order_by(BookAnalysisJob.created_at.desc())

    # 获取总数
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()

    # 分页
    query = query.limit(limit).offset(offset)
    result = await db.execute(query)
    jobs = result.scalars().all()

    return BookAnalysisJobListResponse(
        jobs=[BookAnalysisJobResponse.from_orm(job) for job in jobs],
        total=total
    )


@router.delete("/jobs/{job_id}")
async def delete_job(
    job_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除任务"""
    job = await db.get(BookAnalysisJob, job_id)
    if not job:
        raise HTTPException(404, "任务不存在")

    if job.user_id != current_user.id:
        raise HTTPException(403, "无权操作该任务")

    # 删除文件
    if job.file_path and os.path.exists(job.file_path):
        os.remove(job.file_path)

    # 删除任务 (级联删除建议)
    await db.delete(job)
    await db.commit()

    return {"success": True, "message": "任务已删除"}


@router.get("/jobs/{job_id}/suggestions", response_model=WorldviewSuggestionListResponse)
async def get_suggestions(
    job_id: UUID,
    status: Optional[SuggestionStatus] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取智能建议列表"""
    # 验证任务权限
    job = await db.get(BookAnalysisJob, job_id)
    if not job:
        raise HTTPException(404, "任务不存在")
    if job.user_id != current_user.id:
        raise HTTPException(403, "无权访问该任务")

    # 查询建议
    query = select(WorldviewSuggestion).where(
        WorldviewSuggestion.job_id == job_id
    )

    if status:
        query = query.where(WorldviewSuggestion.status == status)

    query = query.order_by(WorldviewSuggestion.confidence_score.desc())
    result = await db.execute(query)
    suggestions = result.scalars().all()

    # 统计
    by_type = {}
    by_status = {}
    for s in suggestions:
        by_type[s.suggestion_type.value] = by_type.get(s.suggestion_type.value, 0) + 1
        by_status[s.status.value] = by_status.get(s.status.value, 0) + 1

    return WorldviewSuggestionListResponse(
        suggestions=[WorldviewSuggestionResponse.from_orm(s) for s in suggestions],
        total=len(suggestions),
        by_type=by_type,
        by_status=by_status
    )


@router.post("/jobs/{job_id}/adopt", response_model=AdoptSuggestionResponse)
async def adopt_suggestions(
    job_id: UUID,
    request: AdoptSuggestionRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    批量采纳建议

    TODO: 实现实际的采纳逻辑 (创建世界观元素)
    目前仅更新状态
    """
    # 验证任务权限
    job = await db.get(BookAnalysisJob, job_id)
    if not job:
        raise HTTPException(404, "任务不存在")
    if job.user_id != current_user.id:
        raise HTTPException(403, "无权操作该任务")

    adopted_count = 0
    failed_count = 0
    created_elements = []
    errors = []

    from datetime import datetime

    for suggestion_id in request.suggestion_ids:
        suggestion = await db.get(WorldviewSuggestion, suggestion_id)
        if not suggestion:
            errors.append(f"建议不存在: {suggestion_id}")
            failed_count += 1
            continue

        if suggestion.job_id != job_id:
            errors.append(f"建议不属于该任务: {suggestion_id}")
            failed_count += 1
            continue

        # TODO: 实际创建世界观元素的逻辑
        # 目前仅更新状态
        suggestion.status = SuggestionStatus.ADOPTED
        suggestion.adopted_at = datetime.utcnow()
        # suggestion.adopted_as_id = created_element.id

        created_elements.append({
            "suggestion_id": str(suggestion.id),
            "type": suggestion.suggestion_type.value,
            "data": suggestion.suggested_data
        })

        adopted_count += 1

    await db.commit()

    return AdoptSuggestionResponse(
        success=failed_count == 0,
        adopted_count=adopted_count,
        failed_count=failed_count,
        created_elements=created_elements,
        errors=errors
    )


@router.patch("/suggestions/{suggestion_id}", response_model=WorldviewSuggestionResponse)
async def update_suggestion(
    suggestion_id: UUID,
    request: UpdateSuggestionRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """修改单个建议"""
    suggestion = await db.get(WorldviewSuggestion, suggestion_id)
    if not suggestion:
        raise HTTPException(404, "建议不存在")

    if suggestion.user_id != current_user.id:
        raise HTTPException(403, "无权修改该建议")

    # 更新字段
    if request.suggested_data is not None:
        suggestion.suggested_data = request.suggested_data

    if request.status is not None:
        suggestion.status = request.status

    if request.user_notes is not None:
        suggestion.user_notes = request.user_notes

    await db.commit()
    await db.refresh(suggestion)

    return WorldviewSuggestionResponse.from_orm(suggestion)
