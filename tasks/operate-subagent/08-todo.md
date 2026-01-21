# Operate SubAgent 任务清单

## 总览

| 阶段 | 状态 | 说明 |
|------|------|------|
| 阶段0：前置 | ⏳ 待开始 | 扩展底层工具 + 简化 smart_rewrite |
| 阶段1：新增 | ⏳ 待开始 | 添加 operate_apply 工具 |
| 阶段2：共存 | ⏳ 待开始 | 更新示例，灰度验证 |
| 阶段3：弃用 | ⏳ 待开始 | 移除旧模式（可选） |

---

## 核心设计理念

**判断标准：是否需要 AI 生成内容？**
- 需要 → 走 operate_apply（Create → Operate）
- 不需要 → 用户自己在 UI 操作

| 场景 | 需要 AI？ | 走 operate_apply？ |
|------|----------|-------------------|
| 续写 | ✓ | ✓ append |
| 改写部分 | ✓ | ✓ replace |
| 插入 | ✓ | ✓ insert |
| 重写整章 | ✓ | ✓ content |
| 写新章节 | ✓ | ✓ create |
| 改进标题 | ✓ | ✓ title |
| 删除章节 | ✗ | ✗ 用户自己操作 |
| 粘贴替换 | ✗ | ✗ 用户自己操作 |

---

## 阶段0：前置任务

### 0.1 扩展 apply_chapter_edit（新增 replace_all）

**背景**：`content`（整体替换）操作需要走 HITL 确认流程，但现有 `update_chapter_content` 是乐观执行模式（直接写入）。

**方案**：在 `apply_chapter_edit` 中新增 `operation="replace_all"`

**replace_all 语义定义**：
- **含义**：用新内容**完全替换**整个章节的**全部内容**
- **不需要定位**：因为是替换整个章节，无需 paragraph_index/node_id
- **HITL 确认**：需要用户确认后才执行

**现有操作类型**：
| operation | 说明 | 定位方式 |
|-----------|------|---------|
| append | 追加到末尾 | 无需定位 |
| replace | 替换指定段落 | node_id / paragraph_index / original_text / anchors |
| insert | 在指定位置插入 | node_id / paragraph_index / position / anchors |

**新增操作类型**：
| operation | 说明 | 定位方式 |
|-----------|------|---------|
| replace_all | 整体替换章节**全部**内容 | 无需定位 |

**需要修改的文件**：
- [ ] `backend/app/services/agent/tools/editor_tools.py`
  - [ ] 第360行：operation验证列表添加 `"replace_all"`
  - [ ] 添加 replace_all 处理分支（直接用 content 替换整个章节内容）
- [ ] `backend/app/services/chapter_revision_service.py`
  - [ ] `_build_new_content` 方法添加 replace_all 分支
  - [ ] replace_all 逻辑：`new_content = content`（直接全量替换）
- [ ] 添加单元测试

### 0.2 简化 smart_rewrite（从3个版本改为1个）

**背景**：当前 `smart_rewrite` 生成3个改写版本，用户在前端选择。为简化 operate_apply 流程，改为只生成1个版本。

**现有流程**：
```
smart_rewrite → 返回3个版本(versions数组) → 前端展示3个选项 → 用户选择 → apply_chapter_edit
```

**简化后流程**：
```
smart_rewrite → 返回1个版本 → operate_apply → HITL确认
```

**需要修改的文件**：

**后端**：
- [ ] `backend/app/services/agent/tools/editor_tools.py`
  - [ ] 修改 `smart_rewrite` 的提示词，引导 AI 只生成1个最佳版本
  - [ ] 修改返回结构（从 `versions[]` 改为单个 `content`）

**前端**（影响范围较大）：
- [ ] `src/components/agent/AgentEditConfirmDialog.tsx`
  - [ ] 移除版本选择UI（目前依赖 `versions[selectedVersion].content`）
  - [ ] 改为直接显示单个改写结果
- [ ] `src/components/AIPanel.tsx`
  - [ ] 第1478行：修改 `pendingApproval.versions[selectedVersion].content` 的使用方式
  - [ ] 适配新的返回结构

**测试**：
- [ ] 添加单元测试
- [ ] 更新相关文档

---

## 阶段1：新增工具

