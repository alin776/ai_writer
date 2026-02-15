"""add_node_id_to_chapter_vectors

Revision ID: add_node_id_to_chapter_vectors
Revises: add_chapter_content_indexes
Create Date: 2026-01-27 00:01:00.000000
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "add_node_id_to_chapter_vectors"
down_revision = "add_chapter_content_indexes"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("novel_chapter_vectors", sa.Column("node_id", sa.String(length=64), nullable=True))


def downgrade() -> None:
    op.drop_column("novel_chapter_vectors", "node_id")
