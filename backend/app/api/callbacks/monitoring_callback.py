"""
LangChain监控回调 - 用于ChatOpenAI模式

实现LangChain的AsyncCallbackHandler接口，监控LLM调用的各项指标
"""

import time
import logging
from typing import Any, Dict, List, Optional
from uuid import UUID

from langchain_core.callbacks import AsyncCallbackHandler
from langchain_core.outputs import LLMResult

from app.services.agent.utils.monitoring import (
    increment_counter,
    record_timer,
    set_gauge
)

logger = logging.getLogger(__name__)


class MonitoringCallbackHandler(AsyncCallbackHandler):
    """
    LangChain监控回调处理器

    监控指标：
    - llm_calls_total: LLM调用总数（按模型分类）
    - llm_calls_success: LLM调用成功次数
    - llm_calls_error: LLM调用失败次数（按错误类型分类）
    - llm_response_time: LLM响应时间（秒）
    - llm_token_usage_prompt: Prompt token使用量
    - llm_token_usage_completion: Completion token使用量
    - llm_token_usage_total: 总token使用量

    支持AICallLog数据库记录（通过set_context动态设置）
    """

    def __init__(
        self,
        user_id: Optional[str] = None,
        db: Optional[Any] = None,
        work_id: Optional[str] = None,
        chapter_id: Optional[str] = None,
        operation_type: str = "agent_llm_call"
    ):
        """初始化回调处理器

        Args:
            user_id: 用户ID（用于AICallLog记录）
            db: 数据库会话（用于AICallLog记录）
            work_id: 作品ID（用于AICallLog记录）
            chapter_id: 章节ID（用于AICallLog记录）
            operation_type: 操作类型（用于AICallLog记录）
        """
        super().__init__()
        # 使用字典存储每个run_id的开始时间
        self._start_times: Dict[UUID, float] = {}
        self.user_id = user_id
        self.db = db
        self.work_id = work_id
        self.chapter_id = chapter_id
        self.operation_type = operation_type
        logger.info(
            f"[MonitoringCallback] 已初始化 (user_id={user_id}, "
            f"db={'enabled' if db else 'disabled'}, operation_type={operation_type})"
        )

    def set_context(
        self,
        user_id: Optional[str] = None,
        db: Optional[Any] = None,
        work_id: Optional[str] = None,
        chapter_id: Optional[str] = None
    ):
        """动态设置上下文信息（用于全局callback实例）

        Args:
            user_id: 用户ID
            db: 数据库会话
            work_id: 作品ID
            chapter_id: 章节ID
        """
        self.user_id = user_id
        self.db = db
        self.work_id = work_id
        self.chapter_id = chapter_id
        logger.debug(
            f"[MonitoringCallback] 上下文已更新: user_id={user_id}, "
            f"db={'enabled' if db else 'disabled'}"
        )

    async def on_llm_start(
        self,
        serialized: Dict[str, Any],
        prompts: List[str],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """
        LLM调用开始时的回调

        Args:
            serialized: 序列化的LLM配置
            prompts: 输入提示词列表
            run_id: 当前运行ID
            parent_run_id: 父运行ID（如果有）
            tags: 标签列表
            metadata: 元数据
        """
        # 记录开始时间
        self._start_times[run_id] = time.time()

        # 提取模型名称
        model_name = self._extract_model_name(serialized, kwargs)

        # 增加调用计数
        increment_counter(
            "llm_calls_total",
            labels={"model": model_name, "source": "chatgpt"}
        )

        logger.debug(
            f"[MonitoringCallback] LLM调用开始: run_id={run_id}, "
            f"model={model_name}, prompts_count={len(prompts)}"
        )

    async def on_llm_end(
        self,
        response: LLMResult,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> None:
        """
        LLM调用成功结束时的回调

        Args:
            response: LLM响应结果
            run_id: 当前运行ID
            parent_run_id: 父运行ID（如果有）
            tags: 标签列表
        """
        # 计算响应时间
        start_time = self._start_times.pop(run_id, None)
        if start_time:
            duration = time.time() - start_time
        else:
            logger.warning(f"[MonitoringCallback] 未找到run_id={run_id}的开始时间")
            duration = 0

        # 提取模型名称
        model_name = self._extract_model_name_from_response(response)

        # 记录响应时间
        record_timer(
            "llm_response_time",
            duration,
            labels={"model": model_name, "source": "chatgpt"}
        )

        # 增加成功计数
        increment_counter(
            "llm_calls_success",
            labels={"model": model_name, "source": "chatgpt"}
        )

        # 提取token使用量
        prompt_tokens = 0
        completion_tokens = 0
        total_tokens = 0

        if response.llm_output and "token_usage" in response.llm_output:
            token_usage = response.llm_output["token_usage"]

            prompt_tokens = token_usage.get("prompt_tokens", 0)
            completion_tokens = token_usage.get("completion_tokens", 0)
            total_tokens = token_usage.get("total_tokens", 0)

            # 记录token使用量（metrics）
            set_gauge(
                "llm_token_usage_prompt",
                prompt_tokens,
                labels={"model": model_name, "source": "chatgpt"}
            )
            set_gauge(
                "llm_token_usage_completion",
                completion_tokens,
                labels={"model": model_name, "source": "chatgpt"}
            )
            set_gauge(
                "llm_token_usage_total",
                total_tokens,
                labels={"model": model_name, "source": "chatgpt"}
            )

            logger.info(
                f"[MonitoringCallback] LLM调用成功: run_id={run_id}, "
                f"model={model_name}, duration={duration:.2f}s, "
                f"tokens={total_tokens} (prompt={prompt_tokens}, completion={completion_tokens})"
            )

            # 记录到AICallLog数据库（如果配置了user_id和db）
            if self.user_id and self.db and total_tokens > 0:
                try:
                    from app.models.ai_call_log import AICallLog
                    from app.utils.cost_calculator import CostCalculator

                    # 计算成本
                    cost_data = CostCalculator.calculate_cost(
                        model_name=model_name,
                        prompt_tokens=prompt_tokens,
                        completion_tokens=completion_tokens
                    )

                    # 创建AICallLog记录
                    call_log = AICallLog(
                        user_id=UUID(self.user_id),
                        model_name=model_name,
                        operation_type=self.operation_type,
                        work_id=UUID(self.work_id) if self.work_id else None,
                        chapter_id=UUID(self.chapter_id) if self.chapter_id else None,
                        prompt_tokens=prompt_tokens,
                        completion_tokens=completion_tokens,
                        total_tokens=total_tokens,
                        prompt_cost=cost_data["prompt_cost"],
                        completion_cost=cost_data["completion_cost"],
                        total_cost=cost_data["total_cost"],
                        duration_ms=int(duration * 1000),
                        is_success=True,
                        extra_data={
                            "source": "agent_chatgpt",
                            "run_id": str(run_id),
                            "parent_run_id": str(parent_run_id) if parent_run_id else None,
                            "tags": tags if tags else []
                        }
                    )

                    self.db.add(call_log)
                    await self.db.flush()

                    logger.info(
                        f"[Token记录] Agent LLM调用: {total_tokens} tokens "
                        f"(prompt={prompt_tokens}, completion={completion_tokens}), "
                        f"成本=${cost_data['total_cost']:.6f}, "
                        f"耗时={int(duration * 1000)}ms"
                    )

                except Exception as e:
                    logger.error(f"记录token使用到AICallLog失败: {e}")
                    # 记录失败不影响主流程

        else:
            logger.info(
                f"[MonitoringCallback] LLM调用成功: run_id={run_id}, "
                f"model={model_name}, duration={duration:.2f}s, "
                f"tokens=N/A"
            )

    async def on_llm_error(
        self,
        error: BaseException,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> None:
        """
        LLM调用失败时的回调

        Args:
            error: 异常对象
            run_id: 当前运行ID
            parent_run_id: 父运行ID（如果有）
            tags: 标签列表
        """
        # 计算响应时间（即使失败也要记录）
        start_time = self._start_times.pop(run_id, None)
        if start_time:
            duration = time.time() - start_time
        else:
            duration = 0

        # 提取模型名称（从kwargs或使用默认值）
        model_name = kwargs.get("invocation_params", {}).get("model_name", "unknown")

        # 记录响应时间
        record_timer(
            "llm_response_time",
            duration,
            labels={"model": model_name, "source": "chatgpt"}
        )

        # 增加错误计数
        error_type = type(error).__name__
        increment_counter(
            "llm_calls_error",
            labels={
                "model": model_name,
                "source": "chatgpt",
                "error_type": error_type
            }
        )

        logger.error(
            f"[MonitoringCallback] LLM调用失败: run_id={run_id}, "
            f"model={model_name}, duration={duration:.2f}s, "
            f"error_type={error_type}, error={str(error)}"
        )

    def _extract_model_name(
        self,
        serialized: Dict[str, Any],
        kwargs: Dict[str, Any]
    ) -> str:
        """
        从序列化配置或kwargs中提取模型名称

        Args:
            serialized: 序列化的LLM配置
            kwargs: 其他参数

        Returns:
            模型名称（如果找不到则返回"unknown"）
        """
        # 尝试从多个位置提取模型名称
        # 1. 从kwargs的invocation_params中提取
        if "invocation_params" in kwargs:
            model_name = kwargs["invocation_params"].get("model_name")
            if model_name:
                return model_name

        # 2. 从serialized中提取
        if "kwargs" in serialized:
            model_name = serialized["kwargs"].get("model_name")
            if model_name:
                return model_name

        # 3. 从serialized的id字段提取（可能包含模型信息）
        if "id" in serialized and isinstance(serialized["id"], list):
            # id通常是 ["langchain", "chat_models", "openai", "ChatOpenAI"]
            # 我们从kwargs中的model提取
            pass

        # 4. 默认值
        return "unknown"

    def _extract_model_name_from_response(self, response: LLMResult) -> str:
        """
        从LLM响应中提取模型名称

        Args:
            response: LLM响应结果

        Returns:
            模型名称（如果找不到则返回"unknown"）
        """
        # 尝试从llm_output中提取
        if response.llm_output:
            if "model_name" in response.llm_output:
                return response.llm_output["model_name"]

            # OpenAI API通常在system_fingerprint中包含模型信息
            if "system_fingerprint" in response.llm_output:
                # 可以从fingerprint中解析，但通常不可靠
                pass

        # 默认值
        return "unknown"
