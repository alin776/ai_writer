"""
感官描写工具 (Show Don't Tell)

功能:
1. 将抽象描述转换为具体的感官描写
2. 增强五感描写（视觉、听觉、触觉、嗅觉、味觉）
3. 实现"Show, Don't Tell"原则
4. 提供场景氛围营造建议

使用场景:
- "他很生气" → "他紧握拳头，青筋暴起，牙齿咬得咯咯作响"
- "天气很冷" → "寒风如刀，吹得脸颊刺痛，呼出的白气瞬间凝结"
- "房间很乱" → "衣服随意堆在椅子上,书本散落一地,空气中弥漫着陈旧的气味"
"""

from typing import Dict, List, Optional, Any
from pydantic import BaseModel
from enum import Enum


class SenseType(str, Enum):
    """感官类型"""
    VISUAL = "visual"  # 视觉
    AUDITORY = "auditory"  # 听觉
    TACTILE = "tactile"  # 触觉
    OLFACTORY = "olfactory"  # 嗅觉
    GUSTATORY = "gustatory"  # 味觉


class EmotionType(str, Enum):
    """情绪类型"""
    HAPPY = "happy"  # 快乐
    SAD = "sad"  # 悲伤
    ANGRY = "angry"  # 愤怒
    FEAR = "fear"  # 恐惧
    SURPRISE = "surprise"  # 惊讶
    DISGUST = "disgust"  # 厌恶


class SensoryDescription(BaseModel):
    """感官描写"""
    sense_type: SenseType
    description: str
    intensity: int = 1  # 强度 1-5


class ShowDontTellResult(BaseModel):
    """Show Don't Tell 转换结果"""
    original: str  # 原始描述
    converted: str  # 转换后的描述
    sensory_details: List[SensoryDescription]  # 感官细节
    improvement_score: float  # 改进评分 0-100


