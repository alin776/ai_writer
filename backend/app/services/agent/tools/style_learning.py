"""
风格学习系统 (Style Learning System)

功能:
1. 从用户文本学习写作风格
2. 模仿用户风格生成内容
3. 风格迁移
4. 风格一致性检查

学习维度:
- 句式结构（长短句比例、句式类型）
- 词汇特征（常用词、专业术语、成语使用）
- 修辞手法（比喻、拟人、排比等）
- 叙事视角（第一人称/第三人称）
- 节奏韵律（语句节奏、段落长度）

使用场景:
- 续写时保持用户风格
- 批量生成时统一风格
- 多作者协作时风格统一
"""

from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from pydantic import BaseModel
from collections import Counter
import re
from app.utils.datetime_utils import get_utc_now


class StyleFeatures(BaseModel):
    """风格特征"""
    # 句式特征
    avg_sentence_length: float = 0.0  # 平均句长
    sentence_length_variance: float = 0.0  # 句长方差
    long_sentence_ratio: float = 0.0  # 长句比例
    short_sentence_ratio: float = 0.0  # 短句比例

    # 词汇特征
    vocabulary_richness: float = 0.0  # 词汇丰富度
    common_words: List[str] = []  # 常用词
    common_phrases: List[str] = []  # 常用短语
    idiom_usage: float = 0.0  # 成语使用频率

    # 修辞特征
    metaphor_count: int = 0  # 比喻数量
    personification_count: int = 0  # 拟人数量
    rhetorical_question_count: int = 0  # 反问数量

    # 标点特征
    exclamation_usage: float = 0.0  # 感叹号使用频率
    ellipsis_usage: float = 0.0  # 省略号使用频率
    comma_usage: float = 0.0  # 逗号使用频率

    # 叙事特征
    pov: Optional[str] = None  # first_person/third_person
    tense: Optional[str] = None  # past/present
    dialogue_ratio: float = 0.0  # 对话占比

    # 段落特征
    avg_paragraph_length: float = 0.0  # 平均段落长度
    paragraph_count: int = 0  # 段落数量


class StyleProfile(BaseModel):
    """风格档案"""
    user_id: str
    profile_name: str  # 档案名称
    features: StyleFeatures
    sample_count: int = 0  # 样本数量
    total_words: int = 0  # 总字数
    created_at: str
    updated_at: str
    confidence_score: float = 0.0  # 置信度 0-100


class StyleLearningSystem:
    """风格学习系统"""

    def __init__(self):
        """初始化风格学习系统"""
        self.profiles: Dict[str, StyleProfile] = {}

    # ==================== 风格分析 ====================

    def analyze_text(self, text: str) -> StyleFeatures:
        """
        分析文本风格特征

        Args:
            text: 文本内容

        Returns:
            StyleFeatures: 风格特征
        """
        # 分句
        sentences = self._split_sentences(text)

        # 分段
        paragraphs = text.split('\n\n')
        paragraphs = [p.strip() for p in paragraphs if p.strip()]

        # 句式特征
        sentence_lengths = [len(s) for s in sentences]
        avg_sentence_length = sum(sentence_lengths) / len(sentence_lengths) if sentence_lengths else 0

        import statistics
        sentence_variance = statistics.variance(sentence_lengths) if len(sentence_lengths) > 1 else 0

        long_sentences = [s for s in sentences if len(s) > 30]
        short_sentences = [s for s in sentences if len(s) <= 15]

        long_ratio = len(long_sentences) / len(sentences) if sentences else 0
        short_ratio = len(short_sentences) / len(sentences) if sentences else 0

        # 词汇特征
        words = self._tokenize(text)
        vocab_richness = len(set(words)) / len(words) if words else 0

        word_freq = Counter(words)
        common_words = [word for word, _ in word_freq.most_common(20)]

        # 成语检测
        idiom_count = self._count_idioms(text)
        idiom_usage = idiom_count / len(sentences) if sentences else 0

        # 标点特征
        exclamation_count = text.count('!')
        ellipsis_count = text.count('...')
        comma_count = text.count('，')

        total_chars = len(text)
        exclamation_usage = exclamation_count / total_chars * 1000 if total_chars else 0
        ellipsis_usage = ellipsis_count / total_chars * 1000 if total_chars else 0
        comma_usage = comma_count / total_chars * 1000 if total_chars else 0

        # 叙事特征
        pov = self._detect_pov(text)
        dialogue_ratio = self._calculate_dialogue_ratio(text)

        # 段落特征
        para_lengths = [len(p) for p in paragraphs]
        avg_para_length = sum(para_lengths) / len(para_lengths) if para_lengths else 0

        return StyleFeatures(
            avg_sentence_length=round(avg_sentence_length, 2),
            sentence_length_variance=round(sentence_variance, 2),
            long_sentence_ratio=round(long_ratio, 2),
            short_sentence_ratio=round(short_ratio, 2),
            vocabulary_richness=round(vocab_richness, 2),
            common_words=common_words[:10],
            idiom_usage=round(idiom_usage, 2),
            exclamation_usage=round(exclamation_usage, 2),
            ellipsis_usage=round(ellipsis_usage, 2),
            comma_usage=round(comma_usage, 2),
            pov=pov,
            dialogue_ratio=round(dialogue_ratio, 2),
            avg_paragraph_length=round(avg_para_length, 2),
            paragraph_count=len(paragraphs)
        )

    def _split_sentences(self, text: str) -> List[str]:
        """分句"""
        # 简化版：按句号、问号、感叹号分句
        sentences = re.split(r'[。！？!?]', text)
        return [s.strip() for s in sentences if s.strip()]

    def _tokenize(self, text: str) -> List[str]:
        """分词（简化版）"""
        # 实际应该使用jieba等分词工具
        # 这里简化为按字符分割
        import re
        words = re.findall(r'[\u4e00-\u9fa5]+', text)
        return words

    def _count_idioms(self, text: str) -> int:
        """统计成语数量（简化版）"""
        # 简化版：检测4字词组
        pattern = r'[\u4e00-\u9fa5]{4}'
        matches = re.findall(pattern, text)
        # 实际应该使用成语词典匹配
        return len(matches) // 2  # 简化估计

    def _detect_pov(self, text: str) -> str:
        """检测人称视角"""
        first_person_words = ["我", "我们", "咱们"]
        third_person_words = ["他", "她", "它", "他们", "她们"]

        first_count = sum(text.count(word) for word in first_person_words)
        third_count = sum(text.count(word) for word in third_person_words)

        if first_count > third_count:
            return "first_person"
        elif third_count > 0:
            return "third_person"
        else:
            return "unknown"

    def _calculate_dialogue_ratio(self, text: str) -> float:
        """计算对话占比"""
        # 简化版：检测引号内容
        dialogue_pattern = r'"[^"]*"'
        dialogues = re.findall(dialogue_pattern, text)
        dialogue_chars = sum(len(d) for d in dialogues)

        return dialogue_chars / len(text) if len(text) > 0 else 0.0

    # ==================== 风格学习 ====================

    def learn_from_text(
        self,
        user_id: str,
        text: str,
        profile_name: str = "default"
    ) -> StyleProfile:
        """
        从文本学习用户风格

        Args:
            user_id: 用户ID
            text: 文本内容
            profile_name: 档案名称

        Returns:
            StyleProfile: 更新后的风格档案
        """
        profile_key = f"{user_id}:{profile_name}"

        # 分析新文本
        new_features = self.analyze_text(text)

        if profile_key in self.profiles:
            # 更新现有档案
            profile = self.profiles[profile_key]
            profile.features = self._merge_features(
                profile.features,
                new_features,
                profile.sample_count
            )
            profile.sample_count += 1
            profile.total_words += len(text)
            profile.updated_at = get_utc_now().isoformat()

        else:
            # 创建新档案
            profile = StyleProfile(
                user_id=user_id,
                profile_name=profile_name,
                features=new_features,
                sample_count=1,
                total_words=len(text),
                created_at=get_utc_now().isoformat(),
                updated_at=get_utc_now().isoformat()
            )
            self.profiles[profile_key] = profile

        # 更新置信度
        profile.confidence_score = self._calculate_confidence(profile)

        return profile

    def _merge_features(
        self,
        old_features: StyleFeatures,
        new_features: StyleFeatures,
        old_sample_count: int
    ) -> StyleFeatures:
        """
        合并风格特征（加权平均）

        Args:
            old_features: 旧特征
            new_features: 新特征
            old_sample_count: 旧样本数量

        Returns:
            StyleFeatures: 合并后的特征
        """
        weight_old = old_sample_count
        weight_new = 1
        total_weight = weight_old + weight_new

        def weighted_avg(old_val: float, new_val: float) -> float:
            return (old_val * weight_old + new_val * weight_new) / total_weight

        # 合并数值特征
        merged = StyleFeatures(
            avg_sentence_length=weighted_avg(
                old_features.avg_sentence_length,
                new_features.avg_sentence_length
            ),
            sentence_length_variance=weighted_avg(
                old_features.sentence_length_variance,
                new_features.sentence_length_variance
            ),
            long_sentence_ratio=weighted_avg(
                old_features.long_sentence_ratio,
                new_features.long_sentence_ratio
            ),
            short_sentence_ratio=weighted_avg(
                old_features.short_sentence_ratio,
                new_features.short_sentence_ratio
            ),
            vocabulary_richness=weighted_avg(
                old_features.vocabulary_richness,
                new_features.vocabulary_richness
            ),
            idiom_usage=weighted_avg(
                old_features.idiom_usage,
                new_features.idiom_usage
            ),
            exclamation_usage=weighted_avg(
                old_features.exclamation_usage,
                new_features.exclamation_usage
            ),
            dialogue_ratio=weighted_avg(
                old_features.dialogue_ratio,
                new_features.dialogue_ratio
            ),
            avg_paragraph_length=weighted_avg(
                old_features.avg_paragraph_length,
                new_features.avg_paragraph_length
            )
        )

        # 合并列表特征（取并集）
        merged.common_words = list(set(old_features.common_words + new_features.common_words))[:10]

        # 取最常见的POV
        merged.pov = new_features.pov or old_features.pov

        return merged

    def _calculate_confidence(self, profile: StyleProfile) -> float:
        """计算置信度"""
        # 基于样本数量和字数
        sample_score = min(profile.sample_count * 10, 50)
        word_score = min(profile.total_words / 100, 50)

        return sample_score + word_score

    # ==================== 风格应用 ====================

    def get_style_guidance(
        self,
        user_id: str,
        profile_name: str = "default"
    ) -> str:
        """
        获取风格指导（用于Prompt）

        Args:
            user_id: 用户ID
            profile_name: 档案名称

        Returns:
            str: 风格指导文本
        """
        profile_key = f"{user_id}:{profile_name}"
        profile = self.profiles.get(profile_key)

        if not profile:
            return "保持自然的写作风格。"

        features = profile.features
        guidance_parts = []

        # 句式指导
        if features.avg_sentence_length > 25:
            guidance_parts.append(f"使用较长的句子，平均{features.avg_sentence_length:.0f}字左右")
        elif features.avg_sentence_length < 15:
            guidance_parts.append("使用简短的句子")

        if features.long_sentence_ratio > 0.3:
            guidance_parts.append(f"包含{features.long_sentence_ratio*100:.0f}%的长句")

        # 叙事视角
        if features.pov == "first_person":
            guidance_parts.append("使用第一人称叙述")
        elif features.pov == "third_person":
            guidance_parts.append("使用第三人称叙述")

        # 对话占比
        if features.dialogue_ratio > 0.3:
            guidance_parts.append(f"包含较多对话（约{features.dialogue_ratio*100:.0f}%）")

        # 标点使用
        if features.exclamation_usage > 5:
            guidance_parts.append("适当使用感叹号表达情绪")

        if features.ellipsis_usage > 3:
            guidance_parts.append("使用省略号营造氛围")

        # 段落风格
        if features.avg_paragraph_length > 200:
            guidance_parts.append("使用较长的段落")
        elif features.avg_paragraph_length < 100:
            guidance_parts.append("使用简短的段落")

        # 词汇风格
        if features.common_words:
            common_words_str = "、".join(features.common_words[:5])
            guidance_parts.append(f"常用词汇：{common_words_str}")

        guidance = "；".join(guidance_parts) + "。"

        return f"写作风格要求：{guidance}"

    def compare_styles(
        self,
        user_id: str,
        profile1: str,
        profile2: str
    ) -> Dict[str, Any]:
        """
        比较两个风格档案

        Args:
            user_id: 用户ID
            profile1: 档案1名称
            profile2: 档案2名称

        Returns:
            Dict: 比较结果
        """
        key1 = f"{user_id}:{profile1}"
        key2 = f"{user_id}:{profile2}"

        p1 = self.profiles.get(key1)
        p2 = self.profiles.get(key2)

        if not p1 or not p2:
            return {"error": "档案不存在"}

        f1 = p1.features
        f2 = p2.features

        differences = []

        # 比较句长
        if abs(f1.avg_sentence_length - f2.avg_sentence_length) > 5:
            differences.append({
                "aspect": "句子长度",
                "profile1": f1.avg_sentence_length,
                "profile2": f2.avg_sentence_length,
                "difference": abs(f1.avg_sentence_length - f2.avg_sentence_length)
            })

        # 比较视角
        if f1.pov != f2.pov:
            differences.append({
                "aspect": "叙事视角",
                "profile1": f1.pov,
                "profile2": f2.pov
            })

        # 比较对话比例
        if abs(f1.dialogue_ratio - f2.dialogue_ratio) > 0.1:
            differences.append({
                "aspect": "对话占比",
                "profile1": f"{f1.dialogue_ratio*100:.1f}%",
                "profile2": f"{f2.dialogue_ratio*100:.1f}%"
            })

        similarity_score = 100 - min(len(differences) * 20, 100)

        return {
            "similarity_score": similarity_score,
            "differences": differences,
            "recommendation": "风格差异较大" if similarity_score < 60 else "风格较为接近"
        }

    # ==================== 风格管理 ====================

    def get_profile(
        self,
        user_id: str,
        profile_name: str = "default"
    ) -> Optional[StyleProfile]:
        """获取风格档案"""
        profile_key = f"{user_id}:{profile_name}"
        return self.profiles.get(profile_key)

    def list_profiles(self, user_id: str) -> List[StyleProfile]:
        """列出用户的所有风格档案"""
        return [
            profile for key, profile in self.profiles.items()
            if profile.user_id == user_id
        ]

    def delete_profile(self, user_id: str, profile_name: str):
        """删除风格档案"""
        profile_key = f"{user_id}:{profile_name}"
        if profile_key in self.profiles:
            del self.profiles[profile_key]


# ==================== 全局实例 ====================

global_style_system = StyleLearningSystem()


# ==================== 便捷函数 ====================

def learn_user_style(user_id: str, text: str, profile_name: str = "default") -> StyleProfile:
    """学习用户风格"""
    return global_style_system.learn_from_text(user_id, text, profile_name)


def get_style_prompt(user_id: str, profile_name: str = "default") -> str:
    """获取风格Prompt"""
    return global_style_system.get_style_guidance(user_id, profile_name)


def analyze_writing_style(text: str) -> StyleFeatures:
    """分析写作风格"""
    return global_style_system.analyze_text(text)
