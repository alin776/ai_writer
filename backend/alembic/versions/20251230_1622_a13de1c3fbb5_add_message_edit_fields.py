"""add_message_edit_fields

Revision ID: a13de1c3fbb5
Revises: 072013f12c3f
Create Date: 2025-12-30 16:22:42.000520

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a13de1c3fbb5'
down_revision = '072013f12c3f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 添加 is_edited 字段
    op.add_column(
        'channel_messages',
        sa.Column('is_edited', sa.Boolean(), nullable=False, server_default='false')
    )
    # 添加 edited_at 字段
    op.add_column(
        'channel_messages',
        sa.Column('edited_at', sa.DateTime(timezone=True), nullable=True)
    )


def downgrade() -> None:
    op.drop_column('channel_messages', 'edited_at')
    op.drop_column('channel_messages', 'is_edited')
