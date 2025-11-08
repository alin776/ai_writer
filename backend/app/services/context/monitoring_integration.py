"""
上下文管理监控集成

为ContextManager提供全面的监控指标收集能力
- Token计数监控
- 摘要生成监控
- 上下文构建监控
- 压缩操作监控
"""

import time
import logging
import functools
from typing import Optional, Callable, Any

from app.services.agent.utils.monitoring import MetricsCollector, MetricType

logger = logging.getLogger(__name__)

# 全局监控收集器（懒加载）
_metrics_collector: Optional[MetricsCollector] = None


def get_metrics_collector() -> MetricsCollector:
    """获取全局监控收集器（单例）"""
    global _metrics_collector
    if _metrics_collector is None:
        _metrics_collector = MetricsCollector(max_history=10000)
        logger.info("✅ ContextManager监控收集器已初始化")
    return _metrics_collector


# ==================== 监控指标定义 ====================

class ContextMetrics:
    """上下文管理监控指标名称常量"""

    # Token计数相关（4个指标）
    TOKEN_COUNT_TOTAL = "context_token_count_total"  # 总调用次数
    TOKEN_COUNT_DURATION = "context_token_count_duration"  # 计数耗时
    TOKEN_COUNT_RESULT = "context_token_count_result"  # 计数结果（Token数）
    TOKEN_COUNT_STRATEGY = "context_token_count_strategy"  # 使用的策略

    # 摘要生成相关（6个指标）
    SUMMARY_GENERATION_TOTAL = "context_summary_generation_total"  # 总调用次数
    SUMMARY_GENERATION_DURATION = "context_summary_generation_duration"  # 生成耗时
    SUMMARY_GENERATION_SUCCESS = "context_summary_generation_success"  # 成功次数
    SUMMARY_GENERATION_FALLBACK = "context_summary_generation_fallback"  # 降级次数
    SUMMARY_LENGTH = "context_summary_length"  # 摘要长度
    SUMMARY_MESSAGE_COUNT = "context_summary_message_count"  # 处理的消息数

    # 上下文构建相关（4个指标）
    BUILD_TOTAL = "context_build_total"  # 构建次数
    BUILD_DURATION = "context_build_duration"  # 构建耗时
    BUILD_TOKEN_COUNT = "context_build_token_count"  # 构建后的Token数
    BUILD_MESSAGE_COUNT = "context_build_message_count"  # 消息数量

    # 上下文更新相关（2个指标）
    UPDATE_TOTAL = "context_update_total"  # 更新次数
    UPDATE_DURATION = "context_update_duration"  # 更新耗时

    # 压缩相关（2个指标）
    COMPRESSION_RATIO = "context_compression_ratio"  # 压缩比率
    COMPRESSION_TOTAL = "context_compression_total"  # 压缩次数

    # 内存使用相关（2个指标）
    SHORT_MEMORY_SIZE = "context_short_memory_size"  # 短期记忆大小
    SUMMARY_MEMORY_SIZE = "context_summary_memory_size"  # 摘要记忆大小


# ==================== 监控装饰器 ====================

def monitor_token_counting(func: Callable) -> Callable:
    """
    监控Token计数操作

    记录指标:
    - 调用次数
    - 计数耗时
    - Token数量
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        collector = get_metrics_collector()
        start_time = time.time()

        try:
            # 执行Token计数
            result = func(*args, **kwargs)

            # 记录成功指标
            duration = time.time() - start_time

            # 增加调用次数
            collector.increment_counter(ContextMetrics.TOKEN_COUNT_TOTAL)

            # 记录耗时
            collector.record_timer(
                ContextMetrics.TOKEN_COUNT_DURATION,
                duration
            )

            # 记录Token数量（如果结果是数字）
            if isinstance(result, (int, float)):
                collector.set_gauge(
                    ContextMetrics.TOKEN_COUNT_RESULT,
                    result
                )

            logger.debug(f"[Monitor] Token计数: {result} tokens, 耗时 {duration*1000:.2f}ms")
            return result

        except Exception as e:
            logger.error(f"[Monitor] Token计数失败: {e}")
            raise

    return wrapper


def monitor_summary_generation(func: Callable) -> Callable:
    """
    监控摘要生成操作

    记录指标:
    - 调用次数
    - 生成耗时
    - 成功/降级次数
    - 摘要长度
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        collector = get_metrics_collector()
        start_time = time.time()

        try:
            # 执行摘要生成
            result = await func(*args, **kwargs)

            # 记录成功指标
            duration = time.time() - start_time

            # 增加调用次数
            collector.increment_counter(ContextMetrics.SUMMARY_GENERATION_TOTAL)

            # 记录耗时
            collector.record_timer(
                ContextMetrics.SUMMARY_GENERATION_DURATION,
                duration
            )

            # 记录摘要长度
            if isinstance(result, str):
                collector.set_gauge(
                    ContextMetrics.SUMMARY_LENGTH,
                    len(result)
                )

                # 判断是否使用了降级策略（简单检测）
                if "用户请求:" in result and "|" in result:
                    # 降级策略的摘要格式
                    collector.increment_counter(ContextMetrics.SUMMARY_GENERATION_FALLBACK)
                    logger.info(f"[Monitor] 摘要生成（降级策略）: {len(result)}字符, 耗时 {duration:.2f}s")
                else:
                    # LLM生成的摘要
                    collector.increment_counter(ContextMetrics.SUMMARY_GENERATION_SUCCESS)
                    logger.info(f"[Monitor] 摘要生成（LLM）: {len(result)}字符, 耗时 {duration:.2f}s")

            return result

        except Exception as e:
            logger.error(f"[Monitor] 摘要生成失败: {e}")
            # 增加降级计数（因为异常会触发降级）
            collector.increment_counter(ContextMetrics.SUMMARY_GENERATION_FALLBACK)
            raise

    return wrapper


def monitor_context_build(func: Callable) -> Callable:
    """
    监控上下文构建操作

    记录指标:
    - 构建次数
    - 构建耗时
    - Token数量
    - 消息数量
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        collector = get_metrics_collector()
        start_time = time.time()

        try:
            # 执行上下文构建
            result = await func(*args, **kwargs)

            # 记录指标
            duration = time.time() - start_time

            # 增加构建次数
            collector.increment_counter(ContextMetrics.BUILD_TOTAL)

            # 记录耗时
            collector.record_timer(
                ContextMetrics.BUILD_DURATION,
                duration
            )

            # 记录Token数和消息数（从结果中提取）
            if isinstance(result, dict):
                metadata = result.get("metadata", {})
                token_count = metadata.get("token_count", 0)
                message_count = len(result.get("messages", []))

                collector.set_gauge(ContextMetrics.BUILD_TOKEN_COUNT, token_count)
                collector.set_gauge(ContextMetrics.BUILD_MESSAGE_COUNT, message_count)

                logger.info(
                    f"[Monitor] 上下文构建: {message_count}条消息, "
                    f"{token_count} tokens, 耗时 {duration*1000:.2f}ms"
                )

            return result

        except Exception as e:
            logger.error(f"[Monitor] 上下文构建失败: {e}")
            raise

    return wrapper


def monitor_context_update(func: Callable) -> Callable:
    """
    监控上下文更新操作

    记录指标:
    - 更新次数
    - 更新耗时
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        collector = get_metrics_collector()
        start_time = time.time()

        try:
            # 执行上下文更新
            result = await func(*args, **kwargs)

            # 记录指标
            duration = time.time() - start_time

            # 增加更新次数
            collector.increment_counter(ContextMetrics.UPDATE_TOTAL)

            # 记录耗时
            collector.record_timer(
                ContextMetrics.UPDATE_DURATION,
                duration
            )

            logger.debug(f"[Monitor] 上下文更新: 耗时 {duration*1000:.2f}ms")

            return result

        except Exception as e:
            logger.error(f"[Monitor] 上下文更新失败: {e}")
            raise

    return wrapper


# ==================== 指标记录函数 ====================

def record_compression_metrics(
    original_tokens: int,
    compressed_tokens: int,
    session_id: str
):
    """
    记录压缩操作指标

    Args:
        original_tokens: 压缩前Token数
        compressed_tokens: 压缩后Token数
        session_id: 会话ID
    """
    collector = get_metrics_collector()

    # 增加压缩次数
    collector.increment_counter(ContextMetrics.COMPRESSION_TOTAL)

    # 计算压缩比率
    if original_tokens > 0:
        ratio = compressed_tokens / original_tokens
        collector.set_gauge(ContextMetrics.COMPRESSION_RATIO, ratio)

        logger.info(
            f"[Monitor] 上下文压缩 [{session_id}]: "
            f"{original_tokens} → {compressed_tokens} tokens "
            f"(压缩比 {ratio:.2%})"
        )


def record_memory_size(
    short_memory_size: int,
    summary_memory_size: int,
    session_id: str
):
    """
    记录内存使用指标

    Args:
        short_memory_size: 短期记忆大小（消息数）
        summary_memory_size: 摘要记忆大小（字符数）
        session_id: 会话ID
    """
    collector = get_metrics_collector()

    # 记录内存大小
    collector.set_gauge(ContextMetrics.SHORT_MEMORY_SIZE, short_memory_size)
    collector.set_gauge(ContextMetrics.SUMMARY_MEMORY_SIZE, summary_memory_size)

    logger.debug(
        f"[Monitor] 内存使用 [{session_id}]: "
        f"短期记忆={short_memory_size}条, "
        f"摘要记忆={summary_memory_size}字符"
    )


# ==================== 监控查询接口 ====================

def get_context_metrics_summary() -> dict:
    """
    获取上下文管理监控指标摘要

    Returns:
        监控指标摘要字典
    """
    collector = get_metrics_collector()

    summary = {
        "token_counting": {
            "total_calls": collector._counters.get(ContextMetrics.TOKEN_COUNT_TOTAL, 0),
            "current_tokens": collector._gauges.get(ContextMetrics.TOKEN_COUNT_RESULT, 0),
        },
        "summary_generation": {
            "total_calls": collector._counters.get(ContextMetrics.SUMMARY_GENERATION_TOTAL, 0),
            "success_count": collector._counters.get(ContextMetrics.SUMMARY_GENERATION_SUCCESS, 0),
            "fallback_count": collector._counters.get(ContextMetrics.SUMMARY_GENERATION_FALLBACK, 0),
            "current_length": collector._gauges.get(ContextMetrics.SUMMARY_LENGTH, 0),
        },
        "context_build": {
            "total_builds": collector._counters.get(ContextMetrics.BUILD_TOTAL, 0),
            "current_tokens": collector._gauges.get(ContextMetrics.BUILD_TOKEN_COUNT, 0),
            "current_messages": collector._gauges.get(ContextMetrics.BUILD_MESSAGE_COUNT, 0),
        },
        "compression": {
            "total_compressions": collector._counters.get(ContextMetrics.COMPRESSION_TOTAL, 0),
            "compression_ratio": collector._gauges.get(ContextMetrics.COMPRESSION_RATIO, 0),
        },
        "memory": {
            "short_memory_size": collector._gauges.get(ContextMetrics.SHORT_MEMORY_SIZE, 0),
            "summary_memory_size": collector._gauges.get(ContextMetrics.SUMMARY_MEMORY_SIZE, 0),
        }
    }

    return summary
