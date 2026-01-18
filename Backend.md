INFO:     127.0.0.1:55619 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2026-01-18 22:23:43,297 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 请深度分析本作中"祭道之上"概念对剧情因果的影响：

  1. 时间线逻辑：遮天三部曲（完美世界-遮...
2026-01-18 22:23:43,304 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-18 22:23:43,307 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-18 22:23:43,309 - app.services.ai.http_ai_service - INFO - [成本追踪] 初始化未传db/user_id，将使用请求上下文按需记录成本
2026-01-18 22:23:49,538 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-18 22:23:49,542 - app.services.agent.tools.writing_tools - INFO - Writing tools AI service initialized
2026-01-18 22:23:49,547 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ AI Service 已同时设置到 langgraph_tools 和 writing_tools
2026-01-18 22:23:49,551 - app.services.context.adaptive_budget - INFO - ✅ 所有预算配置验证通过
2026-01-18 22:24:02,489 - app.services.context.vector_memory_store - INFO - ✅ VectorMemoryStore初始化成功 | 目录=./data/chroma_db | 模型=paraphrase-multilingual-MiniLM-L12-v2 | 集合=user_memories
2026-01-18 22:24:02,489 - app.services.context.manager - INFO - ✅ VectorMemoryStore 已初始化
2026-01-18 22:24:02,490 - app.services.context.manager - INFO - ✅ ContextManager: 长期记忆已启用 (user_id=None)
2026-01-18 22:24:02,490 - app.services.context.manager - INFO - ✅ ContextManager: 自适应预算已启用
2026-01-18 22:24:02,490 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ ContextManager已初始化（长期记忆已启用，自适应预算已启用，总预算=16000 tokens）
成功加载模板: analyze_text (版本 3.1.0)
成功加载模板: writing_agent (版本 2.0.0)
成功加载模板: system_agent_prompt (版本 2.1.0)
成功加载模板: creative_writing_prompt (版本 1.0.0)
2026-01-18 22:24:02,531 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ PromptManager已初始化
2026-01-18 22:24:02,537 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ Redis连接验证成功
2026-01-18 22:24:02,540 - app.services.agent.langgraph_agent - INFO - [LangGraph] OK 使用 AsyncRedisSaver（redis://localhost:6379/0，TTL=7天）
2026-01-18 22:24:02,541 - app.services.agent.memory.metrics - INFO - [MemoryMetrics] 监控系统已初始化
2026-01-18 22:24:02,542 - app.services.agent.memory.long_term_store - INFO - [LongTermStore] Initialized: base_dir=./data/long_term_memory, max_size=50KB, compression=True
2026-01-18 22:24:02,543 - app.services.agent.memory.enhanced_memory_manager - INFO - EnhancedMemoryManager initialized: short=10, medium=100, threshold=0.1, long_term_backup=enabled
2026-01-18 22:24:02,543 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ EnhancedMemoryManager已创建
2026-01-18 22:24:02,544 - app.services.agent.memory.unified_coordinator - INFO - [UnifiedMemoryCoordinator] 初始化统一记忆协调器
2026-01-18 22:24:02,544 - app.services.agent.memory.unified_coordinator - INFO - [UnifiedMemoryCoordinator] 全局实例已设置
2026-01-18 22:24:02,544 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ UnifiedMemoryCoordinator已初始化 | checkpointer=AsyncRedisSaver | enhanced_memory=yes | context_manager=yes
2026-01-18 22:24:02,544 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ 解耦模块已初始化 (IntentClassifier, ToolExecutor, EventParser, ResponseBuilder, ToolDispatcher, ParallelExecutor, PlanGenerator, QuickPathHandler, StreamEventHandler, SecondaryToolHandler, TaskRunner, AgentExecutor)
2026-01-18 22:24:02,553 - app.services.agent.parallel_tool_node - INFO - [ParallelToolNode] 初始化完成，最大并发数=5，并行安全工具=6个
2026-01-18 22:24:02,569 - app.api.v1.agent - INFO - [Global Agent] created global agent instance; MemorySaver shared across requests
2026-01-18 22:24:02,575 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第37章 【白日飞升，千古传奇】 (75 paragraphs)
2026-01-18 22:24:04,134 - app.api.v1.agent - INFO - [agent_chat_stream] 📚 世界观数据已注入: 人物=9, 地点=7, 设定=8, 规范=无
2026-01-18 22:24:04,134 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:5d5d90f8-cc82-4a5b-b1f9-a7da80dd11e2:551684cc-e807-4b02-8f65-c70c2ed716d1 (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=5d5d90f8-cc82-4a5b-b1f9-a7da80dd11e2, conversation_id=551684cc-e807-4b02-8f65-c70c2ed716d1)
2026-01-18 22:24:04,135 - app.services.context.monitoring_integration - INFO - ✅ ContextManager监控收集器已初始化
2026-01-18 22:24:04,136 - app.services.context.store - INFO - [ContextStore] Redis连接成功
2026-01-18 22:24:04,153 - app.services.context.manager - INFO - [ContextManager] 创建新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:5d5d90f8-cc82-4a5b-b1f9-a7da80dd11e2:551684cc-e807-4b02-8f65-c70c2ed716d1
2026-01-18 22:24:04,392 - app.services.context.token_counter - INFO - ✅ tiktoken初始化成功，模型: gemini-2.5-pro -> cl100k_base
2026-01-18 22:24:04,392 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:5d5d90f8-cc82-4a5b-b1f9-a7da80dd11e2:551684cc-e807-4b02-8f65-c70c2ed716d1: 0/16000 tokens
2026-01-18 22:24:05,144 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='请深度分析本作中"祭道之上"概念对剧情因果的影响：

  1...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:5d5d90f8-cc82-4a5b-b1f9-a7da80dd11e2', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=3条
2026-01-18 22:24:05,144 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=5d5d90f8-cc82-4a5b-b1f9-a7da80dd11e2 | 含用户级=True | 找到=3条
2026-01-18 22:24:05,215 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 1条消息, 0 tokens, 耗时 1078.58ms
2026-01-18 22:24:05,215 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 1 条历史消息 (token: 0, has_summary: False)
2026-01-18 22:24:05,216 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-18 22:24:05,217 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-18 22:24:05,217 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=200, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-18 22:24:05,222 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第37章 【白日飞升，千古传奇】 (75 paragraphs)
2026-01-18 22:24:06,834 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-18 22:24:06,835 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-18 22:24:06,881 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-18 22:24:06,883 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=571, cost=$0.000063, time=1618ms
2026-01-18 22:24:06,883 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=39, 尝试次数=1
2026-01-18 22:24:06,885 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-18 22:24:06,886 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-18 22:24:06,886 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=20, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-18 22:24:07,958 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-18 22:24:07,959 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-18 22:24:07,990 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-18 22:24:07,991 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=497, cost=$0.000050, time=1073ms
2026-01-18 22:24:07,991 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=8, 尝试次数=1
2026-01-18 22:24:07,991 - app.services.agent.intent.classifier - INFO - [Intent] AI识别结果: analysis
2026-01-18 22:24:07,991 - app.services.agent.langgraph_agent - INFO - [Planning] AI意图分类: analysis (置信度: 0.90)
2026-01-18 22:24:07,991 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 请深度分析本作中"祭道之上"概念对剧情因果的影响：

  1. 时间线逻辑：遮天三部曲（完美世界-遮...
2026-01-18 22:24:07,995 - app.core.cache - INFO - ⚠️ 缓存未命中: prompt:planning:v2.39.1:get_planning_static_prompt:fca6eb91156619d0
2026-01-18 22:24:08,003 - app.core.cache - INFO - 💾 缓存已保存: prompt:planning:v2.39.1:get_planning_static_prompt:fca6eb91156619d0 (expire=3600s)
2026-01-18 22:24:08,008 - app.services.agent.planning.plan_generator - INFO - [Planning] 检测到枚举项: ['祭道之上', '尊重穿越法则才是生存第一法则', '无所谓', '我会摆烂', '至尊级大成圣体', '天帝级狠人女帝', '仙帝级荒天帝', '祭道之上叶天帝', '抱大腿', '福地宝地', '巨坑天坑', '四个可能出手的叶凡', '这种时间悖论对林仙的', '的认知转变过程中', '哪些关键信息导致了系统界的集体恐惧']
2026-01-18 22:24:08,012 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-18 22:24:08,013 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=story_planning, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: story_planning; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-01-18 22:24:08,013 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.3, task_type=TaskType.STORY_PLANNING
2026-01-18 22:24:19,954 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-18 22:24:25,210 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 11 个数据块，总长度: 1450
2026-01-18 22:24:25,212 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 25419 (prompt=24759, completion=660)
2026-01-18 22:24:25,213 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-18 22:24:25,214 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-18 22:24:25,230 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-18 22:24:25,232 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=25419, cost=$0.037549, time=17200ms
2026-01-18 22:24:25,232 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=25419
2026-01-18 22:24:25,233 - app.services.agent.planning.plan_generator - WARNING - [Planning] 枚举项覆盖不完整，缺失: ['尊重穿越法则才是生存第一法则', '无所谓', '我会摆烂', '至尊级大成圣体', '天帝级狠人女帝', '仙帝级荒天帝', '祭道之上叶天帝', '抱大腿', '福地宝地', '巨坑天坑', '四个可能出手的叶凡', '这种时间悖论对林仙的', '的认知转变过程中', '哪些关键信息导致了系统界的集体恐惧']
2026-01-18 22:24:25,239 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-18 22:24:25,240 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=story_planning, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: story_planning; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-01-18 22:24:25,240 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.4, task_type=TaskType.STORY_PLANNING
2026-01-18 22:24:42,844 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-18 22:24:53,328 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 21 个数据块，总长度: 3013
2026-01-18 22:24:53,329 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 26726 (prompt=25400, completion=1326)
2026-01-18 22:24:53,329 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-18 22:24:53,329 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-18 22:24:53,338 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-18 22:24:53,342 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=26726, cost=$0.045010, time=28090ms
2026-01-18 22:24:53,343 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=26726
2026-01-18 22:24:53,343 - app.services.agent.planning.plan_generator - WARNING - [Planning] 枚举项覆盖不完整，缺失: ['这种时间悖论对林仙的']
2026-01-18 22:24:53,344 - app.services.agent.planning.plan_generator - INFO - [Planning] 第2次重试成功
2026-01-18 22:24:53,344 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户期望得到一个深度分析报告，针对其提出的四个关于“祭道之上, 原料=需要读取并理解当前章节（chapter_, 处理=首先使用 explore_content
2026-01-18 22:24:53,366 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共5个任务
2026-01-18 22:24:53,367 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共5个任务，耗时: 45.38s
2026-01-18 22:24:53,367 - app.api.v1.agent - INFO - [Stream] Plan tasks: 5 items
2026-01-18 22:24:53,367 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2026-01-18 22:24:53,368 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2026-01-18 22:24:53,368 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2026-01-18 22:24:53,368 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] DAG 调度启用，任务数=5, 有依赖任务=4
2026-01-18 22:24:53,368 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1开始: 为深度分析“祭道之上”概念，需要先读取当前章节的全部内容。
2026-01-18 22:24:53,368 - app.api.v1.agent - INFO - [Stream] Task started: 为深度分析“祭道之上”概念，需要先读取当前章节的全部内容。 (icon=Wrench)
2026-01-18 22:24:53,368 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: explore_content
2026-01-18 22:24:53,368 - app.services.agent.tools.explore_tools - INFO - [explore_content] 开始: work_id=5d5d90f8-cc82-4a5b-b1f9-a7da80dd11e2, target=读取章节 2ebca199-c7d0-47d3-9965-ec91e8f9fadf 的全部内容，以分...
2026-01-18 22:24:53,368 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 开始探索: work_id=5d5d90f8-cc82-4a5b-b1f9-a7da80dd11e2, target=读取章节 2ebca199-c7d0-47d3-9965-ec91e8f9fadf 的全部内容，以分...
2026-01-18 22:24:53,368 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-18 22:24:53,368 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-18 22:24:53,368 - app.services.ai.http_ai_service - INFO - [成本追踪] 初始化未传db/user_id，将使用请求上下文按需记录成本
2026-01-18 22:24:53,845 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-18 22:24:53,847 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-18 22:24:53,848 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=deep_analysis, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro
2026-01-18 22:24:53,848 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.3, 尝试=1/3, task_type=TaskType.DEEP_ANALYSIS
2026-01-18 22:25:09,369 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-18 22:25:09,369 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-18 22:25:09,384 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-18 22:25:09,387 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1824, cost=$0.006314, time=15521ms
2026-01-18 22:25:09,387 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=737, 尝试次数=1
2026-01-18 22:25:09,387 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] AI 任务理解完成: 分析特定章节内容，阐明“祭道之上”这一顶级设定如何从根本上解释了小说中的时间悖论、角色多重存在以及世界观的演变等核心因果问题。...
2026-01-18 22:25:09,387 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-18 22:25:09,389 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-18 22:25:09,389 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=300, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-18 22:25:12,147 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-18 22:25:12,148 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-18 22:25:12,157 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-18 22:25:12,162 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1035, cost=$0.000236, time=2759ms
2026-01-18 22:25:12,162 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=650, 尝试次数=1
2026-01-18 22:25:12,189 - app.services.agent.langgraph_tools - INFO - [get_writing_context] ✅ 获取创作上下文成功: include=worldview
2026-01-18 22:25:12,688 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=5d5d90f8-cc82-4a5b-b1f9-a7da80dd11e2, current_order=1000000, query=章节 2ebca199-c7d0-47d3-9965-ec91e8f9fadf 祭道之上 能力...
2026-01-18 22:25:13,503 - app.services.chapter_vector_service - INFO - RAG retrieved 10 segments within order<=2000000
Building prefix dict from the default dictionary ...
2026-01-18 22:25:13,512 - jieba - DEBUG - Building prefix dict from the default dictionary ...
Loading model from cache D:\Temp\jieba.cache
2026-01-18 22:25:13,515 - jieba - DEBUG - Loading model from cache D:\Temp\jieba.cache
Loading model cost 0.475 seconds.
2026-01-18 22:25:13,989 - jieba - DEBUG - Loading model cost 0.475 seconds.
Prefix dict has been built successfully.
2026-01-18 22:25:13,990 - jieba - DEBUG - Prefix dict has been built successfully.
2026-01-18 22:25:14,080 - app.services.search.hybrid_retriever - INFO - [Reranker] 正在加载模型: BAAI/bge-reranker-base
2026-01-18 22:25:17,618 - app.services.search.hybrid_retriever - INFO - [Reranker] 模型加载成功
2026-01-18 22:25:19,392 - app.services.search.hybrid_retriever - INFO - [Rerank] 重排序完成: 10 个候选 -> top 5
2026-01-18 22:25:19,393 - app.services.agent.langgraph_tools - INFO - [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
2026-01-18 22:25:19,399 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=5d5d90f8-cc82-4a5b-b1f9-a7da80dd11e2, current_order=1000000, query=章节 2ebca199-c7d0-47d3-9965-ec91e8f9fadf 时间线 逻辑 影响...
2026-01-18 22:25:20,874 - app.services.chapter_vector_service - INFO - RAG retrieved 10 segments within order<=2000000
2026-01-18 22:25:21,830 - app.services.search.hybrid_retriever - INFO - [Rerank] 重排序完成: 10 个候选 -> top 5
2026-01-18 22:25:21,830 - app.services.agent.langgraph_tools - INFO - [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
2026-01-18 22:25:21,836 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=5d5d90f8-cc82-4a5b-b1f9-a7da80dd11e2, current_order=1000000, query=章节 2ebca199-c7d0-47d3-9965-ec91e8f9fadf 叶凡 多重身位 原因...
2026-01-18 22:25:22,830 - app.services.chapter_vector_service - INFO - RAG retrieved 10 segments within order<=2000000
2026-01-18 22:25:23,521 - app.services.search.hybrid_retriever - INFO - [Rerank] 重排序完成: 10 个候选 -> top 5
2026-01-18 22:25:23,524 - app.services.agent.langgraph_tools - INFO - [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
2026-01-18 22:25:23,526 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-18 22:25:23,527 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=quality_evaluation, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-18 22:25:23,527 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=200, temp=0.1, 尝试=1/3, task_type=TaskType.QUALITY_EVALUATION
2026-01-18 22:25:25,948 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-18 22:25:25,948 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-18 22:25:25,963 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-18 22:25:25,965 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=850, cost=$0.000171, time=2420ms
2026-01-18 22:25:25,967 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=460, 尝试次数=1
2026-01-18 22:25:25,967 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-18 22:25:25,968 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-18 22:25:25,968 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=300, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-18 22:25:30,073 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-18 22:25:30,075 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-18 22:25:30,106 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-18 22:25:30,107 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1177, cost=$0.000251, time=4107ms
2026-01-18 22:25:30,108 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=657, 尝试次数=1
2026-01-18 22:25:30,111 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=5d5d90f8-cc82-4a5b-b1f9-a7da80dd11e2, current_order=1000000, query=章节 2ebca199-c7d0-47d3-9965-ec91e8f9fadf 祭道之上 时间因果操...
2026-01-18 22:25:31,928 - app.services.chapter_vector_service - INFO - RAG retrieved 10 segments within order<=2000000
2026-01-18 22:25:40,594 - app.services.search.hybrid_retriever - INFO - [Rerank] 重排序完成: 10 个候选 -> top 5
2026-01-18 22:25:40,598 - app.services.agent.langgraph_tools - INFO - [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
2026-01-18 22:25:40,620 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=5d5d90f8-cc82-4a5b-b1f9-a7da80dd11e2, current_order=1000000, query=章节 2ebca199-c7d0-47d3-9965-ec91e8f9fadf 祭道之上 穿越法则...
2026-01-18 22:25:50,576 - app.services.chapter_vector_service - INFO - RAG retrieved 10 segments within order<=2000000
2026-01-18 22:25:56,092 - app.services.search.hybrid_retriever - INFO - [Rerank] 重排序完成: 10 个候选 -> top 5
2026-01-18 22:25:56,094 - app.services.agent.langgraph_tools - INFO - [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
2026-01-18 22:25:56,113 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=5d5d90f8-cc82-4a5b-b1f9-a7da80dd11e2, current_order=1000000, query=章节 2ebca199-c7d0-47d3-9965-ec91e8f9fadf 系统一族 认知演变 ...
2026-01-18 22:26:03,646 - app.services.chapter_vector_service - INFO - RAG retrieved 10 segments within order<=2000000
2026-01-18 22:26:09,969 - app.services.search.hybrid_retriever - INFO - [Rerank] 重排序完成: 10 个候选 -> top 5
2026-01-18 22:26:09,969 - app.services.agent.langgraph_tools - INFO - [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
2026-01-18 22:26:09,982 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-18 22:26:09,983 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=quality_evaluation, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-18 22:26:09,983 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=200, temp=0.1, 尝试=1/3, task_type=TaskType.QUALITY_EVALUATION
2026-01-18 22:26:13,090 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-18 22:26:13,090 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-18 22:26:13,091 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-18 22:26:13,099 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=865, cost=$0.000172, time=3108ms
2026-01-18 22:26:13,099 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=460, 尝试次数=1
2026-01-18 22:26:13,099 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-18 22:26:13,099 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-18 22:26:13,099 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=300, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-18 22:26:15,946 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-18 22:26:15,949 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-18 22:26:15,960 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-18 22:26:15,960 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1414, cost=$0.000302, time=2850ms
2026-01-18 22:26:15,960 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=773, 尝试次数=1
2026-01-18 22:26:15,968 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=5d5d90f8-cc82-4a5b-b1f9-a7da80dd11e2, current_order=1000000, query=章节 2ebca199-c7d0-47d3-9965-ec91e8f9fadf 祭道之上 剧情因果影...
2026-01-18 22:26:16,943 - app.services.chapter_vector_service - INFO - RAG retrieved 10 segments within order<=2000000
2026-01-18 22:26:17,425 - app.services.search.hybrid_retriever - INFO - [Rerank] 重排序完成: 10 个候选 -> top 5
2026-01-18 22:26:17,425 - app.services.agent.langgraph_tools - INFO - [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
2026-01-18 22:26:17,431 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=5d5d90f8-cc82-4a5b-b1f9-a7da80dd11e2, current_order=1000000, query=章节 2ebca199-c7d0-47d3-9965-ec91e8f9fadf 叶凡多重身位 祭道之...
2026-01-18 22:26:18,618 - app.services.chapter_vector_service - INFO - RAG retrieved 10 segments within order<=2000000
2026-01-18 22:26:19,414 - app.services.search.hybrid_retriever - INFO - [Rerank] 重排序完成: 10 个候选 -> top 5
2026-01-18 22:26:19,414 - app.services.agent.langgraph_tools - INFO - [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
2026-01-18 22:26:19,420 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=5d5d90f8-cc82-4a5b-b1f9-a7da80dd11e2, current_order=1000000, query=章节 2ebca199-c7d0-47d3-9965-ec91e8f9fadf 系统一族 祭道之上 ...
2026-01-18 22:26:26,186 - app.services.chapter_vector_service - INFO - RAG retrieved 10 segments within order<=2000000
2026-01-18 22:26:45,856 - app.services.search.hybrid_retriever - INFO - [Rerank] 重排序完成: 10 个候选 -> top 5
2026-01-18 22:26:45,861 - app.services.agent.langgraph_tools - INFO - [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
2026-01-18 22:26:45,895 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-18 22:26:45,934 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=quality_evaluation, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-18 22:26:45,961 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=200, temp=0.1, 尝试=1/3, task_type=TaskType.QUALITY_EVALUATION
2026-01-18 22:26:50,043 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-18 22:26:50,058 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-18 22:26:50,184 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-18 22:26:50,202 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=872, cost=$0.000173, time=4110ms
2026-01-18 22:26:50,216 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=458, 尝试次数=1
2026-01-18 22:26:50,226 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-18 22:26:50,232 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-18 22:26:50,237 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=300, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-18 22:26:52,751 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-18 22:26:52,757 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-18 22:26:52,847 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-18 22:26:52,861 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1412, cost=$0.000258, time=2543ms
2026-01-18 22:26:52,876 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=583, 尝试次数=1
2026-01-18 22:26:52,910 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=5d5d90f8-cc82-4a5b-b1f9-a7da80dd11e2, current_order=1000000, query=章节 2ebca199-c7d0-47d3-9965-ec91e8f9fadf 祭道之上 叶凡 多重...
2026-01-18 22:27:03,868 - app.services.chapter_vector_service - INFO - RAG retrieved 10 segments within order<=2000000
2026-01-18 22:27:07,236 - app.services.search.hybrid_retriever - INFO - [Rerank] 重排序完成: 10 个候选 -> top 5
2026-01-18 22:27:07,236 - app.services.agent.langgraph_tools - INFO - [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
2026-01-18 22:27:07,242 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=5d5d90f8-cc82-4a5b-b1f9-a7da80dd11e2, current_order=1000000, query=章节 2ebca199-c7d0-47d3-9965-ec91e8f9fadf 祭道之上 系统一族 ...
2026-01-18 22:27:08,333 - app.services.chapter_vector_service - INFO - RAG retrieved 10 segments within order<=2000000
2026-01-18 22:27:09,560 - app.services.search.hybrid_retriever - INFO - [Rerank] 重排序完成: 10 个候选 -> top 5
2026-01-18 22:27:09,561 - app.services.agent.langgraph_tools - INFO - [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
2026-01-18 22:27:09,565 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-18 22:27:09,565 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=quality_evaluation, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-18 22:27:09,566 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=200, temp=0.1, 尝试=1/3, task_type=TaskType.QUALITY_EVALUATION
2026-01-18 22:27:12,283 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-18 22:27:12,283 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-18 22:27:12,295 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-18 22:27:12,297 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=915, cost=$0.000189, time=2717ms
2026-01-18 22:27:12,298 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=495, 尝试次数=1
2026-01-18 22:27:12,299 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-18 22:27:12,299 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-18 22:27:12,300 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=300, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-18 22:27:14,608 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-18 22:27:14,609 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-18 22:27:14,613 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-18 22:27:14,613 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1523, cost=$0.000286, time=2309ms
2026-01-18 22:27:14,613 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=658, 尝试次数=1
2026-01-18 22:27:14,613 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=5d5d90f8-cc82-4a5b-b1f9-a7da80dd11e2, current_order=1000000, query=章节 2ebca199-c7d0-47d3-9965-ec91e8f9fadf 祭道之上 概念解析...
2026-01-18 22:27:15,451 - app.services.chapter_vector_service - INFO - RAG retrieved 10 segments within order<=2000000
2026-01-18 22:27:15,822 - app.services.search.hybrid_retriever - INFO - [Rerank] 重排序完成: 10 个候选 -> top 5
2026-01-18 22:27:15,822 - app.services.agent.langgraph_tools - INFO - [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
2026-01-18 22:27:15,823 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=5d5d90f8-cc82-4a5b-b1f9-a7da80dd11e2, current_order=1000000, query=章节 2ebca199-c7d0-47d3-9965-ec91e8f9fadf 祭道之上 对时间线逻...
2026-01-18 22:27:16,576 - app.services.chapter_vector_service - INFO - RAG retrieved 10 segments within order<=2000000
2026-01-18 22:27:17,652 - app.services.search.hybrid_retriever - INFO - [Rerank] 重排序完成: 10 个候选 -> top 5
2026-01-18 22:27:17,653 - app.services.agent.langgraph_tools - INFO - [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
2026-01-18 22:27:17,658 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=5d5d90f8-cc82-4a5b-b1f9-a7da80dd11e2, current_order=1000000, query=章节 2ebca199-c7d0-47d3-9965-ec91e8f9fadf 祭道之上 对穿越法则...
2026-01-18 22:27:18,864 - app.services.chapter_vector_service - INFO - RAG retrieved 10 segments within order<=2000000
2026-01-18 22:27:19,520 - app.services.search.hybrid_retriever - INFO - [Rerank] 重排序完成: 10 个候选 -> top 5
2026-01-18 22:27:19,522 - app.services.agent.langgraph_tools - INFO - [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
2026-01-18 22:27:19,525 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-18 22:27:19,525 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=quality_evaluation, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-18 22:27:19,525 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=200, temp=0.1, 尝试=1/3, task_type=TaskType.QUALITY_EVALUATION
2026-01-18 22:27:22,119 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-18 22:27:22,119 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-18 22:27:22,129 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-18 22:27:22,129 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=882, cost=$0.000174, time=2594ms
2026-01-18 22:27:22,129 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=458, 尝试次数=1
2026-01-18 22:27:22,129 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-18 22:27:22,129 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-18 22:27:22,129 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=300, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-18 22:27:24,088 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-18 22:27:24,091 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-18 22:27:24,100 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-18 22:27:24,102 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1409, cost=$0.000241, time=1961ms
2026-01-18 22:27:24,104 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=499, 尝试次数=1
2026-01-18 22:27:24,105 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=5d5d90f8-cc82-4a5b-b1f9-a7da80dd11e2, current_order=1000000, query=章节 2ebca199-c7d0-47d3-9965-ec91e8f9fadf 叶凡 多重身位 祭道...
2026-01-18 22:27:24,734 - app.services.chapter_vector_service - INFO - RAG retrieved 10 segments within order<=2000000
2026-01-18 22:27:25,132 - app.services.search.hybrid_retriever - INFO - [Rerank] 重排序完成: 10 个候选 -> top 5
2026-01-18 22:27:25,132 - app.services.agent.langgraph_tools - INFO - [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
2026-01-18 22:27:25,132 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=5d5d90f8-cc82-4a5b-b1f9-a7da80dd11e2, current_order=1000000, query=章节 2ebca199-c7d0-47d3-9965-ec91e8f9fadf 系统一族 祭道之上 ...
2026-01-18 22:27:26,072 - app.services.chapter_vector_service - INFO - RAG retrieved 10 segments within order<=2000000
2026-01-18 22:27:27,312 - app.services.search.hybrid_retriever - INFO - [Rerank] 重排序完成: 10 个候选 -> top 5
2026-01-18 22:27:27,312 - app.services.agent.langgraph_tools - INFO - [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
2026-01-18 22:27:27,316 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-18 22:27:27,317 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=quality_evaluation, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-18 22:27:27,317 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=200, temp=0.1, 尝试=1/3, task_type=TaskType.QUALITY_EVALUATION
2026-01-18 22:27:29,523 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-18 22:27:29,523 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-18 22:27:29,535 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-18 22:27:29,536 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=887, cost=$0.000175, time=2207ms
2026-01-18 22:27:29,536 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=462, 尝试次数=1
2026-01-18 22:27:29,537 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-18 22:27:29,537 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-18 22:27:29,538 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=300, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-18 22:27:31,810 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-18 22:27:31,814 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-18 22:27:31,824 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-18 22:27:31,826 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1520, cost=$0.000283, time=2275ms
2026-01-18 22:27:31,826 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=633, 尝试次数=1
2026-01-18 22:27:31,828 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=5d5d90f8-cc82-4a5b-b1f9-a7da80dd11e2, current_order=1000000, query=章节 2ebca199-c7d0-47d3-9965-ec91e8f9fadf 叶凡 多重身位 祭道...
2026-01-18 22:27:32,463 - app.services.chapter_vector_service - INFO - RAG retrieved 10 segments within order<=2000000
2026-01-18 22:27:33,220 - app.services.search.hybrid_retriever - INFO - [Rerank] 重排序完成: 10 个候选 -> top 5
2026-01-18 22:27:33,222 - app.services.agent.langgraph_tools - INFO - [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
2026-01-18 22:27:33,224 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=5d5d90f8-cc82-4a5b-b1f9-a7da80dd11e2, current_order=1000000, query=章节 2ebca199-c7d0-47d3-9965-ec91e8f9fadf 祭道之上 时间线逻辑...
2026-01-18 22:27:39,183 - app.services.chapter_vector_service - INFO - RAG retrieved 10 segments within order<=2000000
2026-01-18 22:27:49,253 - app.services.search.hybrid_retriever - INFO - [Rerank] 重排序完成: 10 个候选 -> top 5
2026-01-18 22:27:49,255 - app.services.agent.langgraph_tools - INFO - [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
2026-01-18 22:27:49,272 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-18 22:27:49,280 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=quality_evaluation, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-18 22:27:49,291 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=200, temp=0.1, 尝试=1/3, task_type=TaskType.QUALITY_EVALUATION
2026-01-18 22:27:52,539 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-18 22:27:52,547 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-18 22:27:52,597 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-18 22:27:52,609 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=885, cost=$0.000174, time=3258ms
2026-01-18 22:27:52,612 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=460, 尝试次数=1
2026-01-18 22:27:52,615 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-18 22:27:52,617 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-18 22:27:52,617 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=300, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-18 22:27:55,282 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-18 22:27:55,288 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-18 22:27:55,346 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-18 22:27:55,354 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1540, cost=$0.000292, time=2673ms
2026-01-18 22:27:55,357 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=674, 尝试次数=1
2026-01-18 22:27:57,715 - app.services.agent.langgraph_tools - INFO - [get_writing_context] ✅ 获取创作上下文成功: include=chapter
2026-01-18 22:27:57,810 - app.services.agent.langgraph_tools - INFO - [get_writing_context] ✅ 获取创作上下文成功: include=chapter
2026-01-18 22:27:57,822 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-18 22:27:57,827 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=quality_evaluation, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-18 22:27:57,829 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=200, temp=0.1, 尝试=1/3, task_type=TaskType.QUALITY_EVALUATION
2026-01-18 22:28:01,129 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-18 22:28:01,136 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-18 22:28:01,199 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-18 22:28:01,205 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=998, cost=$0.000212, time=3317ms
2026-01-18 22:28:01,207 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=567, 尝试次数=1
2026-01-18 22:28:01,209 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-18 22:28:01,214 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-18 22:28:01,220 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=300, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-18 22:28:03,415 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-18 22:28:03,418 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-18 22:28:03,577 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-18 22:28:03,626 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1483, cost=$0.000261, time=2216ms
2026-01-18 22:28:03,647 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=560, 尝试次数=1
2026-01-18 22:28:03,692 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=5d5d90f8-cc82-4a5b-b1f9-a7da80dd11e2, current_order=1000000, query=章节 2ebca199-c7d0-47d3-9965-ec91e8f9fadf 祭道之上 剧情因果...
2026-01-18 22:28:10,487 - app.services.chapter_vector_service - INFO - RAG retrieved 10 segments within order<=2000000
2026-01-18 22:28:11,404 - app.services.search.hybrid_retriever - INFO - [Rerank] 重排序完成: 10 个候选 -> top 5
2026-01-18 22:28:11,406 - app.services.agent.langgraph_tools - INFO - [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
2026-01-18 22:28:11,409 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-18 22:28:11,409 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=quality_evaluation, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-18 22:28:11,411 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=200, temp=0.1, 尝试=1/3, task_type=TaskType.QUALITY_EVALUATION
2026-01-18 22:28:13,938 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-18 22:28:13,939 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-18 22:28:13,959 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-18 22:28:13,962 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=951, cost=$0.000193, time=2528ms
2026-01-18 22:28:13,964 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=509, 尝试次数=1
2026-01-18 22:28:13,965 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-18 22:28:13,966 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-18 22:28:13,966 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=300, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-18 22:28:17,430 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-18 22:28:17,449 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-18 22:28:17,584 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-18 22:28:17,600 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1571, cost=$0.000297, time=3495ms
2026-01-18 22:28:17,610 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=689, 尝试次数=1
2026-01-18 22:28:17,661 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=5d5d90f8-cc82-4a5b-b1f9-a7da80dd11e2, current_order=1000000, query=章节 2ebca199-c7d0-47d3-9965-ec91e8f9fadf 祭道之上 时间线重塑...
2026-01-18 22:28:30,493 - app.services.chapter_vector_service - INFO - RAG retrieved 10 segments within order<=2000000
2026-01-18 22:28:41,389 - app.services.search.hybrid_retriever - INFO - [Rerank] 重排序完成: 10 个候选 -> top 5
2026-01-18 22:28:41,405 - app.services.agent.langgraph_tools - INFO - [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
2026-01-18 22:28:41,476 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=5d5d90f8-cc82-4a5b-b1f9-a7da80dd11e2, current_order=1000000, query=章节 2ebca199-c7d0-47d3-9965-ec91e8f9fadf 祭道之上 穿越规则...
2026-01-18 22:28:56,570 - app.services.chapter_vector_service - INFO - RAG retrieved 10 segments within order<=2000000
2026-01-18 22:29:02,850 - app.services.search.hybrid_retriever - INFO - [Rerank] 重排序完成: 10 个候选 -> top 5
2026-01-18 22:29:02,855 - app.services.agent.langgraph_tools - INFO - [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
2026-01-18 22:29:02,910 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=5d5d90f8-cc82-4a5b-b1f9-a7da80dd11e2, current_order=1000000, query=章节 2ebca199-c7d0-47d3-9965-ec91e8f9fadf 系统一族 认知 祭道...
2026-01-18 22:29:14,479 - app.services.chapter_vector_service - INFO - RAG retrieved 10 segments within order<=2000000
2026-01-18 22:29:28,327 - app.services.search.hybrid_retriever - INFO - [Rerank] 重排序完成: 10 个候选 -> top 5
2026-01-18 22:29:28,333 - app.services.agent.langgraph_tools - INFO - [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
2026-01-18 22:29:28,351 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-18 22:29:28,362 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=quality_evaluation, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-18 22:29:28,370 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=200, temp=0.1, 尝试=1/3, task_type=TaskType.QUALITY_EVALUATION
2026-01-18 22:29:31,820 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-18 22:29:31,828 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-18 22:29:31,900 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-18 22:29:31,923 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1000, cost=$0.000213, time=3462ms
2026-01-18 22:29:31,927 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=568, 尝试次数=1
2026-01-18 22:29:31,940 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 探索完成: 10轮, 原因=达到最大轮次
2026-01-18 22:29:31,979 - app.services.agent.execution.tool_executor - INFO - [StandardTool] explore_content 执行成功
2026-01-18 22:29:31,994 - app.api.v1.agent - INFO - [Stream] 任务完成: 为深度分析“祭道之上”概念，需要先读取当前章节的全部内容。 (278.6s)
2026-01-18 22:29:32,000 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1完成
2026-01-18 22:29:32,004 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务2开始: 分析遮天三部曲（完美世界-遮天-圣墟）的时间序列如何影响林仙和系统10086的生存判断。
2026-01-18 22:29:32,007 - app.api.v1.agent - INFO - [Stream] Task started: 分析遮天三部曲（完美世界-遮天-圣墟）的时间序列如何影响林仙和系统10086的生存判断。 (icon=FileSearch)
2026-01-18 22:29:32,017 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 解析路径 context_for_task -> tokens: ['context_for_task']
2026-01-18 22:29:32,019 - app.services.agent.utils.tool_helpers - INFO - [参数标准化] analyze_content.content → text
2026-01-18 22:29:32,022 - app.services.agent.execution.task_runner - INFO - [TaskRunner] analyze_text_tool 使用 focus: '分析遮天三部曲的时间序列对林仙和系统10086生存判断的影响。...'
2026-01-18 22:29:32,030 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 ToolExecutor(analyze_content)
2026-01-18 22:29:32,049 - app.services.agent.tools.tool_types - INFO - [analyze_content] 开始执行工具
2026-01-18 22:29:32,099 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-18 22:29:32,104 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-18 22:29:32,109 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=3000, temp=0.3, task_type=TaskType.SUMMARIZATION
2026-01-18 22:29:50,450 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-18 22:30:02,881 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 43 个数据块，总长度: 2915
2026-01-18 22:30:02,881 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 16476 (prompt=14415, completion=2061)
2026-01-18 22:30:02,881 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-18 22:30:02,881 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-18 22:30:02,891 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-18 22:30:02,891 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=16476, cost=$0.009477, time=30768ms
2026-01-18 22:30:02,895 - app.services.agent.tools.tool_types - INFO - [analyze_content] 执行成功 (耗时: 30.847s)
2026-01-18 22:30:02,897 - app.services.agent.tools.tool_monitor - INFO - ToolMonitor initialized with Memory storage, retention: 7 days
2026-01-18 22:30:02,897 - app.services.agent.execution.tool_executor - INFO - [StandardTool] analyze_content 执行成功
2026-01-18 22:30:02,897 - app.services.agent.execution.task_runner - INFO - [TaskRunner] analyze_content 执行成功（ToolExecutor）
2026-01-18 22:30:02,897 - app.api.v1.agent - INFO - [Stream] 任务完成: 分析遮天三部曲（完美世界-遮天-圣墟）的时间序列如何影响林仙和系统10086的生存判断。 (30.9s)
2026-01-18 22:30:02,897 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务2完成
2026-01-18 22:30:02,897 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务3开始: 分析系统“尊重穿越法则才是生存第一法则”与林仙“无所谓，我会摆烂”的策略冲突，以及祭道之上存在时“因果点切割”的深意。
2026-01-18 22:30:02,897 - app.api.v1.agent - INFO - [Stream] Task started: 分析系统“尊重穿越法则才是生存第一法则”与林仙“无所谓，我会摆烂”的策略冲突，以及祭道之上存在时“因果点切割”的深意。 (icon=FileSearch)
2026-01-18 22:30:02,897 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 解析路径 context_for_task -> tokens: ['context_for_task']
2026-01-18 22:30:02,899 - app.services.agent.utils.tool_helpers - INFO - [参数标准化] analyze_content.content → text
2026-01-18 22:30:02,899 - app.services.agent.execution.task_runner - INFO - [TaskRunner] analyze_text_tool 使用 focus: '分析系统“尊重穿越法则”与林仙“摆烂”策略的冲突，并解释“祭道之上”存在时的“因果点切割”有何深意。...'
2026-01-18 22:30:02,899 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 ToolExecutor(analyze_content)
2026-01-18 22:30:02,899 - app.services.agent.tools.tool_types - INFO - [analyze_content] 开始执行工具
2026-01-18 22:30:02,903 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-18 22:30:02,903 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-18 22:30:02,907 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=3000, temp=0.3, task_type=TaskType.SUMMARIZATION
2026-01-18 22:30:10,675 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-18 22:30:28,232 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 58 个数据块，总长度: 5376
2026-01-18 22:30:28,240 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 18663 (prompt=14896, completion=3767)
2026-01-18 22:30:28,243 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-18 22:30:28,245 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-18 22:30:28,292 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-18 22:30:28,300 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=18663, cost=$0.013886, time=25340ms
2026-01-18 22:30:28,317 - app.services.agent.tools.tool_types - INFO - [analyze_content] 执行成功 (耗时: 25.418s)
2026-01-18 22:30:28,319 - app.services.agent.execution.tool_executor - INFO - [StandardTool] analyze_content 执行成功
2026-01-18 22:30:28,320 - app.services.agent.execution.task_runner - INFO - [TaskRunner] analyze_content 执行成功（ToolExecutor）
2026-01-18 22:30:28,322 - app.api.v1.agent - INFO - [Stream] 任务完成: 分析系统“尊重穿越法则才是生存第一法则”与林仙“无所谓，我会摆烂”的策略冲突，以及祭道之上存在时“因果点切割”的深意。 (25.4s)
2026-01-18 22:30:28,324 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务3完成
2026-01-18 22:30:28,332 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务4开始: 分析“至尊级大成圣体、天帝级狠人女帝、仙帝级荒天帝、祭道之上叶天帝”这四个可能出手的叶凡，及其时间悖论对林仙“抱大腿”策略的影响。
2026-01-18 22:30:28,335 - app.api.v1.agent - INFO - [Stream] Task started: 分析“至尊级大成圣体、天帝级狠人女帝、仙帝级荒天帝、祭道之上叶天帝”这四个可能出手的叶凡，及其时间悖论对林仙“抱大腿”策略的影响。 (icon=FileSearch)
2026-01-18 22:30:28,339 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 解析路径 context_for_task -> tokens: ['context_for_task']
2026-01-18 22:30:28,340 - app.services.agent.utils.tool_helpers - INFO - [参数标准化] analyze_content.content → text
2026-01-18 22:30:28,346 - app.services.agent.execution.task_runner - INFO - [TaskRunner] analyze_text_tool 使用 focus: '分析文中提到的四个可能出手的叶凡（至尊级大成圣体、天帝级狠人女帝、仙帝级荒天帝、祭道之上叶天帝）所引发的时间悖论，及其对林仙“抱大腿”策略的影响。...'
2026-01-18 22:30:28,348 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 ToolExecutor(analyze_content)
2026-01-18 22:30:28,350 - app.services.agent.tools.tool_types - INFO - [analyze_content] 开始执行工具
2026-01-18 22:30:28,384 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-18 22:30:28,387 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-18 22:30:28,392 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=3000, temp=0.3, task_type=TaskType.SUMMARIZATION
2026-01-18 22:30:41,678 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-18 22:30:57,588 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 79 个数据块，总长度: 5431
2026-01-18 22:30:57,588 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 23792 (prompt=19992, completion=3800)
2026-01-18 22:30:57,588 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-18 22:30:57,588 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-18 22:30:57,602 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-18 22:30:57,604 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=23792, cost=$0.015498, time=29185ms
2026-01-18 22:30:57,607 - app.services.agent.tools.tool_types - INFO - [analyze_content] 执行成功 (耗时: 29.257s)
2026-01-18 22:30:57,607 - app.services.agent.execution.tool_executor - INFO - [StandardTool] analyze_content 执行成功
2026-01-18 22:30:57,607 - app.services.agent.execution.task_runner - INFO - [TaskRunner] analyze_content 执行成功（ToolExecutor）
2026-01-18 22:30:57,608 - app.api.v1.agent - INFO - [Stream] 任务完成: 分析“至尊级大成圣体、天帝级狠人女帝、仙帝级荒天帝、祭道之上叶天帝”这四个可能出手的叶凡，及其时间悖论对林仙“抱大腿”策略的影响。 (29.3s)
2026-01-18 22:30:57,609 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务4完成
2026-01-18 22:30:57,610 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务5开始: 分析系统一族从视穿越世界为“福地宝地”到“巨坑天坑”的认知转变过程中，哪些关键信息导致了系统界的集体恐惧。
2026-01-18 22:30:57,610 - app.api.v1.agent - INFO - [Stream] Task started: 分析系统一族从视穿越世界为“福地宝地”到“巨坑天坑”的认知转变过程中，哪些关键信息导致了系统界的集体恐惧。 (icon=FileSearch)
2026-01-18 22:30:57,610 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 解析路径 context_for_task -> tokens: ['context_for_task']
2026-01-18 22:30:57,611 - app.services.agent.utils.tool_helpers - INFO - [参数标准化] analyze_content.content → text
2026-01-18 22:30:57,612 - app.services.agent.execution.task_runner - INFO - [TaskRunner] analyze_text_tool 使用 focus: '分析系统一族认知从“福地宝地”到“巨坑天坑”的转变，并找出导致系统界集体恐惧的关键信息。...'
2026-01-18 22:30:57,612 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 ToolExecutor(analyze_content)
2026-01-18 22:30:57,613 - app.services.agent.tools.tool_types - INFO - [analyze_content] 开始执行工具
2026-01-18 22:30:57,617 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-18 22:30:57,617 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-18 22:30:57,618 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=3000, temp=0.3, task_type=TaskType.SUMMARIZATION
2026-01-18 22:31:07,149 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-18 22:31:19,566 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 60 个数据块，总长度: 5453
2026-01-18 22:31:19,567 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 26746 (prompt=22925, completion=3821)
2026-01-18 22:31:19,567 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-18 22:31:19,569 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-18 22:31:19,579 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-18 22:31:19,581 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=26746, cost=$0.016430, time=21951ms
2026-01-18 22:31:19,586 - app.services.agent.tools.tool_types - INFO - [analyze_content] 执行成功 (耗时: 21.973s)
2026-01-18 22:31:19,587 - app.services.agent.execution.tool_executor - INFO - [StandardTool] analyze_content 执行成功
2026-01-18 22:31:19,587 - app.services.agent.execution.task_runner - INFO - [TaskRunner] analyze_content 执行成功（ToolExecutor）
2026-01-18 22:31:19,588 - app.api.v1.agent - INFO - [Stream] 任务完成: 分析系统一族从视穿越世界为“福地宝地”到“巨坑天坑”的认知转变过程中，哪些关键信息导致了系统界的集体恐惧。 (22.0s)
2026-01-18 22:31:19,588 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务5完成
2026-01-18 22:31:19,589 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共5个任务，耗时: 386.22s
2026-01-18 22:31:19,589 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2026-01-18 22:31:19,589 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=5, 展示型=0
2026-01-18 22:31:19,589 - app.services.agent.langgraph_agent - INFO - [Response] 5个输出任务（含续写），使用AI整合
2026-01-18 22:31:19,589 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2026-01-18 22:31:19,589 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=5, 展示型=0
2026-01-18 22:31:19,590 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=25384字符, 处理后=13927字符
2026-01-18 22:31:19,590 - app.services.agent.planning.response_builder - INFO - [Summarization] 准备发送 summarization_start 事件
2026-01-18 22:31:19,590 - app.services.agent.stream.stream_event_handler - INFO - [StreamEventHandler] emit_summarization_start 被调用, _on_flow_event=True
2026-01-18 22:31:19,590 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_start 事件已发送
2026-01-18 22:31:19,590 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2026-01-18 22:31:19,590 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2026-01-18 22:31:19,595 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-18 22:31:19,596 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-18 22:31:19,596 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
2026-01-18 22:31:29,193 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-18 22:31:29,193 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_complete 事件已发送（第一个chunk时）
2026-01-18 22:31:29,193 - app.services.agent.planning.response_builder - INFO - [Summarization] output_ready 事件已发送（第一个chunk时）
2026-01-18 22:31:39,925 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 48 个数据块，总长度: 3391
2026-01-18 22:31:39,925 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 22946 (prompt=20612, completion=2334)
2026-01-18 22:31:39,925 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-18 22:31:39,927 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-18 22:31:39,938 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-18 22:31:39,938 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=22946, cost=$0.012019, time=20331ms
2026-01-18 22:31:39,938 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=3391
2026-01-18 22:31:40,284 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:5d5d90f8-cc82-4a5b-b1f9-a7da80dd11e2 | 重要度=0.60
2026-01-18 22:31:40,504 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:5d5d90f8-cc82-4a5b-b1f9-a7da80dd11e2 | 重要度=0.60
2026-01-18 22:31:40,531 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:5d5d90f8-cc82-4a5b-b1f9-a7da80dd11e2:551684cc-e807-4b02-8f65-c70c2ed716d1, token=3982
2026-01-18 22:31:40,532 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:5d5d90f8-cc82-4a5b-b1f9-a7da80dd11e2:551684cc-e807-4b02-8f65-c70c2ed716d1, 消息数=2, 摘要长度=0, Token=3982
2026-01-18 22:31:40,533 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:5d5d90f8-cc82-4a5b-b1f9-a7da80dd11e2:551684cc-e807-4b02-8f65-c70c2ed716d1)
2026-01-18 22:31:40,533 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2026-01-18 22:31:40,542 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed
2026-01-18 22:32:18,809 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/551684cc-e807-4b02-8f65-c70c2ed716d1
INFO:     127.0.0.1:52130 - "GET /api/v1/agent/operations/551684cc-e807-4b02-8f65-c70c2ed716d1 HTTP/1.1" 200 OK