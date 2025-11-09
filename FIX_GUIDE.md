# 快速修复指南

## 概览
需要修复 4 个问题，总预期时间: < 20 分钟

---

## 修复 1: 删除 chatReactStream() 函数 (P0)

### 步骤 1: 打开文件
文件: src/services/agentApi.ts

### 步骤 2: 定位要删除的代码
查找行号: 97-186

完整函数如下所示:
```typescript
async chatReactStream(
  request: AgentChatRequest,
  callbacks: {
    onStart?: (conversationId: string) => void;
    onProgress?: (progress: any) => void;
    onToolCall?: (toolCall: any) => void;
    onContent?: (content: string) => void;
    onDone?: (result: any) => void;
    onError?: (error: string) => void;
  }
): Promise<void> {
  // ... 整个函数体 (90 行代码)
}
```

### 步骤 3: 删除函数
完全删除第 97-186 行 (整个函数定义)

### 步骤 4: 验证
- [ ] 删除后文件仍然编译正常
- [ ] 没有语法错误

### 预期耗时: 2 分钟

---

## 修复 2: 更新 useAgentChatStream.ts (P0)

### 步骤 1: 打开文件
文件: src/hooks/useAgentChatStream.ts

### 步骤 2: 修改 sendMessage 函数

**原代码 (第 128-137 行)**:
```typescript
const request: AgentChatRequest = {
  message,
  conversation_id: conversationId || undefined,
  ...requestOptions,
};

// 调用API
await agentApi.chatReactStream(request, {
```

**改为**:
```typescript
const request: AgentChatRequest = {
  message,
  mode: 'react',  // ✅ 新增: 明确指定 React 模式
  conversation_id: conversationId || undefined,
  ...requestOptions,
};

// 调用API
await agentApi.chatStream(request, {  // ✅ 改为: chatStream()
```

### 步骤 3: 保持所有回调不变
回调函数列表保持不变:
```typescript
{
  onStart: (convId) => { ... },
  onProgress: (progress) => { ... },
  onToolCall: (toolCall) => { ... },
  onContent: (chunk) => { ... },
  onDone: (data) => { ... },
  onError: (errorMsg) => { ... }
}
```

### 步骤 4: 验证
- [ ] 文件编译无误
- [ ] 所有回调都正确传递

### 预期耗时: 3 分钟

---

## 修复 3: 清理 AgentChatPanel.tsx 中的未使用变量 (P1)

### 步骤 1: 打开文件
文件: src/components/agent/AgentChatPanel.tsx

### 步骤 2: 删除未使用的状态
**查找第 46 行的代码**:
```typescript
const [useStreaming, setUseStreaming] = useState(true);
```

**删除这一行**: 注释掉或删除

### 步骤 3: 检查使用
搜索 "setUseStreaming" 和 "useStreaming"，确保：
- [ ] 没有其他地方使用这些变量
- [ ] 删除后代码仍然运行

### 步骤 4: 验证条件逻辑
当前代码中:
```typescript
if (useStreaming) {
  // 使用流式响应
  await sendMessageStream(request);
} else {
  // 使用普通响应
  const response = await sendMessage(request);
  if (response?.conversation_id) {
    setConversationId(response.conversation_id);
  }
}
```

**改为** (总是使用流式):
```typescript
// 总是使用流式响应
await sendMessageStream(request);
```

### 预期耗时: 2 分钟

---

## 修复 4: 处理 ModeSelector 的 compact 参数 (P1)

### 选项 A: 删除未使用的参数 (推荐)

**步骤 1**: 打开 src/components/agent/ModeSelector.tsx

**步骤 2**: 修改 ModeSelectorProps 接口
```typescript
// 删除 compact 参数
interface ModeSelectorProps {
  mode: AgentMode;
  onModeChange: (mode: AgentMode) => void;
  // ❌ 删除: compact?: boolean;
  disabled?: boolean;
}
```

**步骤 3**: 删除函数参数
```typescript
export default function ModeSelector({
  mode,
  onModeChange,
  // ❌ 删除: compact = false,
  disabled = false
}: ModeSelectorProps) {
```

### 选项 B: 实现 compact 模式 (如果需要)

如果未来需要紧凑模式，保留参数并实现逻辑：
```typescript
{compact && (
  // 紧凑模式渲染
)}
{!compact && (
  // 完整模式渲染
)}
```

### 推荐: 选择 A (删除)

### 预期耗时: 1 分钟

---

## 修复 5 (可选): 完善 AIPanel.tsx (P2)

### 步骤 1: 打开文件
文件: src/components/editor/AIPanel.tsx

### 步骤 2: 修改请求对象
**原代码 (第 159-166 行)**:
```typescript
const request: AgentChatRequest = {
  message: inputValue.trim(),
  work_id: workId,
  chapter_id: chapterId,
  context: {
    chapter_context: chapterId ? `当前章节ID: ${chapterId}` : undefined,
  },
};
```

**改为**:
```typescript
const request: AgentChatRequest = {
  message: inputValue.trim(),
  mode: 'planning',  // ✅ 添加: 默认为 planning 模式
  work_id: workId,
  chapter_id: chapterId,
  context: {
    chapter_context: chapterId ? `当前章节ID: ${chapterId}` : undefined,
  },
};
```

### 步骤 3: 验证
- [ ] 编译无误
- [ ] mode 字段正确传递

### 预期耗时: 1 分钟

---

## 验证检查清单

修复完成后，执行以下检查:

### 编译检查
```bash
npm run build
# 或
npx tsc --noEmit
```

验证:
- [ ] 无新的编译错误
- [ ] 类型检查通过

### 导入检查
验证所有导入:
- [ ] chatReactStream 不再被导入或使用
- [ ] chatStream 被正确使用

### 功能检查
- [ ] AgentChatPanel 能正常渲染
- [ ] ModeSelector 能正常切换模式
- [ ] AIPanel 能正常发送消息

### 代码质量
- [ ] 删除了所有未使用的变量
- [ ] 删除了冗余的函数
- [ ] 代码结构清晰

---

## 修复摘要

| 修复 | 优先级 | 耗时 | 状态 |
|-----|------|------|------|
| 删除 chatReactStream() | P0 | 2 min | [ ] |
| 更新 useAgentChatStream.ts | P0 | 3 min | [ ] |
| 清理 AgentChatPanel.tsx | P1 | 2 min | [ ] |
| 处理 compact 参数 | P1 | 1 min | [ ] |
| 完善 AIPanel.tsx | P2 | 1 min | [ ] |

**总耗时**: 约 9 分钟

---

## 常见问题

Q: 删除 chatReactStream() 后，useAgentChatStream 会出错吗?
A: 不会，因为我们会同时更新 useAgentChatStream.ts 使用 chatStream()

Q: 为什么要删除 useStreaming 状态?
A: 因为代码中总是使用流式响应，这个状态是死代码

Q: AIPanel 不传递 mode 会有问题吗?
A: 不会，mode 是可选的，会使用后端默认值。但为了完整性建议添加

Q: 修复后需要测试吗?
A: 是的，修复后应该运行编译检查和基本功能测试

---

## 完成确认

完成所有修复后:

```
✅ 所有 P0 问题已修复
✅ 所有 P1 问题已修复
✅ P2 问题已考虑
✅ 编译检查通过
✅ 代码质量提升
```

然后可以提交 Pull Request
