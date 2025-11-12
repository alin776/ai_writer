"""add humanize composite index

Revision ID: 20251112_0001
Revises: 20251026_0000
Create Date: 2025-11-12

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20251112_0001'
down_revision = '9ef580281a13'  # 修复：指向最新的迁移(20251102)
branch_labels = None
depends_on = None


def upgrade():
    """添加复合索引以优化历史查询性能"""
    # 创建复合索引 (user_id, created_at)
    op.create_index(
        'idx_humanize_user_created',
        'humanize_sessions',
        ['user_id', 'created_at'],
        unique=False
    )


def downgrade():
    """移除复合索引"""
    op.drop_index('idx_humanize_user_created', table_name='humanize_sessions')
