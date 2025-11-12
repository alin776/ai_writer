"""
NLP预处理器 - 基于规则的快速去痕迹

在AI改写前快速去除明显的AI痕迹，降低成本和提升效果。
灵感来源: CBIhalsen/text-rewriter (MIT License)

作者: AI Writer Team
创建时间: 2025-11-11
"""

import re
import logging
from typing import List, Tuple

logger = logging.getLogger(__name__)


class NLPPreprocessor:
    """NLP预处理器 - 在AI改写前快速去除明显痕迹"""

    # AI痕迹模式库 - 50+常见AI生成文本的特征
    AI_PATTERNS = {
        # 1. 套路化开头
        "客套开头": [
            "当然", "很高兴为您服务", "让我来", "我来帮您",
            "我很荣幸", "非常感谢您的提问", "感谢您的询问"
        ],

        # 2. AI常用过渡词
        "过渡词": [
            "首先，", "其次，", "再次，", "最后，", "第一，", "第二，", "第三，",
            "综上所述", "值得注意的是", "需要强调的是", "需要指出的是",
            "总而言之", "换句话说", "简而言之"
        ],

        # 3. 客套结尾
        "客套结尾": [
            "希望对您有帮助", "祝您", "如有其他问题",
            "欢迎继续咨询", "期待为您服务", "随时为您服务"
        ],

        # 4. 过度正式的表达
        "正式表达": [
            "在此", "对此", "关于这一点", "就这个问题而言"
        ]
    }

    # 替换规则 - 将AI痕迹替换为更自然的表达或直接删除
    REPLACEMENTS = {
        # === 开头套话（直接删除）===
        "当然，": "",
        "当然": "",
        "很高兴为您服务。": "",
        "让我来": "",
        "我来帮您": "",
        "感谢您的询问，": "",
        "感谢您的提问，": "",

        # === 过渡词简化 ===
        "值得注意的是": "要注意",
        "需要强调的是": "重点是",
        "需要指出的是": "要说的是",
        "综上所述": "总的来说",
        "总而言之": "总之",
        "换句话说": "也就是说",
        "简而言之": "简单说",

        # === 结构词去除（常见的AI列表化表达）===
        "首先，": "",
        "其次，": "",
        "再次，": "",
        "最后，": "",
        "第一，": "",
        "第二，": "",
        "第三，": "",
        "第四，": "",

        # === 客套结尾（直接删除）===
        "希望对您有帮助": "",
        "希望这能帮到您": "",
        "如有其他问题": "",
        "欢迎继续咨询": "",
        "期待为您服务": "",

        # === 过度正式的表达（简化）===
        "在此": "这里",
        "对此": "对这",
        "关于这一点，": "",
        "就这个问题而言，": ""
    }

    def __init__(self):
        """初始化NLP预处理器"""
        self.total_processed = 0
        self.total_changes = 0
        logger.info("✅ NLP预处理器初始化完成，规则库包含 %d 条替换规则", len(self.REPLACEMENTS))

    def preprocess(self, text: str) -> Tuple[str, List[str]]:
        """
        预处理文本，去除AI痕迹

        Args:
            text: 原始文本

        Returns:
            (处理后文本, 修改记录列表)
        """
        if not text or len(text.strip()) == 0:
            return text, []

        changes = []
        original_length = len(text)

        # 1. 去除AI套路
        text = self._remove_ai_patterns(text, changes)

        # 2. 清理多余空格和标点
        text = self._clean_formatting(text, changes)

        # 3. 记录处理结果
        final_length = len(text)
        reduction = original_length - final_length

        # 统计
        self.total_processed += 1
        self.total_changes += len(changes)

        if reduction > 0:
            changes.append(f"总共减少{reduction}个字符")
            logger.debug(
                f"[NLP预处理] 原文长度={original_length}, "
                f"处理后={final_length}, 减少={reduction}, 修改={len(changes)}处"
            )

        return text, changes

    def _remove_ai_patterns(self, text: str, changes: List[str]) -> str:
        """去除AI模式"""
        for pattern, replacement in self.REPLACEMENTS.items():
            if pattern in text:
                count = text.count(pattern)
                text = text.replace(pattern, replacement)
                changes.append(f"去除'{pattern}' (共{count}处)")
                logger.debug(f"[NLP规则] 匹配到'{pattern}' {count}次，已替换")

        return text

    def _clean_formatting(self, text: str, changes: List[str]) -> str:
        """清理格式"""
        original = text

        # 1. 多个空格 → 单个空格
        text = re.sub(r' +', ' ', text)
        if text != original:
            changes.append("清理多余空格")
            original = text

        # 2. 句首空格
        text = re.sub(r'^\s+', '', text, flags=re.MULTILINE)

        # 3. 句尾空格
        text = re.sub(r'\s+$', '', text, flags=re.MULTILINE)

        # 4. 多个换行 → 双换行（保持段落间距）
        text = re.sub(r'\n{3,}', '\n\n', text)

        # 5. 去除句子开头的多余标点
        text = re.sub(r'^[，。、]', '', text, flags=re.MULTILINE)

        return text

    def get_statistics(self) -> dict:
        """获取预处理统计信息"""
        return {
            "total_processed": self.total_processed,
            "total_changes": self.total_changes,
            "avg_changes_per_text": (
                self.total_changes / self.total_processed
                if self.total_processed > 0
                else 0
            )
        }


# ========== 测试代码 ==========

if __name__ == "__main__":
    # 配置日志
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    preprocessor = NLPPreprocessor()

    # 测试用例1: 典型AI生成文本
    test_text_1 = """
    当然，首先我需要强调的是，这个问题非常重要。其次，我们应该值得注意的是，
    需要考虑多个因素。最后，综上所述，希望对您有帮助。
    """

    print("=" * 60)
    print("测试用例1: 典型AI生成文本")
    print("=" * 60)
    print(f"原文:\n{test_text_1.strip()}\n")

    result_1, changes_1 = preprocessor.preprocess(test_text_1)

    print(f"处理后:\n{result_1.strip()}\n")
    print("修改记录:")
    for i, change in enumerate(changes_1, 1):
        print(f"  {i}. {change}")

    # 测试用例2: 复杂的AI痕迹
    test_text_2 = """
    很高兴为您服务。关于您的问题，让我来详细解释一下。

    第一，我们需要理解基本概念。第二，需要指出的是，实践很重要。
    第三，值得注意的是，要保持耐心。

    总而言之，希望这能帮到您。如有其他问题，欢迎继续咨询。
    """

    print("\n" + "=" * 60)
    print("测试用例2: 复杂的AI痕迹")
    print("=" * 60)
    print(f"原文:\n{test_text_2.strip()}\n")

    result_2, changes_2 = preprocessor.preprocess(test_text_2)

    print(f"处理后:\n{result_2.strip()}\n")
    print("修改记录:")
    for i, change in enumerate(changes_2, 1):
        print(f"  {i}. {change}")

    # 统计信息
    print("\n" + "=" * 60)
    print("统计信息")
    print("=" * 60)
    stats = preprocessor.get_statistics()
    print(f"总处理次数: {stats['total_processed']}")
    print(f"总修改次数: {stats['total_changes']}")
    print(f"平均每次修改: {stats['avg_changes_per_text']:.2f}")
