# NovelAIde 核心流程图

## 核心业务流程

```mermaid
graph TB
    Start([用户登录]) --> Works[作品管理]

    Works --> Editor[章节编辑器]
    Works --> Analysis[小说分析]
    Works --> Worldview[世界观管理]

    Editor --> AI{AI 功能}
    AI --> Continue[续写]
    AI --> Polish[润色]
    AI --> Translate[翻译]
    AI --> Expand[扩写]

    Continue --> HTTPAIService
    Polish --> HTTPAIService
    Translate --> HTTPAIService
    Expand --> HTTPAIService

    HTTPAIService --> OpenAI[OpenAI API]
    HTTPAIService --> AILog[AI 日志记录]

    Analysis --> Micro[微观分析<br/>逐章分析]
    Analysis --> Macro[宏观分析<br/>整体分析]

    Micro --> Vector[向量化存储<br/>pgvector]
    Macro --> AutoExtract[自动提取世界观]
    AutoExtract --> Worldview

    Worldview --> Characters[角色]
    Worldview --> Locations[地点]
    Worldview --> Settings[设定]

    style Editor fill:#2196F3
    style AI fill:#FF9800
    style AILog fill:#F44336
    style Analysis fill:#9C27B0
    style Worldview fill:#00BCD4
```

## 技术架构

```mermaid
graph LR
    subgraph 前端
        React[React + TypeScript<br/>Zustand + Tiptap]
    end

    subgraph 后端
        FastAPI[FastAPI<br/>异步 AsyncSession]
    end

    subgraph 数据层
        DB[(PostgreSQL<br/>+ pgvector)]
    end

    subgraph 外部服务
        OpenAI[OpenAI API]
    end

    React --> FastAPI
    FastAPI --> DB
    FastAPI --> OpenAI

    style React fill:#61DAFB
    style FastAPI fill:#009688
    style DB fill:#336791
    style OpenAI fill:#412991
```

## 核心数据模型

```mermaid
erDiagram
    USER ||--o{ WORK : creates
    USER ||--o{ AI_CALL_LOG : generates

    WORK ||--o{ CHAPTER : contains
    WORK ||--o{ CHARACTER : has
    WORK ||--o{ LOCATION : has
    WORK ||--o{ NOVEL_ANALYSIS : analyzed_by

    CHAPTER ||--o{ AI_CALL_LOG : related_to
    NOVEL_ANALYSIS ||--o{ NOVEL_ANALYSIS_VECTOR : contains

    USER {
        int id
        string username
        boolean is_admin
    }

    WORK {
        int id
        string title
        int total_words
    }

    CHAPTER {
        int id
        string title
        text content
        string status
    }

    AI_CALL_LOG {
        int id
        string model_name
        int total_tokens
        float total_cost
    }
```

## 核心流程说明

### 1. 用户创作流程
```
登录 → 作品列表 → 编辑章节 → AI 辅助 → 保存
```

### 2. AI 调用链路
```
前端编辑器 → AIService → FastAPI /ai/complete
→ HTTPAIService → OpenAI API
→ AILogMiddleware 自动记录日志 → 返回流式响应
```

### 3. 小说分析流程
```
启动分析 → 后台异步任务 → 微观分析（逐章）+ 宏观分析（整体）
→ 向量化存储 → 自动提取世界观 → 更新角色/地点/设定
```

### 4. 关键技术特性
- ✅ 异步数据库操作 (AsyncSession)
- ✅ SSE 流式 AI 响应
- ✅ AI 调用自动日志记录
- ✅ 向量化语义搜索 (pgvector)
- ✅ JWT 认证 + 多设备会话管理
