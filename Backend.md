16:49:40 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/auth/refresh
INFO:     127.0.0.1:51330 - "POST /api/v1/auth/refresh HTTP/1.1" 200 OK
16:49:41 app.api.v1.chapters INFO   [GET chapters] work_id=9398f47b-1e74-4e1c-93dd-e837e51dbaaf, user_id=602f5147-846a-4cde-95d3-405fa75f133f
16:49:41 app.api.v1.chapters INFO   ⚠️ [GET chapters] 缓存未命中: chapters:work:9398f47b-1e74-4e1c-93dd-e837e51dbaaf
16:49:41 app.services.chapter_service INFO   [ChapterService] Querying chapters for work_id=9398f47b-1e74-4e1c-93dd-e837e51dbaaf, type=<class 'uuid.UUID'>
16:49:41 app.api.v1.worldview INFO   ⚠️ [Worldview] 缓存未命中: worldview:settings:9398f47b-1e74-4e1c-93dd-e837e51dbaaf
16:49:41 app.api.v1.worldview INFO   ⚠️ [Worldview] 缓存未命中: worldview:characters:9398f47b-1e74-4e1c-93dd-e837e51dbaaf
16:49:41 app.api.v1.worldview INFO   ⚠️ [Worldview] 缓存未命中: worldview:locations:9398f47b-1e74-4e1c-93dd-e837e51dbaaf
16:49:41 app.services.chapter_service INFO   [ChapterService] Found 5 chapters
16:49:41 app.services.chapter_service INFO     - Chapter: 百年关，天机变, order=1
16:49:41 app.services.chapter_service INFO     - Chapter: 道祖出关，太极震群魔, order=2
16:49:41 app.services.chapter_service INFO     - Chapter: 下山, order=3
16:49:41 app.services.chapter_service INFO     - Chapter: 荒村孤烟，道祖传心, order=4
16:49:41 app.services.chapter_service INFO     - Chapter: 一饭之恩，乱世人心, order=5
16:49:41 app.api.v1.chapters INFO   [GET chapters] Returning 5 chapters
16:49:41 app.api.v1.chapters INFO   💾 [GET chapters] 缓存已保存: chapters:work:9398f47b-1e74-4e1c-93dd-e837e51dbaaf (expire=60s)
16:49:41 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works/9398f47b-1e74-4e1c-93dd-e837e51dbaaf
16:49:41 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:settings:9398f47b-1e74-4e1c-93dd-e837e51dbaaf (expire=300s)
16:49:41 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:characters:9398f47b-1e74-4e1c-93dd-e837e51dbaaf (expire=300s)
16:49:41 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:locations:9398f47b-1e74-4e1c-93dd-e837e51dbaaf (expire=300s)
16:49:41 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works/9398f47b-1e74-4e1c-93dd-e837e51dbaaf
INFO:     127.0.0.1:51331 - "GET /api/v1/works/9398f47b-1e74-4e1c-93dd-e837e51dbaaf HTTP/1.1" 200 OK
INFO:     127.0.0.1:51330 - "GET /api/v1/works/9398f47b-1e74-4e1c-93dd-e837e51dbaaf HTTP/1.1" 200 OK
16:49:41 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/chapters/work/9398f47b-1e74-4e1c-93dd-e837e51dbaaf
16:49:41 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/9398f47b-1e74-4e1c-93dd-e837e51dbaaf/settings
16:49:41 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/9398f47b-1e74-4e1c-93dd-e837e51dbaaf/characters
16:49:41 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/9398f47b-1e74-4e1c-93dd-e837e51dbaaf/locations
INFO:     127.0.0.1:51327 - "GET /api/v1/chapters/work/9398f47b-1e74-4e1c-93dd-e837e51dbaaf HTTP/1.1" 200 OK
INFO:     127.0.0.1:51328 - "GET /api/v1/worldview/works/9398f47b-1e74-4e1c-93dd-e837e51dbaaf/settings HTTP/1.1" 200 OK
INFO:     127.0.0.1:51329 - "GET /api/v1/worldview/works/9398f47b-1e74-4e1c-93dd-e837e51dbaaf/characters HTTP/1.1" 200 OK
INFO:     127.0.0.1:51332 - "GET /api/v1/worldview/works/9398f47b-1e74-4e1c-93dd-e837e51dbaaf/locations HTTP/1.1" 200 OK
16:49:41 app.api.v1.chapters INFO   [GET chapters] work_id=9398f47b-1e74-4e1c-93dd-e837e51dbaaf, user_id=602f5147-846a-4cde-95d3-405fa75f133f
16:49:41 app.api.v1.worldview INFO   ⚠️ [Worldview] 缓存未命中: worldview:guidelines:9398f47b-1e74-4e1c-93dd-e837e51dbaaf
16:49:41 app.api.v1.chapters INFO   ✅ [GET chapters] 缓存命中: chapters:work:9398f47b-1e74-4e1c-93dd-e837e51dbaaf
16:49:41 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:guidelines:9398f47b-1e74-4e1c-93dd-e837e51dbaaf (expire=300s)
16:49:41 app.api.v1.worldview INFO   ✅ [Worldview] 缓存命中: worldview:locations:9398f47b-1e74-4e1c-93dd-e837e51dbaaf
16:49:41 app.api.v1.worldview INFO   ✅ [Worldview] 缓存命中: worldview:characters:9398f47b-1e74-4e1c-93dd-e837e51dbaaf
16:49:41 app.api.v1.worldview INFO   ✅ [Worldview] 缓存命中: worldview:settings:9398f47b-1e74-4e1c-93dd-e837e51dbaaf
16:49:41 app.api.v1.worldview INFO   ⚠️ [Worldview] 缓存未命中: worldview:ai-guidelines:9398f47b-1e74-4e1c-93dd-e837e51dbaaf
16:49:41 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/chapters/work/9398f47b-1e74-4e1c-93dd-e837e51dbaaf
16:49:41 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/9398f47b-1e74-4e1c-93dd-e837e51dbaaf/guidelines
16:49:41 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/9398f47b-1e74-4e1c-93dd-e837e51dbaaf/locations
INFO:     127.0.0.1:51331 - "GET /api/v1/chapters/work/9398f47b-1e74-4e1c-93dd-e837e51dbaaf HTTP/1.1" 200 OK
16:49:41 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/9398f47b-1e74-4e1c-93dd-e837e51dbaaf/characters
16:49:41 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/9398f47b-1e74-4e1c-93dd-e837e51dbaaf/settings
16:49:41 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:ai-guidelines:9398f47b-1e74-4e1c-93dd-e837e51dbaaf (expire=300s)
INFO:     127.0.0.1:51330 - "GET /api/v1/worldview/works/9398f47b-1e74-4e1c-93dd-e837e51dbaaf/guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:51327 - "GET /api/v1/worldview/works/9398f47b-1e74-4e1c-93dd-e837e51dbaaf/locations HTTP/1.1" 200 OK
INFO:     127.0.0.1:51328 - "GET /api/v1/worldview/works/9398f47b-1e74-4e1c-93dd-e837e51dbaaf/characters HTTP/1.1" 200 OK
INFO:     127.0.0.1:51329 - "GET /api/v1/worldview/works/9398f47b-1e74-4e1c-93dd-e837e51dbaaf/settings HTTP/1.1" 200 OK
16:49:41 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/9398f47b-1e74-4e1c-93dd-e837e51dbaaf/ai-guidelines
INFO:     127.0.0.1:51332 - "GET /api/v1/worldview/works/9398f47b-1e74-4e1c-93dd-e837e51dbaaf/ai-guidelines HTTP/1.1" 200 OK
16:49:41 app.api.v1.worldview INFO   ✅ [Worldview] 缓存命中: worldview:guidelines:9398f47b-1e74-4e1c-93dd-e837e51dbaaf
16:49:41 app.api.v1.worldview INFO   ✅ [Worldview] 缓存命中: worldview:ai-guidelines:9398f47b-1e74-4e1c-93dd-e837e51dbaaf
16:49:41 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/9398f47b-1e74-4e1c-93dd-e837e51dbaaf/guidelines
16:49:41 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/9398f47b-1e74-4e1c-93dd-e837e51dbaaf/ai-guidelines
INFO:     127.0.0.1:51331 - "GET /api/v1/worldview/works/9398f47b-1e74-4e1c-93dd-e837e51dbaaf/guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:51330 - "GET /api/v1/worldview/works/9398f47b-1e74-4e1c-93dd-e837e51dbaaf/ai-guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:51327 - "OPTIONS /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
16:49:42 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: 9398f47b-1e74-4e1c-93dd-e837e51dbaaf, chapter_id: 6481bdc8-3657-4aca-a638-af31744a57cf
16:49:42 app.core.redis INFO   ✅ Redis connected: redis://localhost:6379/0
16:49:42 app.api.v1.ai INFO   [预加载] AI Guidelines 已缓存: 9398f47b-1e74-4e1c-93dd-e837e51dbaaf
16:49:42 app.api.v1.ai INFO   [预加载] 当前章节已加载: 6481bdc8-3657-4aca-a638-af31744a57cf
16:49:42 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': True, 'current_chapter': True, 'previous_chapter': False}
16:49:42 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:51331 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
16:49:42 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: 9398f47b-1e74-4e1c-93dd-e837e51dbaaf, chapter_id: 6481bdc8-3657-4aca-a638-af31744a57cf
16:49:42 app.api.v1.ai INFO   [预加载] AI Guidelines 缓存已存在: 9398f47b-1e74-4e1c-93dd-e837e51dbaaf
16:49:42 app.api.v1.ai INFO   [预加载] 当前章节已加载: 6481bdc8-3657-4aca-a638-af31744a57cf
16:49:42 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': True, 'current_chapter': True, 'previous_chapter': False}
16:49:42 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:51327 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
INFO:     127.0.0.1:51331 - "OPTIONS /api/v1/chapters/6481bdc8-3657-4aca-a638-af31744a57cf HTTP/1.1" 200 OK
16:49:42 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:9398f47b-1e74-4e1c-93dd-e837e51dbaaf
16:49:42 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/6481bdc8-3657-4aca-a638-af31744a57cf
INFO:     127.0.0.1:51327 - "PUT /api/v1/chapters/6481bdc8-3657-4aca-a638-af31744a57cf HTTP/1.1" 200 OK
16:49:42 app.services.chapter_vector_service INFO   开始向量化章节: 百年关，天机变 (order=1)
16:49:44 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:9398f47b-1e74-4e1c-93dd-e837e51dbaaf
16:49:44 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/6481bdc8-3657-4aca-a638-af31744a57cf
INFO:     127.0.0.1:51331 - "PUT /api/v1/chapters/6481bdc8-3657-4aca-a638-af31744a57cf HTTP/1.1" 200 OK
16:49:44 app.services.chapter_vector_service INFO   开始向量化章节: 百年关，天机变 (order=1)
16:49:44 app.services.chapter_vector_service INFO   ✅ 章节向量存储完成: 百年关，天机变 (5段)
16:49:45 app.services.chapter_vector_service INFO   ✅ 章节向量存储完成: 百年关，天机变 (5段)
INFO:     127.0.0.1:64139 - "OPTIONS /api/v1/agent/chat/stream HTTP/1.1" 200 OK
16:49:53 app.services.ai.prompts INFO   Prompts loaded successfully from D:\Java\ai_writer\backend\app\services\ai\prompts\default.json
16:49:53 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
16:49:53 app.services.ai.http_ai_service INFO   ModelSelector 已启用
16:49:53 app.services.ai.http_ai_service INFO   AILogService 已启用 (用于成本追踪)
16:49:55 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
16:49:55 app.api.v1.agent INFO   [Chat Stream] Mode: planning
16:49:55 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:64139 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
16:49:55 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: planning, Message: 第五章的标题是什么？...
16:49:55 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
16:49:55 app.services.ai.http_ai_service INFO   ModelSelector 已启用
16:49:55 app.services.ai.http_ai_service INFO   [成本追踪] 初始化未传db/user_id，将使用请求上下文按需记录成本
16:49:59 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
16:49:59 app.services.context.adaptive_budget INFO   ✅ 所有预算配置验证通过
16:50:08 app.services.context.vector_memory_store INFO   ✅ VectorMemoryStore初始化成功 | 目录=./data/chroma_db | 模型=paraphrase-multilingual-MiniLM-L12-v2 | 集合=user_memories
16:50:08 app.services.context.manager INFO   ✅ VectorMemoryStore 已初始化
16:50:08 app.services.context.manager INFO   ✅ ContextManager: 长期记忆已启用 (user_id=None)
16:50:08 app.services.context.manager INFO   ✅ ContextManager: 自适应预算已启用
16:50:08 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ ContextManager已初始化（长期记忆已启用，自适应预算已启用，总预算=16000 tokens）
成功加载模板: intent_classifier (版本 2.0.0)
成功加载模板: writing_agent (版本 2.0.0)
成功加载模板: planning_agent (版本 2.0.0)
成功加载模板: tool_agent (版本 2.0.0)
成功加载模板: query_agent (版本 2.0.0)
成功加载模板: system_agent_prompt (版本 2.0.0)
成功加载模板: creative_writing_prompt (版本 1.0.0)
16:50:08 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ PromptManager已初始化
16:50:08 app.services.agent.langgraph_agent INFO   [LangGraph] 使用 HTTPAIService 模式（手动工具调用，绕过 Cloudflare）
16:50:08 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ Redis连接验证成功
16:50:08 app.services.agent.langgraph_agent INFO   [LangGraph] OK 使用 AsyncRedisSaver（redis://localhost:6379/0，TTL=7天）
16:50:08 app.services.agent.memory.metrics INFO   [MemoryMetrics] 监控系统已初始化
16:50:08 app.services.agent.memory.long_term_store INFO   [LongTermStore] Initialized: base_dir=./data/long_term_memory, max_size=50KB, compression=True
16:50:08 app.services.agent.memory.enhanced_memory_manager INFO   EnhancedMemoryManager initialized: short=10, medium=100, threshold=0.1, long_term_backup=enabled
16:50:08 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ EnhancedMemoryManager已创建
16:50:08 app.services.agent.memory.unified_coordinator INFO   [UnifiedMemoryCoordinator] 初始化统一记忆协调器
16:50:08 app.services.agent.memory.unified_coordinator INFO   [UnifiedMemoryCoordinator] 全局实例已设置
16:50:08 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ UnifiedMemoryCoordinator已初始化 | checkpointer=AsyncRedisSaver | enhanced_memory=yes | context_manager=yes
16:50:08 app.services.agent.parallel_tool_node INFO   [ParallelToolNode] 初始化完成，最大并发数=5，并行安全工具=4个
16:50:09 app.api.v1.agent INFO   [Global Agent] created global agent instance; MemorySaver shared across requests
16:50:09 app.services.agent.langgraph_agent INFO   [Planning] 使用隔离的thread_id: 9398f47b-1e74-4e1c-93dd-e837e51dbaaf:b33918f6-e912-42b5-9541-88ecdd1ef0ce (work_id=9398f47b-1e74-4e1c-93dd-e837e51dbaaf, conversation_id=b33918f6-e912-42b5-9541-88ecdd1ef0ce)
16:50:09 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: 第五章的标题是什么？...
16:50:09 app.core.cache INFO   ⚠️ 缓存未命中: prompt:get_planning_static_prompt:fca6eb91156619d0
16:50:09 app.core.cache INFO   💾 缓存已保存: prompt:get_planning_static_prompt:fca6eb91156619d0 (expire=3600s)
16:50:09 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
16:50:09 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
16:50:09 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=1200, temp=0.3, task_type=TaskType.SIMPLE_QA
16:50:11 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
16:50:13 app.services.ai.http_ai_service INFO   API 响应完成，共接收 5 个数据块，总长度: 479
16:50:13 app.services.ai.http_ai_service INFO   流式响应Token统计: 3319 (prompt=3105, completion=214)
16:50:13 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
16:50:13 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=3319, cost=$0.006021, time=4284ms
16:50:13 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=3319
16:50:13 app.services.agent.langgraph_agent INFO   [JSON解析] 方法2成功: 从```json块提取
16:50:13 app.services.agent.langgraph_agent INFO   [Planning] 思维链: 输出=用户想知道第五章的标题（元数据查询）, 原料=需要第五章的元数据, 处理=get_chapter_by_order
16:50:13 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共1个任务，耗时: 4.37s
16:50:13 app.api.v1.agent INFO   [Stream] Plan tasks: 1 items
16:50:13 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
16:50:13 app.services.agent.parameter_resolver INFO   [ParameterResolver] 初始化完成, 严格模式: False
16:50:13 app.services.agent.langgraph_agent INFO   [ParameterResolver] 参数解析器已启用
16:50:13 app.services.agent.langgraph_agent INFO   [ParallelExecution] 任务分组: 并行=1, 串行=0
16:50:13 app.services.agent.langgraph_agent INFO   [ParallelExecution] 开始并行执行1个任务
16:50:13 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务1开始: 获取第五章信息
16:50:13 app.api.v1.agent INFO   [Stream] Task started: 获取第五章信息
16:50:13 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
16:50:13 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第5章: 一饭之恩，乱世人心
16:50:13 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务1完成
16:50:13 app.api.v1.agent INFO   [Stream] 任务完成: 获取第五章信息 (0.1s)
16:50:13 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共1个任务，耗时: 0.08s
16:50:13 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
16:50:13 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=0, 输出型=0, 展示型=1
16:50:13 app.services.agent.langgraph_agent INFO   [Response] 纯展示型任务(1个)，直接格式化返回（跳过AI整合，节省成本）
16:50:13 app.api.v1.agent INFO   [Stream] 跳过最终响应（内容已流式发送）
16:50:13 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed
16:51:16 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
16:51:16 app.services.ai.http_ai_service INFO   ModelSelector 已启用
16:51:16 app.services.ai.http_ai_service INFO   AILogService 已启用 (用于成本追踪)
16:51:17 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
16:51:17 app.api.v1.agent INFO   [Chat Stream] Mode: planning
16:51:17 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:64746 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
16:51:17 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: planning, Message: 分析前面五章内容，来写出后续6到10章的大纲...
16:51:17 app.services.agent.langgraph_agent INFO   [Planning] 使用隔离的thread_id: 9398f47b-1e74-4e1c-93dd-e837e51dbaaf:b33918f6-e912-42b5-9541-88ecdd1ef0ce (work_id=9398f47b-1e74-4e1c-93dd-e837e51dbaaf, conversation_id=b33918f6-e912-42b5-9541-88ecdd1ef0ce)
16:51:17 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: 分析前面五章内容，来写出后续6到10章的大纲...
16:51:17 app.core.cache INFO   ✅ 缓存命中: prompt:get_planning_static_prompt:fca6eb91156619d0
16:51:17 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
16:51:17 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
16:51:17 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=1200, temp=0.3, task_type=TaskType.SIMPLE_QA
16:51:20 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
16:51:23 app.services.ai.http_ai_service INFO   API 响应完成，共接收 11 个数据块，总长度: 1570
16:51:23 app.services.ai.http_ai_service INFO   流式响应Token统计: 4022 (prompt=3313, completion=709)
16:51:23 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
16:51:23 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4022, cost=$0.011231, time=5872ms
16:51:23 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=4022
16:51:23 app.services.agent.langgraph_agent INFO   [JSON解析] 方法2成功: 从```json块提取
16:51:23 app.services.agent.langgraph_agent INFO   [Planning] 思维链: 输出=用户期望看到一个结构化的规划，即后续第6到10章的大纲，包含, 原料=需要获取前五章（第1章至第5章）的全部内, 处理=需要使用 `get_chapter_by
16:51:23 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共6个任务，耗时: 5.92s
16:51:23 app.api.v1.agent INFO   [Stream] Plan tasks: 6 items
16:51:23 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
16:51:23 app.services.agent.parameter_resolver INFO   [ParameterResolver] 初始化完成, 严格模式: False
16:51:23 app.services.agent.langgraph_agent INFO   [ParameterResolver] 参数解析器已启用
16:51:23 app.services.agent.langgraph_agent INFO   [ParallelExecution] 任务分组: 并行=5, 串行=1
16:51:23 app.services.agent.langgraph_agent INFO   [ParallelExecution] 开始并行执行5个任务
16:51:23 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务1开始: 获取第一章内容
16:51:23 app.api.v1.agent INFO   [Stream] Task started: 获取第一章内容
16:51:23 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
16:51:23 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务2开始: 获取第二章内容
16:51:23 app.api.v1.agent INFO   [Stream] Task started: 获取第二章内容
16:51:23 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
16:51:23 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务3开始: 获取第三章内容
16:51:23 app.api.v1.agent INFO   [Stream] Task started: 获取第三章内容
16:51:23 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
16:51:23 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务4开始: 获取第四章内容
16:51:23 app.api.v1.agent INFO   [Stream] Task started: 获取第四章内容
16:51:23 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
16:51:23 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务5开始: 获取第五章内容
16:51:23 app.api.v1.agent INFO   [Stream] Task started: 获取第五章内容
16:51:23 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
16:51:23 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第4章: 荒村孤烟，道祖传心
16:51:23 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第5章: 一饭之恩，乱世人心
16:51:23 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 百年关，天机变
16:51:23 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第2章: 道祖出关，太极震群魔
16:51:23 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第3章: 下山
16:51:23 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务4完成
16:51:23 app.api.v1.agent INFO   [Stream] 任务完成: 获取第四章内容 (0.1s)
16:51:23 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务5完成
16:51:23 app.api.v1.agent INFO   [Stream] 任务完成: 获取第五章内容 (0.1s)
16:51:23 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务1完成
16:51:23 app.api.v1.agent INFO   [Stream] 任务完成: 获取第一章内容 (0.1s)
16:51:23 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务2完成
16:51:23 app.api.v1.agent INFO   [Stream] 任务完成: 获取第二章内容 (0.1s)
16:51:23 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务3完成
16:51:23 app.api.v1.agent INFO   [Stream] 任务完成: 获取第三章内容 (0.1s)
16:51:23 app.services.agent.langgraph_agent INFO   [ParallelExecution] 开始串行执行1个任务
16:51:23 app.services.agent.langgraph_agent INFO   [ParallelExecution] 串行任务6开始: 分析前五章内容，规划第6-10章大纲
16:51:23 app.api.v1.agent INFO   [Stream] Task started: 分析前五章内容，规划第6-10章大纲
16:51:23 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
16:51:23 app.prompts.constraint_manager INFO   ✅ 已加载模板: analyze_text (v3.1.0)
16:51:23 app.prompts.constraint_manager INFO   ✅ 已加载模板: creative_writing (v1.0.0)
16:51:23 app.prompts.constraint_manager INFO   ✅ 已加载模板: intent_classifier (v2.0.0)
16:51:24 app.prompts.constraint_manager INFO   ✅ 已加载模板: planning_agent (v2.0.0)
16:51:24 app.prompts.constraint_manager INFO   ✅ 已加载模板: query_agent (v2.0.0)
16:51:24 app.prompts.constraint_manager INFO   ✅ 已加载模板: system_agent (v2.0.0)
16:51:24 app.prompts.constraint_manager INFO   ✅ 已加载模板: tool_agent (v2.0.0)
16:51:24 app.prompts.constraint_manager INFO   ✅ 已加载模板: writing_agent (v2.0.0)
16:51:24 app.prompts.constraint_manager INFO   ✅ 约束提示词管理器已初始化: 加载8个模板, 注册0个验证器
16:51:24 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
16:51:24 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
16:51:24 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
16:51:25 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
16:52:07 app.services.ai.http_ai_service INFO   API 响应完成，共接收 103 个数据块，总长度: 6775
16:52:07 app.services.ai.http_ai_service INFO   流式响应Token统计: 19720 (prompt=14664, completion=5056)
16:52:08 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
16:52:08 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=19720, cost=$0.068890, time=43903ms
16:52:08 app.services.agent.langgraph_agent INFO   ✅ [Agent分析] 分析完成，结果长度: 6775
16:52:08 app.services.agent.langgraph_agent INFO   [ParallelExecution] 串行任务6完成
16:52:08 app.api.v1.agent INFO   [Stream] 任务完成: 分析前五章内容，规划第6-10章大纲 (44.1s)
16:52:08 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共6个任务，耗时: 44.19s
16:52:08 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
16:52:08 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=0, 输出型=1, 展示型=5
16:52:08 app.services.agent.langgraph_agent INFO   [Response] 单个分析任务(analyze_text_tool)，使用AI格式化
16:52:08 app.services.agent.langgraph_agent INFO   [Summarization] 使用AI整合任务结果
16:52:08 app.services.agent.langgraph_agent INFO   [Summarization] 上下文压缩: 原始=21652字符, 压缩后=4126字符, 压缩率=81%
16:52:08 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
16:52:08 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
16:52:08 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
16:52:10 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
16:52:12 app.services.ai.http_ai_service INFO   API 响应完成，共接收 3 个数据块，总长度: 217
16:52:12 app.services.ai.http_ai_service INFO   流式响应Token统计: 4261 (prompt=4119, completion=142)
16:52:12 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
16:52:12 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4261, cost=$0.006569, time=4633ms
16:52:12 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=4261
16:52:12 app.api.v1.agent INFO   [Stream] 跳过最终响应（内容已流式发送）
16:52:12 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed
16:53:12 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
16:53:12 app.services.ai.http_ai_service INFO   ModelSelector 已启用
16:53:12 app.services.ai.http_ai_service INFO   AILogService 已启用 (用于成本追踪)
16:53:14 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
16:53:14 app.api.v1.agent INFO   [Chat Stream] Mode: planning
16:53:14 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:61671 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
16:53:14 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: planning, Message: 1到5章分别讲了什么？...
16:53:14 app.services.agent.langgraph_agent INFO   [Planning] 使用隔离的thread_id: 9398f47b-1e74-4e1c-93dd-e837e51dbaaf:b33918f6-e912-42b5-9541-88ecdd1ef0ce (work_id=9398f47b-1e74-4e1c-93dd-e837e51dbaaf, conversation_id=b33918f6-e912-42b5-9541-88ecdd1ef0ce)
16:53:14 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: 1到5章分别讲了什么？...
16:53:14 app.core.cache INFO   ✅ 缓存命中: prompt:get_planning_static_prompt:fca6eb91156619d0
16:53:14 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
16:53:14 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
16:53:14 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=1200, temp=0.3, task_type=TaskType.SIMPLE_QA
16:53:17 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
16:53:21 app.services.ai.http_ai_service INFO   API 响应完成，共接收 18 个数据块，总长度: 2118
16:53:21 app.services.ai.http_ai_service INFO   流式响应Token统计: 4542 (prompt=3688, completion=854)
16:53:21 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
16:53:21 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4542, cost=$0.013150, time=6770ms
16:53:21 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=4542
16:53:21 app.services.agent.langgraph_agent INFO   [JSON解析] 方法2成功: 从```json块提取
16:53:21 app.services.agent.langgraph_agent INFO   [Planning] 思维链: 输出=用户期望看到对1到5章内容的概括性总结，了解每一章分别讲了什, 原料=需要获取第1、2、3、4、5章的原文内容, 处理=分别获取这五章的内容，然后对每一章的内容
16:53:21 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共10个任务，耗时: 6.81s
16:53:21 app.api.v1.agent INFO   [Stream] Plan tasks: 10 items
16:53:21 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
16:53:21 app.services.agent.parameter_resolver INFO   [ParameterResolver] 初始化完成, 严格模式: False
16:53:21 app.services.agent.langgraph_agent INFO   [ParameterResolver] 参数解析器已启用
16:53:21 app.services.agent.langgraph_agent INFO   [ParallelExecution] 任务分组: 并行=5, 串行=5
16:53:21 app.services.agent.langgraph_agent INFO   [ParallelExecution] 开始并行执行5个任务
16:53:21 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务1开始: 获取第一章内容
16:53:21 app.api.v1.agent INFO   [Stream] Task started: 获取第一章内容
16:53:21 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
16:53:21 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务3开始: 获取第二章内容
16:53:21 app.api.v1.agent INFO   [Stream] Task started: 获取第二章内容
16:53:21 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
16:53:21 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务5开始: 获取第三章内容
16:53:21 app.api.v1.agent INFO   [Stream] Task started: 获取第三章内容
16:53:21 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
16:53:21 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务7开始: 获取第四章内容
16:53:21 app.api.v1.agent INFO   [Stream] Task started: 获取第四章内容
16:53:21 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
16:53:21 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务9开始: 获取第五章内容
16:53:21 app.api.v1.agent INFO   [Stream] Task started: 获取第五章内容
16:53:21 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
16:53:21 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第2章: 道祖出关，太极震群魔
16:53:21 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第3章: 下山
16:53:21 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第5章: 一饭之恩，乱世人心
16:53:21 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 百年关，天机变
16:53:21 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第4章: 荒村孤烟，道祖传心
16:53:21 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务3完成
16:53:21 app.api.v1.agent INFO   [Stream] 任务完成: 获取第二章内容 (0.1s)
16:53:21 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务5完成
16:53:21 app.api.v1.agent INFO   [Stream] 任务完成: 获取第三章内容 (0.1s)
16:53:21 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务9完成
16:53:21 app.api.v1.agent INFO   [Stream] 任务完成: 获取第五章内容 (0.1s)
16:53:21 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务1完成
16:53:21 app.api.v1.agent INFO   [Stream] 任务完成: 获取第一章内容 (0.1s)
16:53:21 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务7完成
16:53:21 app.api.v1.agent INFO   [Stream] 任务完成: 获取第四章内容 (0.1s)
16:53:21 app.services.agent.langgraph_agent INFO   [ParallelExecution] 开始串行执行5个任务
16:53:21 app.services.agent.langgraph_agent INFO   [ParallelExecution] 串行任务2开始: 概括第一章内容
16:53:21 app.api.v1.agent INFO   [Stream] Task started: 概括第一章内容
16:53:21 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
16:53:21 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
16:53:21 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
16:53:21 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
16:53:23 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
16:53:36 app.services.ai.http_ai_service INFO   API 响应完成，共接收 34 个数据块，总长度: 2104
16:53:36 app.services.ai.http_ai_service INFO   流式响应Token统计: 4848 (prompt=3211, completion=1637)
16:53:36 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
16:53:36 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4848, cost=$0.020384, time=14637ms
16:53:36 app.services.agent.langgraph_agent INFO   ✅ [Agent分析] 分析完成，结果长度: 2104
16:53:36 app.services.agent.langgraph_agent INFO   [ParallelExecution] 串行任务2完成
16:53:36 app.api.v1.agent INFO   [Stream] 任务完成: 概括第一章内容 (14.7s)
16:53:36 app.services.agent.langgraph_agent INFO   [ParallelExecution] 串行任务4开始: 概括第二章内容
16:53:36 app.api.v1.agent INFO   [Stream] Task started: 概括第二章内容
16:53:36 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
16:53:36 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
16:53:36 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
16:53:36 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
16:53:38 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
16:53:55 app.services.ai.http_ai_service INFO   API 响应完成，共接收 29 个数据块，总长度: 2437
16:53:55 app.services.ai.http_ai_service INFO   流式响应Token统计: 6768 (prompt=4904, completion=1864)
16:53:55 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
16:53:55 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=6768, cost=$0.024770, time=19311ms
16:53:55 app.services.agent.langgraph_agent INFO   ✅ [Agent分析] 分析完成，结果长度: 2437
16:53:55 app.services.agent.langgraph_agent INFO   [ParallelExecution] 串行任务4完成
16:53:55 app.api.v1.agent INFO   [Stream] 任务完成: 概括第二章内容 (19.3s)
16:53:55 app.services.agent.langgraph_agent INFO   [ParallelExecution] 串行任务6开始: 概括第三章内容
16:53:55 app.api.v1.agent INFO   [Stream] Task started: 概括第三章内容
16:53:55 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
16:53:55 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
16:53:55 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
16:53:55 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
16:53:57 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
16:54:18 app.services.ai.http_ai_service INFO   API 响应完成，共接收 42 个数据块，总长度: 2655
16:54:18 app.services.ai.http_ai_service INFO   流式响应Token统计: 6978 (prompt=4938, completion=2040)
16:54:18 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
16:54:18 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=6978, cost=$0.026572, time=22180ms
16:54:18 app.services.agent.langgraph_agent INFO   ✅ [Agent分析] 分析完成，结果长度: 2655
16:54:18 app.services.agent.langgraph_agent INFO   [ParallelExecution] 串行任务6完成
16:54:18 app.api.v1.agent INFO   [Stream] 任务完成: 概括第三章内容 (22.2s)
16:54:18 app.services.agent.langgraph_agent INFO   [ParallelExecution] 串行任务8开始: 概括第四章内容
16:54:18 app.api.v1.agent INFO   [Stream] Task started: 概括第四章内容
16:54:18 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
16:54:18 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
16:54:18 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
16:54:18 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
16:54:20 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
16:54:37 app.services.ai.http_ai_service INFO   API 响应完成，共接收 28 个数据块，总长度: 2415
16:54:37 app.services.ai.http_ai_service INFO   流式响应Token统计: 6550 (prompt=4769, completion=1781)
16:54:37 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
16:54:37 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=6550, cost=$0.023771, time=19213ms
16:54:37 app.services.agent.langgraph_agent INFO   ✅ [Agent分析] 分析完成，结果长度: 2415
16:54:37 app.services.agent.langgraph_agent INFO   [ParallelExecution] 串行任务8完成
16:54:37 app.api.v1.agent INFO   [Stream] 任务完成: 概括第四章内容 (19.3s)
16:54:37 app.services.agent.langgraph_agent INFO   [ParallelExecution] 串行任务10开始: 概括第五章内容
16:54:37 app.api.v1.agent INFO   [Stream] Task started: 概括第五章内容
16:54:37 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
16:54:37 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
16:54:37 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
16:54:37 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
16:54:38 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
16:54:53 app.services.ai.http_ai_service INFO   API 响应完成，共接收 31 个数据块，总长度: 2085
16:54:53 app.services.ai.http_ai_service INFO   流式响应Token统计: 5280 (prompt=3782, completion=1498)
16:54:53 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
16:54:53 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=5280, cost=$0.019707, time=16279ms
16:54:53 app.services.agent.langgraph_agent INFO   ✅ [Agent分析] 分析完成，结果长度: 2085
16:54:53 app.services.agent.langgraph_agent INFO   [ParallelExecution] 串行任务10完成
16:54:53 app.api.v1.agent INFO   [Stream] 任务完成: 概括第五章内容 (16.3s)
16:54:53 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共10个任务，耗时: 91.89s
16:54:53 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
16:54:53 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=0, 输出型=5, 展示型=5
16:54:53 app.services.agent.langgraph_agent INFO   [Response] 5个输出任务，简单拼接
16:54:53 app.api.v1.agent INFO   [Stream] 跳过最终响应（内容已流式发送）
16:54:53 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed
16:55:55 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
16:55:55 app.services.ai.http_ai_service INFO   ModelSelector 已启用
16:55:55 app.services.ai.http_ai_service INFO   AILogService 已启用 (用于成本追踪)
16:55:58 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
16:55:58 app.api.v1.agent INFO   [Chat Stream] Mode: planning
16:55:58 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:50284 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
16:55:58 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: planning, Message: 分析前面五章内容，来写出后续6到10章的大纲...
16:55:58 app.services.agent.langgraph_agent INFO   [Planning] 使用隔离的thread_id: 9398f47b-1e74-4e1c-93dd-e837e51dbaaf:b33918f6-e912-42b5-9541-88ecdd1ef0ce (work_id=9398f47b-1e74-4e1c-93dd-e837e51dbaaf, conversation_id=b33918f6-e912-42b5-9541-88ecdd1ef0ce)
16:55:58 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: 分析前面五章内容，来写出后续6到10章的大纲...
16:55:58 app.core.cache INFO   ✅ 缓存命中: prompt:get_planning_static_prompt:fca6eb91156619d0
16:55:58 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
16:55:58 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
16:55:58 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=1200, temp=0.3, task_type=TaskType.SIMPLE_QA
16:56:01 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
16:56:04 app.services.ai.http_ai_service INFO   API 响应完成，共接收 12 个数据块，总长度: 1577
16:56:04 app.services.ai.http_ai_service INFO   流式响应Token统计: 4296 (prompt=3583, completion=713)
16:56:04 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
16:56:04 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4296, cost=$0.011609, time=6138ms
16:56:04 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=4296
16:56:04 app.services.agent.langgraph_agent INFO   [JSON解析] 方法2成功: 从```json块提取
16:56:04 app.services.agent.langgraph_agent INFO   [Planning] 思维链: 输出=用户期望看到一个后续章节（6-10章）的大纲，该大纲需要基于, 原料=需要获取前五章（1-5章）的内容作为分析, 处理=需要先按顺序获取第1至第5章的内容，然后
16:56:04 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共6个任务，耗时: 6.18s
16:56:04 app.api.v1.agent INFO   [Stream] Plan tasks: 6 items
16:56:04 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
16:56:04 app.services.agent.parameter_resolver INFO   [ParameterResolver] 初始化完成, 严格模式: False
16:56:04 app.services.agent.langgraph_agent INFO   [ParameterResolver] 参数解析器已启用
16:56:04 app.services.agent.langgraph_agent INFO   [ParallelExecution] 任务分组: 并行=5, 串行=1
16:56:04 app.services.agent.langgraph_agent INFO   [ParallelExecution] 开始并行执行5个任务
16:56:04 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务1开始: 获取第一章内容
16:56:04 app.api.v1.agent INFO   [Stream] Task started: 获取第一章内容
16:56:04 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
16:56:04 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务2开始: 获取第二章内容
16:56:04 app.api.v1.agent INFO   [Stream] Task started: 获取第二章内容
16:56:04 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
16:56:04 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务3开始: 获取第三章内容
16:56:04 app.api.v1.agent INFO   [Stream] Task started: 获取第三章内容
16:56:04 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
16:56:04 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务4开始: 获取第四章内容
16:56:04 app.api.v1.agent INFO   [Stream] Task started: 获取第四章内容
16:56:04 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
16:56:04 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务5开始: 获取第五章内容
16:56:04 app.api.v1.agent INFO   [Stream] Task started: 获取第五章内容
16:56:04 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
16:56:04 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第3章: 下山
16:56:04 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第2章: 道祖出关，太极震群魔
16:56:05 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第4章: 荒村孤烟，道祖传心
16:56:05 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第5章: 一饭之恩，乱世人心
16:56:05 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务3完成
16:56:05 app.api.v1.agent INFO   [Stream] 任务完成: 获取第三章内容 (0.0s)
16:56:05 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务2完成
16:56:05 app.api.v1.agent INFO   [Stream] 任务完成: 获取第二章内容 (0.0s)
16:56:05 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务4完成
16:56:05 app.api.v1.agent INFO   [Stream] 任务完成: 获取第四章内容 (0.0s)
16:56:05 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务5完成
16:56:05 app.api.v1.agent INFO   [Stream] 任务完成: 获取第五章内容 (0.0s)
16:56:05 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 百年关，天机变
16:56:05 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务1完成
16:56:05 app.api.v1.agent INFO   [Stream] 任务完成: 获取第一章内容 (0.0s)
16:56:05 app.services.agent.langgraph_agent INFO   [ParallelExecution] 开始串行执行1个任务
16:56:05 app.services.agent.langgraph_agent INFO   [ParallelExecution] 串行任务6开始: 分析前五章内容并规划第6-10章大纲
16:56:05 app.api.v1.agent INFO   [Stream] Task started: 分析前五章内容并规划第6-10章大纲
16:56:05 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
16:56:05 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
16:56:05 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
16:56:05 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
16:56:07 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
16:56:48 app.services.ai.http_ai_service INFO   API 响应完成，共接收 76 个数据块，总长度: 6664
16:56:48 app.services.ai.http_ai_service INFO   流式响应Token统计: 19688 (prompt=14742, completion=4946)
16:56:48 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
16:56:48 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=19688, cost=$0.067887, time=43044ms
16:56:48 app.services.agent.langgraph_agent INFO   ✅ [Agent分析] 分析完成，结果长度: 6664
16:56:48 app.services.agent.langgraph_agent INFO   [ParallelExecution] 串行任务6完成
16:56:48 app.api.v1.agent INFO   [Stream] 任务完成: 分析前五章内容并规划第6-10章大纲 (43.1s)
16:56:48 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共6个任务，耗时: 43.13s
16:56:48 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
16:56:48 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=0, 输出型=1, 展示型=5
16:56:48 app.services.agent.langgraph_agent INFO   [Response] 单个分析任务(analyze_text_tool)，使用AI格式化
16:56:48 app.services.agent.langgraph_agent INFO   [Summarization] 使用AI整合任务结果
16:56:48 app.services.agent.langgraph_agent INFO   [Summarization] 上下文压缩: 原始=21541字符, 压缩后=4126字符, 压缩率=81%
16:56:48 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
16:56:48 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
16:56:48 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
16:56:50 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
16:57:06 app.services.ai.http_ai_service INFO   API 响应完成，共接收 17 个数据块，总长度: 1110
16:57:06 app.services.ai.http_ai_service INFO   流式响应Token统计: 6922 (prompt=6101, completion=821)
16:57:06 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
16:57:06 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=6922, cost=$0.015836, time=18511ms
16:57:06 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=6922
16:57:06 app.api.v1.agent INFO   [Stream] 跳过最终响应（内容已流式发送）
16:57:06 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed