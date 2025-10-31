# 前端开发规范

> 📋 **文档**: 06-frontend-specs.md | **最后更新**: 2025-10-24

[← 返回文档导航](./README.md)

---

## 📋 目录

- [代码规范](#代码规范)
- [组件设计模式](#组件设计模式)
- [状态管理规范](#状态管理规范)
- [路由设计](#路由设计)
- [性能优化](#性能优化)
- [最佳实践](#最佳实践)

---

## 💻 代码规范

### 命名规范

```typescript
// ✅ 组件名使用 PascalCase
const EditorView = () => { }
const NovelEditor = () => { }

// ✅ 变量和函数使用 camelCase
const userName = "Alice"
const handleSubmit = () => { }

// ✅ 常量使用 UPPER_SNAKE_CASE
const API_BASE_URL = "https://api.example.com"
const MAX_RETRY_COUNT = 3

// ✅ 类型定义使用 PascalCase
interface UserProfile { }
type WorkStatus = 'draft' | 'published'
```

### 文件组织

```
src/
├── components/          # 通用组件
│   ├── ui/             # UI基础组件
│   └── editor/         # 编辑器组件
├── views/              # 页面组件
├── services/           # 服务层
├── stores/             # 状态管理
├── hooks/              # 自定义Hooks
├── utils/              # 工具函数
└── types/              # TypeScript类型定义
```

### 代码格式

- **缩进**: 2空格
- **引号**: 单引号 (字符串)
- **分号**: 不使用
- **行宽**: 100字符
- **格式化工具**: Prettier

---

## 🧩 组件设计模式

### 组件职责

```typescript
// ✅ 好的组件设计 - 单一职责
const UserAvatar = ({ user }: { user: User }) => {
  return <img src={user.avatar} alt={user.name} />
}

const UserCard = ({ user }: { user: User }) => {
  return (
    <div>
      <UserAvatar user={user} />
      <UserInfo user={user} />
    </div>
  )
}

// ❌ 不好的设计 - 职责混乱
const UserComponent = ({ user, onEdit, onDelete }: Props) => {
  // 做了太多事情：展示、编辑、删除
}
```

### Props 设计

```typescript
// ✅ 使用 TypeScript 接口定义 Props
interface EditorProps {
  initialContent: string
  onSave: (content: string) => void
  autoSave?: boolean  // 可选属性
  className?: string
}

const Editor = ({
  initialContent,
  onSave,
  autoSave = true,  // 默认值
  className
}: EditorProps) => {
  // ...
}
```

### 状态提升原则

```typescript
// ✅ 状态在需要的最低公共父组件
const WorkList = () => {
  const [selectedWork, setSelectedWork] = useState(null)

  return (
    <>
      <WorkSelector onSelect={setSelectedWork} />
      <WorkDetail work={selectedWork} />
    </>
  )
}
```

---

## 🗂️ 状态管理规范

### 使用 Zustand 管理全局状态

```typescript
// stores/authStore.ts
import { create } from 'zustand'

interface AuthState {
  user: User | null
  token: string | null
  login: (user: User, token: string) => void
  logout: () => void
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  token: null,
  login: (user, token) => set({ user, token }),
  logout: () => set({ user: null, token: null })
}))

// 使用
const { user, login, logout } = useAuthStore()
```

### 组件内状态

```typescript
// ✅ 简单状态使用 useState
const [count, setCount] = useState(0)
const [text, setText] = useState('')

// ✅ 复杂状态使用 useReducer
const [state, dispatch] = useReducer(reducer, initialState)
```

---

## 🛣️ 路由设计

### 路由结构

```typescript
// 主路由
/ - 首页
/auth/login - 登录
/auth/register - 注册

// 应用路由 (需要认证)
/works - 作品列表
/works/:id - 作品详情
/works/:workId/chapters/:chapterId - 章节编辑
/worldview/:workId - 世界观管理
/settings - 用户设置

// 管理后台 (需要管理员权限)
/admin/dashboard - 管理仪表盘
/admin/users - 用户管理
/admin/ai-models - AI模型管理
```

### 路由守卫

```typescript
// AuthLayout - 需要登录
const AuthLayout = ({ children }: { children: React.ReactNode }) => {
  const { user } = useAuthStore()

  if (!user) {
    return <Navigate to="/auth/login" />
  }

  return <>{children}</>
}

// AdminLayout - 需要管理员
const AdminLayout = ({ children }: { children: React.ReactNode }) => {
  const { user } = useAuthStore()

  if (!user?.isAdmin) {
    return <Navigate to="/" />
  }

  return <>{children}</>
}
```

---

## ⚡ 性能优化

### 组件优化

```typescript
// ✅ 使用 React.memo 避免不必要的重渲染
const ExpensiveComponent = React.memo(({ data }: { data: any }) => {
  // 复杂计算或渲染
})

// ✅ 使用 useMemo 缓存计算结果
const sortedList = useMemo(() => {
  return items.sort((a, b) => a.name.localeCompare(b.name))
}, [items])

// ✅ 使用 useCallback 缓存函数
const handleClick = useCallback(() => {
  console.log('clicked')
}, [])
```

### 代码分割

```typescript
// ✅ 懒加载路由组件
const EditorView = lazy(() => import('./views/EditorView'))
const WorksView = lazy(() => import('./views/WorksView'))

// 使用 Suspense
<Suspense fallback={<Loading />}>
  <EditorView />
</Suspense>
```

### 列表渲染优化

```typescript
// ✅ 使用 key
{items.map(item => (
  <Item key={item.id} data={item} />
))}

// ✅ 虚拟滚动 (大列表)
import { FixedSizeList } from 'react-window'

<FixedSizeList
  height={600}
  itemCount={1000}
  itemSize={50}
>
  {Row}
</FixedSizeList>
```

---

## 📝 最佳实践

### 1. TypeScript 使用

```typescript
// ✅ 充分利用类型推断
const [user, setUser] = useState<User | null>(null)
const works: Work[] = []

// ✅ 避免使用 any
// ❌ const data: any = {}
// ✅ const data: unknown = {}
```

### 2. 错误处理

```typescript
// ✅ 使用 try-catch
const saveWork = async () => {
  try {
    await api.saveWork(data)
    toast.success('保存成功')
  } catch (error) {
    console.error('保存失败:', error)
    toast.error('保存失败')
  }
}

// ✅ 错误边界
class ErrorBoundary extends React.Component {
  componentDidCatch(error, errorInfo) {
    console.error('Error:', error, errorInfo)
  }

  render() {
    return this.props.children
  }
}
```

### 3. API 调用

```typescript
// ✅ 统一的 API 服务层
class WorkService {
  static async getWorks(): Promise<Work[]> {
    const response = await fetch('/api/works')
    return response.json()
  }

  static async saveWork(work: Work): Promise<void> {
    await fetch('/api/works', {
      method: 'POST',
      body: JSON.stringify(work)
    })
  }
}

// 使用
const works = await WorkService.getWorks()
```

### 4. 自定义 Hooks

```typescript
// ✅ 封装可复用逻辑
const useDebounce = (value: string, delay: number) => {
  const [debouncedValue, setDebouncedValue] = useState(value)

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay)
    return () => clearTimeout(timer)
  }, [value, delay])

  return debouncedValue
}

// 使用
const debouncedSearch = useDebounce(searchTerm, 500)
```

### 5. 样式管理

```typescript
// ✅ 使用 Tailwind CSS 类名
<div className="flex items-center gap-4 p-4 bg-white rounded-lg">
  <Avatar src={user.avatar} />
  <div className="flex-1">
    <h3 className="text-lg font-semibold">{user.name}</h3>
    <p className="text-gray-500">{user.email}</p>
  </div>
</div>

// ✅ 使用 clsx 组合类名
import clsx from 'clsx'

<button className={clsx(
  'px-4 py-2 rounded',
  isActive && 'bg-blue-500 text-white',
  !isActive && 'bg-gray-200 text-gray-700'
)}>
  {label}
</button>
```

---

## 🔍 代码审查清单

### 提交代码前检查

- [ ] TypeScript 类型定义完整
- [ ] 组件职责单一清晰
- [ ] 没有 console.log 调试代码
- [ ] 错误处理完善
- [ ] 代码格式化 (Prettier)
- [ ] 没有未使用的导入
- [ ] 性能优化已考虑
- [ ] 可访问性符合标准

---

## 🔗 相关链接

- **上一章**: [开发任务清单](./05-tasks.md)
- **下一章**: [API参考文档](./07-api-reference.md)
- **返回**: [文档导航](./README.md)
- **主文档**: [NovelAIde 项目文档 v2.12.md](../NovelAIde%20项目文档%20v2.12.md)

---

**最后更新**: 2025-10-24
**维护者**: NovelAIde 团队
