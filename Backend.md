(venv) PS D:\Java\ai_writer\backend> python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
INFO:     Will watch for changes in these directories: ['D:\\Java\\ai_writer\\backend']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [45980] using WatchFiles
已注册策略: web_novel_11d - 网文11维度分析
2026-01-28 13:05:22,430 - app.main - INFO - [STARTUP] 监控中间件已注册: TraceMiddleware, MonitoringMiddleware
INFO:     Started server process [66668]
INFO:     Waiting for application startup.
2026-01-28 13:05:22,964 - app.main - INFO - [STARTUP] 应用启动中...
2026-01-28 13:05:22,964 - app.core.database - INFO - 正在初始化数据库... (尝试 1/3)
2026-01-28 13:05:23,142 - app.core.database - INFO - ✅ 数据库初始化成功
2026-01-28 13:05:23,142 - app.main - INFO - [STARTUP] 开始检查并初始化官方频道...
检查官方频道...
现有官方频道: {'读者茶馆', '作者酒馆', '官方实验室', '公共酒馆'}

✓ 所有官方频道都已存在，无需创建

现有官方频道列表:
  - 作者酒馆 (ID: c4a5fcd7-7fd1-4a18-8677-a15c052c7507)
  - 读者茶馆 (ID: 2e1b9d33-1400-4a40-802b-6d212d7a2fe5)
  - 公共酒馆 (ID: 3749ebb4-a2d6-4ab8-aa14-cf6c26611fc0)
  - 官方实验室 (ID: 452cfe84-3ac4-49e1-986b-260bcc3b8a6a)
2026-01-28 13:05:23,158 - app.main - INFO - [STARTUP] ✅ 官方频道检查完成
2026-01-28 13:05:23,160 - apscheduler.scheduler - INFO - Adding job tentatively -- it will be properly scheduled when the scheduler starts
2026-01-28 13:05:23,162 - apscheduler.scheduler - INFO - Adding job tentatively -- it will be properly scheduled when the scheduler starts
2026-01-28 13:05:23,163 - apscheduler.scheduler - INFO - Added job "清理过期的去痕迹会话详情" to job store "default"
2026-01-28 13:05:23,168 - apscheduler.scheduler - INFO - Added job "清理过期的 Agent 会话" to job store "default"
2026-01-28 13:05:23,168 - apscheduler.scheduler - INFO - Scheduler started
2026-01-28 13:05:23,168 - app.tasks.cleanup_humanize_details - INFO - 定时任务调度器已启动
2026-01-28 13:05:23,168 - apscheduler.scheduler - INFO - Adding job tentatively -- it will be properly scheduled when the scheduler starts
2026-01-28 13:05:23,168 - app.services.channel_scheduler - INFO - Channel scheduler initialized
2026-01-28 13:05:23,168 - apscheduler.scheduler - INFO - Added job "检查作品频道活跃度" to job store "default"
2026-01-28 13:05:23,168 - apscheduler.scheduler - INFO - Scheduler started
2026-01-28 13:05:23,168 - app.services.channel_scheduler - INFO - Channel scheduler started
2026-01-28 13:05:23,168 - app.main - INFO - [STARTUP] 开始预初始化同步Redis连接...
2026-01-28 13:05:23,172 - app.api.v1.agent - INFO - [Redis] 全局连接池已创建
2026-01-28 13:05:23,190 - app.main - INFO - [STARTUP] ✅ 同步Redis连接池预初始化完成
2026-01-28 13:05:23,190 - app.main - INFO - [STARTUP] 开始初始化AsyncRedisSaver索引...
2026-01-28 13:05:23,203 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ setup_checkpointer Redis连接验证成功
2026-01-28 13:05:23,212 - redisvl.index.index - INFO - Index already exists, not overwriting.
2026-01-28 13:05:23,215 - redisvl.index.index - INFO - Index already exists, not overwriting.
2026-01-28 13:05:23,216 - redisvl.index.index - INFO - Index already exists, not overwriting.
2026-01-28 13:05:23,217 - langgraph.checkpoint.redis.aio - INFO - Redis client is a standalone client
2026-01-28 13:05:23,217 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ AsyncRedisSaver索引预创建成功
2026-01-28 13:05:23,218 - app.main - INFO - [STARTUP] AsyncRedisSaver索引初始化完成
2026-01-28 13:05:23,219 - app.main - INFO - [STARTUP] 开始预加载Embedding模型...
2026-01-28 13:05:23,219 - app.services.vector_store_service - INFO - 🔄 预加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
2026-01-28 13:05:29,760 - app.services.vector_store_service - INFO - ✅ Embedding模型预加载成功，耗时: 6.54秒
2026-01-28 13:05:29,761 - app.main - INFO - [STARTUP] Embedding模型预加载完成
2026-01-28 13:05:29,761 - app.main - INFO - [STARTUP] P0性能优化已暂时禁用（诊断模式）
2026-01-28 13:05:29,761 - app.main - INFO - [STARTUP] 应用启动完成
INFO:     Application startup complete.
INFO:     ('127.0.0.1', 60162) - "WebSocket /api/v1/ws/notifications/79913e7e-d5cd-4e09-bce6-ca6639bd8456" [accepted]
2026-01-28 13:05:30,607 - app.api.v1.ws - INFO - [WebSocket] 通知连接建立: user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
INFO:     connection open
INFO:     ('127.0.0.1', 60019) - "WebSocket /api/v1/ws/notifications/79913e7e-d5cd-4e09-bce6-ca6639bd8456" [accepted]
2026-01-28 13:05:33,599 - app.api.v1.ws - INFO - [WebSocket] 通知连接建立: user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
INFO:     connection open
2026-01-28 13:05:53,000 - monitoring - INFO - Registered health check: cpu_usage
2026-01-28 13:05:53,000 - monitoring - INFO - Registered health check: memory_usage
2026-01-28 13:05:53,000 - monitoring - INFO - Registered health check: disk_usage
2026-01-28 13:05:53,000 - monitoring - INFO - Registered health check: process_status
2026-01-28 13:05:53,000 - monitoring - INFO - Added alert rule: high_cpu_usage
2026-01-28 13:05:53,009 - monitoring - INFO - Added alert rule: high_memory_usage
2026-01-28 13:05:53,009 - monitoring - INFO - Added alert rule: low_disk_space
2026-01-28 13:05:53,020 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, chapter_id: 6d3a500b-ca4f-436c-87c9-7eff4829f4f8
2026-01-28 13:05:53,069 - app.core.redis - INFO - ✅ Redis connected: redis://localhost:6379/0
2026-01-28 13:05:53,107 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 6d3a500b-ca4f-436c-87c9-7eff4829f4f8
2026-01-28 13:05:53,121 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: c682287e-0ebf-47c2-8d4b-489ec163ff73
2026-01-28 13:05:53,123 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-28 13:05:53,128 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:56917 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-28 13:05:53,536 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, chapter_id: 6d3a500b-ca4f-436c-87c9-7eff4829f4f8
2026-01-28 13:05:53,691 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 6d3a500b-ca4f-436c-87c9-7eff4829f4f8
2026-01-28 13:05:53,722 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: c682287e-0ebf-47c2-8d4b-489ec163ff73
2026-01-28 13:05:53,724 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-28 13:05:53,784 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:52362 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-28 13:05:53,999 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:52727 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2026-01-28 13:05:54,011 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/6d3a500b-ca4f-436c-87c9-7eff4829f4f8/revisions
INFO:     127.0.0.1:52729 - "GET /api/v1/chapters/6d3a500b-ca4f-436c-87c9-7eff4829f4f8/revisions?status=pending HTTP/1.1" 200 OK
2026-01-28 13:05:54,159 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21
2026-01-28 13:05:54,163 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/6d3a500b-ca4f-436c-87c9-7eff4829f4f8
INFO:     127.0.0.1:58253 - "PUT /api/v1/chapters/6d3a500b-ca4f-436c-87c9-7eff4829f4f8 HTTP/1.1" 200 OK
2026-01-28 13:05:54,173 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第37章 【白日飞升，千古传奇】 (order=31)
2026-01-28 13:05:54,190 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/6d3a500b-ca4f-436c-87c9-7eff4829f4f8/revisions
INFO:     127.0.0.1:51515 - "GET /api/v1/chapters/6d3a500b-ca4f-436c-87c9-7eff4829f4f8/revisions?status=pending HTTP/1.1" 200 OK
2026-01-28 13:05:57,509 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/4a93b891-fc7b-468c-90e8-4ccaac9a1cff
2026-01-28 13:05:57,509 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/5ea810a8-77d4-48f3-9af6-bc03a8014326
INFO:     127.0.0.1:57530 - "GET /api/v1/agent/operations/4a93b891-fc7b-468c-90e8-4ccaac9a1cff HTTP/1.1" 200 OK
INFO:     127.0.0.1:57531 - "GET /api/v1/agent/operations/5ea810a8-77d4-48f3-9af6-bc03a8014326 HTTP/1.1" 200 OK
2026-01-28 13:05:57,526 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/c682287e-0ebf-47c2-8d4b-489ec163ff73/revisions
INFO:     127.0.0.1:55784 - "GET /api/v1/chapters/c682287e-0ebf-47c2-8d4b-489ec163ff73/revisions?status=pending HTTP/1.1" 200 OK
2026-01-28 13:05:57,810 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第37章 【白日飞升，千古传奇】 (75 paragraphs)
2026-01-28 13:05:57,826 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/4a93b891-fc7b-468c-90e8-4ccaac9a1cff
2026-01-28 13:05:57,829 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, chapter_id: c682287e-0ebf-47c2-8d4b-489ec163ff73
INFO:     127.0.0.1:53074 - "GET /api/v1/agent/operations/4a93b891-fc7b-468c-90e8-4ccaac9a1cff HTTP/1.1" 200 OK
2026-01-28 13:05:57,835 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/5ea810a8-77d4-48f3-9af6-bc03a8014326
2026-01-28 13:05:57,837 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, chapter_id: c682287e-0ebf-47c2-8d4b-489ec163ff73
INFO:     127.0.0.1:51557 - "GET /api/v1/agent/operations/5ea810a8-77d4-48f3-9af6-bc03a8014326 HTTP/1.1" 200 OK
2026-01-28 13:05:57,896 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: c682287e-0ebf-47c2-8d4b-489ec163ff73
2026-01-28 13:05:57,908 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: f44a723d-f23b-407c-9279-ef0be02b202d
2026-01-28 13:05:57,908 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-28 13:05:57,919 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: c682287e-0ebf-47c2-8d4b-489ec163ff73
2026-01-28 13:05:57,929 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
2026-01-28 13:05:57,936 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: f44a723d-f23b-407c-9279-ef0be02b202d
2026-01-28 13:05:57,936 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
INFO:     127.0.0.1:55969 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-28 13:05:57,948 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:55782 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-28 13:05:57,961 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/c682287e-0ebf-47c2-8d4b-489ec163ff73/revisions
2026-01-28 13:05:57,965 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21
INFO:     127.0.0.1:62888 - "GET /api/v1/chapters/c682287e-0ebf-47c2-8d4b-489ec163ff73/revisions?status=pending HTTP/1.1" 200 OK
2026-01-28 13:05:57,969 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/c682287e-0ebf-47c2-8d4b-489ec163ff73
INFO:     127.0.0.1:53073 - "PUT /api/v1/chapters/c682287e-0ebf-47c2-8d4b-489ec163ff73 HTTP/1.1" 200 OK
2026-01-28 13:05:57,995 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第36章 【齐天大圣，九窍通天】 (order=30)
2026-01-28 13:06:01,064 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 6d3a500b-ca4f-436c-87c9-7eff4829f4f8 内容更新，新段落数: 75
2026-01-28 13:06:01,180 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第36章 【齐天大圣，九窍通天】 (81 paragraphs)
2026-01-28 13:06:01,182 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:58777 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2026-01-28 13:06:01,206 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21
2026-01-28 13:06:01,209 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/6d3a500b-ca4f-436c-87c9-7eff4829f4f8
INFO:     127.0.0.1:57999 - "PUT /api/v1/chapters/6d3a500b-ca4f-436c-87c9-7eff4829f4f8 HTTP/1.1" 200 OK
2026-01-28 13:06:01,215 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第37章 【白日飞升，千古传奇】 (order=31)
2026-01-28 13:06:04,746 - app.services.ai.prompts - INFO - Prompts loaded successfully from D:\Java\ai_writer\backend\app\services\ai\prompts\default.json
2026-01-28 13:06:04,746 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-28 13:06:04,746 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-28 13:06:04,746 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2026-01-28 13:06:06,241 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz:8443/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-28 13:06:06,241 - app.api.v1.agent - INFO - [Chat Stream] Mode: planning
2026-01-28 13:06:06,253 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第37章 【白日飞升，千古传奇】 (75 paragraphs)
2026-01-28 13:06:06,253 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:51337 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2026-01-28 13:06:06,270 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21
2026-01-28 13:06:06,273 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/c682287e-0ebf-47c2-8d4b-489ec163ff73
INFO:     127.0.0.1:54336 - "PUT /api/v1/chapters/c682287e-0ebf-47c2-8d4b-489ec163ff73 HTTP/1.1" 200 OK
2026-01-28 13:06:06,275 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第36章 【齐天大圣，九窍通天】 (order=30)
2026-01-28 13:06:06,279 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 主题：系统10086的态度变化如何被“林仙的修行路线/价值观”推动。
  要求：

  1. 给出系...
