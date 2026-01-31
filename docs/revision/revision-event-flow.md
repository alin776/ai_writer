# 修订编辑器章节 - 事件流程

## 1. 整体流程图

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              用户发送消息                                │
│                         "帮我续写第五章"                                 │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           后端 Agent 执行                                │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                  │
│  │ 意图识别    │ →  │ 工具调用    │ →  │ 内容生成    │                  │
│  │ (writing)   │    │ smart_      │    │             │                  │
│  │             │    │ continue    │    │             │                  │
│  └─────────────┘    └─────────────┘    └─────────────┘                  │
│                            │                                            │
│                            ▼                                            │
│                   返回 requires_confirmation: true                       │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      StreamEventHandler 处理                             │
│                                                                         │
│  1. _handle_hitl_confirmation() 检测到确认请求                           │
│  2. 构建 approval_data                                                  │
│  3. 调用 approval_callback (发送 SSE)                                   │
│  4. emit_revision_event (发送执行轨迹事件)                               │
│  5. Agent 继续执行 (不等待)                                              │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    ▼                               ▼
        ┌─────────────────────┐         ┌─────────────────────┐
        │  SSE: approval_     │         │  SSE: flow_event    │
        │       request       │         │  (type: revision)   │
        └─────────────────────┘         └─────────────────────┘
                    │                               │
                    └───────────────┬───────────────┘
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           前端接收事件                                   │
│                                                                         │
│  useAgentChatStream:                                                    │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ onApprovalRequest → 设置 pendingApproval 状态                    │   │
│  │ onFlowEvent       → 添加 revision FlowItem                       │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           UI 渲染                                        │
│                                                                         │
│  ExecutionFlow:                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  ┌─────────────────────────────────────────────────────────┐    │   │
│  │  │ RevisionCard                                             │    │   │
│  │  │ ┌─────────────────────────────────────────────────────┐ │    │   │
│  │  │ │ 📝 章节续写                              待确认      │ │    │   │
│  │  │ │ 第五章：外门初修                                     │ │    │   │
│  │  │ │ ─────────────────────────────────────────────────── │ │    │   │
│  │  │ │ 新增内容预览：                                       │ │    │   │
│  │  │ │ "清晨的第一缕阳光穿透薄雾..."                        │ │    │   │
│  │  │ │                                                     │ │    │   │
│  │  │ │ [× 弃用]  [√ 采纳]                                  │ │    │   │
│  │  │ └─────────────────────────────────────────────────────┘ │    │   │
│  │  └─────────────────────────────────────────────────────────┘    │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                        用户点击 [√ 采纳] 或 [× 弃用]
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           用户确认流程                                   │
│                                                                         │
│  submitApproval(approved, selectedVersion?):                            │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ 1. 触发 agent-show-revision 自定义事件                           │   │
│  │    → 编辑器应用/回滚修改                                         │   │
│  │                                                                  │   │
│  │ 2. POST /api/v1/agent/approvals/{id}/action                     │   │
│  │    → 后端记录确认结果                                            │   │
│  │                                                                  │   │
│  │ 3. 更新 FlowItem 状态 (pending → accepted/discarded)            │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. SSE 事件详解

### 2.1 approval_request 事件

```json
{
  "event": "approval_request",
  "data": {
    "request_id": "smart_continue_abc123",
    "action_type": "edit",
    "operation": "append",
    "chapter_id": "chapter-uuid",
    "new_content": "清晨的第一缕阳光穿透薄雾...",
    "description": "AI续写：+1234字",
    "editor_action": {
      "type": "continue",
      "new_text": "清晨的第一缕阳光穿透薄雾..."
    }
  }
}
```

### 2.2 flow_event (revision) 事件

```json
{
  "event": "flow_event",
  "data": {
    "type": "revision",
    "data": {
      "revisionType": "append",
      "status": "pending",
      "requestId": "smart_continue_abc123",
      "chapterId": "chapter-uuid",
      "chapterTitle": "第五章：外门初修",
      "contentPreview": "清晨的第一缕阳光穿透薄雾...",
      "contentLength": 1234,
      "description": "AI续写：+1234字"
    }
  }
}
```

---

## 3. 后端事件发送

### 3.1 StreamEventHandler 修改

```python
# backend/app/services/agent/stream/stream_event_handler.py

async def _handle_hitl_confirmation(self, node_data: dict):
    """处理 HITL 确认请求"""
    # ... 现有代码 ...

    if tool_result.get("requires_confirmation"):
        # 1. 发送 approval_request 事件
        await self._approval_callback(approval_data)

        # 2. 发送 revision flow_event
        await self._emit_revision_flow_event(tool_result)

async def _emit_revision_flow_event(self, tool_result: dict):
    """发送修订执行轨迹事件"""
    if not self._on_flow_event:
        return

    action_type = tool_result.get("action_type", "edit")

    # 映射 action_type 到 revision_type
    revision_type_map = {
        "edit": tool_result.get("operation", "append"),
        "rewrite": "replace",
        "insert": "insert",
        "create": "create",
        "rename": "rename"
    }
    revision_type = revision_type_map.get(action_type, "append")

    # 获取章节标题
    chapter_title = await self._get_chapter_title(tool_result.get("chapter_id"))

    self._on_flow_event({
        "type": "revision",
        "data": {
            "revisionType": revision_type,
            "status": "pending",
            "requestId": tool_result.get("request_id"),
            "chapterId": tool_result.get("chapter_id"),
            "chapterTitle": chapter_title or tool_result.get("title"),
            "workId": tool_result.get("work_id"),
            "contentPreview": (tool_result.get("content") or "")[:100],
            "contentLength": tool_result.get("content_length"),
            "versions": tool_result.get("versions"),
            "oldTitle": tool_result.get("old_title"),
            "newTitle": tool_result.get("new_title"),
            "description": tool_result.get("description")
        }
    })
```

---

## 4. 前端事件处理

### 4.1 useAgentChatStream 修改

```typescript
// src/hooks/useAgentChatStream.ts

const handleFlowEvent = (event: FlowEvent) => {
  const { type, data } = event;

  if (type === 'revision') {
    // 添加修订 FlowItem
    const revisionItem: FlowItem = {
      id: `revision-${data.requestId}`,
      type: 'revision',
      data: data as RevisionFlowData,
      timestamp: new Date().toISOString()
    };

    setFlowItems(prev => [...prev, revisionItem]);
  }

  // ... 其他类型处理 ...
};
```

### 4.2 submitApproval 修改

```typescript
// src/hooks/useAgentChat.ts

const submitApproval = useCallback(
  async (approved: boolean, selectedVersion?: number) => {
    const pending = sessionManager.getSession(sessionId)?.pendingApproval;
    if (!pending) return;

    try {
      // 1. 触发编辑器事件
      if (approved) {
        window.dispatchEvent(
          new CustomEvent('agent-show-revision', {
            detail: {
              type: getRevisionType(pending),
              // ... 其他数据
            }
          })
        );
      }

      // 2. 调用后端 API
      await agentApi.submitApprovalResponse({
        request_id: pending.request_id,
        approved,
        selected_version: selectedVersion
      });

      // 3. 更新 FlowItem 状态
      updateRevisionStatus(
        pending.request_id,
        approved ? 'accepted' : 'discarded'
      );

      // 4. 清理 pendingApproval
      sessionManager.updateSession(sessionId, { pendingApproval: null });

    } catch (err) {
      console.error('Submit approval failed:', err);
    }
  },
  [sessionId, sessionManager]
);

// 更新修订状态
const updateRevisionStatus = (requestId: string, status: RevisionStatus) => {
  setFlowItems(prev =>
    prev.map(item => {
      if (item.type === 'revision' && (item.data as RevisionFlowData).requestId === requestId) {
        return {
          ...item,
          data: { ...item.data, status }
        };
      }
      return item;
    })
  );
};
```

---

## 5. 编辑器事件处理

### 5.1 agent-show-revision 事件

```typescript
// 在编辑器组件中监听

useEffect(() => {
  const handleShowRevision = (event: CustomEvent) => {
    const { type, original, replacement, position, revisionId } = event.detail;

    switch (type) {
      case 'continue':
        // 追加内容到末尾，显示为绿色高亮
        appendContentWithHighlight(replacement);
        break;

      case 'modify':
        // 替换内容，显示修订标记
        replaceContentWithRevision(original, replacement, position);
        break;

      case 'create':
        // 新建章节（可能需要刷新章节列表）
        refreshChapterList();
        break;

      case 'rename':
        // 修改标题（刷新目录）
        refreshChapterList();
        break;
    }
  };

  window.addEventListener('agent-show-revision', handleShowRevision);
  return () => window.removeEventListener('agent-show-revision', handleShowRevision);
}, []);
```

---

## 6. 状态同步

### 6.1 修订状态持久化

```typescript
// 在消息中保存修订状态

interface Message {
  // ... 现有字段 ...
  flowItems?: FlowItem[];  // 包含修订状态
}

// 保存时
const agentMessage: Message = {
  role: 'agent',
  content: streamingContent,
  flowItems: currentFlowItems,  // 包含修订状态
  timestamp: new Date().toISOString()
};
```

### 6.2 历史会话恢复

```typescript
// 加载历史会话时恢复修订状态

const loadHistorySession = (sessionId: string) => {
  const persisted = loadSession(sessionId);
  if (persisted) {
    const lastAgentMessage = persisted.messages
      .filter(m => m.role === 'agent')
      .pop();

    if (lastAgentMessage?.flowItems) {
      setFlowItems(lastAgentMessage.flowItems);
    }
  }
};
```

---

## 7. 错误处理

```typescript
// 确认失败时的处理

const submitApproval = async (approved: boolean, selectedVersion?: number) => {
  try {
    // ... 正常流程 ...
  } catch (err) {
    // 1. 显示错误提示
    toast.error('操作失败，请重试');

    // 2. 保持 pending 状态，允许重试
    // 不清理 pendingApproval

    // 3. 记录错误日志
    console.error('[submitApproval] failed:', err);
  }
};
```
