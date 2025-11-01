"""
日志系统测试

测试结构化日志记录器、性能监控装饰器等功能
"""

import pytest
import asyncio
import time
import json
from unittest.mock import Mock, patch
from datetime import datetime
import logging

from app.services.agent.utils import (
    AgentLogger,
    get_logger,
    setup_logging,
    log_performance,
    log_operation_context,
    default_logger
)


class TestAgentLogger:
    """测试Agent日志记录器"""

    def setup_method(self):
        """测试前准备"""
        self.logger = AgentLogger("test_logger", structured=True)

    def test_logger_creation(self):
        """测试日志记录器创建"""
        assert self.logger.name == "test_logger"
        assert self.logger.structured is True
        assert self.logger.enable_performance is True

    def test_logger_without_structlog(self):
        """测试无structlog时的日志记录器"""
        logger = AgentLogger("test_logger", structured=False)
        assert logger.structured is False
        assert logger.struct_logger is None

    def test_format_structured_log(self):
        """测试结构化日志格式化"""
        message = "Test message"
        kwargs = {"user_id": "test_user", "action": "test_action"}

        log_entry = self.logger._format_structured_log("INFO", message, **kwargs)

        assert log_entry["level"] == "INFO"
        assert log_entry["logger"] == "test_logger"
        assert log_entry["message"] == message
        assert log_entry["user_id"] == "test_user"
        assert log_entry["action"] == "test_action"
        assert "timestamp" in log_entry

    def test_info_logging(self):
        """测试信息日志记录"""
        with patch.object(self.logger, 'struct_logger') as mock_struct_logger:
            self.logger.info("Test info", user_id="test_user")
            mock_struct_logger.info.assert_called_once()

    def test_warning_logging(self):
        """测试警告日志记录"""
        with patch.object(self.logger, 'struct_logger') as mock_struct_logger:
            self.logger.warning("Test warning", action="test_action")
            mock_struct_logger.warning.assert_called_once()

    def test_error_logging(self):
        """测试错误日志记录"""
        with patch.object(self.logger, 'struct_logger') as mock_struct_logger:
            self.logger.error("Test error", error_code=500)
            mock_struct_logger.error.assert_called_once()

    def test_error_logging_with_exception(self):
        """测试带异常的错误日志记录"""
        exception = ValueError("Test exception")

        with patch.object(self.logger, 'struct_logger') as mock_struct_logger:
            self.logger.error("Test error", exception=exception)
            mock_struct_logger.error.assert_called_once()

    def test_debug_logging(self):
        """测试调试日志记录"""
        with patch.object(self.logger, 'struct_logger') as mock_struct_logger:
            self.logger.debug("Test debug", debug_info="test")
            mock_struct_logger.debug.assert_called_once()

    def test_critical_logging(self):
        """测试严重错误日志记录"""
        with patch.object(self.logger, 'struct_logger') as mock_struct_logger:
            self.logger.critical("Test critical", system_failure=True)
            mock_struct_logger.critical.assert_called_once()

    def test_log_action_start(self):
        """测试Action开始日志"""
        with patch.object(self.logger, 'info') as mock_info:
            self.logger.log_action_start(
                "writing",
                user_id="test_user",
                conversation_id="test_conv"
            )

            mock_info.assert_called_once()
            call_args = mock_info.call_args
            assert "Action started: writing" in call_args[0][0]
            assert call_args[1]["action_name"] == "writing"
            assert call_args[1]["user_id"] == "test_user"
            assert call_args[1]["event_type"] == "action_started"

    def test_log_action_complete(self):
        """测试Action完成日志"""
        with patch.object(self.logger, 'info') as mock_info:
            self.logger.log_action_complete(
                "writing",
                duration=2.5,
                success=True,
                user_id="test_user"
            )

            mock_info.assert_called_once()
            call_args = mock_info.call_args
            assert "Action completed: writing" in call_args[0][0]
            assert call_args[1]["duration"] == 2.5
            assert call_args[1]["success"] is True
            assert call_args[1]["event_type"] == "action_completed"

    def test_log_action_error(self):
        """测试Action错误日志"""
        error = ValueError("Test error")

        with patch.object(self.logger, 'error') as mock_error:
            self.logger.log_action_error(
                "writing",
                error,
                user_id="test_user"
            )

            mock_error.assert_called_once()
            call_args = mock_error.call_args
            assert "Action failed: writing" in call_args[0][0]
            assert call_args[1]["action_name"] == "writing"
            assert call_args[1]["error_type"] == "ValueError"
            assert call_args[1]["error_message"] == "Test error"
            assert call_args[1]["exception"] == error

    def test_log_tool_call(self):
        """测试工具调用日志"""
        parameters = {"input": "test"}
        result = "output"

        with patch.object(self.logger, 'info') as mock_info:
            self.logger.log_tool_call(
                "test_tool",
                parameters,
                result,
                1.5,
                success=True
            )

            mock_info.assert_called_once()
            call_args = mock_info.call_args
            assert "Tool call: test_tool" in call_args[0][0]
            assert call_args[1]["tool_name"] == "test_tool"
            assert call_args[1]["parameters"] == parameters
            assert call_args[1]["duration"] == 1.5
            assert call_args[1]["success"] is True

    def test_log_llm_call(self):
        """测试LLM调用日志"""
        tokens_used = {"input": 100, "output": 200}

        with patch.object(self.logger, 'info') as mock_info:
            self.logger.log_llm_call(
                "gemini-2.5-flash",
                tokens_used,
                0.05,
                3.2,
                success=True
            )

            mock_info.assert_called_once()
            call_args = mock_info.call_args
            assert "LLM call: gemini-2.5-flash" in call_args[0][0]
            assert call_args[1]["model"] == "gemini-2.5-flash"
            assert call_args[1]["tokens_used"] == tokens_used
            assert call_args[1]["cost"] == 0.05
            assert call_args[1]["duration"] == 3.2

    def test_log_memory_operation(self):
        """测试Memory操作日志"""
        with patch.object(self.logger, 'info') as mock_info:
            self.logger.log_memory_operation(
                "add",
                "test_user",
                memory_count=10
            )

            mock_info.assert_called_once()
            call_args = mock_info.call_args
            assert "Memory operation: add" in call_args[0][0]
            assert call_args[1]["operation"] == "add"
            assert call_args[1]["user_id"] == "test_user"
            assert call_args[1]["memory_count"] == 10

    def test_log_quality_evaluation(self):
        """测试质量评估日志"""
        dimension_scores = {"content": 8.5, "coherence": 7.5}

        with patch.object(self.logger, 'info') as mock_info:
            self.logger.log_quality_evaluation(
                "content_1",
                8.0,
                dimension_scores,
                True
            )

            mock_info.assert_called_once()
            call_args = mock_info.call_args
            assert "Quality evaluation: 8.00" in call_args[0][0]
            assert call_args[1]["content_id"] == "content_1"
            assert call_args[1]["overall_score"] == 8.0
            assert call_args[1]["passes"] is True


