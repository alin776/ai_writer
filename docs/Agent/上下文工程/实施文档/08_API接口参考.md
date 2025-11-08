# API接口参考 📚

> ⚠️ **文档性质：规划性参考文档**
>
> - 📋 **文档用途**: 描述计划实施后的API接口设计
> - ❌ **实施状态**: 大部分API尚不存在
> - ✅ **已存在**: HTTPAIService（25%的API已实现）
> - ❌ **不存在**: TokenCounter、SummaryService、VectorMemoryStore等
> - 💡 **使用建议**: 作为实施时的API设计参考

---

> 快速查阅常用接口和方法
>
> **用途**: 实施过程中快速查找API签名
> **维护**: 随项目更新

---

## HTTPAIService 接口

### 核心方法

#### 1. call_ai() - 非流式调用 ⭐ 推荐

```python
async def call_ai(
    self,
    system_prompt: str,
    user_prompt: str,
    max_tokens: int = 2000,
    temperature: float = 0.7,
    max_retries: int = 3,
    task_type: Optional[TaskType] = None
) -> str
```

**返回**: `str` - 完整的响应文本

**用途**: 摘要生成、分析任务等非流式场景

**示例**:
```python
from app.services.ai.http_ai_service import HTTPAIService

ai_service = HTTPAIService()
response = await ai_service.call_ai(
    system_prompt="你是一个专业的内容摘要助手",
    user_prompt="请总结以下内容：...",
    max_tokens=300,
    temperature=0.3
)
```

---

#### 2. stream_summarize() - 流式摘要

```python
async def stream_summarize(
    self,
    text: str,
    max_tokens: int = 500,
    temperature: float = 0.3
) -> AsyncGenerator[tuple[str, dict | None], None]
```

**返回**: `AsyncGenerator[(str, dict|None)]` - 流式响应

**用途**: 实时摘要生成（可选）

---

#### 3. stream_chat() - 流式对话

```python
async def stream_chat(
    self,
    messages: List[Dict[str, str]],
    max_tokens: int = 2000,
    temperature: float = 0.7
) -> AsyncGenerator[tuple[str, dict | None], None]
```

---

#### 4. 其他工具方法

```python
def count_tokens(self, text: str) -> int
    """Token计数"""

def get_available_models(self) -> List[str]
    """获取可用模型列表"""

async def health_check(self) -> bool
    """健康检查"""
```

---

## TokenCounter 接口

### 核心方法

#### 1. count_tokens() - 精确计数

```python
def count_tokens(text: str, model: str = "gpt-4") -> int
```

**便捷函数**，自动使用全局单例

**示例**:
```python
from app.services.context.token_counter import count_tokens

tokens = count_tokens("你好世界")
print(f"Tokens: {tokens}")  # 输出: Tokens: 6
```

---

#### 2. TokenCounter类

```python
class TokenCounter:
    def __init__(self, model: str = "gpt-4", fallback_enabled: bool = True):
        """初始化Token计数器"""

    def count_tokens(self, text: str) -> int:
        """计数Token（三层降级策略）"""

    def count_messages_tokens(self, messages: List[dict]) -> int:
        """计算消息列表的总Token数"""

    def get_stats(self) -> dict:
        """获取计数器状态"""
```

---

## SummaryService 接口

### 核心方法

```python
class SummaryService:
    def __init__(
        self,
        ai_service: Optional[HTTPAIService] = None,
        model: str = "gpt-4o-mini",
        max_retries: int = 2
    ):
        """初始化摘要服务"""

    async def summarize_conversation(
        self,
        messages: List[Message],
        max_length: int = 200,
        target_ratio: float = 0.3
    ) -> str:
        """总结对话历史"""

    async def summarize_chapter_content(
        self,
        content: str,
        max_length: int = 100
    ) -> str:
        """总结章节内容"""

    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
```

---

## ContextManager 接口

### 核心方法

```python
class ContextManager:
    def __init__(
        self,
        store: Optional[ContextStore] = None,
        token_budget: Optional[TokenBudget] = None,
        ai_service: Optional[HTTPAIService] = None,
        enable_long_term_memory: bool = False
    ):
        """初始化上下文管理器"""

    async def build_context(
        self,
        session_id: str,
        system_prompt: str = ""
    ) -> Dict[str, Any]:
        """构建上下文"""

    async def update_context(
        self,
        session_id: str,
        new_messages: List[Dict],
        context: Optional[Context] = None
    ):
        """更新上下文"""

    async def compress_context(self, context: Context):
        """压缩上下文"""

    async def clear_context(self, session_id: str):
        """清除上下文"""

    # ✅ 新增：长期记忆支持
    async def build_context_with_ltm(
        self,
        session_id: str,
        user_id: str,
        query: str,
        system_prompt: str = ""
    ) -> Dict[str, Any]:
        """构建包含长期记忆的上下文"""

    async def save_to_long_term_memory(
        self,
        user_id: str,
        conversation_id: str,
        content: str,
        importance: float = 0.5
    ):
        """保存到长期记忆"""
```

---

## VectorMemoryStore 接口

### 核心方法

