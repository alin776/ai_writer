"""add_comment_dislike

Revision ID: 20260103_0001
Revises: 20260101_0002
Create Date: 2026-01-03 00:01:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import uuid


# revision identifiers, used by Alembic.
revision = '20260103_0001'
down_revision = '20260101_0002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 在 comments 表添加 dislike_count 列
    op.add_column('comments', sa.Column('dislike_count', sa.Integer(), nullable=False, server_default='0'))

    # 创建 comment_dislikes 表
    op.create_table(
        'comment_dislikes',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True),
        sa.Column('comment_id', UUID(as_uuid=True), sa.ForeignKey('comments.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # 创建唯一索引：防止重复踩
    op.create_index('ix_comment_dislikes_comment_user', 'comment_dislikes', ['comment_id', 'user_id'], unique=True)


def downgrade() -> None:
    op.drop_index('ix_comment_dislikes_comment_user', table_name='comment_dislikes')
    op.drop_table('comment_dislikes')
    op.drop_column('comments', 'dislike_count')
