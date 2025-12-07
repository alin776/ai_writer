"""总编 Agent

负责根据审查意见进行最终修订。
"""

from typing import Dict, Any, List
from app.services.agent.model_selector import TaskType
from .base_agent import BaseAgent
from ..prompts import EDITOR_PROMPT

import logging

logger = logging.getLogger(__name__)


class EditorAgent(BaseAgent):
    """总编 Agent

    职责：
    - 综合角色守护和逻辑审计的意见
    - 进行最终修订
    - 确保内容质量
    """

    @property
    def name(self) -> str:
        return "总编"

    @property
    def role_description(self) -> str:
        return "负责综合审查意见进行最终修订"

    async def execute(
        self,
        input_data: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """执行修订

        Args:
            input_data: 初稿和审查结果
            context: 上下文信息

        Returns:
            修订结果
        """
        draft = input_data.get("draft", {})
        character_review = input_data.get("character_review", {})
        logic_review = input_data.get("logic_review", {})
        return await self.revise(draft, character_review, logic_review, context)

    async def revise(
        self,
        draft: Dict[str, Any],
        character_review: Dict[str, Any],
        logic_review: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """根据审查意见修订内容

        Args:
            draft: 初稿
            character_review: 角色检查结果
            logic_review: 逻辑检查结果
            context: 上下文

        Returns:
            修订后的内容
        """
        self._log_execution("开始综合修订")

        content = draft.get("content", "")

        # 收集所有问题
        all_issues = []

        character_issues = character_review.get("issues", [])
        for issue in character_issues:
            issue["source"] = "角色守护"
            all_issues.append(issue)

        logic_issues = logic_review.get("issues", [])
        for issue in logic_issues:
            issue["source"] = "逻辑审计"
            all_issues.append(issue)

        if not all_issues:
            self._log_execution("无需修订，直接返回原稿")
            return {
                "content": content,
                "word_count": len(content),
                "quality_score": 0.9,
                "revision_summary": "无需修订",
                "conflicts_resolved": []
            }

        # 构建问题描述
        issues_text = "\n".join([
            f"- [{issue.get('source', '未知')}] {issue.get('type', '问题')}: {issue.get('description', '')} "
            f"| 建议: {issue.get('suggestion', '无')}"
            for issue in all_issues
        ])

        user_prompt = f"""请根据以下审查意见修订章节内容：

## 审查问题（共 {len(all_issues)} 个）
{issues_text}

## 原始内容
{content}

## 角色设定参考
{context.get('character_document', '未提供')}

请修订内容，解决上述问题，直接输出修订后的完整内容。"""

        # 调用 LLM
        response = await self._call_llm(
            system_prompt=EDITOR_PROMPT,
            user_prompt=user_prompt,
            temperature=0.6,
            max_tokens=4000,
            task_type=TaskType.TEXT_POLISH
        )

        # 计算质量评分（简单估算）
        quality_score = max(0.7, 0.95 - len(all_issues) * 0.05)

        result = {
            "content": response,
            "word_count": len(response),
            "quality_score": quality_score,
            "revision_summary": f"已修订 {len(all_issues)} 个问题",
            "conflicts_resolved": [
                {
                    "type": issue.get("type", ""),
                    "source": issue.get("source", ""),
                    "resolved": True
                }
                for issue in all_issues
            ]
        }

        self._log_execution(
            "修订完成",
            {"issues_resolved": len(all_issues), "word_count": result["word_count"]}
        )

        return result
