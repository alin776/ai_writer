"""
Agent记忆系统模块

提供三层记忆架构:
1. 短期记忆 (Short-term Memory): 单次会话内的对话历史
2. 长期记忆 (Long-term Memory): 跨会话的用户偏好和习惯
3. 知识库 (Knowledge Base): 作品相关的世界观、人物等设定

Agent增强功能:
- EnhancedMemoryManager: 增强的记忆管理器（三层记忆+智能遗忘）
- SmartForgetStrategy: 智能遗忘策略
- MemoryItem/MemorySnapshot: 数据类型定义
"""

# 旧的记忆系统（保持兼容性）
from .long_term_memory import LongTermMemoryService
from .user_profile import UserProfileMemory
from .memory_manager import MemoryManager

# 新的增强记忆系统
from .types import (
    MemoryItem,
    MemoryLayer,
    MemorySnapshot,
    MemoryStats,
    ForgetDecision
)
from .memory_strategy import SmartForgetStrategy
from .enhanced_memory_manager import EnhancedMemoryManager

__all__ = [
    # 新的增强功能
    "EnhancedMemoryManager",
    "SmartForgetStrategy",
    "MemoryItem",
    "MemoryLayer",
    "MemorySnapshot",
    "MemoryStats",
    "ForgetDecision",

    # 旧的兼容接口
    "LongTermMemoryService",
    "UserProfileMemory",
    "MemoryManager"
]
