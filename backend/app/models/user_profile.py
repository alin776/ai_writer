from sqlalchemy import Column, String, DateTime, Boolean, Float, Integer, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.core.database import Base


class UserProfile(Base):
    """用户画像模型 - 用于去痕迹功能的个性化控制"""

    __tablename__ = "user_profiles"

    # 主键
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # 关联用户 (一对一)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)

    # ========== 使用统计 ==========
    total_uses = Column(Integer, nullable=False, server_default="0")  # 总使用次数
    avg_text_length = Column(Integer, nullable=True)  # 平均文本长度
    most_used_function = Column(String(50), nullable=True)  # 最常用功能

    # ========== 偏好设置 (自动学习) ==========
    preferred_intensity = Column(String(20), nullable=True)  # 偏好强度: light/medium/strong (自动检测)
    preferred_speed_over_quality = Column(Boolean, nullable=False, server_default="false")  # 偏好速度还是质量

    # 用户类型标签 (自动检测)
    is_novel_writer = Column(Boolean, nullable=False, server_default="false")  # 是否小说作者

    # ========== 反馈统计 ==========
    total_accepted = Column(Integer, nullable=False, server_default="0")  # 接受次数
    total_rejected = Column(Integer, nullable=False, server_default="0")  # 拒绝次数
    accept_rate = Column(Float, nullable=False, server_default="0.0")  # 接受率 (0.0-1.0)

    # ========== 开关控制 ==========
    humanize_enabled_global = Column(Boolean, nullable=False, server_default="true")  # 全局开关

    # 分功能开关 (JSON字段)
    humanize_enabled_by_function = Column(
        JSONB,
        nullable=False,
        server_default=text("'{\"complete\": true, \"polish\": true, \"expand\": true, \"translate\": false, \"summarize\": false, \"rewrite\": true}'::jsonb"),
        comment="分功能开关配置"
    )

    # ========== 智能显示策略 ==========
    # 根据 total_uses 和 accept_rate 自动判断:
    # - 前5次: 显示详细对比
    # - 6-20次: 显示简化对比
    # - 21次+且接受率>80%: 静默模式

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # 关联关系
    user = relationship("User", backref="profile", uselist=False)

    def __repr__(self):
        return f"<UserProfile user_id={self.user_id} uses={self.total_uses} accept_rate={self.accept_rate:.2%}>"

    @property
    def display_mode(self) -> str:
        """根据使用次数和接受率判断显示模式"""
        if self.total_uses <= 5:
            return "detailed"  # 详细对比
        elif self.total_uses <= 20:
            return "simplified"  # 简化对比
        elif self.accept_rate >= 0.8:
            return "silent"  # 静默模式
        else:
            return "simplified"

    def should_enable_humanize(self, function_name: str) -> bool:
        """判断指定功能是否启用去痕迹"""
        if not self.humanize_enabled_global:
            return False

        function_settings = self.humanize_enabled_by_function or {}
        return function_settings.get(function_name, True)
