"""
提示词系统基础类
参考: LangChain + GitHub Blog Agentic Primitives
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class ConstraintType(str, Enum):
    """约束类型枚举"""
    MUST = "must"           # 必须遵守
    MUST_NOT = "must_not"   # 必须禁止
    SHOULD = "should"       # 应该遵守（建议）


class Constraint(BaseModel):
    """
    单个约束定义

    示例:
    Constraint(
        type=ConstraintType.MUST,
        description="只能分析提供的文本内容",
        validation_func="validate_entities"
    )
    """
    type: ConstraintType = Field(..., description="约束类型")
    description: str = Field(..., description="约束描述")
    validation_func: Optional[str] = Field(
        None,
        description="关联的验证函数名称"
    )


class PromptTemplate(BaseModel):
    """
    结构化提示词模板

    核心字段:
    - name: 模板名称（唯一标识）
    - role: AI角色定义
    - constraints: 约束条件列表
    - input_variables: 输入变量列表
    - template: 模板主体
    """
    name: str = Field(..., description="模板名称")
    description: Optional[str] = Field(None, description="模板描述")
    version: str = Field("1.0.0", description="版本号")

    role: str = Field(..., description="AI角色定义")
    constraints: List[Constraint] = Field(
        default_factory=list,
        description="约束条件列表"
    )
    input_variables: List[str] = Field(..., description="输入变量列表")
    output_format: Optional[str] = Field(None, description="输出格式说明")
    template: str = Field(..., description="模板主体")

    tags: List[str] = Field(default_factory=list, description="标签")

    def format(self, **kwargs) -> Dict[str, str]:
        """
        格式化提示词（分离system和user message）

        Args:
            **kwargs: 输入变量的值

        Returns:
            Dict包含:
                - system: 系统提示（角色+约束）
                - user: 用户消息（实际内容）

        Raises:
            ValueError: 缺少必要的输入变量
        """
        # 1. 验证输入变量
        missing_vars = set(self.input_variables) - set(kwargs.keys())
        if missing_vars:
            raise ValueError(f"缺少必要的输入变量: {missing_vars}")

        # 2. 构建系统提示（角色+约束）
        system_prompt = f"**角色**: {self.role}\n\n"

        # 3. 添加约束（关键！）
        if self.constraints:
            system_prompt += "**重要约束**:\n"
            for i, constraint in enumerate(self.constraints, 1):
                # 根据约束类型选择图标
                if constraint.type == ConstraintType.MUST:
                    icon = "✅ [必须]"
                elif constraint.type == ConstraintType.MUST_NOT:
                    icon = "❌ [禁止]"
                else:
                    icon = "💡 [建议]"

                system_prompt += f"{i}. {icon} {constraint.description}\n"
            system_prompt += "\n"

        # 4. 添加输出格式说明
        if self.output_format:
            system_prompt += f"**输出格式**: {self.output_format}\n\n"

        # 5. 格式化用户消息模板
        try:
            user_message = self.template.format(**kwargs)
        except KeyError as e:
            raise ValueError(f"模板格式化失败: {e}")

        # ✅ 修复：返回分离的system和user message
        return {
            "system": system_prompt.strip(),
            "user": user_message.strip()
        }

    def format_combined(self, **kwargs) -> str:
        """
        格式化为单个字符串（向后兼容）

        Returns:
            组合的提示词
        """
        messages = self.format(**kwargs)
        return f"{messages['system']}\n\n{messages['user']}"

    def validate_inputs(self, **kwargs) -> tuple[bool, Optional[str]]:
        """
        验证输入参数

        Args:
            **kwargs: 输入参数

        Returns:
            (是否有效, 错误信息)
        """
        # 检查必要参数
        missing = set(self.input_variables) - set(kwargs.keys())
        if missing:
            return False, f"缺少必要参数: {missing}"

        # 检查参数值非空
        empty_vars = [k for k, v in kwargs.items() if not v]
        if empty_vars:
            return False, f"以下参数值为空: {empty_vars}"

        return True, None

    class Config:
        use_enum_values = True
