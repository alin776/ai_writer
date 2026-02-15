# -*- coding: utf-8 -*-
"""
场景处理器

从 langgraph_agent.py 提取的 5 个场景处理方法：
- writing: 写作场景
- planning: 规划场景
- analysis: 分析场景
- stuck: 卡文场景
- general: 一般对话
"""

from typing import TYPE_CHECKING
import logging

from langchain_core.messages import AIMessage, HumanMessage

if TYPE_CHECKING:
    from app.services.agent.langgraph_agent import AgentState

logger = logging.getLogger(__name__)


async def handle_writing(agent, state: "AgentState") -> "AgentState":
    """处理写作场景 - 使用新架构

    新架构流程：
    1. 使用WritingAction.prepare()准备参数
    2. 调用_handle_agent_with_tools统一处理（触发监控）
    """
    from app.services.agent.actions import WritingAction

    logger.info("[LangGraph] 处理写作请求（新架构）")

    # 1. 使用Action准备参数（业务逻辑）
    writing_action = WritingAction()
    prep_result = await writing_action.prepare(state)

    # 2. 检查准备结果
    if not prep_result.success:
        logger.error(f"[LangGraph] WritingAction.prepare()失败: {prep_result.error}")
        error_msg = AIMessage(content=f"抱歉，写作请求处理失败: {prep_result.error}")
        return {
            "messages": [error_msg],
            "final_response": error_msg.content,
            "agent_steps": [{
                "step": "writing_error",
                "result": f"准备失败: {prep_result.error}"
            }]
        }

    # 3. 记录业务信息
    logger.info(
        f"[LangGraph] WritingAction准备完成: "
        f"phase={prep_result.metadata.get('phase')}, "
        f"chapter_num={prep_result.metadata.get('chapter_num')}"
    )

    # 4. 统一使用框架调用LLM（触发监控）
    return await agent._handle_agent_with_tools(
        state,
        agent_type=prep_result.metadata.get("agent_type", "writing"),
        system_prompt=prep_result.system_prompt
    )


async def handle_planning(agent, state: "AgentState") -> "AgentState":
    """处理规划场景 - 使用新架构

    新架构流程：
    1. 使用PlanningAction.prepare()准备参数
    2. 调用_handle_agent_with_tools统一处理（触发监控）
    """
    from app.services.agent.actions import PlanningAction

    logger.info("[LangGraph] 处理规划请求（新架构）")

    # 1. 使用Action准备参数（业务逻辑）
    planning_action = PlanningAction()
    prep_result = await planning_action.prepare(state)

    # 2. 检查准备结果
    if not prep_result.success:
        logger.error(f"[LangGraph] PlanningAction.prepare()失败: {prep_result.error}")
        error_msg = AIMessage(content=f"抱歉，规划请求处理失败: {prep_result.error}")
        return {
            "messages": [error_msg],
            "final_response": error_msg.content,
            "agent_steps": [{
                "step": "planning_error",
                "result": f"准备失败: {prep_result.error}"
            }]
        }

    # 3. 统一使用框架调用LLM（触发监控）
    return await agent._handle_agent_with_tools(
        state,
        agent_type=prep_result.metadata.get("agent_type", "planning"),
        system_prompt=prep_result.system_prompt
    )


async def handle_analysis(agent, state: "AgentState") -> "AgentState":
    """处理分析场景 - 使用新架构

    新架构流程：
    1. 使用AnalysisAction.prepare()准备参数
    2. 调用_handle_agent_with_tools统一处理（触发监控）
    """
    from app.services.agent.actions import AnalysisAction

    logger.info("[LangGraph] 处理分析请求（新架构）")

    # 1. 使用Action准备参数（业务逻辑）
    analysis_action = AnalysisAction()
    prep_result = await analysis_action.prepare(state)

    # 2. 检查准备结果
    if not prep_result.success:
        logger.error(f"[LangGraph] AnalysisAction.prepare()失败: {prep_result.error}")
        error_msg = AIMessage(content=f"抱歉，分析请求处理失败: {prep_result.error}")
        return {
            "messages": [error_msg],
            "final_response": error_msg.content,
            "agent_steps": [{
                "step": "analysis_error",
                "result": f"准备失败: {prep_result.error}"
            }]
        }

    # 3. 记录业务信息
    logger.info(
        f"[LangGraph] AnalysisAction准备完成: "
        f"work_id={prep_result.metadata.get('work_id')}, "
        f"chapter_id={prep_result.metadata.get('chapter_id')}"
    )

    # 4. 统一使用框架调用LLM（触发监控）
    return await agent._handle_agent_with_tools(
        state,
        agent_type=prep_result.metadata.get("agent_type", "analysis"),
        system_prompt=prep_result.system_prompt
    )


async def handle_stuck(agent, state: "AgentState") -> "AgentState":
    """处理卡文场景 - 使用新架构

    新架构流程：
    1. 使用StuckAction.prepare()准备参数
    2. 调用_handle_agent_with_tools统一处理（触发监控）
    """
    from app.services.agent.actions import StuckAction

    logger.info("[LangGraph] 处理卡文请求（新架构）")

    # 1. 使用Action准备参数（业务逻辑）
    stuck_action = StuckAction()
    prep_result = await stuck_action.prepare(state)

    # 2. 检查准备结果
    if not prep_result.success:
        logger.error(f"[LangGraph] StuckAction.prepare()失败: {prep_result.error}")
        error_msg = AIMessage(content=f"抱歉，卡文请求处理失败: {prep_result.error}")
        return {
            "messages": [error_msg],
            "final_response": error_msg.content,
            "agent_steps": [{
                "step": "stuck_error",
                "result": f"准备失败: {prep_result.error}"
            }]
        }

    # 3. 记录业务信息
    logger.info(
        f"[LangGraph] StuckAction准备完成: "
        f"work_id={prep_result.metadata.get('work_id')}, "
        f"chapter_id={prep_result.metadata.get('chapter_id')}"
    )

    # 4. 统一使用框架调用LLM（触发监控）
    return await agent._handle_agent_with_tools(
        state,
        agent_type=prep_result.metadata.get("agent_type", "stuck"),
        system_prompt=prep_result.system_prompt
    )


async def handle_general(agent, state: "AgentState") -> "AgentState":
    """处理一般对话 - 支持工具调用的智能对话模式

    ✅ 新版本：general意图也支持工具调用（如查询世界观、读取章节等）

    流程：
    1. 使用GeneralChatAction.prepare()准备参数
    2. 调用_handle_agent_with_tools统一处理（支持工具调用）

    改进说明：
    - 之前版本完全跳过工具决策，导致无法查询世界观等信息
    - 新版本与其他场景一致，都通过_handle_agent_with_tools处理
    - 保留了general特有的prompt设置
    """
    from app.services.agent.actions import GeneralChatAction

    logger.info("[LangGraph] 处理一般对话（新架构，支持工具调用）")

    # 1. 使用Action准备参数（业务逻辑）
    general_action = GeneralChatAction()
    prep_result = await general_action.prepare(state)

    # 2. 检查准备结果
    if not prep_result.success:
        logger.error(f"[LangGraph] GeneralChatAction.prepare()失败: {prep_result.error}")
        error_msg = AIMessage(content=f"抱歉，无法处理您的请求: {prep_result.error}")
        return {
            "messages": [error_msg],
            "final_response": error_msg.content,
            "agent_steps": [{
                "step": "general_chat_error",
                "result": f"准备失败: {prep_result.error}"
            }]
        }

    logger.info(f"[LangGraph] General准备完成，agent_type={prep_result.metadata.get('agent_type', 'general')}")

    # 3. ✅ 统一使用框架调用LLM（支持工具调用，触发监控）
    return await agent._handle_agent_with_tools(
        state,
        agent_type=prep_result.metadata.get("agent_type", "general"),
        system_prompt=prep_result.system_prompt
    )
