"""
LangGraph Agent 工作流实现

使用 LangGraph 框架实现智能写作助手，支持：
- 4个核心场景（写作/规划/分析/卡文）
- 工具调用（HTTPAIService集成）
- 记忆管理（Checkpointer）
- 人机协同（HITL）
"""

from typing import TypedDict, Annotated, List, Dict, Any, Optional, Literal
from datetime import datetime
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from app.services.agent.parallel_tool_node import ParallelToolNode
from langgraph.checkpoint.redis import AsyncRedisSaver
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
import operator
import logging
import httpx
import uuid
import asyncio
import redis
import json
import re

from app.services.ai.http_ai_service import HTTPAIService
from app.core.config import settings
from app.core.database import AsyncSessionLocal
from app.services.agent.prompts import NovelPhase, PhaseCharacteristics
from app.services.agent.prompt_library import get_content_prompt
from app.services.agent.model_selector import TaskType
from app.services.agent.prompt_cache import get_tool_decision_static_prompt, get_planning_static_prompt

logger = logging.getLogger(__name__)


# ==================== State 定义 ====================

class AgentState(TypedDict):
    """Agent 状态定义"""
    messages: Annotated[List[Any], operator.add]  # 对话历史
    work_id: Optional[str]  # 作品ID
    chapter_id: Optional[str]  # 章节ID
    intent: Optional[str]  # 用户意图
    context: Dict[str, Any]  # 上下文信息
    agent_steps: Annotated[List[Dict[str, Any]], operator.add]  # Agent执行步骤
    suggested_actions: Annotated[List[str], operator.add]  # 建议操作
    final_response: Optional[str]  # 最终响应


# ==================== UUID 验证 ====================

# 标准UUID格式正则表达式
UUID_PATTERN = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', re.IGNORECASE)

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
            "example": "627feba4-2097-4f28-a3f3-7641d10f7f40",
            "suggestion": "请使用get_context_tool获取章节列表，或使用get_chapter_by_order_tool通过章节序号查询"
        }, ensure_ascii=False, indent=2)

    return None


# ==================== 工具定义 ====================

# 全局 AI Service 实例（用于工具调用）
_global_ai_service: Optional[HTTPAIService] = None

def set_global_ai_service(ai_service: HTTPAIService):
    """设置全局 AI Service"""
    global _global_ai_service
    _global_ai_service = ai_service


async def _retry_on_failure(func, *args, max_retries=3, **kwargs):
    """通用重试包装器：用于数据库操作等可能失败的操作

    Args:
        func: 要执行的异步函数
        max_retries: 最大重试次数
        *args, **kwargs: 传递给func的参数

    Returns:
        函数执行结果
    """
    import asyncio
    retry_count = 0

    while retry_count < max_retries:
        try:
            result = await func(*args, **kwargs)
            return result
        except Exception as e:
            retry_count += 1
            logger.error(f"[Retry] {func.__name__} 失败 (尝试 {retry_count}/{max_retries}): {e}")

            if retry_count >= max_retries:
                raise  # 重试次数用尽，抛出异常

            # 指数退避
            await asyncio.sleep(2 ** retry_count)

    raise Exception(f"{func.__name__} 失败，已重试{max_retries}次")


async def _with_timeout_and_retry(
    coro,
    timeout_seconds: int = 300,
    max_retries: int = 2,
    operation_name: str = "Operation",
    retry_on_timeout: bool = False
):
    """
    为协程添加超时保护和重试机制

    Args:
        coro: 要执行的协程
        timeout_seconds: 超时时间（秒）
        max_retries: 最大重试次数（不包括首次尝试）
        operation_name: 操作名称（用于日志）
        retry_on_timeout: 是否在超时后重试（默认False，超时直接抛出）

    Returns:
        协程执行结果

    Raises:
        asyncio.TimeoutError: 超时
        Exception: 其他异常
    """
    retry_count = 0

    # ✅ P0-3: 修复循环条件（<= 改为 <，避免多执行一次）
    while retry_count < max_retries + 1:
        try:
            # 添加超时保护
            async with asyncio.timeout(timeout_seconds):
                result = await coro
                return result

        except asyncio.TimeoutError:
            logger.error(f"[Timeout] {operation_name} 超时（{timeout_seconds}秒），尝试 {retry_count + 1}/{max_retries + 1}")

            if not retry_on_timeout or retry_count >= max_retries:
                # 不重试或已达最大重试次数
                raise

            retry_count += 1
            await asyncio.sleep(2 ** retry_count)  # 指数退避

        except Exception as e:
            logger.error(f"[Error] {operation_name} 失败：{e}，尝试 {retry_count + 1}/{max_retries + 1}")

            if retry_count >= max_retries:
                raise

            retry_count += 1
            await asyncio.sleep(2 ** retry_count)

    raise Exception(f"{operation_name} 失败，已重试{max_retries}次")


async def _generate_text_helper(
    prompt: str,
    temperature: float = 0.7,
    max_tokens: int = 1000,
    task_type: Optional[TaskType] = None  # ← 新增参数
) -> str:
    """辅助函数：使用 HTTPAIService 生成文本（带重试机制）"""
    if not _global_ai_service:
        return "错误：AI服务未初始化"

    messages = [{"role": "user", "content": prompt}]
    generated_text = ""
    max_retries = 3
    retry_count = 0

    while retry_count < max_retries:
        try:
            # ✅ 为单次LLM调用添加超时保护（120秒，匹配_generate_text）
            async with asyncio.timeout(120):
                async for chunk, _ in _global_ai_service._stream_chat(
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    task_type=task_type  # ← 传递task_type参数
                ):
                    if chunk:
                        generated_text += chunk

            # 成功生成内容，退出循环
            if generated_text:
                return generated_text

            # 如果没有生成内容，重试
            retry_count += 1
            logger.warning(f"[_generate_text_helper] 生成文本为空，重试 {retry_count}/{max_retries}")

        except asyncio.TimeoutError:
            retry_count += 1
            logger.error(f"[_generate_text_helper] 生成超时（120秒）(尝试 {retry_count}/{max_retries})")

            if retry_count >= max_retries:
                return f"错误：AI服务调用超时，已重试{max_retries}次"

            # 等待后重试（指数退避）
            await asyncio.sleep(2 ** retry_count)

        except Exception as e:
            retry_count += 1
            logger.error(f"[_generate_text_helper] 生成失败 (尝试 {retry_count}/{max_retries}): {e}")

            if retry_count >= max_retries:
                return f"错误：AI服务调用失败，已重试{max_retries}次。错误信息：{str(e)}"

            # 等待后重试（指数退避）
            await asyncio.sleep(2 ** retry_count)

    return generated_text or "错误：生成内容为空"


@tool
async def continue_writing_tool(context: str, requirements: str = "") -> str:
    """续写工具：根据上下文续写内容

    Args:
        context: 已有的文本上下文
        requirements: 续写要求（可选）

    Returns:
        续写后的文本
    """
    prompt = f"""你是专业的小说续写助手。请直接续写小说内容，不要给建议或提问！

上下文：
{context}

续写要求：{requirements if requirements else '保持原有风格，情节自然连贯，字数500-800字'}

重要：请直接输出续写的小说正文，不要输出任何说明文字、建议或问题。立即开始续写："""

    return await _generate_text_helper(
        prompt,
        temperature=0.8,
        max_tokens=2000,
        task_type=TaskType.CONTENT_CREATION  # ← 新增：续写任务
    )


@tool
async def polish_text_tool(text: str, style: str = "professional") -> str:
    """润色工具：优化文本质量

    Args:
        text: 待润色的文本
        style: 润色风格（professional/creative/concise）

    Returns:
        润色后的文本
    """
    prompt = f"""请润色以下文本，风格：{style}

原文：
{text}

请提供润色后的版本："""

    return await _generate_text_helper(
        prompt,
        temperature=0.7,
        max_tokens=2000,
        task_type=TaskType.TEXT_POLISH  # ← 新增：润色任务
    )


@tool
async def analyze_text_tool(text: str, focus: str = "all") -> str:
    """分析工具：分析文本问题（V2.0 - 防幻觉版）

    Args:
        text: 待分析的文本
        focus: 分析重点（all/grammar/logic/style）

    Returns:
        分析报告

    变更:
        - ✅ 使用结构化提示词模板（防幻觉）
        - ✅ 添加输出验证
        - ✅ 降低temperature从0.3到0.1
        - ✅ 验证失败时添加警告标记
        - ✅ 异步执行验证（不阻塞事件循环）
    """
    from app.prompts.constraint_manager import get_constraint_manager
    import asyncio

    try:
        # 1. 使用约束提示词管理器
        prompt_manager = get_constraint_manager()

        # 2. 格式化提示词（包含约束）
        prompt = prompt_manager.format_prompt(
            "analyze_text",
            text=text,
            focus=focus
        )

        # 3. 调用AI（降低创造性）
        result = await _generate_text_helper(
            prompt,
            temperature=0.1,  # ✅ 从0.3降到0.1，减少幻觉
            max_tokens=1500,
            task_type=TaskType.SUMMARIZATION
        )

        # 4. ✅ 异步验证输出（不阻塞事件循环）
        validation = await asyncio.to_thread(
            prompt_manager.validate_output,
            template_name="analyze_text",
            source_text=text,
            ai_output=result
        )

        # 5. ✅ 验证失败时的补救措施
        if not validation["valid"]:
            logger.warning(
                f"⚠️ AI输出验证失败: {validation.get('details', [])}"
            )

            # 添加警告标记到结果中
            warning_msg = "\n\n---\n⚠️ **注意**: 此分析可能包含不准确信息，请谨慎参考。\n"

            # 如果发现编造实体，列出来
            for detail in validation.get('details', []):
                if not detail['result'].get('valid', True):
                    fabricated = detail['result'].get('fabricated_entities', [])
                    if fabricated:
                        warning_msg += f"检测到可能编造的内容: {', '.join(fabricated[:5])}\n"

            result += warning_msg

        return result

    except Exception as e:
        # 降级方案：如果新系统失败，使用原来的简单提示词
        logger.error(f"约束提示词系统失败，使用降级方案: {e}")
        prompt = f"""请分析以下文本，重点关注：{focus}

文本：
{text}

请提供详细的分析报告："""

        return await _generate_text_helper(
            prompt,
            temperature=0.1,
            max_tokens=1500,
            task_type=TaskType.SUMMARIZATION
        )


@tool
async def read_chapter_tool(work_id: Optional[str] = None, chapter_id: str = "") -> str:
    """读取指定章节工具：从数据库读取章节内容（连接安全版本 v2）

    Args:
        work_id: 作品ID（可选，但强烈推荐提供），必须是标准UUID格式（36字符）
                 示例: c9dd9cbf-fa57-447e-9605-3020bbde5350
        chapter_id: 章节ID，必须是标准UUID格式（36字符），不能使用简化ID如"ch_1"
                    示例: 627feba4-2097-4f28-a3f3-7641d10f7f40
                    获取方式：从RAG检索结果、用户上下文或get_context_tool返回的章节列表中获取

    Returns:
        章节信息（包含标题和内容）的JSON字符串
    """
    # ✅ 优化：提前验证参数，避免不必要的数据库连接
    if not work_id:
        return json.dumps({
            "status": "missing_prerequisite",
            "missing": "work_id",
            "message": "需要指定作品ID才能读取章节",
            "user_action_required": True,
            "suggested_response": "请问您想读取哪个作品的章节？您可以在作品详情页使用此功能，或者告诉我作品ID。"
        }, ensure_ascii=False, indent=2)

    if not chapter_id:
        return json.dumps({
            "status": "missing_prerequisite",
            "missing": "chapter_id",
            "message": "需要指定章节ID才能读取章节",
            "user_action_required": True,
            "suggested_response": "请问您想读取第几章？或者告诉我章节ID。"
        }, ensure_ascii=False, indent=2)

    # UUID格式验证（提前返回，避免数据库连接）
    uuid_error = validate_uuid(work_id, "作品ID")
    if uuid_error:
        return uuid_error

    uuid_error = validate_uuid(chapter_id, "章节ID")
    if uuid_error:
        return uuid_error

    # ✅ 修复：正确使用 async with 管理连接
    async with AsyncSessionLocal() as db:
        try:
            from app.services.chapter_service import ChapterService

            chapter_service = ChapterService(db)

            # 使用重试机制（防止临时网络错误）
            chapter = await _retry_on_failure(
                chapter_service.get_chapter_by_id,
                chapter_id,
                max_retries=2
            )

            if not chapter:
                return json.dumps({
                    "error": f"未找到章节 {chapter_id}",
                    "work_id": work_id
                }, ensure_ascii=False, indent=2)

            # 返回章节信息
            chapter_info = {
                "chapter_id": str(chapter.id),
                "title": chapter.title,
                "order": chapter.order,
                "content": chapter.content[:5000] if chapter.content else "",
                "content_length": len(chapter.content) if chapter.content else 0,
                "word_count": chapter.word_count,
                "status": chapter.status.value if hasattr(chapter, 'status') else "unknown"
            }

            logger.info(f"[read_chapter_tool] ✅ 读取章节成功: {chapter.title}")
            return json.dumps(chapter_info, ensure_ascii=False, indent=2)

        except Exception as e:
            # ✅ 异常时回滚事务
            try:
                await db.rollback()
            except:
                pass

            logger.error(f"[read_chapter_tool] ❌ 读取章节失败: {e}", exc_info=True)
            return json.dumps({
                "error": f"读取章节失败: {str(e)}",
                "work_id": work_id,
                "chapter_id": chapter_id
            }, ensure_ascii=False, indent=2)

        finally:
            # ✅ 双重保险：确保连接关闭
            try:
                await db.close()
                logger.debug(f"[read_chapter_tool] 数据库连接已关闭")
            except Exception as close_error:
                logger.warning(f"[read_chapter_tool] 关闭数据库连接时出错: {close_error}")
                # 强制失效连接
                try:
                    await db.invalidate()
                except:
                    pass


@tool
async def get_chapter_by_order_tool(work_id: Optional[str] = None, chapter_order: int = 1) -> str:
    """通过章节序号获取章节ID和内容（连接安全版本 v2）

    Args:
        work_id: 作品ID（可选，但强烈推荐提供），必须是标准UUID格式（36字符）
                 示例: c9dd9cbf-fa57-447e-9605-3020bbde5350
        chapter_order: 章节序号（第1章=1，第2章=2，...）

    Returns:
        章节信息（包含ID、标题和内容）的JSON字符串
    """
    # ✅ 优化：提前验证参数
    if not work_id:
        return json.dumps({
            "status": "missing_prerequisite",
            "missing": "work_id",
            "message": "需要指定作品ID才能查询章节",
            "user_action_required": True,
            "suggested_response": "请问您想查询哪个作品的第{}章？您可以在作品详情页使用此功能，或者告诉我作品ID。".format(chapter_order)
        }, ensure_ascii=False, indent=2)

    # UUID格式验证（提前返回）
    uuid_error = validate_uuid(work_id, "作品ID")
    if uuid_error:
        return uuid_error

    # ✅ 修复：正确使用 async with 管理连接
    async with AsyncSessionLocal() as db:
        try:
            from app.services.work_service import WorkService
            from app.utils.text_cleaner import text_cleaner

            work_service = WorkService(db)

            # 使用重试机制获取作品
            work = await _retry_on_failure(
                work_service.get_work_by_id,
                work_id,
                use_cache=False,
                max_retries=2
            )

            if not work or not work.chapters:
                return json.dumps({
                    "error": f"未找到作品或作品没有章节",
                    "work_id": work_id
                }, ensure_ascii=False, indent=2)

            # 查找对应序号的章节
            target_chapter = None
            for chapter in work.chapters:
                if chapter.order == chapter_order:
                    target_chapter = chapter
                    break

            if not target_chapter:
                return json.dumps({
                    "error": f"未找到第{chapter_order}章",
                    "work_id": work_id,
                    "total_chapters": len(work.chapters)
                }, ensure_ascii=False, indent=2)

            # 返回章节信息（V2.0 - 添加HTML清理）
            clean_content = text_cleaner.html_to_clean_text(
                target_chapter.content if target_chapter.content else "",
                preserve_structure=True,
                max_length=5000
            )

            token_estimate = text_cleaner.estimate_tokens(clean_content)

            chapter_info = {
                "chapter_id": str(target_chapter.id),
                "title": target_chapter.title,
                "order": target_chapter.order,
                "content": clean_content,
                "content_length": len(clean_content),
                "word_count": target_chapter.word_count,
                "token_estimate": token_estimate,
                "status": target_chapter.status.value if hasattr(target_chapter, 'status') else "unknown"
            }

            logger.info(f"[get_chapter_by_order_tool] ✅ 找到第{chapter_order}章: {target_chapter.title}")
            return json.dumps(chapter_info, ensure_ascii=False, indent=2)

        except Exception as e:
            # ✅ 异常时回滚事务
            try:
                await db.rollback()
            except:
                pass

            logger.error(f"[get_chapter_by_order_tool] ❌ 查询失败: {e}", exc_info=True)
            return json.dumps({
                "error": f"查询失败: {str(e)}",
                "work_id": work_id,
                "chapter_order": chapter_order
            }, ensure_ascii=False, indent=2)

        finally:
            # ✅ 双重保险：确保连接关闭
            try:
                await db.close()
                logger.debug(f"[get_chapter_by_order_tool] 数据库连接已关闭")
            except Exception as close_error:
                logger.warning(f"[get_chapter_by_order_tool] 关闭数据库连接时出错: {close_error}")
                try:
                    await db.invalidate()
                except:
                    pass


@tool
async def search_analysis_fragments_tool(work_id: Optional[str] = None, query: str = "", top_k: int = 5) -> str:
    """检索分析碎片工具：从向量数据库检索相关的小说分析片段（RAG）（连接安全版本）

    Args:
        work_id: 作品ID（可选，但强烈推荐提供），必须是标准UUID格式（36字符）
                 示例: c9dd9cbf-fa57-447e-9605-3020bbde5350
                 不能使用简化ID如"YXTW_001"
        query: 查询文本（用户的问题或需求）
        top_k: 返回前K个最相关结果（默认5个）

    Returns:
        相关的分析片段列表（JSON格式）
    """
    # ✅ 优化：提前验证参数
    if not work_id:
        return json.dumps({
            "status": "missing_prerequisite",
            "missing": "work_id",
            "message": "需要指定作品ID才能检索分析片段",
            "user_action_required": True,
            "suggested_response": "请问您想检索哪个作品的分析内容？您可以在作品详情页使用此功能，或者告诉我作品ID。"
        }, ensure_ascii=False, indent=2)

    # UUID格式验证（提前返回）
    uuid_error = validate_uuid(work_id, "作品ID")
    if uuid_error:
        return uuid_error

    # ✅ 修复：正确使用 async with 管理连接
    async with AsyncSessionLocal() as db:
        try:
            from app.services.vector_store_service import VectorStoreService

            vector_service = VectorStoreService(db)

            # RAG检索（使用重试机制）
            results = await _retry_on_failure(
                vector_service.retrieve_relevant_analysis,
                work_id=work_id,
                query=query,
                top_k=top_k,
                similarity_threshold=0.3,
                max_retries=2
            )

            if not results:
                return json.dumps({
                    "message": "未找到相关的分析片段",
                    "work_id": work_id,
                    "query": query,
                    "results": []
                }, ensure_ascii=False, indent=2)

            # 格式化结果
            formatted_results = []
            for i, result in enumerate(results):
                formatted_results.append({
                    "rank": i + 1,
                    "similarity": result['similarity'],
                    "chapter_id": result['chapter_id'],
                    "content": result['content_text'][:2000],
                    "micro_data_summary": {
                        "theme": result['micro_data'].get('chapter_theme', 'N/A') if result['micro_data'] else 'N/A'
                    }
                })

            logger.info(f"[search_analysis_fragments_tool] ✅ RAG检索成功: 找到{len(results)}个相关片段")

            return json.dumps({
                "work_id": work_id,
                "query": query,
                "total_results": len(results),
                "results": formatted_results
            }, ensure_ascii=False, indent=2)

        except Exception as e:
            # ✅ 异常时回滚事务
            try:
                await db.rollback()
            except:
                pass

            logger.error(f"[search_analysis_fragments_tool] ❌ RAG检索失败: {e}", exc_info=True)
            return json.dumps({
                "error": f"检索失败: {str(e)}",
                "work_id": work_id,
                "query": query
            }, ensure_ascii=False, indent=2)

        finally:
            # ✅ 双重保险：确保连接关闭
            try:
                await db.close()
                logger.debug(f"[search_analysis_fragments_tool] 数据库连接已关闭")
            except Exception as close_error:
                logger.warning(f"[search_analysis_fragments_tool] 关闭数据库连接时出错: {close_error}")
                try:
                    await db.invalidate()
                except:
                    pass


@tool
async def get_context_tool(work_id: Optional[str] = None, chapter_id: str = "") -> str:
    """获取上下文工具：检索作品、章节和世界观信息（真实数据）（连接安全版本）

    Args:
        work_id: 作品ID（可选，但强烈推荐提供），必须是标准UUID格式（36字符）
                 示例: c9dd9cbf-fa57-447e-9605-3020bbde5350
        chapter_id: 章节ID（可选），必须是标准UUID格式（36字符）
                    示例: 627feba4-2097-4f28-a3f3-7641d10f7f40

    Returns:
        上下文信息（JSON格式字符串）
    """
    # ✅ 优化：提前验证参数
    if not work_id:
        return json.dumps({
            "status": "missing_prerequisite",
            "missing": "work_id",
            "message": "需要指定作品ID才能获取上下文",
            "user_action_required": True,
            "suggested_response": "请问您想查看哪个作品的信息？您可以在作品详情页使用此功能，或者告诉我作品ID。"
        }, ensure_ascii=False, indent=2)

    # UUID格式验证（提前返回）
    uuid_error = validate_uuid(work_id, "作品ID")
    if uuid_error:
        return uuid_error

    if chapter_id:  # chapter_id是可选的，只在提供时验证
        uuid_error = validate_uuid(chapter_id, "章节ID")
        if uuid_error:
            return uuid_error

    # ✅ 修复：正确使用 async with 管理连接
    async with AsyncSessionLocal() as db:
        try:
            from app.services.work_service import WorkService
            from app.services.chapter_service import ChapterService
            from app.services.vector_store_service import VectorStoreService

            logger.info(f"[get_context_tool] 🔥 新版本工具被调用！work_id={work_id}, chapter_id={chapter_id}")

            work_service = WorkService(db)
            chapter_service = ChapterService(db)
            vector_service = VectorStoreService(db)

            context_info = {
                "work_id": work_id,
                "work_info": {},
                "current_chapter": {},
                "related_analysis": []
            }

            # 1. 获取作品信息（使用重试机制）
            work = await _retry_on_failure(
                work_service.get_work_by_id,
                work_id,
                use_cache=False,
                max_retries=2
            )

            if work:
                context_info["work_info"] = {
                    "title": work.title,
                    "description": work.description[:200] if work.description else "",
                    "genre": work.genre if hasattr(work, 'genre') else "未知",
                    "total_chapters": len(work.chapters) if work.chapters else 0
                }
            else:
                context_info["work_info"] = {"error": "作品未找到"}

            # 2. 获取当前章节（如果提供了chapter_id）
            if chapter_id:
                chapter = await _retry_on_failure(
                    chapter_service.get_chapter_by_id,
                    chapter_id,
                    max_retries=2
                )

                if chapter:
                    context_info["current_chapter"] = {
                        "chapter_id": str(chapter.id),
                        "title": chapter.title,
                        "order": chapter.order,
                        "content_preview": chapter.content[:1000] if chapter.content else "",
                        "word_count": chapter.word_count
                    }
                else:
                    context_info["current_chapter"] = {"error": "章节未找到"}

            # 3. RAG检索相关分析（如果有）
            try:
                query = f"作品背景和设定"
                analysis_results = await _retry_on_failure(
                    vector_service.retrieve_relevant_analysis,
                    work_id=work_id,
                    query=query,
                    top_k=3,
                    similarity_threshold=0.4,
                    max_retries=2
                )

                if analysis_results:
                    context_info["related_analysis"] = [
                        {
                            "chapter_id": r['chapter_id'],
                            "similarity": r['similarity'],
                            "summary": r['content_text'][:500]
                        }
                        for r in analysis_results
                    ]
            except Exception as rag_error:
                logger.warning(f"RAG检索失败（非致命）: {rag_error}")
                context_info["related_analysis"] = []

            logger.info(f"[get_context_tool] ✅ 获取上下文成功: work={work.title if work else 'N/A'}")
            return json.dumps(context_info, ensure_ascii=False, indent=2)

        except Exception as e:
            # ✅ 异常时回滚事务
            try:
                await db.rollback()
            except:
                pass

            logger.error(f"[get_context_tool] ❌ 获取上下文失败: {e}", exc_info=True)
            return json.dumps({
                "error": f"获取上下文失败: {str(e)}",
                "work_id": work_id
            }, ensure_ascii=False, indent=2)

        finally:
            # ✅ 双重保险：确保连接关闭
            try:
                await db.close()
                logger.debug(f"[get_context_tool] 数据库连接已关闭")
            except Exception as close_error:
                logger.warning(f"[get_context_tool] 关闭数据库连接时出错: {close_error}")
                try:
                    await db.invalidate()
                except:
                    pass


# 工具列表
WRITING_TOOLS = [
    continue_writing_tool,
    polish_text_tool,
    analyze_text_tool,
    get_context_tool,
    read_chapter_tool,
    get_chapter_by_order_tool,  # 新增：通过章节序号获取章节
    search_analysis_fragments_tool
]


# ==================== Summarization上下文压缩工具 ====================

def _compress_task_result(
    task_id: int,
    task_description: str,
    task_result: str,
    max_length: int = 2000  # 提高默认限制，保留更多上下文
) -> str:
    """智能压缩任务结果

    Args:
        task_id: 任务ID
        task_description: 任务描述
        task_result: 原始任务结果
        max_length: 最大保留长度

    Returns:
        压缩后的结果
    """
    # 类型安全检查
    if not isinstance(task_result, str):
        logger.warning(
            f"[Compress] 任务{task_id}结果不是字符串: {type(task_result)}, "
            f"已转换为字符串"
        )
        task_result = str(task_result) if task_result is not None else ""

    # 如果结果很短，直接返回
    if len(task_result) <= max_length:
        return task_result

    # 【修复】尝试解析JSON格式的工具返回结果（如get_chapter_by_order_tool）
    try:
        data = json.loads(task_result)
        # 如果是JSON且有content字段，提取真正的内容
        if isinstance(data, dict) and 'content' in data:
            content = data.get('content')
            task_result = content if content is not None else ""
            # 重新检查长度
            if len(task_result) <= max_length:
                return task_result
    except (json.JSONDecodeError, TypeError, ValueError) as e:
        logger.debug(f"任务结果不是JSON格式: {e}")
        # 不是JSON或解析失败，继续原有逻辑

    # 章节内容：只保留摘要
    if "章" in task_result and ("第" in task_result or "标题" in task_result):
        lines = task_result.split('\n')
        summary_lines = []

        for line in lines[:10]:  # 只看前10行
            if "标题" in line or "章" in line or "摘要" in line:
                summary_lines.append(line)

        if summary_lines:
            compressed = '\n'.join(summary_lines)
            return f"[章节信息摘要]\n{compressed}\n[完整内容已压缩]"
        else:
            # 保留开头和结尾（增加保留长度）
            return f"[章节内容摘要]\n{task_result[:1500]}...\n{task_result[-500:]}"

    # RAG检索结果
    if "检索" in task_description or "搜索" in task_description:
        # 只保留关键信息
        return f"[检索结果摘要]\n{task_result[:max_length]}"

    # 其他类型结果：保留前后部分
    half = max_length // 2
    return f"{task_result[:half]}...[省略{len(task_result)-max_length}字符]...{task_result[-half:]}"


def _build_summarization_context(
    user_message: str,
    task_results: List[Dict[str, Any]],
    max_context_length: int = 3000
) -> str:
    """构建Summarization的压缩上下文

    Args:
        user_message: 用户原始请求
        task_results: 任务执行结果列表 [{"task_id": 1, "description": "...", "result": "...", "status": "completed"}, ...]
        max_context_length: 最大上下文长度（字符）

    Returns:
        压缩后的上下文字符串
    """
    context_parts = [f"用户请求：{user_message}\n\n执行结果："]
    current_length = len(context_parts[0])

    for task in task_results:
        task_id = task["task_id"]
        description = task["description"]
        result = task.get("result")
        result = result if result is not None else ""  # 防御性编程：处理None值
        status = task["status"]

        # 压缩结果
        if status == "completed":
            compressed_result = _compress_task_result(
                task_id=task_id,
                task_description=description,
                task_result=result,
                max_length=2000  # 提高压缩限制，保留更多上下文
            )
        else:
            # 失败的任务保留错误信息
            compressed_result = result[:200] if result else ""

        # 构建任务文本
        task_text = f"\n任务{task_id}（{description}）：\n{compressed_result}\n"

        # 检查是否超过限制
        if current_length + len(task_text) > max_context_length:
            # 超过限制，进一步简化
            task_text = f"\n任务{task_id}：[结果已省略]\n"

        context_parts.append(task_text)
        current_length += len(task_text)

        # 如果已经接近限制，停止添加
        if current_length >= max_context_length * 0.95:
            remaining_tasks = len(task_results) - (task_id)
            if remaining_tasks > 0:
                omit_msg = f"\n[还有{remaining_tasks}个任务结果已省略]\n"
                # 检查提示信息本身是否会超限
                if current_length + len(omit_msg) <= max_context_length:
                    context_parts.append(omit_msg)
            break

    return ''.join(context_parts)

# ==================================================================


# ==================== Agent 节点定义 ====================

