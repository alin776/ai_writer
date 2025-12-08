"""反思工具和逻辑

基于 Deep Agents 的 think_tool 设计，实现纯上下文工程的反思能力。
"""

import json
import logging
import asyncio
from dataclasses import dataclass
from typing import Dict, Any, List, Optional

from .config import DeepAgentConfig

logger = logging.getLogger(__name__)


@dataclass
class ReflectionResult:
    """反思结果"""
    reflection: str           # 反思内容
    needs_replan: bool        # 是否需要重规划
    suggested_tasks: Optional[List[str]] = None  # 建议的新任务


async def think_tool(
    task: Dict[str, Any],
    result: Dict[str, Any],
    remaining_tasks: List[Dict[str, Any]],
    context: Dict[str, Any],
    agent_graph: Optional[Any] = None,  # WritingAgentGraph 实例（复用 _generate_text 抽象层）
) -> ReflectionResult:
    """反思工具

    纯上下文工程工具，迫使 Agent 在关键节点评估进度。
    使用 agent_graph._generate_text() 复用已有的 AI 调用抽象层。

    Args:
        task: 刚执行完的任务
        result: 任务执行结果
        remaining_tasks: 剩余待执行的任务
        context: 上下文信息
        agent_graph: WritingAgentGraph 实例

    Returns:
        ReflectionResult: 反思结果
    """
    # P1-1: 空值检查
    if agent_graph is None:
        logger.warning("agent_graph 为空，跳过反思")
        return ReflectionResult(reflection="agent_graph 未初始化，跳过反思", needs_replan=False)

    prompt = _build_reflection_prompt(task, result, remaining_tasks)

    try:
        # 复用 _generate_text 抽象层（支持 ChatOpenAI/HTTPAIService 双模式）
        response = await asyncio.wait_for(
            agent_graph._generate_text(
                prompt=prompt,
                temperature=0.3,
                max_tokens=500,
            ),
            timeout=DeepAgentConfig.REFLECTION_TIMEOUT
        )

        # 检查是否有错误
        if response.get("error"):
            logger.warning(f"反思 AI 调用失败: {response.get('error')}")
            return ReflectionResult(reflection="AI 调用失败，继续执行", needs_replan=False)

        content = response.get("text", "")
        if not content:
            logger.warning("反思响应为空")
            return ReflectionResult(reflection="响应为空，继续执行", needs_replan=False)

        return _parse_reflection_response(content)

    except asyncio.TimeoutError:
        logger.warning("反思超时")
        return ReflectionResult(reflection="反思超时，继续执行", needs_replan=False)
    except Exception as e:
        logger.error(f"反思失败: {e}")
        return ReflectionResult(reflection=f"反思异常: {str(e)}", needs_replan=False)


def _build_reflection_prompt(
    task: Dict[str, Any],
    result: Dict[str, Any],
    remaining_tasks: List[Dict[str, Any]],
) -> str:
    """构建反思 Prompt"""
    task_desc = task.get("description", "未知任务")
    task_status = result.get("status", "unknown")

    # 获取任务输出摘要
    task_output = result.get("output", result.get("content", ""))
    if isinstance(task_output, str) and len(task_output) > 300:
        task_output = task_output[:300] + "..."
    elif isinstance(task_output, dict):
        task_output = json.dumps(task_output, ensure_ascii=False)[:300]

    # 构建剩余任务列表
    remaining_str = "\n".join([
        f"  - {t.get('description', '未知')}"
        for t in remaining_tasks[:5]
    ]) if remaining_tasks else "  (无剩余任务)"

    return f"""你是一个 AI Agent，刚完成了一个任务。请简短反思。

## 刚完成的任务
- 描述: {task_desc}
- 状态: {task_status}
- 输出: {task_output}

## 剩余任务
{remaining_str}

## 请思考
1. 结果是否达到预期？
2. 是否发现需要补充的信息？
3. 剩余任务是否仍然合理？

## 输出格式
第一行必须是决策标记：REPLAN:YES 或 REPLAN:NO
然后是简短反思（<100字）

示例：
REPLAN:NO
分析结果符合预期，后续任务规划合理，继续执行。
"""