2026-01-28 13:06:06,279 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-28 13:06:06,280 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-28 13:06:06,280 - app.services.ai.http_ai_service - INFO - [成本追踪] 初始化未传db/user_id，将使用请求上下文按需记录成本
2026-01-28 13:06:07,797 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz:8443/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-28 13:06:07,797 - app.services.agent.tools.writing_tools - INFO - Writing tools AI service initialized
2026-01-28 13:06:07,797 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ AI Service 已同时设置到 langgraph_tools 和 writing_tools
2026-01-28 13:06:07,805 - app.services.context.adaptive_budget - INFO - ✅ 所有预算配置验证通过
2026-01-28 13:06:14,451 - app.services.context.vector_memory_store - INFO - ✅ VectorMemoryStore初始化成功 | 目录=./data/chroma_db | 模型=paraphrase-multilingual-MiniLM-L12-v2 | 集合=user_memories
2026-01-28 13:06:14,451 - app.services.context.manager - INFO - ✅ VectorMemoryStore 已初始化
2026-01-28 13:06:14,451 - app.services.context.manager - INFO - ✅ ContextManager: 长期记忆已启用 (user_id=None)
2026-01-28 13:06:14,451 - app.services.context.manager - INFO - ✅ ContextManager: 自适应预算已启用
2026-01-28 13:06:14,451 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ ContextManager已初始化（长期记忆已启用，自适应预算已启用，总预算=16000 tokens）
成功加载模板: analyze_text (版本 3.1.0)
成功加载模板: writing_agent (版本 2.0.0)
成功加载模板: system_agent_prompt (版本 2.1.0)
成功加载模板: creative_writing_prompt (版本 1.0.0)
2026-01-28 13:06:14,594 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ PromptManager已初始化
2026-01-28 13:06:14,602 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ Redis连接验证成功
2026-01-28 13:06:14,604 - app.services.agent.langgraph_agent - INFO - [LangGraph] OK 使用 AsyncRedisSaver（redis://localhost:6379/0，TTL=7天）
2026-01-28 13:06:14,604 - app.services.agent.memory.metrics - INFO - [MemoryMetrics] 监控系统已初始化
2026-01-28 13:06:14,605 - app.services.agent.memory.long_term_store - INFO - [LongTermStore] Initialized: base_dir=./data/long_term_memory, max_size=50KB, compression=True
2026-01-28 13:06:14,605 - app.services.agent.memory.enhanced_memory_manager - INFO - EnhancedMemoryManager initialized: short=10, medium=100, threshold=0.1, long_term_backup=enabled
2026-01-28 13:06:14,606 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ EnhancedMemoryManager已创建
2026-01-28 13:06:14,606 - app.services.agent.memory.unified_coordinator - INFO - [UnifiedMemoryCoordinator] 初始化统一记忆协调器
2026-01-28 13:06:14,606 - app.services.agent.memory.unified_coordinator - INFO - [UnifiedMemoryCoordinator] 全局实例已设置
2026-01-28 13:06:14,607 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ UnifiedMemoryCoordinator已初始化 | checkpointer=AsyncRedisSaver | enhanced_memory=yes | context_manager=yes
2026-01-28 13:06:14,607 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ 解耦模块已初始化 (IntentClassifier, ToolExecutor, EventParser, ResponseBuilder, ToolDispatcher, ParallelExecutor, PlanGenerator, QuickPathHandler, StreamEventHandler, SecondaryToolHandler, TaskRunner, AgentExecutor)
2026-01-28 13:06:14,617 - app.services.agent.parallel_tool_node - INFO - [ParallelToolNode] 初始化完成，最大并发数=5，并行安全工具=6个
2026-01-28 13:06:14,693 - app.api.v1.agent - INFO - [Global Agent] created global agent instance; MemorySaver shared across requests
2026-01-28 13:06:16,484 - app.api.v1.agent - INFO - [agent_chat_stream] 📚 世界观数据已注入: 人物=8, 地点=7, 设定=7, 规范=无
2026-01-28 13:06:16,484 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21:26e13e5c-f8ea-4efd-88c1-03bb694d0510 (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, conversation_id=26e13e5c-f8ea-4efd-88c1-03bb694d0510)
2026-01-28 13:06:16,484 - app.services.context.monitoring_integration - INFO - ✅ ContextManager监控收集器已初始化
2026-01-28 13:06:16,487 - app.services.context.store - INFO - [ContextStore] Redis连接成功
2026-01-28 13:06:16,492 - app.services.context.manager - INFO - [ContextManager] 创建新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21:26e13e5c-f8ea-4efd-88c1-03bb694d0510
2026-01-28 13:06:16,797 - app.services.context.token_counter - INFO - ✅ tiktoken初始化成功，模型: gemini-2.5-pro -> cl100k_base
2026-01-28 13:06:16,798 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21:26e13e5c-f8ea-4efd-88c1-03bb694d0510: 0/16000 tokens
2026-01-28 13:06:18,069 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='主题：系统10086的态度变化如何被“林仙的修行路线/价值观...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=3条
2026-01-28 13:06:18,070 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21 | 含用户级=True | 找到=3条
2026-01-28 13:06:18,110 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 1条消息, 0 tokens, 耗时 1625.85ms
2026-01-28 13:06:18,110 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 1 条历史消息 (token: 0, has_summary: False)
2026-01-28 13:06:18,115 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-28 13:06:18,115 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-28 13:06:18,116 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=200, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-28 13:06:18,121 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第36章 【齐天大圣，九窍通天】 (81 paragraphs)
2026-01-28 13:06:19,901 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 13:06:19,901 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-28 13:06:19,932 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 13:06:19,938 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=547, cost=$0.000060, time=1784ms
2026-01-28 13:06:19,938 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=39, 尝试次数=1
2026-01-28 13:06:19,942 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-28 13:06:19,943 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-28 13:06:19,944 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=20, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-28 13:06:21,330 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 13:06:21,330 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-28 13:06:21,352 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 13:06:21,358 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=473, cost=$0.000048, time=1386ms
2026-01-28 13:06:21,358 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=8, 尝试次数=1
2026-01-28 13:06:21,358 - app.services.agent.intent.classifier - INFO - [Intent] AI识别结果: analysis
2026-01-28 13:06:21,358 - app.services.agent.langgraph_agent - INFO - [Planning] AI意图分类: analysis (置信度: 0.90)
2026-01-28 13:06:21,358 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 主题：系统10086的态度变化如何被“林仙的修行路线/价值观”推动。
  要求：

  1. 给出系...
