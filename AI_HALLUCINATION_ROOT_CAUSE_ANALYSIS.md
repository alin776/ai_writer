# AI生成内容严重错误 - 根因分析报告

## 📋 执行摘要

**问题描述**：用户询问"第28章讲了什么？有什么亮点？"，AI返回了完全错误的内容。
- **期望**：分析段融修炼内功、学习九州八宗的故事
- **实际**：返回了林寻在宁家演武场比武的故事
- **结论**：两个故事来自完全不同的小说，AI产生严重幻觉

---

## 🔍 深度调查结果

### 1. 数据库内容验证 ✅ 正确

**验证方法**：直接连接PostgreSQL数据库查询第28章内容

**查询结果**：
- 章节ID: `3eb38429-7cd9-4691-9661-bb74beaf3c6f`
- 标题: `第28章 九州八宗`
- 字数: `2041`
- 内容长度: `3068字符`
- 状态: `draft`

**关键词检查**：
| 关键词 | 状态 | 说明 |
|--------|------|------|
| 段融 | ✅ 存在 | 正确的主角 |
| 血鹿茸 | ✅ 存在 | 修炼道具 |
| 内息 | ✅ 存在 | 修炼体系 |
| 九州八宗 | ✅ 存在 | 世界观设定 |
| 青阳门 | ✅ 存在 | 门派名称 |
| **林寻** | ❌ 不存在 | AI幻觉出的主角 |
| **宁蒙** | ❌ 不存在 | AI幻觉出的角色 |
| **灵海境** | ❌ 不存在 | AI幻觉出的境界 |
| **宁家** | ❌ 不存在 | AI幻觉出的家族 |

**结论**：数据库中存储的内容完全正确，与BACKEND.md一致。

---

### 2. 工具实现检查 ✅ 正确

**文件**：`backend/app/services/agent/langgraph_agent.py:341-402`

**get_chapter_by_order_tool 实现**：
```python
async def get_chapter_by_order_tool(work_id: str, chapter_order: int) -> str:
    # 查询数据库获取章节
    chapter_info = {
        "chapter_id": str(target_chapter.id),
        "title": target_chapter.title,
        "order": target_chapter.order,
        "content": target_chapter.content[:5000],  # ⚠️ 只返回前5000字
        "content_length": len(target_chapter.content),
        "word_count": target_chapter.word_count,
        "status": target_chapter.status.value
    }
    return json.dumps(chapter_info, ensure_ascii=False, indent=2)
```

**发现的问题**：
- ⚠️ **内容截断**：工具只返回前5000字符，第28章有3068字符，全部返回但可能被HTML标签占用大量空间
- ⚠️ **HTML格式**：章节内容包含`<p>`标签，可能干扰AI理解

**结论**：工具实现正确，但存在优化空间。

---

### 3. 执行流程追踪 ✅ 正确

**执行日志分析**（ERROR.md）：
```
17:50:39  任务1: 使用get_chapter_by_order_tool获取第28章
17:50:39  [get_chapter_by_order_tool] 找到第28章: 第28章 九州八宗  ✅
17:50:39  任务2: 分析获取到的章节内容
17:50:41  使用模型: gemini-2.5-flash, 任务类型: summarization
17:50:59  任务2完成，tokens: 2030+1535=3565
17:50:59  任务3: 整合分析结果
```

**上下文传递逻辑**（langgraph_agent.py:3099-3138）：
```python
# 任务1的结果被添加到all_context
all_context += f"\n任务{result['task_id']}结果：\n{result['result']}\n"

# 任务2执行时接收all_context
result = await self._execute_task(
    task=task,
    context=all_context,  # ✅ 包含任务1的结果
    ...
)
```

**结论**：执行流程正确，任务2确实接收到了任务1返回的章节内容。

---

### 4. AI分析任务检查 ⚠️ 发现问题

**analyze_text_tool 实现**（langgraph_agent.py:263-285）：
```python
async def analyze_text_tool(text: str, focus: str = "all") -> str:
    prompt = f"""请分析以下文本，重点关注：{focus}

文本：
{text}

请提供详细的分析报告："""

    return await _generate_text_helper(
        prompt,
        temperature=0.3,
        max_tokens=1500,
        task_type=TaskType.SUMMARIZATION
    )
```

**问题识别**：
1. ❌ **提示词过于简单**：只有"请分析以下文本"，没有约束条件
2. ❌ **缺乏输入验证**：没有检查text是否包含HTML标签
3. ❌ **缺乏幻觉防护**：没有明确告诉AI"必须基于提供的文本内容，不能编造"
4. ❌ **缺乏格式转换**：HTML格式的文本直接传给AI，可能干扰理解

---

## 🎯 根本原因分析

### 主要原因：AI模型幻觉（Hallucination）

**证据链**：
1. ✅ 数据库内容正确（段融的故事）
2. ✅ 工具返回正确（段融的故事）
3. ✅ 上下文传递正确（任务2接收到段融的故事）
4. ❌ AI输出错误（林寻的故事）

**结论**：在所有数据都正确的情况下，只有AI模型本身产生了幻觉。

### 诱发因素分析

#### 因素1：提示词缺乏约束 🔴 高风险
```python
# 当前提示词
prompt = f"""请分析以下文本，重点关注：{focus}

文本：
{text}

请提供详细的分析报告："""
```

**问题**：
- 没有明确要求"基于文本内容"
- 没有禁止"编造或猜测"
- 没有要求"引用原文"

#### 因素2：HTML格式干扰 🟡 中风险
```html
<p>段融回到镖局，在演武场一个僻静的角落...</p>
<p>　　段融能清楚地感觉到...</p>
```

**问题**：
- HTML标签占用大量token
- 可能被AI误认为是网页内容，触发不同的理解模式
- 空格和格式符号可能干扰语义理解

#### 因素3：模型选择 🟡 中风险
- 使用模型：`gemini-2.5-flash`
- 任务类型：`SUMMARIZATION`

**问题**：
- Flash模型更注重速度，准确性可能稍差
- 总结任务可能会触发模型的"创造性"模式
- 没有设置明确的"事实性"约束

#### 因素4：用户历史污染 🟢 低风险（可能性低）
- 可能用户之前和AI讨论过"林寻"的故事
- 模型可能有记忆混淆（尽管理论上不应该）

---

## 💡 修复方案

### 方案1：增强提示词约束 🔴 必须实施

**修改analyze_text_tool**：
```python
async def analyze_text_tool(text: str, focus: str = "all") -> str:
    prompt = f"""你是一个专业的小说内容分析助手。请严格基于下面提供的文本内容进行分析。

**重要规则**：
1. 只能分析提供的文本内容，不能添加任何不在文本中的信息
2. 不能编造角色、情节或设定
3. 必须忠实于原文，引用原文内容支持你的分析
4. 如果文本不完整，说明"文本未完整提供"，不要猜测后续内容

**分析重点**：{focus}

**待分析文本**：
{text}

请提供详细的分析报告（必须基于上述文本内容）："""

    return await _generate_text_helper(
        prompt,
        temperature=0.1,  # 降低temperature，减少创造性
        max_tokens=1500,
        task_type=TaskType.SUMMARIZATION
    )
```

**改进点**：
- ✅ 明确约束："只能分析提供的文本"
- ✅ 禁止行为："不能编造"
- ✅ 要求证据："引用原文"
- ✅ 降低temperature：从0.3降到0.1

### 方案2：HTML转纯文本 🟡 推荐实施

**在get_chapter_by_order_tool中添加**：
```python
from bs4 import BeautifulSoup

# 将HTML转为纯文本
def html_to_plain_text(html_content: str) -> str:
    if not html_content:
        return ""
    soup = BeautifulSoup(html_content, 'html.parser')
    # 移除所有标签，保留文本
    text = soup.get_text(separator='\n')
    # 清理多余空白
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    return '\n'.join(lines)

# 返回纯文本版本
chapter_info = {
    "chapter_id": str(target_chapter.id),
    "title": target_chapter.title,
    "order": target_chapter.order,
    "content": html_to_plain_text(target_chapter.content[:5000]),
    ...
}
```

### 方案3：增加内容验证 🟢 可选实施

**在任务完成后验证**：
```python
def validate_analysis_content(analysis: str, source_text: str) -> bool:
    """验证分析内容是否基于源文本"""
    # 提取源文本中的关键人名
    source_names = extract_person_names(source_text)
    # 提取分析中的人名
    analysis_names = extract_person_names(analysis)

    # 检查是否有未在源文本中出现的人名
    fake_names = analysis_names - source_names
    if fake_names:
        logger.warning(f"⚠️ 分析中出现了源文本没有的人名: {fake_names}")
        return False
    return True
```

### 方案4：模型选择优化 🟢 可选实施

```python
# 对于需要高精度的分析任务，使用Pro模型
if task_type == TaskType.SUMMARIZATION and focus == "all":
    model = "gemini-2.5-pro"  # 更准确
    temperature = 0.1  # 更严格
else:
    model = "gemini-2.5-flash"  # 平衡速度
    temperature = 0.3
```

---

## 📊 优先级建议

| 方案 | 优先级 | 难度 | 预期效果 | 工作量 |
|------|--------|------|----------|--------|
| 方案1：增强提示词 | 🔴 P0 | ⭐ 低 | 80% | 10分钟 |
| 方案2：HTML转文本 | 🟡 P1 | ⭐⭐ 中 | 60% | 30分钟 |
| 方案3：内容验证 | 🟢 P2 | ⭐⭐⭐ 高 | 40% | 2小时 |
| 方案4：模型优化 | 🟢 P2 | ⭐ 低 | 30% | 15分钟 |

**建议**：立即实施方案1（提示词增强），这是最简单且效果最好的解决方案。

---

## 🧪 验证方案

修复后，使用相同的问题重新测试：
1. 询问"第28章讲了什么？有什么亮点？"
2. 验证AI返回的主角是否是"段融"（不是"林寻"）
3. 验证AI返回的内容是否包含"血鹿茸"、"内息"、"九州八宗"
4. 验证AI没有提到"宁蒙"、"灵海境"、"宁家"等幻觉内容

---

## 📝 总结

### 核心问题
AI模型在分析章节内容时产生了严重幻觉，完全脱离了实际输入的文本内容，编造了一个不存在的故事。

### 根本原因
**提示词缺乏有效约束**，导致AI没有遵循"基于输入内容"的原则，而是从自己的"知识库"或"记忆"中提取了错误内容。

### 关键发现
1. ✅ 所有基础设施都正常工作（数据库、工具、流程）
2. ❌ AI提示词设计存在严重缺陷
3. ⚠️ HTML格式可能是次要干扰因素
4. ⚠️ 使用Flash模型可能降低了准确性

### 修复建议
**立即修复**：增强analyze_text_tool的提示词约束，明确要求AI只能基于输入文本进行分析。

---

生成时间：2025-11-08
调查人：Claude AI Assistant
