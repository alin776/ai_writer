"""DeepAgent 配置常量

基于 Deep Agents 设计理念，提供反思和重规划的配置项。
"""

from typing import List


class DeepAgentConfig:
    """DeepAgent 配置"""

    # 反思限制
    MAX_REFLECTIONS: int = 3      # 单次请求最多反思次数
    MAX_REPLANS: int = 2          # 单次请求最多重规划次数

    # 超时设置（秒）
    REFLECTION_TIMEOUT: int = 30  # 反思超时
    REPLAN_TIMEOUT: int = 45      # 重规划超时

    # 反思触发条件
    REFLECT_ON_FAILURE: bool = True           # 任务失败时反思
    REFLECT_ON_LOW_QUALITY: bool = True       # 低质量结果时反思
    QUALITY_THRESHOLD: float = 0.6            # 质量阈值
    REFLECT_ON_ANALYSIS: bool = True          # 分析类任务后反思
    REFLECT_EVERY_N_TASKS: int = 3            # 每 N 个任务反思一次

    # 反思关键词（用于判断是否需要重规划）
    REPLAN_KEYWORDS: List[str] = [
        "需要", "补充", "调整", "新增", "不足",
        "缺少", "修改计划", "遗漏", "重新"
    ]
