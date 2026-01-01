"""add_friend_system

Revision ID: 20260101_0001
Revises: a1b2c3d4e5f6
Create Date: 2026-01-01 00:01:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = '20260101_0001'
down_revision = 'a1b2c3d4e5f6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. 添加 'private' 到 channeltype 枚举
    op.execute("ALTER TYPE channeltype ADD VALUE IF NOT EXISTS 'private'")

    # 2. 创建 friendships 表
    op.create_table(
        'friendships',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('friend_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('private_channel_id', UUID(as_uuid=True), sa.ForeignKey('channels.id', ondelete='SET NULL'), nullable=True, index=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # 创建唯一约束和检查约束
    op.create_unique_constraint('uq_friendship', 'friendships', ['user_id', 'friend_id'])
    op.execute("ALTER TABLE friendships ADD CONSTRAINT ck_not_self_friend CHECK (user_id != friend_id)")

    # 3. 创建 friend_requests 表
    op.create_table(
        'friend_requests',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('from_user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('to_user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('message', sa.String(200), nullable=True, comment='请求消息'),
        sa.Column('status', sa.String(20), nullable=False, default='pending', index=True, comment='状态: pending/accepted/rejected'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )

    # 创建唯一约束和检查约束
    op.create_unique_constraint('uq_friend_request', 'friend_requests', ['from_user_id', 'to_user_id'])
    op.execute("ALTER TABLE friend_requests ADD CONSTRAINT ck_not_self_request CHECK (from_user_id != to_user_id)")
    op.execute("ALTER TABLE friend_requests ADD CONSTRAINT ck_valid_status CHECK (status IN ('pending', 'accepted', 'rejected'))")

    # 创建索引：便于查询某用户收到的待处理请求
    op.create_index('ix_friend_requests_to_user_status', 'friend_requests', ['to_user_id', 'status'])


def downgrade() -> None:
    op.drop_index('ix_friend_requests_to_user_status', table_name='friend_requests')
    op.execute("ALTER TABLE friend_requests DROP CONSTRAINT IF EXISTS ck_valid_status")
    op.execute("ALTER TABLE friend_requests DROP CONSTRAINT IF EXISTS ck_not_self_request")
    op.drop_constraint('uq_friend_request', 'friend_requests', type_='unique')
    op.drop_table('friend_requests')

    op.execute("ALTER TABLE friendships DROP CONSTRAINT IF EXISTS ck_not_self_friend")
    op.drop_constraint('uq_friendship', 'friendships', type_='unique')
    op.drop_table('friendships')

    # 注意：PostgreSQL 不支持从枚举中移除值，所以 'private' 将保留
