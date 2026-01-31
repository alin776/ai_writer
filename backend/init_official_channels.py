"""
初始化官方频道脚本

创建4个默认的官方频道：
1. 公共酒馆
2. 作者酒馆
3. 读者茶馆
4. 官方实验室
"""
import asyncio
import sys
import uuid
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy import select
from app.core.database import async_session_maker
from app.models.channel import Channel, ChannelType, ChannelStatus
# 导入所有模型以避免关系解析错误
from app.models import *


official_channels = [
    {
        "id": uuid.uuid4(),
        "name": "公共酒馆",
        "description": "所有读者和作者交流的地方，欢迎大家畅所欲言！",
        "type": ChannelType.OFFICIAL,
        "status": ChannelStatus.ACTIVE,
        "is_permanent": True,
        "is_pinned": False,
    },
    {
        "id": uuid.uuid4(),
        "name": "作者酒馆",
        "description": "作者专属交流空间，分享创作经验和心得",
        "type": ChannelType.OFFICIAL,
        "status": ChannelStatus.ACTIVE,
        "is_permanent": True,
        "is_pinned": False,
    },
    {
        "id": uuid.uuid4(),
        "name": "读者茶馆",
        "description": "读者们的聚集地，推荐好书、交流阅读感受",
        "type": ChannelType.OFFICIAL,
        "status": ChannelStatus.ACTIVE,
        "is_permanent": True,
        "is_pinned": False,
    },
    {
        "id": uuid.uuid4(),
        "name": "官方实验室",
        "description": "新功能试用、问题反馈、建议征集",
        "type": ChannelType.OFFICIAL,
        "status": ChannelStatus.ACTIVE,
        "is_permanent": True,
        "is_pinned": False,
    },
]


async def init_channels():
    """初始化官方频道"""
    async with async_session_maker() as session:
        # 检查是否已经存在官方频道
        result = await session.execute(
            select(Channel).where(Channel.type == ChannelType.OFFICIAL)
        )
        existing_channels = result.scalars().all()

        if existing_channels:
            print(f"已存在 {len(existing_channels)} 个官方频道，跳过初始化")
            print("现有频道:")
            for channel in existing_channels:
                print(f"  - {channel.name} (ID: {channel.id})")
            return

        # 创建官方频道
        print("正在创建官方频道...")
        for channel_data in official_channels:
            channel = Channel(**channel_data)
            session.add(channel)
            print(f"  创建频道: {channel.name}")

        await session.commit()
        print(f"\n成功创建 {len(official_channels)} 个官方频道!")

        # 验证
        result = await session.execute(
            select(Channel).where(Channel.type == ChannelType.OFFICIAL)
        )
        channels = result.scalars().all()
        print("\n创建的频道列表:")
        for channel in channels:
            print(f"  - {channel.name} (ID: {channel.id})")


if __name__ == "__main__":
    print("=" * 50)
    print("初始化官方频道")
    print("=" * 50)
    asyncio.run(init_channels())
    print("\n完成!")
