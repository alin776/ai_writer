"""
关系管理API
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from typing import List
from uuid import UUID
import logging
import json

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.relationship import EntityRelationship
from app.models.work import Work
from app.schemas.relationship import (
    RelationshipCreate,
    RelationshipUpdate,
    RelationshipResponse,
    RelationshipListResponse,
    AIGenerateRelationshipRequest,
    AIGenerateRelationshipResponse
)

router = APIRouter()
logger = logging.getLogger(__name__)

# AI 生成关系的 Prompt 模板
RELATIONSHIP_GENERATION_PROMPT = """你是一个小说世界观设计助手。

## 任务
为小说世界观中的两个实体生成关系标签和描述。

## 输入信息
- 源节点：{source_name}（类型：{source_type_cn}）
  描述：{source_description}

- 目标节点：{target_name}（类型：{target_type_cn}）
  描述：{target_description}

- 关系类型：{relationship_type}
- 关系方向：{direction_cn}

## 用户想法
{user_input}

## 输出要求
请返回JSON格式：
{{
  "label": "简短标签（2-6个字，概括关系本质）",
  "description": "详细描述（50-200字，说明关系的具体内容、背景、影响）"
}}

## 注意事项
1. 标签要简洁有力，能一眼看出关系本质
2. 描述要结合用户想法，丰富关系细节
3. 保持与小说世界观风格一致
4. 如果用户想法不清晰，基于节点信息合理推断
5. 只返回JSON，不要有其他内容
"""


def _get_type_cn(entity_type: str) -> str:
    """获取实体类型的中文名"""
    type_map = {"character": "角色", "location": "地点", "setting": "设定"}
    return type_map.get(entity_type, entity_type)


async def verify_work_owner(work_id: UUID, user_id: UUID, db: AsyncSession):
    """验证作品所有权"""
    result = await db.execute(
        select(Work).where(and_(Work.id == work_id, Work.author_id == user_id))
    )
    work = result.scalar_one_or_none()
    if not work:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Work not found or you don't have permission"
        )
    return work


# ==================== AI 生成关系（必须在动态路由之前） ====================

@router.post("/ai-generate", response_model=AIGenerateRelationshipResponse)
async def ai_generate_relationship(
    request: AIGenerateRelationshipRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """AI 生成关系标签和描述"""
    from app.services.ai.langchain_ai_service import LangChainAIService

    logger.info(
        f"[AI生成关系] 用户: {current_user.username}, "
        f"源: {request.source.name}, 目标: {request.target.name}, "
        f"类型: {request.relationship_type}"
    )

    # 验证作品所有权
    await verify_work_owner(request.work_id, current_user.id, db)

    # 构建 Prompt
    prompt = RELATIONSHIP_GENERATION_PROMPT.format(
        source_name=request.source.name,
        source_type_cn=_get_type_cn(request.source.type),
        source_description=request.source.description or "暂无描述",
        target_name=request.target.name,
        target_type_cn=_get_type_cn(request.target.type),
        target_description=request.target.description or "暂无描述",
        relationship_type=request.relationship_type,
        direction_cn="双向" if request.direction == "two-way" else "单向",
        user_input=request.user_input
    )

    result_text = ""
    try:
        # 调用 AI 服务
        ai_service = LangChainAIService(db=db, user_id=str(current_user.id))

        # 收集流式响应
        async for chunk, usage in ai_service.stream_complete(
            context=prompt,
            prompt="请生成关系标签和描述",
            max_tokens=500
        ):
            if chunk:
                result_text += chunk

        await ai_service.close()

        # 解析 JSON 响应
        result_text = result_text.strip()
        # 处理可能的 markdown 代码块
        if result_text.startswith("```"):
            result_text = result_text.split("```")[1]
            if result_text.startswith("json"):
                result_text = result_text[4:]
            result_text = result_text.strip()

        # 尝试解析 JSON
        try:
            result = json.loads(result_text)
            label = result.get("label", request.relationship_type)[:20]
            description = result.get("description", "")
        except json.JSONDecodeError:
            # AI 可能直接返回了文本而非 JSON
            if len(result_text) > 10 and not result_text.startswith("{"):
                logger.info(f"[AI生成关系] AI返回纯文本，直接使用")
                label = request.relationship_type
                description = result_text
            else:
                raise

        logger.info(f"[AI生成关系] 成功: label={label}")

        return AIGenerateRelationshipResponse(
            label=label,
            description=description
        )

    except json.JSONDecodeError as e:
        logger.error(f"[AI生成关系] JSON解析失败: {e}, 原文: {result_text[:200] if result_text else 'empty'}")
        # 降级：如果有返回文本，用作描述
        if result_text and len(result_text) > 10:
            return AIGenerateRelationshipResponse(
                label=request.relationship_type,
                description=result_text
            )
        return AIGenerateRelationshipResponse(
            label=request.relationship_type,
            description=f"基于用户想法：{request.user_input}"
        )
    except Exception as e:
        logger.error(f"[AI生成关系] 失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI生成失败: {str(e)}"
        )


# ==================== CRUD 路由 ====================

@router.post("/", response_model=RelationshipResponse, status_code=status.HTTP_201_CREATED)
async def create_relationship(
    relationship: RelationshipCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """创建关系"""
    import logging
    logger = logging.getLogger(__name__)

    try:
        logger.info(f"Creating relationship: {relationship.dict()}")

        # 验证作品所有权
        await verify_work_owner(relationship.work_id, current_user.id, db)

        # 创建关系
        relationship_data = relationship.dict()
        logger.info(f"Relationship data for DB: {relationship_data}")

        db_relationship = EntityRelationship(**relationship_data)
        db.add(db_relationship)
        await db.commit()
        await db.refresh(db_relationship)

        logger.info(f"Relationship created successfully: {db_relationship.id}")
        return db_relationship
    except Exception as e:
        logger.error(f"Error creating relationship: {type(e).__name__}: {str(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise


@router.get("/{relationship_id}", response_model=RelationshipResponse)
async def get_relationship(
    relationship_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取单个关系详情"""
    result = await db.execute(
        select(EntityRelationship).where(EntityRelationship.id == relationship_id)
    )
    relationship = result.scalar_one_or_none()
    
    if not relationship:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relationship not found"
        )
    
    # 验证作品所有权
    await verify_work_owner(relationship.work_id, current_user.id, db)
    
    return relationship


