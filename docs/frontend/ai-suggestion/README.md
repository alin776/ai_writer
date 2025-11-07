# AI建议功能 - 总览文档

## 📋 功能概述

实现AI生成内容在编辑器中的实时预览与确认机制，提供流畅的用户体验。

### 核心交互流程

```
用户发起请求 → 两侧同步展示 → 用户确认决策

右侧（Agent卡片）          左侧（编辑器）
     ↓                         ↓
[⚪ 生成中...]  ←────────→  [实时流式插入]
     ↓                         ↓
[展开完整内容]  ←────────→  [待确认高亮状态]
 [✓] [✗]                    [黄色背景+虚线框]
     ↓                         ↓
点击[✓] → 编辑器内容变为正式文本
点击[✗] → 编辑器内容直接删除
```

## 🎯 设计目标

1. **实时同步**：AI生成内容实时显示在编辑器中
2. **明确状态**：通过视觉样式区分待确认内容
3. **简洁操作**：符号化按钮（✓/✗）快速确认
4. **流畅体验**：动画过渡自然，反馈及时

## 🏗️ 架构设计

```
EditorView (Container)
├── EditorContext (共享状态)
│   ├── editor instance
│   └── aiSuggestion state
├── NovelEditor (Left)
│   ├── AIPendingMark 扩展
│   └── 待确认内容高亮
└── AgentChatPanel (Right)
    └── AISuggestionCard
        ├── ⚪ 生成中状态
        ├── ✓/✗ 操作按钮
        └── ✅/❌ 确认反馈
```

## 📦 技术栈

- **编辑器**：Tiptap (ProseMirror)
- **状态管理**：React Context + Custom Hook
- **流式传输**：SSE (Server-Sent Events)
- **样式方案**：CSS Modules + 自定义动画

## 📚 文档导航

### 核心实现

- [架构设计](./01-architecture.md) - 整体架构与数据流
- [状态管理](./02-state-management.md) - AI建议状态管理系统 (Phase 1)
- [Agent卡片](./03-agent-card.md) - 右侧卡片UI实现 (Phase 2)
- [编辑器同步](./04-editor-sync.md) - 实时同步机制 (Phase 3)
- [交互实现](./05-interaction.md) - 确认/拒绝交互 (Phase 4)

### 集成与优化

- [集成测试](./06-integration.md) - EditorView集成 (Phase 5)
- [UX优化](./07-ux-optimization.md) - 体验优化 (Phase 6)

### 参考文档

- [API参考](./api-reference.md) - 所有API接口说明
- [组件Props](./component-props.md) - 组件属性详解
- [样式规范](./style-guide.md) - CSS样式规范
- [使用示例](./examples.md) - 完整代码示例

## 🎨 符号系统

| 符号 | 含义 | 使用场景 |
|------|------|----------|
| ⚪ | 生成中 | Agent卡片收起状态（旋转动画） |
| ✓ | 接受 | 操作按钮（绿色） |
| ✗ | 拒绝 | 操作按钮（灰色） |
| ✅ | 已采纳 | 确认后提示 |
| ❌ | 已拒绝 | 拒绝后提示 |

## ⚡ 快捷键

- `Tab` → 接受当前建议
- `Esc` → 拒绝当前建议

## 🚀 快速开始

查看 [集成测试文档](./06-integration.md) 了解如何在项目中使用。

## 📝 开发进度

- [ ] Phase 1: 状态管理系统
- [ ] Phase 2: Agent卡片UI
- [ ] Phase 3: 编辑器同步
- [ ] Phase 4: 交互实现
- [ ] Phase 5: 集成测试
- [ ] Phase 6: UX优化
