"""
评审相关 API 路由
提供章节评审、任务管理、版本管理的接口
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID
import logging

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.schemas.review import (
    ReviewSessionCreate,
    ReviewSessionResponse,
    ChapterReviewResponse,
    ReviewTaskCreate,
    ReviewTaskUpdate,
    ReviewTaskResponse,
    ReviewTaskStatusUpdate,
    ReviewTaskListResponse,
    TaskStatsResponse,
    BatchOperationRequest,
    ChapterVersionCreate,
    ChapterVersionResponse,
    ChapterVersionDetailResponse,
    ChapterVersionListResponse,
    VersionMilestoneUpdate,
    TaskPriorityEnum,
    TaskStatusEnum,
    ParagraphReviewRequest,
    ParagraphReviewResponse,
    BookReviewRequest,
    BookReviewResponse
)
from app.services.review.novel_review_service import NovelReviewService
from app.services.review.task_generator_service import TaskGeneratorService
from app.services.review.version_manager_service import VersionManagerService
from app.services.chapter_service import ChapterService

logger = logging.getLogger(__name__)

router = APIRouter()


# ==================== 评审接口 ====================

@router.post("/chapters/{chapter_id}/review", response_model=ChapterReviewResponse)
async def review_chapter(
    chapter_id: UUID,
    request: ReviewSessionCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    发起章节评审

    - **chapter_id**: 章节ID
    - **review_type**: 评审深度 (quick/standard/deep)
    - **auto_generate_tasks**: 是否自动生成任务
    - **create_version**: 是否创建版本快照
    """
    logger.info(
        f"[POST /review/chapters/{chapter_id}] user_id={current_user.id}, "
        f"review_type={request.review_type}"
    )

    # 验证章节权限
    chapter_service = ChapterService(db)
    chapter = await chapter_service.get_chapter_by_id(str(chapter_id))

    if not chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="章节不存在"
        )

    # TODO: 验证作品权限 (通过 chapter.work_id)

    # 1. 执行评审
    review_service = NovelReviewService(db)
    session = await review_service.review_chapter(
        chapter_id=chapter_id,
        user_id=current_user.id,
        request=request
    )

    # 2. 自动生成任务 (如果需要)
    generated_tasks = []
    if request.auto_generate_tasks:
        task_service = TaskGeneratorService(db)
        generated_tasks = await task_service.generate_tasks_from_review(
            review_session_id=session.id,
            chapter_id=chapter_id,
            user_id=current_user.id
        )

    # 3. 创建版本快照 (如果需要)
    version = None
    if request.create_version:
        version_service = VersionManagerService(db)
        version = await version_service.create_version(
            chapter_id=chapter_id,
            user_id=current_user.id,
            request=ChapterVersionCreate(
                is_milestone=False,
                version_tag="评审后版本",
                change_summary=f"评审总分: {session.overall_score}"
            ),
            review_session_id=session.id
        )

    logger.info(
        f"[POST /review/chapters/{chapter_id}] 评审完成: session_id={session.id}, "
        f"tasks={len(generated_tasks)}, version={version.id if version else None}"
    )

    return ChapterReviewResponse(
        session=session,
        generated_tasks=[ReviewTaskResponse.model_validate(t) for t in generated_tasks],
        version=ChapterVersionResponse.model_validate(version) if version else None
    )


@router.get("/sessions/{session_id}", response_model=ReviewSessionResponse)
async def get_review_session(
    session_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """获取评审结果"""
    review_service = NovelReviewService(db)
    session = await review_service.get_review_session(session_id)

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="评审会话不存在"
        )

    if session.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权访问此评审结果"
        )

    return ReviewSessionResponse.model_validate(session)


@router.get("/chapters/{chapter_id}/review-history", response_model=List[ReviewSessionResponse])
async def get_chapter_review_history(
    chapter_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=50),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """获取章节的评审历史"""
    review_service = NovelReviewService(db)
    sessions = await review_service.get_chapter_review_history(
        chapter_id=chapter_id,
        skip=skip,
        limit=limit
    )

    return [ReviewSessionResponse.model_validate(s) for s in sessions]


