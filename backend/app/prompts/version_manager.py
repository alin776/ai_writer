"""
Prompt版本管理器

负责Prompt版本跟踪、A/B测试等功能
"""

import json
import time
from typing import Dict, Any, Optional
from datetime import datetime


class PromptVersionManager:
    """Prompt版本管理器"""

    def __init__(self):
        """初始化版本管理器"""
        # 活跃版本映射 {template_name: version}
        self.active_versions: Dict[str, str] = {}

        # A/B测试配置 {template_name: test_config}
        self.ab_tests: Dict[str, Dict] = {}

        # 版本使用记录（内存存储，生产环境应使用Redis等）
        self.version_usage: Dict[str, list] = {}

        # 初始化默认版本
        self._init_default_versions()

    def _init_default_versions(self):
        """初始化默认版本配置"""
        default_templates = [
            "intent_classifier",
            "writing_agent",
            "planning_agent",
            "tool_agent"
        ]

        for template_name in default_templates:
            self.active_versions[template_name] = "1.0.0"

    def get_prompt_version(
        self,
        template_name: str,
        session_id: Optional[str] = None
    ) -> str:
        """
        获取要使用的Prompt版本

        Args:
            template_name: 模板名称
            session_id: 会话ID（用于A/B测试）

        Returns:
            版本号（如 "1.0.0" 或 "1.1.0-beta"）
        """
        # 检查是否在A/B测试中
        if template_name in self.ab_tests and session_id:
            version = self._get_ab_test_version(template_name, session_id)
        else:
            # 返回活跃版本
            version = self.active_versions.get(template_name, "1.0.0")

        # 记录版本使用
        self._record_version_usage(template_name, version, session_id)

        return version

    def _get_ab_test_version(
        self,
        template_name: str,
        session_id: str
    ) -> str:
        """
        获取A/B测试版本

        使用session_id的哈希值来稳定分配版本
        确保同一会话始终使用同一版本

        Args:
            template_name: 模板名称
            session_id: 会话ID

        Returns:
            分配的版本号
        """
        test_config = self.ab_tests[template_name]

        # 使用session_id的哈希值来分配版本（确保稳定性）
        hash_value = hash(f"{template_name}:{session_id}")
        normalized_hash = abs(hash_value) % 100 / 100.0  # 转换为0-1之间的值

        # 根据流量配置分配版本
        cumulative = 0.0
        for version, traffic in test_config["traffic"].items():
            cumulative += traffic
            if normalized_hash < cumulative:
                return version

        # 默认返回control组
        return test_config["control"]

    def _record_version_usage(
        self,
        template_name: str,
        version: str,
        session_id: Optional[str]
    ):
        """
        记录版本使用情况

        Args:
            template_name: 模板名称
            version: 版本号
            session_id: 会话ID
        """
        key = f"{template_name}:{version}"

        if key not in self.version_usage:
            self.version_usage[key] = []

        self.version_usage[key].append({
            "timestamp": datetime.now().isoformat(),
            "session_id": session_id
        })

    def set_active_version(self, template_name: str, version: str):
        """
        设置活跃版本

        Args:
            template_name: 模板名称
            version: 版本号
        """
        self.active_versions[template_name] = version
        print(f"已设置 {template_name} 的活跃版本为: {version}")

    def create_ab_test(
        self,
        template_name: str,
        control_version: str,
        test_version: str,
        traffic_split: float = 0.5
    ):
        """
        创建A/B测试

        Args:
            template_name: 模板名称
            control_version: 对照版本
            test_version: 测试版本
            traffic_split: 测试组流量比例（0-1）
        """
        if not 0 <= traffic_split <= 1:
            raise ValueError("traffic_split 必须在0-1之间")

        self.ab_tests[template_name] = {
            "control": control_version,
            "traffic": {
                control_version: 1.0 - traffic_split,
                test_version: traffic_split
            },
            "created_at": datetime.now().isoformat()
        }

        print(
            f"已创建A/B测试: {template_name}\n"
            f"  对照组: {control_version} ({(1-traffic_split)*100:.0f}%)\n"
            f"  测试组: {test_version} ({traffic_split*100:.0f}%)"
        )

    def stop_ab_test(self, template_name: str, winning_version: Optional[str] = None):
        """
        停止A/B测试

        Args:
            template_name: 模板名称
            winning_version: 获胜版本（如果指定，会设置为活跃版本）
        """
        if template_name not in self.ab_tests:
            print(f"警告: {template_name} 没有进行中的A/B测试")
            return

        test_config = self.ab_tests.pop(template_name)

        if winning_version:
            self.set_active_version(template_name, winning_version)

        print(f"已停止 {template_name} 的A/B测试")

    def get_version_stats(self, template_name: str) -> Dict[str, Any]:
        """
        获取版本使用统计

        Args:
            template_name: 模板名称

        Returns:
            统计信息字典
        """
        stats = {
            "template_name": template_name,
            "active_version": self.active_versions.get(template_name, "unknown"),
            "versions": {}
        }

        # 统计各版本使用次数
        for key, records in self.version_usage.items():
            if key.startswith(f"{template_name}:"):
                version = key.split(":", 1)[1]
                stats["versions"][version] = {
                    "usage_count": len(records),
                    "unique_sessions": len(set(
                        r["session_id"] for r in records if r["session_id"]
                    ))
                }

        # 添加A/B测试信息
        if template_name in self.ab_tests:
            stats["ab_test"] = self.ab_tests[template_name]

        return stats

    def record_prompt_metrics(
        self,
        template_name: str,
        version: str,
        session_id: str,
        metrics: Dict[str, Any]
    ):
        """
        记录Prompt效果指标

        Args:
            template_name: 模板名称
            version: 版本号
            session_id: 会话ID
            metrics: 指标数据
        """
        # 简化实现：仅打印日志
        # 生产环境应该存储到数据库或监控系统
        print(
            f"Prompt指标 - {template_name}:{version}\n"
            f"  会话: {session_id}\n"
            f"  指标: {json.dumps(metrics, ensure_ascii=False, indent=2)}"
        )


# 全局单例实例
_version_manager_instance: Optional[PromptVersionManager] = None


def get_version_manager() -> PromptVersionManager:
    """
    获取全局VersionManager单例

    Returns:
        PromptVersionManager实例
    """
    global _version_manager_instance
    if _version_manager_instance is None:
        _version_manager_instance = PromptVersionManager()
    return _version_manager_instance
