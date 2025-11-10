# Add to Chat 功能 - v1.2 修订说明

## 📋 修订概述

**修订版本：** v1.2
**修订日期：** 2025-01-10
**修订原因：** 根据用户需求，将"填充输入框"模式改为"引用块"模式，提供更现代化的用户体验

---

## 🔑 核心变更

### v1.0/v1.1 的设计（旧）

**交互方式：** 选中文字 → 直接填充到输入框

```
┌──────────────────────────────┐
│ Agent 聊天面板                │
├──────────────────────────────┤
│ （历史消息）                  │
├──────────────────────────────┤
│ ┌──────────────────────────┐ │
│ │ UI简化显示逻辑 (20分钟)   │ │ ← 选中的文字直接填充在输入框
│ │ █                        │ │
│ └──────────────────────────┘ │
│ [发送]                        │
└──────────────────────────────┘
```

**问题：**
- ❌ 输入框被选中文字占用
- ❌ 用户需要手动清除或编辑选中文字
- ❌ 无法清晰区分"参考内容"和"用户问题"
- ❌ 不符合现代聊天工具的使用习惯

---

### v1.2 的设计（新）✨

**交互方式：** 选中文字 → 变成引用块

```
┌──────────────────────────────┐
│ Agent 聊天面板                │
├──────────────────────────────┤
│ （历史消息）                  │
├──────────────────────────────┤
│ ┌─────────────────────────┐  │
│ │ 📎 引用: filename.md    │  │ ← 引用块（参考内容）
│ │ ───────────────────────│  │
│ │ UI简化显示逻辑 (20分钟) │  │
│ │                 [×移除] │  │
│ └─────────────────────────┘  │
│                              │
│ ┌─────────────────────────┐  │
│ │ 在这里输入提示词...      │  │ ← 输入框（干净）
│ │ █                       │  │
│ └─────────────────────────┘  │
│ [发送]                        │
└──────────────────────────────┘
```

**优势：**
- ✅ 输入框保持干净，用户专注输入提示词
- ✅ 引用块清晰展示参考内容
- ✅ 可以随时移除引用
- ✅ 类似微信/Telegram的引用回复，用户熟悉
- ✅ 上下文和问题分离明确

---

## 🎯 用户体验对比

### 使用场景：询问任务详情

#### v1.0/v1.1 的体验（旧）

```
1. 用户选中："UI简化显示逻辑 (20分钟)"
2. 点击 Add to Chat
3. 输入框中显示：
   "UI简化显示逻辑 (20分钟)█"
4. 用户需要：
   - 把光标移到最后
   - 加个换行
   - 输入："这个任务要怎么做？"
5. 最终输入框内容：
   "UI简化显示逻辑 (20分钟)
    这个任务要怎么做？"
```

**问题：** 需要手动编辑，容易出错

---

#### v1.2 的体验（新）✨

```
1. 用户选中："UI简化显示逻辑 (20分钟)"
2. 点击 Add to Chat
3. 显示：
   ┌──────────────────────────┐
   │ 📎 引用: ...md    [×移除]│
   │ ─────────────────────────│
   │ UI简化显示逻辑 (20分钟)   │
   └──────────────────────────┘

   ┌──────────────────────────┐
   │ █                        │ ← 光标直接在输入框
   └──────────────────────────┘
4. 用户直接输入："这个任务要怎么做？"
5. 点击发送
```

**优势：** 直接输入，无需编辑

---

## 📊 技术实现对比

### 数据结构变化

#### v1.0/v1.1（旧）

```typescript
interface AddToChatConfig {
  text: string;          // 选中的文字
  mode: 'fill' | 'send'; // 填充模式或发送模式
  timestamp: number;
}

// 使用方式
setAddToChatText("UI简化显示逻辑", 'fill');

// 在AgentChatPanel中
setInputValue(text);  // 直接填充到输入框
```

---

#### v1.2（新）✨

```typescript
// 新增 Reference 类型
interface Reference {
  id: string;        // 唯一ID
  content: string;   // 引用内容
  source?: string;   // 来源文件
  timestamp: number; // 时间戳
}

interface AddToChatConfig {
  reference: Reference;  // 引用对象（不是纯文本）
  timestamp: number;
}

// 使用方式
setAddToChatReference("UI简化显示逻辑", "REACT_VERIFICATION_REPORT.md");

// 在AgentChatPanel中
setCurrentReference(reference);  // 设置引用
// 输入框保持空白
```

---

### UI组件变化

#### v1.0/v1.1（旧）

```typescript
// AgentChatPanel.tsx
useEffect(() => {
  if (addToChatConfig) {
    const { text } = addToChatConfig;
    setInputValue(text);  // ❌ 直接填充到输入框
  }
}, [addToChatConfig]);

return (
  <ChatInput
    value={inputValue}  // 包含选中的文字
    onChange={setInputValue}
  />
);
```

---

#### v1.2（新）✨

```typescript
// 新增 ReferenceBlock 组件
<ReferenceBlock
  reference={currentReference}
  onRemove={handleRemoveReference}
/>

// AgentChatPanel.tsx
useEffect(() => {
  if (addToChatConfig) {
    const { reference } = addToChatConfig;
    setCurrentReference(reference);  // ✅ 设置引用块
    // 输入框不变！
  }
}, [addToChatConfig]);

return (
  <>
    {/* ✨ 引用块 */}
    {currentReference && (
      <ReferenceBlock
        reference={currentReference}
        onRemove={() => setCurrentReference(null)}
      />
    )}

    {/* 输入框（空白） */}
    <ChatInput
      value={inputValue}  // 不包含引用内容
      onChange={setInputValue}
      placeholder="在这里输入提示词..."
    />
  </>
);
```

