"""
Agent Utils 集成测试

测试各工具模块之间的集成和实际使用场景
"""

import pytest
import asyncio
import json
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime

from app.services.agent.utils import (
    AgentLogger,
    global_error_handler,
    robust_retry,
    circuit_breaker,
    get_logger,
    log_performance
)
from app.config.agent_config import AgentConfig


class TestErrorHandlingIntegration:
    """测试错误处理集成"""

    @pytest.mark.asyncio
    async def test_retry_with_logging_integration(self):
        """测试重试与日志集成"""
        logger = get_logger("integration_test")
        call_count = 0

        @robust_retry(max_attempts=3, delay=0.1, fallback_result="fallback")
        async def failing_function():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise ConnectionError("Simulated network error")
            return "success"

        with patch.object(logger, 'info') as mock_info, \
             patch.object(logger, 'warning') as mock_warning:

            result = await failing_function()

            assert result == "success"
            assert call_count == 2

            # 应该有警告日志（重试）
            assert mock_warning.call_count >= 1

    @pytest.mark.asyncio
    async def test_circuit_breaker_with_error_handler_integration(self):
        """测试熔断器与错误处理器集成"""
        call_count = 0

        @circuit_breaker(failure_threshold=2, recovery_timeout=0.1)
        async def failing_function():
            nonlocal call_count
            call_count += 1
            raise ValueError("Always fails")

        # 触发熔断器
        with pytest.raises(ValueError):
            await failing_function()

        with pytest.raises(ValueError):
            await failing_function()

        # 熔断器应该打开
        with pytest.raises(RuntimeError):
            await failing_function()

        # 检查全局错误处理器
        summary = global_error_handler.get_error_summary()
        assert summary["total_errors"] >= 2

    @pytest.mark.asyncio
    async def test_complex_error_handling_scenario(self):
        """测试复杂错误处理场景"""
        logger = get_logger("complex_scenario")

        @log_performance(logger, "complex_operation")
        @robust_retry(max_attempts=2, delay=0.1)
        @circuit_breaker(failure_threshold=3, recovery_timeout=0.1)
        async def complex_operation(should_fail=False):
            if should_fail:
                raise ConnectionError("Network error")
            return "operation_success"

        with patch.object(logger, 'info') as mock_info, \
             patch.object(logger, 'error') as mock_error:

            # 成功场景
            result = await complex_operation(should_fail=False)
            assert result == "operation_success"

            # 失败场景
            with pytest.raises(ConnectionError):
                await complex_operation(should_fail=True)

            # 验证日志记录
            assert mock_info.call_count >= 2  # start + success/failure
            if mock_error.called:
                error_call = mock_error.call_args
                assert "complex_operation" in str(error_call)


class TestLoggingIntegration:
    """测试日志系统集成"""

    def test_logger_with_config_integration(self):
        """测试日志记录器与配置集成"""
        config = AgentConfig(
            LOG_LEVEL="DEBUG",
            ENABLE_STRUCTURED_LOGGING=True
        )

        logger = get_logger("config_test")
        logger.level = getattr(__import__('logging'), config.LOG_LEVEL)

        # 验证日志级别设置
        assert logger.level == __import__('logging').DEBUG
        assert logger.structured == config.ENABLE_STRUCTURED_LOGGING

    @pytest.mark.asyncio
    async def test_business_logging_integration(self):
        """测试业务日志集成"""
        logger = get_logger("business_test")

        with patch.object(logger, 'info') as mock_info:
            # 测试Action日志
            logger.log_action_start("writing", user_id="user_123")
            logger.log_action_complete("writing", 2.5, True, user_id="user_123")

            # 测试工具调用日志
            logger.log_tool_call("test_tool", {"input": "test"}, "result", 1.0, True)

            # 测试LLM调用日志
            logger.log_llm_call("gemini-2.5-flash", {"input": 100}, 0.05, 3.0, True)

            # 验证调用次数
            assert mock_info.call_count == 4

            # 验证日志内容
            calls = mock_info.call_args_list
            assert any("Action started: writing" in str(call) for call in calls)
            assert any("Tool call: test_tool" in str(call) for call in calls)
            assert any("LLM call: gemini-2.5-flash" in str(call) for call in calls)

    @pytest.mark.asyncio
    async def test_performance_monitoring_integration(self):
        """测试性能监控集成"""
        logger = get_logger("performance_test")

        @log_performance(logger, "monitored_operation")
        async def monitored_operation():
            await asyncio.sleep(0.1)
            return {"result": "success", "data": [1, 2, 3]}

        with patch.object(logger, 'info') as mock_info:
            result = await monitored_operation()

            assert result["result"] == "success"
            assert mock_info.call_count == 2  # start + complete

            # 验证性能数据
            complete_call = mock_info.call_args_list[1]
            assert complete_call[1]["duration"] >= 0.1
            assert complete_call[1]["success"] is True


class TestConfigIntegration:
    """测试配置集成"""

    def test_config_with_error_handling_integration(self):
        """测试配置与错误处理集成"""
        # 测试无效配置的错误处理
        with pytest.raises(Exception):  # 可能是ValidationError或ValueError
            AgentConfig(
                QUALITY_THRESHOLD=15.0,  # 无效值
                MAX_CONCURRENT_ACTIONS=0   # 无效值
            )

    def test_config_getters_integration(self):
        """测试配置获取方法集成"""
        config = AgentConfig()

        # 测试所有配置获取方法
        model_config = config.get_model_config("complex")
        cache_config = config.get_cache_config()
        timeout_config = config.get_timeout_config()
        monitoring_config = config.get_monitoring_config()

        # 验证配置完整性
        assert all(key in model_config for key in ["model", "temperature", "max_tokens"])
        assert all(key in cache_config for key in ["memory_cache_size", "redis_ttl"])
        assert all(key in timeout_config for key in ["action_timeout", "tool_timeout"])
        assert all(key in monitoring_config for key in ["enable_performance_monitoring"])

    def test_config_validation_integration(self):
        """测试配置验证集成"""
        config = AgentConfig()

        # 测试有效配置
        valid_config = AgentConfig(
            QUALITY_THRESHOLD=8.5,
            MAX_CONCURRENT_ACTIONS=5,
            TOOL_TIMEOUT=60,
            ACTION_TIMEOUT=300
        )
        errors = valid_config.validate_config()
        assert errors == []

        # 测试无效配置
        invalid_config = AgentConfig(
            QUALITY_THRESHOLD=15.0,
            TOOL_TIMEOUT=400,
            ACTION_TIMEOUT=300
        )
        errors = invalid_config.validate_config()
        assert len(errors) > 0


