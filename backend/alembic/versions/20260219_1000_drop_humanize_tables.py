"""drop_humanize_tables

删除已废弃的 humanize 相关表（humanize_session_details, humanize_sessions, user_profiles）。
该功能已被 Skills 系统取代。

Revision ID: drop_humanize_tables
Revises: unify_embedding_dim_512
Create Date: 2026-02-19 10:00:00.000000
"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "drop_humanize_tables"
down_revision = "unify_embedding_dim_512"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("DROP TABLE IF EXISTS humanize_session_details")
    op.execute("DROP TABLE IF EXISTS humanize_sessions")
    op.execute("DROP TABLE IF EXISTS user_profiles")


def downgrade() -> None:
    # 不恢复已废弃的表
    pass
