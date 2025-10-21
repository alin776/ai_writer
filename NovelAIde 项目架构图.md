# NovelAIde 项目架构图

> **更新时间**: 2025-10-21 (最新更新)  
> **当前状态**: ✅ Milestone 1 完成，Milestone 2 进行中  
> **整体完成度**: 约 **85%**  
> - ✅ 后端核心: 95%（用户、作品、章节、世界观、AI服务已完成）
> - ✅ 前端核心: 90%（编辑器、世界观、导入导出、搜索已完成）
> - ✅ AI服务: 95%（前后端完整实现，5种AI功能）
> - ✅ 世界观系统: 95%（数据模型+API+关系图可视化已完成）
> - ✅ 小说分析: 100%（微观+宏观分析+向量存储）
> - ✅ 导入导出: 100%（JSON/Markdown支持）
> - ✅ 全局搜索: 100%（5种类型搜索）

## 图例说明
- 🟢 **绿色**: 已完成（90%以上）
- 🟡 **黄色**: 进行中（30-90%）
- 🔴 **红色**: 未开始（0-30%）

## 📐 完整架构总览（当前实现状态）

```mermaid
graph TB
    subgraph "客户端层"
        Browser[浏览器]
        Mobile[移动端 PWA]
    end

    subgraph "前端层 - React 19 + Vite ✅ 90%"
        UI[🟢 UI 组件层<br/>核心完成90%]
        Editor[🟢 编辑器 Tiptap 3.7.0<br/>已完成90%]
        State[🟢 状态管理 Zustand<br/>已完成100%]
        API_Client[🟢 API 客户端<br/>已完整对接95%]
        Router[🟢 路由 React Router v7<br/>已完成100%]
    end

    subgraph "网关层 ⚠️ 未部署"
        NGINX[🔴 Nginx 反向代理<br/>未配置 0%]
        CORS[🟢 CORS 中间件<br/>FastAPI已配置 100%]
    end

    subgraph "后端层 - FastAPI ✅ 95%"
        Auth[🟢 认证模块<br/>JWT已完成 100%]
        Works[🟢 作品管理<br/>CRUD已完成 100%]
        Chapters[🟢 章节管理<br/>CRUD+排序 100%]
        AI_Service[🟢 AI 服务<br/>5种功能已实现 95%]
        WorldView[🟢 世界观系统<br/>15个API已完成 95%]
        Analysis[🟢 小说分析<br/>微观+宏观 100%]
        Search[🟢 全局搜索<br/>5种类型 100%]
        Export[🟢 导入导出<br/>JSON/Markdown 100%]
        Prompt[🟡 提示词管理<br/>JSON配置 60%]
    end

    subgraph "数据层"
        PostgreSQL[🟢 PostgreSQL 数据库<br/>核心表已完成 90%]
        Redis[🟡 Redis 缓存<br/>已配置未使用 30%]
        OSS[🔴 阿里云 OSS<br/>未配置 0%]
    end

    subgraph "第三方服务"
        OpenAI[🟢 OpenAI API<br/>https://204992.xyz<br/>已完整集成 95%]
        CDN[🔴 CDN 加速<br/>未配置 0%]
    end

    Browser --> UI
    Mobile --> UI
    UI --> Editor
    UI --> State
    State --> API_Client
    Router --> UI
    
    API_Client --> NGINX
    NGINX --> CORS
    CORS --> Auth
    CORS --> Works
    CORS --> Chapters
    CORS --> AI_Service
    CORS --> WorldView
    CORS --> Prompt
    
    Auth --> PostgreSQL
    Works --> PostgreSQL
    Chapters --> PostgreSQL
    AI_Service --> Redis
    AI_Service --> OpenAI
    WorldView --> PostgreSQL
    Prompt --> PostgreSQL
    
    Works --> OSS
    Editor --> CDN
    
    style Browser fill:#e1f5ff
    style Mobile fill:#e1f5ff
    style Editor fill:#c8e6c9
    style State fill:#c8e6c9
    style Router fill:#c8e6c9
    style Auth fill:#c8e6c9
    style Works fill:#c8e6c9
    style Chapters fill:#c8e6c9
    style PostgreSQL fill:#c8e6c9
    style CORS fill:#c8e6c9
    style UI fill:#c8e6c9
    style API_Client fill:#c8e6c9
    style Redis fill:#fff3e0
    style AI_Service fill:#c8e6c9
    style WorldView fill:#c8e6c9
    style Analysis fill:#c8e6c9
    style Search fill:#c8e6c9
    style Export fill:#c8e6c9
    style Prompt fill:#fff3e0
    style OpenAI fill:#c8e6c9
    style OSS fill:#ffcdd2
    style CDN fill:#ffcdd2
    style NGINX fill:#ffcdd2
```

---

## 🏗️ 系统分层架构

```mermaid
graph LR
    subgraph "表现层 Presentation"
        Views[页面视图]
        Components[UI 组件]
        Hooks[自定义 Hooks]
    end

    subgraph "业务逻辑层 Business Logic"
        Services[业务服务]
        Store[状态管理]
        Validators[数据验证]
    end

    subgraph "数据访问层 Data Access"
        API[API 层]
        Models[数据模型]
        Schemas[Schema 验证]
    end

    subgraph "基础设施层 Infrastructure"
        Database[数据库 ORM]
        Cache[缓存服务]
        Auth_Core[认证授权]
        Logger[日志系统]
    end

    Views --> Components
    Components --> Hooks
    Hooks --> Services
    Services --> Store
    Store --> API
    API --> Models
    Models --> Schemas
    Schemas --> Database
    Services --> Cache
    API --> Auth_Core
    Database --> Logger

    style Views fill:#e3f2fd
    style Services fill:#fff3e0
    style API fill:#f3e5f5
    style Database fill:#c8e6c9
```

---

## 🎨 前端架构详解

```mermaid
graph TB
    subgraph "页面层 Pages"
        Login[登录页]
        Dashboard[仪表盘]
        Works_Page[作品列表]
        Editor_Page[编辑器页]
        WorldView_Page[世界观页]
        Settings[设置页]
    end

    subgraph "组件层 Components"
        Layout[布局组件]
        WorkCard[作品卡片]
        ChapterList[章节列表]
        EditorToolbar[编辑工具栏]
        AIPanel[AI 面板]
        CharacterCard[角色卡片]
    end

    subgraph "状态管理 Zustand"
        AuthStore[用户状态]
        WorkStore[作品状态]
        EditorStore[编辑器状态]
        UIStore[UI 状态]
    end

    subgraph "服务层 Services"
        DataService[数据服务]
        AIService[AI 服务]
        StorageService[本地存储]
    end

    subgraph "工具层 Utils"
        HTTP[HTTP 客户端]
        Formatter[格式化工具]
        Validator[验证工具]
    end

    Login --> Layout
    Dashboard --> Layout
    Works_Page --> WorkCard
    Editor_Page --> EditorToolbar
    Editor_Page --> ChapterList
    Editor_Page --> AIPanel
    WorldView_Page --> CharacterCard

    WorkCard --> WorkStore
    ChapterList --> WorkStore
    EditorToolbar --> EditorStore
    AIPanel --> EditorStore
    
    AuthStore --> DataService
    WorkStore --> DataService
    EditorStore --> AIService
    
    DataService --> HTTP
    AIService --> HTTP
    StorageService --> Validator

    style Login fill:#e3f2fd
    style Dashboard fill:#e3f2fd
    style AuthStore fill:#fff3e0
    style DataService fill:#f3e5f5
    style HTTP fill:#c8e6c9
```

---

## ⚙️ 后端架构详解

```mermaid
graph TB
    subgraph "API 路由层"
        Auth_Router["POST /api/v1/auth"]
        User_Router["GET /api/v1/users"]
        Work_Router["CRUD /api/v1/works"]
        Chapter_Router["CRUD /api/v1/chapters"]
        AI_Router["POST /api/v1/ai"]
        WorldView_Router["CRUD /api/v1/worldview"]
    end

    subgraph "中间件层"
        JWT_Middleware[JWT 认证]
        CORS_Middleware[CORS]
        Logger_Middleware[日志记录]
        Error_Handler[异常处理]
    end

    subgraph "服务层 Services"
        UserService[用户服务]
        WorkService[作品服务]
        ChapterService[章节服务]
        AIService_Backend[AI 服务]
        WorldViewService[世界观服务]
    end

    subgraph "数据模型层 Models"
        User_Model[User]
        Work_Model[Work]
        Chapter_Model[Chapter]
        Character_Model[Character]
        Setting_Model[Setting]
    end

    subgraph "数据库层"
        SQLAlchemy[SQLAlchemy ORM]
        AsyncPG[AsyncPG 驱动]
        PostgreSQL_DB[(PostgreSQL)]
    end

    Auth_Router --> JWT_Middleware
    User_Router --> JWT_Middleware
    Work_Router --> JWT_Middleware
    Chapter_Router --> JWT_Middleware
    AI_Router --> JWT_Middleware
    WorldView_Router --> JWT_Middleware

    JWT_Middleware --> CORS_Middleware
    CORS_Middleware --> Logger_Middleware
    Logger_Middleware --> Error_Handler

    Auth_Router --> UserService
    User_Router --> UserService
    Work_Router --> WorkService
    Chapter_Router --> ChapterService
    AI_Router --> AIService_Backend
    WorldView_Router --> WorldViewService

    UserService --> User_Model
    WorkService --> Work_Model
    ChapterService --> Chapter_Model
    WorldViewService --> Character_Model
    WorldViewService --> Setting_Model

    User_Model --> SQLAlchemy
    Work_Model --> SQLAlchemy
    Chapter_Model --> SQLAlchemy
    Character_Model --> SQLAlchemy
    Setting_Model --> SQLAlchemy

    SQLAlchemy --> AsyncPG
    AsyncPG --> PostgreSQL_DB

    style Auth_Router fill:#e3f2fd
    style JWT_Middleware fill:#fff3e0
    style UserService fill:#f3e5f5
    style User_Model fill:#c8e6c9
    style PostgreSQL_DB fill:#ffcdd2
```

---

## 🗄️ 数据库 ER 图 (更新日期: 2025-10-21)

> **已实现**: USERS ✅, WORKS ✅, CHAPTERS ✅, CHARACTERS ✅, LOCATIONS ✅, SETTINGS ✅, WORK_GUIDELINES ✅, AI_GUIDELINES ✅, NOVEL_ANALYSIS ✅, NOVEL_ANALYSIS_VECTOR ✅  
> **部分实现**: SETTING_RELATIONS 🟡 (字段已有，UI待完善)  
> **未实现**: FACTIONS ❌, PROMPTS ❌, AI_REQUESTS ❌ (待Milestone 2实现)

```mermaid
erDiagram
    USERS ||--o{ WORKS : creates
    USERS ||--o{ PROMPTS : creates
    USERS {
        uuid id PK
        string username UK
        string email UK
        string hashed_password
        boolean is_active
        string role
        datetime created_at
        datetime updated_at
    }

    WORKS ||--o{ CHAPTERS : contains
    WORKS ||--o{ CHARACTERS : has
    WORKS ||--o{ LOCATIONS : has
    WORKS ||--o{ FACTIONS : has
    WORKS {
        uuid id PK
        uuid author_id FK
        string title
        text description
        string genre
        string status
        int total_words
        int total_chapters
        datetime created_at
        datetime updated_at
    }

    CHAPTERS {
        uuid id PK
        uuid work_id FK
        string title
        text content
        int order
        int word_count
        boolean is_published
        datetime created_at
        datetime updated_at
    }

    CHARACTERS {
        uuid id PK
        uuid work_id FK
        string name
        text description
        json attributes
        string avatar
        datetime created_at
    }

    LOCATIONS {
        uuid id PK
        uuid work_id FK
        string name
        text description
        json attributes
        datetime created_at
    }

    FACTIONS {
        uuid id PK
        uuid work_id FK
        string name
        text description
        json attributes
        datetime created_at
    }

    SETTING_RELATIONS {
        uuid id PK
        uuid from_setting_id FK
        uuid to_setting_id FK
        string relation_type
        text description
    }

    CHARACTERS ||--o{ SETTING_RELATIONS : "from_character"
    SETTING_RELATIONS }o--|| CHARACTERS : "to_character"

    PROMPTS {
        uuid id PK
        uuid user_id FK
        string name
        text content
        string category
        boolean is_public
        int usage_count
        datetime created_at
    }

    AI_REQUESTS {
        uuid id PK
        uuid user_id FK
        string model
        text prompt
        text response
        int tokens_used
        float cost
        datetime created_at
    }

    USERS ||--o{ AI_REQUESTS : makes
```

---

## 🔄 核心业务流程图

### 用户写作流程

```mermaid
sequenceDiagram
    actor User as 用户
    participant UI as 前端界面
    participant Auth as 认证服务
    participant Work as 作品服务
    participant Chapter as 章节服务
    participant AI as AI 服务
    participant DB as 数据库

    User->>UI: 1. 打开编辑器
    UI->>Auth: 2. 验证 Token
    Auth-->>UI: 3. Token 有效
    
    User->>UI: 4. 创建新作品
    UI->>Work: 5. POST /api/v1/works
    Work->>DB: 6. 插入作品数据
    DB-->>Work: 7. 返回作品 ID
    Work-->>UI: 8. 作品创建成功
    
    User->>UI: 9. 创建章节
    UI->>Chapter: 10. POST /api/v1/chapters
    Chapter->>DB: 11. 插入章节数据
    DB-->>Chapter: 12. 返回章节 ID
    Chapter-->>UI: 13. 章节创建成功
    
    User->>UI: 14. 开始写作
    User->>UI: 15. 请求 AI 续写
    UI->>AI: 16. POST /api/v1/ai/complete
    AI->>OpenAI: 17. 调用 OpenAI API
    OpenAI-->>AI: 18. 流式返回内容
    AI-->>UI: 19. 实时推送内容 (SSE)
    UI-->>User: 20. 显示 AI 续写
    
    User->>UI: 21. 保存章节
    UI->>Chapter: 22. PUT /api/v1/chapters/{id}
    Chapter->>DB: 23. 更新章节内容
    Chapter->>Work: 24. 更新作品统计
    Work->>DB: 25. 更新字数统计
    DB-->>Chapter: 26. 保存成功
    Chapter-->>UI: 27. 保存成功提示
```

---

## 🤖 AI 服务流程

```mermaid
flowchart TD
    Start([用户请求 AI 续写]) --> CheckAuth{验证用户身份}
    CheckAuth -->|失败| Unauthorized[返回 401 未授权]
    CheckAuth -->|成功| CheckQuota{检查配额}
    
    CheckQuota -->|超额| QuotaExceeded[返回配额不足]
    CheckQuota -->|充足| GetContext[获取上下文]
    
    GetContext --> BuildPrompt[构建提示词]
    BuildPrompt --> SelectModel{选择 AI 模型}
    
    SelectModel --> GPT4[GPT-4]
    SelectModel --> GPT35[GPT-3.5-Turbo]
    
    GPT4 --> CallAPI[调用 OpenAI API]
    GPT35 --> CallAPI
    
    CallAPI --> Stream{流式响应?}
    Stream -->|是| SSE[Server-Sent Events]
    Stream -->|否| JSON[JSON 响应]
    
    SSE --> LogRequest[记录请求日志]
    JSON --> LogRequest
    
    LogRequest --> UpdateQuota[更新用户配额]
    UpdateQuota --> Cache[缓存结果]
    Cache --> End([返回结果])
    
    style Start fill:#e3f2fd
    style CheckAuth fill:#fff3e0
    style CallAPI fill:#f3e5f5
    style LogRequest fill:#c8e6c9
    style End fill:#e3f2fd
```

---

## 📡 API 接口架构

```mermaid
graph TB
    subgraph "认证接口"
        A1["POST /auth/register<br/>用户注册"]
        A2["POST /auth/login<br/>用户登录"]
        A3["POST /auth/refresh<br/>刷新 Token"]
        A4["POST /auth/logout<br/>用户登出"]
    end

    subgraph "用户接口"
        U1["GET /users/me<br/>获取当前用户"]
        U2["PUT /users/me<br/>更新用户信息"]
        U3["GET /users/:id<br/>获取用户详情"]
    end

    subgraph "作品接口"
        W1["GET /works<br/>获取作品列表"]
        W2["GET /works/:id<br/>获取作品详情"]
        W3["POST /works<br/>创建作品"]
        W4["PUT /works/:id<br/>更新作品"]
        W5["DELETE /works/:id<br/>删除作品"]
    end

    subgraph "章节接口"
        C1["GET /chapters/work/:id<br/>获取章节列表"]
        C2["GET /chapters/:id<br/>获取章节详情"]
        C3["POST /chapters<br/>创建章节"]
        C4["PUT /chapters/:id<br/>更新章节"]
        C5["DELETE /chapters/:id<br/>删除章节"]
        C6["POST /chapters/reorder<br/>章节排序"]
    end

    subgraph "AI 接口"
        AI1["POST /ai/complete<br/>AI 续写"]
        AI2["POST /ai/chat<br/>AI 对话"]
        AI3["POST /ai/outline<br/>生成大纲"]
        AI4["POST /ai/polish<br/>内容润色"]
    end

    subgraph "世界观接口"
        WV1["GET /worldview/:workId<br/>获取世界观"]
        WV2["POST /worldview/character<br/>创建角色"]
        WV3["POST /worldview/location<br/>创建地点"]
        WV4["POST /worldview/faction<br/>创建势力"]
        WV5["GET /worldview/relations<br/>关系网络"]
    end

    subgraph "提示词接口"
        P1["GET /prompts<br/>获取提示词列表"]
        P2["POST /prompts<br/>创建提示词"]
        P3["PUT /prompts/:id<br/>更新提示词"]
        P4["DELETE /prompts/:id<br/>删除提示词"]
    end

    style A1 fill:#e3f2fd
    style A2 fill:#e3f2fd
    style W3 fill:#fff3e0
    style C3 fill:#fff3e0
    style AI1 fill:#f3e5f5
    style WV2 fill:#c8e6c9
```

---

## 🔐 认证授权流程

```mermaid
sequenceDiagram
    participant Client as 客户端
    participant API as API 服务器
    participant Auth as 认证服务
    participant DB as 数据库
    participant Redis as Redis 缓存

    Note over Client,Redis: 用户登录流程
    Client->>API: POST /auth/login (username, password)
    API->>Auth: 验证用户凭证
    Auth->>DB: 查询用户信息
    DB-->>Auth: 返回用户数据
    Auth->>Auth: 验证密码 (bcrypt)
    Auth->>Auth: 生成 JWT Token
    Auth->>Redis: 存储 Token (TTL 24h)
    Auth-->>API: 返回 Token
    API-->>Client: 200 OK {access_token, refresh_token}

    Note over Client,Redis: 访问受保护资源
    Client->>API: GET /works (Authorization Bearer)
    API->>Auth: 验证 Token
    Auth->>Redis: 检查 Token 是否存在
    Redis-->>Auth: Token 有效
    Auth->>Auth: 解析 Token 获取 user_id
    Auth->>DB: 查询用户信息
    DB-->>Auth: 返回用户数据
    Auth-->>API: 用户已认证
    API->>DB: 查询作品列表
    DB-->>API: 返回数据
    API-->>Client: 200 OK + 作品数据

    Note over Client,Redis: Token 刷新流程
    Client->>API: POST /auth/refresh {refresh_token}
    API->>Auth: 验证 Refresh Token
    Auth->>Redis: 检查 Refresh Token
    Redis-->>Auth: Token 有效
    Auth->>Auth: 生成新的 Access Token
    Auth->>Redis: 存储新 Token
    Auth-->>API: 返回新 Token
    API-->>Client: 200 OK {new_access_token}
```

---

## 📦 部署架构

```mermaid
graph TB
    subgraph "客户端"
        Browser[浏览器]
    end

    subgraph "CDN 层"
        CDN[Cloudflare CDN]
    end

    subgraph "负载均衡层"
        NGINX[Nginx 负载均衡器]
    end

    subgraph "应用服务器集群"
        App1[FastAPI 实例 1]
        App2[FastAPI 实例 2]
        App3[FastAPI 实例 N]
    end

    subgraph "数据库层"
        PG_Master[(PostgreSQL 主库)]
        PG_Slave1[(PostgreSQL 从库 1)]
        PG_Slave2[(PostgreSQL 从库 2)]
    end

    subgraph "缓存层"
        Redis_Master[(Redis 主节点)]
        Redis_Slave[(Redis 从节点)]
    end

    subgraph "对象存储"
        OSS[阿里云 OSS]
    end

    subgraph "监控和日志"
        Prometheus[Prometheus 监控]
        Grafana[Grafana 可视化]
        ELK[ELK 日志系统]
    end

    Browser --> CDN
    CDN --> NGINX
    NGINX --> App1
    NGINX --> App2
    NGINX --> App3

    App1 --> PG_Master
    App2 --> PG_Master
    App3 --> PG_Master

    PG_Master -.->|复制| PG_Slave1
    PG_Master -.->|复制| PG_Slave2

    App1 --> Redis_Master
    App2 --> Redis_Master
    App3 --> Redis_Master

    Redis_Master -.->|复制| Redis_Slave

    App1 --> OSS
    App2 --> OSS
    App3 --> OSS

    App1 -.->|指标| Prometheus
    App2 -.->|指标| Prometheus
    App3 -.->|指标| Prometheus

    Prometheus --> Grafana

    App1 -.->|日志| ELK
    App2 -.->|日志| ELK
    App3 -.->|日志| ELK

    style Browser fill:#e3f2fd
    style NGINX fill:#fff3e0
    style App1 fill:#f3e5f5
    style PG_Master fill:#c8e6c9
    style Redis_Master fill:#ffcdd2
```

---

## 🔍 数据流向图

```mermaid
flowchart LR
    subgraph "前端"
        User[用户操作]
        UI[React 组件]
        Store[Zustand Store]
    end

    subgraph "网络层"
        HTTP[HTTP 客户端]
        WS[WebSocket]
    end

    subgraph "后端"
        Router[路由层]
        Middleware[中间件]
        Service[服务层]
        Model[模型层]
    end

    subgraph "数据存储"
        Cache[(Redis)]
        DB[(PostgreSQL)]
        Storage[对象存储]
    end

    subgraph "外部服务"
        AI[OpenAI API]
    end

    User --> UI
    UI --> Store
    Store --> HTTP
    Store --> WS

    HTTP --> Router
    WS --> Router
    Router --> Middleware
    Middleware --> Service

    Service --> Model
    Service --> Cache
    Service --> AI

    Model --> DB
    Service --> Storage

    Cache -.->|缓存命中| Service
    DB -.->|查询结果| Model
    AI -.->|AI 响应| Service

    style User fill:#e3f2fd
    style Store fill:#fff3e0
    style Service fill:#f3e5f5
    style DB fill:#c8e6c9
    style Cache fill:#ffcdd2
    style AI fill:#f3e5f5
```

