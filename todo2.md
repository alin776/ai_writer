# AI Writer 项目开发任务清单 v2.1

> 基于当前项目实际情况生成的开发任务清单
>
> **项目现状**: React + Vite + TypeScript 前端（已完成基础架构 + Novel 编辑器集成）
> **技术栈**: React 19.1.1, TypeScript, Tailwind CSS 4.1.8, Zustand, Recharts, Tiptap 3.7.0
> **当前进度**: 前端UI框架完成，编辑器集成完成，后端未开始
>
> **⚠️ 重要说明**: 本项目采用 React + Vite 架构，使用自定义组件库，不迁移到 Next.js 或 Shadcn/ui

---

## 📐 代码规范

### 1. TypeScript 规范

#### 类型定义
```typescript
// ✅ 推荐：使用 interface 定义对象类型
interface User {
  id: string;
  name: string;
  email: string;
  createdAt: Date;
}

// ✅ 推荐：使用 type 定义联合类型和工具类型
type Status = 'pending' | 'active' | 'inactive';
type Optional<T> = T | null | undefined;

// ❌ 避免：使用 any
const data: any = fetchData(); // 不推荐

// ✅ 推荐：使用明确的类型或 unknown
const data: unknown = fetchData();
if (isUser(data)) {
  console.log(data.name);
}
```

#### 组件 Props
```typescript
// ✅ 推荐：明确定义 Props 接口
interface ButtonProps {
  children: React.ReactNode;
  onClick?: () => void;
  variant?: 'primary' | 'secondary' | 'outline';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
}

const Button: React.FC<ButtonProps> = ({
  children,
  onClick,
  variant = 'primary',
  size = 'md',
  disabled = false
}) => {
  // ...
};
```

#### 泛型使用
```typescript
// ✅ 推荐：使用泛型提高复用性
interface ApiResponse<T> {
  data: T;
  message: string;
  code: number;
}

async function fetchData<T>(url: string): Promise<ApiResponse<T>> {
  const response = await fetch(url);
  return response.json();
}

// 使用
const userData = await fetchData<User>('/api/users/1');
```

---

### 2. React 组件规范

#### 组件文件结构
```typescript
/**
 * 组件功能描述
 */
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
// 外部依赖

import Button from '@/components/Button';
import { DataService } from '@/services/DataService';
// 内部依赖

import styles from './ComponentName.module.css';
// 样式

// ============= 类型定义 =============
interface ComponentProps {
  // ...
}

interface ComponentState {
  // ...
}

// ============= 常量定义 =============
const DEFAULT_CONFIG = {
  // ...
};

// ============= 组件主体 =============
const ComponentName: React.FC<ComponentProps> = ({ prop1, prop2 }) => {
  // 1. Hooks
  const [state, setState] = useState<ComponentState>({});
  const navigate = useNavigate();

  // 2. 副作用
  useEffect(() => {
    // ...
  }, []);

  // 3. 事件处理
  const handleClick = () => {
    // ...
  };

  // 4. 渲染函数
  const renderContent = () => {
    // ...
  };

  // 5. 主渲染
  return (
    <div className={styles.container}>
      {/* ... */}
    </div>
  );
};

export default ComponentName;
```

#### 组件命名
```typescript
// ✅ 推荐：PascalCase 命名组件
const UserProfile: React.FC = () => { /* ... */ };
const WorkListItem: React.FC = () => { /* ... */ };

// ✅ 推荐：描述性命名
const EditorToolbar: React.FC = () => { /* ... */ };
const ChapterList: React.FC = () => { /* ... */ };

// ❌ 避免：过于简短或模糊
const UP: React.FC = () => { /* ... */ }; // 不推荐
const Component1: React.FC = () => { /* ... */ }; // 不推荐
```

#### Hooks 使用顺序
```typescript
const Component: React.FC = () => {
  // 1. State hooks
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<Data[]>([]);

  // 2. Context hooks
  const { user } = useAuth();
  const theme = useTheme();

  // 3. Router hooks
  const navigate = useNavigate();
  const { id } = useParams();

  // 4. Ref hooks
  const inputRef = useRef<HTMLInputElement>(null);

  // 5. Custom hooks
  const { works, fetchWorks } = useWorks();

  // 6. Effect hooks（最后）
  useEffect(() => {
    // ...
  }, []);

  // ...
};
```

---

### 3. 编辑器开发规范

#### Tiptap 扩展结构
```typescript
import { Extension } from '@tiptap/core';
import { Plugin, PluginKey } from '@tiptap/pm/state';

// ✅ 推荐：清晰的扩展结构
export const CustomExtension = Extension.create({
  name: 'customExtension',

  addOptions() {
    return {
      option1: 'default',
      option2: 100,
    };
  },

  addStorage() {
    return {
      data: null,
    };
  },

  addCommands() {
    return {
      customCommand: (attrs) => ({ commands }) => {
        return commands.insertContent({ type: 'custom', attrs });
      },
    };
  },

  addKeyboardShortcuts() {
    return {
      'Mod-Shift-x': () => this.editor.commands.customCommand(),
    };
  },

  addProseMirrorPlugins() {
    return [
      new Plugin({
        key: new PluginKey('customExtension'),
        // ...
      }),
    ];
  },
});
```

#### 编辑器组件规范
```typescript
// ✅ 推荐：编辑器组件统一接口
interface EditorComponentProps {
  content?: string;
  onSave?: (content: string, json: any) => void;
  placeholder?: string;
  autoSave?: boolean;
  autoSaveInterval?: number;
  readOnly?: boolean;
}

// ✅ 推荐：使用 useEditor hook 初始化
const editor = useEditor({
  extensions: [
    // 按功能分组
    // 基础功能
    StarterKit.configure({
      history: { depth: 100 },
      heading: { levels: [1, 2, 3, 4, 5, 6] },
    }),

    // 文本样式
    Underline,
    TextStyle,
    Color,

    // 交互功能
    SlashCommand,
    BubbleMenuExtension,
    GlobalDragHandle,
  ],
  content: content || '<p></p>',
  editorProps: {
    attributes: {
      class: 'prose prose-lg max-w-none focus:outline-none',
    },
  },
  onUpdate: ({ editor }) => {
    // 自动保存逻辑
  },
});
```

#### 样式规范
```css
/* ✅ 推荐：使用语义化类名 */
.slash-commands-menu { /* 功能名-元素名 */ }
.slash-command-item { }
.slash-command-icon { }
.slash-command-title { }

/* ✅ 推荐：使用 BEM 命名法 */
.bubble-menu-container { /* 块 */ }
.bubble-menu-container__button { /* 元素 */ }
.bubble-menu-container__button--active { /* 修饰符 */ }

/* ✅ 推荐：统一动画时长 */
.transition-fast { transition: all 0.15s; }
.transition-normal { transition: all 0.3s; }
.transition-slow { transition: all 0.5s; }

/* ✅ 推荐：使用 CSS 变量 */
:root {
  --editor-font-size: 16px;
  --editor-line-height: 1.8;
  --editor-padding: 2rem;
}
```

---

### 4. 文件和目录规范

#### 目录结构
```
src/
├── components/          # 通用组件
│   ├── Button/
│   │   ├── index.tsx
│   │   ├── Button.module.css
│   │   └── Button.test.tsx
│   ├── editor/         # 编辑器组件
│   │   ├── NovelEditor.tsx
│   │   ├── EditorToolbar.tsx
│   │   ├── BubbleMenu.tsx
│   │   ├── SlashCommands.tsx
│   │   ├── SlashCommandExtension.tsx
│   │   ├── editor-styles.css
│   │   └── interactive-styles.css
│   └── ...
├── views/              # 页面视图
│   ├── EditorView/
│   │   ├── index.tsx
│   │   └── EditorView.module.css
│   └── ...
├── hooks/              # 自定义 Hooks
│   ├── useAuth.ts
│   ├── useWorks.ts
│   └── useEditor.ts
├── services/           # API 服务
│   ├── DataService.ts
│   ├── AuthService.ts
│   └── AIService.ts
├── stores/             # Zustand 状态管理
│   ├── authStore.ts
│   ├── editorStore.ts
│   └── workStore.ts
├── types/              # 全局类型定义
│   ├── user.ts
│   ├── work.ts
│   └── editor.ts
├── utils/              # 工具函数
│   ├── format.ts
│   ├── validation.ts
│   └── storage.ts
└── styles/             # 全局样式
    ├── globals.css
    └── variables.css
```

#### 文件命名
```
✅ 推荐：
- components/Button/index.tsx
- components/editor/NovelEditor.tsx
- views/EditorView/index.tsx
- hooks/useAuth.ts
- utils/formatDate.ts

❌ 避免：
- components/button.tsx
- components/Btn.tsx
- views/editor-view.tsx
- hooks/Auth.ts
```

---

### 5. Git 提交规范

#### Commit Message 格式
```bash
<type>(<scope>): <subject>

<body>

<footer>
```

#### Type 类型
```
feat:     新功能
fix:      Bug 修复
docs:     文档更新
style:    代码格式（不影响代码运行）
refactor: 重构
perf:     性能优化
test:     测试相关
chore:    构建过程或辅助工具变动
```

