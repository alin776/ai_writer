"""add_message_reactions

Revision ID: 072013f12c3f
Revises: add_chapter_comments
Create Date: 2025-12-30 16:12:47.033768

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '072013f12c3f'
down_revision = 'add_chapter_comments'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 创建 message_reactions 表
    op.create_table(
        'message_reactions',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('message_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('emoji', sa.String(50), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),

        # 外键约束
        sa.ForeignKeyConstraint(['message_id'], ['channel_messages.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),

        # 唯一约束：每个用户对同一消息的同一 emoji 只能有一个反应
        sa.UniqueConstraint('message_id', 'user_id', 'emoji', name='uq_message_user_emoji'),
    )

    # 创建索引
    op.create_index('idx_reactions_message_id', 'message_reactions', ['message_id'])
    op.create_index('idx_reactions_user_id', 'message_reactions', ['user_id'])
    op.create_index('idx_reactions_message_emoji', 'message_reactions', ['message_id', 'emoji'])


def downgrade() -> None:
    # 删除索引
    op.drop_index('idx_reactions_message_emoji', table_name='message_reactions')
    op.drop_index('idx_reactions_user_id', table_name='message_reactions')
    op.drop_index('idx_reactions_message_id', table_name='message_reactions')

    # 删除表
    op.drop_table('message_reactions')
