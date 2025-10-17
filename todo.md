

# NovelAIde - AI辅助写小说工具 - 完整项目文档 v2.1

> 整合版本说明: 本文档整合了原技术栈规划(v1.2)与当前项目实际情况(v2.0)
> 项目现状: React 19 + Vite + TypeScript 前端（已完成基础架构）
> 技术栈: React 19.1.1, TypeScript, Tailwind CSS 4.1.8, Zustand, Recharts
> 当前进度: 前端UI框架完成，后端未开始，编辑器未集成
> 技术方案: React 19 + Vite + FastAPI + PostgreSQL
> 状态: 🚧 开发中 - 前端基础完成，后端进行中

📑 文档导航
● 🎯 项目概述
● 👥 团队简介
● ⚙️ 技术栈规划
  ○ 前端技术栈
  ○ 后端技术栈
  ○ 数据库设计
  ○ 开发工具链
  ○ 基础设施
  ○ 第三方服务
● 📊 当前项目状态
● 📋 开发任务清单
● 🗓️ 开发路线图
● 🚀 快速启动
● 📚 参考资源

🎯 项目概述
项目背景
基于三个开源项目的深度分析（MaliangAINovalWriter、Novel、novelWriter），从零到一开发一款专业的AI辅助写小说工具。
项目目标
● ✅ 提升创作效率：AI续写、润色、大纲生成，让创作更快速
● ✅ 构建完整世界观：角色、地点、势力设定的系统化管理
● ✅ 管理长篇小说：清晰的章节、场景、片段管理体系
● ✅ 降低创作门槛：智能提示、自动补全，人人都能写小说
核心特色
● 🚀 现代化编辑器：基于Novel/Tiptap，提供Notion级别的编辑体验
● 🤖 强大AI能力：集成主流AI模型，支持多种创作辅助功能
● 🎨 世界观可视化：关系图、时间线、设定卡片等可视化工具
● 💰 成本可控：使用第三方OpenAI兼容API，价格友好

👥 团队简介
关于我们
我们是一支专注于AI内容创作工具的技术团队，致力于打造一款真正好用的AI辅助写小说工具，帮助小说作者提升创作效率，降低创作门槛。
项目使命
让每个热爱写作的人都能轻松创作出精彩的小说故事。
核心价值观
● 🚀 技术驱动：采用最新的AI技术和现代化Web架构
● 💡 用户为先：深度理解小说创作者的需求和痛点  
● ⚡ 快速迭代：敏捷开发，快速响应用户反馈
● 🎯 专业专注：专注小说创作领域，不做大而全的工具
团队构成（当前规划）
👨‍💻 技术团队（2-3人）
   - 全栈工程师：负责前后端开发
   - 技能栈：React + Vite + Python + AI集成

📊 产品团队（1人）
   - 产品经理：负责需求分析和产品规划
我们在做什么
产品名称：NovelAIde
核心功能：
● ✍️ 智能续写：AI根据上下文自动续写故事
● 📝 大纲生成：一键生成完整的章节大纲
● 🎨 世界观构建：AI辅助构建角色、地点、势力等设定
● 🔄 内容润色：智能优化文字表达和情节逻辑
● 📚 章节管理：高效管理长篇小说的章节和场景
技术亮点：
● 基于Novel编辑器，提供Notion级别的编辑体验
● 使用第三方OpenAI兼容API（https://204992.xyz），成本可控
● 现代化技术栈：React 19 + Vite + FastAPI + PostgreSQL
● 完整的CI/CD流程和Docker部署方案
当前状态
📍 阶段：开发初期 - 前端基础完成，后端待启动
📅 预计启动：2025年10月中旬
🎯 MVP目标：3个月内上线可用版本

---

## Fix: 注册成功却返回 500（期望 201）

现象
- 注册接口 `POST /api/v1/auth/register` 成功创建用户，但响应状态为 500。
- 预期行为：成功应返回 201 Created。

初步分析（基于代码通读）
- 路由：`backend/app/api/v1/auth.py` 中 `@router.post("/register", status_code=201)` 已声明 201。
- 服务层：`UserService.create_user` 内已执行 `await self.db.commit()` 并刷新实体。
- 数据库依赖：`get_db()` 在 `yield` 之后还会再次 `await session.commit()`。
- 全局异常：`backend/app/main.py` 对未处理异常统一转 500。

可能触发 500 的路径
- 业务层已提交成功后，`get_db` 退出时再次 `commit()` 或 `close()` 发生异常，被全局异常捕获 → 500。

解决思路（最小改动优先）
- 移除 `get_db()` 中 `yield` 之后的自动 `commit()`，由服务层显式掌控事务提交（当前服务层已普遍提交）。
- 同时在注册接口中明确返回 `JSONResponse(status_code=201, content=result)`，杜绝状态码被中间环节干扰。

待办清单（执行时逐条勾选）
- [x] 通读并确认注册接口与DB依赖实现（auth.py / database.py）
- [x] 修改 `get_db()`：移除 `yield` 后自动 `commit()`，保留异常回滚与关闭
- [x] 调整注册接口：使用 `JSONResponse(status_code=201, content=...)`
- [ ] 本地验证：重复注册应 400，首次注册应 201，且不再出现 500
- [ ] Review：记录修改点、影响面与后续建议

Review
- 变更文件：
  - `backend/app/core/database.py`：去除自动提交，避免请求结束阶段异常。
  - `backend/app/api/v1/auth.py`：注册接口返回 `JSONResponse(201)`。
- 影响面：
  - 事务提交从“依赖自动提交 + 服务层提交并存”收敛为“服务层显式提交”。
  - 其他服务层已使用 `await self.db.commit()`，无需额外调整。
- 风险与回退：
  - 若部分路径遗漏提交，将表现为数据未持久化；可在对应服务路径补上 `commit()`。
  - 如需回退，只需恢复 `get_db()` 的自动提交行。

本地验证建议
- 首次调用 `POST /api/v1/auth/register`，应返回 201 且包含用户字段。
- 使用相同用户名或邮箱再次注册，应返回 400（ValueError -> HTTP 400）。
- 观察不再出现 500；如仍出现，请提供服务端日志定位余留路径。

补充修复：并发下唯一约束异常映射
- 新增：在 `backend/app/api/v1/auth.py` 注册接口中捕获 `IntegrityError`，返回 400（`Username or email already exists`）。
- 目的：避免并发或竞态时命中数据库唯一约束由全局异常处理转 500。

进一步重构（已完成）
- 注册接口 `response_model=UserResponse`，直接返回 ORM 对象，由 Pydantic 统一序列化，移除手写字典与自定义 JSONResponse。
- 重复冲突返回码调整为 `409 Conflict`，更符合 REST 语义。

验证补充
- 注册成功：201 + UserResponse 结构（含 id/时间戳等）。
- 重复用户名/邮箱：409，detail 为 `Username or email already exists`。


