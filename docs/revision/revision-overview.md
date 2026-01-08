# 修订编辑器章节 - 总体设计文档

> 最后更新: 2026-01-08
> 开发进度: ✅ 100% 完成

## 1. 功能概述

"修订编辑器章节"是一个非阻塞式的人机协同(HITL)功能，允许 Agent 对章节内容进行修改，用户可以随时审核并决定是否采纳。

### 核心特点
- **非阻塞**: Agent 执行不等待用户确认，继续后续任务
- **异步确认**: 用户可随时点击"采纳"或"弃用"
- **可视化**: 在执行轨迹中显示修订胶囊UI

---

## 2. 修订场景

### 2.1 内容编辑类

| 场景 | 工具 | 操作类型 | 状态 |
|------|------|----------|------|
| 续写章节 | `smart_continue` | append | ✅ 已有 |
| 改写文本 | `smart_rewrite` | replace | ✅ 已有 |
| 插入内容 | `smart_insert` | insert | ✅ 已有 |
| 通用编辑 | `apply_chapter_edit` | 混合 | ✅ 已有 |

### 2.2 章节管理类

| 场景 | 工具 | 操作类型 | 状态 |
|------|------|----------|------|
| 新建章节 | `create_chapter` | create | ✅ 已有 |
| 修改标题 | `update_chapter_title` | rename | ✅ 已有 |

---

## 3. 修订类型定义

```typescript
type RevisionType =
  | 'append'   // 续写（追加到末尾）
  | 'replace'  // 改写（替换内容）
  | 'insert'   // 插入（指定位置）
  | 'create'   // 新建章节
  | 'rename'   // 修改标题
```

---

## 4. 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                        用户界面                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │  聊天面板   │  │  执行轨迹   │  │      编辑器         │  │
│  │             │  │  ┌───────┐  │  │                     │  │
│  │             │  │  │修订胶囊│  │  │  [修订标记显示]    │  │
│  │             │  │  └───────┘  │  │                     │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              ↑
                              │ SSE 事件
                              │
┌─────────────────────────────────────────────────────────────┐
│                        后端服务                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Agent     │→ │  工具执行   │→ │  HITL 事件发送      │  │
│  │  (LangGraph)│  │             │  │                     │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. 数据流

### 5.1 修订请求流程

```
1. Agent 调用编辑工具 (smart_continue/smart_rewrite/...)
                ↓
2. 工具返回 { requires_confirmation: true, ... }
                ↓
3. StreamEventHandler 检测到确认请求
                ↓
4. 发送 SSE 事件: approval_request
                ↓
5. 前端收到事件，设置 pendingApproval 状态
                ↓
6. 执行轨迹显示修订胶囊
                ↓
7. Agent 继续执行（不等待）
```

### 5.2 用户确认流程

```
1. 用户点击 [√ 采纳] 或 [× 弃用]
                ↓
2. 调用 submitApproval(approved, selectedVersion?)
                ↓
3. 触发 agent-show-revision 自定义事件
                ↓
4. 编辑器应用/回滚修改
                ↓
5. POST /api/v1/agent/approvals/{id}/action
                ↓
6. 更新修订状态（已采纳/已弃用）
```

---

## 6. 文件结构

```
后端:
backend/app/services/agent/tools/
├── editor_tools.py          # 编辑器工具 (已有)
├── chapter_tools.py         # 章节管理工具 (待新增)
└── ...

backend/app/services/agent/stream/
├── stream_event_handler.py  # 事件处理 (需修改)
├── flow_events.py           # 执行轨迹事件 (需修改)
└── ...

前端:
src/types/
└── agent.ts                 # 类型定义 ✅ 已修改

src/components/agent/ExecutionFlow/
├── index.tsx                # 执行轨迹入口 ✅ 已修改
├── RevisionCard.tsx         # 修订胶囊组件 ✅ 已新增
└── ...

src/components/editor/
├── NovelEditor.tsx          # 编辑器 ✅ 已修改 (insert 类型)
├── AIRevisionBar.tsx        # 修订操作栏 ✅ 已修改
├── AIPanel.tsx              # AI面板 ✅ 已修改 (自动滚动)
└── ...

src/hooks/
├── useAgentChat.ts          # Agent聊天Hook ✅ 已修改
└── useAgentChatStream.ts    # 流式Hook ✅ 已修改
```

---

## 7. 实现优先级

### P0 - 核心功能 ✅ 已完成
1. ✅ 新增 `revision` FlowItem 类型
2. ✅ 新建 `RevisionCard.tsx` 组件
3. ✅ NovelEditor 支持 insert 类型
4. ✅ AIPanel 自动滚动到最新步骤

### P1 - 新增工具 ✅ 已完成
5. ✅ 新增 `create_chapter` 工具
6. ✅ 新增 `update_chapter_title` 工具
7. ✅ 后端发送 revision 事件

### P2 - 优化 ✅ 已完成
8. ✅ 修订状态持久化
9. ✅ 批量修订管理
10. ✅ 撤销/重做功能

---

## 8. 开发进度

> 详见 [验证报告](./revision-validation-report.md)（2026-01-08 更新）

### 8.1 已完成 ✅
- `smart_continue` / `smart_rewrite` / `smart_insert` / `apply_chapter_edit` 工具
- HITL 确认流程（后端→前端→用户）
- FlowItem 事件机制（含 revision 类型）
- `RevisionCard.tsx` 修订胶囊组件
- `NovelEditor.tsx` insert 类型处理
- `AIPanel.tsx` 自动滚动到最新步骤
- `AIRevisionBar.tsx` insert 类型支持
- `create_chapter` / `update_chapter_title` 章节管理工具
- 后端 `emit_revision` 方法
- 前端 revision 事件处理
- 修订状态持久化（localStorage）
- 批量修订管理（全部采纳/全部弃用）

### 8.2 待开发 ❌
- （无）

### 8.3 后续优化 ⚠️
- 修订历史记录表（可选）
- 修订统计分析（可选）

---

## 9. 相关文档

- [后端工具实现](./revision-backend-tools.md)
- [前端组件实现](./revision-frontend-components.md)
- [类型定义](./revision-types.md)
- [事件流程](./revision-event-flow.md)
- [验证报告](./revision-validation-report.md)
- [UI预览](./preview.html) - 浏览器打开查看 RevisionCard 效果
