"""No-op migration: keep invitation code length at 8

Revision ID: 9e2a6c8e4a10
Revises: 823e04320956
Create Date: 2025-12-04 01:01:00.000000
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "9e2a6c8e4a10"
down_revision = "823e04320956"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # requirement changed: keep codes at 8 characters, so no schema change needed
    pass


def downgrade() -> None:
    # no-op
    pass
