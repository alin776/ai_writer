"""
上下文管理 - 数据模型

实现三层记忆体系：
- ShortMemory: 短期记忆（最近N轮对话）
- SummaryMemory: 摘要记忆（滚动摘要）
- LongTermMemory: 长期记忆（向量存储，可选）
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

from app.services.context.token_counter import count_tokens


@dataclass
class Message:
    """消息模型"""
    role: str  # user, assistant, system
    content: str
    timestamp: float
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ShortMemory:
    """短期记忆 - 保留最近N轮对话"""
    messages: List[Message] = field(default_factory=list)
    max_turns: int = 6  # 保留最近6轮(12条消息)

    def add_message(self, message: Message):
        """添加消息"""
        self.messages.append(message)

        # 保持最近N轮（每轮2条消息：user + assistant）
        if len(self.messages) > self.max_turns * 2:
            self.messages = self.messages[-(self.max_turns * 2):]

    def get_token_count(self) -> int:
        """计算Token数量（使用精确计数）"""
        # 旧代码（注释保留）:
        # total = sum(len(msg.content) // 4 for msg in self.messages)
        # return total

        # ✅ 新代码：使用Token计数器
        total = sum(count_tokens(msg.content) for msg in self.messages)
        return total


@dataclass
class SummaryMemory:
    """摘要记忆 - 对话的滚动摘要"""
    summary: str = ""
    last_updated: float = 0
    important_facts: List[str] = field(default_factory=list)

    def get_token_count(self) -> int:
        """计算Token数量（使用精确计数）"""
        # 旧代码（注释保留）:
        # summary_tokens = len(self.summary) // 4
        # facts_tokens = sum(len(fact) // 4 for fact in self.important_facts)
        # return summary_tokens + facts_tokens

        # ✅ 新代码
        summary_tokens = count_tokens(self.summary)
        facts_tokens = sum(count_tokens(fact) for fact in self.important_facts)
        return summary_tokens + facts_tokens


@dataclass
class LongTermMemory:
    """长期记忆 - 向量存储（可选，暂未实现）"""
    enabled: bool = False
    vector_store: Optional[Any] = None

    def search(self, query: str, top_k: int = 3) -> List[str]:
        """检索相关记忆"""
        if not self.enabled or not self.vector_store:
            return []
        # TODO: 实现向量检索
        return []


@dataclass
class Context:
    """完整上下文 - 包含所有层次的记忆"""
    session_id: str
    short_memory: ShortMemory = field(default_factory=ShortMemory)
    summary_memory: SummaryMemory = field(default_factory=SummaryMemory)
    long_term_memory: LongTermMemory = field(default_factory=LongTermMemory)
    system_prompt: str = ""

    def get_total_tokens(self) -> int:
        """计算总Token数（使用精确计数）"""
        # 旧代码（注释保留）:
        # return (
        #     len(self.system_prompt) // 4 +
        #     self.short_memory.get_token_count() +
        #     self.summary_memory.get_token_count()
        # )

        # ✅ 新代码
        return (
            count_tokens(self.system_prompt) +
            self.short_memory.get_token_count() +
            self.summary_memory.get_token_count()
        )


@dataclass
class TokenBudget:
    """Token预算配置"""
    total: int = 8000  # 总预算（适配常见模型）
    system_prompt: float = 0.20  # 20% - 系统提示
    summary: float = 0.25  # 25% - 摘要上下文
    short_memory: float = 0.35  # 35% - 近期对话
    tools: float = 0.15  # 15% - 工具结果
    reserved: float = 0.05  # 5% - 预留区

    def get_budget(self, category: str) -> int:
        """获取某类别的Token预算"""
        ratios = {
            "system_prompt": self.system_prompt,
            "summary": self.summary,
            "short_memory": self.short_memory,
            "tools": self.tools,
            "reserved": self.reserved
        }
        return int(self.total * ratios.get(category, 0))

    def validate(self) -> bool:
        """验证预算配置是否合理（总和应为100%）"""
        total_ratio = (
            self.system_prompt +
            self.summary +
            self.short_memory +
            self.tools +
            self.reserved
        )
        return abs(total_ratio - 1.0) < 0.01  # 允许0.01的误差
