"""
版本控制测试 - pytest 配置和 fixtures

提供测试所需的共享fixtures
"""

import pytest
import fakeredis
from datetime import datetime

from app.services.agent.version_control import (
    VersionControlService,
    Patch,
    PatchOperation,
    Version,
    VersionedContent
)


@pytest.fixture
def redis_client():
    """Redis客户端fixture (使用fakeredis模拟)"""
    return fakeredis.FakeStrictRedis(decode_responses=False)


@pytest.fixture
def vc_service(redis_client):
    """VersionControlService fixture"""
    return VersionControlService(redis_client)


@pytest.fixture
def sample_content():
    """示例内容"""
    return "第一章 开端\n\n李明站在城墙上，眺望远方。"


@pytest.fixture
def sample_patch():
    """示例补丁"""
    return Patch(
        patch_id="patch_001",
        operation=PatchOperation.INSERT,
        position=0,
        content="序言：\n\n",
        created_at=datetime.now(),
        created_by="user_test",
        description="添加序言"
    )


@pytest.fixture
def versioned_content(vc_service, sample_content):
    """创建一个版本化内容用于测试"""
    return vc_service.create_content(
        content_id="test_content_001",
        initial_content=sample_content,
        created_by="user_test"
    )
