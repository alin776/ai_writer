"""add_worldview_scan_progress

Revision ID: add_worldview_scan_progress
Revises: add_agent_session_message_index
Create Date: 2026-02-03 00:01:00.000000
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "add_worldview_scan_progress"
down_revision = "add_agent_session_message_index"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "worldview_scan_progress",
        sa.Column("id", sa.String(), primary_key=True, nullable=False),
        sa.Column("work_id", sa.String(), nullable=False),
        sa.Column("status", sa.String(), nullable=False, server_default=sa.text("'pending'")),
        sa.Column("scan_mode", sa.String(), nullable=True, server_default=sa.text("'incremental'")),
        sa.Column("chapters_total", sa.Integer(), nullable=True),
        sa.Column("chapters_processed", sa.Integer(), nullable=True),
        sa.Column("batches_total", sa.Integer(), nullable=True),
        sa.Column("batches_completed", sa.Integer(), nullable=True),
        sa.Column("characters_created", sa.Integer(), nullable=True),
        sa.Column("characters_updated", sa.Integer(), nullable=True),
        sa.Column("locations_created", sa.Integer(), nullable=True),
        sa.Column("locations_updated", sa.Integer(), nullable=True),
        sa.Column("settings_created", sa.Integer(), nullable=True),
        sa.Column("settings_updated", sa.Integer(), nullable=True),
        sa.Column("relationships_created", sa.Integer(), nullable=True),
        sa.Column("last_error", sa.Text(), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("metadata_json", sa.Text(), nullable=True)
    )
    op.create_index(
        "ix_worldview_scan_progress_work_id",
        "worldview_scan_progress",
        ["work_id"],
        unique=True
    )


def downgrade() -> None:
    op.drop_index("ix_worldview_scan_progress_work_id", table_name="worldview_scan_progress")
    op.drop_table("worldview_scan_progress")
