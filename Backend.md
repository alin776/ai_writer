INFO:     127.0.0.1:58313 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2026-02-03 21:41:41,937 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 改写这段，让画面感更强...
2026-02-03 21:41:41,938 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-02-03 21:41:41,938 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-02-03 21:41:41,938 - app.services.ai.http_ai_service - INFO - [成本追踪] 初始化未传db/user_id，将使用请求上下文按需记录成本
2026-02-03 21:41:43,495 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz:8443/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-02-03 21:41:43,499 - app.services.agent.tools.writing_tools - INFO - Writing tools AI service initialized
2026-02-03 21:41:43,500 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ AI Service 已同时设置到 langgraph_tools 和 writing_tools
2026-02-03 21:41:43,500 - app.services.context.adaptive_budget - INFO - ✅ 所有预算配置验证通过
2026-02-03 21:41:49,347 - app.services.context.vector_memory_store - INFO - ✅ VectorMemoryStore初始化成功 | 目录=./data/chroma_db | 模型=paraphrase-multilingual-MiniLM-L12-v2 | 集合=user_memories
2026-02-03 21:41:49,347 - app.services.context.manager - INFO - ✅ VectorMemoryStore 已初始化
2026-02-03 21:41:49,347 - app.services.context.manager - INFO - ✅ ContextManager: 长期记忆已启用 (user_id=None)
2026-02-03 21:41:49,347 - app.services.context.manager - INFO - ✅ ContextManager: 自适应预算已启用
2026-02-03 21:41:49,347 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ ContextManager已初始化（长期记忆已启用，自适应预算已启用，总预算=16000 tokens）
成功加载模板: analyze_text (版本 3.1.0)
成功加载模板: writing_agent (版本 2.0.0)
成功加载模板: system_agent_prompt (版本 2.1.0)
成功加载模板: creative_writing_prompt (版本 1.0.0)
2026-02-03 21:41:49,378 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ PromptManager已初始化
2026-02-03 21:41:49,392 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ Redis连接验证成功
2026-02-03 21:41:49,394 - app.services.agent.langgraph_agent - INFO - [LangGraph] OK 使用 AsyncRedisSaver（redis://localhost:6379/0，TTL=7天）
2026-02-03 21:41:49,395 - app.services.agent.memory.metrics - INFO - [MemoryMetrics] 监控系统已初始化
2026-02-03 21:41:49,395 - app.services.agent.memory.long_term_store - INFO - [LongTermStore] Initialized: base_dir=./data/long_term_memory, max_size=50KB, compression=True
2026-02-03 21:41:49,395 - app.services.agent.memory.enhanced_memory_manager - INFO - EnhancedMemoryManager initialized: short=10, medium=100, threshold=0.1, long_term_backup=enabled
2026-02-03 21:41:49,395 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ EnhancedMemoryManager已创建
2026-02-03 21:41:49,396 - app.services.agent.memory.unified_coordinator - INFO - [UnifiedMemoryCoordinator] 初始化统一记忆协调器
2026-02-03 21:41:49,397 - app.services.agent.memory.unified_coordinator - INFO - [UnifiedMemoryCoordinator] 全局实例已设置
2026-02-03 21:41:49,397 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ UnifiedMemoryCoordinator已初始化 | checkpointer=AsyncRedisSaver | enhanced_memory=yes | context_manager=yes
2026-02-03 21:41:49,397 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ 解耦模块已初始化 (IntentClassifier, ToolExecutor, EventParser, ResponseBuilder, ToolDispatcher, ParallelExecutor, PlanGenerator, QuickPathHandler, StreamEventHandler, SecondaryToolHandler, TaskRunner, AgentExecutor)
2026-02-03 21:41:49,410 - app.services.agent.parallel_tool_node - INFO - [ParallelToolNode] 初始化完成，最大并发数=5，并行安全工具=6个
2026-02-03 21:41:49,423 - app.api.v1.agent - INFO - [Global Agent] created global agent instance; MemorySaver shared across requests
2026-02-03 21:41:49,441 - app.api.v1.agent - INFO - [agent_chat_stream] 📚 世界观数据已注入: 人物=11, 地点=6, 设定=7, 规范=无
2026-02-03 21:41:49,441 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f289900b-b924-4a77-b97b-2e4887bfc29a:47cb1b38-580a-46e0-b98e-6da4845756c1 (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=f289900b-b924-4a77-b97b-2e4887bfc29a, conversation_id=47cb1b38-580a-46e0-b98e-6da4845756c1)
2026-02-03 21:41:49,441 - app.services.context.monitoring_integration - INFO - ✅ ContextManager监控收集器已初始化
2026-02-03 21:41:49,441 - app.services.context.store - INFO - [ContextStore] Redis连接成功
2026-02-03 21:41:49,441 - app.services.context.store - INFO - [ContextStore] 加载上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f289900b-b924-4a77-b97b-2e4887bfc29a:47cb1b38-580a-46e0-b98e-6da4845756c1, 6条消息
2026-02-03 21:41:49,636 - app.services.context.token_counter - INFO - ✅ tiktoken初始化成功，模型: gemini-2.5-pro -> cl100k_base
2026-02-03 21:41:49,640 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f289900b-b924-4a77-b97b-2e4887bfc29a:47cb1b38-580a-46e0-b98e-6da4845756c1: 1040/16000 tokens
2026-02-03 21:41:50,323 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='改写这段，让画面感更强...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:f289900b-b924-4a77-b97b-2e4887bfc29a', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=3条
2026-02-03 21:41:50,323 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=f289900b-b924-4a77-b97b-2e4887bfc29a | 含用户级=True | 找到=3条
2026-02-03 21:41:50,399 - app.services.context.manager - INFO - [Deduplication] ✅ 去重完成: 6 -> 5条消息 (移除1条重复)
2026-02-03 21:41:50,399 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 6条消息, 1027 tokens, 耗时 958.28ms
2026-02-03 21:41:50,399 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 6 条历史消息 (token: 1027, has_summary: False)
2026-02-03 21:41:50,410 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-02-03 21:41:50,411 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-02-03 21:41:52,048 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-02-03 21:41:52,048 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-02-03 21:41:53,327 - app.services.agent.intent.classifier - INFO - [Intent] AI识别结果: writing
2026-02-03 21:41:53,330 - app.services.agent.langgraph_agent - INFO - [Planning] AI意图分类: writing (置信度: 0.90)
2026-02-03 21:41:53,330 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 改写这段，让画面感更强...
2026-02-03 21:41:53,346 - app.services.agent.planning.plan_generator - INFO - [Planning] 注入选中文本到prompt: 此处是镖局内，堆放柴炭的地方，平常少有人至，但此时，却有十多个单薄的身影，在空地上，稀稀落落地站着。...
2026-02-03 21:41:53,347 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-02-03 21:41:53,347 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=story_planning, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: story_planning; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-02-03 21:42:40,699 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=29194
2026-02-03 21:42:40,700 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户期望获得一段改写后的文本，并替换掉编辑器中选中的原文。改, 原料=1. 需要改写的原文：用户在编辑器中选中, 处理=这是一个标准的“改写并替换”流程，遵循三
2026-02-03 21:42:40,736 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共3个任务
2026-02-03 21:42:40,737 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共3个任务，耗时: 47.41s
2026-02-03 21:42:40,737 - app.api.v1.agent - INFO - [Stream] Plan tasks: 3 items
2026-02-03 21:42:40,738 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2026-02-03 21:42:40,739 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2026-02-03 21:42:40,740 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2026-02-03 21:42:40,741 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] DAG 调度启用，任务数=3, 有依赖任务=2
2026-02-03 21:42:40,742 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1开始: 定位用户选中的文本“此处是镖局内...”，并获取其上下文信息，为改写做准备。
2026-02-03 21:42:40,742 - app.api.v1.agent - INFO - [Stream] Task started: 定位用户选中的文本“此处是镖局内...”，并获取其上下文信息，为改写做准备。 (icon=Wrench)
2026-02-03 21:42:40,743 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: explore_content
2026-02-03 21:42:40,744 - app.services.agent.tools.explore_tools - INFO - [explore_content] 开始: work_id=f289900b-b924-4a77-b97b-2e4887bfc29a, target=定位用户在第一章选中的文本“此处是镖局内，堆放柴炭的地方...”，并获取其上下文。（需精确段落定位）...
2026-02-03 21:42:40,744 - app.services.agent.tools.explore_tools - INFO - [explore_content] 规划传入关键词: ['镖局内', '堆放柴炭', '单薄的身影', '稀稀落落']
2026-02-03 21:42:40,755 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 启用严格段落号模式
2026-02-03 21:42:40,755 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 章节范围锁定: 第1章
2026-02-03 21:42:40,756 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 开始探索 V5: work_id=f289900b-b924-4a77-b97b-2e4887bfc29a, target=定位用户在第一章选中的文本“此处是镖局内，堆放柴炭的地方...”，并获取其上下文。（需精确段落定位）...
2026-02-03 21:42:40,756 - app.services.chapter_service - INFO - [ChapterService] Querying chapters for work_id=f289900b-b924-4a77-b97b-2e4887bfc29a, type=<class 'uuid.UUID'>
2026-02-03 21:42:40,765 - app.services.chapter_service - INFO - [ChapterService] Found 5 chapters
2026-02-03 21:42:40,766 - app.services.chapter_service - INFO -   - Chapter: 第1章 吞噬, order=1
2026-02-03 21:42:40,766 - app.services.chapter_service - INFO -   - ... (3 more chapters)
2026-02-03 21:42:40,767 - app.services.chapter_service - INFO -   - Chapter: 第5章 太一门, order=5
2026-02-03 21:42:40,794 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 章节范围映射: 第1章 -> 第1章
2026-02-03 21:42:40,808 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 自动获取世界观...
2026-02-03 21:42:40,829 - app.services.agent.langgraph_tools - INFO - [get_writing_context] ✅ 获取创作上下文成功: include=worldview
2026-02-03 21:42:40,831 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 世界观获取完成: 24 条
2026-02-03 21:42:40,831 - app.services.ai.http_ai_service - INFO - [成本追踪] 初始化未传db/user_id，将使用请求上下文按需记录成本
2026-02-03 21:42:42,311 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz:8443/v1, Model: gemini-2.5-flash, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: False, CostTracking: True
2026-02-03 21:42:42,312 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-02-03 21:42:55,674 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 强制流程步骤: list_chapters
2026-02-03 21:42:55,675 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=list_chapters params={"work_id": "f289900b-b924-4a77-b97b-2e4887bfc29a"}
2026-02-03 21:42:55,676 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=list_chapters success=True count=1
2026-02-03 21:43:07,972 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 强制流程步骤: list_paragraphs
2026-02-03 21:43:07,973 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=list_paragraphs params={"chapter_order": 1, "offset": 0, "limit": 50, "preview_len": 80, "work_id": "f289900b-b924-4a77-b97b-2e4887bfc29a"}
2026-02-03 21:43:07,996 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=list_paragraphs success=True chapter=1 offset=0 limit=50 approximate=None
2026-02-03 21:43:17,014 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=read_paragraph params={"chapter_order": 1, "paragraph_index": 3, "context_before": 2, "context_after": 2, "work_id": "f289900b-b924-4a77-b97b-2e4887bfc29a"}
2026-02-03 21:43:17,031 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=read_paragraph success=True chapter=1 paragraph=3 index_base=zero
2026-02-03 21:43:38,762 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 探索完成(工具循环): 3轮, 原因=目标文本“此处是镖局内，堆放柴炭的地方...”已在第1章第3段找到，并且其上下文（段落1-5）已通过上一次read_paragraph工具调用获取并覆盖，任务已完成。
2026-02-03 21:43:39,039 - app.services.agent.execution.tool_executor - INFO - [StandardTool] explore_content 执行成功
2026-02-03 21:43:39,041 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 目标章节已固化: 228fadc5-37d4-4925-8a83-414990e1e012 (source=explore.locate_targets)
2026-02-03 21:43:39,043 - app.api.v1.agent - INFO - [Stream] 任务完成: 定位用户选中的文本“此处是镖局内...”，并获取其上下文信息，为改写做准备。 (58.3s)
2026-02-03 21:43:39,043 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1完成
2026-02-03 21:43:39,044 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务2开始: 根据用户“增强画面感”的要求，对指定的段落进行改写。
2026-02-03 21:43:39,045 - app.api.v1.agent - INFO - [Stream] Task started: 根据用户“增强画面感”的要求，对指定的段落进行改写。 (icon=Edit3)
2026-02-03 21:43:39,046 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 任务2 绑定目标章节: 228fadc5-37d4-4925-8a83-414990e1e012
2026-02-03 21:43:39,050 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: smart_rewrite
2026-02-03 21:43:39,051 - app.services.agent.execution.tool_executor - WARNING - [ToolExecutor] smart_rewrite evidence_context 非字符串，已强制转换
2026-02-03 21:43:39,076 - app.services.agent.tools.tool_types - INFO - [smart_rewrite] 开始执行工具
2026-02-03 21:43:39,089 - app.services.agent.tools.editor_tools - INFO - [smart_rewrite] 开始生成改写结果，原文长度: 50, 用户要求: 改写这段，让画面感更强。可以从环境（如柴炭、煤灰、阴暗角落）、人物（单薄、紧张、期待的眼神）和氛围（僻静、压抑中带着一丝希望）等角度进行描绘。
2026-02-03 21:43:39,090 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-02-03 21:43:39,090 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-02-03 21:43:39,091 - app.services.ai.http_ai_service - INFO - [成本追踪] 初始化未传db/user_id，将使用请求上下文按需记录成本
2026-02-03 21:43:41,261 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz:8443/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-02-03 21:43:41,267 - app.services.agent.tools.editor_tools - INFO - [smart_rewrite] 使用传统单Prompt架构
2026-02-03 21:43:41,269 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-02-03 21:43:41,271 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=content_creation, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro
2026-02-03 21:44:00,588 - app.services.agent.tools.editor_tools - INFO - [smart_rewrite] AI返回长度: 158
2026-02-03 21:44:00,588 - app.services.agent.tools.editor_tools - INFO - [smart_rewrite] 成功生成1条改写结果
2026-02-03 21:44:00,593 - app.services.agent.tools.tool_types - INFO - [smart_rewrite] 执行成功 (耗时: 21.517s)
2026-02-03 21:44:00,593 - app.services.agent.tools.tool_monitor - INFO - ToolMonitor initialized with Memory storage, retention: 7 days
2026-02-03 21:44:00,593 - app.services.agent.execution.tool_executor - INFO - [StandardTool] smart_rewrite 执行成功
2026-02-03 21:44:00,593 - app.api.v1.agent - INFO - [Stream] 任务完成: 根据用户“增强画面感”的要求，对指定的段落进行改写。 (21.5s)
2026-02-03 21:44:00,597 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务2完成
2026-02-03 21:44:00,597 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务3开始: 将改写后的内容替换回原文位置。
2026-02-03 21:44:00,597 - app.api.v1.agent - INFO - [Stream] Task started: 将改写后的内容替换回原文位置。 (icon=Check)
2026-02-03 21:44:00,598 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 任务3 绑定目标章节: 228fadc5-37d4-4925-8a83-414990e1e012
2026-02-03 21:44:00,599 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: operate_apply
2026-02-03 21:44:00,599 - app.services.agent.execution.tool_executor - INFO - [ToolExecutor] operate_apply chapter_id 来源=explicit value=228fadc5-37d4-4925-8a83-414990e1e012
2026-02-03 21:44:00,600 - app.services.agent.tools.tool_types - INFO - [operate_apply] 开始执行工具
2026-02-03 21:44:00,600 - app.services.agent.tools.operate_tools - INFO - [Operate] 开始: op=replace, chapter=228fadc5-37d4-4925-8a83-414990e1e012
2026-02-03 21:44:00,600 - app.services.agent.tools.operate_tools - INFO - [Operate] 路由: tool=apply_chapter_edit, target_op=replace, needs_locate=True
2026-02-03 21:44:00,604 - app.services.agent.tools.operate_tools - INFO - [Operate] 使用 DIRECT 定位: para=3, node=xwjo4bg1
2026-02-03 21:44:00,604 - app.services.agent.tools.operate_tools - INFO - [Operate] 定位完成: method=direct, para=3
2026-02-03 21:44:00,604 - app.services.agent.tools.editor_tools - INFO - [apply_chapter_edit] 参数: chapter_id=228fadc5-37d4-4925-8a83-414990e1e012, operation=replace, content_len=58
2026-02-03 21:44:00,652 - app.services.agent.tools.tool_types - INFO - [operate_apply] 执行成功 (耗时: 0.052s)
2026-02-03 21:44:00,652 - app.services.agent.execution.tool_executor - INFO - [StandardTool] operate_apply 执行成功
2026-02-03 21:44:00,665 - app.api.v1.agent - INFO - [Stream] 任务完成: 将改写后的内容替换回原文位置。 (0.1s)
2026-02-03 21:44:00,666 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务3完成
2026-02-03 21:44:00,667 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共3个任务，耗时: 79.93s
2026-02-03 21:44:00,667 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2026-02-03 21:44:00,667 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=3, 展示型=0
2026-02-03 21:44:00,668 - app.services.agent.langgraph_agent - INFO - [Response] 3个输出任务（含续写），使用AI整合
2026-02-03 21:44:00,668 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2026-02-03 21:44:00,668 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=3, 展示型=0
2026-02-03 21:44:00,669 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=2731字符, 处理后=2815字符
2026-02-03 21:44:00,669 - app.services.agent.planning.response_builder - INFO - [Summarization] 准备发送 summarization_start 事件
2026-02-03 21:44:00,669 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-02-03 21:44:00,669 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-02-03 21:44:02,579 - app.services.agent.planning.response_builder - INFO - [Summarization] reason生成: len=35 content=成功改写了“此处是镖局内...”的文本，增强了画面感，并已替换回原文。
2026-02-03 21:44:02,587 - app.services.agent.stream.stream_event_handler - INFO - [StreamEventHandler] emit_summarization_start 被调用, _on_flow_event=True, reason_len=35, reason=成功改写了“此处是镖局内...”的文本，增强了画面感，并已替换回原文。
2026-02-03 21:44:02,588 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_start 事件已发送
2026-02-03 21:44:02,589 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2026-02-03 21:44:02,589 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2026-02-03 21:44:02,592 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-02-03 21:44:02,592 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-02-03 21:44:05,159 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_complete 事件已发送（第一个chunk时）
2026-02-03 21:44:05,159 - app.services.agent.planning.response_builder - INFO - [Summarization] output_ready 事件已发送（第一个chunk时）
2026-02-03 21:44:06,189 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=300
2026-02-03 21:44:06,411 - app.services.context.vector_memory_store - INFO - 🔁 跳过重复记忆，复用ID=79913e7e-d5cd-4e09-bce6-ca6639bd8456_1770121745541_63cdb878
2026-02-03 21:44:06,411 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:f289900b-b924-4a77-b97b-2e4887bfc29a | 重要度=0.65
2026-02-03 21:44:07,055 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:f289900b-b924-4a77-b97b-2e4887bfc29a | 重要度=0.94
2026-02-03 21:44:07,064 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f289900b-b924-4a77-b97b-2e4887bfc29a:47cb1b38-580a-46e0-b98e-6da4845756c1, token=1362
2026-02-03 21:44:07,066 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f289900b-b924-4a77-b97b-2e4887bfc29a:47cb1b38-580a-46e0-b98e-6da4845756c1, 消息数=7, 摘要长度=0, Token=1362
2026-02-03 21:44:07,067 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:f289900b-b924-4a77-b97b-2e4887bfc29a:47cb1b38-580a-46e0-b98e-6da4845756c1)
2026-02-03 21:44:07,067 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2026-02-03 21:44:07,394 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed