"""
LLM专用文本清理器
参考: Reader-LM (Jina AI) + Markdowner + DOM-to-Semantic-Markdown

功能:
1. HTML → 纯文本（语义保留）
2. 文本规范化（空白、换行）
3. Token估算和优化
4. 批量处理支持
"""
from bs4 import BeautifulSoup
import re
from typing import Optional, List, Dict, Any
import logging
from functools import lru_cache

logger = logging.getLogger(__name__)


class TextCleaner:
    """
    文本清理工具类

    设计原则:
    - LLM-First: 专为LLM优化
    - 语义保留: 保留重要结构和标记
    - Token高效: 移除冗余，优化Token使用
    - 快速处理: 缓存+优化算法
    """

    # 需要完全移除的HTML标签（无语义价值）
    STRIP_TAGS = [
        'script', 'style', 'meta', 'link', 'noscript',
        'iframe', 'embed', 'object', 'applet'
    ]

    # 语义标签映射（HTML → Markdown）
    SEMANTIC_TAGS = {
        'h1': '\n# ',
        'h2': '\n## ',
        'h3': '\n### ',
        'h4': '\n#### ',
        'h5': '\n##### ',
        'h6': '\n###### ',
        'strong': '**',
        'b': '**',
        'em': '*',
        'i': '*',
        'code': '`',
        'pre': '\n```\n',
    }

    # HTML实体映射
    HTML_ENTITIES = {
        '&nbsp;': ' ',
        '&lt;': '<',
        '&gt;': '>',
        '&amp;': '&',
        '&quot;': '"',
        '&apos;': "'",
        '&#8220;': '"',
        '&#8221;': '"',
        '&#8216;': "'",
        '&#8217;': "'",
    }

    @classmethod
    def html_to_clean_text(
        cls,
        html_content: str,
        preserve_structure: bool = True,
        max_length: Optional[int] = None
    ) -> str:
        """
        将HTML转换为LLM友好的纯文本

        Args:
            html_content: HTML内容
            preserve_structure: 是否保留段落结构
            max_length: 最大长度限制

        Returns:
            清理后的纯文本

        Example:
            >>> html = '<p>&nbsp; &nbsp; 段融回到<strong>镖局</strong>...</p>'
            >>> clean = TextCleaner.html_to_clean_text(html)
            >>> print(clean)
            '段融回到**镖局**...'
        """
        if not html_content:
            return ""

        try:
            # 1. 解析HTML
            soup = BeautifulSoup(html_content, 'html.parser')

            # 2. 移除无用标签
            for tag_name in cls.STRIP_TAGS:
                for tag in soup.find_all(tag_name):
                    tag.decompose()

            # 3. 处理语义标签（转换为Markdown）
            if preserve_structure:
                cls._convert_semantic_tags(soup)

            # 4. 提取文本
            text = soup.get_text(separator='\n')

            # 5. 清理和规范化
            text = cls._normalize_text(text)

            # 6. 长度限制
            if max_length and len(text) > max_length:
                text = cls._smart_truncate(text, max_length)
                logger.debug(f"文本被截断到{max_length}字符")

            return text

        except Exception as e:
            logger.error(f"HTML清理失败: {e}")
            # 降级方案：直接提取文本
            soup = BeautifulSoup(html_content, 'html.parser')
            return soup.get_text()

    @classmethod
    def _convert_semantic_tags(cls, soup: BeautifulSoup):
        """
        将语义标签转换为Markdown格式

        修复：使用 replace_with 而不是 tag.string 以保留嵌套结构
        """
        for tag_name, markdown_prefix in cls.SEMANTIC_TAGS.items():
            for tag in soup.find_all(tag_name):
                # 获取标签的文本内容（包括所有子节点）
                text_content = tag.get_text()

                if tag_name == 'pre':
                    # 代码块特殊处理
                    new_text = f"{markdown_prefix}{text_content}\n```"
                elif tag_name in ['strong', 'b', 'em', 'i', 'code']:
                    # 行内标记：前后包围
                    new_text = f"{markdown_prefix}{text_content}{markdown_prefix}"
                else:
                    # 标题：前置标记
                    new_text = f"{markdown_prefix}{text_content}"

                # ✅ 修复：使用 replace_with 而不是 tag.string
                # 这样可以正确处理嵌套标签
                from bs4 import NavigableString
                tag.replace_with(NavigableString(new_text))

    @classmethod
    def _normalize_text(cls, text: str) -> str:
        """
        文本规范化

        处理:
        1. HTML实体替换
        2. 多余空白清理
        3. 多余换行清理
        4. 首尾清理

        Args:
            text: 原始文本

        Returns:
            规范化后的文本
        """
        # 1. 替换HTML实体
        for entity, replacement in cls.HTML_ENTITIES.items():
            text = text.replace(entity, replacement)

        # 2. 清理多余空白
        text = re.sub(r'[ \t]+', ' ', text)  # 多个空格→单个
        text = re.sub(r'\n[ \t]+', '\n', text)  # 行首空格
        text = re.sub(r'[ \t]+\n', '\n', text)  # 行尾空格

        # 3. 清理多余换行
        text = re.sub(r'\n{3,}', '\n\n', text)  # 多个换行→双换行

        # 4. 首尾清理
        text = text.strip()

        return text

    @classmethod
    def _smart_truncate(cls, text: str, max_length: int) -> str:
        """
        智能截断（在句子边界）

        Args:
            text: 文本
            max_length: 最大长度

        Returns:
            截断后的文本
        """
        if len(text) <= max_length:
            return text

        # 在max_length附近找句子结束符
        truncated = text[:max_length]

        # 查找最后的句子结束符
        sentence_endings = ['。', '！', '？', '.', '!', '?', '\n']
        last_ending = -1

        for ending in sentence_endings:
            pos = truncated.rfind(ending)
            if pos > last_ending:
                last_ending = pos

        # 如果找到句子结束符，在那里截断
        if last_ending > max_length * 0.8:  # 至少保留80%
            return text[:last_ending + 1] + "..."
        else:
            # 否则直接截断
            return truncated + "..."

    @classmethod
    def estimate_tokens(cls, text: str) -> int:
        """
        估算Token数量（中文）

        规则 (基于GPT tokenizer的统计规律):
        - 中文字符: 1字符 ≈ 1.5 tokens
        - 英文单词: 1单词 ≈ 1 token
        - 标点符号: 1字符 ≈ 0.5 tokens
        - 数字: 1个 ≈ 0.3 tokens

        Args:
            text: 文本内容

        Returns:
            估算的token数量

        Example:
            >>> text = "段融回到镖局，开始修炼。"
            >>> tokens = TextCleaner.estimate_tokens(text)
            >>> print(tokens)
            15
        """
        # 统计中文字符
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))

        # 统计英文单词
        english_words = len(re.findall(r'\b[a-zA-Z]+\b', text))

        # 统计数字
        digits = len(re.findall(r'\d', text))

        # 统计标点和其他
        total_chars = len(text)
        other_chars = total_chars - chinese_chars - len(re.findall(r'[a-zA-Z]', text)) - digits

        # 估算tokens
        estimated = (
            chinese_chars * 1.5 +
            english_words * 1.0 +
            digits * 0.3 +
            other_chars * 0.5
        )

        return int(estimated)

    @classmethod
    def optimize_for_llm(
        cls,
        text: str,
        target_tokens: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        为LLM优化文本

        Args:
            text: 原始文本
            target_tokens: 目标token数（如果超过则压缩）

        Returns:
            {
                "text": "优化后的文本",
                "original_tokens": 123,
                "optimized_tokens": 89,
                "compression_ratio": 0.27,
                "truncated": False
            }
        """
        original_tokens = cls.estimate_tokens(text)

        # 如果无需压缩，直接返回
        if not target_tokens or original_tokens <= target_tokens:
            return {
                "text": text,
                "original_tokens": original_tokens,
                "optimized_tokens": original_tokens,
                "compression_ratio": 0.0,
                "truncated": False
            }

        # 计算需要保留的比例
        keep_ratio = target_tokens / original_tokens

        # 计算对应的字符长度
        target_length = int(len(text) * keep_ratio)

        # 智能截断
        optimized_text = cls._smart_truncate(text, target_length)

        optimized_tokens = cls.estimate_tokens(optimized_text)

        return {
            "text": optimized_text,
            "original_tokens": original_tokens,
            "optimized_tokens": optimized_tokens,
            "compression_ratio": 1 - (optimized_tokens / original_tokens),
            "truncated": True
        }

    @classmethod
    @lru_cache(maxsize=128)
    def cached_clean(cls, html_content: str) -> str:
        """
        带缓存的HTML清理（用于重复访问的内容）

        Args:
            html_content: HTML内容

        Returns:
            清理后的文本

        Note:
            使用LRU缓存，最多缓存128个结果
        """
        return cls.html_to_clean_text(html_content)

    @classmethod
    def batch_clean(
        cls,
        html_list: List[str],
        preserve_structure: bool = True
    ) -> List[str]:
        """
        批量清理HTML

        Args:
            html_list: HTML内容列表
            preserve_structure: 是否保留结构

        Returns:
            清理后的文本列表
        """
        return [
            cls.html_to_clean_text(html, preserve_structure)
            for html in html_list
        ]

    @classmethod
    def get_stats(cls, html_content: str) -> Dict[str, Any]:
        """
        获取清理统计信息

        Args:
            html_content: HTML内容

        Returns:
            统计信息字典
        """
        cleaned = cls.html_to_clean_text(html_content)

        original_length = len(html_content)
        cleaned_length = len(cleaned)

        original_tokens = cls.estimate_tokens(html_content)
        cleaned_tokens = cls.estimate_tokens(cleaned)

        return {
            'original_length': original_length,
            'cleaned_length': cleaned_length,
            'reduction_percent': round((1 - cleaned_length / original_length) * 100, 1) if original_length > 0 else 0,
            'original_tokens': original_tokens,
            'cleaned_tokens': cleaned_tokens,
            'token_reduction_percent': round((1 - cleaned_tokens / original_tokens) * 100, 1) if original_tokens > 0 else 0
        }


# 全局单例
text_cleaner = TextCleaner()
