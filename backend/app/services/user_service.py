from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from datetime import datetime, timedelta, timezone
from uuid import UUID

from app.models.user import User
from app.models.user_session import UserSession
from app.schemas.user import (
    UserCreate,
    UserUpdate,
    NotificationSettings,
    Preferences,
    UserSessionResponse,
    validate_password_strength,
)
from app.core.security import get_password_hash, verify_password


class UserService:
    """用户服务"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        """根据 ID 获取用户"""
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """根据邮箱获取用户"""
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()
    
    async def get_user_by_username(self, username: str) -> Optional[User]:
        """根据用户名获取用户"""
        result = await self.db.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()
    
    async def get_users(
        self,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None
    ) -> List[User]:
        """获取用户列表"""
        query = select(User)
        
        if search:
            query = query.where(
                User.username.ilike(f"%{search}%") |
                User.email.ilike(f"%{search}%")
            )
        
        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def create_user(self, user_data: UserCreate) -> User:
        """创建用户"""
        # 检查用户名是否已存在
        existing = await self.get_user_by_username(user_data.username)
        if existing:
            raise ValueError("用户名已被使用，请更换其他用户名")

        # 如果提供了邮箱，检查是否已存在
        if user_data.email:
            existing = await self.get_user_by_email(user_data.email)
            if existing:
                raise ValueError("该邮箱已被注册，请使用其他邮箱或直接登录")
        
        # 创建用户
        user = User(
            username=user_data.username,
            hashed_password=get_password_hash(user_data.password),
            email=user_data.email,  # 可选
        )

        self.db.add(user)
        await self.db.flush()  # 只 flush，不 commit，让调用方控制事务
        await self.db.refresh(user)

        return user
    
    async def update_user(self, user_id: str, user_data: UserUpdate) -> Optional[User]:
        """更新用户"""
        user = await self.get_user_by_id(user_id)
        if not user:
            return None
        
        # 检查邮箱是否重复
        if user_data.email and user_data.email != user.email:
            existing = await self.get_user_by_email(user_data.email)
            if existing:
                raise ValueError("Email already in use")
        
        # 检查用户名是否重复
        if user_data.username and user_data.username != user.username:
            existing = await self.get_user_by_username(user_data.username)
            if existing:
                raise ValueError("Username already taken")
        
        # 更新字段
        update_data = user_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)

        await self.db.flush()
        await self.db.refresh(user)

        return user
    
    async def delete_user(self, user_id: str) -> bool:
        """删除用户"""
        user = await self.get_user_by_id(user_id)
        if not user:
            return False

        await self.db.delete(user)
        await self.db.flush()

        return True
    
    async def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """认证用户"""
        user = await self.get_user_by_username(username)
        if not user:
            user = await self.get_user_by_email(username)
        
        if not user:
            return None
        
        if not verify_password(password, user.hashed_password):
            return None
        
        # 更新最后登录时间
        user.last_login_at = datetime.now(timezone.utc)
        await self.db.flush()

        return user

    async def get_notification_settings(self, user_id: str) -> NotificationSettings:
        """获取用户通知设置"""
        user = await self.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        data = user.notification_settings or {}
        return NotificationSettings.model_validate(data)

    async def update_notification_settings(
        self,
        user_id: str,
        settings: NotificationSettings
    ) -> NotificationSettings:
        """更新用户通知设置"""
        user = await self.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        user.notification_settings = settings.model_dump()
        await self.db.flush()
        await self.db.refresh(user)
        return NotificationSettings.model_validate(user.notification_settings or {})

    async def get_preferences(self, user_id: str) -> Preferences:
        """获取用户偏好设置"""
        user = await self.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        data = user.preferences or {}
        return Preferences.model_validate(data)

    async def update_preferences(
        self,
        user_id: str,
        preferences: Preferences
    ) -> Preferences:
        """更新用户偏好设置"""
        user = await self.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        user.preferences = preferences.model_dump()
        await self.db.flush()
        await self.db.refresh(user)
        return Preferences.model_validate(user.preferences or {})

    async def change_password(self, user_id: str, current_password: str, new_password: str) -> None:
        """修改用户密码"""
        user = await self.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        if not verify_password(current_password, user.hashed_password):
            raise ValueError("当前密码不正确")

        if verify_password(new_password, user.hashed_password):
            raise ValueError("新密码不能与当前密码相同")

        # 验证新密码强度
        try:
            validate_password_strength(new_password)
        except ValueError as e:
            raise ValueError(str(e))

        user.hashed_password = get_password_hash(new_password)
        await self.db.flush()

    async def update_user_password(self, user_id: str, new_password: str) -> None:
        """
        更新用户密码（用于忘记密码场景，不验证当前密码）

        Args:
            user_id: 用户ID
            new_password: 新密码

        Raises:
            ValueError: 用户不存在或密码强度不足
        """
        user = await self.get_user_by_id(user_id)
        if not user:
            raise ValueError("用户不存在")

        # 验证新密码强度
        try:
            validate_password_strength(new_password)
        except ValueError as e:
            raise ValueError(str(e))

        user.hashed_password = get_password_hash(new_password)
        user.updated_at = datetime.now(timezone.utc)
        await self.db.flush()

    async def soft_delete_user(self, user_id: str, password: str) -> None:
        """软删除用户账号"""
        user = await self.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        if not verify_password(password, user.hashed_password):
            raise ValueError("Password is incorrect")

        user.is_active = False
        user.is_verified = False
        user.username = f"deleted_{user.id}"
        # keep a valid placeholder email to satisfy response schema and uniqueness
        user.email = f"deleted+{user.id}@example.invalid"
        user.full_name = None
        user.bio = None
        user.avatar = None
        user.notification_settings = {}
        user.preferences = {}

        await self.db.flush()

    async def update_avatar(self, user_id: str, avatar_url: str) -> User:
        """更新用户头像"""
        user = await self.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        user.avatar = avatar_url
        await self.db.flush()
        await self.db.refresh(user)
        return user

    # ==================== 会话管理 ====================

    async def create_session(
        self,
        user_id: str,
        session_token: str,
        device_info: dict,
        ip_address: Optional[str] = None
    ) -> UserSession:
        """
        创建用户会话

        Args:
            user_id: 用户ID
            session_token: 会话令牌（access_token）
            device_info: 设备信息字典
            ip_address: IP地址

        Returns:
            UserSession 对象
        """
        # 计算过期时间（与 access_token 一致）
        from app.core.config import settings
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        session = UserSession(
            user_id=UUID(user_id),
            session_token=session_token,
            device_type=device_info.get('device_type'),
            device_name=device_info.get('device_name'),
            browser=device_info.get('browser'),
            browser_version=device_info.get('browser_version'),
            operating_system=device_info.get('operating_system'),
            ip_address=ip_address,
            user_agent=device_info.get('user_agent'),
            is_active=True,
            last_active_at=datetime.now(timezone.utc),
            expires_at=expires_at,
        )

        self.db.add(session)
        await self.db.flush()
        await self.db.refresh(session)

        return session

    async def get_user_sessions(
        self,
        user_id: str,
        current_token: Optional[str] = None
    ) -> List[UserSessionResponse]:
        """
        获取用户所有活跃会话

        Args:
            user_id: 用户ID
            current_token: 当前会话token，用于标记当前设备

        Returns:
            会话列表
        """
        result = await self.db.execute(
            select(UserSession)
            .where(
                and_(
                    UserSession.user_id == UUID(user_id),
                    UserSession.is_active == True
                )
            )
            .order_by(UserSession.last_active_at.desc())
        )
        sessions = result.scalars().all()

        # 转换为响应格式，并标记当前会话
        session_responses = []
        for session in sessions:
            response = UserSessionResponse.model_validate(session)
            # 判断是否为当前会话
            if current_token and session.session_token == current_token:
                response.is_current = True
            session_responses.append(response)

        return session_responses

    async def logout_session(self, user_id: str, session_id: str) -> bool:
        """
        退出指定会话

        Args:
            user_id: 用户ID
            session_id: 会话ID

        Returns:
            是否成功
        """
        result = await self.db.execute(
            select(UserSession)
            .where(
                and_(
                    UserSession.id == UUID(session_id),
                    UserSession.user_id == UUID(user_id)
                )
            )
        )
        session = result.scalar_one_or_none()

        if not session:
            raise ValueError("Session not found")

        # 标记会话为非活跃
        session.is_active = False
        session.logged_out_at = datetime.now(timezone.utc)

        await self.db.flush()
        return True

    async def logout_other_sessions(self, user_id: str, current_token: str) -> int:
        """
        退出除当前会话外的所有会话

        Args:
            user_id: 用户ID
            current_token: 当前会话token

        Returns:
            退出的会话数量
        """
        result = await self.db.execute(
            select(UserSession)
            .where(
                and_(
                    UserSession.user_id == UUID(user_id),
                    UserSession.is_active == True,
                    UserSession.session_token != current_token
                )
            )
        )
        sessions = result.scalars().all()

        count = 0
        for session in sessions:
            session.is_active = False
            session.logged_out_at = datetime.now(timezone.utc)
            count += 1

        await self.db.flush()
        return count

    async def update_session_activity(self, session_token: str) -> None:
        """
        更新会话活动时间

        Args:
            session_token: 会话token
        """
        result = await self.db.execute(
            select(UserSession)
            .where(UserSession.session_token == session_token)
        )
        session = result.scalar_one_or_none()

        if session:
            session.last_active_at = datetime.now(timezone.utc)
            await self.db.flush()

    async def update_email(self, user_id: str, new_email: str) -> User:
        """
        更新用户邮箱

        Args:
            user_id: 用户ID
            new_email: 新邮箱地址

        Returns:
            更新后的用户对象

        Raises:
            ValueError: 邮箱已被使用或用户不存在
        """
        user = await self.get_user_by_id(user_id)
        if not user:
            raise ValueError("用户不存在")

        # 检查新邮箱是否与当前邮箱相同
        if user.email == new_email:
            raise ValueError("新邮箱不能与当前邮箱相同")

        # 检查新邮箱是否已被其他用户使用
        existing = await self.get_user_by_email(new_email)
        if existing and str(existing.id) != user_id:
            raise ValueError("该邮箱已被其他用户使用")

        # 更新邮箱
        user.email = new_email
        user.updated_at = datetime.now(timezone.utc)

        await self.db.flush()
        await self.db.refresh(user)

        return user

