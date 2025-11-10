INFO:     127.0.0.1:60631 - "OPTIONS /api/v1/agent/chat/stream HTTP/1.1" 200 OK
20:20:58 app.services.ai.prompts INFO   Prompts loaded successfully from D:\Java\ai_writer\backend\app\services\ai\prompts\default.json
20:20:58 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
20:20:58 app.services.ai.http_ai_service INFO   ModelSelector 已启用
20:20:58 app.services.agent.cost_tracker INFO   CostTracker 初始化完成, 持久化: False
20:20:58 app.services.ai.http_ai_service INFO   CostTracker 已启用
20:21:00 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
20:21:00 app.api.v1.agent INFO   [Chat Stream] Mode: react
20:21:00 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:60631 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
20:21:21 app.core.redis INFO   ✅ Redis connected: redis://localhost:6379/0
20:21:21 app.api.v1.agent INFO   [Session] 创建新会话归属: 0d901e52-11fd-43f8-acc4-35151912ebfb -> 602f5147-846a-4cde-95d3-405fa75f133f
20:21:21 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: react, Message: 请基于《一夕千悟》前4章的内容，续写第5章。 要求： 1. 保持段融的人设和成长轨迹 2. 延续修仙...
20:21:21 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
20:21:21 app.services.ai.http_ai_service INFO   ModelSelector 已启用
20:21:21 app.services.ai.http_ai_service INFO   CostTracker 已启用
20:21:22 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
20:21:22 chromadb.telemetry.product.posthog INFO   Anonymized telemetry enabled. See                     https://docs.trychroma.com/telemetry for more information.
20:21:22 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
20:21:29 app.services.context.vector_memory_store INFO   ✅ VectorMemoryStore初始化成功 | 目录=./data/chroma_db | 模型=paraphrase-multilingual-MiniLM-L12-v2 | 集合=user_memories
20:21:29 app.services.context.manager INFO   ✅ VectorMemoryStore 已初始化
20:21:29 app.services.context.manager INFO   ✅ ContextManager: 长期记忆已启用 (user_id=None)
20:21:29 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ ContextManager已初始化（长期记忆已启用）
成功加载模板: intent_classifier (版本 2.0.0)
成功加载模板: writing_agent (版本 2.0.0)
成功加载模板: planning_agent (版本 2.0.0)
成功加载模板: tool_agent (版本 2.0.0)
成功加载模板: query_agent (版本 2.0.0)
20:21:29 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ PromptManager已初始化
20:21:29 app.services.agent.langgraph_agent INFO   [LangGraph] 使用 ChatOpenAI 模式（原生工具调用）
20:21:30 app.api.callbacks.monitoring_callback INFO   [MonitoringCallback] 已初始化
20:21:30 app.services.agent.langgraph_agent INFO   [LangGraph] 已创建MonitoringCallbackHandler
20:21:52 app.services.agent.langgraph_agent INFO   [LangGraph] OK 使用 AsyncRedisSaver（redis://localhost:6379/0，TTL=7天）
20:21:52 app.services.agent.parallel_tool_node INFO   [ParallelToolNode] 初始化完成，最大并发数=5，并行安全工具=4个
20:21:52 app.api.v1.agent INFO   [Global Agent] 创建全局Agent实例，MemorySaver将在请求间共享
20:21:52 app.services.agent.langgraph_agent INFO   [LangGraph Stream] 开始流式执行: 请基于《一夕千悟》前4章的内容，续写第5章。 要求： 1. 保持段融的人设和成长轨迹 2. 延续修仙...
20:22:13 redisvl.index.index INFO   Index already exists, not overwriting.
20:22:13 redisvl.index.index INFO   Index already exists, not overwriting.
20:22:13 redisvl.index.index INFO   Index already exists, not overwriting.
20:22:13 langgraph.checkpoint.redis.aio INFO   Redis client is a standalone client
20:22:13 app.services.agent.langgraph_agent INFO   [LangGraph] AsyncRedisSaver索引创建成功
20:22:13 app.services.agent.langgraph_agent INFO   [Context] 设置用户ID: 602f5147-846a-4cde-95d3-405fa75f133f
20:22:13 app.services.context.monitoring_integration INFO   ✅ ContextManager监控收集器已初始化
20:22:13 app.services.context.store INFO   [ContextStore] Redis连接成功
20:22:34 app.services.context.manager INFO   [ContextManager] 创建新上下文: 0d901e52-11fd-43f8-acc4-35151912ebfb
20:22:34 app.services.context.token_counter INFO   ✅ tiktoken初始化成功，模型: gpt-4
20:22:34 app.services.context.manager INFO   [ContextManager] Session 0d901e52-11fd-43f8-acc4-35151912ebfb: 685/8000 tokens
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  4.92it/s]
20:22:35 app.services.context.vector_memory_store INFO   🔍 检索记忆 | 查询='请基于《一夕千悟》前4章的内容，续写第5章。 要求： 1. ...' | 用户=602f5147-846a-4cde-95d3-405fa75f133f | 找到=3条 | 阈值=0.3
20:22:35 app.services.context.manager INFO   🔍 检索长期记忆 | 查询='请基于《一夕千悟》前4章的内容，续写第5章。 要求： 1. ...' | 找到=3条 | 阈值=0.3
20:22:35 app.services.context.monitoring_integration INFO   [Monitor] 上下文构建: 2条消息, 685 tokens, 耗时 21583.57ms
20:22:35 app.services.agent.langgraph_agent INFO   [Context] 加载上下文: {'session_id': '0d901e52-11fd-43f8-acc4-35151912ebfb', 'token_count': 685, 'short_memory_size': 0, 'has_summary': False, 'compression_triggered': False, 'long_term_memories': 3, 'adaptive_budget_enabled': False, 'task_type': None}
20:22:35 app.services.agent.langgraph_agent INFO   [LangGraph] 意图分类（规则识别）
20:22:35 app.services.agent.langgraph_agent INFO   [Intent] 规则识别结果: writing, 置信度: 0.98
20:22:35 app.services.agent.langgraph_agent INFO   [LangGraph] 路由到: writing
20:22:35 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: intent_classifier
20:22:35 app.services.agent.langgraph_agent INFO   [Stream Event] progress_event = {'type': 'progress', 'step': 'intent_analysis', 'description': '识别为：写作任务', 'node': 'intent_classifier', 'details': {'intent': 'writing'}, 'timestamp': '2025-11-10T20:22:35.264971'}
20:22:35 app.services.agent.langgraph_agent INFO   [Stream Event] on_progress 回调已调用
20:22:35 app.api.v1.agent INFO   [SSE] 发送 progress 事件: step=intent_analysis, desc=识别为：写作任务
20:22:35 app.services.agent.actions.action_registry INFO   [ActionRegistry] 注册Action: echo (class=EchoAction, category=example)
20:22:35 app.services.agent.actions.action_registry INFO   [ActionRegistry] 注册Action: writing (class=WritingAction, category=content_creation)
20:22:35 app.services.agent.actions.action_registry INFO   [ActionRegistry] 注册Action: planning (class=PlanningAction, category=planning)
20:22:35 app.services.agent.actions.action_registry INFO   [ActionRegistry] 注册Action: analysis (class=AnalysisAction, category=analysis)
20:22:35 app.services.agent.actions.action_registry INFO   [ActionRegistry] 注册Action: stuck (class=StuckAction, category=writing_assistance)
20:22:35 app.services.agent.actions.action_registry INFO   [ActionRegistry] 注册Action: general_chat (class=GeneralChatAction, category=conversation)
20:22:35 app.services.agent.langgraph_agent INFO   [LangGraph] 处理写作请求（新架构）
20:22:35 Action.writing INFO   [writing] PromptManager已初始化
20:22:35 Action.writing INFO   [writing] 从消息中识别到章节号: 5
20:22:35 Action.writing INFO   [writing] 章节 5 属于阶段: opening
20:22:35 Action.writing INFO   [writing] work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=627feba4-2097-4f28-a3f3-7641d10f7f40, phase=opening, chapter_num=5
20:22:35 app.services.agent.langgraph_agent INFO   [LangGraph] WritingAction准备完成: phase=opening, chapter_num=5
20:22:35 app.services.agent.langgraph_agent INFO   [LangGraph] 处理writing场景 (use_chatgpt=True)
20:23:01 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
20:23:01 app.api.callbacks.monitoring_callback INFO   [MonitoringCallback] LLM调用成功: run_id=02cc8c75-c9e3-4209-850a-e90841ec857d, model=gemini-2.5-pro, duration=26.43s, tokens=3007 (prompt=2946, completion=61)
20:23:01 app.services.agent.langgraph_agent INFO   [LangGraph] 检测到工具调用: 1 个工具
20:23:01 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: writing_agent
20:23:01 app.services.agent.langgraph_agent INFO   [Stream Event] progress_event = {'type': 'progress', 'step': 'thinking', 'description': '正在思考如何帮助您...', 'node': 'writing_agent', 'details': {}, 'timestamp': '2025-11-10T20:23:01.730043'}
20:23:01 app.api.v1.agent INFO   [Stream] Activity完成: intent_analysis (26.5s)
20:23:01 app.services.agent.langgraph_agent INFO   [Stream Event] on_progress 回调已调用
20:23:01 app.api.v1.agent INFO   [SSE] 发送 activity_complete 事件: step=intent_analysis, elapsed=26.5s
20:23:01 app.services.agent.parallel_tool_node INFO   [ParallelToolNode] 工具分组: 并行=1, 串行=0
20:23:01 app.services.agent.parallel_tool_node INFO   [ParallelToolNode] 开始并行执行1个工具
20:23:01 app.api.v1.agent INFO   [SSE] 发送 progress 事件: step=thinking, desc=正在思考如何帮助您...
20:23:01 app.services.agent.parallel_tool_node INFO   [ParallelToolNode] 并行执行完成，成功=1，失败=0
20:23:01 app.services.agent.langgraph_agent INFO   [LangGraph] 工具执行完毕，路由回: writing_agent
20:23:01 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: tools
20:23:01 app.services.agent.langgraph_agent INFO   [Stream Event] progress_event = {'type': 'progress', 'step': 'tool_execution', 'description': '正在检索设定...', 'node': 'tools', 'details': {'tools': ['search_analysis_fragments_tool']}, 'timestamp': '2025-11-10T20:23:01.745569'}
20:23:01 app.api.v1.agent INFO   [Stream] Activity完成: thinking (0.0s)
20:23:01 app.services.agent.langgraph_agent INFO   [Stream Event] on_progress 回调已调用
20:23:01 app.api.v1.agent INFO   [SSE] 发送 activity_complete 事件: step=thinking, elapsed=0.0s
20:23:01 app.services.agent.langgraph_agent INFO   [LangGraph] 处理写作请求（新架构）
20:23:01 Action.writing INFO   [writing] PromptManager已初始化
20:23:01 Action.writing INFO   [writing] work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=627feba4-2097-4f28-a3f3-7641d10f7f40, phase=None, chapter_num=None
20:23:01 app.services.agent.langgraph_agent INFO   [LangGraph] WritingAction准备完成: phase=None, chapter_num=None
20:23:01 app.services.agent.langgraph_agent INFO   [LangGraph] 处理writing场景 (use_chatgpt=True)
20:23:01 app.services.agent.langgraph_agent INFO   [LangGraph] writing - 处理工具执行结果 (ChatOpenAI)
20:23:01 app.api.v1.agent INFO   [SSE] 发送 progress 事件: step=tool_execution, desc=正在检索设定...
20:23:40 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
20:23:40 app.api.callbacks.monitoring_callback INFO   [MonitoringCallback] LLM调用成功: run_id=1be2d731-b074-4ec8-96ae-92c4c3ba8735, model=gemini-2.5-pro, duration=38.64s, tokens=3702 (prompt=388, completion=3314)
20:23:40 app.services.agent.langgraph_agent INFO   [LangGraph] 无需工具调用，结束流程
20:23:40 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: writing_agent
20:23:40 app.services.agent.langgraph_agent INFO   [Stream Event] progress_event = {'type': 'progress', 'step': 'thinking', 'description': '正在思考如何帮助您...', 'node': 'writing_agent', 'details': {}, 'timestamp': '2025-11-10T20:23:40.426480'}
20:23:40 app.api.v1.agent INFO   [Stream] Activity完成: tool_execution (38.7s)
20:23:40 app.services.agent.langgraph_agent INFO   [Stream Event] on_progress 回调已调用
20:23:40 app.api.v1.agent INFO   [SSE] 发送 activity_complete 事件: step=tool_execution, elapsed=38.7s
20:23:40 app.api.v1.agent INFO   [SSE] 发送 progress 事件: step=thinking, desc=正在思考如何帮助您...
20:23:40 app.services.agent.langgraph_agent INFO   [LangGraph Stream] 流式执行完成，共4个事件
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  2.36it/s]
20:23:42 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 重要度=0.90 | 长度=88
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  1.28it/s]
20:23:43 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 重要度=0.90 | 长度=1791
20:23:43 app.services.context.store INFO   [ContextStore] 保存上下文: 0d901e52-11fd-43f8-acc4-35151912ebfb, token=3136
20:23:43 app.services.context.manager INFO   [ContextManager] 更新上下文: 0d901e52-11fd-43f8-acc4-35151912ebfb, 消息数=2, Token=3136
20:23:43 app.services.agent.langgraph_agent INFO   [Context] 上下文已更新: 0d901e52-11fd-43f8-acc4-35151912ebfb
20:23:43 app.api.v1.agent INFO   [Stream] 最后活动完成: thinking (2.9s)
20:23:43 app.api.v1.agent INFO   [SSE] 发送 activity_complete 事件: step=thinking, elapsed=2.9s
20:23:43 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: react, Stream completed
20:25:18 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
20:25:18 app.services.ai.http_ai_service INFO   ModelSelector 已启用
20:25:18 app.services.ai.http_ai_service INFO   CostTracker 已启用
20:25:21 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
20:25:21 app.api.v1.agent INFO   [Chat Stream] Mode: react
20:25:21 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
20:25:21 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: react, Message: 基于《一夕千悟》现有内容，为主角段融制定后续20章的详细成长大纲。 要求： 1. 涵盖从杂役弟子到高...
INFO:     127.0.0.1:59474 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
20:25:21 app.services.agent.langgraph_agent INFO   [LangGraph Stream] 开始流式执行: 基于《一夕千悟》现有内容，为主角段融制定后续20章的详细成长大纲。 要求： 1. 涵盖从杂役弟子到高...
20:25:21 app.services.agent.langgraph_agent INFO   [Context] 设置用户ID: 602f5147-846a-4cde-95d3-405fa75f133f
20:25:21 app.services.context.store INFO   [ContextStore] 加载上下文: 0d901e52-11fd-43f8-acc4-35151912ebfb, 2条消息
20:25:21 app.services.context.manager INFO   [ContextManager] Session 0d901e52-11fd-43f8-acc4-35151912ebfb: 3136/8000 tokens
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  6.41it/s]
20:25:22 app.services.context.vector_memory_store INFO   🔍 检索记忆 | 查询='基于《一夕千悟》现有内容，为主角段融制定后续20章的详细成长...' | 用户=602f5147-846a-4cde-95d3-405fa75f133f | 找到=3条 | 阈值=0.3
20:25:22 app.services.context.manager INFO   🔍 检索长期记忆 | 查询='基于《一夕千悟》现有内容，为主角段融制定后续20章的详细成长...' | 找到=3条 | 阈值=0.3
20:25:22 app.services.context.monitoring_integration INFO   [Monitor] 上下文构建: 4条消息, 3136 tokens, 耗时 187.20ms
20:25:22 app.services.agent.langgraph_agent INFO   [Context] 加载上下文: {'session_id': '0d901e52-11fd-43f8-acc4-35151912ebfb', 'token_count': 3136, 'short_memory_size': 2, 'has_summary': False, 'compression_triggered': False, 'long_term_memories': 3, 'adaptive_budget_enabled': False, 'task_type': None}
20:25:22 app.services.agent.langgraph_agent INFO   [LangGraph] 意图分类（规则识别）
20:25:22 app.services.agent.langgraph_agent INFO   [Intent] 规则识别结果: writing, 置信度: 0.90
20:25:22 app.services.agent.langgraph_agent INFO   [LangGraph] 路由到: writing
20:25:22 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: intent_classifier
20:25:22 app.services.agent.langgraph_agent INFO   [Stream Event] progress_event = {'type': 'progress', 'step': 'intent_analysis', 'description': '识别为：写作任务', 'node': 'intent_classifier', 'details': {'intent': 'writing'}, 'timestamp': '2025-11-10T20:25:22.177349'}
20:25:22 app.services.agent.langgraph_agent INFO   [Stream Event] on_progress 回调已调用
20:25:22 app.api.v1.agent INFO   [SSE] 发送 progress 事件: step=intent_analysis, desc=识别为：写作任务
20:25:22 app.services.agent.langgraph_agent INFO   [LangGraph] 处理写作请求（新架构）
20:25:22 Action.writing INFO   [writing] PromptManager已初始化
20:25:22 Action.writing INFO   [writing] work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=627feba4-2097-4f28-a3f3-7641d10f7f40, phase=None, chapter_num=None
20:25:22 app.services.agent.langgraph_agent INFO   [LangGraph] WritingAction准备完成: phase=None, chapter_num=None
20:25:22 app.services.agent.langgraph_agent INFO   [LangGraph] 处理writing场景 (use_chatgpt=True)
20:26:39 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
20:26:39 app.api.callbacks.monitoring_callback INFO   [MonitoringCallback] LLM调用成功: run_id=1c221a97-1c9c-4f93-9e75-0e606441ca22, model=gemini-2.5-pro, duration=77.15s, tokens=9676 (prompt=6608, completion=3068)
20:26:39 app.services.agent.langgraph_agent INFO   [LangGraph] 无需工具调用，结束流程
20:26:39 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: writing_agent
20:26:39 app.services.agent.langgraph_agent INFO   [Stream Event] progress_event = {'type': 'progress', 'step': 'thinking', 'description': '正在思考如何帮助您...', 'node': 'writing_agent', 'details': {}, 'timestamp': '2025-11-10T20:26:39.369096'}
20:26:39 app.api.v1.agent INFO   [Stream] Activity完成: intent_analysis (77.2s)
20:26:39 app.services.agent.langgraph_agent INFO   [Stream Event] on_progress 回调已调用
20:26:39 app.api.v1.agent INFO   [SSE] 发送 activity_complete 事件: step=intent_analysis, elapsed=77.2s
20:26:39 app.api.v1.agent INFO   [SSE] 发送 progress 事件: step=thinking, desc=正在思考如何帮助您...
20:26:39 app.services.agent.langgraph_agent INFO   [LangGraph Stream] 流式执行完成，共2个事件
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  1.66it/s]
20:26:40 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 重要度=0.90 | 长度=105
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:01<00:00,  1.04s/it]
20:26:42 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 重要度=0.90 | 长度=4389
20:26:42 app.services.context.store INFO   [ContextStore] 保存上下文: 0d901e52-11fd-43f8-acc4-35151912ebfb, token=7967
20:26:42 app.services.context.manager INFO   [ContextManager] 更新上下文: 0d901e52-11fd-43f8-acc4-35151912ebfb, 消息数=4, Token=7967
20:26:42 app.services.agent.langgraph_agent INFO   [Context] 上下文已更新: 0d901e52-11fd-43f8-acc4-35151912ebfb
20:26:42 app.api.v1.agent INFO   [Stream] 最后活动完成: thinking (2.8s)
20:26:42 app.api.v1.agent INFO   [SSE] 发送 activity_complete 事件: step=thinking, elapsed=2.8s
20:26:42 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: react, Stream completed
20:29:06 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
20:29:06 app.services.ai.http_ai_service INFO   ModelSelector 已启用
20:29:06 app.services.ai.http_ai_service INFO   CostTracker 已启用
20:29:09 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
20:29:09 app.api.v1.agent INFO   [Chat Stream] Mode: react
20:29:09 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
20:29:09 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: react, Message: 请深度分析《一夕千悟》主角段融的以下方面： 1. 性格特征和心理变化 2. 能力体系和成长轨迹 3....
INFO:     127.0.0.1:52823 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
20:29:09 app.services.agent.langgraph_agent INFO   [LangGraph Stream] 开始流式执行: 请深度分析《一夕千悟》主角段融的以下方面： 1. 性格特征和心理变化 2. 能力体系和成长轨迹 3....
20:29:09 app.services.agent.langgraph_agent INFO   [Context] 设置用户ID: 602f5147-846a-4cde-95d3-405fa75f133f
20:29:09 app.services.context.store INFO   [ContextStore] 加载上下文: 0d901e52-11fd-43f8-acc4-35151912ebfb, 4条消息
20:29:09 app.services.context.manager INFO   [ContextManager] Session 0d901e52-11fd-43f8-acc4-35151912ebfb: 7967/8000 tokens
20:29:09 app.services.context.manager WARNING   [ContextManager] Token使用率过高 (7967/8000), 触发压缩
20:29:09 app.services.context.manager INFO   [ContextManager] 开始压缩: 0d901e52-11fd-43f8-acc4-35151912ebfb
20:29:09 app.services.context.manager INFO   [ContextManager] 消息数不足，无需压缩
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  5.24it/s]
20:29:10 app.services.context.vector_memory_store INFO   🔍 检索记忆 | 查询='请深度分析《一夕千悟》主角段融的以下方面： 1. 性格特征和...' | 用户=602f5147-846a-4cde-95d3-405fa75f133f | 找到=3条 | 阈值=0.3
20:29:10 app.services.context.manager INFO   🔍 检索长期记忆 | 查询='请深度分析《一夕千悟》主角段融的以下方面： 1. 性格特征和...' | 找到=3条 | 阈值=0.3
20:29:10 app.services.context.monitoring_integration INFO   [Monitor] 上下文构建: 6条消息, 7967 tokens, 耗时 247.33ms
20:29:10 app.services.agent.langgraph_agent INFO   [Context] 加载上下文: {'session_id': '0d901e52-11fd-43f8-acc4-35151912ebfb', 'token_count': 7967, 'short_memory_size': 4, 'has_summary': False, 'compression_triggered': True, 'long_term_memories': 3, 'adaptive_budget_enabled': False, 'task_type': None}
20:29:10 app.services.agent.langgraph_agent INFO   [LangGraph] 意图分类（规则识别）
20:29:10 app.services.agent.langgraph_agent INFO   [Intent] 规则识别结果: analysis, 置信度: 0.93
20:29:10 app.services.agent.langgraph_agent INFO   [LangGraph] 路由到: analysis
20:29:10 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: intent_classifier
20:29:10 app.services.agent.langgraph_agent INFO   [Stream Event] progress_event = {'type': 'progress', 'step': 'intent_analysis', 'description': '识别为：分析任务', 'node': 'intent_classifier', 'details': {'intent': 'analysis'}, 'timestamp': '2025-11-10T20:29:10.066772'}
20:29:10 app.services.agent.langgraph_agent INFO   [Stream Event] on_progress 回调已调用
20:29:10 app.api.v1.agent INFO   [SSE] 发送 progress 事件: step=intent_analysis, desc=识别为：分析任务
20:29:10 app.services.agent.langgraph_agent INFO   [LangGraph] 处理分析请求（新架构）
20:29:10 Action.analysis INFO   [analysis] PromptManager已初始化
20:29:10 Action.analysis INFO   [analysis] work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=627feba4-2097-4f28-a3f3-7641d10f7f40
20:29:10 app.services.agent.langgraph_agent INFO   [LangGraph] AnalysisAction准备完成: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=627feba4-2097-4f28-a3f3-7641d10f7f40
20:29:10 app.services.agent.langgraph_agent INFO   [LangGraph] 处理analysis场景 (use_chatgpt=True)
20:30:13 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
20:30:13 app.api.callbacks.monitoring_callback INFO   [MonitoringCallback] LLM调用成功: run_id=cc79c28b-208b-4e05-ba25-072a08c3d6ed, model=gemini-2.5-pro, duration=63.11s, tokens=17047 (prompt=14735, completion=2312)
20:30:13 app.services.agent.langgraph_agent INFO   [LangGraph] 无需工具调用，结束流程
20:30:13 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: analysis_agent
20:30:13 app.services.agent.langgraph_agent INFO   [Stream Event] progress_event = {'type': 'progress', 'step': 'thinking', 'description': '正在分析内容...', 'node': 'analysis_agent', 'details': {}, 'timestamp': '2025-11-10T20:30:13.263173'}
20:30:13 app.api.v1.agent INFO   [Stream] Activity完成: intent_analysis (63.2s)
20:30:13 app.services.agent.langgraph_agent INFO   [Stream Event] on_progress 回调已调用
20:30:13 app.api.v1.agent INFO   [SSE] 发送 activity_complete 事件: step=intent_analysis, elapsed=63.2s
20:30:13 app.api.v1.agent INFO   [SSE] 发送 progress 事件: step=thinking, desc=正在分析内容...
20:30:13 app.services.agent.langgraph_agent INFO   [LangGraph Stream] 流式执行完成，共2个事件
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  1.58it/s]
20:30:14 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 重要度=0.90 | 长度=3485
20:30:14 app.services.context.store INFO   [ContextStore] 保存上下文: 0d901e52-11fd-43f8-acc4-35151912ebfb, token=11652
20:30:14 app.services.context.manager INFO   [ContextManager] 更新上下文: 0d901e52-11fd-43f8-acc4-35151912ebfb, 消息数=6, Token=11652
20:30:14 app.services.agent.langgraph_agent INFO   [Context] 上下文已更新: 0d901e52-11fd-43f8-acc4-35151912ebfb
20:30:14 app.api.v1.agent INFO   [Stream] 最后活动完成: thinking (1.2s)
20:30:14 app.api.v1.agent INFO   [SSE] 发送 activity_complete 事件: step=thinking, elapsed=1.2s
20:30:14 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: react, Stream complete