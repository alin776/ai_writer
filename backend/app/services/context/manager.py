"""
上下文管理 - 核心管理器

为chat_stream()提供上下文管理能力：
- 构建上下文：从存储加载并格式化为LLM消息
- 更新上下文：保存新的对话轮次
- 压缩上下文：当Token超限时自动压缩
"""

import time
import logging
from typing import List, Optional, Dict, Any

from app.services.context.models import (
    Context, Message, ShortMemory, SummaryMemory, TokenBudget
)
from app.services.context.store import ContextStore, RedisContextStore
from app.services.context.monitoring_integration import (
    monitor_context_build,
    monitor_context_update,
    monitor_summary_generation,
    record_compression_metrics,
    record_memory_size
)

logger = logging.getLogger(__name__)


class ContextManager:
    """上下文管理器 - 专为chat_stream优化"""

    def __init__(
        self,
        store: Optional[ContextStore] = None,
        token_budget: Optional[TokenBudget] = None,
        ai_service: Optional[Any] = None,  # ✅ AI服务（用于LLM摘要）
        enable_long_term_memory: bool = False,  # ✅ 启用长期记忆
        user_id: Optional[str] = None,  # ✅ 用户ID（用于长期记忆隔离）
        enable_adaptive_budget: bool = False,  # ✅ 新增：启用自适应预算
        adaptive_budget: Optional[Any] = None  # ✅ 新增：自适应预算实例
    ):
        self.store = store or RedisContextStore()
        self.token_budget = token_budget or TokenBudget()
        self.ai_service = ai_service  # ✅ 保存AI服务引用
        self._summary_service = None  # ✅ 懒加载摘要服务

        # ✅ 初始化长期记忆
        self.enable_long_term_memory = enable_long_term_memory
        self.user_id = user_id
        self._vector_store = None  # 懒加载向量存储

        if enable_long_term_memory:
            self._init_vector_store()
            logger.info(f"✅ ContextManager: 长期记忆已启用 (user_id={user_id})")

        # ✅ 初始化自适应预算
        self.enable_adaptive_budget = enable_adaptive_budget
        if enable_adaptive_budget:
            if adaptive_budget:
                self.adaptive_budget = adaptive_budget
            else:
                from app.services.context.adaptive_budget import get_adaptive_budget
                self.adaptive_budget = get_adaptive_budget(total=self.token_budget.total)
            logger.info(f"✅ ContextManager: 自适应预算已启用")

    @monitor_context_build
    async def build_context(
        self,
        session_id: str,
        system_prompt: str = "",
        query: Optional[str] = None,  # ✅ 用于长期记忆检索的查询
        task_type: Optional[Any] = None,  # ✅ 新增：任务类型（用于自适应预算）
        work_id: Optional[str] = None  # ✅ 新增：作品ID（用于向量记忆隔离）
    ) -> Dict[str, Any]:
        """
        构建上下文 - 用于chat_stream方法

        Args:
            session_id: 会话ID
            system_prompt: 系统提示
            query: 查询文本（用于长期记忆检索，可选）
            task_type: 任务类型（用于自适应预算，可选）
                      可选值：TaskType.CREATIVE, TaskType.ANALYTICAL, TaskType.QA, TaskType.CHAT
            work_id: 作品ID（可选，用于隔离不同作品的向量记忆）

        Returns:
            Dict包含:
            - messages: List[Dict] - 格式化的LLM消息列表
            - metadata: Dict - 元数据（token数、消息数等）
            - context: Context - 原始Context对象（供后续更新使用）
        """
        # ✅ 选择预算配置（自适应 vs 固定）
        if self.enable_adaptive_budget and task_type:
            # 使用自适应预算
            budget = self.adaptive_budget.to_token_budget(task_type)
            logger.debug(f"[ContextManager] 使用自适应预算: {task_type.value if hasattr(task_type, 'value') else task_type}")
        else:
            # 使用固定预算
            budget = self.token_budget

        # 加载或创建上下文
        context = await self.store.load(session_id)

        if not context:
            context = Context(
                session_id=session_id,
                system_prompt=system_prompt
            )
            logger.info(f"[ContextManager] 创建新上下文: {session_id}")

        # 检查Token使用情况
        total_tokens = context.get_total_tokens()
        max_tokens = budget.total

        logger.info(f"[ContextManager] Session {session_id}: {total_tokens}/{max_tokens} tokens")

        # ✅ P0-4修复：添加硬限制检查
        HARD_LIMIT_RATIO = 0.95  # 硬限制：95%
        if total_tokens > max_tokens * HARD_LIMIT_RATIO:
            logger.error(
                f"[ContextManager] ❌ Token超过硬限制({total_tokens}/{max_tokens})，"
                f"强制截断到{int(max_tokens * 0.7)}tokens"
            )
            # 强制截断：只保留最近的消息，确保不超过70%预算
            context = await self._force_truncate_context(context, int(max_tokens * 0.7))
            total_tokens = context.get_total_tokens()

        # 如果超过80%预算，触发压缩
        if total_tokens > max_tokens * 0.8:
            logger.warning(f"[ContextManager] Token使用率过高 ({total_tokens}/{max_tokens}), 触发压缩")
            await self.compress_context(context)

        # ✅ 检索长期记忆（如果启用）
        long_term_memories = []
        if self.enable_long_term_memory and query and self._vector_store and self.user_id:
            # ✅ 修改：传递work_id进行记忆隔离
            long_term_memories = await self._retrieve_long_term_memories(
                query,
                work_id=work_id  # ✅ 新增：传递work_id
            )

        # 构建LLM消息列表
        messages = self._build_messages(context, long_term_memories)

        return {
            "messages": messages,
            "metadata": {
                "session_id": session_id,
                "token_count": context.get_total_tokens(),
                "short_memory_size": len(context.short_memory.messages),
                "has_summary": bool(context.summary_memory.summary),
                "compression_triggered": total_tokens > max_tokens * 0.8,
                "long_term_memories": len(long_term_memories),  # ✅ 长期记忆数量
                "adaptive_budget_enabled": self.enable_adaptive_budget,  # ✅ 新增：是否启用自适应预算
                "task_type": task_type.value if (task_type and hasattr(task_type, 'value')) else None  # ✅ 新增：任务类型
            },
            "context": context  # 返回context对象供后续更新
        }

    def _build_messages(
        self,
        context: Context,
        long_term_memories: List[Dict] = None  # ✅ 新增：长期记忆
    ) -> List[Dict]:
        """
        构建LLM消息列表

        按照Token预算分配：
        1. 系统提示 (20%)
        2. 长期记忆 (15%) - ✅ 新增
        3. 摘要上下文 (25%)
        4. 近期对话 (35%)
        """
        messages = []

        # 1. 系统提示词 (20%)
        if context.system_prompt:
            messages.append({
                "role": "system",
                "content": context.system_prompt
            })

        # 2. 长期记忆 (15%) - ✅ 新增
        if long_term_memories:
            ltm_content = self._format_long_term_memories(long_term_memories)
            messages.append({
                "role": "system",
                "content": ltm_content
            })

        # 3. 摘要上下文 (25%)
        if context.summary_memory.summary:
            summary_content = f"对话摘要：\n{context.summary_memory.summary}"

            # 添加重要事实
            if context.summary_memory.important_facts:
                facts = "\n".join(f"- {fact}" for fact in context.summary_memory.important_facts)
                summary_content += f"\n\n重要信息：\n{facts}"

            messages.append({
                "role": "system",
                "content": summary_content
            })

        # 4. 近期对话 (35%)
        for msg in context.short_memory.messages:
            messages.append({
                "role": msg.role,
                "content": msg.content
            })

        return messages

    @monitor_context_update
    async def update_context(
        self,
        session_id: str,
        new_messages: List[Dict],
        context: Optional[Context] = None,
        work_id: Optional[str] = None  # ✅ 新增：作品ID（用于向量记忆隔离）
    ):
        """
        更新上下文 - chat_stream完成后调用

        Args:
            session_id: 会话ID
            new_messages: 新消息列表 [{"role": "user", "content": "..."}, ...]
            context: 现有上下文（如果有）
            work_id: 作品ID（可选，用于向量记忆隔离）
        """
        if not context:
            context = await self.store.load(session_id)
            if not context:
                context = Context(session_id=session_id)

        # 添加新消息到短期记忆
        for msg_dict in new_messages:
            message = Message(
                role=msg_dict["role"],
                content=msg_dict["content"],
                timestamp=time.time(),
                metadata=msg_dict.get("metadata", {})
            )
            context.short_memory.add_message(message)

            # ✅ 自动保存到长期记忆
            if self.enable_long_term_memory:
                await self._save_to_long_term_memory(
                    content=message.content,
                    session_id=session_id,
                    role=message.role,
                    work_id=work_id  # ✅ 新增：传递work_id
                )

        # 保存更新后的上下文
        await self.store.save(context)

        logger.info(
            f"[ContextManager] 更新上下文: {session_id}, "
            f"消息数={len(context.short_memory.messages)}, "
            f"Token={context.get_total_tokens()}"
        )


    async def compress_context(self, context: Context):
        """
        压缩上下文 - 当Token超限时调用

        策略：
        1. 保留最近2轮对话（4条消息）
        2. 将旧消息生成摘要
        3. 提取重要事实
        """
        logger.info(f"[ContextManager] 开始压缩: {context.session_id}")

        # ✅ 记录压缩前的Token数（用于监控）
        original_tokens = context.get_total_tokens()

        # 获取需要摘要的消息（保留最近2轮）
        messages_to_summarize = context.short_memory.messages[:-4] if len(context.short_memory.messages) > 4 else []

        if not messages_to_summarize:
            logger.info(f"[ContextManager] 消息数不足，无需压缩")
            return

        # 生成摘要
        new_summary = await self._generate_summary(messages_to_summarize)

        # 合并到现有摘要
        if context.summary_memory.summary:
            context.summary_memory.summary = f"{context.summary_memory.summary}\n\n---\n\n{new_summary}"
        else:
            context.summary_memory.summary = new_summary

        context.summary_memory.last_updated = time.time()

        # 清理已摘要的消息，只保留最近4条
        context.short_memory.messages = context.short_memory.messages[-4:] if len(context.short_memory.messages) > 4 else context.short_memory.messages

        # ✅ 记录压缩后的Token数和内存使用（用于监控）
        compressed_tokens = context.get_total_tokens()
        record_compression_metrics(original_tokens, compressed_tokens, context.session_id)
        record_memory_size(
            len(context.short_memory.messages),
            len(context.summary_memory.summary),
            context.session_id
        )

        logger.info(
            f"[ContextManager] 压缩完成: {context.session_id}, "
            f"保留{len(context.short_memory.messages)}条消息, "
            f"摘要长度={len(context.summary_memory.summary)}"
        )

    @monitor_summary_generation
    async def _generate_summary(self, messages: List[Message]) -> str:
        """
        生成对话摘要（LLM驱动）

        策略：
        1. 如果有AI服务，使用LLM生成高质量摘要
        2. 如果没有AI服务，使用降级策略（简单提取）
        """
        if not messages:
            return ""

        # ✅ 如果没有AI服务，使用降级策略
        if self.ai_service is None:
            logger.info("[ContextManager] AI服务未配置，使用简单摘要策略")
            return self._fallback_summary(messages)

        try:
            # ✅ 懒加载摘要服务
            if self._summary_service is None:
                from app.services.context.summary_service import SummaryService
                self._summary_service = SummaryService(self.ai_service)
                logger.info("[ContextManager] ✅ SummaryService已初始化")

            # ✅ 调用LLM生成摘要
            summary = await self._summary_service.summarize_conversation(
                messages,
                max_length=200
            )
            return summary

        except Exception as e:
            logger.error(f"[ContextManager] ❌ LLM摘要失败: {e}，使用降级策略")
            return self._fallback_summary(messages)

    def _fallback_summary(self, messages: List[Message]) -> str:
        """
        降级策略：简单提取式摘要（当LLM不可用时）

        策略与SummaryService._fallback_summary相同
        """
        if not messages:
            return ""

        # 简单策略：提取用户请求和助手回复的关键信息
        summary_parts = []

        user_messages = [m for m in messages if m.role == "user"]
        assistant_messages = [m for m in messages if m.role == "assistant"]

        if user_messages:
            first_user = user_messages[0].content[:100]
            summary_parts.append(f"用户请求: {first_user}...")

        if assistant_messages:
            first_assistant = assistant_messages[0].content[:100]
            summary_parts.append(f"助手回复: {first_assistant}...")

        # 统计信息
        summary_parts.append(f"共{len(messages)}条消息")

        return " | ".join(summary_parts)

    def _estimate_tokens(self, text: str) -> int:
        """
        更准确的Token估算（考虑中英混合）

        Args:
            text: 文本内容

        Returns:
            估算的Token数
        """
        # 中文字数（CJK字符：1字≈1.5 tokens）
        cn_count = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
        # 移除中文后，计算英文单词（1词≈0.3 tokens）
        text_without_cn = ''.join(c for c in text if not ('\u4e00' <= c <= '\u9fff'))
        en_count = len(text_without_cn.split())
        # 其他字符（标点、数字等，1字≈0.2 tokens）
        other_count = len(text) - cn_count - len(text_without_cn.replace(' ', ''))
        return int(cn_count * 1.5 + en_count * 0.3 + other_count * 0.2)

    def _calculate_message_importance(self, msg: Message, position: int, total: int) -> float:
        """
        计算消息的综合重要度（✅ P0-7：智能截断核心）

        综合考虑:
        1. 内容重要度（关键词、角色信息、设定等）
        2. 时间位置（近期消息权重更高）
        3. 角色权重（用户消息 > 助手消息）
        4. 消息长度（长消息可能包含更多信息）

        Args:
            msg: 消息对象
            position: 消息在列表中的位置（0为最旧）
            total: 消息总数

        Returns:
            综合重要度分数 (0.0 - 1.0)
        """
        content = msg.content
        content_lower = content.lower()

        # === 1. 内容重要度 (0.0 - 0.5) ===
        content_score = 0.0

        # 核心设定关键词（最高权重）
        critical_keywords = [
            "大纲", "设定", "角色", "世界观", "背景", "人物", "主角", "配角",
            "plot", "character", "setting", "worldview", "protagonist"
        ]
        if any(kw in content_lower for kw in critical_keywords):
            content_score = max(content_score, 0.5)

        # 重要指令关键词（中高权重）
        important_keywords = [
            "要求", "必须", "不要", "风格", "注意", "关键", "重点",
            "修改", "添加", "删除", "调整", "remember", "important"
        ]
        if any(kw in content_lower for kw in important_keywords):
            content_score = max(content_score, 0.35)

        # 写作相关关键词（中等权重）
        writing_keywords = [
            "续写", "扩写", "润色", "改写", "章节", "段落", "对话",
            "描写", "叙述", "情节", "冲突", "结局"
        ]
        if any(kw in content_lower for kw in writing_keywords):
            content_score = max(content_score, 0.25)

        # === 2. 时间位置分数 (0.0 - 0.25) ===
        # 最近的消息权重更高，使用平方根函数使衰减更平缓
        if total > 1:
            recency = position / (total - 1)  # 0.0（最旧）到 1.0（最新）
            position_score = 0.25 * (recency ** 0.5)  # 平方根使衰减更平缓
        else:
            position_score = 0.25

        # === 3. 角色权重 (0.0 - 0.15) ===
        role_score = 0.15 if msg.role == "user" else 0.08

        # === 4. 消息长度分数 (0.0 - 0.10) ===
        length = len(content)
        if length > 1000:
            length_score = 0.10
        elif length > 500:
            length_score = 0.07
        elif length > 200:
            length_score = 0.04
        else:
            length_score = 0.02

        # 综合得分
        total_score = content_score + position_score + role_score + length_score
        return min(total_score, 1.0)

    async def _force_truncate_context(self, context: Context, target_tokens: int) -> Context:
        """
        智能截断上下文到目标Token数（✅ P0-7修复：智能截断替代强制截断）

        改进策略：
        1. 计算每条消息的综合重要度（内容+时间+角色+长度）
        2. 优先保留重要消息，而非简单的时间顺序
        3. 为被截断的消息生成简短摘要，保持上下文连贯性
        4. 确保最近2条消息始终保留（上下文连贯性）

        Args:
            context: 当前上下文
            target_tokens: 目标Token数

        Returns:
            截断后的上下文
        """
        logger.warning(
            f"[ContextManager] 🧠 智能截断上下文: {context.get_total_tokens()} -> {target_tokens} tokens"
        )

        messages = context.short_memory.messages
        if not messages:
            return context

        total_messages = len(messages)

        # === Step 1: 计算每条消息的重要度和Token数 ===
        message_scores = []
        for i, msg in enumerate(messages):
            importance = self._calculate_message_importance(msg, i, total_messages)
            tokens = self._estimate_tokens(msg.content)
            message_scores.append({
                "index": i,
                "message": msg,
                "importance": importance,
                "tokens": tokens
            })

        # === Step 2: 确保最近2条消息始终保留（上下文连贯性） ===
        must_keep_count = min(2, total_messages)
        must_keep_indices = set(range(total_messages - must_keep_count, total_messages))

        # 计算必须保留消息的Token数
        must_keep_tokens = sum(
            ms["tokens"] for ms in message_scores
            if ms["index"] in must_keep_indices
        )

        # 可用于其他消息的Token预算
        remaining_budget = target_tokens - must_keep_tokens

        if remaining_budget <= 0:
            # Token预算极少，只保留最后1-2条消息
            logger.warning("[ContextManager] Token预算极少，仅保留最近消息")
            context.short_memory.messages = [ms["message"] for ms in message_scores if ms["index"] in must_keep_indices]
            return context

        # === Step 3: 按重要度排序非必须保留的消息 ===
        optional_messages = [
            ms for ms in message_scores
            if ms["index"] not in must_keep_indices
        ]
        optional_messages.sort(key=lambda x: x["importance"], reverse=True)

        # === Step 4: 贪心选择重要消息直到Token预算用尽 ===
        selected_indices = set(must_keep_indices)
        current_tokens = must_keep_tokens
        truncated_messages = []

        for ms in optional_messages:
            if current_tokens + ms["tokens"] <= remaining_budget + must_keep_tokens:
                selected_indices.add(ms["index"])
                current_tokens += ms["tokens"]
            else:
                # 记录被截断的消息（用于生成摘要）
                truncated_messages.append(ms)

        # === Step 5: 按原始顺序排列保留的消息 ===
        kept_messages = [
            ms["message"] for ms in message_scores
            if ms["index"] in selected_indices
        ]
        # 按原始索引排序
        kept_indices_sorted = sorted(selected_indices)
        kept_messages = [message_scores[i]["message"] for i in kept_indices_sorted]

        # === Step 6: 为截断的消息生成简短摘要（保持连贯性）===
        if truncated_messages:
            truncated_summary = self._generate_truncation_summary(truncated_messages)
            if truncated_summary and context.summary_memory:
                # 追加到现有摘要
                if context.summary_memory.summary:
                    context.summary_memory.summary += f"\n\n[智能截断摘要]\n{truncated_summary}"
                else:
                    context.summary_memory.summary = f"[智能截断摘要]\n{truncated_summary}"
                logger.info(f"[ContextManager] 📝 生成截断摘要: {len(truncated_summary)}字符")

        logger.warning(
            f"[ContextManager] 🧠 智能截断完成: 保留{len(kept_messages)}/{total_messages}条消息, "
            f"截断{len(truncated_messages)}条, Token: {context.get_total_tokens()} -> ~{current_tokens}"
        )

        # 记录保留消息的重要度分布
        if kept_messages:
            kept_scores = [ms["importance"] for ms in message_scores if ms["index"] in selected_indices]
            avg_importance = sum(kept_scores) / len(kept_scores)
            logger.info(f"[ContextManager] 📊 保留消息平均重要度: {avg_importance:.3f}")

        context.short_memory.messages = kept_messages
        return context

    def _generate_truncation_summary(self, truncated_messages: list) -> str:
        """
        为被截断的消息生成简短摘要（✅ P0-7：保持上下文连贯性）

        Args:
            truncated_messages: 被截断的消息列表 [{"message": Message, "importance": float, ...}]

        Returns:
            简短摘要文本
        """
        if not truncated_messages:
            return ""

        summary_parts = []

        # 统计被截断消息的信息
        user_msgs = [m for m in truncated_messages if m["message"].role == "user"]
        assistant_msgs = [m for m in truncated_messages if m["message"].role == "assistant"]

        # 提取用户请求的关键信息
        if user_msgs:
            # 按重要度排序，取最重要的2条
            user_msgs.sort(key=lambda x: x["importance"], reverse=True)
            for um in user_msgs[:2]:
                content = um["message"].content
                # 提取前80字符作为摘要
                if len(content) > 80:
                    content = content[:80] + "..."
                summary_parts.append(f"用户曾请求: {content}")

        # 提取助手回复的关键信息
        if assistant_msgs:
            assistant_msgs.sort(key=lambda x: x["importance"], reverse=True)
            for am in assistant_msgs[:2]:
                content = am["message"].content
                if len(content) > 80:
                    content = content[:80] + "..."
                summary_parts.append(f"助手曾回复: {content}")

        # 添加统计信息
        summary_parts.append(f"(共截断{len(truncated_messages)}条历史消息)")

        return " | ".join(summary_parts)

    async def clear_context(self, session_id: str):
        """清除上下文 - 用于重置会话"""
        await self.store.delete(session_id)
        logger.info(f"[ContextManager] 清除上下文: {session_id}")

    def set_ai_service(self, ai_service: Any):
        """
        设置AI服务（向后兼容）

        用于在创建ContextManager后注入AI服务

        Args:
            ai_service: HTTPAIService实例
        """
        self.ai_service = ai_service
        self._summary_service = None  # 重置摘要服务，下次使用时重新初始化
        logger.info("[ContextManager] ✅ AI服务已设置")

    def _init_vector_store(self):
        """初始化向量存储（懒加载）"""
        try:
            from app.services.context.vector_memory_store import get_vector_memory_store
            self._vector_store = get_vector_memory_store()
            logger.info("✅ VectorMemoryStore 已初始化")
        except Exception as e:
            logger.error(f"❌ VectorMemoryStore 初始化失败: {e}")
            self.enable_long_term_memory = False

    def _evaluate_importance(self, content: str, role: str) -> float:
        """
        评估记忆重要度（0.0-1.0）

        规则：
        - 用户消息优先级高于助手消息
        - 包含"大纲"、"设定"、"角色"等关键词 → 0.9+
        - 包含"修改"、"要求"、"添加" → 0.7+
        - 长内容（>500字符） → 0.6+
        - 普通对话 → 0.3-0.5
        """
        content_lower = content.lower()
        importance = 0.3  # 基础分数

        # 用户消息权重更高
        if role == "user":
            importance += 0.1

        # 核心设定关键词
        high_value_keywords = ["大纲", "设定", "角色", "世界观", "背景", "人物", "plot", "character"]
        if any(kw in content_lower for kw in high_value_keywords):
            importance = max(importance, 0.9)

        # 重要指令关键词
        medium_value_keywords = ["修改", "要求", "添加", "删除", "更新", "调整"]
        if any(kw in content_lower for kw in medium_value_keywords):
            importance = max(importance, 0.7)

        # 长内容
        if len(content) > 500:
            importance = max(importance, 0.6)
        elif len(content) > 200:
            importance = max(importance, 0.5)

        return min(importance, 1.0)  # 确保不超过1.0

    async def _save_to_long_term_memory(
        self,
        content: str,
        session_id: str,
        role: str,
        importance: Optional[float] = None,
        work_id: Optional[str] = None  # ✅ 新增：作品ID
    ):
        """
        保存到长期记忆

        Args:
            content: 记忆内容
            session_id: 会话ID
            role: 角色（user/assistant）
            importance: 重要度（如未指定则自动评估）
            work_id: 作品ID（可选，用于隔离不同作品的记忆）
        """
        if not self.enable_long_term_memory or not self._vector_store or not self.user_id:
            return

        try:
            # 评估重要度
            if importance is None:
                importance = self._evaluate_importance(content, role)

            # 只保存重要度 >= 0.5 的记忆
            if importance < 0.5:
                logger.debug(f"记忆重要度过低 ({importance:.2f})，跳过保存")
                return

            # 保存到向量库
            memory_id = await self._vector_store.add_memory(
                content=content,
                user_id=self.user_id,
                work_id=work_id,  # ✅ 新增：传递work_id
                session_id=session_id,
                memory_type="conversation",
                importance=importance
            )

            logger.info(
                f"✅ 保存长期记忆 | ID={memory_id[:20]}... | "
                f"work_id={work_id or 'NONE'} | "  # ✅ 新增：显示work_id
                f"重要度={importance:.2f} | 长度={len(content)}"
            )

        except Exception as e:
            logger.error(f"❌ 保存长期记忆失败: {e}")

    async def _retrieve_long_term_memories(
        self,
        query: str,
        work_id: Optional[str] = None,  # ✅ 新增：作品ID过滤
        top_k: int = 3,
        min_similarity: float = 0.3
    ) -> List[Dict]:
        """
        检索长期记忆

        Args:
            query: 查询文本
            work_id: 作品ID（可选，用于只检索特定作品的记忆）
            top_k: 返回Top K结果
            min_similarity: 最低相似度

        Returns:
            记忆列表
        """
        if not self._vector_store or not self.user_id:
            return []

        try:
            # ✅ 修改：传递work_id进行过滤
            memories = await self._vector_store.search_memories(
                query=query,
                user_id=self.user_id,
                work_id=work_id,  # ✅ 新增：传递work_id
                top_k=top_k,
                min_similarity=min_similarity
            )

            logger.info(
                f"🔍 检索长期记忆 | work_id={work_id or 'ALL'} | "  # ✅ 新增：显示work_id
                f"查询='{query[:30]}...' | 找到={len(memories)}条 | 阈值={min_similarity}"
            )

            return memories

        except Exception as e:
            logger.error(f"❌ 检索长期记忆失败: {e}")
            return []

    def _format_long_term_memories(self, memories: List[Dict]) -> str:
        """
        格式化长期记忆

        Args:
            memories: 记忆列表

        Returns:
            格式化后的文本
        """
        if not memories:
            return ""

        lines = ["相关历史记忆："]
        for i, mem in enumerate(memories, 1):
            content = mem["content"]
            similarity = mem.get("similarity", 0)
            importance = mem.get("metadata", {}).get("importance", 0)

            # 限制每条记忆的长度
            if len(content) > 200:
                content = content[:200] + "..."

            lines.append(
                f"{i}. {content} "
                f"(相关度: {similarity:.2f}, 重要度: {importance:.2f})"
            )

        return "\n".join(lines)
