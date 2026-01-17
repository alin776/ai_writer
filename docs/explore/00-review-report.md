# Explore 设计 Review 报告 (V4)

## 0. 第四轮 Review 发现的问题（最新 - 严重）

### 0.1 数据流设计缺失 ❌ 严重

**发现**：`smart_continue` 没有 `context` 参数！

**实际接口**（editor_tools.py:630）：
```python
async def smart_continue(
    chapter_id: str,
    chapter_content: Optional[str] = None,  # 只有这个！
    user_requirement: Optional[str] = None,
    word_count: int = 500,
    user_id: Optional[str] = None
) -> str:
```

**设计文档错误**（06-output.md:278）：
```python
# 错误的使用方式！
await smart_continue(
    work_id="work_123",
    chapter_order=6,
    context=context  # 这个参数不存在！
)
```

**修正方案**：

1. Explore 结果通过 TaskRunner 的 `context` 参数传递
2. TaskRunner 内部调用 `build_context_for_task()` 转换
3. 转换后的字符串通过 `chapter_content` 传递给 smart_continue

```python
# TaskRunner._prepare_tool_params 中添加
elif tool_name == "smart_continue":
    # 如果 context 中有 explore_result，使用它构建 chapter_content
    if context_payload and "explore_result" in context_payload:
        from app.services.agent.tools.explore_tools import build_context_for_task
        context_param = build_context_for_task(context_payload["explore_result"])
    else:
        context_param = self._extract_context_param(params, context)
    return {
        "chapter_content": context_param,
        ...
    }
```

---

### 0.2 前端事件未处理 ⚠️

**发现**：前端没有处理 `explore_analysis` 事件类型。

**需要修改的文件**：
- `src/services/agentApi.ts` - 添加 case 处理
- `src/hooks/useAgentChat.ts` - 添加事件处理逻辑
- `src/hooks/useAgentChatStream.ts` - 添加事件处理逻辑

**修正**：前端需要在 switch case 中添加：
```typescript
case 'explore_analysis':
  callbacks.onFlowEvent?.({
    type: 'explore_analysis',
    stepId: data.step_id,
    roundIdx: data.round_idx,
    reasoning: data.reasoning,
    stats: data.stats,
    sufficient: data.sufficient,
    nextActions: data.next_actions,
    timestamp: data.timestamp
  });
  break;
```

---

### 0.3 TaskRunner 集成缺失 ⚠️

**发现**：设计文档没有说明 `build_context_for_task` 在哪里调用。

**补充设计**：

```python
# execution/task_runner.py 修改

async def execute_task(self, task, ...):
    tool_name = task.get("tool")

    # explore_content 完成后，保存结果到 state
    if tool_name == "explore_content":
        result = await self._call_tool_via_registry(...)
        # 保存到 state 供后续任务使用
        explore_result = json.loads(result)
        state["explore_result"] = explore_result
        state["explore_context"] = build_context_for_task(explore_result)
        return result

    # smart_continue 使用 explore 结果
    elif tool_name == "smart_continue":
        if state.get("explore_context"):
            params["chapter_content"] = state["explore_context"]
        ...
```

---

### 0.4 改动清单更新

新增前端修改：

| 文件 | 改动 | 代码量 |
|------|------|--------|
| `src/services/agentApi.ts` | 添加 explore_analysis case | ~15行 |
| `src/hooks/useAgentChat.ts` | 添加事件处理 | ~20行 |
| `src/hooks/useAgentChatStream.ts` | 添加事件处理 | ~20行 |

**后端新增**：~510行
**前端新增**：~55行
**总计**：~565行

---

## 1. 第三轮 Review 发现的问题（已修正）

### 0.1 ChapterRepository.get_by_order 不存在 ❌ 已修正

**发现**：设计文档中使用了 `ChapterRepository.get_by_order(session, work_id, chapter_order)`，但这个类/方法不存在。

**实际代码获取章节方式**（langgraph_tools.py:1040-1055）：
```python
from app.services.work_service import WorkService

async with AsyncSessionLocal() as db:
    work_service = WorkService(db)
    work = await work_service.get_work_by_id(work_id, use_cache=True)

    if work and work.chapters:
        chapter_map = {ch.order: ch for ch in work.chapters}
        chapter = chapter_map.get(chapter_order)
```

**修正**：02-tools.md 已更新为正确的实现方式。

---

### 0.2 工具描述添加位置 ⚠️ 需要修正

**发现**：设计文档说添加到 `prompts/planning_prompts.py`，但实际工具描述统一管理在 `prompts/tool_descriptions.py`。

**修正**：应该在 `tool_descriptions.py` 中新增 `_get_explore_tools_section()` 函数。

---

### 0.3 段落级缓存实现方式 ⚠️ 需要明确

**发现**：设计文档提到需要段落级缓存，但未明确如何与现有 `ToolCache` 集成。

**补充设计**：
```python
# 在 tool_cache.py 中添加

PARAGRAPH_CACHE_PREFIX = "para_cache"

class ParagraphCache:
    """段落级缓存 - 独立于 ToolCache"""

    @staticmethod
    def get_key(work_id: str, chapter_order: int, para_start: int, para_end: int) -> str:
        return f"{PARAGRAPH_CACHE_PREFIX}:{work_id}:{chapter_order}:{para_start}-{para_end}"

    @staticmethod
    def read(key: str) -> Optional[str]:
        if redis_client.is_available():
            return redis_client.get(key)
        return _local_cache.get(key)

    @staticmethod
    def write(key: str, value: str, ttl_seconds: int = 600):
        if redis_client.is_available():
            redis_client.set(key, value, ttl_seconds)
        else:
            _local_cache.set(key, value, ttl=ttl_seconds)
```

---

### 0.4 接口参数验证结果 ✅

| 接口 | 验证结果 |
|------|----------|
| `_split_paragraphs(content)` → `List[Dict]` | ✅ 匹配 |
| `search_content` 返回 `snippet` 字段 | ✅ 匹配 |
| `get_writing_context` 参数 | ✅ 匹配（额外的 user_id/use_cache 可选） |
| `FlowEventBuilder` 方法 | ✅ 可直接复用 |
| `ParallelExecutor` 并发控制 | ✅ Semaphore(5) |
| `_retry_on_failure` 重试机制 | ✅ 可复用 |

---

## 1. 第一轮 Review 发现的问题（已修正）

| 问题 | 修正 |
|------|------|
| 工具重复定义 | 复用现有 search_content、get_writing_context、locate_content |
| 事件类型不兼容 | 融入现有 FlowEventBuilder 体系 |
| Planning 强制第一步 | AI 自主选择 |

---

## 2. 第二轮深度 Review 发现的新问题

### 2.1 段落解析逻辑 ✅ 可直接复用

**发现**：现有 `locate_tools.py` 中已有成熟的段落解析：

```python
# locate_tools.py:39-78
def _split_paragraphs(content: str) -> List[Dict]:
    # 支持 HTML 和纯文本
    # 返回 {index, text, preview}
```

**结论**：read_paragraph 可直接复用此函数，无需重新实现。

---

### 2.2 缓存系统 ⚠️ 需要补充设计

**发现**：现有缓存粒度是**工具级**，不支持**段落级**缓存。

**问题**：
- Explore 多轮调用同一段落，会重复读取
- 缓存键空间可能爆炸（work_id × chapter_id × paragraph_index）

**补充设计**：

```python
# 在 tool_cache.py 中添加
PARAGRAPH_CACHE_PREFIX = "para"

def get_paragraph_cache_key(chapter_id: str, para_start: int, para_end: int) -> str:
    """段落范围缓存键"""
    return f"{PARAGRAPH_CACHE_PREFIX}:{chapter_id}:{para_start}-{para_end}"

# TTL: 10分钟
# 淘汰策略: LRU, 最大 1000 个段落范围
```

---

### 2.3 大章节性能 ⚠️ 需要考虑

**发现**：若章节超过 100K 字符，`_split_paragraphs()` 正则匹配可能缓慢。

**补充设计**：

```python
# 在 read_paragraph 中添加保护
MAX_CHAPTER_SIZE = 200_000  # 200K 字符
MAX_PARAGRAPHS = 2000       # 最多 2000 个段落

if len(chapter_content) > MAX_CHAPTER_SIZE:
    # 分块处理，只解析目标段落附近的内容
    start_pos = max(0, paragraph_index * 500 - 5000)
    end_pos = min(len(chapter_content), paragraph_index * 500 + 5000)
    chunk = chapter_content[start_pos:end_pos]
    paragraphs = _split_paragraphs(chunk)
```

---

### 2.4 上下文传递格式 ⚠️ 需要明确

**发现**：smart_continue 的 context 参数没有固定格式，Explore 输出需要与之兼容。

**现有格式**（smart_continue）：
```python
context = chapter_content[-1000:]  # 简单截取
```

**Explore 输出格式建议**：
```python
{
    "explore_summary": "经过2轮探索，收集到...",  # AI 分析（辅助）

    # 以下为原文内容（精度零丢失）
    "chapters": {
        "5": {"title": "...", "content": "完整原文..."}
    },
    "worldview": {...},
    "evidences": [
        {"chapter_order": 3, "paragraph_index": 18, "text": "原文片段..."}
    ],
    "paragraphs": [
        {"chapter_order": 5, "paragraph_index": 25, "text": "原文...", "context_before": [...]}
    ]
}
```

**smart_continue 对接**：
```python
# 在 TaskRunner 中
if "explore_result" in context:
    explore = context["explore_result"]
    # 构建 context 字符串
    ctx_parts = []
    for ch in explore.get("chapters", {}).values():
        ctx_parts.append(f"【{ch['title']}】\n{ch['content']}")
    for ev in explore.get("evidences", []):
        ctx_parts.append(f"【第{ev['chapter_order']}章·第{ev['paragraph_index']}段】\n{ev['text']}")
    task.params["context"] = "\n\n".join(ctx_parts)
```

---

### 2.5 Planning Prompt 工具描述 ⚠️ 需要添加

**发现**：工具描述统一管理在 `tool_descriptions.py`，需要按现有格式添加。

**现有格式参考**：
```python
# tool_descriptions.py
- get_writing_context: 一站式获取创作上下文
  参数: chapter_orders, include, rag_query
  返回: {work_info, chapters[], worldview, rag_context[]}
  ✅ 使用示例: 续写前获取上下文
```

**explore_content 描述**：
```python
- explore_content: 深度探索工具（get_writing_context 的增强版）
  参数:
    - work_id: 作品ID（必需）
    - target_task: 目标任务描述（必需）
    - max_rounds: 最大探索轮数（默认5）
  返回: {
    explore_summary,      # AI 分析
    chapters,            # 完整章节原文
    worldview,           # 世界观设定
    evidences,           # 搜索证据片段
    paragraphs           # 精确读取的段落
  }

  ✅ 使用场景:
    - 任务涉及多个章节的关联分析
    - 需要深入理解人物关系、情节发展
    - 搜索结果需要原文验证

  ⚠️ 与 get_writing_context 的对比:
    - get_writing_context: 一次性获取，适合简单任务
    - explore_content: 多轮探索，适合复杂任务
```

---

### 2.6 并发控制 ✅ 现有架构支持

**发现**：现有 `ParallelExecutor` 已实现 Semaphore(5) 并发控制，Explore 可直接复用。

```python
# parallel_executor.py:91
semaphore = asyncio.Semaphore(self.max_concurrent)  # 默认5
```

**结论**：无需额外设计。

---

### 2.7 错误处理 ✅ 现有模式可复用

**发现**：现有 `_retry_on_failure()` 提供指数退避重试，Explore 可直接使用。

```python
# langgraph_tools.py:185-202
async def _retry_on_failure(func, *args, max_retries=3):
    # 指数退避重试
    await asyncio.sleep(2 ** retry_count)
```

**结论**：无需额外设计。

---

## 3. 更新后的改动清单

| 文件 | 改动类型 | 说明 | 代码量 |
|------|----------|------|--------|
| `tools/explore_tools.py` | 新增 | Explore 核心实现 | ~300行 |
| `langgraph_tools.py` | 修改 | 添加 read_paragraph | ~50行 |
| `prompts/tool_descriptions.py` | **修改** | 添加 explore_content 描述 | ~40行 |
| `prompts/planning_prompts.py` | 修改 | 导入新工具描述 | ~5行 |
| `execution/tool_executor.py` | 修改 | 添加工具调用支持 | ~20行 |
| `stream/flow_events.py` | 修改 | 添加事件 + 图标 | ~30行 |
| `utils/tool_cache.py` | **新增** | 段落级缓存支持 | ~30行 |

**总计**：~475行新代码

---

## 4. 验证清单（更新）

| 验证项 | 结果 | 说明 |
|--------|------|------|
| 是否引入新问题？ | ✅ | 复用现有工具，不引入问题 |
| 是否解决原问题？ | ✅ | 多轮探索 + 精度验证 |
| 修改完整性？ | ✅ | 补充了 tool_descriptions.py 和 tool_cache.py |
| 逻辑一致性？ | ✅ | 融入现有架构，格式一致 |
| 段落解析可行？ | ✅ | 复用现有 _split_paragraphs() |
| 缓存兼容？ | ✅ | 新增段落级缓存层 |
| 并发控制？ | ✅ | 复用现有 ParallelExecutor |
| 错误处理？ | ✅ | 复用现有 _retry_on_failure() |
| 大章节性能？ | ✅ | 添加分块保护逻辑 |
| 上下文对接？ | ✅ | 定义了输出格式和对接方式 |

---

## 5. 遗留问题（待开发时验证）

1. **大章节实际性能**：需要用 10 万字章节测试
2. **缓存淘汰策略**：LRU vs TTL 的选择
3. **Planning Agent 理解**：多轮机制的 Prompt 优化
