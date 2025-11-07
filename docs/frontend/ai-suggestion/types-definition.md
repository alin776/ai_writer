# 类型定义文件

本文档说明AI建议功能所需的TypeScript类型定义。

---

## 📦 创建类型文件

### 文件路径
```
src/types/ai-suggestion.ts
```

### 完整代码

```typescript
/**
 * AI建议相关类型定义
 */

/**
 * AI建议对象
 */
export interface AISuggestion {
  /** 唯一标识符 */
  id: string;

  /** 生成的文本内容 */
  content: string;

  /** ProseMirror起始位置 */
  startPos: number;

  /** ProseMirror结束位置 */
  endPos: number;

  /** 建议状态 */
  status: 'pending' | 'accepted' | 'rejected';

  /** 创建时间戳 */
  createdAt: number;
}

/**
 * useAISuggestion Hook配置选项
 */
export interface UseAISuggestionOptions {
  /** 接受建议时的回调 */
  onAccept?: (suggestion: AISuggestion) => void;

  /** 拒绝建议时的回调 */
  onReject?: (suggestion: AISuggestion) => void;

  /** 开始新建议时的回调 */
  onStart?: (suggestionId: string) => void;
}

/**
 * startSuggestion方法的配置选项
 */
export interface StartSuggestionOptions {
  /** 插入模式 */
  mode?: 'cursor' | 'end' | 'auto';

  /** 精确插入位置（优先级高于mode） */
  position?: number;
}

/**
 * AIPendingMark的属性
 */
export interface AIPendingAttributes {
  /** 关联的建议ID */
  suggestionId: string;
}

/**
 * Toast消息类型
 */
export type ToastType = 'success' | 'error' | 'info' | 'warning';

/**
 * Toast消息对象
 */
export interface ToastMessage {
  /** 消息唯一ID */
  id: string;

  /** 消息类型 */
  type: ToastType;

  /** 消息文本 */
  message: string;

  /** 显示时长（毫秒），默认3000 */
  duration?: number;
}

/**
 * 键盘快捷键配置
 */
export interface KeyboardShortcut {
  /** 按键名称 */
  key: string;

  /** 是否需要Ctrl/Command键 */
  ctrl?: boolean;

  /** 是否需要Shift键 */
  shift?: boolean;

  /** 是否需要Alt键 */
  alt?: boolean;

  /** 快捷键处理函数 */
  handler: (event: KeyboardEvent) => void;

  /** 快捷键描述 */
  description?: string;
}
```

---

## 📝 使用示例

### 在组件中使用

```typescript
import type { AISuggestion, ToastMessage } from '@/types/ai-suggestion';

function MyComponent() {
  const [suggestion, setSuggestion] = useState<AISuggestion | null>(null);
  const [toasts, setToasts] = useState<ToastMessage[]>([]);

  // ...
}
```

### 在Hook中使用

```typescript
import type {
  UseAISuggestionOptions,
  StartSuggestionOptions
} from '@/types/ai-suggestion';

export const useAISuggestion = (
  editor: Editor | null,
  options?: UseAISuggestionOptions
) => {
  const startSuggestion = (opts?: StartSuggestionOptions) => {
    // ...
  };

  // ...
};
```

---

## 🔧 扩展类型

如果需要扩展类型，可以使用TypeScript的继承：

```typescript
// src/types/ai-suggestion-extended.ts

import type { AISuggestion } from './ai-suggestion';

/**
 * 扩展的AI建议类型（包含更多元数据）
 */
export interface ExtendedAISuggestion extends AISuggestion {
  /** 生成使用的模型 */
  model?: string;

  /** 生成耗时（毫秒） */
  duration?: number;

  /** 用户评分（1-5） */
  rating?: number;

  /** 拒绝原因 */
  rejectionReason?: string;
}
```

---

## 📚 相关文档

- [状态管理](./02-state-management.md) - 使用这些类型
- [API参考](./api-reference.md) - 完整API说明
- [集成指南](./integration-guide.md) - 如何集成到项目
