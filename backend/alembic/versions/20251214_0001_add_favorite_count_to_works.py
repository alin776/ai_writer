"""add favorite_count to works

Revision ID: add_favorite_count_to_works
Revises: c9f4976bae60
Create Date: 2025-12-14 00:01:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_favorite_count_to_works'
down_revision = 'c9f4976bae60'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 添加 favorite_count 字段到 works 表
    op.add_column('works', sa.Column('favorite_count', sa.Integer(), nullable=False, server_default='0', comment='收藏数'))


def downgrade() -> None:
    # 删除 favorite_count 字段
    op.drop_column('works', 'favorite_count')
