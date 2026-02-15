"""add_channel_join_requests_table

Revision ID: a1b2c3d4e5f6
Revises: 07f1a3503b46
Create Date: 2025-12-31 23:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = 'a1b2c3d4e5f6'
down_revision = '07f1a3503b46'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 创建申请状态枚举（如果不存在）
    op.execute("""
        DO $$ BEGIN
            CREATE TYPE joinrequeststatus AS ENUM ('pending', 'approved', 'rejected');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
    """)

    # 创建频道加入申请表
    op.create_table(
        'channel_join_requests',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('channel_id', UUID(as_uuid=True), sa.ForeignKey('channels.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('message', sa.Text, nullable=True, comment='申请留言'),
        sa.Column('status', sa.Enum('pending', 'approved', 'rejected', name='joinrequeststatus'), nullable=False, default='pending', index=True),
        sa.Column('reviewed_by', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('reviewed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('reject_reason', sa.Text, nullable=True, comment='拒绝原因'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )

    # 创建索引：便于查询某个频道的待审核申请
    op.create_index('ix_channel_join_requests_channel_status', 'channel_join_requests', ['channel_id', 'status'])


def downgrade() -> None:
    op.drop_index('ix_channel_join_requests_channel_status', table_name='channel_join_requests')
    op.drop_table('channel_join_requests')
    op.execute("DROP TYPE joinrequeststatus")
