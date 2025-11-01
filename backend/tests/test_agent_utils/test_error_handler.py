"""
错误处理系统测试

测试统一错误处理器、重试机制、熔断器等功能
"""

import pytest
import asyncio
import time
from unittest.mock import Mock, patch
from datetime import datetime

from app.services.agent.utils import (
    ErrorHandler,
    ErrorInfo,
    ErrorSeverity,
    ErrorCategory,
    RetryStrategy,
    FallbackStrategy,
    global_error_handler,
    robust_retry,
    circuit_breaker,
    timeout_handler,
    safe_execute,
    safe_execute_async
)


class TestErrorHandler:
    """测试错误处理器"""

    def setup_method(self):
        """测试前准备"""
        self.error_handler = ErrorHandler()

    def test_classify_network_error(self):
        """测试网络错误分类"""
        error = ConnectionError("Network timeout")
        context = {"user_id": "test_user"}

        error_info = self.error_handler.classify_error(error, context)

        assert error_info.category == ErrorCategory.NETWORK
        assert error_info.severity == ErrorSeverity.MEDIUM
        assert error_info.user_id == "test_user"
        assert error_info.original_error == error

    def test_classify_redis_error(self):
        """测试Redis错误分类"""
        error = Exception("redis connection failed")
        context = {"action": "memory_add"}

        error_info = self.error_handler.classify_error(error, context)

        assert error_info.category == ErrorCategory.REDIS
        assert error_info.severity == ErrorSeverity.MEDIUM
        assert error_info.action_name == "memory_add"

    def test_classify_timeout_error(self):
        """测试超时错误分类"""
        error = TimeoutError("Operation timeout")
        context = {"conversation_id": "test_conv"}

        error_info = self.error_handler.classify_error(error, context)

        assert error_info.category == ErrorCategory.TIMEOUT
        assert error_info.severity == ErrorSeverity.MEDIUM
        assert error_info.conversation_id == "test_conv"

    def test_classify_validation_error(self):
        """测试验证错误分类"""
        error = ValueError("Invalid input")
        context = {}

        error_info = self.error_handler.classify_error(error, context)

        assert error_info.category == ErrorCategory.VALIDATION
        assert error_info.severity == ErrorSeverity.LOW

    def test_handle_error(self):
        """测试错误处理"""
        error_info = ErrorInfo(
            category=ErrorCategory.NETWORK,
            severity=ErrorSeverity.MEDIUM,
            message="Test error",
            original_error=Exception("test"),
            context={"test": True},
            timestamp=datetime.now()
        )

        result = self.error_handler.handle_error(error_info)

        assert result["status"] == "warning"
        assert result["should_retry"] == True
        assert result["error"] == error_info

    def test_get_error_summary(self):
        """测试错误统计摘要"""
        # 添加一些错误
        for i in range(3):
            error_info = ErrorInfo(
                category=ErrorCategory.NETWORK,
                severity=ErrorSeverity.MEDIUM,
                message=f"Test error {i}",
                original_error=Exception("test"),
                context={},
                timestamp=datetime.now()
            )
            self.error_handler.handle_error(error_info)

        summary = self.error_handler.get_error_summary()

        assert summary["total_errors"] == 3
        assert summary["error_by_category"][ErrorCategory.NETWORK] == 3


class TestRetryStrategy:
    """测试重试策略"""

    def test_retry_delay_calculation(self):
        """测试重试延迟计算"""
        strategy = RetryStrategy(
            max_attempts=3,
            base_delay=1.0,
            max_delay=10.0,
            exponential_base=2.0,
            jitter=False
        )

        # 测试指数退避
        assert strategy.get_delay(0) == 1.0
        assert strategy.get_delay(1) == 2.0
        assert strategy.get_delay(2) == 4.0

        # 测试最大延迟限制
        large_base = RetryStrategy(base_delay=100, max_delay=10, jitter=False)
        assert large_base.get_delay(0) == 10

    def test_jitter(self):
        """测试抖动功能"""
        strategy = RetryStrategy(
            base_delay=1.0,
            jitter=True
        )

        # 多次测试，应该有随机性
        delays = [strategy.get_delay(0) for _ in range(10)]
        assert len(set(delays)) > 1  # 应该有不同的值
        assert all(0.5 <= d <= 1.0 for d in delays)  # 应该在范围内


class TestFallbackStrategy:
    """测试降级策略"""

    def test_fallback_data(self):
        """测试降级数据"""
        fallback_data = {"result": "fallback_value"}
        strategy = FallbackStrategy(
            fallback_enabled=True,
            fallback_data=fallback_data
        )

        assert strategy.fallback_enabled is True
        assert strategy.fallback_data == fallback_data

    def test_fallback_function(self):
        """测试降级函数"""
        def fallback_func():
            return "computed_fallback"

        strategy = FallbackStrategy(
            fallback_enabled=True,
            fallback_function=fallback_func
        )

        assert strategy.fallback_function == fallback_func


