INFO:     127.0.0.1:61866 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
INFO:     127.0.0.1:60478 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
INFO:     127.0.0.1:60490 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
INFO:     127.0.0.1:63386 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-10 16:05:46,818 - monitoring - INFO - Registered health check: cpu_usage
2026-01-10 16:05:46,818 - monitoring - INFO - Registered health check: memory_usage
2026-01-10 16:05:46,818 - monitoring - INFO - Registered health check: disk_usage
2026-01-10 16:05:46,819 - monitoring - INFO - Registered health check: process_status
2026-01-10 16:05:46,819 - monitoring - INFO - Added alert rule: high_cpu_usage
2026-01-10 16:05:46,819 - monitoring - INFO - Added alert rule: high_memory_usage
2026-01-10 16:05:46,820 - monitoring - INFO - Added alert rule: low_disk_space
2026-01-10 16:05:47,051 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:61605 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2026-01-10 16:05:52,208 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:61648 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2026-01-10 16:05:52,227 - app.services.ai.prompts - INFO - Prompts loaded successfully from D:\Java\ai_writer\backend\app\services\ai\prompts\default.json
2026-01-10 16:05:52,228 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-10 16:05:52,228 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-10 16:05:52,230 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2026-01-10 16:05:53,588 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-10 16:05:53,589 - app.api.v1.agent - INFO - [Chat Stream] Mode: planning
2026-01-10 16:05:53,593 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:60626 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2026-01-10 16:05:53,605 - app.core.redis - INFO - ✅ Redis connected: redis://localhost:6379/0
2026-01-10 16:05:53,608 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 把第三段改得更有画面感，增加环境描写...
2026-01-10 16:05:53,609 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-10 16:05:53,609 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-10 16:05:53,610 - app.services.ai.http_ai_service - INFO - [成本追踪] 初始化未传db/user_id，将使用请求上下文按需记录成本
2026-01-10 16:05:54,976 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-10 16:05:54,978 - app.services.agent.tools.writing_tools - INFO - Writing tools AI service initialized
2026-01-10 16:05:54,979 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ AI Service 已同时设置到 langgraph_tools 和 writing_tools
2026-01-10 16:05:54,979 - app.services.context.adaptive_budget - INFO - ✅ 所有预算配置验证通过
2026-01-10 16:06:00,949 - app.services.context.vector_memory_store - INFO - ✅ VectorMemoryStore初始化成功 | 目录=./data/chroma_db | 模型=paraphrase-multilingual-MiniLM-L12-v2 | 集合=user_memories
2026-01-10 16:06:00,949 - app.services.context.manager - INFO - ✅ VectorMemoryStore 已初始化
2026-01-10 16:06:00,949 - app.services.context.manager - INFO - ✅ ContextManager: 长期记忆已启用 (user_id=None)
2026-01-10 16:06:00,949 - app.services.context.manager - INFO - ✅ ContextManager: 自适应预算已启用
2026-01-10 16:06:00,949 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ ContextManager已初始化（长期记忆已启用，自适应预算已启用，总预算=16000 tokens）
成功加载模板: analyze_text (版本 3.1.0)
成功加载模板: writing_agent (版本 2.0.0)
成功加载模板: system_agent_prompt (版本 2.1.0)
成功加载模板: creative_writing_prompt (版本 1.0.0)
2026-01-10 16:06:00,963 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ PromptManager已初始化
2026-01-10 16:06:00,971 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ Redis连接验证成功
2026-01-10 16:06:00,973 - app.services.agent.langgraph_agent - INFO - [LangGraph] OK 使用 AsyncRedisSaver（redis://localhost:6379/0，TTL=7天）
2026-01-10 16:06:00,973 - app.services.agent.memory.metrics - INFO - [MemoryMetrics] 监控系统已初始化
2026-01-10 16:06:00,973 - app.services.agent.memory.long_term_store - INFO - [LongTermStore] Initialized: base_dir=./data/long_term_memory, max_size=50KB, compression=True
2026-01-10 16:06:00,974 - app.services.agent.memory.enhanced_memory_manager - INFO - EnhancedMemoryManager initialized: short=10, medium=100, threshold=0.1, long_term_backup=enabled
2026-01-10 16:06:00,974 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ EnhancedMemoryManager已创建
2026-01-10 16:06:00,974 - app.services.agent.memory.unified_coordinator - INFO - [UnifiedMemoryCoordinator] 初始化统一记忆协调器
2026-01-10 16:06:00,974 - app.services.agent.memory.unified_coordinator - INFO - [UnifiedMemoryCoordinator] 全局实例已设置
2026-01-10 16:06:00,974 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ UnifiedMemoryCoordinator已初始化 | checkpointer=AsyncRedisSaver | enhanced_memory=yes | context_manager=yes
2026-01-10 16:06:00,974 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ 解耦模块已初始化 (IntentClassifier, ToolExecutor, EventParser, ResponseBuilder, ToolDispatcher, ParallelExecutor, PlanGenerator, QuickPathHandler, StreamEventHandler, SecondaryToolHandler, TaskRunner, AgentExecutor)
2026-01-10 16:06:00,979 - app.services.agent.parallel_tool_node - INFO - [ParallelToolNode] 初始化完成，最大并发数=5，并行安全工具=4个
2026-01-10 16:06:00,984 - app.api.v1.agent - INFO - [Global Agent] created global agent instance; MemorySaver shared across requests
INFO:     127.0.0.1:60793 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-10 16:06:01,002 - app.api.v1.agent - INFO - [agent_chat_stream] 📚 世界观数据已注入: 人物=11, 地点=6, 设定=6, 规范=无
2026-01-10 16:06:01,002 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:08f6ddac-3648-4815-9dd8-55ad345b5419:84d6430f-0692-4bea-816d-0204ff421018 (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=08f6ddac-3648-4815-9dd8-55ad345b5419, conversation_id=84d6430f-0692-4bea-816d-0204ff421018)
2026-01-10 16:06:01,002 - app.services.context.monitoring_integration - INFO - ✅ ContextManager监控收集器已初始化
2026-01-10 16:06:01,002 - app.services.context.store - INFO - [ContextStore] Redis连接成功
2026-01-10 16:06:01,017 - app.services.context.manager - INFO - [ContextManager] 创建新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:08f6ddac-3648-4815-9dd8-55ad345b5419:84d6430f-0692-4bea-816d-0204ff421018
2026-01-10 16:06:01,128 - app.services.context.token_counter - INFO - ✅ tiktoken初始化成功，模型: gemini-2.5-pro -> cl100k_base
2026-01-10 16:06:01,128 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:08f6ddac-3648-4815-9dd8-55ad345b5419:84d6430f-0692-4bea-816d-0204ff421018: 0/16000 tokens
2026-01-10 16:06:03,072 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='把第三段改得更有画面感，增加环境描写...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:08f6ddac-3648-4815-9dd8-55ad345b5419', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=3条
2026-01-10 16:06:03,074 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=08f6ddac-3648-4815-9dd8-55ad345b5419 | 含用户级=True | 找到=3条
2026-01-10 16:06:03,075 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 1条消息, 0 tokens, 耗时 2073.16ms
2026-01-10 16:06:03,076 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 1 条历史消息 (token: 0)
2026-01-10 16:06:03,084 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-10 16:06:03,087 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-10 16:06:03,088 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=20, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-10 16:06:05,240 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-10 16:06:05,242 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-10 16:06:05,303 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-10 16:06:05,307 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=291, cost=$0.000029, time=2155ms
2026-01-10 16:06:05,308 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=7, 尝试次数=1
2026-01-10 16:06:05,309 - app.services.agent.intent.classifier - INFO - [Intent] AI识别结果: writing
2026-01-10 16:06:05,309 - app.services.agent.langgraph_agent - INFO - [Planning] AI意图分类: writing (置信度: 0.90)
2026-01-10 16:06:05,312 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 把第三段改得更有画面感，增加环境描写...
2026-01-10 16:06:05,325 - app.core.cache - INFO - ✅ 缓存命中: prompt:planning:v2.39.0:get_planning_static_prompt:fca6eb91156619d0
2026-01-10 16:06:05,334 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-10 16:06:05,335 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=story_planning, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: story_planning; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-01-10 16:06:05,337 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.3, task_type=TaskType.STORY_PLANNING
INFO:     127.0.0.1:50374 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-10 16:06:16,724 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-10 16:06:21,223 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 10 个数据块，总长度: 1442
2026-01-10 16:06:21,224 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 19285 (prompt=18628, completion=657)
2026-01-10 16:06:21,225 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-10 16:06:21,226 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-10 16:06:21,253 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-10 16:06:21,257 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=19285, cost=$0.029855, time=15888ms
2026-01-10 16:06:21,259 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=19285
2026-01-10 16:06:21,261 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户想要改写当前章节的第三段，期望得到一个更有画面感、包含更, 原料=需要先定位到当前章节的“第三段”的具体内, 处理=这是一个典型的“定位-改写-应用”流程。
2026-01-10 16:06:21,271 - app.services.agent.planning.plan_generator - INFO - [PlanValidator] 检测到人物查询'增加环境'但未指定章节，自动插入搜索任务
2026-01-10 16:06:21,274 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共4个任务
2026-01-10 16:06:21,274 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共4个任务，耗时: 15.96s
2026-01-10 16:06:21,276 - app.api.v1.agent - INFO - [Stream] Plan tasks: 4 items
2026-01-10 16:06:21,277 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2026-01-10 16:06:21,283 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2026-01-10 16:06:21,284 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2026-01-10 16:06:21,286 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 任务分组: 第一层并行=1, 第二层并行=0, 串行=3
2026-01-10 16:06:21,287 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始第一层并行执行1个任务
2026-01-10 16:06:21,289 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务1开始: 搜索'增加环境'出现位置
2026-01-10 16:06:21,290 - app.api.v1.agent - INFO - [Stream] Task started: 搜索'增加环境'出现位置 (icon=Search)
2026-01-10 16:06:21,291 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(search_analysis_fragments)
2026-01-10 16:06:21,292 - app.services.agent.tools.tool_types - INFO - [search_analysis_fragments] 开始执行工具
2026-01-10 16:06:22,942 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=08f6ddac-3648-4815-9dd8-55ad345b5419, current_order=1, query=增加环境...
2026-01-10 16:06:23,114 - app.services.chapter_vector_service - INFO - RAG retrieved 0 segments within order<=3
Building prefix dict from the default dictionary ...
2026-01-10 16:06:23,114 - jieba - DEBUG - Building prefix dict from the default dictionary ...
Loading model from cache D:\Temp\jieba.cache
2026-01-10 16:06:23,114 - jieba - DEBUG - Loading model from cache D:\Temp\jieba.cache
Loading model cost 0.723 seconds.
2026-01-10 16:06:23,837 - jieba - DEBUG - Loading model cost 0.723 seconds.
Prefix dict has been built successfully.
2026-01-10 16:06:23,837 - jieba - DEBUG - Prefix dict has been built successfully.
2026-01-10 16:06:23,847 - app.services.agent.tools.tool_types - INFO - [search_analysis_fragments] 执行成功 (耗时: 2.555s)
2026-01-10 16:06:23,848 - app.services.agent.tools.tool_monitor - INFO - ToolMonitor initialized with Memory storage, retention: 7 days
2026-01-10 16:06:23,849 - app.services.agent.execution.task_runner - INFO - [TaskRunner] search_analysis_fragments 执行成功（DeepAgent模式）
2026-01-10 16:06:23,850 - app.api.v1.agent - INFO - [Stream] 任务完成: 搜索'增加环境'出现位置 (2.6s)
2026-01-10 16:06:23,850 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务1完成
2026-01-10 16:06:23,850 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始串行执行3个任务
2026-01-10 16:06:23,851 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务2开始: 在当前章节中定位第三段的位置和内容
2026-01-10 16:06:23,851 - app.api.v1.agent - INFO - [Stream] Task started: 在当前章节中定位第三段的位置和内容 (icon=Wrench)
2026-01-10 16:06:23,851 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: locate_content
2026-01-10 16:06:23,852 - app.services.agent.tools.locate_tools - INFO - [locate_content] 开始定位: chapter_id=625092a5-7b4c-4d92-a617-0f3a9079d731, query=第三段
2026-01-10 16:06:23,858 - app.services.agent.tools.locate_tools - INFO - [locate_content] 章节共 88 个段落
2026-01-10 16:06:23,858 - app.services.agent.tools.locate_tools - INFO - [locate_content] 段落定位成功: 第3段
2026-01-10 16:06:23,859 - app.services.agent.execution.tool_executor - INFO - [StandardTool] locate_content 执行成功
2026-01-10 16:06:23,860 - app.api.v1.agent - INFO - [Stream] 任务完成: 在当前章节中定位第三段的位置和内容 (0.0s)
2026-01-10 16:06:23,860 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务2完成
2026-01-10 16:06:23,861 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务3开始: 根据用户要求，将原文改写得更有画面感，并增加环境描写
2026-01-10 16:06:23,861 - app.api.v1.agent - INFO - [Stream] Task started: 根据用户要求，将原文改写得更有画面感，并增加环境描写 (icon=Edit3)
2026-01-10 16:06:23,861 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: smart_rewrite
2026-01-10 16:06:23,862 - app.services.agent.tools.tool_types - INFO - [smart_rewrite] 开始执行工具
2026-01-10 16:06:23,868 - app.services.agent.tools.editor_tools - INFO - [smart_rewrite] 开始生成改写版本，原文长度: 16, 用户要求: 把这段改得更有画面感，增加环境描写, 基准版本: 无
2026-01-10 16:06:23,870 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-10 16:06:23,870 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-10 16:06:23,870 - app.services.ai.http_ai_service - INFO - [成本追踪] 初始化未传db/user_id，将使用请求上下文按需记录成本
2026-01-10 16:06:24,701 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-10 16:06:24,702 - app.services.agent.tools.editor_tools - INFO - [smart_rewrite] 使用传统单Prompt架构
2026-01-10 16:06:24,702 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-10 16:06:24,703 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=content_creation, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro
2026-01-10 16:06:24,703 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=4000, temp=0.8, 尝试=1/3, task_type=TaskType.CONTENT_CREATION
INFO:     127.0.0.1:64705 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
INFO:     127.0.0.1:58188 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
INFO:     127.0.0.1:58209 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-10 16:06:52,687 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-10 16:06:52,687 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-10 16:06:52,704 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-10 16:06:52,704 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=3130, cost=$0.005662, time=27986ms
2026-01-10 16:06:52,704 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=347, 尝试次数=1
2026-01-10 16:06:52,704 - app.services.agent.tools.editor_tools - INFO - [smart_rewrite] AI返回长度: 347
2026-01-10 16:06:52,704 - app.services.agent.tools.editor_tools - INFO - [smart_rewrite] 成功生成3个改写版本
2026-01-10 16:06:52,704 - app.services.agent.tools.tool_types - INFO - [smart_rewrite] 执行成功 (耗时: 28.842s)
2026-01-10 16:06:52,713 - app.services.agent.execution.tool_executor - INFO - [StandardTool] smart_rewrite 执行成功
2026-01-10 16:06:52,713 - app.api.v1.agent - INFO - [Stream] 任务完成: 根据用户要求，将原文改写得更有画面感，并增加环境描写 (28.9s)
2026-01-10 16:06:52,713 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务3完成
2026-01-10 16:06:52,713 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务4开始: 将新生成的段落内容应用到编辑器，替换掉原来的第三段
2026-01-10 16:06:52,713 - app.api.v1.agent - INFO - [Stream] Task started: 将新生成的段落内容应用到编辑器，替换掉原来的第三段 (icon=Check)
2026-01-10 16:06:52,713 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: apply_chapter_edit
2026-01-10 16:06:52,713 - app.services.agent.tools.tool_types - INFO - [apply_chapter_edit] 开始执行工具
2026-01-10 16:06:52,718 - app.services.agent.tools.tool_types - INFO - [apply_chapter_edit] 执行成功 (耗时: 0.005s)
2026-01-10 16:06:52,718 - app.services.agent.execution.tool_executor - INFO - [StandardTool] apply_chapter_edit 执行成功
2026-01-10 16:06:52,727 - app.api.v1.agent - INFO - [Stream] 任务完成: 将新生成的段落内容应用到编辑器，替换掉原来的第三段 (0.0s)
2026-01-10 16:06:52,727 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务4完成
2026-01-10 16:06:52,728 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共4个任务，耗时: 31.45s
2026-01-10 16:06:52,728 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2026-01-10 16:06:52,728 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=1, 输出型=3, 展示型=0
2026-01-10 16:06:52,728 - app.services.agent.langgraph_agent - INFO - [Response] 3个输出任务（含续写），使用AI整合
2026-01-10 16:06:52,729 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2026-01-10 16:06:52,729 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=1, 输出型=3, 展示型=0
2026-01-10 16:06:52,729 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=1387字符, 处理后=1472字符
2026-01-10 16:06:52,730 - app.services.agent.planning.response_builder - INFO - [Summarization] 准备发送 summarization_start 事件
2026-01-10 16:06:52,730 - app.services.agent.stream.stream_event_handler - INFO - [StreamEventHandler] emit_summarization_start 被调用, _on_flow_event=True
2026-01-10 16:06:52,730 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_start 事件已发送
2026-01-10 16:06:52,730 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2026-01-10 16:06:52,731 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2026-01-10 16:06:52,734 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-10 16:06:52,735 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-10 16:06:52,735 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
2026-01-10 16:06:56,348 - app.services.chapter_word_stat_service - INFO - 记录字数增量: chapter_id=625092a5-7b4c-4d92-a617-0f3a9079d731, delta=36, edit_event_id=63aff447-17cb-421a-b4e8-2bfbc7451bc4
2026-01-10 16:06:56,349 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 625092a5-7b4c-4d92-a617-0f3a9079d731 内容更新，新段落数: 90
[TaskService] Checking daily writing task for user 79913e7e-d5cd-4e09-bce6-ca6639bd8456, word_count: 4555
[TaskService] Daily writing task result: None
2026-01-10 16:06:56,382 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:08f6ddac-3648-4815-9dd8-55ad345b5419
2026-01-10 16:06:56,383 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/625092a5-7b4c-4d92-a617-0f3a9079d731
INFO:     127.0.0.1:65210 - "PUT /api/v1/chapters/625092a5-7b4c-4d92-a617-0f3a9079d731 HTTP/1.1" 200 OK
2026-01-10 16:06:56,383 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-10 16:06:56,563 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (5 chunks)
2026-01-10 16:06:56,578 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:08f6ddac-3648-4815-9dd8-55ad345b5419
2026-01-10 16:06:56,580 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/625092a5-7b4c-4d92-a617-0f3a9079d731
INFO:     127.0.0.1:60263 - "PUT /api/v1/chapters/625092a5-7b4c-4d92-a617-0f3a9079d731 HTTP/1.1" 200 OK
2026-01-10 16:06:56,580 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-10 16:06:56,709 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (5 chunks)
INFO:     127.0.0.1:65364 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-10 16:06:59,508 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-10 16:06:59,508 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_complete 事件已发送（第一个chunk时）
2026-01-10 16:06:59,508 - app.services.agent.planning.response_builder - INFO - [Summarization] output_ready 事件已发送（第一个chunk时）
2026-01-10 16:07:01,193 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 7 个数据块，总长度: 615
2026-01-10 16:07:01,193 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 2698 (prompt=2293, completion=405)
2026-01-10 16:07:01,193 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-10 16:07:01,193 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-10 16:07:01,211 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-10 16:07:01,211 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2698, cost=$0.001700, time=8457ms
2026-01-10 16:07:01,211 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=615
2026-01-10 16:07:01,877 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:08f6ddac-3648-4815-9dd8-55ad345b5419 | 重要度=0.65
2026-01-10 16:07:02,472 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:08f6ddac-3648-4815-9dd8-55ad345b5419 | 重要度=0.77
2026-01-10 16:07:02,480 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:08f6ddac-3648-4815-9dd8-55ad345b5419:84d6430f-0692-4bea-816d-0204ff421018, token=585
2026-01-10 16:07:02,480 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:08f6ddac-3648-4815-9dd8-55ad345b5419:84d6430f-0692-4bea-816d-0204ff421018, 消息数=2, Token=585
2026-01-10 16:07:02,480 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:08f6ddac-3648-4815-9dd8-55ad345b5419:84d6430f-0692-4bea-816d-0204ff421018)
2026-01-10 16:07:02,482 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2026-01-10 16:07:02,488 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed