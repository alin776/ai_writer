"""add_workgenre_new_values

Revision ID: add_workgenre_new_values
Revises: add_worldview_entity_glossary
Create Date: 2026-02-15 10:00:00.000000
"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "add_workgenre_new_values"
down_revision = "add_worldview_entity_glossary"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("ALTER TYPE workgenre ADD VALUE IF NOT EXISTS 'suspense'")
    op.execute("ALTER TYPE workgenre ADD VALUE IF NOT EXISTS 'western_fantasy'")
    op.execute("ALTER TYPE workgenre ADD VALUE IF NOT EXISTS 'apocalypse'")


def downgrade() -> None:
    # PostgreSQL 不支持直接删除 enum 值，需要重建类型
    pass
