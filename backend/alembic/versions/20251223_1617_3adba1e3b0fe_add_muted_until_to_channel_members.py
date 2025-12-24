"""add_muted_until_to_channel_members

Revision ID: 3adba1e3b0fe
Revises: 5e2ae31dbc87
Create Date: 2025-12-23 16:17:52.838051

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3adba1e3b0fe'
down_revision = '5e2ae31dbc87'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 添加禁言到期时间字段
    op.add_column('channel_members', sa.Column('muted_until', sa.DateTime(timezone=True), nullable=True, comment='禁言到期时间'))


def downgrade() -> None:
    # 删除禁言到期时间字段
    op.drop_column('channel_members', 'muted_until')
