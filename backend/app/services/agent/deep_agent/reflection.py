"""反思工具和逻辑

基于 Deep Agents 的 think_tool 设计，实现纯上下文工程的反思能力。
"""

import json
import logging
import asyncio
from dataclasses import dataclass
from typing import Dict, Any, List, Optional

from .config import DeepAgentConfig
from app.services.agent.model_selector import TaskType

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
    acceptance: Optional[Dict[str, Any]] = None,
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

    prompt = _build_reflection_prompt(task, result, remaining_tasks, context, acceptance)

    try:
        # 复用 _generate_text 抽象层
        # ✅ 2025-12-08: 添加 task_type=SIMPLE_QA，使用快速模型避免超时
        logger.info(f"[DeepAgent反思] 开始调用 AI，task_id={task.get('task_id')}")
        response = await asyncio.wait_for(
            agent_graph._generate_text(
                prompt=prompt,
                temperature=0.3,
                max_tokens=500,
                task_type=TaskType.SIMPLE_QA,  # ✅ 反思是简单决策任务
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
    context: Dict[str, Any],
    acceptance: Optional[Dict[str, Any]] = None,
) -> str:
    """构建反思 Prompt"""
    task_desc = task.get("description", "未知任务")
    task_status = result.get("status", "unknown")
    user_intent = (
        context.get("user_intent")
        or context.get("intent")
        or context.get("goal")
        or ""
    )

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
{"- 验收标准: " + json.dumps(acceptance, ensure_ascii=False) if acceptance else ""}

## 剩余任务
{remaining_str}

## 用户意图
- {user_intent or "未指定"}

## ⚠️ 关键判断原则：足够好就行，不必追求完美

**核心思想：只有在明显无法完成用户需求时才返回 needs_replan=true**

### 什么时候 needs_replan=true（仅限以下严重问题）：
1. **明显的数量不足**：用户明确要求"5个"但只有1-2个
2. **关键信息缺失**：例如需要章节内容但没获取到
3. **任务执行失败**：状态为 failed 且无法通过剩余任务补救
4. **方向完全错误**：理解偏差导致无法回答用户问题

### 什么时候 needs_replan=false（大多数情况）：
- ✅ 已经有部分结果，剩余任务能补足（例如：要3个生成了2个，还有续写任务）
- ✅ 虽不完美但基本满足需求（例如：分析不够深入，但关键点都有）
- ✅ 只是风格/细节问题（后续任务或最终整合可以优化）
- ✅ 输入任务完成，输出任务尚未执行（例如：检索完成，分析任务还在后面）
- ✅ 剩余任务足够完成目标（例如：读取完成，后面有分析任务）

### 常见误判提醒：
- ❌ 错误："还没回答用户问题" → 正确：检查后续任务是否包含回答步骤
- ❌ 错误："分析不够深入" → 正确：有基本分析即可，不必完美
- ❌ 错误："少了一些细节" → 正确：足够好就行，后续可以优化

## 输出格式（必须是合法JSON，不要添加其他内容）
{{"needs_replan": false, "reflection": "简短反思内容（<100字）"}}

示例（needs_replan=false的典型情况）：
{{"needs_replan": false, "reflection": "检索成功，后续分析任务可完成目标。"}}
{{"needs_replan": false, "reflection": "已生成2个角色，剩余续写任务能补足到3个。"}}
{{"needs_replan": false, "reflection": "分析基本到位，后续整合即可完成。"}}

示例（needs_replan=true的严重情况）：
{{"needs_replan": true, "reflection": "用户要5个章节分析，但只规划了1个，需要补充任务。"}}
{{"needs_replan": true, "reflection": "章节读取失败，无法进行后续分析，需要重新获取。"}}

"""


def _parse_reflection_response(response: str) -> ReflectionResult:
    """解析反思响应（JSON格式）

    解析 JSON 格式输出：
    {"needs_replan": false, "reflection": "反思内容"}

    🔧 2025-12-09: 重构为 JSON 解析，消除文本匹配歧义
    """
    raw_text = (response or "").strip()

    # 尝试直接解析 JSON
    try:
        data = json.loads(raw_text)
        needs_replan = bool(data.get("needs_replan", False))
        reflection = str(data.get("reflection", ""))
        logger.info(f"[Reflection] JSON解析成功: needs_replan={needs_replan}")
        return ReflectionResult(reflection=reflection, needs_replan=needs_replan)
    except json.JSONDecodeError:
        pass

    # 尝试从文本中提取第一个完整的 JSON 对象
    # 🔧 2025-12-09: 使用括号匹配而非 rfind，避免多个 JSON 对象时提取错误
    try:
        start = raw_text.find("{")
        if start != -1:
            depth = 0
            end = start
            for i, char in enumerate(raw_text[start:], start):
                if char == "{":
                    depth += 1
                elif char == "}":
                    depth -= 1
                    if depth == 0:
                        end = i + 1
                        break
            if end > start:
                json_str = raw_text[start:end]
                data = json.loads(json_str)
                needs_replan = bool(data.get("needs_replan", False))
                reflection = str(data.get("reflection", ""))
                logger.info(f"[Reflection] JSON提取成功: needs_replan={needs_replan}")
                return ReflectionResult(reflection=reflection, needs_replan=needs_replan)
    except json.JSONDecodeError:
        pass

    # 兜底：无法解析时，默认不重规划
    logger.warning(f"[Reflection] JSON解析失败，使用默认值: {raw_text[:100]}")
    return ReflectionResult(reflection=raw_text, needs_replan=False)


def should_reflect(
    task: Dict[str, Any],
    result: Dict[str, Any],
    completed_count: int,
    reflection_count: int,
    total_tasks: int,
    remaining_tasks_count: int,
    has_checkpoint: bool,
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
        total_tasks: 任务总数
        remaining_tasks_count: 剩余任务数
        has_checkpoint: 计划中是否有任务标记了 checkpoint

    Returns:
        bool: 是否需要反思

    🔧 2025-12-08: 重构 - 基于 checkpoint 字段判断，让 AI 决定何时反思
    🔧 2025-12-11: 新增 total_tasks, remaining_tasks_count, has_checkpoint 参数
    """
    config = DeepAgentConfig

    # 1. 达到上限检查
    if reflection_count >= config.MAX_REFLECTIONS:
        logger.debug(f"已达到最大反思次数 ({config.MAX_REFLECTIONS})，跳过反思")
        return False

    # 2. 核心：Planner 标记 checkpoint 的任务才反思
    if task.get("checkpoint") is True:
        task_id = task.get("task_id", "?")
        logger.info(f"[Checkpoint] 任务 {task_id} 标记了 checkpoint，触发反思")
        return True

    # 2.1 规划完全未标记 checkpoint 时的兜底（仅首个任务一次）
    if (
        config.REFLECT_ON_FIRST_TASK_IF_NO_CHECKPOINT
        and not has_checkpoint
        and completed_count == 1
        and reflection_count == 0
    ):
        task_id = task.get("task_id", "?")
        logger.info(
            f"[Checkpoint] 首个任务 {task_id} 未标记 checkpoint，触发一次兜底反思以校验规划"
        )
        return True

    # 3. 任务失败时兜底反思
    if config.REFLECT_ON_FAILURE and result.get("status") == "failed":
        logger.debug("任务失败，触发反思")
        return True

    # 4. 其他情况不触发反思
    #    注意：移除了基于关键词的判断，因为现在由 AI 通过 checkpoint 字段控制
    return False
