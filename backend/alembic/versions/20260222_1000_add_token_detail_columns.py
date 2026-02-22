"""add_token_detail_columns

为 ai_call_logs 表添加 token 细分列：
- cache_read_tokens: 缓存命中的输入 token
- cache_creation_tokens: 创建缓存的 token (Anthropic)
- reasoning_tokens: 推理 token (o1/o3/GPT-5.2)

Revision ID: add_token_detail_cols
Revises: drop_humanize_tables
Create Date: 2026-02-22 10:00:00.000000
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "add_token_detail_cols"
down_revision = "drop_humanize_tables"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('ai_call_logs', sa.Column('cache_read_tokens', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('ai_call_logs', sa.Column('cache_creation_tokens', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('ai_call_logs', sa.Column('reasoning_tokens', sa.Integer(), nullable=False, server_default='0'))


def downgrade() -> None:
    op.drop_column('ai_call_logs', 'reasoning_tokens')
    op.drop_column('ai_call_logs', 'cache_creation_tokens')
    op.drop_column('ai_call_logs', 'cache_read_tokens')
