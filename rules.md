# AI 写作平台 - 开发规范
重点：除非我提出来，否则不要随意创建文档，要创建的时候要询问我，每次修改完记得修改todo2.md等进度有关文件。
## 一、架构原则

### 1.1 关注点分离 (Separation of Concerns)
项目采用分层架构，严格遵循职责分离：

```
View Layer (视图层)
    ↓ (渲染)
Container Layer (容器层)
    ↓ (数据)
Component Layer (组件层)
    ↓ (逻辑)
Service Layer (服务层)
    ↓ (适配)
Adapter Layer (适配器层: Mock/Real API)
```

**层级职责**:
- **View**: 页面布局和整体结构
- **Container**: 连接数据和组件，处理业务逻辑
- **Component**: 展示型组件，仅通过props接收数据
- **Service**: 数据服务统一接口
- **Adapter**: 数据适配器（Mock或真实API）

### 1.2 数据流向
```
开发阶段: View → Container → Service → Adapter → Mock/API
                                            ↑
生产环境: View → Container → Service → Adapter → Mock/API
```

## 二、代码规范

### 2.0 搜索和工具使用规范

#### 2.0.1 Grep/搜索工具使用原则

**CRITICAL: 必须遵守以下搜索规范，避免工具执行超时或卡死**

1. **优先使用 Grep 工具**
   - 优先使用封装好的 Grep 工具（基于 ripgrep）
   - Grep 工具有内部优化和限制，性能更好
   - 使用 `head_limit` 参数限制结果数量，避免处理过多数据

   ```typescript
   // ✅ 正确示例
   Grep("Chapter|chapter", {
     output_mode: "content",
     head_limit: 100,  // 限制结果数量
     case_insensitive: true
   });
   ```

2. **Execute 工具执行 grep/rg 必须设置 timeout**
   - 如果必须使用 Execute 工具执行 grep/rg 命令
   - **必须明确设置 timeout 参数**，否则可能执行很长时间无法停止
   - 建议设置 120-300 秒的 timeout

   ```typescript
   // ✅ 正确示例
   Execute({
     command: 'rg "Chapter|chapter" --timeout 120',
     timeout: 150  // Execute 工具本身也设置 timeout
   });

   // ❌ 错误示例 - 没有设置 timeout
   Execute({
     command: 'rg "Chapter|chapter"'  // 可能会卡死
   });
   ```

3. **合理使用限制参数**
   - 对于可能返回大量结果的搜索，使用 `head_limit` 限制
   - 使用 `glob_pattern` 或 `type` 参数缩小搜索范围
   - 避免在大型文件或目录上执行无限制搜索

   ```typescript
   // ✅ 正确示例 - 限制搜索范围
   Grep("pattern", {
     path: "D:\\Java\\ai_writer\\src",  // 限定目录
     type: "tsx",  // 限定文件类型
     head_limit: 50  // 限制结果数量
   });
   ```

4. **大文件处理**
   - 对于超过 2400 行的文件，Read 工具会自动截断
   - 使用 `offset` 和 `limit` 参数分段读取
   - 避免一次性读取整个大文件

### 2.1 TypeScript 严格模式
- **强制类型定义**: 所有函数、变量必须显式声明类型
- **禁止使用 `any`**: 使用 `unknown` 或具体类型
- **接口优先**: 使用 `interface` 定义数据结构
- **类型复用**: 所有类型定义统一放在 `src/types/index.ts`

```typescript
// ✅ 正确示例
interface User {
  id: string;
  name: string;
  email: string;
}

async function getUser(id: string): Promise<User> {
  // ...
}

// ❌ 错误示例
function getUser(id): any {
  // ...
}
```

### 2.2 组件规范

#### 展示型组件 (Presentational Components)
- 必须放在 `src/components/` 目录
- 只接受props传入数据
- 使用函数式组件 + Hooks
- 必须使用 TypeScript 定义props类型

```typescript
// src/components/common/Button.tsx
interface ButtonProps {
  label: string;
  onClick: () => void;
  variant?: 'primary' | 'secondary';
  disabled?: boolean;
}

export const Button: React.FC<ButtonProps> = ({
  label,
  onClick,
  variant = 'primary',
  disabled = false
}) => {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`btn btn-${variant}`}
    >
      {label}
    </button>
  );
};
```

