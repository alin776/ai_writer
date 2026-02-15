# -*- coding: utf-8 -*-
"""
统一意图路由器 - 优雅的意图识别解决方案

核心优势：
1. 一次AI调用完成意图识别+复杂度判断+参数提取
2. 使用Pydantic确保类型安全
3. 支持对话历史和上下文
4. 结构化输出，无需解析JSON
"""

from pydantic import BaseModel, Field
from typing import Literal, Optional, Dict, Any, List
from datetime import datetime
import logging
import json
import re

logger = logging.getLogger(__name__)


class IntentRoute(BaseModel):
    """统一的意图路由结果"""

    # 意图类型
    intent: Literal[
        "writing",       # 创作内容（续写、改写、润色）
        "planning",      # 规划设计（大纲、角色、世界观）
        "analysis",      # 分析评估（质量分析、诊断）
        "query_simple",  # 简单查询（直接执行工具，如"第X章标题"）
        "query_complex", # 复杂查询（需要分析，如"第X章讲了什么"）
        "chat",          # 普通对话（问候、闲聊）
        "stuck"          # 写作卡顿（需要灵感）
    ] = Field(description="用户意图类型")

    # 执行策略
    execution: Literal["direct", "agent", "multi_agent"] = Field(
        description="执行策略：direct=直接执行工具或回答，agent=单Agent处理，multi_agent=多Agent协作"
    )

    # 工具调用（如果是direct且需要工具）
    tool_call: Optional[Dict[str, Any]] = Field(
        default=None,
        description="工具名称和参数，例如: {'name': 'explore_content', 'args': {'target_task': '获取第五章标题'}}"
    )

    # 直接回答（如果是direct且不需要工具）
    direct_answer: Optional[str] = Field(
        default=None,
        description="可以直接回答的内容（用于问候、简单问答）"
    )

    # 前置动作（多意图优先级识别）
    prerequisite_actions: Optional[List[Dict[str, Any]]] = Field(
        default=None,
        description="在主要意图之前需要执行的动作，例如: [{'action': 'analyze', 'target': '前两章'}]"
    )

    # 置信度
    confidence: float = Field(ge=0.0, le=1.0, description="判断置信度")

    # 推理过程
    reasoning: str = Field(description="判断依据（简短说明）")


