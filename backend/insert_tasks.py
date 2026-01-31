import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

async def insert_tasks():
    database_url = os.getenv('DATABASE_URL', '').replace('postgresql+asyncpg://', 'postgresql://')
    
    conn = await asyncpg.connect(database_url)
    
    # 插入三个默认任务模板
    await conn.execute("""
        INSERT INTO task_templates (id, task_key, title, description, icon, task_type, reward_credits, target_config, is_active, sort_order, created_at, updated_at)
        VALUES
        (gen_random_uuid(), 'daily_write_1000', '每日写作1000字', '每天完成1000字的创作，获得积分奖励', '✍️', 'daily', 500, '{"type": "write_words", "target": 1000}', true, 1, NOW(), NOW()),
        (gen_random_uuid(), 'set_avatar', '设置头像', '上传个人头像，完善个人资料', '🖼️', 'once', 500, '{"type": "set_avatar"}', true, 2, NOW(), NOW()),
        (gen_random_uuid(), 'change_username', '修改用户名', '设置个性化的用户名', '✨', 'once', 500, '{"type": "change_username"}', true, 3, NOW(), NOW())
        ON CONFLICT (task_key) DO NOTHING
    """)
    
    # 查询确认
    rows = await conn.fetch("SELECT task_key, title FROM task_templates ORDER BY sort_order")
    
    print(f"✓ 成功插入任务模板，共 {len(rows)} 个:")
    for row in rows:
        print(f"  - [{row['task_key']}] {row['title']}")
    
    await conn.close()

if __name__ == "__main__":
    asyncio.run(insert_tasks())
