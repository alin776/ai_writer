# 修订编辑器章节 - 总体设计文档

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
| 新建章节 | `create_chapter` | create | ❌ 待新增 |
| 修改标题 | `update_chapter_title` | rename | ❌ 待新增 |

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
└── agent.ts                 # 类型定义 (需修改)

src/components/agent/ExecutionFlow/
├── index.tsx                # 执行轨迹入口 (需修改)
├── RevisionCard.tsx         # 修订胶囊组件 (待新增)
└── ...

src/hooks/
└── useAgentChat.ts          # Agent聊天Hook (需修改)
```

---

## 7. 实现优先级

### P0 - 核心功能
1. 新增 `revision` FlowItem 类型
2. 新建 `RevisionCard.tsx` 组件
3. 后端发送 revision 事件

### P1 - 新增工具
4. 新增 `create_chapter` 工具
5. 新增 `update_chapter_title` 工具

### P2 - 优化
6. 修订状态持久化
7. 批量修订管理

---

## 8. 验证发现的问题

### 8.1 缺失的工具
- ❌ `create_chapter_tool` - Agent 无法创建新章节
- ❌ `update_chapter_title_tool` - Agent 无法修改章节标题

### 8.2 前端处理不完整
- ❌ `handleShowRevision` 不支持 `insert` 类型（NovelEditor.tsx:503-628）
- ❌ `EditorAction` 缺少 `chapter_id`、`revision_id` 字段

### 8.3 其他遗漏
- ❌ 修订状态未持久化（刷新后丢失）
- ❌ 无批量修订机制

详见 [验证报告](./revision-validation-report.md)

---

## 9. 相关文档

- [后端工具实现](./revision-backend-tools.md)
- [前端组件实现](./revision-frontend-components.md)
- [类型定义](./revision-types.md)
- [事件流程](./revision-event-flow.md)
- [验证报告](./revision-validation-report.md)
