# Agent 工具重构方案 - 总体设计

> **实现状态**: ✅ 阶段 1-3 已完成 (2026-01-12)

## 1. 背景

当前 Agent 有 21 个工具（LANGGRAPH_TOOLS），存在以下问题：

1. **工具职责重叠**：`read_chapter_tool` 和 `get_chapter_by_order_tool` 功能有重叠（但不完全重复）
2. **职责不清**：Read 类工具和 Analyze 类工具混在一起
3. **调用链路冗长**：续写需要调用 4-6 个工具（分两轮）
4. **分类混乱**：原三大类（Search/Read/Update）无法清晰区分"获取数据"和"分析数据"
5. **重复读取**：Planning 和 Execution 阶段会重复读取相同章节

> ⚠️ **验证说明**：详见 [07-validation-report.md](./07-validation-report.md)

## 2. 重构目标

- 按 **Search / Read / Analyze / Update** 四大类重新设计
- 精简到 **15 个工具**
- 减少续写调用次数：6 次（分两轮）→ 2-3 次
- 引入章节缓存，避免重复读取

## 3. 四大类定义

| 类别 | 定义 | 是否需要 LLM | 返回内容 |
|------|------|-------------|---------|
| **Search** | 定位位置，返回片段 | ❌（或轻量 LLM 辅助定位） | 位置 + 片段 |
| **Read** | 获取内容，智能预处理 | ❌ | 完整内容 |
| **Analyze** | 评估内容，生成报告 | ✅ | 分析报告 |
| **Update** | 创建/修改/删除 | ✅ | 操作结果 |

### 3.1 Search vs Read 的关系

> **Search 和 Read 是「弱依赖的探索式关系」**

```
Search（定位）
   ↓ 返回：位置 + 片段（snippet）
   ↓
（模型推理/判断）
   ↓
Read（获取上下文）
   ↓ 返回：完整上下文
```

**类比**：
- Search = `grep / ripgrep`（快速定位）
- Read = `vim / less`（查看完整内容）

### 3.2 Read vs Analyze 的关系

| 维度 | Read | Analyze |
|------|------|---------|
| 目的 | 获取原始数据 | 评估/判断数据 |
| 处理方式 | 规则/向量预处理 | LLM 语义推理 |
| 返回内容 | 内容本身 | 对内容的评价 |
| 示例 | "给我看第三章" | "第三章写得怎么样？" |

## 4. 工具分类总览

### 4.1 Search 类 - 2 个

| 工具 | 功能 | 返回 |
|------|------|------|
| `search_content` | 搜索多个相关位置 | 位置 + 片段（多个） |
| `locate_content` | 定位单个位置 | 位置 + 片段（单个） |

### 4.2 Read 类 - 1 个

| 工具 | 功能 | 返回 |
|------|------|------|
| `get_writing_context` | 获取创作上下文（一站式） | 完整上下文 |

### 4.3 Analyze 类 - 1 个

| 工具 | 功能 | 返回 |
|------|------|------|
| `analyze_content` | 分析内容质量（一站式） | 分析报告 |

### 4.4 Update 类 - 11 个

| 工具 | 功能 | 类型 |
|------|------|------|
| `smart_continue` | 智能续写 | 创作 |
| `smart_rewrite` | 智能重写 | 创作 |
| `smart_insert` | 智能插入 | 创作 |
| `show_emotion_tool` | 展示情感 | 增强 |
| `enhance_scene_tool` | 增强场景 | 增强 |
| `learn_style_tool` | 学习风格 | 增强 |
| `apply_chapter_edit` | 应用编辑 | 操作 |
| `create_chapter` | 创建章节 | 操作 |
| `update_chapter_title` | 更新标题 | 操作 |
| `update_chapter_content` | 更新内容 | 操作 |
| `delete_chapter` | 删除章节 | 操作 |

## 5. 设计原则

1. **Search 返回片段，Read 返回完整上下文**
2. **Read 只做预处理，Analyze 做语义推理**
3. **参数控制返回内容**，而不是创建多个工具
4. **一站式调用**，常见场景一次搞定
5. **向后兼容**，旧工具名称通过别名映射
6. **章节缓存**，避免重复数据库查询（新增）

## 6. 预期效果

| 指标 | Before | After |
|------|--------|-------|
| 工具总数 | 21 | 15 |
| 续写调用次数 | 6 次（分两轮） | 2-3 次 |
| Agent 决策复杂度 | 高 | 低 |
| 分类清晰度 | 3 类混乱 | 4 类清晰 |
| 重复数据库查询 | 有 | 无（缓存） |

## 7. 文档索引

- [02-search-tools.md](./02-search-tools.md) - Search 类工具设计
- [03-read-tools.md](./03-read-tools.md) - Read 类工具设计
- [04-analyze-tools.md](./04-analyze-tools.md) - Analyze 类工具设计
- [05-update-tools.md](./05-update-tools.md) - Update 类工具设计
- [06-implementation-plan.md](./06-implementation-plan.md) - 实现计划
- [07-validation-report.md](./07-validation-report.md) - 验证报告（新增）
