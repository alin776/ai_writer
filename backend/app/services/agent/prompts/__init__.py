"""
Prompts 模块

网文创作 Prompt 库,包含:
- 阶段特性和场景类型枚举
- 格式指南
- 工具描述（单一数据源）
- 决策类提示词
- 规划核心逻辑
- 规划示例
"""

# 导出核心类和枚举
from .novel_phases import (
    NovelPhase,
    SceneType,
    PhaseCharacteristics,
    SlapFaceStructure,
    CoolnessFormula
)

# 导出工具描述
from .tool_descriptions import (
    get_all_tools_description,
)

# 导出决策类提示词
from .decision_prompts import (
    PROMPT_VERSION,
    get_tool_decision_static_prompt,
    get_complexity_decision_prompt,
)

# 导出规划提示词
from .planning_prompts import (
    get_planning_static_prompt,
    get_planning_agent_mode_prompt,
)

# 导出规划示例
from .planning_examples import (
    get_all_planning_examples,
    get_agent_mode_examples,
)

__all__ = [
    # 枚举和数据类
    'NovelPhase',
    'SceneType',
    'PhaseCharacteristics',
    'SlapFaceStructure',
    'CoolnessFormula',
    # 工具描述
    'get_all_tools_description',
    # 决策类提示词
    'PROMPT_VERSION',
    'get_tool_decision_static_prompt',
    'get_complexity_decision_prompt',
    # 规划提示词
    'get_planning_static_prompt',
    'get_planning_agent_mode_prompt',
    # 规划示例
    'get_all_planning_examples',
    'get_agent_mode_examples',
]