@pytest.mark.asyncio
class TestPerformanceDecorators:
    """测试性能监控装饰器"""

    def test_log_performance_sync_success(self):
        """测试同步性能监控装饰器成功"""
        logger = AgentLogger("test_perf")

        @log_performance(logger, "test_operation")
        def test_function():
            time.sleep(0.1)
            return "success"

        with patch.object(logger, 'info') as mock_info:
            result = test_function()

            assert result == "success"
            assert mock_info.call_count == 2  # start + complete

            # 检查开始日志
            start_call = mock_info.call_args_list[0]
            assert "Operation started: test_operation" in start_call[0][0]
            assert start_call[1]["event_type"] == "operation_started"

            # 检查完成日志
            complete_call = mock_info.call_args_list[1]
            assert "Operation completed: test_operation" in complete_call[0][0]
            assert complete_call[1]["success"] is True
            assert complete_call[1]["duration"] >= 0.1

    async def test_log_performance_async_success(self):
        """测试异步性能监控装饰器成功"""
        logger = AgentLogger("test_perf")

        @log_performance(logger, "test_async_operation")
        async def test_async_function():
            await asyncio.sleep(0.1)
            return "async_success"

        with patch.object(logger, 'info') as mock_info:
            result = await test_async_function()

            assert result == "async_success"
            assert mock_info.call_count == 2  # start + complete

    def test_log_performance_sync_failure(self):
        """测试同步性能监控装饰器失败"""
        logger = AgentLogger("test_perf")

        @log_performance(logger, "test_operation")
        def test_function():
            time.sleep(0.1)
            raise ValueError("Test error")

        with patch.object(logger, 'info') as mock_info, \
             patch.object(logger, 'error') as mock_error:

            with pytest.raises(ValueError):
                test_function()

            assert mock_info.call_count == 1  # start
            assert mock_error.call_count == 1  # failed

            # 检查失败日志
            error_call = mock_error.call_args
            assert "Operation failed: test_operation" in error_call[0][0]
            assert error_call[1]["success"] is False
            assert error_call[1]["error_type"] == "ValueError"

    async def test_log_performance_async_failure(self):
        """测试异步性能监控装饰器失败"""
        logger = AgentLogger("test_perf")

        @log_performance(logger, "test_async_operation")
        async def test_async_function():
            await asyncio.sleep(0.1)
            raise ValueError("Test async error")

        with patch.object(logger, 'info') as mock_info, \
             patch.object(logger, 'error') as mock_error:

            with pytest.raises(ValueError):
                await test_async_function()

            assert mock_info.call_count == 1  # start
            assert mock_error.call_count == 1  # failed

    async def test_log_operation_context_success(self):
        """测试操作上下文管理器成功"""
        logger = AgentLogger("test_context")

        with patch.object(logger, 'info') as mock_info:
            async with log_operation_context(
                logger,
                "context_operation",
                user_id="test_user"
            ) as operation_id:
                await asyncio.sleep(0.1)
                assert operation_id is not None

            assert mock_info.call_count == 2  # start + complete

            # 检查开始日志
            start_call = mock_info.call_args_list[0]
            assert "Operation started: context_operation" in start_call[0][0]
            assert start_call[1]["user_id"] == "test_user"

            # 检查完成日志
            complete_call = mock_info.call_args_list[1]
            assert "Operation completed: context_operation" in complete_call[0][0]
            assert complete_call[1]["success"] is True

    async def test_log_operation_context_failure(self):
        """测试操作上下文管理器失败"""
        logger = AgentLogger("test_context")

        with patch.object(logger, 'info') as mock_info, \
             patch.object(logger, 'error') as mock_error:

            with pytest.raises(ValueError):
                async with log_operation_context(
                    logger,
                    "context_operation",
                    user_id="test_user"
                ):
                    await asyncio.sleep(0.1)
                    raise ValueError("Test context error")

            assert mock_info.call_count == 1  # start
            assert mock_error.call_count == 1  # failed

            # 检查失败日志
            error_call = mock_error.call_args
            assert "Operation failed: context_operation" in error_call[0][0]
            assert error_call[1]["success"] is False


