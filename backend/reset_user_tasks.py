"""重置用户任务进度的脚本"""
import asyncio
import sys
import os
from pathlib import Path

# 添加backend目录到Python路径
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

# 加载环境变量
from dotenv import load_dotenv
env_path = backend_dir / '.env'
if env_path.exists():
    load_dotenv(env_path)
    print(f"✅ 已加载环境变量: {env_path}")
else:
    print(f"⚠️  未找到 .env 文件: {env_path}")

from sqlalchemy import text
from app.core.database import AsyncSessionLocal


async def reset_user_tasks():
    """重置所有用户任务"""
    async with AsyncSessionLocal() as session:
        try:
            print("🔄 正在重置所有用户任务...")

            # 重置所有用户任务
            await session.execute(text("""
                UPDATE user_tasks
                SET
                    current_progress = 0,
                    is_completed = false,
                    completed_at = NULL,
                    is_claimed = false,
                    claimed_at = NULL,
                    claimed_credits = 0,
                    reset_date = NULL,
                    updated_at = NOW()
            """))

            await session.commit()
            print("✅ 所有用户任务已重置")

            # 显示当前任务状态
            result = await session.execute(text("""
                SELECT
                    ut.id,
                    tt.title,
                    tt.task_key,
                    ut.current_progress,
                    ut.target_progress,
                    ut.is_completed,
                    ut.is_claimed
                FROM user_tasks ut
                JOIN task_templates tt ON ut.template_id = tt.id
                ORDER BY tt.sort_order
            """))

            print("\n📋 当前任务状态:")
            rows = result.fetchall()
            if rows:
                for row in rows:
                    status = "✅ 已完成" if row.is_completed else "⏳ 进行中"
                    claimed = "💰 已领取" if row.is_claimed else "🎁 未领取"
                    print(f"  {row.title} ({row.task_key}): {row.current_progress}/{row.target_progress} - {status} {claimed}")
            else:
                print("  暂无任务记录")

        except Exception as e:
            print(f"❌ 错误: {e}")
            import traceback
            traceback.print_exc()
            await session.rollback()


if __name__ == "__main__":
    print("=" * 50)
    print("🔄 用户任务重置工具")
    print("=" * 50)
    asyncio.run(reset_user_tasks())
    print("\n✨ 完成！")
