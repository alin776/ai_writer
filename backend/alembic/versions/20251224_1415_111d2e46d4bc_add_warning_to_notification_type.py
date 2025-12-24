"""add_warning_to_notification_type

Revision ID: 111d2e46d4bc
Revises: add_work_reports
Create Date: 2025-12-24 14:15:23.842866

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '111d2e46d4bc'
down_revision = 'add_work_reports'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 添加 'WARNING' 值到 notificationtype ENUM 类型（大写以匹配其他 enum 成员）
    op.execute("ALTER TYPE notificationtype ADD VALUE IF NOT EXISTS 'WARNING'")


def downgrade() -> None:
    # PostgreSQL 不支持直接从 ENUM 中删除值
    # 需要创建新类型、迁移数据、删除旧类型、重命名新类型
    # 这里暂不实现降级，因为删除 ENUM 值比较复杂且可能导致数据丢失
    pass
