# Agent数据截断问题修复方案

## 问题总结
Agent虽然成功检索到数据，但由于多层截断，最终AI收到的是严重残缺的信息，导致回答"找不到信息"。

## 修复优先级

### 🔥 优先级1：放宽工具返回的初始截断限制
**目标**：让工具返回更完整的数据

```python
# langgraph_agent.py:380 - RAG检索
- "content": result['content_text'][:500]  # ❌ 太小
+ "content": result['content_text'][:2000]  # ✅ 增加到2000

# langgraph_agent.py:253 - 章节内容
- "content": chapter.content[:2000]  # ❌ 对于长章节不够
+ "content": chapter.content[:5000]  # ✅ 增加到5000
```

**风险**：Token消耗增加，但必要（否则功能完全不可用）

---

### 🔥 优先级2：智能压缩而非暴力截断
**目标**：保留关键信息，而不是简单截断

```python
# langgraph_agent.py:511-556 _compress_task_result

修改前（第546行）：
return f"[章节内容摘要]\n{task_result[:200]}...\n{task_result[-100:]}"

修改后：
1. 提取章节的关键段落（标题、开头、结尾、对话）
2. 使用AI生成智能摘要（保留关键情节和人物信息）
3. 保留用户查询相关的上下文
```

**示例实现**：
```python
def _smart_compress_chapter(chapter_content: str, user_query: str, max_length: int = 1000) -> str:
    """智能压缩章节内容"""
    # 1. 提取关键部分
    lines = chapter_content.split('\n')
    key_parts = []

    # 开头（前500字）
    key_parts.append(f"【章节开头】\n{chapter_content[:500]}")

    # 结尾（后300字）
    if len(chapter_content) > 800:
        key_parts.append(f"【章节结尾】\n{chapter_content[-300:]}")

    # 2. 查询相关段落（简单关键词匹配）
    query_keywords = user_query.split()[:3]  # 取前3个关键词
    relevant_lines = []
    for line in lines:
        if any(kw in line for kw in query_keywords):
            relevant_lines.append(line)
            if len(relevant_lines) >= 5:  # 最多5行相关内容
                break

    if relevant_lines:
        key_parts.append(f"【相关内容】\n" + '\n'.join(relevant_lines))

    compressed = '\n\n'.join(key_parts)

    # 如果还是太长，截断到max_length
    if len(compressed) > max_length:
        return compressed[:max_length] + "...[后续内容省略]"

    return compressed
```

---

### ⚡ 优先级3：减少不必要的Summarization调用
**目标**：对于简单查询，直接使用RAG结果，不经过Summarization压缩

```python
# langgraph_agent.py:2274 _build_final_response

修改前：
# 分析类任务，可能需要格式化
logger.info(f"[Response] 单个分析任务({tool_name})，使用AI格式化")
return await self._ai_summarization(task_results, message, on_content)

修改后：
# 判断是否需要Summarization
if self._is_simple_query(message):
    # 简单查询：直接返回工具结果
    logger.info(f"[Response] 简单查询，直接返回工具结果")
    return task["result"]
else:
    # 复杂查询：使用AI整合
    logger.info(f"[Response] 复杂查询，使用AI整合")
    return await self._ai_summarization(task_results, message, on_content)
```

**判断逻辑**：
```python
def _is_simple_query(self, message: str) -> bool:
    """判断是否为简单查询"""
    simple_patterns = [
        "是什么", "有什么", "叫什么", "怎么样",
        "总结", "概括", "列出"
    ]
    return any(pattern in message for pattern in simple_patterns)
```

---

### 🎯 优先级4：提高max_context_length限制
**目标**：让AI能看到更多上下文

```python
# langgraph_agent.py:2335
- max_context_length=3000
+ max_context_length=8000  # Gemini 2.5 Pro可以处理更多tokens
```

---

## 实施建议

### 阶段1：快速修复（5分钟）
1. 修改第380行：RAG内容限制 500 → 2000
2. 修改第253行：章节内容限制 2000 → 5000
3. 修改第2335行：上下文限制 3000 → 8000

**预期效果**：问题立即缓解，但可能仍有压缩损失

---

### 阶段2：优化压缩（30分钟）
1. 实现`_smart_compress_chapter`（智能章节压缩）
2. 实现`_smart_compress_rag`（智能RAG压缩）
3. 修改`_compress_task_result`使用智能压缩

**预期效果**：保留关键信息，回答质量显著提升

---

### 阶段3：减少Summarization（15分钟）
1. 实现`_is_simple_query`判断逻辑
2. 修改`_build_final_response`跳过简单查询的Summarization
3. 测试性能提升

**预期效果**：简单查询响应时间大幅缩短（从60-90秒降到15-20秒）

---

## 测试验证

修复后重新测试：

### 测试1：简单查询
```
段融的金手指能力是什么？具体有什么效果？
```
**预期**：
- ✅ 能找到完整的金手指描述
- ✅ 响应时间 < 20秒
- ✅ 使用flash模型

### 测试2：总结查询
```
帮我总结一下前两章的主要内容，包括：1）主角设定 2）当前处境 3）主要冲突
```
**预期**：
- ✅ 能完整总结两章内容
- ✅ 响应时间 < 30秒
- ✅ 内容完整且准确

---

## 长期优化（可选）

1. **智能分块**：对于超长章节，使用滑动窗口+重叠分块
2. **向量召回**：RAG检索时，使用更高的top_k，然后rerank
3. **缓存机制**：常见查询结果缓存，避免重复处理
4. **流式压缩**：边读取边压缩，而不是一次性加载

---

## 成本评估

| 优化项 | Token增加 | 成本增加（单次） | 性价比 |
|--------|----------|----------------|--------|
| 工具返回增大 | +3000 | +$0.0001 | ⭐⭐⭐⭐⭐ |
| 智能压缩 | -1000 | -$0.00005 | ⭐⭐⭐⭐⭐ |
| 跳过Summarization | -2000 | -$0.0001 | ⭐⭐⭐⭐⭐ |
| 上下文增大 | +5000 | +$0.0002 | ⭐⭐⭐⭐ |

**总成本增加**：约 $0.0001/次查询（可忽略不计）
**收益**：功能从"完全不可用"变为"正常可用"

---

## 总结

**根本原因**：过度的截断和压缩导致AI收到的数据完全不足以回答问题

**核心修复**：
1. 放宽初始截断限制（RAG 500→2000，章节 2000→5000）
2. 使用智能压缩代替暴力截断
3. 对简单查询跳过Summarization压缩

**预期效果**：
- 功能可用性：0% → 90%+
- 响应质量：❌ → ✅
- 响应时间：从60-90秒降到15-30秒
- 成本增加：可忽略不计

**建议**：立即实施阶段1修复（5分钟），然后逐步实施阶段2和3。
