"""
检查数据库中的 chapterstatus 枚举值
"""
import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

async def check_enum_values():
    """检查数据库中的枚举值"""
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as db:
        try:
            # 查询枚举值
            result = await db.execute(text("""
                SELECT enumlabel
                FROM pg_enum
                WHERE enumtypid = (
                    SELECT oid FROM pg_type WHERE typname = 'chapterstatus'
                )
                ORDER BY enumsortorder;
            """))

            enum_values = [row[0] for row in result.fetchall()]

            print("=" * 60)
            print("数据库中的 chapterstatus 枚举值:")
            print("=" * 60)
            for value in enum_values:
                print(f"  - {value!r}")
            print("=" * 60)

            print("\nPython 模型中定义的枚举值:")
            print("=" * 60)
            from app.models.chapter import ChapterStatus
            for status in ChapterStatus:
                print(f"  - {status.name} = {status.value!r}")
            print("=" * 60)

        except Exception as e:
            print(f"错误: {e}")
            import traceback
            traceback.print_exc()
        finally:
            await engine.dispose()

if __name__ == "__main__":
    asyncio.run(check_enum_values())
