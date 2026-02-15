"""add_bookshelf

Revision ID: 202e540d4993
Revises: 48bc19c8cb14
Create Date: 2025-12-14 15:14:37.272310

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '202e540d4993'
down_revision = '48bc19c8cb14'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 创建书架表
    op.create_table(
        'bookshelves',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column('work_id', postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column('last_read_chapter_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('last_read_position', sa.Integer(), nullable=False, server_default='0', comment='阅读位置(字符偏移量)'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False, comment='加入书架时间'),
        sa.Column('last_read_at', sa.DateTime(timezone=True), nullable=True, comment='最后阅读时间'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['work_id'], ['works.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['last_read_chapter_id'], ['chapters.id'], ondelete='SET NULL'),
    )
    op.create_index('ix_bookshelves_id', 'bookshelves', ['id'])

    # 创建联合唯一索引，防止用户重复收藏同一作品
    op.create_index(
        'ix_bookshelves_unique',
        'bookshelves',
        ['user_id', 'work_id'],
        unique=True
    )


def downgrade() -> None:
    op.drop_index('ix_bookshelves_unique', 'bookshelves')
    op.drop_index('ix_bookshelves_id', 'bookshelves')
    op.drop_table('bookshelves')
