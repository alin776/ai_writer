migration_content = """\"\"\"add_channel_tables

Revision ID: 2875c8bb72fb
Revises: add_favorite_count_to_works
Create Date: 2025-12-21 00:39:41.401683

\"\"\"
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '2875c8bb72fb'
down_revision = 'add_favorite_count_to_works'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create channels table
    op.create_table(
        'channels',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('cover_image', sa.String(500), nullable=True),
        sa.Column('type', sa.Enum('official', 'fangroup', 'work', name='channeltype'), nullable=False),
        sa.Column('status', sa.Enum('active', 'warning', 'locked', name='channelstatus'), nullable=False, server_default='active'),
        sa.Column('creator_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('work_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('is_permanent', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('is_pinned', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('member_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('message_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('last_message_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('warning_days', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('locked_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['creator_id'], ['users.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['work_id'], ['works.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_channels_id', 'channels', ['id'])
    op.create_index('ix_channels_name', 'channels', ['name'])
    op.create_index('ix_channels_type', 'channels', ['type'])
    op.create_index('ix_channels_creator_id', 'channels', ['creator_id'])
    op.create_index('ix_channels_work_id', 'channels', ['work_id'])

    # Create channel_members table
    op.create_table(
        'channel_members',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('channel_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('role', sa.Enum('owner', 'admin', 'member', name='memberrole'), nullable=False, server_default='member'),
        sa.Column('is_muted', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('is_banned', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('custom_title', sa.String(50), nullable=True),
        sa.Column('title_color', sa.String(20), nullable=True),
        sa.Column('joined_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('last_read_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['channel_id'], ['channels.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('channel_id', 'user_id', name='uix_channel_user')
    )
    op.create_index('ix_channel_members_id', 'channel_members', ['id'])
    op.create_index('ix_channel_members_channel_id', 'channel_members', ['channel_id'])
    op.create_index('ix_channel_members_user_id', 'channel_members', ['user_id'])

    # Create channel_messages table
    op.create_table(
        'channel_messages',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('channel_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('type', sa.Enum('normal', 'announcement', 'mention', name='messagetype'), nullable=False, server_default='normal'),
        sa.Column('is_pinned', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('reply_to_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('reaction_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['channel_id'], ['channels.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['reply_to_id'], ['channel_messages.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_channel_messages_id', 'channel_messages', ['id'])
    op.create_index('ix_channel_messages_channel_id', 'channel_messages', ['channel_id'])
    op.create_index('ix_channel_messages_user_id', 'channel_messages', ['user_id'])
    op.create_index('ix_channel_messages_created_at', 'channel_messages', ['created_at'])


def downgrade() -> None:
    op.drop_index('ix_channel_messages_created_at', 'channel_messages')
    op.drop_index('ix_channel_messages_user_id', 'channel_messages')
    op.drop_index('ix_channel_messages_channel_id', 'channel_messages')
    op.drop_index('ix_channel_messages_id', 'channel_messages')
    op.drop_table('channel_messages')

    op.drop_index('ix_channel_members_user_id', 'channel_members')
    op.drop_index('ix_channel_members_channel_id', 'channel_members')
    op.drop_index('ix_channel_members_id', 'channel_members')
    op.drop_table('channel_members')

    op.drop_index('ix_channels_work_id', 'channels')
    op.drop_index('ix_channels_creator_id', 'channels')
    op.drop_index('ix_channels_type', 'channels')
    op.drop_index('ix_channels_name', 'channels')
    op.drop_index('ix_channels_id', 'channels')
    op.drop_table('channels')

    op.execute('DROP TYPE IF EXISTS messagetype')
    op.execute('DROP TYPE IF EXISTS memberrole')
    op.execute('DROP TYPE IF EXISTS channelstatus')
    op.execute('DROP TYPE IF EXISTS channeltype')
"""

with open('alembic/versions/20251221_0039_2875c8bb72fb_add_channel_tables.py', 'w', encoding='utf-8') as f:
    f.write(migration_content)
print("Migration file updated successfully!")