⚙️ 技术栈规划
技术选型说明
最终确定方案：React 19 + Vite + FastAPI + PostgreSQL
前端状态：✅ 基础架构已完成
后端状态：⚠️ 进行中
优势：快速迭代、灵活可控、生态成熟
一、前端技术栈
核心框架 ✅ 已确定
● 框架: React 19.1.1
● 语言: TypeScript 5.x
● 包管理: npm / pnpm
● 构建工具: Vite 5.x
编辑器方案 ⭐
● 推荐方案: Novel (基于Tiptap 2.x)
● 为什么选Novel:
  ○ ✅ 开箱即用的Notion风格编辑器
  ○ ✅ AI功能已集成（续写、补全、Slash命令）
  ○ ✅ 节省2-3周开发时间
  ○ ✅ Apache 2.0许可证，可商用
  ○ ✅ 6.2k+ Stars，持续维护
● 核心依赖:
  ○ novel - 完整编辑器组件
  ○ ai - Vercel AI SDK
  ○ @ai-sdk/openai - OpenAI集成
● 实施方案: 
  ○ 方案A: 直接使用Tiptap（推荐，更灵活）
  ○ 方案B: 集成Novel（需要适配Vite）
  ○ 决策: 先用Tiptap快速实现，后期评估是否迁移到Novel
AI集成 ⭐
● AI提供商: 第三方OpenAI兼容接口
  ○ Base URL: https://204992.xyz
  ○ API Key: 环境变量配置 {:LOCAL_API_KEY}
● 优势:
  ○ ✅ 无需申请OpenAI官方账号
  ○ ✅ 成本可控，统一管理
  ○ ✅ 完全兼容OpenAI SDK
  ○ ✅ 支持GPT-4、GPT-3.5等主流模型
● 前端SDK: Vercel AI SDK (ai)
● 流式处理: EventSource / SSE
● 后续使用Gemini的模型，好处上下文够长、语言有温度，对中文理解比模型要好
UI框架与组件
● 原计划: Shadcn/ui + Radix UI
● 当前实现: 自定义组件（建议调整）
● 样式方案: Tailwind CSS 4.1.8
● 图标: Lucide React
● 动画: Framer Motion（可选）
状态管理
● 全局状态: Zustand ✅（已实现）
● 服务端状态: TanStack Query (React Query) ⚠️（待添加）
● 表单状态: React Hook Form（待添加）
数据验证
● Schema验证: Zod（待添加）
图表与可视化
● 图表库: Recharts ✅（已集成）
● 关系图: ReactFlow（用于世界观关系网络，待集成）