---

## 📊 技术栈总览

```mermaid
mindmap
  root((NovelAIde<br/>技术栈))
    前端
      React 19
      Vite 5
      TypeScript 5
      Tailwind CSS 4
      Tiptap/Novel
      Zustand
      React Query
      React Router
      Recharts
      Lucide Icons
    后端
      Python 3.11+
      FastAPI 0.109+
      SQLAlchemy 2.0
      Pydantic 2.5+
      Uvicorn
      Alembic
      python-jose
      passlib
    数据库
      PostgreSQL 15+
      Redis 7+
      asyncpg
    AI 服务
      OpenAI API
      LangChain
      tiktoken
    基础设施
      Docker
      Nginx
      阿里云 OSS
      Cloudflare CDN
    开发工具
      Git
      ESLint
      Prettier
      Black
      pytest
      Vitest
```

---

## 🎯 核心模块交互

```mermaid
graph TB
    subgraph "用户界面"
        EditorUI[编辑器界面]
        WorksUI[作品管理界面]
        WorldViewUI[世界观界面]
    end

    subgraph "核心功能模块"
        EditorCore[编辑器核心]
        AutoSave[自动保存]
        WordCount[字数统计]
        AIAssist[AI 辅助写作]
        WorldViewCore[世界观管理]
        PromptCore[提示词管理]
    end

    subgraph "数据管理"
        WorkManager[作品管理器]
        ChapterManager[章节管理器]
        SettingManager[设定管理器]
        UserManager[用户管理器]
    end

    subgraph "外部服务集成"
        OpenAIService[OpenAI 服务]
        StorageService[存储服务]
        CacheService[缓存服务]
    end

    EditorUI --> EditorCore
    EditorCore --> AutoSave
    EditorCore --> WordCount
    EditorCore --> AIAssist
    
    WorksUI --> WorkManager
    WorldViewUI --> WorldViewCore
    
    AIAssist --> PromptCore
    AIAssist --> OpenAIService
    
    AutoSave --> ChapterManager
    WorkManager --> ChapterManager
    WorldViewCore --> SettingManager
    
    ChapterManager --> CacheService
    SettingManager --> StorageService
    UserManager --> CacheService

    style EditorCore fill:#e3f2fd
    style AIAssist fill:#f3e5f5
    style OpenAIService fill:#f3e5f5
    style ChapterManager fill:#c8e6c9
```

---

## 📝 总结

以上是 NovelAIde 项目的完整架构图，包括：

1. ✅ **系统整体架构** - 展示所有层次和组件
2. ✅ **前端架构** - React 组件和状态管理
3. ✅ **后端架构** - FastAPI 分层设计
4. ✅ **数据库设计** - ER 图和表关系
5. ✅ **业务流程** - 用户写作和 AI 服务流程
6. ✅ **认证授权** - JWT 完整流程
7. ✅ **部署架构** - 生产环境部署方案
8. ✅ **数据流向** - 数据在系统中的流动
9. ✅ **技术栈** - 所有使用的技术
10. ✅ **模块交互** - 核心功能模块关系

这些架构图可以帮助你：
- 📖 理解系统整体设计
- 🔍 定位具体功能的实现位置
- 🚀 规划新功能的开发
- 🤝 团队协作和技术交流

---

## 🎯 当前项目实现状态（详细） - 更新日期: 2025-10-21

### ✅ 已完成模块（90%+）

#### 后端 (95%)

**1. 用户认证系统 - 100%**
- ✅ 用户注册 `POST /api/v1/auth/register`
- ✅ 用户登录 `POST /api/v1/auth/login`
- ✅ Token 刷新 `POST /api/v1/auth/refresh`
- ✅ JWT Token 生成和验证
- ✅ 密码加密（bcrypt）
- ✅ 获取当前用户 `GET /api/v1/auth/me`
- ✅ 管理员权限验证

**2. 作品管理系统 - 100%**
- ✅ 创建作品 `POST /api/v1/works`
- ✅ 获取作品列表 `GET /api/v1/works`
- ✅ 获取作品详情 `GET /api/v1/works/{id}`
- ✅ 更新作品 `PUT /api/v1/works/{id}`
- ✅ 删除作品 `DELETE /api/v1/works/{id}`
- ✅ 作品统计（字数、章节数）

**3. 章节管理系统 - 100%**
- ✅ 创建章节 `POST /api/v1/chapters`
- ✅ 获取章节列表 `GET /api/v1/chapters/work/{id}`
- ✅ 获取章节详情 `GET /api/v1/chapters/{id}`
- ✅ 更新章节 `PUT /api/v1/chapters/{id}`
- ✅ 删除章节 `DELETE /api/v1/chapters/{id}`
- ✅ 章节排序 `POST /api/v1/chapters/reorder`
- ✅ 字数统计自动更新

**4. 世界观系统 - 95%**
- ✅ 角色管理 `CRUD /api/v1/worldview/characters`
- ✅ 地点管理 `CRUD /api/v1/worldview/locations`
- ✅ 设定管理 `CRUD /api/v1/worldview/settings`
- ✅ 作品规范 `CRUD /api/v1/worldview/work-guidelines`
- ✅ AI规范管理 (31个字段完整管理)
- ✅ 聚合接口 `GET /api/v1/worldview/all/{work_id}`

