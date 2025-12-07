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
    ai_service: Optional[Any] = None,  # HTTPAIService 实例
) -> ReflectionResult:
    """反思工具

    纯上下文工程工具，迫使 Agent 在关键节点评估进度。

    Args:
        task: 刚执行完的任务
        result: 任务执行结果
        remaining_tasks: 剩余待执行的任务
        context: 上下文信息
        ai_service: AI 服务实例

    Returns:
        ReflectionResult: 反思结果
    """
    # P1-1: 空值检查
    if ai_service is None:
        logger.warning("ai_service 为空，跳过反思")
        return ReflectionResult(reflection="ai_service 未初始化，跳过反思", needs_replan=False)

    prompt = _build_reflection_prompt(task, result, remaining_tasks)

    try:
        response = await asyncio.wait_for(
            ai_service.chat(
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
            ),
            timeout=DeepAgentConfig.REFLECTION_TIMEOUT
        )

        # 提取响应内容
        if isinstance(response, dict):
            content = response.get("content", str(response))
        else:
            content = str(response)

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

## 输出格式（JSON）
{{"reflection": "简短反思（<100字）", "needs_replan": true/false}}
"""


def _parse_reflection_response(response: str) -> ReflectionResult:
    """解析反思响应"""
    try:
        # 尝试提取 JSON
        response = response.strip()

        # 处理可能的 markdown 代码块
        if "```json" in response:
            start = response.find("```json") + 7
            end = response.find("```", start)
            response = response[start:end].strip()
        elif "```" in response:
            start = response.find("```") + 3
            end = response.find("```", start)
            response = response[start:end].strip()

        # 尝试找到 JSON 对象
        if "{" in response:
            start = response.find("{")
            end = response.rfind("}") + 1
            json_str = response[start:end]
            data = json.loads(json_str)

            return ReflectionResult(
                reflection=data.get("reflection", response),
                needs_replan=data.get("needs_replan", False),
                suggested_tasks=data.get("suggested_tasks"),
            )
    except json.JSONDecodeError as e:
        # P2-4: 记录 JSON 解析异常
        logger.debug(f"反思响应 JSON 解析失败: {e}, 原始响应: {response[:200]}...")

    # 降级处理：基于关键词判断
    needs_replan = any(kw in response for kw in DeepAgentConfig.REPLAN_KEYWORDS)
    return ReflectionResult(reflection=response, needs_replan=needs_replan)


def should_reflect(
    task: Dict[str, Any],
    result: Dict[str, Any],
    completed_count: int,
    reflection_count: int,
) -> bool:
    """判断是否需要触发反思

    Args:
        task: 当前任务
        result: 任务结果
        completed_count: 已完成任务数
        reflection_count: 已反思次数

    Returns:
        bool: 是否需要反思
    """
    config = DeepAgentConfig

    # 达到上限
    if reflection_count >= config.MAX_REFLECTIONS:
        logger.debug(f"已达到最大反思次数 ({config.MAX_REFLECTIONS})，跳过反思")
        return False

    # 任务失败
    if config.REFLECT_ON_FAILURE and result.get("status") == "failed":
        logger.debug("任务失败，触发反思")
        return True

    # 低质量
    if config.REFLECT_ON_LOW_QUALITY:
        quality = result.get("quality_score", 1.0)
        if quality < config.QUALITY_THRESHOLD:
            logger.debug(f"任务质量较低 ({quality} < {config.QUALITY_THRESHOLD})，触发反思")
            return True

    # 分析类任务
    if config.REFLECT_ON_ANALYSIS:
        desc = task.get("description", "").lower()
        task_type = task.get("type", "")
        if "分析" in desc or task_type == "analysis":
            logger.debug("分析类任务完成，触发反思")
            return True

    # 定期反思
    if completed_count > 0 and completed_count % config.REFLECT_EVERY_N_TASKS == 0:
        logger.debug(f"定期反思检查点 (每 {config.REFLECT_EVERY_N_TASKS} 个任务)")
        return True

    return False
