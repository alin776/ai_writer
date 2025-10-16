# AI辅助小说创作平台 - 项目规划文档

## 项目概述
构建一个功能完整、架构优美的AI辅助小说平台前端原型。使用React + TypeScript实现，所有数据交互使用Mock Data，但预留极度便利的API替换接口。

## 技术栈选型

### 核心技术
- **框架**: React 18+
- **语言**: TypeScript (强制类型校验)
- **状态管理**: Zustand (轻量级)
- **样式**: Tailwind CSS (原子化CSS)
- **路由**: React Router DOM v6+
- **包管理器**: npm

### 功能库
- **富文本编辑器**: Lexical (Meta开发，现代化、可扩展)
- **图表库**: Recharts (React原生，轻量)
- **HTTP客户端**: Axios (预留，用于未来真实API)
- **日期处理**: date-fns
- **图标库**: Lucide React

## 项目架构

```
ai-writer/
├── src/
│   ├── components/          # 展示组件（纯UI）
│   │   ├── common/          # 通用组件
│   │   ├── editor/          # 编辑器相关组件
│   │   ├── works/           # 作品相关组件
│   │   └── admin/           # 后台管理组件
│   ├── containers/          # 容器组件（连接数据）
│   ├── views/               # 页面视图
│   │   ├── LoginView/
│   │   ├── RegisterView/
│   │   ├── WorksView/
│   │   ├── WorkDetailView/
│   │   ├── EditorView/
│   │   ├── AdminSettingsView/
│   │   └── AdminUsersView/
│   ├── services/            # 数据服务层 (核心抽象层)
│   │   ├── DataService.ts   # 统一数据服务接口
│   │   ├── MockAdapter.ts   # Mock数据适配器
│   │   └── ApiAdapter.ts    # 真实API适配器（预留）
│   ├── store/               # Zustand状态管理
│   │   ├── authStore.ts     # 认证状态
│   │   ├── editorStore.ts   # 编辑器状态
│   │   └── globalStore.ts   # 全局状态
│   ├── types/               # TypeScript类型定义
│   │   └── index.ts         # 所有接口定义
│   ├── mock/                # Mock数据
│   │   ├── data/            # 静态JSON数据
│   │   └── index.ts         # Mock数据导出
│   ├── utils/               # 工具函数
│   ├── hooks/               # 自定义Hooks
│   ├── router/              # 路由配置
│   ├── App.tsx              # 应用入口
│   └── main.tsx             # 渲染入口
├── public/
├── package.json
├── tsconfig.json
├── tailwind.config.js
├── vite.config.ts
├── project.md               # 本文档
└── rules.md                 # 开发规则文档
```

## 核心功能模块

### 1. 写作编辑器视图 (`/editor/:workId/:chapterId`)
- **主编辑区**: 基于Lexical的富文本编辑器
- **AI辅助侧边栏**: AI续写、润色、摘要/分析
- **世界观/设定区**: 关联角色、地点、道具
- **顶部工具栏**: 保存、撤销/重做、章节设置

### 2. 作品管理列表视图 (`/works`)
- **作品列表**: 卡片展示，支持排序、搜索
- **新建作品**: Modal表单

### 3. 作品详情/章节管理视图 (`/works/:workId`)
- **作品信息**: 摘要、模型、成本统计
- **章节树**: 支持拖拽排序、CRUD
- **世界观管理**: 人物、地点、设定管理

### 4. 后台管理/模型配置视图 (`/admin/settings`)
- **模型/API管理**: AI模型配置表格
- **成本/调用监控**: 数据可视化仪表盘（Recharts）

### 5. 用户/权限管理视图 (`/admin/users`)
- **用户列表**: 用户信息表格，支持搜索、分页
- **权限配置**: 角色权限设置

### 6. 登录/注册视图 (`/login`, `/register`)
- **表单**: 用户认证表单
- **Mock JWT**: 模拟Token返回

## 数据抽象层设计（核心）

### 关键设计原则
1. **组件不直接访问Mock数据**
2. **所有数据通过DataService统一接口**
3. **适配器模式实现Mock/Real切换**

### 实现示例
```typescript
// DataService.ts
class DataService {
  private adapter: IDataAdapter;

  constructor() {
    // 环境判断，切换适配器
    this.adapter = import.meta.env.MODE === 'production'
      ? new ApiAdapter()
      : new MockAdapter();
  }

  async getWorks(): Promise<Work[]> {
    return this.adapter.get('/works');
  }

  async saveChapter(chapter: Chapter): Promise<Chapter> {
    return this.adapter.post('/chapters', chapter);
  }
}
```

### 未来API替换步骤
1. 实现 `ApiAdapter.ts`，使用Axios调用真实API
2. 修改 `DataService` 构造函数中的适配器选择逻辑
3. 无需修改任何组件代码

## 开发里程碑

### Phase 1: 基础架构 (当前)
- [x] 项目初始化
- [ ] 类型系统定义
- [ ] 数据抽象层搭建
- [ ] Mock数据创建
- [ ] 路由配置

### Phase 2: 核心视图
- [ ] 登录/注册
- [ ] 作品列表
- [ ] 作品详情

### Phase 3: 编辑器
- [ ] 编辑器基础界面
- [ ] AI辅助功能
- [ ] 世界观关联

### Phase 4: 后台管理
- [ ] 模型配置
- [ ] 用户管理
- [ ] 数据可视化

### Phase 5: 优化与测试
- [ ] 性能优化
- [ ] 响应式适配
- [ ] 整体测试

## 交付标准
- ✅ 完整的项目结构
- ✅ 强类型TypeScript代码
- ✅ 清晰的代码注释
- ✅ 所有核心视图实现
- ✅ Mock数据完整
- ✅ 明确的API替换路径
- ✅ 专业的UI/UX设计
- ✅ Loading状态模拟

## 当前进度
**正在进行**: 创建项目规划和规则文档
**下一步**: 初始化React项目结构

---
*最后更新: 2025-10-15*