@router.get("/work/{work_id}", response_model=RelationshipListResponse)
async def get_work_relationships(
    work_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取作品的所有关系"""
    # 验证作品所有权
    await verify_work_owner(work_id, current_user.id, db)
    
    # 查询关系
    result = await db.execute(
        select(EntityRelationship)
        .where(EntityRelationship.work_id == work_id)
        .order_by(EntityRelationship.created_at.desc())
    )
    relationships = result.scalars().all()
    
    return {
        "items": relationships,
        "total": len(relationships)
    }


@router.put("/{relationship_id}", response_model=RelationshipResponse)
async def update_relationship(
    relationship_id: UUID,
    relationship_update: RelationshipUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """更新关系"""
    # 查询关系
    result = await db.execute(
        select(EntityRelationship).where(EntityRelationship.id == relationship_id)
    )
    db_relationship = result.scalar_one_or_none()
    
    if not db_relationship:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relationship not found"
        )
    
    # 验证作品所有权
    await verify_work_owner(db_relationship.work_id, current_user.id, db)
    
    # 更新字段
    update_data = relationship_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_relationship, field, value)
    
    await db.commit()
    await db.refresh(db_relationship)
    
    return db_relationship


@router.delete("/{relationship_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_relationship(
    relationship_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """删除关系"""
    # 查询关系
    result = await db.execute(
        select(EntityRelationship).where(EntityRelationship.id == relationship_id)
    )
    db_relationship = result.scalar_one_or_none()
    
    if not db_relationship:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relationship not found"
        )
    
    # 验证作品所有权
    await verify_work_owner(db_relationship.work_id, current_user.id, db)
    
    # 删除关系
    await db.delete(db_relationship)
    await db.commit()

    return None
