"""add timeline_events table

Revision ID: c1d2e3f4g5h6
Revises: b3c4d5e6f7g8
Create Date: 2025-10-21 16:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'c1d2e3f4g5h6'
down_revision = 'b3c4d5e6f7g8'
branch_labels = None
depends_on = None


def upgrade():
    # 创建ENUM类型
    entity_type_enum = postgresql.ENUM('character', 'location', 'setting', 'relationship', name='entity_type_enum', create_type=False)
    entity_type_enum.create(op.get_bind(), checkfirst=True)
    
    event_type_enum = postgresql.ENUM('milestone', 'change', 'created', 'removed', name='event_type_enum', create_type=False)
    event_type_enum.create(op.get_bind(), checkfirst=True)
    
    # 创建timeline_events表
    op.create_table(
        'timeline_events',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('work_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('entity_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('entity_type', entity_type_enum, nullable=False),
        sa.Column('event_type', event_type_enum, nullable=False),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('icon', sa.String(50)),
        sa.Column('chapter_id', postgresql.UUID(as_uuid=True)),
        sa.Column('chapter_number', sa.Integer()),
        sa.Column('timestamp', sa.BigInteger()),
        sa.Column('color', sa.String(20)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['work_id'], ['works.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['chapter_id'], ['chapters.id'], ondelete='SET NULL'),
    )
    
    # 创建索引
    op.create_index('idx_timeline_work_id', 'timeline_events', ['work_id'])
    op.create_index('idx_timeline_entity', 'timeline_events', ['entity_id', 'entity_type'])
    op.create_index('idx_timeline_chapter', 'timeline_events', ['chapter_id'])
    op.create_index('idx_timeline_timestamp', 'timeline_events', ['timestamp'])


def downgrade():
    # 删除索引
    op.drop_index('idx_timeline_timestamp', 'timeline_events')
    op.drop_index('idx_timeline_chapter', 'timeline_events')
    op.drop_index('idx_timeline_entity', 'timeline_events')
    op.drop_index('idx_timeline_work_id', 'timeline_events')
    
    # 删除表
    op.drop_table('timeline_events')
    
    # 删除ENUM类型
    event_type_enum = postgresql.ENUM('milestone', 'change', 'created', 'removed', name='event_type_enum')
    event_type_enum.drop(op.get_bind(), checkfirst=True)
    
    entity_type_enum = postgresql.ENUM('character', 'location', 'setting', 'relationship', name='entity_type_enum')
    entity_type_enum.drop(op.get_bind(), checkfirst=True)
