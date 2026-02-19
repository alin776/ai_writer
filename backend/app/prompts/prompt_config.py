"""
Prompt 配置集中管理

统一管理所有 Prompt 相关配置，包括：
- 模块路径索引
- 模板文件索引
- 版本信息
- 通用配置参数

参考: context_config.py, memory_config.py
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum


class PromptCategory(Enum):
    """Prompt 类别枚举"""
    AI_SERVICE = "ai_service"           # AI 服务层 Prompt
    AGENT = "agent"                     # Agent 专用 Prompt
    REVIEW = "review"                   # 评审 Prompt
    EVALUATION = "evaluation"           # 评估 Prompt
    PLANNING = "planning"               # 规划 Prompt
    CONTENT_CREATION = "content_creation"  # 内容创作 Prompt
    TEMPLATE = "template"               # YAML/JSON 模板文件
    CONFIG = "config"                   # 配置类 Prompt


class PromptFileType(Enum):
    """Prompt 文件类型"""
    PYTHON = "python"       # Python 模块
    YAML = "yaml"           # YAML 模板文件
    JSON = "json"           # JSON 配置文件


@dataclass
class PromptModuleInfo:
    """Prompt 模块信息"""
    path: str                           # 模块/文件路径
    description: str                    # 模块描述
    category: PromptCategory            # 类别
    file_type: PromptFileType = PromptFileType.PYTHON  # 文件类型
    version: str = "1.0.0"              # 版本号
    deprecated: bool = False            # 是否废弃


class PromptConfig:
    """Prompt 配置中心"""

    # ==================== Python 模块注册表 ====================

    MODULES: Dict[str, PromptModuleInfo] = {
        # AI 服务层 Prompt
        "ai_prompts": PromptModuleInfo(
            path="app.services.ai.prompts",
            description="AI 基础服务 Prompt (续写/润色/扩展/翻译)",
            category=PromptCategory.AI_SERVICE,
            version="1.0.0"
        ),
        "evaluation_prompts": PromptModuleInfo(
            path="app.services.ai.evaluation_prompts",
            description="AI 评估 Prompt",
            category=PromptCategory.EVALUATION,
            version="1.0.0"
        ),

        # 主 Prompt 模块
        "review_prompts": PromptModuleInfo(
            path="app.prompts.review_prompts",
            description="评审 Prompt 模板",
            category=PromptCategory.REVIEW,
            version="1.0.0"
        ),
        "prompt_manager": PromptModuleInfo(
            path="app.prompts.prompt_manager",
            description="YAML 模板管理器",
            category=PromptCategory.AGENT,
            version="1.0.0"
        ),

        # 配置类 Prompt
        "agent_config": PromptModuleInfo(
            path="app.core.agent_config",
            description="Agent 配置 (含 system_prompt)",
            category=PromptCategory.CONFIG,
            version="1.0.0"
        ),
    }

    # ==================== YAML 模板文件注册表 ====================

    YAML_TEMPLATES: Dict[str, PromptModuleInfo] = {
        "writing_agent": PromptModuleInfo(
            path="app/prompts/templates/writing_agent.yaml",
            description="写作 Agent Prompt",
            category=PromptCategory.TEMPLATE,
            file_type=PromptFileType.YAML,
            version="1.0.0"
        ),
        "system_agent_prompt": PromptModuleInfo(
            path="app/prompts/templates/system_agent_prompt.yaml",
            description="双Prompt架构：系统层 Prompt",
            category=PromptCategory.TEMPLATE,
            file_type=PromptFileType.YAML,
            version="1.0.0"
        ),
        "creative_writing_prompt": PromptModuleInfo(
            path="app/prompts/templates/creative_writing_prompt.yaml",
            description="双Prompt架构：创作层 Prompt",
            category=PromptCategory.TEMPLATE,
            file_type=PromptFileType.YAML,
            version="1.0.0"
        ),
        "analyze_text": PromptModuleInfo(
            path="app/prompts/templates/analyze_text.yaml",
            description="文本分析 Prompt",
            category=PromptCategory.TEMPLATE,
            file_type=PromptFileType.YAML,
            version="1.0.0"
        ),
    }

    # ==================== JSON 配置文件注册表 ====================

    JSON_CONFIGS: Dict[str, PromptModuleInfo] = {
        "default_prompts": PromptModuleInfo(
            path="app/services/ai/prompts/default.json",
            description="默认 Prompt 配置 (autocomplete/complete/polish/expand/summarize/translate)",
            category=PromptCategory.CONFIG,
            file_type=PromptFileType.JSON,
            version="1.0.0"
        ),
        "novel_analysis": PromptModuleInfo(
            path="app/services/ai/prompts/novel_analysis.json",
            description="小说分析 Prompt 配置",
            category=PromptCategory.CONFIG,
            file_type=PromptFileType.JSON,
            version="1.0.0"
        ),
    }

    # ==================== 通用配置 ====================

    # Prompt 缓存配置
    CACHE_ENABLED: bool = True
    CACHE_TTL: int = 3600               # 缓存 TTL (秒)
    CACHE_MAX_SIZE: int = 100           # 最大缓存条目数

    # Prompt 长度限制
    MAX_SYSTEM_PROMPT_LENGTH: int = 8000    # 系统 Prompt 最大长度
    MAX_USER_PROMPT_LENGTH: int = 4000      # 用户 Prompt 最大长度

    # 模板渲染配置
    TEMPLATE_ENGINE: str = "jinja2"         # 模板引擎 (jinja2/string)
    STRICT_MODE: bool = False               # 严格模式 (缺少变量时抛异常)

    # 版本控制配置
    VERSION_TRACKING_ENABLED: bool = True   # 是否启用版本追踪
    MAX_VERSION_HISTORY: int = 10           # 最大版本历史数

    # ==================== 便捷方法 ====================

    @classmethod
    def get_modules_by_category(cls, category: PromptCategory) -> Dict[str, PromptModuleInfo]:
        """按类别获取 Prompt 模块（包括所有类型）"""
        result = {}
        # Python 模块
        for name, info in cls.MODULES.items():
            if info.category == category:
                result[name] = info
        # YAML 模板
        for name, info in cls.YAML_TEMPLATES.items():
            if info.category == category:
                result[name] = info
        # JSON 配置
        for name, info in cls.JSON_CONFIGS.items():
            if info.category == category:
                result[name] = info
        return result

    @classmethod
    def get_modules_by_file_type(cls, file_type: PromptFileType) -> Dict[str, PromptModuleInfo]:
        """按文件类型获取 Prompt 模块"""
        result = {}
        if file_type == PromptFileType.PYTHON:
            result.update(cls.MODULES)
        elif file_type == PromptFileType.YAML:
            result.update(cls.YAML_TEMPLATES)
        elif file_type == PromptFileType.JSON:
            result.update(cls.JSON_CONFIGS)
        return result

    @classmethod
    def get_module_path(cls, module_name: str) -> Optional[str]:
        """获取模块路径（搜索所有注册表）"""
        # 先查 Python 模块
        if module_name in cls.MODULES:
            return cls.MODULES[module_name].path
        # 再查 YAML 模板
        if module_name in cls.YAML_TEMPLATES:
            return cls.YAML_TEMPLATES[module_name].path
        # 最后查 JSON 配置
        if module_name in cls.JSON_CONFIGS:
            return cls.JSON_CONFIGS[module_name].path
        return None

    @classmethod
    def list_all_modules(cls) -> List[str]:
        """列出所有模块名称"""
        all_names = list(cls.MODULES.keys())
        all_names.extend(cls.YAML_TEMPLATES.keys())
        all_names.extend(cls.JSON_CONFIGS.keys())
        return all_names

    @classmethod
    def get_category_summary(cls) -> Dict[str, int]:
        """获取各类别 Prompt 数量统计"""
        summary = {}
        for category in PromptCategory:
            count = len(cls.get_modules_by_category(category))
            if count > 0:
                summary[category.value] = count
        return summary

    @classmethod
    def get_file_type_summary(cls) -> Dict[str, int]:
        """获取各文件类型 Prompt 数量统计"""
        return {
            "python": len(cls.MODULES),
            "yaml": len(cls.YAML_TEMPLATES),
            "json": len(cls.JSON_CONFIGS),
        }


class PromptRegistry:
    """
    Prompt 统一注册表

    提供全局访问入口，整合所有 Prompt 管理器
    """

    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self._managers = {}
        self._initialized = True

    def register_manager(self, name: str, manager: object):
        """注册一个 Prompt 管理器"""
        self._managers[name] = manager

    def get_manager(self, name: str) -> Optional[object]:
        """获取 Prompt 管理器"""
        return self._managers.get(name)

    def list_managers(self) -> List[str]:
        """列出所有已注册的管理器"""
        return list(self._managers.keys())

    @classmethod
    def get_instance(cls) -> "PromptRegistry":
        """获取单例实例"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance


# 全局单例
_prompt_registry: Optional[PromptRegistry] = None


def get_prompt_registry() -> PromptRegistry:
    """获取全局 PromptRegistry 单例"""
    global _prompt_registry
    if _prompt_registry is None:
        _prompt_registry = PromptRegistry()
    return _prompt_registry
