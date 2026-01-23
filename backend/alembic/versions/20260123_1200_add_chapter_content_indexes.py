"""add_chapter_content_indexes

Revision ID: add_chapter_content_indexes
Revises: add_chapter_revisions
Create Date: 2026-01-23 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = "add_chapter_content_indexes"
down_revision = "add_chapter_revisions"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "chapter_content_indexes",
        sa.Column("chapter_id", UUID(as_uuid=True), nullable=False),
        sa.Column("work_id", UUID(as_uuid=True), nullable=False),
        sa.Column("plain_text", sa.Text(), nullable=False),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("content_hash", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["chapter_id"], ["chapters.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["work_id"], ["works.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("chapter_id"),
    )
    op.create_index("ix_chapter_content_indexes_work_id", "chapter_content_indexes", ["work_id"])
    op.create_index("ix_chapter_content_indexes_content_hash", "chapter_content_indexes", ["content_hash"])


def downgrade() -> None:
    op.drop_index("ix_chapter_content_indexes_content_hash", table_name="chapter_content_indexes")
    op.drop_index("ix_chapter_content_indexes_work_id", table_name="chapter_content_indexes")
    op.drop_table("chapter_content_indexes")
