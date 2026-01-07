2026-01-07 12:16:24,903 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:53134 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-07 12:16:24,933 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:63410 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-07 12:16:25,050 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:51408 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-07 12:16:33,013 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:53102 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-07 12:16:37,367 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:64393 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-07 12:17:03,038 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:59544 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-07 12:17:23,991 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:62752 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-07 12:17:25,631 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI(Join)(602f5147-846a-4cde-95d3-405fa75f133f), work_id: e81ab1f7-7d84-4436-8793-fedac77c5123, chapter_id: 26e75531-13a7-4c29-8bcc-7e5baf94b921
2026-01-07 12:17:25,640 - app.core.redis - INFO - ✅ Redis connected: redis://localhost:6379/0
2026-01-07 12:17:25,679 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 26e75531-13a7-4c29-8bcc-7e5baf94b921
2026-01-07 12:17:25,685 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: 5440c4b0-2341-4fd3-80bd-11f2ce8607cb
2026-01-07 12:17:25,686 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-07 12:17:25,688 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:64166 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-07 12:17:25,701 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI(Join)(602f5147-846a-4cde-95d3-405fa75f133f), work_id: e81ab1f7-7d84-4436-8793-fedac77c5123, chapter_id: 26e75531-13a7-4c29-8bcc-7e5baf94b921
2026-01-07 12:17:25,727 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 26e75531-13a7-4c29-8bcc-7e5baf94b921
2026-01-07 12:17:25,731 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: 5440c4b0-2341-4fd3-80bd-11f2ce8607cb
2026-01-07 12:17:25,731 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-07 12:17:25,734 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:60870 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-07 12:17:26,204 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:e81ab1f7-7d84-4436-8793-fedac77c5123
2026-01-07 12:17:26,208 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/26e75531-13a7-4c29-8bcc-7e5baf94b921
INFO:     127.0.0.1:63333 - "PUT /api/v1/chapters/26e75531-13a7-4c29-8bcc-7e5baf94b921 HTTP/1.1" 200 OK
2026-01-07 12:17:26,231 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第4章 家底 (order=4)
2026-01-07 12:17:28,202 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第4章 家底 (6 chunks)
2026-01-07 12:17:28,483 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:64328 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2026-01-07 12:17:28,576 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:e81ab1f7-7d84-4436-8793-fedac77c5123
2026-01-07 12:17:28,579 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/26e75531-13a7-4c29-8bcc-7e5baf94b921
INFO:     127.0.0.1:49462 - "PUT /api/v1/chapters/26e75531-13a7-4c29-8bcc-7e5baf94b921 HTTP/1.1" 200 OK
2026-01-07 12:17:28,584 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第4章 家底 (order=4)
2026-01-07 12:17:29,616 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第4章 家底 (6 chunks)
2026-01-07 12:17:32,977 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:56403 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-07 12:17:33,480 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:58706 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2026-01-07 12:17:33,496 - app.services.ai.prompts - INFO - Prompts loaded successfully from D:\Java\ai_writer\backend\app\services\ai\prompts\default.json
2026-01-07 12:17:33,496 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-07 12:17:33,496 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-07 12:17:33,496 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2026-01-07 12:17:35,155 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-07 12:17:35,155 - app.api.v1.agent - INFO - [Chat Stream] Mode: planning
2026-01-07 12:17:35,164 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:59132 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2026-01-07 12:17:35,182 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: planning, Message: 基于小说中的设定，帮我续写一段段融第二天在马厩工作时，意外发现一件旧马鞍也有器灵的情节。要求：
  ...
