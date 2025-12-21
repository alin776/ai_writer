"""add_channel_read_states_and_mentions

Revision ID: 301f8cfd9d0c
Revises: 46e9f9fbc803
Create Date: 2025-12-21 13:13:09.228340

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '301f8cfd9d0c'
down_revision = '46e9f9fbc803'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 创建频道已读状态表
    op.create_table(
        'channel_read_states',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('channel_id', sa.UUID(), nullable=False),
        sa.Column('last_read_message_id', sa.UUID(), nullable=True),
        sa.Column('unread_count', sa.Integer(), nullable=False, server_default='0', comment='未读消息数'),
        sa.Column('mention_count', sa.Integer(), nullable=False, server_default='0', comment='@我的消息数'),
        sa.Column('last_read_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['channel_id'], ['channels.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['last_read_message_id'], ['channel_messages.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
    )

    # 创建复合唯一索引
    op.create_index('idx_user_channel', 'channel_read_states', ['user_id', 'channel_id'], unique=True)


def downgrade() -> None:
    op.drop_index('idx_user_channel', table_name='channel_read_states')
    op.drop_table('channel_read_states')
