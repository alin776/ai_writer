"""
清理旧版本的Redis缓存

由于缓存键从 novel_analysis:xxx 升级到 novel_analysis:v2:xxx
需要清理旧版本的缓存数据
"""
import asyncio
import redis.asyncio as redis
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def clear_old_cache():
    """清理旧版本缓存"""
    try:
        # 连接Redis
        r = redis.Redis(
            host="localhost",
            port=6379,
            db=0,
            decode_responses=True
        )

        await r.ping()
        logger.info("✓ Redis连接成功")

        # 查找旧版本的缓存键
        old_patterns = [
            "novel_analysis:micro:*",
            "novel_analysis:macro:*",
            "novel_analysis:book_breakdown:*"
        ]

        total_deleted = 0

        for pattern in old_patterns:
            logger.info(f"🔍 搜索模式: {pattern}")

            keys = []
            async for key in r.scan_iter(match=pattern):
                keys.append(key)

            if keys:
                deleted = await r.delete(*keys)
                logger.info(f"  ✓ 删除 {deleted} 个旧缓存键")
                total_deleted += deleted
            else:
                logger.info(f"  - 未找到匹配的键")

        logger.info(f"\n📊 总计删除: {total_deleted} 个旧缓存键")

        # 关闭连接
        await r.close()

    except Exception as e:
        logger.error(f"❌ 清理失败: {e}")
        raise


if __name__ == "__main__":
    print("=" * 60)
    print("清理旧版本Redis缓存")
    print("=" * 60)
    print()

    asyncio.run(clear_old_cache())

    print()
    print("✅ 清理完成!")
