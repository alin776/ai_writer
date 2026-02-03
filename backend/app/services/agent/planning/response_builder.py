# -*- coding: utf-8 -*-
"""
响应构建器

从 langgraph_agent.py 提取的规划响应构建逻辑：
- 任务分类
- 响应构建
- 格式化输出
- AI 整合（Phase 4.3）
"""

from typing import Dict, List, Any, Optional, Callable, Awaitable, TYPE_CHECKING
import json
import logging

from app.services.agent.utils.context_builder import _build_summarization_context
from app.services.agent.model_selector import TaskType
from app.services.agent.prompts.format_guidelines import get_format_guidelines

if TYPE_CHECKING:
    from app.services.agent.stream.stream_event_handler import StreamEventHandler

logger = logging.getLogger(__name__)


# 定义工具类型
INPUT_TOOLS = {
    "get_context_tool",
    "search_content",
    "get_writing_context",
    "get_worldview_summary",  # 世界观查询工具，仅用于提供创作上下文
    "get_chapter_by_order_tool",  # 章节读取工具，在续写场景下是输入型
    "read_chapter_tool"  # 章节读取工具，在续写场景下是输入型
}

DISPLAY_TOOLS = {
    # 移除章节读取工具，因为在分阶段执行场景下，它们是输入型
    # 如果用户明确要求"获取第三章"，AI整合后也会正确返回内容
}

OUTPUT_TOOLS = {
    "smart_continue",
    "smart_rewrite",
    "smart_insert",
    "analyze_content"
}


def classify_tasks(task_results: List[Dict]) -> Dict[str, List]:
    """分类任务：输入型 vs 输出型 vs 展示型

    Args:
        task_results: 任务结果列表

    Returns:
        分类后的任务字典，包含 input_tasks, output_tasks, display_tasks
    """
    input_tasks = []
    output_tasks = []
    display_tasks = []

    for task in task_results:
        tool = task.get("tool", "")
        if tool in DISPLAY_TOOLS:
            display_tasks.append(task)
        elif tool in INPUT_TOOLS:
            input_tasks.append(task)
        elif tool in OUTPUT_TOOLS:
            output_tasks.append(task)
        else:
            output_tasks.append(task)

    logger.info(
        f"[TaskClassify] 任务分类: 输入型={len(input_tasks)}, "
        f"输出型={len(output_tasks)}, 展示型={len(display_tasks)}"
    )

    return {
        "input_tasks": input_tasks,
        "output_tasks": output_tasks,
        "display_tasks": display_tasks
    }


