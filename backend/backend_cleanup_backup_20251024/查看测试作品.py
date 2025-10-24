"""
快速查看测试作品信息
"""
import asyncio
from app.core.database import get_db
from app.models.work import Work
from sqlalchemy import select


async def main():
    async for db in get_db():
        # 查找最新的测试作品
        result = await db.execute(
            select(Work)
            .where(Work.title.like('性能测试作品%'))
            .order_by(Work.created_at.desc())
            .limit(1)
        )
        work = result.scalar_one_or_none()
        
        if work:
            print("=" * 60)
            print("找到测试作品！")
            print("=" * 60)
            print(f"作品ID: {work.id}")
            print(f"作品标题: {work.title}")
            print(f"创建时间: {work.created_at}")
            print(f"章节数: {work.total_chapters}")
            print()
            print("📱 前端查看地址:")
            print(f"http://localhost:5173/works/{work.id}")
            print()
            print("🔗 后端API地址:")
            print(f"http://localhost:8000/api/v1/analysis/works/{work.id}/result")
            print("=" * 60)
        else:
            print("未找到测试作品，请先运行压测脚本")
        
        break


if __name__ == "__main__":
    asyncio.run(main())
