"""
Pytest 配置文件

设置测试环境变量，避免加载完整应用配置时报错。
"""

import os

# 在导入任何 app 模块之前设置环境变量
os.environ.setdefault("SECRET_KEY", "test-secret-key-for-unit-tests")
os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://test:test@localhost/test")
os.environ.setdefault("OPENAI_API_KEY", "test-openai-api-key")
os.environ.setdefault("ADMIN_PASSWORD", "test-admin-password")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")
os.environ.setdefault("ENVIRONMENT", "test")

import pytest


@pytest.fixture(scope="session", autouse=True)
def setup_test_env():
    """确保测试环境变量已设置"""
    yield