**5. AI服务系统 - 95%**
- ✅ AI续写 `POST /api/v1/ai/continue`
- ✅ AI扩写 `POST /api/v1/ai/expand`
- ✅ AI总结 `POST /api/v1/ai/summarize`
- ✅ AI润色 `POST /api/v1/ai/polish`
- ✅ AI翻译 `POST /api/v1/ai/translate`
- ✅ HTTPAIService完整实现
- ✅ 提示词管理系统 (JSON配置)

**6. 小说分析系统 - 100%**
- ✅ 触发分析 `POST /api/v1/analysis/works/{work_id}/trigger`
- ✅ 查询状态 `GET /api/v1/analysis/works/{work_id}/status`
- ✅ 章节概括 `POST /api/v1/chapters/{chapter_id}/summary`
- ✅ 世界观提取 `POST /api/v1/analysis/works/{work_id}/extract-worldview`
- ✅ 微观分析 (逐章节JSON结构化)
- ✅ 宏观分析 (人物/世界观/冲突)
- ✅ 向量存储服务

**7. 导入导出系统 - 100%**
- ✅ 导出作品 `POST /api/v1/works/{work_id}/export`
- ✅ 导入预览 `POST /api/v1/works/import/preview`
- ✅ 确认导入 `POST /api/v1/works/import/confirm`
- ✅ 文件下载 `GET /api/v1/downloads/{file_id}`
- ✅ JSON/Markdown导出
- ✅ 智能章节分割

**8. 全局搜索系统 - 100%**
- ✅ 全局搜索 `GET /api/v1/search`
- ✅ 5种类型搜索 (作品/章节/角色/地点/设定)
- ✅ 关键词片段提取
- ✅ 权限验证

**9. 管理后台 - 60%**
- ✅ 用户管理 `GET /api/v1/admin/users`
- ✅ 封禁用户 `PATCH /api/v1/admin/users/{id}/ban`
- ✅ 解封用户 `PATCH /api/v1/admin/users/{id}/unban`
- ✅ 角色切换 `PATCH /api/v1/admin/users/{id}/toggle-admin`

**10. 数据库模型 - 100%**
- ✅ User 模型（完整）
- ✅ Work 模型（完整）
- ✅ Chapter 模型（完整，含summary字段）
- ✅ Character 模型（完整）
- ✅ Location 模型（完整）
- ✅ Setting 模型（完整）
- ✅ WorkGuidelines 模型（完整）
- ✅ AIGuidelines 模型（31字段）
- ✅ NovelAnalysis 模型（完整）
- ✅ NovelAnalysisVector 模型（完整）
- ✅ SQLAlchemy Async ORM
- ✅ PostgreSQL 异步驱动（asyncpg）
- ✅ Alembic 数据库迁移

**5. 基础设施 - 70%**
- ✅ FastAPI 应用配置
- ✅ CORS 中间件
- ✅ JWT 认证中间件
- ✅ 全局异常处理
- ✅ 日志系统（基础）
- ✅ Pydantic 数据验证
- 🟡 Redis 配置（已配置，未实际使用）

#### 前端 (90%)

**1. 核心技术栈 - 100%**
- ✅ React 19.1.1
- ✅ TypeScript 5.9.3
- ✅ Vite 7.1.7
- ✅ Tailwind CSS 4.1.8
- ✅ React Router DOM 7.5.1
- ✅ Zustand 5.0.4
- ✅ ReactFlow 12 (世界观可视化)
- ✅ Recharts (图表)

**2. 编辑器系统 - 90%**
- ✅ Tiptap 3.7.0 完整集成
- ✅ 富文本编辑功能
- ✅ Markdown 支持
- ✅ 代码块语法高亮（37种语言）
- ✅ Slash命令系统（11个命令）
- ✅ AI功能菜单（5种AI操作）
- ✅ 自动保存
- ✅ 实时字数统计
- ✅ 拖拽处理（GlobalDragHandle）
- ✅ 气泡菜单（BubbleMenu）
- ✅ AI内容高亮

**3. 页面视图 - 100%**
- ✅ LoginView - 登录页
- ✅ RegisterView - 注册页
- ✅ HomeView - 首页
- ✅ WorksView - 作品列表
- ✅ WorkDetailView - 作品详情
- ✅ EditorView - 编辑器页面
- ✅ SettingsView - 设置页
- ✅ AdminDashboardView - 管理后台
- ✅ AdminUsersView - 用户管理
- ✅ AdminAIModelsView - AI模型管理
- ✅ AdminCostView - 成本统计
- ✅ NotFoundView - 404页面

**4. 编辑器组件 - 95%**
- ✅ NovelEditor.tsx - 主编辑器 (312行)
- ✅ EditorToolbar.tsx - 工具栏
- ✅ BubbleMenu.tsx - 气泡菜单
- ✅ AIMenu.tsx - AI助手菜单 (20KB)
- ✅ AIContinueDrawer.tsx - AI续写抽屉
- ✅ AIContinueDialog.tsx - AI续写对话框
- ✅ AIAutoComplete.tsx - AI自动补全
- ✅ SlashCommands.tsx - 斜杠命令
- ✅ ChapterTree.tsx - 章节树 (拖拽排序)
- ✅ EditorSidebar.tsx - 编辑器侧边栏
- ✅ WorldManager.tsx - 世界观管理器 (58KB)
- ✅ WorldviewSidebar.tsx - 简化侧边栏
- ✅ NovelAnalysisPanel.tsx - 小说分析面板
- ✅ NovelSummaryPanel.tsx - 概括面板

**5. 状态管理 - 100%**
- ✅ authStore.ts - 认证状态（含持久化）
- ✅ editorStore.ts - 编辑器状态
- ✅ globalStore.ts - 全局状态（Toast、Loading）

**6. 服务架构 - 95%**
- ✅ DataService.ts - 统一数据服务（完整实现）
- ✅ AIService.ts - AI服务类
- ✅ AuthService.ts - 认证服务
- ✅ ApiAdapter.ts - API适配器（完整对接）
- ✅ 字段名自动转换（camelCase ↔ snake_case）
- ✅ 请求/响应拦截器
- ✅ Token自动管理

