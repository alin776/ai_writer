# P1 优化方案 - Planning优化和HTTP连接池

> **优先级：** P1（重要但不紧急）
> **预期效果：** 在P0基础上再提升10-15秒
> **实施时间：** 2-3小时

## 🎯 优化目标

在P0优化基础上，进一步提升：
1. **简单任务跳过Planning** - 减少15-20秒
2. **HTTP连接池优化** - 减少2-5秒
3. **实现缓存机制** - 重复请求加速90%+

---

## 优化1：简单任务跳过Planning

### 问题分析

**当前状态：**
```
第二次请求："我刚才说了什么？"（简单问题）
→ Planning阶段仍然耗时：20秒
→ 完全不需要AI规划
```

**日志证据：**
```
2025-11-04 19:45:20 - Planning开始
2025-11-04 19:45:41 - Planning完成 (20秒)

规划结果：
1. 分析用户请求（识别询问历史）
2. 评估工具（确认无历史工具）
3. 准备回复（解释限制）

→ 这些步骤完全不需要AI，可以直接判断
```

**适合跳过Planning的场景：**
- 简单问答（"什么是XX"、"怎么做XX"）
- 历史查询（"我刚才说了什么"、"上次的结果"）
- 状态查询（"当前进度"、"有哪些章节"）
- 工具类查询（"第X章的内容"）

### 解决方案：规则判断 + 快速响应

**文件：** `backend/app/services/agent/langgraph_agent.py`

**步骤1：添加规则判断函数**

在类外添加（或作为类方法）：

```python
def _is_simple_query(message: str) -> bool:
    """判断是否是简单查询，可以跳过AI规划

    Args:
        message: 用户消息

    Returns:
        True if 简单查询
    """
    # 转小写方便匹配
    msg_lower = message.lower()

    # 简单问答模式
    simple_patterns = [
        # 历史查询
        "我刚才说", "我之前", "上次", "上一次", "历史",
        "刚才的", "之前的", "上个",

        # 状态查询
        "有哪些", "有几个", "有多少",
        "当前", "现在",

        # 工具类查询（按序号）
        "第一章", "第二章", "第三章", "第四章", "第五章",
        "第1章", "第2章", "第3章", "第4章", "第5章",
    ]

    # 检查是否包含简单模式
    for pattern in simple_patterns:
        if pattern in msg_lower:
            return True

    # 短消息（<20字）且包含疑问词
    if len(message) < 20:
        question_words = ["什么", "哪", "谁", "怎么", "为什么", "吗", "？", "?"]
        if any(word in message for word in question_words):
            return True

    return False


def _generate_simple_response_plan(message: str, work_id: str, chapter_id: str) -> Dict[str, Any]:
    """为简单查询生成快速响应计划

    Args:
        message: 用户消息
        work_id: 作品ID
        chapter_id: 章节ID

    Returns:
        计划数据
    """
    msg_lower = message.lower()

    # 历史查询
    if any(word in msg_lower for word in ["刚才", "之前", "上次", "历史"]):
        return {
            "user_intent": "查询对话历史",
            "tasks": [
                {
                    "task_id": 1,
                    "description": "直接回答：当前系统暂不支持历史查询",
                    "tool": "auto",
                    "estimated_time": "1秒"
                }
            ]
        }

    # 章节序号查询（如"第2章"）
    for i in range(1, 20):
        if f"第{i}章" in message or f"第{i}章" in message:
            return {
                "user_intent": f"获取第{i}章内容",
                "tasks": [
                    {
                        "task_id": 1,
                        "description": f"获取第{i}章内容",
                        "tool": "get_chapter_by_order_tool",
                        "params": {"chapter_order": i},
                        "estimated_time": "2秒"
                    }
                ]
            }

    # 状态查询
    if any(word in msg_lower for word in ["有哪些", "有几个", "有多少"]):
        return {
            "user_intent": "查询作品信息",
            "tasks": [
                {
                    "task_id": 1,
                    "description": "获取作品上下文信息",
                    "tool": "get_context_tool",
                    "estimated_time": "2秒"
                }
            ]
        }

    # 默认：获取上下文
    return {
        "user_intent": "理解用户请求",
        "tasks": [
            {
                "task_id": 1,
                "description": "获取作品上下文",
                "tool": "get_context_tool",
                "estimated_time": "2秒"
            }
        ]
    }
```

**步骤2：修改Planning阶段**

**位置：** `langgraph_agent.py:1526-1652`

```python
# ========== 阶段1: 规划（Planning） ==========
logger.info(f"[Planning] 开始规划: {message[:50]}...")

# ====== 新增：检查是否简单查询 ======
if _is_simple_query(message):
    logger.info("[Planning] 检测到简单查询，跳过AI规划，使用规则生成计划")

    plan_data = _generate_simple_response_plan(
        message=message,
        work_id=work_id,
        chapter_id=chapter_id
    )

    logger.info(f"[Planning] 规则生成计划成功，共{len(plan_data['tasks'])}个任务")

    # 回调：发送规划
    if on_plan:
        await on_plan(plan_data)

else:
    # ====== 原有逻辑：执行AI规划 ======
    logger.info("[Planning] 复杂任务，执行AI规划")

    # 构建规划prompt（包含历史）
    history_section = ""
    if conversation_history:
        history_section = f"""
【对话历史】
{conversation_history}

"""

    plan_prompt = f"""你是专业的AI写作助手。{history_section}用户请求如下：
    ...
    """

    try:
        plan_result = await self._generate_text(
            plan_prompt,
            temperature=0.3,
            max_tokens=1000,
            task_type=TaskType.STORY_PLANNING
        )
        plan_text = plan_result.get("text", "").strip()

        # 解析规划JSON
        plan_data = self._extract_json_from_text(plan_text)

    except Exception as e:
        logger.error(f"[Planning Agent] 执行失败: {e}", exc_info=True)
        # ... 错误处理
# ====================================

# 继续执行任务...
```

**预期效果：**
```
简单查询（如"我刚才说了什么"）：
- 原Planning: 20秒 (AI规划)
- 新Planning: <0.1秒 (规则判断)
- 提升: 99.5%

复杂任务（如"续写第5章"）：
- 仍执行AI规划，不受影响
```

---

## 优化2：HTTP连接池优化

### 问题分析

**当前代码：** `backend/app/services/ai/http_ai_service.py:67-80`

```python
self.client = httpx.AsyncClient(
    headers={...},
    timeout=httpx.Timeout(timeout_value, connect=10.0),
    http2=False,  # ← 未启用HTTP/2
    # ❌ 缺少连接池配置
)
```

**问题：**
- 每个HTTPAIService实例创建自己的client
- 没有连接池限制
- 未启用HTTP/2
- 可能重复建立TCP连接

### 解决方案：优化连接池配置

**注意：** 不实施全局单例（docs中建议的方案），因为：
- 当前每个请求已经复用同一个HTTPAIService实例
- 全局单例会增加复杂度
- 只需优化连接池参数即可

**步骤：修改HTTPAIService初始化**

```python
# backend/app/services/ai/http_ai_service.py:67-80

# 原代码
self.client = httpx.AsyncClient(
    headers={...},
    timeout=httpx.Timeout(timeout_value, connect=10.0),
    follow_redirects=True,
    http2=False,
)

# 修改为
self.client = httpx.AsyncClient(
    headers={
        "User-Agent": "okhttp/4.12.0",
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
    },
    timeout=httpx.Timeout(
        timeout_value,
        connect=10.0
    ),
    # ====== 新增：连接池配置 ======
    limits=httpx.Limits(
        max_keepalive_connections=20,  # 保持20个连接
        max_connections=50,             # 最多50个连接
        keepalive_expiry=30.0          # 连接保持30秒
    ),
    http2=True,  # 启用HTTP/2（改为True）
    # ==============================
    follow_redirects=True,
)
```

**配置说明：**
```python
max_keepalive_connections=20
# Agent场景通常是单用户串行请求
# 20个足够应对偶尔的并发
# 不要设置过大（如50），会浪费资源

max_connections=50
# 最大连接数限制
# 防止连接泄漏

keepalive_expiry=30.0
# 连接保持30秒
# 对话场景下，用户请求间隔通常<30秒

http2=True
# 启用HTTP/2多路复用
# 提升并发性能
```