二、后端技术栈（Python）
核心框架
● Web框架: FastAPI 0.109+
● 异步服务器: Uvicorn
● ASGI服务器: Gunicorn（生产环境）
● Python版本: 3.11+
数据库
● 主数据库: PostgreSQL 15+
● ORM: SQLAlchemy 2.0 (Async)
● 数据库驱动: asyncpg
● 数据库迁移: Alembic
● 缓存: Redis 7.x
● Redis客户端: redis-py + aioredis
AI核心 ⭐
● 主要AI提供商: 第三方OpenAI兼容API (https://204992.xyz)
● AI框架: LangChain 0.1+
● AI集成:
  ○ openai - OpenAI SDK（配置自定义base_url）
  ○ langchain-openai - LangChain OpenAI集成
● Token计数: tiktoken
● 向量数据库: ChromaDB/PGSQL
● Embeddings: sentence-transformers
认证与安全
● JWT: python-jose[cryptography]
● 密码加密: passlib[bcrypt]
● CORS: fastapi.middleware.cors
异步任务
● 任务队列: Celery 5.3+
● 消息代理: Redis (Celery Broker)
● 任务监控: Flower
数据验证
● Schema: Pydantic 2.5+
● Email验证: email-validator
文件存储
● 对象存储: 阿里云OSS
● 本地存储: aiofiles
日志与监控
● 日志: loguru
● 性能监控: prometheus-client
● 错误追踪: sentry-sdk

三、数据库设计
核心表结构
用户系统:
● users - 用户表
● user_profiles - 用户资料
● user_subscriptions - 订阅信息
● user_credits - 积分账户
● roles - 角色表
● permissions - 权限表
小说系统:
● works / novels - 小说作品
● volumes - 卷
● chapters - 章节
● scenes - 场景
● novel_tags - 标签
● novel_statistics - 统计数据
世界观系统:
● settings - 设定条目
● setting_relations - 设定关系
● setting_snapshots - 历史快照
● characters - 角色设定
● locations - 地点设定
● factions - 势力设定
AI系统:
● ai_requests - AI请求日志
● ai_models - AI模型配置
● user_api_keys - 用户API密钥
● prompts - 提示词
● prompt_presets - 提示词预设
● ai_templates - AI模板
内容管理:
● snippets - 片段/灵感
● outlines - 大纲
● notes - 笔记
● bookmarks - 书签

四、开发工具链
版本控制
● VCS: Git
● 代码托管: GitHub
● 分支策略: Git Flow
容器化
● 容器引擎: Docker 24+
● 编排工具: Docker Compose
● 镜像仓库: Docker Hub / 私有Registry
CI/CD
● CI平台: GitHub Actions
● 自动化测试: pytest + Vitest/Jest
● 部署方式: Docker + Nginx
代码质量
前端:
● ESLint + Prettier
● TypeScript strict mode
● Husky pre-commit hooks
后端:
● black (代码格式化)
● isort (导入排序)
● flake8 (代码检查)
● mypy (类型检查)
● pre-commit

五、基础设施
云服务提供商
选项1 - 阿里云:
● 计算: ECS / SAE
● 数据库: RDS PostgreSQL
● 缓存: Redis
● 存储: OSS
● CDN: CDN
● 负载均衡: SLB
监控与日志
● 应用监控: Prometheus + Grafana
● 错误追踪: Sentry
● 日志聚合: ELK Stack（可选）

六、第三方服务
AI服务 ⭐ 主力方案
推荐：第三方OpenAI兼容API
● 服务地址: https://204992.xyz
● API密钥: {:LOCAL_API_KEY}（环境变量配置）
● 兼容性: 完全兼容OpenAI API规范
● 优势:
  ○ ✅ 无需注册OpenAI官方账号
  ○ ✅ 无需信用卡和海外手机号
  ○ ✅ 成本统一管理，预算可控
  ○ ✅ 国内访问稳定，无需代理
  ○ ✅ 完全兼容现有OpenAI SDK
对象存储
● 阿里云OSS
CDN
● Cloudflare（推荐，免费）
● 阿里云CDN

📊 当前项目状态分析
🎯 项目关键差异分析
当前实现状态对比
方面	规划方案	当前实现	状态
前端框架	React 19 + Vite	React 19 + Vite	✅ 已完成
编辑器	Tiptap / Novel	未集成	❌ 待实现（P0）
后端	FastAPI + Python	进行中	⚠️ 进行中
数据库	PostgreSQL + Redis	未开始	❌ 待实现（P0）
AI集成	OpenAI兼容API	未集成	❌ 待实现（P0）
状态管理	Zustand + React Query	Zustand	⚠️ 部分实现
UI组件	Shadcn/ui	自定义组件	⚠️ 建议调整

📋 任务优先级分类
🔴 P0 - 阻塞性任务（必须立即完成）
1. 编辑器集成 (预计3-5天)
状态: ❌ 未开始
阻塞原因: 这是小说写作平台的核心功能，没有编辑器无法进行任何写作操作
子任务:
[ ] 安装 Novel 编辑器依赖 (novel, ai, @ai-sdk/openai)
[ ] 创建编辑器组件 (src/components/editor/NovelEditor.tsx)
[ ] 集成到 EditorView 页面
[ ] 实现自动保存功能（本地 + 服务端）
[ ] 添加字数统计和保存状态显示
[ ] 配置中文提示词
技术方案:
# 方案A: 使用 Tiptap（推荐）
npm install @tiptap/react @tiptap/starter-kit @tiptap/extension-placeholder

# 方案B: 使用 Novel（需要适配Vite）
npm install novel ai @ai-sdk/openai
# 注意：Novel 需要在 Vite 中进行额外配置
实施建议:
● ✅ 优先方案A（Tiptap）：更灵活，与React + Vite完美兼容
● ⚠️ 备选方案B（Novel）：功能更丰富，但需要适配工作
● 📌 快速迭代：先用Tiptap实现MVP，后续可评估是否需要Novel的高级功能

2. 后端基础架构搭建 (预计1周)
状态: ❌ 未开始
阻塞原因: 前端已有大量 DataService 调用，但后端完全缺失
子任务:
[ ] 创建 FastAPI 项目结构
[ ] 配置数据库 (PostgreSQL + SQLAlchemy)
[ ] 配置 Redis 缓存
[ ] 实现用户认证系统 (JWT)
[ ] 实现基础 CRUD API
    [ ] /api/auth/* - 登录/注册/登出
    [ ] /api/users/* - 用户管理
    [ ] /api/works/* - 作品管理
    [ ] /api/chapters/* - 章节管理
[ ] 配置 CORS 允许前端访问
[ ] Docker Compose 本地开发环境
目录结构:
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

3. AI 服务集成 (预计3-5天)
状态: ❌ 未开始
阻塞原因: AI 续写是核心卖点，但目前完全缺失
子任务:
[ ] 后端: 创建 OpenAI 服务类 (app/services/ai/openai_service.py)
[ ] 后端: 实现流式 AI 续写接口 (/api/v1/ai/complete)
[ ] 后端: 实现 AI 对话接口 (/api/v1/ai/chat)
[ ] 后端: Token 计数和成本追踪
[ ] 前端: 创建 AI 请求 Hook (src/hooks/useAI.ts)
[ ] 前端: 实现流式响应处理 (SSE)
[ ] 前端: EditorView 集成 AI 续写按钮
环境变量配置:
# 后端 .env
OPENAI_API_KEY={:LOCAL_API_KEY}
OPENAI_BASE_URL=https://204992.xyz/v1

# 前端 .env
VITE_API_URL=http://localhost:8000

🟡 P1 - 高优先级任务（核心功能）
4. 作品和章节管理完善 (预计1周)
状态: ⚠️ 部分完成（仅前端UI）
已完成:
● ✅ WorksView - 作品列表页面
● ✅ WorkDetailView - 作品详情页面
● ✅ EditorView - 编辑器页面
待完成:
[ ] 连接后端 API 替换 Mock 数据
[ ] 实现作品 CRUD 完整流程
    [ ] 创建作品（含封面上传）
    [ ] 编辑作品信息
    [ ] 删除作品（含确认弹窗）
    [ ] 作品归档/发布状态切换
[ ] 实现章节 CRUD 完整流程
    [ ] 创建章节
    [ ] 重命名章节
    [ ] 删除章节
    [ ] 章节排序（拖拽）
[ ] 实现卷（Volume）功能
    [ ] 创建卷
    [ ] 章节归类到卷
[ ] 作品统计数据实时更新
    [ ] 总字数
    [ ] 章节数
    [ ] 最后更新时间
技术细节:
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

5. 用户系统完善 (预计5天)
状态: ⚠️ 部分完成（仅前端UI）
已完成:
● ✅ LoginView - 登录页面
● ✅ RegisterView - 注册页面
● ✅ SettingsView - 设置页面
● ✅ Zustand authStore 状态管理
待完成:
[ ] 连接后端认证 API
    [ ] 登录接口
    [ ] 注册接口
    [ ] 登出接口
    [ ] Token 刷新机制
[ ] JWT Token 管理
    [ ] 存储到 localStorage
    [ ] 自动附加到请求头
    [ ] Token 过期处理
    [ ] 自动刷新 Token
[ ] 用户资料管理
    [ ] 修改用户名
    [ ] 修改邮箱
    [ ] 上传头像
    [ ] 修改简介
[ ] 密码管理
    [ ] 修改密码
    [ ] 忘记密码（邮件重置）
[ ] 第三方登录（可选）
    [ ] Google OAuth
    [ ] GitHub OAuth

6. 管理后台数据对接 (预计3天)
    状态: ⚠️ 部分完成（仅前端UI + Mock数据）
    已完成:
    ● ✅ AdminDashboardView - 数据面板 (Mock 数据)
    ● ✅ AdminUsersView - 用户管理 (Mock 数据)
    ● ✅ AdminAIModelsView - AI 模型管理 (Mock 数据)
    ● ✅ AdminCostView - 成本监控 (Mock 数据)
    ● ✅ AdminContentView - 内容审核 (Mock 数据)
    待完成:
    [ ] 连接后端管理 API
    [ ] /api/admin/dashboard - 仪表盘数据
    [ ] /api/admin/users - 用户管理
    [ ] /api/admin/ai-models - AI 模型配置
    [ ] /api/admin/cost - 成本统计
    [ ] /api/admin/content - 内容审核
    [ ] 实现管理员权限验证
    [ ] 实现用户管理功能
    [ ] 用户列表分页
    [ ] 用户封禁/解封
    [ ] 用户角色修改
    [ ] 用户搜索和筛选
    [ ] 实现 AI 模型配置管理
    [ ] 模型启用/禁用
    [ ] 模型参数配置
    [ ] 费率设置
    [ ] 实现内容审核功能
    [ ] 审核队列
    [ ] 批准/拒绝操作
    [ ] 审核日志

🟢 P2 - 中优先级任务（增强功能）
7. 世界观构建系统 (预计2周)
状态: ❌ 未开始
功能需求:
[ ] 创建世界观管理页面 (/worldbuilding/:workId)
[ ] 设定条目管理
    [ ] 角色设定 (Characters)
    [ ] 地点设定 (Locations)
    [ ] 势力设定 (Factions)
    [ ] 物品设定 (Items)
    [ ] 设定关系网络 (Relations)
[ ] AI 辅助生成设定
    [ ] 根据作品描述生成角色
    [ ] 根据情节生成地点
    [ ] 自动提取设定信息
[ ] 可视化展示
    [ ] 使用 ReactFlow 展示关系图
    [ ] 设定卡片视图
    [ ] 时间线视图
[ ] 在编辑器中引用设定
    [ ] @character 标记
    [ ] @location 标记
    [ ] 悬浮卡片显示详情
数据库设计:
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

8. 大纲生成功能 (预计1周)
状态: ❌ 未开始
功能需求:
[ ] 创建大纲页面 (/outline/:workId)
[ ] AI 生成大纲
    [ ] 根据作品简介生成整体大纲
    [ ] 根据章节标题生成详细大纲
    [ ] 支持多种大纲模板（三幕剧、起承转合等）
[ ] 大纲编辑
    [ ] 树形结构编辑
    [ ] 拖拽排序
    [ ] 折叠/展开
[ ] 大纲与章节关联
    [ ] 大纲节点转为章节
    [ ] 章节反向关联大纲
[ ] 大纲导出
    [ ] Markdown 格式
    [ ] 思维导图格式
AI Prompt 示例:
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

9. 提示词管理系统 (预计5天)
状态: ❌ 未开始
功能需求:
[ ] 创建提示词管理页面 (/prompts)
[ ] 提示词分类
    [ ] 系统预设提示词（续写、润色、扩写、缩写）
    [ ] 用户自定义提示词
    [ ] 作品专用提示词
[ ] 提示词编辑器
    [ ] 变量支持 ({context}, {style}, {length})
    [ ] 预览功能
    [ ] 版本管理
[ ] 提示词快捷使用
    [ ] 右键菜单集成
    [ ] 快捷键绑定
    [ ] 编辑器 Slash 命令 (/prompt)
数据结构:
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

10. 数据统计和可视化完善 (预计3天)
状态: ⚠️ 部分完成（仅前端UI）
已完成:
● ✅ AdminDashboardView 基础图表（用户增长、AI 调用统计）
● ✅ AdminCostView 成本图表（成本趋势、模型分布）
待完成:
[ ] 个人写作统计页面 (/stats)
    [ ] 每日字数统计（折线图）
    [ ] 写作热力图（类似 GitHub Contribution）
    [ ] 创作效率分析
    [ ] AI 使用统计
[ ] 作品统计页面
    [ ] 章节字数分布（柱状图）
    [ ] 创作时间轴
    [ ] 角色出场频率
    [ ] 关键词云图
[ ] 导出统计报告
    [ ] PDF 格式
    [ ] Excel 格式
技术方案:
● 使用现有 Recharts 库
● 新增 D3.js 用于复杂可视化（词云图、热力图）
● 后端提供聚合查询接口

🔵 P3 - 低优先级任务（优化和扩展）
11. 文件导入导出 (预计1周)
状态: ❌ 未开始
导入功能:
[ ] 支持导入格式
    [ ] TXT 文本
    [ ] Markdown
    [ ] DOCX (Word)
    [ ] EPUB
[ ] 智能章节分割
[ ] 格式保留和转换
导出功能:
[ ] 支持导出格式
    [ ] TXT
    [ ] Markdown
    [ ] DOCX
    [ ] EPUB
    [ ] PDF
[ ] 导出设置
    [ ] 选择章节范围
    [ ] 格式化选项
    [ ] 封面和版权页
[ ] 批量导出

12. 协作功能 (预计2周)
状态: ❌ 未开始
功能需求:
[ ] 作品分享
    [ ] 生成分享链接
    [ ] 权限控制（只读/评论/编辑）
    [ ] 链接过期时间
[ ] 实时协作编辑
    [ ] WebSocket 集成
    [ ] 操作同步（使用 Yjs）
    [ ] 光标位置显示
    [ ] 冲突解决
[ ] 评论系统
    [ ] 段落级评论
    [ ] 回复和讨论
    [ ] @提及用户
    [ ] 评论解决状态
技术栈:
● WebSocket (FastAPI WebSocket)
● Yjs (CRDT 协作算法)
● Tiptap Collaboration 扩展

13. 离线编辑支持 (预计3天)
状态: ❌ 未开始
功能需求:
[ ] PWA 配置
    [ ] Service Worker
    [ ] 离线缓存策略
    [ ] App Manifest
[ ] 本地存储
    [ ] IndexedDB 存储草稿
    [ ] 自动同步到服务器
    [ ] 冲突检测
[ ] 离线提示
    [ ] 网络状态检测
    [ ] 离线模式 UI 提示

14. 搜索功能 (预计5天)
状态: ❌ 未开始（Header 有搜索按钮但无功能）
功能需求:
[ ] 全局搜索
    [ ] 作品搜索
    [ ] 章节内容搜索
    [ ] 世界观设定搜索
[ ] 高级搜索
    [ ] 正则表达式支持
    [ ] 多条件筛选
    [ ] 搜索历史
[ ] 搜索结果
    [ ] 高亮显示
    [ ] 上下文预览
    [ ] 快速跳转
技术方案:
● 后端: PostgreSQL 全文搜索
● 前端: 搜索框组件 + 结果面板
-- PostgreSQL 全文搜索索引
CREATE INDEX idx_chapters_content_fts
ON chapters
USING gin(to_tsvector('chinese', content));

15. 通知系统 (预计3天)
状态: ❌ 未开始（Header 有通知按钮但无功能）
功能需求:
[ ] 通知类型
    [ ] 系统通知（维护、更新）
    [ ] 作品通知（评论、分享）
    [ ] AI 通知（任务完成、配额提醒）
[ ] 通知中心
    [ ] 未读/已读状态
    [ ] 批量操作（全部已读、清空）
    [ ] 通知分类和筛选
[ ] 通知设置
    [ ] 通知偏好设置
    [ ] 静默时段
    [ ] 邮件通知开关
技术方案:
● WebSocket 实时通知推送
● 邮件通知（使用 SendGrid 或阿里云邮件）

16. 主题和个性化 (预计2天)
状态: ⚠️ 部分完成（SettingsView 有主题设置但未实现）
已完成:
● ✅ SettingsView 主题选择器 UI
待完成:
[ ] 暗黑模式实现
    [ ] Tailwind Dark Mode 配置
    [ ] 全局主题切换
    [ ] 主题持久化（localStorage）
[ ] 编辑器主题
    [ ] 亮色主题
    [ ] 暗色主题
    [ ] 护眼模式
[ ] 字体和排版设置
    [ ] 字体大小
    [ ] 字体家族
    [ ] 行高
    [ ] 段落间距

17. 移动端适配 (预计1周)
    状态: ⚠️ 部分完成（使用 Tailwind 响应式但未充分测试）
    待完成:
    [ ] 响应式布局优化
    [ ] 侧边栏移动端适配（抽屉式）
    [ ] 编辑器移动端适配
    [ ] 表格移动端适配
    [ ] 触摸交互优化
    [ ] 滑动手势
    [ ] 长按菜单
    [ ] 双击缩放
    [ ] 性能优化
    [ ] 移动端代码分割
    [ ] 图片懒加载
    [ ] 虚拟滚动

🟣 P4 - 长期规划任务
18. 支付和订阅系统 (预计2周)
状态: ❌ 未开始
功能需求:
[ ] 订阅计划设计
    [ ] 免费版（基础功能）
    [ ] 专业版（增强功能 + 更多配额）
    [ ] 团队版（协作功能）
[ ] 支付集成
    [ ] 支付宝
    [ ] 微信支付
    [ ] Stripe（国际支付）
[ ] 订阅管理
    [ ] 升级/降级
    [ ] 续费提醒
    [ ] 发票管理
[ ] 配额管理
    [ ] AI 调用次数限制
    [ ] 存储空间限制
    [ ] 作品数量限制

19. 插件系统 (预计3周)
状态: ❌ 未开始
功能需求:
[ ] 插件架构设计
[ ] 插件 API 定义
[ ] 插件市场
[ ] 插件安装和管理
[ ] 示例插件
    [ ] 语法检查插件
    [ ] 敏感词检测插件
    [ ] 自定义 AI 模型插件

20. 性能优化和监控 (预计1周)
    状态: ❌ 未开始
    优化项:
    [ ] 前端性能优化
    [ ] 代码分割
    [ ] 懒加载
    [ ] 图片优化
    [ ] Bundle 体积分析
    [ ] 后端性能优化
    [ ] 数据库查询优化
    [ ] Redis 缓存策略
    [ ] API 响应时间优化
    [ ] 监控集成
    [ ] Sentry 错误追踪
    [ ] Prometheus + Grafana
    [ ] 性能指标监控

🛠️ 技术债务和重构任务
技术栈调整评估
问题1: 编辑器方案选择
现状: ✅ 前端技术栈已确定为 React + Vite
待决策: 选择 Tiptap 还是 Novel 编辑器
方案A - Tiptap（推荐）:
● ✅ 优势:
  ○ 与 React + Vite 完美兼容
  ○ 高度可定制，灵活性强
  ○ 社区活跃，文档完善
  ○ 不依赖特定框架
● ❌ 劣势:
  ○ 需要自己实现AI集成
  ○ UI需要自己设计
方案B - Novel:
● ✅ 优势:
  ○ AI功能开箱即用
  ○ Notion风格UI现成
  ○ 节省开发时间
● ❌ 劣势:
  ○ 需要适配Vite环境
  ○ 定制性相对较弱
最终决策: ✅ 优先使用 Tiptap，快速实现MVP功能

问题2: 自定义组件 vs Shadcn/ui
现状: 使用自定义组件 (Button, Input, Card 等)
计划: todo.md 建议使用 Shadcn/ui
评估:
● 当前自定义组件功能有限
● Shadcn/ui 提供更丰富的组件和一致性
● Shadcn/ui 基于 Radix UI，可访问性更好
建议: 逐步迁移到 Shadcn/ui
1. 保留现有组件（向后兼容）
2. 新功能使用 Shadcn/ui
3. 逐步替换旧组件

问题3: 缺少 React Query
现状: 仅使用 Zustand，缺少服务端状态管理
影响: 手动管理 API 请求、缓存、加载状态
建议: 引入 TanStack Query (React Query)
npm install @tanstack/react-query
示例用法:
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

代码规范和工具链

📐 一、前端代码规范

1.1 TypeScript 规范
类型定义:
● 优先使用 interface 定义对象类型
● 使用 type 定义联合类型和复杂类型
● 避免使用 any，必要时使用 unknown
● 所有组件 props 必须定义类型

示例:
// ✅ 推荐
interface UserProps {
  id: string;
  name: string;
  email: string;
  role?: 'admin' | 'user';
}

// ❌ 避免
const user: any = {...};

命名规范:
● Interface/Type: PascalCase，如 UserProfile
● 函数/变量: camelCase，如 getUserData
● 常量: UPPER_SNAKE_CASE，如 MAX_RETRY_COUNT
● 组件: PascalCase，如 UserCard.tsx
● 私有方法: 前缀 _，如 _handlePrivateMethod

1.2 React 组件规范
组件结构顺序:
1. import 语句
2. 类型定义
3. 组件定义
4. 子组件
5. 导出语句

示例:
// 1. Import
import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';

// 2. Types
interface UserCardProps {
  user: User;
  onEdit?: (id: string) => void;
}

// 3. Component
export function UserCard({ user, onEdit }: UserCardProps) {
  // Hooks 放在最前面
  const [isLoading, setIsLoading] = useState(false);

  // useEffect
  useEffect(() => {
    // ...
  }, []);

  // Event handlers
  const handleEdit = () => {
    onEdit?.(user.id);
  };

  // Render helpers
  const renderStatus = () => {
    return <span>{user.status}</span>;
  };

  // JSX
  return (
    <div>
      {/* ... */}
    </div>
  );
}

