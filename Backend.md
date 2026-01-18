INFO:     127.0.0.1:60526 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2026-01-18 11:31:48,675 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 请全面梳理林仙的"摆烂策略"与核心机遇，包括：

  1. 林仙与系统10086的关系演变过程：
 ...
2026-01-18 11:31:48,680 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-18 11:31:48,683 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-18 11:31:48,684 - app.services.ai.http_ai_service - INFO - [成本追踪] 初始化未传db/user_id，将使用请求上下文按需记录成本
2026-01-18 11:31:52,850 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-18 11:31:52,854 - app.services.agent.tools.writing_tools - INFO - Writing tools AI service initialized
2026-01-18 11:31:52,855 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ AI Service 已同时设置到 langgraph_tools 和 writing_tools
2026-01-18 11:31:52,856 - app.services.context.adaptive_budget - INFO - ✅ 所有预算配置验证通过
2026-01-18 11:32:00,048 - app.services.context.vector_memory_store - INFO - ✅ VectorMemoryStore初始化成功 | 目录=./data/chroma_db | 模型=paraphrase-multilingual-MiniLM-L12-v2 | 集合=user_memories
2026-01-18 11:32:00,048 - app.services.context.manager - INFO - ✅ VectorMemoryStore 已初始化
2026-01-18 11:32:00,048 - app.services.context.manager - INFO - ✅ ContextManager: 长期记忆已启用 (user_id=None)
2026-01-18 11:32:00,048 - app.services.context.manager - INFO - ✅ ContextManager: 自适应预算已启用
2026-01-18 11:32:00,048 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ ContextManager已初始化（长期记忆已启用，自适应预算已启用，总预算=16000 tokens）
成功加载模板: analyze_text (版本 3.1.0)
成功加载模板: writing_agent (版本 2.0.0)
成功加载模板: system_agent_prompt (版本 2.1.0)
成功加载模板: creative_writing_prompt (版本 1.0.0)
2026-01-18 11:32:00,065 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ PromptManager已初始化
2026-01-18 11:32:00,074 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ Redis连接验证成功
2026-01-18 11:32:00,075 - app.services.agent.langgraph_agent - INFO - [LangGraph] OK 使用 AsyncRedisSaver（redis://localhost:6379/0，TTL=7天）
2026-01-18 11:32:00,076 - app.services.agent.memory.metrics - INFO - [MemoryMetrics] 监控系统已初始化
2026-01-18 11:32:00,076 - app.services.agent.memory.long_term_store - INFO - [LongTermStore] Initialized: base_dir=./data/long_term_memory, max_size=50KB, compression=True
2026-01-18 11:32:00,076 - app.services.agent.memory.enhanced_memory_manager - INFO - EnhancedMemoryManager initialized: short=10, medium=100, threshold=0.1, long_term_backup=enabled
2026-01-18 11:32:00,076 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ EnhancedMemoryManager已创建
2026-01-18 11:32:00,077 - app.services.agent.memory.unified_coordinator - INFO - [UnifiedMemoryCoordinator] 初始化统一记忆协调器
2026-01-18 11:32:00,077 - app.services.agent.memory.unified_coordinator - INFO - [UnifiedMemoryCoordinator] 全局实例已设置
2026-01-18 11:32:00,077 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ UnifiedMemoryCoordinator已初始化 | checkpointer=AsyncRedisSaver | enhanced_memory=yes | context_manager=yes
2026-01-18 11:32:00,077 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ 解耦模块已初始化 (IntentClassifier, ToolExecutor, EventParser, ResponseBuilder, ToolDispatcher, ParallelExecutor, PlanGenerator, QuickPathHandler, StreamEventHandler, SecondaryToolHandler, TaskRunner, AgentExecutor)
2026-01-18 11:32:00,082 - app.services.agent.parallel_tool_node - INFO - [ParallelToolNode] 初始化完成，最大并发数=5，并行安全工具=6个
2026-01-18 11:32:00,088 - app.api.v1.agent - INFO - [Global Agent] created global agent instance; MemorySaver shared across requests
2026-01-18 11:32:00,107 - app.api.v1.agent - INFO - [agent_chat_stream] 📚 世界观数据已注入: 人物=10, 地点=8, 设定=7, 规范=无
2026-01-18 11:32:00,110 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:dc4e73dc-d64f-4669-a984-2fa3d9efea9d:4a879457-ade8-4e57-b680-db07e405fbec (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=dc4e73dc-d64f-4669-a984-2fa3d9efea9d, conversation_id=4a879457-ade8-4e57-b680-db07e405fbec)
2026-01-18 11:32:00,110 - app.services.context.monitoring_integration - INFO - ✅ ContextManager监控收集器已初始化
2026-01-18 11:32:00,111 - app.services.context.store - INFO - [ContextStore] Redis连接成功
2026-01-18 11:32:00,116 - app.services.context.manager - INFO - [ContextManager] 创建新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:dc4e73dc-d64f-4669-a984-2fa3d9efea9d:4a879457-ade8-4e57-b680-db07e405fbec
2026-01-18 11:32:00,211 - app.services.context.token_counter - INFO - ✅ tiktoken初始化成功，模型: gemini-2.5-pro -> cl100k_base
2026-01-18 11:32:00,220 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:dc4e73dc-d64f-4669-a984-2fa3d9efea9d:4a879457-ade8-4e57-b680-db07e405fbec: 0/16000 tokens
2026-01-18 11:32:00,457 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='请全面梳理林仙的"摆烂策略"与核心机遇，包括：

  1. ...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:dc4e73dc-d64f-4669-a984-2fa3d9efea9d', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=3条
