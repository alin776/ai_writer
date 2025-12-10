# -*- coding: utf-8 -*-
"""
LangGraph 工具定义

从 langgraph_agent.py 拆分的 LangChain @tool 装饰器工具：
- 写作工具: continue_writing_tool, analyze_text_tool
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
from typing import Optional

from langchain_core.tools import tool

from app.services.ai.http_ai_service import HTTPAIService
from app.services.agent.model_selector import TaskType
from app.services.agent.timeout_config import TimeoutConfig
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
            async with asyncio.timeout(TimeoutConfig.LLM_CALL):
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
            retry_count += 1
            logger.error(f"[_generate_text_helper] 生成失败 (尝试 {retry_count}/{max_retries}): {e}")

            if retry_count >= max_retries:
                return f"错误：AI服务调用失败，已重试{max_retries}次。错误信息：{str(e)}"

            await asyncio.sleep(2 ** retry_count)

    return generated_text or "错误：生成内容为空"


# ==================== 写作工具 ====================

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
        task_type=TaskType.CONTENT_CREATION
    )


@tool
async def analyze_text_tool(text: str, focus: str = "all") -> str:
    """分析工具：分析文本问题

    Args:
        text: 待分析的文本
        focus: 分析重点（all/grammar/logic/style）

    Returns:
        分析报告
    """
    from app.prompts.constraint_manager import get_constraint_manager

    if not text or not text.strip():
        logger.warning("[analyze_text_tool] 收到空文本")
        return "错误：未提供待分析的文本内容。"

    if "$TASK_" in text and "$" in text[text.find("$TASK_")+1:]:
        logger.warning(f"[analyze_text_tool] 检测到未解析的占位符")
        return f"错误：文本参数中包含未解析的占位符。原始参数: {text[:200]}"

    try:
        prompt_manager = get_constraint_manager()
        base_prompt = prompt_manager.format_prompt("analyze_text", text=text, focus=focus)

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


# ==================== 章节工具 ====================

@tool
async def read_chapter_tool(work_id: Optional[str] = None, chapter_id: str = "") -> str:
    """读取指定章节工具：从数据库读取单个或多个章节内容

    Args:
        work_id: 作品ID（UUID格式）
        chapter_id: 章节ID（UUID格式）或多个章节ID（用逗号分隔，如 "id1,id2,id3"）

    Returns:
        章节信息JSON（单章节）或章节列表JSON（多章节）
    """
    if not work_id:
        return json.dumps({
            "status": "missing_prerequisite",
            "missing": "work_id",
            "message": "需要指定作品ID才能读取章节"
        }, ensure_ascii=False, indent=2)

    if not chapter_id:
        return json.dumps({
            "status": "missing_prerequisite",
            "missing": "chapter_id",
            "message": "需要指定章节ID才能读取章节"
        }, ensure_ascii=False, indent=2)

    uuid_error = validate_uuid(work_id, "作品ID")
    if uuid_error:
        return uuid_error

    # 🆕 支持多章节ID（逗号分隔）
    chapter_ids = [cid.strip() for cid in chapter_id.split(",") if cid.strip()]

    # 验证所有章节ID格式
    for cid in chapter_ids:
        uuid_error = validate_uuid(cid, "章节ID")
        if uuid_error:
            return uuid_error

    async with AsyncSessionLocal() as db:
        try:
            from app.services.chapter_service import ChapterService

            chapter_service = ChapterService(db)

            # 🆕 多章节处理
            if len(chapter_ids) > 1:
                chapters_info = []
                for cid in chapter_ids:
                    chapter = await _retry_on_failure(
                        chapter_service.get_chapter_by_id,
                        cid,
                        max_retries=2
                    )

                    if chapter:
                        chapters_info.append({
                            "chapter_id": str(chapter.id),
                            "title": chapter.title,
                            "order": chapter.order,
                            "content": chapter.content[:5000] if chapter.content else "",
                            "content_length": len(chapter.content) if chapter.content else 0,
                            "word_count": chapter.word_count,
                            "status": chapter.status.value if hasattr(chapter, 'status') else "unknown"
                        })
                    else:
                        chapters_info.append({
                            "chapter_id": cid,
                            "error": f"未找到章节 {cid}"
                        })

                logger.info(f"[read_chapter_tool] ✅ 读取多章节成功: 共 {len(chapters_info)} 章")
                return json.dumps({
                    "type": "multi_chapter",
                    "count": len(chapters_info),
                    "chapters": chapters_info
                }, ensure_ascii=False, indent=2)

            # 单章节处理（保持原有逻辑）
            else:
                chapter = await _retry_on_failure(
                    chapter_service.get_chapter_by_id,
                    chapter_ids[0],
                    max_retries=2
                )

                if not chapter:
                    return json.dumps({
                        "error": f"未找到章节 {chapter_ids[0]}",
                        "work_id": work_id
                    }, ensure_ascii=False, indent=2)

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
            try:
                await db.rollback()
            except:
                pass
            logger.error(f"[read_chapter_tool] ❌ 读取章节失败: {e}")
            return json.dumps({
                "error": f"读取章节失败: {str(e)}",
                "work_id": work_id,
                "chapter_id": chapter_id
            }, ensure_ascii=False, indent=2)

        finally:
            try:
                await db.close()
            except:
                pass


@tool
async def get_chapter_by_order_tool(work_id: Optional[str] = None, chapter_order: int = 1) -> str:
    """通过章节序号获取章节ID和内容

    Args:
        work_id: 作品ID（UUID格式）
        chapter_order: 章节序号（第1章=1）

    Returns:
        章节信息JSON
    """
    if not work_id:
        return json.dumps({
            "status": "missing_prerequisite",
            "missing": "work_id",
            "message": f"需要指定作品ID才能查询第{chapter_order}章"
        }, ensure_ascii=False, indent=2)

    uuid_error = validate_uuid(work_id, "作品ID")
    if uuid_error:
        return uuid_error

    async with AsyncSessionLocal() as db:
        try:
            from app.services.work_service import WorkService
            from app.utils.text_cleaner import text_cleaner

            work_service = WorkService(db)
            work = await _retry_on_failure(
                work_service.get_work_by_id,
                work_id,
                use_cache=False,
                max_retries=2
            )

            if not work or not work.chapters:
                return json.dumps({
                    "error": "未找到作品或作品没有章节",
                    "work_id": work_id
                }, ensure_ascii=False, indent=2)

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

            clean_content = text_cleaner.html_to_clean_text(
                target_chapter.content if target_chapter.content else "",
                preserve_structure=True,
                max_length=5000
            )

            chapter_info = {
                "chapter_id": str(target_chapter.id),
                "title": target_chapter.title,
                "order": target_chapter.order,
                "content": clean_content,
                "content_length": len(clean_content),
                "word_count": target_chapter.word_count,
                "status": target_chapter.status.value if hasattr(target_chapter, 'status') else "unknown"
            }

            logger.info(f"[get_chapter_by_order_tool] ✅ 找到第{chapter_order}章: {target_chapter.title}")
            return json.dumps(chapter_info, ensure_ascii=False, indent=2)

        except Exception as e:
            try:
                await db.rollback()
            except:
                pass
            logger.error(f"[get_chapter_by_order_tool] ❌ 查询失败: {e}")
            return json.dumps({
                "error": f"查询失败: {str(e)}",
                "work_id": work_id
            }, ensure_ascii=False, indent=2)

        finally:
            try:
                await db.close()
            except:
                pass


@tool
async def search_analysis_fragments_tool(work_id: Optional[str] = None, query: str = "", top_k: int = 5) -> str:
    """检索分析碎片工具：从向量数据库检索相关的小说分析片段（RAG）

    Args:
        work_id: 作品ID（UUID格式）
        query: 查询文本
        top_k: 返回前K个最相关结果

    Returns:
        相关片段JSON
    """
    if not work_id:
        return json.dumps({
            "status": "missing_prerequisite",
            "missing": "work_id",
            "message": "需要指定作品ID才能检索分析片段"
        }, ensure_ascii=False, indent=2)

    uuid_error = validate_uuid(work_id, "作品ID")
    if uuid_error:
        return uuid_error

    async with AsyncSessionLocal() as db:
        try:
            from app.services.vector_store_service import VectorStoreService

            vector_service = VectorStoreService(db)
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
            try:
                await db.rollback()
            except:
                pass
            logger.error(f"[search_analysis_fragments_tool] ❌ RAG检索失败: {e}")
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
async def get_context_tool(work_id: Optional[str] = None, chapter_id: str = "") -> str:
    """获取上下文工具：检索作品、章节和世界观信息

    Args:
        work_id: 作品ID（UUID格式）
        chapter_id: 章节ID（可选）

    Returns:
        上下文信息JSON
    """
    if not work_id:
        return json.dumps({
            "status": "limited_mode",
            "error": "missing_work_id",
            "work_id": None,
            "work_info": {},
            "current_chapter": {},
            "related_analysis": [],
            "message": "未指定作品，无法获取详细上下文。",
            "suggestion": "提供作品ID可获得更详细的上下文信息"
        }, ensure_ascii=False, indent=2)

    uuid_error = validate_uuid(work_id, "作品ID")
    if uuid_error:
        return uuid_error

    if chapter_id:
        uuid_error = validate_uuid(chapter_id, "章节ID")
        if uuid_error:
            return uuid_error

    async with AsyncSessionLocal() as db:
        try:
            from app.services.work_service import WorkService
            from app.services.chapter_service import ChapterService
            from app.services.chapter_vector_service import ChapterVectorService

            work_service = WorkService(db)
            chapter_service = ChapterService(db)
            chapter_vector_service = ChapterVectorService(db)

            context_info = {
                "work_id": work_id,
                "work_info": {},
                "current_chapter": {},
                "related_analysis": []
            }

            # 1. 获取作品信息
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

            # 2. 获取当前章节
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

            # 3. RAG检索章节上下文
            try:
                current_order = 999
                if chapter_id:
                    chapter = await chapter_service.get_chapter_by_id(chapter_id)
                    if chapter:
                        current_order = chapter.order

                query = "作品背景、人物关系、情节发展、伏笔线索"
                chapter_rag_results = await _retry_on_failure(
                    chapter_vector_service.retrieve_for_writing,
                    work_id=work_id,
                    current_chapter_order=current_order,
                    query=query,
                    top_k=5,
                    similarity_threshold=0.3,
                    max_retries=2
                )

                if chapter_rag_results:
                    context_info["related_context"] = [
                        {
                            "chapter_title": r['chapter_title'],
                            "chapter_order": r['chapter_order'],
                            "similarity": r['similarity'],
                            "content": r['chunk_text'][:500]
                        }
                        for r in chapter_rag_results
                    ]
                else:
                    context_info["related_context"] = []

            except Exception as rag_error:
                logger.error(f"[get_context_tool] RAG检索失败: {rag_error}")
                context_info["related_context"] = []

            logger.info(f"[get_context_tool] ✅ 获取上下文成功")
            return json.dumps(context_info, ensure_ascii=False, indent=2)

        except Exception as e:
            try:
                await db.rollback()
            except:
                pass
            logger.error(f"[get_context_tool] ❌ 获取上下文失败: {e}")
            return json.dumps({
                "error": f"获取上下文失败: {str(e)}",
                "work_id": work_id
            }, ensure_ascii=False, indent=2)

        finally:
            try:
                await db.close()
            except:
                pass


# ==================== 工具列表 ====================

# 导入编辑器工具
from app.services.agent.tools.editor_tools import (
    smart_continue,
    smart_rewrite,
    smart_insert,
    apply_chapter_edit
)

LANGGRAPH_TOOLS = [
    # 写作工具
    continue_writing_tool,
    analyze_text_tool,
    # 章节工具
    get_context_tool,
    read_chapter_tool,
    get_chapter_by_order_tool,
    search_analysis_fragments_tool,
    # 编辑器工具
    smart_continue,
    smart_rewrite,
    smart_insert,
    apply_chapter_edit
]

__all__ = [
    # 全局服务管理
    "set_global_ai_service",
    "get_global_ai_service",
    # 辅助函数
    "validate_uuid",
    "_retry_on_failure",
    "_generate_text_helper",
    # 写作工具
    "continue_writing_tool",
    "analyze_text_tool",
    # 章节工具
    "read_chapter_tool",
    "get_chapter_by_order_tool",
    "search_analysis_fragments_tool",
    "get_context_tool",
    # 工具列表
    "LANGGRAPH_TOOLS",
]