组件规范:
● 优先使用函数组件
● 使用 React Hooks 管理状态
● 大组件拆分成小组件（单一职责）
● 提取可复用逻辑到自定义 Hooks
● Props 解构放在参数位置
● 条件渲染使用三元运算符或 &&
● 列表渲染必须添加 key

自定义 Hooks 规范:
● 命名必须以 use 开头
● 返回值使用数组或对象
● 处理副作用和清理逻辑

示例:
// ✅ 推荐
function useUser(userId: string) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    let cancelled = false;
    
    const fetchUser = async () => {
      try {
        const data = await DataService.getUser(userId);
        if (!cancelled) {
          setUser(data);
        }
      } catch (err) {
        if (!cancelled) {
          setError(err as Error);
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    };
    
    fetchUser();
    
    return () => {
      cancelled = true;
    };
  }, [userId]);

  return { user, loading, error };
}

1.3 文件和目录命名
文件命名:
● 组件文件: PascalCase.tsx，如 UserCard.tsx
● Hooks: camelCase.ts，如 useAuth.ts
● 工具函数: camelCase.ts，如 formatDate.ts
● 类型文件: camelCase.types.ts，如 user.types.ts
● 常量文件: camelCase.constants.ts，如 api.constants.ts

目录结构:
src/
├── components/          # 组件
│   ├── ui/             # UI基础组件
│   ├── layout/         # 布局组件
│   └── features/       # 功能组件
├── hooks/              # 自定义Hooks
├── stores/             # 状态管理
├── services/           # API服务
├── utils/              # 工具函数
├── types/              # 类型定义
├── constants/          # 常量
├── styles/             # 样式文件
└── views/              # 页面视图

1.4 CSS/Tailwind 规范
Tailwind CSS 使用规范:
● 优先使用 Tailwind 类名
● 复杂样式抽取到 @apply 或组件
● 响应式优先（mobile-first）
● 使用 clsx 或 cn 工具函数合并类名

示例:
// ✅ 推荐
<div className={cn(
  "flex items-center gap-2 p-4",
  isActive && "bg-blue-500 text-white",
  className
)}>
  {children}
</div>

// ❌ 避免
<div className="flex items-center gap-2 p-4 bg-blue-500 text-white border border-gray-300 rounded-lg shadow-md hover:shadow-lg transition-all duration-300">

样式组织:
● 布局相关: flex, grid, block
● 尺寸相关: w-*, h-*, max-w-*
● 间距相关: p-*, m-*, gap-*
● 颜色相关: bg-*, text-*, border-*
● 其他: rounded-*, shadow-*, hover:*

1.5 注释规范
何时添加注释:
● ✅ 复杂的业务逻辑
● ✅ 非常规的解决方案（需要说明原因）
● ✅ 公共 API 和工具函数
● ✅ TODO/FIXME 标记
● ❌ 不要注释显而易见的代码

注释格式:
/**
 * 获取用户详细信息
 * @param userId - 用户ID
 * @returns 用户对象
 * @throws 当用户不存在时抛出错误
 */
 async function getUserDetails(userId: string): Promise<User> {
    // 实现...
 }

// TODO: 实现缓存机制
// FIXME: 修复并发请求问题
// HACK: 临时解决方案，等待上游修复
// NOTE: 这里使用了非常规方法，因为...

1.6 ESLint 配置
推荐规则:
{
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:react/recommended",
    "plugin:react-hooks/recommended",
    "prettier"
  ],
  "rules": {
    // TypeScript
    "@typescript-eslint/no-explicit-any": "error",
    "@typescript-eslint/explicit-function-return-type": "off",
    "@typescript-eslint/no-unused-vars": ["error", { 
      "argsIgnorePattern": "^_" 
    }],
    
    // React
    "react/react-in-jsx-scope": "off",
    "react/prop-types": "off",
    "react-hooks/rules-of-hooks": "error",
    "react-hooks/exhaustive-deps": "warn",
    
    // 通用
    "no-console": ["warn", { "allow": ["warn", "error"] }],
    "prefer-const": "error",
    "no-var": "error"
  }
}

1.7 Prettier 配置
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 80,
  "tabWidth": 2,
  "useTabs": false,
  "arrowParens": "always",
  "endOfLine": "lf"
}

📐 二、后端代码规范（Python/FastAPI）

2.1 Python 代码规范
基本规范:
● 遵循 PEP 8 规范
● 使用 4 个空格缩进
● 行长度限制 88 字符（Black 默认）
● 使用类型注解

命名规范:
● 类名: PascalCase，如 UserService
● 函数/方法: snake_case，如 get_user_by_id
● 变量: snake_case，如 user_count
● 常量: UPPER_SNAKE_CASE，如 MAX_RETRY_COUNT
● 私有属性/方法: 前缀 _，如 _internal_method

2.2 FastAPI 路由规范
目录结构:
app/
├── api/
│   └── v1/
│       ├── __init__.py
│       ├── auth.py          # 认证相关
│       ├── users.py         # 用户管理
│       ├── works.py         # 作品管理
│       └── ai.py            # AI服务
├── models/                  # 数据库模型
├── schemas/                 # Pydantic模型
├── services/                # 业务逻辑
├── core/                    # 核心配置
└── main.py

路由定义规范:
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.user_service import UserService
from app.core.auth import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

@router.get("", response_model=List[UserResponse])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends()
) -> List[UserResponse]:
    """
    获取用户列表
    
    - **skip**: 跳过的记录数（分页）
    - **limit**: 返回的最大记录数
    """
    users = await user_service.get_users(skip=skip, limit=limit)
    return users

@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    user_service: UserService = Depends()
) -> UserResponse:
    """创建新用户"""
    try:
        user = await user_service.create_user(user_data)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

2.3 数据模型规范
Pydantic Schema:
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

# 基础模型
class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    
# 创建时使用
class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    
# 更新时使用
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    
# 响应时使用
class UserResponse(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

SQLAlchemy Model:
from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

2.4 Service 层规范
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        """根据ID获取用户"""
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def get_users(
        self, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[User]:
        """获取用户列表"""
        result = await self.db.execute(
            select(User).offset(skip).limit(limit)
        )
        return result.scalars().all()
    
    async def create_user(self, user_data: UserCreate) -> User:
        """创建用户"""
        # 检查邮箱是否已存在
        existing = await self.get_user_by_email(user_data.email)
        if existing:
            raise ValueError("Email already registered")
        
        # 创建用户
        user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hash_password(user_data.password)
        )
        
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        
        return user

2.5 异常处理规范
自定义异常:
class AppException(Exception):
    """应用基础异常"""
    pass

class NotFoundError(AppException):
    """资源不存在"""
    pass

class ValidationError(AppException):
    """数据验证错误"""
    pass

class AuthenticationError(AppException):
    """认证失败"""
    pass

异常处理:
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(NotFoundError)
async def not_found_handler(request: Request, exc: NotFoundError):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)}
    )

@app.exception_handler(ValidationError)
async def validation_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )

2.6 Python 工具配置
Black (代码格式化):
# pyproject.toml
[tool.black]
line-length = 88
target-version = ['py311']
include = '\.pyi?$'

isort (导入排序):
[tool.isort]
profile = "black"
line_length = 88
multi_line_output = 3

Flake8 (代码检查):
# .flake8
[flake8]
max-line-length = 88
extend-ignore = E203, W503
exclude = .git,__pycache__,venv

mypy (类型检查):
# mypy.ini
[mypy]
python_version = 3.11
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True

📐 三、Git 提交规范

3.1 Commit Message 格式
格式:
<type>(<scope>): <subject>

<body>

<footer>

Type 类型:
● feat: 新功能
● fix: 修复bug
● docs: 文档更新
● style: 代码格式（不影响功能）
● refactor: 重构（不是新功能也不是修复bug）
● perf: 性能优化
● test: 添加测试
● chore: 构建过程或辅助工具的变动
● revert: 回滚到上一个版本

示例:
feat(editor): 添加AI续写功能

- 集成OpenAI API
- 实现流式响应处理
- 添加续写按钮到编辑器工具栏

Closes #123

fix(auth): 修复token刷新逻辑

当token过期时，自动刷新机制没有正确触发。
现在会在token过期前5分钟自动刷新。

Fixes #456

3.2 分支管理规范
分支命名:
● main - 主分支（生产环境）
● develop - 开发分支
● feature/xxx - 功能分支
● fix/xxx - 修复分支
● hotfix/xxx - 紧急修复
● release/xxx - 发布分支

示例:
feature/user-authentication
fix/editor-save-bug
hotfix/api-crash

工作流程:
1. 从 develop 创建 feature 分支
2. 开发完成后提交 PR 到 develop
3. Code Review 通过后合并
4. 定期从 develop 合并到 main

3.3 commitlint 配置
# .commitlintrc.js
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [
      2,
      'always',
      [
        'feat',
        'fix',
        'docs',
        'style',
        'refactor',
        'perf',
        'test',
        'chore',
        'revert'
      ]
    ],
    'subject-case': [0]
  }
};

📐 四、API 设计规范

4.1 RESTful API 规范
URL 设计:
● 使用名词复数形式
● 使用小写字母和连字符
● 版本号放在路径中

示例:
✅ GET    /api/v1/users
✅ GET    /api/v1/users/{id}
✅ POST   /api/v1/users
✅ PUT    /api/v1/users/{id}
✅ DELETE /api/v1/users/{id}
✅ GET    /api/v1/users/{id}/works

❌ GET /api/v1/getUsers
❌ POST /api/v1/user/create
❌ GET /api/v1/Users

HTTP 状态码:
● 200 OK - 成功
● 201 Created - 创建成功
● 204 No Content - 删除成功
● 400 Bad Request - 请求参数错误
● 401 Unauthorized - 未认证
● 403 Forbidden - 无权限
● 404 Not Found - 资源不存在
● 422 Unprocessable Entity - 验证失败
● 500 Internal Server Error - 服务器错误

4.2 响应格式规范
成功响应:
{
  "data": {
    "id": "123",
    "name": "John Doe"
  },
  "message": "Success"
}

列表响应:
{
  "data": [
    {"id": "1", "name": "Item 1"},
    {"id": "2", "name": "Item 2"}
  ],
  "pagination": {
    "total": 100,
    "page": 1,
    "pageSize": 10,
    "totalPages": 10
  }
}

错误响应:
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email format",
    "details": [
      {
        "field": "email",
        "message": "Email must be a valid email address"
      }
    ]
  }
}

4.3 请求参数规范
查询参数:
● page - 页码（从1开始）
● pageSize / limit - 每页数量
● sort - 排序字段
● order - 排序方向（asc/desc）
● search / q - 搜索关键词
● filter - 筛选条件

示例:
GET /api/v1/users?page=1&pageSize=20&sort=createdAt&order=desc&search=john

请求体:
● 使用 JSON 格式
● 使用 camelCase 命名
● 必填字段标注清楚

{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "secret123"
}

📐 五、测试规范

5.1 前端测试规范
测试文件命名:
● 组件测试: ComponentName.test.tsx
● Hook测试: hookName.test.ts
● 工具函数测试: functionName.test.ts

测试结构:
import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { UserCard } from './UserCard';

describe('UserCard', () => {
  const mockUser = {
    id: '1',
    name: 'John Doe',
    email: 'john@example.com'
  };

  it('renders user information correctly', () => {
    render(<UserCard user={mockUser} />);
    
    expect(screen.getByText('John Doe')).toBeInTheDocument();
    expect(screen.getByText('john@example.com')).toBeInTheDocument();
  });

  it('calls onEdit when edit button is clicked', () => {
    const handleEdit = vi.fn();
    render(<UserCard user={mockUser} onEdit={handleEdit} />);
    
    const editButton = screen.getByRole('button', { name: /edit/i });
    fireEvent.click(editButton);
    
    expect(handleEdit).toHaveBeenCalledWith('1');
  });
});

测试覆盖率目标:
● 核心功能: 80%+
● UI组件: 60%+
● 工具函数: 90%+

5.2 后端测试规范
测试文件命名:
● test_module_name.py

