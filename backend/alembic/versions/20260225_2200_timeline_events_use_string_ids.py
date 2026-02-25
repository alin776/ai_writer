"""timeline_events_use_string_ids

将 timeline_events 表的 entity_id/chapter_id 从 UUID 改为 VARCHAR(64)，
移除 chapter_id → chapters.id 的 FK 约束，与 FS 章节架构对齐。

Revision ID: timeline_events_use_string_ids
Revises: chapter_comments_use_chapter_num
Create Date: 2026-02-25 22:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = "timeline_events_use_string_ids"
down_revision = "chapter_comments_use_chapter_num"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. 删除 chapter_id 的 FK 约束（FS 迁移后章节不再存于 chapters 表）
    op.drop_constraint(
        "timeline_events_chapter_id_fkey", "timeline_events", type_="foreignkey"
    )

    # 2. 删除旧索引（若存在；原始建表可能未创建这些索引）
    op.execute("DROP INDEX IF EXISTS idx_timeline_entity")
    op.execute("DROP INDEX IF EXISTS idx_timeline_chapter")

    # 3. 将 entity_id 从 UUID 改为 VARCHAR(64)
    op.alter_column(
        "timeline_events",
        "entity_id",
        existing_type=UUID(as_uuid=True),
        type_=sa.String(64),
        existing_nullable=False,
        postgresql_using="entity_id::text",
    )

    # 4. 将 chapter_id 从 UUID 改为 VARCHAR(64)
    op.alter_column(
        "timeline_events",
        "chapter_id",
        existing_type=UUID(as_uuid=True),
        type_=sa.String(64),
        existing_nullable=True,
        postgresql_using="chapter_id::text",
    )

    # 5. 重建索引
    op.create_index("idx_timeline_entity", "timeline_events", ["entity_id", "entity_type"])
    op.create_index("idx_timeline_chapter", "timeline_events", ["chapter_id"])


def downgrade() -> None:
    # 删除索引
    op.drop_index("idx_timeline_chapter", table_name="timeline_events")
    op.drop_index("idx_timeline_entity", table_name="timeline_events")

    # 恢复 entity_id 为 UUID（非 UUID 格式的数据会丢失）
    op.execute("""
        DELETE FROM timeline_events
        WHERE entity_id !~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    """)
    op.alter_column(
        "timeline_events",
        "entity_id",
        existing_type=sa.String(64),
        type_=UUID(as_uuid=True),
        existing_nullable=False,
        postgresql_using="entity_id::uuid",
    )

    # 恢复 chapter_id 为 UUID
    op.execute("""
        UPDATE timeline_events SET chapter_id = NULL
        WHERE chapter_id IS NOT NULL
          AND chapter_id !~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    """)
    op.alter_column(
        "timeline_events",
        "chapter_id",
        existing_type=sa.String(64),
        type_=UUID(as_uuid=True),
        existing_nullable=True,
        postgresql_using="chapter_id::uuid",
    )

    # 恢复索引
    op.create_index("idx_timeline_entity", "timeline_events", ["entity_id", "entity_type"])
    op.create_index("idx_timeline_chapter", "timeline_events", ["chapter_id"])

    # 恢复 FK 约束
    op.create_foreign_key(
        "timeline_events_chapter_id_fkey",
        "timeline_events",
        "chapters",
        ["chapter_id"],
        ["id"],
        ondelete="SET NULL",
    )
