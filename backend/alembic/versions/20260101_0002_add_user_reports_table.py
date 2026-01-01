"""add_user_reports_table

Revision ID: 20260101_0002
Revises: 20260101_0001
Create Date: 2026-01-01 00:02:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import uuid


# revision identifiers, used by Alembic.
revision = '20260101_0002'
down_revision = '20260101_0001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 创建用户举报原因枚举
    op.execute("""
        DO $$ BEGIN
            CREATE TYPE userreportreason AS ENUM ('spam', 'harassment', 'inappropriate', 'impersonation', 'other');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
    """)

    # 创建用户举报状态枚举
    op.execute("""
        DO $$ BEGIN
            CREATE TYPE userreportstatus AS ENUM ('pending', 'reviewed', 'dismissed', 'actioned');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
    """)

    # 创建 user_reports 表
    op.create_table(
        'user_reports',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True),
        sa.Column('reporter_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True, comment='举报者ID'),
        sa.Column('reported_user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True, comment='被举报用户ID'),
        sa.Column('reason', sa.Enum('spam', 'harassment', 'inappropriate', 'impersonation', 'other', name='userreportreason'), nullable=False, comment='举报原因'),
        sa.Column('description', sa.Text, nullable=True, comment='详细描述'),
        sa.Column('status', sa.Enum('pending', 'reviewed', 'dismissed', 'actioned', name='userreportstatus'), default='pending', nullable=False, comment='举报状态'),
        sa.Column('reviewed_at', sa.DateTime(timezone=True), nullable=True, comment='审核时间'),
        sa.Column('reviewed_by', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True, comment='审核人ID'),
        sa.Column('admin_note', sa.Text, nullable=True, comment='管理员备注'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )

    # 创建索引：便于查询某用户收到的举报
    op.create_index('ix_user_reports_reported_user_status', 'user_reports', ['reported_user_id', 'status'])
    # 创建索引：便于查询待处理的举报
    op.create_index('ix_user_reports_status', 'user_reports', ['status'])


def downgrade() -> None:
    op.drop_index('ix_user_reports_status', table_name='user_reports')
    op.drop_index('ix_user_reports_reported_user_status', table_name='user_reports')
    op.drop_table('user_reports')
    op.execute("DROP TYPE IF EXISTS userreportstatus")
    op.execute("DROP TYPE IF EXISTS userreportreason")
