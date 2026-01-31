"""修复迁移记录"""
import asyncio
from sqlalchemy import text
from app.core.database import engine

async def fix_migration():
    async with engine.begin() as conn:
        # 删除错误的迁移记录
        await conn.execute(text("DELETE FROM alembic_version WHERE version_num = '16144b2711da'"))
        # 删除旧的tasks表
        await conn.execute(text("DROP TABLE IF EXISTS tasks CASCADE"))
        print("Fixed migration records and dropped old tasks table")

if __name__ == "__main__":
    asyncio.run(fix_migration())
