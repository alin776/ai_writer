2025-12-25 12:45:12,575 - app.services.ai.prompts - INFO - Prompts loaded successfully from D:\Java\ai_writer\backend\app\services\ai\prompts\default.json
2025-12-25 12:45:12,575 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2025-12-25 12:45:12,577 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2025-12-25 12:45:12,578 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2025-12-25 12:45:14,307 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2025-12-25 12:45:14,308 - app.api.v1.agent - INFO - [Chat Stream] Mode: planning
2025-12-25 12:45:14,311 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:56611 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2025-12-25 12:45:14,320 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 你好，我是一个新手作家，正在写修仙小说...
2025-12-25 12:45:14,321 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2025-12-25 12:45:14,322 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2025-12-25 12:45:14,322 - app.services.ai.http_ai_service - INFO - [成本追踪] 初始化未传db/user_id，将使用请求上下文按需记录成本
2025-12-25 12:45:15,973 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2025-12-25 12:45:15,974 - app.services.agent.tools.writing_tools - INFO - Writing tools AI service initialized
2025-12-25 12:45:15,974 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ AI Service 已同时设置到 langgraph_tools 和 writing_tools
2025-12-25 12:45:15,974 - app.services.context.adaptive_budget - INFO - ✅ 所有预算配置验证通过
2025-12-25 12:45:26,259 - app.services.context.vector_memory_store - INFO - ✅ VectorMemoryStore初始化成功 | 目录=./data/chroma_db | 模型=paraphrase-multilingual-MiniLM-L12-v2 | 集合=user_memories
2025-12-25 12:45:26,261 - app.services.context.manager - INFO - ✅ VectorMemoryStore 已初始化
2025-12-25 12:45:26,262 - app.services.context.manager - INFO - ✅ ContextManager: 长期记忆已启用 (user_id=None)
2025-12-25 12:45:26,262 - app.services.context.manager - INFO - ✅ ContextManager: 自适应预算已启用
2025-12-25 12:45:26,262 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ ContextManager已初始化（长期记忆已启用，自适应预算已启用，总预算=16000 tokens）
成功加载模板: analyze_text (版本 3.1.0)
成功加载模板: intent_classifier (版本 2.0.0)
成功加载模板: writing_agent (版本 2.0.0)
成功加载模板: planning_agent (版本 2.0.0)
成功加载模板: tool_agent (版本 2.0.0)
成功加载模板: query_agent (版本 2.0.0)
成功加载模板: system_agent_prompt (版本 2.0.0)
成功加载模板: creative_writing_prompt (版本 1.0.0)
2025-12-25 12:45:26,364 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ PromptManager已初始化
2025-12-25 12:45:26,373 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ Redis连接验证成功
2025-12-25 12:45:26,376 - app.services.agent.langgraph_agent - INFO - [LangGraph] OK 使用 AsyncRedisSaver（redis://localhost:6379/0，TTL=7天）
2025-12-25 12:45:26,377 - app.services.agent.memory.metrics - INFO - [MemoryMetrics] 监控系统已初始化
2025-12-25 12:45:26,379 - app.services.agent.memory.long_term_store - INFO - [LongTermStore] Initialized: base_dir=./data/long_term_memory, max_size=50KB, compression=True
2025-12-25 12:45:26,379 - app.services.agent.memory.enhanced_memory_manager - INFO - EnhancedMemoryManager initialized: short=10, medium=100, threshold=0.1, long_term_backup=enabled
2025-12-25 12:45:26,379 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ EnhancedMemoryManager已创建
2025-12-25 12:45:26,379 - app.services.agent.memory.unified_coordinator - INFO - [UnifiedMemoryCoordinator] 初始化统一记忆协调器
2025-12-25 12:45:26,380 - app.services.agent.memory.unified_coordinator - INFO - [UnifiedMemoryCoordinator] 全局实例已设置
2025-12-25 12:45:26,381 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ UnifiedMemoryCoordinator已初始化 | checkpointer=AsyncRedisSaver | enhanced_memory=yes | context_manager=yes
2025-12-25 12:45:26,381 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ 解耦模块已初始化 (IntentClassifier, ToolExecutor, EventParser, ResponseBuilder, ToolDispatcher, ParallelExecutor, PlanGenerator, QuickPathHandler, StreamEventHandler, SecondaryToolHandler, TaskRunner, AgentExecutor)
2025-12-25 12:45:26,388 - app.services.agent.parallel_tool_node - INFO - [ParallelToolNode] 初始化完成，最大并发数=5，并行安全工具=4个
2025-12-25 12:45:26,463 - app.api.v1.agent - INFO - [Global Agent] created global agent instance; MemorySaver shared across requests
2025-12-25 12:45:26,464 - app.api.v1.agent - INFO - [agent_chat_stream] 📥 收到的 context 字段:
2025-12-25 12:45:26,464 - app.api.v1.agent - INFO -   - selected_text: N/A...
2025-12-25 12:45:26,465 - app.api.v1.agent - INFO -   - selection_position: N/A
2025-12-25 12:45:26,465 - app.api.v1.agent - INFO -   - chapter_context: 当前章节ID: c726baba-b01b-42ea-9c5d-0d2d5b221d94...
2025-12-25 12:45:26,466 - app.api.v1.agent - INFO -   - instruction_context: N/A...
2025-12-25 12:45:26,466 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:9a44f30e-86be-48ca-b066-606eef7e1d99 (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=f141c5ed-0a75-4429-ba2a-912c74d167a3, conversation_id=9a44f30e-86be-48ca-b066-606eef7e1d99)
2025-12-25 12:45:26,467 - app.services.context.monitoring_integration - INFO - ✅ ContextManager监控收集器已初始化
2025-12-25 12:45:26,467 - app.services.context.store - INFO - [ContextStore] Redis连接成功
2025-12-25 12:45:26,482 - app.services.context.manager - INFO - [ContextManager] 创建新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:9a44f30e-86be-48ca-b066-606eef7e1d99
2025-12-25 12:45:26,884 - app.services.context.token_counter - INFO - ✅ tiktoken初始化成功，模型: gemini-2.5-pro -> cl100k_base
2025-12-25 12:45:26,887 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:9a44f30e-86be-48ca-b066-606eef7e1d99: 0/16000 tokens
2025-12-25 12:45:28,615 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='你好，我是一个新手作家，正在写修仙小说...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:f141c5ed-0a75-4429-ba2a-912c74d167a3', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=0条
2025-12-25 12:45:28,620 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=f141c5ed-0a75-4429-ba2a-912c74d167a3 | 含用户级=True | 找到=0条
2025-12-25 12:45:28,621 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 0条消息, 0 tokens, 耗时 2153.68ms
2025-12-25 12:45:28,626 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 你好，我是一个新手作家，正在写修仙小说...
2025-12-25 12:45:28,635 - app.core.cache - INFO - ⚠️ 缓存未命中: prompt:planning_agent:v2.12.0:get_planning_agent_mode_prompt:fca6eb91156619d0
2025-12-25 12:45:28,639 - app.core.cache - INFO - ⚠️ 缓存未命中: prompt:planning:v2.12.0:get_planning_static_prompt:fca6eb91156619d0
2025-12-25 12:45:28,649 - app.core.cache - INFO - 💾 缓存已保存: prompt:planning:v2.12.0:get_planning_static_prompt:fca6eb91156619d0 (expire=3600s)
2025-12-25 12:45:28,653 - app.core.cache - INFO - 💾 缓存已保存: prompt:planning_agent:v2.12.0:get_planning_agent_mode_prompt:fca6eb91156619d0 (expire=3600s)
2025-12-25 12:45:28,677 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2025-12-25 12:45:28,681 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=simple_qa, complexity=simple, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro, reason=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
2025-12-25 12:45:28,681 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=2000, temp=0.3, task_type=TaskType.SIMPLE_QA
2025-12-25 12:45:30,620 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-12-25 12:45:32,149 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 10 个数据块，总长度: 812
2025-12-25 12:45:32,150 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 5937 (prompt=5519, completion=418)
2025-12-25 12:45:32,152 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2025-12-25 12:45:32,153 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2025-12-25 12:45:32,195 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/3749ebb4-a2d6-4ab8-aa14-cf6c26611fc0/unread-info
INFO:     127.0.0.1:54787 - "GET /api/v1/channels/3749ebb4-a2d6-4ab8-aa14-cf6c26611fc0/unread-info HTTP/1.1" 200 OK
2025-12-25 12:45:32,204 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:54785 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2025-12-25 12:45:32,294 - app.services.ai.http_ai_service - INFO - [积分扣除] 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456: 扣除 8.92 积分, 余额: 54599.36 → 54590.44
2025-12-25 12:45:32,296 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=5937, cost=$0.000719, time=3471ms
2025-12-25 12:45:32,297 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=5937
2025-12-25 12:45:32,297 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户是新手作家，正在写修仙小说，需要AI写作助手的帮助。具体, 原料=用户是新手作家，需要写作方面的帮助。, 处理=需要引导用户明确具体需求，例如是需要构思
2025-12-25 12:45:32,298 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共1个任务
2025-12-25 12:45:32,298 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共1个任务，耗时: 3.67s
2025-12-25 12:45:32,298 - app.api.v1.agent - INFO - [Stream] Plan tasks: 1 items
2025-12-25 12:45:32,299 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2025-12-25 12:45:32,299 - app.services.agent.langgraph_agent - INFO - [DeepAgent] 启用反思模式
2025-12-25 12:45:32,321 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2025-12-25 12:45:32,322 - app.services.agent.langgraph_agent - INFO - [DeepAgent] ParameterResolver 已启用
2025-12-25 12:45:32,329 - app.services.agent.deep_agent.executor - INFO - DeepAgent 开始执行，共 1 个任务，反思功能已启用
2025-12-25 12:45:32,329 - app.services.agent.deep_agent.task_enricher - INFO - [TaskEnricher] AI 推断功能已启用
2025-12-25 12:45:32,330 - app.api.v1.agent - INFO - [Stream] Task started: 引导用户明确写作需求
2025-12-25 12:45:32,330 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(continue_writing)
2025-12-25 12:45:32,331 - app.services.agent.tools.tool_types - INFO - [continue_writing] 开始执行工具
2025-12-25 12:45:32,342 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2025-12-25 12:45:32,343 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=content_creation, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: content_creation; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2025-12-25 12:45:32,343 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=1000, temp=0.8, task_type=TaskType.CONTENT_CREATION
2025-12-25 12:45:56,705 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-12-25 12:45:58,647 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 6 个数据块，总长度: 436
2025-12-25 12:45:58,648 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 3225 (prompt=2873, completion=352)
2025-12-25 12:45:58,648 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2025-12-25 12:45:58,648 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2025-12-25 12:45:58,686 - app.services.ai.http_ai_service - INFO - [积分扣除] 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456: 扣除 88.18 积分, 余额: 54590.44 → 54502.26
2025-12-25 12:45:58,686 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=3225, cost=$0.007111, time=26303ms
2025-12-25 12:45:58,691 - app.services.agent.tools.tool_types - INFO - [continue_writing] 执行成功 (耗时: 26.360s)
2025-12-25 12:45:58,691 - app.services.agent.tools.tool_monitor - INFO - ToolMonitor initialized with Memory storage, retention: 7 days
2025-12-25 12:45:58,691 - app.services.agent.execution.task_runner - INFO - [TaskRunner] continue_writing 执行成功（DeepAgent模式）
2025-12-25 12:45:58,691 - app.api.v1.agent - INFO - [Stream] 任务完成: 引导用户明确写作需求 (26.4s)
2025-12-25 12:45:58,691 - app.services.agent.deep_agent.reflection - INFO - [Checkpoint] 首个任务 1 未标记 checkpoint，触发一次兜底反思以校验规划
2025-12-25 12:45:58,691 - app.services.agent.deep_agent.executor - INFO - 任务 1 触发反思检查点
2025-12-25 12:45:58,698 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2025-12-25 12:45:58,698 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=simple_qa, complexity=simple, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro, reason=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
2025-12-25 12:45:58,698 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
2025-12-25 12:45:59,869 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-12-25 12:45:59,920 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 1 个数据块，总长度: 4
2025-12-25 12:45:59,920 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 95 (prompt=94, completion=1)
2025-12-25 12:45:59,920 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2025-12-25 12:45:59,920 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2025-12-25 12:45:59,952 - app.services.ai.http_ai_service - INFO - [积分扣除] 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456: 扣除 0.12 积分, 余额: 54502.26 → 54502.14
2025-12-25 12:45:59,952 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=95, cost=$0.000010, time=1222ms
2025-12-25 12:45:59,952 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=95
2025-12-25 12:45:59,952 - app.services.agent.deep_agent.reflection - INFO - [DeepAgent反思] 开始调用 AI，task_id=1
2025-12-25 12:45:59,959 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2025-12-25 12:45:59,959 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=simple_qa, complexity=simple, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro, reason=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
2025-12-25 12:45:59,959 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=500, temp=0.3, task_type=TaskType.SIMPLE_QA
2025-12-25 12:46:00,670 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-12-25 12:46:00,823 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 3 个数据块，总长度: 92
2025-12-25 12:46:00,824 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 1237 (prompt=1192, completion=45)
2025-12-25 12:46:00,824 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2025-12-25 12:46:00,824 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2025-12-25 12:46:00,847 - app.services.ai.http_ai_service - INFO - [积分扣除] 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456: 扣除 1.7 积分, 余额: 54502.14 → 54500.44
2025-12-25 12:46:00,849 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1237, cost=$0.000137, time=864ms
2025-12-25 12:46:00,849 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=1237
2025-12-25 12:46:00,849 - app.services.agent.deep_agent.reflection - INFO - [Reflection] JSON解析成功: needs_replan=False
2025-12-25 12:46:00,855 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2025-12-25 12:46:00,855 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=simple_qa, complexity=simple, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro, reason=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
2025-12-25 12:46:00,855 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
2025-12-25 12:46:01,946 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-12-25 12:46:01,951 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 1 个数据块，总长度: 4
2025-12-25 12:46:01,953 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 95 (prompt=94, completion=1)
2025-12-25 12:46:01,953 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2025-12-25 12:46:01,953 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2025-12-25 12:46:01,977 - app.services.ai.http_ai_service - INFO - [积分扣除] 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456: 扣除 0.12 积分, 余额: 54500.44 → 54500.32
2025-12-25 12:46:01,977 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=95, cost=$0.000010, time=1098ms
2025-12-25 12:46:01,985 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=95
2025-12-25 12:46:01,985 - app.services.agent.deep_agent.executor - INFO - DeepAgent 执行完成: 任务=1, 反思=1, 重规划=0
2025-12-25 12:46:01,985 - app.services.agent.langgraph_agent - INFO - [DeepAgent] 执行完成: 反思=1次, 重规划=0次
2025-12-25 12:46:01,985 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共1个任务，耗时: 29.69s
2025-12-25 12:46:01,987 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2025-12-25 12:46:01,987 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=1, 展示型=0
2025-12-25 12:46:01,987 - app.services.agent.langgraph_agent - INFO - [Response] 单个分析任务(continue_writing_tool)，使用AI格式化
2025-12-25 12:46:01,989 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2025-12-25 12:46:01,989 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=471字符, 处理后=486字符
2025-12-25 12:46:01,989 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2025-12-25 12:46:01,989 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2025-12-25 12:46:01,997 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2025-12-25 12:46:01,997 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2025-12-25 12:46:01,997 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
2025-12-25 12:46:13,572 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-12-25 12:46:15,814 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 10 个数据块，总长度: 817
2025-12-25 12:46:15,814 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 2683 (prompt=2072, completion=611)
2025-12-25 12:46:15,814 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2025-12-25 12:46:15,814 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2025-12-25 12:46:15,829 - app.services.ai.http_ai_service - INFO - [积分扣除] 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456: 扣除 26.65 积分, 余额: 54500.32 → 54473.67
2025-12-25 12:46:15,834 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2683, cost=$0.002149, time=13816ms
2025-12-25 12:46:15,834 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=817
2025-12-25 12:46:16,438 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:f141c5ed-0a75-4429-ba2a-912c74d167a3 | 重要度=0.60
2025-12-25 12:46:16,443 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:9a44f30e-86be-48ca-b066-606eef7e1d99, token=1018
2025-12-25 12:46:16,443 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:9a44f30e-86be-48ca-b066-606eef7e1d99, 消息数=2, Token=1018
2025-12-25 12:46:16,443 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:9a44f30e-86be-48ca-b066-606eef7e1d99)
2025-12-25 12:46:16,443 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2025-12-25 12:46:16,458 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed
2025-12-25 12:46:32,137 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:54265 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2025-12-25 12:46:32,147 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/3749ebb4-a2d6-4ab8-aa14-cf6c26611fc0/unread-info
INFO:     127.0.0.1:54264 - "GET /api/v1/channels/3749ebb4-a2d6-4ab8-aa14-cf6c26611fc0/unread-info HTTP/1.1" 200 OK
2025-12-25 12:47:04,094 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2025-12-25 12:47:04,095 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2025-12-25 12:47:04,095 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2025-12-25 12:47:05,814 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2025-12-25 12:47:05,815 - app.api.v1.agent - INFO - [Chat Stream] Mode: planning
2025-12-25 12:47:05,819 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:60016 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2025-12-25 12:47:05,831 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 什么是"器灵"？在修仙小说中器灵一般有什么作用？...
2025-12-25 12:47:05,832 - app.api.v1.agent - INFO - [agent_chat_stream] 📥 收到的 context 字段:
2025-12-25 12:47:05,833 - app.api.v1.agent - INFO -   - selected_text: N/A...
2025-12-25 12:47:05,834 - app.api.v1.agent - INFO -   - selection_position: N/A
2025-12-25 12:47:05,835 - app.api.v1.agent - INFO -   - chapter_context: 当前章节ID: c726baba-b01b-42ea-9c5d-0d2d5b221d94...
2025-12-25 12:47:05,835 - app.api.v1.agent - INFO -   - instruction_context: N/A...
2025-12-25 12:47:05,837 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:9a44f30e-86be-48ca-b066-606eef7e1d99 (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=f141c5ed-0a75-4429-ba2a-912c74d167a3, conversation_id=9a44f30e-86be-48ca-b066-606eef7e1d99)
2025-12-25 12:47:05,840 - app.services.context.store - INFO - [ContextStore] 加载上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:9a44f30e-86be-48ca-b066-606eef7e1d99, 2条消息
2025-12-25 12:47:05,843 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:9a44f30e-86be-48ca-b066-606eef7e1d99: 1018/16000 tokens
2025-12-25 12:47:05,956 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='什么是"器灵"？在修仙小说中器灵一般有什么作用？...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:f141c5ed-0a75-4429-ba2a-912c74d167a3', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=1条
2025-12-25 12:47:05,957 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=f141c5ed-0a75-4429-ba2a-912c74d167a3 | 含用户级=True | 找到=1条
2025-12-25 12:47:05,958 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 3条消息, 1018 tokens, 耗时 119.80ms
2025-12-25 12:47:05,959 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 3 条历史消息 (token: 1018)
2025-12-25 12:47:05,960 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 什么是"器灵"？在修仙小说中器灵一般有什么作用？...
2025-12-25 12:47:05,965 - app.core.cache - INFO - ✅ 缓存命中: prompt:planning_agent:v2.12.0:get_planning_agent_mode_prompt:fca6eb91156619d0
2025-12-25 12:47:05,972 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2025-12-25 12:47:05,972 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=simple_qa, complexity=simple, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro, reason=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
2025-12-25 12:47:05,973 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=2000, temp=0.3, task_type=TaskType.SIMPLE_QA
2025-12-25 12:47:07,805 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-12-25 12:47:09,024 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 8 个数据块，总长度: 642
2025-12-25 12:47:09,024 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 6464 (prompt=6160, completion=304)
2025-12-25 12:47:09,024 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2025-12-25 12:47:09,024 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2025-12-25 12:47:09,042 - app.services.ai.http_ai_service - INFO - [积分扣除] 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456: 扣除 9.15 积分, 余额: 54473.67 → 54464.52
2025-12-25 12:47:09,045 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=6464, cost=$0.000738, time=3050ms
2025-12-25 12:47:09,045 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=6464
2025-12-25 12:47:09,045 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户想了解“器灵”的概念以及在修仙小说中的作用，期望得到解释, 原料=需要对“器灵”这个概念进行解释和说明，可, 处理=使用 continue_writing_
2025-12-25 12:47:09,045 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共1个任务
2025-12-25 12:47:09,045 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共1个任务，耗时: 3.09s
2025-12-25 12:47:09,045 - app.api.v1.agent - INFO - [Stream] Plan tasks: 1 items
2025-12-25 12:47:09,045 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2025-12-25 12:47:09,045 - app.services.agent.langgraph_agent - INFO - [DeepAgent] 启用反思模式
2025-12-25 12:47:09,045 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2025-12-25 12:47:09,045 - app.services.agent.langgraph_agent - INFO - [DeepAgent] ParameterResolver 已启用
2025-12-25 12:47:09,045 - app.services.agent.deep_agent.executor - INFO - DeepAgent 开始执行，共 1 个任务，反思功能已启用
2025-12-25 12:47:09,045 - app.services.agent.deep_agent.task_enricher - INFO - [TaskEnricher] AI 推断功能已启用
2025-12-25 12:47:09,045 - app.api.v1.agent - INFO - [Stream] Task started: 创作关于“器灵”的定义和作用的解释性内容。
2025-12-25 12:47:09,045 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(continue_writing)
2025-12-25 12:47:09,045 - app.services.agent.tools.tool_types - INFO - [continue_writing] 开始执行工具
2025-12-25 12:47:09,049 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2025-12-25 12:47:09,049 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=content_creation, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: content_creation; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2025-12-25 12:47:09,053 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=1000, temp=0.8, task_type=TaskType.CONTENT_CREATION
2025-12-25 12:47:32,141 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:53310 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2025-12-25 12:47:32,166 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/3749ebb4-a2d6-4ab8-aa14-cf6c26611fc0/unread-info
INFO:     127.0.0.1:53311 - "GET /api/v1/channels/3749ebb4-a2d6-4ab8-aa14-cf6c26611fc0/unread-info HTTP/1.1" 200 OK
2025-12-25 12:47:33,248 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-12-25 12:47:34,370 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 4 个数据块，总长度: 317
2025-12-25 12:47:34,370 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 2211 (prompt=1952, completion=259)
2025-12-25 12:47:34,370 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2025-12-25 12:47:34,370 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2025-12-25 12:47:34,391 - app.services.ai.http_ai_service - INFO - [积分扣除] 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456: 扣除 62.37 积分, 余额: 54464.52 → 54402.15
2025-12-25 12:47:34,398 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2211, cost=$0.005030, time=25317ms
2025-12-25 12:47:34,400 - app.services.agent.tools.tool_types - INFO - [continue_writing] 执行成功 (耗时: 25.355s)
2025-12-25 12:47:34,400 - app.services.agent.execution.task_runner - INFO - [TaskRunner] continue_writing 执行成功（DeepAgent模式）
2025-12-25 12:47:34,400 - app.api.v1.agent - INFO - [Stream] 任务完成: 创作关于“器灵”的定义和作用的解释性内容。 (25.4s)
2025-12-25 12:47:34,400 - app.services.agent.deep_agent.reflection - INFO - [Checkpoint] 首个任务 1 未标记 checkpoint，触发一次兜底反思以校验规划
2025-12-25 12:47:34,400 - app.services.agent.deep_agent.executor - INFO - 任务 1 触发反思检查点
2025-12-25 12:47:34,409 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2025-12-25 12:47:34,409 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=simple_qa, complexity=simple, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro, reason=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
2025-12-25 12:47:34,409 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
2025-12-25 12:47:35,479 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-12-25 12:47:35,552 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 1 个数据块，总长度: 4
2025-12-25 12:47:35,555 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 110 (prompt=109, completion=1)
2025-12-25 12:47:35,555 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2025-12-25 12:47:35,555 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2025-12-25 12:47:35,589 - app.services.ai.http_ai_service - INFO - [积分扣除] 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456: 扣除 0.14 积分, 余额: 54402.15 → 54402.01
2025-12-25 12:47:35,591 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=110, cost=$0.000011, time=1142ms
2025-12-25 12:47:35,591 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=110
2025-12-25 12:47:35,591 - app.services.agent.deep_agent.reflection - INFO - [DeepAgent反思] 开始调用 AI，task_id=1
2025-12-25 12:47:35,601 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2025-12-25 12:47:35,601 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=simple_qa, complexity=simple, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro, reason=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
2025-12-25 12:47:35,601 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=500, temp=0.3, task_type=TaskType.SIMPLE_QA
2025-12-25 12:47:36,304 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-12-25 12:47:36,457 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 3 个数据块，总长度: 96
2025-12-25 12:47:36,457 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 1262 (prompt=1212, completion=50)
2025-12-25 12:47:36,457 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2025-12-25 12:47:36,460 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2025-12-25 12:47:36,482 - app.services.ai.http_ai_service - INFO - [积分扣除] 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456: 扣除 1.75 积分, 余额: 54402.01 → 54400.26
2025-12-25 12:47:36,482 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1262, cost=$0.000141, time=858ms
2025-12-25 12:47:36,482 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=1262
2025-12-25 12:47:36,482 - app.services.agent.deep_agent.reflection - INFO - [Reflection] JSON解析成功: needs_replan=False
2025-12-25 12:47:36,491 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2025-12-25 12:47:36,491 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=simple_qa, complexity=simple, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro, reason=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
2025-12-25 12:47:36,498 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
2025-12-25 12:47:37,582 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-12-25 12:47:37,582 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 1 个数据块，总长度: 4
2025-12-25 12:47:37,582 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 110 (prompt=109, completion=1)
2025-12-25 12:47:37,582 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2025-12-25 12:47:37,586 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2025-12-25 12:47:37,613 - app.services.ai.http_ai_service - INFO - [积分扣除] 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456: 扣除 0.14 积分, 余额: 54400.26 → 54400.12
2025-12-25 12:47:37,613 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=110, cost=$0.000011, time=1088ms
2025-12-25 12:47:37,613 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=110
2025-12-25 12:47:37,613 - app.services.agent.deep_agent.executor - INFO - DeepAgent 执行完成: 任务=1, 反思=1, 重规划=0
2025-12-25 12:47:37,613 - app.services.agent.langgraph_agent - INFO - [DeepAgent] 执行完成: 反思=1次, 重规划=0次
2025-12-25 12:47:37,613 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共1个任务，耗时: 28.57s
2025-12-25 12:47:37,613 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2025-12-25 12:47:37,613 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=1, 展示型=0
2025-12-25 12:47:37,613 - app.services.agent.langgraph_agent - INFO - [Response] 单个分析任务(continue_writing_tool)，使用AI格式化
2025-12-25 12:47:37,613 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2025-12-25 12:47:37,613 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=357字符, 处理后=383字符
2025-12-25 12:47:37,613 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2025-12-25 12:47:37,623 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2025-12-25 12:47:37,630 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2025-12-25 12:47:37,630 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2025-12-25 12:47:37,630 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
2025-12-25 12:47:39,688 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-12-25 12:47:40,398 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 6 个数据块，总长度: 317
2025-12-25 12:47:40,398 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 967 (prompt=708, completion=259)
2025-12-25 12:47:40,398 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2025-12-25 12:47:40,398 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2025-12-25 12:47:40,425 - app.services.ai.http_ai_service - INFO - [积分扣除] 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456: 扣除 10.66 积分, 余额: 54400.12 → 54389.46
2025-12-25 12:47:40,428 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=967, cost=$0.000860, time=2767ms
2025-12-25 12:47:40,428 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=317
2025-12-25 12:47:40,935 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:f141c5ed-0a75-4429-ba2a-912c74d167a3 | 重要度=0.88
2025-12-25 12:47:40,942 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:9a44f30e-86be-48ca-b066-606eef7e1d99, token=1460
2025-12-25 12:47:40,942 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:9a44f30e-86be-48ca-b066-606eef7e1d99, 消息数=4, Token=1460
2025-12-25 12:47:40,942 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:9a44f30e-86be-48ca-b066-606eef7e1d99)
2025-12-25 12:47:40,942 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2025-12-25 12:47:40,942 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed
2025-12-25 12:48:25,707 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2025-12-25 12:48:25,707 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2025-12-25 12:48:25,708 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2025-12-25 12:48:27,351 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2025-12-25 12:48:27,352 - app.api.v1.agent - INFO - [Chat Stream] Mode: planning
2025-12-25 12:48:27,355 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:63769 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2025-12-25 12:48:27,371 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 我的小说主角有"吞噬器灵"的能力，这个设定怎么样？会不会太过强大？...
2025-12-25 12:48:27,373 - app.api.v1.agent - INFO - [agent_chat_stream] 📥 收到的 context 字段:
2025-12-25 12:48:27,373 - app.api.v1.agent - INFO -   - selected_text: N/A...
2025-12-25 12:48:27,374 - app.api.v1.agent - INFO -   - selection_position: N/A
2025-12-25 12:48:27,374 - app.api.v1.agent - INFO -   - chapter_context: 当前章节ID: c726baba-b01b-42ea-9c5d-0d2d5b221d94...
2025-12-25 12:48:27,374 - app.api.v1.agent - INFO -   - instruction_context: N/A...
2025-12-25 12:48:27,375 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:9a44f30e-86be-48ca-b066-606eef7e1d99 (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=f141c5ed-0a75-4429-ba2a-912c74d167a3, conversation_id=9a44f30e-86be-48ca-b066-606eef7e1d99)
2025-12-25 12:48:27,380 - app.services.context.store - INFO - [ContextStore] 加载上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:9a44f30e-86be-48ca-b066-606eef7e1d99, 4条消息
2025-12-25 12:48:27,382 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:9a44f30e-86be-48ca-b066-606eef7e1d99: 1460/16000 tokens
2025-12-25 12:48:27,493 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='我的小说主角有"吞噬器灵"的能力，这个设定怎么样？会不会太过...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:f141c5ed-0a75-4429-ba2a-912c74d167a3', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=2条
2025-12-25 12:48:27,493 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=f141c5ed-0a75-4429-ba2a-912c74d167a3 | 含用户级=True | 找到=2条
2025-12-25 12:48:27,518 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 5条消息, 1460 tokens, 耗时 143.79ms
2025-12-25 12:48:27,519 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 5 条历史消息 (token: 1460)
2025-12-25 12:48:27,519 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 我的小说主角有"吞噬器灵"的能力，这个设定怎么样？会不会太过强大？...
2025-12-25 12:48:27,524 - app.core.cache - INFO - ✅ 缓存命中: prompt:planning_agent:v2.12.0:get_planning_agent_mode_prompt:fca6eb91156619d0
2025-12-25 12:48:27,534 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2025-12-25 12:48:27,535 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=simple_qa, complexity=simple, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro, reason=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
2025-12-25 12:48:27,535 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=2000, temp=0.3, task_type=TaskType.SIMPLE_QA
2025-12-25 12:48:29,621 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-12-25 12:48:30,697 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 9 个数据块，总长度: 756
2025-12-25 12:48:30,699 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 6791 (prompt=6445, completion=346)
2025-12-25 12:48:30,701 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2025-12-25 12:48:30,702 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2025-12-25 12:48:30,731 - app.services.ai.http_ai_service - INFO - [积分扣除] 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456: 扣除 9.71 积分, 余额: 54389.46 → 54379.75
2025-12-25 12:48:30,732 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=6791, cost=$0.000783, time=3167ms
2025-12-25 12:48:30,734 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=6791
2025-12-25 12:48:30,735 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户想了解“吞噬器灵”这个设定的优缺点，以及是否会过于强大，, 原料=用户关于“吞噬器灵”设定的描述。, 处理=分析该设定的潜力、潜在问题，并给出平衡的
2025-12-25 12:48:30,736 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共2个任务
2025-12-25 12:48:30,737 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共2个任务，耗时: 3.22s
2025-12-25 12:48:30,737 - app.api.v1.agent - INFO - [Stream] Plan tasks: 2 items
2025-12-25 12:48:30,738 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2025-12-25 12:48:30,738 - app.services.agent.langgraph_agent - INFO - [DeepAgent] 启用反思模式
2025-12-25 12:48:30,739 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2025-12-25 12:48:30,739 - app.services.agent.langgraph_agent - INFO - [DeepAgent] ParameterResolver 已启用
2025-12-25 12:48:30,740 - app.services.agent.deep_agent.executor - INFO - DeepAgent 开始执行，共 2 个任务，反思功能已启用
2025-12-25 12:48:30,740 - app.services.agent.deep_agent.task_enricher - INFO - [TaskEnricher] AI 推断功能已启用
2025-12-25 12:48:30,741 - app.api.v1.agent - INFO - [Stream] Task started: 分析“吞噬器灵”设定的优点和潜力
2025-12-25 12:48:30,741 - app.services.agent.execution.task_runner - INFO - [TaskRunner] analyze_text_tool 使用 focus: '分析“吞噬器灵”设定的优点、在修仙小说中的潜力，以及可能带来的精彩情节。...'
2025-12-25 12:48:30,741 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(analyze_text)
2025-12-25 12:48:30,743 - app.services.agent.tools.tool_types - INFO - [analyze_text] 开始执行工具
2025-12-25 12:48:30,745 - app.services.agent.tools.analysis_tools - INFO - [analyze_text_tool] 尝试第 1 次调用，config={'temperature': 0.3, 'task_type': <TaskType.SUMMARIZATION: 'summarization'>}
2025-12-25 12:48:30,762 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2025-12-25 12:48:30,763 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2025-12-25 12:48:30,764 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
2025-12-25 12:48:32,141 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/3749ebb4-a2d6-4ab8-aa14-cf6c26611fc0/unread-info
INFO:     127.0.0.1:54867 - "GET /api/v1/channels/3749ebb4-a2d6-4ab8-aa14-cf6c26611fc0/unread-info HTTP/1.1" 200 OK
2025-12-25 12:48:32,164 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:54865 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2025-12-25 12:48:37,509 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-12-25 12:48:40,752 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 9 个数据块，总长度: 792
2025-12-25 12:48:40,753 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 1731 (prompt=1147, completion=584)
2025-12-25 12:48:40,753 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2025-12-25 12:48:40,754 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2025-12-25 12:48:40,784 - app.services.ai.http_ai_service - INFO - [积分扣除] 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456: 扣除 22.37 积分, 余额: 54379.75 → 54357.38
2025-12-25 12:48:40,789 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1731, cost=$0.001804, time=9990ms
2025-12-25 12:48:40,794 - app.services.agent.tools.analysis_tools - INFO - [analyze_text_tool] 第 1 次调用成功
2025-12-25 12:48:40,796 - app.services.agent.tools.analysis_tools - INFO - [analyze_text_tool] 分析完成，结果长度: 792
2025-12-25 12:48:40,797 - app.services.agent.tools.tool_types - INFO - [analyze_text] 执行成功 (耗时: 10.054s)
2025-12-25 12:48:40,797 - app.services.agent.execution.task_runner - INFO - [TaskRunner] analyze_text 执行成功（DeepAgent模式）
2025-12-25 12:48:40,798 - app.api.v1.agent - INFO - [Stream] 任务完成: 分析“吞噬器灵”设定的优点和潜力 (10.1s)
2025-12-25 12:48:40,798 - app.services.agent.deep_agent.reflection - INFO - [Checkpoint] 首个任务 1 未标记 checkpoint，触发一次兜底反思以校验规划
2025-12-25 12:48:40,799 - app.services.agent.deep_agent.executor - INFO - 任务 1 触发反思检查点
2025-12-25 12:48:40,811 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2025-12-25 12:48:40,813 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=simple_qa, complexity=simple, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro, reason=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
2025-12-25 12:48:40,814 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
2025-12-25 12:48:42,622 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-12-25 12:48:42,720 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 1 个数据块，总长度: 4
2025-12-25 12:48:42,720 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 107 (prompt=106, completion=1)
2025-12-25 12:48:42,720 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2025-12-25 12:48:42,720 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2025-12-25 12:48:42,751 - app.services.ai.http_ai_service - INFO - [积分扣除] 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456: 扣除 0.14 积分, 余额: 54357.38 → 54357.24
2025-12-25 12:48:42,751 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=107, cost=$0.000011, time=1907ms
2025-12-25 12:48:42,751 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=107
2025-12-25 12:48:42,754 - app.services.agent.deep_agent.reflection - INFO - [DeepAgent反思] 开始调用 AI，task_id=1
2025-12-25 12:48:42,762 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2025-12-25 12:48:42,762 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=simple_qa, complexity=simple, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro, reason=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
2025-12-25 12:48:42,762 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=500, temp=0.3, task_type=TaskType.SIMPLE_QA
2025-12-25 12:48:43,439 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-12-25 12:48:43,672 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 3 个数据块，总长度: 91
2025-12-25 12:48:43,672 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 1228 (prompt=1182, completion=46)
2025-12-25 12:48:43,672 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2025-12-25 12:48:43,673 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2025-12-25 12:48:43,715 - app.services.ai.http_ai_service - INFO - [积分扣除] 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456: 扣除 1.69 积分, 余额: 54357.24 → 54355.55
2025-12-25 12:48:43,715 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1228, cost=$0.000137, time=912ms
2025-12-25 12:48:43,722 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=1228
2025-12-25 12:48:43,722 - app.services.agent.deep_agent.reflection - INFO - [Reflection] JSON解析成功: needs_replan=False
2025-12-25 12:48:43,722 - app.api.v1.agent - INFO - [Stream] Task started: 分析“吞噬器灵”设定的潜在问题和强度平衡
2025-12-25 12:48:43,722 - app.services.agent.execution.task_runner - INFO - [TaskRunner] analyze_text_tool 使用 focus: '分析“吞噬器灵”设定的潜在问题，例如是否会过于强大导致剧情失衡，并提出平衡设定的建议。...'
2025-12-25 12:48:43,726 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(analyze_text)
2025-12-25 12:48:43,726 - app.services.agent.tools.tool_types - INFO - [analyze_text] 开始执行工具
2025-12-25 12:48:43,727 - app.services.agent.tools.analysis_tools - INFO - [analyze_text_tool] 尝试第 1 次调用，config={'temperature': 0.3, 'task_type': <TaskType.SUMMARIZATION: 'summarization'>}
2025-12-25 12:48:43,738 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2025-12-25 12:48:43,738 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2025-12-25 12:48:43,738 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
2025-12-25 12:48:48,423 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-12-25 12:48:52,160 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 14 个数据块，总长度: 1027
2025-12-25 12:48:52,160 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 1757 (prompt=1087, completion=670)
2025-12-25 12:48:52,160 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2025-12-25 12:48:52,161 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2025-12-25 12:48:52,179 - app.services.ai.http_ai_service - INFO - [积分扣除] 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456: 扣除 24.81 积分, 余额: 54355.55 → 54330.74
2025-12-25 12:48:52,180 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1757, cost=$0.002001, time=8417ms
2025-12-25 12:48:52,180 - app.services.agent.tools.analysis_tools - INFO - [analyze_text_tool] 第 1 次调用成功
2025-12-25 12:48:52,181 - app.services.agent.tools.analysis_tools - INFO - [analyze_text_tool] 分析完成，结果长度: 1027
2025-12-25 12:48:52,181 - app.services.agent.tools.tool_types - INFO - [analyze_text] 执行成功 (耗时: 8.455s)
2025-12-25 12:48:52,181 - app.services.agent.execution.task_runner - INFO - [TaskRunner] analyze_text 执行成功（DeepAgent模式）
2025-12-25 12:48:52,182 - app.api.v1.agent - INFO - [Stream] 任务完成: 分析“吞噬器灵”设定的潜在问题和强度平衡 (8.5s)
2025-12-25 12:48:52,188 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2025-12-25 12:48:52,189 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=simple_qa, complexity=simple, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro, reason=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
2025-12-25 12:48:52,189 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
2025-12-25 12:48:53,623 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-12-25 12:48:53,627 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 1 个数据块，总长度: 4
2025-12-25 12:48:53,627 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 107 (prompt=106, completion=1)
2025-12-25 12:48:53,628 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2025-12-25 12:48:53,628 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2025-12-25 12:48:53,647 - app.services.ai.http_ai_service - INFO - [积分扣除] 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456: 扣除 0.14 积分, 余额: 54330.74 → 54330.6
2025-12-25 12:48:53,648 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=107, cost=$0.000011, time=1438ms
2025-12-25 12:48:53,649 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=107
2025-12-25 12:48:53,654 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2025-12-25 12:48:53,654 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=simple_qa, complexity=simple, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro, reason=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
2025-12-25 12:48:53,655 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
2025-12-25 12:48:54,292 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-12-25 12:48:54,300 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 1 个数据块，总长度: 4
2025-12-25 12:48:54,300 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 110 (prompt=109, completion=1)
2025-12-25 12:48:54,300 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2025-12-25 12:48:54,301 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2025-12-25 12:48:54,320 - app.services.ai.http_ai_service - INFO - [积分扣除] 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456: 扣除 0.14 积分, 余额: 54330.6 → 54330.46
2025-12-25 12:48:54,324 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=110, cost=$0.000011, time=647ms
2025-12-25 12:48:54,324 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=110
2025-12-25 12:48:54,326 - app.services.agent.deep_agent.executor - INFO - DeepAgent 执行完成: 任务=2, 反思=1, 重规划=0
2025-12-25 12:48:54,326 - app.services.agent.langgraph_agent - INFO - [DeepAgent] 执行完成: 反思=1次, 重规划=0次
2025-12-25 12:48:54,326 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共2个任务，耗时: 23.59s
2025-12-25 12:48:54,327 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2025-12-25 12:48:54,327 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=2, 展示型=0
2025-12-25 12:48:54,327 - app.services.agent.langgraph_agent - INFO - [Response] 2个分析类任务，使用AI整合（避免冗余）
2025-12-25 12:48:54,327 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2025-12-25 12:48:54,328 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=1877字符, 处理后=1918字符
2025-12-25 12:48:54,328 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2025-12-25 12:48:54,328 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2025-12-25 12:48:54,333 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2025-12-25 12:48:54,334 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2025-12-25 12:48:54,334 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
2025-12-25 12:48:58,571 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-12-25 12:49:03,556 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 17 个数据块，总长度: 1617
2025-12-25 12:49:03,556 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 2992 (prompt=1895, completion=1097)
2025-12-25 12:49:03,557 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2025-12-25 12:49:03,558 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2025-12-25 12:49:03,579 - app.services.ai.http_ai_service - INFO - [积分扣除] 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456: 扣除 41.06 积分, 余额: 54330.46 → 54289.4
2025-12-25 12:49:03,579 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2992, cost=$0.003311, time=9224ms
2025-12-25 12:49:03,579 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=1617
2025-12-25 12:49:04,919 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:f141c5ed-0a75-4429-ba2a-912c74d167a3 | 重要度=0.60
2025-12-25 12:49:06,268 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:f141c5ed-0a75-4429-ba2a-912c74d167a3 | 重要度=0.92
2025-12-25 12:49:06,276 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:9a44f30e-86be-48ca-b066-606eef7e1d99, token=3341
2025-12-25 12:49:06,279 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:9a44f30e-86be-48ca-b066-606eef7e1d99, 消息数=6, Token=3341
2025-12-25 12:49:06,279 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:9a44f30e-86be-48ca-b066-606eef7e1d99)
2025-12-25 12:49:06,280 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2025-12-25 12:49:06,287 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed
2025-12-25 12:49:32,150 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/3749ebb4-a2d6-4ab8-aa14-cf6c26611fc0/unread-info
INFO:     127.0.0.1:57616 - "GET /api/v1/channels/3749ebb4-a2d6-4ab8-aa14-cf6c26611fc0/unread-info HTTP/1.1" 200 OK
2025-12-25 12:49:32,181 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:57614 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2025-12-25 12:50:32,135 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:51007 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2025-12-25 12:50:32,146 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/3749ebb4-a2d6-4ab8-aa14-cf6c26611fc0/unread-info
INFO:     127.0.0.1:51009 - "GET /api/v1/channels/3749ebb4-a2d6-4ab8-aa14-cf6c26611fc0/unread-info HTTP/1.1" 200 OK
2025-12-25 12:50:43,426 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:58274 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2025-12-25 12:50:46,460 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:53463 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2025-12-25 12:50:46,489 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2025-12-25 12:50:46,492 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2025-12-25 12:50:46,492 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2025-12-25 12:50:48,181 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2025-12-25 12:50:48,182 - app.api.v1.agent - INFO - [Chat Stream] Mode: planning
2025-12-25 12:50:48,184 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:59220 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2025-12-25 12:50:48,196 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 读取第1章的内容...
2025-12-25 12:50:48,197 - app.api.v1.agent - INFO - [agent_chat_stream] 📥 收到的 context 字段:
2025-12-25 12:50:48,198 - app.api.v1.agent - INFO -   - selected_text: N/A...
2025-12-25 12:50:48,199 - app.api.v1.agent - INFO -   - selection_position: N/A
2025-12-25 12:50:48,199 - app.api.v1.agent - INFO -   - chapter_context: 当前章节ID: c726baba-b01b-42ea-9c5d-0d2d5b221d94...
2025-12-25 12:50:48,199 - app.api.v1.agent - INFO -   - instruction_context: N/A...
2025-12-25 12:50:48,200 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:d4b53eb7-f412-4d8d-9a93-b5372a558d05 (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=f141c5ed-0a75-4429-ba2a-912c74d167a3, conversation_id=d4b53eb7-f412-4d8d-9a93-b5372a558d05)
2025-12-25 12:50:48,204 - app.services.context.manager - INFO - [ContextManager] 创建新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:d4b53eb7-f412-4d8d-9a93-b5372a558d05
2025-12-25 12:50:48,205 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:d4b53eb7-f412-4d8d-9a93-b5372a558d05: 0/16000 tokens
2025-12-25 12:50:48,359 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='读取第1章的内容...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:f141c5ed-0a75-4429-ba2a-912c74d167a3', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=3条
2025-12-25 12:50:48,362 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=f141c5ed-0a75-4429-ba2a-912c74d167a3 | 含用户级=True | 找到=3条
2025-12-25 12:50:48,362 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 1条消息, 0 tokens, 耗时 162.20ms
2025-12-25 12:50:48,364 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 1 条历史消息 (token: 0)
2025-12-25 12:50:48,365 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 读取第1章的内容...
2025-12-25 12:50:48,372 - app.core.cache - INFO - ✅ 缓存命中: prompt:planning:v2.12.0:get_planning_static_prompt:fca6eb91156619d0
2025-12-25 12:50:48,378 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2025-12-25 12:50:48,378 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=simple_qa, complexity=simple, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro, reason=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
2025-12-25 12:50:48,378 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=2000, temp=0.3, task_type=TaskType.SIMPLE_QA
2025-12-25 12:50:50,940 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-12-25 12:50:51,456 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 7 个数据块，总长度: 349
2025-12-25 12:50:51,460 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 4587 (prompt=4437, completion=150)
2025-12-25 12:50:51,462 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2025-12-25 12:50:51,463 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2025-12-25 12:50:51,513 - app.services.ai.http_ai_service - INFO - [积分扣除] 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456: 扣除 6.25 积分, 余额: 54289.4 → 54283.15
2025-12-25 12:50:51,515 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4587, cost=$0.000504, time=3085ms
2025-12-25 12:50:51,517 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=4587
2025-12-25 12:50:51,517 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户期望看到原文内容，直接返回, 原料=需要第1章的内容, 处理=直接返回，无需处理
2025-12-25 12:50:51,518 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共1个任务
2025-12-25 12:50:51,519 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共1个任务，耗时: 3.15s
2025-12-25 12:50:51,519 - app.api.v1.agent - INFO - [Stream] Plan tasks: 1 items
2025-12-25 12:50:51,519 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2025-12-25 12:50:51,520 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2025-12-25 12:50:51,521 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2025-12-25 12:50:51,521 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 任务分组: 第一层并行=1, 第二层并行=0, 串行=0
2025-12-25 12:50:51,521 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始第一层并行执行1个任务
2025-12-25 12:50:51,522 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务1开始: 获取第1章的内容
2025-12-25 12:50:51,522 - app.api.v1.agent - INFO - [Stream] Task started: 获取第1章的内容
2025-12-25 12:50:51,523 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(get_chapter_by_order)
2025-12-25 12:50:51,523 - app.services.agent.tools.tool_types - INFO - [get_chapter_by_order] 开始执行工具
2025-12-25 12:50:51,547 - app.services.agent.langgraph_tools - INFO - [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
2025-12-25 12:50:51,550 - app.services.agent.tools.tool_types - INFO - [get_chapter_by_order] 执行成功 (耗时: 0.026s)
2025-12-25 12:50:51,550 - app.services.agent.execution.task_runner - INFO - [TaskRunner] get_chapter_by_order 执行成功（DeepAgent模式）
2025-12-25 12:50:51,551 - app.api.v1.agent - INFO - [Stream] 任务完成: 获取第1章的内容 (0.0s)
2025-12-25 12:50:51,551 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务1完成
2025-12-25 12:50:51,553 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共1个任务，耗时: 0.03s
2025-12-25 12:50:51,554 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2025-12-25 12:50:51,555 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=0, 展示型=1
2025-12-25 12:50:51,555 - app.services.agent.langgraph_agent - INFO - [Response] 纯展示型任务(1个)，直接格式化返回（跳过AI整合，节省成本）
2025-12-25 12:50:53,023 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:f141c5ed-0a75-4429-ba2a-912c74d167a3 | 重要度=0.73
2025-12-25 12:50:53,029 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:d4b53eb7-f412-4d8d-9a93-b5372a558d05, token=1935
2025-12-25 12:50:53,032 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:d4b53eb7-f412-4d8d-9a93-b5372a558d05, 消息数=2, Token=1935
2025-12-25 12:50:53,032 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:d4b53eb7-f412-4d8d-9a93-b5372a558d05)
2025-12-25 12:50:53,034 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2025-12-25 12:50:53,040 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed
2025-12-25 12:51:09,245 - app.api.v1.ai - INFO - [预加载元数据] 用户: 2072855200@qq.com(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: f141c5ed-0a75-4429-ba2a-912c74d167a3, chapter_id: f191ba48-5d94-41bb-a94e-33257003ae93
2025-12-25 12:51:09,258 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: f191ba48-5d94-41bb-a94e-33257003ae93
2025-12-25 12:51:09,262 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: 1cb73820-a951-48f1-8d81-7dced6d8d278
2025-12-25 12:51:09,263 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2025-12-25 12:51:09,264 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:50072 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2025-12-25 12:51:09,294 - app.api.v1.ai - INFO - [预加载元数据] 用户: 2072855200@qq.com(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: f141c5ed-0a75-4429-ba2a-912c74d167a3, chapter_id: f191ba48-5d94-41bb-a94e-33257003ae93
2025-12-25 12:51:09,302 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: f191ba48-5d94-41bb-a94e-33257003ae93
2025-12-25 12:51:09,306 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: 1cb73820-a951-48f1-8d81-7dced6d8d278
2025-12-25 12:51:09,306 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2025-12-25 12:51:09,308 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:56425 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2025-12-25 12:51:09,394 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:56427 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2025-12-25 12:51:09,464 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:f141c5ed-0a75-4429-ba2a-912c74d167a3
2025-12-25 12:51:09,465 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/f191ba48-5d94-41bb-a94e-33257003ae93
INFO:     127.0.0.1:57426 - "PUT /api/v1/chapters/f191ba48-5d94-41bb-a94e-33257003ae93 HTTP/1.1" 200 OK
2025-12-25 12:51:09,467 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第3章 一夕千悟 (order=3)
2025-12-25 12:51:10,058 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第3章 一夕千悟 (6 chunks)
2025-12-25 12:51:10,082 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:f141c5ed-0a75-4429-ba2a-912c74d167a3
2025-12-25 12:51:10,084 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/f191ba48-5d94-41bb-a94e-33257003ae93
INFO:     127.0.0.1:54696 - "PUT /api/v1/chapters/f191ba48-5d94-41bb-a94e-33257003ae93 HTTP/1.1" 200 OK
2025-12-25 12:51:10,086 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第3章 一夕千悟 (order=3)
2025-12-25 12:51:10,665 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第3章 一夕千悟 (6 chunks)
2025-12-25 12:51:13,034 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:54056 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2025-12-25 12:51:13,066 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2025-12-25 12:51:13,066 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2025-12-25 12:51:13,066 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2025-12-25 12:51:14,800 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2025-12-25 12:51:14,802 - app.api.v1.agent - INFO - [Chat Stream] Mode: planning
2025-12-25 12:51:14,805 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:57264 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2025-12-25 12:51:14,819 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 帮我读取"第3章 一夕千悟"的内容...
2025-12-25 12:51:14,819 - app.api.v1.agent - INFO - [agent_chat_stream] 📥 收到的 context 字段:
2025-12-25 12:51:14,820 - app.api.v1.agent - INFO -   - selected_text: N/A...
2025-12-25 12:51:14,821 - app.api.v1.agent - INFO -   - selection_position: N/A
2025-12-25 12:51:14,821 - app.api.v1.agent - INFO -   - chapter_context: 当前章节ID: f191ba48-5d94-41bb-a94e-33257003ae93...
2025-12-25 12:51:14,821 - app.api.v1.agent - INFO -   - instruction_context: N/A...
2025-12-25 12:51:14,822 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:9a128dc4-f3f2-4e1f-bd73-5f5c5b78af36 (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=f141c5ed-0a75-4429-ba2a-912c74d167a3, conversation_id=9a128dc4-f3f2-4e1f-bd73-5f5c5b78af36)
2025-12-25 12:51:14,829 - app.services.context.manager - INFO - [ContextManager] 创建新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:9a128dc4-f3f2-4e1f-bd73-5f5c5b78af36
2025-12-25 12:51:14,829 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:9a128dc4-f3f2-4e1f-bd73-5f5c5b78af36: 0/16000 tokens
2025-12-25 12:51:14,978 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='帮我读取"第3章 一夕千悟"的内容...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:f141c5ed-0a75-4429-ba2a-912c74d167a3', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=3条
2025-12-25 12:51:14,978 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=f141c5ed-0a75-4429-ba2a-912c74d167a3 | 含用户级=True | 找到=3条
2025-12-25 12:51:14,979 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 1条消息, 0 tokens, 耗时 156.54ms
2025-12-25 12:51:14,979 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 1 条历史消息 (token: 0)
2025-12-25 12:51:14,980 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 帮我读取"第3章 一夕千悟"的内容...
2025-12-25 12:51:14,983 - app.core.cache - INFO - ✅ 缓存命中: prompt:planning:v2.12.0:get_planning_static_prompt:fca6eb91156619d0
2025-12-25 12:51:14,991 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2025-12-25 12:51:14,992 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=simple_qa, complexity=simple, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro, reason=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
2025-12-25 12:51:14,992 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=2000, temp=0.3, task_type=TaskType.SIMPLE_QA
2025-12-25 12:51:16,843 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-12-25 12:51:17,272 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 6 个数据块，总长度: 386
2025-12-25 12:51:17,273 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 4623 (prompt=4447, completion=176)
2025-12-25 12:51:17,273 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2025-12-25 12:51:17,274 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2025-12-25 12:51:17,297 - app.services.ai.http_ai_service - INFO - [积分扣除] 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456: 扣除 6.39 积分, 余额: 54283.15 → 54276.76
2025-12-25 12:51:17,299 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4623, cost=$0.000515, time=2281ms
2025-12-25 12:51:17,300 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=4623
2025-12-25 12:51:17,301 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户期望看到“第3章 一夕千悟”的原文内容。, 原料=需要“第3章 一夕千悟”的章节内容。, 处理=直接获取章节内容并返回。
2025-12-25 12:51:17,301 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共1个任务
2025-12-25 12:51:17,302 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共1个任务，耗时: 2.32s
2025-12-25 12:51:17,302 - app.api.v1.agent - INFO - [Stream] Plan tasks: 1 items
2025-12-25 12:51:17,303 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2025-12-25 12:51:17,303 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2025-12-25 12:51:17,303 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2025-12-25 12:51:17,304 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 任务分组: 第一层并行=1, 第二层并行=0, 串行=0
2025-12-25 12:51:17,304 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始第一层并行执行1个任务
2025-12-25 12:51:17,305 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务1开始: 获取“第3章 一夕千悟”的内容
2025-12-25 12:51:17,305 - app.api.v1.agent - INFO - [Stream] Task started: 获取“第3章 一夕千悟”的内容
2025-12-25 12:51:17,306 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(get_chapter_by_order)
2025-12-25 12:51:17,306 - app.services.agent.tools.tool_types - INFO - [get_chapter_by_order] 开始执行工具
2025-12-25 12:51:17,326 - app.services.agent.langgraph_tools - INFO - [get_chapter_by_order_tool] ✅ 找到第3章: 第3章 一夕千悟
2025-12-25 12:51:17,329 - app.services.agent.tools.tool_types - INFO - [get_chapter_by_order] 执行成功 (耗时: 0.023s)
2025-12-25 12:51:17,329 - app.services.agent.execution.task_runner - INFO - [TaskRunner] get_chapter_by_order 执行成功（DeepAgent模式）
2025-12-25 12:51:17,330 - app.api.v1.agent - INFO - [Stream] 任务完成: 获取“第3章 一夕千悟”的内容 (0.0s)
2025-12-25 12:51:17,330 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务1完成
2025-12-25 12:51:17,330 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共1个任务，耗时: 0.03s
2025-12-25 12:51:17,331 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2025-12-25 12:51:17,331 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=0, 展示型=1
2025-12-25 12:51:17,331 - app.services.agent.langgraph_agent - INFO - [Response] 纯展示型任务(1个)，直接格式化返回（跳过AI整合，节省成本）
2025-12-25 12:51:18,480 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:f141c5ed-0a75-4429-ba2a-912c74d167a3 | 重要度=0.58
2025-12-25 12:51:18,486 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:9a128dc4-f3f2-4e1f-bd73-5f5c5b78af36, token=1893
2025-12-25 12:51:18,487 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:9a128dc4-f3f2-4e1f-bd73-5f5c5b78af36, 消息数=2, Token=1893
2025-12-25 12:51:18,488 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:9a128dc4-f3f2-4e1f-bd73-5f5c5b78af36)
2025-12-25 12:51:18,489 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2025-12-25 12:51:18,495 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed
2025-12-25 12:51:32,151 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/3749ebb4-a2d6-4ab8-aa14-cf6c26611fc0/unread-info
INFO:     127.0.0.1:60521 - "GET /api/v1/channels/3749ebb4-a2d6-4ab8-aa14-cf6c26611fc0/unread-info HTTP/1.1" 200 OK
2025-12-25 12:51:32,164 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:60520 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2025-12-25 12:51:45,083 - app.api.v1.ai - INFO - [预加载元数据] 用户: 2072855200@qq.com(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: f141c5ed-0a75-4429-ba2a-912c74d167a3, chapter_id: c0661752-e71b-48ad-8597-0957516a43fe
2025-12-25 12:51:45,093 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: c0661752-e71b-48ad-8597-0957516a43fe
2025-12-25 12:51:45,098 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: 3d3c8ed2-78ab-4e75-bb90-c79e1b446040
2025-12-25 12:51:45,098 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2025-12-25 12:51:45,101 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:60162 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2025-12-25 12:51:45,138 - app.api.v1.ai - INFO - [预加载元数据] 用户: 2072855200@qq.com(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: f141c5ed-0a75-4429-ba2a-912c74d167a3, chapter_id: c0661752-e71b-48ad-8597-0957516a43fe
2025-12-25 12:51:45,145 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: c0661752-e71b-48ad-8597-0957516a43fe
2025-12-25 12:51:45,149 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: 3d3c8ed2-78ab-4e75-bb90-c79e1b446040
2025-12-25 12:51:45,149 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2025-12-25 12:51:45,151 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:50726 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2025-12-25 12:51:45,213 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:50727 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2025-12-25 12:51:45,278 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:f141c5ed-0a75-4429-ba2a-912c74d167a3
2025-12-25 12:51:45,280 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/c0661752-e71b-48ad-8597-0957516a43fe
INFO:     127.0.0.1:57418 - "PUT /api/v1/chapters/c0661752-e71b-48ad-8597-0957516a43fe HTTP/1.1" 200 OK
2025-12-25 12:51:45,281 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2025-12-25 12:51:45,855 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (6 chunks)
2025-12-25 12:51:45,879 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:f141c5ed-0a75-4429-ba2a-912c74d167a3
2025-12-25 12:51:45,880 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/c0661752-e71b-48ad-8597-0957516a43fe
INFO:     127.0.0.1:52570 - "PUT /api/v1/chapters/c0661752-e71b-48ad-8597-0957516a43fe HTTP/1.1" 200 OK
2025-12-25 12:51:45,881 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2025-12-25 12:51:46,472 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (6 chunks)
2025-12-25 12:51:48,271 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:58183 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2025-12-25 12:51:48,290 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2025-12-25 12:51:48,290 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2025-12-25 12:51:48,292 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2025-12-25 12:51:49,979 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2025-12-25 12:51:49,980 - app.api.v1.agent - INFO - [Chat Stream] Mode: planning
2025-12-25 12:51:49,984 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:59477 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2025-12-25 12:51:49,992 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 这部小说有哪些章节？...
2025-12-25 12:51:49,995 - app.api.v1.agent - INFO - [agent_chat_stream] 📥 收到的 context 字段:
2025-12-25 12:51:49,995 - app.api.v1.agent - INFO -   - selected_text: N/A...
2025-12-25 12:51:49,995 - app.api.v1.agent - INFO -   - selection_position: N/A
2025-12-25 12:51:49,996 - app.api.v1.agent - INFO -   - chapter_context: 当前章节ID: c0661752-e71b-48ad-8597-0957516a43fe...
2025-12-25 12:51:49,996 - app.api.v1.agent - INFO -   - instruction_context: N/A...
2025-12-25 12:51:49,996 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:ed0a7a9f-cbc3-48fe-80f2-0f980472da82 (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=f141c5ed-0a75-4429-ba2a-912c74d167a3, conversation_id=ed0a7a9f-cbc3-48fe-80f2-0f980472da82)
2025-12-25 12:51:50,000 - app.services.context.manager - INFO - [ContextManager] 创建新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:ed0a7a9f-cbc3-48fe-80f2-0f980472da82
2025-12-25 12:51:50,000 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:ed0a7a9f-cbc3-48fe-80f2-0f980472da82: 0/16000 tokens
2025-12-25 12:51:50,141 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='这部小说有哪些章节？...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:f141c5ed-0a75-4429-ba2a-912c74d167a3', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=3条
2025-12-25 12:51:50,144 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=f141c5ed-0a75-4429-ba2a-912c74d167a3 | 含用户级=True | 找到=3条
2025-12-25 12:51:50,145 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 1条消息, 0 tokens, 耗时 148.36ms
2025-12-25 12:51:50,145 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 1 条历史消息 (token: 0)
2025-12-25 12:51:50,146 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 这部小说有哪些章节？...
2025-12-25 12:51:50,158 - app.core.cache - INFO - ✅ 缓存命中: prompt:planning:v2.12.0:get_planning_static_prompt:fca6eb91156619d0
2025-12-25 12:51:50,168 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2025-12-25 12:51:50,169 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=simple_qa, complexity=simple, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro, reason=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
2025-12-25 12:51:50,170 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=2000, temp=0.3, task_type=TaskType.SIMPLE_QA
2025-12-25 12:51:52,323 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-12-25 12:51:53,013 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 7 个数据块，总长度: 422
2025-12-25 12:51:53,014 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 4637 (prompt=4441, completion=196)
2025-12-25 12:51:53,015 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2025-12-25 12:51:53,015 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2025-12-25 12:51:53,047 - app.services.ai.http_ai_service - INFO - [积分扣除] 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456: 扣除 6.48 积分, 余额: 54276.76 → 54270.28
2025-12-25 12:51:53,049 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4637, cost=$0.000522, time=2846ms
2025-12-25 12:51:53,051 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=4637
2025-12-25 12:51:53,051 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户想知道这部小说有哪些章节，期望得到一个章节列表。, 原料=需要作品的章节信息。, 处理=获取作品的章节列表，并直接返回给用户。
2025-12-25 12:51:53,052 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共1个任务
2025-12-25 12:51:53,052 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共1个任务，耗时: 2.91s
2025-12-25 12:51:53,052 - app.api.v1.agent - INFO - [Stream] Plan tasks: 1 items
2025-12-25 12:51:53,052 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2025-12-25 12:51:53,053 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2025-12-25 12:51:53,053 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2025-12-25 12:51:53,053 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 任务分组: 第一层并行=1, 第二层并行=0, 串行=0
2025-12-25 12:51:53,054 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始第一层并行执行1个任务
2025-12-25 12:51:53,054 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务1开始: 获取作品的章节列表
2025-12-25 12:51:53,055 - app.api.v1.agent - INFO - [Stream] Task started: 获取作品的章节列表
2025-12-25 12:51:53,056 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(get_context)
2025-12-25 12:51:53,056 - app.services.agent.tools.tool_types - INFO - [get_context] 开始执行工具
2025-12-25 12:51:53,069 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=f141c5ed-0a75-4429-ba2a-912c74d167a3, current_order=5, query=作品背景、人物关系、情节发展、伏笔线索...
2025-12-25 12:51:53,203 - app.services.chapter_vector_service - INFO - RAG retrieved 5 segments within order<=5
2025-12-25 12:51:53,204 - app.services.agent.langgraph_tools - INFO - [get_context_tool] ✅ 获取上下文成功
2025-12-25 12:51:53,209 - app.services.agent.tools.tool_types - INFO - [get_context] 执行成功 (耗时: 0.153s)
2025-12-25 12:51:53,210 - app.services.agent.execution.task_runner - INFO - [TaskRunner] get_context 执行成功（DeepAgent模式）
2025-12-25 12:51:53,210 - app.api.v1.agent - INFO - [Stream] 任务完成: 获取作品的章节列表 (0.2s)
2025-12-25 12:51:53,211 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务1完成
2025-12-25 12:51:53,211 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共1个任务，耗时: 0.16s
2025-12-25 12:51:53,211 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2025-12-25 12:51:53,212 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=1, 输出型=0, 展示型=0
2025-12-25 12:51:53,212 - app.services.agent.langgraph_agent - WARNING - [Response] 没有明确输出任务，使用AI整合
2025-12-25 12:51:53,212 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2025-12-25 12:51:53,213 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=4152字符, 处理后=4166字符
2025-12-25 12:51:53,213 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2025-12-25 12:51:53,214 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2025-12-25 12:51:53,222 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2025-12-25 12:51:53,226 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2025-12-25 12:51:53,226 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
2025-12-25 12:51:59,412 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-12-25 12:51:59,416 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 2 个数据块，总长度: 79
2025-12-25 12:51:59,416 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 4279 (prompt=4220, completion=59)
2025-12-25 12:51:59,418 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2025-12-25 12:51:59,419 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2025-12-25 12:51:59,462 - app.services.ai.http_ai_service - INFO - [积分扣除] 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456: 扣除 17.53 积分, 余额: 54270.28 → 54252.75
2025-12-25 12:51:59,464 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4279, cost=$0.001414, time=6193ms
2025-12-25 12:51:59,464 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=79
2025-12-25 12:52:00,826 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:f141c5ed-0a75-4429-ba2a-912c74d167a3 | 重要度=0.65
2025-12-25 12:52:02,037 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:f141c5ed-0a75-4429-ba2a-912c74d167a3 | 重要度=0.54
2025-12-25 12:52:02,043 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:ed0a7a9f-cbc3-48fe-80f2-0f980472da82, token=94
2025-12-25 12:52:02,043 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:ed0a7a9f-cbc3-48fe-80f2-0f980472da82, 消息数=2, Token=94
2025-12-25 12:52:02,043 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:ed0a7a9f-cbc3-48fe-80f2-0f980472da82)
2025-12-25 12:52:02,043 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2025-12-25 12:52:02,049 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed
2025-12-25 12:52:25,710 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2025-12-25 12:52:25,710 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2025-12-25 12:52:25,710 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2025-12-25 12:52:27,235 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2025-12-25 12:52:27,237 - app.api.v1.agent - INFO - [Chat Stream] Mode: planning
2025-12-25 12:52:27,240 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:64533 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2025-12-25 12:52:27,247 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 帮我续写第5章"太一门"的内容，写段融和杨震吃完饭后的剧情...
2025-12-25 12:52:27,248 - app.api.v1.agent - INFO - [agent_chat_stream] 📥 收到的 context 字段:
2025-12-25 12:52:27,248 - app.api.v1.agent - INFO -   - selected_text: N/A...
2025-12-25 12:52:27,249 - app.api.v1.agent - INFO -   - selection_position: N/A
2025-12-25 12:52:27,250 - app.api.v1.agent - INFO -   - chapter_context: 当前章节ID: c0661752-e71b-48ad-8597-0957516a43fe...
2025-12-25 12:52:27,252 - app.api.v1.agent - INFO -   - instruction_context: N/A...
2025-12-25 12:52:27,253 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:ed0a7a9f-cbc3-48fe-80f2-0f980472da82 (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=f141c5ed-0a75-4429-ba2a-912c74d167a3, conversation_id=ed0a7a9f-cbc3-48fe-80f2-0f980472da82)
2025-12-25 12:52:27,257 - app.services.context.store - INFO - [ContextStore] 加载上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:ed0a7a9f-cbc3-48fe-80f2-0f980472da82, 2条消息
2025-12-25 12:52:27,259 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:ed0a7a9f-cbc3-48fe-80f2-0f980472da82: 94/16000 tokens
2025-12-25 12:52:27,358 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='帮我续写第5章"太一门"的内容，写段融和杨震吃完饭后的剧情...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:f141c5ed-0a75-4429-ba2a-912c74d167a3', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=3条
2025-12-25 12:52:27,359 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=f141c5ed-0a75-4429-ba2a-912c74d167a3 | 含用户级=True | 找到=3条
2025-12-25 12:52:27,360 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 3条消息, 94 tokens, 耗时 106.22ms
2025-12-25 12:52:27,360 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 3 条历史消息 (token: 94)
2025-12-25 12:52:27,361 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 帮我续写第5章"太一门"的内容，写段融和杨震吃完饭后的剧情...
2025-12-25 12:52:27,365 - app.core.cache - INFO - ✅ 缓存命中: prompt:planning:v2.12.0:get_planning_static_prompt:fca6eb91156619d0
2025-12-25 12:52:27,372 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2025-12-25 12:52:27,372 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=simple_qa, complexity=simple, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro, reason=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
2025-12-25 12:52:27,373 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=2000, temp=0.3, task_type=TaskType.SIMPLE_QA
2025-12-25 12:52:29,373 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-12-25 12:52:30,721 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 12 个数据块，总长度: 861
2025-12-25 12:52:30,722 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 4989 (prompt=4538, completion=451)
2025-12-25 12:52:30,722 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2025-12-25 12:52:30,723 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2025-12-25 12:52:30,748 - app.services.ai.http_ai_service - INFO - [积分扣除] 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456: 扣除 7.86 积分, 余额: 54252.75 → 54244.89
2025-12-25 12:52:30,750 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4989, cost=$0.000634, time=3350ms
2025-12-25 12:52:30,751 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=4989
2025-12-25 12:52:30,752 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户期望看到续写的内容，即第5章“太一门”的后续剧情，重点是, 原料=需要第4章“家底”的内容作为承接，以及第, 处理=获取第4章内容作为上下文，然后使用 `c
2025-12-25 12:52:30,753 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共2个任务
2025-12-25 12:52:30,753 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共2个任务，耗时: 3.39s
2025-12-25 12:52:30,755 - app.api.v1.agent - INFO - [Stream] Plan tasks: 2 items
2025-12-25 12:52:30,756 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2025-12-25 12:52:30,756 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2025-12-25 12:52:30,758 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2025-12-25 12:52:30,759 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 任务分组: 第一层并行=1, 第二层并行=0, 串行=1
2025-12-25 12:52:30,760 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始第一层并行执行1个任务
2025-12-25 12:52:30,761 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务1开始: 获取第4章“家底”的内容作为续写上下文
2025-12-25 12:52:30,763 - app.api.v1.agent - INFO - [Stream] Task started: 获取第4章“家底”的内容作为续写上下文
2025-12-25 12:52:30,765 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(get_chapter_by_order)
2025-12-25 12:52:30,766 - app.services.agent.tools.tool_types - INFO - [get_chapter_by_order] 开始执行工具
2025-12-25 12:52:30,790 - app.services.agent.langgraph_tools - INFO - [get_chapter_by_order_tool] ✅ 找到第4章: 第4章 家底
2025-12-25 12:52:30,794 - app.services.agent.tools.tool_types - INFO - [get_chapter_by_order] 执行成功 (耗时: 0.028s)
2025-12-25 12:52:30,795 - app.services.agent.execution.task_runner - INFO - [TaskRunner] get_chapter_by_order 执行成功（DeepAgent模式）
2025-12-25 12:52:30,795 - app.api.v1.agent - INFO - [Stream] 任务完成: 获取第4章“家底”的内容作为续写上下文 (0.0s)
2025-12-25 12:52:30,796 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务1完成
2025-12-25 12:52:30,797 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始串行执行1个任务
2025-12-25 12:52:30,797 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务2开始: 续写第5章“太一门”中，融和杨震吃完饭后的剧情
2025-12-25 12:52:30,798 - app.api.v1.agent - INFO - [Stream] Task started: 续写第5章“太一门”中，融和杨震吃完饭后的剧情
2025-12-25 12:52:30,798 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(continue_writing)
2025-12-25 12:52:30,798 - app.services.agent.tools.tool_types - INFO - [continue_writing] 开始执行工具
2025-12-25 12:52:30,809 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2025-12-25 12:52:30,810 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=content_creation, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: content_creation; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2025-12-25 12:52:30,810 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=1000, temp=0.8, task_type=TaskType.CONTENT_CREATION
2025-12-25 12:52:32,147 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:54334 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2025-12-25 12:52:32,152 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/3749ebb4-a2d6-4ab8-aa14-cf6c26611fc0/unread-info
INFO:     127.0.0.1:54336 - "GET /api/v1/channels/3749ebb4-a2d6-4ab8-aa14-cf6c26611fc0/unread-info HTTP/1.1" 200 OK
2025-12-25 12:53:06,120 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-12-25 12:53:08,020 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 6 个数据块，总长度: 487
2025-12-25 12:53:08,020 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 4672 (prompt=4290, completion=382)
2025-12-25 12:53:08,021 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2025-12-25 12:53:08,021 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2025-12-25 12:53:08,032 - app.services.ai.http_ai_service - INFO - [积分扣除] 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456: 扣除 113.86 积分, 余额: 54244.89 → 54131.03
2025-12-25 12:53:08,032 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4672, cost=$0.009183, time=37210ms
2025-12-25 12:53:08,032 - app.services.agent.tools.tool_types - INFO - [continue_writing] 执行成功 (耗时: 37.234s)
2025-12-25 12:53:08,032 - app.services.agent.execution.task_runner - INFO - [TaskRunner] continue_writing 执行成功（DeepAgent模式）
2025-12-25 12:53:08,032 - app.api.v1.agent - INFO - [Stream] 任务完成: 续写第5章“太一门”中，融和杨震吃完饭后的剧情 (37.2s)
2025-12-25 12:53:08,032 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务2完成
2025-12-25 12:53:08,032 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共2个任务，耗时: 37.28s
2025-12-25 12:53:08,032 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2025-12-25 12:53:08,032 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=1, 展示型=1
2025-12-25 12:53:08,032 - app.services.agent.langgraph_agent - INFO - [Response] 单个分析任务(continue_writing_tool)，使用AI格式化
2025-12-25 12:53:08,032 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2025-12-25 12:53:08,032 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=2899字符, 处理后=2946字符
2025-12-25 12:53:08,032 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2025-12-25 12:53:08,032 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2025-12-25 12:53:08,032 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2025-12-25 12:53:08,039 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2025-12-25 12:53:08,039 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
2025-12-25 12:53:21,717 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-12-25 12:53:25,119 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 16 个数据块，总长度: 1284
2025-12-25 12:53:25,119 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 4855 (prompt=3856, completion=999)
2025-12-25 12:53:25,119 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2025-12-25 12:53:25,119 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2025-12-25 12:53:25,147 - app.services.ai.http_ai_service - INFO - [积分扣除] 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456: 扣除 45.31 积分, 余额: 54131.03 → 54085.72
2025-12-25 12:53:25,147 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4855, cost=$0.003654, time=17079ms
2025-12-25 12:53:25,147 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=1284
2025-12-25 12:53:25,630 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:f141c5ed-0a75-4429-ba2a-912c74d167a3 | 重要度=0.99
2025-12-25 12:53:26,113 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:f141c5ed-0a75-4429-ba2a-912c74d167a3 | 重要度=0.73
2025-12-25 12:53:26,128 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:ed0a7a9f-cbc3-48fe-80f2-0f980472da82, token=1809
2025-12-25 12:53:26,129 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:ed0a7a9f-cbc3-48fe-80f2-0f980472da82, 消息数=4, Token=1809
2025-12-25 12:53:26,129 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:ed0a7a9f-cbc3-48fe-80f2-0f980472da82)
2025-12-25 12:53:26,129 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2025-12-25 12:53:26,140 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed
2025-12-25 12:53:30,793 - app.api.v1.ai - INFO - [预加载元数据] 用户: 2072855200@qq.com(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: f141c5ed-0a75-4429-ba2a-912c74d167a3, chapter_id: c726baba-b01b-42ea-9c5d-0d2d5b221d94
2025-12-25 12:53:30,801 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: c726baba-b01b-42ea-9c5d-0d2d5b221d94
2025-12-25 12:53:30,801 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
2025-12-25 12:53:30,803 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:50448 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2025-12-25 12:53:30,847 - app.api.v1.ai - INFO - [预加载元数据] 用户: 2072855200@qq.com(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: f141c5ed-0a75-4429-ba2a-912c74d167a3, chapter_id: c726baba-b01b-42ea-9c5d-0d2d5b221d94
2025-12-25 12:53:30,854 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: c726baba-b01b-42ea-9c5d-0d2d5b221d94
2025-12-25 12:53:30,854 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
2025-12-25 12:53:30,857 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:56803 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2025-12-25 12:53:31,000 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:f141c5ed-0a75-4429-ba2a-912c74d167a3
2025-12-25 12:53:31,001 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/c726baba-b01b-42ea-9c5d-0d2d5b221d94
INFO:     127.0.0.1:59924 - "PUT /api/v1/chapters/c726baba-b01b-42ea-9c5d-0d2d5b221d94 HTTP/1.1" 200 OK
2025-12-25 12:53:31,003 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2025-12-25 12:53:31,677 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (7 chunks)
2025-12-25 12:53:31,730 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:f141c5ed-0a75-4429-ba2a-912c74d167a3
2025-12-25 12:53:31,733 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/c726baba-b01b-42ea-9c5d-0d2d5b221d94
INFO:     127.0.0.1:64485 - "PUT /api/v1/chapters/c726baba-b01b-42ea-9c5d-0d2d5b221d94 HTTP/1.1" 200 OK
2025-12-25 12:53:31,742 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2025-12-25 12:53:32,380 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (7 chunks)
2025-12-25 12:53:32,392 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:51086 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2025-12-25 12:53:32,395 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/3749ebb4-a2d6-4ab8-aa14-cf6c26611fc0/unread-info
INFO:     127.0.0.1:51087 - "GET /api/v1/channels/3749ebb4-a2d6-4ab8-aa14-cf6c26611fc0/unread-info HTTP/1.1" 200 OK
2025-12-25 12:53:34,213 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2025-12-25 12:53:34,213 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2025-12-25 12:53:34,213 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2025-12-25 12:53:35,724 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2025-12-25 12:53:35,725 - app.api.v1.agent - INFO - [Chat Stream] Mode: planning
2025-12-25 12:53:35,729 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:49270 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2025-12-25 12:53:35,735 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 请帮我把第1章开头"青州。渊阳府，贤古县。"这段改写得更有气势...
2025-12-25 12:53:35,737 - app.api.v1.agent - INFO - [agent_chat_stream] 📥 收到的 context 字段:
2025-12-25 12:53:35,738 - app.api.v1.agent - INFO -   - selected_text: N/A...
2025-12-25 12:53:35,739 - app.api.v1.agent - INFO -   - selection_position: N/A
2025-12-25 12:53:35,739 - app.api.v1.agent - INFO -   - chapter_context: 当前章节ID: c726baba-b01b-42ea-9c5d-0d2d5b221d94...
2025-12-25 12:53:35,739 - app.api.v1.agent - INFO -   - instruction_context: N/A...
2025-12-25 12:53:35,741 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:d4b53eb7-f412-4d8d-9a93-b5372a558d05 (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=f141c5ed-0a75-4429-ba2a-912c74d167a3, conversation_id=d4b53eb7-f412-4d8d-9a93-b5372a558d05)
2025-12-25 12:53:35,746 - app.services.context.store - INFO - [ContextStore] 加载上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:d4b53eb7-f412-4d8d-9a93-b5372a558d05, 2条消息
2025-12-25 12:53:35,748 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:d4b53eb7-f412-4d8d-9a93-b5372a558d05: 1935/16000 tokens
2025-12-25 12:53:35,843 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='请帮我把第1章开头"青州。渊阳府，贤古县。"这段改写得更有气...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:f141c5ed-0a75-4429-ba2a-912c74d167a3', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=3条
2025-12-25 12:53:35,844 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=f141c5ed-0a75-4429-ba2a-912c74d167a3 | 含用户级=True | 找到=3条
2025-12-25 12:53:35,846 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 3条消息, 1935 tokens, 耗时 104.50ms
2025-12-25 12:53:35,846 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 3 条历史消息 (token: 1935)
2025-12-25 12:53:35,847 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 请帮我把第1章开头"青州。渊阳府，贤古县。"这段改写得更有气势...
2025-12-25 12:53:35,851 - app.core.cache - INFO - ✅ 缓存命中: prompt:planning:v2.12.0:get_planning_static_prompt:fca6eb91156619d0
2025-12-25 12:53:35,856 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2025-12-25 12:53:35,857 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=simple_qa, complexity=simple, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro, reason=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
2025-12-25 12:53:35,858 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=2000, temp=0.3, task_type=TaskType.SIMPLE_QA
2025-12-25 12:53:37,872 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-12-25 12:53:38,671 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 10 个数据块，总长度: 697
2025-12-25 12:53:38,671 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 5958 (prompt=5649, completion=309)
2025-12-25 12:53:38,672 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2025-12-25 12:53:38,673 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2025-12-25 12:53:38,700 - app.services.ai.http_ai_service - INFO - [积分扣除] 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456: 扣除 8.54 积分, 余额: 54085.72 → 54077.18
2025-12-25 12:53:38,701 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=5958, cost=$0.000688, time=2814ms
2025-12-25 12:53:38,702 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=5958
2025-12-25 12:53:38,703 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户希望对原文的开头部分进行改写，使其更具气势。这属于创作内, 原料=需要原文的开头部分作为改写的基础。, 处理=获取原文开头，然后使用continue_
2025-12-25 12:53:38,703 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共2个任务
2025-12-25 12:53:38,703 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共2个任务，耗时: 2.86s
2025-12-25 12:53:38,704 - app.api.v1.agent - INFO - [Stream] Plan tasks: 2 items
2025-12-25 12:53:38,704 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2025-12-25 12:53:38,704 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2025-12-25 12:53:38,705 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2025-12-25 12:53:38,705 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 任务分组: 第一层并行=1, 第二层并行=0, 串行=1
2025-12-25 12:53:38,706 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始第一层并行执行1个任务
2025-12-25 12:53:38,707 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务1开始: 获取第1章的原文内容
2025-12-25 12:53:38,707 - app.api.v1.agent - INFO - [Stream] Task started: 获取第1章的原文内容
2025-12-25 12:53:38,708 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(get_chapter_by_order)
2025-12-25 12:53:38,709 - app.services.agent.tools.tool_types - INFO - [get_chapter_by_order] 开始执行工具
2025-12-25 12:53:38,724 - app.services.agent.langgraph_tools - INFO - [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
2025-12-25 12:53:38,726 - app.services.agent.tools.tool_types - INFO - [get_chapter_by_order] 执行成功 (耗时: 0.018s)
2025-12-25 12:53:38,727 - app.services.agent.execution.task_runner - INFO - [TaskRunner] get_chapter_by_order 执行成功（DeepAgent模式）
2025-12-25 12:53:38,727 - app.api.v1.agent - INFO - [Stream] 任务完成: 获取第1章的原文内容 (0.0s)
2025-12-25 12:53:38,727 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务1完成
2025-12-25 12:53:38,728 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始串行执行1个任务
2025-12-25 12:53:38,728 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务2开始: 改写第1章开头，使其更具气势
2025-12-25 12:53:38,728 - app.api.v1.agent - INFO - [Stream] Task started: 改写第1章开头，使其更具气势
2025-12-25 12:53:38,730 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(continue_writing)
2025-12-25 12:53:38,730 - app.services.agent.tools.tool_types - INFO - [continue_writing] 开始执行工具
2025-12-25 12:53:38,740 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2025-12-25 12:53:38,741 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=content_creation, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: content_creation; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2025-12-25 12:53:38,742 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=1000, temp=0.8, task_type=TaskType.CONTENT_CREATION
2025-12-25 12:53:55,112 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-12-25 12:54:14,123 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 38 个数据块，总长度: 3091
2025-12-25 12:54:14,125 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 5759 (prompt=3311, completion=2448)
2025-12-25 12:54:14,127 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2025-12-25 12:54:14,127 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2025-12-25 12:54:14,171 - app.services.ai.http_ai_service - INFO - [积分扣除] 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456: 扣除 354.87 积分, 余额: 54077.18 → 53722.31
2025-12-25 12:54:14,173 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=5759, cost=$0.028619, time=35385ms
2025-12-25 12:54:14,175 - app.services.agent.tools.tool_types - INFO - [continue_writing] 执行成功 (耗时: 35.445s)
2025-12-25 12:54:14,176 - app.services.agent.execution.task_runner - INFO - [TaskRunner] continue_writing 执行成功（DeepAgent模式）
2025-12-25 12:54:14,176 - app.api.v1.agent - INFO - [Stream] 任务完成: 改写第1章开头，使其更具气势 (35.4s)
2025-12-25 12:54:14,177 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务2完成
2025-12-25 12:54:14,177 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共2个任务，耗时: 35.47s
2025-12-25 12:54:14,177 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2025-12-25 12:54:14,177 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=1, 展示型=1
2025-12-25 12:54:14,179 - app.services.agent.langgraph_agent - INFO - [Response] 单个创作任务(continue_writing_tool)，输出3091字符，直接返回（跳过AI调用）
2025-12-25 12:54:15,511 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:f141c5ed-0a75-4429-ba2a-912c74d167a3 | 重要度=0.65
2025-12-25 12:54:16,997 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:f141c5ed-0a75-4429-ba2a-912c74d167a3 | 重要度=0.60
2025-12-25 12:54:17,004 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:d4b53eb7-f412-4d8d-9a93-b5372a558d05, token=5996
2025-12-25 12:54:17,009 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:d4b53eb7-f412-4d8d-9a93-b5372a558d05, 消息数=4, Token=5996
2025-12-25 12:54:17,010 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:d4b53eb7-f412-4d8d-9a93-b5372a558d05)
2025-12-25 12:54:17,012 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2025-12-25 12:54:17,019 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed
2025-12-25 12:54:32,126 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:57517 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2025-12-25 12:54:32,129 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/3749ebb4-a2d6-4ab8-aa14-cf6c26611fc0/unread-info
INFO:     127.0.0.1:57518 - "GET /api/v1/channels/3749ebb4-a2d6-4ab8-aa14-cf6c26611fc0/unread-info HTTP/1.1" 200 OK
2025-12-25 12:54:48,082 - app.api.v1.ai - INFO - [预加载元数据] 用户: 2072855200@qq.com(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: f141c5ed-0a75-4429-ba2a-912c74d167a3, chapter_id: c0661752-e71b-48ad-8597-0957516a43fe
2025-12-25 12:54:48,092 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: c0661752-e71b-48ad-8597-0957516a43fe
2025-12-25 12:54:48,095 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: 3d3c8ed2-78ab-4e75-bb90-c79e1b446040
2025-12-25 12:54:48,096 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2025-12-25 12:54:48,099 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:57322 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2025-12-25 12:54:48,130 - app.api.v1.ai - INFO - [预加载元数据] 用户: 2072855200@qq.com(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: f141c5ed-0a75-4429-ba2a-912c74d167a3, chapter_id: c0661752-e71b-48ad-8597-0957516a43fe
2025-12-25 12:54:48,138 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: c0661752-e71b-48ad-8597-0957516a43fe
2025-12-25 12:54:48,141 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: 3d3c8ed2-78ab-4e75-bb90-c79e1b446040
2025-12-25 12:54:48,141 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2025-12-25 12:54:48,143 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:57349 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2025-12-25 12:54:48,266 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:f141c5ed-0a75-4429-ba2a-912c74d167a3
2025-12-25 12:54:48,268 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/c0661752-e71b-48ad-8597-0957516a43fe
INFO:     127.0.0.1:52391 - "PUT /api/v1/chapters/c0661752-e71b-48ad-8597-0957516a43fe HTTP/1.1" 200 OK
2025-12-25 12:54:48,269 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2025-12-25 12:54:48,821 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (6 chunks)
2025-12-25 12:54:48,863 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:f141c5ed-0a75-4429-ba2a-912c74d167a3
2025-12-25 12:54:48,865 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/c0661752-e71b-48ad-8597-0957516a43fe
INFO:     127.0.0.1:56606 - "PUT /api/v1/chapters/c0661752-e71b-48ad-8597-0957516a43fe HTTP/1.1" 200 OK
2025-12-25 12:54:48,867 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2025-12-25 12:54:49,425 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (6 chunks)
2025-12-25 12:54:51,028 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2025-12-25 12:54:51,029 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2025-12-25 12:54:51,029 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2025-12-25 12:54:52,618 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2025-12-25 12:54:52,620 - app.api.v1.agent - INFO - [Chat Stream] Mode: planning
2025-12-25 12:54:52,626 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:64465 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2025-12-25 12:54:52,640 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 分析一下段融这个角色的性格特点和成长轨迹...
2025-12-25 12:54:52,644 - app.api.v1.agent - INFO - [agent_chat_stream] 📥 收到的 context 字段:
2025-12-25 12:54:52,645 - app.api.v1.agent - INFO -   - selected_text: N/A...
2025-12-25 12:54:52,646 - app.api.v1.agent - INFO -   - selection_position: N/A
2025-12-25 12:54:52,647 - app.api.v1.agent - INFO -   - chapter_context: 当前章节ID: c0661752-e71b-48ad-8597-0957516a43fe...
2025-12-25 12:54:52,647 - app.api.v1.agent - INFO -   - instruction_context: N/A...
2025-12-25 12:54:52,650 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:ed0a7a9f-cbc3-48fe-80f2-0f980472da82 (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=f141c5ed-0a75-4429-ba2a-912c74d167a3, conversation_id=ed0a7a9f-cbc3-48fe-80f2-0f980472da82)
2025-12-25 12:54:52,659 - app.services.context.store - INFO - [ContextStore] 加载上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:ed0a7a9f-cbc3-48fe-80f2-0f980472da82, 4条消息
2025-12-25 12:54:52,662 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:ed0a7a9f-cbc3-48fe-80f2-0f980472da82: 1809/16000 tokens
2025-12-25 12:54:52,776 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='分析一下段融这个角色的性格特点和成长轨迹...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:f141c5ed-0a75-4429-ba2a-912c74d167a3', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=3条
2025-12-25 12:54:52,778 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=f141c5ed-0a75-4429-ba2a-912c74d167a3 | 含用户级=True | 找到=3条
2025-12-25 12:54:52,785 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 5条消息, 1809 tokens, 耗时 134.85ms
2025-12-25 12:54:52,786 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 5 条历史消息 (token: 1809)
2025-12-25 12:54:52,787 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 分析一下段融这个角色的性格特点和成长轨迹...
2025-12-25 12:54:52,789 - app.core.cache - INFO - ✅ 缓存命中: prompt:planning:v2.12.0:get_planning_static_prompt:fca6eb91156619d0
2025-12-25 12:54:52,795 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2025-12-25 12:54:52,796 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=simple_qa, complexity=simple, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro, reason=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
2025-12-25 12:54:52,796 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=2000, temp=0.3, task_type=TaskType.SIMPLE_QA
2025-12-25 12:54:55,818 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-12-25 12:54:59,269 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 24 个数据块，总长度: 1783
2025-12-25 12:54:59,270 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 6770 (prompt=5555, completion=1215)
2025-12-25 12:54:59,271 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2025-12-25 12:54:59,271 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2025-12-25 12:54:59,307 - app.services.ai.http_ai_service - INFO - [积分扣除] 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456: 扣除 12.91 积分, 余额: 53722.31 → 53709.4
2025-12-25 12:54:59,309 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=6770, cost=$0.001041, time=6474ms
2025-12-25 12:54:59,310 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=6770
2025-12-25 12:54:59,311 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户希望对段融这个角色进行性格特点和成长轨迹的分析，输出形式, 原料=需要分析已有的文本内容，特别是关于段融的, 处理=使用 analyze_text_tool
2025-12-25 12:54:59,312 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共1个任务
2025-12-25 12:54:59,314 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共1个任务，耗时: 6.53s
2025-12-25 12:54:59,314 - app.api.v1.agent - INFO - [Stream] Plan tasks: 1 items
2025-12-25 12:54:59,316 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2025-12-25 12:54:59,317 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2025-12-25 12:54:59,318 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2025-12-25 12:54:59,319 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 任务分组: 第一层并行=1, 第二层并行=0, 串行=0
2025-12-25 12:54:59,319 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始第一层并行执行1个任务
2025-12-25 12:54:59,320 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务1开始: 分析段融的性格特点和成长轨迹
2025-12-25 12:54:59,321 - app.api.v1.agent - INFO - [Stream] Task started: 分析段融的性格特点和成长轨迹
2025-12-25 12:54:59,322 - app.services.agent.execution.task_runner - INFO - [TaskRunner] analyze_text_tool 使用 focus: '分析段融的性格特点，包括他的冷静、务实、深思熟虑、以及对自身能力的探索欲。同时分析他的成长轨迹，从杂役弟子到外门弟子的转变，以及他面对新环境和挑战时的心态和目标...'
2025-12-25 12:54:59,322 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(analyze_text)
2025-12-25 12:54:59,323 - app.services.agent.tools.tool_types - INFO - [analyze_text] 开始执行工具
2025-12-25 12:54:59,325 - app.services.agent.tools.analysis_tools - INFO - [analyze_text_tool] 尝试第 1 次调用，config={'temperature': 0.3, 'task_type': <TaskType.SUMMARIZATION: 'summarization'>}
2025-12-25 12:54:59,340 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2025-12-25 12:54:59,341 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2025-12-25 12:54:59,342 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
2025-12-25 12:55:04,679 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-12-25 12:55:05,794 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 5 个数据块，总长度: 357
2025-12-25 12:55:05,795 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 2501 (prompt=2252, completion=249)
2025-12-25 12:55:05,796 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2025-12-25 12:55:05,796 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2025-12-25 12:55:05,837 - app.services.ai.http_ai_service - INFO - [积分扣除] 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456: 扣除 16.1 积分, 余额: 53709.4 → 53693.3
2025-12-25 12:55:05,843 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2501, cost=$0.001298, time=6453ms
2025-12-25 12:55:05,844 - app.services.agent.tools.analysis_tools - INFO - [analyze_text_tool] 第 1 次调用成功
2025-12-25 12:55:05,845 - app.services.agent.tools.analysis_tools - INFO - [analyze_text_tool] 分析完成，结果长度: 357
2025-12-25 12:55:05,846 - app.services.agent.tools.tool_types - INFO - [analyze_text] 执行成功 (耗时: 6.523s)
2025-12-25 12:55:05,847 - app.services.agent.execution.task_runner - INFO - [TaskRunner] analyze_text 执行成功（DeepAgent模式）
2025-12-25 12:55:05,848 - app.api.v1.agent - INFO - [Stream] 任务完成: 分析段融的性格特点和成长轨迹 (6.5s)
2025-12-25 12:55:05,848 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务1完成
2025-12-25 12:55:05,850 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共1个任务，耗时: 6.53s
2025-12-25 12:55:05,851 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2025-12-25 12:55:05,851 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=1, 展示型=0
2025-12-25 12:55:05,852 - app.services.agent.langgraph_agent - INFO - [Response] 单个分析任务(analyze_text_tool)，使用AI格式化
2025-12-25 12:55:05,853 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2025-12-25 12:55:05,853 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=393字符, 处理后=412字符
2025-12-25 12:55:05,854 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2025-12-25 12:55:05,854 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2025-12-25 12:55:05,865 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2025-12-25 12:55:05,866 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2025-12-25 12:55:05,867 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
2025-12-25 12:55:08,416 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-12-25 12:55:10,734 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 8 个数据块，总长度: 713
2025-12-25 12:55:10,734 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 1137 (prompt=664, completion=473)
2025-12-25 12:55:10,734 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2025-12-25 12:55:10,736 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2025-12-25 12:55:10,756 - app.services.ai.http_ai_service - INFO - [积分扣除] 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456: 扣除 17.13 积分, 余额: 53693.3 → 53676.17
2025-12-25 12:55:10,758 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1137, cost=$0.001382, time=4868ms
2025-12-25 12:55:10,758 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=713
2025-12-25 12:55:11,994 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:f141c5ed-0a75-4429-ba2a-912c74d167a3 | 重要度=0.89
2025-12-25 12:55:13,207 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:f141c5ed-0a75-4429-ba2a-912c74d167a3 | 重要度=0.94
2025-12-25 12:55:13,214 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:ed0a7a9f-cbc3-48fe-80f2-0f980472da82, token=2637
2025-12-25 12:55:13,216 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:ed0a7a9f-cbc3-48fe-80f2-0f980472da82, 消息数=6, Token=2637
2025-12-25 12:55:13,217 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:ed0a7a9f-cbc3-48fe-80f2-0f980472da82)
2025-12-25 12:55:13,218 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2025-12-25 12:55:13,223 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed
2025-12-25 12:55:32,135 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:64933 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2025-12-25 12:55:32,143 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/3749ebb4-a2d6-4ab8-aa14-cf6c26611fc0/unread-info
INFO:     127.0.0.1:64935 - "GET /api/v1/channels/3749ebb4-a2d6-4ab8-aa14-cf6c26611fc0/unread-info HTTP/1.1" 200 OK
2025-12-25 12:55:47,811 - app.api.v1.ai - INFO - [预加载元数据] 用户: 2072855200@qq.com(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: f141c5ed-0a75-4429-ba2a-912c74d167a3, chapter_id: 1cb73820-a951-48f1-8d81-7dced6d8d278
2025-12-25 12:55:47,817 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 1cb73820-a951-48f1-8d81-7dced6d8d278
2025-12-25 12:55:47,820 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: c726baba-b01b-42ea-9c5d-0d2d5b221d94
2025-12-25 12:55:47,820 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2025-12-25 12:55:47,822 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:63037 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2025-12-25 12:55:47,862 - app.api.v1.ai - INFO - [预加载元数据] 用户: 2072855200@qq.com(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: f141c5ed-0a75-4429-ba2a-912c74d167a3, chapter_id: 1cb73820-a951-48f1-8d81-7dced6d8d278
2025-12-25 12:55:47,871 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 1cb73820-a951-48f1-8d81-7dced6d8d278
2025-12-25 12:55:47,874 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: c726baba-b01b-42ea-9c5d-0d2d5b221d94
2025-12-25 12:55:47,875 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2025-12-25 12:55:47,878 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:55176 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2025-12-25 12:55:47,936 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:55178 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2025-12-25 12:55:48,040 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:f141c5ed-0a75-4429-ba2a-912c74d167a3
2025-12-25 12:55:48,043 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/1cb73820-a951-48f1-8d81-7dced6d8d278
INFO:     127.0.0.1:51738 - "PUT /api/v1/chapters/1cb73820-a951-48f1-8d81-7dced6d8d278 HTTP/1.1" 200 OK
2025-12-25 12:55:48,044 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第2章 浑圆桩 (order=2)
2025-12-25 12:55:48,651 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第2章 浑圆桩 (6 chunks)
2025-12-25 12:55:48,693 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:f141c5ed-0a75-4429-ba2a-912c74d167a3
2025-12-25 12:55:48,696 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/1cb73820-a951-48f1-8d81-7dced6d8d278
INFO:     127.0.0.1:59400 - "PUT /api/v1/chapters/1cb73820-a951-48f1-8d81-7dced6d8d278 HTTP/1.1" 200 OK
2025-12-25 12:55:48,701 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第2章 浑圆桩 (order=2)
2025-12-25 12:55:49,318 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第2章 浑圆桩 (6 chunks)
2025-12-25 12:55:52,313 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:54800 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2025-12-25 12:55:52,332 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2025-12-25 12:55:52,333 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2025-12-25 12:55:52,333 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2025-12-25 12:55:53,852 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2025-12-25 12:55:53,853 - app.api.v1.agent - INFO - [Chat Stream] Mode: planning
2025-12-25 12:55:53,856 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:62126 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2025-12-25 12:55:53,863 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 读取第2章，然后把浑圆桩的描写改得更加生动...
2025-12-25 12:55:53,864 - app.api.v1.agent - INFO - [agent_chat_stream] 📥 收到的 context 字段:
2025-12-25 12:55:53,865 - app.api.v1.agent - INFO -   - selected_text: N/A...
2025-12-25 12:55:53,866 - app.api.v1.agent - INFO -   - selection_position: N/A
2025-12-25 12:55:53,866 - app.api.v1.agent - INFO -   - chapter_context: 当前章节ID: 1cb73820-a951-48f1-8d81-7dced6d8d278...
2025-12-25 12:55:53,866 - app.api.v1.agent - INFO -   - instruction_context: N/A...
2025-12-25 12:55:53,867 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:2284c23b-55c1-4e7b-98fc-66db3c2f512a (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=f141c5ed-0a75-4429-ba2a-912c74d167a3, conversation_id=2284c23b-55c1-4e7b-98fc-66db3c2f512a)
2025-12-25 12:55:53,871 - app.services.context.manager - INFO - [ContextManager] 创建新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:2284c23b-55c1-4e7b-98fc-66db3c2f512a
2025-12-25 12:55:53,871 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:2284c23b-55c1-4e7b-98fc-66db3c2f512a: 0/16000 tokens
2025-12-25 12:55:53,959 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='读取第2章，然后把浑圆桩的描写改得更加生动...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:f141c5ed-0a75-4429-ba2a-912c74d167a3', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=3条
2025-12-25 12:55:53,959 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=f141c5ed-0a75-4429-ba2a-912c74d167a3 | 含用户级=True | 找到=3条
2025-12-25 12:55:53,960 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 1条消息, 0 tokens, 耗时 93.30ms
2025-12-25 12:55:53,960 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 1 条历史消息 (token: 0)
2025-12-25 12:55:53,960 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 读取第2章，然后把浑圆桩的描写改得更加生动...
2025-12-25 12:55:53,964 - app.core.cache - INFO - ✅ 缓存命中: prompt:planning:v2.12.0:get_planning_static_prompt:fca6eb91156619d0
2025-12-25 12:55:53,970 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2025-12-25 12:55:53,970 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=simple_qa, complexity=simple, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro, reason=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
2025-12-25 12:55:53,971 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=2000, temp=0.3, task_type=TaskType.SIMPLE_QA
2025-12-25 12:55:57,080 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-12-25 12:55:57,983 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 11 个数据块，总长度: 823
2025-12-25 12:55:57,985 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 4850 (prompt=4450, completion=400)
2025-12-25 12:55:57,986 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2025-12-25 12:55:57,986 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2025-12-25 12:55:58,019 - app.services.ai.http_ai_service - INFO - [积分扣除] 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456: 扣除 7.5 积分, 余额: 53676.17 → 53668.67
2025-12-25 12:55:58,022 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4850, cost=$0.000605, time=4015ms
2025-12-25 12:55:58,023 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=4850
2025-12-25 12:55:58,024 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户希望对第2章中关于“浑圆桩”的描写进行修改，使其更加生动, 原料=需要第2章的原文内容，以便找到并修改“浑, 处理=使用 `get_chapter_by_o
2025-12-25 12:55:58,025 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共2个任务
2025-12-25 12:55:58,026 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共2个任务，耗时: 4.07s
2025-12-25 12:55:58,026 - app.api.v1.agent - INFO - [Stream] Plan tasks: 2 items
2025-12-25 12:55:58,027 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2025-12-25 12:55:58,027 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2025-12-25 12:55:58,028 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2025-12-25 12:55:58,029 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 任务分组: 第一层并行=1, 第二层并行=0, 串行=1
2025-12-25 12:55:58,030 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始第一层并行执行1个任务
2025-12-25 12:55:58,032 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务1开始: 获取第2章内容
2025-12-25 12:55:58,032 - app.api.v1.agent - INFO - [Stream] Task started: 获取第2章内容
2025-12-25 12:55:58,033 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(get_chapter_by_order)
2025-12-25 12:55:58,034 - app.services.agent.tools.tool_types - INFO - [get_chapter_by_order] 开始执行工具
2025-12-25 12:55:58,057 - app.services.agent.langgraph_tools - INFO - [get_chapter_by_order_tool] ✅ 找到第2章: 第2章 浑圆桩
2025-12-25 12:55:58,059 - app.services.agent.tools.tool_types - INFO - [get_chapter_by_order] 执行成功 (耗时: 0.025s)
2025-12-25 12:55:58,060 - app.services.agent.execution.task_runner - INFO - [TaskRunner] get_chapter_by_order 执行成功（DeepAgent模式）
2025-12-25 12:55:58,061 - app.api.v1.agent - INFO - [Stream] 任务完成: 获取第2章内容 (0.0s)
2025-12-25 12:55:58,061 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务1完成
2025-12-25 12:55:58,062 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始串行执行1个任务
2025-12-25 12:55:58,062 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务2开始: 改写浑圆桩的描写，使其更加生动
2025-12-25 12:55:58,063 - app.api.v1.agent - INFO - [Stream] Task started: 改写浑圆桩的描写，使其更加生动
2025-12-25 12:55:58,065 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(continue_writing)
2025-12-25 12:55:58,067 - app.services.agent.tools.tool_types - INFO - [continue_writing] 开始执行工具
2025-12-25 12:55:58,079 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2025-12-25 12:55:58,080 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=content_creation, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: content_creation; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2025-12-25 12:55:58,082 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=1000, temp=0.8, task_type=TaskType.CONTENT_CREATION
2025-12-25 12:56:16,045 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-12-25 12:56:23,771 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 12 个数据块，总长度: 858
2025-12-25 12:56:23,772 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 4432 (prompt=3718, completion=714)
2025-12-25 12:56:23,773 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2025-12-25 12:56:23,774 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2025-12-25 12:56:23,802 - app.services.ai.http_ai_service - INFO - [积分扣除] 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456: 扣除 146.16 积分, 余额: 53668.67 → 53522.51
2025-12-25 12:56:23,804 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4432, cost=$0.011787, time=25692ms
2025-12-25 12:56:23,804 - app.services.agent.tools.tool_types - INFO - [continue_writing] 执行成功 (耗时: 25.737s)
2025-12-25 12:56:23,805 - app.services.agent.execution.task_runner - INFO - [TaskRunner] continue_writing 执行成功（DeepAgent模式）
2025-12-25 12:56:23,805 - app.api.v1.agent - INFO - [Stream] 任务完成: 改写浑圆桩的描写，使其更加生动 (25.7s)
2025-12-25 12:56:23,806 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务2完成
2025-12-25 12:56:23,807 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共2个任务，耗时: 25.78s
2025-12-25 12:56:23,807 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2025-12-25 12:56:23,808 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=1, 展示型=1
2025-12-25 12:56:23,808 - app.services.agent.langgraph_agent - INFO - [Response] 单个创作任务(continue_writing_tool)，输出858字符，直接返回（跳过AI调用）
2025-12-25 12:56:24,934 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:f141c5ed-0a75-4429-ba2a-912c74d167a3 | 重要度=0.65
2025-12-25 12:56:26,159 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:f141c5ed-0a75-4429-ba2a-912c74d167a3 | 重要度=0.60
2025-12-25 12:56:26,166 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:2284c23b-55c1-4e7b-98fc-66db3c2f512a, token=1200
2025-12-25 12:56:26,168 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:2284c23b-55c1-4e7b-98fc-66db3c2f512a, 消息数=2, Token=1200
2025-12-25 12:56:26,169 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:2284c23b-55c1-4e7b-98fc-66db3c2f512a)
2025-12-25 12:56:26,169 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2025-12-25 12:56:26,176 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed
2025-12-25 12:56:32,140 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:54984 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2025-12-25 12:56:32,146 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/3749ebb4-a2d6-4ab8-aa14-cf6c26611fc0/unread-info
INFO:     127.0.0.1:54985 - "GET /api/v1/channels/3749ebb4-a2d6-4ab8-aa14-cf6c26611fc0/unread-info HTTP/1.1" 200 OK
2025-12-25 12:56:33,933 - app.api.v1.ai - INFO - [预加载元数据] 用户: 2072855200@qq.com(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: f141c5ed-0a75-4429-ba2a-912c74d167a3, chapter_id: f191ba48-5d94-41bb-a94e-33257003ae93
2025-12-25 12:56:33,938 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: f191ba48-5d94-41bb-a94e-33257003ae93
2025-12-25 12:56:33,939 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: 1cb73820-a951-48f1-8d81-7dced6d8d278
2025-12-25 12:56:33,940 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2025-12-25 12:56:33,941 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:60038 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2025-12-25 12:56:33,979 - app.api.v1.ai - INFO - [预加载元数据] 用户: 2072855200@qq.com(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: f141c5ed-0a75-4429-ba2a-912c74d167a3, chapter_id: f191ba48-5d94-41bb-a94e-33257003ae93
2025-12-25 12:56:33,989 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: f191ba48-5d94-41bb-a94e-33257003ae93
2025-12-25 12:56:33,993 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: 1cb73820-a951-48f1-8d81-7dced6d8d278
2025-12-25 12:56:33,994 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2025-12-25 12:56:33,995 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:52322 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2025-12-25 12:56:34,111 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:f141c5ed-0a75-4429-ba2a-912c74d167a3
2025-12-25 12:56:34,112 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/f191ba48-5d94-41bb-a94e-33257003ae93
INFO:     127.0.0.1:52892 - "PUT /api/v1/chapters/f191ba48-5d94-41bb-a94e-33257003ae93 HTTP/1.1" 200 OK
2025-12-25 12:56:34,113 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第3章 一夕千悟 (order=3)
2025-12-25 12:56:34,700 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第3章 一夕千悟 (6 chunks)
2025-12-25 12:56:34,741 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:f141c5ed-0a75-4429-ba2a-912c74d167a3
2025-12-25 12:56:34,742 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/f191ba48-5d94-41bb-a94e-33257003ae93
INFO:     127.0.0.1:59717 - "PUT /api/v1/chapters/f191ba48-5d94-41bb-a94e-33257003ae93 HTTP/1.1" 200 OK
2025-12-25 12:56:34,743 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第3章 一夕千悟 (order=3)
2025-12-25 12:56:35,274 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第3章 一夕千悟 (6 chunks)
2025-12-25 12:56:36,919 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:63393 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2025-12-25 12:56:39,989 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:61456 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2025-12-25 12:56:40,005 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2025-12-25 12:56:40,006 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2025-12-25 12:56:40,007 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2025-12-25 12:56:41,771 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2025-12-25 12:56:41,772 - app.api.v1.agent - INFO - [Chat Stream] Mode: planning
2025-12-25 12:56:41,776 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:55878 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2025-12-25 12:56:41,784 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 找到段融吞噬器灵的片段，帮我润色一下语言...
2025-12-25 12:56:41,785 - app.api.v1.agent - INFO - [agent_chat_stream] 📥 收到的 context 字段:
2025-12-25 12:56:41,786 - app.api.v1.agent - INFO -   - selected_text: N/A...
2025-12-25 12:56:41,787 - app.api.v1.agent - INFO -   - selection_position: N/A
2025-12-25 12:56:41,787 - app.api.v1.agent - INFO -   - chapter_context: 当前章节ID: f191ba48-5d94-41bb-a94e-33257003ae93...
2025-12-25 12:56:41,787 - app.api.v1.agent - INFO -   - instruction_context: N/A...
2025-12-25 12:56:41,788 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:aa34dbf8-2e07-4c2e-9675-8eb918f93eda (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=f141c5ed-0a75-4429-ba2a-912c74d167a3, conversation_id=aa34dbf8-2e07-4c2e-9675-8eb918f93eda)
2025-12-25 12:56:41,793 - app.services.context.manager - INFO - [ContextManager] 创建新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:aa34dbf8-2e07-4c2e-9675-8eb918f93eda
2025-12-25 12:56:41,794 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:aa34dbf8-2e07-4c2e-9675-8eb918f93eda: 0/16000 tokens
2025-12-25 12:56:41,903 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='找到段融吞噬器灵的片段，帮我润色一下语言...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:f141c5ed-0a75-4429-ba2a-912c74d167a3', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=3条
2025-12-25 12:56:41,905 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=f141c5ed-0a75-4429-ba2a-912c74d167a3 | 含用户级=True | 找到=3条
2025-12-25 12:56:41,907 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 1条消息, 0 tokens, 耗时 117.73ms
2025-12-25 12:56:41,908 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 1 条历史消息 (token: 0)
2025-12-25 12:56:41,909 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 找到段融吞噬器灵的片段，帮我润色一下语言...
2025-12-25 12:56:41,912 - app.core.cache - INFO - ✅ 缓存命中: prompt:planning:v2.12.0:get_planning_static_prompt:fca6eb91156619d0
2025-12-25 12:56:41,920 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2025-12-25 12:56:41,920 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=simple_qa, complexity=simple, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro, reason=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
2025-12-25 12:56:41,921 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=2000, temp=0.3, task_type=TaskType.SIMPLE_QA
2025-12-25 12:56:44,077 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-12-25 12:56:45,037 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 12 个数据块，总长度: 832
2025-12-25 12:56:45,040 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 4860 (prompt=4449, completion=411)
2025-12-25 12:56:45,041 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2025-12-25 12:56:45,042 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2025-12-25 12:56:45,081 - app.services.ai.http_ai_service - INFO - [积分扣除] 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456: 扣除 7.56 积分, 余额: 53522.51 → 53514.95
2025-12-25 12:56:45,083 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4860, cost=$0.000609, time=3121ms
2025-12-25 12:56:45,084 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=4860
2025-12-25 12:56:45,085 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户希望找到“段融吞噬器灵”的片段，并对找到的片段进行语言润, 原料=需要查找作品中与“段融吞噬器灵”相关的片, 处理=首先使用`search_analysis
2025-12-25 12:56:45,085 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共2个任务
2025-12-25 12:56:45,086 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共2个任务，耗时: 3.18s
2025-12-25 12:56:45,087 - app.api.v1.agent - INFO - [Stream] Plan tasks: 2 items
2025-12-25 12:56:45,088 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2025-12-25 12:56:45,088 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2025-12-25 12:56:45,089 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2025-12-25 12:56:45,092 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 任务分组: 第一层并行=2, 第二层并行=0, 串行=0
2025-12-25 12:56:45,094 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始第一层并行执行2个任务
2025-12-25 12:56:45,096 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务1开始: 查找包含“段融吞噬器灵”的片段
2025-12-25 12:56:45,097 - app.api.v1.agent - INFO - [Stream] Task started: 查找包含“段融吞噬器灵”的片段
2025-12-25 12:56:45,098 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(search_analysis_fragments)
2025-12-25 12:56:45,099 - app.services.agent.tools.tool_types - INFO - [search_analysis_fragments] 开始执行工具
2025-12-25 12:56:45,102 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务2开始: 润色找到的片段
2025-12-25 12:56:45,104 - app.api.v1.agent - INFO - [Stream] Task started: 润色找到的片段
2025-12-25 12:56:45,105 - app.services.agent.execution.task_runner - INFO - [TaskRunner] analyze_text_tool 的 text 参数为空或含占位符，使用 context 兜底（27字符）
2025-12-25 12:56:45,106 - app.services.agent.execution.task_runner - INFO - [TaskRunner] analyze_text_tool 使用 focus: '润色这段文字，使其语言更生动、更具冲击力，突出吞噬器灵的场景感和力量感。...'
2025-12-25 12:56:45,108 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(analyze_text)
2025-12-25 12:56:45,109 - app.services.agent.tools.tool_types - INFO - [analyze_text] 开始执行工具
2025-12-25 12:56:45,110 - app.services.agent.tools.analysis_tools - INFO - [analyze_text_tool] 尝试第 1 次调用，config={'temperature': 0.3, 'task_type': <TaskType.SUMMARIZATION: 'summarization'>}
2025-12-25 12:56:46,826 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=f141c5ed-0a75-4429-ba2a-912c74d167a3, current_order=3, query=段融吞噬器灵...
2025-12-25 12:56:47,040 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2025-12-25 12:56:47,042 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2025-12-25 12:56:47,042 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
2025-12-25 12:56:47,057 - app.services.chapter_vector_service - INFO - RAG retrieved 10 segments within order<=5
Building prefix dict from the default dictionary ...
2025-12-25 12:56:47,059 - jieba - DEBUG - Building prefix dict from the default dictionary ...
Dumping model to file cache D:\Temp\jieba.cache
2025-12-25 12:56:48,585 - jieba - DEBUG - Dumping model to file cache D:\Temp\jieba.cache
Loading model cost 1.675 seconds.
2025-12-25 12:56:48,735 - jieba - DEBUG - Loading model cost 1.675 seconds.
Prefix dict has been built successfully.
2025-12-25 12:56:48,736 - jieba - DEBUG - Prefix dict has been built successfully.
2025-12-25 12:56:48,747 - app.services.agent.langgraph_tools - INFO - [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
2025-12-25 12:56:48,750 - app.services.agent.tools.tool_types - INFO - [search_analysis_fragments] 执行成功 (耗时: 3.650s)
2025-12-25 12:56:48,751 - app.services.agent.execution.task_runner - INFO - [TaskRunner] search_analysis_fragments 执行成功（DeepAgent模式）
2025-12-25 12:56:48,752 - app.api.v1.agent - INFO - [Stream] 任务完成: 查找包含“段融吞噬器灵”的片段 (3.7s)
2025-12-25 12:56:48,752 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务1完成
2025-12-25 12:56:51,162 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-12-25 12:56:54,145 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 12 个数据块，总长度: 764
2025-12-25 12:56:54,146 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 1558 (prompt=996, completion=562)
2025-12-25 12:56:54,148 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2025-12-25 12:56:54,149 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2025-12-25 12:56:54,178 - app.services.ai.http_ai_service - INFO - [积分扣除] 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456: 扣除 21.13 积分, 余额: 53514.95 → 53493.82
2025-12-25 12:56:54,178 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1558, cost=$0.001704, time=7108ms
2025-12-25 12:56:54,180 - app.services.agent.tools.analysis_tools - INFO - [analyze_text_tool] 第 1 次调用成功
2025-12-25 12:56:54,182 - app.services.agent.tools.analysis_tools - INFO - [analyze_text_tool] 分析完成，结果长度: 764
2025-12-25 12:56:54,182 - app.services.agent.tools.tool_types - INFO - [analyze_text] 执行成功 (耗时: 9.073s)
2025-12-25 12:56:54,182 - app.services.agent.execution.task_runner - INFO - [TaskRunner] analyze_text 执行成功（DeepAgent模式）
2025-12-25 12:56:54,182 - app.api.v1.agent - INFO - [Stream] 任务完成: 润色找到的片段 (9.1s)
2025-12-25 12:56:54,182 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务2完成
2025-12-25 12:56:54,182 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共2个任务，耗时: 9.09s
2025-12-25 12:56:54,182 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2025-12-25 12:56:54,182 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=1, 输出型=1, 展示型=0
2025-12-25 12:56:54,182 - app.services.agent.langgraph_agent - INFO - [Response] 单个分析任务(analyze_text_tool)，使用AI格式化
2025-12-25 12:56:54,182 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2025-12-25 12:56:54,182 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=4168字符, 处理后=4195字符
2025-12-25 12:56:54,182 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2025-12-25 12:56:54,188 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2025-12-25 12:56:54,205 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2025-12-25 12:56:54,205 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2025-12-25 12:56:54,209 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
2025-12-25 12:57:06,197 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-12-25 12:57:09,489 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 14 个数据块，总长度: 1190
2025-12-25 12:57:09,490 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 5654 (prompt=4753, completion=901)
2025-12-25 12:57:09,492 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2025-12-25 12:57:09,492 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2025-12-25 12:57:09,512 - app.services.ai.http_ai_service - INFO - [积分扣除] 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456: 扣除 45.61 积分, 余额: 53493.82 → 53448.21
2025-12-25 12:57:09,515 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=5654, cost=$0.003678, time=15284ms
2025-12-25 12:57:09,516 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=1190
2025-12-25 12:57:10,842 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:f141c5ed-0a75-4429-ba2a-912c74d167a3 | 重要度=0.65
2025-12-25 12:57:12,304 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:f141c5ed-0a75-4429-ba2a-912c74d167a3 | 重要度=0.73
2025-12-25 12:57:12,309 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:aa34dbf8-2e07-4c2e-9675-8eb918f93eda, token=1447
2025-12-25 12:57:12,311 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:aa34dbf8-2e07-4c2e-9675-8eb918f93eda, 消息数=2, Token=1447
2025-12-25 12:57:12,311 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:aa34dbf8-2e07-4c2e-9675-8eb918f93eda)
2025-12-25 12:57:12,312 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2025-12-25 12:57:12,315 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed
2025-12-25 12:57:32,137 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:58701 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2025-12-25 12:57:32,150 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/3749ebb4-a2d6-4ab8-aa14-cf6c26611fc0/unread-info
INFO:     127.0.0.1:53796 - "GET /api/v1/channels/3749ebb4-a2d6-4ab8-aa14-cf6c26611fc0/unread-info HTTP/1.1" 200 OK
2025-12-25 12:57:55,749 - app.api.v1.ai - INFO - [预加载元数据] 用户: 2072855200@qq.com(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: f141c5ed-0a75-4429-ba2a-912c74d167a3, chapter_id: 3d3c8ed2-78ab-4e75-bb90-c79e1b446040
2025-12-25 12:57:55,758 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 3d3c8ed2-78ab-4e75-bb90-c79e1b446040
2025-12-25 12:57:55,760 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: f191ba48-5d94-41bb-a94e-33257003ae93
2025-12-25 12:57:55,760 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2025-12-25 12:57:55,763 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:51784 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2025-12-25 12:57:55,808 - app.api.v1.ai - INFO - [预加载元数据] 用户: 2072855200@qq.com(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: f141c5ed-0a75-4429-ba2a-912c74d167a3, chapter_id: 3d3c8ed2-78ab-4e75-bb90-c79e1b446040
2025-12-25 12:57:55,814 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 3d3c8ed2-78ab-4e75-bb90-c79e1b446040
2025-12-25 12:57:55,817 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: f191ba48-5d94-41bb-a94e-33257003ae93
2025-12-25 12:57:55,817 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2025-12-25 12:57:55,820 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:52835 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2025-12-25 12:57:55,948 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:52836 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2025-12-25 12:57:56,001 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:f141c5ed-0a75-4429-ba2a-912c74d167a3
2025-12-25 12:57:56,002 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/3d3c8ed2-78ab-4e75-bb90-c79e1b446040
INFO:     127.0.0.1:65207 - "PUT /api/v1/chapters/3d3c8ed2-78ab-4e75-bb90-c79e1b446040 HTTP/1.1" 200 OK
2025-12-25 12:57:56,004 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第4章 家底 (order=4)
2025-12-25 12:57:56,580 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第4章 家底 (6 chunks)
2025-12-25 12:57:56,618 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:f141c5ed-0a75-4429-ba2a-912c74d167a3
2025-12-25 12:57:56,619 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/3d3c8ed2-78ab-4e75-bb90-c79e1b446040
INFO:     127.0.0.1:62585 - "PUT /api/v1/chapters/3d3c8ed2-78ab-4e75-bb90-c79e1b446040 HTTP/1.1" 200 OK
2025-12-25 12:57:56,620 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第4章 家底 (order=4)
2025-12-25 12:57:57,180 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第4章 家底 (6 chunks)
2025-12-25 12:58:00,132 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:62182 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2025-12-25 12:58:00,149 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2025-12-25 12:58:00,149 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2025-12-25 12:58:00,149 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2025-12-25 12:58:01,792 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2025-12-25 12:58:01,795 - app.api.v1.agent - INFO - [Chat Stream] Mode: planning
2025-12-25 12:58:01,800 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:61471 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2025-12-25 12:58:01,821 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 帮我把赵穆的人物描写改得更有特色，让他显得更加老练...
2025-12-25 12:58:01,824 - app.api.v1.agent - INFO - [agent_chat_stream] 📥 收到的 context 字段:
2025-12-25 12:58:01,826 - app.api.v1.agent - INFO -   - selected_text: N/A...
2025-12-25 12:58:01,827 - app.api.v1.agent - INFO -   - selection_position: N/A
2025-12-25 12:58:01,828 - app.api.v1.agent - INFO -   - chapter_context: 当前章节ID: 3d3c8ed2-78ab-4e75-bb90-c79e1b446040...
2025-12-25 12:58:01,828 - app.api.v1.agent - INFO -   - instruction_context: N/A...
2025-12-25 12:58:01,830 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:2c0c4281-cdf8-4e88-9dde-e76c712c46aa (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=f141c5ed-0a75-4429-ba2a-912c74d167a3, conversation_id=2c0c4281-cdf8-4e88-9dde-e76c712c46aa)
2025-12-25 12:58:01,842 - app.services.context.manager - INFO - [ContextManager] 创建新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:2c0c4281-cdf8-4e88-9dde-e76c712c46aa
2025-12-25 12:58:01,842 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:2c0c4281-cdf8-4e88-9dde-e76c712c46aa: 0/16000 tokens
2025-12-25 12:58:01,967 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='帮我把赵穆的人物描写改得更有特色，让他显得更加老练...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:f141c5ed-0a75-4429-ba2a-912c74d167a3', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=3条
2025-12-25 12:58:01,967 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=f141c5ed-0a75-4429-ba2a-912c74d167a3 | 含用户级=True | 找到=3条
2025-12-25 12:58:01,969 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 1条消息, 0 tokens, 耗时 132.79ms
2025-12-25 12:58:01,973 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 1 条历史消息 (token: 0)
2025-12-25 12:58:01,976 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 帮我把赵穆的人物描写改得更有特色，让他显得更加老练...
2025-12-25 12:58:01,982 - app.core.cache - INFO - ✅ 缓存命中: prompt:planning:v2.12.0:get_planning_static_prompt:fca6eb91156619d0
2025-12-25 12:58:01,989 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2025-12-25 12:58:01,991 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=simple_qa, complexity=simple, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro, reason=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
2025-12-25 12:58:01,991 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=2000, temp=0.3, task_type=TaskType.SIMPLE_QA
2025-12-25 12:58:04,089 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-12-25 12:58:06,039 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 13 个数据块，总长度: 960
2025-12-25 12:58:06,040 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 4962 (prompt=4451, completion=511)
2025-12-25 12:58:06,042 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2025-12-25 12:58:06,043 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2025-12-25 12:58:06,078 - app.services.ai.http_ai_service - INFO - [积分扣除] 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456: 扣除 8.05 积分, 余额: 53448.21 → 53440.16
2025-12-25 12:58:06,079 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4962, cost=$0.000650, time=4052ms
2025-12-25 12:58:06,080 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=4962
2025-12-25 12:58:06,080 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户希望对赵穆的人物描写进行修改，使其更具特色和老练感。这需, 原料=需要获取当前章节（chapter_id:, 处理=首先使用 `read_chapter_t
2025-12-25 12:58:06,080 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共2个任务
2025-12-25 12:58:06,081 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共2个任务，耗时: 4.10s
2025-12-25 12:58:06,081 - app.api.v1.agent - INFO - [Stream] Plan tasks: 2 items
2025-12-25 12:58:06,081 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2025-12-25 12:58:06,082 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2025-12-25 12:58:06,082 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2025-12-25 12:58:06,082 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 任务分组: 第一层并行=1, 第二层并行=1, 串行=0
2025-12-25 12:58:06,083 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始第一层并行执行1个任务
2025-12-25 12:58:06,083 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务1开始: 读取当前章节的全部内容，为人物描写改写提供上下文。
2025-12-25 12:58:06,084 - app.api.v1.agent - INFO - [Stream] Task started: 读取当前章节的全部内容，为人物描写改写提供上下文。
2025-12-25 12:58:06,085 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(read_chapter)
2025-12-25 12:58:06,085 - app.services.agent.tools.tool_types - INFO - [read_chapter] 开始执行工具
2025-12-25 12:58:06,095 - app.services.agent.langgraph_tools - INFO - [read_chapter_tool] ✅ 读取章节成功: 第4章 家底
2025-12-25 12:58:06,098 - app.services.agent.tools.tool_types - INFO - [read_chapter] 执行成功 (耗时: 0.013s)
2025-12-25 12:58:06,099 - app.services.agent.execution.task_runner - INFO - [TaskRunner] read_chapter 执行成功（DeepAgent模式）
2025-12-25 12:58:06,099 - app.api.v1.agent - INFO - [Stream] 任务完成: 读取当前章节的全部内容，为人物描写改写提供上下文。 (0.0s)
2025-12-25 12:58:06,100 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务1完成
2025-12-25 12:58:06,101 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始第二层并行执行1个任务
2025-12-25 12:58:06,102 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第二层任务2开始: 分析赵穆的人物描写，并给出更具特色和老练感的改写建议。
2025-12-25 12:58:06,102 - app.api.v1.agent - INFO - [Stream] Task started: 分析赵穆的人物描写，并给出更具特色和老练感的改写建议。
2025-12-25 12:58:06,102 - app.services.agent.execution.task_runner - INFO - [TaskRunner] analyze_text_tool 使用 focus: '分析当前章节中对赵穆的人物描写，找出可以提升其“老练”和“特色”之处，并提供具体的改写建议，例如通过动作、语言、神态、心理活动等细节来展现其城府、经验和不凡之处...'
2025-12-25 12:58:06,103 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(analyze_text)
2025-12-25 12:58:06,103 - app.services.agent.tools.tool_types - INFO - [analyze_text] 开始执行工具
2025-12-25 12:58:06,104 - app.services.agent.tools.analysis_tools - INFO - [analyze_text_tool] 尝试第 1 次调用，config={'temperature': 0.3, 'task_type': <TaskType.SUMMARIZATION: 'summarization'>}
2025-12-25 12:58:06,113 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2025-12-25 12:58:06,114 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2025-12-25 12:58:06,115 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
2025-12-25 12:58:09,872 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-12-25 12:58:09,875 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 2 个数据块，总长度: 76
2025-12-25 12:58:09,876 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 3043 (prompt=2993, completion=50)
2025-12-25 12:58:09,877 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2025-12-25 12:58:09,878 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2025-12-25 12:58:09,904 - app.services.ai.http_ai_service - INFO - [积分扣除] 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456: 扣除 12.68 积分, 余额: 53440.16 → 53427.48
2025-12-25 12:58:09,906 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=3043, cost=$0.001023, time=3762ms
2025-12-25 12:58:09,907 - app.services.agent.tools.analysis_tools - INFO - [analyze_text_tool] 第 1 次调用成功
2025-12-25 12:58:09,908 - app.services.agent.tools.analysis_tools - INFO - [analyze_text_tool] 分析完成，结果长度: 76
2025-12-25 12:58:09,908 - app.services.agent.tools.tool_types - INFO - [analyze_text] 执行成功 (耗时: 3.804s)
2025-12-25 12:58:09,909 - app.services.agent.execution.task_runner - INFO - [TaskRunner] analyze_text 执行成功（DeepAgent模式）
2025-12-25 12:58:09,909 - app.api.v1.agent - INFO - [Stream] 任务完成: 分析赵穆的人物描写，并给出更具特色和老练感的改写建议。 (3.8s)
2025-12-25 12:58:09,909 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第二层任务2完成
2025-12-25 12:58:09,910 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共2个任务，耗时: 3.83s
2025-12-25 12:58:09,911 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2025-12-25 12:58:09,911 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=1, 展示型=1
2025-12-25 12:58:09,911 - app.services.agent.langgraph_agent - INFO - [Response] 单个分析任务(analyze_text_tool)，使用AI格式化
2025-12-25 12:58:09,912 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2025-12-25 12:58:09,912 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=2786字符, 处理后=2843字符
2025-12-25 12:58:09,912 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2025-12-25 12:58:09,913 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2025-12-25 12:58:09,925 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2025-12-25 12:58:09,926 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2025-12-25 12:58:09,927 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
2025-12-25 12:58:12,362 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-12-25 12:58:12,639 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 2 个数据块，总长度: 147
2025-12-25 12:58:12,648 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 2461 (prompt=2366, completion=95)
2025-12-25 12:58:12,648 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2025-12-25 12:58:12,649 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2025-12-25 12:58:12,678 - app.services.ai.http_ai_service - INFO - [积分扣除] 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456: 扣除 11.75 积分, 余额: 53427.48 → 53415.73
2025-12-25 12:58:12,678 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2461, cost=$0.000947, time=2721ms
2025-12-25 12:58:12,684 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=147
2025-12-25 12:58:14,121 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:f141c5ed-0a75-4429-ba2a-912c74d167a3 | 重要度=0.99
2025-12-25 12:58:15,482 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:f141c5ed-0a75-4429-ba2a-912c74d167a3 | 重要度=0.91
2025-12-25 12:58:15,485 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:2c0c4281-cdf8-4e88-9dde-e76c712c46aa, token=182
2025-12-25 12:58:15,486 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:2c0c4281-cdf8-4e88-9dde-e76c712c46aa, 消息数=2, Token=182
2025-12-25 12:58:15,487 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:2c0c4281-cdf8-4e88-9dde-e76c712c46aa)
2025-12-25 12:58:15,487 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2025-12-25 12:58:15,492 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed
2025-12-25 12:58:32,139 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
2025-12-25 12:58:32,141 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/3749ebb4-a2d6-4ab8-aa14-cf6c26611fc0/unread-info
INFO:     127.0.0.1:55325 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
INFO:     127.0.0.1:55326 - "GET /api/v1/channels/3749ebb4-a2d6-4ab8-aa14-cf6c26611fc0/unread-info HTTP/1.1" 200 OK
2025-12-25 12:58:39,693 - app.api.v1.ai - INFO - [预加载元数据] 用户: 2072855200@qq.com(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: f141c5ed-0a75-4429-ba2a-912c74d167a3, chapter_id: c0661752-e71b-48ad-8597-0957516a43fe
2025-12-25 12:58:39,697 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: c0661752-e71b-48ad-8597-0957516a43fe
2025-12-25 12:58:39,699 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: 3d3c8ed2-78ab-4e75-bb90-c79e1b446040
2025-12-25 12:58:39,700 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2025-12-25 12:58:39,702 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:54750 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2025-12-25 12:58:39,747 - app.api.v1.ai - INFO - [预加载元数据] 用户: 2072855200@qq.com(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: f141c5ed-0a75-4429-ba2a-912c74d167a3, chapter_id: c0661752-e71b-48ad-8597-0957516a43fe
2025-12-25 12:58:39,751 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: c0661752-e71b-48ad-8597-0957516a43fe
2025-12-25 12:58:39,753 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: 3d3c8ed2-78ab-4e75-bb90-c79e1b446040
2025-12-25 12:58:39,753 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2025-12-25 12:58:39,754 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:52179 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2025-12-25 12:58:39,894 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:f141c5ed-0a75-4429-ba2a-912c74d167a3
2025-12-25 12:58:39,896 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/c0661752-e71b-48ad-8597-0957516a43fe
INFO:     127.0.0.1:56298 - "PUT /api/v1/chapters/c0661752-e71b-48ad-8597-0957516a43fe HTTP/1.1" 200 OK
2025-12-25 12:58:39,898 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2025-12-25 12:58:40,453 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (6 chunks)
2025-12-25 12:58:40,492 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:f141c5ed-0a75-4429-ba2a-912c74d167a3
2025-12-25 12:58:40,494 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/c0661752-e71b-48ad-8597-0957516a43fe
INFO:     127.0.0.1:64508 - "PUT /api/v1/chapters/c0661752-e71b-48ad-8597-0957516a43fe HTTP/1.1" 200 OK
2025-12-25 12:58:40,495 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2025-12-25 12:58:41,089 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (6 chunks)
2025-12-25 12:58:43,885 - app.api.v1.ai - INFO - [预加载元数据] 用户: 2072855200@qq.com(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: f141c5ed-0a75-4429-ba2a-912c74d167a3, chapter_id: 3d3c8ed2-78ab-4e75-bb90-c79e1b446040
2025-12-25 12:58:43,891 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 3d3c8ed2-78ab-4e75-bb90-c79e1b446040
2025-12-25 12:58:43,894 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: f191ba48-5d94-41bb-a94e-33257003ae93
2025-12-25 12:58:43,895 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2025-12-25 12:58:43,897 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:60550 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2025-12-25 12:58:43,928 - app.api.v1.ai - INFO - [预加载元数据] 用户: 2072855200@qq.com(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: f141c5ed-0a75-4429-ba2a-912c74d167a3, chapter_id: 3d3c8ed2-78ab-4e75-bb90-c79e1b446040
2025-12-25 12:58:43,934 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 3d3c8ed2-78ab-4e75-bb90-c79e1b446040
2025-12-25 12:58:43,935 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: f191ba48-5d94-41bb-a94e-33257003ae93
2025-12-25 12:58:43,935 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2025-12-25 12:58:43,936 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:61919 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2025-12-25 12:58:44,037 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:f141c5ed-0a75-4429-ba2a-912c74d167a3
2025-12-25 12:58:44,038 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/3d3c8ed2-78ab-4e75-bb90-c79e1b446040
INFO:     127.0.0.1:55748 - "PUT /api/v1/chapters/3d3c8ed2-78ab-4e75-bb90-c79e1b446040 HTTP/1.1" 200 OK
2025-12-25 12:58:44,040 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第4章 家底 (order=4)
2025-12-25 12:58:44,590 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第4章 家底 (6 chunks)
2025-12-25 12:58:44,622 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:f141c5ed-0a75-4429-ba2a-912c74d167a3
2025-12-25 12:58:44,623 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/3d3c8ed2-78ab-4e75-bb90-c79e1b446040
INFO:     127.0.0.1:57783 - "PUT /api/v1/chapters/3d3c8ed2-78ab-4e75-bb90-c79e1b446040 HTTP/1.1" 200 OK
2025-12-25 12:58:44,624 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第4章 家底 (order=4)
2025-12-25 12:58:45,171 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第4章 家底 (6 chunks)
2025-12-25 12:59:22,180 - app.api.v1.ai - INFO - [预加载元数据] 用户: 2072855200@qq.com(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: f141c5ed-0a75-4429-ba2a-912c74d167a3, chapter_id: c0661752-e71b-48ad-8597-0957516a43fe
2025-12-25 12:59:22,186 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: c0661752-e71b-48ad-8597-0957516a43fe
2025-12-25 12:59:22,188 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: 3d3c8ed2-78ab-4e75-bb90-c79e1b446040
2025-12-25 12:59:22,189 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2025-12-25 12:59:22,191 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:50212 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2025-12-25 12:59:22,235 - app.api.v1.ai - INFO - [预加载元数据] 用户: 2072855200@qq.com(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: f141c5ed-0a75-4429-ba2a-912c74d167a3, chapter_id: c0661752-e71b-48ad-8597-0957516a43fe
2025-12-25 12:59:22,240 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: c0661752-e71b-48ad-8597-0957516a43fe
2025-12-25 12:59:22,242 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: 3d3c8ed2-78ab-4e75-bb90-c79e1b446040
2025-12-25 12:59:22,242 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2025-12-25 12:59:22,244 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:65004 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2025-12-25 12:59:22,383 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:f141c5ed-0a75-4429-ba2a-912c74d167a3
2025-12-25 12:59:22,385 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/c0661752-e71b-48ad-8597-0957516a43fe
INFO:     127.0.0.1:59236 - "PUT /api/v1/chapters/c0661752-e71b-48ad-8597-0957516a43fe HTTP/1.1" 200 OK
2025-12-25 12:59:22,386 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2025-12-25 12:59:22,956 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (6 chunks)
2025-12-25 12:59:22,998 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:f141c5ed-0a75-4429-ba2a-912c74d167a3
2025-12-25 12:59:23,001 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/c0661752-e71b-48ad-8597-0957516a43fe
INFO:     127.0.0.1:50845 - "PUT /api/v1/chapters/c0661752-e71b-48ad-8597-0957516a43fe HTTP/1.1" 200 OK
2025-12-25 12:59:23,002 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2025-12-25 12:59:23,558 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (6 chunks)
2025-12-25 12:59:24,243 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:63241 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2025-12-25 12:59:26,924 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:57518 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2025-12-25 12:59:26,940 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2025-12-25 12:59:26,941 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2025-12-25 12:59:26,941 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2025-12-25 12:59:28,722 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2025-12-25 12:59:28,724 - app.api.v1.agent - INFO - [Chat Stream] Mode: planning
2025-12-25 12:59:28,727 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:50918 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2025-12-25 12:59:28,740 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 这部小说的主角叫什么名字？...
2025-12-25 12:59:28,742 - app.api.v1.agent - INFO - [agent_chat_stream] 📥 收到的 context 字段:
2025-12-25 12:59:28,742 - app.api.v1.agent - INFO -   - selected_text: N/A...
2025-12-25 12:59:28,743 - app.api.v1.agent - INFO -   - selection_position: N/A
2025-12-25 12:59:28,743 - app.api.v1.agent - INFO -   - chapter_context: 当前章节ID: c0661752-e71b-48ad-8597-0957516a43fe...
2025-12-25 12:59:28,743 - app.api.v1.agent - INFO -   - instruction_context: N/A...
2025-12-25 12:59:28,745 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:6d53f074-d87b-4327-a648-82a8c6d0903b (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=f141c5ed-0a75-4429-ba2a-912c74d167a3, conversation_id=6d53f074-d87b-4327-a648-82a8c6d0903b)
2025-12-25 12:59:28,753 - app.services.context.manager - INFO - [ContextManager] 创建新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:6d53f074-d87b-4327-a648-82a8c6d0903b
2025-12-25 12:59:28,754 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:6d53f074-d87b-4327-a648-82a8c6d0903b: 0/16000 tokens
2025-12-25 12:59:28,850 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='这部小说的主角叫什么名字？...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:f141c5ed-0a75-4429-ba2a-912c74d167a3', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=3条
2025-12-25 12:59:28,851 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=f141c5ed-0a75-4429-ba2a-912c74d167a3 | 含用户级=True | 找到=3条
2025-12-25 12:59:28,851 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 1条消息, 0 tokens, 耗时 105.30ms
2025-12-25 12:59:28,851 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 1 条历史消息 (token: 0)
2025-12-25 12:59:28,852 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 这部小说的主角叫什么名字？...
2025-12-25 12:59:28,856 - app.core.cache - INFO - ✅ 缓存命中: prompt:planning:v2.12.0:get_planning_static_prompt:fca6eb91156619d0
2025-12-25 12:59:28,863 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2025-12-25 12:59:28,863 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=simple_qa, complexity=simple, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro, reason=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
2025-12-25 12:59:28,864 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=2000, temp=0.3, task_type=TaskType.SIMPLE_QA
2025-12-25 12:59:30,866 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-12-25 12:59:31,536 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 9 个数据块，总长度: 450
2025-12-25 12:59:31,536 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 4657 (prompt=4444, completion=213)
2025-12-25 12:59:31,538 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2025-12-25 12:59:31,538 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2025-12-25 12:59:31,557 - app.services.ai.http_ai_service - INFO - [积分扣除] 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456: 扣除 6.57 积分, 余额: 53415.73 → 53409.16
2025-12-25 12:59:31,559 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4657, cost=$0.000530, time=2674ms
2025-12-25 12:59:31,560 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=4657
2025-12-25 12:59:31,560 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户希望知道这部小说主角的名字，这是一个信息查询任务，需要从, 原料=需要作品的上下文信息，以便从中找到主角的, 处理=使用get_context_tool获取
2025-12-25 12:59:31,561 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共1个任务
2025-12-25 12:59:31,561 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共1个任务，耗时: 2.71s
2025-12-25 12:59:31,561 - app.api.v1.agent - INFO - [Stream] Plan tasks: 1 items
2025-12-25 12:59:31,562 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2025-12-25 12:59:31,562 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2025-12-25 12:59:31,562 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2025-12-25 12:59:31,562 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 任务分组: 第一层并行=1, 第二层并行=0, 串行=0
2025-12-25 12:59:31,563 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始第一层并行执行1个任务
2025-12-25 12:59:31,564 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务1开始: 获取作品上下文信息，查找主角名字
2025-12-25 12:59:31,564 - app.api.v1.agent - INFO - [Stream] Task started: 获取作品上下文信息，查找主角名字
2025-12-25 12:59:31,565 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(get_context)
2025-12-25 12:59:31,565 - app.services.agent.tools.tool_types - INFO - [get_context] 开始执行工具
2025-12-25 12:59:31,579 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=f141c5ed-0a75-4429-ba2a-912c74d167a3, current_order=5, query=作品背景、人物关系、情节发展、伏笔线索...
2025-12-25 12:59:31,669 - app.services.chapter_vector_service - INFO - RAG retrieved 5 segments within order<=5
2025-12-25 12:59:31,670 - app.services.agent.langgraph_tools - INFO - [get_context_tool] ✅ 获取上下文成功
2025-12-25 12:59:31,671 - app.services.agent.tools.tool_types - INFO - [get_context] 执行成功 (耗时: 0.106s)
2025-12-25 12:59:31,672 - app.services.agent.execution.task_runner - INFO - [TaskRunner] get_context 执行成功（DeepAgent模式）
2025-12-25 12:59:31,672 - app.api.v1.agent - INFO - [Stream] 任务完成: 获取作品上下文信息，查找主角名字 (0.1s)
2025-12-25 12:59:31,672 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务1完成
2025-12-25 12:59:31,673 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共1个任务，耗时: 0.11s
2025-12-25 12:59:31,673 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2025-12-25 12:59:31,674 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=1, 输出型=0, 展示型=0
2025-12-25 12:59:31,674 - app.services.agent.langgraph_agent - WARNING - [Response] 没有明确输出任务，使用AI整合
2025-12-25 12:59:31,675 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2025-12-25 12:59:31,675 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=4155字符, 处理后=4176字符
2025-12-25 12:59:31,676 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2025-12-25 12:59:31,676 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2025-12-25 12:59:31,682 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2025-12-25 12:59:31,683 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2025-12-25 12:59:31,683 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
2025-12-25 12:59:32,149 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/3749ebb4-a2d6-4ab8-aa14-cf6c26611fc0/unread-info
INFO:     127.0.0.1:51386 - "GET /api/v1/channels/3749ebb4-a2d6-4ab8-aa14-cf6c26611fc0/unread-info HTTP/1.1" 200 OK
2025-12-25 12:59:32,169 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:51385 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2025-12-25 12:59:33,626 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-12-25 12:59:33,627 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 1 个数据块，总长度: 15
2025-12-25 12:59:33,627 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 3323 (prompt=3313, completion=10)
2025-12-25 12:59:33,627 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2025-12-25 12:59:33,628 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2025-12-25 12:59:33,642 - app.services.ai.http_ai_service - INFO - [积分扣除] 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456: 扣除 12.63 积分, 余额: 53409.16 → 53396.53
2025-12-25 12:59:33,644 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=3323, cost=$0.001019, time=1945ms
2025-12-25 12:59:33,645 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=15
2025-12-25 12:59:35,084 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:f141c5ed-0a75-4429-ba2a-912c74d167a3 | 重要度=0.89
2025-12-25 12:59:36,609 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:f141c5ed-0a75-4429-ba2a-912c74d167a3 | 重要度=0.79
2025-12-25 12:59:36,613 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:6d53f074-d87b-4327-a648-82a8c6d0903b, token=31
2025-12-25 12:59:36,613 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:6d53f074-d87b-4327-a648-82a8c6d0903b, 消息数=2, Token=31
2025-12-25 12:59:36,614 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:6d53f074-d87b-4327-a648-82a8c6d0903b)
2025-12-25 12:59:36,614 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2025-12-25 12:59:36,618 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed
2025-12-25 12:59:48,588 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2025-12-25 12:59:48,589 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2025-12-25 12:59:48,590 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2025-12-25 12:59:50,396 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2025-12-25 12:59:50,399 - app.api.v1.agent - INFO - [Chat Stream] Mode: planning
2025-12-25 12:59:50,401 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:58508 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2025-12-25 12:59:50,413 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 他有什么特殊能力？...
2025-12-25 12:59:50,414 - app.api.v1.agent - INFO - [agent_chat_stream] 📥 收到的 context 字段:
2025-12-25 12:59:50,415 - app.api.v1.agent - INFO -   - selected_text: N/A...
2025-12-25 12:59:50,417 - app.api.v1.agent - INFO -   - selection_position: N/A
2025-12-25 12:59:50,418 - app.api.v1.agent - INFO -   - chapter_context: 当前章节ID: c0661752-e71b-48ad-8597-0957516a43fe...
2025-12-25 12:59:50,418 - app.api.v1.agent - INFO -   - instruction_context: N/A...
2025-12-25 12:59:50,420 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:6d53f074-d87b-4327-a648-82a8c6d0903b (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=f141c5ed-0a75-4429-ba2a-912c74d167a3, conversation_id=6d53f074-d87b-4327-a648-82a8c6d0903b)
2025-12-25 12:59:50,424 - app.services.context.store - INFO - [ContextStore] 加载上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:6d53f074-d87b-4327-a648-82a8c6d0903b, 2条消息
2025-12-25 12:59:50,425 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:6d53f074-d87b-4327-a648-82a8c6d0903b: 31/16000 tokens
2025-12-25 12:59:50,528 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='他有什么特殊能力？...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:f141c5ed-0a75-4429-ba2a-912c74d167a3', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=3条
2025-12-25 12:59:50,528 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=f141c5ed-0a75-4429-ba2a-912c74d167a3 | 含用户级=True | 找到=3条
2025-12-25 12:59:50,529 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 3条消息, 31 tokens, 耗时 108.64ms
2025-12-25 12:59:50,529 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 3 条历史消息 (token: 31)
2025-12-25 12:59:50,530 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 他有什么特殊能力？...
2025-12-25 12:59:50,534 - app.core.cache - INFO - ✅ 缓存命中: prompt:planning:v2.12.0:get_planning_static_prompt:fca6eb91156619d0
2025-12-25 12:59:50,542 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2025-12-25 12:59:50,543 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=simple_qa, complexity=simple, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro, reason=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
2025-12-25 12:59:50,544 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=2000, temp=0.3, task_type=TaskType.SIMPLE_QA
2025-12-25 12:59:52,608 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-12-25 12:59:53,521 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 10 个数据块，总长度: 724
2025-12-25 12:59:53,523 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 4794 (prompt=4471, completion=323)
2025-12-25 12:59:53,524 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2025-12-25 12:59:53,524 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2025-12-25 12:59:53,552 - app.services.ai.http_ai_service - INFO - [积分扣除] 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456: 扣除 7.15 积分, 余额: 53396.53 → 53389.38
2025-12-25 12:59:53,553 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4794, cost=$0.000576, time=2979ms
2025-12-25 12:59:53,554 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=4794
2025-12-25 12:59:53,554 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户想了解主角段融的特殊能力，需要分析现有文本来回答。, 原料=需要获取包含主角段融能力描述的文本内容。, 处理=使用 search_analysis_f
2025-12-25 12:59:53,555 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共2个任务
2025-12-25 12:59:53,555 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共2个任务，耗时: 3.03s
2025-12-25 12:59:53,556 - app.api.v1.agent - INFO - [Stream] Plan tasks: 2 items
2025-12-25 12:59:53,556 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2025-12-25 12:59:53,557 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2025-12-25 12:59:53,557 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2025-12-25 12:59:53,557 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 任务分组: 第一层并行=1, 第二层并行=1, 串行=0
2025-12-25 12:59:53,558 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始第一层并行执行1个任务
2025-12-25 12:59:53,558 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务1开始: 搜索关于段融特殊能力的内容
2025-12-25 12:59:53,559 - app.api.v1.agent - INFO - [Stream] Task started: 搜索关于段融特殊能力的内容
2025-12-25 12:59:53,559 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(search_analysis_fragments)
2025-12-25 12:59:53,560 - app.services.agent.tools.tool_types - INFO - [search_analysis_fragments] 开始执行工具
2025-12-25 12:59:53,569 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=f141c5ed-0a75-4429-ba2a-912c74d167a3, current_order=5, query=段融 特殊能力...
2025-12-25 12:59:53,695 - app.services.chapter_vector_service - INFO - RAG retrieved 10 segments within order<=7
2025-12-25 12:59:53,700 - app.services.agent.langgraph_tools - INFO - [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
2025-12-25 12:59:53,702 - app.services.agent.tools.tool_types - INFO - [search_analysis_fragments] 执行成功 (耗时: 0.142s)
2025-12-25 12:59:53,702 - app.services.agent.execution.task_runner - INFO - [TaskRunner] search_analysis_fragments 执行成功（DeepAgent模式）
2025-12-25 12:59:53,702 - app.api.v1.agent - INFO - [Stream] 任务完成: 搜索关于段融特殊能力的内容 (0.1s)
2025-12-25 12:59:53,703 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务1完成
2025-12-25 12:59:53,703 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始第二层并行执行1个任务
2025-12-25 12:59:53,704 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第二层任务2开始: 分析搜索到的内容，提取段融的特殊能力
2025-12-25 12:59:53,704 - app.api.v1.agent - INFO - [Stream] Task started: 分析搜索到的内容，提取段融的特殊能力
2025-12-25 12:59:53,704 - app.services.agent.execution.task_runner - INFO - [TaskRunner] analyze_text_tool 使用 focus: '总结主角段融的特殊能力...'
2025-12-25 12:59:53,704 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(analyze_text)
2025-12-25 12:59:53,705 - app.services.agent.tools.tool_types - INFO - [analyze_text] 开始执行工具
2025-12-25 12:59:53,705 - app.services.agent.tools.analysis_tools - INFO - [analyze_text_tool] 尝试第 1 次调用，config={'temperature': 0.3, 'task_type': <TaskType.SUMMARIZATION: 'summarization'>}
2025-12-25 12:59:53,718 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2025-12-25 12:59:53,718 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2025-12-25 12:59:53,718 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
2025-12-25 12:59:59,662 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-12-25 13:00:01,083 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 4 个数据块，总长度: 349
2025-12-25 13:00:01,084 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 2176 (prompt=1937, completion=239)
2025-12-25 13:00:01,085 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2025-12-25 13:00:01,085 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2025-12-25 13:00:01,135 - app.services.ai.http_ai_service - INFO - [积分扣除] 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456: 扣除 14.61 积分, 余额: 53389.38 → 53374.77
2025-12-25 13:00:01,143 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2176, cost=$0.001179, time=7367ms
2025-12-25 13:00:01,143 - app.services.agent.tools.analysis_tools - INFO - [analyze_text_tool] 第 1 次调用成功
2025-12-25 13:00:01,144 - app.services.agent.tools.analysis_tools - INFO - [analyze_text_tool] 分析完成，结果长度: 349
2025-12-25 13:00:01,144 - app.services.agent.tools.tool_types - INFO - [analyze_text] 执行成功 (耗时: 7.439s)
2025-12-25 13:00:01,144 - app.services.agent.execution.task_runner - INFO - [TaskRunner] analyze_text 执行成功（DeepAgent模式）
2025-12-25 13:00:01,145 - app.api.v1.agent - INFO - [Stream] 任务完成: 分析搜索到的内容，提取段融的特殊能力 (7.4s)
2025-12-25 13:00:01,146 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第二层任务2完成
2025-12-25 13:00:01,146 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共2个任务，耗时: 7.59s
2025-12-25 13:00:01,147 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2025-12-25 13:00:01,148 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=1, 输出型=1, 展示型=0
2025-12-25 13:00:01,150 - app.services.agent.langgraph_agent - INFO - [Response] 单个分析任务(analyze_text_tool)，使用AI格式化
2025-12-25 13:00:01,150 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2025-12-25 13:00:01,151 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=2125字符, 处理后=2161字符
2025-12-25 13:00:01,152 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2025-12-25 13:00:01,152 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2025-12-25 13:00:01,162 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2025-12-25 13:00:01,162 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2025-12-25 13:00:01,163 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
2025-12-25 13:00:03,859 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-12-25 13:00:04,549 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 6 个数据块，总长度: 358
2025-12-25 13:00:04,551 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 2083 (prompt=1835, completion=248)
2025-12-25 13:00:04,551 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2025-12-25 13:00:04,551 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2025-12-25 13:00:04,578 - app.services.ai.http_ai_service - INFO - [积分扣除] 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456: 扣除 14.51 积分, 余额: 53374.77 → 53360.26
2025-12-25 13:00:04,582 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2083, cost=$0.001171, time=3389ms
2025-12-25 13:00:04,585 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=358
2025-12-25 13:00:06,023 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:f141c5ed-0a75-4429-ba2a-912c74d167a3 | 重要度=0.70
2025-12-25 13:00:06,030 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:6d53f074-d87b-4327-a648-82a8c6d0903b, token=451
2025-12-25 13:00:06,032 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:6d53f074-d87b-4327-a648-82a8c6d0903b, 消息数=4, Token=451
2025-12-25 13:00:06,032 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:6d53f074-d87b-4327-a648-82a8c6d0903b)
2025-12-25 13:00:06,032 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2025-12-25 13:00:06,039 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed
2025-12-25 13:00:32,142 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:54389 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2025-12-25 13:00:32,148 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/3749ebb4-a2d6-4ab8-aa14-cf6c26611fc0/unread-info
INFO:     127.0.0.1:54391 - "GET /api/v1/channels/3749ebb4-a2d6-4ab8-aa14-cf6c26611fc0/unread-info HTTP/1.1" 200 OK
2025-12-25 13:00:32,800 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2025-12-25 13:00:32,801 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2025-12-25 13:00:32,802 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2025-12-25 13:00:34,483 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2025-12-25 13:00:34,486 - app.api.v1.agent - INFO - [Chat Stream] Mode: planning
2025-12-25 13:00:34,489 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:55399 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2025-12-25 13:00:34,499 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 帮我给他设计一个新的器灵吞噬场景...
2025-12-25 13:00:34,500 - app.api.v1.agent - INFO - [agent_chat_stream] 📥 收到的 context 字段:
2025-12-25 13:00:34,501 - app.api.v1.agent - INFO -   - selected_text: N/A...
2025-12-25 13:00:34,501 - app.api.v1.agent - INFO -   - selection_position: N/A
2025-12-25 13:00:34,502 - app.api.v1.agent - INFO -   - chapter_context: 当前章节ID: c0661752-e71b-48ad-8597-0957516a43fe...
2025-12-25 13:00:34,502 - app.api.v1.agent - INFO -   - instruction_context: N/A...
2025-12-25 13:00:34,502 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:6d53f074-d87b-4327-a648-82a8c6d0903b (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=f141c5ed-0a75-4429-ba2a-912c74d167a3, conversation_id=6d53f074-d87b-4327-a648-82a8c6d0903b)
2025-12-25 13:00:34,510 - app.services.context.store - INFO - [ContextStore] 加载上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:6d53f074-d87b-4327-a648-82a8c6d0903b, 4条消息
2025-12-25 13:00:34,511 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:6d53f074-d87b-4327-a648-82a8c6d0903b: 451/16000 tokens
2025-12-25 13:00:34,630 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='帮我给他设计一个新的器灵吞噬场景...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:f141c5ed-0a75-4429-ba2a-912c74d167a3', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=3条
2025-12-25 13:00:34,631 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=f141c5ed-0a75-4429-ba2a-912c74d167a3 | 含用户级=True | 找到=3条
2025-12-25 13:00:34,632 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 5条消息, 451 tokens, 耗时 126.98ms
2025-12-25 13:00:34,633 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 5 条历史消息 (token: 451)
2025-12-25 13:00:34,633 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 帮我给他设计一个新的器灵吞噬场景...
2025-12-25 13:00:34,638 - app.core.cache - INFO - ✅ 缓存命中: prompt:planning:v2.12.0:get_planning_static_prompt:fca6eb91156619d0
2025-12-25 13:00:34,645 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2025-12-25 13:00:34,647 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=simple_qa, complexity=simple, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro, reason=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
2025-12-25 13:00:34,648 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=2000, temp=0.3, task_type=TaskType.SIMPLE_QA
2025-12-25 13:00:37,152 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-12-25 13:00:38,503 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 10 个数据块，总长度: 687
2025-12-25 13:00:38,509 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 5102 (prompt=4736, completion=366)
2025-12-25 13:00:38,509 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2025-12-25 13:00:38,510 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2025-12-25 13:00:38,553 - app.services.ai.http_ai_service - INFO - [积分扣除] 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456: 扣除 7.69 积分, 余额: 53360.26 → 53352.57
2025-12-25 13:00:38,556 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=5102, cost=$0.000620, time=3860ms
2025-12-25 13:00:38,557 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=5102
2025-12-25 13:00:38,557 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户希望我为主角段融设计一个新的器灵吞噬场景，这意味着需要创, 原料=需要了解段融的背景信息（已提供：能吞噬器, 处理=使用 `continue_writing
2025-12-25 13:00:38,558 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共1个任务
2025-12-25 13:00:38,558 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共1个任务，耗时: 3.92s
2025-12-25 13:00:38,559 - app.api.v1.agent - INFO - [Stream] Plan tasks: 1 items
2025-12-25 13:00:38,560 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2025-12-25 13:00:38,561 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2025-12-25 13:00:38,562 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2025-12-25 13:00:38,565 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 任务分组: 第一层并行=0, 第二层并行=0, 串行=1
2025-12-25 13:00:38,566 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始串行执行1个任务
2025-12-25 13:00:38,566 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务1开始: 创作一个新的器灵吞噬场景
2025-12-25 13:00:38,567 - app.api.v1.agent - INFO - [Stream] Task started: 创作一个新的器灵吞噬场景
2025-12-25 13:00:38,567 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(continue_writing)
2025-12-25 13:00:38,569 - app.services.agent.tools.tool_types - INFO - [continue_writing] 开始执行工具
2025-12-25 13:00:38,588 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2025-12-25 13:00:38,590 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=content_creation, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: content_creation; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2025-12-25 13:00:38,590 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=1000, temp=0.8, task_type=TaskType.CONTENT_CREATION
2025-12-25 13:00:57,207 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-12-25 13:00:59,411 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 5 个数据块，总长度: 387
2025-12-25 13:00:59,414 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 2436 (prompt=2112, completion=324)
2025-12-25 13:00:59,417 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2025-12-25 13:00:59,420 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2025-12-25 13:00:59,459 - app.services.ai.http_ai_service - INFO - [积分扣除] 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456: 扣除 72.91 积分, 余额: 53352.57 → 53279.66
2025-12-25 13:00:59,463 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2436, cost=$0.005880, time=20829ms
2025-12-25 13:00:59,464 - app.services.agent.tools.tool_types - INFO - [continue_writing] 执行成功 (耗时: 20.895s)
2025-12-25 13:00:59,466 - app.services.agent.execution.task_runner - INFO - [TaskRunner] continue_writing 执行成功（DeepAgent模式）
2025-12-25 13:00:59,466 - app.api.v1.agent - INFO - [Stream] 任务完成: 创作一个新的器灵吞噬场景 (20.9s)
2025-12-25 13:00:59,466 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务1完成
2025-12-25 13:00:59,467 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共1个任务，耗时: 20.91s
2025-12-25 13:00:59,467 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2025-12-25 13:00:59,468 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=1, 展示型=0
2025-12-25 13:00:59,468 - app.services.agent.langgraph_agent - INFO - [Response] 单个分析任务(continue_writing_tool)，使用AI格式化
2025-12-25 13:00:59,468 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2025-12-25 13:00:59,469 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=419字符, 处理后=436字符
2025-12-25 13:00:59,469 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2025-12-25 13:00:59,470 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2025-12-25 13:00:59,481 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2025-12-25 13:00:59,482 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2025-12-25 13:00:59,482 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
2025-12-25 13:01:01,375 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-12-25 13:01:02,375 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 6 个数据块，总长度: 406
2025-12-25 13:01:02,375 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 987 (prompt=651, completion=336)
2025-12-25 13:01:02,376 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2025-12-25 13:01:02,378 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2025-12-25 13:01:02,399 - app.services.ai.http_ai_service - INFO - [积分扣除] 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456: 扣除 12.84 积分, 余额: 53279.66 → 53266.82
2025-12-25 13:01:02,400 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=987, cost=$0.001035, time=2895ms
2025-12-25 13:01:02,401 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=406
2025-12-25 13:01:03,843 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:f141c5ed-0a75-4429-ba2a-912c74d167a3 | 重要度=0.51
2025-12-25 13:01:03,848 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:6d53f074-d87b-4327-a648-82a8c6d0903b, token=1063
2025-12-25 13:01:03,850 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:6d53f074-d87b-4327-a648-82a8c6d0903b, 消息数=6, Token=1063
2025-12-25 13:01:03,850 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:6d53f074-d87b-4327-a648-82a8c6d0903b)
2025-12-25 13:01:03,850 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2025-12-25 13:01:03,866 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed
2025-12-25 13:01:11,463 - app.api.v1.ai - INFO - [预加载元数据] 用户: 2072855200@qq.com(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: f141c5ed-0a75-4429-ba2a-912c74d167a3, chapter_id: c726baba-b01b-42ea-9c5d-0d2d5b221d94
2025-12-25 13:01:11,469 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: c726baba-b01b-42ea-9c5d-0d2d5b221d94
2025-12-25 13:01:11,469 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
2025-12-25 13:01:11,472 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:56434 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2025-12-25 13:01:11,517 - app.api.v1.ai - INFO - [预加载元数据] 用户: 2072855200@qq.com(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: f141c5ed-0a75-4429-ba2a-912c74d167a3, chapter_id: c726baba-b01b-42ea-9c5d-0d2d5b221d94
2025-12-25 13:01:11,520 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: c726baba-b01b-42ea-9c5d-0d2d5b221d94
2025-12-25 13:01:11,521 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
2025-12-25 13:01:11,522 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:56949 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2025-12-25 13:01:11,656 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:f141c5ed-0a75-4429-ba2a-912c74d167a3
2025-12-25 13:01:11,657 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/c726baba-b01b-42ea-9c5d-0d2d5b221d94
INFO:     127.0.0.1:52522 - "PUT /api/v1/chapters/c726baba-b01b-42ea-9c5d-0d2d5b221d94 HTTP/1.1" 200 OK
2025-12-25 13:01:11,659 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2025-12-25 13:01:12,383 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (7 chunks)
2025-12-25 13:01:12,424 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:f141c5ed-0a75-4429-ba2a-912c74d167a3
2025-12-25 13:01:12,426 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/c726baba-b01b-42ea-9c5d-0d2d5b221d94
INFO:     127.0.0.1:65249 - "PUT /api/v1/chapters/c726baba-b01b-42ea-9c5d-0d2d5b221d94 HTTP/1.1" 200 OK
2025-12-25 13:01:12,428 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2025-12-25 13:01:13,045 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (7 chunks)
2025-12-25 13:01:15,020 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:57066 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2025-12-25 13:01:17,109 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:62242 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2025-12-25 13:01:17,129 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2025-12-25 13:01:17,129 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2025-12-25 13:01:17,131 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2025-12-25 13:01:18,870 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2025-12-25 13:01:18,874 - app.api.v1.agent - INFO - [Chat Stream] Mode: planning
2025-12-25 13:01:18,878 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:61157 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2025-12-25 13:01:18,886 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 请先读取第1章内容，分析其中的人物关系，然后帮我写一段新的场景描写...
2025-12-25 13:01:18,887 - app.api.v1.agent - INFO - [agent_chat_stream] 📥 收到的 context 字段:
2025-12-25 13:01:18,888 - app.api.v1.agent - INFO -   - selected_text: N/A...
2025-12-25 13:01:18,888 - app.api.v1.agent - INFO -   - selection_position: N/A
2025-12-25 13:01:18,889 - app.api.v1.agent - INFO -   - chapter_context: 当前章节ID: c726baba-b01b-42ea-9c5d-0d2d5b221d94...
2025-12-25 13:01:18,890 - app.api.v1.agent - INFO -   - instruction_context: N/A...
2025-12-25 13:01:18,891 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:5d047ee2-6392-482e-9261-22cf6b3395bc (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=f141c5ed-0a75-4429-ba2a-912c74d167a3, conversation_id=5d047ee2-6392-482e-9261-22cf6b3395bc)
2025-12-25 13:01:18,895 - app.services.context.manager - INFO - [ContextManager] 创建新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:5d047ee2-6392-482e-9261-22cf6b3395bc
2025-12-25 13:01:18,896 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:5d047ee2-6392-482e-9261-22cf6b3395bc: 0/16000 tokens
2025-12-25 13:01:19,170 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='请先读取第1章内容，分析其中的人物关系，然后帮我写一段新的场...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:f141c5ed-0a75-4429-ba2a-912c74d167a3', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=3条
2025-12-25 13:01:19,174 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=f141c5ed-0a75-4429-ba2a-912c74d167a3 | 含用户级=True | 找到=3条
2025-12-25 13:01:19,174 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 1条消息, 0 tokens, 耗时 282.57ms
2025-12-25 13:01:19,175 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 1 条历史消息 (token: 0)
2025-12-25 13:01:19,175 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 请先读取第1章内容，分析其中的人物关系，然后帮我写一段新的场景描写...
2025-12-25 13:01:19,181 - app.core.cache - INFO - ✅ 缓存命中: prompt:planning:v2.12.0:get_planning_static_prompt:fca6eb91156619d0
2025-12-25 13:01:19,191 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2025-12-25 13:01:19,192 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=simple_qa, complexity=simple, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro, reason=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
2025-12-25 13:01:19,192 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=2000, temp=0.3, task_type=TaskType.SIMPLE_QA
2025-12-25 13:01:21,890 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-12-25 13:01:22,936 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 12 个数据块，总长度: 968
2025-12-25 13:01:22,936 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 4852 (prompt=4453, completion=399)
2025-12-25 13:01:22,936 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2025-12-25 13:01:22,936 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2025-12-25 13:01:22,960 - app.services.ai.http_ai_service - INFO - [积分扣除] 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456: 扣除 7.5 积分, 余额: 53266.82 → 53259.32
2025-12-25 13:01:22,963 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4852, cost=$0.000605, time=3745ms
2025-12-25 13:01:22,964 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=4852
2025-12-25 13:01:22,966 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户希望我先阅读第一章内容，然后分析其中的人物关系，最后根据, 原料=需要第一章的全部内容。, 处理=首先使用get_chapter_by_o
2025-12-25 13:01:22,966 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共3个任务
2025-12-25 13:01:22,967 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共3个任务，耗时: 3.79s
2025-12-25 13:01:22,967 - app.api.v1.agent - INFO - [Stream] Plan tasks: 3 items
2025-12-25 13:01:22,968 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2025-12-25 13:01:22,968 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2025-12-25 13:01:22,969 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2025-12-25 13:01:22,972 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 任务分组: 第一层并行=1, 第二层并行=1, 串行=1
2025-12-25 13:01:22,974 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始第一层并行执行1个任务
2025-12-25 13:01:22,975 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务1开始: 获取第一章内容
2025-12-25 13:01:22,975 - app.api.v1.agent - INFO - [Stream] Task started: 获取第一章内容
2025-12-25 13:01:22,976 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(get_chapter_by_order)
2025-12-25 13:01:22,977 - app.services.agent.tools.tool_types - INFO - [get_chapter_by_order] 开始执行工具
2025-12-25 13:01:23,000 - app.services.agent.langgraph_tools - INFO - [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
2025-12-25 13:01:23,003 - app.services.agent.tools.tool_types - INFO - [get_chapter_by_order] 执行成功 (耗时: 0.025s)
2025-12-25 13:01:23,003 - app.services.agent.execution.task_runner - INFO - [TaskRunner] get_chapter_by_order 执行成功（DeepAgent模式）
2025-12-25 13:01:23,004 - app.api.v1.agent - INFO - [Stream] 任务完成: 获取第一章内容 (0.0s)
2025-12-25 13:01:23,004 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务1完成
2025-12-25 13:01:23,006 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始第二层并行执行1个任务
2025-12-25 13:01:23,007 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第二层任务2开始: 分析第一章的人物关系
2025-12-25 13:01:23,008 - app.api.v1.agent - INFO - [Stream] Task started: 分析第一章的人物关系
2025-12-25 13:01:23,009 - app.services.agent.execution.task_runner - INFO - [TaskRunner] analyze_text_tool 使用 focus: '分析第一章中的人物关系，包括主要人物、次要人物、他们之间的互动、情感联系和潜在冲突。...'
2025-12-25 13:01:23,009 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(analyze_text)
2025-12-25 13:01:23,011 - app.services.agent.tools.tool_types - INFO - [analyze_text] 开始执行工具
2025-12-25 13:01:23,012 - app.services.agent.tools.analysis_tools - INFO - [analyze_text_tool] 尝试第 1 次调用，config={'temperature': 0.3, 'task_type': <TaskType.SUMMARIZATION: 'summarization'>}
2025-12-25 13:01:23,023 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2025-12-25 13:01:23,023 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2025-12-25 13:01:23,024 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
2025-12-25 13:01:29,412 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-12-25 13:01:30,941 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 10 个数据块，总长度: 596
2025-12-25 13:01:30,942 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 3815 (prompt=3356, completion=459)
2025-12-25 13:01:30,944 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2025-12-25 13:01:30,944 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2025-12-25 13:01:30,978 - app.services.ai.http_ai_service - INFO - [积分扣除] 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456: 扣除 26.71 积分, 余额: 53259.32 → 53232.61
2025-12-25 13:01:30,980 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=3815, cost=$0.002154, time=7920ms
2025-12-25 13:01:30,982 - app.services.agent.tools.analysis_tools - INFO - [analyze_text_tool] 第 1 次调用成功
2025-12-25 13:01:30,984 - app.services.agent.tools.analysis_tools - INFO - [analyze_text_tool] 分析完成，结果长度: 596
2025-12-25 13:01:30,984 - app.services.agent.tools.tool_types - INFO - [analyze_text] 执行成功 (耗时: 7.973s)
2025-12-25 13:01:30,986 - app.services.agent.execution.task_runner - INFO - [TaskRunner] analyze_text 执行成功（DeepAgent模式）
2025-12-25 13:01:30,986 - app.api.v1.agent - INFO - [Stream] 任务完成: 分析第一章的人物关系 (8.0s)
2025-12-25 13:01:30,987 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第二层任务2完成
2025-12-25 13:01:30,989 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始串行执行1个任务
2025-12-25 13:01:30,991 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务3开始: 创作新的场景描写
2025-12-25 13:01:30,992 - app.api.v1.agent - INFO - [Stream] Task started: 创作新的场景描写
2025-12-25 13:01:30,994 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(continue_writing)
2025-12-25 13:01:30,995 - app.services.agent.tools.tool_types - INFO - [continue_writing] 开始执行工具
2025-12-25 13:01:31,015 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2025-12-25 13:01:31,016 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=content_creation, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: content_creation; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2025-12-25 13:01:31,017 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=1000, temp=0.8, task_type=TaskType.CONTENT_CREATION
2025-12-25 13:01:32,140 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:63932 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2025-12-25 13:01:32,150 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/3749ebb4-a2d6-4ab8-aa14-cf6c26611fc0/unread-info
INFO:     127.0.0.1:63933 - "GET /api/v1/channels/3749ebb4-a2d6-4ab8-aa14-cf6c26611fc0/unread-info HTTP/1.1" 200 OK
2025-12-25 13:01:50,767 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-12-25 13:01:53,166 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 6 个数据块，总长度: 418
2025-12-25 13:01:53,168 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 4776 (prompt=4432, completion=344)
2025-12-25 13:01:53,169 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2025-12-25 13:01:53,169 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2025-12-25 13:01:53,208 - app.services.ai.http_ai_service - INFO - [积分扣除] 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456: 扣除 111.35 积分, 余额: 53232.61 → 53121.26
2025-12-25 13:01:53,211 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4776, cost=$0.008980, time=22152ms
2025-12-25 13:01:53,213 - app.services.agent.tools.tool_types - INFO - [continue_writing] 执行成功 (耗时: 22.219s)
2025-12-25 13:01:53,214 - app.services.agent.execution.task_runner - INFO - [TaskRunner] continue_writing 执行成功（DeepAgent模式）
2025-12-25 13:01:53,216 - app.api.v1.agent - INFO - [Stream] 任务完成: 创作新的场景描写 (22.2s)
2025-12-25 13:01:53,216 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务3完成
2025-12-25 13:01:53,217 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共3个任务，耗时: 30.25s
2025-12-25 13:01:53,218 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2025-12-25 13:01:53,219 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=2, 展示型=1
2025-12-25 13:01:53,220 - app.services.agent.langgraph_agent - INFO - [Response] 2个输出任务，简单拼接
2025-12-25 13:01:54,414 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:f141c5ed-0a75-4429-ba2a-912c74d167a3 | 重要度=0.99
2025-12-25 13:01:55,806 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:f141c5ed-0a75-4429-ba2a-912c74d167a3 | 重要度=0.60
2025-12-25 13:01:55,813 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:5d047ee2-6392-482e-9261-22cf6b3395bc, token=1367
2025-12-25 13:01:55,814 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:5d047ee2-6392-482e-9261-22cf6b3395bc, 消息数=2, Token=1367
2025-12-25 13:01:55,814 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:5d047ee2-6392-482e-9261-22cf6b3395bc)
2025-12-25 13:01:55,816 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2025-12-25 13:01:55,821 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed
2025-12-25 13:02:13,488 - app.api.v1.ai - INFO - [预加载元数据] 用户: 2072855200@qq.com(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: f141c5ed-0a75-4429-ba2a-912c74d167a3, chapter_id: c0661752-e71b-48ad-8597-0957516a43fe
2025-12-25 13:02:13,494 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: c0661752-e71b-48ad-8597-0957516a43fe
2025-12-25 13:02:13,495 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: 3d3c8ed2-78ab-4e75-bb90-c79e1b446040
2025-12-25 13:02:13,496 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2025-12-25 13:02:13,498 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:61504 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2025-12-25 13:02:13,541 - app.api.v1.ai - INFO - [预加载元数据] 用户: 2072855200@qq.com(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: f141c5ed-0a75-4429-ba2a-912c74d167a3, chapter_id: c0661752-e71b-48ad-8597-0957516a43fe
2025-12-25 13:02:13,546 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: c0661752-e71b-48ad-8597-0957516a43fe
2025-12-25 13:02:13,548 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: 3d3c8ed2-78ab-4e75-bb90-c79e1b446040
2025-12-25 13:02:13,548 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2025-12-25 13:02:13,550 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:58965 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2025-12-25 13:02:13,680 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:f141c5ed-0a75-4429-ba2a-912c74d167a3
2025-12-25 13:02:13,681 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/c0661752-e71b-48ad-8597-0957516a43fe
INFO:     127.0.0.1:62184 - "PUT /api/v1/chapters/c0661752-e71b-48ad-8597-0957516a43fe HTTP/1.1" 200 OK
2025-12-25 13:02:13,683 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2025-12-25 13:02:14,290 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (6 chunks)
2025-12-25 13:02:14,335 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:f141c5ed-0a75-4429-ba2a-912c74d167a3
2025-12-25 13:02:14,338 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/c0661752-e71b-48ad-8597-0957516a43fe
INFO:     127.0.0.1:51331 - "PUT /api/v1/chapters/c0661752-e71b-48ad-8597-0957516a43fe HTTP/1.1" 200 OK
2025-12-25 13:02:14,343 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2025-12-25 13:02:14,961 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (6 chunks)
2025-12-25 13:02:16,416 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:65203 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2025-12-25 13:02:19,481 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:57498 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2025-12-25 13:02:19,501 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2025-12-25 13:02:19,503 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2025-12-25 13:02:19,503 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2025-12-25 13:02:21,250 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2025-12-25 13:02:21,257 - app.api.v1.agent - INFO - [Chat Stream] Mode: planning
2025-12-25 13:02:21,259 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:64007 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2025-12-25 13:02:21,270 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 帮我把这部小说的前5章都分析一遍，提取出主要的剧情脉络...
2025-12-25 13:02:21,272 - app.api.v1.agent - INFO - [agent_chat_stream] 📥 收到的 context 字段:
2025-12-25 13:02:21,274 - app.api.v1.agent - INFO -   - selected_text: N/A...
2025-12-25 13:02:21,275 - app.api.v1.agent - INFO -   - selection_position: N/A
2025-12-25 13:02:21,276 - app.api.v1.agent - INFO -   - chapter_context: 当前章节ID: c0661752-e71b-48ad-8597-0957516a43fe...
2025-12-25 13:02:21,276 - app.api.v1.agent - INFO -   - instruction_context: N/A...
2025-12-25 13:02:21,277 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:65024582-f3d1-40e6-9bcf-0af3a3e3dc4e (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=f141c5ed-0a75-4429-ba2a-912c74d167a3, conversation_id=65024582-f3d1-40e6-9bcf-0af3a3e3dc4e)
2025-12-25 13:02:21,283 - app.services.context.manager - INFO - [ContextManager] 创建新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:65024582-f3d1-40e6-9bcf-0af3a3e3dc4e
2025-12-25 13:02:21,283 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:65024582-f3d1-40e6-9bcf-0af3a3e3dc4e: 0/16000 tokens
2025-12-25 13:02:21,436 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='帮我把这部小说的前5章都分析一遍，提取出主要的剧情脉络...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:f141c5ed-0a75-4429-ba2a-912c74d167a3', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=3条
2025-12-25 13:02:21,439 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=f141c5ed-0a75-4429-ba2a-912c74d167a3 | 含用户级=True | 找到=3条
2025-12-25 13:02:21,440 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 1条消息, 0 tokens, 耗时 162.47ms
2025-12-25 13:02:21,440 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 1 条历史消息 (token: 0)
2025-12-25 13:02:21,440 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 帮我把这部小说的前5章都分析一遍，提取出主要的剧情脉络...
2025-12-25 13:02:21,446 - app.core.cache - INFO - ✅ 缓存命中: prompt:planning:v2.12.0:get_planning_static_prompt:fca6eb91156619d0
2025-12-25 13:02:21,456 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2025-12-25 13:02:21,457 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=simple_qa, complexity=simple, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro, reason=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
2025-12-25 13:02:21,458 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=2000, temp=0.3, task_type=TaskType.SIMPLE_QA
2025-12-25 13:02:23,765 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-12-25 13:02:25,101 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 14 个数据块，总长度: 1375
2025-12-25 13:02:25,102 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 5031 (prompt=4455, completion=576)
2025-12-25 13:02:25,103 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2025-12-25 13:02:25,105 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2025-12-25 13:02:25,142 - app.services.ai.http_ai_service - INFO - [积分扣除] 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456: 扣除 8.38 积分, 余额: 53121.26 → 53112.88
2025-12-25 13:02:25,145 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=5031, cost=$0.000676, time=3647ms
2025-12-25 13:02:25,148 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=5031
2025-12-25 13:02:25,148 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户希望对小说前5章进行分析，并提取出主要的剧情脉络。输出形, 原料=需要获取小说前5章的全部内容。, 处理=获取前5章内容后，使用analyze_t
2025-12-25 13:02:25,149 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共6个任务
2025-12-25 13:02:25,152 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共6个任务，耗时: 3.71s
2025-12-25 13:02:25,153 - app.api.v1.agent - INFO - [Stream] Plan tasks: 6 items
2025-12-25 13:02:25,153 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2025-12-25 13:02:25,153 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2025-12-25 13:02:25,154 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2025-12-25 13:02:25,156 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 任务分组: 第一层并行=5, 第二层并行=1, 串行=0
2025-12-25 13:02:25,159 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始第一层并行执行5个任务
2025-12-25 13:02:25,160 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务1开始: 获取第一章内容
2025-12-25 13:02:25,160 - app.api.v1.agent - INFO - [Stream] Task started: 获取第一章内容
2025-12-25 13:02:25,161 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(get_chapter_by_order)
2025-12-25 13:02:25,161 - app.services.agent.tools.tool_types - INFO - [get_chapter_by_order] 开始执行工具
2025-12-25 13:02:25,162 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务2开始: 获取第二章内容
2025-12-25 13:02:25,162 - app.api.v1.agent - INFO - [Stream] Task started: 获取第二章内容
2025-12-25 13:02:25,163 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(get_chapter_by_order)
2025-12-25 13:02:25,165 - app.services.agent.tools.tool_types - INFO - [get_chapter_by_order] 开始执行工具
2025-12-25 13:02:25,166 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务3开始: 获取第三章内容
2025-12-25 13:02:25,166 - app.api.v1.agent - INFO - [Stream] Task started: 获取第三章内容
2025-12-25 13:02:25,167 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(get_chapter_by_order)
2025-12-25 13:02:25,167 - app.services.agent.tools.tool_types - INFO - [get_chapter_by_order] 开始执行工具
2025-12-25 13:02:25,168 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务4开始: 获取第四章内容
2025-12-25 13:02:25,168 - app.api.v1.agent - INFO - [Stream] Task started: 获取第四章内容
2025-12-25 13:02:25,169 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(get_chapter_by_order)
2025-12-25 13:02:25,169 - app.services.agent.tools.tool_types - INFO - [get_chapter_by_order] 开始执行工具
2025-12-25 13:02:25,170 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务5开始: 获取第五章内容
2025-12-25 13:02:25,170 - app.api.v1.agent - INFO - [Stream] Task started: 获取第五章内容
2025-12-25 13:02:25,173 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(get_chapter_by_order)
2025-12-25 13:02:25,173 - app.services.agent.tools.tool_types - INFO - [get_chapter_by_order] 开始执行工具
2025-12-25 13:02:25,210 - app.services.agent.langgraph_tools - INFO - [get_chapter_by_order_tool] ✅ 找到第4章: 第4章 家底
2025-12-25 13:02:25,219 - app.services.agent.langgraph_tools - INFO - [get_chapter_by_order_tool] ✅ 找到第3章: 第3章 一夕千悟
2025-12-25 13:02:25,233 - app.services.agent.langgraph_tools - INFO - [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
2025-12-25 13:02:25,241 - app.services.agent.langgraph_tools - INFO - [get_chapter_by_order_tool] ✅ 找到第5章: 第5章 太一门
2025-12-25 13:02:25,250 - app.services.agent.langgraph_tools - INFO - [get_chapter_by_order_tool] ✅ 找到第2章: 第2章 浑圆桩
2025-12-25 13:02:25,253 - app.services.agent.tools.tool_types - INFO - [get_chapter_by_order] 执行成功 (耗时: 0.083s)
2025-12-25 13:02:25,254 - app.services.agent.execution.task_runner - INFO - [TaskRunner] get_chapter_by_order 执行成功（DeepAgent模式）
2025-12-25 13:02:25,254 - app.api.v1.agent - INFO - [Stream] 任务完成: 获取第四章内容 (0.1s)
2025-12-25 13:02:25,254 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务4完成
2025-12-25 13:02:25,255 - app.services.agent.tools.tool_types - INFO - [get_chapter_by_order] 执行成功 (耗时: 0.087s)
2025-12-25 13:02:25,256 - app.services.agent.execution.task_runner - INFO - [TaskRunner] get_chapter_by_order 执行成功（DeepAgent模式）
2025-12-25 13:02:25,256 - app.api.v1.agent - INFO - [Stream] 任务完成: 获取第三章内容 (0.1s)
2025-12-25 13:02:25,256 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务3完成
2025-12-25 13:02:25,257 - app.services.agent.tools.tool_types - INFO - [get_chapter_by_order] 执行成功 (耗时: 0.096s)
2025-12-25 13:02:25,257 - app.services.agent.execution.task_runner - INFO - [TaskRunner] get_chapter_by_order 执行成功（DeepAgent模式）
2025-12-25 13:02:25,257 - app.api.v1.agent - INFO - [Stream] 任务完成: 获取第一章内容 (0.1s)
2025-12-25 13:02:25,257 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务1完成
2025-12-25 13:02:25,258 - app.services.agent.tools.tool_types - INFO - [get_chapter_by_order] 执行成功 (耗时: 0.085s)
2025-12-25 13:02:25,259 - app.services.agent.execution.task_runner - INFO - [TaskRunner] get_chapter_by_order 执行成功（DeepAgent模式）
2025-12-25 13:02:25,260 - app.api.v1.agent - INFO - [Stream] 任务完成: 获取第五章内容 (0.1s)
2025-12-25 13:02:25,260 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务5完成
2025-12-25 13:02:25,261 - app.services.agent.tools.tool_types - INFO - [get_chapter_by_order] 执行成功 (耗时: 0.096s)
2025-12-25 13:02:25,262 - app.services.agent.execution.task_runner - INFO - [TaskRunner] get_chapter_by_order 执行成功（DeepAgent模式）
2025-12-25 13:02:25,262 - app.api.v1.agent - INFO - [Stream] 任务完成: 获取第二章内容 (0.1s)
2025-12-25 13:02:25,264 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务2完成
2025-12-25 13:02:25,265 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始第二层并行执行1个任务
2025-12-25 13:02:25,266 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第二层任务6开始: 分析前5章内容，提取主要剧情脉络
2025-12-25 13:02:25,266 - app.api.v1.agent - INFO - [Stream] Task started: 分析前5章内容，提取主要剧情脉络
2025-12-25 13:02:25,266 - app.services.agent.execution.task_runner - INFO - [TaskRunner] analyze_text_tool 使用 focus: '分析前5章的主要剧情脉络，梳理核心事件、人物关系发展、主要冲突和伏笔。...'
2025-12-25 13:02:25,266 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(analyze_text)
2025-12-25 13:02:25,267 - app.services.agent.tools.tool_types - INFO - [analyze_text] 开始执行工具
2025-12-25 13:02:25,267 - app.services.agent.tools.analysis_tools - INFO - [analyze_text_tool] 尝试第 1 次调用，config={'temperature': 0.3, 'task_type': <TaskType.SUMMARIZATION: 'summarization'>}
2025-12-25 13:02:25,280 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2025-12-25 13:02:25,280 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2025-12-25 13:02:25,281 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
2025-12-25 13:02:32,159 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:59992 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2025-12-25 13:02:32,173 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/3749ebb4-a2d6-4ab8-aa14-cf6c26611fc0/unread-info
INFO:     127.0.0.1:59993 - "GET /api/v1/channels/3749ebb4-a2d6-4ab8-aa14-cf6c26611fc0/unread-info HTTP/1.1" 200 OK
2025-12-25 13:02:34,251 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-12-25 13:02:36,876 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 9 个数据块，总长度: 711
2025-12-25 13:02:36,877 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 10900 (prompt=10346, completion=554)
2025-12-25 13:02:36,877 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2025-12-25 13:02:36,877 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2025-12-25 13:02:36,902 - app.services.ai.http_ai_service - INFO - [积分扣除] 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456: 扣除 55.66 积分, 余额: 53112.88 → 53057.22
2025-12-25 13:02:36,903 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=10900, cost=$0.004489, time=11597ms
2025-12-25 13:02:36,904 - app.services.agent.tools.analysis_tools - INFO - [analyze_text_tool] 第 1 次调用成功
2025-12-25 13:02:36,904 - app.services.agent.tools.analysis_tools - INFO - [analyze_text_tool] 分析完成，结果长度: 711
2025-12-25 13:02:36,904 - app.services.agent.tools.tool_types - INFO - [analyze_text] 执行成功 (耗时: 11.638s)
2025-12-25 13:02:36,906 - app.services.agent.execution.task_runner - INFO - [TaskRunner] analyze_text 执行成功（DeepAgent模式）
2025-12-25 13:02:36,906 - app.api.v1.agent - INFO - [Stream] 任务完成: 分析前5章内容，提取主要剧情脉络 (11.6s)
2025-12-25 13:02:36,907 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第二层任务6完成
2025-12-25 13:02:36,909 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共6个任务，耗时: 11.76s
2025-12-25 13:02:36,909 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2025-12-25 13:02:36,911 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=1, 展示型=5
2025-12-25 13:02:36,911 - app.services.agent.langgraph_agent - INFO - [Response] 单个分析任务(analyze_text_tool)，使用AI格式化
2025-12-25 13:02:36,912 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2025-12-25 13:02:36,913 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=13629字符, 处理后=5392字符
2025-12-25 13:02:36,914 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2025-12-25 13:02:36,914 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2025-12-25 13:02:36,925 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2025-12-25 13:02:36,925 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2025-12-25 13:02:36,926 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
2025-12-25 13:02:43,118 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-12-25 13:02:47,240 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 15 个数据块，总长度: 1017
2025-12-25 13:02:47,240 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 5962 (prompt=5232, completion=730)
2025-12-25 13:02:47,241 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2025-12-25 13:02:47,241 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2025-12-25 13:02:47,252 - app.services.ai.http_ai_service - INFO - [积分扣除] 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456: 扣除 42.09 积分, 余额: 53057.22 → 53015.13
2025-12-25 13:02:47,252 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=5962, cost=$0.003395, time=10313ms
2025-12-25 13:02:47,253 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=1017
2025-12-25 13:02:48,560 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:f141c5ed-0a75-4429-ba2a-912c74d167a3 | 重要度=0.89
2025-12-25 13:02:49,957 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:f141c5ed-0a75-4429-ba2a-912c74d167a3 | 重要度=0.94
2025-12-25 13:02:49,961 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:65024582-f3d1-40e6-9bcf-0af3a3e3dc4e, token=1250
2025-12-25 13:02:49,962 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:65024582-f3d1-40e6-9bcf-0af3a3e3dc4e, 消息数=2, Token=1250
2025-12-25 13:02:49,962 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:65024582-f3d1-40e6-9bcf-0af3a3e3dc4e)
2025-12-25 13:02:49,963 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2025-12-25 13:02:49,967 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed
2025-12-25 13:03:32,157 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:59812 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2025-12-25 13:03:32,188 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/3749ebb4-a2d6-4ab8-aa14-cf6c26611fc0/unread-info
INFO:     127.0.0.1:56856 - "GET /api/v1/channels/3749ebb4-a2d6-4ab8-aa14-cf6c26611fc0/unread-info HTTP/1.1" 200 OK
2025-12-25 13:04:32,131 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:59288 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2025-12-25 13:04:32,149 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/3749ebb4-a2d6-4ab8-aa14-cf6c26611fc0/unread-info
INFO:     127.0.0.1:50469 - "GET /api/v1/channels/3749ebb4-a2d6-4ab8-aa14-cf6c26611fc0/unread-info HTTP/1.1" 200 OK
2025-12-25 13:05:32,147 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:55025 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2025-12-25 13:05:32,158 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/3749ebb4-a2d6-4ab8-aa14-cf6c26611fc0/unread-info
INFO:     127.0.0.1:57142 - "GET /api/v1/channels/3749ebb4-a2d6-4ab8-aa14-cf6c26611fc0/unread-info HTTP/1.1" 200 OK