class TestLoggerUtilities:
    """测试日志工具��数"""

    def test_get_logger(self):
        """测试获取日志记录器"""
        logger = get_logger("custom_logger", level="DEBUG")

        assert isinstance(logger, AgentLogger)
        assert logger.name == "custom_logger"
        assert logger.level == logging.DEBUG

    def test_setup_logging(self):
        """测试设置日志配置"""
        # 这个测试主要验证函数调用不抛出异常
        try:
            setup_logging(level="INFO", structured=True)
            setup_logging(level="DEBUG", structured=False, format_string="%(message)s")
        except Exception as e:
            pytest.fail(f"setup_logging raised {e}")

    def test_default_logger(self):
        """测试默认日志记录器"""
        assert default_logger is not None
        assert isinstance(default_logger, AgentLogger)
        assert default_logger.name == "agent"


class TestNonStructuredLogging:
    """测试非结构化日志记录"""

    def test_non_structured_logging(self):
        """测试非结构化日志记录"""
        logger = AgentLogger("test_non_structured", structured=False)

        with patch.object(logger.logger, 'info') as mock_info:
            logger.info("Test message", user_id="test")

            mock_info.assert_called_once_with("Test message")

    def test_non_structured_error_logging(self):
        """测试非结构化错误日志记录"""
        logger = AgentLogger("test_non_structured", structured=False)

        with patch.object(logger.logger, 'error') as mock_error:
            logger.error("Test error", error_type="ValueError")

            mock_error.assert_called_once()
            # 检查是否包含JSON格式的日志
            call_args = mock_error.call_args[0][0]
            assert "Test error" in call_args
            # 应该包含JSON结构
            assert isinstance(call_args, str)


if __name__ == "__main__":
    pytest.main([__file__])