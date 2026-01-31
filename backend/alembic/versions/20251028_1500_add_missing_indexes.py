"""add missing performance indexes

Revision ID: add_missing_indexes
Revises: 1f19710e6576
Create Date: 2025-10-28 15:00:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision = 'add_missing_indexes'
down_revision = '1f19710e6576'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """添加缺失的性能索引

    基于数据库性能审查结果,添加5个缺失的索引:
    1. chapters.author_id (如果字段存在)
    2. entity_relationships.work_id
    3. entity_relationships.source_id
    4. entity_relationships.target_id
    5. timeline_events.work_id
    """

    conn = op.get_bind()
    inspector = inspect(conn)

    print("[INFO] 添加缺失的性能索引...")

    # 1. chapters.author_id (仅在字段存在时创建)
    try:
        chapters_columns = [c['name'] for c in inspector.get_columns('chapters')]
        if 'author_id' in chapters_columns:
            op.create_index(
                'ix_chapters_author_id',
                'chapters',
                ['author_id'],
                unique=False
            )
            print("[OK] 创建索引: ix_chapters_author_id")
        else:
            print("[SKIP] chapters表没有author_id字段,跳过")
    except Exception as e:
        print("[SKIP] 跳过索引 ix_chapters_author_id:", str(e))

    # 2. entity_relationships.work_id
    try:
        op.create_index(
            'ix_entity_relationships_work_id',
            'entity_relationships',
            ['work_id'],
            unique=False
        )
        print("[OK] 创建索引: ix_entity_relationships_work_id")
    except Exception as e:
        print("[SKIP] 跳过索引 ix_entity_relationships_work_id:", str(e))

    # 3. entity_relationships.source_id
    try:
        op.create_index(
            'ix_entity_relationships_source_id',
            'entity_relationships',
            ['source_id'],
            unique=False
        )
        print("[OK] 创建索引: ix_entity_relationships_source_id")
    except Exception as e:
        print("[SKIP] 跳过索引 ix_entity_relationships_source_id:", str(e))

    # 4. entity_relationships.target_id
    try:
        op.create_index(
            'ix_entity_relationships_target_id',
            'entity_relationships',
            ['target_id'],
            unique=False
        )
        print("[OK] 创建索引: ix_entity_relationships_target_id")
    except Exception as e:
        print("[SKIP] 跳过索引 ix_entity_relationships_target_id:", str(e))

    # 5. timeline_events.work_id
    try:
        op.create_index(
            'ix_timeline_events_work_id',
            'timeline_events',
            ['work_id'],
            unique=False
        )
        print("[OK] 创建索引: ix_timeline_events_work_id")
    except Exception as e:
        print("[SKIP] 跳过索引 ix_timeline_events_work_id:", str(e))

    print("[OK] 所有缺失索引添加完成!")


def downgrade() -> None:
    """删除添加的索引"""

    print("[INFO] 删除性能索引...")

    # 按相反顺序删除,使用if_exists避免错误
    try:
        op.drop_index('ix_timeline_events_work_id', table_name='timeline_events', if_exists=True)
    except:
        pass

    try:
        op.drop_index('ix_entity_relationships_target_id', table_name='entity_relationships', if_exists=True)
    except:
        pass

    try:
        op.drop_index('ix_entity_relationships_source_id', table_name='entity_relationships', if_exists=True)
    except:
        pass

    try:
        op.drop_index('ix_entity_relationships_work_id', table_name='entity_relationships', if_exists=True)
    except:
        pass

    try:
        op.drop_index('ix_chapters_author_id', table_name='chapters', if_exists=True)
    except:
        pass

    print("[OK] 索引删除完成!")
