"""
AI 服务模块

提供 AI 相关的服务封装，包括：
- LangChain ChatOpenAI 调用
- 流式响应处理
- Token 计数和成本计算
"""

from .langchain_ai_service import LangChainAIService

__all__ = ['LangChainAIService']
