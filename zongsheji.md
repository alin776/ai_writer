任务目标：构建一个功能完整、架构优美的AI辅助小说平台前端原型
该原型需使用React配合TypeScript实现，所有数据交互必须使用Mock Data，但要求设计模式（尤其是数据层和组件层）必须预留出极度便利的接口替换能力，确保未来能够无缝统一替换为真实的API调用。

一、 技术栈与架构要求 (Expert-Level Foundation)
核心技术栈： React 18+ (Hooks, Context/Zustand/Redux-Toolkit for State Management), TypeScript (强制类型校验), Tailwind CSS (或类似原子化CSS框架，提供高度定制性)。

数据/状态管理：

数据抽象层（关键）： 引入一个数据服务层（DataService 或 ApiLayer），所有组件不直接调用 Mock Data。组件只调用 DataService 中的抽象方法（如 DataService.fetchChapterContent(id)）。

Mock 机制： 在 DataService 内部实现一个开关或环境判断，使其在原型阶段指向 MockAdapter，在生产阶段指向 RealApiAdapter。

状态管理： 采用分层状态管理。全局状态（如用户权限、平台设置）使用 Context API 或轻量级库（如Zustand）。组件局部状态使用 useState。

路由： React Router DOM (v6+)。

编码规范： 遵循现代React最佳实践，组件拆分合理，高阶组件/Hooks抽象逻辑，代码注释清晰详尽。

二、 核心功能模块与组件细节 (Detailed Specification)
要求实现以下六大核心视图（Views）和一个共享组件库（Shared Components）：

1. 写作编辑器视图 (/editor/:workId/:chapterId)
模块	核心功能	界面要求	交互/数据点 (Mock)
主编辑区	类似 Notion 的无缝富文本编辑器（只要求外观和基础输入/选中文本功能，不需要完整的富文本逻辑）。	居中、宽敞、极简设计，专注内容。	chapterContent: string (Markdown/HTML 模拟), lastSaveTime: string。
AI 辅助侧边栏	AI续写 (按钮/快捷键)、AI润色 (选择文本后显示)、AI摘要/分析 (点击生成)。	可收起/展开。提供输入框让用户调整续写/生成要求。	aiSuggestions: string[] (续写结果列表), aiConfig: {tone: string, length: number}。
世界观/设定区	实时关联：显示当前章节内提及的关键人物、地点、道具等（从 WorldData 中筛选）。	悬浮或右侧固定面板，点击可查看/编辑详情。	relatedCharacters: Character[], relatedLocations: Location[]。
顶部工具栏	保存、撤销/重做、章节设置、返回作品列表。		

导出到 Google 表格
2. 作品管理列表视图 (/works)
模块	核心功能	界面要求	交互/数据点 (Mock)
作品列表	卡片/列表展示：作品名、简介、总字数、最新更新时间、AI模型、操作（进入编辑、设置、删除）。	支持按更新时间、字数排序、搜索作品。	works: Work[] (包含 id, title, description, totalWords, updateTime, aiModelUsed, status 等)。
新建作品	Modal/侧边栏表单：输入作品名、简介、选择初始AI模型（模拟）。		

3. 作品详情/章节管理视图 (/works/:workId)
模块	核心功能	界面要求	交互/数据点 (Mock)
作品信息	展示作品摘要、当前使用模型、总成本（模拟）。		workDetails: Work。
章节树/列表	树形结构：支持拖拽排序（模拟）、新增章节、进入编辑。	清晰的层级结构，显示每章字数、状态（草稿/已发布）。	chapters: Chapter[] (包含 id, title, wordCount, status, order 等)。
世界观管理	Tab或区域：管理该作品下的人物、地点、设定。CRUD操作。		worldData: WorldData (包含 characters: Character[], locations: Location[] 等)。

4. 后台管理/模型配置视图 (/admin/settings)
模块	核心功能	界面要求	交互/数据点 (Mock)
模型/API 管理	表格：展示可用的 AI 模型（如 GPT-4o, Claude 3），模型名称、API Key（脱敏显示）、调用限额、状态。	提供新增/编辑/删除模型配置的表单。	models: AIModel[] (包含 id, name, type, apiKey, usageLimit, status 等)。
成本/调用监控	仪表盘：模拟显示平台总调用次数、总花费（美元/人民币），及趋势图（近7天/30天）。	简洁的数据可视化组件（如柱状图/折线图，使用 Echarts/Recharts 模拟数据）。	costMetrics: CostMetric[]。

5. 用户/权限管理视图 (/admin/users)
模块	核心功能	界面要求	交互/数据点 (Mock)
用户列表	表格：用户ID、用户名、邮箱、角色（管理员/普通用户）、注册时间、操作（禁用/修改角色）。	支持搜索、分页。	users: User[] (包含 id, name, email, role, registrationDate 等)。
权限配置	简单模拟：不同角色（如付费用户）可以配置不同的每日AI调用额度。		

6. 登录/注册视图 (/login, /register)
模块	核心功能	界面要求	交互/数据点 (Mock)
表单	标准表单：用户名/邮箱、密码、登录/注册按钮。	简洁、专业的全屏居中设计。	登录/注册成功后，Mock返回一个JWT Token和用户信息。

三、 数据结构与 Mock 策略 (API-Ready Design)
要求在 /src/mock 目录下创建以下TypeScript 接口 (Interfaces)和Mock 数据文件：

TypeScript 接口定义 (types.ts)： 严格定义所有核心数据结构，确保强类型化。

interface Work { id: string; title: string; description: string; ... }

interface Chapter { id: string; workId: string; title: string; content: string; ... }

interface Character { id: string; name: string; description: string; ... }

interface AIModel { id: string; name: string; ... }

interface User { id: string; name: string; role: 'admin' | 'user'; ... }

Mock 数据抽象层 (DataService.ts)：

所有数据请求必须通过该层，禁止组件直接导入 Mock JSON。

提供类似 Axios 的异步方法签名，例如：

TypeScript

// DataService.ts
async function getWorks(): Promise<Work[]> {
    // 模拟 API 延迟
    await new Promise(resolve => setTimeout(resolve, 500));
    // 调用 MockAdapter
    return MockAdapter.get('/works');
}
async function saveChapter(chapter: Chapter): Promise<Chapter> { ... }
MockAdapter： 负责返回静态 JSON 数据或基于请求参数（如 ID）进行简单的 CRUD 模拟。

四、 资深专家视角总结与交付标准
架构前瞻性： 整个项目必须体现关注分离 (Separation of Concerns, SoC) 原则。视图 (Views) -> 容器组件 (Containers) -> 展示组件 (Components) -> 数据服务层 (DataService) 的层次必须清晰。

可替换性保障： 必须以代码或清晰的注释明确指出未来将 DataService 内部的 MockAdapter 替换为 RealApiAdapter（如使用 fetch 或 axios）的步骤。

用户体验 (UX)： 界面设计需保持专业、干净、高效的风格，符合现代SaaS应用标准。核心操作（如保存、AI调用）应有清晰的加载状态（Loading State）模拟。

交付物： 提供完整的项目结构、配置文件（tsconfig.json 等）、所有核心视图和组件的代码。