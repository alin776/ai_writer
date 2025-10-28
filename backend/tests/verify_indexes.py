"""验证索引是否成功添加"""
import asyncio
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.core.database import AsyncSessionLocal


async def verify_indexes():
    """验证缺失的索引是否已添加"""

    print("=" * 70)
    print("验证索引是否成功添加")
    print("=" * 70)
    print()

    async with AsyncSessionLocal() as db:
        # 查询所有索引
        query = """
        SELECT
            tablename,
            indexname
        FROM pg_indexes
        WHERE schemaname = 'public'
            AND indexname IN (
                'ix_entity_relationships_work_id',
                'ix_entity_relationships_source_id',
                'ix_entity_relationships_target_id',
                'ix_timeline_events_work_id'
            )
        ORDER BY indexname;
        """

        result = await db.execute(text(query))
        indexes = result.fetchall()

        print("检查新添加的索引:")
        print()

        expected_indexes = {
            'ix_entity_relationships_work_id': False,
            'ix_entity_relationships_source_id': False,
            'ix_entity_relationships_target_id': False,
            'ix_timeline_events_work_id': False,
        }

        for row in indexes:
            tablename, indexname = row
            print(f"  [OK] {indexname} (on {tablename})")
            expected_indexes[indexname] = True

        print()
        print("=" * 70)
        print("验证结果:")
        print("=" * 70)

        all_created = all(expected_indexes.values())
        created_count = sum(expected_indexes.values())

        if all_created:
            print(f"[SUCCESS] 所有 {len(expected_indexes)} 个索引都已成功创建!")
        else:
            print(f"[PARTIAL] {created_count}/{len(expected_indexes)} 个索引已创建")
            print()
            print("缺失的索引:")
            for idx, created in expected_indexes.items():
                if not created:
                    print(f"  [MISSING] {idx}")

        print()


if __name__ == "__main__":
    asyncio.run(verify_indexes())