#### 示例
```bash
# ✅ 推荐
feat(editor): 添加 Slash 命令菜单功能

- 实现 11 个常用命令
- 支持中文/拼音/英文搜索
- 添加键盘导航支持

Closes #123

# ✅ 推荐
fix(editor): 修复 BubbleMenu 导入错误

将 @tiptap/extension-bubble-menu/react 改为 @tiptap/react/menus

# ❌ 避免
update editor
fix bug
改了点东西
```

---

### 6. API 接口规范

#### 请求格式
```typescript
// ✅ 推荐：统一的请求封装
class ApiClient {
  private baseURL: string;
  private token: string | null;

  async request<T>(
    method: string,
    endpoint: string,
    data?: any
  ): Promise<ApiResponse<T>> {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    const response = await fetch(`${this.baseURL}${endpoint}`, {
      method,
      headers,
      body: data ? JSON.stringify(data) : undefined,
    });

    if (!response.ok) {
      throw new ApiError(response.status, await response.text());
    }

    return response.json();
  }

  get<T>(endpoint: string) {
    return this.request<T>('GET', endpoint);
  }

  post<T>(endpoint: string, data: any) {
    return this.request<T>('POST', endpoint, data);
  }

  // ...
}
```

#### 响应格式
```typescript
// ✅ 推荐：统一的响应格式
interface ApiResponse<T> {
  code: number;
  message: string;
  data: T;
  timestamp: number;
}

// 成功响应
{
  "code": 200,
  "message": "Success",
  "data": { /* ... */ },
  "timestamp": 1697123456789
}

// 错误响应
{
  "code": 400,
  "message": "Invalid input",
  "data": null,
  "timestamp": 1697123456789
}
```

---

### 7. 错误处理规范

#### 前端错误处理
```typescript
// ✅ 推荐：使用 try-catch 包裹异步操作
const fetchWorks = async () => {
  setLoading(true);
  setError(null);

  try {
    const data = await DataService.getWorks();
    setWorks(data);
  } catch (error) {
    if (error instanceof ApiError) {
      setError(error.message);
    } else {
      setError('发生未知错误，请稍后重试');
    }
    console.error('Failed to fetch works:', error);
  } finally {
    setLoading(false);
  }
};

// ✅ 推荐：自定义错误类
class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
    public data?: any
  ) {
    super(message);
    this.name = 'ApiError';
  }
}
```

#### 用户友好的错误提示
```typescript
// ✅ 推荐：根据错误类型显示不同提示
const getErrorMessage = (error: any): string => {
  if (error instanceof ApiError) {
    switch (error.status) {
      case 401:
        return '请先登录';
      case 403:
        return '没有权限访问';
      case 404:
        return '请求的资源不存在';
      case 500:
        return '服务器错误，请稍后重试';
      default:
        return error.message || '操作失败';
    }
  }

  if (error instanceof NetworkError) {
    return '网络连接失败，请检查网络';
  }

  return '发生未知错误，请稍后重试';
};
```

---

### 8. 性能优化规范

#### React 优化
```typescript
// ✅ 推荐：使用 memo 避免不必要的重渲染
const WorkListItem = React.memo<WorkListItemProps>(({ work, onEdit }) => {
  return <div>{work.title}</div>;
});

// ✅ 推荐：使用 useCallback 缓存回调函数
const handleEdit = useCallback((id: string) => {
  navigate(`/editor/${id}`);
}, [navigate]);

// ✅ 推荐：使用 useMemo 缓存计算结果
const filteredWorks = useMemo(() => {
  return works.filter(work =>
    work.title.toLowerCase().includes(searchQuery.toLowerCase())
  );
}, [works, searchQuery]);

// ✅ 推荐：大列表使用虚拟滚动
import { FixedSizeList } from 'react-window';

const VirtualList: React.FC = ({ items }) => (
  <FixedSizeList
    height={600}
    itemCount={items.length}
    itemSize={80}
    width="100%"
  >
    {({ index, style }) => (
      <div style={style}>{items[index]}</div>
    )}
  </FixedSizeList>
);
```

#### 资源加载优化
```typescript
// ✅ 推荐：路由懒加载
const EditorView = lazy(() => import('@/views/EditorView'));
const WorksView = lazy(() => import('@/views/WorksView'));

// ✅ 推荐：图片懒加载
<img
  src={work.cover}
  loading="lazy"
  alt={work.title}
/>

// ✅ 推荐：预加载关键资源
<link rel="preload" href="/fonts/main.woff2" as="font" type="font/woff2" crossorigin />
```

---

### 9. 测试规范

#### 单元测试
```typescript
// ✅ 推荐：测试文件命名
// Button.test.tsx
// utils.test.ts
// DataService.test.ts

// ✅ 推荐：使用 describe 和 it 组织测试
import { render, screen, fireEvent } from '@testing-library/react';
import Button from './Button';

describe('Button', () => {
  it('should render children correctly', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('should call onClick when clicked', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click me</Button>);
    fireEvent.click(screen.getByText('Click me'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('should be disabled when disabled prop is true', () => {
    render(<Button disabled>Click me</Button>);
    expect(screen.getByText('Click me')).toBeDisabled();
  });
});
```

---

### 10. 文档注释规范

#### 函数注释
```typescript
/**
 * 获取用户作品列表
 *
 * @param userId - 用户ID
 * @param params - 查询参数
 * @param params.page - 页码（从1开始）
 * @param params.pageSize - 每页数量
 * @param params.status - 作品状态筛选
 * @returns 作品列表和分页信息
 *
 * @example
 * ```typescript
 * const { works, total } = await getWorks('user-123', {
 *   page: 1,
 *   pageSize: 20,
 *   status: 'published'
 * });
 * ```
 */
async function getWorks(
  userId: string,
  params: WorksQueryParams
): Promise<WorksResponse> {
  // ...
}
```

#### 组件注释
```typescript
/**
 * Novel 编辑器组件
 *
 * 基于 Tiptap 的富文本编辑器，支持：
 * - Slash 命令菜单
 * - 气泡菜单（选中文本工具栏）
 * - 拖拽手柄
 * - 代码语法高亮
 * - Markdown 支持
 * - 自动保存
 *
 * @example
 * ```tsx
 * <NovelEditor
 *   content={initialContent}
 *   onSave={(html, json) => {
 *     console.log('Saved:', html);
 *   }}
 *   placeholder="开始写作..."
 *   autoSave={true}
 *   autoSaveInterval={3000}
 * />
 * ```
 */
const NovelEditor: React.FC<NovelEditorProps> = ({ /* ... */ }) => {
  // ...
};
```

---

## 📋 任务优先级分类

### 🔴 P0 - 阻塞性任务（必须立即完成）

#### 1. 编辑器集成 ✅ **已完成 (100%)**
**状态**: ✅ 已完成
**完成时间**: 2025-10-15

**已完成功能**:
- ✅ Tiptap 依赖安装（3.7.0）
- ✅ Novel 编辑器组件创建 (`NovelEditor.tsx`)
- ✅ 基础富文本功能（粗体、斜体、标题、列表等）
- ✅ 工具栏组件 (`EditorToolbar.tsx`)
- ✅ 字数统计实时显示
- ✅ 占位符提示
- ✅ 自动保存（localStorage + 回调）
- ✅ 保存状态提示（已保存/保存中/未保存）
- ✅ Slash 命令菜单（11 个命令 + 搜索）
- ✅ 气泡菜单（9 个格式化工具）
- ✅ 拖拽手柄（段落拖拽）
- ✅ 代码块语法高亮（37 种语言）
- ✅ Markdown 支持（粘贴转换）
- ✅ 集成到 EditorView 页面

**完成度**: 85% (相比 Novel 原版)

**核心文件**:
- `src/components/editor/NovelEditor.tsx` - 主编辑器
- `src/components/editor/EditorToolbar.tsx` - 工具栏
- `src/components/editor/BubbleMenu.tsx` - 气泡菜单
- `src/components/editor/SlashCommands.tsx` - 命令列表
- `src/components/editor/SlashCommandExtension.tsx` - Slash 扩展
- `src/components/editor/editor-styles.css` - 编辑器样式
- `src/components/editor/interactive-styles.css` - 交互样式

**缺失功能**（非阻塞）:
- ⚠️ 图片上传（拖拽 + 粘贴）
- ⚠️ YouTube/Twitter 嵌入
- ⚠️ AI 功能（续写、补全）
- ⚠️ 数学公式支持

---

#### 2. 后端基础架构搭建 (预计1周)
**状态**: ❌ 未开始
**阻塞原因**: 前端已有大量 DataService 调用，但后端完全缺失

**子任务**:
- [ ] 创建 FastAPI 项目结构
- [ ] 配置数据库 (PostgreSQL + SQLAlchemy)
- [ ] 配置 Redis 缓存
- [ ] 实现用户认证系统 (JWT)
- [ ] 实现基础 CRUD API
  - [ ] `/api/auth/*` - 登录/注册/登出
  - [ ] `/api/users/*` - 用户管理
  - [ ] `/api/works/*` - 作品管理
  - [ ] `/api/chapters/*` - 章节管理
- [ ] 配置 CORS 允许前端访问
- [ ] Docker Compose 本地开发环境

