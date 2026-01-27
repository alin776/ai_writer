2026-01-27 19:44:48,172 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ PromptManager已初始化
2026-01-27 19:44:48,181 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ Redis连接验证成功
2026-01-27 19:44:48,182 - app.services.agent.langgraph_agent - INFO - [LangGraph] OK 使用 AsyncRedisSaver（redis://localhost:6379/0，TTL=7天）
2026-01-27 19:44:48,183 - app.services.agent.memory.metrics - INFO - [MemoryMetrics] 监控系统已初始化
2026-01-27 19:44:48,184 - app.services.agent.memory.long_term_store - INFO - [LongTermStore] Initialized: base_dir=./data/long_term_memory, max_size=50KB, compression=True
2026-01-27 19:44:48,184 - app.services.agent.memory.enhanced_memory_manager - INFO - EnhancedMemoryManager initialized: short=10, medium=100, threshold=0.1, long_term_backup=enabled
2026-01-27 19:44:48,184 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ EnhancedMemoryManager已创建
2026-01-27 19:44:48,185 - app.services.agent.memory.unified_coordinator - INFO - [UnifiedMemoryCoordinator] 初始化统一记忆协调器
2026-01-27 19:44:48,185 - app.services.agent.memory.unified_coordinator - INFO - [UnifiedMemoryCoordinator] 全局实例已设置
2026-01-27 19:44:48,186 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ UnifiedMemoryCoordinator已初始化 | checkpointer=AsyncRedisSaver | enhanced_memory=yes | context_manager=yes
2026-01-27 19:44:48,186 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ 解耦模块已初始化 (IntentClassifier, ToolExecutor, EventParser, ResponseBuilder, ToolDispatcher, ParallelExecutor, PlanGenerator, QuickPathHandler, StreamEventHandler, SecondaryToolHandler, TaskRunner, AgentExecutor)
2026-01-27 19:44:48,197 - app.services.agent.parallel_tool_node - INFO - [ParallelToolNode] 初始化完成，最大并发数=5，并行安全工具=6个
2026-01-27 19:44:48,213 - app.api.v1.agent - INFO - [Global Agent] created global agent instance; MemorySaver shared across requests
2026-01-27 19:44:48,236 - app.api.v1.agent - INFO - [agent_chat_stream] 📚 世界观数据已注入: 人物=8, 地点=7, 设定=7, 规范=无
2026-01-27 19:44:48,236 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21:c2f843f2-f06e-4e46-9f63-2b862f35b786 (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, conversation_id=c2f843f2-f06e-4e46-9f63-2b862f35b786)
2026-01-27 19:44:48,236 - app.services.context.monitoring_integration - INFO - ✅ ContextManager监控收集器已初始化
2026-01-27 19:44:48,243 - app.services.context.store - INFO - [ContextStore] Redis连接成功
2026-01-27 19:44:48,250 - app.services.context.manager - INFO - [ContextManager] 创建新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21:c2f843f2-f06e-4e46-9f63-2b862f35b786
2026-01-27 19:44:48,519 - app.services.context.token_counter - INFO - ✅ tiktoken初始化成功，模型: gemini-2.5-pro -> cl100k_base
2026-01-27 19:44:48,524 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21:c2f843f2-f06e-4e46-9f63-2b862f35b786: 0/16000 tokens
2026-01-27 19:44:49,488 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='仅限第1-60章。输出至少24条原文证据，覆盖以下主题：
1...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=3条
2026-01-27 19:44:49,488 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21 | 含用户级=True | 找到=3条
2026-01-27 19:44:49,540 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 1条消息, 0 tokens, 耗时 1303.68ms
2026-01-27 19:44:49,540 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 1 条历史消息 (token: 0, has_summary: False)
2026-01-27 19:44:49,540 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:44:49,540 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:44:49,543 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=200, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-27 19:44:51,682 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:44:51,682 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:44:51,718 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:44:51,718 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=678, cost=$0.000073, time=2138ms
2026-01-27 19:44:51,718 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=39, 尝试次数=1
2026-01-27 19:44:51,726 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:44:51,726 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:44:51,726 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=20, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-27 19:44:53,630 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:44:53,630 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:44:53,643 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:44:53,649 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=607, cost=$0.000061, time=1903ms
2026-01-27 19:44:53,649 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=7, 尝试次数=1
2026-01-27 19:44:53,651 - app.services.agent.intent.classifier - INFO - [Intent] AI识别结果: writing
2026-01-27 19:44:53,651 - app.services.agent.langgraph_agent - INFO - [Planning] AI意图分类: writing (置信度: 0.90)
2026-01-27 19:44:53,651 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 仅限第1-60章。输出至少24条原文证据，覆盖以下主题：
1. 林仙“摆烂/躺平/咸鱼/浑水摸鱼”的...
2026-01-27 19:44:53,651 - app.core.cache - INFO - ✅ 缓存命中: prompt:planning:v2.41.0:get_planning_static_prompt:fca6eb91156619d0
2026-01-27 19:44:53,661 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-27 19:44:53,661 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=story_planning, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: story_planning; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-01-27 19:44:53,661 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.3, task_type=TaskType.STORY_PLANNING
2026-01-27 19:45:09,181 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-27 19:45:24,754 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 25 个数据块，总长度: 1980
2026-01-27 19:45:24,754 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 22985 (prompt=21408, completion=1577)
2026-01-27 19:45:24,754 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:45:24,754 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-27 19:45:24,764 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:45:24,768 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=22985, cost=$0.042530, time=31093ms
2026-01-27 19:45:24,770 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=22985
2026-01-27 19:45:24,770 - app.services.agent.planning.plan_generator - WARNING - [Planning] 第1次尝试: JSON解析失败
2026-01-27 19:45:25,781 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-27 19:45:25,784 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=story_planning, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: story_planning; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-01-27 19:45:25,785 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.4, task_type=TaskType.STORY_PLANNING
2026-01-27 19:45:44,361 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-27 19:45:50,048 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 12 个数据块，总长度: 1408
2026-01-27 19:45:50,048 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 22380 (prompt=21646, completion=734)
2026-01-27 19:45:50,048 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:45:50,048 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-27 19:45:50,061 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:45:50,063 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=22380, cost=$0.034397, time=24263ms
2026-01-27 19:45:50,064 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=22380
2026-01-27 19:45:50,064 - app.services.agent.planning.plan_generator - INFO - [Planning] 第2次重试成功
2026-01-27 19:45:50,064 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户需要从作品的第1-60章中，提取并整理满足六个特定主题的, 原料=需要访问作品第1-60章的全部内容，以便, 处理=这是一个信息检索和整理任务。我将使用 `
2026-01-27 19:45:50,080 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共1个任务
2026-01-27 19:45:50,080 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共1个任务，耗时: 56.43s
2026-01-27 19:45:50,084 - app.api.v1.agent - INFO - [Stream] Plan tasks: 1 items
2026-01-27 19:45:50,085 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2026-01-27 19:45:50,085 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2026-01-27 19:45:50,085 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2026-01-27 19:45:50,085 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] DAG 调度启用，任务数=1, 有依赖任务=0
2026-01-27 19:45:50,087 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1开始: 在第1-60章内，检索并提取关于六个主题的原文证据：1. 林仙摆烂/躺平/咸鱼；2. 系统10086任务/提示；3. 坐标错投/一人之下/遮天/九龙拉棺/泰山；4. 遮天修炼体系/秘境术语；5. 青帝坟/帝兵/妖族/天璇/太玄/姬家等势力事件；6. 场景氛围转折。
2026-01-27 19:45:50,088 - app.api.v1.agent - INFO - [Stream] Task started: 在第1-60章内，检索并提取关于六个主题的原文证据：1. 林仙摆烂/躺平/咸鱼；2. 系统10086任务/提示；3. 坐标错投/一人之下/遮天/九龙拉棺/泰山；4. 遮天修炼体系/秘境术语；5. 青帝坟/帝兵/妖族/天璇/太玄/姬家等势力事件；6. 场景氛围转折。 (icon=Wrench)
2026-01-27 19:45:50,088 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: explore_content
2026-01-27 19:45:50,088 - app.services.agent.tools.explore_tools - INFO - [explore_content] 开始: work_id=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, target=在第1-60章内，检索并提取关于六个主题的原文证据：1. 林仙摆烂/躺平/咸鱼；2. 系统10086...
2026-01-27 19:45:50,089 - app.services.agent.tools.explore_tools - INFO - [explore_content] 规划传入关键词: ['摆烂', '躺平', '咸鱼', '浑水摸鱼', '系统10086', '试炼任务', '支线任务', '主线任务', '坐标错投', '一人之下']
2026-01-27 19:45:50,093 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 启用严格段落号模式
2026-01-27 19:45:50,097 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 章节范围锁定: 第1-60章
2026-01-27 19:45:50,098 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 任务禁止整章阅读
2026-01-27 19:45:50,098 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 开始探索 V5: work_id=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, target=在第1-60章内，检索并提取关于六个主题的原文证据：1. 林仙摆烂/躺平/咸鱼；2. 系统10086...
2026-01-27 19:45:50,099 - app.services.chapter_service - INFO - [ChapterService] Querying chapters for work_id=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, type=<class 'uuid.UUID'>
2026-01-27 19:45:50,118 - app.services.chapter_service - INFO - [ChapterService] Found 77 chapters
2026-01-27 19:45:50,118 - app.services.chapter_service - INFO -   - Chapter: 第1章 【摆烂的宿主】, order=1
2026-01-27 19:45:50,118 - app.services.chapter_service - INFO -   - ... (75 more chapters)
2026-01-27 19:45:50,119 - app.services.chapter_service - INFO -   - Chapter: 第100章 【火域铸真器，两脉起冲突】, order=77
2026-01-27 19:45:50,186 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 章节范围映射: 第1-60章 -> 第1-50章
2026-01-27 19:45:50,186 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-27 19:45:50,186 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-27 19:45:50,186 - app.services.ai.http_ai_service - INFO - [成本追踪] 初始化未传db/user_id，将使用请求上下文按需记录成本
2026-01-27 19:45:51,606 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz:8443/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-27 19:45:51,606 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:45:51,607 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:45:51,607 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:45:54,677 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:45:54,677 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:45:54,708 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:45:54,709 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=682, cost=$0.000116, time=3069ms
2026-01-27 19:45:54,710 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=293, 尝试次数=1
2026-01-27 19:45:54,768 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['林仙,摆烂,躺平,咸鱼']..., mode=all, range=(1, 50), hits=0
2026-01-27 19:45:54,770 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:45:54,770 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:45:54,770 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:45:56,813 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:45:56,814 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:45:56,824 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:45:56,825 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=718, cost=$0.000110, time=2043ms
2026-01-27 19:45:56,827 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=253, 尝试次数=1
2026-01-27 19:45:56,871 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['系统', '任务', '提示']..., mode=any, range=(1, 50), hits=10
2026-01-27 19:45:56,872 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:45:56,872 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:45:56,872 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:45:58,251 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:45:58,251 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:45:58,268 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:45:58,269 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1013, cost=$0.000167, time=1378ms
2026-01-27 19:45:58,269 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=570, 尝试次数=1
2026-01-27 19:45:58,301 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第23段
2026-01-27 19:45:58,326 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第24段
2026-01-27 19:45:58,343 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第25段
2026-01-27 19:45:58,352 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第28段
2026-01-27 19:45:58,372 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第34段
2026-01-27 19:45:58,376 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:45:58,376 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:45:58,376 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:45:59,816 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:45:59,818 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:45:59,834 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:45:59,838 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1387, cost=$0.000187, time=1441ms
2026-01-27 19:45:59,838 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=305, 尝试次数=1
2026-01-27 19:45:59,851 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['林仙', '摆烂', '躺平']..., mode=any, range=(1, 50), hits=5
2026-01-27 19:45:59,851 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:45:59,851 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:45:59,851 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:46:01,321 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:46:01,321 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:46:01,335 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:46:01,337 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=933, cost=$0.000139, time=1469ms
2026-01-27 19:46:01,338 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=334, 尝试次数=1
2026-01-27 19:46:01,351 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第2段
2026-01-27 19:46:01,368 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第6段
2026-01-27 19:46:01,378 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第10段
2026-01-27 19:46:01,387 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:46:01,388 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:46:01,388 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:46:02,828 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:46:02,828 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:46:02,837 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:46:02,837 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1399, cost=$0.000183, time=1440ms
2026-01-27 19:46:02,837 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=281, 尝试次数=1
2026-01-27 19:46:02,851 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第6段
2026-01-27 19:46:02,851 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:46:02,857 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:46:02,857 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:46:04,603 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:46:04,603 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:46:04,618 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:46:04,618 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1231, cost=$0.000189, time=1748ms
2026-01-27 19:46:04,618 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=446, 尝试次数=1
2026-01-27 19:46:04,759 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['一人之下', '遮天', '九龙拉棺']..., mode=any, range=(1, 50), hits=10
2026-01-27 19:46:04,762 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:46:04,762 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:46:04,762 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:46:05,784 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:46:05,784 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:46:05,801 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:46:05,801 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=991, cost=$0.000137, time=1022ms
2026-01-27 19:46:05,801 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=268, 尝试次数=1
2026-01-27 19:46:05,818 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['林仙', '摆烂', '躺平']..., mode=any, range=(1, 50), hits=5
2026-01-27 19:46:05,819 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:46:05,819 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:46:05,819 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:46:07,997 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:46:07,998 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:46:08,009 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:46:08,009 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1020, cost=$0.000173, time=2179ms
2026-01-27 19:46:08,009 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=486, 尝试次数=1
2026-01-27 19:46:08,009 - app.services.agent.tools.explore_tools - INFO - [ExploreState] 搜索词与已有词相似，跳过: '青帝坟' ~ '青帝'
2026-01-27 19:46:08,030 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['修炼', '秘境', '帝兵']..., mode=any, range=(1, 50), hits=10
2026-01-27 19:46:08,032 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:46:08,032 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:46:08,032 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:46:10,163 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:46:10,163 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:46:10,185 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:46:10,185 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=988, cost=$0.000133, time=2131ms
2026-01-27 19:46:10,185 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=235, 尝试次数=1
2026-01-27 19:46:10,201 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['林仙', '摆烂', '躺平']..., mode=any, range=(1, 50), hits=5
2026-01-27 19:46:10,201 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:46:10,209 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:46:10,209 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:46:11,743 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:46:11,743 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:46:11,756 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:46:11,759 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=936, cost=$0.000141, time=1533ms
2026-01-27 19:46:11,760 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=389, 尝试次数=1
2026-01-27 19:46:11,774 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第2段
2026-01-27 19:46:11,784 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第6段
2026-01-27 19:46:11,801 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第10段
2026-01-27 19:46:11,801 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:46:11,801 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:46:11,801 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:46:13,601 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:46:13,601 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:46:13,618 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:46:13,618 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1432, cost=$0.000197, time=1799ms
2026-01-27 19:46:13,618 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=375, 尝试次数=1
2026-01-27 19:46:13,637 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第2段
2026-01-27 19:46:13,651 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第6段
2026-01-27 19:46:13,659 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:46:13,659 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:46:13,660 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:46:15,209 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:46:15,209 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:46:15,226 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:46:15,228 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1447, cost=$0.000203, time=1549ms
2026-01-27 19:46:15,228 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=384, 尝试次数=1
2026-01-27 19:46:15,244 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第2段
2026-01-27 19:46:15,256 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第6段
2026-01-27 19:46:15,259 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:46:15,259 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:46:15,259 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:46:16,555 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:46:16,559 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:46:16,576 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:46:16,576 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1419, cost=$0.000191, time=1299ms
2026-01-27 19:46:16,579 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=350, 尝试次数=1
2026-01-27 19:46:16,593 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第2段
2026-01-27 19:46:16,612 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第6段
2026-01-27 19:46:16,612 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:46:16,617 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:46:16,618 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:46:17,744 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:46:17,744 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:46:17,753 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:46:17,759 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1450, cost=$0.000204, time=1126ms
2026-01-27 19:46:17,760 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=389, 尝试次数=1
2026-01-27 19:46:17,768 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第2段
2026-01-27 19:46:17,781 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第6段
2026-01-27 19:46:17,785 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:46:17,787 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:46:17,787 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:46:18,968 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:46:18,968 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:46:18,978 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:46:18,978 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1415, cost=$0.000190, time=1180ms
2026-01-27 19:46:18,978 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=344, 尝试次数=1
2026-01-27 19:46:18,993 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第2段
2026-01-27 19:46:19,004 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第6段
2026-01-27 19:46:19,004 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:46:19,009 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:46:19,010 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:46:20,063 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:46:20,063 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:46:20,076 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:46:20,082 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1396, cost=$0.000182, time=1053ms
2026-01-27 19:46:20,082 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=277, 尝试次数=1
2026-01-27 19:46:20,093 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第6段
2026-01-27 19:46:20,101 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:46:20,101 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:46:20,103 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:46:21,369 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:46:21,369 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:46:21,384 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:46:21,385 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1151, cost=$0.000159, time=1266ms
2026-01-27 19:46:21,385 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=286, 尝试次数=1
2026-01-27 19:46:21,397 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第6段
2026-01-27 19:46:21,401 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:46:21,401 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:46:21,401 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:46:22,814 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:46:22,814 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:46:22,826 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:46:22,826 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1175, cost=$0.000169, time=1412ms
2026-01-27 19:46:22,826 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=319, 尝试次数=1
2026-01-27 19:46:22,877 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['泰山', '一人之下', '遮天']..., mode=any, range=(1, 50), hits=5
2026-01-27 19:46:22,882 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:46:22,882 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:46:22,882 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:46:24,327 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:46:24,328 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:46:24,343 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:46:24,345 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=856, cost=$0.000116, time=1446ms
2026-01-27 19:46:24,345 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=217, 尝试次数=1
2026-01-27 19:46:24,361 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['林仙', '摆烂', '躺平']..., mode=any, range=(1, 50), hits=5
2026-01-27 19:46:24,361 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:46:24,361 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:46:24,361 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:46:25,671 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:46:25,671 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:46:25,684 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:46:25,684 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=913, cost=$0.000132, time=1310ms
2026-01-27 19:46:25,684 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=279, 尝试次数=1
2026-01-27 19:46:25,701 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['林仙', '一人之下', '遮天']..., mode=any, range=(1, 50), hits=5
2026-01-27 19:46:25,702 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:46:25,702 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:46:25,702 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:46:27,271 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:46:27,271 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:46:27,288 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:46:27,292 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=945, cost=$0.000143, time=1568ms
2026-01-27 19:46:27,293 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=312, 尝试次数=1
2026-01-27 19:46:27,330 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['林仙', '摆烂', '躺平']..., mode=all, range=(1, 50), hits=0
2026-01-27 19:46:27,330 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:46:27,330 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:46:27,334 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:46:28,643 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:46:28,643 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:46:28,657 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:46:28,659 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=733, cost=$0.000109, time=1309ms
2026-01-27 19:46:28,659 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=255, 尝试次数=1
2026-01-27 19:46:28,674 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['林仙', '摆烂']..., mode=any, range=(1, 50), hits=5
2026-01-27 19:46:28,674 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:46:28,674 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:46:28,674 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:46:30,132 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:46:30,132 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:46:30,143 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:46:30,143 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=888, cost=$0.000124, time=1458ms
2026-01-27 19:46:30,143 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=239, 尝试次数=1
2026-01-27 19:46:30,159 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['林仙', '躺平']..., mode=any, range=(1, 50), hits=5
2026-01-27 19:46:30,159 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:46:30,163 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:46:30,163 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:46:31,379 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:46:31,379 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:46:31,393 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:46:31,393 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=891, cost=$0.000125, time=1215ms
2026-01-27 19:46:31,399 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=243, 尝试次数=1
2026-01-27 19:46:31,464 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['一人之下', '遮天', '九龙拉棺']..., mode=any, range=(1, 50), hits=10
2026-01-27 19:46:31,464 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:46:31,468 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:46:31,468 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:46:32,955 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:46:32,955 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:46:32,967 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:46:32,967 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1031, cost=$0.000160, time=1486ms
2026-01-27 19:46:32,967 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=455, 尝试次数=1
2026-01-27 19:46:32,985 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第36段
2026-01-27 19:46:32,994 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第39段
2026-01-27 19:46:33,009 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第40段
2026-01-27 19:46:33,025 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第42段
2026-01-27 19:46:33,035 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第43段
2026-01-27 19:46:33,035 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:46:33,035 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:46:33,035 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:46:34,751 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:46:34,751 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:46:34,767 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:46:34,767 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1492, cost=$0.000231, time=1715ms
2026-01-27 19:46:34,767 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=615, 尝试次数=1
2026-01-27 19:46:34,784 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第34段
2026-01-27 19:46:34,803 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第35段
2026-01-27 19:46:34,818 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第36段
2026-01-27 19:46:34,829 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第37段
2026-01-27 19:46:34,834 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第38段
2026-01-27 19:46:34,843 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:46:34,843 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:46:34,844 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:46:36,447 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:46:36,447 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:46:36,461 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:46:36,461 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1399, cost=$0.000191, time=1603ms
2026-01-27 19:46:36,461 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=363, 尝试次数=1
2026-01-27 19:46:36,484 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第36段
2026-01-27 19:46:36,493 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第37段
2026-01-27 19:46:36,493 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:46:36,493 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:46:36,501 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:46:38,455 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:46:38,455 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:46:38,469 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:46:38,476 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1416, cost=$0.000203, time=1958ms
2026-01-27 19:46:38,476 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=444, 尝试次数=1
2026-01-27 19:46:38,493 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第34段
2026-01-27 19:46:38,511 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第35段
2026-01-27 19:46:38,521 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第36段
2026-01-27 19:46:38,521 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:46:38,526 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:46:38,526 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:46:40,430 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:46:40,430 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:46:40,447 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:46:40,447 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1462, cost=$0.000216, time=1904ms
2026-01-27 19:46:40,447 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=425, 尝试次数=1
2026-01-27 19:46:40,447 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:46:40,451 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:46:40,452 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:46:41,347 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:46:41,351 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:46:41,360 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:46:41,368 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=695, cost=$0.000098, time=900ms
2026-01-27 19:46:41,368 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=216, 尝试次数=1
2026-01-27 19:46:41,396 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['泰山']..., mode=any, range=(1, 50), hits=5
2026-01-27 19:46:41,396 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:46:41,396 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:46:41,396 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:46:42,402 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:46:42,402 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:46:42,417 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:46:42,419 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=870, cost=$0.000122, time=1005ms
2026-01-27 19:46:42,420 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=248, 尝试次数=1
2026-01-27 19:46:42,437 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['林仙', '摆烂', '躺平']..., mode=any, range=(1, 50), hits=5
2026-01-27 19:46:42,440 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:46:42,441 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:46:42,442 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:46:43,792 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:46:43,793 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:46:43,809 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:46:43,811 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=919, cost=$0.000134, time=1351ms
2026-01-27 19:46:43,811 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=288, 尝试次数=1
2026-01-27 19:46:43,861 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['林仙', '摆烂', '躺平']..., mode=any, range=(1, 50), hits=3
2026-01-27 19:46:43,861 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:46:43,864 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:46:43,864 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:46:45,160 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:46:45,160 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:46:45,176 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:46:45,180 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=858, cost=$0.000125, time=1295ms
2026-01-27 19:46:45,180 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=274, 尝试次数=1
2026-01-27 19:46:45,202 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['坐标错投']..., mode=any, range=(1, 50), hits=0
2026-01-27 19:46:45,202 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:46:45,202 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:46:45,202 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:46:46,452 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:46:46,452 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:46:46,468 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:46:46,468 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=746, cost=$0.000117, time=1250ms
2026-01-27 19:46:46,468 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=284, 尝试次数=1
2026-01-27 19:46:46,530 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['一人之下', '遮天', '九龙拉棺']..., mode=any, range=(1, 50), hits=10
2026-01-27 19:46:46,534 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:46:46,534 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:46:46,534 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:46:48,380 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:46:48,380 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:46:48,401 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:46:48,401 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1032, cost=$0.000160, time=1846ms
2026-01-27 19:46:48,401 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=459, 尝试次数=1
2026-01-27 19:46:48,418 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第36段
2026-01-27 19:46:48,428 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第39段
2026-01-27 19:46:48,446 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第40段
2026-01-27 19:46:48,463 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第42段
2026-01-27 19:46:48,477 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第43段
2026-01-27 19:46:48,482 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:46:48,482 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:46:48,485 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:46:50,024 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:46:50,026 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:46:50,034 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:46:50,034 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1449, cost=$0.000213, time=1541ms
2026-01-27 19:46:50,034 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=440, 尝试次数=1
2026-01-27 19:46:50,053 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第36段
2026-01-27 19:46:50,068 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第39段
2026-01-27 19:46:50,073 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:46:50,074 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:46:50,074 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:46:51,294 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:46:51,294 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:46:51,301 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:46:51,301 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1402, cost=$0.000195, time=1222ms
2026-01-27 19:46:51,301 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=372, 尝试次数=1
2026-01-27 19:46:51,319 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第36段
2026-01-27 19:46:51,327 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第39段
2026-01-27 19:46:51,333 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:46:51,333 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:46:51,334 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:46:53,243 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:46:53,243 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:46:53,251 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:46:53,251 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1410, cost=$0.000197, time=1908ms
2026-01-27 19:46:53,259 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=381, 尝试次数=1
2026-01-27 19:46:53,276 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第36段
2026-01-27 19:46:53,293 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第39段
2026-01-27 19:46:53,293 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:46:53,293 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:46:53,293 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:46:54,897 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:46:54,898 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:46:54,911 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:46:54,911 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1413, cost=$0.000199, time=1605ms
2026-01-27 19:46:54,911 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=388, 尝试次数=1
2026-01-27 19:46:54,931 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第36段
2026-01-27 19:46:54,942 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第39段
2026-01-27 19:46:54,942 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:46:54,942 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:46:54,942 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:46:56,427 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:46:56,427 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:46:56,436 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:46:56,438 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1420, cost=$0.000202, time=1484ms
2026-01-27 19:46:56,438 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=395, 尝试次数=1
2026-01-27 19:46:56,448 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第36段
2026-01-27 19:46:56,459 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第39段
2026-01-27 19:46:56,464 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:46:56,465 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:46:56,465 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:46:57,681 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:46:57,681 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:46:57,698 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:46:57,698 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1419, cost=$0.000201, time=1217ms
2026-01-27 19:46:57,698 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=394, 尝试次数=1
2026-01-27 19:46:57,710 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第36段
2026-01-27 19:46:57,723 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第39段
2026-01-27 19:46:57,726 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:46:57,726 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:46:57,726 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:46:58,881 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:46:58,881 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:46:58,897 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:46:58,897 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1406, cost=$0.000196, time=1154ms
2026-01-27 19:46:58,899 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=377, 尝试次数=1
2026-01-27 19:46:58,910 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第36段
2026-01-27 19:46:58,923 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第39段
2026-01-27 19:46:58,927 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:46:58,928 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:46:58,928 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:47:00,352 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:47:00,352 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:47:00,369 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:47:00,369 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1405, cost=$0.000196, time=1424ms
2026-01-27 19:47:00,371 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=379, 尝试次数=1
2026-01-27 19:47:00,381 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第36段
2026-01-27 19:47:00,394 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第39段
2026-01-27 19:47:00,395 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 探索完成(工具循环): 44轮, 原因=达到读取上限
2026-01-27 19:47:00,402 - app.services.agent.execution.tool_executor - INFO - [StandardTool] explore_content 执行成功
2026-01-27 19:47:00,406 - app.api.v1.agent - INFO - [Stream] 任务完成: 在第1-60章内，检索并提取关于六个主题的原文证据：1. 林仙摆烂/躺平/咸鱼；2. 系统10086任务/提示；3. 坐标错投/一人之下/遮天/九龙拉棺/泰山；4. 遮天修炼体系/秘境术语；5. 青帝坟/帝兵/妖族/天璇/太玄/姬家等势力事件；6. 场景氛围转折。 (70.3s)
2026-01-27 19:47:00,407 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1完成
2026-01-27 19:47:00,408 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共1个任务，耗时: 70.32s
2026-01-27 19:47:00,410 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2026-01-27 19:47:00,411 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=1, 展示型=0
2026-01-27 19:47:00,411 - app.services.agent.langgraph_agent - INFO - [Response] 单个输出任务(explore_content)，使用AI整合
2026-01-27 19:47:00,412 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2026-01-27 19:47:00,412 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=1, 展示型=0
2026-01-27 19:47:00,412 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=1026字符, 处理后=1163字符
2026-01-27 19:47:00,412 - app.services.agent.planning.response_builder - INFO - [Summarization] 准备发送 summarization_start 事件
2026-01-27 19:47:00,412 - app.services.agent.stream.stream_event_handler - INFO - [StreamEventHandler] emit_summarization_start 被调用, _on_flow_event=True
2026-01-27 19:47:00,412 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_start 事件已发送
2026-01-27 19:47:00,414 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2026-01-27 19:47:00,414 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2026-01-27 19:47:00,422 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-27 19:47:00,424 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-27 19:47:00,424 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
2026-01-27 19:47:25,973 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-27 19:47:25,977 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_complete 事件已发送（第一个chunk时）
2026-01-27 19:47:25,978 - app.services.agent.planning.response_builder - INFO - [Summarization] output_ready 事件已发送（第一个chunk时）
2026-01-27 19:47:31,535 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 21 个数据块，总长度: 1778
2026-01-27 19:47:31,536 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 9080 (prompt=7768, completion=1312)
2026-01-27 19:47:31,536 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:47:31,537 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-27 19:47:31,553 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:47:31,554 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=9080, cost=$0.005610, time=31112ms
2026-01-27 19:47:31,555 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=1778
2026-01-27 19:47:31,634 - app.services.context.vector_memory_store - INFO - 🔁 跳过重复记忆，复用ID=79913e7e-d5cd-4e09-bce6-ca6639bd8456_1769513360100_5a4e7a65
2026-01-27 19:47:31,635 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21 | 重要度=0.87
2026-01-27 19:47:32,560 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21 | 重要度=0.77
2026-01-27 19:47:32,568 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21:c2f843f2-f06e-4e46-9f63-2b862f35b786, token=2318
2026-01-27 19:47:32,571 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21:c2f843f2-f06e-4e46-9f63-2b862f35b786, 消息数=2, 摘要长度=0, Token=2318
2026-01-27 19:47:32,572 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21:c2f843f2-f06e-4e46-9f63-2b862f35b786)
2026-01-27 19:47:32,573 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2026-01-27 19:47:32,579 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed
2026-01-27 19:47:43,920 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/c2f843f2-f06e-4e46-9f63-2b862f35b786
INFO:     127.0.0.1:49270 - "GET /api/v1/agent/operations/c2f843f2-f06e-4e46-9f63-2b862f35b786 HTTP/1.1" 200 OK
2026-01-27 19:48:29,865 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-27 19:48:29,866 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-27 19:48:29,866 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2026-01-27 19:48:31,339 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz:8443/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-27 19:48:31,340 - app.api.v1.agent - INFO - [Chat Stream] Mode: planning
2026-01-27 19:48:31,343 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:54151 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2026-01-27 19:48:31,349 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 仅限第40–100章。输出至少24条原文证据，覆盖以下主题：

  1. 青帝坟/妖帝/帝兵/混沌青...
2026-01-27 19:48:31,363 - app.api.v1.agent - INFO - [agent_chat_stream] 📚 世界观数据已注入: 人物=8, 地点=7, 设定=7, 规范=无
2026-01-27 19:48:31,363 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21:c2f843f2-f06e-4e46-9f63-2b862f35b786 (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, conversation_id=c2f843f2-f06e-4e46-9f63-2b862f35b786)
2026-01-27 19:48:31,370 - app.services.context.store - INFO - [ContextStore] 加载上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21:c2f843f2-f06e-4e46-9f63-2b862f35b786, 2条消息
2026-01-27 19:48:31,371 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21:c2f843f2-f06e-4e46-9f63-2b862f35b786: 2318/16000 tokens
2026-01-27 19:48:31,511 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='仅限第40–100章。输出至少24条原文证据，覆盖以下主题：...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=3条
2026-01-27 19:48:31,511 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21 | 含用户级=True | 找到=3条
2026-01-27 19:48:31,520 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 3条消息, 2318 tokens, 耗时 156.86ms
2026-01-27 19:48:31,520 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 3 条历史消息 (token: 2318, has_summary: False)
2026-01-27 19:48:31,520 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:48:31,520 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:48:31,522 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=200, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-27 19:48:32,911 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:48:32,911 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:48:32,932 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:48:32,932 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2123, cost=$0.000218, time=1388ms
2026-01-27 19:48:32,932 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=39, 尝试次数=1
2026-01-27 19:48:32,932 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:48:32,932 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:48:32,932 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=20, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-27 19:48:33,681 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:48:33,681 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:48:33,698 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:48:33,700 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=557, cost=$0.000056, time=748ms
2026-01-27 19:48:33,700 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=7, 尝试次数=1
2026-01-27 19:48:33,702 - app.services.agent.intent.classifier - INFO - [Intent] AI识别结果: writing
2026-01-27 19:48:33,702 - app.services.agent.langgraph_agent - INFO - [Planning] AI意图分类: writing (置信度: 0.90)
2026-01-27 19:48:33,702 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 仅限第40–100章。输出至少24条原文证据，覆盖以下主题：

  1. 青帝坟/妖帝/帝兵/混沌青...
2026-01-27 19:48:33,712 - app.core.cache - INFO - ✅ 缓存命中: prompt:planning:v2.41.0:get_planning_static_prompt:fca6eb91156619d0
2026-01-27 19:48:33,717 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-27 19:48:33,717 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=story_planning, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: story_planning; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-01-27 19:48:33,717 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.3, task_type=TaskType.STORY_PLANNING
2026-01-27 19:48:53,145 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-27 19:48:58,077 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 12 个数据块，总长度: 1419
2026-01-27 19:48:58,077 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 24170 (prompt=23459, completion=711)
2026-01-27 19:48:58,078 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:48:58,078 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-27 19:48:58,089 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:48:58,089 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=24170, cost=$0.036434, time=24362ms
2026-01-27 19:48:58,089 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=24170
2026-01-27 19:48:58,089 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户需要从第40-100章中，根据6个指定主题，提取至少24, 原料=需要使用`explore_content, 处理=构建一个`explore_content
2026-01-27 19:48:58,089 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共1个任务
2026-01-27 19:48:58,089 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共1个任务，耗时: 24.39s
2026-01-27 19:48:58,089 - app.api.v1.agent - INFO - [Stream] Plan tasks: 1 items
2026-01-27 19:48:58,089 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2026-01-27 19:48:58,089 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2026-01-27 19:48:58,089 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2026-01-27 19:48:58,089 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] DAG 调度启用，任务数=1, 有依赖任务=0
2026-01-27 19:48:58,089 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1开始: 在第40-100章内，根据用户指定的六个主题和关键词，检索并提取原文段落作为证据。
2026-01-27 19:48:58,098 - app.api.v1.agent - INFO - [Stream] Task started: 在第40-100章内，根据用户指定的六个主题和关键词，检索并提取原文段落作为证据。 (icon=Wrench)
2026-01-27 19:48:58,098 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: explore_content
2026-01-27 19:48:58,098 - app.services.agent.tools.explore_tools - INFO - [explore_content] 开始: work_id=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, target=在第40-100章范围内，检索并提取满足以下6个主题的原文证据，并标注章节和段落号：1. 青帝坟/妖...
2026-01-27 19:48:58,098 - app.services.agent.tools.explore_tools - INFO - [explore_content] 规划传入关键词: ['青帝坟', '妖帝', '帝兵', '混沌青莲', '颜如玉', '聚宝盆', '系统10086', '系统10086为您服务', '段德', '考古']
2026-01-27 19:48:58,098 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 启用严格段落号模式
2026-01-27 19:48:58,098 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 章节范围锁定: 第40-100章
2026-01-27 19:48:58,102 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 任务禁止整章阅读
2026-01-27 19:48:58,102 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 开始探索 V5: work_id=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, target=在第40-100章范围内，检索并提取满足以下6个主题的原文证据，并标注章节和段落号：1. 青帝坟/妖...
2026-01-27 19:48:58,102 - app.services.chapter_service - INFO - [ChapterService] Querying chapters for work_id=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, type=<class 'uuid.UUID'>
2026-01-27 19:48:58,119 - app.services.chapter_service - INFO - [ChapterService] Found 77 chapters
2026-01-27 19:48:58,119 - app.services.chapter_service - INFO -   - Chapter: 第1章 【摆烂的宿主】, order=1
2026-01-27 19:48:58,122 - app.services.chapter_service - INFO -   - ... (75 more chapters)
2026-01-27 19:48:58,122 - app.services.chapter_service - INFO -   - Chapter: 第100章 【火域铸真器，两脉起冲突】, order=77
2026-01-27 19:48:58,162 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 章节范围映射: 第40-100章 -> 第34-77章
2026-01-27 19:48:58,163 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:48:58,163 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:48:58,164 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:48:59,726 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:48:59,726 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:48:59,752 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:48:59,752 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=656, cost=$0.000088, time=1565ms
2026-01-27 19:48:59,752 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=151, 尝试次数=1
2026-01-27 19:48:59,752 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:48:59,752 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:48:59,752 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:49:02,009 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:49:02,009 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:49:02,027 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:49:02,029 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1756, cost=$0.000282, time=2257ms
2026-01-27 19:49:02,029 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=696, 尝试次数=1
2026-01-27 19:49:02,071 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['青帝坟', '妖帝', '帝兵']..., mode=any, range=(34, 77), hits=10
2026-01-27 19:49:02,073 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:49:02,073 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:49:02,073 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:49:03,642 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:49:03,642 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:49:03,655 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:49:03,655 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1293, cost=$0.000192, time=1569ms
2026-01-27 19:49:03,655 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=556, 尝试次数=1
2026-01-27 19:49:03,683 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第2段
2026-01-27 19:49:03,697 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第3段
2026-01-27 19:49:03,710 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第6段
2026-01-27 19:49:03,721 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第8段
2026-01-27 19:49:03,721 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:49:03,721 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:49:03,725 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:49:05,280 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:49:05,282 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:49:05,292 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:49:05,300 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1515, cost=$0.000205, time=1558ms
2026-01-27 19:49:05,303 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=363, 尝试次数=1
2026-01-27 19:49:05,317 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第40章第2段
2026-01-27 19:49:05,327 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第40章第3段
2026-01-27 19:49:05,331 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:49:05,331 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:49:05,333 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:49:07,097 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:49:07,097 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:49:07,109 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:49:07,109 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1619, cost=$0.000253, time=1765ms
2026-01-27 19:49:07,109 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=646, 尝试次数=1
2026-01-27 19:49:07,125 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第47章第1段
2026-01-27 19:49:07,139 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第47章第2段
2026-01-27 19:49:07,150 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第47章第3段
2026-01-27 19:49:07,167 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第47章第4段
2026-01-27 19:49:07,171 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:49:07,171 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:49:07,171 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:49:08,412 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:49:08,412 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:49:08,432 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:49:08,434 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1480, cost=$0.000199, time=1241ms
2026-01-27 19:49:08,434 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=361, 尝试次数=1
2026-01-27 19:49:08,453 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第47章第1段
2026-01-27 19:49:08,472 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第47章第2段
2026-01-27 19:49:08,475 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:49:08,475 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:49:08,475 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:49:10,352 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:49:10,352 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:49:10,371 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:49:10,373 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1638, cost=$0.000262, time=1877ms
2026-01-27 19:49:10,373 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=648, 尝试次数=1
2026-01-27 19:49:10,427 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['青帝坟', '妖帝', '帝兵']..., mode=any, range=(34, 77), hits=10
2026-01-27 19:49:10,428 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:49:10,429 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:49:10,429 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:49:11,960 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:49:11,960 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:49:11,976 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:49:11,977 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1266, cost=$0.000181, time=1530ms
2026-01-27 19:49:11,977 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=453, 尝试次数=1
2026-01-27 19:49:11,991 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第2段
2026-01-27 19:49:12,000 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第3段
2026-01-27 19:49:12,009 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第6段
2026-01-27 19:49:12,026 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第8段
2026-01-27 19:49:12,028 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:49:12,028 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:49:12,028 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:49:13,312 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:49:13,313 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:49:13,327 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:49:13,328 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1550, cost=$0.000218, time=1285ms
2026-01-27 19:49:13,329 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=445, 尝试次数=1
2026-01-27 19:49:13,342 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第40章第2段
2026-01-27 19:49:13,354 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第40章第3段
2026-01-27 19:49:13,354 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:49:13,358 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:49:13,359 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:49:15,920 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:49:15,920 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:49:15,932 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:49:15,933 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1611, cost=$0.000248, time=2561ms
2026-01-27 19:49:15,933 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=644, 尝试次数=1
2026-01-27 19:49:15,945 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第47章第1段
2026-01-27 19:49:15,955 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第47章第2段
2026-01-27 19:49:15,966 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第47章第3段
2026-01-27 19:49:15,977 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第47章第4段
2026-01-27 19:49:15,980 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:49:15,980 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:49:15,981 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:49:17,223 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:49:17,223 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:49:17,234 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:49:17,242 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1479, cost=$0.000199, time=1242ms
2026-01-27 19:49:17,243 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=361, 尝试次数=1
2026-01-27 19:49:17,262 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第47章第1段
2026-01-27 19:49:17,277 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第47章第2段
2026-01-27 19:49:17,277 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:49:17,277 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:49:17,277 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:49:19,181 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:49:19,182 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:49:19,195 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:49:19,195 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1653, cost=$0.000268, time=1906ms
2026-01-27 19:49:19,195 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=687, 尝试次数=1
2026-01-27 19:49:19,235 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['青帝坟', '妖帝', '帝兵']..., mode=any, range=(34, 77), hits=10
2026-01-27 19:49:19,235 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:49:19,235 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:49:19,242 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:49:20,703 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:49:20,703 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:49:20,724 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:49:20,725 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1303, cost=$0.000195, time=1460ms
2026-01-27 19:49:20,725 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=568, 尝试次数=1
2026-01-27 19:49:20,734 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第2段
2026-01-27 19:49:20,753 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第3段
2026-01-27 19:49:20,763 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第6段
2026-01-27 19:49:20,773 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第8段
2026-01-27 19:49:20,775 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:49:20,775 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:49:20,775 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:49:22,102 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:49:22,102 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:49:22,118 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:49:22,118 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1531, cost=$0.000210, time=1328ms
2026-01-27 19:49:22,118 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=386, 尝试次数=1
2026-01-27 19:49:22,135 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第40章第2段
2026-01-27 19:49:22,150 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第40章第3段
2026-01-27 19:49:22,150 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:49:22,156 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:49:22,156 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:49:23,572 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:49:23,572 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:49:23,588 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:49:23,592 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1574, cost=$0.000234, time=1415ms
2026-01-27 19:49:23,592 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=593, 尝试次数=1
2026-01-27 19:49:23,603 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第47章第1段
2026-01-27 19:49:23,617 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第47章第2段
2026-01-27 19:49:23,625 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第47章第3段
2026-01-27 19:49:23,642 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第47章第4段
2026-01-27 19:49:23,645 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:49:23,645 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:49:23,645 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:49:24,980 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:49:24,980 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:49:25,000 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:49:25,000 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1487, cost=$0.000201, time=1335ms
2026-01-27 19:49:25,000 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=366, 尝试次数=1
2026-01-27 19:49:25,017 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第54章第1段
2026-01-27 19:49:25,027 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第54章第2段
2026-01-27 19:49:25,033 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:49:25,033 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:49:25,033 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:49:26,602 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:49:26,606 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:49:26,618 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:49:26,618 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1435, cost=$0.000203, time=1572ms
2026-01-27 19:49:26,626 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=397, 尝试次数=1
2026-01-27 19:49:26,642 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第70章第1段
2026-01-27 19:49:26,650 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第70章第2段
2026-01-27 19:49:26,650 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:49:26,650 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:49:26,650 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:49:28,192 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:49:28,193 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:49:28,202 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:49:28,202 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1569, cost=$0.000219, time=1543ms
2026-01-27 19:49:28,202 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=400, 尝试次数=1
2026-01-27 19:49:28,212 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第70章第1段
2026-01-27 19:49:28,225 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第70章第2段
2026-01-27 19:49:28,225 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:49:28,225 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:49:28,225 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:49:29,897 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:49:29,897 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:49:29,907 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:49:29,907 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1551, cost=$0.000212, time=1675ms
2026-01-27 19:49:29,917 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=387, 尝试次数=1
2026-01-27 19:49:29,933 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第70章第1段
2026-01-27 19:49:29,949 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第70章第2段
2026-01-27 19:49:29,950 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:49:29,955 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:49:29,955 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:49:31,427 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:49:31,427 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:49:31,443 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:49:31,443 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1574, cost=$0.000222, time=1477ms
2026-01-27 19:49:31,450 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=406, 尝试次数=1
2026-01-27 19:49:31,467 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第70章第1段
2026-01-27 19:49:31,477 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第70章第2段
2026-01-27 19:49:31,477 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:49:31,483 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:49:31,484 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:49:33,234 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:49:33,234 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:49:33,252 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:49:33,252 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1579, cost=$0.000224, time=1750ms
2026-01-27 19:49:33,252 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=411, 尝试次数=1
2026-01-27 19:49:33,272 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第70章第1段
2026-01-27 19:49:33,284 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第70章第2段
2026-01-27 19:49:33,284 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:49:33,284 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:49:33,284 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:49:35,633 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:49:35,633 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:49:35,650 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:49:35,652 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1868, cost=$0.000339, time=2350ms
2026-01-27 19:49:35,652 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=1284, 尝试次数=1
2026-01-27 19:49:35,667 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第40章第1段
2026-01-27 19:49:35,687 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第40章第2段
2026-01-27 19:49:35,704 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第40章第3段
2026-01-27 19:49:35,718 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第40章第4段
2026-01-27 19:49:35,732 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第40章第5段
2026-01-27 19:49:35,745 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第40章第6段
2026-01-27 19:49:35,756 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第40章第7段
2026-01-27 19:49:35,767 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第40章第8段
2026-01-27 19:49:35,778 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第40章第9段
2026-01-27 19:49:35,787 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第40章第10段
2026-01-27 19:49:35,798 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第40章第11段
2026-01-27 19:49:35,809 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第40章第12段
2026-01-27 19:49:35,819 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第40章第13段
2026-01-27 19:49:35,819 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:49:35,819 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:49:35,825 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:49:37,441 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:49:37,443 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:49:37,459 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:49:37,462 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1552, cost=$0.000224, time=1617ms
2026-01-27 19:49:37,462 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=516, 尝试次数=1
2026-01-27 19:49:37,462 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:49:37,462 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:49:37,468 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:49:38,888 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:49:38,888 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:49:38,904 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:49:38,908 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=851, cost=$0.000131, time=1423ms
2026-01-27 19:49:38,910 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=291, 尝试次数=1
2026-01-27 19:49:38,968 - app.services.chapter_vector_service - INFO - [exact_search] work=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21, keywords=['段德', '源', '寻宝']..., mode=any, range=(34, 77), hits=10
2026-01-27 19:49:38,968 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-27 19:49:38,968 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-27 19:49:38,973 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-27 19:49:40,128 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:49:40,128 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-27 19:49:40,143 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:49:40,151 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1036, cost=$0.000137, time=1159ms
2026-01-27 19:49:40,151 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=225, 尝试次数=1
2026-01-27 19:49:40,167 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第34章第14段
2026-01-27 19:49:40,167 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 探索完成(工具循环): 25轮, 原因=达到读取上限
2026-01-27 19:49:40,184 - app.services.agent.execution.tool_executor - INFO - [StandardTool] explore_content 执行成功
2026-01-27 19:49:40,186 - app.api.v1.agent - INFO - [Stream] 任务完成: 在第40-100章内，根据用户指定的六个主题和关键词，检索并提取原文段落作为证据。 (42.1s)
2026-01-27 19:49:40,186 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1完成
2026-01-27 19:49:40,192 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共1个任务，耗时: 42.10s
2026-01-27 19:49:40,192 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2026-01-27 19:49:40,192 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=1, 展示型=0
2026-01-27 19:49:40,192 - app.services.agent.langgraph_agent - INFO - [Response] 单个输出任务(explore_content)，使用AI整合
2026-01-27 19:49:40,192 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2026-01-27 19:49:40,196 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=1, 展示型=0
2026-01-27 19:49:40,196 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=1782字符, 处理后=1828字符
2026-01-27 19:49:40,196 - app.services.agent.planning.response_builder - INFO - [Summarization] 准备发送 summarization_start 事件
2026-01-27 19:49:40,196 - app.services.agent.stream.stream_event_handler - INFO - [StreamEventHandler] emit_summarization_start 被调用, _on_flow_event=True
2026-01-27 19:49:40,197 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_start 事件已发送
2026-01-27 19:49:40,197 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2026-01-27 19:49:40,197 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2026-01-27 19:49:40,209 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-27 19:49:40,209 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-27 19:49:40,209 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
2026-01-27 19:50:12,881 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-27 19:50:12,884 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_complete 事件已发送（第一个chunk时）
2026-01-27 19:50:12,885 - app.services.agent.planning.response_builder - INFO - [Summarization] output_ready 事件已发送（第一个chunk时）
2026-01-27 19:50:18,577 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 21 个数据块，总长度: 1833
2026-01-27 19:50:18,577 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 11861 (prompt=10502, completion=1359)
2026-01-27 19:50:18,578 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-27 19:50:18,578 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-27 19:50:18,589 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-27 19:50:18,589 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=11861, cost=$0.006548, time=38369ms
2026-01-27 19:50:18,590 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=1833
2026-01-27 19:50:18,592 - app.services.context.vector_memory_store - INFO - 🔁 跳过重复记忆，复用ID=79913e7e-d5cd-4e09-bce6-ca6639bd8456_1769513204940_e9bb499d
2026-01-27 19:50:18,593 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21 | 重要度=1.00
2026-01-27 19:50:19,488 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21 | 重要度=0.60
2026-01-27 19:50:19,496 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21:c2f843f2-f06e-4e46-9f63-2b862f35b786, token=4675
2026-01-27 19:50:19,499 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21:c2f843f2-f06e-4e46-9f63-2b862f35b786, 消息数=4, 摘要长度=0, Token=4675
2026-01-27 19:50:19,500 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:5fe6c67d-8a1b-48c1-ad56-a5281eb22e21:c2f843f2-f06e-4e46-9f63-2b862f35b786)
2026-01-27 19:50:19,501 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2026-01-27 19:50:19,507 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed