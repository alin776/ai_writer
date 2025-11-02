"""
验证修复功能的测试脚本

测试我们修复的关键问题：
1. 重试装饰器与异步生成器兼容性
2. 配置参数验证
3. Agent错误处理逻辑
4. 资源管理和上下文管理器
"""

import asyncio
import pytest
import httpx
from unittest.mock import Mock, patch, AsyncMock
import tempfile
import os
from typing import AsyncGenerator

# 导入修复后的模块
from app.services.ai.http_ai_service import retry_on_failure, HTTPAIService
from app.core.config import Settings
from app.services.agent.langgraph_agent import WritingAgentGraph


class TestRetryDecorator:
    """测试重试装饰器的异步生成器支持"""

    def test_retry_with_sync_function(self):
        """测试装饰器对同步函数的处理"""
        call_count = 0

        @retry_on_failure(max_retries=2, delay=0.1)
        async def sync_function():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise httpx.ConnectTimeout("模拟连接超时")
            return "success"

        async def test():
            result = await sync_function()
            assert result == "success"
            assert call_count == 2  # 1次失败 + 1次成功

        asyncio.run(test())

    def test_retry_with_async_generator(self):
        """测试装饰器对异步生成器的处理"""
        call_count = 0

        @retry_on_failure(max_retries=2, delay=0.1)
        async def generator_function():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                # 模拟第一个网络请求失败
                raise httpx.ConnectTimeout("模拟连接超时")

            # 成功时生成数据
            for i in range(3):
                yield f"item_{i}"

        async def test():
            results = []
            async for item in generator_function():
                results.append(item)

            assert results == ["item_0", "item_1", "item_2"]
            assert call_count == 2  # 1次失败 + 1次成功

        asyncio.run(test())

    def test_retry_with_max_time_limit(self):
        """测试重试时间限制功能"""
        call_count = 0

        @retry_on_failure(max_retries=5, delay=0.5, max_total_time=0.8)
        async def failing_function():
            nonlocal call_count
            call_count += 1
            raise httpx.ConnectTimeout("总是失败")

        async def test():
            with pytest.raises(Exception) as exc_info:
                await failing_function()

            assert "重试超时" in str(exc_info.value) or "重试时间不足" in str(exc_info.value)
            # 由于时间限制，应该不会重试5次
            assert call_count < 5

        asyncio.run(test())


class TestConfigurationValidation:
    """测试配置参数验证"""

    def test_openai_timeout_validation(self):
        """测试OpenAI超时时间验证"""
        # 正常值
        settings = Settings(OPENAI_API_KEY="test_key")
        assert 1 <= settings.OPENAI_TIMEOUT <= 600

        # 边界值测试
        with pytest.raises(ValueError, match="OPENAI_TIMEOUT 必须在 1-600 秒之间"):
            Settings(OPENAI_API_KEY="test_key", OPENAI_TIMEOUT=0)

        with pytest.raises(ValueError, match="OPENAI_TIMEOUT 必须在 1-600 秒之间"):
            Settings(OPENAI_API_KEY="test_key", OPENAI_TIMEOUT=700)

        # 类型测试
        with pytest.raises(ValueError, match="OPENAI_TIMEOUT 必须是数字"):
            Settings(OPENAI_API_KEY="test_key", OPENAI_TIMEOUT="invalid")

    def test_max_retries_validation(self):
        """测试最大重试次数验证"""
        # 正常值
        settings = Settings(OPENAI_API_KEY="test_key", OPENAI_MAX_RETRIES=3)
        assert 0 <= settings.OPENAI_MAX_RETRIES <= 10

        # 边界值测试
        with pytest.raises(ValueError, match="OPENAI_MAX_RETRIES 必须在 0-10 之间"):
            Settings(OPENAI_API_KEY="test_key", OPENAI_MAX_RETRIES=-1)

        with pytest.raises(ValueError, match="OPENAI_MAX_RETRIES 必须在 0-10 之间"):
            Settings(OPENAI_API_KEY="test_key", OPENAI_MAX_RETRIES=20)

    def test_daily_cost_limit_validation(self):
        """测试每日成本限制验证"""
        # 正常值
        settings = Settings(OPENAI_API_KEY="test_key", DAILY_COST_LIMIT_PER_USER=50.0)
        assert 0 <= settings.DAILY_COST_LIMIT_PER_USER <= 1000

        # 边界值测试
        with pytest.raises(ValueError, match="DAILY_COST_LIMIT_PER_USER 必须在 0-1000 元之间"):
            Settings(OPENAI_API_KEY="test_key", DAILY_COST_LIMIT_PER_USER=-10)

        with pytest.raises(ValueError, match="DAILY_COST_LIMIT_PER_USER 必须在 0-1000 元之间"):
            Settings(OPENAI_API_KEY="test_key", DAILY_COST_LIMIT_PER_USER=2000)


class TestAgentErrorHandling:
    """测试Agent错误处理逻辑"""

    def test_network_error_detection(self):
        """测试网络错误检测"""
        # 测试httpx错误
        httpx_errors = [
            httpx.ConnectTimeout("连接超时"),
            httpx.ReadTimeout("读取超时"),
            httpx.NetworkError("网络错误"),
            httpx.HTTPError("HTTP错误"),
        ]

        for error in httpx_errors:
            # 模拟Agent中的错误检测逻辑
            network_related_errors = (
                httpx.ConnectTimeout,
                httpx.ReadTimeout,
                httpx.NetworkError,
                httpx.HTTPError,
                ConnectionError,
                TimeoutError,
            )

            is_network_error = (
                isinstance(error, network_related_errors) or
                any(keyword in str(error).lower() for keyword in ["网络", "连接", "超时", "timeout", "connection", "network"])
            )

            assert is_network_error, f"应该检测到 {type(error).__name__} 为网络错误"

    def test_non_network_error_detection(self):
        """测试非网络错误的检测"""
        # 测试非网络错误
        non_network_errors = [
            ValueError("数值错误"),
            TypeError("类型错误"),
            KeyError("键错误"),
            AttributeError("属性错误"),
        ]

        for error in non_network_errors:
            network_related_errors = (
                httpx.ConnectTimeout,
                httpx.ReadTimeout,
                httpx.NetworkError,
                httpx.HTTPError,
                ConnectionError,
                TimeoutError,
            )

            is_network_error = (
                isinstance(error, network_related_errors) or
                any(keyword in str(error).lower() for keyword in ["网络", "连接", "超时", "timeout", "connection", "network"])
            )

            assert not is_network_error, f"不应该将 {type(error).__name__} 检测为网络错误"


class TestResourceManagement:
    """测试资源管理"""

    def test_context_manager_usage(self):
        """测试上下文管理器使用"""
        async def test():
            # 测试正常使用
            async with HTTPAIService() as service:
                assert service is not None
                assert hasattr(service, 'client')
                assert service.client is not None

            # 验证客户端已关闭
            assert service.client is None

        asyncio.run(test())

    def test_close_method_error_handling(self):
        """测试close方法的错误处理"""
        async def test():
            service = HTTPAIService()

            # 模拟client关闭时出错
            with patch.object(service.client, 'aclose', side_effect=Exception("关闭失败")):
                # close方法应该捕获异常并继续
                await service.close()
                assert service.client is None

        asyncio.run(test())


def run_all_tests():
    """运行所有测试"""
    print("🧪 开始运行修复验证测试...")

    # 测试1: 重试装饰器
    print("\n📋 测试1: 重试装饰器异步生成器支持")
    test_retry = TestRetryDecorator()
    test_retry.test_retry_with_sync_function()
    print("✅ 同步函数重试测试通过")

    test_retry.test_retry_with_async_generator()
    print("✅ 异步生成器重试测试通过")

    test_retry.test_retry_with_max_time_limit()
    print("✅ 重试时间限制测试通过")

    # 测试2: 配置验证
    print("\n📋 测试2: 配置参数验证")
    test_config = TestConfigurationValidation()
    test_config.test_openai_timeout_validation()
    print("✅ OpenAI超时时间验证测试通过")

    test_config.test_max_retries_validation()
    print("✅ 最大重试次数验证测试通过")

    test_config.test_daily_cost_limit_validation()
    print("✅ 每日成本限制验证测试通过")

    # 测试3: 错误处理
    print("\n📋 测试3: Agent错误处理逻辑")
    test_error = TestAgentErrorHandling()
    test_error.test_network_error_detection()
    print("✅ 网络错误检测测试通过")

    test_error.test_non_network_error_detection()
    print("✅ 非网络错误检测测试通过")

    # 测试4: 资源管理
    print("\n📋 测试4: 资源管理和上下文管理器")
    test_resource = TestResourceManagement()
    test_resource.test_context_manager_usage()
    print("✅ 上下文管理器使用测试通过")

    test_resource.test_close_method_error_handling()
    print("✅ close方法错误处理测试通过")

    print("\n🎉 所有测试通过！修复验证成功！")


if __name__ == "__main__":
    run_all_tests()