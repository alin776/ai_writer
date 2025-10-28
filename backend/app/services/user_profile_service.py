"""
UserProfileService - 用户画像服务

管理用户的去痕迹偏好设置和使用统计
"""

from typing import Optional, Literal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from uuid import UUID
import logging

from app.models.user_profile import UserProfile
from app.schemas.humanize import UserProfileResponse, UserProfileUpdateRequest

logger = logging.getLogger(__name__)


class UserProfileService:
    """用户画像服务"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_or_create_profile(self, user_id: UUID) -> UserProfile:
        """
        获取或创建用户画像

        Args:
            user_id: 用户ID

        Returns:
            UserProfile: 用户画像对象
        """
        # 尝试获取现有画像
        result = await self.db.execute(
            select(UserProfile).where(UserProfile.user_id == user_id)
        )
        profile = result.scalar_one_or_none()

        if profile:
            logger.debug(f"获取到现有用户画像: user_id={user_id}")
            return profile

        # 创建新画像
        profile = UserProfile(user_id=user_id)
        self.db.add(profile)
        await self.db.commit()
        await self.db.refresh(profile)

        logger.info(f"创建新用户画像: user_id={user_id}")
        return profile

    async def update_profile_settings(
        self,
        user_id: UUID,
        settings: UserProfileUpdateRequest
    ) -> UserProfile:
        """
        更新用户画像设置

        Args:
            user_id: 用户ID
            settings: 更新的设置

        Returns:
            UserProfile: 更新后的用户画像
        """
        profile = await self.get_or_create_profile(user_id)

        # 更新设置
        profile.humanize_enabled_global = settings.humanize_enabled_global
        profile.humanize_enabled_by_function = settings.humanize_enabled_by_function

        if settings.preferred_intensity:
            profile.preferred_intensity = settings.preferred_intensity

        await self.db.commit()
        await self.db.refresh(profile)

        logger.info(f"更新用户画像设置: user_id={user_id}")
        return profile

    async def update_profile_after_use(
        self,
        user_id: UUID,
        ai_function: str,
        text_length: int,
        user_accepted: Optional[bool] = None
    ) -> UserProfile:
        """
        使用后更新用户画像统计

        Args:
            user_id: 用户ID
            ai_function: 使用的AI功能
            text_length: 文本长度
            user_accepted: 用户是否接受结果

        Returns:
            UserProfile: 更新后的用户画像
        """
        profile = await self.get_or_create_profile(user_id)

        # 更新使用统计
        profile.total_uses += 1

        # 更新平均文本长度
        if profile.avg_text_length is None:
            profile.avg_text_length = text_length
        else:
            # 滑动平均
            profile.avg_text_length = int(
                (profile.avg_text_length * (profile.total_uses - 1) + text_length) / profile.total_uses
            )

        # 更新最常用功能
        profile.most_used_function = ai_function  # 简化实现,直接记录最新的

        # 更新反馈统计
        if user_accepted is True:
            profile.total_accepted += 1
        elif user_accepted is False:
            profile.total_rejected += 1

        # 重新计算接受率
        total_feedback = profile.total_accepted + profile.total_rejected
        if total_feedback > 0:
            profile.accept_rate = profile.total_accepted / total_feedback

        # 自动检测用户类型
        self._auto_detect_user_type(profile)

        await self.db.commit()
        await self.db.refresh(profile)

        logger.info(
            f"更新用户画像统计: user_id={user_id}, "
            f"total_uses={profile.total_uses}, accept_rate={profile.accept_rate:.2%}"
        )
        return profile

    def _auto_detect_user_type(self, profile: UserProfile):
        """
        自动检测用户类型

        Args:
            profile: 用户画像对象
        """
        # 检测是否为小说作者 (使用次数 > 50 且平均长度 > 500)
        if profile.total_uses > 50 and (profile.avg_text_length or 0) > 500:
            profile.is_novel_writer = True
            logger.debug(f"检测到小说作者: user_id={profile.user_id}")

        # 根据接受率推荐强度
        if profile.total_uses >= 10:
            if profile.accept_rate >= 0.8:
                # 高接受率,可能喜欢当前强度
                pass  # 保持现有偏好
            elif profile.accept_rate < 0.5:
                # 低接受率,可能需要调整强度
                if profile.preferred_intensity == "strong":
                    profile.preferred_intensity = "medium"
                elif profile.preferred_intensity == "light":
                    profile.preferred_intensity = "medium"

    def get_recommended_intensity(
        self,
        profile: UserProfile
    ) -> Literal["light", "medium", "strong"]:
        """
        根据用户画像推荐去痕迹强度

        Args:
            profile: 用户画像对象

        Returns:
            推荐的强度
        """
        # 如果用户已设置偏好,优先使用
        if profile.preferred_intensity:
            return profile.preferred_intensity

        # 根据用户类型推荐
        if profile.is_novel_writer:
            return "light"  # 小说作者通常需要保留更多个人风格

        # 默认中度
        return "medium"

    def should_enable_humanize(
        self,
        profile: UserProfile,
        function_name: str
    ) -> bool:
        """
        判断指定功能是否启用去痕迹

        Args:
            profile: 用户画像对象
            function_name: 功能名称

        Returns:
            是否启用去痕迹
        """
        return profile.should_enable_humanize(function_name)

    def get_display_mode(
        self,
        profile: UserProfile
    ) -> Literal["detailed", "simplified", "silent"]:
        """
        获取显示模式

        Args:
            profile: 用户画像对象

        Returns:
            显示模式
        """
        return profile.display_mode

    async def record_feedback(
        self,
        user_id: UUID,
        accepted: bool
    ) -> UserProfile:
        """
        记录用户反馈

        Args:
            user_id: 用户ID
            accepted: 是否接受结果

        Returns:
            UserProfile: 更新后的用户画像
        """
        profile = await self.get_or_create_profile(user_id)

        if accepted:
            profile.total_accepted += 1
        else:
            profile.total_rejected += 1

        # 重新计算接受率
        total_feedback = profile.total_accepted + profile.total_rejected
        if total_feedback > 0:
            profile.accept_rate = profile.total_accepted / total_feedback

        await self.db.commit()
        await self.db.refresh(profile)

        logger.info(
            f"记录用户反馈: user_id={user_id}, accepted={accepted}, "
            f"accept_rate={profile.accept_rate:.2%}"
        )
        return profile

    async def record_humanize_use(
        self,
        user_id: UUID,
        text_length: int,
        ai_function: str,
        intensity: str,
        improvement: float
    ) -> UserProfile:
        """
        记录去痕迹使用情况

        Args:
            user_id: 用户ID
            text_length: 文本长度
            ai_function: AI功能类型
            intensity: 使用的强度
            improvement: 改进幅度

        Returns:
            UserProfile: 更新后的用户画像
        """
        profile = await self.get_or_create_profile(user_id)

        # 更新使用统计
        profile.total_uses += 1

        # 更新平均文本长度
        if profile.avg_text_length is None:
            profile.avg_text_length = text_length
        else:
            # 滑动平均
            profile.avg_text_length = int(
                (profile.avg_text_length * (profile.total_uses - 1) + text_length) / profile.total_uses
            )

        # 更新最常用功能
        profile.most_used_function = ai_function

        # 更新偏好强度（如果用户多次使用某个强度，记录为偏好）
        if profile.total_uses >= 3:
            profile.preferred_intensity = intensity

        # 自动检测用户类型
        self._auto_detect_user_type(profile)

        await self.db.commit()
        await self.db.refresh(profile)

        logger.info(
            f"记录去痕迹使用: user_id={user_id}, "
            f"total_uses={profile.total_uses}, intensity={intensity}, "
            f"improvement={improvement:.1f}"
        )
        return profile
