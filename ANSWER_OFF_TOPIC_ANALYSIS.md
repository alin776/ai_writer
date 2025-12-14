# AI答非所问问题 - 深度分析报告

## 问题描述

**用户输入**：
```
设计林仙的5个成长节点，并续写第一个节点的精彩场景
```

**期望输出**：
1. 林仙的5个成长节点（具体的成长阶段描述）
2. 第一个节点的精彩场景续写

**实际输出**：
1. ❌ 对用户请求的文本分析（主题分析、人物分析、情节梳理等）
2. ✅ 第一个节点的精彩场景续写（正确）

**问题表现**：
第一个任务完全答非所问，AI分析了用户的请求文本本身，而不是去创作5个成长节点。

---

## 根本原因分析

### 原因1：Planning Prompt的误导 ⭐⭐⭐⭐⭐ (Critical)

**位置**: `backend/app/services/agent/prompt_cache.py:212-213`

```python
- analyze_text_tool: 概括、分析、规划大纲 (参数: text, focus)
  - 适用于：概括内容、分析人物、分析情节、写大纲、规划章节
```

**同时在第191-192行**：
```python
大纲 vs 正文：
- 大纲 = 结构化规划（章节标题、主线、伏笔列表）→ analyze_text_tool
- 正文 = 完整故事叙述（续写内容）→ continue_writing_tool
```

**问题分析**：

1. **Prompt明确指示**："规划大纲"应该使用 `analyze_text_tool`
2. **Planning Agent的推理链**：
   - 用户请求："设计林仙的5个成长节点"
   - AI判断：这是一个"规划"/"设计"类任务
   - 参考Prompt："规划 → analyze_text_tool"
   - 选择：analyze_text_tool ❌

3. **工具本质冲突**：
   - `analyze_text_tool` 是一个**分析工具**
   - 设计用途：分析现有文本（人物、情节、主题等）
   - 不适用于：从零创作新内容

4. **实际执行结果**：
   - analyze_text_tool 没有合适的文本可分析
   - 只能分析用户的请求文本本身
   - 输出：对请求的主题分析、人物分析等

**证据链**：

从Backend.md日志：
```
第79行: [Stream] Task started: 设计林仙的5个成长节点
第80行: [_execute_task] analyze_text_tool 的 focus 参数无效: '设计林仙的5个成长节点...'，使用默认值 'all'
第81行: [_execute_task] 调用 registry.call_tool(analyze_text)
第82行: [analyze_text] 开始执行工具
```

**影响程度**: 🔴 90%

这是导致答非所问的直接原因。

---

### 原因2：工具分类关键词缺失 ⭐⭐⭐ (Important)

**位置**: `backend/app/services/agent/tools/tool_registry.py:622-624`

```python
def _detect_task_category(self, description: str) -> Optional[str]:
    desc = description.lower()

    # WRITING 类关键词（通用）
    if any(kw in desc for kw in ["续写", "创作", "生成", "写", "补充", "修正", "撰写", "编写"]):
        return "writing"

    # ANALYSIS 类关键词（通用）
    if any(kw in desc for kw in ["分析", "总结", "梳理", "评估", "研究", "归纳", "概括"]):
        return "analysis"
```

**问题分析**：

1. **关键词"设计"缺失**：
   - "设计林仙的5个成长节点"包含"设计"这个词
   - "设计"不在 WRITING 类关键词列表中
   - "设计"也不在 ANALYSIS 类关键词列表中
   - 导致无法正确识别为创作类任务

2. **关联问题**：
   - 类似的词还有："构思"、"规划"、"策划"、"设定"
   - 这些词在用户请求中常见，但都不在关键词列表中

**影响程度**: 🟡 30%

虽然这个方法可能不是Planning Agent直接使用的，但它反映了系统对"创作类任务"的理解不完整。

---

## 问题影响

### 用户体验
- ❌ 完全答非所问，用户得不到想要的内容
- ❌ 降低用户对AI的信任度
- ❌ 需要用户重新提问，浪费时间

### Token消耗
- 生成了无用的分析内容
- 浪费了约2000 tokens

### 系统问题
- Planning Agent对"创作" vs "分析"的理解有偏差
- 工具选择逻辑存在缺陷

---

## 修复方案

### 方案1：修正Planning Prompt（推荐） ⭐⭐⭐⭐⭐

**修改位置**: `backend/app/services/agent/prompt_cache.py:212-217`

**当前内容**：
```python
- analyze_text_tool: 概括、分析、规划大纲 (参数: text, focus)
  - 适用于：概括内容、分析人物、分析情节、写大纲、规划章节
```

**修改为**：
```python
- analyze_text_tool: 分析已有文本 (参数: text, focus)
  - 适用于：分析人物、分析情节、概括内容、评估文本质量
  - ⚠️ 只能分析现有文本，不能创作新内容！
  - ⚠️ "设计"/"规划"/"创作"类任务 → 使用 continue_writing_tool

- continue_writing_tool: 创作新内容/大纲 (参数: context, requirements)
  - 适用于：续写、创作、生成大纲、设计角色成长、规划情节
  - 可用于创作大纲/规划（如"设计5个成长节点"、"规划第5-9章大纲"）
```

**修改第191-192行**：
```python
大纲 vs 正文：
- 大纲 = 结构化规划（章节标题、主线、伏笔列表）→ continue_writing_tool
  注意：大纲也是"创作"，需要从零生成内容
- 正文 = 完整故事叙述（续写内容）→ continue_writing_tool
- 分析现有大纲/内容 → analyze_text_tool
```

**优点**：
- 直接修正误导性的Prompt
- 明确区分"分析"和"创作"
- 对所有类似场景都有效

**缺点**：
- 需要更新PROMPT_VERSION（已有机制）
- 需要重新测试Planning逻辑

---

### 方案2：增强工具分类关键词（辅助）⭐⭐⭐

**修改位置**: `backend/app/services/agent/tools/tool_registry.py:622-624`

**当前内容**：
```python
# WRITING 类关键词（通用）
if any(kw in desc for kw in ["续写", "创作", "生成", "写", "补充", "修正", "撰写", "编写"]):
    return "writing"
```

**修改为**：
```python
# WRITING 类关键词（通用）
if any(kw in desc for kw in ["续写", "创作", "生成", "写", "补充", "修正", "撰写", "编写", "设计", "构思", "规划", "策划", "设定"]):
    return "writing"
```

**优点**：
- 增强工具选择的准确性
- 覆盖更多用户表达方式

**缺点**：
- "规划"这个词有歧义（可能是规划大纲，也可能是规划分析）
- 需要配合方案1一起使用

---

### 方案3：添加Planning Agent的二次校验（可选）⭐⭐

**实现方式**：
在Planning Agent生成任务后，添加一个校验步骤：
1. 检查任务描述是否包含"设计"/"规划"/"创作"等词
2. 检查选择的工具是否为 analyze_text_tool
3. 如果匹配，给出警告或自动纠正

**优点**：
- 多一道防线
- 可以catch类似的错误

**缺点**：
- 增加系统复杂度
- 治标不治本

---

## 修复优先级

| 方案 | 优先级 | 工作量 | 效果 |
|------|--------|--------|------|
| 方案1：修正Planning Prompt | P0 - Critical | 30分钟 | 解决根本问题 |
| 方案2：增强工具分类关键词 | P1 - Important | 10分钟 | 辅助改进 |
| 方案3：二次校验 | P2 - Nice to have | 2小时 | 防御性编程 |

---

## 建议实施步骤

### Phase 1：快速修复 (30分钟)
1. ✅ 修改 `prompt_cache.py` 的 Planning Prompt
   - 明确 analyze_text_tool 只用于分析现有文本
   - 明确"设计"/"规划"类任务使用 continue_writing_tool
2. ✅ 更新 PROMPT_VERSION 为 v2.12.0
3. ✅ 测试相同的用户请求，验证修复效果

### Phase 2：增强鲁棒性 (10分钟)
4. ✅ 修改 `tool_registry.py` 的关键词列表
5. ✅ 添加"设计"、"构思"、"规划"、"策划"、"设定"

### Phase 3：回归测试 (1小时)
6. ✅ 测试多种"设计"/"规划"类请求
7. ✅ 确保不影响原有的分析类请求
8. ✅ 更新测试用例

---

## 预期效果

**修复前**：
```
用户：设计林仙的5个成长节点
AI输出：【登场人物】林仙
        主题分析: 本文本的主题是关于角色成长弧线的设计与规划...
```

**修复后**：
```
用户：设计林仙的5个成长节点
AI输出：
1. 觉醒节点：林仙在村庄遭遇危机时，首次觉醒操控植物的能力...
2. 修炼节点：林仙拜入仙门，开始系统学习...
3. 突破节点：面对强敌，林仙突破境界...
4. 抉择节点：在正邪之间做出艰难选择...
5. 成帝节点：最终摆烂成帝，登顶修真界...
```

---

## 相关代码文件

- `backend/app/services/agent/prompt_cache.py:212-217` - Planning Prompt（主要修改）
- `backend/app/services/agent/prompt_cache.py:191-192` - 大纲 vs 正文说明
- `backend/app/services/agent/tools/tool_registry.py:622-624` - 工具分类关键词
- `backend/app/services/agent/langgraph_agent.py:5359` - analyze_text_tool 参数验证

---

## 总结

**核心问题**：
Planning Prompt将"规划大纲"错误地指向 analyze_text_tool（分析工具），导致AI在面对"设计"/"规划"类创作任务时，选择了错误的工具。

**根本原因**：
对"分析"和"创作"的边界理解不清晰。大纲虽然是"规划"，但本质是"创作"（从零生成内容），而不是"分析"（处理现有内容）。

**修复方向**：
明确区分"分析现有内容"和"创作新内容"，让Planning Agent做出正确的工具选择。

---

**分析完成时间**: 2025-12-14
**分析人员**: Claude Sonnet 4.5
**优先级**: P0 - Critical
