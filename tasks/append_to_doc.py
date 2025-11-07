#!/usr/bin/env python3
"""
将完整的实施文档内容追加到 context_optimization_implementation.md
"""

# Day 3-4 剩余步骤 + Day 5-11 + 验收标准等

CONTENT_TO_APPEND = """

#### 步骤2: 修改manager.py集成摘要服务（2小时）

**文件**: `backend/app/services/context/manager.py`

**修改位置**: `_generate_summary()` 方法（200-227行）

```python
# 在文件顶部添加导入
from app.services.context.summary_service import get_summary_service

class ContextManager:
    """上下文管理器 - 专为chat_stream优化"""

    def __init__(
        self,
        store: Optional[ContextStore] = None,
        token_budget: Optional[TokenBudget] = None,
        ai_service = None  # 新增：AI服务实例
    ):
        self.store = store or RedisContextStore()
        self.token_budget = token_budget or TokenBudget()
        self.ai_service = ai_service  # 新增

        # 初始化摘要服务（如果提供了AI服务）
        self.summary_service = None
        if ai_service:
            self.summary_service = get_summary_service(ai_service)

    async def _generate_summary(self, messages: List[Message]) -> str:
        """
        生成对话摘要

        使用两层策略：
        1. 优先使用LLM生成高质量摘要（如果summary_service可用）
        2. 降级使用简单策略
        """
        if not messages:
            return ""

        # 策略1: 使用LLM生成摘要
        if self.summary_service:
            try:
                logger.info(f"[ContextManager] 使用LLM生成摘要，消息数={len(messages)}")
                summary = await self.summary_service.summarize_conversation(
                    messages=messages,
                    max_length=200,
                    target_ratio=0.3
                )

                if summary:
                    logger.info(f"[ContextManager] LLM摘要生成成功，长度={len(summary)}")
                    return summary
                else:
                    logger.warning(f"[ContextManager] LLM摘要为空，使用降级策略")
            except Exception as e:
                logger.warning(f"[ContextManager] LLM摘要失败: {e}，使用降级策略")

        # 策略2: 降级策略（简单提取）
        logger.info(f"[ContextManager] 使用降级策略生成摘要")
        return self._fallback_summary(messages)

    @staticmethod
    def _fallback_summary(messages: List[Message]) -> str:
        """降级策略：简单提取关键信息"""
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
```

---

#### 步骤3: 修改langgraph_agent.py的章节压缩逻辑（2小时）

**文件**: `backend/app/services/agent/langgraph_agent.py`

**修改策略**: 集成summary_service.summarize_chapter_content()

```python
# 在文件顶部添加导入
from app.services.context.summary_service import get_summary_service

class LangGraphAgent:
    """LangGraph Agent主类"""

    def __init__(self, ...):
        # ... 现有初始化代码 ...

        # 新增：初始化摘要服务
        self.summary_service = get_summary_service(self.ai_service)

    async def _compress_chapter_content(self, content: str, target_length: int = 500) -> str:
        """
        压缩章节内容

        使用两层策略：
        1. 优先使用LLM生成语义摘要
        2. 降级使用规则提取

        Args:
            content: 章节原文
            target_length: 目标长度

        Returns:
            压缩后的内容
        """
        if not content or len(content) <= target_length:
            return content

        logger.info(f"[Agent] 压缩章节内容: {len(content)} → {target_length}")

        # 策略1: 使用LLM摘要
        try:
            summary = await self.summary_service.summarize_chapter_content(
                content=content,
                max_length=target_length
            )

            if summary and len(summary) > 50:  # 验证摘要有效性
                logger.info(f"[Agent] LLM章节摘要成功: {len(content)} → {len(summary)}")
                return summary
            else:
                logger.warning(f"[Agent] LLM摘要质量不佳，使用降级策略")
        except Exception as e:
            logger.warning(f"[Agent] LLM摘要失败: {e}，使用降级策略")

        # 策略2: 规则提取（降级）
        return self._fallback_compress_chapter(content, target_length)

    @staticmethod
    def _fallback_compress_chapter(content: str, target_length: int) -> str:
        """降级策略：规则提取关键内容"""
        lines = content.split('\\n')

        # 提取包含关键词的行
        keywords = ['主角', '情节', '冲突', '转折', '结局', '关键']
        important_lines = []

        for line in lines:
            if any(keyword in line for keyword in keywords):
                important_lines.append(line.strip())

        # 如果关键行太少，添加开头和结尾
        if len('\\n'.join(important_lines)) < target_length // 2:
            important_lines.insert(0, lines[0] if lines else "")
            important_lines.append(lines[-1] if lines else "")

        result = '\\n'.join(important_lines)

        # 确保不超过目标长度
        if len(result) > target_length:
            result = result[:target_length] + "..."

        return result
```

---

#### 步骤4: 编写单元测试（2小时）

测试文件已在步骤1创建，这里补充集成测试：

**新建文件**: `backend/tests/test_context_integration.py`

```python
\"\"\"
上下文系统集成测试
验证Token计数和摘要生成在实际场景中的效果
\"\"\"

import pytest
import asyncio
import time
from app.services.context.manager import ContextManager
from app.services.context.models import Message, TokenBudget
from app.services.ai.http_ai_service import HTTPAIService


class TestContextIntegration:
    \"\"\"上下文集成测试\"\"\"

    @pytest.fixture
    async def manager(self):
        \"\"\"创建ContextManager实例\"\"\"
        ai_service = HTTPAIService()
        token_budget = TokenBudget(total=4000)
        return ContextManager(ai_service=ai_service, token_budget=token_budget)

    @pytest.mark.asyncio
    async def test_long_conversation_compression(self, manager):
        \"\"\"测试长对话自动压缩\"\"\"
        session_id = "test_long_conv"

        # 模拟10轮对话
        for i in range(10):
            ctx_data = await manager.build_context(
                session_id=session_id,
                system_prompt="你是一个智能写作助手"
            )

            new_messages = [
                {"role": "user", "content": f"这是第{i+1}轮对话，我想询问关于写作的问题。" * 10},
                {"role": "assistant", "content": f"好的，关于第{i+1}个问题，我的建议是..." * 10}
            ]

            await manager.update_context(
                session_id=session_id,
                new_messages=new_messages,
                context=ctx_data["context"]
            )

        # 验证压缩效果
        final_ctx = await manager.build_context(session_id=session_id)

        print(f"\\n最终Token数: {final_ctx['metadata']['token_count']}")
        print(f"短期记忆消息数: {final_ctx['metadata']['short_memory_size']}")
        print(f"是否有摘要: {final_ctx['metadata']['has_summary']}")

        assert final_ctx['metadata']['token_count'] < 4000
        assert final_ctx['metadata']['has_summary']
        assert final_ctx['metadata']['short_memory_size'] <= 8

        await manager.clear_context(session_id)
```

---

#### 步骤5: 集成测试（1.5小时）

运行完整测试套件：

```bash
# 1. 单元测试
pytest tests/test_token_counter.py -v
pytest tests/test_summary_service.py -v

# 2. 集成测试
pytest tests/test_context_integration.py -v

# 3. 验证修改
python test_manager_summary.py
```

---

#### 步骤6: 验收检查（30分钟）

```bash
# 执行验收清单
cd D:\\Java\\ai_writer\\backend

# 1. 所有测试通过
pytest tests/test_*.py -v

# 2. 代码质量检查
flake8 app/services/context/ --max-line-length=120

# 3. 性能基准
python -m pytest tests/test_context_integration.py::TestContextIntegration::test_long_conversation_compression -v -s
```

---

### ✅ Day 3-4 验收标准

- [ ] summary_service.py创建完成（994行代码）
- [ ] manager.py修改完成，集成摘要服务
- [ ] langgraph_agent.py修改完成，章节压缩使用LLM
- [ ] 测试文件全部通过（test_summary_service.py, test_context_integration.py）
- [ ] 摘要质量验证 ≥ 7/10分
- [ ] 摘要生成成功率 ≥ 90%
- [ ] 降级策略正常工作
- [ ] 性能测试：单次摘要 < 15秒

---

### 📊 Day 3-4 预期效果

| 指标 | 修改前 | 修改后 | 提升 |
|------|--------|--------|------|
| 摘要质量 | 3/10 | 8/10 | +167% |
| 摘要准确性 | 简单截取 | 语义理解 | 质的飞跃 |
| 压缩效果 | 30-40% | 60-70% | +75% |
| 可用性 | 100% | 100% | 保持 |
| 成本 | 0 | 低（gpt-4o-mini） | 可接受 |

---

## Day 5: 监控集成

### 📍 任务目标

集成现有的监控系统(`app/services/agent/utils/monitoring.py`)，实现Token计数和摘要生成的全面监控。

### 🔍 现状分析

**现有监控系统位置**: `backend/app/services/agent/utils/monitoring.py`

**已有功能**:
- ✅ 指标收集（Counter, Gauge, Histogram, Timer）
- ✅ 告警系统（AlertLevel: INFO/WARNING/ERROR/CRITICAL）
- ✅ 健康检查（HealthStatus）
- ✅ 性能统计

**需要集成的监控点**:
1. Token计数器性能监控
2. 摘要服务性能和质量监控
3. 压缩效果监控
4. 上下文管理器监控

### 🛠️ 实施步骤

#### 步骤1: 全局监控实例初始化（30分钟）

**新建文件**: `backend/app/services/context/monitoring_integration.py`

```python
\"\"\"
上下文系统监控集成
使用现有的 app/services/agent/utils/monitoring.py
\"\"\"

import logging
from typing import Optional
from app.services.agent.utils.monitoring import MonitoringSystem

logger = logging.getLogger(__name__)

# 全局监控实例
_global_monitoring: Optional[MonitoringSystem] = None


def init_context_monitoring(
    monitoring_system: Optional[MonitoringSystem] = None
) -> MonitoringSystem:
    \"\"\"
    初始化上下文系统监控

    Args:
        monitoring_system: 外部传入的监控系统实例，如果为None则创建新实例

    Returns:
        MonitoringSystem实例
    \"\"\"
    global _global_monitoring

    if monitoring_system:
        _global_monitoring = monitoring_system
        logger.info("[MonitoringIntegration] 使用外部监控系统")
    elif _global_monitoring is None:
        _global_monitoring = MonitoringSystem(name="context_system")
        logger.info("[MonitoringIntegration] 创建新的监控系统实例")

    return _global_monitoring


def get_context_monitoring() -> Optional[MonitoringSystem]:
    \"\"\"获取全局监控实例\"\"\"
    return _global_monitoring
```

---

#### 步骤2: 在TokenCounter中集成监控（1小时）

**修改文件**: `backend/app/services/context/token_counter.py`

```python
# 在文件顶部添加导入
from app.services.agent.utils.monitoring import MonitoringSystem, MetricType
from app.services.context.monitoring_integration import get_context_monitoring

class TokenCounter:
    \"\"\"Token计数器 - 支持多种策略\"\"\"

    def __init__(
        self,
        model: str = "gpt-4",
        fallback_enabled: bool = True
    ):
        self.model = model
        self.fallback_enabled = fallback_enabled
        self._encoding = None
        self.monitoring = get_context_monitoring()  # 获取全局监控实例
        self._init_encoding()

    def count_tokens(self, text: str) -> int:
        \"\"\"计数Token - 自动选择最佳策略（集成监控）\"\"\"
        import time
        start_time = time.time()

        if not text:
            return 0

        strategy_used = None
        tokens = 0

        try:
            # 策略1: tiktoken精确计数
            if self._encoding is not None:
                try:
                    tokens = len(self._encoding.encode(text))
                    strategy_used = "tiktoken"

                    # 监控：记录成功
                    if self.monitoring:
                        self.monitoring.record_metric(
                            name="token_counter.strategy.tiktoken",
                            value=1,
                            metric_type=MetricType.COUNTER,
                            labels={"model": self.model}
                        )

                    return tokens
                except Exception as e:
                    logger.warning(f"tiktoken计数失败: {e}")

                    # 监控：记录失败
                    if self.monitoring:
                        self.monitoring.record_metric(
                            name="token_counter.tiktoken.errors",
                            value=1,
                            metric_type=MetricType.COUNTER
                        )

            # 策略2: 中文优化估算
            if self.fallback_enabled:
                tokens = self._estimate_tokens_with_chinese(text)
                strategy_used = "chinese_optimized"

                if self.monitoring:
                    self.monitoring.record_metric(
                        name="token_counter.strategy.fallback",
                        value=1,
                        metric_type=MetricType.COUNTER,
                        labels={"strategy": "chinese_optimized"}
                    )

                return tokens

            # 策略3: 简单估算
            tokens = len(text) // 4
            strategy_used = "simple"

            return tokens

        finally:
            # 监控：性能指标
            duration = time.time() - start_time

            if self.monitoring and strategy_used:
                # 计数耗时
                self.monitoring.record_metric(
                    name="token_counter.duration",
                    value=duration * 1000,
                    metric_type=MetricType.HISTOGRAM,
                    labels={"strategy": strategy_used},
                    unit="ms"
                )

                # Token数分布
                self.monitoring.record_metric(
                    name="token_counter.tokens_counted",
                    value=tokens,
                    metric_type=MetricType.HISTOGRAM,
                    labels={"strategy": strategy_used}
                )
```

---

#### 步骤3: 在SummaryService中集成监控（1.5小时）

**修改文件**: `backend/app/services/context/summary_service.py`

```python
# 在文件顶部添加导入
from app.services.agent.utils.monitoring import MonitoringSystem, MetricType, AlertLevel
from app.services.context.monitoring_integration import get_context_monitoring

class SummaryService:
    \"\"\"摘要生成服务\"\"\"

    def __init__(
        self,
        ai_service,
        model: str = "gpt-4o-mini",
        max_retries: int = 2,
        timeout: float = 10.0
    ):
        self.ai_service = ai_service
        self.model = model
        self.max_retries = max_retries
        self.timeout = timeout
        self.monitoring = get_context_monitoring()  # 获取全局监控实例

        self._stats = {
            "total_calls": 0,
            "successes": 0,
            "failures": 0,
            "fallbacks": 0,
            "total_time": 0.0
        }

    async def summarize_conversation(
        self,
        messages: List[Message],
        max_length: int = 200,
        target_ratio: float = 0.3
    ) -> str:
        \"\"\"总结对话历史（集成监控）\"\"\"
        if not messages:
            return ""

        start_time = time.time()
        self._stats["total_calls"] += 1
        success = False
        used_fallback = False

        try:
            conversation = self._format_messages(messages)

            # 监控：记录输入规模
            if self.monitoring:
                self.monitoring.record_metric(
                    name="summary.conversation.input_messages",
                    value=len(messages),
                    metric_type=MetricType.GAUGE
                )
                self.monitoring.record_metric(
                    name="summary.conversation.input_length",
                    value=len(conversation),
                    metric_type=MetricType.HISTOGRAM
                )

            prompt = self._build_conversation_summary_prompt(conversation, max_length)
            summary = await self._call_llm_with_retry(prompt)

            if self._validate_summary(summary, max_length):
                self._stats["successes"] += 1
                success = True
                duration = time.time() - start_time
                self._stats["total_time"] += duration

                # 监控：记录成功和性能
                if self.monitoring:
                    self.monitoring.record_metric(
                        name="summary.conversation.success",
                        value=1,
                        metric_type=MetricType.COUNTER
                    )
                    self.monitoring.record_metric(
                        name="summary.conversation.duration",
                        value=duration * 1000,
                        metric_type=MetricType.HISTOGRAM,
                        unit="ms"
                    )

                    # 压缩率
                    compression_ratio = len(summary) / len(conversation) if len(conversation) > 0 else 0
                    self.monitoring.record_metric(
                        name="summary.conversation.compression_ratio",
                        value=compression_ratio,
                        metric_type=MetricType.GAUGE
                    )

                return summary
            else:
                raise ValueError("Summary validation failed")

        except Exception as e:
            self._stats["failures"] += 1
            self._stats["fallbacks"] += 1
            used_fallback = True

            # 监控：记录失败
            if self.monitoring:
                self.monitoring.record_metric(
                    name="summary.conversation.failure",
                    value=1,
                    metric_type=MetricType.COUNTER,
                    labels={"error": str(e)[:50]}
                )

                # 检查失败率并触发告警
                failure_rate = self._stats["failures"] / self._stats["total_calls"]
                if failure_rate > 0.3:
                    self.monitoring.create_alert(
                        level=AlertLevel.WARNING,
                        title="摘要服务失败率过高",
                        message=f"失败率: {failure_rate:.1%}",
                        metadata={"failure_rate": failure_rate}
                    )

            return self._fallback_conversation_summary(messages, max_length)
```

---

#### 步骤4: 在ContextManager中集成监控（1小时）

**修改文件**: `backend/app/services/context/manager.py`

```python
# 在文件顶部添加导入
from app.services.agent.utils.monitoring import MetricType
from app.services.context.monitoring_integration import get_context_monitoring

class ContextManager:
    \"\"\"上下文管理器\"\"\"

    def __init__(
        self,
        store: Optional[ContextStore] = None,
        token_budget: Optional[TokenBudget] = None,
        ai_service = None
    ):
        self.store = store or RedisContextStore()
        self.token_budget = token_budget or TokenBudget()
        self.ai_service = ai_service
        self.monitoring = get_context_monitoring()  # 获取监控实例

        # 初始化摘要服务
        self.summary_service = None
        if ai_service:
            self.summary_service = get_summary_service(ai_service)

    async def build_context(
        self,
        session_id: str,
        system_prompt: str = ""
    ) -> Dict[str, Any]:
        \"\"\"构建上下文（集成监控）\"\"\"
        import time
        start_time = time.time()

        context = await self.store.load(session_id)

        if not context:
            context = Context(session_id=session_id, system_prompt=system_prompt)

        total_tokens = context.get_total_tokens()
        max_tokens = self.token_budget.total

        # 监控：Token使用情况
        if self.monitoring:
            self.monitoring.record_metric(
                name="context.tokens.total",
                value=total_tokens,
                metric_type=MetricType.GAUGE
            )
            self.monitoring.record_metric(
                name="context.tokens.usage_ratio",
                value=total_tokens / max_tokens if max_tokens > 0 else 0,
                metric_type=MetricType.GAUGE
            )
            self.monitoring.record_metric(
                name="context.messages.count",
                value=len(context.short_memory.messages),
                metric_type=MetricType.GAUGE
            )

        # 压缩检查
        compression_triggered = total_tokens > max_tokens * 0.8
        if compression_triggered:
            if self.monitoring:
                self.monitoring.record_metric(
                    name="context.compression.triggered",
                    value=1,
                    metric_type=MetricType.COUNTER
                )
            await self.compress_context(context)

        messages = self._build_messages(context)

        # 监控：构建耗时
        duration = time.time() - start_time
        if self.monitoring:
            self.monitoring.record_metric(
                name="context.build.duration",
                value=duration * 1000,
                metric_type=MetricType.HISTOGRAM,
                unit="ms"
            )

        return {
            "messages": messages,
            "metadata": {
                "session_id": session_id,
                "token_count": context.get_total_tokens(),
                "short_memory_size": len(context.short_memory.messages),
                "has_summary": bool(context.summary_memory.summary),
                "compression_triggered": compression_triggered
            },
            "context": context
        }

    async def compress_context(self, context: Context):
        \"\"\"压缩上下文（集成监控）\"\"\"
        import time
        start_time = time.time()

        before_tokens = context.get_total_tokens()
        before_messages = len(context.short_memory.messages)

        messages_to_summarize = context.short_memory.messages[:-4] if len(context.short_memory.messages) > 4 else []

        if not messages_to_summarize:
            return

        new_summary = await self._generate_summary(messages_to_summarize)

        if context.summary_memory.summary:
            context.summary_memory.summary = f"{context.summary_memory.summary}\\n\\n---\\n\\n{new_summary}"
        else:
            context.summary_memory.summary = new_summary

        context.summary_memory.last_updated = time.time()
        context.short_memory.messages = context.short_memory.messages[-4:]

        after_tokens = context.get_total_tokens()
        tokens_saved = before_tokens - after_tokens
        compression_ratio = tokens_saved / before_tokens if before_tokens > 0 else 0

        # 监控：压缩效果
        if self.monitoring:
            self.monitoring.record_metric(
                name="context.compression.completed",
                value=1,
                metric_type=MetricType.COUNTER
            )
            self.monitoring.record_metric(
                name="context.compression.tokens_saved",
                value=tokens_saved,
                metric_type=MetricType.HISTOGRAM
            )
            self.monitoring.record_metric(
                name="context.compression.ratio",
                value=compression_ratio,
                metric_type=MetricType.GAUGE
            )
            self.monitoring.record_metric(
                name="context.compression.duration",
                value=(time.time() - start_time) * 1000,
                metric_type=MetricType.HISTOGRAM,
                unit="ms"
            )

        logger.info(
            f"压缩完成: 消息{before_messages}→{len(context.short_memory.messages)}, "
            f"Token{before_tokens}→{after_tokens}, 节省{tokens_saved}({compression_ratio:.1%})"
        )
```

---

#### 步骤5: 创建监控测试（1小时）

**新建文件**: `backend/tests/test_monitoring_integration.py`

```python
\"\"\"
监控集成测试
验证监控指标正确记录
\"\"\"

import pytest
import asyncio
from app.services.context.monitoring_integration import init_context_monitoring
from app.services.context.token_counter import TokenCounter
from app.services.context.manager import ContextManager
from app.services.ai.http_ai_service import HTTPAIService
from app.services.agent.utils.monitoring import MonitoringSystem


class TestMonitoringIntegration:
    \"\"\"监控集成测试\"\"\"

    @pytest.fixture
    def monitoring_system(self):
        \"\"\"创建监控系统\"\"\"
        monitoring = MonitoringSystem(name="test_context")
        init_context_monitoring(monitoring)
        return monitoring

    def test_token_counter_metrics(self, monitoring_system):
        \"\"\"测试Token计数器监控\"\"\"
        counter = TokenCounter()

        # 执行计数
        text = "这是一个测试文本。" * 10
        tokens = counter.count_tokens(text)

        # 验证监控指标
        metrics = monitoring_system.get_all_metrics()
        print(f"\\n记录的指标数: {len(metrics)}")

        # 应该至少有strategy和duration指标
        assert len(metrics) > 0, "应该记录了监控指标"

        # 打印指标详情
        for metric in metrics:
            print(f"  {metric.name}: {metric.value} {metric.unit}")

    @pytest.mark.asyncio
    async def test_context_manager_metrics(self, monitoring_system):
        \"\"\"测试ContextManager监控\"\"\"
        ai_service = HTTPAIService()
        manager = ContextManager(ai_service=ai_service)

        # 构建上下文
        ctx = await manager.build_context("test_session", "测试提示词")

        # 验证监控指标
        metrics = monitoring_system.get_all_metrics()
        print(f"\\n记录的指标数: {len(metrics)}")

        # 应该有tokens、messages、duration等指标
        metric_names = [m.name for m in metrics]
        assert any("context" in name for name in metric_names)

        await manager.clear_context("test_session")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
```

---

#### 步骤6: 验收检查（30分钟）

```bash
# 1. 运行监控测试
pytest tests/test_monitoring_integration.py -v -s

# 2. 验证监控数据输出
python -c "
from app.services.context.monitoring_integration import init_context_monitoring
from app.services.context.token_counter import TokenCounter

monitoring = init_context_monitoring()
counter = TokenCounter()

# 执行一些操作
counter.count_tokens('测试' * 100)

# 查看监控数据
metrics = monitoring.get_all_metrics()
print(f'\\n总指标数: {len(metrics)}')
for m in metrics:
    print(f'{m.name}: {m.value} {m.unit}')
"
```

---

### ✅ Day 5 验收标准

- [ ] monitoring_integration.py创建完成
- [ ] TokenCounter集成监控完成
- [ ] SummaryService集成监控完成
- [ ] ContextManager集成监控完成
- [ ] 监控测试全部通过
- [ ] 所有关键操作都有监控覆盖
- [ ] 告警机制正常工作（失败率>30%触发告警）

---

### 📊 Day 5 预期效果

| 监控维度 | 覆盖指标 | 数量 |
|---------|---------|------|
| Token计数 | strategy, duration, tokens_counted | 3+ |
| 摘要生成 | success, failure, duration, compression_ratio | 5+ |
| 上下文管理 | tokens.total, messages.count, compression | 6+ |
| 总计 | - | 14+ |

---

## Day 6-7: 端到端测试

### 📍 任务目标

编写全面的端到端测试，验证整个上下文压缩系统在实际场景中的表现。

### 🛠️ 实施步骤

#### 步骤1: 对话层端到端测试（3小时）

**新建文件**: `backend/tests/test_e2e_conversation.py`

```python
\"\"\"
对话层端到端测试
模拟真实的长对话场景，验证压缩效果
\"\"\"

import pytest
import asyncio
import time
from app.services.context.manager import ContextManager
from app.services.context.models import TokenBudget
from app.services.ai.http_ai_service import HTTPAIService


class TestE2EConversation:
    \"\"\"端到端对话测试\"\"\"

    @pytest.fixture
    async def manager(self):
        \"\"\"创建ContextManager\"\"\"
        ai_service = HTTPAIService()
        token_budget = TokenBudget(total=2000)  # 较小预算，方便触发压缩
        return ContextManager(ai_service=ai_service, token_budget=token_budget)

    @pytest.mark.asyncio
    async def test_20_round_conversation(self, manager):
        \"\"\"测试20轮对话的完整流程\"\"\"
        session_id = "e2e_test_20_rounds"

        compression_count = 0
        final_token_count = 0

        # 模拟20轮对话
        for i in range(20):
            ctx = await manager.build_context(
                session_id=session_id,
                system_prompt="你是智能写作助手"
            )

            if ctx['metadata']['compression_triggered']:
                compression_count += 1

            # 模拟用户和助手对话
            new_messages = [
                {
                    "role": "user",
                    "content": f"第{i+1}轮：请帮我构思一个关于{['科幻', '奇幻', '都市', '武侠'][i % 4]}的故事情节。"
                },
                {
                    "role": "assistant",
                    "content": f"好的，关于第{i+1}轮的{['科幻', '奇幻', '都市', '武侠'][i % 4]}故事，我建议从以下几个方面入手：\\n"
                              f"1. 世界观设定...\\n2. 主要角色...\\n3. 核心冲突...\\n4. 情节发展..." * 3
                }
            ]

            await manager.update_context(
                session_id=session_id,
                new_messages=new_messages,
                context=ctx["context"]
            )

            final_token_count = ctx['metadata']['token_count']

            print(f"\\r第{i+1}轮: Token={final_token_count}, 压缩={compression_count}次", end="")

        print(f"\\n\\n测试完成:")
        print(f"  总轮数: 20")
        print(f"  压缩次数: {compression_count}")
        print(f"  最终Token数: {final_token_count}")

        # 验证
        assert compression_count > 0, "应该触发了压缩"
        assert final_token_count < 2000, "Token数应该在预算内"

        # 检查是否生成了摘要
        final_ctx = await manager.build_context(session_id=session_id)
        assert final_ctx['metadata']['has_summary'], "应该生成了摘要"

        await manager.clear_context(session_id)

    @pytest.mark.asyncio
    async def test_very_long_messages(self, manager):
        \"\"\"测试超长消息的处理\"\"\"
        session_id = "e2e_test_long_msg"

        # 创建超长消息（每条消息约500 tokens）
        long_content = "这是一个非常详细的故事设定。" * 100

        for i in range(5):
            ctx = await manager.build_context(session_id=session_id)

            new_messages = [
                {"role": "user", "content": long_content},
                {"role": "assistant", "content": long_content}
            ]

            await manager.update_context(
                session_id=session_id,
                new_messages=new_messages,
                context=ctx["context"]
            )

        final_ctx = await manager.build_context(session_id=session_id)

        print(f"\\n超长消息测试:")
        print(f"  最终Token数: {final_ctx['metadata']['token_count']}")
        print(f"  是否有摘要: {final_ctx['metadata']['has_summary']}")

        assert final_ctx['metadata']['token_count'] < 2000

        await manager.clear_context(session_id)
```

---

#### 步骤2: 压力测试（2小时）

**新建文件**: `backend/tests/test_stress.py`

```python
\"\"\"
压力测试
验证系统在高负载下的稳定性
\"\"\"

import pytest
import asyncio
import time
from app.services.context.manager import ContextManager
from app.services.ai.http_ai_service import HTTPAIService


class TestStress:
    \"\"\"压力测试\"\"\"

    @pytest.mark.asyncio
    async def test_concurrent_sessions(self):
        \"\"\"测试并发会话处理\"\"\"
        ai_service = HTTPAIService()
        manager = ContextManager(ai_service=ai_service)

        async def simulate_session(session_id: str):
            \"\"\"模拟一个会话\"\"\"
            for i in range(10):
                ctx = await manager.build_context(session_id=session_id)
                new_messages = [
                    {"role": "user", "content": f"消息{i}"},
                    {"role": "assistant", "content": f"回复{i}"}
                ]
                await manager.update_context(
                    session_id=session_id,
                    new_messages=new_messages,
                    context=ctx["context"]
                )

        # 并发10个会话
        start_time = time.time()
        sessions = [f"stress_session_{i}" for i in range(10)]

        await asyncio.gather(*[simulate_session(sid) for sid in sessions])

        duration = time.time() - start_time
        print(f"\\n并发测试完成:")
        print(f"  会话数: 10")
        print(f"  每会话轮数: 10")
        print(f"  总耗时: {duration:.2f}s")
        print(f"  平均每轮: {duration / 100:.2f}s")

        # 清理
        for sid in sessions:
            await manager.clear_context(sid)

        assert duration < 60, "10个会话应该在60秒内完成"

    @pytest.mark.asyncio
    async def test_performance_baseline(self):
        \"\"\"性能基准测试\"\"\"
        ai_service = HTTPAIService()
        manager = ContextManager(ai_service=ai_service)

        session_id = "baseline_test"

        times = []

        for i in range(10):
            start = time.time()

            ctx = await manager.build_context(session_id=session_id)
            new_messages = [
                {"role": "user", "content": "测试消息" * 20},
                {"role": "assistant", "content": "测试回复" * 20}
            ]
            await manager.update_context(
                session_id=session_id,
                new_messages=new_messages,
                context=ctx["context"]
            )

            times.append(time.time() - start)

        avg_time = sum(times) / len(times)
        max_time = max(times)
        min_time = min(times)

        print(f"\\n性能基准:")
        print(f"  平均耗时: {avg_time*1000:.2f}ms")
        print(f"  最大耗时: {max_time*1000:.2f}ms")
        print(f"  最小耗时: {min_time*1000:.2f}ms")

        await manager.clear_context(session_id)

        assert avg_time < 2.0, "平均响应时间应该小于2秒"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
```

---

#### 步骤3: 运行完整测试套件（1小时）

```bash
# 1. 运行所有单元测试
pytest tests/test_token_counter.py -v
pytest tests/test_summary_service.py -v

# 2. 运行集成测试
pytest tests/test_context_integration.py -v

# 3. 运行端到端测试
pytest tests/test_e2e_conversation.py -v -s

# 4. 运行压力测试
pytest tests/test_stress.py -v -s

# 5. 生成覆盖率报告
pytest --cov=app/services/context --cov-report=html
```

---

### ✅ Day 6-7 验收标准

- [ ] 端到端测试全部通过
- [ ] 20轮对话测试通过
- [ ] 超长消息处理正常
- [ ] 并发10个会话测试通过
- [ ] 性能基准达标（平均<2s）
- [ ] 测试覆盖率 ≥ 80%

---

## Day 8-11: 自适应Token分配

### 📍 任务目标

实现根据任务类型动态调整Token预算分配的功能。

### 🔍 场景分析

不同任务类型对Token的需求不同：

| 任务类型 | 系统提示 | 摘要上下文 | 近期对话 | 建议分配 |
|---------|---------|-----------|---------|---------|
| 创作型 | 15% | 20% | 45% | 重对话 |
| 分析型 | 25% | 35% | 20% | 重历史 |
| 问答型 | 20% | 25% | 35% | 均衡 |
| 闲聊型 | 10% | 15% | 55% | 超重对话 |

### 🛠️ 实施步骤

#### 步骤1: 创建动态预算分配器（2小时）

**新建文件**: `backend/app/services/context/adaptive_budget.py`

```python
\"\"\"
自适应Token预算分配器
根据任务类型动态调整Token分配比例
\"\"\"

import logging
from typing import Dict, Optional
from enum import Enum
from dataclasses import dataclass

logger = logging.getLogger(__name__)


class TaskType(Enum):
    \"\"\"任务类型\"\"\"
    CREATIVE = "creative"      # 创作型（写作、构思）
    ANALYTICAL = "analytical"  # 分析型（分析、总结）
    QA = "qa"                  # 问答型（一般问答）
    CHAT = "chat"              # 闲聊型（日常对话）
    UNKNOWN = "unknown"        # 未知类型


@dataclass
class BudgetAllocation:
    \"\"\"预算分配方案\"\"\"
    system_prompt_ratio: float   # 系统提示词比例
    summary_ratio: float          # 摘要上下文比例
    short_memory_ratio: float    # 近期对话比例
    reserved_ratio: float        # 保留比例

    def validate(self):
        \"\"\"验证分配方案总和为1.0\"\"\"
        total = (
            self.system_prompt_ratio +
            self.summary_ratio +
            self.short_memory_ratio +
            self.reserved_ratio
        )
        assert abs(total - 1.0) < 0.01, f"总比例应为1.0，实际为{total}"


class AdaptiveBudgetAllocator:
    \"\"\"自适应预算分配器\"\"\"

    # 预设的分配方案
    ALLOCATIONS = {
        TaskType.CREATIVE: BudgetAllocation(
            system_prompt_ratio=0.15,
            summary_ratio=0.20,
            short_memory_ratio=0.45,
            reserved_ratio=0.20
        ),
        TaskType.ANALYTICAL: BudgetAllocation(
            system_prompt_ratio=0.25,
            summary_ratio=0.35,
            short_memory_ratio=0.20,
            reserved_ratio=0.20
        ),
        TaskType.QA: BudgetAllocation(
            system_prompt_ratio=0.20,
            summary_ratio=0.25,
            short_memory_ratio=0.35,
            reserved_ratio=0.20
        ),
        TaskType.CHAT: BudgetAllocation(
            system_prompt_ratio=0.10,
            summary_ratio=0.15,
            short_memory_ratio=0.55,
            reserved_ratio=0.20
        ),
        TaskType.UNKNOWN: BudgetAllocation(
            system_prompt_ratio=0.20,
            summary_ratio=0.25,
            short_memory_ratio=0.35,
            reserved_ratio=0.20
        )
    }

    def __init__(self, total_budget: int = 4000):
        \"\"\"
        初始化分配器

        Args:
            total_budget: 总Token预算
        \"\"\"
        self.total_budget = total_budget

        # 验证所有分配方案
        for task_type, allocation in self.ALLOCATIONS.items():
            allocation.validate()

    def allocate(
        self,
        task_type: TaskType,
        custom_allocation: Optional[BudgetAllocation] = None
    ) -> Dict[str, int]:
        \"\"\"
        分配Token预算

        Args:
            task_type: 任务类型
            custom_allocation: 自定义分配方案（可选）

        Returns:
            分配结果 {"system_prompt": 800, "summary": 1000, ...}
        \"\"\"
        # 使用自定义方案或预设方案
        allocation = custom_allocation or self.ALLOCATIONS.get(
            task_type,
            self.ALLOCATIONS[TaskType.UNKNOWN]
        )

        result = {
            "system_prompt": int(self.total_budget * allocation.system_prompt_ratio),
            "summary": int(self.total_budget * allocation.summary_ratio),
            "short_memory": int(self.total_budget * allocation.short_memory_ratio),
            "reserved": int(self.total_budget * allocation.reserved_ratio)
        }

        logger.info(
            f"[AdaptiveBudget] {task_type.value}任务分配: "
            f"系统={result['system_prompt']}, "
            f"摘要={result['summary']}, "
            f"对话={result['short_memory']}"
        )

        return result

    @staticmethod
    def detect_task_type(system_prompt: str, recent_messages: list) -> TaskType:
        \"\"\"
        检测任务类型（简单规则）

        Args:
            system_prompt: 系统提示词
            recent_messages: 近期消息

        Returns:
            TaskType
        \"\"\"
        prompt_lower = system_prompt.lower()

        # 关键词匹配
        if any(kw in prompt_lower for kw in ["写作", "创作", "构思", "故事"]):
            return TaskType.CREATIVE
        elif any(kw in prompt_lower for kw in ["分析", "总结", "归纳", "提炼"]):
            return TaskType.ANALYTICAL
        elif any(kw in prompt_lower for kw in ["问答", "咨询", "帮助"]):
            return TaskType.QA
        elif any(kw in prompt_lower for kw in ["闲聊", "聊天", "对话"]):
            return TaskType.CHAT

        # 基于对话轮数判断
        if recent_messages and len(recent_messages) > 10:
            return TaskType.CHAT  # 长对话倾向于闲聊

        return TaskType.UNKNOWN
```

---

#### 步骤2: 集成到ContextManager（1.5小时）

**修改文件**: `backend/app/services/context/manager.py`

```python
# 在文件顶部添加导入
from app.services.context.adaptive_budget import AdaptiveBudgetAllocator, TaskType

class ContextManager:
    \"\"\"上下文管理器\"\"\"

    def __init__(
        self,
        store: Optional[ContextStore] = None,
        token_budget: Optional[TokenBudget] = None,
        ai_service = None,
        enable_adaptive_budget: bool = False  # 新增：是否启用自适应分配
    ):
        self.store = store or RedisContextStore()
        self.token_budget = token_budget or TokenBudget()
        self.ai_service = ai_service
        self.monitoring = get_context_monitoring()

        # 自适应预算分配器
        self.enable_adaptive_budget = enable_adaptive_budget
        if enable_adaptive_budget:
            self.budget_allocator = AdaptiveBudgetAllocator(
                total_budget=self.token_budget.total
            )
            logger.info("[ContextManager] 自适应Token分配已启用")
        else:
            self.budget_allocator = None

        # 摘要服务
        self.summary_service = None
        if ai_service:
            self.summary_service = get_summary_service(ai_service)

    def _build_messages_with_budget(
        self,
        context: Context,
        budget_allocation: Optional[Dict[str, int]] = None
    ) -> List[Dict]:
        \"\"\"
        根据预算分配构建消息

        Args:
            context: 上下文对象
            budget_allocation: 预算分配方案

        Returns:
            消息列表
        \"\"\"
        messages = []

        # 如果没有提供分配方案，使用默认逻辑
        if not budget_allocation:
            return self._build_messages(context)

        # 1. 系统提示（按预算裁剪）
        if context.system_prompt:
            from app.services.context.token_counter import count_tokens

            system_tokens = count_tokens(context.system_prompt)
            max_system_tokens = budget_allocation.get("system_prompt", 800)

            if system_tokens > max_system_tokens:
                # 简单裁剪（实际可以使用更智能的方法）
                ratio = max_system_tokens / system_tokens
                truncated = context.system_prompt[:int(len(context.system_prompt) * ratio)]
                messages.append({"role": "system", "content": truncated})
                logger.warning(
                    f"[ContextManager] 系统提示被裁剪: {system_tokens} → {max_system_tokens} tokens"
                )
            else:
                messages.append({"role": "system", "content": context.system_prompt})

        # 2. 摘要上下文（按预算裁剪）
        if context.summary_memory.summary:
            summary_content = f"对话摘要：\\n{context.summary_memory.summary}"

            if context.summary_memory.important_facts:
                facts = "\\n".join(f"- {fact}" for fact in context.summary_memory.important_facts)
                summary_content += f"\\n\\n重要信息：\\n{facts}"

            messages.append({"role": "system", "content": summary_content})

        # 3. 近期对话（按预算选择条数）
        max_memory_tokens = budget_allocation.get("short_memory", 1400)
        selected_messages = []
        current_tokens = 0

        # 从最近的消息开始选择
        for msg in reversed(context.short_memory.messages):
            from app.services.context.token_counter import count_tokens
            msg_tokens = count_tokens(msg.content)

            if current_tokens + msg_tokens <= max_memory_tokens:
                selected_messages.insert(0, msg)
                current_tokens += msg_tokens
            else:
                break

        for msg in selected_messages:
            messages.append({"role": msg.role, "content": msg.content})

        logger.info(
            f"[ContextManager] 自适应构建消息: "
            f"系统提示={budget_allocation.get('system_prompt')}t, "
            f"对话消息={len(selected_messages)}条"
        )

        return messages

    async def build_context(
        self,
        session_id: str,
        system_prompt: str = ""
    ) -> Dict[str, Any]:
        \"\"\"构建上下文（支持自适应分配）\"\"\"
        import time
        start_time = time.time()

        context = await self.store.load(session_id)

        if not context:
            context = Context(session_id=session_id, system_prompt=system_prompt)

        total_tokens = context.get_total_tokens()
        max_tokens = self.token_budget.total

        # 监控
        if self.monitoring:
            self.monitoring.record_metric(
                name="context.tokens.total",
                value=total_tokens,
                metric_type=MetricType.GAUGE
            )

        # 压缩检查
        compression_triggered = total_tokens > max_tokens * 0.8
        if compression_triggered:
            await self.compress_context(context)

        # 自适应预算分配
        budget_allocation = None
        if self.enable_adaptive_budget and self.budget_allocator:
            # 检测任务类型
            task_type = self.budget_allocator.detect_task_type(
                system_prompt,
                context.short_memory.messages
            )

            # 分配预算
            budget_allocation = self.budget_allocator.allocate(task_type)

            logger.info(f"[ContextManager] 任务类型: {task_type.value}")

        # 构建消息
        if budget_allocation:
            messages = self._build_messages_with_budget(context, budget_allocation)
        else:
            messages = self._build_messages(context)

        return {
            "messages": messages,
            "metadata": {
                "session_id": session_id,
                "token_count": context.get_total_tokens(),
                "short_memory_size": len(context.short_memory.messages),
                "has_summary": bool(context.summary_memory.summary),
                "compression_triggered": compression_triggered,
                "adaptive_budget_enabled": self.enable_adaptive_budget,
                "budget_allocation": budget_allocation
            },
            "context": context
        }
```

---

#### 步骤3: 测试自适应分配（1.5小时）

**新建文件**: `backend/tests/test_adaptive_budget.py`

```python
\"\"\"
自适应Token分配测试
\"\"\"

import pytest
from app.services.context.adaptive_budget import (
    AdaptiveBudgetAllocator,
    TaskType,
    BudgetAllocation
)


class TestAdaptiveBudget:
    \"\"\"自适应预算测试\"\"\"

    def test_creative_task_allocation(self):
        \"\"\"测试创作型任务分配\"\"\"
        allocator = AdaptiveBudgetAllocator(total_budget=4000)

        result = allocator.allocate(TaskType.CREATIVE)

        print(f"\\n创作型任务分配:")
        for key, value in result.items():
            print(f"  {key}: {value}")

        # 创作型应该有最多的对话Token
        assert result["short_memory"] > result["summary"]
        assert result["short_memory"] > result["system_prompt"]

    def test_analytical_task_allocation(self):
        \"\"\"测试分析型任务分配\"\"\"
        allocator = AdaptiveBudgetAllocator(total_budget=4000)

        result = allocator.allocate(TaskType.ANALYTICAL)

        print(f"\\n分析型任务分配:")
        for key, value in result.items():
            print(f"  {key}: {value}")

        # 分析型应该有最多的摘要Token
        assert result["summary"] > result["short_memory"]

    def test_task_type_detection(self):
        \"\"\"测试任务类型检测\"\"\"
        allocator = AdaptiveBudgetAllocator()

        # 测试创作型
        task_type = allocator.detect_task_type("你是一个智能写作助手", [])
        assert task_type == TaskType.CREATIVE

        # 测试分析型
        task_type = allocator.detect_task_type("请帮我分析以下内容", [])
        assert task_type == TaskType.ANALYTICAL

        # 测试闲聊型（长对话）
        messages = [{"role": "user", "content": f"消息{i}"} for i in range(15)]
        task_type = allocator.detect_task_type("助手", messages)
        assert task_type == TaskType.CHAT

    def test_custom_allocation(self):
        \"\"\"测试自定义分配方案\"\"\"
        allocator = AdaptiveBudgetAllocator(total_budget=4000)

        custom = BudgetAllocation(
            system_prompt_ratio=0.3,
            summary_ratio=0.3,
            short_memory_ratio=0.2,
            reserved_ratio=0.2
        )

        result = allocator.allocate(TaskType.UNKNOWN, custom_allocation=custom)

        assert result["system_prompt"] == 1200
        assert result["summary"] == 1200


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
```

---

### ✅ Day 8-11 验收标准

- [ ] AdaptiveBudgetAllocator实现完成
- [ ] ContextManager集成自适应分配
- [ ] 4种任务类型分配方案定义完成
- [ ] 任务类型检测逻辑实现
- [ ] 测试全部通过
- [ ] 可通过配置开关启用/禁用

---

## 验收标准总清单

### 代码质量

- [ ] 所有代码使用中文注释
- [ ] 符合PEP8规范
- [ ] 无明显代码异味
- [ ] 关键函数有文档字符串

### 功能完整性

- [ ] Day 1-2: Token估算准确率 ≥ 95%
- [ ] Day 3-4: 摘要质量 ≥ 8/10
- [ ] Day 5: 监控覆盖率 100%
- [ ] Day 6-7: 所有端到端测试通过
- [ ] Day 8-11: 自适应分配正常工作

### 测试覆盖

- [ ] 单元测试覆盖率 ≥ 80%
- [ ] 集成测试通过
- [ ] 端到端测试通过
- [ ] 压力测试通过

### 性能指标

- [ ] Token计数 < 10ms
- [ ] 摘要生成 < 15s
- [ ] 上下文构建 < 2s
- [ ] 并发10会话 < 60s

### 可用性

- [ ] 所有功能有降级策略
- [ ] 异常处理完善
- [ ] 日志记录完整
- [ ] 监控告警正常

---

## 风险控制

### P0级风险

**风险1: LLM摘要服务不稳定**

- **影响**: 摘要生成失败率高
- **缓解**: 实现降级策略（简单提取）
- **检测**: 监控失败率，超30%告警
- **回滚**: 禁用LLM摘要，只用降级策略

**风险2: tiktoken兼容性问题**

- **影响**: Token计数失败
- **缓解**: 三层降级策略
- **检测**: 监控计数错误率
- **回滚**: 使用中文优化估算

### P1级风险

**风险3: 监控数据量过大**

- **影响**: 性能下降，存储占用高
- **缓解**: 限制监控指标保留时间
- **检测**: 监控系统性能
- **回滚**: 减少监控指标

**风险4: 自适应分配效果不佳**

- **影响**: Token利用率低
- **缓解**: 提供配置开关，默认禁用
- **检测**: A/B测试对比
- **回滚**: 关闭自适应分配

---

## FAQ常见问题

### Q1: 为什么使用gpt-4o-mini而不是gpt-4？

A: 摘要生成是高频操作，使用gpt-4o-mini可以：
- 降低成本（约1/10）
- 提高速度（响应更快）
- 对于摘要任务，质量已足够

### Q2: 降级策略会不会导致质量下降？

A: 降级策略设计原则：
- 只在LLM失败时触发
- 简单提取好于完全失败
- 监控会记录降级次数
- 可根据数据优化降级逻辑

### Q3: 自适应分配是否适合所有场景？

A: 不是，建议：
- 初期默认禁用
- 在稳定场景下启用
- 通过A/B测试验证效果
- 根据反馈调整分配比例

### Q4: 如何判断实施是否成功？

A: 关键指标：
- Token估算准确率 > 95%
- 摘要质量评分 > 8/10
- 压缩率达到60-70%
- 系统稳定性保持100%

### Q5: 出现问题如何快速回滚？

A: 回滚步骤：
1. 禁用自适应分配（enable_adaptive_budget=False）
2. 禁用LLM摘要（不传ai_service）
3. 回退到简单Token估算
4. 重启服务，观察稳定性

---

## 回滚方案

### 紧急回滚（5分钟内）

```bash
# 1. 修改配置，禁用新功能
# 在 config.py 或环境变量中：
ENABLE_ADAPTIVE_BUDGET=false
ENABLE_LLM_SUMMARY=false

# 2. 重启服务
systemctl restart ai-writer-backend

# 3. 验证系统恢复
curl http://localhost:8000/health
```

### 完全回滚（30分钟内）

```bash
# 1. 切换到稳定分支
git checkout main

# 2. 重新部署
cd backend
pip install -r requirements.txt
systemctl restart ai-writer-backend

# 3. 验证功能
pytest tests/test_basic.py -v
```

### 分步回滚

如果只某个功能有问题，可分步回滚：

**只回滚自适应分配**:
```python
manager = ContextManager(
    enable_adaptive_budget=False  # 禁用自适应
)
```

**只回滚LLM摘要**:
```python
manager = ContextManager(
    ai_service=None  # 不传AI服务，使用降级策略
)
```

**只回滚Token精确计数**:
```python
# 卸载tiktoken
pip uninstall tiktoken -y
# 系统会自动使用降级策略
```

---

## 附录

### A. 相关文件清单

| 文件 | 类型 | 说明 |
|------|------|------|
| app/services/context/token_counter.py | 新建 | Token计数器 |
| app/services/context/summary_service.py | 新建 | 摘要服务 |
| app/services/context/adaptive_budget.py | 新建 | 自适应分配器 |
| app/services/context/monitoring_integration.py | 新建 | 监控集成 |
| app/services/context/manager.py | 修改 | 集成新功能 |
| app/services/agent/langgraph_agent.py | 修改 | 章节压缩 |
| tests/test_*.py | 新建 | 测试文件 |

### B. 依赖项

```txt
tiktoken>=0.5.0
pytest>=7.0.0
pytest-asyncio>=0.21.0
pytest-cov>=4.0.0
```

### C. 配置参数

```python
# 环境变量
ENABLE_ADAPTIVE_BUDGET=true|false
ENABLE_LLM_SUMMARY=true|false
TOKEN_BUDGET_TOTAL=4000
SUMMARY_MODEL=gpt-4o-mini
SUMMARY_TIMEOUT=10.0
```

---

## 最后更新

**文档版本**: v1.0
**完成时间**: 2025-01-07
**总工期**: 9-11个工作日
**预期ROI**: 4-6倍

**下一步**:
1. 获得批准后开始实施
2. 按照Day 1-2开始执行
3. 每日更新进度到todo.md
4. 遇到问题及时调整方案

---

**完整实施文档编写完成！** ✅
"""

def main():
    """追加内容到文档"""
    doc_path = r"D:\\Java\\ai_writer\\tasks\\context_optimization_implementation.md"

    # 读取现有内容
    with open(doc_path, 'r', encoding='utf-8') as f:
        existing_content = f.read()

    # 移除"文档太长，继续编写中..."标记
    if "**文档太长，继续编写中...**" in existing_content:
        existing_content = existing_content.replace("\\n\\n**文档太长，继续编写中...**\\n", "")
        existing_content = existing_content.replace("**文档太长，继续编写中...**", "")

    # 追加新内容
    full_content = existing_content + CONTENT_TO_APPEND

    # 写回文件
    with open(doc_path, 'w', encoding='utf-8') as f:
        f.write(full_content)

    print(f"✅ 内容已成功追加到 {doc_path}")
    print(f"新增内容长度: {len(CONTENT_TO_APPEND)} 字符")
    print(f"总文档长度: {len(full_content)} 字符")

if __name__ == "__main__":
    main()
