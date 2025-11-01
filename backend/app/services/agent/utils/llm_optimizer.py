"""
LLM调用优化器

提供LLM调用的性能优化，包括缓存、批量处理、智能选择等功能。
"""

import asyncio
import time
import hashlib
from typing import Dict, Any, List, Optional, Union, Callable
from dataclasses import dataclass
from functools import wraps
from datetime import datetime, timedelta
from collections import defaultdict

from .performance import cache_result, performance_optimizer
from .error_handler import robust_retry
from .logger import get_logger

logger = get_logger("llm_optimizer")


@dataclass
class LLMRequest:
    """LLM请求"""
    prompt: str
    model: str
    temperature: float
    max_tokens: int
    user_id: Optional[str] = None
    conversation_id: Optional[str] = None
    metadata: Dict[str, Any] = None

    def to_cache_key(self) -> str:
        """生成缓存键"""
        content = f"{self.prompt}:{self.model}:{self.temperature}:{self.max_tokens}"
        return hashlib.md5(content.encode()).hexdigest()

    def estimate_tokens(self) -> int:
        """估算token数量"""
        # 简单的token估算：约4个字符 = 1个token
        return len(self.prompt) // 4 + len(self.prompt) % 4


@dataclass
class LLMResponse:
    """LLM响应"""
    content: str
    model: str
    tokens_used: Dict[str, int]
    cost: float
    duration: float
    cached: bool = False
    metadata: Dict[str, Any] = None


class LLMBatchProcessor:
    """LLM批量处理器"""

    def __init__(self, batch_size: int = 5, max_wait_time: float = 0.5):
        self.batch_size = batch_size
        self.max_wait_time = max_wait_time
        self._queue: List[LLMRequest] = []
        self._processing = False
        self._results: Dict[str, LLMResponse] = {}

    def add_request(self, request: LLMRequest) -> str:
        """添加请求到批处理队列"""
        request_id = request.to_cache_key()
        self._queue.append((request_id, request))

        # 如果达到批处理大小或开始处理，触发处理
        if (len(self._queue) >= self.batch_size or
            not self._processing and len(self._queue) > 0):
            asyncio.create_task(self._process_batch())

        return request_id

    async def _process_batch(self) -> None:
        """处理批量请求"""
        if self._processing or not self._queue:
            return

        self._processing = True
        batch = self._queue.copy()
        self._queue.clear()

        try:
            # 并行处理所有请求
            tasks = [self._process_single_request(request_id, request)
                     for request_id, request in batch]
            await asyncio.gather(*tasks, return_exceptions=True)

        except Exception as e:
            logger.error(f"Batch processing failed: {e}")

        finally:
            self._processing = False

    async def _process_single_request(self, request_id: str, request: LLMRequest) -> LLMResponse:
        """处理单个请求"""
        start_time = time.time()

        try:
            # 这里应该调用实际的LLM服务
            # result = await ai_service.call_ai(...)
            # 模拟LLM调用
            await asyncio.sleep(0.1)  # 模拟延迟

            duration = time.time() - start_time
            cost = self._estimate_cost(request.model, request.estimate_tokens())

            response = LLMResponse(
                content="Mock response for batch processing",
                model=request.model,
                tokens_used={"input": request.estimate_tokens(), "output": 100},
                cost=cost,
                duration=duration,
                cached=False
            )

            self._results[request_id] = response
            return response

        except Exception as e:
            error_response = LLMResponse(
                content=f"Error: {str(e)}",
                model=request.model,
                tokens_used={"input": 0, "output": 0},
                cost=0.0,
                duration=time.time() - start_time,
                cached=False
            )
            self._results[request_id] = error_response
            return error_response

    def get_result(self, request_id: str) -> Optional[LLMResponse]:
        """获取处理结果"""
        return self._results.get(request_id)