---

### 发送消息的变化

#### v1.0/v1.1（旧）

```typescript
const handleSend = () => {
  // inputValue 直接包含了选中的文字
  await agentApi.chatStream({
    message: inputValue,  // "UI简化显示逻辑\n这个任务要怎么做？"
    work_id,
    chapter_id,
  });
};
```

---

#### v1.2（新）✨

```typescript
const handleSend = () => {
  let message = inputValue;  // 只是用户输入的提示词

  if (currentReference) {
    // ✨ 将引用内容和用户问题组合
    message = `参考内容：
${currentReference.content}

用户问题：
${inputValue}`;
  }

  await agentApi.chatStream({
    message,
    work_id,
    chapter_id,
  });

  // 清空引用和输入框
  setCurrentReference(null);
  setInputValue('');
};
```

---

## 🎨 UI设计参考

### 类似产品的引用功能

**1. 微信引用回复**
```
┌────────────────────────┐
│ [Alice的消息]          │
│  │引用                 │
│  ↓                     │
│ ┌───────────────────┐  │
│ │ 我们明天几点见？   │  │ ← 引用块
│ └───────────────────┘  │
│ 好的，上午10点          │ ← 回复内容
└────────────────────────┘
```

**2. Telegram 引用回复**
```
┌────────────────────────┐
│ Alice                  │
│ ┌───────────────────┐  │
│ │ 明天会议几点？     │  │ ← 引用块
│ └───────────────────┘  │
│ 上午10点               │ ← 回复内容
│ 12:35                  │
└────────────────────────┘
```

**3. Discord 引用回复**
```
┌────────────────────────┐
│ @Alice                 │
│ ▌明天会议几点？  ← 引用│
│                        │
│ 上午10点               │ ← 回复内容
│ Today at 12:35         │
└────────────────────────┘
```

**我们的设计（v1.2）：**
```
┌────────────────────────┐
│ 📎 引用: filename.md   │ ← 引用块
│ ──────────────────────│
│ 选中的文字内容         │
│              [×移除]   │
└────────────────────────┘
┌────────────────────────┐
│ 输入框...             │ ← 用户问题
└────────────────────────┘
```

---

## ✅ 需要修改的文件

### 已创建的新文档
1. ✅ `02_Add_to_Chat功能设计_v1.2修订版.md` - 完整的v1.2设计文档
2. ✅ `00_总览_v1.1修订版.md` - 已更新交互流程图

### 需要新增的代码文件
1. 🆕 `src/types/agent.ts` - 添加 `Reference` 类型定义
2. 🆕 `src/components/agent/ReferenceBlock.tsx` - 引用块组件
3. 🆕 `src/components/agent/ReferenceBlock.module.css` - 引用块样式

### 需要修改的现有文件
1. ✏️ `src/store/editorStore.ts` - 修改状态管理（text → reference）
2. ✏️ `src/components/editor/BubbleMenu.tsx` - 修改调用方法
3. ✏️ `src/components/agent/AgentChatPanel.tsx` - 集成引用块显示

---

## 🚀 迁移指南

### 如果你已经基于v1.0/v1.1开始开发

#### 步骤1：更新类型定义
```typescript
// src/types/agent.ts

// ✨ 新增
export interface Reference {
  id: string;
  content: string;
  source?: string;
  timestamp: number;
}

// ✏️ 修改
export interface AddToChatConfig {
  reference: Reference;  // 改为 reference 对象
  timestamp: number;
  // ❌ 删除 mode: 'fill' | 'send'
}
```

#### 步骤2：更新 Zustand Store
```typescript
// src/store/editorStore.ts

// ❌ 删除
setAddToChatText: (text: string, mode: 'fill' | 'send') => void;

// ✅ 新增
setAddToChatReference: (text: string, source?: string) => void;
```

#### 步骤3：创建 ReferenceBlock 组件
参考 `02_Add_to_Chat功能设计_v1.2修订版.md` 第2节

#### 步骤4：修改 AgentChatPanel
```typescript
// ❌ 删除：填充输入框逻辑
setInputValue(text);

// ✅ 新增：设置引用块
setCurrentReference(reference);
```

---

## 📝 总结

### v1.2 的核心优势

1. ✅ **用户体验更好** - 输入框干净，操作更直观
2. ✅ **上下文更清晰** - 引用块明确展示参考内容
3. ✅ **符合现代习惯** - 类似主流聊天工具
4. ✅ **可扩展性强** - 未来可支持多个引用
5. ✅ **减少操作步骤** - 无需手动编辑输入框

### 推荐

**强烈建议使用 v1.2 设计**，提供更现代化的用户体验！

---

**版本:** v1.2 修订说明
**日期:** 2025-01-10
**作者:** Claude & 开发团队

**参考文档：**
- [02_Add_to_Chat功能设计_v1.2修订版.md](./02_Add_to_Chat功能设计_v1.2修订版.md)
- [00_总览_v1.1修订版.md](./00_总览_v1.1修订版.md)
