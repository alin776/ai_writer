15:20:33 app.api.v1.auth INFO   [LOGIN] 尝试登录: 2072855200@qq.com
15:20:33 app.api.v1.auth INFO   [LOGIN] 会话创建成功: 602f5147-846a-4cde-95d3-405fa75f133f (127.0.0.1)
15:20:33 app.api.v1.auth INFO   [LOGIN] 登录成功: testuser_new-1 (602f5147-846a-4cde-95d3-405fa75f133f) from 127.0.0.1
15:20:33 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/auth/login
INFO:     127.0.0.1:57059 - "POST /api/v1/auth/login HTTP/1.1" 200 OK
15:20:33 app.api.middleware.monitoring_middleware INFO   API请求完成: OPTIONS /api/v1/users/me
INFO:     127.0.0.1:57059 - "OPTIONS /api/v1/users/me HTTP/1.1" 200 OK
15:20:34 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/users/me
INFO:     127.0.0.1:57059 - "GET /api/v1/users/me HTTP/1.1" 200 OK
15:20:34 app.api.middleware.monitoring_middleware INFO   API请求完成: OPTIONS /api/v1/works
15:20:34 app.api.middleware.monitoring_middleware INFO   API请求完成: OPTIONS /api/v1/works
INFO:     127.0.0.1:57059 - "OPTIONS /api/v1/works HTTP/1.1" 200 OK
INFO:     127.0.0.1:60607 - "OPTIONS /api/v1/works HTTP/1.1" 200 OK
15:20:34 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works
INFO:     127.0.0.1:57059 - "GET /api/v1/works HTTP/1.1" 200 OK
15:20:34 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works
INFO:     127.0.0.1:57059 - "GET /api/v1/works HTTP/1.1" 200 OK
15:20:38 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works/ad948837-e94e-4d0f-92a4-a75cf1301b07
INFO:     127.0.0.1:57059 - "GET /api/v1/works/ad948837-e94e-4d0f-92a4-a75cf1301b07 HTTP/1.1" 200 OK
15:20:38 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/characters
INFO:     127.0.0.1:57059 - "GET /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/characters HTTP/1.1" 200 OK
15:20:38 app.api.v1.chapters INFO   [GET chapters] work_id=ad948837-e94e-4d0f-92a4-a75cf1301b07, user_id=602f5147-846a-4cde-95d3-405fa75f133f
15:20:38 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/locations
INFO:     127.0.0.1:57059 - "GET /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/locations HTTP/1.1" 200 OK
15:20:38 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/settings
INFO:     127.0.0.1:57059 - "GET /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/settings HTTP/1.1" 200 OK
15:20:38 app.services.chapter_service INFO   [ChapterService] Querying chapters for work_id=ad948837-e94e-4d0f-92a4-a75cf1301b07, type=<class 'uuid.UUID'>
15:20:38 app.services.chapter_service INFO   [ChapterService] Found 3 chapters
15:20:38 app.services.chapter_service INFO     - Chapter: 钢铁坟场, order=1
15:20:38 app.services.chapter_service INFO     - Chapter: 归巢与低语, order=2
15:20:38 app.services.chapter_service INFO     - Chapter: 遗落的星图, order=3
15:20:38 app.api.v1.chapters INFO   [GET chapters] Returning 3 chapters
15:20:38 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/guidelines
INFO:     127.0.0.1:57059 - "GET /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/guidelines HTTP/1.1" 200 OK
15:20:38 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/chapters/work/ad948837-e94e-4d0f-92a4-a75cf1301b07
INFO:     127.0.0.1:60607 - "GET /api/v1/chapters/work/ad948837-e94e-4d0f-92a4-a75cf1301b07 HTTP/1.1" 200 OK
15:20:38 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works/ad948837-e94e-4d0f-92a4-a75cf1301b07
INFO:     127.0.0.1:60607 - "GET /api/v1/works/ad948837-e94e-4d0f-92a4-a75cf1301b07 HTTP/1.1" 200 OK
15:20:38 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/ai-guidelines
INFO:     127.0.0.1:57059 - "GET /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/ai-guidelines HTTP/1.1" 200 OK
15:20:38 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/characters
15:20:38 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/locations
INFO:     127.0.0.1:60607 - "GET /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/characters HTTP/1.1" 200 OK
INFO:     127.0.0.1:57059 - "GET /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/locations HTTP/1.1" 200 OK
15:20:38 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/guidelines
INFO:     127.0.0.1:57059 - "GET /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/guidelines HTTP/1.1" 200 OK
15:20:38 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/settings
INFO:     127.0.0.1:60607 - "GET /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/settings HTTP/1.1" 200 OK
15:20:38 app.api.v1.chapters INFO   [GET chapters] work_id=ad948837-e94e-4d0f-92a4-a75cf1301b07, user_id=602f5147-846a-4cde-95d3-405fa75f133f
15:20:38 app.services.chapter_service INFO   [ChapterService] Querying chapters for work_id=ad948837-e94e-4d0f-92a4-a75cf1301b07, type=<class 'uuid.UUID'>
15:20:38 app.services.chapter_service INFO   [ChapterService] Found 3 chapters
15:20:38 app.services.chapter_service INFO     - Chapter: 钢铁坟场, order=1
15:20:38 app.services.chapter_service INFO     - Chapter: 归巢与低语, order=2
15:20:38 app.services.chapter_service INFO     - Chapter: 遗落的星图, order=3
15:20:38 app.api.v1.chapters INFO   [GET chapters] Returning 3 chapters
15:20:38 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/chapters/work/ad948837-e94e-4d0f-92a4-a75cf1301b07
INFO:     127.0.0.1:57059 - "GET /api/v1/chapters/work/ad948837-e94e-4d0f-92a4-a75cf1301b07 HTTP/1.1" 200 OK
15:20:38 app.api.middleware.monitoring_middleware INFO   API请求完成: OPTIONS /api/v1/analysis/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/status
INFO:     127.0.0.1:57059 - "OPTIONS /api/v1/analysis/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/status HTTP/1.1" 200 OK
15:20:38 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/ai-guidelines
INFO:     127.0.0.1:60607 - "GET /api/v1/worldview/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/ai-guidelines HTTP/1.1" 200 OK
15:20:38 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/analysis/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/status
INFO:     127.0.0.1:57059 - "GET /api/v1/analysis/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/status HTTP/1.1" 200 OK
15:20:38 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/analysis/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/status
INFO:     127.0.0.1:57059 - "GET /api/v1/analysis/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/status HTTP/1.1" 200 OK
15:20:38 app.api.middleware.monitoring_middleware INFO   API请求完成: OPTIONS /api/v1/chapters/ef5eb68c-32b8-4249-83a3-31d57363c0a9
15:20:38 app.api.middleware.monitoring_middleware INFO   API请求完成: OPTIONS /api/v1/chapters/ef5eb68c-32b8-4249-83a3-31d57363c0a9
INFO:     127.0.0.1:57059 - "OPTIONS /api/v1/chapters/ef5eb68c-32b8-4249-83a3-31d57363c0a9 HTTP/1.1" 200 OK
INFO:     127.0.0.1:60607 - "OPTIONS /api/v1/chapters/ef5eb68c-32b8-4249-83a3-31d57363c0a9 HTTP/1.1" 200 OK
15:20:38 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/ef5eb68c-32b8-4249-83a3-31d57363c0a9
15:20:38 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/ef5eb68c-32b8-4249-83a3-31d57363c0a9
INFO:     127.0.0.1:57059 - "PUT /api/v1/chapters/ef5eb68c-32b8-4249-83a3-31d57363c0a9 HTTP/1.1" 200 OK
INFO:     127.0.0.1:62893 - "PUT /api/v1/chapters/ef5eb68c-32b8-4249-83a3-31d57363c0a9 HTTP/1.1" 200 OK
15:21:11 app.api.middleware.monitoring_middleware INFO   API请求完成: OPTIONS /api/v1/agent/chat/stream
INFO:     127.0.0.1:49286 - "OPTIONS /api/v1/agent/chat/stream HTTP/1.1" 200 OK
15:21:11 app.services.ai.prompts INFO   Prompts loaded successfully from D:\Java\ai_writer\backend\app\services\ai\prompts\default.json
15:21:11 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
15:21:11 app.services.ai.http_ai_service INFO   ModelSelector 已启用
15:21:11 app.services.agent.cost_tracker INFO   CostTracker 初始化完成, 持久化: False
15:21:11 app.services.ai.http_ai_service INFO   CostTracker 已启用
15:21:12 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
15:21:12 app.api.v1.agent INFO   [Chat Stream] Mode: react
15:21:12 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:61132 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
15:21:33 app.core.redis INFO   ✅ Redis connected: redis://localhost:6379/0
15:21:33 app.api.v1.agent INFO   [Session] 创建新会话归属: 6515ce20-3116-4f79-bed5-e1804c0365f3 -> 602f5147-846a-4cde-95d3-405fa75f133f
15:21:33 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: react, Message: 前面三章核心讲了什么内容...
15:21:33 app.services.agent.memory.long_term_memory INFO   [LTM] 从作品 ad948837-e94e-4d0f-92a4-a75cf1301b07 检索到 0 条对话ID
15:21:33 app.services.agent.memory.long_term_memory INFO   [LTM] 最终返回 0 条对话摘要 (work_id=ad948837-e94e-4d0f-92a4-a75cf1301b07)
15:21:33 app.services.agent.memory.long_term_memory INFO   [LTM] 从作品 ad948837-e94e-4d0f-92a4-a75cf1301b07 检索到 0 条对话ID
15:21:33 app.services.agent.memory.long_term_memory INFO   [LTM] 最终返回 0 条对话摘要 (work_id=ad948837-e94e-4d0f-92a4-a75cf1301b07)
15:21:33 app.services.agent.memory.long_term_memory INFO   [LTM] 从作品 ad948837-e94e-4d0f-92a4-a75cf1301b07 检索到 0 条对话ID
15:21:33 app.services.agent.memory.long_term_memory INFO   [LTM] 最终返回 0 条对话摘要 (work_id=ad948837-e94e-4d0f-92a4-a75cf1301b07)
15:21:33 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
15:21:33 app.services.ai.http_ai_service INFO   ModelSelector 已启用
15:21:33 app.services.ai.http_ai_service INFO   CostTracker 已启用
15:21:35 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
15:21:35 chromadb.telemetry.product.posthog INFO   Anonymized telemetry enabled. See                     https://docs.trychroma.com/telemetry for more information.
15:21:35 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
15:21:42 app.services.context.vector_memory_store INFO   ✅ VectorMemoryStore初始化成功 | 目录=./data/chroma_db | 模型=paraphrase-multilingual-MiniLM-L12-v2 | 集合=user_memories
15:21:42 app.services.context.manager INFO   ✅ VectorMemoryStore 已初始化
15:21:42 app.services.context.manager INFO   ✅ ContextManager: 长期记忆已启用 (user_id=None)
15:21:42 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ ContextManager已初始化（长期记忆已启用）
成功加载模板: intent_classifier (版本 2.0.0)
成功加载模板: writing_agent (版本 2.0.0)
成功加载模板: planning_agent (版本 2.0.0)
成功加载模板: tool_agent (版本 2.0.0)
成功加载模板: query_agent (版本 2.0.0)
15:21:43 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ PromptManager已初始化
15:21:43 app.services.agent.langgraph_agent INFO   [LangGraph] 使用 ChatOpenAI 模式（原生工具调用）
15:21:46 app.api.callbacks.monitoring_callback INFO   [MonitoringCallback] 已初始化
15:21:46 app.services.agent.langgraph_agent INFO   [LangGraph] 已创建MonitoringCallbackHandler
15:22:08 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ Redis连接验证成功
15:22:08 app.services.agent.langgraph_agent INFO   [LangGraph] OK 使用 AsyncRedisSaver（redis://localhost:6379/0，TTL=7天）
15:22:08 app.services.agent.parallel_tool_node INFO   [ParallelToolNode] 初始化完成，最大并发数=5，并行安全工具=4个
15:22:08 app.api.v1.agent INFO   [Global Agent] 创建全局Agent实例，MemorySaver将在请求间共享
15:22:08 app.services.agent.langgraph_agent INFO   [LangGraph Stream] 开始流式执行: 前面三章核心讲了什么内容...
15:22:29 redisvl.index.index INFO   Index already exists, not overwriting.
15:22:29 redisvl.index.index INFO   Index already exists, not overwriting.
15:22:29 redisvl.index.index INFO   Index already exists, not overwriting.
15:22:29 langgraph.checkpoint.redis.aio INFO   Redis client is a standalone client
15:22:29 app.services.agent.langgraph_agent INFO   [LangGraph] AsyncRedisSaver索引创建成功
15:22:29 app.services.agent.langgraph_agent INFO   [Context] 设置用户ID: 602f5147-846a-4cde-95d3-405fa75f133f
15:22:29 app.services.context.monitoring_integration INFO   ✅ ContextManager监控收集器已初始化
15:22:29 app.services.context.store INFO   [ContextStore] Redis连接成功
15:22:50 app.services.context.manager INFO   [ContextManager] 创建新上下文: 6515ce20-3116-4f79-bed5-e1804c0365f3
15:22:50 app.services.context.token_counter INFO   ✅ tiktoken初始化成功，模型: gpt-4
15:22:50 app.services.context.manager INFO   [ContextManager] Session 6515ce20-3116-4f79-bed5-e1804c0365f3: 599/8000 tokens
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  3.75it/s]
15:22:51 app.services.context.vector_memory_store INFO   🔍 检索记忆 | 查询='前面三章核心讲了什么内容...' | 用户=602f5147-846a-4cde-95d3-405fa75f133f | work_id=ad948837-e94e-4d0f-92a4-a75cf1301b07 | 找到=3条 | 阈值=0.3
15:22:51 app.services.context.manager INFO   🔍 检索长期记忆 | work_id=ad948837-e94e-4d0f-92a4-a75cf1301b07 | 查询='前面三章核心讲了什么内容...' | 找到=3条 | 阈值=0.3
15:22:51 app.services.context.monitoring_integration INFO   [Monitor] 上下文构建: 2条消息, 599 tokens, 耗时 22069.58ms
15:22:51 app.services.agent.langgraph_agent INFO   [Context] 加载上下文: {'session_id': '6515ce20-3116-4f79-bed5-e1804c0365f3', 'token_count': 599, 'short_memory_size': 0, 'has_summary': False, 'compression_triggered': False, 'long_term_memories': 3, 'adaptive_budget_enabled': False, 'task_type': None}
15:22:51 app.services.agent.langgraph_agent INFO   [LangGraph] 使用隔离的thread_id: ad948837-e94e-4d0f-92a4-a75cf1301b07:6515ce20-3116-4f79-bed5-e1804c0365f3 (work_id=ad948837-e94e-4d0f-92a4-a75cf1301b07, conversation_id=6515ce20-3116-4f79-bed5-e1804c0365f3)
15:22:51 app.services.agent.progress_tracker INFO   [ProgressTracker] 初始化完成，使用动态节点追踪模式（根据实际执行的节点自动计算进度）
15:22:51 app.services.agent.langgraph_agent INFO   [ProgressTracker] 初始化完成，使用动态节点追踪模式
15:22:51 app.services.agent.langgraph_agent INFO   [LangGraph] 意图分类（规则识别）
15:22:51 app.services.agent.langgraph_agent INFO   [Intent] 规则识别结果: writing, 置信度: 0.90
15:22:51 app.services.agent.langgraph_agent INFO   [LangGraph] 路由到: writing
15:22:51 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: _route_intent
15:22:51 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: intent_classifier
15:22:51 app.services.agent.langgraph_agent INFO   [Stream Event] progress_event = {'type': 'progress', 'step': 'intent_analysis', 'description': '识别为：写作任务', 'node': 'intent_classifier', 'details': {'intent': 'writing'}, 'timestamp': '2025-11-12T15:22:51.368273', 'progress': 100.0, 'eta': 0, 'eta_display': '即将完成', 'eta_confidence': 'high', 'current_step': 3, 'total_steps': 3, 'step_description': '第 3/3 步', 'elapsed': 0.0}
15:22:51 app.services.agent.langgraph_agent INFO   [Stream Event] on_progress 回调已调用
15:22:51 app.api.v1.agent INFO   [SSE] 发送 progress 事件: step=intent_analysis, desc=识别为：写作任务
15:22:51 app.services.agent.actions.action_registry INFO   [ActionRegistry] 注册Action: echo (class=EchoAction, category=example)
15:22:51 app.services.agent.actions.action_registry INFO   [ActionRegistry] 注册Action: writing (class=WritingAction, category=content_creation)
15:22:51 app.services.agent.actions.action_registry INFO   [ActionRegistry] 注册Action: planning (class=PlanningAction, category=planning)
15:22:51 app.services.agent.actions.action_registry INFO   [ActionRegistry] 注册Action: analysis (class=AnalysisAction, category=analysis)
15:22:51 app.services.agent.actions.action_registry INFO   [ActionRegistry] 注册Action: stuck (class=StuckAction, category=writing_assistance)
15:22:51 app.services.agent.actions.action_registry INFO   [ActionRegistry] 注册Action: general_chat (class=GeneralChatAction, category=conversation)
15:22:51 app.services.agent.langgraph_agent INFO   [LangGraph] 处理写作请求（新架构）
15:22:51 Action.writing INFO   [writing] PromptManager已初始化
15:22:51 Action.writing INFO   [writing] work_id=ad948837-e94e-4d0f-92a4-a75cf1301b07, chapter_id=ef5eb68c-32b8-4249-83a3-31d57363c0a9, phase=None, chapter_num=None
15:22:51 app.services.agent.langgraph_agent INFO   [LangGraph] WritingAction准备完成: phase=None, chapter_num=None
15:22:51 app.services.agent.langgraph_agent INFO   [LangGraph] 处理writing场景 (use_chatgpt=True)
15:22:55 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
15:22:57 app.api.callbacks.monitoring_callback INFO   [MonitoringCallback] LLM调用成功: run_id=0fde948f-820f-4a30-9e0f-d4a0169db52b, model=unknown, duration=5.62s, tokens=N/A
15:22:57 app.services.agent.langgraph_agent INFO   [LangGraph] 检测到工具调用: 3 个工具
15:22:57 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: _should_continue
15:22:57 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: writing_agent
15:22:57 app.services.agent.langgraph_agent INFO   [Stream Event] progress_event = {'type': 'progress', 'step': 'thinking', 'description': '正在思考如何帮助您...', 'node': 'writing_agent', 'details': {}, 'timestamp': '2025-11-12T15:22:57.024136', 'progress': 100.0, 'eta': 0, 'eta_display': '即将完成', 'eta_confidence': 'high', 'current_step': 5, 'total_steps': 5, 'step_description': '第 5/5 步', 'elapsed': 5.7}
15:22:57 app.api.v1.agent INFO   [Stream] Activity完成: intent_analysis (5.7s)
15:22:57 app.services.agent.langgraph_agent INFO   [Stream Event] on_progress 回调已调用
15:22:57 app.api.v1.agent INFO   [SSE] 发送 activity_complete 事件: step=intent_analysis, elapsed=5.7s
15:22:57 app.api.v1.agent INFO   [SSE] 发送 progress 事件: step=thinking, desc=正在思考如何帮助您...
15:22:57 app.services.agent.parallel_tool_node INFO   [ParallelToolNode] 工具分组: 并行=3, 串行=0
15:22:57 app.services.agent.parallel_tool_node INFO   [ParallelToolNode] 开始并行执行3个工具
15:22:57 app.services.agent.parallel_tool_node INFO   [ParallelToolNode] 并行执行完成，成功=3，失败=0
15:22:57 app.services.agent.langgraph_agent INFO   [LangGraph] 工具执行完毕，路由回: writing_agent
15:22:57 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: _route_after_tools
15:22:57 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: tools
15:22:57 app.services.agent.langgraph_agent WARNING   [Tools Node] 未找到AIMessage的tool_calls，尝试从ToolMessage提取
15:22:57 app.services.agent.langgraph_agent INFO   [Tools Node] 使用缓存参数: get_chapter_by_order_tool -> {'chapter_order': 3}
15:22:57 app.services.agent.langgraph_agent INFO   [Tools Node] 最终使用: tool_name=get_chapter_by_order_tool, tool_args={'chapter_order': 3}
15:22:57 app.services.agent.langgraph_agent INFO   [Stream Event] progress_event = {'type': 'progress', 'step': 'tool_execution', 'description': '📚 正在读取第3章...', 'node': 'tools', 'details': {'tools': ['get_chapter_by_order_tool'], 'tool_args': {'chapter_order': 3}}, 'timestamp': '2025-11-12T15:22:57.046521', 'progress': 100.0, 'eta': 0, 'eta_display': '即将完成', 'eta_confidence': 'high', 'current_step': 7, 'total_steps': 7, 'step_description': '第 7/7 步', 'elapsed': 5.7}
15:22:57 app.api.v1.agent INFO   [Stream] Activity完成: thinking (0.0s)
15:22:57 app.services.agent.langgraph_agent INFO   [Stream Event] on_progress 回调已调用
15:22:57 app.api.v1.agent INFO   [SSE] 发送 activity_complete 事件: step=thinking, elapsed=0.0s
15:22:57 app.api.v1.agent INFO   [SSE] 发送 progress 事件: step=tool_execution, desc=📚 正在读取第3章...
15:22:57 app.services.agent.langgraph_agent INFO   [LangGraph] 处理写作请求（新架构）
15:22:57 Action.writing INFO   [writing] PromptManager已初始化
15:22:57 Action.writing INFO   [writing] 从消息中识别到章节号: 3
15:22:57 Action.writing INFO   [writing] 章节 3 属于阶段: opening
15:22:57 Action.writing INFO   [writing] work_id=ad948837-e94e-4d0f-92a4-a75cf1301b07, chapter_id=ef5eb68c-32b8-4249-83a3-31d57363c0a9, phase=opening, chapter_num=3
15:22:57 app.services.agent.langgraph_agent INFO   [LangGraph] WritingAction准备完成: phase=opening, chapter_num=3
15:22:57 app.services.agent.langgraph_agent INFO   [LangGraph] 处理writing场景 (use_chatgpt=True)
15:22:57 app.services.agent.langgraph_agent INFO   [LangGraph] writing - 处理工具执行结果 (ChatOpenAI)
15:23:04 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
15:23:23 app.api.callbacks.monitoring_callback INFO   [MonitoringCallback] LLM调用成功: run_id=53c450f9-9f50-48e1-8314-d5c763746b58, model=unknown, duration=26.05s, tokens=N/A
15:23:23 app.services.agent.langgraph_agent INFO   [LangGraph] 无需工具调用，结束流程
15:23:23 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: _should_continue
15:23:23 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: writing_agent
15:23:23 app.services.agent.langgraph_agent INFO   [Stream Event] progress_event = {'type': 'progress', 'step': 'thinking', 'description': '正在思考如何帮助您...', 'node': 'writing_agent', 'details': {}, 'timestamp': '2025-11-12T15:23:23.108374', 'progress': 100.0, 'eta': 0, 'eta_display': '即将完成', 'eta_confidence': 'high', 'current_step': 7, 'total_steps': 7, 'step_description': '第 7/7 步', 'elapsed': 31.8}
15:23:23 app.api.v1.agent INFO   [Stream] Activity完成: tool_execution (26.1s)
15:23:23 app.services.agent.langgraph_agent INFO   [Stream Event] on_progress 回调已调用
15:23:23 app.api.v1.agent INFO   [SSE] 发送 activity_complete 事件: step=tool_execution, elapsed=26.1s
15:23:23 app.api.v1.agent INFO   [SSE] 发送 progress 事件: step=thinking, desc=正在思考如何帮助您...
15:23:23 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: LangGraph
15:23:23 app.services.agent.langgraph_agent INFO   [LangGraph Stream] 流式执行完成，共134个事件
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  5.72it/s]
15:23:23 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | work_id=ad948837-e94e-4d0f-92a4-a75cf1301b07 | 重要度=0.90 | 长度=1440
15:23:23 app.services.context.store INFO   [ContextStore] 保存上下文: 6515ce20-3116-4f79-bed5-e1804c0365f3, token=2149
15:23:23 app.services.context.manager INFO   [ContextManager] 更新上下文: 6515ce20-3116-4f79-bed5-e1804c0365f3, 消息数=2, Token=2149
15:23:23 app.services.agent.langgraph_agent INFO   [Context] 上下文已更新: 6515ce20-3116-4f79-bed5-e1804c0365f3 (work_id=ad948837-e94e-4d0f-92a4-a75cf1301b07)
15:23:23 app.services.agent.progress_tracker INFO   [ProgressTracker] 状态已重置
15:23:23 app.api.v1.agent INFO   [Stream] 最后活动完成: thinking (0.5s)
15:23:23 app.api.v1.agent INFO   [SSE] 发送 activity_complete 事件: step=thinking, elapsed=0.5s
15:23:23 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: react, Stream completed
15:27:38 app.api.middleware.monitoring_middleware INFO   API请求完成: OPTIONS /api/v1/ai/complete
INFO:     127.0.0.1:53906 - "OPTIONS /api/v1/ai/complete HTTP/1.1" 200 OK
15:27:38 app.api.v1.ai INFO   [AI续写] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), 上下文长度: 197, 风格: 默认
15:27:38 app.api.v1.ai INFO   [AI续写] context内容: '器，也是他的工具。 今天的收获……少得可怜。背包里只有几根没用的电缆和一块还算完整的电路板，这些东西带回“聚落”，最多只能换半块干巴巴的能量棒。 空手而归，就意味着更少的配给，更强烈的饥饿。在聚落里，没有价值的人，就会被无情地淘汰。 凌风深吸一口气，压下心中的焦躁，目光如鹰隼般再次扫视着周围。他像一只灵巧的猫，无声无息地从掩体后窜出，踩着一根悬空的钢梁，轻松地跃到对面一处还算完整的楼层平台。'
15:27:38 app.api.v1.ai INFO   [AI续写] prompt: '续写', max_tokens: 100
15:27:38 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
15:27:38 app.services.ai.http_ai_service INFO   ModelSelector 已启用
15:27:38 app.services.ai.http_ai_service INFO   CostTracker 已启用
15:27:39 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
15:27:39 app.services.ai.http_ai_service INFO   AI自动补全请求 - 上下文长度: 197
15:27:39 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=100, temp=0.7, task_type=None
15:27:39 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/complete
INFO:     127.0.0.1:53906 - "POST /api/v1/ai/complete HTTP/1.1" 200 OK
15:27:43 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/2 200 OK"
15:27:43 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
15:28:00 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 36
15:28:00 app.services.ai.http_ai_service INFO   流式响应Token统计: 1981 (prompt=1957, completion=24)
15:28:00 app.services.agent.cost_tracker INFO   [CostTracker] 记录API调用: gemini-2.5-pro, tokens: 1957+24=1981, cost: $0.000062
15:28:00 app.services.ai.http_ai_service INFO   [CostTracker] API调用已记录: tokens=1957+24, cost=$0.000062, time=20.71s
15:28:00 app.services.ai.ai_log_middleware INFO   AI调用日志已记录: operation=continue, tokens=142, cost=$0.000260, duration=20706ms, success=True
15:28:00 app.api.v1.ai INFO   [AI续写] 用户 testuser_new-1 请求完成，生成字数: 36
15:28:10 app.api.v1.ai INFO   [AI续写] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), 上下文长度: 194, 风格: 默认
15:28:10 app.api.v1.ai INFO   [AI续写] context内容: '镌刻着一些他从未见过的、仿佛由无数精密几何线条构成的神秘符号。 这是什么？旧世界的某种高级设备？ 凌风的心脏狂跳起来。他小心翼翼地将黑盒捧起，入手分量不轻。他翻来覆去地检查，却找不到任何开关或者接口。 就在他被灰尘染黑的拇指无意间划过其中一个最复杂的符号时—— “嗡……” 一声极度轻微的蜂鸣声响起，黑盒表面那些原本暗淡的符号，竟一个个亮起了柔和的蓝色微光，光芒流转，仿佛活了过来。 凌风'
15:28:10 app.api.v1.ai INFO   [AI续写] prompt: '续写', max_tokens: 100
15:28:10 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
15:28:10 app.services.ai.http_ai_service INFO   ModelSelector 已启用
15:28:10 app.services.ai.http_ai_service INFO   CostTracker 已启用
15:28:11 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
15:28:11 app.services.ai.http_ai_service INFO   AI自动补全请求 - 上下文长度: 194
15:28:11 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=100, temp=0.7, task_type=None
15:28:11 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/complete
INFO:     127.0.0.1:60808 - "POST /api/v1/ai/complete HTTP/1.1" 200 OK
15:28:12 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/ef5eb68c-32b8-4249-83a3-31d57363c0a9
INFO:     127.0.0.1:65138 - "PUT /api/v1/chapters/ef5eb68c-32b8-4249-83a3-31d57363c0a9 HTTP/1.1" 200 OK
15:28:12 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/ef5eb68c-32b8-4249-83a3-31d57363c0a9
INFO:     127.0.0.1:61915 - "PUT /api/v1/chapters/ef5eb68c-32b8-4249-83a3-31d57363c0a9 HTTP/1.1" 200 OK
15:28:14 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/2 200 OK"
15:28:14 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
15:28:14 app.services.ai.http_ai_service INFO   API 响应完成，共接收 3 个数据块，总长度: 25
15:28:14 app.services.ai.http_ai_service INFO   流式响应Token统计: 266 (prompt=247, completion=19)
15:28:14 app.services.agent.cost_tracker INFO   [CostTracker] 记录API调用: gemini-2.5-pro, tokens: 247+19=266, cost: $0.000010
15:28:14 app.services.ai.http_ai_service INFO   [CostTracker] API调用已记录: tokens=247+19, cost=$0.000010, time=2.62s
15:28:14 app.services.ai.ai_log_middleware INFO   AI调用日志已记录: operation=continue, tokens=133, cost=$0.000223, duration=2625ms, success=True
15:28:14 app.api.v1.ai INFO   [AI续写] 用户 testuser_new-1 请求完成，生成字数: 25
15:28:17 app.api.v1.ai INFO   [AI续写] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), 上下文长度: 194, 风格: 默认
15:28:17 app.api.v1.ai INFO   [AI续写] context内容: '一个属于那个传说时代的造物，就在他的手中苏醒。 “吼——！！！” 就在他心神激荡之际，一声充满了暴戾与疯狂的非人嘶吼，猛地从钢铁坟场的深处传来！ 那声音穿透了层层钢筋水泥，带着一股令人灵魂战栗的威压，仿佛有一头史前巨兽正在苏醒。 是“掘墓者”！一种常年盘踞在废墟地下的强大变异体！ 凌风的脸色瞬间变得惨白。他很清楚，那声音距离自己并不算远，而且正在快速靠近！ 来不及多想，他一把将仍在发光'
15:28:17 app.api.v1.ai INFO   [AI续写] prompt: '续写', max_tokens: 100
15:28:17 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
15:28:17 app.services.ai.http_ai_service INFO   ModelSelector 已启用
15:28:17 app.services.ai.http_ai_service INFO   CostTracker 已启用
15:28:19 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
15:28:19 app.services.ai.http_ai_service INFO   AI自动补全请求 - 上下文长度: 194
15:28:19 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=100, temp=0.7, task_type=None
15:28:19 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/complete
INFO:     127.0.0.1:60808 - "POST /api/v1/ai/complete HTTP/1.1" 200 OK
15:28:21 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/2 200 OK"
15:28:21 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
15:28:21 app.services.ai.http_ai_service INFO   API 响应完成，共接收 3 个数据块，总长度: 25
15:28:21 app.services.ai.http_ai_service INFO   流式响应Token统计: 267 (prompt=250, completion=17)
15:28:21 app.services.agent.cost_tracker INFO   [CostTracker] 记录API调用: gemini-2.5-pro, tokens: 250+17=267, cost: $0.000010
15:28:21 app.services.ai.http_ai_service INFO   [CostTracker] API调用已记录: tokens=250+17, cost=$0.000010, time=2.18s
15:28:21 app.services.ai.ai_log_middleware INFO   AI调用日志已记录: operation=continue, tokens=131, cost=$0.000220, duration=2187ms, success=True
15:28:21 app.api.v1.ai INFO   [AI续写] 用户 testuser_new-1 请求完成，生成字数: 25
15:28:43 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
15:28:43 app.services.ai.http_ai_service INFO   ModelSelector 已启用
15:28:43 app.services.ai.http_ai_service INFO   CostTracker 已启用
15:28:45 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
15:28:45 app.api.v1.agent INFO   [Chat Stream] Mode: react
15:28:45 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:51768 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
15:28:45 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: react, Message: 根据前面三章，来写第四章，逐渐展开剧情...
15:28:45 app.services.agent.memory.long_term_memory INFO   [LTM] 从作品 ad948837-e94e-4d0f-92a4-a75cf1301b07 检索到 0 条对话ID
15:28:45 app.services.agent.memory.long_term_memory INFO   [LTM] 最终返回 0 条对话摘要 (work_id=ad948837-e94e-4d0f-92a4-a75cf1301b07)
15:28:45 app.services.agent.memory.long_term_memory INFO   [LTM] 从作品 ad948837-e94e-4d0f-92a4-a75cf1301b07 检索到 0 条对话ID
15:28:45 app.services.agent.memory.long_term_memory INFO   [LTM] 最终返回 0 条对话摘要 (work_id=ad948837-e94e-4d0f-92a4-a75cf1301b07)
15:28:45 app.services.agent.memory.long_term_memory INFO   [LTM] 从作品 ad948837-e94e-4d0f-92a4-a75cf1301b07 检索到 0 条对话ID
15:28:45 app.services.agent.memory.long_term_memory INFO   [LTM] 最终返回 0 条对话摘要 (work_id=ad948837-e94e-4d0f-92a4-a75cf1301b07)
15:28:45 app.services.agent.langgraph_agent INFO   [LangGraph Stream] 开始流式执行: 根据前面三章，来写第四章，逐渐展开剧情...
15:28:45 app.services.agent.langgraph_agent INFO   [Context] 设置用户ID: 602f5147-846a-4cde-95d3-405fa75f133f
15:28:45 app.services.context.store INFO   [ContextStore] 加载上下文: 6515ce20-3116-4f79-bed5-e1804c0365f3, 2条消息
15:28:45 app.services.context.manager INFO   [ContextManager] Session 6515ce20-3116-4f79-bed5-e1804c0365f3: 2149/8000 tokens
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 15.96it/s]
15:28:45 app.services.context.vector_memory_store INFO   🔍 检索记忆 | 查询='根据前面三章，来写第四章，逐渐展开剧情...' | 用户=602f5147-846a-4cde-95d3-405fa75f133f | work_id=ad948837-e94e-4d0f-92a4-a75cf1301b07 | 找到=3条 | 阈值=0.3
15:28:45 app.services.context.manager INFO   🔍 检索长期记忆 | work_id=ad948837-e94e-4d0f-92a4-a75cf1301b07 | 查询='根据前面三章，来写第四章，逐渐展开剧情...' | 找到=3条 | 阈值=0.3
15:28:45 app.services.context.monitoring_integration INFO   [Monitor] 上下文构建: 4条消息, 2149 tokens, 耗时 78.32ms
15:28:45 app.services.agent.langgraph_agent INFO   [Context] 加载上下文: {'session_id': '6515ce20-3116-4f79-bed5-e1804c0365f3', 'token_count': 2149, 'short_memory_size': 2, 'has_summary': False, 'compression_triggered': False, 'long_term_memories': 3, 'adaptive_budget_enabled': False, 'task_type': None}
15:28:45 app.services.agent.langgraph_agent INFO   [LangGraph] 使用隔离的thread_id: ad948837-e94e-4d0f-92a4-a75cf1301b07:6515ce20-3116-4f79-bed5-e1804c0365f3 (work_id=ad948837-e94e-4d0f-92a4-a75cf1301b07, conversation_id=6515ce20-3116-4f79-bed5-e1804c0365f3)
15:28:45 app.services.agent.progress_tracker INFO   [ProgressTracker] 初始化完成，使用动态节点追踪模式（根据实际执行的节点自动计算进度）
15:28:45 app.services.agent.langgraph_agent INFO   [ProgressTracker] 初始化完成，使用动态节点追踪模式
15:28:45 app.services.agent.langgraph_agent INFO   [LangGraph] 意图分类（规则识别）
15:28:45 app.services.agent.langgraph_agent INFO   [Intent] 规则识别结果: writing, 置信度: 0.90
15:28:45 app.services.agent.langgraph_agent INFO   [LangGraph] 路由到: writing
15:28:45 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: _route_intent
15:28:45 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: intent_classifier
15:28:45 app.services.agent.langgraph_agent INFO   [Stream Event] progress_event = {'type': 'progress', 'step': 'intent_analysis', 'description': '识别为：写作任务', 'node': 'intent_classifier', 'details': {'intent': 'writing'}, 'timestamp': '2025-11-12T15:28:45.141004', 'progress': 100.0, 'eta': 0, 'eta_display': '即将完成', 'eta_confidence': 'high', 'current_step': 3, 'total_steps': 3, 'step_description': '第 3/3 步', 'elapsed': 0.0}
15:28:45 app.services.agent.langgraph_agent INFO   [Stream Event] on_progress 回调已调用
15:28:45 app.api.v1.agent INFO   [SSE] 发送 progress 事件: step=intent_analysis, desc=识别为：写作任务
15:28:45 app.services.agent.langgraph_agent INFO   [LangGraph] 处理写作请求（新架构）
15:28:45 Action.writing INFO   [writing] PromptManager已初始化
15:28:45 Action.writing INFO   [writing] work_id=ad948837-e94e-4d0f-92a4-a75cf1301b07, chapter_id=ef5eb68c-32b8-4249-83a3-31d57363c0a9, phase=None, chapter_num=None
15:28:45 app.services.agent.langgraph_agent INFO   [LangGraph] WritingAction准备完成: phase=None, chapter_num=None
15:28:45 app.services.agent.langgraph_agent INFO   [LangGraph] 处理writing场景 (use_chatgpt=True)
15:28:45 sqlalchemy.pool.impl.AsyncAdaptedQueuePool ERROR   The garbage collector is trying to clean up non-checked-in connection <AdaptedConnection <asyncpg.connection.Connection object at 0x0000019A844B57C0>>, which will be terminated.  Please ensure that SQLAlchemy pooled connections are returned to the pool explicitly, either by calling ``close()`` or by using appropriate context managers to manage their lifecycle.
D:\Java\ai_writer\backend\venv\Lib\site-packages\langchain_core\callbacks\manager.py:1904: SAWarning: The garbage collector is trying to clean up non-checked-in connection <AdaptedConnection <asyncpg.connection.Connection object at 0x0000019A844B57C0>>, which will be terminated.  Please ensure that SQLAlchemy pooled connections are returned to the pool explicitly, either by calling ``close()`` or by using appropriate context managers to manage their lifecycle.
  non_inline_tasks.append(task)
