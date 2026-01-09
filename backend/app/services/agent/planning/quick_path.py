# -*- coding: utf-8 -*-
"""
快速路径处理模块

从 langgraph_agent.py 提取的快速路径逻辑：
- 简单查询的快速响应（无需规划）
- 章节信息查询
- 问候响应
"""

import json
import logging
import re
import time
from typing import Dict, Any, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.services.agent.langgraph_agent import WritingAgentGraph

logger = logging.getLogger(__name__)


class QuickPathHandler:
    """快速路径处理器 - 处理简单查询"""

    def __init__(self, agent: "WritingAgentGraph"):
        """
        初始化快速路径处理器

        Args:
            agent: WritingAgentGraph 实例
        """
        self.agent = agent

    async def try_quick_path(
        self,
        message: str,
        work_id: Optional[str],
        on_plan: Optional[callable] = None,
        on_task_start: Optional[callable] = None,
        on_task_done: Optional[callable] = None,
        on_content: Optional[callable] = None,
        on_flow_event: Optional[callable] = None  # v6.2: 添加flow事件回调
    ) -> Optional[Dict[str, Any]]:
        """Planning 模式的快速路径判断

        在规划生成前判断是否可以走快速路径，适用于简单查询：
        - 获取章节标题
        - 获取章节字数
        - 简单问候

        Args:
            message: 用户消息
            work_id: 作品 ID
            on_plan: 规划回调
            on_task_start: 任务开始回调
            on_task_done: 任务完成回调
            on_content: 内容回调

        Returns:
            Optional[Dict]: 如果命中快速路径返回结果，否则返回 None
        """
        from app.services.agent.langgraph_tools import get_chapter_by_order_tool

        # 1. 规则快速判断（不调用 AI）
        quick_action = self._detect_quick_action(message)

        if not quick_action:
            return None

        action_type = quick_action.get("type")
        logger.info(f"[QuickPath-Planning] 命中快速路径: {action_type}")

        # 2. 执行快速路径
        start_time = time.time()

        try:
            if action_type == "get_chapter_info":
                # 获取章节信息
                chapter_order = quick_action.get("chapter_order", 1)
                field = quick_action.get("field", "title")  # title, word_count, content

                if not work_id:
                    return {
                        "response": "需要先选择一部作品才能查看章节信息。",
                        "agent_steps": [{"step": "quick_path", "result": "缺少 work_id"}]
                    }

                # 发送简化的计划
                if on_plan:
                    await on_plan([{
                        "task_id": 1,
                        "description": f"获取第{chapter_order}章信息"
                    }])

                if on_task_start:
                    await on_task_start({"task_id": 1, "description": f"获取第{chapter_order}章信息"})

                # 直接调用工具
                result = await get_chapter_by_order_tool.ainvoke({
                    "work_id": work_id,
                    "chapter_order": chapter_order
                })

                elapsed = time.time() - start_time
                if on_task_done:
                    await on_task_done({
                        "task_id": 1,
                        "description": f"获取第{chapter_order}章信息",
                        "elapsed_time": elapsed
                    })

                # 解析结果
                try:
                    if isinstance(result, str):
                        data = json.loads(result)
                    elif isinstance(result, dict):
                        data = result
                    elif isinstance(result, list):
                        # 如果是 list，取第一个元素或转换
                        data = result[0] if result and isinstance(result[0], dict) else {"content": str(result)}
                    else:
                        data = {"content": str(result)}
                except (json.JSONDecodeError, TypeError, IndexError) as e:
                    logger.warning(f"[QuickPath-Planning] 解析结果失败: {e}, result type: {type(result)}")
                    data = {"error": str(result)}

                # 格式化响应
                if data.get("error"):
                    response = f"获取章节信息失败：{data.get('error')}"
                elif field == "title":
                    response = f"第{chapter_order}章的标题是：**{data.get('title', '未知')}**"
                elif field == "word_count":
                    response = f"第{chapter_order}章共 **{data.get('word_count', 0)}** 字"
                else:
                    title = data.get('title', '未知')
                    word_count = data.get('word_count', 0)
                    response = f"第{chapter_order}章「{title}」共 **{word_count}** 字"

                if on_content:
                    # v6.3: 先发送 output_ready（带空内容），再发送内容
                    if on_flow_event:
                        from app.services.agent.stream.flow_events import FlowEventBuilder
                        await on_flow_event(FlowEventBuilder.agent_header())
                        await on_flow_event(FlowEventBuilder.output_ready("章节信息", "", is_applicable=False))
                    await on_content({"content": response})

                logger.info(f"[QuickPath-Planning] 完成，耗时: {elapsed:.2f}s")

                return {
                    "response": response,
                    "agent_steps": [{
                        "step": "quick_path",
                        "action": action_type,
                        "elapsed": elapsed
                    }]
                }

            elif action_type == "greeting":
                # 问候直接回复
                response = quick_action.get("response", "你好！我是 AI 写作助手，有什么可以帮你的吗？")

                if on_content:
                    # v6.3: 先发送 output_ready（带空内容），再发送内容
                    if on_flow_event:
                        from app.services.agent.stream.flow_events import FlowEventBuilder
                        await on_flow_event(FlowEventBuilder.agent_header())
                        await on_flow_event(FlowEventBuilder.output_ready("问候回复", "", is_applicable=False))
                    await on_content({"content": response})

                return {
                    "response": response,
                    "agent_steps": [{"step": "quick_path", "action": "greeting"}]
                }

        except Exception as e:
            logger.warning(f"[QuickPath-Planning] 执行失败: {e}，降级到规划模式")
            return None

        return None

    def _detect_quick_action(self, message: str) -> Optional[Dict]:
        """规则检测是否可以走快速路径（不调用 AI）

        Returns:
            Dict: {"type": "get_chapter_info", "chapter_order": 5, "field": "title"}
            或 None
        """
        message = message.strip()

        # 1. 问候检测
        greetings = ["你好", "您好", "在吗", "hello", "hi", "嗨"]
        if any(message.lower().startswith(g) for g in greetings) and len(message) < 10:
            return {
                "type": "greeting",
                "response": "你好！我是 AI 写作助手，有什么可以帮你的吗？"
            }

        # 2. 章节标题查询
        # 匹配："第五章的标题是什么"、"第5章标题"、"第三章叫什么"
        title_patterns = [
            r'第([一二三四五六七八九十百千\d]+)章.{0,2}(?:的)?(?:标题|题目|名字|叫什么)',
            r'(?:标题|题目|名字).{0,2}第([一二三四五六七八九十百千\d]+)章',
        ]
        for pattern in title_patterns:
            match = re.search(pattern, message)
            if match:
                chapter_str = match.group(1)
                chapter_order = self._chinese_to_number(chapter_str)
                return {
                    "type": "get_chapter_info",
                    "chapter_order": chapter_order,
                    "field": "title"
                }

        # 3. 章节字数查询
        # 匹配："第三章有多少字"、"第5章字数"
        word_count_patterns = [
            r'第([一二三四五六七八九十百千\d]+)章.{0,3}(?:有)?(?:多少|几)(?:个)?字',
            r'第([一二三四五六七八九十百千\d]+)章.{0,2}(?:的)?字数',
        ]
        for pattern in word_count_patterns:
            match = re.search(pattern, message)
            if match:
                chapter_str = match.group(1)
                chapter_order = self._chinese_to_number(chapter_str)
                return {
                    "type": "get_chapter_info",
                    "chapter_order": chapter_order,
                    "field": "word_count"
                }

        # 4. 不符合快速路径条件
        return None

    @staticmethod
    def _chinese_to_number(s: str) -> int:
        """中文数字转阿拉伯数字"""
        chinese_map = {
            '零': 0, '一': 1, '二': 2, '三': 3, '四': 4,
            '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
            '十': 10, '百': 100, '千': 1000
        }

        # 纯数字
        if s.isdigit():
            return int(s)

        # 简单中文数字（1-99）
        if len(s) == 1 and s in chinese_map:
            return chinese_map[s]

        # "十"、"十一"、"二十"、"二十三" 等
        result = 0
        if '十' in s:
            parts = s.split('十')
            tens = chinese_map.get(parts[0], 1) if parts[0] else 1
            ones = chinese_map.get(parts[1], 0) if len(parts) > 1 and parts[1] else 0
            result = tens * 10 + ones
        else:
            # 单个字符
            result = chinese_map.get(s, 1)

        return result if result > 0 else 1
