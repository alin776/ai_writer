"""
Agent记忆系统模块

提供三层记忆架构:
1. 短期记忆 (Short-term Memory): 单次会话内的对话历史
2. 长期记忆 (Long-term Memory): 跨会话的用户偏好和习惯
3. 知识库 (Knowledge Base): 作品相关的世界观、人物等设定
"""

from .long_term_memory import LongTermMemoryService
from .user_profile import UserProfileMemory
from .memory_manager import MemoryManager

__all__ = [
    "LongTermMemoryService",
    "UserProfileMemory",
    "MemoryManager"
]
