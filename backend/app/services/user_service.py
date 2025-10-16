from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from datetime import datetime

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
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
            raise ValueError("Username already taken")

        # 如果提供了邮箱，检查是否已存在
        if user_data.email:
            existing = await self.get_user_by_email(user_data.email)
            if existing:
                raise ValueError("Email already registered")

        # 创建用户
        user = User(
            username=user_data.username,
            hashed_password=get_password_hash(user_data.password),
            email=user_data.email,  # 可选
        )

        self.db.add(user)
        await self.db.flush()  # flush 而不是 commit，这样如果后续有错误可以回滚
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
        
        await self.db.commit()
        await self.db.refresh(user)
        
        return user
    
    async def delete_user(self, user_id: str) -> bool:
        """删除用户"""
        user = await self.get_user_by_id(user_id)
        if not user:
            return False
        
        await self.db.delete(user)
        await self.db.commit()
        
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
        user.last_login_at = datetime.utcnow()
        await self.db.flush()  # flush 而不是 commit
        await self.db.refresh(user)  # 刷新对象，确保所有字段都已加载

        return user
