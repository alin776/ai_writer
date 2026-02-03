(venv) PS D:\Java\ai_writer\backend>
(venv) PS D:\Java\ai_writer\backend> python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
INFO:     Will watch for changes in these directories: ['D:\\Java\\ai_writer\\backend']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [43788] using WatchFiles
已注册策略: web_novel_11d - 网文11维度分析
2026-02-03 16:14:21,864 - app.main - INFO - [STARTUP] 监控中间件已注册: TraceMiddleware, MonitoringMiddleware
INFO:     Started server process [45100]
INFO:     Waiting for application startup.
2026-02-03 16:14:22,124 - app.main - INFO - [STARTUP] 应用启动中...
2026-02-03 16:14:22,124 - app.core.database - INFO - 正在初始化数据库... (尝试 1/3)
2026-02-03 16:14:22,281 - app.core.database - INFO - ✅ 数据库初始化成功
2026-02-03 16:14:22,290 - app.main - INFO - [STARTUP] 开始检查并初始化官方频道...
检查官方频道...
现有官方频道: {'公共酒馆', '作者酒馆', '读者茶馆', '官方实验室'}

✓ 所有官方频道都已存在，无需创建

现有官方频道列表:
  - 作者酒馆 (ID: c4a5fcd7-7fd1-4a18-8677-a15c052c7507)
  - 读者茶馆 (ID: 2e1b9d33-1400-4a40-802b-6d212d7a2fe5)
  - 公共酒馆 (ID: 3749ebb4-a2d6-4ab8-aa14-cf6c26611fc0)
  - 官方实验室 (ID: 452cfe84-3ac4-49e1-986b-260bcc3b8a6a)
