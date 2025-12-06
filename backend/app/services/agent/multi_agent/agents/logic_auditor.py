"""逻辑审计 Agent

负责检查内容中的逻辑一致性和合理性。
"""

from typing import Dict, Any
from .base_agent import BaseAgent
from ..prompts import LOGIC_AUDITOR_PROMPT

import logging

logger = logging.getLogger(__name__)


class LogicAuditor(BaseAgent):
    """逻辑审计 Agent

    职责：
    - 检查情节逻辑一致性
    - 检查时间线合理性
    - 检查因果关系
    - 检查设定冲突
    """

    @property
    def name(self) -> str:
        return "逻辑审计"

    @property
    def role_description(self) -> str:
        return "负责检查情节逻辑一致性和合理性"

    async def execute(
        self,
        input_data: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """执行逻辑检查

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
        """检查逻辑一致性

        Args:
            draft: 初稿（包含 content）
            work_id: 作品 ID
            context: 上下文（previous_summary, world_setting）

        Returns:
            检查结果，包含 status 和 issues
        """
        self._log_execution("开始逻辑一致性检查")

        content = draft.get("content", "")
        previous_summary = context.get("previous_summary", "")
        world_setting = context.get("world_setting", "")

        user_prompt = f"""请检查以下章节内容的逻辑一致性：

## 前文摘要
{previous_summary or '这是第一章，无前文'}

## 世界观设定
{world_setting or '未提供世界观设定'}

## 当前章节内容
{content[:6000]}  # 限制长度

请进行逻辑一致性检查。"""

        # 调用 LLM
        response = await self._call_llm(
            system_prompt=LOGIC_AUDITOR_PROMPT,
            user_prompt=user_prompt,
            temperature=0.3,
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
            "逻辑检查完成",
            {"status": check_result["status"], "issue_count": len(check_result["issues"])}
        )

        return check_result