**预期效果：**
```
首次请求：2-5秒（建立连接）
后续请求：0.1-0.5秒（复用连接）

连接复用率：60-80%
（取决于用户请求间隔）
```

---

## 优化3：实现缓存机制

### 问题分析

**当前代码：** `backend/app/services/ai/http_ai_service.py:139`

```python
# 生成了cache_key但未使用
cache_key = self._generate_cache_key(messages, self.model, temperature, max_tokens)

# 直接发起HTTP请求
async with self.client.stream("POST", url, ...) as response:
    # ...
```

### 解决方案：实现简单的内存缓存

**适用场景：**
- 重复的简单问答
- 相同的章节查询
- 但**不适用于创作类任务**（每次都需要新内容）

**步骤1：添加缓存管理器**

在 `http_ai_service.py` 顶部添加：

```python
from datetime import datetime, timedelta
from typing import Dict, Tuple, Optional

# 简单的内存缓存
_response_cache: Dict[str, Tuple[str, datetime]] = {}
_cache_ttl = timedelta(minutes=10)  # 缓存10分钟
```

**步骤2：修改 _stream_chat 方法**

```python
async def _stream_chat(
    self,
    messages: list,
    max_tokens: int = 1000,
    temperature: float = 0.7,
    task_type: Optional[TaskType] = None,
    use_cache: bool = True  # ← 新增参数
) -> AsyncGenerator[tuple[str, dict | None], None]:
    """通用流式聊天方法"""

    # ... 模型选择代码 ...

    # ====== 新增：检查缓存 ======
    cache_key = None
    if use_cache:
        cache_key = self._generate_cache_key(messages, model, temperature, max_tokens)

        # 检查缓存
        if cache_key in _response_cache:
            cached_content, cached_time = _response_cache[cache_key]

            # 检查是否过期
            if datetime.now() - cached_time < _cache_ttl:
                logger.info(f"[Cache] 命中缓存，key={cache_key[:16]}...")

                # 返回缓存内容（模拟流式）
                yield cached_content, None
                return
            else:
                # 过期，删除
                del _response_cache[cache_key]
                logger.info(f"[Cache] 缓存已过期，key={cache_key[:16]}...")
    # ===========================

    url = f"{self.base_url}/chat/completions"
    # ... 准备请求 ...

    try:
        total_content = ""
        async with self.client.stream("POST", url, json=payload, headers=headers) as response:
            # ... 流式接收 ...

            async for line in response.aiter_lines():
                # ... 解析数据 ...
                if content:
                    chunk_count += 1
                    total_content += content
                    yield content, None

        # ====== 新增：存入缓存 ======
        if use_cache and cache_key and total_content:
            # 检查缓存大小，避免内存溢出
            if len(_response_cache) > 100:
                # 删除最老的缓存
                oldest_key = min(
                    _response_cache.keys(),
                    key=lambda k: _response_cache[k][1]
                )
                del _response_cache[oldest_key]
                logger.info(f"[Cache] 缓存已满，删除最老条目")

            _response_cache[cache_key] = (total_content, datetime.now())
            logger.info(
                f"[Cache] 存入缓存，key={cache_key[:16]}..., "
                f"size={len(total_content)}, total_cached={len(_response_cache)}"
            )
        # ===========================

        # ... 成本追踪等 ...

    except Exception as e:
        # ... 错误处理 ...
```

**步骤3：某些场景禁用缓存**

在调用处指定 `use_cache=False`：

```python
# 创作类任务不使用缓存
if tool_name == "continue_writing_tool":
    async for chunk, _ in self.ai_service._stream_chat(
        messages=[...],
        max_tokens=2000,
        temperature=0.8,
        task_type=TaskType.CONTENT_CREATION,
        use_cache=False  # ← 禁用缓存
    ):
        # ...

# Planning阶段不使用缓存（每次上下文不同）
plan_result = await self._generate_text(
    plan_prompt,
    temperature=0.3,
    max_tokens=1000,
    task_type=TaskType.STORY_PLANNING,
    use_cache=False  # ← 禁用缓存
)

# Summarization不使用缓存（每次结果不同）
async for chunk, _ in self.ai_service._stream_chat(
    messages=[{"role": "user", "content": summary_prompt}],
    max_tokens=2000,
    temperature=0.7,
    task_type=TaskType.SUMMARIZATION,
    use_cache=False  # ← 禁用缓存
):
    # ...
```

**预期效果：**
```
重复的简单查询（如"第2章的内容"）：
- 首次: 5-10秒
- 重复: <0.1秒（命中缓存）
- 提升: 99%

创作类任务：
- 不使用缓存，不受影响
```

---

## 📊 综合效果预测

### 在P0基础上的进一步提升

**假设P0已实施，当前耗时30秒**

```
P0优化后: 30秒

P1优化后：
- 简单查询: 5-10秒（跳过Planning）
- 复杂查询: 25-28秒（连接池优化）
- 重复查询: <1秒（缓存命中）

平均提升: 10-15秒
```

### 不同场景的总耗时

| 场景 | 当前(P0前) | P0后 | P1后 | 总提升 |
|------|-----------|------|------|--------|
| **简单查询** | 60秒 | 20秒 | **5-10秒** | 83-92% |
| **首次复杂查询** | 136秒 | 30秒 | **25-28秒** | 79-82% |
| **重复查询** | 136秒 | 30秒 | **<1秒** | 99%+ |

---

## ✅ 实施检查清单

### 优化1：简单任务跳过Planning
- [ ] 添加 `_is_simple_query` 函数
- [ ] 添加 `_generate_simple_response_plan` 函数
- [ ] 修改Planning阶段添加规则判断
- [ ] 测试简单查询（如"第2章"、"我刚才说什么"）
- [ ] 测试复杂查询（如"续写第5章"）
- [ ] 验证日志中是否跳过AI规划

### 优化2：HTTP连接池
- [ ] 修改 `http_ai_service.py` 的client初始化
- [ ] 添加 `limits` 配置
- [ ] 修改 `http2=True`
- [ ] 重启服务
- [ ] 测试多次请求验证连接复用
- [ ] 检查日志中的连接建立时间

### 优化3：缓存机制
- [ ] 添加缓存相关imports
- [ ] 初始化缓存字典
- [ ] 修改 `_stream_chat` 添加缓存逻辑
- [ ] 在创作类任务禁用缓存
- [ ] 测试重复查询
- [ ] 验证缓存命中率

---

## 🔍 验证方法

### 1. 检查日志

```bash
# 检查Planning跳过
grep "跳过AI规划" INFO.md

# 检查缓存命中
grep "\[Cache\]" INFO.md

# 检查连接复用
grep "keep-alive" INFO.md
```

### 2. 性能测试

```python
# 测试脚本
import time
import requests

# 测试1：简单查询
start = time.time()
response = requests.post("http://localhost:8000/api/v1/agent/chat/stream", json={
    "message": "第2章的内容",
    "work_id": "xxx",
    "chapter_id": "xxx"
})
print(f"简单查询耗时: {time.time() - start:.2f}秒")

# 测试2：重复查询（验证缓存）
start = time.time()
response = requests.post("http://localhost:8000/api/v1/agent/chat/stream", json={
    "message": "第2章的内容",  # 相同请求
    "work_id": "xxx",
    "chapter_id": "xxx"
})
print(f"重复查询耗时: {time.time() - start:.2f}秒")
```

---

## ⚠️ 注意事项

1. **简单任务判断**：可能有误判，需要持续优化规则
2. **缓存策略**：创作类任务禁用缓存，避免返回相同内容
3. **缓存大小**：限制在100条，避免内存溢出
4. **连接池大小**：根据实际并发调整，不要设置过大
5. **回滚计划**：保留原配置，出现问题可快速回滚

---

## 📁 修改文件清单

| 文件 | 修改内容 | 预期提升 |
|------|---------|---------|
| `backend/app/services/agent/langgraph_agent.py` | 添加简单查询判断 | 15-20秒 |
| `backend/app/services/ai/http_ai_service.py` | 连接池配置 + 缓存 | 2-5秒 + 重复请求99% |

---

## 下一步

完成P1优化后，查看 [实施步骤清单](./实施步骤清单.md) 开始实际操作
