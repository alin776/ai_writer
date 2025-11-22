# ReAct Agent 直接修改编辑器内容 - 工程设计文档

**功能**: Agent在React模式下直接修改编辑器内容
**状态**: 待实现
**创建日期**: 2025-11-23
**版本**: v2.0 (完善版)

---

## 1. 功能概述

### 1.1 核心需求

让ReAct Agent能够在用户对话过程中，通过调用工具直接修改编辑器中的章节内容，而不是仅仅返回文本让用户手动复制粘贴。

### 1.2 关键约束

1. **用户确认机制**: 每次修改编辑器内容前**必须征求用户同意**
2. **改写场景**: AI改写需要先通过**写作竞技场**生成多个版本供用户选择
3. **续写场景**: 可参考现有的AI续写抽屉(`AIContinueDrawer`)的交互模式
4. **权限控制**: Agent只能修改当前用户有权限的章节

---

## 2. 现有系统分析

### 2.1 已有的AI写作功能

| 功能 | 文件路径 | 说明 |
|------|----------|------|
| AI自动补全 | `src/components/editor/AIAutoCompleteExtension.tsx` | Tab接受、Escape取消、灰色预览文本 |
| AI续写抽屉 | `src/components/editor/AIContinueDrawer.tsx` | 右侧滑出、快速/专业模式、参数配置 |
| 写作竞技场 | `backend/app/services/agent/tools/advanced_tools.py` | `rewrite_arena`工具生成多版本改写 |
| 章节更新API | `backend/app/api/v1/chapters.py` | `PUT /chapters/{chapter_id}` |
| 前端更新方法 | `src/services/DataService.ts` | `updateChapter()` |

### 2.2 现有AI续写交互模式

```
用户点击AI续写 → 右侧滑出AIContinueDrawer → 配置参数 → 生成续写 → 显示预览 → 用户确认 → 插入编辑器
```

**关键特性**:
- 快速模式 vs 专业模式
- 参数配置（目标长度、文风、视角等）
- 折叠面板组织复杂选项
- 生成前显示上下文预览

### 2.3 现有Agent工具集

```python
# backend/app/services/agent/tools/
- continue_writing_tool    # 续写（只返回文本，不保存）
- polish_text_tool         # 润色（只返回文本，不保存）
- expand_text_tool         # 扩写（只返回文本，不保存）
- rewrite_arena            # 多版本改写（返回多个版本）
```

**缺失**: 没有直接更新章节数据库内容的工具

---

## 3. 架构设计

### 3.1 整体架构

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Agent 对话     │────>│  确认机制组件     │────>│  编辑器同步      │
│   (ReAct模式)    │     │  (用户审批)       │     │  (实时更新)      │
└─────────────────┘     └──────────────────┘     └─────────────────┘
         │                       │                        │
         v                       v                        v
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  新增Agent工具   │     │  前端确认UI      │     │  WebSocket推送   │
│  - apply_edit   │     │  - 预览对比      │     │  / 轮询同步      │
│  - select_arena │     │  - 多版本选择    │     │                 │
└─────────────────┘     └──────────────────┘     └─────────────────┘
```

### 3.2 工作流程

#### 场景A: AI续写

```
1. 用户: "帮我续写第三章"
2. Agent: 调用 continue_writing_tool 生成续写内容
3. Agent: 调用 request_user_approval 请求用户确认
4. 前端: 显示确认对话框（预览续写内容、插入位置）
5. 用户: 点击"确认应用"
6. Agent: 调用 apply_chapter_edit 将内容写入数据库
7. 前端: 编辑器实时同步更新
```

#### 场景B: AI改写（竞技场）

```
1. 用户: "改写这段话，让它更有悬念感"
2. Agent: 调用 rewrite_arena 生成3个改写版本
3. Agent: 调用 request_version_selection 让用户选择
4. 前端: 显示多版本对比选择器
5. 用户: 选择版本2
6. Agent: 调用 apply_chapter_edit 用选中版本替换原文
7. 前端: 编辑器实时同步更新
```

---

## 4. 详细设计

### 4.1 后端新增工具

#### 4.1.1 `apply_chapter_edit` - 应用章节编辑

```python
# backend/app/services/agent/tools/editor_tools.py

from langchain_core.tools import tool
from typing import Literal

@tool
async def apply_chapter_edit(
    chapter_id: str,
    operation: Literal["append", "replace", "insert"],
    content: str,
    position: int = None,  # insert时需要
    selection_start: int = None,  # replace时需要
    selection_end: int = None,    # replace时需要
    user_id: str = None
) -> dict:
    """
    应用章节编辑操作

    Args:
        chapter_id: 章节UUID
        operation: 操作类型
            - append: 在末尾追加
            - replace: 替换指定范围
            - insert: 在指定位置插入
        content: 要写入的内容
        position: insert操作的插入位置（字符偏移）
        selection_start: replace操作的起始位置
        selection_end: replace操作的结束位置
        user_id: 用户ID（用于权限验证）

    Returns:
        {
            "success": bool,
            "chapter_id": str,
            "operation": str,
            "content_length": int,
            "new_word_count": int
        }
    """
    # 1. 验证UUID格式
    # 2. 验证用户权限
    # 3. 获取当前章节内容
    # 4. 根据operation执行相应操作
    # 5. 调用ChapterService.update_chapter()
    # 6. 返回结果
```

#### 4.1.2 `request_user_approval` - 请求用户确认

```python
@tool
async def request_user_approval(
    action_type: Literal["edit", "select_version"],
    preview_content: str,
    metadata: dict = None
) -> dict:
    """
    请求用户确认操作

    这个工具会暂停Agent执行，等待用户在前端UI中确认或取消。

    Args:
        action_type: 操作类型
            - edit: 编辑确认（显示预览）
            - select_version: 版本选择（多版本对比）
        preview_content: 预览内容（或JSON编码的多版本列表）
        metadata: 额外信息（如操作描述、位置信息等）

    Returns:
        {
            "approved": bool,
            "selected_version": int,  # 仅select_version时有效
            "user_feedback": str      # 用户反馈（可选）
        }
    """
```

### 4.2 前端新增组件

#### 4.2.1 `AgentEditConfirmDialog` - 编辑确认对话框

```typescript
// src/components/agent/AgentEditConfirmDialog.tsx

interface AgentEditConfirmDialogProps {
  isOpen: boolean;
  actionType: 'edit' | 'select_version';
  previewContent: string;
  originalContent?: string;  // 用于对比显示
  versions?: Array<{
    id: number;
    style: string;
    content: string;
  }>;
  metadata?: {
    operation: string;
    position?: string;
    description?: string;
  };
  onConfirm: (selectedVersion?: number) => void;
  onCancel: () => void;
}
```

**UI设计**:
- 模态对话框，居中显示
- 左右分栏对比（原文 vs 新文）
- 差异高亮显示
- 多版本时显示标签页切换
- 确认/取消按钮
- 显示操作描述和影响范围

#### 4.2.2 `AgentVersionSelector` - 多版本选择器

```typescript
// src/components/agent/AgentVersionSelector.tsx

interface AgentVersionSelectorProps {
  versions: Array<{
    version_id: string;
    style: string;
    style_name: string;
    content: string;
    score?: number;
  }>;
  originalText: string;
  onSelect: (versionId: string) => void;
  onCancel: () => void;
}
```

**UI设计**:
- 卡片式布局，每个版本一张卡片
- 显示风格标签（正式、口语、诗意等）
- 悬停预览全文
- 点击选择
- 参考现有的写作竞技场UI

### 4.3 编辑器同步机制

#### 4.3.1 方案对比

| 方案 | 优点 | 缺点 | 推荐场景 |
|------|------|------|----------|
| WebSocket实时推送 | 即时、高效 | 实现复杂、需维护连接 | 多用户协作 |
| 轮询检测更新 | 实现简单 | 延迟、浪费资源 | 简单场景 |
| 事件总线 | 解耦、灵活 | 需要全局状态管理 | 单用户场景 |

**推荐方案**: 事件总线 + 乐观更新

#### 4.3.2 实现方案

```typescript
// src/services/EditorSyncService.ts

class EditorSyncService {
  private eventEmitter = new EventEmitter();

  // Agent完成编辑后触发
  notifyChapterUpdated(chapterId: string, newContent: string) {
    this.eventEmitter.emit('chapter-updated', { chapterId, newContent });
  }

  // 编辑器订阅更新
  onChapterUpdated(callback: (data: { chapterId: string, newContent: string }) => void) {
    this.eventEmitter.on('chapter-updated', callback);
    return () => this.eventEmitter.off('chapter-updated', callback);
  }
}

export const editorSyncService = new EditorSyncService();
```

```typescript
// 在NovelEditor中使用
useEffect(() => {
  const unsubscribe = editorSyncService.onChapterUpdated(({ chapterId, newContent }) => {
    if (chapterId === currentChapterId && editor) {
      // 保存当前光标位置
      const { from } = editor.state.selection;

      // 更新内容
      editor.commands.setContent(newContent);

      // 尝试恢复光标位置
      editor.commands.setTextSelection(Math.min(from, newContent.length));

      // 显示提示
      toast.success('内容已由AI助手更新');
    }
  });

  return unsubscribe;
}, [editor, currentChapterId]);
```

### 4.4 Agent执行流程修改

#### 4.4.1 新增SSE事件类型

```python
# 新增事件类型用于用户确认
class StreamEventType(str, Enum):
    # ... 现有类型 ...
    USER_APPROVAL_REQUEST = "user_approval_request"  # 请求用户确认
    USER_APPROVAL_RESPONSE = "user_approval_response"  # 用户确认响应
    EDITOR_UPDATE = "editor_update"  # 编辑器更新通知
```

#### 4.4.2 确认机制实现

```python
# 在langgraph_agent.py中

async def handle_user_approval_request(state: AgentState, request_data: dict):
    """
    处理用户确认请求

    1. 发送SSE事件到前端，携带预览数据
    2. 等待前端通过API返回用户决定
    3. 根据用户决定继续或取消操作
    """
    # 发送确认请求事件
    yield {
        "type": StreamEventType.USER_APPROVAL_REQUEST,
        "data": request_data
    }

    # 等待用户响应（通过Redis或内存队列）
    approval_result = await wait_for_user_approval(
        conversation_id=state['conversation_id'],
        timeout=300  # 5分钟超时
    )

    return approval_result
```

---

## 5. 文件清单

### 5.1 新增文件

```
backend/
├── app/
│   ├── models/
│   │   └── chapter_history.py               # ~50行 - 历史记录模型
│   └── services/
│       ├── agent/
│       │   └── tools/
│       │       ├── editor_tools.py          # ~300行 - Agent编辑器工具
│       │       ├── position_inferrer.py     # ~100行 - 智能位置推断
│       │       └── style_adapter.py         # ~150行 - 风格自适应
│       ├── chapter_history_service.py       # ~100行 - 历史记录服务
│       └── rate_limiter.py                  # ~50行 - 速率限制器
│
src/
├── components/
│   └── agent/
│       ├── AgentEditConfirmDialog.tsx       # ~350行 - 编辑确认对话框
│       ├── AgentVersionSelector.tsx         # ~300行 - 多版本选择器
│       ├── DiffViewer.tsx                   # ~100行 - Diff差异视图
│       └── UndoAgentEdit.tsx                # ~80行 - 撤销AI编辑
├── components/
│   └── editor/
│       └── ConflictResolutionDialog.tsx     # ~200行 - 冲突解决对话框
├── services/
│   ├── EditorSyncService.ts                 # ~150行 - 编辑器同步服务
│   └── ConflictResolver.ts                  # ~120行 - 冲突解决器
├── styles/
│   └── diff-viewer.css                      # ~30行 - Diff视图样式
```

### 5.2 修改文件

```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── agent_react_stream.py        # 添加确认响应API
│   ├── models/
│   │   └── chapter.py                       # 添加version字段（乐观锁）
│   └── services/
│       ├── agent/
│       │   └── langgraph_agent.py           # 集成新工具、确认机制
│       └── chapter_service.py               # 添加带锁更新方法

