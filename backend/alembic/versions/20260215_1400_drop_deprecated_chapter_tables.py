"""drop_deprecated_chapter_tables

删除废弃的章节卫星表：
- chapter_word_stats
- chapter_content_indexes
- chapter_revisions
- chapter_histories
- novel_chapter_vectors
- opensearch_sync_statuses
- chapter_versions

Revision ID: drop_deprecated_chapter_tables
Revises: add_workgenre_new_values
Create Date: 2026-02-15 14:00:00.000000
"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "drop_deprecated_chapter_tables"
down_revision = "add_workgenre_new_values"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 先删子表（FK 指向 chapters），使用 CASCADE 处理依赖
    op.execute("DROP TABLE IF EXISTS chapter_word_stats CASCADE")
    op.execute("DROP TABLE IF EXISTS chapter_content_indexes CASCADE")
    op.execute("DROP TABLE IF EXISTS chapter_revisions CASCADE")
    op.execute("DROP TABLE IF EXISTS chapter_histories CASCADE")
    op.execute("DROP TABLE IF EXISTS novel_chapter_vectors CASCADE")
    op.execute("DROP TABLE IF EXISTS opensearch_sync_statuses CASCADE")
    op.execute("DROP TABLE IF EXISTS chapter_versions CASCADE")

    # 清理枚举类型
    op.execute("DROP TYPE IF EXISTS chapterrevisionstatus")
    op.execute("DROP TYPE IF EXISTS versiontype")
    op.execute("DROP TYPE IF EXISTS opensearchsyncstatusenum")


def downgrade() -> None:
    # 用户确认不需要回退，downgrade 为 no-op
    pass