2026-01-07 12:17:35,183 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-07 12:17:35,183 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-07 12:17:35,183 - app.services.ai.http_ai_service - INFO - [成本追踪] 初始化未传db/user_id，将使用请求上下文按需记录成本
2026-01-07 12:17:37,113 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-07 12:17:37,114 - app.services.agent.tools.writing_tools - INFO - Writing tools AI service initialized
2026-01-07 12:17:37,114 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ AI Service 已同时设置到 langgraph_tools 和 writing_tools
2026-01-07 12:17:37,114 - app.services.context.adaptive_budget - INFO - ✅ 所有预算配置验证通过
2026-01-07 12:17:43,544 - app.services.context.vector_memory_store - INFO - ✅ VectorMemoryStore初始化成功 | 目录=./data/chroma_db | 模型=paraphrase-multilingual-MiniLM-L12-v2 | 集合=user_memories
2026-01-07 12:17:43,544 - app.services.context.manager - INFO - ✅ VectorMemoryStore 已初始化
2026-01-07 12:17:43,544 - app.services.context.manager - INFO - ✅ ContextManager: 长期记忆已启用 (user_id=None)
2026-01-07 12:17:43,546 - app.services.context.manager - INFO - ✅ ContextManager: 自适应预算已启用
2026-01-07 12:17:43,547 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ ContextManager已初始化（长期记忆已启用，自适应预算已启用，总预算=16000 tokens）
成功加载模板: analyze_text (版本 3.1.0)
成功加载模板: intent_classifier (版本 2.0.0)
成功加载模板: writing_agent (版本 2.0.0)
成功加载模板: planning_agent (版本 2.0.0)
成功加载模板: tool_agent (版本 2.0.0)
成功加载模板: query_agent (版本 2.0.0)
成功加载模板: system_agent_prompt (版本 2.0.0)
成功加载模板: creative_writing_prompt (版本 1.0.0)
2026-01-07 12:17:43,608 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ PromptManager已初始化
2026-01-07 12:17:43,620 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ Redis连接验证成功
2026-01-07 12:17:43,620 - app.services.agent.langgraph_agent - INFO - [LangGraph] OK 使用 AsyncRedisSaver（redis://localhost:6379/0，TTL=7天）
2026-01-07 12:17:43,623 - app.services.agent.memory.metrics - INFO - [MemoryMetrics] 监控系统已初始化
2026-01-07 12:17:43,624 - app.services.agent.memory.long_term_store - INFO - [LongTermStore] Initialized: base_dir=./data/long_term_memory, max_size=50KB, compression=True
2026-01-07 12:17:43,625 - app.services.agent.memory.enhanced_memory_manager - INFO - EnhancedMemoryManager initialized: short=10, medium=100, threshold=0.1, long_term_backup=enabled
2026-01-07 12:17:43,625 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ EnhancedMemoryManager已创建
2026-01-07 12:17:43,626 - app.services.agent.memory.unified_coordinator - INFO - [UnifiedMemoryCoordinator] 初始化统一记忆协调器
2026-01-07 12:17:43,626 - app.services.agent.memory.unified_coordinator - INFO - [UnifiedMemoryCoordinator] 全局实例已设置
2026-01-07 12:17:43,626 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ UnifiedMemoryCoordinator已初始化 | checkpointer=AsyncRedisSaver | enhanced_memory=yes | context_manager=yes
2026-01-07 12:17:43,626 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ 解耦模块已初始化 (IntentClassifier, ToolExecutor, EventParser, ResponseBuilder, ToolDispatcher, ParallelExecutor, PlanGenerator, QuickPathHandler, StreamEventHandler, SecondaryToolHandler, TaskRunner, AgentExecutor)
2026-01-07 12:17:43,639 - app.services.agent.parallel_tool_node - INFO - [ParallelToolNode] 初始化完成，最大并发数=5，并行安全工具=4个
2026-01-07 12:17:43,656 - app.api.v1.agent - INFO - [Global Agent] created global agent instance; MemorySaver shared across requests
2026-01-07 12:17:43,656 - app.api.v1.agent - INFO - [agent_chat_stream] 📥 收到的 context 字段:
2026-01-07 12:17:43,656 - app.api.v1.agent - INFO -   - selected_text: N/A...
2026-01-07 12:17:43,656 - app.api.v1.agent - INFO -   - selection_position: N/A
2026-01-07 12:17:43,658 - app.api.v1.agent - INFO -   - chapter_context: 当前章节ID: 26e75531-13a7-4c29-8bcc-7e5baf94b921...
2026-01-07 12:17:43,658 - app.api.v1.agent - INFO -   - instruction_context: N/A...
2026-01-07 12:17:43,681 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:57384 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-07 12:17:43,693 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 602f5147-846a-4cde-95d3-405fa75f133f:e81ab1f7-7d84-4436-8793-fedac77c5123:e219262a-c4fa-4185-9d4a-e595808b326d (user_id=602f5147-846a-4cde-95d3-405fa75f133f, work_id=e81ab1f7-7d84-4436-8793-fedac77c5123, conversation_id=e219262a-c4fa-4185-9d4a-e595808b326d)
2026-01-07 12:17:43,693 - app.services.context.monitoring_integration - INFO - ✅ ContextManager监控收集器已初始化
2026-01-07 12:17:43,694 - app.services.context.store - INFO - [ContextStore] Redis连接成功
2026-01-07 12:17:43,708 - app.services.context.manager - INFO - [ContextManager] 创建新上下文: 602f5147-846a-4cde-95d3-405fa75f133f:e81ab1f7-7d84-4436-8793-fedac77c5123:e219262a-c4fa-4185-9d4a-e595808b326d
2026-01-07 12:17:43,943 - app.services.context.token_counter - INFO - ✅ tiktoken初始化成功，模型: gemini-2.5-pro -> cl100k_base
2026-01-07 12:17:43,945 - app.services.context.manager - INFO - [ContextManager] Session 602f5147-846a-4cde-95d3-405fa75f133f:e81ab1f7-7d84-4436-8793-fedac77c5123:e219262a-c4fa-4185-9d4a-e595808b326d: 0/16000 tokens
2026-01-07 12:17:44,995 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='基于小说中的设定，帮我续写一段段融第二天在马厩工作时，意外发...' | 隔离键=['user:602f5147-846a-4cde-95d3-405fa75f133f:work:e81ab1f7-7d84-4436-8793-fedac77c5123', 'user:602f5147-846a-4cde-95d3-405fa75f133f'] | 找到=3条
2026-01-07 12:17:44,995 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=e81ab1f7-7d84-4436-8793-fedac77c5123 | 含用户级=True | 找到=3条
2026-01-07 12:17:44,995 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 1条消息, 0 tokens, 耗时 1300.67ms
2026-01-07 12:17:44,997 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 1 条历史消息 (token: 0)
2026-01-07 12:17:44,999 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-07 12:17:44,999 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-07 12:17:44,999 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=20, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-07 12:17:46,479 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
2026-01-07 12:17:46,479 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-07 12:17:46,513 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
2026-01-07 12:17:46,517 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=347, cost=$0.000035, time=1481ms
2026-01-07 12:17:46,517 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=7, 尝试次数=1
2026-01-07 12:17:46,517 - app.services.agent.intent.classifier - INFO - [Intent] AI识别结果: writing
2026-01-07 12:17:46,517 - app.services.agent.langgraph_agent - INFO - [Planning] AI意图分类: writing (置信度: 0.90)
2026-01-07 12:17:46,517 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 基于小说中的设定，帮我续写一段段融第二天在马厩工作时，意外发现一件旧马鞍也有器灵的情节。要求：
  ...
