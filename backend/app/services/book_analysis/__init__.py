"""
图书分析服务模块

提供网文小说的智能分析功能,包括:
- 策略模式架构 (支持多种分析策略)
- 智能采样分析 (针对长篇网文优化)
- 11维度网文分析 (番茄小说策略)
- 智能建议生成 (自动关联世界观元素)
"""

from .strategy import BookAnalysisStrategy, AnalysisDimension
from .web_novel_strategy import WebNovelStrategy
from .smart_sampling import SmartSamplingAnalyzer
from .suggestion_generator import SuggestionGenerator

__all__ = [
    "BookAnalysisStrategy",
    "AnalysisDimension",
    "WebNovelStrategy",
    "SmartSamplingAnalyzer",
    "SuggestionGenerator",
]
