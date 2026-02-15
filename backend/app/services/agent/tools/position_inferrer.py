"""
智能位置推断 - 根据用户意图推断内容插入位置

支持三种定位方式：
1. 文本锚点（before_anchor / after_anchor）
2. 关键词推断（续写→末尾，开头→开头）
3. 段落定位（第N段）
"""
import re
from typing import Optional, Dict, Any
from difflib import SequenceMatcher


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

    def find_by_anchors(
        self,
        content: str,
        before_anchor: Optional[str] = None,
        after_anchor: Optional[str] = None,
        fallback: str = "end"
    ) -> Dict[str, Any]:
        """
        通过前后锚点定位插入位置

        三级回退策略：
        1. 精确匹配：同时找到 before + after
        2. 单锚点匹配：只找到其中一个
        3. 模糊匹配：用相似度找最接近的位置
        4. fallback：都失败时用备用位置

        Args:
            content: 章节内容
            before_anchor: 插入点前面的文本
            after_anchor: 插入点后面的文本
            fallback: 备用位置

        Returns:
            {"position": int, "confidence": float, "reason": str}
        """
        if not content:
            return {
                "position": 0,
                "confidence": 0.5,
                "reason": "内容为空，插入到开头"
            }

        # Level 1: 双锚点精确匹配
        if before_anchor and after_anchor:
            before_idx = content.find(before_anchor)
            if before_idx != -1:
                # 在 before_anchor 后面找 after_anchor
                search_start = before_idx + len(before_anchor)
                after_idx = content.find(after_anchor, search_start)
                if after_idx != -1 and after_idx - search_start < 200:
                    # 两个锚点之间距离合理（<200字符）
                    position = before_idx + len(before_anchor)
                    return {
                        "position": position,
                        "confidence": 1.0,
                        "reason": f"精确匹配：在「{before_anchor[-10:]}」后插入"
                    }

        # Level 2: 单锚点匹配
        if before_anchor:
            # 找最后一个匹配（更可能是用户指的位置）
            idx = content.rfind(before_anchor)
            if idx != -1:
                position = idx + len(before_anchor)
                return {
                    "position": position,
                    "confidence": 0.9,
                    "reason": f"单锚点匹配：在「{before_anchor[-10:]}」后插入"
                }

        if after_anchor:
            # 找第一个匹配
            idx = content.find(after_anchor)
            if idx != -1:
                return {
                    "position": idx,
                    "confidence": 0.85,
                    "reason": f"单锚点匹配：在「{after_anchor[:10]}」前插入"
                }

        # Level 3: 模糊匹配（滑动窗口 + 相似度）
        anchor = before_anchor or after_anchor
        if anchor and len(anchor) >= 10:
            fuzzy_result = self._fuzzy_find(content, anchor)
            if fuzzy_result and fuzzy_result["confidence"] >= 0.7:
                return fuzzy_result

        # Level 4: Fallback
        fallback_pos = self.resolve_position(fallback, content)
        return {
            "position": fallback_pos,
            "confidence": 0.5,
            "reason": f"锚点匹配失败，使用备用位置: {fallback}"
        }

    def _fuzzy_find(self, content: str, anchor: str, threshold: float = 0.7) -> Optional[Dict[str, Any]]:
        """
        模糊匹配：用滑动窗口找最相似的位置

        Args:
            content: 章节内容
            anchor: 要匹配的锚点文本
            threshold: 相似度阈值

        Returns:
            {"position": int, "confidence": float, "reason": str} 或 None
        """
        anchor_len = len(anchor)
        best_ratio = 0.0
        best_pos = -1

        # 滑动窗口，步长为 anchor 长度的 1/4
        step = max(1, anchor_len // 4)
        for i in range(0, len(content) - anchor_len + 1, step):
            window = content[i:i + anchor_len]
            ratio = SequenceMatcher(None, anchor, window).ratio()
            if ratio > best_ratio:
                best_ratio = ratio
                best_pos = i

        if best_ratio >= threshold:
            return {
                "position": best_pos + anchor_len,
                "confidence": best_ratio,
                "reason": f"模糊匹配（相似度{best_ratio:.0%}）"
            }

        return None


# 单例实例
position_inferrer = PositionInferrer()


def find_by_anchors(
    content: str,
    before_anchor: Optional[str] = None,
    after_anchor: Optional[str] = None,
    fallback: str = "end"
) -> Dict[str, Any]:
    """
    通过前后锚点定位插入位置（模块级函数，方便直接调用）

    Args:
        content: 章节内容
        before_anchor: 插入点前面的文本（20-50字）
        after_anchor: 插入点后面的文本（20-50字）
        fallback: 定位失败时的备用位置 ("end" | "start" | int)

    Returns:
        {"position": int, "confidence": float, "reason": str}
    """
    return position_inferrer.find_by_anchors(content, before_anchor, after_anchor, fallback)
