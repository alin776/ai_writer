"""
实体验证器 - 检测AI是否编造实体
参考: OpenAI Hallucination Detection
"""
import re
import logging
from typing import Set, Dict, Any

try:
    import jieba.posseg as pseg
except ImportError:
    pseg = None
    logging.warning("jieba未安装，实体提取功能受限")

logger = logging.getLogger(__name__)


class EntityValidator:
    """
    实体验证器

    功能:
    1. 提取文本中的实体（人名、地名等）
    2. 对比AI输出和源文本的实体差异
    3. 检测AI是否编造了不存在的实体
    """

    @staticmethod
    def extract_entities(text: str) -> Set[str]:
        """
        提取文本中的实体（人名、地名等）

        使用jieba分词进行中文实体识别

        Args:
            text: 文本内容

        Returns:
            实体集合
        """
        entities = set()

        # 1. 使用jieba提取人名、地名
        if pseg:
            words = pseg.cut(text)
            for word, flag in words:
                if flag == 'nr':  # 人名
                    entities.add(word)
                elif flag == 'ns':  # 地名
                    entities.add(word)

        # 2. 提取引号中的内容（可能是重要实体）
        quoted = re.findall(r'["""](.*?)["""]', text)
        entities.update(quoted)

        # 3. 提取特殊标记的概念
        concepts = re.findall(r'[《「](.*?)[》」]', text)
        entities.update(concepts)

        # ❌ 4. 提取2-4字的中文名字（简单规则）- 已禁用
        # 原因：正则 r'[\u4e00-\u9fff]{2,4}(?=[说道告诉问答]|的|，)' 过于宽泛
        # 会误判大量普通词汇为实体，如："一个有效"、"严格遵守"、"于您提供"等
        # 导致90%的日志都是误报，掩盖真正的编造问题
        # jieba的词性标注已经足够准确，不需要这个正则
        # 修复日期: 2025-11-09
        # 参见: tasks/P1-1_entity_validator_fix.md
        # chinese_names = re.findall(r'[\u4e00-\u9fff]{2,4}(?=[说道告诉问答]|的|，)', text)
        # entities.update(chinese_names)

        return entities

    @classmethod
    def validate(cls, source_text: str, ai_output: str) -> Dict[str, Any]:
        """
        验证AI输出是否编造了实体

        核心逻辑:
        1. 提取源文本的实体
        2. 提取AI输出的实体
        3. 找出AI新增的实体
        4. 判断是否为编造

        Args:
            source_text: 源文本
            ai_output: AI输出

        Returns:
            {
                "valid": bool,
                "fabricated_entities": List[str],
                "confidence": float,
                ...
            }
        """
        source_entities = cls.extract_entities(source_text)
        output_entities = cls.extract_entities(ai_output)

        # ✅ 特殊情况1: 如果源文本很短（<50字符），放宽验证
        if len(source_text.strip()) < 50:
            return {
                "valid": True,
                "message": "源文本过短，跳过实体验证",
                "source_text_length": len(source_text.strip()),
                "warning": "源文本内容不足，建议检查数据完整性"
            }

        # ✅ 特殊情况2: AI明确表示内容为空
        empty_indicators = ['内容为空', '文本为空', '无法分析', '信息不足']
        if any(indicator in ai_output for indicator in empty_indicators):
            return {
                "valid": True,
                "message": "AI正确识别了内容缺失情况",
                "ai_feedback": "AI表明源文本内容不足"
            }

        # 找出AI输出中但源文本没有的实体
        fabricated_entities = output_entities - source_entities

        # 过滤常见分析用语（这些不算编造）
        common_words = {
            # 基础分析词汇
            '小说', '章节', '情节', '人物', '作者',
            '读者', '故事', '文本', '主角', '配角',
            '内容', '分析', '报告', '总结', '结论',

            # AI常见回复用语（防止误判）
            '提供', '具体', '分析', '无法', '不足',
            '缺少', '建议', '需要', '可以', '进行',
            '包含', '显示', '表明', '说明', '提到',

            # 特殊状态描述
            '内容为空', '文本为空', '信息不足', '数据不足',
            '内容', '文本', '信息', '数据', '细节',

            # 常见动词
            '写', '写作', '创作', '修改', '润色',
            '描写', '刻画', '展现', '体现', '反映',

            # 🔧 2025-12-02: P1修复 - 增加常见的分析和概括性词汇
            # 注意：只添加通用的分析词汇，不添加特定作品的角色名
            '关联', '深度', '高潮', '余波', '内省',
            '道德', '道德修养', '王朝',
            '关系', '冲突', '转折', '铺垫', '伏笔',
            '氛围', '张力', '节奏', '画面', '心理',
            '动作', '对话', '环境', '场景', '背景', '设定',
            '悬念', '线索', '矛盾', '发展', '结局', '开端',
            '叙事', '视角', '手法', '象征', '隐喻', '主题'
        }
        fabricated_entities = fabricated_entities - common_words

        # 过滤单字（误判率高）
        fabricated_entities = {e for e in fabricated_entities if len(e) > 1}

        if fabricated_entities:
            confidence = len(fabricated_entities) / max(len(output_entities), 1)

            # 🔧 2025-12-02: P1修复 - 提高容错阈值
            # 只有当编造比例超过30%时才判定为失败（原来是任何编造都失败）
            if confidence > 0.3:
                return {
                    "valid": False,
                    "error": "AI可能编造了以下实体",
                    "fabricated_entities": sorted(list(fabricated_entities)),
                    "source_entities": sorted(list(source_entities))[:10],  # 最多返回10个
                    "output_entities": sorted(list(output_entities))[:10],
                    "confidence": round(confidence, 2),
                    "recommendation": "重新生成或人工审查"
                }
            else:
                # 编造比例较低，给予警告但通过验证
                return {
                    "valid": True,
                    "warning": "AI输出包含少量新实体（可能是合理的概括）",
                    "fabricated_entities": sorted(list(fabricated_entities)),
                    "confidence": round(confidence, 2),
                    "message": "实体验证通过（容错模式）"
                }

        return {
            "valid": True,
            "message": "未发现明显的实体编造",
            "source_entities_count": len(source_entities),
            "output_entities_count": len(output_entities)
        }
