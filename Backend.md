2026-01-08 00:37:14,772 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 请帮我梳理一下目前出现的所有武功和刀法：
  1. 列出所有提到的刀法名称和等级
  2. 分析段融...
2026-01-08 00:37:14,774 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-08 00:37:14,775 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-08 00:37:14,776 - app.services.ai.http_ai_service - INFO - [成本追踪] 初始化未传db/user_id，将使用请求上下文按需记录成本
2026-01-08 00:37:17,799 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-08 00:37:17,807 - app.services.agent.tools.writing_tools - INFO - Writing tools AI service initialized
2026-01-08 00:37:17,809 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ AI Service 已同时设置到 langgraph_tools 和 writing_tools
2026-01-08 00:37:17,816 - app.services.context.adaptive_budget - INFO - ✅ 所有预算配置验证通过
2026-01-08 00:37:29,116 - app.services.context.vector_memory_store - INFO - ✅ VectorMemoryStore初始化成功 | 目录=./data/chroma_db | 模型=paraphrase-multilingual-MiniLM-L12-v2 | 集合=user_memories
2026-01-08 00:37:29,118 - app.services.context.manager - INFO - ✅ VectorMemoryStore 已初始化
2026-01-08 00:37:29,120 - app.services.context.manager - INFO - ✅ ContextManager: 长期记忆已启用 (user_id=None)
2026-01-08 00:37:29,122 - app.services.context.manager - INFO - ✅ ContextManager: 自适应预算已启用
2026-01-08 00:37:29,123 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ ContextManager已初始化（长期记忆已启用，自适应预算已启用，总预算=16000 tokens）
成功加载模板: analyze_text (版本 3.1.0)
成功加载模板: intent_classifier (版本 2.0.0)
成功加载模板: writing_agent (版本 2.0.0)
成功加载模板: planning_agent (版本 2.0.0)
成功加载模板: tool_agent (版本 2.0.0)
成功加载模板: query_agent (版本 2.0.0)
成功加载模板: system_agent_prompt (版本 2.0.0)
成功加载模板: creative_writing_prompt (版本 1.0.0)
2026-01-08 00:37:29,378 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ PromptManager已初始化
2026-01-08 00:37:29,413 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ Redis连接验证成功
2026-01-08 00:37:29,430 - app.services.agent.langgraph_agent - INFO - [LangGraph] OK 使用 AsyncRedisSaver（redis://localhost:6379/0，TTL=7天）
2026-01-08 00:37:29,435 - app.services.agent.memory.metrics - INFO - [MemoryMetrics] 监控系统已初始化
2026-01-08 00:37:29,438 - app.services.agent.memory.long_term_store - INFO - [LongTermStore] Initialized: base_dir=./data/long_term_memory, max_size=50KB, compression=True
2026-01-08 00:37:29,439 - app.services.agent.memory.enhanced_memory_manager - INFO - EnhancedMemoryManager initialized: short=10, medium=100, threshold=0.1, long_term_backup=enabled
2026-01-08 00:37:29,440 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ EnhancedMemoryManager已创建
2026-01-08 00:37:29,443 - app.services.agent.memory.unified_coordinator - INFO - [UnifiedMemoryCoordinator] 初始化统一记忆协调器
2026-01-08 00:37:29,445 - app.services.agent.memory.unified_coordinator - INFO - [UnifiedMemoryCoordinator] 全局实例已设置
2026-01-08 00:37:29,446 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ UnifiedMemoryCoordinator已初始化 | checkpointer=AsyncRedisSaver | enhanced_memory=yes | context_manager=yes
2026-01-08 00:37:29,451 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ 解耦模块已初始化 (IntentClassifier, ToolExecutor, EventParser, ResponseBuilder, ToolDispatcher, ParallelExecutor, PlanGenerator, QuickPathHandler, StreamEventHandler, SecondaryToolHandler, TaskRunner, AgentExecutor)
2026-01-08 00:37:29,625 - app.services.agent.parallel_tool_node - INFO - [ParallelToolNode] 初始化完成，最大并发数=5，并行安全工具=4个
2026-01-08 00:37:29,751 - app.api.v1.agent - INFO - [Global Agent] created global agent instance; MemorySaver shared across requests
2026-01-08 00:37:29,788 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
2026-01-08 00:37:29,793 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:7bc10a35-cce3-4258-80a3-8eeb933d72b3 (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=f141c5ed-0a75-4429-ba2a-912c74d167a3, conversation_id=7bc10a35-cce3-4258-80a3-8eeb933d72b3)
2026-01-08 00:37:29,795 - app.services.context.monitoring_integration - INFO - ✅ ContextManager监控收集器已初始化
2026-01-08 00:37:29,798 - app.services.context.store - INFO - [ContextStore] Redis连接成功
INFO:     127.0.0.1:54422 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 00:37:29,823 - app.services.context.manager - INFO - [ContextManager] 创建新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:7bc10a35-cce3-4258-80a3-8eeb933d72b3
2026-01-08 00:37:30,609 - app.services.context.token_counter - INFO - ✅ tiktoken初始化成功，模型: gemini-2.5-pro -> cl100k_base
2026-01-08 00:37:30,612 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:7bc10a35-cce3-4258-80a3-8eeb933d72b3: 0/16000 tokens
2026-01-08 00:37:34,814 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='请帮我梳理一下目前出现的所有武功和刀法：
  1. 列出所有...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:f141c5ed-0a75-4429-ba2a-912c74d167a3', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=3条
