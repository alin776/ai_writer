
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

**验证脚本**:

```bash
# 创建测试脚本: backend/test_manager_summary.py
python -c "
import asyncio
from app.services.context.manager import ContextManager
from app.services.context.models import Message
from app.services.ai.http_ai_service import HTTPAIService
import time

async def test_summary():
    ai_service = HTTPAIService()
    manager = ContextManager(ai_service=ai_service)
    
    messages = [
        Message(role='user', content='你好，我想写一本科幻小说', timestamp=time.time()),
        Message(role='assistant', content='很高兴帮助你！你有什么具体的想法吗？', timestamp=time.time()),
    ]
    
    summary = await manager._generate_summary(messages)
    print(f'摘要长度: {len(summary)}')
    print(f'摘要内容: {summary}')
    assert len(summary) > 0
    print('✅ 测试通过')

asyncio.run(test_summary())
"
```

---

#### 步骤3: 修改langgraph_agent.py的章节压缩逻辑（2小时）

**文件**: `backend/app/services/agent/langgraph_agent.py`

在Agent类的初始化中添加摘要服务，并修改章节压缩方法：

```python
# 在文件顶部添加导入
from app.services.context.summary_service import get_summary_service

class LangGraphAgent:
    """LangGraph Agent主类"""
    
    def __init__(self, ...):
        # ... 现有初始化代码 ...
        
        # 新增：初始化摘要服务
        if hasattr(self, 'ai_service'):
            self.summary_service = get_summary_service(self.ai_service)
    
    async def _compress_chapter_content(self, content: str, target_length: int = 500) -> str:
        """
        压缩章节内容
        
        使用两层策略：
        1. 优先使用LLM生成语义摘要
        2. 降级使用规则提取
        """
        if not content or len(content) <= target_length:
            return content
        
        logger.info(f"[Agent] 压缩章节内容: {len(content)} → {target_length}")
        
        # 策略1: 使用LLM摘要
        if hasattr(self, 'summary_service'):
            try:
                summary = await self.summary_service.summarize_chapter_content(
                    content=content,
                    max_length=target_length
                )
                
                if summary and len(summary) > 50:
                    logger.info(f"[Agent] LLM章节摘要成功: {len(content)} → {len(summary)}")
                    return summary
            except Exception as e:
                logger.warning(f"[Agent] LLM摘要失败: {e}，使用降级策略")
        
        # 策略2: 规则提取（降级）
        return self._fallback_compress_chapter(content, target_length)
```

---

#### 步骤4-6: 测试和验收

详细的测试代码已在步骤1的summary_service.py文件创建时包含。

**运行测试**:

```bash
cd D:\Java\ai_writer\backend

# 运行所有相关测试
pytest tests/test_summary_service.py -v
pytest tests/test_context_integration.py -v
```

---

### ✅ Day 3-4 验收标准

- [ ] summary_service.py创建完成（约1000行代码）
- [ ] manager.py修改完成，集成摘要服务
- [ ] langgraph_agent.py修改完成
- [ ] 测试文件全部通过
- [ ] 摘要质量 ≥ 7/10分
- [ ] 摘要生成成功率 ≥ 90%
- [ ] 降级策略正常工作

---

### 📊 Day 3-4 预期效果

| 指标 | 修改前 | 修改后 | 提升 |
|------|--------|--------|------|
| 摘要质量 | 3/10 | 8/10 | +167% |
| 压缩效果 | 30-40% | 60-70% | +75% |
| 可用性 | 100% | 100% | 保持 |

