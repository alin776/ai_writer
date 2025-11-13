11:05:31 app.api.v1.auth INFO   [LOGIN] 尝试登录: 2072855200@qq.com
11:05:32 app.api.v1.auth INFO   [LOGIN] 会话创建成功: 602f5147-846a-4cde-95d3-405fa75f133f (127.0.0.1)
11:05:32 app.api.v1.auth INFO   [LOGIN] 登录成功: testuser_new-1 (602f5147-846a-4cde-95d3-405fa75f133f) from 127.0.0.1
11:05:32 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/auth/login
INFO:     127.0.0.1:58653 - "POST /api/v1/auth/login HTTP/1.1" 200 OK
11:05:32 app.api.middleware.monitoring_middleware INFO   API请求完成: OPTIONS /api/v1/users/me
INFO:     127.0.0.1:58653 - "OPTIONS /api/v1/users/me HTTP/1.1" 200 OK
11:05:32 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/users/me
INFO:     127.0.0.1:58653 - "GET /api/v1/users/me HTTP/1.1" 200 OK
11:05:33 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works
INFO:     127.0.0.1:58653 - "GET /api/v1/works HTTP/1.1" 200 OK
11:05:33 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works
INFO:     127.0.0.1:63983 - "GET /api/v1/works HTTP/1.1" 200 OK
11:05:36 app.api.middleware.monitoring_middleware INFO   API请求完成: OPTIONS /api/v1/works/ff5c96e1-068a-40f5-a974-45e681c4174d
INFO:     127.0.0.1:63983 - "OPTIONS /api/v1/works/ff5c96e1-068a-40f5-a974-45e681c4174d HTTP/1.1" 200 OK
11:05:36 app.api.middleware.monitoring_middleware INFO   API请求完成: DELETE /api/v1/works/ff5c96e1-068a-40f5-a974-45e681c4174d
INFO:     127.0.0.1:63983 - "DELETE /api/v1/works/ff5c96e1-068a-40f5-a974-45e681c4174d HTTP/1.1" 204 No Content
11:05:38 app.api.middleware.monitoring_middleware INFO   API请求完成: OPTIONS /api/v1/works/e54fc473-7ed6-4e80-9446-b3ced17bd289
INFO:     127.0.0.1:63983 - "OPTIONS /api/v1/works/e54fc473-7ed6-4e80-9446-b3ced17bd289 HTTP/1.1" 200 OK
11:05:38 app.api.middleware.monitoring_middleware INFO   API请求完成: DELETE /api/v1/works/e54fc473-7ed6-4e80-9446-b3ced17bd289
INFO:     127.0.0.1:63983 - "DELETE /api/v1/works/e54fc473-7ed6-4e80-9446-b3ced17bd289 HTTP/1.1" 204 No Content
11:06:40 app.api.middleware.monitoring_middleware INFO   API请求完成: OPTIONS /api/v1/works
INFO:     127.0.0.1:55229 - "OPTIONS /api/v1/works HTTP/1.1" 200 OK
11:06:40 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/works
INFO:     127.0.0.1:55229 - "POST /api/v1/works HTTP/1.1" 201 Created
11:06:40 app.api.middleware.monitoring_middleware INFO   API请求完成: OPTIONS /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/ai-guidelines
INFO:     127.0.0.1:55229 - "OPTIONS /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/ai-guidelines HTTP/1.1" 200 OK
11:06:41 app.api.v1.worldview INFO   [AI Guidelines] 创建 work_id=eb13b431-caef-4ec3-83b2-453951b16a72 的AI规范
11:06:41 app.api.v1.worldview INFO   [自动创建] 设定: 世界规则
11:06:41 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/ai-guidelines
INFO:     127.0.0.1:55229 - "POST /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/ai-guidelines HTTP/1.1" 201 Created
11:06:41 app.api.middleware.monitoring_middleware INFO   API请求完成: OPTIONS /api/v1/works/eb13b431-caef-4ec3-83b2-453951b16a72
11:06:41 app.api.middleware.monitoring_middleware INFO   API请求完成: OPTIONS /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/characters
11:06:41 app.api.middleware.monitoring_middleware INFO   API请求完成: OPTIONS /api/v1/chapters/work/eb13b431-caef-4ec3-83b2-453951b16a72
INFO:     127.0.0.1:55229 - "OPTIONS /api/v1/works/eb13b431-caef-4ec3-83b2-453951b16a72 HTTP/1.1" 200 OK
11:06:41 app.api.middleware.monitoring_middleware INFO   API请求完成: OPTIONS /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/locations
INFO:     127.0.0.1:52630 - "OPTIONS /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/characters HTTP/1.1" 200 OK
INFO:     127.0.0.1:53547 - "OPTIONS /api/v1/chapters/work/eb13b431-caef-4ec3-83b2-453951b16a72 HTTP/1.1" 200 OK
INFO:     127.0.0.1:53987 - "OPTIONS /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/locations HTTP/1.1" 200 OK
11:06:41 app.api.middleware.monitoring_middleware INFO   API请求完成: OPTIONS /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/settings
11:06:41 app.api.middleware.monitoring_middleware INFO   API请求完成: OPTIONS /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/guidelines
11:06:41 app.api.middleware.monitoring_middleware INFO   API请求完成: OPTIONS /api/v1/works/eb13b431-caef-4ec3-83b2-453951b16a72
INFO:     127.0.0.1:55229 - "OPTIONS /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/settings HTTP/1.1" 200 OK
INFO:     127.0.0.1:52630 - "OPTIONS /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:53547 - "OPTIONS /api/v1/works/eb13b431-caef-4ec3-83b2-453951b16a72 HTTP/1.1" 200 OK
11:06:41 app.api.middleware.monitoring_middleware INFO   API请求完成: OPTIONS /api/v1/chapters/work/eb13b431-caef-4ec3-83b2-453951b16a72
11:06:41 app.api.middleware.monitoring_middleware INFO   API请求完成: OPTIONS /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/characters
11:06:41 app.api.middleware.monitoring_middleware INFO   API请求完成: OPTIONS /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/locations
INFO:     127.0.0.1:55229 - "OPTIONS /api/v1/chapters/work/eb13b431-caef-4ec3-83b2-453951b16a72 HTTP/1.1" 200 OK
INFO:     127.0.0.1:52630 - "OPTIONS /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/characters HTTP/1.1" 200 OK
INFO:     127.0.0.1:53547 - "OPTIONS /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/locations HTTP/1.1" 200 OK
11:06:41 app.api.middleware.monitoring_middleware INFO   API请求完成: OPTIONS /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/settings
11:06:41 app.api.middleware.monitoring_middleware INFO   API请求完成: OPTIONS /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/guidelines
INFO:     127.0.0.1:55229 - "OPTIONS /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/settings HTTP/1.1" 200 OK
INFO:     127.0.0.1:52630 - "OPTIONS /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/guidelines HTTP/1.1" 200 OK
11:06:41 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/ai-guidelines
INFO:     127.0.0.1:53987 - "GET /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/ai-guidelines HTTP/1.1" 200 OK
11:06:41 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/characters
INFO:     127.0.0.1:55229 - "GET /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/characters HTTP/1.1" 200 OK
11:06:41 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/settings
INFO:     127.0.0.1:55229 - "GET /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/settings HTTP/1.1" 200 OK
11:06:41 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/guidelines
INFO:     127.0.0.1:55229 - "GET /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/guidelines HTTP/1.1" 200 OK
11:06:41 app.api.v1.chapters INFO   [GET chapters] work_id=eb13b431-caef-4ec3-83b2-453951b16a72, user_id=602f5147-846a-4cde-95d3-405fa75f133f
11:06:41 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/settings
INFO:     127.0.0.1:55229 - "GET /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/settings HTTP/1.1" 200 OK
11:06:41 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/guidelines
INFO:     127.0.0.1:55229 - "GET /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/guidelines HTTP/1.1" 200 OK
11:06:41 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works/eb13b431-caef-4ec3-83b2-453951b16a72
INFO:     127.0.0.1:53547 - "GET /api/v1/works/eb13b431-caef-4ec3-83b2-453951b16a72 HTTP/1.1" 200 OK
11:06:41 app.services.chapter_service INFO   [ChapterService] Querying chapters for work_id=eb13b431-caef-4ec3-83b2-453951b16a72, type=<class 'uuid.UUID'>
11:06:41 app.services.chapter_service INFO   [ChapterService] Found 0 chapters
11:06:41 app.api.v1.chapters INFO   [GET chapters] Returning 0 chapters
11:06:41 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/chapters/work/eb13b431-caef-4ec3-83b2-453951b16a72
11:06:42 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/locations
INFO:     127.0.0.1:52630 - "GET /api/v1/chapters/work/eb13b431-caef-4ec3-83b2-453951b16a72 HTTP/1.1" 200 OK
INFO:     127.0.0.1:53987 - "GET /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/locations HTTP/1.1" 200 OK
11:06:42 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works/eb13b431-caef-4ec3-83b2-453951b16a72
INFO:     127.0.0.1:53547 - "GET /api/v1/works/eb13b431-caef-4ec3-83b2-453951b16a72 HTTP/1.1" 200 OK
11:06:42 app.api.v1.chapters INFO   [GET chapters] work_id=eb13b431-caef-4ec3-83b2-453951b16a72, user_id=602f5147-846a-4cde-95d3-405fa75f133f
11:06:42 app.services.chapter_service INFO   [ChapterService] Querying chapters for work_id=eb13b431-caef-4ec3-83b2-453951b16a72, type=<class 'uuid.UUID'>
11:06:42 app.services.chapter_service INFO   [ChapterService] Found 0 chapters
11:06:42 app.api.v1.chapters INFO   [GET chapters] Returning 0 chapters
11:06:42 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/chapters/work/eb13b431-caef-4ec3-83b2-453951b16a72
11:06:42 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/locations
INFO:     127.0.0.1:55229 - "GET /api/v1/chapters/work/eb13b431-caef-4ec3-83b2-453951b16a72 HTTP/1.1" 200 OK
INFO:     127.0.0.1:52630 - "GET /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/locations HTTP/1.1" 200 OK
11:06:42 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/characters
INFO:     127.0.0.1:49495 - "GET /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/characters HTTP/1.1" 200 OK
11:06:42 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/ai-guidelines
INFO:     127.0.0.1:55237 - "GET /api/v1/worldview/works/eb13b431-caef-4ec3-83b2-453951b16a72/ai-guidelines HTTP/1.1" 200 OK
11:07:22 app.api.middleware.monitoring_middleware INFO   API请求完成: OPTIONS /api/v1/agent/chat/stream
INFO:     127.0.0.1:50386 - "OPTIONS /api/v1/agent/chat/stream HTTP/1.1" 200 OK
11:07:22 app.services.ai.prompts INFO   Prompts loaded successfully from D:\Java\ai_writer\backend\app\services\ai\prompts\default.json
11:07:22 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
11:07:22 app.services.ai.http_ai_service INFO   ModelSelector 已启用
11:07:22 app.services.agent.cost_tracker INFO   CostTracker 初始化完成, 持久化: False
11:07:22 app.services.ai.http_ai_service INFO   CostTracker 已启用
11:07:23 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
11:07:23 app.api.v1.agent INFO   [Chat Stream] Mode: react
11:07:23 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:50386 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
11:07:44 app.core.redis INFO   ✅ Redis connected: redis://localhost:6379/0
11:07:44 app.api.v1.agent INFO   [Session] 创建新会话归属: 2147a190-de66-49b9-b3c3-a8d9d1baf905 -> 602f5147-846a-4cde-95d3-405fa75f133f
11:07:44 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: react, Message: 第一章：琼林夜宴，天子疾      场景： 皇宫，琼林宴（新科进士的庆功宴）。      氛围： 古...
11:07:44 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
11:07:44 app.services.ai.http_ai_service INFO   ModelSelector 已启用
11:07:44 app.services.ai.http_ai_service INFO   CostTracker 已启用
11:07:46 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
11:07:46 chromadb.telemetry.product.posthog INFO   Anonymized telemetry enabled. See                     https://docs.trychroma.com/telemetry for more information.
11:07:46 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
11:07:54 app.services.context.vector_memory_store INFO   ✅ VectorMemoryStore初始化成功 | 目录=./data/chroma_db | 模型=paraphrase-multilingual-MiniLM-L12-v2 | 集合=user_memories
11:07:54 app.services.context.manager INFO   ✅ VectorMemoryStore 已初始化
11:07:54 app.services.context.manager INFO   ✅ ContextManager: 长期记忆已启用 (user_id=None)
11:07:54 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ ContextManager已初始化（长期记忆已启用）
成功加载模板: intent_classifier (版本 2.0.0)
成功加载模板: writing_agent (版本 2.0.0)
成功加载模板: planning_agent (版本 2.0.0)
成功加载模板: tool_agent (版本 2.0.0)
成功加载模板: query_agent (版本 2.0.0)
11:07:54 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ PromptManager已初始化
11:07:54 app.services.agent.langgraph_agent INFO   [LangGraph] 使用 HTTPAIService 模式（手动工具调用，绕过 Cloudflare）
11:08:15 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ Redis连接验证成功
11:08:15 app.services.agent.langgraph_agent INFO   [LangGraph] OK 使用 AsyncRedisSaver（redis://localhost:6379/0，TTL=7天）
11:08:15 app.services.agent.parallel_tool_node INFO   [ParallelToolNode] 初始化完成，最大并发数=5，并行安全工具=4个
11:08:15 app.api.v1.agent INFO   [Global Agent] 创建全局Agent实例，MemorySaver将在请求间共享
11:08:15 app.services.agent.langgraph_agent INFO   [LangGraph Stream] 开始流式执行: 第一章：琼林夜宴，天子疾      场景： 皇宫，琼林宴（新科进士的庆功宴）。      氛围： 古...
11:08:36 redisvl.index.index INFO   Index already exists, not overwriting.
11:08:36 redisvl.index.index INFO   Index already exists, not overwriting.
11:08:36 redisvl.index.index INFO   Index already exists, not overwriting.
11:08:36 langgraph.checkpoint.redis.aio INFO   Redis client is a standalone client
11:08:36 app.services.agent.langgraph_agent INFO   [LangGraph] AsyncRedisSaver索引创建成功
11:08:36 app.services.agent.langgraph_agent INFO   [Context] 设置用户ID: 602f5147-846a-4cde-95d3-405fa75f133f
11:08:36 app.services.context.monitoring_integration INFO   ✅ ContextManager监控收集器已初始化
11:08:36 app.services.context.store INFO   [ContextStore] Redis连接成功
11:08:57 app.services.context.manager INFO   [ContextManager] 创建新上下文: 2147a190-de66-49b9-b3c3-a8d9d1baf905
11:08:57 app.services.context.token_counter INFO   ✅ tiktoken初始化成功，模型: gpt-4
11:08:57 app.services.context.manager INFO   [ContextManager] Session 2147a190-de66-49b9-b3c3-a8d9d1baf905: 1179/8000 tokens
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  3.18it/s]
11:08:58 app.services.context.vector_memory_store INFO   🔍 检索记忆 | 查询='第一章：琼林夜宴，天子疾      场景： 皇宫，琼林宴（新...' | 用户=602f5147-846a-4cde-95d3-405fa75f133f | work_id=eb13b431-caef-4ec3-83b2-453951b16a72 | 找到=0条 | 阈值=0.3
11:08:58 app.services.context.manager INFO   🔍 检索长期记忆 | work_id=eb13b431-caef-4ec3-83b2-453951b16a72 | 查询='第一章：琼林夜宴，天子疾      场景： 皇宫，琼林宴（新...' | 找到=0条 | 阈值=0.3
11:08:58 app.services.context.monitoring_integration INFO   [Monitor] 上下文构建: 1条消息, 1179 tokens, 耗时 21732.78ms
11:08:58 app.services.agent.langgraph_agent INFO   [Context] 加载上下文: {'session_id': '2147a190-de66-49b9-b3c3-a8d9d1baf905', 'token_count': 1179, 'short_memory_size': 0, 'has_summary': False, 'compression_triggered': False, 'long_term_memories': 0, 'adaptive_budget_enabled': False, 'task_type': None}
11:08:58 app.services.agent.langgraph_agent INFO   [LangGraph] 使用隔离的thread_id: eb13b431-caef-4ec3-83b2-453951b16a72:2147a190-de66-49b9-b3c3-a8d9d1baf905 (work_id=eb13b431-caef-4ec3-83b2-453951b16a72, conversation_id=2147a190-de66-49b9-b3c3-a8d9d1baf905)
11:08:58 app.services.agent.progress_tracker INFO   [ProgressTracker] 初始化完成，使用动态节点追踪模式（根据实际执行的节点自动计算进度）
11:08:58 app.services.agent.langgraph_agent INFO   [ProgressTracker] 初始化完成，使用动态节点追踪模式
11:08:58 app.services.agent.langgraph_agent INFO   [LangGraph] 意图分类（规则识别）
11:08:58 app.services.agent.langgraph_agent INFO   [Intent] 规则识别结果: writing, 置信度: 0.90
11:08:58 app.services.agent.langgraph_agent INFO   [LangGraph] 路由到: writing
11:08:58 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: _route_intent
11:08:58 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: intent_classifier
11:08:58 app.services.agent.langgraph_agent INFO   [Stream Event] progress_event = {'type': 'progress', 'step': 'intent_analysis', 'description': '识别为：写作任务', 'node': 'intent_classifier', 'details': {'intent': 'writing'}, 'timestamp': '2025-11-13T11:08:58.463809', 'progress': 100.0, 'eta': 0, 'eta_display': '即将完成', 'eta_confidence': 'high', 'current_step': 3, 'total_steps': 3, 'step_description': '第 3/3 步', 'elapsed': 0.0}
11:08:58 app.services.agent.langgraph_agent INFO   [Stream Event] on_progress 回调已调用
11:08:58 app.api.v1.agent INFO   [SSE] 发送 progress 事件: step=intent_analysis, desc=识别为：写作任务
11:08:58 app.services.agent.actions.action_registry INFO   [ActionRegistry] 注册Action: echo (class=EchoAction, category=example)
11:08:58 app.services.agent.actions.action_registry INFO   [ActionRegistry] 注册Action: writing (class=WritingAction, category=content_creation)
11:08:58 app.services.agent.actions.action_registry INFO   [ActionRegistry] 注册Action: planning (class=PlanningAction, category=planning)
11:08:58 app.services.agent.actions.action_registry INFO   [ActionRegistry] 注册Action: analysis (class=AnalysisAction, category=analysis)
11:08:58 app.services.agent.actions.action_registry INFO   [ActionRegistry] 注册Action: stuck (class=StuckAction, category=writing_assistance)
11:08:58 app.services.agent.actions.action_registry INFO   [ActionRegistry] 注册Action: general_chat (class=GeneralChatAction, category=conversation)
11:08:58 app.services.agent.langgraph_agent INFO   [LangGraph] 处理写作请求（新架构）
11:08:58 Action.writing INFO   [writing] PromptManager已初始化
11:08:58 Action.writing INFO   [writing] work_id=eb13b431-caef-4ec3-83b2-453951b16a72, chapter_id=None, phase=None, chapter_num=None
11:08:58 Action.writing INFO   [writing] 提取到场景设定消息（长度：503）
11:08:58 Action.writing INFO   [writing] 共提取 1 条上下文消息
11:08:58 app.services.agent.langgraph_agent INFO   [LangGraph] WritingAction准备完成: phase=None, chapter_num=None
11:08:58 app.services.agent.langgraph_agent INFO   [LangGraph] 处理writing场景 (use_chatgpt=False)
11:08:58 app.core.cache INFO   ⚠️ 缓存未命中: prompt:get_tool_decision_static_prompt:fca6eb91156619d0
11:08:58 app.core.cache INFO   💾 缓存已保存: prompt:get_tool_decision_static_prompt:fca6eb91156619d0 (expire=3600s)
11:08:58 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
11:08:58 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
11:08:58 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=200, temp=0.3, task_type=TaskType.SIMPLE_QA
11:09:00 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/2 200 OK"
11:09:00 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:09:06 app.services.ai.http_ai_service INFO   API 响应完成，共接收 22 个数据块，总长度: 1427
11:09:06 app.services.ai.http_ai_service INFO   流式响应Token统计: 3669 (prompt=2622, completion=1047)
11:09:06 app.services.agent.cost_tracker INFO   [CostTracker] 记录API调用: gemini-2.5-pro, tokens: 2622+1047=3669, cost: $0.013747
11:09:06 app.services.ai.http_ai_service INFO   [CostTracker] API调用已记录: tokens=2622+1047, cost=$0.013747, time=7.70s
11:09:06 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=3669
11:09:06 app.services.agent.langgraph_agent INFO   [LangGraph] AI 决策原文: ```json
{
  "need_tools": true,
  "tool_name": "continue_writing_tool",
  "tool_args": {
    "prompt": "你是专业的网络小说作家Agent，专注于创作网文故事。\n\n请根据以下要求，创作小说第一章内容，字数约2000字。\n\n**章节标题**：第一章：琼林夜宴，天子疾\n\n**场景设定**：\n- **地点**：皇宫，琼林宴（新科进士的庆功宴）。\n- **时代背景**：古典宫廷（具体朝代不限，但需符合古典宫廷氛围）。\n- **氛围**：古典雅致，文采风流。宴会上诗词唱和，觥筹交错，表面繁华，实则暗流涌动，朝堂新贵与老臣之间弥漫着无形的较量与审视。\n\n**角色设定**：\n- **主角**：楚明楼，新科状元。初次踏入宫廷盛宴，成为全场焦点。他秉持儒家礼法，言行举止得体，内心怀有“以天下为己任”的理想主义情怀。初登场时，应展现其风采与稳重。\n- **配角**：皇帝（或太子，根据故事需要选择，此处暂定为皇帝），朝中老臣，新科进士，御医，以及一位关键的神秘老太监。\n\n**核心事件**：\n- **宴会高潮**：在宴会进行到高潮时，皇帝突然发病，症状类似“中风”或“癫狂”，口眼歪斜，言语不清，甚至可能出现失禁或暴躁等失态，令场面瞬间失控。\n- **御医束手无策**：宫廷御医上前诊治，却显得手足无措，束手无策，无法控制病情，加剧了恐慌气氛。\n\n**转折（玄幻元素引入）**：\n- **神秘老太监**：在众人惊慌失措之际，一名一直隐没在宫廷阴影中、毫不起眼的老太监（可设定为天一阁的凡间代理人，但初期不点明身份）缓步上前。\n- **施法**：他无视御医的存在和宫廷礼法，走到皇帝面前，仅以手指在空中虚空画出一道常人无法看见的复杂符咒（或微光轨迹）。\n- **治愈**：符咒（或微光）按向皇帝眉心，皇帝的症状瞬间消失，恢复如常，仿佛之前的病发只是幻觉。\n\n**结局与伏笔**：\n- **老太监退场**：老太监完成动作后，悄无声息地退回阴影之中，消失不见，仿佛从未出现过。\n- **朝堂寂静**：满朝文武被这离奇的一幕惊呆，无人敢发出质疑或议论，现场一片死寂。\n- **主角视角**：楚明楼作为离得较近且观察力敏锐的人，目睹了老太监施法的全过程。他看到了那道常人无法看见的、违背了“子不语怪力乱神”的圣人教诲的奇异微光（或符咒）。这一幕深深烙印在他心中，成为他日后探寻真相、怀疑现实的起点，心中悄然种下了一颗怀疑的种子。\n\n**写作要求**：\n- **风格**：保持古典、雅致的文风，同时融入网文的节奏感和代入感。\n- **描写**：细致描绘琼林宴的盛况、人物的对话神态、皇帝发病时的惊悚、御医的无能、老太监的神秘以及楚明楼的内心感受。\n- **节奏**：从宴会的风雅，到突发的惊变，再到玄幻的转折，最后以主角的疑虑和宫廷的寂静结束，节奏张弛有度。\n- **爽点**：老太监的神秘手段和瞬间治愈皇帝制造“反差爽”；主角目睹真相埋下“智斗/探索爽”的伏笔。\n- **人物**：初步展现楚明楼的儒雅、理想主义和敏锐观察力。\n- **细节**：强调楚明楼看到的“微光”或符咒，以及它如何违背常理，给主角留下深刻印象。\n- **字数**：约2000字。\n\n请开始创作第一章。"
  }
}
```
11:09:06 app.services.agent.langgraph_agent INFO   [LangGraph] 方法2成功: 正则提取 JSON
11:09:06 app.services.agent.langgraph_agent INFO   [LangGraph] 最终决策: {'need_tools': True, 'tool_name': 'continue_writing_tool', 'tool_args': {'prompt': '你是专业的网络小说作家Agent，专注于创作网文故事。\n\n请根据以下要求，创作小说第一章内容，字数约2000字。\n\n**章节标题**：第一章：琼林夜宴，天子疾\n\n**场景设定**：\n- **地点**：皇宫，琼林宴（新科进士的庆功宴）。\n- **时代背景**：古典宫廷（具体朝代不限，但需符合古典宫廷氛围）。\n- **氛围**：古典雅致，文采风流。宴会上诗词唱和，觥筹交错，表面繁华，实则暗流涌动，朝堂新贵与老臣之间弥漫着无形的较量与审视。\n\n**角色设定**：\n- **主角**：楚明楼，新科状元。初次踏入宫廷盛宴，成为全场焦点。他秉持儒家礼法，言行举止得体，内心怀有“以天下为己任”的理想主义情怀。初登场时，应展现其风采与稳重。\n- **配角**：皇帝（或太子，根据故事需要选择，此处暂定为皇帝），朝中老臣，新科进士，御医，以及一位关键的神秘老太监。\n\n**核心事件**：\n- **宴会高潮**：在宴会进行到高潮时，皇帝突然发病，症状类似“中风”或“癫狂”，口眼歪斜，言语不清，甚至可能出现失禁或暴躁等失态，令场面瞬间失控。\n- **御医束手无策**：宫廷御医上前诊治，却显得手足无措，束手无策，无法控制病情，加剧了恐慌气氛。\n\n**转折（玄幻元素引入）**：\n- **神秘老太监**：在众人惊慌失措之际，一名一直隐没在宫廷阴影中、毫不起眼的老太监（可设定为天一阁的凡间代理人，但初期不点明身份）缓步上前。\n- **施法**：他无视御医的存在和宫廷礼法，走到皇帝面前，仅以手指在空中虚空画出一道常人无法看见的复杂符咒（或微光轨迹）。\n- **治愈**：符咒（或微光）按向皇帝眉心，皇帝的症状瞬间消失，恢复如常，仿佛之前的病发只是幻觉。\n\n**结局与伏笔**：\n- **老太监退场**：老太监完成动作后，悄无声息地退回阴影之中，消失不见，仿佛从未出现过。\n- **朝堂寂静**：满朝文武被这离奇的一幕惊呆，无人敢发出质疑或议论，现场一片死寂。\n- **主角视角**：楚明楼作为离得较近且观察力敏锐的人，目睹了老太监施法的全过程。他看到了那道常人无法看见的、违背了“子不语怪力乱神”的圣人教诲的奇异微光（或符咒）。这一幕深深烙印在他心中，成为他日后探寻真相、怀疑现实的起点，心中悄然种下了一颗怀疑的种子。\n\n**写作要求**：\n- **风格**：保持古典、雅致的文风，同时融入网文的节奏感和代入感。\n- **描写**：细致描绘琼林宴的盛况、人物的对话神态、皇帝发病时的惊悚、御医的无能、老太监的神秘以及楚明楼的内心感受。\n- **节奏**：从宴会的风雅，到突发的惊变，再到玄幻的转折，最后以主角的疑虑和宫廷的寂静结束，节奏张弛有度。\n- **爽点**：老太监的神秘手段和瞬间治愈皇帝制造“反差爽”；主角目睹真相埋下“智斗/探索爽”的伏笔。\n- **人物**：初步展现楚明楼的儒雅、理想主义和敏锐观察力。\n- **细节**：强调楚明楼看到的“微光”或符咒，以及它如何违背常理，给主角留下深刻印象。\n- **字数**：约2000字。\n\n请开始创作第一章。'}}
11:09:06 app.services.agent.langgraph_agent INFO   [LangGraph] writing 决策 (HTTPAIService): True
11:09:06 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: complex
11:09:06 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=content_creation, 模型=gemini-2.5-pro, 原因=任务复杂度为 complex; 任务类型: content_creation; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
11:09:06 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.8, task_type=TaskType.CONTENT_CREATION
11:09:22 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/2 200 OK"
11:09:22 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:09:57 app.services.ai.http_ai_service INFO   API 响应完成，共接收 18 个数据块，总长度: 1356
11:09:57 app.services.ai.http_ai_service INFO   流式响应Token统计: 3593 (prompt=2497, completion=1096)
11:09:57 app.services.agent.cost_tracker INFO   [CostTracker] 记录API调用: gemini-2.5-pro, tokens: 2497+1096=3593, cost: $0.014081
11:09:57 app.services.ai.http_ai_service INFO   [CostTracker] API调用已记录: tokens=2497+1096, cost=$0.014081, time=51.36s
11:09:57 app.services.agent.langgraph_agent INFO   [LangGraph] writing - 处理工具执行结果 (HTTPAIService)
11:09:57 app.services.agent.langgraph_agent INFO   [LangGraph] 🔍 工具返回内容长度: 1356 字符
11:09:57 app.services.agent.langgraph_agent INFO   [LangGraph] 🔍 工具返回内容预览:
琼林宴上的丝竹声，不知何时已经停了。
死寂，如同三九寒冬的冰层，凝固了整座文华殿。方才还觥筹交错、诗酒风流的殿宇，此刻只剩下粗重的呼吸与心跳。金樽玉液倾洒在地，与名贵的波斯地毯交融，无人理会。新科进士们煞白的脸上，满是劫后余生的惊恐与茫然。而那些久历宦海的老臣，则个个垂首敛目，神情复杂，仿佛方寸之间已历经了无数惊涛骇浪。

御座之上，方才还目眦欲裂、举止癫狂的昭武帝，此刻已恢复了清明。他微微喘息着，明黄的龙袍上沾染了几滴酒渍，额角尚有冷汗。他抬手，看了看自己方才险些抓向近侍的手，眼中闪过一丝后怕与迷惘，随即被深沉的帝王威仪所掩盖。

“朕……偶感眩晕，如今已无碍。”昭武帝的声音略带沙哑，却依旧沉稳，他环视一周，目光在每一个噤若寒蝉的臣子脸上一一扫过，“众卿，继续宴饮。”

然而，无人敢动。
乐师不敢奏，舞姬不敢起，甚至连侍奉的宫人，都僵立原地，不敢发出一丝声响。那道退入阴影的苍老身影，如同一座无形的巨山，压在所有人的心头。那违背常理、近乎神迹的一幕，是比天子之怒更深沉的恐惧。

御座旁的内阁首辅李延年，颤巍巍地出列，俯身跪倒：“陛下龙体为重，今夜琼林宴已尽兴，臣等诚惶诚恐，恳请陛下还宫
11:09:57 app.services.agent.langgraph_agent INFO   [LangGraph] writing 最终响应使用模型: task_type=content_creation
11:09:57 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: complex
11:09:57 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=content_creation, 模型=gemini-2.5-pro, 原因=任务复杂度为 complex; 任务类型: content_creation; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
11:09:57 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=1500, temp=0.7, task_type=TaskType.CONTENT_CREATION
11:10:08 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/2 200 OK"
11:10:08 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:10:52 app.services.ai.http_ai_service INFO   API 响应完成，共接收 84 个数据块，总长度: 2607
11:10:52 app.services.ai.http_ai_service INFO   流式响应Token统计: 6675 (prompt=4630, completion=2045)
11:10:52 app.services.agent.cost_tracker INFO   [CostTracker] 记录API调用: gemini-2.5-pro, tokens: 4630+2045=6675, cost: $0.026237
11:10:52 app.services.ai.http_ai_service INFO   [CostTracker] API调用已记录: tokens=4630+2045, cost=$0.026237, time=54.46s
11:10:52 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=6675
11:10:52 app.services.agent.langgraph_agent INFO   [LangGraph] 无需工具调用，结束流程
11:10:52 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: _should_continue
11:10:52 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: writing_agent
11:10:52 app.services.agent.langgraph_agent INFO   [Stream Event] progress_event = {'type': 'progress', 'step': 'thinking', 'description': '正在思考如何帮助您...', 'node': 'writing_agent', 'details': {}, 'timestamp': '2025-11-13T11:10:52.014773', 'progress': 100.0, 'eta': 0, 'eta_display': '即将完成', 'eta_confidence': 'high', 'current_step': 5, 'total_steps': 5, 'step_description': '第 5/5 步', 'elapsed': 113.6}
11:10:52 app.api.v1.agent INFO   [Stream] Activity完成: intent_analysis (113.6s)
11:10:52 app.services.agent.langgraph_agent INFO   [Stream Event] on_progress 回调已调用
11:10:52 app.api.v1.agent INFO   [SSE] 发送 activity_complete 事件: step=intent_analysis, elapsed=113.6s
11:10:52 app.api.v1.agent INFO   [SSE] 发送 progress 事件: step=thinking, desc=正在思考如何帮助您...
11:10:52 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: LangGraph
11:10:52 app.services.agent.langgraph_agent INFO   [LangGraph Stream] 流式执行完成，共16个事件
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 20.75it/s]
11:10:52 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | work_id=eb13b431-caef-4ec3-83b2-453951b16a72 | 重要度=0.50 | 长度=372
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 19.76it/s]
11:10:52 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | work_id=eb13b431-caef-4ec3-83b2-453951b16a72 | 重要度=0.90 | 长度=2607
11:10:52 app.services.context.store INFO   [ContextStore] 保存上下文: 2147a190-de66-49b9-b3c3-a8d9d1baf905, token=4877
11:10:52 app.services.context.manager INFO   [ContextManager] 更新上下文: 2147a190-de66-49b9-b3c3-a8d9d1baf905, 消息数=2, Token=4877
11:10:52 app.services.agent.langgraph_agent INFO   [Context] 上下文已更新: 2147a190-de66-49b9-b3c3-a8d9d1baf905 (work_id=eb13b431-caef-4ec3-83b2-453951b16a72)
11:10:52 app.services.agent.progress_tracker INFO   [ProgressTracker] 状态已重置
11:10:52 app.api.v1.agent INFO   [Stream] 最后活动完成: thinking (0.5s)
11:10:52 app.api.v1.agent INFO   [SSE] 发送 activity_complete 事件: step=thinking, elapsed=0.5s
11:10:52 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: react, Stream completed
11:11:58 app.api.middleware.monitoring_middleware INFO   API请求完成: OPTIONS /api/v1/chapters
INFO:     127.0.0.1:53095 - "OPTIONS /api/v1/chapters HTTP/1.1" 200 OK
11:11:58 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/chapters
INFO:     127.0.0.1:53095 - "POST /api/v1/chapters HTTP/1.1" 201 Created
11:11:58 app.api.middleware.monitoring_middleware INFO   API请求完成: OPTIONS /api/v1/analysis/works/eb13b431-caef-4ec3-83b2-453951b16a72/start
INFO:     127.0.0.1:53095 - "OPTIONS /api/v1/analysis/works/eb13b431-caef-4ec3-83b2-453951b16a72/start HTTP/1.1" 200 OK
11:11:59 app.services.novel_analysis_service INFO   Created analysis task for work eb13b431-caef-4ec3-83b2-453951b16a72, total_chapters: 1
11:11:59 app.api.v1.novel_analysis INFO   User 602f5147-846a-4cde-95d3-405fa75f133f started analysis for work eb13b431-caef-4ec3-83b2-453951b16a72, analysis_id: 428408e4-2a19-4d2a-9dad-3ab9ba078c23
11:11:59 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/analysis/works/eb13b431-caef-4ec3-83b2-453951b16a72/start
INFO:     127.0.0.1:53095 - "POST /api/v1/analysis/works/eb13b431-caef-4ec3-83b2-453951b16a72/start HTTP/1.1" 201 Created
11:11:59 app.api.middleware.monitoring_middleware INFO   API请求完成: OPTIONS /api/v1/chapters/6c46612a-5d6f-4ad2-9310-7d8aac83e881
INFO:     127.0.0.1:53095 - "OPTIONS /api/v1/chapters/6c46612a-5d6f-4ad2-9310-7d8aac83e881 HTTP/1.1" 200 OK
11:11:59 app.api.v1.novel_analysis INFO   后台任务开始：分析作品 eb13b431-caef-4ec3-83b2-453951b16a72
11:11:59 app.api.middleware.monitoring_middleware INFO   API请求完成: OPTIONS /api/v1/chapters/6c46612a-5d6f-4ad2-9310-7d8aac83e881
INFO:     127.0.0.1:53095 - "OPTIONS /api/v1/chapters/6c46612a-5d6f-4ad2-9310-7d8aac83e881 HTTP/1.1" 200 OK
11:11:59 app.api.v1.novel_analysis INFO   后台任务已找到分析记录 analysis_id=428408e4-2a19-4d2a-9dad-3ab9ba078c23
11:11:59 app.services.ai.novel_analysis_orchestrator INFO   ============================================================
11:11:59 app.services.ai.novel_analysis_orchestrator INFO   开始分析作品: eb13b431-caef-4ec3-83b2-453951b16a72
11:11:59 app.services.ai.novel_analysis_orchestrator INFO   ============================================================
11:11:59 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/6c46612a-5d6f-4ad2-9310-7d8aac83e881
INFO:     127.0.0.1:53095 - "PUT /api/v1/chapters/6c46612a-5d6f-4ad2-9310-7d8aac83e881 HTTP/1.1" 200 OK
11:11:59 app.services.novel_analysis_service INFO   Updated analysis 428408e4-2a19-4d2a-9dad-3ab9ba078c23 progress: 0/1, stage: AnalysisStage.MICRO_ANALYSIS, status: AnalysisStatus.ANALYZING
11:11:59 app.services.ai.novel_analysis_orchestrator INFO   初始化AI分析服务...
11:11:59 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
11:11:59 app.services.ai.http_ai_service INFO   ModelSelector 已启用
11:11:59 app.services.ai.http_ai_service INFO   CostTracker 已启用
11:12:00 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
11:12:00 app.services.ai.novel_micro_analysis INFO   微观分析提示词加载成功
11:12:00 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
11:12:00 app.services.ai.http_ai_service INFO   ModelSelector 已启用
11:12:00 app.services.ai.http_ai_service INFO   CostTracker 已启用
11:12:02 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
11:12:02 app.services.ai.novel_macro_analysis INFO   宏观分析提示词加载成功
11:12:02 app.services.ai.novel_analysis_orchestrator INFO   共获取 1 个章节，开始微观分析...
11:12:02 app.services.ai.novel_analysis_orchestrator INFO   ⚡ 使用并行分析模式 (并发数: 5)
11:12:02 app.services.ai.novel_analysis_orchestrator INFO   ⚡ 启动 1 个并发分析任务...
11:12:02 app.services.ai.novel_analysis_orchestrator INFO   [1/1] 🔄 开始分析: 琼林夜宴，天子疾
11:12:02 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/6c46612a-5d6f-4ad2-9310-7d8aac83e881
INFO:     127.0.0.1:64090 - "PUT /api/v1/chapters/6c46612a-5d6f-4ad2-9310-7d8aac83e881 HTTP/1.1" 200 OK
11:12:10 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/6c46612a-5d6f-4ad2-9310-7d8aac83e881
INFO:     127.0.0.1:64466 - "PUT /api/v1/chapters/6c46612a-5d6f-4ad2-9310-7d8aac83e881 HTTP/1.1" 200 OK
11:12:10 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/6c46612a-5d6f-4ad2-9310-7d8aac83e881
INFO:     127.0.0.1:64794 - "PUT /api/v1/chapters/6c46612a-5d6f-4ad2-9310-7d8aac83e881 HTTP/1.1" 200 OK
11:12:12 app.services.redis_cache_service WARNING   ⚠️  Redis连接失败,缓存功能将禁用: Timeout connecting to server
11:12:12 app.services.ai.novel_micro_analysis INFO   开始AI分析章节: 6c46612a-5d6f-4ad2-9310-7d8aac83e881 - 琼林夜宴，天子疾
11:12:12 app.services.ai.novel_micro_analysis INFO   第 1/3 次尝试调用AI分析
11:12:12 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=4000, temp=0.3, task_type=None
11:12:15 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/2 200 OK"
11:12:15 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:12:18 app.api.middleware.monitoring_middleware INFO   API请求完成: OPTIONS /api/v1/ai/complete
INFO:     127.0.0.1:51716 - "OPTIONS /api/v1/ai/complete HTTP/1.1" 200 OK
11:12:18 app.api.v1.ai INFO   [AI续写] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), 上下文长度: 198, 风格: 默认
11:12:18 app.api.v1.ai INFO   [AI续写] context内容: '楚明楼的呼吸猛地一滞。 这个名字，他仿佛在某本早已被列为禁书的野史杂谈中见过一角，书中只说其是“掌天意，司人间”的神秘所在，语焉不详，被斥为无稽之谈。 可现在，这三个字就真实地握在他的手中。 木牌上，似乎还残留着一丝若有若无的、与他在文华殿中所见微光同源的气息。 他紧紧攥住木牌，粗糙的边缘硌得他掌心生疼。 去，还是不去？ 去，前方是万丈深渊，是他认知之外的、足以颠覆一切的未知。 不去，今夜的疑'
11:12:18 app.api.v1.ai INFO   [AI续写] prompt: '续写', max_tokens: 100
11:12:18 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
11:12:18 app.services.ai.http_ai_service INFO   ModelSelector 已启用
11:12:18 app.services.ai.http_ai_service INFO   CostTracker 已启用
11:12:20 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
11:12:20 app.services.ai.http_ai_service INFO   AI自动补全请求 - 上下文长度: 198
11:12:20 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=100, temp=0.7, task_type=None
11:12:20 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/complete
11:12:20 app.services.ai.http_ai_service INFO   API 响应完成，共接收 2 个数据块，总长度: 158
11:12:20 app.services.ai.http_ai_service INFO   流式响应Token统计: 1141 (prompt=1076, completion=65)
11:12:20 app.services.agent.cost_tracker INFO   [CostTracker] 记录API调用: gemini-2.5-pro, tokens: 1076+65=1141, cost: $0.001995
11:12:20 app.services.ai.http_ai_service INFO   [CostTracker] API调用已记录: tokens=1076+65, cost=$0.001995, time=7.98s
INFO:     127.0.0.1:56700 - "POST /api/v1/ai/complete HTTP/1.1" 200 OK
11:12:20 app.services.ai.novel_micro_analysis INFO   [Token记录] 微观分析: 1141 tokens (prompt=1076, completion=65), 成本=$0.001995, 耗时=7977ms
11:12:20 app.services.ai.novel_micro_analysis INFO   章节 6c46612a-5d6f-4ad2-9310-7d8aac83e881 分析成功，提取事件数: 0
11:12:20 app.services.ai.novel_analysis_orchestrator INFO   [1/1] ✓ 分析完成: 琼林夜宴，天子疾 (18.0秒)
11:12:20 app.services.ai.novel_analysis_orchestrator INFO   ⚡ 并行分析完成: 成功 1/1 章
11:12:20 app.services.ai.novel_analysis_orchestrator INFO   💾 开始批量保存 1 个分析结果...
11:12:20 app.services.novel_analysis_service INFO   Batch saved 1 micro results for analysis 428408e4-2a19-4d2a-9dad-3ab9ba078c23, total: 1
11:12:20 app.services.ai.novel_analysis_orchestrator INFO   ✅ 批量保存完成: 1 个结果
11:12:20 app.services.ai.novel_analysis_orchestrator INFO   🔍 开始批量存储向量...
11:12:20 app.services.vector_store_service INFO   开始向量化章节 6c46612a-5d6f-4ad2-9310-7d8aac83e881 的微观分析数据
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 11.48it/s]
11:12:20 app.services.vector_store_service INFO   生成向量维度: 384
11:12:20 app.services.vector_store_service INFO   向量存储成功: vector_id=287e3030-c7d4-43d8-802f-f367fdb2f26d
11:12:20 app.services.ai.novel_analysis_orchestrator INFO   ✅ 批量向量存储完成
11:12:20 app.services.ai.novel_analysis_orchestrator INFO   ============================================================
11:12:20 app.services.ai.novel_analysis_orchestrator INFO   微观分析完成统计:
11:12:20 app.services.ai.novel_analysis_orchestrator INFO     成功: 1/1 章节 (100.0%)
11:12:20 app.services.ai.novel_analysis_orchestrator INFO     失败: 0 章节
11:12:20 app.services.ai.novel_analysis_orchestrator INFO     总耗时: 21.0秒 (平均 21.0秒/章)
11:12:20 app.services.ai.novel_analysis_orchestrator INFO   ============================================================
11:12:20 app.services.novel_analysis_service INFO   Updated analysis 428408e4-2a19-4d2a-9dad-3ab9ba078c23 progress: 1/1, stage: AnalysisStage.MACRO_ANALYSIS, status: None
11:12:20 app.services.ai.novel_analysis_orchestrator INFO   ============================================================
11:12:20 app.services.ai.novel_analysis_orchestrator INFO   开始宏观分析...
11:12:20 app.services.ai.novel_analysis_orchestrator INFO   ============================================================
11:12:20 app.services.ai.novel_macro_analysis INFO   开始宏观分析，共 1 个章节的数据
11:12:20 app.services.ai.novel_macro_analysis INFO   第 1/3 次尝试调用AI宏观分析
11:12:20 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=6000, temp=0.5, task_type=None
11:12:24 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/2 200 OK"
11:12:24 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:12:24 app.services.ai.http_ai_service INFO   API 响应完成，共接收 2 个数据块，总长度: 16
11:12:24 app.services.ai.http_ai_service INFO   流式响应Token统计: 287 (prompt=273, completion=14)
11:12:24 app.services.agent.cost_tracker INFO   [CostTracker] 记录API调用: gemini-2.5-pro, tokens: 273+14=287, cost: $0.000481
11:12:24 app.services.ai.http_ai_service INFO   [CostTracker] API调用已记录: tokens=273+14, cost=$0.000481, time=4.97s
11:12:25 app.services.ai.ai_log_middleware INFO   AI调用日志已记录: operation=continue, tokens=128, cost=$0.000239, duration=4973ms, success=True
11:12:25 app.api.v1.ai INFO   [AI续写] 用户 testuser_new-1 请求完成，生成字数: 16
11:12:28 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/2 200 OK"
11:12:28 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:12:36 app.services.ai.http_ai_service INFO   API 响应完成，共接收 8 个数据块，总长度: 306
11:12:36 app.services.ai.http_ai_service INFO   流式响应Token统计: 1741 (prompt=1562, completion=179)
11:12:36 app.services.agent.cost_tracker INFO   [CostTracker] 记录API调用: gemini-2.5-pro, tokens: 1562+179=1741, cost: $0.003743
11:12:36 app.services.ai.http_ai_service INFO   [CostTracker] API调用已记录: tokens=1562+179, cost=$0.003743, time=16.46s
11:12:36 app.services.ai.novel_macro_analysis INFO   [Token记录] 宏观分析: 1741 tokens (prompt=1562, completion=179), 成本=$0.003743, 耗时=16459ms
11:12:36 app.services.ai.novel_macro_analysis INFO   宏观分析完成，报告长度: 306 字符
11:12:36 app.services.ai.novel_macro_analysis WARNING   报告长度过短: 306 字符
11:12:36 app.services.ai.novel_macro_analysis WARNING   第 1 次尝试：报告格式验证失败
11:12:36 app.services.ai.novel_macro_analysis INFO   第 2/3 次尝试调用AI宏观分析
11:12:36 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=6000, temp=0.5, task_type=None
11:12:40 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/2 200 OK"
11:12:40 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:12:45 app.api.v1.ai INFO   [AI续写] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), 上下文长度: 197, 风格: 默认
11:12:45 app.api.v1.ai INFO   [AI续写] context内容: '殿中所见微光同源的气息。 他紧紧攥住木牌，粗糙的边缘硌得他掌心生疼。 去，还是不去？ 去，前方是万丈深渊，是他认知之外的、足以颠覆一切的未知。 不去，今夜的疑问将永远成为他心中的一根毒刺，让他终生寝食难安。 “格物，致知……”楚明楼低声念着圣人教诲。 真正的儒者，不应畏惧未知，而应探求世间万物的真理。 他的眼中，迷茫与恐惧渐渐褪去，取而代之的，是一种前所未有的坚定与锐利。 他将木牌收入袖中，'
11:12:45 app.api.v1.ai INFO   [AI续写] prompt: '续写', max_tokens: 100
11:12:45 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
11:12:45 app.services.ai.http_ai_service INFO   ModelSelector 已启用
11:12:45 app.services.ai.http_ai_service INFO   CostTracker 已启用
11:12:46 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
11:12:46 app.services.ai.http_ai_service INFO   AI自动补全请求 - 上下文长度: 197
11:12:46 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=100, temp=0.7, task_type=None
11:12:46 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/complete
INFO:     127.0.0.1:50676 - "POST /api/v1/ai/complete HTTP/1.1" 200 OK
11:12:49 app.services.ai.http_ai_service INFO   API 响应完成，共接收 3 个数据块，总长度: 301
11:12:49 app.services.ai.http_ai_service INFO   流式响应Token统计: 1779 (prompt=1593, completion=186)
11:12:49 app.services.agent.cost_tracker INFO   [CostTracker] 记录API调用: gemini-2.5-pro, tokens: 1593+186=1779, cost: $0.003851
11:12:49 app.services.ai.http_ai_service INFO   [CostTracker] API调用已记录: tokens=1593+186, cost=$0.003851, time=12.48s
11:12:49 app.services.ai.novel_macro_analysis INFO   [Token记录] 宏观分析: 1779 tokens (prompt=1593, completion=186), 成本=$0.003851, 耗时=12485ms
11:12:49 app.services.ai.novel_macro_analysis INFO   宏观分析完成，报告长度: 301 字符
11:12:49 app.services.ai.novel_macro_analysis WARNING   报告长度过短: 301 字符
11:12:49 app.services.ai.novel_macro_analysis WARNING   第 2 次尝试：报告格式验证失败
11:12:49 app.services.ai.novel_macro_analysis INFO   第 3/3 次尝试调用AI宏观分析
11:12:49 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=6000, temp=0.5, task_type=None
11:12:49 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/2 200 OK"
11:12:49 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:12:49 app.services.ai.http_ai_service INFO   API 响应完成，共接收 2 个数据块，总长度: 18
11:12:49 app.services.ai.http_ai_service INFO   流式响应Token统计: 280 (prompt=265, completion=15)
11:12:49 app.services.agent.cost_tracker INFO   [CostTracker] 记录API调用: gemini-2.5-pro, tokens: 265+15=280, cost: $0.000481
11:12:49 app.services.ai.http_ai_service INFO   [CostTracker] API调用已记录: tokens=265+15, cost=$0.000481, time=3.17s
11:12:49 app.services.ai.ai_log_middleware INFO   AI调用日志已记录: operation=continue, tokens=128, cost=$0.000256, duration=3169ms, success=True
11:12:49 app.api.v1.ai INFO   [AI续写] 用户 testuser_new-1 请求完成，生成字数: 18
11:12:52 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/2 200 OK"
11:12:52 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:12:59 app.services.ai.http_ai_service INFO   API 响应完成，共接收 4 个数据块，总长度: 322
11:12:59 app.services.ai.http_ai_service INFO   流式响应Token统计: 1749 (prompt=1535, completion=214)
11:12:59 app.services.agent.cost_tracker INFO   [CostTracker] 记录API调用: gemini-2.5-pro, tokens: 1535+214=1749, cost: $0.004059
11:12:59 app.services.ai.http_ai_service INFO   [CostTracker] API调用已记录: tokens=1535+214, cost=$0.004059, time=10.66s
11:12:59 app.services.ai.novel_macro_analysis INFO   [Token记录] 宏观分析: 1749 tokens (prompt=1535, completion=214), 成本=$0.004059, 耗时=10658ms
11:12:59 app.services.ai.novel_macro_analysis INFO   宏观分析完成，报告长度: 322 字符
11:12:59 app.services.ai.novel_macro_analysis WARNING   报告长度过短: 322 字符
11:12:59 app.services.ai.novel_macro_analysis WARNING   第 3 次尝试：报告格式验证失败
11:12:59 app.services.ai.novel_macro_analysis WARNING   宏观分析报告格式不完全符合预期，但仍然返回
11:12:59 app.services.ai.novel_analysis_orchestrator INFO   宏观分析完成，报告长度: 322 字符，耗时: 39.6秒
11:12:59 app.services.novel_analysis_service INFO   Saved macro result for analysis 428408e4-2a19-4d2a-9dad-3ab9ba078c23, marked as completed
11:12:59 app.services.ai.novel_analysis_orchestrator INFO   ============================================================
11:12:59 app.services.ai.novel_analysis_orchestrator INFO   作品 eb13b431-caef-4ec3-83b2-453951b16a72 分析全部完成！
11:12:59 app.services.ai.novel_analysis_orchestrator INFO   ============================================================
11:12:59 app.services.ai.novel_analysis_orchestrator INFO   📊 分析统计:
11:12:59 app.services.ai.novel_analysis_orchestrator INFO     微观分析: 1/1 章 (成功率 100.0%)
11:12:59 app.services.ai.novel_analysis_orchestrator INFO     宏观报告: 322 字符
11:12:59 app.services.ai.novel_analysis_orchestrator INFO     总耗时: 60.6秒 (1.0分钟)
11:12:59 app.services.ai.novel_analysis_orchestrator INFO     平均速度: 60.6秒/章
11:12:59 app.services.ai.novel_analysis_orchestrator INFO     向量存储: 1 条，覆盖 1 章
11:12:59 app.services.ai.novel_analysis_orchestrator INFO   ============================================================
11:12:59 app.services.ai.novel_analysis_orchestrator INFO   AI服务资源已清理
11:12:59 app.services.ai.novel_analysis_orchestrator INFO   AI服务资源已清理
11:12:59 app.api.v1.novel_analysis INFO   后台任务完成：作品 eb13b431-caef-4ec3-83b2-453951b16a72 分析成功
11:13:09 app.api.v1.ai INFO   [AI续写] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), 上下文长度: 196, 风格: 默认
11:13:09 app.api.v1.ai INFO   [AI续写] context内容: ' 可现在，这三个字就真实地握在他的手中。 木牌上，似乎还残留着一丝若有若无的、与他在文华殿中所见微光同源的气息。 他紧紧攥住木牌，粗糙的边缘硌得他掌心生疼。 去，还是不去？ 去，前方是万丈深渊，是他认知之外的、足以颠覆一切的未知。 不去，今夜的疑问将永远成为他心中的一根毒刺，让他终生寝食难安。 “格物，致知……”楚明楼低声念着圣人教诲。 真正的儒者，不应畏惧未知，而应探求世间万物的真理。 '
11:13:09 app.api.v1.ai INFO   [AI续写] prompt: '续写', max_tokens: 100
11:13:09 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
11:13:09 app.services.ai.http_ai_service INFO   ModelSelector 已启用
11:13:09 app.services.ai.http_ai_service INFO   CostTracker 已启用
11:13:10 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
11:13:10 app.services.ai.http_ai_service INFO   AI自动补全请求 - 上下文长度: 196
11:13:10 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=100, temp=0.7, task_type=None
11:13:10 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/complete
INFO:     127.0.0.1:49989 - "POST /api/v1/ai/complete HTTP/1.1" 200 OK
11:13:13 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/2 200 OK"
11:13:13 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:13:26 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
11:13:26 app.services.ai.http_ai_service INFO   ModelSelector 已启用
11:13:26 app.services.ai.http_ai_service INFO   CostTracker 已启用
11:13:28 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
11:13:28 app.api.v1.agent INFO   [Chat Stream] Mode: react
11:13:28 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:59665 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
11:13:28 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: react, Message: 第二章：翰林寻秘，怪力乱神      场景： 翰林院书库（或皇家秘阁），深夜。      动机： 楚...
11:13:28 app.services.agent.langgraph_agent INFO   [LangGraph Stream] 开始流式执行: 第二章：翰林寻秘，怪力乱神      场景： 翰林院书库（或皇家秘阁），深夜。      动机： 楚...
11:13:28 app.services.agent.langgraph_agent INFO   [Context] 设置用户ID: 602f5147-846a-4cde-95d3-405fa75f133f
11:13:28 app.services.context.store INFO   [ContextStore] 加载上下文: 2147a190-de66-49b9-b3c3-a8d9d1baf905, 2条消息
11:13:28 app.services.context.manager INFO   [ContextManager] Session 2147a190-de66-49b9-b3c3-a8d9d1baf905: 4877/8000 tokens
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  7.05it/s]
11:13:28 app.services.context.vector_memory_store INFO   🔍 检索记忆 | 查询='第二章：翰林寻秘，怪力乱神      场景： 翰林院书库（或...' | 用户=602f5147-846a-4cde-95d3-405fa75f133f | work_id=eb13b431-caef-4ec3-83b2-453951b16a72 | 找到=2条 | 阈值=0.3
11:13:28 app.services.context.manager INFO   🔍 检索长期记忆 | work_id=eb13b431-caef-4ec3-83b2-453951b16a72 | 查询='第二章：翰林寻秘，怪力乱神      场景： 翰林院书库（或...' | 找到=2条 | 阈值=0.3
11:13:28 app.services.context.monitoring_integration INFO   [Monitor] 上下文构建: 4条消息, 4877 tokens, 耗时 160.96ms
11:13:28 app.services.agent.langgraph_agent INFO   [Context] 加载上下文: {'session_id': '2147a190-de66-49b9-b3c3-a8d9d1baf905', 'token_count': 4877, 'short_memory_size': 2, 'has_summary': False, 'compression_triggered': False, 'long_term_memories': 2, 'adaptive_budget_enabled': False, 'task_type': None}
11:13:28 app.services.agent.langgraph_agent INFO   [LangGraph] 使用隔离的thread_id: eb13b431-caef-4ec3-83b2-453951b16a72:2147a190-de66-49b9-b3c3-a8d9d1baf905 (work_id=eb13b431-caef-4ec3-83b2-453951b16a72, conversation_id=2147a190-de66-49b9-b3c3-a8d9d1baf905)
11:13:28 app.services.agent.progress_tracker INFO   [ProgressTracker] 初始化完成，使用动态节点追踪模式（根据实际执行的节点自动计算进度）
11:13:28 app.services.agent.langgraph_agent INFO   [ProgressTracker] 初始化完成，使用动态节点追踪模式
11:13:28 app.services.agent.langgraph_agent INFO   [LangGraph] 意图分类（规则识别）
11:13:28 app.services.agent.langgraph_agent INFO   [Intent] 规则识别结果: writing, 置信度: 0.90
11:13:28 app.services.agent.langgraph_agent INFO   [LangGraph] 路由到: writing
11:13:28 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: _route_intent
11:13:28 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: intent_classifier
11:13:28 app.services.agent.langgraph_agent INFO   [Stream Event] progress_event = {'type': 'progress', 'step': 'intent_analysis', 'description': '识别为：写作任务', 'node': 'intent_classifier', 'details': {'intent': 'writing'}, 'timestamp': '2025-11-13T11:13:28.481622', 'progress': 100.0, 'eta': 0, 'eta_display': '即将完成', 'eta_confidence': 'high', 'current_step': 3, 'total_steps': 3, 'step_description': '第 3/3 步', 'elapsed': 0.0}
11:13:28 app.services.agent.langgraph_agent INFO   [Stream Event] on_progress 回调已调用
11:13:28 app.api.v1.agent INFO   [SSE] 发送 progress 事件: step=intent_analysis, desc=识别为：写作任务
11:13:28 app.services.agent.langgraph_agent INFO   [LangGraph] 处理写作请求（新架构）
11:13:28 Action.writing INFO   [writing] PromptManager已初始化
11:13:28 Action.writing INFO   [writing] work_id=eb13b431-caef-4ec3-83b2-453951b16a72, chapter_id=6c46612a-5d6f-4ad2-9310-7d8aac83e881, phase=None, chapter_num=None
11:13:28 Action.writing INFO   [writing] 提取到场景设定消息（长度：503）
11:13:28 Action.writing INFO   [writing] 提取到场景设定消息（长度：372）
11:13:28 Action.writing INFO   [writing] 提取到场景设定消息（长度：503）
11:13:28 Action.writing INFO   [writing] 提取到场景设定消息（长度：503）
11:13:28 Action.writing INFO   [writing] 提取到场景设定消息（长度：467）
11:13:28 Action.writing INFO   [writing] 提取到场景设定消息（长度：372）
11:13:28 Action.writing INFO   [writing] 提取到场景设定消息（长度：503）
11:13:28 Action.writing INFO   [writing] 共提取 7 条上下文消息
11:13:28 app.services.agent.langgraph_agent INFO   [LangGraph] WritingAction准备完成: phase=None, chapter_num=None
11:13:28 app.services.agent.langgraph_agent INFO   [LangGraph] 处理writing场景 (use_chatgpt=False)
11:13:28 app.core.cache INFO   ✅ 缓存命中: prompt:get_tool_decision_static_prompt:fca6eb91156619d0
11:13:28 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
11:13:28 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
11:13:28 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=200, temp=0.3, task_type=TaskType.SIMPLE_QA
11:13:31 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/2 200 OK"
11:13:31 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:13:37 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 28
11:13:37 app.services.ai.http_ai_service INFO   流式响应Token统计: 3021 (prompt=3003, completion=18)
11:13:37 app.services.agent.cost_tracker INFO   [CostTracker] 记录API调用: gemini-2.5-pro, tokens: 3003+18=3021, cost: $0.003934
11:13:37 app.services.ai.http_ai_service INFO   [CostTracker] API调用已记录: tokens=3003+18, cost=$0.003934, time=26.73s
11:13:37 app.services.ai.ai_log_middleware INFO   AI调用日志已记录: operation=continue, tokens=133, cost=$0.000315, duration=26733ms, success=True
11:13:37 app.api.v1.ai INFO   [AI续写] 用户 testuser_new-1 请求完成，生成字数: 28
11:13:44 app.api.v1.ai INFO   [AI续写] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), 上下文长度: 196, 风格: 默认
11:13:44 app.api.v1.ai INFO   [AI续写] context内容: ' 可现在，这三个字就真实地握在他的手中。 木牌上，似乎还残留着一丝若有若无的、与他在文华殿中所见微光同源的气息。 他紧紧攥住木牌，粗糙的边缘硌得他掌心生疼。 去，还是不去？ 去，前方是万丈深渊，是他认知之外的、足以颠覆一切的未知。 不去，今夜的疑问将永远成为他心中的一根毒刺，让他终生寝食难安。 “格物，致知……”楚明楼低声念着圣人教诲。 真正的儒者，不应畏惧未知，而应探求世间万物的真理。 '
11:13:44 app.api.v1.ai INFO   [AI续写] prompt: '续写', max_tokens: 100
11:13:44 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
11:13:44 app.services.ai.http_ai_service INFO   ModelSelector 已启用
11:13:44 app.services.ai.http_ai_service INFO   CostTracker 已启用
11:13:45 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
11:13:45 app.services.ai.http_ai_service INFO   AI自动补全请求 - 上下文长度: 196
11:13:45 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=100, temp=0.7, task_type=None
11:13:45 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/complete
INFO:     127.0.0.1:58006 - "POST /api/v1/ai/complete HTTP/1.1" 200 OK
11:13:47 app.services.ai.http_ai_service INFO   API 响应完成，共接收 34 个数据块，总长度: 2775
11:13:47 app.services.ai.http_ai_service INFO   流式响应Token统计: 7253 (prompt=5102, completion=2151)
11:13:47 app.services.agent.cost_tracker INFO   [CostTracker] 记录API调用: gemini-2.5-pro, tokens: 5102+2151=7253, cost: $0.027888
11:13:47 app.services.ai.http_ai_service INFO   [CostTracker] API调用已记录: tokens=5102+2151, cost=$0.027888, time=19.00s
11:13:47 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=7253
11:13:47 app.services.agent.langgraph_agent INFO   [LangGraph] AI 决策原文: {
    "need_tools": false,
    "direct_response": "## 第二章：翰林寻秘，怪力乱神\n\n月华依旧清冷，但此刻已无暇欣赏。宫门外的喧嚣散尽，留下的是楚明楼心中越发沉重的寂静。刚才那一幕，如同一根刺，深深扎入他以“格物致知”为根基的认知体系中。\n\n皇帝的癫狂，老太监的虚空画符，那道转瞬即逝却又无比真实的光芒……这一切都与他所学的圣贤之道格格不入。儒家讲究“子不语怪力乱神”，讲究实事求是，可他亲眼所见，却偏偏是“怪力乱神”。\n\n“气血不畅？”温庭筠的解释在耳边回响，显得如此苍白无力。若真是气血不畅，又怎会有那般形销骨立般的癫狂？又怎会瞬间恢复？那老太监的手法，绝非凡俗医术所能比拟，甚至……不像是人力所能及。\n\n“那道微光……”楚明楼攥紧了拳头，指节因用力而泛白。他确信自己看到了，那并非幻觉。那光芒蕴含着一种难以言喻的力量，瞬间驱散了笼罩在皇帝身上的诡异状态。\n\n“那老太监是谁？他又是何来历？”\n\n“天一阁的凡间代理？”这个念头刚一闪过，就被楚明楼自己否定了。天一阁乃是皇家藏书之地，阁中老者多是学究天人、皓首穷经之辈，绝无可能涉及这等……近乎妖术的手段。\n\n可若非天一阁，那又是谁？宫中何时藏匿了如此神秘的人物？\n\n他与赵子昂、温庭筠道别，脚步却并未放缓。状元府邸就在不远处，但此刻他无心归去。脑海中不断回放着宫宴上的惊险一幕，以及那老太监的身影。\n\n“不行，我必须弄清楚。”\n\n作为翰林院修撰，他拥有进入皇家藏书阁的权限，尤其是存放一些“前朝秘辛”和“禁书”的丙字库。那里存放着许多不为外人所知的典籍，或许……或许能找到一些蛛丝马迹。\n\n“格物致知，穷理于事，方能明辨是非。”楚明楼默念着书中的教诲，心中燃起一股莫名的冲动。他不能让这疑虑压在心头，更不能让这种“怪力乱神”之事，成为悬在大晏王朝头顶的利剑。\n\n夜色渐深，皇城内逐渐安静下来。楚明楼借着月光，悄然离开了同僚的视线，转身朝着翰林院的方向行去。他的身影融入夜色，如同一个潜行的刺客，目标直指那座存放着无数秘密的古老建筑。\n\n翰林院，深夜。\n\n寂静无声，只有偶尔传来的夜枭啼鸣，更添了几分森然。\n\n楚明楼凭借着翰林修撰的身份令牌，避开了值夜的禁卫，熟门熟路地来到了存放禁书的丙字库。\n\n丙字库的大门由沉重的乌木制成，门上绘着古朴的符文，散发着冰冷的气息。这里存放的，大多是皇家认为不宜公开流传的典籍，或是被认为过于偏僻、怪诞的记载。\n\n他深吸一口气，推开了厚重的大门。一股混合着陈腐纸张、灰尘和墨香的气息扑面而来，仿佛将他带入了另一个时空。\n\n库房内，书架高耸入顶，密密麻麻的书卷层叠摆放，在昏暗的光线下投下巨大的阴影。楚明楼点亮了一盏宫灯，微弱的灯火驱散了部分黑暗，却也让阴影更加摇曳，如同鬼魅。\n\n他心中默念着“心正身直”，开始在书架间搜寻。\n\n“异闻录……地理志……前朝秘史……”\n\n他的目光快速扫过一卷卷书脊上的标题，手指轻轻拂过布满灰尘的封面。他知道，自己要找的，并非是那些广为流传的史书，而是那些被遗忘在角落，甚至可能被列为禁忌的记载。\n\n时间一分一秒地过去，宫灯里的灯油在缓缓减少。楚明楼的心也渐渐沉了下去，难道，真的只是自己看错了？或者，那件事，根本就不是人力所能解释，也无法在任何史料中找到答案？\n\n就在他准备放弃，离开这个令人窒息的地方时，他的目光无意间扫过了一个角落。\n\n那里，一本残破的书卷被随意地丢弃在一旁，似乎是被遗忘了很久。\n\n书名已经模糊不清，只隐约可见“大晏异闻录”几个字样，但字体古老，与如今通行的写法已有差异。书页泛黄，边缘卷曲，甚至有几处明显的虫蛀痕迹，仿佛随时会化为飞灰。\n\n“《大晏异闻录》……”楚明楼心中一动，这似乎与他最初的猜测不谋而合。\n\n他小心翼翼地将书取下，捧在手中。书页散发出一种奇异的、混合着霉味和淡淡药草香的气息。\n\n他盘膝坐下，将宫灯放在身侧，开始翻阅。\n\n书中的记载，果然如他所料，并未涉及什么长生不老、呼风唤雨的仙法。更多的是一些零散的、关于历代王朝的奇闻异事，以及一些模糊的记载。\n\n“……景兴年间，宫中曾有方士，以奇术蛊惑圣心，后被贬斥……”\n\n“……元和朝，边关告急，朝廷命术士占卜吉凶，竟引来妖邪作祟……”\n\n“……太祖皇帝曾言，国之兴衰，非仅系于兵戈民心，亦关乎……”\n\n楚明楼的心跳开始加速。这些零散的记载，虽然语焉不详，却指向了一个共同的模糊概念——“方士”以及他们对朝政的影响。\n\n“方士……他们究竟是何许人也？”\n\n他继续向下翻阅，目光落在其中一段模糊的记载上：\n\n“……夫天地之间，气有浩然，正气存内，邪不可干。方术诡谲，惑人心智，唯‘浩然正气’可御之……”\n\n“浩然正气……”\n\n这四个字，如同惊雷般在楚明楼的脑海中炸响。这是他从小熟读的儒家经典中的概念，是孟子所言的“吾善养吾浩然之气”。\n\n他一直以为，这只是修身养性的道德说辞，是精神层面的追求。\n\n可现在，这本书却明确指出，这“浩然正气”，竟然是抵御“方术”的关键？\n\n就在他读到此处时，他惊讶地发现，手中这本残破的《大晏异闻录》的书页上，一个原本模糊不清的古老印记，突然散发出了一道微弱的、几乎难以察觉的淡金色光芒。\n\n那光芒一闪即逝，仿佛只是灯火的折射。但楚明楼知道，那绝对不是错觉。\n\n那个印记……它在回应“浩然正气”这几个字？\n\n一股寒意从脚底升起，瞬间蔓延至全身。他猛地抬起头，环顾四周阴森的库房，感觉自己仿佛闯入了一个巨大而古老的阴谋之中。\n\n皇帝的怪病，老太监的神秘手段，以及这本记载着“方士”和“气运”的禁书……\n\n这一切，都指向了一个他从未想象过的、隐藏在大晏王朝光鲜外表之下的黑暗秘密。\n\n他，楚明楼，一个坚信圣贤之道的读书人，似乎无意间，触碰到了皇室最深层的禁忌。\n\n……\n\n与此同时，京城另一处不起眼的角落。\n\n一座古朴的宅院内，烛火摇曳。\n\n一个身着道袍的老者，正全神贯注地盯着桌上一个布满复杂纹路的铜盘。\n\n铜盘中央，一根细长的指针，正随着某种无形的力量微微颤动。\n\n突然，指针猛地一顿，然后，极其轻微地，朝着一个方向偏转了过去。\n\n老者浑浊的眼睛微微眯起，顺着指针的方向望去，口中喃喃自语：“嗯？翰林院……有异动？”\n\n他的手指轻轻抚过铜盘边缘的刻纹，空气中弥漫着一股淡淡的、如同檀香般的奇异气味。\n\n“气运……果然有所感应……”\n\n老者眼中闪过一丝不易察觉的光芒，随即又隐没下去，仿佛什么都没有发生过。\n\n夜，依旧深沉。"
}
11:13:47 app.services.agent.langgraph_agent INFO   [LangGraph] 方法1成功: 直接解析整个文本
11:13:47 app.services.agent.langgraph_agent INFO   [LangGraph] 最终决策: {'need_tools': False, 'direct_response': '## 第二章：翰林寻秘，怪力乱神\n\n月华依旧清冷，但此刻已无暇欣赏。宫门外的喧嚣散尽，留下的是楚明楼心中越发沉重的寂静。刚才那一幕，如同一根刺，深深扎入他以“格物致知”为根基的认知体系中。\n\n皇帝的癫狂，老太监的虚空画符，那道转瞬即逝却又无比真实的光芒……这一切都与他所学的圣贤之道格格不入。儒家讲究“子不语怪力乱神”，讲究实事求是，可他亲眼所见，却偏偏是“怪力乱神”。\n\n“气血不畅？”温庭筠的解释在耳边回响，显得如此苍白无力。若真是气血不畅，又怎会有那般形销骨立般的癫狂？又怎会瞬间恢复？那老太监的手法，绝非凡俗医术所能比拟，甚至……不像是人力所能及。\n\n“那道微光……”楚明楼攥紧了拳头，指节因用力而泛白。他确信自己看到了，那并非幻觉。那光芒蕴含着一种难以言喻的力量，瞬间驱散了笼罩在皇帝身上的诡异状态。\n\n“那老太监是谁？他又是何来历？”\n\n“天一阁的凡间代理？”这个念头刚一闪过，就被楚明楼自己否定了。天一阁乃是皇家藏书之地，阁中老者多是学究天人、皓首穷经之辈，绝无可能涉及这等……近乎妖术的手段。\n\n可若非天一阁，那又是谁？宫中何时藏匿了如此神秘的人物？\n\n他与赵子昂、温庭筠道别，脚步却并未放缓。状元府邸就在不远处，但此刻他无心归去。脑海中不断回放着宫宴上的惊险一幕，以及那老太监的身影。\n\n“不行，我必须弄清楚。”\n\n作为翰林院修撰，他拥有进入皇家藏书阁的权限，尤其是存放一些“前朝秘辛”和“禁书”的丙字库。那里存放着许多不为外人所知的典籍，或许……或许能找到一些蛛丝马迹。\n\n“格物致知，穷理于事，方能明辨是非。”楚明楼默念着书中的教诲，心中燃起一股莫名的冲动。他不能让这疑虑压在心头，更不能让这种“怪力乱神”之事，成为悬在大晏王朝头顶的利剑。\n\n夜色渐深，皇城内逐渐安静下来。楚明楼借着月光，悄然离开了同僚的视线，转身朝着翰林院的方向行去。他的身影融入夜色，如同一个潜行的刺客，目标直指那座存放着无数秘密的古老建筑。\n\n翰林院，深夜。\n\n寂静无声，只有偶尔传来的夜枭啼鸣，更添了几分森然。\n\n楚明楼凭借着翰林修撰的身份令牌，避开了值夜的禁卫，熟门熟路地来到了存放禁书的丙字库。\n\n丙字库的大门由沉重的乌木制成，门上绘着古朴的符文，散发着冰冷的气息。这里存放的，大多是皇家认为不宜公开流传的典籍，或是被认为过于偏僻、怪诞的记载。\n\n他深吸一口气，推开了厚重的大门。一股混合着陈腐纸张、灰尘和墨香的气息扑面而来，仿佛将他带入了另一个时空。\n\n库房内，书架高耸入顶，密密麻麻的书卷层叠摆放，在昏暗的光线下投下巨大的阴影。楚明楼点亮了一盏宫灯，微弱的灯火驱散了部分黑暗，却也让阴影更加摇曳，如同鬼魅。\n\n他心中默念着“心正身直”，开始在书架间搜寻。\n\n“异闻录……地理志……前朝秘史……”\n\n他的目光快速扫过一卷卷书脊上的标题，手指轻轻拂过布满灰尘的封面。他知道，自己要找的，并非是那些广为流传的史书，而是那些被遗忘在角落，甚至可能被列为禁忌的记载。\n\n时间一分一秒地过去，宫灯里的灯油在缓缓减少。楚明楼的心也渐渐沉了下去，难道，真的只是自己看错了？或者，那件事，根本就不是人力所能解释，也无法在任何史料中找到答案？\n\n就在他准备放弃，离开这个令人窒息的地方时，他的目光无意间扫过了一个角落。\n\n那里，一本残破的书卷被随意地丢弃在一旁，似乎是被遗忘了很久。\n\n书名已经模糊不清，只隐约可见“大晏异闻录”几个字样，但字体古老，与如今通行的写法已有差异。书页泛黄，边缘卷曲，甚至有几处明显的虫蛀痕迹，仿佛随时会化为飞灰。\n\n“《大晏异闻录》……”楚明楼心中一动，这似乎与他最初的猜测不谋而合。\n\n他小心翼翼地将书取下，捧在手中。书页散发出一种奇异的、混合着霉味和淡淡药草香的气息。\n\n他盘膝坐下，将宫灯放在身侧，开始翻阅。\n\n书中的记载，果然如他所料，并未涉及什么长生不老、呼风唤雨的仙法。更多的是一些零散的、关于历代王朝的奇闻异事，以及一些模糊的记载。\n\n“……景兴年间，宫中曾有方士，以奇术蛊惑圣心，后被贬斥……”\n\n“……元和朝，边关告急，朝廷命术士占卜吉凶，竟引来妖邪作祟……”\n\n“……太祖皇帝曾言，国之兴衰，非仅系于兵戈民心，亦关乎……”\n\n楚明楼的心跳开始加速。这些零散的记载，虽然语焉不详，却指向了一个共同的模糊概念——“方士”以及他们对朝政的影响。\n\n“方士……他们究竟是何许人也？”\n\n他继续向下翻阅，目光落在其中一段模糊的记载上：\n\n“……夫天地之间，气有浩然，正气存内，邪不可干。方术诡谲，惑人心智，唯‘浩然正气’可御之……”\n\n“浩然正气……”\n\n这四个字，如同惊雷般在楚明楼的脑海中炸响。这是他从小熟读的儒家经典中的概念，是孟子所言的“吾善养吾浩然之气”。\n\n他一直以为，这只是修身养性的道德说辞，是精神层面的追求。\n\n可现在，这本书却明确指出，这“浩然正气”，竟然是抵御“方术”的关键？\n\n就在他读到此处时，他惊讶地发现，手中这本残破的《大晏异闻录》的书页上，一个原本模糊不清的古老印记，突然散发出了一道微弱的、几乎难以察觉的淡金色光芒。\n\n那光芒一闪即逝，仿佛只是灯火的折射。但楚明楼知道，那绝对不是错觉。\n\n那个印记……它在回应“浩然正气”这几个字？\n\n一股寒意从脚底升起，瞬间蔓延至全身。他猛地抬起头，环顾四周阴森的库房，感觉自己仿佛闯入了一个巨大而古老的阴谋之中。\n\n皇帝的怪病，老太监的神秘手段，以及这本记载着“方士”和“气运”的禁书……\n\n这一切，都指向了一个他从未想象过的、隐藏在大晏王朝光鲜外表之下的黑暗秘密。\n\n他，楚明楼，一个坚信圣贤之道的读书人，似乎无意间，触碰到了皇室最深层的禁忌。\n\n……\n\n与此同时，京城另一处不起眼的角落。\n\n一座古朴的宅院内，烛火摇曳。\n\n一个身着道袍的老者，正全神贯注地盯着桌上一个布满复杂纹路的铜盘。\n\n铜盘中央，一根细长的指针，正随着某种无形的力量微微颤动。\n\n突然，指针猛地一顿，然后，极其轻微地，朝着一个方向偏转了过去。\n\n老者浑浊的眼睛微微眯起，顺着指针的方向望去，口中喃喃自语：“嗯？翰林院……有异动？”\n\n他的手指轻轻抚过铜盘边缘的刻纹，空气中弥漫着一股淡淡的、如同檀香般的奇异气味。\n\n“气运……果然有所感应……”\n\n老者眼中闪过一丝不易察觉的光芒，随即又隐没下去，仿佛什么都没有发生过。\n\n夜，依旧深沉。'}
11:13:47 app.services.agent.langgraph_agent INFO   [LangGraph] writing 决策 (HTTPAIService): False
11:13:47 app.services.agent.langgraph_agent INFO   [LangGraph] 无需工具调用，结束流程
11:13:47 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: _should_continue
11:13:47 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: writing_agent
11:13:47 app.services.agent.langgraph_agent INFO   [Stream Event] progress_event = {'type': 'progress', 'step': 'thinking', 'description': '正在思考如何帮助您...', 'node': 'writing_agent', 'details': {}, 'timestamp': '2025-11-13T11:13:47.514226', 'progress': 100.0, 'eta': 0, 'eta_display': '即将完成', 'eta_confidence': 'high', 'current_step': 5, 'total_steps': 5, 'step_description': '第 5/5 步', 'elapsed': 19.0}
11:13:47 app.api.v1.agent INFO   [Stream] Activity完成: intent_analysis (19.0s)
11:13:47 app.services.agent.langgraph_agent INFO   [Stream Event] on_progress 回调已调用
11:13:47 app.api.v1.agent INFO   [SSE] 发送 activity_complete 事件: step=intent_analysis, elapsed=19.0s
11:13:47 app.api.v1.agent INFO   [SSE] 发送 progress 事件: step=thinking, desc=正在思考如何帮助您...
11:13:47 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: LangGraph
11:13:47 app.services.agent.langgraph_agent INFO   [LangGraph Stream] 流式执行完成，共14个事件
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  8.10it/s]
11:13:47 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | work_id=eb13b431-caef-4ec3-83b2-453951b16a72 | 重要度=0.50 | 长度=384
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 21.16it/s]
11:13:47 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | work_id=eb13b431-caef-4ec3-83b2-453951b16a72 | 重要度=0.90 | 长度=2605
11:13:47 app.services.context.store INFO   [ContextStore] 保存上下文: 2147a190-de66-49b9-b3c3-a8d9d1baf905, token=8630
11:13:47 app.services.context.manager INFO   [ContextManager] 更新上下文: 2147a190-de66-49b9-b3c3-a8d9d1baf905, 消息数=4, Token=8630
11:13:47 app.services.agent.langgraph_agent INFO   [Context] 上下文已更新: 2147a190-de66-49b9-b3c3-a8d9d1baf905 (work_id=eb13b431-caef-4ec3-83b2-453951b16a72)
11:13:47 app.services.agent.progress_tracker INFO   [ProgressTracker] 状态已重置
11:13:47 app.api.v1.agent INFO   [Stream] 最后活动完成: thinking (0.5s)
11:13:47 app.api.v1.agent INFO   [SSE] 发送 activity_complete 事件: step=thinking, elapsed=0.5s
11:13:47 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: react, Stream completed
11:13:49 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/2 200 OK"
11:13:49 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:14:11 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 26
11:14:11 app.services.ai.http_ai_service INFO   流式响应Token统计: 2444 (prompt=2433, completion=11)
11:14:11 app.services.agent.cost_tracker INFO   [CostTracker] 记录API调用: gemini-2.5-pro, tokens: 2433+11=2444, cost: $0.003151
11:14:11 app.services.ai.http_ai_service INFO   [CostTracker] API调用已记录: tokens=2433+11, cost=$0.003151, time=25.77s
11:14:11 app.services.ai.ai_log_middleware INFO   AI调用日志已记录: operation=continue, tokens=132, cost=$0.000305, duration=25773ms, success=True
11:14:11 app.api.v1.ai INFO   [AI续写] 用户 testuser_new-1 请求完成，生成字数: 26
11:14:15 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/chapters
INFO:     127.0.0.1:58006 - "POST /api/v1/chapters HTTP/1.1" 201 Created
11:14:15 sqlalchemy.pool.impl.AsyncAdaptedQueuePool ERROR   The garbage collector is trying to clean up non-checked-in connection <AdaptedConnection <asyncpg.connection.Connection object at 0x0000021047152E40>>, which will be terminated.  Please ensure that SQLAlchemy pooled connections are returned to the pool explicitly, either by calling ``close()`` or by using appropriate context managers to manage their lifecycle.
sys:1: SAWarning: The garbage collector is trying to clean up non-checked-in connection <AdaptedConnection <asyncpg.connection.Connection object at 0x0000021047152E40>>, which will be terminated.  Please ensure that SQLAlchemy pooled connections are returned to the pool explicitly, either by calling ``close()`` or by using appropriate context managers to manage their lifecycle.
11:14:15 sqlalchemy.pool.impl.AsyncAdaptedQueuePool ERROR   The garbage collector is trying to clean up non-checked-in connection <AdaptedConnection <asyncpg.connection.Connection object at 0x000002104696D9A0>>, which will be terminated.  Please ensure that SQLAlchemy pooled connections are returned to the pool explicitly, either by calling ``close()`` or by using appropriate context managers to manage their lifecycle.
sys:1: SAWarning: The garbage collector is trying to clean up non-checked-in connection <AdaptedConnection <asyncpg.connection.Connection object at 0x000002104696D9A0>>, which will be terminated.  Please ensure that SQLAlchemy pooled connections are returned to the pool explicitly, either by calling ``close()`` or by using appropriate context managers to manage their lifecycle.
11:14:15 sqlalchemy.pool.impl.AsyncAdaptedQueuePool ERROR   The garbage collector is trying to clean up non-checked-in connection <AdaptedConnection <asyncpg.connection.Connection object at 0x0000021047191310>>, which will be terminated.  Please ensure that SQLAlchemy pooled connections are returned to the pool explicitly, either by calling ``close()`` or by using appropriate context managers to manage their lifecycle.
sys:1: SAWarning: The garbage collector is trying to clean up non-checked-in connection <AdaptedConnection <asyncpg.connection.Connection object at 0x0000021047191310>>, which will be terminated.  Please ensure that SQLAlchemy pooled connections are returned to the pool explicitly, either by calling ``close()`` or by using appropriate context managers to manage their lifecycle.
11:14:15 sqlalchemy.pool.impl.AsyncAdaptedQueuePool ERROR   The garbage collector is trying to clean up non-checked-in connection <AdaptedConnection <asyncpg.connection.Connection object at 0x00000210471517C0>>, which will be terminated.  Please ensure that SQLAlchemy pooled connections are returned to the pool explicitly, either by calling ``close()`` or by using appropriate context managers to manage their lifecycle.
sys:1: SAWarning: The garbage collector is trying to clean up non-checked-in connection <AdaptedConnection <asyncpg.connection.Connection object at 0x00000210471517C0>>, which will be terminated.  Please ensure that SQLAlchemy pooled connections are returned to the pool explicitly, either by calling ``close()`` or by using appropriate context managers to manage their lifecycle.
11:14:15 app.services.novel_analysis_service INFO   Deleted old analysis for work eb13b431-caef-4ec3-83b2-453951b16a72, creating new one
11:14:15 app.services.novel_analysis_service INFO   Created analysis task for work eb13b431-caef-4ec3-83b2-453951b16a72, total_chapters: 2
11:14:15 app.api.v1.novel_analysis INFO   User 602f5147-846a-4cde-95d3-405fa75f133f started analysis for work eb13b431-caef-4ec3-83b2-453951b16a72, analysis_id: 70ad01bb-18cc-4b49-a18e-2407965d9436
11:14:15 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/analysis/works/eb13b431-caef-4ec3-83b2-453951b16a72/start
INFO:     127.0.0.1:58006 - "POST /api/v1/analysis/works/eb13b431-caef-4ec3-83b2-453951b16a72/start HTTP/1.1" 201 Created
11:14:15 app.api.middleware.monitoring_middleware INFO   API请求完成: OPTIONS /api/v1/chapters/e240ac64-5541-4987-8adf-ddf6dd1e4105
INFO:     127.0.0.1:58006 - "OPTIONS /api/v1/chapters/e240ac64-5541-4987-8adf-ddf6dd1e4105 HTTP/1.1" 200 OK
11:14:15 app.api.middleware.monitoring_middleware INFO   API请求完成: OPTIONS /api/v1/chapters/e240ac64-5541-4987-8adf-ddf6dd1e4105
INFO:     127.0.0.1:58006 - "OPTIONS /api/v1/chapters/e240ac64-5541-4987-8adf-ddf6dd1e4105 HTTP/1.1" 200 OK
11:14:16 app.api.v1.novel_analysis INFO   后台任务开始：分析作品 eb13b431-caef-4ec3-83b2-453951b16a72
11:14:16 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/e240ac64-5541-4987-8adf-ddf6dd1e4105
INFO:     127.0.0.1:59741 - "PUT /api/v1/chapters/e240ac64-5541-4987-8adf-ddf6dd1e4105 HTTP/1.1" 200 OK
11:14:16 app.api.v1.novel_analysis INFO   后台任务已找到分析记录 analysis_id=70ad01bb-18cc-4b49-a18e-2407965d9436
11:14:16 app.services.ai.novel_analysis_orchestrator INFO   ============================================================
11:14:16 app.services.ai.novel_analysis_orchestrator INFO   开始分析作品: eb13b431-caef-4ec3-83b2-453951b16a72
11:14:16 app.services.ai.novel_analysis_orchestrator INFO   ============================================================
11:14:16 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/e240ac64-5541-4987-8adf-ddf6dd1e4105
INFO:     127.0.0.1:58006 - "PUT /api/v1/chapters/e240ac64-5541-4987-8adf-ddf6dd1e4105 HTTP/1.1" 200 OK
11:14:16 app.services.novel_analysis_service INFO   Updated analysis 70ad01bb-18cc-4b49-a18e-2407965d9436 progress: 0/2, stage: AnalysisStage.MICRO_ANALYSIS, status: AnalysisStatus.ANALYZING
11:14:16 app.services.ai.novel_analysis_orchestrator INFO   初始化AI分析服务...
11:14:16 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
11:14:16 app.services.ai.http_ai_service INFO   ModelSelector 已启用
11:14:16 app.services.ai.http_ai_service INFO   CostTracker 已启用
11:14:17 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
11:14:17 app.services.ai.novel_micro_analysis INFO   微观分析提示词加载成功
11:14:17 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
11:14:17 app.services.ai.http_ai_service INFO   ModelSelector 已启用
11:14:17 app.services.ai.http_ai_service INFO   CostTracker 已启用
11:14:19 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
11:14:19 app.services.ai.novel_macro_analysis INFO   宏观分析提示词加载成功
11:14:19 app.services.ai.novel_analysis_orchestrator INFO   共获取 2 个章节，开始微观分析...
11:14:19 app.services.ai.novel_analysis_orchestrator INFO   ⚡ 使用并行分析模式 (并发数: 5)
11:14:19 app.services.ai.novel_analysis_orchestrator INFO   ⚡ 启动 2 个并发分析任务...
11:14:19 app.services.ai.novel_analysis_orchestrator INFO   [1/2] 🔄 开始分析: 琼林夜宴，天子疾
11:14:19 app.services.ai.novel_micro_analysis INFO   开始AI分析章节: 6c46612a-5d6f-4ad2-9310-7d8aac83e881 - 琼林夜宴，天子疾
11:14:19 app.services.ai.novel_micro_analysis INFO   第 1/3 次尝试调用AI分析
11:14:19 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=4000, temp=0.3, task_type=None
11:14:19 app.services.ai.novel_analysis_orchestrator INFO   [2/2] 🔄 开始分析: 翰林寻秘，怪力乱神
11:14:19 app.services.ai.novel_micro_analysis INFO   开始AI分析章节: e240ac64-5541-4987-8adf-ddf6dd1e4105 - 翰林寻秘，怪力乱神
11:14:19 app.services.ai.novel_micro_analysis INFO   第 1/3 次尝试调用AI分析
11:14:19 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=4000, temp=0.3, task_type=None
11:14:19 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/e240ac64-5541-4987-8adf-ddf6dd1e4105
INFO:     127.0.0.1:59741 - "PUT /api/v1/chapters/e240ac64-5541-4987-8adf-ddf6dd1e4105 HTTP/1.1" 200 OK
11:14:19 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/e240ac64-5541-4987-8adf-ddf6dd1e4105
INFO:     127.0.0.1:58006 - "PUT /api/v1/chapters/e240ac64-5541-4987-8adf-ddf6dd1e4105 HTTP/1.1" 200 OK
11:14:22 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/2 200 OK"
11:14:22 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:14:23 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/2 200 OK"
11:14:23 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:14:23 app.api.v1.ai INFO   [AI续写] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), 上下文长度: 28, 风格: 默认
11:14:23 app.api.v1.ai INFO   [AI续写] context内容: '月华如水，倾泻在紫禁城的琉璃瓦上，反射出冰冷而破碎的光。'
11:14:23 app.api.v1.ai INFO   [AI续写] prompt: '续写', max_tokens: 100
11:14:23 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
11:14:23 app.services.ai.http_ai_service INFO   ModelSelector 已启用
11:14:23 app.services.ai.http_ai_service INFO   CostTracker 已启用
11:14:24 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
11:14:24 app.services.ai.http_ai_service INFO   AI自动补全请求 - 上下文长度: 28
11:14:24 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=100, temp=0.7, task_type=None
11:14:24 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/complete
INFO:     127.0.0.1:58006 - "POST /api/v1/ai/complete HTTP/1.1" 200 OK
11:14:40 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/e240ac64-5541-4987-8adf-ddf6dd1e4105
INFO:     127.0.0.1:51996 - "PUT /api/v1/chapters/e240ac64-5541-4987-8adf-ddf6dd1e4105 HTTP/1.1" 200 OK
11:14:40 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/e240ac64-5541-4987-8adf-ddf6dd1e4105
INFO:     127.0.0.1:57074 - "PUT /api/v1/chapters/e240ac64-5541-4987-8adf-ddf6dd1e4105 HTTP/1.1" 200 OK
11:14:41 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/2 200 OK"
11:14:41 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:14:52 app.services.ai.http_ai_service INFO   API 响应完成，共接收 30 个数据块，总长度: 4592
11:14:52 app.services.ai.http_ai_service INFO   流式响应Token统计: 6371 (prompt=4461, completion=1910)
11:14:52 app.services.agent.cost_tracker INFO   [CostTracker] 记录API调用: gemini-2.5-pro, tokens: 4461+1910=6371, cost: $0.024676
11:14:52 app.services.ai.http_ai_service INFO   [CostTracker] API调用已记录: tokens=4461+1910, cost=$0.024676, time=32.95s
11:14:52 app.services.ai.novel_micro_analysis INFO   [Token记录] 微观分析: 6371 tokens (prompt=4461, completion=1910), 成本=$0.024676, 耗时=32952ms
11:14:52 app.services.ai.novel_micro_analysis INFO   章节 6c46612a-5d6f-4ad2-9310-7d8aac83e881 分析成功，提取事件数: 7
11:14:52 app.services.ai.novel_analysis_orchestrator INFO   [1/2] ✓ 分析完成: 琼林夜宴，天子疾 (33.0秒)
11:14:53 app.services.ai.http_ai_service INFO   API 响应完成，共接收 26 个数据块，总长度: 3971
11:14:53 app.services.ai.http_ai_service INFO   流式响应Token统计: 6353 (prompt=4677, completion=1676)
11:14:53 app.services.agent.cost_tracker INFO   [CostTracker] 记录API调用: gemini-2.5-pro, tokens: 4677+1676=6353, cost: $0.022606
11:14:53 app.services.ai.http_ai_service INFO   [CostTracker] API调用已记录: tokens=4677+1676, cost=$0.022606, time=34.10s
11:14:53 app.services.ai.novel_micro_analysis INFO   [Token记录] 微观分析: 6353 tokens (prompt=4677, completion=1676), 成本=$0.022606, 耗时=34103ms
11:14:53 app.services.ai.novel_micro_analysis INFO   章节 e240ac64-5541-4987-8adf-ddf6dd1e4105 分析成功，提取事件数: 5
11:14:53 app.services.ai.novel_analysis_orchestrator INFO   [2/2] ✓ 分析完成: 翰林寻秘，怪力乱神 (34.1秒)
11:14:53 app.services.ai.novel_analysis_orchestrator INFO   ⚡ 并行分析完成: 成功 2/2 章
11:14:53 app.services.ai.novel_analysis_orchestrator INFO   💾 开始批量保存 2 个分析结果...
11:14:53 app.services.novel_analysis_service INFO   Batch saved 2 micro results for analysis 70ad01bb-18cc-4b49-a18e-2407965d9436, total: 2
11:14:53 app.services.ai.novel_analysis_orchestrator INFO   ✅ 批量保存完成: 2 个结果
11:14:53 app.services.ai.novel_analysis_orchestrator INFO   🔍 开始批量存储向量...
11:14:53 app.services.vector_store_service INFO   开始向量化章节 6c46612a-5d6f-4ad2-9310-7d8aac83e881 的微观分析数据
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  5.69it/s]
11:14:53 app.services.vector_store_service INFO   生成向量维度: 384
11:14:53 app.services.vector_store_service INFO   向量存储成功: vector_id=c05f5333-3b29-4490-8305-be15a0991403
11:14:53 app.services.vector_store_service INFO   开始向量化章节 e240ac64-5541-4987-8adf-ddf6dd1e4105 的微观分析数据
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  7.66it/s]
11:14:53 app.services.vector_store_service INFO   生成向量维度: 384
11:14:53 app.services.vector_store_service INFO   向量存储成功: vector_id=1c9f6abb-7f84-46a6-8470-c8393d73b034
11:14:53 app.services.ai.novel_analysis_orchestrator INFO   ✅ 批量向量存储完成
11:14:53 app.services.ai.novel_analysis_orchestrator INFO   ============================================================
11:14:53 app.services.ai.novel_analysis_orchestrator INFO   微观分析完成统计:
11:14:53 app.services.ai.novel_analysis_orchestrator INFO     成功: 2/2 章节 (100.0%)
11:14:53 app.services.ai.novel_analysis_orchestrator INFO     失败: 0 章节
11:14:53 app.services.ai.novel_analysis_orchestrator INFO     总耗时: 37.5秒 (平均 18.8秒/章)
11:14:53 app.services.ai.novel_analysis_orchestrator INFO   ============================================================
11:14:53 app.services.novel_analysis_service INFO   Updated analysis 70ad01bb-18cc-4b49-a18e-2407965d9436 progress: 2/2, stage: AnalysisStage.MACRO_ANALYSIS, status: None
11:14:53 app.services.ai.novel_analysis_orchestrator INFO   ============================================================
11:14:53 app.services.ai.novel_analysis_orchestrator INFO   开始宏观分析...
11:14:53 app.services.ai.novel_analysis_orchestrator INFO   ============================================================
11:14:53 app.services.ai.novel_macro_analysis INFO   开始宏观分析，共 2 个章节的数据
11:14:53 app.services.ai.novel_macro_analysis INFO   第 1/3 次尝试调用AI宏观分析
11:14:53 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=6000, temp=0.5, task_type=None
11:14:55 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
11:14:55 app.services.ai.http_ai_service INFO   ModelSelector 已启用
11:14:55 app.services.ai.http_ai_service INFO   CostTracker 已启用
11:14:57 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
11:14:57 app.api.v1.agent INFO   [Chat Stream] Mode: react
11:14:57 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
11:14:57 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: react, Message: 刚才我问了你什么问题？...
INFO:     127.0.0.1:62776 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
11:14:57 app.services.agent.langgraph_agent INFO   [LangGraph Stream] 开始流式执行: 刚才我问了你什么问题？...
11:14:57 app.services.agent.langgraph_agent INFO   [Context] 设置用户ID: 602f5147-846a-4cde-95d3-405fa75f133f
11:14:57 app.services.context.store INFO   [ContextStore] 加载上下文: 2147a190-de66-49b9-b3c3-a8d9d1baf905, 4条消息
11:14:57 app.services.context.manager INFO   [ContextManager] Session 2147a190-de66-49b9-b3c3-a8d9d1baf905: 8630/8000 tokens
11:14:57 app.services.context.manager ERROR   [ContextManager] ❌ Token超过硬限制(8630/8000)，强制截断到5600tokens
11:14:57 app.services.context.manager WARNING   [ContextManager] 🔪 强制截断上下文: 8630 -> 5600 tokens
11:14:57 app.services.context.manager WARNING   [ContextManager] 截断结果: 保留2/4条消息, Token: 8630 -> ~3638
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 15.14it/s]
11:14:57 app.services.context.vector_memory_store INFO   🔍 检索记忆 | 查询='刚才我问了你什么问题？...' | 用户=602f5147-846a-4cde-95d3-405fa75f133f | work_id=eb13b431-caef-4ec3-83b2-453951b16a72 | 找到=0条 | 阈值=0.3
11:14:57 app.services.context.manager INFO   🔍 检索长期记忆 | work_id=eb13b431-caef-4ec3-83b2-453951b16a72 | 查询='刚才我问了你什么问题？...' | 找到=0条 | 阈值=0.3
11:14:57 app.services.context.monitoring_integration INFO   [Monitor] 上下文构建: 3条消息, 4932 tokens, 耗时 115.95ms
11:14:57 app.services.agent.langgraph_agent INFO   [Context] 加载上下文: {'session_id': '2147a190-de66-49b9-b3c3-a8d9d1baf905', 'token_count': 4932, 'short_memory_size': 2, 'has_summary': False, 'compression_triggered': False, 'long_term_memories': 0, 'adaptive_budget_enabled': False, 'task_type': None}
11:14:57 app.services.agent.langgraph_agent INFO   [LangGraph] 使用隔离的thread_id: eb13b431-caef-4ec3-83b2-453951b16a72:2147a190-de66-49b9-b3c3-a8d9d1baf905 (work_id=eb13b431-caef-4ec3-83b2-453951b16a72, conversation_id=2147a190-de66-49b9-b3c3-a8d9d1baf905)
11:14:57 app.services.agent.progress_tracker INFO   [ProgressTracker] 初始化完成，使用动态节点追踪模式（根据实际执行的节点自动计算进度）
11:14:57 app.services.agent.langgraph_agent INFO   [ProgressTracker] 初始化完成，使用动态节点追踪模式
11:14:57 app.services.agent.langgraph_agent INFO   [LangGraph] 意图分类（规则识别）
11:14:57 app.services.agent.langgraph_agent INFO   [Intent] 规则识别结果: general, 置信度: 0.85
11:14:57 app.services.agent.langgraph_agent INFO   [LangGraph] 路由到: general
11:14:57 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: _route_intent
11:14:57 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: intent_classifier
11:14:57 app.services.agent.langgraph_agent INFO   [Stream Event] progress_event = {'type': 'progress', 'step': 'intent_analysis', 'description': '识别为：一般对话', 'node': 'intent_classifier', 'details': {'intent': 'general'}, 'timestamp': '2025-11-13T11:14:57.191586', 'progress': 100.0, 'eta': 0, 'eta_display': '即将完成', 'eta_confidence': 'high', 'current_step': 3, 'total_steps': 3, 'step_description': '第 3/3 步', 'elapsed': 0.0}
11:14:57 app.services.agent.langgraph_agent INFO   [Stream Event] on_progress 回调已调用
11:14:57 app.api.v1.agent INFO   [SSE] 发送 progress 事件: step=intent_analysis, desc=识别为：一般对话
11:14:57 app.services.agent.langgraph_agent INFO   [LangGraph] 处理一般对话（新架构）
11:14:57 Action.general_chat INFO   [general_chat] 准备一般对话，历史消息数: 15
11:14:57 app.services.agent.langgraph_agent INFO   [LangGraph] 使用system_prompt调用LLM: 你是友好的AI写作助手，以专业、简洁的方式回复用户。

【你的特点】
- 友好、专业、有耐心
- 简洁明了，避免冗长
- 善于引导用户使用功能

【你能做什么】
- 写作：帮助用户续写、创作小说内容
...
11:14:57 app.services.agent.langgraph_agent INFO   [LangGraph] 处理general场景 (use_chatgpt=False)
11:14:57 app.core.cache INFO   ✅ 缓存命中: prompt:get_tool_decision_static_prompt:fca6eb91156619d0
11:14:57 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
11:14:57 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
11:14:57 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=200, temp=0.3, task_type=TaskType.SIMPLE_QA
11:14:57 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/2 200 OK"
11:14:57 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:14:59 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/2 200 OK"
11:14:59 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:15:00 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 85
11:15:00 app.services.ai.http_ai_service INFO   流式响应Token统计: 847 (prompt=812, completion=35)
11:15:00 app.services.agent.cost_tracker INFO   [CostTracker] 记录API调用: gemini-2.5-pro, tokens: 812+35=847, cost: $0.001365
11:15:00 app.services.ai.http_ai_service INFO   [CostTracker] API调用已记录: tokens=812+35, cost=$0.001365, time=3.29s
11:15:00 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=847
11:15:00 app.services.agent.langgraph_agent INFO   [LangGraph] AI 决策原文: ```json
{
  "need_tools": true,
  "tool_name": "get_context",
  "tool_args": {}
}
```
11:15:00 app.services.agent.langgraph_agent INFO   [LangGraph] 方法2成功: 正则提取 JSON
11:15:00 app.services.agent.langgraph_agent INFO   [LangGraph] 最终决策: {'need_tools': True, 'tool_name': 'get_context', 'tool_args': {}}
11:15:00 app.services.agent.langgraph_agent INFO   [LangGraph] general 决策 (HTTPAIService): True
11:15:00 app.services.agent.langgraph_agent WARNING   [LangGraph] 尝试调用未知工具: get_context
11:15:00 app.services.agent.langgraph_agent INFO   [LangGraph] 🎯 检测到工具错误(unknown_tool)，直接返回友好提示
11:15:00 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: general_chat
11:15:00 app.services.agent.langgraph_agent INFO   [Stream Event] progress_event = {'type': 'progress', 'step': 'thinking', 'description': '正在思考回复...', 'node': 'general_chat', 'details': {}, 'timestamp': '2025-11-13T11:15:00.484478', 'progress': 100.0, 'eta': 0, 'eta_display': '即将完成', 'eta_confidence': 'high', 'current_step': 4, 'total_steps': 4, 'step_description': '第 4/4 步', 'elapsed': 3.3}
11:15:00 app.api.v1.agent INFO   [Stream] Activity完成: intent_analysis (3.3s)
11:15:00 app.services.agent.langgraph_agent INFO   [Stream Event] on_progress 回调已调用
11:15:00 app.api.v1.agent INFO   [SSE] 发送 activity_complete 事件: step=intent_analysis, elapsed=3.3s
11:15:00 app.api.v1.agent INFO   [SSE] 发送 progress 事件: step=thinking, desc=正在思考回复...
11:15:00 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: LangGraph
11:15:00 app.services.agent.langgraph_agent INFO   [LangGraph Stream] 流式执行完成，共12个事件
11:15:00 app.services.context.store INFO   [ContextStore] 保存上下文: 2147a190-de66-49b9-b3c3-a8d9d1baf905, token=4970
11:15:00 app.services.context.manager INFO   [ContextManager] 更新上下文: 2147a190-de66-49b9-b3c3-a8d9d1baf905, 消息数=4, Token=4970
11:15:00 app.services.agent.langgraph_agent INFO   [Context] 上下文已更新: 2147a190-de66-49b9-b3c3-a8d9d1baf905 (work_id=eb13b431-caef-4ec3-83b2-453951b16a72)
11:15:00 app.services.agent.progress_tracker INFO   [ProgressTracker] 状态已重置
11:15:00 app.api.v1.agent INFO   [Stream] 最后活动完成: thinking (0.0s)
11:15:00 app.api.v1.agent INFO   [SSE] 发送 activity_complete 事件: step=thinking, elapsed=0.0s
11:15:00 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: react, Stream completed
11:15:09 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 21
11:15:09 app.services.ai.http_ai_service INFO   流式响应Token统计: 3458 (prompt=3441, completion=17)
11:15:09 app.services.agent.cost_tracker INFO   [CostTracker] 记录API调用: gemini-2.5-pro, tokens: 3441+17=3458, cost: $0.004471
11:15:09 app.services.ai.http_ai_service INFO   [CostTracker] API调用已记录: tokens=3441+17, cost=$0.004471, time=45.08s
11:15:09 app.services.ai.ai_log_middleware INFO   AI调用日志已记录: operation=continue, tokens=30, cost=$0.000151, duration=45077ms, success=True
11:15:09 app.api.v1.ai INFO   [AI续写] 用户 testuser_new-1 请求完成，生成字数: 21