15:28:45 sqlalchemy.pool.impl.AsyncAdaptedQueuePool ERROR   The garbage collector is trying to clean up non-checked-in connection <AdaptedConnection <asyncpg.connection.Connection object at 0x0000019B002A0F50>>, which will be terminated.  Please ensure that SQLAlchemy pooled connections are returned to the pool explicitly, either by calling ``close()`` or by using appropriate context managers to manage their lifecycle.
D:\Java\ai_writer\backend\venv\Lib\site-packages\langchain_core\callbacks\manager.py:1904: SAWarning: The garbage collector is trying to clean up non-checked-in connection <AdaptedConnection <asyncpg.connection.Connection object at 0x0000019B002A0F50>>, which will be terminated.  Please ensure that SQLAlchemy pooled connections are returned to the pool explicitly, either by calling ``close()`` or by using appropriate context managers to manage their lifecycle.
  non_inline_tasks.append(task)
15:28:45 sqlalchemy.pool.impl.AsyncAdaptedQueuePool ERROR   The garbage collector is trying to clean up non-checked-in connection <AdaptedConnection <asyncpg.connection.Connection object at 0x0000019B03A63A70>>, which will be terminated.  Please ensure that SQLAlchemy pooled connections are returned to the pool explicitly, either by calling ``close()`` or by using appropriate context managers to manage their lifecycle.
D:\Java\ai_writer\backend\venv\Lib\site-packages\langchain_core\callbacks\manager.py:1904: SAWarning: The garbage collector is trying to clean up non-checked-in connection <AdaptedConnection <asyncpg.connection.Connection object at 0x0000019B03A63A70>>, which will be terminated.  Please ensure that SQLAlchemy pooled connections are returned to the pool explicitly, either by calling ``close()`` or by using appropriate context managers to manage their lifecycle.
  non_inline_tasks.append(task)