2026-02-03 16:14:22,300 - app.main - INFO - [STARTUP] ✅ 官方频道检查完成
2026-02-03 16:14:22,300 - app.tasks.cleanup_humanize_details - INFO - 定时任务调度器已启动
2026-02-03 16:14:22,300 - app.services.channel_scheduler - INFO - Channel scheduler initialized
2026-02-03 16:14:22,306 - app.services.channel_scheduler - INFO - Channel scheduler started
2026-02-03 16:14:22,306 - app.main - INFO - [STARTUP] 开始预初始化同步Redis连接...
2026-02-03 16:14:22,306 - app.api.v1.agent - INFO - [Redis] 全局连接池已创建
2026-02-03 16:14:22,325 - app.main - INFO - [STARTUP] ✅ 同步Redis连接池预初始化完成
2026-02-03 16:14:22,326 - app.main - INFO - [STARTUP] 开始初始化AsyncRedisSaver索引...
2026-02-03 16:14:22,333 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ setup_checkpointer Redis连接验证成功
2026-02-03 16:14:22,348 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ AsyncRedisSaver索引预创建成功
2026-02-03 16:14:22,348 - app.main - INFO - [STARTUP] AsyncRedisSaver索引初始化完成
2026-02-03 16:14:22,348 - app.main - INFO - [STARTUP] 开始预加载Embedding模型...
2026-02-03 16:14:22,349 - app.services.vector_store_service - INFO - 🔄 预加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
2026-02-03 16:14:28,879 - app.services.vector_store_service - INFO - ✅ Embedding模型预加载成功，耗时: 6.53秒
2026-02-03 16:14:28,879 - app.main - INFO - [STARTUP] Embedding模型预加载完成
2026-02-03 16:14:28,879 - app.main - INFO - [STARTUP] P0性能优化已暂时禁用（诊断模式）
2026-02-03 16:14:28,879 - app.main - INFO - [STARTUP] 应用启动完成
INFO:     Application startup complete.
INFO:     ('127.0.0.1', 58800) - "WebSocket /api/v1/ws/notifications/79913e7e-d5cd-4e09-bce6-ca6639bd8456" [accepted]
2026-02-03 16:14:29,029 - app.api.v1.ws - INFO - [WebSocket] 通知连接建立: user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
INFO:     connection open
2026-02-03 16:14:35,571 - monitoring - INFO - Registered health check: cpu_usage
2026-02-03 16:14:35,572 - monitoring - INFO - Registered health check: memory_usage
2026-02-03 16:14:35,572 - monitoring - INFO - Registered health check: disk_usage
2026-02-03 16:14:35,572 - monitoring - INFO - Registered health check: process_status
2026-02-03 16:14:35,572 - monitoring - INFO - Added alert rule: high_cpu_usage
2026-02-03 16:14:35,572 - monitoring - INFO - Added alert rule: high_memory_usage
2026-02-03 16:14:35,572 - monitoring - INFO - Added alert rule: low_disk_space
INFO:     127.0.0.1:59025 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
INFO:     127.0.0.1:56402 - "GET /api/v1/agent/sessions/caac9658-6b2d-4049-b971-44de6ee18706/messages?order=asc&limit=200 HTTP/1.1" 200 OK
INFO:     127.0.0.1:63903 - "GET /api/v1/agent/sessions/caac9658-6b2d-4049-b971-44de6ee18706/messages?order=asc&limit=200 HTTP/1.1" 200 OK
INFO:     127.0.0.1:56047 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2026-02-03 16:14:50,084 - app.services.ai.prompts - INFO - Prompts loaded successfully from D:\Java\ai_writer\backend\app\services\ai\prompts\default.json
2026-02-03 16:14:50,084 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-02-03 16:14:50,084 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-02-03 16:14:50,084 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2026-02-03 16:14:51,637 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz:8443/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-02-03 16:14:51,639 - app.api.v1.agent - INFO - [Chat Stream] Mode: planning
2026-02-03 16:14:51,640 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:58695 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2026-02-03 16:14:51,651 - app.core.redis - INFO - ✅ Redis connected: redis://localhost:6379/0
2026-02-03 16:14:51,654 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 请用 explore_content 搜索“段融 读取器灵 牛尾刀”，输出证据，并在结果里给出 ar...
2026-02-03 16:14:51,654 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-02-03 16:14:51,656 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-02-03 16:14:51,656 - app.services.ai.http_ai_service - INFO - [成本追踪] 初始化未传db/user_id，将使用请求上下文按需记录成本
2026-02-03 16:14:52,880 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz:8443/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-02-03 16:14:52,880 - app.services.agent.tools.writing_tools - INFO - Writing tools AI service initialized
2026-02-03 16:14:52,880 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ AI Service 已同时设置到 langgraph_tools 和 writing_tools
2026-02-03 16:14:52,880 - app.services.context.adaptive_budget - INFO - ✅ 所有预算配置验证通过
2026-02-03 16:14:58,765 - app.services.context.vector_memory_store - INFO - ✅ VectorMemoryStore初始化成功 | 目录=./data/chroma_db | 模型=paraphrase-multilingual-MiniLM-L12-v2 | 集合=user_memories
2026-02-03 16:14:58,765 - app.services.context.manager - INFO - ✅ VectorMemoryStore 已初始化
2026-02-03 16:14:58,765 - app.services.context.manager - INFO - ✅ ContextManager: 长期记忆已启用 (user_id=None)
2026-02-03 16:14:58,765 - app.services.context.manager - INFO - ✅ ContextManager: 自适应预算已启用
2026-02-03 16:14:58,765 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ ContextManager已初始化（长期记忆已启用，自适应预算已启用，总预算=16000 tokens）
成功加载模板: analyze_text (版本 3.1.0)
成功加载模板: writing_agent (版本 2.0.0)
成功加载模板: system_agent_prompt (版本 2.1.0)
成功加载模板: creative_writing_prompt (版本 1.0.0)
2026-02-03 16:14:58,785 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ PromptManager已初始化
2026-02-03 16:14:58,799 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ Redis连接验证成功
2026-02-03 16:14:58,800 - app.services.agent.langgraph_agent - INFO - [LangGraph] OK 使用 AsyncRedisSaver（redis://localhost:6379/0，TTL=7天）
2026-02-03 16:14:58,801 - app.services.agent.memory.metrics - INFO - [MemoryMetrics] 监控系统已初始化
2026-02-03 16:14:58,801 - app.services.agent.memory.long_term_store - INFO - [LongTermStore] Initialized: base_dir=./data/long_term_memory, max_size=50KB, compression=True
2026-02-03 16:14:58,802 - app.services.agent.memory.enhanced_memory_manager - INFO - EnhancedMemoryManager initialized: short=10, medium=100, threshold=0.1, long_term_backup=enabled
2026-02-03 16:14:58,802 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ EnhancedMemoryManager已创建
2026-02-03 16:14:58,802 - app.services.agent.memory.unified_coordinator - INFO - [UnifiedMemoryCoordinator] 初始化统一记忆协调器
2026-02-03 16:14:58,802 - app.services.agent.memory.unified_coordinator - INFO - [UnifiedMemoryCoordinator] 全局实例已设置
2026-02-03 16:14:58,803 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ UnifiedMemoryCoordinator已初始化 | checkpointer=AsyncRedisSaver | enhanced_memory=yes | context_manager=yes
2026-02-03 16:14:58,803 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ 解耦模块已初始化 (IntentClassifier, ToolExecutor, EventParser, ResponseBuilder, ToolDispatcher, ParallelExecutor, PlanGenerator, QuickPathHandler, StreamEventHandler, SecondaryToolHandler, TaskRunner, AgentExecutor)
2026-02-03 16:14:58,812 - app.services.agent.parallel_tool_node - INFO - [ParallelToolNode] 初始化完成，最大并发数=5，并行安全工具=6个
2026-02-03 16:14:58,822 - app.api.v1.agent - INFO - [Global Agent] created global agent instance; MemorySaver shared across requests
2026-02-03 16:14:58,849 - app.api.v1.agent - INFO - [agent_chat_stream] 📚 世界观数据已注入: 人物=11, 地点=9, 设定=6, 规范=无
2026-02-03 16:14:58,849 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:73db1555-41d1-427a-bac1-2e2164c2a427:caac9658-6b2d-4049-b971-44de6ee18706 (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=73db1555-41d1-427a-bac1-2e2164c2a427, conversation_id=caac9658-6b2d-4049-b971-44de6ee18706)
2026-02-03 16:14:58,849 - app.services.context.monitoring_integration - INFO - ✅ ContextManager监控收集器已初始化
2026-02-03 16:14:58,851 - app.services.context.store - INFO - [ContextStore] Redis连接成功
2026-02-03 16:14:58,855 - app.services.context.manager - INFO - [ContextManager] 创建新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:73db1555-41d1-427a-bac1-2e2164c2a427:caac9658-6b2d-4049-b971-44de6ee18706
2026-02-03 16:14:59,014 - app.services.context.token_counter - INFO - ✅ tiktoken初始化成功，模型: gemini-2.5-pro -> cl100k_base
2026-02-03 16:14:59,016 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:73db1555-41d1-427a-bac1-2e2164c2a427:caac9658-6b2d-4049-b971-44de6ee18706: 0/16000 tokens
2026-02-03 16:14:59,613 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='请用 explore_content 搜索“段融 读取器灵 ...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:73db1555-41d1-427a-bac1-2e2164c2a427', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=3条
2026-02-03 16:14:59,615 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=73db1555-41d1-427a-bac1-2e2164c2a427 | 含用户级=True | 找到=3条
2026-02-03 16:14:59,647 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 1条消息, 0 tokens, 耗时 796.08ms
2026-02-03 16:14:59,647 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 1 条历史消息 (token: 0, has_summary: False)
2026-02-03 16:14:59,649 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-02-03 16:14:59,650 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-02-03 16:15:01,345 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-02-03 16:15:01,345 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-02-03 16:15:02,600 - app.services.agent.intent.classifier - INFO - [Intent] AI识别结果: general
2026-02-03 16:15:02,600 - app.services.agent.langgraph_agent - INFO - [Planning] AI意图分类: general (置信度: 0.90)
2026-02-03 16:15:02,600 - app.services.agent.langgraph_agent - INFO - [Planning] 识别为 general 意图，但仍走 LangGraph 流程（支持工具调用）
2026-02-03 16:15:02,600 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 请用 explore_content 搜索“段融 读取器灵 牛尾刀”，输出证据，并在结果里给出 ar...
2026-02-03 16:15:02,622 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-02-03 16:15:02,622 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=story_planning, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: story_planning; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-02-03 16:15:13,495 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=21341
2026-02-03 16:15:13,495 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户想要根据关键词“段融”、“读取器灵”、“牛尾刀”在作品中, 原料=需要调用工具在作品内容中进行搜索。统一使, 处理=使用 explore_content 工
2026-02-03 16:15:13,527 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共1个任务
2026-02-03 16:15:13,527 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共1个任务，耗时: 10.93s
2026-02-03 16:15:13,527 - app.api.v1.agent - INFO - [Stream] Plan tasks: 1 items
2026-02-03 16:15:13,527 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2026-02-03 16:15:13,527 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2026-02-03 16:15:13,527 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2026-02-03 16:15:13,527 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] DAG 调度启用，任务数=1, 有依赖任务=0
2026-02-03 16:15:13,527 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1开始: 使用 explore_content 搜索包含“段融”、“读取器灵”、“牛尾刀”的内容，并输出证据和 artifact_id。
2026-02-03 16:15:13,527 - app.api.v1.agent - INFO - [Stream] Task started: 使用 explore_content 搜索包含“段融”、“读取器灵”、“牛尾刀”的内容，并输出证据和 artifact_id。 (icon=Wrench)
2026-02-03 16:15:13,527 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: explore_content
2026-02-03 16:15:13,533 - app.services.agent.tools.explore_tools - INFO - [explore_content] 开始: work_id=73db1555-41d1-427a-bac1-2e2164c2a427, target=搜索与“段融”、“读取器灵”和“牛尾刀”相关的内容...
2026-02-03 16:15:13,533 - app.services.agent.tools.explore_tools - INFO - [explore_content] 规划传入关键词: ['段融', '读取器灵', '牛尾刀']
2026-02-03 16:15:13,547 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 开始探索 V5: work_id=73db1555-41d1-427a-bac1-2e2164c2a427, target=搜索与“段融”、“读取器灵”和“牛尾刀”相关的内容...
2026-02-03 16:15:13,548 - app.services.chapter_service - INFO - [ChapterService] Querying chapters for work_id=73db1555-41d1-427a-bac1-2e2164c2a427, type=<class 'uuid.UUID'>
2026-02-03 16:15:13,571 - app.services.chapter_service - INFO - [ChapterService] Found 5 chapters
2026-02-03 16:15:13,572 - app.services.chapter_service - INFO -   - Chapter: 第1章 吞噬, order=1
2026-02-03 16:15:13,572 - app.services.chapter_service - INFO -   - ... (3 more chapters)
2026-02-03 16:15:13,572 - app.services.chapter_service - INFO -   - Chapter: 第5章 太一门, order=5
2026-02-03 16:15:13,601 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 自动获取世界观...
2026-02-03 16:15:13,622 - app.services.agent.langgraph_tools - INFO - [get_writing_context] ✅ 获取创作上下文成功: include=worldview
2026-02-03 16:15:13,624 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 世界观获取完成: 26 条
2026-02-03 16:15:13,624 - app.services.ai.http_ai_service - INFO - [成本追踪] 初始化未传db/user_id，将使用请求上下文按需记录成本
2026-02-03 16:15:14,285 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz:8443/v1, Model: gemini-2.5-flash, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: False, CostTracking: True
2026-02-03 16:15:14,285 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-02-03 16:15:24,073 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 强制流程步骤: list_chapters
2026-02-03 16:15:24,073 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=list_chapters params={"work_id": "73db1555-41d1-427a-bac1-2e2164c2a427"}
2026-02-03 16:15:24,073 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=list_chapters success=True count=5
2026-02-03 16:15:29,560 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 强制流程步骤: list_paragraphs
2026-02-03 16:15:29,560 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=list_paragraphs params={"chapter_order": 1, "offset": 0, "limit": 50, "preview_len": 80, "work_id": "73db1555-41d1-427a-bac1-2e2164c2a427"}
2026-02-03 16:15:29,596 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=list_paragraphs success=True chapter=1 offset=0 limit=50 approximate=None
2026-02-03 16:15:37,718 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"keywords": ["段融", "读取器灵", "牛尾刀"], "match_mode": "keywords", "limit": 50, "chapter_order": 1, "work_id": "73db1555-41d1-427a-bac1-2e2164c2a427"}
2026-02-03 16:15:37,718 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 世界观匹配: 6 条
2026-02-03 16:15:37,779 - app.services.chapter_vector_service - INFO - [exact_search] work=73db1555-41d1-427a-bac1-2e2164c2a427, keywords=['段融', '读取器灵', '牛尾刀']..., mode=any, range=(1, 1), hits=50
2026-02-03 16:15:37,870 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=17 (chapter=17, worldview=6) keywords=段融,读取器灵,牛尾刀
2026-02-03 16:15:44,319 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 探索完成(工具循环): 3轮, 原因=已通过精确搜索找到并读取了所有与“段融”、“读取器灵”和“牛尾刀”相关的段落（共17条），所有命中段落均已收集为证据。目前已获取目标任务所需的所有关键信息，无需进一步搜索或读取。
2026-02-03 16:15:44,430 - app.services.agent.execution.tool_executor - INFO - [StandardTool] explore_content 执行成功
2026-02-03 16:15:44,431 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 目标章节已固化: 12d36da8-05bf-4cbf-ba1e-5044dcdf6c06 (source=explore.locate_targets)
2026-02-03 16:15:44,431 - app.api.v1.agent - INFO - [Stream] 任务完成: 使用 explore_content 搜索包含“段融”、“读取器灵”、“牛尾刀”的内容，并输出证据和 artifact_id。 (30.9s)
2026-02-03 16:15:44,431 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1完成
2026-02-03 16:15:44,432 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共1个任务，耗时: 30.90s
2026-02-03 16:15:44,432 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2026-02-03 16:15:44,432 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=1, 展示型=0
2026-02-03 16:15:44,432 - app.services.agent.langgraph_agent - INFO - [Response] 单个输出任务(explore_content)，使用AI整合
2026-02-03 16:15:44,432 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2026-02-03 16:15:44,432 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=1, 展示型=0
2026-02-03 16:15:44,432 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=1781字符, 处理后=1849字符
2026-02-03 16:15:44,432 - app.services.agent.planning.response_builder - INFO - [Summarization] 准备发送 summarization_start 事件
2026-02-03 16:15:44,433 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-02-03 16:15:44,433 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-02-03 16:15:45,761 - app.services.agent.planning.response_builder - INFO - [Summarization] reason生成: len=38 content=搜索“段融 读取器灵 牛尾刀”得到证据，并成功获取 artifact_id。
2026-02-03 16:15:45,761 - app.services.agent.stream.stream_event_handler - INFO - [StreamEventHandler] emit_summarization_start 被调用, _on_flow_event=True, reason_len=38, reason=搜索“段融 读取器灵 牛尾刀”得到证据，并成功获取 artifact_id。
2026-02-03 16:15:45,769 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_start 事件已发送
2026-02-03 16:15:45,769 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2026-02-03 16:15:45,770 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2026-02-03 16:15:45,776 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-02-03 16:15:45,776 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-02-03 16:15:48,606 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_complete 事件已发送（第一个chunk时）
2026-02-03 16:15:48,606 - app.services.agent.planning.response_builder - INFO - [Summarization] output_ready 事件已发送（第一个chunk时）
2026-02-03 16:15:52,025 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=1352
2026-02-03 16:15:52,693 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:73db1555-41d1-427a-bac1-2e2164c2a427 | 重要度=0.73
2026-02-03 16:15:52,701 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:73db1555-41d1-427a-bac1-2e2164c2a427:caac9658-6b2d-4049-b971-44de6ee18706, token=1468
2026-02-03 16:15:52,702 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:73db1555-41d1-427a-bac1-2e2164c2a427:caac9658-6b2d-4049-b971-44de6ee18706, 消息数=2, 摘要长度=0, Token=1468
2026-02-03 16:15:52,702 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:73db1555-41d1-427a-bac1-2e2164c2a427:caac9658-6b2d-4049-b971-44de6ee18706)
2026-02-03 16:15:52,704 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2026-02-03 16:15:52,936 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed
INFO:     127.0.0.1:64624 - "GET /api/v1/agent/operations/caac9658-6b2d-4049-b971-44de6ee18706 HTTP/1.1" 200 OK
2026-02-03 16:16:30,850 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-02-03 16:16:30,850 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-02-03 16:16:30,851 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2026-02-03 16:16:32,327 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz:8443/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-02-03 16:16:32,329 - app.api.v1.agent - INFO - [Chat Stream] Mode: planning
2026-02-03 16:16:32,330 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:54203 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2026-02-03 16:16:32,347 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 使用 load_explore_artifact 读取刚才的 artifact_id，mode=su...
2026-02-03 16:16:32,357 - app.api.v1.agent - INFO - [agent_chat_stream] 📚 世界观数据已注入: 人物=11, 地点=9, 设定=6, 规范=无
2026-02-03 16:16:32,358 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:73db1555-41d1-427a-bac1-2e2164c2a427:caac9658-6b2d-4049-b971-44de6ee18706 (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=73db1555-41d1-427a-bac1-2e2164c2a427, conversation_id=caac9658-6b2d-4049-b971-44de6ee18706)
2026-02-03 16:16:32,366 - app.services.context.store - INFO - [ContextStore] 加载上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:73db1555-41d1-427a-bac1-2e2164c2a427:caac9658-6b2d-4049-b971-44de6ee18706, 2条消息
2026-02-03 16:16:32,369 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:73db1555-41d1-427a-bac1-2e2164c2a427:caac9658-6b2d-4049-b971-44de6ee18706: 1468/16000 tokens
2026-02-03 16:16:32,456 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='使用 load_explore_artifact 读取刚才的...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:73db1555-41d1-427a-bac1-2e2164c2a427', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=3条
2026-02-03 16:16:32,456 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=73db1555-41d1-427a-bac1-2e2164c2a427 | 含用户级=True | 找到=3条
2026-02-03 16:16:32,469 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 3条消息, 1468 tokens, 耗时 110.07ms
2026-02-03 16:16:32,475 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 3 条历史消息 (token: 1468, has_summary: False)
2026-02-03 16:16:32,480 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-02-03 16:16:32,480 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-02-03 16:16:33,938 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-02-03 16:16:33,944 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-02-03 16:16:35,156 - app.services.agent.intent.classifier - INFO - [Intent] AI识别结果: general
2026-02-03 16:16:35,159 - app.services.agent.langgraph_agent - INFO - [Planning] AI意图分类: general (置信度: 0.90)
2026-02-03 16:16:35,159 - app.services.agent.langgraph_agent - INFO - [Planning] 识别为 general 意图，但仍走 LangGraph 流程（支持工具调用）
2026-02-03 16:16:35,159 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 使用 load_explore_artifact 读取刚才的 artifact_id，mode=su...
2026-02-03 16:16:35,172 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-02-03 16:16:35,172 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=story_planning, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: story_planning; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-02-03 16:16:43,144 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=22998
2026-02-03 16:16:43,146 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户想要读取之前探索任务的结果摘要。, 原料=需要的原料是之前任务返回的 `artif, 处理=直接调用 `load_explore_a
2026-02-03 16:16:43,146 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共1个任务
2026-02-03 16:16:43,146 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共1个任务，耗时: 7.99s
2026-02-03 16:16:43,146 - app.api.v1.agent - INFO - [Stream] Plan tasks: 1 items
2026-02-03 16:16:43,146 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2026-02-03 16:16:43,146 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2026-02-03 16:16:43,146 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2026-02-03 16:16:43,146 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] DAG 调度启用，任务数=1, 有依赖任务=0
2026-02-03 16:16:43,146 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1开始: 使用 load_explore_artifact 读取 artifact_id: 50fe756714434d5dbabee3b6eafcbd57 的摘要信息。
2026-02-03 16:16:43,146 - app.api.v1.agent - INFO - [Stream] Task started: 使用 load_explore_artifact 读取 artifact_id: 50fe756714434d5dbabee3b6eafcbd57 的摘要信息。 (icon=Wrench)
2026-02-03 16:16:43,146 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: load_explore_artifact
2026-02-03 16:16:43,201 - app.services.agent.execution.tool_executor - INFO - [StandardTool] load_explore_artifact 执行成功
2026-02-03 16:16:43,206 - app.api.v1.agent - INFO - [Stream] 任务完成: 使用 load_explore_artifact 读取 artifact_id: 50fe756714434d5dbabee3b6eafcbd57 的摘要信息。 (0.1s)
2026-02-03 16:16:43,206 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1完成
2026-02-03 16:16:43,206 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共1个任务，耗时: 0.06s
2026-02-03 16:16:43,206 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2026-02-03 16:16:43,206 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=1, 展示型=0
2026-02-03 16:16:43,206 - app.services.agent.langgraph_agent - INFO - [Response] 单个输出任务(load_explore_artifact)，使用AI整合
2026-02-03 16:16:43,211 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2026-02-03 16:16:43,211 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=1, 展示型=0
2026-02-03 16:16:43,211 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=74字符, 处理后=159字符
2026-02-03 16:16:43,212 - app.services.agent.planning.response_builder - INFO - [Summarization] 准备发送 summarization_start 事件
2026-02-03 16:16:43,213 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-02-03 16:16:43,214 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-02-03 16:16:44,265 - app.services.agent.planning.response_builder - INFO - [Summarization] reason生成: len=57 content=成功读取 artifact_id: 50fe756714434d5dbabee3b6eafcbd57 的摘要信息。
2026-02-03 16:16:44,265 - app.services.agent.stream.stream_event_handler - INFO - [StreamEventHandler] emit_summarization_start 被调用, _on_flow_event=True, reason_len=57, reason=成功读取 artifact_id: 50fe756714434d5dbabee3b6eafcbd57 的摘要信息。
2026-02-03 16:16:44,265 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_start 事件已发送
2026-02-03 16:16:44,265 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2026-02-03 16:16:44,265 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2026-02-03 16:16:44,275 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-02-03 16:16:44,276 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-02-03 16:16:48,479 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_complete 事件已发送（第一个chunk时）
2026-02-03 16:16:48,479 - app.services.agent.planning.response_builder - INFO - [Summarization] output_ready 事件已发送（第一个chunk时）
2026-02-03 16:16:48,780 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=130
2026-02-03 16:16:48,789 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:73db1555-41d1-427a-bac1-2e2164c2a427:caac9658-6b2d-4049-b971-44de6ee18706, token=1559
2026-02-03 16:16:48,793 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:73db1555-41d1-427a-bac1-2e2164c2a427:caac9658-6b2d-4049-b971-44de6ee18706, 消息数=4, 摘要长度=0, Token=1559
2026-02-03 16:16:48,793 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:73db1555-41d1-427a-bac1-2e2164c2a427:caac9658-6b2d-4049-b971-44de6ee18706)
2026-02-03 16:16:48,794 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2026-02-03 16:16:49,108 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed
INFO:     127.0.0.1:62159 - "GET /api/v1/agent/operations/caac9658-6b2d-4049-b971-44de6ee18706 HTTP/1.1" 200 OK
