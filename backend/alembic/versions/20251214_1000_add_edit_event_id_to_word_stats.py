"""add_edit_event_id_to_chapter_word_stats

Revision ID: 20251214_1000
Revises: 0518fa576df4
Create Date: 2025-12-14 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20251214_1000'
down_revision = '0518fa576df4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. 添加 edit_event_id 字段
    op.add_column('chapter_word_stats',
        sa.Column('edit_event_id', sa.String(64), nullable=True)
    )

    # 2. 创建普通索引（用于查询优化）
    op.create_index(
        'ix_chapter_word_stats_edit_event_id',
        'chapter_word_stats',
        ['edit_event_id'],
        unique=False
    )

    # 3. 创建部分唯一索引（PostgreSQL）
    # 只对非 NULL 的 edit_event_id 进行唯一约束
    # 这样允许多条历史记录的 edit_event_id 为 NULL
    op.execute("""
        CREATE UNIQUE INDEX uq_chapter_word_stats_edit_event_id_partial
        ON chapter_word_stats (edit_event_id)
        WHERE edit_event_id IS NOT NULL
    """)

    # 4. 清理历史负数数据
    op.execute("DELETE FROM chapter_word_stats WHERE delta < 0")


def downgrade() -> None:
    # 1. 删除部分唯一索引
    op.execute("DROP INDEX IF EXISTS uq_chapter_word_stats_edit_event_id_partial")

    # 2. 删除普通索引
    op.drop_index('ix_chapter_word_stats_edit_event_id', table_name='chapter_word_stats')

    # 3. 删除字段
    op.drop_column('chapter_word_stats', 'edit_event_id')
