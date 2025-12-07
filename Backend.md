14:51:51 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/auth/refresh
INFO:     127.0.0.1:52103 - "POST /api/v1/auth/refresh HTTP/1.1" 200 OK
14:51:53 app.api.v1.chapters INFO   [GET chapters] work_id=9398f47b-1e74-4e1c-93dd-e837e51dbaaf, user_id=602f5147-846a-4cde-95d3-405fa75f133f
14:51:53 app.api.v1.chapters INFO   ⚠️ [GET chapters] 缓存未命中: chapters:work:9398f47b-1e74-4e1c-93dd-e837e51dbaaf
14:51:53 app.services.chapter_service INFO   [ChapterService] Querying chapters for work_id=9398f47b-1e74-4e1c-93dd-e837e51dbaaf, type=<class 'uuid.UUID'>
14:51:53 app.services.chapter_service INFO   [ChapterService] Found 5 chapters
14:51:53 app.services.chapter_service INFO     - Chapter: 百年关，天机变, order=1
14:51:53 app.services.chapter_service INFO     - Chapter: 道祖出关，太极震群魔, order=2
14:51:53 app.services.chapter_service INFO     - Chapter: 下山, order=3
14:51:53 app.services.chapter_service INFO     - Chapter: 荒村孤烟，道祖传心, order=4
14:51:53 app.services.chapter_service INFO     - Chapter: 一饭之恩，乱世人心, order=5
14:51:53 app.api.v1.chapters INFO   [GET chapters] Returning 5 chapters
14:51:53 app.api.v1.chapters INFO   💾 [GET chapters] 缓存已保存: chapters:work:9398f47b-1e74-4e1c-93dd-e837e51dbaaf (expire=60s)
14:51:53 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/chapters/work/9398f47b-1e74-4e1c-93dd-e837e51dbaaf
14:51:53 app.api.v1.worldview INFO   ⚠️ [Worldview] 缓存未命中: worldview:settings:9398f47b-1e74-4e1c-93dd-e837e51dbaaf
14:51:53 app.api.v1.worldview INFO   ⚠️ [Worldview] 缓存未命中: worldview:characters:9398f47b-1e74-4e1c-93dd-e837e51dbaaf
INFO:     127.0.0.1:52103 - "GET /api/v1/chapters/work/9398f47b-1e74-4e1c-93dd-e837e51dbaaf HTTP/1.1" 200 OK
14:51:53 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:settings:9398f47b-1e74-4e1c-93dd-e837e51dbaaf (expire=300s)
14:51:53 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works/9398f47b-1e74-4e1c-93dd-e837e51dbaaf
14:51:53 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:characters:9398f47b-1e74-4e1c-93dd-e837e51dbaaf (expire=300s)
14:51:53 app.api.v1.worldview INFO   ⚠️ [Worldview] 缓存未命中: worldview:locations:9398f47b-1e74-4e1c-93dd-e837e51dbaaf
14:51:53 app.api.v1.worldview INFO   ⚠️ [Worldview] 缓存未命中: worldview:guidelines:9398f47b-1e74-4e1c-93dd-e837e51dbaaf
INFO:     127.0.0.1:56904 - "GET /api/v1/works/9398f47b-1e74-4e1c-93dd-e837e51dbaaf HTTP/1.1" 200 OK
14:51:53 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/9398f47b-1e74-4e1c-93dd-e837e51dbaaf/settings
14:51:53 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:locations:9398f47b-1e74-4e1c-93dd-e837e51dbaaf (expire=300s)
14:51:53 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/9398f47b-1e74-4e1c-93dd-e837e51dbaaf/characters
14:51:53 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:guidelines:9398f47b-1e74-4e1c-93dd-e837e51dbaaf (expire=300s)
INFO:     127.0.0.1:59638 - "GET /api/v1/worldview/works/9398f47b-1e74-4e1c-93dd-e837e51dbaaf/settings HTTP/1.1" 200 OK
INFO:     127.0.0.1:59250 - "GET /api/v1/worldview/works/9398f47b-1e74-4e1c-93dd-e837e51dbaaf/characters HTTP/1.1" 200 OK
14:51:53 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/9398f47b-1e74-4e1c-93dd-e837e51dbaaf/locations
14:51:53 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/9398f47b-1e74-4e1c-93dd-e837e51dbaaf/guidelines
INFO:     127.0.0.1:50476 - "GET /api/v1/worldview/works/9398f47b-1e74-4e1c-93dd-e837e51dbaaf/locations HTTP/1.1" 200 OK
INFO:     127.0.0.1:64364 - "GET /api/v1/worldview/works/9398f47b-1e74-4e1c-93dd-e837e51dbaaf/guidelines HTTP/1.1" 200 OK
14:51:53 app.api.v1.worldview INFO   ⚠️ [Worldview] 缓存未命中: worldview:ai-guidelines:9398f47b-1e74-4e1c-93dd-e837e51dbaaf
14:51:53 app.api.v1.chapters INFO   [GET chapters] work_id=9398f47b-1e74-4e1c-93dd-e837e51dbaaf, user_id=602f5147-846a-4cde-95d3-405fa75f133f
14:51:53 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:ai-guidelines:9398f47b-1e74-4e1c-93dd-e837e51dbaaf (expire=300s)
14:51:53 app.api.v1.chapters INFO   ✅ [GET chapters] 缓存命中: chapters:work:9398f47b-1e74-4e1c-93dd-e837e51dbaaf
14:51:53 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/9398f47b-1e74-4e1c-93dd-e837e51dbaaf/ai-guidelines
14:51:53 app.api.v1.worldview INFO   ✅ [Worldview] 缓存命中: worldview:settings:9398f47b-1e74-4e1c-93dd-e837e51dbaaf
INFO:     127.0.0.1:52103 - "GET /api/v1/worldview/works/9398f47b-1e74-4e1c-93dd-e837e51dbaaf/ai-guidelines HTTP/1.1" 200 OK
14:51:53 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/chapters/work/9398f47b-1e74-4e1c-93dd-e837e51dbaaf
INFO:     127.0.0.1:56904 - "GET /api/v1/chapters/work/9398f47b-1e74-4e1c-93dd-e837e51dbaaf HTTP/1.1" 200 OK
14:51:53 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works/9398f47b-1e74-4e1c-93dd-e837e51dbaaf
14:51:53 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/9398f47b-1e74-4e1c-93dd-e837e51dbaaf/settings
14:51:53 app.api.v1.worldview INFO   ✅ [Worldview] 缓存命中: worldview:characters:9398f47b-1e74-4e1c-93dd-e837e51dbaaf
14:51:53 app.api.v1.worldview INFO   ✅ [Worldview] 缓存命中: worldview:locations:9398f47b-1e74-4e1c-93dd-e837e51dbaaf
INFO:     127.0.0.1:59638 - "GET /api/v1/works/9398f47b-1e74-4e1c-93dd-e837e51dbaaf HTTP/1.1" 200 OK
INFO:     127.0.0.1:59250 - "GET /api/v1/worldview/works/9398f47b-1e74-4e1c-93dd-e837e51dbaaf/settings HTTP/1.1" 200 OK
14:51:53 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/9398f47b-1e74-4e1c-93dd-e837e51dbaaf/characters
14:51:53 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/9398f47b-1e74-4e1c-93dd-e837e51dbaaf/locations
INFO:     127.0.0.1:50476 - "GET /api/v1/worldview/works/9398f47b-1e74-4e1c-93dd-e837e51dbaaf/characters HTTP/1.1" 200 OK
INFO:     127.0.0.1:64364 - "GET /api/v1/worldview/works/9398f47b-1e74-4e1c-93dd-e837e51dbaaf/locations HTTP/1.1" 200 OK
14:51:53 app.api.v1.worldview INFO   ✅ [Worldview] 缓存命中: worldview:guidelines:9398f47b-1e74-4e1c-93dd-e837e51dbaaf
14:51:53 app.api.v1.worldview INFO   ✅ [Worldview] 缓存命中: worldview:ai-guidelines:9398f47b-1e74-4e1c-93dd-e837e51dbaaf
14:51:53 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/9398f47b-1e74-4e1c-93dd-e837e51dbaaf/guidelines
INFO:     127.0.0.1:52103 - "GET /api/v1/worldview/works/9398f47b-1e74-4e1c-93dd-e837e51dbaaf/guidelines HTTP/1.1" 200 OK
14:51:53 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/9398f47b-1e74-4e1c-93dd-e837e51dbaaf/ai-guidelines
INFO:     127.0.0.1:56904 - "GET /api/v1/worldview/works/9398f47b-1e74-4e1c-93dd-e837e51dbaaf/ai-guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:56904 - "OPTIONS /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
14:51:53 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: 9398f47b-1e74-4e1c-93dd-e837e51dbaaf, chapter_id: 6481bdc8-3657-4aca-a638-af31744a57cf
14:51:54 app.core.redis INFO   ✅ Redis connected: redis://localhost:6379/0
14:51:54 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: 9398f47b-1e74-4e1c-93dd-e837e51dbaaf, chapter_id: 6481bdc8-3657-4aca-a638-af31744a57cf
14:51:54 app.api.v1.ai INFO   [预加载] AI Guidelines 缓存已存在: 9398f47b-1e74-4e1c-93dd-e837e51dbaaf
14:51:54 app.api.v1.ai INFO   [预加载] 当前章节已加载: 6481bdc8-3657-4aca-a638-af31744a57cf
14:51:54 app.api.v1.ai INFO   [预加载] AI Guidelines 缓存已存在: 9398f47b-1e74-4e1c-93dd-e837e51dbaaf
14:51:54 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': True, 'current_chapter': True, 'previous_chapter': False}
14:51:54 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
14:51:54 app.api.v1.ai INFO   [预加载] 当前章节已加载: 6481bdc8-3657-4aca-a638-af31744a57cf
INFO:     127.0.0.1:52103 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
14:51:54 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': True, 'current_chapter': True, 'previous_chapter': False}
14:51:54 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:56904 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
INFO:     127.0.0.1:56904 - "OPTIONS /api/v1/chapters/6481bdc8-3657-4aca-a638-af31744a57cf HTTP/1.1" 200 OK
14:51:54 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:9398f47b-1e74-4e1c-93dd-e837e51dbaaf
14:51:54 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/6481bdc8-3657-4aca-a638-af31744a57cf
INFO:     127.0.0.1:52103 - "PUT /api/v1/chapters/6481bdc8-3657-4aca-a638-af31744a57cf HTTP/1.1" 200 OK
14:51:54 app.services.chapter_vector_service INFO   开始向量化章节: 百年关，天机变 (order=1)
14:51:55 app.services.chapter_vector_service INFO   ✅ 章节向量存储完成: 百年关，天机变 (5段)
14:51:55 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:9398f47b-1e74-4e1c-93dd-e837e51dbaaf
14:51:55 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/6481bdc8-3657-4aca-a638-af31744a57cf
INFO:     127.0.0.1:52103 - "PUT /api/v1/chapters/6481bdc8-3657-4aca-a638-af31744a57cf HTTP/1.1" 200 OK
14:51:55 app.services.chapter_vector_service INFO   开始向量化章节: 百年关，天机变 (order=1)
14:51:56 app.services.chapter_vector_service INFO   ✅ 章节向量存储完成: 百年关，天机变 (5段)
INFO:     127.0.0.1:52103 - "OPTIONS /api/v1/agent/chat/stream HTTP/1.1" 200 OK
14:51:57 app.services.ai.prompts INFO   Prompts loaded successfully from D:\Java\ai_writer\backend\app\services\ai\prompts\default.json
14:51:57 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
14:51:57 app.services.ai.http_ai_service INFO   ModelSelector 已启用
14:51:57 app.services.ai.http_ai_service INFO   AILogService 已启用 (用于成本追踪)
14:52:00 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
14:52:00 app.api.v1.agent INFO   [Chat Stream] Mode: planning
14:52:00 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:56904 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
14:52:00 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: planning, Message: 第五章的标题是什么？...
14:52:00 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
14:52:00 app.services.ai.http_ai_service INFO   ModelSelector 已启用
14:52:00 app.services.ai.http_ai_service INFO   [成本追踪] 初始化未传db/user_id，将使用请求上下文按需记录成本
14:52:04 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
14:52:04 app.services.context.adaptive_budget INFO   ✅ 所有预算配置验证通过
14:52:14 app.services.context.vector_memory_store INFO   ✅ VectorMemoryStore初始化成功 | 目录=./data/chroma_db | 模型=paraphrase-multilingual-MiniLM-L12-v2 | 集合=user_memories
14:52:14 app.services.context.manager INFO   ✅ VectorMemoryStore 已初始化
14:52:14 app.services.context.manager INFO   ✅ ContextManager: 长期记忆已启用 (user_id=None)
14:52:14 app.services.context.manager INFO   ✅ ContextManager: 自适应预算已启用
14:52:14 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ ContextManager已初始化（长期记忆已启用，自适应预算已启用，总预算=16000 tokens）
成功加载模板: intent_classifier (版本 2.0.0)
成功加载模板: writing_agent (版本 2.0.0)
成功加载模板: planning_agent (版本 2.0.0)
成功加载模板: tool_agent (版本 2.0.0)
成功加载模板: query_agent (版本 2.0.0)
成功加载模板: system_agent_prompt (版本 2.0.0)
成功加载模板: creative_writing_prompt (版本 1.0.0)
14:52:14 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ PromptManager已初始化
14:52:14 app.services.agent.langgraph_agent INFO   [LangGraph] 使用 HTTPAIService 模式（手动工具调用，绕过 Cloudflare）
14:52:14 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ Redis连接验证成功
14:52:14 app.services.agent.langgraph_agent INFO   [LangGraph] OK 使用 AsyncRedisSaver（redis://localhost:6379/0，TTL=7天）
14:52:14 app.services.agent.memory.metrics INFO   [MemoryMetrics] 监控系统已初始化
14:52:14 app.services.agent.memory.long_term_store INFO   [LongTermStore] Initialized: base_dir=./data/long_term_memory, max_size=50KB, compression=True
14:52:14 app.services.agent.memory.enhanced_memory_manager INFO   EnhancedMemoryManager initialized: short=10, medium=100, threshold=0.1, long_term_backup=enabled
14:52:14 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ EnhancedMemoryManager已创建
14:52:14 app.services.agent.memory.unified_coordinator INFO   [UnifiedMemoryCoordinator] 初始化统一记忆协调器
14:52:14 app.services.agent.memory.unified_coordinator INFO   [UnifiedMemoryCoordinator] 全局实例已设置
14:52:14 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ UnifiedMemoryCoordinator已初始化 | checkpointer=AsyncRedisSaver | enhanced_memory=yes | context_manager=yes
14:52:14 app.services.agent.parallel_tool_node INFO   [ParallelToolNode] 初始化完成，最大并发数=5，并行安全工具=4个
14:52:14 app.api.v1.agent INFO   [Global Agent] created global agent instance; MemorySaver shared across requests
14:52:14 app.services.agent.langgraph_agent INFO   [Planning] 使用隔离的thread_id: 9398f47b-1e74-4e1c-93dd-e837e51dbaaf:cd025001-1109-41f5-bded-f13997cd146c (work_id=9398f47b-1e74-4e1c-93dd-e837e51dbaaf, conversation_id=cd025001-1109-41f5-bded-f13997cd146c)
14:52:14 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: 第五章的标题是什么？...
14:52:14 app.core.cache INFO   ✅ 缓存命中: prompt:get_planning_static_prompt:fca6eb91156619d0
14:52:14 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
14:52:14 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
14:52:14 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=1200, temp=0.3, task_type=TaskType.SIMPLE_QA
14:52:17 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
14:52:28 app.services.ai.http_ai_service INFO   API 响应完成，共接收 6 个数据块，总长度: 642
14:52:28 app.services.ai.http_ai_service INFO   流式响应Token统计: 4334 (prompt=4081, completion=253)
14:52:28 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
14:52:28 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4334, cost=$0.007631, time=13945ms
14:52:28 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=4334
14:52:28 app.services.agent.langgraph_agent INFO   [JSON解析] 方法2成功: 从```json块提取
14:52:28 app.services.agent.langgraph_agent INFO   [Planning] 思维链: 输出=用户期望看到一个文本字符串，即第五章的标题。, 原料=需要第五章的内容。可以使用 `get_c, 处理=获取第五章内容后，使用 `analyze
14:52:28 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共2个任务，耗时: 13.98s
14:52:28 app.api.v1.agent INFO   [Stream] Plan tasks: 2 items
14:52:28 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
14:52:28 app.services.agent.parameter_resolver INFO   [ParameterResolver] 初始化完成, 严格模式: False
14:52:28 app.services.agent.langgraph_agent INFO   [ParameterResolver] 参数解析器已启用
14:52:28 app.services.agent.langgraph_agent INFO   [ParallelExecution] 任务分组: 并行=1, 串行=1
14:52:28 app.services.agent.langgraph_agent INFO   [ParallelExecution] 开始并行执行1个任务
14:52:28 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务1开始: 获取第五章的内容
14:52:28 app.api.v1.agent INFO   [Stream] Task started: 获取第五章的内容
14:52:28 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
14:52:28 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第5章: 一饭之恩，乱世人心
14:52:28 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务1完成
14:52:28 app.api.v1.agent INFO   [Stream] 任务完成: 获取第五章的内容 (0.0s)
14:52:28 app.services.agent.langgraph_agent INFO   [ParallelExecution] 开始串行执行1个任务
14:52:28 app.services.agent.langgraph_agent INFO   [ParallelExecution] 串行任务2开始: 从第五章内容中提取标题
14:52:28 app.api.v1.agent INFO   [Stream] Task started: 从第五章内容中提取标题
14:52:28 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
14:52:28 app.prompts.constraint_manager INFO   ✅ 已加载模板: analyze_text (v3.1.0)
14:52:28 app.prompts.constraint_manager INFO   ✅ 已加载模板: creative_writing (v1.0.0)
14:52:28 app.prompts.constraint_manager INFO   ✅ 已加载模板: intent_classifier (v2.0.0)
14:52:28 app.prompts.constraint_manager INFO   ✅ 已加载模板: planning_agent (v2.0.0)
14:52:28 app.prompts.constraint_manager INFO   ✅ 已加载模板: query_agent (v2.0.0)
14:52:28 app.prompts.constraint_manager INFO   ✅ 已加载模板: system_agent (v2.0.0)
14:52:28 app.prompts.constraint_manager INFO   ✅ 已加载模板: tool_agent (v2.0.0)
14:52:28 app.prompts.constraint_manager INFO   ✅ 已加载模板: writing_agent (v2.0.0)
14:52:28 app.prompts.constraint_manager INFO   ✅ 约束提示词管理器已初始化: 加载8个模板, 注册0个验证器
14:52:28 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
14:52:28 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
14:52:28 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
14:52:31 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
14:52:50 app.services.ai.http_ai_service INFO   API 响应完成，共接收 27 个数据块，总长度: 2365
14:52:50 app.services.ai.http_ai_service INFO   流式响应Token统计: 6307 (prompt=4561, completion=1746)
14:52:50 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
14:52:50 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=6307, cost=$0.023161, time=22043ms
14:52:50 app.services.agent.langgraph_agent INFO   ✅ [Agent分析] 分析完成，结果长度: 2365
14:52:50 app.services.agent.langgraph_agent INFO   [ParallelExecution] 串行任务2完成
14:52:50 app.api.v1.agent INFO   [Stream] 任务完成: 从第五章内容中提取标题 (22.1s)
14:52:50 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共2个任务，耗时: 22.11s
14:52:50 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
14:52:50 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=0, 输出型=1, 展示型=1
14:52:50 app.services.agent.langgraph_agent INFO   [Response] 单个分析任务(analyze_text_tool)，使用AI格式化
14:52:50 app.services.agent.langgraph_agent INFO   [Summarization] 使用AI整合任务结果
14:52:50 app.services.agent.langgraph_agent INFO   [Summarization] 上下文压缩: 原始=5223字符, 压缩后=2162字符, 压缩率=59%
14:52:50 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
14:52:50 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
14:52:50 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
14:52:52 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
14:52:53 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 25
14:52:53 app.services.ai.http_ai_service INFO   流式响应Token统计: 2101 (prompt=2083, completion=18)
14:52:53 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
14:52:53 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2101, cost=$0.002784, time=3178ms
14:52:53 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=2101
14:52:53 app.api.v1.agent INFO   [Stream] 跳过最终响应（内容已流式发送）
14:52:53 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed