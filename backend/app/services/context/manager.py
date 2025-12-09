"""
上下文管理 - 核心管理器

为chat_stream()提供上下文管理能力：
- 构建上下文：从存储加载并格式化为LLM消息
- 更新上下文：保存新的对话轮次
- 压缩上下文：当Token超限时自动压缩
"""

import time
import logging
import asyncio
from typing import List, Optional, Dict, Any

from app.services.context.models import (
    Context, Message, ShortMemory, SummaryMemory, TokenBudget,
    IsolationLevel, build_isolation_key  # ✅ 新增：隔离层级
)
from app.services.context.store import ContextStore, RedisContextStore
from app.services.context.monitoring_integration import (
    monitor_context_build,
    monitor_context_update,
    monitor_summary_generation,
    record_compression_metrics,
    record_memory_size,
    record_dedup,
    record_timeout_event
)
from app.services.context.context_config import ContextConfig

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
        # ✅ P1-7修复：自动检测任务类型（如果未指定且启用了自适应预算）
        if self.enable_adaptive_budget and not task_type and query:
            task_type = self._analyze_task_type(query)
            logger.debug(f"[ContextManager] 自动检测任务类型: {task_type.value if hasattr(task_type, 'value') else task_type}")

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

        # ✅ P0-4修复：添加硬限制检查（集中配置）
        if total_tokens > max_tokens * ContextConfig.HARD_LIMIT_RATIO:
            logger.error(
                f"[ContextManager] ❌ Token超过硬限制({total_tokens}/{max_tokens})，"
                f"强制截断到{int(max_tokens * ContextConfig.TRUNCATE_TARGET_RATIO)}tokens"
            )
            # 强制截断：只保留最近的消息，确保不超过70%预算
            context = await self._force_truncate_context(
                context,
                int(max_tokens * ContextConfig.TRUNCATE_TARGET_RATIO)
            )
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

        # ✅ P1-4修复：去重短期记忆
        if context.short_memory.messages:
            original_count = len(context.short_memory.messages)
            context.short_memory.messages = self._deduplicate_messages(
                context.short_memory.messages,
                threshold=None  # 自适应阈值
            )
            if len(context.short_memory.messages) < original_count:
                # 记录去重后的短期记忆大小（摘要长度保持不变）
                record_memory_size(
                    len(context.short_memory.messages),
                    len(context.summary_memory.summary),
                    session_id
                )
                record_dedup(original_count - len(context.short_memory.messages))

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
        1. 保留短期记忆窗口（与max_turns一致）
        2. 将更旧的消息生成摘要
        3. 提取重要事实
        """
        logger.info(f"[ContextManager] 开始压缩: {context.session_id}")

        # ✅ 记录压缩前的Token数（用于监控）
        original_tokens = context.get_total_tokens()

        # 获取需要摘要的消息（保留最近max_turns轮）
        keep_count = context.short_memory.max_turns * 2
        messages_to_summarize = context.short_memory.messages[:-keep_count] if len(context.short_memory.messages) > keep_count else []

        if not messages_to_summarize:
            logger.info(f"[ContextManager] 消息数不足，无需压缩")
            return

        # 生成摘要，添加超时保护
        try:
            new_summary = await asyncio.wait_for(
                self._generate_summary(messages_to_summarize),
                timeout=ContextConfig.SUMMARY_TIMEOUT
            )
        except asyncio.TimeoutError:
            logger.error("[ContextManager] 摘要生成超时，使用降级摘要")
            record_timeout_event("summary_generation_timeout")
            new_summary = self._fallback_summary(messages_to_summarize)

        # 合并到现有摘要
        if context.summary_memory.summary:
            context.summary_memory.summary = f"{context.summary_memory.summary}\n\n---\n\n{new_summary}"
        else:
            context.summary_memory.summary = new_summary

        context.summary_memory.last_updated = time.time()

        # 清理已摘要的消息，只保留配置的短期窗口
        context.short_memory.messages = (
            context.short_memory.messages[-keep_count:]
            if len(context.short_memory.messages) > keep_count
            else context.short_memory.messages
        )

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
        降级策略：智能提取式摘要（✅ P1-3修复：增强AI摘要降级）

        改进策略：
        1. 关键词提取：识别核心概念（人名、地名、关键动作）
        2. 重要句子选择：基于重要度选择保留的句子
        3. 信息密度优化：优先保留信息量大的内容
        4. 结构化输出：按类别组织摘要内容

        当LLM不可用时，提供比简单截断更好的替代方案
        """
        if not messages:
            return ""

        summary_parts = []

        user_messages = [m for m in messages if m.role == "user"]
        assistant_messages = [m for m in messages if m.role == "assistant"]

        # === 1. 提取核心需求（从第一条用户消息）===
        if user_messages:
            core_request = self._extract_core_request(user_messages[0].content)
            if core_request:
                summary_parts.append(f"核心需求: {core_request}")

        # === 2. 提取关键实体（人名、地名、物品等）===
        all_content = " ".join([m.content for m in messages])
        entities = self._extract_key_entities(all_content)
        if entities:
            # 限制显示前10个实体
            entity_str = "、".join(entities[:10])
            if len(entities) > 10:
                entity_str += f"等{len(entities)}个"
            summary_parts.append(f"关键要素: {entity_str}")

        # === 3. 提取重要动作/事件 ===
        important_actions = self._extract_important_actions(messages)
        if important_actions:
            action_str = "；".join(important_actions[:3])
            summary_parts.append(f"关键操作: {action_str}")

        # === 4. 提取关键指令或要求 ===
        key_requirements = self._extract_key_requirements(user_messages)
        if key_requirements:
            req_str = "、".join(key_requirements[:5])
            summary_parts.append(f"用户要求: {req_str}")

        # === 5. 统计信息 ===
        user_count = len(user_messages)
        assistant_count = len(assistant_messages)
        summary_parts.append(
            f"对话轮次: {user_count}条用户消息, {assistant_count}条助手回复"
        )

        result = " | ".join(summary_parts)

        # 如果摘要为空或太短，使用基础降级策略
        if not result or len(result) < 50:
            if user_messages:
                first_user = user_messages[0].content[:150]
                result = f"用户请求: {first_user}..."
            if assistant_messages and len(result) < 100:
                first_assistant = assistant_messages[0].content[:150]
                result += f" | 助手回复: {first_assistant}..."

        logger.info(f"[FallbackSummary] 生成摘要: {len(result)}字符")
        return result

    def _extract_core_request(self, text: str) -> str:
        """
        提取核心需求（✅ P1-3修复：关键句子提取）

        策略：
        1. 查找包含关键动词的句子（想、要、帮我、创作等）
        2. 优先选择第一句或包含"想"、"要"的句子
        3. 限制长度为200字符

        Args:
            text: 用户输入文本

        Returns:
            核心需求文本
        """
        # 关键动词
        key_verbs = ["想", "要", "帮我", "帮忙", "创作", "写", "生成", "制作", "需要"]

        # 分句（按句号、问号、感叹号）
        import re
        sentences = re.split(r'[。？！?!]', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        if not sentences:
            return text[:200]

        # 查找包含关键动词的句子
        for sent in sentences:
            if any(verb in sent for verb in key_verbs):
                return sent[:200]

        # 如果没找到，返回第一句
        return sentences[0][:200]

    def _extract_key_entities(self, text: str) -> list:
        """
        提取关键实体（✅ P1-3修复：实体识别）

        使用规则匹配提取：
        1. 中文人名（2-4个汉字，常见姓氏开头）
        2. 地名（带"市"、"省"、"国"等后缀）
        3. 专有名词（引号内容、书名号内容）

        Args:
            text: 文本内容

        Returns:
            实体列表
        """
        import re
        entities = set()

        # 1. 匹配引号内容（专有名词）
        quoted = re.findall(r'["""](.*?)["""]', text)
        entities.update(q for q in quoted if 2 <= len(q) <= 20)

        # 2. 匹配书名号内容
        book_names = re.findall(r'《(.*?)》', text)
        entities.update(b for b in book_names if len(b) <= 20)

        # 3. 匹配常见姓氏开头的人名（2-4字）
        common_surnames = [
            "张", "王", "李", "赵", "刘", "陈", "杨", "黄", "周", "吴",
            "徐", "孙", "马", "朱", "胡", "郭", "何", "高", "林", "罗"
        ]
        for surname in common_surnames:
            names = re.findall(rf'{surname}[\u4e00-\u9fff]{{1,3}}', text)
            entities.update(n for n in names if len(n) <= 4)

        # 4. 匹配地名（带特定后缀）
        place_suffixes = ["市", "省", "国", "洲", "城", "镇", "县", "区", "岛"]
        for suffix in place_suffixes:
            places = re.findall(rf'[\u4e00-\u9fff]{{2,6}}{suffix}', text)
            entities.update(places)

        return list(entities)[:20]  # 限制最多20个

    def _extract_important_actions(self, messages: List[Message]) -> list:
        """
        提取重要动作/事件（✅ P1-3修复：事件提取）

        从助手回复中提取关键操作：
        1. 规划、创作、修改等主要动作
        2. 优先选择包含这些动词的句子

        Args:
            messages: 消息列表

        Returns:
            重要动作列表
        """
        import re
        actions = []

        # 关键动作词
        action_keywords = [
            "规划", "创作", "修改", "删除", "添加", "设定", "设计",
            "编写", "撰写", "生成", "制作", "优化", "调整"
        ]

        # 从助手消息中提取
        assistant_messages = [m for m in messages if m.role == "assistant"]

        for msg in assistant_messages[:5]:  # 只看前5条助手消息
            sentences = re.split(r'[。！？?!]', msg.content)
            for sent in sentences:
                sent = sent.strip()
                if not sent:
                    continue

                # 如果包含关键动作词
                for keyword in action_keywords:
                    if keyword in sent:
                        # 提取包含该动作的短句（最多50字符）
                        if len(sent) > 50:
                            # 尝试提取动作附近的内容
                            idx = sent.find(keyword)
                            start = max(0, idx - 10)
                            end = min(len(sent), idx + 40)
                            action = sent[start:end]
                        else:
                            action = sent

                        actions.append(action)
                        break  # 每句只提取一个动作

                if len(actions) >= 5:  # 最多提取5个动作
                    break

        return actions

    def _extract_key_requirements(self, user_messages: List[Message]) -> list:
        """
        提取关键指令或要求（✅ P1-3修复：需求提取）

        从用户消息中提取明确的要求：
        1. "必须"、"不要"、"要求"等强指令
        2. "注意"、"关键"、"重点"等提示

        Args:
            user_messages: 用户消息列表

        Returns:
            关键要求列表
        """
        import re
        requirements = []

        # 强指令关键词
        strong_keywords = [
            "必须", "一定要", "务必", "不要", "不能", "禁止",
            "要求", "需要", "希望", "注意", "关键", "重点"
        ]

        for msg in user_messages[:5]:  # 只看前5条用户消息
            sentences = re.split(r'[。！？?!]', msg.content)
            for sent in sentences:
                sent = sent.strip()
                if not sent:
                    continue

                # 如果包含强指令关键词
                for keyword in strong_keywords:
                    if keyword in sent:
                        # 提取该句（最多30字符）
                        if len(sent) > 30:
                            idx = sent.find(keyword)
                            start = max(0, idx - 5)
                            end = min(len(sent), idx + 25)
                            req = sent[start:end]
                        else:
                            req = sent

                        requirements.append(req)
                        break

                if len(requirements) >= 5:
                    break

        return requirements

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
        评估记忆重要度（0.0-1.0）（✅ P1-2修复：增强语义理解和上下文感知）

        改进策略：
        1. 检测否定词，避免误判（如"不想写设定" → 低重要度）
        2. 多层次关键词匹配，更精准的语义分类
        3. 考虑句子结构和信息密度
        4. 综合评分而非简单最大值

        规则：
        - 用户消息优先级高于助手消息
        - 包含"大纲"、"设定"、"角色"等关键词 → 0.9+
        - 包含"修改"、"要求"、"添加" → 0.7+
        - 长内容（>500字符） → 0.6+
        - 普通对话 → 0.3-0.5
        """
        content_lower = content.lower()
        importance = 0.3  # 基础分数

        # === 1. 否定词检测（✅ 新增：避免误判）===
        negative_patterns = [
            "不想", "不要", "别", "不用", "没有", "不需要", "不写",
            "取消", "删掉", "忽略", "跳过",
            "don't", "no need", "skip", "ignore", "cancel"
        ]

        # 检测是否包含否定词 + 关键词的组合
        has_negation = any(neg in content_lower for neg in negative_patterns)

        # === 2. 角色权重 ===
        if role == "user":
            importance += 0.1

        # === 3. 核心设定关键词（最高优先级）===
        high_value_keywords = [
            "大纲", "设定", "角色", "世界观", "背景", "人物", "主角", "配角",
            "剧情", "情节", "冲突", "高潮", "结局",
            "plot", "character", "setting", "worldview", "protagonist", "outline"
        ]

        high_value_score = 0.0
        matched_high = sum(1 for kw in high_value_keywords if kw in content_lower)
        if matched_high > 0:
            # 如果有否定词，降低权重
            if has_negation:
                high_value_score = 0.3  # 降低到中等重要度
                logger.debug(f"[ImportanceEval] 检测到否定词+核心关键词，降低重要度: {content[:50]}...")
            else:
                # 多个关键词 → 更高重要度
                high_value_score = min(0.6 + matched_high * 0.1, 0.7)

        # === 4. 重要指令关键词（中高优先级）===
        medium_value_keywords = [
            "修改", "要求", "添加", "删除", "更新", "调整", "优化", "改进",
            "必须", "不要", "注意", "关键", "重点",
            "modify", "update", "add", "delete", "change", "important", "must"
        ]

        medium_value_score = 0.0
        matched_medium = sum(1 for kw in medium_value_keywords if kw in content_lower)
        if matched_medium > 0:
            medium_value_score = min(0.4 + matched_medium * 0.05, 0.5)

        # === 5. 创作相关关键词（中等优先级）===
        creative_keywords = [
            "续写", "扩写", "润色", "改写", "创作", "编写",
            "章节", "段落", "对话", "描写", "叙述",
            "write", "continue", "compose", "rewrite"
        ]

        creative_score = 0.0
        matched_creative = sum(1 for kw in creative_keywords if kw in content_lower)
        if matched_creative > 0:
            creative_score = min(0.3 + matched_creative * 0.05, 0.4)

        # === 6. 内容长度和信息密度 ===
        length_score = 0.0
        if len(content) > 500:
            length_score = 0.3
        elif len(content) > 200:
            length_score = 0.2
        elif len(content) > 100:
            length_score = 0.1

        # === 7. 信息密度评估（句号、逗号数量反映信息量）===
        sentences = content.count('。') + content.count('.') + content.count('！') + content.count('!')
        if sentences >= 5:  # 多个句子 → 信息丰富
            length_score += 0.1

        # === 8. 综合评分（加权平均而非简单最大值）===
        # 取最高的两个类别分数进行加权
        category_scores = [
            high_value_score,
            medium_value_score,
            creative_score,
            length_score
        ]
        category_scores.sort(reverse=True)

        # 最高类别占70%，次高类别占30%
        final_score = importance + category_scores[0] * 0.7
        if len(category_scores) > 1:
            final_score += category_scores[1] * 0.3

        # === 9. 特殊模式检测 ===
        # 9.1 纯数字列表（可能是数据）
        if content.replace('\n', ' ').replace(',', ' ').replace('，', ' ').replace(' ', '').replace('.', '').isdigit():
            final_score = max(final_score, 0.4)  # 数据有一定重要度

        # 9.2 代码片段检测
        code_indicators = ['def ', 'class ', 'import ', 'function ', '```', '{', '}']
        if any(ind in content_lower for ind in code_indicators):
            final_score = max(final_score, 0.5)  # 代码片段有一定重要度

        # 9.3 问题式对话（重要度略低）
        question_marks = content.count('?') + content.count('？')
        if question_marks >= 2:  # 多个问题
            final_score = min(final_score, 0.6)  # 问题式对话重要度上限

        result = min(final_score, 1.0)  # 确保不超过1.0

        # 记录调试信息
        if matched_high > 0 or matched_medium > 0 or matched_creative > 0:
            logger.debug(
                f"[ImportanceEval] 分数={result:.2f} | "
                f"核心={high_value_score:.2f}({matched_high}) | "
                f"指令={medium_value_score:.2f}({matched_medium}) | "
                f"创作={creative_score:.2f}({matched_creative}) | "
                f"长度={length_score:.2f} | 否定={has_negation}"
            )

        return result

    async def _save_to_long_term_memory(
        self,
        content: str,
        session_id: str,
        role: str,
        importance: Optional[float] = None,
        work_id: Optional[str] = None,
        isolation_level: IsolationLevel = IsolationLevel.WORK  # ✅ 新增：隔离级别
    ):
        """
        保存到长期记忆

        Args:
            content: 记忆内容
            session_id: 会话ID
            role: 角色（user/assistant）
            importance: 重要度（如未指定则自动评估）
            work_id: 作品ID（WORK 级别时使用）
            isolation_level: 隔离级别（默认 WORK）
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

            # ✅ 保存到向量库（传递隔离级别）
            memory_id = await self._vector_store.add_memory(
                content=content,
                user_id=self.user_id,
                work_id=work_id,
                session_id=session_id,
                memory_type="conversation",
                importance=importance,
                isolation_level=isolation_level  # ✅ 新增
            )

            logger.info(
                f"✅ 保存长期记忆 | ID={memory_id[:20]}... | "
                f"隔离={isolation_level.value}:{work_id or 'N/A'} | "
                f"重要度={importance:.2f}"
            )

        except Exception as e:
            logger.error(f"❌ 保存长期记忆失败: {e}")

    async def _retrieve_long_term_memories(
        self,
        query: str,
        work_id: Optional[str] = None,
        session_id: Optional[str] = None,
        top_k: int = 3,
        min_similarity: float = 0.3,
        include_user_level: bool = True,  # ✅ 新增：是否包含用户级记忆
        isolation_level: IsolationLevel = IsolationLevel.WORK  # ✅ 新增：主要隔离级别
    ) -> List[Dict]:
        """
        检索长期记忆（支持多级隔离）

        Args:
            query: 查询文本
            work_id: 作品ID（WORK 级别时使用）
            session_id: 会话ID（SESSION 级别时使用）
            top_k: 返回Top K结果
            min_similarity: 最低相似度
            include_user_level: 是否包含用户级记忆（如偏好、风格）
            isolation_level: 主要隔离级别（默认 WORK）

        Returns:
            记忆列表
        """
        if not self._vector_store or not self.user_id:
            return []

        try:
            # ✅ 使用新的多级检索 API
            memories = await asyncio.wait_for(
                self._vector_store.search_memories(
                    query=query,
                    user_id=self.user_id,
                    work_id=work_id,
                    session_id=session_id,
                    top_k=top_k,
                    min_similarity=min_similarity,
                    include_user_level=include_user_level,
                    isolation_level=isolation_level
                ),
                timeout=ContextConfig.LTM_TIMEOUT
            )

            logger.info(
                f"🔍 检索长期记忆 | 级别={isolation_level.value} | "
                f"work_id={work_id or 'N/A'} | "
                f"含用户级={include_user_level} | 找到={len(memories)}条"
            )

            return memories

        except asyncio.TimeoutError:
            logger.error(f"❌ 检索长期记忆超时 ({ContextConfig.LTM_TIMEOUT}s)")
            record_timeout_event("ltm_search_timeout")
            return []
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

    def _analyze_task_type(self, query: str):
        """
        自动检测任务类型（✅ P1-7修复：启用自适应预算）

        根据查询内容的关键词和模式，自动判断任务类型，以便使用最优的Token预算分配策略。

        分类逻辑：
        1. CREATIVE（创作类）：续写、创作、改写、扩写等创作任务
        2. ANALYTICAL（分析类）：分析、评估、总结、诊断等分析任务
        3. QA（问答类）：问题、查询、解释等知识型对话
        4. CHAT（闲聊类）：日常对话、情感交流、简短回应

        Args:
            query: 用户查询文本

        Returns:
            TaskType枚举值
        """
        from app.services.context.adaptive_budget import TaskType

        query_lower = query.lower()

        # === 1. 创作类关键词（优先级最高）===
        creative_keywords = [
            "续写", "创作", "改写", "扩写", "润色", "编写", "写作",
            "章节", "段落", "对话", "描写", "叙述", "情节",
            "生成", "创建文本", "写一个", "写一段",
            "continue writing", "write", "compose", "create story"
        ]
        if any(kw in query_lower for kw in creative_keywords):
            logger.debug(f"[TaskType] 检测为 CREATIVE: {query[:50]}...")
            return TaskType.CREATIVE

        # === 2. 分析类关键词 ===
        analytical_keywords = [
            "分析", "评估", "总结", "诊断", "检查", "审查", "报告",
            "大纲", "结构", "优化", "改进建议", "问题",
            "质量", "评价", "对比", "比较",
            "analyze", "evaluate", "assess", "review", "summarize"
        ]
        if any(kw in query_lower for kw in analytical_keywords):
            logger.debug(f"[TaskType] 检测为 ANALYTICAL: {query[:50]}...")
            return TaskType.ANALYTICAL

        # === 3. 问答类关键词（包含疑问词和查询意图）===
        # 疑问词检测
        question_words = [
            "什么", "为什么", "怎么", "如何", "哪里", "哪个", "谁", "何时",
            "吗", "呢", "是否", "能否", "可以吗",
            "what", "why", "how", "where", "which", "who", "when", "is", "can"
        ]

        # 查询类关键词
        query_keywords = [
            "查询", "搜索", "查看", "显示", "找到", "获取", "告诉我",
            "解释", "说明", "定义", "介绍",
            "search", "find", "show", "get", "explain", "tell me"
        ]

        # 疑问句检测（以问号结尾）
        is_question = query.strip().endswith("?") or query.strip().endswith("？")

        if is_question or \
           any(qw in query_lower for qw in question_words) or \
           any(qk in query_lower for qk in query_keywords):
            logger.debug(f"[TaskType] 检测为 QA: {query[:50]}...")
            return TaskType.QA

        # === 4. 闲聊类关键词（简短、情感性、日常对话）===
        chat_keywords = [
            "你好", "嗨", "hi", "hello", "hey",
            "谢谢", "感谢", "thank",
            "再见", "拜拜", "bye",
            "哈哈", "呵呵", "嘿嘿",
            "好的", "知道了", "明白", "ok", "got it"
        ]

        # 简短文本判断（小于20字符且包含闲聊关键词）
        if len(query) < 20 and any(ck in query_lower for ck in chat_keywords):
            logger.debug(f"[TaskType] 检测为 CHAT: {query[:50]}...")
            return TaskType.CHAT

        # === 5. 默认：问答类（最通用的类型）===
        logger.debug(f"[TaskType] 默认检测为 QA: {query[:50]}...")
        return TaskType.QA

    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """
        计算文本相似度（✅ P1-4修复：记忆去重核心）

        使用改进的Jaccard相似度 + 字符级相似度：
        1. Jaccard: 词级别的交集/并集
        2. 字符级: 长公共子序列（LCS）比例
        3. 综合评分: 70% Jaccard + 30% LCS

        Args:
            text1: 第一个文本
            text2: 第二个文本

        Returns:
            相似度 (0.0-1.0)
        """
        # 预处理：去除空白字符并转小写
        t1 = text1.strip().lower()
        t2 = text2.strip().lower()

        if not t1 or not t2:
            return 0.0

        # 完全相同
        if t1 == t2:
            return 1.0

        # === 1. 词级别 Jaccard 相似度 ===
        # 中英文混合分词
        import re
        # 提取中文字符（每个字作为一个词）
        cn_words1 = [c for c in t1 if '\u4e00' <= c <= '\u9fff']
        cn_words2 = [c for c in t2 if '\u4e00' <= c <= '\u9fff']

        # 提取英文单词
        en_words1 = re.findall(r'[a-z]+', t1)
        en_words2 = re.findall(r'[a-z]+', t2)

        # 合并中英文词汇
        words1 = set(cn_words1 + en_words1)
        words2 = set(cn_words2 + en_words2)

        if not words1 or not words2:
            return 0.0

        intersection = words1 & words2
        union = words1 | words2

        jaccard_similarity = len(intersection) / len(union) if union else 0.0

        # === 2. 字符级相似度（简化版LCS）===
        # 计算公共字符占比
        common_chars = sum(1 for c in set(t1) if c in set(t2))
        total_chars = len(set(t1)) + len(set(t2))
        char_similarity = (2 * common_chars) / total_chars if total_chars > 0 else 0.0

        # === 3. 综合评分 ===
        similarity = jaccard_similarity * 0.7 + char_similarity * 0.3

        return min(similarity, 1.0)

    def _deduplicate_messages(
        self,
        messages: List[Message],
        threshold: Optional[float] = None
    ) -> List[Message]:
        """
        去除重复消息（✅ P1-4修复：记忆去重）

        策略：
        1. 计算相邻消息的相似度
        2. 如果相似度 >= threshold，保留重要度更高的（或更新的）
        3. 对于完全相同的消息，只保留第一条

        Args:
            messages: 消息列表
            threshold: 相似度阈值（可选，未指定时根据消息长度自适应）

        Returns:
            去重后的消息列表
        """
        if not messages or len(messages) <= 1:
            return messages

        logger.debug(f"[Deduplication] 开始去重: {len(messages)}条消息")

        unique_messages = []
        duplicate_count = 0

        for i, msg in enumerate(messages):
            is_duplicate = False

            # 与已保留的消息比较
            for j, existing in enumerate(unique_messages):
                # 只比较相同角色的消息
                if msg.role != existing.role:
                    continue

                similarity = self._calculate_text_similarity(msg.content, existing.content)

                # 自适应阈值：短消息要求更高相似度，长消息放宽
                adaptive_threshold = threshold
                if adaptive_threshold is None:
                    msg_tokens = self._estimate_tokens(msg.content)
                    adaptive_threshold = ContextConfig.dedup_threshold(msg_tokens)

                # 相似度超过阈值，视为重复
                if similarity >= adaptive_threshold:
                    is_duplicate = True
                    duplicate_count += 1

                    # 如果新消息内容更长或更新，替换旧消息
                    if len(msg.content) > len(existing.content):
                        logger.debug(
                            f"[Deduplication] 替换消息 #{j}: "
                            f"相似度={similarity:.2f}, "
                            f"新消息更长({len(msg.content)} > {len(existing.content)})"
                        )
                        unique_messages[j] = msg
                    else:
                        logger.debug(
                            f"[Deduplication] 跳过重复消息: "
                            f"相似度={similarity:.2f}, "
                            f"内容='{msg.content[:30]}...'"
                        )
                    break

            if not is_duplicate:
                unique_messages.append(msg)

        if duplicate_count > 0:
            logger.info(
                f"[Deduplication] ✅ 去重完成: "
                f"{len(messages)} -> {len(unique_messages)}条消息 "
                f"(移除{duplicate_count}条重复)"
            )

        return unique_messages