2026-01-18 11:32:00,457 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=dc4e73dc-d64f-4669-a984-2fa3d9efea9d | 含用户级=True | 找到=3条
2026-01-18 11:32:00,492 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 1条消息, 0 tokens, 耗时 380.95ms
2026-01-18 11:32:00,492 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 1 条历史消息 (token: 0, has_summary: False)
2026-01-18 11:32:00,492 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-18 11:32:00,492 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-18 11:32:00,492 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=200, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-18 11:32:01,951 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-18 11:32:01,951 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-18 11:32:01,978 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-18 11:32:01,979 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=662, cost=$0.000072, time=1459ms
2026-01-18 11:32:01,979 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=39, 尝试次数=1
2026-01-18 11:32:01,979 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-18 11:32:01,979 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-18 11:32:01,979 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=20, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-18 11:32:02,949 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-18 11:32:02,949 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-18 11:32:02,959 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-18 11:32:02,959 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=586, cost=$0.000059, time=970ms
2026-01-18 11:32:02,959 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=8, 尝试次数=1
2026-01-18 11:32:02,959 - app.services.agent.intent.classifier - INFO - [Intent] AI识别结果: analysis
2026-01-18 11:32:02,970 - app.services.agent.langgraph_agent - INFO - [Planning] AI意图分类: analysis (置信度: 0.90)
2026-01-18 11:32:02,970 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 请全面梳理林仙的"摆烂策略"与核心机遇，包括：

  1. 林仙与系统10086的关系演变过程：
 ...
