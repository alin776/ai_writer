"""add_work_reports_table

Revision ID: add_work_reports
Revises: fix_fangroup_default
Create Date: 2025-12-23 19:00:00.000000

添加小说举报表
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'add_work_reports'
down_revision = 'fix_fangroup_default'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 创建小说举报原因枚举类型
    work_report_reason = postgresql.ENUM(
        'spam', 'porn', 'illegal', 'plagiarism', 'false', 'other',
        name='workreportreason',
        create_type=False
    )
    # 检查枚举类型是否已存在
    conn = op.get_bind()
    res = conn.execute(sa.text("SELECT 1 FROM pg_type WHERE typname = 'workreportreason'"))
    if not res.fetchone():
        work_report_reason.create(conn, checkfirst=True)

    # 创建小说举报状态枚举类型
    work_report_status = postgresql.ENUM(
        'pending', 'reviewed', 'dismissed', 'actioned',
        name='workreportstatus',
        create_type=False
    )
    res = conn.execute(sa.text("SELECT 1 FROM pg_type WHERE typname = 'workreportstatus'"))
    if not res.fetchone():
        work_report_status.create(conn, checkfirst=True)

    # 创建小说举报表
    op.create_table(
        'work_reports',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('work_id', postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column('reporter_id', postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column('reason', work_report_reason, nullable=False),
        sa.Column('description', sa.Text(), nullable=True, comment='详细描述'),
        sa.Column('status', work_report_status, nullable=False, server_default='pending'),
        sa.Column('action_taken', sa.String(50), nullable=True, comment='采取的操作'),
        sa.Column('admin_note', sa.Text(), nullable=True, comment='管理员备注'),
        sa.Column('reviewed_at', sa.DateTime(timezone=True), nullable=True, comment='审核时间'),
        sa.Column('reviewed_by', postgresql.UUID(as_uuid=True), nullable=True, comment='审核人'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['work_id'], ['works.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['reporter_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['reviewed_by'], ['users.id'], ondelete='SET NULL'),
    )
    op.create_index('ix_work_reports_id', 'work_reports', ['id'])

    # 创建唯一索引，防止用户重复举报同一小说
    op.create_index(
        'uq_user_work_report',
        'work_reports',
        ['reporter_id', 'work_id'],
        unique=True
    )


def downgrade() -> None:
    # 删除索引和表
    op.drop_index('uq_user_work_report', 'work_reports')
    op.drop_index('ix_work_reports_id', 'work_reports')
    op.drop_table('work_reports')

    # 删除枚举类型
    conn = op.get_bind()
    conn.execute(sa.text("DROP TYPE IF EXISTS workreportstatus"))
    conn.execute(sa.text("DROP TYPE IF EXISTS workreportreason"))
