"""超时配置模块

统一管理所有超时设置，避免分散在多个文件中。

使用方式：
```python
from app.services.agent.timeout_config import TimeoutConfig, async_timeout

# 获取 Multi-Agent 总超时
timeout = TimeoutConfig.MULTI_AGENT_TOTAL

# 获取某阶段超时
outline_timeout = TimeoutConfig.get_stage_timeout("outline")

# 使用超时上下文管理器（兼容 Python 3.10+）
async with async_timeout(TimeoutConfig.LLM_CALL):
    await some_async_operation()
```
"""

import sys
from typing import Dict

# ==================== 兼容性超时导入 ====================
# asyncio.timeout 是 Python 3.11+ 新增的特性
# 对于 Python 3.10，使用 async-timeout 包作为替代
if sys.version_info >= (3, 11):
    from asyncio import timeout as async_timeout
else:
    from async_timeout import timeout as async_timeout

# 导出 async_timeout 供其他模块使用
__all__ = ["TimeoutConfig", "async_timeout"]


class TimeoutConfig:
    """超时配置（单位：秒）

    层级结构：
    ├── 外层任务执行 (TASK_EXECUTION = 900s)
    │   └── Multi-Agent 总超时 (MULTI_AGENT_TOTAL = 480s)
    │       ├── 大纲师 (outline = 120s)
    │       ├── 主笔 (writing = 120s)
    │       ├── 角色守护 + 逻辑审计 (check = 60s) [并行]
    │       └── 总编 (editor = 120s)
    │       └── 串行总计 = 420s (< 480s ✓)
    │
    └── 单次 LLM 调用 (LLM_CALL = 120s)
    """

    # ==================== 外层超时 ====================
    # 任务执行总超时（15分钟）
    TASK_EXECUTION: int = 900

    # 规划流程总超时（15分钟）
    PLANNING_TOTAL: int = 900

    # LangGraph 流式响应超时（8分钟）
    LANGGRAPH_STREAM: int = 480

    # ==================== Multi-Agent 超时 ====================
    # Multi-Agent 内部总超时（8分钟）
    MULTI_AGENT_TOTAL: int = 480

    # 各阶段超时配置（统一设为120s，与单次LLM调用超时一致）
    STAGE_TIMEOUTS: Dict[str, int] = {
        "outline": 120,       # 大纲师
        "writing": 120,       # 主笔
        "character_guard": 60,  # 角色守护
        "logic_auditor": 60,    # 逻辑审计
        "editor": 120,        # 总编
    }

    # ==================== LLM 调用超时 ====================
    # 单次 LLM 调用超时（2分钟）
    LLM_CALL: int = 120

    # HTTP 连接超时
    HTTP_CONNECT: int = 10

    # ==================== 工具方法 ====================

    @classmethod
    def get_stage_timeout(cls, stage: str) -> int:
        """获取某阶段的超时时间

        Args:
            stage: 阶段名称 (outline/writing/character_guard/logic_auditor/editor)

        Returns:
            超时时间（秒）
        """
        return cls.STAGE_TIMEOUTS.get(stage, 60)  # 默认60秒

    @classmethod
    def get_check_timeout(cls) -> int:
        """获取检查阶段超时（取角色守护和逻辑审计的最大值）

        Returns:
            超时时间（秒）
        """
        return max(
            cls.STAGE_TIMEOUTS["character_guard"],
            cls.STAGE_TIMEOUTS["logic_auditor"]
        )

    @classmethod
    def validate(cls) -> bool:
        """验证超时配置的合理性

        检查：
        1. 内层超时 < 外层超时
        2. 各阶段超时之和 < Multi-Agent 总超时

        Returns:
            True 如果配置合理
        """
        # 1. Multi-Agent 总超时 < 任务执行总超时
        if cls.MULTI_AGENT_TOTAL >= cls.TASK_EXECUTION:
            return False

        # 2. 各阶段超时之和 < Multi-Agent 总超时
        # 注意：角色守护和逻辑审计是并行的，取最大值
        serial_sum = (
            cls.STAGE_TIMEOUTS["outline"] +
            cls.STAGE_TIMEOUTS["writing"] +
            cls.get_check_timeout() +  # 并行阶段取最大值
            cls.STAGE_TIMEOUTS["editor"]
        )
        if serial_sum >= cls.MULTI_AGENT_TOTAL:
            return False

        return True

    @classmethod
    def get_summary(cls) -> str:
        """获取超时配置摘要

        Returns:
            配置摘要字符串
        """
        serial_sum = (
            cls.STAGE_TIMEOUTS["outline"] +
            cls.STAGE_TIMEOUTS["writing"] +
            cls.get_check_timeout() +
            cls.STAGE_TIMEOUTS["editor"]
        )

        return f"""超时配置摘要:
├── 任务执行总超时: {cls.TASK_EXECUTION}s ({cls.TASK_EXECUTION / 60:.1f}分钟)
│   └── Multi-Agent 总超时: {cls.MULTI_AGENT_TOTAL}s ({cls.MULTI_AGENT_TOTAL / 60:.1f}分钟)
│       ├── 大纲师: {cls.STAGE_TIMEOUTS['outline']}s
│       ├── 主笔: {cls.STAGE_TIMEOUTS['writing']}s
│       ├── 检查(并行): {cls.get_check_timeout()}s
│       └── 总编: {cls.STAGE_TIMEOUTS['editor']}s
│       └── 串行总计: {serial_sum}s (< {cls.MULTI_AGENT_TOTAL}s ✓)
│
└── 单次 LLM 调用: {cls.LLM_CALL}s
"""
