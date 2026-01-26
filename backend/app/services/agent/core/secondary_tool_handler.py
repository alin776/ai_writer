# -*- coding: utf-8 -*-
"""
二次工具调用处理器

负责处理工具执行后的二次工具调用逻辑，主要场景：
- 用户说"修改第2章"，AI先调get_chapter_by_order_tool获取chapter_id
- 然后需要调用smart_rewrite进行实际修改

从 langgraph_agent.py 拆分，减少主文件复杂度
"""

import json
import re
import logging
from typing import Dict, Any, Optional, Tuple, Callable, Awaitable

from langchain_core.messages import AIMessage, ToolMessage

from app.services.agent.tools import registry
from app.services.agent.tools.editor_tools import (
    smart_continue,
    smart_rewrite,
    smart_insert,
    apply_chapter_edit
)
from app.services.agent.model_selector import TaskType

logger = logging.getLogger(__name__)


class SecondaryToolHandler:
    """二次工具调用处理器

    处理工具执行后需要进行的二次工具调用，主要用于编辑器工具链式调用
    """

    # 修改意图关键词（已弃用，保留作为参考）
    # 现在改用结构化判断，不再依赖硬编码关键词
    _LEGACY_MODIFY_KEYWORDS = [
        "修改", "改写", "重写", "续写", "插入", "帮我改", "你来改",
        "来帮我改", "改一下", "太平淡", "帮改", "改改", "优化", "扩写", "润色"
    ]

    # 读取意图关键词
    READ_KEYWORDS = ["读", "看", "查看", "显示", "展示", "告诉我", "第几章", "内容是什么"]

    # 写作/编辑意图关键词（包含创作和编辑两类）
    # 2026-01-09: 添加编辑意图词，避免"看看第三章，帮我优化一下"被误判为纯读取
    WRITE_KEYWORDS = [
        # 创作类
        "写", "续写", "创作", "生成", "继续", "补充",
        # 编辑类（改写/润色场景）
        "修改", "改写", "重写", "润色", "优化", "扩写",
        "帮我改", "改一下", "帮改", "改改", "太平淡"
    ]

    # 获取类工具（返回数据，不执行编辑）
    GETTER_TOOLS = [
        "get_chapter_by_order_tool",
        "get_context_tool",
        "read_chapter_tool",
        "search_analysis_fragments_tool",
        "search_content",
        "get_worldview_summary"
    ]

    # 编辑类工具（执行实际编辑，会返回 requires_confirmation）
    EDITOR_TOOLS = [
        "smart_rewrite",
        "smart_continue",
        "smart_insert",
        "apply_chapter_edit"
    ]

    def __init__(self, generate_text_func: Callable[..., Awaitable[Dict[str, Any]]]):
        """
        初始化

        Args:
            generate_text_func: AI 文本生成函数（从主类传入）
        """
        self._generate_text = generate_text_func

    def needs_secondary_tool_call(
        self,
        user_message: str,
        agent_type: str,
        already_did_second_call: bool,
        tool_result: str = None
    ) -> bool:
        """检查是否需要二次工具调用

        改进说明（2026-01-09）：
        移除硬编码关键词判断，改用结构化判断：
        - 基于第一次工具调用结果的结构来判断
        - 如果结果包含 chapter_id 且不是编辑器工具的结果，则可能需要二次调用

        Args:
            user_message: 用户消息
            agent_type: Agent 类型
            already_did_second_call: 是否已执行过二次调用
            tool_result: 第一次工具调用的结果（JSON字符串）

        Returns:
            是否需要二次工具调用
        """
        # 基础检查
        if already_did_second_call:
            return False
        if agent_type != "writing":
            return False

        # 如果没有工具结果，无法判断
        if not tool_result:
            return False

        # 结构化判断：分析工具结果
        try:
            result = json.loads(tool_result)

            # 1. 检查是否已经是编辑器工具的结果（有 requires_confirmation）
            if result.get("requires_confirmation"):
                # 已经是编辑器工具结果，不需要二次调用
                return False

            # 2. 检查是否已经是错误结果
            if result.get("error"):
                return False

            # 3. 检查是否包含 chapter_id（说明是获取类工具的结果）
            has_chapter_id = (
                result.get("chapter_id") or
                (result.get("current_chapter") or {}).get("id") or
                (result.get("chapter") or {}).get("id")
            )

            # 4. 检查是否有章节内容（说明成功获取了数据）
            has_content = (
                result.get("content") or
                (result.get("current_chapter") or {}).get("content") or
                (result.get("chapter") or {}).get("content")
            )

            # 5. 如果是纯读取请求，不需要二次调用
            is_pure_read = any(kw in user_message for kw in self.READ_KEYWORDS)
            is_write_intent = any(kw in user_message for kw in self.WRITE_KEYWORDS)

            # 如果只是读取请求且没有写作意图，不触发二次调用
            if is_pure_read and not is_write_intent:
                return False

            # 6. 如果有 chapter_id 且有内容，可能需要二次调用来执行编辑
            if has_chapter_id and has_content:
                logger.info(f"[SecondaryToolHandler] 📋 检测到获取类工具结果，可能需要二次编辑调用")
                return True

            return False

        except (json.JSONDecodeError, TypeError, AttributeError) as e:
            logger.debug(f"[SecondaryToolHandler] 工具结果解析失败: {e}")
            return False

    def extract_chapter_id_from_tool_result(self, tool_result: str) -> Optional[str]:
        """从工具返回结果中提取 chapter_id

        Args:
            tool_result: 工具返回的 JSON 字符串

        Returns:
            chapter_id 或 None
        """
        try:
            tool_data = json.loads(tool_result)
            chapter_id = (
                tool_data.get("chapter_id") or
                (tool_data.get("current_chapter") or {}).get("id") or
                (tool_data.get("chapter") or {}).get("id")
            )
            return chapter_id
        except (json.JSONDecodeError, TypeError, AttributeError):
            return None

    async def handle_secondary_tool_call(
        self,
        user_message: str,
        tool_result: str,
        chapter_id: str,
        system_prompt: str,
        state: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """处理二次工具调用

        Args:
            user_message: 用户原始消息
            tool_result: 第一次工具调用结果
            chapter_id: 提取到的章节ID
            system_prompt: 系统提示词
            state: Agent 状态

        Returns:
            二次工具调用结果，或 None（如果不需要/失败）
        """
        logger.info(f"[SecondaryToolHandler] ✅ 提取到chapter_id: {chapter_id[:20]}...")

        # 构建二次工具决策 prompt
        second_decision_prompt = self._build_decision_prompt(user_message, chapter_id)

        # 调用 AI 做二次工具决策
        second_result = await self._generate_text(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": second_decision_prompt}
            ],
            max_tokens=200,
            temperature=0.3,
            task_type=TaskType.SIMPLE_QA
        )
        second_decision_text = second_result.get("text", "")
        logger.info(f"[SecondaryToolHandler] 🔄 二次工具决策原文: {second_decision_text}")

        # 解析决策
        second_decision = self._parse_decision(second_decision_text)

        # 如果需要调用第二个工具
        if second_decision and second_decision.get("need_tools", False):
            tool_name = second_decision.get("tool_name", "")
            tool_args = second_decision.get("tool_args", {})

            logger.info(f"[SecondaryToolHandler] 🚀 准备二次工具调用: {tool_name}, args={tool_args}")

            # 执行二次工具调用
            second_tool_result = await self._execute_secondary_tool(
                tool_name=tool_name,
                tool_args=tool_args,
                state=state
            )

            if second_tool_result:
                return {
                    "tool_name": tool_name,
                    "tool_result": second_tool_result
                }

        return None

    def _build_decision_prompt(self, user_message: str, chapter_id: str) -> str:
        """构建二次工具决策 Prompt

        Args:
            user_message: 用户消息
            chapter_id: 章节ID

        Returns:
            决策 Prompt
        """
        return f"""用户原始请求：{user_message}

第一次工具调用已获取章节信息，chapter_id: {chapter_id}

现在判断是否需要第二次工具调用来完成用户的实际编辑需求。

可用的编辑器工具：
- smart_rewrite: 改写/修改章节内容 (参数: chapter_id, text_to_rewrite, user_requirement)
- smart_continue: 生成续写内容 (参数: chapter_id, chapter_content, user_requirement, word_count)
- smart_insert: 生成插入内容 (参数: chapter_id, user_intent, chapter_content, insert_context, word_count)

⚠️ 重要规则：
1. 用户说"修改"、"改写"、"重写"、"润色" → 使用 smart_rewrite
2. 用户说"续写"、"继续写" → 使用 smart_continue
3. 用户说"插入" → 使用 smart_insert
4. 必须严格返回JSON格式！

返回JSON:
{{"need_tools": true, "tool_name": "工具名", "tool_args": {{"chapter_id": "{chapter_id}", "instructions": "根据用户要求..."}}}}

或者如果不需要工具：
{{"need_tools": false, "direct_response": "..."}}

请返回JSON:"""

    def _parse_decision(self, decision_text: str) -> Optional[Dict[str, Any]]:
        """解析二次决策 JSON

        Args:
            decision_text: AI 返回的决策文本

        Returns:
            解析后的决策字典，或 None
        """
        # 方法1：直接解析
        try:
            return json.loads(decision_text.strip())
        except json.JSONDecodeError:
            pass

        # 方法2：正则提取
        json_matches = re.finditer(r'\{(?:[^{}]|(?:\{[^}]*\}))*\}', decision_text)
        for match in json_matches:
            try:
                candidate = json.loads(match.group())
                if "need_tools" in candidate:
                    return candidate
            except json.JSONDecodeError:
                continue

        return None

    async def _execute_secondary_tool(
        self,
        tool_name: str,
        tool_args: Dict[str, Any],
        state: Dict[str, Any]
    ) -> Optional[str]:
        """执行二次工具调用

        Args:
            tool_name: 工具名称
            tool_args: 工具参数
            state: Agent 状态

        Returns:
            工具执行结果，或 None
        """
        try:
            if tool_name == "smart_rewrite":
                return await self._call_smart_rewrite(tool_args, state)
            elif tool_name == "smart_continue":
                return await self._call_smart_continue(tool_args, state)
            elif tool_name == "smart_insert":
                return await self._call_smart_insert(tool_args, state)
            elif tool_name == "apply_chapter_edit":
                return await self._call_apply_chapter_edit(tool_args, state)
            else:
                logger.warning(f"[SecondaryToolHandler] 未知的二次工具调用: {tool_name}")
                return None
        except Exception as e:
            logger.error(f"[SecondaryToolHandler] 二次工具调用失败: {e}", exc_info=True)
            return None

    async def _call_smart_rewrite(
        self,
        tool_args: Dict[str, Any],
        state: Dict[str, Any]
    ) -> str:
        """调用 smart_rewrite 工具"""
        context = state.get("context", {}) if isinstance(state.get("context"), dict) else {}
        selected_text = context.get("selected_text", "")
        locate_original_text = context.get("locate_original_text", "")
        text_to_rewrite = tool_args.get("text_to_rewrite", "")
        if selected_text:
            text_to_rewrite = selected_text
        elif locate_original_text and not text_to_rewrite:
            text_to_rewrite = locate_original_text

        logger.info(f"[SecondaryToolHandler] 🚀 调用 smart_rewrite, chapter_id={tool_args.get('chapter_id')}")

        try:
            result = await registry.call_tool("smart_rewrite", {
                "chapter_id": tool_args.get("chapter_id") or state.get("chapter_id") or "",
                "text_to_rewrite": text_to_rewrite,
                "chapter_content": None,
                "user_requirement": tool_args.get("user_requirement", ""),
                "user_id": state.get("user_id")
            })
            if isinstance(result, dict) and result.get("success"):
                return json.dumps(result.get("data", {}), ensure_ascii=False)
            return json.dumps(result, ensure_ascii=False)
        except Exception as e:
            logger.warning(f"[SecondaryToolHandler] smart_rewrite 失败，降级: {e}")
            return await smart_rewrite.ainvoke({
                "chapter_id": tool_args.get("chapter_id") or state.get("chapter_id") or "",
                "text_to_rewrite": text_to_rewrite,
                "chapter_content": None,
                "user_requirement": tool_args.get("user_requirement", ""),
                "user_id": state.get("user_id")
            })

    async def _call_smart_continue(
        self,
        tool_args: Dict[str, Any],
        state: Dict[str, Any]
    ) -> str:
        """调用 smart_continue 工具"""
        logger.info(f"[SecondaryToolHandler] 🚀 调用 smart_continue, chapter_id={tool_args.get('chapter_id')}")

        try:
            # 🔧 2026-01-09: 更新参数以匹配新的 smart_continue 签名
            result = await registry.call_tool("smart_continue", {
                "chapter_id": tool_args.get("chapter_id") or state.get("chapter_id") or "",
                "chapter_content": tool_args.get("chapter_content"),
                "user_requirement": tool_args.get("user_requirement", ""),
                "word_count": tool_args.get("word_count", 500),
                "user_id": state.get("user_id")
            })
            if isinstance(result, dict) and result.get("success"):
                return json.dumps(result.get("data", {}), ensure_ascii=False)
            return json.dumps(result, ensure_ascii=False)
        except Exception as e:
            logger.warning(f"[SecondaryToolHandler] smart_continue 失败，降级: {e}")
            return await smart_continue.ainvoke({
                "chapter_id": tool_args.get("chapter_id") or state.get("chapter_id") or "",
                "chapter_content": tool_args.get("chapter_content"),
                "user_requirement": tool_args.get("user_requirement", ""),
                "word_count": tool_args.get("word_count", 500),
                "user_id": state.get("user_id")
            })

    async def _call_smart_insert(
        self,
        tool_args: Dict[str, Any],
        state: Dict[str, Any]
    ) -> str:
        """调用 smart_insert 工具"""
        logger.info(f"[SecondaryToolHandler] 🚀 调用 smart_insert, chapter_id={tool_args.get('chapter_id')}")

        try:
            # 🔧 2026-01-09: 更新参数以匹配新的 smart_insert 签名
            result = await registry.call_tool("smart_insert", {
                "chapter_id": tool_args.get("chapter_id") or state.get("chapter_id") or "",
                "user_intent": tool_args.get("user_intent") or tool_args.get("position", "插入内容"),
                "chapter_content": tool_args.get("chapter_content"),
                "insert_context": tool_args.get("insert_context"),
                "word_count": tool_args.get("word_count", 200),
                "user_id": state.get("user_id")
            })
            if isinstance(result, dict) and result.get("success"):
                return json.dumps(result.get("data", {}), ensure_ascii=False)
            return json.dumps(result, ensure_ascii=False)
        except Exception as e:
            logger.warning(f"[SecondaryToolHandler] smart_insert 失败，降级: {e}")
            return await smart_insert.ainvoke({
                "chapter_id": tool_args.get("chapter_id") or state.get("chapter_id") or "",
                "user_intent": tool_args.get("user_intent") or tool_args.get("position", "插入内容"),
                "chapter_content": tool_args.get("chapter_content"),
                "insert_context": tool_args.get("insert_context"),
                "word_count": tool_args.get("word_count", 200),
                "user_id": state.get("user_id")
            })

    async def _call_apply_chapter_edit(
        self,
        tool_args: Dict[str, Any],
        state: Dict[str, Any]
    ) -> str:
        """调用 apply_chapter_edit 工具"""
        logger.info(f"[SecondaryToolHandler] 🚀 调用 apply_chapter_edit, chapter_id={tool_args.get('chapter_id')}")
        context = state.get("context", {}) if isinstance(state.get("context"), dict) else {}
        node_id = tool_args.get("node_id") or context.get("locate_node_id")
        paragraph_index = tool_args.get("paragraph_index") or context.get("locate_paragraph_index")
        before_anchor = tool_args.get("before_anchor") or context.get("locate_before_anchor")
        after_anchor = tool_args.get("after_anchor") or context.get("locate_after_anchor")
        original_text = tool_args.get("original_text") or context.get("locate_original_text")

        try:
            result = await registry.call_tool("apply_chapter_edit", {
                "chapter_id": tool_args.get("chapter_id") or state.get("chapter_id") or "",
                "content": tool_args.get("content", ""),
                "operation": tool_args.get("operation", "replace"),
                "position": None,
                "before_anchor": before_anchor,
                "after_anchor": after_anchor,
                "original_text": original_text,
                "node_id": node_id,
                "paragraph_index": paragraph_index,
                "user_id": state.get("user_id"),
                "description": None,
                "conversation_id": tool_args.get("conversation_id") or state.get("conversation_id"),
                "work_id": tool_args.get("work_id") or state.get("work_id")
            })
            if isinstance(result, dict) and result.get("success"):
                return json.dumps(result.get("data", {}), ensure_ascii=False)
            return json.dumps(result, ensure_ascii=False)
        except Exception as e:
            logger.warning(f"[SecondaryToolHandler] apply_chapter_edit 失败，降级: {e}")
            return await apply_chapter_edit.ainvoke({
                "chapter_id": tool_args.get("chapter_id") or state.get("chapter_id") or "",
                "content": tool_args.get("content", ""),
                "operation": tool_args.get("operation", "replace"),
                "position": None,
                "before_anchor": before_anchor,
                "after_anchor": after_anchor,
                "original_text": original_text,
                "node_id": node_id,
                "paragraph_index": paragraph_index,
                "user_id": state.get("user_id"),
                "description": None,
                "conversation_id": tool_args.get("conversation_id") or state.get("conversation_id"),
                "work_id": tool_args.get("work_id") or state.get("work_id")
            })

    def build_task_instruction(
        self,
        user_message: str,
        tool_result: str,
        agent_type: str
    ) -> str:
        """构建任务指令

        根据 agent_type 和用户意图构建不同的任务指令

        Args:
            user_message: 用户消息
            tool_result: 工具返回结果
            agent_type: Agent 类型

        Returns:
            任务指令字符串
        """
        is_read_request = any(kw in user_message for kw in self.READ_KEYWORDS)
        is_write_request = any(kw in user_message for kw in self.WRITE_KEYWORDS)

        if agent_type == "writing":
            if is_read_request and not is_write_request:
                return self._build_reading_instruction(user_message, tool_result)
            else:
                return self._build_writing_instruction(user_message, tool_result)
        elif agent_type == "stuck":
            return self._build_stuck_instruction(user_message, tool_result)
        elif agent_type == "planning":
            return self._build_planning_instruction(user_message, tool_result)
        else:  # analysis 或其他
            if is_read_request and not is_write_request:
                return self._build_analysis_read_instruction(user_message, tool_result)
            else:
                return self._build_analysis_instruction(user_message, tool_result)

    def _build_reading_instruction(self, user_message: str, tool_result: str) -> str:
        """构建读取型任务指令"""
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

    def _build_writing_instruction(self, user_message: str, tool_result: str) -> str:
        """构建写作型任务指令"""
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

    def _build_stuck_instruction(self, user_message: str, tool_result: str) -> str:
        """构建卡文场景任务指令"""
        return f"""用户遇到的问题：{user_message}

当前创作背景：
{tool_result}

请基于背景信息，给用户3-5个具体的创作方向建议，每个建议包含：
1. 方向概述
2. 可以这样写的理由
3. 示例开头（50字左右）"""

    def _build_planning_instruction(self, user_message: str, tool_result: str) -> str:
        """构建规划场景任务指令"""
        return f"""用户需求：{user_message}

当前信息：
{tool_result}

请基于现有信息，提供详细的规划方案。"""

    def _build_analysis_read_instruction(self, user_message: str, tool_result: str) -> str:
        """构建分析场景读取型任务指令"""
        return f"""用户请求：{user_message}

工具返回的数据：
{tool_result}

请注意：用户想要「查看/读取」内容！
请直接整理并呈现工具返回的数据内容，用清晰易读的格式展示给用户。"""

    def _build_analysis_instruction(self, user_message: str, tool_result: str) -> str:
        """构建分析场景任务指令"""
        return f"""用户请求：{user_message}

分析材料：
{tool_result}

请基于材料，生成详细的分析报告。"""

    def get_user_intent(self, user_message: str) -> Tuple[bool, bool]:
        """获取用户意图

        Args:
            user_message: 用户消息

        Returns:
            (is_read_request, is_write_request)
        """
        is_read_request = any(kw in user_message for kw in self.READ_KEYWORDS)
        is_write_request = any(kw in user_message for kw in self.WRITE_KEYWORDS)
        return is_read_request, is_write_request
