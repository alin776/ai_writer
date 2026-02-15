"""
一次性脚本：将所有现有粉丝群改为非永久状态
"""
import asyncio
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sqlalchemy import select, update
from app.core.database import async_session_maker
from app.models.channel import Channel


async def update_fangroups():
    """将所有粉丝群改为非永久状态"""
    async with async_session_maker() as session:
        # 查询所有粉丝群
        result = await session.execute(
            select(Channel).where(Channel.type == 'fangroup')
        )
        fangroups = result.scalars().all()

        print(f"找到 {len(fangroups)} 个粉丝群")

        if not fangroups:
            print("没有需要更新的粉丝群")
            return

        # 更新所有粉丝群为非永久
        for channel in fangroups:
            old_status = channel.is_permanent
            channel.is_permanent = False
            print(f"  - {channel.name} (ID: {channel.id}): {old_status} -> False")

        await session.commit()
        print(f"\n✓ 成功更新 {len(fangroups)} 个粉丝群为非永久状态")


if __name__ == "__main__":
    asyncio.run(update_fangroups())
