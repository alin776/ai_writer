"""
迁移脚本：为现有章节生成向量数据

用法：
    python scripts/migrate_chapter_vectors.py
"""
import asyncio
import logging
import sys
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import select
from app.core.database import async_session_maker
from app.models.chapter import Chapter
from app.services.chapter_vector_service import ChapterVectorService

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def migrate_existing_chapters():
    """迁移现有章节到新向量表"""

    async with async_session_maker() as db:
        try:
            logger.info("=" * 60)
            logger.info("开始迁移现有章节向量数据")
            logger.info("=" * 60)

            # 1. 查询所有有内容的章节
            stmt = select(Chapter).where(
                Chapter.content.isnot(None),
                Chapter.content != ""
            ).order_by(Chapter.work_id, Chapter.order)

            result = await db.execute(stmt)
            chapters = result.scalars().all()

            logger.info(f"找到 {len(chapters)} 个有内容的章节")

            if len(chapters) == 0:
                logger.info("没有需要迁移的章节")
                return

            # 2. 初始化向量服务
            vector_service = ChapterVectorService(db)

            # 3. 统计
            success_count = 0
            failed_count = 0
            skipped_count = 0
            failed_chapters = []

            # 4. 逐个处理章节
            for i, chapter in enumerate(chapters, 1):
                try:
                    # 检查内容长度
                    content_length = len(chapter.content.strip())

                    if content_length < 100:
                        logger.info(
                            f"[{i}/{len(chapters)}] 跳过: {chapter.title} "
                            f"(内容过短: {content_length}字符)"
                        )
                        skipped_count += 1
                        continue

                    # 向量化并存储
                    logger.info(
                        f"[{i}/{len(chapters)}] 处理中: {chapter.title} "
                        f"(order={chapter.order}, {content_length}字符)"
                    )

                    chunks_count = await vector_service.store_chapter_vector(
                        work_id=str(chapter.work_id),
                        chapter_id=str(chapter.id),
                        chapter_order=chapter.order,
                        chapter_title=chapter.title,
                        content=chapter.content
                    )

                    success_count += 1
                    logger.info(f"  ✅ 成功: 生成{chunks_count}个向量段落")

                except Exception as e:
                    failed_count += 1
                    error_msg = str(e)
                    logger.error(f"  ❌ 失败: {error_msg}")
                    failed_chapters.append({
                        'title': chapter.title,
                        'chapter_id': str(chapter.id),
                        'error': error_msg
                    })

            # 5. 输出迁移报告
            logger.info("=" * 60)
            logger.info("迁移完成")
            logger.info("=" * 60)
            logger.info(f"总计章节: {len(chapters)}")
            logger.info(f"成功迁移: {success_count}")
            logger.info(f"跳过章节: {skipped_count} (内容过短)")
            logger.info(f"失败章节: {failed_count}")

            if failed_chapters:
                logger.info("")
                logger.info("失败章节列表:")
                for fc in failed_chapters:
                    logger.info(f"  - {fc['title']} (ID: {fc['chapter_id']})")
                    logger.info(f"    错误: {fc['error']}")

            logger.info("=" * 60)

            # 6. 获取统计信息（验证迁移结果）
            if success_count > 0:
                # 随机抽取一个成功的章节验证
                sample_chapter = next(
                    (c for c in chapters if len(c.content.strip()) >= 100),
                    None
                )
                if sample_chapter:
                    stats = await vector_service.get_stats(str(sample_chapter.work_id))
                    logger.info(f"抽样验证 - 作品 {sample_chapter.work.title if sample_chapter.work else 'N/A'}:")
                    logger.info(f"  向量总数: {stats['total_vectors']}")
                    logger.info(f"  章节总数: {stats['total_chapters']}")
                    logger.info(f"  向量维度: {stats['vector_dimension']}")
                    logger.info(f"  模型名称: {stats['model_name']}")

        except Exception as e:
            logger.error(f"迁移过程发生错误: {e}", exc_info=True)
            raise


if __name__ == "__main__":
    try:
        asyncio.run(migrate_existing_chapters())
    except KeyboardInterrupt:
        logger.info("迁移被用户中断")
    except Exception as e:
        logger.error(f"迁移失败: {e}")
        sys.exit(1)
