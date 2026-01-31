"""add_worldview_tables

Revision ID: 73bf53905445
Revises: dfef30e5f344
Create Date: 2025-10-18 10:56:38.700938

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '73bf53905445'
down_revision = 'dfef30e5f344'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create characters table
    op.create_table(
        'characters',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('work_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('avatar', sa.String(500), nullable=True),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('role', sa.String(100), nullable=True),
        sa.Column('tags', postgresql.JSON(), nullable=True),
        sa.Column('relationships', postgresql.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['work_id'], ['works.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_characters_id', 'characters', ['id'])
    op.create_index('ix_characters_work_id', 'characters', ['work_id'])
    
    # Create locations table
    op.create_table(
        'locations',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('work_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('image', sa.String(500), nullable=True),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('type', sa.String(100), nullable=True),
        sa.Column('tags', postgresql.JSON(), nullable=True),
        sa.Column('related_locations', postgresql.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['work_id'], ['works.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_locations_id', 'locations', ['id'])
    op.create_index('ix_locations_work_id', 'locations', ['work_id'])
    
    # Create settings table
    op.create_table(
        'settings',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('work_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('category', sa.String(100), nullable=True),
        sa.Column('content', sa.Text(), nullable=True),
        sa.Column('tags', postgresql.JSON(), nullable=True),
        sa.Column('related_items', postgresql.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['work_id'], ['works.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_settings_id', 'settings', ['id'])
    op.create_index('ix_settings_work_id', 'settings', ['work_id'])
    
    # Create work_guidelines table
    op.create_table(
        'work_guidelines',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('work_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('outline', sa.Text(), nullable=True),
        sa.Column('style', sa.String(200), nullable=True),
        sa.Column('tone', sa.String(200), nullable=True),
        sa.Column('words_per_chapter', sa.Integer(), nullable=True),
        sa.Column('update_frequency', sa.String(100), nullable=True),
        sa.Column('power_system', sa.Text(), nullable=True),
        sa.Column('world_rules', sa.Text(), nullable=True),
        sa.Column('target_audience', sa.String(200), nullable=True),
        sa.Column('main_theme', sa.String(200), nullable=True),
        sa.Column('plot_direction', sa.Text(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['work_id'], ['works.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('work_id')
    )
    op.create_index('ix_work_guidelines_id', 'work_guidelines', ['id'])
    op.create_index('ix_work_guidelines_work_id', 'work_guidelines', ['work_id'])


def downgrade() -> None:
    # Drop all tables in reverse order
    op.drop_index('ix_work_guidelines_work_id', table_name='work_guidelines')
    op.drop_index('ix_work_guidelines_id', table_name='work_guidelines')
    op.drop_table('work_guidelines')
    
    op.drop_index('ix_settings_work_id', table_name='settings')
    op.drop_index('ix_settings_id', table_name='settings')
    op.drop_table('settings')
    
    op.drop_index('ix_locations_work_id', table_name='locations')
    op.drop_index('ix_locations_id', table_name='locations')
    op.drop_table('locations')
    
    op.drop_index('ix_characters_work_id', table_name='characters')
    op.drop_index('ix_characters_id', table_name='characters')
    op.drop_table('characters')
