"""
内容定位工具 - locate_content

职责单一：只负责定位，不生成内容

支持三种定位模式：
1. 段落定位：第N段
2. 语义定位：主角出场的地方（需要 LLM）
3. 精确定位：具体文本片段
"""
import re
import json
import logging
from typing import Optional, List, Dict, Any, Tuple
from difflib import SequenceMatcher

from langchain_core.tools import tool
from .tool_registry import register_as_tool
from app.core.database import AsyncSessionLocal
from app.services.ai.http_ai_service import HTTPAIService
from app.services.agent.model_selector import TaskType

logger = logging.getLogger(__name__)

# AI服务实例（延迟初始化）
_ai_service: Optional[HTTPAIService] = None


def _get_ai_service() -> HTTPAIService:
    """获取AI服务实例"""
    global _ai_service
    if _ai_service is None:
        _ai_service = HTTPAIService()
    return _ai_service


# ==================== 辅助函数 ====================

def _split_paragraphs(content: str) -> List[Dict[str, Any]]:
    """
    将内容分割为段落列表（与前端 Tiptap 编辑器保持一致）

    Args:
        content: 章节内容（HTML 格式）

    Returns:
        段落列表，每个包含 index, text, preview
    """
    paragraphs = []

    # 优先按 HTML <p> 标签分割（与前端 Tiptap 一致）
    if '<p' in content:
        # 匹配 <p>...</p>、<p ...>...</p>、<h1>...</h1> 等块级元素
        block_pattern = r'<(p|h[1-6]|blockquote|pre)[^>]*>(.*?)</\1>'
        matches = re.findall(block_pattern, content, re.DOTALL | re.IGNORECASE)

        for i, (tag, inner_html) in enumerate(matches):
            # 去除内部 HTML 标签，只保留文本
            text = re.sub(r'<[^>]+>', '', inner_html).strip()
            if text:  # 跳过空段落
                paragraphs.append({
                    "index": len(paragraphs),
                    "text": text,
                    "preview": text[:50] + "..." if len(text) > 50 else text
                })
    else:
        # 纯文本模式：按换行分割
        raw_paragraphs = re.split(r'\n\n+|\n', content)
        for para in raw_paragraphs:
            para = para.strip()
            if para:
                paragraphs.append({
                    "index": len(paragraphs),
                    "text": para,
                    "preview": para[:50] + "..." if len(para) > 50 else para
                })

    return paragraphs


def _parse_paragraph_query(query: str) -> Optional[int]:
    """
    解析段落定位查询

    支持格式：
    - "第3段" / "第三段"
    - "第1个段落"
    - "paragraph 3"

    Returns:
        段落索引（0-based），如果无法解析返回 None
    """
    # 中文数字映射
    cn_nums = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5,
               "六": 6, "七": 7, "八": 8, "九": 9, "十": 10}

    # 匹配 "第N段"
    match = re.search(r'第(\d+|[一二三四五六七八九十]+)段', query)
    if match:
        num_str = match.group(1)
        if num_str.isdigit():
            return int(num_str) - 1  # 转为 0-based
        elif num_str in cn_nums:
            return cn_nums[num_str] - 1

    # 匹配 "paragraph N"
    match = re.search(r'paragraph\s*(\d+)', query, re.IGNORECASE)
    if match:
        return int(match.group(1)) - 1

    return None


def _fuzzy_match_paragraphs(query: str, paragraphs: List[Dict[str, Any]], threshold: float = 0.5) -> Optional[Tuple[int, float]]:
    """
    使用相似度算法在段落中搜索最佳匹配

    Args:
        query: 搜索查询
        paragraphs: 段落列表
        threshold: 相似度阈值（0.0-1.0），默认 0.5

    Returns:
        (最佳匹配的段落索引, 相似度) 或 None
    """
    best_match = None
    best_ratio = 0.0

    # 规范化查询：去除多余空格
    normalized_query = re.sub(r'\s+', '', query)

    # 🔧 2026-01-12: 优化精确匹配逻辑 - 找到最精确匹配的段落，而不是第一个包含的段落
    exact_matches = []  # 收集所有完全包含匹配的段落

    for i, para in enumerate(paragraphs):
        text = para["text"]
        # 规范化段落文本
        normalized_text = re.sub(r'\s+', '', text)

        # 方法1：完全包含匹配 - 收集所有匹配，稍后选择最佳
        if normalized_query in normalized_text:
            # 计算匹配精确度：查询长度 / 段落长度（越接近1越精确）
            precision = len(normalized_query) / len(normalized_text) if normalized_text else 0
            exact_matches.append((i, precision))

        # 方法2：滑动窗口相似度匹配
        query_len = len(normalized_query)
        if query_len > 0 and len(normalized_text) >= query_len:
            # 在段落中滑动窗口查找最相似的部分
            for j in range(len(normalized_text) - query_len + 1):
                window = normalized_text[j:j + query_len]
                ratio = SequenceMatcher(None, normalized_query, window).ratio()
                if ratio > best_ratio:
                    best_ratio = ratio
                    best_match = i

        # 方法3：整体相似度（用于短文本）
        if query_len <= 20:
            # 对于短查询，检查段落开头的相似度
            head = normalized_text[:min(50, len(normalized_text))]
            ratio = SequenceMatcher(None, normalized_query, head).ratio()
            if ratio > best_ratio:
                best_ratio = ratio
                best_match = i

    # 🔧 如果有完全包含匹配，选择精确度最高的（查询占段落比例最大的）
    if exact_matches:
        # 按精确度降序排序，选择最精确的匹配
        exact_matches.sort(key=lambda x: x[1], reverse=True)
        best_idx, best_precision = exact_matches[0]
        logger.info(f"[_fuzzy_match] 完全包含匹配成功: 第{best_idx + 1}段, 精确度={best_precision:.2f}")
        return (best_idx, 1.0)

    if best_match is not None and best_ratio >= threshold:
        logger.info(f"[_fuzzy_match] 相似度匹配成功: 第{best_match + 1}段, 相似度={best_ratio:.2f}")
        return (best_match, best_ratio)

    return None


async def _llm_assisted_locate(
    query: str,
    paragraphs: List[Dict[str, Any]],
    top_k: int = 8
) -> Optional[Tuple[int, float]]:
    """
    LLM 辅助定位（当模糊匹配置信度低时使用）

    使用 lite 模型（gemini-2.5-flash-lite）进行语义理解

    Args:
        query: 用户查询
        paragraphs: 段落列表
        top_k: 候选段落数量

    Returns:
        (段落索引, 置信度) 或 None
    """
    if not paragraphs:
        return None

    # 🔧 2026-01-12: 基于相似度选择 top_k 个候选段落，而不是简单取前 top_k 个
    # 计算每个段落与查询的相似度
    normalized_query = re.sub(r'\s+', '', query)
    scored_paragraphs = []

    for i, para in enumerate(paragraphs):
        text = para["text"]
        normalized_text = re.sub(r'\s+', '', text)

        # 计算相似度（多种方法取最高）
        score = 0.0

        # 方法1：包含匹配
        if normalized_query in normalized_text:
            score = max(score, 0.8)

        # 方法2：关键词匹配（提取查询中的关键词）
        # 简单实现：按2-4字切分查询，检查段落是否包含
        for kw_len in [4, 3, 2]:
            if len(normalized_query) >= kw_len:
                for j in range(len(normalized_query) - kw_len + 1):
                    keyword = normalized_query[j:j + kw_len]
                    if keyword in normalized_text:
                        score = max(score, 0.5 + kw_len * 0.1)
                        break

        # 方法3：整体相似度
        ratio = SequenceMatcher(None, normalized_query[:50], normalized_text[:100]).ratio()
        score = max(score, ratio)

        scored_paragraphs.append((i, para, score))

    # 按相似度降序排序，取 top_k 个
    scored_paragraphs.sort(key=lambda x: x[2], reverse=True)
    top_candidates = scored_paragraphs[:min(top_k, len(scored_paragraphs))]

    # 构建候选列表（保留原始索引映射）
    candidates_text = "\n".join([
        f"{j + 1}. [第{orig_idx + 1}段] {para['preview']}"
        for j, (orig_idx, para, score) in enumerate(top_candidates)
    ])

    prompt = f"""用户想找的内容："{query}"

候选段落（按相关度排序）：
{candidates_text}

请选择最符合用户意图的段落编号（1-{len(top_candidates)}）。
只返回数字，不要解释。如果都不符合，返回 0。"""

    logger.info(f"[_llm_assisted_locate] 开始调用 LLM，候选数量: {len(top_candidates)}")

    try:
        ai_service = _get_ai_service()
        result = await ai_service.call_ai(
            system_prompt="你是内容定位助手，帮助用户找到正确的段落。",
            user_prompt=prompt,
            max_tokens=10,
            temperature=0.1,
            task_type=TaskType.SIMPLE_QA  # 使用 lite 模型
        )

        # 解析结果
        match = re.search(r'\d+', result.strip())
        if match:
            selected_idx = int(match.group()) - 1  # 转为 0-based
            if 0 <= selected_idx < len(top_candidates):
                # 映射回原始段落索引
                original_idx = top_candidates[selected_idx][0]
                logger.info(f"[_llm_assisted_locate] LLM 选择候选 {selected_idx + 1} → 原始第 {original_idx + 1} 段")
                return (original_idx, 0.85)  # LLM 辅助的置信度设为 0.85
            elif int(match.group()) == 0:
                logger.info("[_llm_assisted_locate] LLM 认为没有匹配的段落")
                return None

    except Exception as e:
        logger.warning(f"[_llm_assisted_locate] LLM 辅助定位失败: {e}")

    return None