src/
├── components/
│   └── editor/
│       └── NovelEditor.tsx                  # 添加同步订阅、版本追踪
├── hooks/
│   └── useAgentChat.ts                      # 处理确认事件
├── components/
│   └── agent/
│       └── AgentChatPanel.tsx               # 集成确认对话框
└── services/
    └── DataService.ts                       # 添加历史恢复API
```

### 5.3 新增依赖

```json
// package.json
{
  "dependencies": {
    "diff-match-patch": "^1.0.5"  // Diff算法库（~20KB）
  },
  "devDependencies": {
    "@types/diff-match-patch": "^1.0.36"
  }
}
```

**新增代码量估计**: ~2100行（后端~750行，前端~1350行）

---

## 6. 接口设计

### 6.1 SSE事件格式

#### 用户确认请求

```json
{
  "type": "user_approval_request",
  "data": {
    "request_id": "req_123456",
    "action_type": "edit",
    "preview": {
      "content": "生成的续写内容...",
      "operation": "append",
      "position": "end",
      "word_count": 350
    },
    "metadata": {
      "description": "续写第三章，增加350字",
      "timestamp": "2025-11-23T10:30:00Z"
    }
  }
}
```

#### 多版本选择请求

```json
{
  "type": "user_approval_request",
  "data": {
    "request_id": "req_123457",
    "action_type": "select_version",
    "original_text": "原始文本...",
    "versions": [
      {
        "version_id": "v1",
        "style": "formal",
        "style_name": "正式风格",
        "content": "改写版本1..."
      },
      {
        "version_id": "v2",
        "style": "casual",
        "style_name": "口语风格",
        "content": "改写版本2..."
      },
      {
        "version_id": "v3",
        "style": "poetic",
        "style_name": "诗意风格",
        "content": "改写版本3..."
      }
    ]
  }
}
```

### 6.2 用户确认响应API

```
POST /api/v1/agent/approval-response

Request Body:
{
  "request_id": "req_123456",
  "approved": true,
  "selected_version": "v2",  // 仅多版本选择时
  "user_feedback": "选择口语风格"
}

Response:
{
  "success": true,
  "message": "Approval recorded"
}
```

---

## 7. 用户交互设计

### 7.1 确认对话框UI

```
┌─────────────────────────────────────────────────────────────┐
│  ⚠️ AI助手请求修改编辑器内容                           [×]  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  操作: 在章节末尾追加续写内容                                │
│  字数: +350字                                               │
│                                                             │
│  ┌─────────────────────┐  ┌─────────────────────┐           │
│  │ 原文（最后200字）    │  │ 新增内容预览        │           │
│  │                     │  │                     │           │
│  │ ...他缓缓走向门口   │  │ 门外的风雪呼啸而过 │           │
│  │ ，心中充满了不安。  │  │ ，他紧了紧衣领，  │           │
│  │                     │  │ 迈出了决定性的...  │           │
│  └─────────────────────┘  └─────────────────────┘           │
│                                                             │
│                              [取消]  [确认应用]              │
└─────────────────────────────────────────────────────────────┘
```

### 7.2 多版本选择器UI

```
┌─────────────────────────────────────────────────────────────┐
│  ✨ 选择改写版本                                      [×]  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  原文: "他走进房间，看到了一片混乱。"                        │
│                                                             │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐│
│  │ 正式风格        │ │ 口语风格        │ │ 诗意风格        ││
│  │                 │ │                 │ │                 ││
│  │ 他迈入室内，   │ │ 他一推门，好   │ │ 他踏入那片     ││
│  │ 映入眼帘的是   │ │ 家伙，里面简   │ │ 混沌，仿佛     ││
│  │ 一片狼藉。     │ │ 直乱成一锅粥。 │ │ 踏入梦境...    ││
│  │                 │ │                 │ │                 ││
│  │    [选择]       │ │    [选择]       │ │    [选择]       ││
│  └─────────────────┘ └─────────────────┘ └─────────────────┘│
│                                                             │
│                                           [取消]            │
└─────────────────────────────────────────────────────────────┘
```

### 7.3 编辑器更新提示

```
┌────────────────────────────────┐
│ ✅ 内容已由AI助手更新          │
│    +350字已追加到章节末尾      │
└────────────────────────────────┘
```

---

## 8. 安全与并发控制

### 8.1 权限验证

1. **用户身份验证**: 通过JWT token验证用户身份
2. **章节所有权验证**: 确认章节属于当前用户的作品
3. **操作范围限制**: Agent只能修改当前会话关联的章节

### 8.2 乐观锁机制 (防止并发冲突)

#### 8.2.1 数据库模型修改

```python
# backend/app/models/chapter.py

class Chapter(Base):
    # ... 现有字段 ...
    version = Column(Integer, default=1, nullable=False)  # 版本号
    last_modified_by = Column(String, nullable=True)  # 最后修改者(user/agent)
    last_modified_at = Column(DateTime, default=func.now(), onupdate=func.now())
```

#### 8.2.2 乐观锁实现

```python
# backend/app/services/chapter_service.py

async def update_chapter_with_lock(
    self,
    chapter_id: str,
    chapter_data: ChapterUpdate,
    expected_version: int,
    modifier: str = "user"  # "user" or "agent"
) -> tuple[Optional[Chapter], str]:
    """
    带乐观锁的章节更新

    Returns:
        (chapter, error_message)
        成功时返回 (chapter, "")
        失败时返回 (None, "conflict" | "not_found")
    """
    chapter = await self.get_chapter_by_id(chapter_id)
    if not chapter:
        return (None, "not_found")

    # 检查版本号
    if chapter.version != expected_version:
        return (None, "conflict")

    # 更新数据
    update_data = chapter_data.model_dump(exclude_unset=True)
    update_data["version"] = chapter.version + 1
    update_data["last_modified_by"] = modifier

    for field, value in update_data.items():
        setattr(chapter, field, value)

    await self.db.commit()
    await self.db.refresh(chapter)

    return (chapter, "")
```

#### 8.2.3 前端版本追踪

```typescript
// src/store/editorStore.ts 或 NovelEditor.tsx

interface ChapterState {
  chapterId: string;
  content: string;
  version: number;  // 当前版本号
  isDirty: boolean;
}

// 加载章节时保存版本号
const loadChapter = async (chapterId: string) => {
  const chapter = await DataService.getChapter(chapterId);
  setChapterState({
    chapterId: chapter.id,
    content: chapter.content,
    version: chapter.version,
    isDirty: false
  });
};

// 保存时携带版本号
const saveChapter = async () => {
  const result = await DataService.updateChapter(chapterId, {
    content: newContent,
    expected_version: chapterState.version
  });

  if (result.error === 'conflict') {
    // 显示冲突解决对话框
    showConflictDialog(result.server_content, newContent);
  } else {
    // 更新本地版本号
    setChapterState(prev => ({ ...prev, version: result.version }));
  }
};
```

### 8.3 自动备份到历史记录

#### 8.3.1 历史记录数据模型

```python
# backend/app/models/chapter_history.py

class ChapterHistory(Base):
    __tablename__ = "chapter_histories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chapter_id = Column(UUID(as_uuid=True), ForeignKey("chapters.id"), nullable=False)
    content = Column(Text, nullable=False)
    word_count = Column(Integer, default=0)
    version = Column(Integer, nullable=False)
    modified_by = Column(String, nullable=False)  # "user" | "agent"
    operation = Column(String, nullable=True)  # "append" | "replace" | "insert" | "manual"
    description = Column(String, nullable=True)  # 操作描述
    created_at = Column(DateTime, default=func.now())

    # 关联
    chapter = relationship("Chapter", back_populates="histories")
```

#### 8.3.2 自动保存历史

```python
# backend/app/services/chapter_history_service.py