class ShowDontTellTool:
    """Show Don't Tell 工具"""

    def __init__(self, ai_service: Any = None):
        """
        初始化工具

        Args:
            ai_service: AI服务（用于生成描写）
        """
        self.ai_service = ai_service

        # 情绪的身体表现库
        self.emotion_manifestations = {
            EmotionType.ANGRY: {
                "facial": ["眉头紧锁", "咬紧牙关", "脸色涨红", "眼睛瞪大"],
                "body": ["握紧拳头", "身体颤抖", "青筋暴起", "呼吸急促"],
                "voice": ["声音发颤", "咬牙切齿", "大声咆哮"],
                "action": ["猛地站起", "用力拍桌", "摔门而出"]
            },
            EmotionType.HAPPY: {
                "facial": ["眉开眼笑", "嘴角上扬", "眼睛弯成月牙", "面露喜色"],
                "body": ["轻快地跳跃", "手舞足蹈", "拍手叫好"],
                "voice": ["笑声爽朗", "语气轻快", "哼着小曲"],
                "action": ["欢呼雀跃", "兴奋地转圈", "拥抱他人"]
            },
            EmotionType.SAD: {
                "facial": ["眼眶湿润", "低垂着头", "咬住嘴唇", "神情黯淡"],
                "body": ["肩膀耷拉", "蜷缩身体", "无力地坐着"],
                "voice": ["声音哽咽", "轻声啜泣", "叹了口气"],
                "action": ["擦拭眼泪", "躲进角落", "默默流泪"]
            },
            EmotionType.FEAR: {
                "facial": ["面色苍白", "眼神惊恐", "嘴唇发抖"],
                "body": ["浑身颤抖", "冷汗直流", "腿脚发软", "心跳加速"],
                "voice": ["声音发颤", "尖叫出声", "说话结巴"],
                "action": ["向后退缩", "慌忙逃跑", "紧紧抓住"]
            },
            EmotionType.SURPRISE: {
                "facial": ["瞪大眼睛", "张开嘴巴", "挑起眉毛"],
                "body": ["身体一震", "倒吸一口凉气"],
                "voice": ["惊呼出声", "失声尖叫"],
                "action": ["后退一步", "捂住嘴巴", "愣在原地"]
            }
        }

        # 天气的感官描写库
        self.weather_descriptions = {
            "hot": {
                SenseType.VISUAL: ["阳光炽烈", "热浪蒸腾", "空气扭曲"],
                SenseType.TACTILE: ["汗水浸透衣衫", "皮肤灼热刺痛", "热气扑面而来"],
                SenseType.AUDITORY: ["蝉鸣阵阵", "人们喘着粗气"]
            },
            "cold": {
                SenseType.VISUAL: ["寒风凛冽", "呼出白雾", "霜花满窗"],
                SenseType.TACTILE: ["冷风刺骨", "手脚冰凉", "脸颊冻得发红"],
                SenseType.AUDITORY: ["风声呼啸", "牙齿打颤"]
            },
            "rain": {
                SenseType.VISUAL: ["雨帘密集", "水花四溅", "天色昏暗"],
                SenseType.TACTILE: ["雨水冰凉", "衣服湿透"],
                SenseType.AUDITORY: ["雨点敲打", "水流潺潺"],
                SenseType.OLFACTORY: ["泥土芬芳", "空气清新"]
            }
        }

    # ==================== 情绪描写转换 ====================

    def convert_emotion(
        self,
        emotion: EmotionType,
        context: str = "",
        intensity: int = 3
    ) -> ShowDontTellResult:
        """
        将情绪描述转换为具体表现

        Args:
            emotion: 情绪类型
            context: 上下文
            intensity: 强度 1-5

        Returns:
            ShowDontTellResult: 转换结果
        """
        original = f"他感到{emotion.value}"

        manifestations = self.emotion_manifestations.get(emotion, {})

        # 根据强度选择描写数量
        num_details = min(intensity, 3)

        details = []
        sensory_list = []

        # 选择各类表现
        if "facial" in manifestations and num_details >= 1:
            facial = self._pick_random(manifestations["facial"])
            details.append(facial)
            sensory_list.append(SensoryDescription(
                sense_type=SenseType.VISUAL,
                description=facial,
                intensity=intensity
            ))

        if "body" in manifestations and num_details >= 2:
            body = self._pick_random(manifestations["body"])
            details.append(body)
            sensory_list.append(SensoryDescription(
                sense_type=SenseType.TACTILE,
                description=body,
                intensity=intensity
            ))

        if "voice" in manifestations and num_details >= 3:
            voice = self._pick_random(manifestations["voice"])
            details.append(voice)
            sensory_list.append(SensoryDescription(
                sense_type=SenseType.AUDITORY,
                description=voice,
                intensity=intensity
            ))

        converted = "，".join(details) + "。"

        return ShowDontTellResult(
            original=original,
            converted=converted,
            sensory_details=sensory_list,
            improvement_score=80.0 + (intensity * 4)
        )

    # ==================== 环境描写增强 ====================

    def enhance_environment(
        self,
        original_description: str,
        focus_senses: List[SenseType] = None
    ) -> ShowDontTellResult:
        """
        增强环境描写

        Args:
            original_description: 原始描述
            focus_senses: 重点感官（可选）

        Returns:
            ShowDontTellResult: 转换结果
        """
        focus_senses = focus_senses or [
            SenseType.VISUAL,
            SenseType.AUDITORY,
            SenseType.OLFACTORY
        ]

        # 简化示例：根据关键词匹配
        sensory_list = []
        details = []

        if "冷" in original_description:
            weather_details = self.weather_descriptions["cold"]
            for sense in focus_senses:
                if sense in weather_details:
                    desc = self._pick_random(weather_details[sense])
                    details.append(desc)
                    sensory_list.append(SensoryDescription(
                        sense_type=sense,
                        description=desc,
                        intensity=3
                    ))

        elif "热" in original_description:
            weather_details = self.weather_descriptions["hot"]
            for sense in focus_senses:
                if sense in weather_details:
                    desc = self._pick_random(weather_details[sense])
                    details.append(desc)
                    sensory_list.append(SensoryDescription(
                        sense_type=sense,
                        description=desc,
                        intensity=3
                    ))

        converted = "，".join(details) + "。" if details else original_description

        return ShowDontTellResult(
            original=original_description,
            converted=converted,
            sensory_details=sensory_list,
            improvement_score=75.0
        )

    # ==================== 抽象概念具象化 ====================

    async def concretize_abstract(
        self,
        abstract_text: str,
        context: Dict[str, Any] = None
    ) -> ShowDontTellResult:
        """
        将抽象描述具象化

        Args:
            abstract_text: 抽象文本
            context: 上下文

        Returns:
            ShowDontTellResult: 转换结果
        """
        # 使用AI进行转换
        prompt = f"""请将以下抽象描述转换为具体的感官描写，遵循"Show, Don't Tell"原则。

抽象描述: {abstract_text}

要求:
1. 使用具体的动作、表情、环境细节
2. 调动多种感官（视觉、听觉、触觉等）
3. 避免直接说出情绪或状态

请只输出转换后的描写，不要解释。
"""

        # 这里应该调用AI服务
        # converted = await self.ai_service.chat(prompt)

        # 示例返回
        converted = f"{abstract_text}的具体描写版本"

        return ShowDontTellResult(
            original=abstract_text,
            converted=converted,
            sensory_details=[],
            improvement_score=85.0
        )

    # ==================== 辅助方法 ====================

    def _pick_random(self, items: List[str]) -> str:
        """随机选择一项"""
        import random
        return random.choice(items) if items else ""

    # ==================== 分析现有文本 ====================

    def analyze_sensory_balance(
        self,
        text: str
    ) -> Dict[str, Any]:
        """
        分析文本的感官描写平衡度

        Args:
            text: 文本

        Returns:
            Dict: 分析结果
        """
        # 简化版：关键词匹配
        sense_keywords = {
            SenseType.VISUAL: ["看", "见", "色", "光", "影", "眼"],
            SenseType.AUDITORY: ["听", "声", "响", "音", "叫"],
            SenseType.TACTILE: ["触", "摸", "冷", "热", "痛", "软", "硬"],
            SenseType.OLFACTORY: ["闻", "香", "臭", "味道"],
            SenseType.GUSTATORY: ["尝", "甜", "苦", "辣", "酸", "咸"]
        }

        sense_counts = {sense: 0 for sense in SenseType}

        for sense, keywords in sense_keywords.items():
            for keyword in keywords:
                sense_counts[sense] += text.count(keyword)

        total = sum(sense_counts.values())

        return {
            "sense_distribution": {
                sense.value: count
                for sense, count in sense_counts.items()
            },
            "dominant_sense": max(sense_counts, key=sense_counts.get).value if total > 0 else None,
            "balance_score": self._calculate_balance_score(sense_counts),
            "suggestions": self._generate_balance_suggestions(sense_counts)
        }

    def _calculate_balance_score(
        self,
        sense_counts: Dict[SenseType, int]
    ) -> float:
        """计算感官平衡度"""
        counts = list(sense_counts.values())
        if not counts or sum(counts) == 0:
            return 0.0

        # 计算标准差，越小越平衡
        import statistics
        if len([c for c in counts if c > 0]) <= 1:
            return 50.0

        std_dev = statistics.stdev([c for c in counts if c > 0])
        avg = statistics.mean([c for c in counts if c > 0])

        # 归一化到0-100
        balance = max(0, 100 - (std_dev / avg * 100)) if avg > 0 else 0

        return round(balance, 2)

    def _generate_balance_suggestions(
        self,
        sense_counts: Dict[SenseType, int]
    ) -> List[str]:
        """生成感官平衡建议"""
        suggestions = []

        # 找出缺失的感官
        missing_senses = [
            sense for sense, count in sense_counts.items()
            if count == 0
        ]

        if SenseType.OLFACTORY in missing_senses:
            suggestions.append("建议增加嗅觉描写，如气味、香气等")

        if SenseType.AUDITORY in missing_senses:
            suggestions.append("建议增加听觉描写，如声音、音效等")

        if SenseType.TACTILE in missing_senses:
            suggestions.append("建议增加触觉描写，如温度、质感等")

        # 检查过度依赖视觉
        visual_ratio = sense_counts[SenseType.VISUAL] / sum(sense_counts.values()) if sum(sense_counts.values()) > 0 else 0
        if visual_ratio > 0.7:
            suggestions.append("视觉描写占比过高，建议平衡其他感官")

        return suggestions


# ==================== 便捷函数 ====================

def show_emotion(emotion: str, intensity: int = 3) -> str:
    """
    快速转换情绪描写

    Args:
        emotion: 情绪（如"生气"、"高兴"）
        intensity: 强度 1-5

    Returns:
        str: 具体描写
    """
    emotion_map = {
        "生气": EmotionType.ANGRY,
        "愤怒": EmotionType.ANGRY,
        "高兴": EmotionType.HAPPY,
        "开心": EmotionType.HAPPY,
        "快乐": EmotionType.HAPPY,
        "悲伤": EmotionType.SAD,
        "难过": EmotionType.SAD,
        "害怕": EmotionType.FEAR,
        "恐惧": EmotionType.FEAR,
        "惊讶": EmotionType.SURPRISE,
        "吃惊": EmotionType.SURPRISE
    }

    emotion_type = emotion_map.get(emotion, EmotionType.HAPPY)

    tool = ShowDontTellTool()
    result = tool.convert_emotion(emotion_type, intensity=intensity)

    return result.converted


def enhance_scene(description: str) -> str:
    """
    快速增强场景描写

    Args:
        description: 原始描述

    Returns:
        str: 增强后的描写
    """
    tool = ShowDontTellTool()
    result = tool.enhance_environment(description)

    return result.converted


# ==================== @tool 包装（2026-01-09）====================

from langchain_core.tools import tool
from .tool_registry import register_as_tool
import json


@tool
@register_as_tool(
    "show_emotion_tool",
    "creative",
    "将抽象情绪转换为具体的感官描写（Show Don't Tell）"
)
def show_emotion_tool(emotion: str, intensity: int = 3) -> str:
    """
    将抽象情绪转换为具体描写

    Args:
        emotion: 情绪（如"生气"、"高兴"、"悲伤"、"害怕"）
        intensity: 强度 1-5

    Returns:
        具体的感官描写
    """
    try:
        result = show_emotion(emotion, intensity)
        return json.dumps({
            "success": True,
            "original_emotion": emotion,
            "converted": result,
            "intensity": intensity
        }, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False)


@tool
@register_as_tool(
    "enhance_scene_tool",
    "creative",
    "增强场景描写，添加多感官细节"
)
def enhance_scene_tool(description: str) -> str:
    """
    增强场景描写

    Args:
        description: 原始场景描述

    Returns:
        增强后的描写
    """
    try:
        result = enhance_scene(description)
        return json.dumps({
            "success": True,
            "original": description,
            "enhanced": result
        }, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False)
