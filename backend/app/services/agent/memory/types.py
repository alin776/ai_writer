"""
Memory 系统类型定义

定义Memory系统的核心数据结构:
- MemoryItem: 记忆条目
- MemoryLayer: 记忆层级
- MemorySnapshot: 记忆快照
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, Any, Optional, List
from enum import Enum


class MemoryLayer(str, Enum):
    """
    记忆层级枚举

    三层记忆模型:
    - SHORT_TERM: 短期记忆，最近10条，完整保留
    - MEDIUM_TERM: 中期记忆，最近100条，按重要度过滤
    - LONG_TERM: 长期记忆，历史所有，压缩为摘要
    """
    SHORT_TERM = "short_term"    # 短期记忆
    MEDIUM_TERM = "medium_term"  # 中期记忆
    LONG_TERM = "long_term"      # 长期记忆


class MemoryItem(BaseModel):
    """
    记忆条目

    核心数据结构，表示Agent的一条记忆。
    包含内容、时间、重要度等信息，支持智能遗忘和语义检索。
    """

    # ==================== 基础信息 ====================

    id: str = Field(..., description="唯一标识，格式: mem_{uuid}")
    user_id: str = Field(..., description="用户ID")
    conversation_id: str = Field(..., description="会话ID")

    # ==================== 内容信息 ====================

    role: str = Field(
        ...,
        description="角色: user(用户输入)/assistant(AI回复)/system(系统消息)/tool(工具输出)"
    )
    content: str = Field(..., description="记忆内容文本")

    # ==================== 时间信息 ====================

    timestamp: datetime = Field(..., description="创建时间")
    last_access: datetime = Field(..., description="最后访问时间")

    # ==================== 重要度相关 ====================

    importance: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="初始重要度 (0.0-1.0)，用于智能遗忘计算"
    )

    decay_rate: float = Field(
        default=0.1,
        ge=0.0,
        description="时间衰减速率，值越大遗忘越快"
    )

    access_count: int = Field(
        default=0,
        ge=0,
        description="访问次数，越常访问越重要"
    )

    # ==================== 扩展元数据 ====================

    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="""
        扩展元数据，可包含:
        - memory_type: 记忆类型 (dialogue/setting/preference/feedback)
        - source: 来源 (user_input/ai_response/system/tool_output)
        - user_marked: 用户手动标记的重要性
        - tags: 标签列表
        - current_importance: 计算后的当前重要度（遗忘策略使用）
        """
    )

    # ==================== 向量嵌入（语义检索，第二阶段）====================

    embedding: Optional[List[float]] = Field(
        default=None,
        description="向量嵌入，用于语义检索。第一阶段可选，第二阶段集成向量模型"
    )



class MemorySnapshot(BaseModel):
    """
    记忆快照

    用于保存和恢复某个时刻的完整记忆状态。
    支持回滚、实验对比等场景。
    """

    # ==================== 基础信息 ====================

    snapshot_id: str = Field(..., description="快照ID，格式: snap_{uuid}")
    user_id: str = Field(..., description="用户ID")
    conversation_id: str = Field(..., description="会话ID")
    created_at: datetime = Field(..., description="创建时间")

    # ==================== 快照数据 ====================

    short_term_memories: List[MemoryItem] = Field(
        default_factory=list,
        description="短期记忆列表（最多10条）"
    )

    medium_term_memories: List[MemoryItem] = Field(
        default_factory=list,
        description="中期记忆列表（最多100条）"
    )

    long_term_summary: str = Field(
        default="",
        description="长期记忆摘要文本"
    )

    # ==================== 元数据 ====================

    description: str = Field(
        default="",
        description="快照描述，如: '完成第一章创作后的状态'"
    )

    tags: List[str] = Field(
        default_factory=list,
        description="快照标签，便于分类管理"
    )



# ==================== 辅助类型 ====================

class MemoryStats(BaseModel):
    """
    记忆统计信息

    用于监控和展示Memory系统状态
    """
    user_id: str
    short_term_count: int = 0
    medium_term_count: int = 0
    long_term_summary_length: int = 0
    total_access_count: int = 0
    avg_importance: float = 0.0
    last_update: datetime = Field(default_factory=datetime.now)


class ForgetDecision(BaseModel):
    """
    遗忘决策结果

    智能遗忘策略的输出
    """
    memory_id: str
    should_forget: bool
    current_importance: float
    reason: str  # 遗忘原因: "低重要度" / "时间过长" / "访问频率低"