**目录结构**:
```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── auth.py
│   │       ├── users.py
│   │       ├── works.py
│   │       └── chapters.py
│   ├── models/
│   │   ├── user.py
│   │   ├── work.py
│   │   └── chapter.py
│   ├── services/
│   ├── schemas/
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── database.py
│   └── main.py
├── alembic/
├── tests/
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

---

#### 3. AI 服务集成 (预计3-5天)
**状态**: ✅ **已完成 (100%)** - 前端部分
**完成时间**: 2025-10-15

**已完成功能**:
- ✅ 前端: 创建 AI 配置管理 (`src/config/ai.config.ts`)
- ✅ 前端: 创建 AI 服务类 (`src/services/AIService.ts`)
- ✅ 前端: 创建 AI Hook (`src/hooks/useAI.ts`)
- ✅ 前端: 实现流式响应处理
- ✅ 前端: 创建 AI 菜单组件 (`src/components/editor/AIMenu.tsx`)
- ✅ 前端: 创建 AI 高亮扩展 (`src/components/editor/AIHighlightExtension.ts`)
- ✅ 前端: 创建 Toast 通知系统 (`src/components/ui/Toast.tsx` + `src/hooks/useToast.ts`)
- ✅ 前端: 集成到 NovelEditor
- ✅ 前端: Slash 命令触发 AI 功能

**核心文件**:
- `src/config/ai.config.ts` - AI 配置管理
- `src/services/AIService.ts` - AI API 调用（支持流式响应）
- `src/hooks/useAI.ts` - AI Hook 封装
- `src/components/editor/AIMenu.tsx` - AI 操作菜单
- `src/components/editor/AIHighlightExtension.ts` - AI 内容高亮标记
- `src/components/ui/Toast.tsx` - Toast 通知组件
- `src/components/editor/interactive-styles.css` - AI 样式

**实现的 AI 功能**:
1. **AI 续写** - 流式实时输出，支持选中文本或上下文续写
2. **AI 扩写** - 扩展选中文本，增加细节
3. **AI 总结** - 总结选中文本，保留关键信息
4. **AI 润色** - 优化选中文本，提升流畅度
5. **AI 翻译** - 智能识别语言并翻译（中英互译）

**技术亮点**:
- ✅ 流式响应实时显示（SSE）
- ✅ AI 生成内容黄色高亮标记（带脉冲动画）
- ✅ 同意/撤销操作（Accept/Reject）
- ✅ 过滤 `<think>` 标签和 reasoning 内容
- ✅ 完善的错误处理和调试日志
- ✅ 防止标记传染（撤销后清除标记）
- ✅ 支持多种 AI 模型配置

**环境变量配置**:
```bash
# 前端 .env
VITE_OPENAI_API_KEY=sk-xxx
VITE_OPENAI_MODEL=gpt-5
VITE_API_URL=https://204992.xyz
```

**待完成（后端部分）**:
- [ ] 后端: 创建 OpenAI 服务类 (`app/services/ai/openai_service.py`)
- [ ] 后端: 实现流式 AI 续写接口 (`/api/v1/ai/complete`)
- [ ] 后端: 实现 AI 对话接口 (`/api/v1/ai/chat`)
- [ ] 后端: Token 计数和成本追踪

---

### 🟡 P1 - 高优先级任务（核心功能）

#### 4. 作品和章节管理完善 (预计1周)
**状态**: ⚠️ 部分完成（仅前端UI）

**已完成**:
- ✅ WorksView - 作品列表页面
- ✅ WorkDetailView - 作品详情页面
- ✅ EditorView - 编辑器页面

**待完成**:
- [ ] 连接后端 API 替换 Mock 数据
- [ ] 实现作品 CRUD 完整流程
  - [ ] 创建作品（含封面上传）
  - [ ] 编辑作品信息
  - [ ] 删除作品（含确认弹窗）
  - [ ] 作品归档/发布状态切换
- [ ] 实现章节 CRUD 完整流程
  - [ ] 创建章节
  - [ ] 重命名章节
  - [ ] 删除章节
  - [ ] 章节排序（拖拽）
- [ ] 实现卷（Volume）功能
  - [ ] 创建卷
  - [ ] 章节归类到卷
- [ ] 作品统计数据实时更新
  - [ ] 总字数
  - [ ] 章节数
  - [ ] 最后更新时间

---

#### 5. 用户系统完善 (预计5天)
**状态**: ⚠️ 部分完成（仅前端UI）

**已完成**:
- ✅ LoginView - 登录页面
- ✅ RegisterView - 注册页面
- ✅ SettingsView - 设置页面
- ✅ Zustand authStore 状态管理

**待完成**:
- [ ] 连接后端认证 API
  - [ ] 登录接口
  - [ ] 注册接口
  - [ ] 登出接口
  - [ ] Token 刷新机制
- [ ] JWT Token 管理
  - [ ] 存储到 localStorage
  - [ ] 自动附加到请求头
  - [ ] Token 过期处理
  - [ ] 自动刷新 Token
- [ ] 用户资料管理
  - [ ] 修改用户名
  - [ ] 修改邮箱
  - [ ] 上传头像
  - [ ] 修改简介
- [ ] 密码管理
  - [ ] 修改密码
  - [ ] 忘记密码（邮件重置）

---

#### 6. 管理后台数据对接 (预计3天)
**状态**: ⚠️ 部分完成（仅前端UI + Mock数据）

**已完成**:
- ✅ AdminDashboardView - 数据面板 (Mock 数据)
- ✅ AdminUsersView - 用户管理 (Mock 数据)
- ✅ AdminAIModelsView - AI 模型管理 (Mock 数据)
- ✅ AdminCostView - 成本监控 (Mock 数据)

**待完成**:
- [ ] 连接后端管理 API
  - [ ] `/api/admin/dashboard` - 仪表盘数据
  - [ ] `/api/admin/users` - 用户管理
  - [ ] `/api/admin/ai-models` - AI 模型配置
  - [ ] `/api/admin/cost` - 成本统计
- [ ] 实现管理员权限验证
- [ ] 实现用户管理功能
  - [ ] 用户列表分页
  - [ ] 用户封禁/解封
  - [ ] 用户角色修改
  - [ ] 用户搜索和筛选
- [ ] 实现 AI 模型配置管理
  - [ ] 模型启用/禁用
  - [ ] 模型参数配置
  - [ ] 费率设置

---

### 🟢 P2 - 中优先级任务（增强功能）

#### 7. 世界观构建系统 (预计2周)
**状态**: ⚠️ 部分完成（内联编辑版本）

**已完成**:
- ✅ 创建 WorldManager 组件（集成在作品详情页）
- ✅ 设定条目管理（内联编辑模式）
  - ✅ 角色设定 (Characters) - 支持添加/编辑/删除
  - ✅ 地点设定 (Locations) - 支持添加/编辑/删除
  - ✅ 基础设定 (Settings) - 支持添加/编辑/删除
- ✅ 内联编辑交互
  - ✅ 直接在列表中编辑
  - ✅ 临时 ID 模式（temp-前缀）
  - ✅ 保存/取消操作

**待完成**:
- [ ] 扩展功能（如果需要独立页面）
  - [ ] 独立世界观管理页面 (`/worldbuilding/:workId`)
  - [ ] 势力设定 (Factions)
  - [ ] 物品设定 (Items)
  - [ ] 设定关系网络 (Relations)
- [ ] AI 辅助生成设定
  - [ ] 根据作品描述生成角色
  - [ ] 根据情节生成地点
  - [ ] 自动提取设定信息
- [ ] 可视化展示
  - [ ] 使用 ReactFlow 展示关系图
  - [ ] 设定卡片视图
  - [ ] 时间线视图
- [ ] 在编辑器中引用设定
  - [ ] @character 标记
  - [ ] @location 标记
  - [ ] 悬浮卡片显示详情

---

#### 8. 大纲生成功能 (预计1周)
**状态**: ❌ 未开始

**功能需求**:
- [ ] 创建大纲页面 (`/outline/:workId`)
- [ ] AI 生成大纲
  - [ ] 根据作品简介生成整体大纲
  - [ ] 根据章节标题生成详细大纲
  - [ ] 支持多种大纲模板（三幕剧、起承转合等）
- [ ] 大纲编辑
  - [ ] 树形结构编辑
  - [ ] 拖拽排序
  - [ ] 折叠/展开
- [ ] 大纲与章节关联
  - [ ] 大纲节点转为章节
  - [ ] 章节反向关联大纲
- [ ] 大纲导出
  - [ ] Markdown 格式
  - [ ] 思维导图格式

---

#### 9. 提示词管理系统 (预计5天)
**状态**: ❌ 未开始

**功能需求**:
- [ ] 创建提示词管理页面 (`/prompts`)
- [ ] 提示词分类
  - [ ] 系统预设提示词（续写、润色、扩写、缩写）
  - [ ] 用户自定义提示词
  - [ ] 作品专用提示词
- [ ] 提示词编辑器
  - [ ] 变量支持 ({context}, {style}, {length})
  - [ ] 预览功能
  - [ ] 版本管理
- [ ] 提示词快捷使用
  - [ ] 右键菜单集成
  - [ ] 快捷键绑定
  - [ ] 编辑器 Slash 命令 (`/prompt`)

---

#### 10. 数据统计和可视化完善 (预计3天)
**状态**: ⚠️ 部分完成（仅前端UI）

**已完成**:
- ✅ AdminDashboardView 基础图表（用户增长、AI 调用统计）
- ✅ AdminCostView 成本图表（成本趋势、模型分布）

**待完成**:
- [ ] 个人写作统计页面 (`/stats`)
  - [ ] 每日字数统计（折线图）
  - [ ] 写作热力图（类似 GitHub Contribution）
  - [ ] 创作效率分析
  - [ ] AI 使用统计
- [ ] 作品统计页面
  - [ ] 章节字数分布（柱状图）
  - [ ] 创作时间轴
  - [ ] 角色出场频率
  - [ ] 关键词云图
- [ ] 导出统计报告
  - [ ] PDF 格式
  - [ ] Excel 格式

---

### 🔵 P3 - 低优先级任务（优化和扩展）

#### 11. 编辑器增强功能 (预计1周)
**状态**: ⚠️ 部分完成（基础功能已完成）

**待完成**:
- [ ] 图片功能增强
  - [ ] 图片拖拽上传
  - [ ] 图片粘贴上传
  - [ ] 图片调整大小
  - [ ] 图片压缩
- [ ] 多媒体嵌入
  - [ ] YouTube 视频嵌入
  - [ ] Twitter 推文嵌入
  - [ ] Bilibili 视频嵌入
- [ ] 数学公式支持
  - [ ] KaTeX 集成
  - [ ] 公式编辑器
- [ ] 表格功能
  - [ ] 插入表格
  - [ ] 合并单元格
  - [ ] 表格样式

---

#### 12. 文件导入导出 (预计1周)
**状态**: ❌ 未开始

**导入功能**:
- [ ] 支持导入格式
  - [ ] TXT 文本
  - [ ] Markdown
  - [ ] DOCX (Word)
  - [ ] EPUB
- [ ] 智能章节分割
- [ ] 格式保留和转换

**导出功能**:
- [ ] 支持导出格式
  - [ ] TXT
  - [ ] Markdown
  - [ ] DOCX
  - [ ] EPUB
  - [ ] PDF
- [ ] 导出设置
  - [ ] 选择章节范围
  - [ ] 格式化选项
  - [ ] 封面和版权页
- [ ] 批量导出

---

#### 13. 协作功能 (预计2周)
**状态**: ❌ 未开始

**功能需求**:
- [ ] 作品分享
  - [ ] 生成分享链接
  - [ ] 权限控制（只读/评论/编辑）
  - [ ] 链接过期时间
- [ ] 实时协作编辑
  - [ ] WebSocket 集成
  - [ ] 操作同步（使用 Yjs）
  - [ ] 光标位置显示
  - [ ] 冲突解决
- [ ] 评论系统
  - [ ] 段落级评论
  - [ ] 回复和讨论
  - [ ] @提及用户
  - [ ] 评论解决状态

---

#### 14. 离线编辑支持 (预计3天)
**状态**: ❌ 未开始

**功能需求**:
- [ ] PWA 配置
  - [ ] Service Worker
  - [ ] 离线缓存策略
  - [ ] App Manifest
- [ ] 本地存储
  - [ ] IndexedDB 存储草稿
  - [ ] 自动同步到服务器
  - [ ] 冲突检测
- [ ] 离线提示
  - [ ] 网络状态检测
  - [ ] 离线模式 UI 提示

---

#### 15. 搜索功能 (预计5天)
**状态**: ❌ 未开始（Header 有搜索按钮但无功能）

**功能需求**:
- [ ] 全局搜索
  - [ ] 作品搜索
  - [ ] 章节内容搜索
  - [ ] 世界观设定搜索
- [ ] 高级搜索
  - [ ] 正则表达式支持
  - [ ] 多条件筛选
  - [ ] 搜索历史
- [ ] 搜索结果
  - [ ] 高亮显示
  - [ ] 上下文预览
  - [ ] 快速跳转

---

#### 16. 通知系统 (预计3天)
**状态**: ❌ 未开始（Header 有通知按钮但无功能）

**功能需求**:
- [ ] 通知类型
  - [ ] 系统通知（维护、更新）
  - [ ] 作品通知（评论、分享）
  - [ ] AI 通知（任务完成、配额提醒）
- [ ] 通知中心
  - [ ] 未读/已读状态
  - [ ] 批量操作（全部已读、清空）
  - [ ] 通知分类和筛选
- [ ] 通知设置
  - [ ] 通知偏好设置
  - [ ] 静默时段
  - [ ] 邮件通知开关

---

#### 17. 主题和个性化 (预计2天)
**状态**: ⚠️ 部分完成（SettingsView 有主题设置但未实现）

**已完成**:
- ✅ SettingsView 主题选择器 UI

**待完成**:
- [ ] 暗黑模式实现
  - [ ] Tailwind Dark Mode 配置
  - [ ] 全局主题切换
  - [ ] 主题持久化（localStorage）
- [ ] 编辑器主题
  - [ ] 亮色主题
  - [ ] 暗色主题
  - [ ] 护眼模式
- [ ] 字体和排版设置
  - [ ] 字体大小
  - [ ] 字体家族
  - [ ] 行高
  - [ ] 段落间距

---

#### 18. 移动端适配 (预计1周)
**状态**: ⚠️ 部分完成（使用 Tailwind 响应式但未充分测试）

**待完成**:
- [ ] 响应式布局优化
  - [ ] 侧边栏移动端适配（抽屉式）
  - [ ] 编辑器移动端适配
  - [ ] 表格移动端适配
- [ ] 触摸交互优化
  - [ ] 滑动手势
  - [ ] 长按菜单
  - [ ] 双击缩放
- [ ] 性能优化
  - [ ] 移动端代码分割
  - [ ] 图片懒加载
  - [ ] 虚拟滚动

---

### 🟣 P4 - 长期规划任务

#### 19. 支付和订阅系统 (预计2周)
**状态**: ❌ 未开始

#### 20. 插件系统 (预计3周)
**状态**: ❌ 未开始

#### 21. 性能优化和监控 (预计1周)
**状态**: ❌ 未开始

---

## 📊 开发里程碑规划

### Milestone 1: 核心编辑功能 ⚠️ **进行中 (60%)**
**目标**: 实现基本的写作和编辑功能

**任务**:
- ✅ 前端UI框架 (已完成)
- ✅ 编辑器集成 (已完成 - 85%)
- [ ] 后端基础架构 (P0-2) - 未开始
- [ ] AI 服务集成 (P0-3) - 未开始
- [ ] 作品和章节管理 (P1-4) - 前端完成，待后端
- [ ] 用户系统完善 (P1-5) - 前端完成，待后端

**交付物**:
- ✅ 可用的编辑器（已完成）
- ⚠️ 作品和章节 CRUD（待后端对接）
- ❌ AI 续写基础功能
- ⚠️ 用户登录注册（待后端对接）

---

### Milestone 2: AI 增强功能 (预计2周)
**目标**: 完善 AI 辅助写作能力
**状态**: ❌ 未开始

---

### Milestone 3: 世界观和组织工具 (预计3周)
**目标**: 提供专业的创作辅助工具
**状态**: ❌ 未开始

---

### Milestone 4: 协作和优化 (预计2周)
**目标**: 提升用户体验和性能
**状态**: ❌ 未开始

---

### Milestone 5: 商业化 (预计2周)
**目标**: 实现盈利能力
**状态**: ❌ 未开始

---

## 🚀 快速启动建议

### 当前状态
✅ **前端 UI 框架**: 100% 完成
✅ **编辑器集成**: 85% 完成（Novel 风格 Tiptap 编辑器）
❌ **后端**: 0% - 这是当前最大阻塞点
❌ **AI 服务**: 0% - 核心功能缺失

### 下一步行动（按优先级）

#### 本周必做（P0）
1. **搭建后端基础架构**（3-5天）
   - FastAPI 项目初始化
   - PostgreSQL 数据库配置
   - 用户认证 API
   - 作品/章节 CRUD API

2. **AI 服务集成**（2-3天）
   - OpenAI API 封装
   - 流式续写接口
   - 前端 AI Hook

#### 本月完成（P1）
3. **数据对接**
   - 替换所有 Mock 数据
   - 前后端联调

4. **管理后台对接**
   - 管理员 API
   - 数据统计接口

---

## 📝 更新日志

### v2.2 (2025-10-16)
- ✅ 实现世界观管理内联编辑功能
  - ✅ 修改 WorldManager 组件支持内联添加/编辑
  - ✅ 重构 WorkDetailView 处理函数支持新的内联编辑模式
  - ✅ 统一 onCharacterSave、onLocationSave、onSettingSave 接口
  - ✅ 移除旧的 Add/Edit/View 分离模式
  - ✅ 实现临时 ID (temp-) 模式区分新增和更新
- ✅ 删除内容审核功能
  - ✅ 删除 AdminContentView 组件
  - ✅ 从路由配置中移除内容审核路由
  - ✅ 从侧边栏和 Header 中移除内容审核入口
- ✅ 修复编辑器无限循环 Bug
  - ✅ 修复 handleEditorSave 依赖数组导致的无限更新问题
  - ✅ 使用函数式更新避免不必要的依赖

### v2.1 (2025-10-15)
- ✅ 添加完整代码规范（TypeScript、React、编辑器、Git等）
- ✅ 更新编辑器任务状态为"已完成"
- ✅ 删除差异分析部分（已统一技术栈）
- ✅ 新增编辑器增强功能任务（P3-11）
- ✅ 更新 Milestone 1 进度为 60%
- ✅ 明确下一步行动优先级

### v2.0 (2025-10-15)
- 初始版本，基于当前项目实际情况生成

---

## 📞 联系和反馈

如有任何问题或需要调整优先级，请及时沟通。

**最后更新**: 2025-10-16
**版本**: v2.2
**状态**: 🚧 开发中
