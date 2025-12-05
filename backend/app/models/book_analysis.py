"""
图书分析任务模型

记录图书分析任务的状态和进度
"""

import enum
from datetime import datetime
from sqlalchemy import Column, String, Integer, Text, DateTime, Enum as SQLEnum, Float, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid

from app.core.database import Base


class JobStatus(str, enum.Enum):
    """任务状态"""
    PENDING = "pending"  # 待处理
    PARSING = "parsing"  # 解析中
    ANALYZING = "analyzing"  # 分析中
    COMPLETED = "completed"  # 已完成
    FAILED = "failed"  # 失败
    CANCELLED = "cancelled"  # 已取消


class BookAnalysisJob(Base):
    """图书分析任务表"""
    __tablename__ = "book_analysis_jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)

    # 图书信息
    book_title = Column(String(500), nullable=False)
    original_filename = Column(String(500), nullable=False)
    file_format = Column(String(10), nullable=False)  # 'txt', 'epub', 'pdf'
    file_size_bytes = Column(Integer, nullable=False)
    file_hash = Column(String(64), unique=True, index=True)  # SHA256哈希,去重
    file_path = Column(String(500))  # 服务器上的文件路径

    # 分析配置
    strategy_id = Column(String(50), default="web_novel_11d")  # 分析策略ID

    # 任务状态
    status = Column(SQLEnum(JobStatus), default=JobStatus.PENDING, nullable=False, index=True)
    progress = Column(Integer, default=0)  # 0-100
    current_step = Column(String(200))  # 当前步骤描述

    # 分析结果统计
    total_chapters = Column(Integer)  # 总章节数
    analyzed_chapters = Column(Integer, default=0)  # 已分析章节数
    extracted_items_count = Column(Integer, default=0)  # 提取的知识条目数
    suggestions_count = Column(Integer, default=0)  # 生成的智能建议数

    # 错误处理
    error_message = Column(Text)
    retry_count = Column(Integer, default=0)

    # 元数据
    extra_data = Column(JSONB, default={})  # 灵活扩展

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<BookAnalysisJob(id={self.id}, title='{self.book_title}', status={self.status})>"
