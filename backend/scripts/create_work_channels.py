"""
为已发布作品补创建书友圈频道的迁移脚本

功能：
1. 查找所有 is_published=True 且没有对应频道的作品
2. 为每个作品创建书友圈频道
3. 将作者设为频道 owner
4. 将已收藏该作品的用户加入频道

用法：
cd backend
python scripts/create_work_channels.py
"""

import asyncio
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal
from app.models.work import Work
from app.models.channel import Channel
from app.models.channel_member import ChannelMember
from app.models.bookshelf import Bookshelf


async def create_work_channels():
    """为已发布作品创建书友圈频道"""

    async with AsyncSessionLocal() as db:
        # 查找所有已发布但没有频道的作品
        result = await db.execute(
            select(Work).where(
                Work.is_published == True
            ).outerjoin(
                Channel, Channel.work_id == Work.id
            ).where(
                Channel.id == None
            )
        )
        works_without_channel = result.scalars().all()

        print(f"找到 {len(works_without_channel)} 个已发布作品需要创建频道")

        created_count = 0
        member_count = 0

        for work in works_without_channel:
            print(f"\n处理作品: {work.title} (ID: {work.id})")

            # 创建频道
            channel = Channel(
                name=f"《{work.title}》书友圈",
                description=f"{work.title} 的读者交流群",
                type='work',
                status='active',
                creator_id=work.author_id,
                work_id=work.id,
                is_permanent=False,
                member_count=1,  # 初始只有作者
                cover_image=work.cover_image,  # 使用作品封面作为频道头像
            )
            db.add(channel)
            await db.flush()  # 获取 channel.id

            # 作者成为频道 owner
            owner_member = ChannelMember(
                channel_id=channel.id,
                user_id=work.author_id,
                role='owner',
                custom_title='作者',
                title_color='#FF6B6B'
            )
            db.add(owner_member)

            # 查找已收藏该作品的用户（排除作者自己）
            bookshelf_result = await db.execute(
                select(Bookshelf).where(
                    Bookshelf.work_id == work.id,
                    Bookshelf.user_id != work.author_id
                )
            )
            bookshelf_items = bookshelf_result.scalars().all()

            # 将收藏用户加入频道
            for item in bookshelf_items:
                member = ChannelMember(
                    channel_id=channel.id,
                    user_id=item.user_id,
                    role='member'
                )
                db.add(member)
                channel.member_count += 1
                member_count += 1

            created_count += 1
            print(f"  - 创建频道: {channel.name}")
            print(f"  - 添加 {len(bookshelf_items)} 个收藏用户为成员")

        await db.commit()

        print(f"\n===== 迁移完成 =====")
        print(f"创建频道数: {created_count}")
        print(f"添加成员数: {member_count}")


if __name__ == "__main__":
    asyncio.run(create_work_channels())
