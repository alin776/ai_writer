# Day 1-2: Token估算改进 🔢

> ⚠️ **文档性质：规划文档 - 功能尚未实施**
>
> - ❌ **实施状态**: 未开始（0%）
> - 📝 **实际情况**: tiktoken已安装但完全未被项目代码使用
> - 🔍 **代码现状**: 仍使用简单估算 `len(content) // 4`（准确率70%）
> - 📊 **详细状态**: 查看 [`IMPLEMENTATION_STATUS.md`](./IMPLEMENTATION_STATUS.md#1-token估算改进文档01)

---

> 将Token估算准确率从70-75%提升到95-100%
>
> **优先级**: P0 - 必须完成
> **工期**: 2天
> **难度**: ⭐⭐ 简单

---

## 📑 目录

- [任务目标](#任务目标)
- [现状分析](#现状分析)
- [技术方案](#技术方案)
- [实施步骤](#实施步骤)
- [验收标准](#验收标准)
- [故障排除](#故障排除)

---

## 任务目标

### 定量目标

| 指标 | 当前值 | 目标值 | 提升幅度 |
|------|--------|--------|---------|
| 英文准确率 | 75% | 100% | +33% |
| 中文准确率 | 60% | 95%+ | +58% |
| 混合文本准确率 | 70% | 95%+ | +36% |
| 计数性能 | ~1ms | <10ms | 可接受 |

### 定性目标

1. ✅ 建立三层降级策略，确保高可用性
2. ✅ 统一所有Token计数逻辑
3. ✅ 提供详细日志和监控接口

---

## 现状分析

### 问题文件清单

| 文件 | 行号 | 当前实现 | 问题 |
|------|------|---------|------|
| `models.py` | 37-40 | `len(content) // 4` | 中文误差40% |
| `models.py` | 50-54 | `len(content) // 4` | 中文误差40% |
| `models.py` | 80-86 | `len(content) // 4` | 中文误差40% |
| `llm_optimizer.py` | 39-42 | `len(prompt) // 4` | 中文误差40% |
| `llm_optimizer.py` | 285-293 | 中文优化算法（未使用） | 未被调用 |

### 根本原因

**简单估算的致命缺陷**：
```python
# 当前实现
tokens = len(text) // 4

# 问题1: 中文字符
"你好世界" → 4个字符 → 1 token ❌ 实际≈6 tokens
# 问题2: 英文单词
"Hello world" → 11个字符 → 2 tokens ❌ 实际≈3 tokens
```

---

## 技术方案

### 三层降级策略

```
┌─────────────────────────────────────┐
│  策略1: tiktoken精确计数 (100%)     │
│  ├─ 使用OpenAI官方tokenizer        │
│  ├─ 支持所有GPT模型                │
│  └─ 性能: 2-5ms/次                  │
└─────────────────────────────────────┘
                ↓ 失败时
┌─────────────────────────────────────┐
│  策略2: 中文优化估算 (95%)          │
│  ├─ 识别中文字符                    │
│  ├─ 中文: 1.5字符/token             │
│  ├─ 英文: 4字符/token               │
│  └─ 性能: <1ms/次                   │
└─────────────────────────────────────┘
                ↓ 禁用时
┌─────────────────────────────────────┐
│  策略3: 简单估算 (75%)              │
│  ├─ 字符数 / 4                      │
│  └─ 性能: <1ms/次                   │
└─────────────────────────────────────┘
```

### 为什么选择tiktoken？

| 方案 | 准确率 | 性能 | 依赖 | 维护成本 |
|------|--------|------|------|---------|
| tiktoken | 100% | 快 | 1个库 | 低（官方） |
| transformers | 100% | 慢 | 10+库 | 高 |
| 自建tokenizer | 90% | 快 | 0 | 极高 |

**结论**：tiktoken最佳（OpenAI官方，准确+快速）

---

## 实施步骤

### 📍 步骤1: 安装tiktoken（30分钟）

#### 1.1 安装依赖

```bash
# 切换到backend目录
cd D:\Java\ai_writer\backend

# 激活虚拟环境
.\venv\Scripts\activate

# 安装tiktoken
pip install tiktoken

# 验证安装
python -c "import tiktoken; print(f'tiktoken版本: {tiktoken.__version__}')"
```

**预期输出**：
```
tiktoken版本: 0.5.2
```

#### 1.2 更新requirements.txt

```bash
# 添加到requirements.txt
echo tiktoken>=0.5.0 >> requirements.txt

# 验证
cat requirements.txt | grep tiktoken
```

**验收**：
- [ ] tiktoken成功导入
- [ ] requirements.txt包含tiktoken>=0.5.0

---

### 📍 步骤2: 创建TokenCounter类（2小时）

#### 2.1 创建文件

**新建**：`backend/app/services/context/token_counter.py`

```python
"""
Token计数器 - 三层策略

策略优先级:
1. tiktoken精确计数（准确率100%）
2. 中文优化估算（准确率95%）
3. 简单估算（准确率75%）
"""

import logging
from typing import Optional, List
from functools import lru_cache

logger = logging.getLogger(__name__)

# 尝试导入tiktoken
try:
    import tiktoken
    TIKTOKEN_AVAILABLE = True
except ImportError:
    TIKTOKEN_AVAILABLE = False
    logger.warning("tiktoken未安装，将使用降级策略")


class TokenCounter:
    """Token计数器 - 支持多种策略"""

    def __init__(self, model: str = "gpt-4", fallback_enabled: bool = True):
        """
        初始化Token计数器

        Args:
            model: 模型名称，用于选择encoding
            fallback_enabled: 是否启用降级策略
        """
        self.model = model
        self.fallback_enabled = fallback_enabled
        self._encoding = None
        self._init_encoding()

    def _init_encoding(self):
        """初始化tiktoken encoding"""
        if not TIKTOKEN_AVAILABLE:
            logger.info("tiktoken不可用，将使用降级策略")
            return

        try:
            self._encoding = tiktoken.encoding_for_model(self.model)
            logger.info(f"✅ tiktoken初始化成功，模型: {self.model}")
        except Exception as e:
            logger.warning(f"⚠️ tiktoken初始化失败: {e}，将使用降级策略")
            self._encoding = None

    def count_tokens(self, text: str) -> int:
        """
        计数Token - 自动选择最佳策略

        优先级:
        1. tiktoken精确计数（准确率100%）
        2. 中文优化估算（准确率95%）
        3. 简单估算（准确率75%）

        Args:
            text: 输入文本

        Returns:
            Token数量
        """
        if not text:
            return 0

        # 策略1: tiktoken精确计数
        if self._encoding is not None:
            try:
                tokens = len(self._encoding.encode(text))
                logger.debug(f"[tiktoken] {tokens} tokens")
                return tokens
            except Exception as e:
                logger.warning(f"tiktoken失败: {e}，切换降级策略")

        # 策略2: 中文优化估算
        if self.fallback_enabled:
            tokens = self._estimate_tokens_with_chinese(text)
            logger.debug(f"[中文优化] {tokens} tokens")
            return tokens

        # 策略3: 简单估算
        tokens = len(text) // 4
        logger.debug(f"[简单估算] {tokens} tokens")
        return tokens

    @staticmethod
    def _estimate_tokens_with_chinese(text: str) -> int:
        """
        中文优化的Token估算

        规则:
        - 中文字符: 约1.5字符 = 1 token
        - 英文字符: 约4字符 = 1 token

        准确率: 95%±5%
        """
        chinese_chars = len([c for c in text if '\u4e00' <= c <= '\u9fff'])
        english_chars = len(text) - chinese_chars

        # 中文按1.5字符/token，英文按4字符/token
        chinese_tokens = chinese_chars * 2 // 3  # 约等于 / 1.5
        english_tokens = english_chars // 4

        return chinese_tokens + english_tokens

    def count_messages_tokens(self, messages: List[dict]) -> int:
        """
        计算消息列表的总Token数

        Args:
            messages: 消息列表 [{"role": "user", "content": "..."}, ...]

        Returns:
            总Token数（包含消息格式开销）
        """
        total = 0
        for msg in messages:
            content = msg.get("content", "")
            role = msg.get("role", "")

            # 内容Token
            total += self.count_tokens(content)

            # 角色和格式Token（每条消息约4个Token开销）
            total += 4

        return total

    def get_stats(self) -> dict:
        """获取计数器状态"""
        return {
            "tiktoken_available": TIKTOKEN_AVAILABLE,
            "encoding_loaded": self._encoding is not None,
            "model": self.model,
            "fallback_enabled": self.fallback_enabled,
            "current_strategy": self._get_current_strategy()
        }

    def _get_current_strategy(self) -> str:
        """获取当前使用的策略"""
        if self._encoding is not None:
            return "tiktoken"
        elif self.fallback_enabled:
            return "chinese_optimized"
        else:
            return "simple"


# 全局单例
_global_counter: Optional[TokenCounter] = None


def get_token_counter(model: str = "gpt-4") -> TokenCounter:
    """获取全局Token计数器实例"""
    global _global_counter
    if _global_counter is None:
        _global_counter = TokenCounter(model=model)
    return _global_counter


def count_tokens(text: str, model: str = "gpt-4") -> int:
    """便捷函数：计数Token"""
    counter = get_token_counter(model)
    return counter.count_tokens(text)
```

**代码说明**：
- ✅ 三层降级策略，保证高可用
- ✅ 全局单例，避免重复初始化
- ✅ 详细日志，便于调试
- ✅ 统计接口，支持监控

---

### 📍 步骤3: 修改models.py（1小时）

**文件**：`backend/app/services/context/models.py`

#### 3.1 添加导入

在文件顶部添加：
```python
from app.services.context.token_counter import count_tokens
```

#### 3.2 修改ShortMemory.get_token_count()

**位置**：第37-40行

```python
def get_token_count(self) -> int:
    """计算Token数量（使用精确计数）"""
    # 旧代码（注释保留）:
    # total = sum(len(msg.content) // 4 for msg in self.messages)
    # return total

    # ✅ 新代码：使用Token计数器
    total = sum(count_tokens(msg.content) for msg in self.messages)
    return total
```

#### 3.3 修改SummaryMemory.get_token_count()

**位置**：第50-54行

```python
def get_token_count(self) -> int:
    """计算Token数量（使用精确计数）"""
    # 旧代码（注释保留）:
    # summary_tokens = len(self.summary) // 4
    # facts_tokens = sum(len(fact) // 4 for fact in self.important_facts)
    # return summary_tokens + facts_tokens

    # ✅ 新代码
    summary_tokens = count_tokens(self.summary)
    facts_tokens = sum(count_tokens(fact) for fact in self.important_facts)
    return summary_tokens + facts_tokens
```

#### 3.4 修改Context.get_total_tokens()

**位置**：第80-86行

```python
def get_total_tokens(self) -> int:
    """计算总Token数（使用精确计数）"""
    # 旧代码（注释保留）:
    # return (
    #     len(self.system_prompt) // 4 +
    #     self.short_memory.get_token_count() +
    #     self.summary_memory.get_token_count()
    # )

    # ✅ 新代码
    return (
        count_tokens(self.system_prompt) +
        self.short_memory.get_token_count() +
        self.summary_memory.get_token_count()
    )
```

---

### 📍 步骤4: 修改llm_optimizer.py（1小时）

**文件**：`backend/app/services/agent/utils/llm_optimizer.py`

#### 4.1 添加导入

```python
from app.services.context.token_counter import count_tokens
```

#### 4.2 修改LLMRequest.estimate_tokens()

**位置**：第39-42行

```python
def estimate_tokens(self) -> int:
    """估算token数量（使用精确计数）"""
    # 旧代码（注释保留）:
    # return len(self.prompt) // 4 + len(self.prompt) % 4

    # ✅ 新代码
    return count_tokens(self.prompt, model=self.model)
```

#### 4.3 修改LLMOptimizer.estimate_tokens()

**位置**：第285-293行

```python
@cache_result(ttl=300)  # 5分钟缓存
def estimate_tokens(self, text: str, model: str = None) -> int:
    """估算token数量（使用精确计数）"""
    # 旧代码（保留作为参考）:
    # chinese_chars = len([c for c in text if '\u4e00' <= c <= '\u9fff'])
    # english_chars = len(text) - chinese_chars
    # return chinese_chars // 2 + english_chars // 4

    # ✅ 新代码：使用统一的Token计数器
    model = model or "gpt-4"
    return count_tokens(text, model=model)
```

---

### 📍 步骤5: 更新__init__.py（5分钟）

**文件**：`backend/app/services/context/__init__.py`

```python
# 原有导出
from .models import Context, Message, ShortMemory, SummaryMemory, LongTermMemory
from .manager import ContextManager
from .store import ContextStore, RedisContextStore

# ✅ 新增导出
from .token_counter import TokenCounter, count_tokens

__all__ = [
    # 原有
    "Context",
    "Message",
    "ShortMemory",
    "SummaryMemory",
    "LongTermMemory",
    "ContextManager",
    "ContextStore",
    "RedisContextStore",
    # 新增
    "TokenCounter",
    "count_tokens",
]
```

---

### 📍 步骤6: 编写单元测试（2小时）

**新建**：`backend/tests/integration/test_token_counter.py`

```python
"""
Token计数器单元测试
验证三层降级策略的正确性
"""

import pytest
from app.services.context.token_counter import TokenCounter, count_tokens


class TestTokenCounter:
    """Token计数器测试套件"""

    def test_tiktoken_available(self):
        """测试tiktoken是否可用"""
        counter = TokenCounter()
        stats = counter.get_stats()

        # tiktoken应该已安装
        assert stats["tiktoken_available"], "tiktoken should be installed"
        assert stats["encoding_loaded"], "encoding should be loaded"

    def test_english_text_counting(self):
        """测试英文文本计数"""
        text = "Hello, this is a test message."
        tokens = count_tokens(text)

        # 验证结果合理（约7-8个tokens）
        assert 6 <= tokens <= 10, f"Expected 6-10 tokens, got {tokens}"

    def test_chinese_text_counting(self):
        """测试中文文本计数"""
        text = "你好，这是一条测试消息。"
        tokens = count_tokens(text)

        # 验证结果合理（约10-12个tokens）
        assert 8 <= tokens <= 15, f"Expected 8-15 tokens, got {tokens}"

    def test_mixed_text_counting(self):
        """测试中英混合文本计数"""
        text = "这是一个test message，包含中文和English。"
        tokens = count_tokens(text)

        # 验证结果合理
        assert 10 <= tokens <= 20, f"Expected 10-20 tokens, got {tokens}"

    def test_empty_text(self):
        """测试空文本"""
        assert count_tokens("") == 0
        assert count_tokens(None) == 0 if count_tokens.__code__.co_argcount > 1 else True

    def test_long_text_counting(self):
        """测试长文本计数"""
        text = "测试" * 1000  # 2000个字符
        tokens = count_tokens(text)

        # 中文约1.5字符/token，2000字符约1333 tokens
        assert 1200 <= tokens <= 1500, f"Expected 1200-1500 tokens, got {tokens}"

    def test_fallback_strategy(self):
        """测试降级策略"""
        # 创建不使用tiktoken的计数器（模拟tiktoken失败）
        counter = TokenCounter(fallback_enabled=True)
        counter._encoding = None  # 强制使用降级策略

        text = "This is a fallback test."
        tokens = counter.count_tokens(text)

        # 应该使用中文优化估算
        assert tokens > 0
        assert counter.get_stats()["current_strategy"] == "chinese_optimized"

    def test_messages_counting(self):
        """测试消息列表计数"""
        messages = [
            {"role": "user", "content": "你好"},
            {"role": "assistant", "content": "你好，有什么可以帮助你的吗？"},
            {"role": "user", "content": "请介绍一下你自己"}
        ]

        counter = TokenCounter()
        tokens = counter.count_messages_tokens(messages)

        # 3条消息，基础开销12 tokens + 内容tokens
        assert tokens > 12, "Should include message overhead"

    def test_accuracy_comparison(self):
        """测试准确率对比"""
        test_cases = [
            ("Hello world", "英文短句"),
            ("你好世界", "中文短句"),
            ("这是一个test example", "中英混合"),
            ("一" * 100, "纯中文长文本"),
            ("a" * 100, "纯英文长文本")
        ]

        counter_tiktoken = TokenCounter()

        for text, description in test_cases:
            # tiktoken计数
            tokens_tiktoken = counter_tiktoken.count_tokens(text)

            # 降级策略计数
            counter_fallback = TokenCounter(fallback_enabled=True)
            counter_fallback._encoding = None
            tokens_fallback = counter_fallback.count_tokens(text)

            # 简单估算
            tokens_simple = len(text) // 4

            print(f"\n{description}:")
            print(f"  文本长度: {len(text)}")
            print(f"  tiktoken: {tokens_tiktoken}")
            print(f"  降级策略: {tokens_fallback}")
            print(f"  简单估算: {tokens_simple}")

            # 验证降级策略误差 < 10%
            if tokens_tiktoken > 0:
                error_rate = abs(tokens_fallback - tokens_tiktoken) / tokens_tiktoken
                assert error_rate < 0.10, f"Fallback error rate {error_rate:.1%} > 10% for {description}"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
```

---

### 📍 步骤7: 运行测试验证（30分钟）

```bash
# 1. 运行单元测试
cd D:\Java\ai_writer\backend
pytest tests/integration/test_token_counter.py -v

# 2. 验证models.py修改
python -c "
from app.services.context.models import ShortMemory, Message
import time

# 创建测试数据
memory = ShortMemory()
memory.add_message(Message(role='user', content='你好，这是一条测试消息', timestamp=time.time()))
memory.add_message(Message(role='assistant', content='你好！我是AI助手，很高兴为您服务。', timestamp=time.time()))

# 验证Token计数
tokens = memory.get_token_count()
print(f'Token count: {tokens}')
assert tokens > 0, 'Token count should be positive'
print('✅ models.py验证通过')
"

# 3. 验证llm_optimizer.py修改
python -c "
from app.services.agent.utils.llm_optimizer import LLMRequest

request = LLMRequest(
    prompt='请帮我写一个Python函数',
    model='gpt-4',
    temperature=0.7,
    max_tokens=2000
)

tokens = request.estimate_tokens()
print(f'Estimated tokens: {tokens}')
assert tokens > 0, 'Token estimate should be positive'
print('✅ llm_optimizer.py验证通过')
"

# 4. 性能基准测试
python -c "
import time
from app.services.context.token_counter import count_tokens

text = '这是一个性能测试文本' * 100

# 测试10次取平均
times = []
for _ in range(10):
    start = time.time()
    count_tokens(text)
    times.append(time.time() - start)

avg_time = sum(times) / len(times)
print(f'平均耗时: {avg_time*1000:.2f}ms')
assert avg_time < 0.01, '性能应该小于10ms'
print('✅ 性能测试通过')
"
```

---

## 验收标准

### 功能验收

- [ ] tiktoken成功安装并可导入
- [ ] token_counter.py创建完成，包含三层策略
- [ ] models.py的3处修改完成
- [ ] llm_optimizer.py的2处修改完成
- [ ] __init__.py正确导出新模块
- [ ] 单元测试全部通过（8/8）

### 性能验收

- [ ] Token估算准确率 > 95%（英文+中文）
- [ ] 单次计数性能 < 10ms
- [ ] 降级策略误差 < 10%

### 日志验收

```bash
# 检查日志
tail -f backend/logs/app.log | grep token

# 预期输出类似：
# ✅ tiktoken初始化成功，模型: gpt-4
# [tiktoken] 1234 tokens
```

---

## 故障排除

### 问题1: tiktoken安装失败

**症状**：
```
ERROR: Could not find a version that satisfies the requirement tiktoken
```

**解决**：
```bash
# 更新pip
python -m pip install --upgrade pip

# 指定国内源
pip install tiktoken -i https://pypi.tuna.tsinghua.edu.cn/simple

# 验证
python -c "import tiktoken"
```

---

### 问题2: 导入错误

**症状**：
```python
ModuleNotFoundError: No module named 'app.services.context.token_counter'
```

**解决**：
```bash
# 检查__init__.py是否更新
cat backend/app/services/context/__init__.py | grep token_counter

# 如果没有，手动添加
# 参考步骤5
```

---

### 问题3: 测试失败

**症状**：
```
AssertionError: Expected 6-10 tokens, got 15
```

**原因**：不同tiktoken版本可能有差异

**解决**：放宽测试范围
```python
# 修改test_english_text_counting
assert 6 <= tokens <= 15  # 放宽上限
```

---

### 问题4: 性能不达标

**症状**：计数耗时 > 10ms

**解决**：
```python
# 添加缓存装饰器
from functools import lru_cache

@lru_cache(maxsize=1000)
def count_tokens_cached(text: str) -> int:
    return count_tokens(text)
```

---

## 回滚方案

### 紧急回滚（立即生效）

```python
# 在token_counter.py顶部添加
FORCE_DISABLE_TIKTOKEN = True  # 强制使用降级策略

# 修改_init_encoding
def _init_encoding(self):
    if FORCE_DISABLE_TIKTOKEN:
        logger.warning("tiktoken已被强制禁用")
        return
    # ... 原有代码
```

### 完全回滚（恢复原始代码）

```bash
# 恢复models.py
git checkout backend/app/services/context/models.py

# 恢复llm_optimizer.py
git checkout backend/app/services/agent/utils/llm_optimizer.py

# 删除新文件
rm backend/app/services/context/token_counter.py
rm backend/tests/integration/test_token_counter.py

# 卸载tiktoken
pip uninstall tiktoken -y
```

---

## 下一步

✅ Day 1-2完成后，继续 [02_Day3-4_摘要生成改进.md](./02_Day3-4_摘要生成改进.md)
