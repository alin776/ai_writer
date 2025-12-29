# -*- coding: utf-8 -*-
"""
意图分类器

从 langgraph_agent.py 提取的意图分类逻辑，包括：
- 规则快速分类
- AI 语义分类
- CoT 复杂度判断
"""

from typing import Dict, Any, Optional, Tuple
import re
import json
import logging

from app.services.agent.model_selector import TaskType
from app.services.agent.prompt_cache import get_complexity_decision_prompt

logger = logging.getLogger(__name__)


class IntentClassifier:
    """意图分类器

    支持三种分类模式：
    1. 规则快速通道（<1ms）
    2. AI 语义分类
    3. CoT 复杂度判断
    """

    def __init__(self, ai_service):
        """
        Args:
            ai_service: HTTPAIService 实例
        """
        self.ai_service = ai_service

    # ==================== 规则分类 ====================

    def classify_by_rules(self, message: str) -> Tuple[str, float]:
        """基于规则的快速意图识别（<1ms）

        Args:
            message: 用户消息内容

        Returns:
            tuple[str, float]: (intent类型, 置信度)
        """
        msg = message.lower().strip()

        # ========== 极简快速通道（只处理极端情况）==========
        # 这里只处理明显不需要AI判断的情况，其他全部交给AI

        # 1. 空消息或纯空白
        if not msg or len(msg.strip()) == 0:
            logger.info("[Intent] 空消息，判定为 general")
            return "general", 0.99

        # 2. 纯标点/表情（长度<=3且无中文字母数字）
        if len(msg) <= 3 and not re.search(r'[\u4e00-\u9fa5a-zA-Z0-9]', msg):
            logger.info(f"[Intent] 纯标点/表情: {msg}，判定为 general")
            return "general", 0.99

        # 3. 章节模式强匹配（这是明确的写作意图，可以快速判断）
        chapter_pattern = r'第[一二三四五六七八九十\d]+章|chapter\s*\d+'
        if re.search(chapter_pattern, msg, re.IGNORECASE):
            logger.info(f"[Intent] 匹配章节模式: {re.findall(chapter_pattern, msg, re.IGNORECASE)}")
            return "writing", 0.98

        # ========== 其他情况交给AI判断 ==========
        # 不再使用硬编码关键词列表，让AI做语义理解
        logger.info("[Intent] 交给AI进行语义分类")
        return "unknown", 0.3  # 低置信度，强制触发AI判断

    # ==================== AI 分类 ====================

    async def classify_by_ai(self, message: str) -> Tuple[str, float]:
        """使用AI进行意图分类（兜底方案）

        当规则匹配置信度不足时，调用轻量级LLM判断意图

        Args:
            message: 用户消息

        Returns:
            tuple[str, float]: (intent类型, 置信度)
        """
        prompt = f"""你是意图分类器。根据用户消息判断其意图类型。

用户消息: "{message}"

可选意图类型:
- writing: 用户明确要求AI帮忙修改、改写、续写、创作具体内容（必须有明确的创作指令）
- planning: 用户想要规划具体作品的大纲、设计角色、构建世界观
- analysis: 用户想要分析、评估、诊断已有文本的质量
- stuck: 用户写作卡住了，需要AI帮忙生成具体的灵感或内容建议
- general: 普通对话、闲聊、知识问答、写作技巧咨询、不确定的情况

【关键判断规则】
1. 询问"怎么写"、"如何写好"、"写作技巧"等 → general（知识问答，直接回答技巧）
2. 明确要求"帮我写"、"续写"、"修改第X章" → writing（创作请求）
3. 简短的问候、自我介绍询问、感谢 → general
4. 如果用户只是问问题而不是要求创作 → general
5. 不要过度解读用户意图，模糊情况优先判定为 general

只返回一个单词（writing/planning/analysis/stuck/general），不要解释:"""

        try:
            result = await self.ai_service.call_ai(
                system_prompt="你是精确的意图分类器，只返回一个意图类型单词。",
                user_prompt=prompt,
                max_tokens=20,  # 只需要一个单词
                temperature=0.1,  # 低温度，确保稳定输出
                task_type=TaskType.TEXT_CLASSIFICATION
            )

            # 解析结果
            intent = result.strip().lower()
            valid_intents = ["writing", "planning", "analysis", "stuck", "general"]

            if intent in valid_intents:
                logger.info(f"[Intent] AI识别结果: {intent}")
                return intent, 0.90
            else:
                # 尝试从返回中提取有效意图
                for valid in valid_intents:
                    if valid in intent:
                        logger.info(f"[Intent] AI识别结果（提取）: {valid}")
                        return valid, 0.85

                logger.warning(f"[Intent] AI返回无效意图: {intent}，降级为general")
                return "general", 0.70

        except Exception as e:
            logger.error(f"[Intent] AI意图分类失败: {e}，降级为general")
            return "general", 0.60

    # ==================== 复杂度判断 ====================

    async def judge_complexity(self, message: str, intent: str) -> Dict:
        """判断请求复杂度并确定执行方案

        Args:
            message: 用户消息
            intent: 已识别的意图类型

        Returns:
            Dict: {"complexity": "simple|complex", "action": {...}}
        """
        prompt_template = await get_complexity_decision_prompt()
        prompt = prompt_template.format(intent=intent, message=message)

        try:
            result = await self.ai_service.call_ai(
                system_prompt="你是执行路径决策器，返回严格的JSON格式。",
                user_prompt=prompt,
                max_tokens=300,
                temperature=0.1,
                task_type=TaskType.TEXT_CLASSIFICATION
            )

            decision = self._extract_json_from_text(result)
            if decision and decision.get("complexity"):
                return decision

        except Exception as e:
            logger.warning(f"[Intent-CoT] 复杂度判断失败: {e}，降级为 complex")

        # 降级：默认为 complex
        return {"complexity": "complex", "action": {}}

    # ==================== 快速路径检测 ====================

    def detect_quick_action(self, message: str) -> Optional[Dict]:
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

    # ==================== 辅助方法 ====================

    def _chinese_to_number(self, s: str) -> int:
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

    def _extract_json_from_text(self, text: str) -> Optional[dict]:
        """从文本中提取 JSON"""
        try:
            # 尝试直接解析
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        # 尝试提取 JSON 块
        json_pattern = r'\{[^{}]*\}'
        match = re.search(json_pattern, text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass

        return None