class UnifiedIntentRouter:
    """统一意图路由器"""

    def __init__(self, ai_service):
        self.ai_service = ai_service

    async def route(
        self,
        message: str,
        context: Dict[str, Any],
        conversation_history: Optional[List[Dict]] = None
    ) -> IntentRoute:
        """统一的意图识别 - 一次AI调用完成所有判断

        Args:
            message: 用户消息
            context: 上下文信息（selected_text, chapter_id等）
            conversation_history: 对话历史（最近3轮）

        Returns:
            IntentRoute: 路由决策结果
        """

        # 1. 检查编辑器选中文字（强制判定为writing）
        selected_text = context.get("selected_text", "")
        if selected_text and len(selected_text.strip()) > 0:
            logger.info(f"[UnifiedRouter] 检测到选中文字 ({len(selected_text)}字符)，强制判定为 writing/multi_agent")
            return IntentRoute(
                intent="writing",
                execution="multi_agent",
                confidence=0.99,
                reasoning="编辑器选中文字模式，自动判定为写作任务"
            )

        # 2. 快速规则匹配（处理极端情况）
        quick_route = self._quick_rule_match(message)
        if quick_route:
            return quick_route

        # 3. AI统一路由（意图+复杂度+参数一次完成）
        try:
            return await self._ai_unified_route(message, context, conversation_history)
        except Exception as e:
            logger.error(f"[UnifiedRouter] AI路由失败: {e}，降级到规则匹配")
            return self._fallback_route(message)

    def _quick_rule_match(self, message: str) -> Optional[IntentRoute]:
        """快速规则匹配（处理极端情况）"""

        msg = message.lower().strip()

        # 1. 空消息
        if not msg or len(msg) == 0:
            return IntentRoute(
                intent="chat",
                execution="direct",
                direct_answer="你好！我是AI写作助手，可以帮你续写章节、规划大纲、分析内容。有什么可以帮你的吗？",
                confidence=0.99,
                reasoning="空消息，返回默认问候"
            )

        # 2. 纯标点/表情
        if len(msg) <= 3 and not re.search(r'[\u4e00-\u9fa5a-zA-Z0-9]', msg):
            return IntentRoute(
                intent="chat",
                execution="direct",
                direct_answer="我在呢！有什么可以帮你的吗？",
                confidence=0.99,
                reasoning="纯标点/表情，返回简单回应"
            )

        # 3. 简单问候
        greetings = ["你好", "hi", "hello", "嗨", "在吗", "在不在"]
        if any(g in msg for g in greetings) and len(msg) < 10:
            return IntentRoute(
                intent="chat",
                execution="direct",
                direct_answer="你好！我是AI写作助手，可以帮你续写章节、规划大纲、分析内容。有什么可以帮你的吗？",
                confidence=0.95,
                reasoning="简单问候，直接回答"
            )

        # 其他情况交给AI判断
        return None

    async def _ai_unified_route(
        self,
        message: str,
        context: Dict[str, Any],
        conversation_history: Optional[List[Dict]] = None
    ) -> IntentRoute:
        """AI统一路由 - 使用结构化输出"""

        # 构建上下文提示
        context_prompt = self._build_context_prompt(context, conversation_history)

        # 系统提示
        system_prompt = """你是智能路由器，负责理解用户意图并决定最优执行路径。

## 意图类型定义

1. **writing** - 创作内容
   - 明确要求续写、改写、润色、扩写
   - 关键词：续写、写、改写、润色、扩写、继续写
   - 示例："续写第五章"、"润色这段对话"、"把战斗场面写得更精彩"

2. **planning** - 规划设计
   - 规划大纲、设定世界观、角色设定、情节设计
   - 关键词：大纲、规划、设定、世界观、角色、情节
   - 示例："帮我规划小说大纲"、"设计一个修仙世界观"

3. **analysis** - 分析评估
   - 分析文本质量、评估内容、诊断问题
   - 关键词：分析、评估、诊断、检查、质量
   - 示例："分析这段文字"、"评估第三章质量"

4. **query_simple** - 简单查询（直接执行工具）
   - 查询章节标题、字数、基本信息
   - 特征：只需要1个工具调用，无需分析
   - 示例："第五章的标题是什么"、"第三章有多少字"、"获取作品信息"

5. **query_complex** - 复杂查询（需要分析）
   - 查询章节内容并需要概括、分析
   - 特征：需要先获取内容，再进行分析
   - 示例："第三章讲了什么"、"前面写了什么内容"

6. **chat** - 普通对话
   - 问候、闲聊、简单问答、感谢
   - 示例："谢谢"、"好的"、"明白了"

7. **stuck** - 写作卡顿
   - 写作遇到困难，需要灵感或建议
   - 关键词：卡文、写不下去、没思路、需要灵感
   - 示例："我写不下去了"、"卡文了"

## 执行策略

- **direct**: 直接执行工具或直接回答（用于query_simple和chat）
- **agent**: 单Agent处理（用于query_complex、analysis、planning、stuck）
- **multi_agent**: 多Agent协作（用于writing，需要完整的创作流程）

## 判断规则

1. 如果提到"第X章"：
   - 如果只是查询标题/字数 → query_simple + direct + 提供工具调用
   - 如果要查询内容/概括 → query_complex + agent
   - 如果要续写/改写 → writing + multi_agent

2. 如果是问候/感谢 → chat + direct + 提供直接回答

3. 考虑对话历史：
   - 如果用户说"再加点"、"继续"，参考上一轮意图
   - 如果上一轮是writing，这一轮可能也是writing

4. 不确定时，优先选择更保守的策略（agent而非direct）

## 多意图优先级识别

当用户请求包含多个动作时，识别主要意图（目标）和前置动作（手段）：

**识别规则**：
- "然后"、"接着"、"再" → 后面的是主要意图
- "先...再..."、"帮我...然后..." → 前面是前置动作，后面是主要意图
- 前置动作会静默执行，结果用于主要意图

**示例1**：
用户："帮我分析前两章的内容，然后续写这一章"
```json
{
  "intent": "writing",
  "execution": "multi_agent",
  "prerequisite_actions": [{"action": "analysis", "target": "前两章"}],
  "reasoning": "主要意图是续写，分析是前置步骤"
}
```

**示例2**：
用户："先总结第三章，再写第四章"
```json
{
  "intent": "writing",
  "execution": "multi_agent",
  "prerequisite_actions": [{"action": "analysis", "target": "第三章"}],
  "reasoning": "主要意图是写第四章，总结第三章是前置步骤"
}
```

**示例3**：
用户："查看第五章标题，接着续写"
```json
{
  "intent": "writing",
  "execution": "multi_agent",
  "prerequisite_actions": [{"action": "query", "target": "第五章标题"}],
  "reasoning": "主要意图是续写，查看标题是前置步骤"
}
```

**注意**：如果只有单一意图，prerequisite_actions应为null。

## 可用工具列表

当判断为query_simple + direct时，可以使用以下工具：

1. **explore_content** - 统一信息获取工具（推荐！）
   - 参数：target_task (str) - 描述任务目标
   - 返回：根据任务自动获取所需信息
   - 用于：所有信息获取任务

2. **get_context_tool** - 获取作品上下文信息
   - 参数：无
   - 返回：作品摘要和上下文
   - 用于："获取作品信息"、"作品背景"

3. **read_chapter_tool** - 读取章节完整内容
   - 参数：chapter_id (str) - 章节ID
   - 返回：章节内容
   - 用于："读取第X章"（需要先知道chapter_id）

注意：如果用户查询标题/字数等元数据，使用explore_content即可。
如果需要分析内容，应该判定为query_complex + agent。"""

        # 用户提示
        user_prompt = f"""用户消息: {message}

{context_prompt}

请分析用户意图并返回路由决策。返回JSON格式：
{{
  "intent": "writing|planning|analysis|query_simple|query_complex|chat|stuck",
  "execution": "direct|agent|multi_agent",
  "tool_call": {{"name": "工具名", "args": {{"参数": "值"}}}},  // 仅当execution=direct且需要工具时
  "direct_answer": "直接回答内容",  // 仅当execution=direct且不需要工具时
  "confidence": 0.95,
  "reasoning": "判断依据"
}}

示例1 - 简单查询：
用户："第五章的标题是什么"
返回：
{{
  "intent": "query_simple",
  "execution": "direct",
  "tool_call": {{"name": "explore_content", "args": {{"target_task": "获取第五章的标题"}}}},
  "confidence": 0.95,
  "reasoning": "查询章节标题，直接调用工具"
}}

示例2 - 复杂查询：
用户："第三章讲了什么"
返回：
{{
  "intent": "query_complex",
  "execution": "agent",
  "confidence": 0.90,
  "reasoning": "需要获取内容并概括，复杂查询"
}}

示例3 - 问候：
用户："你好"
返回：
{{
  "intent": "chat",
  "execution": "direct",
  "direct_answer": "你好！我是AI写作助手，可以帮你续写章节、规划大纲、分析内容。有什么可以帮你的吗？",
  "confidence": 0.95,
  "reasoning": "简单问候，直接回答"
}}"""

        # 调用AI
        from app.services.agent.model_selector import TaskType

        result = await self.ai_service.call_ai(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            max_tokens=300,
            temperature=0.1,
            task_type=TaskType.TEXT_CLASSIFICATION
        )

        # 解析JSON
        route_data = self._extract_json_from_text(result)

        # 验证并返回
        route = IntentRoute.model_validate(route_data)

        logger.info(
            f"[UnifiedRouter] {route.intent}/{route.execution} "
            f"(confidence={route.confidence:.2f})"
        )

        return route

    def _build_context_prompt(
        self,
        context: Dict[str, Any],
        conversation_history: Optional[List[Dict]] = None
    ) -> str:
        """构建上下文提示"""

        parts = []

        # 对话历史（最近3轮）
        if conversation_history and len(conversation_history) > 0:
            recent = conversation_history[-3:]
            history_lines = []
            for msg in recent:
                role = msg.get("role", "user")
                content = msg.get("content", "")[:50]
                history_lines.append(f"  - {role}: {content}...")
            parts.append("对话历史:\n" + "\n".join(history_lines))

        # 当前章节
        if context.get("chapter_id"):
            parts.append(f"当前章节ID: {context['chapter_id']}")

        # 作品ID
        if context.get("work_id"):
            parts.append(f"当前作品ID: {context['work_id']}")

        return "\n\n".join(parts) if parts else "（无额外上下文）"

    def _extract_json_from_text(self, text: str) -> Dict:
        """从文本中提取JSON"""
        # 尝试直接解析
        try:
            return json.loads(text)
        except:
            pass

        # 尝试提取```json...```
        json_match = re.search(r'```json\s*(\{.*?\})\s*```', text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except:
                pass

        # 尝试提取第一个{}
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(0))
            except:
                pass

        raise ValueError(f"无法从文本中提取JSON: {text[:200]}")

    def _fallback_route(self, message: str) -> IntentRoute:
        """降级路由（AI失败时使用）"""

        msg = message.lower()

        # 简单规则匹配
        if any(kw in msg for kw in ["续写", "写", "改写", "润色", "扩写"]):
            return IntentRoute(
                intent="writing",
                execution="multi_agent",
                confidence=0.70,
                reasoning="降级规则匹配：检测到写作关键词"
            )

        if any(kw in msg for kw in ["大纲", "规划", "设定", "世界观", "角色"]):
            return IntentRoute(
                intent="planning",
                execution="agent",
                confidence=0.70,
                reasoning="降级规则匹配：检测到规划关键词"
            )

        if any(kw in msg for kw in ["分析", "评估", "诊断", "检查"]):
            return IntentRoute(
                intent="analysis",
                execution="agent",
                confidence=0.70,
                reasoning="降级规则匹配：检测到分析关键词"
            )

        # 默认：普通对话
        return IntentRoute(
            intent="chat",
            execution="agent",
            confidence=0.60,
            reasoning="降级规则匹配：无法识别，默认为对话"
        )