class ChapterHistoryService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save_history(
        self,
        chapter_id: str,
        content: str,
        version: int,
        modified_by: str,
        operation: str = None,
        description: str = None
    ) -> ChapterHistory:
        """保存章节历史版本"""
        history = ChapterHistory(
            chapter_id=chapter_id,
            content=content,
            word_count=calculate_word_count(content),
            version=version,
            modified_by=modified_by,
            operation=operation,
            description=description
        )
        self.db.add(history)
        await self.db.commit()
        return history

    async def get_histories(
        self,
        chapter_id: str,
        limit: int = 20
    ) -> List[ChapterHistory]:
        """获取章节历史记录"""
        result = await self.db.execute(
            select(ChapterHistory)
            .where(ChapterHistory.chapter_id == chapter_id)
            .order_by(ChapterHistory.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())

    async def restore_version(
        self,
        chapter_id: str,
        history_id: str
    ) -> Optional[Chapter]:
        """恢复到指定历史版本"""
        history = await self.db.get(ChapterHistory, history_id)
        if not history or str(history.chapter_id) != chapter_id:
            return None

        chapter_service = ChapterService(self.db)
        return await chapter_service.update_chapter(
            chapter_id,
            ChapterUpdate(content=history.content)
        )
```

#### 8.3.3 在Agent编辑前自动备份

```python
# backend/app/services/agent/tools/editor_tools.py

@tool
async def apply_chapter_edit(...):
    # 1. 获取当前章节
    chapter = await chapter_service.get_chapter_by_id(chapter_id)

    # 2. 保存当前内容到历史记录
    history_service = ChapterHistoryService(db)
    await history_service.save_history(
        chapter_id=chapter_id,
        content=chapter.content,
        version=chapter.version,
        modified_by="agent",
        operation=operation,
        description=f"Agent {operation}: +{len(content)}字"
    )

    # 3. 执行编辑操作
    # ...
```

### 8.4 操作速率限制

#### 8.4.1 速率限制服务

```python
# backend/app/services/rate_limiter.py

from app.core.redis import redis_client

class RateLimiter:
    def __init__(self, key_prefix: str, limit: int, window: int):
        """
        Args:
            key_prefix: Redis key前缀
            limit: 时间窗口内最大请求数
            window: 时间窗口（秒）
        """
        self.key_prefix = key_prefix
        self.limit = limit
        self.window = window

    async def check(self, identifier: str) -> tuple[bool, int]:
        """
        检查是否超过速率限制

        Returns:
            (is_allowed, remaining)
        """
        key = f"{self.key_prefix}:{identifier}"

        # 使用Redis INCR + EXPIRE实现滑动窗口
        current = await redis_client.incr(key)
        if current == 1:
            await redis_client.expire(key, self.window)

        remaining = max(0, self.limit - current)
        is_allowed = current <= self.limit

        return (is_allowed, remaining)

# Agent编辑速率限制器
agent_edit_limiter = RateLimiter(
    key_prefix="agent_edit",
    limit=10,      # 每分钟最多10次
    window=60      # 60秒窗口
)
```

#### 8.4.2 在工具中应用

```python
@tool
async def apply_chapter_edit(chapter_id: str, ..., user_id: str):
    # 检查速率限制
    is_allowed, remaining = await agent_edit_limiter.check(user_id)
    if not is_allowed:
        return {
            "success": False,
            "error": "rate_limit_exceeded",
            "message": f"操作过于频繁，请稍后再试。剩余配额将在1分钟后恢复。",
            "retry_after": 60
        }

    # 继续执行...
```

### 8.5 冲突智能合并

#### 8.5.1 冲突检测与处理流程

```typescript
// src/services/ConflictResolver.ts

import { diff_match_patch } from 'diff-match-patch';

interface ConflictResolution {
  strategy: 'keep_user' | 'keep_agent' | 'merge' | 'manual';
  mergedContent?: string;
  conflicts?: Array<{
    position: number;
    userText: string;
    agentText: string;
  }>;
}

class ConflictResolver {
  private dmp = new diff_match_patch();

  /**
   * 尝试智能合并两个版本的内容
   */
  async resolve(
    baseContent: string,      // 原始内容
    userContent: string,      // 用户修改后的内容
    agentContent: string      // Agent修改后的内容
  ): Promise<ConflictResolution> {

    // 1. 计算两边的差异
    const userPatches = this.dmp.patch_make(baseContent, userContent);
    const agentPatches = this.dmp.patch_make(baseContent, agentContent);

    // 2. 检查是否有重叠修改
    const hasOverlap = this.checkPatchOverlap(userPatches, agentPatches);

    if (!hasOverlap) {
      // 3. 无重叠，可以自动合并
      const [merged, results] = this.dmp.patch_apply(
        [...userPatches, ...agentPatches],
        baseContent
      );

      if (results.every(r => r)) {
        return {
          strategy: 'merge',
          mergedContent: merged
        };
      }
    }

    // 4. 有重叠，需要用户手动选择
    return {
      strategy: 'manual',
      conflicts: this.extractConflicts(baseContent, userContent, agentContent)
    };
  }

  private checkPatchOverlap(patches1: any[], patches2: any[]): boolean {
    // 检查两组补丁是否有位置重叠
    for (const p1 of patches1) {
      for (const p2 of patches2) {
        const start1 = p1.start1;
        const end1 = start1 + p1.length1;
        const start2 = p2.start1;
        const end2 = start2 + p2.length1;

        if (!(end1 <= start2 || end2 <= start1)) {
          return true; // 有重叠
        }
      }
    }
    return false;
  }

  private extractConflicts(base: string, user: string, agent: string) {
    // 提取具体冲突位置
    // ...实现细节
  }
}

export const conflictResolver = new ConflictResolver();
```

#### 8.5.2 冲突解决对话框

```typescript
// src/components/editor/ConflictResolutionDialog.tsx

interface ConflictResolutionDialogProps {
  isOpen: boolean;
  baseContent: string;
  userContent: string;
  agentContent: string;
  agentOperation: string;  // 描述Agent做了什么
  onResolve: (resolution: 'keep_user' | 'keep_agent' | 'merge', mergedContent?: string) => void;
  onCancel: () => void;
}

// UI显示三栏对比：
// - 左侧：用户的修改
// - 中间：合并预览（如果可自动合并）
// - 右侧：Agent的修改
```

### 8.6 内容安全

1. **内容长度限制**: 单次编辑最大10000字符
2. **XSS防护**: 对Agent生成的内容进行HTML转义
3. **敏感词过滤**: 可选的敏感词检测（调用后端过滤API）

---

## 9. 测试计划

### 9.1 单元测试

- [ ] `apply_chapter_edit`工具的各种操作类型
- [ ] UUID验证和权限验证
- [ ] 内容长度和位置边界检查

### 9.2 集成测试

- [ ] Agent续写 → 确认 → 应用 完整流程
- [ ] Agent改写 → 多版本选择 → 应用 完整流程
- [ ] 用户取消操作的处理
- [ ] 超时情况的处理

### 9.3 E2E测试

- [ ] 编辑器实时同步更新
- [ ] 多标签页/多设备同步
- [ ] 网络中断后的恢复

---

## 10. 性能优化详细设计

### 10.1 事件总线 + 乐观更新

#### 10.1.1 事件总线实现

```typescript
// src/services/EditorSyncService.ts

import { EventEmitter } from 'events';

interface EditorUpdateEvent {
  chapterId: string;
  content: string;
  operation: 'append' | 'replace' | 'insert';
  position?: { start: number; end: number };
  version: number;
  source: 'agent' | 'sync';
}

class EditorSyncService extends EventEmitter {
  private pendingUpdates: Map<string, EditorUpdateEvent[]> = new Map();

  /**
   * 乐观更新 - 立即更新UI，后台同步数据库
   */
  optimisticUpdate(event: EditorUpdateEvent) {
    // 1. 立即触发UI更新
    this.emit('chapter-updated', event);

    // 2. 记录待同步的更新
    const updates = this.pendingUpdates.get(event.chapterId) || [];
    updates.push(event);
    this.pendingUpdates.set(event.chapterId, updates);

    // 3. 防抖同步到后端
    this.debouncedSync(event.chapterId);
  }

  private syncTimers: Map<string, NodeJS.Timeout> = new Map();

  private debouncedSync(chapterId: string) {
    // 清除之前的定时器
    const existing = this.syncTimers.get(chapterId);
    if (existing) clearTimeout(existing);

    // 设置新的防抖定时器
    const timer = setTimeout(async () => {
      await this.syncToBackend(chapterId);
    }, 1000); // 1秒防抖

    this.syncTimers.set(chapterId, timer);
  }

  private async syncToBackend(chapterId: string) {
    const updates = this.pendingUpdates.get(chapterId);
    if (!updates || updates.length === 0) return;

    try {
      // 合并所有更新，只同步最终状态
      const finalUpdate = updates[updates.length - 1];

      await DataService.updateChapter(chapterId, {
        content: finalUpdate.content,
        expected_version: finalUpdate.version - 1
      });

      // 清除已同步的更新
      this.pendingUpdates.delete(chapterId);
    } catch (error) {
      console.error('[EditorSync] 同步失败:', error);
      this.emit('sync-error', { chapterId, error });
    }
  }

  /**
   * 订阅章节更新
   */
  onUpdate(callback: (event: EditorUpdateEvent) => void): () => void {
    this.on('chapter-updated', callback);
    return () => this.off('chapter-updated', callback);
  }
}

export const editorSyncService = new EditorSyncService();
```

### 10.2 增量预览 (Diff视图)

#### 10.2.1 Diff渲染组件

```typescript
// src/components/agent/DiffViewer.tsx

import { diff_match_patch, DIFF_DELETE, DIFF_INSERT, DIFF_EQUAL } from 'diff-match-patch';

interface DiffViewerProps {
  original: string;
  modified: string;
  showLineNumbers?: boolean;
  maxHeight?: number;
}

export const DiffViewer: React.FC<DiffViewerProps> = ({
  original,
  modified,
  showLineNumbers = true,
  maxHeight = 400
}) => {
  const dmp = useMemo(() => new diff_match_patch(), []);

  const diffs = useMemo(() => {
    const rawDiffs = dmp.diff_main(original, modified);
    dmp.diff_cleanupSemantic(rawDiffs);
    return rawDiffs;
  }, [original, modified, dmp]);

  // 计算统计信息
  const stats = useMemo(() => {
    let added = 0, removed = 0;
    diffs.forEach(([op, text]) => {
      if (op === DIFF_INSERT) added += text.length;
      if (op === DIFF_DELETE) removed += text.length;
    });
    return { added, removed };
  }, [diffs]);

  return (
    <div className="diff-viewer">
      {/* 统计栏 */}
      <div className="diff-stats px-3 py-2 bg-gray-100 border-b text-xs">
        <span className="text-green-600">+{stats.added}字</span>
        <span className="mx-2">|</span>
        <span className="text-red-600">-{stats.removed}字</span>
      </div>

      {/* 差异内容 */}
      <div
        className="diff-content p-3 overflow-y-auto font-mono text-sm"
        style={{ maxHeight }}
      >
        {diffs.map(([op, text], index) => {
          let className = '';
          if (op === DIFF_INSERT) {
            className = 'bg-green-100 text-green-800';
          } else if (op === DIFF_DELETE) {
            className = 'bg-red-100 text-red-800 line-through';
          }

          return (
            <span key={index} className={className}>
              {text}
            </span>
          );
        })}
      </div>
    </div>
  );
};
```

#### 10.2.2 样式定义

```css
/* src/styles/diff-viewer.css */

.diff-viewer {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  overflow: hidden;
}

.diff-content {
  white-space: pre-wrap;
  word-break: break-all;
  line-height: 1.6;
}

/* 删除的文本 */
.diff-content .bg-red-100 {
  background-color: #fee2e2;
  color: #991b1b;
  text-decoration: line-through;
}

/* 新增的文本 */
.diff-content .bg-green-100 {
  background-color: #dcfce7;
  color: #166534;
}
```

### 10.3 懒加载版本内容

```typescript
// src/components/agent/AgentVersionSelector.tsx

interface VersionSummary {
  version_id: string;
  style: string;
  style_name: string;
  preview: string;      // 前100字预览
  word_count: number;
  loaded: boolean;
  content?: string;     // 完整内容（懒加载）
}

export const AgentVersionSelector: React.FC<Props> = ({
  versions: initialVersions,
  originalText,
  onSelect,
  onCancel
}) => {
  const [versions, setVersions] = useState<VersionSummary[]>(
    initialVersions.map(v => ({
      ...v,
      preview: v.content.substring(0, 100) + (v.content.length > 100 ? '...' : ''),
      word_count: v.content.length,
      loaded: false
    }))
  );

  const [expandedVersion, setExpandedVersion] = useState<string | null>(null);
  const [loading, setLoading] = useState<string | null>(null);

  // 点击展开时加载完整内容
  const handleExpand = async (versionId: string) => {
    if (expandedVersion === versionId) {
      setExpandedVersion(null);
      return;
    }

    const version = versions.find(v => v.version_id === versionId);
    if (!version) return;

    // 如果未加载，先加载
    if (!version.loaded) {
      setLoading(versionId);
      // 模拟加载（实际场景中内容已在初始数据中）
      await new Promise(resolve => setTimeout(resolve, 200));

      setVersions(prev => prev.map(v =>
        v.version_id === versionId
          ? { ...v, loaded: true, content: initialVersions.find(iv => iv.version_id === versionId)?.content }
          : v
      ));
      setLoading(null);
    }

    setExpandedVersion(versionId);
  };

  return (
    <div className="version-selector grid grid-cols-1 md:grid-cols-3 gap-4">
      {versions.map(version => (
        <div
          key={version.version_id}
          className={`version-card border-2 rounded-xl p-4 cursor-pointer transition-all
            ${expandedVersion === version.version_id ? 'border-blue-500 shadow-lg' : 'border-gray-200 hover:border-blue-300'}`}
          onClick={() => handleExpand(version.version_id)}
        >
          {/* 风格标签 */}
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-semibold text-gray-800">{version.style_name}</span>
            <span className="text-xs text-gray-500">{version.word_count}字</span>
          </div>

          {/* 内容预览/完整 */}
          <div className="text-sm text-gray-600 mb-3">
            {expandedVersion === version.version_id && version.loaded
              ? version.content
              : version.preview}
          </div>

          {/* 加载中 */}
          {loading === version.version_id && (
            <div className="text-xs text-blue-500">加载中...</div>
          )}

          {/* 选择按钮 */}
          <button
            onClick={(e) => {
              e.stopPropagation();
              onSelect(version.version_id);
            }}
            className="w-full py-2 bg-blue-500 text-white text-sm font-medium rounded-lg hover:bg-blue-600"
          >
            选择此版本
          </button>
        </div>
      ))}
    </div>
  );
};
```

---

## 11. 智能化增强详细设计

### 11.1 智能位置推断

```python
# backend/app/services/agent/tools/position_inferrer.py

from typing import Literal, Optional
import re

class PositionInferrer:
    """智能推断内容插入位置"""

    def infer_position(
        self,
        chapter_content: str,
        operation: str,
        user_intent: str,
        context: dict = None
    ) -> dict:
        """
        根据用户意图推断最佳插入位置

        Args:
            chapter_content: 章节当前内容
            operation: 操作类型 (append/insert/replace)
            user_intent: 用户意图描述
            context: 额外上下文（如选中文本位置）

        Returns:
            {
                "position": "end" | "cursor" | "after_paragraph" | int,
                "confidence": float,  # 0-1
                "reason": str
            }
        """

        # 1. 如果有选中文本，优先使用选中位置
        if context and context.get('selection'):
            return {
                "position": context['selection'],
                "confidence": 1.0,
                "reason": "用户已选中目标位置"
            }

        # 2. 根据关键词推断
        intent_lower = user_intent.lower()

        # 续写类意图 -> 末尾
        if any(kw in intent_lower for kw in ['续写', '继续', '接着写', '往下写']):
            return {
                "position": "end",
                "confidence": 0.95,
                "reason": "续写意图，插入到章节末尾"
            }

        # 开头类意图 -> 开头
        if any(kw in intent_lower for kw in ['开头', '开篇', '第一段']):
            return {
                "position": 0,
                "confidence": 0.9,
                "reason": "开头意图，插入到章节开头"
            }

        # 特定段落意图 -> 查找段落
        paragraph_match = re.search(r'第(\d+)段', user_intent)
        if paragraph_match:
            para_num = int(paragraph_match.group(1))
            position = self._find_paragraph_position(chapter_content, para_num)
            return {
                "position": position,
                "confidence": 0.85,
                "reason": f"在第{para_num}段后插入"
            }

        # 3. 默认：末尾
        return {
            "position": "end",
            "confidence": 0.7,
            "reason": "默认插入到末尾"
        }

    def _find_paragraph_position(self, content: str, para_num: int) -> int:
        """查找第N段的结束位置"""
        paragraphs = content.split('\n\n')
        if para_num > len(paragraphs):
            return len(content)

        # 计算前N段的总长度
        position = 0
        for i in range(para_num):
            position += len(paragraphs[i])
            if i < para_num:
                position += 2  # 段落分隔符

        return position

position_inferrer = PositionInferrer()
```

### 11.2 风格自适应

```python
# backend/app/services/agent/tools/style_adapter.py

from typing import List
import json

class StyleAdapter:
    """根据章节现有风格推荐改写风格"""

    # 风格特征词
    STYLE_FEATURES = {
        "formal": ["然而", "因此", "此外", "综上所述", "显而易见"],
        "casual": ["其实", "反正", "不过", "话说", "简直"],
        "poetic": ["宛如", "仿佛", "恰似", "犹如", "如同"],
        "suspense": ["突然", "竟然", "居然", "不料", "岂料"],
        "humorous": ["哈哈", "嘿嘿", "竟敢", "偏偏", "倒是"]
    }

    def analyze_style(self, content: str) -> dict:
        """
        分析文本风格特征

        Returns:
            {
                "primary_style": str,
                "style_scores": dict,
                "features": list
            }
        """
        style_scores = {}
        found_features = []

        for style, features in self.STYLE_FEATURES.items():
            score = 0
            for feature in features:
                count = content.count(feature)
                if count > 0:
                    score += count
                    found_features.append({"style": style, "feature": feature, "count": count})

            style_scores[style] = score

        # 找出主要风格
        primary_style = max(style_scores, key=style_scores.get) if any(style_scores.values()) else "neutral"

        return {
            "primary_style": primary_style,
            "style_scores": style_scores,
            "features": found_features
        }

    def recommend_styles(self, content: str, num_recommendations: int = 3) -> List[dict]:
        """
        根据内容风格推荐改写风格

        Returns:
            [
                {"style": "formal", "reason": "当前文本偏口语，推荐正式风格作为对比"},
                ...
            ]
        """
        analysis = self.analyze_style(content)
        primary = analysis["primary_style"]

        # 推荐策略：相似风格 + 对比风格 + 增强风格
        recommendations = []

        # 1. 相似风格（保持）
        if primary != "neutral":
            recommendations.append({
                "style": primary,
                "style_name": self._get_style_name(primary),
                "reason": f"保持当前{self._get_style_name(primary)}"
            })

        # 2. 对比风格
        contrast_map = {
            "formal": "casual",
            "casual": "formal",
            "poetic": "casual",
            "suspense": "humorous",
            "humorous": "suspense"
        }
        if primary in contrast_map:
            contrast = contrast_map[primary]
            recommendations.append({
                "style": contrast,
                "style_name": self._get_style_name(contrast),
                "reason": f"对比风格：{self._get_style_name(contrast)}"
            })

        # 3. 其他风格
        all_styles = list(self.STYLE_FEATURES.keys())
        for style in all_styles:
            if len(recommendations) >= num_recommendations:
                break
            if style not in [r["style"] for r in recommendations]:
                recommendations.append({
                    "style": style,
                    "style_name": self._get_style_name(style),
                    "reason": f"尝试{self._get_style_name(style)}"
                })

        return recommendations[:num_recommendations]

    def _get_style_name(self, style: str) -> str:
        names = {
            "formal": "正式风格",
            "casual": "口语风格",
            "poetic": "诗意风格",
            "suspense": "悬疑风格",
            "humorous": "幽默风格",
            "neutral": "中性风格"
        }
        return names.get(style, style)

style_adapter = StyleAdapter()
```

### 11.3 在Agent工具中使用

```python
# backend/app/services/agent/tools/editor_tools.py

from .position_inferrer import position_inferrer
from .style_adapter import style_adapter

@tool
async def smart_insert(
    chapter_id: str,
    content: str,
    user_intent: str,
    user_id: str
) -> dict:
    """
    智能插入内容 - 自动推断最佳位置

    Args:
        chapter_id: 章节ID
        content: 要插入的内容
        user_intent: 用户的意图描述
        user_id: 用户ID
    """
    # 获取章节
    chapter = await chapter_service.get_chapter_by_id(chapter_id)

    # 智能推断位置
    position_result = position_inferrer.infer_position(
        chapter_content=chapter.content,
        operation="insert",
        user_intent=user_intent
    )

    # 执行插入
    # ...

    return {
        "success": True,
        "position": position_result["position"],
        "confidence": position_result["confidence"],
        "reason": position_result["reason"]
    }


@tool
async def smart_rewrite(
    chapter_id: str,
    text_to_rewrite: str,
    user_id: str
) -> dict:
    """
    智能改写 - 自动推荐适合的风格

    自动分析章节风格，推荐3种改写风格供用户选择
    """
    # 获取章节
    chapter = await chapter_service.get_chapter_by_id(chapter_id)

    # 分析风格并推荐
    recommendations = style_adapter.recommend_styles(chapter.content)

    # 调用rewrite_arena生成多版本
    versions = await rewrite_arena(
        text=text_to_rewrite,
        styles=[r["style"] for r in recommendations]
    )

    return {
        "success": True,
        "original_text": text_to_rewrite,
        "style_analysis": style_adapter.analyze_style(chapter.content),
        "recommendations": recommendations,
        "versions": versions
    }
```

---

## 12. 用户体验优化

### 12.1 快捷键支持

```typescript
// src/components/agent/AgentEditConfirmDialog.tsx

useEffect(() => {
  const handleKeyDown = (e: KeyboardEvent) => {
    if (!isOpen) return;

    switch (e.key) {
      case 'Enter':
        if (!e.shiftKey) {
          e.preventDefault();
          onConfirm();
        }
        break;
      case 'Escape':
        e.preventDefault();
        onCancel();
        break;
      case '1':
      case '2':
      case '3':
        if (actionType === 'select_version' && versions) {
          const index = parseInt(e.key) - 1;
          if (versions[index]) {
            e.preventDefault();
            onConfirm(index);
          }
        }
        break;
    }
  };

  window.addEventListener('keydown', handleKeyDown);
  return () => window.removeEventListener('keydown', handleKeyDown);
}, [isOpen, actionType, versions, onConfirm, onCancel]);
```

### 12.2 撤销AI编辑

```typescript
// src/components/editor/UndoAgentEdit.tsx

interface UndoAgentEditProps {
  chapterId: string;
  lastAgentEdit?: {
    historyId: string;
    operation: string;
    timestamp: string;
    wordCount: number;
  };
}

export const UndoAgentEdit: React.FC<UndoAgentEditProps> = ({
  chapterId,
  lastAgentEdit
}) => {
  const [isLoading, setIsLoading] = useState(false);

  if (!lastAgentEdit) return null;

  const handleUndo = async () => {
    if (!confirm('确定要撤销AI的修改吗？')) return;

    setIsLoading(true);
    try {
      await DataService.restoreChapterHistory(chapterId, lastAgentEdit.historyId);
      toast.success('已撤销AI编辑');
    } catch (error) {
      toast.error('撤销失败');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <button
      onClick={handleUndo}
      disabled={isLoading}
      className="flex items-center gap-1.5 px-3 py-1.5 text-xs text-orange-600 bg-orange-50 rounded-lg hover:bg-orange-100"
    >
      <Undo2 className="w-3.5 h-3.5" />
      撤销AI编辑 ({lastAgentEdit.operation})
    </button>
  );
};
```

### 10.4 可扩展性设计

1. **插件化工具**: 使用装饰器模式注册新的编辑工具
2. **自定义确认流程**: 允许用户配置哪些操作需要确认
3. **操作历史回溯**: 保存所有AI编辑操作，支持回溯和审计

### 10.5 借鉴市面流行Agent

1. **Cursor IDE**:
   - Diff视图显示变更
   - 逐行/逐块确认
   - 快捷键操作

2. **GitHub Copilot Chat**:
   - 内联代码建议
   - 一键应用
   - 解释变更

3. **Notion AI**:
   - 选中文本右键菜单
   - 保留原文选项
   - 风格预设

**建议采用**:
- Cursor的Diff视图 + 逐块确认
- Notion AI的风格预设
- 自研的写作竞技场多版本对比

---

## 11. 实现路线图

### Phase 1: 基础功能 (预计3天)

1. 实现`apply_chapter_edit`后端工具
2. 实现`AgentEditConfirmDialog`前端组件
3. 实现编辑器同步服务
4. 集成到Agent执行流程

### Phase 2: 多版本选择 (预计2天)

1. 集成`rewrite_arena`工具
2. 实现`AgentVersionSelector`组件
3. 实现版本选择API

### Phase 3: 优化完善 (预计2天)

1. Diff差异高亮
2. 撤销功能
3. 快捷键支持
4. 性能优化

### Phase 4: 测试上线 (预计1天)

1. 完成测试用例
2. 修复发现的问题
3. 编写用户文档
4. 上线发布

**总计**: 约8个工作日

---

## 12. 相关文档

- [对话持久化功能说明](./conversation-persistence-feature.md)
- [ReAct记忆模块README](./REACT-MEMORY-README.md)
- [后端已完成但前端未实现的API接口文档](./后端已完成但前端未实现的API接口文档.md)

---

## 13. 附录

### 13.1 相关代码位置

| 功能 | 文件路径 |
|------|----------|
| Agent主逻辑 | `backend/app/services/agent/langgraph_agent.py` |
| 工具注册表 | `backend/app/services/agent/tools/tool_registry.py` |
| 写作工具 | `backend/app/services/agent/tools/writing_tools.py` |
| 高级工具 | `backend/app/services/agent/tools/advanced_tools.py` |
| 章节API | `backend/app/api/v1/chapters.py` |
| 章节服务 | `backend/app/services/chapter_service.py` |
| 编辑器组件 | `src/components/editor/NovelEditor.tsx` |
| AI续写抽屉 | `src/components/editor/AIContinueDrawer.tsx` |
| 数据服务 | `src/services/DataService.ts` |

### 13.2 SSE事件流示例

```
data: {"type": "thinking", "content": "正在分析您的请求..."}

data: {"type": "tool_call", "tool": "continue_writing", "input": {...}}

data: {"type": "tool_result", "tool": "continue_writing", "output": {...}}

data: {"type": "user_approval_request", "data": {...}}

// 等待用户确认...

data: {"type": "tool_call", "tool": "apply_chapter_edit", "input": {...}}

data: {"type": "tool_result", "tool": "apply_chapter_edit", "output": {...}}

data: {"type": "editor_update", "chapter_id": "xxx", "operation": "append"}

data: {"type": "done", "content": "已为您续写350字并添加到章节末尾。"}
```

---

**文档版本**: v1.0
**最后更新**: 2025-11-23
**作者**: Claude AI Assistant
