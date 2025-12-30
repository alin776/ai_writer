from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID


# ========== 基础Schema ==========

class AIGuidelinesBase(BaseModel):
    """AI创作规范基础Schema"""
    
    # 第一部分：创作规范
    # 一、战略定位
    business_goal: Optional[str] = None
    target_audience: Optional[str] = None
    commercial_benchmark: Optional[str] = None
    high_concept: Optional[str] = None
    
    # 二、IP架构
    core_paradox: Optional[str] = None
    dominant_emotion: Optional[str] = None
    core_ip_symbols: Optional[str] = None
    
    # 三、叙事引擎
    protagonist_arc: Optional[str] = None
    core_conflict: Optional[str] = None
    narrative_rhythm: Optional[str] = None
    
    # 四、文字质感
    writing_style: Optional[str] = None
    style_notes: Optional[str] = None
    
    # 五、技术规范
    chapter_length: Optional[str] = None
    content_taboos: Optional[str] = None
    
    # 第二部分：核心设定
    # 一、小说类型与体裁
    primary_genre: Optional[str] = None
    secondary_tags: Optional[str] = None
    creative_tone: Optional[str] = None
    
    # 二、世界背景设定
    world_intro: Optional[str] = None
    main_locations: Optional[str] = None
    world_rules: Optional[str] = None
    
    # 三、力量体系
    power_system_name: Optional[str] = None
    power_levels: Optional[str] = None
    power_cost: Optional[str] = None
    
    # 四、主角核心设定
    protagonist_name: Optional[str] = None
    protagonist_identity: Optional[str] = None
    protagonist_traits: Optional[str] = None
    protagonist_goal: Optional[str] = None
    
    # 五、剧情构思
    conflict_design: Optional[str] = None
    act_one: Optional[str] = None
    act_two: Optional[str] = None
    act_three: Optional[str] = None
    
    is_active: bool = True


# ========== 创建Schema ==========

class AIGuidelinesCreate(AIGuidelinesBase):
    """创建AI创作规范"""
    work_id: UUID


# ========== 更新Schema ==========

class AIGuidelinesUpdate(AIGuidelinesBase):
    """更新AI创作规范"""
    pass


# ========== 响应Schema ==========

class AIGuidelinesResponse(AIGuidelinesBase):
    """AI创作规范响应"""
    id: UUID
    work_id: UUID
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True  # 允许使用字段名或别名填充
    )


# ========== 简化的输出Schema（用于AI prompt生成） ==========

class AIGuidelinesPrompt(BaseModel):
    """用于生成AI提示词的简化版"""
    
    # 核心规范
    writing_style: Optional[str] = None
    narrative_rhythm: Optional[str] = None
    dominant_emotion: Optional[str] = None
    
    # 世界设定
    world_intro: Optional[str] = None
    world_rules: Optional[str] = None
    
    # 主角设定
    protagonist_name: Optional[str] = None
    protagonist_traits: Optional[str] = None
    protagonist_goal: Optional[str] = None
    
    # 剧情框架
    conflict_design: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)


# ========== AI生成请求Schema ==========

class AIGuidelinesGenerateRequest(BaseModel):
    """AI生成内容的请求"""

    # 🆕 方案C：支持基于故事梗概快速生成
    story_concept: Optional[str] = None  # 故事梗概（一句话描述）

    # 原有的阶段一15个字段（兼容旧版本，可选）
    business_goal: Optional[str] = None
    target_audience: Optional[str] = None
    commercial_benchmark: Optional[str] = None
    high_concept: Optional[str] = None
    core_paradox: Optional[str] = None
    dominant_emotion: Optional[str] = None
    core_ip_symbols: Optional[str] = None
    protagonist_arc: Optional[str] = None
    core_conflict: Optional[str] = None
    narrative_rhythm: Optional[str] = None
    writing_style: Optional[str] = None
    style_notes: Optional[str] = None
    chapter_length: Optional[str] = None
    content_taboos: Optional[str] = None


class AIGuidelinesGenerateResponse(BaseModel):
    """AI生成内容的响应（完整31个字段）"""

    # 🆕 方案C：返回完整31个字段
    # 阶段一：创作规范（15个字段）
    business_goal: Optional[str] = None
    target_audience: Optional[str] = None
    commercial_benchmark: Optional[str] = None
    high_concept: Optional[str] = None
    core_paradox: Optional[str] = None
    dominant_emotion: Optional[str] = None
    core_ip_symbols: Optional[str] = None
    protagonist_arc: Optional[str] = None
    core_conflict: Optional[str] = None
    narrative_rhythm: Optional[str] = None
    writing_style: Optional[str] = None
    style_notes: Optional[str] = None
    chapter_length: Optional[str] = None
    content_taboos: Optional[str] = None

    # 阶段二：核心设定（17个字段）
    primary_genre: Optional[str] = None
    secondary_tags: Optional[str] = None
    creative_tone: Optional[str] = None
    world_intro: Optional[str] = None
    main_locations: Optional[str] = None
    world_rules: Optional[str] = None
    power_system_name: Optional[str] = None
    power_levels: Optional[str] = None
    power_cost: Optional[str] = None
    protagonist_name: Optional[str] = None
    protagonist_identity: Optional[str] = None
    protagonist_traits: Optional[str] = None
    protagonist_goal: Optional[str] = None
    conflict_design: Optional[str] = None
    act_one: Optional[str] = None
    act_two: Optional[str] = None
    act_three: Optional[str] = None
