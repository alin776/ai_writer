from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from app.models.ai_guidelines import AIGuidelines
from app.schemas.ai_guidelines import AIGuidelinesCreate, AIGuidelinesUpdate


class AIGuidelinesService:
    """AI创作规范服务"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_by_work_id(self, work_id: UUID) -> Optional[AIGuidelines]:
        """根据作品ID获取AI规范"""
        result = await self.db.execute(
            select(AIGuidelines).where(AIGuidelines.work_id == work_id)
        )
        return result.scalar_one_or_none()
    
    async def create(self, data: AIGuidelinesCreate) -> AIGuidelines:
        """创建AI规范"""
        guidelines = AIGuidelines(
            work_id=data.work_id,
            business_goal=data.business_goal,
            target_audience=data.target_audience,
            commercial_benchmark=data.commercial_benchmark,
            high_concept=data.high_concept,
            core_paradox=data.core_paradox,
            dominant_emotion=data.dominant_emotion,
            core_ip_symbols=data.core_ip_symbols,
            protagonist_arc=data.protagonist_arc,
            core_conflict=data.core_conflict,
            narrative_rhythm=data.narrative_rhythm,
            writing_style=data.writing_style,
            style_notes=data.style_notes,
            chapter_length=data.chapter_length,
            content_taboos=data.content_taboos,
            primary_genre=data.primary_genre,
            secondary_tags=data.secondary_tags,
            creative_tone=data.creative_tone,
            world_intro=data.world_intro,
            main_locations=data.main_locations,
            world_rules=data.world_rules,
            power_system_name=data.power_system_name,
            power_levels=data.power_levels,
            power_cost=data.power_cost,
            protagonist_name=data.protagonist_name,
            protagonist_identity=data.protagonist_identity,
            protagonist_traits=data.protagonist_traits,
            protagonist_goal=data.protagonist_goal,
            conflict_design=data.conflict_design,
            act_one=data.act_one,
            act_two=data.act_two,
            act_three=data.act_three,
            is_active=data.is_active,
        )
        
        self.db.add(guidelines)
        await self.db.commit()
        await self.db.refresh(guidelines)
        
        return guidelines
    
    async def update(self, work_id: UUID, data: AIGuidelinesUpdate) -> Optional[AIGuidelines]:
        """更新AI规范"""
        guidelines = await self.get_by_work_id(work_id)
        if not guidelines:
            return None
        
        # 更新字段
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(guidelines, field, value)
        
        await self.db.commit()
        await self.db.refresh(guidelines)
        
        return guidelines
    
    async def delete(self, work_id: UUID) -> bool:
        """删除AI规范"""
        guidelines = await self.get_by_work_id(work_id)
        if not guidelines:
            return False
        
        await self.db.delete(guidelines)
        await self.db.commit()
        
        return True
    
    def generate_ai_prompt(self, guidelines: AIGuidelines) -> str:
        """根据AI规范生成提示词
        
        用于AI创作时的系统提示
        """
        if not guidelines:
            return ""
        
        prompt_parts = []
        
        # 核心角色设定
        prompt_parts.append("你是一名资深商业IP总策划师和专业小说作家。")
        
        # 文字风格
        if guidelines.writing_style:
            prompt_parts.append(f"写作风格：{guidelines.writing_style}")
        
        # 叙事节奏
        if guidelines.narrative_rhythm:
            prompt_parts.append(f"叙事节奏：{guidelines.narrative_rhythm}")
        
        # 主导情感
        if guidelines.dominant_emotion:
            prompt_parts.append(f"主导情感：{guidelines.dominant_emotion}")
        
        # 世界观
        if guidelines.world_intro:
            prompt_parts.append(f"\n世界观：{guidelines.world_intro}")
        
        # 世界规则
        if guidelines.world_rules:
            prompt_parts.append(f"世界规则：{guidelines.world_rules}")
        
        # 主角设定
        if guidelines.protagonist_name or guidelines.protagonist_traits:
            prompt_parts.append("\n主角设定：")
            if guidelines.protagonist_name:
                prompt_parts.append(f"- 姓名：{guidelines.protagonist_name}")
            if guidelines.protagonist_traits:
                prompt_parts.append(f"- 特质：{guidelines.protagonist_traits}")
            if guidelines.protagonist_goal:
                prompt_parts.append(f"- 目标：{guidelines.protagonist_goal}")
        
        # 核心冲突
        if guidelines.conflict_design:
            prompt_parts.append(f"\n核心冲突：{guidelines.conflict_design}")
        
        # 文风注意事项
        if guidelines.style_notes:
            prompt_parts.append(f"\n注意事项：{guidelines.style_notes}")
        
        # 内容禁忌
        if guidelines.content_taboos:
            prompt_parts.append(f"\n内容禁忌：{guidelines.content_taboos}")
        
        prompt_parts.append("\n请严格遵循以上规范进行创作。")
        
        return "\n".join(prompt_parts)
