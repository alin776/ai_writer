"""merge_multiple_heads

Revision ID: 6f42c0fb6213
Revises: d996600d54be, 2c125e3852a5, 9a6f9f4c0c1e
Create Date: 2025-12-11 10:52:56.944337

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6f42c0fb6213'
down_revision = ('d996600d54be', '2c125e3852a5', '9a6f9f4c0c1e')
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
