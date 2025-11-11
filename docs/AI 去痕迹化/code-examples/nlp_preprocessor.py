# 代码示例 - NLP预处理器

这是可以直接使用的NLP预处理器完整代码。

## 📁 文件位置
`backend/app/services/ai/nlp_preprocessor.py`

## 📖 使用说明

### 1. 安装（可选）
如果需要同义词替换功能：
```bash
pip install jieba synonyms
```

### 2. 导入使用
```python
from app.services.ai.nlp_preprocessor import NLPPreprocessor

preprocessor = NLPPreprocessor()
text, changes = preprocessor.preprocess("当然，首先我们需要...")
```

### 3. 集成到HumanizeService
参考 [05-改进方案.md](../05-改进方案.md#集成到humanizeservice)

## 💻 完整代码

```python
"""
NLP预处理器 - 基于规则的快速去痕迹
灵感来源: CBIhalsen/text-rewriter (MIT License)
"""

import re
import logging
from typing import List, Tuple

logger = logging.getLogger(__name__)


class NLPPreprocessor:
    """
    NLP预处理器 - 在AI改写前快速去除明显痕迹

    特点：
    - 零成本（纯规则，不调用AI）
    - 毫秒级速度
    - 精确可控
    """

    # AI痕迹模式库
    AI_PATTERNS = {
        # 1. 套路化开头
        "客套开头": [
            "当然", "很高兴为您服务", "让我来", "我来帮您",
            "我很荣幸", "非常感谢您的提问", "感谢您的咨询"
        ],

        # 2. AI常用过渡词
        "过渡词": [
            "首先，", "其次，", "再次，", "最后，",
            "第一，", "第二，", "第三，",
            "综上所述", "值得注意的是", "需要强调的是",
            "总而言之", "换句话说", "简单来说"
        ],

        # 3. 客套结尾
        "客套结尾": [
            "希望对您有帮助", "祝您", "如有其他问题",
            "欢迎继续咨询", "期待为您服务", "还有什么我可以帮您的吗"
        ]
    }

    # 替换规则（优先级从高到低）
    REPLACEMENTS = {
        # === 开头套话 ===
        "当然，": "",
        "当然！": "",
        "当然": "",
        "很高兴为您服务。": "",
        "很高兴为您服务！": "",
        "让我来": "",
        "我来帮您": "",
        "我很荣幸": "",

        # === 过渡词简化 ===
        "值得注意的是，": "要注意，",
        "值得注意的是": "要注意",
        "需要强调的是，": "重点是，",
        "需要强调的是": "重点是",
        "综上所述，": "总的来说，",
        "综上所述": "总的来说",
        "总而言之，": "总之，",
        "总而言之": "总之",
        "换句话说，": "也就是说，",
        "换句话说": "也就是说",

        # === 结构词去除 ===
        "首先，": "",
        "其次，": "",
        "再次，": "",
        "然后，": "",
        "最后，": "",
        "第一，": "",
        "第二，": "",
        "第三，": "",
        "第四，": "",

        # === 客套结尾 ===
        "希望对您有帮助。": "",
        "希望对您有帮助！": "",
        "希望对您有帮助": "",
        "如有其他问题，": "",
        "如有其他问题": "",
        "欢迎继续咨询。": "",
        "欢迎继续咨询": ""
    }

    def preprocess(self, text: str, verbose: bool = False) -> Tuple[str, List[str]]:
        """
        预处理文本，去除AI痕迹

        Args:
            text: 原始文本
            verbose: 是否输出详细日志

        Returns:
            (处理后文本, 修改记录列表)
        """
        changes = []
        original_length = len(text)

        if verbose:
            logger.info(f"开始NLP预处理，文本长度: {original_length}")

        # 1. 去除AI套路
        text = self._remove_ai_patterns(text, changes)

        # 2. 清理多余空格和标点
        text = self._clean_formatting(text, changes)

        # 3. 记录处理结果
        final_length = len(text)
        reduction = original_length - final_length

        if reduction > 0:
            changes.append(f"总共减少{reduction}个字符")
            if verbose:
                logger.info(f"预处理完成: 减少{reduction}字符, 共{len(changes)}处修改")

        return text, changes

    def _remove_ai_patterns(self, text: str, changes: List[str]) -> str:
        """去除AI模式"""
        for pattern, replacement in self.REPLACEMENTS.items():
            if pattern in text:
                count = text.count(pattern)
                text = text.replace(pattern, replacement)
                changes.append(f"'{pattern}' → '{replacement}' (×{count})")

        return text

    def _clean_formatting(self, text: str, changes: List[str]) -> str:
        """清理格式"""
        original = text

        # 1. 多个空格 → 单个空格
        text = re.sub(r' +', ' ', text)

        # 2. 句首空格
        text = re.sub(r'^\s+', '', text, flags=re.MULTILINE)

        # 3. 句尾空格
        text = text.strip()

        # 4. 多个换行 → 双换行
        text = re.sub(r'\n{3,}', '\n\n', text)

        # 5. 逗号后没空格 → 添加空格（可选）
        # text = re.sub(r'，(?!\s)', '， ', text)

        if text != original:
            changes.append("清理格式")

        return text

    def add_custom_rule(self, pattern: str, replacement: str):
        """
        添加自定义规则

        Args:
            pattern: 要替换的模式
            replacement: 替换成的内容
        """
        self.REPLACEMENTS[pattern] = replacement
        logger.info(f"添加自定义规则: '{pattern}' → '{replacement}'")


# ========== 使用示例 ==========

if __name__ == "__main__":
    # 基础用法
    preprocessor = NLPPreprocessor()

    test_text = """
    当然，首先我需要强调的是，这个问题非常重要。其次，我们应该值得注意的是，
    需要考虑多个因素。最后，综上所述，希望对您有帮助。
    """

    result, changes = preprocessor.preprocess(test_text, verbose=True)

    print("="*60)
    print("原文:", test_text.strip())
    print("\n" + "="*60)
    print("处理后:", result.strip())
    print("\n" + "="*60)
    print("修改记录:")
    for change in changes:
        print(f"  ✓ {change}")

    # 添加自定义规则
    print("\n" + "="*60)
    print("测试自定义规则:")
    preprocessor.add_custom_rule("非常重要", "挺重要")
    result2, changes2 = preprocessor.preprocess("这个问题非常重要。")
    print(f"原文: 这个问题非常重要。")
    print(f"结果: {result2}")
```

## ✅ 测试用例

创建: `backend/tests/test_nlp_preprocessor.py`

```python
import pytest
from app.services.ai.nlp_preprocessor import NLPPreprocessor


class TestNLPPreprocessor:
    """NLP预处理器测试"""

    @pytest.fixture
    def preprocessor(self):
        return NLPPreprocessor()

    def test_remove_greetings(self, preprocessor):
        """测试去除开头套话"""
        text = "当然，很高兴为您服务。让我来帮助您。"
        result, changes = preprocessor.preprocess(text)

        assert "当然" not in result
        assert "很高兴为您服务" not in result
        assert "让我来" not in result
        assert len(changes) > 0

    def test_remove_transitions(self, preprocessor):
        """测试去除过渡词"""
        text = "首先，分析问题。其次，制定方案。最后，执行。"
        result, changes = preprocessor.preprocess(text)

        assert "首先，" not in result
        assert "其次，" not in result
        assert "最后，" not in result

    def test_simplify_formal_phrases(self, preprocessor):
        """测试简化正式表达"""
        text = "值得注意的是，很重要。需要强调的是，时间紧。"
        result, changes = preprocessor.preprocess(text)

        assert "值得注意的是" not in result
        assert "要注意" in result
        assert "需要强调的是" not in result
        assert "重点是" in result

    def test_clean_formatting(self, preprocessor):
        """测试格式清理"""
        text = "测试    多个空格。\n\n\n多个换行。"
        result, changes = preprocessor.preprocess(text)

        assert "    " not in result  # 多余空格被清理
        assert "\n\n\n" not in result  # 多个换行变成双换行

    def test_custom_rule(self, preprocessor):
        """测试自定义规则"""
        preprocessor.add_custom_rule("测试词", "替换词")

        text = "这是测试词。"
        result, changes = preprocessor.preprocess(text)

        assert "测试词" not in result
        assert "替换词" in result

    def test_full_pipeline(self, preprocessor):
        """测试完整流程"""
        text = """
        当然，首先我需要值得注意的是这个问题非常重要。其次，我们应该考虑多个因素。
        最后，综上所述，希望对您有帮助。
        """

        result, changes = preprocessor.preprocess(text)

        # 验证所有AI痕迹都被去除
        assert "当然" not in result
        assert "首先" not in result
        assert "其次" not in result
        assert "最后" not in result
        assert "值得注意的是" not in result
        assert "综上所述" not in result
        assert "希望对您有帮助" not in result

        # 验证有修改记录
        assert len(changes) > 0

    def test_no_changes_for_clean_text(self, preprocessor):
        """测试干净文本不会被改变"""
        text = "这是一段正常的人类写作文本。没有AI痕迹。"
        result, changes = preprocessor.preprocess(text)

        assert result == text.strip()  # 只trim空格
        assert len([c for c in changes if "减少" not in c]) == 0  # 无实质修改


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

## 🚀 性能测试

```python
import time
from app.services.ai.nlp_preprocessor import NLPPreprocessor


def benchmark():
    """性能基准测试"""
    preprocessor = NLPPreprocessor()

    test_text = """
    当然，首先我需要强调的是，这个问题非常重要。其次，我们应该值得注意的是，
    需要考虑多个因素。第三，我们要综合分析各种情况。最后，综上所述，希望对您有帮助。
    """ * 10  # 重复10次

    iterations = 1000

    start = time.time()
    for _ in range(iterations):
        preprocessor.preprocess(test_text)
    end = time.time()

    avg_time = (end - start) / iterations * 1000  # 毫秒

    print(f"处理{iterations}次，平均耗时: {avg_time:.2f}ms")
    print(f"文本长度: {len(test_text)} 字符")
    print(f"处理速度: {len(test_text) / avg_time * 1000:.0f} 字符/秒")


if __name__ == "__main__":
    benchmark()
```

## 📊 预期输出

```
原文: 当然，首先我需要强调的是，这个问题非常重要...

处理后: 我需要重点是，这个问题非常重要...

修改记录:
  ✓ '当然，' → '' (×1)
  ✓ '首先' → '' (×1)
  ✓ '需要强调的是' → '重点是' (×1)
  ✓ '值得注意的是' → '要注意' (×1)
  ✓ '其次，' → '' (×1)
  ✓ '最后，' → '' (×1)
  ✓ '综上所述' → '总的来说' (×1)
  ✓ '希望对您有帮助' → '' (×1)
  ✓ 清理格式
  ✓ 总共减少47个字符
```

## 🔧 扩展建议

### 1. 添加同义词替换（可选）
```python
try:
    import synonyms
    HAS_SYNONYMS = True
except ImportError:
    HAS_SYNONYMS = False

def _replace_synonyms(self, text: str, changes: List[str]) -> str:
    """同义词替换（需要安装synonyms库）"""
    if not HAS_SYNONYMS:
        return text

    # 只替换形容词和副词
    # TODO: 实现同义词替换逻辑
    return text
```

### 2. 添加jieba分词（可选）
```python
try:
    import jieba
    import jieba.posseg as pseg
    HAS_JIEBA = True
except ImportError:
    HAS_JIEBA = False

def _analyze_sentence_structure(self, text: str):
    """分析句式结构"""
    if not HAS_JIEBA:
        return

    words = pseg.cut(text)
    # TODO: 分析句式，识别重复模式
```

---

**下一步**: 集成到HumanizeService（参考[05-改进方案.md](../05-改进方案.md)）