class LLMCache:
    """LLM缓存管理器"""

    def __init__(self, max_size: int = 1000, default_ttl: float = 3600):
        self.max_size = max_size
        self.default_ttl = default_ttl
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._cache_stats = {
            "hits": 0,
            "misses": 0,
            "total_requests": 0,
            "total_cost_saved": 0.0
        }

    def get(self, cache_key: str) -> Optional[LLMResponse]:
        """获取缓存响应"""
        self._cache_stats["total_requests"] += 1

        if cache_key in self._cache:
            cache_entry = self._cache[cache_key]

            # 检查是否过期
            if self._is_expired(cache_entry):
                del self._cache[cache_key]
                self._cache_stats["misses"] += 1
                return None

            self._cache_stats["hits"] += 1
            self._cache_stats["total_cost_saved"] += cache_entry["cost"]

            return LLMResponse(
                content=cache_entry["content"],
                model=cache_entry["model"],
                tokens_used=cache_entry["tokens_used"],
                cost=cache_entry["cost"],
                duration=0.0,  # 缓存命中时duration为0
                cached=True,
                metadata=cache_entry.get("metadata", {})
            )

        self._cache_stats["misses"] += 1
        return None

    def set(self, cache_key: str, response: LLMResponse, ttl: Optional[float] = None) -> None:
        """设置缓存响应"""
        if len(self._cache) >= self.max_size:
            self._evict_oldest()

        ttl = ttl or self.default_ttl
        self._cache[cache_key] = {
            "content": response.content,
            "model": response.model,
            "tokens_used": response.tokens_used,
            "cost": response.cost,
            "timestamp": datetime.now(),
            "ttl": ttl,
            "metadata": response.metadata or {}
        }

    def _is_expired(self, cache_entry: Dict[str, Any]) -> bool:
        """检查缓存是否过期"""
        if "ttl" not in cache_entry:
            return False

        elapsed = (datetime.now() - cache_entry["timestamp"]).total_seconds()
        return elapsed > cache_entry["ttl"]

    def _evict_oldest(self) -> None:
        """删除最旧的缓存条目"""
        if not self._cache:
            return

        oldest_key = min(self._cache.keys(),
                          key=lambda k: self._cache[k]["timestamp"])
        del self._cache[oldest_key]

    def clear(self) -> None:
        """清空缓存"""
        self._cache.clear()
        self._cache_stats = {
            "hits": 0,
            "misses": 0,
            "total_requests": 0,
            "total_cost_saved": 0.0
        }

    def get_stats(self) -> Dict[str, Any]:
        """获取缓存统计"""
        total = self._cache_stats["total_requests"]
        hits = self._cache_stats["hits"]
        hit_rate = hits / total if total > 0 else 0

        return {
            "cache_size": len(self._cache),
            "max_size": self.max_size,
            "hits": hits,
            "misses": self._cache_stats["misses"],
            "hit_rate": hit_rate,
            "total_cost_saved": self._cache_stats["total_cost_saved"],
            "total_requests": total
        }

    def _estimate_cost(self, model: str, tokens: int) -> float:
        """估算成本"""
        cost_per_million = {
            "gemini-2.5-flash-lite": {"input": 0.03, "output": 0.12},
            "gemini-2.5-flash": {"input": 0.075, "output": 0.30},
            "gemini-2.5-pro": {"input": 1.25, "output": 5.00},
            "gpt-4": {"input": 10.00, "output": 30.00},
            "gpt-3.5-turbo": {"input": 0.50, "output": 1.50}
        }

        model_cost = cost_per_million.get(model, {"input": 1.0, "output": 1.0})
        # 假设输入输出各占50%
        return (model_cost["input"] * 0.5 + model_cost["output"] * 0.5) * tokens / 1000000


