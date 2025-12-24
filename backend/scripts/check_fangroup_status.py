"""
检查粉丝群的 is_permanent 状态
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sqlalchemy import select
from app.core.database import async_session_maker
from app.models.channel import Channel


async def check_fangroups():
    """检查所有粉丝群的永久状态"""
    async with async_session_maker() as session:
        result = await session.execute(
            select(Channel).where(Channel.type == 'fangroup').order_by(Channel.created_at.desc())
        )
        fangroups = result.scalars().all()

        print(f"\n找到 {len(fangroups)} 个粉丝群:\n")
        for channel in fangroups:
            print(f"名称: {channel.name}")
            print(f"ID: {channel.id}")
            print(f"is_permanent: {channel.is_permanent}")
            print(f"创建时间: {channel.created_at}")
            print("-" * 50)


if __name__ == "__main__":
    asyncio.run(check_fangroups())
