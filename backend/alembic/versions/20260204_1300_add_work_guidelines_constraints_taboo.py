"""add_work_guidelines_fields

Revision ID: add_work_guidelines_fields
Revises: add_worldview_changes
Create Date: 2026-02-04 13:00:00.000000
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "add_work_guidelines_fields"
down_revision = "add_worldview_changes"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("work_guidelines", sa.Column("constraints", sa.Text(), nullable=True))
    op.add_column("work_guidelines", sa.Column("taboo", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("work_guidelines", "taboo")
    op.drop_column("work_guidelines", "constraints")
