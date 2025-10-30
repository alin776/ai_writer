"""sync all missing fields v2

Revision ID: d06bedc9ec51
Revises: add_missing_indexes
Create Date: 2025-10-29 14:10:50.743934

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd06bedc9ec51'
down_revision = 'add_missing_indexes'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 创建 enum 类型（如果不存在）
    op.execute("DO $$ BEGIN CREATE TYPE chapterstatus AS ENUM ('draft', 'published', 'archived'); EXCEPTION WHEN duplicate_object THEN null; END $$;")
    
    # 添加 chapters.status 字段
    op.add_column('chapters', sa.Column('status', postgresql.ENUM('draft', 'published', 'archived', name='chapterstatus', create_type=False), nullable=True))
    op.execute("UPDATE chapters SET status = 'draft' WHERE status IS NULL")
    op.alter_column('chapters', 'status', nullable=False)
    op.create_index(op.f('ix_chapters_status'), 'chapters', ['status'], unique=False)

    # 添加 novel_analysis_vectors 字段
    op.add_column('novel_analysis_vectors', sa.Column('user_id', sa.UUID(), nullable=True))
    op.add_column('novel_analysis_vectors', sa.Column('source_type', sa.String(length=50), nullable=True))
    op.add_column('novel_analysis_vectors', sa.Column('source_id', sa.UUID(), nullable=True))

    # 为现有数据设置默认值
    op.execute("UPDATE novel_analysis_vectors SET source_type = 'novel_analysis' WHERE source_type IS NULL")
    op.alter_column('novel_analysis_vectors', 'source_type', nullable=False)

    op.alter_column('novel_analysis_vectors', 'work_id',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('novel_analysis_vectors', 'chapter_id',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('novel_analysis_vectors', 'analysis_id',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('novel_analysis_vectors', 'micro_data',
               existing_type=postgresql.JSONB(astext_type=sa.Text()),
               nullable=True)
    op.create_index('idx_novel_vectors_source', 'novel_analysis_vectors', ['source_type', 'source_id'], unique=False)
    op.create_index('idx_novel_vectors_user_source', 'novel_analysis_vectors', ['user_id', 'source_type'], unique=False)
    op.create_index(op.f('ix_novel_analysis_vectors_source_id'), 'novel_analysis_vectors', ['source_id'], unique=False)
    op.create_index(op.f('ix_novel_analysis_vectors_source_type'), 'novel_analysis_vectors', ['source_type'], unique=False)
    op.create_index(op.f('ix_novel_analysis_vectors_user_id'), 'novel_analysis_vectors', ['user_id'], unique=False)
    op.create_foreign_key(None, 'novel_analysis_vectors', 'users', ['user_id'], ['id'], ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint(None, 'novel_analysis_vectors', type_='foreignkey')
    op.drop_index(op.f('ix_novel_analysis_vectors_user_id'), table_name='novel_analysis_vectors')
    op.drop_index(op.f('ix_novel_analysis_vectors_source_type'), table_name='novel_analysis_vectors')
    op.drop_index(op.f('ix_novel_analysis_vectors_source_id'), table_name='novel_analysis_vectors')
    op.drop_index('idx_novel_vectors_user_source', table_name='novel_analysis_vectors')
    op.drop_index('idx_novel_vectors_source', table_name='novel_analysis_vectors')
    op.alter_column('novel_analysis_vectors', 'micro_data',
               existing_type=postgresql.JSONB(astext_type=sa.Text()),
               nullable=False)
    op.alter_column('novel_analysis_vectors', 'analysis_id',
               existing_type=sa.UUID(),
               nullable=False)
    op.alter_column('novel_analysis_vectors', 'chapter_id',
               existing_type=sa.UUID(),
               nullable=False)
    op.alter_column('novel_analysis_vectors', 'work_id',
               existing_type=sa.UUID(),
               nullable=False)
    op.drop_column('novel_analysis_vectors', 'source_id')
    op.drop_column('novel_analysis_vectors', 'source_type')
    op.drop_column('novel_analysis_vectors', 'user_id')
    op.drop_index(op.f('ix_chapters_status'), table_name='chapters')
    op.drop_column('chapters', 'status')
