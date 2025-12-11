"""
历史数据迁移：为现有章节创建初始 delta 记录

运行方式：
    python scripts/migrate_chapter_word_stats.py

功能：
- 为每个现有章节创建一条 delta 记录，delta 值等于章节当前字数
- 使用章节的创建时间作为 delta 记录的创建时间
- 跳过已有 delta 记录的章节
"""
import asyncio
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import select, func
from app.core.database import AsyncSessionLocal
from app.models.chapter import Chapter
from app.models.chapter_word_stat import ChapterWordStat
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def migrate_existing_chapters():
    """为现有章节创建初始 delta 记录"""
    async with AsyncSessionLocal() as db:
        # 获取所有章节
        result = await db.execute(select(Chapter))
        chapters = result.scalars().all()

        logger.info(f"找到 {len(chapters)} 个章节")

        migrated = 0
        skipped = 0

        for chapter in chapters:
            # 检查是否已有 delta 记录
            result = await db.execute(
                select(func.count(ChapterWordStat.id))
                .where(ChapterWordStat.chapter_id == chapter.id)
            )
            existing_count = result.scalar()

            if existing_count > 0:
                logger.info(f"跳过章节 {chapter.id} (已有 {existing_count} 条记录)")
                skipped += 1
                continue

            # 创建初始 delta 记录
            word_count = chapter.word_count or 0
            if word_count > 0:
                stat = ChapterWordStat(
                    chapter_id=chapter.id,
                    delta=word_count,
                    created_at=chapter.created_at  # 使用章节的创建时间
                )
                db.add(stat)
                logger.info(f"为章节 {chapter.id} 创建 delta 记录: {word_count} 字")
                migrated += 1
            else:
                logger.info(f"跳过章节 {chapter.id} (字数为0)")
                skipped += 1

        await db.commit()

        logger.info(f"迁移完成: 已迁移 {migrated} 个章节, 跳过 {skipped} 个")


async def verify_migration():
    """验证迁移结果"""
    async with AsyncSessionLocal() as db:
        # 统计章节数
        result = await db.execute(select(func.count(Chapter.id)))
        chapter_count = result.scalar()

        # 统计delta记录数
        result = await db.execute(select(func.count(ChapterWordStat.id)))
        delta_count = result.scalar()

        # 统计总字数（从章节表）
        result = await db.execute(select(func.coalesce(func.sum(Chapter.word_count), 0)))
        total_words_chapters = result.scalar()

        # 统计总字数（从delta表）
        result = await db.execute(select(func.coalesce(func.sum(ChapterWordStat.delta), 0)))
        total_words_deltas = result.scalar()

        logger.info(f"验证结果:")
        logger.info(f"  章节总数: {chapter_count}")
        logger.info(f"  Delta记录数: {delta_count}")
        logger.info(f"  章节表总字数: {total_words_chapters}")
        logger.info(f"  Delta表总字数: {total_words_deltas}")

        if total_words_chapters == total_words_deltas:
            logger.info("✓ 字数统计一致")
        else:
            logger.warning(f"✗ 字数统计不一致，差异: {total_words_chapters - total_words_deltas}")


async def main():
    """主函数"""
    logger.info("开始历史数据迁移...")

    try:
        await migrate_existing_chapters()
        await verify_migration()
        logger.info("迁移成功完成!")
    except Exception as e:
        logger.error(f"迁移失败: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    asyncio.run(main())
