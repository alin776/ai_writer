"""
智能位置推断 - 根据用户意图推断内容插入位置
"""
import re
from typing import Optional


class PositionInferrer:
    """智能推断内容插入位置"""

    def infer_position(
        self,
        chapter_content: str,
        operation: str,
        user_intent: str,
        context: dict = None
    ) -> dict:
        """
        根据用户意图推断最佳插入位置

        Args:
            chapter_content: 章节当前内容
            operation: 操作类型 (append/insert/replace)
            user_intent: 用户意图描述
            context: 额外上下文（如选中文本位置）

        Returns:
            {
                "position": "end" | "start" | int,
                "confidence": float,  # 0-1
                "reason": str
            }
        """
        # 1. 如果有选中文本，优先使用选中位置
        if context and context.get('selection'):
            return {
                "position": context['selection'],
                "confidence": 1.0,
                "reason": "用户已选中目标位置"
            }

        # 2. 根据关键词推断
        intent_lower = user_intent.lower()

        # 续写类意图 -> 末尾
        if any(kw in intent_lower for kw in ['续写', '继续', '接着写', '往下写', '继续写', '写下去']):
            return {
                "position": "end",
                "confidence": 0.95,
                "reason": "续写意图，插入到章节末尾"
            }

        # 开头类意图 -> 开头
        if any(kw in intent_lower for kw in ['开头', '开篇', '第一段', '开始', '起始']):
            return {
                "position": "start",
                "confidence": 0.9,
                "reason": "开头意图，插入到章节开头"
            }

        # 特定段落意图 -> 查找段落
        paragraph_match = re.search(r'第(\d+)段', user_intent)
        if paragraph_match:
            para_num = int(paragraph_match.group(1))
            position = self._find_paragraph_position(chapter_content, para_num)
            return {
                "position": position,
                "confidence": 0.85,
                "reason": f"在第{para_num}段后插入"
            }

        # 结尾类意图 -> 末尾
        if any(kw in intent_lower for kw in ['结尾', '末尾', '最后', '结束']):
            return {
                "position": "end",
                "confidence": 0.9,
                "reason": "结尾意图，插入到章节末尾"
            }

        # 3. 默认：末尾
        return {
            "position": "end",
            "confidence": 0.7,
            "reason": "默认插入到末尾"
        }

    def _find_paragraph_position(self, content: str, para_num: int) -> int:
        """查找第N段的结束位置"""
        # 按双换行分割段落
        paragraphs = content.split('\n\n')
        if para_num > len(paragraphs):
            return len(content)

        # 计算前N段的总长度
        position = 0
        for i in range(para_num):
            position += len(paragraphs[i])
            if i < para_num - 1:
                position += 2  # 段落分隔符 \n\n

        return position

    def resolve_position(self, position, content: str) -> int:
        """
        将位置标识符解析为实际字符位置

        Args:
            position: "end" | "start" | int
            content: 章节内容

        Returns:
            实际字符位置
        """
        if position == "end":
            return len(content)
        elif position == "start":
            return 0
        elif isinstance(position, int):
            return min(max(0, position), len(content))
        else:
            return len(content)


# 单例实例
position_inferrer = PositionInferrer()