2026-01-28 13:06:21,365 - app.core.cache - INFO - ✅ 缓存命中: prompt:planning:v2.41.0:get_planning_static_prompt:fca6eb91156619d0
2026-01-28 13:06:21,370 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-28 13:06:21,371 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=story_planning, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: story_planning; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-01-28 13:06:21,371 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.3, task_type=TaskType.STORY_PLANNING
2026-01-28 13:06:37,796 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-28 13:06:51,720 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 26 个数据块，总长度: 4993
2026-01-28 13:06:51,720 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 23159 (prompt=21516, completion=1643)
2026-01-28 13:06:51,720 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 13:06:51,720 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-28 13:06:51,729 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 13:06:51,739 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=23159, cost=$0.043325, time=30348ms
2026-01-28 13:06:51,741 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=23159
2026-01-28 13:06:51,741 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户需要一份基于原文证据的分析报告，论证“林仙的修行路线/价, 原料=需要从作品中检索四类关键信息：1. 系统, 处理=通过并行的四个`explore_cont
2026-01-28 13:06:51,762 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共4个任务
2026-01-28 13:06:51,762 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共4个任务，耗时: 30.40s
2026-01-28 13:06:51,762 - app.api.v1.agent - INFO - [Stream] Plan tasks: 4 items
2026-01-28 13:06:51,762 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2026-01-28 13:06:51,762 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2026-01-28 13:06:51,762 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2026-01-28 13:06:51,762 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] DAG 调度启用，任务数=4, 有依赖任务=0
2026-01-28 13:06:51,771 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1开始: 检索系统10086从“机械冷峻”到“慌乱/挣扎”的原文证据。
2026-01-28 13:06:51,771 - app.api.v1.agent - INFO - [Stream] Task started: 检索系统10086从“机械冷峻”到“慌乱/挣扎”的原文证据。 (icon=Wrench)
2026-01-28 13:06:51,772 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: explore_content
2026-01-28 13:06:51,773 - app.services.agent.tools.explore_tools - INFO - [explore_content] 开始: work_id=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, target=查找系统10086态度从机械冷峻到慌乱/挣扎的原文证据...
2026-01-28 13:06:51,774 - app.services.agent.tools.explore_tools - INFO - [explore_content] 规划传入关键词: ['系统10086', '机械', '冷峻', '电子音', '慌乱', '挣扎', '警告']
2026-01-28 13:06:51,781 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 开始探索 V5: work_id=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, target=查找系统10086态度从机械冷峻到慌乱/挣扎的原文证据...
2026-01-28 13:06:51,781 - app.services.chapter_service - INFO - [ChapterService] Querying chapters for work_id=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, type=<class 'uuid.UUID'>
2026-01-28 13:06:51,791 - app.services.chapter_service - INFO - [ChapterService] Found 77 chapters
2026-01-28 13:06:51,791 - app.services.chapter_service - INFO -   - Chapter: 第1章 【摆烂的宿主】, order=1
2026-01-28 13:06:51,791 - app.services.chapter_service - INFO -   - ... (75 more chapters)
2026-01-28 13:06:51,798 - app.services.chapter_service - INFO -   - Chapter: 第100章 【火域铸真器，两脉起冲突】, order=77
2026-01-28 13:06:53,226 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 强制流程步骤: list_chapters
2026-01-28 13:06:53,226 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=list_chapters params={"work_id": "5fe6c67d-8a1b-48c1-ad56-a5281eb22e21"}
2026-01-28 13:06:53,226 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=list_chapters success=True count=77
2026-01-28 13:06:53,226 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 强制流程步骤: list_paragraphs
2026-01-28 13:06:53,229 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=list_paragraphs params={"chapter_order": 1, "offset": 0, "limit": 50, "preview_len": 80, "work_id": "5fe6c67d-8a1b-48c1-ad56-a5281eb22e21"}
2026-01-28 13:06:53,242 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=list_paragraphs success=True chapter=1 offset=0 limit=50 approximate=None
2026-01-28 13:06:53,242 - app.services.ai.http_ai_service - INFO - [成本追踪] 初始化未传db/user_id，将使用请求上下文按需记录成本
2026-01-28 13:06:54,860 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz:8443/v1, Model: gemini-2.5-flash, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: False, CostTracking: True
2026-01-28 13:06:54,860 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-28 13:06:54,860 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-28 13:06:58,342 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 13:06:58,342 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-28 13:06:58,369 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 13:06:58,369 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1448, cost=$0.000751, time=3482ms
2026-01-28 13:06:58,373 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=272, 尝试次数=1
2026-01-28 13:06:58,373 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"work_id": "5fe6c67d-8a1b-48c1-ad56-a5281eb22e21", "keywords": ["系统10086"], "match_mode": "all", "limit": 100}
2026-01-28 13:06:58,799 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['系统10086']..., mode=all, range=None, hits=100
2026-01-28 13:06:58,808 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=23 corrected=False final=23
2026-01-28 13:06:58,808 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第23段
2026-01-28 13:06:58,817 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=61 corrected=False final=61
2026-01-28 13:06:58,817 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第61段
2026-01-28 13:06:58,823 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=64 corrected=False final=64
2026-01-28 13:06:58,823 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第64段
2026-01-28 13:06:58,831 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=105 corrected=False final=105
2026-01-28 13:06:58,831 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第105段
2026-01-28 13:06:58,848 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=106 corrected=False final=106
2026-01-28 13:06:58,848 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第106段
2026-01-28 13:06:58,865 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=19 corrected=False final=19
2026-01-28 13:06:58,865 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第19段
2026-01-28 13:06:58,874 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=23 corrected=False final=23
2026-01-28 13:06:58,874 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第23段
2026-01-28 13:06:58,882 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=24 corrected=False final=24
2026-01-28 13:06:58,882 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第24段
2026-01-28 13:06:58,893 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=49 corrected=False final=49
2026-01-28 13:06:58,893 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第49段
2026-01-28 13:06:58,906 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=52 corrected=False final=52
2026-01-28 13:06:58,907 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第52段
2026-01-28 13:06:58,916 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=60 corrected=False final=60
2026-01-28 13:06:58,916 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第60段
2026-01-28 13:06:58,925 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=77 corrected=False final=77
2026-01-28 13:06:58,925 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第77段
2026-01-28 13:06:58,934 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=79 corrected=False final=79
2026-01-28 13:06:58,934 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第79段
2026-01-28 13:06:58,949 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=89 corrected=False final=89
2026-01-28 13:06:58,949 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第89段
2026-01-28 13:06:58,964 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=25 corrected=False final=25
2026-01-28 13:06:58,965 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第25段
2026-01-28 13:06:58,976 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=27 corrected=False final=27
2026-01-28 13:06:58,976 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第27段
2026-01-28 13:06:58,988 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=29 corrected=False final=29
2026-01-28 13:06:58,988 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第29段
2026-01-28 13:06:58,997 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=30 corrected=False final=30
2026-01-28 13:06:58,997 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第30段
2026-01-28 13:06:59,008 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=34 corrected=False final=34
2026-01-28 13:06:59,008 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第34段
2026-01-28 13:06:59,018 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=35 corrected=False final=35
2026-01-28 13:06:59,018 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第35段
2026-01-28 13:06:59,029 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=41 corrected=False final=41
2026-01-28 13:06:59,029 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第41段
2026-01-28 13:06:59,041 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=46 corrected=False final=46
2026-01-28 13:06:59,041 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第46段
2026-01-28 13:06:59,050 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=60 corrected=False final=60
2026-01-28 13:06:59,050 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第60段
2026-01-28 13:06:59,064 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=128 corrected=False final=128
2026-01-28 13:06:59,065 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第5章第128段
2026-01-28 13:06:59,075 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=123 corrected=False final=123
2026-01-28 13:06:59,075 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第6章第123段
2026-01-28 13:06:59,082 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=129 corrected=False final=129
2026-01-28 13:06:59,082 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第6章第129段
2026-01-28 13:06:59,093 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=134 corrected=False final=134
2026-01-28 13:06:59,093 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第6章第134段
2026-01-28 13:06:59,103 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=141 corrected=False final=141
2026-01-28 13:06:59,103 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第6章第141段
2026-01-28 13:06:59,106 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=8 corrected=False final=8
2026-01-28 13:06:59,106 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第7章第8段
2026-01-28 13:06:59,116 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=18 corrected=False final=18
2026-01-28 13:06:59,116 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第7章第18段
2026-01-28 13:06:59,132 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=26 corrected=False final=26
2026-01-28 13:06:59,132 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第7章第26段
2026-01-28 13:06:59,142 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=28 corrected=False final=28
2026-01-28 13:06:59,142 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第7章第28段
2026-01-28 13:06:59,149 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=36 corrected=False final=36
2026-01-28 13:06:59,149 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第7章第36段
2026-01-28 13:06:59,157 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=40 corrected=False final=40
2026-01-28 13:06:59,157 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第7章第40段
2026-01-28 13:06:59,167 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=42 corrected=False final=42
2026-01-28 13:06:59,167 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第7章第42段
2026-01-28 13:06:59,182 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=46 corrected=False final=46
2026-01-28 13:06:59,182 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第7章第46段
2026-01-28 13:06:59,191 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=27 corrected=False final=27
2026-01-28 13:06:59,191 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第8章第27段
2026-01-28 13:06:59,206 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=36 corrected=False final=36
2026-01-28 13:06:59,206 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第8章第36段
2026-01-28 13:06:59,219 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=55 corrected=False final=55
2026-01-28 13:06:59,219 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第8章第55段
2026-01-28 13:06:59,230 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=58 corrected=False final=58
2026-01-28 13:06:59,230 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第8章第58段
2026-01-28 13:06:59,240 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=61 corrected=False final=61
2026-01-28 13:06:59,240 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第8章第61段
2026-01-28 13:06:59,248 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=39 corrected=False final=39
2026-01-28 13:06:59,251 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第9章第39段
2026-01-28 13:06:59,261 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=42 corrected=False final=42
2026-01-28 13:06:59,261 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第9章第42段
2026-01-28 13:06:59,273 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=45 corrected=False final=45
2026-01-28 13:06:59,274 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第9章第45段
2026-01-28 13:06:59,283 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=34 corrected=False final=34
2026-01-28 13:06:59,283 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第11章第34段
2026-01-28 13:06:59,292 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=46 corrected=False final=46
2026-01-28 13:06:59,292 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第17章第46段
2026-01-28 13:06:59,303 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=53 corrected=False final=53
2026-01-28 13:06:59,307 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第17章第53段
2026-01-28 13:06:59,316 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=71 corrected=False final=71
2026-01-28 13:06:59,316 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第17章第71段
2026-01-28 13:06:59,327 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=73 corrected=False final=73
2026-01-28 13:06:59,327 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第17章第73段
2026-01-28 13:06:59,342 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=76 corrected=False final=76
2026-01-28 13:06:59,342 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第17章第76段
2026-01-28 13:06:59,350 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=77 corrected=False final=77
2026-01-28 13:06:59,355 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第17章第77段
2026-01-28 13:06:59,367 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=78 corrected=False final=78
2026-01-28 13:06:59,368 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第17章第78段
2026-01-28 13:06:59,377 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=80 corrected=False final=80
2026-01-28 13:06:59,377 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第17章第80段
2026-01-28 13:06:59,387 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=90 corrected=False final=90
2026-01-28 13:06:59,387 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第19章第90段
2026-01-28 13:06:59,398 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=2 corrected=False final=2
2026-01-28 13:06:59,398 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第23章第2段
2026-01-28 13:06:59,406 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=3 corrected=False final=3
2026-01-28 13:06:59,406 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第23章第3段
2026-01-28 13:06:59,417 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=8 corrected=False final=8
2026-01-28 13:06:59,417 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第23章第8段
2026-01-28 13:06:59,432 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=11 corrected=False final=11
2026-01-28 13:06:59,432 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第23章第11段
2026-01-28 13:06:59,440 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=16 corrected=False final=16
2026-01-28 13:06:59,440 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第23章第16段
2026-01-28 13:06:59,457 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=19 corrected=False final=19
2026-01-28 13:06:59,459 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第23章第19段
2026-01-28 13:06:59,459 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=92 keywords=系统10086
2026-01-28 13:06:59,459 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 探索完成(工具循环): 3轮, 原因=达到读取上限
2026-01-28 13:06:59,470 - app.services.agent.execution.tool_executor - INFO - [StandardTool] explore_content 执行成功
2026-01-28 13:06:59,474 - app.api.v1.agent - INFO - [Stream] 任务完成: 检索系统10086从“机械冷峻”到“慌乱/挣扎”的原文证据。 (7.7s)
2026-01-28 13:06:59,474 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1完成
2026-01-28 13:06:59,478 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务2开始: 检索林仙“布局十佬/交易王家/收集药材成仙”的原文证据。
2026-01-28 13:06:59,478 - app.api.v1.agent - INFO - [Stream] Task started: 检索林仙“布局十佬/交易王家/收集药材成仙”的原文证据。 (icon=Wrench)
2026-01-28 13:06:59,478 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: explore_content
2026-01-28 13:06:59,478 - app.services.agent.tools.explore_tools - INFO - [explore_content] 开始: work_id=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, target=查找林仙“布局十佬/交易王家/收集药材成仙”的原文证据...
2026-01-28 13:06:59,478 - app.services.agent.tools.explore_tools - INFO - [explore_content] 规划传入关键词: ['林仙', '十佬', '布局', '王家', '交易', '药材', '成仙']
2026-01-28 13:06:59,480 - app.services.agent.tools.explore_tools - INFO - [explore_content] 复用共享状态: searched=1, read_paragraphs=60, read_chapters=0
2026-01-28 13:06:59,480 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 开始探索 V5: work_id=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, target=查找林仙“布局十佬/交易王家/收集药材成仙”的原文证据...
2026-01-28 13:06:59,480 - app.services.chapter_service - INFO - [ChapterService] Querying chapters for work_id=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, type=<class 'uuid.UUID'>
2026-01-28 13:06:59,487 - app.services.chapter_service - INFO - [ChapterService] Found 77 chapters
2026-01-28 13:06:59,487 - app.services.chapter_service - INFO -   - Chapter: 第1章 【摆烂的宿主】, order=1
2026-01-28 13:06:59,487 - app.services.chapter_service - INFO -   - ... (75 more chapters)
2026-01-28 13:06:59,487 - app.services.chapter_service - INFO -   - Chapter: 第100章 【火域铸真器，两脉起冲突】, order=77
2026-01-28 13:06:59,522 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 强制流程步骤: list_chapters
2026-01-28 13:06:59,522 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=list_chapters params={"work_id": "5fe6c67d-8a1b-48c1-ad56-a5281eb22e21"}
2026-01-28 13:06:59,522 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=list_chapters success=True count=77
2026-01-28 13:06:59,522 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 强制流程步骤: list_paragraphs
2026-01-28 13:06:59,522 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=list_paragraphs params={"chapter_order": 1, "offset": 0, "limit": 50, "preview_len": 80, "work_id": "5fe6c67d-8a1b-48c1-ad56-a5281eb22e21"}
2026-01-28 13:06:59,541 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=list_paragraphs success=True chapter=1 offset=0 limit=50 approximate=None
2026-01-28 13:06:59,541 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-28 13:06:59,541 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-28 13:07:02,329 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 13:07:02,329 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-28 13:07:02,358 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 13:07:02,360 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1483, cost=$0.000740, time=2789ms
2026-01-28 13:07:02,362 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=258, 尝试次数=1
2026-01-28 13:07:02,362 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"work_id": "5fe6c67d-8a1b-48c1-ad56-a5281eb22e21", "keywords": "布局十佬", "match_mode": "all", "limit": 10}
2026-01-28 13:07:02,404 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['布局十佬']..., mode=all, range=None, hits=0
2026-01-28 13:07:02,406 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=0 keywords=布局十佬
2026-01-28 13:07:02,406 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-28 13:07:02,406 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-28 13:07:05,148 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 13:07:05,148 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-28 13:07:05,165 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 13:07:05,165 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=840, cost=$0.000514, time=2742ms
2026-01-28 13:07:05,165 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=257, 尝试次数=1
2026-01-28 13:07:05,165 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"work_id": "林仙", "keywords": ["交易", "王家"], "match_mode": "and", "limit": 100}
2026-01-28 13:07:05,258 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['交易', '王家']..., mode=any, range=None, hits=34
2026-01-28 13:07:05,269 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=254 corrected=False final=254
2026-01-28 13:07:05,269 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第17章第254段
2026-01-28 13:07:05,279 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=255 corrected=False final=255
2026-01-28 13:07:05,281 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第17章第255段
2026-01-28 13:07:05,291 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=264 corrected=False final=264
2026-01-28 13:07:05,293 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第17章第264段
2026-01-28 13:07:05,301 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=267 corrected=False final=267
2026-01-28 13:07:05,301 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第17章第267段
2026-01-28 13:07:05,315 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=271 corrected=False final=271
2026-01-28 13:07:05,315 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第17章第271段
2026-01-28 13:07:05,333 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=279 corrected=False final=279
2026-01-28 13:07:05,333 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第17章第279段
2026-01-28 13:07:05,346 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=12 corrected=False final=12
2026-01-28 13:07:05,346 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第21章第12段
2026-01-28 13:07:05,355 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=14 corrected=False final=14
2026-01-28 13:07:05,355 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第21章第14段
2026-01-28 13:07:05,365 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=16 corrected=False final=16
2026-01-28 13:07:05,365 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第21章第16段
2026-01-28 13:07:05,373 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=17 corrected=False final=17
2026-01-28 13:07:05,374 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第21章第17段
2026-01-28 13:07:05,384 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=19 corrected=False final=19
2026-01-28 13:07:05,385 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第21章第19段
2026-01-28 13:07:05,394 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=23 corrected=False final=23
2026-01-28 13:07:05,394 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第21章第23段
2026-01-28 13:07:05,398 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=24 corrected=False final=24
2026-01-28 13:07:05,398 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第21章第24段
2026-01-28 13:07:05,415 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=26 corrected=False final=26
2026-01-28 13:07:05,415 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第21章第26段
2026-01-28 13:07:05,428 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=29 corrected=False final=29
2026-01-28 13:07:05,428 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第21章第29段
2026-01-28 13:07:05,438 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=30 corrected=False final=30
2026-01-28 13:07:05,439 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第21章第30段
2026-01-28 13:07:05,450 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=35 corrected=False final=35
2026-01-28 13:07:05,456 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第21章第35段
2026-01-28 13:07:05,465 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=41 corrected=False final=41
2026-01-28 13:07:05,465 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第21章第41段
2026-01-28 13:07:05,478 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=43 corrected=False final=43
2026-01-28 13:07:05,478 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第21章第43段
2026-01-28 13:07:05,486 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=41 corrected=False final=41
2026-01-28 13:07:05,486 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第22章第41段
2026-01-28 13:07:05,498 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=40 corrected=False final=40
2026-01-28 13:07:05,498 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第44章第40段
2026-01-28 13:07:05,508 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=177 corrected=False final=177
2026-01-28 13:07:05,509 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第49章第177段
2026-01-28 13:07:05,515 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=180 corrected=False final=180
2026-01-28 13:07:05,515 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第49章第180段
2026-01-28 13:07:05,532 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=181 corrected=False final=181
2026-01-28 13:07:05,532 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第49章第181段
2026-01-28 13:07:05,547 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=183 corrected=False final=183
2026-01-28 13:07:05,548 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第49章第183段
2026-01-28 13:07:05,560 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=184 corrected=False final=184
2026-01-28 13:07:05,560 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第49章第184段
2026-01-28 13:07:05,573 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=185 corrected=False final=185
2026-01-28 13:07:05,573 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第49章第185段
2026-01-28 13:07:05,589 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=186 corrected=False final=186
2026-01-28 13:07:05,590 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第49章第186段
2026-01-28 13:07:05,598 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=187 corrected=False final=187
2026-01-28 13:07:05,598 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第49章第187段
2026-01-28 13:07:05,616 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=188 corrected=False final=188
2026-01-28 13:07:05,616 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第49章第188段
2026-01-28 13:07:05,630 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=193 corrected=False final=193
2026-01-28 13:07:05,630 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第49章第193段
2026-01-28 13:07:05,640 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=194 corrected=False final=194
2026-01-28 13:07:05,641 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第49章第194段
2026-01-28 13:07:05,648 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=196 corrected=False final=196
2026-01-28 13:07:05,648 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第49章第196段
2026-01-28 13:07:05,668 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=199 corrected=False final=199
2026-01-28 13:07:05,668 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第49章第199段
2026-01-28 13:07:05,668 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=34 keywords=交易,王家
2026-01-28 13:07:05,668 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-28 13:07:05,673 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-28 13:07:08,282 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 13:07:08,282 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-28 13:07:08,300 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 13:07:08,307 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1194, cost=$0.000631, time=2609ms
2026-01-28 13:07:08,309 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=251, 尝试次数=1
2026-01-28 13:07:08,309 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"work_id": "林仙", "keywords": ["药材", "成仙"], "match_mode": "and", "limit": 50}
2026-01-28 13:07:08,389 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['药材', '成仙']..., mode=any, range=None, hits=50
2026-01-28 13:07:08,399 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=86 corrected=False final=86
2026-01-28 13:07:08,400 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第86段
2026-01-28 13:07:08,406 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=17 corrected=False final=17
2026-01-28 13:07:08,406 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第17段
2026-01-28 13:07:08,414 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=83 corrected=False final=83
2026-01-28 13:07:08,416 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第5章第83段
2026-01-28 13:07:08,424 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=50 corrected=False final=50
2026-01-28 13:07:08,424 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第6章第50段
2026-01-28 13:07:08,432 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=16 corrected=False final=16
2026-01-28 13:07:08,432 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第7章第16段
2026-01-28 13:07:08,443 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=19 corrected=False final=19
2026-01-28 13:07:08,443 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第14章第19段
2026-01-28 13:07:08,451 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=63 corrected=False final=63
2026-01-28 13:07:08,451 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第14章第63段
2026-01-28 13:07:08,467 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=64 corrected=False final=64
2026-01-28 13:07:08,467 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第14章第64段
2026-01-28 13:07:08,474 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=68 corrected=False final=68
2026-01-28 13:07:08,474 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第14章第68段
2026-01-28 13:07:08,484 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=58 corrected=False final=58
2026-01-28 13:07:08,484 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第16章第58段
2026-01-28 13:07:08,492 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=4 corrected=False final=4
2026-01-28 13:07:08,492 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第17章第4段
2026-01-28 13:07:08,507 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=19 corrected=False final=19
2026-01-28 13:07:08,508 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第17章第19段
2026-01-28 13:07:08,519 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=21 corrected=False final=21
2026-01-28 13:07:08,519 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第17章第21段
2026-01-28 13:07:08,523 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=25 corrected=False final=25
2026-01-28 13:07:08,523 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第17章第25段
2026-01-28 13:07:08,540 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=219 corrected=False final=219
2026-01-28 13:07:08,540 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第17章第219段
2026-01-28 13:07:08,550 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=220 corrected=False final=220
2026-01-28 13:07:08,551 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第17章第220段
2026-01-28 13:07:08,556 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=275 corrected=False final=275
2026-01-28 13:07:08,556 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第17章第275段
2026-01-28 13:07:08,573 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=280 corrected=False final=280
2026-01-28 13:07:08,574 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第17章第280段
2026-01-28 13:07:08,583 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=282 corrected=False final=282
2026-01-28 13:07:08,585 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第17章第282段
2026-01-28 13:07:08,595 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=283 corrected=False final=283
2026-01-28 13:07:08,596 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第17章第283段
2026-01-28 13:07:08,607 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=284 corrected=False final=284
2026-01-28 13:07:08,607 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第17章第284段
2026-01-28 13:07:08,619 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=116 corrected=False final=116
2026-01-28 13:07:08,619 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第18章第116段
2026-01-28 13:07:08,631 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=4 corrected=False final=4
2026-01-28 13:07:08,631 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第22章第4段
2026-01-28 13:07:08,640 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=12 corrected=False final=12
2026-01-28 13:07:08,640 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第22章第12段
2026-01-28 13:07:08,652 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=14 corrected=False final=14
2026-01-28 13:07:08,652 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第22章第14段
2026-01-28 13:07:08,665 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=15 corrected=False final=15
2026-01-28 13:07:08,666 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第23章第15段
2026-01-28 13:07:08,666 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=47 keywords=药材,成仙
2026-01-28 13:07:08,666 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 探索完成(工具循环): 5轮, 原因=达到读取上限
2026-01-28 13:07:08,678 - app.services.agent.execution.tool_executor - INFO - [StandardTool] explore_content 执行成功
2026-01-28 13:07:08,682 - app.api.v1.agent - INFO - [Stream] 任务完成: 检索林仙“布局十佬/交易王家/收集药材成仙”的原文证据。 (9.2s)
2026-01-28 13:07:08,683 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务2完成
2026-01-28 13:07:08,683 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务3开始: 检索“天凉了，让王家破产吧/汝从无生来，要往长生去”等价值观推进的证据。
2026-01-28 13:07:08,683 - app.api.v1.agent - INFO - [Stream] Task started: 检索“天凉了，让王家破产吧/汝从无生来，要往长生去”等价值观推进的证据。 (icon=Wrench)
2026-01-28 13:07:08,685 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: explore_content
2026-01-28 13:07:08,685 - app.services.agent.tools.explore_tools - INFO - [explore_content] 开始: work_id=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, target=查找“天凉了，让王家破产吧/汝从无生来，要往长生去”等价值观推进的证据...
2026-01-28 13:07:08,685 - app.services.agent.tools.explore_tools - INFO - [explore_content] 规划传入关键词: ['天凉了', '王家破产', '汝从无生来', '往长生去', '长生']
2026-01-28 13:07:08,685 - app.services.agent.tools.explore_tools - INFO - [explore_content] 复用共享状态: searched=6, read_paragraphs=120, read_chapters=0
2026-01-28 13:07:08,687 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 开始探索 V5: work_id=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, target=查找“天凉了，让王家破产吧/汝从无生来，要往长生去”等价值观推进的证据...
2026-01-28 13:07:08,687 - app.services.chapter_service - INFO - [ChapterService] Querying chapters for work_id=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, type=<class 'uuid.UUID'>
2026-01-28 13:07:08,703 - app.services.chapter_service - INFO - [ChapterService] Found 77 chapters
2026-01-28 13:07:08,703 - app.services.chapter_service - INFO -   - Chapter: 第1章 【摆烂的宿主】, order=1
2026-01-28 13:07:08,707 - app.services.chapter_service - INFO -   - ... (75 more chapters)
2026-01-28 13:07:08,709 - app.services.chapter_service - INFO -   - Chapter: 第100章 【火域铸真器，两脉起冲突】, order=77
2026-01-28 13:07:08,756 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 强制流程步骤: list_chapters
2026-01-28 13:07:08,758 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=list_chapters params={"work_id": "5fe6c67d-8a1b-48c1-ad56-a5281eb22e21"}
2026-01-28 13:07:08,758 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=list_chapters success=True count=77
2026-01-28 13:07:08,759 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 强制流程步骤: list_paragraphs
2026-01-28 13:07:08,759 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=list_paragraphs params={"chapter_order": 1, "offset": 0, "limit": 50, "preview_len": 80, "work_id": "5fe6c67d-8a1b-48c1-ad56-a5281eb22e21"}
2026-01-28 13:07:08,777 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=list_paragraphs success=True chapter=1 offset=0 limit=50 approximate=None
2026-01-28 13:07:08,778 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-28 13:07:08,779 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-28 13:07:11,282 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 13:07:11,283 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-28 13:07:11,297 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 13:07:11,298 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1510, cost=$0.000752, time=2504ms
2026-01-28 13:07:11,298 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=258, 尝试次数=1
2026-01-28 13:07:11,298 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"work_id": "5fe6c67d-8a1b-48c1-ad56-a5281eb22e21", "keywords": "天凉了，让王家破产吧", "match_mode": "exact", "limit": 10}
2026-01-28 13:07:11,356 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['天凉了，让王家破产吧']..., mode=any, range=None, hits=1
2026-01-28 13:07:11,368 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=14 corrected=False final=14
2026-01-28 13:07:11,369 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第21章第14段
2026-01-28 13:07:11,369 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=1 keywords=天凉了，让王家破产吧
2026-01-28 13:07:11,369 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-28 13:07:11,369 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-28 13:07:14,534 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 13:07:14,534 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-28 13:07:14,542 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 13:07:14,542 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=875, cost=$0.000538, time=3165ms
2026-01-28 13:07:14,542 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=265, 尝试次数=1
2026-01-28 13:07:14,542 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=read_paragraph params={"work_id": "default", "chapter_order": 21, "paragraph_index": 14, "context_before": 2, "context_after": 2}
2026-01-28 13:07:14,548 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=read_paragraph success=True chapter=21 paragraph=14 index_base=None
2026-01-28 13:07:14,548 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-28 13:07:14,548 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-28 13:07:17,114 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 13:07:17,114 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-28 13:07:17,125 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 13:07:17,126 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=810, cost=$0.000516, time=2565ms
2026-01-28 13:07:17,127 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=259, 尝试次数=1
2026-01-28 13:07:17,127 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"work_id": "work_id", "keywords": ["天凉了，让王家破产吧", "汝从无生来，要往长生去"], "match_mode": "exact", "limit": 10}
2026-01-28 13:07:17,181 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['汝从无生来，要往长生去']..., mode=any, range=None, hits=1
2026-01-28 13:07:17,193 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=33 corrected=False final=33
2026-01-28 13:07:17,198 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第20章第33段
2026-01-28 13:07:17,200 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=1 keywords=汝从无生来，要往长生去
2026-01-28 13:07:17,200 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-28 13:07:17,201 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-28 13:07:20,047 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 13:07:20,048 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-28 13:07:20,061 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 13:07:20,061 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=926, cost=$0.000579, time=2847ms
2026-01-28 13:07:20,061 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=284, 尝试次数=1
2026-01-28 13:07:20,061 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=read_paragraph params={"work_id": "work_id", "chapter_order": 20, "paragraph_index": 33, "context_before": 1, "context_after": 1}
2026-01-28 13:07:20,061 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=read_paragraph success=True chapter=20 paragraph=33 index_base=None
2026-01-28 13:07:20,061 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-28 13:07:20,061 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-28 13:07:28,130 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 13:07:28,130 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-28 13:07:28,135 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 13:07:28,144 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1693, cost=$0.000763, time=8070ms
2026-01-28 13:07:28,144 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=236, 尝试次数=1
2026-01-28 13:07:28,145 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"work_id": 1, "keywords": ["天凉了，让王家破产吧"], "match_mode": "all", "limit": 20}
2026-01-28 13:07:28,177 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['天凉了，让王家破产吧']..., mode=all, range=None, hits=1
2026-01-28 13:07:28,177 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=1 keywords=天凉了，让王家破产吧
2026-01-28 13:07:28,177 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-28 13:07:28,177 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-28 13:07:30,978 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 13:07:30,978 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-28 13:07:30,990 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 13:07:30,991 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1023, cost=$0.000595, time=2800ms
2026-01-28 13:07:30,991 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=268, 尝试次数=1
2026-01-28 13:07:30,993 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=read_paragraph params={"work_id": 1, "chapter_order": 21, "paragraph_index": 14, "context_before": 5, "context_after": 5}
2026-01-28 13:07:30,993 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=read_paragraph success=True chapter=21 paragraph=14 index_base=None
2026-01-28 13:07:30,994 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-28 13:07:30,994 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-28 13:07:40,371 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 13:07:40,373 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-28 13:07:40,392 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 13:07:40,393 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2129, cost=$0.000936, time=9379ms
2026-01-28 13:07:40,394 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=265, 尝试次数=1
2026-01-28 13:07:40,394 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"work_id": "all", "keywords": "破产", "match_mode": "all", "limit": 100}
2026-01-28 13:07:40,427 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['破产']..., mode=all, range=None, hits=1
2026-01-28 13:07:40,431 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=1 keywords=破产
2026-01-28 13:07:40,432 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-28 13:07:40,432 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-28 13:07:43,507 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 13:07:43,508 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-28 13:07:43,527 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 13:07:43,527 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=985, cost=$0.000577, time=3076ms
2026-01-28 13:07:43,529 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=263, 尝试次数=1
2026-01-28 13:07:43,529 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=read_paragraph params={"work_id": 1, "chapter_order": 21, "paragraph_index": 14, "context_before": 5, "context_after": 5}
2026-01-28 13:07:43,529 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=read_paragraph success=True chapter=21 paragraph=14 index_base=None
2026-01-28 13:07:43,529 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-28 13:07:43,529 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-28 13:07:48,002 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 13:07:48,002 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-28 13:07:48,020 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 13:07:48,020 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1134, cost=$0.000556, time=4472ms
2026-01-28 13:07:48,020 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=209, 尝试次数=1
2026-01-28 13:07:48,020 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"work_id": 1, "keywords": "天凉了，让王家破产吧", "match_mode": "exact", "limit": 10}
2026-01-28 13:07:48,059 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['天凉了，让王家破产吧']..., mode=any, range=None, hits=1
2026-01-28 13:07:48,059 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=1 keywords=天凉了，让王家破产吧
2026-01-28 13:07:48,062 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-28 13:07:48,062 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-28 13:07:51,452 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 13:07:51,452 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-28 13:07:51,465 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 13:07:51,473 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=936, cost=$0.000562, time=3390ms
2026-01-28 13:07:51,473 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=271, 尝试次数=1
2026-01-28 13:07:51,473 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=read_paragraph params={"work_id": "default", "chapter_order": 21, "paragraph_index": 14, "context_before": 5, "context_after": 5}
2026-01-28 13:07:51,474 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=read_paragraph success=True chapter=21 paragraph=14 index_base=None
2026-01-28 13:07:51,474 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-28 13:07:51,474 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-28 13:08:05,306 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 13:08:05,306 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-28 13:08:05,323 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 13:08:05,323 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2932, cost=$0.001194, time=13832ms
2026-01-28 13:08:05,323 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=280, 尝试次数=1
2026-01-28 13:08:05,323 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"work_id": 1, "keywords": ["天凉了，让王家破产吧", "汝从无生来，要往长生去"], "match_mode": "or", "limit": 100}
2026-01-28 13:08:05,398 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['天凉了，让王家破产吧', '汝从无生来，要往长生去']..., mode=any, range=None, hits=2
2026-01-28 13:08:05,398 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=2 keywords=天凉了，让王家破产吧,汝从无生来，要往长生去
2026-01-28 13:08:05,398 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-28 13:08:05,398 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-28 13:08:07,779 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 13:08:07,780 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-28 13:08:07,790 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 13:08:07,799 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=987, cost=$0.000661, time=2382ms
2026-01-28 13:08:07,799 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=397, 尝试次数=1
2026-01-28 13:08:07,801 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=read_paragraphs params={"work_id": "default", "items": [{"chapter_order": 20, "paragraph_index": 33}, {"chapter_order": 21, "paragraph_index": 14}], "context_before": 5, "context_after": 5}
2026-01-28 13:08:07,801 - app.services.agent.langgraph_tools - INFO - [read_paragraphs] start items=2 index_base=zero
2026-01-28 13:08:07,817 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=33 corrected=False final=33
2026-01-28 13:08:07,817 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第20章第33段
2026-01-28 13:08:07,833 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=14 corrected=False final=14
2026-01-28 13:08:07,833 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第21章第14段
2026-01-28 13:08:07,833 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=read_paragraphs success=True count=2 index_base=zero
2026-01-28 13:08:07,833 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-28 13:08:07,839 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-28 13:08:17,128 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 13:08:17,128 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-28 13:08:17,135 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 13:08:17,139 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2392, cost=$0.001188, time=9288ms
2026-01-28 13:08:17,139 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=389, 尝试次数=1
2026-01-28 13:08:17,139 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=read_paragraphs params={"work_id": "5fe6c67d-8a1b-48c1-ad56-a5281eb22e21", "items": [{"chapter_id": "fca581f0-3bce-457a-830f-00efaf22ab8c", "paragraph_index": 12}], "context_before": 5, "context_after": 5}
2026-01-28 13:08:17,139 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=read_paragraphs success=False count=0 index_base=None
2026-01-28 13:08:17,139 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-28 13:08:17,139 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-28 13:08:21,424 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 13:08:21,424 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-28 13:08:21,442 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 13:08:21,442 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1191, cost=$0.000617, time=4284ms
2026-01-28 13:08:21,442 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=238, 尝试次数=1
2026-01-28 13:08:21,448 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"work_id": 1, "keywords": "天凉了，让王家破产吧", "match_mode": "exact", "limit": 100}
2026-01-28 13:08:21,508 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['天凉了，让王家破产吧']..., mode=any, range=None, hits=1
2026-01-28 13:08:21,514 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=1 keywords=天凉了，让王家破产吧
2026-01-28 13:08:21,514 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-28 13:08:21,514 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-28 13:08:24,458 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 13:08:24,458 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-28 13:08:24,473 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 13:08:24,474 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=996, cost=$0.000565, time=2944ms
2026-01-28 13:08:24,474 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=253, 尝试次数=1
2026-01-28 13:08:24,474 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=read_paragraph params={"work_id": 1, "chapter_order": 21, "paragraph_index": 14, "context_before": 5, "context_after": 5}
2026-01-28 13:08:24,474 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=read_paragraph success=True chapter=21 paragraph=14 index_base=None
2026-01-28 13:08:24,474 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-28 13:08:24,474 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-28 13:08:30,499 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 13:08:30,499 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-28 13:08:30,514 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 13:08:30,516 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1465, cost=$0.000715, time=6025ms
2026-01-28 13:08:30,516 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=256, 尝试次数=1
2026-01-28 13:08:30,516 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"work_id": 1, "keywords": ["天凉了，让王家破产吧", "汝从无生来，要往长生去"], "match_mode": "any", "limit": 50}
2026-01-28 13:08:30,581 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['天凉了，让王家破产吧', '汝从无生来，要往长生去']..., mode=any, range=None, hits=2
2026-01-28 13:08:30,581 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=2 keywords=天凉了，让王家破产吧,汝从无生来，要往长生去
2026-01-28 13:08:30,581 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-28 13:08:30,581 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-28 13:08:33,636 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 13:08:33,636 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-28 13:08:33,648 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 13:08:33,649 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1066, cost=$0.000672, time=3054ms
2026-01-28 13:08:33,650 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=387, 尝试次数=1
2026-01-28 13:08:33,650 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=read_paragraphs params={"work_id": "work_id", "items": [{"chapter_order": 20, "paragraph_index": 33}, {"chapter_order": 21, "paragraph_index": 14}], "context_before": 2, "context_after": 2}
2026-01-28 13:08:33,651 - app.services.agent.langgraph_tools - INFO - [read_paragraphs] start items=2 index_base=zero
2026-01-28 13:08:33,657 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=33 corrected=False final=33
2026-01-28 13:08:33,657 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第20章第33段
2026-01-28 13:08:33,668 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=14 corrected=False final=14
2026-01-28 13:08:33,668 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第21章第14段
2026-01-28 13:08:33,673 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=read_paragraphs success=True count=2 index_base=zero
2026-01-28 13:08:33,673 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-28 13:08:33,674 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-28 13:08:35,516 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 13:08:35,516 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-28 13:08:35,533 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 13:08:35,533 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1360, cost=$0.000516, time=1841ms
2026-01-28 13:08:35,533 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=106, 尝试次数=1
2026-01-28 13:08:35,533 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 探索完成(工具循环): 19轮, 原因=已找到目标任务中提及的两个价值观的直接证据，并已通过read_paragraphs工具获取原文。无需进一步探索。
2026-01-28 13:08:35,541 - app.services.agent.execution.tool_executor - INFO - [StandardTool] explore_content 执行成功
2026-01-28 13:08:35,543 - app.api.v1.agent - INFO - [Stream] 任务完成: 检索“天凉了，让王家破产吧/汝从无生来，要往长生去”等价值观推进的证据。 (86.9s)
2026-01-28 13:08:35,543 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务3完成
2026-01-28 13:08:35,545 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务4开始: 检索“道生一/先天一炁/天帝代打/六库仙贼”对修行路径的强化证据。
2026-01-28 13:08:35,547 - app.api.v1.agent - INFO - [Stream] Task started: 检索“道生一/先天一炁/天帝代打/六库仙贼”对修行路径的强化证据。 (icon=Wrench)
2026-01-28 13:08:35,547 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: explore_content
2026-01-28 13:08:35,548 - app.services.agent.tools.explore_tools - INFO - [explore_content] 开始: work_id=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, target=查找“道生一/先天一炁/天帝代打/六库仙贼”对修行路径的强化证据...
2026-01-28 13:08:35,548 - app.services.agent.tools.explore_tools - INFO - [explore_content] 规划传入关键词: ['道生一', '先天一炁', '天帝代打', '六库仙贼', '修行']
2026-01-28 13:08:35,548 - app.services.agent.tools.explore_tools - INFO - [explore_content] 复用共享状态: searched=9, read_paragraphs=121, read_chapters=0
2026-01-28 13:08:35,548 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 开始探索 V5: work_id=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, target=查找“道生一/先天一炁/天帝代打/六库仙贼”对修行路径的强化证据...
2026-01-28 13:08:35,548 - app.services.chapter_service - INFO - [ChapterService] Querying chapters for work_id=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, type=<class 'uuid.UUID'>
2026-01-28 13:08:35,559 - app.services.chapter_service - INFO - [ChapterService] Found 77 chapters
2026-01-28 13:08:35,559 - app.services.chapter_service - INFO -   - Chapter: 第1章 【摆烂的宿主】, order=1
2026-01-28 13:08:35,559 - app.services.chapter_service - INFO -   - ... (75 more chapters)
2026-01-28 13:08:35,559 - app.services.chapter_service - INFO -   - Chapter: 第100章 【火域铸真器，两脉起冲突】, order=77
2026-01-28 13:08:35,600 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 强制流程步骤: list_chapters
2026-01-28 13:08:35,605 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=list_chapters params={"work_id": "5fe6c67d-8a1b-48c1-ad56-a5281eb22e21"}
2026-01-28 13:08:35,606 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=list_chapters success=True count=77
2026-01-28 13:08:35,606 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 强制流程步骤: list_paragraphs
2026-01-28 13:08:35,606 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=list_paragraphs params={"chapter_order": 1, "offset": 0, "limit": 50, "preview_len": 80, "work_id": "5fe6c67d-8a1b-48c1-ad56-a5281eb22e21"}
2026-01-28 13:08:35,618 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=list_paragraphs success=True chapter=1 offset=0 limit=50 approximate=None
2026-01-28 13:08:35,618 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-28 13:08:35,618 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-28 13:08:38,606 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 13:08:38,606 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-28 13:08:38,615 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 13:08:38,622 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1573, cost=$0.000791, time=2989ms
2026-01-28 13:08:38,623 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=275, 尝试次数=1
2026-01-28 13:08:38,623 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"work_id": "5fe6c67d-8a1b-48c1-ad56-a5281eb22e21", "keywords": "道生一|先天一炁|天帝代打|六库仙贼", "match_mode": "contains", "limit": 50}
2026-01-28 13:08:38,668 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['道生一|先天一炁|天帝代打|六库仙贼']..., mode=any, range=None, hits=0
2026-01-28 13:08:38,668 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=0 keywords=道生一|先天一炁|天帝代打|六库仙贼
2026-01-28 13:08:38,668 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-28 13:08:38,670 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-28 13:08:46,110 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 13:08:46,111 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-28 13:08:46,123 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 13:08:46,123 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1593, cost=$0.000742, time=7440ms
2026-01-28 13:08:46,125 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=255, 尝试次数=1
2026-01-28 13:08:46,125 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"work_id": 1, "keywords": ["道生一"], "match_mode": "exact", "limit": 10}
2026-01-28 13:08:46,158 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['道生一']..., mode=any, range=None, hits=7
2026-01-28 13:08:46,169 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=38 corrected=False final=38
2026-01-28 13:08:46,169 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第23章第38段
2026-01-28 13:08:46,180 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=46 corrected=False final=46
2026-01-28 13:08:46,180 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第23章第46段
2026-01-28 13:08:46,190 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=0 corrected=False final=0
2026-01-28 13:08:46,191 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第24章第0段
2026-01-28 13:08:46,201 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=6 corrected=False final=6
2026-01-28 13:08:46,201 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第24章第6段
2026-01-28 13:08:46,208 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=21 corrected=False final=21
2026-01-28 13:08:46,208 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第24章第21段
2026-01-28 13:08:46,223 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=2 corrected=False final=2
2026-01-28 13:08:46,224 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第25章第2段
2026-01-28 13:08:46,234 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=225 corrected=False final=225
2026-01-28 13:08:46,235 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第53章第225段
2026-01-28 13:08:46,236 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=7 keywords=道生一
2026-01-28 13:08:46,236 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-28 13:08:46,236 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-28 13:08:51,986 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 13:08:51,987 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-28 13:08:51,998 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 13:08:52,001 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1578, cost=$0.000843, time=5751ms
2026-01-28 13:08:52,002 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=395, 尝试次数=1
2026-01-28 13:08:52,002 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=read_paragraphs params={"work_id": "default", "items": [{"chapter_order": 23, "paragraph_index": 46}, {"chapter_order": 24, "paragraph_index": 21}], "context_before": 1, "context_after": 1}
2026-01-28 13:08:52,002 - app.services.agent.langgraph_tools - INFO - [read_paragraphs] start items=2 index_base=zero
2026-01-28 13:08:52,016 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=46 corrected=False final=46
2026-01-28 13:08:52,016 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第23章第46段
2026-01-28 13:08:52,028 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=21 corrected=False final=21
2026-01-28 13:08:52,029 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第24章第21段
2026-01-28 13:08:52,030 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=read_paragraphs success=True count=2 index_base=zero
2026-01-28 13:08:52,031 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-28 13:08:52,031 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-28 13:08:58,017 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 13:08:58,017 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-28 13:08:58,031 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 13:08:58,031 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2214, cost=$0.001029, time=5985ms
2026-01-28 13:08:58,031 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=298, 尝试次数=1
2026-01-28 13:08:58,037 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"work_id": "5fe6c67d-8a1b-48c1-ad56-a5281eb22e21", "keywords": "道生一|先天一炁|天帝代打|六库仙贼", "match_mode": "or", "limit": 20}
2026-01-28 13:08:58,081 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['道生一|先天一炁|天帝代打|六库仙贼']..., mode=any, range=None, hits=0
2026-01-28 13:08:58,081 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=0 keywords=道生一|先天一炁|天帝代打|六库仙贼
2026-01-28 13:08:58,081 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-28 13:08:58,081 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-28 13:09:04,720 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 13:09:04,721 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-28 13:09:04,740 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 13:09:04,741 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1362, cost=$0.000668, time=6639ms
2026-01-28 13:09:04,743 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=251, 尝试次数=1
2026-01-28 13:09:04,743 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"work_id": "一人之下", "keywords": ["道生一"], "match_mode": "any", "limit": 100}
2026-01-28 13:09:04,782 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['道生一']..., mode=any, range=None, hits=7
2026-01-28 13:09:04,782 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=7 keywords=道生一
2026-01-28 13:09:04,782 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-28 13:09:04,782 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-28 13:09:08,274 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 13:09:08,275 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-28 13:09:08,287 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 13:09:08,289 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1401, cost=$0.000775, time=3493ms
2026-01-28 13:09:08,289 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=382, 尝试次数=1
2026-01-28 13:09:08,290 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=read_paragraphs params={"work_id": "default", "items": [{"chapter_order": 23, "paragraph_index": 46}, {"chapter_order": 24, "paragraph_index": 21}], "context_before": 2, "context_after": 2}
2026-01-28 13:09:08,291 - app.services.agent.langgraph_tools - INFO - [read_paragraphs] start items=2 index_base=zero
2026-01-28 13:09:08,302 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=46 corrected=False final=46
2026-01-28 13:09:08,302 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第23章第46段
2026-01-28 13:09:08,316 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=21 corrected=False final=21
2026-01-28 13:09:08,316 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第24章第21段
2026-01-28 13:09:08,319 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=read_paragraphs success=True count=2 index_base=zero
2026-01-28 13:09:08,322 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-28 13:09:08,322 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-28 13:09:15,437 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 13:09:15,437 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-28 13:09:15,455 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 13:09:15,456 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2468, cost=$0.001108, time=7114ms
2026-01-28 13:09:15,458 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=303, 尝试次数=1
2026-01-28 13:09:15,458 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"work_id": "5fe6c67d-8a1b-48c1-ad56-a5281eb22e21", "keywords": "道生一|先天一炁|天帝代打|六库仙贼", "match_mode": "or", "limit": 20}
2026-01-28 13:09:15,498 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['道生一|先天一炁|天帝代打|六库仙贼']..., mode=any, range=None, hits=0
2026-01-28 13:09:15,500 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=0 keywords=道生一|先天一炁|天帝代打|六库仙贼
2026-01-28 13:09:15,500 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-28 13:09:15,500 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-28 13:09:23,629 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 13:09:23,629 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-28 13:09:23,643 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 13:09:23,643 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1979, cost=$0.000959, time=8129ms
2026-01-28 13:09:23,643 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=339, 尝试次数=1
2026-01-28 13:09:23,643 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"work_id": "一", "keywords": ["道生一", "先天一炁", "天帝代打", "六库仙贼"], "match_mode": "any", "limit": 100}
2026-01-28 13:09:23,747 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['先天一炁', '天帝代打', '六库仙贼']..., mode=any, range=None, hits=42
2026-01-28 13:09:23,761 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=49 corrected=False final=49
2026-01-28 13:09:23,762 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第16章第49段
2026-01-28 13:09:23,772 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=50 corrected=False final=50
2026-01-28 13:09:23,772 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第16章第50段
2026-01-28 13:09:23,781 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=55 corrected=False final=55
2026-01-28 13:09:23,785 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第16章第55段
2026-01-28 13:09:23,790 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=48 corrected=False final=48
2026-01-28 13:09:23,790 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第17章第48段
2026-01-28 13:09:23,809 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=51 corrected=False final=51
2026-01-28 13:09:23,809 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第17章第51段
2026-01-28 13:09:23,820 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=54 corrected=False final=54
2026-01-28 13:09:23,820 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第17章第54段
2026-01-28 13:09:23,831 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=63 corrected=False final=63
2026-01-28 13:09:23,831 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第17章第63段
2026-01-28 13:09:23,841 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=65 corrected=False final=65
2026-01-28 13:09:23,847 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第17章第65段
2026-01-28 13:09:23,851 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=70 corrected=False final=70
2026-01-28 13:09:23,851 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第17章第70段
2026-01-28 13:09:23,872 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=296 corrected=False final=296
2026-01-28 13:09:23,872 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第17章第296段
2026-01-28 13:09:23,883 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=17 corrected=False final=17
2026-01-28 13:09:23,885 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第19章第17段
2026-01-28 13:09:23,898 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=52 corrected=False final=52
2026-01-28 13:09:23,898 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第21章第52段
2026-01-28 13:09:23,906 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=39 corrected=False final=39
2026-01-28 13:09:23,906 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第23章第39段
2026-01-28 13:09:23,924 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=63 corrected=False final=63
2026-01-28 13:09:23,924 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第23章第63段
2026-01-28 13:09:23,939 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=15 corrected=False final=15
2026-01-28 13:09:23,939 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第24章第15段
2026-01-28 13:09:23,948 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=63 corrected=False final=63
2026-01-28 13:09:23,948 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第24章第63段
2026-01-28 13:09:23,965 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=0 corrected=False final=0
2026-01-28 13:09:23,966 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第25章第0段
2026-01-28 13:09:23,977 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=1 corrected=False final=1
2026-01-28 13:09:23,977 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第25章第1段
2026-01-28 13:09:23,986 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=3 corrected=False final=3
2026-01-28 13:09:23,986 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第25章第3段
2026-01-28 13:09:23,990 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=17 corrected=False final=17
2026-01-28 13:09:23,990 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第25章第17段
2026-01-28 13:09:24,006 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=36 corrected=False final=36
2026-01-28 13:09:24,006 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第25章第36段
2026-01-28 13:09:24,009 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=52 corrected=False final=52
2026-01-28 13:09:24,009 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第25章第52段
2026-01-28 13:09:24,023 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=19 corrected=False final=19
2026-01-28 13:09:24,023 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第26章第19段
2026-01-28 13:09:24,036 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=23 corrected=False final=23
2026-01-28 13:09:24,040 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第26章第23段
2026-01-28 13:09:24,050 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=45 corrected=False final=45
2026-01-28 13:09:24,050 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第26章第45段
2026-01-28 13:09:24,050 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=47 corrected=False final=47
2026-01-28 13:09:24,060 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第26章第47段
2026-01-28 13:09:24,064 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=55 corrected=False final=55
2026-01-28 13:09:24,064 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第26章第55段
2026-01-28 13:09:24,073 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=31 corrected=False final=31
2026-01-28 13:09:24,073 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第28章第31段
2026-01-28 13:09:24,088 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=14 corrected=False final=14
2026-01-28 13:09:24,088 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第14段
2026-01-28 13:09:24,098 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=35 corrected=False final=35
2026-01-28 13:09:24,098 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第35段
2026-01-28 13:09:24,107 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=20 corrected=False final=20
2026-01-28 13:09:24,107 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第36章第20段
2026-01-28 13:09:24,122 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=21 corrected=False final=21
2026-01-28 13:09:24,123 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第36章第21段
2026-01-28 13:09:24,133 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=35 corrected=False final=35
2026-01-28 13:09:24,133 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第36章第35段
2026-01-28 13:09:24,143 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=38 corrected=False final=38
2026-01-28 13:09:24,144 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第36章第38段
2026-01-28 13:09:24,147 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=63 corrected=False final=63
2026-01-28 13:09:24,154 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第76章第63段
2026-01-28 13:09:24,154 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=37 keywords=先天一炁,天帝代打,六库仙贼
2026-01-28 13:09:24,154 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-28 13:09:24,154 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-28 13:09:30,970 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 13:09:30,971 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-28 13:09:30,986 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 13:09:30,986 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2098, cost=$0.000907, time=6817ms
2026-01-28 13:09:30,986 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=264, 尝试次数=1
2026-01-28 13:09:30,989 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=read_paragraph params={"work_id": 1, "chapter_order": 17, "paragraph_index": 51, "context_before": 2, "context_after": 2}
2026-01-28 13:09:30,989 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=read_paragraph success=True chapter=17 paragraph=51 index_base=None
2026-01-28 13:09:30,989 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-28 13:09:30,989 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-28 13:09:37,537 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 13:09:37,537 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-28 13:09:37,555 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 13:09:37,556 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1521, cost=$0.000714, time=6550ms
2026-01-28 13:09:37,556 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=236, 尝试次数=1
2026-01-28 13:09:37,556 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"work_id": 1, "keywords": "道生一|先天一炁|天帝代打|六库仙贼", "match_mode": "or", "limit": 100}
2026-01-28 13:09:37,597 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['道生一|先天一炁|天帝代打|六库仙贼']..., mode=any, range=None, hits=0
2026-01-28 13:09:37,597 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=0 keywords=道生一|先天一炁|天帝代打|六库仙贼
2026-01-28 13:09:37,597 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-28 13:09:37,597 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-28 13:09:49,382 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 13:09:49,382 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-28 13:09:49,398 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 13:09:49,398 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2379, cost=$0.000969, time=11786ms
2026-01-28 13:09:49,398 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=246, 尝试次数=1
2026-01-28 13:09:49,398 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"work_id": 1, "keywords": ["先天一炁"], "match_mode": "any", "limit": 100}
2026-01-28 13:09:49,440 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['先天一炁']..., mode=any, range=None, hits=10
2026-01-28 13:09:49,442 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=10 keywords=先天一炁
2026-01-28 13:09:49,443 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-28 13:09:49,443 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-28 13:09:54,218 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 13:09:54,220 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-28 13:09:54,237 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 13:09:54,239 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1579, cost=$0.000936, time=4776ms
2026-01-28 13:09:54,239 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=483, 尝试次数=1
2026-01-28 13:09:54,240 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=read_paragraphs params={"work_id": "default", "items": [{"chapter_order": 23, "paragraph_index": 39}, {"chapter_order": 23, "paragraph_index": 46}, {"chapter_order": 24, "paragraph_index": 15}], "context_before": 2, "context_after": 2}
2026-01-28 13:09:54,242 - app.services.agent.langgraph_tools - INFO - [read_paragraphs] start items=3 index_base=zero
2026-01-28 13:09:54,252 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=39 corrected=False final=39
2026-01-28 13:09:54,253 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第23章第39段
2026-01-28 13:09:54,260 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=46 corrected=False final=46
2026-01-28 13:09:54,260 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第23章第46段
2026-01-28 13:09:54,273 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=15 corrected=False final=15
2026-01-28 13:09:54,274 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第24章第15段
2026-01-28 13:09:54,275 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=read_paragraphs success=True count=3 index_base=zero
2026-01-28 13:09:54,276 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-28 13:09:54,276 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-28 13:10:03,993 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 13:10:03,993 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-28 13:10:04,006 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 13:10:04,006 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2662, cost=$0.001137, time=9716ms
2026-01-28 13:10:04,006 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=279, 尝试次数=1
2026-01-28 13:10:04,006 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"work_id": "5fe6c67d-8a1b-48c1-ad56-a5281eb22e21", "keywords": "天帝代打|六库仙贼", "match_mode": "any", "limit": 10}
2026-01-28 13:10:04,047 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['天帝代打|六库仙贼']..., mode=any, range=None, hits=0
2026-01-28 13:10:04,048 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=0 keywords=天帝代打|六库仙贼
2026-01-28 13:10:04,049 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-28 13:10:04,049 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-28 13:10:18,550 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 13:10:18,550 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-28 13:10:18,567 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 13:10:18,570 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=3196, cost=$0.001249, time=14501ms
2026-01-28 13:10:18,570 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=266, 尝试次数=1
2026-01-28 13:10:18,572 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"work_id": 1, "keywords": ["道生一", "修行"], "match_mode": "and", "limit": 10}
2026-01-28 13:10:18,581 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['修行']..., mode=any, range=None, hits=10
2026-01-28 13:10:18,598 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=70 corrected=False final=70
2026-01-28 13:10:18,601 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第70段
2026-01-28 13:10:18,614 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=73 corrected=False final=73
2026-01-28 13:10:18,614 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第73段
2026-01-28 13:10:18,633 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=4 corrected=False final=4
2026-01-28 13:10:18,633 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第4段
2026-01-28 13:10:18,648 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=97 corrected=False final=97
2026-01-28 13:10:18,649 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第97段
2026-01-28 13:10:18,666 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=99 corrected=False final=99
2026-01-28 13:10:18,667 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第99段
2026-01-28 13:10:18,682 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=103 corrected=False final=103
2026-01-28 13:10:18,682 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第103段
2026-01-28 13:10:18,700 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=110 corrected=False final=110
2026-01-28 13:10:18,700 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第110段
2026-01-28 13:10:18,716 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=114 corrected=False final=114
2026-01-28 13:10:18,717 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第114段
2026-01-28 13:10:18,717 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=8 keywords=修行
2026-01-28 13:10:18,717 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-28 13:10:18,717 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-28 13:10:29,094 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 13:10:29,094 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-28 13:10:29,114 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 13:10:29,115 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2691, cost=$0.001131, time=10377ms
2026-01-28 13:10:29,117 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=293, 尝试次数=1
2026-01-28 13:10:29,117 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"work_id": "test_work_id", "keywords": ["道生一", "修行"], "match_mode": "and", "limit": 10}
2026-01-28 13:10:29,131 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['道生一', '修行']..., mode=any, range=None, hits=10
2026-01-28 13:10:29,134 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=8 keywords=道生一,修行
2026-01-28 13:10:29,135 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-28 13:10:29,135 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-28 13:10:39,881 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 13:10:39,881 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-28 13:10:39,897 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 13:10:39,898 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2744, cost=$0.001144, time=10745ms
2026-01-28 13:10:39,898 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=297, 尝试次数=1
2026-01-28 13:10:39,901 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"work_id": "work_id", "keywords": ["先天一炁"], "match_mode": "and", "limit": 10}
2026-01-28 13:10:39,938 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['先天一炁']..., mode=any, range=None, hits=10
2026-01-28 13:10:39,940 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=10 keywords=先天一炁
2026-01-28 13:10:39,940 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-28 13:10:39,940 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-28 13:10:46,827 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 13:10:46,827 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-28 13:10:46,840 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 13:10:46,849 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1995, cost=$0.001067, time=6887ms
2026-01-28 13:10:46,849 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=493, 尝试次数=1
2026-01-28 13:10:46,849 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=read_paragraphs params={"work_id": "default", "items": [{"chapter_order": 21, "paragraph_index": 52}, {"chapter_order": 23, "paragraph_index": 39}, {"chapter_order": 24, "paragraph_index": 15}], "context_before": 2, "context_after": 2}
2026-01-28 13:10:46,849 - app.services.agent.langgraph_tools - INFO - [read_paragraphs] start items=2 index_base=zero
2026-01-28 13:10:46,865 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=52 corrected=False final=52
2026-01-28 13:10:46,869 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第21章第52段
2026-01-28 13:10:46,882 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=39 corrected=False final=39
2026-01-28 13:10:46,882 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第23章第39段
2026-01-28 13:10:46,890 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=read_paragraphs success=True count=2 index_base=zero
2026-01-28 13:10:46,890 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 探索完成(工具循环): 19轮, 原因=达到读取上限
2026-01-28 13:10:46,901 - app.services.agent.execution.tool_executor - INFO - [StandardTool] explore_content 执行成功
2026-01-28 13:10:46,907 - app.api.v1.agent - INFO - [Stream] 任务完成: 检索“道生一/先天一炁/天帝代打/六库仙贼”对修行路径的强化证据。 (131.4s)
2026-01-28 13:10:46,907 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务4完成
2026-01-28 13:10:46,907 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共4个任务，耗时: 235.14s
2026-01-28 13:10:46,907 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2026-01-28 13:10:46,911 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=4, 展示型=0
2026-01-28 13:10:46,911 - app.services.agent.langgraph_agent - INFO - [Response] 4个输出任务（含续写），使用AI整合
2026-01-28 13:10:46,911 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2026-01-28 13:10:46,911 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=4, 展示型=0
2026-01-28 13:10:46,914 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=9566字符, 处理后=9698字符
2026-01-28 13:10:46,914 - app.services.agent.planning.response_builder - INFO - [Summarization] 准备发送 summarization_start 事件
2026-01-28 13:10:46,915 - app.services.agent.stream.stream_event_handler - INFO - [StreamEventHandler] emit_summarization_start 被调用, _on_flow_event=True
2026-01-28 13:10:46,915 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_start 事件已发送
2026-01-28 13:10:46,915 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2026-01-28 13:10:46,915 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2026-01-28 13:10:46,925 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-28 13:10:46,925 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-28 13:10:46,925 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
2026-01-28 13:11:30,025 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-28 13:11:30,025 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_complete 事件已发送（第一个chunk时）
2026-01-28 13:11:30,025 - app.services.agent.planning.response_builder - INFO - [Summarization] output_ready 事件已发送（第一个chunk时）
2026-01-28 13:11:50,427 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 60 个数据块，总长度: 5374
2026-01-28 13:11:50,428 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 27449 (prompt=23538, completion=3911)
2026-01-28 13:11:50,429 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 13:11:50,430 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-28 13:11:50,452 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 13:11:50,454 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=27449, cost=$0.016839, time=63504ms
2026-01-28 13:11:50,454 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=5374
2026-01-28 13:11:51,622 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21 | 重要度=0.84
2026-01-28 13:11:52,572 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21 | 重要度=0.60
2026-01-28 13:11:52,583 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21:26e13e5c-f8ea-4efd-88c1-03bb694d0510, token=5724
2026-01-28 13:11:52,588 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21:26e13e5c-f8ea-4efd-88c1-03bb694d0510, 消息数=2, 摘要长度=0, Token=5724
2026-01-28 13:11:52,588 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21:26e13e5c-f8ea-4efd-88c1-03bb694d0510)
2026-01-28 13:11:52,589 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2026-01-28 13:11:52,597 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed
2026-01-28 13:12:15,972 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/auth/refresh
INFO:     127.0.0.1:61322 - "POST /api/v1/auth/refresh HTTP/1.1" 200 OK
2026-01-28 13:12:23,934 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/26e13e5c-f8ea-4efd-88c1-03bb694d0510
INFO:     127.0.0.1:49598 - "GET /api/v1/agent/operations/26e13e5c-f8ea-4efd-88c1-03bb694d0510 HTTP/1.1" 200 OK
2026-01-28 13:14:16,629 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:56431 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2026-01-28 13:14:33,156 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:51163 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2026-01-28 13:14:33,180 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-28 13:14:33,180 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-28 13:14:33,181 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2026-01-28 13:14:34,772 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz:8443/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-28 13:14:34,773 - app.api.v1.agent - INFO - [Chat Stream] Mode: planning
2026-01-28 13:14:34,775 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:62038 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2026-01-28 13:14:34,787 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 目标：构建一条完整因果链：
  ‘摆烂/躺平动机’ → 泰山/九龙拉棺冲击 → 系统10086态度变...
2026-01-28 13:14:34,804 - app.api.v1.agent - INFO - [agent_chat_stream] 📚 世界观数据已注入: 人物=8, 地点=7, 设定=7, 规范=无
2026-01-28 13:14:34,804 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21:60055cd5-3851-46ac-b14c-8d6b99aa1db9 (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, conversation_id=60055cd5-3851-46ac-b14c-8d6b99aa1db9)
2026-01-28 13:14:34,811 - app.services.context.manager - INFO - [ContextManager] 创建新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21:60055cd5-3851-46ac-b14c-8d6b99aa1db9
2026-01-28 13:14:34,811 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21:60055cd5-3851-46ac-b14c-8d6b99aa1db9: 0/16000 tokens
2026-01-28 13:14:34,978 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='目标：构建一条完整因果链：
  ‘摆烂/躺平动机’ → 泰山...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=3条
2026-01-28 13:14:34,980 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21 | 含用户级=True | 找到=3条
2026-01-28 13:14:34,982 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 1条消息, 0 tokens, 耗时 177.91ms
2026-01-28 13:14:34,982 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 1 条历史消息 (token: 0, has_summary: False)
2026-01-28 13:14:34,982 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-28 13:14:34,982 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-28 13:14:34,982 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=200, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-28 13:14:36,505 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 13:14:36,507 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-28 13:14:36,535 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 13:14:36,537 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=584, cost=$0.000064, time=1524ms
2026-01-28 13:14:36,537 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=39, 尝试次数=1
2026-01-28 13:14:36,538 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-28 13:14:36,538 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-28 13:14:36,540 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=20, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-28 13:14:37,618 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 13:14:37,618 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-28 13:14:37,634 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 13:14:37,634 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=512, cost=$0.000051, time=1079ms
2026-01-28 13:14:37,639 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=8, 尝试次数=1
2026-01-28 13:14:37,639 - app.services.agent.intent.classifier - INFO - [Intent] AI识别结果: planning
2026-01-28 13:14:37,639 - app.services.agent.langgraph_agent - INFO - [Planning] AI意图分类: planning (置信度: 0.90)
2026-01-28 13:14:37,639 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 目标：构建一条完整因果链：
  ‘摆烂/躺平动机’ → 泰山/九龙拉棺冲击 → 系统10086态度变...
2026-01-28 13:14:37,643 - app.core.cache - INFO - ⚠️ 缓存未命中: prompt:planning:v2.41.0:get_planning_static_prompt:fca6eb91156619d0
2026-01-28 13:14:37,652 - app.core.cache - INFO - 💾 缓存已保存: prompt:planning:v2.41.0:get_planning_static_prompt:fca6eb91156619d0 (expire=3600s)
2026-01-28 13:14:37,657 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-28 13:14:37,657 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=story_planning, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: story_planning; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-01-28 13:14:37,657 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.3, task_type=TaskType.STORY_PLANNING
2026-01-28 13:14:54,030 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-28 13:14:59,373 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 11 个数据块，总长度: 1209
2026-01-28 13:14:59,374 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 22192 (prompt=21565, completion=627)
2026-01-28 13:14:59,374 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 13:14:59,375 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-28 13:14:59,391 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 13:14:59,393 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=22192, cost=$0.033226, time=21716ms
2026-01-28 13:14:59,393 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=22192
2026-01-28 13:14:59,396 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户需要构建一条包含多个节点的完整因果链，并为每个节点提供原, 原料=需要从作品中检索与以下节点和锚点相关的所, 处理=使用 explore_content 工
2026-01-28 13:14:59,397 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共1个任务
2026-01-28 13:14:59,398 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共1个任务，耗时: 21.76s
2026-01-28 13:14:59,400 - app.api.v1.agent - INFO - [Stream] Plan tasks: 1 items
2026-01-28 13:14:59,400 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2026-01-28 13:14:59,400 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2026-01-28 13:14:59,401 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2026-01-28 13:14:59,401 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] DAG 调度启用，任务数=1, 有依赖任务=0
2026-01-28 13:14:59,402 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1开始: 根据用户提供的因果链节点和锚点，全面检索小说原文，收集所有相关证据。
2026-01-28 13:14:59,402 - app.api.v1.agent - INFO - [Stream] Task started: 根据用户提供的因果链节点和锚点，全面检索小说原文，收集所有相关证据。 (icon=Wrench)
2026-01-28 13:14:59,402 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: explore_content
2026-01-28 13:14:59,402 - app.services.agent.tools.explore_tools - INFO - [explore_content] 开始: work_id=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, target=构建一条从‘摆烂动机’到‘天帝代打’的完整因果链，并为每个节点查找原文证据，必须包含以下锚点：林仙提...
2026-01-28 13:14:59,402 - app.services.agent.tools.explore_tools - INFO - [explore_content] 规划传入关键词: ['摆烂', '躺平', '泰山', '九龙拉棺', '系统10086', '林仙', '天下会', '十佬名额', '王家下去', '冯曜']
2026-01-28 13:14:59,406 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 开始探索 V5: work_id=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, target=构建一条从‘摆烂动机’到‘天帝代打’的完整因果链，并为每个节点查找原文证据，必须包含以下锚点：林仙提...
2026-01-28 13:14:59,406 - app.services.chapter_service - INFO - [ChapterService] Querying chapters for work_id=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, type=<class 'uuid.UUID'>
2026-01-28 13:14:59,414 - app.services.chapter_service - INFO - [ChapterService] Found 77 chapters
2026-01-28 13:14:59,414 - app.services.chapter_service - INFO -   - Chapter: 第1章 【摆烂的宿主】, order=1
2026-01-28 13:14:59,414 - app.services.chapter_service - INFO -   - ... (75 more chapters)
2026-01-28 13:14:59,414 - app.services.chapter_service - INFO -   - Chapter: 第100章 【火域铸真器，两脉起冲突】, order=77
2026-01-28 13:14:59,467 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 强制流程步骤: list_chapters
2026-01-28 13:14:59,469 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=list_chapters params={"work_id": "5fe6c67d-8a1b-48c1-ad56-a5281eb22e21"}
2026-01-28 13:14:59,469 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=list_chapters success=True count=77
2026-01-28 13:14:59,469 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 强制流程步骤: list_paragraphs
2026-01-28 13:14:59,469 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=list_paragraphs params={"chapter_order": 1, "offset": 0, "limit": 50, "preview_len": 80, "work_id": "5fe6c67d-8a1b-48c1-ad56-a5281eb22e21"}
2026-01-28 13:14:59,484 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=list_paragraphs success=True chapter=1 offset=0 limit=50 approximate=None
2026-01-28 13:14:59,484 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-28 13:14:59,484 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-28 13:15:04,596 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 13:15:04,596 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-28 13:15:04,613 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 13:15:04,615 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1854, cost=$0.000943, time=5112ms
2026-01-28 13:15:04,615 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=389, 尝试次数=1
2026-01-28 13:15:04,615 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=read_paragraphs params={"work_id": "5fe6c67d-8a1b-48c1-ad56-a5281eb22e21", "items": [{"chapter_order": 1, "paragraph_index": 9}, {"chapter_order": 1, "paragraph_index": 10}], "context_before": 2, "context_after": 2}
2026-01-28 13:15:04,615 - app.services.agent.langgraph_tools - INFO - [read_paragraphs] start items=2 index_base=zero
2026-01-28 13:15:04,631 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=9 corrected=False final=9
2026-01-28 13:15:04,632 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第9段
2026-01-28 13:15:04,659 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=10 corrected=False final=10
2026-01-28 13:15:04,660 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第10段
2026-01-28 13:15:04,662 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=read_paragraphs success=True count=2 index_base=zero
2026-01-28 13:15:04,663 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-28 13:15:04,664 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-28 13:15:07,851 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 13:15:07,851 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-28 13:15:07,872 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 13:15:07,872 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1574, cost=$0.000787, time=3190ms
2026-01-28 13:15:07,872 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=266, 尝试次数=1
2026-01-28 13:15:07,872 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"work_id": "5fe6c67d-8a1b-48c1-ad56-a5281eb22e21", "keywords": "十佬名额", "match_mode": "keywords", "limit": 10}
2026-01-28 13:15:07,901 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['十佬名额']..., mode=any, range=None, hits=0
2026-01-28 13:15:07,901 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=0 keywords=十佬名额
2026-01-28 13:15:07,901 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-28 13:15:07,901 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-28 13:15:11,840 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 13:15:11,840 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-28 13:15:11,852 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 13:15:11,852 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1195, cost=$0.000620, time=3938ms
2026-01-28 13:15:11,852 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=232, 尝试次数=1
2026-01-28 13:15:11,857 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"keywords": ["林仙", "王家"], "match_mode": "all", "limit": 100, "work_id": "5fe6c67d-8a1b-48c1-ad56-a5281eb22e21"}
2026-01-28 13:15:11,910 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['林仙', '王家']..., mode=all, range=None, hits=1
2026-01-28 13:15:11,920 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=255 corrected=False final=255
2026-01-28 13:15:11,920 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第17章第255段
2026-01-28 13:15:11,927 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=1 keywords=林仙,王家
2026-01-28 13:15:11,927 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-28 13:15:11,928 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-28 13:15:14,339 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 13:15:14,340 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-28 13:15:14,355 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 13:15:14,355 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=953, cost=$0.000554, time=2412ms
2026-01-28 13:15:14,355 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=257, 尝试次数=1
2026-01-28 13:15:14,355 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"work_id": "user_work_id", "keywords": ["冯曜", "无根生"], "match_mode": "all", "limit": 10}
2026-01-28 13:15:14,400 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['冯曜', '无根生']..., mode=all, range=None, hits=4
2026-01-28 13:15:14,412 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=76 corrected=False final=76
2026-01-28 13:15:14,412 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第18章第76段
2026-01-28 13:15:14,424 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=77 corrected=False final=77
2026-01-28 13:15:14,424 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第18章第77段
2026-01-28 13:15:14,435 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=134 corrected=False final=134
2026-01-28 13:15:14,435 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第18章第134段
2026-01-28 13:15:14,446 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=135 corrected=False final=135
2026-01-28 13:15:14,447 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第18章第135段
2026-01-28 13:15:14,447 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=4 keywords=冯曜,无根生
2026-01-28 13:15:14,447 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-28 13:15:14,447 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-28 13:15:18,241 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 13:15:18,241 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-28 13:15:18,251 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 13:15:18,253 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1460, cost=$0.000691, time=3794ms
2026-01-28 13:15:18,253 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=244, 尝试次数=1
2026-01-28 13:15:18,253 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"work_id": "text-00001", "keywords": ["林仙", "十佬名额"], "match_mode": "all", "limit": 10}
2026-01-28 13:15:18,285 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['林仙', '十佬名额']..., mode=all, range=None, hits=0
2026-01-28 13:15:18,295 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=0 keywords=林仙,十佬名额
2026-01-28 13:15:18,295 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-28 13:15:18,295 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-28 13:15:21,132 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 13:15:21,132 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-28 13:15:21,153 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 13:15:21,153 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1002, cost=$0.000595, time=2837ms
2026-01-28 13:15:21,153 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=267, 尝试次数=1
2026-01-28 13:15:21,153 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"work_id": "一人之下", "keywords": ["林仙", "王家"], "match_mode": "and", "limit": 10}
2026-01-28 13:15:21,167 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['林仙', '王家']..., mode=any, range=None, hits=10
2026-01-28 13:15:21,179 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=2 corrected=False final=2
2026-01-28 13:15:21,179 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第2段
2026-01-28 13:15:21,194 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=6 corrected=False final=6
2026-01-28 13:15:21,194 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第6段
2026-01-28 13:15:21,209 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=12 corrected=False final=12
2026-01-28 13:15:21,209 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第12段
2026-01-28 13:15:21,225 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=13 corrected=False final=13
2026-01-28 13:15:21,225 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第13段
2026-01-28 13:15:21,227 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=5 keywords=林仙,王家
2026-01-28 13:15:21,227 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-28 13:15:21,229 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-28 13:15:24,618 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 13:15:24,619 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-28 13:15:24,638 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 13:15:24,639 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1280, cost=$0.000677, time=3389ms
2026-01-28 13:15:24,641 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=274, 尝试次数=1
2026-01-28 13:15:24,641 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"work_id": "user_work_id", "keywords": ["林仙", "十佬名额"], "match_mode": "all", "limit": 10}
2026-01-28 13:15:24,676 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['林仙', '十佬名额']..., mode=all, range=None, hits=0
2026-01-28 13:15:24,676 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=0 keywords=林仙,十佬名额
2026-01-28 13:15:24,678 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-28 13:15:24,678 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-28 13:15:27,599 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 13:15:27,599 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-28 13:15:27,616 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 13:15:27,616 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1000, cost=$0.000571, time=2923ms
2026-01-28 13:15:27,616 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=247, 尝试次数=1
2026-01-28 13:15:27,616 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"work_id": "一人之下", "keywords": ["林仙"], "match_mode": "all", "limit": 100}
2026-01-28 13:15:27,657 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['林仙']..., mode=all, range=None, hits=100
2026-01-28 13:15:27,676 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=15 corrected=False final=15
2026-01-28 13:15:27,676 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第15段
2026-01-28 13:15:27,689 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=31 corrected=False final=31
2026-01-28 13:15:27,691 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第31段
2026-01-28 13:15:27,705 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=43 corrected=False final=43
2026-01-28 13:15:27,706 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第43段
2026-01-28 13:15:27,717 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=60 corrected=False final=60
2026-01-28 13:15:27,717 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第60段
2026-01-28 13:15:27,730 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=66 corrected=False final=66
2026-01-28 13:15:27,730 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第66段
2026-01-28 13:15:27,741 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=83 corrected=False final=83
2026-01-28 13:15:27,741 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第83段
2026-01-28 13:15:27,755 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=84 corrected=False final=84
2026-01-28 13:15:27,755 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第84段
2026-01-28 13:15:27,767 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=107 corrected=False final=107
2026-01-28 13:15:27,767 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第107段
2026-01-28 13:15:27,772 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=1 corrected=False final=1
2026-01-28 13:15:27,772 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第1段
2026-01-28 13:15:27,780 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=3 corrected=False final=3
2026-01-28 13:15:27,787 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第3段
2026-01-28 13:15:27,799 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=9 corrected=False final=9
2026-01-28 13:15:27,799 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第9段
2026-01-28 13:15:27,812 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=13 corrected=False final=13
2026-01-28 13:15:27,812 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第13段
2026-01-28 13:15:27,823 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=18 corrected=False final=18
2026-01-28 13:15:27,823 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第18段
2026-01-28 13:15:27,823 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=26 corrected=False final=26
2026-01-28 13:15:27,833 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第26段
2026-01-28 13:15:27,840 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=34 corrected=False final=34
2026-01-28 13:15:27,842 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第34段
2026-01-28 13:15:27,843 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=38 corrected=False final=38
2026-01-28 13:15:27,851 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第38段
2026-01-28 13:15:27,857 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=55 corrected=False final=55
2026-01-28 13:15:27,857 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第55段
2026-01-28 13:15:27,869 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=68 corrected=False final=68
2026-01-28 13:15:27,869 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第68段
2026-01-28 13:15:27,874 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=80 corrected=False final=80
2026-01-28 13:15:27,874 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第80段
2026-01-28 13:15:27,886 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=84 corrected=False final=84
2026-01-28 13:15:27,886 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第84段
2026-01-28 13:15:27,900 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=89 corrected=False final=89
2026-01-28 13:15:27,900 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第89段
2026-01-28 13:15:27,908 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=101 corrected=False final=101
2026-01-28 13:15:27,908 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第101段
2026-01-28 13:15:27,918 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=6 corrected=False final=6
2026-01-28 13:15:27,918 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第6段
2026-01-28 13:15:27,926 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=18 corrected=False final=18
2026-01-28 13:15:27,926 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第18段
2026-01-28 13:15:27,937 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=20 corrected=False final=20
2026-01-28 13:15:27,937 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第20段
2026-01-28 13:15:27,949 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=25 corrected=False final=25
2026-01-28 13:15:27,949 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第25段
2026-01-28 13:15:27,959 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=28 corrected=False final=28
2026-01-28 13:15:27,959 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第28段
2026-01-28 13:15:27,970 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=46 corrected=False final=46
2026-01-28 13:15:27,971 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第46段
2026-01-28 13:15:27,981 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=50 corrected=False final=50
2026-01-28 13:15:27,981 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第50段
2026-01-28 13:15:27,990 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=57 corrected=False final=57
2026-01-28 13:15:27,990 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第57段
2026-01-28 13:15:28,003 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=7 corrected=False final=7
2026-01-28 13:15:28,003 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第4章第7段
2026-01-28 13:15:28,014 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=8 corrected=False final=8
2026-01-28 13:15:28,014 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第4章第8段
2026-01-28 13:15:28,027 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=21 corrected=False final=21
2026-01-28 13:15:28,028 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第4章第21段
2026-01-28 13:15:28,038 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=30 corrected=False final=30
2026-01-28 13:15:28,038 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第4章第30段
2026-01-28 13:15:28,044 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=31 corrected=False final=31
2026-01-28 13:15:28,044 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第4章第31段
2026-01-28 13:15:28,060 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=49 corrected=False final=49
2026-01-28 13:15:28,060 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第4章第49段
2026-01-28 13:15:28,072 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=57 corrected=False final=57
2026-01-28 13:15:28,074 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第4章第57段
2026-01-28 13:15:28,084 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=61 corrected=False final=61
2026-01-28 13:15:28,084 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第4章第61段
2026-01-28 13:15:28,097 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=62 corrected=False final=62
2026-01-28 13:15:28,099 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第4章第62段
2026-01-28 13:15:28,110 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=72 corrected=False final=72
2026-01-28 13:15:28,110 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第4章第72段
2026-01-28 13:15:28,126 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=16 corrected=False final=16
2026-01-28 13:15:28,126 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第5章第16段
2026-01-28 13:15:28,136 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=25 corrected=False final=25
2026-01-28 13:15:28,136 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第5章第25段
2026-01-28 13:15:28,147 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=37 corrected=False final=37
2026-01-28 13:15:28,149 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第5章第37段
2026-01-28 13:15:28,157 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=39 corrected=False final=39
2026-01-28 13:15:28,157 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第5章第39段
2026-01-28 13:15:28,168 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=40 corrected=False final=40
2026-01-28 13:15:28,171 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第5章第40段
2026-01-28 13:15:28,178 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=41 corrected=False final=41
2026-01-28 13:15:28,178 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第5章第41段
2026-01-28 13:15:28,190 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=47 corrected=False final=47
2026-01-28 13:15:28,190 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第5章第47段
2026-01-28 13:15:28,202 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=69 corrected=False final=69
2026-01-28 13:15:28,203 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第5章第69段
2026-01-28 13:15:28,211 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=74 corrected=False final=74
2026-01-28 13:15:28,211 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第5章第74段
2026-01-28 13:15:28,211 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=87 keywords=林仙
2026-01-28 13:15:28,211 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 探索完成(工具循环): 10轮, 原因=达到读取上限
2026-01-28 13:15:28,224 - app.services.agent.execution.tool_executor - INFO - [StandardTool] explore_content 执行成功
2026-01-28 13:15:28,224 - app.api.v1.agent - INFO - [Stream] 任务完成: 根据用户提供的因果链节点和锚点，全面检索小说原文，收集所有相关证据。 (28.8s)
2026-01-28 13:15:28,224 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1完成
2026-01-28 13:15:28,224 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共1个任务，耗时: 28.82s
2026-01-28 13:15:28,224 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2026-01-28 13:15:28,230 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=1, 展示型=0
2026-01-28 13:15:28,230 - app.services.agent.langgraph_agent - INFO - [Response] 单个输出任务(explore_content)，使用AI整合
2026-01-28 13:15:28,230 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2026-01-28 13:15:28,230 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=1, 展示型=0
2026-01-28 13:15:28,230 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=3092字符, 处理后=3131字符
2026-01-28 13:15:28,230 - app.services.agent.planning.response_builder - INFO - [Summarization] 准备发送 summarization_start 事件
2026-01-28 13:15:28,230 - app.services.agent.stream.stream_event_handler - INFO - [StreamEventHandler] emit_summarization_start 被调用, _on_flow_event=True
2026-01-28 13:15:28,230 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_start 事件已发送
2026-01-28 13:15:28,230 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2026-01-28 13:15:28,230 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2026-01-28 13:15:28,241 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-28 13:15:28,241 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-28 13:15:28,243 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
2026-01-28 13:15:41,733 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-28 13:15:41,733 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_complete 事件已发送（第一个chunk时）
2026-01-28 13:15:41,733 - app.services.agent.planning.response_builder - INFO - [Summarization] output_ready 事件已发送（第一个chunk时）
2026-01-28 13:15:51,389 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 31 个数据块，总长度: 2756
2026-01-28 13:15:51,390 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 9793 (prompt=7838, completion=1955)
2026-01-28 13:15:51,391 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 13:15:51,392 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-28 13:15:51,407 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 13:15:51,408 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=9793, cost=$0.007239, time=23148ms
2026-01-28 13:15:51,409 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=2756
2026-01-28 13:15:52,397 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21 | 重要度=0.87
2026-01-28 13:15:53,284 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21 | 重要度=0.60
2026-01-28 13:15:53,290 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21:60055cd5-3851-46ac-b14c-8d6b99aa1db9, token=3082
2026-01-28 13:15:53,294 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21:60055cd5-3851-46ac-b14c-8d6b99aa1db9, 消息数=2, 摘要长度=0, Token=3082
2026-01-28 13:15:53,294 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21:60055cd5-3851-46ac-b14c-8d6b99aa1db9)
2026-01-28 13:15:53,295 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2026-01-28 13:15:53,301 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed
2026-01-28 13:16:09,398 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/60055cd5-3851-46ac-b14c-8d6b99aa1db9