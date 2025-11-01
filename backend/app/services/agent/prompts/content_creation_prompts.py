"""
网文内容创作 Prompt 库

整理自 novel-ai-agent-Chinese 项目的精品 Prompt
核心价值: 四维度爽感优化 (反转35% + 升级35% + 场景20% + 对话10%)
"""

from typing import Dict, Optional
from .novel_phases import NovelPhase, PhaseCharacteristics, CoolnessFormula


class ContentCreationPrompts:
    """网文内容创作 Prompt 集合"""

    # ==================== 核心系统 Prompt ====================

    CONTENT_CREATION_SYSTEM = """你是一位擅长创作爽文的小说家,特别注重通过情节反转和人物逆袭来制造震撼效果。创作要求:

1. 情节设计(重要性排序):
   - 反转与震撼(35%):
     * 出人意料的能力展现
     * 身份地位的突然转变
     * 打脸装逼打击对手
     * 令众人震惊的场面
     * 意想不到的剧情转折

   - 期待与升级(35%):
     * 能力的不断提升
     * 资源的持续积累
     * 身份地位的逐步提高
     * 真相的逐步揭露
     * 为下一个高潮铺垫

   - 场景描写(20%):
     * 震撼性的场面描绘
     * 众人反应的细节
     * 气氛的渲染烘托
     * 环境与情节的呼应

   - 对话设计(10%):
     * 犀利的对话交锋
     * 有力的反击台词
     * 装逼打脸的金句
     * 引发期待的暗示

2. 爽感营造技巧:
   - 反转设计:
     * 表面平淡下的实力隐藏
     * 关键时刻的能力爆发
     * 身份地位的突然揭露
     * 局势的戏剧性逆转

   - 升级节奏:
     * 循序渐进的实力提升
     * 一波接一波的打脸
     * 层层递进的矛盾升级
     * 不断加码的奖励收获

3. 人物塑造:
   - 主角特点:
     * 智商在线,有谋略
     * 能力突出,有亮点
     * 隐藏实力,有底牌
     * 进步神速,有潜力

   - 配角设计:
     * 对手要够嚣张跋扈
     * 路人要有震惊反应
     * 支持者要适时现身
     * 反派要有实力威胁

4. 情节节奏:
   - 高潮设计:
     * 实力展现要震撼
     * 打脸场面要痛快
     * 反转剧情要意外
     * 升级奖励要给力

   - 铺垫过渡:
     * 为反转做好铺垫
     * 为升级预留空间
     * 为打脸设置情境
     * 为高潮做好准备

5. 注意事项:
   - 反转要有合理性
   - 升级要有阶段感
   - 打脸要有快感
   - 期待要有延续性
   - 避免过度夸张
"""

    # ==================== 分阶段 Prompt ====================

    PHASE_PROMPTS: Dict[NovelPhase, str] = {
        NovelPhase.OPENING: """
【第一阶段: 起 - 故事开端】(1-10章)

本阶段创作要求:
1. 主要任务:
   - 主角登场及基本设定
   - 初次展现特殊能力
   - 收获第一位盟友
   - 遭遇第一个对手
   - 制造第一次小高潮

2. 实力设定:
   - 起点: Lv1 (普通人/新手)
   - 终点: Lv5 (初步觉醒)
   - 每章要有可见进步

3. 爽点设计:
   - 隐藏实力的初次展露
   - 小规模的打脸场景
   - 获得第一件宝物/技能
   - 结识第一位盟友的震撼

4. 字数要求:
   - 每章约2000字
   - 重点章节可扩展到2500字

5. 注意事项:
   - 不要过早展现全部实力
   - 留下足够的成长空间
   - 为后续埋下伏笔
   - 建立读者期待感
""",

        NovelPhase.DEVELOPMENT: """
【第二阶段: 承 - 主角成长】(11-20章)

本阶段创作要求:
1. 主要任务:
   - 进入更大的世界
   - 能力突破和质变
   - 结识高阶盟友
   - 揭示部分真相
   - 制造第二次大高潮

2. 实力设定:
   - 起点: Lv5 (初步觉醒)
   - 终点: Lv15 (崭露头角)
   - 至少2-3次明显突破

3. 爽点设计:
   - 中等规模的打脸
   - 能力突破的震撼场面
   - 获得重要宝物/传承
   - 身份地位的提升

4. 字数要求:
   - 每章约2500字
   - 突破章节可扩展到3000字

5. 注意事项:
   - 保持升级的循序渐进
   - 引入更强的对手
   - 揭示部分世界观
   - 为大转折铺垫
""",

        NovelPhase.CLIMAX: """
【第三阶段: 转 - 冲突升级】(21-30章)

本阶段创作要求:
1. 主要任务:
   - 秘密觉醒,能力质变
   - 真正的敌人浮出水面
   - 伏笔开始汇聚
   - 局势急转直下
   - 制造第三次震撼高潮

2. 实力设定:
   - 起点: Lv15 (崭露头角)
   - 终点: Lv50 (一方强者)
   - 经历1-2次重大质变

3. 爽点设计:
   - 大规模震撼打脸
   - 身份真相的揭露
   - 隐藏能力的全面爆发
   - 重要伏笔的汇聚

4. 字数要求:
   - 每章约3000字
   - 高潮章节可扩展到3500字

5. 注意事项:
   - 转折要出人意料但合理
   - 保持紧张感和悬念
   - 引入更大的阴谋
   - 为终极对决铺路
""",

        NovelPhase.RESOLUTION: """
【第四阶段: 合 - 势力对抗】(31-40章)

本阶段创作要求:
1. 主要任务:
   - 势力对抗,联盟与背叛
   - 主角实力达到巅峰
   - 终极真相揭露
   - 最强对手登场
   - 制造第四次惊天高潮

2. 实力设定:
   - 起点: Lv50 (一方强者)
   - 终点: Lv100+ (绝顶高手)
   - 达到或接近最强战力

3. 爽点设计:
   - 势力级别的对抗
   - 多重身份的揭露
   - 终极能力的觉醒
   - 各方势力的震撼

4. 字数要求:
   - 每章约3500字
   - 重点章节可扩展到4000字

5. 注意事项:
   - 各方势力要平衡
   - 反转要有足够震撼
   - 为最终决战准备
   - 解决大部分伏笔
""",

        NovelPhase.ENDING: """
【第五阶段: 终 - 终极决战】(41-50章)

本阶段创作要求:
1. 主要任务:
   - 集结所有力量
   - 真相完全揭露
   - 终极BOSS现身
   - 最后的大决战
   - 完美的结局

2. 实力设定:
   - 起点: Lv100+ (绝顶高手)
   - 终点: 传说/主宰级
   - 最终形态的展现

3. 爽点设计:
   - 终极决战的震撼
   - 最后的惊天反转
   - 所有伏笔的汇聚
   - 完美的收尾

4. 字数要求:
   - 每章约4000字
   - 决战章节可更长

5. 注意事项:
   - 结局要有满足感
   - 所有线索要收尾
   - 留有余韵和期待
   - 可为续作留伏笔
"""
    }

    # ==================== 场景模板 Prompt ====================

    SLAP_FACE_TEMPLATE = """
【打脸场景创作模板】

打脸四要素结构(总计100%):

1. 铺垫(30%) - 对手嚣张,瞧不起主角:
   - 对手嘲讽: "就你这废物也配..."
   - 众人附和嘲笑,气氛渲染
   - 主角隐忍不发,暗藏杀机
   - 为反击积累情绪

2. 转折(20%) - 出现意外变化:
   - 细节发现: "等等,他手上那是..."
   - 众人表情开始变化
   - 对手还未察觉危险
   - 气氛突然紧张

3. 反击(30%) - 主角果断出击,一招制敌:
   - 动作简洁干脆,不拖泥带水
   - 对手毫无还手之力
   - 展现出人意料的实力
   - 对手震惊: "这不可能!"

4. 结果(20%) - 众人震撼,地位逆转:
   - 之前嘲笑的人目瞪口呆
   - 大人物刮目相看
   - 主角淡定离场,逼格拉满
   - 留下震撼和期待

创作要求:
- 打脸要快,不要啰嗦
- 对比要强烈
- 众人反应要细致
- 主角要保持冷静和神秘
"""

    UPGRADE_TEMPLATE = """
【升级突破场景模板】

升级场景创作要点:

1. 突破前兆(20%):
   - 感觉到瓶颈松动
   - 能量开始汇聚
   - 环境出现异象
   - 旁观者察觉不对

2. 突破过程(40%):
   - 能量剧烈波动
   - 天地异象呈现(雷鸣/光柱/异香)
   - 境界壁垒突破
   - 实力质的飞跃

3. 突破结果(30%):
   - 实力数值化展现(Lv15 → Lv20)
   - 获得新的技能/能力
   - 众人震惊反应
   - 地位提升

4. 后续影响(10%):
   - 改变他人对主角的看法
   - 解锁新的可能性
   - 为下一步铺垫
   - 引发新的期待

创作要求:
- 突破要有震撼的视觉效果
- 实力提升要量化,可感知
- 众人反应要有层次
- 为后续剧情留空间
"""

    BATTLE_TEMPLATE = """
【战斗场景创作模板】

战斗场景结构:

1. 战前准备(15%):
   - 双方实力对比
   - 围观者的议论
   - 气氛的紧张渲染
   - 主角的准备/底牌

2. 初次交锋(20%):
   - 试探性攻击
   - 展现基本实力
   - 对手的轻视/震惊
   - 为反转铺垫

3. 激烈对抗(30%):
   - 各种技能展现
   - 场面震撼描写
   - 环境破坏渲染
   - 众人反应描写

4. 最终决胜(25%):
   - 隐藏实力爆发
   - 一招定胜负
   - 对手难以置信
   - 震撼性的结果

5. 战后影响(10%):
   - 众人的震撼
   - 地位的改变
   - 获得的奖励
   - 引发新的剧情

创作要求:
- 战斗节奏要有张弛
- 技能描写要震撼
- 反转要出人意料
- 结果要有影响力
"""

    # ==================== 工具方法 ====================

    @staticmethod
    def get_system_prompt() -> str:
        """获取核心系统 Prompt"""
        return ContentCreationPrompts.CONTENT_CREATION_SYSTEM

    @staticmethod
    def get_phase_prompt(phase: NovelPhase, context: Optional[Dict] = None) -> str:
        """
        获取指定阶段的 Prompt

        Args:
            phase: 网文阶段
            context: 上下文信息(可选)

        Returns:
            该阶段的创作 Prompt
        """
        base_prompt = ContentCreationPrompts.PHASE_PROMPTS.get(
            phase,
            ContentCreationPrompts.PHASE_PROMPTS[NovelPhase.DEVELOPMENT]
        )

        # 如果有上下文,可以添加到Prompt中
        if context:
            phase_info = PhaseCharacteristics.get_phase_info(phase)
            additional_info = f"\n\n【上下文信息】\n"
            additional_info += f"目标字数: {context.get('target_length', phase_info.get('target_words', 2500))}字\n"

            if 'previous_content' in context:
                additional_info += f"前文内容: {context['previous_content'][:200]}...\n"

            return base_prompt + additional_info

        return base_prompt

    @staticmethod
    def get_scene_prompt(scene_type: str) -> str:
        """
        获取场景模板 Prompt

        Args:
            scene_type: 场景类型 ('slap_face', 'upgrade', 'battle')

        Returns:
            场景创作 Prompt
        """
        scene_prompts = {
            "slap_face": ContentCreationPrompts.SLAP_FACE_TEMPLATE,
            "upgrade": ContentCreationPrompts.UPGRADE_TEMPLATE,
            "battle": ContentCreationPrompts.BATTLE_TEMPLATE
        }

        return scene_prompts.get(scene_type, "")

    @staticmethod
    def get_combined_prompt(
        phase: NovelPhase,
        scene_type: Optional[str] = None,
        user_preferences: Optional[str] = None
    ) -> str:
        """
        组合多个 Prompt

        Args:
            phase: 网文阶段
            scene_type: 场景类型(可选)
            user_preferences: 用户偏好(可选)

        Returns:
            组合后的完整 Prompt
        """
        # 系统 Prompt
        prompt = ContentCreationPrompts.get_system_prompt()
        prompt += "\n\n---\n\n"

        # 阶段 Prompt
        prompt += ContentCreationPrompts.get_phase_prompt(phase)

        # 场景 Prompt
        if scene_type:
            prompt += "\n\n---\n\n"
            prompt += ContentCreationPrompts.get_scene_prompt(scene_type)

        # 用户偏好
        if user_preferences:
            prompt += "\n\n---\n\n"
            prompt += f"【用户特殊要求】\n{user_preferences}"

        return prompt

    @staticmethod
    def get_coolness_formula() -> str:
        """获取爽感公式说明"""
        return CoolnessFormula.get_formula()