class ResponseBuilder:
    """响应构建器

    负责将任务结果整合为最终响应
    """

    def __init__(
        self,
        ai_service,
        generate_text_stream_func: Optional[Callable[..., Awaitable[Dict]]] = None,
        stream_event_handler: Optional["StreamEventHandler"] = None
    ):
        """
        Args:
            ai_service: HTTPAIService 实例
            generate_text_stream_func: 流式文本生成函数（用于 AI 整合）
            stream_event_handler: 流式事件处理器（用于发送 Summarization 事件）
        """
        self.ai_service = ai_service
        self._generate_text_stream = generate_text_stream_func
        self._stream_event_handler = stream_event_handler

    def set_stream_generator(self, func: Callable[..., Awaitable[Dict]]):
        """设置流式生成函数（延迟初始化用）"""
        self._generate_text_stream = func

    def set_stream_event_handler(self, handler: "StreamEventHandler"):
        """设置流式事件处理器"""
        self._stream_event_handler = handler

    async def _generate_summarization_reason(
        self,
        message: str,
        task_results: List[Dict[str, Any]]
    ) -> str:
        """生成 AI 整合分析的简短理由（用于前端展示）"""
        try:
            tasks = []
            for task in task_results[:6]:
                tool = str(task.get("tool", "")).strip() or "unknown_tool"
                desc = str(task.get("description", "")).strip()
                snippet = str(task.get("result", "")).strip().replace("\n", " ")
                if len(snippet) > 60:
                    snippet = snippet[:60] + "…"
                if desc and snippet:
                    tasks.append(f"{tool}：{desc}｜{snippet}")
                elif desc:
                    tasks.append(f"{tool}：{desc}")
                elif snippet:
                    tasks.append(f"{tool}｜{snippet}")
                else:
                    tasks.append(tool)
            tasks_text = "；".join(tasks)
            prompt = (
                "请基于【任务摘要】输出一段中文“任务结果摘要”（50字以内），"
                "必须包含任务中出现的具体名词或事件，不要空泛表述。\n"
                f"用户请求：{message}\n"
                f"任务数：{len(task_results)}\n"
                f"任务摘要：{tasks_text}\n"
                "只输出摘要本身，不要其他内容。"
            )
            response = await self.ai_service.call_ai(
                system_prompt="你是任务整合助手，只输出一句中文理由。",
                user_prompt=prompt,
                max_tokens=60,
                temperature=0.2,
                task_type=TaskType.SIMPLE_QA
            )
            reason = (response or "").strip()
            logger.info(f"[Summarization] reason生成: len={len(reason)} content={reason}")
            return reason
        except Exception as e:
            logger.warning(f"[Summarization] 生成理由失败: {e}")
            return ""

    async def build_final_response(
        self,
        task_results: List[Dict],
        message: str,
        on_content: Optional[Callable] = None,
        response_hint: Optional[str] = None,
        knowledge_docs: Optional[List[Dict]] = None,
        direct_answer: Optional[str] = None
    ) -> str:
        """智能构建最终响应

        根据任务类型智能判断是否需要AI整合：
        - 缺失前置条件 → 直接返回友好提示
        - 单个创作任务 → 直接返回
        - 多个输出任务 → 简单拼接
        - 其他情况 → AI整合
        """
        # 优先检查：缺失前置条件或积分不足
        for result in task_results:
            try:
                result_str = result.get('result', '')
                if not result_str:
                    continue

                result_json = json.loads(result_str)

                if result_json.get('status') == 'missing_prerequisite':
                    suggested = result_json.get('suggested_response', '')
                    if suggested:
                        logger.info("[Response] 检测到missing_prerequisite，直接返回友好提示")
                        if on_content:
                            await on_content(suggested)
                        return suggested

                if result_json.get('error') == 'tool_failed':
                    error_msg = result_json.get('message', '')
                    if "积分" in error_msg and ("不足" in error_msg or "余额" in error_msg):
                        friendly_msg = "积分余额不足，请先充值后再使用此功能。"
                        if on_content:
                            await on_content(friendly_msg)
                        return friendly_msg

            except (json.JSONDecodeError, TypeError, KeyError):
                continue

        # 分类任务
        classified = classify_tasks(task_results)
        output_tasks = classified["output_tasks"]
        display_tasks = classified["display_tasks"]

        # 情况0：纯展示型任务
        if len(output_tasks) == 0 and len(display_tasks) > 0:
            logger.info(f"[Response] 纯展示型任务({len(display_tasks)}个)，直接格式化返回")
            return await self.format_display_response(display_tasks, response_hint, on_content)

        # 情况1：没有输出任务
        if len(output_tasks) == 0:
            # ✅ 分阶段执行：如果有 direct_answer，说明是第一阶段，返回询问
            if direct_answer:
                logger.info("[Response] 分阶段执行第一阶段，返回 direct_answer 询问用户")
                if on_content:
                    on_content(direct_answer)
                return direct_answer

            logger.warning("[Response] 没有明确输出任务，使用AI整合")
            return await self.ai_summarization(task_results, message, on_content, knowledge_docs)

        # 情况2：单个输出任务
        elif len(output_tasks) == 1:
            task = output_tasks[0]
            tool_name = task.get("tool", "unknown")
            result = task.get("result", "") or ""

            # 使用知识库时，走AI整合路径
            if knowledge_docs:
                logger.info(f"[Response] 检测到知识库文档，使用AI整合")
                return await self.ai_summarization(task_results, message, on_content, knowledge_docs)

            # 创作类任务，且输出充分
            if tool_name in ["smart_continue", "smart_rewrite", "smart_insert"] and len(result) > 500:
                logger.info(f"[Response] 单个创作任务({tool_name})，直接返回")
                if on_content:
                    await on_content(result)
                return result

            # 分析类任务
            logger.info(f"[Response] 单个分析任务({tool_name})，使用AI格式化")
            return await self.ai_summarization(task_results, message, on_content, knowledge_docs)

        # 情况3：多个输出任务
        else:
            if knowledge_docs:
                logger.info(f"[Response] 检测到知识库文档，使用AI整合")
                return await self.ai_summarization(task_results, message, on_content, knowledge_docs)

            # 检查是否全是分析类任务
            analysis_like_tools = {"analyze_text_tool", "summarization", "analyze_content"}
            all_analyze = all(task.get("tool") in analysis_like_tools for task in output_tasks)
            has_writing = any(task.get("tool") in {"smart_continue", "smart_rewrite", "smart_insert"} for task in output_tasks)

            if all_analyze and not has_writing:
                logger.info(f"[Response] {len(output_tasks)}个分析类任务，使用AI整合")
                return await self.ai_summarization(task_results, message, on_content, knowledge_docs)

            # 简单拼接
            logger.info(f"[Response] {len(output_tasks)}个输出任务，简单拼接")
            parts = []
            for task in output_tasks:
                tool_name = task.get("tool", "unknown")
                result = task.get("result", "") or ""

                if tool_name in {"analyze_text_tool", "analyze_content"}:
                    parts.append(f"## 分析结果\n\n{result}")
                elif tool_name in {"smart_continue", "smart_rewrite", "smart_insert"}:
                    parts.append(f"## 创作内容\n\n{result}")
                else:
                    parts.append(result)

            final_content = "\n\n".join(parts)
            if on_content:
                await on_content(final_content)
            return final_content

    async def format_display_response(
        self,
        display_tasks: List[Dict],
        response_hint: Optional[str] = None,
        on_content: Optional[Callable] = None
    ) -> str:
        """格式化展示型任务的响应

        当用户只是查看数据（如查看章节内容）时，直接格式化返回，
        不需要调用AI进行整合，节省成本。

        Args:
            display_tasks: 展示型任务列表
            response_hint: Planning 阶段提供的响应提示
            on_content: 内容回调函数

        Returns:
            格式化后的响应内容
        """
        response_parts = []

        for task in display_tasks:
            description = task.get("description", "")
            result = task.get("result", "")

            try:
                result_json = json.loads(result)

                if isinstance(result_json, dict):
                    # 先检查是否是错误响应
                    if "error" in result_json:
                        error_msg = result_json.get("error", "未知错误")
                        total_chapters = result_json.get("total_chapters")
                        if total_chapters:
                            response_parts.append(f"❌ {error_msg}（该作品共有 {total_chapters} 章）")
                        else:
                            response_parts.append(f"❌ {error_msg}")
                        continue

                    title = result_json.get("title", "")
                    content = result_json.get("content", "")
                    word_count = result_json.get("word_count", 0)
                    chapter_order = result_json.get("order") or result_json.get("chapter_order", "")

                    # 根据 response_hint 智能返回
                    effective_hint = response_hint
                    if not effective_hint:
                        desc_lower = description.lower()
                        if "标题" in desc_lower or "题目" in desc_lower or "章名" in desc_lower:
                            effective_hint = "title"
                        elif "字数" in desc_lower or "多少字" in desc_lower:
                            effective_hint = "word_count"

                    if effective_hint == "title":
                        response_parts.append(f"第{chapter_order}章的标题是：**{title}**")
                    elif effective_hint == "word_count":
                        response_parts.append(f"第{chapter_order}章《{title}》共 **{word_count}** 字")
                    elif effective_hint == "title_and_word_count":
                        response_parts.append(f"第{chapter_order}章《**{title}**》，共 **{word_count}** 字")
                    elif title and content:
                        chapter_header = f"**第{chapter_order}章: {title}**" if chapter_order else f"**{title}**"
                        content_preview = content[:1500] + "..." if len(content) > 1500 else content
                        response_parts.append(f"{chapter_header}\n\n{content_preview}")
                    else:
                        response_parts.append(result)
                else:
                    response_parts.append(result)

            except (json.JSONDecodeError, TypeError):
                response_parts.append(result)

        final_response = "\n\n---\n\n".join(response_parts)

        if on_content and final_response:
            await on_content(final_response)

        return final_response

    async def ai_summarization(
        self,
        task_results: List[Dict],
        message: str,
        on_content: Optional[Callable] = None,
        knowledge_docs: Optional[List[Dict]] = None,
        output_title: Optional[str] = None,  # v6.5: 输出标题
        is_applicable: bool = False  # v6.5: 是否可应用
    ) -> str:
        """AI整合任务结果

        Args:
            task_results: 任务结果列表
            message: 用户原始消息
            on_content: 内容回调函数
            knowledge_docs: 用户引用的知识库文档列表
            output_title: 输出标题（用于 output_ready 事件）
            is_applicable: 是否可应用到编辑器

        Returns:
            AI整合后的最终响应
        """
        from app.services.agent.utils.monitoring import increment_counter

        logger.info("[Summarization] 使用AI整合任务结果")

        # 检查是否设置了流式生成函数
        if not self._generate_text_stream:
            logger.warning("[Summarization] 未设置流式生成函数，返回简单拼接")
            return self._simple_concat(task_results, on_content)

        # 任务分类
        classified = classify_tasks(task_results)

        # 构建知识库文档上下文
        knowledge_section = self._build_knowledge_section(knowledge_docs)
        task_results_snapshot = self._build_task_results_snapshot(task_results)

        # 构建完整上下文
        all_context = f"用户请求：{message}\n\n"
        for result in task_results:
            all_context += f"\n任务{result['task_id']}结果：\n{result['result']}\n"

        # 上下文压缩
        # 🔧 2026-01-12: 增加 max_context_length 从 6000 到 15000，避免分析结果被省略
        compressed_context = _build_summarization_context(
            user_message=message,
            task_results=task_results,
            max_context_length=15000
        )

        original_length = len(all_context)
        compressed_length = len(compressed_context)

        logger.info(
            f"[Summarization] 上下文处理: "
            f"原始={original_length}字符, "
            f"处理后={compressed_length}字符"
        )

        # 发送 Summarization 开始事件
        if self._stream_event_handler:
            logger.info("[Summarization] 准备发送 summarization_start 事件")
            reason = await self._generate_summarization_reason(message, task_results)
            task_classification = {
                "input_tasks": [{"tool": t.get("tool", ""), "description": t.get("description", "")} for t in classified["input_tasks"]],
                "output_tasks": [{"tool": t.get("tool", ""), "description": t.get("description", "")} for t in classified["output_tasks"]],
                "display_tasks": [{"tool": t.get("tool", ""), "description": t.get("description", "")} for t in classified["display_tasks"]]
            }
            context_stats = {
                "original_length": original_length,
                "compressed_length": compressed_length,
                "mode": "流式生成"
            }
            await self._stream_event_handler.emit_summarization_start(
                task_classification, context_stats, reason
            )
            logger.info("[Summarization] summarization_start 事件已发送")
        else:
            logger.warning("[Summarization] _stream_event_handler 未设置，跳过事件发送")

        # 获取格式指导
        format_guidelines = get_format_guidelines(lite=True)

        # 构建总结 prompt
        summary_prompt = f"""基于以下任务执行结果，生成最终的响应给用户。
{knowledge_section}
【任务结果快照(JSON，仅可依据此处与压缩上下文回答)】
{task_results_snapshot}

{compressed_context}

⚠️ 重要规则（必须遵守）：
1. 【数据忠实性】必须使用工具返回的真实数据，禁止编造或猜测！
   - 章节标题 = 工具返回的 title 字段值
   - 章节内容 = 工具返回的 content 字段值
   - 章节序号 = 工具返回的 order 字段值
   - 禁止引入其他作品/人物/设定，若未在任务结果中出现，请明确说明“未找到”

2. 【分阶段执行识别】⚠️ 最重要！
   - 只有当**用户原始请求是创作类**（续写/创作/改写/插入/写作/写大纲）时，才允许进入“分阶段追问”
   - 如果任务结果只包含**准备信息**（如世界观、章节内容），且用户原始请求是创作类：
     → 这是**创作请求的第一阶段**，需要询问用户创作细节
   - 如果用户原始请求是**分析/推演/设定补充/世界观文档**：
     → **禁止追问创作风格/字数/续写方向**，必须直接输出分析结论或指出分析缺口
   - 必须基于准备信息，生成针对性的询问：
     * 创作类：展示世界观或章节概括，询问字数、风格、重点
     * 分析类：只可询问缺失的分析维度或证据，不可引导续写/创作
   - 示例格式：
     "我看到世界观中有以下设定：
     - 主角：【XX】
     - 场景：【XX】
     - 设定：【XX】

     关于第一章，您希望：
     1. 字数大约多少？（建议2000-3000字）
     2. 风格偏好？（激昂、平淡、悬疑等）
     3. 重点展开哪些内容？"

3. 【编辑器操作识别】⚠️ 非常重要！
   - 如果任务结果中包含 `requires_confirmation: true`，表示内容**已经应用到编辑器**
   - 此时**禁止**在响应中重复展示完整的创作内容！
   - 应该只输出：
     a) 简要总结做了什么操作（如"已在第一章末尾续写了约500字"）
     b) 概括内容要点（2-3个要点即可）
     c) 引导用户下一步（如"内容已在编辑器中显示，需要我调整吗？"）
   - 示例格式：
     "已为第一章续写了约500字内容。

     【续写要点】
     - 延续了主角的内心独白
     - 加入了新角色的伏笔

     内容已在编辑器中显示，你可以直接查看和编辑。需要我继续往下写吗？"

4. 综合所有任务结果，用清晰、友好的语言呈现
5. 编号列表必须使用 Markdown 有序列表语法 `1.`，禁止 `1、` / `（1）` / `一、`
6. 如果是创作内容且**没有** `requires_confirmation`，直接输出创作结果
7. 如果是分析/规划，给出详细说明
8. 如果用户询问事实性问题（如标题、内容等），直接引用工具返回的数据
9. 如果用户引用了知识库文档，优先基于文档内容回答

{format_guidelines}

请生成最终响应："""

        # 使用流式生成
        logger.info("[Summarization] 使用流式生成（_generate_text_stream）")

        # v6.6: 在第一个 chunk 输出时才发送 summarization_complete 和 output_ready
        # 这样 SummarizationCard 的转圈状态会持续到 LLM 开始输出
        first_chunk_sent = False

        async def stream_callback(chunk: str):
            nonlocal first_chunk_sent
            # 第一个 chunk 时发送 summarization_complete 和 output_ready
            if not first_chunk_sent and chunk:
                first_chunk_sent = True
                if self._stream_event_handler:
                    # 1. 先发送 summarization_complete（AI整合完成）
                    await self._stream_event_handler.emit_summarization_complete()
                    logger.info("[Summarization] summarization_complete 事件已发送（第一个chunk时）")

                    # 2. 再发送 output_ready（输出容器出现）
                    from app.services.agent.stream.flow_events import FlowEventBuilder
                    await self._stream_event_handler.emit_flow_event(
                        FlowEventBuilder.output_ready(
                            output_title or "生成内容",
                            "",  # 内容将通过 on_content 流式发送
                            is_applicable=is_applicable
                        )
                    )
                    logger.info("[Summarization] output_ready 事件已发送（第一个chunk时）")

            if on_content and chunk:
                await on_content(chunk)

        result = await self._generate_text_stream(
            prompt=summary_prompt,
            on_chunk=stream_callback,
            max_tokens=20000,
            temperature=0.7,
            task_type=TaskType.SUMMARIZATION,
            buffer_size=1
        )

        # 检查是否有错误
        if "error" in result and not result.get("partial"):
            error_msg = result.get('error', '')
            logger.warning(f"[Summarization] _generate_text_stream 失败: {error_msg}")
            increment_counter("ai_summarization_error", labels={"error_type": error_msg[:50] if error_msg else 'unknown'})

            # 检测积分不足错误
            if "积分" in error_msg and ("不足" in error_msg or "余额" in error_msg):
                fallback_content = "积分余额不足，请先充值后再使用此功能。"
                if on_content:
                    await on_content(fallback_content)
                return fallback_content

            # 返回简单的任务结果拼接作为 fallback
            return await self._simple_concat(task_results, on_content, with_error=True)

        if result.get("partial"):
            logger.warning(f"[Summarization] 流式生成超时，返回部分内容（{len(result.get('text', ''))}字符）")

        return result.get("text", "")

    def _build_task_results_snapshot(self, task_results: List[Dict]) -> str:
        """构建任务结果快照，避免上下文污染。

        2026-01-21: 根据工具类型使用不同的截断限制，与 context_builder.py 保持一致
        """
        from app.services.agent.utils.context_builder import FULL_CONTENT_TOOLS

        DEFAULT_LIMIT = 2000  # 默认截断限制

        snapshot = []
        for task in task_results:
            tool_name = task.get("tool", "")
            result = task.get("result", "")
            if not isinstance(result, str):
                try:
                    result = json.dumps(result, ensure_ascii=False)
                except Exception:
                    result = str(result)

            # 根据工具类型确定截断限制
            truncate_limit = FULL_CONTENT_TOOLS.get(tool_name, DEFAULT_LIMIT)

            if len(result) > truncate_limit:
                result = f"{result[:truncate_limit]}...[省略{len(result) - truncate_limit}字符]..."
            snapshot.append({
                "task_id": task.get("task_id"),
                "tool": tool_name,
                "status": task.get("status", ""),
                "description": task.get("description", ""),
                "result": result
            })

        return json.dumps(snapshot, ensure_ascii=False)

    def _build_knowledge_section(self, knowledge_docs: Optional[List[Dict]]) -> str:
        """构建知识库文档上下文"""
        if not knowledge_docs:
            return ""

        logger.info(f"[Summarization] 注入 {len(knowledge_docs)} 个知识库文档到总结prompt")
        knowledge_parts = []

        for doc in knowledge_docs[:3]:
            title = doc.get("title") or "未命名文档"
            tags = doc.get("tags") or []
            source = doc.get("source_type") or "unknown"
            content = doc.get("content") or ""
            snippet = content.strip()[:1200] if content else ""

            if snippet:
                tags_str = ', '.join(tags) if tags else '无'
                knowledge_parts.append(
                    f"=== 知识库文档 ===\n"
                    f"文档标题: {title}\n"
                    f"文档来源: {source}\n"
                    f"文档标签: {tags_str}\n"
                    f"文档正文内容:\n{snippet}\n"
                    f"=== 文档结束 ==="
                )

        if knowledge_parts:
            return "\n\n【用户引用的知识库文档】\n请优先参考以下文档内容回答用户问题：\n\n" + "\n\n".join(knowledge_parts) + "\n\n"
        return ""

    async def _simple_concat(
        self,
        task_results: List[Dict],
        on_content: Optional[Callable] = None,
        with_error: bool = False
    ) -> str:
        """简单拼接任务结果"""
        if with_error:
            fallback_content = "抱歉，AI整合失败。以下是任务结果摘要：\n\n"
        else:
            fallback_content = ""

        for task_result in task_results:
            fallback_content += f"- 任务{task_result['task_id']}: {task_result.get('description', 'N/A')}\n"
            if task_result.get('status') == 'completed':
                result_text = str(task_result.get('result', ''))[:200]
                fallback_content += f"  结果: {result_text}...\n"

        if on_content:
            await on_content(fallback_content)
        return fallback_content