2026-01-18 11:32:02,978 - app.core.cache - INFO - ✅ 缓存命中: prompt:planning:v2.39.1:get_planning_static_prompt:fca6eb91156619d0
2026-01-18 11:32:02,982 - app.services.agent.planning.plan_generator - INFO - [Planning] 检测到枚举项: ['摆烂策略', '试炼任务', '宿主系统命运共同体', '八奇技之一', '躺赢逻辑', '龙虎山天师府门人', '看相', '与核心机遇', '包括', '炁婴', '元婴', '苦海', '生命之轮这些概念的关系是什么', '小赢', '中赢', '大赢', '超大赢分别对应什么修为目标', '庞博最终成为道祖', '这对林仙的策略有什么启示', '请引用原文证据', '分析林仙的摆烂哲学与生存智慧']
2026-01-18 11:32:02,984 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-18 11:32:02,984 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=story_planning, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: story_planning; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-01-18 11:32:02,985 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.3, task_type=TaskType.STORY_PLANNING
2026-01-18 11:32:21,381 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-18 11:32:45,390 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 36 个数据块，总长度: 3304
2026-01-18 11:32:45,390 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 27815 (prompt=25505, completion=2310)
2026-01-18 11:32:45,390 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-18 11:32:45,390 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-18 11:32:45,410 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-18 11:32:45,411 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=27815, cost=$0.054981, time=42404ms
2026-01-18 11:32:45,413 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=27815
2026-01-18 11:32:45,413 - app.services.agent.planning.plan_generator - WARNING - [Planning] 第1次尝试: JSON解析失败
2026-01-18 11:32:46,429 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-18 11:32:46,429 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=story_planning, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: story_planning; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-01-18 11:32:46,429 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.4, task_type=TaskType.STORY_PLANNING
2026-01-18 11:32:57,709 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-18 11:33:01,503 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 8 个数据块，总长度: 876
2026-01-18 11:33:01,503 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 25347 (prompt=24902, completion=445)
2026-01-18 11:33:01,503 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-18 11:33:01,503 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-18 11:33:01,517 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-18 11:33:01,517 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=25347, cost=$0.035578, time=15074ms
2026-01-18 11:33:01,517 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=25347
2026-01-18 11:33:01,517 - app.services.agent.planning.plan_generator - WARNING - [Planning] 枚举项覆盖不完整，缺失: ['试炼任务', '宿主系统命运共同体', '八奇技之一', '龙虎山天师府门人', '看相', '炁婴', '元婴', '苦海', '生命之轮这些概念的关系是什么', '小赢', '中赢', '大赢', '超大赢分别对应什么修为目标', '庞博最终成为道祖', '这对林仙的策略有什么启示', '请引用原文证据', '分析林仙的摆烂哲学与生存智慧']
2026-01-18 11:33:01,517 - app.services.agent.planning.plan_generator - INFO - [Planning] 第2次重试成功
2026-01-18 11:33:01,517 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户需要一份关于角色“林仙”的全面分析报告，内容涵盖他与系统, 原料=为了回答用户的所有问题并引用原文，我需要, 处理=1. 使用 explore_conten
2026-01-18 11:33:01,529 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共1个任务
2026-01-18 11:33:01,529 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共1个任务，耗时: 58.56s
2026-01-18 11:33:01,529 - app.api.v1.agent - INFO - [Stream] Plan tasks: 1 items
2026-01-18 11:33:01,529 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2026-01-18 11:33:01,529 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2026-01-18 11:33:01,529 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2026-01-18 11:33:01,529 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] DAG 调度启用，任务数=1, 有依赖任务=0
2026-01-18 11:33:01,529 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1开始: 全面梳理林仙的'摆烂策略'与核心机遇，包括他与系统的关系、获得的技能、躺赢逻辑以及在青铜棺内的行为。
2026-01-18 11:33:01,529 - app.api.v1.agent - INFO - [Stream] Task started: 全面梳理林仙的'摆烂策略'与核心机遇，包括他与系统的关系、获得的技能、躺赢逻辑以及在青铜棺内的行为。 (icon=Wrench)
2026-01-18 11:33:01,529 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: explore_content
2026-01-18 11:33:01,534 - app.services.agent.tools.explore_tools - INFO - [explore_content] 开始: work_id=dc4e73dc-d64f-4669-a984-2fa3d9efea9d, target=全面梳理林仙的'摆烂策略'与核心机遇，包括他与系统的关系、获得的技能、躺赢逻辑以及在青铜棺内的行为。...
2026-01-18 11:33:01,534 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 开始探索: work_id=dc4e73dc-d64f-4669-a984-2fa3d9efea9d, target=全面梳理林仙的'摆烂策略'与核心机遇，包括他与系统的关系、获得的技能、躺赢逻辑以及在青铜棺内的行为。...
2026-01-18 11:33:01,548 - app.services.agent.langgraph_tools - INFO - [get_writing_context] ✅ 获取创作上下文成功: include=worldview
2026-01-18 11:33:02,002 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=dc4e73dc-d64f-4669-a984-2fa3d9efea9d, current_order=1000000, query=全面梳理林仙的 摆烂策略 与核心机遇...
2026-01-18 11:33:02,321 - app.services.chapter_vector_service - INFO - RAG retrieved 10 segments within order<=2000000
Building prefix dict from the default dictionary ...
2026-01-18 11:33:02,324 - jieba - DEBUG - Building prefix dict from the default dictionary ...
Loading model from cache D:\Temp\jieba.cache
2026-01-18 11:33:02,325 - jieba - DEBUG - Loading model from cache D:\Temp\jieba.cache
Loading model cost 0.433 seconds.
2026-01-18 11:33:02,758 - jieba - DEBUG - Loading model cost 0.433 seconds.
Prefix dict has been built successfully.
2026-01-18 11:33:02,758 - jieba - DEBUG - Prefix dict has been built successfully.
2026-01-18 11:33:02,807 - app.services.search.hybrid_retriever - INFO - [Reranker] 正在加载模型: BAAI/bge-reranker-base
2026-01-18 11:33:05,596 - app.services.search.hybrid_retriever - INFO - [Reranker] 模型加载成功
2026-01-18 11:33:14,860 - app.services.search.hybrid_retriever - INFO - [Rerank] 重排序完成: 15 个候选 -> top 5
2026-01-18 11:33:14,860 - app.services.agent.langgraph_tools - INFO - [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
2026-01-18 11:33:14,866 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=dc4e73dc-d64f-4669-a984-2fa3d9efea9d, current_order=1000000, query=全面梳理林仙的...
2026-01-18 11:33:15,279 - app.services.chapter_vector_service - INFO - RAG retrieved 10 segments within order<=2000000
2026-01-18 11:33:22,494 - app.services.search.hybrid_retriever - INFO - [Rerank] 重排序完成: 12 个候选 -> top 5
2026-01-18 11:33:22,495 - app.services.agent.langgraph_tools - INFO - [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
2026-01-18 11:33:22,499 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=dc4e73dc-d64f-4669-a984-2fa3d9efea9d, current_order=1000000, query=摆烂策略...
2026-01-18 11:33:22,941 - app.services.chapter_vector_service - INFO - RAG retrieved 10 segments within order<=2000000
2026-01-18 11:33:42,132 - app.services.search.hybrid_retriever - INFO - [Rerank] 重排序完成: 9 个候选 -> top 5
2026-01-18 11:33:42,135 - app.services.agent.langgraph_tools - INFO - [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
2026-01-18 11:33:42,197 - app.services.agent.langgraph_tools - INFO - [get_writing_context] ✅ 获取创作上下文成功: include=chapter
2026-01-18 11:33:42,246 - app.services.agent.langgraph_tools - INFO - [get_writing_context] ✅ 获取创作上下文成功: include=chapter
2026-01-18 11:33:42,262 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=dc4e73dc-d64f-4669-a984-2fa3d9efea9d, current_order=1000000, query=与核心机遇...
2026-01-18 11:33:43,957 - app.services.chapter_vector_service - INFO - RAG retrieved 10 segments within order<=2000000
2026-01-18 11:34:15,851 - app.services.search.hybrid_retriever - INFO - [Rerank] 重排序完成: 15 个候选 -> top 5
2026-01-18 11:34:15,851 - app.services.agent.langgraph_tools - INFO - [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
2026-01-18 11:34:15,868 - app.services.agent.langgraph_tools - INFO - [get_writing_context] ✅ 获取创作上下文成功: include=chapter
2026-01-18 11:34:15,886 - app.services.agent.langgraph_tools - INFO - [get_writing_context] ✅ 获取创作上下文成功: include=chapter
2026-01-18 11:34:15,902 - app.services.agent.langgraph_tools - INFO - [get_writing_context] ✅ 获取创作上下文成功: include=chapter
2026-01-18 11:34:15,918 - app.services.agent.langgraph_tools - INFO - [get_writing_context] ✅ 获取创作上下文成功: include=chapter
2026-01-18 11:34:15,921 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 达到 3 轮，强制判断为充足
2026-01-18 11:34:15,921 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 探索完成: 3轮, 原因=AI 判断信息充足
2026-01-18 11:34:15,923 - app.services.agent.execution.tool_executor - INFO - [StandardTool] explore_content 执行成功
2026-01-18 11:34:15,924 - app.services.agent.execution.parallel_executor - WARNING - [ParallelExecution] explore_content 结果解析失败
2026-01-18 11:34:15,924 - app.api.v1.agent - INFO - [Stream] 任务完成: 全面梳理林仙的'摆烂策略'与核心机遇，包括他与系统的关系、获得的技能、躺赢逻辑以及在青铜棺内的行为。 (74.4s)
2026-01-18 11:34:15,925 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1完成
2026-01-18 11:34:15,926 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共1个任务，耗时: 74.40s
2026-01-18 11:34:15,926 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2026-01-18 11:34:15,926 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=1, 展示型=0
2026-01-18 11:34:15,927 - app.services.agent.langgraph_agent - INFO - [Response] 单个输出任务(explore_content)，使用AI整合
2026-01-18 11:34:15,927 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2026-01-18 11:34:15,927 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=1, 展示型=0
2026-01-18 11:34:15,927 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=6363字符, 处理后=569字符
2026-01-18 11:34:15,927 - app.services.agent.planning.response_builder - INFO - [Summarization] 准备发送 summarization_start 事件
2026-01-18 11:34:15,929 - app.services.agent.stream.stream_event_handler - INFO - [StreamEventHandler] emit_summarization_start 被调用, _on_flow_event=True
2026-01-18 11:34:15,930 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_start 事件已发送
2026-01-18 11:34:15,930 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2026-01-18 11:34:15,930 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2026-01-18 11:34:15,937 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-18 11:34:15,937 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-18 11:34:15,939 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
2026-01-18 11:34:25,569 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-18 11:34:25,569 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_complete 事件已发送（第一个chunk时）
2026-01-18 11:34:25,569 - app.services.agent.planning.response_builder - INFO - [Summarization] output_ready 事件已发送（第一个chunk时）
2026-01-18 11:34:29,648 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 13 个数据块，总长度: 1152
2026-01-18 11:34:29,648 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 5409 (prompt=4608, completion=801)
2026-01-18 11:34:29,648 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-18 11:34:29,648 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-18 11:34:29,662 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-18 11:34:29,662 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=5409, cost=$0.003385, time=13708ms
2026-01-18 11:34:29,662 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=1152
2026-01-18 11:34:29,989 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:dc4e73dc-d64f-4669-a984-2fa3d9efea9d | 重要度=0.60
2026-01-18 11:34:30,166 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:dc4e73dc-d64f-4669-a984-2fa3d9efea9d | 重要度=0.60
2026-01-18 11:34:30,171 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:dc4e73dc-d64f-4669-a984-2fa3d9efea9d:4a879457-ade8-4e57-b680-db07e405fbec, token=1693
2026-01-18 11:34:30,171 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:dc4e73dc-d64f-4669-a984-2fa3d9efea9d:4a879457-ade8-4e57-b680-db07e405fbec, 消息数=2, 摘要长度=0, Token=1693
2026-01-18 11:34:30,172 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:dc4e73dc-d64f-4669-a984-2fa3d9efea9d:4a879457-ade8-4e57-b680-db07e405fbec)
2026-01-18 11:34:30,172 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）