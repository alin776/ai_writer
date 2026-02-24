"""chapter_comments_use_chapter_num

将 chapter_comments 表的 chapter_id UUID FK 替换为 work_id + chapter_num，
与文件系统章节标识对齐。

Revision ID: chapter_comments_use_chapter_num
Revises: add_last_read_chapter_num
Create Date: 2026-02-24 16:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = "chapter_comments_use_chapter_num"
down_revision = "add_last_read_chapter_num"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. 添加新列（先 nullable）
    op.add_column(
        "chapter_comments",
        sa.Column("work_id", UUID(as_uuid=True), nullable=True),
    )
    op.add_column(
        "chapter_comments",
        sa.Column("chapter_num", sa.Integer(), nullable=True),
    )

    # 2. 从 chapters 表回填已有数据
    op.execute("""
        UPDATE chapter_comments cc
        SET work_id = c.work_id, chapter_num = c."order"
        FROM chapters c
        WHERE cc.chapter_id = c.id
    """)

    # 3. 删除无法回填的孤儿评论（chapter_id 指向已不存在的章节）
    op.execute("""
        DELETE FROM chapter_comments
        WHERE work_id IS NULL OR chapter_num IS NULL
    """)

    # 4. 删除 chapter_id 的 FK 约束和索引
    op.drop_constraint(
        "chapter_comments_chapter_id_fkey", "chapter_comments", type_="foreignkey"
    )
    op.drop_index("ix_chapter_comments_chapter_id", table_name="chapter_comments")

    # 5. 删除 chapter_id 列
    op.drop_column("chapter_comments", "chapter_id")

    # 6. 设置 NOT NULL
    op.alter_column("chapter_comments", "work_id", nullable=False)
    op.alter_column("chapter_comments", "chapter_num", nullable=False)

    # 7. 创建 works.id 的 FK 和复合索引
    op.create_foreign_key(
        "fk_chapter_comments_work_id",
        "chapter_comments",
        "works",
        ["work_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_index(
        "ix_chapter_comments_work_chapter",
        "chapter_comments",
        ["work_id", "chapter_num"],
    )


def downgrade() -> None:
    # 回退：恢复 chapter_id 列（数据无法完全恢复）
    op.drop_index("ix_chapter_comments_work_chapter", table_name="chapter_comments")
    op.drop_constraint(
        "fk_chapter_comments_work_id", "chapter_comments", type_="foreignkey"
    )

    op.add_column(
        "chapter_comments",
        sa.Column("chapter_id", UUID(as_uuid=True), nullable=True),
    )

    # 尝试从 chapters 表回填 chapter_id
    op.execute("""
        UPDATE chapter_comments cc
        SET chapter_id = c.id
        FROM chapters c
        WHERE cc.work_id = c.work_id AND cc.chapter_num = c."order"
    """)

    # 删除无法回填的记录
    op.execute("DELETE FROM chapter_comments WHERE chapter_id IS NULL")

    op.alter_column("chapter_comments", "chapter_id", nullable=False)
    op.create_index("ix_chapter_comments_chapter_id", "chapter_comments", ["chapter_id"])
    op.create_foreign_key(
        "chapter_comments_chapter_id_fkey",
        "chapter_comments",
        "chapters",
        ["chapter_id"],
        ["id"],
        ondelete="CASCADE",
    )

    op.drop_column("chapter_comments", "chapter_num")
    op.drop_column("chapter_comments", "work_id")
