"""
配置管理测试

测试AgentConfig配置类、环境变量支持、配置验证等功能
"""

import pytest
import os
from unittest.mock import patch
from pathlib import Path
from pydantic import ValidationError

from app.config.agent_config import AgentConfig, get_config, reload_config, load_config_from_file


class TestAgentConfig:
    """测试Agent配置类"""

    def test_default_config(self):
        """测试默认配置"""
        config = AgentConfig()

        # 检查默认值
        assert config.DEFAULT_MODEL == "gemini-2.5-flash"
        assert config.FALLBACK_MODEL == "gemini-2.5-flash-lite"
        assert config.ENABLE_MODEL_SELECTOR is True
        assert config.ENABLE_COST_TRACKING is True

        # 性能配置
        assert config.MAX_CONCURRENT_ACTIONS == 5
        assert config.MAX_CONCURRENT_TOOLS == 3
        assert config.ACTION_TIMEOUT == 300

        # 缓存配置
        assert config.MEMORY_SHORT_TERM_SIZE == 10
        assert config.MEMORY_MEDIUM_TERM_SIZE == 100
        assert config.REDIS_TTL == 3600

        # 质量控制
        assert config.QUALITY_THRESHOLD == 8.0
        assert config.MAX_QUALITY_RETRIES == 3

    def test_config_from_env(self):
        """测试从环境变量创建配置"""
        config = AgentConfig.from_env(
            DEFAULT_MODEL="custom-model",
            MAX_CONCURRENT_ACTIONS=10,
            MEMORY_SHORT_TERM_SIZE=20
        )

        assert config.DEFAULT_MODEL == "custom-model"
        assert config.MAX_CONCURRENT_ACTIONS == 10
        assert config.MEMORY_SHORT_TERM_SIZE == 20

    def test_config_validation_success(self):
        """测试配置验证成功"""
        config = AgentConfig()
        errors = config.validate_config()

        assert errors == []  # 默认配置应该通过验证

    def test_config_validation_quality_threshold(self):
        """测试质量阈值验证"""
        config = AgentConfig(QUALITY_THRESHOLD=15.0)  # 超出范围
        errors = config.validate_config()

        assert len(errors) > 0
        assert any("QUALITY_THRESHOLD" in error for error in errors)

    def test_config_validation_memory_threshold(self):
        """测试记忆阈值验证"""
        config = AgentConfig(MEMORY_FORGET_THRESHOLD=1.5)  # 超出范围
        errors = config.validate_config()

        assert len(errors) > 0
        assert any("MEMORY_FORGET_THRESHOLD" in error for error in errors)

    def test_config_validation_timeout_logic(self):
        """测试超时配置逻辑验证"""
        config = AgentConfig(
            TOOL_TIMEOUT=400,
            ACTION_TIMEOUT=300  # TOOL_TIMEOUT >= ACTION_TIMEOUT
        )
        errors = config.validate_config()

        assert len(errors) > 0
        assert any("TOOL_TIMEOUT" in error for error in errors)

    def test_config_validation_concurrent_logic(self):
        """测试并发配置逻辑验证"""
        config = AgentConfig(
            MAX_CONCURRENT_TOOLS=10,
            MAX_CONCURRENT_ACTIONS=5  # TOOLS > ACTIONS
        )
        errors = config.validate_config()

        assert len(errors) > 0
        assert any("MAX_CONCURRENT_TOOLS" in error for error in errors)

    def test_to_dict(self):
        """测试转换为字典"""
        config = AgentConfig()
        config_dict = config.to_dict()

        assert isinstance(config_dict, dict)
        assert "DEFAULT_MODEL" in config_dict
        assert "MAX_CONCURRENT_ACTIONS" in config_dict
        assert config_dict["DEFAULT_MODEL"] == config.DEFAULT_MODEL

    def test_get_model_config_simple(self):
        """测试获取简单任务模型配置"""
        config = AgentConfig()
        model_config = config.get_model_config("simple")

        assert model_config["model"] == config.FALLBACK_MODEL
        assert model_config["temperature"] == 0.1
        assert model_config["max_tokens"] == 1000

    def test_get_model_config_medium(self):
        """测试获取中等任务模型配置"""
        config = AgentConfig()
        model_config = config.get_model_config("medium")

        assert model_config["model"] == config.DEFAULT_MODEL
        assert model_config["temperature"] == 0.7
        assert model_config["max_tokens"] == 2000

    def test_get_model_config_complex(self):
        """测试获取复杂任务模型配置"""
        config = AgentConfig()
        model_config = config.get_model_config("complex")

        assert model_config["model"] == "gemini-2.5-pro"
        assert model_config["temperature"] == 0.8
        assert model_config["max_tokens"] == 4000

    def test_get_model_config_default(self):
        """测试获取默认模型配置"""
        config = AgentConfig()
        model_config = config.get_model_config("unknown")

        # 应该返回medium配置作为默认值
        assert model_config["temperature"] == 0.7
        assert model_config["max_tokens"] == 2000

    def test_get_cache_config(self):
        """测试获取缓存配置"""
        config = AgentConfig()
        cache_config = config.get_cache_config()

        assert cache_config["memory_cache_size"] == config.MEMORY_CACHE_SIZE
        assert cache_config["redis_ttl"] == config.REDIS_TTL
        assert cache_config["connection_pool_size"] == config.REDIS_CONNECTION_POOL_SIZE
        assert cache_config["enable_quality_cache"] is config.ENABLE_QUALITY_CACHE

    def test_get_timeout_config(self):
        """测试获取超时配置"""
        config = AgentConfig()
        timeout_config = config.get_timeout_config()

        assert timeout_config["action_timeout"] == config.ACTION_TIMEOUT
        assert timeout_config["tool_timeout"] == config.TOOL_TIMEOUT
        assert timeout_config["llm_timeout"] == config.LLM_TIMEOUT

    def test_get_monitoring_config(self):
        """测试获取监控配置"""
        config = AgentConfig()
        monitoring_config = config.get_monitoring_config()

        assert monitoring_config["enable_performance_monitoring"] is config.ENABLE_PERFORMANCE_MONITORING
        assert monitoring_config["slow_query_threshold"] == config.SLOW_QUERY_THRESHOLD
        assert monitoring_config["cost_alert_threshold"] == config.COST_ALERT_THRESHOLD
        assert monitoring_config["daily_cost_limit"] == config.DAILY_COST_LIMIT


class TestConfigUtilities:
    """测试配置工具函数"""

    def test_get_config(self):
        """测试获取全局配置"""
        config = get_config()
        assert isinstance(config, AgentConfig)
        assert config.DEFAULT_MODEL == "gemini-2.5-flash"

    def test_reload_config_success(self):
        """测试重新加载配置成功"""
        with patch('app.config.agent_config.config') as mock_global_config:
            mock_config = AgentConfig(DEFAULT_MODEL="reloaded-model")
            mock_global_config.__setattr__ = Mock()

            new_config = reload_config(DEFAULT_MODEL="reloaded-model")

            assert isinstance(new_config, AgentConfig)
            assert new_config.DEFAULT_MODEL == "reloaded-model"

    def test_reload_config_validation_failure(self):
        """测试重新加载配置验证失败"""
        with pytest.raises(ValueError) as exc_info:
            reload_config(QUALITY_THRESHOLD=15.0)  # 无效值

        assert "配置验证失败" in str(exc_info.value)

    def test_load_config_from_file_not_exists(self):
        """测试从不存在的文件加载配置"""
        with pytest.raises(FileNotFoundError):
            load_config_from_file(Path("/nonexistent/config.json"))

    @patch('pathlib.Path.exists')
    def test_load_config_from_file_exists(self, mock_exists):
        """测试从存在的文件加载配置"""
        mock_exists.return_value = True

        # 目前这个函数只是返回新的AgentConfig实例
        config = load_config_from_file(Path("config.json"))
        assert isinstance(config, AgentConfig)


class TestConfigEnvironmentVariables:
    """测试环境变量支持"""

    @patch.dict(os.environ, {
        'DEFAULT_MODEL': 'env-model',
        'MAX_CONCURRENT_ACTIONS': '8',
        'ENABLE_MODEL_SELECTOR': 'false'
    })
    def test_environment_variables(self):
        """测试环境变量支持"""
        # 创建配置时应该读取环境变量
        config = AgentConfig()

        # 注意：pydantic会自动处理类型转换
        # 环境变量名需要与字段名完全匹配
        assert config.DEFAULT_MODEL == "env-model"
        assert config.MAX_CONCURRENT_ACTIONS == 8
        assert config.ENABLE_MODEL_SELECTOR is False

    def test_field_validation(self):
        """测试字段验证"""
        # 测试范围验证
        with pytest.raises(ValidationError):
            AgentConfig(MAX_CONCURRENT_ACTIONS=0)  # 小于最小值

        with pytest.raises(ValidationError):
            AgentConfig(MAX_CONCURRENT_ACTIONS=25)  # 大于最大值

        # 测试类型验证
        with pytest.raises(ValidationError):
            AgentConfig(DEFAULT_MODEL=123)  # 错误的类型

    def test_optional_fields(self):
        """测试可选字段"""
        config = AgentConfig()

        # 测试所有字段都有默认值
        assert hasattr(config, 'DEFAULT_MODEL')
        assert hasattr(config, 'FALLBACK_MODEL')
        assert hasattr(config, 'ENABLE_MODEL_SELECTOR')
        assert hasattr(config, 'ENABLE_COST_TRACKING')

        # 测试数值字段
        assert isinstance(config.MAX_CONCURRENT_ACTIONS, int)
        assert isinstance(config.QUALITY_THRESHOLD, float)
        assert isinstance(config.ENABLE_MODEL_SELECTOR, bool)


class TestConfigCategories:
    """测试配置分类"""

    def test_model_config_completeness(self):
        """测试模型配置完整性"""
        config = AgentConfig()

        # 检查所有模型相关配置
        model_configs = {
            "simple": config.get_model_config("simple"),
            "medium": config.get_model_config("medium"),
            "complex": config.get_model_config("complex")
        }

        for complexity, model_config in model_configs.items():
            assert "model" in model_config
            assert "temperature" in model_config
            assert "max_tokens" in model_config
            assert isinstance(model_config["temperature"], float)
            assert isinstance(model_config["max_tokens"], int)

    def test_performance_config_completeness(self):
        """测试性能配置完整性"""
        config = AgentConfig()

        # 检查所有性能相关配置
        assert config.MAX_CONCURRENT_ACTIONS > 0
        assert config.MAX_CONCURRENT_TOOLS > 0
        assert config.ACTION_TIMEOUT > 0
        assert config.TOOL_TIMEOUT > 0
        assert config.LLM_TIMEOUT > 0

    def test_monitoring_config_completeness(self):
        """测试监控配置完整性"""
        config = AgentConfig()

        monitoring_config = config.get_monitoring_config()

        assert "enable_performance_monitoring" in monitoring_config
        assert "slow_query_threshold" in monitoring_config
        assert "cost_alert_threshold" in monitoring_config
        assert "daily_cost_limit" in monitoring_config

        # 检查值的合理性
        assert monitoring_config["slow_query_threshold"] > 0
        assert monitoring_config["cost_alert_threshold"] > 0
        assert monitoring_config["daily_cost_limit"] >= 0


class TestConfigEdgeCases:
    """测试配置边界情况"""

    def test_boundary_values(self):
        """测试边界值"""
        # 测试最小值
        config = AgentConfig(
            MAX_CONCURRENT_ACTIONS=1,
            MAX_CONCURRENT_TOOLS=1,
            QUALITY_THRESHOLD=1.0,
            MEMORY_FORGET_THRESHOLD=0.0
        )
        errors = config.validate_config()
        assert errors == []  # 边界值应该有效

        # 测试最大值
        config = AgentConfig(
            MAX_CONCURRENT_ACTIONS=20,
            MAX_CONCURRENT_TOOLS=10,
            QUALITY_THRESHOLD=10.0,
            MEMORY_FORGET_THRESHOLD=1.0
        )
        errors = config.validate_config()
        assert errors == []  # 边界值应该有效

    def test_boolean_configurations(self):
        """测试布尔配置"""
        config = AgentConfig(
            ENABLE_MODEL_SELECTOR=False,
            ENABLE_COST_TRACKING=False,
            ENABLE_QUALITY_CACHE=False,
            ENABLE_PERFORMANCE_MONITORING=False,
            ENABLE_DATA_ENCRYPTION=False,
            ENABLE_EXPERIMENTAL_FEATURES=False
        )

        # 所有布尔配置应该都是False
        assert config.ENABLE_MODEL_SELECTOR is False
        assert config.ENABLE_COST_TRACKING is False
        assert config.ENABLE_QUALITY_CACHE is False
        assert config.ENABLE_PERFORMANCE_MONITORING is False
        assert config.ENABLE_DATA_ENCRYPTION is False
        assert config.ENABLE_EXPERIMENTAL_FEATURES is False


if __name__ == "__main__":
    pytest.main([__file__])