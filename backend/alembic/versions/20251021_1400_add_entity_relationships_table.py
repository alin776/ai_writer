"""add entity_relationships table

Revision ID: b3c4d5e6f7g8
Revises: a1b2c3d4e5f6
Create Date: 2025-10-21 14:00:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'b3c4d5e6f7g8'
down_revision = 'a1b2c3d4e5f6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create entity_relationships table
    op.create_table(
        'entity_relationships',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('work_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('source_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('source_type', sa.String(length=50), nullable=False),
        sa.Column('target_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('target_type', sa.String(length=50), nullable=False),
        sa.Column('relationship_type', sa.String(length=100), nullable=False),
        sa.Column('label', sa.String(length=200), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('strength', sa.Integer(), nullable=True),
        sa.Column('direction', sa.String(length=20), nullable=True),
        sa.Column('start_chapter_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('end_chapter_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('start_time', sa.TIMESTAMP(), nullable=True),
        sa.Column('end_time', sa.TIMESTAMP(), nullable=True),
        sa.Column('color', sa.String(length=20), nullable=True),
        sa.Column('line_style', sa.String(length=20), nullable=True),
        sa.Column('tags', postgresql.ARRAY(sa.Text()), nullable=True),
        sa.Column('category', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['work_id'], ['works.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['start_chapter_id'], ['chapters.id']),
        sa.ForeignKeyConstraint(['end_chapter_id'], ['chapters.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.CheckConstraint("source_type IN ('character', 'location', 'setting')", name='valid_source_type'),
        sa.CheckConstraint("target_type IN ('character', 'location', 'setting')", name='valid_target_type'),
        sa.CheckConstraint("direction IN ('one-way', 'two-way')", name='valid_direction'),
        sa.CheckConstraint("line_style IN ('solid', 'dashed', 'dotted')", name='valid_line_style'),
        sa.CheckConstraint("strength BETWEEN 1 AND 10", name='valid_strength'),
    )
    
    # Create indexes for better query performance
    op.create_index('ix_entity_relationships_work_id', 'entity_relationships', ['work_id'])
    op.create_index('ix_entity_relationships_source', 'entity_relationships', ['source_id', 'source_type'])
    op.create_index('ix_entity_relationships_target', 'entity_relationships', ['target_id', 'target_type'])


def downgrade() -> None:
    # Drop indexes
    op.drop_index('ix_entity_relationships_target', table_name='entity_relationships')
    op.drop_index('ix_entity_relationships_source', table_name='entity_relationships')
    op.drop_index('ix_entity_relationships_work_id', table_name='entity_relationships')
    
    # Drop table
    op.drop_table('entity_relationships')