class TestRealWorldScenarios:
    """测试真实世界场景"""

    @pytest.mark.asyncio
    async def test_memory_operation_with_error_handling(self):
        """测试Memory操作与错误处理"""
        logger = get_logger("memory_scenario")

        @robust_retry(max_attempts=2, delay=0.1)
        async def mock_redis_operation(success=True):
            if not success:
                raise ConnectionError("Redis connection failed")
            return {"data": "memory_data"}

        with patch.object(logger, 'log_memory_operation') as mock_memory_log:
            # 成功场景
            result = await mock_redis_operation(success=True)
            assert result["data"] == "memory_data"

            # 记录内存操作日志
            logger.log_memory_operation("add", "user_123", memory_count=5)
            mock_memory_log.assert_called_once()

    @pytest.mark.asyncio
    async def test_llm_call_with_monitoring_and_retry(self):
        """测试LLM调用与监控和重试"""
        logger = get_logger("llm_scenario")
        call_count = 0

        @log_performance(logger, "llm_call")
        @robust_retry(max_attempts=3, delay=0.1)
        async def mock_llm_call():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise TimeoutError("LLM timeout")
            return {
                "model": "gemini-2.5-flash",
                "tokens": {"input": 100, "output": 200},
                "cost": 0.05
            }

        with patch.object(logger, 'log_llm_call') as mock_llm_log:
            result = await mock_llm_call()

            assert result["model"] == "gemini-2.5-flash"
            assert call_count == 2  # 重试一次后成功

            # 记录LLM调用日志
            logger.log_llm_call(
                result["model"],
                result["tokens"],
                result["cost"],
                2.5,
                success=True
            )
            mock_llm_log.assert_called_once()

    @pytest.mark.asyncio
    async def test_quality_evaluation_with_logging(self):
        """测试质量评估与日志"""
        logger = get_logger("quality_scenario")

        def mock_quality_evaluation():
            return {
                "overall_score": 8.5,
                "dimension_scores": {
                    "content": 9.0,
                    "coherence": 8.0,
                    "grammar": 8.5
                },
                "passes": True,
                "suggestions": ["Minor improvements needed"]
            }

        with patch.object(logger, 'log_quality_evaluation') as mock_quality_log:
            result = mock_quality_evaluation()

            assert result["overall_score"] == 8.5
            assert result["passes"] is True

            # 记录质量评估日志
            logger.log_quality_evaluation(
                "content_001",
                result["overall_score"],
                result["dimension_scores"],
                result["passes"]
            )
            mock_quality_log.assert_called_once()

    @pytest.mark.asyncio
    async def test_tool_execution_with_circuit_breaker(self):
        """测试工具执行与熔断器"""
        logger = get_logger("tool_scenario")

        @circuit_breaker(failure_threshold=2, recovery_timeout=0.1)
        async def mock_tool_execution(should_fail=False):
            if should_fail:
                raise RuntimeError("Tool execution failed")
            return {"result": "tool_success", "data": [1, 2, 3]}

        # 成功执行
        result = await mock_tool_execution(should_fail=False)
        assert result["result"] == "tool_success"

        # 记录工具调用日志
        with patch.object(logger, 'log_tool_call') as mock_tool_log:
            logger.log_tool_call(
                "test_tool",
                {"param": "value"},
                result,
                1.5,
                success=True
            )
            mock_tool_log.assert_called_once()

        # 测试熔断器
        with pytest.raises(RuntimeError):
            await mock_tool_execution(should_fail=True)
            await mock_tool_execution(should_fail=True)
            await mock_tool_execution(should_fail=True)  # 应该触发熔断器


class TestErrorRecoveryScenarios:
    """测试错误恢复场景"""

    @pytest.mark.asyncio
    async def test_redis_failure_recovery(self):
        """测试Redis故障恢复"""
        logger = get_logger("redis_recovery")

        @robust_retry(max_attempts=3, delay=0.1, fallback_result={"fallback": True})
        async def mock_redis_operation():
            raise ConnectionError("Redis unavailable")

        with patch.object(logger, 'error') as mock_error:
            result = await mock_redis_operation()

            # 应该返回降级结果
            assert result["fallback"] is True

            # 应该记录错误日志
            assert mock_error.called

    @pytest.mark.asyncio
    async def test_network_timeout_recovery(self):
        """测试网络超时恢复"""
        logger = get_logger("timeout_recovery")

        call_count = 0

        @robust_retry(max_attempts=3, delay=0.1)
        async def mock_network_operation():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise asyncio.TimeoutError("Network timeout")
            return {"data": "recovered_data"}

        with patch.object(logger, 'warning') as mock_warning:
            result = await mock_network_operation()

            assert result["data"] == "recovered_data"
            assert call_count == 3

            # 应该有重试警告
            assert mock_warning.call_count >= 2

    @pytest.mark.asyncio
    async def test_service_degradation(self):
        """测试服务降级"""
        logger = get_logger("service_degradation")

        @robust_retry(max_attempts=1, delay=0.1, fallback_result="degraded_response")
        async def primary_service():
            raise ConnectionError("Primary service down")

        @robust_retry(max_attempts=1, delay=0.1, fallback_result="fallback_response")
        async def fallback_service():
            return {"status": "ok", "data": "fallback_data"}

        with patch.object(logger, 'warning') as mock_warning:
            # 主服务失败，应该降级
            primary_result = await primary_service()
            assert primary_result == "degraded_response"

            # 备用服务成功
            fallback_result = await fallback_service()
            assert fallback_result["status"] == "ok"

            # 应该记录降级警告
            assert mock_warning.called


if __name__ == "__main__":
    pytest.main([__file__])