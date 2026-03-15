"""
Agent 计费上下文

在 Agent 会话期间，内部工具/技能可能多次调用 LLM，每次都经过
langchain_ai_service._track_api_cost() 独立记录。本模块通过 ContextVar
提供一个"累加器"，让 _track_api_cost() 在 Agent 上下文中只记录 AICallLog
而跳过独立积分扣除，最终由 agent.py 合并为 1 条 CreditTransaction。

非 Agent 场景（润色、翻译等）累加器为 None，走原有完整扣费路径，不受影响。
"""

from contextvars import ContextVar
from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class AgentBillingAccumulator:
    """单轮 Agent 对话的计费累加器"""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    cache_read_tokens: int = 0
    cache_creation_tokens: int = 0
    reasoning_tokens: int = 0
    prompt_cost_usd: float = 0.0
    completion_cost_usd: float = 0.0
    total_cost_usd: float = 0.0
    call_count: int = 0
    ai_call_log_ids: List[str] = field(default_factory=list)
    model_breakdown: dict = field(default_factory=dict)

    def accumulate(
        self,
        prompt_tokens: int,
        completion_tokens: int,
        prompt_cost: float,
        completion_cost: float,
        total_cost: float,
        cache_read: int = 0,
        cache_creation: int = 0,
        reasoning: int = 0,
        model_name: str = "unknown",
        ai_call_log_id: Optional[str] = None,
    ):
        self.prompt_tokens += prompt_tokens
        self.completion_tokens += completion_tokens
        self.cache_read_tokens += cache_read
        self.cache_creation_tokens += cache_creation
        self.reasoning_tokens += reasoning
        self.prompt_cost_usd += prompt_cost
        self.completion_cost_usd += completion_cost
        self.total_cost_usd += total_cost
        self.call_count += 1
        if ai_call_log_id:
            self.ai_call_log_ids.append(str(ai_call_log_id))
        # 按模型分组
        entry = self.model_breakdown.setdefault(model_name, {
            "input_tokens": 0, "output_tokens": 0,
            "cache_read": 0, "cache_creation": 0, "reasoning": 0,
        })
        entry["input_tokens"] += prompt_tokens
        entry["output_tokens"] += completion_tokens
        entry["cache_read"] += cache_read
        entry["cache_creation"] += cache_creation
        entry["reasoning"] += reasoning

    @property
    def total_tokens(self) -> int:
        return self.prompt_tokens + self.completion_tokens


agent_billing_ctx: ContextVar[Optional[AgentBillingAccumulator]] = ContextVar(
    "agent_billing_ctx", default=None
)


def get_agent_billing() -> Optional[AgentBillingAccumulator]:
    return agent_billing_ctx.get()


def set_agent_billing(acc: AgentBillingAccumulator):
    return agent_billing_ctx.set(acc)