class WritingAgentGraph:
    """
    LangGraph 写作 Agent - 支持双模式

    模式 1 (use_chatgpt=True): 使用 ChatOpenAI + 原生工具调用
    模式 2 (use_chatgpt=False): 使用 HTTPAIService + 手动工具调用（绕过 Cloudflare）
    """

    @classmethod
    async def setup_checkpointer(cls):
        """
        预创建AsyncRedisSaver索引（应用启动时调用）

        优化点: 避免首次请求时的21秒索引创建延迟
        """
        try:
            from app.core.config import settings
            redis_url = settings.REDIS_URL

            # 创建临时checkpointer实例用于预初始化
            ttl_config = {
                "default_ttl": 10080,  # 7天
                "refresh_on_read": False  # 禁用自动续期，减少Redis操作
            }

            # 测试Redis连接
            test_client = redis.Redis.from_url(redis_url, decode_responses=False)
            test_client.ping()
            test_client.close()

            # 创建并初始化checkpointer
            checkpointer = AsyncRedisSaver(redis_url=redis_url, ttl=ttl_config)
            await checkpointer.asetup()  # 预创建索引
            logger.info("[LangGraph] ✅ AsyncRedisSaver索引预创建成功")
        except Exception as e:
            logger.warning(f"[LangGraph] ⚠️ AsyncRedisSaver索引预创建失败: {e}")
            logger.warning("[LangGraph] 将在首次使用时自动创建索引")

    def __init__(self, ai_service: HTTPAIService, use_chatgpt: bool = False):
        """
        初始化 Agent

        Args:
            ai_service: HTTPAIService 实例
            use_chatgpt: 是否使用 ChatOpenAI（True=原生工具调用，False=手动工具调用）
        """
        self.ai_service = ai_service
        self.use_chatgpt = use_chatgpt  # 模式开关

        # 设置全局 AI Service（供工具使用）
        set_global_ai_service(ai_service)

        # 初始化上下文管理器（用于chat_stream的长对话管理）
        from app.services.context import ContextManager
        self.context_manager = ContextManager(
            ai_service=self.ai_service,  # 传入AI服务（用于LLM摘要）
            enable_long_term_memory=True  # 启用长期记忆
        )
        logger.info("[LangGraph] ✅ ContextManager已初始化（长期记忆已启用）")

        # 初始化Prompt管理器（用于统一管理各类Agent的Prompt模板）
        from app.prompts import get_prompt_manager
        self.prompt_manager = get_prompt_manager()
        logger.info("[LangGraph] ✅ PromptManager已初始化")

        # 根据模式初始化
        if use_chatgpt:
            logger.info("[LangGraph] 使用 ChatOpenAI 模式（原生工具调用）")
            self._init_chatgpt_mode()
        else:
            logger.info("[LangGraph] 使用 HTTPAIService 模式（手动工具调用，绕过 Cloudflare）")
            self.llm = None
            self.llm_with_tools = None

        # 创建 Checkpointer（记忆系统）
        # 使用 AsyncRedisSaver 替代 MemorySaver，解决内存泄漏和数据持久化问题
        try:
            # AsyncRedisSaver必须使用db0（RediSearch索引限制）
            # 使用checkpoint:前缀避免与缓存key冲突
            redis_url = settings.REDIS_URL  # 使用db0

            # 测试Redis连接
            test_client = redis.Redis.from_url(redis_url, decode_responses=False)
            test_client.ping()
            test_client.close()

            # AsyncRedisSaver支持异步操作，直接传递URL字符串
            # 配置TTL：7天自动清理不活跃对话
            ttl_config = {
                "default_ttl": 10080,  # 7天 = 7 * 24 * 60分钟
                "refresh_on_read": False  # 禁用自动续期（性能优化）
            }
            self.checkpointer = AsyncRedisSaver(redis_url=redis_url, ttl=ttl_config)
            self._checkpointer_setup_done = False  # 标记是否已初始化索引
            logger.info(f"[LangGraph] OK 使用 AsyncRedisSaver（{redis_url}，TTL=7天）")
        except Exception as e:
            logger.warning(f"[LangGraph] 警告 Redis连接失败，降级使用MemorySaver: {e}")
            # 降级方案：如果Redis不可用，使用MemorySaver
            from langgraph.checkpoint.memory import MemorySaver
            self.checkpointer = MemorySaver()
            self._checkpointer_setup_done = True  # MemorySaver不需要setup

        # 构建图
        self.graph = self._build_graph()

    def _init_chatgpt_mode(self):
        """初始化 ChatOpenAI 模式"""
        import httpx
        from app.api.callbacks import MonitoringCallbackHandler

        # 创建自定义 httpx 客户端（尝试绕过 Cloudflare）
        sync_http_client = httpx.Client(
            headers={
                "User-Agent": "okhttp/4.12.0",
                "Accept": "application/json",
                "Accept-Encoding": "gzip, deflate",
                "Connection": "keep-alive",
            },
            timeout=httpx.Timeout(120.0, connect=10.0),
            follow_redirects=True,
            http2=False,
        )

        async_http_client = httpx.AsyncClient(
            headers={
                "User-Agent": "okhttp/4.12.0",
                "Accept": "application/json",
                "Accept-Encoding": "gzip, deflate",
                "Connection": "keep-alive",
            },
            timeout=httpx.Timeout(120.0, connect=10.0),
            follow_redirects=True,
            http2=False,
        )

        # 🔧 监控：创建监控回调
        monitoring_callback = MonitoringCallbackHandler()
        logger.info("[LangGraph] 已创建MonitoringCallbackHandler")

        # 创建 LLM（附加监控回调）
        self.llm = ChatOpenAI(
            model=settings.OPENAI_MODEL,
            api_key=settings.OPENAI_API_KEY,
            base_url=settings.OPENAI_BASE_URL,
            temperature=0.7,
            request_timeout=120,  # ← 明确设置120秒超时，避免双重超时冲突
            http_client=sync_http_client,
            http_async_client=async_http_client,
            callbacks=[monitoring_callback]  # ← 添加监控回调
        )

        # 绑定工具（工具调用也会触发回调）
        self.llm_with_tools = self.llm.bind_tools(WRITING_TOOLS)

    def _build_graph(self) -> StateGraph:
        """
        构建 LangGraph 工作流

        完整工作流结构：
        START
          ↓
        intent_classifier (分类意图)
          ↓
        [条件路由]
          ├─> writing_agent (生成AIMessage + tool_calls)
          ├─> planning_agent (生成AIMessage + tool_calls)
          ├─> analysis_agent (生成AIMessage + tool_calls)
          ├─> stuck_agent (生成AIMessage + tool_calls)
          └─> general_chat (直接响应)
          ↓
        [条件判断: 是否需要工具?]
          ├─> YES → tools (ToolNode执行工具)
          └─> NO  → END
          ↓
        [工具执行后返回Agent]
          ↓
        Agent节点 (处理工具结果，生成最终响应)
          ↓
        END
        """

        # 创建图
        workflow = StateGraph(AgentState)

        # 添加节点
        workflow.add_node("intent_classifier", self._classify_intent)
        workflow.add_node("writing_agent", self._handle_writing)
        workflow.add_node("planning_agent", self._handle_planning)
        workflow.add_node("analysis_agent", self._handle_analysis)
        workflow.add_node("stuck_agent", self._handle_stuck)
        workflow.add_node("general_chat", self._handle_general)
        # 🟢 Phase 3.7: 使用ParallelToolNode替代标准ToolNode，支持并行执行
        workflow.add_node("tools", ParallelToolNode(
            WRITING_TOOLS,
            max_concurrent=5  # 最大并发数（基于数据库连接池大小）
        ))

        # 设置入口点
        workflow.set_entry_point("intent_classifier")

        # 添加条件边：根据意图路由到不同Agent
        workflow.add_conditional_edges(
            "intent_classifier",
            self._route_intent,
            {
                "writing": "writing_agent",
                "planning": "planning_agent",
                "analysis": "analysis_agent",
                "stuck": "stuck_agent",
                "general": "general_chat"
            }
        )

        # 各Agent节点添加条件边：判断是否需要调用工具
        for agent_node in ["writing_agent", "planning_agent", "analysis_agent", "stuck_agent"]:
            workflow.add_conditional_edges(
                agent_node,
                self._should_continue,
                {
                    "continue": "tools",  # 需要工具 → 执行工具
                    "end": END  # 不需要工具 → 结束
                }
            )

        # 工具执行后，根据意图返回对应的Agent节点（让Agent处理工具结果）
        workflow.add_conditional_edges(
            "tools",
            self._route_after_tools,
            {
                "writing": "writing_agent",
                "planning": "planning_agent",
                "analysis": "analysis_agent",
                "stuck": "stuck_agent"
            }
        )

        # 一般对话直接结束
        workflow.add_edge("general_chat", END)

        # 编译图
        return workflow.compile(checkpointer=self.checkpointer)

    def _should_continue(self, state: AgentState) -> Literal["continue", "end"]:
        """判断是否需要继续执行工具"""
        messages = state["messages"]
        last_message = messages[-1]

        # 如果最后一条消息是 AIMessage 且包含 tool_calls，则继续执行工具
        if isinstance(last_message, AIMessage) and last_message.tool_calls:
            logger.info(f"[LangGraph] 检测到工具调用: {len(last_message.tool_calls)} 个工具")
            return "continue"

        # 否则结束
        logger.info("[LangGraph] 无需工具调用，结束流程")
        return "end"

    def _route_after_tools(self, state: AgentState) -> str:
        """工具执行后路由回对应的Agent"""
        intent = state.get("intent", "general")
        logger.info(f"[LangGraph] 工具执行完毕，路由回: {intent}_agent")
        return intent

    async def _generate_text(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        task_type: Optional[TaskType] = None  # ← 新增参数
    ) -> dict:
        """生成文本的辅助方法（根据use_chatgpt选择使用ChatOpenAI或HTTPAIService）

        Args:
            prompt: 提示词
            temperature: 温度参数
            max_tokens: 最大token数
            task_type: 任务类型（用于模型选择）

        Returns:
            dict: {"text": str, "usage": dict}
        """
        from app.services.agent.utils.monitoring import increment_counter

        # ✅ P0-1: 添加120秒超时保护（匹配ChatOpenAI的request_timeout）
        try:
            async with asyncio.timeout(120):
                # 🔧 修复：根据use_chatgpt选择使用ChatOpenAI还是HTTPAIService
                if self.use_chatgpt:
                    # 模式1：使用ChatOpenAI（触发监控）
                    from langchain_core.messages import HumanMessage
                    messages = [HumanMessage(content=prompt)]

                    # 调用ChatOpenAI（会触发MonitoringCallbackHandler）
                    # ✅ 使用 bind() 动态绑定参数，确保 temperature 和 max_tokens 生效
                    llm_with_params = self.llm.bind(
                        temperature=temperature,
                        max_tokens=max_tokens
                    )
                    response = await llm_with_params.ainvoke(messages)

                    generated_text = response.content

                    # 提取token使用情况
                    usage = {}
                    if hasattr(response, 'response_metadata'):
                        token_usage = response.response_metadata.get('token_usage', {})
                        if token_usage:
                            usage = {
                                "prompt_tokens": token_usage.get('prompt_tokens', 0),
                                "completion_tokens": token_usage.get('completion_tokens', 0),
                                "total_tokens": token_usage.get('total_tokens', 0)
                            }

                    logger.info(f"[_generate_text] 使用ChatOpenAI生成文本，tokens={usage.get('total_tokens', 0)}")

                    return {
                        "text": generated_text,
                        "usage": usage
                    }
                else:
                    # 模式2：使用HTTPAIService（兼容模式）
                    messages = [{"role": "user", "content": prompt}]

                    generated_text = ""
                    usage = None

                    async for chunk, chunk_usage in self.ai_service._stream_chat(
                        messages=messages,
                        max_tokens=max_tokens,
                        temperature=temperature,
                        task_type=task_type  # ← 传递task_type
                    ):
                        if chunk:
                            generated_text += chunk
                        if chunk_usage:
                            usage = chunk_usage

                    logger.info(f"[_generate_text] 使用HTTPAIService生成文本，tokens={usage.get('total_tokens', 0) if usage else 0}")

                    return {
                        "text": generated_text,
                        "usage": usage or {}
                    }

        except asyncio.TimeoutError:
            # 超时处理
            mode = "ChatOpenAI" if self.use_chatgpt else "HTTPAIService"
            logger.error(f"[_generate_text] {mode} LLM调用超时（120秒）")
            increment_counter("generate_text_error", labels={"error_type": "TimeoutError", "mode": mode})

            # 返回错误结果
            return {
                "text": f"抱歉，AI响应超时（超过120秒）。请稍后重试。",
                "usage": {},
                "error": "timeout"
            }

        except Exception as e:
            # 其他异常处理
            mode = "ChatOpenAI" if self.use_chatgpt else "HTTPAIService"
            logger.error(f"[_generate_text] {mode} LLM调用失败: {e}", exc_info=True)
            increment_counter("generate_text_error", labels={"error_type": type(e).__name__, "mode": mode})

            # 返回错误结果
            return {
                "text": f"抱歉，AI服务调用失败：{str(e)}",
                "usage": {},
                "error": str(e)
            }

    def _classify_intent_by_rules(self, message: str) -> tuple[str, float]:
        """基于规则的快速意图识别（<1ms）

        Args:
            message: 用户消息内容

        Returns:
            tuple[str, float]: (intent类型, 置信度)
        """
        msg = message.lower()

        # 1. 写作：续写、扩写、生成内容
        writing_keywords = ["续写", "扩写", "第", "章", "生成内容", "创作", "写作", "继续写", "完成"]
        if any(kw in msg for kw in writing_keywords):
            # 章节特征强相关
            if re.search(r'第\d+章|chapter\s*\d+', msg, re.IGNORECASE):
                return "writing", 0.98
            return "writing", 0.90

        # 2. 规划：大纲、世界观、设定
        planning_keywords = ["规划", "大纲", "世界观", "设定", "角色", "背景", "剧情", "框架", "结构"]
        if any(kw in msg for kw in planning_keywords):
            return "planning", 0.95

        # 3. 分析：评估、诊断、检查
        analysis_keywords = ["分析", "评估", "诊断", "检查", "质量", "评价", "看看", "怎么样", "如何"]
        if any(kw in msg for kw in analysis_keywords):
            return "analysis", 0.93

        # 4. 卡文：灵感、写不下去
        stuck_keywords = ["卡文", "灵感", "写不下去", "没思路", "瓶颈", "困难", "卡住", "不知道"]
        if any(kw in msg for kw in stuck_keywords):
            return "stuck", 0.95

        # 5. 默认：一般对话
        return "general", 0.85

    async def _classify_intent(self, state: AgentState) -> AgentState:
        """意图分类节点 - 使用规则识别"""
        logger.info("[LangGraph] 意图分类（规则识别）")

        last_message = state["messages"][-1].content

        # 使用规则快速识别
        intent, confidence = self._classify_intent_by_rules(last_message)

        logger.info(
            f"[Intent] 规则识别结果: {intent}, 置信度: {confidence:.2f}"
        )

        # ✅ 只返回节点新增/修改的字段，避免 operator.add 重复添加
        return {
            "intent": intent,
            "agent_steps": [{
                "step": "intent_classification",
                "result": f"识别意图: {intent} (规则识别)",
                "usage": {}  # 无Token消耗
            }]
        }

    def _route_intent(self, state: AgentState) -> str:
        """路由决策函数"""
        intent = state.get("intent", "general")
        logger.info(f"[LangGraph] 路由到: {intent}")
        return intent

    async def _handle_agent_with_tools(self, state: AgentState, agent_type: str, system_prompt: str) -> AgentState:
        """
        通用的Agent处理逻辑 - 支持双模式

        模式 1: ChatOpenAI 原生工具调用
        模式 2: HTTPAIService 手动工具调用
        """
        logger.info(f"[LangGraph] 处理{agent_type}场景 (use_chatgpt={self.use_chatgpt})")

        if self.use_chatgpt:
            # 模式 1: 使用 ChatOpenAI 原生工具调用
            return await self._handle_with_chatgpt(state, agent_type, system_prompt)
        else:
            # 模式 2: 使用 HTTPAIService 手动工具调用
            return await self._handle_with_httpai(state, agent_type, system_prompt)

    async def _handle_with_chatgpt(self, state: AgentState, agent_type: str, system_prompt: str) -> AgentState:
        """ChatOpenAI 模式 - 原生工具调用"""
        messages = state["messages"]

        # 检查是否已经有工具结果（第二次进入）
        if messages and isinstance(messages[-1], ToolMessage):
            logger.info(f"[LangGraph] {agent_type} - 处理工具执行结果 (ChatOpenAI)")
            response = await self.llm.ainvoke(messages)
            # ✅ 只返回新消息，避免 operator.add 重复添加
            return {
                "messages": [response],
                "final_response": response.content,
                "agent_steps": [{
                    "step": f"{agent_type}_final_response",
                    "result": "基于工具结果生成最终响应 (ChatOpenAI)"
                }]
            }

        # 第一次进入：让 LLM 决定是否需要工具
        messages_with_system = [SystemMessage(content=system_prompt)] + messages
        response = await self.llm_with_tools.ainvoke(messages_with_system)

        # ✅ 只返回新消息，避免 operator.add 重复添加
        result = {
            "messages": [response],
            "agent_steps": [{
                "step": f"{agent_type}_decision",
                "result": f"LLM决策 (ChatOpenAI): {'调用工具' if response.tool_calls else '直接响应'}",
                "tool_calls": len(response.tool_calls) if response.tool_calls else 0
            }]
        }

        if not response.tool_calls:
            result["final_response"] = response.content

        return result

    async def _handle_with_httpai(self, state: AgentState, agent_type: str, system_prompt: str) -> AgentState:
        """HTTPAIService 模式 - 手动工具调用（绕过 Cloudflare）"""
        messages = state["messages"]

        # 检查是否已经有工具结果（第二次进入）
        if messages and isinstance(messages[-1], ToolMessage):
            logger.info(f"[LangGraph] {agent_type} - 处理工具执行结果 (HTTPAIService)")

            # 获取用户原始请求
            user_message = ""
            for msg in messages:
                if isinstance(msg, HumanMessage):
                    user_message = msg.content
                    break

            # 使用 HTTPAIService 基于工具结果生成最终响应
            tool_result = messages[-1].content

            logger.info(f"[LangGraph] 🔍 工具返回内容长度: {len(tool_result)} 字符")
            logger.info(f"[LangGraph] 🔍 工具返回内容预览:\n{tool_result[:500]}")

            # 判断用户意图：是想「查看/读取」内容，还是想「创作/续写」内容
            read_keywords = ["读", "看", "查看", "显示", "展示", "告诉我", "第几章", "内容是什么"]
            write_keywords = ["写", "续写", "创作", "生成", "继续", "扩写", "补充"]

            is_read_request = any(keyword in user_message for keyword in read_keywords)
            is_write_request = any(keyword in user_message for keyword in write_keywords)

            # 根据 agent_type 和用户实际意图定制响应方式
            if agent_type == "writing":
                # 如果用户明确想「读取/查看」内容
                if is_read_request and not is_write_request:
                    final_prompt = f"""{system_prompt}

用户请求：{user_message}

工具返回的真实数据（JSON格式）：
{tool_result}

【重要指令】
上面是从数据库读取的真实数据，包含作品信息、章节内容、分析片段等。

请按照以下格式清晰地展示给用户：

**作品信息**
- 标题：[从 work_info.title 获取]
- 描述：[从 work_info.description 获取]
- 章节总数：[从 work_info.total_chapters 获取]

**章节信息**
- 章节标题：[从 current_chapter.title 获取]
- 章节序号：第 [从 current_chapter.order 获取] 章
- 字数：[从 current_chapter.word_count 获取]

**章节内容**
[从 current_chapter.content_preview 或完整 content 获取，保持原文格式]

注意：
1. 所有信息必须来自上述JSON数据，不要编造
2. 如果某个字段为空或不存在，标注为"暂无"
3. 用清晰的markdown格式展示
4. 不要添加任何评论、分析或续写"""

                # 如果用户明确想「创作/续写」内容
                else:
                    final_prompt = f"""{system_prompt}

用户请求：{user_message}

工具提供的真实上下文数据（JSON格式）：
{tool_result}

【重要指令】
1. 上面的工具返回数据是从数据库读取的真实内容，包含：
   - 作品的真实标题、描述、类型
   - 章节的真实标题、序号、已有内容
   - 从向量数据库检索到的世界观、角色设定等分析片段

2. 你必须仔细阅读上述JSON数据，特别是：
   - current_chapter.content_preview（当前章节已有内容）
   - related_analysis（相关世界观和角色设定）
   - work_info（作品整体信息）

3. 创作续写时，必须：
   - 基于 current_chapter.content_preview 中的真实内容进行续写
   - 保持与已有内容的风格、人物、情节连贯
   - 参考 related_analysis 中的世界观和角色设定
   - 不要编造与上述数据矛盾的信息

4. 如果上述数据中某些字段为空或缺失，说明数据库中确实没有相关内容，此时可以合理发挥创作。

请直接开始续写内容（至少500字），不要重复说明你看到了什么数据。"""

            elif agent_type == "stuck":
                final_prompt = f"""{system_prompt}

用户遇到的问题：{user_message}

当前创作背景：
{tool_result}

请基于背景信息，给用户3-5个具体的创作方向建议，每个建议包含：
1. 方向概述
2. 可以这样写的理由
3. 示例开头（50字左右）"""

            elif agent_type == "planning":
                final_prompt = f"""{system_prompt}

用户需求：{user_message}

当前信息：
{tool_result}

请基于现有信息，提供详细的规划方案。"""

            else:  # analysis 或其他
                # 如果用户明确想「读取/查看」内容
                if is_read_request and not is_write_request:
                    final_prompt = f"""{system_prompt}

用户请求：{user_message}

工具返回的数据：
{tool_result}

请注意：用户想要「查看/读取」内容！
请直接整理并呈现工具返回的数据内容，用清晰易读的格式展示给用户。"""
                else:
                    final_prompt = f"""{system_prompt}

用户请求：{user_message}

分析材料：
{tool_result}

请基于材料，生成详细的分析报告。"""

            # 根据 agent_type 和用户意图智能选择 task_type
            if agent_type == "writing":
                # 写作场景：根据用户意图区分
                if is_read_request and not is_write_request:
                    selected_task_type = TaskType.SUMMARIZATION  # 展示数据
                else:
                    selected_task_type = TaskType.CONTENT_CREATION  # 续写创作
            elif agent_type == "stuck":
                selected_task_type = TaskType.SIMPLE_QA  # 提供建议
            elif agent_type == "planning":
                selected_task_type = TaskType.STORY_PLANNING  # 规划方案
            elif agent_type == "analysis":
                # 分析场景：根据复杂度区分
                if is_read_request and not is_write_request:
                    selected_task_type = TaskType.SUMMARIZATION  # 展示数据
                else:
                    selected_task_type = TaskType.DEEP_ANALYSIS  # 深度分析
            else:
                # 其他场景：默认摘要
                selected_task_type = TaskType.SUMMARIZATION

            logger.info(f"[LangGraph] {agent_type} 最终响应使用模型: task_type={selected_task_type.value}")

            # ✅ 使用 _generate_text 以支持 ChatOpenAI/HTTPAIService 双模式
            result = await self._generate_text(
                prompt=final_prompt,
                max_tokens=1500,
                temperature=0.7,
                task_type=selected_task_type  # 智能选择的task_type
            )
            final_text = result.get("text", "")

            response = AIMessage(content=final_text)
            # ✅ 只返回新消息，避免 operator.add 重复添加
            return {
                "messages": [response],
                "final_response": final_text,
                "agent_steps": [{
                    "step": f"{agent_type}_final_response",
                    "result": "基于工具结果生成最终响应 (HTTPAIService)"
                }]
            }

        # 第一次进入：使用 HTTPAIService 决定是否需要工具
        last_user_message = messages[-1].content

        # ✅ P0修复：改进AI决策Prompt，明确当前上下文
        current_work_id = state.get("work_id")
        current_chapter_id = state.get("chapter_id")

        # ✅ P2修复：显示实际的ID值（安全截断）
        def _format_id(value: Optional[str], max_len: int = 20) -> str:
            """格式化ID值，安全截断过长ID"""
            if not value:
                return "未设置"
            if len(value) <= max_len:
                return f"{value}"
            return f"{value[:max_len]}..."

        context_info = f"""
当前上下文：
- 作品ID (work_id): {_format_id(current_work_id)}
- 章节ID (chapter_id): {_format_id(current_chapter_id)}
"""

        # ✅ Phase 2.6: 使用缓存的静态 Prompt（节省构建时间和 Token）
        static_prompt = await get_tool_decision_static_prompt()

        decision_prompt = f"""{system_prompt}

用户: {last_user_message}
{context_info}

{static_prompt}"""

        # ✅ 使用 _generate_text 以支持 ChatOpenAI/HTTPAIService 双模式
        result = await self._generate_text(
            prompt=decision_prompt,
            max_tokens=200,  # ✅ Phase 2.5: 优化从500→200 (JSON响应通常<100 tokens)
            temperature=0.3,
            task_type=TaskType.SIMPLE_QA  # 工具决策任务
        )
        decision_text = result.get("text", "")

        # 解析决策
        import json
        import re

        logger.info(f"[LangGraph] AI 决策原文: {decision_text}")

        # 方法 1: 尝试直接解析整个文本（如果 AI 只返回 JSON）
        decision = None
        try:
            decision = json.loads(decision_text.strip())
            logger.info(f"[LangGraph] 方法1成功: 直接解析整个文本")
        except:
            pass

        # 方法 2: 使用正则提取 JSON（支持嵌套，贪婪匹配）
        if not decision:
            # 匹配 { ... } 包括嵌套的 JSON
            json_matches = re.finditer(r'\{(?:[^{}]|(?:\{[^}]*\}))*\}', decision_text)
            for match in json_matches:
                try:
                    candidate = json.loads(match.group())
                    # 验证是否包含必需字段
                    if "need_tools" in candidate:
                        decision = candidate
                        logger.info(f"[LangGraph] 方法2成功: 正则提取 JSON")
                        break
                except:
                    continue

        # 方法 3: 如果都失败，返回默认决策
        if not decision:
            logger.error(f"[LangGraph] 无法解析决策，原文: {decision_text[:200]}")
            decision = {
                "need_tools": False,
                "direct_response": "抱歉，我在理解您的请求时遇到了问题。能否更详细地描述一下？"
            }

        logger.info(f"[LangGraph] 最终决策: {decision}")

        logger.info(f"[LangGraph] {agent_type} 决策 (HTTPAIService): {decision.get('need_tools', False)}")

        if decision.get("need_tools", False):
            # 需要工具：手动调用
            tool_name = decision.get("tool_name", "continue_writing_tool")
            tool_args = decision.get("tool_args", {})

            # 标准化参数格式
            tool_args = self._normalize_tool_params(tool_name, tool_args)

            # 调用工具（使用 .ainvoke() 方法，因为 @tool 装饰器返回的是 StructuredTool 对象）
            tool_result = ""
            if tool_name == "continue_writing_tool":
                tool_result = await continue_writing_tool.ainvoke({
                    "context": tool_args.get("context", last_user_message),
                    "requirements": tool_args.get("requirements", "")
                })
            elif tool_name == "polish_text_tool":
                tool_result = await polish_text_tool.ainvoke({
                    "text": tool_args.get("text", last_user_message),
                    "style": tool_args.get("style", "professional")
                })
            elif tool_name == "analyze_text_tool":
                tool_result = await analyze_text_tool.ainvoke({
                    "text": tool_args.get("text", last_user_message),
                    "focus": tool_args.get("focus", "all")
                })
            elif tool_name == "get_context_tool":
                # ✅ P0修复：添加参数完整性检查
                work_id_value = state.get("work_id")
                if not work_id_value:
                    logger.warning(f"[LangGraph] ⚠️ get_context_tool 缺少必需参数 work_id")
                    tool_result = json.dumps({
                        "error": "missing_work_id",
                        "message": "需要提供作品ID才能获取上下文",
                        "user_prompt": "请先告诉我您要操作哪部作品？"
                    }, ensure_ascii=False)
                else:
                    logger.info(f"[LangGraph] 🚀 准备调用 get_context_tool, work_id={work_id_value}, chapter_id={state.get('chapter_id')}")
                    tool_result = await get_context_tool.ainvoke({
                        "work_id": work_id_value,
                        "chapter_id": state.get("chapter_id", "")
                    })
                    logger.info(f"[LangGraph] ✅ get_context_tool 返回结果长度: {len(tool_result)} 字符")
                    logger.info(f"[LangGraph] ✅ get_context_tool 返回内容预览: {tool_result[:200]}")
            elif tool_name == "read_chapter_tool":
                # ✅ P0修复：添加参数完整性检查
                work_id_value = state.get("work_id")
                if not work_id_value:
                    logger.warning(f"[LangGraph] ⚠️ read_chapter_tool 缺少必需参数 work_id")
                    tool_result = json.dumps({
                        "error": "missing_work_id",
                        "message": "需要提供作品ID才能读取章节",
                        "user_prompt": "请先告诉我您要读取哪部作品的章节？"
                    }, ensure_ascii=False)
                else:
                    tool_result = await read_chapter_tool.ainvoke({
                        "work_id": work_id_value,
                        "chapter_id": tool_args.get("chapter_id") or state.get("chapter_id") or ""
                    })
            elif tool_name == "get_chapter_by_order_tool":
                # ✅ P0修复：添加参数完整性检查
                work_id_value = state.get("work_id")
                if not work_id_value:
                    logger.warning(f"[LangGraph] ⚠️ get_chapter_by_order_tool 缺少必需参数 work_id")
                    tool_result = json.dumps({
                        "error": "missing_work_id",
                        "message": "需要提供作品ID才能查询章节",
                        "user_prompt": "请先告诉我您要查看哪部作品的章节？您可以说：\n- 「我想看《作品名》的第X章」\n- 或者先创建一部新作品"
                    }, ensure_ascii=False)
                else:
                    logger.info(f"[LangGraph] 🚀 准备调用 get_chapter_by_order_tool, work_id={work_id_value}, chapter_order={tool_args.get('chapter_order')}")
                    tool_result = await get_chapter_by_order_tool.ainvoke({
                        "work_id": work_id_value,
                        "chapter_order": tool_args.get("chapter_order", 1)
                    })
                    logger.info(f"[LangGraph] ✅ get_chapter_by_order_tool 返回结果长度: {len(tool_result)} 字符")
            elif tool_name == "search_analysis_fragments_tool":
                # ✅ P0修复：添加参数完整性检查
                work_id_value = state.get("work_id")
                if not work_id_value:
                    logger.warning(f"[LangGraph] ⚠️ search_analysis_fragments_tool 缺少必需参数 work_id")
                    tool_result = json.dumps({
                        "error": "missing_work_id",
                        "message": "需要提供作品ID才能搜索分析片段",
                        "user_prompt": "请先告诉我您要搜索哪部作品的分析片段？"
                    }, ensure_ascii=False)
                else:
                    tool_result = await search_analysis_fragments_tool.ainvoke({
                        "work_id": work_id_value,
                        "query": tool_args.get("query", last_user_message),
                        "top_k": tool_args.get("top_k", 5)
                    })
            else:
                # ✅ P1修复：未知工具返回标准JSON错误格式
                tool_result = json.dumps({
                    "error": "unknown_tool",
                    "message": f"未知工具: {tool_name}",
                    "user_prompt": "抱歉，我在处理您的请求时遇到了问题。能否换个方式描述？"
                }, ensure_ascii=False)
                logger.warning(f"[LangGraph] 尝试调用未知工具: {tool_name}")

            # ✅ 创建新消息（不直接修改 state，避免重复）
            ai_decision = AIMessage(content=f"我需要使用 {tool_name} 工具来帮助你。")
            tool_message = ToolMessage(content=tool_result, tool_call_id="manual_call")

            new_step = {
                "step": f"{agent_type}_tool_call",
                "result": f"调用工具 (HTTPAIService): {tool_name}",
                "tool_result_length": len(tool_result)
            }

            # ✅ 创建更新后的 state（不修改原 state）
            updated_state = state.copy()
            updated_state["messages"] = state["messages"] + [ai_decision, tool_message]
            updated_state["agent_steps"] = state["agent_steps"] + [new_step]

            # ✅ P0修复：检查工具是否返回错误，如果是错误则直接返回友好提示
            try:
                tool_result_obj = json.loads(tool_result)
                error_type = tool_result_obj.get("error")
                if error_type in ["missing_work_id", "unknown_tool"]:
                    logger.info(f"[LangGraph] 🎯 检测到工具错误({error_type})，直接返回友好提示")
                    direct_response = tool_result_obj.get("user_prompt", "请先告诉我您要操作哪部作品？")
                    return {
                        "messages": [AIMessage(content=direct_response)],
                        "final_response": direct_response,
                        "agent_steps": [{
                            "step": f"{agent_type}_{error_type}",
                            "result": f"检测到错误: {error_type}"
                        }]
                    }
            except json.JSONDecodeError:
                # 正常的工具返回结果，继续处理
                pass
            except Exception as e:
                logger.warning(f"[LangGraph] 解析工具结果异常: {e}")
                # 继续处理，不返回错误

            # ✅ P1修复：智能清理累积的消息，防止上下文无限增长
            current_messages = updated_state["messages"]
            message_count = len(current_messages)

            # 智能清理策略：根据消息数量动态调整
            if message_count > 8:  # 降低阈值，更早触发清理
                logger.info(f"[LangGraph] 🧹 智能清理累积消息：{message_count}条 -> ", end="")

                # 分类消息
                system_messages = []
                user_messages = []
                ai_messages = []
                tool_messages = []

                for msg in current_messages:
                    if isinstance(msg, SystemMessage):
                        system_messages.append(msg)
                    elif isinstance(msg, HumanMessage):
                        user_messages.append(msg)
                    elif isinstance(msg, AIMessage):
                        ai_messages.append(msg)
                    elif isinstance(msg, ToolMessage):
                        tool_messages.append(msg)

                # 智能保留策略：
                # 1. 保留所有系统消息（通常只有1条）
                # 2. 保留最近的1条用户消息（当前请求）
                # 3. 保留最近的2对AI-Tool交互（最多4条）
                # 总共最多保留: 1(system) + 1(user) + 4(ai+tool) = 6条

                cleaned_messages = system_messages.copy()

                # 保留最近的用户消息
                if user_messages:
                    cleaned_messages.append(user_messages[-1])

                # ✅ P2修复：智能成对保留最近的AI-Tool交互
                # 确保AI消息和Tool消息成对保留，避免破坏对话连贯性
                recent_pairs = []
                ai_idx = len(ai_messages) - 1
                tool_idx = len(tool_messages) - 1

                # 从最新的开始，成对保留最多2对交互（4条消息）
                pairs_count = 0
                while pairs_count < 2 and ai_idx >= 0 and tool_idx >= 0:
                    # 成对添加（先AI后Tool）
                    recent_pairs.insert(0, tool_messages[tool_idx])
                    recent_pairs.insert(0, ai_messages[ai_idx])
                    ai_idx -= 1
                    tool_idx -= 1
                    pairs_count += 1

                # 按原始顺序重组
                for msg in current_messages:
                    if msg in recent_pairs and msg not in cleaned_messages:
                        cleaned_messages.append(msg)

                updated_state["messages"] = cleaned_messages
                logger.info(f"保留{len(cleaned_messages)}条（压缩率{100 - len(cleaned_messages) * 100 // message_count}%）")
            else:
                logger.debug(f"[LangGraph] 消息数量{message_count}条，无需清理")

            # 递归处理工具结果
            result = await self._handle_with_httpai(updated_state, agent_type, system_prompt)

            # ✅ 返回所有新增的消息（工具调用消息 + 递归结果）
            # 注意：updated_state是局部变量，不会影响外部state
            # 所以需要在返回时包含ai_decision和tool_message
            return {
                "messages": [ai_decision, tool_message] + result.get("messages", []),
                "final_response": result.get("final_response"),
                "agent_steps": [new_step] + result.get("agent_steps", [])
            }

        else:
            # 不需要工具：直接响应
            direct_response = decision.get("direct_response", "抱歉，我无法处理您的请求。")
            response = AIMessage(content=direct_response)
            # ✅ 只返回新消息，避免 operator.add 重复添加
            return {
                "messages": [response],
                "final_response": direct_response,
                "agent_steps": [{
                    "step": f"{agent_type}_direct_response",
                    "result": "直接响应用户 (HTTPAIService)"
                }]
            }

    async def _handle_writing(self, state: AgentState) -> AgentState:
        """
        处理写作场景 - 使用新架构

        新架构流程：
        1. 使用WritingAction.prepare()准备参数
        2. 调用_handle_agent_with_tools统一处理（触发监控）
        """
        from app.services.agent.actions import WritingAction

        logger.info("[LangGraph] 处理写作请求（新架构）")

        # 1. 使用Action准备参数（业务逻辑）
        writing_action = WritingAction()  # 新架构不需要ai_service
        prep_result = await writing_action.prepare(state)

        # 2. 检查准备结果
        if not prep_result.success:
            logger.error(f"[LangGraph] WritingAction.prepare()失败: {prep_result.error}")
            from langchain_core.messages import AIMessage
            error_msg = AIMessage(content=f"抱歉，写作请求处理失败: {prep_result.error}")
            return {
                "messages": [error_msg],
                "final_response": error_msg.content,
                "agent_steps": [{
                    "step": "writing_error",
                    "result": f"准备失败: {prep_result.error}"
                }]
            }

        # 3. 记录业务信息
        logger.info(
            f"[LangGraph] WritingAction准备完成: "
            f"phase={prep_result.metadata.get('phase')}, "
            f"chapter_num={prep_result.metadata.get('chapter_num')}"
        )

        # 4. 统一使用框架调用LLM（触发监控）
        return await self._handle_agent_with_tools(
            state,
            agent_type=prep_result.metadata.get("agent_type", "writing"),
            system_prompt=prep_result.system_prompt
        )

    async def _handle_planning(self, state: AgentState) -> AgentState:
        """
        处理规划场景 - 使用新架构

        新架构流程：
        1. 使用PlanningAction.prepare()准备参数
        2. 调用_handle_agent_with_tools统一处理（触发监控）
        """
        from app.services.agent.actions import PlanningAction

        logger.info("[LangGraph] 处理规划请求（新架构）")

        # 1. 使用Action准备参数（业务逻辑）
        planning_action = PlanningAction()  # 新架构不需要ai_service
        prep_result = await planning_action.prepare(state)

        # 2. 检查准备结果
        if not prep_result.success:
            logger.error(f"[LangGraph] PlanningAction.prepare()失败: {prep_result.error}")
            from langchain_core.messages import AIMessage
            error_msg = AIMessage(content=f"抱歉，规划请求处理失败: {prep_result.error}")
            return {
                "messages": [error_msg],
                "final_response": error_msg.content,
                "agent_steps": [{
                    "step": "planning_error",
                    "result": f"准备失败: {prep_result.error}"
                }]
            }

        # 3. 统一使用框架调用LLM（触发监控）
        return await self._handle_agent_with_tools(
            state,
            agent_type=prep_result.metadata.get("agent_type", "planning"),
            system_prompt=prep_result.system_prompt
        )

    async def _handle_analysis(self, state: AgentState) -> AgentState:
        """
        处理分析场景 - 使用新架构

        新架构流程：
        1. 使用AnalysisAction.prepare()准备参数
        2. 调用_handle_agent_with_tools统一处理（触发监控）
        """
        from app.services.agent.actions import AnalysisAction

        logger.info("[LangGraph] 处理分析请求（新架构）")

        # 1. 使用Action准备参数（业务逻辑）
        analysis_action = AnalysisAction()  # 新架构不需要ai_service
        prep_result = await analysis_action.prepare(state)

        # 2. 检查准备结果
        if not prep_result.success:
            logger.error(f"[LangGraph] AnalysisAction.prepare()失败: {prep_result.error}")
            from langchain_core.messages import AIMessage
            error_msg = AIMessage(content=f"抱歉，分析请求处理失败: {prep_result.error}")
            return {
                "messages": [error_msg],
                "final_response": error_msg.content,
                "agent_steps": [{
                    "step": "analysis_error",
                    "result": f"准备失败: {prep_result.error}"
                }]
            }

        # 3. 记录业务信息
        logger.info(
            f"[LangGraph] AnalysisAction准备完成: "
            f"work_id={prep_result.metadata.get('work_id')}, "
            f"chapter_id={prep_result.metadata.get('chapter_id')}"
        )

        # 4. 统一使用框架调用LLM（触发监控）
        return await self._handle_agent_with_tools(
            state,
            agent_type=prep_result.metadata.get("agent_type", "analysis"),
            system_prompt=prep_result.system_prompt
        )

    async def _handle_stuck(self, state: AgentState) -> AgentState:
        """
        处理卡文场景 - 使用新架构

        新架构流程：
        1. 使用StuckAction.prepare()准备参数
        2. 调用_handle_agent_with_tools统一处理（触发监控）
        """
        from app.services.agent.actions import StuckAction

        logger.info("[LangGraph] 处理卡文请求（新架构）")

        # 1. 使用Action准备参数（业务逻辑）
        stuck_action = StuckAction()  # 新架构不需要ai_service
        prep_result = await stuck_action.prepare(state)

        # 2. 检查准备结果
        if not prep_result.success:
            logger.error(f"[LangGraph] StuckAction.prepare()失败: {prep_result.error}")
            from langchain_core.messages import AIMessage
            error_msg = AIMessage(content=f"抱歉，卡文请求处理失败: {prep_result.error}")
            return {
                "messages": [error_msg],
                "final_response": error_msg.content,
                "agent_steps": [{
                    "step": "stuck_error",
                    "result": f"准备失败: {prep_result.error}"
                }]
            }

        # 3. 记录业务信息
        logger.info(
            f"[LangGraph] StuckAction准备完成: "
            f"work_id={prep_result.metadata.get('work_id')}, "
            f"chapter_id={prep_result.metadata.get('chapter_id')}"
        )

        # 4. 统一使用框架调用LLM（触发监控）
        return await self._handle_agent_with_tools(
            state,
            agent_type=prep_result.metadata.get("agent_type", "stuck"),
            system_prompt=prep_result.system_prompt
        )

    async def _handle_general(self, state: AgentState) -> AgentState:
        """
        处理一般对话 - 使用新架构

        新架构流程：
        1. 使用GeneralChatAction.prepare()准备参数
        2. 调用_handle_agent_with_tools统一处理（触发监控）
        """
        from app.services.agent.actions import GeneralChatAction

        logger.info("[LangGraph] 处理一般对话（新架构）")

        # 1. 使用Action准备参数（业务逻辑）
        general_action = GeneralChatAction()  # 新架构不需要ai_service
        prep_result = await general_action.prepare(state)

        # 2. 检查准备结果
        if not prep_result.success:
            logger.error(f"[LangGraph] GeneralChatAction.prepare()失败: {prep_result.error}")
            from langchain_core.messages import AIMessage
            error_msg = AIMessage(content=f"抱歉，无法处理您的请求: {prep_result.error}")
            return {
                "messages": [error_msg],
                "final_response": error_msg.content,
                "agent_steps": [{
                    "step": "general_chat_error",
                    "result": f"准备失败: {prep_result.error}"
                }]
            }

        # 3. 统一使用框架调用LLM（触发监控）
        logger.info(f"[LangGraph] 使用system_prompt调用LLM: {prep_result.system_prompt[:100]}...")
        return await self._handle_agent_with_tools(
            state,
            agent_type=prep_result.metadata.get("agent_type", "general"),
            system_prompt=prep_result.system_prompt
        )

    async def chat(
        self,
        message: str,
        work_id: Optional[str] = None,
        chapter_id: Optional[str] = None,
        conversation_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        与 Agent 对话

        Args:
            message: 用户消息
            work_id: 作品ID
            chapter_id: 章节ID
            conversation_id: 会话ID（用于记忆）
            context: 额外上下文

        Returns:
            Dict: Agent响应
        """

        # 懒加载：第一次使用时初始化AsyncRedisSaver索引
        if isinstance(self.checkpointer, AsyncRedisSaver) and not self._checkpointer_setup_done:
            try:
                await self.checkpointer.asetup()
                self._checkpointer_setup_done = True
                logger.info(f"[LangGraph] AsyncRedisSaver索引创建成功")
            except Exception as setup_error:
                logger.error(f"[LangGraph] AsyncRedisSaver索引创建失败: {setup_error}")
                raise

        # 构建初始状态
        initial_state = {
            "messages": [HumanMessage(content=message)],
            "work_id": work_id,
            "chapter_id": chapter_id,
            "intent": None,
            "context": context or {},
            "agent_steps": [],
            "suggested_actions": [],
            "final_response": None
        }

        # 运行图
        config = {"configurable": {"thread_id": conversation_id or "default"}}

        try:
            result = await self.graph.ainvoke(initial_state, config)

            return {
                "response": result["final_response"],
                "conversation_id": conversation_id or "default",
                "messages": result["messages"],  # ✅ 添加 messages 到返回值
                "agent_steps": result["agent_steps"],
                "suggested_actions": result["suggested_actions"],
                "metadata": {
                    "intent": result.get("intent"),
                    "timestamp": str(datetime.now())
                }
            }

        except Exception as e:
            import traceback
            error_msg = str(e) or repr(e)
            error_trace = traceback.format_exc()
            logger.error(f"[LangGraph] Agent执行失败: {error_msg}")
            logger.error(f"[LangGraph] 错误堆栈:\n{error_trace}")
            return {
                "response": f"抱歉，处理您的请求时出错了：{error_msg}",
                "conversation_id": conversation_id or "default",
                "agent_steps": [],
                "suggested_actions": [],
                "metadata": {"error": error_msg, "traceback": error_trace}
            }

    async def chat_stream(
        self,
        message: str,
        user_id: Optional[str] = None,  # 新增：用户ID（用于长期记忆隔离）
        work_id: Optional[str] = None,
        chapter_id: Optional[str] = None,
        conversation_id: Optional[str] = None,
        context: Optional[dict] = None,
        on_progress: Optional[callable] = None,
        on_tool_call: Optional[callable] = None,
        on_content: Optional[callable] = None
    ) -> dict:
        """
        流式执行chat()，提供实时进度反馈（已集成上下文管理）

        Args:
            message: 用户消息
            user_id: 用户ID（用于长期记忆隔离）
            work_id: 作品ID
            chapter_id: 章节ID
            conversation_id: 会话ID
            context: 额外上下文
            on_progress: 进度回调 async def on_progress(event: dict)
            on_tool_call: 工具调用回调 async def on_tool_call(tool_name: str, tool_args: dict)
            on_content: 内容生成回调 async def on_content(content: str)

        Returns:
            Dict: Agent响应（同chat()方法）
        """

        # 🔧 监控：导入监控工具
        import time
        from app.services.agent.utils.monitoring import increment_counter, record_timer

        # 🔧 监控：记录总体开始时间
        overall_start = time.time()

        logger.info(f"[LangGraph Stream] 开始流式执行: {message[:50]}...")

        # 懒加载AsyncRedisSaver索引
        if isinstance(self.checkpointer, AsyncRedisSaver) and not self._checkpointer_setup_done:
            try:
                await self.checkpointer.asetup()
                self._checkpointer_setup_done = True
                logger.info(f"[LangGraph] AsyncRedisSaver索引创建成功")
            except Exception as setup_error:
                logger.error(f"[LangGraph] AsyncRedisSaver索引创建失败: {setup_error}")
                raise

        # 🔧 新增：构建上下文（加载历史对话）
        session_id = conversation_id or "default"

        # 动态设置user_id（用于长期记忆隔离）
        if user_id:
            self.context_manager.user_id = user_id
            logger.info(f"[Context] 设置用户ID: {user_id}")

        # ✅ 优化：移除重复的意图识别
        # LangGraph的intent_classifier节点会自动完成意图识别
        # 这里不再预先识别,避免重复调用

        # 🔧 监控：上下文构建计时
        context_start = time.time()

        # 使用默认的writing_agent模板（LangGraph会根据实际意图动态切换）
        system_prompt = self.prompt_manager.render(
            "writing_agent",
            user_message=message,
            context_summary="",
            user_preferences={},
            writing_constraints=[],
            examples=[]
        )

        context_bundle = await self.context_manager.build_context(
            session_id=session_id,
            system_prompt=system_prompt,
            query=message  # 新增：触发长期记忆检索
        )

        # 🔧 监控：记录上下文构建耗时
        record_timer("context_build_duration", time.time() - context_start)

        logger.info(f"[Context] 加载上下文: {context_bundle['metadata']}")

        # 🔧 新增：将历史消息转换为LangGraph消息格式
        history_messages = []
        for msg in context_bundle["messages"]:
            if msg["role"] == "system":
                history_messages.append(SystemMessage(content=msg["content"]))
            elif msg["role"] == "user":
                history_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                history_messages.append(AIMessage(content=msg["content"]))

        # 构建初始状态（不预设intent,由LangGraph的intent_classifier节点识别）
        initial_state = {
            "messages": history_messages + [HumanMessage(content=message)],  # 历史消息 + 当前消息
            "work_id": work_id,
            "chapter_id": chapter_id,
            "intent": None,  # ✅ 优化：由LangGraph的intent_classifier节点自动识别
            "context": context or {},
            "agent_steps": [],
            "suggested_actions": [],
            "final_response": None
        }

        # 配置
        config = {
            "configurable": {
                "thread_id": conversation_id or "default"
            }
        }

        try:
            # 🔧 监控：LangGraph执行计时
            graph_start = time.time()

            # 使用astream()流式执行
            event_count = 0

            # ✅ 添加超时保护（5分钟）
            async with asyncio.timeout(300):
                async for event in self.graph.astream(initial_state, config):
                    event_count += 1

                    # 处理事件并触发回调
                    await self._handle_stream_event(
                        event,
                        on_progress=on_progress,
                        on_tool_call=on_tool_call,
                        on_content=on_content
                    )

            # 🔧 监控：记录LangGraph执行耗时
            record_timer("graph_execution_duration", time.time() - graph_start)

            logger.info(f"[LangGraph Stream] 流式执行完成，共{event_count}个事件")

            # 获取最终状态
            final_state = await self.graph.aget_state(config)

            # 构建返回结果（与chat()相同的格式）
            if final_state and final_state.values:
                result = final_state.values
                final_response = result.get("final_response")

                # 🔧 新增：更新上下文（保存本轮对话）
                await self.context_manager.update_context(
                    session_id=session_id,
                    new_messages=[
                        {"role": "user", "content": message},
                        {"role": "assistant", "content": final_response or ""}
                    ],
                    context=context_bundle.get("context")
                )
                logger.info(f"[Context] 上下文已更新: {session_id}")

                # 🔧 监控：记录成功
                increment_counter("chat_stream_success")
                record_timer("chat_stream_total_duration", time.time() - overall_start)

                return {
                    "response": final_response,
                    "conversation_id": conversation_id or "default",
                    "messages": result.get("messages", []),
                    "agent_steps": result.get("agent_steps", []),
                    "suggested_actions": result.get("suggested_actions", []),
                    "metadata": {
                        "intent": result.get("intent"),
                        "timestamp": str(datetime.now()),
                        "stream_events": event_count,
                        "context_token_count": context_bundle["metadata"]["token_count"]
                    }
                }
            else:
                logger.error("[LangGraph Stream] 无法获取最终状态")

                # 🔧 监控：记录失败（无最终状态）
                increment_counter("chat_stream_error", labels={"error_type": "NoFinalState"})
                record_timer("chat_stream_total_duration", time.time() - overall_start)

                return {
                    "response": "执行完成，但无法获取结果",
                    "conversation_id": conversation_id or "default",
                    "agent_steps": [],
                    "suggested_actions": [],
                    "metadata": {"error": "No final state"}
                }

        except asyncio.TimeoutError:
            # ✅ 超时异常的特殊处理
            logger.error(f"[LangGraph Stream] 执行超时（300秒）")

            # 🔧 监控：记录超时
            increment_counter("chat_stream_error", labels={"error_type": "TimeoutError"})
            record_timer("chat_stream_total_duration", time.time() - overall_start)

            return {
                "response": "抱歉，请求处理超时（超过5分钟）。请尝试简化您的问题或稍后再试。",
                "conversation_id": conversation_id or "default",
                "agent_steps": [],
                "suggested_actions": ["简化问题", "稍后重试"],
                "metadata": {"error": "Request timeout after 300 seconds", "timeout": 300}
            }

        except Exception as e:
            import traceback
            error_msg = str(e) or repr(e)
            error_trace = traceback.format_exc()

            # 🔧 监控：记录异常
            increment_counter("chat_stream_error", labels={"error_type": type(e).__name__})
            record_timer("chat_stream_total_duration", time.time() - overall_start)

            logger.error(f"[LangGraph Stream] 执行失败: {error_msg}")
            logger.error(f"[LangGraph Stream] 错误堆栈:\n{error_trace}")
            return {
                "response": f"抱歉，处理您的请求时出错了：{error_msg}",
                "conversation_id": conversation_id or "default",
                "agent_steps": [],
                "suggested_actions": [],
                "metadata": {"error": error_msg, "traceback": error_trace}
            }

    async def _handle_stream_event(
        self,
        event: dict,
        on_progress: Optional[callable] = None,
        on_tool_call: Optional[callable] = None,
        on_content: Optional[callable] = None
    ):
        """处理astream事件，转换为用户友好的进度信息并触发回调"""

        if not event:
            return

        # 提取节点名和数据
        node_name = list(event.keys())[0]
        node_data = event[node_name]

        logger.info(f"[Stream Event] 节点: {node_name}")  # 改为info级别

        # 1. 解析进度事件并触发on_progress
        if on_progress:
            progress_event = self._parse_node_event(node_name, node_data)
            if progress_event:
                logger.info(f"[Stream Event] progress_event = {progress_event}")  # 添加日志
                try:
                    await on_progress(progress_event)
                    logger.info(f"[Stream Event] on_progress 回调已调用")  # 添加日志
                except Exception as e:
                    logger.error(f"[Stream] 进度回调失败: {e}")

        # 2. 检测工具调用并触发on_tool_call
        if on_tool_call and node_name == "tools":
            tool_calls = self._extract_tool_calls(node_data)
            for tool_name, tool_args in tool_calls:
                try:
                    await on_tool_call(tool_name, tool_args)
                except Exception as e:
                    logger.error(f"[Stream] 工具回调失败: {e}")

        # 3. 检测内容生成并触发on_content
        if on_content:
            content = self._extract_content(node_name, node_data)
            if content:
                try:
                    await on_content(content)
                except Exception as e:
                    logger.error(f"[Stream] 内容回调失败: {e}")

    def _parse_node_event(self, node_name: str, node_data: dict) -> Optional[dict]:
        """将LangGraph节点事件转换为用户友好的进度信息"""

        # 节点映射表
        node_mapping = {
            "intent_classifier": {
                "step": "intent_analysis",
                "description": "正在分析您的需求..."
            },
            "writing_agent": {
                "step": "thinking",
                "description": "正在思考如何帮助您..."
            },
            "planning_agent": {
                "step": "thinking",
                "description": "正在规划方案..."
            },
            "analysis_agent": {
                "step": "thinking",
                "description": "正在分析内容..."
            },
            "stuck_agent": {
                "step": "thinking",
                "description": "正在寻找解决方案..."
            },
            "general_chat": {
                "step": "thinking",
                "description": "正在思考回复..."
            },
            "tools": {
                "step": "tool_execution",
                "description": "正在调用工具..."
            }
        }

        mapping = node_mapping.get(node_name)
        if not mapping:
            return None

        # 提取额外信息
        details = {}

        if node_name == "intent_classifier":
            # 提取识别的意图
            intent = node_data.get("intent")
            if intent:
                details["intent"] = intent
                # 更新描述
                intent_names = {
                    "writing": "写作任务",
                    "planning": "规划任务",
                    "analysis": "分析任务",
                    "stuck": "卡文求助",
                    "general": "一般对话"
                }
                intent_display = intent_names.get(intent, intent)
                mapping["description"] = f"识别为：{intent_display}"

        elif node_name == "tools":
            # 提取工具名称
            messages = node_data.get("messages", [])
            tool_names = []
            for msg in messages:
                if hasattr(msg, "name"):
                    tool_names.append(msg.name)

            if tool_names:
                details["tools"] = tool_names
                # 更新描述（显示工具名）
                tool_display_names = {
                    "get_chapter_by_order_tool": "读取章节",
                    "continue_writing_tool": "继续创作",
                    "search_analysis_fragments_tool": "检索设定",
                    "search_memory_tool": "搜索记忆",
                    "add_todo_tool": "添加待办",
                    "get_work_details_tool": "获取作品信息",
                    "update_work_metadata_tool": "更新元数据"
                }
                display_names = [tool_display_names.get(t, t) for t in tool_names]
                mapping["description"] = f"正在{', '.join(display_names[:2])}..."

        return {
            "type": "progress",
            "step": mapping["step"],
            "description": mapping["description"],
            "node": node_name,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }

    def _extract_tool_calls(self, node_data: dict) -> list:
        """提取工具调用信息"""
        tool_calls = []
        messages = node_data.get("messages", [])

        for msg in messages:
            if isinstance(msg, ToolMessage) and hasattr(msg, "name"):
                tool_name = msg.name
                tool_args = {}
                tool_calls.append((tool_name, tool_args))

        return tool_calls

    def _extract_content(self, node_name: str, node_data: dict) -> Optional[str]:
        """提取生成的内容"""
        # 只处理agent节点
        if not node_name.endswith("_agent") and node_name != "general_chat":
            return None

        messages = node_data.get("messages", [])
        if not messages:
            return None

        last_message = messages[-1]
        if isinstance(last_message, AIMessage) and last_message.content:
            # 避免返回工具调用指令
            if not hasattr(last_message, "tool_calls") or not last_message.tool_calls:
                return last_message.content

        return None

    def _extract_json_from_text(self, text: str) -> Optional[dict]:
        """从文本中提取JSON对象

        支持：
        1. 纯JSON
        2. Markdown代码块包裹的JSON
        3. 混合文本中的JSON
        """
        import json
        import re

        text = text.strip()

        if not text:
            logger.error("[JSON解析] 输入文本为空")
            return None

        # 方法1: 尝试直接解析（最快）
        try:
            result = json.loads(text)
            logger.info("[JSON解析] 方法1成功: 直接解析")
            return result
        except json.JSONDecodeError as e:
            logger.debug(f"[JSON解析] 方法1失败: {e}")

        # 方法2: 尝试去除Markdown代码块 ```json ... ```
        if "```json" in text:
            # 使用贪婪匹配，确保捕获完整JSON
            match = re.search(r'```json\s*\n(.*?)```', text, re.DOTALL)
            if match:
                json_str = match.group(1).strip()
                try:
                    result = json.loads(json_str)
                    logger.info("[JSON解析] 方法2成功: 从```json块提取")
                    return result
                except json.JSONDecodeError as e:
                    logger.warning(f"[JSON解析] 方法2失败: {e}, JSON字符串: {json_str[:200]}")

        # 方法3: 尝试去除普通代码块 ``` ... ```
        if "```" in text:
            match = re.search(r'```\s*\n(.*?)```', text, re.DOTALL)
            if match:
                json_str = match.group(1).strip()
                try:
                    result = json.loads(json_str)
                    logger.info("[JSON解析] 方法3成功: 从```块提取")
                    return result
                except json.JSONDecodeError as e:
                    logger.warning(f"[JSON解析] 方法3失败: {e}, JSON字符串: {json_str[:200]}")

        # 方法4: 使用正则查找第一个完整的JSON对象 { ... }
        # 注意：要处理字符串中的大括号（在字符串中的大括号不算）
        match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', text, re.DOTALL)
        if match:
            json_str = match.group(0)
            try:
                result = json.loads(json_str)
                logger.info("[JSON解析] 方法4成功: 正则匹配JSON对象")
                return result
            except json.JSONDecodeError as e:
                logger.warning(f"[JSON解析] 方法4失败: {e}, JSON字符串: {json_str[:200]}")

        # 方法5: 逐字符扫描，手动匹配大括号（最后的手段）
        in_string = False
        escape = False
        brace_count = 0
        start_idx = -1

        for i, char in enumerate(text):
            if escape:
                escape = False
                continue

            if char == '\\':
                escape = True
                continue

            if char == '"' and not escape:
                in_string = not in_string
                continue

            if not in_string:
                if char == '{':
                    if brace_count == 0:
                        start_idx = i
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0 and start_idx != -1:
                        # 找到完整的JSON对象
                        json_str = text[start_idx:i+1]
                        try:
                            result = json.loads(json_str)
                            logger.info("[JSON解析] 方法5成功: 手动扫描大括号")
                            return result
                        except json.JSONDecodeError as e:
                            logger.warning(f"[JSON解析] 方法5失败: {e}, JSON字符串: {json_str[:200]}")
                            # 继续查找下一个
                            start_idx = -1

        logger.error(f"[JSON解析] 所有方法均失败，原始文本: {text[:500]}")
        return None

    async def chat_with_planning(
        self,
        message: str,
        work_id: Optional[str] = None,
        chapter_id: Optional[str] = None,
        conversation_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        on_plan: Optional[callable] = None,
        on_task_start: Optional[callable] = None,
        on_task_progress: Optional[callable] = None,
        on_task_done: Optional[callable] = None,
        on_content: Optional[callable] = None
    ) -> Dict[str, Any]:
        """
        与 Agent 对话 - Planning + Execution 模式

        Args:
            message: 用户消息
            work_id: 作品ID
            chapter_id: 章节ID
            conversation_id: 会话ID
            context: 额外上下文
            on_plan: 规划生成回调
            on_task_start: 任务开始回调
            on_task_progress: 任务进度回调
            on_task_done: 任务完成回调
            on_content: 内容生成回调

        Returns:
            Dict: Agent响应
        """
        # ✅ P0-2: 添加360秒总体超时保护（6分钟）
        try:
            import time
            from app.services.agent.utils.monitoring import increment_counter, record_timer
            start_time = time.time()

            # 设置总体超时
            async with asyncio.timeout(360):
                # ========== 加载对话历史 ==========
                conversation_history = ""

                if conversation_id and self.checkpointer:
                    try:
                        # 从checkpointer加载历史状态
                        from langgraph.checkpoint.base import CheckpointTuple
                        config = {"configurable": {"thread_id": conversation_id, "checkpoint_ns": ""}}

                        checkpoint_tuple = await self.checkpointer.aget_tuple(config)

                        if checkpoint_tuple and checkpoint_tuple.checkpoint:
                            messages = checkpoint_tuple.checkpoint.get("channel_values", {}).get("messages", [])

                            if messages:
                                logger.info(f"[Planning] 从checkpointer加载了 {len(messages)} 条历史消息")
                                # 格式化历史消息
                                history_lines = []
                                for msg in messages:
                                    if isinstance(msg, HumanMessage):
                                        history_lines.append(f"用户: {msg.content}")
                                    elif isinstance(msg, AIMessage):
                                        history_lines.append(f"助手: {msg.content}")
                                if history_lines:
                                    conversation_history = "\n".join(history_lines)
                    except Exception as e:
                        logger.warning(f"[Planning] 加载历史失败: {e}", exc_info=True)

                # ========== 阶段1: 规划（Planning） ==========
                # ✅ P1-7: 添加监控记录
                planning_start = time.time()
                logger.info(f"[Planning] 开始规划: {message[:50]}...")
                increment_counter("planning_phase_start")

                # 构建规划prompt（包含历史）
                history_section = ""
                if conversation_history:
                    history_section = f"""
【对话历史】
{conversation_history}

"""

                # ✅ Phase 2.6: 使用缓存的静态 Prompt（节省构建时间和 Token）
                static_prompt = await get_planning_static_prompt()

                plan_prompt = f"""AI写作助手。{history_section}
用户: {message}
work_id: {work_id}
chapter_id: {chapter_id}

{static_prompt}"""

                try:
                    plan_result = await self._generate_text(
                        plan_prompt,
                        temperature=0.3,
                        max_tokens=600,  # ✅ Phase 2.5: 优化从1000→600 (JSON任务列表)
                        task_type=TaskType.SIMPLE_QA  # ← Planning阶段用轻量模型快速生成任务列表
                    )
                    plan_text = plan_result.get("text", "").strip()

                    # 解析规划JSON
                    plan_data = self._extract_json_from_text(plan_text)

                except Exception as e:
                    logger.error(f"[Planning Agent] 执行失败: {e}", exc_info=True)

                    # 定义网络相关异常类型
                    network_related_errors = (
                    httpx.ConnectTimeout,
                    httpx.ReadTimeout,
                    httpx.NetworkError,
                    httpx.HTTPError,
                    ConnectionError,
                    TimeoutError,
                    # 移除过于宽泛的 OSError，只保留特定的网络错误
                    )

                    # 检查是否是网络相关错误
                    is_network_error = (
                    isinstance(e, network_related_errors) or
                    any(keyword in str(e).lower() for keyword in ["网络", "连接", "超时", "timeout", "connection", "network"])
                    )

                    if is_network_error:
                        logger.warning(f"[Planning] 检测到网络错误，使用简化规划流程")
                        # 使用简化的规划，避免再次调用AI
                        plan_data = {
                        "user_intent": "执行用户请求",
                        "tasks": [
                            {
                                "task_id": 1,
                                "description": "直接执行用户请求",
                                "tool": "get_context_tool",
                                "estimated_time": "5秒"
                            }
                        ]
                        }
                    else:
                        # 其他错误，返回错误响应
                        return {
                        "response": f"抱歉，规划阶段出现问题：{str(e)}。请稍后重试。",
                        "conversation_id": conversation_id or "default",
                        "agent_steps": [],
                        "suggested_actions": [],
                        "metadata": {"error": str(e), "stage": "planning", "error_type": type(e).__name__}
                        }

                if not plan_data:
                    logger.warning(f"[Planning] 无法解析规划JSON，AI返回: {plan_text[:500]}")

                if not plan_data or "tasks" not in plan_data:
                    # 默认规划
                    plan_data = {
                        "user_intent": "执行用户请求",
                        "tasks": [
                            {
                                "task_id": 1,
                                "description": "理解用户意图并获取相关上下文",
                                "tool": "get_context_tool",
                                "estimated_time": "5秒"
                            },
                            {
                                "task_id": 2,
                                "description": "执行用户请求",
                                "tool": "auto",
                                "estimated_time": "10秒"
                            }
                        ]
                    }

                # ✅ P1-7: 记录Planning阶段完成
                planning_duration = time.time() - planning_start

                logger.info(f"[Planning] 规划生成成功，共{len(plan_data['tasks'])}个任务，耗时: {planning_duration:.2f}s")
                increment_counter("planning_phase_completed")
                record_timer("planning_phase_duration", planning_duration)

                # 回调：发送规划
                if on_plan:
                    await on_plan(plan_data)

                # ========== 阶段2: 执行（Execution）- 智能并行执行 ==========
                # ✅ P1-7: 添加Execution阶段监控
                execution_start = time.time()
                logger.info("[Execution] 开始智能并行执行任务")
                increment_counter("execution_phase_start")

                initial_context = f"用户请求：{message}\n\n"

                # 使用新的并行执行方法
                # ✅ 为任务执行添加超时保护（4分钟，留1分钟给规划和总结）
                try:
                    async with asyncio.timeout(240):
                        task_results = await self._execute_tasks_in_parallel(
                            tasks=plan_data["tasks"],
                            work_id=work_id,
                            chapter_id=chapter_id,
                            context=initial_context,
                            on_task_start=on_task_start,
                            on_task_progress=on_task_progress,
                            on_task_done=on_task_done
                        )
                except asyncio.TimeoutError:
                    logger.error(f"[Execution] 任务执行超时（240秒）")
                    return {
                        "response": "抱歉，任务执行超时。请尝试简化您的请求。",
                        "conversation_id": conversation_id or "default",
                        "plan": plan_data,
                        "task_results": [],
                        "agent_steps": [],
                        "suggested_actions": ["简化请求", "稍后重试"],
                        "metadata": {"error": "Task execution timeout", "timeout": 240}
                    }

                # 构建完整上下文用于后续总结
                all_context = initial_context
                for result in task_results:
                    all_context += f"\n任务{result['task_id']}结果：\n{result['result']}\n"

                # ✅ P1-7: 记录Execution阶段完成
                execution_duration = time.time() - execution_start
                logger.info(f"[Execution] 所有任务执行完成，共{len(task_results)}个任务，耗时: {execution_duration:.2f}s")
                increment_counter("execution_phase_completed")
                record_timer("execution_phase_duration", execution_duration)

                # ========== 阶段3: 智能返回（Response） ==========
                logger.info("[Response] 生成最终响应")

                # 使用新的智能判断方法
                final_content = await self._build_final_response(
                    task_results=task_results,
                    message=message,
                    on_content=on_content
                )

                # ========== 保存对话到checkpointer ==========
                if conversation_id and self.checkpointer:
                    try:
                        # 构建新消息
                        new_messages = [
                        HumanMessage(content=message),
                        AIMessage(content=final_content)
                        ]

                        # 从checkpointer加载现有消息
                        config = {"configurable": {"thread_id": conversation_id, "checkpoint_ns": ""}}
                        checkpoint_tuple = await self.checkpointer.aget_tuple(config)

                        existing_messages = []
                        if checkpoint_tuple and checkpoint_tuple.checkpoint:
                            existing_messages = checkpoint_tuple.checkpoint.get("channel_values", {}).get("messages", [])

                            # 合并消息
                            all_messages = existing_messages + new_messages

                            # 构建新checkpoint
                            checkpoint_id = str(uuid.uuid4())
                            new_checkpoint = {
                            "v": 1,
                            "id": checkpoint_id,
                            "ts": datetime.now().isoformat(),
                            "channel_values": {
                            "messages": all_messages,
                            "work_id": work_id,
                            "chapter_id": chapter_id
                            },
                            "channel_versions": {
                            "messages": checkpoint_id,
                            "work_id": checkpoint_id,
                            "chapter_id": checkpoint_id
                            },
                            "versions_seen": {
                            "__start__": checkpoint_id
                            }
                            }

                            # 构建new_versions（用于标识哪些channel被更新了）
                            new_versions = {
                            "messages": checkpoint_id,
                            "work_id": checkpoint_id,
                            "chapter_id": checkpoint_id
                            }

                            # 保存checkpoint（提供完整的4个参数）
                            await self.checkpointer.aput(config, new_checkpoint, {}, new_versions)
                            logger.info(f"[Planning] 已保存 {len(new_messages)} 条新消息到checkpointer (总计: {len(all_messages)})")
                    except Exception as e:
                        logger.warning(f"[Planning] 保存消息到checkpointer失败: {e}")

                return {
                    "response": final_content,
                    "conversation_id": conversation_id or "default",
                    "plan": plan_data,
                    "task_results": task_results,
                    "agent_steps": [
                        {"step": "planning", "result": f"生成了{len(plan_data['tasks'])}个任务"},
                        {"step": "execution", "result": f"完成了{len(task_results)}个任务"},
                        {"step": "summarization", "result": "生成最终响应"}
                    ],
                    "suggested_actions": [],
                    "metadata": {
                        "intent": plan_data.get("user_intent"),
                        "total_tasks": len(plan_data["tasks"]),
                        "completed_tasks": len([t for t in task_results if t["status"] == "completed"]),
                        "timestamp": str(datetime.now())
                    }
                }

        except asyncio.TimeoutError:
            # 总体超时处理
            elapsed = time.time() - start_time
            logger.error(f"[Planning] 总体超时（{elapsed:.1f}秒，限制360秒）")
            increment_counter("chat_with_planning_error", labels={"error_type": "TimeoutError"})

            return {
                "response": f"抱歉，请求处理超时（超过6分钟）。您的请求可能过于复杂，建议：\n1. 简化请求内容\n2. 分步骤进行操作\n3. 稍后重试",
                "conversation_id": conversation_id or "default",
                "agent_steps": [],
                "suggested_actions": ["简化请求", "分步操作", "稍后重试"],
                "metadata": {
                    "error": "Overall timeout",
                    "timeout_seconds": 360,
                    "elapsed_seconds": elapsed
                }
            }

        except Exception as e:
            logger.error(f"[Planning Agent] 执行失败: {e}", exc_info=True)
            return {
                "response": f"抱歉，处理您的请求时出错了：{str(e)}",
                "conversation_id": conversation_id or "default",
                "agent_steps": [],
                "suggested_actions": [],
                "metadata": {"error": str(e)}
            }

    async def _execute_tasks_in_parallel(
        self,
        tasks: List[Dict[str, Any]],
        work_id: str,
        chapter_id: str,
        context: str,
        on_task_start: Optional[callable] = None,
        on_task_progress: Optional[callable] = None,
        on_task_done: Optional[callable] = None
    ) -> List[Dict[str, Any]]:
        """智能并行执行任务

        Args:
            tasks: 任务列表
            work_id: 作品ID
            chapter_id: 章节ID
            context: 上下文
            on_task_start: 任务开始回调
            on_task_progress: 任务进度回调
            on_task_done: 任务完成回调

        Returns:
            任务结果列表
        """
        # ✅ 创建参数解析器
        from app.services.agent.parameter_resolver import ParameterResolver

        resolver = ParameterResolver(strict_mode=False)  # 使用非严格模式，兼容性更好
        logger.info("[ParameterResolver] 参数解析器已启用")

        # ✅ 【修复-问题3】辅助函数：检查参数中是否包含占位符
        def _has_placeholder_dependency(params: Dict[str, Any]) -> bool:
            """检查参数中是否包含占位符（表示依赖其他任务）"""
            import json
            try:
                params_str = json.dumps(params, ensure_ascii=False)
                return bool(ParameterResolver.PLACEHOLDER_PATTERN.search(params_str))
            except Exception as e:
                logger.warning(f"[参数依赖检测] 序列化参数失败: {e}")
                return False  # 序列化失败，保守处理：假设无依赖

        # 定义可以并行执行的独立数据获取工具
        PARALLEL_SAFE_TOOLS = {
            "get_context_tool",
            "read_chapter_tool",
            "get_chapter_by_order_tool",
            "search_analysis_fragments_tool"
            # analyze_text_tool 移除：它依赖其他任务的结果，应该串行执行
        }

        # 分组任务：独立任务 vs 依赖任务
        parallel_tasks = []
        sequential_tasks = []

        # ✅ 【修复-问题3】改进分组策略：同时检查工具类型和参数依赖
        for task in tasks:
            tool_name = task.get("tool", "auto")
            has_dependency = _has_placeholder_dependency(task.get("params", {}))

            # 只有工具类型安全且无参数依赖的任务才能并行
            if tool_name in PARALLEL_SAFE_TOOLS and not has_dependency:
                parallel_tasks.append(task)
                logger.debug(
                    f"[任务分组] 任务{task['task_id']}({tool_name}) → 并行组"
                )
            else:
                sequential_tasks.append(task)
                reason = "有依赖" if has_dependency else "工具不支持并行"
                logger.debug(
                    f"[任务分组] 任务{task['task_id']}({tool_name}) → 串行组 ({reason})"
                )

        logger.info(
            f"[ParallelExecution] 任务分组: "
            f"并行={len(parallel_tasks)}, 串行={len(sequential_tasks)}"
        )

        task_results = []
        all_context = context

        # 第1批：并行执行独立的数据获取任务
        if parallel_tasks:
            logger.info(f"[ParallelExecution] 开始并行执行{len(parallel_tasks)}个任务")

            # 使用Semaphore限制并发数为5
            semaphore = asyncio.Semaphore(5)

            async def execute_with_semaphore(task):
                async with semaphore:
                    task_id = task["task_id"]
                    description = task["description"]
                    tool_name = task.get("tool", "unknown")  # 获取工具名称

                    logger.info(f"[ParallelExecution] 并行任务{task_id}开始: {description}")

                    if on_task_start:
                        await on_task_start(task)

                    # ✅ P1-5: 添加重试机制（最多3次尝试）
                    max_retries = 2
                    last_error = None

                    for retry_count in range(max_retries + 1):
                        try:
                            # ✅ 解析任务参数中的占位符
                            resolved_task = task.copy()
                            if "params" in resolved_task:
                                resolved_task["params"] = await resolver.resolve_params(
                                    resolved_task["params"],
                                    current_task_id=task_id
                                )
                                logger.debug(
                                    f"[ParameterResolver] 任务{task_id}参数已解析: "
                                    f"{resolved_task['params']}"
                                )

                            result = await self._execute_task(
                                task=resolved_task,  # ✅ 使用解析后的任务
                                work_id=work_id,
                                chapter_id=chapter_id,
                                context=all_context,
                                on_progress=on_task_progress
                            )

                            logger.info(f"[ParallelExecution] 并行任务{task_id}完成" + (f"（重试{retry_count}次后成功）" if retry_count > 0 else ""))

                            # ✅ 注册任务结果到参数解析器
                            await resolver.register_result(task_id, result)
                            logger.debug(f"[ParameterResolver] 任务{task_id}结果已注册")

                            if on_task_done:
                                await on_task_done(task, result)

                            return {
                                "task_id": task_id,
                                "description": description,
                                "tool": tool_name,
                                "result": result,
                                "status": "completed"
                            }

                        except Exception as e:
                            last_error = e

                            # 判断是否为可重试的错误（网络相关）
                            is_retryable = any(keyword in str(e).lower() for keyword in [
                                "timeout", "connection", "network", "网络", "连接", "超时"
                            ])

                            if is_retryable and retry_count < max_retries:
                                wait_time = 2 ** (retry_count + 1)  # 指数退避：2, 4, 8秒
                                logger.warning(f"[ParallelExecution] 任务{task_id}失败（{e}），{wait_time}秒后重试（{retry_count + 1}/{max_retries}）")
                                await asyncio.sleep(wait_time)
                            else:
                                # 不可重试或已达最大次数
                                logger.error(f"[ParallelExecution] 并行任务{task_id}最终失败: {last_error}")

                                # ✅ 【修复-问题2】注册失败结果到参数解析器
                                error_result = f"错误: {str(last_error)}"
                                await resolver.register_result(task_id, error_result)
                                logger.debug(f"[ParameterResolver] 任务{task_id}失败结果已注册")

                                return {
                                    "task_id": task_id,
                                    "description": description,
                                    "tool": tool_name,
                                    "result": error_result,
                                    "status": "failed"
                                }

                    # 如果所有重试都失败
                    # ✅ 【修复-问题2】注册重试失败结果到参数解析器
                    error_result = f"错误: {str(last_error)}（已重试{max_retries}次）"
                    await resolver.register_result(task_id, error_result)
                    logger.debug(f"[ParameterResolver] 任务{task_id}重试失败结果已注册")

                    return {
                        "task_id": task_id,
                        "description": description,
                        "tool": tool_name,
                        "result": error_result,
                        "status": "failed"
                    }

            # 并行执行所有独立任务
            # ✅ P0-4: 修复 return_exceptions=True，避免一个任务失败导致所有任务取消
            parallel_results = await asyncio.gather(
                *[execute_with_semaphore(task) for task in parallel_tasks],
                return_exceptions=True
            )

            # ✅ P0-4: 处理可能的异常结果（因为 return_exceptions=True）
            for i, result in enumerate(parallel_results):
                if isinstance(result, Exception):
                    # 异常结果 - 创建失败的任务记录
                    logger.error(f"[ParallelExecution] 并行任务失败: {result}")
                    failed_task = {
                        "task_id": parallel_tasks[i]["task_id"] if i < len(parallel_tasks) else "unknown",
                        "result": f"任务执行失败: {str(result)}",
                        "status": "failed",
                        "error": str(result)
                    }
                    task_results.append(failed_task)
                    all_context += f"\n任务{failed_task['task_id']}失败：{str(result)}\n"
                else:
                    # 正常结果
                    # 注意：任务结果已在execute_with_semaphore内部注册到resolver
                    task_results.append(result)
                    all_context += f"\n任务{result['task_id']}结果：\n{result['result']}\n"

        # 第2批：串行执行依赖任务（它们可能需要前面的结果）
        if sequential_tasks:
            logger.info(f"[ParallelExecution] 开始串行执行{len(sequential_tasks)}个任务")

            for task in sequential_tasks:
                task_id = task["task_id"]
                description = task["description"]
                tool_name = task.get("tool", "unknown")  # 获取工具名称

                logger.info(f"[ParallelExecution] 串行任务{task_id}开始: {description}")

                if on_task_start:
                    await on_task_start(task)

                # ✅ P1-5: 为串行任务也添加重试机制
                max_retries = 2
                last_error = None
                task_succeeded = False

                for retry_count in range(max_retries + 1):
                    try:
                        # ✅ 解析任务参数中的占位符
                        resolved_task = task.copy()
                        if "params" in resolved_task:
                            resolved_task["params"] = await resolver.resolve_params(
                                resolved_task["params"],
                                current_task_id=task_id
                            )
                            logger.debug(
                                f"[ParameterResolver] 任务{task_id}参数已解析: "
                                f"{resolved_task['params']}"
                            )

                        result = await self._execute_task(
                            task=resolved_task,  # ✅ 使用解析后的任务
                            work_id=work_id,
                            chapter_id=chapter_id,
                            context=all_context,
                            on_progress=on_task_progress
                        )

                        # ✅ 注册任务结果到参数解析器
                        await resolver.register_result(task_id, result)
                        logger.debug(f"[ParameterResolver] 任务{task_id}结果已注册")

                        task_results.append({
                            "task_id": task_id,
                            "description": description,
                            "tool": tool_name,
                            "result": result,
                            "status": "completed"
                        })

                        all_context += f"\n任务{task_id}结果：\n{result}\n"

                        logger.info(f"[ParallelExecution] 串行任务{task_id}完成" + (f"（重试{retry_count}次后成功）" if retry_count > 0 else ""))

                        if on_task_done:
                            await on_task_done(task, result)

                        task_succeeded = True
                        break  # 成功，退出重试循环

                    except Exception as e:
                        last_error = e

                        # 判断是否为可重试的错误（网络相关）
                        is_retryable = any(keyword in str(e).lower() for keyword in [
                            "timeout", "connection", "network", "网络", "连接", "超时"
                        ])

                        if is_retryable and retry_count < max_retries:
                            wait_time = 2 ** (retry_count + 1)
                            logger.warning(f"[ParallelExecution] 串行任务{task_id}失败（{e}），{wait_time}秒后重试（{retry_count + 1}/{max_retries}）")
                            await asyncio.sleep(wait_time)
                        else:
                            # 不可重试或已达最大次数
                            break

                # 如果所有重试都失败
                if not task_succeeded:
                    logger.error(f"[ParallelExecution] 串行任务{task_id}最终失败: {last_error}")

                    # ✅ 【修复-问题2】注册失败结果到参数解析器
                    error_result = f"错误: {str(last_error)}"
                    await resolver.register_result(task_id, error_result)
                    logger.debug(f"[ParameterResolver] 任务{task_id}失败结果已注册")

                    task_results.append({
                        "task_id": task_id,
                        "description": description,
                        "tool": tool_name,
                        "result": error_result,
                        "status": "failed"
                    })

        # 按task_id排序，保持原始顺序
        task_results.sort(key=lambda x: x["task_id"])

        return task_results

    def _classify_tasks(self, task_results: List[Dict]) -> Dict[str, List]:
        """分类任务：输入型 vs 输出型

        Args:
            task_results: 任务结果列表

        Returns:
            分类后的任务字典，包含 input_tasks 和 output_tasks
        """
        # 定义输入型工具（只是获取数据，不产生最终输出）
        INPUT_TOOLS = {
            "get_context_tool",
            "read_chapter_tool",
            "get_chapter_by_order_tool",
            "search_analysis_fragments_tool"
        }

        # 定义输出型工具（产生用户需要的最终内容）
        OUTPUT_TOOLS = {
            "continue_writing_tool",   # 续写
            "polish_text_tool",        # 润色
            "analyze_text_tool"        # 分析
        }

        input_tasks = []
        output_tasks = []

        for task in task_results:
            tool = task.get("tool", "")
            if tool in INPUT_TOOLS:
                input_tasks.append(task)
            elif tool in OUTPUT_TOOLS:
                output_tasks.append(task)
            else:
                # 未分类的工具，保守起见归为输出型
                output_tasks.append(task)

        logger.info(
            f"[TaskClassify] 任务分类: 输入型={len(input_tasks)}, 输出型={len(output_tasks)}"
        )

        return {
            "input_tasks": input_tasks,
            "output_tasks": output_tasks
        }

    async def _build_final_response(
        self,
        task_results: List[Dict],
        message: str,
        on_content: Optional[callable] = None
    ) -> str:
        """智能构建最终响应

        根据任务类型智能判断是否需要AI整合：
        - 缺失前置条件 → 直接返回友好提示（优先级最高）
        - 单个创作任务 → 直接返回（节省AI调用）
        - 多个输出任务 → 简单拼接（节省AI调用）
        - 其他情况 → AI整合

        Args:
            task_results: 任务结果列表
            message: 用户原始消息
            on_content: 内容回调函数

        Returns:
            最终响应内容
        """
        # ✅ 优先检查：是否有缺失前置条件的情况
        # 如果有工具返回了 missing_prerequisite 状态，直接返回友好提示
        for result in task_results:
            try:
                result_str = result.get('result', '')
                if not result_str:
                    continue

                # 尝试解析为JSON
                result_json = json.loads(result_str)

                # 检查是否为missing_prerequisite状态
                if result_json.get('status') == 'missing_prerequisite':
                    suggested = result_json.get('suggested_response', '')

                    if suggested:
                        logger.info(
                            f"[Response] 检测到missing_prerequisite "
                            f"(缺失: {result_json.get('missing', 'unknown')}), "
                            f"直接返回友好提示，跳过AI整合"
                        )

                        # 模拟流式输出（保持用户体验一致）
                        if on_content:
                            chunk_size = 20  # 每次发送20个字符
                            for i in range(0, len(suggested), chunk_size):
                                chunk = suggested[i:i + chunk_size]
                                await on_content(chunk)

                        return suggested
            except (json.JSONDecodeError, TypeError, KeyError):
                # 不是JSON或格式不对，继续下一个
                continue

        # 分类任务
        classified = self._classify_tasks(task_results)
        output_tasks = classified["output_tasks"]

        # 情况1：没有输出任务（极少见）
        if len(output_tasks) == 0:
            logger.warning("[Response] 没有明确输出任务，使用AI整合")
            return await self._ai_summarization(task_results, message, on_content)

        # 情况2：单个输出任务（主要场景，约85%）
        elif len(output_tasks) == 1:
            task = output_tasks[0]
            tool_name = task["tool"]
            result = task.get("result", "") or ""  # 处理None的情况

            # 创作类任务，且输出充分 → 直接返回
            if tool_name in ["continue_writing_tool", "polish_text_tool"]:
                if len(result) > 500:
                    logger.info(
                        f"[Response] 单个创作任务({tool_name})，"
                        f"输出{len(result)}字符，直接返回（跳过AI调用）"
                    )

                    # 模拟流式输出（保持用户体验一致）
                    if on_content:
                        # 分块发送，模拟流式输出效果
                        chunk_size = 50  # 每次发送50个字符
                        for i in range(0, len(result), chunk_size):
                            chunk = result[i:i + chunk_size]
                            await on_content(chunk)

                    return result

            # 分析类任务，可能需要格式化
            logger.info(f"[Response] 单个分析任务({tool_name})，使用AI格式化")
            return await self._ai_summarization(task_results, message, on_content)

        # 情况3：多个输出任务（约15%）
        else:
            logger.info(f"[Response] {len(output_tasks)}个输出任务，简单拼接")

            parts = []
            for task in output_tasks:
                tool_name = task["tool"]
                result = task.get("result", "") or ""  # 处理None的情况

                # 添加标题
                if tool_name == "analyze_text_tool":
                    parts.append(f"## 分析结果\n\n{result}")
                elif tool_name == "continue_writing_tool":
                    parts.append(f"## 续写内容\n\n{result}")
                elif tool_name == "polish_text_tool":
                    parts.append(f"## 润色结果\n\n{result}")
                else:
                    parts.append(result)

            final_content = "\n\n".join(parts)

            # 模拟流式输出（保持用户体验一致）
            if on_content:
                # 分块发送，模拟流式输出效果
                chunk_size = 50  # 每次发送50个字符
                for i in range(0, len(final_content), chunk_size):
                    chunk = final_content[i:i + chunk_size]
                    await on_content(chunk)

            return final_content

    async def _ai_summarization(
        self,
        task_results: List[Dict],
        message: str,
        on_content: Optional[callable] = None
    ) -> str:
        """AI整合（保留原有的Summarization逻辑）

        Args:
            task_results: 任务结果列表
            message: 用户原始消息
            on_content: 内容回调函数

        Returns:
            AI整合后的最终响应
        """
        from app.services.agent.utils.monitoring import increment_counter

        logger.info("[Summarization] 使用AI整合任务结果")

        # 构建完整上下文
        all_context = f"用户请求：{message}\n\n"
        for result in task_results:
            all_context += f"\n任务{result['task_id']}结果：\n{result['result']}\n"

        # 上下文压缩
        compressed_context = _build_summarization_context(
            user_message=message,
            task_results=task_results,
            max_context_length=6000  # 减少到6000字符，提高响应速度，避免超时
        )

        logger.info(
            f"[Summarization] 上下文压缩: "
            f"原始={len(all_context)}字符, "
            f"压缩后={len(compressed_context)}字符, "
            f"压缩率={(100 - len(compressed_context) * 100 // len(all_context)) if len(all_context) > 0 else 0}%"
        )

        summary_prompt = f"""基于以下任务执行结果，生成最终的响应给用户。

{compressed_context}

要求：
1. 综合所有任务结果
2. 用清晰、友好的语言呈现
3. 如果是创作内容，直接输出创作结果
4. 如果是分析/规划，给出详细说明

请生成最终响应："""

        # ✅ 直接调用 _generate_text（内部已有120秒超时保护）
        result = await self._generate_text(
            prompt=summary_prompt,
            max_tokens=2000,
            temperature=0.7,
            task_type=TaskType.SUMMARIZATION
        )

        # 检查是否有错误（超时或其他异常）
        if "error" in result:
            logger.warning(f"[Summarization] _generate_text 失败: {result.get('error')}")
            increment_counter("ai_summarization_error", labels={"error_type": result.get('error', 'unknown')})
            # 返回简单的任务结果拼接作为fallback
            fallback_content = f"抱歉，AI整合失败。以下是任务结果摘要：\n\n"
            for task_result in task_results:
                fallback_content += f"- 任务{task_result['task_id']}: {task_result.get('description', 'N/A')}\n"
                if task_result.get('status') == 'completed':
                    result_text = str(task_result.get('result', ''))[:200]
                    fallback_content += f"  结果: {result_text}...\n"
            return fallback_content

        final_content = result.get("text", "")

        # 如果有流式回调，发送完整内容
        if on_content and final_content:
            await on_content(final_content)

        return final_content

    def _normalize_tool_params(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """标准化工具参数，将不符合格式的参数转换为正确格式

        Args:
            tool_name: 工具名称
            params: 原始参数

        Returns:
            标准化后的参数
        """
        import json

        normalized = params.copy()

        # continue_writing_tool 的 requirements 必须是字符串
        if tool_name == "continue_writing_tool":
            requirements = params.get("requirements", "")
            if isinstance(requirements, dict):
                # 将字典转换为可读的字符串
                parts = []
                for key, value in requirements.items():
                    parts.append(f"{key}: {value}")
                normalized["requirements"] = "，".join(parts)
                logger.info(f"[参数标准化] continue_writing_tool.requirements: dict → str")

        # polish_text_tool 的 text 和 style 必须是字符串
        elif tool_name == "polish_text_tool":
            if "text" in params and not isinstance(params["text"], str):
                normalized["text"] = str(params["text"])
                logger.info(f"[参数标准化] polish_text_tool.text: {type(params['text']).__name__} → str")
            if "style" in params and not isinstance(params["style"], str):
                normalized["style"] = str(params["style"])

        # analyze_text_tool 的参数必须是字符串
        elif tool_name == "analyze_text_tool":
            if "text" in params and not isinstance(params["text"], str):
                normalized["text"] = str(params["text"])
                logger.info(f"[参数标准化] analyze_text_tool.text: {type(params['text']).__name__} → str")
            if "focus" in params and not isinstance(params["focus"], str):
                normalized["focus"] = str(params["focus"])

        return normalized

    async def _execute_task(
        self,
        task: Dict[str, Any],
        work_id: str,
        chapter_id: str,
        context: str,
        on_progress: Optional[callable] = None
    ) -> str:
        """执行单个任务"""
        tool_name = task.get("tool", "auto")
        params = task.get("params", {})

        # 标准化参数格式
        params = self._normalize_tool_params(tool_name, params)

        if on_progress:
            await on_progress(task, "正在执行...")

        # 根据工具名称调用对应工具
        if tool_name == "get_chapter_by_order_tool":
            result = await get_chapter_by_order_tool.ainvoke({
                "work_id": work_id,
                "chapter_order": params.get("chapter_order", 1)
            })
        elif tool_name == "get_context_tool":
            result = await get_context_tool.ainvoke({
                "work_id": work_id,
                "chapter_id": chapter_id or ""
            })
        elif tool_name == "read_chapter_tool":
            # 检查是否提供了 chapter_id 参数
            if "chapter_id" not in params or not params["chapter_id"]:
                logger.warning(
                    f"[_execute_task] read_chapter_tool 缺少 chapter_id 参数，"
                    f"将使用当前章节ID: {chapter_id}。"
                    f"任务描述: {task.get('description', 'N/A')}"
                )

            result = await read_chapter_tool.ainvoke({
                "work_id": work_id,
                "chapter_id": params.get("chapter_id") or chapter_id or ""
            })
        elif tool_name == "search_analysis_fragments_tool":
            # 验证work_id参数（必需）
            if not work_id:
                logger.warning(
                    f"[_execute_task] search_analysis_fragments_tool 需要 work_id 参数，"
                    f"但当前 work_id 为空。任务描述: {task.get('description', 'N/A')}"
                )
                result = json.dumps({
                    "error": "需要指定作品ID才能检索分析片段",
                    "message": "请在聊天时指定作品ID，或在作品详情页使用此功能",
                    "tool": "search_analysis_fragments_tool"
                }, ensure_ascii=False, indent=2)
            else:
                result = await search_analysis_fragments_tool.ainvoke({
                    "work_id": work_id,
                    "query": params.get("query", "相关内容"),
                    "top_k": params.get("top_k", 5)
                })
        elif tool_name == "continue_writing_tool":
            result = await continue_writing_tool.ainvoke({
                "context": params.get("context", context),
                "requirements": params.get("requirements", "")
            })
        elif tool_name == "polish_text_tool":
            result = await polish_text_tool.ainvoke({
                "text": params.get("text", ""),
                "style": params.get("style", "professional")
            })
        elif tool_name == "analyze_text_tool":
            # ✅ 参数已由ParameterResolver解析，直接使用
            result = await analyze_text_tool.ainvoke({
                "text": params.get("text", ""),
                "focus": params.get("focus", "all")
            })
        else:
            # 自动选择工具
            result = f"任务 {task['description']} 需要手动处理"

        if on_progress:
            await on_progress(task, "完成")

        return result


# ==================== 导出 ====================

__all__ = ["WritingAgentGraph", "AgentState"]
 
