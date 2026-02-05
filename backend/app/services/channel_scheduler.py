"""
频道系统定时任务调度器
负责管理频道相关的定时任务：
1. 检查作品频道活跃度并自动折叠
2. 发送预警提醒
3. 转正永久频道
"""

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timedelta
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from app.core.database import AsyncSessionLocal
from app.utils.datetime_utils import get_utc_now, make_aware
from app.models.channel import Channel, ChannelType, ChannelStatus
from app.models.channel_message import ChannelMessage
from app.models.notification import (
    Notification,
    NotificationCategory,
    NotificationType,
    NotificationPriority,
    NotificationStatus,
    TargetUserType,
    UserNotification,
)
import uuid

logger = logging.getLogger(__name__)

# 全局调度器实例
scheduler: AsyncIOScheduler = None


def init_scheduler():
    """初始化调度器"""
    global scheduler
    if scheduler is None:
        scheduler = AsyncIOScheduler()

        # 每天凌晨2点执行频道活跃度检查
        scheduler.add_job(
            check_work_channel_activity,
            CronTrigger(hour=2, minute=0),
            id='check_work_channel_activity',
            name='检查作品频道活跃度',
            replace_existing=True
        )

        logger.info("Channel scheduler initialized")

    return scheduler


def start_scheduler():
    """启动调度器"""
    global scheduler
    if scheduler and not scheduler.running:
        scheduler.start()
        logger.info("Channel scheduler started")


def shutdown_scheduler():
    """关闭调度器"""
    global scheduler
    if scheduler and scheduler.running:
        scheduler.shutdown()
        logger.info("Channel scheduler shutdown")


async def check_work_channel_activity():
    """
    检查作品频道活跃度

    规则：
    - 连续 7 天无人发言 -> 折叠频道
    - 第 5 天无人发言 -> 发送预警通知
    - 活跃满 30 天且数据增长 -> 转正为永久频道
    """
    logger.info("Starting work channel activity check...")

    async with AsyncSessionLocal() as session:
        try:
            # 查询所有活跃的作品频道
            result = await session.execute(
                select(Channel).where(
                    Channel.type == ChannelType.WORK,
                    Channel.status.in_([ChannelStatus.ACTIVE, ChannelStatus.WARNING])
                )
            )
            channels = result.scalars().all()

            now = get_utc_now()
            locked_count = 0
            warning_count = 0
            promoted_count = 0

            for channel in channels:
                # 获取频道最后一条消息的时间
                last_message_result = await session.execute(
                    select(ChannelMessage)
                    .where(ChannelMessage.channel_id == channel.id)
                    .order_by(ChannelMessage.created_at.desc())
                    .limit(1)
                )
                last_message = last_message_result.scalar_one_or_none()

                if last_message:
                    last_message_time = make_aware(last_message.created_at)
                    channel.last_message_at = last_message_time
                else:
                    # 如果没有消息，使用频道创建时间
                    last_message_time = make_aware(channel.created_at)
                    channel.last_message_at = last_message_time

                days_since_last_message = (now - last_message_time).days

                # 规则1: 7天无消息 -> 折叠
                if days_since_last_message >= 7 and channel.status != ChannelStatus.LOCKED:
                    channel.status = ChannelStatus.LOCKED
                    channel.locked_at = now
                    channel.warning_days = None
                    locked_count += 1
                    logger.info(f"Locked channel {channel.id} ({channel.name}) - {days_since_last_message} days inactive")

                    # 发送折叠通知给作者
                    if channel.creator_id:
                        notification = Notification(
                            id=uuid.uuid4(),
                            title="作品频道已折叠",
                            content=f"您的作品频道「{channel.name}」因连续7天无人发言已被自动折叠。在频道内发送消息可重新激活。",
                            category=NotificationCategory.SYSTEM,
                            type=NotificationType.INACTIVITY_ALERT,
                            priority=NotificationPriority.IMPORTANT,
                            target_users=TargetUserType.CUSTOM,
                            custom_user_ids=[channel.creator_id],
                            status=NotificationStatus.ACTIVE,
                            published_at=now,
                            display_type=["notification"],
                        )
                        session.add(notification)
                        session.add(UserNotification(
                            user_id=channel.creator_id,
                            notification_id=notification.id,
                            is_read=False,
                            is_dismissed=False,
                            clicked=False,
                        ))

                # 规则2: 第5天无消息 -> 预警
                elif days_since_last_message == 5 and channel.status == ChannelStatus.ACTIVE:
                    channel.status = ChannelStatus.WARNING
                    channel.warning_days = 2  # 还剩2天
                    warning_count += 1
                    logger.info(f"Warning channel {channel.id} ({channel.name}) - {days_since_last_message} days inactive")

                    # 发送预警通知给作者
                    if channel.creator_id:
                        notification = Notification(
                            id=uuid.uuid4(),
                            title="作品频道即将折叠",
                            content=f"您的作品频道「{channel.name}」已连续5天无人发言，还有2天将被自动折叠。快去发送消息唤醒频道吧！",
                            category=NotificationCategory.SYSTEM,
                            type=NotificationType.INACTIVITY_ALERT,
                            priority=NotificationPriority.IMPORTANT,
                            target_users=TargetUserType.CUSTOM,
                            custom_user_ids=[channel.creator_id],
                            status=NotificationStatus.ACTIVE,
                            published_at=now,
                            display_type=["notification"],
                        )
                        session.add(notification)
                        session.add(UserNotification(
                            user_id=channel.creator_id,
                            notification_id=notification.id,
                            is_read=False,
                            is_dismissed=False,
                            clicked=False,
                        ))

                # 规则3: 活跃满30天且成员增长 -> 转正永久
                elif not channel.is_permanent:
                    channel_age_days = (now - make_aware(channel.created_at)).days

                    if (channel_age_days >= 30 and
                        days_since_last_message < 7 and  # 仍然活跃
                        channel.member_count >= 10):  # 至少10个成员

                        channel.is_permanent = True
                        channel.status = ChannelStatus.ACTIVE
                        channel.warning_days = None
                        promoted_count += 1
                        logger.info(f"Promoted channel {channel.id} ({channel.name}) to permanent")

                        # 发送转正通知给作者
                        if channel.creator_id:
                            notification = Notification(
                                id=uuid.uuid4(),
                                title="作品频道已转正",
                                content=f"恭喜！您的作品频道「{channel.name}」已活跃满30天并获得「永久频道」资格，不会再被自动折叠！",
                                category=NotificationCategory.SYSTEM,
                                type=NotificationType.MILESTONE,
                                priority=NotificationPriority.NORMAL,
                                target_users=TargetUserType.CUSTOM,
                                custom_user_ids=[channel.creator_id],
                                status=NotificationStatus.ACTIVE,
                                published_at=now,
                                display_type=["notification"],
                            )
                            session.add(notification)
                            session.add(UserNotification(
                                user_id=channel.creator_id,
                                notification_id=notification.id,
                                is_read=False,
                                is_dismissed=False,
                                clicked=False,
                            ))

                # 更新warning_days
                elif channel.status == ChannelStatus.WARNING:
                    remaining_days = 7 - days_since_last_message
                    channel.warning_days = max(0, remaining_days)

            await session.commit()

            logger.info(
                f"Channel activity check completed: "
                f"{locked_count} locked, {warning_count} warned, {promoted_count} promoted"
            )

        except Exception as e:
            logger.error(f"Error in channel activity check: {e}", exc_info=True)
            await session.rollback()
