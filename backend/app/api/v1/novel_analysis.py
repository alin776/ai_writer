"""
小说分析 API 路由
提供小说分析任务的创建、状态查询、结果获取等接口
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from uuid import UUID
import logging
import asyncio

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.novel_analysis import AnalysisStatus
from app.schemas.novel_analysis import (
    NovelAnalysisCreate,
    NovelAnalysisResponse,
    NovelAnalysisSimple,
    AnalysisProgress
)
from app.services.novel_analysis_service import NovelAnalysisService
from app.services.work_service import WorkService
from app.services.ai.novel_analysis_orchestrator import NovelAnalysisOrchestrator
from app.services.worldview_extraction_service import WorldviewExtractionService

router = APIRouter()
logger = logging.getLogger(__name__)


# ==================== 辅助函数 ====================

async def _run_analysis_in_background_async(work_id: str):
    """
    在后台运行分析任务（异步版本）
    
    Args:
        work_id: 作品ID
    
    注意：必须在主事件循环中调用，因为需要使用主引擎的数据库连接
    """
    from app.core.database import create_db_session
    
    # 短暂延迟，确保主记录的commit完成
    # 避免后台任务在主记录commit前就开始执行
    await asyncio.sleep(0.1)
    
    async with create_db_session() as db:
        try:
            logger.info(f"后台任务开始：分析作品 {work_id}")
            
            # 验证主记录是否可见
            analysis_service = NovelAnalysisService(db)
            analysis = await analysis_service.get_analysis_by_work(work_id)
            
            if not analysis:
                logger.error(f"后台任务失败：找不到分析记录 work_id={work_id}")
                return
            
            logger.info(f"后台任务已找到分析记录 analysis_id={analysis.id}")
            
            orchestrator = NovelAnalysisOrchestrator(db)
            success = await orchestrator.run_full_analysis(work_id)

            if success:
                logger.info(f"后台任务完成：作品 {work_id} 分析成功")
            else:
                logger.error(f"后台任务失败：作品 {work_id} 分析失败")

        except Exception as e:
            logger.error(f"后台任务异常：{e}", exc_info=True)


async def _verify_work_ownership(
    work_id: str,
    current_user: User,
    db: AsyncSession
) -> None:
    """
    验证作品归属于当前用户

    Args:
        work_id: 作品ID
        current_user: 当前用户
        db: 数据库会话

    Raises:
        HTTPException: 如果作品不存在或不属于当前用户
    """
    work_service = WorkService(db)
    work = await work_service.get_work_by_id(work_id)

    if not work:
        logger.warning(f"Work not found: {work_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Work with id {work_id} not found"
        )

    # 统一转换为字符串进行比较，并去除大括号和空格
    work_author_id = str(work.author_id).strip('{}').lower()
    current_user_id = str(current_user.id).strip('{}').lower()

    logger.debug(f"Verifying work ownership: work_id={work_id}, work_author_id={work_author_id}, current_user_id={current_user_id}")

    if work_author_id != current_user_id:
        logger.warning(f"Permission denied: user {current_user_id} tried to access work {work_id} owned by {work_author_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to analyze this work"
        )


# ==================== API 端点 ====================

@router.post(
    "/works/{work_id}/start",
    response_model=NovelAnalysisSimple,
    status_code=status.HTTP_201_CREATED,
    summary="触发小说分析",
    description="为指定作品创建并启动小说分析任务。如果已有进行中的任务，将返回现有任务。"
)
async def start_analysis(
    work_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> NovelAnalysisSimple:
    """
    触发小说分析
    
    - **work_id**: 作品UUID
    - 返回创建的分析任务（简化版）
    - 分析将在后台执行
    """
    try:
        # 1. 验证作品归属
        await _verify_work_ownership(work_id, current_user, db)
        
        # 2. 创建分析任务
        analysis_service = NovelAnalysisService(db)
        analysis = await analysis_service.create_analysis(work_id)
        
        # 3. 在主事件循环中创建后台任务
        # 使用 asyncio.create_task 而不是 BackgroundTasks，避免事件循环冲突
        asyncio.create_task(_run_analysis_in_background_async(work_id))
        
        logger.info(f"User {current_user.id} started analysis for work {work_id}, analysis_id: {analysis.id}")
        
        return NovelAnalysisSimple(
            id=analysis.id,
            work_id=analysis.work_id,
            status=analysis.status,
            current_stage=analysis.current_stage,
            progress_percentage=analysis.progress_percentage,
            error_message=analysis.error_message
        )
        
    except ValueError as e:
        logger.error(f"Failed to create analysis: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error creating analysis: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create analysis: {str(e)}"
        )


@router.get(
    "/works/{work_id}",
    response_model=AnalysisProgress,
    summary="查询分析状态（简化路径）",
    description="查询指定作品的分析任务状态和进度信息"
)
async def get_analysis(
    work_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> AnalysisProgress:
    """
    查询分析状态（简化路径）

    - **work_id**: 作品UUID
    - 返回分析进度信息
    """
    try:
        # 1. 验证作品归属
        await _verify_work_ownership(work_id, current_user, db)

        # 2. 获取分析任务
        analysis_service = NovelAnalysisService(db)
        analysis = await analysis_service.get_analysis_by_work(work_id)

        if not analysis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No analysis found for work {work_id}"
            )

        return AnalysisProgress(
            status=analysis.status,
            current_stage=analysis.current_stage,
            total_chapters=analysis.total_chapters,
            analyzed_chapters=analysis.analyzed_chapters,
            progress_percentage=analysis.progress_percentage,
            error_message=analysis.error_message
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting analysis status: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get analysis status: {str(e)}"
        )


@router.get(
    "/works/{work_id}/status",
    response_model=AnalysisProgress,
    summary="查询分析状态",
    description="查询指定作品的分析任务状态和进度信息"
)
async def get_analysis_status(
    work_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> AnalysisProgress:
    """
    查询分析状态

    - **work_id**: 作品UUID
    - 返回分析进度信息
    """
    # 直接调用上面的函数，避免重复代码
    return await get_analysis(work_id, current_user, db)


@router.get(
    "/works/{work_id}/result",
    response_model=NovelAnalysisResponse,
    summary="获取分析结果",
    description="获取指定作品的完整分析结果（包含微观和宏观分析）"
)
async def get_analysis_result(
    work_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> NovelAnalysisResponse:
    """
    获取分析结果
    
    - **work_id**: 作品UUID
    - 返回完整的分析结果
    - 如果分析未完成，仍会返回当前进度
    """
    try:
        # 1. 验证作品归属
        await _verify_work_ownership(work_id, current_user, db)
        
        # 2. 获取分析结果
        analysis_service = NovelAnalysisService(db)
        analysis = await analysis_service.get_analysis_result(work_id)
        
        if not analysis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No analysis found for work {work_id}"
            )
        
        return NovelAnalysisResponse(
            id=analysis.id,
            work_id=analysis.work_id,
            status=analysis.status,
            current_stage=analysis.current_stage,
            total_chapters=analysis.total_chapters,
            analyzed_chapters=analysis.analyzed_chapters,
            progress_percentage=analysis.progress_percentage,
            micro_results=analysis.micro_results,
            macro_results=analysis.macro_results,
            error_message=analysis.error_message,
            started_at=analysis.started_at,
            completed_at=analysis.completed_at,
            created_at=analysis.created_at,
            updated_at=analysis.updated_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting analysis result: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get analysis result: {str(e)}"
        )


@router.delete(
    "/works/{work_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="删除分析任务",
    description="删除指定作品的分析任务及其所有结果"
)
async def delete_analysis(
    work_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> None:
    """
    删除分析任务
    
    - **work_id**: 作品UUID
    - 删除成功返回204
    """
    try:
        # 1. 验证作品归属
        await _verify_work_ownership(work_id, current_user, db)
        
        # 2. 删除分析任务
        analysis_service = NovelAnalysisService(db)
        success = await analysis_service.delete_analysis(work_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No analysis found for work {work_id}"
            )
        
        logger.info(f"User {current_user.id} deleted analysis for work {work_id}")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting analysis: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete analysis: {str(e)}"
        )


@router.post(
    "/works/{work_id}/extract-worldview",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="从分析结果提取世界观数据",
    description="从小说分析结果中自动提取并创建/更新角色、地点和设定信息"
)
async def extract_worldview_from_analysis(
    work_id: str,
    extract_characters: bool = True,
    extract_locations: bool = True,
    extract_settings: bool = True,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> dict:
    """
    从小说分析结果提取世界观数据
    
    - **work_id**: 作品UUID
    - **extract_characters**: 是否提取角色（默认True）
    - **extract_locations**: 是否提取地点（默认True）
    - **extract_settings**: 是否提取设定（默认True）
    
    返回提取结果统计：
    ```json
    {
        "characters": {"created": 5, "updated": 2},
        "locations": {"created": 3, "updated": 1},
        "settings": {"created": 4, "updated": 0}
    }
    ```
    """
    try:
        # 1. 验证作品归属
        await _verify_work_ownership(work_id, current_user, db)
        
        # 2. 获取分析结果
        analysis_service = NovelAnalysisService(db)
        analysis = await analysis_service.get_analysis_by_work(work_id)
        
        if not analysis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No analysis found for work {work_id}. Please run analysis first."
            )
        
        if analysis.status != AnalysisStatus.COMPLETED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Analysis is not completed yet. Current status: {analysis.status.value}"
            )
        
        # 3. 执行世界观提取
        extraction_service = WorldviewExtractionService(db)
        
        options = {
            "characters": extract_characters,
            "locations": extract_locations,
            "settings": extract_settings
        }
        
        logger.info(f"User {current_user.id} started worldview extraction for work {work_id}, options: {options}")
        
        result = await extraction_service.extract_from_analysis(
            work_id=work_id,
            analysis=analysis,
            options=options
        )
        
        logger.info(f"Worldview extraction completed for work {work_id}: {result}")
        
        return result
        
    except HTTPException:
        raise
    except ValueError as e:
        logger.warning(f"Invalid request for worldview extraction: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error extracting worldview: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to extract worldview: {str(e)}"
        )
