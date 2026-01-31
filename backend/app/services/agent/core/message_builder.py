"""
消息构建模块 - 构建 AI 对话消息

从 langgraph_agent.py 的 _handle_with_httpai 方法中拆分。
负责构建传递给 AI 的消息列表。
"""

import logging
from typing import List, Dict, Any, Optional

from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    AIMessage,
)

logger = logging.getLogger(__name__)


class MessageBuilder:
    """消息构建器 - 构建传递给 AI 的消息列表"""

    # 工具响应阶段的最大历史消息数
    MAX_HISTORY_FOR_TOOL_RESPONSE = 20

    # 工具决策阶段的最大历史消息数
    MAX_HISTORY_FOR_DECISION = 10

    @classmethod
    def build_tool_response_messages(
        cls,
        system_prompt: str,
        messages: List[BaseMessage],
        task_instruction: str,
    ) -> List[Dict[str, str]]:
        """
        构建工具响应阶段的消息列表

        用于处理工具执行结果后，生成最终响应。

        Args:
            system_prompt: 系统提示词
            messages: 当前消息历史
            task_instruction: 任务指令（包含工具结果）

        Returns:
            格式化的消息列表
        """
        response_messages = []

        # 1. 添加系统提示
        response_messages.append({
            "role": "system",
            "content": system_prompt
        })

        # 2. 添加历史对话消息（排除工具调用相关消息）
        history_messages = cls._extract_history_messages(
            messages[:-1],  # 排除最后一条 ToolMessage
            max_count=cls.MAX_HISTORY_FOR_TOOL_RESPONSE
        )
        response_messages.extend(history_messages)

        # 3. 添加当前的任务指令（包含工具结果）
        response_messages.append({
            "role": "user",
            "content": task_instruction
        })

        logger.info(
            f"[MessageBuilder] 🧠 工具响应阶段：传递 {len(response_messages)} 条消息给AI"
        )

        return response_messages

    @classmethod
    def build_decision_messages(
        cls,
        system_prompt: str,
        context_info: str,
        static_prompt: str,
        chapter_context_hint: str,
        messages: List[BaseMessage],
    ) -> List[Dict[str, str]]:
        """
        构建工具决策阶段的消息列表

        用于让 AI 决定是否需要调用工具。

        Args:
            system_prompt: 系统提示词
            context_info: 上下文信息
            static_prompt: 静态工具决策 prompt
            chapter_context_hint: 章节上下文提示
            messages: 当前消息历史

        Returns:
            格式化的消息列表
        """
        chat_messages = []

        # 1. 添加系统提示作为第一条消息
        chat_messages.append({
            "role": "system",
            "content": f"{system_prompt}\n\n{context_info}\n\n{static_prompt}{chapter_context_hint}"
        })

        # 2. 添加历史对话消息（保留上下文）
        history_messages = cls._extract_history_messages(
            messages,
            max_count=cls.MAX_HISTORY_FOR_DECISION
        )
        chat_messages.extend(history_messages)

        logger.info(
            f"[MessageBuilder] 🧠 记忆修复：传递 {len(chat_messages)} 条消息给AI（包含历史对话）"
        )

        return chat_messages

    @classmethod
    def _extract_history_messages(
        cls,
        messages: List[BaseMessage],
        max_count: int,
    ) -> List[Dict[str, str]]:
        """
        从消息历史中提取格式化的历史消息

        Args:
            messages: 原始消息列表
            max_count: 最大保留数量

        Returns:
            格式化的历史消息列表
        """
        history_messages = []

        for msg in messages:
            if isinstance(msg, HumanMessage):
                history_messages.append({"role": "user", "content": msg.content})
            elif isinstance(msg, AIMessage):
                # 跳过工具调用相关的 AI 消息
                if not msg.content.startswith("我需要使用"):
                    history_messages.append({"role": "assistant", "content": msg.content})
            # SystemMessage 和 ToolMessage 不添加到历史

        # 如果历史消息过多，只保留最近的 N 条
        if len(history_messages) > max_count:
            history_messages = history_messages[-max_count:]
            logger.info(
                f"[MessageBuilder] ⚠️ 历史消息过多，截断为最近 {max_count} 条"
            )

        return history_messages

    @classmethod
    def build_task_instruction(
        cls,
        agent_type: str,
        user_message: str,
        tool_result: str,
        is_read_request: bool,
        is_write_request: bool,
    ) -> str:
        """
        构建任务指令

        根据 agent 类型和用户意图，构建不同的任务指令。

        Args:
            agent_type: Agent 类型
            user_message: 用户消息
            tool_result: 工具返回结果
            is_read_request: 是否是读取请求
            is_write_request: 是否是写入请求

        Returns:
            任务指令字符串
        """
        if agent_type == "writing":
            if is_read_request and not is_write_request:
                return cls._build_writing_read_instruction(user_message, tool_result)
            else:
                return cls._build_writing_create_instruction(user_message, tool_result)
        elif agent_type == "stuck":
            return cls._build_stuck_instruction(user_message, tool_result)
        elif agent_type == "planning":
            return cls._build_planning_instruction(user_message, tool_result)
        else:  # analysis 或其他
            if is_read_request and not is_write_request:
                return cls._build_analysis_read_instruction(user_message, tool_result)
            else:
                return cls._build_analysis_create_instruction(user_message, tool_result)

    @classmethod
    def _build_writing_read_instruction(cls, user_message: str, tool_result: str) -> str:
        """构建写作场景的读取指令"""
        return f"""用户请求：{user_message}

工具返回的真实数据（JSON格式）：
{tool_result}

【重要指令】
上面是从数据库读取的真实数据，包含作品信息、章节内容、分析片段等。

请按照以下格式清晰地展示给用户：

**作品信息**
- 标题：[从 work_info.title 获取]
- 描述：[从 work_info.description 获取]
- 章节总数：[从 work_info.total_chapters 获取]

**章节信息**
- 章节标题：[从 current_chapter.title 获取]
- 章节序号：第 [从 current_chapter.order 获取] 章
- 字数：[从 current_chapter.word_count 获取]

**章节内容**
[从 current_chapter.content_preview 或完整 content 获取，保持原文格式]

注意：
1. 所有信息必须来自上述JSON数据，不要编造
2. 如果某个字段为空或不存在，标注为"暂无"
3. 用清晰的markdown格式展示
4. 不要添加任何评论、分析或续写"""

    @classmethod
    def _build_writing_create_instruction(cls, user_message: str, tool_result: str) -> str:
        """构建写作场景的创作指令"""
        return f"""用户请求：{user_message}

工具提供的真实上下文数据（JSON格式）：
{tool_result}

【重要指令】
1. 上面的工具返回数据是从数据库读取的真实内容，包含：
   - 作品的真实标题、描述、类型
   - 章节的真实标题、序号、已有内容
   - 从向量数据库检索到的世界观、角色设定等分析片段

2. 你必须仔细阅读上述JSON数据，特别是：
   - current_chapter.content_preview（当前章节已有内容）
   - related_analysis（相关世界观和角色设定）
   - work_info（作品整体信息）

3. 创作续写时，必须：
   - 基于 current_chapter.content_preview 中的真实内容进行续写
   - 保持与已有内容的风格、人物、情节连贯
   - 参考 related_analysis 中的世界观和角色设定
   - 不要编造与上述数据矛盾的信息

4. 如果上述数据中某些字段为空或缺失，说明数据库中确实没有相关内容，此时可以合理发挥创作。

请直接开始续写内容（至少500字），不要重复说明你看到了什么数据。"""

    @classmethod
    def _build_stuck_instruction(cls, user_message: str, tool_result: str) -> str:
        """构建卡壳场景的指令"""
        return f"""用户遇到的问题：{user_message}

当前创作背景：
{tool_result}

请基于背景信息，给用户3-5个具体的创作方向建议，每个建议包含：
1. 方向概述
2. 可以这样写的理由
3. 示例开头（50字左右）"""

    @classmethod
    def _build_planning_instruction(cls, user_message: str, tool_result: str) -> str:
        """构建规划场景的指令"""
        return f"""用户需求：{user_message}

当前信息：
{tool_result}

请基于现有信息，提供详细的规划方案。"""

    @classmethod
    def _build_analysis_read_instruction(cls, user_message: str, tool_result: str) -> str:
        """构建分析场景的读取指令"""
        return f"""用户请求：{user_message}

工具返回的数据：
{tool_result}

请注意：用户想要「查看/读取」内容！
请直接整理并呈现工具返回的数据内容，用清晰易读的格式展示给用户。"""

    @classmethod
    def _build_analysis_create_instruction(cls, user_message: str, tool_result: str) -> str:
        """构建分析场景的创作指令"""
        return f"""用户请求：{user_message}

分析材料：
{tool_result}

请基于材料，生成详细的分析报告。"""

    @classmethod
    def detect_user_intent(cls, user_message: str) -> tuple:
        """
        检测用户意图：是读取还是写入

        Args:
            user_message: 用户消息

        Returns:
            (is_read_request, is_write_request)
        """
        read_keywords = ["读", "看", "查看", "显示", "展示", "告诉我", "第几章", "内容是什么"]
        # 2026-01-09: 添加编辑意图词，与 secondary_tool_handler.py 保持一致
        write_keywords = [
            "写", "续写", "创作", "生成", "继续", "扩写", "补充",
            "修改", "改写", "重写", "润色", "优化"  # 编辑类
        ]

        is_read_request = any(keyword in user_message for keyword in read_keywords)
        is_write_request = any(keyword in user_message for keyword in write_keywords)

        return is_read_request, is_write_request

    @classmethod
    def format_id(cls, value: Optional[str], max_len: int = 20) -> str:
        """
        格式化 ID 值，安全截断过长 ID

        Args:
            value: ID 值
            max_len: 最大长度

        Returns:
            格式化后的 ID 字符串
        """
        if not value:
            return "未设置"
        if len(value) <= max_len:
            return f"{value}"
        return f"{value[:max_len]}..."
