21:00:23 app.services.ai.prompts INFO   Prompts loaded successfully from D:\Java\ai_writer\backend\app\services\ai\prompts\default.json
21:00:23 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
21:00:23 app.services.ai.http_ai_service INFO   ModelSelector 已启用
21:00:23 app.services.agent.cost_tracker INFO   CostTracker 初始化完成, 持久化: False
21:00:23 app.services.ai.http_ai_service INFO   CostTracker 已启用
21:00:25 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
21:00:25 app.api.v1.agent INFO   [Chat Stream] Mode: react
21:00:25 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:51332 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
21:00:46 app.core.redis INFO   ✅ Redis connected: redis://localhost:6379/0
21:00:46 app.api.v1.agent INFO   [Session] 创建新会话归属: 04455be0-8032-4d45-bc77-71afb4c066d9 -> 602f5147-846a-4cde-95d3-405fa75f133f
21:00:46 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: react, Message: 请基于《一夕千悟》前4章的内容，续写第5章。 要求： 1. 保持段融的人设和成长轨迹 2. 延续修仙...
21:00:46 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
21:00:46 app.services.ai.http_ai_service INFO   ModelSelector 已启用
21:00:46 app.services.ai.http_ai_service INFO   CostTracker 已启用
21:00:46 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
21:00:47 chromadb.telemetry.product.posthog INFO   Anonymized telemetry enabled. See                     https://docs.trychroma.com/telemetry for more information.
21:00:47 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
21:00:54 app.services.context.vector_memory_store INFO   ✅ VectorMemoryStore初始化成功 | 目录=./data/chroma_db | 模型=paraphrase-multilingual-MiniLM-L12-v2 | 集合=user_memories
21:00:54 app.services.context.manager INFO   ✅ VectorMemoryStore 已初始化
21:00:54 app.services.context.manager INFO   ✅ ContextManager: 长期记忆已启用 (user_id=None)
21:00:54 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ ContextManager已初始化（长期记忆已启用）
成功加载模板: intent_classifier (版本 2.0.0)
成功加载模板: writing_agent (版本 2.0.0)
成功加载模板: planning_agent (版本 2.0.0)
成功加载模板: tool_agent (版本 2.0.0)
成功加载模板: query_agent (版本 2.0.0)
21:00:54 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ PromptManager已初始化
21:00:54 app.services.agent.langgraph_agent INFO   [LangGraph] 使用 ChatOpenAI 模式（原生工具调用）
21:00:55 app.api.callbacks.monitoring_callback INFO   [MonitoringCallback] 已初始化
21:00:55 app.services.agent.langgraph_agent INFO   [LangGraph] 已创建MonitoringCallbackHandler
21:01:17 app.services.agent.langgraph_agent INFO   [LangGraph] OK 使用 AsyncRedisSaver（redis://localhost:6379/0，TTL=7天）
21:01:17 app.api.v1.agent INFO   [Global Agent] 创建全局Agent实例，MemorySaver将在请求间共享
21:01:17 app.services.agent.langgraph_agent INFO   [LangGraph Stream] 开始流式执行: 请基于《一夕千悟》前4章的内容，续写第5章。 要求： 1. 保持段融的人设和成长轨迹 2. 延续修仙...
21:01:38 redisvl.index.index INFO   Index already exists, not overwriting.
21:01:38 redisvl.index.index INFO   Index already exists, not overwriting.
21:01:38 redisvl.index.index INFO   Index already exists, not overwriting.
21:01:38 langgraph.checkpoint.redis.aio INFO   Redis client is a standalone client
21:01:38 app.services.agent.langgraph_agent INFO   [LangGraph] AsyncRedisSaver索引创建成功
21:01:38 app.services.agent.langgraph_agent INFO   [Context] 设置用户ID: 602f5147-846a-4cde-95d3-405fa75f133f
21:01:38 app.services.agent.langgraph_agent INFO   [Intent] 开始识别意图: 请基于《一夕千悟》前4章的内容，续写第5章。 要求： 1. 保持段融的人设和成长轨迹 2. 延续修仙...
21:01:48 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
21:01:48 app.api.callbacks.monitoring_callback INFO   [MonitoringCallback] LLM调用成功: run_id=ca487a18-f35a-4c47-a519-53b0bdb43b39, model=gemini-2.5-pro, duration=9.89s, tokens=1354 (prompt=1279, completion=75)
21:01:48 app.services.agent.langgraph_agent INFO   [_generate_text] 使用ChatOpenAI生成文本，tokens=1354
21:01:48 app.services.agent.langgraph_agent INFO   [Intent] 识别结果: writing, 置信度: 0.95
21:01:48 app.services.agent.langgraph_agent INFO   [Intent] 用户意图: writing, 置信度: 0.95, 原因: 用户明确要求“续写第5章”，这是一个直接的小说内容创作指令，完全符合writing意图的定义。
21:01:48 app.services.agent.langgraph_agent INFO   [Intent] 选择 Prompt 模板: writing_agent, 版本: 2.0.0
21:01:48 app.services.context.monitoring_integration INFO   ✅ ContextManager监控收集器已初始化
21:01:48 app.services.context.store INFO   [ContextStore] Redis连接成功
21:02:09 app.services.context.manager INFO   [ContextManager] 创建新上下文: 04455be0-8032-4d45-bc77-71afb4c066d9
21:02:09 app.services.context.token_counter INFO   ✅ tiktoken初始化成功，模型: gpt-4
21:02:09 app.services.context.manager INFO   [ContextManager] Session 04455be0-8032-4d45-bc77-71afb4c066d9: 685/8000 tokens
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  4.48it/s]
21:02:10 app.services.context.vector_memory_store INFO   🔍 检索记忆 | 查询='请基于《一夕千悟》前4章的内容，续写第5章。 要求： 1. ...' | 用户=602f5147-846a-4cde-95d3-405fa75f133f | 找到=3条 | 阈值=0.3
21:02:10 app.services.context.manager INFO   🔍 检索长期记忆 | 查询='请基于《一夕千悟》前4章的内容，续写第5章。 要求： 1. ...' | 找到=3条 | 阈值=0.3
21:02:10 app.services.context.monitoring_integration INFO   [Monitor] 上下文构建: 2条消息, 685 tokens, 耗时 21846.99ms
21:02:10 app.services.agent.langgraph_agent INFO   [Context] 加载上下文: {'session_id': '04455be0-8032-4d45-bc77-71afb4c066d9', 'token_count': 685, 'short_memory_size': 0, 'has_summary': False, 'compression_triggered': False, 'long_term_memories': 3, 'adaptive_budget_enabled': False, 'task_type': None}
21:02:10 app.services.agent.langgraph_agent INFO   [LangGraph] 意图分类
21:02:20 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
21:02:20 app.api.callbacks.monitoring_callback INFO   [MonitoringCallback] LLM调用成功: run_id=077fef2b-aa9b-47c8-94df-8ad571e94802, model=gemini-2.5-pro, duration=10.44s, tokens=760 (prompt=759, completion=1)
21:02:20 app.services.agent.langgraph_agent INFO   [_generate_text] 使用ChatOpenAI生成文本，tokens=760
21:02:20 app.services.agent.langgraph_agent INFO   [LangGraph] 路由到: writing
21:02:20 app.services.agent.actions.action_registry INFO   [ActionRegistry] 注册Action: echo (class=EchoAction, category=example)
21:02:20 app.services.agent.actions.action_registry INFO   [ActionRegistry] 注册Action: writing (class=WritingAction, category=content_creation)
21:02:20 app.services.agent.actions.action_registry INFO   [ActionRegistry] 注册Action: planning (class=PlanningAction, category=planning)
21:02:20 app.services.agent.actions.action_registry INFO   [ActionRegistry] 注册Action: analysis (class=AnalysisAction, category=analysis)
21:02:20 app.services.agent.actions.action_registry INFO   [ActionRegistry] 注册Action: stuck (class=StuckAction, category=writing_assistance)
21:02:20 app.services.agent.actions.action_registry INFO   [ActionRegistry] 注册Action: general_chat (class=GeneralChatAction, category=conversation)
21:02:20 app.services.agent.langgraph_agent INFO   [LangGraph] 处理写作请求（新架构）
21:02:20 Action.writing INFO   [writing] PromptManager已初始化
21:02:20 Action.writing INFO   [writing] 从消息中识别到章节号: 5
21:02:20 Action.writing INFO   [writing] 章节 5 属于阶段: opening
21:02:20 Action.writing INFO   [writing] work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=627feba4-2097-4f28-a3f3-7641d10f7f40, phase=opening, chapter_num=5
21:02:20 app.services.agent.langgraph_agent INFO   [LangGraph] WritingAction准备完成: phase=opening, chapter_num=5
21:02:20 app.services.agent.langgraph_agent INFO   [LangGraph] 处理writing场景 (use_chatgpt=True)
21:02:50 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
21:02:50 app.api.callbacks.monitoring_callback INFO   [MonitoringCallback] LLM调用成功: run_id=de993fd0-fdd5-42e4-b152-6bfc25183a2b, model=gemini-2.5-pro, duration=29.87s, tokens=3830 (prompt=3323, completion=507)
21:02:50 app.services.agent.langgraph_agent INFO   [LangGraph] 检测到工具调用: 1 个工具
21:02:50 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: complex
21:02:50 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=content_creation, 模型=gemini-2.5-pro, 原因=任务复杂度为 complex; 任务类型: content_creation; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$5.0 per 1M tokens)
21:02:50 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.8, task_type=TaskType.CONTENT_CREATION
21:02:53 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/2 200 OK"
21:02:53 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
21:03:23 app.services.ai.http_ai_service INFO   API 响应完成，共接收 18 个数据块，总长度: 1435
21:03:23 app.services.ai.http_ai_service INFO   流式响应Token统计: 3637 (prompt=2532, completion=1105)
21:03:23 app.services.agent.cost_tracker INFO   [CostTracker] 记录API调用: gemini-2.5-pro, tokens: 2532+1105=3637, cost: $0.000209
21:03:23 app.services.ai.http_ai_service INFO   [CostTracker] API调用已记录: tokens=2532+1105, cost=$0.000209, time=32.73s
21:03:23 app.services.agent.langgraph_agent INFO   [LangGraph] 工具执行完毕，路由回: writing_agent
21:03:23 app.services.agent.langgraph_agent INFO   [LangGraph] 处理写作请求（新架构）
21:03:23 Action.writing INFO   [writing] PromptManager已初始化
21:03:23 Action.writing INFO   [writing] work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=627feba4-2097-4f28-a3f3-7641d10f7f40, phase=None, chapter_num=None
21:03:23 app.services.agent.langgraph_agent INFO   [LangGraph] WritingAction准备完成: phase=None, chapter_num=None
21:03:23 app.services.agent.langgraph_agent INFO   [LangGraph] 处理writing场景 (use_chatgpt=True)
21:03:23 app.services.agent.langgraph_agent INFO   [LangGraph] writing - 处理工具执行结果 (ChatOpenAI)
21:03:44 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
21:03:44 app.api.callbacks.monitoring_callback INFO   [MonitoringCallback] LLM调用成功: run_id=17c0d576-0d27-44a3-92b6-3820325d487b, model=gemini-2.5-pro, duration=21.18s, tokens=2052 (prompt=509, completion=1543)
21:03:44 app.services.agent.langgraph_agent INFO   [LangGraph] 无需工具调用，结束流程
21:03:44 app.services.agent.langgraph_agent INFO   [LangGraph Stream] 流式执行完成，共4个事件
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  8.61it/s]
21:03:44 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 重要度=0.90 | 长度=88
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  5.36it/s]
21:03:45 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 重要度=0.70 | 长度=2077
21:03:45 app.services.context.store INFO   [ContextStore] 保存上下文: 04455be0-8032-4d45-bc77-71afb4c066d9, token=3478
21:03:45 app.services.context.manager INFO   [ContextManager] 更新上下文: 04455be0-8032-4d45-bc77-71afb4c066d9, 消息数=2, Token=3478
21:03:45 app.services.agent.langgraph_agent INFO   [Context] 上下文已更新: 04455be0-8032-4d45-bc77-71afb4c066d9
21:03:45 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: react, Stream completed
21:04:51 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
21:04:51 app.services.ai.http_ai_service INFO   ModelSelector 已启用
21:04:51 app.services.ai.http_ai_service INFO   CostTracker 已启用
21:04:53 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
21:04:53 app.api.v1.agent INFO   [Chat Stream] Mode: react
21:04:53 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:62379 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
21:04:53 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: react, Message: 基于《一夕千悟》现有内容，为主角段融制定后续20章的详细成长大纲。 要求： 1. 涵盖从杂役弟子到高...
21:04:53 app.services.agent.langgraph_agent INFO   [LangGraph Stream] 开始流式执行: 基于《一夕千悟》现有内容，为主角段融制定后续20章的详细成长大纲。 要求： 1. 涵盖从杂役弟子到高...
21:04:53 app.services.agent.langgraph_agent INFO   [Context] 设置用户ID: 602f5147-846a-4cde-95d3-405fa75f133f
21:04:53 app.services.agent.langgraph_agent INFO   [Intent] 开始识别意图: 基于《一夕千悟》现有内容，为主角段融制定后续20章的详细成长大纲。 要求： 1. 涵盖从杂役弟子到高...
21:05:07 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
21:05:07 app.api.callbacks.monitoring_callback INFO   [MonitoringCallback] LLM调用成功: run_id=9722aa4d-4063-497d-b0c3-2ddddc365bba, model=gemini-2.5-pro, duration=14.04s, tokens=1848 (prompt=1760, completion=88)
21:05:07 app.services.agent.langgraph_agent INFO   [_generate_text] 使用ChatOpenAI生成文本，tokens=1848
21:05:07 app.services.agent.langgraph_agent INFO   [Intent] 识别结果: planning, 置信度: 0.95
21:05:07 app.services.agent.langgraph_agent INFO   [Intent] 用户意图: planning, 置信度: 0.95, 原因: 用户明确要求制定“后续20章的详细成长大纲”，包含“成长路径”、“情节节点”、“冲突和挑战”，这些都属于小说规划的核心内容。
21:05:07 app.services.agent.langgraph_agent INFO   [Intent] 选择 Prompt 模板: planning_agent, 版本: 2.0.0
21:05:07 app.services.context.store INFO   [ContextStore] 加载上下文: 04455be0-8032-4d45-bc77-71afb4c066d9, 2条消息
21:05:07 app.services.context.manager INFO   [ContextManager] Session 04455be0-8032-4d45-bc77-71afb4c066d9: 3478/8000 tokens
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  8.97it/s]
21:05:07 app.services.context.vector_memory_store INFO   🔍 检索记忆 | 查询='基于《一夕千悟》现有内容，为主角段融制定后续20章的详细成长...' | 用户=602f5147-846a-4cde-95d3-405fa75f133f | 找到=3条 | 阈值=0.3
21:05:07 app.services.context.manager INFO   🔍 检索长期记忆 | 查询='基于《一夕千悟》现有内容，为主角段融制定后续20章的详细成长...' | 找到=3条 | 阈值=0.3
21:05:07 app.services.context.monitoring_integration INFO   [Monitor] 上下文构建: 4条消息, 3478 tokens, 耗时 141.76ms
21:05:07 app.services.agent.langgraph_agent INFO   [Context] 加载上下文: {'session_id': '04455be0-8032-4d45-bc77-71afb4c066d9', 'token_count': 3478, 'short_memory_size': 2, 'has_summary': False, 'compression_triggered': False, 'long_term_memories': 3, 'adaptive_budget_enabled': False, 'task_type': None}
21:05:07 app.services.agent.langgraph_agent INFO   [LangGraph] 意图分类
21:05:17 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
21:05:17 app.api.callbacks.monitoring_callback INFO   [MonitoringCallback] LLM调用成功: run_id=5278e2cf-60df-4d65-89d1-95db88915850, model=gemini-2.5-pro, duration=10.48s, tokens=936 (prompt=935, completion=1)
21:05:17 app.services.agent.langgraph_agent INFO   [_generate_text] 使用ChatOpenAI生成文本，tokens=936
21:05:17 app.services.agent.langgraph_agent INFO   [LangGraph] 路由到: planning
21:05:17 app.services.agent.langgraph_agent INFO   [LangGraph] 处理规划请求（新架构）
21:05:17 Action.planning INFO   [planning] PromptManager已初始化
21:05:17 Action.planning INFO   [planning] work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350
21:05:17 app.services.agent.langgraph_agent INFO   [LangGraph] 处理planning场景 (use_chatgpt=True)
21:06:24 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
21:06:24 app.api.callbacks.monitoring_callback INFO   [MonitoringCallback] LLM调用成功: run_id=84aff4d8-b02f-4977-b96f-812ef9d1d9a1, model=gemini-2.5-pro, duration=67.12s, tokens=10326 (prompt=7575, completion=2751)
21:06:24 app.services.agent.langgraph_agent INFO   [LangGraph] 无需工具调用，结束流程
21:06:24 app.services.agent.langgraph_agent INFO   [LangGraph Stream] 流式执行完成，共2个事件
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 15.71it/s]
21:06:25 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 重要度=0.90 | 长度=105
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 15.91it/s]
21:06:25 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 重要度=0.90 | 长度=3946
21:06:25 app.services.context.store INFO   [ContextStore] 保存上下文: 04455be0-8032-4d45-bc77-71afb4c066d9, token=7837
21:06:25 app.services.context.manager INFO   [ContextManager] 更新上下文: 04455be0-8032-4d45-bc77-71afb4c066d9, 消息数=4, Token=7837
21:06:25 app.services.agent.langgraph_agent INFO   [Context] 上下文已更新: 04455be0-8032-4d45-bc77-71afb4c066d9
21:06:25 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: react, Stream completed
21:07:34 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
21:07:34 app.services.ai.http_ai_service INFO   ModelSelector 已启用
21:07:34 app.services.ai.http_ai_service INFO   CostTracker 已启用
21:07:35 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
21:07:35 app.api.v1.agent INFO   [Chat Stream] Mode: react
21:07:35 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
21:07:35 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: react, Message: 请深度分析《一夕千悟》主角段融的以下方面：   1. 性格特征和心理变化   2. 能力体系和成长轨...
INFO:     127.0.0.1:58356 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
21:07:35 app.services.agent.langgraph_agent INFO   [LangGraph Stream] 开始流式执行: 请深度分析《一夕千悟》主角段融的以下方面：   1. 性格特征和心理变化   2. 能力体系和成长轨...
21:07:35 app.services.agent.langgraph_agent INFO   [Context] 设置用户ID: 602f5147-846a-4cde-95d3-405fa75f133f
21:07:35 app.services.agent.langgraph_agent INFO   [Intent] 开始识别意图: 请深度分析《一夕千悟》主角段融的以下方面：   1. 性格特征和心理变化   2. 能力体系和成长轨...
21:07:50 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
21:07:50 app.api.callbacks.monitoring_callback INFO   [MonitoringCallback] LLM调用成功: run_id=e219f4a3-53ef-4f12-80b2-2b2b1f9b755f, model=gemini-2.5-pro, duration=15.39s, tokens=1727 (prompt=1644, completion=83)
21:07:50 app.services.agent.langgraph_agent INFO   [_generate_text] 使用ChatOpenAI生成文本，tokens=1727
21:07:50 app.services.agent.langgraph_agent INFO   [Intent] 识别结果: planning, 置信度: 0.95
21:07:50 app.services.agent.langgraph_agent INFO   [Intent] 用户意图: planning, 置信度: 0.95, 原因: 用户要求深度分析角色的性格、能力和人际关系，这属于角色设定的范畴，是小说规划的一部分。
21:07:50 app.services.agent.langgraph_agent INFO   [Intent] 选择 Prompt 模板: planning_agent, 版本: 2.0.0
21:07:50 app.services.context.store INFO   [ContextStore] 加载上下文: 04455be0-8032-4d45-bc77-71afb4c066d9, 4条消息
21:07:50 app.services.context.manager INFO   [ContextManager] Session 04455be0-8032-4d45-bc77-71afb4c066d9: 7837/8000 tokens
21:07:50 app.services.context.manager WARNING   [ContextManager] Token使用率过高 (7837/8000), 触发压缩
21:07:50 app.services.context.manager INFO   [ContextManager] 开始压缩: 04455be0-8032-4d45-bc77-71afb4c066d9
21:07:50 app.services.context.manager INFO   [ContextManager] 消息数不足，无需压缩
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 43.47it/s]
21:07:51 app.services.context.vector_memory_store INFO   🔍 检索记忆 | 查询='请深度分析《一夕千悟》主角段融的以下方面：   1. 性格特...' | 用户=602f5147-846a-4cde-95d3-405fa75f133f | 找到=3条 | 阈值=0.3
21:07:51 app.services.context.manager INFO   🔍 检索长期记忆 | 查询='请深度分析《一夕千悟》主角段融的以下方面：   1. 性格特...' | 找到=3条 | 阈值=0.3
21:07:51 app.services.context.monitoring_integration INFO   [Monitor] 上下文构建: 6条消息, 7837 tokens, 耗时 47.69ms
21:07:51 app.services.agent.langgraph_agent INFO   [Context] 加载上下文: {'session_id': '04455be0-8032-4d45-bc77-71afb4c066d9', 'token_count': 7837, 'short_memory_size': 4, 'has_summary': False, 'compression_triggered': True, 'long_term_memories': 3, 'adaptive_budget_enabled': False, 'task_type': None}
21:07:51 app.services.agent.langgraph_agent INFO   [LangGraph] 意图分类
21:07:59 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
21:07:59 app.api.callbacks.monitoring_callback INFO   [MonitoringCallback] LLM调用成功: run_id=b3066c6f-00e8-4295-b347-be3b9b10d9e4, model=gemini-2.5-pro, duration=8.24s, tokens=632 (prompt=631, completion=1)
21:07:59 app.services.agent.langgraph_agent INFO   [_generate_text] 使用ChatOpenAI生成文本，tokens=632
21:07:59 app.services.agent.langgraph_agent INFO   [LangGraph] 路由到: analysis
21:07:59 app.services.agent.langgraph_agent INFO   [LangGraph] 处理分析请求（新架构）
21:07:59 Action.analysis INFO   [analysis] PromptManager已初始化
21:07:59 Action.analysis INFO   [analysis] work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=627feba4-2097-4f28-a3f3-7641d10f7f40
21:07:59 app.services.agent.langgraph_agent INFO   [LangGraph] AnalysisAction准备完成: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=627feba4-2097-4f28-a3f3-7641d10f7f40
21:07:59 app.services.agent.langgraph_agent INFO   [LangGraph] 处理analysis场景 (use_chatgpt=True)
21:08:49 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
21:08:49 app.api.callbacks.monitoring_callback INFO   [MonitoringCallback] LLM调用成功: run_id=bf3ed132-0062-4b8f-846c-d5ceebad26df, model=gemini-2.5-pro, duration=50.39s, tokens=15982 (prompt=13822, completion=2160)
21:08:49 app.services.agent.langgraph_agent INFO   [LangGraph] 无需工具调用，结束流程
21:08:49 app.services.agent.langgraph_agent INFO   [LangGraph Stream] 流式执行完成，共2个事件
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  4.60it/s]
21:08:50 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 重要度=0.90 | 长度=3230
21:08:50 app.services.context.store INFO   [ContextStore] 保存上下文: 04455be0-8032-4d45-bc77-71afb4c066d9, token=11346
21:08:50 app.services.context.manager INFO   [ContextManager] 更新上下文: 04455be0-8032-4d45-bc77-71afb4c066d9, 消息数=6, Token=11346
21:08:50 app.services.agent.langgraph_agent INFO   [Context] 上下文已更新: 04455be0-8032-4d45-bc77-71afb4c066d9
21:08:50 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: react, Stream completed
