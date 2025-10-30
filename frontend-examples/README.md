# Agent智能助手 - 前端完整示例代码

> **版本**: v1.0
> **更新时间**: 2025-10-29
> **状态**: ✅ 生产就绪

---

## 📁 目录结构

```
frontend-examples/
├── components/agent/          # Agent组件
│   ├── AgentChatPanel.tsx    # 主对话面板
│   ├── AgentMessage.tsx      # 消息显示组件
│   ├── ChatInput.tsx         # 输入框组件
│   ├── SuggestedActions.tsx  # 建议操作组件
│   └── ThinkingIndicator.tsx # 思考指示器
├── hooks/
│   └── useAgentChat.ts       # Agent对话Hook
├── services/
│   └── agentApi.ts           # API服务封装
├── types/
│   └── agent.ts              # TypeScript类型定义
├── pages/
│   └── agent-demo.tsx        # 完整示例页面
└── README.md                 # 本文档
```

---

## 🚀 快速开始

### 1. 安装依赖

```bash
npm install axios react-markdown react-syntax-highlighter
npm install --save-dev @types/react-syntax-highlighter
```

或使用yarn:

```bash
yarn add axios react-markdown react-syntax-highlighter
yarn add --dev @types/react-syntax-highlighter
```

### 2. 配置环境变量

创建 `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. 复制代码到项目

将以下文件复制到你的项目中：

```bash
# 组件
cp components/agent/* your-project/src/components/agent/

# Hooks
cp hooks/useAgentChat.ts your-project/src/hooks/

# 服务
cp services/agentApi.ts your-project/src/services/

# 类型
cp types/agent.ts your-project/src/types/
```

### 4. 使用组件

```tsx
import AgentChatPanel from '@/components/agent/AgentChatPanel';

export default function YourPage() {
  return (
    <div className="h-screen">
      <AgentChatPanel
        workId="your-work-id"
        chapterId="your-chapter-id"
      />
    </div>
  );
}
```

---

## 📦 组件说明

### AgentChatPanel - 主对话面板

**功能特性**:
- ✅ 支持4个核心场景（写作/规划/分析/卡文）
- ✅ 显示Agent思考过程
- ✅ 建议操作按钮
- ✅ Markdown渲染
- ✅ 历史记录管理
- ✅ 快捷开始按钮

**Props**:
```typescript
interface AgentChatPanelProps {
  workId?: string;         // 作品ID
  chapterId?: string;      // 章节ID
  initialMessage?: string; // 初始消息
  className?: string;      // 自定义样式
}
```

**示例**:
```tsx
<AgentChatPanel
  workId="work-123"
  chapterId="chapter-456"
  initialMessage="帮我写第三章"
  className="custom-class"
/>
```

---

### AgentMessage - 消息显示组件

**功能特性**:
- ✅ Markdown渲染（支持代码高亮）
- ✅ 思考过程展开/折叠
- ✅ Token统计显示
- ✅ 复制消息功能
- ✅ 意图图标显示

**Props**:
```typescript
interface AgentMessageProps {
  message: Message;      // 消息对象
  isLatest?: boolean;    // 是否最新消息（动画效果）
}
```

---

### ChatInput - 输入框组件

**功能特性**:
- ✅ 多行输入（自动调整高度）
- ✅ Enter发送, Shift+Enter换行
- ✅ 字符计数
- ✅ 附加上下文
- ✅ 禁用状态

**Props**:
```typescript
interface ChatInputProps {
  onSend: (message: string, context?: any) => void;
  disabled?: boolean;
  placeholder?: string;
  maxLength?: number;     // 默认2000
}
```

---

### SuggestedActions - 建议操作

**功能特性**:
- ✅ 智能图标匹配
- ✅ 点击快速发送
- ✅ 悬停效果

**Props**:
```typescript
interface SuggestedActionsProps {
  actions: string[];
  onActionClick: (action: string) => void;
}
```

---

## 🎣 Hooks说明

### useAgentChat

**功能特性**:
- ✅ 消息状态管理
- ✅ API调用封装
- ✅ 错误处理
- ✅ 重试机制

**返回值**:
```typescript
interface UseAgentChatReturn {
  messages: Message[];              // 消息列表
  isLoading: boolean;               // 加载状态
  error: string | null;             // 错误信息
  suggestedActions: string[];       // 建议操作
  sendMessage: (request) => Promise<AgentChatResponse | null>;
  clearMessages: () => void;        // 清空消息
  retryLastMessage: () => Promise<void>; // 重试最后一条消息
}
```

**使用示例**:
```typescript
const {
  messages,
  sendMessage,
  isLoading,
  suggestedActions,
  clearMessages
} = useAgentChat();

// 发送消息
await sendMessage({
  message: "帮我写第三章",
  work_id: "work-123",
  context: { chapter_context: "前文..." }
});

// 清空对话
clearMessages();
```

---

## 🔌 API服务

### agentApi

**可用方法**:

```typescript
// 1. Agent对话
agentApi.chat(request: AgentChatRequest): Promise<AgentChatResponse>

// 2. 创建计划
agentApi.createPlan(request: PlanCreationRequest): Promise<PlanResponse>

// 3. 查询计划
agentApi.getPlan(planId: string): Promise<PlanResponse>

// 4. 获取待批准请求
agentApi.getPendingApprovals(): Promise<ApprovalResponse[]>

// 5. 批准请求
agentApi.approveRequest(requestId: string, action: ApprovalActionRequest): Promise<any>

// 6. 拒绝请求
agentApi.rejectRequest(requestId: string, action: ApprovalActionRequest): Promise<any>

// 7. 获取记忆上下文
agentApi.getMemoryContext(): Promise<any>

// 8. 更新用户偏好
agentApi.updatePreferences(preferences: any): Promise<any>
```

---

## 🎨 样式定制

### TailwindCSS配置

确保你的 `tailwind.config.js` 包含以下配置：

```javascript
module.exports = {
  content: [
    './src/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      keyframes: {
        'fade-in': {
          '0%': { opacity: '0', transform: 'translateY(10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' }
        }
      },
      animation: {
        'fade-in': 'fade-in 0.3s ease-out'
      }
    }
  },
  plugins: [
    require('@tailwindcss/typography'),
  ]
}
```

### 自定义样式

你可以通过以下方式自定义样式：

1. **修改组件className**:
```tsx
<AgentChatPanel className="your-custom-class" />
```

2. **覆盖默认样式**:
```css
/* 自定义消息背景色 */
.message-content {
  background-color: your-color;
}

