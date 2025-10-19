from sqlalchemy import Column, String, DateTime, Integer, Text, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
import enum

from app.core.database import Base


class AnalysisStatus(str, enum.Enum):
    """分析状态"""
    PENDING = "pending"  # 等待开始
    ANALYZING = "analyzing"  # 分析中
    COMPLETED = "completed"  # 已完成
    FAILED = "failed"  # 失败


class AnalysisStage(str, enum.Enum):
    """分析阶段"""
    MICRO_ANALYSIS = "micro_analysis"  # 微观分析阶段
    MACRO_ANALYSIS = "macro_analysis"  # 宏观分析阶段
    COMPLETED = "completed"  # 完成


class NovelAnalysis(Base):
    """小说分析模型
    
    存储小说的分层记忆与迭代分析结果
    包括微观分析（章节级别）和宏观分析（全局级别）
    """
    
    __tablename__ = "novel_analyses"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    work_id = Column(UUID(as_uuid=True), ForeignKey("works.id"), nullable=False, unique=True, index=True)
    
    # 状态信息
    status = Column(Enum(AnalysisStatus), nullable=False, default=AnalysisStatus.PENDING, index=True)
    current_stage = Column(Enum(AnalysisStage), nullable=False, default=AnalysisStage.MICRO_ANALYSIS)
    
    # 进度信息
    total_chapters = Column(Integer, default=0, nullable=False)  # 总章节数
    analyzed_chapters = Column(Integer, default=0, nullable=False)  # 已分析章节数
    
    # 分析结果
    micro_results = Column(JSONB, nullable=True)  # 微观分析JSON结果（所有章节）
    macro_results = Column(Text, nullable=True)  # 宏观分析报告（三大报告）
    
    # 错误信息
    error_message = Column(Text, nullable=True)  # 错误消息
    
    # 时间戳
    started_at = Column(DateTime(timezone=True), nullable=True)  # 开始时间
    completed_at = Column(DateTime(timezone=True), nullable=True)  # 完成时间
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # 关联关系
    work = relationship("Work", back_populates="novel_analysis")
    vectors = relationship("NovelAnalysisVector", back_populates="analysis", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<NovelAnalysis work_id={self.work_id} status={self.status.value}>"
    
    @property
    def progress_percentage(self) -> float:
        """计算分析进度百分比"""
        if self.total_chapters == 0:
            return 0.0
        return (self.analyzed_chapters / self.total_chapters) * 100
    
    @property
    def is_completed(self) -> bool:
        """是否已完成"""
        return self.status == AnalysisStatus.COMPLETED
    
    @property
    def is_analyzing(self) -> bool:
        """是否正在分析中"""
        return self.status == AnalysisStatus.ANALYZING