#### 容器组件 (Container Components)
- 必须放在 `src/containers/` 目录
- 负责连接Zustand状态
- 调用数据DataService获取数据
- 处理业务逻辑

```typescript
// src/containers/WorkListContainer.tsx
import { useEffect, useState } from 'react';
import { DataService } from '@/services/DataService';
import { WorkList } from '@/components/works/WorkList';
import type { Work } from '@/types';

export const WorkListContainer: React.FC = () => {
  const [works, setWorks] = useState<Work[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchWorks = async () => {
      setLoading(true);
      const data = await DataService.getWorks();
      setWorks(data);
      setLoading(false);
    };
    fetchWorks();
  }, []);

  return <WorkList works={works} loading={loading} />;
};
```

#### 视图组件 (View Components)
- 必须放在 `src/views/` 目录
- 页面级别的最顶层组件
- 组合多个容器组件
- 定义页面布局

```typescript
// src/views/WorksView/index.tsx
import { WorkListContainer } from '@/containers/WorkListContainer';
import { Header } from '@/components/common/Header';

export const WorksView: React.FC = () => {
  return (
    <div className="works-view">
      <Header title="我的作品" />
      <WorkListContainer />
    </div>
  );
};
```

### 2.3 命名规范

#### 文件命名
- **组件文件**: PascalCase，如 `Button.tsx`, `WorkList.tsx`
- **工具函数**: camelCase，如 `formatDate.ts`, `validation.ts`
- **类型定义**: PascalCase，如 `types.ts`, `interfaces.ts`
- **常量**: UPPER_SNAKE_CASE，如 `CONSTANTS.ts`

#### 变量命名
- **组件名**: PascalCase，如 `const Button = () => {}`
- **函数**: camelCase，如 `const getUserName = () => {}`
- **常量**: UPPER_SNAKE_CASE，如 `const MAX_LENGTH = 100`
- **类型/接口**: PascalCase，如 `interface User {}`

#### 目录命名
- **功能目录**: `components`, `views`, `services`
- **业务模块**: 使用描述性名称（PascalCase），如 `components/WorkList/`

### 2.4 注释规范

#### 组件注释
```typescript
/**
 * 作品列表组件
 *
 * @description 用于开发阶段显示所有作品/章节列表
 * @param {Work[]} works - 作品列表数据
 * @param {boolean} loading - 加载状态
 * @param {Function} onWorkClick - 点击作品回调
 */
export const WorkList: React.FC<WorkListProps> = ({ works, loading, onWorkClick }) => {
  // ...
};
```

#### 函数注释
```typescript
/**
 * 格式化相对时间
 *
 * @param {Date | string} date - 输入日期或ISO字符串
 * @returns {string} 格式化后的字符串，如 "2天前"
 *
 * @example
 * formatRelativeTime(new Date()) // "刚刚"
 * formatRelativeTime('2025-10-14') // "1天前"
 */
export function formatRelativeTime(date: Date | string): string {
  // ...
}
```

#### 复杂逻辑注释
```typescript
// 步骤1: 过滤已发布章节
const publishedChapters = chapters.filter(ch => ch.status === 'published');

// 步骤2: 按章节顺序排序
publishedChapters.sort((a, b) => a.order - b.order);

// 步骤3: 计算总字数
const totalWords = publishedChapters.reduce((sum, ch) => sum + ch.wordCount, 0);
```

## 三、数据服务层规范

### 3.1 核心原则

#### DataService 唯一入口
- 所有组件**禁止直接引入Mock数据**
- 必须通过 `DataService` 获取所有数据
- 遵循标准RESTful接口规范

```typescript
// src/services/DataService.ts
import { MockAdapter } from './MockAdapter';
import { ApiAdapter } from './ApiAdapter';
import type { IDataAdapter } from './IDataAdapter';

class DataServiceClass {
  private adapter: IDataAdapter;

  constructor() {
    // 根据环境变量决定使用Mock还是真实API
    this.adapter = import.meta.env.MODE === 'production'
      ? new ApiAdapter()
      : new MockAdapter();
  }

  /**
   * 获取所有作品
   * @returns {Promise<Work[]>} 作品列表
   */
  async getWorks(): Promise<Work[]> {
    return this.adapter.get('/works');
  }

  /**
   * 获取单个作品详情
   * @param {string} id - 作品ID
   * @returns {Promise<Work>} 作品详情
   */
  async getWork(id: string): Promise<Work> {
    return this.adapter.get(`/works/${id}`);
  }

  /**
   * 创建作品
   * @param {Partial<Work>} work - 作品数据
   * @returns {Promise<Work>} 创建的作品
   */
  async createWork(work: Partial<Work>): Promise<Work> {
    return this.adapter.post('/works', work);
  }

  /**
   * 更新作品
   * @param {string} id - 作品ID
   * @param {Partial<Work>} work - 更新的数据
   * @returns {Promise<Work>} 更新后的作品
   */
  async updateWork(id: string, work: Partial<Work>): Promise<Work> {
    return this.adapter.put(`/works/${id}`, work);
  }

  /**
   * 删除作品
   * @param {string} id - 作品ID
   * @returns {Promise<void>}
   */
  async deleteWork(id: string): Promise<void> {
    return this.adapter.delete(`/works/${id}`);
  }

  // ... 其他方法
}

// 导出单例
export const DataService = new DataServiceClass();
```

#### 适配器接口
```typescript
// src/services/IDataAdapter.ts
export interface IDataAdapter {
  get<T>(url: string, params?: any): Promise<T>;
  post<T>(url: string, data?: any): Promise<T>;
  put<T>(url: string, data?: any): Promise<T>;
  delete<T>(url: string): Promise<T>;
}
```

#### Mock适配器实现
```typescript
// src/services/MockAdapter.ts
import { mockWorks, mockChapters, mockUsers } from '@/mock';
import type { IDataAdapter } from './IDataAdapter';

export class MockAdapter implements IDataAdapter {
  /**
   * 模拟网络延迟
   * @param {number} ms - 延迟毫秒数
   */
  private async delay(ms: number = 500): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  async get<T>(url: string, params?: any): Promise<T> {
    await this.delay();

    // 路由匹配逻辑
    if (url === '/works') {
      return mockWorks as T;
    }

    if (url.startsWith('/works/')) {
      const id = url.split('/')[2];
      const work = mockWorks.find(w => w.id === id);
      if (!work) throw new Error('Work not found');
      return work as T;
    }

    // ... 其他路由

    throw new Error(`Mock route not implemented: ${url}`);
  }

  async post<T>(url: string, data?: any): Promise<T> {
    await this.delay();
    // 模拟创建逻辑
    // ...
  }

  async put<T>(url: string, data?: any): Promise<T> {
    await this.delay();
    // 模拟更新逻辑
    // ...
  }

  async delete<T>(url: string): Promise<T> {
    await this.delay();
    // 模拟删除逻辑
    // ...
  }
}
```

#### 真实API适配器（预留）
```typescript
// src/services/ApiAdapter.ts
import axios, { AxiosInstance } from 'axios';
import type { IDataAdapter } from './IDataAdapter';

export class ApiAdapter implements IDataAdapter {
  private axiosInstance: AxiosInstance;

  constructor() {
    this.axiosInstance = axios.create({
      baseURL: import.meta.env.VITE_API_BASE_URL,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json'
      }
    });

    // 请求拦截器：添加Token
    this.axiosInstance.interceptors.request.use(config => {
      const token = localStorage.getItem('token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });

    // 响应拦截器
    this.axiosInstance.interceptors.response.use(
      response => response.data,
      error => {
        // 错误处理
        console.error('API Error:', error);
        return Promise.reject(error);
      }
    );
  }

  async get<T>(url: string, params?: any): Promise<T> {
    return this.axiosInstance.get(url, { params });
  }

  async post<T>(url: string, data?: any): Promise<T> {
    return this.axiosInstance.post(url, data);
  }

  async put<T>(url: string, data?: any): Promise<T> {
    return this.axiosInstance.put(url, data);
  }

  async delete<T>(url: string): Promise<T> {
    return this.axiosInstance.delete(url);
  }
}
```

### 3.2 API切换流程

**从Mock数据切换到真实API的步骤**:

1. **完善ApiAdapter**: 实现 `src/services/ApiAdapter.ts`
2. **配置环境变量**: 在 `.env.production` 中设置 `VITE_API_BASE_URL`
3. **切换DataService**: 适配器选择逻辑会根据环境自动切换
4. **测试验证接口**: 所有组件无需修改

```typescript
// DataService.ts 中的适配器选择逻辑
constructor() {
  this.adapter = import.meta.env.MODE === 'production'
    ? new ApiAdapter()  // 生产环境：真实API
    : new MockAdapter(); // 开发环境：Mock数据
}
```

## 四、状态管理 (Zustand)

### 4.1 使用原则
- **最小化原则**: 开发阶段尽量少用
- **局部优先**: 容器组件内部优先使用 `useState`
- **全局状态**: 仅用于跨组件共享的状态（如用户认证）

### 4.2 Store 定义

#### 认证Store
```typescript
// src/store/authStore.ts
import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { User } from '@/types';

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  login: (user: User, token: string) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      isAuthenticated: false,

      login: (user, token) => {
        localStorage.setItem('token', token);
        set({ user, token, isAuthenticated: true });
      },

      logout: () => {
        localStorage.removeItem('token');
        set({ user: null, token: null, isAuthenticated: false });
      }
    }),
    {
      name: 'auth-storage'
    }
  )
);
```

#### 编辑器Store
```typescript
// src/store/editorStore.ts
import { create } from 'zustand';
import type { Chapter } from '@/types';

interface EditorState {
  currentChapter: Chapter | null;
  isSaving: boolean;
  lastSaveTime: Date | null;
  aiSidebarOpen: boolean;
  setCurrentChapter: (chapter: Chapter) => void;
  setIsSaving: (saving: boolean) => void;
  setLastSaveTime: (time: Date) => void;
  toggleAiSidebar: () => void;
}

export const useEditorStore = create<EditorState>((set) => ({
  currentChapter: null,
  isSaving: false,
  lastSaveTime: null,
  aiSidebarOpen: true,

  setCurrentChapter: (chapter) => set({ currentChapter: chapter }),
  setIsSaving: (saving) => set({ isSaving: saving }),
  setLastSaveTime: (time) => set({ lastSaveTime: time }),
  toggleAiSidebar: () => set((state) => ({ aiSidebarOpen: !state.aiSidebarOpen }))
}));
```

### 4.3 使用方式
```typescript
// 在组件中使用
import { useAuthStore } from '@/store/authStore';

const MyComponent = () => {
  const { user, isAuthenticated, logout } = useAuthStore();

  // 或只订阅需要的状态
  const user = useAuthStore(state => state.user);

  return <div>{user?.name}</div>;
};
```

## 五、样式规范 (Tailwind CSS)

### 5.1 基本原则
- 优先使用 Tailwind 原子类
- 复杂样式使用 `@apply` 提取
- 避免内联样式，统一使用工具类

### 5.2 自定义配置
```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          // ... 其他色阶
          500: '#3b82f6',
          600: '#2563eb',
        },
        secondary: { /* ... */ },
        success: { /* ... */ },
        warning: { /* ... */ },
        error: { /* ... */ },
      }
    }
  }
}
```

### 5.3 常用类复用
```typescript
// src/styles/commonClasses.ts
export const buttonClasses = {
  base: 'px-4 py-2 rounded-lg font-medium transition-colors',
  primary: 'bg-primary-500 text-white hover:bg-primary-600',
  secondary: 'bg-gray-200 text-gray-800 hover:bg-gray-300',
};

export const cardClasses = 'bg-white rounded-xl shadow-sm p-6 border border-gray-100';
```

## 六、路由规范

### 6.1 路由结构
```typescript
// src/router/index.tsx
import { createBrowserRouter } from 'react-router-dom';
import { LoginView } from '@/views/LoginView';
import { WorksView } from '@/views/WorksView';
// ... 其他视图

export const router = createBrowserRouter([
  {
    path: '/login',
    element: <LoginView />
  },
  {
    path: '/register',
    element: <RegisterView />
  },
  {
    path: '/',
    element: <AuthLayout />, // 需要认证的布局
    children: [
      {
        path: 'works',
        element: <WorksView />
      },
      {
        path: 'works/:workId',
        element: <WorkDetailView />
      },
      {
        path: 'editor/:workId/:chapterId',
        element: <EditorView />
      },
      {
        path: 'admin',
        children: [
          {
            path: 'settings',
            element: <AdminSettingsView />
          },
          {
            path: 'users',
            element: <AdminUsersView />
          }
        ]
      }
    ]
  }
]);
```

### 6.2 路由守卫
```typescript
// src/components/layout/AuthLayout.tsx
import { Navigate, Outlet } from 'react-router-dom';
import { useAuthStore } from '@/store/authStore';

export const AuthLayout: React.FC = () => {
  const isAuthenticated = useAuthStore(state => state.isAuthenticated);

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return (
    <div className="app-layout">
      <Sidebar />
      <main className="main-content">
        <Outlet />
      </main>
    </div>
  );
};
```

## 七、错误处理

### 7.1 异步错误
```typescript
// 使用 try-catch
const handleSubmit = async () => {
  try {
    setLoading(true);
    await DataService.createWork(formData);
    // 成功处理
  } catch (error) {
    console.error('Failed to create work:', error);
    // 显示错误提示
    showToast('创建失败，请重试', 'error');
  } finally {
    setLoading(false);
  }
};
```

### 7.2 错误边界
```typescript
// src/components/common/ErrorBoundary.tsx
import React, { Component, ErrorInfo, ReactNode } from 'react';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('ErrorBoundary caught:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="error-fallback">
          <h1>出错了</h1>
          <p>{this.state.error?.message}</p>
        </div>
      );
    }

    return this.props.children;
  }
}
```

## 八、性能优化

### 8.1 组件优化
```typescript
// 使用 React.memo 避免不必要的重渲染
export const WorkCard = React.memo<WorkCardProps>(({ work, onClick }) => {
  return (
    <div onClick={() => onClick(work.id)}>
      {/* ... */}
    </div>
  );
});

// 使用 useMemo 缓存计算结果
const sortedWorks = useMemo(() => {
  return works.sort((a, b) => b.updateTime - a.updateTime);
}, [works]);

// 使用 useCallback 缓存函数
const handleWorkClick = useCallback((id: string) => {
  navigate(`/works/${id}`);
}, [navigate]);
```

### 8.2 懒加载
```typescript
// 路由懒加载
import { lazy, Suspense } from 'react';

const EditorView = lazy(() => import('@/views/EditorView'));

// 使用
<Suspense fallback={<LoadingSpinner />}>
  <EditorView />
</Suspense>
```

## 九、测试规范（预留）

### 9.1 单元测试
- 使用 Vitest + React Testing Library
- 测试覆盖率 > 70%
- 关注业务逻辑核心测试

### 9.2 E2E测试
- 使用 Playwright 或 Cypress
- 测试核心开发流程

## 十、Git 工作流

### 10.1 Commit Message格式
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Type类型**:
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式调整（不影响功能）
- `refactor`: 重构
- `test`: 测试
- `chore`: 构建/工具配置

**示例**:
```
feat(editor): 添加AI续写功能

- 新增AI续写侧边栏
- 集成配置管理
- 更新MockAdapter模拟API调用

Closes #123
```

## 十一、项目目录结构详解