2026-01-07 12:17:46,521 - app.core.cache - INFO - ⚠️ 缓存未命中: prompt:planning:v2.28.0:get_planning_static_prompt:fca6eb91156619d0
2026-01-07 12:17:46,528 - app.core.cache - INFO - 💾 缓存已保存: prompt:planning:v2.28.0:get_planning_static_prompt:fca6eb91156619d0 (expire=3600s)
2026-01-07 12:17:46,532 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-07 12:17:46,533 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=story_planning, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: story_planning; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-01-07 12:17:46,533 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.3, task_type=TaskType.STORY_PLANNING
2026-01-07 12:18:02,999 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:57593 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-07 12:18:07,331 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:59812 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-07 12:18:07,891 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-07 12:18:14,639 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 11 个数据块，总长度: 1280
2026-01-07 12:18:14,639 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 14096 (prompt=13392, completion=704)
2026-01-07 12:18:14,639 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
2026-01-07 12:18:14,641 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-07 12:18:14,653 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
2026-01-07 12:18:14,653 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=14096, cost=$0.023780, time=28108ms
2026-01-07 12:18:14,653 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=14096
2026-01-07 12:18:14,653 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户需要创作一段续写内容，属于创作类请求。输出形式为一段约5, 原料=为了保证续写内容符合原文设定，需要获取以, 处理=这是一个创作请求，必须分阶段执行。
第一
2026-01-07 12:18:14,653 - app.services.agent.planning.plan_generator - INFO - [Planning] 直接回答模式，答案长度: 95
2026-01-07 12:18:14,653 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共2个任务
2026-01-07 12:18:14,653 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共2个任务，耗时: 28.14s
2026-01-07 12:18:14,653 - app.api.v1.agent - INFO - [Stream] Plan tasks: 2 items
2026-01-07 12:18:14,653 - app.services.agent.langgraph_agent - INFO - [FlowEvent] 准备发送 agent_header 事件
2026-01-07 12:18:14,660 - app.api.v1.agent - INFO - [FlowEvent] 发送事件: type=agent_header
2026-01-07 12:18:14,660 - app.services.agent.langgraph_agent - INFO - [FlowEvent] 准备发送 text 事件
2026-01-07 12:18:14,660 - app.api.v1.agent - INFO - [FlowEvent] 发送事件: type=text
2026-01-07 12:18:14,661 - app.services.agent.langgraph_agent - WARNING - [Planning-Alert] AI 违反协议：同时返回 direct_answer(95字) 和 2 个 tasks，将执行 tasks 而忽略 direct_answer
2026-01-07 12:18:14,661 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2026-01-07 12:18:14,662 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2026-01-07 12:18:14,662 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2026-01-07 12:18:14,662 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 任务分组: 第一层并行=1, 第二层并行=0, 串行=1
2026-01-07 12:18:14,662 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始第一层并行执行1个任务
2026-01-07 12:18:14,662 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务2开始: 读取用户当前所在章节（chapter_id: 26e75531-13a7-4c29-8bcc-7e5baf94b921）的内容，以了解续写的上下文。
2026-01-07 12:18:14,669 - app.api.v1.agent - INFO - [FlowEvent] 发送事件: type=step_start
2026-01-07 12:18:14,669 - app.api.v1.agent - INFO - [Stream] Task started: 读取用户当前所在章节（chapter_id: 26e75531-13a7-4c29-8bcc-7e5baf94b921）的内容，以了解续写的上下文。 (icon=FileText)
2026-01-07 12:18:14,669 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(read_chapter)
2026-01-07 12:18:14,669 - app.services.agent.tools.tool_types - INFO - [read_chapter] 开始执行工具
2026-01-07 12:18:14,676 - app.services.agent.langgraph_tools - INFO - [read_chapter_tool] ✅ 读取章节成功: 第4章 家底
2026-01-07 12:18:14,683 - app.services.agent.tools.tool_types - INFO - [read_chapter] 执行成功 (耗时: 0.014s)
2026-01-07 12:18:14,683 - app.services.agent.tools.tool_monitor - INFO - ToolMonitor initialized with Memory storage, retention: 7 days
2026-01-07 12:18:14,683 - app.services.agent.execution.task_runner - INFO - [TaskRunner] read_chapter 执行成功（DeepAgent模式）
2026-01-07 12:18:14,683 - app.api.v1.agent - INFO - [FlowEvent] 发送事件: type=step_complete
2026-01-07 12:18:14,683 - app.api.v1.agent - INFO - [Stream] 任务完成: 读取用户当前所在章节（chapter_id: 26e75531-13a7-4c29-8bcc-7e5baf94b921）的内容，以了解续写的上下文。 (0.0s)
2026-01-07 12:18:14,683 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务2完成
2026-01-07 12:18:14,683 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始串行执行1个任务
2026-01-07 12:18:14,683 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务1开始: 获取世界观以了解器灵规则和主角段融的性格设定。
2026-01-07 12:18:14,683 - app.api.v1.agent - INFO - [FlowEvent] 发送事件: type=step_start
2026-01-07 12:18:14,683 - app.api.v1.agent - INFO - [Stream] Task started: 获取世界观以了解器灵规则和主角段融的性格设定。 (icon=Wrench)
2026-01-07 12:18:14,683 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: get_worldview_summary
2026-01-07 12:18:14,683 - app.services.agent.execution.tool_executor - WARNING - [StandardTool] 'get_worldview_summary' 不存在，降级到 @tool: 工具 'get_worldview_summary' 不存在
可用的 StandardTool: ['continue_writing', 'expand_text', 'analyze_content', 'analyze_text', 'evaluate_quality', 'smart_rewrite', 'smart_continue', 'smart_insert', 'apply_chapter_edit', 'get_context', 'read_chapter', 'get_chapter_by_order', 'search_analysis_fragments']
可用的 DynamicTool: []
2026-01-07 12:18:14,683 - app.services.agent.execution.tool_executor - INFO - [LegacyTool] 使用 @tool 版本: get_worldview_summary
2026-01-07 12:18:14,694 - app.services.agent.langgraph_tools - INFO - [get_worldview_summary] ✅ 获取世界观摘要成功: {'characters': 0, 'locations': 0, 'settings': 0}
2026-01-07 12:18:14,694 - app.api.v1.agent - INFO - [FlowEvent] 发送事件: type=step_complete
2026-01-07 12:18:14,694 - app.api.v1.agent - INFO - [Stream] 任务完成: 获取世界观以了解器灵规则和主角段融的性格设定。 (0.0s)
2026-01-07 12:18:14,694 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务1完成
2026-01-07 12:18:14,694 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共2个任务，耗时: 0.03s
2026-01-07 12:18:14,694 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2026-01-07 12:18:14,694 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=2, 输出型=0, 展示型=0
2026-01-07 12:18:14,694 - app.services.agent.langgraph_agent - INFO - [Response] 分阶段执行第一阶段，基于任务结果生成询问
2026-01-07 12:18:14,694 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2026-01-07 12:18:14,694 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=2916字符, 处理后=3018字符
2026-01-07 12:18:14,694 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2026-01-07 12:18:14,694 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2026-01-07 12:18:14,704 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-07 12:18:14,704 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-07 12:18:14,704 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
2026-01-07 12:18:24,295 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-07 12:18:24,297 - app.services.agent.planning.response_builder - INFO - [Summarization] stream_callback 收到 chunk: 91 字符
2026-01-07 12:18:24,298 - app.services.agent.planning.response_builder - INFO - [Summarization] 调用 on_content 发送 chunk
2026-01-07 12:18:24,298 - app.api.v1.agent - INFO - [on_content] 收到 chunk: <class 'str'>, 长度: 91
2026-01-07 12:18:24,299 - app.api.v1.agent - INFO - [on_content] 发送到队列: 91 字符
2026-01-07 12:18:24,300 - app.api.v1.agent - INFO - [SSE] 发送 content 事件: 91 字符
2026-01-07 12:18:24,717 - app.services.agent.planning.response_builder - INFO - [Summarization] stream_callback 收到 chunk: 86 字符
2026-01-07 12:18:24,718 - app.services.agent.planning.response_builder - INFO - [Summarization] 调用 on_content 发送 chunk
2026-01-07 12:18:24,718 - app.api.v1.agent - INFO - [on_content] 收到 chunk: <class 'str'>, 长度: 86
2026-01-07 12:18:24,719 - app.api.v1.agent - INFO - [on_content] 发送到队列: 86 字符
2026-01-07 12:18:24,720 - app.api.v1.agent - INFO - [SSE] 发送 content 事件: 86 字符
2026-01-07 12:18:25,300 - app.services.agent.planning.response_builder - INFO - [Summarization] stream_callback 收到 chunk: 102 字符
2026-01-07 12:18:25,301 - app.services.agent.planning.response_builder - INFO - [Summarization] 调用 on_content 发送 chunk
2026-01-07 12:18:25,301 - app.api.v1.agent - INFO - [on_content] 收到 chunk: <class 'str'>, 长度: 102
2026-01-07 12:18:25,302 - app.api.v1.agent - INFO - [on_content] 发送到队列: 102 字符
2026-01-07 12:18:25,302 - app.api.v1.agent - INFO - [SSE] 发送 content 事件: 102 字符
2026-01-07 12:18:25,749 - app.services.agent.planning.response_builder - INFO - [Summarization] stream_callback 收到 chunk: 113 字符
2026-01-07 12:18:25,749 - app.services.agent.planning.response_builder - INFO - [Summarization] 调用 on_content 发送 chunk
2026-01-07 12:18:25,750 - app.api.v1.agent - INFO - [on_content] 收到 chunk: <class 'str'>, 长度: 113
2026-01-07 12:18:25,751 - app.api.v1.agent - INFO - [on_content] 发送到队列: 113 字符
2026-01-07 12:18:25,752 - app.api.v1.agent - INFO - [SSE] 发送 content 事件: 113 字符
2026-01-07 12:18:26,273 - app.services.agent.planning.response_builder - INFO - [Summarization] stream_callback 收到 chunk: 104 字符
2026-01-07 12:18:26,274 - app.services.agent.planning.response_builder - INFO - [Summarization] 调用 on_content 发送 chunk
2026-01-07 12:18:26,274 - app.api.v1.agent - INFO - [on_content] 收到 chunk: <class 'str'>, 长度: 104
2026-01-07 12:18:26,274 - app.api.v1.agent - INFO - [on_content] 发送到队列: 104 字符
2026-01-07 12:18:26,275 - app.api.v1.agent - INFO - [SSE] 发送 content 事件: 104 字符
2026-01-07 12:18:26,681 - app.services.agent.planning.response_builder - INFO - [Summarization] stream_callback 收到 chunk: 97 字符
2026-01-07 12:18:26,682 - app.services.agent.planning.response_builder - INFO - [Summarization] 调用 on_content 发送 chunk
2026-01-07 12:18:26,684 - app.api.v1.agent - INFO - [on_content] 收到 chunk: <class 'str'>, 长度: 97
2026-01-07 12:18:26,684 - app.api.v1.agent - INFO - [on_content] 发送到队列: 97 字符
2026-01-07 12:18:26,685 - app.api.v1.agent - INFO - [SSE] 发送 content 事件: 97 字符
2026-01-07 12:18:27,078 - app.services.agent.planning.response_builder - INFO - [Summarization] stream_callback 收到 chunk: 100 字符
2026-01-07 12:18:27,078 - app.services.agent.planning.response_builder - INFO - [Summarization] 调用 on_content 发送 chunk
2026-01-07 12:18:27,079 - app.api.v1.agent - INFO - [on_content] 收到 chunk: <class 'str'>, 长度: 100
2026-01-07 12:18:27,080 - app.api.v1.agent - INFO - [on_content] 发送到队列: 100 字符
2026-01-07 12:18:27,080 - app.api.v1.agent - INFO - [SSE] 发送 content 事件: 100 字符
2026-01-07 12:18:27,325 - app.services.agent.planning.response_builder - INFO - [Summarization] stream_callback 收到 chunk: 50 字符
2026-01-07 12:18:27,325 - app.services.agent.planning.response_builder - INFO - [Summarization] 调用 on_content 发送 chunk
2026-01-07 12:18:27,325 - app.api.v1.agent - INFO - [on_content] 收到 chunk: <class 'str'>, 长度: 50
2026-01-07 12:18:27,325 - app.api.v1.agent - INFO - [on_content] 发送到队列: 50 字符
2026-01-07 12:18:27,328 - app.api.v1.agent - INFO - [SSE] 发送 content 事件: 50 字符
2026-01-07 12:18:27,355 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 8 个数据块，总长度: 743
2026-01-07 12:18:27,356 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 4282 (prompt=3793, completion=489)
2026-01-07 12:18:27,356 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
2026-01-07 12:18:27,357 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-07 12:18:27,372 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
2026-01-07 12:18:27,373 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4282, cost=$0.002360, time=12653ms
2026-01-07 12:18:27,373 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=743
2026-01-07 12:18:27,373 - app.api.v1.agent - INFO - [FlowEvent] 发送事件: type=completion
2026-01-07 12:18:27,440 - app.services.context.vector_memory_store - INFO - 🔁 跳过重复记忆，复用ID=79913e7e-d5cd-4e09-bce6-ca6639bd8456_1767735042807_0b14d34f
2026-01-07 12:18:27,441 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:e81ab1f7-7d84-4436-8793-fedac77c5123 | 重要度=1.00
2026-01-07 12:18:29,860 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 隔离=work:e81ab1f7-7d84-4436-8793-fedac77c5123 | 重要度=0.60
2026-01-07 12:18:29,860 - app.api.v1.agent - INFO - [SSE] 发送 completion 事件
2026-01-07 12:18:29,879 - app.services.context.store - INFO - [ContextStore] 保存上下文: 602f5147-846a-4cde-95d3-405fa75f133f:e81ab1f7-7d84-4436-8793-fedac77c5123:e219262a-c4fa-4185-9d4a-e595808b326d, token=882
2026-01-07 12:18:29,879 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 602f5147-846a-4cde-95d3-405fa75f133f:e81ab1f7-7d84-4436-8793-fedac77c5123:e219262a-c4fa-4185-9d4a-e595808b326d, 消息数=2, Token=882
2026-01-07 12:18:29,880 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=602f5147-846a-4cde-95d3-405fa75f133f:e81ab1f7-7d84-4436-8793-fedac77c5123:e219262a-c4fa-4185-9d4a-e595808b326d)
2026-01-07 12:18:29,881 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2026-01-07 12:18:29,888 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed
2026-01-07 12:18:32,996 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:64905 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-07 12:18:37,331 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:64395 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK