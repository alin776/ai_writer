"""add_online_status_to_users

Revision ID: b6d2d534d191
Revises: 20260103_0001
Create Date: 2026-01-03 12:34:58.146648

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'b6d2d534d191'
down_revision = '20260103_0001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 添加用户在线状态字段
    op.add_column('users', sa.Column('online_status', sa.String(length=20), nullable=False, server_default='online'))


def downgrade() -> None:
    # 移除用户在线状态字段
    op.drop_column('users', 'online_status')
