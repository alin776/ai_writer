"""
Prompts 模块

网文创作 Prompt 库,包含:
- 内容创作 Prompts (系统级/分阶段/场景模板)
- 规划类 Prompts (主题/世界观/角色/大纲等)
- Prompt 优化器
- Prompt 库管理系统

参考: novel-ai-agent-Chinese 项目精华
"""

# 导出核心类和枚举
from .novel_phases import (
    NovelPhase,
    SceneType,
    PhaseCharacteristics,
    SlapFaceStructure,
    CoolnessFormula
)

from .content_creation_prompts import ContentCreationPrompts
from .novel_planning_prompts import NovelPlanningPrompts
from .prompt_optimizer import PromptOptimizer
from .quality_prompts import QualityPrompts

__all__ = [
    # 枚举和数据类
    'NovelPhase',
    'SceneType',
    'PhaseCharacteristics',
    'SlapFaceStructure',
    'CoolnessFormula',

    # Prompt 类
    'ContentCreationPrompts',
    'NovelPlanningPrompts',
    'QualityPrompts',
    'PromptOptimizer',
]