# ==================== 任务管理接口 ====================

@router.get("/chapters/{chapter_id}/tasks", response_model=ReviewTaskListResponse)
async def get_chapter_tasks(
    chapter_id: UUID,
    status: Optional[TaskStatusEnum] = Query(None),
    priority: Optional[TaskPriorityEnum] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取章节的任务清单

    - **status**: 任务状态筛选 (pending/in_progress/completed/skipped)
    - **priority**: 优先级筛选 (P0/P1/P2)
    - **limit**: 返回记录数，范围 1-100（默认20）
    """
    task_service = TaskGeneratorService(db)
    tasks = await task_service.get_tasks_by_chapter(
        chapter_id=chapter_id,
        status=status,
        priority=priority,
        skip=skip,
        limit=limit
    )

    return ReviewTaskListResponse(
        total=len(tasks),
        items=[ReviewTaskResponse.model_validate(t) for t in tasks]
    )


@router.post("/tasks", response_model=ReviewTaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    request: ReviewTaskCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """手动创建任务"""
    task_service = TaskGeneratorService(db)
    task = await task_service.create_manual_task(
        user_id=current_user.id,
        request=request
    )

    logger.info(f"[POST /tasks] 手动创建任务: task_id={task.id}")

    return ReviewTaskResponse.model_validate(task)


@router.patch("/tasks/{task_id}", response_model=ReviewTaskResponse)
async def update_task(
    task_id: UUID,
    request: ReviewTaskUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """更新任务"""
    task_service = TaskGeneratorService(db)

    try:
        task = await task_service.update_task(task_id, request)
        return ReviewTaskResponse.model_validate(task)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.patch("/tasks/{task_id}/status", response_model=ReviewTaskResponse)
async def update_task_status(
    task_id: UUID,
    request: ReviewTaskStatusUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """更新任务状态"""
    task_service = TaskGeneratorService(db)

    try:
        task = await task_service.update_task_status(task_id, request)
        return ReviewTaskResponse.model_validate(task)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/tasks/batch-operations")
async def batch_operations(
    request: BatchOperationRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    批量操作任务

    - **action**: complete/skip/delete/update_priority/reorder
    - **task_ids**: 任务ID列表
    """
    task_service = TaskGeneratorService(db)
    result = await task_service.batch_operation(request)

    logger.info(
        f"[POST /tasks/batch-operations] action={request.action}, "
        f"success={result['success']}, failed={result['failed']}"
    )

    return result


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """删除任务"""
    task_service = TaskGeneratorService(db)
    await task_service.delete_task(task_id)
    logger.info(f"[DELETE /tasks/{task_id}] 任务已删除")


@router.get("/tasks/stats", response_model=TaskStatsResponse)
async def get_task_stats(
    chapter_id: Optional[UUID] = Query(None),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """获取任务统计"""
    task_service = TaskGeneratorService(db)
    stats = await task_service.get_task_stats(
        chapter_id=chapter_id,
        user_id=current_user.id
    )

    return stats


# ==================== 版本管理接口 ====================

@router.post("/chapters/{chapter_id}/versions", response_model=ChapterVersionResponse, status_code=status.HTTP_201_CREATED)
async def create_chapter_version(
    chapter_id: UUID,
    request: ChapterVersionCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """创建章节版本快照"""
    version_service = VersionManagerService(db)

    version = await version_service.create_version(
        chapter_id=chapter_id,
        user_id=current_user.id,
        request=request
    )

    logger.info(
        f"[POST /chapters/{chapter_id}/versions] 版本创建成功: "
        f"version_id={version.id}, version_number={version.version_number}"
    )

    return ChapterVersionResponse.model_validate(version)


@router.get("/chapters/{chapter_id}/versions", response_model=ChapterVersionListResponse)
async def get_chapter_versions(
    chapter_id: UUID,
    milestones_only: bool = Query(False),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """获取章节的版本列表"""
    version_service = VersionManagerService(db)

    versions = await version_service.get_chapter_versions(
        chapter_id=chapter_id,
        include_milestones_only=milestones_only,
        skip=skip,
        limit=limit
    )

    return ChapterVersionListResponse(
        total=len(versions),
        versions=[ChapterVersionResponse.model_validate(v) for v in versions]
    )


@router.get("/versions/{version_id}", response_model=ChapterVersionDetailResponse)
async def get_version_detail(
    version_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """获取版本详情 (包含内容)"""
    version_service = VersionManagerService(db)

    version = await version_service.get_version_by_id(version_id)
    if not version:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="版本不存在"
        )

    # 获取完整内容
    content = await version_service.get_version_content(version_id)

    response = ChapterVersionDetailResponse.model_validate(version)
    response.content = content

    return response


@router.patch("/versions/{version_id}/milestone", response_model=ChapterVersionResponse)
async def update_version_milestone(
    version_id: UUID,
    request: VersionMilestoneUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """更新版本的里程碑状态"""
    version_service = VersionManagerService(db)

    try:
        version = await version_service.update_milestone_status(version_id, request)
        return ChapterVersionResponse.model_validate(version)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/versions/compare")
async def compare_versions(
    version1_id: UUID = Query(...),
    version2_id: UUID = Query(...),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """对比两个版本"""
    version_service = VersionManagerService(db)

    try:
        result = await version_service.compare_versions(version1_id, version2_id)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


# ==================== 段落级评审接口 ====================

@router.post(
    "/paragraphs",
    response_model=ParagraphReviewResponse,
    summary="段落级评审",
    description="对选中的段落进行快速4维度评审 (5秒内返回)"
)
async def review_paragraph(
    request: ParagraphReviewRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    段落级评审

    **使用场景**:
    - 用户正在编辑器中写作
    - 选中一段文字 (50-2000字)
    - 想要即时反馈: "这段写得怎么样?"

    **评审维度** (4个):
    1. 语言质量 - 文字流畅度、修辞手法
    2. 描写生动度 - 画面感、细节描写
    3. 对话真实性 - 符合人物性格、对话自然
    4. 情感表达 - 感染力、情绪传递

    **特点**:
    - ⚡ 快速 - 5秒内返回
    - 🎯 聚焦 - 只评价这一段
    - 💡 即时 - 边写边改
    - 💾 缓存 - 相同文本1小时内不重复调用AI

    **参数**:
    - **text**: 段落文本 (50-2000字)
    - **context**: 上下文信息 (可选，帮助AI理解段落含义)

    **返回**:
    - overall_score: 总分 (0-100)
    - dimension_scores: 4维度评分
    - quick_feedback: 简短反馈
    - suggestions: 改进建议列表
    """
    logger.info(
        f"[POST /review/paragraphs] user_id={current_user.id}, "
        f"text_length={len(request.text)}"
    )

    # 导入服务
    from app.services.review.paragraph_review_service import ParagraphReviewService

    try:
        # 调用服务
        # ✅ 2025-12-02: 传递db和user_id以启用成本追踪
        service = ParagraphReviewService(db=db, user_id=str(current_user.id))
        result = await service.review_paragraph(
            text=request.text,
            context=request.context
        )

        # 转换为响应格式
        from app.schemas.review import ParagraphDimensionScores

        response = ParagraphReviewResponse(
            overall_score=result.get("overall_score", 0),
            dimension_scores=ParagraphDimensionScores(**result.get("dimension_scores", {})),
            quick_feedback=result.get("quick_feedback", ""),
            suggestions=result.get("suggestions", [])
        )

        logger.info(f"[POST /review/paragraphs] 评审完成, 总分={response.overall_score}")
        return response

    except Exception as e:
        logger.error(f"[POST /review/paragraphs] 错误: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"评审失败: {str(e)}"
        )


# ==================== 作品级评审接口 ====================

@router.post(
    "/books",
    response_model=BookReviewResponse,
    summary="作品级评审",
    description="对完整作品进行深度分析 (情节/人物/世界观/文风)"
)
async def review_book(
    request: BookReviewRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    作品级评审

    **使用场景**:
    - 完成了多个章节,想要整体评估
    - 分析整体情节脉络、人物关系
    - 检查世界观一致性
    - 了解文风特色

    **分析维度** (4个):
    1. **情节分析** - 结构、节奏、伏笔、高潮设计
    2. **人物分析** - 主要角色、关系网络、性格一致性
    3. **世界观分析** - 设定完整性、规则一致性、独特性
    4. **文风分析** - 语言风格、描写手法、对话质量

    **要求**:
    - 至少3个章节
    - 每章不少于500字
    - 建议10章以内 (使用quick_mode可分析前10章)

    **参数**:
    - **novel_id**: 小说ID
    - **book_title**: 书名
    - **chapters**: 章节列表 [{title, content, order}, ...]
    - **author_notes**: 作者备注 (可选)
    - **quick_mode**: 快速模式 (仅分析前10章)

    **返回**:
    - overall_score: 综合评分 (0-100)
    - plot_analysis: 情节分析详情
    - character_analysis: 人物分析详情
    - worldview_analysis: 世界观分析详情
    - writing_style: 文风分析详情
    - recommendations: 综合修改建议
    """
    logger.info(
        f"[POST /review/books] user_id={current_user.id}, "
        f"novel_id={request.novel_id}, chapters={len(request.chapters)}, "
        f"quick_mode={request.quick_mode}"
    )

    # 参数验证
    if len(request.chapters) < 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="至少需要3个章节才能进行作品级评审"
        )

    # 导入服务
    from app.services.review.book_review_service import BookReviewService

    try:
        # 转换章节格式
        chapters_data = [
            {
                "title": ch.title,
                "content": ch.content,
                "order": ch.order
            }
            for ch in request.chapters
        ]

        # 调用服务
        # ✅ 2025-12-02: 传递db和user_id以启用成本追踪
        service = BookReviewService(db=db, user_id=str(current_user.id))

        if request.quick_mode:
            result = await service.quick_review_book(
                novel_id=request.novel_id,
                book_title=request.book_title,
                chapters=chapters_data
            )
        else:
            result = await service.review_book(
                novel_id=request.novel_id,
                book_title=request.book_title,
                chapters=chapters_data,
                author_notes=request.author_notes
            )

        # 转换为响应格式
        from app.schemas.review import (
            PlotAnalysis,
            CharacterAnalysis,
            WorldviewAnalysis,
            WritingStyleAnalysis,
            Recommendations
        )

        response = BookReviewResponse(
            book_title=result["book_title"],
            novel_id=result["novel_id"],
            total_chapters=result["total_chapters"],
            analysis_date=result["analysis_date"],
            overall_score=result["overall_score"],
            plot_analysis=PlotAnalysis(**result["plot_analysis"]),
            character_analysis=CharacterAnalysis(**result["character_analysis"]),
            worldview_analysis=WorldviewAnalysis(**result["worldview_analysis"]),
            writing_style=WritingStyleAnalysis(**result["writing_style"]),
            recommendations=Recommendations(**result["recommendations"]),
            is_quick_review=result.get("is_quick_review", False),
            sampled_chapters=result.get("sampled_chapters")
        )

        logger.info(
            f"[POST /review/books] 评审完成, "
            f"novel_id={request.novel_id}, overall_score={response.overall_score}"
        )

        return response

    except ValueError as e:
        logger.error(f"[POST /review/books] 参数错误: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"[POST /review/books] 错误: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"评审失败: {str(e)}"
        )

