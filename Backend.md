15:27:09 app.tasks.cleanup_humanize_details INFO   定时任务调度器已启动
15:27:09 app.main INFO   [STARTUP] 开始预初始化同步Redis连接...
15:27:09 app.main INFO   [STARTUP] ✅ 同步Redis连接池预初始化完成
15:27:09 app.main INFO   [STARTUP] 开始初始化AsyncRedisSaver索引...
15:27:09 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ setup_checkpointer Redis连接验证成功
15:27:09 redisvl.index.index INFO   Index already exists, not overwriting.
15:27:09 redisvl.index.index INFO   Index already exists, not overwriting.
15:27:09 redisvl.index.index INFO   Index already exists, not overwriting.
15:27:09 langgraph.checkpoint.redis.aio INFO   Redis client is a standalone client
15:27:09 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ AsyncRedisSaver索引预创建成功
15:27:09 app.main INFO   [STARTUP] AsyncRedisSaver索引初始化完成
15:27:09 app.main INFO   [STARTUP] 开始预加载Embedding模型...
15:27:09 app.services.vector_store_service INFO   🔄 预加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
15:27:15 app.services.vector_store_service INFO   ✅ Embedding模型预加载成功，耗时: 6.17秒
15:27:15 app.main INFO   [STARTUP] Embedding模型预加载完成
15:27:15 app.main INFO   [STARTUP] P0性能优化已暂时禁用（诊断模式）
15:27:15 app.main INFO   [STARTUP] 应用启动完成
INFO:     Application startup complete.
15:27:50 monitoring INFO   Registered health check: cpu_usage
15:27:50 monitoring INFO   Registered health check: memory_usage
15:27:50 monitoring INFO   Registered health check: disk_usage
15:27:50 monitoring INFO   Registered health check: process_status
15:27:50 monitoring INFO   Added alert rule: high_cpu_usage
15:27:50 monitoring INFO   Added alert rule: high_memory_usage
15:27:50 monitoring INFO   Added alert rule: low_disk_space
15:27:50 app.api.v1.auth INFO   [LOGIN] 尝试登录: 2072855200@qq.com
15:27:51 app.api.v1.auth INFO   [LOGIN] 会话创建成功: 602f5147-846a-4cde-95d3-405fa75f133f (127.0.0.1)
15:27:51 app.api.v1.auth INFO   [LOGIN] 登录成功: testuser_new-1 (602f5147-846a-4cde-95d3-405fa75f133f) from 127.0.0.1
15:27:51 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/auth/login
INFO:     127.0.0.1:62711 - "POST /api/v1/auth/login HTTP/1.1" 200 OK
15:27:51 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/users/me
INFO:     127.0.0.1:51833 - "GET /api/v1/users/me HTTP/1.1" 200 OK
15:27:52 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works
INFO:     127.0.0.1:51180 - "GET /api/v1/works HTTP/1.1" 200 OK
15:27:52 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works
INFO:     127.0.0.1:51182 - "GET /api/v1/works HTTP/1.1" 200 OK
15:27:55 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works/c9dd9cbf-fa57-447e-9605-3020bbde5350
INFO:     127.0.0.1:49432 - "GET /api/v1/works/c9dd9cbf-fa57-447e-9605-3020bbde5350 HTTP/1.1" 200 OK
15:27:56 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:ai-guidelines:c9dd9cbf-fa57-447e-9605-3020bbde5350 (expire=300s)
15:27:56 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/ai-guidelines
INFO:     127.0.0.1:60621 - "GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/ai-guidelines HTTP/1.1" 200 OK
15:27:56 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works/c9dd9cbf-fa57-447e-9605-3020bbde5350
INFO:     127.0.0.1:61143 - "GET /api/v1/works/c9dd9cbf-fa57-447e-9605-3020bbde5350 HTTP/1.1" 200 OK
15:27:56 app.api.v1.chapters INFO   [GET chapters] work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, user_id=602f5147-846a-4cde-95d3-405fa75f133f
15:27:56 app.api.v1.worldview INFO   ✅ [Worldview] 缓存命中: worldview:ai-guidelines:c9dd9cbf-fa57-447e-9605-3020bbde5350
15:27:56 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/ai-guidelines
INFO:     127.0.0.1:59374 - "GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/ai-guidelines HTTP/1.1" 200 OK
15:27:56 app.api.v1.chapters INFO   ⚠️ [GET chapters] 缓存未命中: chapters:work:c9dd9cbf-fa57-447e-9605-3020bbde5350
15:27:56 app.services.chapter_service INFO   [ChapterService] Querying chapters for work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, type=<class 'uuid.UUID'>
15:27:56 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:characters:c9dd9cbf-fa57-447e-9605-3020bbde5350 (expire=300s)
15:27:56 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:settings:c9dd9cbf-fa57-447e-9605-3020bbde5350 (expire=300s)
15:27:56 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:locations:c9dd9cbf-fa57-447e-9605-3020bbde5350 (expire=300s)
15:27:56 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:guidelines:c9dd9cbf-fa57-447e-9605-3020bbde5350 (expire=300s)
15:27:56 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/characters
15:27:56 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/settings
15:27:56 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/locations
INFO:     127.0.0.1:49434 - "GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/characters HTTP/1.1" 200 OK
15:27:56 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/guidelines
INFO:     127.0.0.1:49436 - "GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/settings HTTP/1.1" 200 OK
15:27:56 app.services.chapter_service INFO   [ChapterService] Found 39 chapters
15:27:56 app.services.chapter_service INFO     - Chapter: 第1章 吞噬, order=1
15:27:56 app.services.chapter_service INFO     - Chapter: 第2章 浑圆桩, order=2
15:27:56 app.services.chapter_service INFO     - Chapter: 第3章 一夕千悟, order=3
15:27:56 app.services.chapter_service INFO     - Chapter: 第4章 家底, order=4
15:27:56 app.services.chapter_service INFO     - Chapter: 第5章 太一门, order=5
15:27:56 app.services.chapter_service INFO     - Chapter: 第6章 行住坐卧都是修行, order=6
15:27:56 app.services.chapter_service INFO     - Chapter: 第7章 立竿见影, order=7
15:27:56 app.services.chapter_service INFO     - Chapter: 第8章 豹子钻林, order=8
15:27:56 app.services.chapter_service INFO     - Chapter: 第9章 残酷的现实, order=9
15:27:56 app.services.chapter_service INFO     - Chapter: 第10章 呼吸感, order=10
15:27:56 app.services.chapter_service INFO     - Chapter: 第11章 以巧破力, order=11
15:27:56 app.services.chapter_service INFO     - Chapter: 第12章 白吃, order=12
15:27:56 app.services.chapter_service INFO     - Chapter: 第13章 牵牛子, order=13
15:27:56 app.services.chapter_service INFO     - Chapter: 第14章 考核（一）, order=14
15:27:56 app.services.chapter_service INFO     - Chapter: 第15章 考核（二）, order=15
15:27:56 app.services.chapter_service INFO     - Chapter: 第16章 萧白鲛, order=16
15:27:56 app.services.chapter_service INFO     - Chapter: 第17章 内功心法, order=17
15:27:56 app.services.chapter_service INFO     - Chapter: 第18章 所谓武功, order=18
15:27:56 app.services.chapter_service INFO     - Chapter: 第19章 吞噬之法, order=19
15:27:56 app.services.chapter_service INFO     - Chapter: 第20章 万物有灵, order=20
15:27:56 app.services.chapter_service INFO     - Chapter: 第21章 壮大内息, order=21
15:27:56 app.services.chapter_service INFO     - Chapter: 第22章 内息发力, order=22
15:27:56 app.services.chapter_service INFO     - Chapter: 第23章 古月斋, order=23
15:27:56 app.services.chapter_service INFO     - Chapter: 第24章 汤万红, order=24
15:27:56 app.services.chapter_service INFO     - Chapter: 第25章 香炉, order=25
15:27:56 app.services.chapter_service INFO     - Chapter: 第26章 狭巷, order=26
15:27:56 app.services.chapter_service INFO     - Chapter: 第27章 杀人如草不闻声, order=27
15:27:56 app.services.chapter_service INFO     - Chapter: 第28章 九州八宗, order=28
15:27:56 app.services.chapter_service INFO     - Chapter: 第29章 抽了, order=29
15:27:56 app.services.chapter_service INFO     - Chapter: 第30章 梅花刺针, order=30
15:27:56 app.services.chapter_service INFO     - Chapter: 第31章 化外为内, order=31
15:27:56 app.services.chapter_service INFO     - Chapter: 第32章 摸一下, order=32
15:27:56 app.services.chapter_service INFO     - Chapter: 第33章 苦心孤诣, order=33
15:27:56 app.services.chapter_service INFO     - Chapter: 第34章 书生的疑惑, order=34
15:27:56 app.services.chapter_service INFO     - Chapter: 第1章 吞噬, order=35
15:27:56 app.services.chapter_service INFO     - Chapter: 第2章 浑圆桩, order=36
15:27:56 app.services.chapter_service INFO     - Chapter: 第3章 一夕千悟, order=37
15:27:56 app.services.chapter_service INFO     - Chapter: 第4章 家底, order=38
15:27:56 app.services.chapter_service INFO     - Chapter: 第5章 太一门, order=39
15:27:56 app.api.v1.chapters INFO   [GET chapters] Returning 39 chapters
15:27:56 app.api.v1.chapters INFO   💾 [GET chapters] 缓存已保存: chapters:work:c9dd9cbf-fa57-447e-9605-3020bbde5350 (expire=60s)
INFO:     127.0.0.1:49435 - "GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/locations HTTP/1.1" 200 OK
INFO:     127.0.0.1:49437 - "GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/guidelines HTTP/1.1" 200 OK
15:27:56 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/chapters/work/c9dd9cbf-fa57-447e-9605-3020bbde5350
INFO:     127.0.0.1:49433 - "GET /api/v1/chapters/work/c9dd9cbf-fa57-447e-9605-3020bbde5350 HTTP/1.1" 200 OK
15:27:57 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:characters:c9dd9cbf-fa57-447e-9605-3020bbde5350 (expire=300s)
15:27:57 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:settings:c9dd9cbf-fa57-447e-9605-3020bbde5350 (expire=300s)
15:27:57 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/characters
15:27:57 app.api.v1.worldview INFO   ✅ [Worldview] 缓存命中: worldview:guidelines:c9dd9cbf-fa57-447e-9605-3020bbde5350
15:27:57 app.api.v1.chapters INFO   [GET chapters] work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, user_id=602f5147-846a-4cde-95d3-405fa75f133f
INFO:     127.0.0.1:64451 - "GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/characters HTTP/1.1" 200 OK
15:27:57 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/settings
15:27:57 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:locations:c9dd9cbf-fa57-447e-9605-3020bbde5350 (expire=300s)
15:27:57 app.api.v1.chapters INFO   ✅ [GET chapters] 缓存命中: chapters:work:c9dd9cbf-fa57-447e-9605-3020bbde5350
15:27:57 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/guidelines
INFO:     127.0.0.1:64452 - "GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/settings HTTP/1.1" 200 OK
INFO:     127.0.0.1:65254 - "GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/guidelines HTTP/1.1" 200 OK
15:27:57 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/locations
15:27:57 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/chapters/work/c9dd9cbf-fa57-447e-9605-3020bbde5350
INFO:     127.0.0.1:65252 - "GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/locations HTTP/1.1" 200 OK
INFO:     127.0.0.1:57886 - "GET /api/v1/chapters/work/c9dd9cbf-fa57-447e-9605-3020bbde5350 HTTP/1.1" 200 OK
15:27:57 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/analysis/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/status
INFO:     127.0.0.1:53640 - "GET /api/v1/analysis/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/status HTTP/1.1" 200 OK
15:27:57 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/analysis/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/status
INFO:     127.0.0.1:53370 - "GET /api/v1/analysis/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/status HTTP/1.1" 200 OK
15:27:57 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id: 627feba4-2097-4f28-a3f3-7641d10f7f40
15:27:57 app.core.redis INFO   ✅ Redis connected: redis://localhost:6379/0
15:27:57 app.api.v1.ai INFO   [预加载] 当前章节已加载: 627feba4-2097-4f28-a3f3-7641d10f7f40
15:27:57 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
15:27:57 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:61764 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
15:27:57 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id: 627feba4-2097-4f28-a3f3-7641d10f7f40
15:27:57 app.api.v1.ai INFO   [预加载] 当前章节已加载: 627feba4-2097-4f28-a3f3-7641d10f7f40
15:27:57 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
15:27:57 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:57014 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
15:27:58 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:c9dd9cbf-fa57-447e-9605-3020bbde5350
15:27:58 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/627feba4-2097-4f28-a3f3-7641d10f7f40
INFO:     127.0.0.1:57609 - "PUT /api/v1/chapters/627feba4-2097-4f28-a3f3-7641d10f7f40 HTTP/1.1" 200 OK
15:27:58 app.services.chapter_vector_service INFO   开始向量化章节: 第1章 吞噬 (order=1)
15:28:01 app.services.chapter_vector_service INFO   ✅ 章节向量存储完成: 第1章 吞噬 (7段)
15:28:01 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:c9dd9cbf-fa57-447e-9605-3020bbde5350
15:28:01 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:56913 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
15:28:01 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/627feba4-2097-4f28-a3f3-7641d10f7f40
INFO:     127.0.0.1:54407 - "PUT /api/v1/chapters/627feba4-2097-4f28-a3f3-7641d10f7f40 HTTP/1.1" 200 OK
15:28:01 app.services.chapter_vector_service INFO   开始向量化章节: 第1章 吞噬 (order=1)
15:28:03 app.services.chapter_vector_service INFO   ✅ 章节向量存储完成: 第1章 吞噬 (7段)
15:28:37 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:58561 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
15:28:37 app.services.ai.prompts INFO   Prompts loaded successfully from D:\Java\ai_writer\backend\app\services\ai\prompts\default.json
15:28:37 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
15:28:37 app.services.ai.http_ai_service INFO   ModelSelector 已启用
15:28:37 app.services.ai.http_ai_service INFO   AILogService 已启用 (用于成本追踪)
15:28:40 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
15:28:40 app.api.v1.agent INFO   [Chat Stream] Mode: planning
15:28:40 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:62326 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
15:28:40 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: planning, Message: 请先深度分析《一夕千悟，从杂役弟子开始》前5章的：
  1. 人物关系图谱（段融、杨震、孔斌三人组、...
15:28:40 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
15:28:40 app.services.ai.http_ai_service INFO   ModelSelector 已启用
15:28:40 app.services.ai.http_ai_service INFO   [成本追踪] 初始化未传db/user_id，将使用请求上下文按需记录成本
15:28:41 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
15:28:41 app.services.context.adaptive_budget INFO   ✅ 所有预算配置验证通过
15:28:47 app.services.context.vector_memory_store INFO   ✅ VectorMemoryStore初始化成功 | 目录=./data/chroma_db | 模型=paraphrase-multilingual-MiniLM-L12-v2 | 集合=user_memories
15:28:47 app.services.context.manager INFO   ✅ VectorMemoryStore 已初始化
15:28:47 app.services.context.manager INFO   ✅ ContextManager: 长期记忆已启用 (user_id=None)
15:28:47 app.services.context.manager INFO   ✅ ContextManager: 自适应预算已启用
15:28:47 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ ContextManager已初始化（长期记忆已启用，自适应预算已启用，总预算=16000 tokens）
成功加载模板: intent_classifier (版本 2.0.0)
成功加载模板: writing_agent (版本 2.0.0)
成功加载模板: planning_agent (版本 2.0.0)
成功加载模板: tool_agent (版本 2.0.0)
成功加载模板: query_agent (版本 2.0.0)
成功加载模板: system_agent_prompt (版本 2.0.0)
成功加载模板: creative_writing_prompt (版本 1.0.0)
15:28:47 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ PromptManager已初始化
15:28:47 app.services.agent.langgraph_agent INFO   [LangGraph] 使用 HTTPAIService 模式（手动工具调用，绕过 Cloudflare）
15:28:47 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ Redis连接验证成功
15:28:47 app.services.agent.langgraph_agent INFO   [LangGraph] OK 使用 AsyncRedisSaver（redis://localhost:6379/0，TTL=7天）
15:28:47 app.services.agent.memory.metrics INFO   [MemoryMetrics] 监控系统已初始化
15:28:47 app.services.agent.memory.long_term_store INFO   [LongTermStore] Initialized: base_dir=./data/long_term_memory, max_size=50KB, compression=True
15:28:47 app.services.agent.memory.enhanced_memory_manager INFO   EnhancedMemoryManager initialized: short=10, medium=100, threshold=0.1, long_term_backup=enabled
15:28:47 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ EnhancedMemoryManager已创建
15:28:47 app.services.agent.memory.unified_coordinator INFO   [UnifiedMemoryCoordinator] 初始化统一记忆协调器
15:28:47 app.services.agent.memory.unified_coordinator INFO   [UnifiedMemoryCoordinator] 全局实例已设置
15:28:47 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ UnifiedMemoryCoordinator已初始化 | checkpointer=AsyncRedisSaver | enhanced_memory=yes | context_manager=yes
15:28:47 app.services.agent.parallel_tool_node INFO   [ParallelToolNode] 初始化完成，最大并发数=5，并行安全工具=4个
15:28:47 app.api.v1.agent INFO   [Global Agent] created global agent instance; MemorySaver shared across requests
15:28:47 app.services.agent.langgraph_agent INFO   [Planning] 使用隔离的thread_id: c9dd9cbf-fa57-447e-9605-3020bbde5350:0702afa8-4fb8-4ac8-8321-166bc44beafe (work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, conversation_id=0702afa8-4fb8-4ac8-8321-166bc44beafe)
15:28:47 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: 请先深度分析《一夕千悟，从杂役弟子开始》前5章的：
  1. 人物关系图谱（段融、杨震、孔斌三人组、...
15:28:47 app.core.cache INFO   ⚠️ 缓存未命中: prompt:get_planning_agent_mode_prompt:fca6eb91156619d0
15:28:47 app.core.cache INFO   ⚠️ 缓存未命中: prompt:get_planning_static_prompt:fca6eb91156619d0
15:28:47 app.core.cache INFO   💾 缓存已保存: prompt:get_planning_static_prompt:fca6eb91156619d0 (expire=3600s)
15:28:47 app.core.cache INFO   💾 缓存已保存: prompt:get_planning_agent_mode_prompt:fca6eb91156619d0 (expire=3600s)
15:28:47 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
15:28:47 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
15:28:47 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=1200, temp=0.3, task_type=TaskType.SIMPLE_QA
15:28:50 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
15:29:08 app.services.ai.http_ai_service INFO   API 响应完成，共接收 34 个数据块，总长度: 3739
15:29:08 app.services.ai.http_ai_service INFO   流式响应Token统计: 10144 (prompt=7945, completion=2199)
15:29:08 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
15:29:08 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=10144, cost=$0.031921, time=21067ms
15:29:08 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=10144
15:29:08 app.services.agent.langgraph_agent INFO   [JSON解析] 方法2成功: 从```json块提取
15:29:08 app.services.agent.langgraph_agent INFO   [Planning] 思维链: 输出=用户期望得到两部分内容：首先是对《一夕千悟，从杂役弟子开始》, 原料=需要《一夕千悟，从杂役弟子开始》第1章至, 处理=1. 使用`get_chapter_by
15:29:08 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共7个任务，耗时: 21.13s
15:29:08 app.api.v1.agent INFO   [Stream] Plan tasks: 7 items
15:29:08 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
15:29:08 app.services.agent.langgraph_agent INFO   [DeepAgent] 启用反思模式
15:29:08 app.services.agent.parameter_resolver INFO   [ParameterResolver] 初始化完成, 严格模式: False
15:29:08 app.services.agent.langgraph_agent INFO   [DeepAgent] ParameterResolver 已启用
15:29:08 app.services.agent.deep_agent.executor INFO   DeepAgent 开始执行，共 7 个任务，反思功能已启用
15:29:08 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] AI 推断功能已启用
15:29:08 app.api.v1.agent INFO   [Stream] Task started: 获取《一夕千悟，从杂役弟子开始》第一章内容
15:29:08 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
15:29:08 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
15:29:08 app.api.v1.agent INFO   [Stream] 任务完成: 获取《一夕千悟，从杂役弟子开始》第一章内容 (0.0s)
15:29:08 app.api.v1.agent INFO   [Stream] Task started: 获取《一夕千悟，从杂役弟子开始》第二章内容
15:29:08 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
15:29:08 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第2章: 第2章 浑圆桩
15:29:08 app.api.v1.agent INFO   [Stream] 任务完成: 获取《一夕千悟，从杂役弟子开始》第二章内容 (0.0s)
15:29:08 app.api.v1.agent INFO   [Stream] Task started: 获取《一夕千悟，从杂役弟子开始》第三章内容
15:29:08 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
15:29:08 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第3章: 第3章 一夕千悟
15:29:08 app.api.v1.agent INFO   [Stream] 任务完成: 获取《一夕千悟，从杂役弟子开始》第三章内容 (0.0s)
15:29:08 app.api.v1.agent INFO   [Stream] Task started: 获取《一夕千悟，从杂役弟子开始》第四章内容
15:29:08 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
15:29:08 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第4章: 第4章 家底
15:29:08 app.api.v1.agent INFO   [Stream] 任务完成: 获取《一夕千悟，从杂役弟子开始》第四章内容 (0.0s)
15:29:08 app.api.v1.agent INFO   [Stream] Task started: 获取《一夕千悟，从杂役弟子开始》第五章内容
15:29:08 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
15:29:08 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第5章: 第5章 太一门
15:29:08 app.api.v1.agent INFO   [Stream] 任务完成: 获取《一夕千悟，从杂役弟子开始》第五章内容 (0.0s)
15:29:08 app.api.v1.agent INFO   [Stream] Task started: 深度分析《一夕千悟，从杂役弟子开始》前5章的内容（人物关系、能力体系、世界观、伏笔）
15:29:08 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
15:29:08 app.prompts.constraint_manager INFO   ✅ 已加载模板: analyze_text (v3.1.0)
15:29:08 app.prompts.constraint_manager INFO   ✅ 已加载模板: creative_writing (v1.0.0)
15:29:08 app.prompts.constraint_manager INFO   ✅ 已加载模板: intent_classifier (v2.0.0)
15:29:08 app.prompts.constraint_manager INFO   ✅ 已加载模板: planning_agent (v2.0.0)
15:29:08 app.prompts.constraint_manager INFO   ✅ 已加载模板: query_agent (v2.0.0)
15:29:08 app.prompts.constraint_manager INFO   ✅ 已加载模板: system_agent (v2.0.0)
15:29:08 app.prompts.constraint_manager INFO   ✅ 已加载模板: tool_agent (v2.0.0)
15:29:08 app.prompts.constraint_manager INFO   ✅ 已加载模板: writing_agent (v2.0.0)
15:29:08 app.prompts.constraint_manager INFO   ✅ 约束提示词管理器已初始化: 加载8个模板, 注册0个验证器
15:29:08 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
15:29:08 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
15:29:08 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
15:29:10 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
15:29:40 app.services.ai.http_ai_service INFO   API 响应完成，共接收 61 个数据块，总长度: 3944
15:29:40 app.services.ai.http_ai_service INFO   流式响应Token统计: 17412 (prompt=14465, completion=2947)
15:29:40 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
15:29:40 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=17412, cost=$0.047551, time=31160ms
15:29:40 app.services.agent.langgraph_agent INFO   ✅ [Agent分析] 分析完成，结果长度: 3944
15:29:40 app.api.v1.agent INFO   [Stream] 任务完成: 深度分析《一夕千悟，从杂役弟子开始》前5章的内容（人物关系、能力体系、世界观、伏笔） (31.3s)
15:29:40 app.services.agent.deep_agent.reflection INFO   [Checkpoint] 任务 6 标记了 checkpoint，触发反思
15:29:40 app.services.agent.deep_agent.executor INFO   任务 6 触发反思检查点
15:29:40 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=500, temp=0.3, task_type=None
15:29:43 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
15:29:56 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 58
15:29:56 app.services.ai.http_ai_service INFO   流式响应Token统计: 1698 (prompt=1661, completion=37)
15:29:56 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
15:29:56 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1698, cost=$0.002446, time=16148ms
15:29:56 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=1698
15:29:56 app.services.agent.deep_agent.reflection INFO   [Reflection] 解析结果: needs_replan=True, first_line=REPLAN:YES, raw_len=58
15:29:56 app.services.agent.deep_agent.executor INFO   反思结果需要重规划 (第 1 次)
15:29:56 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=1000, temp=0.3, task_type=None
15:29:59 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
15:30:08 app.services.ai.http_ai_service INFO   API 响应完成，共接收 2 个数据块，总长度: 147
15:30:08 app.services.ai.http_ai_service INFO   流式响应Token统计: 1443 (prompt=1369, completion=74)
15:30:08 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
15:30:08 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1443, cost=$0.002451, time=12617ms
15:30:08 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=1443
15:30:08 app.api.v1.agent INFO   [Stream] Plan tasks: 8 items
15:30:08 app.services.agent.deep_agent.executor INFO   计划已更新，新任务数: 2
15:30:08 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=200, temp=0.1, task_type=None
15:30:11 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
15:30:18 app.services.agent.deep_agent.task_enricher WARNING   [TaskEnricher] AI 推断超时
15:30:18 app.services.agent.deep_agent.task_enricher WARNING   [TaskEnricher] 无法推断工具: '深度拆解前5章的能力体系、人物关系与核心伏笔...'
15:30:18 app.api.v1.agent INFO   [Stream] Task started: 深度拆解前5章的能力体系、人物关系与核心伏笔
15:30:18 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
15:30:18 app.api.v1.agent INFO   [Stream] 任务完成: 深度拆解前5章的能力体系、人物关系与核心伏笔 (0.0s)
15:30:18 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=200, temp=0.1, task_type=None
15:30:28 app.services.agent.deep_agent.task_enricher WARNING   [TaskEnricher] AI 推断超时
15:30:28 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] 规则匹配成功: '基于拆解结果，规划第6-10章的详细大纲...' → tool=get_chapter_by_order_tool
15:30:28 app.api.v1.agent INFO   [Stream] Task started: 基于拆解结果，规划第6-10章的详细大纲
15:30:28 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
15:30:29 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
15:30:29 app.api.v1.agent INFO   [Stream] 任务完成: 基于拆解结果，规划第6-10章的详细大纲 (0.0s)
15:30:29 app.services.agent.deep_agent.executor INFO   DeepAgent 执行完成: 任务=8, 反思=1, 重规划=1
15:30:29 app.services.agent.langgraph_agent INFO   [DeepAgent] 执行完成: 反思=1次, 重规划=1次
15:30:29 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共8个任务，耗时: 80.26s
15:30:29 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
15:30:29 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=0, 输出型=2, 展示型=6
15:30:29 app.services.agent.langgraph_agent INFO   [Response] 2个输出任务，简单拼接
15:30:29 app.api.v1.agent INFO   [Stream] 跳过最终响应（内容已流式发送）
15:30:29 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed
15:31:10 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
15:31:10 app.services.ai.http_ai_service INFO   ModelSelector 已启用
15:31:10 app.services.ai.http_ai_service INFO   AILogService 已启用 (用于成本追踪)
15:31:13 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
15:31:13 app.api.v1.agent INFO   [Chat Stream] Mode: planning
15:31:13 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:52653 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
15:31:13 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: planning, Message: 概括第五章的主要内容...
15:31:13 app.services.agent.langgraph_agent INFO   [Planning] 使用隔离的thread_id: c9dd9cbf-fa57-447e-9605-3020bbde5350:0702afa8-4fb8-4ac8-8321-166bc44beafe (work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, conversation_id=0702afa8-4fb8-4ac8-8321-166bc44beafe)
15:31:13 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: 概括第五章的主要内容...
15:31:13 app.core.cache INFO   ✅ 缓存命中: prompt:get_planning_agent_mode_prompt:fca6eb91156619d0
15:31:13 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
15:31:13 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
15:31:13 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=1200, temp=0.3, task_type=TaskType.SIMPLE_QA
15:31:16 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
15:31:19 app.services.ai.http_ai_service INFO   API 响应完成，共接收 6 个数据块，总长度: 632
15:31:19 app.services.ai.http_ai_service INFO   流式响应Token统计: 4040 (prompt=3785, completion=255)
15:31:20 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
15:31:20 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4040, cost=$0.007281, time=6020ms
15:31:20 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=4040
15:31:20 app.services.agent.langgraph_agent INFO   [JSON解析] 方法2成功: 从```json块提取
15:31:20 app.services.agent.langgraph_agent INFO   [Planning] 思维链: 输出=用户期望看到第五章内容的概括性摘要，而不是原文。, 原料=需要第五章的原文内容。, 处理=使用 get_chapter_by_or
15:31:20 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共2个任务，耗时: 6.26s
15:31:20 app.api.v1.agent INFO   [Stream] Plan tasks: 2 items
15:31:20 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
15:31:20 app.services.agent.langgraph_agent INFO   [DeepAgent] 启用反思模式
15:31:20 app.services.agent.parameter_resolver INFO   [ParameterResolver] 初始化完成, 严格模式: False
15:31:20 app.services.agent.langgraph_agent INFO   [DeepAgent] ParameterResolver 已启用
15:31:20 app.services.agent.deep_agent.executor INFO   DeepAgent 开始执行，共 2 个任务，反思功能已启用
15:31:20 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] AI 推断功能已启用
15:31:20 app.api.v1.agent INFO   [Stream] Task started: 获取第五章内容
15:31:20 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
15:31:20 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第5章: 第5章 太一门
15:31:20 app.api.v1.agent INFO   [Stream] 任务完成: 获取第五章内容 (0.1s)
15:31:20 app.api.v1.agent INFO   [Stream] Task started: 概括第五章的主要内容
15:31:20 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
15:31:20 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
15:31:20 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
15:31:20 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
15:31:22 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
15:31:38 app.services.ai.http_ai_service INFO   API 响应完成，共接收 26 个数据块，总长度: 2356
15:31:38 app.services.ai.http_ai_service INFO   流式响应Token统计: 6089 (prompt=4397, completion=1692)
15:31:38 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
15:31:38 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=6089, cost=$0.022416, time=18693ms
15:31:38 app.services.agent.langgraph_agent INFO   ✅ [Agent分析] 分析完成，结果长度: 2356
15:31:38 app.api.v1.agent INFO   [Stream] 任务完成: 概括第五章的主要内容 (18.8s)
15:31:38 app.services.agent.deep_agent.executor INFO   DeepAgent 执行完成: 任务=2, 反思=0, 重规划=0
15:31:38 app.services.agent.langgraph_agent INFO   [DeepAgent] 执行完成: 反思=0次, 重规划=0次
15:31:38 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共2个任务，耗时: 18.84s
15:31:38 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
15:31:38 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=0, 输出型=1, 展示型=1
15:31:38 app.services.agent.langgraph_agent INFO   [Response] 单个分析任务(analyze_text_tool)，使用AI格式化
15:31:38 app.services.agent.langgraph_agent INFO   [Summarization] 使用AI整合任务结果
15:31:38 app.services.agent.langgraph_agent INFO   [Summarization] 上下文压缩: 原始=5334字符, 压缩后=4087字符, 压缩率=24%
15:31:38 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
15:31:38 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
15:31:38 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
15:31:41 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
15:31:44 app.services.ai.http_ai_service INFO   API 响应完成，共接收 13 个数据块，总长度: 1109
15:31:44 app.services.ai.http_ai_service INFO   流式响应Token统计: 4464 (prompt=3628, completion=836)
15:31:44 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
15:31:44 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4464, cost=$0.012895, time=5873ms
15:31:44 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=4464
15:31:44 app.api.v1.agent INFO   [Stream] 跳过最终响应（内容已流式发送）
15:31:44 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed