"""
直接使用SQL初始化官方频道脚本
检查并创建缺失的官方频道
"""
import asyncio
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy import text
from app.core.database import async_session_maker


# 官方频道定义
OFFICIAL_CHANNELS = [
    {
        'name': '公共酒馆',
        'description': '所有读者和作者交流的地方，欢迎大家畅所欲言！'
    },
    {
        'name': '作者酒馆',
        'description': '作者专属交流空间，分享创作经验和心得'
    },
    {
        'name': '读者茶馆',
        'description': '读者们的聚集地，推荐好书、交流阅读感受'
    },
    {
        'name': '官方实验室',
        'description': '新功能试用、问题反馈、建议征集'
    }
]


async def init_channels():
    """初始化官方频道 - 检查并创建缺失的频道"""
    async with async_session_maker() as session:
        print("检查官方频道...")

        # 获取现有的官方频道名称
        result = await session.execute(
            text("SELECT name FROM channels WHERE type = 'official'")
        )
        existing_names = {row[0] for row in result.fetchall()}

        print(f"现有官方频道: {existing_names if existing_names else '无'}")

        # 检查哪些频道需要创建
        channels_to_create = []
        for channel in OFFICIAL_CHANNELS:
            if channel['name'] not in existing_names:
                channels_to_create.append(channel)

        if not channels_to_create:
            print("\n✓ 所有官方频道都已存在，无需创建")
            # 显示现有频道
            result = await session.execute(
                text("SELECT id, name FROM channels WHERE type = 'official' ORDER BY created_at")
            )
            channels = result.fetchall()
            print("\n现有官方频道列表:")
            for channel_id, name in channels:
                print(f"  - {name} (ID: {channel_id})")
            return

        # 创建缺失的官方频道
        print(f"\n需要创建 {len(channels_to_create)} 个频道:")
        for channel in channels_to_create:
            print(f"  - {channel['name']}")

        print("\n正在创建...")
        created_count = 0

        for channel in channels_to_create:
            channel_id = uuid.uuid4()
            sql = text("""
                INSERT INTO channels
                (id, name, description, type, status, is_permanent, is_pinned, member_count, message_count, created_at, updated_at)
                VALUES
                (:id, :name, :description, 'official', 'active', true, false, 0, 0, NOW(), NOW())
            """)

            await session.execute(sql, {
                'id': channel_id,
                'name': channel['name'],
                'description': channel['description']
            })
            created_count += 1
            print(f"  ✓ 创建 '{channel['name']}' (ID: {channel_id})")

        await session.commit()
        print(f"\n成功创建 {created_count} 个官方频道!")

        # 显示所有官方频道
        result = await session.execute(
            text("SELECT id, name FROM channels WHERE type = 'official' ORDER BY created_at")
        )
        channels = result.fetchall()
        print("\n当前所有官方频道:")
        for channel_id, name in channels:
            print(f"  - {name} (ID: {channel_id})")


if __name__ == "__main__":
    print("=" * 50)
    print("初始化官方频道 (SQL方式)")
    print("=" * 50)
    asyncio.run(init_channels())
    print("\n完成!")
