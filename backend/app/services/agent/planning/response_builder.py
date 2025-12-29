# -*- coding: utf-8 -*-
"""
响应构建器

从 langgraph_agent.py 提取的规划响应构建逻辑：
- 任务分类
- 响应构建
- 格式化输出
- AI 整合（Phase 4.3）
"""

from typing import Dict, List, Any, Optional, Callable, Awaitable
import json
import logging

from app.services.agent.utils.context_builder import _build_summarization_context
from app.services.agent.model_selector import TaskType
from app.services.agent.prompts.format_guidelines import get_format_guidelines

logger = logging.getLogger(__name__)


# 定义工具类型
INPUT_TOOLS = {
    "get_context_tool",
    "search_analysis_fragments_tool"
}

DISPLAY_TOOLS = {
    "get_chapter_by_order_tool",
    "read_chapter_tool"
}

OUTPUT_TOOLS = {
    "continue_writing_tool",
    "analyze_text_tool"
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
        generate_text_stream_func: Optional[Callable[..., Awaitable[Dict]]] = None
    ):
        """
        Args:
            ai_service: HTTPAIService 实例
            generate_text_stream_func: 流式文本生成函数（用于 AI 整合）
        """
        self.ai_service = ai_service
        self._generate_text_stream = generate_text_stream_func

    def set_stream_generator(self, func: Callable[..., Awaitable[Dict]]):
        """设置流式生成函数（延迟初始化用）"""
        self._generate_text_stream = func

    async def build_final_response(
        self,
        task_results: List[Dict],
        message: str,
        on_content: Optional[Callable] = None,
        response_hint: Optional[str] = None,
        knowledge_docs: Optional[List[Dict]] = None
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
            if tool_name in ["continue_writing_tool"] and len(result) > 500:
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
            has_writing = any(task.get("tool") == "continue_writing_tool" for task in output_tasks)

            if all_analyze and not has_writing:
                logger.info(f"[Response] {len(output_tasks)}个分析类任务，使用AI整合")
                return await self.ai_summarization(task_results, message, on_content, knowledge_docs)

            # 简单拼接
            logger.info(f"[Response] {len(output_tasks)}个输出任务，简单拼接")
            parts = []
            for task in output_tasks:
                tool_name = task.get("tool", "unknown")
                result = task.get("result", "") or ""

                if tool_name == "analyze_text_tool":
                    parts.append(f"## 分析结果\n\n{result}")
                elif tool_name == "continue_writing_tool":
                    parts.append(f"## 续写内容\n\n{result}")
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
        knowledge_docs: Optional[List[Dict]] = None
    ) -> str:
        """AI整合任务结果

        Args:
            task_results: 任务结果列表
            message: 用户原始消息
            on_content: 内容回调函数
            knowledge_docs: 用户引用的知识库文档列表

        Returns:
            AI整合后的最终响应
        """
        from app.services.agent.utils.monitoring import increment_counter

        logger.info("[Summarization] 使用AI整合任务结果")

        # 检查是否设置了流式生成函数
        if not self._generate_text_stream:
            logger.warning("[Summarization] 未设置流式生成函数，返回简单拼接")
            return self._simple_concat(task_results, on_content)

        # 构建知识库文档上下文
        knowledge_section = self._build_knowledge_section(knowledge_docs)

        # 构建完整上下文
        all_context = f"用户请求：{message}\n\n"
        for result in task_results:
            all_context += f"\n任务{result['task_id']}结果：\n{result['result']}\n"

        # 上下文压缩
        compressed_context = _build_summarization_context(
            user_message=message,
            task_results=task_results,
            max_context_length=6000
        )

        logger.info(
            f"[Summarization] 上下文处理: "
            f"原始={len(all_context)}字符, "
            f"处理后={len(compressed_context)}字符"
        )

        # 获取格式指导
        format_guidelines = get_format_guidelines(lite=True)

        # 构建总结 prompt
        summary_prompt = f"""基于以下任务执行结果，生成最终的响应给用户。
{knowledge_section}
{compressed_context}

⚠️ 重要规则（必须遵守）：
1. 【数据忠实性】必须使用工具返回的真实数据，禁止编造或猜测！
   - 章节标题 = 工具返回的 title 字段值
   - 章节内容 = 工具返回的 content 字段值
   - 章节序号 = 工具返回的 order 字段值
2. 综合所有任务结果，用清晰、友好的语言呈现
3. 如果是创作内容，直接输出创作结果
4. 如果是分析/规划，给出详细说明
5. 如果用户询问事实性问题（如标题、内容等），直接引用工具返回的数据
6. 如果用户引用了知识库文档，优先基于文档内容回答

{format_guidelines}

请生成最终响应："""

        # 使用流式生成
        logger.info("[Summarization] 使用流式生成（_generate_text_stream）")

        async def stream_callback(chunk: str):
            if on_content and chunk:
                await on_content(chunk)

        result = await self._generate_text_stream(
            prompt=summary_prompt,
            on_chunk=stream_callback,
            max_tokens=2000,
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