@pytest.mark.asyncio
class TestRobustRetry:
    """测试健壮重试装饰器"""

    def test_sync_retry_success(self):
        """测试同步重试成功"""
        call_count = 0

        @robust_retry(max_attempts=3, delay=0.1)
        def test_function():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise ConnectionError("Simulated failure")
            return "success"

        result = test_function()
        assert result == "success"
        assert call_count == 2

    async def test_async_retry_success(self):
        """测试异步重试成功"""
        call_count = 0

        @robust_retry(max_attempts=3, delay=0.1)
        async def test_async_function():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise ConnectionError("Simulated failure")
            return "async_success"

        result = await test_async_function()
        assert result == "async_success"
        assert call_count == 2

    def test_retry_with_fallback(self):
        """测试重试失败时降级"""
        @robust_retry(max_attempts=2, delay=0.1, fallback_result="fallback")
        def always_fail_function():
            raise ValueError("Always fails")

        result = always_fail_function()
        assert result == "fallback"

    async def test_async_retry_with_fallback(self):
        """测试异步重试失败时降级"""
        @robust_retry(max_attempts=2, delay=0.1, fallback_result="fallback")
        async def always_fail_async_function():
            raise ValueError("Always fails")

        result = await always_fail_async_function()
        assert result == "fallback"

    def test_specific_exception_types(self):
        """测试特定异常类型重试"""
        call_count = 0

        @robust_retry(max_attempts=3, delay=0.1, exceptions=ConnectionError)
        def test_function():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise ConnectionError("Network error")
            return "success"

        result = test_function()
        assert result == "success"
        assert call_count == 2

    def test_non_retry_exception(self):
        """测试非重试异常"""
        @robust_retry(max_attempts=3, delay=0.1, exceptions=ConnectionError)
        def test_function():
            raise ValueError("Not retryable")

        with pytest.raises(ValueError):
            test_function()


@pytest.mark.asyncio
class TestCircuitBreaker:
    """测试熔断器"""

    async def test_circuit_breaker_success(self):
        """测试熔断器成功场景"""
        @circuit_breaker(failure_threshold=3, recovery_timeout=1.0)
        async def success_function():
            return "success"

        result = await success_function()
        assert result == "success"

    async def test_circuit_breaker_open(self):
        """测试熔断器打开"""
        call_count = 0

        @circuit_breaker(failure_threshold=2, recovery_timeout=0.1)
        async def fail_function():
            nonlocal call_count
            call_count += 1
            raise ValueError("Always fails")

        # 触发熔断器
        with pytest.raises(ValueError):
            await fail_function()

        with pytest.raises(ValueError):
            await fail_function()

        # 熔断器应该打开
        call_count_after_open = call_count
        with pytest.raises(RuntimeError, match="Circuit breaker is open"):
            await fail_function()

        # 调用次数不应该增加
        assert call_count == call_count_after_open

    async def test_circuit_breaker_recovery(self):
        """测试熔断器恢复"""
        call_count = 0

        @circuit_breaker(failure_threshold=2, recovery_timeout=0.1)
        async def function():
            nonlocal call_count
            call_count += 1
            if call_count <= 2:
                raise ValueError("Fail first few times")
            return "success"

        # 触发熔断器
        with pytest.raises(ValueError):
            await function()

        with pytest.raises(ValueError):
            await function()

        # 等待恢复时间
        await asyncio.sleep(0.2)

        # 应该恢复并成功
        result = await function()
        assert result == "success"


class TestTimeoutHandler:
    """测试超时处理"""

    @pytest.mark.asyncio
    async def test_async_timeout_success(self):
        """测试异步超时成功"""
        @timeout_handler(timeout_seconds=1.0)
        async def quick_function():
            await asyncio.sleep(0.1)
            return "success"

        result = await quick_function()
        assert result == "success"

    @pytest.mark.asyncio
    async def test_async_timeout_failure(self):
        """测试异步超时失败"""
        @timeout_handler(timeout_seconds=0.1)
        async def slow_function():
            await asyncio.sleep(0.5)
            return "should not reach"

        with pytest.raises(TimeoutError):
            await slow_function()

    def test_sync_timeout_success(self):
        """测试同步超时成功"""
        @timeout_handler(timeout_seconds=1.0)
        def quick_function():
            time.sleep(0.1)
            return "success"

        result = quick_function()
        assert result == "success"


class TestSafeExecute:
    """测试��全执行"""

    def test_safe_execute_success(self):
        """测试安全执行成功"""
        def success_function():
            return "success"

        result = safe_execute(success_function)
        assert result == "success"

    def test_safe_execute_with_fallback(self):
        """测试安全执行失败降级"""
        def fail_function():
            raise ValueError("Always fails")

        result = safe_execute(fail_function, fallback_result="fallback")
        assert result == "fallback"

    def test_safe_execute_without_fallback(self):
        """测试安全执行失败无降级"""
        def fail_function():
            raise ValueError("Always fails")

        with pytest.raises(ValueError):
            safe_execute(fail_function)

    @pytest.mark.asyncio
    async def test_safe_execute_async_success(self):
        """测试异步安全执行成功"""
        async def success_async_function():
            return "async_success"

        result = await safe_execute_async(success_async_function)
        assert result == "async_success"

    @pytest.mark.asyncio
    async def test_safe_execute_async_with_fallback(self):
        """测试异步安全执行失败降级"""
        async def fail_async_function():
            raise ValueError("Always fails")

        result = await safe_execute_async(
            fail_async_function,
            fallback_result="async_fallback"
        )
        assert result == "async_fallback"


class TestGlobalErrorHandler:
    """测试全局错误处理器"""

    def test_global_error_handler(self):
        """测试全局错误处理器"""
        # 确保全局错误处理器可用
        assert global_error_handler is not None
        assert isinstance(global_error_handler, ErrorHandler)

        # 测试错误分类
        error = ConnectionError("Test error")
        error_info = global_error_handler.classify_error(error)

        assert error_info.category == ErrorCategory.NETWORK
        assert error_info.severity == ErrorSeverity.MEDIUM


if __name__ == "__main__":
    pytest.main([__file__])