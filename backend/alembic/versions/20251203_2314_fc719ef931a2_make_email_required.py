"""make_email_required

Revision ID: fc719ef931a2
Revises: 791aaaeeaacb
Create Date: 2025-12-03 23:14:36.260413

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fc719ef931a2'
down_revision = '791aaaeeaacb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. 先为NULL的email设置默认值（使用username@placeholder.local）
    op.execute("""
        UPDATE users
        SET email = username || '@placeholder.local'
        WHERE email IS NULL
    """)

    # 2. 修改列为NOT NULL
    op.alter_column('users', 'email',
                    existing_type=sa.String(255),
                    nullable=False)


def downgrade() -> None:
    # 恢复为可选
    op.alter_column('users', 'email',
                    existing_type=sa.String(255),
                    nullable=True)
