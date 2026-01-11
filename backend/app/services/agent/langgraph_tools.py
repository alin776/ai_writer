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
from typing import Optional

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


# ==================== 章节工具 ====================

@tool
async def read_chapter_tool(work_id: Optional[str] = None, chapter_id: str = "") -> str:
    """读取指定章节工具：从数据库读取单个或多个章节内容

    Args:
        work_id: 作品ID（UUID格式）
        chapter_id: 章节ID（UUID格式或章节序号）或多个章节引用（用逗号分隔，如 "id1,id2,id3" 或 "1,2,3"）

    Returns:
        章节信息JSON（单章节）或章节列表JSON（多章节）

    🔧 2025-12-15: 支持章节序号自动转 UUID
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
    chapter_refs = [cid.strip() for cid in chapter_id.split(",") if cid.strip()]

    # 🔧 2025-12-15: 智能解析章节引用（支持 UUID 或序号）
    chapter_ids = []
    for ref in chapter_refs:
        resolved_id, resolve_error = await resolve_chapter_id(work_id, ref)
        if resolve_error:
            return resolve_error
        if resolved_id:
            chapter_ids.append(resolved_id)

    async with AsyncSessionLocal() as db:
        try:
            from app.services.chapter_service import ChapterService

            chapter_service = ChapterService(db)

            # 🆕 多章节处理
            if len(chapter_ids) > 1:
                # 🔧 2025-12-25: 智能压缩 - 与 get_chapter_by_order_tool 保持一致
                content_limit = _get_content_limit_for_batch(len(chapter_ids))
                is_compressed = content_limit < 5000

                chapters_info = []
                for cid in chapter_ids:
                    chapter = await _retry_on_failure(
                        chapter_service.get_chapter_by_id,
                        cid,
                        max_retries=2
                    )

                    if chapter:
                        # 清理 HTML 标签
                        from app.utils.text_cleaner import text_cleaner
                        clean_content = text_cleaner.html_to_clean_text(
                            chapter.content if chapter.content else "",
                            preserve_structure=False
                        )
                        chapters_info.append({
                            "chapter_id": str(chapter.id),
                            "title": chapter.title,
                            "order": chapter.order,
                            "content": clean_content[:content_limit] if clean_content else "",
                            "content_length": len(clean_content) if clean_content else 0,
                            "word_count": chapter.word_count,
                            "status": chapter.status.value if hasattr(chapter, 'status') else "unknown"
                        })
                    else:
                        chapters_info.append({
                            "chapter_id": cid,
                            "error": f"未找到章节 {cid}"
                        })

                compression_note = f"（已压缩，每章限制{content_limit}字）" if is_compressed else ""
                logger.info(f"[read_chapter_tool] ✅ 读取多章节成功: 共 {len(chapters_info)} 章{compression_note}")

                result = {
                    "type": "multi_chapter",
                    "count": len(chapters_info),
                    "chapters": chapters_info
                }
                if is_compressed:
                    result["compression_note"] = f"由于章节数量较多（{len(chapter_ids)}章），每章内容已压缩至{content_limit}字以内"

                return json.dumps(result, ensure_ascii=False, indent=2)

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

                # 清理 HTML 标签
                from app.utils.text_cleaner import text_cleaner
                clean_content = text_cleaner.html_to_clean_text(
                    chapter.content if chapter.content else "",
                    preserve_structure=False
                )

                chapter_info = {
                    "chapter_id": str(chapter.id),
                    "title": chapter.title,
                    "order": chapter.order,
                    "content": clean_content[:5000] if clean_content else "",
                    "content_length": len(clean_content) if clean_content else 0,
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


def _parse_chapter_orders(chapter_order: str) -> list[int]:
    """解析章节序号参数，支持三种格式

    Args:
        chapter_order: 章节序号，支持以下格式：
            - 单个: "1" 或 1
            - 多个: "1,2,3,4,5"
            - 范围: "1-5"（读取第1到第5章）

    Returns:
        章节序号列表，如 [1, 2, 3, 4, 5]
    """
    # 处理整数输入（向后兼容）
    if isinstance(chapter_order, int):
        return [chapter_order]

    chapter_order = str(chapter_order).strip()

    # 格式1: 范围 "1-5"
    if "-" in chapter_order and "," not in chapter_order:
        parts = chapter_order.split("-")
        if len(parts) == 2:
            try:
                start = int(parts[0].strip())
                end = int(parts[1].strip())
                if start <= end:
                    return list(range(start, end + 1))
            except ValueError:
                pass

    # 格式2: 多个 "1,2,3,4,5"
    if "," in chapter_order:
        orders = []
        for part in chapter_order.split(","):
            try:
                orders.append(int(part.strip()))
            except ValueError:
                continue
        return sorted(set(orders))  # 去重并排序

    # 格式3: 单个 "1"
    try:
        return [int(chapter_order)]
    except ValueError:
        return [1]  # 默认返回第1章


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
    """通过章节序号获取章节内容（支持批量读取）

    Args:
        work_id: 作品ID（UUID格式）
        chapter_order: 章节序号，支持三种格式：
                      - 单个: "1"
                      - 多个: "1,2,3,4,5"
                      - 范围: "1-5"（读取第1到第5章）

    Returns:
        章节信息JSON（单章节）或章节列表JSON（多章节）

    🔧 2025-12-25: 优化支持多章节批量读取，减少规划任务数
    """
    # 解析章节序号
    orders = _parse_chapter_orders(chapter_order)

    if not work_id:
        order_desc = f"第{orders[0]}章" if len(orders) == 1 else f"第{orders[0]}-{orders[-1]}章"
        return json.dumps({
            "status": "missing_prerequisite",
            "missing": "work_id",
            "message": f"需要指定作品ID才能查询{order_desc}"
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

            # 构建章节序号到章节的映射
            chapter_map = {ch.order: ch for ch in work.chapters}

            # 🆕 多章节处理
            if len(orders) > 1:
                # 🔧 2025-12-25: 智能压缩 - 根据章节数量动态调整每章内容限制
                content_limit = _get_content_limit_for_batch(len(orders))
                is_compressed = content_limit < 5000

                chapters_info = []
                for order in orders:
                    chapter = chapter_map.get(order)
                    if chapter:
                        clean_content = text_cleaner.html_to_clean_text(
                            chapter.content if chapter.content else "",
                            preserve_structure=True,
                            max_length=content_limit
                        )
                        chapters_info.append({
                            "chapter_id": str(chapter.id),
                            "title": chapter.title,
                            "order": chapter.order,
                            "content": clean_content,
                            "content_length": len(clean_content),
                            "word_count": chapter.word_count,
                            "status": chapter.status.value if hasattr(chapter, 'status') else "unknown"
                        })
                    else:
                        chapters_info.append({
                            "order": order,
                            "error": f"未找到第{order}章"
                        })

                compression_note = f"（已压缩，每章限制{content_limit}字）" if is_compressed else ""
                logger.info(f"[get_chapter_by_order_tool] ✅ 批量读取成功: 共 {len(chapters_info)} 章{compression_note}")

                result = {
                    "type": "multi_chapter",
                    "count": len(chapters_info),
                    "chapters": chapters_info
                }
                # 如果启用了压缩，添加提示信息
                if is_compressed:
                    result["compression_note"] = f"由于章节数量较多（{len(orders)}章），每章内容已压缩至{content_limit}字以内"

                return json.dumps(result, ensure_ascii=False, indent=2)

            # 单章节处理（保持原有逻辑）
            target_order = orders[0]
            target_chapter = chapter_map.get(target_order)

            if not target_chapter:
                return json.dumps({
                    "error": f"未找到第{target_order}章",
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

            logger.info(f"[get_chapter_by_order_tool] ✅ 找到第{target_order}章: {target_chapter.title}")
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
async def search_analysis_fragments_tool(
    work_id: str,
    query: str,
    top_k: int = 5,
    chapter_id: str = "",
    include_current: bool = True,
    look_ahead: int = 0,
    max_content_length: int = 2000
) -> str:
    """检索分析碎片工具：混合检索（向量+全文），召回作品相关片段

    Args:
        work_id: 作品ID（UUID格式，必需）
        query: 查询文本（必需）
        top_k: 返回前K个最相关结果
        chapter_id: 当前章节ID（可选，用于确定时序窗口）
        include_current: 是否包含当前章
        look_ahead: 允许向后看的章节数（默认0表示不限制，检索所有章节）
        max_content_length: 返回内容的最大长度（默认2000）

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
            results = await retriever.search(
                work_id=work_id,
                query=query,
                current_order=current_order,
                top_k=top_k,
                include_current=include_current,
                look_ahead=look_ahead if look_ahead > 0 else None,
            )

            if not results:
                return json.dumps({
                    "message": "未找到相关片段",
                    "work_id": work_id,
                    "query": query,
                    "results": []
                }, ensure_ascii=False, indent=2)

            formatted_results = []
            for i, result in enumerate(results):
                formatted_results.append({
                    "rank": i + 1,
                    "chapter_id": result.get("chapter_id"),  # 新增
                    "similarity": result.get("similarity", 0),
                    "chapter_title": result.get("chapter_title"),
                    "chapter_order": result.get("chapter_order"),
                    "paragraph_index": result.get("paragraph_index"),  # 新增
                    "content": result.get("content", "")[:max_content_length],
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
                    # 清理 HTML 标签
                    from app.utils.text_cleaner import text_cleaner
                    clean_preview = text_cleaner.html_to_clean_text(
                        chapter.content[:1200] if chapter.content else "",
                        preserve_structure=False
                    )
                    context_info["current_chapter"] = {
                        "chapter_id": str(chapter.id),
                        "title": chapter.title,
                        "order": chapter.order,
                        "content_preview": clean_preview[:1000] if clean_preview else "",
                        "word_count": chapter.word_count
                    }

            # 3. RAG检索章节上下文
            try:
                current_order = None  # 默认无限制检索
                if chapter_id:
                    chapter = await chapter_service.get_chapter_by_id(chapter_id)
                    if chapter:
                        current_order = chapter.order

                query = "作品背景、人物关系、情节发展、伏笔线索"
                chapter_rag_results = await _retry_on_failure(
                    chapter_vector_service.retrieve_for_writing,
                    work_id=work_id,
                    current_chapter_order=current_order if current_order is not None else 10**6,  # 无限制时使用大数
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


# ==================== 世界观查询工具 ====================

@tool
async def get_worldview_summary(work_id: str) -> str:
    """获取作品的世界观摘要信息

    这个工具用于查询作品中已保存的世界观内容，包括：
    - 角色列表及其描述、关系
    - 地点列表及其描述
    - 世界设定列表（魔法体系、规则等）

    适用场景：
    - 用户询问"世界观里有什么"、"有哪些角色"等问题时使用
    - 需要了解作品全局设定时使用

    参数:
        work_id: 作品ID（UUID格式）

    返回:
        JSON格式的世界观摘要，包含characters、locations、settings三个部分

    示例:
        work_id = "627feba4-2097-4f28-a3f3-7641d10f7f40"
    """
    # 验证 work_id 格式
    uuid_error = validate_uuid(work_id, "作品ID")
    if uuid_error:
        return uuid_error

    async with AsyncSessionLocal() as db:
        try:
            from app.services.worldview_service import WorldviewService

            worldview_service = WorldviewService(db)

            # 获取世界观数据
            characters = await worldview_service.get_characters_by_work(work_id)
            locations = await worldview_service.get_locations_by_work(work_id)
            settings = await worldview_service.get_settings_by_work(work_id)

            # 构建摘要
            summary = {
                "total": {
                    "characters": len(characters),
                    "locations": len(locations),
                    "settings": len(settings)
                },
                "characters": [],
                "locations": [],
                "settings": []
            }

            # 添加角色信息
            for char in characters:
                char_info = {
                    "name": char.name,
                    "role": char.role if hasattr(char, 'role') else "",
                    "description": char.description[:200] if char.description else ""
                }
                if hasattr(char, 'tags') and char.tags:
                    char_info["tags"] = char.tags[:5]  # 最多5个标签
                summary["characters"].append(char_info)

            # 添加地点信息
            for loc in locations:
                loc_info = {
                    "name": loc.name,
                    "type": loc.type if hasattr(loc, 'type') else "",
                    "description": loc.description[:200] if loc.description else ""
                }
                summary["locations"].append(loc_info)

            # 添加设定信息
            for setting in settings:
                setting_info = {
                    "title": setting.title,
                    "category": setting.category if hasattr(setting, 'category') else "",
                    "content": setting.content[:200] if setting.content else ""
                }
                summary["settings"].append(setting_info)

            logger.info(f"[get_worldview_summary] ✅ 获取世界观摘要成功: {summary['total']}")
            return json.dumps(summary, ensure_ascii=False, indent=2)

        except Exception as e:
            logger.error(f"[get_worldview_summary] 获取世界观摘要失败: {e}", exc_info=True)
            return json.dumps({
                "error": "获取世界观摘要失败",
                "message": str(e)
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
    create_chapter,
    update_chapter_title,
    delete_chapter,
    update_chapter_content
)

# 导入辅助工具（2026-01-09）
from app.services.agent.tools.consistency_checker import check_story_consistency_tool
from app.services.agent.tools.show_dont_tell import show_emotion_tool, enhance_scene_tool
from app.services.agent.tools.style_learning import learn_style_tool, get_style_guidance_tool, analyze_style_tool

# 导入定位工具（2026-01-10）
from app.services.agent.tools.locate_tools import locate_content

LANGGRAPH_TOOLS = [
    # 查询工具
    get_context_tool,
    read_chapter_tool,
    get_chapter_by_order_tool,
    search_analysis_fragments_tool,
    get_worldview_summary,
    get_style_guidance_tool,
    # 分析工具
    analyze_text_tool,
    check_story_consistency_tool,
    analyze_style_tool,
    # 定位工具（2026-01-10）
    locate_content,
    # 创作工具
    smart_continue,
    smart_rewrite,
    smart_insert,
    show_emotion_tool,
    enhance_scene_tool,
    learn_style_tool,
    # 操作工具
    apply_chapter_edit,
    create_chapter,
    update_chapter_title,
    delete_chapter,
    update_chapter_content,
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
    # 章节工具
    "read_chapter_tool",
    "get_chapter_by_order_tool",
    "search_analysis_fragments_tool",
    "get_context_tool",
    # 世界观工具
    "get_worldview_summary",
    # 工具列表
    "LANGGRAPH_TOOLS",
    # StandardTool 版本（2025-12-14）
    "get_context_tool_st",
    "read_chapter_tool_st",
    "get_chapter_by_order_tool_st",
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
    max_content_length: int = Field(default=2000, description="返回内容的最大长度", ge=100, le=10000)


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


# ==================== 5. GetWorldviewSummaryTool StandardTool ====================

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

