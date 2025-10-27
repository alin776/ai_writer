"""
智能采样分析器

针对长篇网文(100万字+)的优化分析策略:
- 前30章深度分析 (建立核心设定)
- 关键章节识别 (正则+固定间隔)
- 增量分析 (只提取新内容)
- 成本控制 (最大分析章节数限制)
"""

import re
from typing import List, Dict, Optional, Any
from dataclasses import dataclass


@dataclass
class ChapterData:
    """章节数据结构"""
    index: int  # 章节序号 (从1开始)
    title: str  # 章节标题
    content: str  # 章节内容
    word_count: int  # 字数

    @classmethod
    def from_text(cls, index: int, title: str, content: str) -> "ChapterData":
        """从文本创建章节数据"""
        return cls(
            index=index,
            title=title,
            content=content,
            word_count=len(content)
        )


class SmartSamplingAnalyzer:
    """
    智能采样分析器

    根据章节数量和内容长度,智能选择分析策略
    """

    # 章节标题正则表达式
    CHAPTER_TITLE_PATTERN = re.compile(
        r'^(?:'
        r'(?:第[一二三四五六七八九十百千万零〇\d]+[章节部回集卷])|'
        r'(?:序章|楔子|尾声|后记|番外)|'
        r'(?:Chapter\s+\d+)|'
        r'(?:[IVXLCDM]+\.)'
        r')\s*(.*?)$',
        re.MULTILINE | re.IGNORECASE
    )

    def __init__(
        self,
        max_chapters_to_analyze: int = 150,  # 最大分析章节数
        deep_analysis_chapters: int = 30,  # 深度分析章节数
        min_chapter_length: int = 100,  # 最小章节长度 (降低以支持测试和短章节)
        max_chapter_length: int = 8000,  # 单章最大分析长度
    ):
        self.max_chapters_to_analyze = max_chapters_to_analyze
        self.deep_analysis_chapters = deep_analysis_chapters
        self.min_chapter_length = min_chapter_length
        self.max_chapter_length = max_chapter_length

    def parse_txt_file(self, file_path: str) -> List[ChapterData]:
        """
        解析TXT文件为章节列表

        Args:
            file_path: TXT文件路径

        Returns:
            章节数据列表
        """
        import logging
        import os
        logger = logging.getLogger(__name__)

        logger.info(f"🔍 准备解析文件: {file_path}")
        logger.info(f"📁 文件是否存在: {os.path.exists(file_path)}")
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            logger.info(f"📏 文件大小: {file_size} 字节")

        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        logger.info(f"📖 读取内容长度: {len(content)} 字符")
        logger.info(f"📝 内容前200字符: {content[:200]}")

        return self.parse_txt_content(content)

    def parse_txt_content(self, content: str) -> List[ChapterData]:
        """
        解析TXT内容为章节列表

        Args:
            content: TXT文本内容

        Returns:
            章节数据列表
        """
        import logging
        logger = logging.getLogger(__name__)

        chapters = []
        matches = list(self.CHAPTER_TITLE_PATTERN.finditer(content))

        logger.info(f"🔎 正则匹配结果: 找到 {len(matches)} 个章节标题")
        for i, match in enumerate(matches[:5]):  # 只显示前5个
            logger.info(f"  匹配{i+1}: {match.group(0)!r} at position {match.start()}")

        if not matches:
            logger.warning(f"⚠️ 正则未匹配到任何章节,使用备用策略")
            # 备用策略: 按空行分割
            return self._fallback_split(content)

        for i, match in enumerate(matches):
            start = match.start()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(content)

            title = match.group(0).strip()
            chapter_content = content[start:end].strip()

            # 移除标题行
            chapter_content = chapter_content[len(title):].strip()

            # 过滤过短的章节
            if len(chapter_content) < self.min_chapter_length:
                logger.info(f"  ⏭️ 跳过章节 '{title}': 长度{len(chapter_content)}字符 < 最小长度{self.min_chapter_length}")
                continue

            logger.info(f"  ✅ 保留章节 '{title}': {len(chapter_content)}字符")
            chapters.append(ChapterData.from_text(
                index=len(chapters) + 1,
                title=title,
                content=chapter_content
            ))

        logger.info(f"✨ 最终保留 {len(chapters)} 个有效章节")
        return chapters

    def _fallback_split(self, content: str) -> List[ChapterData]:
        """备用策略: 按空行分割"""
        parts = re.split(r'\n\s*\n', content)
        chapters = []

        for i, part in enumerate(parts):
            part = part.strip()
            if len(part) < self.min_chapter_length:
                continue

            # 尝试提取第一行作为标题
            lines = part.split('\n', 1)
            if len(lines) == 2 and len(lines[0]) < 50:
                title = lines[0].strip()
                chapter_content = lines[1].strip()
            else:
                title = f"第{i + 1}部分"
                chapter_content = part

            chapters.append(ChapterData.from_text(
                index=len(chapters) + 1,
                title=title,
                content=chapter_content
            ))

        return chapters

    def select_chapters_to_analyze(
        self,
        chapters: List[ChapterData]
    ) -> List[Dict[str, Any]]:
        """
        智能选择需要分析的章节

        策略:
        1. 前30章全部深度分析
        2. 30章后每隔N章采样一次
        3. 识别关键章节 (篇幅特别长/标题特殊)
        4. 总数不超过max_chapters_to_analyze

        Args:
            chapters: 所有章节列表

        Returns:
            待分析章节列表 [{chapter, is_deep_analysis}]
        """
        total_chapters = len(chapters)
        selected = []

        # 1. 前30章深度分析
        deep_count = min(self.deep_analysis_chapters, total_chapters)
        for i in range(deep_count):
            selected.append({
                "chapter": chapters[i],
                "is_deep_analysis": True,
                "reason": "前期深度分析"
            })

        # 2. 后续章节采样
        if total_chapters > self.deep_analysis_chapters:
            remaining = total_chapters - self.deep_analysis_chapters
            max_sample = self.max_chapters_to_analyze - deep_count

            # 计算采样间隔
            if remaining <= max_sample:
                # 全部分析
                interval = 1
            else:
                # 等间隔采样
                interval = max(2, remaining // max_sample)

            for i in range(self.deep_analysis_chapters, total_chapters, interval):
                if len(selected) >= self.max_chapters_to_analyze:
                    break

                chapter = chapters[i]
                is_key = self._is_key_chapter(chapter)

                selected.append({
                    "chapter": chapter,
                    "is_deep_analysis": is_key,
                    "reason": "关键章节" if is_key else f"采样分析(间隔{interval})"
                })

        return selected

    def _is_key_chapter(self, chapter: ChapterData) -> bool:
        """
        判断是否为关键章节

        关键章节特征:
        - 篇幅特别长 (>1.5倍平均长度)
        - 标题包含特殊关键词 (决战/大结局/转折等)
        """
        # 关键词识别
        key_words = [
            "决战", "大战", "大结局", "终章", "转折",
            "觉醒", "突破", "晋级", "boss", "高潮"
        ]
        title_lower = chapter.title.lower()
        if any(word in title_lower for word in key_words):
            return True

        # 篇幅识别 (暂时简单判断>6000字)
        if chapter.word_count > 6000:
            return True

        return False

    def truncate_content(self, content: str) -> str:
        """
        截断过长的内容

        Args:
            content: 原始内容

        Returns:
            截断后的内容
        """
        if len(content) <= self.max_chapter_length:
            return content

        truncated = content[:self.max_chapter_length]
        truncated += "\n\n...(内容过长已截断)"
        return truncated

    def estimate_cost(
        self,
        chapters: List[ChapterData],
        cost_per_1k_tokens: float = 0.001
    ) -> Dict[str, Any]:
        """
        估算分析成本

        Args:
            chapters: 章节列表
            cost_per_1k_tokens: 每1k tokens的成本

        Returns:
            成本估算 {total_chapters, analyzed_chapters, estimated_tokens, estimated_cost}
        """
        selected = self.select_chapters_to_analyze(chapters)

        total_words = sum(
            min(item["chapter"].word_count, self.max_chapter_length)
            for item in selected
        )

        # 粗略估算: 1字 ≈ 1.5 tokens (中文)
        estimated_input_tokens = int(total_words * 1.5)
        # 输出 tokens 约为输入的 20%
        estimated_output_tokens = int(estimated_input_tokens * 0.2)
        total_tokens = estimated_input_tokens + estimated_output_tokens

        estimated_cost = (total_tokens / 1000) * cost_per_1k_tokens

        return {
            "total_chapters": len(chapters),
            "analyzed_chapters": len(selected),
            "deep_analysis_chapters": sum(1 for item in selected if item["is_deep_analysis"]),
            "estimated_input_tokens": estimated_input_tokens,
            "estimated_output_tokens": estimated_output_tokens,
            "estimated_total_tokens": total_tokens,
            "estimated_cost_usd": round(estimated_cost, 2),
        }
