"""
网文创作阶段定义

定义网文创作的五个阶段(起承转合终)和常见场景类型
参考: novel-ai-agent-Chinese 项目
"""

from enum import Enum
from typing import Dict, List


class NovelPhase(Enum):
    """网文创作的五个阶段"""

    OPENING = "opening"           # 起 - 故事开端 (1-10章)
    DEVELOPMENT = "development"   # 承 - 主角成长 (11-20章)
    CLIMAX = "climax"             # 转 - 冲突升级 (21-30章)
    RESOLUTION = "resolution"     # 合 - 势力对抗 (31-40章)
    ENDING = "ending"             # 终 - 终极决战 (41-50章)


class SceneType(Enum):
    """常见网文场景类型"""

    SLAP_FACE = "slap_face"       # 打脸场景
    UPGRADE = "upgrade"           # 升级突破
    BATTLE = "battle"             # 战斗场景
    REVEAL = "reveal"             # 真相揭露
    ALLIANCE = "alliance"         # 结盟
    BETRAYAL = "betrayal"         # 背叛反转
    TREASURE = "treasure"         # 获得宝物
    RECOGNITION = "recognition"   # 身份认可


class PhaseCharacteristics:
    """各阶段的特征和要求"""

    PHASE_FEATURES: Dict[NovelPhase, Dict] = {
        NovelPhase.OPENING: {
            "name": "起 - 故事开端",
            "chapters": (1, 10),
            "description": "引入主角和基本矛盾",
            "key_points": [
                "主角登场及基本设定",
                "初次展现特殊能力",
                "收获第一位盟友",
                "遭遇第一个对手",
                "第一次小高潮"
            ],
            "power_level": "Lv1 → Lv5",
            "target_words": 2000
        },
        NovelPhase.DEVELOPMENT: {
            "name": "承 - 主角成长",
            "chapters": (11, 20),
            "description": "主角成长,认识世界,收获盟友",
            "key_points": [
                "进入更大的世界",
                "能力突破 Lv5 → Lv15",
                "结识高阶盟友",
                "揭示部分真相",
                "第二次大高潮"
            ],
            "power_level": "Lv5 → Lv15",
            "target_words": 2500
        },
        NovelPhase.CLIMAX: {
            "name": "转 - 冲突升级",
            "chapters": (21, 30),
            "description": "冲突升级,秘密揭露,能力质变",
            "key_points": [
                "秘密觉醒,能力质变",
                "真正的敌人浮出水面",
                "伏笔开始汇聚",
                "局势急转直下",
                "第三次震撼高潮"
            ],
            "power_level": "Lv15 → Lv50",
            "target_words": 3000
        },
        NovelPhase.RESOLUTION: {
            "name": "合 - 势力对抗",
            "chapters": (31, 40),
            "description": "势力对抗,真相显现,决战前夕",
            "key_points": [
                "势力对抗,联盟与背叛",
                "主角实力巅峰 Lv50 → Lv100+",
                "终极真相揭露",
                "最强对手登场",
                "第四次惊天高潮"
            ],
            "power_level": "Lv50 → Lv100+",
            "target_words": 3500
        },
        NovelPhase.ENDING: {
            "name": "终 - 终极决战",
            "chapters": (41, 50),
            "description": "终极决战,尘埃落定,结局展望",
            "key_points": [
                "集结所有力量",
                "真相完全揭露",
                "终极BOSS现身",
                "最后的大决战",
                "完美的结局"
            ],
            "power_level": "Lv100+ → 传说",
            "target_words": 4000
        }
    }

    @classmethod
    def get_phase_info(cls, phase: NovelPhase) -> Dict:
        """获取阶段信息"""
        return cls.PHASE_FEATURES.get(phase, {})

    @classmethod
    def get_phase_by_chapter(cls, chapter_num: int) -> NovelPhase:
        """根据章节号获取对应阶段"""
        if 1 <= chapter_num <= 10:
            return NovelPhase.OPENING
        elif 11 <= chapter_num <= 20:
            return NovelPhase.DEVELOPMENT
        elif 21 <= chapter_num <= 30:
            return NovelPhase.CLIMAX
        elif 31 <= chapter_num <= 40:
            return NovelPhase.RESOLUTION
        elif 41 <= chapter_num <= 50:
            return NovelPhase.ENDING
        else:
            return NovelPhase.DEVELOPMENT  # 默认


class SlapFaceStructure:
    """打脸场景的四要素结构"""

    STRUCTURE = {
        "setup": {
            "weight": 0.30,
            "description": "铺垫 - 对手嚣张,瞧不起主角",
            "elements": [
                "对手嘲讽: '就你这废物也配...'",
                "众人附和嘲笑",
                "主角隐忍不发"
            ]
        },
        "twist": {
            "weight": 0.20,
            "description": "转折 - 出现意外变化",
            "elements": [
                "意外发现: '等等,他手上那是...'",
                "众人表情开始变化",
                "对手还未察觉"
            ]
        },
        "counter": {
            "weight": 0.30,
            "description": "反击 - 主角果断出击,一招秒杀",
            "elements": [
                "动作简洁干脆",
                "对手毫无还手之力",
                "震撼: '这不可能!'"
            ]
        },
        "result": {
            "weight": 0.20,
            "description": "结果 - 对手惊呆,众人膜拜",
            "elements": [
                "之前嘲笑的人震惊",
                "大人物刮目相看",
                "主角淡定离场"
            ]
        }
    }

    @classmethod
    def get_structure(cls) -> Dict:
        """获取打脸结构"""
        return cls.STRUCTURE


class CoolnessFormula:
    """爽感公式 - 四维度加权"""

    DIMENSIONS = {
        "reversal_shock": {
            "weight": 0.35,
            "name": "反转与震撼",
            "elements": [
                "出人意料的能力展现",
                "身份地位的突然转变",
                "打脸装逼打击对手",
                "令众人震惊的场面",
                "意想不到的剧情转折"
            ]
        },
        "expectation_upgrade": {
            "weight": 0.35,
            "name": "期待与升级",
            "elements": [
                "能力的不断提升",
                "资源的持续积累",
                "身份地位的逐步提高",
                "真相的逐步揭露",
                "为下一个高潮铺垫"
            ]
        },
        "scene_description": {
            "weight": 0.20,
            "name": "场景描写",
            "elements": [
                "震撼性的场面描绘",
                "众人反应的细节",
                "气氛的渲染烘托",
                "环境与情节的呼应"
            ]
        },
        "dialogue_design": {
            "weight": 0.10,
            "name": "对话设计",
            "elements": [
                "犀利的对话交锋",
                "有力的反击台词",
                "装逼打脸的金句",
                "引发期待的暗示"
            ]
        }
    }

    @classmethod
    def get_formula(cls) -> str:
        """获取爽感公式"""
        return "爽感 = 反转(35%) + 升级(35%) + 场景(20%) + 对话(10%)"

    @classmethod
    def get_dimension(cls, dimension_key: str) -> Dict:
        """获取维度信息"""
        return cls.DIMENSIONS.get(dimension_key, {})
