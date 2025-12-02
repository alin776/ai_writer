21:42:37 app.api.v1.agent INFO   [Redis] 全局连接池已创建
已注册策略: web_novel_11d - 网文11维度分析
21:42:37 app.utils.file_storage INFO   临时文件存储目录: D:\Temp\novelaide_exports
21:42:38 app.main INFO   [STARTUP] 监控中间件已注册: TraceMiddleware, MonitoringMiddleware
INFO:     Started server process [38516]
INFO:     Waiting for application startup.
21:42:38 app.main INFO   [STARTUP] 应用启动中...
21:42:38 app.core.database INFO   正在初始化数据库... (尝试 1/3)
21:42:38 app.core.database INFO   ✅ 数据库初始化成功
21:42:38 apscheduler.scheduler INFO   Adding job tentatively -- it will be properly scheduled when the scheduler starts
21:42:38 apscheduler.scheduler INFO   Added job "清理过期的去痕迹会话详情" to job store "default"
21:42:38 apscheduler.scheduler INFO   Scheduler started
21:42:38 app.tasks.cleanup_humanize_details INFO   定时任务调度器已启动
21:42:38 app.main INFO   [STARTUP] 开始预初始化同步Redis连接...
21:42:38 app.main INFO   [STARTUP] ✅ 同步Redis连接池预初始化完成
21:42:38 app.main INFO   [STARTUP] 开始初始化AsyncRedisSaver索引...
21:42:38 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ setup_checkpointer Redis连接验证成功
21:42:38 redisvl.index.index INFO   Index already exists, not overwriting.
21:42:38 redisvl.index.index INFO   Index already exists, not overwriting.
21:42:38 redisvl.index.index INFO   Index already exists, not overwriting.
21:42:38 langgraph.checkpoint.redis.aio INFO   Redis client is a standalone client
21:42:38 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ AsyncRedisSaver索引预创建成功
21:42:38 app.main INFO   [STARTUP] AsyncRedisSaver索引初始化完成
21:42:38 app.main INFO   [STARTUP] 开始预加载Embedding模型...
21:42:38 app.services.vector_store_service INFO   🔄 预加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
21:42:44 app.services.vector_store_service INFO   ✅ Embedding模型预加载成功，耗时: 6.51秒
21:42:44 app.main INFO   [STARTUP] Embedding模型预加载完成
21:42:44 app.main INFO   [STARTUP] P0性能优化已暂时禁用（诊断模式）
21:42:44 app.main INFO   [STARTUP] 应用启动完成
INFO:     Application startup complete.
21:44:48 monitoring INFO   Registered health check: cpu_usage
21:44:48 monitoring INFO   Registered health check: memory_usage
21:44:48 monitoring INFO   Registered health check: disk_usage
21:44:48 monitoring INFO   Registered health check: process_status
21:44:48 monitoring INFO   Added alert rule: high_cpu_usage
21:44:48 monitoring INFO   Added alert rule: high_memory_usage
21:44:48 monitoring INFO   Added alert rule: low_disk_space
21:44:48 app.api.v1.auth INFO   [LOGIN] 尝试登录: 2072855200@qq.com
21:44:48 app.api.v1.auth INFO   [LOGIN] 会话创建成功: 602f5147-846a-4cde-95d3-405fa75f133f (127.0.0.1)
21:44:48 app.api.v1.auth INFO   [LOGIN] 登录成功: testuser_new-1 (602f5147-846a-4cde-95d3-405fa75f133f) from 127.0.0.1
21:44:48 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/auth/login
INFO:     127.0.0.1:57872 - "POST /api/v1/auth/login HTTP/1.1" 200 OK
INFO:     127.0.0.1:57872 - "OPTIONS /api/v1/users/me HTTP/1.1" 200 OK
21:44:48 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/users/me
INFO:     127.0.0.1:57872 - "GET /api/v1/users/me HTTP/1.1" 200 OK
INFO:     127.0.0.1:57872 - "OPTIONS /api/v1/works HTTP/1.1" 200 OK
INFO:     127.0.0.1:58649 - "OPTIONS /api/v1/works HTTP/1.1" 200 OK
21:44:49 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works
INFO:     127.0.0.1:57872 - "GET /api/v1/works HTTP/1.1" 200 OK
21:44:49 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works
INFO:     127.0.0.1:58649 - "GET /api/v1/works HTTP/1.1" 200 OK
INFO:     127.0.0.1:52251 - "OPTIONS /api/v1/works/ad948837-e94e-4d0f-92a4-a75cf1301b07 HTTP/1.1" 200 OK
INFO:     127.0.0.1:54541 - "OPTIONS /api/v1/chapters/work/ad948837-e94e-4d0f-92a4-a75cf1301b07 HTTP/1.1" 200 OK
INFO:     127.0.0.1:54785 - "OPTIONS /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/characters HTTP/1.1" 200 OK
INFO:     127.0.0.1:49553 - "OPTIONS /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:57019 - "OPTIONS /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/settings HTTP/1.1" 200 OK
INFO:     127.0.0.1:57154 - "OPTIONS /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/locations HTTP/1.1" 200 OK
INFO:     127.0.0.1:49553 - "OPTIONS /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/ai-guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:57019 - "OPTIONS /api/v1/works/ad948837-e94e-4d0f-92a4-a75cf1301b07 HTTP/1.1" 200 OK
INFO:     127.0.0.1:57154 - "OPTIONS /api/v1/chapters/work/ad948837-e94e-4d0f-92a4-a75cf1301b07 HTTP/1.1" 200 OK
INFO:     127.0.0.1:49553 - "OPTIONS /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/characters HTTP/1.1" 200 OK
INFO:     127.0.0.1:57154 - "OPTIONS /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/locations HTTP/1.1" 200 OK
INFO:     127.0.0.1:49553 - "OPTIONS /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/settings HTTP/1.1" 200 OK
INFO:     127.0.0.1:57154 - "OPTIONS /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:49553 - "OPTIONS /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/ai-guidelines HTTP/1.1" 200 OK
21:44:59 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works/ad948837-e94e-4d0f-92a4-a75cf1301b07
INFO:     127.0.0.1:57154 - "GET /api/v1/works/ad948837-e94e-4d0f-92a4-a75cf1301b07 HTTP/1.1" 200 OK
21:44:59 app.api.v1.chapters INFO   [GET chapters] work_id=ad948837-e94e-4d0f-92a4-a75cf1301b07, user_id=602f5147-846a-4cde-95d3-405fa75f133f
21:44:59 app.api.v1.chapters INFO   ⚠️ [GET chapters] 缓存未命中: chapters:work:ad948837-e94e-4d0f-92a4-a75cf1301b07
21:44:59 app.services.chapter_service INFO   [ChapterService] Querying chapters for work_id=ad948837-e94e-4d0f-92a4-a75cf1301b07, type=<class 'uuid.UUID'>
21:44:59 app.services.chapter_service INFO   [ChapterService] Found 4 chapters
21:44:59 app.services.chapter_service INFO     - Chapter: 钢铁坟场, order=1
21:44:59 app.services.chapter_service INFO     - Chapter: 归巢与低语, order=2
21:44:59 app.services.chapter_service INFO     - Chapter: 遗落的星图, order=3
21:44:59 app.services.chapter_service INFO     - Chapter: 天眼与土獾, order=4
21:44:59 app.api.v1.chapters INFO   [GET chapters] Returning 4 chapters
21:44:59 app.api.v1.chapters INFO   💾 [GET chapters] 缓存已保存: chapters:work:ad948837-e94e-4d0f-92a4-a75cf1301b07 (expire=60s)
21:44:59 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/chapters/work/ad948837-e94e-4d0f-92a4-a75cf1301b07
INFO:     127.0.0.1:57154 - "GET /api/v1/chapters/work/ad948837-e94e-4d0f-92a4-a75cf1301b07 HTTP/1.1" 200 OK
21:44:59 app.api.v1.worldview INFO   ⚠️ [Worldview] 缓存未命中: worldview:characters:ad948837-e94e-4d0f-92a4-a75cf1301b07
21:44:59 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:characters:ad948837-e94e-4d0f-92a4-a75cf1301b07 (expire=300s)
21:44:59 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/characters
INFO:     127.0.0.1:57154 - "GET /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/characters HTTP/1.1" 200 OK
21:44:59 app.api.v1.worldview INFO   ⚠️ [Worldview] 缓存未命中: worldview:guidelines:ad948837-e94e-4d0f-92a4-a75cf1301b07
21:44:59 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:guidelines:ad948837-e94e-4d0f-92a4-a75cf1301b07 (expire=300s)
21:44:59 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/guidelines
INFO:     127.0.0.1:57154 - "GET /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/guidelines HTTP/1.1" 200 OK
21:44:59 app.api.v1.worldview INFO   ⚠️ [Worldview] 缓存未命中: worldview:settings:ad948837-e94e-4d0f-92a4-a75cf1301b07
21:44:59 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:settings:ad948837-e94e-4d0f-92a4-a75cf1301b07 (expire=300s)
21:44:59 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/settings
INFO:     127.0.0.1:57154 - "GET /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/settings HTTP/1.1" 200 OK
21:44:59 app.api.v1.worldview INFO   ⚠️ [Worldview] 缓存未命中: worldview:locations:ad948837-e94e-4d0f-92a4-a75cf1301b07
21:44:59 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:locations:ad948837-e94e-4d0f-92a4-a75cf1301b07 (expire=300s)
21:44:59 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/locations
INFO:     127.0.0.1:57154 - "GET /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/locations HTTP/1.1" 200 OK
21:44:59 app.api.v1.worldview INFO   ⚠️ [Worldview] 缓存未命中: worldview:ai-guidelines:ad948837-e94e-4d0f-92a4-a75cf1301b07
21:44:59 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:ai-guidelines:ad948837-e94e-4d0f-92a4-a75cf1301b07 (expire=300s)
21:44:59 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/ai-guidelines
INFO:     127.0.0.1:57154 - "GET /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/ai-guidelines HTTP/1.1" 200 OK
21:44:59 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works/ad948837-e94e-4d0f-92a4-a75cf1301b07
INFO:     127.0.0.1:57154 - "GET /api/v1/works/ad948837-e94e-4d0f-92a4-a75cf1301b07 HTTP/1.1" 200 OK
21:44:59 app.api.v1.chapters INFO   [GET chapters] work_id=ad948837-e94e-4d0f-92a4-a75cf1301b07, user_id=602f5147-846a-4cde-95d3-405fa75f133f
21:44:59 app.api.v1.chapters INFO   ✅ [GET chapters] 缓存命中: chapters:work:ad948837-e94e-4d0f-92a4-a75cf1301b07
21:44:59 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/chapters/work/ad948837-e94e-4d0f-92a4-a75cf1301b07
INFO:     127.0.0.1:57154 - "GET /api/v1/chapters/work/ad948837-e94e-4d0f-92a4-a75cf1301b07 HTTP/1.1" 200 OK
21:44:59 app.api.v1.worldview INFO   ⚠️ [Worldview] 缓存未命中: worldview:characters:ad948837-e94e-4d0f-92a4-a75cf1301b07
21:44:59 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:characters:ad948837-e94e-4d0f-92a4-a75cf1301b07 (expire=300s)
21:44:59 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/characters
INFO:     127.0.0.1:57154 - "GET /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/characters HTTP/1.1" 200 OK
21:44:59 app.api.v1.worldview INFO   ✅ [Worldview] 缓存命中: worldview:guidelines:ad948837-e94e-4d0f-92a4-a75cf1301b07
21:44:59 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/guidelines
INFO:     127.0.0.1:65015 - "GET /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:50065 - "OPTIONS /api/v1/analysis/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/status HTTP/1.1" 200 OK
21:44:59 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/analysis/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/status
INFO:     127.0.0.1:50065 - "GET /api/v1/analysis/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/status HTTP/1.1" 200 OK
INFO:     127.0.0.1:50065 - "OPTIONS /api/v1/chapters/ef5eb68c-32b8-4249-83a3-31d57363c0a9 HTTP/1.1" 200 OK
INFO:     127.0.0.1:65015 - "OPTIONS /api/v1/chapters/ef5eb68c-32b8-4249-83a3-31d57363c0a9 HTTP/1.1" 200 OK
21:44:59 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:ad948837-e94e-4d0f-92a4-a75cf1301b07
21:44:59 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/ef5eb68c-32b8-4249-83a3-31d57363c0a9
INFO:     127.0.0.1:65015 - "PUT /api/v1/chapters/ef5eb68c-32b8-4249-83a3-31d57363c0a9 HTTP/1.1" 200 OK
21:44:59 app.api.v1.worldview INFO   ✅ [Worldview] 缓存命中: worldview:ai-guidelines:ad948837-e94e-4d0f-92a4-a75cf1301b07
21:44:59 app.api.v1.worldview INFO   ⚠️ [Worldview] 缓存未命中: worldview:locations:ad948837-e94e-4d0f-92a4-a75cf1301b07
21:44:59 app.api.v1.worldview INFO   ✅ [Worldview] 缓存命中: worldview:settings:ad948837-e94e-4d0f-92a4-a75cf1301b07
21:45:00 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/ai-guidelines
21:45:00 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/settings
INFO:     127.0.0.1:53276 - "GET /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/ai-guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:50328 - "GET /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/settings HTTP/1.1" 200 OK
21:45:00 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:locations:ad948837-e94e-4d0f-92a4-a75cf1301b07 (expire=300s)
21:45:00 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/locations
INFO:     127.0.0.1:57154 - "GET /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/locations HTTP/1.1" 200 OK
21:45:00 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/analysis/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/status
INFO:     127.0.0.1:57154 - "GET /api/v1/analysis/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/status HTTP/1.1" 200 OK
21:45:00 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:ad948837-e94e-4d0f-92a4-a75cf1301b07
21:45:00 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/ef5eb68c-32b8-4249-83a3-31d57363c0a9
INFO:     127.0.0.1:64126 - "PUT /api/v1/chapters/ef5eb68c-32b8-4249-83a3-31d57363c0a9 HTTP/1.1" 200 OK
INFO:     127.0.0.1:58243 - "OPTIONS /api/v1/agent/chat/stream HTTP/1.1" 200 OK
21:45:24 app.services.ai.prompts INFO   Prompts loaded successfully from D:\Java\ai_writer\backend\app\services\ai\prompts\default.json
21:45:24 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
21:45:24 app.services.ai.http_ai_service INFO   ModelSelector 已启用
21:45:24 app.services.ai.http_ai_service INFO   AILogService 已启用 (用于成本追踪)
21:45:26 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
21:45:26 app.api.v1.agent INFO   [Chat Stream] Mode: planning
21:45:26 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:58243 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
21:45:26 app.core.redis INFO   ✅ Redis connected: redis://localhost:6379/0
21:45:26 app.api.v1.agent INFO   [Session] 创建新会话归属: 9207f386-1021-4c17-9bfa-634adf7e17ee -> 602f5147-846a-4cde-95d3-405fa75f133f
21:45:26 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: planning, Message: who are you?...
21:45:26 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
21:45:26 app.services.ai.http_ai_service INFO   ModelSelector 已启用
21:45:26 app.services.ai.http_ai_service WARNING   成本追踪已启用，但未提供db或user_id，成本数据将不会被记录！请检查HTTPAIService初始化参数。
21:45:28 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
21:45:28 app.services.context.adaptive_budget INFO   ✅ 所有预算配置验证通过
21:45:36 app.services.context.vector_memory_store INFO   ✅ VectorMemoryStore初始化成功 | 目录=./data/chroma_db | 模型=paraphrase-multilingual-MiniLM-L12-v2 | 集合=user_memories
21:45:36 app.services.context.manager INFO   ✅ VectorMemoryStore 已初始化
21:45:36 app.services.context.manager INFO   ✅ ContextManager: 长期记忆已启用 (user_id=None)
21:45:36 app.services.context.manager INFO   ✅ ContextManager: 自适应预算已启用
21:45:36 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ ContextManager已初始化（长期记忆已启用，自适应预算已启用，总预算=16000 tokens）
成功加载模板: intent_classifier (版本 2.0.0)
成功加载模板: writing_agent (版本 2.0.0)
成功加载模板: planning_agent (版本 2.0.0)
成功加载模板: tool_agent (版本 2.0.0)
成功加载模板: query_agent (版本 2.0.0)
成功加载模板: system_agent_prompt (版本 2.0.0)
成功加载模板: creative_writing_prompt (版本 1.0.0)
21:45:36 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ PromptManager已初始化
21:45:36 app.services.agent.langgraph_agent INFO   [LangGraph] 使用 HTTPAIService 模式（手动工具调用，绕过 Cloudflare）
21:45:36 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ Redis连接验证成功
21:45:36 app.services.agent.langgraph_agent INFO   [LangGraph] OK 使用 AsyncRedisSaver（redis://localhost:6379/0，TTL=7天）
21:45:36 app.services.agent.memory.metrics INFO   [MemoryMetrics] 监控系统已初始化
21:45:36 app.services.agent.memory.long_term_store INFO   [LongTermStore] Initialized: base_dir=./data/long_term_memory, max_size=50KB, compression=True
21:45:36 app.services.agent.memory.enhanced_memory_manager INFO   EnhancedMemoryManager initialized: short=10, medium=100, threshold=0.1, long_term_backup=enabled
21:45:36 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ EnhancedMemoryManager已创建
21:45:36 app.services.agent.memory.unified_coordinator INFO   [UnifiedMemoryCoordinator] 初始化统一记忆协调器
21:45:36 app.services.agent.memory.unified_coordinator INFO   [UnifiedMemoryCoordinator] 全局实例已设置
21:45:36 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ UnifiedMemoryCoordinator已初始化 | checkpointer=AsyncRedisSaver | enhanced_memory=yes | context_manager=yes
21:45:36 app.services.agent.parallel_tool_node INFO   [ParallelToolNode] 初始化完成，最大并发数=5，并行安全工具=4个
21:45:36 app.api.v1.agent INFO   [Global Agent] 创建全局Agent实例，MemorySaver将在请求间共享
21:45:36 app.services.agent.langgraph_agent INFO   [Planning] 使用隔离的thread_id: ad948837-e94e-4d0f-92a4-a75cf1301b07:9207f386-1021-4c17-9bfa-634adf7e17ee (work_id=ad948837-e94e-4d0f-92a4-a75cf1301b07, conversation_id=9207f386-1021-4c17-9bfa-634adf7e17ee)
21:45:36 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: who are you?...
21:45:36 app.core.cache INFO   ⚠️ 缓存未命中: prompt:get_planning_static_prompt:fca6eb91156619d0
21:45:36 app.core.cache INFO   💾 缓存已保存: prompt:get_planning_static_prompt:fca6eb91156619d0 (expire=3600s)
21:45:36 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
21:45:36 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
21:45:36 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=600, temp=0.3, task_type=TaskType.SIMPLE_QA
21:45:38 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
21:45:47 app.services.ai.http_ai_service INFO   API 响应完成，共接收 6 个数据块，总长度: 624
21:45:47 app.services.ai.http_ai_service INFO   流式响应Token统计: 2822 (prompt=2569, completion=253)
21:45:47 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2822, cost=$0.005741, time=11008ms
21:45:47 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=2822
21:45:47 app.services.agent.langgraph_agent INFO   [JSON解析] 方法2成功: 从```json块提取
21:45:47 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共3个任务，耗时: 11.04s
21:45:47 app.api.v1.agent INFO   [Stream] 规划生成: 3 个任务
21:45:47 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
21:45:47 app.services.agent.parameter_resolver INFO   [ParameterResolver] 初始化完成, 严格模式: False
21:45:47 app.services.agent.langgraph_agent INFO   [ParameterResolver] 参数解析器已启用
21:45:47 app.services.agent.langgraph_agent INFO   [ParallelExecution] 任务分组: 并行=2, 串行=1
21:45:47 app.services.agent.langgraph_agent INFO   [ParallelExecution] 开始并行执行2个任务
21:45:47 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务1开始: 读取指定章节内容
21:45:47 app.api.v1.agent INFO   [Stream] 任务开始: 读取指定章节内容
21:45:47 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务2开始: 获取作品上下文信息
21:45:47 app.api.v1.agent INFO   [Stream] 任务开始: 获取作品上下文信息
21:45:47 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=ad948837-e94e-4d0f-92a4-a75cf1301b07, chapter_id=ef5eb68c-32b8-4249-83a3-31d57363c0a9
21:45:47 app.services.agent.langgraph_agent INFO   [read_chapter_tool] ✅ 读取章节成功: 钢铁坟场
21:45:47 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务1完成
21:45:47 app.api.v1.agent INFO   [Stream] 任务完成: 读取指定章节内容 (0.0s)
21:45:47 app.services.vector_store_service INFO   RAG检索: work_id=ad948837-e94e-4d0f-92a4-a75cf1301b07, query=作品背景和设定...
21:45:47 app.services.vector_store_service INFO   检索到 0 个相关结果（阈值=0.4）
21:45:47 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=大寂灭
21:45:47 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务2完成
21:45:47 app.api.v1.agent INFO   [Stream] 任务完成: 获取作品上下文信息 (0.2s)
21:45:47 app.services.agent.langgraph_agent INFO   [ParallelExecution] 开始串行执行1个任务
21:45:47 app.services.agent.langgraph_agent INFO   [ParallelExecution] 串行任务3开始: 分析章节内容以寻找AI身份线索
21:45:47 app.api.v1.agent INFO   [Stream] 任务开始: 分析章节内容以寻找AI身份线索
21:45:47 app.prompts.constraint_manager INFO   ✅ 已加载模板: analyze_text (v3.0.0)
21:45:47 app.prompts.constraint_manager INFO   ✅ 已加载模板: creative_writing (v1.0.0)
21:45:47 app.prompts.constraint_manager INFO   ✅ 已加载模板: intent_classifier (v2.0.0)
21:45:47 app.prompts.constraint_manager INFO   ✅ 已加载模板: planning_agent (v2.0.0)
21:45:47 app.prompts.constraint_manager INFO   ✅ 已加载模板: query_agent (v2.0.0)
21:45:47 app.prompts.constraint_manager INFO   ✅ 已加载模板: system_agent (v2.0.0)
21:45:47 app.prompts.constraint_manager INFO   ✅ 已加载模板: tool_agent (v2.0.0)
21:45:47 app.prompts.constraint_manager INFO   ✅ 已加载模板: writing_agent (v2.0.0)
21:45:47 app.prompts.constraint_manager INFO   ✅ 约束提示词管理器已初始化: 加载8个模板, 注册0个验证器
21:45:47 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
21:45:47 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
21:45:47 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
21:45:50 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
21:46:10 app.services.ai.http_ai_service INFO   API 响应完成，共接收 36 个数据块，总长度: 3397
21:46:10 app.services.ai.http_ai_service INFO   流式响应Token统计: 5594 (prompt=3329, completion=2265)
21:46:10 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=5594, cost=$0.026811, time=22856ms
21:46:10 app.services.agent.langgraph_agent INFO   ✅ [Agent分析] 分析完成，结果长度: 3397
21:46:10 app.services.agent.langgraph_agent INFO   [ParallelExecution] 串行任务3完成
21:46:10 app.api.v1.agent INFO   [Stream] 任务完成: 分析章节内容以寻找AI身份线索 (22.9s)
21:46:10 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共3个任务，耗时: 23.13s
21:46:10 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
21:46:10 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=1, 输出型=1, 展示型=1
21:46:10 app.services.agent.langgraph_agent INFO   [Response] 单个分析任务(analyze_text_tool)，使用AI格式化
21:46:10 app.services.agent.langgraph_agent INFO   [Summarization] 使用AI整合任务结果
21:46:10 app.services.agent.langgraph_agent INFO   [Summarization] 上下文压缩: 原始=8098字符, 压缩后=5683字符, 压缩率=30%
21:46:10 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
21:46:10 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
21:46:10 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
21:46:12 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
21:46:18 app.services.ai.http_ai_service INFO   API 响应完成，共接收 5 个数据块，总长度: 361
21:46:18 app.services.ai.http_ai_service INFO   流式响应Token统计: 5277 (prompt=5050, completion=227)
21:46:18 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=5277, cost=$0.008582, time=8345ms
21:46:18 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=5277
21:46:19 app.api.v1.agent INFO   [Stream] 跳过最终响应（内容已流式发送）
21:46:19 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed
INFO:     127.0.0.1:55060 - "OPTIONS /api/v1/ai/complete HTTP/1.1" 200 OK
21:49:13 app.api.v1.ai INFO   [AI续写] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), 上下文长度: 110, 风格: 默认, work_id: None, chapter_id: None
21:49:13 app.api.v1.ai INFO   [AI续写] context内容: '呼—— 刺骨的寒风卷着铁锈与黄沙的味道，穿过摩天大楼扭曲的钢铁骸骨，发出鬼哭般的呜咽。 凌风将身体缩在一段断裂的承重墙后，小心翼翼地探出半个脑袋。头顶上，那轮被污染大气层过滤成昏黄色蛋黄的太阳，正不情愿地向着地平线沉去。'
21:49:13 app.api.v1.ai INFO   [AI续写] prompt: '续写', max_tokens: 100
21:49:13 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
21:49:13 app.services.ai.http_ai_service INFO   ModelSelector 已启用
21:49:13 app.services.ai.http_ai_service INFO   AILogService 已启用 (用于成本追踪)
21:49:14 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
21:49:14 app.services.ai.http_ai_service INFO   AI自动补全请求 - 上下文长度: 110, work_id: None
21:49:14 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=100, temp=0.7, task_type=None
21:49:14 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/complete
INFO:     127.0.0.1:55060 - "POST /api/v1/ai/complete HTTP/1.1" 200 OK
21:49:18 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
21:49:18 app.services.ai.http_ai_service INFO   API 响应完成，共接收 2 个数据块，总长度: 23
21:49:18 app.services.ai.http_ai_service INFO   流式响应Token统计: 269 (prompt=252, completion=17)
21:49:18 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:实例): tokens=269, cost=$0.000485, time=4310ms
21:49:18 app.api.v1.ai INFO   [AI续写] 用户 testuser_new-1 请求完成，生成字数: 23
21:49:37 app.api.v1.ai INFO   [AI续写] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), 上下文长度: 110, 风格: 默认, work_id: None, chapter_id: None
21:49:37 app.api.v1.ai INFO   [AI续写] context内容: '呼—— 刺骨的寒风卷着铁锈与黄沙的味道，穿过摩天大楼扭曲的钢铁骸骨，发出鬼哭般的呜咽。 凌风将身体缩在一段断裂的承重墙后，小心翼翼地探出半个脑袋。头顶上，那轮被污染大气层过滤成昏黄色蛋黄的太阳，正不情愿地向着地平线沉去。'
21:49:37 app.api.v1.ai INFO   [AI续写] prompt: '续写', max_tokens: 100
21:49:37 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
21:49:37 app.services.ai.http_ai_service INFO   ModelSelector 已启用
21:49:37 app.services.ai.http_ai_service INFO   AILogService 已启用 (用于成本追踪)
21:49:38 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
21:49:38 app.services.ai.http_ai_service INFO   AI自动补全请求 - 上下文长度: 110, work_id: None
21:49:38 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=100, temp=0.7, task_type=None
21:49:38 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/complete
INFO:     127.0.0.1:57956 - "POST /api/v1/ai/complete HTTP/1.1" 200 OK
21:49:40 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
21:49:40 app.services.ai.http_ai_service INFO   API 响应完成，共接收 3 个数据块，总长度: 27
21:49:40 app.services.ai.http_ai_service INFO   流式响应Token统计: 284 (prompt=261, completion=23)
21:49:40 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:实例): tokens=284, cost=$0.000556, time=2734ms
21:49:40 app.api.v1.ai INFO   [AI续写] 用户 testuser_new-1 请求完成，生成字数: 27
21:49:54 app.api.v1.ai INFO   [AI续写] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), 上下文长度: 110, 风格: 默认, work_id: None, chapter_id: None
21:49:54 app.api.v1.ai INFO   [AI续写] context内容: '呼—— 刺骨的寒风卷着铁锈与黄沙的味道，穿过摩天大楼扭曲的钢铁骸骨，发出鬼哭般的呜咽。 凌风将身体缩在一段断裂的承重墙后，小心翼翼地探出半个脑袋。头顶上，那轮被污染大气层过滤成昏黄色蛋黄的太阳，正不情愿地向着地平线沉去。'
21:49:54 app.api.v1.ai INFO   [AI续写] prompt: '续写', max_tokens: 100
21:49:54 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
21:49:54 app.services.ai.http_ai_service INFO   ModelSelector 已启用
21:49:54 app.services.ai.http_ai_service INFO   AILogService 已启用 (用于成本追踪)
21:49:56 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
21:49:56 app.services.ai.http_ai_service INFO   AI自动补全请求 - 上下文长度: 110, work_id: None
21:49:56 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=100, temp=0.7, task_type=None
21:49:56 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/complete
INFO:     127.0.0.1:56329 - "POST /api/v1/ai/complete HTTP/1.1" 200 OK
21:49:58 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
21:49:59 app.services.ai.http_ai_service INFO   API 响应完成，共接收 3 个数据块，总长度: 26
21:49:59 app.services.ai.http_ai_service INFO   流式响应Token统计: 274 (prompt=252, completion=22)
21:49:59 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:实例): tokens=274, cost=$0.000535, time=2586ms
21:49:59 app.api.v1.ai INFO   [AI续写] 用户 testuser_new-1 请求完成，生成字数: 26
21:50:46 app.api.v1.ai INFO   [AI续写] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), 上下文长度: 197, 风格: 默认, work_id: None, chapter_id: None
21:50:46 app.api.v1.ai INFO   [AI续写] context内容: '次扫视着周围。他像一只灵巧的猫，无声无息地从掩体后窜出，踩着一根悬空的钢梁，轻松地跃到对面一处还算完整的楼层平台。 “嘎吱——” 脚下的楼板发出一声令人牙酸的呻吟，无数裂纹如蛛网般蔓延。凌风的瞳孔骤然一缩，身体瞬间绷紧，重心压低，几乎是贴着地面滑行了数米，才堪堪避开了那片最不稳定的区域。 冷汗，从他的额角渗出。在这片钢铁坟场里，最大的敌人往往不是变异的怪物或是“机械神教”那些冷酷的巡逻机器人'
21:50:46 app.api.v1.ai INFO   [AI续写] prompt: '续写', max_tokens: 100
21:50:46 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
21:50:46 app.services.ai.http_ai_service INFO   ModelSelector 已启用
21:50:46 app.services.ai.http_ai_service INFO   AILogService 已启用 (用于成本追踪)
21:50:48 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
21:50:48 app.services.ai.http_ai_service INFO   AI自动补全请求 - 上下文长度: 197, work_id: None
21:50:48 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=100, temp=0.7, task_type=None
21:50:48 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/complete
INFO:     127.0.0.1:49953 - "POST /api/v1/ai/complete HTTP/1.1" 200 OK
21:50:49 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
21:50:49 app.services.ai.http_ai_service INFO   ModelSelector 已启用
21:50:49 app.services.ai.http_ai_service INFO   AILogService 已启用 (用于成本追踪)
21:50:51 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
21:50:51 app.api.v1.agent INFO   [Chat Stream] Mode: planning
21:50:51 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:55515 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
21:50:51 app.api.v1.agent INFO   [Session] 创建新会话归属: bbd9131d-9a62-4beb-82c5-5b684fb85d49 -> 602f5147-846a-4cde-95d3-405fa75f133f
21:50:51 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: planning, Message: 第五章应该起什么名字？说的是章名...
21:50:51 app.services.agent.langgraph_agent INFO   [Planning] 使用隔离的thread_id: ad948837-e94e-4d0f-92a4-a75cf1301b07:bbd9131d-9a62-4beb-82c5-5b684fb85d49 (work_id=ad948837-e94e-4d0f-92a4-a75cf1301b07, conversation_id=bbd9131d-9a62-4beb-82c5-5b684fb85d49)
21:50:51 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: 第五章应该起什么名字？说的是章名...
21:50:51 app.core.cache INFO   ✅ 缓存命中: prompt:get_planning_static_prompt:fca6eb91156619d0
21:50:51 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
21:50:51 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
21:50:51 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=600, temp=0.3, task_type=TaskType.SIMPLE_QA
21:50:54 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
21:50:57 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
21:51:00 app.services.ai.http_ai_service INFO   API 响应完成，共接收 6 个数据块，总长度: 835
21:51:00 app.services.ai.http_ai_service INFO   流式响应Token统计: 2578 (prompt=2233, completion=345)
21:51:00 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2578, cost=$0.006241, time=9117ms
21:51:00 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=2578
21:51:00 app.services.agent.langgraph_agent INFO   [JSON解析] 方法2成功: 从```json块提取
21:51:00 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共4个任务，耗时: 9.14s
21:51:00 app.api.v1.agent INFO   [Stream] 规划生成: 4 个任务
21:51:00 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
21:51:00 app.services.agent.parameter_resolver INFO   [ParameterResolver] 初始化完成, 严格模式: False
21:51:00 app.services.agent.langgraph_agent INFO   [ParameterResolver] 参数解析器已启用
21:51:00 app.services.agent.langgraph_agent INFO   [ParallelExecution] 任务分组: 并行=2, 串行=2
21:51:00 app.services.agent.langgraph_agent INFO   [ParallelExecution] 开始并行执行2个任务
21:51:00 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务1开始: 获取第四章内容
21:51:00 app.api.v1.agent INFO   [Stream] 任务开始: 获取第四章内容
21:51:00 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务2开始: 获取作品上下文信息
21:51:00 app.api.v1.agent INFO   [Stream] 任务开始: 获取作品上下文信息
21:51:00 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=ad948837-e94e-4d0f-92a4-a75cf1301b07, chapter_id=ef5eb68c-32b8-4249-83a3-31d57363c0a9
21:51:00 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第4章: 天眼与土獾
21:51:00 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务1完成
21:51:00 app.api.v1.agent INFO   [Stream] 任务完成: 获取第四章内容 (0.0s)
21:51:00 app.services.vector_store_service INFO   RAG检索: work_id=ad948837-e94e-4d0f-92a4-a75cf1301b07, query=作品背景和设定...
21:51:00 app.services.vector_store_service INFO   检索到 0 个相关结果（阈值=0.4）
21:51:00 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=大寂灭
21:51:00 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务2完成
21:51:00 app.api.v1.agent INFO   [Stream] 任务完成: 获取作品上下文信息 (0.2s)
21:51:00 app.services.agent.langgraph_agent INFO   [ParallelExecution] 开始串行执行2个任务
21:51:00 app.services.agent.langgraph_agent INFO   [ParallelExecution] 串行任务3开始: 分析第四章内容，提取关键情节和主题
21:51:00 app.api.v1.agent INFO   [Stream] 任务开始: 分析第四章内容，提取关键情节和主题
21:51:00 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
21:51:00 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
21:51:00 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
21:51:02 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
21:51:13 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 9
21:51:13 app.services.ai.http_ai_service INFO   流式响应Token统计: 2160 (prompt=2160, completion=0)
21:51:13 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:实例): tokens=2160, cost=$0.002700, time=24760ms
21:51:13 app.api.v1.ai INFO   [AI续写] 用户 testuser_new-1 请求完成，生成字数: 9
21:51:29 app.api.v1.ai INFO   [AI续写] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), 上下文长度: 197, 风格: 默认, work_id: None, chapter_id: None
21:51:29 app.api.v1.ai INFO   [AI续写] context内容: '的猫，无声无息地从掩体后窜出，踩着一根悬空的钢梁，轻松地跃到对面一处还算完整的楼层平台。 “嘎吱——” 脚下的楼板发出一声令人牙酸的呻吟，无数裂纹如蛛网般蔓延。凌风的瞳孔骤然一缩，身体瞬间绷紧，重心压低，几乎是贴着地面滑行了数米，才堪堪避开了那片最不稳定的区域。 冷汗，从他的额角渗出。在这片钢铁坟场里，最大的敌人往往不是变异的怪物或是“机械神教”那些冷酷的巡逻机器人，而是这片沉默的废墟本身。'
21:51:29 app.api.v1.ai INFO   [AI续写] prompt: '续写', max_tokens: 100
21:51:29 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
21:51:29 app.services.ai.http_ai_service INFO   ModelSelector 已启用
21:51:29 app.services.ai.http_ai_service INFO   AILogService 已启用 (用于成本追踪)
21:51:32 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
21:51:32 app.services.ai.http_ai_service INFO   API 响应完成，共接收 54 个数据块，总长度: 5299
21:51:32 app.services.ai.http_ai_service INFO   流式响应Token统计: 7067 (prompt=3562, completion=3505)
21:51:32 app.services.ai.http_ai_service INFO   AI自动补全请求 - 上下文长度: 197, work_id: None
21:51:32 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=100, temp=0.7, task_type=None
21:51:32 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/complete
INFO:     127.0.0.1:62299 - "POST /api/v1/ai/complete HTTP/1.1" 200 OK
21:51:32 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=7067, cost=$0.039502, time=31715ms
21:51:32 app.services.agent.langgraph_agent INFO   ✅ [Agent分析] 分析完成，结果长度: 5299
21:51:32 app.services.agent.langgraph_agent INFO   [ParallelExecution] 串行任务3完成
21:51:32 app.api.v1.agent INFO   [Stream] 任务完成: 分析第四章内容，提取关键情节和主题 (31.7s)
21:51:32 app.services.agent.langgraph_agent INFO   [ParallelExecution] 串行任务4开始: 根据作品上下文和第四章分析结果，构思第五章的可能名称
21:51:32 app.api.v1.agent INFO   [Stream] 任务开始: 根据作品上下文和第四章分析结果，构思第五章的可能名称
21:51:32 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: complex
21:51:32 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=content_creation, 模型=gemini-2.5-pro, 原因=任务复杂度为 complex; 任务类型: content_creation; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
21:51:32 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.8, task_type=TaskType.CONTENT_CREATION
21:51:35 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
21:51:35 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
21:51:58 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 25
21:51:58 app.services.ai.http_ai_service INFO   流式响应Token统计: 2763 (prompt=2746, completion=17)
21:51:58 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:实例): tokens=2763, cost=$0.003603, time=26579ms
21:51:58 app.api.v1.ai INFO   [AI续写] 用户 testuser_new-1 请求完成，生成字数: 25
21:52:15 app.api.v1.ai INFO   [AI续写] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), 上下文长度: 197, 风格: 默认, work_id: None, chapter_id: None
21:52:15 app.api.v1.ai INFO   [AI续写] context内容: '的猫，无声无息地从掩体后窜出，踩着一根悬空的钢梁，轻松地跃到对面一处还算完整的楼层平台。 “嘎吱——” 脚下的楼板发出一声令人牙酸的呻吟，无数裂纹如蛛网般蔓延。凌风的瞳孔骤然一缩，身体瞬间绷紧，重心压低，几乎是贴着地面滑行了数米，才堪堪避开了那片最不稳定的区域。 冷汗，从他的额角渗出。在这片钢铁坟场里，最大的敌人往往不是变异的怪物或是“机械神教”那些冷酷的巡逻机器人，而是这片沉默的废墟本身。'
21:52:15 app.api.v1.ai INFO   [AI续写] prompt: '续写', max_tokens: 100
21:52:15 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
21:52:15 app.services.ai.http_ai_service INFO   ModelSelector 已启用
21:52:15 app.services.ai.http_ai_service INFO   AILogService 已启用 (用于成本追踪)
21:52:16 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
21:52:16 app.services.ai.http_ai_service INFO   AI自动补全请求 - 上下文长度: 197, work_id: None
21:52:16 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=100, temp=0.7, task_type=None
21:52:16 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/complete
INFO:     127.0.0.1:64643 - "POST /api/v1/ai/complete HTTP/1.1" 200 OK
21:52:19 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
21:52:37 app.services.ai.http_ai_service INFO   API 响应完成，共接收 26 个数据块，总长度: 2196
21:52:37 app.services.ai.http_ai_service INFO   流式响应Token统计: 7541 (prompt=5933, completion=1608)
21:52:37 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=7541, cost=$0.023496, time=65456ms
21:52:37 app.services.agent.langgraph_agent INFO   [ParallelExecution] 串行任务4完成
21:52:37 app.api.v1.agent INFO   [Stream] 任务完成: 根据作品上下文和第四章分析结果，构思第五章的可能名称 (65.5s)
21:52:37 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共4个任务，耗时: 97.42s
21:52:37 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
21:52:37 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=1, 输出型=2, 展示型=1
21:52:37 app.services.agent.langgraph_agent INFO   [Response] 2个输出任务，简单拼接
21:52:37 app.api.v1.agent INFO   [Stream] 跳过最终响应（内容已流式发送）
21:52:37 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed
21:52:43 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 22
21:52:43 app.services.ai.http_ai_service INFO   流式响应Token统计: 2416 (prompt=2402, completion=14)
21:52:43 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:实例): tokens=2416, cost=$0.003142, time=27563ms
21:52:43 app.api.v1.ai INFO   [AI续写] 用户 testuser_new-1 请求完成，生成字数: 22
21:52:54 app.api.v1.ai INFO   [AI续写] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), 上下文长度: 197, 风格: 默认, work_id: None, chapter_id: None
21:52:54 app.api.v1.ai INFO   [AI续写] context内容: '的猫，无声无息地从掩体后窜出，踩着一根悬空的钢梁，轻松地跃到对面一处还算完整的楼层平台。 “嘎吱——” 脚下的楼板发出一声令人牙酸的呻吟，无数裂纹如蛛网般蔓延。凌风的瞳孔骤然一缩，身体瞬间绷紧，重心压低，几乎是贴着地面滑行了数米，才堪堪避开了那片最不稳定的区域。 冷汗，从他的额角渗出。在这片钢铁坟场里，最大的敌人往往不是变异的怪物或是“机械神教”那些冷酷的巡逻机器人，而是这片沉默的废墟本身。'
21:52:54 app.api.v1.ai INFO   [AI续写] prompt: '续写', max_tokens: 100
21:52:54 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
21:52:54 app.services.ai.http_ai_service INFO   ModelSelector 已启用
21:52:54 app.services.ai.http_ai_service INFO   AILogService 已启用 (用于成本追踪)
21:52:55 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
21:52:55 app.services.ai.http_ai_service INFO   AI自动补全请求 - 上下文长度: 197, work_id: None
21:52:55 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=100, temp=0.7, task_type=None
21:52:55 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/complete
INFO:     127.0.0.1:61765 - "POST /api/v1/ai/complete HTTP/1.1" 200 OK
21:53:00 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
21:53:20 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 25
21:53:20 app.services.ai.http_ai_service INFO   流式响应Token统计: 2463 (prompt=2453, completion=10)
21:53:20 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:实例): tokens=2463, cost=$0.003166, time=24459ms
21:53:20 app.api.v1.ai INFO   [AI续写] 用户 testuser_new-1 请求完成，生成字数: 25
21:53:33 app.api.v1.ai INFO   [AI续写] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), 上下文长度: 196, 风格: 默认, work_id: None, chapter_id: None
21:53:33 app.api.v1.ai INFO   [AI续写] context内容: '声音穿透了层层钢筋水泥，带着一股令人灵魂战栗的威压，仿佛有一头史前巨兽正在苏醒。 是“掘墓者”！一种常年盘踞在废墟地下的强大变异体！ 凌风的脸色瞬间变得惨白。他很清楚，那声音距离自己并不算远，而且正在快速靠近！ 来不及多想，他一把将仍在发光的黑盒塞进背包，拉上拉链。然后，他像是想起了什么，猛地转身，在那被撬开的储物柜最深处，摸出了一罐被遗忘在角落里的东西。 是一罐没有标签，但保存完好的午餐'
21:53:33 app.api.v1.ai INFO   [AI续写] prompt: '续写', max_tokens: 100
21:53:33 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
21:53:33 app.services.ai.http_ai_service INFO   ModelSelector 已启用
21:53:33 app.services.ai.http_ai_service INFO   AILogService 已启用 (用于成本追踪)
21:53:34 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
21:53:34 app.services.ai.http_ai_service INFO   AI自动补全请求 - 上下文长度: 196, work_id: None
21:53:34 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=100, temp=0.7, task_type=None
21:53:34 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/complete
INFO:     127.0.0.1:50421 - "POST /api/v1/ai/complete HTTP/1.1" 200 OK
21:53:38 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
21:53:56 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 22
21:53:56 app.services.ai.http_ai_service INFO   流式响应Token统计: 2187 (prompt=2171, completion=16)
21:53:56 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:实例): tokens=2187, cost=$0.002874, time=21826ms
21:53:56 app.api.v1.ai INFO   [AI续写] 用户 testuser_new-1 请求完成，生成字数: 22
INFO:     127.0.0.1:59971 - "OPTIONS /api/v1/agent/chat/stream HTTP/1.1" 200 OK
21:56:40 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
21:56:40 app.services.ai.http_ai_service INFO   ModelSelector 已启用
21:56:40 app.services.ai.http_ai_service INFO   AILogService 已启用 (用于成本追踪)
21:56:42 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
21:56:42 app.api.v1.agent INFO   [Chat Stream] Mode: planning
21:56:42 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:59971 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
21:56:42 app.api.v1.agent INFO   [Session] 创建新会话归属: e58a0de5-6318-4abe-9917-4593b5f24997 -> 602f5147-846a-4cde-95d3-405fa75f133f
21:56:42 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: planning, Message: 给第五章起名字。不是续写第五章...
21:56:42 app.services.agent.langgraph_agent INFO   [Planning] 使用隔离的thread_id: ad948837-e94e-4d0f-92a4-a75cf1301b07:e58a0de5-6318-4abe-9917-4593b5f24997 (work_id=ad948837-e94e-4d0f-92a4-a75cf1301b07, conversation_id=e58a0de5-6318-4abe-9917-4593b5f24997)
21:56:42 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: 给第五章起名字。不是续写第五章...
21:56:42 app.core.cache INFO   ✅ 缓存命中: prompt:get_planning_static_prompt:fca6eb91156619d0
21:56:42 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
21:56:42 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
21:56:42 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=600, temp=0.3, task_type=TaskType.SIMPLE_QA
21:56:46 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
21:56:52 app.services.ai.http_ai_service INFO   API 响应完成，共接收 3 个数据块，总长度: 449
21:56:52 app.services.ai.http_ai_service INFO   流式响应Token统计: 2385 (prompt=2192, completion=193)
21:56:52 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2385, cost=$0.004670, time=9437ms
21:56:52 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=2385
21:56:52 app.services.agent.langgraph_agent INFO   [JSON解析] 方法2成功: 从```json块提取
21:56:52 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共2个任务，耗时: 9.46s
21:56:52 app.api.v1.agent INFO   [Stream] 规划生成: 2 个任务
21:56:52 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
21:56:52 app.services.agent.parameter_resolver INFO   [ParameterResolver] 初始化完成, 严格模式: False
21:56:52 app.services.agent.langgraph_agent INFO   [ParameterResolver] 参数解析器已启用
21:56:52 app.services.agent.langgraph_agent INFO   [ParallelExecution] 任务分组: 并行=1, 串行=1
21:56:52 app.services.agent.langgraph_agent INFO   [ParallelExecution] 开始并行执行1个任务
21:56:52 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务1开始: 读取指定章节内容
21:56:52 app.api.v1.agent INFO   [Stream] 任务开始: 读取指定章节内容
21:56:52 app.services.agent.langgraph_agent INFO   [read_chapter_tool] ✅ 读取章节成功: 钢铁坟场
21:56:52 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务1完成
21:56:52 app.api.v1.agent INFO   [Stream] 任务完成: 读取指定章节内容 (0.0s)
21:56:52 app.services.agent.langgraph_agent INFO   [ParallelExecution] 开始串行执行1个任务
21:56:52 app.services.agent.langgraph_agent INFO   [ParallelExecution] 串行任务2开始: 分析章节内容以生成标题
21:56:52 app.api.v1.agent INFO   [Stream] 任务开始: 分析章节内容以生成标题
21:56:52 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
21:56:52 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
21:56:52 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
21:56:54 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
21:57:15 app.services.ai.http_ai_service INFO   API 响应完成，共接收 37 个数据块，总长度: 2953
21:57:15 app.services.ai.http_ai_service INFO   流式响应Token统计: 6719 (prompt=4933, completion=1786)
21:57:15 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=6719, cost=$0.024026, time=23103ms
21:57:15 app.services.agent.langgraph_agent INFO   ✅ [Agent分析] 分析完成，结果长度: 2953
21:57:15 app.services.agent.langgraph_agent INFO   [ParallelExecution] 串行任务2完成
21:57:15 app.api.v1.agent INFO   [Stream] 任务完成: 分析章节内容以生成标题 (23.1s)
21:57:15 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共2个任务，耗时: 23.15s
21:57:15 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
21:57:15 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=0, 输出型=1, 展示型=1
21:57:15 app.services.agent.langgraph_agent INFO   [Response] 单个分析任务(analyze_text_tool)，使用AI格式化
21:57:15 app.services.agent.langgraph_agent INFO   [Summarization] 使用AI整合任务结果
21:57:15 app.services.agent.langgraph_agent INFO   [Summarization] 上下文压缩: 原始=6079字符, 压缩后=4094字符, 压缩率=33%
21:57:15 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
21:57:15 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
21:57:15 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
21:57:17 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
21:57:24 app.services.ai.http_ai_service INFO   API 响应完成，共接收 4 个数据块，总长度: 363
21:57:24 app.services.ai.http_ai_service INFO   流式响应Token统计: 4016 (prompt=3775, completion=241)
21:57:24 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4016, cost=$0.007129, time=9094ms
21:57:24 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=4016
21:57:24 app.api.v1.agent INFO   [Stream] 跳过最终响应（内容已流式发送）
21:57:24 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed
21:58:18 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
21:58:18 app.services.ai.http_ai_service INFO   ModelSelector 已启用
21:58:18 app.services.ai.http_ai_service INFO   AILogService 已启用 (用于成本追踪)
21:58:20 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
21:58:20 app.api.v1.agent INFO   [Chat Stream] Mode: planning
21:58:20 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:60212 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
21:58:20 app.api.v1.agent INFO   [Session] 创建新会话归属: 769c4a74-49d5-448a-b425-dc8aefadaf9e -> 602f5147-846a-4cde-95d3-405fa75f133f
21:58:20 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: planning, Message: 分析前面四章内容，来写第五章...
21:58:20 app.services.agent.langgraph_agent INFO   [Planning] 使用隔离的thread_id: ad948837-e94e-4d0f-92a4-a75cf1301b07:769c4a74-49d5-448a-b425-dc8aefadaf9e (work_id=ad948837-e94e-4d0f-92a4-a75cf1301b07, conversation_id=769c4a74-49d5-448a-b425-dc8aefadaf9e)
21:58:20 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: 分析前面四章内容，来写第五章...
21:58:20 app.core.cache INFO   ✅ 缓存命中: prompt:get_planning_static_prompt:fca6eb91156619d0
21:58:20 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
21:58:20 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
21:58:20 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=600, temp=0.3, task_type=TaskType.SIMPLE_QA
21:58:22 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
21:58:30 app.services.ai.http_ai_service INFO   API 响应完成，共接收 10 个数据块，总长度: 1484
21:58:30 app.services.ai.http_ai_service INFO   流式响应Token统计: 3591 (prompt=2952, completion=639)
21:58:30 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=3591, cost=$0.010080, time=9584ms
21:58:30 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=3591
21:58:30 app.services.agent.langgraph_agent INFO   [JSON解析] 方法2成功: 从```json块提取
21:58:30 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共7个任务，耗时: 9.62s
21:58:30 app.api.v1.agent INFO   [Stream] 规划生成: 7 个任务
21:58:30 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
21:58:30 app.services.agent.parameter_resolver INFO   [ParameterResolver] 初始化完成, 严格模式: False
21:58:30 app.services.agent.langgraph_agent INFO   [ParameterResolver] 参数解析器已启用
21:58:30 app.services.agent.langgraph_agent INFO   [ParallelExecution] 任务分组: 并行=5, 串行=2
21:58:30 app.services.agent.langgraph_agent INFO   [ParallelExecution] 开始并行执行5个任务
21:58:30 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务1开始: 获取作品上下文和当前章节信息
21:58:30 app.api.v1.agent INFO   [Stream] 任务开始: 获取作品上下文和当前章节信息
21:58:30 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务2开始: 获取第一章内容
21:58:30 app.api.v1.agent INFO   [Stream] 任务开始: 获取第一章内容
21:58:30 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务3开始: 获取第二章内容
21:58:30 app.api.v1.agent INFO   [Stream] 任务开始: 获取第二章内容
21:58:30 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务4开始: 获取第三章内容
21:58:30 app.api.v1.agent INFO   [Stream] 任务开始: 获取第三章内容
21:58:30 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务5开始: 获取第四章内容
21:58:30 app.api.v1.agent INFO   [Stream] 任务开始: 获取第四章内容
21:58:30 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=ad948837-e94e-4d0f-92a4-a75cf1301b07, chapter_id=ef5eb68c-32b8-4249-83a3-31d57363c0a9
21:58:30 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第4章: 天眼与土獾
21:58:30 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 钢铁坟场
21:58:30 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第2章: 归巢与低语
21:58:30 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第3章: 遗落的星图
21:58:30 app.services.vector_store_service INFO   RAG检索: work_id=ad948837-e94e-4d0f-92a4-a75cf1301b07, query=作品背景和设定...
21:58:30 app.services.vector_store_service INFO   检索到 0 个相关结果（阈值=0.4）
21:58:30 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=大寂灭
21:58:30 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务5完成
21:58:30 app.api.v1.agent INFO   [Stream] 任务完成: 获取第四章内容 (0.3s)
21:58:30 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务2完成
21:58:30 app.api.v1.agent INFO   [Stream] 任务完成: 获取第一章内容 (0.3s)
21:58:30 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务3完成
21:58:30 app.api.v1.agent INFO   [Stream] 任务完成: 获取第二章内容 (0.3s)
21:58:30 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务4完成
21:58:30 app.api.v1.agent INFO   [Stream] 任务完成: 获取第三章内容 (0.3s)
21:58:30 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务1完成
21:58:30 app.api.v1.agent INFO   [Stream] 任务完成: 获取作品上下文和当前章节信息 (0.3s)
21:58:30 app.services.agent.langgraph_agent INFO   [ParallelExecution] 开始串行执行2个任务
21:58:30 app.services.agent.langgraph_agent INFO   [ParallelExecution] 串行任务6开始: 分析前四章内容，提取关键信息
21:58:30 app.api.v1.agent INFO   [Stream] 任务开始: 分析前四章内容，提取关键信息
21:58:30 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
21:58:30 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
21:58:30 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
21:58:32 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
21:59:22 app.services.ai.http_ai_service INFO   API 响应完成，共接收 94 个数据块，总长度: 6569
21:59:22 app.services.ai.http_ai_service INFO   流式响应Token统计: 18539 (prompt=14015, completion=4524)
21:59:22 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=18539, cost=$0.062759, time=51764ms
21:59:22 app.services.agent.langgraph_agent INFO   ✅ [Agent分析] 分析完成，结果长度: 6569
21:59:22 app.services.agent.langgraph_agent INFO   [ParallelExecution] 串行任务6完成
21:59:22 app.api.v1.agent INFO   [Stream] 任务完成: 分析前四章内容，提取关键信息 (51.8s)
21:59:22 app.services.agent.langgraph_agent INFO   [ParallelExecution] 串行任务7开始: 根据分析结果续写第五章
21:59:22 app.api.v1.agent INFO   [Stream] 任务开始: 根据分析结果续写第五章
21:59:22 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: complex
21:59:22 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=content_creation, 模型=gemini-2.5-pro, 原因=任务复杂度为 complex; 任务类型: content_creation; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
21:59:22 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.8, task_type=TaskType.CONTENT_CREATION
21:59:24 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
22:00:03 app.services.ai.http_ai_service INFO   API 响应完成，共接收 71 个数据块，总长度: 2283
22:00:03 app.services.ai.http_ai_service INFO   流式响应Token统计: 8308 (prompt=6565, completion=1743)
22:00:03 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=8308, cost=$0.025636, time=41370ms
22:00:03 app.services.agent.langgraph_agent INFO   [ParallelExecution] 串行任务7完成
22:00:03 app.api.v1.agent INFO   [Stream] 任务完成: 根据分析结果续写第五章 (41.4s)
22:00:03 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共7个任务，耗时: 93.52s
22:00:03 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
22:00:03 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=1, 输出型=2, 展示型=4
22:00:03 app.services.agent.langgraph_agent INFO   [Response] 2个输出任务，简单拼接
22:00:03 app.api.v1.agent INFO   [Stream] 跳过最终响应（内容已流式发送）
22:00:03 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed
INFO:     127.0.0.1:64514 - "OPTIONS /api/v1/chapters HTTP/1.1" 200 OK
22:00:42 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:ad948837-e94e-4d0f-92a4-a75cf1301b07
22:00:42 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/chapters
INFO:     127.0.0.1:64514 - "POST /api/v1/chapters HTTP/1.1" 201 Created
INFO:     127.0.0.1:64514 - "OPTIONS /api/v1/analysis/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/start HTTP/1.1" 200 OK
22:00:43 app.services.novel_analysis_service INFO   Analysis already exists for work ad948837-e94e-4d0f-92a4-a75cf1301b07, status: AnalysisStatus.ANALYZING
22:00:43 app.api.v1.novel_analysis INFO   User 602f5147-846a-4cde-95d3-405fa75f133f started analysis for work ad948837-e94e-4d0f-92a4-a75cf1301b07, analysis_id: 9e3368de-0b78-4e20-9b70-3443e01c4358
22:00:43 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/analysis/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/start
INFO:     127.0.0.1:64514 - "POST /api/v1/analysis/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/start HTTP/1.1" 201 Created
22:00:43 app.api.v1.novel_analysis INFO   后台任务开始：分析作品 ad948837-e94e-4d0f-92a4-a75cf1301b07
22:00:43 app.api.v1.novel_analysis INFO   后台任务已找到分析记录 analysis_id=9e3368de-0b78-4e20-9b70-3443e01c4358
22:00:43 app.services.ai.novel_analysis_orchestrator INFO   ============================================================
22:00:43 app.services.ai.novel_analysis_orchestrator INFO   开始分析作品: ad948837-e94e-4d0f-92a4-a75cf1301b07
22:00:43 app.services.ai.novel_analysis_orchestrator INFO   ============================================================
22:00:43 app.services.novel_analysis_service INFO   Updated analysis 9e3368de-0b78-4e20-9b70-3443e01c4358 progress: 0/4, stage: AnalysisStage.MICRO_ANALYSIS, status: AnalysisStatus.ANALYZING
22:00:43 app.services.ai.novel_analysis_orchestrator INFO   初始化AI分析服务...
22:00:43 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
22:00:43 app.services.ai.http_ai_service INFO   ModelSelector 已启用
22:00:43 app.services.ai.http_ai_service INFO   AILogService 已启用 (用于成本追踪)
22:00:45 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
22:00:45 app.services.ai.novel_micro_analysis INFO   微观分析提示词加载成功
22:00:45 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
22:00:45 app.services.ai.http_ai_service INFO   ModelSelector 已启用
22:00:45 app.services.ai.http_ai_service INFO   AILogService 已启用 (用于成本追踪)
22:00:47 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
22:00:47 app.services.ai.novel_macro_analysis INFO   宏观分析提示词加载成功
22:00:47 app.services.ai.novel_analysis_orchestrator ERROR   分析前验证失败: 1/5 章节内容不足
22:00:47 app.services.ai.novel_analysis_orchestrator ERROR   分析流程失败: 无法开始分析：以下 1 个章节内容为空或过短

  - 红雾下的星图 (当前0字符)

