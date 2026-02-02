INFO:     127.0.0.1:54361 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2026-02-03 01:34:49,617 - app.core.redis - INFO - ✅ Redis connected: redis://localhost:6379/0
2026-02-03 01:34:49,624 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 请仅根据【测试文本1】写一段 300-500 字的场景描写：时间为考核前的某个傍晚，段融完成马坊杂活...
2026-02-03 01:34:49,629 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-02-03 01:34:49,629 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-02-03 01:34:49,629 - app.services.ai.http_ai_service - INFO - [成本追踪] 初始化未传db/user_id，将使用请求上下文按需记录成本
2026-02-03 01:34:50,647 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz:8443/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-02-03 01:34:50,647 - app.services.agent.tools.writing_tools - INFO - Writing tools AI service initialized
2026-02-03 01:34:50,652 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ AI Service 已同时设置到 langgraph_tools 和 writing_tools
2026-02-03 01:34:50,652 - app.services.context.adaptive_budget - INFO - ✅ 所有预算配置验证通过
2026-02-03 01:34:56,618 - app.services.context.vector_memory_store - INFO - ✅ VectorMemoryStore初始化成功 | 目录=./data/chroma_db | 模型=paraphrase-multilingual-MiniLM-L12-v2 | 集合=user_memories
2026-02-03 01:34:56,618 - app.services.context.manager - INFO - ✅ VectorMemoryStore 已初始化
2026-02-03 01:34:56,618 - app.services.context.manager - INFO - ✅ ContextManager: 长期记忆已启用 (user_id=None)
2026-02-03 01:34:56,618 - app.services.context.manager - INFO - ✅ ContextManager: 自适应预算已启用
2026-02-03 01:34:56,618 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ ContextManager已初始化（长期记忆已启用，自适应预算已启用，总预算=16000 tokens）
成功加载模板: analyze_text (版本 3.1.0)
成功加载模板: writing_agent (版本 2.0.0)
成功加载模板: system_agent_prompt (版本 2.1.0)
成功加载模板: creative_writing_prompt (版本 1.0.0)
2026-02-03 01:34:56,681 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ PromptManager已初始化
2026-02-03 01:34:56,688 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ Redis连接验证成功
2026-02-03 01:34:56,688 - app.services.agent.langgraph_agent - INFO - [LangGraph] OK 使用 AsyncRedisSaver（redis://localhost:6379/0，TTL=7天）
2026-02-03 01:34:56,689 - app.services.agent.memory.metrics - INFO - [MemoryMetrics] 监控系统已初始化
2026-02-03 01:34:56,689 - app.services.agent.memory.long_term_store - INFO - [LongTermStore] Initialized: base_dir=./data/long_term_memory, max_size=50KB, compression=True
2026-02-03 01:34:56,689 - app.services.agent.memory.enhanced_memory_manager - INFO - EnhancedMemoryManager initialized: short=10, medium=100, threshold=0.1, long_term_backup=enabled
2026-02-03 01:34:56,689 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ EnhancedMemoryManager已创建
2026-02-03 01:34:56,690 - app.services.agent.memory.unified_coordinator - INFO - [UnifiedMemoryCoordinator] 初始化统一记忆协调器
2026-02-03 01:34:56,690 - app.services.agent.memory.unified_coordinator - INFO - [UnifiedMemoryCoordinator] 全局实例已设置
2026-02-03 01:34:56,691 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ UnifiedMemoryCoordinator已初始化 | checkpointer=AsyncRedisSaver | enhanced_memory=yes | context_manager=yes
2026-02-03 01:34:56,691 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ 解耦模块已初始化 (IntentClassifier, ToolExecutor, EventParser, ResponseBuilder, ToolDispatcher, ParallelExecutor, PlanGenerator, QuickPathHandler, StreamEventHandler, SecondaryToolHandler, TaskRunner, AgentExecutor)
2026-02-03 01:34:56,696 - app.services.agent.parallel_tool_node - INFO - [ParallelToolNode] 初始化完成，最大并发数=5，并行安全工具=6个
2026-02-03 01:34:56,721 - app.api.v1.agent - INFO - [Global Agent] created global agent instance; MemorySaver shared across requests
2026-02-03 01:34:56,721 - app.services.knowledge_service - INFO - 语义搜索知识库: user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, query=请仅根据【测试文本1】写一段 300-500 字的场景描写：时间为考核前的某个傍晚，段融完成马坊杂活后去院子练功。必须出现：赵穆、羚羊献食、浑圆桩、孔斌/李充/张征、吞噬器灵、牛尾刀。禁止新增设定或角色，不要改写成现代语气。
2026-02-03 01:34:56,721 - app.services.vector_store_service - INFO - 知识库RAG检索: user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, query=请仅根据【测试文本1】写一段 300-500 字的场景描写：时间为考核前的某个傍晚，段融完成马坊杂活..., doc_ids=1
2026-02-03 01:34:56,957 - app.services.vector_store_service - INFO - 检索到 2 个相关知识条目（阈值=0.3）
2026-02-03 01:34:56,979 - app.services.knowledge_service - INFO - 语义搜索完成: 返回1个结果
2026-02-03 01:34:56,989 - app.services.knowledge_service - INFO - 引用次数增加: item_id=e68ae11f-dec0-401f-89bf-49ea94c94920, count=3
2026-02-03 01:34:56,989 - app.api.v1.agent - INFO - [agent_chat_stream] Injected 1 knowledge docs into context
2026-02-03 01:34:57,010 - app.api.v1.agent - INFO - [agent_chat_stream] 📚 世界观数据已注入: 人物=11, 地点=10, 设定=6, 规范=无
2026-02-03 01:34:57,012 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:58a111d4-1083-4fd9-b907-723b605e3481:5283ef8e-8f5f-44c9-8b09-752a59864dc5 (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=58a111d4-1083-4fd9-b907-723b605e3481, conversation_id=5283ef8e-8f5f-44c9-8b09-752a59864dc5)
2026-02-03 01:34:57,012 - app.services.context.monitoring_integration - INFO - ✅ ContextManager监控收集器已初始化
2026-02-03 01:34:57,012 - app.services.context.store - INFO - [ContextStore] Redis连接成功
2026-02-03 01:34:57,024 - app.services.context.manager - INFO - [ContextManager] 创建新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:58a111d4-1083-4fd9-b907-723b605e3481:5283ef8e-8f5f-44c9-8b09-752a59864dc5
2026-02-03 01:34:57,192 - app.services.context.token_counter - INFO - ✅ tiktoken初始化成功，模型: gemini-2.5-pro -> cl100k_base
2026-02-03 01:34:57,192 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:58a111d4-1083-4fd9-b907-723b605e3481:5283ef8e-8f5f-44c9-8b09-752a59864dc5: 0/16000 tokens
2026-02-03 01:34:57,903 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='请仅根据【测试文本1】写一段 300-500 字的场景描写：...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:58a111d4-1083-4fd9-b907-723b605e3481', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=3条
2026-02-03 01:34:57,903 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=58a111d4-1083-4fd9-b907-723b605e3481 | 含用户级=True | 找到=3条
2026-02-03 01:34:57,965 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 1条消息, 0 tokens, 耗时 953.71ms
2026-02-03 01:34:57,965 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 1 条历史消息 (token: 0, has_summary: False)
2026-02-03 01:34:57,965 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-02-03 01:34:57,965 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-02-03 01:35:00,957 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-02-03 01:35:00,961 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-02-03 01:35:02,035 - app.services.agent.intent.classifier - INFO - [Intent] AI识别结果: writing
2026-02-03 01:35:02,035 - app.services.agent.langgraph_agent - INFO - [Planning] AI意图分类: writing (置信度: 0.90)
2026-02-03 01:35:02,035 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 请仅根据【测试文本1】写一段 300-500 字的场景描写：时间为考核前的某个傍晚，段融完成马坊杂活...
2026-02-03 01:35:02,053 - app.services.agent.planning.plan_generator - INFO - [Planning] 注入 1 个知识库文档到prompt
2026-02-03 01:35:02,058 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-02-03 01:35:02,058 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=story_planning, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: story_planning; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-02-03 01:35:36,137 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=23819
2026-02-03 01:35:36,139 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户需要一段300-500字的场景描写，这是一个创作类请求。, 原料=需要的原料包括：用户提供的【测试文本1】, 处理=这是一个非常具体的创作请求，可以直接执行
2026-02-03 01:35:36,166 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共1个任务
2026-02-03 01:35:36,168 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共1个任务，耗时: 34.13s
2026-02-03 01:35:36,169 - app.api.v1.agent - INFO - [Stream] Plan tasks: 1 items
2026-02-03 01:35:36,169 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2026-02-03 01:35:36,171 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2026-02-03 01:35:36,171 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2026-02-03 01:35:36,172 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] DAG 调度启用，任务数=1, 有依赖任务=0
2026-02-03 01:35:36,173 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1开始: 根据用户提供的知识库文档和详细要求，创作一段300-500字的场景描写。
2026-02-03 01:35:36,173 - app.api.v1.agent - INFO - [Stream] Task started: 根据用户提供的知识库文档和详细要求，创作一段300-500字的场景描写。 (icon=PenTool)
2026-02-03 01:35:36,174 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 ToolExecutor(smart_continue)
2026-02-03 01:35:36,175 - app.services.agent.execution.tool_executor - INFO - [ToolExecutor] smart_continue chapter_id 来源=explicit value=ec40b80d-0764-482e-96a3-e5923496d4b0
2026-02-03 01:35:36,175 - app.services.agent.tools.tool_types - INFO - [smart_continue] 开始执行工具
2026-02-03 01:35:36,177 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-02-03 01:35:36,177 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-02-03 01:35:36,181 - app.services.ai.http_ai_service - INFO - [成本追踪] 初始化未传db/user_id，将使用请求上下文按需记录成本
2026-02-03 01:35:36,892 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz:8443/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
D:\Java\ai_writer\backend\app\utils\text_cleaner.py:96: MarkupResemblesLocatorWarning: The input looks more like a filename than markup. You may want to open this file and pass the filehandle into Beautiful Soup.
  soup = BeautifulSoup(html_content, 'html.parser')
2026-02-03 01:35:36,897 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-02-03 01:35:36,898 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=content_creation, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro
2026-02-03 01:36:07,171 - app.services.agent.tools.tool_types - INFO - [smart_continue] 执行成功 (耗时: 30.996s)
2026-02-03 01:36:07,171 - app.services.agent.tools.tool_monitor - INFO - ToolMonitor initialized with Memory storage, retention: 7 days
2026-02-03 01:36:07,176 - app.services.agent.execution.tool_executor - INFO - [StandardTool] smart_continue 执行成功
2026-02-03 01:36:07,176 - app.services.agent.execution.task_runner - INFO - [TaskRunner] smart_continue 执行成功（ToolExecutor）
2026-02-03 01:36:07,176 - app.api.v1.agent - INFO - [Stream] 任务完成: 根据用户提供的知识库文档和详细要求，创作一段300-500字的场景描写。 (31.0s)
2026-02-03 01:36:07,176 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1完成
2026-02-03 01:36:07,176 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共1个任务，耗时: 31.01s
2026-02-03 01:36:07,176 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2026-02-03 01:36:07,176 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=1, 展示型=0
2026-02-03 01:36:07,176 - app.services.agent.langgraph_agent - INFO - [Response] 检测到知识库文档(1个)，使用AI整合（确保流式输出）
2026-02-03 01:36:07,181 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2026-02-03 01:36:07,181 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=1, 展示型=0
2026-02-03 01:36:07,181 - app.services.agent.planning.response_builder - INFO - [Summarization] 注入 1 个知识库文档到总结prompt
2026-02-03 01:36:07,181 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=1003字符, 处理后=1044字符
2026-02-03 01:36:07,181 - app.services.agent.planning.response_builder - INFO - [Summarization] 准备发送 summarization_start 事件
2026-02-03 01:36:07,181 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-02-03 01:36:07,181 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-02-03 01:36:08,785 - app.services.agent.planning.response_builder - INFO - [Summarization] reason生成: len=58 content=段融傍晚完成马坊杂活后，在院中练习浑圆桩，赵穆在一旁，他回忆起羚羊献食的往事，并思考吞噬器灵的可能，手中紧握牛尾刀。
2026-02-03 01:36:08,785 - app.services.agent.stream.stream_event_handler - INFO - [StreamEventHandler] emit_summarization_start 被调用, _on_flow_event=True, reason_len=58, reason=段融傍晚完成马坊杂活后，在院中练习浑圆桩，赵穆在一旁，他回忆起羚羊献食的往事，并思考吞噬器灵的可能，手中紧握牛尾刀。
2026-02-03 01:36:08,785 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_start 事件已发送
2026-02-03 01:36:08,785 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2026-02-03 01:36:08,785 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2026-02-03 01:36:08,796 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-02-03 01:36:08,796 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-02-03 01:36:13,514 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_complete 事件已发送（第一个chunk时）
2026-02-03 01:36:13,516 - app.services.agent.planning.response_builder - INFO - [Summarization] output_ready 事件已发送（第一个chunk时）
2026-02-03 01:36:15,863 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=782
2026-02-03 01:36:16,574 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:58a111d4-1083-4fd9-b907-723b605e3481 | 重要度=0.87
2026-02-03 01:36:17,114 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:58a111d4-1083-4fd9-b907-723b605e3481 | 重要度=0.60
2026-02-03 01:36:17,125 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:58a111d4-1083-4fd9-b907-723b605e3481:5283ef8e-8f5f-44c9-8b09-752a59864dc5, token=1173
2026-02-03 01:36:17,126 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:58a111d4-1083-4fd9-b907-723b605e3481:5283ef8e-8f5f-44c9-8b09-752a59864dc5, 消息数=2, 摘要长度=0, Token=1173
2026-02-03 01:36:17,127 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:58a111d4-1083-4fd9-b907-723b605e3481:5283ef8e-8f5f-44c9-8b09-752a59864dc5)
2026-02-03 01:36:17,127 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2026-02-03 01:36:17,322 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed