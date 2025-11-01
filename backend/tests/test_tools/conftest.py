"""
测试工具系统的pytest配置和共享fixtures
"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from typing import AsyncIterator


@pytest.fixture
def mock_ai_service():
    """Mock AI Service用于测试"""
    service = MagicMock()

    async def mock_stream_chat(*args, **kwargs):
        """模拟流式聊天响应"""
        # 返回一个简单的测试文本
        yield "这是一个测试生成的文本内容。"
        yield "它包含了多个句子。"
        yield "用于验证工具的功能。"

    service._stream_chat = mock_stream_chat
    return service


@pytest.fixture
def mock_redis_client():
    """Mock Redis客户端用于测试"""
    client = MagicMock()

    # Mock基本的Redis操作
    client.lpush = MagicMock(return_value=1)
    client.lrange = MagicMock(return_value=[])
    client.expire = MagicMock(return_value=True)
    client.ltrim = MagicMock(return_value=True)
    client.get = MagicMock(return_value=None)
    client.set = MagicMock(return_value=True)

    return client
