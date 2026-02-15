"""drop_review_tables

删除废弃的评审模块表：
- review_tasks（FK 指向 review_sessions + chapters）
- review_sessions

前端无任何引用，后端整个评审模块已删除。

Revision ID: drop_review_tables
Revises: drop_deprecated_chapter_tables
Create Date: 2026-02-15 15:00:00.000000
"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "drop_review_tables"
down_revision = "drop_deprecated_chapter_tables"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 先删子表（review_tasks FK → review_sessions + chapters）
    op.execute("DROP TABLE IF EXISTS review_tasks CASCADE")
    op.execute("DROP TABLE IF EXISTS review_sessions CASCADE")

    # 清理枚举类型
    op.execute("DROP TYPE IF EXISTS reviewlevel")
    op.execute("DROP TYPE IF EXISTS reviewtype")
    op.execute("DROP TYPE IF EXISTS taskpriority")
    op.execute("DROP TYPE IF EXISTS taskstatus")
    op.execute("DROP TYPE IF EXISTS tasksource")


def downgrade() -> None:
    # 用户确认不需要回退，downgrade 为 no-op
    pass