async def _llm_rerank_global_results(
    query: str,
    candidates: List[Dict[str, Any]]
) -> Optional[Dict[str, Any]]:
    """
    LLM 重排序全局搜索结果

    当多个候选相似度接近时，用 LLM 判断哪个是"真正发生的场景"

    Args:
        query: 用户查询
        candidates: 候选结果列表（已排除当前章节）

    Returns:
        最佳候选或 None
    """
    if len(candidates) < 2:
        return candidates[0] if candidates else None

    # 优先使用 rerank_score（如果有），否则使用 similarity
    def get_score(c):
        return c.get("rerank_score", c.get("similarity", 0))

    sim1 = get_score(candidates[0])
    sim2 = get_score(candidates[1])
    if abs(sim1 - sim2) >= 0.15:
        return candidates[0]  # 差距明显，直接返回第一个

    logger.info(f"[_llm_rerank] top-2 相似度接近 ({sim1:.2f} vs {sim2:.2f})，调用 LLM 重排序")

    # 构建候选列表（最多取前3个）
    top_candidates = candidates[:min(3, len(candidates))]
    candidates_text = "\n".join([
        f"{i + 1}. [第{c.get('chapter_order', '?')}章 {c.get('chapter_title', '')}]: {c.get('content', '')[:80]}..."
        for i, c in enumerate(top_candidates)
    ])

    prompt = f"""用户想找的内容："{query}"

候选段落：
{candidates_text}

请判断哪个是用户要找的"真正发生的场景/动作"，而非"讨论/回忆/解释"。
只返回数字（1-{len(top_candidates)}），不要解释。"""

    try:
        ai_service = _get_ai_service()
        result = await ai_service.call_ai(
            system_prompt="你是内容定位助手，帮助区分'场景描写'和'概念讨论'。",
            user_prompt=prompt,
            max_tokens=10,
            temperature=0.1,
            task_type=TaskType.SIMPLE_QA
        )

        match = re.search(r'\d+', result.strip())
        if match:
            selected_idx = int(match.group()) - 1
            if 0 <= selected_idx < len(top_candidates):
                logger.info(f"[_llm_rerank] LLM 选择候选 {selected_idx + 1}")
                return top_candidates[selected_idx]

    except Exception as e:
        logger.warning(f"[_llm_rerank] LLM 重排序失败: {e}")

    return candidates[0]  # 失败时返回第一个


def _find_text_position(content: str, target_text: str) -> Optional[Dict[str, Any]]:
    """
    在内容中查找目标文本的位置

    Args:
        content: 章节内容
        target_text: 要查找的文本

    Returns:
        包含位置信息的字典，或 None
    """
    # 去除 HTML 标签
    text = re.sub(r'<[^>]+>', '', content)

    idx = text.find(target_text)
    if idx == -1:
        return None

    # 生成锚点
    before_anchor = text[max(0, idx - 30):idx] if idx > 0 else None
    end_idx = idx + len(target_text)
    after_anchor = text[end_idx:min(len(text), end_idx + 30)] if end_idx < len(text) else None

    return {
        "position": idx,
        "before_anchor": before_anchor,
        "after_anchor": after_anchor,
        "matched_text": target_text
    }