测试结构:
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
class TestUserAPI:
    async def test_create_user(self, client: AsyncClient):
        """测试创建用户"""
        response = await client.post(
            "/api/v1/users",
            json={
                "username": "johndoe",
                "email": "john@example.com",
                "password": "secret123"
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "johndoe"
        assert data["email"] == "john@example.com"
        assert "password" not in data
    
    async def test_create_user_duplicate_email(self, client: AsyncClient):
        """测试创建重复邮箱用户"""
        # 先创建一个用户
        await client.post("/api/v1/users", json={...})
        
        # 尝试创建相同邮箱的用户
        response = await client.post("/api/v1/users", json={...})
        
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"].lower()

测试覆盖率目标:
● API端点: 80%+
● Service层: 90%+
● 工具函数: 95%+

📐 六、文档规范

6.1 代码文档
组件文档:
/**
 * 用户卡片组件
 * 
 * 显示用户的基本信息，支持编辑和删除操作
 * 
 * @example
 * ```tsx
 * <UserCard 
 *   user={user} 
 *   onEdit={handleEdit}
 *   onDelete={handleDelete}
 * />
 * ```
 */
 export function UserCard({ user, onEdit, onDelete }: UserCardProps) {
    // ...
 }

API文档:
FastAPI 会自动生成文档，但需要添加详细描述：

@router.post("/users", response_model=UserResponse)
async def create_user(user_data: UserCreate) -> UserResponse:
    """
    创建新用户
    
    ## 请求体
    - **username**: 用户名（3-50字符）
    - **email**: 邮箱地址
    - **password**: 密码（至少8字符）
    
    ## 响应
    返回创建的用户信息（不包含密码）
    
    ## 错误
    - **400**: 邮箱已被注册
    - **422**: 请求参数验证失败
    """
    pass

6.2 README 文档规范
项目 README 应包含:
● 项目简介
● 技术栈
● 快速开始
● 环境变量配置
● 开发指南
● 部署指南
● 贡献指南
● 许可证

📋 开发工具清单

必须配置的工具:
[ ] 配置 ESLint 规则完善
[ ] 配置 Prettier
[ ] 配置 Husky + lint-staged (Git Hooks)
[ ] 配置 commitlint (规范 commit message)
[ ] 配置 Vitest (单元测试)
[ ] 配置 Playwright (E2E 测试)
[ ] 配置 Black (Python格式化)
[ ] 配置 isort (Python导入排序)
[ ] 配置 flake8 (Python代码检查)
[ ] 配置 mypy (Python类型检查)
[ ] 配置 pytest (Python测试)
[ ] 配置 pre-commit (Git pre-commit hooks)

推荐的 VS Code 插件:
● ESLint
● Prettier
● Tailwind CSS IntelliSense
● Python
● Pylance
● GitLens
● Auto Rename Tag
● Import Cost
● Error Lens

📋 代码审查清单

提交代码前检查:
[ ] 代码符合命名规范
[ ] 添加了必要的类型注解
[ ] 删除了 console.log 和调试代码
[ ] 添加了必要的注释
[ ] 通过了所有测试
[ ] 没有 ESLint/flake8 警告
[ ] Commit message 符合规范
[ ] 更新了相关文档

Code Review 重点:
[ ] 代码逻辑是否正确
[ ] 是否有性能问题
[ ] 是否有安全隐患
[ ] 错误处理是否完善
[ ] 测试覆盖是否充分
[ ] 代码可读性如何
[ ] 是否符合项目规范

📊 开发里程碑规划
Milestone 1: 核心编辑功能 (2-3周)
目标: 实现基本的写作和编辑功能
任务:
● ✅ 前端UI框架 (已完成)
[ ] 后端基础架构 (P0-2)
[ ] 编辑器集成 (P0-1)
[ ] AI 服务集成 (P0-3)
[ ] 作品和章节管理 (P1-4)
[ ] 用户系统完善 (P1-5)
交付物:
● 可用的编辑器
● 作品和章节 CRUD
● AI 续写基础功能
● 用户登录注册

Milestone 2: AI 增强功能 (2周)
目标: 完善 AI 辅助写作能力
任务:
[ ] 提示词管理系统 (P2-9)
[ ] 大纲生成功能 (P2-8)
[ ] AI 参数配置
[ ] Token 计费系统
[ ] 管理后台数据对接 (P1-6)
交付物:
● 多样化的 AI 写作工具
● 完整的成本追踪
● 管理后台正常运作

Milestone 3: 世界观和组织工具 (3周)
目标: 提供专业的创作辅助工具
任务:
[ ] 世界观构建系统 (P2-7)
[ ] 数据统计和可视化 (P2-10)
[ ] 搜索功能 (P3-14)
[ ] 文件导入导出 (P3-11)
交付物:
● 世界观管理功能
● 创作统计分析
● 全局搜索
● 文件导入导出

Milestone 4: 协作和优化 (2周)
目标: 提升用户体验和性能
任务:
[ ] 协作功能 (P3-12)
[ ] 离线编辑支持 (P3-13)
[ ] 通知系统 (P3-15)
[ ] 主题和个性化 (P3-16)
[ ] 移动端适配 (P3-17)
[ ] 性能优化 (P4-20)

Milestone 5: 商业化 (2周)
目标: 实现盈利能力
任务:
[ ] 支付和订阅系统 (P4-18)
[ ] 营销落地页
[ ] 用户增长功能
[ ] SEO 优化

🚀 快速启动建议
如果你只有1周时间
聚焦 MVP:
1. ✅ 保持现有 React + Vite（暂不迁移）
[ ] 完成后端基础架构（3天）
[ ] 集成简单文本编辑器（Tiptap，1天）
[ ] 连接前后端 API（2天）
[ ] 基本的 AI 续写（1天）
如果你有1个月时间
完成 Milestone 1 + 2:
[ ] 使用Tiptap集成编辑器（5天）
[ ] 完成核心编辑功能（3周）
[ ] 完成 AI 增强功能（1周）
如果你有3个月时间
完成 Milestone 1-4:
● 第1个月: 核心功能 + AI 功能
● 第2个月: 世界观工具 + 搜索导出
● 第3个月: 协作功能 + 优化

📝 备注说明
技术选型说明
1. 前端框架: ✅ 确定使用 React 19 + Vite
2. UI 组件: ⚠️ 建议从自定义组件迁移到 Shadcn/ui
3. 状态管理: ⚠️ 建议添加 TanStack Query（React Query）
4. 编辑器: ⚠️ 优先使用 Tiptap，备选 Novel
关键风险提示
⚠️ 编辑器待集成: 编辑器是核心功能，需要优先实现（P0）
⚠️ 后端缺失: 前端已有大量 DataService 调用，但后端完全缺失，需尽快搭建
⚠️ 服务端状态管理: 建议尽快集成 React Query，提升数据管理能力

📞 联系和反馈
如有任何问题或需要调整优先级，请及时沟通。

📚 参考资源
开源项目参考
1. MaliangAINovalWriter（马良AI写作）
    ● GitHub: https://github.com/Deng-m1/MaliangAINovalWriter
    ● 技术栈: Flutter Web + Spring Boot
    ● 可借鉴点:
    ○ 完整的SaaS架构设计
    ○ 世界观构建系统
    ○ 提示词管理（系统/用户/预设三层）
    ○ LLM可观测性（日志/统计/成本分析）
    ○ 多模型动态切换机制
2. Novel
    ● 官网: https://novel.sh
    ● GitHub: https://github.com/steven-tey/novel
    ● 技术栈: Tiptap + React
    ● 可借鉴点:
    ○ Notion风格的编辑器体验
    ○ AI自动补全集成
    ○ Slash命令系统
    ○ Bubble Menu（选中文本工具栏）
    ○ 无头架构设计（编辑器核心与UI分离）
3. novelWriter
● GitHub: https://github.com/vkbo/novelWriter
● 技术栈: Python + Qt
● 可借鉴点:
    ○ 纯文本存储方案（易于版本控制）
    ○ 文档树形组织结构
    ○ 元数据标记系统（@character, @location等）
    ○ 实时索引与交叉引用
    ○ 项目快照与版本管理
技术文档
前端相关
● React官方文档: https://react.dev
● Vite文档: https://vitejs.dev
● Tiptap文档: https://tiptap.dev
● Novel文档: https://novel.sh
● Tailwind CSS: https://tailwindcss.com
● Shadcn/ui: https://ui.shadcn.com
● TanStack Query: https://tanstack.com/query
● Zustand: https://github.com/pmndrs/zustand
后端相关
● FastAPI文档: https://fastapi.tiangolo.com
● SQLAlchemy: https://www.sqlalchemy.org
● PostgreSQL文档: https://www.postgresql.org/docs
● Redis文档: https://redis.io/docs
● LangChain文档: https://python.langchain.com
● OpenAI API: https://platform.openai.com/docs
AI相关
● Vercel AI SDK: https://sdk.vercel.ai/docs
● OpenAI Cookbook: https://github.com/openai/openai-cookbook
● Prompt Engineering Guide: https://www.promptingguide.ai
学习资源
视频教程
● Tiptap入门: YouTube搜索 "Tiptap Tutorial"
● FastAPI教程: FastAPI官方教程
● LangChain实战: LangChain官方文档
博客文章
● 如何构建AI写作工具: 搜索相关技术博客
● Novel编辑器深度解析: Novel GitHub讨论区
● 小说写作平台架构设计: 各大技术社区
社区与支持
开发者社区
● GitHub Discussions: 各项目的讨论区
● Discord: Tiptap、FastAPI官方Discord
● Stack Overflow: 技术问题求助
中文社区
● 掘金: 搜索相关技术文章
● V2EX: 技术讨论
● 知乎: AI应用开发相关话题

📋 文档更新日志
v2.1 (2025-01-15)
● 🎉 整合v1.2技术栈规划与v2.0任务清单
● ✅ 新增完整的技术栈详细说明
● ✅ 新增团队简介部分
● ✅ 新增参考资源章节
● ✅ 优化文档结构，添加导航目录
● ✅ 统一格式和排版
v2.0 (2025-01-10)
● 📊 基于当前项目实际情况的任务清单
● 🎯 明确当前实现与原计划的差异
● 📋 按优先级划分任务（P0-P3）
● 🗓️ 制定详细的里程碑规划
v1.2 (2025-01-05)
● ⚙️ 完整的技术栈选型说明
● 👥 团队简介与协作流程
● 🔧 详细的AI配置指南
● 📚 开发工具链和基础设施规划

📊 项目信息
● 项目名称: NovelAIde
● 创建时间: 2025-01-05
● 当前版本: v2.1 (整合版)
● 最后更新: 2025-01-15
● 项目状态: 🚧 开发中 - 前端基础完成，后端进行中
● 技术栈: React 19 + Vite + FastAPI + PostgreSQL
● 团队规模: 建议2-3人起步（MVP阶段）
● 编辑器方案: Tiptap（优先）/ Novel（备选） ⭐
● AI方案: 第三方OpenAI兼容API (https://204992.xyz) ⭐
● 预计MVP: 2025年Q1（3个月）

🎯 下一步行动
立即要做的事（本周）
[ ] 搭建后端基础架构（FastAPI + PostgreSQL）
[ ] 集成Tiptap编辑器
[ ] 实现AI服务基础接口
[ ] 完成用户认证系统
近期目标（本月）
1. 完成P0任务（编辑器、后端、AI集成）
2. 完成P1任务（作品管理、用户系统）
3. 前后端联调测试
4. 完成Milestone 1
中期目标（3个月）
1. 完成核心功能开发（Milestone 1-3）
2. 内部测试和优化
3. 准备上线MVP版本
4. 开始用户推广

祝开发顺利！如有问题，请随时联系团队成员。 🚀
