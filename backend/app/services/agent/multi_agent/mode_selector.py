"""Multi-Agent 执行模式选择器

根据任务特征动态选择执行模式：
- lite: 轻量模式，1-2 阶段（适合短内容/简单任务）
- standard: 标准模式，4 阶段（适合中等内容）
- full: 完整模式，5 阶段（适合长内容/复杂任务）
"""

import re
import logging
from typing import Dict, Optional, Literal

logger = logging.getLogger(__name__)


class ModeSelector:
    """Multi-Agent 执行模式选择器"""

    # 模式配置
    MODE_CONFIG = {
        "lite": {
            "stages": [1, 2],
            "optional_stages": [1],
            "skip_revision": True,
            "max_quality_score": 0.80,
            "description": "轻量模式（大纲可选 + 主笔）",
        },
        "standard": {
            "stages": [1, 2, 3, 4],
            "optional_stages": [],
            "skip_revision": True,
            "max_quality_score": 0.85,
            "description": "标准模式（大纲 + 主笔 + 并行审查）",
        },
        "full": {
            "stages": [1, 2, 3, 4, 5],
            "optional_stages": [],
            "skip_revision": False,
            "max_quality_score": 1.00,
            "description": "完整模式（全 5 阶段）",
        },
    }

    # 字数阈值
    WORD_THRESHOLDS = {
        "lite": 500,
        "standard": 1500,
    }

    # 任务类型 → 模式映射
    TASK_TYPE_MODE_MAP = {
        # Lite
        "polish": "lite",
        "expand": "lite",
        "dialogue": "lite",
        "description": "lite",
        # Standard
        "scene": "standard",
        "transition": "standard",
        "flashback": "standard",
        # Full
        "chapter": "full",
        "climax": "full",
        "battle": "full",
        "finale": "full",
    }

    # 任务类型关键词
    TASK_TYPE_KEYWORDS = {
        "polish": ["润色", "优化", "改进", "修饰"],
        "expand": ["扩写", "展开", "详细写"],
        "dialogue": ["对话", "对白", "交谈"],
        "description": ["描写", "描述", "刻画"],
        "scene": ["场景", "一幕", "画面"],
        "transition": ["过渡", "衔接", "承接"],
        "flashback": ["回忆", "闪回", "往事"],
        "chapter": ["一章", "整章", r"第.*章"],
        "climax": ["高潮", "决战", "最终"],
        "battle": ["战斗", "打斗", "交战", "对决"],
        "finale": ["结局", "结尾", "大结局"],
    }

    def select(
        self,
        task: Dict,
        context: Dict
    ) -> Literal["lite", "standard", "full"]:
        """选择执行模式

        Args:
            task: 任务信息
            context: 上下文信息

        Returns:
            执行模式
        """
        return self._determine_mode(task, context)

    def get_config(self, mode: str) -> Dict:
        """获取模式配置"""
        return self.MODE_CONFIG.get(mode, self.MODE_CONFIG["standard"])

    def _determine_mode(
        self,
        task: Dict,
        context: Dict
    ) -> Literal["lite", "standard", "full"]:
        """综合判断执行模式"""

        # 1. 用户强制指定
        if task.get("force_mode"):
            mode = task["force_mode"]
            if mode in self.MODE_CONFIG:
                logger.info(f"[ModeSelector] 用户强制指定: {mode}")
                return mode

        # 2. 多维度判断
        modes = []

        # 字数判断
        word_mode = self._judge_by_word_count(task)
        if word_mode:
            modes.append(("word_count", word_mode))

        # 任务类型判断
        type_mode = self._judge_by_task_type(task)
        if type_mode:
            modes.append(("task_type", type_mode))

        # 复杂度判断
        complexity_mode = self._judge_by_complexity(context)
        modes.append(("complexity", complexity_mode))

        # 3. 记录判断过程
        for source, mode in modes:
            logger.info(f"[ModeSelector] {source} → {mode}")

        # 4. 取最高模式（保守策略）
        MODE_PRIORITY = {"lite": 1, "standard": 2, "full": 3}
        mode_values = [m for _, m in modes]

        if not mode_values:
            final_mode = "standard"
        else:
            final_mode = max(mode_values, key=lambda m: MODE_PRIORITY.get(m, 0))

        logger.info(f"[ModeSelector] 最终选择: {final_mode}")
        return final_mode

    def _judge_by_word_count(self, task: Dict) -> Optional[str]:
        """按目标字数判断"""
        target_words = self._get_target_words(task)

        if target_words is None:
            return None

        if target_words < self.WORD_THRESHOLDS["lite"]:
            return "lite"
        elif target_words < self.WORD_THRESHOLDS["standard"]:
            return "standard"
        else:
            return "full"

    def _judge_by_task_type(self, task: Dict) -> Optional[str]:
        """按任务类型判断"""
        task_type = self._infer_task_type(task.get("description", ""))
        return self.TASK_TYPE_MODE_MAP.get(task_type)

    def _judge_by_complexity(self, context: Dict) -> str:
        """按上下文复杂度判断"""
        score = 0

        # 角色数量
        characters = context.get("key_characters", [])
        if len(characters) > 3:
            score += 2
        elif len(characters) > 1:
            score += 1

        # 伏笔/悬念
        if context.get("pending_foreshadowing"):
            score += 2

        # 关键情节点
        if context.get("is_key_plot_point"):
            score += 2

        # 多视角
        if context.get("multi_perspective"):
            score += 1

        if score >= 4:
            return "full"
        elif score >= 2:
            return "standard"
        else:
            return "lite"

    def _get_target_words(self, task: Dict) -> Optional[int]:
        """提取目标字数"""
        # 直接指定
        if task.get("target_words"):
            return task["target_words"]

        desc = task.get("description", "")

        # 正则匹配
        patterns = [
            (r'(\d+)\s*字', 1),
            (r'约\s*(\d+)\s*字', 1),
            (r'(\d+)\s*字左右', 1),
            (r'(\d+)-(\d+)\s*字', 2),
        ]

        for pattern, group_count in patterns:
            match = re.search(pattern, desc)
            if match:
                if group_count == 2:
                    return (int(match.group(1)) + int(match.group(2))) // 2
                else:
                    return int(match.group(1))

        # 关键词推断
        keyword_map = {
            r'一段|一小段|几句': 300,
            r'一节|一小节': 800,
            r'一章|整章|完整章节': 3000,
        }

        for pattern, word_count in keyword_map.items():
            if re.search(pattern, desc):
                return word_count

        return None

    def _infer_task_type(self, description: str) -> str:
        """推断任务类型"""
        for task_type, keywords in self.TASK_TYPE_KEYWORDS.items():
            for keyword in keywords:
                if re.search(keyword, description):
                    return task_type
        return "unknown"
