"""主笔 Agent

负责根据大纲撰写章节内容。
"""

from typing import Dict, Any
from .base_agent import BaseAgent
from ..prompts import WRITER_PROMPT

import logging

logger = logging.getLogger(__name__)


class WriterAgent(BaseAgent):
    """主笔 Agent

    职责：
    - 根据大纲撰写正文
    - 保持文风一致
    - 控制字数和节奏
    """

    @property
    def name(self) -> str:
        return "主笔"

    @property
    def role_description(self) -> str:
        return "负责根据大纲撰写章节正文内容"

    async def execute(
        self,
        input_data: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """执行写作

        Args:
            input_data: 章节大纲
            context: 上下文信息

        Returns:
            写作结果
        """
        return await self.write(input_data, context)

    async def write(
        self,
        outline: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """根据大纲撰写内容

        Args:
            outline: 章节大纲
            context: 上下文（character_document, previous_content, style_guide）

        Returns:
            包含 content 和 word_count 的字典
        """
        self._log_execution("开始撰写章节", {"title": outline.get("title", "")})

        # 构建用户提示
        characters_info = "\n".join([
            f"- {c.get('name', '未知')}: {c.get('role', '')}，情绪变化：{c.get('emotion_arc', '')}"
            for c in outline.get("characters", [])
        ]) or "无特定角色要求"

        emotion_curve = outline.get("emotion_curve", {})
        emotion_info = f"""
- 开头：{emotion_curve.get('start', '平静')}
- 发展：{emotion_curve.get('development', '渐进')}
- 高潮：{emotion_curve.get('climax', '紧张')}
- 结尾：{emotion_curve.get('end', '余韵')}
"""

        user_prompt = f"""请根据以下大纲撰写章节内容：

## 章节标题
{outline.get('title', '未命名章节')}

## 核心冲突
{outline.get('core_conflict', '无')}

## 涉及角色
{characters_info}

## 情绪曲线
{emotion_info}

## 与前文衔接
{outline.get('connection_to_previous', '无需衔接')}

## 伏笔设置
{outline.get('foreshadowing', '无')}

## 角色设定参考
{context.get('character_document', '未提供角色设定')}

## 前文内容（用于衔接）
{context.get('previous_content', '这是第一章')[-1000:] if context.get('previous_content') else '这是第一章'}

请撰写完整的章节正文，字数控制在 2000-4000 字。"""

        # 调用 LLM
        response = await self._call_llm(
            system_prompt=WRITER_PROMPT,
            user_prompt=user_prompt,
            temperature=0.8,  # 写作需要更多创造性
            max_tokens=4000
        )

        # 计算字数
        word_count = len(response)

        result = {
            "content": response,
            "word_count": word_count,
            "chapter_id": outline.get("chapter_id", "unknown"),
            "title": outline.get("title", "未命名章节")
        }

        self._log_execution("章节撰写完成", {"word_count": word_count})

        return result
