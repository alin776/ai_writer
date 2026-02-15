"""
NLP preprocessor for lightweight AI-trace cleanup before rewrite.
"""

from __future__ import annotations

import logging
import re
from typing import List, Tuple

logger = logging.getLogger(__name__)


class NLPPreprocessor:
    """Rule-based preprocessor to remove common AI-style phrases quickly."""

    AI_PATTERNS = {
        "套路开头": [
            "当然",
            "很高兴为您服务",
            "让我来",
            "我来帮您",
            "我很荣幸",
            "非常感谢您的提问",
            "感谢您的咨询",
        ],
        "过渡词": [
            "首先",
            "其次",
            "再次",
            "最后",
            "第一",
            "第二",
            "第三",
            "综上所述",
            "值得注意的是",
            "需要强调的是",
            "需要指出的是",
            "总而言之",
            "换句话说",
            "简而言之",
        ],
        "套路结尾": [
            "希望对您有帮助",
            "祝您",
            "如有其他问题",
            "欢迎继续咨询",
            "期待为您服务",
            "随时为您服务",
        ],
        "正式表达": [
            "在此",
            "对此",
            "关于这一点",
            "就这个问题而言",
        ],
    }

    REPLACEMENTS = {
        # 套路开头
        "当然，": "",
        "当然": "",
        "很高兴为您服务。": "",
        "让我来": "",
        "我来帮您": "",
        "感谢您的咨询，": "",
        "感谢您的咨询": "",
        "感谢您的提问，": "",
        "感谢您的提问": "",
        "非常感谢您的提问": "",
        # 过渡词替换/删除
        "值得注意的是": "要注意",
        "需要强调的是": "重点是",
        "需要指出的是": "要说的是",
        "综上所述": "总的来说",
        "总而言之": "总之",
        "换句话说": "也就是说",
        "简而言之": "简单说",
        "首先，": "",
        "首先": "",
        "其次，": "",
        "再次，": "",
        "最后，": "",
        "第一，": "",
        "第二，": "",
        "第三，": "",
        "第四，": "",
        # 套路结尾
        "希望对您有帮助": "",
        "希望这能帮到您": "",
        "如有其他问题": "",
        "欢迎继续咨询": "",
        "期待为您服务": "",
        "随时为您服务": "",
        # 过度正式表达
        "在此": "这里",
        "对此": "对这",
        "关于这一点，": "",
        "关于这一点": "",
        "就这个问题而言，": "",
        "就这个问题而言": "",
    }

    def __init__(self) -> None:
        self.total_processed = 0
        self.total_changes = 0
        logger.info("NLPPreprocessor initialized with %d replacement rules", len(self.REPLACEMENTS))

    def preprocess(self, text: str) -> Tuple[str, List[str]]:
        """Preprocess text and return (processed_text, change_logs)."""
        if not text or not text.strip():
            return text, []

        changes: List[str] = []
        original_length = len(text)

        text = self._remove_ai_patterns(text, changes)
        text = self._clean_formatting(text, changes)

        self.total_processed += 1
        self.total_changes += len(changes)

        reduction = original_length - len(text)
        if reduction > 0:
            changes.append(f"总共减少{reduction}个字符")

        return text, changes

    def _remove_ai_patterns(self, text: str, changes: List[str]) -> str:
        # Longest-first avoids partial replacement eating longer tokens.
        for pattern in sorted(self.REPLACEMENTS.keys(), key=len, reverse=True):
            replacement = self.REPLACEMENTS[pattern]
            if pattern in text:
                count = text.count(pattern)
                text = text.replace(pattern, replacement)
                changes.append(f"替换'{pattern}' x{count}")
        return text

    def _clean_formatting(self, text: str, changes: List[str]) -> str:
        original = text

        text = text.replace("\r\n", "\n").replace("\r", "\n")
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\s+([，。,.！？!?；;：:])", r"\1", text)
        text = re.sub(r"^[，。,.、！？!?；;：:]+", "", text, flags=re.MULTILINE)

        lines = [line.strip() for line in text.split("\n")]
        text = "\n".join(lines)
        text = re.sub(r"\n{3,}", "\n\n", text)
        text = text.strip()

        if text != original:
            changes.append("清理格式")

        return text

    def get_statistics(self) -> dict:
        """Return processing statistics."""
        avg = self.total_changes / self.total_processed if self.total_processed else 0
        return {
            "total_processed": self.total_processed,
            "total_changes": self.total_changes,
            "avg_changes_per_text": avg,
        }
