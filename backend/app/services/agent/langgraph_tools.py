# -*- coding: utf-8 -*-
"""
LangGraph 工具定义

从 langgraph_agent.py 拆分的 LangChain @tool 装饰器工具：
- 写作工具: analyze_text_tool
- 章节工具: read_chapter_tool (支持多章节), get_chapter_by_order_tool, get_context_tool
- 检索工具: search_analysis_fragments_tool
- 辅助函数: _generate_text_helper, validate_uuid, _retry_on_failure

更新记录:
- v2.8.0 (2025-12-10): 删除 polish_text_tool，read_chapter_tool 支持多章节读取
"""

import asyncio
import json
import logging
import re
import threading
from typing import Optional, Union, List, Dict, Any

from langchain_core.tools import tool

from app.services.ai.http_ai_service import HTTPAIService
from app.services.agent.model_selector import TaskType
from app.services.agent.timeout_config import TimeoutConfig, async_timeout
from app.core.database import AsyncSessionLocal

logger = logging.getLogger(__name__)


# ==================== 全局 AI Service 管理 ====================

_global_ai_service: Optional[HTTPAIService] = None
_global_ai_service_lock = threading.Lock()


def set_global_ai_service(ai_service: HTTPAIService):
    """设置全局 AI Service（线程安全版本）"""
    global _global_ai_service
    with _global_ai_service_lock:
        _global_ai_service = ai_service
        logger.debug("[set_global_ai_service] AI Service已设置（线程安全）")


def get_global_ai_service() -> Optional[HTTPAIService]:
    """获取全局 AI Service（线程安全版本）"""
    with _global_ai_service_lock:
        return _global_ai_service


# ==================== UUID 验证 ====================

UUID_PATTERN = re.compile(
    r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
    re.IGNORECASE
)


def validate_uuid(value: str, field_name: str = "ID") -> Optional[str]:
    """验证UUID格式

    Args:
        value: 要验证的UUID字符串
        field_name: 字段名称（用于错误消息）

    Returns:
        如果格式正确返回None，否则返回错误消息JSON字符串
    """
    if not value:
        return None

    if not UUID_PATTERN.match(value):
        return json.dumps({
            "error": f"无效的{field_name}格式",
            "provided_value": value,
            "message": f"{field_name}必须是标准UUID格式（36字符）",
            "example": "627feba4-2097-4f28-a3f3-7641d10f7f40"
        }, ensure_ascii=False, indent=2)

    return None


def is_chapter_order(value: str) -> bool:
    """检查值是否为章节序号（纯数字）

    Args:
        value: 要检查的值

    Returns:
        如果是纯数字返回 True
    """
    if not value:
        return False
    return value.isdigit() and 1 <= int(value) <= 9999


async def resolve_chapter_id(
    work_id: str,
    chapter_ref: str,
    db_session=None
) -> tuple[str, Optional[str]]:
    """智能解析章节引用（支持 UUID 或序号）

    🔧 2025-12-15: 新增支持章节序号自动转 UUID

    Args:
        work_id: 作品 ID
        chapter_ref: 章节引用（可以是 UUID 或章节序号）
        db_session: 可选的数据库会话

    Returns:
        (chapter_id, error_json): 成功返回 (chapter_uuid, None)，失败返回 (None, error_json)
    """
    if not chapter_ref:
        return None, None

    # 如果是有效的 UUID，直接返回
    if UUID_PATTERN.match(chapter_ref):
        return chapter_ref, None

    # 如果是章节序号，查询数据库获取 UUID
    if is_chapter_order(chapter_ref):
        chapter_order = int(chapter_ref)

        # 如果没有提供 db_session，创建一个新的
        if db_session is None:
            async with AsyncSessionLocal() as db:
                return await _query_chapter_by_order(db, work_id, chapter_order)
        else:
            return await _query_chapter_by_order(db_session, work_id, chapter_order)

    # 既不是 UUID 也不是序号，返回错误
    return None, json.dumps({
        "error": "无效的章节引用格式",
        "provided_value": chapter_ref,
        "message": "章节引用必须是 UUID 格式或章节序号（1-9999）",
        "example_uuid": "627feba4-2097-4f28-a3f3-7641d10f7f40",
        "example_order": "1"
    }, ensure_ascii=False, indent=2)


async def _query_chapter_by_order(db, work_id: str, chapter_order: int) -> tuple[str, Optional[str]]:
    """根据章节序号查询章节 UUID"""
    try:
        from app.models.work import Work
        from sqlalchemy.orm import selectinload
        from sqlalchemy import select

        result = await db.execute(
            select(Work)
            .options(selectinload(Work.chapters))
            .where(Work.id == work_id)
        )
        work = result.scalar_one_or_none()

        if not work:
            return None, json.dumps({
                "error": "作品不存在",
                "work_id": work_id
            }, ensure_ascii=False, indent=2)

        for chapter in work.chapters:
            if chapter.order == chapter_order:
                logger.info(f"[resolve_chapter_id] 序号 {chapter_order} -> UUID {chapter.id}")
                return str(chapter.id), None

        return None, json.dumps({
            "error": f"未找到第{chapter_order}章",
            "work_id": work_id,
            "total_chapters": len(work.chapters)
        }, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"[resolve_chapter_id] 查询失败: {e}")
        return None, json.dumps({
            "error": f"查询章节失败: {str(e)}",
            "work_id": work_id,
            "chapter_order": chapter_order
        }, ensure_ascii=False, indent=2)


# ==================== 辅助函数 ====================

async def _retry_on_failure(func, *args, max_retries=3, **kwargs):
    """通用重试包装器：用于数据库操作等可能失败的操作"""
    retry_count = 0

    while retry_count < max_retries:
        try:
            result = await func(*args, **kwargs)
            return result
        except Exception as e:
            retry_count += 1
            logger.error(f"[Retry] {func.__name__} 失败 (尝试 {retry_count}/{max_retries}): {e}")

            if retry_count >= max_retries:
                raise

            await asyncio.sleep(2 ** retry_count)

    raise Exception(f"{func.__name__} 失败，已重试{max_retries}次")


async def _generate_text_helper(
    prompt: str,
    temperature: float = 0.7,
    max_tokens: int = 1000,
    task_type: Optional[TaskType] = None
) -> str:
    """辅助函数：使用 HTTPAIService 生成文本（带重试机制）"""
    ai_service = get_global_ai_service()
    if not ai_service:
        return "错误：AI服务未初始化"

    messages = [{"role": "user", "content": prompt}]
    generated_text = ""
    max_retries = 3
    retry_count = 0

    while retry_count < max_retries:
        try:
            async with async_timeout(TimeoutConfig.LLM_CALL):
                async for chunk, _ in ai_service._stream_chat(
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    task_type=task_type
                ):
                    if chunk:
                        generated_text += chunk

            if generated_text:
                return generated_text

            retry_count += 1
            logger.warning(f"[_generate_text_helper] 生成文本为空，重试 {retry_count}/{max_retries}")

        except asyncio.TimeoutError:
            retry_count += 1
            logger.error(f"[_generate_text_helper] 生成超时（{TimeoutConfig.LLM_CALL}秒）(尝试 {retry_count}/{max_retries})")

            if retry_count >= max_retries:
                return f"错误：AI服务调用超时，已重试{max_retries}次"

            await asyncio.sleep(2 ** retry_count)

        except Exception as e:
            error_str = str(e)
            # 检测积分不足错误，直接返回友好提示（不重试）
            if "积分" in error_str and ("不足" in error_str or "余额" in error_str):
                logger.warning(f"[_generate_text_helper] 积分不足: {error_str}")
                return "积分余额不足，请先充值后再使用此功能。"

            retry_count += 1
            logger.error(f"[_generate_text_helper] 生成失败 (尝试 {retry_count}/{max_retries}): {e}")

            if retry_count >= max_retries:
                return f"错误：AI服务调用失败，已重试{max_retries}次。错误信息：{error_str}"

            await asyncio.sleep(2 ** retry_count)

    return generated_text or "错误：生成内容为空"


# ==================== 写作工具 ====================

@tool
async def analyze_text_tool(text: str, focus: str = "all") -> str:
    """分析工具：分析文本问题

    Args:
        text: 待分析的文本
        focus: 分析重点（all/grammar/logic/style）

    Returns:
        分析报告
    """
    from app.prompts import get_prompt_manager

    if not text or not text.strip():
        logger.warning("[analyze_text_tool] 收到空文本")
        return "错误：未提供待分析的文本内容。"

    if "$TASK_" in text and "$" in text[text.find("$TASK_")+1:]:
        logger.warning(f"[analyze_text_tool] 检测到未解析的占位符")
        return f"错误：文本参数中包含未解析的占位符。原始参数: {text[:200]}"

    try:
        prompt_manager = get_prompt_manager()
        base_prompt = prompt_manager.render("analyze_text", text=text, focus=focus)

        result = await _generate_text_helper(
            base_prompt,
            temperature=0.3,
            max_tokens=1500,
            task_type=TaskType.SUMMARIZATION
        )

        logger.info(f"✅ [Agent分析] 分析完成，结果长度: {len(result)}")
        return result

    except Exception as e:
        logger.error(f"约束提示词系统失败，使用降级方案: {e}")
        prompt = f"""请分析以下文本，重点关注：{focus}

文本：
{text}

请提供详细的分析报告："""

        return await _generate_text_helper(
            prompt,
            temperature=0.3,
            max_tokens=1500,
            task_type=TaskType.SUMMARIZATION
        )


# ==================== 分析工具（聚合） ====================

def _extract_content_from_context(context_value: str) -> str:
    if not context_value:
        return ""
    context_text = str(context_value).strip()
    if not context_text:
        return ""

    parsed = None
    if context_text[:1] in ("{", "["):
        try:
            parsed = json.loads(context_text)
        except Exception:
            parsed = None

    if isinstance(parsed, dict):
        chapters = parsed.get("chapters")
        if isinstance(chapters, list) and chapters:
            contents = []
            for chapter in chapters:
                if isinstance(chapter, dict):
                    content = chapter.get("content", "")
                else:
                    content = str(chapter) if chapter is not None else ""
                if content:
                    contents.append(content)
            if contents:
                return "\n\n".join(contents)
        for key in ("content", "text", "chapter_content"):
            value = parsed.get(key)
            if isinstance(value, str) and value.strip():
                return value

    if isinstance(parsed, list):
        contents = []
        for item in parsed:
            if isinstance(item, dict):
                content = item.get("content", "")
            else:
                content = item if isinstance(item, str) else ""
            if content:
                contents.append(content)
        if contents:
            return "\n\n".join(contents)

    if len(context_text) >= 10:
        return context_text
    return ""

@tool
async def analyze_content(
    content: str = "",
    text: str = "",
    work_id: str = "",
    chapter_id: str = "",
    analysis_types: Union[str, List[str]] = "text,style",
    focus: str = "all",
    depth: str = "normal",
    context: str = ""
) -> str:
    """分析工具：一站式内容分析"""
    content_value = content or text
    if not isinstance(content_value, str):
        content_value = str(content_value) if content_value is not None else ""
    if not content_value.strip():
        content_value = _extract_content_from_context(context)
    if not content_value or not content_value.strip():
        logger.warning("[analyze_content] 收到空文本")
        return "错误：未提供待分析的文本内容。"

    if "$TASK_" in content_value and "$" in content_value[content_value.find("$TASK_")+1:]:
        logger.warning("[analyze_content] 检测到未解析的占位符")
        return f"错误：文本参数中包含未解析的占位符。原始参数: {content_value[:200]}"

    analysis_list: List[str] = []
    if isinstance(analysis_types, (list, tuple, set)):
        analysis_list = [str(item).strip().lower() for item in analysis_types if str(item).strip()]
    else:
        analysis_list = [
            item.strip().lower()
            for item in str(analysis_types).split(",")
            if item.strip()
        ]
    if not analysis_list:
        analysis_list = ["text", "style"]

    try:
        from app.services.agent.tools.analysis_tools import AnalyzeContentInput, analyze_content_executor
        input_data = AnalyzeContentInput(
            text=content_value,
            analysis_types=analysis_list,
            focus=focus,
            depth=depth,
            context=context,
            work_id=work_id,
            chapter_id=chapter_id
        )
        result = await analyze_content_executor(input_data)
        if result.success and result.data is not None:
            return json.dumps(result.data, ensure_ascii=False, indent=2)
        return json.dumps({
            "error": result.message,
            "data": result.data
        }, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"[analyze_content] 执行失败: {e}")
        return json.dumps({
            "error": f"分析失败: {str(e)}"
        }, ensure_ascii=False, indent=2)


# ==================== 章节工具 ====================

@tool
async def read_chapter_tool(work_id: Optional[str] = None, chapter_id: str = "") -> str:
    """[DEPRECATED] 读取指定章节工具 - 请使用 get_writing_context 代替

    Args:
        work_id: 作品ID（UUID格式）
        chapter_id: 章节ID（UUID格式或章节序号）

    Returns:
        章节信息JSON

    @deprecated 请使用 get_writing_context(work_id=..., chapter_id=..., include="chapter")
    """
    logger.warning("[read_chapter_tool] ⚠️ 此工具已废弃，请使用 get_writing_context")
    result_str = await get_writing_context.ainvoke({
        "work_id": work_id or "",
        "chapter_id": chapter_id,
        "include": "chapter"
    })
    # 格式转换：从 {"chapters": [...]} 转为单章节格式
    try:
        result = json.loads(result_str)
        chapters = result.get("chapters", [])
        if chapters and len(chapters) == 1:
            ch = chapters[0]
            return json.dumps({
                "chapter_id": ch.get("id"),
                "title": ch.get("title"),
                "order": ch.get("order"),
                "content": ch.get("content", ""),
                "content_length": len(ch.get("content", "")),
                "word_count": ch.get("word_count"),
                "status": "unknown"
            }, ensure_ascii=False, indent=2)
        elif chapters:
            return json.dumps({
                "type": "multi_chapter",
                "count": len(chapters),
                "chapters": [{
                    "chapter_id": ch.get("id"),
                    "title": ch.get("title"),
                    "order": ch.get("order"),
                    "content": ch.get("content", ""),
                    "content_length": len(ch.get("content", "")),
                    "word_count": ch.get("word_count"),
                    "status": "unknown"
                } for ch in chapters]
            }, ensure_ascii=False, indent=2)
    except:
        pass
    return result_str


def _parse_chapter_orders(
    chapter_order: str,
    available_orders: Optional[List[int]] = None
) -> tuple[list[int], list[str], bool]:
    """解析章节序号参数，支持混合格式与最近 N 章

    Args:
        chapter_order: 章节序号，支持以下格式：
            - 单个: "1" 或 1
            - 多个: "1,2,3,4,5"
            - 范围: "1-5"
            - 混合: "1-5,7"
            - 最近: "-3"（最近三章，需要 available_orders）
        available_orders: 作品中可用的章节序号（用于 -N 解析）

    Returns:
        (orders, ignored_parts, used_fallback)
        - orders: 按输入顺序去重后的章节序号列表
        - ignored_parts: 无法解析的片段
        - used_fallback: 是否回退到默认第1章
    """
    orders: list[int] = []
    ignored_parts: list[str] = []
    seen: set[int] = set()
    used_fallback = False
    available_orders = sorted(available_orders or [])

    def append_order(order: int) -> None:
        if order not in seen:
            orders.append(order)
            seen.add(order)

    def append_recent(n: int) -> None:
        if n <= 0:
            ignored_parts.append(f"-{abs(n)}")
            return
        if not available_orders:
            ignored_parts.append(f"-{n}")
            return
        for order in available_orders[-n:]:
            append_order(order)

    # 处理整数输入（向后兼容）
    if isinstance(chapter_order, int):
        if chapter_order < 0:
            append_recent(abs(chapter_order))
        else:
            append_order(chapter_order)
        if not orders:
            used_fallback = True
            append_order(1)
        return orders, ignored_parts, used_fallback

    chapter_order = str(chapter_order).strip()
    if not chapter_order:
        return [], [], False

    parts = [part.strip() for part in chapter_order.split(",") if part.strip()]
    for part in parts:
        if re.fullmatch(r"-\d+", part):
            append_recent(abs(int(part)))
            continue

        if re.fullmatch(r"\d+\s*-\s*\d+", part):
            start_str, end_str = part.split("-", 1)
            try:
                start = int(start_str.strip())
                end = int(end_str.strip())
                if start < 0 or end < 0 or start > end:
                    ignored_parts.append(part)
                    continue
                for order in range(start, end + 1):
                    append_order(order)
                continue
            except ValueError:
                ignored_parts.append(part)
                continue

        try:
            order = int(part)
            if order < 0:
                ignored_parts.append(part)
                continue
            append_order(order)
        except ValueError:
            ignored_parts.append(part)

    if not orders:
        used_fallback = True
        append_order(1)

    return orders, ignored_parts, used_fallback


def _get_content_limit_for_batch(chapter_count: int) -> int:
    """根据批量读取的章节数量，动态计算每章的内容限制

    🔧 2025-12-25: 智能压缩策略，避免大量章节导致内容过长

    策略:
    - 1-5 章: 完整内容 (5000 字/章)
    - 6-15 章: 精简内容 (2000 字/章)
    - 16-30 章: 摘要模式 (1000 字/章)
    - 31-50 章: 极简摘要 (500 字/章)
    - 51+ 章: 标题+开头 (300 字/章)

    目标: 无论多少章，总内容控制在 50,000 字符以内

    Args:
        chapter_count: 批量读取的章节总数

    Returns:
        每章内容的字符限制
    """
    if chapter_count <= 5:
        return 5000  # 5 × 5000 = 25,000
    elif chapter_count <= 15:
        return 2000  # 15 × 2000 = 30,000
    elif chapter_count <= 30:
        return 1000  # 30 × 1000 = 30,000
    elif chapter_count <= 50:
        return 500   # 50 × 500 = 25,000
    else:
        return 300   # 100 × 300 = 30,000


@tool
async def get_chapter_by_order_tool(work_id: Optional[str] = None, chapter_order: str = "1") -> str:
    """[DEPRECATED] 通过章节序号获取章节内容 - 请使用 get_writing_context 代替

    Args:
        work_id: 作品ID（UUID格式）
        chapter_order: 章节序号（支持 "1" / "1,2,3" / "1-5"）

    Returns:
        章节信息JSON

    @deprecated 请使用 get_writing_context(work_id=..., chapter_orders=..., include="chapter")
    """
    logger.warning("[get_chapter_by_order_tool] ⚠️ 此工具已废弃，请使用 get_writing_context")
    result_str = await get_writing_context.ainvoke({
        "work_id": work_id or "",
        "chapter_orders": chapter_order,
        "include": "chapter"
    })
    # 格式转换：从 {"chapters": [...]} 转为原格式
    try:
        result = json.loads(result_str)
        chapters = result.get("chapters", [])
        if chapters and len(chapters) == 1:
            ch = chapters[0]
            return json.dumps({
                "chapter_id": ch.get("id"),
                "title": ch.get("title"),
                "order": ch.get("order"),
                "content": ch.get("content", ""),
                "content_length": len(ch.get("content", "")),
                "word_count": ch.get("word_count"),
                "status": "unknown"
            }, ensure_ascii=False, indent=2)
        elif chapters:
            return json.dumps({
                "type": "multi_chapter",
                "count": len(chapters),
                "chapters": [{
                    "chapter_id": ch.get("id"),
                    "title": ch.get("title"),
                    "order": ch.get("order"),
                    "content": ch.get("content", ""),
                    "content_length": len(ch.get("content", "")),
                    "word_count": ch.get("word_count"),
                    "status": "unknown"
                } for ch in chapters]
            }, ensure_ascii=False, indent=2)
    except:
        pass
    return result_str


@tool
async def search_analysis_fragments_tool(
    work_id: str,
    query: str,
    top_k: int = 5,
    chapter_id: str = "",
    include_current: bool = True,
    look_ahead: int = 0,
    max_content_length: int = 200
) -> str:
    """检索分析碎片工具：混合检索（向量+全文），召回作品相关片段（兼容旧名）

    Args:
        work_id: 作品ID（UUID格式，必需）
        query: 查询文本（必需）
        top_k: 返回前K个最相关结果
        chapter_id: 当前章节ID（可选，用于确定时序窗口）
        include_current: 是否包含当前章
        look_ahead: 允许向后看的章节数（默认0表示不限制，检索所有章节）
        max_content_length: 返回片段长度上限（默认200）

    Returns:
        相关片段JSON
    """
    if not work_id:
        return json.dumps({
            "status": "missing_prerequisite",
            "missing": "work_id",
            "message": "需要指定作品ID才能检索分析片段"
        }, ensure_ascii=False, indent=2)

    if not query or not query.strip():
        return json.dumps({
            "status": "missing_prerequisite",
            "missing": "query",
            "message": "需要指定查询文本才能检索分析片段"
        }, ensure_ascii=False, indent=2)

    uuid_error = validate_uuid(work_id, "作品ID")
    if uuid_error:
        return uuid_error

    current_order = None
    if chapter_id:
        uuid_error = validate_uuid(chapter_id, "章节ID")
        if uuid_error:
            return uuid_error

    async with AsyncSessionLocal() as db:
        try:
            from app.services.search import HybridRetriever
            from app.services.chapter_service import ChapterService

            # 获取当前章节序号（若提供）
            if chapter_id:
                chapter_service = ChapterService(db)
                chapter = await _retry_on_failure(
                    chapter_service.get_chapter_by_id,
                    chapter_id,
                    max_retries=2
                )
                if chapter:
                    current_order = chapter.order

            retriever = HybridRetriever(db)
            # look_ahead=0 表示不限制时序窗口，检索所有章节
            # current_order=None 时传 None 让 retriever 自行处理
            look_ahead_param = look_ahead
            if not chapter_id and look_ahead <= 0:
                look_ahead_param = None
            min_order = None
            max_order = None
            if current_order is not None and look_ahead_param is not None:
                min_order = current_order
                max_order = current_order + look_ahead_param
            results = await retriever.search(
                work_id=work_id,
                query=query,
                current_order=current_order,
                top_k=top_k,
                include_current=include_current,
                look_ahead=look_ahead_param,
                min_order=min_order,
                max_order=max_order,
            )

            if not results:
                return json.dumps({
                    "message": "未找到相关片段",
                    "work_id": work_id,
                    "query": query,
                    "results": []
                }, ensure_ascii=False, indent=2)

            snippet_length = min(max_content_length, 200)
            formatted_results = []
            for i, result in enumerate(results):
                content = result.get("content", "")
                snippet = content[:snippet_length]
                if len(content) > snippet_length:
                    snippet += "..."
                formatted_results.append({
                    "rank": i + 1,
                    "chapter_id": result.get("chapter_id"),  # 新增
                    "similarity": result.get("similarity", 0),
                    "chapter_title": result.get("chapter_title"),
                    "chapter_order": result.get("chapter_order"),
                    "paragraph_index": result.get("paragraph_index"),  # 新增
                    "node_id": result.get("node_id"),
                    "snippet": snippet,
                    "source": result.get("source", "vector")
                })

            logger.info(f"[search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到{len(results)}个片段")

            return json.dumps({
                "work_id": work_id,
                "query": query,
                "total_results": len(results),
                "results": formatted_results
            }, ensure_ascii=False, indent=2)

        except Exception as e:
            try:
                await db.rollback()
            except:
                pass
            logger.error(f"[search_analysis_fragments_tool] ❌ Hybrid检索失败: {e}")
            return json.dumps({
                "error": f"检索失败: {str(e)}",
                "work_id": work_id
            }, ensure_ascii=False, indent=2)

        finally:
            try:
                await db.close()
            except:
                pass


@tool
async def search_content(
    work_id: str,
    query: str,
    top_k: int = 10,
    chapter_id: str = "",
    look_ahead: int = 0
) -> str:
    """搜索多个相关位置（返回位置 + 片段）

    Args:
        work_id: 作品ID（UUID格式，必需）
        query: 查询文本（必需）
        top_k: 返回前K个最相关结果
        chapter_id: 当前章节ID（可选，用于时序窗口）
        look_ahead: 允许向后看的章节数（默认0表示不限制）

    Returns:
        位置 + 片段 JSON
    """
    # 复用旧检索实现，统一返回片段字段
    result_str = await search_analysis_fragments_tool.ainvoke({
        "work_id": work_id,
        "query": query,
        "top_k": top_k,
        "chapter_id": chapter_id,
        "include_current": True,
        "look_ahead": look_ahead,
        "max_content_length": 200
    })

    try:
        result = json.loads(result_str) if isinstance(result_str, str) else result_str
        if not isinstance(result, dict) or "results" not in result:
            return result_str

        formatted_results = []
        for i, item in enumerate(result.get("results", [])):
            content = item.get("content", "") if isinstance(item, dict) else ""
            snippet = item.get("snippet", "") if isinstance(item, dict) else ""
            if not snippet:
                snippet = content[:200] + "..." if len(content) > 200 else content
            formatted_results.append({
                "rank": i + 1,
                "chapter_id": item.get("chapter_id"),
                "chapter_order": item.get("chapter_order"),
                "chapter_title": item.get("chapter_title"),
                "paragraph_index": item.get("paragraph_index"),
                "node_id": item.get("node_id"),
                "snippet": snippet,
                "similarity": item.get("similarity", 0),
                "source": item.get("source", "hybrid")
            })

        return json.dumps({
            "work_id": result.get("work_id", work_id),
            "query": result.get("query", query),
            "total_results": len(formatted_results),
            "results": formatted_results
        }, ensure_ascii=False, indent=2)
    except Exception:
        return result_str


