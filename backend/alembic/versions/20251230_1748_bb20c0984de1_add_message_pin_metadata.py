"""add_message_pin_metadata

Revision ID: bb20c0984de1
Revises: a13de1c3fbb5
Create Date: 2025-12-30 17:48:20.985556

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bb20c0984de1'
down_revision = 'a13de1c3fbb5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 添加置顶时间字段
    op.add_column('channel_messages', sa.Column('pinned_at', sa.DateTime(timezone=True), nullable=True, comment='置顶时间'))
    # 添加置顶操作人字段
    op.add_column('channel_messages', sa.Column('pinned_by', sa.UUID(), nullable=True, comment='置顶操作人'))
    # 添加外键约束
    op.create_foreign_key(
        'fk_channel_messages_pinned_by_users',
        'channel_messages', 'users',
        ['pinned_by'], ['id'],
        ondelete='SET NULL'
    )


def downgrade() -> None:
    op.drop_constraint('fk_channel_messages_pinned_by_users', 'channel_messages', type_='foreignkey')
    op.drop_column('channel_messages', 'pinned_by')
    op.drop_column('channel_messages', 'pinned_at')
