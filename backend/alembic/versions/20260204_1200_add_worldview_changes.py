"""add_worldview_changes

Revision ID: add_worldview_changes
Revises: add_worldview_scan_progress
Create Date: 2026-02-04 12:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB


# revision identifiers, used by Alembic.
revision = "add_worldview_changes"
down_revision = "add_worldview_scan_progress"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 检查列是否存在，不存在才添加
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    columns = [col['name'] for col in inspector.get_columns('works')]

    if 'worldview_version' not in columns:
        op.add_column(
            "works",
            sa.Column("worldview_version", sa.Integer(), nullable=False, server_default="1")
        )

    # 检查枚举类型是否存在
    result = conn.execute(sa.text(
        "SELECT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'worldviewchangestatus')"
    ))
    enum_exists = result.scalar()

    if not enum_exists:
        # 创建枚举类型
        op.execute("CREATE TYPE worldviewchangestatus AS ENUM ('pending', 'applied', 'rejected')")

    # 检查表是否存在
    tables = inspector.get_table_names()
    if 'worldview_changes' not in tables:
        op.create_table(
            "worldview_changes",
            sa.Column("id", UUID(as_uuid=True), primary_key=True, nullable=False),
            sa.Column("work_id", UUID(as_uuid=True), nullable=False),
            sa.Column("user_id", UUID(as_uuid=True), nullable=False),
            sa.Column("applied_by", UUID(as_uuid=True), nullable=True),
            sa.Column(
                "status",
                sa.Enum("pending", "applied", "rejected", name="worldviewchangestatus", create_type=False),
                nullable=False,
            ),
            sa.Column("source", sa.String(length=50), nullable=True),
            sa.Column("changes", JSONB, nullable=False),
            sa.Column("selected_items", JSONB, nullable=True),
            sa.Column("evidence", JSONB, nullable=True),
            sa.Column("user_notes", sa.Text(), nullable=True),
            sa.Column("version_before", sa.Integer(), nullable=True),
            sa.Column("version_after", sa.Integer(), nullable=True),
            sa.Column("apply_stats", JSONB, nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
            sa.Column("applied_at", sa.DateTime(timezone=True), nullable=True),
            sa.ForeignKeyConstraint(["work_id"], ["works.id"], ondelete="CASCADE"),
            sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
            sa.ForeignKeyConstraint(["applied_by"], ["users.id"]),
        )
        op.create_index("ix_worldview_changes_work_id", "worldview_changes", ["work_id"])
        op.create_index("ix_worldview_changes_user_id", "worldview_changes", ["user_id"])
        op.create_index("ix_worldview_changes_applied_by", "worldview_changes", ["applied_by"])
        op.create_index("ix_worldview_changes_status", "worldview_changes", ["status"])


def downgrade() -> None:
    op.drop_index("ix_worldview_changes_status", table_name="worldview_changes")
    op.drop_index("ix_worldview_changes_applied_by", table_name="worldview_changes")
    op.drop_index("ix_worldview_changes_user_id", table_name="worldview_changes")
    op.drop_index("ix_worldview_changes_work_id", table_name="worldview_changes")
    op.drop_table("worldview_changes")
    op.drop_column("works", "worldview_version")
    op.execute("DROP TYPE IF EXISTS worldviewchangestatus")