/* 自定义输入框 */
.chat-input-wrapper textarea {
  border-color: your-color;
}
```

---

## 🧪 测试

### 单元测试示例

```typescript
import { renderHook, act } from '@testing-library/react-hooks';
import { useAgentChat } from '@/hooks/useAgentChat';

test('should send message successfully', async () => {
  const { result } = renderHook(() => useAgentChat());

  await act(async () => {
    await result.current.sendMessage({
      message: 'Test message'
    });
  });

  expect(result.current.messages.length).toBeGreaterThan(0);
});
```

---

## 🐛 常见问题

### Q1: API调用401错误

**原因**: Token过期或未设置

**解决**:
```typescript
// 确保Token已保存
localStorage.setItem('access_token', 'your-token');

// 或在API调用前手动设置
axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
```

### Q2: Markdown不渲染

**原因**: 缺少react-markdown依赖

**解决**:
```bash
npm install react-markdown react-syntax-highlighter
```

### Q3: TypeScript类型错误

**原因**: 类型定义未导入

**解决**:
```typescript
import type {
  AgentChatRequest,
  AgentChatResponse
} from '@/types/agent';
```

### Q4: 样式不生效

**原因**: TailwindCSS配置问题

**解决**: 确保组件路径在 `tailwind.config.js` 的 `content` 中

---

## 📚 API文档

完整API文档请查看: [FRONTEND_GUIDE.md](../backend/app/services/agent/FRONTEND_GUIDE.md)

---

## 🔗 相关资源

- [后端API集成文档](../backend/app/services/agent/INTEGRATION.md)
- [Agent系统架构](../backend/app/services/agent/README.md)
- [快速开始指南](../backend/app/services/agent/QUICKSTART.md)

---

## 📝 更新日志

### v1.0 (2025-10-29)

- ✅ 完成所有核心组件
- ✅ 实现4个核心场景
- ✅ 添加完整类型定义
- ✅ 提供示例页面
- ✅ 编写完整文档

---

## 💬 支持

如有问题，请联系:
- 开发团队: NovelAIde
- 文档维护: 2025-10-29

---

## 📄 许可证

MIT License
