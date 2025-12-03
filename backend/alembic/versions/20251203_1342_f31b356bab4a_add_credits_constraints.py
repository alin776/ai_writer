"""add_credits_constraints

Revision ID: f31b356bab4a
Revises: f520ea037045
Create Date: 2025-12-03 13:42:01.109837

修复内容:
- H1: invitee_id 添加唯一约束
- M1: user_credits 添加非负约束
- M2: user_invitations 添加范围约束
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'f31b356bab4a'
down_revision = 'f520ea037045'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # H1: invitee_id 添加唯一约束 (替换普通索引为唯一索引)
    op.drop_index('ix_invitation_usages_invitee_id', table_name='invitation_usages')
    op.create_index(op.f('ix_invitation_usages_invitee_id'), 'invitation_usages', ['invitee_id'], unique=True)

    # M1: user_credits 添加非负约束
    op.create_check_constraint(
        'check_balance_non_negative',
        'user_credits',
        'balance >= 0'
    )
    op.create_check_constraint(
        'check_recharged_non_negative',
        'user_credits',
        'total_recharged >= 0'
    )
    op.create_check_constraint(
        'check_consumed_non_negative',
        'user_credits',
        'total_consumed >= 0'
    )
    op.create_check_constraint(
        'check_gifted_non_negative',
        'user_credits',
        'total_gifted >= 0'
    )

    # M2: user_invitations 添加范围约束
    op.create_check_constraint(
        'check_used_count_non_negative',
        'user_invitations',
        'used_count >= 0'
    )
    op.create_check_constraint(
        'check_used_count_limit',
        'user_invitations',
        'used_count <= max_uses'
    )
    op.create_check_constraint(
        'check_activated_count_non_negative',
        'user_invitations',
        'activated_count >= 0'
    )
    op.create_check_constraint(
        'check_activated_count_limit',
        'user_invitations',
        'activated_count <= used_count'
    )


def downgrade() -> None:
    # 移除 M2 约束
    op.drop_constraint('check_activated_count_limit', 'user_invitations', type_='check')
    op.drop_constraint('check_activated_count_non_negative', 'user_invitations', type_='check')
    op.drop_constraint('check_used_count_limit', 'user_invitations', type_='check')
    op.drop_constraint('check_used_count_non_negative', 'user_invitations', type_='check')

    # 移除 M1 约束
    op.drop_constraint('check_gifted_non_negative', 'user_credits', type_='check')
    op.drop_constraint('check_consumed_non_negative', 'user_credits', type_='check')
    op.drop_constraint('check_recharged_non_negative', 'user_credits', type_='check')
    op.drop_constraint('check_balance_non_negative', 'user_credits', type_='check')

    # 恢复 H1 普通索引
    op.drop_index(op.f('ix_invitation_usages_invitee_id'), table_name='invitation_usages')
    op.create_index('ix_invitation_usages_invitee_id', 'invitation_usages', ['invitee_id'], unique=False)