### 1.1 创建核心文件
- [ ] 创建 `backend/app/services/agent/tools/operate_tools.py`
- [ ] 实现 `OperationType` 枚举（6种类型）
- [ ] 实现 `OperateResult` 数据类
- [ ] 实现 `ContentOperator` 类
  - [ ] `operate()` 主方法（三阶段流程）
  - [ ] `_route_operation()` 意图路由
  - [ ] `_smart_locate()` 智能定位（仅 replace/insert）
  - [ ] `_execute_operation()` 执行底层工具

### 1.2 实现意图路由

路由表：
| operation | 底层工具 | 需要定位 |
|-----------|----------|---------|
| append | apply_chapter_edit(append) | ✗ |
| replace | apply_chapter_edit(replace) | ✓ |
| insert | apply_chapter_edit(insert) | ✓ |
| content | apply_chapter_edit(replace_all) | ✗ |
| create | create_chapter | ✗ |
| title | update_chapter_title | ✗ |

- [ ] 实现 `ROUTING_TABLE` 路由表
- [ ] 实现路由逻辑

### 1.3 实现工具定义
- [ ] 实现 `@tool operate_apply`
- [ ] 实现 `OperateApplyInput` (Pydantic)
- [ ] 实现 `OperateApplyOutput` (Pydantic)
- [ ] 实现 `operate_apply_executor`
- [ ] 创建 `operate_apply_tool` (StandardTool)

### 1.4 注册工具
- [ ] 在 `tools/__init__.py` 添加导出
- [ ] 在 `tool_dispatcher.py` 添加到 `OPERATION_TOOLS`
- [ ] 验证工具可被正确识别和调用

### 1.5 单元测试
- [ ] 创建 `tests/unit/agent/tools/test_operate_tools.py`
- [ ] 测试意图路由
  - [ ] append → apply_chapter_edit(append), 无需定位
  - [ ] replace → apply_chapter_edit(replace), 需要定位
  - [ ] insert → apply_chapter_edit(insert), 需要定位
  - [ ] content → apply_chapter_edit(replace_all), 无需定位
  - [ ] create → create_chapter, 无需定位
  - [ ] title → update_chapter_title, 无需定位
- [ ] 测试定位策略
  - [ ] replace + original_text → 文本匹配
  - [ ] insert + target_description → 语义定位
  - [ ] 定位失败处理
- [ ] 测试各操作执行
  - [ ] append 操作
  - [ ] replace 操作
  - [ ] insert 操作
  - [ ] content 操作
  - [ ] create 操作
  - [ ] title 操作
- [ ] 测试错误处理
  - [ ] 路由失败（未知 operation）
  - [ ] 定位失败
  - [ ] 执行失败

---

## 阶段2：更新示例

### 2.1 更新 planning_prompts.py
- [ ] 添加 `operate_apply` 工具描述
- [ ] 说明支持的 6 种 operation
- [ ] 强调：需要 AI 生成内容 → operate_apply
- [ ] 标记底层工具为内部使用

### 2.2 更新 planning_examples.py
- [ ] 添加续写示例（append）
- [ ] 添加改写部分示例（replace）
- [ ] 添加插入示例（insert）
- [ ] 添加重写整章示例（content）
- [ ] 添加写新章节示例（create）
- [ ] 添加改进标题示例（title）
- [ ] 保留旧示例（兼容性）

### 2.3 集成测试
- [ ] 创建 `tests/integration/agent/test_operate_apply.py`
- [ ] 测试 append 完整流程
- [ ] 测试 replace 完整流程（自动定位）
- [ ] 测试 insert 完整流程（语义定位）
- [ ] 测试 content 完整流程（整体替换）
- [ ] 测试 create 完整流程
- [ ] 测试 title 完整流程
- [ ] 测试 Planning → Operate 链路

### 2.4 灰度验证
- [ ] 部署到测试环境
- [ ] 收集成功率数据
- [ ] 收集定位准确率数据
- [ ] 收集用户反馈

---

## 阶段3：弃用旧模式（可选）

### 3.1 清理示例
- [ ] 移除 locate_content + apply_chapter_edit 示例
- [ ] 移除直接调用 create_chapter 示例
- [ ] 移除直接调用 update_chapter_title 示例
- [ ] 只保留 operate_apply 示例

### 3.2 标记内部使用
- [ ] 更新 apply_chapter_edit 文档
- [ ] 更新 update_chapter_content 文档
- [ ] 更新 create_chapter 文档
- [ ] 更新 update_chapter_title 文档
- [ ] 添加弃用警告日志

### 3.3 文档更新
- [ ] 更新 API 文档
- [ ] 更新开发指南

---

## 验收标准

### 功能验收
- [ ] 续写流程正常（operation=append）
- [ ] 改写部分流程正常（operation=replace，自动定位原文）
- [ ] 插入流程正常（operation=insert，语义定位）
- [ ] 重写整章流程正常（operation=content，整体替换）
- [ ] 写新章节流程正常（operation=create，含标题+内容）
- [ ] 改进标题流程正常（operation=title）
- [ ] HITL 确认流程正常
- [ ] 错误信息清晰

### 性能验收
- [ ] 路由延迟 < 10ms
- [ ] 定位延迟 < 500ms
- [ ] 整体操作延迟 < 2s
- [ ] 无明显内存泄漏

### 质量验收
- [ ] 单元测试覆盖率 >= 90%
- [ ] 集成测试通过
- [ ] 代码评审通过

---

## 风险与对策

| 风险 | 对策 |
|------|------|
| 路由逻辑错误 | 完善单元测试，覆盖所有 operation |
| 定位准确率低 | replace 用原文匹配，insert 用语义定位 |
| 与旧模式冲突 | 保持向后兼容，不修改旧工具 |
| Planning 不稳定 | 提供清晰的示例和工具描述 |
| HITL 流程中断 | 复用现有底层工具的 HITL 逻辑 |
| **replace_all 前端适配** | 前端 HITL 确认界面需要支持显示整章替换对比 |
| **smart_rewrite 简化影响前端** | 需要同步修改 AgentEditConfirmDialog.tsx 和 AIPanel.tsx |
| **operation 验证分散** | 统一在 editor_tools.py 和 chapter_revision_service.py 中维护 operation 列表 |
| **并发冲突** | replace_all 操作需要验证 base_version，防止覆盖他人修改 |

---

## 深度验证发现的问题

### 已确认的问题

| # | 问题 | 影响 | 状态 |
|---|------|------|------|
| 1 | `editor_tools.py:360` operation 验证列表缺少 replace_all | 阻塞 | ❌ 待修复 |
| 2 | `chapter_revision_service.py` 缺少 replace_all 分支 | 阻塞 | ❌ 待修复 |
| 3 | 前端 versions[] 依赖需要适配 | 阻塞 | ❌ 待修复 |
| 4 | planning_prompts.py 缺少 replace_all 说明 | 中等 | ❌ 待修复 |

### 已验证无问题的部分

| # | 验证项 | 结果 |
|---|--------|------|
| 1 | ChapterRevision 模型支持 replace_all | ✅ operation 字段为 String(20)，足够 |
| 2 | locate_content 返回值与 apply_chapter_edit 参数匹配 | ✅ 100% 兼容 |
| 3 | tool_dispatcher.py operation 参数传递 | ✅ 已正确处理 |
| 4 | HITL 流程完整性 | ✅ 已支持 |

---

## 相关文档

- [00-总体规划.md](./00-总体规划.md) - 概述、目标、核心设计理念
- [01-架构设计.md](./01-架构设计.md) - 三阶段流程设计
- [02-数据结构.md](./02-数据结构.md) - 数据结构定义
- [03-核心实现.md](./03-核心实现.md) - ContentOperator 类实现
- [04-工具定义.md](./04-工具定义.md) - operate_apply 工具定义
- [05-Planning集成.md](./05-Planning集成.md) - Prompt 和示例修改
- [06-测试计划.md](./06-测试计划.md) - 测试用例和验证方案
- [07-迁移指南.md](./07-迁移指南.md) - 渐进式迁移步骤
- [09-流程图.md](./09-流程图.md) - 完整流程图

---

## 更新记录

| 日期 | 更新内容 |
|------|----------|
| 2026-01-21 | 初始版本 |
| 2026-01-21 | 更新：整合所有需要 AI 的操作（append/replace/insert/create/title） |
| 2026-01-21 | 更新：明确核心设计理念（需要 AI 生成 → operate_apply） |
| 2026-01-21 | 更新：新增 content 操作（整体替换章节内容） |
| 2026-01-21 | 更新：content 操作改用 apply_chapter_edit(replace_all) 以支持 HITL |
| 2026-01-21 | 更新：新增阶段0前置任务（扩展 replace_all + 简化 smart_rewrite） |
| 2026-01-21 | 更新：深度验证，补充遗漏的修改文件和风险点 |
