"""add is_published to works

Revision ID: add_is_published_to_works
Revises: add_task_reward_system
Create Date: 2025-12-14 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_is_published_to_works'
down_revision = 'add_task_reward_system'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 添加 is_published 字段到 works 表
    op.add_column('works', sa.Column('is_published', sa.Boolean(), nullable=False, server_default='false', comment='是否发布到小说广场'))


def downgrade() -> None:
    # 删除 is_published 字段
    op.drop_column('works', 'is_published')
