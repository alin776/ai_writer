"""add_interaction_notification_types

Revision ID: add_interaction_types
Revises: b6d2d534d191
Create Date: 2026-01-03 15:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_interaction_types'
down_revision = 'b6d2d534d191'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 添加 'INTERACTION' 值到 notificationcategory ENUM 类型
    op.execute("ALTER TYPE notificationcategory ADD VALUE IF NOT EXISTS 'INTERACTION'")

    # 添加 'COMMENT_REPLY' 和 'WORK_FAVORITED' 值到 notificationtype ENUM 类型
    op.execute("ALTER TYPE notificationtype ADD VALUE IF NOT EXISTS 'COMMENT_REPLY'")
    op.execute("ALTER TYPE notificationtype ADD VALUE IF NOT EXISTS 'WORK_FAVORITED'")


def downgrade() -> None:
    # PostgreSQL 不支持直接从 ENUM 中删除值
    # 需要创建新类型、迁移数据、删除旧类型、重命名新类型
    # 这里暂不实现降级，因为删除 ENUM 值比较复杂且可能导致数据丢失
    pass