def _find_text_by_node_id(content: str, node_id: str) -> Optional[str]:
    """
    根据 data-id 从 HTML 中提取节点文本

    Args:
        content: 章节内容（HTML）
        node_id: 节点 ID（UniqueID）

    Returns:
        纯文本或 None
    """
    if not node_id:
        return None

    pattern = rf'<(p|h[1-6]|blockquote|pre)[^>]*\\sdata-id=["\\\']{re.escape(node_id)}["\\\'][^>]*>(.*?)</\\1>'
    match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
    if not match:
        return None

    inner_html = match.group(2)
    text = re.sub(r'<[^>]+>', '', inner_html).strip()
    return text if text else None


def _match_node_by_index(nodes_info: List[Dict], paragraph_index: int) -> Optional[str]:
    """
    根据段落索引从 nodes_info 中获取 node_id

    Args:
        nodes_info: 前端传入的节点列表
        paragraph_index: 段落索引

    Returns:
        node_id 或 None
    """
    if not nodes_info:
        return None

    if 0 <= paragraph_index < len(nodes_info):
        return nodes_info[paragraph_index].get("id")

    return None


# ==================== 主工具函数 ====================

@tool
@register_as_tool(
    "locate_content",
    "operation",
    """定位章节中的内容位置（只定位，不生成内容）。

【使用场景】：
- 用户说"把第三段改了" → 先用此工具定位第三段
- 用户说"修改主角出场的地方" → 先用此工具定位

【输入】：
- chapter_id: 章节ID
- query: 定位描述，如"第三段"、"开头"、"结尾"、具体文本片段
- nodes_info: [可选] 前端传入的节点列表

【输出】：
- node_id: 节点ID（如果前端传了nodes_info）
- paragraph_index: 段落索引
- text_preview: 内容预览
- before_anchor / after_anchor: 定位锚点"""
)
async def locate_content(
    chapter_id: str,
    query: str,
    nodes_info: Optional[str] = None,  # JSON 字符串格式的节点列表
    node_id: Optional[str] = None,  # node_id (front-end structural hint)
    user_id: Optional[str] = None
) -> str:
    """
    定位章节中的内容位置

    Args:
        chapter_id: 章节ID
        query: 定位查询（如"第三段"、"主角出场的地方"、具体文本）
        nodes_info: 前端传入的节点列表（JSON字符串）
        user_id: 用户ID

    Returns:
        JSON 格式的定位结果
    """
    try:
        logger.info(f"[locate_content] 开始定位: chapter_id={chapter_id}, query={query}")

        # 解析 nodes_info
        nodes_list = None
        if nodes_info:
            try:
                nodes_list = json.loads(nodes_info)
                logger.info(f"[locate_content] 收到 {len(nodes_list)} 个节点信息")
            except json.JSONDecodeError:
                logger.warning("[locate_content] nodes_info 解析失败")

        # 获取章节内容
        chapter_content = ""
        work_id = None  # 用于全局降级
        chapter_title = ""
        async with AsyncSessionLocal() as db:
            from app.services.chapter_service import ChapterService
            chapter_svc = ChapterService(db)
            chapter = await chapter_svc.get_chapter_by_id(chapter_id)
            if chapter and chapter.content:
                chapter_content = chapter.content
                work_id = str(chapter.work_id) if chapter.work_id else None
                chapter_title = chapter.title or ""

        if not chapter_content:
            return json.dumps({
                "success": False,
                "error": "chapter_empty",
                "message": f"章节内容为空: {chapter_id}"
            }, ensure_ascii=False)

        # 分割段落
        paragraphs = _split_paragraphs(chapter_content)
        logger.info(f"[locate_content] 章节共 {len(paragraphs)} 个段落")

        # ===== 定位策略 =====

        result = {
            "success": True,
            "query": query,
            "chapter_id": chapter_id,
            "total_paragraphs": len(paragraphs)
        }

        # Structured locate: node_id hint from front-end
        if node_id:
            node_text = _find_text_by_node_id(chapter_content, node_id)
            node_para_index = None
            if nodes_list:
                for i, node in enumerate(nodes_list):
                    if node.get("id") == node_id:
                        node_para_index = i
                        break

            if node_text is None and node_para_index is not None and 0 <= node_para_index < len(paragraphs):
                node_text = paragraphs[node_para_index]["text"]

            result.update({
                "locate_method": "node_id",
                "paragraph_index": node_para_index,
                "text_preview": (node_text[:50] + "...") if node_text and len(node_text) > 50 else (node_text or ""),
                "text": node_text or "",
                "node_id": node_id,
                "confidence": 1.0
            })

            if node_para_index is not None and 0 <= node_para_index < len(paragraphs):
                if node_para_index > 0:
                    result["before_anchor"] = paragraphs[node_para_index - 1]["text"][-30:]
                if node_para_index < len(paragraphs) - 1:
                    result["after_anchor"] = paragraphs[node_para_index + 1]["text"][:30]

            logger.info(f"[locate_content] node_id locate success: {node_id}")
            return json.dumps(result, ensure_ascii=False)


        # 策略1: 段落索引定位（第N段）
        para_index = _parse_paragraph_query(query)
        if para_index is not None:
            if 0 <= para_index < len(paragraphs):
                para = paragraphs[para_index]
                result.update({
                    "locate_method": "paragraph_index",
                    "paragraph_index": para_index,
                    "text_preview": para["preview"],
                    "text": para["text"],
                    "node_id": _match_node_by_index(nodes_list, para_index),
                    "confidence": 1.0
                })

                # 生成锚点
                if para_index > 0:
                    result["before_anchor"] = paragraphs[para_index - 1]["text"][-30:]
                if para_index < len(paragraphs) - 1:
                    result["after_anchor"] = paragraphs[para_index + 1]["text"][:30]

                logger.info(f"[locate_content] 段落定位成功: 第{para_index + 1}段")
                return json.dumps(result, ensure_ascii=False)
            else:
                return json.dumps({
                    "success": False,
                    "error": "paragraph_out_of_range",
                    "message": f"段落索引超出范围，共{len(paragraphs)}段，请求第{para_index + 1}段"
                }, ensure_ascii=False)

        # 策略2: 特殊位置（开头/结尾）
        query_lower = query.lower()
        if any(kw in query_lower for kw in ["开头", "开篇", "第一段", "开始"]):
            para = paragraphs[0]
            result.update({
                "locate_method": "keyword",
                "paragraph_index": 0,
                "text_preview": para["preview"],
                "text": para["text"],
                "node_id": _match_node_by_index(nodes_list, 0),
                "confidence": 0.95
            })
            logger.info("[locate_content] 定位到开头")
            return json.dumps(result, ensure_ascii=False)

        if any(kw in query_lower for kw in ["结尾", "末尾", "最后", "结束", "最后一段"]):
            last_idx = len(paragraphs) - 1
            para = paragraphs[last_idx]
            result.update({
                "locate_method": "keyword",
                "paragraph_index": last_idx,
                "text_preview": para["preview"],
                "text": para["text"],
                "node_id": _match_node_by_index(nodes_list, last_idx),
                "confidence": 0.95
            })
            logger.info("[locate_content] 定位到结尾")
            return json.dumps(result, ensure_ascii=False)

        # 策略3: 精确文本匹配（🔧 移除长度限制，支持任意长度查询）
        if len(query) > 0:
            text_result = _find_text_position(chapter_content, query)
            if text_result:
                # 找到对应的段落索引
                found_para_index = None
                # 规范化查询进行匹配
                normalized_query = re.sub(r'\s+', '', query)
                for i, para in enumerate(paragraphs):
                    normalized_text = re.sub(r'\s+', '', para["text"])
                    if normalized_query in normalized_text:
                        found_para_index = i
                        break

                result.update({
                    "locate_method": "exact_match",
                    "paragraph_index": found_para_index,
                    "text_preview": query[:50] + "..." if len(query) > 50 else query,
                    "text": query,
                    "node_id": _match_node_by_index(nodes_list, found_para_index) if found_para_index is not None else None,
                    "before_anchor": text_result["before_anchor"],
                    "after_anchor": text_result["after_anchor"],
                    "confidence": 1.0
                })
                logger.info("[locate_content] 精确文本匹配成功")
                return json.dumps(result, ensure_ascii=False)

        # 策略4: 模糊匹配 + LLM 辅助
        # 🔧 2026-01-12: 当模糊匹配置信度 < 0.7 时，调用 LLM 辅助定位
        fuzzy_result = _fuzzy_match_paragraphs(query, paragraphs, threshold=0.5)
        logger.info(f"[locate_content] 模糊匹配结果: {fuzzy_result}")

        if fuzzy_result:
            para_idx, similarity = fuzzy_result

            # 置信度 >= 0.7，直接返回模糊匹配结果
            if similarity >= 0.7:
                para = paragraphs[para_idx]
                result.update({
                    "locate_method": "fuzzy_match",
                    "paragraph_index": para_idx,
                    "text_preview": para["preview"],
                    "text": para["text"],
                    "node_id": _match_node_by_index(nodes_list, para_idx),
                    "confidence": similarity
                })
                logger.info(f"[locate_content] 模糊匹配成功: 第{para_idx + 1}段, 相似度={similarity:.2f}")
                return json.dumps(result, ensure_ascii=False)

            # 置信度 < 0.7，调用 LLM 辅助定位
            logger.info(f"[locate_content] 模糊匹配置信度低({similarity:.2f})，调用 LLM 辅助定位")
            llm_result = await _llm_assisted_locate(query, paragraphs, top_k=8)

            if llm_result:
                llm_idx, llm_confidence = llm_result
                para = paragraphs[llm_idx]
                result.update({
                    "locate_method": "llm_assisted",
                    "paragraph_index": llm_idx,
                    "text_preview": para["preview"],
                    "text": para["text"],
                    "node_id": _match_node_by_index(nodes_list, llm_idx),
                    "confidence": llm_confidence
                })
                # 生成锚点
                if llm_idx > 0:
                    result["before_anchor"] = paragraphs[llm_idx - 1]["text"][-30:]
                if llm_idx < len(paragraphs) - 1:
                    result["after_anchor"] = paragraphs[llm_idx + 1]["text"][:30]
                logger.info(f"[locate_content] LLM 辅助定位成功: 第{llm_idx + 1}段")
                return json.dumps(result, ensure_ascii=False)

            # LLM 也无法定位，降级返回模糊匹配结果
            para = paragraphs[para_idx]
            result.update({
                "locate_method": "fuzzy_match",
                "paragraph_index": para_idx,
                "text_preview": para["preview"],
                "text": para["text"],
                "node_id": _match_node_by_index(nodes_list, para_idx),
                "confidence": similarity
            })
            logger.info(f"[locate_content] LLM 辅助失败，降级使用模糊匹配: 第{para_idx + 1}段")
            return json.dumps(result, ensure_ascii=False)

        # 策略5: 无模糊匹配结果，尝试 LLM 辅助
        logger.info("[locate_content] 无模糊匹配结果，尝试 LLM 辅助定位")
        try:
            llm_result = await _llm_assisted_locate(query, paragraphs, top_k=8)
            logger.info(f"[locate_content] LLM 辅助定位返回: {llm_result}")
        except Exception as e:
            logger.error(f"[locate_content] LLM 辅助定位异常: {e}", exc_info=True)
            llm_result = None

        if llm_result:
            llm_idx, llm_confidence = llm_result
            para = paragraphs[llm_idx]
            result.update({
                "locate_method": "llm_assisted",
                "paragraph_index": llm_idx,
                "text_preview": para["preview"],
                "text": para["text"],
                "node_id": _match_node_by_index(nodes_list, llm_idx),
                "confidence": llm_confidence
            })
            if llm_idx > 0:
                result["before_anchor"] = paragraphs[llm_idx - 1]["text"][-30:]
            if llm_idx < len(paragraphs) - 1:
                result["after_anchor"] = paragraphs[llm_idx + 1]["text"][:30]
            logger.info(f"[locate_content] LLM 辅助定位成功: 第{llm_idx + 1}段")
            return json.dumps(result, ensure_ascii=False)

        # 策略6: 全局降级 - 在整个作品中搜索
        if work_id:
            logger.info(f"[locate_content] 章节内未找到，尝试全局搜索: work_id={work_id}")
            try:
                async with AsyncSessionLocal() as db:
                    from app.services.search.hybrid_retriever import HybridRetriever
                    retriever = HybridRetriever(db)
                    global_results = await retriever.search(
                        work_id=work_id,
                        query=query,
                        top_k=5,  # 增加到5，确保有足够的跨章节候选
                        current_order=None,  # 不限制时序
                        look_ahead=None,
                    )

                    if global_results:
                        # 过滤掉当前章节（章节内定位已失败，说明内容不在当前章节）
                        other_chapter_results = [
                            r for r in global_results
                            if r.get("chapter_id") and r.get("chapter_id") != chapter_id
                        ]

                        # 初始化变量
                        best = None
                        target_chapter_id = None
                        target_paragraph_index = None

                        if not other_chapter_results:
                            logger.info(f"[locate_content] 全局搜索结果都在当前章节，跳过")
                        else:
                            # LLM 重排序（当 top-2 相似度接近时）
                            best = await _llm_rerank_global_results(query, other_chapter_results)
                            if best:
                                target_chapter_id = best.get("chapter_id")
                                target_paragraph_index = best.get("paragraph_index")

                        # 如果向量检索直接返回了 paragraph_index，直接使用
                        if best and target_chapter_id and target_paragraph_index is not None:
                            result.update({
                                "locate_method": "global_fallback",
                                "chapter_id": target_chapter_id,
                                "chapter_title": best.get("chapter_title", ""),
                                "paragraph_index": target_paragraph_index,
                                "text_preview": best.get("content", "")[:50] + "...",
                                "text": best.get("content", ""),
                                "confidence": best.get("similarity", 0.7),
                                "cross_chapter": target_chapter_id != chapter_id
                            })
                            logger.info(f"[locate_content] 全局降级成功: chapter={target_chapter_id}, para={target_paragraph_index}")
                            return json.dumps(result, ensure_ascii=False)

                        # 如果没有 paragraph_index（全文检索结果），需要在目标章节内二次定位
                        elif best and target_chapter_id:
                            # 获取目标章节内容并定位
                            from app.services.chapter_service import ChapterService
                            chapter_svc = ChapterService(db)
                            target_chapter = await chapter_svc.get_chapter_by_id(target_chapter_id)
                            if target_chapter and target_chapter.content:
                                target_paragraphs = _split_paragraphs(target_chapter.content)
                                # 用全局搜索返回的 content 进行精确匹配
                                match_result = _fuzzy_match_paragraphs(best.get("content", ""), target_paragraphs, threshold=0.3)
                                if match_result:
                                    para_idx, similarity = match_result
                                    para = target_paragraphs[para_idx]
                                    result.update({
                                        "locate_method": "global_fallback",
                                        "chapter_id": target_chapter_id,
                                        "chapter_title": target_chapter.title or "",
                                        "paragraph_index": para_idx,
                                        "text_preview": para["preview"],
                                        "text": para["text"],
                                        "confidence": similarity * 0.8,  # 降低置信度
                                        "cross_chapter": target_chapter_id != chapter_id
                                    })
                                    logger.info(f"[locate_content] 全局降级+二次定位成功: chapter={target_chapter_id}, para={para_idx}")
                                    return json.dumps(result, ensure_ascii=False)

            except Exception as e:
                logger.warning(f"[locate_content] 全局降级失败: {e}")

        # 策略7: 返回段落列表，让调用方选择
        result.update({
            "locate_method": "list",
            "message": "无法自动定位，请从以下段落中选择",
            "paragraphs": [
                {"index": p["index"], "preview": p["preview"]}
                for p in paragraphs[:10]  # 最多返回前10段
            ],
            "confidence": 0.0
        })
        logger.info("[locate_content] 无法自动定位，返回段落列表")
        return json.dumps(result, ensure_ascii=False)

    except Exception as e:
        logger.error(f"[locate_content] 定位失败: {e}", exc_info=True)
        return json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False)


# ==================== 导出 ====================

__all__ = [
    "locate_content"
]
