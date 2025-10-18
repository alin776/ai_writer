from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.core.database import Base


class AIGuidelines(Base):
    """AI创作规范模型
    
    存储商业化小说创作的AI规范和核心设定
    基于《商业化小说创作规范与核心设定》框架
    """
    
    __tablename__ = "ai_guidelines"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    work_id = Column(UUID(as_uuid=True), ForeignKey("works.id"), nullable=False, unique=True, index=True)
    
    # ========== 第一部分：创作规范 ==========
    
    # 一、战略定位
    business_goal = Column(Text, nullable=True)  # 商业目标
    target_audience = Column(Text, nullable=True)  # 目标读者
    commercial_benchmark = Column(Text, nullable=True)  # 商业对标
    high_concept = Column(Text, nullable=True)  # 高概念卖点
    
    # 二、IP架构
    core_paradox = Column(Text, nullable=True)  # 核心悖论/设定
    dominant_emotion = Column(Text, nullable=True)  # 主导情感
    core_ip_symbols = Column(Text, nullable=True)  # 核心IP符号
    
    # 三、叙事引擎
    protagonist_arc = Column(Text, nullable=True)  # 主角弧光（缺陷/能力/转变）
    core_conflict = Column(Text, nullable=True)  # 核心关系冲突
    narrative_rhythm = Column(Text, nullable=True)  # 叙事节奏
    
    # 四、文字质感
    writing_style = Column(Text, nullable=True)  # 文笔风格
    style_notes = Column(Text, nullable=True)  # 文风注意事项
    
    # 五、技术规范
    chapter_length = Column(String(100), nullable=True)  # 章节长度
    content_taboos = Column(Text, nullable=True)  # 内容禁忌
    
    # ========== 第二部分：核心设定 ==========
    
    # 一、小说类型与体裁
    primary_genre = Column(String(100), nullable=True)  # 一级类型
    secondary_tags = Column(Text, nullable=True)  # 二级标签
    creative_tone = Column(Text, nullable=True)  # 创作基调
    
    # 二、世界背景设定
    world_intro = Column(Text, nullable=True)  # 核心世界观简介
    main_locations = Column(Text, nullable=True)  # 主要场景/地点
    world_rules = Column(Text, nullable=True)  # 世界规则
    
    # 三、力量体系/特殊设定
    power_system_name = Column(String(200), nullable=True)  # 体系名称与原理
    power_levels = Column(Text, nullable=True)  # 等级划分
    power_cost = Column(Text, nullable=True)  # 能力获取与代价
    
    # 四、主角核心设定
    protagonist_name = Column(String(200), nullable=True)  # 主角姓名/代号
    protagonist_identity = Column(Text, nullable=True)  # 核心身份
    protagonist_traits = Column(Text, nullable=True)  # 强化缺陷与能力
    protagonist_goal = Column(Text, nullable=True)  # 核心目标与动机
    
    # 五、剧情构思
    conflict_design = Column(Text, nullable=True)  # 冲突点设计
    act_one = Column(Text, nullable=True)  # 第一幕
    act_two = Column(Text, nullable=True)  # 第二幕
    act_three = Column(Text, nullable=True)  # 第三幕
    
    # 元数据
    is_active = Column(Boolean, default=True, nullable=False)  # 是否启用
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # 关联关系
    work = relationship("Work", back_populates="ai_guidelines")
    
    def __repr__(self):
        return f"<AIGuidelines work_id={self.work_id}>"
