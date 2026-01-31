# 修订编辑器章节 - 类型定义

## 1. 前端类型定义

### 1.1 修订类型枚举

```typescript
// src/types/agent.ts

/**
 * 修订操作类型
 */
export type RevisionType =
  | 'append'   // 续写（追加到末尾）
  | 'replace'  // 改写（替换内容）
  | 'insert'   // 插入（指定位置）
  | 'create'   // 新建章节
  | 'rename';  // 修改标题

/**
 * 修订状态
 */
export type RevisionStatus = 'pending' | 'accepted' | 'discarded';
```

### 1.2 修订数据结构

```typescript
/**
 * 改写版本
 */
export interface RewriteVersion {
  style_name: string;  // "版本A"
  reason: string;      // "更有画面感"
  content: string;     // 改写后的内容
}

/**
 * 修订 FlowItem 数据
 */
export interface RevisionFlowData {
  // 基础信息
  revisionType: RevisionType;
  status: RevisionStatus;
  requestId: string;           // HITL 请求ID

  // 章节信息
  chapterId?: string;
  chapterTitle?: string;
  workId?: string;

  // 内容编辑 (append/replace/insert)
  operation?: 'append' | 'replace' | 'insert';
  contentPreview?: string;     // 内容预览（前100字）
  contentLength?: number;      // 内容长度
  position?: number;           // 插入位置

  // 改写 (replace with versions)
  originalContent?: string;    // 原内容
  versions?: RewriteVersion[]; // 改写版本列表

  // 新建章节 (create)
  title?: string;              // 新章节标题
  order?: number;              // 章节顺序

  // 修改标题 (rename)
  oldTitle?: string;           // 原标题
  newTitle?: string;           // 新标题

  // 描述
  description?: string;        // "AI续写：+1234字"
}
```

### 1.3 FlowItem 类型扩展

```typescript
/**
 * 执行轨迹项类型 (扩展)
 */
export type FlowItemType =
  | 'text'
  | 'tool'
  | 'content'
  | 'step'
  | 'output'
  | 'agent_header'
  | 'completion'
  | 'summarization'
  | 'revision';  // 新增

/**
 * 执行轨迹项 (扩展)
 */
export interface FlowItem {
  id: string;
  type: FlowItemType;
  data:
    | TextFlowData
    | ToolFlowData
    | ContentFlowData
    | StepFlowData
    | OutputFlowData
    | AgentHeaderFlowData
    | CompletionFlowData
    | SummarizationFlowData
    | RevisionFlowData;  // 新增
  timestamp: string;
}
```

### 1.4 ApprovalRequest 扩展

```typescript
/**
 * HITL 确认请求 (扩展)
 */
export interface ApprovalRequest {
  request_id: string;
  action_type: 'edit' | 'rewrite' | 'insert' | 'create' | 'rename';  // 扩展

  // 通用字段
  chapter_id?: string;
  description?: string;

  // 内容编辑
  operation?: string;
  original_content?: string;
  new_content?: string;
  versions?: RewriteVersion[];
  editor_action?: EditorAction;

  // 新建章节
  work_id?: string;
  title?: string;
  order?: number;

  // 修改标题
  old_title?: string;
  new_title?: string;
}
```

---

## 2. 后端类型定义

### 2.1 工具返回类型

```python
# backend/app/services/agent/tools/types.py

from typing import TypedDict, List, Optional, Literal

class RewriteVersion(TypedDict):
    style_name: str
    reason: str
    content: str

class ToolConfirmationResult(TypedDict):
    """工具确认请求返回结构"""
    success: bool
    requires_confirmation: bool
    action_type: Literal['edit', 'rewrite', 'insert', 'create', 'rename']

    # 通用字段
    chapter_id: Optional[str]
    description: Optional[str]

    # 内容编辑
    operation: Optional[Literal['append', 'replace', 'insert']]
    content: Optional[str]
    content_length: Optional[int]
    position: Optional[int]

    # 改写
    original_text: Optional[str]
    versions: Optional[List[RewriteVersion]]

    # 新建章节
    work_id: Optional[str]
    title: Optional[str]
    order: Optional[int]

    # 修改标题
    old_title: Optional[str]
    new_title: Optional[str]
```

### 2.2 SSE 事件类型

```python
# backend/app/services/agent/stream/event_types.py

from typing import TypedDict, List, Optional, Literal

class RevisionEventData(TypedDict):
    """修订事件数据"""
    revision_type: Literal['append', 'replace', 'insert', 'create', 'rename']
    status: Literal['pending', 'accepted', 'discarded']
    request_id: str

    # 章节信息
    chapter_id: Optional[str]
    chapter_title: Optional[str]
    work_id: Optional[str]

    # 内容
    content_preview: Optional[str]
    content_length: Optional[int]

    # 改写版本
    versions: Optional[List[RewriteVersion]]

    # 标题
    old_title: Optional[str]
    new_title: Optional[str]
    title: Optional[str]

    # 描述
    description: Optional[str]

class FlowEvent(TypedDict):
    """执行轨迹事件"""
    type: Literal['text', 'tool', 'step', 'output', 'revision', ...]
    data: dict
```

---

## 3. API 类型定义

### 3.1 确认请求 API

```python
# backend/app/schemas/agent.py

from pydantic import BaseModel
from typing import Optional, List, Literal

class ApprovalActionRequest(BaseModel):
    """确认操作请求"""
    action: Literal['approve', 'reject', 'modify']
    selected_version: Optional[int] = None  # 改写时选择的版本
    modifications: Optional[dict] = None
    feedback: Optional[str] = None

class ApprovalResponse(BaseModel):
    """确认响应"""
    request_id: str
    action_type: str
    status: str
    timestamp: str
```

### 3.2 前端 API 类型

```typescript
// src/services/agentApi.ts

interface SubmitApprovalRequest {
  request_id: string;
  approved: boolean;
  selected_version?: number;
}

interface ApprovalActionResponse {
  success: boolean;
  request_id: string;
  action: string;
  status: string;
  timestamp: string;
}
```

---

## 4. 类型映射关系

```
后端工具返回 → SSE事件 → 前端状态
─────────────────────────────────────────────────────
action_type: "edit"      → revision_type: "append"   → revisionType: "append"
action_type: "rewrite"   → revision_type: "replace"  → revisionType: "replace"
action_type: "insert"    → revision_type: "insert"   → revisionType: "insert"
action_type: "create"    → revision_type: "create"   → revisionType: "create"
action_type: "rename"    → revision_type: "rename"   → revisionType: "rename"
```

---

## 5. 类型守卫函数

```typescript
// src/types/guards.ts

export function isRevisionFlowData(data: any): data is RevisionFlowData {
  return (
    data &&
    typeof data.revisionType === 'string' &&
    ['append', 'replace', 'insert', 'create', 'rename'].includes(data.revisionType)
  );
}

export function isRewriteRevision(data: RevisionFlowData): boolean {
  return data.revisionType === 'replace' && Array.isArray(data.versions);
}

export function isCreateRevision(data: RevisionFlowData): boolean {
  return data.revisionType === 'create';
}

export function isRenameRevision(data: RevisionFlowData): boolean {
  return data.revisionType === 'rename';
}
```
