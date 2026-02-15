"""add_banned_at_to_channel_members

Revision ID: 07f1a3503b46
Revises: 94e8fc7d9c2f
Create Date: 2025-12-31 21:58:30.576182

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '07f1a3503b46'
down_revision = '94e8fc7d9c2f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('channel_members', sa.Column('banned_at', sa.DateTime(timezone=True), nullable=True, comment='封禁时间'))


def downgrade() -> None:
    op.drop_column('channel_members', 'banned_at')