要求：每个章节至少需要 100 字符的内容
建议：填写章节内容后再触发分析，以获得完整的分析报告
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\services\ai\novel_analysis_orchestrator.py", line 170, in _run_analysis_internal
    raise ValueError(error_msg)
ValueError: 无法开始分析：以下 1 个章节内容为空或过短

  - 红雾下的星图 (当前0字符)

要求：每个章节至少需要 100 字符的内容
建议：填写章节内容后再触发分析，以获得完整的分析报告
INFO:     127.0.0.1:63146 - "OPTIONS /api/v1/chapters/484090bc-6bd4-4118-8fd4-5c988e4a2c98 HTTP/1.1" 200 OK
INFO:     127.0.0.1:64514 - "OPTIONS /api/v1/chapters/484090bc-6bd4-4118-8fd4-5c988e4a2c98 HTTP/1.1" 200 OK
22:00:47 app.services.novel_analysis_service ERROR   Marked analysis 9e3368de-0b78-4e20-9b70-3443e01c4358 as failed: 无法开始分析：以下 1 个章节内容为空或过短

  - 红雾下的星图 (当前0字符)

要求：每个章节至少需要 100 字符的内容
建议：填写章节内容后再触发分析，以获得完整的分析报告
22:00:47 app.services.ai.novel_analysis_orchestrator INFO   AI服务资源已清理
22:00:47 app.services.ai.novel_analysis_orchestrator INFO   AI服务资源已清理
22:00:47 app.api.v1.novel_analysis ERROR   后台任务失败：作品 ad948837-e94e-4d0f-92a4-a75cf1301b07 分析失败
22:00:47 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:ad948837-e94e-4d0f-92a4-a75cf1301b07
22:00:47 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/484090bc-6bd4-4118-8fd4-5c988e4a2c98
INFO:     127.0.0.1:58610 - "PUT /api/v1/chapters/484090bc-6bd4-4118-8fd4-5c988e4a2c98 HTTP/1.1" 200 OK
22:00:47 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:ad948837-e94e-4d0f-92a4-a75cf1301b07
22:00:47 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/484090bc-6bd4-4118-8fd4-5c988e4a2c98
INFO:     127.0.0.1:59697 - "PUT /api/v1/chapters/484090bc-6bd4-4118-8fd4-5c988e4a2c98 HTTP/1.1" 200 OK
INFO:     127.0.0.1:59697 - "OPTIONS /api/v1/chapters/298f5ac1-437c-4087-919b-5db66b1b3b14 HTTP/1.1" 200 OK
INFO:     127.0.0.1:58610 - "OPTIONS /api/v1/chapters/298f5ac1-437c-4087-919b-5db66b1b3b14 HTTP/1.1" 200 OK
22:00:51 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:ad948837-e94e-4d0f-92a4-a75cf1301b07
22:00:51 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:ad948837-e94e-4d0f-92a4-a75cf1301b07
22:00:51 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/298f5ac1-437c-4087-919b-5db66b1b3b14
22:00:51 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/298f5ac1-437c-4087-919b-5db66b1b3b14
INFO:     127.0.0.1:58610 - "PUT /api/v1/chapters/298f5ac1-437c-4087-919b-5db66b1b3b14 HTTP/1.1" 200 OK
INFO:     127.0.0.1:59697 - "PUT /api/v1/chapters/298f5ac1-437c-4087-919b-5db66b1b3b14 HTTP/1.1" 200 OK
INFO:     127.0.0.1:59697 - "OPTIONS /api/v1/chapters/work/ad948837-e94e-4d0f-92a4-a75cf1301b07 HTTP/1.1" 200 OK
INFO:     127.0.0.1:58610 - "OPTIONS /api/v1/chapters/work/ad948837-e94e-4d0f-92a4-a75cf1301b07 HTTP/1.1" 200 OK
22:00:55 app.api.v1.chapters INFO   [GET chapters] work_id=ad948837-e94e-4d0f-92a4-a75cf1301b07, user_id=602f5147-846a-4cde-95d3-405fa75f133f
22:00:55 app.api.v1.chapters INFO   ⚠️ [GET chapters] 缓存未命中: chapters:work:ad948837-e94e-4d0f-92a4-a75cf1301b07
22:00:55 app.services.chapter_service INFO   [ChapterService] Querying chapters for work_id=ad948837-e94e-4d0f-92a4-a75cf1301b07, type=<class 'uuid.UUID'>
22:00:55 app.services.chapter_service INFO   [ChapterService] Found 5 chapters
22:00:55 app.services.chapter_service INFO     - Chapter: 钢铁坟场, order=1
22:00:55 app.services.chapter_service INFO     - Chapter: 归巢与低语, order=2
22:00:55 app.services.chapter_service INFO     - Chapter: 遗落的星图, order=3
22:00:55 app.services.chapter_service INFO     - Chapter: 天眼与土獾, order=4
22:00:55 app.services.chapter_service INFO     - Chapter: 红雾下的星图, order=5
22:00:55 app.api.v1.chapters INFO   [GET chapters] Returning 5 chapters
22:00:55 app.api.v1.chapters INFO   💾 [GET chapters] 缓存已保存: chapters:work:ad948837-e94e-4d0f-92a4-a75cf1301b07 (expire=60s)
22:00:55 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/chapters/work/ad948837-e94e-4d0f-92a4-a75cf1301b07
INFO:     127.0.0.1:58610 - "GET /api/v1/chapters/work/ad948837-e94e-4d0f-92a4-a75cf1301b07 HTTP/1.1" 200 OK
22:00:55 app.api.v1.chapters INFO   [GET chapters] work_id=ad948837-e94e-4d0f-92a4-a75cf1301b07, user_id=602f5147-846a-4cde-95d3-405fa75f133f
22:00:55 app.api.v1.chapters INFO   ✅ [GET chapters] 缓存命中: chapters:work:ad948837-e94e-4d0f-92a4-a75cf1301b07
22:00:55 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/chapters/work/ad948837-e94e-4d0f-92a4-a75cf1301b07
INFO:     127.0.0.1:59697 - "GET /api/v1/chapters/work/ad948837-e94e-4d0f-92a4-a75cf1301b07 HTTP/1.1" 200 OK
22:00:56 app.api.v1.chapters INFO   [GET chapters] work_id=ad948837-e94e-4d0f-92a4-a75cf1301b07, user_id=602f5147-846a-4cde-95d3-405fa75f133f
22:00:56 app.api.v1.chapters INFO   ✅ [GET chapters] 缓存命中: chapters:work:ad948837-e94e-4d0f-92a4-a75cf1301b07
22:00:56 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/chapters/work/ad948837-e94e-4d0f-92a4-a75cf1301b07
INFO:     127.0.0.1:59697 - "GET /api/v1/chapters/work/ad948837-e94e-4d0f-92a4-a75cf1301b07 HTTP/1.1" 200 OK
22:00:56 app.api.v1.chapters INFO   [GET chapters] work_id=ad948837-e94e-4d0f-92a4-a75cf1301b07, user_id=602f5147-846a-4cde-95d3-405fa75f133f
22:00:56 app.api.v1.chapters INFO   ✅ [GET chapters] 缓存命中: chapters:work:ad948837-e94e-4d0f-92a4-a75cf1301b07
22:00:56 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/chapters/work/ad948837-e94e-4d0f-92a4-a75cf1301b07
INFO:     127.0.0.1:58610 - "GET /api/v1/chapters/work/ad948837-e94e-4d0f-92a4-a75cf1301b07 HTTP/1.1" 200 OK
INFO:     127.0.0.1:58610 - "OPTIONS /api/v1/chapters/ef5eb68c-32b8-4249-83a3-31d57363c0a9 HTTP/1.1" 200 OK
INFO:     127.0.0.1:59697 - "OPTIONS /api/v1/chapters/ef5eb68c-32b8-4249-83a3-31d57363c0a9 HTTP/1.1" 200 OK
22:00:59 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:ad948837-e94e-4d0f-92a4-a75cf1301b07
22:00:59 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:ad948837-e94e-4d0f-92a4-a75cf1301b07
22:00:59 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/ef5eb68c-32b8-4249-83a3-31d57363c0a9
22:00:59 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/ef5eb68c-32b8-4249-83a3-31d57363c0a9
INFO:     127.0.0.1:58610 - "PUT /api/v1/chapters/ef5eb68c-32b8-4249-83a3-31d57363c0a9 HTTP/1.1" 200 OK
INFO:     127.0.0.1:59697 - "PUT /api/v1/chapters/ef5eb68c-32b8-4249-83a3-31d57363c0a9 HTTP/1.1" 200 OK
22:01:14 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:ad948837-e94e-4d0f-92a4-a75cf1301b07
22:01:14 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/484090bc-6bd4-4118-8fd4-5c988e4a2c98
INFO:     127.0.0.1:51529 - "PUT /api/v1/chapters/484090bc-6bd4-4118-8fd4-5c988e4a2c98 HTTP/1.1" 200 OK
22:01:14 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:ad948837-e94e-4d0f-92a4-a75cf1301b07
22:01:14 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/484090bc-6bd4-4118-8fd4-5c988e4a2c98
INFO:     127.0.0.1:51529 - "PUT /api/v1/chapters/484090bc-6bd4-4118-8fd4-5c988e4a2c98 HTTP/1.1" 200 OK
22:01:19 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:ad948837-e94e-4d0f-92a4-a75cf1301b07
22:01:19 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/484090bc-6bd4-4118-8fd4-5c988e4a2c98
INFO:     127.0.0.1:52212 - "PUT /api/v1/chapters/484090bc-6bd4-4118-8fd4-5c988e4a2c98 HTTP/1.1" 200 OK
22:01:19 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:ad948837-e94e-4d0f-92a4-a75cf1301b07
22:01:19 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/484090bc-6bd4-4118-8fd4-5c988e4a2c98
INFO:     127.0.0.1:52212 - "PUT /api/v1/chapters/484090bc-6bd4-4118-8fd4-5c988e4a2c98 HTTP/1.1" 200 OK
