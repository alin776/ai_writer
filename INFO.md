09:29:49 app.api.v1.agent INFO   [Redis] 全局连接池已创建
已注册策略: web_novel_11d - 网文11维度分析
09:29:50 app.utils.file_storage INFO   临时文件存储目录: D:\Temp\novelaide_exports
09:29:50 app.main INFO   [STARTUP] 监控中间件已注册: TraceMiddleware, MonitoringMiddleware
INFO:     Started server process [30936]
INFO:     Waiting for application startup.
09:29:50 app.main INFO   [STARTUP] 应用启动中...
09:29:50 app.core.database INFO   正在初始化数据库... (尝试 1/3)
09:29:50 app.core.database INFO   ✅ 数据库初始化成功
09:29:50 apscheduler.scheduler INFO   Adding job tentatively -- it will be properly scheduled when the scheduler starts
09:29:50 apscheduler.scheduler INFO   Added job "清理过期的去痕迹会话详情" to job store "default"
09:29:50 apscheduler.scheduler INFO   Scheduler started
09:29:50 app.tasks.cleanup_humanize_details INFO   定时任务调度器已启动
09:29:50 app.main INFO   [STARTUP] 开始预初始化同步Redis连接...
09:29:50 app.main INFO   [STARTUP] ✅ 同步Redis连接池预初始化完成
09:29:50 app.main INFO   [STARTUP] 开始初始化AsyncRedisSaver索引...
09:29:50 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ setup_checkpointer Redis连接验证成功
09:29:50 redisvl.index.index INFO   Index already exists, not overwriting.
09:29:50 redisvl.index.index INFO   Index already exists, not overwriting.
09:29:50 redisvl.index.index INFO   Index already exists, not overwriting.
09:29:50 langgraph.checkpoint.redis.aio INFO   Redis client is a standalone client
09:29:50 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ AsyncRedisSaver索引预创建成功
09:29:50 app.main INFO   [STARTUP] AsyncRedisSaver索引初始化完成
09:29:50 app.main INFO   [STARTUP] 开始预加载Embedding模型...
09:29:50 app.services.vector_store_service INFO   🔄 预加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
09:29:57 app.services.vector_store_service INFO   ✅ Embedding模型预加载成功，耗时: 7.03秒
09:29:57 app.main INFO   [STARTUP] Embedding模型预加载完成
09:29:57 app.main INFO   [STARTUP] P0性能优化已暂时禁用（诊断模式）
09:29:57 app.main INFO   [STARTUP] 应用启动完成
INFO:     Application startup complete.
INFO:     127.0.0.1:61766 - "OPTIONS /api/v1/works HTTP/1.1" 200 OK
INFO:     127.0.0.1:65104 - "OPTIONS /api/v1/works HTTP/1.1" 200 OK
09:30:51 monitoring INFO   Registered health check: cpu_usage
09:30:51 monitoring INFO   Registered health check: memory_usage
09:30:51 monitoring INFO   Registered health check: disk_usage
09:30:51 monitoring INFO   Registered health check: process_status
09:30:51 monitoring INFO   Added alert rule: high_cpu_usage
09:30:51 monitoring INFO   Added alert rule: high_memory_usage
09:30:51 monitoring INFO   Added alert rule: low_disk_space
09:30:51 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works
INFO:     127.0.0.1:65104 - "GET /api/v1/works HTTP/1.1" 200 OK
09:30:51 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works
INFO:     127.0.0.1:65104 - "GET /api/v1/works HTTP/1.1" 200 OK
INFO:     127.0.0.1:65104 - "OPTIONS /api/v1/works/ad948837-e94e-4d0f-92a4-a75cf1301b07 HTTP/1.1" 200 OK
INFO:     127.0.0.1:61766 - "OPTIONS /api/v1/chapters/work/ad948837-e94e-4d0f-92a4-a75cf1301b07 HTTP/1.1" 200 OK
INFO:     127.0.0.1:56279 - "OPTIONS /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/characters HTTP/1.1" 200 OK
INFO:     127.0.0.1:65104 - "OPTIONS /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/locations HTTP/1.1" 200 OK
INFO:     127.0.0.1:61766 - "OPTIONS /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/settings HTTP/1.1" 200 OK
INFO:     127.0.0.1:56279 - "OPTIONS /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:65104 - "OPTIONS /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/ai-guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:61766 - "OPTIONS /api/v1/works/ad948837-e94e-4d0f-92a4-a75cf1301b07 HTTP/1.1" 200 OK
INFO:     127.0.0.1:56279 - "OPTIONS /api/v1/chapters/work/ad948837-e94e-4d0f-92a4-a75cf1301b07 HTTP/1.1" 200 OK
INFO:     127.0.0.1:65104 - "OPTIONS /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/characters HTTP/1.1" 200 OK
INFO:     127.0.0.1:61766 - "OPTIONS /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/locations HTTP/1.1" 200 OK
INFO:     127.0.0.1:56279 - "OPTIONS /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/settings HTTP/1.1" 200 OK
INFO:     127.0.0.1:65104 - "OPTIONS /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:61766 - "OPTIONS /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/ai-guidelines HTTP/1.1" 200 OK
09:30:55 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works/ad948837-e94e-4d0f-92a4-a75cf1301b07
INFO:     127.0.0.1:56279 - "GET /api/v1/works/ad948837-e94e-4d0f-92a4-a75cf1301b07 HTTP/1.1" 200 OK
09:30:55 app.api.v1.worldview INFO   ⚠️ [Worldview] 缓存未命中: worldview:locations:ad948837-e94e-4d0f-92a4-a75cf1301b07
09:30:55 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:locations:ad948837-e94e-4d0f-92a4-a75cf1301b07 (expire=300s)
09:30:55 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/locations
INFO:     127.0.0.1:56279 - "GET /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/locations HTTP/1.1" 200 OK
09:30:55 app.api.v1.chapters INFO   [GET chapters] work_id=ad948837-e94e-4d0f-92a4-a75cf1301b07, user_id=602f5147-846a-4cde-95d3-405fa75f133f
09:30:55 app.api.v1.worldview INFO   ⚠️ [Worldview] 缓存未命中: worldview:settings:ad948837-e94e-4d0f-92a4-a75cf1301b07
09:30:55 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:settings:ad948837-e94e-4d0f-92a4-a75cf1301b07 (expire=300s)
09:30:55 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/settings
INFO:     127.0.0.1:58013 - "GET /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/settings HTTP/1.1" 200 OK
09:30:55 app.api.v1.worldview INFO   ⚠️ [Worldview] 缓存未命中: worldview:locations:ad948837-e94e-4d0f-92a4-a75cf1301b07
09:30:55 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:locations:ad948837-e94e-4d0f-92a4-a75cf1301b07 (expire=300s)
09:30:55 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/locations
INFO:     127.0.0.1:58013 - "GET /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/locations HTTP/1.1" 200 OK
09:30:55 app.api.v1.worldview INFO   ⚠️ [Worldview] 缓存未命中: worldview:characters:ad948837-e94e-4d0f-92a4-a75cf1301b07
09:30:55 app.api.v1.chapters INFO   ⚠️ [GET chapters] 缓存未命中: chapters:work:ad948837-e94e-4d0f-92a4-a75cf1301b07
09:30:55 app.services.chapter_service INFO   [ChapterService] Querying chapters for work_id=ad948837-e94e-4d0f-92a4-a75cf1301b07, type=<class 'uuid.UUID'>
09:30:55 app.api.v1.worldview INFO   ✅ [Worldview] 缓存命中: worldview:settings:ad948837-e94e-4d0f-92a4-a75cf1301b07
09:30:55 app.services.chapter_service INFO   [ChapterService] Found 5 chapters
09:30:55 app.services.chapter_service INFO     - Chapter: 钢铁坟场, order=1
09:30:55 app.services.chapter_service INFO     - Chapter: 归巢与低语, order=2
09:30:55 app.services.chapter_service INFO     - Chapter: 遗落的星图, order=3
09:30:55 app.services.chapter_service INFO     - Chapter: 天眼与土獾, order=4
09:30:55 app.services.chapter_service INFO     - Chapter: 红雾下的星图, order=5
09:30:55 app.api.v1.chapters INFO   [GET chapters] Returning 5 chapters
09:30:55 app.api.v1.chapters INFO   💾 [GET chapters] 缓存已保存: chapters:work:ad948837-e94e-4d0f-92a4-a75cf1301b07 (expire=60s)
09:30:55 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:characters:ad948837-e94e-4d0f-92a4-a75cf1301b07 (expire=300s)
09:30:55 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/settings
INFO:     127.0.0.1:58013 - "GET /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/settings HTTP/1.1" 200 OK
09:30:55 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/chapters/work/ad948837-e94e-4d0f-92a4-a75cf1301b07
09:30:55 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/characters
INFO:     127.0.0.1:65104 - "GET /api/v1/chapters/work/ad948837-e94e-4d0f-92a4-a75cf1301b07 HTTP/1.1" 200 OK
INFO:     127.0.0.1:61766 - "GET /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/characters HTTP/1.1" 200 OK
09:30:55 app.api.v1.chapters INFO   [GET chapters] work_id=ad948837-e94e-4d0f-92a4-a75cf1301b07, user_id=602f5147-846a-4cde-95d3-405fa75f133f
09:30:55 app.api.v1.chapters INFO   ✅ [GET chapters] 缓存命中: chapters:work:ad948837-e94e-4d0f-92a4-a75cf1301b07
09:30:55 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/chapters/work/ad948837-e94e-4d0f-92a4-a75cf1301b07
09:30:55 app.api.v1.worldview INFO   ⚠️ [Worldview] 缓存未命中: worldview:characters:ad948837-e94e-4d0f-92a4-a75cf1301b07
INFO:     127.0.0.1:65104 - "GET /api/v1/chapters/work/ad948837-e94e-4d0f-92a4-a75cf1301b07 HTTP/1.1" 200 OK
09:30:55 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:characters:ad948837-e94e-4d0f-92a4-a75cf1301b07 (expire=300s)
09:30:55 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/characters
INFO:     127.0.0.1:61766 - "GET /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/characters HTTP/1.1" 200 OK
09:30:55 app.api.v1.worldview INFO   ⚠️ [Worldview] 缓存未命中: worldview:guidelines:ad948837-e94e-4d0f-92a4-a75cf1301b07
09:30:55 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works/ad948837-e94e-4d0f-92a4-a75cf1301b07
INFO:     127.0.0.1:56279 - "GET /api/v1/works/ad948837-e94e-4d0f-92a4-a75cf1301b07 HTTP/1.1" 200 OK
09:30:55 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:guidelines:ad948837-e94e-4d0f-92a4-a75cf1301b07 (expire=300s)
09:30:55 app.api.v1.worldview INFO   ⚠️ [Worldview] 缓存未命中: worldview:ai-guidelines:ad948837-e94e-4d0f-92a4-a75cf1301b07
09:30:55 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/guidelines
INFO:     127.0.0.1:64218 - "GET /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/guidelines HTTP/1.1" 200 OK
09:30:55 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:ai-guidelines:ad948837-e94e-4d0f-92a4-a75cf1301b07 (expire=300s)
09:30:55 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/ai-guidelines
INFO:     127.0.0.1:63531 - "GET /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/ai-guidelines HTTP/1.1" 200 OK
09:30:55 app.api.v1.worldview INFO   ✅ [Worldview] 缓存命中: worldview:guidelines:ad948837-e94e-4d0f-92a4-a75cf1301b07
INFO:     127.0.0.1:56279 - "OPTIONS /api/v1/analysis/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/status HTTP/1.1" 200 OK
09:30:55 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/guidelines
INFO:     127.0.0.1:64218 - "GET /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/guidelines HTTP/1.1" 200 OK
09:30:55 app.api.v1.worldview INFO   ✅ [Worldview] 缓存命中: worldview:ai-guidelines:ad948837-e94e-4d0f-92a4-a75cf1301b07
09:30:55 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/ai-guidelines
INFO:     127.0.0.1:63531 - "GET /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/ai-guidelines HTTP/1.1" 200 OK
09:30:55 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/analysis/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/status
INFO:     127.0.0.1:56279 - "GET /api/v1/analysis/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/status HTTP/1.1" 200 OK
09:30:56 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/analysis/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/status
INFO:     127.0.0.1:56279 - "GET /api/v1/analysis/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/status HTTP/1.1" 200 OK
INFO:     127.0.0.1:56279 - "OPTIONS /api/v1/chapters/ef5eb68c-32b8-4249-83a3-31d57363c0a9 HTTP/1.1" 200 OK
09:30:56 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:ad948837-e94e-4d0f-92a4-a75cf1301b07
09:30:56 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/ef5eb68c-32b8-4249-83a3-31d57363c0a9
INFO:     127.0.0.1:56279 - "PUT /api/v1/chapters/ef5eb68c-32b8-4249-83a3-31d57363c0a9 HTTP/1.1" 200 OK
09:30:56 app.services.chapter_vector_service INFO   开始向量化章节: 钢铁坟场 (order=1)
09:30:57 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:ad948837-e94e-4d0f-92a4-a75cf1301b07
09:30:57 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/ef5eb68c-32b8-4249-83a3-31d57363c0a9
INFO:     127.0.0.1:56279 - "PUT /api/v1/chapters/ef5eb68c-32b8-4249-83a3-31d57363c0a9 HTTP/1.1" 200 OK
09:30:57 app.services.chapter_vector_service INFO   开始向量化章节: 钢铁坟场 (order=1)
09:30:57 app.services.chapter_vector_service INFO   ✅ 章节向量存储完成: 钢铁坟场 (6段)
09:30:58 app.services.chapter_vector_service INFO   ✅ 章节向量存储完成: 钢铁坟场 (6段)
INFO:     127.0.0.1:50589 - "OPTIONS /api/v1/agent/chat/stream HTTP/1.1" 200 OK
09:31:37 app.services.ai.prompts INFO   Prompts loaded successfully from D:\Java\ai_writer\backend\app\services\ai\prompts\default.json
09:31:37 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
09:31:37 app.services.ai.http_ai_service INFO   ModelSelector 已启用
09:31:37 app.services.ai.http_ai_service INFO   AILogService 已启用 (用于成本追踪)
09:31:38 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
09:31:38 app.api.v1.agent INFO   [Chat Stream] Mode: planning
09:31:38 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:50589 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
09:31:38 app.core.redis INFO   ✅ Redis connected: redis://localhost:6379/0
09:31:38 app.api.v1.agent INFO   [Session] 创建新会话归属: 7b92904b-470e-4c63-9259-d133c4b734a1 -> 602f5147-846a-4cde-95d3-405fa75f133f
09:31:38 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: planning, Message: 分析前面五章内容，来写第六章...
09:31:38 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
09:31:38 app.services.ai.http_ai_service INFO   ModelSelector 已启用
09:31:38 app.services.ai.http_ai_service WARNING   成本追踪已启用，但未提供db或user_id，成本数据将不会被记录！请检查HTTPAIService初始化参数。
09:31:40 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
09:31:40 app.services.context.adaptive_budget INFO   ✅ 所有预算配置验证通过
09:31:50 app.services.context.vector_memory_store INFO   ✅ VectorMemoryStore初始化成功 | 目录=./data/chroma_db | 模型=paraphrase-multilingual-MiniLM-L12-v2 | 集合=user_memories
09:31:50 app.services.context.manager INFO   ✅ VectorMemoryStore 已初始化
09:31:50 app.services.context.manager INFO   ✅ ContextManager: 长期记忆已启用 (user_id=None)
09:31:50 app.services.context.manager INFO   ✅ ContextManager: 自适应预算已启用
09:31:50 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ ContextManager已初始化（长期记忆已启用，自适应预算已启用，总预算=16000 tokens）
成功加载模板: intent_classifier (版本 2.0.0)
成功加载模板: writing_agent (版本 2.0.0)
成功加载模板: planning_agent (版本 2.0.0)
成功加载模板: tool_agent (版本 2.0.0)
成功加载模板: query_agent (版本 2.0.0)
成功加载模板: system_agent_prompt (版本 2.0.0)
成功加载模板: creative_writing_prompt (版本 1.0.0)
09:31:50 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ PromptManager已初始化
09:31:50 app.services.agent.langgraph_agent INFO   [LangGraph] 使用 HTTPAIService 模式（手动工具调用，绕过 Cloudflare）
09:31:50 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ Redis连接验证成功
09:31:50 app.services.agent.langgraph_agent INFO   [LangGraph] OK 使用 AsyncRedisSaver（redis://localhost:6379/0，TTL=7天）
09:31:50 app.services.agent.memory.metrics INFO   [MemoryMetrics] 监控系统已初始化
09:31:50 app.services.agent.memory.long_term_store INFO   [LongTermStore] Initialized: base_dir=./data/long_term_memory, max_size=50KB, compression=True
09:31:50 app.services.agent.memory.enhanced_memory_manager INFO   EnhancedMemoryManager initialized: short=10, medium=100, threshold=0.1, long_term_backup=enabled
09:31:50 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ EnhancedMemoryManager已创建
09:31:50 app.services.agent.memory.unified_coordinator INFO   [UnifiedMemoryCoordinator] 初始化统一记忆协调器
09:31:50 app.services.agent.memory.unified_coordinator INFO   [UnifiedMemoryCoordinator] 全局实例已设置
09:31:50 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ UnifiedMemoryCoordinator已初始化 | checkpointer=AsyncRedisSaver | enhanced_memory=yes | context_manager=yes
09:31:50 app.services.agent.parallel_tool_node INFO   [ParallelToolNode] 初始化完成，最大并发数=5，并行安全工具=4个
09:31:51 app.api.v1.agent INFO   [Global Agent] 创建全局Agent实例，MemorySaver将在请求间共享
09:31:51 app.services.agent.langgraph_agent INFO   [Planning] 使用隔离的thread_id: ad948837-e94e-4d0f-92a4-a75cf1301b07:7b92904b-470e-4c63-9259-d133c4b734a1 (work_id=ad948837-e94e-4d0f-92a4-a75cf1301b07, conversation_id=7b92904b-470e-4c63-9259-d133c4b734a1)
09:31:51 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: 分析前面五章内容，来写第六章...
09:31:51 app.core.cache INFO   ⚠️ 缓存未命中: prompt:get_planning_static_prompt:fca6eb91156619d0
09:31:51 app.core.cache INFO   💾 缓存已保存: prompt:get_planning_static_prompt:fca6eb91156619d0 (expire=3600s)
09:31:51 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
09:31:51 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
09:31:51 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=600, temp=0.3, task_type=TaskType.SIMPLE_QA
09:31:53 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
09:32:01 app.services.ai.http_ai_service INFO   API 响应完成，共接收 9 个数据块，总长度: 1415
09:32:01 app.services.ai.http_ai_service INFO   流式响应Token统计: 3067 (prompt=2496, completion=571)
09:32:01 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
09:32:01 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=3067, cost=$0.008830, time=10638ms
09:32:01 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=3067
09:32:01 app.services.agent.langgraph_agent INFO   [JSON解析] 方法2成功: 从```json块提取
09:32:01 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共7个任务，耗时: 10.73s
09:32:01 app.api.v1.agent INFO   [Stream] 规划生成: 7 个任务
09:32:01 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
09:32:01 app.services.agent.parameter_resolver INFO   [ParameterResolver] 初始化完成, 严格模式: False
09:32:01 app.services.agent.langgraph_agent INFO   [ParameterResolver] 参数解析器已启用
09:32:01 app.services.agent.langgraph_agent INFO   [ParallelExecution] 任务分组: 并行=5, 串行=2
09:32:01 app.services.agent.langgraph_agent INFO   [ParallelExecution] 开始并行执行5个任务
09:32:01 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务1开始: 获取第一章内容
09:32:01 app.api.v1.agent INFO   [Stream] 任务开始: 获取第一章内容
09:32:01 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务2开始: 获取第二章内容
09:32:01 app.api.v1.agent INFO   [Stream] 任务开始: 获取第二章内容
09:32:01 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务3开始: 获取第三章内容
09:32:01 app.api.v1.agent INFO   [Stream] 任务开始: 获取第三章内容
09:32:01 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务4开始: 获取第四章内容
09:32:01 app.api.v1.agent INFO   [Stream] 任务开始: 获取第四章内容
09:32:01 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务5开始: 获取第五章内容
09:32:01 app.api.v1.agent INFO   [Stream] 任务开始: 获取第五章内容
09:32:01 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第2章: 归巢与低语
09:32:01 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第3章: 遗落的星图
09:32:01 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第4章: 天眼与土獾
09:32:01 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第5章: 红雾下的星图
09:32:01 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 钢铁坟场
09:32:01 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务2完成
09:32:01 app.api.v1.agent INFO   [Stream] 任务完成: 获取第二章内容 (0.1s)
09:32:01 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务3完成
09:32:01 app.api.v1.agent INFO   [Stream] 任务完成: 获取第三章内容 (0.1s)
09:32:01 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务4完成
09:32:01 app.api.v1.agent INFO   [Stream] 任务完成: 获取第四章内容 (0.1s)
09:32:01 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务5完成
09:32:01 app.api.v1.agent INFO   [Stream] 任务完成: 获取第五章内容 (0.1s)
09:32:01 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务1完成
09:32:01 app.api.v1.agent INFO   [Stream] 任务完成: 获取第一章内容 (0.1s)
09:32:01 app.services.agent.langgraph_agent INFO   [ParallelExecution] 开始串行执行2个任务
09:32:01 app.services.agent.langgraph_agent INFO   [ParallelExecution] 串行任务6开始: 分析前五章内容
09:32:01 app.api.v1.agent INFO   [Stream] 任务开始: 分析前五章内容
09:32:01 app.prompts.constraint_manager INFO   ✅ 已加载模板: analyze_text (v3.0.0)
09:32:01 app.prompts.constraint_manager INFO   ✅ 已加载模板: creative_writing (v1.0.0)
09:32:01 app.prompts.constraint_manager INFO   ✅ 已加载模板: intent_classifier (v2.0.0)
09:32:01 app.prompts.constraint_manager INFO   ✅ 已加载模板: planning_agent (v2.0.0)
09:32:01 app.prompts.constraint_manager INFO   ✅ 已加载模板: query_agent (v2.0.0)
09:32:01 app.prompts.constraint_manager INFO   ✅ 已加载模板: system_agent (v2.0.0)
09:32:01 app.prompts.constraint_manager INFO   ✅ 已加载模板: tool_agent (v2.0.0)
09:32:01 app.prompts.constraint_manager INFO   ✅ 已加载模板: writing_agent (v2.0.0)
09:32:01 app.prompts.constraint_manager INFO   ✅ 约束提示词管理器已初始化: 加载8个模板, 注册0个验证器
09:32:01 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
09:32:01 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
09:32:01 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
09:32:03 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
09:32:31 app.services.ai.http_ai_service INFO   API 响应完成，共接收 89 个数据块，总长度: 6330
09:32:31 app.services.ai.http_ai_service INFO   流式响应Token统计: 15296 (prompt=10936, completion=4360)
09:32:31 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
09:32:31 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=15296, cost=$0.057270, time=29961ms
09:32:31 app.services.agent.langgraph_agent INFO   ✅ [Agent分析] 分析完成，结果长度: 6330
09:32:31 app.services.agent.langgraph_agent INFO   [ParallelExecution] 串行任务6完成
09:32:31 app.api.v1.agent INFO   [Stream] 任务完成: 分析前五章内容 (30.1s)
09:32:31 app.services.agent.langgraph_agent INFO   [ParallelExecution] 串行任务7开始: 根据分析结果续写第六章
09:32:31 app.api.v1.agent INFO   [Stream] 任务开始: 根据分析结果续写第六章
09:32:31 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: complex
09:32:31 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=content_creation, 模型=gemini-2.5-pro, 原因=任务复杂度为 complex; 任务类型: content_creation; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
09:32:31 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.8, task_type=TaskType.CONTENT_CREATION
09:32:34 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
09:33:09 app.services.ai.http_ai_service INFO   API 响应完成，共接收 62 个数据块，总长度: 2032
09:33:09 app.services.ai.http_ai_service INFO   流式响应Token统计: 12166 (prompt=10651, completion=1515)
09:33:09 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
09:33:09 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=12166, cost=$0.028464, time=37135ms
09:33:09 app.services.agent.langgraph_agent INFO   [ParallelExecution] 串行任务7完成
09:33:09 app.api.v1.agent INFO   [Stream] 任务完成: 根据分析结果续写第六章 (37.2s)
09:33:09 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共7个任务，耗时: 67.36s
09:33:09 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
09:33:09 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=0, 输出型=2, 展示型=5
09:33:09 app.services.agent.langgraph_agent INFO   [Response] 2个输出任务，简单拼接
09:33:09 app.api.v1.agent INFO   [Stream] 跳过最终响应（内容已流式发送）
09:33:09 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed
09:34:22 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
09:34:22 app.services.ai.http_ai_service INFO   ModelSelector 已启用
09:34:22 app.services.ai.http_ai_service INFO   AILogService 已启用 (用于成本追踪)
09:34:23 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
09:34:23 app.api.v1.agent INFO   [Chat Stream] Mode: planning
09:34:23 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:58981 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
09:34:23 app.api.v1.agent INFO   [Session] 创建新会话归属: 1d9db3f7-f5f0-4fe3-8fec-adfc8246cc5f -> 602f5147-846a-4cde-95d3-405fa75f133f
09:34:23 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: planning, Message: 你知道刚才你干了什么吗？...
09:34:23 app.services.agent.langgraph_agent INFO   [Planning] 使用隔离的thread_id: ad948837-e94e-4d0f-92a4-a75cf1301b07:1d9db3f7-f5f0-4fe3-8fec-adfc8246cc5f (work_id=ad948837-e94e-4d0f-92a4-a75cf1301b07, conversation_id=1d9db3f7-f5f0-4fe3-8fec-adfc8246cc5f)
09:34:23 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: 你知道刚才你干了什么吗？...
09:34:23 app.core.cache INFO   ✅ 缓存命中: prompt:get_planning_static_prompt:fca6eb91156619d0
09:34:23 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
09:34:23 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
09:34:23 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=600, temp=0.3, task_type=TaskType.SIMPLE_QA
09:34:26 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
09:34:30 app.services.ai.http_ai_service INFO   API 响应完成，共接收 2 个数据块，总长度: 198
09:34:30 app.services.ai.http_ai_service INFO   流式响应Token统计: 1920 (prompt=1840, completion=80)
09:34:30 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
09:34:30 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1920, cost=$0.003100, time=6697ms
09:34:30 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=1920
09:34:30 app.services.agent.langgraph_agent INFO   [JSON解析] 方法2成功: 从```json块提取
09:34:30 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共1个任务，耗时: 6.79s
09:34:30 app.api.v1.agent INFO   [Stream] 规划生成: 1 个任务
09:34:30 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
09:34:30 app.services.agent.parameter_resolver INFO   [ParameterResolver] 初始化完成, 严格模式: False
09:34:30 app.services.agent.langgraph_agent INFO   [ParameterResolver] 参数解析器已启用
09:34:30 app.services.agent.langgraph_agent INFO   [ParallelExecution] 任务分组: 并行=1, 串行=0
09:34:30 app.services.agent.langgraph_agent INFO   [ParallelExecution] 开始并行执行1个任务
09:34:30 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务1开始: 获取当前作品和章节上下文，以了解AI之前的状态或操作
09:34:30 app.api.v1.agent INFO   [Stream] 任务开始: 获取当前作品和章节上下文，以了解AI之前的状态或操作
09:34:30 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=ad948837-e94e-4d0f-92a4-a75cf1301b07, chapter_id=ef5eb68c-32b8-4249-83a3-31d57363c0a9
09:34:30 app.services.agent.langgraph_agent INFO   [get_context_tool] 当前章节order=1，将检索前0章
09:34:30 app.services.chapter_vector_service INFO   RAG检索: work_id=ad948837-e94e-4d0f-92a4-a75cf1301b07, current_order=1, query=作品背景、人物关系、情节发展、伏笔线索...
09:34:31 app.services.chapter_vector_service WARNING   ⚠️ 作品 ad948837-e94e-4d0f-92a4-a75cf1301b07 前0章暂无向量数据
09:34:31 app.services.agent.langgraph_agent WARNING   [get_context_tool] RAG检索为空，使用Worldview降级
09:34:31 app.services.agent.langgraph_agent ERROR   [get_context_tool] RAG检索失败: 'Setting' object has no attribute 'name'
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\services\agent\langgraph_agent.py", line 891, in get_context_tool
    "settings": [{"name": s.name, "description": s.description[:200]} for s in (settings[:5] if settings else [])]
                          ^^^^^^
