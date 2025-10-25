"""
上下文提取器

根据文本长度智能提取上下文，用于改写时提供参考
"""

from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class ContextExtractor:
    """上下文提取器 - 智能分级提取策略"""

    # 上下文提取规则（根据原文长度）
    CONTEXT_RULES = [
        (50, 800),    # 原文 < 50字，前后各 800 字
        (200, 500),   # 原文 < 200字，前后各 500 字
        (500, 300),   # 原文 < 500字，前后各 300 字
    ]
    # 原文 >= 500字，不提取上下文

    def __init__(self):
        """初始化提取器"""
        logger.info("ContextExtractor 初始化成功")

    def get_context_length(self, text_length: int) -> int:
        """
        根据原文长度获取应该提取的上下文长度

        Args:
            text_length: 原文长度

        Returns:
            int: 上下文长度（单侧），0 表示不需要上下文
        """
        for threshold, context_len in self.CONTEXT_RULES:
            if text_length < threshold:
                return context_len
        return 0  # 原文较长，不需要上下文

    def extract_context(
        self,
        full_text: str,
        start_pos: int,
        end_pos: int
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        从全文中提取指定位置的上下文

        Args:
            full_text: 完整文本
            start_pos: 选中文本的起始位置
            end_pos: 选中文本的结束位置

        Returns:
            Tuple[Optional[str], Optional[str]]: (前文上下文, 后文上下文)
        """
        # 计算选中文本长度
        selected_length = end_pos - start_pos

        # 获取应提取的上下文长度
        context_length = self.get_context_length(selected_length)

        if context_length == 0:
            logger.info(f"原文长度 {selected_length} 字，无需提取上下文")
            return None, None

        # 提取前文（从 start_pos 往前取 context_length 个字符）
        context_before_start = max(0, start_pos - context_length)
        context_before = full_text[context_before_start:start_pos] if start_pos > 0 else None

        # 提取后文（从 end_pos 往后取 context_length 个字符）
        context_after_end = min(len(full_text), end_pos + context_length)
        context_after = full_text[end_pos:context_after_end] if end_pos < len(full_text) else None

        # 清理空白上下文
        if context_before:
            context_before = context_before.strip()
            if not context_before:
                context_before = None

        if context_after:
            context_after = context_after.strip()
            if not context_after:
                context_after = None

        logger.info(
            f"提取上下文完成 - 原文: {selected_length}字, "
            f"前文: {len(context_before) if context_before else 0}字, "
            f"后文: {len(context_after) if context_after else 0}字"
        )

        return context_before, context_after

    def extract_context_by_text(
        self,
        full_text: str,
        selected_text: str
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        根据选中的文本内容提取上下文（自动查找位置）

        Args:
            full_text: 完整文本
            selected_text: 选中的文本内容

        Returns:
            Tuple[Optional[str], Optional[str]]: (前文上下文, 后文上下文)
        """
        # 查找选中文本在全文中的位置
        start_pos = full_text.find(selected_text)

        if start_pos == -1:
            logger.warning("未在全文中找到选中的文本")
            return None, None

        end_pos = start_pos + len(selected_text)

        return self.extract_context(full_text, start_pos, end_pos)

    def get_context_info(self, text_length: int) -> str:
        """
        获取上下文提取说明（用于前端显示）

        Args:
            text_length: 原文长度

        Returns:
            str: 上下文提取说明
        """
        context_length = self.get_context_length(text_length)

        if context_length == 0:
            return "原文较长，无需提取上下文"

        return f"已自动提取前后各 {context_length} 字作为上下文"


# 全局单例
_context_extractor: Optional[ContextExtractor] = None


def get_context_extractor() -> ContextExtractor:
    """获取上下文提取器单例"""
    global _context_extractor
    if _context_extractor is None:
        _context_extractor = ContextExtractor()
    return _context_extractor
