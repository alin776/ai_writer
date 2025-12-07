"""大纲师 Agent

负责生成章节大纲，包括：
- 核心冲突
- 涉及角色
- 情绪曲线
- 伏笔设置
"""

from typing import Dict, Any
from app.services.agent.model_selector import TaskType
from .base_agent import BaseAgent
from ..prompts import OUTLINE_PROMPT
from ..character_extractor import extract_characters_from_text

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
            context: 上下文（total_outline, character_document, previous_summary, analysis_result, previous_content, chapters_info）

        Returns:
            大纲结构
        """
        self._log_execution("开始生成章节大纲", {"task": task.get("description", "")[:50]})

        # ✅ 意图路由优化：支持多种上下文来源
        # 优先级：analysis_result > previous_summary > previous_content
        analysis_content = context.get('analysis_result', '') or context.get('previous_summary', '')

        # ✅ 新增：如果没有分析结果但有前文内容，提示大纲师需要先分析
        previous_content = context.get('previous_content', '')
        chapters_info = context.get('chapters_info', {})
        target_chapter = chapters_info.get('target_chapter', 0)
        chapter_titles = chapters_info.get('chapter_titles', [])

        # 决定分析来源
        need_analyze_content = not analysis_content and previous_content
        if need_analyze_content:
            logger.info(f"[大纲师] 无现成分析结果，将直接分析前文内容（{len(previous_content)}字）")
            # 使用前文内容作为分析基础
            analysis_source = previous_content[:8000]  # 限制长度，避免 token 过多
        else:
            analysis_source = analysis_content

        # ✅ 重构：使用公共模块提取角色（基于特征过滤，而非硬编码跳过词）
        key_characters = extract_characters_from_text(analysis_source, max_count=5)
        if key_characters:
            logger.info(f"[大纲师] 从分析中提取关键角色: {key_characters}")

        # 构建章节信息提示
        chapter_context = ""
        if target_chapter:
            chapter_context = f"目标：续写第{target_chapter}章"
            if chapter_titles:
                chapter_context += f"\n前文章节：{', '.join(chapter_titles)}"

        # 构建用户提示（增强版：支持直接分析前文）
        if need_analyze_content:
            user_prompt = f"""请为以下写作任务生成章节大纲：

## 任务描述
{task.get('description', '未提供任务描述')}

## {chapter_context if chapter_context else '章节信息'}

## 【核心】前文内容（请先分析，再基于分析结果设计大纲）
{analysis_source}

## 总体大纲
{context.get('total_outline', '未提供总大纲')}

## 角色设定
{context.get('character_document', '未提供角色设定')}

{"## 关键角色约束（新章节必须包含以下角色）" + chr(10) + chr(10).join(f"- {c}" for c in key_characters) if key_characters else ""}

【重要提醒】
1. 请先分析前文内容，识别：主要角色、当前剧情进展、未解决的伏笔
2. 基于分析结果设计新章节大纲
3. 新章节必须承接前文的角色和故事线，不得引入无关内容
4. 章节标题应体现与前文的连贯性

请生成详细的章节大纲。"""
        else:
            user_prompt = f"""请为以下写作任务生成章节大纲：

## 任务描述
{task.get('description', '未提供任务描述')}

## {chapter_context if chapter_context else '章节信息'}

## 【重要】前文分析结果（必须严格基于此内容续写）
{analysis_source if analysis_source else '未提供前文分析，请根据任务描述自行构思'}

## 总体大纲
{context.get('total_outline', '未提供总大纲')}

## 角色设定
{context.get('character_document', '未提供角色设定')}

## 前文摘要
{context.get('previous_summary', '这是第一章，无前文')}

## 章节ID
{task.get('chapter_id', 'unknown')}

{"## 关键角色约束（新章节必须包含以下角色）" + chr(10) + chr(10).join(f"- {c}" for c in key_characters) if key_characters else ""}

【重要提醒】
1. 新章节的角色、世界观、故事线必须与前文分析保持一致
2. 不得引入前文未出现的新角色或完全不相关的剧情
3. 章节标题和内容必须承接前文的故事发展

请生成详细的章节大纲。"""

        # 调用 LLM
        response = await self._call_llm(
            system_prompt=OUTLINE_PROMPT,
            user_prompt=user_prompt,
            temperature=0.5,  # 大纲生成需要更稳定
            max_tokens=2000,
            task_type=TaskType.STORY_PLANNING
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
            "connection_to_previous": result.get("connection_to_previous", ""),
            "key_characters_from_analysis": key_characters  # ✅ 保存提取的关键角色
        }

        self._log_execution("章节大纲生成完成", {"title": outline["title"]})

        return outline
