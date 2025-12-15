"""查询用户列表"""
import asyncio
import sys
sys.path.insert(0, '.')

async def main():
    from app.core.database import async_session_maker
    from app.models.user import User
    from sqlalchemy import select

    async with async_session_maker() as session:
        result = await session.execute(
            select(User.id, User.username, User.email, User.is_admin, User.is_active, User.created_at)
            .order_by(User.created_at.desc())
        )
        users = result.all()

        print(f"\n共 {len(users)} 个用户:")
        print("-" * 100)
        for u in users:
            admin = "是" if u.is_admin else "否"
            active = "是" if u.is_active else "否"
            print(f"{str(u.id)[:8]}... | {u.username:<15} | {u.email:<30} | 管理员:{admin} | 激活:{active} | {str(u.created_at)[:19]}")
        print("-" * 100)

if __name__ == "__main__":
    asyncio.run(main())
