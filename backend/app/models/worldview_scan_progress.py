"""
世界观扫描进度模型（导入解析专用）
"""
from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy import Column, String, Text, DateTime, Integer
from sqlalchemy.sql import func

from app.core.database import Base


class WorldviewScanProgress(Base):
    """世界观扫描进度记录"""
    __tablename__ = "worldview_scan_progress"

    id = Column(String, primary_key=True)  # 使用 work_id 作为主键
    work_id = Column(String, unique=True, nullable=False, index=True)

    # 进度状态
    status = Column(String, nullable=False, default="pending")  # pending, running, completed, failed
    scan_mode = Column(String, nullable=True, default="incremental")  # incremental/full

    # 进度统计
    chapters_total = Column(Integer, default=0)
    chapters_processed = Column(Integer, default=0)
    batches_total = Column(Integer, default=0)
    batches_completed = Column(Integer, default=0)

    # 结果统计
    characters_created = Column(Integer, default=0)
    characters_updated = Column(Integer, default=0)
    locations_created = Column(Integer, default=0)
    locations_updated = Column(Integer, default=0)
    settings_created = Column(Integer, default=0)
    settings_updated = Column(Integer, default=0)
    relationships_created = Column(Integer, default=0)

    # 错误信息
    last_error = Column(Text, nullable=True)

    # 时间戳
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # 元数据
    metadata_json = Column(Text, nullable=True)

    def to_dict(self) -> Dict[str, Any]:
        progress_percentage = 0.0
        if self.batches_total:
            progress_percentage = (self.batches_completed / self.batches_total) * 100
        elif self.chapters_total:
            progress_percentage = (self.chapters_processed / self.chapters_total) * 100

        return {
            "work_id": self.work_id,
            "status": self.status,
            "scan_mode": self.scan_mode,
            "chapters_total": self.chapters_total,
            "chapters_processed": self.chapters_processed,
            "batches_total": self.batches_total,
            "batches_completed": self.batches_completed,
            "progress_percentage": round(progress_percentage, 2),
            "results": {
                "characters_created": self.characters_created,
                "characters_updated": self.characters_updated,
                "locations_created": self.locations_created,
                "locations_updated": self.locations_updated,
                "settings_created": self.settings_created,
                "settings_updated": self.settings_updated,
                "relationships_created": self.relationships_created
            },
            "last_error": self.last_error,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "metadata_json": self.metadata_json
        }
