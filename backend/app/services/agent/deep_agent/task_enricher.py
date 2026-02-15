"""任务增强器：为缺少工具信息的任务自动推断 tool 和 params

设计理念：
1. AI 优先：使用 AI 理解任务意图，智能推断工具
2. 规则兜底：AI 推断失败时，使用关键词规则兜底
3. 上下文感知：利用已完成任务的结果构建参数
"""

import re
import json
import logging
import asyncio
from typing import Dict, Any, Optional, List, Callable

from app.services.agent.model_selector import TaskType

logger = logging.getLogger(__name__)


# 工具描述（供 AI 参考）
# 🔧 2025-12-14: 与 Planning Prompt 保持一致，确保工具选择逻辑统一
AVAILABLE_TOOLS = """
可用工具列表：

1. get_chapter_by_order_tool
   - 用途：按章节序号获取章节内容
   - 参数：chapter_order (int) - 章节序号
   - 适用场景：获取第X章、读取某章内容、查看章节

2. get_context_tool
   - 用途：获取作品上下文信息（世界观、人物设定等）
   - 参数：无
   - 适用场景：获取背景、了解设定、查看世界观

3. analyze_text_tool
   - 用途：分析已有文本内容
   - 参数：text (str) - 要分析的文本, focus (str) - 分析焦点
   - 适用场景：分析人物、分析情节、概括内容、总结章节、评估质量
   - ⚠️ 只能分析现有内容，不能创作新内容（如大纲、设定等）
   - focus 可选值：all/character/plot/foreshadowing/system/worldview

4. smart_continue
   - 用途：续写章节内容
   - 参数：chapter_id (str) - 章节ID, content (str) - 上下文（可选）
   - 适用场景：续写、继续写、接着写

5. smart_rewrite
   - 用途：改写/润色章节内容
   - 参数：chapter_id (str), text_to_rewrite (str), user_requirement (str)
   - 适用场景：改写、润色、优化、扩写

注意：工具名称不带 _tool 后缀，如 smart_continue、analyze_text 等。
"""


