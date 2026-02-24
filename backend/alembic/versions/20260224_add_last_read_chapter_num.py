"""add_last_read_chapter_num

为 bookshelves 表添加 last_read_chapter_num 列，支持文件系统章节迁移后的阅读进度记录。

Revision ID: add_last_read_chapter_num
Revises: create_system_config
Create Date: 2026-02-24 10:00:00.000000
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "add_last_read_chapter_num"
down_revision = "create_system_config"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "bookshelves",
        sa.Column(
            "last_read_chapter_num",
            sa.Integer(),
            nullable=True,
            comment="最后阅读的章节序号（FS 迁移后使用）",
        ),
    )


def downgrade():
    op.drop_column("bookshelves", "last_read_chapter_num")
