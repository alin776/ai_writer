"""add_is_featured_to_works

Revision ID: 882cdba7c8a1
Revises: 202e540d4993
Create Date: 2025-12-14 15:25:51.993245

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '882cdba7c8a1'
down_revision = '202e540d4993'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 添加 is_featured 字段到 works 表
    op.add_column('works', sa.Column('is_featured', sa.Boolean(), nullable=False, server_default='false', comment='是否为推荐作品(最多5本)'))
    op.create_index('ix_works_is_featured', 'works', ['is_featured'])


def downgrade() -> None:
    # 删除索引和字段
    op.drop_index('ix_works_is_featured', 'works')
    op.drop_column('works', 'is_featured')
