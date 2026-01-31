"""add entity_groups and group_members tables

Revision ID: c5d6e7f8g9h0
Revises: b4c5d6e7f8g9
Create Date: 2025-10-21 17:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'c5d6e7f8g9h0'
down_revision = 'c1d2e3f4g5h6'  # 指向timeline_events表的版本
branch_labels = None
depends_on = None


def upgrade():
    # 创建entity_groups表
    op.create_table(
        'entity_groups',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('work_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('group_type', sa.String(length=50), nullable=False, server_default='manual'),
        sa.Column('auto_rule', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('color', sa.String(length=20), nullable=True),
        sa.Column('icon', sa.String(length=50), nullable=True),
        sa.Column('parent_group_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('order_index', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['work_id'], ['works.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['parent_group_id'], ['entity_groups.id'], ondelete='SET NULL')
    )
    op.create_index(op.f('ix_entity_groups_work_id'), 'entity_groups', ['work_id'], unique=False)
    
    # 创建group_members表
    op.create_table(
        'group_members',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('group_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('entity_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('entity_type', sa.String(length=50), nullable=False),
        sa.Column('order_index', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['group_id'], ['entity_groups.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('group_id', 'entity_id', 'entity_type', name='uq_group_entity')
    )
    op.create_index(op.f('ix_group_members_group_id'), 'group_members', ['group_id'], unique=False)
    op.create_index(op.f('ix_group_members_entity_id'), 'group_members', ['entity_id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_group_members_entity_id'), table_name='group_members')
    op.drop_index(op.f('ix_group_members_group_id'), table_name='group_members')
    op.drop_table('group_members')
    
    op.drop_index(op.f('ix_entity_groups_work_id'), table_name='entity_groups')
    op.drop_table('entity_groups')