@tool
async def get_context_tool(work_id: Optional[str] = None, chapter_id: str = "") -> str:
    """[DEPRECATED] 获取上下文工具 - 请使用 get_writing_context 代替

    Args:
        work_id: 作品ID（UUID格式）
        chapter_id: 章节ID（可选）

    Returns:
        上下文信息JSON

    @deprecated 请使用 get_writing_context(work_id=..., chapter_id=..., include="work,chapter,rag")
    """
    logger.warning("[get_context_tool] ⚠️ 此工具已废弃，请使用 get_writing_context")
    result_str = await get_writing_context.ainvoke({
        "work_id": work_id or "",
        "chapter_id": chapter_id,
        "include": "work,chapter,rag"
    })
    # 格式转换：转为原格式
    try:
        result = json.loads(result_str)
        converted = {
            "work_id": result.get("work_id"),
            "work_info": result.get("work_info", {}),
            "current_chapter": {},
            "related_context": result.get("rag_context", [])
        }
        # 转换章节信息
        chapters = result.get("chapters", [])
        if chapters:
            ch = chapters[0]
            converted["current_chapter"] = {
                "chapter_id": ch.get("id"),
                "title": ch.get("title"),
                "order": ch.get("order"),
                "content_preview": ch.get("content", "")[:1000],
                "word_count": ch.get("word_count")
            }
        return json.dumps(converted, ensure_ascii=False, indent=2)
    except:
        pass
    return result_str


# ==================== 世界观查询工具 ====================

@tool
async def get_worldview_summary(work_id: str) -> str:
    """[DEPRECATED] 获取作品的世界观摘要信息 - 请使用 get_writing_context 代替

    Args:
        work_id: 作品ID（UUID格式）

    Returns:
        世界观摘要JSON

    @deprecated 请使用 get_writing_context(work_id=..., include="worldview")
    """
    logger.warning("[get_worldview_summary] ⚠️ 此工具已废弃，请使用 get_writing_context")
    result_str = await get_writing_context.ainvoke({
        "work_id": work_id,
        "include": "worldview"
    })
    # 格式转换：转为原格式
    try:
        result = json.loads(result_str)
        worldview = result.get("worldview", {})
        converted = {
            "total": {
                "characters": len(worldview.get("characters", [])),
                "locations": len(worldview.get("locations", [])),
                "settings": len(worldview.get("settings", []))
            },
            "characters": worldview.get("characters", []),
            "locations": worldview.get("locations", []),
            "settings": worldview.get("settings", [])
        }
        return json.dumps(converted, ensure_ascii=False, indent=2)
    except:
        pass
    return result_str


# ==================== 聚合工具 ====================

@tool
async def get_writing_context(
    work_id: str,
    chapter_id: str = "",
    chapter_orders: str = "",
    user_id: str = "",
    include: Union[str, List[str]] = "work,chapter,worldview,style,rag",
    rag_query: str = "",
    rag_top_k: int = 5,
    use_cache: bool = True
) -> str:
    """获取创作上下文（一站式聚合工具）

    合并了 get_context_tool, read_chapter_tool, get_chapter_by_order_tool,
    get_worldview_summary, get_style_guidance_tool 的功能。

    Args:
        work_id: 作品ID（UUID格式，必需）
        chapter_id: 章节ID（UUID格式，可选，用于单章节读取）
        chapter_orders: 章节序号（支持 "1" / "1,2,3" / "1-5" / "1-5,7" / "-3"，可选）
        user_id: 用户ID（用于获取风格指导，可选）
        include: 包含的内容类型，逗号分隔（可选值：work,chapter,worldview,style,rag）
        rag_query: RAG检索查询（可选，默认自动生成）
        rag_top_k: RAG返回数量（默认5）
        use_cache: 是否使用章节缓存（默认True）

    Returns:
        JSON格式的创作上下文

    使用示例:
        # 续写前获取完整上下文
        get_writing_context(work_id="xxx", chapter_orders="5", include="work,chapter,worldview,style,rag")

        # 只获取章节内容
        get_writing_context(work_id="xxx", chapter_orders="1-5", include="chapter")

        # 只获取世界观
        get_writing_context(work_id="xxx", include="worldview")
    """
    if not work_id:
        return json.dumps({
            "error": "缺少必需参数",
            "missing": "work_id",
            "message": "需要指定作品ID"
        }, ensure_ascii=False, indent=2)

    uuid_error = validate_uuid(work_id, "作品ID")
    if uuid_error:
        return uuid_error

    # 解析 include 参数
    include_value = include
    if isinstance(include_value, (list, tuple, set)):
        include_value = ",".join([str(i).strip() for i in include_value if str(i).strip()])
    include_value = include_value or "work,chapter,worldview,style,rag"
    include_set = set(i.strip() for i in str(include_value).split(",") if i.strip())

    result = {"work_id": work_id}

    async with AsyncSessionLocal() as db:
        try:
            from app.services.work_service import WorkService
            from app.services.worldview_service import WorldviewService
            from app.services.chapter_vector_service import ChapterVectorService
            from app.utils.text_cleaner import text_cleaner
            from app.utils.chapter_file_storage import chapter_storage

            work_service = WorkService(db)
            work = None

            # 预先获取 work（避免重复查询）
            if "work" in include_set or "chapter" in include_set:
                work = await _retry_on_failure(
                    work_service.get_work_by_id, work_id, use_cache=use_cache, max_retries=2
                )
                # 检查 work 是否存在
                if not work:
                    return json.dumps({
                        "error": "作品不存在",
                        "work_id": work_id,
                        "message": f"未找到ID为 {work_id} 的作品"
                    }, ensure_ascii=False, indent=2)

            # 1. 获取作品信息
            if "work" in include_set and work:
                result["work_info"] = {
                    "id": str(work.id),
                    "title": work.title,
                    "description": work.description[:300] if work.description else "",
                    "genre": work.genre if hasattr(work, 'genre') else "",
                    "total_chapters": len(work.chapters) if work.chapters else 0
                }

            # 2. 获取章节内容
            if "chapter" in include_set:
                chapters = []

                # 优先使用 chapter_orders（支持范围格式）
                if chapter_orders and work and work.chapters:
                    chapter_map = {ch.order: ch for ch in work.chapters}
                    available_orders = sorted(chapter_map.keys())
                    orders, ignored_parts, used_fallback = _parse_chapter_orders(
                        chapter_orders,
                        available_orders=available_orders
                    )
                    missing_orders = []
                    selected_chapters = []

                    for order in orders:
                        ch = chapter_map.get(order)
                        if ch:
                            selected_chapters.append(ch)
                        else:
                            missing_orders.append(order)

                    content_limit = _get_content_limit_for_batch(len(selected_chapters))

                    for ch in selected_chapters:
                        min_mtime = ch.updated_at.timestamp() if ch.updated_at else None
                        raw_content = chapter_storage.read_content(
                            str(ch.work_id), str(ch.id), min_mtime=min_mtime
                        )
                        if raw_content is None:
                            raw_content = ch.content if ch.content else ""
                        clean_content = text_cleaner.html_to_clean_text(
                            raw_content,
                            preserve_structure=True,
                            max_length=content_limit
                        )
                        if raw_content and len(raw_content) > content_limit:
                            clean_content = (
                                f"{clean_content}\n\n"
                                f"[内容已截断，完整内容共 {len(raw_content)} 字]"
                            )
                        chapters.append({
                            "id": str(ch.id),
                            "title": ch.title,
                            "order": ch.order,
                            "content": clean_content,
                            "word_count": ch.word_count
                        })

                    orders_info = {}
                    if ignored_parts:
                        orders_info["ignored_parts"] = ignored_parts
                    if missing_orders:
                        orders_info["missing_orders"] = missing_orders
                    if used_fallback:
                        orders_info["fallback_order"] = 1
                    if orders_info:
                        result["chapter_orders_info"] = orders_info

                # 使用 chapter_id（单章节）
                elif chapter_id:
                    from app.services.chapter_service import ChapterService
                    chapter_service = ChapterService(db)
                    resolved_id, resolve_error = await resolve_chapter_id(work_id, chapter_id)
                    if resolve_error:
                        return resolve_error
                    if resolved_id:
                        ch = await chapter_service.get_chapter_by_id(resolved_id)
                        if ch:
                            clean_content = text_cleaner.html_to_clean_text(
                                ch.content if ch.content else "",
                                preserve_structure=True
                            )
                            chapters.append({
                                "id": str(ch.id),
                                "title": ch.title,
                                "order": ch.order,
                                "content": clean_content,
                                "word_count": ch.word_count
                            })

                result["chapters"] = chapters

            # 3. 获取世界观
            if "worldview" in include_set:
                worldview_service = WorldviewService(db)
                characters = await worldview_service.get_characters_by_work(work_id)
                locations = await worldview_service.get_locations_by_work(work_id)
                settings = await worldview_service.get_settings_by_work(work_id)

                result["worldview"] = {
                    "characters": [
                        {"name": c.name, "description": c.description[:200] if c.description else ""}
                        for c in characters
                    ],
                    "locations": [
                        {"name": l.name, "description": l.description[:200] if l.description else ""}
                        for l in locations
                    ],
                    "settings": [
                        {
                            "name": s.title,
                            "description": s.content[:200] if s.content else "",
                            "title": s.title,
                            "content": s.content[:200] if s.content else ""
                        }
                        for s in settings
                    ]
                }

            # 4. 获取风格指导
            if "style" in include_set and user_id:
                from app.services.agent.tools.style_learning import get_style_prompt
                result["style_guidance"] = get_style_prompt(user_id)

            # 5. RAG检索
            if "rag" in include_set:
                chapter_vector_service = ChapterVectorService(db)
                current_order = None

                # 确定当前章节序号
                if result.get("chapters"):
                    current_order = result["chapters"][-1].get("order")

                query = rag_query or "作品背景、人物关系、情节发展"
                rag_results = await chapter_vector_service.retrieve_for_writing(
                    work_id=work_id,
                    current_chapter_order=current_order,
                    query=query,
                    top_k=rag_top_k
                )

                result["rag_context"] = [
                    {
                        "chapter_order": r.get("chapter_order"),
                        "chapter_title": r.get("chapter_title", ""),
                        "content": r.get("chunk_text", "")[:500],
                        "relevance": round(r.get("similarity", 0), 2)
                    }
                    for r in rag_results
                ]

            logger.info(f"[get_writing_context] ✅ 获取创作上下文成功: include={include}")
            return json.dumps(result, ensure_ascii=False, indent=2)

        except Exception as e:
            logger.error(f"[get_writing_context] 获取创作上下文失败: {e}", exc_info=True)
            return json.dumps({
                "error": "获取创作上下文失败",
                "message": str(e)
            }, ensure_ascii=False, indent=2)


