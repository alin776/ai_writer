"""add novel_chapter_vectors table for RAG writing context

Revision ID: 20251203_0001
Revises: 73195da690de
Create Date: 2025-12-03 00:01:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import pgvector.sqlalchemy

# revision identifiers, used by Alembic.
revision = '20251203_0001'
down_revision = '73195da690de'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 创建章节内容向量表
    op.create_table('novel_chapter_vectors',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('work_id', sa.UUID(), nullable=False),
        sa.Column('chapter_id', sa.UUID(), nullable=False),
        sa.Column('chapter_order', sa.Integer(), nullable=False),
        sa.Column('chapter_title', sa.String(length=255), nullable=False),
        sa.Column('chunk_index', sa.Integer(), nullable=False),
        sa.Column('chunk_text', sa.Text(), nullable=False),
        sa.Column('embedding', pgvector.sqlalchemy.vector.VECTOR(dim=384), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['chapter_id'], ['chapters.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['work_id'], ['works.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # 创建索引
    op.create_index('idx_chapter_vectors_work_id', 'novel_chapter_vectors', ['work_id'], unique=False)
    op.create_index('idx_chapter_vectors_chapter_id', 'novel_chapter_vectors', ['chapter_id'], unique=False)
    op.create_index('idx_chapter_vectors_chapter_order', 'novel_chapter_vectors', ['chapter_order'], unique=False)
    op.create_index('idx_chapter_vectors_work_order', 'novel_chapter_vectors', ['work_id', 'chapter_order'], unique=False)
    op.create_index('idx_chapter_vectors_chapter_chunks', 'novel_chapter_vectors', ['chapter_id', 'chunk_index'], unique=False)


def downgrade() -> None:
    # 删除索引
    op.drop_index('idx_chapter_vectors_chapter_chunks', table_name='novel_chapter_vectors')
    op.drop_index('idx_chapter_vectors_work_order', table_name='novel_chapter_vectors')
    op.drop_index('idx_chapter_vectors_chapter_order', table_name='novel_chapter_vectors')
    op.drop_index('idx_chapter_vectors_chapter_id', table_name='novel_chapter_vectors')
    op.drop_index('idx_chapter_vectors_work_id', table_name='novel_chapter_vectors')

    # 删除表
    op.drop_table('novel_chapter_vectors')
