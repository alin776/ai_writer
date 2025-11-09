# ModeSelector 集成方案对比

## 方案1：输入框上方左侧（推荐）⭐

**位置**：在AgentChatPanel的输入框容器上方

**优点**：
- ✅ 位置醒目，用户容易发现
- ✅ 不占用输入框内部空间
- ✅ 与VS Code Copilot布局一致
- ✅ 可以显示当前模式的完整描述

**效果图**：
```
┌─────────────────────────────────────┐
│ 消息列表区域                         │
│                                     │
├─────────────────────────────────────┤
│ [💬 Ask ▼]     快速问答，简单咨询    │  ← 模式选择器在这里
├─────────────────────────────────────┤
│ [                              ]    │  ← 输入框
│ [📎] [发送]                         │
└─────────────────────────────────────┘
```

**代码修改**：

### AgentChatPanel.tsx（修改行179-185）

```typescript
// 添加mode状态
const [mode, setMode] = useState<AgentMode>('plan'); // 默认Plan模式

// ...

{/* 输入框区域 */}
<div className="px-4 py-3 border-t border-gray-200">
  {/* 模式选择器 - 输入框上方 */}
  <div className="flex items-center justify-between mb-2">
    <ModeSelector
      mode={mode}
      onModeChange={setMode}
      disabled={isLoading}
    />
    <div className="text-[10px] text-gray-400">
      {MODE_CONFIG[mode].description}
    </div>
  </div>

  <ChatInput
    onSend={handleSendMessage}
    disabled={isLoading}
    placeholder="试试：帮我写第三章..."
  />
</div>
```

---

## 方案2：输入框左侧

**位置**：在ChatInput组件内部，textarea左侧

**优点**：
- ✅ 节省垂直空间
- ✅ 紧凑布局
- ✅ 所有输入控件在一行

**缺点**：
- ⚠️ 输入框可用宽度变小
- ⚠️ 位置可能不够显眼

**效果图**：
```
┌─────────────────────────────────────┐
│ 消息列表区域                         │
│                                     │
├─────────────────────────────────────┤
│ [💬▼] [                    ] [📎][发送]│  ← 模式选择器在左侧
│        输入框                        │
└─────────────────────────────────────┘
```

**代码修改**：

### ChatInput.tsx（修改行114-149）

```typescript
// 添加props
interface ChatInputProps {
  onSend: (message: string, context?: any) => void;
  disabled?: boolean;
  placeholder?: string;
  maxLength?: number;
  mode?: AgentMode;           // ← 新增
  onModeChange?: (mode: AgentMode) => void;  // ← 新增
}

// ...

{/* 主输入框 */}
<div className="flex items-end gap-2">
  {/* 左侧：模式选择器（可选） */}
  {mode && onModeChange && (
    <div className="flex-shrink-0">
      <ModeSelector
        mode={mode}
        onModeChange={onModeChange}
        disabled={disabled}
        compact  // 紧凑模式
      />
    </div>
  )}

  {/* 中间：输入框 */}
  <div className="flex-1 relative">
    <textarea ... />
    {/* 字符计数 */}
  </div>

  {/* 右侧：工具按钮 */}
  <div className="flex gap-1.5">
    <button>📎</button>
    <button>发送</button>
  </div>
</div>
```

---

## 方案3：输入框下方左侧（备选）

**位置**：在提示文本那一行的左侧

**效果图**：
```
┌─────────────────────────────────────┐
│ [                              ]    │  ← 输入框
│ [📎] [发送]                         │
├─────────────────────────────────────┤
│ [💬 Ask ▼]  按Enter发送 · Shift+Enter换行│  ← 模式选择器
└─────────────────────────────────────┘
```

**代码修改**：

### ChatInput.tsx（修改行182-187）

```typescript
{/* 底部：模式选择器 + 提示文本 */}
<div className="mt-1.5 flex items-center justify-between">
  {/* 左侧：模式选择器 */}
  {mode && onModeChange && (
    <ModeSelector
      mode={mode}
      onModeChange={onModeChange}
      disabled={disabled}
      compact
    />
  )}

  {/* 右侧：提示文本 */}
  <div className="text-[10px] text-gray-500">
    <span>按 Enter 发送</span>
    <span className="mx-1.5">·</span>
    <span>Shift + Enter 换行</span>
  </div>
</div>
```

---

## 推荐方案：方案1 ⭐

**理由**：
1. **参考VS Code Copilot**：微软的成熟设计，用户熟悉
2. **位置醒目**：用户容易发现和使用
3. **空间充足**：可以显示模式描述，帮助用户理解
4. **不影响输入框**：保持输入框的完整性

**实施步骤**：
1. ✅ 已创建 `ModeSelector.tsx`
2. 修改 `AgentChatPanel.tsx` 添加mode状态
3. 在输入框上方添加ModeSelector组件
4. 根据mode调用不同的API

---

## 视觉效果对比

### 方案1（推荐）
```
┌───────────────────────────────────────────┐
│           消息列表区域                      │
│                                           │
├───────────────────────────────────────────┤
│ 💬 Ask ▼              快速问答，简单咨询  │  ← 清晰明显
├───────────────────────────────────────────┤
│ ┌─────────────────────────────────┐      │
│ │ 试试：帮我写第三章...            │      │
│ └─────────────────────────────────┘      │
│                          [📎] [发送]      │
└───────────────────────────────────────────┘
```

### 方案2
```
┌───────────────────────────────────────────┐
│           消息列表区域                      │
│                                           │
├───────────────────────────────────────────┤
│ [💬▼] ┌────────────────┐ [📎] [发送]     │  ← 紧凑但可能不显眼
│       │ 试试：帮我写... │                 │
│       └────────────────┘                  │
└───────────────────────────────────────────┘
```

### 方案3
```
┌───────────────────────────────────────────┐
│ ┌─────────────────────────────────┐      │
│ │ 试试：帮我写第三章...            │      │
│ └─────────────────────────────────┘      │
│                          [📎] [发送]      │
├───────────────────────────────────────────┤
│ [💬 Ask ▼]    按Enter发送 · Shift+Enter换行│  ← 位置偏下
└───────────────────────────────────────────┘
```

---

## 你觉得哪个方案更好？

我个人推荐**方案1**，理由：
1. 位置最显眼 ✅
2. 符合VS Code设计 ✅
3. 用户体验最好 ✅

但如果你有其他想法，我们也可以调整！🎨
