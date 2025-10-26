"""
知识库测试数据生成脚本
创建8条示例知识条目用于测试
"""
import asyncio
import sys
from pathlib import Path

# 添加项目根目录到Python路径
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from uuid import uuid4

from app.core.config import settings
from app.models.knowledge_item import KnowledgeItem, KnowledgeCategory, KnowledgeSource
from app.models.user import User
from app.services.vector_store_service import VectorStoreService


async def create_test_data():
    """创建测试数据"""
    # 创建数据库引擎
    engine = create_async_engine(
        str(settings.DATABASE_URL),
        echo=True
    )

    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        # 1. 查找测试用户（假设存在username='test'的用户）
        from sqlalchemy import select
        result = await session.execute(select(User).where(User.username == "test"))
        user = result.scalar_one_or_none()

        if not user:
            print("❌ 未找到测试用户(username='test')，请先创建测试用户")
            return

        print(f"✅ 找到测试用户: {user.username} (ID: {user.id})")

        # 2. 创建8条测试数据
        test_items = [
            {
                "title": "修仙境界体系",
                "content": """完整的修仙境界划分：

                1. 练气期 - 入门境界，感知灵气
                2. 筑基期 - 建立修炼根基
                3. 金丹期 - 凝聚金丹，寿命大增
                4. 元婴期 - 元婴出窍，神通初显
                5. 化神期 - 化身千万，法力无边
                6. 返虚期 - 返璞归真
                7. 合体期 - 天人合一
                8. 大乘期 - 大道之巅
                9. 渡劫期 - 飞升前的最后考验

                每个大境界又分初期、中期、后期、圆满四个小境界。""",
                "category": KnowledgeCategory.WORLDVIEW,
                "tags": ["修仙", "境界体系", "设定"],
                "source_type": KnowledgeSource.MANUAL
            },
            {
                "title": "剑法描写 - 一剑光寒",
                "content": """他缓缓拔剑，剑身未出鞘，四周温度骤降。

                "嗡——"

                一声轻鸣，银光乍现。

                剑尖破空而出，在空中划出一道完美的弧线。那是极致的速度与力量的结合，快到肉眼难以捕捉，却又美得令人窒息。

                剑光所过之处，空气被撕裂，发出尖锐的呼啸声。地面上的落叶瞬间被剑气斩成齑粉，连石子都被震得崩飞。

                这一剑，快、准、狠，没有任何花哨，却蕴含着千锤百炼的剑道真意。""",
                "category": KnowledgeCategory.DESCRIPTION,
                "tags": ["武侠", "剑法", "动作戏", "场景描写"],
                "source_type": KnowledgeSource.MANUAL
            },
            {
                "title": "反派角色塑造技巧",
                "content": """优秀反派的五个关键要素：

                1. **合理的动机** - 反派的行为要有说服力，即使邪恶也要有其逻辑
                2. **复杂的性格** - 不是单纯的坏，要有多面性
                3. **强大的实力** - 能与主角抗衡，制造真实的威胁感
                4. **独特的魅力** - 让读者又恨又爱，甚至产生共鸣
                5. **成长弧线** - 反派也需要成长和变化

                示例：灭霸（复仇者联盟）- 动机是拯救宇宙，手段是消灭一半生命。这种扭曲的正义感让他成为经典反派。""",
                "category": KnowledgeCategory.TECHNIQUE,
                "tags": ["人物塑造", "反派", "写作技巧"],
                "source_type": KnowledgeSource.MANUAL
            },
            {
                "title": "对话 - 紧张场景中的交锋",
                "content": """"你以为自己赢了？"他冷笑一声。

                "难道不是吗？"她反问，手中的剑指向他的咽喉。

                "你杀了我，就永远找不到真相。"

                "那我也不需要了。"剑尖前移一寸。

                "等等！"他额头渗出冷汗，"你真的以为...你父亲的死，只是一场意外？"

                她的手颤抖了。就是这一刹那的犹豫，成为了转折点。

                **分析**:
                - 对话简短有力，每句话都推动剧情
                - 反转出现在最关键的时刻
                - 肢体动作穿插其中，画面感强""",
                "category": KnowledgeCategory.DIALOGUE,
                "tags": ["对话", "紧张", "反转"],
                "source_type": KnowledgeSource.MANUAL
            },
            {
                "title": "情节点 - 主角的至暗时刻",
                "content": """设计"至暗时刻"的三个层次：

                **外部危机** - 敌人占据绝对优势，主角陷入绝境
                **内部崩溃** - 信念动摇，怀疑自己的选择
                **关系破裂** - 失去重要的伙伴或亲人

                经典案例：
                1. 《星球大战5》- 卢克失去手臂，发现维达是父亲
                2. 《黑暗骑士》- 蝙蝠侠被全城通缉，哈维变成双面人
                3. 《权力的游戏》- 血色婚礼

                关键：至暗时刻后必须有转机或成长，否则故事就真的"黑暗"了。""",
                "category": KnowledgeCategory.PLOT,
                "tags": ["剧情", "转折点", "至暗时刻"],
                "source_type": KnowledgeSource.MANUAL
            },
            {
                "title": "科幻设定 - 时间旅行的逻辑",
                "content": """时间旅行的三大理论派别：

                **1. 固定时间线理论**
                - 过去无法改变，一切早已注定
                - 代表作品：《十二猴子》

                **2. 多重宇宙理论**
                - 改变过去会创建新的平行宇宙
                - 代表作品：《复仇者联盟4》

                **3. 动态时间线理论**
                - 改变过去会影响现在，但有一定容错性
                - 代表作品：《回到未来》

                选择理论要自洽，在故事中保持一致，不要前后矛盾。""",
                "category": KnowledgeCategory.WORLDVIEW,
                "tags": ["科幻", "时间旅行", "设定"],
                "source_type": KnowledgeSource.MANUAL
            },
            {
                "title": "参考资料 - 中国古代官职体系",
                "content": """唐朝官职结构（简化版）：

                **中央三省**
                - 中书省：负责起草诏令
                - 门下省：负责审核诏令
                - 尚书省：负责执行诏令

                **六部**
                - 吏部：管理官员任免
                - 户部：管理财政税收
                - 礼部：管理科举礼仪
                - 兵部：管理军事国防
                - 刑部：管理司法审判
                - 工部：管理建设工程

                **地方官**
                - 道：监察大区
                - 州/府：地方行政单位
                - 县：基层行政单位

                写历史小说或穿越文时可以参考此结构。""",
                "category": KnowledgeCategory.REFERENCE,
                "tags": ["历史", "古代官职", "参考"],
                "source_type": KnowledgeSource.MANUAL
            },
            {
                "title": "魔法体系 - 元素魔法设定",
                "content": """经典元素魔法系统：

                **基础四元素**
                - 火：攻击、爆裂、燃烧
                - 水：治疗、防御、流动
                - 风：速度、切割、飞行
                - 土：防御、束缚、力量

                **高级元素**
                - 光：神圣、治愈、净化
                - 暗：诅咒、腐蚀、隐匿
                - 雷：速度、破坏、麻痹
                - 冰：冻结、控制、防御

                **进阶设定**
                1. 元素相克：水克火、火克风、风克土、土克水
                2. 元素融合：火+风=爆炸、水+风=冰、土+水=泥沼
                3. 魔力来源：自然、信仰、血脉、契约

                建议：选择3-5种元素深入刻画，不要贪多。""",
                "category": KnowledgeCategory.WORLDVIEW,
                "tags": ["魔法", "元素", "体系设定", "奇幻"],
                "source_type": KnowledgeSource.MANUAL
            }
        ]

        # 3. 创建知识条目
        created_items = []
        vector_service = VectorStoreService(session)

        for item_data in test_items:
            item = KnowledgeItem(
                user_id=user.id,
                **item_data
            )
            session.add(item)
            await session.flush()

            # 生成向量
            try:
                await vector_service.add_knowledge(item)
                print(f"✅ 创建知识条目: {item.title}")
            except Exception as e:
                print(f"⚠️  向量生成失败: {e}")

            created_items.append(item)

        await session.commit()

        print(f"\n🎉 成功创建 {len(created_items)} 条测试数据!")
        print("\n测试数据列表:")
        for i, item in enumerate(created_items, 1):
            print(f"{i}. [{item.category.value}] {item.title}")
            print(f"   标签: {', '.join(item.tags)}")


if __name__ == "__main__":
    print("=" * 60)
    print("知识库测试数据生成脚本")
    print("=" * 60)
    print()

    asyncio.run(create_test_data())
