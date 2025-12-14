"""Merge heads

Revision ID: 00e8e68c3c88
Revises: add_activity_fields, 0518fa576df4
Create Date: 2025-12-13 19:55:06.963002

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '00e8e68c3c88'
down_revision = ('add_activity_fields', '0518fa576df4')
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
