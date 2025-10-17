> **整合版本说明**: 本文档整合了原技术栈规划(v1.2)、项目任务清单(v2.0)、前端开发规范(v2.1)，并更新了后端完成状态(v2.3)
>
> **项目现状**: React 19 + Vite + TypeScript 前端 + FastAPI 后端（核心功能已完成）  
**技术栈**: React 19.1.1, TypeScript, Tailwind CSS 4.1.8, Zustand, Tiptap 3.7.0, FastAPI, PostgreSQL  
**当前进度**:
>

+ ✅ 前端UI框架完成（100%）
+ ✅ 编辑器集成完成（Tiptap + Slash命令 + AI菜单，85%）
+ ✅ 后端API完成（用户、作品、章节，85-90%）
+ ✅ **前后端认证对接完成（登录/注册）- 2025-10-16**
+ 🔴 其他模块前后端对接待完成（作品、章节等）
+ 🔴 AI后端服务未实现

**技术方案**: React 19 + Vite + FastAPI + PostgreSQL  
**状态**: 🚧 开发中 - Milestone 1 进度 88-92%，下一步：完成其他模块对接

---

## 📑 文档导航
+ [🎯 项目概述](#-项目概述)
+ [👥 团队简介](#-团队简介)
+ [⚙️ 技术栈规划](#️-技术栈规划)
    - [前端技术栈](#一前端技术栈)
    - [后端技术栈](#二后端技术栈python)
    - [数据库设计](#三数据库设计)
    - [开发工具链](#四开发工具链)
    - [基础设施](#五基础设施)
    - [第三方服务](#六第三方服务)
+ [📊 当前项目状态](#-当前项目状态分析)
+ [📋 开发任务清单](#-任务优先级分类)
+ [🗓️ 开发路线图](#️-开发路线图里程碑规划)
+ [🚀 快速启动](#-快速启动建议)
+ [📚 参考资源](#-参考资源)

---

## 🎯 项目概述
### 项目背景
基于三个开源项目的深度分析（[MaliangAINovalWriter](https://github.com/Deng-m1/MaliangAINovalWriter)、[Novel](https://github.com/steven-tey/novel)、[novelWriter](https://github.com/vkbo/novelWriter)），从零到一开发一款专业的AI辅助写小说工具。

### 项目目标
+ ✅ **提升创作效率**：AI续写、润色、大纲生成，让创作更快速
+ ✅ **构建完整世界观**：角色、地点、势力设定的系统化管理
+ ✅ **管理长篇小说**：清晰的章节、场景、片段管理体系
+ ✅ **降低创作门槛**：智能提示、自动补全，人人都能写小说

### 核心特色
+ 🚀 **现代化编辑器**：基于Novel/Tiptap，提供Notion级别的编辑体验
+ 🤖 **强大AI能力**：集成主流AI模型，支持多种创作辅助功能
+ 🎨 **世界观可视化**：关系图、时间线、设定卡片等可视化工具
+ 💰 **成本可控**：使用第三方OpenAI兼容API，价格友好

---

## 👥 团队简介
### 关于我们
我们是一支专注于**AI内容创作工具**的技术团队，致力于打造一款真正好用的AI辅助写小说工具，帮助小说作者提升创作效率，降低创作门槛。

### 项目使命
让每个热爱写作的人都能轻松创作出精彩的小说故事。

### 核心价值观
+ 🚀 **技术驱动**：采用最新的AI技术和现代化Web架构
+ 💡 **用户为先**：深度理解小说创作者的需求和痛点  
+ ⚡ **快速迭代**：敏捷开发，快速响应用户反馈
+ 🎯 **专业专注**：专注小说创作领域，不做大而全的工具

### 团队构成（当前规划）
```plain
👨‍💻 技术团队（2-3人）
   - 全栈工程师：负责前后端开发
   - 技能栈：React + Vite + Python + AI集成

📊 产品团队（1人）
   - 产品经理：负责需求分析和产品规划
```

### 我们在做什么
**产品名称**：NovelAIde

**核心功能**：

+ ✍️ **智能续写**：AI根据上下文自动续写故事
+ 📝 **大纲生成**：一键生成完整的章节大纲
+ 🎨 **世界观构建**：AI辅助构建角色、地点、势力等设定
+ 🔄 **内容润色**：智能优化文字表达和情节逻辑
+ 📚 **章节管理**：高效管理长篇小说的章节和场景

**技术亮点**：

+ 基于Novel编辑器，提供Notion级别的编辑体验
+ 使用第三方OpenAI兼容API（[https://204992.xyz），成本可控](https://204992.xyz），成本可控)
+ 现代化技术栈：React 19 + Vite + FastAPI + PostgreSQL
+ 完整的CI/CD流程和Docker部署方案

### 当前状态
📍 **阶段**：开发初期 - 前端基础完成，后端待启动  
📅 **预计启动**：2025年10月中旬  
🎯 **MVP目标**：3个月内上线可用版本



## ⚙️ 技术栈规划
### 技术选型说明
**最终确定方案**：React 19 + Vite + FastAPI + PostgreSQL  
**前端状态**：✅ 基础架构已完成  
**后端状态**：⚠️ 进行中  
**优势**：快速迭代、灵活可控、生态成熟

### 一、前端技术栈
#### 核心框架 ✅ 已确定
+ **框架**: React 19.1.1
+ **语言**: TypeScript 5.x
+ **包管理**: npm / pnpm
+ **构建工具**: Vite 5.x

#### 编辑器方案 ⭐
+ **推荐方案**: Novel (基于Tiptap 2.x)
+ **为什么选Novel**:
    - ✅ 开箱即用的Notion风格编辑器
    - ✅ AI功能已集成（续写、补全、Slash命令）
    - ✅ 节省2-3周开发时间
    - ✅ Apache 2.0许可证，可商用
    - ✅ 6.2k+ Stars，持续维护
+ **核心依赖**:
    - `novel` - 完整编辑器组件
    - `ai` - Vercel AI SDK
    - `@ai-sdk/openai` - OpenAI集成
+ **实施方案**: 
    - **方案A**: 直接使用Tiptap（推荐，更灵活）
    - **方案B**: 集成Novel（需要适配Vite）
    - **决策**: 先用Tiptap快速实现，后期评估是否迁移到Novel

#### AI集成 ⭐
+ **AI提供商**: 第三方OpenAI兼容接口
    - **Base URL**: `https://204992.xyz`
    - **API Key**: 环境变量配置 `{:LOCAL_API_KEY}`
+ **优势**:
    - ✅ 无需申请OpenAI官方账号
    - ✅ 成本可控，统一管理
    - ✅ 完全兼容OpenAI SDK
    - ✅ 支持GPT-4、GPT-3.5等主流模型
+ **前端SDK**: Vercel AI SDK (ai)
+ **流式处理**: EventSource / SSE
+ 后续使用Gemini的模型，好处上下文够长、语言有温度，对中文理解比模型要好

#### UI框架与组件
+ **原计划**: Shadcn/ui + Radix UI
+ **当前实现**: 自定义组件（建议调整）
+ **样式方案**: Tailwind CSS 4.1.8
+ **图标**: Lucide React
+ **动画**: Framer Motion（可选）

#### 状态管理
+ **全局状态**: Zustand ✅（已实现）
+ **服务端状态**: TanStack Query (React Query) ⚠️（待添加）
+ **表单状态**: React Hook Form（待添加）

#### 数据验证
+ **Schema验证**: Zod（待添加）

#### 图表与可视化
+ **图表库**: Recharts ✅（已集成）
+ **关系图**: ReactFlow（用于世界观关系网络，待集成）

---

### 二、后端技术栈（Python）
#### 核心框架
+ **Web框架**: FastAPI 0.109+
+ **异步服务器**: Uvicorn
+ **ASGI服务器**: Gunicorn（生产环境）
+ **Python版本**: 3.11+

#### 数据库
+ **主数据库**: PostgreSQL 15+
+ **ORM**: SQLAlchemy 2.0 (Async)
+ **数据库驱动**: asyncpg
+ **数据库迁移**: Alembic
+ **缓存**: Redis 7.x
+ **Redis客户端**: redis-py + aioredis

#### AI核心 ⭐
+ **主要AI提供商**: 第三方OpenAI兼容API ([https://204992.xyz](https://204992.xyz))
+ **AI框架**: LangChain 0.1+
+ **AI集成**:
    - `openai` - OpenAI SDK（配置自定义base_url）
    - `langchain-openai` - LangChain OpenAI集成
+ **Token计数**: tiktoken
+ **向量数据库**: ChromaDB/PGSQL
+ **Embeddings**: sentence-transformers

#### 认证与安全
+ **JWT**: python-jose[cryptography]
+ **密码加密**: passlib[bcrypt]
+ **CORS**: fastapi.middleware.cors

#### 异步任务
+ **任务队列**: Celery 5.3+
+ **消息代理**: Redis (Celery Broker)
+ **任务监控**: Flower

#### 数据验证
+ **Schema**: Pydantic 2.5+
+ **Email验证**: email-validator

#### 文件存储
+ **对象存储**: 阿里云OSS
+ **本地存储**: aiofiles

#### 日志与监控
+ **日志**: loguru
+ **性能监控**: prometheus-client
+ **错误追踪**: sentry-sdk

---

### 三、数据库设计
#### 核心表结构
**用户系统**:

+ `users` - 用户表
+ `user_profiles` - 用户资料
+ `user_subscriptions` - 订阅信息
+ `user_credits` - 积分账户
+ `roles` - 角色表
+ `permissions` - 权限表

**小说系统**:

+ `works` / `novels` - 小说作品
+ `volumes` - 卷
+ `chapters` - 章节
+ `scenes` - 场景
+ `novel_tags` - 标签
+ `novel_statistics` - 统计数据

**世界观系统**:

+ `settings` - 设定条目
+ `setting_relations` - 设定关系
+ `setting_snapshots` - 历史快照
+ `characters` - 角色设定
+ `locations` - 地点设定
+ `factions` - 势力设定

**AI系统**:

+ `ai_requests` - AI请求日志
+ `ai_models` - AI模型配置
+ `user_api_keys` - 用户API密钥
+ `prompts` - 提示词
+ `prompt_presets` - 提示词预设
+ `ai_templates` - AI模板

**内容管理**:

+ `snippets` - 片段/灵感
+ `outlines` - 大纲
+ `notes` - 笔记
+ `bookmarks` - 书签

---

### 四、开发工具链
#### 版本控制
+ **VCS**: Git
+ **代码托管**: GitHub
+ **分支策略**: Git Flow

#### 容器化
+ **容器引擎**: Docker 24+
+ **编排工具**: Docker Compose
+ **镜像仓库**: Docker Hub / 私有Registry

#### CI/CD
+ **CI平台**: GitHub Actions
+ **自动化测试**: pytest + Vitest/Jest
+ **部署方式**: Docker + Nginx

#### 代码质量
**前端**:

+ ESLint + Prettier
+ TypeScript strict mode
+ Husky pre-commit hooks

**后端**:

+ black (代码格式化)
+ isort (导入排序)
+ flake8 (代码检查)
+ mypy (类型检查)
+ pre-commit

---

### 五、基础设施
#### 云服务提供商
**选项1 - 阿里云**:

+ **计算**: ECS / SAE
+ **数据库**: RDS PostgreSQL
+ **缓存**: Redis
+ **存储**: OSS
+ **CDN**: CDN
+ **负载均衡**: SLB

#### 监控与日志
+ **应用监控**: Prometheus + Grafana
+ **错误追踪**: Sentry
+ **日志聚合**: ELK Stack（可选）

---

### 六、第三方服务
#### AI服务 ⭐ 主力方案
**推荐：第三方OpenAI兼容API**

+ **服务地址**: `https://204992.xyz`
+ **API密钥**: `{:LOCAL_API_KEY}`（环境变量配置）
+ **兼容性**: 完全兼容OpenAI API规范
+ **优势**:
    - ✅ 无需注册OpenAI官方账号
    - ✅ 无需信用卡和海外手机号
    - ✅ 成本统一管理，预算可控
    - ✅ 国内访问稳定，无需代理
    - ✅ 完全兼容现有OpenAI SDK

#### 对象存储
+ 阿里云OSS

#### CDN
+ Cloudflare（推荐，免费）
+ 阿里云CDN

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

---

### 4. Git 提交规范
#### Commit Message 格式
```bash
<type>(<scope>): <subject>

<body>

<footer>
```

#### Type 类型
```plain
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

# ❌ 避免
update editor
fix bug
改了点东西
```

---

## 📊 当前项目状态分析
## 🎯 项目关键差异分析
### 当前实现状态对比
| 方面 | 规划方案 | 当前实现 | 状态 |
| --- | --- | --- | --- |
| **前端框架** | React 19 + Vite | React 19 + Vite | ✅ 已完成 |
| **编辑器** | Tiptap / Novel | 未集成 | ❌ 待实现（P0） |
| **后端** | FastAPI + Python | 进行中 | ⚠️ 进行中 |
| **数据库** | PostgreSQL + Redis | 未开始 | ❌ 待实现（P0） |
| **AI集成** | OpenAI兼容API | 未集成 | ❌ 待实现（P0） |
| **状态管理** | Zustand + React Query | Zustand | ⚠️ 部分实现 |
| **UI组件** | Shadcn/ui | 自定义组件 | ⚠️ 建议调整 |


---

## 📋 任务优先级分类
### 🔴 P0 - 阻塞性任务（必须立即完成）
#### 1. 编辑器集成 ✅ **已完成 (100%)**
**状态**: ✅ 已完成  
**完成时间**: 2025-10-16

**已完成功能**:

+ ✅ Tiptap 依赖安装（3.7.0）
+ ✅ Novel 编辑器组件创建 (`NovelEditor.tsx`)
+ ✅ 基础富文本功能（粗体、斜体、标题、列表等）
+ ✅ 工具栏组件 (`EditorToolbar.tsx`)
+ ✅ 字数统计实时显示
+ ✅ 占位符提示
+ ✅ 自动保存（localStorage + 回调）
+ ✅ 保存状态提示（已保存/保存中/未保存）
+ ✅ Slash 命令菜单（11 个命令 + 搜索）
+ ✅ 气泡菜单（9 个格式化工具）
+ ✅ 拖拽手柄（段落拖拽）
+ ✅ 代码块语法高亮（37 种语言）
+ ✅ Markdown 支持（粘贴转换）
+ ✅ 集成到 EditorView 页面

**完成度**: 85% (相比 Novel 原版)

**核心文件**:

+ `src/components/editor/NovelEditor.tsx` - 主编辑器
+ `src/components/editor/EditorToolbar.tsx` - 工具栏
+ `src/components/editor/BubbleMenu.tsx` - 气泡菜单
+ `src/components/editor/SlashCommands.tsx` - 命令列表
+ `src/components/editor/SlashCommandExtension.tsx` - Slash 扩展
+ `src/components/editor/editor-styles.css` - 编辑器样式
+ `src/components/editor/interactive-styles.css` - 交互样式

**编辑器状态**:

+ ✅ 核心文本编辑功能完整（富文本、标题、列表等）
+ ✅ Slash 命令系统（11个命令）
+ ✅ AI 功能集成（续写、润色、扩写、总结、翻译）
+ ✅ 字数统计和自动保存

> **注**: 图片上传、视频嵌入、数学公式等功能对小说写作编辑器不是必需功能，已从需求中移除
>

---

#### 2. 后端基础架构搭建 ✅ **已完成 (85-90%)**
**状态**: ✅ 核心功能已完成  
**完成时间**: 2025-10-15

**已完成功能**:

**1. 用户认证系统 - 100% ****⭐**** 前后端已完整对接**

**后端接口**:

+ ✅ 用户注册 `POST /api/v1/auth/register` - 返回用户信息和Token
+ ✅ 用户登录 `POST /api/v1/auth/login` - 返回用户信息和Token
+ ✅ Token 刷新 `POST /api/v1/auth/refresh`
+ ✅ 获取当前用户 `GET /api/v1/auth/me`
+ ✅ JWT Token 生成和验证
+ ✅ 密码加密（bcrypt）

**前端对接** (2025-10-16完成):

+ ✅ 创建 `AuthService.ts` - 统一认证服务
+ ✅ 更新 `ApiAdapter.ts` - 配置请求/响应拦截器
+ ✅ 修改类型定义 - 匹配后端数据结构
+ ✅ 优化登录/注册流程 - 一次请求完成（无需额外/me请求）
+ ✅ 实现 Token 自动管理 - localStorage持久化
+ ✅ LoginView 完整对接 - 支持用户名/邮箱登录
+ ✅ RegisterView 完整对接 - 注册即登录

**2. 作品管理系统 - 100%**

+ ✅ 创建作品 `POST /api/v1/works`
+ ✅ 获取作品列表 `GET /api/v1/works`
+ ✅ 获取作品详情 `GET /api/v1/works/{id}`
+ ✅ 更新作品 `PUT /api/v1/works/{id}`
+ ✅ 删除作品 `DELETE /api/v1/works/{id}`
+ ✅ 作品统计（字数、章节数）自动更新

**3. 章节管理系统 - 100%**

+ ✅ 创建章节 `POST /api/v1/chapters`
+ ✅ 获取章节列表 `GET /api/v1/chapters/work/{id}`
+ ✅ 获取章节详情 `GET /api/v1/chapters/{id}`
+ ✅ 更新章节 `PUT /api/v1/chapters/{id}`
+ ✅ 删除章节 `DELETE /api/v1/chapters/{id}`
+ ✅ 章节排序 `POST /api/v1/chapters/reorder`
+ ✅ 字数统计自动更新

**4. 数据库系统 - 90%**

+ ✅ PostgreSQL 数据库连接
+ ✅ SQLAlchemy Async ORM
+ ✅ User 模型（完整）
+ ✅ Work 模型（完整）
+ ✅ Chapter 模型（完整）
+ ✅ 数据库关系配置
+ ✅ Alembic 数据库迁移配置

**5. 基础设施 - 70%**

+ ✅ FastAPI 应用配置
+ ✅ CORS 中间件
+ ✅ JWT 认证中间件
+ ✅ 全局异常处理
+ ✅ 日志系统（基础）
+ ✅ Pydantic 数据验证
+ ✅ asyncpg 异步驱动
+ 🟡 Redis 配置（已配置，未实际使用）

**测试状态**:

+ ✅ 14/14 核心API测试通过（100%通过率）
+ ✅ 用户注册/登录流程测试通过
+ ✅ 作品和章节CRUD完整测试
+ ✅ Token刷新机制测试通过

**核心文件**:

+ `backend/app/main.py` - 应用入口
+ `backend/app/api/v1/auth.py` - 认证接口
+ `backend/app/api/v1/users.py` - 用户接口
+ `backend/app/api/v1/works.py` - 作品接口
+ `backend/app/api/v1/chapters.py` - 章节接口
+ `backend/app/models/` - 数据模型
+ `backend/app/services/` - 业务逻辑
+ `backend/app/core/` - 核心配置

**待完成（低优先级）**:

- [ ] Redis 实际使用（Token缓存、数据缓存）
- [ ] Docker Compose 生产环境配置
- [ ] 世界观相关模型（Character、Location、Faction）
- [ ] 监控系统（Prometheus + Grafana）

**实际目录结构**:

```plain
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

+ ✅ 前端: 创建 AI 配置管理 (`src/config/ai.config.ts`)
+ ✅ 前端: 创建 AI 服务类 (`src/services/AIService.ts`)
+ ✅ 前端: 创建 AI Hook (`src/hooks/useAI.ts`)
+ ✅ 前端: 实现流式响应处理
+ ✅ 前端: 创建 AI 菜单组件 (`src/components/editor/AIMenu.tsx`)
+ ✅ 前端: 创建 AI 高亮扩展 (`src/components/editor/AIHighlightExtension.ts`)
+ ✅ 前端: 创建 Toast 通知系统 (`src/components/ui/Toast.tsx` + `src/hooks/useToast.ts`)
+ ✅ 前端: 集成到 NovelEditor
+ ✅ 前端: Slash 命令触发 AI 功能

**核心文件**:

+ `src/config/ai.config.ts` - AI 配置管理
+ `src/services/AIService.ts` - AI API 调用（支持流式响应）
+ `src/hooks/useAI.ts` - AI Hook 封装
+ `src/components/editor/AIMenu.tsx` - AI 操作菜单
+ `src/components/editor/AIHighlightExtension.ts` - AI 内容高亮标记
+ `src/components/ui/Toast.tsx` - Toast 通知组件
+ `src/components/editor/interactive-styles.css` - AI 样式

**实现的 AI 功能**:

1. **AI 续写** - 流式实时输出，支持选中文本或上下文续写
2. **AI 扩写** - 扩展选中文本，增加细节
3. **AI 总结** - 总结选中文本，保留关键信息
4. **AI 润色** - 优化选中文本，提升流畅度
5. **AI 翻译** - 智能识别语言并翻译（中英互译）

**技术亮点**:

+ ✅ 流式响应实时显示（SSE）
+ ✅ AI 生成内容黄色高亮标记（带脉冲动画）
+ ✅ 同意/撤销操作（Accept/Reject）
+ ✅ 过滤 `<think>` 标签和 reasoning 内容
+ ✅ 完善的错误处理和调试日志
+ ✅ 防止标记传染（撤销后清除标记）
+ ✅ 支持多种 AI 模型配置

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

+ ✅ WorksView - 作品列表页面
+ ✅ WorkDetailView - 作品详情页面
+ ✅ EditorView - 编辑器页面

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

**技术细节**:

```typescript
// 需要实现的接口
interface WorkAPI {
  createWork(data: CreateWorkDTO): Promise<Work>;
  updateWork(id: string, data: UpdateWorkDTO): Promise<Work>;
  deleteWork(id: string): Promise<void>;
  getWorks(params: WorksQueryParams): Promise<WorksResponse>;
  getWorkDetail(id: string): Promise<WorkDetail>;
}

interface ChapterAPI {
  createChapter(workId: string, data: CreateChapterDTO): Promise<Chapter>;
  updateChapter(id: string, data: UpdateChapterDTO): Promise<Chapter>;
  deleteChapter(id: string): Promise<void>;
  reorderChapters(workId: string, order: string[]): Promise<void>;
}
```

---

#### 5. 用户系统完善 (预计5天)
**状态**: ✅ **已完成 (100%)** - 2025-10-16

**已完成**:

+ ✅ LoginView - 登录页面 (完整对接后端)
+ ✅ RegisterView - 注册页面 (完整对接后端)
+ ✅ SettingsView - 设置页面
+ ✅ Zustand authStore 状态管理
+ ✅ **连接后端认证 API** (2025-10-16完成)
    - ✅ 登录接口 - 支持用户名/邮箱登录
    - ✅ 注册接口 - 注册即登录
    - ✅ 登出接口 - 清除本地Token
    - ✅ Token 刷新机制 - 自动刷新过期Token
+ ✅ **JWT Token 管理** (2025-10-16完成)
    - ✅ 存储到 localStorage - 使用 auth-storage
    - ✅ 自动附加到请求头 - 通过 axios 拦截器
    - ✅ Token 过期处理 - 统一错误处理
    - ✅ 自动刷新 Token - 支持 refresh_token
+ ✅ **事务管理优化** (2025-10-16完成)
    - ✅ 修复注册/登录事务回滚问题
    - ✅ 使用 flush 替代 commit（延迟提交）
    - ✅ 统一异常处理和回滚机制

**待完成** (低优先级):

- [ ] 用户资料管理
    - [ ] 修改用户名
    - [ ] 修改邮箱
    - [ ] 上传头像
    - [ ] 修改简介
- [ ] 密码管理
    - [ ] 修改密码
    - [ ] 忘记密码（邮件重置）
- [ ] 第三方登录（可选）
    - [ ] Google OAuth
    - [ ] GitHub OAuth

---

#### 6. 管理后台数据对接 (预计3天)
**状态**: ⚠️ 部分完成（仅前端UI + Mock数据）

**已完成**:

+ ✅ AdminDashboardView - 数据面板 (Mock 数据)
+ ✅ AdminUsersView - 用户管理 (Mock 数据)
+ ✅ AdminAIModelsView - AI 模型管理 (Mock 数据)
+ ✅ AdminCostView - 成本监控 (Mock 数据)
+ ✅ AdminContentView - 内容审核 (Mock 数据)

**待完成**:

- [ ] 连接后端管理 API
    - [ ] `/api/admin/dashboard` - 仪表盘数据
    - [ ] `/api/admin/users` - 用户管理
    - [ ] `/api/admin/ai-models` - AI 模型配置
    - [ ] `/api/admin/cost` - 成本统计
    - [ ] `/api/admin/content` - 内容审核
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
- [ ] 实现内容审核功能
    - [ ] 审核队列
    - [ ] 批准/拒绝操作
    - [ ] 审核日志

---

### 🟢 P2 - 中优先级任务（增强功能）
#### 7. 世界观构建系统 (预计2周)
**状态**: ❌ 未开始

**功能需求**:

- [ ] 创建世界观管理页面 (`/worldbuilding/:workId`)
- [ ] 设定条目管理
    - [ ] 角色设定 (Characters)
    - [ ] 地点设定 (Locations)
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

**数据库设计**:

```sql
-- 设定表
CREATE TABLE settings (
  id UUID PRIMARY KEY,
  work_id UUID REFERENCES works(id),
  type VARCHAR(50), -- character/location/faction/item
  name VARCHAR(200),
  description TEXT,
  attributes JSONB, -- 灵活存储各类属性
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);

-- 设定关系表
CREATE TABLE setting_relations (
  id UUID PRIMARY KEY,
  from_setting_id UUID REFERENCES settings(id),
  to_setting_id UUID REFERENCES settings(id),
  relation_type VARCHAR(50), -- family/enemy/friend/belongs_to
  description TEXT
);
```

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

**AI Prompt 示例**:

```typescript
const outlinePrompt = `
请为以下小说生成详细大纲：

【作品信息】
标题: {title}
类型: {genre}
简介: {description}

【要求】
1. 采用三幕剧结构
2. 包含3-5个主要情节线
3. 每一幕包含3-5个关键事件
4. 每个事件控制在50-100字

【输出格式】
以JSON格式输出，结构如下:
{
  "act1": [...],
  "act2": [...],
  "act3": [...]
}
`;
```

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

**数据结构**:

```typescript
interface Prompt {
  id: string;
  name: string;
  description: string;
  category: 'system' | 'user' | 'work';
  content: string; // 支持变量占位符
  variables: PromptVariable[]; // 变量定义
  isPublic: boolean;
  usageCount: number;
  createdAt: Date;
}

interface PromptVariable {
  key: string;
  label: string;
  type: 'text' | 'number' | 'select';
  defaultValue?: any;
  options?: string[]; // for select type
}
```

---

#### 10. 数据统计和可视化完善 (预计3天)
**状态**: ⚠️ 部分完成（仅前端UI）

**已完成**:

+ ✅ AdminDashboardView 基础图表（用户增长、AI 调用统计）
+ ✅ AdminCostView 成本图表（成本趋势、模型分布）

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

**技术方案**:

+ 使用现有 Recharts 库
+ 新增 D3.js 用于复杂可视化（词云图、热力图）
+ 后端提供聚合查询接口

---

### 🔵 P3 - 低优先级任务（优化和扩展）
#### 11. 文件导入导出 (预计1周)
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

#### 12. 协作功能 (预计2周)
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

**技术栈**:

+ WebSocket (FastAPI WebSocket)
+ Yjs (CRDT 协作算法)
+ Tiptap Collaboration 扩展

---

#### 13. 离线编辑支持 (预计3天)
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

#### 14. 搜索功能 (预计5天)
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

**技术方案**:

+ 后端: PostgreSQL 全文搜索
+ 前端: 搜索框组件 + 结果面板

```sql
-- PostgreSQL 全文搜索索引
CREATE INDEX idx_chapters_content_fts
ON chapters
USING gin(to_tsvector('chinese', content));
```

---

#### 15. 通知系统 (预计3天)
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

**技术方案**:

+ WebSocket 实时通知推送
+ 邮件通知（使用 SendGrid 或阿里云邮件）

---

#### 16. 主题和个性化 (预计2天)
**状态**: ⚠️ 部分完成（SettingsView 有主题设置但未实现）

**已完成**:

+ ✅ SettingsView 主题选择器 UI

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

#### 17. 移动端适配 (预计1周)
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
#### 18. 支付和订阅系统 (预计2周)
**状态**: ❌ 未开始

**功能需求**:

- [ ] 订阅计划设计
    - [ ] 免费版（基础功能）
    - [ ] 专业版（增强功能 + 更多配额）
    - [ ] 团队版（协作功能）
- [ ] 支付集成
    - [ ] 支付宝
    - [ ] 微信支付
    - [ ] Stripe（国际支付）
- [ ] 订阅管理
    - [ ] 升级/降级
    - [ ] 续费提醒
    - [ ] 发票管理
- [ ] 配额管理
    - [ ] AI 调用次数限制
    - [ ] 存储空间限制
    - [ ] 作品数量限制

---

#### 19. 插件系统 (预计3周)
**状态**: ❌ 未开始

**功能需求**:

- [ ] 插件架构设计
- [ ] 插件 API 定义
- [ ] 插件市场
- [ ] 插件安装和管理
- [ ] 示例插件
    - [ ] 语法检查插件
    - [ ] 敏感词检测插件
    - [ ] 自定义 AI 模型插件

---

#### 20. 性能优化和监控 (预计1周)
**状态**: ❌ 未开始

**优化项**:

- [ ] 前端性能优化
    - [ ] 代码分割
    - [ ] 懒加载
    - [ ] 图片优化
    - [ ] Bundle 体积分析
- [ ] 后端性能优化
    - [ ] 数据库查询优化
    - [ ] Redis 缓存策略
    - [ ] API 响应时间优化
- [ ] 监控集成
    - [ ] Sentry 错误追踪
    - [ ] Prometheus + Grafana
    - [ ] 性能指标监控

---

## 🛠️ 技术债务和重构任务
### 技术栈调整评估
#### 问题1: 编辑器方案选择
**现状**: ✅ 前端技术栈已确定为 React + Vite  
**待决策**: 选择 Tiptap 还是 Novel 编辑器

**方案A - Tiptap（推荐）**:

+ ✅ 优势:
    - 与 React + Vite 完美兼容
    - 高度可定制，灵活性强
    - 社区活跃，文档完善
    - 不依赖特定框架
+ ❌ 劣势:
    - 需要自己实现AI集成
    - UI需要自己设计

**方案B - Novel**:

+ ✅ 优势:
    - AI功能开箱即用
    - Notion风格UI现成
    - 节省开发时间
+ ❌ 劣势:
    - 需要适配Vite环境
    - 定制性相对较弱

**最终决策**: ✅ 优先使用 Tiptap，快速实现MVP功能

---

#### 问题2: 自定义组件 vs Shadcn/ui
**现状**: 使用自定义组件 (Button, Input, Card 等)  
**计划**: todo.md 建议使用 Shadcn/ui

**评估**:

+ 当前自定义组件功能有限
+ Shadcn/ui 提供更丰富的组件和一致性
+ Shadcn/ui 基于 Radix UI，可访问性更好

**建议**: 逐步迁移到 Shadcn/ui

1. 保留现有组件（向后兼容）
2. 新功能使用 Shadcn/ui
3. 逐步替换旧组件

---

#### 问题3: 缺少 React Query
**现状**: 仅使用 Zustand，缺少服务端状态管理  
**影响**: 手动管理 API 请求、缓存、加载状态

**建议**: 引入 TanStack Query (React Query)

```bash
npm install @tanstack/react-query
```

**示例用法**:

```typescript
// 替换前
const fetchWorks = async () => {
  setLoading(true);
  try {
    const data = await DataService.getWorks();
    setWorks(data);
  } catch (error) {
    setError(error);
  } finally {
    setLoading(false);
  }
};

// 替换后
const { data: works, isLoading, error } = useQuery({
  queryKey: ['works'],
  queryFn: DataService.getWorks
});
```

---

### 代码规范和工具链
#### 缺失的开发工具
- [ ] 配置 ESLint 规则完善
- [ ] 配置 Prettier
- [ ] 配置 Husky + lint-staged (Git Hooks)
- [ ] 配置 commitlint (规范 commit message)
- [ ] 配置 Jest 或 Vitest (单元测试)
- [ ] 配置 Playwright (E2E 测试)

---

## 📊 开发里程碑规划
### Milestone 1: 核心编辑功能 ⚠️ **进行中 (80-85%)**
**目标**: 实现基本的写作和编辑功能

**任务**:

+ ✅ 前端UI框架 (已完成 100%)
+ ✅ 后端基础架构 (P0-2) - 已完成 85-90%
+ ✅ 编辑器集成 (P0-1) - 已完成 100%
+ ✅ AI 服务集成 (P0-3) - 前端完成 100%，后端待开发
- [ ] 作品和章节管理 (P1-4) - 后端完成，前端待对接
- [ ] 用户系统完善 (P1-5) - 后端完成，前端待对接

**交付物完成度**:

+ ✅ 可用的编辑器 (已完成 - Tiptap + Slash命令 + AI菜单)
+ ✅ 作品和章节 CRUD (后端已完成，前端待对接)
+ ⚠️ AI 续写基础功能 (前端已完成，后端待实现)
+ ✅ 用户登录注册 (后端已完成，前端待对接)

**当前瓶颈**: 

+ 🔴 前后端未对接 - 前端使用Mock数据，需要切换到真实API
+ 🔴 AI后端服务未实现 - 前端AI功能完整，但后端接口缺失

---

### Milestone 2: AI 增强功能 (2周)
**目标**: 完善 AI 辅助写作能力

**任务**:

- [ ] 提示词管理系统 (P2-9)
- [ ] 大纲生成功能 (P2-8)
- [ ] AI 参数配置
- [ ] Token 计费系统
- [ ] 管理后台数据对接 (P1-6)

**交付物**:

+ 多样化的 AI 写作工具
+ 完整的成本追踪
+ 管理后台正常运作

---

### Milestone 3: 世界观和组织工具 (3周)
**目标**: 提供专业的创作辅助工具

**任务**:

- [ ] 世界观构建系统 (P2-7)
- [ ] 数据统计和可视化 (P2-10)
- [ ] 搜索功能 (P3-14)
- [ ] 文件导入导出 (P3-11)

**交付物**:

+ 世界观管理功能
+ 创作统计分析
+ 全局搜索
+ 文件导入导出

---

### Milestone 4: 协作和优化 (2周)
**目标**: 提升用户体验和性能

**任务**:

- [ ] 协作功能 (P3-12)
- [ ] 离线编辑支持 (P3-13)
- [ ] 通知系统 (P3-15)
- [ ] 主题和个性化 (P3-16)
- [ ] 移动端适配 (P3-17)
- [ ] 性能优化 (P4-20)

---

### Milestone 5: 商业化 (2周)
**目标**: 实现盈利能力

**任务**:

- [ ] 支付和订阅系统 (P4-18)
- [ ] 营销落地页
- [ ] 用户增长功能
- [ ] SEO 优化

---

## 🚀 快速启动建议
### 如果你只有1周时间
**聚焦 MVP**:

1. ✅ 保持现有 React + Vite（暂不迁移）
- [ ] 完成后端基础架构（3天）
- [ ] 集成简单文本编辑器（Tiptap，1天）
- [ ] 连接前后端 API（2天）
- [ ] 基本的 AI 续写（1天）

### 如果你有1个月时间
**完成 Milestone 1 + 2**:

- [ ] 使用Tiptap集成编辑器（5天）
- [ ] 完成核心编辑功能（3周）
- [ ] 完成 AI 增强功能（1周）

### 如果你有3个月时间
**完成 Milestone 1-4**:

+ 第1个月: 核心功能 + AI 功能
+ 第2个月: 世界观工具 + 搜索导出
+ 第3个月: 协作功能 + 优化

---

## 📝 备注说明
### 技术选型说明
1. **前端框架**: ✅ 确定使用 React 19 + Vite
2. **UI 组件**: ⚠️ 建议从自定义组件迁移到 Shadcn/ui
3. **状态管理**: ⚠️ 建议添加 TanStack Query（React Query）
4. **编辑器**: ⚠️ 优先使用 Tiptap，备选 Novel

### 关键风险提示
✅ ~~编辑器待集成~~: 编辑器已完成集成（Tiptap 3.7.0 + Slash命令 + AI菜单）  
✅ ~~后端缺失~~: 后端核心功能已完成（用户、作品、章节 API 已实现并测试通过）  
🔴 **前后端未对接**: 前端仍使用Mock数据，需要实现ApiAdapter连接真实后端API（最高优先级）  
🔴 **AI后端服务缺失**: 前端AI功能完整，但后端OpenAI集成未实现（最高优先级）  
⚠️ **服务端状态管理**: 建议集成 React Query，优化数据管理和缓存

---

## 📞 联系和反馈
如有任何问题或需要调整优先级，请及时沟通。

---

## 📚 参考资源
### 开源项目参考
#### 1. MaliangAINovalWriter（马良AI写作）
+ **GitHub**: [https://github.com/Deng-m1/MaliangAINovalWriter](https://github.com/Deng-m1/MaliangAINovalWriter)
+ **技术栈**: Flutter Web + Spring Boot
+ **可借鉴点**:
    - 完整的SaaS架构设计
    - 世界观构建系统
    - 提示词管理（系统/用户/预设三层）
    - LLM可观测性（日志/统计/成本分析）
    - 多模型动态切换机制

#### 2. Novel
+ **官网**: [https://novel.sh](https://novel.sh)
+ **GitHub**: [https://github.com/steven-tey/novel](https://github.com/steven-tey/novel)
+ **技术栈**: Tiptap + React
+ **可借鉴点**:
    - Notion风格的编辑器体验
    - AI自动补全集成
    - Slash命令系统
    - Bubble Menu（选中文本工具栏）
    - 无头架构设计（编辑器核心与UI分离）

#### 3. novelWriter
+ **GitHub**: [https://github.com/vkbo/novelWriter](https://github.com/vkbo/novelWriter)
+ **技术栈**: Python + Qt
+ **可借鉴点**:
    - 纯文本存储方案（易于版本控制）
    - 文档树形组织结构
    - 元数据标记系统（@character, @location等）
    - 实时索引与交叉引用
    - 项目快照与版本管理

### 技术文档
#### 前端相关
+ **React官方文档**: [https://react.dev](https://react.dev)
+ **Vite文档**: [https://vitejs.dev](https://vitejs.dev)
+ **Tiptap文档**: [https://tiptap.dev](https://tiptap.dev)
+ **Novel文档**: [https://novel.sh](https://novel.sh)
+ **Tailwind CSS**: [https://tailwindcss.com](https://tailwindcss.com)
+ **Shadcn/ui**: [https://ui.shadcn.com](https://ui.shadcn.com)
+ **TanStack Query**: [https://tanstack.com/query](https://tanstack.com/query)
+ **Zustand**: [https://github.com/pmndrs/zustand](https://github.com/pmndrs/zustand)

#### 后端相关
+ **FastAPI文档**: [https://fastapi.tiangolo.com](https://fastapi.tiangolo.com)
+ **SQLAlchemy**: [https://www.sqlalchemy.org](https://www.sqlalchemy.org)
+ **PostgreSQL文档**: [https://www.postgresql.org/docs](https://www.postgresql.org/docs)
+ **Redis文档**: [https://redis.io/docs](https://redis.io/docs)
+ **LangChain文档**: [https://python.langchain.com](https://python.langchain.com)
+ **OpenAI API**: [https://platform.openai.com/docs](https://platform.openai.com/docs)

#### AI相关
+ **Vercel AI SDK**: [https://sdk.vercel.ai/docs](https://sdk.vercel.ai/docs)
+ **OpenAI Cookbook**: [https://github.com/openai/openai-cookbook](https://github.com/openai/openai-cookbook)
+ **Prompt Engineering Guide**: [https://www.promptingguide.ai](https://www.promptingguide.ai)

### 学习资源
#### 视频教程
+ **Tiptap入门**: YouTube搜索 "Tiptap Tutorial"
+ **FastAPI教程**: FastAPI官方教程
+ **LangChain实战**: LangChain官方文档

#### 博客文章
+ **如何构建AI写作工具**: 搜索相关技术博客
+ **Novel编辑器深度解析**: Novel GitHub讨论区
+ **小说写作平台架构设计**: 各大技术社区

### 社区与支持
#### 开发者社区
+ **GitHub Discussions**: 各项目的讨论区
+ **Discord**: Tiptap、FastAPI官方Discord
+ **Stack Overflow**: 技术问题求助

#### 中文社区
+ **掘金**: 搜索相关技术文章
+ **V2EX**: 技术讨论
+ **知乎**: AI应用开发相关话题

---

## 📋 文档更新日志
### v2.3 (2025-01-16)
+ 🎉 更新后端开发完成状态
+ ✅ 更新P0-2后端基础架构任务状态为"已完成 85-90%"
+ ✅ 详细列出后端已完成的5大模块
    - 用户认证系统 100%
    - 作品管理系统 100%
    - 章节管理系统 100%
    - 数据库系统 90%
    - 基础设施 70%
+ ✅ 更新Milestone 1进度为"进行中 80-85%"
+ ✅ 更新关键风险提示（编辑器和后端风险已解决）
+ ✅ 标注当前主要瓶颈：前后端对接和AI后端服务

### v2.2 (2025-01-16)
+ 🎉 整合前端开发规范文档（todo2.md）
+ ✅ 新增完整的代码规范章节
    - TypeScript 规范
    - React 组件规范
    - 编辑器开发规范
    - Git 提交规范
+ ✅ 更新编辑器集成任务状态为"已完成"
+ ✅ 更新 AI 服务前端部分状态为"已完成"
+ ✅ 详细列出编辑器和 AI 功能的完成项
+ ✅ 统一文档版本和格式

### v2.1 (2025-01-15)
+ 🎉 整合v1.2技术栈规划与v2.0任务清单
+ ✅ 新增完整的技术栈详细说明
+ ✅ 新增团队简介部分
+ ✅ 新增参考资源章节
+ ✅ 优化文档结构，添加导航目录
+ ✅ 统一格式和排版

### v2.0 (2025-01-10)
+ 📊 基于当前项目实际情况的任务清单
+ 🎯 明确当前实现与原计划的差异
+ 📋 按优先级划分任务（P0-P3）
+ 🗓️ 制定详细的里程碑规划

### v1.2 (2025-01-05)
+ ⚙️ 完整的技术栈选型说明
+ 👥 团队简介与协作流程
+ 🔧 详细的AI配置指南
+ 📚 开发工具链和基础设施规划

---

## 📊 项目信息
+ **项目名称**: NovelAIde
+ **创建时间**: 2025-01-05
+ **当前版本**: v2.3 (整合版 + 前后端状态更新)
+ **最后更新**: 2025-01-16
+ **项目状态**: 🚧 开发中 - 前后端核心功能已完成，待对接
+ **技术栈**: React 19 + Vite + FastAPI + PostgreSQL
+ **团队规模**: 建议2-3人起步（MVP阶段）
+ **编辑器方案**: Tiptap（优先）/ Novel（备选） ⭐
+ **AI方案**: 第三方OpenAI兼容API ([https://204992.xyz](https://204992.xyz)) ⭐
+ **预计MVP**: 2025年Q1（3个月）

---

## 🎯 下一步行动
### 立即要做的事（本周）🔴 最高优先级
1. **前后端对接** (预计2-3天)
    - [ ] 实现ApiAdapter.ts，连接真实后端API
    - [ ] 配置axios拦截器和Token管理
    - [ ] 替换所有Mock数据调用
    - [ ] 测试用户注册-登录-作品-章节完整流程
2. **AI后端服务实现** (预计2-3天)
    - [ ] 创建OpenAI服务类（app/services/ai/openai_service.py）
    - [ ] 实现流式AI续写接口（POST /api/v1/ai/complete）
    - [ ] 实现Token计数和成本追踪
    - [ ] 前后端联调测试AI功能

### 近期目标（本月）
1. ✅ ~~完成P0任务（编辑器、后端、AI集成）~~ - 基本完成
2. 完成前后端完整对接
3. 完成AI后端服务实现
4. 完成Milestone 1 (目标: 95%以上)

### 中期目标（3个月）
1. 完成核心功能开发（Milestone 1-3）
2. 内部测试和优化
3. 准备上线MVP版本
4. 开始用户推广

---

**祝开发顺利！如有问题，请随时联系团队成员。** 🚀