**7. 新增组件 - 100%**
- ✅ WorldviewGraph.tsx - 关系图组件 (380行)
- ✅ GlobalSearch.tsx - 全局搜索 (381行)
- ✅ ExportDialog.tsx - 导出对话框 (233行)
- ✅ ImportDialog.tsx - 导入对话框 (371行)
- ✅ ConfirmDialog.tsx - 确认对话框
- ✅ Toast.tsx - 通知组件

**8. 世界观组件 - 95%**
- ✅ WorldviewView - 全屏管理页面
- ✅ WorldviewGraph - 关系图可视化
- ✅ 三种自定义节点（角色/地点/设定）
- ✅ 自动布局和交互

### 🟡 部分完成模块（30-90%）

**1. 管理后台 - 60%**
- ✅ 用户管理界面（封禁/解封/角色切换）
- 🟡 AI模型管理（仅UI，功能占位）
- 🟡 成本监控（仅UI，功能占位）
- ❌ 数据面板（待实现）

#### 后端

**1. Redis集成 - 30%**
- ✅ Redis配置完成（config.py）
- ✅ 依赖已安装（redis==5.0.1, aioredis==2.0.1）
- ❌ 未创建Redis连接池
- ❌ 未实现Token缓存
- ❌ 未实现数据缓存服务

### ❌ 未实现模块（0-30%） - Milestone 2 规划功能

#### Milestone 2 - AI增强功能（待实施）

**1. 去AI痕迹功能 - 0%**
- ❌ AI痕迹检测（0-100评分）
- ❌ 规则引擎实现
- ❌ AI二次润色
- ❌ 混合策略处理
- ❌ 10级强度调节
- ❌ 批量处理功能

**2. AI交互式反馈系统 - 0%**
- ❌ 多维度评分（5个维度）
- ❌ 优点分析
- ❌ 问题诊断
- ❌ 改进建议生成
- ❌ 一键重新生成

**3. 小说评审功能增强 - 0%**
- ❌ 专业评审报告
- ❌ 改稿任务清单
- ❌ 版本对比
- ❌ 3种评审模板

**4. AI写作竞技场 - 0%** ⭐⭐ **明星功能 - 独立页面**
- ❌ 独立页面设计（/ai-arena路由）
- ❌ 并发调用4-6个模型（GPT-4, Claude, Gemini, Qwen等）
- ❌ 战斗竞技场风格UI
- ❌ 实时生成状态展示
- ❌ 智能质量评分系统
- ❌ 用户选择与投票功能
- ❌ 历史记录与统计分析
- ❌ 数据库设计（compare_tasks, compare_results表）

**5. 提示词管理UI - 40%**
- ✅ JSON配置文件已实现
- ✅ PromptsManager类已实现
- ❌ 提示词管理界面
- ❌ 用户自定义提示词
- ❌ 快捷使用功能

**6. 数据统计增强 - 20%**
- ✅ 基础统计（字数、章节数）
- ❌ 个人写作统计页面
- ❌ 每日字数图表
- ❌ 创作热力图
- ❌ AI 使用统计详情

#### 基础设施

**1. 部署架构 - 0%**
- ❌ Docker 容器化
- ❌ Nginx 配置
- ❌ 负载均衡
- ❌ 监控系统（Prometheus + Grafana）
- ❌ 日志系统（ELK）
- ❌ CI/CD 流程

**2. 对象存储 - 0%**
- ❌ 阿里云 OSS 配置
- ❌ 图片上传服务
- ❌ 文件管理服务

**3. CDN 加速 - 0%**
- ❌ CDN 配置
- ❌ 静态资源优化

#### 其他功能

**1. 文件导入导出 - 100%** ✅ **已完成**
- ✅ JSON 导出（完整数据）
- ✅ Markdown 导出（格式化）
- ✅ JSON 导入（完整恢复）
- ✅ TXT/Markdown 导入（智能章节分割）
- ✅ 临时文件管理（24小时自动清理）
- ❌ DOCX 导入（待实现）
- ❌ EPUB 导出（待实现）
- ❌ PDF 导出（待实现）

**2. 协作功能 - 0%**
- ❌ 作品分享
- ❌ 权限控制
- ❌ 实时协作编辑
- ❌ 评论系统
- ❌ WebSocket 集成

---

## 🚀 下一步开发优先级 (更新日期: 2025-10-21)

### 🎉 Milestone 1 已100%完成！

**已完成的重要工作：**
- ✅ 前后端完全对接（ApiAdapter实现）
- ✅ AI服务集成（5种AI功能）
- ✅ 世界观系统（含关系图可视化）
- ✅ 小说分析系统
- ✅ 导入导出系统
- ✅ 全局搜索功能

---

### Phase 1: 去AI痕迹功能（5-7天）⚠️ P0 最高优先级

```
核心任务：
1. [2天] 规则引擎实现（TypeScript，0-100评分）
2. [2天] AI二次润色后端（Python + Prompt设计）
3. [1天] 前端UI实现（对比视图 + 强度调节）
4. [1天] 混合策略实现 + 批量处理
5. [1天] 测试优化

预期成果：
✅ AI痕迹检测功能
✅ 10级强度调节
✅ 对比视图
✅ 差异化竞争力核心功能
```

### Phase 2: AI交互式反馈系统（3天）⚠️ P0 高优先级

```
核心任务：
1. [1天] 多维度评分系统（5个维度）
2. [1天] 优点分析 + 问题诊断组件
3. [1天] AI反馈Prompt + 一键重新生成

预期成果：
✅ 多维度评分展示
✅ 优点和问题诊断
✅ 改进建议生成
✅ 增强用户信任
```

### Phase 3: 小说评审功能增强（3天）- P1 重要

