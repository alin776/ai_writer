"""fix_fangroup_is_permanent_default

Revision ID: fix_fangroup_default
Revises: b86546416013
Create Date: 2025-12-23 17:30:00.000000

修复粉丝群 is_permanent 字段的默认值问题
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fix_fangroup_default'
down_revision = 'b86546416013'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. 先将所有现有粉丝群改为非永久
    op.execute("""
        UPDATE channels
        SET is_permanent = false
        WHERE type = 'fangroup'
    """)

    print("✓ 已将所有现有粉丝群设置为非永久状态")


def downgrade() -> None:
    # 回滚：将所有粉丝群改回永久
    op.execute("""
        UPDATE channels
        SET is_permanent = true
        WHERE type = 'fangroup'
    """)