```
ai-writer/
├── src/
│   ├── components/              # 展示型组件
│   │   ├── common/              # 通用组件
│   │   │   ├── Button.tsx
│   │   │   ├── Input.tsx
│   │   │   ├── Modal.tsx
│   │   │   ├── Loading.tsx
│   │   │   └── ErrorBoundary.tsx
│   │   ├── editor/              # 编辑器组件
│   │   │   ├── EditorToolbar.tsx
│   │   │   ├── AiSidebar.tsx
│   │   │   └── WorldPanel.tsx
│   │   ├── works/               # 作品组件
│   │   │   ├── WorkCard.tsx
│   │   │   ├── WorkList.tsx
│   │   │   └── ChapterTree.tsx
│   │   ├── admin/               # 管理组件
│   │   │   ├── ModelTable.tsx
│   │   │   ├── UserTable.tsx
│   │   │   └── CostChart.tsx
│   │   └── layout/              # 布局组件
│   │       ├── Header.tsx
│   │       ├── Sidebar.tsx
│   │       └── AuthLayout.tsx
│   ├── containers/              # 容器组件
│   │   ├── WorkListContainer.tsx
│   │   ├── EditorContainer.tsx
│   │   └── AdminContainer.tsx
│   ├── views/                   # 页面视图
│   │   ├── LoginView/
│   │   │   └── index.tsx
│   │   ├── RegisterView/
│   │   │   └── index.tsx
│   │   ├── WorksView/
│   │   │   └── index.tsx
│   │   ├── WorkDetailView/
│   │   │   └── index.tsx
│   │   ├── EditorView/
│   │   │   └── index.tsx
│   │   ├── AdminSettingsView/
│   │   │   └── index.tsx
│   │   └── AdminUsersView/
│   │       └── index.tsx
│   ├── services/                # 数据服务层
│   │   ├── IDataAdapter.ts      # 适配器接口
│   │   ├── MockAdapter.ts       # Mock适配器
│   │   ├── ApiAdapter.ts        # API适配器（预留）
│   │   └── DataService.ts       # 统一数据服务
│   ├── store/                   # Zustand状态管理
│   │   ├── authStore.ts
│   │   ├── editorStore.ts
│   │   └── globalStore.ts
│   ├── types/                   # TypeScript类型
│   │   └── index.ts
│   ├── mock/                    # Mock数据
│   │   ├── data/
│   │   │   ├── works.ts
│   │   │   ├── chapters.ts
│   │   │   ├── users.ts
│   │   │   ├── models.ts
│   │   │   └── worldData.ts
│   │   └── index.ts
│   ├── utils/                   # 工具函数
│   │   ├── formatDate.ts
│   │   ├── validation.ts
│   │   └── constants.ts
│   ├── hooks/                   # 自定义Hooks
│   │   ├── useDebounce.ts
│   │   ├── useLocalStorage.ts
│   │   └── useAsync.ts
│   ├── router/                  # 路由配置
│   │   └── index.tsx
│   ├── styles/                  # 样式文件
│   │   ├── globals.css
│   │   └── commonClasses.ts
│   ├── App.tsx
│   ├── main.tsx
│   └── vite-env.d.ts
├── public/
├── .env
├── .env.production
├── .gitignore
├── package.json
├── tsconfig.json
├── tailwind.config.js
├── postcss.config.js
├── vite.config.ts
├── project.md                   # 项目规划文档
└── rules.md                     # 本文档
```

## 十二、开发工作流程

### 12.1 标准流程
1. **设计先行**: 定义数据结构
2. **类型定义**: 编写TypeScript类型
3. **创建Mock**: 准备Mock数据
4. **开发组件**: 按照 Component → Container → View 顺序
5. **测试功能**: 测试数据流和交互
6. **代码审查**: 确保符合规范
7. **提交代码**: 遵循提交规范

### 12.2 调试技巧
- 使用React DevTools查看组件树
- 使用Zustand DevTools查看状态
- 使用浏览器Network标签检查Mock数据返回（虽然是本地）
- Console.log + TypeScript类型帮助定位问题

## 十三、检查清单（每次提交前）

在提交代码前，请确认以下所有事项：

- [ ] 所有变量有TypeScript类型定义
- [ ] 所有数据通过DataService获取
- [ ] 所有组件有清晰的职责分离
- [ ] 所有复杂逻辑有注释（容器/服务/路由）
- [ ] Loading状态正确处理
- [ ] 错误处理完善
- [ ] 命名符合规范
- [ ] 无TypeScript编译错误
- [ ] 无Console警告
- [ ] 响应式布局正常（如需要）
- [ ] 项目文档正确更新（npm run build）
- [ ] Mock数据完整且符合真实场景
- [ ] API切换路径清晰可执行

---

**重要提醒**: 本规范文档/项目规划文档 都是提示词的重要组成部分，在整个项目开发过程中持续遵守，确保代码质量和架构一致性。

*最后更新: 2025-10-15*
