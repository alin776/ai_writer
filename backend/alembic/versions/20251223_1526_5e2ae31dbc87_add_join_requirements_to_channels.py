"""add_join_requirements_to_channels

Revision ID: 5e2ae31dbc87
Revises: 54978086aa10
Create Date: 2025-12-23 15:26:39.299845

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5e2ae31dbc87'
down_revision = '54978086aa10'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 添加进入要求配置字段
    op.add_column('channels', sa.Column('join_requirement', sa.Text(), nullable=True, comment='进入要求配置(JSON)'))

    # 为"作者酒馆"设置进入要求：需要至少发布一本作品
    op.execute("""
        UPDATE channels
        SET join_requirement = '{"type": "published_works", "min_count": 1, "message": "需要发布至少一本作品才能加入作者酒馆"}'
        WHERE name = '作者酒馆' AND type = 'official'
    """)


def downgrade() -> None:
    # 删除进入要求字段
    op.drop_column('channels', 'join_requirement')
