"""检查数据库中的表"""
import asyncio
from app.core.database import engine
from sqlalchemy import text

async def check_tables():
    async with engine.begin() as conn:
        # 查询所有表
        result = await conn.execute(
            text("SELECT tablename FROM pg_tables WHERE schemaname='public' ORDER BY tablename")
        )
        tables = [row[0] for row in result]
        
        print("数据库中的表:")
        print("=" * 50)
        for table in tables:
            print(f"  - {table}")
        
        print("\n" + "=" * 50)
        print(f"总计: {len(tables)} 个表")
        
        # 检查 alembic_version
        result = await conn.execute(text("SELECT version_num FROM alembic_version"))
        version = result.fetchone()
        if version:
            print(f"\nAlembic 当前版本: {version[0]}")
        else:
            print("\n警告: alembic_version 表为空")

if __name__ == "__main__":
    asyncio.run(check_tables())