```python
class VectorMemoryStore:
    def __init__(
        self,
        persist_directory: str = "./data/chroma_db",
        embedding_provider: str = "openai"
    ):
        """初始化向量存储"""

    async def add_memory(
        self,
        memory_id: str,
        content: str,
        metadata: Dict
    ):
        """添加记忆"""

    async def search_similar(
        self,
        query: str,
        user_id: str,
        top_k: int = 5,
        min_score: float = 0.7
    ) -> List[Dict]:
        """语义检索相关记忆"""

    async def delete_memory(self, memory_id: str):
        """删除记忆"""

    async def clear_user_memories(self, user_id: str):
        """清除用户的所有记忆"""

    def get_stats(self) -> Dict:
        """获取统计信息"""
```

---

## 数据模型

### Context

```python
@dataclass
class Context:
    session_id: str
    short_memory: ShortMemory = field(default_factory=ShortMemory)
    summary_memory: SummaryMemory = field(default_factory=SummaryMemory)
    long_term_memory: LongTermMemory = field(default_factory=LongTermMemory)
    system_prompt: str = ""

    def get_total_tokens(self) -> int:
        """计算总Token数"""
```

### Message

```python
@dataclass
class Message:
    role: str  # user, assistant, system
    content: str
    timestamp: float
    metadata: Dict[str, Any] = field(default_factory=dict)
```

### TokenBudget

```python
@dataclass
class TokenBudget:
    total: int = 8000
    system_prompt: float = 0.20
    summary: float = 0.25
    short_memory: float = 0.35
    tools: float = 0.15
    reserved: float = 0.05

    def get_budget(self, category: str) -> int:
        """获取某类别的Token预算"""
```

---

## 常用导入路径

```python
# AI服务
from app.services.ai.http_ai_service import HTTPAIService

# Token计数
from app.services.context.token_counter import TokenCounter, count_tokens

# 摘要服务
from app.services.context.summary_service import SummaryService

# 上下文管理
from app.services.context.manager import ContextManager
from app.services.context.models import Context, Message

# 向量存储
from app.services.context.vector_memory_store import VectorMemoryStore

# 监控
from app.services.context.monitoring_integration import (
    ContextMetrics,
    monitor_token_counting,
    monitor_summary_generation
)
```

---

## 配置参数

### 环境变量

```bash
# 基础配置
REDIS_URL=redis://localhost:6379/0
OPENAI_API_KEY=sk-...

# 长期记忆（可选）
ENABLE_LONG_TERM_MEMORY=true
VECTOR_STORE_PROVIDER=openai  # openai | local
CHROMA_PERSIST_DIR=./data/chroma_db

# 摘要配置
ENABLE_LLM_SUMMARY=true
SUMMARY_MODEL=gpt-4o-mini
SUMMARY_TIMEOUT=10.0
SUMMARY_MAX_RETRIES=2

# Token预算
TOKEN_BUDGET_TOTAL=8000
```

---

## 快速示例

### 基础用法

```python
# 1. 创建AI服务
ai_service = HTTPAIService()

# 2. 创建ContextManager
manager = ContextManager(ai_service=ai_service)

# 3. 构建上下文
context_result = await manager.build_context(
    session_id="session_123",
    system_prompt="你是AI写作助手"
)

# 4. 使用上下文
messages = context_result["messages"]
print(f"Token数: {context_result['metadata']['token_count']}")

# 5. 更新上下文
await manager.update_context(
    session_id="session_123",
    new_messages=[
        {"role": "user", "content": "你好"},
        {"role": "assistant", "content": "你好！"}
    ]
)
```

### 长期记忆用法

```python
# 1. 启用长期记忆
manager = ContextManager(
    ai_service=ai_service,
    enable_long_term_memory=True
)

# 2. 保存重要记忆
await manager.save_to_long_term_memory(
    user_id="user_123",
    conversation_id="conv_456",
    content="主角李明修炼火系功法",
    importance=0.9
)

# 3. 检索相关记忆
context_result = await manager.build_context_with_ltm(
    session_id="session_789",
    user_id="user_123",
    query="主角的功法是什么？"
)
```

---

## 监控指标

### 可用指标

```python
# Token计数
ContextMetrics.TOKEN_COUNT_DURATION
ContextMetrics.TOKEN_COUNT_TOTAL

# 摘要生成
ContextMetrics.SUMMARY_GENERATION_TOTAL
ContextMetrics.SUMMARY_GENERATION_SUCCESS
ContextMetrics.SUMMARY_GENERATION_FAILURE
ContextMetrics.SUMMARY_GENERATION_DURATION

# 压缩效果
ContextMetrics.CONTEXT_COMPRESSION_RATIO
ContextMetrics.CONTEXT_TOKEN_USAGE

# 上下文操作
ContextMetrics.CONTEXT_BUILD_DURATION
ContextMetrics.CONTEXT_BUILD_TOTAL
```

### 使用监控

```python
from app.services.context.monitoring_integration import (
    monitor_token_counting,
    record_compression_metrics
)

# 装饰器监控
@monitor_token_counting
def my_token_counting_function(text: str) -> int:
    return count_tokens(text)

# 手动记录
record_compression_metrics(
    original_tokens=1000,
    compressed_tokens=400,
    session_id="session_123"
)
```

---

**最后更新**: 2025-01-08
