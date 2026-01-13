"""add_chapter_revisions

Revision ID: add_chapter_revisions
Revises: add_interaction_types
Create Date: 2026-01-13 18:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB


# revision identifiers, used by Alembic.
revision = "add_chapter_revisions"
down_revision = "add_interaction_types"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "chapter_revisions",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("request_id", sa.String(length=64), nullable=False),
        sa.Column("work_id", UUID(as_uuid=True), nullable=False),
        sa.Column("chapter_id", UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", UUID(as_uuid=True), nullable=True),
        sa.Column(
            "status",
            sa.Enum(
                "pending",
                "accepted",
                "discarded",
                "conflict",
                name="chapterrevisionstatus",
            ),
            nullable=False,
        ),
        sa.Column("operation", sa.String(length=20), nullable=False),
        sa.Column("original_text", sa.Text(), nullable=True),
        sa.Column("new_text", sa.Text(), nullable=False),
        sa.Column("position", JSONB, nullable=True),
        sa.Column("before_anchor", sa.Text(), nullable=True),
        sa.Column("after_anchor", sa.Text(), nullable=True),
        sa.Column("node_id", sa.String(length=64), nullable=True),
        sa.Column("paragraph_index", sa.Integer(), nullable=True),
        sa.Column("base_version", sa.Integer(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("applied_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["chapter_id"], ["chapters.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["work_id"], ["works.id"], ondelete="CASCADE"),
    )

    op.create_index("ix_chapter_revisions_request_id", "chapter_revisions", ["request_id"], unique=True)
    op.create_index("ix_chapter_revisions_work_id", "chapter_revisions", ["work_id"])
    op.create_index("ix_chapter_revisions_chapter_id", "chapter_revisions", ["chapter_id"])
    op.create_index("ix_chapter_revisions_user_id", "chapter_revisions", ["user_id"])
    op.create_index("ix_chapter_revisions_status", "chapter_revisions", ["status"])


def downgrade() -> None:
    op.drop_index("ix_chapter_revisions_status", table_name="chapter_revisions")
    op.drop_index("ix_chapter_revisions_user_id", table_name="chapter_revisions")
    op.drop_index("ix_chapter_revisions_chapter_id", table_name="chapter_revisions")
    op.drop_index("ix_chapter_revisions_work_id", table_name="chapter_revisions")
    op.drop_index("ix_chapter_revisions_request_id", table_name="chapter_revisions")
    op.drop_table("chapter_revisions")
    op.execute("DROP TYPE IF EXISTS chapterrevisionstatus")
