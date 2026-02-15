# 04 - 反思机制增强

## 文件位置

`backend/app/services/agent/deep_agent/reflection.py`（改造）

## 现有代码分析

当前 `think_tool` 输出：
```python
@dataclass
class ReflectionResult:
    reflection: str      # 反思内容
    needs_replan: bool   # 是否需要重规划
```

## 增强后的输出

```python
@dataclass
class IterativeReflectionResult:
    """迭代反思结果 - 增强版"""

    # 展示给用户
    summary: str          # 任务结果摘要（1-2句话）
    next_step: str        # 下一步说明

    # 内部决策
    action: str           # continue / add_task / skip_next / done
    new_task: Optional[Dict[str, Any]] = None  # action=add_task 时的新任务

    # 调试信息
    reasoning: str = ""   # 决策理由（日志用）
```

## 新增函数

```python
async def iterative_reflect(
    task: Dict[str, Any],
    result: str,
    remaining_tasks: List[Dict[str, Any]],
    user_request: str,
    completed_results: List[Dict[str, Any]],
    agent_graph: Any
) -> IterativeReflectionResult:
    """迭代反思 - 每个任务执行后调用

    Args:
        task: 刚执行完的任务
        result: 任务执行结果
        remaining_tasks: 剩余待执行任务
        user_request: 用户原始请求
        completed_results: 已完成的所有任务结果
        agent_graph: WritingAgentGraph 实例（复用 _generate_text）

    Returns:
        IterativeReflectionResult: 反思结果
    """
    prompt = _build_iterative_reflection_prompt(
        task=task,
        result=result,
        remaining_tasks=remaining_tasks,
        user_request=user_request,
        completed_results=completed_results
    )

    try:
        response = await asyncio.wait_for(
            agent_graph._generate_text(
                prompt=prompt,
                temperature=0.3,
                max_tokens=500,
                task_type=TaskType.SIMPLE_QA
            ),
            timeout=10.0
        )

        content = response.get("text", "")
        return _parse_iterative_reflection(content)

    except asyncio.TimeoutError:
        return IterativeReflectionResult(
            summary="反思超时",
            next_step="继续执行下一个任务",
            action="continue"
        )
    except Exception as e:
        logger.error(f"[IterativeReflect] 失败: {e}")
        return IterativeReflectionResult(
            summary="反思失败",
            next_step="继续执行",
            action="continue"
        )
```

## 反思 Prompt

```python
def _build_iterative_reflection_prompt(
    task: Dict[str, Any],
    result: str,
    remaining_tasks: List[Dict[str, Any]],
    user_request: str,
    completed_results: List[Dict[str, Any]]
) -> str:
    """构建迭代反思 Prompt"""

    # 结果摘要（限制长度）
    result_preview = result[:500] + "..." if len(result) > 500 else result

    # 剩余任务列表
    remaining_str = "\n".join([
        f"  - {t.get('title', '未知')}"
        for t in remaining_tasks[:5]
    ]) if remaining_tasks else "  (无剩余任务)"

    # 已完成任务摘要
    completed_str = "\n".join([
        f"  - {r.get('tool', '未知')}: 完成"
        for r in completed_results[-3:]  # 只显示最近3个
    ]) if completed_results else "  (无)"

    return f"""你是 AI Agent，刚完成了一个任务。请反思并决定下一步。

## 用户请求
{user_request}

## 刚完成的任务
- 工具：{task.get('tool', '未知')}
- 描述：{task.get('title', '未知')}
- 结果预览：
{result_preview}

## 已完成任务
{completed_str}

## 剩余任务
{remaining_str}

## 请回答（JSON格式）

1. summary: 用 1-2 句话总结这个任务的结果（给用户看）
2. next_step: 说明接下来要做什么（给用户看）
3. action: 决定下一步行动
   - "continue": 继续执行下一个任务
   - "add_task": 需要补充任务（必须提供 new_task）
   - "skip_next": 跳过下一个任务（发现不需要了）
   - "done": 已经可以完成用户请求，不需要执行剩余任务

4. new_task: 如果 action="add_task"，提供新任务配置

## 判断原则

- 结果足够 → continue
- 缺少关键信息 → add_task
- 下一个任务不需要了 → skip_next
- 已经能回答用户 → done

## 输出格式（必须是合法JSON）

{{
  "summary": "获取了第三章内容，共2000字，讲述主角进入森林...",
  "next_step": "接下来我会分析章节结构，然后开始续写",
  "action": "continue",
  "new_task": null
}}

或者（需要补充任务时）：

{{
  "summary": "获取了章节内容，但缺少世界观信息",
  "next_step": "我需要先获取世界观，了解魔法体系",
  "action": "add_task",
  "new_task": {{
    "title": "获取世界观",
    "tool": "get_worldview_summary",
    "params": {{}}
  }}
}}
"""
```

## 解析函数

```python
def _parse_iterative_reflection(response: str) -> IterativeReflectionResult:
    """解析迭代反思响应"""
    try:
        # 尝试直接解析
        data = json.loads(response.strip())
    except json.JSONDecodeError:
        # 尝试提取 JSON
        match = re.search(r'\{[\s\S]*\}', response)
        if match:
            try:
                data = json.loads(match.group())
            except:
                data = {}
        else:
            data = {}

    return IterativeReflectionResult(
        summary=data.get("summary", "任务完成"),
        next_step=data.get("next_step", "继续执行"),
        action=data.get("action", "continue"),
        new_task=data.get("new_task"),
        reasoning=data.get("reasoning", "")
    )
```

## 与现有 think_tool 的关系

| 函数 | 用途 | 触发时机 |
|------|------|----------|
| `think_tool` | checkpoint 反思 | 仅 checkpoint=true 的任务 |
| `iterative_reflect` | 迭代反思 | 每个任务执行后 |

**建议**：保留 `think_tool`，新增 `iterative_reflect`，两者可以共存。
