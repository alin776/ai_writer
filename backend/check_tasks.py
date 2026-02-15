"""检查任务模板是否存在"""
import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

async def check_tasks():
    # 从环境变量获取数据库连接信息
    database_url = os.getenv('DATABASE_URL', '')

    # 将 SQLAlchemy 格式转换为 asyncpg 格式
    # postgresql+asyncpg://user:pass@host:port/dbname -> postgresql://user:pass@host:port/dbname
    database_url = database_url.replace('postgresql+asyncpg://', 'postgresql://')

    print(f"连接数据库: {database_url.split('@')[1] if '@' in database_url else '...'}")

    try:
        conn = await asyncpg.connect(database_url)

        # 检查 task_templates 表是否存在
        table_exists = await conn.fetchval("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_name = 'task_templates'
            )
        """)

        print(f"\ntask_templates 表是否存在: {table_exists}")

        if table_exists:
            # 查询任务模板
            rows = await conn.fetch("""
                SELECT id, task_key, title, description, task_type, reward_credits, is_active, sort_order
                FROM task_templates
                ORDER BY sort_order
            """)

            print(f"\n找到 {len(rows)} 个任务模板:\n")
            for row in rows:
                print(f"- [{row['task_key']}] {row['title']}")
                print(f"  描述: {row['description']}")
                print(f"  类型: {row['task_type']}, 奖励: {row['reward_credits']} 积分")
                print(f"  激活状态: {row['is_active']}, 排序: {row['sort_order']}")
                print()
        else:
            print("\n❌ task_templates 表不存在!")
            print("需要运行数据库迁移: alembic upgrade head")

        await conn.close()

    except Exception as e:
        print(f"\n❌ 错误: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(check_tasks())