class LLMOptimizer:
    """LLM优化器"""

    def __init__(self):
        self.cache = LLMCache(max_size=1000, default_ttl=1800)  # 30分钟TTL
        self.batch_processor = LLMBatchProcessor(batch_size=5, max_wait_time=0.5)
        self._request_stats = defaultdict(list)
        self._model_costs = {
            "gemini-2.5-flash-lite": {"input": 0.03, "output": 0.12},
            "gemini-2.5-flash": {"input": 0.075, "output": 0.30},
            "gemini-2.5-pro": {"input": 1.25, "output": 5.00}
        }

    @cache_result(ttl=1800)  # 30分钟缓存
    def optimize_prompt(self, prompt: str) -> str:
        """优化Prompt"""
        # 移除多余的空白字符
        optimized = ' '.join(prompt.split())

        # 移除重复的换行
        while '\n\n\n' in optimized:
            optimized = optimized.replace('\n\n\n', '\n\n')

        return optimized

    @cache_result(ttl=300)  # 5分钟缓存
    def estimate_tokens(self, text: str) -> int:
        """估算token数量"""
        # 更精确的token估算
        # 约1个token = 4个字符（中文字符约2个字符）
        # 英文平均约4个字符，中文平均约2个字符
        chinese_chars = len([c for c in text if '\u4e00' <= c <= '\u9fff'])
        english_chars = len(text) - chinese_chars

        return chinese_chars // 2 + english_chars // 4

    def get_optimal_model(self, complexity: str, max_cost: Optional[float] = None) -> str:
        """获取最优模型"""
        model_mapping = {
            "simple": "gemini-2.5-flash-lite",
            "medium": "gemini-2.5-flash",
            "complex": "gemini-2.5-pro"
        }

        base_model = model_mapping.get(complexity, "gemini-2.5-flash")

        # 如果有成本限制，选择最便宜的模型
        if max_cost is not None:
            for model, costs in self._model_costs.items():
                estimated_cost = (costs["input"] + costs["output"]) * 0.0001  # 估算100 tokens
                if estimated_cost <= max_cost:
                    base_model = model
                    break

        return base_model

    async def call_llm_with_cache(
        self,
        prompt: str,
        model: str = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        user_id: Optional[str] = None,
        conversation_id: Optional[str] = None,
        metadata: Dict[str, Any] = None
    ) -> LLMResponse:
        """带缓存的LLM调用"""
        # 优化prompt
        optimized_prompt = self.optimize_prompt(prompt)

        # 选择最优模型
        if model is None:
            model = self.get_optimal_model("medium")

        # 创建请求
        request = LLMRequest(
            prompt=optimized_prompt,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            user_id=user_id,
            conversation_id=conversation_id,
            metadata=metadata
        )

        # 检查缓存
        cache_key = request.to_cache_key()
        cached_response = self.cache.get(cache_key)
        if cached_response:
            logger.debug(f"LLM cache hit for model {model}")
            return cached_response

        # 这里应该调用实际的LLM服务
        start_time = time.time()

        # 模拟LLM调用
        await asyncio.sleep(0.1)

        # 实际项目中应该调用：
        # response_content = await ai_service.call_ai(
        #     optimized_prompt,
        #     model=model,
        #     temperature=temperature,
        #     max_tokens=max_tokens
        # )
        response_content = f"Optimized response for model {model}"

        duration = time.time() - start_time
        estimated_tokens = self.estimate_tokens(optimized_prompt + response_content)
        cost = self.cache._estimate_cost(model, estimated_tokens)

        response = LLMResponse(
            content=response_content,
            model=model,
            tokens_used={"input": self.estimate_tokens(optimized_prompt),
                           "output": self.estimate_tokens(response_content)},
            cost=cost,
            duration=duration,
            cached=False,
            metadata=metadata
        )

        # 缓存结果
        self.cache.set(cache_key, response, ttl=1800)

        # 记录统计
        self._record_request_stats(request, response)

        return response

    async def batch_call_llm(
        self,
        requests: List[LLMRequest]
    ) -> List[LLMResponse]:
        """批量调用LLM"""
        results = []

        for request in requests:
            request_id = self.batch_processor.add_request(request)
            results.append(request_id)

        # 等待所有请求完成
        await asyncio.sleep(0.2)  # 给批处理器一些时间

        # 获取结果
        for request_id in results:
            result = self.batch_processor.get_result(request_id)
            if result:
                results[results.index(request_id)] = result

        return results

    def _record_request_stats(self, request: LLMRequest, response: LLMResponse) -> None:
        """记录请求统计"""
        model = request.model
        self._request_stats[model].append({
            "timestamp": datetime.now(),
            "duration": response.duration,
            "tokens_used": response.tokens_used,
            "cost": response.cost,
            "cached": response.cached
        })

        # 只保留最近100条记录
        if len(self._request_stats[model]) > 100:
            self._request_stats[model] = self._request_stats[model][-100:]

    def get_performance_stats(self) -> Dict[str, Any]:
        """获取性能统计"""
        cache_stats = self.cache.get_stats()

        # 计算模型性能统计
        model_stats = {}
        for model, stats in self._request_stats.items():
            if stats:
                avg_duration = sum(s["duration"] for s in stats) / len(stats)
                avg_cost = sum(s["cost"] for s in stats) / len(stats)
                avg_tokens = sum(sum(s["tokens_used"].values()) for s in stats) / len(stats)
                hit_rate = sum(1 for s in stats if s["cached"]) / len(stats)

                model_stats[model] = {
                    "requests": len(stats),
                    "avg_duration": avg_duration,
                    "avg_cost": avg_cost,
                    "avg_tokens": avg_tokens,
                    "hit_rate": hit_rate
                }

        return {
            "cache": cache_stats,
            "models": model_stats,
            "timestamp": datetime.now().isoformat()
        }

    def clear_cache(self) -> None:
        """清空缓存"""
        self.cache.clear()
        self._request_stats.clear()

    def clear_model_cache(self, model: str) -> None:
        """清空特定模型的缓存"""
        keys_to_remove = []
        for key, entry in self.cache._cache.items():
            if entry.get("model") == model:
                keys_to_remove.append(key)

        for key in keys_to_remove:
            del self.cache._cache[key]


# 全局LLM优化器实例
llm_optimizer = LLMOptimizer()


def get_llm_optimizer() -> LLMOptimizer:
    """获取全局LLM优化器实例"""
    return llm_optimizer


# 便捷函数
def optimized_llm_call(
    prompt: str,
    model: str = None,
    temperature: float = 0.7,
    max_tokens: int = 2000,
    **kwargs
):
    """优化的LLM调用装饰器"""
    return llm_optimizer.call_llm_with_cache(
        prompt=prompt,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        **kwargs
    )


# 缓存管理函数
def clear_llm_cache() -> None:
    """清空LLM缓存"""
    llm_optimizer.clear_cache()


def get_llm_performance_stats() -> Dict[str, Any]:
    """获取LLM性能统计"""
    return llm_optimizer.get_performance_stats()