# ==================== 段落精确读取工具 ====================

@tool
async def read_paragraph(
    work_id: str,
    chapter_order: int,
    paragraph_index: int,
    chapter_id: str = "",
    context_before: int = 2,
    context_after: int = 2
) -> str:
    """精确读取段落原文 + 上下文

    根据搜索结果的位置信息，精确读取指定段落及其前后上下文原文。
    用于验证搜索结果片段的完整含义。

    Args:
        work_id: 作品ID（UUID格式，必需）
        chapter_order: 章节序号（1-based，必需）
        paragraph_index: 段落索引（0-based，必需）
        chapter_id: 章节ID（可选，优先于 chapter_order）
        context_before: 向前读取段落数（默认2）
        context_after: 向后读取段落数（默认2）

    Returns:
        JSON格式的段落原文列表

    使用示例:
        # 读取第3章第18段及前后2段
        read_paragraph(work_id="xxx", chapter_order=3, paragraph_index=18)

        # 读取第5章第7段及前后5段上下文
        read_paragraph(work_id="xxx", chapter_order=5, paragraph_index=7, context_before=5, context_after=5)
    """
    if not work_id:
        return json.dumps({
            "success": False,
            "error": "缺少必需参数 work_id"
        }, ensure_ascii=False, indent=2)

    uuid_error = validate_uuid(work_id, "作品ID")
    if uuid_error:
        return uuid_error

    # 大章节保护
    MAX_CHAPTER_SIZE = 200_000  # 200K 字符

    async with AsyncSessionLocal() as db:
        try:
            from app.services.work_service import WorkService
            from app.services.chapter_service import ChapterService
            from app.services.agent.tools.locate_tools import _split_paragraphs

            chapter = None
            if chapter_id:
                chapter_svc = ChapterService(db)
                chapter = await chapter_svc.get_chapter_by_id(chapter_id)
                if not chapter:
                    return json.dumps({
                        "success": False,
                        "error": f"章节ID不存在: {chapter_id}"
                    }, ensure_ascii=False, indent=2)
                if work_id and str(chapter.work_id) != str(work_id):
                    return json.dumps({
                        "success": False,
                        "error": "chapter_id 与 work_id 不匹配"
                    }, ensure_ascii=False, indent=2)
                chapter_order = chapter.order
                if not work_id:
                    work_id = str(chapter.work_id)

            work = None
            if chapter is None:
                work_service = WorkService(db)
                work = await work_service.get_work_by_id(work_id, use_cache=True)

                if not work:
                    return json.dumps({
                        "success": False,
                        "error": f"作品 {work_id} 不存在"
                    }, ensure_ascii=False, indent=2)

                if not work.chapters:
                    return json.dumps({
                        "success": False,
                        "error": "作品没有章节"
                    }, ensure_ascii=False, indent=2)

                # 按序号查找章节
                chapter_map = {ch.order: ch for ch in work.chapters}
                chapter = chapter_map.get(chapter_order)

            if not chapter:
                available_orders = sorted(chapter_map.keys())
                return json.dumps({
                    "success": False,
                    "error": f"章节序号 {chapter_order} 不存在",
                    "available_orders": available_orders[:10]  # 只显示前10个
                }, ensure_ascii=False, indent=2)

            # 2026-01-17: 检查缓存（已解析章节）
            from app.services.agent.utils.tool_cache import ToolCache
            cached_result = ToolCache.get_paragraph_cache(
                work_id=work_id,
                chapter_order=chapter_order,
                paragraph_index=paragraph_index,
                context_before=context_before,
                context_after=context_after
            )
            if cached_result:
                logger.info(f"[read_paragraph] 缓存命中: 第{chapter_order}章第{paragraph_index}段")
                return cached_result

            from app.services.chapter_content_provider import ChapterContentProvider
            content_provider = ChapterContentProvider()
            content = content_provider.read_content(str(chapter.work_id), str(chapter.id)) or ""

            # 大章节分块处理
            if len(content) > MAX_CHAPTER_SIZE:
                # 估算目标位置，只解析附近 10K 字符
                avg_para_len = 500
                start_pos = max(0, paragraph_index * avg_para_len - 5000)
                end_pos = min(len(content), paragraph_index * avg_para_len + 5000)
                content = content[start_pos:end_pos]
                # 调整索引
                paragraph_index = min(paragraph_index, 10)

            # 复用现有段落解析（支持 HTML 和纯文本）
            paragraphs = _split_paragraphs(content)

            if not paragraphs:
                return json.dumps({
                    "success": False,
                    "error": "章节内容为空或无法解析段落"
                }, ensure_ascii=False, indent=2)

            if paragraph_index >= len(paragraphs):
                return json.dumps({
                    "success": False,
                    "error": f"段落索引 {paragraph_index} 超出范围",
                    "total_paragraphs": len(paragraphs),
                    "valid_range": f"0-{len(paragraphs) - 1}"
                }, ensure_ascii=False, indent=2)

            # 计算范围
            start_idx = max(0, paragraph_index - context_before)
            end_idx = min(len(paragraphs), paragraph_index + context_after + 1)

            # 构建结果
            result_paragraphs = []
            target_text = ""
            target_node_id = None
            for i in range(start_idx, end_idx):
                para = paragraphs[i]
                result_paragraphs.append({
                    "index": i,
                    "text": para["text"],
                    "is_target": i == paragraph_index
                })
                if i == paragraph_index:
                    target_text = para["text"]
                    target_node_id = para.get("node_id")

            result = json.dumps({
                "success": True,
                # 🔧 新增字段：方便规划层直接使用
                "content": target_text,                    # 目标段落文本（别名）
                "paragraph_index": paragraph_index,        # 段落索引
                "node_id": target_node_id,                 # 节点ID（如果有）
                "chapter_id": str(chapter.id) if chapter.id else "",
                # 原有字段
                "work_id": work_id,
                "chapter_order": chapter_order,
                "chapter_title": chapter.title,
                "paragraphs": result_paragraphs,
                "target_index": paragraph_index,
                "total_paragraphs_in_chapter": len(paragraphs)
            }, ensure_ascii=False, indent=2)

            # 2026-01-17: 写入缓存
            ToolCache.set_paragraph_cache(
                work_id=work_id,
                chapter_order=chapter_order,
                paragraph_index=paragraph_index,
                value=result,
                context_before=context_before,
                context_after=context_after
            )
            logger.info(f"[read_paragraph] 缓存写入: 第{chapter_order}章第{paragraph_index}段")

            return result

        except Exception as e:
            logger.error(f"read_paragraph 失败: {e}")
            return json.dumps({
                "success": False,
                "error": "读取段落失败",
                "message": str(e)
            }, ensure_ascii=False, indent=2)


