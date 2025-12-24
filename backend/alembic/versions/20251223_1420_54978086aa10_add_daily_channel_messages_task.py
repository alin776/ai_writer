"""add_daily_channel_messages_task

Revision ID: 54978086aa10
Revises: 8b32e832859c
Create Date: 2025-12-23 14:20:41.266144

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '54978086aa10'
down_revision = '8b32e832859c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 添加每日频道发言任务
    op.execute("""
        INSERT INTO task_templates (id, task_key, title, description, icon, task_type, reward_credits, target_config, is_active, sort_order)
        VALUES
        (gen_random_uuid(), 'daily_channel_messages', '每日频道发言', '每天在频道中发送10条消息，活跃社区氛围', '💬', 'daily', 1000, '{"type": "channel_messages", "target": 10}', true, 4)
    """)


def downgrade() -> None:
    # 删除每日频道发言任务
    op.execute("""
        DELETE FROM task_templates WHERE task_key = 'daily_channel_messages'
    """)
