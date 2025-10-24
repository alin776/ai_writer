"""检查AI日志数据库状态"""
import asyncio
from app.core.database import AsyncSessionLocal
from sqlalchemy import select, func
from app.models.ai_call_log import AICallLog
from datetime import datetime, timezone

async def check_logs():
    async with AsyncSessionLocal() as db:
        # 1. 检查总数
        count = await db.scalar(select(func.count(AICallLog.id)))
        print(f"✅ AI日志总数: {count}")

        if count == 0:
            print("❌ 数据库中没有AI日志数据")
            return

        # 2. 查看最近的日志
        result = await db.execute(
            select(AICallLog)
            .order_by(AICallLog.created_at.desc())
            .limit(5)
        )
        logs = result.scalars().all()

        print(f"\n📋 最近{len(logs)}条日志:")
        for i, log in enumerate(logs, 1):
            print(f"\n{i}. 日志详情:")
            print(f"   - ID: {log.id}")
            print(f"   - 用户ID: {log.user_id}")
            print(f"   - 操作类型: {log.operation_type}")
            print(f"   - 模型: {log.model_name}")
            print(f"   - 创建时间: {log.created_at}")
            print(f"   - 时区信息: {log.created_at.tzinfo}")
            print(f"   - 成功: {log.is_success}")
            print(f"   - Tokens: {log.total_tokens}")
            print(f"   - 成本: ${log.total_cost}")

        # 3. 检查时间范围
        min_time = await db.scalar(select(func.min(AICallLog.created_at)))
        max_time = await db.scalar(select(func.max(AICallLog.created_at)))
        print(f"\n⏰ 时间范围:")
        print(f"   - 最早: {min_time}")
        print(f"   - 最晚: {max_time}")

        # 4. 当前UTC时间
        now_utc = datetime.utcnow()
        print(f"\n🌍 当前UTC时间: {now_utc}")
        print(f"   - 本地时间: {datetime.now()}")

        # 5. 测试统计查询
        print("\n📊 测试统计查询:")

        # 无时间限制的统计
        total = await db.scalar(select(func.count(AICallLog.id)))
        print(f"   - 无时间限制: {total} 条")

        # 最近24小时
        from datetime import timedelta
        yesterday = now_utc - timedelta(days=1)
        recent_count = await db.scalar(
            select(func.count(AICallLog.id))
            .where(AICallLog.created_at >= yesterday)
        )
        print(f"   - 最近24小时: {recent_count} 条")

        # 最近7天
        week_ago = now_utc - timedelta(days=7)
        week_count = await db.scalar(
            select(func.count(AICallLog.id))
            .where(AICallLog.created_at >= week_ago)
        )
        print(f"   - 最近7天: {week_count} 条")

if __name__ == "__main__":
    asyncio.run(check_logs())