2026-01-08 00:37:34,816 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=f141c5ed-0a75-4429-ba2a-912c74d167a3 | 含用户级=True | 找到=3条
2026-01-08 00:37:34,817 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 1条消息, 0 tokens, 耗时 5020.69ms
2026-01-08 00:37:34,819 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 1 条历史消息 (token: 0)
2026-01-08 00:37:34,827 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-08 00:37:34,829 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-08 00:37:34,830 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=20, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-08 00:37:37,004 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-08 00:37:37,006 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-08 00:37:37,084 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-08 00:37:37,086 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=346, cost=$0.000035, time=2178ms
2026-01-08 00:37:37,086 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=8, 尝试次数=1
2026-01-08 00:37:37,087 - app.services.agent.intent.classifier - INFO - [Intent] AI识别结果: analysis
2026-01-08 00:37:37,089 - app.services.agent.langgraph_agent - INFO - [Planning] AI意图分类: analysis (置信度: 0.90)
2026-01-08 00:37:37,090 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 请帮我梳理一下目前出现的所有武功和刀法：
  1. 列出所有提到的刀法名称和等级
  2. 分析段融...
2026-01-08 00:37:37,099 - app.core.cache - INFO - ⚠️ 缓存未命中: prompt:planning:v2.29.0:get_planning_static_prompt:fca6eb91156619d0
2026-01-08 00:37:37,110 - app.core.cache - INFO - 💾 缓存已保存: prompt:planning:v2.29.0:get_planning_static_prompt:fca6eb91156619d0 (expire=3600s)
2026-01-08 00:37:37,129 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-08 00:37:37,133 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=story_planning, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: story_planning; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-01-08 00:37:37,136 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.3, task_type=TaskType.STORY_PLANNING
2026-01-08 00:37:44,928 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:52064 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 00:37:48,919 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-08 00:37:56,144 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 14 个数据块，总长度: 1672
2026-01-08 00:37:56,144 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 14813 (prompt=13948, completion=865)
2026-01-08 00:37:56,144 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-08 00:37:56,144 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-08 00:37:56,170 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-08 00:37:56,170 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=14813, cost=$0.026085, time=19007ms
2026-01-08 00:37:56,170 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=14813
2026-01-08 00:37:56,170 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户需要一个基于作品内容的分析报告，包含三个具体要点：1. , 原料=为了完成这个分析，我需要以下信息：
1., 处理=我将分步执行以下操作：
1. 使用搜索工
2026-01-08 00:37:56,176 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共4个任务
2026-01-08 00:37:56,176 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共4个任务，耗时: 19.09s
2026-01-08 00:37:56,176 - app.api.v1.agent - INFO - [Stream] Plan tasks: 4 items
2026-01-08 00:37:56,176 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2026-01-08 00:37:56,184 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2026-01-08 00:37:56,185 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2026-01-08 00:37:56,186 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 任务分组: 第一层并行=2, 第二层并行=1, 串行=1
2026-01-08 00:37:56,186 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始第一层并行执行2个任务
2026-01-08 00:37:56,189 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务1开始: 在作品中搜索关键词“刀法”，以找出所有被提及的刀法名称。
2026-01-08 00:37:56,189 - app.api.v1.agent - INFO - [Stream] Task started: 在作品中搜索关键词“刀法”，以找出所有被提及的刀法名称。 (icon=Search)
2026-01-08 00:37:56,189 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(search_analysis_fragments)
2026-01-08 00:37:56,193 - app.services.agent.tools.tool_types - INFO - [search_analysis_fragments] 开始执行工具
2026-01-08 00:37:56,199 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务3开始: 读取当前章节（chapter_id: c0661752-e71b-48ad-8597-0957516a43fe）内容，以获取关于段融和杂役弟子的最新信息。
2026-01-08 00:37:56,199 - app.api.v1.agent - INFO - [Stream] Task started: 读取当前章节（chapter_id: c0661752-e71b-48ad-8597-0957516a43fe）内容，以获取关于段融和杂役弟子的最新信息。 (icon=FileText)
2026-01-08 00:37:56,199 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(read_chapter)
2026-01-08 00:37:56,199 - app.services.agent.tools.tool_types - INFO - [read_chapter] 开始执行工具
2026-01-08 00:37:56,873 - app.services.agent.langgraph_tools - INFO - [read_chapter_tool] ✅ 读取章节成功: 第5章 太一门
2026-01-08 00:37:56,875 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=f141c5ed-0a75-4429-ba2a-912c74d167a3, current_order=5, query=刀法...
2026-01-08 00:37:56,900 - app.services.agent.tools.tool_types - INFO - [read_chapter] 执行成功 (耗时: 0.701s)
2026-01-08 00:37:56,901 - app.services.agent.tools.tool_monitor - INFO - ToolMonitor initialized with Memory storage, retention: 7 days
2026-01-08 00:37:56,901 - app.services.agent.execution.task_runner - INFO - [TaskRunner] read_chapter 执行成功（DeepAgent模式）
2026-01-08 00:37:56,901 - app.api.v1.agent - INFO - [Stream] 任务完成: 读取当前章节（chapter_id: c0661752-e71b-48ad-8597-0957516a43fe）内容，以获取关于段融和杂役弟子的最新信息。 (0.7s)
2026-01-08 00:37:56,901 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务3完成
2026-01-08 00:37:56,918 - app.services.chapter_vector_service - INFO - RAG retrieved 10 segments within order<=7
Building prefix dict from the default dictionary ...
2026-01-08 00:37:56,918 - jieba - DEBUG - Building prefix dict from the default dictionary ...
Loading model from cache D:\Temp\jieba.cache
2026-01-08 00:37:56,920 - jieba - DEBUG - Loading model from cache D:\Temp\jieba.cache
Loading model cost 0.539 seconds.
2026-01-08 00:37:57,456 - jieba - DEBUG - Loading model cost 0.539 seconds.
Prefix dict has been built successfully.
2026-01-08 00:37:57,456 - jieba - DEBUG - Prefix dict has been built successfully.
2026-01-08 00:37:57,467 - app.services.agent.langgraph_tools - INFO - [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
2026-01-08 00:37:57,468 - app.services.agent.tools.tool_types - INFO - [search_analysis_fragments] 执行成功 (耗时: 1.274s)
2026-01-08 00:37:57,470 - app.services.agent.execution.task_runner - INFO - [TaskRunner] search_analysis_fragments 执行成功（DeepAgent模式）
2026-01-08 00:37:57,470 - app.api.v1.agent - INFO - [Stream] 任务完成: 在作品中搜索关键词“刀法”，以找出所有被提及的刀法名称。 (1.3s)
2026-01-08 00:37:57,470 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务1完成
2026-01-08 00:37:57,470 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始第二层并行执行1个任务
2026-01-08 00:37:57,470 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第二层任务4开始: 结合搜索结果、世界观和章节内容，整理出所有刀法和等级，分析段融的武功储备，并对比他与其他杂役弟子的差距。
2026-01-08 00:37:57,470 - app.api.v1.agent - INFO - [Stream] Task started: 结合搜索结果、世界观和章节内容，整理出所有刀法和等级，分析段融的武功储备，并对比他与其他杂役弟子的差距。 (icon=BarChart2)
2026-01-08 00:37:57,470 - app.services.agent.parameter_resolver - WARNING - [ParameterResolver] 任务2尚未执行，无法解析占位符 $TASK_2.worldview$, 保留占位符（非严格模式）
2026-01-08 00:37:57,470 - app.services.agent.execution.task_runner - INFO - [TaskRunner] analyze_text_tool 的 text 参数为空或含占位符，使用 context 兜底（5351字符）
2026-01-08 00:37:57,470 - app.services.agent.execution.task_runner - INFO - [TaskRunner] analyze_text_tool 使用 focus: '根据提供的资料，详细回答用户的三个问题：1. 列出所有提到的刀法名称和等级。2. 分析段融目前的武功储备。3. 对比段融和其他杂役弟子的差距。...'
2026-01-08 00:37:57,470 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(analyze_text)
2026-01-08 00:37:57,470 - app.services.agent.tools.tool_types - INFO - [analyze_text] 开始执行工具
2026-01-08 00:37:57,475 - app.services.agent.tools.analysis_tools - INFO - [analyze_text_tool] 尝试第 1 次调用，config={'temperature': 0.3, 'task_type': <TaskType.SUMMARIZATION: 'summarization'>}
2026-01-08 00:37:57,478 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-08 00:37:57,478 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-08 00:37:57,478 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
2026-01-08 00:37:57,611 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:60664 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 00:38:07,237 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-08 00:38:08,516 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 9 个数据块，总长度: 543
2026-01-08 00:38:08,517 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 6363 (prompt=5973, completion=390)
2026-01-08 00:38:08,519 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-08 00:38:08,519 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-08 00:38:08,548 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-08 00:38:08,551 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=6363, cost=$0.002767, time=11041ms
2026-01-08 00:38:08,553 - app.services.agent.tools.analysis_tools - INFO - [analyze_text_tool] 第 1 次调用成功
2026-01-08 00:38:08,554 - app.services.agent.tools.analysis_tools - INFO - [analyze_text_tool] 分析完成，结果长度: 543
2026-01-08 00:38:08,555 - app.services.agent.tools.tool_types - INFO - [analyze_text] 执行成功 (耗时: 11.085s)
2026-01-08 00:38:08,557 - app.services.agent.execution.task_runner - INFO - [TaskRunner] analyze_text 执行成功（DeepAgent模式）
2026-01-08 00:38:08,558 - app.api.v1.agent - INFO - [Stream] 任务完成: 结合搜索结果、世界观和章节内容，整理出所有刀法和等级，分析段融的武功储备，并对比他与其他杂役弟子的差距。 (11.1s)
2026-01-08 00:38:08,559 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第二层任务4完成
2026-01-08 00:38:08,561 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始串行执行1个任务
2026-01-08 00:38:08,562 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务2开始: 获取作品的世界观设定，以了解武功的等级划分体系。
2026-01-08 00:38:08,562 - app.api.v1.agent - INFO - [Stream] Task started: 获取作品的世界观设定，以了解武功的等级划分体系。 (icon=Wrench)
2026-01-08 00:38:08,563 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: get_worldview_summary
2026-01-08 00:38:08,565 - app.services.agent.execution.tool_executor - WARNING - [StandardTool] 'get_worldview_summary' 不存在，降级到 @tool: 工具 'get_worldview_summary' 不存在
可用的 StandardTool: ['continue_writing', 'expand_text', 'analyze_content', 'analyze_text', 'evaluate_quality', 'smart_rewrite', 'smart_continue', 'smart_insert', 'apply_chapter_edit', 'get_context', 'read_chapter', 'get_chapter_by_order', 'search_analysis_fragments']
可用的 DynamicTool: []
2026-01-08 00:38:08,566 - app.services.agent.execution.tool_executor - INFO - [LegacyTool] 使用 @tool 版本: get_worldview_summary
2026-01-08 00:38:08,596 - app.services.agent.langgraph_tools - INFO - [get_worldview_summary] ✅ 获取世界观摘要成功: {'characters': 0, 'locations': 0, 'settings': 0}
2026-01-08 00:38:08,600 - app.api.v1.agent - INFO - [Stream] 任务完成: 获取作品的世界观设定，以了解武功的等级划分体系。 (0.0s)
2026-01-08 00:38:08,601 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务2完成
2026-01-08 00:38:08,602 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共4个任务，耗时: 12.43s
2026-01-08 00:38:08,602 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2026-01-08 00:38:08,603 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=3, 输出型=1, 展示型=0
2026-01-08 00:38:08,605 - app.services.agent.langgraph_agent - INFO - [Response] 单个分析任务(analyze_text_tool)，使用AI格式化
2026-01-08 00:38:08,606 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2026-01-08 00:38:08,607 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=6048字符, 处理后=5643字符
2026-01-08 00:38:08,609 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2026-01-08 00:38:08,609 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2026-01-08 00:38:08,627 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-08 00:38:08,629 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-08 00:38:08,631 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
2026-01-08 00:38:14,316 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:54839 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 00:38:20,967 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-08 00:38:26,547 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 15 个数据块，总长度: 1416
2026-01-08 00:38:26,549 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 7069 (prompt=6089, completion=980)
2026-01-08 00:38:26,551 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-08 00:38:26,556 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-08 00:38:26,602 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-08 00:38:26,606 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=7069, cost=$0.004277, time=17926ms
2026-01-08 00:38:26,608 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=1416
2026-01-08 00:38:26,767 - app.services.context.vector_memory_store - INFO - 🔁 跳过重复记忆，复用ID=602f5147-846a-4cde-95d3-405fa75f133f_1767777797504_5b5dbe55
2026-01-08 00:38:26,772 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 隔离=work:f141c5ed-0a75-4429-ba2a-912c74d167a3 | 重要度=0.99
2026-01-08 00:38:29,883 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:f141c5ed-0a75-4429-ba2a-912c74d167a3 | 重要度=0.77
2026-01-08 00:38:29,904 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:7bc10a35-cce3-4258-80a3-8eeb933d72b3, token=1673
2026-01-08 00:38:29,908 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:7bc10a35-cce3-4258-80a3-8eeb933d72b3, 消息数=2, Token=1673
2026-01-08 00:38:29,908 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:7bc10a35-cce3-4258-80a3-8eeb933d72b3)
2026-01-08 00:38:29,910 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2026-01-08 00:38:29,925 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed