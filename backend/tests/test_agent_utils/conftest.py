"""
Agent Utils 测试配置

提供测试夹具和通用设置
"""

import pytest
import asyncio
import logging
from unittest.mock import Mock, AsyncMock


@pytest.fixture
def mock_redis_client():
    """模拟Redis客户端"""
    redis_mock = Mock()
    redis_mock.get = Mock(return_value=None)
    redis_mock.set = Mock(return_value=True)
    redis_mock.delete = Mock(return_value=True)
    redis_mock.ping = Mock(return_value=True)
    return redis_mock


@pytest.fixture
def mock_ai_service():
    """模拟AI服务"""
    ai_service_mock = AsyncMock()
    ai_service_mock.call_ai = AsyncMock(return_value="Mock response")
    ai_service_mock.stream_chat = AsyncMock()
    return ai_service_mock


@pytest.fixture
def sample_memory_item():
    """示例记忆条目"""
    from app.services.agent.memory.types import MemoryItem
    from datetime import datetime, timezone

    return MemoryItem(
        id="test_memory_001",
        user_id="test_user",
        conversation_id="test_conv",
        role="user",
        content="Test content",
        timestamp=datetime.now(timezone.utc),
        last_access=datetime.now(timezone.utc),
        importance=0.8,
        metadata={"test": True}
    )


@pytest.fixture
def sample_agent_state():
    """示例Agent状态"""
    return {
        "conversation_id": "test_conv_001",
        "user_id": "test_user_001",
        "messages": [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"}
        ],
        "work_id": "work_001",
        "intent": "writing",
        "context": {"chapter": 1},
        "final_response": None
    }


@pytest.fixture
def setup_logging():
    """设置测试日志"""
    # 设置测试日志级别
    logging.basicConfig(level=logging.DEBUG)

    # 禁用第三方库的日志
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)

    yield

    # 测试后清理
    logging.getLogger().handlers.clear()


@pytest.fixture(scope="session")
def event_loop():
    """为测试提供事件循环"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def temp_config_file(tmp_path):
    """临时配置文件"""
    config_file = tmp_path / "test_config.yaml"
    config_file.write_text("""
DEFAULT_MODEL: "test-model"
MAX_CONCURRENT_ACTIONS: 3
QUALITY_THRESHOLD: 7.5
""")
    return config_file


class MockError(Exception):
    """模拟错误"""
    pass


class MockTimeoutError(TimeoutError):
    """模拟超时错误"""
    pass


@pytest.fixture
def mock_network_error():
    """模拟网络错误"""
    import requests
    return requests.ConnectionError("Network error")


@pytest.fixture
def mock_timeout_error():
    """模拟超时错误"""
    return asyncio.TimeoutError("Operation timeout")


# 测试数据
SAMPLE_CONFIG_VALUES = {
    "model": "gemini-2.5-flash",
    "temperature": 0.7,
    "max_tokens": 2000,
    "user_id": "test_user_123",
    "conversation_id": "test_conv_456",
    "action_name": "test_action",
    "tool_name": "test_tool",
    "error_message": "Test error message"
}


@pytest.fixture
def sample_config_values():
    """示例配置值"""
    return SAMPLE_CONFIG_VALUES.copy()