15:28:49 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
15:29:14 app.api.v1.ai INFO   [AI续写] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), 上下文长度: 195, 风格: 默认
15:29:14 app.api.v1.ai INFO   [AI续写] context内容: '他一把将仍在发光的黑盒塞进背包，拉上拉链。然后，他像是想起了什么，猛地转身，在那被撬开的储物柜最深处，摸出了一罐被遗忘在角落里的东西。 是一罐没有标签，但保存完好的午餐肉罐头！ 刚才的失望让他忽略了这个真正的“宝藏”。 此刻，这沉甸甸的罐头和那个神秘的黑盒一起躺在他的背包里，一边是生存的保障，另一边是未知的命运。 远处的嘶吼声越来越近，甚至能感觉到脚下的楼板在微微震颤。 没有时间犹豫了！'
15:29:14 app.api.v1.ai INFO   [AI续写] prompt: '续写', max_tokens: 100
15:29:14 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
15:29:14 app.services.ai.http_ai_service INFO   ModelSelector 已启用
15:29:14 app.services.ai.http_ai_service INFO   CostTracker 已启用
15:29:16 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
15:29:16 app.services.ai.http_ai_service INFO   AI自动补全请求 - 上下文长度: 195
15:29:16 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=100, temp=0.7, task_type=None
15:29:16 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/complete
INFO:     127.0.0.1:61104 - "POST /api/v1/ai/complete HTTP/1.1" 200 OK
15:29:18 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/2 200 OK"
15:29:18 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
15:29:18 app.services.ai.http_ai_service INFO   API 响应完成，共接收 3 个数据块，总长度: 27
15:29:18 app.services.ai.http_ai_service INFO   流式响应Token统计: 267 (prompt=249, completion=18)
15:29:18 app.services.agent.cost_tracker INFO   [CostTracker] 记录API调用: gemini-2.5-pro, tokens: 249+18=267, cost: $0.000010
15:29:18 app.services.ai.http_ai_service INFO   [CostTracker] API调用已记录: tokens=249+18, cost=$0.000010, time=2.37s
15:29:19 app.services.ai.ai_log_middleware INFO   AI调用日志已记录: operation=continue, tokens=136, cost=$0.000230, duration=2374ms, success=True
15:29:19 app.api.v1.ai INFO   [AI续写] 用户 testuser_new-1 请求完成，生成字数: 27
15:29:26 app.api.middleware.monitoring_middleware INFO   API请求完成: OPTIONS /api/v1/chapters/f0908bf1-bbc2-4d8e-9211-d33327dc82e7
15:29:26 app.api.middleware.monitoring_middleware INFO   API请求完成: OPTIONS /api/v1/chapters/f0908bf1-bbc2-4d8e-9211-d33327dc82e7
INFO:     127.0.0.1:53380 - "OPTIONS /api/v1/chapters/f0908bf1-bbc2-4d8e-9211-d33327dc82e7 HTTP/1.1" 200 OK
INFO:     127.0.0.1:52311 - "OPTIONS /api/v1/chapters/f0908bf1-bbc2-4d8e-9211-d33327dc82e7 HTTP/1.1" 200 OK
15:29:27 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/f0908bf1-bbc2-4d8e-9211-d33327dc82e7
INFO:     127.0.0.1:52311 - "PUT /api/v1/chapters/f0908bf1-bbc2-4d8e-9211-d33327dc82e7 HTTP/1.1" 200 OK
15:29:27 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/f0908bf1-bbc2-4d8e-9211-d33327dc82e7
INFO:     127.0.0.1:53380 - "PUT /api/v1/chapters/f0908bf1-bbc2-4d8e-9211-d33327dc82e7 HTTP/1.1" 200 OK
15:29:32 app.api.callbacks.monitoring_callback INFO   [MonitoringCallback] LLM调用成功: run_id=d491020a-b2a8-4d5a-8205-8fd7ebf031e9, model=unknown, duration=46.97s, tokens=N/A
15:29:32 app.services.agent.langgraph_agent INFO   [LangGraph] 无需工具调用，结束流程
15:29:32 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: _should_continue
15:29:32 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: writing_agent
15:29:32 app.services.agent.langgraph_agent INFO   [Stream Event] progress_event = {'type': 'progress', 'step': 'thinking', 'description': '正在思考如何帮助您...', 'node': 'writing_agent', 'details': {}, 'timestamp': '2025-11-12T15:29:32.158667', 'progress': 100.0, 'eta': 0, 'eta_display': '即将完成', 'eta_confidence': 'high', 'current_step': 5, 'total_steps': 5, 'step_description': '第 5/5 步', 'elapsed': 47.0}
15:29:32 app.api.v1.agent INFO   [Stream] Activity完成: intent_analysis (47.0s)
15:29:32 app.services.agent.langgraph_agent INFO   [Stream Event] on_progress 回调已调用
15:29:32 app.api.v1.agent INFO   [SSE] 发送 activity_complete 事件: step=intent_analysis, elapsed=47.0s
15:29:32 app.api.v1.agent INFO   [SSE] 发送 progress 事件: step=thinking, desc=正在思考如何帮助您...
15:29:32 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: LangGraph
15:29:32 app.services.agent.langgraph_agent INFO   [LangGraph Stream] 流式执行完成，共48个事件
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  3.33it/s]
15:29:32 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | work_id=ad948837-e94e-4d0f-92a4-a75cf1301b07 | 重要度=0.90 | 长度=2299
15:29:32 app.services.context.store INFO   [ContextStore] 保存上下文: 6515ce20-3116-4f79-bed5-e1804c0365f3, token=4992
15:29:32 app.services.context.manager INFO   [ContextManager] 更新上下文: 6515ce20-3116-4f79-bed5-e1804c0365f3, 消息数=4, Token=4992
15:29:32 app.services.agent.langgraph_agent INFO   [Context] 上下文已更新: 6515ce20-3116-4f79-bed5-e1804c0365f3 (work_id=ad948837-e94e-4d0f-92a4-a75cf1301b07)
15:29:32 app.services.agent.progress_tracker INFO   [ProgressTracker] 状态已重置
15:29:32 app.api.v1.agent INFO   [Stream] 最后活动完成: thinking (0.7s)
15:29:32 app.api.v1.agent INFO   [SSE] 发送 activity_complete 事件: step=thinking, elapsed=0.7s
15:29:32 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: react, Stream completed
15:29:34 app.api.v1.ai INFO   [AI续写] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), 上下文长度: 195, 风格: 默认
15:29:34 app.api.v1.ai INFO   [AI续写] context内容: '石般的外皮和能轻易撕裂钢板的巨爪，它的出现，就意味着死亡。 逃！ 肾上腺素压倒了一切杂念，求生的本能接管了身体。凌风将背包勒紧，身体压得极低，像一头被惊动的猎豹，朝着来时的方向亡命狂奔。 “轰！！” 身后传来震耳欲聋的巨响，一大片天花板连带着钢筋混凝土轰然砸落。气浪夹杂着粉尘扑面而来，呛得他剧烈咳嗽。那怪物正在用最野蛮的方式开路，它巨大的体型让任何精巧的建筑结构都形同虚设。 不能走直线！'
15:29:34 app.api.v1.ai INFO   [AI续写] prompt: '续写', max_tokens: 100
15:29:34 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
15:29:34 app.services.ai.http_ai_service INFO   ModelSelector 已启用
15:29:34 app.services.ai.http_ai_service INFO   CostTracker 已启用
15:29:36 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
15:29:36 app.services.ai.http_ai_service INFO   AI自动补全请求 - 上下文长度: 195
15:29:36 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=100, temp=0.7, task_type=None
15:29:36 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/complete
INFO:     127.0.0.1:51768 - "POST /api/v1/ai/complete HTTP/1.1" 200 OK
15:29:38 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/2 200 OK"
15:29:38 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
15:29:38 app.services.ai.http_ai_service INFO   API 响应完成，共接收 3 个数据块，总长度: 27
15:29:38 app.services.ai.http_ai_service INFO   流式响应Token统计: 287 (prompt=266, completion=21)
15:29:38 app.services.agent.cost_tracker INFO   [CostTracker] 记录API调用: gemini-2.5-pro, tokens: 266+21=287, cost: $0.000010
15:29:38 app.services.ai.http_ai_service INFO   [CostTracker] API调用已记录: tokens=266+21, cost=$0.000010, time=2.33s
15:29:38 app.services.ai.ai_log_middleware INFO   AI调用日志已记录: operation=continue, tokens=135, cost=$0.000229, duration=2331ms, success=True
15:29:38 app.api.v1.ai INFO   [AI续写] 用户 testuser_new-1 请求完成，生成字数: 27
15:30:31 app.api.v1.ai INFO   [AI续写] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), 上下文长度: 196, 风格: 默认
15:30:31 app.api.v1.ai INFO   [AI续写] context内容: '在这里登记，并上交至少一半的收获，才能换取当日的生存配给。 物资处前排着长队，一个身材魁梧、脸上有一道狰狞刀疤的男人正不耐烦地将一个拾荒者推开，他就是物资官“疤脸”。 “就这么点破烂？滚！今天只有半份水！”疤脸吼道。 轮到凌风时，一个如铁塔般的身影挡在了他面前。 “哟，这不是我们最‘能干’的凌风吗？”来人是聚落里有名的恶霸“铁拳”，他总是以欺凌比他弱小的人为乐，“今天又捡了什么垃圾回来？”'
15:30:31 app.api.v1.ai INFO   [AI续写] prompt: '续写', max_tokens: 100
15:30:31 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
15:30:31 app.services.ai.http_ai_service INFO   ModelSelector 已启用
15:30:31 app.services.ai.http_ai_service INFO   CostTracker 已启用
15:30:33 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
15:30:33 app.services.ai.http_ai_service INFO   AI自动补全请求 - 上下文长度: 196
15:30:33 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=100, temp=0.7, task_type=None
15:30:33 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/complete
INFO:     127.0.0.1:54390 - "POST /api/v1/ai/complete HTTP/1.1" 200 OK
15:30:35 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/2 200 OK"
15:30:35 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
15:30:35 app.services.ai.http_ai_service INFO   API 响应完成，共接收 3 个数据块，总长度: 43
15:30:35 app.services.ai.http_ai_service INFO   流式响应Token统计: 292 (prompt=259, completion=33)
15:30:35 app.services.agent.cost_tracker INFO   [CostTracker] 记录API调用: gemini-2.5-pro, tokens: 259+33=292, cost: $0.000012
15:30:35 app.services.ai.http_ai_service INFO   [CostTracker] API调用已记录: tokens=259+33, cost=$0.000012, time=2.41s
15:30:35 app.services.ai.ai_log_middleware INFO   AI调用日志已记录: operation=continue, tokens=142, cost=$0.000275, duration=2418ms, success=True
15:30:35 app.api.v1.ai INFO   [AI续写] 用户 testuser_new-1 请求完成，生成字数: 43
15:30:51 app.api.v1.ai INFO   [AI续写] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), 上下文长度: 197, 风格: 默认
15:30:51 app.api.v1.ai INFO   [AI续写] context内容: '是整个蚁巢最偏僻的角落之一，潮湿、阴冷，却能给他带来一丝宝贵的安宁。 确认四周无人后，他坐上吊床，小心翼翼地从夹层里拿出那罐午餐肉。在昏暗的光线下，金属罐身反射着诱人的光泽。他用多功能钳撬开一个小口，一股早已被遗忘的、浓郁的肉香瞬间钻入鼻孔。 饥饿的胃在疯狂抗议，唾液不受控制地分泌。但他只是深深地吸了一口气，又用极大的毅力，将那个小口重新压平、卷好。 现在还不是时候。这罐头，是他未来的底牌。'
15:30:51 app.api.v1.ai INFO   [AI续写] prompt: '续写', max_tokens: 100
15:30:51 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
15:30:51 app.services.ai.http_ai_service INFO   ModelSelector 已启用
15:30:51 app.services.ai.http_ai_service INFO   CostTracker 已启用
15:30:53 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
15:30:53 app.services.ai.http_ai_service INFO   AI自动补全请求 - 上下文长度: 197
15:30:53 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=100, temp=0.7, task_type=None
15:30:53 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/complete
INFO:     127.0.0.1:49839 - "POST /api/v1/ai/complete HTTP/1.1" 200 OK
15:31:04 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/2 200 OK"
15:31:04 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
15:31:12 app.api.middleware.monitoring_middleware INFO   API请求完成: OPTIONS /api/v1/chapters/803ee3d1-5cc6-48a7-871d-f4a53511a749
15:31:12 app.api.middleware.monitoring_middleware INFO   API请求完成: OPTIONS /api/v1/chapters/803ee3d1-5cc6-48a7-871d-f4a53511a749
INFO:     127.0.0.1:52141 - "OPTIONS /api/v1/chapters/803ee3d1-5cc6-48a7-871d-f4a53511a749 HTTP/1.1" 200 OK
INFO:     127.0.0.1:59530 - "OPTIONS /api/v1/chapters/803ee3d1-5cc6-48a7-871d-f4a53511a749 HTTP/1.1" 200 OK
15:31:12 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/803ee3d1-5cc6-48a7-871d-f4a53511a749
INFO:     127.0.0.1:52141 - "PUT /api/v1/chapters/803ee3d1-5cc6-48a7-871d-f4a53511a749 HTTP/1.1" 200 OK
15:31:13 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/803ee3d1-5cc6-48a7-871d-f4a53511a749
INFO:     127.0.0.1:59530 - "PUT /api/v1/chapters/803ee3d1-5cc6-48a7-871d-f4a53511a749 HTTP/1.1" 200 OK
15:31:42 app.api.v1.ai INFO   [AI续写] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), 上下文长度: 194, 风格: 默认
15:31:42 app.api.v1.ai INFO   [AI续写] context内容: '一片深邃的黑暗。 不，不是黑暗。 凌风凑近了看，才发现那是一块纯黑色的晶体屏幕。此刻，屏幕上正有点点星光亮起，由少变多，迅速汇聚成一片璀璨的星河。 “这是……”凌风的呼吸停滞了。 他从未见过如此美丽的景象。聚落的夜晚虽然也能看到星星，但远没有眼前这般清晰、浩瀚。星辰在他的眼前缓缓旋转，一条条淡蓝色的光线在星辰之间连接，勾勒出复杂的航线和坐标。 这不是简单的星空图。 这是一幅星际航行图！'
15:31:42 app.api.v1.ai INFO   [AI续写] prompt: '续写', max_tokens: 100
15:31:42 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
15:31:42 app.services.ai.http_ai_service INFO   ModelSelector 已启用
15:31:42 app.services.ai.http_ai_service INFO   CostTracker 已启用
15:31:43 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
15:31:43 app.services.ai.http_ai_service INFO   AI自动补全请求 - 上下文长度: 194
15:31:43 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=100, temp=0.7, task_type=None
15:31:43 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/complete
15:31:43 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 33
15:31:43 app.services.ai.http_ai_service INFO   流式响应Token统计: 4027 (prompt=4000, completion=27)
15:31:43 app.services.agent.cost_tracker INFO   [CostTracker] 记录API调用: gemini-2.5-pro, tokens: 4000+27=4027, cost: $0.000123
15:31:43 app.services.ai.http_ai_service INFO   [CostTracker] API调用已记录: tokens=4000+27, cost=$0.000123, time=50.14s
INFO:     127.0.0.1:53104 - "POST /api/v1/ai/complete HTTP/1.1" 200 OK
15:31:43 app.services.ai.ai_log_middleware INFO   AI调用日志已记录: operation=continue, tokens=141, cost=$0.000251, duration=50159ms, success=True
15:31:43 app.api.v1.ai INFO   [AI续写] 用户 testuser_new-1 请求完成，生成字数: 33
15:31:45 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/2 200 OK"
15:31:45 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
15:31:46 app.services.ai.http_ai_service INFO   API 响应完成，共接收 2 个数据块，总长度: 25
15:31:46 app.services.ai.http_ai_service INFO   流式响应Token统计: 263 (prompt=247, completion=16)
15:31:46 app.services.agent.cost_tracker INFO   [CostTracker] 记录API调用: gemini-2.5-pro, tokens: 247+16=263, cost: $0.000009
15:31:46 app.services.ai.http_ai_service INFO   [CostTracker] API调用已记录: tokens=247+16, cost=$0.000009, time=2.24s
15:31:46 app.services.ai.ai_log_middleware INFO   AI调用日志已记录: operation=continue, tokens=132, cost=$0.000221, duration=2245ms, success=True
15:31:46 app.api.v1.ai INFO   [AI续写] 用户 testuser_new-1 请求完成，生成字数: 25
15:31:54 app.api.v1.ai INFO   [AI续写] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), 上下文长度: 194, 风格: 默认
15:31:54 app.api.v1.ai INFO   [AI续写] context内容: '一片深邃的黑暗。 不，不是黑暗。 凌风凑近了看，才发现那是一块纯黑色的晶体屏幕。此刻，屏幕上正有点点星光亮起，由少变多，迅速汇聚成一片璀璨的星河。 “这是……”凌风的呼吸停滞了。 他从未见过如此美丽的景象。聚落的夜晚虽然也能看到星星，但远没有眼前这般清晰、浩瀚。星辰在他的眼前缓缓旋转，一条条淡蓝色的光线在星辰之间连接，勾勒出复杂的航线和坐标。 这不是简单的星空图。 这是一幅星际航行图！'
15:31:54 app.api.v1.ai INFO   [AI续写] prompt: '续写', max_tokens: 100
15:31:54 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
15:31:54 app.services.ai.http_ai_service INFO   ModelSelector 已启用
15:31:54 app.services.ai.http_ai_service INFO   CostTracker 已启用
15:31:56 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
15:31:56 app.services.ai.http_ai_service INFO   AI自动补全请求 - 上下文长度: 194
15:31:56 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=100, temp=0.7, task_type=None
15:31:56 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/complete
15:31:56 sqlalchemy.pool.impl.AsyncAdaptedQueuePool ERROR   The garbage collector is trying to clean up non-checked-in connection <AdaptedConnection <asyncpg.connection.Connection object at 0x0000019ADA84B4D0>>, which will be terminated.  Please ensure that SQLAlchemy pooled connections are returned to the pool explicitly, either by calling ``close()`` or by using appropriate context managers to manage their lifecycle.
C:\Program Files\Python312\Lib\contextlib.py:132: SAWarning: The garbage collector is trying to clean up non-checked-in connection <AdaptedConnection <asyncpg.connection.Connection object at 0x0000019ADA84B4D0>>, which will be terminated.  Please ensure that SQLAlchemy pooled connections are returned to the pool explicitly, either by calling ``close()`` or by using appropriate context managers to manage their lifecycle.
  def __enter__(self):
15:31:56 sqlalchemy.pool.impl.AsyncAdaptedQueuePool ERROR   The garbage collector is trying to clean up non-checked-in connection <AdaptedConnection <asyncpg.connection.Connection object at 0x0000019B03A2C6E0>>, which will be terminated.  Please ensure that SQLAlchemy pooled connections are returned to the pool explicitly, either by calling ``close()`` or by using appropriate context managers to manage their lifecycle.
C:\Program Files\Python312\Lib\contextlib.py:132: SAWarning: The garbage collector is trying to clean up non-checked-in connection <AdaptedConnection <asyncpg.connection.Connection object at 0x0000019B03A2C6E0>>, which will be terminated.  Please ensure that SQLAlchemy pooled connections are returned to the pool explicitly, either by calling ``close()`` or by using appropriate context managers to manage their lifecycle.
  def __enter__(self):
15:31:56 sqlalchemy.pool.impl.AsyncAdaptedQueuePool ERROR   The garbage collector is trying to clean up non-checked-in connection <AdaptedConnection <asyncpg.connection.Connection object at 0x0000019ADA84A300>>, which will be terminated.  Please ensure that SQLAlchemy pooled connections are returned to the pool explicitly, either by calling ``close()`` or by using appropriate context managers to manage their lifecycle.
C:\Program Files\Python312\Lib\contextlib.py:132: SAWarning: The garbage collector is trying to clean up non-checked-in connection <AdaptedConnection <asyncpg.connection.Connection object at 0x0000019ADA84A300>>, which will be terminated.  Please ensure that SQLAlchemy pooled connections are returned to the pool explicitly, either by calling ``close()`` or by using appropriate context managers to manage their lifecycle.
  def __enter__(self):
15:31:56 sqlalchemy.pool.impl.AsyncAdaptedQueuePool ERROR   The garbage collector is trying to clean up non-checked-in connection <AdaptedConnection <asyncpg.connection.Connection object at 0x0000019B03A2FA70>>, which will be terminated.  Please ensure that SQLAlchemy pooled connections are returned to the pool explicitly, either by calling ``close()`` or by using appropriate context managers to manage their lifecycle.
C:\Program Files\Python312\Lib\contextlib.py:132: SAWarning: The garbage collector is trying to clean up non-checked-in connection <AdaptedConnection <asyncpg.connection.Connection object at 0x0000019B03A2FA70>>, which will be terminated.  Please ensure that SQLAlchemy pooled connections are returned to the pool explicitly, either by calling ``close()`` or by using appropriate context managers to manage their lifecycle.
  def __enter__(self):
15:31:56 sqlalchemy.pool.impl.AsyncAdaptedQueuePool ERROR   The garbage collector is trying to clean up non-checked-in connection <AdaptedConnection <asyncpg.connection.Connection object at 0x0000019B03A2E5D0>>, which will be terminated.  Please ensure that SQLAlchemy pooled connections are returned to the pool explicitly, either by calling ``close()`` or by using appropriate context managers to manage their lifecycle.
C:\Program Files\Python312\Lib\contextlib.py:132: SAWarning: The garbage collector is trying to clean up non-checked-in connection <AdaptedConnection <asyncpg.connection.Connection object at 0x0000019B03A2E5D0>>, which will be terminated.  Please ensure that SQLAlchemy pooled connections are returned to the pool explicitly, either by calling ``close()`` or by using appropriate context managers to manage their lifecycle.
  def __enter__(self):
INFO:     127.0.0.1:61477 - "POST /api/v1/ai/complete HTTP/1.1" 200 OK
15:31:57 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/2 200 OK"
15:31:57 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
15:31:58 app.services.ai.http_ai_service INFO   API 响应完成，共接收 3 个数据块，总长度: 37
15:31:58 app.services.ai.http_ai_service INFO   流式响应Token统计: 271 (prompt=247, completion=24)
15:31:58 app.services.agent.cost_tracker INFO   [CostTracker] 记录API调用: gemini-2.5-pro, tokens: 247+24=271, cost: $0.000010
15:31:58 app.services.ai.http_ai_service INFO   [CostTracker] API调用已记录: tokens=247+24, cost=$0.000010, time=2.21s
15:31:58 app.services.ai.ai_log_middleware INFO   AI调用日志已记录: operation=continue, tokens=138, cost=$0.000251, duration=2206ms, success=True
15:31:58 app.api.v1.ai INFO   [AI续写] 用户 testuser_new-1 请求完成，生成字数: 37
15:32:06 app.api.v1.ai INFO   [AI续写] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), 上下文长度: 195, 风格: 默认
15:32:06 app.api.v1.ai INFO   [AI续写] context内容: '这就是“星辰之钥”？ 紧接着，另一组坐标信息在“星辰之钥”的投影旁浮现： [“星辰之钥”组件#1 位置：坐标（34.0522, -118.2437）] [警告：该区域能量波动异常，已被高阶污染物“利维坦”占据] “利维坦……” 凌风倒吸一口凉气。如果说“掘墓者”是拾荒者的噩梦，那“利维坦”就是所有废土聚落的末日天灾。那是传说中如山峦般巨大的移动堡垒型污染物，所过之处，一切都会被夷为平地。'
15:32:06 app.api.v1.ai INFO   [AI续写] prompt: '续写', max_tokens: 100
15:32:06 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
15:32:06 app.services.ai.http_ai_service INFO   ModelSelector 已启用
15:32:06 app.services.ai.http_ai_service INFO   CostTracker 已启用
15:32:07 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
15:32:07 app.services.ai.http_ai_service INFO   AI自动补全请求 - 上下文长度: 195
15:32:07 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=100, temp=0.7, task_type=None
15:32:07 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/complete
INFO:     127.0.0.1:64565 - "POST /api/v1/ai/complete HTTP/1.1" 200 OK
15:32:11 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/2 200 OK"
15:32:11 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
15:32:27 app.api.middleware.monitoring_middleware INFO   API请求完成: OPTIONS /api/v1/chapters/ef5eb68c-32b8-4249-83a3-31d57363c0a9
INFO:     127.0.0.1:58284 - "OPTIONS /api/v1/chapters/ef5eb68c-32b8-4249-83a3-31d57363c0a9 HTTP/1.1" 200 OK
15:32:27 app.api.middleware.monitoring_middleware INFO   API请求完成: OPTIONS /api/v1/chapters/ef5eb68c-32b8-4249-83a3-31d57363c0a9
INFO:     127.0.0.1:58284 - "OPTIONS /api/v1/chapters/ef5eb68c-32b8-4249-83a3-31d57363c0a9 HTTP/1.1" 200 OK
15:32:28 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/ef5eb68c-32b8-4249-83a3-31d57363c0a9
INFO:     127.0.0.1:58284 - "PUT /api/v1/chapters/ef5eb68c-32b8-4249-83a3-31d57363c0a9 HTTP/1.1" 200 OK
15:32:28 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/ef5eb68c-32b8-4249-83a3-31d57363c0a9
INFO:     127.0.0.1:53688 - "PUT /api/v1/chapters/ef5eb68c-32b8-4249-83a3-31d57363c0a9 HTTP/1.1" 200 OK
15:32:28 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 25
15:32:28 app.services.ai.http_ai_service INFO   流式响应Token统计: 1854 (prompt=1839, completion=15)
15:32:28 app.services.agent.cost_tracker INFO   [CostTracker] 记录API调用: gemini-2.5-pro, tokens: 1839+15=1854, cost: $0.000057
15:32:28 app.services.ai.http_ai_service INFO   [CostTracker] API调用已记录: tokens=1839+15, cost=$0.000057, time=20.62s
15:32:28 app.services.ai.ai_log_middleware INFO   AI调用日志已记录: operation=continue, tokens=120, cost=$0.000206, duration=20625ms, success=True
15:32:28 app.api.v1.ai INFO   [AI续写] 用户 testuser_new-1 请求完成，生成字数: 25
15:32:28 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/f0908bf1-bbc2-4d8e-9211-d33327dc82e7
INFO:     127.0.0.1:53688 - "PUT /api/v1/chapters/f0908bf1-bbc2-4d8e-9211-d33327dc82e7 HTTP/1.1" 200 OK
15:32:28 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/f0908bf1-bbc2-4d8e-9211-d33327dc82e7
INFO:     127.0.0.1:64565 - "PUT /api/v1/chapters/f0908bf1-bbc2-4d8e-9211-d33327dc82e7 HTTP/1.1" 200 OK
15:32:29 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/803ee3d1-5cc6-48a7-871d-f4a53511a749
15:32:29 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/803ee3d1-5cc6-48a7-871d-f4a53511a749
INFO:     127.0.0.1:53688 - "PUT /api/v1/chapters/803ee3d1-5cc6-48a7-871d-f4a53511a749 HTTP/1.1" 200 OK
INFO:     127.0.0.1:64565 - "PUT /api/v1/chapters/803ee3d1-5cc6-48a7-871d-f4a53511a749 HTTP/1.1" 200 OK
15:32:32 app.api.middleware.monitoring_middleware INFO   API请求完成: OPTIONS /api/v1/chapters
INFO:     127.0.0.1:64565 - "OPTIONS /api/v1/chapters HTTP/1.1" 200 OK
15:32:32 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/chapters
INFO:     127.0.0.1:53688 - "POST /api/v1/chapters HTTP/1.1" 201 Created
15:32:32 app.api.middleware.monitoring_middleware INFO   API请求完成: OPTIONS /api/v1/analysis/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/start
INFO:     127.0.0.1:53688 - "OPTIONS /api/v1/analysis/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/start HTTP/1.1" 200 OK
15:32:33 app.services.novel_analysis_service INFO   Deleted old analysis for work ad948837-e94e-4d0f-92a4-a75cf1301b07, creating new one
15:32:33 app.api.middleware.monitoring_middleware INFO   API请求完成: OPTIONS /api/v1/chapters/298f5ac1-437c-4087-919b-5db66b1b3b14
15:32:33 app.api.middleware.monitoring_middleware INFO   API请求完成: OPTIONS /api/v1/chapters/298f5ac1-437c-4087-919b-5db66b1b3b14
INFO:     127.0.0.1:53688 - "OPTIONS /api/v1/chapters/298f5ac1-437c-4087-919b-5db66b1b3b14 HTTP/1.1" 200 OK
INFO:     127.0.0.1:58284 - "OPTIONS /api/v1/chapters/298f5ac1-437c-4087-919b-5db66b1b3b14 HTTP/1.1" 200 OK
15:32:33 sqlalchemy.pool.impl.AsyncAdaptedQueuePool ERROR   The garbage collector is trying to clean up non-checked-in connection <AdaptedConnection <asyncpg.connection.Connection object at 0x0000019B03A2E300>>, which will be terminated.  Please ensure that SQLAlchemy pooled connections are returned to the pool explicitly, either by calling ``close()`` or by using appropriate context managers to manage their lifecycle.
D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\middleware\base.py:27: SAWarning: The garbage collector is trying to clean up non-checked-in connection <AdaptedConnection <asyncpg.connection.Connection object at 0x0000019B03A2E300>>, which will be terminated.  Please ensure that SQLAlchemy pooled connections are returned to the pool explicitly, either by calling ``close()`` or by using appropriate context managers to manage their lifecycle.
  def __init__(self, scope: Scope, receive: Receive):
15:32:33 app.services.novel_analysis_service INFO   Created analysis task for work ad948837-e94e-4d0f-92a4-a75cf1301b07, total_chapters: 4
15:32:33 app.api.v1.novel_analysis INFO   User 602f5147-846a-4cde-95d3-405fa75f133f started analysis for work ad948837-e94e-4d0f-92a4-a75cf1301b07, analysis_id: 9e3368de-0b78-4e20-9b70-3443e01c4358
15:32:33 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/analysis/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/start
INFO:     127.0.0.1:64565 - "POST /api/v1/analysis/works/ad948837-e94e-4d0f-92a4-a75cf1301b07/start HTTP/1.1" 201 Created
15:32:33 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/298f5ac1-437c-4087-919b-5db66b1b3b14
INFO:     127.0.0.1:53688 - "PUT /api/v1/chapters/298f5ac1-437c-4087-919b-5db66b1b3b14 HTTP/1.1" 200 OK
15:32:33 app.api.v1.novel_analysis INFO   后台任务开始：分析作品 ad948837-e94e-4d0f-92a4-a75cf1301b07
15:32:33 app.api.v1.novel_analysis INFO   后台任务已找到分析记录 analysis_id=9e3368de-0b78-4e20-9b70-3443e01c4358
15:32:33 app.services.ai.novel_analysis_orchestrator INFO   ============================================================
15:32:33 app.services.ai.novel_analysis_orchestrator INFO   开始分析作品: ad948837-e94e-4d0f-92a4-a75cf1301b07
15:32:33 app.services.ai.novel_analysis_orchestrator INFO   ============================================================
15:32:33 app.services.novel_analysis_service INFO   Updated analysis 9e3368de-0b78-4e20-9b70-3443e01c4358 progress: 0/4, stage: AnalysisStage.MICRO_ANALYSIS, status: AnalysisStatus.ANALYZING
15:32:33 app.services.ai.novel_analysis_orchestrator INFO   初始化AI分析服务...
15:32:33 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
15:32:33 app.services.ai.http_ai_service INFO   ModelSelector 已启用
15:32:33 app.services.ai.http_ai_service INFO   CostTracker 已启用
15:32:34 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
15:32:34 app.services.ai.novel_micro_analysis INFO   微观分析提示词加载成功
15:32:34 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
15:32:34 app.services.ai.http_ai_service INFO   ModelSelector 已启用
15:32:34 app.services.ai.http_ai_service INFO   CostTracker 已启用
15:32:36 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
15:32:36 app.services.ai.novel_macro_analysis INFO   宏观分析提示词加载成功
15:32:36 app.services.ai.novel_analysis_orchestrator INFO   共获取 4 个章节，开始微观分析...
15:32:36 app.services.ai.novel_analysis_orchestrator INFO   ⚡ 使用并行分析模式 (并发数: 5)
15:32:36 app.services.ai.novel_analysis_orchestrator INFO   ⚡ 启动 4 个并发分析任务...
15:32:36 app.services.ai.novel_analysis_orchestrator INFO   [1/4] 🔄 开始分析: 钢铁坟场
15:32:36 app.services.ai.novel_analysis_orchestrator INFO   [2/4] 🔄 开始分析: 归巢与低语
15:32:36 app.services.ai.novel_analysis_orchestrator INFO   [3/4] 🔄 开始分析: 遗落的星图
15:32:36 app.services.ai.novel_analysis_orchestrator INFO   [4/4] 🔄 开始分析: 天眼与土獾
15:32:36 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/298f5ac1-437c-4087-919b-5db66b1b3b14
INFO:     127.0.0.1:53788 - "PUT /api/v1/chapters/298f5ac1-437c-4087-919b-5db66b1b3b14 HTTP/1.1" 200 OK
15:32:46 app.services.redis_cache_service WARNING   ⚠️  Redis连接失败,缓存功能将禁用: Timeout connecting to server
15:32:46 app.services.ai.novel_micro_analysis INFO   开始AI分析章节: ef5eb68c-32b8-4249-83a3-31d57363c0a9 - 钢铁坟场
15:32:46 app.services.ai.novel_micro_analysis INFO   第 1/3 次尝试调用AI分析
15:32:46 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=4000, temp=0.3, task_type=None
15:32:46 app.services.redis_cache_service WARNING   查询缓存失败 (重试 1/2): Timeout connecting to server
15:32:46 app.services.redis_cache_service WARNING   查询缓存最终失败: 'NoneType' object has no attribute 'get'
15:32:46 app.services.ai.novel_micro_analysis INFO   开始AI分析章节: 803ee3d1-5cc6-48a7-871d-f4a53511a749 - 遗落的星图
15:32:46 app.services.ai.novel_micro_analysis INFO   第 1/3 次尝试调用AI分析
15:32:46 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=4000, temp=0.3, task_type=None
15:32:46 app.services.redis_cache_service WARNING   查询缓存失败 (重试 1/2): Timeout connecting to server
15:32:46 app.services.redis_cache_service WARNING   查询缓存最终失败: 'NoneType' object has no attribute 'get'
15:32:46 app.services.ai.novel_micro_analysis INFO   开始AI分析章节: 298f5ac1-437c-4087-919b-5db66b1b3b14 - 天眼与土獾
15:32:46 app.services.ai.novel_micro_analysis INFO   第 1/3 次尝试调用AI分析
15:32:46 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=4000, temp=0.3, task_type=None
15:32:46 app.services.redis_cache_service WARNING   查询缓存失败 (重试 1/2): Timeout connecting to server
15:32:46 app.services.redis_cache_service WARNING   查询缓存最终失败: 'NoneType' object has no attribute 'get'
15:32:46 app.services.ai.novel_micro_analysis INFO   开始AI分析章节: f0908bf1-bbc2-4d8e-9211-d33327dc82e7 - 归巢与低语
15:32:46 app.services.ai.novel_micro_analysis INFO   第 1/3 次尝试调用AI分析
15:32:46 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=4000, temp=0.3, task_type=None
15:32:48 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/298f5ac1-437c-4087-919b-5db66b1b3b14
INFO:     127.0.0.1:53141 - "PUT /api/v1/chapters/298f5ac1-437c-4087-919b-5db66b1b3b14 HTTP/1.1" 200 OK
15:32:49 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/298f5ac1-437c-4087-919b-5db66b1b3b14
INFO:     127.0.0.1:53141 - "PUT /api/v1/chapters/298f5ac1-437c-4087-919b-5db66b1b3b14 HTTP/1.1" 200 OK