# ==================== 章节清单工具 ====================

@tool
async def list_chapters(
    work_id: str
) -> str:
    """列出作品章节清单（只读）

    Args:
        work_id: 作品ID（UUID格式，必需）

    Returns:
        JSON格式章节清单（含 paragraph_count）
    """
    if not work_id and not chapter_id:
        return json.dumps({
            "success": False,
            "error": "缺少必需参数 work_id 或 chapter_id"
        }, ensure_ascii=False, indent=2)

    if work_id:
        uuid_error = validate_uuid(work_id, "作品ID")
        if uuid_error:
            return uuid_error

    async with AsyncSessionLocal() as db:
        try:
            from app.services.chapter_service import ChapterService
            from app.services.chapter_content_provider import ChapterContentProvider
            from app.services.agent.tools.locate_tools import _split_paragraphs
            chapter_svc = ChapterService(db)
            chapters = await chapter_svc.get_chapters_by_work(work_id)
            content_provider = ChapterContentProvider()
            result = []
            for ch in chapters or []:
                content = content_provider.read_content(str(ch.work_id), str(ch.id)) or ""
                paragraph_count = len(_split_paragraphs(content)) if content else 0
                result.append({
                    "chapter_id": str(ch.id) if ch.id else "",
                    "id": str(ch.id) if ch.id else "",
                    "order": ch.order,
                    "title": ch.title or "",
                    "word_count": getattr(ch, "word_count", 0) or 0,
                    "paragraph_count": paragraph_count
                })
            result.sort(key=lambda x: x.get("order") or 0)
            return json.dumps({
                "success": True,
                "work_id": work_id,
                "count": len(result),
                "chapters": result
            }, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"list_chapters 失败: {e}")
            return json.dumps({
                "success": False,
                "error": "读取章节清单失败",
                "message": str(e)
            }, ensure_ascii=False, indent=2)


# ==================== 段落清单工具 ====================

@tool
async def list_paragraphs(
    work_id: str,
    chapter_order: int = 0,
    chapter_id: str = "",
    offset: int = 0,
    limit: int = 50,
    preview_len: int = 80
) -> str:
    """列出章节段落索引（只读，支持 offset/limit）

    Args:
        work_id: 作品ID（UUID格式，必需）
        chapter_order: 章节序号（优先）
        chapter_id: 章节ID（可选）
        offset: 起始段落索引（默认0）
        limit: 返回段落数量（默认50）
        preview_len: 预览长度（默认80）

    Returns:
        JSON格式段落清单
    """
    if not work_id:
        return json.dumps({
            "success": False,
            "error": "缺少必需参数 work_id"
        }, ensure_ascii=False, indent=2)

    uuid_error = validate_uuid(work_id, "作品ID")
    if uuid_error:
        return uuid_error
    if chapter_id:
        uuid_error = validate_uuid(chapter_id, "章节ID")
        if uuid_error:
            return uuid_error

    if limit <= 0:
        limit = 1
    if offset < 0:
        offset = 0

    MAX_CHAPTER_SIZE = 200_000

    async with AsyncSessionLocal() as db:
        try:
            from app.services.work_service import WorkService
            from app.services.chapter_service import ChapterService
            from app.services.agent.tools.locate_tools import _split_paragraphs
            from app.services.chapter_content_provider import ChapterContentProvider

            chapter = None
            if chapter_id:
                chapter_svc = ChapterService(db)
                chapter = await chapter_svc.get_chapter_by_id(chapter_id)
                if chapter:
                    chapter_order = chapter.order
            if chapter is None:
                work_service = WorkService(db)
                work = await work_service.get_work_by_id(work_id, use_cache=True)
                if not work or not work.chapters:
                    return json.dumps({
                        "success": False,
                        "error": "作品没有章节"
                    }, ensure_ascii=False, indent=2)
                chapter_map = {ch.order: ch for ch in work.chapters}
                chapter = chapter_map.get(chapter_order)
            if not chapter:
                return json.dumps({
                    "success": False,
                    "error": f"章节不存在: order={chapter_order} id={chapter_id}"
                }, ensure_ascii=False, indent=2)

            content_provider = ChapterContentProvider()
            content = content_provider.read_content(str(chapter.work_id), str(chapter.id)) or ""
            if len(content) > MAX_CHAPTER_SIZE:
                return json.dumps({
                    "success": False,
                    "error": "章节过大，无法列出全部段落",
                    "message": "请改用 exact_search_paragraphs + read_paragraph",
                    "chapter_order": chapter.order
                }, ensure_ascii=False, indent=2)

            paragraphs = _split_paragraphs(content)
            total = len(paragraphs)
            end = min(total, offset + limit)
            sliced = []
            for i in range(offset, end):
                para = paragraphs[i]
                text = para.get("text", "")
                sliced.append({
                    "index": para.get("index", i),
                    "preview": text[:preview_len] + ("..." if len(text) > preview_len else ""),
                    "node_id": para.get("node_id") or ""
                })

            return json.dumps({
                "success": True,
                "work_id": work_id,
                "chapter_id": str(chapter.id) if chapter.id else "",
                "chapter_order": chapter.order,
                "chapter_title": chapter.title or "",
                "total_paragraphs": total,
                "offset": offset,
                "limit": limit,
                "paragraphs": sliced
            }, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"list_paragraphs 失败: {e}")
            return json.dumps({
                "success": False,
                "error": "读取段落清单失败",
                "message": str(e)
            }, ensure_ascii=False, indent=2)


# ==================== 批量段落读取工具 ====================

@tool
async def read_paragraphs(
    work_id: str,
    items: List[Dict[str, Any]],
    context_before: int = 2,
    context_after: int = 2
) -> str:
    """批量读取段落原文

    Args:
        work_id: 作品ID（UUID格式，必需）
        items: 段落列表 [{"chapter_order": 3, "paragraph_index": 18}, ...]
        context_before: 默认前文段落数
        context_after: 默认后文段落数

    Returns:
        JSON格式段落原文列表
    """
    if not work_id:
        return json.dumps({
            "success": False,
            "error": "缺少必需参数 work_id"
        }, ensure_ascii=False, indent=2)

    uuid_error = validate_uuid(work_id, "作品ID")
    if uuid_error:
        return uuid_error

    if not isinstance(items, list) or not items:
        return json.dumps({
            "success": False,
            "error": "items 不能为空"
        }, ensure_ascii=False, indent=2)

    results = []
    errors = 0
    for item in items:
        if not isinstance(item, dict):
            errors += 1
            continue
        chapter_order = item.get("chapter_order") or item.get("chapter")
        paragraph_index = item.get("paragraph_index") or item.get("paragraph")
        if isinstance(chapter_order, str) and chapter_order.isdigit():
            chapter_order = int(chapter_order)
        if isinstance(paragraph_index, str) and paragraph_index.isdigit():
            paragraph_index = int(paragraph_index)
        if not isinstance(chapter_order, int) or not isinstance(paragraph_index, int):
            errors += 1
            continue
        cb = item.get("context_before", context_before)
        ca = item.get("context_after", context_after)
        try:
            result = await read_paragraph.ainvoke({
                "work_id": work_id,
                "chapter_order": chapter_order,
                "paragraph_index": paragraph_index,
                "context_before": cb,
                "context_after": ca
            })
            result_data = json.loads(result) if isinstance(result, str) else result
            results.append(result_data)
        except Exception as e:
            errors += 1
            results.append({
                "success": False,
                "error": str(e),
                "chapter_order": chapter_order,
                "paragraph_index": paragraph_index
            })

    return json.dumps({
        "success": True,
        "work_id": work_id,
        "count": len(results),
        "errors": errors,
        "results": results
    }, ensure_ascii=False, indent=2)

# ==================== 工具列表 ====================

# 导入编辑器工具
from app.services.agent.tools.editor_tools import (
    smart_continue,
    smart_rewrite,
    smart_insert,
    apply_chapter_edit
)

# 导入章节管理工具
from app.services.agent.tools.chapter_tools import (
    delete_chapter,
    update_chapter_content
)

# 导入统一操作工具（2026-01-23）
from app.services.agent.tools.operate_tools import operate_apply

# 导入辅助工具（2026-01-09）
from app.services.agent.tools.consistency_checker import check_story_consistency_tool
from app.services.agent.tools.show_dont_tell import show_emotion_tool, enhance_scene_tool
from app.services.agent.tools.style_learning import learn_style_tool, get_style_guidance_tool, analyze_style_tool

# 导入探索工具（2026-01-17）
from app.services.agent.tools.explore_tools import explore_content

LANGGRAPH_TOOLS = [
    # 统一信息获取入口（2026-01-18 更新）
    explore_content,  # 深度探索 - 替代 search_content 和 get_writing_context
    # 分析工具
    analyze_content,
    # 创作工具
    smart_continue,
    smart_rewrite,
    smart_insert,
    show_emotion_tool,
    enhance_scene_tool,
    learn_style_tool,
    # 操作工具（统一入口）
    operate_apply,
    delete_chapter,
    update_chapter_content,
    # 内部工具（不暴露给 AI 规划器，但保留以供 explore_content 内部调用）
    # search_content,      # 内部工具
    # get_writing_context, # 内部工具
    # read_paragraph,      # 内部工具
]

__all__ = [
    # 全局服务管理
    "set_global_ai_service",
    "get_global_ai_service",
    # 辅助函数
    "validate_uuid",
    "is_chapter_order",
    "resolve_chapter_id",
    "_retry_on_failure",
    "_generate_text_helper",
    # 写作工具
    "analyze_text_tool",
    "analyze_content",
    # 章节工具
    "read_chapter_tool",
    "get_chapter_by_order_tool",
    "search_content",
    "search_analysis_fragments_tool",
    "get_context_tool",
    # 世界观工具
    "get_worldview_summary",
    # 聚合工具（2026-01-12）
    "get_writing_context",
    # 段落读取工具（2026-01-17）
    "read_paragraph",
    # 探索工具（2026-01-17）
    "explore_content",
    # 工具列表
    "LANGGRAPH_TOOLS",
    # StandardTool 版本（2025-12-14）
    "get_context_tool_st",
    "read_chapter_tool_st",
    "get_chapter_by_order_tool_st",
    "search_content_tool_st",
    "search_analysis_fragments_tool_st",
    "get_worldview_summary_tool_st",
]


# ==================== 2025-12-14: StandardTool 包装版本 ====================
# 为章节工具创建 StandardTool 包装，以支持元数据驱动和执行监控

from app.services.agent.tools.tool_types import ToolInput, ToolOutput, ToolCategory, StandardTool
from pydantic import Field


# ==================== 1. GetContextTool StandardTool ====================

class GetContextInput(ToolInput):
    """获取上下文工具输入"""
    work_id: str = Field(..., description="作品ID")
    chapter_id: str = Field(default="", description="章节ID（可选）")


class GetContextOutput(ToolOutput):
    """获取上下文工具输出"""
    pass


async def get_context_executor(input_data: GetContextInput) -> GetContextOutput:
    """获取上下文执行器（包装 @tool 版本）"""
    try:
        # 🔧 2025-12-14: @tool 装饰器返回 StructuredTool，需要用 .ainvoke() 调用
        result_str = await get_context_tool.ainvoke({
            "work_id": input_data.work_id,
            "chapter_id": input_data.chapter_id
        })

        return GetContextOutput(
            success=True,
            message="获取上下文成功",
            data={"context": result_str},
            metadata={"tool": "get_context"}
        )
    except Exception as e:
        logger.error(f"get_context_executor 失败: {e}")
        return GetContextOutput(
            success=False,
            message=f"获取上下文失败: {str(e)}",
            data=None,
            metadata={"error": str(e)}
        )


get_context_tool_st = StandardTool(
    name="get_context",
    description="获取作品上下文信息（世界观、人物设定等）",
    category=ToolCategory.UTILITY,
    input_schema=GetContextInput,
    output_schema=GetContextOutput,
    executor=get_context_executor,
    tags=["chapter", "context", "memory"],
    version="1.0.0"
)


# ==================== 2. ReadChapterTool StandardTool ====================

class ReadChapterInput(ToolInput):
    """读取章节工具输入"""
    work_id: str = Field(..., description="作品ID")
    chapter_id: str = Field(default="", description="章节ID（可多个，用逗号分隔）")


class ReadChapterOutput(ToolOutput):
    """读取章节工具输出"""
    pass


async def read_chapter_executor(input_data: ReadChapterInput) -> ReadChapterOutput:
    """读取章节执行器（包装 @tool 版本）"""
    try:
        # 🔧 2025-12-14: @tool 装饰器返回 StructuredTool，需要用 .ainvoke() 调用
        result_str = await read_chapter_tool.ainvoke({
            "work_id": input_data.work_id,
            "chapter_id": input_data.chapter_id
        })

        return ReadChapterOutput(
            success=True,
            message="读取章节成功",
            data={"chapter_info": result_str},
            metadata={"tool": "read_chapter"}
        )
    except Exception as e:
        logger.error(f"read_chapter_executor 失败: {e}")
        return ReadChapterOutput(
            success=False,
            message=f"读取章节失败: {str(e)}",
            data=None,
            metadata={"error": str(e)}
        )


read_chapter_tool_st = StandardTool(
    name="read_chapter",
    description="读取指定章节内容，支持单章或多章（逗号分隔）",
    category=ToolCategory.UTILITY,
    input_schema=ReadChapterInput,
    output_schema=ReadChapterOutput,
    executor=read_chapter_executor,
    tags=["chapter", "read"],
    version="1.0.0"
)


# ==================== 3. GetChapterByOrderTool StandardTool ====================

class GetChapterByOrderInput(ToolInput):
    """按序号获取章节工具输入

    🔧 2025-12-25: 更新 chapter_order 为 str 类型，支持批量格式
    """
    work_id: str = Field(..., description="作品ID")
    chapter_order: str = Field(default="1", description="章节序号，支持: 单个'1', 多个'1,2,3', 范围'1-5'")


class GetChapterByOrderOutput(ToolOutput):
    """按序号获取章节工具输出"""
    pass


async def get_chapter_by_order_executor(input_data: GetChapterByOrderInput) -> GetChapterByOrderOutput:
    """按序号获取章节执行器（包装 @tool 版本）

    🔧 2025-12-25: 支持批量读取格式
    """
    try:
        # 🔧 2025-12-14: @tool 装饰器返回 StructuredTool，需要用 .ainvoke() 调用
        result_str = await get_chapter_by_order_tool.ainvoke({
            "work_id": input_data.work_id,
            "chapter_order": input_data.chapter_order
        })

        return GetChapterByOrderOutput(
            success=True,
            message=f"获取章节成功: {input_data.chapter_order}",
            data={"chapter_info": result_str},
            metadata={"tool": "get_chapter_by_order", "chapter_order": input_data.chapter_order}
        )
    except Exception as e:
        logger.error(f"get_chapter_by_order_executor 失败: {e}")
        return GetChapterByOrderOutput(
            success=False,
            message=f"获取章节失败: {str(e)}",
            data=None,
            metadata={"error": str(e)}
        )


get_chapter_by_order_tool_st = StandardTool(
    name="get_chapter_by_order",
    description="按章节序号获取章节内容（支持批量：'1-5' 或 '1,2,3'）",
    category=ToolCategory.UTILITY,
    input_schema=GetChapterByOrderInput,
    output_schema=GetChapterByOrderOutput,
    executor=get_chapter_by_order_executor,
    tags=["chapter", "read", "order", "batch"],
    version="2.0.0"  # 🔧 2025-12-25: 升级版本号，支持批量读取
)


# ==================== 4. SearchAnalysisFragmentsTool StandardTool ====================

class SearchAnalysisFragmentsInput(ToolInput):
    """检索分析碎片工具输入"""
    work_id: str = Field(..., description="作品ID（必需）")
    query: str = Field(..., description="查询文本（必需）")
    top_k: int = Field(default=5, description="返回前K个最相关结果", ge=1, le=20)
    chapter_id: str = Field(default="", description="当前章节ID（可选）")
    include_current: bool = Field(default=True, description="是否包含当前章")
    look_ahead: int = Field(default=0, description="允许向后看的章节数（0表示不限制）", ge=0)
    max_content_length: int = Field(default=200, description="返回片段长度上限", ge=100, le=10000)


class SearchAnalysisFragmentsOutput(ToolOutput):
    """检索分析碎片工具输出"""
    pass


async def search_analysis_fragments_executor(input_data: SearchAnalysisFragmentsInput) -> SearchAnalysisFragmentsOutput:
    """检索分析碎片执行器（包装 @tool 版本）"""
    try:
        # 🔧 2025-12-14: @tool 装饰器返回 StructuredTool，需要用 .ainvoke() 调用
        result_str = await search_analysis_fragments_tool.ainvoke({
            "work_id": input_data.work_id,
            "query": input_data.query,
            "top_k": input_data.top_k,
            "chapter_id": input_data.chapter_id,
            "include_current": input_data.include_current,
            "look_ahead": input_data.look_ahead,
            "max_content_length": input_data.max_content_length
        })

        return SearchAnalysisFragmentsOutput(
            success=True,
            message="检索成功",
            data={"fragments": result_str},
            metadata={"tool": "search_analysis_fragments", "query": input_data.query}
        )
    except Exception as e:
        logger.error(f"search_analysis_fragments_executor 失败: {e}")
        return SearchAnalysisFragmentsOutput(
            success=False,
            message=f"检索失败: {str(e)}",
            data=None,
            metadata={"error": str(e)}
        )


search_analysis_fragments_tool_st = StandardTool(
    name="search_analysis_fragments",
    description="混合检索（向量+全文）召回作品相关片段",
    category=ToolCategory.UTILITY,
    input_schema=SearchAnalysisFragmentsInput,
    output_schema=SearchAnalysisFragmentsOutput,
    executor=search_analysis_fragments_executor,
    tags=["chapter", "search", "analysis"],
    version="1.0.0"
)


# ==================== 5. SearchContentTool StandardTool ====================

class SearchContentInput(ToolInput):
    """搜索内容工具输入"""
    work_id: str = Field(..., description="作品ID（必需）")
    query: str = Field(..., description="查询文本（必需）")
    top_k: int = Field(default=10, description="返回前K个最相关结果", ge=1, le=50)
    chapter_id: str = Field(default="", description="当前章节ID（可选）")
    look_ahead: int = Field(default=0, description="允许向后看的章节数（0表示不限制）", ge=0)


class SearchContentOutput(ToolOutput):
    """搜索内容工具输出"""
    pass


async def search_content_executor(input_data: SearchContentInput) -> SearchContentOutput:
    """搜索内容执行器（包装 @tool 版本）"""
    try:
        result_str = await search_content.ainvoke({
            "work_id": input_data.work_id,
            "query": input_data.query,
            "top_k": input_data.top_k,
            "chapter_id": input_data.chapter_id,
            "look_ahead": input_data.look_ahead
        })

        return SearchContentOutput(
            success=True,
            message="搜索成功",
            data={"results": result_str},
            metadata={"tool": "search_content", "query": input_data.query}
        )
    except Exception as e:
        logger.error(f"search_content_executor 失败: {e}")
        return SearchContentOutput(
            success=False,
            message=f"搜索失败: {str(e)}",
            data=None,
            metadata={"error": str(e)}
        )


search_content_tool_st = StandardTool(
    name="search_content",
    description="搜索多个相关位置，返回位置+片段（snippet）",
    category=ToolCategory.UTILITY,
    input_schema=SearchContentInput,
    output_schema=SearchContentOutput,
    executor=search_content_executor,
    tags=["chapter", "search", "snippet"],
    version="1.0.0"
)


# ==================== 6. GetWorldviewSummaryTool StandardTool ====================

class GetWorldviewSummaryInput(ToolInput):
    """获取世界观摘要工具输入"""
    work_id: str = Field(..., description="作品ID")


class GetWorldviewSummaryOutput(ToolOutput):
    """获取世界观摘要工具输出"""
    pass


async def get_worldview_summary_executor(input_data: GetWorldviewSummaryInput) -> GetWorldviewSummaryOutput:
    """获取世界观摘要执行器（包装 @tool 版本）"""
    try:
        result_str = await get_worldview_summary.ainvoke({
            "work_id": input_data.work_id
        })

        return GetWorldviewSummaryOutput(
            success=True,
            message="获取世界观摘要成功",
            data={"worldview_summary": result_str},
            metadata={"tool": "get_worldview_summary"}
        )
    except Exception as e:
        logger.error(f"get_worldview_summary_executor 失败: {e}")
        return GetWorldviewSummaryOutput(
            success=False,
            message=f"获取世界观摘要失败: {str(e)}",
            data=None,
            metadata={"error": str(e)}
        )


get_worldview_summary_tool_st = StandardTool(
    name="get_worldview_summary",
    description="获取作品的世界观摘要信息（角色、地点、设定）",
    category=ToolCategory.UTILITY,
    input_schema=GetWorldviewSummaryInput,
    output_schema=GetWorldviewSummaryOutput,
    executor=get_worldview_summary_executor,
    tags=["worldview", "summary", "context"],
    version="1.0.0"
)


# ==================== 6. GetWritingContextTool StandardTool (2026-01-12) ====================

class GetWritingContextInput(ToolInput):
    """获取创作上下文工具输入"""
    work_id: str = Field(..., description="作品ID")
    chapter_id: str = Field(default="", description="章节ID（可选）")
    chapter_orders: str = Field(default="", description="章节序号，支持批量：1 / 1,2,3 / 1-5")
    user_id: str = Field(default="", description="用户ID（用于获取风格）")
    include: Union[str, List[str]] = Field(default="work,chapter,worldview,style,rag", description="包含内容类型")
    rag_query: str = Field(default="", description="RAG检索查询")
    rag_top_k: int = Field(default=5, description="RAG返回数量")
    use_cache: bool = Field(default=True, description="是否使用缓存")


class GetWritingContextOutput(ToolOutput):
    """获取创作上下文工具输出"""
    pass


async def get_writing_context_executor(input_data: GetWritingContextInput) -> GetWritingContextOutput:
    """获取创作上下文执行器（包装 @tool 版本）"""
    try:
        result_str = await get_writing_context.ainvoke({
            "work_id": input_data.work_id,
            "chapter_id": input_data.chapter_id,
            "chapter_orders": input_data.chapter_orders,
            "user_id": input_data.user_id,
            "include": input_data.include,
            "rag_query": input_data.rag_query,
            "rag_top_k": input_data.rag_top_k,
            "use_cache": input_data.use_cache
        })

        context_data = result_str
        if isinstance(result_str, str):
            try:
                context_data = json.loads(result_str)
            except Exception:
                context_data = result_str

        return GetWritingContextOutput(
            success=True,
            message="获取创作上下文成功",
            data={"context": context_data},
            metadata={"tool": "get_writing_context"}
        )
    except Exception as e:
        logger.error(f"get_writing_context_executor 失败: {e}")
        return GetWritingContextOutput(
            success=False,
            message=f"获取创作上下文失败: {str(e)}",
            data=None,
            metadata={"error": str(e)}
        )


get_writing_context_tool_st = StandardTool(
    name="get_writing_context",
    description="一站式获取创作上下文（章节、世界观、RAG等）",
    category=ToolCategory.UTILITY,
    input_schema=GetWritingContextInput,
    output_schema=GetWritingContextOutput,
    executor=get_writing_context_executor,
    tags=["chapter", "context", "worldview", "rag"],
    version="1.0.0"
)

