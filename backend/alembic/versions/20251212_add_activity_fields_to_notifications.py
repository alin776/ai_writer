"""add activity fields to notifications

Revision ID: add_activity_fields
Revises: 20251214_1000
Create Date: 2025-12-12 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'add_activity_fields'
down_revision = '20251214_1000'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """添加活动相关字段到通知表"""
    # 添加 activity_type 字段
    op.add_column('notifications', sa.Column('activity_type', sa.String(length=50), nullable=True))

    # 添加 activity_rules 字段（JSONB 类型，用于存储活动规则）
    op.add_column('notifications', sa.Column('activity_rules', postgresql.JSONB(astext_type=sa.Text()), nullable=True))


def downgrade() -> None:
    """回滚：删除活动相关字段"""
    op.drop_column('notifications', 'activity_rules')
    op.drop_column('notifications', 'activity_type')
