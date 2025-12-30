"""add_channel_features

Revision ID: e2f3g4h5i6j7
Revises: d1a2b3c4d5e6
Create Date: 2025-12-30 21:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy import inspect


revision = 'e2f3g4h5i6j7'
down_revision = 'd1a2b3c4d5e6'
branch_labels = None
depends_on = None


def table_exists(table_name: str) -> bool:
    """检查表是否存在"""
    bind = op.get_bind()
    inspector = inspect(bind)
    return table_name in inspector.get_table_names()


def column_exists(table_name: str, column_name: str) -> bool:
    """检查列是否存在"""
    bind = op.get_bind()
    inspector = inspect(bind)
    columns = inspector.get_columns(table_name)
    return any(col['name'] == column_name for col in columns)


def upgrade() -> None:
    # 1. 频道邀请链接表（如果不存在）
    if not table_exists('channel_invites'):
        op.create_table(
            'channel_invites',
            sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
            sa.Column('channel_id', postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column('creator_id', postgresql.UUID(as_uuid=True), nullable=True),
            sa.Column('code', sa.String(20), unique=True, nullable=False),
            sa.Column('max_uses', sa.Integer, nullable=True, comment='最大使用次数'),
            sa.Column('use_count', sa.Integer, default=0, nullable=False),
            sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
            sa.Column('is_active', sa.Boolean, default=True, nullable=False),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
            sa.ForeignKeyConstraint(['channel_id'], ['channels.id'], ondelete='CASCADE'),
            sa.ForeignKeyConstraint(['creator_id'], ['users.id'], ondelete='SET NULL'),
        )
        op.create_index('idx_invites_channel_id', 'channel_invites', ['channel_id'])
        op.create_index('idx_invites_code', 'channel_invites', ['code'])

    # 2. 消息书签表（如果不存在）
    if not table_exists('message_bookmarks'):
        op.create_table(
            'message_bookmarks',
            sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
            sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column('message_id', postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column('channel_id', postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column('note', sa.String(500), nullable=True, comment='书签备注'),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
            sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
            sa.ForeignKeyConstraint(['message_id'], ['channel_messages.id'], ondelete='CASCADE'),
            sa.ForeignKeyConstraint(['channel_id'], ['channels.id'], ondelete='CASCADE'),
            sa.UniqueConstraint('user_id', 'message_id', name='uq_user_message_bookmark'),
        )
        op.create_index('idx_bookmarks_user_id', 'message_bookmarks', ['user_id'])
        op.create_index('idx_bookmarks_message_id', 'message_bookmarks', ['message_id'])

    # 3. 频道慢速模式字段（如果不存在）
    if not column_exists('channels', 'slowmode_interval'):
        op.add_column('channels', sa.Column(
            'slowmode_interval',
            sa.Integer,
            nullable=True,
            comment='慢速模式间隔(秒)，null表示关闭'
        ))

    # 4. 频道通知设置表（如果不存在）
    if not table_exists('channel_notification_settings'):
        op.create_table(
            'channel_notification_settings',
            sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
            sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column('channel_id', postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column('is_muted', sa.Boolean, default=False, nullable=False, comment='是否静音'),
            sa.Column('mute_until', sa.DateTime(timezone=True), nullable=True, comment='静音到期时间'),
            sa.Column('notify_mentions', sa.Boolean, default=True, nullable=False, comment='是否通知@提醒'),
            sa.Column('notify_announcements', sa.Boolean, default=True, nullable=False, comment='是否通知公告'),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
            sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
            sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
            sa.ForeignKeyConstraint(['channel_id'], ['channels.id'], ondelete='CASCADE'),
            sa.UniqueConstraint('user_id', 'channel_id', name='uq_user_channel_notification'),
        )
        op.create_index('idx_notification_settings_user', 'channel_notification_settings', ['user_id'])
        op.create_index('idx_notification_settings_channel', 'channel_notification_settings', ['channel_id'])


def downgrade() -> None:
    op.drop_index('idx_notification_settings_channel', table_name='channel_notification_settings')
    op.drop_index('idx_notification_settings_user', table_name='channel_notification_settings')
    op.drop_table('channel_notification_settings')

    op.drop_column('channels', 'slowmode_interval')

    op.drop_index('idx_bookmarks_message_id', table_name='message_bookmarks')
    op.drop_index('idx_bookmarks_user_id', table_name='message_bookmarks')
    op.drop_table('message_bookmarks')

    op.drop_index('idx_invites_code', table_name='channel_invites')
    op.drop_index('idx_invites_channel_id', table_name='channel_invites')
    op.drop_table('channel_invites')
