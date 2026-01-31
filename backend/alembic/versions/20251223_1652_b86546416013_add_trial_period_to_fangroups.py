"""add_trial_period_to_fangroups

Revision ID: b86546416013
Revises: 3adba1e3b0fe
Create Date: 2025-12-23 16:52:13.169462

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b86546416013'
down_revision = '3adba1e3b0fe'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 添加测试期结束时间字段（预留字段，目前暂未使用）
    # 实际使用 last_message_at 来判断是否需要解散
    op.add_column('channels', sa.Column('trial_end_at', sa.DateTime(timezone=True), nullable=True, comment='测试期结束时间'))


def downgrade() -> None:
    # 删除测试期字段
    op.drop_column('channels', 'trial_end_at')
