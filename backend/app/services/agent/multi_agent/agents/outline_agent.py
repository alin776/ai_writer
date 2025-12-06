"""大纲师 Agent

负责生成章节大纲，包括：
- 核心冲突
- 涉及角色
- 情绪曲线
- 伏笔设置
"""

from typing import Dict, Any
from .base_agent import BaseAgent
from ..prompts import OUTLINE_PROMPT

import logging

logger = logging.getLogger(__name__)


class OutlineAgent(BaseAgent):
    """大纲师 Agent

    职责：
    - 分析任务需求
    - 生成章节大纲
    - 设计冲突和情绪曲线
    - 规划角色出场和伏笔
    """

    @property
    def name(self) -> str:
        return "大纲师"

    @property
    def role_description(self) -> str:
        return "负责章节结构设计，规划冲突、角色、情绪曲线"

    async def execute(
        self,
        input_data: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """执行大纲生成

        Args:
            input_data: 包含任务描述等
            context: 包含总大纲、人设、前文摘要等

        Returns:
            章节大纲
        """
        return await self.generate(input_data, context)

    async def generate(
        self,
        task: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """生成章节大纲

        Args:
            task: 任务信息
            context: 上下文（total_outline, character_document, previous_summary）

        Returns:
            大纲结构
        """
        self._log_execution("开始生成章节大纲", {"task": task.get("description", "")[:50]})

        # 构建用户提示
        user_prompt = f"""请为以下写作任务生成章节大纲：

## 任务描述
{task.get('description', '未提供任务描述')}

## 总体大纲
{context.get('total_outline', '未提供总大纲')}

## 角色设定
{context.get('character_document', '未提供角色设定')}

## 前文摘要
{context.get('previous_summary', '这是第一章，无前文')}

## 章节ID
{task.get('chapter_id', 'unknown')}

请生成详细的章节大纲。"""

        # 调用 LLM
        response = await self._call_llm(
            system_prompt=OUTLINE_PROMPT,
            user_prompt=user_prompt,
            temperature=0.5,  # 大纲生成需要更稳定
            max_tokens=2000
        )

        # 解析响应
        result = self._parse_json_response(response)

        # 确保必要字段存在
        outline = {
            "chapter_id": result.get("chapter_id", task.get("chapter_id", "unknown")),
            "title": result.get("title", "未命名章节"),
            "core_conflict": result.get("core_conflict", ""),
            "characters": result.get("characters", []),
            "emotion_curve": result.get("emotion_curve", {}),
            "foreshadowing": result.get("foreshadowing", ""),
            "connection_to_previous": result.get("connection_to_previous", "")
        }

        self._log_execution("章节大纲生成完成", {"title": outline["title"]})

        return outline
