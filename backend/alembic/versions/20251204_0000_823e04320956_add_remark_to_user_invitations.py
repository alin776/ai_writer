"""add_remark_to_user_invitations

Revision ID: 823e04320956
Revises: fc719ef931a2
Create Date: 2025-12-04 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '823e04320956'
down_revision = 'fc719ef931a2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 为 user_invitations 表添加 remark 字段
    op.add_column('user_invitations',
                  sa.Column('remark', sa.String(length=255), nullable=True))


def downgrade() -> None:
    # 移除 remark 字段
    op.drop_column('user_invitations', 'remark')
