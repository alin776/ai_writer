"""Multi-Agent 执行器

协调 5 个 Agent 完成写作任务：
大纲师 → 主笔 → 角色守护 + 逻辑审计（并行） → 总编
"""

import asyncio
import logging
import time
from typing import Dict, Any, Optional, Callable, Awaitable, Set

from .agents import (
    OutlineAgent,
    WriterAgent,
    CharacterGuard,
    LogicAuditor,
    EditorAgent
)

logger = logging.getLogger(__name__)


class MultiAgentExecutor:
    """写作任务的 Multi-Agent 执行器

    流程：
    1. 大纲师：生成章节大纲
    2. 主笔：根据大纲撰写内容
    3. 角色守护 + 逻辑审计：并行检查（提高效率）
    4. 总编：根据检查结果进行修订（如需要）

    事件回调：
    - 发送 Planning 格式的事件（task_start, task_done, content）
    - 与前端 TaskListPanel 组件兼容
    """

    # 写作类任务类型
    WRITING_TASK_TYPES: Set[str] = {
        "write_chapter",
        "continue_writing",
        "expand_content",
        "rewrite_content",
        "write_content",
    }

    # 写作关键词（用于模糊匹配）
    WRITING_KEYWORDS: Set[str] = {
        "写", "续写", "扩写", "重写", "创作", "生成内容", "章节"
    }

    # 超时配置（秒）
    STAGE_TIMEOUTS: Dict[str, int] = {
        "outline": 30,       # 大纲师
        "writing": 120,      # 主笔（生成长文本，需要较长时间）
        "character_guard": 30,  # 角色守护
        "logic_auditor": 30,    # 逻辑审计
        "editor": 60,        # 总编
    }
    TOTAL_TIMEOUT = 300      # 整体超时 5 分钟

    def __init__(self, ai_service, memory_manager=None):
        """初始化执行器

        Args:
            ai_service: HTTPAIService 实例
            memory_manager: 记忆管理器（可选）
        """
        self.ai_service = ai_service
        self.memory_manager = memory_manager

        # 初始化各 Agent
        self.outline_agent = OutlineAgent(ai_service)
        self.writer_agent = WriterAgent(ai_service)
        self.character_guard = CharacterGuard(ai_service)
        self.logic_auditor = LogicAuditor(ai_service)
        self.editor_agent = EditorAgent(ai_service)

        logger.info("[MultiAgent] 执行器初始化完成")

    def is_writing_task(self, task: Dict[str, Any]) -> bool:
        """判断是否是写作类任务

        Args:
            task: 任务信息

        Returns:
            是否是写作任务
        """
        task_type = task.get("type", "").lower()
        task_tool = task.get("tool", "").lower()
        description = task.get("description", "").lower()

        # 检查任务类型
        if task_type in self.WRITING_TASK_TYPES:
            return True

        # 检查工具名称
        if any(keyword in task_tool for keyword in ["write", "content", "chapter"]):
            return True

        # 检查描述中的关键词
        if any(kw in description for kw in self.WRITING_KEYWORDS):
            return True

        return False

    async def execute(
        self,
        task: Dict[str, Any],
        work_id: str,
        chapter_id: str,
        context: Dict[str, Any],
        on_event: Optional[Callable[[Dict], Awaitable[None]]] = None
    ) -> Dict[str, Any]:
        """执行写作任务的完整 Multi-Agent 流程（带超时保护）

        Args:
            task: 任务信息
            work_id: 作品 ID
            chapter_id: 章节 ID
            context: 上下文（character_document, previous_summary, total_outline 等）
            on_event: 事件回调（发送 Planning 格式事件）

        Returns:
            执行结果
        """
        logger.info(f"[MultiAgent] 开始执行写作任务: {task.get('description', '')[:50]}")

        try:
            # 整体超时保护
            return await asyncio.wait_for(
                self._execute_internal(task, work_id, chapter_id, context, on_event),
                timeout=self.TOTAL_TIMEOUT
            )
        except asyncio.TimeoutError:
            logger.error(f"[MultiAgent] 整体执行超时（>{self.TOTAL_TIMEOUT}s）")
            raise TimeoutError(f"Multi-Agent 写作流程超时，请稍后重试")

    async def _execute_internal(
        self,
        task: Dict[str, Any],
        work_id: str,
        chapter_id: str,
        context: Dict[str, Any],
        on_event: Optional[Callable[[Dict], Awaitable[None]]] = None
    ) -> Dict[str, Any]:
        """内部执行逻辑（带回退机制）"""

        # 发送初始计划（5 个阶段）
        await self._send_plan_event(on_event)

        try:
            # 阶段1: 大纲师（可回退）
            await self._report_event(on_event, "task_start", 1, "大纲师正在分析任务...")
            start_time = time.time()

            try:
                outline = await asyncio.wait_for(
                    self.outline_agent.generate(task, context),
                    timeout=self.STAGE_TIMEOUTS["outline"]
                )
            except (asyncio.TimeoutError, Exception) as e:
                logger.warning(f"[MultiAgent] 大纲生成失败，使用默认大纲: {e}")
                outline = self._default_outline(task)

            outline_time = time.time() - start_time
            await self._report_event(on_event, "task_done", 1, elapsed_time=outline_time)
            logger.info(f"[MultiAgent] 大纲生成完成: {outline.get('title', '')} ({outline_time:.1f}s)")

            # 阶段2: 主笔（不可回退 - 核心步骤）
            await self._report_event(on_event, "task_start", 2, "主笔正在撰写内容...")
            start_time = time.time()

            draft = await asyncio.wait_for(
                self.writer_agent.write(outline, context),
                timeout=self.STAGE_TIMEOUTS["writing"]
            )

            writer_time = time.time() - start_time
            await self._report_event(on_event, "task_done", 2, elapsed_time=writer_time)
            logger.info(f"[MultiAgent] 初稿完成: {draft.get('word_count', 0)} 字 ({writer_time:.1f}s)")

            # 阶段3&4: 角色守护 + 逻辑审计（并行执行，可回退）
            await self._report_event(on_event, "task_start", 3, "角色守护正在检查...")
            await self._report_event(on_event, "task_start", 4, "逻辑审计正在检查...")
            start_time = time.time()

            # 使用 return_exceptions=True 允许部分失败
            check_timeout = max(
                self.STAGE_TIMEOUTS["character_guard"],
                self.STAGE_TIMEOUTS["logic_auditor"]
            )

            try:
                results = await asyncio.wait_for(
                    asyncio.gather(
                        self.character_guard.check(draft, work_id, context),
                        self.logic_auditor.check(draft, work_id, context),
                        return_exceptions=True
                    ),
                    timeout=check_timeout
                )

                # 处理可能的异常结果
                if isinstance(results[0], Exception):
                    logger.warning(f"[MultiAgent] 角色守护失败，跳过: {results[0]}")
                    character_review = self._default_pass_review(f"角色守护失败: {results[0]}")
                else:
                    character_review = results[0]

                if isinstance(results[1], Exception):
                    logger.warning(f"[MultiAgent] 逻辑审计失败，跳过: {results[1]}")
                    logic_review = self._default_pass_review(f"逻辑审计失败: {results[1]}")
                else:
                    logic_review = results[1]

            except asyncio.TimeoutError:
                logger.warning("[MultiAgent] 校验阶段超时，跳过校验")
                character_review = self._default_pass_review("角色守护超时，已跳过")
                logic_review = self._default_pass_review("逻辑审计超时，已跳过")

            check_time = time.time() - start_time
            await self._report_event(on_event, "task_done", 3, elapsed_time=check_time)
            await self._report_event(on_event, "task_done", 4, elapsed_time=check_time)

            logger.info(
                f"[MultiAgent] 校验完成: "
                f"角色={character_review.get('status')}, "
                f"逻辑={logic_review.get('status')} ({check_time:.1f}s)"
            )

            # 阶段5: 总编裁决（可回退）
            await self._report_event(on_event, "task_start", 5, "总编正在审核...")
            start_time = time.time()

            if self._needs_revision(character_review, logic_review):
                try:
                    final = await asyncio.wait_for(
                        self.editor_agent.revise(draft, character_review, logic_review, context),
                        timeout=self.STAGE_TIMEOUTS["editor"]
                    )
                    editor_time = time.time() - start_time
                    logger.info(f"[MultiAgent] 总编修订完成 ({editor_time:.1f}s)")
                except (asyncio.TimeoutError, Exception) as e:
                    logger.warning(f"[MultiAgent] 总编修订失败，使用初稿: {e}")
                    final = {
                        "content": draft.get("content", ""),
                        "word_count": draft.get("word_count", 0),
                        "quality_score": 0.75,  # 降低评分表示未经修订
                        "revision_summary": f"修订失败，使用初稿: {str(e)[:50]}",
                        "conflicts_resolved": []
                    }
                    editor_time = time.time() - start_time
            else:
                # 无需修订，直接使用初稿
                final = {
                    "content": draft.get("content", ""),
                    "word_count": draft.get("word_count", 0),
                    "quality_score": 0.85,
                    "revision_summary": "无需修订",
                    "conflicts_resolved": []
                }
                editor_time = time.time() - start_time
                logger.info(f"[MultiAgent] 无需修订，使用初稿 ({editor_time:.1f}s)")

            await self._report_event(on_event, "task_done", 5, elapsed_time=editor_time)

            # 发送最终内容
            await self._send_content_event(on_event, final.get("content", ""))

            return {
                "content": final.get("content", ""),
                "word_count": final.get("word_count", 0),
                "quality_score": final.get("quality_score", 0.85),
                "outline": outline,
                "draft": draft,
                "character_review": character_review,
                "logic_review": logic_review,
                "revision_summary": final.get("revision_summary"),
                "conflicts_resolved": final.get("conflicts_resolved", [])
            }

        except Exception as e:
            logger.error(f"[MultiAgent] 执行失败: {e}", exc_info=True)
            raise

    def _default_outline(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """默认大纲模板（回退用）"""
        return {
            "chapter_id": task.get("chapter_id", "unknown"),
            "title": task.get("description", "未命名章节")[:20],
            "core_conflict": "待定",
            "characters": [],
            "emotion_curve": {"start": "平静", "mid": "高潮", "end": "收尾"},
            "foreshadowing": "",
            "connection_to_previous": ""
        }

    def _default_pass_review(self, reason: str = "校验已跳过") -> Dict[str, Any]:
        """默认通过的检查结果（回退用）"""
        return {
            "status": "SKIPPED",
            "issues": [],
            "summary": reason
        }

    def _needs_revision(
        self,
        character_review: Dict[str, Any],
        logic_review: Dict[str, Any]
    ) -> bool:
        """判断是否需要修订

        Args:
            character_review: 角色检查结果
            logic_review: 逻辑检查结果

        Returns:
            是否需要修订
        """
        return (
            character_review.get("status") == "NEED_REVISION" or
            logic_review.get("status") == "NEED_REVISION"
        )

    async def _send_plan_event(
        self,
        callback: Optional[Callable[[Dict], Awaitable[None]]]
    ):
        """发送计划事件

        发送 5 个阶段的任务列表，与前端 TaskListPanel 兼容
        """
        if callback:
            plan = {
                "type": "plan",
                "data": {
                    "tasks": [
                        {"task_id": 1, "description": "大纲师：生成章节大纲"},
                        {"task_id": 2, "description": "主笔：撰写章节内容"},
                        {"task_id": 3, "description": "角色守护：检查角色一致性"},
                        {"task_id": 4, "description": "逻辑审计：检查逻辑合理性"},
                        {"task_id": 5, "description": "总编：综合审核与修订"},
                    ]
                }
            }
            await callback(plan)

    async def _report_event(
        self,
        callback: Optional[Callable[[Dict], Awaitable[None]]],
        event_type: str,
        task_id: int,
        description: str = "",
        elapsed_time: float = 0
    ):
        """报告任务事件

        Args:
            callback: 事件回调
            event_type: 事件类型（task_start, task_done）
            task_id: 任务 ID（1-5）
            description: 描述（task_start 时使用）
            elapsed_time: 耗时（task_done 时使用）
        """
        if callback:
            if event_type == "task_start":
                event = {
                    "type": "task_start",
                    "data": {
                        "task_id": task_id,
                        "description": description
                    }
                }
            elif event_type == "task_done":
                event = {
                    "type": "task_done",
                    "data": {
                        "task_id": task_id,
                        "elapsed_time": elapsed_time
                    }
                }
            else:
                return

            await callback(event)

    async def _send_content_event(
        self,
        callback: Optional[Callable[[Dict], Awaitable[None]]],
        content: str
    ):
        """发送内容事件

        Args:
            callback: 事件回调
            content: 生成的内容
        """
        if callback:
            event = {
                "type": "content",
                "data": {
                    "content": content
                }
            }
            await callback(event)
