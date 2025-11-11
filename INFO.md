14:43:24 app.api.v1.chapters INFO   [GET chapters] Returning 34 chapters
INFO:     127.0.0.1:56309 - "GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/characters HTTP/1.1" 200 OK
14:43:24 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/chapters/work/c9dd9cbf-fa57-447e-9605-3020bbde5350
INFO:     127.0.0.1:56310 - "GET /api/v1/chapters/work/c9dd9cbf-fa57-447e-9605-3020bbde5350 HTTP/1.1" 200 OK
14:43:24 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/locations
14:43:24 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/settings
INFO:     127.0.0.1:56311 - "GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/locations HTTP/1.1" 200 OK
INFO:     127.0.0.1:56308 - "GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/settings HTTP/1.1" 200 OK
14:43:24 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/guidelines
INFO:     127.0.0.1:56312 - "GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/guidelines HTTP/1.1" 200 OK
14:43:24 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/ai-guidelines
INFO:     127.0.0.1:56307 - "GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/ai-guidelines HTTP/1.1" 200 OK
14:43:24 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/analysis/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/status
INFO:     127.0.0.1:56309 - "GET /api/v1/analysis/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/status HTTP/1.1" 200 OK
14:43:24 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/analysis/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/status
INFO:     127.0.0.1:56310 - "GET /api/v1/analysis/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/status HTTP/1.1" 200 OK
14:43:24 app.api.middleware.monitoring_middleware INFO   API请求完成: OPTIONS /api/v1/chapters/627feba4-2097-4f28-a3f3-7641d10f7f40
14:43:24 app.api.middleware.monitoring_middleware INFO   API请求完成: OPTIONS /api/v1/chapters/627feba4-2097-4f28-a3f3-7641d10f7f40
INFO:     127.0.0.1:56312 - "OPTIONS /api/v1/chapters/627feba4-2097-4f28-a3f3-7641d10f7f40 HTTP/1.1" 200 OK
INFO:     127.0.0.1:56310 - "OPTIONS /api/v1/chapters/627feba4-2097-4f28-a3f3-7641d10f7f40 HTTP/1.1" 200 OK
14:43:24 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/627feba4-2097-4f28-a3f3-7641d10f7f40
INFO:     127.0.0.1:56310 - "PUT /api/v1/chapters/627feba4-2097-4f28-a3f3-7641d10f7f40 HTTP/1.1" 200 OK
14:43:24 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/627feba4-2097-4f28-a3f3-7641d10f7f40
INFO:     127.0.0.1:56312 - "PUT /api/v1/chapters/627feba4-2097-4f28-a3f3-7641d10f7f40 HTTP/1.1" 200 OK
14:43:40 app.api.middleware.monitoring_middleware INFO   API请求完成: OPTIONS /api/v1/agent/chat/stream
INFO:     127.0.0.1:49857 - "OPTIONS /api/v1/agent/chat/stream HTTP/1.1" 200 OK
14:43:40 app.services.ai.prompts INFO   Prompts loaded successfully from D:\Java\ai_writer\backend\app\services\ai\prompts\default.json
14:43:40 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
14:43:40 app.services.ai.http_ai_service INFO   ModelSelector 已启用
14:43:40 app.services.agent.cost_tracker INFO   CostTracker 初始化完成, 持久化: False
14:43:40 app.services.ai.http_ai_service INFO   CostTracker 已启用
14:43:42 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
14:43:42 app.api.v1.agent INFO   [Chat Stream] Mode: react
14:43:42 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:49857 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
14:44:03 app.core.redis INFO   ✅ Redis connected: redis://localhost:6379/0
14:44:03 app.api.v1.agent INFO   [Session] 创建新会话归属: ffea963b-fbad-4af4-91af-b5b1f7e65edd -> 602f5147-846a-4cde-95d3-405fa75f133f
14:44:03 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: react, Message: 基于《一夕千悟》现有内容，为主角段融制定后续20章的详细成长大纲。 要求： 1. 涵盖从杂役弟子到高...
14:44:03 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
14:44:03 app.services.ai.http_ai_service INFO   ModelSelector 已启用
14:44:03 app.services.ai.http_ai_service INFO   CostTracker 已启用
14:44:04 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
14:44:04 chromadb.telemetry.product.posthog INFO   Anonymized telemetry enabled. See                     https://docs.trychroma.com/telemetry for more information.
14:44:04 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
14:44:12 app.services.context.vector_memory_store INFO   ✅ VectorMemoryStore初始化成功 | 目录=./data/chroma_db | 模型=paraphrase-multilingual-MiniLM-L12-v2 | 集合=user_memories
14:44:12 app.services.context.manager INFO   ✅ VectorMemoryStore 已初始化
14:44:12 app.services.context.manager INFO   ✅ ContextManager: 长期记忆已启用 (user_id=None)
14:44:12 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ ContextManager已初始化（长期记忆已启用）
成功加载模板: intent_classifier (版本 2.0.0)
成功加载模板: writing_agent (版本 2.0.0)
成功加载模板: planning_agent (版本 2.0.0)
成功加载模板: tool_agent (版本 2.0.0)
成功加载模板: query_agent (版本 2.0.0)
14:44:12 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ PromptManager已初始化
14:44:12 app.services.agent.langgraph_agent INFO   [LangGraph] 使用 ChatOpenAI 模式（原生工具调用）
14:44:15 app.api.callbacks.monitoring_callback INFO   [MonitoringCallback] 已初始化
14:44:15 app.services.agent.langgraph_agent INFO   [LangGraph] 已创建MonitoringCallbackHandler
14:44:37 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ Redis连接验证成功
14:44:37 app.services.agent.langgraph_agent INFO   [LangGraph] OK 使用 AsyncRedisSaver（redis://localhost:6379/0，TTL=7天）
14:44:37 app.services.agent.parallel_tool_node INFO   [ParallelToolNode] 初始化完成，最大并发数=5，并行安全工具=4个
14:44:37 app.api.v1.agent INFO   [Global Agent] 创建全局Agent实例，MemorySaver将在请求间共享
14:44:37 app.services.agent.langgraph_agent INFO   [LangGraph Stream] 开始流式执行: 基于《一夕千悟》现有内容，为主角段融制定后续20章的详细成长大纲。 要求： 1. 涵盖从杂役弟子到高...
14:44:58 redisvl.index.index INFO   Index already exists, not overwriting.
14:44:58 redisvl.index.index INFO   Index already exists, not overwriting.
14:44:58 redisvl.index.index INFO   Index already exists, not overwriting.
14:44:58 langgraph.checkpoint.redis.aio INFO   Redis client is a standalone client
14:44:58 app.services.agent.langgraph_agent INFO   [LangGraph] AsyncRedisSaver索引创建成功
14:44:58 app.services.agent.langgraph_agent INFO   [Context] 设置用户ID: 602f5147-846a-4cde-95d3-405fa75f133f
14:44:58 app.services.context.monitoring_integration INFO   ✅ ContextManager监控收集器已初始化
14:44:58 app.services.context.store INFO   [ContextStore] Redis连接成功
14:45:19 app.services.context.manager INFO   [ContextManager] 创建新上下文: ffea963b-fbad-4af4-91af-b5b1f7e65edd
14:45:19 app.services.context.token_counter INFO   ✅ tiktoken初始化成功，模型: gpt-4
14:45:19 app.services.context.manager INFO   [ContextManager] Session ffea963b-fbad-4af4-91af-b5b1f7e65edd: 711/8000 tokens
Batches: 100%|█████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 17.35it/s]
14:45:19 app.services.context.vector_memory_store INFO   🔍 检索记忆 | 查询='基于《一夕千悟》现有内容，为主角段融制定后续20章的详细成长...' | 用户=602f5147-846a-4cde-95d3-405fa75f133f | 找到=3条 | 阈值=0.3
14:45:19 app.services.context.manager INFO   🔍 检索长期记忆 | 查询='基于《一夕千悟》现有内容，为主角段融制定后续20章的详细成长...' | 找到=3条 | 阈值=0.3
14:45:19 app.services.context.monitoring_integration INFO   [Monitor] 上下文构建: 2条消息, 711 tokens, 耗时 21412.73ms
14:45:19 app.services.agent.langgraph_agent INFO   [Context] 加载上下文: {'session_id': 'ffea963b-fbad-4af4-91af-b5b1f7e65edd', 'token_count': 711, 'short_memory_size': 0, 'has_summary': False, 'compression_triggered': False, 'long_term_memories': 3, 'adaptive_budget_enabled': False, 'task_type': None}
14:45:19 app.services.agent.progress_tracker INFO   [ProgressTracker] 初始化完成，使用动态节点追踪模式（根据实际执行的节点自动计算进度）
14:45:19 app.services.agent.langgraph_agent INFO   [ProgressTracker] 初始化完成，使用动态节点追踪模式
14:45:19 app.services.agent.langgraph_agent INFO   [LangGraph] 意图分类（规则识别）
14:45:19 app.services.agent.langgraph_agent INFO   [Intent] 规则识别结果: writing, 置信度: 0.90
14:45:19 app.services.agent.langgraph_agent INFO   [LangGraph] 路由到: writing
14:45:19 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: _route_intent
14:45:19 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: intent_classifier
14:45:19 app.services.agent.langgraph_agent INFO   [Stream Event] progress_event = {'type': 'progress', 'step': 'intent_analysis', 'description': '识别为：写作任务', 'node': 'intent_classifier', 'details': {'intent': 'writing'}, 'timestamp': '2025-11-11T14:45:19.726256', 'progress': 100.0, 'eta': 0, 'eta_display': '即将完成', 'eta_confidence': 'high', 'current_step': 3, 'total_steps': 3, 'step_description': '第 3/3 步', 'elapsed': 0.0}
14:45:19 app.services.agent.langgraph_agent INFO   [Stream Event] on_progress 回调已调用
14:45:19 app.api.v1.agent INFO   [SSE] 发送 progress 事件: step=intent_analysis, desc=识别为：写作任务
14:45:19 app.services.agent.actions.action_registry INFO   [ActionRegistry] 注册Action: echo (class=EchoAction, category=example)
14:45:19 app.services.agent.actions.action_registry INFO   [ActionRegistry] 注册Action: writing (class=WritingAction, category=content_creation)
14:45:19 app.services.agent.actions.action_registry INFO   [ActionRegistry] 注册Action: planning (class=PlanningAction, category=planning)
14:45:19 app.services.agent.actions.action_registry INFO   [ActionRegistry] 注册Action: analysis (class=AnalysisAction, category=analysis)
14:45:19 app.services.agent.actions.action_registry INFO   [ActionRegistry] 注册Action: stuck (class=StuckAction, category=writing_assistance)
14:45:19 app.services.agent.actions.action_registry INFO   [ActionRegistry] 注册Action: general_chat (class=GeneralChatAction, category=conversation)
14:45:19 app.services.agent.langgraph_agent INFO   [LangGraph] 处理写作请求（新架构）
14:45:19 Action.writing INFO   [writing] PromptManager已初始化
14:45:19 Action.writing INFO   [writing] work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=627feba4-2097-4f28-a3f3-7641d10f7f40, phase=None, chapter_num=None
14:45:19 app.services.agent.langgraph_agent INFO   [LangGraph] WritingAction准备完成: phase=None, chapter_num=None
14:45:19 app.services.agent.langgraph_agent INFO   [LangGraph] 处理writing场景 (use_chatgpt=True)
14:45:23 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
14:46:26 app.api.callbacks.monitoring_callback INFO   [MonitoringCallback] LLM调用成功: run_id=f805bdf4-f497-4a7c-917e-370d1c7e556d, model=unknown, duration=66.99s, tokens=N/A
14:46:26 app.services.agent.langgraph_agent INFO   [LangGraph] 无需工具调用，结束流程
14:46:26 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: _should_continue
14:46:26 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: writing_agent
14:46:26 app.services.agent.langgraph_agent INFO   [Stream Event] progress_event = {'type': 'progress', 'step': 'thinking', 'description': '正在思考如何帮助您...', 'node': 'writing_agent', 'details': {}, 'timestamp': '2025-11-11T14:46:26.724829', 'progress': 100.0, 'eta': 0, 'eta_display': '即将完成', 'eta_confidence': 'high', 'current_step': 5, 'total_steps': 5, 'step_description': '第 5/5 步', 'elapsed': 67.0}
14:46:26 app.api.v1.agent INFO   [Stream] Activity完成: intent_analysis (67.0s)
14:46:26 app.services.agent.langgraph_agent INFO   [Stream Event] on_progress 回调已调用
14:46:26 app.api.v1.agent INFO   [SSE] 发送 activity_complete 事件: step=intent_analysis, elapsed=67.0s
14:46:26 app.api.v1.agent INFO   [SSE] 发送 progress 事件: step=thinking, desc=正在思考如何帮助您...
14:46:26 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: LangGraph
14:46:26 app.services.agent.langgraph_agent INFO   [LangGraph Stream] 流式执行完成，共69个事件
Batches: 100%|█████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 11.83it/s]
14:46:27 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 重要度=0.90 | 长度=105
Batches: 100%|█████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  7.55it/s]
14:46:27 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 重要度=0.90 | 长度=3589
14:46:27 app.services.context.store INFO   [ContextStore] 保存上下文: ffea963b-fbad-4af4-91af-b5b1f7e65edd, token=4698
14:46:27 app.services.context.manager INFO   [ContextManager] 更新上下文: ffea963b-fbad-4af4-91af-b5b1f7e65edd, 消息数=2, Token=4698
14:46:27 app.services.agent.langgraph_agent INFO   [Context] 上下文已更新: ffea963b-fbad-4af4-91af-b5b1f7e65edd
14:46:27 app.services.agent.progress_tracker INFO   [ProgressTracker] 状态已重置
14:46:27 app.api.v1.agent INFO   [Stream] 最后活动完成: thinking (0.6s)
14:46:27 app.api.v1.agent INFO   [SSE] 发送 activity_complete 事件: step=thinking, elapsed=0.6s
14:46:27 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: react, Stream completed
14:47:42 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
14:47:42 app.services.ai.http_ai_service INFO   ModelSelector 已启用
14:47:42 app.services.ai.http_ai_service INFO   CostTracker 已启用
14:47:44 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
14:47:44 app.api.v1.agent INFO   [Chat Stream] Mode: react
14:47:44 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
14:47:44 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: react, Message: 请深度分析《一夕千悟》主角段融的以下方面： 1. 性格特征和心理变化 2. 能力体系和成长轨迹 3....
INFO:     127.0.0.1:58258 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
14:47:44 app.services.agent.langgraph_agent INFO   [LangGraph Stream] 开始流式执行: 请深度分析《一夕千悟》主角段融的以下方面： 1. 性格特征和心理变化 2. 能力体系和成长轨迹 3....
14:47:44 app.services.agent.langgraph_agent INFO   [Context] 设置用户ID: 602f5147-846a-4cde-95d3-405fa75f133f
14:47:44 app.services.context.store INFO   [ContextStore] 加载上下文: ffea963b-fbad-4af4-91af-b5b1f7e65edd, 2条消息
14:47:44 app.services.context.manager INFO   [ContextManager] Session ffea963b-fbad-4af4-91af-b5b1f7e65edd: 4698/8000 tokens
Batches: 100%|█████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  9.79it/s]
14:47:44 app.services.context.vector_memory_store INFO   🔍 检索记忆 | 查询='请深度分析《一夕千悟》主角段融的以下方面： 1. 性格特征和...' | 用户=602f5147-846a-4cde-95d3-405fa75f133f | 找到=3条 | 阈值=0.3
14:47:44 app.services.context.manager INFO   🔍 检索长期记忆 | 查询='请深度分析《一夕千悟》主角段融的以下方面： 1. 性格特征和...' | 找到=3条 | 阈值=0.3
14:47:44 app.services.context.monitoring_integration INFO   [Monitor] 上下文构建: 4条消息, 4698 tokens, 耗时 130.05ms
14:47:44 app.services.agent.langgraph_agent INFO   [Context] 加载上下文: {'session_id': 'ffea963b-fbad-4af4-91af-b5b1f7e65edd', 'token_count': 4698, 'short_memory_size': 2, 'has_summary': False, 'compression_triggered': False, 'long_term_memories': 3, 'adaptive_budget_enabled': False, 'task_type': None}
14:47:44 app.services.agent.progress_tracker INFO   [ProgressTracker] 初始化完成，使用动态节点追踪模式（根据实际执行的节点自动计算进度）
14:47:44 app.services.agent.langgraph_agent INFO   [ProgressTracker] 初始化完成，使用动态节点追踪模式
14:47:44 app.services.agent.langgraph_agent INFO   [LangGraph] 意图分类（规则识别）
14:47:44 app.services.agent.langgraph_agent INFO   [Intent] 规则识别结果: analysis, 置信度: 0.93
14:47:44 app.services.agent.langgraph_agent INFO   [LangGraph] 路由到: analysis
14:47:44 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: _route_intent
14:47:44 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: intent_classifier
14:47:44 app.services.agent.langgraph_agent INFO   [Stream Event] progress_event = {'type': 'progress', 'step': 'intent_analysis', 'description': '识别为：分析任务', 'node': 'intent_classifier', 'details': {'intent': 'analysis'}, 'timestamp': '2025-11-11T14:47:44.630125', 'progress': 100.0, 'eta': 0, 'eta_display': '即将完成', 'eta_confidence': 'high', 'current_step': 3, 'total_steps': 3, 'step_description': '第 3/3 步', 'elapsed': 0.0}
14:47:44 app.services.agent.langgraph_agent INFO   [Stream Event] on_progress 回调已调用
14:47:44 app.api.v1.agent INFO   [SSE] 发送 progress 事件: step=intent_analysis, desc=识别为：分析任务
14:47:44 app.services.agent.langgraph_agent INFO   [LangGraph] 处理分析请求（新架构）
14:47:44 Action.analysis INFO   [analysis] PromptManager已初始化
14:47:44 Action.analysis INFO   [analysis] work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=627feba4-2097-4f28-a3f3-7641d10f7f40
14:47:44 app.services.agent.langgraph_agent INFO   [LangGraph] AnalysisAction准备完成: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=627feba4-2097-4f28-a3f3-7641d10f7f40
14:47:44 app.services.agent.langgraph_agent INFO   [LangGraph] 处理analysis场景 (use_chatgpt=True)
14:47:54 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
14:48:39 app.api.callbacks.monitoring_callback INFO   [MonitoringCallback] LLM调用成功: run_id=ed8ab36a-52b3-42d7-aaac-a4a534a66e03, model=unknown, duration=55.33s, tokens=N/A
14:48:39 app.services.agent.langgraph_agent INFO   [LangGraph] 无需工具调用，结束流程
14:48:39 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: _should_continue
14:48:39 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: analysis_agent
14:48:39 app.services.agent.langgraph_agent INFO   [Stream Event] progress_event = {'type': 'progress', 'step': 'thinking', 'description': '正在分析内容...', 'node': 'analysis_agent', 'details': {}, 'timestamp': '2025-11-11T14:48:39.973677', 'progress': 100.0, 'eta': 0, 'eta_display': '即将完成', 'eta_confidence': 'high', 'current_step': 5, 'total_steps': 5, 'step_description': '第 5/5 步', 'elapsed': 55.4}
14:48:39 app.api.v1.agent INFO   [Stream] Activity完成: intent_analysis (55.3s)
14:48:39 app.services.agent.langgraph_agent INFO   [Stream Event] on_progress 回调已调用
14:48:39 app.api.v1.agent INFO   [SSE] 发送 activity_complete 事件: step=intent_analysis, elapsed=55.3s
14:48:39 app.api.v1.agent INFO   [SSE] 发送 progress 事件: step=thinking, desc=正在分析内容...
14:48:39 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: LangGraph
14:48:39 app.services.agent.langgraph_agent INFO   [LangGraph Stream] 流式执行完成，共211个事件
Batches: 100%|█████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  7.66it/s]
14:48:40 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 重要度=0.90 | 长度=3116
14:48:40 app.services.context.store INFO   [ContextStore] 保存上下文: ffea963b-fbad-4af4-91af-b5b1f7e65edd, token=8239
14:48:40 app.services.context.manager INFO   [ContextManager] 更新上下文: ffea963b-fbad-4af4-91af-b5b1f7e65edd, 消息数=4, Token=8239
14:48:40 app.services.agent.langgraph_agent INFO   [Context] 上下文已更新: ffea963b-fbad-4af4-91af-b5b1f7e65edd
14:48:40 app.services.agent.progress_tracker INFO   [ProgressTracker] 状态已重置
14:48:40 app.api.v1.agent INFO   [Stream] 最后活动完成: thinking (0.4s)
14:48:40 app.api.v1.agent INFO   [SSE] 发送 activity_complete 事件: step=thinking, elapsed=0.4s
14:48:40 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: react, Stream completed
