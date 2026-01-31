"""add_humanize_tables

Revision ID: m4n5o6p7q8r9
Revises: 8h9i0j1k2l3m
Create Date: 2025-10-26 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision = 'm4n5o6p7q8r9'
down_revision = '8h9i0j1k2l3m'
branch_labels = None
depends_on = None


def table_exists(table_name):
    """检查表是否存在"""
    bind = op.get_bind()
    inspector = inspect(bind)
    return table_name in inspector.get_table_names()


def upgrade() -> None:
    # ========== 创建 user_profiles 表 ==========
    if not table_exists('user_profiles'):
        op.create_table(
            'user_profiles',
            sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),

            # 使用统计
            sa.Column('total_uses', sa.Integer(), nullable=False, server_default='0'),
            sa.Column('avg_text_length', sa.Integer(), nullable=True),
            sa.Column('most_used_function', sa.String(length=50), nullable=True),

            # 偏好设置
            sa.Column('preferred_intensity', sa.String(length=20), nullable=True),
            sa.Column('preferred_speed_over_quality', sa.Boolean(), nullable=False, server_default='false'),
            sa.Column('is_novel_writer', sa.Boolean(), nullable=False, server_default='false'),

            # 反馈统计
            sa.Column('total_accepted', sa.Integer(), nullable=False, server_default='0'),
            sa.Column('total_rejected', sa.Integer(), nullable=False, server_default='0'),
            sa.Column('accept_rate', sa.Float(), nullable=False, server_default='0.0'),

            # 开关控制
            sa.Column('humanize_enabled_global', sa.Boolean(), nullable=False, server_default='true'),
            sa.Column('humanize_enabled_by_function', postgresql.JSONB(astext_type=sa.Text()), nullable=False,
                      server_default=sa.text("'{\"complete\": true, \"polish\": true, \"expand\": true, \"translate\": false, \"summarize\": false, \"rewrite\": true}'::jsonb")),

            # 时间戳
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
            sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),

            sa.PrimaryKeyConstraint('id'),
            sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        )

        # 创建索引
        op.create_index(op.f('ix_user_profiles_user_id'), 'user_profiles', ['user_id'], unique=True)


    # ========== 创建 humanize_sessions 表 ==========
    if not table_exists('humanize_sessions'):
        op.create_table(
            'humanize_sessions',
            sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),

            # 使用场景
            sa.Column('ai_function', sa.String(length=50), nullable=False),

            # 核心指标
            sa.Column('score_before', sa.Float(), nullable=False),
            sa.Column('score_after', sa.Float(), nullable=False),
            sa.Column('improvement', sa.Float(), nullable=False),

            # 去痕迹强度
            sa.Column('intensity', sa.String(length=20), nullable=False, server_default='medium'),

            # 用户反馈
            sa.Column('user_accepted', sa.Boolean(), nullable=True),

            # 性能指标
            sa.Column('processing_time', sa.Float(), nullable=False),
            sa.Column('tokens_used', sa.Integer(), nullable=False),
            sa.Column('cost', sa.Float(), nullable=False),

            # 时间戳
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),

            sa.PrimaryKeyConstraint('id'),
            sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        )

        # 创建索引
        op.create_index(op.f('ix_humanize_sessions_id'), 'humanize_sessions', ['id'], unique=False)
        op.create_index(op.f('ix_humanize_sessions_user_id'), 'humanize_sessions', ['user_id'], unique=False)
        op.create_index(op.f('ix_humanize_sessions_ai_function'), 'humanize_sessions', ['ai_function'], unique=False)
        op.create_index(op.f('ix_humanize_sessions_created_at'), 'humanize_sessions', ['created_at'], unique=False)


    # ========== 创建 humanize_session_details 表 ==========
    if not table_exists('humanize_session_details'):
        op.create_table(
            'humanize_session_details',
            sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column('session_id', postgresql.UUID(as_uuid=True), nullable=False),

            # 五维度评分详情
            sa.Column('dimensions_before', postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'{}'::jsonb")),
            sa.Column('dimensions_after', postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'{}'::jsonb")),

            # 检测到的AI痕迹
            sa.Column('detected_patterns', postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'[]'::jsonb")),

            # 文本预览
            sa.Column('original_preview', sa.String(length=200), nullable=True),
            sa.Column('humanized_preview', sa.String(length=200), nullable=True),

            # 过期时间
            sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),

            # 时间戳
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),

            sa.PrimaryKeyConstraint('id'),
            sa.ForeignKeyConstraint(['session_id'], ['humanize_sessions.id'], ondelete='CASCADE'),
        )

        # 创建索引
        op.create_index(op.f('ix_humanize_session_details_session_id'), 'humanize_session_details', ['session_id'], unique=True)
        op.create_index(op.f('ix_humanize_session_details_expires_at'), 'humanize_session_details', ['expires_at'], unique=False)


def downgrade() -> None:
    # 删除表 (逆序)
    op.drop_index(op.f('ix_humanize_session_details_expires_at'), table_name='humanize_session_details')
    op.drop_index(op.f('ix_humanize_session_details_session_id'), table_name='humanize_session_details')
    op.drop_table('humanize_session_details')

    op.drop_index(op.f('ix_humanize_sessions_created_at'), table_name='humanize_sessions')
    op.drop_index(op.f('ix_humanize_sessions_ai_function'), table_name='humanize_sessions')
    op.drop_index(op.f('ix_humanize_sessions_user_id'), table_name='humanize_sessions')
    op.drop_index(op.f('ix_humanize_sessions_id'), table_name='humanize_sessions')
    op.drop_table('humanize_sessions')

    op.drop_index(op.f('ix_user_profiles_user_id'), table_name='user_profiles')
    op.drop_table('user_profiles')
