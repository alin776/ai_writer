21:22:45 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
21:22:45 app.services.ai.http_ai_service INFO   ModelSelector 已启用
21:22:45 app.services.agent.cost_tracker INFO   CostTracker 初始化完成, 持久化: False
21:22:45 app.services.ai.http_ai_service INFO   CostTracker 已启用
21:22:48 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
21:22:48 app.api.v1.agent INFO   [Chat Stream] Mode: react
21:22:48 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:60928 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
21:23:09 app.core.redis INFO   ✅ Redis connected: redis://localhost:6379/0
21:23:09 app.api.v1.agent INFO   [Session] 创建新会话归属: fad45aed-deee-4aad-898f-b76511ef0626 -> 602f5147-846a-4cde-95d3-405fa75f133f
21:23:09 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: react, Message: 第一章讲了什么？...
21:23:09 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
21:23:09 app.services.ai.http_ai_service INFO   ModelSelector 已启用
21:23:09 app.services.ai.http_ai_service INFO   CostTracker 已启用
21:23:10 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
21:23:10 chromadb.telemetry.product.posthog INFO   Anonymized telemetry enabled. See                     https://docs.trychroma.com/telemetry for more information.
21:23:11 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
21:23:19 app.services.context.vector_memory_store INFO   ✅ VectorMemoryStore初始化成功 | 目录=./data/chroma_db | 模型=paraphrase-multilingual-MiniLM-L12-v2 | 集合=user_memories
21:23:19 app.services.context.manager INFO   ✅ VectorMemoryStore 已初始化
21:23:19 app.services.context.manager INFO   ✅ ContextManager: 长期记忆已启用 (user_id=None)
21:23:19 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ ContextManager已初始化（长期记忆已启用）
成功加载模板: intent_classifier (版本 2.0.0)
成功加载模板: writing_agent (版本 2.0.0)
成功加载模板: planning_agent (版本 2.0.0)
成功加载模板: tool_agent (版本 2.0.0)
成功加载模板: query_agent (版本 2.0.0)
21:23:19 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ PromptManager已初始化
21:23:19 app.services.agent.langgraph_agent INFO   [LangGraph] 使用 ChatOpenAI 模式（原生工具调用）
21:23:22 app.api.callbacks.monitoring_callback INFO   [MonitoringCallback] 已初始化
21:23:22 app.services.agent.langgraph_agent INFO   [LangGraph] 已创建MonitoringCallbackHandler
21:23:44 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ Redis连接验证成功
21:23:44 app.services.agent.langgraph_agent INFO   [LangGraph] OK 使用 AsyncRedisSaver（redis://localhost:6379/0，TTL=7天）
21:23:44 app.services.agent.parallel_tool_node INFO   [ParallelToolNode] 初始化完成，最大并发数=5，并行安全工具=4个
21:23:44 app.api.v1.agent INFO   [Global Agent] 创建全局Agent实例，MemorySaver将在请求间共享
21:23:44 app.services.agent.langgraph_agent INFO   [LangGraph Stream] 开始流式执行: 第一章讲了什么？...
21:24:05 redisvl.index.index INFO   Index already exists, not overwriting.
21:24:05 redisvl.index.index INFO   Index already exists, not overwriting.
21:24:05 redisvl.index.index INFO   Index already exists, not overwriting.
21:24:05 langgraph.checkpoint.redis.aio INFO   Redis client is a standalone client
21:24:05 app.services.agent.langgraph_agent INFO   [LangGraph] AsyncRedisSaver索引创建成功
21:24:05 app.services.agent.langgraph_agent INFO   [Context] 设置用户ID: 602f5147-846a-4cde-95d3-405fa75f133f
21:24:05 app.services.context.monitoring_integration INFO   ✅ ContextManager监控收集器已初始化
21:24:05 app.services.context.store INFO   [ContextStore] Redis连接成功
21:24:26 app.services.context.manager INFO   [ContextManager] 创建新上下文: fad45aed-deee-4aad-898f-b76511ef0626
21:24:26 app.services.context.token_counter INFO   ✅ tiktoken初始化成功，模型: gpt-4
21:24:26 app.services.context.manager INFO   [ContextManager] Session fad45aed-deee-4aad-898f-b76511ef0626: 596/8000 tokens
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  3.79it/s]
21:24:27 app.services.context.vector_memory_store INFO   🔍 检索记忆 | 查询='第一章讲了什么？...' | 用户=602f5147-846a-4cde-95d3-405fa75f133f | 找到=3条 | 阈值=0.3
21:24:27 app.services.context.manager INFO   🔍 检索长期记忆 | 查询='第一章讲了什么？...' | 找到=3条 | 阈值=0.3
21:24:27 app.services.context.monitoring_integration INFO   [Monitor] 上下文构建: 2条消息, 596 tokens, 耗时 22044.69ms
21:24:27 app.services.agent.langgraph_agent INFO   [Context] 加载上下文: {'session_id': 'fad45aed-deee-4aad-898f-b76511ef0626', 'token_count': 596, 'short_memory_size': 0, 'has_summary': False, 'compression_triggered': False, 'long_term_memories': 3, 'adaptive_budget_enabled': False, 'task_type': None}
21:24:27 app.services.agent.progress_tracker INFO   [ProgressTracker] 初始化完成，使用动态节点追踪模式（根据实际执行的节点自动计算进度）
21:24:27 app.services.agent.langgraph_agent INFO   [ProgressTracker] 初始化完成，使用动态节点追踪模式
21:24:27 app.services.agent.langgraph_agent INFO   [LangGraph] 意图分类（规则识别）
21:24:27 app.services.agent.langgraph_agent INFO   [Intent] 规则识别结果: writing, 置信度: 0.90
21:24:27 app.services.agent.langgraph_agent INFO   [LangGraph] 路由到: writing
21:24:27 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: _route_intent
21:24:27 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: intent_classifier
21:24:27 app.services.agent.langgraph_agent INFO   [Stream Event] progress_event = {'type': 'progress', 'step': 'intent_analysis', 'description': '识别为：写作任务', 'node': 'intent_classifier', 'details': {'intent': 'writing'}, 'timestamp': '2025-11-11T21:24:27.591914', 'progress': 100.0, 'eta': 0, 'eta_display': '即将完成', 'eta_confidence': 'high', 'current_step': 3, 'total_steps': 3, 'step_description': '第 3/3 步', 'elapsed': 0.0}
21:24:27 app.services.agent.langgraph_agent INFO   [Stream Event] on_progress 回调已调用
21:24:27 app.api.v1.agent INFO   [SSE] 发送 progress 事件: step=intent_analysis, desc=识别为：写作任务
21:24:27 app.services.agent.actions.action_registry INFO   [ActionRegistry] 注册Action: echo (class=EchoAction, category=example)
21:24:27 app.services.agent.actions.action_registry INFO   [ActionRegistry] 注册Action: writing (class=WritingAction, category=content_creation)
21:24:27 app.services.agent.actions.action_registry INFO   [ActionRegistry] 注册Action: planning (class=PlanningAction, category=planning)
21:24:27 app.services.agent.actions.action_registry INFO   [ActionRegistry] 注册Action: analysis (class=AnalysisAction, category=analysis)
21:24:27 app.services.agent.actions.action_registry INFO   [ActionRegistry] 注册Action: stuck (class=StuckAction, category=writing_assistance)
21:24:27 app.services.agent.actions.action_registry INFO   [ActionRegistry] 注册Action: general_chat (class=GeneralChatAction, category=conversation)
21:24:27 app.services.agent.langgraph_agent INFO   [LangGraph] 处理写作请求（新架构）
21:24:27 Action.writing INFO   [writing] PromptManager已初始化
21:24:27 Action.writing INFO   [writing] work_id=7caa9cfb-e028-4d84-9eb3-42550d11d3a4, chapter_id=7295d191-a203-47f1-bdd7-9ff28258cff1, phase=None, chapter_num=None
21:24:27 app.services.agent.langgraph_agent INFO   [LangGraph] WritingAction准备完成: phase=None, chapter_num=None
21:24:27 app.services.agent.langgraph_agent INFO   [LangGraph] 处理writing场景 (use_chatgpt=True)
21:24:47 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
21:24:50 app.api.callbacks.monitoring_callback INFO   [MonitoringCallback] LLM调用成功: run_id=4d2e4a9b-fc8e-4d65-9f8e-f9fc5ff3a041, model=unknown, duration=22.58s, tokens=N/A
21:24:50 app.services.agent.langgraph_agent INFO   [LangGraph] 检测到工具调用: 1 个工具
21:24:50 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: _should_continue
21:24:50 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: writing_agent
21:24:50 app.services.agent.langgraph_agent INFO   [Stream Event] progress_event = {'type': 'progress', 'step': 'thinking', 'description': '正在思考如何帮助您...', 'node': 'writing_agent', 'details': {}, 'timestamp': '2025-11-11T21:24:50.203136', 'progress': 100.0, 'eta': 0, 'eta_display': '即将完成', 'eta_confidence': 'high', 'current_step': 5, 'total_steps': 5, 'step_description': '第 5/5 步', 'elapsed': 22.7}
21:24:50 app.api.v1.agent INFO   [Stream] Activity完成: intent_analysis (22.6s)
21:24:50 app.services.agent.langgraph_agent INFO   [Stream Event] on_progress 回调已调用
21:24:50 app.api.v1.agent INFO   [SSE] 发送 activity_complete 事件: step=intent_analysis, elapsed=22.6s
21:24:50 app.api.v1.agent INFO   [SSE] 发送 progress 事件: step=thinking, desc=正在思考如何帮助您...
21:24:50 app.services.agent.parallel_tool_node INFO   [ParallelToolNode] 工具分组: 并行=1, 串行=0
21:24:50 app.services.agent.parallel_tool_node INFO   [ParallelToolNode] 开始并行执行1个工具
21:24:50 app.services.agent.parallel_tool_node INFO   [ParallelToolNode] 并行执行完成，成功=1，失败=0
21:24:50 app.services.agent.langgraph_agent INFO   [LangGraph] 工具执行完毕，路由回: writing_agent
21:24:50 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: _route_after_tools
21:24:50 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: tools
21:24:50 app.services.agent.langgraph_agent WARNING   [Tools Node] 未找到AIMessage的tool_calls，尝试从ToolMessage提取
21:24:50 app.services.agent.langgraph_agent INFO   [Tools Node] 最终使用: tool_name=get_chapter_by_order_tool, tool_args={}
21:24:50 app.services.agent.langgraph_agent INFO   [Stream Event] progress_event = {'type': 'progress', 'step': 'tool_execution', 'description': '📚 正在读取第?章...', 'node': 'tools', 'details': {'tools': ['get_chapter_by_order_tool'], 'tool_args': {}}, 'timestamp': '2025-11-11T21:24:50.221809', 'progress': 100.0, 'eta': 0, 'eta_display': '即将完成', 'eta_confidence': 'high', 'current_step': 7, 'total_steps': 7, 'step_description': '第 7/7 步', 'elapsed': 22.7}
21:24:50 app.api.v1.agent INFO   [Stream] Activity完成: thinking (0.0s)
21:24:50 app.services.agent.langgraph_agent INFO   [Stream Event] on_progress 回调已调用
21:24:50 app.api.v1.agent INFO   [SSE] 发送 activity_complete 事件: step=thinking, elapsed=0.0s
21:24:50 app.api.v1.agent INFO   [SSE] 发送 progress 事件: step=tool_execution, desc=📚 正在读取第?章...
21:24:50 app.services.agent.langgraph_agent INFO   [LangGraph] 处理写作请求（新架构）
21:24:50 Action.writing INFO   [writing] PromptManager已初始化
21:24:50 Action.writing INFO   [writing] 从消息中识别到章节号: 1
21:24:50 Action.writing INFO   [writing] 章节 1 属于阶段: opening
21:24:50 Action.writing INFO   [writing] work_id=7caa9cfb-e028-4d84-9eb3-42550d11d3a4, chapter_id=7295d191-a203-47f1-bdd7-9ff28258cff1, phase=opening, chapter_num=1
21:24:50 app.services.agent.langgraph_agent INFO   [LangGraph] WritingAction准备完成: phase=opening, chapter_num=1
21:24:50 app.services.agent.langgraph_agent INFO   [LangGraph] 处理writing场景 (use_chatgpt=True)
21:24:50 app.services.agent.langgraph_agent INFO   [LangGraph] writing - 处理工具执行结果 (ChatOpenAI)
21:24:53 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
21:25:23 app.api.callbacks.monitoring_callback INFO   [MonitoringCallback] LLM调用成功: run_id=1337fb4b-f5c8-4354-9e9e-8ac99ff5a2bd, model=unknown, duration=33.09s, tokens=N/A
21:25:23 app.services.agent.langgraph_agent INFO   [LangGraph] 无需工具调用，结束流程
21:25:23 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: _should_continue
21:25:23 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: writing_agent
21:25:23 app.services.agent.langgraph_agent INFO   [Stream Event] progress_event = {'type': 'progress', 'step': 'thinking', 'description': '正在思考如何帮助您...', 'node': 'writing_agent', 'details': {}, 'timestamp': '2025-11-11T21:25:23.326347', 'progress': 100.0, 'eta': 0, 'eta_display': '即将完成', 'eta_confidence': 'high', 'current_step': 7, 'total_steps': 7, 'step_description': '第 7/7 步', 'elapsed': 55.8}
21:25:23 app.api.v1.agent INFO   [Stream] Activity完成: tool_execution (33.1s)
21:25:23 app.services.agent.langgraph_agent INFO   [Stream Event] on_progress 回调已调用
21:25:23 app.api.v1.agent INFO   [SSE] 发送 activity_complete 事件: step=tool_execution, elapsed=33.1s
21:25:23 app.api.v1.agent INFO   [SSE] 发送 progress 事件: step=thinking, desc=正在思考如何帮助您...
21:25:23 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: LangGraph
21:25:23 app.services.agent.langgraph_agent INFO   [LangGraph Stream] 流式执行完成，共56个事件
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  6.27it/s]
21:25:23 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 重要度=0.90 | 长度=1166
21:25:23 app.services.context.store INFO   [ContextStore] 保存上下文: fad45aed-deee-4aad-898f-b76511ef0626, token=2014
21:25:23 app.services.context.manager INFO   [ContextManager] 更新上下文: fad45aed-deee-4aad-898f-b76511ef0626, 消息数=2, Token=2014
21:25:23 app.services.agent.langgraph_agent INFO   [Context] 上下文已更新: fad45aed-deee-4aad-898f-b76511ef0626
21:25:23 app.services.agent.progress_tracker INFO   [ProgressTracker] 状态已重置
21:25:23 app.api.v1.agent INFO   [Stream] 最后活动完成: thinking (0.5s)
21:25:23 app.api.v1.agent INFO   [SSE] 发送 activity_complete 事件: step=thinking, elapsed=0.5s
21:25:23 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: react, Stream completed
