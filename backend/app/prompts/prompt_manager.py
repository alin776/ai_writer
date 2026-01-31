"""
Prompt模板管理器

负责加载、管理和渲染各类Prompt模板
"""

import os
import yaml
from typing import Dict, Any, Optional
from jinja2 import Template
from pathlib import Path


class PromptManager:
    """Prompt模板管理器"""

    def __init__(self, prompts_dir: Optional[str] = None):
        """
        初始化PromptManager

        Args:
            prompts_dir: Prompt模板目录路径，默认为当前目录下的templates
        """
        if prompts_dir is None:
            # 默认使用当前文件所在目录的templates子目录
            current_dir = Path(__file__).parent
            prompts_dir = current_dir / "templates"

        self.prompts_dir = Path(prompts_dir)
        self.templates: Dict[str, Template] = {}
        self.versions: Dict[str, str] = {}
        self.descriptions: Dict[str, str] = {}

        # 加载所有模板
        self._load_templates()

    def _load_templates(self):
        """加载所有Prompt模板"""
        if not self.prompts_dir.exists():
            raise FileNotFoundError(f"Prompt模板目录不存在: {self.prompts_dir}")

        # 定义需要加载的模板列表
        template_files = [
            "analyze_text.yaml",  # 文本分析模板
            "writing_agent.yaml",
            "system_agent_prompt.yaml",  # 🆕 双Prompt架构：系统层Prompt
            "creative_writing_prompt.yaml",  # 🆕 双Prompt架构：创作层Prompt
        ]

        for filename in template_files:
            try:
                template_name = filename.replace(".yaml", "")
                self._load_template(filename, template_name)
            except FileNotFoundError:
                # 模板文件不存在时跳过（因为可能还未创建）
                print(f"警告: 模板文件不存在，跳过: {filename}")
                continue
            except Exception as e:
                print(f"警告: 加载模板失败 {filename}: {e}")
                continue

    def _load_template(self, filename: str, template_name: str):
        """
        加载单个模板文件

        Args:
            filename: 模板文件名
            template_name: 模板名称（用于索引）
        """
        filepath = self.prompts_dir / filename

        if not filepath.exists():
            raise FileNotFoundError(f"模板文件不存在: {filepath}")

        with open(filepath, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)

        # 保存版本信息和描述
        self.versions[template_name] = config.get("version", "1.0.0")
        self.descriptions[template_name] = config.get("description", "")

        # 创建Jinja2模板
        template_str = config.get("template", "")
        if not template_str:
            raise ValueError(f"模板 {filename} 中缺少 template 字段")

        self.templates[template_name] = Template(template_str)
        print(f"成功加载模板: {template_name} (版本 {self.versions[template_name]})")

    def render(self, template_name: str, **kwargs) -> str:
        """
        渲染模板

        Args:
            template_name: 模板名称
            **kwargs: 模板参数

        Returns:
            渲染后的Prompt文本

        Raises:
            ValueError: 模板不存在
        """
        template = self.templates.get(template_name)
        if not template:
            available = ", ".join(self.templates.keys())
            raise ValueError(
                f"模板不存在: {template_name}. "
                f"可用模板: {available}"
            )

        try:
            return template.render(**kwargs)
        except Exception as e:
            raise ValueError(f"模板渲染失败 {template_name}: {e}")

    def get_version(self, template_name: str) -> str:
        """
        获取模板版本

        Args:
            template_name: 模板名称

        Returns:
            版本号字符串
        """
        return self.versions.get(template_name, "unknown")

    def get_description(self, template_name: str) -> str:
        """
        获取模板描述

        Args:
            template_name: 模板名称

        Returns:
            描述文本
        """
        return self.descriptions.get(template_name, "")

    def list_templates(self) -> Dict[str, Dict[str, str]]:
        """
        列出所有已加载的模板

        Returns:
            模板信息字典 {template_name: {version, description}}
        """
        return {
            name: {
                "version": self.versions.get(name, "unknown"),
                "description": self.descriptions.get(name, "")
            }
            for name in self.templates.keys()
        }

    def reload_template(self, template_name: str):
        """
        重新加载指定模板（用于开发调试）

        Args:
            template_name: 模板名称
        """
        filename = f"{template_name}.yaml"
        try:
            self._load_template(filename, template_name)
            print(f"模板已重新加载: {template_name}")
        except Exception as e:
            print(f"重新加载失败: {e}")


# 全局单例实例（可选）
_prompt_manager_instance: Optional[PromptManager] = None


def get_prompt_manager() -> PromptManager:
    """
    获取全局PromptManager单例

    Returns:
        PromptManager实例
    """
    global _prompt_manager_instance
    if _prompt_manager_instance is None:
        _prompt_manager_instance = PromptManager()
    return _prompt_manager_instance
