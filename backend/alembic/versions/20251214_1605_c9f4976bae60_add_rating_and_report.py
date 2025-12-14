"""add_rating_and_report

Revision ID: c9f4976bae60
Revises: 882cdba7c8a1
Create Date: 2025-12-14 16:05:52.229714

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'c9f4976bae60'
down_revision = '882cdba7c8a1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 创建评分表
    op.create_table(
        'work_ratings',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column('work_id', postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column('rating', sa.Integer(), nullable=False, comment='评分(1-5)'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['work_id'], ['works.id'], ondelete='CASCADE'),
    )
    op.create_index('ix_work_ratings_id', 'work_ratings', ['id'])

    # 创建唯一索引,防止用户重复评分
    op.create_index(
        'uq_user_work_rating',
        'work_ratings',
        ['user_id', 'work_id'],
        unique=True
    )

    # 创建举报原因枚举类型 (如果不存在)
    report_reason = postgresql.ENUM(
        'spam', 'abuse', 'porn', 'illegal', 'false', 'other',
        name='reportreason',
        create_type=False
    )
    # 检查枚举类型是否已存在
    conn = op.get_bind()
    res = conn.execute(sa.text("SELECT 1 FROM pg_type WHERE typname = 'reportreason'"))
    if not res.fetchone():
        report_reason.create(conn, checkfirst=True)

    # 创建评论举报表
    op.create_table(
        'comment_reports',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('comment_id', postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column('reason', report_reason, nullable=False),
        sa.Column('description', sa.Text(), nullable=True, comment='详细描述'),
        sa.Column('is_processed', sa.Boolean(), nullable=False, server_default='false', comment='是否已处理'),
        sa.Column('processed_at', sa.DateTime(timezone=True), nullable=True, comment='处理时间'),
        sa.Column('processed_by', postgresql.UUID(as_uuid=True), nullable=True, comment='处理人'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['comment_id'], ['comments.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['processed_by'], ['users.id'], ondelete='SET NULL'),
    )
    op.create_index('ix_comment_reports_id', 'comment_reports', ['id'])


def downgrade() -> None:
    # 删除举报表
    op.drop_index('ix_comment_reports_id', 'comment_reports')
    op.drop_table('comment_reports')

    # 删除枚举类型
    report_reason = postgresql.ENUM(
        'spam', 'abuse', 'porn', 'illegal', 'false', 'other',
        name='reportreason'
    )
    report_reason.drop(op.get_bind())

    # 删除评分表
    op.drop_index('uq_user_work_rating', 'work_ratings')
    op.drop_index('ix_work_ratings_id', 'work_ratings')
    op.drop_table('work_ratings')
