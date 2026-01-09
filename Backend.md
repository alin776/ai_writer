2026-01-09 22:36:17,150 - app.services.context.adaptive_budget - INFO - ✅ 所有预算配置验证通过
2026-01-09 22:36:23,769 - app.services.context.vector_memory_store - INFO - ✅ VectorMemoryStore初始化成功 | 目录=./data/chroma_db | 模型=paraphrase-multilingual-MiniLM-L12-v2 | 集合=user_memories
2026-01-09 22:36:23,769 - app.services.context.manager - INFO - ✅ VectorMemoryStore 已初始化
2026-01-09 22:36:23,772 - app.services.context.manager - INFO - ✅ ContextManager: 长期记忆已启用 (user_id=None)
2026-01-09 22:36:23,772 - app.services.context.manager - INFO - ✅ ContextManager: 自适应预算已启用
2026-01-09 22:36:23,772 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ ContextManager已初始化（长期记忆已启用，自适应预算已启用，总预算=16000 tokens）
成功加载模板: analyze_text (版本 3.1.0)
成功加载模板: writing_agent (版本 2.0.0)
成功加载模板: system_agent_prompt (版本 2.1.0)
成功加载模板: creative_writing_prompt (版本 1.0.0)
2026-01-09 22:36:23,793 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ PromptManager已初始化
2026-01-09 22:36:23,799 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ Redis连接验证成功
2026-01-09 22:36:23,800 - app.services.agent.langgraph_agent - INFO - [LangGraph] OK 使用 AsyncRedisSaver（redis://localhost:6379/0，TTL=7天）
2026-01-09 22:36:23,800 - app.services.agent.memory.metrics - INFO - [MemoryMetrics] 监控系统已初始化
2026-01-09 22:36:23,801 - app.services.agent.memory.long_term_store - INFO - [LongTermStore] Initialized: base_dir=./data/long_term_memory, max_size=50KB, compression=True
2026-01-09 22:36:23,801 - app.services.agent.memory.enhanced_memory_manager - INFO - EnhancedMemoryManager initialized: short=10, medium=100, threshold=0.1, long_term_backup=enabled
2026-01-09 22:36:23,802 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ EnhancedMemoryManager已创建
2026-01-09 22:36:23,802 - app.services.agent.memory.unified_coordinator - INFO - [UnifiedMemoryCoordinator] 初始化统一记忆协调器
2026-01-09 22:36:23,802 - app.services.agent.memory.unified_coordinator - INFO - [UnifiedMemoryCoordinator] 全局实例已设置
2026-01-09 22:36:23,802 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ UnifiedMemoryCoordinator已初始化 | checkpointer=AsyncRedisSaver | enhanced_memory=yes | context_manager=yes
2026-01-09 22:36:23,802 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ 解耦模块已初始化 (IntentClassifier, ToolExecutor, EventParser, ResponseBuilder, ToolDispatcher, ParallelExecutor, PlanGenerator, QuickPathHandler, StreamEventHandler, SecondaryToolHandler, TaskRunner, AgentExecutor)
2026-01-09 22:36:23,807 - app.services.agent.parallel_tool_node - INFO - [ParallelToolNode] 初始化完成，最大并发数=5，并行安全工具=4个
2026-01-09 22:36:23,813 - app.api.v1.agent - INFO - [Global Agent] created global agent instance; MemorySaver shared across requests
2026-01-09 22:36:23,844 - app.api.v1.agent - INFO - [agent_chat_stream] 📚 世界观数据已注入: 人物=9, 地点=6, 设定=6, 规范=无
2026-01-09 22:36:23,844 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:0fd87250-a111-4d14-8804-ba6cd06e776d (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=9f98efd6-1593-4967-ad43-f5dac759ac1c, conversation_id=0fd87250-a111-4d14-8804-ba6cd06e776d)
2026-01-09 22:36:23,847 - app.services.context.monitoring_integration - INFO - ✅ ContextManager监控收集器已初始化
2026-01-09 22:36:23,847 - app.services.context.store - INFO - [ContextStore] Redis连接成功
2026-01-09 22:36:23,851 - app.services.context.manager - INFO - [ContextManager] 创建新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:0fd87250-a111-4d14-8804-ba6cd06e776d
2026-01-09 22:36:23,972 - app.services.context.token_counter - INFO - ✅ tiktoken初始化成功，模型: gemini-2.5-pro -> cl100k_base
2026-01-09 22:36:23,972 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:0fd87250-a111-4d14-8804-ba6cd06e776d: 0/16000 tokens
2026-01-09 22:36:24,721 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='帮我找到段融第一次吞噬器灵的场景，然后用"展示而非告诉"的手...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:9f98efd6-1593-4967-ad43-f5dac759ac1c', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=3条
2026-01-09 22:36:24,721 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=9f98efd6-1593-4967-ad43-f5dac759ac1c | 含用户级=True | 找到=3条
2026-01-09 22:36:24,721 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 1条消息, 0 tokens, 耗时 873.82ms
2026-01-09 22:36:24,721 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 1 条历史消息 (token: 0)
2026-01-09 22:36:24,721 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-09 22:36:24,721 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-09 22:36:24,721 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=20, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-09 22:36:26,637 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-09 22:36:26,640 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-09 22:36:26,847 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-09 22:36:26,847 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=322, cost=$0.000033, time=1920ms
2026-01-09 22:36:26,847 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=7, 尝试次数=1
2026-01-09 22:36:26,847 - app.services.agent.intent.classifier - INFO - [Intent] AI识别结果: writing
2026-01-09 22:36:26,847 - app.services.agent.langgraph_agent - INFO - [Planning] AI意图分类: writing (置信度: 0.90)
2026-01-09 22:36:26,847 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 帮我找到段融第一次吞噬器灵的场景，然后用"展示而非告诉"的手法改写他内心的兴奋和紧张，让读者能感受到...
2026-01-09 22:36:26,873 - app.core.cache - INFO - ✅ 缓存命中: prompt:planning:v2.36.0:get_planning_static_prompt:fca6eb91156619d0
2026-01-09 22:36:26,880 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-09 22:36:26,880 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=story_planning, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: story_planning; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-01-09 22:36:26,880 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.3, task_type=TaskType.STORY_PLANNING
2026-01-09 22:36:27,007 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:61297 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 22:36:35,545 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-09 22:36:39,617 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 9 个数据块，总长度: 1129
2026-01-09 22:36:39,617 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 12869 (prompt=12301, completion=568)
2026-01-09 22:36:39,619 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-09 22:36:39,619 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-09 22:36:39,645 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-09 22:36:39,645 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=12869, cost=$0.021056, time=12740ms
2026-01-09 22:36:39,645 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=12869
2026-01-09 22:36:39,645 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户想要找到一个特定场景的原文，并对其进行改写，以“展示而非, 原料=1. 需要通过搜索找到“段融第一次吞噬器, 处理=1. 使用 `search_analys
2026-01-09 22:36:39,654 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共2个任务
2026-01-09 22:36:39,654 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共2个任务，耗时: 12.81s
2026-01-09 22:36:39,654 - app.api.v1.agent - INFO - [Stream] Plan tasks: 2 items
2026-01-09 22:36:39,657 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2026-01-09 22:36:39,659 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2026-01-09 22:36:39,662 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2026-01-09 22:36:39,662 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 任务分组: 第一层并行=1, 第二层并行=0, 串行=1
2026-01-09 22:36:39,662 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始第一层并行执行1个任务
2026-01-09 22:36:39,662 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务1开始: 搜索“段融第一次吞噬器灵”的场景
2026-01-09 22:36:39,662 - app.api.v1.agent - INFO - [Stream] Task started: 搜索“段融第一次吞噬器灵”的场景 (icon=Search)
2026-01-09 22:36:39,664 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(search_analysis_fragments)
2026-01-09 22:36:39,664 - app.services.agent.tools.tool_types - INFO - [search_analysis_fragments] 开始执行工具
2026-01-09 22:36:40,896 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=9f98efd6-1593-4967-ad43-f5dac759ac1c, current_order=1, query=吞噬器灵...
2026-01-09 22:36:41,141 - app.services.chapter_vector_service - INFO - RAG retrieved 10 segments within order<=3
Building prefix dict from the default dictionary ...
2026-01-09 22:36:41,141 - jieba - DEBUG - Building prefix dict from the default dictionary ...
Loading model from cache D:\Temp\jieba.cache
2026-01-09 22:36:41,143 - jieba - DEBUG - Loading model from cache D:\Temp\jieba.cache
Loading model cost 0.996 seconds.
2026-01-09 22:36:42,139 - jieba - DEBUG - Loading model cost 0.996 seconds.
Prefix dict has been built successfully.
2026-01-09 22:36:42,139 - jieba - DEBUG - Prefix dict has been built successfully.
2026-01-09 22:36:42,149 - app.services.agent.langgraph_tools - INFO - [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
2026-01-09 22:36:42,149 - app.services.agent.tools.tool_types - INFO - [search_analysis_fragments] 执行成功 (耗时: 2.485s)
2026-01-09 22:36:42,149 - app.services.agent.tools.tool_monitor - INFO - ToolMonitor initialized with Memory storage, retention: 7 days
2026-01-09 22:36:42,149 - app.services.agent.execution.task_runner - INFO - [TaskRunner] search_analysis_fragments 执行成功（DeepAgent模式）
2026-01-09 22:36:42,149 - app.api.v1.agent - INFO - [Stream] 任务完成: 搜索“段融第一次吞噬器灵”的场景 (2.5s)
2026-01-09 22:36:42,149 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务1完成
2026-01-09 22:36:42,156 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始串行执行1个任务
2026-01-09 22:36:42,156 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务2开始: 使用“展示而非告诉”的手法，改写段融发现能力可用时的内心活动
2026-01-09 22:36:42,156 - app.api.v1.agent - INFO - [Stream] Task started: 使用“展示而非告诉”的手法，改写段融发现能力可用时的内心活动 (icon=Edit3)
2026-01-09 22:36:42,156 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: smart_rewrite
2026-01-09 22:36:42,156 - app.services.agent.tools.tool_types - INFO - [smart_rewrite] 开始执行工具
2026-01-09 22:36:42,166 - app.services.agent.tools.editor_tools - INFO - [smart_rewrite] 开始生成改写版本，原文长度: 28, 用户要求: 找到段融第一次吞噬器灵的场景，然后用'展示而非告诉'的手法改写他内心的兴奋和紧张，让读者能感受到他发现自己能力可用时的激动心情。重点描绘他的生理反应和下意识的动作，而不是直接说他'很激动'或'很紧张'。, 基准版本: 无
2026-01-09 22:36:42,167 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-09 22:36:42,167 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-09 22:36:42,168 - app.services.ai.http_ai_service - INFO - [成本追踪] 初始化未传db/user_id，将使用请求上下文按需记录成本
2026-01-09 22:36:43,542 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-09 22:36:43,542 - app.services.agent.tools.editor_tools - INFO - [smart_rewrite] 使用传统单Prompt架构
2026-01-09 22:36:43,542 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-09 22:36:43,544 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=content_creation, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro
2026-01-09 22:36:43,544 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=4000, temp=0.8, 尝试=1/3, task_type=TaskType.CONTENT_CREATION
2026-01-09 22:36:57,284 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:64408 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 22:37:16,198 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-09 22:37:16,198 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-09 22:37:16,218 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-09 22:37:16,220 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=3426, cost=$0.009043, time=32656ms
2026-01-09 22:37:16,220 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=766, 尝试次数=1
2026-01-09 22:37:16,220 - app.services.agent.tools.editor_tools - INFO - [smart_rewrite] AI返回长度: 766
2026-01-09 22:37:16,220 - app.services.agent.tools.editor_tools - INFO - [smart_rewrite] 成功生成3个改写版本
2026-01-09 22:37:16,224 - app.services.agent.tools.tool_types - INFO - [smart_rewrite] 执行成功 (耗时: 34.068s)
2026-01-09 22:37:16,224 - app.services.agent.execution.tool_executor - INFO - [StandardTool] smart_rewrite 执行成功
2026-01-09 22:37:16,226 - app.api.v1.agent - INFO - [Stream] 任务完成: 使用“展示而非告诉”的手法，改写段融发现能力可用时的内心活动 (34.1s)
2026-01-09 22:37:16,226 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务2完成
2026-01-09 22:37:16,226 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共2个任务，耗时: 36.57s
2026-01-09 22:37:16,226 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2026-01-09 22:37:16,226 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=1, 输出型=1, 展示型=0
2026-01-09 22:37:16,226 - app.services.agent.langgraph_agent - INFO - [Response] 单个输出任务(smart_rewrite)，使用AI整合
2026-01-09 22:37:16,233 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2026-01-09 22:37:16,234 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=1, 输出型=1, 展示型=0
2026-01-09 22:37:16,234 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=4380字符, 处理后=4431字符
2026-01-09 22:37:16,234 - app.services.agent.planning.response_builder - INFO - [Summarization] 准备发送 summarization_start 事件
2026-01-09 22:37:16,236 - app.services.agent.stream.stream_event_handler - INFO - [StreamEventHandler] emit_summarization_start 被调用, _on_flow_event=True
2026-01-09 22:37:16,236 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_start 事件已发送
2026-01-09 22:37:16,236 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2026-01-09 22:37:16,238 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2026-01-09 22:37:16,244 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-09 22:37:16,244 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-09 22:37:16,244 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
2026-01-09 22:37:27,318 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:58043 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 22:37:33,867 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-09 22:37:33,867 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_complete 事件已发送（第一个chunk时）
2026-01-09 22:37:33,867 - app.services.agent.planning.response_builder - INFO - [Summarization] output_ready 事件已发送（第一个chunk时）
2026-01-09 22:37:39,178 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 27 个数据块，总长度: 1731
2026-01-09 22:37:39,179 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 7978 (prompt=6686, completion=1292)
2026-01-09 22:37:39,181 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-09 22:37:39,182 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-09 22:37:39,206 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-09 22:37:39,208 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=7978, cost=$0.005236, time=22937ms
2026-01-09 22:37:39,210 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=1731
2026-01-09 22:37:44,447 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:9f98efd6-1593-4967-ad43-f5dac759ac1c | 重要度=0.65
2026-01-09 22:37:49,105 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:9f98efd6-1593-4967-ad43-f5dac759ac1c | 重要度=0.77
2026-01-09 22:37:49,128 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:0fd87250-a111-4d14-8804-ba6cd06e776d, token=2227
2026-01-09 22:37:49,133 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:0fd87250-a111-4d14-8804-ba6cd06e776d, 消息数=2, Token=2227
2026-01-09 22:37:49,133 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:0fd87250-a111-4d14-8804-ba6cd06e776d)
2026-01-09 22:37:49,135 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2026-01-09 22:37:49,146 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed
2026-01-09 22:37:57,378 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:50453 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 22:38:04,378 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 9f98efd6-1593-4967-ad43-f5dac759ac1c, chapter_id: cdabcd19-8562-4d6e-82b6-d37caae83a5d
2026-01-09 22:38:04,417 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 9f98efd6-1593-4967-ad43-f5dac759ac1c, chapter_id: cdabcd19-8562-4d6e-82b6-d37caae83a5d
2026-01-09 22:38:04,438 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: cdabcd19-8562-4d6e-82b6-d37caae83a5d
2026-01-09 22:38:04,453 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: 270de73b-23af-4723-b61c-1b6fdc77bc9f
2026-01-09 22:38:04,455 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-09 22:38:04,460 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: cdabcd19-8562-4d6e-82b6-d37caae83a5d
2026-01-09 22:38:04,470 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
2026-01-09 22:38:04,475 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: 270de73b-23af-4723-b61c-1b6fdc77bc9f
2026-01-09 22:38:04,477 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
INFO:     127.0.0.1:57484 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-09 22:38:04,495 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:57481 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-09 22:38:04,999 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:9f98efd6-1593-4967-ad43-f5dac759ac1c
2026-01-09 22:38:05,008 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/cdabcd19-8562-4d6e-82b6-d37caae83a5d
INFO:     127.0.0.1:57487 - "PUT /api/v1/chapters/cdabcd19-8562-4d6e-82b6-d37caae83a5d HTTP/1.1" 200 OK
2026-01-09 22:38:05,013 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第3章 一夕千悟 (order=3)
2026-01-09 22:38:05,757 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第3章 一夕千悟 (5 chunks)
2026-01-09 22:38:05,784 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:9f98efd6-1593-4967-ad43-f5dac759ac1c
2026-01-09 22:38:05,786 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/cdabcd19-8562-4d6e-82b6-d37caae83a5d
INFO:     127.0.0.1:57490 - "PUT /api/v1/chapters/cdabcd19-8562-4d6e-82b6-d37caae83a5d HTTP/1.1" 200 OK
2026-01-09 22:38:05,788 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第3章 一夕千悟 (order=3)
2026-01-09 22:38:07,334 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第3章 一夕千悟 (5 chunks)
2026-01-09 22:38:07,701 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:52424 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2026-01-09 22:38:10,407 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:52428 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2026-01-09 22:38:10,422 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-09 22:38:10,422 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-09 22:38:10,422 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2026-01-09 22:38:13,417 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-09 22:38:13,418 - app.api.v1.agent - INFO - [Chat Stream] Mode: planning
2026-01-09 22:38:13,418 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:52431 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2026-01-09 22:38:13,427 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 读取第3章"一夕千悟"的内容，然后帮我续写500字，描写段融在月光下练刀的场景，要增强环境描写的感官...
2026-01-09 22:38:13,439 - app.api.v1.agent - INFO - [agent_chat_stream] 📚 世界观数据已注入: 人物=9, 地点=6, 设定=6, 规范=无
2026-01-09 22:38:13,439 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:b2cee05e-5336-4ab7-8af6-60818c5f7583 (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=9f98efd6-1593-4967-ad43-f5dac759ac1c, conversation_id=b2cee05e-5336-4ab7-8af6-60818c5f7583)
2026-01-09 22:38:13,445 - app.services.context.manager - INFO - [ContextManager] 创建新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:b2cee05e-5336-4ab7-8af6-60818c5f7583
2026-01-09 22:38:13,445 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:b2cee05e-5336-4ab7-8af6-60818c5f7583: 0/16000 tokens
2026-01-09 22:38:13,555 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='读取第3章"一夕千悟"的内容，然后帮我续写500字，描写段融...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:9f98efd6-1593-4967-ad43-f5dac759ac1c', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=3条
2026-01-09 22:38:13,555 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=9f98efd6-1593-4967-ad43-f5dac759ac1c | 含用户级=True | 找到=3条
2026-01-09 22:38:13,555 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 1条消息, 0 tokens, 耗时 115.57ms
2026-01-09 22:38:13,555 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 1 条历史消息 (token: 0)
2026-01-09 22:38:13,555 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-09 22:38:13,555 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-09 22:38:13,560 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=20, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-09 22:38:14,775 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-09 22:38:14,778 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-09 22:38:14,800 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-09 22:38:14,800 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=329, cost=$0.000033, time=1217ms
2026-01-09 22:38:14,800 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=7, 尝试次数=1
2026-01-09 22:38:14,800 - app.services.agent.intent.classifier - INFO - [Intent] AI识别结果: writing
2026-01-09 22:38:14,800 - app.services.agent.langgraph_agent - INFO - [Planning] AI意图分类: writing (置信度: 0.90)
2026-01-09 22:38:14,800 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 读取第3章"一夕千悟"的内容，然后帮我续写500字，描写段融在月光下练刀的场景，要增强环境描写的感官...
2026-01-09 22:38:14,809 - app.core.cache - INFO - ✅ 缓存命中: prompt:planning:v2.36.0:get_planning_static_prompt:fca6eb91156619d0
2026-01-09 22:38:14,814 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-09 22:38:14,814 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=story_planning, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: story_planning; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-01-09 22:38:14,814 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.3, task_type=TaskType.STORY_PLANNING
2026-01-09 22:38:27,407 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:59577 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 22:38:33,524 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-09 22:38:37,582 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 8 个数据块，总长度: 836
2026-01-09 22:38:37,582 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 13659 (prompt=13186, completion=473)
2026-01-09 22:38:37,582 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-09 22:38:37,584 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-09 22:38:37,601 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-09 22:38:37,601 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=13659, cost=$0.021213, time=22769ms
2026-01-09 22:38:37,603 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=13659
2026-01-09 22:38:37,603 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户希望我续写一段500字的小说内容，这是一个创作类请求。续, 原料=为了准确续写，我需要首先了解第三章“一夕, 处理=这是一个创作类请求，应遵循“分阶段执行”
2026-01-09 22:38:37,605 - app.services.agent.planning.plan_generator - INFO - [Planning] 直接回答模式，答案长度: 107
2026-01-09 22:38:37,605 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共1个任务
2026-01-09 22:38:37,605 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共1个任务，耗时: 22.81s
2026-01-09 22:38:37,608 - app.api.v1.agent - INFO - [Stream] Plan tasks: 1 items
2026-01-09 22:38:37,608 - app.services.agent.langgraph_agent - WARNING - [Planning-Alert] AI 违反协议：同时返回 direct_answer(107字) 和 1 个 tasks，将执行 tasks 而忽略 direct_answer
2026-01-09 22:38:37,608 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2026-01-09 22:38:37,610 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2026-01-09 22:38:37,610 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2026-01-09 22:38:37,610 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 任务分组: 第一层并行=1, 第二层并行=0, 串行=0
2026-01-09 22:38:37,610 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始第一层并行执行1个任务
2026-01-09 22:38:37,612 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务1开始: 读取章节'一夕千悟'的原文内容，以了解续写的上下文。
2026-01-09 22:38:37,612 - app.api.v1.agent - INFO - [Stream] Task started: 读取章节'一夕千悟'的原文内容，以了解续写的上下文。 (icon=FileText)
2026-01-09 22:38:37,612 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(read_chapter)
2026-01-09 22:38:37,614 - app.services.agent.tools.tool_types - INFO - [read_chapter] 开始执行工具
2026-01-09 22:38:37,626 - app.services.agent.langgraph_tools - INFO - [read_chapter_tool] ✅ 读取章节成功: 第3章 一夕千悟
2026-01-09 22:38:37,626 - app.services.agent.tools.tool_types - INFO - [read_chapter] 执行成功 (耗时: 0.013s)
2026-01-09 22:38:37,626 - app.services.agent.execution.task_runner - INFO - [TaskRunner] read_chapter 执行成功（DeepAgent模式）
2026-01-09 22:38:37,626 - app.api.v1.agent - INFO - [Stream] 任务完成: 读取章节'一夕千悟'的原文内容，以了解续写的上下文。 (0.0s)
2026-01-09 22:38:37,626 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务1完成
2026-01-09 22:38:37,626 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共1个任务，耗时: 0.02s
2026-01-09 22:38:37,626 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2026-01-09 22:38:37,626 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=1, 输出型=0, 展示型=0
2026-01-09 22:38:37,632 - app.services.agent.langgraph_agent - INFO - [Response] 分阶段执行第一阶段，基于任务结果生成询问
2026-01-09 22:38:37,632 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2026-01-09 22:38:37,633 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=1, 输出型=0, 展示型=0
2026-01-09 22:38:37,633 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=2502字符, 处理后=2533字符
2026-01-09 22:38:37,633 - app.services.agent.planning.response_builder - INFO - [Summarization] 准备发送 summarization_start 事件
2026-01-09 22:38:37,633 - app.services.agent.stream.stream_event_handler - INFO - [StreamEventHandler] emit_summarization_start 被调用, _on_flow_event=True
2026-01-09 22:38:37,633 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_start 事件已发送
2026-01-09 22:38:37,634 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2026-01-09 22:38:37,634 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2026-01-09 22:38:37,639 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-09 22:38:37,639 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-09 22:38:37,639 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
2026-01-09 22:38:57,415 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:64462 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 22:38:57,814 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-09 22:38:57,814 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_complete 事件已发送（第一个chunk时）
2026-01-09 22:38:57,816 - app.services.agent.planning.response_builder - INFO - [Summarization] output_ready 事件已发送（第一个chunk时）
2026-01-09 22:39:04,714 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 13 个数据块，总长度: 972
2026-01-09 22:39:04,714 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 6051 (prompt=5266, completion=785)
2026-01-09 22:39:04,715 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-09 22:39:04,715 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-09 22:39:04,732 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-09 22:39:04,732 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=6051, cost=$0.003542, time=27076ms
2026-01-09 22:39:04,732 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=972
2026-01-09 22:39:08,316 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:9f98efd6-1593-4967-ad43-f5dac759ac1c | 重要度=0.68
2026-01-09 22:39:12,500 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:9f98efd6-1593-4967-ad43-f5dac759ac1c | 重要度=0.73
2026-01-09 22:39:12,510 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:b2cee05e-5336-4ab7-8af6-60818c5f7583, token=1399
2026-01-09 22:39:12,513 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:b2cee05e-5336-4ab7-8af6-60818c5f7583, 消息数=2, Token=1399
2026-01-09 22:39:12,515 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:b2cee05e-5336-4ab7-8af6-60818c5f7583)
2026-01-09 22:39:12,517 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2026-01-09 22:39:12,527 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed
2026-01-09 22:39:27,420 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:52149 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 22:39:38,851 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-09 22:39:38,851 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-09 22:39:38,851 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2026-01-09 22:39:40,429 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-09 22:39:40,432 - app.api.v1.agent - INFO - [Chat Stream] Mode: planning
2026-01-09 22:39:40,434 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:64683 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2026-01-09 22:39:40,441 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 分析这部小说前三章的写作风格特点，学习作者的文风，然后给我一份风格指导，告诉我如何保持与原作一致的写...
2026-01-09 22:39:40,447 - app.api.v1.agent - INFO - [agent_chat_stream] 📚 世界观数据已注入: 人物=9, 地点=6, 设定=6, 规范=无
2026-01-09 22:39:40,448 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:b2cee05e-5336-4ab7-8af6-60818c5f7583 (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=9f98efd6-1593-4967-ad43-f5dac759ac1c, conversation_id=b2cee05e-5336-4ab7-8af6-60818c5f7583)
2026-01-09 22:39:40,451 - app.services.context.store - INFO - [ContextStore] 加载上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:b2cee05e-5336-4ab7-8af6-60818c5f7583, 2条消息
2026-01-09 22:39:40,451 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:b2cee05e-5336-4ab7-8af6-60818c5f7583: 1399/16000 tokens
2026-01-09 22:39:40,551 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='分析这部小说前三章的写作风格特点，学习作者的文风，然后给我一...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:9f98efd6-1593-4967-ad43-f5dac759ac1c', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=3条
2026-01-09 22:39:40,551 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=9f98efd6-1593-4967-ad43-f5dac759ac1c | 含用户级=True | 找到=3条
2026-01-09 22:39:40,556 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 3条消息, 1399 tokens, 耗时 108.09ms
2026-01-09 22:39:40,556 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 3 条历史消息 (token: 1399)
2026-01-09 22:39:40,556 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-09 22:39:40,558 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-09 22:39:40,558 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=20, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-09 22:39:42,151 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-09 22:39:42,151 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-09 22:39:42,160 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-09 22:39:42,162 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=316, cost=$0.000032, time=1592ms
2026-01-09 22:39:42,162 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=7, 尝试次数=1
2026-01-09 22:39:42,162 - app.services.agent.intent.classifier - INFO - [Intent] AI识别结果: writing
2026-01-09 22:39:42,162 - app.services.agent.langgraph_agent - INFO - [Planning] AI意图分类: writing (置信度: 0.90)
2026-01-09 22:39:42,162 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 分析这部小说前三章的写作风格特点，学习作者的文风，然后给我一份风格指导，告诉我如何保持与原作一致的写...
2026-01-09 22:39:42,167 - app.core.cache - INFO - ✅ 缓存命中: prompt:planning:v2.36.0:get_planning_static_prompt:fca6eb91156619d0
2026-01-09 22:39:42,170 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-09 22:39:42,170 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=story_planning, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: story_planning; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-01-09 22:39:42,172 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.3, task_type=TaskType.STORY_PLANNING
2026-01-09 22:39:57,801 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-09 22:39:58,050 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:61462 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 22:40:02,455 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 10 个数据块，总长度: 1356
2026-01-09 22:40:02,455 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 14466 (prompt=13837, completion=629)
2026-01-09 22:40:02,456 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-09 22:40:02,456 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-09 22:40:02,469 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-09 22:40:02,470 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=14466, cost=$0.023586, time=20284ms
2026-01-09 22:40:02,470 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=14466
2026-01-09 22:40:02,471 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户需要两部分内容：1. 对前三章写作风格的分析报告。2. , 原料=要完成这个任务，我需要读取小说前三章的全, 处理=1. 使用 `get_chapter_b
2026-01-09 22:40:02,474 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共3个任务
2026-01-09 22:40:02,474 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共3个任务，耗时: 20.31s
2026-01-09 22:40:02,475 - app.api.v1.agent - INFO - [Stream] Plan tasks: 3 items
2026-01-09 22:40:02,475 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2026-01-09 22:40:02,476 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2026-01-09 22:40:02,477 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2026-01-09 22:40:02,478 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 任务分组: 第一层并行=1, 第二层并行=0, 串行=2
2026-01-09 22:40:02,479 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始第一层并行执行1个任务
2026-01-09 22:40:02,479 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务1开始: 使用 get_chapter_by_order_tool 批量读取第1、2、3章的完整内容，作为风格分析的样本。
2026-01-09 22:40:02,480 - app.api.v1.agent - INFO - [Stream] Task started: 使用 get_chapter_by_order_tool 批量读取第1、2、3章的完整内容，作为风格分析的样本。 (icon=FileText)
2026-01-09 22:40:02,480 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(get_chapter_by_order)
2026-01-09 22:40:02,481 - app.services.agent.tools.tool_types - INFO - [get_chapter_by_order] 开始执行工具
2026-01-09 22:40:02,505 - app.services.agent.langgraph_tools - INFO - [get_chapter_by_order_tool] ✅ 批量读取成功: 共 3 章
2026-01-09 22:40:02,508 - app.services.agent.tools.tool_types - INFO - [get_chapter_by_order] 执行成功 (耗时: 0.027s)
2026-01-09 22:40:02,509 - app.services.agent.execution.task_runner - INFO - [TaskRunner] get_chapter_by_order 执行成功（DeepAgent模式）
2026-01-09 22:40:02,509 - app.api.v1.agent - INFO - [Stream] 任务完成: 使用 get_chapter_by_order_tool 批量读取第1、2、3章的完整内容，作为风格分析的样本。 (0.0s)
2026-01-09 22:40:02,509 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务1完成
2026-01-09 22:40:02,510 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始串行执行2个任务
2026-01-09 22:40:02,511 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务2开始: 将前三章内容合并，调用 analyze_style_tool 分析其在句式、用词、节奏和描写手法上的特点。
2026-01-09 22:40:02,512 - app.api.v1.agent - INFO - [Stream] Task started: 将前三章内容合并，调用 analyze_style_tool 分析其在句式、用词、节奏和描写手法上的特点。 (icon=Wrench)
2026-01-09 22:40:02,513 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: analyze_style_tool
2026-01-09 22:40:02,514 - app.services.agent.execution.tool_executor - WARNING - [StandardTool] 'analyze_style_tool' 不存在，降级到 @tool: 工具 'analyze_style_tool' 不存在
可用的 StandardTool: ['expand_text', 'analyze_content', 'analyze_text', 'evaluate_quality', 'smart_rewrite', 'smart_continue', 'smart_insert', 'apply_chapter_edit', 'get_context', 'read_chapter', 'get_chapter_by_order', 'search_analysis_fragments', 'get_worldview_summary', 'check_story_consistency']
可用的 DynamicTool: []
2026-01-09 22:40:02,514 - app.services.agent.execution.tool_executor - INFO - [LegacyTool] 使用 @tool 版本: analyze_style_tool
2026-01-09 22:40:02,522 - app.api.v1.agent - INFO - [Stream] 任务完成: 将前三章内容合并，调用 analyze_style_tool 分析其在句式、用词、节奏和描写手法上的特点。 (0.0s)
2026-01-09 22:40:02,523 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务2完成
2026-01-09 22:40:02,523 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务3开始: 基于作品的整体风格，调用 get_style_guidance_tool 生成一份具体的写作指导，帮助用户在后续创作中保持文风一致。
2026-01-09 22:40:02,524 - app.api.v1.agent - INFO - [Stream] Task started: 基于作品的整体风格，调用 get_style_guidance_tool 生成一份具体的写作指导，帮助用户在后续创作中保持文风一致。 (icon=Wrench)
2026-01-09 22:40:02,525 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: get_style_guidance_tool
2026-01-09 22:40:02,525 - app.services.agent.execution.tool_executor - WARNING - [StandardTool] 'get_style_guidance_tool' 不存在，降级到 @tool: 工具 'get_style_guidance_tool' 不存在
可用的 StandardTool: ['expand_text', 'analyze_content', 'analyze_text', 'evaluate_quality', 'smart_rewrite', 'smart_continue', 'smart_insert', 'apply_chapter_edit', 'get_context', 'read_chapter', 'get_chapter_by_order', 'search_analysis_fragments', 'get_worldview_summary', 'check_story_consistency']
可用的 DynamicTool: []
2026-01-09 22:40:02,525 - app.services.agent.execution.tool_executor - INFO - [LegacyTool] 使用 @tool 版本: get_style_guidance_tool
2026-01-09 22:40:02,528 - app.api.v1.agent - INFO - [Stream] 任务完成: 基于作品的整体风格，调用 get_style_guidance_tool 生成一份具体的写作指导，帮助用户在后续创作中保持文风一致。 (0.0s)
2026-01-09 22:40:02,528 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务3完成
2026-01-09 22:40:02,529 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共3个任务，耗时: 0.05s
2026-01-09 22:40:02,529 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2026-01-09 22:40:02,531 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=1, 输出型=2, 展示型=0
2026-01-09 22:40:02,531 - app.services.agent.langgraph_agent - INFO - [Response] 2个输出任务（含续写），使用AI整合
2026-01-09 22:40:02,532 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2026-01-09 22:40:02,532 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=1, 输出型=2, 展示型=0
2026-01-09 22:40:02,534 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=8415字符, 处理后=673字符
2026-01-09 22:40:02,534 - app.services.agent.planning.response_builder - INFO - [Summarization] 准备发送 summarization_start 事件
2026-01-09 22:40:02,534 - app.services.agent.stream.stream_event_handler - INFO - [StreamEventHandler] emit_summarization_start 被调用, _on_flow_event=True
2026-01-09 22:40:02,534 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_start 事件已发送
2026-01-09 22:40:02,536 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2026-01-09 22:40:02,537 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2026-01-09 22:40:02,546 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-09 22:40:02,546 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-09 22:40:02,546 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
2026-01-09 22:40:09,901 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-09 22:40:09,903 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_complete 事件已发送（第一个chunk时）
2026-01-09 22:40:09,903 - app.services.agent.planning.response_builder - INFO - [Summarization] output_ready 事件已发送（第一个chunk时）
2026-01-09 22:40:14,841 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 18 个数据块，总长度: 1299
2026-01-09 22:40:14,842 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 2876 (prompt=2007, completion=869)
2026-01-09 22:40:14,842 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-09 22:40:14,842 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-09 22:40:14,861 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-09 22:40:14,863 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2876, cost=$0.002775, time=12300ms
2026-01-09 22:40:14,863 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=1299
2026-01-09 22:40:18,076 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:9f98efd6-1593-4967-ad43-f5dac759ac1c | 重要度=0.68
2026-01-09 22:40:22,185 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:9f98efd6-1593-4967-ad43-f5dac759ac1c | 重要度=0.73
2026-01-09 22:40:22,202 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:b2cee05e-5336-4ab7-8af6-60818c5f7583, token=2795
2026-01-09 22:40:22,208 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:b2cee05e-5336-4ab7-8af6-60818c5f7583, 消息数=4, Token=2795
2026-01-09 22:40:22,209 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:b2cee05e-5336-4ab7-8af6-60818c5f7583)
2026-01-09 22:40:22,211 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2026-01-09 22:40:22,221 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed
2026-01-09 22:40:28,065 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:58023 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 22:40:49,790 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-09 22:40:49,790 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-09 22:40:49,790 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2026-01-09 22:40:51,174 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-09 22:40:51,174 - app.api.v1.agent - INFO - [Chat Stream] Mode: planning
2026-01-09 22:40:51,177 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:62369 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2026-01-09 22:40:51,182 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 查看这部小说的世界观设定，包括器灵等阶系统、精神力等级、源顺镖局的人物关系，然后检查前三章是否存在设...
2026-01-09 22:40:51,188 - app.api.v1.agent - INFO - [agent_chat_stream] 📚 世界观数据已注入: 人物=9, 地点=6, 设定=6, 规范=无
2026-01-09 22:40:51,189 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:b2cee05e-5336-4ab7-8af6-60818c5f7583 (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=9f98efd6-1593-4967-ad43-f5dac759ac1c, conversation_id=b2cee05e-5336-4ab7-8af6-60818c5f7583)
2026-01-09 22:40:51,193 - app.services.context.store - INFO - [ContextStore] 加载上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:b2cee05e-5336-4ab7-8af6-60818c5f7583, 4条消息
2026-01-09 22:40:51,196 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:b2cee05e-5336-4ab7-8af6-60818c5f7583: 2795/16000 tokens
2026-01-09 22:40:51,314 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='查看这部小说的世界观设定，包括器灵等阶系统、精神力等级、源顺...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:9f98efd6-1593-4967-ad43-f5dac759ac1c', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=3条
2026-01-09 22:40:51,314 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=9f98efd6-1593-4967-ad43-f5dac759ac1c | 含用户级=True | 找到=3条
2026-01-09 22:40:51,353 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 5条消息, 2795 tokens, 耗时 163.98ms
2026-01-09 22:40:51,353 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 5 条历史消息 (token: 2795)
2026-01-09 22:40:51,353 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-09 22:40:51,355 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-09 22:40:51,355 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=20, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-09 22:40:52,479 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-09 22:40:52,481 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-09 22:40:52,498 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-09 22:40:52,500 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=318, cost=$0.000032, time=1128ms
2026-01-09 22:40:52,502 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=8, 尝试次数=1
2026-01-09 22:40:52,502 - app.services.agent.intent.classifier - INFO - [Intent] AI识别结果: analysis
2026-01-09 22:40:52,503 - app.services.agent.langgraph_agent - INFO - [Planning] AI意图分类: analysis (置信度: 0.90)
2026-01-09 22:40:52,503 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 查看这部小说的世界观设定，包括器灵等阶系统、精神力等级、源顺镖局的人物关系，然后检查前三章是否存在设...
2026-01-09 22:40:52,509 - app.core.cache - INFO - ✅ 缓存命中: prompt:planning:v2.36.0:get_planning_static_prompt:fca6eb91156619d0
2026-01-09 22:40:52,513 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-09 22:40:52,513 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=story_planning, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: story_planning; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-01-09 22:40:52,514 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.3, task_type=TaskType.STORY_PLANNING
2026-01-09 22:40:58,845 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:63825 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 22:41:01,032 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-09 22:41:04,518 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 9 个数据块，总长度: 1154
2026-01-09 22:41:04,518 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 14670 (prompt=14101, completion=569)
2026-01-09 22:41:04,519 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-09 22:41:04,520 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-09 22:41:04,527 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-09 22:41:04,530 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=14670, cost=$0.023316, time=12005ms
2026-01-09 22:41:04,531 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=14670
2026-01-09 22:41:04,531 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户需要一份关于小说前三章设定矛盾或逻辑漏洞的分析报告。, 原料=要完成这个任务，需要：1. 小说的世界观, 处理=首先，调用工具获取完整的世界观设定。然后
2026-01-09 22:41:04,531 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共3个任务
2026-01-09 22:41:04,531 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共3个任务，耗时: 12.03s
2026-01-09 22:41:04,531 - app.api.v1.agent - INFO - [Stream] Plan tasks: 3 items
2026-01-09 22:41:04,533 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2026-01-09 22:41:04,533 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2026-01-09 22:41:04,534 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2026-01-09 22:41:04,534 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 任务分组: 第一层并行=1, 第二层并行=0, 串行=2
2026-01-09 22:41:04,534 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始第一层并行执行1个任务
2026-01-09 22:41:04,534 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务2开始: 批量读取小说第一章至第三章的全部内容，为逻辑检查做准备。
2026-01-09 22:41:04,536 - app.api.v1.agent - INFO - [Stream] Task started: 批量读取小说第一章至第三章的全部内容，为逻辑检查做准备。 (icon=FileText)
2026-01-09 22:41:04,536 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(get_chapter_by_order)
2026-01-09 22:41:04,536 - app.services.agent.tools.tool_types - INFO - [get_chapter_by_order] 开始执行工具
2026-01-09 22:41:04,558 - app.services.agent.langgraph_tools - INFO - [get_chapter_by_order_tool] ✅ 批量读取成功: 共 3 章
2026-01-09 22:41:04,560 - app.services.agent.tools.tool_types - INFO - [get_chapter_by_order] 执行成功 (耗时: 0.023s)
2026-01-09 22:41:04,560 - app.services.agent.execution.task_runner - INFO - [TaskRunner] get_chapter_by_order 执行成功（DeepAgent模式）
2026-01-09 22:41:04,561 - app.api.v1.agent - INFO - [Stream] 任务完成: 批量读取小说第一章至第三章的全部内容，为逻辑检查做准备。 (0.0s)
2026-01-09 22:41:04,561 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务2完成
2026-01-09 22:41:04,562 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始串行执行2个任务
2026-01-09 22:41:04,562 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务1开始: 查询作品的世界观设定，包括器灵等阶系统、精神力等级、源顺镖局人物关系等。
2026-01-09 22:41:04,563 - app.api.v1.agent - INFO - [Stream] Task started: 查询作品的世界观设定，包括器灵等阶系统、精神力等级、源顺镖局人物关系等。 (icon=Wrench)
2026-01-09 22:41:04,563 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: get_worldview_summary
2026-01-09 22:41:04,563 - app.services.agent.tools.tool_types - INFO - [get_worldview_summary] 开始执行工具
2026-01-09 22:41:04,579 - app.services.agent.langgraph_tools - INFO - [get_worldview_summary] ✅ 获取世界观摘要成功: {'characters': 9, 'locations': 6, 'settings': 6}
2026-01-09 22:41:04,581 - app.services.agent.tools.tool_types - INFO - [get_worldview_summary] 执行成功 (耗时: 0.018s)
2026-01-09 22:41:04,581 - app.services.agent.execution.tool_executor - INFO - [StandardTool] get_worldview_summary 执行成功
2026-01-09 22:41:04,583 - app.api.v1.agent - INFO - [Stream] 任务完成: 查询作品的世界观设定，包括器灵等阶系统、精神力等级、源顺镖局人物关系等。 (0.0s)
2026-01-09 22:41:04,583 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务1完成
2026-01-09 22:41:04,583 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务3开始: 基于获取的世界观和章节内容，检查前三章是否存在设定矛盾或逻辑漏洞。
2026-01-09 22:41:04,583 - app.api.v1.agent - INFO - [Stream] Task started: 基于获取的世界观和章节内容，检查前三章是否存在设定矛盾或逻辑漏洞。 (icon=Wrench)
2026-01-09 22:41:04,585 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: check_story_consistency_tool
2026-01-09 22:41:04,585 - app.services.agent.execution.tool_executor - WARNING - [StandardTool] 'check_story_consistency_tool' 不存在，降级到 @tool: 工具 'check_story_consistency_tool' 不存在
可用的 StandardTool: ['expand_text', 'analyze_content', 'analyze_text', 'evaluate_quality', 'smart_rewrite', 'smart_continue', 'smart_insert', 'apply_chapter_edit', 'get_context', 'read_chapter', 'get_chapter_by_order', 'search_analysis_fragments', 'get_worldview_summary', 'check_story_consistency']
可用的 DynamicTool: []
2026-01-09 22:41:04,585 - app.services.agent.execution.tool_executor - INFO - [LegacyTool] 使用 @tool 版本: check_story_consistency_tool
2026-01-09 22:41:04,587 - app.api.v1.agent - INFO - [Stream] 任务完成: 基于获取的世界观和章节内容，检查前三章是否存在设定矛盾或逻辑漏洞。 (0.0s)
2026-01-09 22:41:04,587 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务3完成
2026-01-09 22:41:04,587 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共3个任务，耗时: 0.05s
2026-01-09 22:41:04,587 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2026-01-09 22:41:04,589 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=2, 输出型=1, 展示型=0
2026-01-09 22:41:04,590 - app.services.agent.langgraph_agent - INFO - [Response] 单个输出任务(check_story_consistency_tool)，使用AI整合
2026-01-09 22:41:04,590 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2026-01-09 22:41:04,590 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=2, 输出型=1, 展示型=0
2026-01-09 22:41:04,591 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=11517字符, 处理后=2369字符
2026-01-09 22:41:04,591 - app.services.agent.planning.response_builder - INFO - [Summarization] 准备发送 summarization_start 事件
2026-01-09 22:41:04,592 - app.services.agent.stream.stream_event_handler - INFO - [StreamEventHandler] emit_summarization_start 被调用, _on_flow_event=True
2026-01-09 22:41:04,592 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_start 事件已发送
2026-01-09 22:41:04,592 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2026-01-09 22:41:04,592 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2026-01-09 22:41:04,600 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-09 22:41:04,600 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-09 22:41:04,602 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
2026-01-09 22:41:14,937 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-09 22:41:14,937 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_complete 事件已发送（第一个chunk时）
2026-01-09 22:41:14,937 - app.services.agent.planning.response_builder - INFO - [Summarization] output_ready 事件已发送（第一个chunk时）
2026-01-09 22:41:19,761 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 15 个数据块，总长度: 1490
2026-01-09 22:41:19,763 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 4260 (prompt=3311, completion=949)
2026-01-09 22:41:19,763 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-09 22:41:19,763 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-09 22:41:19,782 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-09 22:41:19,782 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4260, cost=$0.003366, time=15161ms
2026-01-09 22:41:19,784 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=1490
2026-01-09 22:41:24,004 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:9f98efd6-1593-4967-ad43-f5dac759ac1c | 重要度=0.89
2026-01-09 22:41:28,316 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:9f98efd6-1593-4967-ad43-f5dac759ac1c | 重要度=0.94
2026-01-09 22:41:28,333 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:b2cee05e-5336-4ab7-8af6-60818c5f7583, token=4296
2026-01-09 22:41:28,341 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:b2cee05e-5336-4ab7-8af6-60818c5f7583, 消息数=6, Token=4296
2026-01-09 22:41:28,343 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:b2cee05e-5336-4ab7-8af6-60818c5f7583)
2026-01-09 22:41:28,344 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2026-01-09 22:41:28,355 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed
2026-01-09 22:41:28,873 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:58546 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 22:41:58,872 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:57025 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 22:42:28,884 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:60277 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 22:42:58,902 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:63835 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 22:43:28,913 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:60675 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 22:43:51,766 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-09 22:43:51,766 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-09 22:43:51,766 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2026-01-09 22:43:53,169 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-09 22:43:53,170 - app.api.v1.agent - INFO - [Chat Stream] Mode: planning
2026-01-09 22:43:53,174 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:50732 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2026-01-09 22:43:53,179 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 搜索赵穆出现的所有场景，分析他的人物形象塑造是否立体，然后帮我改写第1章中赵穆第一次出场的描写，让他...
2026-01-09 22:43:53,187 - app.api.v1.agent - INFO - [agent_chat_stream] 📚 世界观数据已注入: 人物=9, 地点=6, 设定=6, 规范=无
2026-01-09 22:43:53,187 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:b2cee05e-5336-4ab7-8af6-60818c5f7583 (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=9f98efd6-1593-4967-ad43-f5dac759ac1c, conversation_id=b2cee05e-5336-4ab7-8af6-60818c5f7583)
2026-01-09 22:43:53,190 - app.services.context.store - INFO - [ContextStore] 加载上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:b2cee05e-5336-4ab7-8af6-60818c5f7583, 6条消息
2026-01-09 22:43:53,192 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:b2cee05e-5336-4ab7-8af6-60818c5f7583: 4296/16000 tokens
2026-01-09 22:43:53,351 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='搜索赵穆出现的所有场景，分析他的人物形象塑造是否立体，然后帮...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:9f98efd6-1593-4967-ad43-f5dac759ac1c', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=3条
2026-01-09 22:43:53,352 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=9f98efd6-1593-4967-ad43-f5dac759ac1c | 含用户级=True | 找到=3条
2026-01-09 22:43:53,575 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 7条消息, 4296 tokens, 耗时 387.08ms
2026-01-09 22:43:53,575 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 7 条历史消息 (token: 4296)
2026-01-09 22:43:53,575 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-09 22:43:53,575 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-09 22:43:53,575 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=20, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-09 22:43:55,098 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-09 22:43:55,100 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-09 22:43:55,119 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-09 22:43:55,121 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=317, cost=$0.000032, time=1525ms
2026-01-09 22:43:55,121 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=7, 尝试次数=1
2026-01-09 22:43:55,121 - app.services.agent.intent.classifier - INFO - [Intent] AI识别结果: writing
2026-01-09 22:43:55,121 - app.services.agent.langgraph_agent - INFO - [Planning] AI意图分类: writing (置信度: 0.90)
2026-01-09 22:43:55,121 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 搜索赵穆出现的所有场景，分析他的人物形象塑造是否立体，然后帮我改写第1章中赵穆第一次出场的描写，让他...
2026-01-09 22:43:55,130 - app.core.cache - INFO - ✅ 缓存命中: prompt:planning:v2.36.0:get_planning_static_prompt:fca6eb91156619d0
2026-01-09 22:43:55,137 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-09 22:43:55,137 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=story_planning, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: story_planning; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-01-09 22:43:55,137 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.3, task_type=TaskType.STORY_PLANNING
2026-01-09 22:43:58,920 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:58008 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 22:44:08,521 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-09 22:44:14,388 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 13 个数据块，总长度: 1718
2026-01-09 22:44:14,388 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 16449 (prompt=15638, completion=811)
2026-01-09 22:44:14,388 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-09 22:44:14,388 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-09 22:44:14,401 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-09 22:44:14,401 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=16449, cost=$0.027657, time=19250ms
2026-01-09 22:44:14,401 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=16449
2026-01-09 22:44:14,401 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户期望得到一个包含三部分的输出：1. 对角色“赵穆”的分析, 原料=要完成这个任务，需要以下原料：1. 所有, 处理=处理流程分为三步：1. 使用`searc
2026-01-09 22:44:14,401 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共4个任务
2026-01-09 22:44:14,401 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共4个任务，耗时: 19.28s
2026-01-09 22:44:14,401 - app.api.v1.agent - INFO - [Stream] Plan tasks: 4 items
2026-01-09 22:44:14,405 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2026-01-09 22:44:14,405 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2026-01-09 22:44:14,405 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2026-01-09 22:44:14,405 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 任务分组: 第一层并行=2, 第二层并行=1, 串行=1
2026-01-09 22:44:14,405 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始第一层并行执行2个任务
2026-01-09 22:44:14,405 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务1开始: 在整个作品中搜索角色“赵穆”出现的所有场景。
2026-01-09 22:44:14,405 - app.api.v1.agent - INFO - [Stream] Task started: 在整个作品中搜索角色“赵穆”出现的所有场景。 (icon=Search)
2026-01-09 22:44:14,405 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(search_analysis_fragments)
2026-01-09 22:44:14,410 - app.services.agent.tools.tool_types - INFO - [search_analysis_fragments] 开始执行工具
2026-01-09 22:44:14,411 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务3开始: 获取第1章的完整内容，用于定位赵穆首次出场的段落。
2026-01-09 22:44:14,411 - app.api.v1.agent - INFO - [Stream] Task started: 获取第1章的完整内容，用于定位赵穆首次出场的段落。 (icon=FileText)
2026-01-09 22:44:14,411 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(get_chapter_by_order)
2026-01-09 22:44:14,413 - app.services.agent.tools.tool_types - INFO - [get_chapter_by_order] 开始执行工具
2026-01-09 22:44:14,416 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=9f98efd6-1593-4967-ad43-f5dac759ac1c, current_order=3, query=赵穆...
2026-01-09 22:44:14,479 - app.services.agent.langgraph_tools - INFO - [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
2026-01-09 22:44:14,482 - app.services.agent.tools.tool_types - INFO - [get_chapter_by_order] 执行成功 (耗时: 0.069s)
2026-01-09 22:44:14,482 - app.services.agent.execution.task_runner - INFO - [TaskRunner] get_chapter_by_order 执行成功（DeepAgent模式）
2026-01-09 22:44:14,482 - app.api.v1.agent - INFO - [Stream] 任务完成: 获取第1章的完整内容，用于定位赵穆首次出场的段落。 (0.1s)
2026-01-09 22:44:14,482 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务3完成
2026-01-09 22:44:14,492 - app.services.chapter_vector_service - INFO - RAG retrieved 10 segments within order<=5
2026-01-09 22:44:14,500 - app.services.agent.langgraph_tools - INFO - [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
2026-01-09 22:44:14,500 - app.services.agent.tools.tool_types - INFO - [search_analysis_fragments] 执行成功 (耗时: 0.090s)
2026-01-09 22:44:14,500 - app.services.agent.execution.task_runner - INFO - [TaskRunner] search_analysis_fragments 执行成功（DeepAgent模式）
2026-01-09 22:44:14,500 - app.api.v1.agent - INFO - [Stream] 任务完成: 在整个作品中搜索角色“赵穆”出现的所有场景。 (0.1s)
2026-01-09 22:44:14,500 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务1完成
2026-01-09 22:44:14,500 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始第二层并行执行1个任务
2026-01-09 22:44:14,500 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第二层任务2开始: 基于搜索到的所有相关片段，分析赵穆的人物形象塑造是否立体。
2026-01-09 22:44:14,500 - app.api.v1.agent - INFO - [Stream] Task started: 基于搜索到的所有相关片段，分析赵穆的人物形象塑造是否立体。 (icon=BarChart2)
2026-01-09 22:44:14,500 - app.services.agent.execution.task_runner - INFO - [TaskRunner] analyze_text_tool 使用 focus: '分析赵穆的人物形象塑造是否立体...'
2026-01-09 22:44:14,505 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(analyze_text)
2026-01-09 22:44:14,505 - app.services.agent.tools.tool_types - INFO - [analyze_text] 开始执行工具
2026-01-09 22:44:14,506 - app.services.agent.tools.analysis_tools - INFO - [analyze_text_tool] 尝试第 1 次调用，config={'temperature': 0.3, 'task_type': <TaskType.SUMMARIZATION: 'summarization'>}
2026-01-09 22:44:14,511 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-09 22:44:14,511 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-09 22:44:14,511 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
2026-01-09 22:44:21,500 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-09 22:44:23,804 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 8 个数据块，总长度: 488
2026-01-09 22:44:23,804 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 3973 (prompt=3614, completion=359)
2026-01-09 22:44:23,804 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-09 22:44:23,804 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-09 22:44:23,823 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-09 22:44:23,823 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=3973, cost=$0.001982, time=9295ms
2026-01-09 22:44:23,826 - app.services.agent.tools.analysis_tools - INFO - [analyze_text_tool] 第 1 次调用成功
2026-01-09 22:44:23,826 - app.services.agent.tools.analysis_tools - INFO - [analyze_text_tool] 分析完成，结果长度: 488
2026-01-09 22:44:23,826 - app.services.agent.tools.tool_types - INFO - [analyze_text] 执行成功 (耗时: 9.320s)
2026-01-09 22:44:23,826 - app.services.agent.execution.task_runner - INFO - [TaskRunner] analyze_text 执行成功（DeepAgent模式）
2026-01-09 22:44:23,826 - app.api.v1.agent - INFO - [Stream] 任务完成: 基于搜索到的所有相关片段，分析赵穆的人物形象塑造是否立体。 (9.3s)
2026-01-09 22:44:23,826 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第二层任务2完成
2026-01-09 22:44:23,829 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始串行执行1个任务
2026-01-09 22:44:23,830 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务4开始: 改写第1章中赵穆第一次出场的描写，使其性格特点更加鲜明。
2026-01-09 22:44:23,830 - app.api.v1.agent - INFO - [Stream] Task started: 改写第1章中赵穆第一次出场的描写，使其性格特点更加鲜明。 (icon=Edit3)
2026-01-09 22:44:23,830 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: smart_rewrite
2026-01-09 22:44:23,830 - app.services.agent.tools.tool_types - INFO - [smart_rewrite] 开始执行工具
2026-01-09 22:44:23,839 - app.services.agent.tools.editor_tools - INFO - [smart_rewrite] 开始生成改写版本，原文长度: 2476, 用户要求: 改写第1章中赵穆第一次出场的描写，让他的性格特点更加鲜明, 基准版本: 无
2026-01-09 22:44:23,839 - app.services.agent.tools.editor_tools - INFO - [smart_rewrite] 使用传统单Prompt架构
2026-01-09 22:44:23,840 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-09 22:44:23,841 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=content_creation, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro
2026-01-09 22:44:23,841 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=4000, temp=0.8, 尝试=1/3, task_type=TaskType.CONTENT_CREATION
2026-01-09 22:44:29,029 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:55576 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 22:44:59,024 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:65450 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 22:45:17,500 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-09 22:45:17,500 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-09 22:45:17,516 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-09 22:45:17,516 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=8609, cost=$0.032111, time=53658ms
2026-01-09 22:45:17,516 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=3167, 尝试次数=1
2026-01-09 22:45:17,516 - app.services.agent.tools.editor_tools - INFO - [smart_rewrite] AI返回长度: 3167
2026-01-09 22:45:17,516 - app.services.agent.tools.editor_tools - INFO - [smart_rewrite] 成功生成3个改写版本
2026-01-09 22:45:17,516 - app.services.agent.tools.tool_types - INFO - [smart_rewrite] 执行成功 (耗时: 53.685s)
2026-01-09 22:45:17,516 - app.services.agent.execution.tool_executor - INFO - [StandardTool] smart_rewrite 执行成功
2026-01-09 22:45:17,516 - app.api.v1.agent - INFO - [Stream] 任务完成: 改写第1章中赵穆第一次出场的描写，使其性格特点更加鲜明。 (53.7s)
2026-01-09 22:45:17,516 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务4完成
2026-01-09 22:45:17,516 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共4个任务，耗时: 63.11s
2026-01-09 22:45:17,525 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2026-01-09 22:45:17,526 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=2, 输出型=2, 展示型=0
2026-01-09 22:45:17,526 - app.services.agent.langgraph_agent - INFO - [Response] 2个输出任务（含续写），使用AI整合
2026-01-09 22:45:17,526 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2026-01-09 22:45:17,528 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=2, 输出型=2, 展示型=0
2026-01-09 22:45:17,528 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=12422字符, 处理后=5952字符
2026-01-09 22:45:17,528 - app.services.agent.planning.response_builder - INFO - [Summarization] 准备发送 summarization_start 事件
2026-01-09 22:45:17,528 - app.services.agent.stream.stream_event_handler - INFO - [StreamEventHandler] emit_summarization_start 被调用, _on_flow_event=True
2026-01-09 22:45:17,528 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_start 事件已发送
2026-01-09 22:45:17,531 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2026-01-09 22:45:17,531 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2026-01-09 22:45:17,537 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-09 22:45:17,537 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-09 22:45:17,537 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
2026-01-09 22:45:29,033 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:58605 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 22:45:35,179 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-09 22:45:35,180 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_complete 事件已发送（第一个chunk时）
2026-01-09 22:45:35,180 - app.services.agent.planning.response_builder - INFO - [Summarization] output_ready 事件已发送（第一个chunk时）
2026-01-09 22:45:59,069 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:54485 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 22:46:00,006 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 102 个数据块，总长度: 168527
2026-01-09 22:46:00,006 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 14459 (prompt=7769, completion=6690)
2026-01-09 22:46:00,006 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-09 22:46:00,006 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-09 22:46:00,034 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-09 22:46:00,039 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=14459, cost=$0.019056, time=42466ms
2026-01-09 22:46:00,041 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=168527
2026-01-09 22:46:04,225 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:9f98efd6-1593-4967-ad43-f5dac759ac1c | 重要度=1.00
2026-01-09 22:46:08,351 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:9f98efd6-1593-4967-ad43-f5dac759ac1c | 重要度=0.77
2026-01-09 22:46:40,985 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:b2cee05e-5336-4ab7-8af6-60818c5f7583, token=7700
2026-01-09 22:47:05,706 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:b2cee05e-5336-4ab7-8af6-60818c5f7583, 消息数=8, Token=7700
2026-01-09 22:47:05,708 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:b2cee05e-5336-4ab7-8af6-60818c5f7583)
2026-01-09 22:47:05,708 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2026-01-09 22:47:05,718 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed
2026-01-09 22:47:05,730 - sqlalchemy.pool.impl.AsyncAdaptedQueuePool - ERROR - Exception terminating connection <AdaptedConnection <asyncpg.connection.Connection object at 0x000001DE71361B80>>
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\pool\base.py", line 377, in _close_connection
    self._dialect.do_terminate(connection)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 1109, in do_terminate
    dbapi_connection.terminate()
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 892, in terminate
    self.await_(self._connection.close(timeout=2))
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 130, in await_only
    return current.driver.switch(awaitable)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 195, in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\connection.py", line 1467, in close
    await self._protocol.close(timeout)
  File "asyncpg\protocol\protocol.pyx", line 641, in close
asyncio.exceptions.CancelledError: Cancelled via cancel scope 1deb8631fa0 by <Task pending name='starlette.middleware.base.BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro' coro=<BaseHTTPMiddleware.__call__.<locals>.call_next.<locals>.coro() running at D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\base.py:151> cb=[TaskGroup._spawn.<locals>.task_done() at D:\Java\ai_writer\backend\venv\Lib\site-packages\anyio\_backends\_asyncio.py:803]>
2026-01-09 22:47:05,773 - sqlalchemy.pool.impl.AsyncAdaptedQueuePool - ERROR - The garbage collector is trying to clean up non-checked-in connection <AdaptedConnection <asyncpg.connection.Connection object at 0x000001DE71361B80>>, which will be terminated.  Please ensure that SQLAlchemy pooled connections are returned to the pool explicitly, either by calling ``close()`` or by using appropriate context managers to manage their lifecycle.
C:\Program Files\Python312\Lib\asyncio\events.py:36: SAWarning: The garbage collector is trying to clean up non-checked-in connection <AdaptedConnection <asyncpg.connection.Connection object at 0x000001DE71361B80>>, which will be terminated.  Please ensure that SQLAlchemy pooled connections are returned to the pool explicitly, either by calling ``close()`` or by using appropriate context managers to manage their lifecycle.
  def __init__(self, callback, args, loop, context=None):
2026-01-09 22:47:05,813 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:59954 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 22:47:05,820 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:51986 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 22:47:12,196 - app.services.chapter_word_stat_service - INFO - 记录字数增量: chapter_id=cdabcd19-8562-4d6e-82b6-d37caae83a5d, delta=5, edit_event_id=1d864785-4859-4a58-86b6-6d19219bdf29
2026-01-09 22:47:12,201 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 cdabcd19-8562-4d6e-82b6-d37caae83a5d 内容更新，新段落数: 65
[TaskService] Checking daily writing task for user 79913e7e-d5cd-4e09-bce6-ca6639bd8456, word_count: 64
[TaskService] Daily writing task result: None
2026-01-09 22:47:12,258 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:9f98efd6-1593-4967-ad43-f5dac759ac1c
2026-01-09 22:47:12,259 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/cdabcd19-8562-4d6e-82b6-d37caae83a5d
INFO:     127.0.0.1:56601 - "PUT /api/v1/chapters/cdabcd19-8562-4d6e-82b6-d37caae83a5d HTTP/1.1" 200 OK
2026-01-09 22:47:12,263 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第3章 一夕千悟 (order=3)
2026-01-09 22:47:13,597 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第3章 一夕千悟 (5 chunks)
2026-01-09 22:47:13,645 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:9f98efd6-1593-4967-ad43-f5dac759ac1c
2026-01-09 22:47:13,649 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/cdabcd19-8562-4d6e-82b6-d37caae83a5d
INFO:     127.0.0.1:56605 - "PUT /api/v1/chapters/cdabcd19-8562-4d6e-82b6-d37caae83a5d HTTP/1.1" 200 OK
2026-01-09 22:47:13,653 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第3章 一夕千悟 (order=3)
2026-01-09 22:47:14,956 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第3章 一夕千悟 (5 chunks)
2026-01-09 22:47:20,026 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 cdabcd19-8562-4d6e-82b6-d37caae83a5d 内容更新，新段落数: 64
2026-01-09 22:47:20,048 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:9f98efd6-1593-4967-ad43-f5dac759ac1c
2026-01-09 22:47:20,050 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/cdabcd19-8562-4d6e-82b6-d37caae83a5d
INFO:     127.0.0.1:60074 - "PUT /api/v1/chapters/cdabcd19-8562-4d6e-82b6-d37caae83a5d HTTP/1.1" 200 OK
2026-01-09 22:47:20,052 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第3章 一夕千悟 (order=3)
2026-01-09 22:47:20,519 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第3章 一夕千悟 (5 chunks)
2026-01-09 22:47:20,553 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:9f98efd6-1593-4967-ad43-f5dac759ac1c
2026-01-09 22:47:20,555 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/cdabcd19-8562-4d6e-82b6-d37caae83a5d
INFO:     127.0.0.1:60077 - "PUT /api/v1/chapters/cdabcd19-8562-4d6e-82b6-d37caae83a5d HTTP/1.1" 200 OK
2026-01-09 22:47:20,558 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第3章 一夕千悟 (order=3)
2026-01-09 22:47:21,403 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第3章 一夕千悟 (5 chunks)
2026-01-09 22:47:29,198 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:61084 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 22:47:39,094 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-09 22:47:39,096 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-09 22:47:39,096 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2026-01-09 22:47:40,440 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-09 22:47:40,440 - app.api.v1.agent - INFO - [Chat Stream] Mode: planning
2026-01-09 22:47:40,448 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:49182 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2026-01-09 22:47:40,460 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 帮我创建第4章，标题叫"初露锋芒"，然后在章节开头插入一段承上启下的过渡内容，衔接第3章段融练刀的情...
2026-01-09 22:47:40,475 - app.api.v1.agent - INFO - [agent_chat_stream] 📚 世界观数据已注入: 人物=9, 地点=6, 设定=6, 规范=无
2026-01-09 22:47:40,475 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:b2cee05e-5336-4ab7-8af6-60818c5f7583 (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=9f98efd6-1593-4967-ad43-f5dac759ac1c, conversation_id=b2cee05e-5336-4ab7-8af6-60818c5f7583)
2026-01-09 22:47:40,508 - app.services.context.store - INFO - [ContextStore] 加载上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:b2cee05e-5336-4ab7-8af6-60818c5f7583, 8条消息
2026-01-09 22:47:57,764 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:b2cee05e-5336-4ab7-8af6-60818c5f7583: 7700/16000 tokens
2026-01-09 22:47:57,868 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='帮我创建第4章，标题叫"初露锋芒"，然后在章节开头插入一段承...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:9f98efd6-1593-4967-ad43-f5dac759ac1c', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=3条
2026-01-09 22:47:57,868 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=9f98efd6-1593-4967-ad43-f5dac759ac1c | 含用户级=True | 找到=3条
2026-01-09 22:48:13,217 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 9条消息, 7700 tokens, 耗时 32741.34ms
2026-01-09 22:48:13,217 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 9 条历史消息 (token: 7700)
2026-01-09 22:48:13,217 - app.services.agent.planning.quick_path - INFO - [QuickPath-Planning] 命中快速路径: get_chapter_info
2026-01-09 22:48:13,217 - app.services.agent.planning.quick_path - WARNING - [QuickPath-Planning] 执行失败: 'list' object has no attribute 'get'，降级到规划模式
2026-01-09 22:48:13,217 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-09 22:48:13,217 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-09 22:48:13,217 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=20, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-09 22:48:13,243 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:57892 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 22:48:14,459 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-09 22:48:14,460 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-09 22:48:14,477 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-09 22:48:14,480 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=327, cost=$0.000033, time=1243ms
2026-01-09 22:48:14,480 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=7, 尝试次数=1
2026-01-09 22:48:14,483 - app.services.agent.intent.classifier - INFO - [Intent] AI识别结果: writing
2026-01-09 22:48:14,483 - app.services.agent.langgraph_agent - INFO - [Planning] AI意图分类: writing (置信度: 0.90)
2026-01-09 22:48:14,484 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 帮我创建第4章，标题叫"初露锋芒"，然后在章节开头插入一段承上启下的过渡内容，衔接第3章段融练刀的情...
2026-01-09 22:48:14,489 - app.core.cache - INFO - ✅ 缓存命中: prompt:planning:v2.36.0:get_planning_static_prompt:fca6eb91156619d0
2026-01-09 22:48:14,495 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-09 22:48:14,497 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=story_planning, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: story_planning; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-01-09 22:48:14,497 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.3, task_type=TaskType.STORY_PLANNING
2026-01-09 22:48:30,003 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:59604 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 22:48:37,129 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-09 22:48:40,274 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 8 个数据块，总长度: 928
2026-01-09 22:48:40,275 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 23623 (prompt=23169, completion=454)
2026-01-09 22:48:40,275 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-09 22:48:40,275 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-09 22:48:40,281 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-09 22:48:40,291 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=23623, cost=$0.033501, time=25775ms
2026-01-09 22:48:40,291 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=23623
2026-01-09 22:48:40,291 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户需要一份关于小说世界观的总结报告，并对前三章进行逻辑一致, 原料=需要调用工具来获取已设定的世界观信息，并, 处理=1. 使用 `get_worldview
2026-01-09 22:48:40,291 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共2个任务
2026-01-09 22:48:40,291 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共2个任务，耗时: 25.81s
2026-01-09 22:48:40,291 - app.api.v1.agent - INFO - [Stream] Plan tasks: 2 items
2026-01-09 22:48:40,291 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2026-01-09 22:48:40,296 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2026-01-09 22:48:40,297 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2026-01-09 22:48:40,298 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 任务分组: 第一层并行=0, 第二层并行=0, 串行=2
2026-01-09 22:48:40,299 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始串行执行2个任务
2026-01-09 22:48:40,299 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务1开始: 查询并汇总作品的世界观设定，包括器灵等阶系统、精神力等级和源顺镖局的人物关系。
2026-01-09 22:48:40,300 - app.api.v1.agent - INFO - [Stream] Task started: 查询并汇总作品的世界观设定，包括器灵等阶系统、精神力等级和源顺镖局的人物关系。 (icon=Wrench)
2026-01-09 22:48:40,301 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: get_worldview_summary
2026-01-09 22:48:40,301 - app.services.agent.tools.tool_types - INFO - [get_worldview_summary] 开始执行工具
2026-01-09 22:48:40,313 - app.services.agent.langgraph_tools - INFO - [get_worldview_summary] ✅ 获取世界观摘要成功: {'characters': 9, 'locations': 6, 'settings': 6}
2026-01-09 22:48:40,316 - app.services.agent.tools.tool_types - INFO - [get_worldview_summary] 执行成功 (耗时: 0.015s)
2026-01-09 22:48:40,318 - app.services.agent.execution.tool_executor - INFO - [StandardTool] get_worldview_summary 执行成功
2026-01-09 22:48:40,318 - app.api.v1.agent - INFO - [Stream] 任务完成: 查询并汇总作品的世界观设定，包括器灵等阶系统、精神力等级和源顺镖局的人物关系。 (0.0s)
2026-01-09 22:48:40,320 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务1完成
2026-01-09 22:48:40,320 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务2开始: 分析小说前三章的内容，检查是否存在设定矛盾或逻辑漏洞。
2026-01-09 22:48:40,322 - app.api.v1.agent - INFO - [Stream] Task started: 分析小说前三章的内容，检查是否存在设定矛盾或逻辑漏洞。 (icon=Wrench)
2026-01-09 22:48:40,322 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: check_story_consistency_tool
2026-01-09 22:48:40,322 - app.services.agent.execution.tool_executor - WARNING - [StandardTool] 'check_story_consistency_tool' 不存在，降级到 @tool: 工具 'check_story_consistency_tool' 不存在
可用的 StandardTool: ['expand_text', 'analyze_content', 'analyze_text', 'evaluate_quality', 'smart_rewrite', 'smart_continue', 'smart_insert', 'apply_chapter_edit', 'get_context', 'read_chapter', 'get_chapter_by_order', 'search_analysis_fragments', 'get_worldview_summary', 'check_story_consistency']
可用的 DynamicTool: []
2026-01-09 22:48:40,322 - app.services.agent.execution.tool_executor - INFO - [LegacyTool] 使用 @tool 版本: check_story_consistency_tool
2026-01-09 22:48:40,326 - app.api.v1.agent - INFO - [Stream] 任务完成: 分析小说前三章的内容，检查是否存在设定矛盾或逻辑漏洞。 (0.0s)
2026-01-09 22:48:40,326 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务2完成
2026-01-09 22:48:40,326 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共2个任务，耗时: 0.03s
2026-01-09 22:48:40,326 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2026-01-09 22:48:40,328 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=1, 输出型=1, 展示型=0
2026-01-09 22:48:40,328 - app.services.agent.langgraph_agent - INFO - [Response] 单个输出任务(check_story_consistency_tool)，使用AI整合
2026-01-09 22:48:40,328 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2026-01-09 22:48:40,328 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=1, 输出型=1, 展示型=0
2026-01-09 22:48:40,330 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=3645字符, 处理后=2360字符
2026-01-09 22:48:40,330 - app.services.agent.planning.response_builder - INFO - [Summarization] 准备发送 summarization_start 事件
2026-01-09 22:48:40,330 - app.services.agent.stream.stream_event_handler - INFO - [StreamEventHandler] emit_summarization_start 被调用, _on_flow_event=True
2026-01-09 22:48:40,332 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_start 事件已发送
2026-01-09 22:48:40,332 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2026-01-09 22:48:40,332 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2026-01-09 22:48:40,338 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-09 22:48:40,338 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-09 22:48:40,340 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
2026-01-09 22:48:52,999 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-09 22:48:53,000 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_complete 事件已发送（第一个chunk时）
2026-01-09 22:48:53,000 - app.services.agent.planning.response_builder - INFO - [Summarization] output_ready 事件已发送（第一个chunk时）
2026-01-09 22:48:58,298 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 23 个数据块，总长度: 1645
2026-01-09 22:48:58,299 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 5210 (prompt=4108, completion=1102)
2026-01-09 22:48:58,301 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-09 22:48:58,303 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-09 22:48:58,328 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-09 22:48:58,331 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=5210, cost=$0.003987, time=17963ms
2026-01-09 22:48:58,334 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=1645
2026-01-09 22:49:03,394 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:9f98efd6-1593-4967-ad43-f5dac759ac1c | 重要度=1.00
2026-01-09 22:49:08,547 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:9f98efd6-1593-4967-ad43-f5dac759ac1c | 重要度=0.60
2026-01-09 22:49:45,379 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:b2cee05e-5336-4ab7-8af6-60818c5f7583, token=9467
2026-01-09 22:50:16,948 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:b2cee05e-5336-4ab7-8af6-60818c5f7583, 消息数=10, Token=9467
2026-01-09 22:50:16,948 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:b2cee05e-5336-4ab7-8af6-60818c5f7583)
2026-01-09 22:50:16,948 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2026-01-09 22:50:16,963 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed
2026-01-09 22:50:16,998 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:59493 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 22:50:16,998 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:58332 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 22:50:17,132 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:53748 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 22:50:30,210 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:57265 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 22:50:57,058 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-09 22:50:57,059 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-09 22:50:57,060 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2026-01-09 22:50:59,290 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-09 22:50:59,291 - app.api.v1.agent - INFO - [Chat Stream] Mode: planning
2026-01-09 22:50:59,292 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:54454 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2026-01-09 22:50:59,303 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 段融如何在日常训练；建议2000-3000字；沉稳内敛...
2026-01-09 22:50:59,307 - app.api.v1.agent - INFO - [agent_chat_stream] 📚 世界观数据已注入: 人物=9, 地点=6, 设定=6, 规范=无
2026-01-09 22:50:59,307 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:b2cee05e-5336-4ab7-8af6-60818c5f7583 (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=9f98efd6-1593-4967-ad43-f5dac759ac1c, conversation_id=b2cee05e-5336-4ab7-8af6-60818c5f7583)
2026-01-09 22:50:59,324 - app.services.context.store - INFO - [ContextStore] 加载上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:b2cee05e-5336-4ab7-8af6-60818c5f7583, 10条消息
2026-01-09 22:51:14,058 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:b2cee05e-5336-4ab7-8af6-60818c5f7583: 9467/16000 tokens
2026-01-09 22:51:14,228 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='段融如何在日常训练；建议2000-3000字；沉稳内敛...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:9f98efd6-1593-4967-ad43-f5dac759ac1c', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=3条
2026-01-09 22:51:14,231 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=9f98efd6-1593-4967-ad43-f5dac759ac1c | 含用户级=True | 找到=3条
2026-01-09 22:51:32,492 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 11条消息, 9467 tokens, 耗时 33185.06ms
2026-01-09 22:51:32,492 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 11 条历史消息 (token: 9467)
2026-01-09 22:51:32,492 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-09 22:51:32,492 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-09 22:51:32,492 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=20, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-09 22:51:32,520 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:59972 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 22:51:32,523 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:57120 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 22:51:34,314 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-09 22:51:34,316 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-09 22:51:34,336 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-09 22:51:34,341 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=301, cost=$0.000030, time=1823ms
2026-01-09 22:51:34,343 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=7, 尝试次数=1
2026-01-09 22:51:34,343 - app.services.agent.intent.classifier - INFO - [Intent] AI识别结果: writing
2026-01-09 22:51:34,343 - app.services.agent.langgraph_agent - INFO - [Planning] AI意图分类: writing (置信度: 0.90)
2026-01-09 22:51:34,343 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 段融如何在日常训练；建议2000-3000字；沉稳内敛...
2026-01-09 22:51:34,350 - app.core.cache - INFO - ✅ 缓存命中: prompt:planning:v2.36.0:get_planning_static_prompt:fca6eb91156619d0
2026-01-09 22:51:34,356 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-09 22:51:34,356 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=story_planning, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: story_planning; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-01-09 22:51:34,358 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.3, task_type=TaskType.STORY_PLANNING
2026-01-09 22:51:51,558 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-09 22:51:59,944 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 14 个数据块，总长度: 1720
2026-01-09 22:51:59,944 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 24568 (prompt=23674, completion=894)
2026-01-09 22:51:59,944 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-09 22:51:59,944 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-09 22:51:59,953 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-09 22:51:59,954 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=24568, cost=$0.038532, time=25586ms
2026-01-09 22:51:59,954 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=24568
2026-01-09 22:51:59,954 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户希望我创作一个全新的章节，即第四章，标题为“初露锋芒”。, 原料=为了创作这一章，我需要：1. 读取第三章, 处理=这是一个创作任务，我将分步执行：1. 创
2026-01-09 22:51:59,955 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共3个任务
2026-01-09 22:51:59,955 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共3个任务，耗时: 25.61s
2026-01-09 22:51:59,955 - app.api.v1.agent - INFO - [Stream] Plan tasks: 3 items
2026-01-09 22:51:59,955 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2026-01-09 22:51:59,955 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2026-01-09 22:51:59,955 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2026-01-09 22:51:59,955 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 任务分组: 第一层并行=1, 第二层并行=0, 串行=2
2026-01-09 22:51:59,955 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始第一层并行执行1个任务
2026-01-09 22:51:59,955 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务1开始: 读取第3章《一夕千悟》的内容，作为续写第4章的上下文。
2026-01-09 22:51:59,955 - app.api.v1.agent - INFO - [Stream] Task started: 读取第3章《一夕千悟》的内容，作为续写第4章的上下文。 (icon=FileText)
2026-01-09 22:51:59,955 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(get_chapter_by_order)
2026-01-09 22:51:59,955 - app.services.agent.tools.tool_types - INFO - [get_chapter_by_order] 开始执行工具
2026-01-09 22:51:59,981 - app.services.agent.langgraph_tools - INFO - [get_chapter_by_order_tool] ✅ 找到第3章: 第3章 一夕千悟
2026-01-09 22:51:59,981 - app.services.agent.tools.tool_types - INFO - [get_chapter_by_order] 执行成功 (耗时: 0.026s)
2026-01-09 22:51:59,981 - app.services.agent.execution.task_runner - INFO - [TaskRunner] get_chapter_by_order 执行成功（DeepAgent模式）
2026-01-09 22:51:59,981 - app.api.v1.agent - INFO - [Stream] 任务完成: 读取第3章《一夕千悟》的内容，作为续写第4章的上下文。 (0.0s)
2026-01-09 22:51:59,984 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务1完成
2026-01-09 22:51:59,984 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始串行执行2个任务
2026-01-09 22:51:59,984 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务2开始: 创建第四章，并设置标题为“初露锋芒”。
2026-01-09 22:51:59,984 - app.api.v1.agent - INFO - [Stream] Task started: 创建第四章，并设置标题为“初露锋芒”。 (icon=Wrench)
2026-01-09 22:51:59,984 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: create_chapter
2026-01-09 22:51:59,984 - app.services.agent.execution.tool_executor - WARNING - [StandardTool] 'create_chapter' 不存在，降级到 @tool: 工具 'create_chapter' 不存在
可用的 StandardTool: ['expand_text', 'analyze_content', 'analyze_text', 'evaluate_quality', 'smart_rewrite', 'smart_continue', 'smart_insert', 'apply_chapter_edit', 'get_context', 'read_chapter', 'get_chapter_by_order', 'search_analysis_fragments', 'get_worldview_summary', 'check_story_consistency']
可用的 DynamicTool: []
2026-01-09 22:51:59,986 - app.services.agent.execution.tool_executor - INFO - [LegacyTool] 使用 @tool 版本: create_chapter
2026-01-09 22:51:59,987 - app.services.agent.langgraph_agent - WARNING - [HITL] 审批回调执行失败: name 'hitl' is not defined
2026-01-09 22:51:59,988 - app.api.v1.agent - INFO - [Stream] 任务完成: 创建第四章，并设置标题为“初露锋芒”。 (0.0s)
2026-01-09 22:51:59,988 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务2完成
2026-01-09 22:51:59,988 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务3开始: 根据用户要求，创作第四章的完整内容。
2026-01-09 22:51:59,988 - app.api.v1.agent - INFO - [Stream] Task started: 根据用户要求，创作第四章的完整内容。 (icon=PenTool)
2026-01-09 22:51:59,988 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(smart_continue)
2026-01-09 22:51:59,988 - app.services.agent.tools.tool_types - INFO - [smart_continue] 开始执行工具
2026-01-09 22:51:59,995 - app.services.agent.tools.editor_tools - WARNING - [smart_continue] 获取章节内容失败: (sqlalchemy.dialects.postgresql.asyncpg.Error) <class 'asyncpg.exceptions.DataError'>: invalid input for query argument $1: '{"success": true, "requires_confirmatio... (invalid UUID '{"success": true, "requires_confirmation": true, "action_type": "create", "work_id": "9f98efd6-1593-4967-ad43-f5dac759ac1c", "chapter_title": "第四章 初露锋芒", "content": "", "content_preview": "", "order": 4, "description": "创建新章节：第四章 初露锋芒"}': length must be between 32..36 characters, got 276)
[SQL: SELECT chapters.id, chapters.work_id, chapters.title, chapters.content, chapters.summary, chapters.status, chapters."order", chapters.is_published, chapters.word_count, chapters.view_count, chapters.version, chapters.last_modified_by, chapters.created_at, chapters.updated_at, chapters.published_at
FROM chapters
WHERE chapters.id = $1::UUID]
[parameters: ('{"success": true, "requires_confirmation": true, "action_type": "create", "work_id": "9f98efd6-1593-4967-ad43-f5dac759ac1c", "chapter_title": "第四章 初露锋芒", "content": "", "content_preview": "", "order": 4, "description": "创建新章节：第四章 初露锋芒"}',)]
(Background on this error at: https://sqlalche.me/e/20/dbapi)
2026-01-09 22:51:59,995 - app.services.agent.tools.tool_types - WARNING - [smart_continue] 执行失败: 续写完成 (耗时: 0.006s)
2026-01-09 22:51:59,995 - app.services.agent.execution.task_runner - ERROR - [TaskRunner] smart_continue 执行失败（DeepAgent模式）: 续写完成
2026-01-09 22:51:59,995 - app.services.agent.langgraph_agent - WARNING - [HITL] 审批回调执行失败: name 'hitl' is not defined
2026-01-09 22:51:59,995 - app.api.v1.agent - INFO - [Stream] 任务完成: 根据用户要求，创作第四章的完整内容。 (0.0s)
2026-01-09 22:51:59,995 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务3完成
2026-01-09 22:51:59,995 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共3个任务，耗时: 0.04s
2026-01-09 22:51:59,995 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2026-01-09 22:51:59,995 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=1, 输出型=2, 展示型=0
2026-01-09 22:51:59,995 - app.services.agent.langgraph_agent - INFO - [Response] 2个输出任务（含续写），使用AI整合
2026-01-09 22:51:59,995 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2026-01-09 22:51:59,995 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=1, 输出型=2, 展示型=0
2026-01-09 22:51:59,995 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=2764字符, 处理后=2833字符
2026-01-09 22:51:59,995 - app.services.agent.planning.response_builder - INFO - [Summarization] 准备发送 summarization_start 事件
2026-01-09 22:51:59,995 - app.services.agent.stream.stream_event_handler - INFO - [StreamEventHandler] emit_summarization_start 被调用, _on_flow_event=True
2026-01-09 22:51:59,995 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_start 事件已发送
2026-01-09 22:51:59,995 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2026-01-09 22:51:59,995 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2026-01-09 22:51:59,995 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-09 22:51:59,995 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-09 22:52:00,001 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
2026-01-09 22:52:01,127 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:59019 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 22:52:03,170 - app.services.chapter_word_stat_service - INFO - 记录字数增量: chapter_id=cdabcd19-8562-4d6e-82b6-d37caae83a5d, delta=8, edit_event_id=b110ad4c-cd92-442a-acae-619bf618df29
2026-01-09 22:52:03,172 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 cdabcd19-8562-4d6e-82b6-d37caae83a5d 内容更新，新段落数: 65
[TaskService] Checking daily writing task for user 79913e7e-d5cd-4e09-bce6-ca6639bd8456, word_count: 101
[TaskService] Daily writing task result: None
2026-01-09 22:52:03,184 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:9f98efd6-1593-4967-ad43-f5dac759ac1c
2026-01-09 22:52:03,186 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/cdabcd19-8562-4d6e-82b6-d37caae83a5d
INFO:     127.0.0.1:59022 - "PUT /api/v1/chapters/cdabcd19-8562-4d6e-82b6-d37caae83a5d HTTP/1.1" 200 OK
2026-01-09 22:52:03,187 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第3章 一夕千悟 (order=3)
2026-01-09 22:52:03,331 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第3章 一夕千悟 (5 chunks)
2026-01-09 22:52:03,397 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:9f98efd6-1593-4967-ad43-f5dac759ac1c
2026-01-09 22:52:03,397 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/cdabcd19-8562-4d6e-82b6-d37caae83a5d
INFO:     127.0.0.1:59025 - "PUT /api/v1/chapters/cdabcd19-8562-4d6e-82b6-d37caae83a5d HTTP/1.1" 200 OK
2026-01-09 22:52:03,397 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第3章 一夕千悟 (order=3)
2026-01-09 22:52:03,554 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第3章 一夕千悟 (5 chunks)
2026-01-09 22:52:09,236 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-09 22:52:09,236 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_complete 事件已发送（第一个chunk时）
2026-01-09 22:52:09,236 - app.services.agent.planning.response_builder - INFO - [Summarization] output_ready 事件已发送（第一个chunk时）
2026-01-09 22:52:12,606 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 10 个数据块，总长度: 908
2026-01-09 22:52:12,608 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 4397 (prompt=3766, completion=631)
2026-01-09 22:52:12,608 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-09 22:52:12,608 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-09 22:52:12,625 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-09 22:52:12,629 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4397, cost=$0.002707, time=12606ms
2026-01-09 22:52:12,629 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=908
2026-01-09 22:52:16,674 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:9f98efd6-1593-4967-ad43-f5dac759ac1c | 重要度=0.60
2026-01-09 22:52:56,523 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:b2cee05e-5336-4ab7-8af6-60818c5f7583, token=10448
2026-01-09 22:53:15,922 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:b2cee05e-5336-4ab7-8af6-60818c5f7583, 消息数=12, Token=10448
2026-01-09 22:53:15,924 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:b2cee05e-5336-4ab7-8af6-60818c5f7583)
2026-01-09 22:53:15,924 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2026-01-09 22:53:15,933 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed
2026-01-09 22:53:15,957 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
2026-01-09 22:53:15,958 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:57086 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
INFO:     127.0.0.1:49973 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 22:53:31,223 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:57099 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 22:53:53,551 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 cdabcd19-8562-4d6e-82b6-d37caae83a5d 内容更新，新段落数: 65
2026-01-09 22:53:53,564 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:9f98efd6-1593-4967-ad43-f5dac759ac1c
2026-01-09 22:53:53,565 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/cdabcd19-8562-4d6e-82b6-d37caae83a5d
INFO:     127.0.0.1:53695 - "PUT /api/v1/chapters/cdabcd19-8562-4d6e-82b6-d37caae83a5d HTTP/1.1" 200 OK
2026-01-09 22:53:53,565 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第3章 一夕千悟 (order=3)
2026-01-09 22:53:54,275 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第3章 一夕千悟 (5 chunks)
2026-01-09 22:53:54,337 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:9f98efd6-1593-4967-ad43-f5dac759ac1c
2026-01-09 22:53:54,341 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/cdabcd19-8562-4d6e-82b6-d37caae83a5d
INFO:     127.0.0.1:53698 - "PUT /api/v1/chapters/cdabcd19-8562-4d6e-82b6-d37caae83a5d HTTP/1.1" 200 OK
2026-01-09 22:53:54,343 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第3章 一夕千悟 (order=3)
2026-01-09 22:53:54,653 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第3章 一夕千悟 (5 chunks)
2026-01-09 22:53:59,307 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 9f98efd6-1593-4967-ad43-f5dac759ac1c, chapter_id: 0e65cce3-13f9-4864-9465-111fcda0ad0f
2026-01-09 22:53:59,317 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 0e65cce3-13f9-4864-9465-111fcda0ad0f
2026-01-09 22:53:59,324 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: c318c024-26cd-4584-bfd6-e2d602a2c8ac
2026-01-09 22:53:59,324 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-09 22:53:59,326 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:49651 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-09 22:53:59,351 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 9f98efd6-1593-4967-ad43-f5dac759ac1c, chapter_id: 0e65cce3-13f9-4864-9465-111fcda0ad0f
2026-01-09 22:53:59,363 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 0e65cce3-13f9-4864-9465-111fcda0ad0f
2026-01-09 22:53:59,367 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: c318c024-26cd-4584-bfd6-e2d602a2c8ac
2026-01-09 22:53:59,369 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-09 22:53:59,371 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:49656 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-09 22:53:59,517 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:49657 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2026-01-09 22:53:59,760 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:9f98efd6-1593-4967-ad43-f5dac759ac1c
2026-01-09 22:53:59,763 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/0e65cce3-13f9-4864-9465-111fcda0ad0f
INFO:     127.0.0.1:57646 - "PUT /api/v1/chapters/0e65cce3-13f9-4864-9465-111fcda0ad0f HTTP/1.1" 200 OK
2026-01-09 22:53:59,765 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2026-01-09 22:54:01,564 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (6 chunks)
2026-01-09 22:54:01,601 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:57652 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 22:54:01,646 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:9f98efd6-1593-4967-ad43-f5dac759ac1c
2026-01-09 22:54:01,648 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/0e65cce3-13f9-4864-9465-111fcda0ad0f
INFO:     127.0.0.1:57649 - "PUT /api/v1/chapters/0e65cce3-13f9-4864-9465-111fcda0ad0f HTTP/1.1" 200 OK
2026-01-09 22:54:01,650 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2026-01-09 22:54:02,645 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (6 chunks)
2026-01-09 22:54:04,134 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:57655 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2026-01-09 22:54:04,148 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-09 22:54:04,148 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-09 22:54:04,148 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2026-01-09 22:54:06,517 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-09 22:54:06,517 - app.api.v1.agent - INFO - [Chat Stream] Mode: planning
2026-01-09 22:54:06,520 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:57658 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2026-01-09 22:54:06,523 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 获取当前作品的完整上下文，然后帮我续写一段段融在考核中展示五虎群羊刀法的精彩打斗场面，写完后直接应用...
2026-01-09 22:54:06,527 - app.api.v1.agent - INFO - [agent_chat_stream] 📚 世界观数据已注入: 人物=9, 地点=6, 设定=6, 规范=无
2026-01-09 22:54:06,527 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:27c8f1f8-fa03-4675-9c76-cdd670869551 (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=9f98efd6-1593-4967-ad43-f5dac759ac1c, conversation_id=27c8f1f8-fa03-4675-9c76-cdd670869551)
2026-01-09 22:54:06,531 - app.services.context.manager - INFO - [ContextManager] 创建新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:27c8f1f8-fa03-4675-9c76-cdd670869551
2026-01-09 22:54:06,531 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:27c8f1f8-fa03-4675-9c76-cdd670869551: 0/16000 tokens
2026-01-09 22:54:06,648 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='获取当前作品的完整上下文，然后帮我续写一段段融在考核中展示五...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:9f98efd6-1593-4967-ad43-f5dac759ac1c', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=3条
2026-01-09 22:54:06,649 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=9f98efd6-1593-4967-ad43-f5dac759ac1c | 含用户级=True | 找到=3条
2026-01-09 22:54:06,649 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 1条消息, 0 tokens, 耗时 122.19ms
2026-01-09 22:54:06,649 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 1 条历史消息 (token: 0)
2026-01-09 22:54:06,649 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-09 22:54:06,649 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-09 22:54:06,649 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=20, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-09 22:54:07,791 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-09 22:54:07,792 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-09 22:54:07,812 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-09 22:54:07,815 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=320, cost=$0.000032, time=1143ms
2026-01-09 22:54:07,817 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=7, 尝试次数=1
2026-01-09 22:54:07,818 - app.services.agent.intent.classifier - INFO - [Intent] AI识别结果: writing
2026-01-09 22:54:07,818 - app.services.agent.langgraph_agent - INFO - [Planning] AI意图分类: writing (置信度: 0.90)
2026-01-09 22:54:07,819 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 获取当前作品的完整上下文，然后帮我续写一段段融在考核中展示五虎群羊刀法的精彩打斗场面，写完后直接应用...
2026-01-09 22:54:07,826 - app.core.cache - INFO - ✅ 缓存命中: prompt:planning:v2.36.0:get_planning_static_prompt:fca6eb91156619d0
2026-01-09 22:54:07,832 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-09 22:54:07,832 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=story_planning, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: story_planning; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-01-09 22:54:07,832 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.3, task_type=TaskType.STORY_PLANNING
2026-01-09 22:54:20,520 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-09 22:54:24,202 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 9 个数据块，总长度: 1175
2026-01-09 22:54:24,202 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 13227 (prompt=12657, completion=570)
2026-01-09 22:54:24,205 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-09 22:54:24,205 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-09 22:54:24,225 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-09 22:54:24,226 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=13227, cost=$0.021521, time=16372ms
2026-01-09 22:54:24,227 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=13227
2026-01-09 22:54:24,227 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户需要创作一段新的小说内容，具体是一段精彩的打斗场面，并希, 原料=为了保证续写内容的连贯性，需要获取当前章, 处理=首先使用 `read_chapter_t
2026-01-09 22:54:24,227 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共2个任务
2026-01-09 22:54:24,227 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共2个任务，耗时: 16.41s
2026-01-09 22:54:24,227 - app.api.v1.agent - INFO - [Stream] Plan tasks: 2 items
2026-01-09 22:54:24,227 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2026-01-09 22:54:24,227 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2026-01-09 22:54:24,227 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2026-01-09 22:54:24,227 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 任务分组: 第一层并行=1, 第二层并行=0, 串行=1
2026-01-09 22:54:24,227 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始第一层并行执行1个任务
2026-01-09 22:54:24,227 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务1开始: 获取当前章节的完整内容，作为续写的上下文。
2026-01-09 22:54:24,227 - app.api.v1.agent - INFO - [Stream] Task started: 获取当前章节的完整内容，作为续写的上下文。 (icon=FileText)
2026-01-09 22:54:24,227 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(read_chapter)
2026-01-09 22:54:24,236 - app.services.agent.tools.tool_types - INFO - [read_chapter] 开始执行工具
2026-01-09 22:54:24,247 - app.services.agent.langgraph_tools - INFO - [read_chapter_tool] ✅ 读取章节成功: 第5章 太一门
2026-01-09 22:54:24,247 - app.services.agent.tools.tool_types - INFO - [read_chapter] 执行成功 (耗时: 0.011s)
2026-01-09 22:54:24,247 - app.services.agent.execution.task_runner - INFO - [TaskRunner] read_chapter 执行成功（DeepAgent模式）
2026-01-09 22:54:24,247 - app.api.v1.agent - INFO - [Stream] 任务完成: 获取当前章节的完整内容，作为续写的上下文。 (0.0s)
2026-01-09 22:54:24,247 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务1完成
2026-01-09 22:54:24,247 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始串行执行1个任务
2026-01-09 22:54:24,247 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务2开始: 根据上下文，续写一段段融在考核中展示五虎群羊刀法的精彩打斗场面，并应用到编辑器。
2026-01-09 22:54:24,247 - app.api.v1.agent - INFO - [Stream] Task started: 根据上下文，续写一段段融在考核中展示五虎群羊刀法的精彩打斗场面，并应用到编辑器。 (icon=PenTool)
2026-01-09 22:54:24,255 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(smart_continue)
2026-01-09 22:54:24,256 - app.services.agent.tools.tool_types - INFO - [smart_continue] 开始执行工具
2026-01-09 22:54:24,258 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-09 22:54:24,258 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=content_creation, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro
2026-01-09 22:54:24,258 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=1000, temp=0.8, 尝试=1/3, task_type=TaskType.CONTENT_CREATION
2026-01-09 22:54:31,344 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:54890 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 22:54:50,711 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-09 22:54:50,712 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-09 22:54:50,735 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-09 22:54:50,736 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=3101, cost=$0.009275, time=26453ms
2026-01-09 22:54:50,736 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=758, 尝试次数=1
2026-01-09 22:54:50,736 - app.services.agent.tools.tool_types - INFO - [smart_continue] 执行成功 (耗时: 26.480s)
2026-01-09 22:54:50,736 - app.services.agent.execution.task_runner - INFO - [TaskRunner] smart_continue 执行成功（DeepAgent模式）
2026-01-09 22:54:50,736 - app.services.agent.langgraph_agent - WARNING - [HITL] 审批回调执行失败: name 'hitl' is not defined
2026-01-09 22:54:50,740 - app.api.v1.agent - INFO - [Stream] 任务完成: 根据上下文，续写一段段融在考核中展示五虎群羊刀法的精彩打斗场面，并应用到编辑器。 (26.5s)
2026-01-09 22:54:50,741 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务2完成
2026-01-09 22:54:50,741 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共2个任务，耗时: 26.51s
2026-01-09 22:54:50,741 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2026-01-09 22:54:50,742 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=1, 输出型=1, 展示型=0
2026-01-09 22:54:50,742 - app.services.agent.langgraph_agent - INFO - [Response] 单个输出任务(smart_continue)，使用AI整合
2026-01-09 22:54:50,743 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2026-01-09 22:54:50,743 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=1, 输出型=1, 展示型=0
2026-01-09 22:54:50,744 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=3812字符, 处理后=3878字符
2026-01-09 22:54:50,744 - app.services.agent.planning.response_builder - INFO - [Summarization] 准备发送 summarization_start 事件
2026-01-09 22:54:50,744 - app.services.agent.stream.stream_event_handler - INFO - [StreamEventHandler] emit_summarization_start 被调用, _on_flow_event=True
2026-01-09 22:54:50,745 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_start 事件已发送
2026-01-09 22:54:50,746 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2026-01-09 22:54:50,746 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2026-01-09 22:54:50,758 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-09 22:54:50,760 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-09 22:54:50,760 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
2026-01-09 22:54:53,966 - app.services.chapter_word_stat_service - INFO - 记录字数增量: chapter_id=0e65cce3-13f9-4864-9465-111fcda0ad0f, delta=624, edit_event_id=5cd7b100-4bcd-4610-89b6-85cf43d406c6
2026-01-09 22:54:53,970 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 0e65cce3-13f9-4864-9465-111fcda0ad0f 内容更新，新段落数: 84
[TaskService] Checking daily writing task for user 79913e7e-d5cd-4e09-bce6-ca6639bd8456, word_count: 1593
[TaskService] Daily writing task result: None
2026-01-09 22:54:54,022 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:9f98efd6-1593-4967-ad43-f5dac759ac1c
2026-01-09 22:54:54,027 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/0e65cce3-13f9-4864-9465-111fcda0ad0f
INFO:     127.0.0.1:58099 - "PUT /api/v1/chapters/0e65cce3-13f9-4864-9465-111fcda0ad0f HTTP/1.1" 200 OK
2026-01-09 22:54:54,033 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2026-01-09 22:54:56,039 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (7 chunks)
2026-01-09 22:54:56,132 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:9f98efd6-1593-4967-ad43-f5dac759ac1c
2026-01-09 22:54:56,134 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/0e65cce3-13f9-4864-9465-111fcda0ad0f
INFO:     127.0.0.1:58102 - "PUT /api/v1/chapters/0e65cce3-13f9-4864-9465-111fcda0ad0f HTTP/1.1" 200 OK
2026-01-09 22:54:56,136 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2026-01-09 22:54:57,426 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (7 chunks)
2026-01-09 22:54:58,980 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/approval-response
INFO:     127.0.0.1:55016 - "POST /api/v1/agent/chat/approval-response HTTP/1.1" 200 OK
2026-01-09 22:55:01,396 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:55021 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 22:55:04,847 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-09 22:55:04,847 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_complete 事件已发送（第一个chunk时）
2026-01-09 22:55:04,847 - app.services.agent.planning.response_builder - INFO - [Summarization] output_ready 事件已发送（第一个chunk时）
2026-01-09 22:55:09,724 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 23 个数据块，总长度: 1415
2026-01-09 22:55:09,724 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 7216 (prompt=6107, completion=1109)
2026-01-09 22:55:09,724 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-09 22:55:09,727 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-09 22:55:09,747 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-09 22:55:09,749 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=7216, cost=$0.004605, time=18965ms
2026-01-09 22:55:09,749 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=1415
2026-01-09 22:55:13,447 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:9f98efd6-1593-4967-ad43-f5dac759ac1c | 重要度=0.65
2026-01-09 22:55:17,481 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:9f98efd6-1593-4967-ad43-f5dac759ac1c | 重要度=0.60
2026-01-09 22:55:17,492 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:27c8f1f8-fa03-4675-9c76-cdd670869551, token=1758
2026-01-09 22:55:17,497 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:27c8f1f8-fa03-4675-9c76-cdd670869551, 消息数=2, Token=1758
2026-01-09 22:55:17,499 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:27c8f1f8-fa03-4675-9c76-cdd670869551)
2026-01-09 22:55:17,501 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2026-01-09 22:55:17,511 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed
2026-01-09 22:55:31,386 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:49546 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 22:56:01,652 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:49260 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 22:56:05,736 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 9f98efd6-1593-4967-ad43-f5dac759ac1c, chapter_id: c318c024-26cd-4584-bfd6-e2d602a2c8ac
2026-01-09 22:56:05,746 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: c318c024-26cd-4584-bfd6-e2d602a2c8ac
2026-01-09 22:56:05,746 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: cdabcd19-8562-4d6e-82b6-d37caae83a5d
2026-01-09 22:56:05,746 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-09 22:56:05,750 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:64182 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-09 22:56:05,884 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 9f98efd6-1593-4967-ad43-f5dac759ac1c, chapter_id: c318c024-26cd-4584-bfd6-e2d602a2c8ac
2026-01-09 22:56:05,892 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: c318c024-26cd-4584-bfd6-e2d602a2c8ac
2026-01-09 22:56:05,897 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: cdabcd19-8562-4d6e-82b6-d37caae83a5d
2026-01-09 22:56:05,898 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-09 22:56:05,901 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:64185 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-09 22:56:06,313 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:9f98efd6-1593-4967-ad43-f5dac759ac1c
2026-01-09 22:56:06,318 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/c318c024-26cd-4584-bfd6-e2d602a2c8ac
INFO:     127.0.0.1:64188 - "PUT /api/v1/chapters/c318c024-26cd-4584-bfd6-e2d602a2c8ac HTTP/1.1" 200 OK
2026-01-09 22:56:06,321 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第4章 家底 (order=4)
2026-01-09 22:56:07,894 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第4章 家底 (6 chunks)
2026-01-09 22:56:07,900 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 9f98efd6-1593-4967-ad43-f5dac759ac1c, chapter_id: cdabcd19-8562-4d6e-82b6-d37caae83a5d
2026-01-09 22:56:07,905 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 9f98efd6-1593-4967-ad43-f5dac759ac1c, chapter_id: cdabcd19-8562-4d6e-82b6-d37caae83a5d
2026-01-09 22:56:07,926 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: cdabcd19-8562-4d6e-82b6-d37caae83a5d
2026-01-09 22:56:07,938 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: 270de73b-23af-4723-b61c-1b6fdc77bc9f
2026-01-09 22:56:07,942 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-09 22:56:07,957 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
2026-01-09 22:56:07,960 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: cdabcd19-8562-4d6e-82b6-d37caae83a5d
2026-01-09 22:56:07,966 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: 270de73b-23af-4723-b61c-1b6fdc77bc9f
2026-01-09 22:56:07,966 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
INFO:     127.0.0.1:64191 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-09 22:56:07,988 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:64194 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-09 22:56:08,141 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:9f98efd6-1593-4967-ad43-f5dac759ac1c
2026-01-09 22:56:08,146 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/cdabcd19-8562-4d6e-82b6-d37caae83a5d
INFO:     127.0.0.1:64200 - "PUT /api/v1/chapters/cdabcd19-8562-4d6e-82b6-d37caae83a5d HTTP/1.1" 200 OK
2026-01-09 22:56:08,147 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第3章 一夕千悟 (order=3)
2026-01-09 22:56:09,445 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第3章 一夕千悟 (5 chunks)
2026-01-09 22:56:09,568 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:9f98efd6-1593-4967-ad43-f5dac759ac1c
2026-01-09 22:56:09,572 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/c318c024-26cd-4584-bfd6-e2d602a2c8ac
INFO:     127.0.0.1:64197 - "PUT /api/v1/chapters/c318c024-26cd-4584-bfd6-e2d602a2c8ac HTTP/1.1" 200 OK
2026-01-09 22:56:09,575 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第4章 家底 (order=4)
2026-01-09 22:56:09,579 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:9f98efd6-1593-4967-ad43-f5dac759ac1c
2026-01-09 22:56:09,582 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/cdabcd19-8562-4d6e-82b6-d37caae83a5d
INFO:     127.0.0.1:64205 - "PUT /api/v1/chapters/cdabcd19-8562-4d6e-82b6-d37caae83a5d HTTP/1.1" 200 OK
2026-01-09 22:56:09,584 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第3章 一夕千悟 (order=3)
2026-01-09 22:56:12,032 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第4章 家底 (6 chunks)
2026-01-09 22:56:12,038 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第3章 一夕千悟 (5 chunks)
2026-01-09 22:56:12,212 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:55482 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2026-01-09 22:56:17,310 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:65104 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2026-01-09 22:56:17,457 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-09 22:56:17,457 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-09 22:56:17,457 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2026-01-09 22:56:20,259 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-09 22:56:20,264 - app.api.v1.agent - INFO - [Chat Stream] Mode: planning
2026-01-09 22:56:20,266 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:65107 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2026-01-09 22:56:20,275 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 读取第1章到第3章的内容，分析每章的核心情节，然后帮我把第2章的标题从"浑圆桩"改成更能体现章节内容...
2026-01-09 22:56:20,295 - app.api.v1.agent - INFO - [agent_chat_stream] 📚 世界观数据已注入: 人物=9, 地点=6, 设定=6, 规范=无
2026-01-09 22:56:20,295 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:1b0b2d85-6715-4606-98dc-81cee1748897 (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=9f98efd6-1593-4967-ad43-f5dac759ac1c, conversation_id=1b0b2d85-6715-4606-98dc-81cee1748897)
2026-01-09 22:56:20,302 - app.services.context.manager - INFO - [ContextManager] 创建新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:1b0b2d85-6715-4606-98dc-81cee1748897
2026-01-09 22:56:20,303 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:1b0b2d85-6715-4606-98dc-81cee1748897: 0/16000 tokens
2026-01-09 22:56:20,513 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='读取第1章到第3章的内容，分析每章的核心情节，然后帮我把第2...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:9f98efd6-1593-4967-ad43-f5dac759ac1c', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=3条
2026-01-09 22:56:20,513 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=9f98efd6-1593-4967-ad43-f5dac759ac1c | 含用户级=True | 找到=3条
2026-01-09 22:56:20,515 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 1条消息, 0 tokens, 耗时 220.55ms
2026-01-09 22:56:20,517 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 1 条历史消息 (token: 0)
2026-01-09 22:56:20,518 - app.services.agent.planning.quick_path - INFO - [QuickPath-Planning] 命中快速路径: get_chapter_info
2026-01-09 22:56:20,518 - app.services.agent.planning.quick_path - WARNING - [QuickPath-Planning] 执行失败: 'list' object has no attribute 'get'，降级到规划模式
2026-01-09 22:56:20,520 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-09 22:56:20,522 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-09 22:56:20,522 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=20, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-09 22:56:22,003 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-09 22:56:22,003 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-09 22:56:22,021 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-09 22:56:22,022 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=316, cost=$0.000032, time=1480ms
2026-01-09 22:56:22,022 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=7, 尝试次数=1
2026-01-09 22:56:22,023 - app.services.agent.intent.classifier - INFO - [Intent] AI识别结果: writing
2026-01-09 22:56:22,023 - app.services.agent.langgraph_agent - INFO - [Planning] AI意图分类: writing (置信度: 0.90)
2026-01-09 22:56:22,023 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 读取第1章到第3章的内容，分析每章的核心情节，然后帮我把第2章的标题从"浑圆桩"改成更能体现章节内容...
2026-01-09 22:56:22,027 - app.core.cache - INFO - ✅ 缓存命中: prompt:planning:v2.36.0:get_planning_static_prompt:fca6eb91156619d0
2026-01-09 22:56:22,033 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-09 22:56:22,034 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=story_planning, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: story_planning; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-01-09 22:56:22,034 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.3, task_type=TaskType.STORY_PLANNING
2026-01-09 22:56:31,653 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:50065 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 22:56:35,443 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-09 22:56:42,564 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 15 个数据块，总长度: 2119
2026-01-09 22:56:42,564 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 13857 (prompt=12906, completion=951)
2026-01-09 22:56:42,566 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-09 22:56:42,566 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-09 22:56:42,581 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-09 22:56:42,581 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=13857, cost=$0.025643, time=20531ms
2026-01-09 22:56:42,581 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=13857
2026-01-09 22:56:42,587 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户期望得到一个包含三项内容的输出：1. 对第1至3章核心情, 原料=需要第1章、第2章和第3章的完整内容。还, 处理=这是一个多步骤的分析和操作任务，可以一次
2026-01-09 22:56:42,587 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共6个任务
2026-01-09 22:56:42,587 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共6个任务，耗时: 20.56s
2026-01-09 22:56:42,587 - app.api.v1.agent - INFO - [Stream] Plan tasks: 6 items
2026-01-09 22:56:42,587 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2026-01-09 22:56:42,587 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2026-01-09 22:56:42,587 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2026-01-09 22:56:42,592 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 任务分组: 第一层并行=1, 第二层并行=4, 串行=1
2026-01-09 22:56:42,593 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始第一层并行执行1个任务
2026-01-09 22:56:42,594 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务1开始: 使用范围参数一次性读取第1章到第3章的全部内容。
2026-01-09 22:56:42,595 - app.api.v1.agent - INFO - [Stream] Task started: 使用范围参数一次性读取第1章到第3章的全部内容。 (icon=FileText)
2026-01-09 22:56:42,595 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(get_chapter_by_order)
2026-01-09 22:56:42,597 - app.services.agent.tools.tool_types - INFO - [get_chapter_by_order] 开始执行工具
2026-01-09 22:56:42,625 - app.services.agent.langgraph_tools - INFO - [get_chapter_by_order_tool] ✅ 批量读取成功: 共 3 章
2026-01-09 22:56:42,627 - app.services.agent.tools.tool_types - INFO - [get_chapter_by_order] 执行成功 (耗时: 0.032s)
2026-01-09 22:56:42,628 - app.services.agent.execution.task_runner - INFO - [TaskRunner] get_chapter_by_order 执行成功（DeepAgent模式）
2026-01-09 22:56:42,629 - app.api.v1.agent - INFO - [Stream] 任务完成: 使用范围参数一次性读取第1章到第3章的全部内容。 (0.0s)
2026-01-09 22:56:42,629 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务1完成
2026-01-09 22:56:42,629 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始第二层并行执行4个任务
2026-01-09 22:56:42,630 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第二层任务2开始: 分析第1章的核心情节。
2026-01-09 22:56:42,630 - app.api.v1.agent - INFO - [Stream] Task started: 分析第1章的核心情节。 (icon=BarChart2)
2026-01-09 22:56:42,630 - app.services.agent.execution.task_runner - INFO - [TaskRunner] analyze_text_tool 使用 focus: '分析并概括本章的核心情节...'
2026-01-09 22:56:42,630 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(analyze_text)
2026-01-09 22:56:42,630 - app.services.agent.tools.tool_types - INFO - [analyze_text] 开始执行工具
2026-01-09 22:56:42,632 - app.services.agent.tools.analysis_tools - INFO - [analyze_text_tool] 尝试第 1 次调用，config={'temperature': 0.3, 'task_type': <TaskType.SUMMARIZATION: 'summarization'>}
2026-01-09 22:56:42,635 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第二层任务3开始: 分析第2章的核心情节。
2026-01-09 22:56:42,635 - app.api.v1.agent - INFO - [Stream] Task started: 分析第2章的核心情节。 (icon=BarChart2)
2026-01-09 22:56:42,635 - app.services.agent.execution.task_runner - INFO - [TaskRunner] analyze_text_tool 使用 focus: '分析并概括本章的核心情节...'
2026-01-09 22:56:42,635 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(analyze_text)
2026-01-09 22:56:42,635 - app.services.agent.tools.tool_types - INFO - [analyze_text] 开始执行工具
2026-01-09 22:56:42,635 - app.services.agent.tools.analysis_tools - INFO - [analyze_text_tool] 尝试第 1 次调用，config={'temperature': 0.3, 'task_type': <TaskType.SUMMARIZATION: 'summarization'>}
2026-01-09 22:56:42,635 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第二层任务4开始: 分析第3章的核心情节。
2026-01-09 22:56:42,635 - app.api.v1.agent - INFO - [Stream] Task started: 分析第3章的核心情节。 (icon=BarChart2)
2026-01-09 22:56:42,635 - app.services.agent.execution.task_runner - INFO - [TaskRunner] analyze_text_tool 使用 focus: '分析并概括本章的核心情节...'
2026-01-09 22:56:42,635 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(analyze_text)
2026-01-09 22:56:42,639 - app.services.agent.tools.tool_types - INFO - [analyze_text] 开始执行工具
2026-01-09 22:56:42,639 - app.services.agent.tools.analysis_tools - INFO - [analyze_text_tool] 尝试第 1 次调用，config={'temperature': 0.3, 'task_type': <TaskType.SUMMARIZATION: 'summarization'>}
2026-01-09 22:56:42,641 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第二层任务5开始: 根据第2章的核心情节，生成一个更能体现章节内容的新标题。
2026-01-09 22:56:42,641 - app.api.v1.agent - INFO - [Stream] Task started: 根据第2章的核心情节，生成一个更能体现章节内容的新标题。 (icon=BarChart2)
2026-01-09 22:56:42,642 - app.services.agent.execution.task_runner - INFO - [TaskRunner] analyze_text_tool 使用 focus: '根据章节内容，生成一个更能体现核心情节的、有吸引力的章节标题...'
2026-01-09 22:56:42,642 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(analyze_text)
2026-01-09 22:56:42,642 - app.services.agent.tools.tool_types - INFO - [analyze_text] 开始执行工具
2026-01-09 22:56:42,643 - app.services.agent.tools.analysis_tools - INFO - [analyze_text_tool] 尝试第 1 次调用，config={'temperature': 0.3, 'task_type': <TaskType.SUMMARIZATION: 'summarization'>}
2026-01-09 22:56:42,650 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-09 22:56:42,650 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-09 22:56:42,650 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
2026-01-09 22:56:42,656 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-09 22:56:42,656 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-09 22:56:42,657 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
2026-01-09 22:56:42,658 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-09 22:56:42,660 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-09 22:56:42,660 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
2026-01-09 22:56:42,662 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-09 22:56:42,664 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-09 22:56:42,664 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
2026-01-09 22:56:48,347 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-09 22:56:48,760 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-09 22:56:48,818 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-09 22:56:49,586 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 4 个数据块，总长度: 284
2026-01-09 22:56:49,586 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 2898 (prompt=2676, completion=222)
2026-01-09 22:56:49,589 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-09 22:56:49,590 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-09 22:56:49,603 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-09 22:56:49,609 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2898, cost=$0.001358, time=6932ms
2026-01-09 22:56:49,609 - app.services.agent.tools.analysis_tools - INFO - [analyze_text_tool] 第 1 次调用成功
2026-01-09 22:56:49,609 - app.services.agent.tools.analysis_tools - INFO - [analyze_text_tool] 分析完成，结果长度: 284
2026-01-09 22:56:49,611 - app.services.agent.tools.tool_types - INFO - [analyze_text] 执行成功 (耗时: 6.971s)
2026-01-09 22:56:49,611 - app.services.agent.execution.task_runner - INFO - [TaskRunner] analyze_text 执行成功（DeepAgent模式）
2026-01-09 22:56:49,613 - app.api.v1.agent - INFO - [Stream] 任务完成: 分析第3章的核心情节。 (7.0s)
2026-01-09 22:56:49,614 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第二层任务4完成
2026-01-09 22:56:49,621 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 4 个数据块，总长度: 287
2026-01-09 22:56:49,621 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 3061 (prompt=2837, completion=224)
2026-01-09 22:56:49,621 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-09 22:56:49,621 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-09 22:56:49,635 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-09 22:56:49,635 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=3061, cost=$0.001411, time=6956ms
2026-01-09 22:56:49,635 - app.services.agent.tools.analysis_tools - INFO - [analyze_text_tool] 第 1 次调用成功
2026-01-09 22:56:49,635 - app.services.agent.tools.analysis_tools - INFO - [analyze_text_tool] 分析完成，结果长度: 287
2026-01-09 22:56:49,638 - app.services.agent.tools.tool_types - INFO - [analyze_text] 执行成功 (耗时: 7.008s)
2026-01-09 22:56:49,638 - app.services.agent.execution.task_runner - INFO - [TaskRunner] analyze_text 执行成功（DeepAgent模式）
2026-01-09 22:56:49,638 - app.api.v1.agent - INFO - [Stream] 任务完成: 分析第1章的核心情节。 (7.0s)
2026-01-09 22:56:49,638 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第二层任务2完成
2026-01-09 22:56:50,643 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 5 个数据块，总长度: 374
2026-01-09 22:56:50,643 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 3028 (prompt=2749, completion=279)
2026-01-09 22:56:50,643 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-09 22:56:50,643 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-09 22:56:50,654 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-09 22:56:50,656 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=3028, cost=$0.001522, time=7993ms
2026-01-09 22:56:50,656 - app.services.agent.tools.analysis_tools - INFO - [analyze_text_tool] 第 1 次调用成功
2026-01-09 22:56:50,657 - app.services.agent.tools.analysis_tools - INFO - [analyze_text_tool] 分析完成，结果长度: 374
2026-01-09 22:56:50,657 - app.services.agent.tools.tool_types - INFO - [analyze_text] 执行成功 (耗时: 8.022s)
2026-01-09 22:56:50,658 - app.services.agent.execution.task_runner - INFO - [TaskRunner] analyze_text 执行成功（DeepAgent模式）
2026-01-09 22:56:50,658 - app.api.v1.agent - INFO - [Stream] 任务完成: 分析第2章的核心情节。 (8.0s)
2026-01-09 22:56:50,658 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第二层任务3完成
2026-01-09 22:56:54,003 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-09 22:56:54,987 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 4 个数据块，总长度: 298
2026-01-09 22:56:54,988 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 3896 (prompt=3685, completion=211)
2026-01-09 22:56:54,988 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-09 22:56:54,988 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-09 22:56:55,005 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-09 22:56:55,007 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=3896, cost=$0.001633, time=12328ms
2026-01-09 22:56:55,007 - app.services.agent.tools.analysis_tools - INFO - [analyze_text_tool] 第 1 次调用成功
2026-01-09 22:56:55,007 - app.services.agent.tools.analysis_tools - INFO - [analyze_text_tool] 分析完成，结果长度: 298
2026-01-09 22:56:55,007 - app.services.agent.tools.tool_types - INFO - [analyze_text] 执行成功 (耗时: 12.365s)
2026-01-09 22:56:55,007 - app.services.agent.execution.task_runner - INFO - [TaskRunner] analyze_text 执行成功（DeepAgent模式）
2026-01-09 22:56:55,007 - app.api.v1.agent - INFO - [Stream] 任务完成: 根据第2章的核心情节，生成一个更能体现章节内容的新标题。 (12.4s)
2026-01-09 22:56:55,007 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第二层任务5完成
2026-01-09 22:56:55,007 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始串行执行1个任务
2026-01-09 22:56:55,007 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务6开始: 将第2章的标题从“浑圆桩”更新为新生成的标题。
2026-01-09 22:56:55,014 - app.api.v1.agent - INFO - [Stream] Task started: 将第2章的标题从“浑圆桩”更新为新生成的标题。 (icon=Wrench)
2026-01-09 22:56:55,014 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: update_chapter_title
2026-01-09 22:56:55,014 - app.services.agent.execution.tool_executor - WARNING - [StandardTool] 'update_chapter_title' 不存在，降级到 @tool: 工具 'update_chapter_title' 不存在
可用的 StandardTool: ['expand_text', 'analyze_content', 'analyze_text', 'evaluate_quality', 'smart_rewrite', 'smart_continue', 'smart_insert', 'apply_chapter_edit', 'get_context', 'read_chapter', 'get_chapter_by_order', 'search_analysis_fragments', 'get_worldview_summary', 'check_story_consistency']
可用的 DynamicTool: []
2026-01-09 22:56:55,014 - app.services.agent.execution.tool_executor - INFO - [LegacyTool] 使用 @tool 版本: update_chapter_title
2026-01-09 22:56:55,021 - app.services.agent.execution.tool_executor - ERROR - [LegacyTool] 调用失败: 1 validation error for update_chapter_title
old_title
  Input should be a valid string [type=string_type, input_value=None, input_type=NoneType]
    For further information visit https://errors.pydantic.dev/2.12/v/string_type
2026-01-09 22:56:55,023 - app.api.v1.agent - INFO - [Stream] 任务完成: 将第2章的标题从“浑圆桩”更新为新生成的标题。 (0.0s)
2026-01-09 22:56:55,023 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务6完成
2026-01-09 22:56:55,025 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共6个任务，耗时: 12.44s
2026-01-09 22:56:55,025 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2026-01-09 22:56:55,025 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=1, 输出型=5, 展示型=0
2026-01-09 22:56:55,025 - app.services.agent.langgraph_agent - INFO - [Response] 5个输出任务（含续写），使用AI整合
2026-01-09 22:56:55,025 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2026-01-09 22:56:55,025 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=1, 输出型=5, 展示型=0
2026-01-09 22:56:55,025 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=9555字符, 处理后=1725字符
2026-01-09 22:56:55,025 - app.services.agent.planning.response_builder - INFO - [Summarization] 准备发送 summarization_start 事件
2026-01-09 22:56:55,025 - app.services.agent.stream.stream_event_handler - INFO - [StreamEventHandler] emit_summarization_start 被调用, _on_flow_event=True
2026-01-09 22:56:55,025 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_start 事件已发送
2026-01-09 22:56:55,025 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2026-01-09 22:56:55,032 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2026-01-09 22:56:55,042 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-09 22:56:55,042 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-09 22:56:55,042 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
2026-01-09 22:57:01,691 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:61760 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 22:57:04,497 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-09 22:57:04,498 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_complete 事件已发送（第一个chunk时）
2026-01-09 22:57:04,498 - app.services.agent.planning.response_builder - INFO - [Summarization] output_ready 事件已发送（第一个chunk时）
2026-01-09 22:57:09,586 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 17 个数据块，总长度: 1707
2026-01-09 22:57:09,587 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 4201 (prompt=3095, completion=1106)
2026-01-09 22:57:09,589 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-09 22:57:09,590 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-09 22:57:09,614 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-09 22:57:09,617 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4201, cost=$0.003694, time=14545ms
2026-01-09 22:57:09,618 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=1707
2026-01-09 22:57:14,540 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:9f98efd6-1593-4967-ad43-f5dac759ac1c | 重要度=0.99
2026-01-09 22:57:18,941 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:9f98efd6-1593-4967-ad43-f5dac759ac1c | 重要度=0.60
2026-01-09 22:57:18,954 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:1b0b2d85-6715-4606-98dc-81cee1748897, token=1705
2026-01-09 22:57:18,958 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:1b0b2d85-6715-4606-98dc-81cee1748897, 消息数=2, Token=1705
2026-01-09 22:57:18,959 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:1b0b2d85-6715-4606-98dc-81cee1748897)
2026-01-09 22:57:18,962 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2026-01-09 22:57:18,973 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed
2026-01-09 22:57:31,681 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:54230 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 22:57:50,977 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-09 22:57:50,977 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-09 22:57:50,977 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2026-01-09 22:57:53,030 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-09 22:57:53,031 - app.api.v1.agent - INFO - [Chat Stream] Mode: planning
2026-01-09 22:57:53,035 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:63865 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2026-01-09 22:57:53,040 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 找到段融被其他杂役弟子嫌弃"一身马粪味"的场景，用展示手法重写他内心的窃喜情绪，同时增强马厩环境的感...
2026-01-09 22:57:53,046 - app.api.v1.agent - INFO - [agent_chat_stream] 📚 世界观数据已注入: 人物=9, 地点=6, 设定=6, 规范=无
2026-01-09 22:57:53,046 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:1b0b2d85-6715-4606-98dc-81cee1748897 (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=9f98efd6-1593-4967-ad43-f5dac759ac1c, conversation_id=1b0b2d85-6715-4606-98dc-81cee1748897)
2026-01-09 22:57:53,049 - app.services.context.store - INFO - [ContextStore] 加载上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:1b0b2d85-6715-4606-98dc-81cee1748897, 2条消息
2026-01-09 22:57:53,051 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:1b0b2d85-6715-4606-98dc-81cee1748897: 1705/16000 tokens
2026-01-09 22:57:53,234 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='找到段融被其他杂役弟子嫌弃"一身马粪味"的场景，用展示手法重...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:9f98efd6-1593-4967-ad43-f5dac759ac1c', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=3条
2026-01-09 22:57:53,234 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=9f98efd6-1593-4967-ad43-f5dac759ac1c | 含用户级=True | 找到=3条
2026-01-09 22:57:53,237 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 3条消息, 1705 tokens, 耗时 189.83ms
2026-01-09 22:57:53,237 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 3 条历史消息 (token: 1705)
2026-01-09 22:57:53,239 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-09 22:57:53,239 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-09 22:57:53,239 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=20, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-09 22:57:54,406 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-09 22:57:54,410 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-09 22:57:54,423 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-09 22:57:54,423 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=337, cost=$0.000034, time=1171ms
2026-01-09 22:57:54,423 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=7, 尝试次数=1
2026-01-09 22:57:54,423 - app.services.agent.intent.classifier - INFO - [Intent] AI识别结果: writing
2026-01-09 22:57:54,423 - app.services.agent.langgraph_agent - INFO - [Planning] AI意图分类: writing (置信度: 0.90)
2026-01-09 22:57:54,429 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 找到段融被其他杂役弟子嫌弃"一身马粪味"的场景，用展示手法重写他内心的窃喜情绪，同时增强马厩环境的感...
2026-01-09 22:57:54,433 - app.core.cache - INFO - ✅ 缓存命中: prompt:planning:v2.36.0:get_planning_static_prompt:fca6eb91156619d0
2026-01-09 22:57:54,440 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-09 22:57:54,442 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=story_planning, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: story_planning; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-01-09 22:57:54,442 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.3, task_type=TaskType.STORY_PLANNING
2026-01-09 22:58:02,366 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:54803 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 22:58:10,685 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-09 22:58:15,879 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 11 个数据块，总长度: 1312
2026-01-09 22:58:15,879 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 15013 (prompt=14356, completion=657)
2026-01-09 22:58:15,879 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-09 22:58:15,881 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-09 22:58:15,897 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-09 22:58:15,899 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=15013, cost=$0.024515, time=21439ms
2026-01-09 22:58:15,899 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=15013
2026-01-09 22:58:15,899 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户期望获得一个重写后的场景文本。这个文本需要满足两个核心要, 原料=要完成这个任务，首先需要找到用户所描述的, 处理=1. 使用 `search_analys
2026-01-09 22:58:15,899 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共2个任务
2026-01-09 22:58:15,899 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共2个任务，耗时: 21.48s
2026-01-09 22:58:15,899 - app.api.v1.agent - INFO - [Stream] Plan tasks: 2 items
2026-01-09 22:58:15,902 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2026-01-09 22:58:15,902 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2026-01-09 22:58:15,903 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2026-01-09 22:58:15,903 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 任务分组: 第一层并行=1, 第二层并行=0, 串行=1
2026-01-09 22:58:15,905 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始第一层并行执行1个任务
2026-01-09 22:58:15,905 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务1开始: 在作品中搜索“马粪味”相关的场景，找到段融被其他杂役弟子嫌弃的原始片段。
2026-01-09 22:58:15,907 - app.api.v1.agent - INFO - [Stream] Task started: 在作品中搜索“马粪味”相关的场景，找到段融被其他杂役弟子嫌弃的原始片段。 (icon=Search)
2026-01-09 22:58:15,907 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(search_analysis_fragments)
2026-01-09 22:58:15,908 - app.services.agent.tools.tool_types - INFO - [search_analysis_fragments] 开始执行工具
2026-01-09 22:58:15,918 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=9f98efd6-1593-4967-ad43-f5dac759ac1c, current_order=3, query=马粪味...
2026-01-09 22:58:15,983 - app.services.chapter_vector_service - INFO - RAG retrieved 10 segments within order<=5
2026-01-09 22:58:15,990 - app.services.agent.langgraph_tools - INFO - [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
2026-01-09 22:58:15,992 - app.services.agent.tools.tool_types - INFO - [search_analysis_fragments] 执行成功 (耗时: 0.084s)
2026-01-09 22:58:15,992 - app.services.agent.execution.task_runner - INFO - [TaskRunner] search_analysis_fragments 执行成功（DeepAgent模式）
2026-01-09 22:58:15,993 - app.api.v1.agent - INFO - [Stream] 任务完成: 在作品中搜索“马粪味”相关的场景，找到段融被其他杂役弟子嫌弃的原始片段。 (0.1s)
2026-01-09 22:58:15,993 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务1完成
2026-01-09 22:58:15,994 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始串行执行1个任务
2026-01-09 22:58:15,994 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务2开始: 根据用户要求，使用展示手法重写段融的窃喜情绪，并增强马厩环境的感官描写。
2026-01-09 22:58:15,995 - app.api.v1.agent - INFO - [Stream] Task started: 根据用户要求，使用展示手法重写段融的窃喜情绪，并增强马厩环境的感官描写。 (icon=Edit3)
2026-01-09 22:58:15,995 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: smart_rewrite
2026-01-09 22:58:15,995 - app.services.agent.tools.tool_types - INFO - [smart_rewrite] 开始执行工具
2026-01-09 22:58:16,001 - app.services.agent.tools.editor_tools - INFO - [smart_rewrite] 开始生成改写版本，原文长度: 2625, 用户要求: 请用展示手法（Show, Don't Tell）重写主角段融内心的窃喜情绪，与周围其他弟子的嫌弃形成鲜明对比。同时，请重点增强马厩环境的感官描写，比如刺鼻的马粪与干草混合的气味、马匹的响鼻与蹄踏声、从门缝透入的熹微晨光等，让整个场景更加生动立体。, 基准版本: 有
2026-01-09 22:58:16,002 - app.services.agent.tools.editor_tools - INFO - [smart_rewrite] 使用传统单Prompt架构
2026-01-09 22:58:16,002 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-09 22:58:16,002 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=content_creation, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro
2026-01-09 22:58:16,003 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=4000, temp=0.8, 尝试=1/3, task_type=TaskType.CONTENT_CREATION
2026-01-09 22:58:32,369 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/auth/refresh
INFO:     127.0.0.1:62381 - "POST /api/v1/auth/refresh HTTP/1.1" 200 OK
2026-01-09 22:58:32,675 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:62384 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 22:58:49,009 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-09 22:58:49,011 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-09 22:58:49,030 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-09 22:58:49,031 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=5485, cost=$0.012027, time=33010ms
2026-01-09 22:58:49,033 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=842, 尝试次数=1
2026-01-09 22:58:49,033 - app.services.agent.tools.editor_tools - INFO - [smart_rewrite] AI返回长度: 842
2026-01-09 22:58:49,033 - app.services.agent.tools.editor_tools - INFO - [smart_rewrite] 成功生成3个改写版本
2026-01-09 22:58:49,033 - app.services.agent.tools.tool_types - INFO - [smart_rewrite] 执行成功 (耗时: 33.038s)
2026-01-09 22:58:49,036 - app.services.agent.execution.tool_executor - INFO - [StandardTool] smart_rewrite 执行成功
2026-01-09 22:58:49,037 - app.api.v1.agent - INFO - [Stream] 任务完成: 根据用户要求，使用展示手法重写段融的窃喜情绪，并增强马厩环境的感官描写。 (33.0s)
2026-01-09 22:58:49,037 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务2完成
2026-01-09 22:58:49,037 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共2个任务，耗时: 33.14s
2026-01-09 22:58:49,037 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2026-01-09 22:58:49,037 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=1, 输出型=1, 展示型=0
2026-01-09 22:58:49,037 - app.services.agent.langgraph_agent - INFO - [Response] 单个输出任务(smart_rewrite)，使用AI整合
2026-01-09 22:58:49,037 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2026-01-09 22:58:49,037 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=1, 输出型=1, 展示型=0
2026-01-09 22:58:49,037 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=9192字符, 处理后=2771字符
2026-01-09 22:58:49,044 - app.services.agent.planning.response_builder - INFO - [Summarization] 准备发送 summarization_start 事件
2026-01-09 22:58:49,045 - app.services.agent.stream.stream_event_handler - INFO - [StreamEventHandler] emit_summarization_start 被调用, _on_flow_event=True
2026-01-09 22:58:49,045 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_start 事件已发送
2026-01-09 22:58:49,046 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2026-01-09 22:58:49,046 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2026-01-09 22:58:49,058 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-09 22:58:49,059 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-09 22:58:49,060 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
2026-01-09 22:58:50,190 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-09 22:58:50,190 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 0 个数据块，总长度: 0
2026-01-09 22:58:50,190 - app.services.ai.http_ai_service - WARNING - 流式响应未返回usage信息
2026-01-09 22:58:50,190 - app.services.ai.http_ai_service - ERROR - 警告: AI 响应为空！未接收到任何内容块。
2026-01-09 22:58:50,190 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=0
2026-01-09 22:58:51,747 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:9f98efd6-1593-4967-ad43-f5dac759ac1c | 重要度=0.65
2026-01-09 22:58:51,753 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:1b0b2d85-6715-4606-98dc-81cee1748897, token=1803
2026-01-09 22:58:51,755 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:1b0b2d85-6715-4606-98dc-81cee1748897, 消息数=4, Token=1803
2026-01-09 22:58:51,756 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:1b0b2d85-6715-4606-98dc-81cee1748897)
2026-01-09 22:58:51,760 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed
2026-01-09 22:59:02,387 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:58079 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 22:59:32,391 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:49579 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 23:00:02,589 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:54011 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 23:00:32,660 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:59040 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 23:01:02,660 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:56497 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 23:01:32,671 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:62393 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 23:02:02,684 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:49819 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 23:02:32,697 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:60016 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 23:03:02,354 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:57994 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2026-01-09 23:03:02,909 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:57997 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 23:03:32,932 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:55182 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 23:04:02,967 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:60016 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 23:04:33,063 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:54217 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 23:04:43,182 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 9f98efd6-1593-4967-ad43-f5dac759ac1c, chapter_id: 8e929bfb-3056-4183-ac21-d1aca962248d
2026-01-09 23:04:43,195 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 8e929bfb-3056-4183-ac21-d1aca962248d
2026-01-09 23:04:43,195 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
2026-01-09 23:04:43,196 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:62558 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-09 23:04:43,210 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 9f98efd6-1593-4967-ad43-f5dac759ac1c, chapter_id: 8e929bfb-3056-4183-ac21-d1aca962248d
2026-01-09 23:04:43,223 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 8e929bfb-3056-4183-ac21-d1aca962248d
2026-01-09 23:04:43,223 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
2026-01-09 23:04:43,225 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:62561 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-09 23:04:43,688 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:9f98efd6-1593-4967-ad43-f5dac759ac1c
2026-01-09 23:04:43,690 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/8e929bfb-3056-4183-ac21-d1aca962248d
INFO:     127.0.0.1:57750 - "PUT /api/v1/chapters/8e929bfb-3056-4183-ac21-d1aca962248d HTTP/1.1" 200 OK
2026-01-09 23:04:43,691 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-09 23:04:45,083 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (5 chunks)
2026-01-09 23:04:45,097 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:9f98efd6-1593-4967-ad43-f5dac759ac1c
2026-01-09 23:04:45,098 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/8e929bfb-3056-4183-ac21-d1aca962248d
INFO:     127.0.0.1:57753 - "PUT /api/v1/chapters/8e929bfb-3056-4183-ac21-d1aca962248d HTTP/1.1" 200 OK
2026-01-09 23:04:45,104 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-09 23:04:46,307 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (5 chunks)
2026-01-09 23:04:48,381 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-09 23:04:48,381 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-09 23:04:48,381 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2026-01-09 23:04:49,932 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-09 23:04:49,934 - app.api.v1.agent - INFO - [Chat Stream] Mode: planning
2026-01-09 23:04:49,937 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:57756 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2026-01-09 23:04:49,949 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 先查看世界观中关于器灵等阶的设定，然后分析第1章中段融读取器灵数据的描写风格，学习这种"系统面板"的...
2026-01-09 23:04:49,963 - app.api.v1.agent - INFO - [agent_chat_stream] 📚 世界观数据已注入: 人物=9, 地点=6, 设定=6, 规范=无
2026-01-09 23:04:49,963 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:0fd87250-a111-4d14-8804-ba6cd06e776d (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=9f98efd6-1593-4967-ad43-f5dac759ac1c, conversation_id=0fd87250-a111-4d14-8804-ba6cd06e776d)
2026-01-09 23:04:49,967 - app.services.context.store - INFO - [ContextStore] 加载上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:0fd87250-a111-4d14-8804-ba6cd06e776d, 2条消息
2026-01-09 23:04:49,971 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:9f98efd6-1593-4967-ad43-f5dac759ac1c:0fd87250-a111-4d14-8804-ba6cd06e776d: 2227/16000 tokens
2026-01-09 23:04:50,257 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='先查看世界观中关于器灵等阶的设定，然后分析第1章中段融读取器...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:9f98efd6-1593-4967-ad43-f5dac759ac1c', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=3条
2026-01-09 23:04:50,258 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=9f98efd6-1593-4967-ad43-f5dac759ac1c | 含用户级=True | 找到=3条
2026-01-09 23:04:50,262 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 3条消息, 2227 tokens, 耗时 298.90ms
2026-01-09 23:04:50,262 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 3 条历史消息 (token: 2227)
2026-01-09 23:04:50,262 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-09 23:04:50,262 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-09 23:04:50,262 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=20, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-09 23:04:52,365 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-09 23:04:52,369 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-09 23:04:52,387 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-09 23:04:52,391 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=354, cost=$0.000036, time=2108ms
2026-01-09 23:04:52,391 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=7, 尝试次数=1
2026-01-09 23:04:52,391 - app.services.agent.intent.classifier - INFO - [Intent] AI识别结果: writing
2026-01-09 23:04:52,393 - app.services.agent.langgraph_agent - INFO - [Planning] AI意图分类: writing (置信度: 0.90)
2026-01-09 23:04:52,394 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 先查看世界观中关于器灵等阶的设定，然后分析第1章中段融读取器灵数据的描写风格，学习这种"系统面板"的...
2026-01-09 23:04:52,398 - app.core.cache - INFO - ⚠️ 缓存未命中: prompt:planning:v2.36.0:get_planning_static_prompt:fca6eb91156619d0
2026-01-09 23:04:52,430 - app.core.cache - INFO - 💾 缓存已保存: prompt:planning:v2.36.0:get_planning_static_prompt:fca6eb91156619d0 (expire=3600s)
2026-01-09 23:04:52,435 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-09 23:04:52,436 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=story_planning, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: story_planning; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-01-09 23:04:52,437 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.3, task_type=TaskType.STORY_PLANNING
2026-01-09 23:05:02,965 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:60299 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 23:05:10,921 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-09 23:05:18,510 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 17 个数据块，总长度: 2270
2026-01-09 23:05:18,510 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 15756 (prompt=14642, completion=1114)
2026-01-09 23:05:18,510 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-09 23:05:18,510 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-09 23:05:18,518 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-09 23:05:18,519 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=15756, cost=$0.029442, time=26073ms
2026-01-09 23:05:18,519 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=15756
2026-01-09 23:05:18,519 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户期望的输出是一个包含新创作内容的新章节片段。这个片段需要, 原料=要完成这个任务，我需要以下原料：
1. , 处理=处理流程如下：
1. 调用 `get_w
2026-01-09 23:05:18,519 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共5个任务
2026-01-09 23:05:18,519 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共5个任务，耗时: 26.13s
2026-01-09 23:05:18,519 - app.api.v1.agent - INFO - [Stream] Plan tasks: 5 items
2026-01-09 23:05:18,519 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2026-01-09 23:05:18,519 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2026-01-09 23:05:18,519 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2026-01-09 23:05:18,519 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 任务分组: 第一层并行=2, 第二层并行=1, 串行=2
2026-01-09 23:05:18,519 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始第一层并行执行2个任务
2026-01-09 23:05:18,519 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务2开始: 获取第一章内容，用于分析“系统面板”的描写风格
2026-01-09 23:05:18,519 - app.api.v1.agent - INFO - [Stream] Task started: 获取第一章内容，用于分析“系统面板”的描写风格 (icon=FileText)
2026-01-09 23:05:18,519 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(get_chapter_by_order)
2026-01-09 23:05:18,519 - app.services.agent.tools.tool_types - INFO - [get_chapter_by_order] 开始执行工具
2026-01-09 23:05:18,519 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务4开始: 获取当前章节的完整内容，作为续写上下文
2026-01-09 23:05:18,519 - app.api.v1.agent - INFO - [Stream] Task started: 获取当前章节的完整内容，作为续写上下文 (icon=FileText)
2026-01-09 23:05:18,519 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(read_chapter)
2026-01-09 23:05:18,519 - app.services.agent.tools.tool_types - INFO - [read_chapter] 开始执行工具
2026-01-09 23:05:18,519 - app.services.agent.langgraph_tools - INFO - [read_chapter_tool] ✅ 读取章节成功: 第1章 吞噬
2026-01-09 23:05:18,530 - app.services.agent.langgraph_tools - INFO - [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
2026-01-09 23:05:18,533 - app.services.agent.tools.tool_types - INFO - [read_chapter] 执行成功 (耗时: 0.014s)
2026-01-09 23:05:18,533 - app.services.agent.execution.task_runner - INFO - [TaskRunner] read_chapter 执行成功（DeepAgent模式）
2026-01-09 23:05:18,533 - app.api.v1.agent - INFO - [Stream] 任务完成: 获取当前章节的完整内容，作为续写上下文 (0.0s)
2026-01-09 23:05:18,534 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务4完成
2026-01-09 23:05:18,534 - app.services.agent.tools.tool_types - INFO - [get_chapter_by_order] 执行成功 (耗时: 0.015s)
2026-01-09 23:05:18,534 - app.services.agent.execution.task_runner - INFO - [TaskRunner] get_chapter_by_order 执行成功（DeepAgent模式）
2026-01-09 23:05:18,534 - app.api.v1.agent - INFO - [Stream] 任务完成: 获取第一章内容，用于分析“系统面板”的描写风格 (0.0s)
2026-01-09 23:05:18,534 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务2完成
2026-01-09 23:05:18,536 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始第二层并行执行1个任务
2026-01-09 23:05:18,536 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第二层任务3开始: 分析第一章中“系统面板”的写作手法
2026-01-09 23:05:18,536 - app.api.v1.agent - INFO - [Stream] Task started: 分析第一章中“系统面板”的写作手法 (icon=BarChart2)
2026-01-09 23:05:18,536 - app.services.agent.execution.task_runner - INFO - [TaskRunner] analyze_text_tool 使用 focus: '分析“系统面板”数据的描写风格和格式...'
2026-01-09 23:05:18,536 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(analyze_text)
2026-01-09 23:05:18,536 - app.services.agent.tools.tool_types - INFO - [analyze_text] 开始执行工具
2026-01-09 23:05:18,536 - app.services.agent.tools.analysis_tools - INFO - [analyze_text_tool] 尝试第 1 次调用，config={'temperature': 0.3, 'task_type': <TaskType.SUMMARIZATION: 'summarization'>}
2026-01-09 23:05:18,540 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-09 23:05:18,540 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-09 23:05:18,540 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
2026-01-09 23:05:27,541 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-09 23:05:29,760 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 7 个数据块，总长度: 701
2026-01-09 23:05:29,760 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 3817 (prompt=3364, completion=453)
2026-01-09 23:05:29,760 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-09 23:05:29,760 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-09 23:05:29,768 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-09 23:05:29,769 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=3817, cost=$0.002142, time=11219ms
2026-01-09 23:05:29,769 - app.services.agent.tools.analysis_tools - INFO - [analyze_text_tool] 第 1 次调用成功
2026-01-09 23:05:29,769 - app.services.agent.tools.analysis_tools - INFO - [analyze_text_tool] 分析完成，结果长度: 701
2026-01-09 23:05:29,769 - app.services.agent.tools.tool_types - INFO - [analyze_text] 执行成功 (耗时: 11.233s)
2026-01-09 23:05:29,769 - app.services.agent.execution.task_runner - INFO - [TaskRunner] analyze_text 执行成功（DeepAgent模式）
2026-01-09 23:05:29,769 - app.api.v1.agent - INFO - [Stream] 任务完成: 分析第一章中“系统面板”的写作手法 (11.2s)
2026-01-09 23:05:29,769 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第二层任务3完成
2026-01-09 23:05:29,769 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始串行执行2个任务
2026-01-09 23:05:29,769 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务1开始: 查看世界观中关于器灵等阶的设定
2026-01-09 23:05:29,769 - app.api.v1.agent - INFO - [Stream] Task started: 查看世界观中关于器灵等阶的设定 (icon=Wrench)
2026-01-09 23:05:29,769 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: get_worldview_summary
2026-01-09 23:05:29,769 - app.services.agent.tools.tool_types - INFO - [get_worldview_summary] 开始执行工具
2026-01-09 23:05:29,778 - app.services.agent.langgraph_tools - INFO - [get_worldview_summary] ✅ 获取世界观摘要成功: {'characters': 9, 'locations': 6, 'settings': 6}
2026-01-09 23:05:29,780 - app.services.agent.tools.tool_types - INFO - [get_worldview_summary] 执行成功 (耗时: 0.012s)
2026-01-09 23:05:29,780 - app.services.agent.execution.tool_executor - INFO - [StandardTool] get_worldview_summary 执行成功
2026-01-09 23:05:29,780 - app.api.v1.agent - INFO - [Stream] 任务完成: 查看世界观中关于器灵等阶的设定 (0.0s)
2026-01-09 23:05:29,780 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务1完成
2026-01-09 23:05:29,780 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务5开始: 创作段融吞噬高阶器物的场景，并更新到章节中
2026-01-09 23:05:29,780 - app.api.v1.agent - INFO - [Stream] Task started: 创作段融吞噬高阶器物的场景，并更新到章节中 (icon=PenTool)
2026-01-09 23:05:29,780 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(smart_continue)
2026-01-09 23:05:29,780 - app.services.agent.tools.tool_types - INFO - [smart_continue] 开始执行工具
2026-01-09 23:05:29,786 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-09 23:05:29,786 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=content_creation, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro
2026-01-09 23:05:29,794 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=1000, temp=0.8, 尝试=1/3, task_type=TaskType.CONTENT_CREATION
2026-01-09 23:05:32,977 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:60653 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 23:06:00,216 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-09 23:06:00,216 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-09 23:06:00,218 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-09 23:06:00,218 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=3728, cost=$0.009656, time=30422ms
2026-01-09 23:06:00,218 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=698, 尝试次数=1
2026-01-09 23:06:00,218 - app.services.agent.tools.tool_types - INFO - [smart_continue] 执行成功 (耗时: 30.438s)
2026-01-09 23:06:00,218 - app.services.agent.execution.task_runner - INFO - [TaskRunner] smart_continue 执行成功（DeepAgent模式）
2026-01-09 23:06:00,218 - app.services.agent.langgraph_agent - WARNING - [HITL] 审批回调执行失败: name 'hitl' is not defined
2026-01-09 23:06:00,218 - app.api.v1.agent - INFO - [Stream] 任务完成: 创作段融吞噬高阶器物的场景，并更新到章节中 (30.4s)
2026-01-09 23:06:00,218 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务5完成
2026-01-09 23:06:00,218 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共5个任务，耗时: 41.70s
2026-01-09 23:06:00,218 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2026-01-09 23:06:00,229 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=3, 输出型=2, 展示型=0
2026-01-09 23:06:00,229 - app.services.agent.langgraph_agent - INFO - [Response] 2个输出任务（含续写），使用AI整合
2026-01-09 23:06:00,229 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2026-01-09 23:06:00,229 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=3, 输出型=2, 展示型=0
2026-01-09 23:06:00,229 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=10602字符, 处理后=5690字符
2026-01-09 23:06:00,229 - app.services.agent.planning.response_builder - INFO - [Summarization] 准备发送 summarization_start 事件
2026-01-09 23:06:00,229 - app.services.agent.stream.stream_event_handler - INFO - [StreamEventHandler] emit_summarization_start 被调用, _on_flow_event=True
2026-01-09 23:06:00,229 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_start 事件已发送
2026-01-09 23:06:00,229 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2026-01-09 23:06:00,231 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2026-01-09 23:06:00,233 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-09 23:06:00,233 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-09 23:06:00,233 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
2026-01-09 23:06:03,505 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:51572 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 23:06:03,526 - app.services.chapter_word_stat_service - INFO - 记录字数增量: chapter_id=8e929bfb-3056-4183-ac21-d1aca962248d, delta=588, edit_event_id=23240d18-1d8e-4969-906e-6d8b1743b6af
2026-01-09 23:06:03,526 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 8e929bfb-3056-4183-ac21-d1aca962248d 内容更新，新段落数: 97
[TaskService] Checking daily writing task for user 79913e7e-d5cd-4e09-bce6-ca6639bd8456, word_count: 1253
[TaskService] Daily writing task result: None
2026-01-09 23:06:03,538 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:9f98efd6-1593-4967-ad43-f5dac759ac1c
2026-01-09 23:06:03,539 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/8e929bfb-3056-4183-ac21-d1aca962248d
INFO:     127.0.0.1:51574 - "PUT /api/v1/chapters/8e929bfb-3056-4183-ac21-d1aca962248d HTTP/1.1" 200 OK
2026-01-09 23:06:03,539 - app.services.chapter_vector_service - I
2026-01-09 23:07:03,544 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:52012 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 23:07:33,555 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:64956 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 23:07:38,746 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 347 个数据块，总长度: 687349
2026-01-09 23:07:38,747 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 28661 (prompt=5776, completion=22885)
2026-01-09 23:07:38,747 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-09 23:07:38,747 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-09 23:07:38,768 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-09 23:07:38,768 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=28661, cost=$0.058945, time=98514ms
2026-01-09 23:07:38,768 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=687349
2026-01-09 23:07:39,718 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:9f98efd6-1593-4967-ad43-f5dac759ac1c | 重要度=1.00
2026-01-09 23:07:41,221 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:9f98efd6-1593-4967-ad43-f5dac759ac1c | 重要度=0.60NFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-09 23:06:03,777 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (7 chunks)
2026-01-09 23:06:03,785 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:9f98efd6-1593-4967-ad43-f5dac759ac1c
2026-01-09 23:06:03,786 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/8e929bfb-3056-4183-ac21-d1aca962248d
INFO:     127.0.0.1:51577 - "PUT /api/v1/chapters/8e929bfb-3056-4183-ac21-d1aca962248d HTTP/1.1" 200 OK
2026-01-09 23:06:03,787 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-09 23:06:03,983 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (7 chunks)
2026-01-09 23:06:15,022 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-09 23:06:15,022 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_complete 事件已发送（第一个chunk时）
2026-01-09 23:06:15,022 - app.services.agent.planning.response_builder - INFO - [Summarization] output_ready 事件已发送（第一个chunk时）
2026-01-09 23:06:33,652 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:49983 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 23:07:03,544 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:52012 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 23:07:33,555 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:64956 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-09 23:07:38,746 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 347 个数据块，总长度: 687349
2026-01-09 23:07:38,747 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 28661 (prompt=5776, completion=22885)
2026-01-09 23:07:38,747 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-09 23:07:38,747 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-09 23:07:38,768 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-09 23:07:38,768 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=28661, cost=$0.058945, time=98514ms
2026-01-09 23:07:38,768 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=687349
2026-01-09 23:07:39,718 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:9f98efd6-1593-4967-ad43-f5dac759ac1c | 重要度=1.00
2026-01-09 23:07:41,221 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:9f98efd6-1593-4967-ad43-f5dac759ac1c | 重要度=0.60