```
核心任务：
1. [1天] 专业评审报告生成（5维度评分）
2. [1天] 改稿任务清单系统
3. [1天] 版本对比 + 3种评审模板

预期成果：
✅ 专业评审报告
✅ 改稿任务管理
✅ 版本进步追踪
```

### Phase 4: AI写作竞技场（1周）- P1 重要 ⭐⭐ **明星功能**

```
功能定位：独立页面，当用户不满意AI生成时，同时调用4-6个模型对比选择最佳

核心任务：
1. [2天] 战斗竞技场风格UI设计与实现
2. [2天] 并发调用多模型（asyncio.gather）
3. [1天] 智能质量评分系统
4. [1天] 历史记录与统计分析
5. [1天] 数据库设计（2张表）+ 5个API接口

预期成果：
✅ 独立竞技场页面（/ai-arena）
✅ 同时调用4-6个模型并发生成
✅ 卡片式对比展示（战斗竞技场风格）
✅ 实时生成状态更新
✅ 用户选择最佳结果
✅ 差异化竞争优势（核心卖点）
```

### Phase 5: Redis 缓存实现（1-2天）- P2 优化项

```
核心任务：
1. [4小时] 创建Redis连接池
2. [2小时] 实现Token缓存
3. [2小时] 实现热门数据缓存
4. [2小时] 配置缓存失效策略

预期成果：
✅ Token存储在Redis中
✅ 频繁访问数据被缓存
✅ 系统性能提升
```

---

## 📌 当前状态总结

### ✅ 已解决的问题
1. ~~前后端未对接~~ → ✅ 已完全对接（ApiAdapter）
2. ~~AI服务未实现~~ → ✅ 已完成（5种AI功能）
3. ~~世界观数据库模型缺失~~ → ✅ 已完成（10张表）
4. ~~导入导出功能缺失~~ → ✅ 已完成
5. ~~搜索功能缺失~~ → ✅ 已完成

### 🎯 下一步重点
1. **Milestone 2 - AI增强功能** (3-4周)
   - 去AI痕迹功能（差异化核心）
   - AI交互式反馈系统
   - 小说评审功能增强
   - **AI写作竞技场（明星功能）** ⭐⭐

2. **核心卖点打造** (重点)
   - AI写作竞技场：独立页面，多模型并发对比
   - 营销价值："6个顶级AI同时为你改写"
   - 差异化竞争优势

3. **可选优化** (低优先级)
   - Redis缓存实现
   - 性能监控
   - 单元测试补充

---

**更新日期**: 2025-10-21 (最新)  
**文档维护**: 请在完成新模块后及时更新本架构文档

## 📈 项目完成度总结

### 整体进度: **85%**

| 模块 | 完成度 | 状态 |
|------|--------|------|
| 用户认证系统 | 100% | ✅ 完成 |
| 作品管理系统 | 100% | ✅ 完成 |
| 章节管理系统 | 100% | ✅ 完成 |
| 编辑器系统 | 90% | ✅ 完成 |
| AI服务系统 | 95% | ✅ 完成 |
| 世界观系统 | 95% | ✅ 完成 |
| 小说分析系统 | 100% | ✅ 完成 |
| 导入导出系统 | 100% | ✅ 完成 |
| 全局搜索系统 | 100% | ✅ 完成 |
| 管理后台 | 60% | 🟡 进行中 |
| 前后端对接 | 95% | ✅ 完成 |
| 数据库设计 | 100% | ✅ 完成 |

### Milestone 完成情况

- **Milestone 1**: ✅ 100% 完成 (核心编辑功能)
- **Milestone 2**: ⏳ 0% 待实施 (AI增强功能)
- **Milestone 3**: 🟢 60% 部分完成 (3个功能提前完成)

### 技术栈实现情况

**前端 (90%)**
- ✅ React 19 + TypeScript
- ✅ Tiptap 3.7.0 编辑器
- ✅ Zustand 状态管理
- ✅ ReactFlow 12 可视化
- ✅ React Router v7 路由
- 🟡 UI组件库 (使用原生+少量自定义)

**后端 (95%)**
- ✅ FastAPI + Python 3.11
- ✅ SQLAlchemy 2.0 Async ORM
- ✅ PostgreSQL 数据库 (10张表)
- ✅ JWT 认证
- ✅ OpenAI API 集成
- 🟡 Redis (已配置未使用)

**已实现的12个后端API模块:**
1. ✅ `/api/v1/auth` - 认证 (3个接口)
2. ✅ `/api/v1/users` - 用户 (1个接口)
3. ✅ `/api/v1/works` - 作品 (6个接口)
4. ✅ `/api/v1/chapters` - 章节 (7个接口)
5. ✅ `/api/v1/ai` - AI服务 (5个接口)
6. ✅ `/api/v1/worldview/characters` - 角色 (5个接口)
7. ✅ `/api/v1/worldview/locations` - 地点 (5个接口)
8. ✅ `/api/v1/worldview/settings` - 设定 (5个接口)
9. ✅ `/api/v1/worldview/work-guidelines` - 作品规范 (5个接口)
10. ✅ `/api/v1/analysis` - 小说分析 (4个接口)
11. ✅ `/api/v1/search` - 全局搜索 (1个接口)
12. ✅ `/api/v1/admin` - 管理后台 (4个接口)

**总计**: ~56个后端API接口已实现 ✅

**待实现的Milestone 2 API模块:**
- ⏳ `/api/v1/ai-arena` - AI写作竞技场 (5个接口) ⭐⭐ **明星功能**
  - `POST /compare` - 创建对比任务
  - `GET /compare/{task_id}` - 查询对比结果
  - `POST /compare/{task_id}/select` - 选择最佳结果
  - `GET /history` - 历史记录
  - `GET /stats` - 统计数据
