"""create_system_config

创建 system_config 表，用于存储可动态修改的系统配置（定价、汇率等）。
初始数据：model_pricing（GPT-5.2 + default 兜底）、credits_per_dollar（5000）。

Revision ID: create_system_config
Revises: add_token_detail_cols
Create Date: 2026-02-22 11:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSON


# revision identifiers, used by Alembic.
revision = "create_system_config"
down_revision = "add_token_detail_cols"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'system_config',
        sa.Column('key', sa.String(100), primary_key=True),
        sa.Column('value', JSON, nullable=False),
        sa.Column('description', sa.String(255), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_by', UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=True),
    )
    # 初始定价数据
    op.execute("""
        INSERT INTO system_config (key, value, description) VALUES
        ('model_pricing', '{"gpt-5.2": {"input": 0.875, "cached_input": 0.1094, "output": 7.0, "reasoning": 7.0, "cache_creation": 0.875}, "default": {"input": 1.0, "cached_input": 0.5, "output": 2.0, "reasoning": 2.0, "cache_creation": 1.0}}', '模型定价 ($/M tokens)'),
        ('credits_per_dollar', '5000', '美元兑积分比例')
    """)


def downgrade() -> None:
    op.drop_table('system_config')
