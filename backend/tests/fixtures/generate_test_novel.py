"""
测试小说数据生成器

生成不同规模的测试小说,用于性能压测
"""
import asyncio
import sys
from pathlib import Path
from datetime import datetime
from uuid import uuid4

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.core.database import AsyncSessionLocal
from app.models.user import User
from app.models.work import Work, WorkStatus
from app.models.chapter import Chapter
from sqlalchemy import select
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestNovelGenerator:
    """测试小说生成器"""

    def __init__(self):
        self.test_user_email = "test_performance@example.com"
        self.test_user_id = None

    async def get_or_create_test_user(self, db) -> str:
        """获取或创建测试用户"""
        result = await db.execute(
            select(User).where(User.email == self.test_user_email)
        )
        user = result.scalar_one_or_none()

        if not user:
            logger.info(f"创建测试用户: {self.test_user_email}")
            user = User(
                email=self.test_user_email,
                username="performance_tester",
                hashed_password="test_password_hash",  # 不重要,仅用于测试
                is_active=True
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)
            logger.info(f"✓ 测试用户已创建: {user.id}")
        else:
            logger.info(f"✓ 测试用户已存在: {user.id}")

        return str(user.id)

    def generate_chapter_content(self, chapter_num: int, words: int = 5000) -> str:
        """
        生成章节内容

        Args:
            chapter_num: 章节编号
            words: 字数 (约)

        Returns:
            章节内容文本
        """
        # 生成模板内容
        base_text = f"""
这是第{chapter_num}章的测试内容。本章讲述了主角在修炼之路上的又一次突破。

【场景描述】
天空中乌云密布,雷霆滚滚。主角盘膝而坐,周身灵气涌动,即将突破到更高的境界。

【对话】
"这就是传说中的天劫吗?"主角喃喃自语。
"不错,这是突破金丹期的必经之路。"师父在一旁提醒道。

【战斗场面】
突然,一道天雷劈下!主角运转全身灵力,凝聚成一道护盾。轰!巨大的冲击波向四周扩散。

【内心独白】
"我一定要成功!为了家族的荣耀,为了师父的期望!"主角咬紧牙关,继续抵抗天劫。

【情节转折】
就在这时,一个黑衣人出现在远处山头,冷冷地看着这一切。"桀桀桀,又一个送死的..."

【章节结尾】
经过三天三夜的苦战,主角终于成功突破,实力大增!但他不知道,更大的危机正在逼近...

"""
        # 重复内容直到达到目标字数
        repeat_times = max(1, words // len(base_text))
        content = (base_text + "\n" * 3) * repeat_times

        # 裁剪到目标字数
        return content[:words] + f"\n\n（第{chapter_num}章完）"

    async def generate_novel(
        self,
        db,
        title: str,
        chapter_count: int,
        words_per_chapter: int = 5000
    ) -> str:
        """
        生成测试小说

        Args:
            db: 数据库会话
            title: 小说标题
            chapter_count: 章节数
            words_per_chapter: 每章字数

        Returns:
            work_id: 作品ID
        """
        logger.info("=" * 60)
        logger.info(f"开始生成测试小说: {title}")
        logger.info(f"章节数: {chapter_count}, 每章字数: {words_per_chapter}")
        logger.info("=" * 60)

        # 1. 获取测试用户
        user_id = await self.get_or_create_test_user(db)

        # 2. 创建作品
        from app.models.work import WorkGenre

        work = Work(
            title=title,
            author_id=user_id,
            description=f"性能测试小说 - {chapter_count}章",
            status=WorkStatus.DRAFT,
            genre=WorkGenre.FANTASY,  # 使用枚举值
            total_words=chapter_count * words_per_chapter
        )
        db.add(work)
        await db.commit()
        await db.refresh(work)

        logger.info(f"✓ 作品已创建: {work.id}")

        # 3. 生成章节
        logger.info(f"正在生成 {chapter_count} 个章节...")

        for i in range(1, chapter_count + 1):
            content = self.generate_chapter_content(i, words_per_chapter)

            chapter = Chapter(
                work_id=str(work.id),
                title=f"第{i}章 修炼之路",
                content=content,
                order=i,
                word_count=len(content)
            )
            db.add(chapter)

            # 每100章提交一次
            if i % 100 == 0:
                await db.commit()
                logger.info(f"  ✓ 已生成 {i}/{chapter_count} 章")

        await db.commit()

        logger.info(f"✓ 所有章节已生成: {chapter_count} 章")
        logger.info(f"✓ 总字数: {chapter_count * words_per_chapter:,} 字")
        logger.info(f"✓ 作品ID: {work.id}")
        logger.info("=" * 60)

        return str(work.id)

    async def cleanup_test_data(self, db):
        """清理测试数据"""
        logger.info("清理测试数据...")

        # 获取测试用户
        result = await db.execute(
            select(User).where(User.email == self.test_user_email)
        )
        user = result.scalar_one_or_none()

        if not user:
            logger.info("未找到测试用户,无需清理")
            return

        # 获取测试用户的所有作品
        result = await db.execute(
            select(Work).where(Work.author_id == str(user.id))
        )
        works = result.scalars().all()

        # 删除作品和章节
        for work in works:
            # 删除章节
            result = await db.execute(
                select(Chapter).where(Chapter.work_id == str(work.id))
            )
            chapters = result.scalars().all()
            for chapter in chapters:
                await db.delete(chapter)

            # 删除作品
            await db.delete(work)
            logger.info(f"✓ 已删除作品: {work.title}")

        await db.commit()
        logger.info(f"✓ 清理完成,共删除 {len(works)} 部作品")


async def main():
    """主函数"""
    generator = TestNovelGenerator()

    async with AsyncSessionLocal() as db:
        print("\n" + "=" * 60)
        print("测试小说数据生成器")
        print("=" * 60)
        print("\n请选择操作:")
        print("1. 生成20章小说 (中篇)")
        print("2. 生成100章小说 (长篇)")
        print("3. 生成500章小说 (超长篇)")
        print("4. 生成全部测试数据 (20+100+500)")
        print("5. 清理测试数据")
        print("0. 退出")
        print()

        choice = input("请输入选项 (0-5): ").strip()

        try:
            if choice == "1":
                work_id = await generator.generate_novel(
                    db,
                    title="【性能测试】中篇小说20章",
                    chapter_count=20,
                    words_per_chapter=5000
                )
                print(f"\n✅ 成功! Work ID: {work_id}")

            elif choice == "2":
                work_id = await generator.generate_novel(
                    db,
                    title="【性能测试】长篇小说100章",
                    chapter_count=100,
                    words_per_chapter=5000
                )
                print(f"\n✅ 成功! Work ID: {work_id}")

            elif choice == "3":
                work_id = await generator.generate_novel(
                    db,
                    title="【性能测试】超长篇小说500章",
                    chapter_count=500,
                    words_per_chapter=4000
                )
                print(f"\n✅ 成功! Work ID: {work_id}")

            elif choice == "4":
                work_id_20 = await generator.generate_novel(
                    db,
                    title="【性能测试】中篇小说20章",
                    chapter_count=20,
                    words_per_chapter=5000
                )

                work_id_100 = await generator.generate_novel(
                    db,
                    title="【性能测试】长篇小说100章",
                    chapter_count=100,
                    words_per_chapter=5000
                )

                work_id_500 = await generator.generate_novel(
                    db,
                    title="【性能测试】超长篇小说500章",
                    chapter_count=500,
                    words_per_chapter=4000
                )

                print(f"\n✅ 全部生成成功!")
                print(f"  20章: {work_id_20}")
                print(f"  100章: {work_id_100}")
                print(f"  500章: {work_id_500}")

            elif choice == "5":
                confirm = input("⚠️  确认清理所有测试数据? (yes/no): ").strip().lower()
                if confirm == "yes":
                    await generator.cleanup_test_data(db)
                    print("\n✅ 清理完成!")
                else:
                    print("\n❌ 已取消")

            elif choice == "0":
                print("\n👋 再见!")

            else:
                print("\n❌ 无效选项")

        except Exception as e:
            logger.error(f"操作失败: {e}", exc_info=True)
            print(f"\n❌ 操作失败: {e}")


if __name__ == "__main__":
    asyncio.run(main())
