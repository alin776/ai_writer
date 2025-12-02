"""
约束提示词管理器
参考: LangChain PromptManager + 约束验证
"""
import yaml
from pathlib import Path
from typing import Dict, Optional, Callable, List
import logging

from .base import PromptTemplate, Constraint, ConstraintType

logger = logging.getLogger(__name__)


class ConstraintPromptManager:
    """
    约束提示词管理器

    功能:
    1. 加载YAML模板
    2. 格式化提示词
    3. 验证输出
    4. 版本管理
    """

    def __init__(self, templates_dir: str = "app/prompts/templates"):
        """
        初始化管理器

        Args:
            templates_dir: YAML模板目录路径
        """
        self.templates_dir = Path(templates_dir)
        self.templates: Dict[str, PromptTemplate] = {}
        self.validators: Dict[str, Callable] = {}

        # 注册验证器（稍后注入）
        self._register_validators()

        # 预加载所有模板
        self._load_all_templates()

        logger.info(
            f"✅ 约束提示词管理器已初始化: "
            f"加载{len(self.templates)}个模板, "
            f"注册{len(self.validators)}个验证器"
        )

    def _register_validators(self):
        """
        注册验证器

        🔧 2025-12-02: 重构 - 移除不合理的验证器
        - 移除 entity_validator（分析任务需要概括，不应检查实体差异）
        - 移除 consistency_validator（引用验证过于严格）
        - 现在使用 prompt 引导代替代码验证
        """
        # 验证器列表为空 - 使用 prompt 引导代替代码验证
        self.validators = {}

    def _load_all_templates(self):
        """加载所有YAML模板"""
        if not self.templates_dir.exists():
            logger.warning(f"模板目录不存在: {self.templates_dir}")
            return

        for yaml_file in self.templates_dir.glob("*.yaml"):
            try:
                template = self._load_template_from_yaml(yaml_file)
                self.templates[template.name] = template
                logger.info(f"✅ 已加载模板: {template.name} (v{template.version})")
            except Exception as e:
                logger.error(f"❌ 加载模板失败: {yaml_file.name}, 错误: {e}")

    def _load_template_from_yaml(self, yaml_file: Path) -> PromptTemplate:
        """
        从YAML文件加载模板

        Args:
            yaml_file: YAML文件路径

        Returns:
            PromptTemplate实例
        """
        with open(yaml_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        # 转换constraints
        constraints = [
            Constraint(
                type=ConstraintType(c['type']),
                description=c['description'],
                validation_func=c.get('validation_func')
            )
            for c in data.get('constraints', [])
        ]

        return PromptTemplate(
            name=data['name'],
            description=data.get('description'),
            version=data.get('version', '1.0.0'),
            role=data['role'],
            constraints=constraints,
            input_variables=data['input_variables'],
            output_format=data.get('output_format'),
            template=data['template'],
            tags=data.get('tags', [])
        )

    def format_prompt(self, template_name: str, **kwargs) -> str:
        """
        格式化提示词（组合版本，向后兼容）

        Args:
            template_name: 模板名称
            **kwargs: 输入变量

        Returns:
            格式化后的提示词

        Raises:
            ValueError: 模板不存在或参数错误
        """
        template = self.templates.get(template_name)
        if not template:
            raise ValueError(
                f"模板不存在: {template_name}. "
                f"可用模板: {list(self.templates.keys())}"
            )

        # 验证输入
        valid, error = template.validate_inputs(**kwargs)
        if not valid:
            raise ValueError(f"输入验证失败: {error}")

        # 使用向后兼容的组合方法
        return template.format_combined(**kwargs)

    def format_prompt_separated(self, template_name: str, **kwargs) -> Dict[str, str]:
        """
        格式化提示词（分离版本，推荐用于新代码）

        Args:
            template_name: 模板名称
            **kwargs: 输入变量

        Returns:
            {
                "system": "系统提示",
                "user": "用户消息"
            }

        Raises:
            ValueError: 模板不存在或参数错误
        """
        template = self.templates.get(template_name)
        if not template:
            raise ValueError(
                f"模板不存在: {template_name}. "
                f"可用模板: {list(self.templates.keys())}"
            )

        # 验证输入
        valid, error = template.validate_inputs(**kwargs)
        if not valid:
            raise ValueError(f"输入验证失败: {error}")

        # 返回分离的消息
        return template.format(**kwargs)

    def validate_output(
        self,
        template_name: str,
        source_text: str,
        ai_output: str
    ) -> Dict:
        """
        验证AI输出（关键功能！）

        Args:
            template_name: 模板名称
            source_text: 源文本
            ai_output: AI输出

        Returns:
            {
                "valid": bool,
                "details": [...],
                "template": str,
                "version": str
            }
        """
        template = self.templates.get(template_name)
        if not template:
            return {
                "valid": False,
                "error": f"模板不存在: {template_name}"
            }

        results = []

        # 执行所有验证器
        for constraint in template.constraints:
            if constraint.validation_func:
                validator_func = self.validators.get(constraint.validation_func)

                if not validator_func:
                    logger.warning(
                        f"验证器不存在: {constraint.validation_func}"
                    )
                    continue

                try:
                    result = validator_func(source_text, ai_output)
                    results.append({
                        "constraint": constraint.description,
                        "validation_func": constraint.validation_func,
                        "result": result
                    })
                except Exception as e:
                    logger.error(f"验证器执行失败: {e}")
                    results.append({
                        "constraint": constraint.description,
                        "validation_func": constraint.validation_func,
                        "result": {"valid": False, "error": str(e)}
                    })

        # 汇总结果
        all_valid = all(r["result"].get("valid", True) for r in results)

        return {
            "valid": all_valid,
            "details": results,
            "template": template_name,
            "version": template.version,
            "total_constraints": len(template.constraints),
            "validated_constraints": len(results)
        }

    def get_template(self, name: str) -> Optional[PromptTemplate]:
        """获取模板"""
        return self.templates.get(name)

    def list_templates(self) -> List[str]:
        """列出所有可用模板"""
        return list(self.templates.keys())


# 全局单例
_constraint_manager: Optional[ConstraintPromptManager] = None


def get_constraint_manager() -> ConstraintPromptManager:
    """获取全局约束提示词管理器"""
    global _constraint_manager
    if _constraint_manager is None:
        _constraint_manager = ConstraintPromptManager()
    return _constraint_manager
