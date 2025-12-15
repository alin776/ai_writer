from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func, delete
from datetime import datetime, timedelta, timezone
from uuid import UUID

from app.models.notification import (
    Notification,
    UserNotification,
    NotificationTemplate,
    NotificationCategory,
    NotificationType,
    NotificationPriority,
    NotificationStatus,
    TargetUserType
)
from app.models.user import User
from app.schemas.notification import (
    NotificationCreate,
    NotificationUpdate,
    NotificationTemplateCreate,
    NotificationTemplateUpdate,
)


class NotificationService:
    """通知服务"""

    def __init__(self, db: AsyncSession):
        self.db = db

    # ==================== 通知CRUD ====================

    async def create_notification(
        self,
        notification_data: NotificationCreate,
        created_by: Optional[UUID] = None
    ) -> Notification:
        """
        创建通知

        Args:
            notification_data: 通知创建数据
            created_by: 创建者ID（管理员）
        """
        # 确定通知状态
        status = NotificationStatus.DRAFT
        published_at = None

        if notification_data.publish_type == "immediate":
            status = NotificationStatus.ACTIVE
            published_at = datetime.now(timezone.utc)
        elif notification_data.publish_type == "scheduled" and notification_data.scheduled_at:
            status = NotificationStatus.SCHEDULED
            published_at = notification_data.scheduled_at

        # 转换 ActionButton 为字典
        action_button_dict = None
        if notification_data.action_button:
            action_button_dict = notification_data.action_button.model_dump()

        # 调试日志：打印接收到的活动数据
        print(f"🔧 创建通知 - 接收到的数据:")
        print(f"  activity_type: {notification_data.activity_type}")
        print(f"  activity_rules: {notification_data.activity_rules}")

        # 创建通知
        notification = Notification(
            title=notification_data.title,
            content=notification_data.content,
            cover_image_url=notification_data.cover_image_url,
            category=notification_data.category,
            type=notification_data.type,
            priority=notification_data.priority,
            display_type=notification_data.display_type,
            action_button=action_button_dict,
            banner_color=notification_data.banner_color,
            target_users=notification_data.target_users,
            custom_user_ids=notification_data.custom_user_ids,
            status=status,
            published_at=published_at,
            valid_from=notification_data.valid_from,
            valid_until=notification_data.valid_until,
            allow_dismiss=notification_data.allow_dismiss,
            show_once=notification_data.show_once,
            # 活动相关字段
            activity_type=notification_data.activity_type,
            activity_rules=notification_data.activity_rules,
            created_by=created_by
        )

        self.db.add(notification)
        await self.db.commit()
        await self.db.refresh(notification)

        # 如果立即发布，创建用户通知关系
        if status == NotificationStatus.ACTIVE:
            await self._create_user_notifications(notification)

        return notification

    async def get_notification(self, notification_id: UUID) -> Optional[Notification]:
        """获取单个通知"""
        result = await self.db.execute(
            select(Notification).where(Notification.id == notification_id)
        )
        return result.scalar_one_or_none()

    async def get_notifications(
        self,
        skip: int = 0,
        limit: int = 100,
        category: Optional[NotificationCategory] = None,
        status: Optional[NotificationStatus] = None,
        type: Optional[NotificationType] = None,
    ) -> tuple[List[Notification], int]:
        """
        获取通知列表（管理员视角）

        Returns:
            (通知列表, 总数)
        """
        # 构建查询条件
        conditions = []
        if category:
            conditions.append(Notification.category == category)
        if status:
            conditions.append(Notification.status == status)
        if type:
            conditions.append(Notification.type == type)

        # 查询总数
        count_query = select(func.count(Notification.id))
        if conditions:
            count_query = count_query.where(and_(*conditions))
        total_result = await self.db.execute(count_query)
        total = total_result.scalar()

        # 查询列表
        query = select(Notification).order_by(Notification.created_at.desc())
        if conditions:
            query = query.where(and_(*conditions))
        query = query.offset(skip).limit(limit)

        result = await self.db.execute(query)
        notifications = result.scalars().all()

        return list(notifications), total

    async def update_notification(
        self,
        notification_id: UUID,
        notification_data: NotificationUpdate
    ) -> Optional[Notification]:
        """更新通知"""
        notification = await self.get_notification(notification_id)
        if not notification:
            return None

        # 更新字段
        update_data = notification_data.model_dump(exclude_unset=True)

        # 调试日志：打印更新数据
        print(f"\n{'='*80}")
        print(f"🔧 更新通知 ID: {notification_id}")
        print(f"{'='*80}")
        print(f"接收到的字段: {list(update_data.keys())}")
        print(f"activity_type: {update_data.get('activity_type')}")
        print(f"activity_rules: {update_data.get('activity_rules')}")
        print(f"{'='*80}\n")

        # 特殊处理 action_button
        if "action_button" in update_data and update_data["action_button"]:
            if hasattr(update_data["action_button"], "model_dump"):
                update_data["action_button"] = update_data["action_button"].model_dump()

        # 逐个更新字段
        for field, value in update_data.items():
            if hasattr(notification, field):
                setattr(notification, field, value)
                print(f"✅ 更新字段 {field}: {value if field not in ['activity_rules'] else '(JSONB data)'}")
            else:
                print(f"⚠️  跳过不存在的字段: {field}")

        notification.updated_at = datetime.now(timezone.utc)

        # 提交并刷新
        await self.db.commit()
        await self.db.refresh(notification)

        # 验证保存结果
        print(f"\n{'='*80}")
        print(f"✅ 保存后验证:")
        print(f"activity_type: {notification.activity_type}")
        print(f"activity_rules: {notification.activity_rules}")
        print(f"{'='*80}\n")

        return notification

    async def delete_notification(self, notification_id: UUID) -> bool:
        """删除通知"""
        notification = await self.get_notification(notification_id)
        if not notification:
            return False

        await self.db.delete(notification)
        await self.db.commit()
        return True

    async def publish_notification(self, notification_id: UUID) -> Optional[Notification]:
        """发布通知（将草稿/定时通知设为激活）"""
        notification = await self.get_notification(notification_id)
        if not notification:
            return None

        notification.status = NotificationStatus.ACTIVE
        notification.published_at = datetime.now(timezone.utc)

        await self.db.commit()
        await self.db.refresh(notification)

        # 创建用户通知关系
        await self._create_user_notifications(notification)

        return notification

    # ==================== 用户通知相关 ====================

    async def get_user_notifications(
        self,
        user_id: UUID,
        skip: int = 0,
        limit: int = 20,
        is_read: Optional[bool] = None,
        display_type: Optional[str] = None,
    ) -> tuple[List[Dict[str, Any]], int, int]:
        """
        获取用户的通知列表

        Args:
            user_id: 用户ID
            skip: 跳过数量
            limit: 限制数量
            is_read: 是否已读（None=全部）
            display_type: 展示类型筛选（modal/banner/notification）

        Returns:
            (通知列表, 总数, 未读数)
        """
        # 基础查询：关联 UserNotification 和 Notification
        base_query = (
            select(UserNotification, Notification)
            .join(Notification, UserNotification.notification_id == Notification.id)
            .where(
                and_(
                    UserNotification.user_id == user_id,
                    UserNotification.is_dismissed == False,  # 过滤掉已删除的通知
                    Notification.status == NotificationStatus.ACTIVE,
                    or_(
                        Notification.valid_until.is_(None),
                        Notification.valid_until > datetime.now(timezone.utc)
                    )
                )
            )
        )

        # 添加筛选条件
        conditions = []
        if is_read is not None:
            conditions.append(UserNotification.is_read == is_read)
        if display_type:
            conditions.append(Notification.display_type.contains([display_type]))

        if conditions:
            base_query = base_query.where(and_(*conditions))

        # 查询总数
        count_query = select(func.count(UserNotification.id)).select_from(
            UserNotification
        ).join(Notification, UserNotification.notification_id == Notification.id).where(
            base_query.whereclause
        )
        total_result = await self.db.execute(count_query)
        total = total_result.scalar()

        # 查询未读数
        unread_query = select(func.count(UserNotification.id)).select_from(
            UserNotification
        ).join(Notification, UserNotification.notification_id == Notification.id).where(
            and_(
                UserNotification.user_id == user_id,
                UserNotification.is_read == False,
                UserNotification.is_dismissed == False,  # 过滤掉已删除的通知
                Notification.status == NotificationStatus.ACTIVE,
                or_(
                    Notification.valid_until.is_(None),
                    Notification.valid_until > datetime.now(timezone.utc)
                )
            )
        )
        unread_result = await self.db.execute(unread_query)
        unread_count = unread_result.scalar()

        # 查询列表
        query = base_query.order_by(UserNotification.created_at.desc())
        query = query.offset(skip).limit(limit)

        result = await self.db.execute(query)
        rows = result.all()

        # 组合数据
        notifications_list = []
        for user_notif, notif in rows:
            notifications_list.append({
                "id": notif.id,
                "title": notif.title,
                "content": notif.content,
                "cover_image_url": notif.cover_image_url,
                "category": notif.category,
                "type": notif.type,
                "priority": notif.priority,
                "display_type": notif.display_type,
                "action_button": notif.action_button,
                "banner_color": notif.banner_color,
                # 活动相关字段
                "activity_type": notif.activity_type,
                "activity_rules": notif.activity_rules,
                "is_read": user_notif.is_read,
                "read_at": user_notif.read_at,
                "is_dismissed": user_notif.is_dismissed,
                "dismissed_at": user_notif.dismissed_at,
                "clicked": user_notif.clicked,
                "clicked_at": user_notif.clicked_at,
                "created_at": user_notif.created_at,
                "published_at": notif.published_at,
                "valid_from": notif.valid_from,
                "valid_until": notif.valid_until,
            })

        return notifications_list, total, unread_count

    async def get_unread_count(self, user_id: UUID) -> int:
        """获取用户未读通知数量"""
        query = select(func.count(UserNotification.id)).select_from(
            UserNotification
        ).join(Notification, UserNotification.notification_id == Notification.id).where(
            and_(
                UserNotification.user_id == user_id,
                UserNotification.is_read == False,
                UserNotification.is_dismissed == False,  # 过滤掉已删除的通知
                Notification.status == NotificationStatus.ACTIVE,
                or_(
                    Notification.valid_until.is_(None),
                    Notification.valid_until > datetime.now(timezone.utc)
                )
            )
        )
        result = await self.db.execute(query)
        return result.scalar()

    async def mark_as_read(
        self,
        user_id: UUID,
        notification_ids: Optional[List[UUID]] = None
    ) -> int:
        """
        标记通知为已读

        Args:
            user_id: 用户ID
            notification_ids: 通知ID列表，为None则标记全部未读为已读

        Returns:
            影响的记录数
        """
        conditions = [
            UserNotification.user_id == user_id,
            UserNotification.is_read == False
        ]

        if notification_ids:
            conditions.append(UserNotification.notification_id.in_(notification_ids))

        # 查询需要更新的记录
        query = select(UserNotification).where(and_(*conditions))
        result = await self.db.execute(query)
        user_notifications = result.scalars().all()

        # 更新为已读
        count = 0
        now = datetime.now(timezone.utc)
        for un in user_notifications:
            un.is_read = True
            un.read_at = now
            count += 1

        await self.db.commit()
        return count

    async def dismiss_notification(self, user_id: UUID, notification_id: UUID) -> bool:
        """关闭通知弹窗"""
        query = select(UserNotification).where(
            and_(
                UserNotification.user_id == user_id,
                UserNotification.notification_id == notification_id
            )
        )
        result = await self.db.execute(query)
        user_notification = result.scalar_one_or_none()

        if not user_notification:
            return False

        user_notification.is_dismissed = True
        user_notification.dismissed_at = datetime.now(timezone.utc)

        await self.db.commit()
        return True

    async def click_action_button(self, user_id: UUID, notification_id: UUID) -> bool:
        """记录用户点击了行动按钮"""
        query = select(UserNotification).where(
            and_(
                UserNotification.user_id == user_id,
                UserNotification.notification_id == notification_id
            )
        )
        result = await self.db.execute(query)
        user_notification = result.scalar_one_or_none()

        if not user_notification:
            return False

        user_notification.clicked = True
        user_notification.clicked_at = datetime.now(timezone.utc)

        # 同时标记为已读
        if not user_notification.is_read:
            user_notification.is_read = True
            user_notification.read_at = datetime.now(timezone.utc)

        await self.db.commit()
        return True

    # ==================== 统计相关 ====================

    async def get_notification_stats(self, notification_id: UUID) -> Optional[Dict[str, Any]]:
        """获取通知统计数据"""
        notification = await self.get_notification(notification_id)
        if not notification:
            return None

        # 总触达用户数
        total_query = select(func.count(UserNotification.id)).where(
            UserNotification.notification_id == notification_id
        )
        total_result = await self.db.execute(total_query)
        total_users = total_result.scalar()

        # 已读用户数
        read_query = select(func.count(UserNotification.id)).where(
            and_(
                UserNotification.notification_id == notification_id,
                UserNotification.is_read == True
            )
        )
        read_result = await self.db.execute(read_query)
        read_count = read_result.scalar()

        # 关闭弹窗用户数
        dismissed_query = select(func.count(UserNotification.id)).where(
            and_(
                UserNotification.notification_id == notification_id,
                UserNotification.is_dismissed == True
            )
        )
        dismissed_result = await self.db.execute(dismissed_query)
        dismissed_count = dismissed_result.scalar()

        # 点击行动按钮用户数
        clicked_query = select(func.count(UserNotification.id)).where(
            and_(
                UserNotification.notification_id == notification_id,
                UserNotification.clicked == True
            )
        )
        clicked_result = await self.db.execute(clicked_query)
        clicked_count = clicked_result.scalar()

        # 计算比率
        read_rate = (read_count / total_users * 100) if total_users > 0 else 0
        click_rate = (clicked_count / total_users * 100) if total_users > 0 else 0

        return {
            "notification_id": notification.id,
            "title": notification.title,
            "total_users": total_users,
            "read_count": read_count,
            "dismissed_count": dismissed_count,
            "clicked_count": clicked_count,
            "read_rate": round(read_rate, 2),
            "click_rate": round(click_rate, 2),
            "published_at": notification.published_at,
            "valid_until": notification.valid_until,
        }

    # ==================== 定时任务相关 ====================

    async def activate_scheduled_notifications(self) -> int:
        """激活定时通知（供定时任务调用）"""
        now = datetime.now(timezone.utc)

        # 查找需要激活的定时通知
        query = select(Notification).where(
            and_(
                Notification.status == NotificationStatus.SCHEDULED,
                Notification.published_at <= now
            )
        )
        result = await self.db.execute(query)
        notifications = result.scalars().all()

        count = 0
        for notification in notifications:
            notification.status = NotificationStatus.ACTIVE
            await self._create_user_notifications(notification)
            count += 1

        await self.db.commit()
        return count

    async def expire_notifications(self) -> int:
        """过期通知（供定时任务调用）"""
        now = datetime.now(timezone.utc)

        query = select(Notification).where(
            and_(
                Notification.status == NotificationStatus.ACTIVE,
                Notification.valid_until.isnot(None),
                Notification.valid_until <= now
            )
        )
        result = await self.db.execute(query)
        notifications = result.scalars().all()

        count = 0
        for notification in notifications:
            notification.status = NotificationStatus.EXPIRED
            count += 1

        await self.db.commit()
        return count

    # ==================== 内部辅助方法 ====================

    async def _create_user_notifications(self, notification: Notification) -> int:
        """
        为通知创建用户通知关系

        Returns:
            创建的记录数
        """
        # 确定目标用户
        user_ids = await self._get_target_user_ids(notification)

        # 创建 UserNotification 记录
        count = 0
        for user_id in user_ids:
            # 检查是否已存在
            existing_query = select(UserNotification).where(
                and_(
                    UserNotification.user_id == user_id,
                    UserNotification.notification_id == notification.id
                )
            )
            existing_result = await self.db.execute(existing_query)
            if existing_result.scalar_one_or_none():
                continue  # 已存在，跳过

            user_notification = UserNotification(
                user_id=user_id,
                notification_id=notification.id,
                is_read=False,
                is_dismissed=False,
                clicked=False
            )
            self.db.add(user_notification)
            count += 1

        await self.db.commit()
        return count

    async def _get_target_user_ids(self, notification: Notification) -> List[UUID]:
        """获取目标用户ID列表"""
        if notification.target_users == TargetUserType.ALL:
            # 全部活跃用户
            query = select(User.id).where(User.is_active == True)
            result = await self.db.execute(query)
            return [row[0] for row in result.all()]

        elif notification.target_users == TargetUserType.ACTIVE:
            # 最近7天登录的用户
            seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)
            query = select(User.id).where(
                and_(
                    User.is_active == True,
                    User.last_login_at >= seven_days_ago
                )
            )
            result = await self.db.execute(query)
            return [row[0] for row in result.all()]

        elif notification.target_users == TargetUserType.INACTIVE:
            # 超过7天未登录的用户
            seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)
            query = select(User.id).where(
                and_(
                    User.is_active == True,
                    or_(
                        User.last_login_at < seven_days_ago,
                        User.last_login_at.is_(None)
                    )
                )
            )
            result = await self.db.execute(query)
            return [row[0] for row in result.all()]

        elif notification.target_users == TargetUserType.CUSTOM:
            # 自定义用户列表
            return notification.custom_user_ids or []

        return []

    # ==================== 通知模板相关 ====================

    async def create_template(self, template_data: NotificationTemplateCreate) -> NotificationTemplate:
        """创建通知模板"""
        template = NotificationTemplate(**template_data.model_dump())
        self.db.add(template)
        await self.db.commit()
        await self.db.refresh(template)
        return template

    async def get_template(self, template_id: UUID) -> Optional[NotificationTemplate]:
        """获取通知模板"""
        result = await self.db.execute(
            select(NotificationTemplate).where(NotificationTemplate.id == template_id)
        )
        return result.scalar_one_or_none()

    async def get_template_by_name(self, name: str) -> Optional[NotificationTemplate]:
        """根据名称获取通知模板"""
        result = await self.db.execute(
            select(NotificationTemplate).where(NotificationTemplate.name == name)
        )
        return result.scalar_one_or_none()

    async def create_notification_from_template(
        self,
        template_name: str,
        variables: Dict[str, str],
        user_id: Optional[UUID] = None
    ) -> Optional[Notification]:
        """
        从模板创建系统通知

        Args:
            template_name: 模板名称
            variables: 变量替换字典，如 {"username": "张三", "chapter_title": "第一章"}
            user_id: 目标用户ID（如果是单个用户的通知）
        """
        template = await self.get_template_by_name(template_name)
        if not template:
            return None

        # 替换变量
        title = template.title_template
        content = template.content_template

        for key, value in variables.items():
            placeholder = f"{{{{{key}}}}}"  # {{key}}
            title = title.replace(placeholder, str(value))
            if content:
                content = content.replace(placeholder, str(value))

        # 创建通知
        notification = Notification(
            title=title,
            content=content,
            category=NotificationCategory.SYSTEM,
            type=template.type,
            priority=template.default_priority,
            display_type=["notification"],  # 系统通知默认只在通知列表显示
            target_users=TargetUserType.CUSTOM if user_id else TargetUserType.ALL,
            custom_user_ids=[user_id] if user_id else None,
            status=NotificationStatus.ACTIVE,
            published_at=datetime.now(timezone.utc),
            allow_dismiss=True,
            show_once=False
        )

        self.db.add(notification)
        await self.db.commit()
        await self.db.refresh(notification)

        # 创建用户通知关系
        await self._create_user_notifications(notification)

        return notification
