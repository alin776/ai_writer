"""add_comment_system

Revision ID: 48bc19c8cb14
Revises: add_is_published_to_works
Create Date: 2025-12-14 15:10:30.027260

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '48bc19c8cb14'
down_revision = 'add_is_published_to_works'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 创建评论表
    op.create_table(
        'comments',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('work_id', postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('parent_id', postgresql.UUID(as_uuid=True), nullable=True, index=True),
        sa.Column('reply_to_user_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('like_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['work_id'], ['works.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['parent_id'], ['comments.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['reply_to_user_id'], ['users.id'], ondelete='SET NULL'),
    )
    op.create_index('ix_comments_id', 'comments', ['id'])

    # 创建评论点赞表
    op.create_table(
        'comment_likes',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('comment_id', postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['comment_id'], ['comments.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    )
    op.create_index('ix_comment_likes_id', 'comment_likes', ['id'])

    # 创建联合唯一索引，防止用户重复点赞同一条评论
    op.create_index(
        'ix_comment_likes_unique',
        'comment_likes',
        ['comment_id', 'user_id'],
        unique=True
    )


def downgrade() -> None:
    op.drop_index('ix_comment_likes_unique', 'comment_likes')
    op.drop_index('ix_comment_likes_id', 'comment_likes')
    op.drop_table('comment_likes')
    op.drop_index('ix_comments_id', 'comments')
    op.drop_table('comments')
