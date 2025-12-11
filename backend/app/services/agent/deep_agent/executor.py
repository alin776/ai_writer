"""DeepAgent 执行器

包装现有的 Planning 执行流程，添加反思循环。
"""

import json
import logging
import asyncio
from datetime import datetime
from typing import Dict, Any, List, Optional, Callable

from .config import DeepAgentConfig
from .reflection import think_tool, should_reflect, ReflectionResult
from .task_enricher import get_task_enricher
from app.services.agent.model_selector import TaskType

logger = logging.getLogger(__name__)


class DeepAgentExecutor:
    """DeepAgent 执行器

    包装 WritingAgentGraph 的执行流程，添加反思能力。
    不修改原有代码，仅在执行过程中插入反思检查点。
    """

    def __init__(
        self,
        agent_graph,  # WritingAgentGraph 实例
        on_plan: Optional[Callable] = None,
        on_task_start: Optional[Callable] = None,
        on_task_progress: Optional[Callable] = None,  # 用于发送反思内容
        on_task_done: Optional[Callable] = None,
        on_content: Optional[Callable] = None,
    ):
        self.agent = agent_graph
        self.on_plan = on_plan
        self.on_task_start = on_task_start
        self.on_task_progress = on_task_progress  # 复用现有事件发送反思
        self.on_task_done = on_task_done
        self.on_content = on_content

        # 状态
        self.reflection_count = 0
        self.replan_count = 0
        self.reflections: List[Dict[str, Any]] = []
        self.final_fix_attempted = False  # 避免重复补救

    async def execute_with_reflection(
        self,
        plan: Dict[str, Any],
        context: Dict[str, Any],
        execute_task_func: Callable,
    ) -> Dict[str, Any]:
        """带反思的执行流程

        Args:
            plan: 初始计划（来自 Planning 阶段）
            context: 执行上下文
            execute_task_func: 任务执行函数（由 langgraph_agent 提供）

        Returns:
            执行结果
        """
        # P1-2: plan 参数验证
        if plan is None:
            logger.error("plan 参数为空")
            return {
                "results": {},
                "tasks": [],
                "reflections": [],
                "reflection_count": 0,
                "replan_count": 0,
                "error": "plan 参数为空",
            }

        tasks = list(plan.get("tasks", []))
        user_intent = plan.get("user_intent", "")  # ✅ 提取用户意图，用于反思和重规划
        results = {}
        completed_count = 0

        # 为关键任务补充验收标准（从描述/意图中推断数量等），便于末尾校验
        tasks = self._inject_acceptance(tasks, user_intent)

        logger.info(f"DeepAgent 开始执行，共 {len(tasks)} 个任务，反思功能已启用")

        # P2-5: 循环逻辑说明
        # 使用 while + 索引而非 for 循环，因为重规划时 tasks 列表可能被替换
        # 重规划只替换 tasks[i+1:] 部分，当前任务索引 i 不变
        # 因此 i += 1 后继续遍历新的任务列表是安全的
        # 获取任务增强器（用于补全缺少 tool 的任务）
        task_enricher = get_task_enricher()
        # ✅ 注入 AI 生成函数（复用 agent 的 _generate_text 方法）
        if hasattr(self.agent, '_generate_text'):
            task_enricher.set_ai_generate_func(self.agent._generate_text)

        has_checkpoint = any(t.get("checkpoint") for t in tasks)
        i = 0
        while i < len(tasks):
            task = tasks[i]
            task_id = task.get("task_id", i + 1)
            total_tasks = len(tasks)
            remaining_tasks_count = total_tasks - (i + 1)

            # ✅ 任务增强：为缺少 tool 的任务自动推断工具
            # 这对重规划生成的任务尤为重要
            # 传递已完成任务结果，供 TaskEnricher 提取文本参数
            if not task.get("tool") or task.get("tool") == "auto":
                task = await task_enricher.enrich(
                    task=task,
                    context=context,
                    completed_results=results  # ✅ 传递已完成任务结果
                )
                tasks[i] = task  # 更新任务列表

            # 发送任务开始事件
            if self.on_task_start:
                await self._safe_callback(self.on_task_start, task)

            # 执行任务（复用现有逻辑）
            try:
                result = await execute_task_func(
                    task=task,
                    context=context,
                    on_task_progress=self.on_task_progress,
                )
                results[task_id] = result
                completed_count += 1
                logger.debug(f"任务 {task_id} 执行完成: {result.get('status', 'unknown')}")
            except Exception as e:
                result = {"status": "failed", "error": str(e)}
                results[task_id] = result
                logger.error(f"任务 {task_id} 执行失败: {e}")

            # 发送任务完成事件
            if self.on_task_done:
                # ✅ 将执行时间从 result 复制到 task，确保前端能正确显示
                task_with_time = {**task, "elapsed_time": result.get("elapsed_time", 0)}
                await self._safe_callback(self.on_task_done, task_with_time, result)

            # ═══════════════════════════════════════
            # 反思检查点
            # ═══════════════════════════════════════
            if should_reflect(
                task,
                result,
                completed_count,
                self.reflection_count,
                total_tasks,
                remaining_tasks_count,
                has_checkpoint,
            ):
                logger.info(f"任务 {task_id} 触发反思检查点")

                reflection_result = await self._do_reflection(
                    task=task,
                    result=result,
                    remaining_tasks=tasks[i + 1:],
                    context={**context, "user_intent": user_intent},  # ✅ 注入 user_intent
                )

                # 如果需要重规划
                if reflection_result.needs_replan and self._can_replan():
                    logger.info(f"反思结果需要重规划 (第 {self.replan_count + 1} 次)")

                    new_tasks = await self._do_replan(
                        reflection=reflection_result.reflection,
                        completed_tasks=tasks[:i + 1],
                        remaining_tasks=tasks[i + 1:],
                        user_intent=user_intent,  # ✅ 传递用户意图
                    )

                    if new_tasks:
                        # 更新任务列表
                        old_remaining = tasks[i + 1:]
                        tasks = tasks[:i + 1] + new_tasks
                        self.replan_count += 1

                        # 发送更新的计划事件
                        if self.on_plan:
                            # 找出新增的任务 ID
                            old_ids = {t.get("task_id") for t in old_remaining}
                            new_task_ids = [
                                t.get("task_id") for t in new_tasks
                                if t.get("task_id") not in old_ids
                            ]

                            await self._safe_callback(self.on_plan, {
                                "tasks": [self._format_task(t, j) for j, t in enumerate(tasks, 1)],
                                "is_update": True,
                                "new_task_ids": new_task_ids,
                                "reason": reflection_result.reflection[:100],
                            })

                        logger.info(f"计划已更新，新任务数: {len(new_tasks)}")

            i += 1

        # 最终校验：发现缺口则追加一次补救任务
        tasks, results = await self._final_check_and_fix(
            tasks=tasks,
            results=results,
            context=context,
            user_intent=user_intent,
            execute_task_func=execute_task_func,
        )

        logger.info(
            f"DeepAgent 执行完成: "
            f"任务={len(tasks)}, 反思={self.reflection_count}, 重规划={self.replan_count}"
        )

        return {
            "results": results,
            "tasks": tasks,
            "reflections": self.reflections,
            "reflection_count": self.reflection_count,
            "replan_count": self.replan_count,
        }

    async def _do_reflection(
        self,
        task: Dict[str, Any],
        result: Dict[str, Any],
        remaining_tasks: List[Dict[str, Any]],
        context: Dict[str, Any],
    ) -> ReflectionResult:
        """执行反思"""
        # P1-1: ai_service 空值检查
        if not hasattr(self.agent, '_generate_text'):
            logger.warning("agent._generate_text 方法不存在，跳过反思")
            return ReflectionResult(reflection="agent 未初始化", needs_replan=False)

        try:
            reflection_result = await think_tool(
                task=task,
                result=result,
                remaining_tasks=remaining_tasks,
                context=context,
                agent_graph=self.agent,  # 传入 agent_graph，复用 _generate_text 抽象层
            )

            self.reflection_count += 1
            self.reflections.append({
                "task_id": task.get("task_id"),
                "reflection": reflection_result.reflection,
                "needs_replan": reflection_result.needs_replan,
                "timestamp": datetime.now().isoformat(),
            })

            # MVP方案：复用 task_progress 事件发送反思内容
            # 前端 progress_status 会自动显示，无需任何改动
            if self.on_task_progress:
                await self._safe_callback(
                    self.on_task_progress,
                    task,
                    f"💭 反思: {reflection_result.reflection}"
                )

            logger.debug(f"反思完成: needs_replan={reflection_result.needs_replan}")
            return reflection_result

        except Exception as e:
            logger.error(f"反思失败: {e}")
            return ReflectionResult(reflection=str(e), needs_replan=False)

    def _get_max_task_id(self, tasks: List[Dict[str, Any]]) -> int:
        """获取任务列表中最大的 task_id（仅限数值，可防御混合类型）"""
        ids: List[int] = []
        for t in tasks:
            if not isinstance(t, dict):
                continue
            tid = t.get("task_id")
            try:
                ids.append(int(tid))
            except (TypeError, ValueError):
                continue
        return max(ids) if ids else 0

    def _infer_acceptance_by_regex(self, task: Dict[str, Any], user_intent: str) -> Optional[Dict[str, Any]]:
        """【第二层】正则快速提取验收标准（成本=0）"""
        text = f"{task.get('description', '')} {user_intent}"[:200]

        import re
        match = re.search(r"(\d{1,3})\s*(个|条|点|段|篇|章节|章|转折点|要点|场景|角色|人物|种|类|组|步|项|处|部分|方面|建议|方案|问题|观点)", text)
        if match:
            count = int(match.group(1))
            return {
                "expected_count": count,
                "requirement": match.group(0),
            }

        return None

    async def _infer_acceptance_by_llm(self, task: Dict[str, Any], user_intent: str) -> Optional[Dict[str, Any]]:
        """【第三层】LLM 提取验收标准（兜底）"""
        if not hasattr(self.agent, "_generate_text"):
            return None

        task_desc = task.get("description", "")
        prompt = f"""从以下内容中提取验收标准。

任务描述：{task_desc}
用户意图：{user_intent}

如果有明确的数量要求（如"5个"、"3条"、"多个"等），返回 JSON：
{{"expected_count": 数字, "requirement": "原文中的数量描述"}}

如果没有明确数量要求，返回：null

只输出 JSON 或 null，不要其他内容。
"""

        try:
            response = await asyncio.wait_for(
                self.agent._generate_text(
                    prompt=prompt,
                    temperature=0.1,
                    max_tokens=100,
                    task_type=TaskType.SIMPLE_QA,
                ),
                timeout=15,
            )

            text = (response or {}).get("text", "").strip()
            if not text or text.lower() == "null":
                return None

            # 解析 JSON
            try:
                data = json.loads(text)
                if isinstance(data, dict) and data.get("expected_count"):
                    logger.debug(f"[LLM提取] 验收标准: {data}")
                    return data
            except json.JSONDecodeError:
                # 尝试提取 JSON
                start = text.find("{")
                end = text.rfind("}") + 1
                if start != -1 and end > start:
                    data = json.loads(text[start:end])
                    if isinstance(data, dict) and data.get("expected_count"):
                        return data

            return None
        except Exception as e:
            logger.debug(f"[LLM提取] 失败: {e}")
            return None

    async def _get_acceptance(self, task: Dict[str, Any], user_intent: str) -> Optional[Dict[str, Any]]:
        """获取验收标准（三层策略）

        第一层：AI 在 Planning 时主动生成的 task.acceptance
        第二层：正则快速提取（成本=0）
        第三层：LLM 提取（兜底）
        """
        # 第一层：Planning 时生成的
        if task.get("acceptance"):
            return task["acceptance"]

        # 第二层：正则快速提取
        acceptance = self._infer_acceptance_by_regex(task, user_intent)
        if acceptance:
            return acceptance

        # 第三层：LLM 兜底
        return await self._infer_acceptance_by_llm(task, user_intent)

    def _inject_acceptance(self, tasks: List[Dict[str, Any]], user_intent: str) -> List[Dict[str, Any]]:
        """为没有验收标准的任务补充 acceptance 字段（仅正则快速提取）"""
        enriched = []
        for t in tasks:
            task = dict(t)
            if not task.get("acceptance"):
                # 只用正则快速提取，LLM 提取在 _final_check_and_fix 时按需调用
                acceptance = self._infer_acceptance_by_regex(task, user_intent)
                if acceptance:
                    task["acceptance"] = acceptance
            enriched.append(task)
        return enriched

    def _count_items(self, output: str) -> int:
        """简单计数：按行项目符号/编号推断条目数"""
        lines = [ln.strip() for ln in output.splitlines() if ln.strip()]
        bullets = [ln for ln in lines if ln[:2] in {"- ", "* "} or ln[:3].isdigit() or ln.startswith(("1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.", "0."))]
        if bullets:
            return len(bullets)
        # 回退：尝试分号/换行切分后看是否为短句列表
        if len(lines) > 1:
            return len(lines)
        return 1 if output.strip() else 0

    async def _final_check_and_fix(
        self,
        tasks: List[Dict[str, Any]],
        results: Dict[Any, Dict[str, Any]],
        context: Dict[str, Any],
        user_intent: str,
        execute_task_func: Callable,
    ) -> (List[Dict[str, Any]], Dict[Any, Dict[str, Any]]):
        """末尾验收：数量/必需要点不达标则追加一次补救任务"""

        if self.final_fix_attempted:
            return tasks, results
        self.final_fix_attempted = True

        if not tasks:
            return tasks, results

        # 依次检查所有带 acceptance 的任务，找到第一个不满足的进行补救
        failed_task = None
        failed_result = None
        failed_acceptance = None

        for t in tasks:
            # 使用三层策略获取验收标准
            acceptance = await self._get_acceptance(t, user_intent)
            if not acceptance:
                continue
            tid = t.get("task_id")
            res = results.get(tid, {}) if tid in results else results.get(str(tid), {})
            output = res.get("output") or res.get("content") or ""

            # 先做硬计数检查，再用 LLM 兜底
            need_fix = False
            if not output:
                need_fix = True
            else:
                expected = acceptance.get("expected_count")
                if expected:
                    item_count = self._count_items(output)
                    if item_count >= expected:
                        need_fix = False
                    else:
                        need_fix = not await self._evaluate_final_output(
                            task_desc=t.get("description", ""),
                            user_intent=user_intent,
                            acceptance=acceptance,
                            output=output,
                        )
                else:
                    need_fix = not await self._evaluate_final_output(
                        task_desc=t.get("description", ""),
                        user_intent=user_intent,
                        acceptance=acceptance,
                        output=output,
                    )

            if need_fix:
                failed_task = t
                failed_result = res
                failed_acceptance = acceptance
                break

        if not failed_task:
            return tasks, results

        logger.info("[FinalCheck] 末尾校验未通过，追加补救任务")

        # 可选：触发一次反思，给出补救提示
        reflection_note = ""
        if self.reflection_count < DeepAgentConfig.MAX_REFLECTIONS:
            try:
                reflection = await self._do_reflection(
                    task=failed_task,
                    result=failed_result,
                    remaining_tasks=[],
                    context={**context, "user_intent": user_intent},
                )
                reflection_note = reflection.reflection
            except Exception:
                reflection_note = ""

        new_task_id = self._get_max_task_id(tasks) + 1
        requirement_text = failed_acceptance.get("requirement") or user_intent or "完善输出"
        remedy_task = {
            "task_id": new_task_id,
            "description": f"补充/修正前一任务结果，确保满足：{requirement_text}",
            "tool": failed_task.get("tool", "auto"),
            "params": failed_task.get("params", {}),
            "checkpoint": True,
            "acceptance": failed_acceptance,
        }

        tasks.append(remedy_task)

        # 执行补救任务（不再进入反思循环，避免无限迭代）
        if self.on_task_start:
            await self._safe_callback(self.on_task_start, remedy_task)

        try:
            remedy_result = await execute_task_func(
                task=remedy_task,
                context=context,
                on_task_progress=self.on_task_progress,
            )
        except Exception as e:
            remedy_result = {"status": "failed", "error": str(e)}
            logger.error(f"补救任务执行失败: {e}")

        results[new_task_id] = remedy_result

        if self.on_task_done:
            task_with_time = {**remedy_task, "elapsed_time": remedy_result.get("elapsed_time", 0)}
            await self._safe_callback(self.on_task_done, task_with_time, remedy_result)

        # 如有反思内容，反馈进度
        if reflection_note and self.on_task_progress:
            await self._safe_callback(self.on_task_progress, remedy_task, f"[FinalCheck] 末尾校验提示: {reflection_note}")

        return tasks, results

    async def _evaluate_final_output(
        self,
        task_desc: str,
        user_intent: str,
        acceptance: Dict[str, Any],
        output: str,
    ) -> bool:
        """调用轻量模型做末尾验收，返回是否通过"""

        if not hasattr(self.agent, "_generate_text"):
            return True  # 无法调用 AI 时不阻断流程

        expected = acceptance.get("expected_count")
        requirement = acceptance.get("requirement", "")

        snippet = output[:2000]
        prompt = f"""
你是写作验收官，判断生成结果是否满足用户明确的数量/要点要求。只输出JSON，不要多余文字。

## 验收基线
- 用户意图: {user_intent or '未提供'}
- 任务描述: {task_desc}
- 验收要求: 期望数量={expected or '未知'}，关键词={requirement or '未知'}

## 待验收内容（截断2000字）
{snippet}

请输出：{{"pass": true/false, "missing": ["缺什么"], "summary": "一句话概括问题"}}
"""

        try:
            response = await asyncio.wait_for(
                self.agent._generate_text(
                    prompt=prompt,
                    temperature=0.1,
                    max_tokens=200,
                    task_type=TaskType.SIMPLE_QA,
                ),
                timeout=20,
            )

            text = (response or {}).get("text", "").strip()
            if not text:
                return True

            try:
                data = json.loads(text)
            except json.JSONDecodeError:
                # 尝试提取第一个 JSON 对象
                start = text.find("{")
                end = text.rfind("}") + 1 if "}" in text else -1
                if start != -1 and end > start:
                    data = json.loads(text[start:end])
                else:
                    return True

            val = data.get("pass", False)
            if isinstance(val, bool):
                return val
            if isinstance(val, str):
                return val.strip().lower() in {"true", "yes", "pass", "ok"}
            return False
        except Exception as e:
            logger.warning(f"末尾验收调用失败，忽略校验: {e}")
            return True

    def _can_replan(self) -> bool:
        """是否还能重规划"""
        return self.replan_count < DeepAgentConfig.MAX_REPLANS

    async def _do_replan(
        self,
        reflection: str,
        completed_tasks: List[Dict[str, Any]],
        remaining_tasks: List[Dict[str, Any]],
        user_intent: str = "",
    ) -> Optional[List[Dict[str, Any]]]:
        """重新规划

        Args:
            reflection: 反思内容
            completed_tasks: 已完成的任务
            remaining_tasks: 原剩余任务
            user_intent: 用户原始意图

        Returns:
            新的任务列表（用于替换 remaining_tasks），失败时返回 None

        🔧 2025-12-09: 重构 JSON 解析逻辑，消除歧义和边界问题
        🔧 2025-12-11: 新增 user_intent 参数，确保重规划不偏离用户意图
        """
        # P1-1: _generate_text 方法检查（与 _do_reflection 保持一致）
        if not hasattr(self.agent, '_generate_text'):
            logger.warning("agent._generate_text 方法不存在，跳过重规划")
            return None

        try:
            # 构建重规划 prompt
            completed_str = "\n".join([
                f"  - [已完成] {t.get('description', '未知')}"
                for t in completed_tasks[-3:]  # 只取最近3个
            ])

            remaining_str = "\n".join([
                f"  - {t.get('description', '未知')}"
                for t in remaining_tasks
            ]) if remaining_tasks else "  (无)"

            prompt = f"""基于反思结果，请调整后续任务计划。

## 用户原始意图
{user_intent or "未指定"}

## 反思内容
{reflection}

## 已完成任务
{completed_str}

## 原剩余任务
{remaining_str}

## 要求
1. 新任务必须围绕用户原始意图，不要偏离
2. 可以在开头插入新任务
3. 可以调整现有任务的描述
4. 可以删除不必要的任务
5. 保持任务描述简洁

## 输出格式（必须是合法JSON，不要添加其他内容）
{{"tasks": [{{"description": "任务描述1"}}, {{"description": "任务描述2"}}]}}
"""

            # 复用 _generate_text 抽象层
            # ✅ 2025-12-08: 添加 task_type=SIMPLE_QA，使用快速模型避免超时
            logger.info("[DeepAgent重规划] 开始调用 AI")
            response = await asyncio.wait_for(
                self.agent._generate_text(
                    prompt=prompt,
                    # 降低采样温度与生成上限，缩短重规划延迟并提升确定性
                    temperature=0.2,
                    max_tokens=800,
                    task_type=TaskType.SIMPLE_QA,  # ✅ 重规划是简单任务规划
                ),
                timeout=DeepAgentConfig.REPLAN_TIMEOUT
            )

            # 检查是否有错误
            if response.get("error"):
                logger.warning(f"重规划 AI 调用失败: {response.get('error')}")
                return None

            content = response.get("text", "")
            if not content:
                logger.warning("重规划响应为空")
                return None

            # 🔧 2025-12-09: 健壮的 JSON 解析
            new_tasks = self._parse_replan_response(content)
            if not new_tasks:
                return None

            # 🔧 2025-12-09: 修复 task_id 冲突 - 收集所有已用的 ID
            used_ids = {t.get("task_id") for t in completed_tasks if t.get("task_id")}
            used_ids.update(t.get("task_id") for t in remaining_tasks if t.get("task_id"))
            max_id = max((t.get("task_id", 0) for t in completed_tasks), default=0)

            for idx, task in enumerate(new_tasks):
                # 如果没有 task_id，或者 task_id 已被使用，重新分配
                if "task_id" not in task or task["task_id"] in used_ids:
                    new_id = max_id + idx + 1
                    # 确保新 ID 也不冲突
                    while new_id in used_ids:
                        new_id += 1
                    task["task_id"] = new_id
                    used_ids.add(new_id)
                task.setdefault("status", "pending")

            logger.info(f"[DeepAgent重规划] 成功生成 {len(new_tasks)} 个新任务")
            return new_tasks

        except asyncio.TimeoutError:
            logger.warning("重规划超时，保持原计划")
            return None
        except Exception as e:
            logger.error(f"重规划失败: {e}")
            return None

    def _parse_replan_response(self, content: str) -> Optional[List[Dict[str, Any]]]:
        """解析重规划响应（JSON格式）

        🔧 2025-12-09: 新增方法，健壮的 JSON 解析逻辑
        """
        content = (content or "").strip()

        # 方法1：直接解析
        try:
            data = json.loads(content)
            return self._validate_replan_data(data)
        except json.JSONDecodeError:
            pass

        # 方法2：提取 ```json ... ``` 代码块
        if "```" in content:
            try:
                # 查找代码块
                if "```json" in content:
                    start = content.find("```json") + 7
                else:
                    start = content.find("```") + 3
                end = content.find("```", start)
                if end > start:
                    json_str = content[start:end].strip()
                    data = json.loads(json_str)
                    return self._validate_replan_data(data)
            except json.JSONDecodeError:
                pass

        # 方法3：提取第一个完整的 JSON 对象
        try:
            start = content.find("{")
            if start != -1:
                # 使用括号匹配找到完整的 JSON 对象
                depth = 0
                end = start
                for i, char in enumerate(content[start:], start):
                    if char == "{":
                        depth += 1
                    elif char == "}":
                        depth -= 1
                        if depth == 0:
                            end = i + 1
                            break
                if end > start:
                    json_str = content[start:end]
                    data = json.loads(json_str)
                    return self._validate_replan_data(data)
        except json.JSONDecodeError:
            pass

        logger.warning(f"[DeepAgent重规划] JSON解析失败: {content[:200]}")
        return None

    def _validate_replan_data(self, data: Any) -> Optional[List[Dict[str, Any]]]:
        """验证重规划数据结构

        🔧 2025-12-09: 新增方法，验证解析后的数据
        """
        if not isinstance(data, dict):
            logger.warning("[DeepAgent重规划] 数据不是字典")
            return None

        tasks = data.get("tasks")
        if not isinstance(tasks, list):
            logger.warning("[DeepAgent重规划] tasks 不是数组")
            return None

        if len(tasks) == 0:
            logger.warning("[DeepAgent重规划] tasks 为空数组")
            return None

        # 验证每个任务
        valid_tasks = []
        for i, task in enumerate(tasks):
            if not isinstance(task, dict):
                logger.warning(f"[DeepAgent重规划] 任务 {i} 不是字典，跳过")
                continue
            if not task.get("description"):
                logger.warning(f"[DeepAgent重规划] 任务 {i} 缺少 description，跳过")
                continue
            valid_tasks.append(task)

        if not valid_tasks:
            logger.warning("[DeepAgent重规划] 没有有效任务")
            return None

        return valid_tasks

    def _format_task(self, task: Dict[str, Any], task_id: int) -> Dict[str, Any]:
        """格式化任务"""
        if isinstance(task, str):
            return {"task_id": task_id, "description": task, "status": "pending"}
        task = dict(task)  # 复制一份
        task["task_id"] = task.get("task_id", task_id)
        task.setdefault("status", "pending")
        return task

    async def _safe_callback(self, callback: Callable, *args):
        """安全调用回调（支持同步和异步函数）"""
        try:
            if asyncio.iscoroutinefunction(callback):
                # 回调本身是 async def 定义的异步函数
                await callback(*args)
            else:
                # 同步函数，但可能返回协程
                result = callback(*args)
                if asyncio.iscoroutine(result):
                    await result
        except Exception as e:
            logger.error(f"回调执行失败: {e}")