AttributeError: 'Setting' object has no attribute 'name'
09:34:31 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=大寂灭
09:34:31 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务1完成
09:34:31 app.api.v1.agent INFO   [Stream] 任务完成: 获取当前作品和章节上下文，以了解AI之前的状态或操作 (0.4s)
09:34:31 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共1个任务，耗时: 0.40s
09:34:31 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
09:34:31 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=1, 输出型=0, 展示型=0
09:34:31 app.services.agent.langgraph_agent WARNING   [Response] 没有明确输出任务，使用AI整合
09:34:31 app.services.agent.langgraph_agent INFO   [Summarization] 使用AI整合任务结果
09:34:31 app.services.agent.langgraph_agent INFO   [Summarization] 上下文压缩: 原始=1681字符, 压缩后=1712字符, 压缩率=-1%
09:34:31 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
09:34:31 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
09:34:31 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
09:34:33 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
09:34:37 app.services.ai.http_ai_service INFO   API 响应完成，共接收 2 个数据块，总长度: 210
09:34:37 app.services.ai.http_ai_service INFO   流式响应Token统计: 2170 (prompt=2038, completion=132)
09:34:37 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
09:34:37 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2170, cost=$0.003867, time=6747ms
09:34:37 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=2170
09:34:37 app.api.v1.agent INFO   [Stream] 跳过最终响应（内容已流式发送）
09:34:37 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed
