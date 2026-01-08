2026-01-08 20:33:46,606 - app.core.redis - INFO - ✅ Redis connected: redis://localhost:6379/0
2026-01-08 20:33:46,610 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 帮我改写第一章中段融第一次成功吞噬器灵的场景（"吞噬！"那段），
  要求：
  1. 增加吞噬过程...
2026-01-08 20:33:46,612 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-08 20:33:46,613 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-08 20:33:46,614 - app.services.ai.http_ai_service - INFO - [成本追踪] 初始化未传db/user_id，将使用请求上下文按需记录成本
2026-01-08 20:33:48,758 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-08 20:33:48,768 - app.services.agent.tools.writing_tools - INFO - Writing tools AI service initialized
2026-01-08 20:33:48,769 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ AI Service 已同时设置到 langgraph_tools 和 writing_tools
2026-01-08 20:33:48,779 - app.services.context.adaptive_budget - INFO - ✅ 所有预算配置验证通过
2026-01-08 20:33:58,149 - app.services.context.vector_memory_store - INFO - ✅ VectorMemoryStore初始化成功 | 目录=./data/chroma_db | 模型=paraphrase-multilingual-MiniLM-L12-v2 | 集合=user_memories
2026-01-08 20:33:58,150 - app.services.context.manager - INFO - ✅ VectorMemoryStore 已初始化
2026-01-08 20:33:58,152 - app.services.context.manager - INFO - ✅ ContextManager: 长期记忆已启用 (user_id=None)
2026-01-08 20:33:58,152 - app.services.context.manager - INFO - ✅ ContextManager: 自适应预算已启用
2026-01-08 20:33:58,152 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ ContextManager已初始化（长期记忆已启用，自适应预算已启用，总预算=16000 tokens）
成功加载模板: analyze_text (版本 3.1.0)
成功加载模板: intent_classifier (版本 2.0.0)
成功加载模板: writing_agent (版本 2.0.0)
成功加载模板: planning_agent (版本 2.0.0)
成功加载模板: tool_agent (版本 2.0.0)
成功加载模板: query_agent (版本 2.0.0)
成功加载模板: system_agent_prompt (版本 2.0.0)
成功加载模板: creative_writing_prompt (版本 1.0.0)
2026-01-08 20:33:58,554 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ PromptManager已初始化
2026-01-08 20:33:58,572 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ Redis连接验证成功
2026-01-08 20:33:58,599 - app.services.agent.langgraph_agent - INFO - [LangGraph] OK 使用 AsyncRedisSaver（redis://localhost:6379/0，TTL=7天）
2026-01-08 20:33:58,607 - app.services.agent.memory.metrics - INFO - [MemoryMetrics] 监控系统已初始化
2026-01-08 20:33:58,608 - app.services.agent.memory.long_term_store - INFO - [LongTermStore] Initialized: base_dir=./data/long_term_memory, max_size=50KB, compression=True
2026-01-08 20:33:58,611 - app.services.agent.memory.enhanced_memory_manager - INFO - EnhancedMemoryManager initialized: short=10, medium=100, threshold=0.1, long_term_backup=enabled
2026-01-08 20:33:58,613 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ EnhancedMemoryManager已创建
2026-01-08 20:33:58,615 - app.services.agent.memory.unified_coordinator - INFO - [UnifiedMemoryCoordinator] 初始化统一记忆协调器
2026-01-08 20:33:58,617 - app.services.agent.memory.unified_coordinator - INFO - [UnifiedMemoryCoordinator] 全局实例已设置
2026-01-08 20:33:58,618 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ UnifiedMemoryCoordinator已初始化 | checkpointer=AsyncRedisSaver | enhanced_memory=yes | context_manager=yes
2026-01-08 20:33:58,623 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ 解耦模块已初始化 (IntentClassifier, ToolExecutor, EventParser, ResponseBuilder, ToolDispatcher, ParallelExecutor, PlanGenerator, QuickPathHandler, StreamEventHandler, SecondaryToolHandler, TaskRunner, AgentExecutor)
2026-01-08 20:33:58,966 - app.services.agent.parallel_tool_node - INFO - [ParallelToolNode] 初始化完成，最大并发数=5，并行安全工具=4个
2026-01-08 20:33:59,116 - app.api.v1.agent - INFO - [Global Agent] created global agent instance; MemorySaver shared across requests
2026-01-08 20:33:59,198 - app.api.v1.agent - INFO - [agent_chat_stream] 📚 世界观数据已注入: 人物=11, 地点=7, 设定=6, 规范=无
2026-01-08 20:33:59,204 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:87ec1ffa-7d94-4d36-a773-227a8195ea36:68977cdc-485e-4281-85c0-d70856550c8a (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=87ec1ffa-7d94-4d36-a773-227a8195ea36, conversation_id=68977cdc-485e-4281-85c0-d70856550c8a)
2026-01-08 20:33:59,207 - app.services.context.monitoring_integration - INFO - ✅ ContextManager监控收集器已初始化
2026-01-08 20:33:59,212 - app.services.context.store - INFO - [ContextStore] Redis连接成功
2026-01-08 20:33:59,237 - app.services.context.manager - INFO - [ContextManager] 创建新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:87ec1ffa-7d94-4d36-a773-227a8195ea36:68977cdc-485e-4281-85c0-d70856550c8a
2026-01-08 20:33:59,769 - app.services.context.token_counter - INFO - ✅ tiktoken初始化成功，模型: gemini-2.5-pro -> cl100k_base
2026-01-08 20:33:59,770 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:87ec1ffa-7d94-4d36-a773-227a8195ea36:68977cdc-485e-4281-85c0-d70856550c8a: 0/16000 tokens
2026-01-08 20:34:02,643 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='帮我改写第一章中段融第一次成功吞噬器灵的场景（"吞噬！"那段...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:87ec1ffa-7d94-4d36-a773-227a8195ea36', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=3条
2026-01-08 20:34:02,644 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=87ec1ffa-7d94-4d36-a773-227a8195ea36 | 含用户级=True | 找到=3条
2026-01-08 20:34:02,646 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 1条消息, 0 tokens, 耗时 3437.28ms
2026-01-08 20:34:02,649 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 1 条历史消息 (token: 0)
2026-01-08 20:34:02,662 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-08 20:34:02,666 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-08 20:34:02,670 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=20, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-08 20:34:02,723 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:57192 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 20:34:05,519 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-08 20:34:05,520 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-08 20:34:05,601 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-08 20:34:05,604 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=346, cost=$0.000035, time=2853ms
2026-01-08 20:34:05,604 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=7, 尝试次数=1
2026-01-08 20:34:05,605 - app.services.agent.intent.classifier - INFO - [Intent] AI识别结果: writing
2026-01-08 20:34:05,605 - app.services.agent.langgraph_agent - INFO - [Planning] AI意图分类: writing (置信度: 0.90)
2026-01-08 20:34:05,606 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 帮我改写第一章中段融第一次成功吞噬器灵的场景（"吞噬！"那段），
  要求：
  1. 增加吞噬过程...
2026-01-08 20:34:05,613 - app.core.cache - INFO - ⚠️ 缓存未命中: prompt:planning:v2.30.0:get_planning_static_prompt:fca6eb91156619d0
2026-01-08 20:34:05,621 - app.core.cache - INFO - 💾 缓存已保存: prompt:planning:v2.30.0:get_planning_static_prompt:fca6eb91156619d0 (expire=3600s)
2026-01-08 20:34:05,625 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-08 20:34:05,627 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=story_planning, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: story_planning; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-01-08 20:34:05,628 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.3, task_type=TaskType.STORY_PLANNING
2026-01-08 20:34:24,121 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-08 20:34:28,001 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 9 个数据块，总长度: 1031
2026-01-08 20:34:28,002 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 15110 (prompt=14583, completion=527)
2026-01-08 20:34:28,003 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-08 20:34:28,004 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-08 20:34:28,029 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-08 20:34:28,031 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=15110, cost=$0.023499, time=22377ms
2026-01-08 20:34:28,033 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=15110
2026-01-08 20:34:28,036 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户想要改写第一章中的一个特定场景，期望得到一段符合新要求的, 原料=为了准确改写，我需要获取第一章的完整内容, 处理=首先，读取第一章的原文。然后，将原文内容
2026-01-08 20:34:28,057 - app.services.agent.planning.plan_generator - INFO - [PlanValidator] 检测到人物查询'身体感受'但未指定章节，自动插入搜索任务
2026-01-08 20:34:28,060 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共3个任务
2026-01-08 20:34:28,062 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共3个任务，耗时: 22.46s
2026-01-08 20:34:28,064 - app.api.v1.agent - INFO - [Stream] Plan tasks: 3 items
2026-01-08 20:34:28,065 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2026-01-08 20:34:28,088 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2026-01-08 20:34:28,090 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2026-01-08 20:34:28,091 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 任务分组: 第一层并行=2, 第二层并行=0, 串行=1
2026-01-08 20:34:28,093 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始第一层并行执行2个任务
2026-01-08 20:34:28,096 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务1开始: 搜索'身体感受'出现位置
2026-01-08 20:34:28,100 - app.api.v1.agent - INFO - [Stream] Task started: 搜索'身体感受'出现位置 (icon=Search)
2026-01-08 20:34:28,102 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(search_analysis_fragments)
2026-01-08 20:34:28,107 - app.services.agent.tools.tool_types - INFO - [search_analysis_fragments] 开始执行工具
2026-01-08 20:34:28,136 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务2开始: 读取第一章的原文，以获取“吞噬器灵”场景的上下文。
2026-01-08 20:34:28,137 - app.api.v1.agent - INFO - [Stream] Task started: 读取第一章的原文，以获取“吞噬器灵”场景的上下文。 (icon=FileText)
2026-01-08 20:34:28,139 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(get_chapter_by_order)
2026-01-08 20:34:28,142 - app.services.agent.tools.tool_types - INFO - [get_chapter_by_order] 开始执行工具
2026-01-08 20:34:31,088 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=87ec1ffa-7d94-4d36-a773-227a8195ea36, current_order=1, query=身体感受...
2026-01-08 20:34:31,765 - app.services.chapter_vector_service - INFO - RAG retrieved 10 segments within order<=3
Building prefix dict from the default dictionary ...
2026-01-08 20:34:31,769 - jieba - DEBUG - Building prefix dict from the default dictionary ...
Loading model from cache D:\Temp\jieba.cache
2026-01-08 20:34:31,775 - jieba - DEBUG - Loading model from cache D:\Temp\jieba.cache
Loading model cost 2.376 seconds.
2026-01-08 20:34:34,149 - jieba - DEBUG - Loading model cost 2.376 seconds.
Prefix dict has been built successfully.
2026-01-08 20:34:34,152 - jieba - DEBUG - Prefix dict has been built successfully.
2026-01-08 20:34:34,192 - app.services.agent.langgraph_tools - INFO - [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
2026-01-08 20:34:34,322 - app.services.agent.tools.tool_types - INFO - [search_analysis_fragments] 执行成功 (耗时: 6.216s)
2026-01-08 20:34:34,325 - app.services.agent.tools.tool_monitor - INFO - ToolMonitor initialized with Memory storage, retention: 7 days
2026-01-08 20:34:34,328 - app.services.agent.execution.task_runner - INFO - [TaskRunner] search_analysis_fragments 执行成功（DeepAgent模式）
2026-01-08 20:34:34,332 - app.api.v1.agent - INFO - [Stream] 任务完成: 搜索'身体感受'出现位置 (6.2s)
2026-01-08 20:34:34,332 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务1完成
2026-01-08 20:34:34,439 - app.services.agent.langgraph_tools - INFO - [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
2026-01-08 20:34:34,450 - app.services.agent.tools.tool_types - INFO - [get_chapter_by_order] 执行成功 (耗时: 6.308s)
2026-01-08 20:34:34,453 - app.services.agent.execution.task_runner - INFO - [TaskRunner] get_chapter_by_order 执行成功（DeepAgent模式）
2026-01-08 20:34:34,456 - app.api.v1.agent - INFO - [Stream] 任务完成: 读取第一章的原文，以获取“吞噬器灵”场景的上下文。 (6.3s)
2026-01-08 20:34:34,460 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务2完成
2026-01-08 20:34:34,468 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始串行执行1个任务
2026-01-08 20:34:34,474 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务3开始: 根据用户要求，对“吞噬器灵”的场景进行改写，增加身体感受、紧张感和惊喜情绪。
2026-01-08 20:34:34,480 - app.api.v1.agent - INFO - [Stream] Task started: 根据用户要求，对“吞噬器灵”的场景进行改写，增加身体感受、紧张感和惊喜情绪。 (icon=PenTool)
2026-01-08 20:34:34,484 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(continue_writing)
2026-01-08 20:34:34,487 - app.services.agent.tools.tool_types - INFO - [continue_writing] 开始执行工具
2026-01-08 20:34:34,529 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-08 20:34:34,531 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=content_creation, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: content_creation; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-01-08 20:34:34,534 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=4000, temp=0.8, task_type=TaskType.CONTENT_CREATION
2026-01-08 20:34:34,544 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:52762 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 20:34:35,886 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:64069 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 20:34:54,142 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-08 20:35:01,527 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:50167 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 20:35:13,406 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 27 个数据块，总长度: 2164
2026-01-08 20:35:13,408 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 5304 (prompt=3607, completion=1697)
2026-01-08 20:35:13,408 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-08 20:35:13,409 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-08 20:35:13,434 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-08 20:35:13,436 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=5304, cost=$0.021479, time=38870ms
2026-01-08 20:35:13,438 - app.services.agent.tools.tool_types - INFO - [continue_writing] 执行成功 (耗时: 38.951s)
2026-01-08 20:35:13,440 - app.services.agent.execution.task_runner - INFO - [TaskRunner] continue_writing 执行成功（DeepAgent模式）
2026-01-08 20:35:13,441 - app.api.v1.agent - INFO - [Stream] 任务完成: 根据用户要求，对“吞噬器灵”的场景进行改写，增加身体感受、紧张感和惊喜情绪。 (39.0s)
2026-01-08 20:35:13,442 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务3完成
2026-01-08 20:35:13,443 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共3个任务，耗时: 45.38s
2026-01-08 20:35:13,444 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2026-01-08 20:35:13,447 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=2, 输出型=1, 展示型=0
2026-01-08 20:35:13,449 - app.services.agent.langgraph_agent - INFO - [Response] 单个输出任务(continue_writing_tool)，使用AI整合
2026-01-08 20:35:13,451 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2026-01-08 20:35:13,452 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=2, 输出型=1, 展示型=0
2026-01-08 20:35:13,454 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=7652字符, 处理后=5534字符
2026-01-08 20:35:13,454 - app.services.agent.planning.response_builder - INFO - [Summarization] 准备发送 summarization_start 事件
2026-01-08 20:35:13,455 - app.services.agent.stream.stream_event_handler - INFO - [StreamEventHandler] emit_summarization_start 被调用, _on_flow_event=True
2026-01-08 20:35:13,455 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_start 事件已发送
2026-01-08 20:35:13,457 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2026-01-08 20:35:13,457 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2026-01-08 20:35:13,466 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-08 20:35:13,467 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-08 20:35:13,467 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
2026-01-08 20:35:31,532 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:54034 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 20:35:35,856 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:55344 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 20:35:37,547 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-08 20:35:37,549 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_complete 事件已发送（第一个chunk时）
2026-01-08 20:35:37,549 - app.services.agent.planning.response_builder - INFO - [Summarization] output_ready 事件已发送（第一个chunk时）
2026-01-08 20:35:41,002 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 15 个数据块，总长度: 1242
2026-01-08 20:35:41,003 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 7484 (prompt=6544, completion=940)
2026-01-08 20:35:41,004 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-08 20:35:41,004 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-08 20:35:41,030 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-08 20:35:41,032 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=7484, cost=$0.004313, time=27537ms
2026-01-08 20:35:41,033 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=1242
2026-01-08 20:35:46,273 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:87ec1ffa-7d94-4d36-a773-227a8195ea36 | 重要度=0.84
2026-01-08 20:35:50,796 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:87ec1ffa-7d94-4d36-a773-227a8195ea36 | 重要度=0.77
2026-01-08 20:35:50,817 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:87ec1ffa-7d94-4d36-a773-227a8195ea36:68977cdc-485e-4281-85c0-d70856550c8a, token=1718
2026-01-08 20:35:50,819 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:87ec1ffa-7d94-4d36-a773-227a8195ea36:68977cdc-485e-4281-85c0-d70856550c8a, 消息数=2, Token=1718
2026-01-08 20:35:50,819 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:87ec1ffa-7d94-4d36-a773-227a8195ea36:68977cdc-485e-4281-85c0-d70856550c8a)
2026-01-08 20:35:50,820 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2026-01-08 20:35:50,832 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed
2026-01-08 20:36:01,531 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:59810 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 20:36:31,526 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:56776 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 20:36:35,849 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:60596 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 20:37:01,519 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:50064 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 20:37:31,527 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:63852 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 20:37:35,844 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:50730 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 20:38:01,526 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:52048 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 20:38:31,526 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:58617 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 20:38:35,846 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:56454 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 20:39:01,522 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:49467 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 20:39:31,523 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:51833 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 20:39:35,849 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:52745 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 20:40:01,525 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:54594 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 20:40:31,522 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:64672 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 20:40:35,841 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:52241 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 20:41:01,516 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:55175 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 20:41:31,515 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:56112 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 20:41:35,835 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:51924 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 20:42:01,517 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:50642 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 20:42:31,516 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:63685 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 20:42:35,843 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:62377 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 20:43:01,521 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:62458 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 20:43:31,517 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:56495 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 20:43:35,843 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:60900 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 20:44:01,518 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:51054 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 20:44:31,520 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:50479 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 20:44:35,839 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:51884 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 20:45:01,515 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:51274 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 20:45:31,520 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:59497 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 20:45:35,854 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:60255 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 20:46:01,518 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:51477 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 20:46:31,516 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:61546 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 20:46:35,849 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:49778 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 20:47:01,520 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:58762 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 20:47:31,521 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:62451 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 20:47:35,856 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:51200 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 20:48:01,521 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:61803 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 20:48:31,516 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:54901 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 20:48:35,840 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:53927 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 20:49:01,517 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:62778 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 20:49:31,517 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:56639 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 20:49:35,842 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:55739 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 20:50:01,517 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:63936 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 20:50:31,521 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:63822 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 20:50:35,842 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:53758 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 20:51:01,522 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:53014 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 20:51:21,431 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:61438 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
INFO:     connection closed
INFO:     connection closed
2026-01-08 21:20:19,137 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/auth/refresh
INFO:     127.0.0.1:60604 - "POST /api/v1/auth/refresh HTTP/1.1" 200 OK
2026-01-08 21:20:26,222 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/auth/refresh
INFO:     127.0.0.1:63777 - "POST /api/v1/auth/refresh HTTP/1.1" 200 OK
INFO:     ('127.0.0.1', 49327) - "WebSocket /api/v1/ws/notifications/79913e7e-d5cd-4e09-bce6-ca6639bd8456" [accepted]
2026-01-08 21:20:29,172 - app.api.v1.ws - INFO - [WebSocket] 通知连接建立: user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
INFO:     connection open
2026-01-08 21:20:29,660 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:49326 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 21:20:29,884 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:63945 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
INFO:     connection closed
INFO:     ('127.0.0.1', 63606) - "WebSocket /api/v1/ws/notifications/79913e7e-d5cd-4e09-bce6-ca6639bd8456" [accepted]
2026-01-08 21:20:34,454 - app.api.v1.ws - INFO - [WebSocket] 通知连接建立: user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
INFO:     connection open
INFO:     ('127.0.0.1', 51596) - "WebSocket /api/v1/ws/notifications/79913e7e-d5cd-4e09-bce6-ca6639bd8456" [accepted]
2026-01-08 21:20:34,478 - app.api.v1.ws - INFO - [WebSocket] 通知连接建立: user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
INFO:     connection open
INFO:     connection closed
2026-01-08 21:20:34,700 - app.api.v1.ws - ERROR - [WebSocket] 通知推送错误:
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\uvicorn\protocols\websockets\websockets_impl.py", line 349, in asgi_send
    await self.send(data)  # type: ignore[arg-type]
    ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\websockets\legacy\protocol.py", line 620, in send
    await self.ensure_open()
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\websockets\legacy\protocol.py", line 921, in ensure_open
    raise self.connection_closed_exc()
websockets.exceptions.ConnectionClosedOK: received 1001 (going away); then sent 1001 (going away)

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\api\v1\ws.py", line 320, in notifications_stream
    await websocket.send_json({
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\websockets.py", line 173, in send_json
    await self.send({"type": "websocket.send", "text": text})
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\websockets.py", line 85, in send
    await self._send(message)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\_exception_handler.py", line 50, in sender
    await send(message)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\uvicorn\protocols\websockets\websockets_impl.py", line 365, in asgi_send
    raise ClientDisconnected from exc
uvicorn.protocols.utils.ClientDisconnected
INFO:     ('127.0.0.1', 52553) - "WebSocket /api/v1/ws/notifications/79913e7e-d5cd-4e09-bce6-ca6639bd8456" [accepted]
2026-01-08 21:20:35,176 - app.api.v1.ws - INFO - [WebSocket] 通知连接建立: user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
INFO:     connection open
INFO:     ('127.0.0.1', 55435) - "WebSocket /api/v1/ws/notifications/79913e7e-d5cd-4e09-bce6-ca6639bd8456" [accepted]
2026-01-08 21:20:35,210 - app.api.v1.ws - INFO - [WebSocket] 通知连接建立: user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
INFO:     connection open
INFO:     connection closed
2026-01-08 21:20:35,731 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:55437 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 21:20:35,785 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:55439 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 21:20:36,629 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:64207 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 21:20:36,657 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:64209 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 21:20:40,484 - app.api.v1.chapters - INFO - [GET chapters] work_id=87ec1ffa-7d94-4d36-a773-227a8195ea36, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
INFO:     ('127.0.0.1', 62764) - "WebSocket /api/v1/ws/notifications/79913e7e-d5cd-4e09-bce6-ca6639bd8456" [accepted]
2026-01-08 21:20:40,534 - app.api.v1.ws - INFO - [WebSocket] 通知连接建立: user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
INFO:     connection open
2026-01-08 21:20:40,825 - app.api.v1.chapters - INFO - ⚠️ [GET chapters] 缓存未命中: chapters:work:87ec1ffa-7d94-4d36-a773-227a8195ea36
2026-01-08 21:20:40,828 - app.services.chapter_service - INFO - [ChapterService] Querying chapters for work_id=87ec1ffa-7d94-4d36-a773-227a8195ea36, type=<class 'uuid.UUID'>
INFO:     ('127.0.0.1', 61375) - "WebSocket /api/v1/ws/notifications/79913e7e-d5cd-4e09-bce6-ca6639bd8456" [accepted]
2026-01-08 21:20:40,908 - app.api.v1.ws - INFO - [WebSocket] 通知连接建立: user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
INFO:     connection open
2026-01-08 21:20:40,915 - app.services.chapter_service - INFO - [ChapterService] Found 5 chapters
2026-01-08 21:20:40,916 - app.services.chapter_service - INFO -   - Chapter: 第1章 吞噬, order=1
2026-01-08 21:20:40,916 - app.services.chapter_service - INFO -   - ... (3 more chapters)
2026-01-08 21:20:40,916 - app.services.chapter_service - INFO -   - Chapter: 第5章 太一门, order=5
2026-01-08 21:20:40,917 - app.api.v1.chapters - INFO - [GET chapters] Returning 5 chapters
2026-01-08 21:20:40,941 - app.api.v1.chapters - INFO - 💾 [GET chapters] 缓存已保存: chapters:work:87ec1ffa-7d94-4d36-a773-227a8195ea36 (expire=60s)
2026-01-08 21:20:40,956 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:guidelines:87ec1ffa-7d94-4d36-a773-227a8195ea36 (expire=300s)
2026-01-08 21:20:40,964 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:locations:87ec1ffa-7d94-4d36-a773-227a8195ea36 (expire=300s)
2026-01-08 21:20:40,972 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works/87ec1ffa-7d94-4d36-a773-227a8195ea36
INFO:     127.0.0.1:62918 - "GET /api/v1/works/87ec1ffa-7d94-4d36-a773-227a8195ea36 HTTP/1.1" 200 OK
2026-01-08 21:20:41,051 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/work/87ec1ffa-7d94-4d36-a773-227a8195ea36
2026-01-08 21:20:41,052 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/87ec1ffa-7d94-4d36-a773-227a8195ea36/guidelines
2026-01-08 21:20:41,055 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/87ec1ffa-7d94-4d36-a773-227a8195ea36/locations
INFO:     127.0.0.1:62919 - "GET /api/v1/chapters/work/87ec1ffa-7d94-4d36-a773-227a8195ea36 HTTP/1.1" 200 OK
INFO:     127.0.0.1:62927 - "GET /api/v1/worldview/works/87ec1ffa-7d94-4d36-a773-227a8195ea36/guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:62926 - "GET /api/v1/worldview/works/87ec1ffa-7d94-4d36-a773-227a8195ea36/locations HTTP/1.1" 200 OK
2026-01-08 21:20:41,134 - app.api.v1.chapters - INFO - [GET chapters] work_id=87ec1ffa-7d94-4d36-a773-227a8195ea36, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-08 21:20:41,155 - app.api.v1.chapters - INFO - ✅ [GET chapters] 缓存命中: chapters:work:87ec1ffa-7d94-4d36-a773-227a8195ea36
2026-01-08 21:20:41,168 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:guidelines:87ec1ffa-7d94-4d36-a773-227a8195ea36
2026-01-08 21:20:41,177 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:ai-guidelines:87ec1ffa-7d94-4d36-a773-227a8195ea36 (expire=300s)
2026-01-08 21:20:41,184 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/work/87ec1ffa-7d94-4d36-a773-227a8195ea36
2026-01-08 21:20:41,185 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works/87ec1ffa-7d94-4d36-a773-227a8195ea36
2026-01-08 21:20:41,186 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/87ec1ffa-7d94-4d36-a773-227a8195ea36/guidelines
2026-01-08 21:20:41,187 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/87ec1ffa-7d94-4d36-a773-227a8195ea36/ai-guidelines
INFO:     127.0.0.1:52109 - "GET /api/v1/chapters/work/87ec1ffa-7d94-4d36-a773-227a8195ea36 HTTP/1.1" 200 OK
INFO:     127.0.0.1:52107 - "GET /api/v1/works/87ec1ffa-7d94-4d36-a773-227a8195ea36 HTTP/1.1" 200 OK
INFO:     127.0.0.1:52110 - "GET /api/v1/worldview/works/87ec1ffa-7d94-4d36-a773-227a8195ea36/guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:54437 - "GET /api/v1/worldview/works/87ec1ffa-7d94-4d36-a773-227a8195ea36/ai-guidelines HTTP/1.1" 200 OK
2026-01-08 21:20:41,242 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:characters:87ec1ffa-7d94-4d36-a773-227a8195ea36 (expire=300s)
2026-01-08 21:20:41,254 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:settings:87ec1ffa-7d94-4d36-a773-227a8195ea36 (expire=300s)
2026-01-08 21:20:41,267 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:locations:87ec1ffa-7d94-4d36-a773-227a8195ea36
2026-01-08 21:20:41,272 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/87ec1ffa-7d94-4d36-a773-227a8195ea36/characters
2026-01-08 21:20:41,276 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:ai-guidelines:87ec1ffa-7d94-4d36-a773-227a8195ea36
2026-01-08 21:20:41,279 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/87ec1ffa-7d94-4d36-a773-227a8195ea36/settings
INFO:     127.0.0.1:62925 - "GET /api/v1/worldview/works/87ec1ffa-7d94-4d36-a773-227a8195ea36/characters HTTP/1.1" 200 OK
2026-01-08 21:20:41,283 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/87ec1ffa-7d94-4d36-a773-227a8195ea36/locations
INFO:     127.0.0.1:62924 - "GET /api/v1/worldview/works/87ec1ffa-7d94-4d36-a773-227a8195ea36/settings HTTP/1.1" 200 OK
2026-01-08 21:20:41,286 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/87ec1ffa-7d94-4d36-a773-227a8195ea36/ai-guidelines
INFO:     127.0.0.1:64646 - "GET /api/v1/worldview/works/87ec1ffa-7d94-4d36-a773-227a8195ea36/locations HTTP/1.1" 200 OK
INFO:     127.0.0.1:64648 - "GET /api/v1/worldview/works/87ec1ffa-7d94-4d36-a773-227a8195ea36/ai-guidelines HTTP/1.1" 200 OK
2026-01-08 21:20:41,318 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:characters:87ec1ffa-7d94-4d36-a773-227a8195ea36
2026-01-08 21:20:41,326 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:settings:87ec1ffa-7d94-4d36-a773-227a8195ea36
2026-01-08 21:20:41,327 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/87ec1ffa-7d94-4d36-a773-227a8195ea36/characters
INFO:     127.0.0.1:64652 - "GET /api/v1/worldview/works/87ec1ffa-7d94-4d36-a773-227a8195ea36/characters HTTP/1.1" 200 OK
2026-01-08 21:20:41,330 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/87ec1ffa-7d94-4d36-a773-227a8195ea36/settings
INFO:     127.0.0.1:64654 - "GET /api/v1/worldview/works/87ec1ffa-7d94-4d36-a773-227a8195ea36/settings HTTP/1.1" 200 OK
2026-01-08 21:20:41,850 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 87ec1ffa-7d94-4d36-a773-227a8195ea36, chapter_id: 33034895-ef52-4fca-80d8-2ec3a8f04644
2026-01-08 21:20:41,868 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 33034895-ef52-4fca-80d8-2ec3a8f04644
2026-01-08 21:20:41,868 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
2026-01-08 21:20:41,870 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:53886 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-08 21:20:41,906 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 87ec1ffa-7d94-4d36-a773-227a8195ea36, chapter_id: 33034895-ef52-4fca-80d8-2ec3a8f04644
2026-01-08 21:20:41,918 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 33034895-ef52-4fca-80d8-2ec3a8f04644
2026-01-08 21:20:41,918 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
2026-01-08 21:20:41,920 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:49557 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-08 21:20:42,349 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works/87ec1ffa-7d94-4d36-a773-227a8195ea36
INFO:     127.0.0.1:54267 - "GET /api/v1/works/87ec1ffa-7d94-4d36-a773-227a8195ea36 HTTP/1.1" 200 OK
2026-01-08 21:20:42,372 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:locations:87ec1ffa-7d94-4d36-a773-227a8195ea36
2026-01-08 21:20:42,379 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:characters:87ec1ffa-7d94-4d36-a773-227a8195ea36
2026-01-08 21:20:42,381 - app.api.v1.chapters - INFO - [GET chapters] work_id=87ec1ffa-7d94-4d36-a773-227a8195ea36, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-08 21:20:42,386 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:settings:87ec1ffa-7d94-4d36-a773-227a8195ea36
2026-01-08 21:20:42,391 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:guidelines:87ec1ffa-7d94-4d36-a773-227a8195ea36
2026-01-08 21:20:42,395 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/87ec1ffa-7d94-4d36-a773-227a8195ea36/locations
2026-01-08 21:20:42,396 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/87ec1ffa-7d94-4d36-a773-227a8195ea36/characters
2026-01-08 21:20:42,397 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/87ec1ffa-7d94-4d36-a773-227a8195ea36/settings
2026-01-08 21:20:42,399 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/87ec1ffa-7d94-4d36-a773-227a8195ea36/guidelines
INFO:     127.0.0.1:57931 - "GET /api/v1/worldview/works/87ec1ffa-7d94-4d36-a773-227a8195ea36/locations HTTP/1.1" 200 OK
INFO:     127.0.0.1:57930 - "GET /api/v1/worldview/works/87ec1ffa-7d94-4d36-a773-227a8195ea36/characters HTTP/1.1" 200 OK
INFO:     127.0.0.1:57932 - "GET /api/v1/worldview/works/87ec1ffa-7d94-4d36-a773-227a8195ea36/settings HTTP/1.1" 200 OK
INFO:     127.0.0.1:57933 - "GET /api/v1/worldview/works/87ec1ffa-7d94-4d36-a773-227a8195ea36/guidelines HTTP/1.1" 200 OK
2026-01-08 21:20:42,418 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:ai-guidelines:87ec1ffa-7d94-4d36-a773-227a8195ea36
2026-01-08 21:20:42,429 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/87ec1ffa-7d94-4d36-a773-227a8195ea36/ai-guidelines
INFO:     127.0.0.1:57183 - "GET /api/v1/worldview/works/87ec1ffa-7d94-4d36-a773-227a8195ea36/ai-guidelines HTTP/1.1" 200 OK
2026-01-08 21:20:42,446 - app.api.v1.chapters - INFO - ✅ [GET chapters] 缓存命中: chapters:work:87ec1ffa-7d94-4d36-a773-227a8195ea36
2026-01-08 21:20:42,461 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:locations:87ec1ffa-7d94-4d36-a773-227a8195ea36
2026-01-08 21:20:42,468 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:settings:87ec1ffa-7d94-4d36-a773-227a8195ea36
2026-01-08 21:20:42,470 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/work/87ec1ffa-7d94-4d36-a773-227a8195ea36
2026-01-08 21:20:42,475 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:characters:87ec1ffa-7d94-4d36-a773-227a8195ea36
2026-01-08 21:20:42,477 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works/87ec1ffa-7d94-4d36-a773-227a8195ea36
INFO:     127.0.0.1:57929 - "GET /api/v1/chapters/work/87ec1ffa-7d94-4d36-a773-227a8195ea36 HTTP/1.1" 200 OK
2026-01-08 21:20:42,480 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/87ec1ffa-7d94-4d36-a773-227a8195ea36/locations
INFO:     127.0.0.1:63268 - "GET /api/v1/works/87ec1ffa-7d94-4d36-a773-227a8195ea36 HTTP/1.1" 200 OK
2026-01-08 21:20:42,485 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/87ec1ffa-7d94-4d36-a773-227a8195ea36/settings
2026-01-08 21:20:42,486 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/87ec1ffa-7d94-4d36-a773-227a8195ea36/characters
INFO:     127.0.0.1:58182 - "GET /api/v1/worldview/works/87ec1ffa-7d94-4d36-a773-227a8195ea36/locations HTTP/1.1" 200 OK
INFO:     127.0.0.1:58186 - "GET /api/v1/worldview/works/87ec1ffa-7d94-4d36-a773-227a8195ea36/settings HTTP/1.1" 200 OK
INFO:     127.0.0.1:58185 - "GET /api/v1/worldview/works/87ec1ffa-7d94-4d36-a773-227a8195ea36/characters HTTP/1.1" 200 OK
2026-01-08 21:20:42,507 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:guidelines:87ec1ffa-7d94-4d36-a773-227a8195ea36
2026-01-08 21:20:42,512 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/87ec1ffa-7d94-4d36-a773-227a8195ea36/guidelines
2026-01-08 21:20:42,515 - app.api.v1.chapters - INFO - [GET chapters] work_id=87ec1ffa-7d94-4d36-a773-227a8195ea36, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
INFO:     127.0.0.1:61528 - "GET /api/v1/worldview/works/87ec1ffa-7d94-4d36-a773-227a8195ea36/guidelines HTTP/1.1" 200 OK
2026-01-08 21:20:42,520 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:ai-guidelines:87ec1ffa-7d94-4d36-a773-227a8195ea36
2026-01-08 21:20:42,532 - app.api.v1.chapters - INFO - ✅ [GET chapters] 缓存命中: chapters:work:87ec1ffa-7d94-4d36-a773-227a8195ea36
2026-01-08 21:20:42,534 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/87ec1ffa-7d94-4d36-a773-227a8195ea36/ai-guidelines
INFO:     127.0.0.1:65360 - "GET /api/v1/worldview/works/87ec1ffa-7d94-4d36-a773-227a8195ea36/ai-guidelines HTTP/1.1" 200 OK
2026-01-08 21:20:42,537 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/work/87ec1ffa-7d94-4d36-a773-227a8195ea36
INFO:     127.0.0.1:65362 - "GET /api/v1/chapters/work/87ec1ffa-7d94-4d36-a773-227a8195ea36 HTTP/1.1" 200 OK
2026-01-08 21:20:43,026 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 87ec1ffa-7d94-4d36-a773-227a8195ea36, chapter_id: 33034895-ef52-4fca-80d8-2ec3a8f04644
2026-01-08 21:20:43,037 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 33034895-ef52-4fca-80d8-2ec3a8f04644
2026-01-08 21:20:43,038 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
2026-01-08 21:20:43,039 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:65391 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-08 21:20:43,213 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/analysis/works/87ec1ffa-7d94-4d36-a773-227a8195ea36/status
2026-01-08 21:20:43,217 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 87ec1ffa-7d94-4d36-a773-227a8195ea36, chapter_id: 33034895-ef52-4fca-80d8-2ec3a8f04644
INFO:     127.0.0.1:52827 - "GET /api/v1/analysis/works/87ec1ffa-7d94-4d36-a773-227a8195ea36/status HTTP/1.1" 404 Not Found
2026-01-08 21:20:43,240 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 33034895-ef52-4fca-80d8-2ec3a8f04644
2026-01-08 21:20:43,241 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
2026-01-08 21:20:43,243 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:55166 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-08 21:20:43,332 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:87ec1ffa-7d94-4d36-a773-227a8195ea36
2026-01-08 21:20:43,337 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/33034895-ef52-4fca-80d8-2ec3a8f04644
INFO:     127.0.0.1:52829 - "PUT /api/v1/chapters/33034895-ef52-4fca-80d8-2ec3a8f04644 HTTP/1.1" 200 OK
2026-01-08 21:20:43,340 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-08 21:20:44,915 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/analysis/works/87ec1ffa-7d94-4d36-a773-227a8195ea36/status
INFO:     127.0.0.1:63564 - "GET /api/v1/analysis/works/87ec1ffa-7d94-4d36-a773-227a8195ea36/status HTTP/1.1" 404 Not Found
2026-01-08 21:20:44,937 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (5 chunks)
2026-01-08 21:20:44,961 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:87ec1ffa-7d94-4d36-a773-227a8195ea36
2026-01-08 21:20:44,962 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/33034895-ef52-4fca-80d8-2ec3a8f04644
INFO:     127.0.0.1:55271 - "PUT /api/v1/chapters/33034895-ef52-4fca-80d8-2ec3a8f04644 HTTP/1.1" 200 OK
2026-01-08 21:20:44,963 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-08 21:20:45,422 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/analysis/works/87ec1ffa-7d94-4d36-a773-227a8195ea36/status
INFO:     127.0.0.1:58809 - "GET /api/v1/analysis/works/87ec1ffa-7d94-4d36-a773-227a8195ea36/status HTTP/1.1" 404 Not Found
2026-01-08 21:20:45,432 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (5 chunks)
2026-01-08 21:20:45,471 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:87ec1ffa-7d94-4d36-a773-227a8195ea36
2026-01-08 21:20:45,472 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/33034895-ef52-4fca-80d8-2ec3a8f04644
INFO:     127.0.0.1:58425 - "PUT /api/v1/chapters/33034895-ef52-4fca-80d8-2ec3a8f04644 HTTP/1.1" 200 OK
2026-01-08 21:20:45,473 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-08 21:20:45,921 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/analysis/works/87ec1ffa-7d94-4d36-a773-227a8195ea36/status
INFO:     127.0.0.1:60223 - "GET /api/v1/analysis/works/87ec1ffa-7d94-4d36-a773-227a8195ea36/status HTTP/1.1" 404 Not Found
2026-01-08 21:20:45,924 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (5 chunks)
2026-01-08 21:20:46,209 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:87ec1ffa-7d94-4d36-a773-227a8195ea36
2026-01-08 21:20:46,209 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/33034895-ef52-4fca-80d8-2ec3a8f04644
INFO:     127.0.0.1:56308 - "PUT /api/v1/chapters/33034895-ef52-4fca-80d8-2ec3a8f04644 HTTP/1.1" 200 OK
2026-01-08 21:20:46,211 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-08 21:20:46,684 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (5 chunks)
2026-01-08 21:21:09,479 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:52848 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 21:21:11,009 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:56971 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 21:21:37,762 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:55651 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 21:21:45,231 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:59255 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 21:22:06,577 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:63568 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 21:22:07,545 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:55108 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 21:22:36,579 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:63259 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 21:22:37,535 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:49648 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 21:23:05,641 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:59458 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 21:23:07,526 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:65482 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 21:23:35,640 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:54278 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 21:23:37,523 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:59035 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 21:24:05,613 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:62379 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 21:24:35,533 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:63965 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 21:24:36,532 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:61812 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 21:24:41,106 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 87ec1ffa-7d94-4d36-a773-227a8195ea36, chapter_id: 5b2703fd-c805-4bae-a06b-3eedeafd2c8f
2026-01-08 21:24:41,157 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 5b2703fd-c805-4bae-a06b-3eedeafd2c8f
2026-01-08 21:24:41,208 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 87ec1ffa-7d94-4d36-a773-227a8195ea36, chapter_id: 5b2703fd-c805-4bae-a06b-3eedeafd2c8f
2026-01-08 21:24:41,263 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: 33034895-ef52-4fca-80d8-2ec3a8f04644
2026-01-08 21:24:41,263 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-08 21:24:41,277 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:64009 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-08 21:24:41,289 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 5b2703fd-c805-4bae-a06b-3eedeafd2c8f
2026-01-08 21:24:41,317 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: 33034895-ef52-4fca-80d8-2ec3a8f04644
2026-01-08 21:24:41,318 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-08 21:24:41,331 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:61838 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-08 21:24:41,578 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:61840 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2026-01-08 21:24:41,696 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:87ec1ffa-7d94-4d36-a773-227a8195ea36
2026-01-08 21:24:41,712 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/5b2703fd-c805-4bae-a06b-3eedeafd2c8f
INFO:     127.0.0.1:52308 - "PUT /api/v1/chapters/5b2703fd-c805-4bae-a06b-3eedeafd2c8f HTTP/1.1" 200 OK
2026-01-08 21:24:41,716 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第2章 浑圆桩 (order=2)
2026-01-08 21:24:43,930 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第2章 浑圆桩 (5 chunks)
2026-01-08 21:24:43,935 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:87ec1ffa-7d94-4d36-a773-227a8195ea36
2026-01-08 21:24:43,937 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/5b2703fd-c805-4bae-a06b-3eedeafd2c8f
INFO:     127.0.0.1:54868 - "PUT /api/v1/chapters/5b2703fd-c805-4bae-a06b-3eedeafd2c8f HTTP/1.1" 200 OK
2026-01-08 21:24:43,938 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第2章 浑圆桩 (order=2)
2026-01-08 21:24:44,650 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第2章 浑圆桩 (5 chunks)
2026-01-08 21:24:45,295 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:55676 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2026-01-08 21:24:45,341 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-08 21:24:45,343 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-08 21:24:45,347 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2026-01-08 21:24:49,380 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-08 21:24:49,400 - app.api.v1.agent - INFO - [Chat Stream] Mode: planning
2026-01-08 21:24:49,423 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:51132 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2026-01-08 21:24:49,449 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 续写第二章的末尾，段融站桩时脑子里那团"东西"逐渐消化，
  他开始感知到五虎群羊刀法的精髓，约 5...
2026-01-08 21:24:49,508 - app.api.v1.agent - INFO - [agent_chat_stream] 📚 世界观数据已注入: 人物=11, 地点=7, 设定=6, 规范=无
2026-01-08 21:24:49,528 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:87ec1ffa-7d94-4d36-a773-227a8195ea36:3fd5fa38-9980-42bf-ab96-8bdc6f801b81 (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=87ec1ffa-7d94-4d36-a773-227a8195ea36, conversation_id=3fd5fa38-9980-42bf-ab96-8bdc6f801b81)
2026-01-08 21:24:49,564 - app.services.context.manager - INFO - [ContextManager] 创建新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:87ec1ffa-7d94-4d36-a773-227a8195ea36:3fd5fa38-9980-42bf-ab96-8bdc6f801b81
2026-01-08 21:24:49,569 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:87ec1ffa-7d94-4d36-a773-227a8195ea36:3fd5fa38-9980-42bf-ab96-8bdc6f801b81: 0/16000 tokens
2026-01-08 21:24:50,499 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='续写第二章的末尾，段融站桩时脑子里那团"东西"逐渐消化，
 ...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:87ec1ffa-7d94-4d36-a773-227a8195ea36', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=3条
2026-01-08 21:24:50,501 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=87ec1ffa-7d94-4d36-a773-227a8195ea36 | 含用户级=True | 找到=3条
2026-01-08 21:24:50,509 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 1条消息, 0 tokens, 耗时 969.59ms
2026-01-08 21:24:50,511 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 1 条历史消息 (token: 0)
2026-01-08 21:24:50,537 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-08 21:24:50,543 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-08 21:24:50,547 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=20, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-08 21:24:52,786 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-08 21:24:52,787 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-08 21:24:52,856 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-08 21:24:52,858 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=323, cost=$0.000033, time=2243ms
2026-01-08 21:24:52,859 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=7, 尝试次数=1
2026-01-08 21:24:52,862 - app.services.agent.intent.classifier - INFO - [Intent] AI识别结果: writing
2026-01-08 21:24:52,864 - app.services.agent.langgraph_agent - INFO - [Planning] AI意图分类: writing (置信度: 0.90)
2026-01-08 21:24:52,870 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 续写第二章的末尾，段融站桩时脑子里那团"东西"逐渐消化，
  他开始感知到五虎群羊刀法的精髓，约 5...
2026-01-08 21:24:52,889 - app.core.cache - INFO - ✅ 缓存命中: prompt:planning:v2.30.0:get_planning_static_prompt:fca6eb91156619d0
2026-01-08 21:24:52,906 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-08 21:24:52,908 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=story_planning, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: story_planning; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-01-08 21:24:52,910 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.3, task_type=TaskType.STORY_PLANNING
2026-01-08 21:25:05,588 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-08 21:25:05,622 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:52655 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 21:25:10,021 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 10 个数据块，总长度: 1207
2026-01-08 21:25:10,022 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 15212 (prompt=14603, completion=609)
2026-01-08 21:25:10,023 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-08 21:25:10,023 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-08 21:25:10,070 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-08 21:25:10,071 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=15212, cost=$0.024344, time=17114ms
2026-01-08 21:25:10,075 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=15212
2026-01-08 21:25:10,081 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户希望续写第二章的结尾，这是一个创作类请求，需要生成一段约, 原料=根据创作类请求的统一策略，需要获取三份原, 处理=这是一个创作任务，必须分阶段执行。第一阶
2026-01-08 21:25:10,085 - app.services.agent.planning.plan_generator - INFO - [Planning] 直接回答模式，答案长度: 56
2026-01-08 21:25:10,086 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共3个任务
2026-01-08 21:25:10,086 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共3个任务，耗时: 17.22s
2026-01-08 21:25:10,087 - app.api.v1.agent - INFO - [Stream] Plan tasks: 3 items
2026-01-08 21:25:10,088 - app.services.agent.langgraph_agent - WARNING - [Planning-Alert] AI 违反协议：同时返回 direct_answer(56字) 和 3 个 tasks，将执行 tasks 而忽略 direct_answer
2026-01-08 21:25:10,090 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2026-01-08 21:25:10,102 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2026-01-08 21:25:10,104 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2026-01-08 21:25:10,108 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 任务分组: 第一层并行=2, 第二层并行=0, 串行=1
2026-01-08 21:25:10,111 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始第一层并行执行2个任务
2026-01-08 21:25:10,124 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务2开始: 读取前一章（第一章）的内容，了解剧情上下文。
2026-01-08 21:25:10,137 - app.api.v1.agent - INFO - [Stream] Task started: 读取前一章（第一章）的内容，了解剧情上下文。 (icon=FileText)
2026-01-08 21:25:10,144 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(get_chapter_by_order)
2026-01-08 21:25:10,157 - app.services.agent.tools.tool_types - INFO - [get_chapter_by_order] 开始执行工具
2026-01-08 21:25:10,215 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务3开始: 读取当前章节（第二章）的已有内容，为续写做准备。
2026-01-08 21:25:10,217 - app.api.v1.agent - INFO - [Stream] Task started: 读取当前章节（第二章）的已有内容，为续写做准备。 (icon=FileText)
2026-01-08 21:25:10,220 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(get_chapter_by_order)
2026-01-08 21:25:10,222 - app.services.agent.tools.tool_types - INFO - [get_chapter_by_order] 开始执行工具
2026-01-08 21:25:10,300 - app.services.agent.langgraph_tools - INFO - [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
2026-01-08 21:25:10,316 - app.services.agent.langgraph_tools - INFO - [get_chapter_by_order_tool] ✅ 找到第2章: 第2章 浑圆桩
2026-01-08 21:25:10,322 - app.services.agent.tools.tool_types - INFO - [get_chapter_by_order] 执行成功 (耗时: 0.168s)
2026-01-08 21:25:10,337 - app.services.agent.execution.task_runner - INFO - [TaskRunner] get_chapter_by_order 执行成功（DeepAgent模式）
2026-01-08 21:25:10,346 - app.api.v1.agent - INFO - [Stream] 任务完成: 读取前一章（第一章）的内容，了解剧情上下文。 (0.2s)
2026-01-08 21:25:10,347 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务2完成
2026-01-08 21:25:10,350 - app.services.agent.tools.tool_types - INFO - [get_chapter_by_order] 执行成功 (耗时: 0.128s)
2026-01-08 21:25:10,352 - app.services.agent.execution.task_runner - INFO - [TaskRunner] get_chapter_by_order 执行成功（DeepAgent模式）
2026-01-08 21:25:10,353 - app.api.v1.agent - INFO - [Stream] 任务完成: 读取当前章节（第二章）的已有内容，为续写做准备。 (0.1s)
2026-01-08 21:25:10,355 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务3完成
2026-01-08 21:25:10,357 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始串行执行1个任务
2026-01-08 21:25:10,361 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务1开始: 获取作品的世界观、角色、设定等背景信息。
2026-01-08 21:25:10,362 - app.api.v1.agent - INFO - [Stream] Task started: 获取作品的世界观、角色、设定等背景信息。 (icon=Wrench)
2026-01-08 21:25:10,364 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: get_worldview_summary
2026-01-08 21:25:10,371 - app.services.agent.tools.tool_types - INFO - [get_worldview_summary] 开始执行工具
2026-01-08 21:25:10,420 - app.services.agent.langgraph_tools - INFO - [get_worldview_summary] ✅ 获取世界观摘要成功: {'characters': 11, 'locations': 7, 'settings': 6}
2026-01-08 21:25:10,429 - app.services.agent.tools.tool_types - INFO - [get_worldview_summary] 执行成功 (耗时: 0.059s)
2026-01-08 21:25:10,434 - app.services.agent.execution.tool_executor - INFO - [StandardTool] get_worldview_summary 执行成功
2026-01-08 21:25:10,436 - app.api.v1.agent - INFO - [Stream] 任务完成: 获取作品的世界观、角色、设定等背景信息。 (0.1s)
2026-01-08 21:25:10,437 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务1完成
2026-01-08 21:25:10,441 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共3个任务，耗时: 0.35s
2026-01-08 21:25:10,445 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2026-01-08 21:25:10,450 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=3, 输出型=0, 展示型=0
2026-01-08 21:25:10,452 - app.services.agent.langgraph_agent - INFO - [Response] 分阶段执行第一阶段，基于任务结果生成询问
2026-01-08 21:25:10,455 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2026-01-08 21:25:10,456 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=3, 输出型=0, 展示型=0
2026-01-08 21:25:10,460 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=9091字符, 处理后=4897字符
2026-01-08 21:25:10,462 - app.services.agent.planning.response_builder - INFO - [Summarization] 准备发送 summarization_start 事件
2026-01-08 21:25:10,463 - app.services.agent.stream.stream_event_handler - INFO - [StreamEventHandler] emit_summarization_start 被调用, _on_flow_event=True
2026-01-08 21:25:10,463 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_start 事件已发送
2026-01-08 21:25:10,468 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2026-01-08 21:25:10,470 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2026-01-08 21:25:10,482 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-08 21:25:10,484 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-08 21:25:10,484 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
2026-01-08 21:25:30,293 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-08 21:25:30,294 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_complete 事件已发送（第一个chunk时）
2026-01-08 21:25:30,295 - app.services.agent.planning.response_builder - INFO - [Summarization] output_ready 事件已发送（第一个chunk时）
2026-01-08 21:25:33,012 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 13 个数据块，总长度: 1063
2026-01-08 21:25:33,013 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 7376 (prompt=6574, completion=802)
2026-01-08 21:25:33,014 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-08 21:25:33,015 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-08 21:25:33,034 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-08 21:25:33,035 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=7376, cost=$0.003977, time=22530ms
2026-01-08 21:25:33,038 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=1063
2026-01-08 21:25:37,270 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:87ec1ffa-7d94-4d36-a773-227a8195ea36 | 重要度=0.65
2026-01-08 21:25:41,349 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:87ec1ffa-7d94-4d36-a773-227a8195ea36 | 重要度=0.91
2026-01-08 21:25:41,412 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:87ec1ffa-7d94-4d36-a773-227a8195ea36:3fd5fa38-9980-42bf-ab96-8bdc6f801b81, token=1476
2026-01-08 21:25:41,413 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:87ec1ffa-7d94-4d36-a773-227a8195ea36:3fd5fa38-9980-42bf-ab96-8bdc6f801b81, 消息数=2, Token=1476
2026-01-08 21:25:41,414 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:87ec1ffa-7d94-4d36-a773-227a8195ea36:3fd5fa38-9980-42bf-ab96-8bdc6f801b81)
2026-01-08 21:25:41,417 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2026-01-08 21:25:41,433 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed
2026-01-08 21:25:41,452 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:60776 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 21:25:41,470 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:52951 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2