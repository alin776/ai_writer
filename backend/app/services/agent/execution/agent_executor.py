# -*- coding: utf-8 -*-
"""
Agent 执行器模块

将 HTTPAIService 模式的执行逻辑从 langgraph_agent.py 中拆分出来，
实现 _handle_with_httpai 的核心功能。

拆分日期：2025-12-25
"""

from typing import Dict, Any, Optional, Callable, TYPE_CHECKING
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
import logging
import json
import re

from app.services.agent.model_selector import TaskType
from app.services.agent.prompts import get_tool_decision_static_prompt
from app.services.agent.utils.tool_helpers import normalize_tool_params
from app.services.agent.core import MessageCleaner
from app.services.agent.prompts.format_guidelines import get_format_guidelines

if TYPE_CHECKING:
    from app.services.agent.langgraph_agent import AgentState
    from app.services.agent.core import SecondaryToolHandler, ToolDispatcher

logger = logging.getLogger(__name__)


class AgentExecutor:
    """
    HTTPAIService 模式的执行引擎

    负责：
    1. 递归深度控制
    2. 工具决策（判断是否需要调用工具）
    3. 工具调用和结果处理
    4. 二次工具调用（编辑意图检测）
    5. 最终响应生成
    """

    # 最大递归深度
    MAX_RECURSION_DEPTH = 5
    # 最大历史消息数量
    MAX_HISTORY_MESSAGES_DECISION = 10  # 工具决策阶段
    MAX_HISTORY_MESSAGES_RESPONSE = 20  # 响应生成阶段

    def __init__(
        self,
        secondary_tool_handler: "SecondaryToolHandler",
        tool_dispatcher: "ToolDispatcher",
        generate_text_func: Callable
    ):
        """
        初始化 Agent 执行器

        Args:
            secondary_tool_handler: 二次工具调用处理器
            tool_dispatcher: 工具分发器
            generate_text_func: 文本生成函数（来自 WritingAgentGraph._generate_text）
        """
        self.secondary_tool_handler = secondary_tool_handler
        self.tool_dispatcher = tool_dispatcher
        self._generate_text = generate_text_func

    async def execute(
        self,
        state: "AgentState",
        agent_type: str,
        system_prompt: str,
        recursion_depth: int = 0
    ) -> Dict[str, Any]:
        """
        HTTPAIService 模式 - 手动工具调用（绕过 Cloudflare）

        Args:
            state: Agent状态
            agent_type: Agent类型
            system_prompt: 系统提示词
            recursion_depth: 递归深度（默认0）

        Returns:
            更新后的状态字典
        """
        # 1. 检查递归深度
        if recursion_depth > self.MAX_RECURSION_DEPTH:
            return self._handle_recursion_limit(agent_type, recursion_depth)

        messages = state["messages"]

        # 2. 检查是否已经有工具结果（第二次进入）
        if messages and isinstance(messages[-1], ToolMessage):
            return await self._handle_tool_result(
                state, agent_type, system_prompt, recursion_depth
            )

        # 3. 第一次进入：使用 HTTPAIService 决定是否需要工具
        return await self._handle_first_entry(
            state, agent_type, system_prompt, recursion_depth
        )

    def _handle_recursion_limit(
        self,
        agent_type: str,
        recursion_depth: int
    ) -> Dict[str, Any]:
        """处理递归深度超限"""
        logger.error(
            f"[AgentExecutor] ❌ 递归深度超限: {recursion_depth} > {self.MAX_RECURSION_DEPTH}，"
            f"可能存在工具循环调用，强制终止"
        )
        return {
            "messages": [AIMessage(content="抱歉，处理您的请求时遇到了问题（递归深度超限），请简化您的需求后重试。")],
            "final_response": "递归深度超限，已强制终止",
            "agent_steps": [{
                "step": f"{agent_type}_recursion_limit",
                "result": f"递归深度{recursion_depth}超过限制{self.MAX_RECURSION_DEPTH}"
            }]
        }

    async def _handle_tool_result(
        self,
        state: "AgentState",
        agent_type: str,
        system_prompt: str,
        recursion_depth: int
    ) -> Dict[str, Any]:
        """处理工具执行结果（第二次进入）"""
        logger.info(f"[AgentExecutor] {agent_type} - 处理工具执行结果 (HTTPAIService)")

        messages = state["messages"]

        # 获取用户原始请求
        user_message = self._extract_user_message(messages)

        # 获取工具结果（防止 None）
        tool_result = messages[-1].content or ""
        logger.info(f"[AgentExecutor] 🔍 工具返回内容长度: {len(tool_result)} 字符")
        if tool_result:
            logger.info(f"[AgentExecutor] 🔍 工具返回内容预览:\n{tool_result[:500]}")

        # 检查是否需要二次工具调用
        secondary_result = await self._check_secondary_tool_call(
            state, user_message, agent_type, tool_result, system_prompt, recursion_depth
        )
        if secondary_result:
            return secondary_result

        # 构建任务指令并生成最终响应
        return await self._generate_final_response(
            state, messages, user_message, tool_result, agent_type, system_prompt
        )

    def _extract_user_message(self, messages: list) -> str:
        """从消息列表中提取用户原始请求"""
        for msg in messages:
            if isinstance(msg, HumanMessage):
                return msg.content or ""  # 修复：防止 None
        return ""

    async def _check_secondary_tool_call(
        self,
        state: "AgentState",
        user_message: str,
        agent_type: str,
        tool_result: str,
        system_prompt: str,
        recursion_depth: int
    ) -> Optional[Dict[str, Any]]:
        """检查并处理二次工具调用"""
        already_did_second_call = state.get("_second_tool_called", False)
        # 2026-01-09: 改用结构化判断，传入 tool_result
        needs_second_tool = self.secondary_tool_handler.needs_secondary_tool_call(
            user_message, agent_type, already_did_second_call, tool_result
        )

        if not needs_second_tool:
            return None

        logger.info(f"[AgentExecutor] 🔄 检测到编辑意图，尝试二次工具调用")

        # 提取 chapter_id
        chapter_id_from_tool = self.secondary_tool_handler.extract_chapter_id_from_tool_result(tool_result)

        if not chapter_id_from_tool:
            logger.info(f"[AgentExecutor] ⚠️ 未能从工具结果中提取chapter_id，继续正常流程")
            return None

        # 更新state中的chapter_id
        state["chapter_id"] = chapter_id_from_tool

        # 执行二次工具调用
        second_result = await self.secondary_tool_handler.handle_secondary_tool_call(
            user_message=user_message,
            tool_result=tool_result,
            chapter_id=chapter_id_from_tool,
            system_prompt=system_prompt,
            state=state
        )

        if not second_result:
            return None

        tool_name = second_result["tool_name"]
        second_tool_result = second_result["tool_result"]

        logger.info(f"[AgentExecutor] ✅ 二次工具调用成功，返回结果长度: {len(second_tool_result)} 字符")

        # 创建工具消息并添加到消息历史
        ai_msg = AIMessage(content=f"我需要使用 {tool_name} 工具来帮助你。")
        tool_msg = ToolMessage(content=second_tool_result, tool_call_id="manual_call_2")

        # 更新state
        updated_state = state.copy()
        updated_state["messages"] = state["messages"] + [ai_msg, tool_msg]
        updated_state["agent_steps"] = state.get("agent_steps", []) + [{
            "step": f"{agent_type}_second_tool_call",
            "result": f"二次调用编辑器工具: {tool_name}",
            "tool_result_length": len(second_tool_result)
        }]
        updated_state["_second_tool_called"] = True

        # 递归处理
        logger.info(f"[AgentExecutor] 🔄 继续处理第二次工具结果 (depth={recursion_depth + 1})")
        return await self.execute(
            updated_state,
            agent_type,
            system_prompt,
            recursion_depth=recursion_depth + 1
        )

    async def _generate_final_response(
        self,
        state: "AgentState",
        messages: list,
        user_message: str,
        tool_result: str,
        agent_type: str,
        system_prompt: str
    ) -> Dict[str, Any]:
        """生成基于工具结果的最终响应"""
        # 使用 SecondaryToolHandler 构建任务指令
        is_read_request, is_write_request = self.secondary_tool_handler.get_user_intent(user_message)
        task_instruction = self.secondary_tool_handler.build_task_instruction(
            user_message=user_message,
            tool_result=tool_result,
            agent_type=agent_type
        )

        # 构建包含历史消息的完整对话上下文
        response_messages = self._build_response_messages(
            messages, system_prompt, task_instruction, agent_type
        )

        logger.info(f"[AgentExecutor] 🧠 工具响应阶段：传递 {len(response_messages)} 条消息给AI（包含历史对话）")

        # 选择 task_type
        selected_task_type = self._select_task_type(
            agent_type, is_read_request, is_write_request
        )

        logger.info(f"[AgentExecutor] {agent_type} 最终响应使用模型: task_type={selected_task_type.value}")

        # 使用 _generate_text 传递完整历史
        try:
            result = await self._generate_text(
                messages=response_messages,
                max_tokens=1500,
                temperature=0.7,
                task_type=selected_task_type
            )
            final_text = result.get("text", "") if result else ""
        except Exception as e:
            logger.error(f"[AgentExecutor] _generate_text 调用失败: {e}")
            final_text = "抱歉，生成响应时遇到了问题，请稍后重试。"

        response = AIMessage(content=final_text)
        return {
            "messages": [response],
            "final_response": final_text,
            "agent_steps": [{
                "step": f"{agent_type}_final_response",
                "result": "基于工具结果生成最终响应 (HTTPAIService)"
            }]
        }

    def _build_response_messages(
        self,
        messages: list,
        system_prompt: str,
        task_instruction: str,
        agent_type: str = "general"
    ) -> list:
        """构建响应阶段的消息列表"""
        response_messages = []

        # 1. 添加系统提示
        response_messages.append({
            "role": "system",
            "content": system_prompt
        })

        # 2. 添加历史对话消息（排除工具调用相关消息）
        history_messages = []
        for msg in messages[:-1]:  # 排除最后一条 ToolMessage
            if isinstance(msg, HumanMessage):
                content = msg.content or ""
                history_messages.append({"role": "user", "content": content})
            elif isinstance(msg, AIMessage):
                content = msg.content or ""
                # 跳过工具调用相关的AI消息
                if content and not content.startswith("我需要使用"):
                    history_messages.append({"role": "assistant", "content": content})

        # 如果历史消息过多，只保留最近的 N 条
        if len(history_messages) > self.MAX_HISTORY_MESSAGES_RESPONSE:
            history_messages = history_messages[-self.MAX_HISTORY_MESSAGES_RESPONSE:]
            logger.info(f"[AgentExecutor] ⚠️ 工具响应阶段：历史消息过多，截断为最近 {self.MAX_HISTORY_MESSAGES_RESPONSE} 条")

        response_messages.extend(history_messages)

        # 3. 添加当前的任务指令（包含工具结果）+ 格式指导
        # 对于 analysis/stuck 等需要丰富格式的场景，使用完整版
        use_lite = agent_type not in ["analysis", "stuck", "planning"]
        format_guidelines = get_format_guidelines(lite=use_lite)
        enhanced_instruction = f"{task_instruction}\n\n{format_guidelines}"

        response_messages.append({
            "role": "user",
            "content": enhanced_instruction
        })

        return response_messages

    def _select_task_type(
        self,
        agent_type: str,
        is_read_request: bool,
        is_write_request: bool
    ) -> TaskType:
        """根据 agent_type 和用户意图智能选择 task_type"""
        if agent_type == "writing":
            if is_read_request and not is_write_request:
                return TaskType.SUMMARIZATION
            else:
                return TaskType.CONTENT_CREATION
        elif agent_type == "stuck":
            return TaskType.SIMPLE_QA
        elif agent_type == "planning":
            return TaskType.STORY_PLANNING
        elif agent_type == "analysis":
            if is_read_request and not is_write_request:
                return TaskType.SUMMARIZATION
            else:
                return TaskType.DEEP_ANALYSIS
        else:
            return TaskType.SUMMARIZATION

    async def _handle_first_entry(
        self,
        state: "AgentState",
        agent_type: str,
        system_prompt: str,
        recursion_depth: int
    ) -> Dict[str, Any]:
        """第一次进入：使用 HTTPAIService 决定是否需要工具"""
        messages = state["messages"]

        # 安全检查：确保 messages 非空
        if not messages:
            logger.warning(f"[AgentExecutor] ⚠️ messages 为空，返回默认响应")
            return self._handle_direct_response(agent_type, {
                "direct_response": "抱歉，我没有收到您的消息，请重新输入。"
            })

        last_user_message = messages[-1].content or ""

        # 构建上下文信息
        context_info = self._build_context_info(state)

        # 获取静态 Prompt
        static_prompt = await get_tool_decision_static_prompt()

        # 动态添加章节上下文提示
        chapter_context_hint = self._build_chapter_context_hint(state)

        # 构建聊天消息
        chat_messages = self._build_decision_messages(
            messages, system_prompt, context_info, static_prompt, chapter_context_hint
        )

        logger.info(f"[AgentExecutor] 🧠 记忆修复：传递 {len(chat_messages)} 条消息给AI（包含历史对话）")

        # 使用 _generate_text 调用 HTTPAIService
        try:
            result = await self._generate_text(
                messages=chat_messages,
                max_tokens=200,
                temperature=0.3,
                task_type=TaskType.SIMPLE_QA
            )
            decision_text = result.get("text", "") if result else ""
        except Exception as e:
            logger.error(f"[AgentExecutor] _generate_text 调用失败: {e}")
            decision_text = ""

        # 解析决策
        decision = self._parse_decision(decision_text)

        logger.info(f"[AgentExecutor] {agent_type} 决策 (HTTPAIService): {decision.get('need_tools', False)}")

        if decision.get("need_tools", False):
            return await self._handle_tool_call(
                state, agent_type, system_prompt, decision, last_user_message, recursion_depth
            )
        else:
            return self._handle_direct_response(agent_type, decision)

    def _build_context_info(self, state: "AgentState") -> str:
        """构建上下文信息"""
        current_work_id = state.get("work_id")
        current_chapter_id = state.get("chapter_id")

        def _format_id(value: Optional[str], max_len: int = 20) -> str:
            if not value:
                return "未设置"
            if len(value) <= max_len:
                return f"{value}"
            return f"{value[:max_len]}..."

        context_info = f"""
当前上下文：
- 作品ID (work_id): {_format_id(current_work_id)}
- 章节ID (chapter_id): {_format_id(current_chapter_id)}
"""

        # Version memory
        last_versions = state.get("context", {}).get("last_rewrite_versions", {})
        if last_versions:
            version_info = "\n[Previous rewrite versions (use when user says 'based on version X')]"
            if last_versions.get("version_a"):
                version_info += f"\n- Version A: {last_versions['version_a'][:100]}..."
            if last_versions.get("version_b"):
                version_info += f"\n- Version B: {last_versions['version_b'][:100]}..."
            if last_versions.get("version_c"):
                version_info += f"\n- Version C: {last_versions['version_c'][:100]}..."
            context_info += version_info
            logger.info(f"[AgentExecutor] Added version memory to context")

        return context_info

    def _build_chapter_context_hint(self, state: "AgentState") -> str:
        """构建章节上下文提示"""
        if not state.get("chapter_id"):
            return ""

        work_id = state.get("work_id", "未知")
        chapter_id = state.get("chapter_id")

        return f"""

⚠️ 【章节上下文提示】：
- 当前用户在章节聊天面板中（work_id={work_id}, chapter_id={chapter_id}）
- 如果用户要求修改/润色/分析本章内容，**必须先调用 read_chapter_tool(work_id="{work_id}", chapter_id="{chapter_id}")** 读取章节原文
- 正确流程：read_chapter_tool → 理解上下文 → smart_rewrite 或其他工具
"""

    def _build_decision_messages(
        self,
        messages: list,
        system_prompt: str,
        context_info: str,
        static_prompt: str,
        chapter_context_hint: str
    ) -> list:
        """构建工具决策阶段的消息列表"""
        chat_messages = []

        # 1. 添加系统提示
        chat_messages.append({
            "role": "system",
            "content": f"""{system_prompt}

{context_info}

{static_prompt}{chapter_context_hint}"""
        })

        # 2. 添加历史对话消息
        history_messages = []
        for msg in messages:
            if isinstance(msg, HumanMessage):
                content = msg.content or ""
                history_messages.append({"role": "user", "content": content})
            elif isinstance(msg, AIMessage):
                content = msg.content or ""
                if content and not content.startswith("我需要使用"):
                    history_messages.append({"role": "assistant", "content": content})

        # 如果历史消息过多，只保留最近的 N 条
        if len(history_messages) > self.MAX_HISTORY_MESSAGES_DECISION:
            history_messages = history_messages[-self.MAX_HISTORY_MESSAGES_DECISION:]
            logger.info(f"[AgentExecutor] ⚠️ 历史消息过多，截断为最近 {self.MAX_HISTORY_MESSAGES_DECISION} 条")

        chat_messages.extend(history_messages)

        return chat_messages

    def _parse_decision(self, decision_text: str) -> Dict[str, Any]:
        """解析 AI 决策"""
        # 防止 None 或空值
        if not decision_text:
            logger.warning(f"[AgentExecutor] decision_text 为空，返回默认决策")
            return {
                "need_tools": False,
                "direct_response": "抱歉，我暂时无法处理您的请求，请稍后重试。"
            }

        logger.info(f"[AgentExecutor] AI 决策原文: {decision_text[:200] if len(decision_text) > 200 else decision_text}")

        decision = None

        # 方法 1: 尝试直接解析整个文本
        try:
            decision = json.loads(decision_text.strip())
            logger.info(f"[AgentExecutor] 方法1成功: 直接解析整个文本")
        except json.JSONDecodeError:
            pass
        except Exception as e:
            logger.warning(f"[AgentExecutor] 方法1解析异常: {e}")

        # 方法 2: 使用正则提取 JSON
        if not decision:
            try:
                json_matches = re.finditer(r'\{(?:[^{}]|(?:\{[^}]*\}))*\}', decision_text)
                for match in json_matches:
                    try:
                        candidate = json.loads(match.group())
                        if "need_tools" in candidate:
                            decision = candidate
                            logger.info(f"[AgentExecutor] 方法2成功: 正则提取 JSON")
                            break
                    except json.JSONDecodeError:
                        continue
            except Exception as e:
                logger.warning(f"[AgentExecutor] 方法2解析异常: {e}")

        # 方法 3: 如果都失败，使用 AI 的原始回答
        if not decision:
            preview = decision_text[:200] if len(decision_text) > 200 else decision_text
            logger.warning(f"[AgentExecutor] 无法解析JSON决策，使用原始回答，原文预览: {preview}")
            decision = {
                "need_tools": False,
                "direct_response": decision_text.strip()
            }

        logger.info(f"[AgentExecutor] 最终决策: {decision}")
        return decision

    async def _handle_tool_call(
        self,
        state: "AgentState",
        agent_type: str,
        system_prompt: str,
        decision: Dict[str, Any],
        last_user_message: str,
        recursion_depth: int
    ) -> Dict[str, Any]:
        """处理需要工具调用的情况"""
        tool_name = decision.get("tool_name", "smart_continue")
        tool_args = decision.get("tool_args", {})

        # 标准化参数格式
        tool_args = normalize_tool_params(tool_name, tool_args)

        # 使用 ToolDispatcher 统一分发工具调用
        tool_result = await self.tool_dispatcher.dispatch_tool(
            tool_name=tool_name,
            tool_args=tool_args,
            state=state,
            last_user_message=last_user_message
        )

        # 创建新消息
        ai_decision = AIMessage(content=f"我需要使用 {tool_name} 工具来帮助你。")
        tool_message = ToolMessage(content=tool_result, tool_call_id="manual_call")

        new_step = {
            "step": f"{agent_type}_tool_call",
            "result": f"调用工具 (HTTPAIService): {tool_name}",
            "tool_result_length": len(tool_result)
        }

        # 创建更新后的 state
        updated_state = state.copy()
        updated_state["messages"] = state["messages"] + [ai_decision, tool_message]
        updated_state["agent_steps"] = state["agent_steps"] + [new_step]

        # 检查工具是否返回错误
        error_response = self._check_tool_error(tool_result, agent_type)
        if error_response:
            return error_response

        # 使用 MessageCleaner 智能清理累积的消息
        current_messages = updated_state["messages"]
        updated_state["messages"] = MessageCleaner.clean_messages(current_messages)

        # 递归处理工具结果
        logger.debug(f"[AgentExecutor] 递归处理工具结果，当前深度={recursion_depth}")
        result = await self.execute(updated_state, agent_type, system_prompt, recursion_depth + 1)

        # 返回所有新增的消息
        return {
            "messages": [ai_decision, tool_message] + result.get("messages", []),
            "final_response": result.get("final_response"),
            "agent_steps": [new_step] + result.get("agent_steps", [])
        }

    def _check_tool_error(
        self,
        tool_result: str,
        agent_type: str
    ) -> Optional[Dict[str, Any]]:
        """检查工具是否返回错误"""
        try:
            tool_result_obj = json.loads(tool_result)
            error_type = tool_result_obj.get("error")
            if error_type in ["missing_work_id", "unknown_tool"]:
                logger.info(f"[AgentExecutor] 🎯 检测到工具错误({error_type})，直接返回友好提示")
                direct_response = tool_result_obj.get("user_prompt", "请先告诉我您要操作哪部作品？")
                return {
                    "messages": [AIMessage(content=direct_response)],
                    "final_response": direct_response,
                    "agent_steps": [{
                        "step": f"{agent_type}_{error_type}",
                        "result": f"检测到错误: {error_type}"
                    }]
                }
        except json.JSONDecodeError:
            pass
        except Exception as e:
            logger.warning(f"[AgentExecutor] 解析工具结果异常: {e}")

        return None

    def _handle_direct_response(
        self,
        agent_type: str,
        decision: Dict[str, Any]
    ) -> Dict[str, Any]:
        """处理不需要工具的直接响应"""
        direct_response = decision.get("direct_response", "抱歉，我无法处理您的请求。")
        response = AIMessage(content=direct_response)
        return {
            "messages": [response],
            "final_response": direct_response,
            "agent_steps": [{
                "step": f"{agent_type}_direct_response",
                "result": "直接响应用户 (HTTPAIService)"
            }]
        }
