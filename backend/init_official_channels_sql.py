"""
直接使用SQL初始化官方频道脚本
"""
import asyncio
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy import text
from app.core.database import async_session_maker


official_channels_sql = """
INSERT INTO channels (id, name, description, type, status, is_permanent, is_pinned, member_count, message_count, created_at, updated_at)
VALUES
    ('{id1}', '公共酒馆', '所有读者和作者交流的地方，欢迎大家畅所欲言！', 'official', 'active', true, false, 0, 0, NOW(), NOW()),
    ('{id2}', '作者酒馆', '作者专属交流空间，分享创作经验和心得', 'official', 'active', true, false, 0, 0, NOW(), NOW()),
    ('{id3}', '读者茶馆', '读者们的聚集地，推荐好书、交流阅读感受', 'official', 'active', true, false, 0, 0, NOW(), NOW()),
    ('{id4}', '官方实验室', '新功能试用、问题反馈、建议征集', 'official', 'active', true, false, 0, 0, NOW(), NOW())
ON CONFLICT DO NOTHING;
"""


async def init_channels():
    """初始化官方频道"""
    async with async_session_maker() as session:
        # 检查是否已经存在官方频道
        result = await session.execute(text("SELECT COUNT(*) FROM channels WHERE type = 'official'"))
        count = result.scalar()

        if count > 0:
            print(f"已存在 {count} 个官方频道，跳过初始化")
            # 显示现有频道
            result = await session.execute(text("SELECT id, name FROM channels WHERE type = 'official'"))
            channels = result.fetchall()
            print("现有频道:")
            for channel_id, name in channels:
                print(f"  - {name} (ID: {channel_id})")
            return

        # 创建官方频道
        print("正在创建官方频道...")
        ids = [uuid.uuid4() for _ in range(4)]
        sql = official_channels_sql.format(
            id1=ids[0],
            id2=ids[1],
            id3=ids[2],
            id4=ids[3]
        )

        await session.execute(text(sql))
        await session.commit()
        print(f"\n成功创建 4 个官方频道!")

        # 验证
        result = await session.execute(text("SELECT id, name FROM channels WHERE type = 'official'"))
        channels = result.fetchall()
        print("\n创建的频道列表:")
        for channel_id, name in channels:
            print(f"  - {name} (ID: {channel_id})")


if __name__ == "__main__":
    print("=" * 50)
    print("初始化官方频道 (SQL方式)")
    print("=" * 50)
    asyncio.run(init_channels())
    print("\n完成!")
