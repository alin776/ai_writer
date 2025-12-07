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
from .character_extractor import (
    extract_characters_from_text,
    check_character_presence
)
from .mode_selector import ModeSelector
from ..timeout_config import TimeoutConfig

logger = logging.getLogger(__name__)


# Multi-Agent 阶段定义（避免硬编码）
MULTI_AGENT_STAGES = {
    1: {"name": "大纲师", "description": "生成章节大纲", "action": "正在分析任务..."},
    2: {"name": "主笔", "description": "撰写章节内容", "action": "正在撰写内容..."},
    3: {"name": "角色守护", "description": "检查角色一致性", "action": "正在检查..."},
    4: {"name": "逻辑审计", "description": "检查逻辑合理性", "action": "正在检查..."},
    5: {"name": "总编", "description": "综合审核与修订", "action": "正在审核..."},
}

TOTAL_STAGES = len(MULTI_AGENT_STAGES)


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

    def __init__(self, ai_service, memory_manager=None):
        """初始化执行器

        Args:
            ai_service: HTTPAIService 实例
            memory_manager: 记忆管理器（可选）
        """
        self.ai_service = ai_service
        self.memory_manager = memory_manager

        # 初始化模式选择器
        self.mode_selector = ModeSelector()

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
        """执行写作任务（带动态模式选择）

        Args:
            task: 任务信息
            work_id: 作品 ID
            chapter_id: 章节 ID
            context: 上下文（character_document, previous_summary, total_outline 等）
            on_event: 事件回调（发送 Planning 格式事件）

        Returns:
            执行结果
        """
        # 1. 选择执行模式
        mode = self.mode_selector.select(task, context)
        mode_config = self.mode_selector.get_config(mode)

        logger.info(
            f"[MultiAgent] 模式: {mode} ({mode_config['description']}), "
            f"任务: {task.get('description', '')[:30]}"
        )

        # 2. 按模式执行（带超时保护）
        try:
            if mode == "lite":
                return await asyncio.wait_for(
                    self._execute_lite(task, context, on_event, mode_config),
                    timeout=TimeoutConfig.MULTI_AGENT_TOTAL // 3  # lite 模式超时更短
                )
            elif mode == "standard":
                return await asyncio.wait_for(
                    self._execute_standard(task, work_id, context, on_event, mode_config),
                    timeout=TimeoutConfig.MULTI_AGENT_TOTAL * 2 // 3
                )
            else:  # full
                return await asyncio.wait_for(
                    self._execute_internal(task, work_id, chapter_id, context, on_event),
                    timeout=TimeoutConfig.MULTI_AGENT_TOTAL
                )
        except asyncio.TimeoutError:
            logger.error(f"[MultiAgent] 执行超时 (mode={mode})")
            raise TimeoutError(f"Multi-Agent 写作流程超时 (mode={mode})")

    async def _execute_lite(
        self,
        task: Dict[str, Any],
        context: Dict[str, Any],
        on_event: Optional[Callable[[Dict], Awaitable[None]]],
        config: Dict
    ) -> Dict[str, Any]:
        """Lite 模式执行：大纲(可选) + 主笔

        适用于短内容、简单任务（< 500 字）
        """
        # 发送计划（1-2 阶段）
        await self._send_plan_event_for_mode(on_event, config["stages"])

        # 阶段1: 大纲（可选）
        outline = None
        if 1 in config["stages"]:
            if self._needs_outline(task):
                await self._report_event(on_event, "task_start", 1, "快速构思中...")
                start_time = time.time()
                try:
                    outline = await asyncio.wait_for(
                        self.outline_agent.generate(task, context),
                        timeout=TimeoutConfig.get_stage_timeout("outline") // 2
                    )
                except (asyncio.TimeoutError, Exception) as e:
                    logger.warning(f"[MultiAgent-Lite] 大纲生成失败: {e}")
                    outline = self._default_outline(task, context)
                await self._report_event(on_event, "task_done", 1, elapsed_time=time.time() - start_time)
            else:
                # 跳过大纲
                await self._report_event(on_event, "task_start", 1, "跳过大纲")
                await self._report_event(on_event, "task_done", 1, elapsed_time=0)
                outline = {"structure": "直接写作", "key_points": []}

        # 阶段2: 主笔
        await self._report_event(on_event, "task_start", 2, "撰写中...")
        start_time = time.time()
        # ✅ 添加超时保护
        try:
            draft = await asyncio.wait_for(
                self.writer_agent.write(outline or {}, context),
                timeout=TimeoutConfig.get_stage_timeout("writing")
            )
        except asyncio.TimeoutError:
            logger.error("[MultiAgent-Lite] 主笔写作超时")
            raise TimeoutError("Lite 模式写作超时")
        writer_time = time.time() - start_time
        await self._report_event(on_event, "task_done", 2, elapsed_time=writer_time)

        # 发送内容
        await self._send_content_event(on_event, draft.get("content", ""))

        return {
            "content": draft.get("content", ""),
            "word_count": draft.get("word_count", 0),
            "mode": "lite",
            "quality_score": min(0.80, config["max_quality_score"]),
            "stages_executed": config["stages"],
            "outline": outline,
            "draft": draft,
        }

    async def _execute_standard(
        self,
        task: Dict[str, Any],
        work_id: str,
        context: Dict[str, Any],
        on_event: Optional[Callable[[Dict], Awaitable[None]]],
        config: Dict
    ) -> Dict[str, Any]:
        """Standard 模式执行：大纲 + 主笔 + 并行审查（不修订）

        适用于中等内容（500-1500 字）
        """
        # 发送计划（4 阶段）
        await self._send_plan_event_for_mode(on_event, config["stages"])

        # 阶段1: 大纲
        await self._report_event(on_event, "task_start", 1, "规划结构中...")
        start_time = time.time()
        try:
            outline = await asyncio.wait_for(
                self.outline_agent.generate(task, context),
                timeout=TimeoutConfig.get_stage_timeout("outline")
            )
        except (asyncio.TimeoutError, Exception) as e:
            logger.warning(f"[MultiAgent-Standard] 大纲生成失败: {e}")
            outline = self._default_outline(task, context)
        await self._report_event(on_event, "task_done", 1, elapsed_time=time.time() - start_time)

        # 传递角色信息
        key_characters = outline.get("key_characters", [])
        if key_characters:
            context["analysis_result"] = f"主要角色：{'、'.join(key_characters)}"

        # 阶段2: 主笔
        await self._report_event(on_event, "task_start", 2, "撰写中...")
        start_time = time.time()
        draft = await asyncio.wait_for(
            self.writer_agent.write(outline, context),
            timeout=TimeoutConfig.get_stage_timeout("writing")
        )
        await self._report_event(on_event, "task_done", 2, elapsed_time=time.time() - start_time)

        # 阶段3&4: 并行审查
        await self._report_event(on_event, "task_start", 3, "检查角色...")
        await self._report_event(on_event, "task_start", 4, "检查逻辑...")
        start_time = time.time()

        try:
            results = await asyncio.wait_for(
                asyncio.gather(
                    self.character_guard.check(draft, work_id, context),
                    self.logic_auditor.check(draft, work_id, context),
                    return_exceptions=True
                ),
                timeout=TimeoutConfig.get_check_timeout()
            )

            character_review = results[0] if not isinstance(results[0], Exception) else self._default_pass_review("角色检查跳过")
            logic_review = results[1] if not isinstance(results[1], Exception) else self._default_pass_review("逻辑检查跳过")
        except asyncio.TimeoutError:
            character_review = self._default_pass_review("审查超时")
            logic_review = self._default_pass_review("审查超时")

        check_time = time.time() - start_time
        await self._report_event(on_event, "task_done", 3, elapsed_time=check_time)
        await self._report_event(on_event, "task_done", 4, elapsed_time=check_time)

        # 提取警告（不修订）
        warnings = self._extract_warnings([character_review, logic_review])

        # 发送内容
        await self._send_content_event(on_event, draft.get("content", ""))

        return {
            "content": draft.get("content", ""),
            "word_count": draft.get("word_count", 0),
            "mode": "standard",
            "quality_score": min(0.85, config["max_quality_score"]),
            "stages_executed": config["stages"],
            "outline": outline,
            "draft": draft,
            "character_review": character_review,
            "logic_review": logic_review,
            "warnings": warnings,
        }

    def _needs_outline(self, task: Dict) -> bool:
        """判断是否需要大纲"""
        task_type = self.mode_selector._infer_task_type(task.get("description", ""))
        if task_type in ["polish", "expand"]:
            return False

        target_words = self.mode_selector._get_target_words(task)
        if target_words and target_words < 300:
            return False

        return True

    def _extract_warnings(self, results: list) -> list:
        """从审查结果提取警告"""
        warnings = []
        for result in results:
            if isinstance(result, dict) and result.get("status") not in ["PASS", "SKIPPED"]:
                issues = result.get("issues", [])
                for issue in issues[:3]:
                    if isinstance(issue, dict):
                        warnings.append(issue.get("description", str(issue)))
                    else:
                        warnings.append(str(issue))
        return warnings

    async def _send_plan_event_for_mode(
        self,
        callback: Optional[Callable[[Dict], Awaitable[None]]],
        stages: list
    ):
        """根据模式发送计划事件"""
        if callback:
            tasks = []
            for stage_id in stages:
                if stage_id in MULTI_AGENT_STAGES:
                    stage = MULTI_AGENT_STAGES[stage_id]
                    tasks.append({
                        "task_id": stage_id,
                        "description": f"{stage['name']}：{stage['description']}"
                    })

            plan = {
                "type": "plan",
                "data": {"tasks": tasks}
            }
            await callback(plan)

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
            await self._report_event(on_event, "task_start", 1, f"{MULTI_AGENT_STAGES[1]['name']}{MULTI_AGENT_STAGES[1]['action']}")
            start_time = time.time()

            try:
                outline = await asyncio.wait_for(
                    self.outline_agent.generate(task, context),
                    timeout=TimeoutConfig.get_stage_timeout("outline")
                )
            except asyncio.TimeoutError:
                timeout_val = TimeoutConfig.get_stage_timeout("outline")
                logger.warning(f"[MultiAgent] 大纲生成超时（>{timeout_val}s），使用默认大纲")
                outline = self._default_outline(task, context)
            except Exception as e:
                logger.warning(f"[MultiAgent] 大纲生成失败（{type(e).__name__}: {e}），使用默认大纲")
                outline = self._default_outline(task, context)

            outline_time = time.time() - start_time
            await self._report_event(on_event, "task_done", 1, elapsed_time=outline_time)
            logger.info(f"[MultiAgent] 大纲生成完成: {outline.get('title', '')} ({outline_time:.1f}s)")

            # ✅ 修复：把大纲中提取的角色加入 context，传递给角色守护
            key_characters = outline.get("key_characters", [])
            if key_characters:
                # 构建分析结果字符串，让角色守护能够从中提取角色
                context["analysis_result"] = f"主要角色：{'、'.join(key_characters)}"
                logger.info(f"[MultiAgent] 传递关键角色到角色守护: {key_characters}")

            # 阶段2: 主笔（不可回退 - 核心步骤）
            await self._report_event(on_event, "task_start", 2, f"{MULTI_AGENT_STAGES[2]['name']}{MULTI_AGENT_STAGES[2]['action']}")
            start_time = time.time()

            draft = await asyncio.wait_for(
                self.writer_agent.write(outline, context),
                timeout=TimeoutConfig.get_stage_timeout("writing")
            )

            writer_time = time.time() - start_time
            await self._report_event(on_event, "task_done", 2, elapsed_time=writer_time)
            logger.info(f"[MultiAgent] 初稿完成: {draft.get('word_count', 0)} 字 ({writer_time:.1f}s)")

            # 阶段3&4: 角色守护 + 逻辑审计（并行执行，可回退）
            await self._report_event(on_event, "task_start", 3, f"{MULTI_AGENT_STAGES[3]['name']}{MULTI_AGENT_STAGES[3]['action']}")
            await self._report_event(on_event, "task_start", 4, f"{MULTI_AGENT_STAGES[4]['name']}{MULTI_AGENT_STAGES[4]['action']}")
            start_time = time.time()

            # 使用 return_exceptions=True 允许部分失败
            check_timeout = TimeoutConfig.get_check_timeout()

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
                logger.warning("[MultiAgent] 校验阶段超时，执行快速降级检查")
                # ✅ P3修复：超时时进行简单的关键词匹配检查，防止完全跑题
                character_review = await self._fallback_character_check(draft, context)
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
            await self._report_event(on_event, "task_start", 5, f"{MULTI_AGENT_STAGES[5]['name']}{MULTI_AGENT_STAGES[5]['action']}")
            start_time = time.time()

            if self._needs_revision(character_review, logic_review):
                try:
                    final = await asyncio.wait_for(
                        self.editor_agent.revise(draft, character_review, logic_review, context),
                        timeout=TimeoutConfig.get_stage_timeout("editor")
                    )
                    editor_time = time.time() - start_time
                    logger.info(f"[MultiAgent] 总编修订完成 ({editor_time:.1f}s)")
                except asyncio.TimeoutError:
                    timeout_val = TimeoutConfig.get_stage_timeout("editor")
                    logger.warning(f"[MultiAgent] 总编修订超时（>{timeout_val}s），使用初稿")
                    final = {
                        "content": draft.get("content", ""),
                        "word_count": draft.get("word_count", 0),
                        "quality_score": 0.75,  # 降低评分表示未经修订
                        "revision_summary": f"修订超时（>{timeout_val}s），使用初稿",
                        "conflicts_resolved": []
                    }
                    editor_time = time.time() - start_time
                except Exception as e:
                    logger.warning(f"[MultiAgent] 总编修订失败（{type(e).__name__}: {e}），使用初稿")
                    final = {
                        "content": draft.get("content", ""),
                        "word_count": draft.get("word_count", 0),
                        "quality_score": 0.75,  # 降低评分表示未经修订
                        "revision_summary": f"修订失败（{type(e).__name__}），使用初稿",
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
                "mode": "full",  # ✅ 添加 mode 字段保持一致性
                "quality_score": final.get("quality_score", 0.85),
                "stages_executed": [1, 2, 3, 4, 5],  # ✅ 添加 stages_executed 字段
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

    def _default_outline(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """默认大纲模板（回退用，携带可用上下文避免跑题）"""
        # ✅ 修复：从前文内容中提取角色（而不是期望 character_document 是列表）
        previous_content = context.get("previous_content", "")
        extracted_chars = []
        if previous_content:
            extracted_chars = extract_characters_from_text(previous_content, max_count=5)
            logger.info(f"[MultiAgent] 默认大纲从前文提取角色: {extracted_chars}")

        return {
            "chapter_id": task.get("chapter_id", "unknown"),
            "title": task.get("description", "未命名章节")[:20],
            "core_conflict": context.get("previous_summary", "承接前文剧情"),
            "characters": extracted_chars,  # ✅ 使用提取的角色列表
            "emotion_curve": {"start": "平静", "mid": "高潮", "end": "收尾"},
            "foreshadowing": context.get("world_setting", ""),
            "connection_to_previous": context.get("previous_summary", ""),
            "key_characters": extracted_chars  # ✅ 新增：显式传递关键角色
        }

    def _default_pass_review(self, reason: str = "校验已跳过") -> Dict[str, Any]:
        """默认通过的检查结果（回退用）"""
        return {
            "status": "SKIPPED",
            "issues": [],
            "summary": reason
        }

    async def _fallback_character_check(
        self,
        draft: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """✅ P3修复：快速降级检查（超时时使用）

        不调用 LLM，仅通过特征过滤检查内容是否跑题。
        ✅ 重构：使用公共模块 character_extractor 进行角色提取

        Args:
            draft: 初稿内容
            context: 上下文

        Returns:
            检查结果
        """
        content = draft.get("content", "")
        analysis = context.get("analysis_result", "") or context.get("previous_summary", "")

        if not analysis:
            return self._default_pass_review("无分析结果，跳过降级检查")

        # ✅ 重构：使用公共模块提取角色（基于特征过滤）
        key_characters = extract_characters_from_text(analysis, max_count=8)

        if not key_characters:
            return self._default_pass_review("无法提取关键角色，跳过降级检查")

        # ✅ 重构：使用公共模块检查角色出现情况
        presence = check_character_presence(content, key_characters)

        logger.info(
            f"[MultiAgent] 降级检查: 角色匹配 {presence['match_count']}/{presence['total']} "
            f"({presence['match_ratio']:.0%}), found={presence['found']}"
        )

        if presence["is_off_topic"]:
            # 严重跑题
            return {
                "status": "NEED_REVISION",
                "issues": [
                    {
                        "type": "content_drift",
                        "severity": "high",
                        "description": f"内容跑题：前文角色 {key_characters[:5]} 在新内容中几乎未出现",
                        "suggestion": "请重新生成，确保延续前文角色和故事线"
                    }
                ],
                "summary": f"降级检查发现内容跑题（角色匹配率 {presence['match_ratio']:.0%}）"
            }
        else:
            return {
                "status": "PASS",
                "issues": [],
                "summary": f"降级检查通过（角色匹配率 {presence['match_ratio']:.0%}）"
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
                        {
                            "task_id": task_id,
                            "description": f"{stage['name']}：{stage['description']}"
                        }
                        for task_id, stage in MULTI_AGENT_STAGES.items()
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
