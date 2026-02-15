"""add task reward system

Revision ID: add_task_reward_system
Revises: 00e8e68c3c88
Create Date: 2025-12-13 20:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'add_task_reward_system'
down_revision = '00e8e68c3c88'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 删除旧的 tasks 表（如果存在）
    op.execute('DROP TABLE IF EXISTS tasks CASCADE')

    # 创建任务模板表
    op.create_table(
        'task_templates',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('task_key', sa.String(50), unique=True, nullable=False, index=True),
        sa.Column('title', sa.String(100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('icon', sa.String(50), nullable=True),
        sa.Column('task_type', sa.String(20), nullable=False, server_default='once'),
        sa.Column('reward_credits', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('target_config', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('sort_order', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # 创建用户任务表
    op.create_table(
        'user_tasks',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column('template_id', postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column('current_progress', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('target_progress', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('is_completed', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('is_claimed', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('claimed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('claimed_credits', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('reset_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['template_id'], ['task_templates.id'], ondelete='CASCADE'),
    )

    # 创建索引
    op.create_index('ix_task_templates_id', 'task_templates', ['id'])
    op.create_index('ix_user_tasks_id', 'user_tasks', ['id'])

    # 初始化默认任务模板
    op.execute("""
        INSERT INTO task_templates (id, task_key, title, description, icon, task_type, reward_credits, target_config, is_active, sort_order)
        VALUES
        (gen_random_uuid(), 'daily_write_1000', '每日写作1000字', '每天完成1000字的创作，获得积分奖励', '✍️', 'daily', 500, '{"type": "write_words", "target": 1000}', true, 1),
        (gen_random_uuid(), 'set_avatar', '设置头像', '上传个人头像，完善个人资料', '🖼️', 'once', 500, '{"type": "set_avatar"}', true, 2),
        (gen_random_uuid(), 'change_username', '修改用户名', '设置个性化的用户名', '✨', 'once', 500, '{"type": "change_username"}', true, 3)
    """)


def downgrade() -> None:
    op.drop_index('ix_user_tasks_id', 'user_tasks')
    op.drop_index('ix_task_templates_id', 'task_templates')
    op.drop_table('user_tasks')
    op.drop_table('task_templates')
