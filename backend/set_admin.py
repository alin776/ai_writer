"""
设置用户为管理员的脚本

用法:
python set_admin.py
"""

import asyncio
from sqlalchemy import select, update
from app.core.database import SessionLocal
from app.models.user import User

async def set_user_as_admin():
    """将指定用户设为管理员"""

    # 这里填写要设为管理员的用户名或用户ID
    username = "123"  # 修改为你的用户名
    # 或者使用 user_id = "7a34938e-bfbd-4300-a0fa-5070b17d186a"

    db = SessionLocal()

    try:
        # 查找用户
        result = await db.execute(
            select(User).where(User.username == username)
        )
        user = result.scalar_one_or_none()

        if not user:
            print(f"❌ 未找到用户: {username}")
            return

        print(f"找到用户: {user.username} (ID: {user.id})")
        print(f"当前管理员状态: {user.is_admin}")

        # 设置为管理员
        user.is_admin = True
        await db.commit()

        print(f"✅ 成功将用户 {username} 设置为管理员！")

        # 验证
        await db.refresh(user)
        print(f"验证: is_admin = {user.is_admin}")

    except Exception as e:
        print(f"❌ 错误: {e}")
        await db.rollback()
    finally:
        await db.close()


if __name__ == "__main__":
    asyncio.run(set_user_as_admin())
