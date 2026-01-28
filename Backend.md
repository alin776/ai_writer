INFO:     127.0.0.1:56911 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2026-01-28 16:44:56,360 - app.core.redis - INFO - ✅ Redis connected: redis://localhost:6379/0
2026-01-28 16:44:56,361 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: “请对全书做跨章节 Explore，围绕‘世界观体量差异（遮天 vs 一人之下）→主线任务体系→宿主...
2026-01-28 16:44:56,361 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-28 16:44:56,362 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-28 16:44:56,362 - app.services.ai.http_ai_service - INFO - [成本追踪] 初始化未传db/user_id，将使用请求上下文按需记录成本
2026-01-28 16:44:57,730 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz:8443/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-28 16:44:57,730 - app.services.agent.tools.writing_tools - INFO - Writing tools AI service initialized
2026-01-28 16:44:57,730 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ AI Service 已同时设置到 langgraph_tools 和 writing_tools
2026-01-28 16:44:57,730 - app.services.context.adaptive_budget - INFO - ✅ 所有预算配置验证通过
2026-01-28 16:45:03,446 - app.services.context.vector_memory_store - INFO - ✅ VectorMemoryStore初始化成功 | 目录=./data/chroma_db | 模型=paraphrase-multilingual-MiniLM-L12-v2 | 集合=user_memories
2026-01-28 16:45:03,447 - app.services.context.manager - INFO - ✅ VectorMemoryStore 已初始化
2026-01-28 16:45:03,448 - app.services.context.manager - INFO - ✅ ContextManager: 长期记忆已启用 (user_id=None)
2026-01-28 16:45:03,448 - app.services.context.manager - INFO - ✅ ContextManager: 自适应预算已启用
2026-01-28 16:45:03,448 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ ContextManager已初始化（长期记忆已启用，自适应预算已启用，总预算=16000 tokens）
成功加载模板: analyze_text (版本 3.1.0)
成功加载模板: writing_agent (版本 2.0.0)
成功加载模板: system_agent_prompt (版本 2.1.0)
成功加载模板: creative_writing_prompt (版本 1.0.0)
2026-01-28 16:45:03,471 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ PromptManager已初始化
2026-01-28 16:45:03,476 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ Redis连接验证成功
2026-01-28 16:45:03,477 - app.services.agent.langgraph_agent - INFO - [LangGraph] OK 使用 AsyncRedisSaver（redis://localhost:6379/0，TTL=7天）
2026-01-28 16:45:03,477 - app.services.agent.memory.metrics - INFO - [MemoryMetrics] 监控系统已初始化
2026-01-28 16:45:03,478 - app.services.agent.memory.long_term_store - INFO - [LongTermStore] Initialized: base_dir=./data/long_term_memory, max_size=50KB, compression=True
2026-01-28 16:45:03,478 - app.services.agent.memory.enhanced_memory_manager - INFO - EnhancedMemoryManager initialized: short=10, medium=100, threshold=0.1, long_term_backup=enabled
2026-01-28 16:45:03,479 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ EnhancedMemoryManager已创建
2026-01-28 16:45:03,479 - app.services.agent.memory.unified_coordinator - INFO - [UnifiedMemoryCoordinator] 初始化统一记忆协调器
2026-01-28 16:45:03,480 - app.services.agent.memory.unified_coordinator - INFO - [UnifiedMemoryCoordinator] 全局实例已设置
2026-01-28 16:45:03,481 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ UnifiedMemoryCoordinator已初始化 | checkpointer=AsyncRedisSaver | enhanced_memory=yes | context_manager=yes
2026-01-28 16:45:03,481 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ 解耦模块已初始化 (IntentClassifier, ToolExecutor, EventParser, ResponseBuilder, ToolDispatcher, ParallelExecutor, PlanGenerator, QuickPathHandler, StreamEventHandler, SecondaryToolHandler, TaskRunner, AgentExecutor)
2026-01-28 16:45:03,486 - app.services.agent.parallel_tool_node - INFO - [ParallelToolNode] 初始化完成，最大并发数=5，并行安全工具=6个
2026-01-28 16:45:03,494 - app.api.v1.agent - INFO - [Global Agent] created global agent instance; MemorySaver shared across requests
2026-01-28 16:45:03,510 - app.api.v1.agent - INFO - [agent_chat_stream] 📚 世界观数据已注入: 人物=8, 地点=7, 设定=7, 规范=无
2026-01-28 16:45:03,510 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21:e6c9868c-d915-4567-8b2a-d02ead305b57 (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, conversation_id=e6c9868c-d915-4567-8b2a-d02ead305b57)
2026-01-28 16:45:03,510 - app.services.context.monitoring_integration - INFO - ✅ ContextManager监控收集器已初始化
2026-01-28 16:45:03,510 - app.services.context.store - INFO - [ContextStore] Redis连接成功
2026-01-28 16:45:03,546 - app.services.context.manager - INFO - [ContextManager] 创建新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21:e6c9868c-d915-4567-8b2a-d02ead305b57
2026-01-28 16:45:03,671 - app.services.context.token_counter - INFO - ✅ tiktoken初始化成功，模型: gemini-2.5-pro -> cl100k_base
2026-01-28 16:45:03,671 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21:e6c9868c-d915-4567-8b2a-d02ead305b57: 0/16000 tokens
2026-01-28 16:45:04,074 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='“请对全书做跨章节 Explore，围绕‘世界观体量差异（遮...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=3条
2026-01-28 16:45:04,074 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21 | 含用户级=True | 找到=3条
2026-01-28 16:45:04,107 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 1条消息, 0 tokens, 耗时 596.33ms
2026-01-28 16:45:04,107 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 1 条历史消息 (token: 0, has_summary: False)
2026-01-28 16:45:04,108 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-28 16:45:04,108 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-28 16:45:04,108 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=200, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-28 16:45:05,820 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 16:45:05,820 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-28 16:45:05,848 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 16:45:05,848 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=431, cost=$0.000048, time=1713ms
2026-01-28 16:45:05,850 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=39, 尝试次数=1
2026-01-28 16:45:05,851 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-28 16:45:05,851 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-28 16:45:05,851 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=20, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-28 16:45:07,483 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 16:45:07,483 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-28 16:45:07,502 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 16:45:07,504 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=359, cost=$0.000036, time=1634ms
2026-01-28 16:45:07,504 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=8, 尝试次数=1
2026-01-28 16:45:07,504 - app.services.agent.intent.classifier - INFO - [Intent] AI识别结果: analysis
2026-01-28 16:45:07,504 - app.services.agent.langgraph_agent - INFO - [Planning] AI意图分类: analysis (置信度: 0.90)
2026-01-28 16:45:07,504 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: “请对全书做跨章节 Explore，围绕‘世界观体量差异（遮天 vs 一人之下）→主线任务体系→宿主...
2026-01-28 16:45:07,507 - app.core.cache - INFO - ⚠️ 缓存未命中: prompt:planning:v2.41.0:get_planning_static_prompt:fca6eb91156619d0
2026-01-28 16:45:07,510 - app.core.cache - INFO - 💾 缓存已保存: prompt:planning:v2.41.0:get_planning_static_prompt:fca6eb91156619d0 (expire=3600s)
2026-01-28 16:45:07,515 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-28 16:45:07,515 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=story_planning, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: story_planning; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-01-28 16:45:07,516 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.3, task_type=TaskType.STORY_PLANNING
2026-01-28 16:45:17,704 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-28 16:45:30,114 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 23 个数据块，总长度: 4897
2026-01-28 16:45:30,114 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 22175 (prompt=20741, completion=1434)
2026-01-28 16:45:30,114 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 16:45:30,114 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-28 16:45:30,127 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 16:45:30,138 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=22175, cost=$0.040266, time=22600ms
2026-01-28 16:45:30,139 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=22175
2026-01-28 16:45:30,139 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户需要一个跨章节的分析报告，建立'世界观体量差异→主线任务, 原料=需要从作品中检索关于'世界观'（特别是与, 处理=使用 explore_content 工
2026-01-28 16:45:30,148 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共1个任务
2026-01-28 16:45:30,148 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共1个任务，耗时: 22.64s
2026-01-28 16:45:30,149 - app.api.v1.agent - INFO - [Stream] Plan tasks: 1 items
2026-01-28 16:45:30,149 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2026-01-28 16:45:30,149 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2026-01-28 16:45:30,149 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2026-01-28 16:45:30,149 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] DAG 调度启用，任务数=1, 有依赖任务=0
2026-01-28 16:45:30,149 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1开始: 跨章节探索，围绕‘世界观体量差异（遮天 vs 一人之下）→主线任务体系→宿主摆烂策略’，检索相关原文证据，要求覆盖第1章和第2章。
2026-01-28 16:45:30,149 - app.api.v1.agent - INFO - [Stream] Task started: 跨章节探索，围绕‘世界观体量差异（遮天 vs 一人之下）→主线任务体系→宿主摆烂策略’，检索相关原文证据，要求覆盖第1章和第2章。 (icon=Wrench)
2026-01-28 16:45:30,149 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: explore_content
2026-01-28 16:45:30,149 - app.services.agent.tools.explore_tools - INFO - [explore_content] 开始: work_id=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, target=检索并提取关于'世界观体量'（特别是与'遮天'、'一人之下'的对比）、'主线任务'的设计以及主角'摆...
2026-01-28 16:45:30,149 - app.services.agent.tools.explore_tools - INFO - [explore_content] 规划传入关键词: ['世界观', '遮天', '一人之下', '主线任务', '摆烂', '宿主', '系统']
2026-01-28 16:45:30,154 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 章节范围锁定: 第1-2章
2026-01-28 16:45:30,154 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 开始探索 V5: work_id=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, target=检索并提取关于'世界观体量'（特别是与'遮天'、'一人之下'的对比）、'主线任务'的设计以及主角'摆...
2026-01-28 16:45:30,154 - app.services.chapter_service - INFO - [ChapterService] Querying chapters for work_id=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, type=<class 'uuid.UUID'>
2026-01-28 16:45:30,169 - app.services.chapter_service - INFO - [ChapterService] Found 77 chapters
2026-01-28 16:45:30,170 - app.services.chapter_service - INFO -   - Chapter: 第1章 【摆烂的宿主】, order=1
2026-01-28 16:45:30,170 - app.services.chapter_service - INFO -   - ... (75 more chapters)
2026-01-28 16:45:30,171 - app.services.chapter_service - INFO -   - Chapter: 第100章 【火域铸真器，两脉起冲突】, order=77
2026-01-28 16:45:30,186 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 章节范围映射: 第1-2章 -> 第1-2章
2026-01-28 16:45:30,186 - app.services.ai.http_ai_service - INFO - [成本追踪] 初始化未传db/user_id，将使用请求上下文按需记录成本
2026-01-28 16:45:30,660 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz:8443/v1, Model: gemini-2.5-flash, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: False, CostTracking: True
2026-01-28 16:45:30,660 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-28 16:45:30,660 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=80, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-28 16:45:36,318 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 16:45:36,318 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-28 16:45:36,332 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 16:45:36,335 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=708, cost=$0.000243, time=5658ms
2026-01-28 16:45:36,335 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=19, 尝试次数=1
2026-01-28 16:45:36,335 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 强制流程步骤: list_chapters
2026-01-28 16:45:36,339 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=list_chapters params={"work_id": "5fe6c67d-8a1b-48c1-ad56-a5281eb22e21"}
2026-01-28 16:45:36,340 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=list_chapters success=True count=2
2026-01-28 16:45:36,340 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-28 16:45:36,340 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=80, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-28 16:45:40,377 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 16:45:40,377 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-28 16:45:40,405 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 16:45:40,406 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=551, cost=$0.000192, time=4037ms
2026-01-28 16:45:40,406 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=17, 尝试次数=1
2026-01-28 16:45:40,406 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 强制流程步骤: list_paragraphs
2026-01-28 16:45:40,408 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=list_paragraphs params={"chapter_order": 1, "offset": 0, "limit": 50, "preview_len": 80, "work_id": "5fe6c67d-8a1b-48c1-ad56-a5281eb22e21"}
2026-01-28 16:45:40,430 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=list_paragraphs success=True chapter=1 offset=0 limit=50 approximate=None
2026-01-28 16:45:40,430 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-28 16:45:40,430 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-28 16:45:43,134 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 16:45:43,135 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-28 16:45:43,146 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 16:45:43,146 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1526, cost=$0.000854, time=2705ms
2026-01-28 16:45:43,146 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=327, 尝试次数=1
2026-01-28 16:45:43,146 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"work_id": "5fe6c67d-8a1b-48c1-ad56-a5281eb22e21", "chapter_order": 1, "keywords": "世界观体量|遮天|一人之下|主线任务|摆烂", "match_mode": "or", "limit": 50}
2026-01-28 16:45:43,162 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['世界观体量|遮天|一人之下|主线任务|摆烂']..., mode=any, range=(1, 2), hits=0
2026-01-28 16:45:43,162 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=0 keywords=世界观体量|遮天|一人之下|主线任务|摆烂
2026-01-28 16:45:43,162 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-28 16:45:43,162 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-28 16:45:58,918 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 16:45:58,918 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-28 16:45:58,931 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 16:45:58,931 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=3121, cost=$0.001282, time=15755ms
2026-01-28 16:45:58,938 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=287, 尝试次数=1
2026-01-28 16:45:58,939 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"work_id": 1, "keywords": "躺平|消极|佛系|咸鱼|任务|主线|世界观|遮天|一人之下", "match_mode": "any", "limit": 50}
2026-01-28 16:45:58,955 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['躺平|消极|佛系|咸鱼|任务|主线|世界观|遮天|一人之下']..., mode=any, range=(1, 2), hits=0
2026-01-28 16:45:58,955 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=0 keywords=躺平|消极|佛系|咸鱼|任务|主线|世界观|遮天|一人之下
2026-01-28 16:45:58,960 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-28 16:45:58,960 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-28 16:46:18,689 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 16:46:18,690 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-28 16:46:18,713 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 16:46:18,714 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=3391, cost=$0.001202, time=19729ms
2026-01-28 16:46:18,715 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=166, 尝试次数=1
2026-01-28 16:46:18,715 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=list_chapters params={"work_id": 1}
2026-01-28 16:46:18,715 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=list_chapters success=True count=2
2026-01-28 16:46:18,715 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-28 16:46:18,717 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-28 16:46:22,728 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 16:46:22,728 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-28 16:46:22,739 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 16:46:22,739 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1253, cost=$0.000761, time=4011ms
2026-01-28 16:46:22,739 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=316, 尝试次数=1
2026-01-28 16:46:22,739 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"work_id": "8796093022479837184", "keywords": "世界观体量|遮天|一人之下|主线任务|摆烂|躺平|消极|佛系|咸鱼|任务|主线|世界观", "match_mode": "or", "limit": 50, "chapter_orders": [1, 2]}
2026-01-28 16:46:22,760 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['世界观体量|遮天|一人之下|主线任务|摆烂|躺平|消极|佛系|咸鱼|任务|主线|世界观']..., mode=any, range=(1, 2), hits=0
2026-01-28 16:46:22,760 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=0 keywords=世界观体量|遮天|一人之下|主线任务|摆烂|躺平|消极|佛系|咸鱼|任务|主线|世界观
2026-01-28 16:46:22,760 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-28 16:46:22,760 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-28 16:46:29,194 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 16:46:29,194 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-28 16:46:29,199 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 16:46:29,199 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1617, cost=$0.000762, time=6435ms
2026-01-28 16:46:29,199 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=261, 尝试次数=1
2026-01-28 16:46:29,199 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=list_paragraphs params={"work_id": "default", "chapter_order": 1, "offset": 0, "limit": 20, "preview_len": 100}
2026-01-28 16:46:29,216 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=list_paragraphs success=True chapter=1 offset=0 limit=20 approximate=None
2026-01-28 16:46:29,216 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-28 16:46:29,216 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-28 16:46:32,621 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 16:46:32,621 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-28 16:46:32,623 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 16:46:32,631 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1668, cost=$0.000914, time=3405ms
2026-01-28 16:46:32,631 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=336, 尝试次数=1
2026-01-28 16:46:32,631 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"work_id": "5fe6c67d-8a1b-48c1-ad56-a5281eb22e21", "keywords": "世界观体量|遮天|一人之下|主线任务|摆烂|躺平|消极|佛系|咸鱼|任务|主线|世界观", "match_mode": "keywords", "limit": 50, "chapter_order": 1}
2026-01-28 16:46:32,642 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['世界观体量|遮天|一人之下|主线任务|摆烂|躺平|消极|佛系|咸鱼|任务|主线|世界观']..., mode=any, range=(1, 2), hits=0
2026-01-28 16:46:32,648 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=0 keywords=世界观体量|遮天|一人之下|主线任务|摆烂|躺平|消极|佛系|咸鱼|任务|主线|世界观
2026-01-28 16:46:32,648 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-28 16:46:32,648 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-28 16:46:49,917 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 16:46:49,917 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-28 16:46:49,926 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 16:46:49,928 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=3125, cost=$0.001146, time=17269ms
2026-01-28 16:46:49,928 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=150, 尝试次数=1
2026-01-28 16:46:49,928 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-28 16:46:49,928 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=200, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-28 16:46:53,498 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 16:46:53,499 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-28 16:46:53,499 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 16:46:53,499 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=616, cost=$0.000301, time=3570ms
2026-01-28 16:46:53,499 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=82, 尝试次数=1
2026-01-28 16:46:53,499 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 探索完成(工具循环): 8轮, 原因=在第1章和第2章中，使用所有相关关键词（包括'世界观体量'、'遮天'、'一人之下'、'主线任务'、'摆烂'及其同义词）进行精确搜索，均未找到任何匹配段落。根据可用工具和约束，无法进一步检索到目标信息。
2026-01-28 16:46:53,499 - app.services.agent.execution.tool_executor - INFO - [StandardTool] explore_content 执行成功
2026-01-28 16:46:53,499 - app.api.v1.agent - INFO - [Stream] 任务完成: 跨章节探索，围绕‘世界观体量差异（遮天 vs 一人之下）→主线任务体系→宿主摆烂策略’，检索相关原文证据，要求覆盖第1章和第2章。 (83.4s)
2026-01-28 16:46:53,499 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1完成
2026-01-28 16:46:53,499 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共1个任务，耗时: 83.35s
2026-01-28 16:46:53,499 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2026-01-28 16:46:53,499 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=1, 展示型=0
2026-01-28 16:46:53,499 - app.services.agent.langgraph_agent - INFO - [Response] 单个输出任务(explore_content)，使用AI整合
2026-01-28 16:46:53,499 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2026-01-28 16:46:53,499 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=1, 展示型=0
2026-01-28 16:46:53,499 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=338字符, 处理后=408字符
2026-01-28 16:46:53,499 - app.services.agent.planning.response_builder - INFO - [Summarization] 准备发送 summarization_start 事件
2026-01-28 16:46:53,499 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-28 16:46:53,499 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-28 16:46:53,499 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=60, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-28 16:46:54,887 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 16:46:54,887 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-28 16:46:54,898 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 16:46:54,900 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=258, cost=$0.000029, time=1388ms
2026-01-28 16:46:54,900 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=19, 尝试次数=1
2026-01-28 16:46:54,901 - app.services.agent.planning.response_builder - INFO - [Summarization] reason生成: len=19 content=探索遮天一人之下世界观差异与任务体系。
2026-01-28 16:46:54,901 - app.services.agent.stream.stream_event_handler - INFO - [StreamEventHandler] emit_summarization_start 被调用, _on_flow_event=True, reason_len=19, reason=探索遮天一人之下世界观差异与任务体系。
2026-01-28 16:46:54,901 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_start 事件已发送
2026-01-28 16:46:54,901 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2026-01-28 16:46:54,901 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2026-01-28 16:46:54,901 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-28 16:46:54,901 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-28 16:46:54,901 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
2026-01-28 16:47:01,383 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-28 16:47:01,384 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_complete 事件已发送（第一个chunk时）
2026-01-28 16:47:01,385 - app.services.agent.planning.response_builder - INFO - [Summarization] output_ready 事件已发送（第一个chunk时）
2026-01-28 16:47:03,489 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 6 个数据块，总长度: 520
2026-01-28 16:47:03,489 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 2776 (prompt=2442, completion=334)
2026-01-28 16:47:03,489 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-28 16:47:03,489 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-28 16:47:03,495 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-28 16:47:03,495 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2776, cost=$0.001568, time=8589ms
2026-01-28 16:47:03,495 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=520
2026-01-28 16:47:03,547 - app.services.context.vector_memory_store - INFO - 🔁 跳过重复记忆，复用ID=79913e7e-d5cd-4e09-bce6-ca6639bd8456_1769540629168_1847a517
2026-01-28 16:47:03,547 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21 | 重要度=1.00
2026-01-28 16:47:03,915 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21 | 重要度=0.77
2026-01-28 16:47:03,921 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21:e6c9868c-d915-4567-8b2a-d02ead305b57, token=620
2026-01-28 16:47:03,922 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21:e6c9868c-d915-4567-8b2a-d02ead305b57, 消息数=2, 摘要长度=0, Token=620
2026-01-28 16:47:03,922 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21:e6c9868c-d915-4567-8b2a-d02ead305b57)
2026-01-28 16:47:03,923 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2026-01-28 16:47:03,926 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed