"""角色守护 Agent

负责检查内容中角色表现的一致性。
"""

from typing import Dict, Any, List
from .base_agent import BaseAgent
from ..prompts import CHARACTER_GUARD_PROMPT

import logging

logger = logging.getLogger(__name__)


class CharacterGuard(BaseAgent):
    """角色守护 Agent

    职责：
    - 检查角色性格一致性
    - 检查对话风格一致性
    - 检查角色行为合理性
    - 识别人设崩塌问题
    """

    @property
    def name(self) -> str:
        return "角色守护"

    @property
    def role_description(self) -> str:
        return "负责检查角色一致性，防止人设崩塌"

    async def execute(
        self,
        input_data: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """执行角色检查

        Args:
            input_data: 初稿内容
            context: 上下文信息

        Returns:
            检查结果
        """
        return await self.check(input_data, context.get("work_id", ""), context)

    async def check(
        self,
        draft: Dict[str, Any],
        work_id: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """检查角色一致性

        Args:
            draft: 初稿（包含 content）
            work_id: 作品 ID
            context: 上下文（character_document）

        Returns:
            检查结果，包含 status 和 issues
        """
        self._log_execution("开始角色一致性检查")

        content = draft.get("content", "")
        character_doc = context.get("character_document", "")

        if not character_doc:
            self._log_execution("无角色设定，跳过检查")
            return {
                "status": "PASS",
                "issues": [],
                "summary": "无角色设定文档，跳过检查"
            }

        user_prompt = f"""请检查以下章节内容中的角色表现是否符合角色设定：

## 角色设定
{character_doc}

## 章节内容
{content[:6000]}  # 限制长度避免超出 token

请进行角色一致性检查。"""

        # 调用 LLM
        response = await self._call_llm(
            system_prompt=CHARACTER_GUARD_PROMPT,
            user_prompt=user_prompt,
            temperature=0.3,  # 审查需要更稳定
            max_tokens=2000
        )

        # 解析响应
        result = self._parse_json_response(response)

        check_result = {
            "status": result.get("status", "PASS"),
            "issues": result.get("issues", []),
            "summary": result.get("summary", "检查完成")
        }

        self._log_execution(
            "角色检查完成",
            {"status": check_result["status"], "issue_count": len(check_result["issues"])}
        )

        return check_result
