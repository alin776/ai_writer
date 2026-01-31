"""创建任务表"""
import asyncio
from sqlalchemy import text
from app.core.database import engine

async def create_tables():
    async with engine.begin() as conn:
        # 删除旧表
        await conn.execute(text("DROP TABLE IF EXISTS tasks CASCADE"))

        # 创建任务模板表
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS task_templates (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                task_key VARCHAR(50) UNIQUE NOT NULL,
                title VARCHAR(100) NOT NULL,
                description TEXT,
                icon VARCHAR(50),
                task_type VARCHAR(20) NOT NULL DEFAULT 'once',
                reward_credits INTEGER NOT NULL DEFAULT 0,
                target_config TEXT,
                is_active BOOLEAN NOT NULL DEFAULT true,
                sort_order INTEGER NOT NULL DEFAULT 0,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
            )
        """))

        # 创建用户任务表
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS user_tasks (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                template_id UUID NOT NULL REFERENCES task_templates(id) ON DELETE CASCADE,
                current_progress INTEGER NOT NULL DEFAULT 0,
                target_progress INTEGER NOT NULL DEFAULT 1,
                is_completed BOOLEAN NOT NULL DEFAULT false,
                completed_at TIMESTAMP WITH TIME ZONE,
                is_claimed BOOLEAN NOT NULL DEFAULT false,
                claimed_at TIMESTAMP WITH TIME ZONE,
                claimed_credits INTEGER NOT NULL DEFAULT 0,
                reset_date TIMESTAMP WITH TIME ZONE,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
            )
        """))

        # 创建索引
        await conn.execute(text("CREATE INDEX IF NOT EXISTS ix_task_templates_id ON task_templates(id)"))
        await conn.execute(text("CREATE INDEX IF NOT EXISTS ix_task_templates_task_key ON task_templates(task_key)"))
        await conn.execute(text("CREATE INDEX IF NOT EXISTS ix_user_tasks_id ON user_tasks(id)"))
        await conn.execute(text("CREATE INDEX IF NOT EXISTS ix_user_tasks_user_id ON user_tasks(user_id)"))
        await conn.execute(text("CREATE INDEX IF NOT EXISTS ix_user_tasks_template_id ON user_tasks(template_id)"))

        # 初始化默认任务模板
        await conn.execute(text("""
            INSERT INTO task_templates (id, task_key, title, description, icon, task_type, reward_credits, target_config, is_active, sort_order)
            VALUES
            (gen_random_uuid(), 'daily_write_1000', '每日写作1000字', '每天完成1000字的创作，获得积分奖励', 'edit', 'daily', 500, '{"type": "write_words", "target": 1000}', true, 1),
            (gen_random_uuid(), 'set_avatar', '设置头像', '上传个人头像，完善个人资料', 'image', 'once', 500, '{"type": "set_avatar"}', true, 2),
            (gen_random_uuid(), 'change_username', '修改用户名', '设置个性化的用户名', 'user', 'once', 500, '{"type": "change_username"}', true, 3)
            ON CONFLICT (task_key) DO NOTHING
        """))

        print("Task tables created successfully!")

if __name__ == "__main__":
    asyncio.run(create_tables())