def _parse_reflection_response(response: str) -> ReflectionResult:
    """解析反思响应

    解析标记式输出格式：
    第一行：REPLAN:YES 或 REPLAN:NO
    后续行：反思内容

    ?? 2025-12-08: 简化解析逻辑，移除 JSON 解析和关键词匹配
    ?? 2025-12-08: 扩展判定规则，支持中文/同义表达，避免模型输出微调导致的漏判
    """
    raw_text = (response or "").strip()
    lines = [line.strip() for line in raw_text.splitlines() if line.strip()]

    first_line = lines[0].upper() if lines else ""

    positive_markers = ("REPLAN:YES", "REPLAN YES", "REPLAN=YES", "REPLAN TRUE", "REPLAN: TRUE", "REPLAN: Y")
    negative_markers = ("REPLAN:NO", "REPLAN NO", "REPLAN=NO", "REPLAN FALSE", "REPLAN: FALSE", "REPLAN: N")

    contains_positive_marker = any(m in first_line for m in positive_markers)
    contains_negative_marker = any(m in first_line for m in negative_markers)

    positive_cn_keywords = (
        "需要重新规划", "需要重规划", "重新规划", "重规划", "重新计划",
        "调整后续任务", "改一下计划", "补充任务", "调整任务"
    )
    negative_cn_keywords = (
        "无需重规划", "不需要重规划", "无需重新规划", "不需要调整", "保持原计划", "继续执行"
    )

    needs_replan_cn = any(k in raw_text for k in positive_cn_keywords)
    no_replan_cn = any(k in raw_text for k in negative_cn_keywords)

    needs_replan = False
    if contains_positive_marker:
        needs_replan = True
    elif contains_negative_marker:
        needs_replan = False
    elif no_replan_cn:
        needs_replan = False
    elif needs_replan_cn:
        needs_replan = True

    # 如果仍未决策，允许第一行包含 REPLAN 但未写 YES/NO 时，用关键词兜底
    if not needs_replan and not contains_negative_marker and "REPLAN" in first_line:
        if "YES" in first_line or "TRUE" in first_line:
            needs_replan = True

    reflection = "\n".join(lines[1:]).strip() if len(lines) > 1 else raw_text
    if not reflection:
        reflection = raw_text

    logger.info(
        "[Reflection] 解析结果: needs_replan=%s, first_line=%s, raw_len=%s",
        needs_replan, first_line[:80], len(raw_text)
    )

    return ReflectionResult(reflection=reflection, needs_replan=needs_replan)


def should_reflect(
    task: Dict[str, Any],
    result: Dict[str, Any],
    completed_count: int,
    reflection_count: int,
) -> bool:
    """判断是否需要触发反思

    基于 LangChain DeepAgents 设计理念重构：
    - 优先检查 AI 在规划阶段标记的 checkpoint 字段
    - 保留任务失败时的兜底反思

    Args:
        task: 当前任务
        result: 任务结果
        completed_count: 已完成任务数
        reflection_count: 已反思次数

    Returns:
        bool: 是否需要反思

    🔧 2025-12-08: 重构 - 基于 checkpoint 字段判断，让 AI 决定何时反思
    """
    config = DeepAgentConfig

    # 1. 达到上限检查
    if reflection_count >= config.MAX_REFLECTIONS:
        logger.debug(f"已达到最大反思次数 ({config.MAX_REFLECTIONS})，跳过反思")
        return False

    # 2. ✅ 新增：检查 AI 标记的 checkpoint 字段（核心逻辑）
    #    这是 Agent 模式的核心：让 AI 在规划时就决定哪些任务需要反思
    if task.get("checkpoint") is True:
        task_id = task.get("task_id", "?")
        logger.info(f"[Checkpoint] 任务 {task_id} 标记了 checkpoint，触发反思")
        return True

    # 3. 任务失败时兜底反思
    if config.REFLECT_ON_FAILURE and result.get("status") == "failed":
        logger.debug("任务失败，触发反思")
        return True

    # 4. 其他情况不触发反思
    #    注意：移除了基于关键词的判断，因为现在由 AI 通过 checkpoint 字段控制
    return False

