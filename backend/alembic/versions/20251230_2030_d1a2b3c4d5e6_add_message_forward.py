"""add_message_forward

Revision ID: d1a2b3c4d5e6
Revises: c9f8e1234567
Create Date: 2025-12-30 20:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision = 'd1a2b3c4d5e6'
down_revision = 'c9f8e1234567'
branch_labels = None
depends_on = None


def column_exists(table_name: str, column_name: str) -> bool:
    """检查列是否存在"""
    bind = op.get_bind()
    inspector = inspect(bind)
    columns = inspector.get_columns(table_name)
    return any(col['name'] == column_name for col in columns)


def index_exists(table_name: str, index_name: str) -> bool:
    """检查索引是否存在"""
    bind = op.get_bind()
    inspector = inspect(bind)
    indexes = inspector.get_indexes(table_name)
    return any(idx['name'] == index_name for idx in indexes)


def upgrade() -> None:
    # 添加转发来源消息ID字段（如果不存在）
    if not column_exists('channel_messages', 'forwarded_from_id'):
        op.add_column('channel_messages', sa.Column(
            'forwarded_from_id',
            postgresql.UUID(as_uuid=True),
            nullable=True,
            comment='转发来源消息ID'
        ))

        # 添加外键约束
        op.create_foreign_key(
            'fk_channel_messages_forwarded_from',
            'channel_messages', 'channel_messages',
            ['forwarded_from_id'], ['id'],
            ondelete='SET NULL'
        )

        # 添加索引
        op.create_index('idx_messages_forwarded_from', 'channel_messages', ['forwarded_from_id'])


def downgrade() -> None:
    op.drop_index('idx_messages_forwarded_from', table_name='channel_messages')
    op.drop_constraint('fk_channel_messages_forwarded_from', 'channel_messages', type_='foreignkey')
    op.drop_column('channel_messages', 'forwarded_from_id')
