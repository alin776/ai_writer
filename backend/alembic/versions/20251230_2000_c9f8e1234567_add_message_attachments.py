"""add_message_attachments

Revision ID: c9f8e1234567
Revises: bb20c0984de1
Create Date: 2025-12-30 20:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision = 'c9f8e1234567'
down_revision = 'bb20c0984de1'
branch_labels = None
depends_on = None


def table_exists(table_name: str) -> bool:
    """检查表是否存在"""
    bind = op.get_bind()
    inspector = inspect(bind)
    return table_name in inspector.get_table_names()


def index_exists(table_name: str, index_name: str) -> bool:
    """检查索引是否存在"""
    bind = op.get_bind()
    inspector = inspect(bind)
    indexes = inspector.get_indexes(table_name)
    return any(idx['name'] == index_name for idx in indexes)


def upgrade() -> None:
    # 创建 message_attachments 表（如果不存在）
    if not table_exists('message_attachments'):
        op.create_table(
            'message_attachments',
            sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
            sa.Column('message_id', postgresql.UUID(as_uuid=True), nullable=True),
            sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
            sa.Column('channel_id', postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column('file_name', sa.String(255), nullable=False, comment='原始文件名'),
            sa.Column('file_type', sa.String(100), nullable=False, comment='MIME类型'),
            sa.Column('file_size', sa.Integer, nullable=False, comment='文件大小(字节)'),
            sa.Column('file_url', sa.String(500), nullable=False, comment='COS存储URL'),
            sa.Column('thumbnail_url', sa.String(500), nullable=True, comment='缩略图URL(图片)'),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),

            # 外键约束
            sa.ForeignKeyConstraint(['message_id'], ['channel_messages.id'], ondelete='CASCADE'),
            sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL'),
            sa.ForeignKeyConstraint(['channel_id'], ['channels.id'], ondelete='CASCADE'),
        )

        # 创建索引
        op.create_index('idx_attachments_message_id', 'message_attachments', ['message_id'])
        op.create_index('idx_attachments_user_id', 'message_attachments', ['user_id'])
        op.create_index('idx_attachments_channel_id', 'message_attachments', ['channel_id'])


def downgrade() -> None:
    # 删除索引
    op.drop_index('idx_attachments_channel_id', table_name='message_attachments')
    op.drop_index('idx_attachments_user_id', table_name='message_attachments')
    op.drop_index('idx_attachments_message_id', table_name='message_attachments')

    # 删除表
    op.drop_table('message_attachments')
