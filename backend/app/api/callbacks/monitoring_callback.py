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
    """

    def __init__(self):
        """初始化回调处理器"""
        super().__init__()
        # 使用字典存储每个run_id的开始时间
        self._start_times: Dict[UUID, float] = {}
        logger.info("[MonitoringCallback] 已初始化")

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
        if response.llm_output and "token_usage" in response.llm_output:
            token_usage = response.llm_output["token_usage"]

            prompt_tokens = token_usage.get("prompt_tokens", 0)
            completion_tokens = token_usage.get("completion_tokens", 0)
            total_tokens = token_usage.get("total_tokens", 0)

            # 记录token使用量
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
