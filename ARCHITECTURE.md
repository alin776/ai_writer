# NovelAIde 项目架构图

## 📐 完整架构总览

```mermaid
graph TB
    subgraph "客户端层"
        Browser[浏览器]
        Mobile[移动端 PWA]
    end

    subgraph "前端层 - React 19 + Vite"
        UI[UI 组件层]
        Editor[编辑器 Tiptap/Novel]
        State[状态管理 Zustand]
        API_Client[API 客户端]
        Router[路由 React Router]
    end

    subgraph "网关层"
        NGINX[Nginx 反向代理]
        CORS[CORS 中间件]
    end

    subgraph "后端层 - FastAPI"
        Auth[认证模块]
        Works[作品管理]
        Chapters[章节管理]
        AI_Service[AI 服务]
        WorldView[世界观系统]
        Prompt[提示词管理]
    end

    subgraph "数据层"
        PostgreSQL[(PostgreSQL 数据库)]
        Redis[(Redis 缓存)]
        OSS[阿里云 OSS 对象存储]
    end

    subgraph "第三方服务"
        OpenAI[OpenAI API<br/>https://204992.xyz]
        CDN[CDN 加速]
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
    style Editor fill:#fff3e0
    style AI_Service fill:#f3e5f5
    style OpenAI fill:#f3e5f5
    style PostgreSQL fill:#c8e6c9
    style Redis fill:#ffcdd2
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

## 🗄️ 数据库 ER 图

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
