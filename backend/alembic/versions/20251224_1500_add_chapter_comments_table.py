"""add chapter comments table

Revision ID: add_chapter_comments
Revises: 111d2e46d4bc
Create Date: 2024-12-24 15:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'add_chapter_comments'
down_revision = '111d2e46d4bc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 创建评论位置类型枚举（如果不存在）
    op.execute("""
        DO $$ BEGIN
            CREATE TYPE commentlocationtype AS ENUM ('chapter', 'paragraph', 'sentence');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
    """)

    # 创建举报原因枚举（如果不存在）
    op.execute("""
        DO $$ BEGIN
            CREATE TYPE chaptercommentreportreason AS ENUM ('spam', 'abuse', 'porn', 'illegal', 'false', 'other');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
    """)

    # 创建章节评论表
    op.create_table('chapter_comments',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('chapter_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('location_type', postgresql.ENUM('chapter', 'paragraph', 'sentence', name='commentlocationtype', create_type=False), nullable=False, server_default='chapter'),
        sa.Column('paragraph_index', sa.Integer(), nullable=True, comment='段落索引 (0-based)'),
        sa.Column('sentence_index', sa.Integer(), nullable=True, comment='句子索引 (段落内, 0-based)'),
        sa.Column('quoted_text', sa.Text(), nullable=True, comment='被引用的原文片段'),
        sa.Column('content', sa.Text(), nullable=False, comment='评论内容'),
        sa.Column('parent_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('reply_to_user_id', postgresql.UUID(as_uuid=True), nullable=True, comment='回复目标用户ID'),
        sa.Column('like_count', sa.Integer(), nullable=True, server_default='0', comment='点赞数'),
        sa.Column('is_deleted', sa.Boolean(), nullable=True, server_default='false', comment='是否已删除'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['chapter_id'], ['chapters.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['parent_id'], ['chapter_comments.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['reply_to_user_id'], ['users.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_chapter_comments_chapter_id'), 'chapter_comments', ['chapter_id'], unique=False)
    op.create_index(op.f('ix_chapter_comments_id'), 'chapter_comments', ['id'], unique=False)
    op.create_index(op.f('ix_chapter_comments_parent_id'), 'chapter_comments', ['parent_id'], unique=False)
    op.create_index(op.f('ix_chapter_comments_user_id'), 'chapter_comments', ['user_id'], unique=False)

    # 创建章节评论点赞表
    op.create_table('chapter_comment_likes',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('comment_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['comment_id'], ['chapter_comments.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('comment_id', 'user_id', name='uq_chapter_comment_like')
    )
    op.create_index(op.f('ix_chapter_comment_likes_comment_id'), 'chapter_comment_likes', ['comment_id'], unique=False)
    op.create_index(op.f('ix_chapter_comment_likes_id'), 'chapter_comment_likes', ['id'], unique=False)
    op.create_index(op.f('ix_chapter_comment_likes_user_id'), 'chapter_comment_likes', ['user_id'], unique=False)

    # 创建章节评论举报表
    op.create_table('chapter_comment_reports',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('comment_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('reason', postgresql.ENUM('spam', 'abuse', 'porn', 'illegal', 'false', 'other', name='chaptercommentreportreason', create_type=False), nullable=False, comment='举报原因'),
        sa.Column('description', sa.Text(), nullable=True, comment='详细描述'),
        sa.Column('is_processed', sa.Boolean(), nullable=True, server_default='false', comment='是否已处理'),
        sa.Column('processed_at', sa.DateTime(timezone=True), nullable=True, comment='处理时间'),
        sa.Column('processed_by', postgresql.UUID(as_uuid=True), nullable=True, comment='处理人'),
        sa.Column('admin_note', sa.Text(), nullable=True, comment='管理员备注'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['comment_id'], ['chapter_comments.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['processed_by'], ['users.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('comment_id', 'user_id', name='uq_chapter_comment_report')
    )
    op.create_index(op.f('ix_chapter_comment_reports_comment_id'), 'chapter_comment_reports', ['comment_id'], unique=False)
    op.create_index(op.f('ix_chapter_comment_reports_id'), 'chapter_comment_reports', ['id'], unique=False)
    op.create_index(op.f('ix_chapter_comment_reports_user_id'), 'chapter_comment_reports', ['user_id'], unique=False)


def downgrade() -> None:
    # 删除章节评论举报表
    op.drop_index(op.f('ix_chapter_comment_reports_user_id'), table_name='chapter_comment_reports')
    op.drop_index(op.f('ix_chapter_comment_reports_id'), table_name='chapter_comment_reports')
    op.drop_index(op.f('ix_chapter_comment_reports_comment_id'), table_name='chapter_comment_reports')
    op.drop_table('chapter_comment_reports')

    # 删除章节评论点赞表
    op.drop_index(op.f('ix_chapter_comment_likes_user_id'), table_name='chapter_comment_likes')
    op.drop_index(op.f('ix_chapter_comment_likes_id'), table_name='chapter_comment_likes')
    op.drop_index(op.f('ix_chapter_comment_likes_comment_id'), table_name='chapter_comment_likes')
    op.drop_table('chapter_comment_likes')

    # 删除章节评论表
    op.drop_index(op.f('ix_chapter_comments_user_id'), table_name='chapter_comments')
    op.drop_index(op.f('ix_chapter_comments_parent_id'), table_name='chapter_comments')
    op.drop_index(op.f('ix_chapter_comments_id'), table_name='chapter_comments')
    op.drop_index(op.f('ix_chapter_comments_chapter_id'), table_name='chapter_comments')
    op.drop_table('chapter_comments')

    # 删除枚举类型
    op.execute('DROP TYPE IF EXISTS chaptercommentreportreason')
    op.execute('DROP TYPE IF EXISTS commentlocationtype')