class TaskEnricher:
    """任务增强器：根据任务描述推断工具和参数

    核心功能：
    1. 使用 AI 智能推断工具（优先）
    2. 关键词规则兜底（快速）
    3. 从已完成任务结果中提取参数
    """

    # 关键词兜底规则（当 AI 推断失败时使用）
    # 🔧 2025-12-14: 与工具描述保持一致
    # 注意：AI推断是主要方式，关键词只是兜底
    FALLBACK_RULES: List[Dict[str, Any]] = [
        {
            # 分析类：只包含"分析现有内容"的关键词
            "keywords": ["分析", "梳理", "总结", "概括", "提取", "归纳", "评估"],
            "tool": "analyze_text_tool",
        },
        {
            "keywords": ["上下文", "背景", "设定", "世界观"],
            "tool": "get_context_tool",
        },
        {
            "keywords": ["获取第", "读取第", "查看第", "第.*章"],
            "tool": "get_chapter_by_order_tool",
        },
        {
            # 续写类
            "keywords": ["续写", "继续写", "接着写", "往后写"],
            "tool": "smart_continue",
        },
        {
            # 改写类
            "keywords": ["改写", "润色", "优化", "扩写", "重写"],
            "tool": "smart_rewrite",
        },
    ]

    def __init__(self, ai_generate_func: Optional[Callable] = None):
        """初始化任务增强器

        Args:
            ai_generate_func: AI 生成函数，用于智能推断工具
                             签名: async def func(prompt: str, ...) -> Dict
        """
        self._ai_generate = ai_generate_func
        self._ai_enabled = ai_generate_func is not None

    def set_ai_generate_func(self, func: Callable):
        """设置 AI 生成函数（延迟注入）"""
        self._ai_generate = func
        self._ai_enabled = func is not None
        logger.info(f"[TaskEnricher] AI 推断功能已{'启用' if self._ai_enabled else '禁用'}")

    async def enrich(
        self,
        task: Dict[str, Any],
        context: Dict[str, Any] = None,
        completed_results: Dict[int, Dict] = None
    ) -> Dict[str, Any]:
        """增强任务，补全 tool 和 params

        Args:
            task: 原始任务 {"description": "...", "task_id": ...}
            context: 执行上下文（包含 context_str 等）
            completed_results: 已完成任务的结果

        Returns:
            增强后的任务，包含 tool 和 params
        """
        # 已有工具信息，直接返回
        if task.get("tool") and task["tool"] != "auto":
            return task

        description = task.get("description", "")
        task_id = task.get("task_id", 0)
        enriched = dict(task)

        # 准备上下文
        enrich_context = {
            "context": context or {},
            "completed_results": completed_results or {},
            "current_task_id": task_id,
        }

        # 策略1：使用 AI 智能推断（优先）
        if self._ai_enabled:
            try:
                ai_result = await self._ai_infer_tool(description, enrich_context)
                if ai_result and ai_result.get("tool"):
                    enriched["tool"] = ai_result["tool"]
                    enriched["params"] = self._build_params(
                        ai_result["tool"],
                        ai_result.get("params", {}),
                        description,
                        enrich_context
                    )
                    logger.info(
                        f"[TaskEnricher] AI 推断成功: "
                        f"'{description[:30]}...' → tool={enriched['tool']}"
                    )
                    return enriched
            except Exception as e:
                logger.warning(f"[TaskEnricher] AI 推断失败，降级到规则匹配: {e}")

        # 策略2：关键词规则兜底
        tool = self._fallback_match(description)
        if tool:
            enriched["tool"] = tool
            enriched["params"] = self._build_params(tool, {}, description, enrich_context)
            logger.info(
                f"[TaskEnricher] 规则匹配成功: "
                f"'{description[:30]}...' → tool={enriched['tool']}"
            )
            return enriched

        # 无法推断 - 使用 analyze_text 作为默认工具
        # 🔧 2025-12-14: 修复 tool:"auto" 无效问题
        logger.warning(f"[TaskEnricher] 无法推断工具: '{description[:50]}...'，使用默认工具 analyze_text")
        enriched["tool"] = "analyze_text"
        enriched["params"] = {
            "text": description,  # 将任务描述作为分析内容
            "focus": "根据任务描述进行分析或回答"
        }
        return enriched

    async def _ai_infer_tool(self, description: str, enrich_context: Dict) -> Optional[Dict]:
        """使用 AI 智能推断工具

        返回: {"tool": "工具名", "params": {...}} 或 None
        """
        prompt = f"""根据任务描述，判断应该使用哪个工具。

{AVAILABLE_TOOLS}

任务描述：{description}

请直接返回 JSON 格式（不要其他内容）：
{{"tool": "工具名", "reason": "简短理由"}}

注意：续写类任务请使用 smart_continue，改写/润色类任务请使用 smart_rewrite。
"""

        try:
            # ✅ 2025-12-08: 添加 task_type=SIMPLE_QA，使用快速模型
            response = await asyncio.wait_for(
                self._ai_generate(
                    prompt=prompt,
                    temperature=0.1,
                    max_tokens=200,
                    task_type=TaskType.SIMPLE_QA,  # 工具推断是简单分类任务
                ),
                timeout=30  # 再放宽至30秒，进一步降低偶发超时
            )

            text = response.get("text", "")
            if not text:
                return None

            # 提取 JSON
            text = text.strip()
            if "```json" in text:
                start = text.find("```json") + 7
                end = text.find("```", start)
                text = text[start:end].strip()
            elif "```" in text:
                start = text.find("```") + 3
                end = text.find("```", start)
                text = text[start:end].strip()

            if "{" in text:
                start = text.find("{")
                end = text.rfind("}") + 1
                json_str = text[start:end]
                result = json.loads(json_str)

                tool = result.get("tool")
                # 2026-01-09: 更新验证列表，使用 smart_continue/smart_rewrite
                if tool and tool in ["get_chapter_by_order_tool", "get_context_tool", "analyze_text_tool", "smart_continue", "smart_rewrite", "smart_insert"]:
                    return {"tool": tool, "params": {}}

            return None

        except asyncio.TimeoutError:
            logger.warning("[TaskEnricher] AI 推断超时")
            return None
        except Exception as e:
            logger.warning(f"[TaskEnricher] AI 推断异常: {e}")
            return None

    def _fallback_match(self, description: str) -> Optional[str]:
        """关键词规则兜底匹配"""
        for rule in self.FALLBACK_RULES:
            for kw in rule["keywords"]:
                if re.search(kw, description):
                    return rule["tool"]
        return None

    def _build_params(
        self,
        tool: str,
        ai_params: Dict,
        description: str,
        enrich_context: Dict
    ) -> Dict[str, Any]:
        """构建工具参数"""

        if tool == "get_chapter_by_order_tool":
            # 提取章节序号
            order = ai_params.get("chapter_order")
            if not order:
                order = self._extract_chapter_order(description)
            return {"chapter_order": order}

        elif tool == "get_context_tool":
            return {}

        elif tool == "analyze_text_tool":
            # 提取分析焦点
            focus = ai_params.get("focus") or self._infer_focus(description)

            # 从已完成任务结果中提取文本
            text = self._get_previous_results_text(enrich_context)
            if not text:
                # 降级：使用上下文
                context = enrich_context.get("context", {})
                text = context.get("context_str", "")

            return {"text": text, "focus": focus}

        elif tool == "smart_continue":
            # 2026-01-09: 续写工具参数构建
            return {"content": description}

        elif tool == "smart_rewrite":
            # 2026-01-09: 改写工具参数构建
            return {"user_requirement": description}

        return {}

    def _extract_chapter_order(self, description: str) -> int:
        """从描述中提取章节序号"""
        cn_nums = {
            '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
            '六': 6, '七': 7, '八': 8, '九': 9, '十': 10,
            '十一': 11, '十二': 12, '十三': 13, '十四': 14, '十五': 15,
        }

        match = re.search(r'第[一二三四五六七八九十百\d]+章', description)
        if match:
            chapter_str = match.group()
            num_match = re.search(r'[一二三四五六七八九十百]+|\d+', chapter_str)
            if num_match:
                num_str = num_match.group()
                if num_str.isdigit():
                    return int(num_str)
                return cn_nums.get(num_str, 1)
        return 1

    def _infer_focus(self, description: str) -> str:
        """推断分析焦点"""
        focus_keywords = {
            "character": ["人物", "角色", "性格", "形象"],
            "plot": ["情节", "剧情", "故事", "发展"],
            "foreshadowing": ["伏笔", "线索", "暗示", "铺垫"],
            "system": ["能力", "体系", "设定", "规则"],
            "worldview": ["世界观", "背景", "环境"],
            "planning": ["规划", "大纲", "计划", "设计"],
        }

        for focus, keywords in focus_keywords.items():
            for kw in keywords:
                if kw in description:
                    return focus

        return "all"

    def _get_previous_results_text(self, enrich_context: Dict) -> str:
        """从已完成任务结果中提取文本"""
        completed_results = enrich_context.get("completed_results", {})
        current_task_id = enrich_context.get("current_task_id", 0)

        if not completed_results:
            return ""

        # 按 task_id 排序，获取当前任务之前的结果
        sorted_ids = sorted(
            [tid for tid in completed_results.keys() if tid < current_task_id],
            reverse=True
        )

        if not sorted_ids:
            sorted_ids = sorted(completed_results.keys(), reverse=True)

        # 收集文本
        texts = []
        total_length = 0
        MAX_LENGTH = 8000

        for tid in sorted_ids:
            result = completed_results.get(tid, {})
            content = result.get("content", "")

            if content and isinstance(content, str):
                # 跳过错误信息
                if content.startswith("错误：") or content.startswith("任务"):
                    continue

                texts.append(content)
                total_length += len(content)

                if total_length >= MAX_LENGTH:
                    break

        if texts:
            combined = "\n\n".join(texts)
            logger.info(
                f"[TaskEnricher] 从 {len(texts)} 个任务结果中提取文本，"
                f"总长度: {len(combined)} 字符"
            )
            return combined

        return ""


# 全局实例
_enricher_instance: Optional[TaskEnricher] = None


def get_task_enricher() -> TaskEnricher:
    """获取全局 TaskEnricher 实例"""
    global _enricher_instance
    if _enricher_instance is None:
        _enricher_instance = TaskEnricher()
    return _enricher_instance


def init_task_enricher(ai_generate_func: Callable) -> TaskEnricher:
    """初始化并返回 TaskEnricher（带 AI 功能）"""
    global _enricher_instance
    _enricher_instance = TaskEnricher(ai_generate_func)
    return _enricher_instance
