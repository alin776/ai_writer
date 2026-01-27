INFO:     127.0.0.1:55532 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2026-01-27 22:37:01,621 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 输出至少25条原文证据，覆盖以下主题：

  1. 世界错位/坐标/《一人之下》→《遮天》/九龙拉棺...
2026-01-27 22:37:01,624 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-27 22:37:01,624 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-27 22:37:01,624 - app.services.ai.http_ai_service - INFO - [成本追踪] 初始化未传db/user_id，将使用请求上下文按需记录成本
2026-01-27 22:37:03,119 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz:8443/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-27 22:37:03,119 - app.services.agent.tools.writing_tools - INFO - Writing tools AI service initialized
2026-01-27 22:37:03,120 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ AI Service 已同时设置到 langgraph_tools 和 writing_tools
2026-01-27 22:37:03,120 - app.services.context.adaptive_budget - INFO - ✅ 所有预算配置验证通过
2026-01-27 22:37:10,719 - app.services.context.vector_memory_store - INFO - ✅ VectorMemoryStore初始化成功 | 目录=./data/chroma_db | 模型=paraphrase-multilingual-MiniLM-L12-v2 | 集合=user_memories
2026-01-27 22:37:10,719 - app.services.context.manager - INFO - ✅ VectorMemoryStore 已初始化
2026-01-27 22:37:10,719 - app.services.context.manager - INFO - ✅ ContextManager: 长期记忆已启用 (user_id=None)
2026-01-27 22:37:10,719 - app.services.context.manager - INFO - ✅ ContextManager: 自适应预算已启用
2026-01-27 22:37:10,719 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ ContextManager已初始化（长期记忆已启用，自适应预算已启用，总预算=16000 tokens）
成功加载模板: analyze_text (版本 3.1.0)
成功加载模板: writing_agent (版本 2.0.0)
成功加载模板: system_agent_prompt (版本 2.1.0)
成功加载模板: creative_writing_prompt (版本 1.0.0)
2026-01-27 22:37:10,769 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ PromptManager已初始化
2026-01-27 22:37:10,777 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ Redis连接验证成功
2026-01-27 22:37:10,777 - app.services.agent.langgraph_agent - INFO - [LangGraph] OK 使用 AsyncRedisSaver（redis://localhost:6379/0，TTL=7天）
2026-01-27 22:37:10,785 - app.services.agent.memory.metrics - INFO - [MemoryMetrics] 监控系统已初始化
2026-01-27 22:37:10,785 - app.services.agent.memory.long_term_store - INFO - [LongTermStore] Initialized: base_dir=./data/long_term_memory, max_size=50KB, compression=True
2026-01-27 22:37:10,785 - app.services.agent.memory.enhanced_memory_manager - INFO - EnhancedMemoryManager initialized: short=10, medium=100, threshold=0.1, long_term_backup=enabled
2026-01-27 22:37:10,785 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ EnhancedMemoryManager已创建
2026-01-27 22:37:10,787 - app.services.agent.memory.unified_coordinator - INFO - [UnifiedMemoryCoordinator] 初始化统一记忆协调器
2026-01-27 22:37:10,787 - app.services.agent.memory.unified_coordinator - INFO - [UnifiedMemoryCoordinator] 全局实例已设置
2026-01-27 22:37:10,787 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ UnifiedMemoryCoordinator已初始化 | checkpointer=AsyncRedisSaver | enhanced_memory=yes | context_manager=yes
2026-01-27 22:37:10,787 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ 解耦模块已初始化 (IntentClassifier, ToolExecutor, EventParser, ResponseBuilder, ToolDispatcher, ParallelExecutor, PlanGenerator, QuickPathHandler, StreamEventHandler, SecondaryToolHandler, TaskRunner, AgentExecutor)
2026-01-27 22:37:10,811 - app.services.agent.parallel_tool_node - INFO - [ParallelToolNode] 初始化完成，最大并发数=5，并行安全工具=6个
2026-01-27 22:37:10,877 - app.api.v1.agent - INFO - [Global Agent] created global agent instance; MemorySaver shared across requests
2026-01-27 22:37:10,893 - app.api.v1.agent - INFO - [agent_chat_stream] 📚 世界观数据已注入: 人物=8, 地点=7, 设定=7, 规范=无
2026-01-27 22:37:10,893 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21:fbfb1a7c-8003-4fcb-b54d-61a936b1ee6b (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, conversation_id=fbfb1a7c-8003-4fcb-b54d-61a936b1ee6b)
2026-01-27 22:37:10,902 - app.services.context.monitoring_integration - INFO - ✅ ContextManager监控收集器已初始化
2026-01-27 22:37:10,902 - app.services.context.store - INFO - [ContextStore] Redis连接成功
2026-01-27 22:37:10,909 - app.services.context.manager - INFO - [ContextManager] 创建新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21:fbfb1a7c-8003-4fcb-b54d-61a936b1ee6b
2026-01-27 22:37:11,172 - app.services.context.token_counter - INFO - ✅ tiktoken初始化成功，模型: gemini-2.5-pro -> cl100k_base
2026-01-27 22:37:11,172 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21:fbfb1a7c-8003-4fcb-b54d-61a936b1ee6b: 0/16000 tokens
2026-01-27 22:37:12,552 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='输出至少25条原文证据，覆盖以下主题：

  1. 世界错位...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=3条
2026-01-27 22:37:12,560 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21 | 含用户级=True | 找到=3条
2026-01-27 22:37:12,610 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 1条消息, 0 tokens, 耗时 1708.41ms
2026-01-27 22:37:12,610 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 1 条历史消息 (token: 0, has_summary: False)
2026-01-27 22:37:12,610 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:37:12,610 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:37:12,610 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=200, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-27 22:37:14,210 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:37:14,210 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:37:14,245 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:37:14,245 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=597, cost=$0.000065, time=1600ms
2026-01-27 22:37:14,245 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=39, 尝试次数=1
2026-01-27 22:37:14,253 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:37:14,254 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:37:14,255 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=20, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-27 22:37:16,741 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:37:16,741 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:37:16,766 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:37:16,766 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=524, cost=$0.000053, time=2486ms
2026-01-27 22:37:16,766 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=7, 尝试次数=1
2026-01-27 22:37:16,768 - app.services.agent.intent.classifier - INFO - [Intent] AI识别结果: writing
2026-01-27 22:37:16,768 - app.services.agent.langgraph_agent - INFO - [Planning] AI意图分类: writing (置信度: 0.90)
2026-01-27 22:37:16,768 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 输出至少25条原文证据，覆盖以下主题：

  1. 世界错位/坐标/《一人之下》→《遮天》/九龙拉棺...
2026-01-27 22:37:16,768 - app.core.cache - INFO - ⚠️ 缓存未命中: prompt:planning:v2.41.0:get_planning_static_prompt:fca6eb91156619d0
2026-01-27 22:37:16,789 - app.core.cache - INFO - 💾 缓存已保存: prompt:planning:v2.41.0:get_planning_static_prompt:fca6eb91156619d0 (expire=3600s)
2026-01-27 22:37:16,795 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-27 22:37:16,795 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=story_planning, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: story_planning; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-01-27 22:37:16,796 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.3, task_type=TaskType.STORY_PLANNING
2026-01-27 22:37:41,260 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-27 22:37:47,502 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 13 个数据块，总长度: 1564
2026-01-27 22:37:47,502 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 22941 (prompt=22206, completion=735)
2026-01-27 22:37:47,502 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:37:47,505 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-27 22:37:47,533 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:37:47,533 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=22941, cost=$0.035107, time=30709ms
2026-01-27 22:37:47,534 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=22941
2026-01-27 22:37:47,534 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户需要一个包含至少25条原文证据的列表，这些证据需要根据7, 原料=为了完成这个任务，我需要访问并搜索作品的, 处理=我将使用 `explore_conten
2026-01-27 22:37:47,552 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共1个任务
2026-01-27 22:37:47,552 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共1个任务，耗时: 30.78s
2026-01-27 22:37:47,552 - app.api.v1.agent - INFO - [Stream] Plan tasks: 1 items
2026-01-27 22:37:47,552 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2026-01-27 22:37:47,552 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2026-01-27 22:37:47,552 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2026-01-27 22:37:47,552 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] DAG 调度启用，任务数=1, 有依赖任务=0
2026-01-27 22:37:47,552 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1开始: 根据用户提供的7个主题（世界错位、系统、主角价值观、修炼体系、青帝、段德、人皇幡等），在全文中搜索并提取所有相关的原文段落作为证据。
2026-01-27 22:37:47,552 - app.api.v1.agent - INFO - [Stream] Task started: 根据用户提供的7个主题（世界错位、系统、主角价值观、修炼体系、青帝、段德、人皇幡等），在全文中搜索并提取所有相关的原文段落作为证据。 (icon=Wrench)
2026-01-27 22:37:47,559 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: explore_content
2026-01-27 22:37:47,560 - app.services.agent.tools.explore_tools - INFO - [explore_content] 开始: work_id=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, target=输出至少25条原文证据，覆盖世界错位/九龙拉棺，系统10086，林仙摆烂，遮天修炼体系，青帝坟，段德...
2026-01-27 22:37:47,560 - app.services.agent.tools.explore_tools - INFO - [explore_content] 规划传入关键词: ['世界错位', '坐标', '一人之下', '遮天', '九龙拉棺', '泰山', '系统', '10086', '任务', '奖励']
2026-01-27 22:37:47,565 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 启用严格段落号模式
2026-01-27 22:37:47,565 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 任务禁止整章阅读
2026-01-27 22:37:47,565 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 开始探索 V5: work_id=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, target=输出至少25条原文证据，覆盖世界错位/九龙拉棺，系统10086，林仙摆烂，遮天修炼体系，青帝坟，段德...
2026-01-27 22:37:47,565 - app.services.chapter_service - INFO - [ChapterService] Querying chapters for work_id=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, type=<class 'uuid.UUID'>
2026-01-27 22:37:47,577 - app.services.chapter_service - INFO - [ChapterService] Found 77 chapters
2026-01-27 22:37:47,577 - app.services.chapter_service - INFO -   - Chapter: 第1章 【摆烂的宿主】, order=1
2026-01-27 22:37:47,579 - app.services.chapter_service - INFO -   - ... (75 more chapters)
2026-01-27 22:37:47,579 - app.services.chapter_service - INFO -   - Chapter: 第100章 【火域铸真器，两脉起冲突】, order=77
2026-01-27 22:37:47,652 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-27 22:37:47,654 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-27 22:37:47,654 - app.services.ai.http_ai_service - INFO - [成本追踪] 初始化未传db/user_id，将使用请求上下文按需记录成本
2026-01-27 22:37:49,077 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz:8443/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-27 22:37:49,077 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:37:49,077 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:37:49,077 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:37:50,887 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:37:50,894 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:37:50,921 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:37:50,924 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=522, cost=$0.000083, time=1816ms
2026-01-27 22:37:50,927 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=229, 尝试次数=1
2026-01-27 22:37:50,956 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['九龙拉棺']..., mode=any, range=None, hits=10
2026-01-27 22:37:50,956 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:37:50,960 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:37:50,960 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:37:55,240 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:37:55,240 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:37:55,245 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:37:55,245 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=956, cost=$0.000154, time=4279ms
2026-01-27 22:37:55,245 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=440, 尝试次数=1
2026-01-27 22:37:55,268 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第66段
2026-01-27 22:37:55,277 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第18段
2026-01-27 22:37:55,286 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第83段
2026-01-27 22:37:55,302 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第22段
2026-01-27 22:37:55,310 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第61段
2026-01-27 22:37:55,310 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:37:55,310 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:37:55,310 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:37:57,386 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:37:57,386 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:37:57,402 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:37:57,402 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1284, cost=$0.000174, time=2075ms
2026-01-27 22:37:57,402 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=293, 尝试次数=1
2026-01-27 22:37:57,535 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['遮天修炼体系', '青帝坟', '段德']..., mode=any, range=None, hits=25
2026-01-27 22:37:57,542 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:37:57,542 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:37:57,544 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:37:59,129 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:37:59,129 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:37:59,145 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:37:59,145 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1028, cost=$0.000161, time=1585ms
2026-01-27 22:37:59,145 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=455, 尝试次数=1
2026-01-27 22:37:59,162 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第9章第37段
2026-01-27 22:37:59,169 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第98段
2026-01-27 22:37:59,185 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第36章第55段
2026-01-27 22:37:59,194 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第36章第56段
2026-01-27 22:37:59,199 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:37:59,202 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:37:59,202 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:38:03,146 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:38:03,146 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:38:03,160 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:38:03,160 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1919, cost=$0.000420, time=3944ms
2026-01-27 22:38:03,160 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=2072, 尝试次数=1
2026-01-27 22:38:03,177 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第1段
2026-01-27 22:38:03,193 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第2段
2026-01-27 22:38:03,207 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第3段
2026-01-27 22:38:03,215 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第4段
2026-01-27 22:38:03,219 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第5段
2026-01-27 22:38:03,235 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第6段
2026-01-27 22:38:03,251 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第7段
2026-01-27 22:38:03,262 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第8段
2026-01-27 22:38:03,272 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第9段
2026-01-27 22:38:03,288 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第10段
2026-01-27 22:38:03,294 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第11段
2026-01-27 22:38:03,307 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第12段
2026-01-27 22:38:03,319 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第13段
2026-01-27 22:38:03,327 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第14段
2026-01-27 22:38:03,335 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第15段
2026-01-27 22:38:03,345 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第16段
2026-01-27 22:38:03,361 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第17段
2026-01-27 22:38:03,368 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第18段
2026-01-27 22:38:03,378 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第19段
2026-01-27 22:38:03,393 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第20段
2026-01-27 22:38:03,408 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第21段
2026-01-27 22:38:03,420 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第22段
2026-01-27 22:38:03,430 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第23段
2026-01-27 22:38:03,443 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第24段
2026-01-27 22:38:03,455 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第25段
2026-01-27 22:38:03,462 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:38:03,462 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:38:03,462 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:38:06,358 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:38:06,358 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:38:06,362 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:38:06,362 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1710, cost=$0.000345, time=2897ms
2026-01-27 22:38:06,362 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=1475, 尝试次数=1
2026-01-27 22:38:06,372 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第1段
2026-01-27 22:38:06,383 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第2段
2026-01-27 22:38:06,387 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第3段
2026-01-27 22:38:06,402 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第1段
2026-01-27 22:38:06,410 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第2段
2026-01-27 22:38:06,419 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第3段
2026-01-27 22:38:06,427 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第1段
2026-01-27 22:38:06,437 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第2段
2026-01-27 22:38:06,452 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第3段
2026-01-27 22:38:06,461 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第4章第1段
2026-01-27 22:38:06,468 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第4章第2段
2026-01-27 22:38:06,477 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第4章第3段
2026-01-27 22:38:06,493 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第5章第1段
2026-01-27 22:38:06,502 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第5章第2段
2026-01-27 22:38:06,510 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第5章第3段
2026-01-27 22:38:06,519 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第6章第1段
2026-01-27 22:38:06,529 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第6章第2段
2026-01-27 22:38:06,539 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第6章第3段
2026-01-27 22:38:06,543 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:38:06,544 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:38:06,544 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:38:08,268 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:38:08,269 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:38:08,285 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:38:08,285 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1321, cost=$0.000189, time=1724ms
2026-01-27 22:38:08,285 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=366, 尝试次数=1
2026-01-27 22:38:08,392 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['段德考古', '系统10086', '林仙摆烂']..., mode=any, range=None, hits=100
2026-01-27 22:38:08,399 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:38:08,399 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:38:08,399 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:38:10,451 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:38:10,453 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:38:10,470 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:38:10,475 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=938, cost=$0.000152, time=2054ms
2026-01-27 22:38:10,475 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=456, 尝试次数=1
2026-01-27 22:38:10,500 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第23段
2026-01-27 22:38:10,520 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第61段
2026-01-27 22:38:10,531 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第64段
2026-01-27 22:38:10,542 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第105段
2026-01-27 22:38:10,562 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第106段
2026-01-27 22:38:10,562 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:38:10,570 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:38:10,570 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:38:11,882 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:38:11,882 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:38:11,893 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:38:11,895 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1345, cost=$0.000197, time=1311ms
2026-01-27 22:38:11,895 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=454, 尝试次数=1
2026-01-27 22:38:11,910 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第23段
2026-01-27 22:38:11,923 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第61段
2026-01-27 22:38:11,941 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第24段
2026-01-27 22:38:11,944 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 探索完成(工具循环): 9轮, 原因=达到读取上限
2026-01-27 22:38:11,954 - app.services.agent.execution.tool_executor - INFO - [StandardTool] explore_content 执行成功
2026-01-27 22:38:11,960 - app.api.v1.agent - INFO - [Stream] 任务完成: 根据用户提供的7个主题（世界错位、系统、主角价值观、修炼体系、青帝、段德、人皇幡等），在全文中搜索并提取所有相关的原文段落作为证据。 (24.4s)
2026-01-27 22:38:11,960 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1完成
2026-01-27 22:38:11,961 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共1个任务，耗时: 24.41s
2026-01-27 22:38:11,965 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2026-01-27 22:38:11,965 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=1, 展示型=0
2026-01-27 22:38:11,968 - app.services.agent.langgraph_agent - INFO - [Response] 单个输出任务(explore_content)，使用AI整合
2026-01-27 22:38:11,968 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2026-01-27 22:38:11,968 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=1, 展示型=0
2026-01-27 22:38:11,968 - app.services.agent.utils.context_builder - INFO - [Compress] 任务1工具'explore_content'，内容长度47282，保留20000字符（省略27282字符）
2026-01-27 22:38:11,968 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=47613字符, 处理后=340字符
2026-01-27 22:38:11,968 - app.services.agent.planning.response_builder - INFO - [Summarization] 准备发送 summarization_start 事件
2026-01-27 22:38:11,968 - app.services.agent.stream.stream_event_handler - INFO - [StreamEventHandler] emit_summarization_start 被调用, _on_flow_event=True
2026-01-27 22:38:11,968 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_start 事件已发送
2026-01-27 22:38:11,968 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2026-01-27 22:38:11,968 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2026-01-27 22:38:11,982 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-27 22:38:11,982 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-27 22:38:11,982 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
2026-01-27 22:38:55,697 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-27 22:38:55,699 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_complete 事件已发送（第一个chunk时）
2026-01-27 22:38:55,699 - app.services.agent.planning.response_builder - INFO - [Summarization] output_ready 事件已发送（第一个chunk时）
2026-01-27 22:39:01,371 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 22 个数据块，总长度: 1724
2026-01-27 22:39:01,371 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 22547 (prompt=21212, completion=1335)
2026-01-27 22:39:01,372 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:39:01,373 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-27 22:39:01,398 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:39:01,399 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=22547, cost=$0.009701, time=49391ms
2026-01-27 22:39:01,400 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=1724
2026-01-27 22:39:02,586 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21 | 重要度=0.84
2026-01-27 22:39:03,471 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21 | 重要度=0.60
2026-01-27 22:39:03,491 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21:fbfb1a7c-8003-4fcb-b54d-61a936b1ee6b, token=2312
2026-01-27 22:39:03,493 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21:fbfb1a7c-8003-4fcb-b54d-61a936b1ee6b, 消息数=2, 摘要长度=0, Token=2312
2026-01-27 22:39:03,494 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21:fbfb1a7c-8003-4fcb-b54d-61a936b1ee6b)
2026-01-27 22:39:03,494 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2026-01-27 22:39:03,504 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed
2026-01-27 22:39:17,503 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/fbfb1a7c-8003-4fcb-b54d-61a936b1ee6b
INFO:     127.0.0.1:58005 - "GET /api/v1/agent/operations/fbfb1a7c-8003-4fcb-b54d-61a936b1ee6b HTTP/1.1" 200 OK
2026-01-27 22:41:09,606 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, chapter_id: fca581f0-3bce-457a-830f-00efaf22ab8c
2026-01-27 22:41:09,615 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: fca581f0-3bce-457a-830f-00efaf22ab8c
2026-01-27 22:41:09,618 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: 5452e126-99a7-4323-8e8c-c3ea9b6f8774
2026-01-27 22:41:09,619 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-27 22:41:09,624 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:58788 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-27 22:41:09,635 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, chapter_id: fca581f0-3bce-457a-830f-00efaf22ab8c
2026-01-27 22:41:09,649 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: fca581f0-3bce-457a-830f-00efaf22ab8c
2026-01-27 22:41:09,652 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/fca581f0-3bce-457a-830f-00efaf22ab8c/revisions
2026-01-27 22:41:09,653 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: 5452e126-99a7-4323-8e8c-c3ea9b6f8774
2026-01-27 22:41:09,653 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
INFO:     127.0.0.1:51996 - "GET /api/v1/chapters/fca581f0-3bce-457a-830f-00efaf22ab8c/revisions?status=pending HTTP/1.1" 200 OK
2026-01-27 22:41:09,659 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:62197 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-27 22:41:09,725 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:51994 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2026-01-27 22:41:09,760 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/fca581f0-3bce-457a-830f-00efaf22ab8c/revisions
INFO:     127.0.0.1:65414 - "GET /api/v1/chapters/fca581f0-3bce-457a-830f-00efaf22ab8c/revisions?status=pending HTTP/1.1" 200 OK
2026-01-27 22:41:09,899 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21
2026-01-27 22:41:09,901 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/fca581f0-3bce-457a-830f-00efaf22ab8c
INFO:     127.0.0.1:61961 - "PUT /api/v1/chapters/fca581f0-3bce-457a-830f-00efaf22ab8c HTTP/1.1" 200 OK
2026-01-27 22:41:09,902 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第25章 【汝从无生来，要往长生去】 (order=20)
2026-01-27 22:41:12,093 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第25章 【汝从无生来，要往长生去】 (61 paragraphs)
2026-01-27 22:41:12,102 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 fca581f0-3bce-457a-830f-00efaf22ab8c 内容更新，新段落数: 61
2026-01-27 22:41:12,126 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21
2026-01-27 22:41:12,128 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/fca581f0-3bce-457a-830f-00efaf22ab8c
INFO:     127.0.0.1:60151 - "PUT /api/v1/chapters/fca581f0-3bce-457a-830f-00efaf22ab8c HTTP/1.1" 200 OK
2026-01-27 22:41:12,129 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第25章 【汝从无生来，要往长生去】 (order=20)
2026-01-27 22:41:14,573 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第25章 【汝从无生来，要往长生去】 (61 paragraphs)
2026-01-27 22:41:14,634 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 fca581f0-3bce-457a-830f-00efaf22ab8c 内容更新，新段落数: 61
2026-01-27 22:41:14,647 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21
2026-01-27 22:41:14,652 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/fca581f0-3bce-457a-830f-00efaf22ab8c
INFO:     127.0.0.1:59749 - "PUT /api/v1/chapters/fca581f0-3bce-457a-830f-00efaf22ab8c HTTP/1.1" 200 OK
2026-01-27 22:41:14,656 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第25章 【汝从无生来，要往长生去】 (order=20)
2026-01-27 22:41:16,718 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第25章 【汝从无生来，要往长生去】 (61 paragraphs)
2026-01-27 22:41:16,793 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:59178 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2026-01-27 22:41:16,816 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21
2026-01-27 22:41:16,817 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/fca581f0-3bce-457a-830f-00efaf22ab8c
INFO:     127.0.0.1:64936 - "PUT /api/v1/chapters/fca581f0-3bce-457a-830f-00efaf22ab8c HTTP/1.1" 200 OK
2026-01-27 22:41:16,819 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第25章 【汝从无生来，要往长生去】 (order=20)
2026-01-27 22:41:16,828 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-27 22:41:16,829 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-27 22:41:16,829 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2026-01-27 22:41:18,720 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz:8443/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-27 22:41:18,727 - app.api.v1.agent - INFO - [Chat Stream] Mode: planning
2026-01-27 22:41:21,250 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:60080 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2026-01-27 22:41:21,258 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 输出至少16条原文证据，覆盖以下主题：

  1. 林仙“摆烂/躺平/咸鱼/浑水摸鱼”态度的直接描述...
2026-01-27 22:41:21,272 - app.api.v1.agent - INFO - [agent_chat_stream] 📚 世界观数据已注入: 人物=8, 地点=7, 设定=7, 规范=无
2026-01-27 22:41:21,272 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21:82287b9a-2e06-4364-a8f9-303b2bb87d01 (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, conversation_id=82287b9a-2e06-4364-a8f9-303b2bb87d01)
2026-01-27 22:41:21,274 - app.services.context.manager - INFO - [ContextManager] 创建新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21:82287b9a-2e06-4364-a8f9-303b2bb87d01
2026-01-27 22:41:21,275 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21:82287b9a-2e06-4364-a8f9-303b2bb87d01: 0/16000 tokens
2026-01-27 22:41:21,472 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='输出至少16条原文证据，覆盖以下主题：

  1. 林仙“摆...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=3条
2026-01-27 22:41:21,473 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21 | 含用户级=True | 找到=3条
2026-01-27 22:41:21,478 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 1条消息, 0 tokens, 耗时 206.50ms
2026-01-27 22:41:21,478 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 1 条历史消息 (token: 0, has_summary: False)
2026-01-27 22:41:21,478 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:41:21,478 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:41:21,478 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=200, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-27 22:41:21,486 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第25章 【汝从无生来，要往长生去】 (61 paragraphs)
2026-01-27 22:41:23,526 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:41:23,526 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:41:23,544 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:41:23,544 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=597, cost=$0.000065, time=2048ms
2026-01-27 22:41:23,544 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=39, 尝试次数=1
2026-01-27 22:41:23,547 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:41:23,547 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:41:23,547 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=20, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-27 22:41:25,108 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:41:25,109 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:41:25,128 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:41:25,128 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=524, cost=$0.000053, time=1562ms
2026-01-27 22:41:25,128 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=7, 尝试次数=1
2026-01-27 22:41:25,128 - app.services.agent.intent.classifier - INFO - [Intent] AI识别结果: writing
2026-01-27 22:41:25,128 - app.services.agent.langgraph_agent - INFO - [Planning] AI意图分类: writing (置信度: 0.90)
2026-01-27 22:41:25,128 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 输出至少16条原文证据，覆盖以下主题：

  1. 林仙“摆烂/躺平/咸鱼/浑水摸鱼”态度的直接描述...
2026-01-27 22:41:25,138 - app.core.cache - INFO - ✅ 缓存命中: prompt:planning:v2.41.0:get_planning_static_prompt:fca6eb91156619d0
2026-01-27 22:41:25,144 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-27 22:41:25,144 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=story_planning, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: story_planning; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-01-27 22:41:25,144 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.3, task_type=TaskType.STORY_PLANNING
2026-01-27 22:42:13,992 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-27 22:42:28,293 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 25 个数据块，总长度: 2091
2026-01-27 22:42:28,293 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 26150 (prompt=24618, completion=1532)
2026-01-27 22:42:28,293 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:42:28,293 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-27 22:42:28,307 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:42:28,307 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=26150, cost=$0.046093, time=63148ms
2026-01-27 22:42:28,308 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=26150
2026-01-27 22:42:28,309 - app.services.agent.planning.plan_generator - INFO - [Planning] AI 决定直接回答，跳过任务执行
2026-01-27 22:42:28,309 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户需要一个包含至少16条原文证据的列表，这些证据需要覆盖6, 原料=需要从作品的章节内容中检索与用户指定的六, 处理=这是一个典型的证据检索和引用的任务。我将
2026-01-27 22:42:28,310 - app.services.agent.planning.plan_generator - INFO - [Planning] 直接回答模式，答案长度: 1501
2026-01-27 22:42:28,310 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共0个任务
2026-01-27 22:42:28,310 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共0个任务，耗时: 63.18s
2026-01-27 22:42:28,310 - app.api.v1.agent - INFO - [Stream] Plan tasks: 0 items
2026-01-27 22:42:28,310 - app.services.agent.langgraph_agent - INFO - [Planning] 检测到 direct_answer(1501字)，直接返回答案，跳过任务执行
2026-01-27 22:42:28,595 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21 | 重要度=0.87
2026-01-27 22:42:28,899 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21 | 重要度=0.60
2026-01-27 22:42:28,912 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21:82287b9a-2e06-4364-a8f9-303b2bb87d01, token=2115
2026-01-27 22:42:28,913 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21:82287b9a-2e06-4364-a8f9-303b2bb87d01, 消息数=2, 摘要长度=0, Token=2115
2026-01-27 22:42:28,914 - app.services.agent.langgraph_agent - INFO - [Planning] direct_answer 对话已保存到 ContextManager
2026-01-27 22:42:28,914 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2026-01-27 22:42:28,919 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed
2026-01-27 22:42:53,962 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/82287b9a-2e06-4364-a8f9-303b2bb87d01
INFO:     127.0.0.1:50549 - "GET /api/v1/agent/operations/82287b9a-2e06-4364-a8f9-303b2bb87d01 HTTP/1.1" 200 OK
2026-01-27 22:43:56,815 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, chapter_id: c682287e-0ebf-47c2-8d4b-489ec163ff73
2026-01-27 22:43:56,822 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: c682287e-0ebf-47c2-8d4b-489ec163ff73
2026-01-27 22:43:56,824 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: f44a723d-f23b-407c-9279-ef0be02b202d
2026-01-27 22:43:56,825 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-27 22:43:56,826 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:64961 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-27 22:43:56,853 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, chapter_id: c682287e-0ebf-47c2-8d4b-489ec163ff73
2026-01-27 22:43:56,859 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: c682287e-0ebf-47c2-8d4b-489ec163ff73
2026-01-27 22:43:56,860 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: f44a723d-f23b-407c-9279-ef0be02b202d
2026-01-27 22:43:56,860 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-27 22:43:56,915 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:61574 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-27 22:43:56,917 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:61575 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2026-01-27 22:43:56,925 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/c682287e-0ebf-47c2-8d4b-489ec163ff73/revisions
INFO:     127.0.0.1:61577 - "GET /api/v1/chapters/c682287e-0ebf-47c2-8d4b-489ec163ff73/revisions?status=pending HTTP/1.1" 200 OK
2026-01-27 22:43:56,956 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/c682287e-0ebf-47c2-8d4b-489ec163ff73/revisions
INFO:     127.0.0.1:61384 - "GET /api/v1/chapters/c682287e-0ebf-47c2-8d4b-489ec163ff73/revisions?status=pending HTTP/1.1" 200 OK
2026-01-27 22:43:57,078 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21
2026-01-27 22:43:57,079 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/c682287e-0ebf-47c2-8d4b-489ec163ff73
INFO:     127.0.0.1:64890 - "PUT /api/v1/chapters/c682287e-0ebf-47c2-8d4b-489ec163ff73 HTTP/1.1" 200 OK
2026-01-27 22:43:57,080 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第36章 【齐天大圣，九窍通天】 (order=30)
2026-01-27 22:43:59,210 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第36章 【齐天大圣，九窍通天】 (81 paragraphs)
2026-01-27 22:43:59,259 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 c682287e-0ebf-47c2-8d4b-489ec163ff73 内容更新，新段落数: 81
2026-01-27 22:43:59,281 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21
2026-01-27 22:43:59,284 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/c682287e-0ebf-47c2-8d4b-489ec163ff73
INFO:     127.0.0.1:56892 - "PUT /api/v1/chapters/c682287e-0ebf-47c2-8d4b-489ec163ff73 HTTP/1.1" 200 OK
2026-01-27 22:43:59,285 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第36章 【齐天大圣，九窍通天】 (order=30)
2026-01-27 22:44:01,825 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第36章 【齐天大圣，九窍通天】 (81 paragraphs)
2026-01-27 22:44:01,884 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 c682287e-0ebf-47c2-8d4b-489ec163ff73 内容更新，新段落数: 81
2026-01-27 22:44:01,905 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21
2026-01-27 22:44:01,909 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/c682287e-0ebf-47c2-8d4b-489ec163ff73
INFO:     127.0.0.1:65316 - "PUT /api/v1/chapters/c682287e-0ebf-47c2-8d4b-489ec163ff73 HTTP/1.1" 200 OK
2026-01-27 22:44:01,911 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第36章 【齐天大圣，九窍通天】 (order=30)
2026-01-27 22:44:04,169 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第36章 【齐天大圣，九窍通天】 (81 paragraphs)
2026-01-27 22:44:04,232 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21
2026-01-27 22:44:04,236 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/c682287e-0ebf-47c2-8d4b-489ec163ff73
INFO:     127.0.0.1:51059 - "PUT /api/v1/chapters/c682287e-0ebf-47c2-8d4b-489ec163ff73 HTTP/1.1" 200 OK
2026-01-27 22:44:04,238 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第36章 【齐天大圣，九窍通天】 (order=30)
2026-01-27 22:44:06,661 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第36章 【齐天大圣，九窍通天】 (81 paragraphs)
2026-01-27 22:44:08,128 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, chapter_id: 8e5ced71-2612-46cd-8234-93f404cf5910
2026-01-27 22:44:08,135 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 8e5ced71-2612-46cd-8234-93f404cf5910
2026-01-27 22:44:08,138 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: b0d975d4-7759-4ea0-8486-666c15fbfd07
2026-01-27 22:44:08,138 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-27 22:44:08,138 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:57311 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-27 22:44:08,165 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, chapter_id: 8e5ced71-2612-46cd-8234-93f404cf5910
2026-01-27 22:44:08,173 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 8e5ced71-2612-46cd-8234-93f404cf5910
2026-01-27 22:44:08,176 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: b0d975d4-7759-4ea0-8486-666c15fbfd07
2026-01-27 22:44:08,176 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-27 22:44:08,176 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
2026-01-27 22:44:08,176 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/8e5ced71-2612-46cd-8234-93f404cf5910/revisions
INFO:     127.0.0.1:58250 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
INFO:     127.0.0.1:58253 - "GET /api/v1/chapters/8e5ced71-2612-46cd-8234-93f404cf5910/revisions?status=pending HTTP/1.1" 200 OK
2026-01-27 22:44:08,247 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:58251 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2026-01-27 22:44:08,262 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/8e5ced71-2612-46cd-8234-93f404cf5910/revisions
INFO:     127.0.0.1:62185 - "GET /api/v1/chapters/8e5ced71-2612-46cd-8234-93f404cf5910/revisions?status=pending HTTP/1.1" 200 OK
2026-01-27 22:44:08,389 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21
2026-01-27 22:44:08,393 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/8e5ced71-2612-46cd-8234-93f404cf5910
INFO:     127.0.0.1:64796 - "PUT /api/v1/chapters/8e5ced71-2612-46cd-8234-93f404cf5910 HTTP/1.1" 200 OK
2026-01-27 22:44:08,395 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第59章 上架感言：萌新求订阅 (order=50)
2026-01-27 22:44:13,182 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第59章 上架感言：萌新求订阅 (144 paragraphs)
2026-01-27 22:44:13,222 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 8e5ced71-2612-46cd-8234-93f404cf5910 内容更新，新段落数: 144
2026-01-27 22:44:13,233 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21
2026-01-27 22:44:13,235 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/8e5ced71-2612-46cd-8234-93f404cf5910
INFO:     127.0.0.1:55263 - "PUT /api/v1/chapters/8e5ced71-2612-46cd-8234-93f404cf5910 HTTP/1.1" 200 OK
2026-01-27 22:44:13,236 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第59章 上架感言：萌新求订阅 (order=50)
2026-01-27 22:44:17,099 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第59章 上架感言：萌新求订阅 (144 paragraphs)
2026-01-27 22:44:17,176 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:50123 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2026-01-27 22:44:17,221 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 8e5ced71-2612-46cd-8234-93f404cf5910 内容更新，新段落数: 144
2026-01-27 22:44:17,232 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 8e5ced71-2612-46cd-8234-93f404cf5910 内容更新，新段落数: 144
2026-01-27 22:44:17,236 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21
2026-01-27 22:44:17,239 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-27 22:44:17,240 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-27 22:44:17,240 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2026-01-27 22:44:18,678 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz:8443/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-27 22:44:18,678 - app.api.v1.agent - INFO - [Chat Stream] Mode: planning
2026-01-27 22:44:18,678 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/8e5ced71-2612-46cd-8234-93f404cf5910
INFO:     127.0.0.1:57947 - "PUT /api/v1/chapters/8e5ced71-2612-46cd-8234-93f404cf5910 HTTP/1.1" 200 OK
2026-01-27 22:44:18,685 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第59章 上架感言：萌新求订阅 (order=50)
2026-01-27 22:44:18,692 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/stream
2026-01-27 22:44:18,695 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21
INFO:     127.0.0.1:62374 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2026-01-27 22:44:18,697 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/8e5ced71-2612-46cd-8234-93f404cf5910
INFO:     127.0.0.1:57946 - "PUT /api/v1/chapters/8e5ced71-2612-46cd-8234-93f404cf5910 HTTP/1.1" 200 OK
2026-01-27 22:44:21,310 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第59章 上架感言：萌新求订阅 (order=50)
2026-01-27 22:44:21,325 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 仅限第34–50章。输出至少18条原文证据，覆盖以下主题：

  1. 段德被林仙“抢/加钱/三擒三...
2026-01-27 22:44:21,342 - app.api.v1.agent - INFO - [agent_chat_stream] 📚 世界观数据已注入: 人物=8, 地点=7, 设定=7, 规范=无
2026-01-27 22:44:21,342 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21:f572379b-fd47-4986-9833-0e1aa63a6308 (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, conversation_id=f572379b-fd47-4986-9833-0e1aa63a6308)
2026-01-27 22:44:21,347 - app.services.context.manager - INFO - [ContextManager] 创建新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21:f572379b-fd47-4986-9833-0e1aa63a6308
2026-01-27 22:44:21,347 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21:f572379b-fd47-4986-9833-0e1aa63a6308: 0/16000 tokens
2026-01-27 22:44:21,443 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='仅限第34–50章。输出至少18条原文证据，覆盖以下主题：
...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=3条
2026-01-27 22:44:21,443 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21 | 含用户级=True | 找到=3条
2026-01-27 22:44:21,453 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 1条消息, 0 tokens, 耗时 111.20ms
2026-01-27 22:44:21,453 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 1 条历史消息 (token: 0, has_summary: False)
2026-01-27 22:44:21,454 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:44:21,454 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:44:21,455 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=200, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-27 22:44:21,462 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第59章 上架感言：萌新求订阅 (144 paragraphs)
2026-01-27 22:44:23,460 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第59章 上架感言：萌新求订阅 (144 paragraphs)
2026-01-27 22:44:24,863 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:44:24,865 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:44:24,873 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:44:24,877 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=594, cost=$0.000065, time=3409ms
2026-01-27 22:44:24,877 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=39, 尝试次数=1
2026-01-27 22:44:24,877 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:44:24,877 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:44:24,877 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=20, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-27 22:44:25,794 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:44:25,794 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:44:25,804 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:44:25,805 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=521, cost=$0.000052, time=916ms
2026-01-27 22:44:25,805 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=7, 尝试次数=1
2026-01-27 22:44:25,806 - app.services.agent.intent.classifier - INFO - [Intent] AI识别结果: writing
2026-01-27 22:44:25,806 - app.services.agent.langgraph_agent - INFO - [Planning] AI意图分类: writing (置信度: 0.90)
2026-01-27 22:44:25,806 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 仅限第34–50章。输出至少18条原文证据，覆盖以下主题：

  1. 段德被林仙“抢/加钱/三擒三...
2026-01-27 22:44:25,811 - app.core.cache - INFO - ✅ 缓存命中: prompt:planning:v2.41.0:get_planning_static_prompt:fca6eb91156619d0
2026-01-27 22:44:25,817 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-27 22:44:25,818 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=story_planning, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: story_planning; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-01-27 22:44:25,818 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.3, task_type=TaskType.STORY_PLANNING
2026-01-27 22:44:43,003 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-27 22:44:49,248 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 13 个数据块，总长度: 1470
2026-01-27 22:44:49,248 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 22227 (prompt=21487, completion=740)
2026-01-27 22:44:49,248 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:44:49,248 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-27 22:44:49,262 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:44:49,262 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=22227, cost=$0.034259, time=23430ms
2026-01-27 22:44:49,262 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=22227
2026-01-27 22:44:49,262 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户需要一个格式化的原文证据列表，这些证据从第34章到第50, 原料=需要访问作品的第34章到第50章的全部内, 处理=使用`explore_content`工
2026-01-27 22:44:49,268 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共1个任务
2026-01-27 22:44:49,268 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共1个任务，耗时: 23.46s
2026-01-27 22:44:49,268 - app.api.v1.agent - INFO - [Stream] Plan tasks: 1 items
2026-01-27 22:44:49,268 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2026-01-27 22:44:49,268 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2026-01-27 22:44:49,268 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2026-01-27 22:44:49,268 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] DAG 调度启用，任务数=1, 有依赖任务=0
2026-01-27 22:44:49,268 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1开始: 在第34章至第50章的范围内，检索并提取与“段德林仙”、“妖帝坟”、“源”、“盗墓考古”、“仙珍图线索”、“叶凡身份暗示”等六个主题相关的原文段落。
2026-01-27 22:44:49,268 - app.api.v1.agent - INFO - [Stream] Task started: 在第34章至第50章的范围内，检索并提取与“段德林仙”、“妖帝坟”、“源”、“盗墓考古”、“仙珍图线索”、“叶凡身份暗示”等六个主题相关的原文段落。 (icon=Wrench)
2026-01-27 22:44:49,268 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: explore_content
2026-01-27 22:44:49,268 - app.services.agent.tools.explore_tools - INFO - [explore_content] 开始: work_id=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, target=在第34至50章中，检索并提取与以下主题相关的原文证据：1. 段德与林仙的互动（抢劫、加钱、擒纵、通...
2026-01-27 22:44:49,268 - app.services.agent.tools.explore_tools - INFO - [explore_content] 规划传入关键词: ['段德', '林仙', '抢', '加钱', '三擒三纵', '通灵兵器', '妖帝坟', '青帝坟', '帝兵', '混沌青莲']
2026-01-27 22:44:49,275 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 启用严格段落号模式
2026-01-27 22:44:49,275 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 章节范围锁定: 第34-50章
2026-01-27 22:44:49,276 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 任务禁止整章阅读
2026-01-27 22:44:49,277 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 开始探索 V5: work_id=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, target=在第34至50章中，检索并提取与以下主题相关的原文证据：1. 段德与林仙的互动（抢劫、加钱、擒纵、通...
2026-01-27 22:44:49,277 - app.services.chapter_service - INFO - [ChapterService] Querying chapters for work_id=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, type=<class 'uuid.UUID'>
2026-01-27 22:44:49,281 - app.services.chapter_service - INFO - [ChapterService] Found 77 chapters
2026-01-27 22:44:49,281 - app.services.chapter_service - INFO -   - Chapter: 第1章 【摆烂的宿主】, order=1
2026-01-27 22:44:49,281 - app.services.chapter_service - INFO -   - ... (75 more chapters)
2026-01-27 22:44:49,281 - app.services.chapter_service - INFO -   - Chapter: 第100章 【火域铸真器，两脉起冲突】, order=77
2026-01-27 22:44:49,322 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 章节范围映射: 第34-50章 -> 第28-43章
2026-01-27 22:44:49,323 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:44:49,323 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:44:49,323 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:44:51,649 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:44:51,649 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:44:51,653 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:44:51,653 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=666, cost=$0.000105, time=2326ms
2026-01-27 22:44:51,653 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=266, 尝试次数=1
2026-01-27 22:44:51,671 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['段德,林仙']..., mode=all, range=(28, 43), hits=0
2026-01-27 22:44:51,671 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:44:51,671 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:44:51,671 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:44:53,560 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:44:53,560 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:44:53,571 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:44:53,571 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=845, cost=$0.000161, time=1889ms
2026-01-27 22:44:53,571 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=526, 尝试次数=1
2026-01-27 22:44:53,615 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['妖帝坟', '青帝', '帝兵']..., mode=any, range=(28, 43), hits=10
2026-01-27 22:44:53,615 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:44:53,615 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:44:53,615 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:44:55,587 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:44:55,588 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:44:55,595 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:44:55,595 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1233, cost=$0.000185, time=1973ms
2026-01-27 22:44:55,595 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=450, 尝试次数=1
2026-01-27 22:44:55,605 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第14段
2026-01-27 22:44:55,612 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第33章第5段
2026-01-27 22:44:55,612 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第33章第27段
2026-01-27 22:44:55,612 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:44:55,612 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:44:55,618 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:44:57,725 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:44:57,725 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:44:57,741 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:44:57,741 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1534, cost=$0.000224, time=2107ms
2026-01-27 22:44:57,741 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=480, 尝试次数=1
2026-01-27 22:44:57,748 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第14段
2026-01-27 22:44:57,752 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第15段
2026-01-27 22:44:57,752 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第16段
2026-01-27 22:44:57,762 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:44:57,763 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:44:57,763 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:44:59,899 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:44:59,899 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:44:59,906 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:44:59,906 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1513, cost=$0.000215, time=2135ms
2026-01-27 22:44:59,906 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=407, 尝试次数=1
2026-01-27 22:44:59,911 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第14段
2026-01-27 22:44:59,911 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第15段
2026-01-27 22:44:59,911 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:44:59,911 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:44:59,911 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:45:02,218 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:45:02,218 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:45:02,230 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:45:02,230 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1500, cost=$0.000210, time=2307ms
2026-01-27 22:45:02,230 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=393, 尝试次数=1
2026-01-27 22:45:02,235 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第14段
2026-01-27 22:45:02,246 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第15段
2026-01-27 22:45:02,247 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:45:02,247 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:45:02,247 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:45:03,908 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:45:03,908 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:45:03,918 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:45:03,919 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1533, cost=$0.000224, time=1661ms
2026-01-27 22:45:03,920 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=436, 尝试次数=1
2026-01-27 22:45:03,925 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第14段
2026-01-27 22:45:03,925 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第15段
2026-01-27 22:45:03,925 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:45:03,925 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:45:03,925 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:45:06,419 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:45:06,419 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:45:06,437 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:45:06,437 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1522, cost=$0.000219, time=2497ms
2026-01-27 22:45:06,437 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=419, 尝试次数=1
2026-01-27 22:45:06,442 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第14段
2026-01-27 22:45:06,449 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第15段
2026-01-27 22:45:06,449 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:45:06,449 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:45:06,449 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:45:08,742 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:45:08,742 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:45:08,742 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:45:08,742 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1510, cost=$0.000214, time=2292ms
2026-01-27 22:45:08,742 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=403, 尝试次数=1
2026-01-27 22:45:08,753 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第14段
2026-01-27 22:45:08,753 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第15段
2026-01-27 22:45:08,762 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:45:08,762 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:45:08,762 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:45:10,325 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:45:10,325 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:45:10,330 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:45:10,330 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1518, cost=$0.000217, time=1563ms
2026-01-27 22:45:10,330 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=415, 尝试次数=1
2026-01-27 22:45:10,337 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第14段
2026-01-27 22:45:10,337 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第15段
2026-01-27 22:45:10,337 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:45:10,337 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:45:10,337 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:45:11,938 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:45:11,939 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:45:11,946 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:45:11,946 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1512, cost=$0.000215, time=1602ms
2026-01-27 22:45:11,946 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=406, 尝试次数=1
2026-01-27 22:45:11,956 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第14段
2026-01-27 22:45:11,956 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第15段
2026-01-27 22:45:11,956 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:45:11,956 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:45:11,956 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:45:14,865 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:45:14,866 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:45:14,874 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:45:14,875 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1536, cost=$0.000224, time=2909ms
2026-01-27 22:45:14,876 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=434, 尝试次数=1
2026-01-27 22:45:14,879 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第14段
2026-01-27 22:45:14,883 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第15段
2026-01-27 22:45:14,883 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:45:14,888 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:45:14,888 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:45:16,270 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:45:16,270 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:45:16,282 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:45:16,282 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1484, cost=$0.000204, time=1385ms
2026-01-27 22:45:16,282 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=375, 尝试次数=1
2026-01-27 22:45:16,291 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第14段
2026-01-27 22:45:16,295 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第15段
2026-01-27 22:45:16,295 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:45:16,295 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:45:16,295 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:45:17,862 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:45:17,863 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:45:17,870 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:45:17,870 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1488, cost=$0.000205, time=1568ms
2026-01-27 22:45:17,870 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=378, 尝试次数=1
2026-01-27 22:45:17,877 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第14段
2026-01-27 22:45:17,880 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第15段
2026-01-27 22:45:17,880 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:45:17,880 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:45:17,880 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:45:20,133 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:45:20,134 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:45:20,141 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:45:20,141 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1596, cost=$0.000248, time=2253ms
2026-01-27 22:45:20,141 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=586, 尝试次数=1
2026-01-27 22:45:20,152 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['段德', '林仙', '叶凡']..., mode=any, range=(28, 43), hits=10
2026-01-27 22:45:20,152 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:45:20,152 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:45:20,152 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:45:24,760 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:45:24,762 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:45:24,769 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:45:24,769 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2056, cost=$0.000542, time=4610ms
2026-01-27 22:45:24,769 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=2831, 尝试次数=1
2026-01-27 22:45:24,779 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第1段
2026-01-27 22:45:24,785 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第2段
2026-01-27 22:45:24,785 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第3段
2026-01-27 22:45:24,795 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第4段
2026-01-27 22:45:24,798 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第5段
2026-01-27 22:45:24,804 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第6段
2026-01-27 22:45:24,808 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第7段
2026-01-27 22:45:24,809 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第8段
2026-01-27 22:45:24,816 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第9段
2026-01-27 22:45:24,816 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第10段
2026-01-27 22:45:24,823 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第11段
2026-01-27 22:45:24,829 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第12段
2026-01-27 22:45:24,829 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第13段
2026-01-27 22:45:24,840 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第14段
2026-01-27 22:45:24,841 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第15段
2026-01-27 22:45:24,848 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第16段
2026-01-27 22:45:24,855 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第17段
2026-01-27 22:45:24,858 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第18段
2026-01-27 22:45:24,858 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第19段
2026-01-27 22:45:24,871 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第20段
2026-01-27 22:45:24,872 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第21段
2026-01-27 22:45:24,879 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第22段
2026-01-27 22:45:24,879 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第23段
2026-01-27 22:45:24,888 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第24段
2026-01-27 22:45:24,891 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第25段
2026-01-27 22:45:24,891 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第26段
2026-01-27 22:45:24,900 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第27段
2026-01-27 22:45:24,905 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第28段
2026-01-27 22:45:24,910 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第29段
2026-01-27 22:45:24,910 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第30段
2026-01-27 22:45:24,919 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第31段
2026-01-27 22:45:24,923 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第32段
2026-01-27 22:45:24,923 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第33段
2026-01-27 22:45:24,931 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:45:24,931 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:45:24,931 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:45:27,380 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:45:27,382 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:45:27,392 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:45:27,392 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1581, cost=$0.000245, time=2450ms
2026-01-27 22:45:27,392 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=582, 尝试次数=1
2026-01-27 22:45:27,416 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['段德', '林仙', '妖帝坟']..., mode=all, range=(28, 43), hits=0
2026-01-27 22:45:27,419 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:45:27,419 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:45:27,419 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:45:29,840 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:45:29,840 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:45:29,854 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:45:29,854 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1091, cost=$0.000223, time=2422ms
2026-01-27 22:45:29,854 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=717, 尝试次数=1
2026-01-27 22:45:29,867 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['抢劫', '加钱', '擒纵']..., mode=all, range=(28, 43), hits=0
2026-01-27 22:45:29,867 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:45:29,867 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:45:29,867 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:45:31,361 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:45:31,361 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:45:31,371 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:45:31,371 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=802, cost=$0.000128, time=1494ms
2026-01-27 22:45:31,371 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=337, 尝试次数=1
2026-01-27 22:45:31,385 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['段德', '林仙', '抢劫']..., mode=all, range=(28, 43), hits=0
2026-01-27 22:45:31,385 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:45:31,385 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:45:31,385 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:45:32,594 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:45:32,594 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:45:32,609 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:45:32,611 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=789, cost=$0.000124, time=1209ms
2026-01-27 22:45:32,611 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=311, 尝试次数=1
2026-01-27 22:45:32,633 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['段德', '林仙', '抢劫']..., mode=any, range=(28, 43), hits=1
2026-01-27 22:45:32,638 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:45:32,638 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:45:32,639 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:45:34,510 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:45:34,510 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:45:34,517 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:45:34,518 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=829, cost=$0.000120, time=1871ms
2026-01-27 22:45:34,518 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=265, 尝试次数=1
2026-01-27 22:45:34,524 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第28章第19段
2026-01-27 22:45:34,525 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 探索完成(工具循环): 21轮, 原因=达到读取上限
2026-01-27 22:45:34,527 - app.services.agent.execution.tool_executor - INFO - [StandardTool] explore_content 执行成功
2026-01-27 22:45:34,528 - app.api.v1.agent - INFO - [Stream] 任务完成: 在第34章至第50章的范围内，检索并提取与“段德林仙”、“妖帝坟”、“源”、“盗墓考古”、“仙珍图线索”、“叶凡身份暗示”等六个主题相关的原文段落。 (45.3s)
2026-01-27 22:45:34,528 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1完成
2026-01-27 22:45:34,528 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共1个任务，耗时: 45.26s
2026-01-27 22:45:34,528 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2026-01-27 22:45:34,529 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=1, 展示型=0
2026-01-27 22:45:34,529 - app.services.agent.langgraph_agent - INFO - [Response] 单个输出任务(explore_content)，使用AI整合
2026-01-27 22:45:34,529 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2026-01-27 22:45:34,529 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=1, 展示型=0
2026-01-27 22:45:34,530 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=20031字符, 处理后=337字符
2026-01-27 22:45:34,530 - app.services.agent.planning.response_builder - INFO - [Summarization] 准备发送 summarization_start 事件
2026-01-27 22:45:34,530 - app.services.agent.stream.stream_event_handler - INFO - [StreamEventHandler] emit_summarization_start 被调用, _on_flow_event=True
2026-01-27 22:45:34,530 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_start 事件已发送
2026-01-27 22:45:34,530 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2026-01-27 22:45:34,530 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2026-01-27 22:45:34,534 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-27 22:45:34,534 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-27 22:45:34,534 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
2026-01-27 22:46:21,675 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-27 22:46:21,679 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_complete 事件已发送（第一个chunk时）
2026-01-27 22:46:21,679 - app.services.agent.planning.response_builder - INFO - [Summarization] output_ready 事件已发送（第一个chunk时）
2026-01-27 22:46:24,961 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 12 个数据块，总长度: 962
2026-01-27 22:46:24,962 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 21872 (prompt=21139, completion=733)
2026-01-27 22:46:24,962 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:46:24,963 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-27 22:46:24,981 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:46:24,983 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=21872, cost=$0.008174, time=50429ms
2026-01-27 22:46:24,985 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=962
2026-01-27 22:46:25,866 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21 | 重要度=0.84
2026-01-27 22:46:26,736 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21 | 重要度=0.73
2026-01-27 22:46:26,741 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21:f572379b-fd47-4986-9833-0e1aa63a6308, token=1384
2026-01-27 22:46:26,743 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21:f572379b-fd47-4986-9833-0e1aa63a6308, 消息数=2, 摘要长度=0, Token=1384
2026-01-27 22:46:26,743 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21:f572379b-fd47-4986-9833-0e1aa63a6308)
2026-01-27 22:46:26,744 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2026-01-27 22:46:26,751 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed
2026-01-27 22:46:31,412 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/f572379b-fd47-4986-9833-0e1aa63a6308
INFO:     127.0.0.1:62351 - "GET /api/v1/agent/operations/f572379b-fd47-4986-9833-0e1aa63a6308 HTTP/1.1" 200 OK
2026-01-27 22:46:34,758 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, chapter_id: 9e73c137-ec1f-4346-b911-993eaaf0b14e
2026-01-27 22:46:34,764 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 9e73c137-ec1f-4346-b911-993eaaf0b14e
2026-01-27 22:46:34,765 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: e2767773-00d9-478e-92df-ecf810ed3847
2026-01-27 22:46:34,766 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-27 22:46:34,770 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:57397 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-27 22:46:34,788 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, chapter_id: 9e73c137-ec1f-4346-b911-993eaaf0b14e
2026-01-27 22:46:34,798 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 9e73c137-ec1f-4346-b911-993eaaf0b14e
2026-01-27 22:46:34,801 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: e2767773-00d9-478e-92df-ecf810ed3847
2026-01-27 22:46:34,801 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-27 22:46:34,802 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/9e73c137-ec1f-4346-b911-993eaaf0b14e/revisions
2026-01-27 22:46:34,802 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:50295 - "GET /api/v1/chapters/9e73c137-ec1f-4346-b911-993eaaf0b14e/revisions?status=pending HTTP/1.1" 200 OK
INFO:     127.0.0.1:50291 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-27 22:46:34,874 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:50293 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2026-01-27 22:46:34,883 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/9e73c137-ec1f-4346-b911-993eaaf0b14e/revisions
INFO:     127.0.0.1:49235 - "GET /api/v1/chapters/9e73c137-ec1f-4346-b911-993eaaf0b14e/revisions?status=pending HTTP/1.1" 200 OK
2026-01-27 22:46:35,084 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21
2026-01-27 22:46:35,085 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/9e73c137-ec1f-4346-b911-993eaaf0b14e
INFO:     127.0.0.1:57688 - "PUT /api/v1/chapters/9e73c137-ec1f-4346-b911-993eaaf0b14e HTTP/1.1" 200 OK
2026-01-27 22:46:35,088 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第79章 【大不了打沉东荒！】 (order=60)
2026-01-27 22:46:37,621 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第79章 【大不了打沉东荒！】 (88 paragraphs)
2026-01-27 22:46:37,654 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 9e73c137-ec1f-4346-b911-993eaaf0b14e 内容更新，新段落数: 88
2026-01-27 22:46:37,678 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21
2026-01-27 22:46:37,678 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/9e73c137-ec1f-4346-b911-993eaaf0b14e
INFO:     127.0.0.1:54934 - "PUT /api/v1/chapters/9e73c137-ec1f-4346-b911-993eaaf0b14e HTTP/1.1" 200 OK
2026-01-27 22:46:37,678 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第79章 【大不了打沉东荒！】 (order=60)
2026-01-27 22:46:39,932 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第79章 【大不了打沉东荒！】 (88 paragraphs)
2026-01-27 22:46:39,968 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 9e73c137-ec1f-4346-b911-993eaaf0b14e 内容更新，新段落数: 88
2026-01-27 22:46:39,982 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21
2026-01-27 22:46:39,984 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/9e73c137-ec1f-4346-b911-993eaaf0b14e
INFO:     127.0.0.1:63689 - "PUT /api/v1/chapters/9e73c137-ec1f-4346-b911-993eaaf0b14e HTTP/1.1" 200 OK
2026-01-27 22:46:39,985 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第79章 【大不了打沉东荒！】 (order=60)
2026-01-27 22:46:42,715 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第79章 【大不了打沉东荒！】 (88 paragraphs)
2026-01-27 22:46:42,902 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:53896 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2026-01-27 22:46:43,000 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21
2026-01-27 22:46:43,007 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/9e73c137-ec1f-4346-b911-993eaaf0b14e
INFO:     127.0.0.1:63550 - "PUT /api/v1/chapters/9e73c137-ec1f-4346-b911-993eaaf0b14e HTTP/1.1" 200 OK
2026-01-27 22:46:43,016 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第79章 【大不了打沉东荒！】 (order=60)
2026-01-27 22:46:46,657 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-27 22:46:46,657 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-27 22:46:46,657 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2026-01-27 22:46:48,762 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz:8443/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-27 22:46:48,771 - app.api.v1.agent - INFO - [Chat Stream] Mode: planning
2026-01-27 22:46:48,779 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:59629 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2026-01-27 22:46:48,780 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第79章 【大不了打沉东荒！】 (88 paragraphs)
2026-01-27 22:46:48,786 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 输出至少15条原文证据，覆盖以下主题：

  1. 林仙传法给叶凡（炁体源流/五雷正法/拘灵遣将/道...
2026-01-27 22:46:48,799 - app.api.v1.agent - INFO - [agent_chat_stream] 📚 世界观数据已注入: 人物=8, 地点=7, 设定=7, 规范=无
2026-01-27 22:46:48,800 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21:540c4675-a4d4-422f-aa79-3dbb0722234b (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, conversation_id=540c4675-a4d4-422f-aa79-3dbb0722234b)
2026-01-27 22:46:48,802 - app.services.context.manager - INFO - [ContextManager] 创建新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21:540c4675-a4d4-422f-aa79-3dbb0722234b
2026-01-27 22:46:48,803 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21:540c4675-a4d4-422f-aa79-3dbb0722234b: 0/16000 tokens
2026-01-27 22:46:48,977 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='输出至少15条原文证据，覆盖以下主题：

  1. 林仙传法...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=3条
2026-01-27 22:46:48,977 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21 | 含用户级=True | 找到=3条
2026-01-27 22:46:48,990 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 1条消息, 0 tokens, 耗时 189.58ms
2026-01-27 22:46:48,990 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 1 条历史消息 (token: 0, has_summary: False)
2026-01-27 22:46:48,991 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:46:48,992 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:46:48,992 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=200, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-27 22:46:50,550 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:46:50,550 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:46:50,581 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:46:50,584 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=587, cost=$0.000064, time=1565ms
2026-01-27 22:46:50,585 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=39, 尝试次数=1
2026-01-27 22:46:50,588 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:46:50,589 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:46:50,590 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=20, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-27 22:46:51,953 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:46:51,953 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:46:51,966 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:46:51,966 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=514, cost=$0.000052, time=1364ms
2026-01-27 22:46:51,966 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=7, 尝试次数=1
2026-01-27 22:46:51,966 - app.services.agent.intent.classifier - INFO - [Intent] AI识别结果: writing
2026-01-27 22:46:51,966 - app.services.agent.langgraph_agent - INFO - [Planning] AI意图分类: writing (置信度: 0.90)
2026-01-27 22:46:51,966 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 输出至少15条原文证据，覆盖以下主题：

  1. 林仙传法给叶凡（炁体源流/五雷正法/拘灵遣将/道...
2026-01-27 22:46:51,976 - app.core.cache - INFO - ✅ 缓存命中: prompt:planning:v2.41.0:get_planning_static_prompt:fca6eb91156619d0
2026-01-27 22:46:51,983 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-27 22:46:51,984 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=story_planning, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: story_planning; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-01-27 22:46:51,984 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.3, task_type=TaskType.STORY_PLANNING
2026-01-27 22:47:04,392 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-27 22:47:16,585 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 23 个数据块，总长度: 3787
2026-01-27 22:47:16,585 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 22561 (prompt=21110, completion=1451)
2026-01-27 22:47:16,585 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:47:16,585 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-27 22:47:16,596 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:47:16,597 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=22561, cost=$0.040898, time=24601ms
2026-01-27 22:47:16,598 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=22561
2026-01-27 22:47:16,598 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户期望得到一个包含至少15条原文证据的列表，每条证据都按照, 原料=需要通过在当前章节内搜索与六个主题相关的, 处理=使用 explore_content 工
2026-01-27 22:47:16,598 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共1个任务
2026-01-27 22:47:16,598 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共1个任务，耗时: 24.63s
2026-01-27 22:47:16,599 - app.api.v1.agent - INFO - [Stream] Plan tasks: 1 items
2026-01-27 22:47:16,599 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2026-01-27 22:47:16,599 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2026-01-27 22:47:16,599 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2026-01-27 22:47:16,599 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] DAG 调度启用，任务数=1, 有依赖任务=0
2026-01-27 22:47:16,599 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1开始: 在当前章节中，根据用户提供的六个主题，搜索相关的原文证据，包括林仙传法、圣体消耗、盗墓对白、青帝妖族、系统吐槽、叶凡修行等方面。
2026-01-27 22:47:16,600 - app.api.v1.agent - INFO - [Stream] Task started: 在当前章节中，根据用户提供的六个主题，搜索相关的原文证据，包括林仙传法、圣体消耗、盗墓对白、青帝妖族、系统吐槽、叶凡修行等方面。 (icon=Wrench)
2026-01-27 22:47:16,600 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: explore_content
2026-01-27 22:47:16,600 - app.services.agent.tools.explore_tools - INFO - [explore_content] 开始: work_id=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, target=输出至少15条原文证据，覆盖以下主题：1. 林仙传法给叶凡（炁体源流/五雷正法/拘灵遣将/道经等）直...
2026-01-27 22:47:16,601 - app.services.agent.tools.explore_tools - INFO - [explore_content] 规划传入关键词: ['林仙', '传法', '炁体源流', '五雷正法', '拘灵遣将', '道经', '荒古圣体', '资源消耗', '道宫', '源']
2026-01-27 22:47:16,602 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 启用严格段落号模式
2026-01-27 22:47:16,602 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 任务禁止整章阅读
2026-01-27 22:47:16,602 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 开始探索 V5: work_id=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, target=输出至少15条原文证据，覆盖以下主题：1. 林仙传法给叶凡（炁体源流/五雷正法/拘灵遣将/道经等）直...
2026-01-27 22:47:16,602 - app.services.chapter_service - INFO - [ChapterService] Querying chapters for work_id=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, type=<class 'uuid.UUID'>
2026-01-27 22:47:16,606 - app.services.chapter_service - INFO - [ChapterService] Found 77 chapters
2026-01-27 22:47:16,606 - app.services.chapter_service - INFO -   - Chapter: 第1章 【摆烂的宿主】, order=1
2026-01-27 22:47:16,606 - app.services.chapter_service - INFO -   - ... (75 more chapters)
2026-01-27 22:47:16,606 - app.services.chapter_service - INFO -   - Chapter: 第100章 【火域铸真器，两脉起冲突】, order=77
2026-01-27 22:47:16,632 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:47:16,634 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:47:16,634 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:47:18,654 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:47:18,654 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:47:18,668 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:47:18,670 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=627, cost=$0.000096, time=2022ms
2026-01-27 22:47:18,672 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=229, 尝试次数=1
2026-01-27 22:47:18,725 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['林仙传法']..., mode=any, range=None, hits=0
2026-01-27 22:47:18,727 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:47:18,727 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:47:18,727 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:47:20,214 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:47:20,215 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:47:20,221 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:47:20,222 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=690, cost=$0.000106, time=1487ms
2026-01-27 22:47:20,223 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=243, 尝试次数=1
2026-01-27 22:47:20,229 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['叶凡', '林仙', '传法']..., mode=any, range=None, hits=10
2026-01-27 22:47:20,232 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:47:20,232 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:47:20,232 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:47:21,725 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:47:21,725 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:47:21,727 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:47:21,738 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1044, cost=$0.000160, time=1493ms
2026-01-27 22:47:21,738 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=374, 尝试次数=1
2026-01-27 22:47:21,760 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['炁体源流', '五雷正法', '拘灵遣将']..., mode=all, range=None, hits=0
2026-01-27 22:47:21,760 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:47:21,760 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:47:21,760 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:47:23,083 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:47:23,083 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:47:23,092 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:47:23,092 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=777, cost=$0.000128, time=1322ms
2026-01-27 22:47:23,092 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=323, 尝试次数=1
2026-01-27 22:47:23,104 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['林仙', '叶凡', '传法']..., mode=any, range=None, hits=10
2026-01-27 22:47:23,104 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:47:23,104 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:47:23,104 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:47:24,864 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:47:24,864 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:47:24,871 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:47:24,871 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1070, cost=$0.000158, time=1761ms
2026-01-27 22:47:24,871 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=331, 尝试次数=1
2026-01-27 22:47:24,917 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['叶凡', '林仙', '传法']..., mode=all, range=None, hits=0
2026-01-27 22:47:24,917 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:47:24,917 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:47:24,917 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:47:26,679 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:47:26,679 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:47:26,687 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:47:26,687 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=805, cost=$0.000135, time=1761ms
2026-01-27 22:47:26,687 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=350, 尝试次数=1
2026-01-27 22:47:26,702 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['叶凡', '林仙', '传法']..., mode=any, range=None, hits=10
2026-01-27 22:47:26,704 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:47:26,704 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:47:26,704 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:47:28,117 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:47:28,117 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:47:28,123 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:47:28,124 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1080, cost=$0.000162, time=1413ms
2026-01-27 22:47:28,124 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=324, 尝试次数=1
2026-01-27 22:47:28,139 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['林仙', '叶凡', '传法']..., mode=any, range=None, hits=10
2026-01-27 22:47:28,140 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:47:28,140 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:47:28,140 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:47:29,546 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:47:29,546 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:47:29,561 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:47:29,561 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1037, cost=$0.000145, time=1405ms
2026-01-27 22:47:29,561 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=277, 尝试次数=1
2026-01-27 22:47:29,639 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['荒古圣体', '道宫', '修行资源']..., mode=any, range=None, hits=5
2026-01-27 22:47:29,649 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:47:29,649 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:47:29,649 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:47:31,186 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:47:31,186 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:47:31,196 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:47:31,196 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=925, cost=$0.000138, time=1537ms
2026-01-27 22:47:31,196 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=315, 尝试次数=1
2026-01-27 22:47:31,212 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['林仙', '传法', '叶凡']..., mode=any, range=None, hits=10
2026-01-27 22:47:31,212 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:47:31,212 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:47:31,212 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:47:33,160 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:47:33,160 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:47:33,170 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:47:33,170 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1071, cost=$0.000160, time=1948ms
2026-01-27 22:47:33,171 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=344, 尝试次数=1
2026-01-27 22:47:33,183 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['叶凡', '林仙', '传法']..., mode=any, range=None, hits=10
2026-01-27 22:47:33,183 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:47:33,183 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:47:33,183 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:47:34,570 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:47:34,570 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:47:34,578 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:47:34,578 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1083, cost=$0.000163, time=1388ms
2026-01-27 22:47:34,579 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=353, 尝试次数=1
2026-01-27 22:47:34,589 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['叶凡', '林仙', '传法']..., mode=any, range=None, hits=5
2026-01-27 22:47:34,589 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:47:34,590 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:47:34,590 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:47:36,475 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:47:36,475 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:47:36,486 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:47:36,486 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=968, cost=$0.000150, time=1885ms
2026-01-27 22:47:36,486 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=353, 尝试次数=1
2026-01-27 22:47:36,500 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['叶凡', '林仙', '传法']..., mode=any, range=None, hits=10
2026-01-27 22:47:36,503 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:47:36,504 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:47:36,505 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:47:37,949 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:47:37,949 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:47:37,961 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:47:37,961 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1048, cost=$0.000149, time=1444ms
2026-01-27 22:47:37,961 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=291, 尝试次数=1
2026-01-27 22:47:37,991 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['叶凡', '林仙', '传法']..., mode=any, range=None, hits=50
2026-01-27 22:47:37,994 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:47:37,994 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:47:37,994 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:47:39,329 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:47:39,329 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:47:39,342 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:47:39,348 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1069, cost=$0.000157, time=1334ms
2026-01-27 22:47:39,349 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=330, 尝试次数=1
2026-01-27 22:47:39,377 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['叶凡', '林仙', '传法']..., mode=any, range=None, hits=50
2026-01-27 22:47:39,379 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:47:39,380 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:47:39,380 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:47:40,930 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:47:40,930 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:47:40,943 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:47:40,950 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1079, cost=$0.000161, time=1550ms
2026-01-27 22:47:40,950 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=422, 尝试次数=1
2026-01-27 22:47:40,968 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第2段
2026-01-27 22:47:40,974 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第6段
2026-01-27 22:47:40,991 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第10段
2026-01-27 22:47:41,003 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第12段
2026-01-27 22:47:41,008 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第13段
2026-01-27 22:47:41,008 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:47:41,016 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:47:41,016 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:47:42,990 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:47:42,991 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:47:42,999 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:47:42,999 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1563, cost=$0.000251, time=1975ms
2026-01-27 22:47:42,999 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=608, 尝试次数=1
2026-01-27 22:47:43,034 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['千万斤源', '段德', '抢宝']..., mode=any, range=None, hits=10
2026-01-27 22:47:43,035 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:47:43,036 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:47:43,036 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:47:44,888 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:47:44,889 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:47:44,899 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:47:44,901 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1094, cost=$0.000183, time=1852ms
2026-01-27 22:47:44,901 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=501, 尝试次数=1
2026-01-27 22:47:44,938 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['林仙', '传法', '叶凡']..., mode=any, range=None, hits=10
2026-01-27 22:47:44,938 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:47:44,941 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:47:44,941 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:47:47,609 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:47:47,609 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:47:47,624 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:47:47,625 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1332, cost=$0.000247, time=2668ms
2026-01-27 22:47:47,625 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=685, 尝试次数=1
2026-01-27 22:47:47,685 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['林仙', '传法', '叶凡']..., mode=all, range=None, hits=0
2026-01-27 22:47:47,685 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:47:47,685 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:47:47,685 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:47:49,304 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:47:49,304 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:47:49,317 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:47:49,319 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=882, cost=$0.000142, time=1619ms
2026-01-27 22:47:49,319 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=322, 尝试次数=1
2026-01-27 22:47:49,333 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['林仙', '传法', '叶凡']..., mode=any, range=None, hits=5
2026-01-27 22:47:49,333 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:47:49,333 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:47:49,333 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:47:50,925 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:47:50,926 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:47:50,931 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:47:50,931 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=917, cost=$0.000129, time=1593ms
2026-01-27 22:47:50,931 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=258, 尝试次数=1
2026-01-27 22:47:50,945 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['叶凡', '荒古圣体', '道宫']..., mode=any, range=None, hits=5
2026-01-27 22:47:50,946 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:47:50,947 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:47:50,947 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:47:52,216 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:47:52,216 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:47:52,224 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:47:52,226 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=942, cost=$0.000143, time=1268ms
2026-01-27 22:47:52,226 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=338, 尝试次数=1
2026-01-27 22:47:52,238 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['林仙', '传法', '叶凡']..., mode=any, range=None, hits=10
2026-01-27 22:47:52,238 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:47:52,238 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:47:52,238 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:47:54,274 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:47:54,274 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:47:54,286 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:47:54,288 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1194, cost=$0.000209, time=2035ms
2026-01-27 22:47:54,288 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=589, 尝试次数=1
2026-01-27 22:47:54,328 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['吐槽']..., mode=any, range=None, hits=10
2026-01-27 22:47:54,328 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:47:54,330 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:47:54,330 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:47:55,723 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:47:55,723 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:47:55,725 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:47:55,732 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1012, cost=$0.000145, time=1393ms
2026-01-27 22:47:55,733 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=302, 尝试次数=1
2026-01-27 22:47:55,746 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['林仙', '传法', '叶凡']..., mode=any, range=None, hits=10
2026-01-27 22:47:55,747 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:47:55,747 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:47:55,747 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:47:56,838 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:47:56,838 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:47:56,846 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:47:56,848 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1058, cost=$0.000153, time=1092ms
2026-01-27 22:47:56,849 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=301, 尝试次数=1
2026-01-27 22:47:56,860 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['叶凡', '林仙', '传法']..., mode=any, range=None, hits=5
2026-01-27 22:47:56,860 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:47:56,860 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:47:56,860 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:47:58,436 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:47:58,437 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:47:58,447 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:47:58,448 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=962, cost=$0.000148, time=1576ms
2026-01-27 22:47:58,448 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=328, 尝试次数=1
2026-01-27 22:47:58,460 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['叶凡', '林仙', '传法']..., mode=any, range=None, hits=10
2026-01-27 22:47:58,461 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:47:58,462 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:47:58,462 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:48:00,039 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:48:00,039 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:48:00,046 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:48:00,047 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1082, cost=$0.000162, time=1577ms
2026-01-27 22:48:00,047 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=363, 尝试次数=1
2026-01-27 22:48:00,058 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['叶凡', '林仙', '传法']..., mode=any, range=None, hits=10
2026-01-27 22:48:00,060 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:48:00,061 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:48:00,061 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:48:01,654 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:48:01,655 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:48:01,665 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:48:01,666 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1156, cost=$0.000192, time=1594ms
2026-01-27 22:48:01,668 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=529, 尝试次数=1
2026-01-27 22:48:01,702 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['叶凡', '林仙', '传法']..., mode=any, range=None, hits=10
2026-01-27 22:48:01,702 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:48:01,702 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:48:01,702 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:48:03,353 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:48:03,353 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:48:03,360 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:48:03,360 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1134, cost=$0.000167, time=1650ms
2026-01-27 22:48:03,362 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=362, 尝试次数=1
2026-01-27 22:48:03,397 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['林仙', '传法', '叶凡']..., mode=all, range=None, hits=0
2026-01-27 22:48:03,399 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:48:03,399 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:48:03,399 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:48:05,362 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:48:05,362 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:48:05,372 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:48:05,372 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=780, cost=$0.000124, time=1962ms
2026-01-27 22:48:05,372 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=314, 尝试次数=1
2026-01-27 22:48:05,390 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['林仙', '传法', '叶凡']..., mode=any, range=None, hits=50
2026-01-27 22:48:05,397 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:48:05,398 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:48:05,399 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:48:07,228 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:48:07,228 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:48:07,237 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:48:07,240 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1123, cost=$0.000178, time=1829ms
2026-01-27 22:48:07,241 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=416, 尝试次数=1
2026-01-27 22:48:07,252 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['林仙', '传法', '叶凡']..., mode=any, range=None, hits=10
2026-01-27 22:48:07,252 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:48:07,252 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:48:07,252 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:48:09,185 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:48:09,185 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:48:09,196 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:48:09,198 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1071, cost=$0.000158, time=1932ms
2026-01-27 22:48:09,198 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=333, 尝试次数=1
2026-01-27 22:48:09,205 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['叶凡', '林仙', '传法']..., mode=any, range=None, hits=10
2026-01-27 22:48:09,213 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:48:09,213 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:48:09,214 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:48:10,925 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:48:10,925 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:48:10,925 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:48:10,925 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1060, cost=$0.000153, time=1711ms
2026-01-27 22:48:10,925 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=311, 尝试次数=1
2026-01-27 22:48:10,947 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['叶凡', '林仙', '传法']..., mode=any, range=None, hits=50
2026-01-27 22:48:10,952 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:48:10,953 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:48:10,954 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:48:12,748 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:48:12,749 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:48:12,751 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:48:12,751 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1108, cost=$0.000173, time=1795ms
2026-01-27 22:48:12,751 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=403, 尝试次数=1
2026-01-27 22:48:12,761 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['林仙', '叶凡', '传法']..., mode=any, range=None, hits=10
2026-01-27 22:48:12,761 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:48:12,761 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:48:12,761 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:48:14,003 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:48:14,003 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:48:14,013 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:48:14,013 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1020, cost=$0.000138, time=1242ms
2026-01-27 22:48:14,013 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=270, 尝试次数=1
2026-01-27 22:48:14,024 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['叶凡', '荒古圣体', '道宫']..., mode=any, range=None, hits=5
2026-01-27 22:48:14,024 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:48:14,024 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:48:14,024 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:48:15,417 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:48:15,417 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:48:15,440 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:48:15,445 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=905, cost=$0.000129, time=1392ms
2026-01-27 22:48:15,445 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=269, 尝试次数=1
2026-01-27 22:48:15,459 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['林仙', '传法', '叶凡']..., mode=any, range=None, hits=50
2026-01-27 22:48:15,459 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:48:15,459 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:48:15,459 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:48:16,939 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:48:16,939 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:48:16,946 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:48:16,946 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1080, cost=$0.000161, time=1480ms
2026-01-27 22:48:16,948 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=426, 尝试次数=1
2026-01-27 22:48:16,955 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第2段
2026-01-27 22:48:16,961 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第6段
2026-01-27 22:48:16,968 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第10段
2026-01-27 22:48:16,972 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第12段
2026-01-27 22:48:16,977 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第13段
2026-01-27 22:48:16,979 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:48:16,979 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:48:16,979 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:48:18,778 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:48:18,778 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:48:18,778 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:48:18,778 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1563, cost=$0.000251, time=1799ms
2026-01-27 22:48:18,778 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=631, 尝试次数=1
2026-01-27 22:48:18,823 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['叶凡', '林仙', '传法']..., mode=any, range=None, hits=50
2026-01-27 22:48:18,823 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:48:18,823 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:48:18,827 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:48:20,658 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:48:20,659 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:48:20,670 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:48:20,670 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1116, cost=$0.000159, time=1832ms
2026-01-27 22:48:20,672 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=322, 尝试次数=1
2026-01-27 22:48:20,694 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['林仙', '传法', '叶凡']..., mode=any, range=None, hits=50
2026-01-27 22:48:20,694 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:48:20,694 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:48:20,694 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:48:22,085 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:48:22,086 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:48:22,086 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:48:22,092 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1075, cost=$0.000160, time=1391ms
2026-01-27 22:48:22,093 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=420, 尝试次数=1
2026-01-27 22:48:22,095 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第2段
2026-01-27 22:48:22,105 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第6段
2026-01-27 22:48:22,112 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第10段
2026-01-27 22:48:22,115 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第12段
2026-01-27 22:48:22,121 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第13段
2026-01-27 22:48:22,124 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:48:22,124 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:48:22,125 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:48:24,036 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:48:24,036 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:48:24,048 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:48:24,048 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1544, cost=$0.000244, time=1911ms
2026-01-27 22:48:24,048 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=599, 尝试次数=1
2026-01-27 22:48:24,078 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['林仙', '传法', '叶凡']..., mode=any, range=None, hits=10
2026-01-27 22:48:24,078 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:48:24,078 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:48:24,078 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:48:26,088 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:48:26,088 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:48:26,099 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:48:26,101 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1109, cost=$0.000161, time=2010ms
2026-01-27 22:48:26,101 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=342, 尝试次数=1
2026-01-27 22:48:26,121 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['林仙', '传法', '叶凡']..., mode=any, range=None, hits=50
2026-01-27 22:48:26,124 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:48:26,124 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:48:26,125 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:48:27,497 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:48:27,498 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:48:27,508 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:48:27,508 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1082, cost=$0.000163, time=1372ms
2026-01-27 22:48:27,511 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=427, 尝试次数=1
2026-01-27 22:48:27,521 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第2段
2026-01-27 22:48:27,528 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第6段
2026-01-27 22:48:27,541 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第10段
2026-01-27 22:48:27,549 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第12段
2026-01-27 22:48:27,558 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第13段
2026-01-27 22:48:27,560 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:48:27,560 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:48:27,560 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:48:30,726 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:48:30,726 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:48:30,738 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:48:30,738 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1602, cost=$0.000267, time=3166ms
2026-01-27 22:48:30,738 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=681, 尝试次数=1
2026-01-27 22:48:30,770 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['叶凡', '林仙', '传法']..., mode=any, range=None, hits=20
2026-01-27 22:48:30,770 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:48:30,770 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:48:30,770 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:48:33,036 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:48:33,037 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:48:33,039 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:48:33,039 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1124, cost=$0.000162, time=2267ms
2026-01-27 22:48:33,039 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=334, 尝试次数=1
2026-01-27 22:48:33,060 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['林仙', '传法', '叶凡']..., mode=any, range=None, hits=10
2026-01-27 22:48:33,060 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:48:33,060 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:48:33,060 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:48:34,107 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:48:34,107 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:48:34,118 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:48:34,118 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=956, cost=$0.000112, time=1046ms
2026-01-27 22:48:34,124 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=109, 尝试次数=1
2026-01-27 22:48:34,124 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 探索完成(工具循环): 44轮, 原因=当前搜索结果未能直接命中目标主题，且剩余工具调用次数不足以进行更广泛的搜索以覆盖所有主题。需要更多信息或调整搜索策略。
2026-01-27 22:48:34,124 - app.services.agent.execution.tool_executor - INFO - [StandardTool] explore_content 执行成功
2026-01-27 22:48:34,124 - app.api.v1.agent - INFO - [Stream] 任务完成: 在当前章节中，根据用户提供的六个主题，搜索相关的原文证据，包括林仙传法、圣体消耗、盗墓对白、青帝妖族、系统吐槽、叶凡修行等方面。 (77.5s)
2026-01-27 22:48:34,124 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1完成
2026-01-27 22:48:34,124 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共1个任务，耗时: 77.53s
2026-01-27 22:48:34,124 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2026-01-27 22:48:34,124 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=1, 展示型=0
2026-01-27 22:48:34,124 - app.services.agent.langgraph_agent - INFO - [Response] 单个输出任务(explore_content)，使用AI整合
2026-01-27 22:48:34,124 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2026-01-27 22:48:34,129 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=1, 展示型=0
2026-01-27 22:48:34,129 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=13171字符, 处理后=13240字符
2026-01-27 22:48:34,130 - app.services.agent.planning.response_builder - INFO - [Summarization] 准备发送 summarization_start 事件
2026-01-27 22:48:34,130 - app.services.agent.stream.stream_event_handler - INFO - [StreamEventHandler] emit_summarization_start 被调用, _on_flow_event=True
2026-01-27 22:48:34,130 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_start 事件已发送
2026-01-27 22:48:34,131 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2026-01-27 22:48:34,131 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2026-01-27 22:48:34,136 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-27 22:48:34,136 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-27 22:48:34,138 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
2026-01-27 22:49:30,982 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-27 22:49:30,984 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_complete 事件已发送（第一个chunk时）
2026-01-27 22:49:30,985 - app.services.agent.planning.response_builder - INFO - [Summarization] output_ready 事件已发送（第一个chunk时）
2026-01-27 22:49:35,923 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 19 个数据块，总长度: 1570
2026-01-27 22:49:35,923 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 28151 (prompt=26927, completion=1224)
2026-01-27 22:49:35,923 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:49:35,923 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-27 22:49:35,936 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:49:35,936 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=28151, cost=$0.011138, time=61785ms
2026-01-27 22:49:35,936 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=1570
2026-01-27 22:49:36,250 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21 | 重要度=0.84
2026-01-27 22:49:36,554 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21 | 重要度=0.77
2026-01-27 22:49:36,558 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21:540c4675-a4d4-422f-aa79-3dbb0722234b, token=1937
2026-01-27 22:49:36,558 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21:540c4675-a4d4-422f-aa79-3dbb0722234b, 消息数=2, 摘要长度=0, Token=1937
2026-01-27 22:49:36,559 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21:540c4675-a4d4-422f-aa79-3dbb0722234b)
2026-01-27 22:49:36,559 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2026-01-27 22:49:36,563 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed
2026-01-27 22:49:49,846 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/540c4675-a4d4-422f-aa79-3dbb0722234b
INFO:     127.0.0.1:50063 - "GET /api/v1/agent/operations/540c4675-a4d4-422f-aa79-3dbb0722234b HTTP/1.1" 200 OK
2026-01-27 22:50:40,211 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, chapter_id: 1b7962cc-0889-4258-be51-c09cbec173cf
2026-01-27 22:50:40,218 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 1b7962cc-0889-4258-be51-c09cbec173cf
2026-01-27 22:50:40,219 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: cd91f2ba-36b8-4ed0-b1fb-276153b44430
2026-01-27 22:50:40,220 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-27 22:50:40,221 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:49875 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-27 22:50:40,242 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, chapter_id: 1b7962cc-0889-4258-be51-c09cbec173cf
2026-01-27 22:50:40,250 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 1b7962cc-0889-4258-be51-c09cbec173cf
2026-01-27 22:50:40,254 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: cd91f2ba-36b8-4ed0-b1fb-276153b44430
2026-01-27 22:50:40,254 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-27 22:50:40,257 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
2026-01-27 22:50:40,258 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/1b7962cc-0889-4258-be51-c09cbec173cf/revisions
INFO:     127.0.0.1:61875 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
INFO:     127.0.0.1:61878 - "GET /api/v1/chapters/1b7962cc-0889-4258-be51-c09cbec173cf/revisions?status=pending HTTP/1.1" 200 OK
2026-01-27 22:50:40,314 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:61877 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2026-01-27 22:50:40,348 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/1b7962cc-0889-4258-be51-c09cbec173cf/revisions
INFO:     127.0.0.1:57533 - "GET /api/v1/chapters/1b7962cc-0889-4258-be51-c09cbec173cf/revisions?status=pending HTTP/1.1" 200 OK
2026-01-27 22:50:40,440 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21
2026-01-27 22:50:40,441 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/1b7962cc-0889-4258-be51-c09cbec173cf
INFO:     127.0.0.1:54179 - "PUT /api/v1/chapters/1b7962cc-0889-4258-be51-c09cbec173cf HTTP/1.1" 200 OK
2026-01-27 22:50:40,442 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第96章 【我才是狠人道主！】 (order=73)
2026-01-27 22:50:42,559 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第96章 【我才是狠人道主！】 (78 paragraphs)
2026-01-27 22:50:42,599 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 1b7962cc-0889-4258-be51-c09cbec173cf 内容更新，新段落数: 78
2026-01-27 22:50:42,628 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21
2026-01-27 22:50:42,630 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/1b7962cc-0889-4258-be51-c09cbec173cf
INFO:     127.0.0.1:59732 - "PUT /api/v1/chapters/1b7962cc-0889-4258-be51-c09cbec173cf HTTP/1.1" 200 OK
2026-01-27 22:50:42,631 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第96章 【我才是狠人道主！】 (order=73)
2026-01-27 22:50:45,239 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第96章 【我才是狠人道主！】 (78 paragraphs)
2026-01-27 22:50:45,292 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 1b7962cc-0889-4258-be51-c09cbec173cf 内容更新，新段落数: 78
2026-01-27 22:50:45,317 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21
2026-01-27 22:50:45,319 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/1b7962cc-0889-4258-be51-c09cbec173cf
INFO:     127.0.0.1:57186 - "PUT /api/v1/chapters/1b7962cc-0889-4258-be51-c09cbec173cf HTTP/1.1" 200 OK
2026-01-27 22:50:45,322 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第96章 【我才是狠人道主！】 (order=73)
2026-01-27 22:50:48,052 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第96章 【我才是狠人道主！】 (78 paragraphs)
2026-01-27 22:50:48,098 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21
2026-01-27 22:50:48,100 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/1b7962cc-0889-4258-be51-c09cbec173cf
INFO:     127.0.0.1:64308 - "PUT /api/v1/chapters/1b7962cc-0889-4258-be51-c09cbec173cf HTTP/1.1" 200 OK
2026-01-27 22:50:48,100 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第96章 【我才是狠人道主！】 (order=73)
2026-01-27 22:50:50,881 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
2026-01-27 22:50:50,882 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第96章 【我才是狠人道主！】 (78 paragraphs)
INFO:     127.0.0.1:65113 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2026-01-27 22:50:50,905 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-27 22:50:50,906 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-27 22:50:50,907 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2026-01-27 22:50:52,111 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz:8443/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-27 22:50:52,113 - app.api.v1.agent - INFO - [Chat Stream] Mode: planning
2026-01-27 22:50:52,115 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:55028 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2026-01-27 22:50:52,122 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 输出至少14条原文证据，覆盖以下主题：

  1. 系统打卡事件/奖励/人皇幡出现（至少3条）
  ...
2026-01-27 22:50:52,129 - app.api.v1.agent - INFO - [agent_chat_stream] 📚 世界观数据已注入: 人物=8, 地点=7, 设定=7, 规范=无
2026-01-27 22:50:52,129 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21:724d1d83-9fd8-437f-99c8-ed96a7d78660 (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, conversation_id=724d1d83-9fd8-437f-99c8-ed96a7d78660)
2026-01-27 22:50:52,132 - app.services.context.manager - INFO - [ContextManager] 创建新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21:724d1d83-9fd8-437f-99c8-ed96a7d78660
2026-01-27 22:50:52,133 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21:724d1d83-9fd8-437f-99c8-ed96a7d78660: 0/16000 tokens
2026-01-27 22:50:52,203 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='输出至少14条原文证据，覆盖以下主题：

  1. 系统打卡...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=3条
2026-01-27 22:50:52,204 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21 | 含用户级=True | 找到=3条
2026-01-27 22:50:52,211 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 1条消息, 0 tokens, 耗时 81.90ms
2026-01-27 22:50:52,211 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 1 条历史消息 (token: 0, has_summary: False)
2026-01-27 22:50:52,211 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:50:52,213 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:50:52,213 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=200, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-27 22:50:53,489 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:50:53,489 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:50:53,503 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:50:53,508 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=539, cost=$0.000059, time=1276ms
2026-01-27 22:50:53,508 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=39, 尝试次数=1
2026-01-27 22:50:53,508 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:50:53,508 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:50:53,511 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=20, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-27 22:50:54,732 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:50:54,732 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:50:54,738 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:50:54,740 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=466, cost=$0.000047, time=1221ms
2026-01-27 22:50:54,741 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=7, 尝试次数=1
2026-01-27 22:50:54,742 - app.services.agent.intent.classifier - INFO - [Intent] AI识别结果: writing
2026-01-27 22:50:54,742 - app.services.agent.langgraph_agent - INFO - [Planning] AI意图分类: writing (置信度: 0.90)
2026-01-27 22:50:54,743 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 输出至少14条原文证据，覆盖以下主题：

  1. 系统打卡事件/奖励/人皇幡出现（至少3条）
  ...
2026-01-27 22:50:54,753 - app.core.cache - INFO - ✅ 缓存命中: prompt:planning:v2.41.0:get_planning_static_prompt:fca6eb91156619d0
2026-01-27 22:50:54,760 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-27 22:50:54,761 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=story_planning, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: story_planning; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-01-27 22:50:54,761 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.3, task_type=TaskType.STORY_PLANNING
2026-01-27 22:51:06,820 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-27 22:51:11,373 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 10 个数据块，总长度: 1160
2026-01-27 22:51:11,373 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 21542 (prompt=20962, completion=580)
2026-01-27 22:51:11,373 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:51:11,373 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-27 22:51:11,383 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:51:11,383 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=21542, cost=$0.032003, time=16611ms
2026-01-27 22:51:11,383 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=21542
2026-01-27 22:51:11,383 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户需要从当前章节中提取至少14条原文证据，并按照5个指定的, 原料=需要读取当前章节的全部内容，以便进行全面, 处理=使用 explore_content 工
2026-01-27 22:51:11,383 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共1个任务
2026-01-27 22:51:11,385 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共1个任务，耗时: 16.64s
2026-01-27 22:51:11,385 - app.api.v1.agent - INFO - [Stream] Plan tasks: 1 items
2026-01-27 22:51:11,385 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2026-01-27 22:51:11,385 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2026-01-27 22:51:11,385 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2026-01-27 22:51:11,385 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] DAG 调度启用，任务数=1, 有依赖任务=0
2026-01-27 22:51:11,385 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1开始: 根据用户指定的五个主题，在当前章节中检索相关的原文证据。
2026-01-27 22:51:11,385 - app.api.v1.agent - INFO - [Stream] Task started: 根据用户指定的五个主题，在当前章节中检索相关的原文证据。 (icon=Wrench)
2026-01-27 22:51:11,385 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: explore_content
2026-01-27 22:51:11,385 - app.services.agent.tools.explore_tools - INFO - [explore_content] 开始: work_id=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, target=输出至少14条原文证据，覆盖以下主题：1. 系统打卡事件/奖励/人皇幡出现（至少3条） 2. 林仙被...
2026-01-27 22:51:11,385 - app.services.agent.tools.explore_tools - INFO - [explore_content] 规划传入关键词: ['系统打卡', '人皇幡', '林仙', '联姻', '桃花林', '黑烟', '鸿蒙紫气', '邪魔外道', '青帝帝心', '帝血']
2026-01-27 22:51:11,385 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 启用严格段落号模式
2026-01-27 22:51:11,385 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 任务禁止整章阅读
2026-01-27 22:51:11,385 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 开始探索 V5: work_id=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, target=输出至少14条原文证据，覆盖以下主题：1. 系统打卡事件/奖励/人皇幡出现（至少3条） 2. 林仙被...
2026-01-27 22:51:11,385 - app.services.chapter_service - INFO - [ChapterService] Querying chapters for work_id=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, type=<class 'uuid.UUID'>
2026-01-27 22:51:11,385 - app.services.chapter_service - INFO - [ChapterService] Found 77 chapters
2026-01-27 22:51:11,385 - app.services.chapter_service - INFO -   - Chapter: 第1章 【摆烂的宿主】, order=1
2026-01-27 22:51:11,385 - app.services.chapter_service - INFO -   - ... (75 more chapters)
2026-01-27 22:51:11,385 - app.services.chapter_service - INFO -   - Chapter: 第100章 【火域铸真器，两脉起冲突】, order=77
2026-01-27 22:51:11,417 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:51:11,417 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:51:11,417 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:51:13,131 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:51:13,131 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:51:13,143 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:51:13,147 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=607, cost=$0.000094, time=1714ms
2026-01-27 22:51:13,147 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=232, 尝试次数=1
2026-01-27 22:51:13,175 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['系统打卡']..., mode=any, range=None, hits=3
2026-01-27 22:51:13,176 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:51:13,176 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:51:13,176 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:51:14,335 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:51:14,335 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:51:14,344 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:51:14,345 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=793, cost=$0.000112, time=1158ms
2026-01-27 22:51:14,346 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=222, 尝试次数=1
2026-01-27 22:51:14,353 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['林仙', '联姻', '圣主']..., mode=any, range=None, hits=5
2026-01-27 22:51:14,356 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:51:14,356 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:51:14,356 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:51:15,683 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:51:15,684 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:51:15,694 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:51:15,695 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=834, cost=$0.000112, time=1329ms
2026-01-27 22:51:15,695 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=207, 尝试次数=1
2026-01-27 22:51:15,761 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['奖励', '人皇幡']..., mode=any, range=None, hits=3
2026-01-27 22:51:15,762 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:51:15,763 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:51:15,763 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:51:18,826 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:51:18,826 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:51:18,834 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:51:18,834 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1174, cost=$0.000255, time=3063ms
2026-01-27 22:51:18,834 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=1026, 尝试次数=1
2026-01-27 22:51:18,853 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第35段
2026-01-27 22:51:18,864 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第8章第51段
2026-01-27 22:51:18,869 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第8章第54段
2026-01-27 22:51:18,879 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第10章第10段
2026-01-27 22:51:18,888 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第10章第12段
2026-01-27 22:51:18,892 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第10章第14段
2026-01-27 22:51:18,898 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第11章第1段
2026-01-27 22:51:18,903 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第11章第3段
2026-01-27 22:51:18,905 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第11章第5段
2026-01-27 22:51:18,913 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第12章第1段
2026-01-27 22:51:18,915 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第12章第3段
2026-01-27 22:51:18,923 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第12章第5段
2026-01-27 22:51:18,928 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第13章第1段
2026-01-27 22:51:18,932 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第13章第3段
2026-01-27 22:51:18,934 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:51:18,935 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:51:18,935 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:51:21,987 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:51:21,987 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:51:22,002 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:51:22,002 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1685, cost=$0.000317, time=3052ms
2026-01-27 22:51:22,005 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=1065, 尝试次数=1
2026-01-27 22:51:22,008 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第35段
2026-01-27 22:51:22,015 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第8章第51段
2026-01-27 22:51:22,019 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第10章第11段
2026-01-27 22:51:22,030 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第11章第17段
2026-01-27 22:51:22,031 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第11章第20段
2026-01-27 22:51:22,040 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第11章第23段
2026-01-27 22:51:22,047 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第12章第10段
2026-01-27 22:51:22,050 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第12章第11段
2026-01-27 22:51:22,061 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第12章第12段
2026-01-27 22:51:22,063 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第13章第15段
2026-01-27 22:51:22,063 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第13章第16段
2026-01-27 22:51:22,071 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第13章第17段
2026-01-27 22:51:22,078 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第14章第25段
2026-01-27 22:51:22,081 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第14章第26段
2026-01-27 22:51:22,081 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:51:22,081 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:51:22,081 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:51:24,632 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:51:24,632 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:51:24,642 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:51:24,642 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1782, cost=$0.000356, time=2550ms
2026-01-27 22:51:24,642 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=1404, 尝试次数=1
2026-01-27 22:51:24,653 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第35段
2026-01-27 22:51:24,653 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第8章第51段
2026-01-27 22:51:24,663 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第11章第10段
2026-01-27 22:51:24,667 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第12章第15段
2026-01-27 22:51:24,669 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第12章第20段
2026-01-27 22:51:24,674 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第12章第25段
2026-01-27 22:51:24,680 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第13章第5段
2026-01-27 22:51:24,684 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第13章第10段
2026-01-27 22:51:24,692 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第13章第15段
2026-01-27 22:51:24,696 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第15章第30段
2026-01-27 22:51:24,701 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第15章第35段
2026-01-27 22:51:24,705 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第15章第40段
2026-01-27 22:51:24,710 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第16章第5段
2026-01-27 22:51:24,715 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第16章第10段
2026-01-27 22:51:24,716 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:51:24,717 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:51:24,717 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:51:26,343 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:51:26,343 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:51:26,355 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:51:26,355 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1420, cost=$0.000211, time=1629ms
2026-01-27 22:51:26,355 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=461, 尝试次数=1
2026-01-27 22:51:26,383 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['青帝', '帝心', '帝血']..., mode=any, range=None, hits=10
2026-01-27 22:51:26,383 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:51:26,383 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:51:26,383 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:51:28,356 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:51:28,356 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:51:28,371 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:51:28,371 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1162, cost=$0.000208, time=1973ms
2026-01-27 22:51:28,372 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=553, 尝试次数=1
2026-01-27 22:51:28,394 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['我背后是青帝']..., mode=any, range=None, hits=4
2026-01-27 22:51:28,394 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:51:28,394 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:51:28,394 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:51:29,574 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:51:29,574 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:51:29,588 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:51:29,588 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=836, cost=$0.000118, time=1179ms
2026-01-27 22:51:29,588 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=244, 尝试次数=1
2026-01-27 22:51:29,645 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['系统打卡', '奖励', '人皇幡']..., mode=any, range=None, hits=43
2026-01-27 22:51:29,657 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:51:29,657 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:51:29,657 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:51:31,836 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:51:31,837 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:51:31,852 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:51:31,853 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1295, cost=$0.000262, time=2179ms
2026-01-27 22:51:31,853 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=1208, 尝试次数=1
2026-01-27 22:51:31,856 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第10段
2026-01-27 22:51:31,856 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第11段
2026-01-27 22:51:31,869 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第12段
2026-01-27 22:51:31,877 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第5段
2026-01-27 22:51:31,882 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第6段
2026-01-27 22:51:31,887 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第7段
2026-01-27 22:51:31,887 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第1段
2026-01-27 22:51:31,887 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第2段
2026-01-27 22:51:31,901 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第3段
2026-01-27 22:51:31,901 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第4章第15段
2026-01-27 22:51:31,908 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第4章第16段
2026-01-27 22:51:31,915 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第5章第20段
2026-01-27 22:51:31,919 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第5章第21段
2026-01-27 22:51:31,919 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第5章第22段
2026-01-27 22:51:31,919 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:51:31,919 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:51:31,919 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:51:37,258 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:51:37,258 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:51:37,265 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:51:37,265 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2221, cost=$0.000524, time=5339ms
2026-01-27 22:51:37,265 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=1817, 尝试次数=1
2026-01-27 22:51:37,265 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:51:37,265 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:51:37,265 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:51:38,485 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:51:38,485 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:51:38,499 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:51:38,502 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=686, cost=$0.000104, time=1222ms
2026-01-27 22:51:38,502 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=254, 尝试次数=1
2026-01-27 22:51:38,523 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['青帝帝心']..., mode=any, range=None, hits=0
2026-01-27 22:51:38,523 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:51:38,526 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:51:38,526 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:51:39,899 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:51:39,900 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:51:39,908 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:51:39,909 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=705, cost=$0.000109, time=1374ms
2026-01-27 22:51:39,909 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=265, 尝试次数=1
2026-01-27 22:51:39,962 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['系统打卡', '奖励', '人皇幡']..., mode=any, range=None, hits=5
2026-01-27 22:51:39,962 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 22:51:39,962 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 22:51:39,962 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 22:51:41,514 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:51:41,515 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 22:51:41,521 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:51:41,523 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1055, cost=$0.000167, time=1554ms
2026-01-27 22:51:41,523 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=487, 尝试次数=1
2026-01-27 22:51:41,525 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第1段
2026-01-27 22:51:41,532 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第2段
2026-01-27 22:51:41,535 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第3段
2026-01-27 22:51:41,542 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第4段
2026-01-27 22:51:41,545 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 探索完成(工具循环): 14轮, 原因=达到读取上限
2026-01-27 22:51:41,547 - app.services.agent.execution.tool_executor - INFO - [StandardTool] explore_content 执行成功
2026-01-27 22:51:41,547 - app.api.v1.agent - INFO - [Stream] 任务完成: 根据用户指定的五个主题，在当前章节中检索相关的原文证据。 (30.2s)
2026-01-27 22:51:41,547 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1完成
2026-01-27 22:51:41,547 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共1个任务，耗时: 30.16s
2026-01-27 22:51:41,547 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2026-01-27 22:51:41,547 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=1, 展示型=0
2026-01-27 22:51:41,547 - app.services.agent.langgraph_agent - INFO - [Response] 单个输出任务(explore_content)，使用AI整合
2026-01-27 22:51:41,547 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2026-01-27 22:51:41,547 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=1, 展示型=0
2026-01-27 22:51:41,547 - app.services.agent.utils.context_builder - INFO - [Compress] 任务1工具'explore_content'，内容长度35340，保留20000字符（省略15340字符）
2026-01-27 22:51:41,547 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=35609字符, 处理后=278字符
2026-01-27 22:51:41,547 - app.services.agent.planning.response_builder - INFO - [Summarization] 准备发送 summarization_start 事件
2026-01-27 22:51:41,547 - app.services.agent.stream.stream_event_handler - INFO - [StreamEventHandler] emit_summarization_start 被调用, _on_flow_event=True
2026-01-27 22:51:41,547 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_start 事件已发送
2026-01-27 22:51:41,547 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2026-01-27 22:51:41,547 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2026-01-27 22:51:41,552 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-27 22:51:41,552 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-27 22:51:41,552 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
2026-01-27 22:52:14,309 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-27 22:52:14,309 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_complete 事件已发送（第一个chunk时）
2026-01-27 22:52:14,309 - app.services.agent.planning.response_builder - INFO - [Summarization] output_ready 事件已发送（第一个chunk时）
2026-01-27 22:52:16,439 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 10 个数据块，总长度: 877
2026-01-27 22:52:16,440 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 19449 (prompt=18830, completion=619)
2026-01-27 22:52:16,441 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 22:52:16,441 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-27 22:52:16,459 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 22:52:16,459 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=19449, cost=$0.007196, time=34885ms
2026-01-27 22:52:16,459 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=877
2026-01-27 22:52:16,747 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21 | 重要度=0.84
2026-01-27 22:52:17,036 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21 | 重要度=0.60
2026-01-27 22:52:17,044 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21:724d1d83-9fd8-437f-99c8-ed96a7d78660, token=1192
2026-01-27 22:52:17,044 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21:724d1d83-9fd8-437f-99c8-ed96a7d78660, 消息数=2, 摘要长度=0, Token=1192
2026-01-27 22:52:17,044 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21:724d1d83-9fd8-437f-99c8-ed96a7d78660)
2026-01-27 22:52:17,045 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2026-01-27 22:52:17,050 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed
2026-01-27 22:52:29,020 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/724d1d83-9fd8-437f-99c8-ed96a7d78660
INFO:     127.0.0.1:58435 - "GET /api/v1/agent/operations/724d1d83-9fd8-437f-99c8-ed96a7d78660 HTTP/1.1" 200 OK
2026-01-27 22:53:20,695 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, chapter_id: fca581f0-3bce-457a-830f-00efaf22ab8c
2026-01-27 22:53:20,704 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: fca581f0-3bce-457a-830f-00efaf22ab8c
2026-01-27 22:53:20,705 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: 5452e126-99a7-4323-8e8c-c3ea9b6f8774
2026-01-27 22:53:20,706 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-27 22:53:20,707 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:58059 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-27 22:53:20,721 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, chapter_id: fca581f0-3bce-457a-830f-00efaf22ab8c
2026-01-27 22:53:20,729 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: fca581f0-3bce-457a-830f-00efaf22ab8c
2026-01-27 22:53:20,735 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: 5452e126-99a7-4323-8e8c-c3ea9b6f8774
2026-01-27 22:53:20,736 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-27 22:53:20,736 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/fca581f0-3bce-457a-830f-00efaf22ab8c/revisions
2026-01-27 22:53:20,736 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:54923 - "GET /api/v1/chapters/fca581f0-3bce-457a-830f-00efaf22ab8c/revisions?status=pending HTTP/1.1" 200 OK
INFO:     127.0.0.1:54921 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-27 22:53:20,792 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/fca581f0-3bce-457a-830f-00efaf22ab8c/revisions
INFO:     127.0.0.1:53341 - "GET /api/v1/chapters/fca581f0-3bce-457a-830f-00efaf22ab8c/revisions?status=pending HTTP/1.1" 200 OK
2026-01-27 22:53:20,906 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/82287b9a-2e06-4364-a8f9-303b2bb87d01
INFO:     127.0.0.1:56626 - "GET /api/v1/agent/operations/82287b9a-2e06-4364-a8f9-303b2bb87d01 HTTP/1.1" 200 OK
2026-01-27 22:53:20,925 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/82287b9a-2e06-4364-a8f9-303b2bb87d01
INFO:     127.0.0.1:60165 - "GET /api/v1/agent/operations/82287b9a-2e06-4364-a8f9-303b2bb87d01 HTTP/1.1" 200 OK
2026-01-27 22:53:21,015 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21
2026-01-27 22:53:21,020 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/fca581f0-3bce-457a-830f-00efaf22ab8c
INFO:     127.0.0.1:56625 - "PUT /api/v1/chapters/fca581f0-3bce-457a-830f-00efaf22ab8c HTTP/1.1" 200 OK
2026-01-27 22:53:21,026 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第25章 【汝从无生来，要往长生去】 (order=20)
2026-01-27 22:53:22,972 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第25章 【汝从无生来，要往长生去】 (61 paragraphs)
2026-01-27 22:53:22,994 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21
2026-01-27 22:53:22,996 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/fca581f0-3bce-457a-830f-00efaf22ab8c
INFO:     127.0.0.1:64263 - "PUT /api/v1/chapters/fca581f0-3bce-457a-830f-00efaf22ab8c HTTP/1.1" 200 OK
2026-01-27 22:53:22,998 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第25章 【汝从无生来，要往长生去】 (order=20)
2026-01-27 22:53:25,032 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第25章 【汝从无生来，要往长生去】 (61 paragraphs)
2026-01-27 22:53:48,621 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, chapter_id: 8e5ced71-2612-46cd-8234-93f404cf5910
2026-01-27 22:53:48,629 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 8e5ced71-2612-46cd-8234-93f404cf5910
2026-01-27 22:53:48,631 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: b0d975d4-7759-4ea0-8486-666c15fbfd07
2026-01-27 22:53:48,631 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-27 22:53:48,633 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:56288 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-27 22:53:48,653 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, chapter_id: 8e5ced71-2612-46cd-8234-93f404cf5910
2026-01-27 22:53:48,658 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 8e5ced71-2612-46cd-8234-93f404cf5910
2026-01-27 22:53:48,662 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: b0d975d4-7759-4ea0-8486-666c15fbfd07
2026-01-27 22:53:48,662 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-27 22:53:48,668 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:63816 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-27 22:53:48,690 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/8e5ced71-2612-46cd-8234-93f404cf5910/revisions
INFO:     127.0.0.1:63817 - "GET /api/v1/chapters/8e5ced71-2612-46cd-8234-93f404cf5910/revisions?status=pending HTTP/1.1" 200 OK
2026-01-27 22:53:48,713 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/8e5ced71-2612-46cd-8234-93f404cf5910/revisions
INFO:     127.0.0.1:52723 - "GET /api/v1/chapters/8e5ced71-2612-46cd-8234-93f404cf5910/revisions?status=pending HTTP/1.1" 200 OK
2026-01-27 22:53:48,854 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/f572379b-fd47-4986-9833-0e1aa63a6308
INFO:     127.0.0.1:65323 - "GET /api/v1/agent/operations/f572379b-fd47-4986-9833-0e1aa63a6308 HTTP/1.1" 200 OK
2026-01-27 22:53:48,933 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/f572379b-fd47-4986-9833-0e1aa63a6308
INFO:     127.0.0.1:51951 - "GET /api/v1/agent/operations/f572379b-fd47-4986-9833-0e1aa63a6308 HTTP/1.1" 200 OK
2026-01-27 22:53:48,994 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21
2026-01-27 22:53:48,999 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/8e5ced71-2612-46cd-8234-93f404cf5910
INFO:     127.0.0.1:65322 - "PUT /api/v1/chapters/8e5ced71-2612-46cd-8234-93f404cf5910 HTTP/1.1" 200 OK
2026-01-27 22:53:49,003 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第59章 上架感言：萌新求订阅 (order=50)
2026-01-27 22:53:53,001 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第59章 上架感言：萌新求订阅 (144 paragraphs)
2026-01-27 22:53:53,057 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21
2026-01-27 22:53:53,059 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/8e5ced71-2612-46cd-8234-93f404cf5910
INFO:     127.0.0.1:64275 - "PUT /api/v1/chapters/8e5ced71-2612-46cd-8234-93f404cf5910 HTTP/1.1" 200 OK
2026-01-27 22:53:53,062 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第59章 上架感言：萌新求订阅 (order=50)
2026-01-27 22:53:57,612 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第59章 上架感言：萌新求订阅 (144 paragraphs)
2026-01-27 22:54:09,896 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, chapter_id: 9e73c137-ec1f-4346-b911-993eaaf0b14e
2026-01-27 22:54:09,905 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 9e73c137-ec1f-4346-b911-993eaaf0b14e
2026-01-27 22:54:09,907 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: e2767773-00d9-478e-92df-ecf810ed3847
2026-01-27 22:54:09,907 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-27 22:54:09,909 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:56531 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-27 22:54:09,919 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, chapter_id: 9e73c137-ec1f-4346-b911-993eaaf0b14e
2026-01-27 22:54:09,932 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 9e73c137-ec1f-4346-b911-993eaaf0b14e
2026-01-27 22:54:09,933 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: e2767773-00d9-478e-92df-ecf810ed3847
2026-01-27 22:54:09,933 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-27 22:54:09,935 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:50292 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-27 22:54:09,944 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/9e73c137-ec1f-4346-b911-993eaaf0b14e/revisions
INFO:     127.0.0.1:50293 - "GET /api/v1/chapters/9e73c137-ec1f-4346-b911-993eaaf0b14e/revisions?status=pending HTTP/1.1" 200 OK
2026-01-27 22:54:09,964 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/9e73c137-ec1f-4346-b911-993eaaf0b14e/revisions
INFO:     127.0.0.1:64240 - "GET /api/v1/chapters/9e73c137-ec1f-4346-b911-993eaaf0b14e/revisions?status=pending HTTP/1.1" 200 OK
2026-01-27 22:54:10,087 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/540c4675-a4d4-422f-aa79-3dbb0722234b
INFO:     127.0.0.1:52563 - "GET /api/v1/agent/operations/540c4675-a4d4-422f-aa79-3dbb0722234b HTTP/1.1" 200 OK
2026-01-27 22:54:10,123 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/540c4675-a4d4-422f-aa79-3dbb0722234b
INFO:     127.0.0.1:62752 - "GET /api/v1/agent/operations/540c4675-a4d4-422f-aa79-3dbb0722234b HTTP/1.1" 200 OK
2026-01-27 22:54:10,162 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21
2026-01-27 22:54:10,168 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/9e73c137-ec1f-4346-b911-993eaaf0b14e
INFO:     127.0.0.1:52562 - "PUT /api/v1/chapters/9e73c137-ec1f-4346-b911-993eaaf0b14e HTTP/1.1" 200 OK
2026-01-27 22:54:10,174 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第79章 【大不了打沉东荒！】 (order=60)
2026-01-27 22:54:12,410 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第79章 【大不了打沉东荒！】 (88 paragraphs)
2026-01-27 22:54:12,461 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21
2026-01-27 22:54:12,465 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/9e73c137-ec1f-4346-b911-993eaaf0b14e
INFO:     127.0.0.1:60346 - "PUT /api/v1/chapters/9e73c137-ec1f-4346-b911-993eaaf0b14e HTTP/1.1" 200 OK
2026-01-27 22:54:12,466 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第79章 【大不了打沉东荒！】 (order=60)
2026-01-27 22:54:15,345 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第79章 【大不了打沉东荒！】 (88 paragraphs)
2026-01-27 22:54:35,291 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, chapter_id: 1b7962cc-0889-4258-be51-c09cbec173cf
2026-01-27 22:54:35,296 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 1b7962cc-0889-4258-be51-c09cbec173cf
2026-01-27 22:54:35,298 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: cd91f2ba-36b8-4ed0-b1fb-276153b44430
2026-01-27 22:54:35,298 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-27 22:54:35,301 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:53026 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-27 22:54:35,317 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, chapter_id: 1b7962cc-0889-4258-be51-c09cbec173cf
2026-01-27 22:54:35,328 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 1b7962cc-0889-4258-be51-c09cbec173cf
2026-01-27 22:54:35,330 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: cd91f2ba-36b8-4ed0-b1fb-276153b44430
2026-01-27 22:54:35,330 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-27 22:54:35,332 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/1b7962cc-0889-4258-be51-c09cbec173cf/revisions
2026-01-27 22:54:35,332 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:52172 - "GET /api/v1/chapters/1b7962cc-0889-4258-be51-c09cbec173cf/revisions?status=pending HTTP/1.1" 200 OK
INFO:     127.0.0.1:52170 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-27 22:54:35,351 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/1b7962cc-0889-4258-be51-c09cbec173cf/revisions
INFO:     127.0.0.1:62180 - "GET /api/v1/chapters/1b7962cc-0889-4258-be51-c09cbec173cf/revisions?status=pending HTTP/1.1" 200 OK
2026-01-27 22:54:35,492 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/724d1d83-9fd8-437f-99c8-ed96a7d78660
INFO:     127.0.0.1:58541 - "GET /api/v1/agent/operations/724d1d83-9fd8-437f-99c8-ed96a7d78660 HTTP/1.1" 200 OK
2026-01-27 22:54:35,536 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/724d1d83-9fd8-437f-99c8-ed96a7d78660
INFO:     127.0.0.1:53435 - "GET /api/v1/agent/operations/724d1d83-9fd8-437f-99c8-ed96a7d78660 HTTP/1.1" 200 OK
2026-01-27 22:54:35,602 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21
2026-01-27 22:54:35,609 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/1b7962cc-0889-4258-be51-c09cbec173cf
INFO:     127.0.0.1:58542 - "PUT /api/v1/chapters/1b7962cc-0889-4258-be51-c09cbec173cf HTTP/1.1" 200 OK
2026-01-27 22:54:35,614 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第96章 【我才是狠人道主！】 (order=73)
2026-01-27 22:54:38,041 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第96章 【我才是狠人道主！】 (78 paragraphs)
2026-01-27 22:54:38,104 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21
2026-01-27 22:54:38,106 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/1b7962cc-0889-4258-be51-c09cbec173cf
INFO:     127.0.0.1:55899 - "PUT /api/v1/chapters/1b7962cc-0889-4258-be51-c09cbec173cf HTTP/1.1" 200 OK
2026-01-27 22:54:38,108 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第96章 【我才是狠人道主！】 (order=73)
2026-01-27 22:54:40,442 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第96章 【我才是狠人道主！】 (78 paragraphs)
2026-01-27 22:54:53,157 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, chapter_id: b5647e1f-7829-4935-9d16-b4003691b4ad
2026-01-27 22:54:53,163 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: b5647e1f-7829-4935-9d16-b4003691b4ad
2026-01-27 22:54:53,169 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: ef242054-b4b9-467d-8974-a7320bd04cab
2026-01-27 22:54:53,170 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-27 22:54:53,174 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:64529 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-27 22:54:53,185 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, chapter_id: b5647e1f-7829-4935-9d16-b4003691b4ad
2026-01-27 22:54:53,196 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: b5647e1f-7829-4935-9d16-b4003691b4ad
2026-01-27 22:54:53,197 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/b5647e1f-7829-4935-9d16-b4003691b4ad/revisions
2026-01-27 22:54:53,198 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: ef242054-b4b9-467d-8974-a7320bd04cab
2026-01-27 22:54:53,199 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
INFO:     127.0.0.1:50102 - "GET /api/v1/chapters/b5647e1f-7829-4935-9d16-b4003691b4ad/revisions?status=pending HTTP/1.1" 200 OK
2026-01-27 22:54:53,204 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:50101 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-27 22:54:53,226 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/b5647e1f-7829-4935-9d16-b4003691b4ad/revisions
INFO:     127.0.0.1:59853 - "GET /api/v1/chapters/b5647e1f-7829-4935-9d16-b4003691b4ad/revisions?status=pending HTTP/1.1" 200 OK
2026-01-27 22:54:53,535 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/f93a223f-2a65-40c0-9b49-97572d6c030b
2026-01-27 22:54:53,536 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/c2dc4281-b25c-49db-aa15-963f19d6cc7a
2026-01-27 22:54:53,537 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/fbfb1a7c-8003-4fcb-b54d-61a936b1ee6b
INFO:     127.0.0.1:57720 - "GET /api/v1/agent/operations/f93a223f-2a65-40c0-9b49-97572d6c030b HTTP/1.1" 200 OK
2026-01-27 22:54:53,539 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/c2f843f2-f06e-4e46-9f63-2b862f35b786
INFO:     127.0.0.1:57722 - "GET /api/v1/agent/operations/c2dc4281-b25c-49db-aa15-963f19d6cc7a HTTP/1.1" 200 OK
INFO:     127.0.0.1:57723 - "GET /api/v1/agent/operations/fbfb1a7c-8003-4fcb-b54d-61a936b1ee6b HTTP/1.1" 200 OK
INFO:     127.0.0.1:57721 - "GET /api/v1/agent/operations/c2f843f2-f06e-4e46-9f63-2b862f35b786 HTTP/1.1" 200 OK
2026-01-27 22:54:53,611 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/f93a223f-2a65-40c0-9b49-97572d6c030b
2026-01-27 22:54:53,632 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/fbfb1a7c-8003-4fcb-b54d-61a936b1ee6b
2026-01-27 22:54:53,634 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/c2dc4281-b25c-49db-aa15-963f19d6cc7a
INFO:     127.0.0.1:50081 - "GET /api/v1/agent/operations/f93a223f-2a65-40c0-9b49-97572d6c030b HTTP/1.1" 200 OK
2026-01-27 22:54:53,650 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/c2f843f2-f06e-4e46-9f63-2b862f35b786
INFO:     127.0.0.1:54283 - "GET /api/v1/agent/operations/fbfb1a7c-8003-4fcb-b54d-61a936b1ee6b HTTP/1.1" 200 OK
INFO:     127.0.0.1:54282 - "GET /api/v1/agent/operations/c2dc4281-b25c-49db-aa15-963f19d6cc7a HTTP/1.1" 200 OK
INFO:     127.0.0.1:54285 - "GET /api/v1/agent/operations/c2f843f2-f06e-4e46-9f63-2b862f35b786 HTTP/1.1" 200 OK
2026-01-27 22:54:53,721 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21
2026-01-27 22:54:53,725 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/b5647e1f-7829-4935-9d16-b4003691b4ad
INFO:     127.0.0.1:57725 - "PUT /api/v1/chapters/b5647e1f-7829-4935-9d16-b4003691b4ad HTTP/1.1" 200 OK
2026-01-27 22:54:53,726 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第100章 【火域铸真器，两脉起冲突】 (order=77)
2026-01-27 22:54:55,722 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第100章 【火域铸真器，两脉起冲突】 (59 paragraphs)
2026-01-27 22:54:55,767 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21
2026-01-27 22:54:55,768 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/b5647e1f-7829-4935-9d16-b4003691b4ad
INFO:     127.0.0.1:62862 - "PUT /api/v1/chapters/b5647e1f-7829-4935-9d16-b4003691b4ad HTTP/1.1" 200 OK
2026-01-27 22:54:55,769 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第100章 【火域铸真器，两脉起冲突】 (order=77)
2026-01-27 22:54:57,880 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第100章 【火域铸真器，两脉起冲突】 (59 paragraphs)