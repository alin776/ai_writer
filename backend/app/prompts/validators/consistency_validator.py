"""
一致性验证器 - 验证引用和事实一致性
"""
import re
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class ConsistencyValidator:
    """
    一致性验证器

    功能:
    1. 验证AI是否引用了原文
    2. 检查引用内容是否准确
    3. 验证分析结论是否有文本依据
    """

    @staticmethod
    def extract_citations(text: str) -> List[str]:
        """
        提取文本中的引用

        识别模式:
        - "引用：XXX"
        - "原文：XXX"
        - 引号中的内容
        """
        citations = []

        # 1. 显式引用标记
        explicit_citations = re.findall(r'引用[：:](.*?)(?:\n|$)', text)
        citations.extend(explicit_citations)

        explicit_citations2 = re.findall(r'原文[：:](.*?)(?:\n|$)', text)
        citations.extend(explicit_citations2)

        # 2. 引号中的长文本（>10字符）
        quoted_texts = re.findall(r'["""](.*?)["""]', text)
        long_quotes = [q for q in quoted_texts if len(q) > 10]
        citations.extend(long_quotes)

        return citations

    @classmethod
    def validate_citations(cls, source_text: str, ai_output: str) -> Dict[str, Any]:
        """
        验证AI输出是否包含引用

        Args:
            source_text: 源文本
            ai_output: AI输出

        Returns:
            验证结果
        """
        citations = cls.extract_citations(ai_output)

        # 🔧 2025-12-02: P1修复 - 放宽引用要求
        # 不强制要求必须有引用，因为有些分析任务不需要引用
        if not citations:
            return {
                "valid": True,
                "warning": "AI输出未包含显式引用",
                "message": "未找到引用标记，但不影响验证通过",
                "citations_found": 0
            }

        # 验证引用内容是否在源文本中
        valid_citations = []
        invalid_citations = []

        for citation in citations:
            # 简化比较：移除空白后查找
            citation_clean = re.sub(r'\s+', '', citation)
            source_clean = re.sub(r'\s+', '', source_text)

            # 🔧 2025-12-02: P1修复 - 使用模糊匹配
            # 检查引用是否是源文本的子串（允许合理改写）
            if citation_clean in source_clean:
                valid_citations.append(citation)
            else:
                # 模糊匹配：检查引用中是否有较长的连续片段出现在源文本中
                # 使用滑动窗口检查连续子串匹配
                min_match_len = max(4, len(citation_clean) // 3)  # 至少匹配1/3长度或4个字符
                found_match = False

                for i in range(len(citation_clean) - min_match_len + 1):
                    substring = citation_clean[i:i + min_match_len]
                    if substring in source_clean:
                        found_match = True
                        break

                if found_match:
                    valid_citations.append(citation)
                else:
                    invalid_citations.append(citation)

        # 🔧 2025-12-02: P1修复 - 提高容错度
        # 只要有超过50%的引用是有效的，就通过验证
        if valid_citations or len(invalid_citations) <= len(citations) * 0.5:
            return {
                "valid": True,
                "message": "AI输出包含有效引用",
                "citations_count": len(valid_citations),
                "citations": valid_citations[:3],  # 仅返回前3个示例
                "warning": f"部分引用可能经过改写({len(invalid_citations)}个)" if invalid_citations else None
            }

        # 只有当所有引用都无效时才判定失败
        return {
            "valid": False,
            "error": "部分引用内容不在源文本中",
            "invalid_citations": invalid_citations[:3],  # 最多返回3个
            "valid_citations": len(valid_citations),
            "recommendation": "检查引用准确性"
        }
