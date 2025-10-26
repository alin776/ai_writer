"""
Pytest 配置文件

设置测试环境、导入路径和共享 fixtures
"""

import sys
from pathlib import Path
import pytest
import pytest_asyncio
from uuid import uuid4

# 添加 backend 目录到 Python 路径
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))


# ========== 共享 Fixtures ==========

@pytest_asyncio.fixture(scope="function")
async def db_session():
    """数据库会话 - 自动事务回滚"""
    from app.core.database import async_session_maker

    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.rollback()  # 测试后回滚，自动清理所有测试数据


async def create_test_user(db_session):
    """辅助函数 - 创建测试用户并返回ID"""
    from app.models.user import User

    user_id = uuid4()
    test_user = User(
        id=user_id,
        username=f"test_user_{user_id.hex[:8]}",
        email=f"test_{user_id.hex[:8]}@example.com",
        hashed_password="dummy_hash_for_test",
        is_active=True
    )

    db_session.add(test_user)
    await db_session.flush()  # 使用 flush 而不是 commit

    return user_id
