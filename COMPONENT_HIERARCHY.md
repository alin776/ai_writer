# 组件层级关系与集成状态

## 当前应用层级结构

```
应用根 (App)
│
├── 路由: /works/:workId (WorkDetailView)
│   │
│   └── WorkDetailView
│       │
│       ├── 左侧: ChapterList (章节列表)
│       │
│       ├── 中间: NovelEditor (小说编辑器)
│       │
│       └── 右侧面板 (RightPanel)
│           │
│           ├── 标签栏: [世界观] [概括] [AI]
│           │
│           └── 内容区域（根据标签切换）
│               ├── [世界观] → WorldviewPanel ✓
│               ├── [概括] → SummaryPanel ✓
│               └── [AI] → AIPanel ❌ 无 ModeSelector
│
├── 路由: /editor/:chapterId (EditorView) [备选方案]
│   │
│   └── EditorView
│       │
│       ├── 中间: NovelEditor (小说编辑器)
│       │
│       └── 右侧浮动面板
│           └── AgentChatPanel ✅ 包含 ModeSelector
│               │
│               ├── 头部: 标题 + ModeSelector
│               ├── 消息区: AgentMessage 列表
│               ├── 建议操作: SuggestedActions
│               └── 输入区: ChatInput + 发送按钮
│
└── 组件库 (/components/agent/)
    │
    ├── ModeSelector ✅ 已创建
    │   ├── 两种模式切换: Planning | ReAct
    │   ├── 下拉菜单 UI
    │   └── 支持禁用状态
    │
    └── AgentChatPanel ✅ 已集成 ModeSelector
        ├── AgentMessage (单条消息)
        ├── ChatInput (输入框)
        ├── SuggestedActions (建议操作)
        ├── TaskListPanel (任务清单)
        └── ThinkingIndicator (思考指示)
```

---

## 文件位置地图

### 主要视图 (Views)
```
src/views/
├── WorkDetailView/
│   └── index.tsx ← 用户当前看到的界面
│       └── 渲染 AIPanel
│
└── EditorView/
    └── index.tsx ← 备选界面
        └── 渲染 AgentChatPanel (已集成 ModeSelector)
```

### 面板组件 (Panels)
```
src/components/editor/
├── AIPanel.tsx ❌ 问题: 硬编码 mode='planning'
├── WorldviewPanel.tsx ✓
└── SummaryPanel.tsx ✓

src/components/agent/
├── AgentChatPanel.tsx ✅ 已整合
├── ModeSelector.tsx ✅ 已创建
├── AgentMessage.tsx ✓
├── ChatInput.tsx ✓
├── TaskListPanel.tsx ✓
├── SuggestedActions.tsx ✓
├── ThinkingIndicator.tsx ✓
└── ProgressIndicator.tsx ✓
```

---

## 为什么看不到 ModeSelector？

### 问题分析流程图

```
用户在 WorkDetailView 看到 AI 面板
    │
    ├─ 点击右侧标签栏的 [AI]
    │
    └─ 触发 setRightPanel('agent')
           │
           ├─ 条件判断: rightPanel === 'agent'
           │
           └─ 渲染: <AIPanel workId={...} chapterId={...} />
                  │
                  ├─ AIPanel 是轻量级组件
                  ├─ 没有导入 ModeSelector
                  ├─ 没有 mode 状态
                  ├─ 发送消息时: mode: 'planning' ← 硬编码!
                  │
                  └─ 结果: 用户看不到 ModeSelector ❌
```

### 对比: AgentChatPanel 路径

```
用户在 EditorView 看到 Agent 面板
    │
    ├─ 点击右侧浮动按钮 (MessageSquare 图标)
    │
    └─ 触发 setSidebarType('agent')
           │
           ├─ 条件判断: sidebarType === 'agent'
           │
           └─ 渲染: <AgentChatPanel workId={...} chapterId={...} />
                  │
                  ├─ AgentChatPanel 是完整组件
                  ├─ 导入了 ModeSelector
                  ├─ 有 mode 状态管理
                  ├─ 头部渲染 ModeSelector
                  ├─ 发送消息时: mode ← 动态值
                  │
                  └─ 结果: 用户看到 ModeSelector ✅
```

---

## 代码对比: AIPanel vs AgentChatPanel

### AIPanel 的 handleSend

```tsx
const handleSend = async () => {
  if (!inputValue.trim() || isLoading) return;

  const request: AgentChatRequest = {
    message: inputValue.trim(),
    mode: 'planning',  // ❌ 硬编码!
    work_id: workId,
    chapter_id: chapterId,
    // ...
  };

  await sendMessageStream(request);
};
```

### AgentChatPanel 的 handleSendMessage

```tsx
const [mode, setMode] = useState<AgentMode>('planning');

const handleSendMessage = async (message: string, context?: any) => {
  const request = {
    message,
    mode,  // ✅ 动态值
    work_id: workId,
    chapter_id: chapterId,
    // ...
  };

  if (useStreaming) {
    await sendMessageStream(request);
  }
};
```

---

## 组件 Props 对比

### AIPanel Props
```tsx
interface AIPanelProps {
  workId: string;
  chapterId?: string;
}
// ❌ 没有 mode 相关的 props
```

### AgentChatPanel Props
```tsx
interface AgentChatPanelProps {
  workId?: string;
  chapterId?: string;
  initialMessage?: string;
  className?: string;
}
// ✅ 内部管理 mode 状态
```

---

## 修复方案对比

### 方案 A: 改进 AIPanel (推荐)
```
改动范围: 小
复杂度: 低
影响面: 仅 WorkDetailView
风险: 低

步骤:
1. 导入 ModeSelector
2. 添加 mode 状态: const [mode, setMode] = useState<AgentMode>('planning')
3. 在输入框上方显示 ModeSelector
4. handleSend 中使用 mode 替代硬编码

改动行数: ~20 行
```

### 方案 B: 替换为 AgentChatPanel (激进)
```
改动范围: 中
复杂度: 中
影响面: WorkDetailView 的导入和渲染逻辑
风险: 中(需要测试样式兼容)

步骤:
1. 在 WorkDetailView 中导入 AgentChatPanel
2. 替换 AIPanel 的渲染调用
3. 调整样式确保布局一致

改动行数: ~10 行
好处: 获得完整的 Agent 功能
```

---

## 立即可采取的行动

### 1. 验证 ModeSelector 的创建
```bash
ls -la src/components/agent/ModeSelector.tsx
```
✅ 文件存在

### 2. 确认 AgentChatPanel 的集成
```bash
grep -n "ModeSelector" src/components/agent/AgentChatPanel.tsx
```
✅ 已导入并使用

### 3. 识别 AIPanel 的问题
```bash
grep -n "mode:" src/components/editor/AIPanel.tsx
```
❌ 第 161 行硬编码为 'planning'

### 4. 推荐下一步
**执行方案 A**: 在 AIPanel 中集成 ModeSelector
