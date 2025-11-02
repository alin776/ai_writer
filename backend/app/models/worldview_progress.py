"""
世界观提取进度模型
用于持久化世界观提取的处理进度，支持中断恢复
"""
from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy import Column, String, Text, DateTime, Integer, Boolean
from sqlalchemy.sql import func

from app.core.database import Base


class WorldviewExtractionProgress(Base):
    """世界观提取进度记录"""
    __tablename__ = "worldview_extraction_progress"

    id = Column(String, primary_key=True)  # 使用 work_id 作为主键
    work_id = Column(String, unique=True, nullable=False, index=True)

    # 进度状态
    status = Column(String, nullable=False, default="pending")  # pending, running, completed, failed, paused
    current_phase = Column(String, nullable=False, default="characters")  # characters, locations, settings

    # 各阶段进度
    characters_total = Column(Integer, default=0)
    characters_processed = Column(Integer, default=0)
    characters_batches_completed = Column(Integer, default=0)
    characters_batches_total = Column(Integer, default=0)

    locations_total = Column(Integer, default=0)
    locations_processed = Column(Integer, default=0)
    locations_batches_completed = Column(Integer, default=0)
    locations_batches_total = Column(Integer, default=0)

    settings_total = Column(Integer, default=0)
    settings_processed = Column(Integer, default=0)
    settings_batches_completed = Column(Integer, default=0)
    settings_batches_total = Column(Integer, default=0)

    # 结果统计
    characters_created = Column(Integer, default=0)
    characters_updated = Column(Integer, default=0)
    locations_created = Column(Integer, default=0)
    locations_updated = Column(Integer, default=0)
    settings_created = Column(Integer, default=0)
    settings_updated = Column(Integer, default=0)

    # 错误信息
    last_error = Column(Text, nullable=True)
    failed_batches = Column(Text, nullable=True)  # JSON格式存储失败的批次信息

    # 时间戳
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # 元数据
    metadata_json = Column(Text, nullable=True)  # JSON格式存储额外的元数据

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "id": self.id,
            "work_id": self.work_id,
            "status": self.status,
            "current_phase": self.current_phase,
            "progress": {
                "characters": {
                    "total": self.characters_total,
                    "processed": self.characters_processed,
                    "batches_completed": self.characters_batches_completed,
                    "batches_total": self.characters_batches_total
                },
                "locations": {
                    "total": self.locations_total,
                    "processed": self.locations_processed,
                    "batches_completed": self.locations_batches_completed,
                    "batches_total": self.locations_batches_total
                },
                "settings": {
                    "total": self.settings_total,
                    "processed": self.settings_processed,
                    "batches_completed": self.settings_batches_completed,
                    "batches_total": self.settings_batches_total
                }
            },
            "results": {
                "characters": {"created": self.characters_created, "updated": self.characters_updated},
                "locations": {"created": self.locations_created, "updated": self.locations_updated},
                "settings": {"created": self.settings_created, "updated": self.settings_updated}
            },
            "errors": {
                "last_error": self.last_error,
                "failed_batches": self.failed_batches
            },
            "timestamps": {
                "started_at": self.started_at.isoformat() if self.started_at else None,
                "updated_at": self.updated_at.isoformat() if self.updated_at else None,
                "completed_at": self.completed_at.isoformat() if self.completed_at else None
            }
        }

    def get_overall_progress(self) -> float:
        """获取总体进度百分比"""
        total_items = (
            self.characters_total +
            self.locations_total +
            self.settings_total
        )
        if total_items == 0:
            return 0.0

        processed_items = (
            self.characters_processed +
            self.locations_processed +
            self.settings_processed
        )

        return (processed_items / total_items) * 100