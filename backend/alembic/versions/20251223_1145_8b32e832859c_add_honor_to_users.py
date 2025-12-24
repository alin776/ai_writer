"""add_honor_to_users

Revision ID: 8b32e832859c
Revises: 301f8cfd9d0c
Create Date: 2025-12-23 11:45:29.637750

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8b32e832859c'
down_revision = '301f8cfd9d0c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 添加 honor 字段到 users 表
    op.add_column('users', sa.Column('honor', sa.String(length=50), nullable=True))


def downgrade() -> None:
    # 移除 honor 字段
    op.drop_column('users', 'honor')
