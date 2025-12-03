(venv) PS D:\Java\ai_writer\backend> python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
INFO:     Will watch for changes in these directories: ['D:\\Java\\ai_writer\\backend']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [16496] using WatchFiles
08:28:26 app.api.v1.agent INFO   [Redis] 全局连接池已创建
已注册策略: web_novel_11d - 网文11维度分析
08:28:27 app.utils.file_storage INFO   临时文件存储目录: D:\Temp\novelaide_exports
08:28:27 app.main INFO   [STARTUP] 监控中间件已注册: TraceMiddleware, MonitoringMiddleware
INFO:     Started server process [10220]
INFO:     Waiting for application startup.
08:28:28 app.main INFO   [STARTUP] 应用启动中...
08:28:28 app.core.database INFO   正在初始化数据库... (尝试 1/3)
08:28:28 app.core.database INFO   ✅ 数据库初始化成功
08:28:28 apscheduler.scheduler INFO   Adding job tentatively -- it will be properly scheduled when the scheduler starts
08:28:28 apscheduler.scheduler INFO   Added job "清理过期的去痕迹会话详情" to job store "default"
08:28:28 apscheduler.scheduler INFO   Scheduler started
08:28:28 app.tasks.cleanup_humanize_details INFO   定时任务调度器已启动
08:28:28 app.main INFO   [STARTUP] 开始预初始化同步Redis连接...
08:28:28 app.main INFO   [STARTUP] ✅ 同步Redis连接池预初始化完成
08:28:28 app.main INFO   [STARTUP] 开始初始化AsyncRedisSaver索引...
08:28:28 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ setup_checkpointer Redis连接验证成功
08:28:28 redisvl.index.index INFO   Index already exists, not overwriting.
08:28:28 redisvl.index.index INFO   Index already exists, not overwriting.
08:28:28 redisvl.index.index INFO   Index already exists, not overwriting.
08:28:28 langgraph.checkpoint.redis.aio INFO   Redis client is a standalone client
08:28:28 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ AsyncRedisSaver索引预创建成功
08:28:28 app.main INFO   [STARTUP] AsyncRedisSaver索引初始化完成
08:28:28 app.main INFO   [STARTUP] 开始预加载Embedding模型...
08:28:28 app.services.vector_store_service INFO   🔄 预加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
08:28:36 app.services.vector_store_service INFO   ✅ Embedding模型预加载成功，耗时: 7.96秒
08:28:36 app.main INFO   [STARTUP] Embedding模型预加载完成
08:28:36 app.main INFO   [STARTUP] P0性能优化已暂时禁用（诊断模式）
08:28:36 app.main INFO   [STARTUP] 应用启动完成
INFO:     Application startup complete.
INFO:     127.0.0.1:63042 - "OPTIONS /api/v1/auth/login HTTP/1.1" 200 OK
08:34:29 monitoring INFO   Registered health check: cpu_usage
08:34:29 monitoring INFO   Registered health check: memory_usage
08:34:29 monitoring INFO   Registered health check: disk_usage
08:34:29 monitoring INFO   Registered health check: process_status
08:34:29 monitoring INFO   Added alert rule: high_cpu_usage
08:34:29 monitoring INFO   Added alert rule: high_memory_usage
08:34:29 monitoring INFO   Added alert rule: low_disk_space
08:34:29 app.api.v1.auth INFO   [LOGIN] 尝试登录: 2072855200@qq.com
08:34:30 app.api.v1.auth INFO   [LOGIN] 会话创建成功: 602f5147-846a-4cde-95d3-405fa75f133f (127.0.0.1)
08:34:30 app.api.v1.auth INFO   [LOGIN] 登录成功: testuser_new-1 (602f5147-846a-4cde-95d3-405fa75f133f) from 127.0.0.1
08:34:30 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/auth/login
INFO:     127.0.0.1:63042 - "POST /api/v1/auth/login HTTP/1.1" 200 OK
INFO:     127.0.0.1:63042 - "OPTIONS /api/v1/users/me HTTP/1.1" 200 OK
08:34:30 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/users/me
INFO:     127.0.0.1:63042 - "GET /api/v1/users/me HTTP/1.1" 200 OK
INFO:     127.0.0.1:63042 - "OPTIONS /api/v1/works HTTP/1.1" 200 OK
INFO:     127.0.0.1:54328 - "OPTIONS /api/v1/works HTTP/1.1" 200 OK
08:34:30 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works
INFO:     127.0.0.1:54328 - "GET /api/v1/works HTTP/1.1" 200 OK
08:34:30 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works
INFO:     127.0.0.1:63042 - "GET /api/v1/works HTTP/1.1" 200 OK
INFO:     127.0.0.1:61167 - "OPTIONS /api/v1/works/eb13b431-caef-4ec3-83b2-453951b16a72 HTTP/1.1" 200 OK
INFO:     127.0.0.1:54886 - "OPTIONS /api/v1/chapters/work/eb13b431-caef-4ec3-83b2-453951b16a72 HTTP/1.1" 200 OK
INFO:     127.0.0.1:61745 - "OPTIONS /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/characters HTTP/1.1" 200 OK
INFO:     127.0.0.1:49760 - "OPTIONS /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/settings HTTP/1.1" 200 OK
INFO:     127.0.0.1:56642 - "OPTIONS /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/locations HTTP/1.1" 200 OK
INFO:     127.0.0.1:53446 - "OPTIONS /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:61167 - "OPTIONS /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/ai-guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:49760 - "OPTIONS /api/v1/works/eb13b431-caef-4ec3-83b2-453951b16a72 HTTP/1.1" 200 OK
INFO:     127.0.0.1:56642 - "OPTIONS /api/v1/chapters/work/eb13b431-caef-4ec3-83b2-453951b16a72 HTTP/1.1" 200 OK
INFO:     127.0.0.1:53446 - "OPTIONS /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/characters HTTP/1.1" 200 OK
INFO:     127.0.0.1:61167 - "OPTIONS /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/locations HTTP/1.1" 200 OK
INFO:     127.0.0.1:53446 - "OPTIONS /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/settings HTTP/1.1" 200 OK
INFO:     127.0.0.1:61167 - "OPTIONS /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:53446 - "OPTIONS /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/ai-guidelines HTTP/1.1" 200 OK
08:35:23 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works/eb13b431-caef-4ec3-83b2-453951b16a72
INFO:     127.0.0.1:61167 - "GET /api/v1/works/eb13b431-caef-4ec3-83b2-453951b16a72 HTTP/1.1" 200 OK
08:35:23 app.api.v1.worldview INFO   ⚠️ [Worldview] 缓存未命中: worldview:characters:eb13b431-caef-4ec3-83b2-453951b16a72
08:35:23 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:characters:eb13b431-caef-4ec3-83b2-453951b16a72 (expire=300s)
08:35:23 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/characters
INFO:     127.0.0.1:61167 - "GET /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/characters HTTP/1.1" 200 OK
08:35:23 app.api.v1.worldview INFO   ⚠️ [Worldview] 缓存未命中: worldview:settings:eb13b431-caef-4ec3-83b2-453951b16a72
08:35:23 app.api.v1.chapters INFO   [GET chapters] work_id=eb13b431-caef-4ec3-83b2-453951b16a72, user_id=602f5147-846a-4cde-95d3-405fa75f133f
08:35:23 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:settings:eb13b431-caef-4ec3-83b2-453951b16a72 (expire=300s)
08:35:23 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/settings
INFO:     127.0.0.1:61167 - "GET /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/settings HTTP/1.1" 200 OK
08:35:23 app.api.v1.worldview INFO   ⚠️ [Worldview] 缓存未命中: worldview:locations:eb13b431-caef-4ec3-83b2-453951b16a72
08:35:23 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:locations:eb13b431-caef-4ec3-83b2-453951b16a72 (expire=300s)
08:35:23 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/locations
INFO:     127.0.0.1:61167 - "GET /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/locations HTTP/1.1" 200 OK
08:35:23 app.api.v1.worldview INFO   ⚠️ [Worldview] 缓存未命中: worldview:guidelines:eb13b431-caef-4ec3-83b2-453951b16a72
08:35:23 app.api.v1.chapters INFO   ⚠️ [GET chapters] 缓存未命中: chapters:work:eb13b431-caef-4ec3-83b2-453951b16a72
08:35:23 app.services.chapter_service INFO   [ChapterService] Querying chapters for work_id=eb13b431-caef-4ec3-83b2-453951b16a72, type=<class 'uuid.UUID'>
08:35:23 app.services.chapter_service INFO   [ChapterService] Found 3 chapters
08:35:23 app.services.chapter_service INFO     - Chapter: 琼林夜宴，天子疾, order=1
08:35:23 app.services.chapter_service INFO     - Chapter: 翰林寻秘，怪力乱神, order=2
08:35:23 app.services.chapter_service INFO     - Chapter: 雨夜杀机，墨香阻刃, order=3
08:35:23 app.api.v1.chapters INFO   [GET chapters] Returning 3 chapters
08:35:23 app.api.v1.chapters INFO   💾 [GET chapters] 缓存已保存: chapters:work:eb13b431-caef-4ec3-83b2-453951b16a72 (expire=60s)
08:35:23 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:guidelines:eb13b431-caef-4ec3-83b2-453951b16a72 (expire=300s)
08:35:23 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/chapters/work/eb13b431-caef-4ec3-83b2-453951b16a72
08:35:23 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/guidelines
INFO:     127.0.0.1:53446 - "GET /api/v1/chapters/work/eb13b431-caef-4ec3-83b2-453951b16a72 HTTP/1.1" 200 OK
INFO:     127.0.0.1:61167 - "GET /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/guidelines HTTP/1.1" 200 OK
08:35:23 app.api.v1.worldview INFO   ⚠️ [Worldview] 缓存未命中: worldview:ai-guidelines:eb13b431-caef-4ec3-83b2-453951b16a72
08:35:23 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works/eb13b431-caef-4ec3-83b2-453951b16a72
INFO:     127.0.0.1:61167 - "GET /api/v1/works/eb13b431-caef-4ec3-83b2-453951b16a72 HTTP/1.1" 200 OK
08:35:23 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:ai-guidelines:eb13b431-caef-4ec3-83b2-453951b16a72 (expire=300s)
08:35:23 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/ai-guidelines
INFO:     127.0.0.1:53446 - "GET /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/ai-guidelines HTTP/1.1" 200 OK
08:35:23 app.api.v1.worldview INFO   ⚠️ [Worldview] 缓存未命中: worldview:characters:eb13b431-caef-4ec3-83b2-453951b16a72
08:35:23 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:characters:eb13b431-caef-4ec3-83b2-453951b16a72 (expire=300s)
08:35:23 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/characters
INFO:     127.0.0.1:62303 - "GET /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/characters HTTP/1.1" 200 OK
08:35:23 app.api.v1.worldview INFO   ✅ [Worldview] 缓存命中: worldview:ai-guidelines:eb13b431-caef-4ec3-83b2-453951b16a72
INFO:     127.0.0.1:62303 - "OPTIONS /api/v1/analysis/works/eb13b431-caef-4ec3-83b2-453951b16a72/status HTTP/1.1" 200 OK
08:35:23 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/ai-guidelines
INFO:     127.0.0.1:53446 - "GET /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/ai-guidelines HTTP/1.1" 200 OK
08:35:23 app.api.v1.chapters INFO   [GET chapters] work_id=eb13b431-caef-4ec3-83b2-453951b16a72, user_id=602f5147-846a-4cde-95d3-405fa75f133f
08:35:23 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/analysis/works/eb13b431-caef-4ec3-83b2-453951b16a72/status
INFO:     127.0.0.1:62303 - "GET /api/v1/analysis/works/eb13b431-caef-4ec3-83b2-453951b16a72/status HTTP/1.1" 200 OK
08:35:23 app.api.v1.worldview INFO   ⚠️ [Worldview] 缓存未命中: worldview:locations:eb13b431-caef-4ec3-83b2-453951b16a72
08:35:23 app.api.v1.chapters INFO   ✅ [GET chapters] 缓存命中: chapters:work:eb13b431-caef-4ec3-83b2-453951b16a72
08:35:23 app.api.v1.worldview INFO   ✅ [Worldview] 缓存命中: worldview:settings:eb13b431-caef-4ec3-83b2-453951b16a72
08:35:23 app.api.v1.worldview INFO   ✅ [Worldview] 缓存命中: worldview:guidelines:eb13b431-caef-4ec3-83b2-453951b16a72
08:35:23 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/chapters/work/eb13b431-caef-4ec3-83b2-453951b16a72
08:35:23 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/settings
08:35:23 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/guidelines
08:35:23 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:locations:eb13b431-caef-4ec3-83b2-453951b16a72 (expire=300s)
INFO:     127.0.0.1:55192 - "GET /api/v1/chapters/work/eb13b431-caef-4ec3-83b2-453951b16a72 HTTP/1.1" 200 OK
INFO:     127.0.0.1:65509 - "GET /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/settings HTTP/1.1" 200 OK
INFO:     127.0.0.1:50398 - "GET /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/guidelines HTTP/1.1" 200 OK
08:35:23 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/locations
INFO:     127.0.0.1:61167 - "GET /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/locations HTTP/1.1" 200 OK
INFO:     127.0.0.1:61167 - "OPTIONS /api/v1/chapters/6c46612a-5d6f-4ad2-9310-7d8aac83e881 HTTP/1.1" 200 OK
08:35:24 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/analysis/works/eb13b431-caef-4ec3-83b2-453951b16a72/status
INFO:     127.0.0.1:50398 - "GET /api/v1/analysis/works/eb13b431-caef-4ec3-83b2-453951b16a72/status HTTP/1.1" 200 OK
08:35:24 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:eb13b431-caef-4ec3-83b2-453951b16a72
08:35:24 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/6c46612a-5d6f-4ad2-9310-7d8aac83e881
INFO:     127.0.0.1:61167 - "PUT /api/v1/chapters/6c46612a-5d6f-4ad2-9310-7d8aac83e881 HTTP/1.1" 200 OK
08:35:24 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:eb13b431-caef-4ec3-83b2-453951b16a72
08:35:24 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/6c46612a-5d6f-4ad2-9310-7d8aac83e881
INFO:     127.0.0.1:61167 - "PUT /api/v1/chapters/6c46612a-5d6f-4ad2-9310-7d8aac83e881 HTTP/1.1" 200 OK
INFO:     127.0.0.1:57379 - "OPTIONS /api/v1/chapters/e240ac64-5541-4987-8adf-ddf6dd1e4105 HTTP/1.1" 200 OK
08:35:33 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:eb13b431-caef-4ec3-83b2-453951b16a72
08:35:33 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/e240ac64-5541-4987-8adf-ddf6dd1e4105
INFO:     127.0.0.1:57379 - "PUT /api/v1/chapters/e240ac64-5541-4987-8adf-ddf6dd1e4105 HTTP/1.1" 200 OK
08:35:33 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:eb13b431-caef-4ec3-83b2-453951b16a72
08:35:33 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/e240ac64-5541-4987-8adf-ddf6dd1e4105
INFO:     127.0.0.1:57379 - "PUT /api/v1/chapters/e240ac64-5541-4987-8adf-ddf6dd1e4105 HTTP/1.1" 200 OK
INFO:     127.0.0.1:62240 - "OPTIONS /api/v1/agent/chat/stream HTTP/1.1" 200 OK
08:36:02 app.services.ai.prompts INFO   Prompts loaded successfully from D:\Java\ai_writer\backend\app\services\ai\prompts\default.json
08:36:02 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
08:36:02 app.services.ai.http_ai_service INFO   ModelSelector 已启用
08:36:02 app.services.ai.http_ai_service INFO   AILogService 已启用 (用于成本追踪)
08:36:04 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
08:36:04 app.api.v1.agent INFO   [Chat Stream] Mode: planning
08:36:04 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:62240 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
08:36:04 app.core.redis INFO   ✅ Redis connected: redis://localhost:6379/0
08:36:04 app.api.v1.agent INFO   [Session] 创建新会话归属: 381deff4-d5e9-4ecb-8a22-be26ef85490f -> 602f5147-846a-4cde-95d3-405fa75f133f
08:36:04 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: planning, Message: 前三章的标题是什么？进行获取...
08:36:04 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
08:36:04 app.services.ai.http_ai_service INFO   ModelSelector 已启用
08:36:04 app.services.ai.http_ai_service WARNING   成本追踪已启用，但未提供db或user_id，成本数据将不会被记录！请检查HTTPAIService初始化参数。
08:36:06 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
08:36:06 app.services.context.adaptive_budget INFO   ✅ 所有预算配置验证通过
08:36:14 app.services.context.vector_memory_store INFO   ✅ VectorMemoryStore初始化成功 | 目录=./data/chroma_db | 模型=paraphrase-multilingual-MiniLM-L12-v2 | 集合=user_memories
08:36:14 app.services.context.manager INFO   ✅ VectorMemoryStore 已初始化
08:36:14 app.services.context.manager INFO   ✅ ContextManager: 长期记忆已启用 (user_id=None)
08:36:14 app.services.context.manager INFO   ✅ ContextManager: 自适应预算已启用
08:36:14 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ ContextManager已初始化（长期记忆已启用，自适应预算已启用，总预算=16000 tokens）
成功加载模板: intent_classifier (版本 2.0.0)
成功加载模板: writing_agent (版本 2.0.0)
成功加载模板: planning_agent (版本 2.0.0)
成功加载模板: tool_agent (版本 2.0.0)
成功加载模板: query_agent (版本 2.0.0)
成功加载模板: system_agent_prompt (版本 2.0.0)
成功加载模板: creative_writing_prompt (版本 1.0.0)
08:36:14 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ PromptManager已初始化
08:36:14 app.services.agent.langgraph_agent INFO   [LangGraph] 使用 HTTPAIService 模式（手动工具调用，绕过 Cloudflare）
08:36:14 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ Redis连接验证成功
08:36:14 app.services.agent.langgraph_agent INFO   [LangGraph] OK 使用 AsyncRedisSaver（redis://localhost:6379/0，TTL=7天）
08:36:14 app.services.agent.memory.metrics INFO   [MemoryMetrics] 监控系统已初始化
08:36:14 app.services.agent.memory.long_term_store INFO   [LongTermStore] Initialized: base_dir=./data/long_term_memory, max_size=50KB, compression=True
08:36:14 app.services.agent.memory.enhanced_memory_manager INFO   EnhancedMemoryManager initialized: short=10, medium=100, threshold=0.1, long_term_backup=enabled
08:36:14 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ EnhancedMemoryManager已创建
08:36:14 app.services.agent.memory.unified_coordinator INFO   [UnifiedMemoryCoordinator] 初始化统一记忆协调器
08:36:14 app.services.agent.memory.unified_coordinator INFO   [UnifiedMemoryCoordinator] 全局实例已设置
08:36:14 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ UnifiedMemoryCoordinator已初始化 | checkpointer=AsyncRedisSaver | enhanced_memory=yes | context_manager=yes
08:36:14 app.services.agent.parallel_tool_node INFO   [ParallelToolNode] 初始化完成，最大并发数=5，并行安全工具=4个
08:36:14 app.api.v1.agent INFO   [Global Agent] 创建全局Agent实例，MemorySaver将在请求间共享
08:36:14 app.services.agent.langgraph_agent INFO   [Planning] 使用隔离的thread_id: eb13b431-caef-4ec3-83b2-453951b16a72:381deff4-d5e9-4ecb-8a22-be26ef85490f (work_id=eb13b431-caef-4ec3-83b2-453951b16a72, conversation_id=381deff4-d5e9-4ecb-8a22-be26ef85490f)
08:36:14 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: 前三章的标题是什么？进行获取...
08:36:14 app.core.cache INFO   ⚠️ 缓存未命中: prompt:get_planning_static_prompt:fca6eb91156619d0
08:36:14 app.core.cache INFO   💾 缓存已保存: prompt:get_planning_static_prompt:fca6eb91156619d0 (expire=3600s)
08:36:14 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
08:36:14 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
08:36:14 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=600, temp=0.3, task_type=TaskType.SIMPLE_QA
08:36:17 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
08:36:18 app.services.ai.http_ai_service INFO   API 响应完成，共接收 4 个数据块，总长度: 543
08:36:18 app.services.ai.http_ai_service INFO   流式响应Token统计: 1049 (prompt=835, completion=214)
08:36:18 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1049, cost=$0.003184, time=3298ms
08:36:18 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=1049
08:36:18 app.services.agent.langgraph_agent INFO   [JSON解析] 方法2成功: 从```json块提取
08:36:18 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共3个任务，耗时: 3.36s
08:36:18 app.api.v1.agent INFO   [Stream] 规划生成: 3 个任务
08:36:18 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
08:36:18 app.services.agent.parameter_resolver INFO   [ParameterResolver] 初始化完成, 严格模式: False
08:36:18 app.services.agent.langgraph_agent INFO   [ParameterResolver] 参数解析器已启用
08:36:18 app.services.agent.langgraph_agent INFO   [ParallelExecution] 任务分组: 并行=3, 串行=0
08:36:18 app.services.agent.langgraph_agent INFO   [ParallelExecution] 开始并行执行3个任务
08:36:18 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务1开始: 获取第一章信息
08:36:18 app.api.v1.agent INFO   [Stream] 任务开始: 获取第一章信息
08:36:18 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务2开始: 获取第二章信息
08:36:18 app.api.v1.agent INFO   [Stream] 任务开始: 获取第二章信息
08:36:18 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务3开始: 获取第三章信息
08:36:18 app.api.v1.agent INFO   [Stream] 任务开始: 获取第三章信息
08:36:18 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 琼林夜宴，天子疾
08:36:18 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第2章: 翰林寻秘，怪力乱神
08:36:18 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第3章: 雨夜杀机，墨香阻刃
08:36:18 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务1完成
08:36:18 app.api.v1.agent INFO   [Stream] 任务完成: 获取第一章信息 (0.0s)
08:36:18 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务2完成
08:36:18 app.api.v1.agent INFO   [Stream] 任务完成: 获取第二章信息 (0.0s)
08:36:18 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务3完成
08:36:18 app.api.v1.agent INFO   [Stream] 任务完成: 获取第三章信息 (0.0s)
08:36:18 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共3个任务，耗时: 0.05s
08:36:18 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
08:36:18 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=0, 输出型=0, 展示型=3
08:36:18 app.services.agent.langgraph_agent INFO   [Response] 纯展示型任务(3个)，直接格式化返回（跳过AI整合，节省成本）
08:36:18 app.api.v1.agent INFO   [Stream] 跳过最终响应（内容已流式发送）
08:36:18 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed
08:37:40 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
08:37:40 app.services.ai.http_ai_service INFO   ModelSelector 已启用
08:37:40 app.services.ai.http_ai_service INFO   AILogService 已启用 (用于成本追踪)
08:37:42 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
08:37:42 app.api.v1.agent INFO   [Chat Stream] Mode: planning
08:37:42 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
08:37:42 app.api.v1.agent INFO   [Session] 创建新会话归属: d525bb7d-e812-4daf-bef9-f195aaea5da2 -> 602f5147-846a-4cde-95d3-405fa75f133f
08:37:42 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: planning, Message: 结合前面三章，把第四章的结构脉络写给我...
INFO:     127.0.0.1:63245 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
08:37:42 app.services.agent.langgraph_agent INFO   [Planning] 使用隔离的thread_id: eb13b431-caef-4ec3-83b2-453951b16a72:d525bb7d-e812-4daf-bef9-f195aaea5da2 (work_id=eb13b431-caef-4ec3-83b2-453951b16a72, conversation_id=d525bb7d-e812-4daf-bef9-f195aaea5da2)
08:37:42 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: 结合前面三章，把第四章的结构脉络写给我...
08:37:42 app.core.cache INFO   ✅ 缓存命中: prompt:get_planning_static_prompt:fca6eb91156619d0
08:37:42 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
08:37:42 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
08:37:42 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=600, temp=0.3, task_type=TaskType.SIMPLE_QA
08:37:44 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
08:37:48 app.services.ai.http_ai_service INFO   API 响应完成，共接收 8 个数据块，总长度: 892
08:37:48 app.services.ai.http_ai_service INFO   流式响应Token统计: 2220 (prompt=1849, completion=371)
08:37:48 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2220, cost=$0.006021, time=6765ms
08:37:48 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=2220
08:37:48 app.services.agent.langgraph_agent INFO   [JSON解析] 方法2成功: 从```json块提取
08:37:48 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共4个任务，耗时: 6.82s
08:37:48 app.api.v1.agent INFO   [Stream] 规划生成: 4 个任务
08:37:48 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
08:37:48 app.services.agent.parameter_resolver INFO   [ParameterResolver] 初始化完成, 严格模式: False
08:37:48 app.services.agent.langgraph_agent INFO   [ParameterResolver] 参数解析器已启用
08:37:48 app.services.agent.langgraph_agent INFO   [ParallelExecution] 任务分组: 并行=3, 串行=1
08:37:48 app.services.agent.langgraph_agent INFO   [ParallelExecution] 开始并行执行3个任务
08:37:48 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务1开始: 获取第一章内容
08:37:48 app.api.v1.agent INFO   [Stream] 任务开始: 获取第一章内容
08:37:48 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务2开始: 获取第二章内容
08:37:48 app.api.v1.agent INFO   [Stream] 任务开始: 获取第二章内容
08:37:48 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务3开始: 获取第三章内容
08:37:48 app.api.v1.agent INFO   [Stream] 任务开始: 获取第三章内容
08:37:49 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第3章: 雨夜杀机，墨香阻刃
08:37:49 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 琼林夜宴，天子疾
08:37:49 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第2章: 翰林寻秘，怪力乱神
08:37:49 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务3完成
08:37:49 app.api.v1.agent INFO   [Stream] 任务完成: 获取第三章内容 (0.1s)
08:37:49 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务1完成
08:37:49 app.api.v1.agent INFO   [Stream] 任务完成: 获取第一章内容 (0.1s)
08:37:49 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务2完成
08:37:49 app.api.v1.agent INFO   [Stream] 任务完成: 获取第二章内容 (0.1s)
08:37:49 app.services.agent.langgraph_agent INFO   [ParallelExecution] 开始串行执行1个任务
08:37:49 app.services.agent.langgraph_agent INFO   [ParallelExecution] 串行任务4开始: 结合前三章内容，生成第四章结构脉络
08:37:49 app.api.v1.agent INFO   [Stream] 任务开始: 结合前三章内容，生成第四章结构脉络
08:37:49 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: complex
08:37:49 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=content_creation, 模型=gemini-2.5-pro, 原因=任务复杂度为 complex; 任务类型: content_creation; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
08:37:49 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.8, task_type=TaskType.CONTENT_CREATION
08:37:52 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
08:38:30 app.services.ai.http_ai_service INFO   API 响应完成，共接收 24 个数据块，总长度: 1903
08:38:30 app.services.ai.http_ai_service INFO   流式响应Token统计: 9702 (prompt=8222, completion=1480)
08:38:30 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=9702, cost=$0.025078, time=41736ms
08:38:30 app.services.agent.langgraph_agent INFO   [ParallelExecution] 串行任务4完成
08:38:30 app.api.v1.agent INFO   [Stream] 任务完成: 结合前三章内容，生成第四章结构脉络 (41.8s)
08:38:30 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共4个任务，耗时: 41.84s
08:38:30 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
08:38:30 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=0, 输出型=1, 展示型=3
08:38:30 app.services.agent.langgraph_agent INFO   [Response] 单个创作任务(continue_writing_tool)，输出1903字符，直接返回（跳过AI调用）
08:38:30 app.api.v1.agent INFO   [Stream] 跳过最终响应（内容已流式发送）
08:38:30 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed