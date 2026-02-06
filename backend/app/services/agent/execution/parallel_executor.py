"""
并行执行器模块 - 智能并行执行任务

从 langgraph_agent.py 的 _execute_tasks_in_parallel 方法中拆分。
负责任务分组、并行执行、重试和结果收集。
"""

import asyncio
import json
import logging
import time
from typing import List, Dict, Any, Optional, Set, TYPE_CHECKING

if TYPE_CHECKING:
    from app.services.agent.langgraph_agent import WritingAgentGraph

logger = logging.getLogger(__name__)


# 可以并行执行的独立数据获取工具
PARALLEL_SAFE_TOOLS = {
    "get_context_tool",
    "read_chapter_tool",
    "get_chapter_by_order_tool",
    "search_analysis_fragments_tool",
    "search_content",
    "analyze_text_tool",  # 允许并行（无参数依赖时）
    "analyze_content"
}


class ParallelExecutor:
    """并行执行器 - 智能并行执行任务"""

    # 并发控制
    MAX_CONCURRENCY = 5

    # 重试配置
    MAX_RETRIES = 2
    RETRYABLE_KEYWORDS = ["timeout", "connection", "network", "网络", "连接", "超时"]

    def __init__(self, agent: "WritingAgentGraph"):
        """
        初始化并行执行器

        Args:
            agent: WritingAgentGraph 实例（用于调用 _execute_task 等方法）
        """
        self.agent = agent

    async def execute_tasks(
        self,
        tasks: List[Dict[str, Any]],
        work_id: str,
        chapter_id: str,
        context: str,
        context_payload: Optional[Dict[str, Any]] = None,
        on_task_start: Optional[callable] = None,
        on_task_progress: Optional[callable] = None,
        on_task_done: Optional[callable] = None,
        conversation_id: Optional[str] = None,  # v8.0: 添加 conversation_id 用于操作日志
        state: Optional[Dict[str, Any]] = None,  # 🆕 2026-01-12: 添加 state 用于章节缓存
        approval_callback: Optional[callable] = None,
    ) -> List[Dict[str, Any]]:
        """
        智能并行执行任务

        三层分组策略：
        - 第一层：完全独立的任务（可立即并行）
        - 第二层：只依赖第一层任务的分析任务（第一层完成后可并行）
        - 第三层：有复杂依赖链的任务（必须串行）

        Args:
            tasks: 任务列表
            work_id: 作品ID
            chapter_id: 章节ID
            context: 上下文
            context_payload: 结构化上下文（原始 request.context）
            on_task_start: 任务开始回调
            on_task_progress: 任务进度回调
            on_task_done: 任务完成回调
            conversation_id: 会话ID（用于操作日志记录）
            state: Agent 状态（用于章节缓存）

        Returns:
            任务结果列表
        """
        # 🆕 2026-01-12: 保存或创建共享 state 用于章节缓存
        shared_state = state if state else {
            "work_id": work_id,
            "chapter_id": chapter_id,
            "context": context_payload or {},
        }
        if isinstance(context_payload, dict) and "tool_policy" in context_payload:
            shared_state.setdefault("tool_policy", context_payload.get("tool_policy"))
        # 创建参数解析器
        from app.services.agent.parameter_resolver import ParameterResolver

        resolver = ParameterResolver(strict_mode=False)
        logger.info("[ParameterResolver] 参数解析器已启用")

        task_results, _ = await self._execute_with_dag(
            tasks=tasks,
            work_id=work_id,
            chapter_id=chapter_id,
            context=context,
            context_payload=context_payload,
            resolver=resolver,
            on_task_start=on_task_start,
            on_task_progress=on_task_progress,
            on_task_done=on_task_done,
            shared_state=shared_state,
            conversation_id=conversation_id,
            approval_callback=approval_callback,
        )

        task_results.sort(key=lambda x: x["task_id"])
        return task_results

    @staticmethod
    def _extract_target_chapter_id(explore_result: Dict[str, Any]) -> tuple[str, str]:
        if not isinstance(explore_result, dict):
            return "", ""
        locate_targets = explore_result.get("locate_targets")
        if isinstance(locate_targets, list):
            for item in locate_targets:
                if isinstance(item, dict) and item.get("chapter_id"):
                    return str(item.get("chapter_id")), "explore.locate_targets"
        evidences = explore_result.get("evidences")
        if isinstance(evidences, list):
            for item in evidences:
                if isinstance(item, dict) and item.get("chapter_id"):
                    return str(item.get("chapter_id")), "explore.evidences"
        chapters = explore_result.get("chapters")
        if isinstance(chapters, list) and len(chapters) == 1:
            entry = chapters[0]
            if isinstance(entry, dict) and entry.get("id"):
                return str(entry.get("id")), "explore.chapters"
        return "", ""

    async def _execute_with_dag(
        self,
        tasks: List[Dict[str, Any]],
        work_id: str,
        chapter_id: str,
        context: str,
        resolver,
        on_task_start: Optional[callable],
        on_task_progress: Optional[callable],
        on_task_done: Optional[callable],
        context_payload: Optional[Dict[str, Any]] = None,
        shared_state: Optional[Dict[str, Any]] = None,
        conversation_id: Optional[str] = None,
        approval_callback: Optional[callable] = None,
    ) -> tuple:
        """基于 depends_on 的就绪队列调度执行任务。"""
        tasks_by_id, deps_by_id, ordered_ids = self._build_dependency_graph(tasks)

        logger.info(
            f"[ParallelExecution] DAG 调度启用，任务数={len(ordered_ids)}, "
            f"有依赖任务={sum(1 for i in ordered_ids if deps_by_id.get(i))}"
        )

        task_results: List[Dict[str, Any]] = []
        all_context = context
        completed: Set[int] = set()
        pending: Set[int] = set(ordered_ids)

        semaphore = asyncio.Semaphore(self.MAX_CONCURRENCY)

        while pending:
            ready = [
                task_id for task_id in ordered_ids
                if task_id in pending and deps_by_id.get(task_id, set()).issubset(completed)
            ]

            if not ready:
                logger.warning("[ParallelExecution] 依赖循环或缺失，降级为按顺序执行剩余任务")
                ready = [task_id for task_id in ordered_ids if task_id in pending]

            parallel_ids = [
                task_id for task_id in ready
                if not deps_by_id.get(task_id)
                and tasks_by_id[task_id].get("tool") in PARALLEL_SAFE_TOOLS
            ]

            if parallel_ids:
                parallel_tasks = [tasks_by_id[task_id] for task_id in parallel_ids]
                results, all_context = await self._execute_parallel_batch(
                    tasks=parallel_tasks,
                    work_id=work_id,
                    chapter_id=chapter_id,
                    context=all_context,
                    context_payload=context_payload,
                    resolver=resolver,
                    semaphore=semaphore,
                    on_task_start=on_task_start,
                    on_task_progress=on_task_progress,
                    on_task_done=on_task_done,
                    batch_name="并行就绪",
                    shared_state=shared_state,
                    conversation_id=conversation_id,
                    approval_callback=approval_callback,
                )
                task_results.extend(results)
                for result in results:
                    task_id = result.get("task_id")
                    if isinstance(task_id, int):
                        completed.add(task_id)
                        pending.discard(task_id)
                continue

            # 依赖任务或非并行安全任务：按顺序串行执行
            task_id = ready[0]
            task = tasks_by_id[task_id]
            result = await self._execute_single_task_with_retry(
                task=task,
                work_id=work_id,
                chapter_id=chapter_id,
                context=all_context,
                context_payload=context_payload,
                resolver=resolver,
                on_task_start=on_task_start,
                on_task_progress=on_task_progress,
                on_task_done=on_task_done,
                batch_name="串行就绪",
                shared_state=shared_state,
                conversation_id=conversation_id,
                approval_callback=approval_callback,
            )
            task_results.append(result)
            all_context += f"\n任务{result['task_id']}结果：\n{result['result']}\n"
            completed.add(task_id)
            pending.discard(task_id)

        return task_results, all_context

    def _build_dependency_graph(
        self,
        tasks: List[Dict[str, Any]]
    ) -> tuple:
        """构建任务依赖关系图（显式 depends_on + 参数引用推断）。"""
        from app.services.agent.parameter_resolver import ParameterResolver

        tasks_by_id: Dict[int, Dict[str, Any]] = {}
        ordered_ids: List[int] = []
        seen: Set[int] = set()
        next_id = 1

        for idx, task in enumerate(tasks):
            raw_task_id = task.get("task_id")
            task_id: Optional[int]
            try:
                task_id = int(raw_task_id)
            except (TypeError, ValueError):
                task_id = None

            if not task_id or task_id in seen:
                task_id = next_id
                next_id += 1
                task["task_id"] = task_id

            seen.add(task_id)
            tasks_by_id[task_id] = task
            ordered_ids.append(task_id)
            next_id = max(next_id, task_id + 1)

        deps_by_id: Dict[int, Set[int]] = {}
        valid_ids = set(tasks_by_id.keys())

        for task_id in ordered_ids:
            task = tasks_by_id[task_id]
            explicit = self._normalize_dep_list(task.get("depends_on"))
            inferred = ParameterResolver.extract_dependencies(task.get("params", {}))
            deps = set(explicit).union(inferred)
            deps.discard(task_id)
            invalid = deps - valid_ids
            if invalid:
                logger.warning(f"[ParallelExecution] 任务{task_id}依赖不存在: {sorted(invalid)}")
            deps_by_id[task_id] = {dep for dep in deps if dep in valid_ids}

        return tasks_by_id, deps_by_id, ordered_ids

    @staticmethod
    def _normalize_dep_list(value: Any) -> List[int]:
        if value is None:
            return []
        if isinstance(value, (int, str)):
            try:
                return [int(value)]
            except (TypeError, ValueError):
                return []
        if isinstance(value, list):
            normalized = []
            for item in value:
                try:
                    normalized.append(int(item))
                except (TypeError, ValueError):
                    continue
            return normalized
        return []

    def _classify_tasks(
        self,
        tasks: List[Dict[str, Any]],
        resolver
    ) -> tuple:
        """
        分类任务到三个层级

        Args:
            tasks: 任务列表
            resolver: 参数解析器

        Returns:
            (parallel_tasks, parallel_dependent_tasks, sequential_tasks, first_layer_ids)
        """
        from app.services.agent.parameter_resolver import ParameterResolver

        parallel_tasks = []
        parallel_dependent_tasks = []
        sequential_tasks = []
        first_layer_ids: Set[str] = set()

        def _has_placeholder_dependency(params: Dict[str, Any]) -> bool:
            """检查参数中是否包含占位符"""
            try:
                params_str = json.dumps(params, ensure_ascii=False)
                return bool(ParameterResolver.PLACEHOLDER_PATTERN.search(params_str))
            except Exception as e:
                logger.warning(f"[参数依赖检测] 序列化参数失败: {e}")
                return False

        # 第一遍：识别第一层任务
        for task in tasks:
            tool_name = task.get("tool", "auto")
            has_dependency = _has_placeholder_dependency(task.get("params", {}))

            if tool_name in PARALLEL_SAFE_TOOLS and not has_dependency:
                parallel_tasks.append(task)
                first_layer_ids.add(task["task_id"])
                logger.debug(f"[任务分组] 任务{task['task_id']}({tool_name}) → 第一层并行")

        # 第二遍：识别第二层任务
        for task in tasks:
            if task in parallel_tasks:
                continue

            tool_name = task.get("tool", "auto")
            params = task.get("params", {})
            has_dependency = _has_placeholder_dependency(params)

            if has_dependency:
                deps = self.agent._extract_task_dependencies(params)
                only_depends_on_first_layer = all(
                    dep_id in first_layer_ids for dep_id in deps
                )

                if only_depends_on_first_layer and tool_name in {"analyze_text_tool", "summarization"}:
                    parallel_dependent_tasks.append(task)
                    logger.debug(f"[任务分组] 任务{task['task_id']}({tool_name}) → 第二层并行")
                else:
                    sequential_tasks.append(task)
                    logger.debug(f"[任务分组] 任务{task['task_id']}({tool_name}) → 串行（复杂依赖）")
            else:
                sequential_tasks.append(task)
                logger.debug(f"[任务分组] 任务{task['task_id']}({tool_name}) → 串行（工具不支持）")

        return parallel_tasks, parallel_dependent_tasks, sequential_tasks, first_layer_ids

    async def _execute_parallel_batch(
        self,
        tasks: List[Dict[str, Any]],
        work_id: str,
        chapter_id: str,
        context: str,
        resolver,
        semaphore: asyncio.Semaphore,
        on_task_start: Optional[callable],
        on_task_progress: Optional[callable],
        on_task_done: Optional[callable],
        batch_name: str,
        context_payload: Optional[Dict[str, Any]] = None,
        shared_state: Optional[Dict[str, Any]] = None,
        conversation_id: Optional[str] = None,
        approval_callback: Optional[callable] = None,
    ) -> tuple:
        """
        并行执行一批任务

        Args:
            tasks: 任务列表
            work_id: 作品ID
            chapter_id: 章节ID
            context: 上下文
            context_payload: 结构化上下文（原始 request.context）
            resolver: 参数解析器
            semaphore: 并发信号量
            on_task_start: 任务开始回调
            on_task_progress: 任务进度回调
            on_task_done: 任务完成回调
            batch_name: 批次名称（用于日志）

        Returns:
            (task_results, updated_context)
        """
        logger.info(f"[ParallelExecution] 开始{batch_name}并行执行{len(tasks)}个任务")

        async def execute_with_semaphore(task):
            async with semaphore:
                return await self._execute_single_task_with_retry(
                    task=task,
                    work_id=work_id,
                    chapter_id=chapter_id,
                    context=context,
                    context_payload=context_payload,
                    resolver=resolver,
                    on_task_start=on_task_start,
                    on_task_progress=on_task_progress,
                    on_task_done=on_task_done,
                    batch_name=batch_name,
                    shared_state=shared_state,
                    conversation_id=conversation_id,
                    approval_callback=approval_callback,
                )

        # 并行执行
        parallel_results = await asyncio.gather(
            *[execute_with_semaphore(task) for task in tasks],
            return_exceptions=True
        )

        # 处理结果
        task_results = []
        all_context = context

        for i, result in enumerate(parallel_results):
            if isinstance(result, Exception):
                logger.error(f"[ParallelExecution] {batch_name}并行任务失败: {result}")
                failed_task = {
                    "task_id": tasks[i]["task_id"] if i < len(tasks) else "unknown",
                    "description": tasks[i].get("description", ""),
                    "tool": tasks[i].get("tool", "unknown"),
                    "result": f"任务执行失败: {str(result)}",
                    "status": "failed",
                    "error": str(result)
                }
                task_results.append(failed_task)
                all_context += f"\n任务{failed_task['task_id']}失败：{str(result)}\n"
            else:
                task_results.append(result)
                all_context += f"\n任务{result['task_id']}结果：\n{result['result']}\n"

        return task_results, all_context

    async def _execute_sequential_batch(
        self,
        tasks: List[Dict[str, Any]],
        work_id: str,
        chapter_id: str,
        context: str,
        resolver,
        on_task_start: Optional[callable],
        on_task_progress: Optional[callable],
        on_task_done: Optional[callable],
        context_payload: Optional[Dict[str, Any]] = None,
        shared_state: Optional[Dict[str, Any]] = None,
        conversation_id: Optional[str] = None,
        approval_callback: Optional[callable] = None,
    ) -> tuple:
        """
        串行执行一批任务

        Args:
            tasks: 任务列表
            work_id: 作品ID
            chapter_id: 章节ID
            context: 上下文
            context_payload: 结构化上下文（原始 request.context）
            resolver: 参数解析器
            on_task_start: 任务开始回调
            on_task_progress: 任务进度回调
            on_task_done: 任务完成回调

        Returns:
            (task_results, updated_context)
        """
        logger.info(f"[ParallelExecution] 开始串行执行{len(tasks)}个任务")

        task_results = []
        all_context = context

        for task in tasks:
            result = await self._execute_single_task_with_retry(
                task=task,
                work_id=work_id,
                chapter_id=chapter_id,
                context=all_context,
                context_payload=context_payload,
                resolver=resolver,
                on_task_start=on_task_start,
                on_task_progress=on_task_progress,
                on_task_done=on_task_done,
                batch_name="串行",
                shared_state=shared_state,
                conversation_id=conversation_id,
                approval_callback=approval_callback,
            )
            task_results.append(result)
            all_context += f"\n任务{result['task_id']}结果：\n{result['result']}\n"

        return task_results, all_context

    async def _execute_single_task_with_retry(
        self,
        task: Dict[str, Any],
        work_id: str,
        chapter_id: str,
        context: str,
        resolver,
        on_task_start: Optional[callable],
        on_task_progress: Optional[callable],
        on_task_done: Optional[callable],
        batch_name: str,
        context_payload: Optional[Dict[str, Any]] = None,
        shared_state: Optional[Dict[str, Any]] = None,
        conversation_id: Optional[str] = None,
        approval_callback: Optional[callable] = None,
    ) -> Dict[str, Any]:
        """
        执行单个任务（带重试）

        Args:
            task: 任务
            work_id: 作品ID
            chapter_id: 章节ID
            context: 上下文
            context_payload: 结构化上下文（原始 request.context）
            resolver: 参数解析器
            on_task_start: 任务开始回调
            on_task_progress: 任务进度回调
            on_task_done: 任务完成回调
            batch_name: 批次名称

        Returns:
            任务结果
        """
        start_time = time.time()
        task_id = task["task_id"]
        description = task["description"]
        tool_name = task.get("tool", "unknown")

        logger.info(f"[ParallelExecution] {batch_name}任务{task_id}开始: {description}")

        if on_task_start:
            await on_task_start(task)

        step_id = None
        if isinstance(shared_state, dict):
            step_map = shared_state.get("task_step_map")
            if isinstance(step_map, dict):
                step_id = step_map.get(task_id)
        if not isinstance(step_id, int):
            step_id = task_id

        task_state = dict(shared_state) if isinstance(shared_state, dict) else {}
        task_state["step_id"] = step_id
        stream_handler = getattr(self.agent, "stream_event_handler", None)
        if stream_handler:
            task_state["stream_event_handler"] = stream_handler

        last_error = None

        for retry_count in range(self.MAX_RETRIES + 1):
            try:
                # 解析任务参数中的占位符
                resolved_task = task.copy()
                if "params" in resolved_task:
                    resolved_task["params"] = await resolver.resolve_params(
                        resolved_task["params"],
                        current_task_id=task_id
                    )
                    # 绑定写回目标章节（只写入 state，不传给工具）
                    target_chapter = resolved_task["params"].pop("__target_chapter_id", None)
                    if target_chapter:
                        if not isinstance(target_chapter, str):
                            target_chapter = str(target_chapter)
                        task_state["target_chapter_id"] = target_chapter
                        task_state["target_chapter_source"] = "task_binding"
                        logger.info(
                            "[ParallelExecution] 任务%s 绑定目标章节: %s",
                            task_id,
                            target_chapter
                        )
                    logger.debug(f"[ParameterResolver] 任务{task_id}参数已解析")

                # 执行任务
                result = await self.agent._execute_task(
                    task=resolved_task,
                    work_id=work_id,
                    chapter_id=chapter_id,
                    context=context,
                    context_payload=context_payload,
                    on_progress=on_task_progress,
                    conversation_id=conversation_id,  # v8.0: 传递 conversation_id
                    state=task_state,  # 🆕 2026-01-12: 传递共享 state 用于章节缓存
                    approval_callback=approval_callback,
                )

                raw_result = result
                result_text = self._stringify_result(result)

                # 🆕 2026-01-18: explore_content 特殊处理 - 发射轮次事件并提取 explore_summary
                if tool_name == "explore_content":
                    raw_result, result_text = await self._handle_explore_content_result(
                        result, task_id, step_id
                    )
                    if isinstance(shared_state, dict) and isinstance(raw_result, dict):
                        if raw_result.get("success"):
                            shared_state["last_explore_result"] = raw_result
                            shared_state["last_explore_summary"] = result_text
                            target_id, source = self._extract_target_chapter_id(raw_result)
                            if target_id:
                                shared_state["target_chapter_id"] = target_id
                                shared_state["target_chapter_source"] = source
                                logger.info(
                                    "[ParallelExecution] 目标章节已固化: %s (source=%s)",
                                    target_id,
                                    source
                                )

                # 注册任务结果（保留结构体）
                await resolver.register_result(task_id, raw_result)
                logger.debug(f"[ParameterResolver] 任务{task_id}结果已注册")

                elapsed_time = time.time() - start_time
                task_with_time = {**task, "elapsed_time": elapsed_time}

                if on_task_done:
                    await on_task_done(task_with_time, result_text)

                logger.info(
                    f"[ParallelExecution] {batch_name}任务{task_id}完成" +
                    (f"（重试{retry_count}次后成功）" if retry_count > 0 else "")
                )

                return {
                    "task_id": task_id,
                    "description": description,
                    "tool": tool_name,
                    "result": result_text,
                    "raw_result": raw_result,
                    "status": "completed",
                    "elapsed_time": elapsed_time
                }

            except Exception as e:
                last_error = e
                is_retryable = any(
                    keyword in str(e).lower()
                    for keyword in self.RETRYABLE_KEYWORDS
                )

                if is_retryable and retry_count < self.MAX_RETRIES:
                    wait_time = 2 ** (retry_count + 1)
                    logger.warning(
                        f"[ParallelExecution] 任务{task_id}失败（{e}），"
                        f"{wait_time}秒后重试（{retry_count + 1}/{self.MAX_RETRIES}）"
                    )
                    await asyncio.sleep(wait_time)
                else:
                    break

        # 所有重试都失败
        logger.error(f"[ParallelExecution] {batch_name}任务{task_id}最终失败: {last_error}")

        error_result = f"错误: {str(last_error)}"
        await resolver.register_result(task_id, error_result)
        logger.debug(f"[ParameterResolver] 任务{task_id}失败结果已注册")

        elapsed_time = time.time() - start_time

        if on_task_done:
            await on_task_done({**task, "elapsed_time": elapsed_time}, error_result)

        return {
            "task_id": task_id,
            "description": description,
            "tool": tool_name,
            "result": error_result,
            "status": "failed"
        }

    @staticmethod
    def _stringify_result(result: Any) -> str:
        if result is None:
            return ""
        if isinstance(result, (dict, list)):
            try:
                return json.dumps(result, ensure_ascii=False)
            except Exception:
                return str(result)
        return str(result)

    async def _handle_explore_content_result(
        self,
        result: Any,
        task_id: int,
        step_id: Optional[int] = None
    ) -> tuple:
        """处理 explore_content 的结果

        1. 解析 JSON 提取 frontend_display
        2. 发射 explore_round 和 explore_summary 事件（若未在工具内发射）
        3. 提取 explore_summary 供后续工具使用

        Args:
            result: explore_content 返回的结果（JSON 字符串或 dict）
            task_id: 任务 ID
            step_id: 步骤 ID

        Returns:
            (raw_result, result_text) - 处理后的结果
        """
        # 解析 JSON
        if isinstance(result, str):
            try:
                result_data = json.loads(result)
            except json.JSONDecodeError:
                logger.warning(f"[ParallelExecution] explore_content 结果解析失败")
                return result, result
        elif isinstance(result, dict):
            result_data = result
        else:
            return result, str(result)

        # 检查是否成功
        if not result_data.get("success"):
            return result_data, json.dumps(result_data, ensure_ascii=False)

        # 发射 explore_round 和 explore_summary 事件
        if result_data.get("frontend_display") and not result_data.get("events_emitted"):
            await self._emit_explore_events(result_data, step_id or task_id)

        # 提取 explore_summary 供后续工具使用
        explore_summary = result_data.get("explore_summary", "")
        if not explore_summary:
            explore_summary = result_data.get("context_for_task", "")
        if not explore_summary:
            try:
                explore_summary = json.dumps(result_data, ensure_ascii=False)
            except Exception:
                explore_summary = ""

        # 返回 explore_summary 作为结果（供 ParameterResolver 解析）
        # 但保留完整 result_data 作为 raw_result（供调试）
        return result_data, explore_summary

    async def _emit_explore_events(
        self,
        result_data: Dict[str, Any],
        step_id: int
    ):
        """发射 explore_round 和 explore_summary 事件

        Args:
            result_data: explore_content 返回的完整数据
            step_id: 步骤 ID
        """
        from app.services.agent.stream.flow_events import FlowEventBuilder

        # 检查是否有 stream_event_handler
        if not hasattr(self.agent, 'stream_event_handler'):
            logger.warning("[ParallelExecution] agent 没有 stream_event_handler，无法发射 explore 事件")
            return

        stream_handler = self.agent.stream_event_handler
        if not stream_handler:
            return

        frontend_display = result_data.get("frontend_display", {})
        if not frontend_display:
            logger.warning("[ParallelExecution] explore_content 结果缺少 frontend_display")
            return

        # 发射每一轮的 explore_round 事件
        rounds = frontend_display.get("rounds", [])
        for round_data in rounds:
            try:
                event = FlowEventBuilder.explore_round(
                    step_id=step_id,
                    round_idx=round_data.get("round_idx", 1),
                    title=round_data.get("title", "探索"),
                    tool_calls=round_data.get("tool_calls", []),
                    hit_count=round_data.get("hit_count", 0),
                    missing_items=round_data.get("missing_items", []),
                    status_text=round_data.get("status_text", ""),
                    evidences=round_data.get("evidences", []),
                    review_status=round_data.get("review_status", ""),
                    reason=round_data.get("reason", "")
                )
                await stream_handler.emit_flow_event(event)
                logger.info(f"[ParallelExecution] 发射 explore_round 事件: 轮次 {round_data.get('round_idx')}")
            except Exception as e:
                logger.error(f"[ParallelExecution] 发射 explore_round 事件失败: {e}")

        # 发射 explore_summary 事件
        ai_analysis = frontend_display.get("ai_analysis", {})
        try:
            event = FlowEventBuilder.explore_summary(
                step_id=step_id,
                total_rounds=len(rounds),
                summary=ai_analysis.get("summary", result_data.get("analysis", "")),
                next_action=ai_analysis.get("next_action", ""),
                next_tool=ai_analysis.get("next_tool", ""),
                stats=ai_analysis.get("stats", result_data.get("stats", {})),
                sufficient=ai_analysis.get("sufficient"),
                coverage=ai_analysis.get("coverage")
            )
            await stream_handler.emit_flow_event(event)
            logger.info(f"[ParallelExecution] 发射 explore_summary 事件: {len(rounds)} 轮")
        except Exception as e:
            logger.error(f"[ParallelExecution] 发射 explore_summary 事件失败: {e}")
