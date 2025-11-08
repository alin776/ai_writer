已注册策略: web_novel_11d - 网文11维度分析
12:21:02 app.utils.file_storage INFO   临时文件存储目录: D:\Temp\novelaide_exports
12:21:03 app.main INFO   [STARTUP] 监控中间件已注册: TraceMiddleware, MonitoringMiddleware
INFO:     Started server process [16660]
INFO:     Waiting for application startup.
12:21:03 app.main INFO   [STARTUP] 应用启动中...
12:21:03 app.core.database INFO   正在初始化数据库... (尝试 1/3)
12:21:04 app.core.database INFO   ✅ 数据库初始化成功
12:21:04 apscheduler.scheduler INFO   Adding job tentatively -- it will be properly scheduled when the scheduler starts
12:21:04 apscheduler.scheduler INFO   Added job "清理过期的去痕迹会话详情" to job store "default"
12:21:04 apscheduler.scheduler INFO   Scheduler started
12:21:04 app.tasks.cleanup_humanize_details INFO   定时任务调度器已启动
12:21:04 app.main INFO   [STARTUP] 开始预初始化同步Redis连接...
12:21:04 app.api.v1.agent INFO   [Redis] 全局连接池已创建
12:21:09 app.main INFO   [STARTUP] ✅ 同步Redis连接池预初始化完成
12:21:09 app.main INFO   [STARTUP] 开始初始化AsyncRedisSaver索引...
12:21:51 langgraph.checkpoint.redis.aio INFO   Redis client is a standalone client
12:21:51 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ AsyncRedisSaver索引预创建成功
12:21:51 app.main INFO   [STARTUP] AsyncRedisSaver索引初始化完成
12:21:51 app.main INFO   [STARTUP] 开始预加载Embedding模型...
12:21:51 app.services.vector_store_service INFO   🔄 预加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
12:21:51 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
12:21:51 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
12:22:01 app.services.vector_store_service INFO   ✅ Embedding模型预加载成功，耗时: 10.05秒
12:22:01 app.main INFO   [STARTUP] Embedding模型预加载完成
12:22:01 app.main INFO   [STARTUP] P0性能优化已暂时禁用（诊断模式）
12:22:01 app.main INFO   [STARTUP] 应用启动完成
INFO:     Application startup complete.
12:23:33 monitoring INFO   Registered health check: cpu_usage
12:23:33 monitoring INFO   Registered health check: memory_usage
12:23:33 monitoring INFO   Registered health check: disk_usage
12:23:33 monitoring INFO   Registered health check: process_status
12:23:33 monitoring INFO   Added alert rule: high_cpu_usage
12:23:33 monitoring INFO   Added alert rule: high_memory_usage
12:23:33 monitoring INFO   Added alert rule: low_disk_space
12:23:33 app.api.v1.auth INFO   [LOGIN] 尝试登录: 2072855200@qq.com
12:23:33 app.api.v1.auth INFO   [LOGIN] 会话创建成功: 602f5147-846a-4cde-95d3-405fa75f133f (127.0.0.1)
12:23:33 app.api.v1.auth INFO   [LOGIN] 登录成功: testuser_new-1 (602f5147-846a-4cde-95d3-405fa75f133f) from 127.0.0.1
12:23:33 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/auth/login
INFO:     127.0.0.1:51677 - "POST /api/v1/auth/login HTTP/1.1" 200 OK
12:23:33 app.services.ai.prompts INFO   Prompts loaded successfully from D:\Java\ai_writer\backend\app\services\ai\prompts\default.json
12:23:33 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
12:23:33 app.services.ai.http_ai_service INFO   ModelSelector 已启用
12:23:33 app.services.agent.cost_tracker INFO   CostTracker 初始化完成, 持久化: False
12:23:33 app.services.ai.http_ai_service INFO   CostTracker 已启用
12:23:34 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
12:23:34 app.api.v1.agent INFO   [LangGraph Agent] User: 602f5147-846a-4cde-95d3-405fa75f133f, Message: Hello, how are you today?...
12:23:34 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
12:23:34 app.services.ai.http_ai_service INFO   ModelSelector 已启用
12:23:34 app.services.ai.http_ai_service INFO   CostTracker 已启用
12:23:34 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
12:23:34 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ ContextManager已初始化
成功加载模板: intent_classifier (版本 2.0.0)
成功加载模板: writing_agent (版本 2.0.0)
成功加载模板: planning_agent (版本 2.0.0)
成功加载模板: tool_agent (版本 2.0.0)
成功加载模板: query_agent (版本 2.0.0)
12:23:34 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ PromptManager已初始化
12:23:34 app.services.agent.langgraph_agent INFO   [LangGraph] 使用 ChatOpenAI 模式（原生工具调用）
12:23:36 app.api.callbacks.monitoring_callback INFO   [MonitoringCallback] 已初始化
12:23:36 app.services.agent.langgraph_agent INFO   [LangGraph] 已创建MonitoringCallbackHandler
12:23:57 app.services.agent.langgraph_agent INFO   [LangGraph] OK 使用 AsyncRedisSaver（redis://localhost:6379/0，TTL=7天）
12:23:57 app.api.v1.agent INFO   [Global Agent] 创建全局Agent实例，MemorySaver将在请求间共享
12:24:19 redisvl.index.index INFO   Index already exists, not overwriting.
12:24:19 redisvl.index.index INFO   Index already exists, not overwriting.
12:24:19 redisvl.index.index INFO   Index already exists, not overwriting.
12:24:19 langgraph.checkpoint.redis.aio INFO   Redis client is a standalone client
12:24:19 app.services.agent.langgraph_agent INFO   [LangGraph] AsyncRedisSaver索引创建成功
12:24:19 app.services.agent.langgraph_agent INFO   [LangGraph] 意图分类
12:24:26 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
12:24:26 app.api.callbacks.monitoring_callback INFO   [MonitoringCallback] LLM调用成功: run_id=a745bf14-f753-431d-9236-e95275596a2f, model=gemini-2.5-pro, duration=7.68s, tokens=450 (prompt=449, completion=1)
12:24:26 app.services.agent.langgraph_agent INFO   [_generate_text] 使用ChatOpenAI生成文本，tokens=450
12:24:26 app.services.agent.langgraph_agent INFO   [LangGraph] 路由到: general
12:24:26 app.services.agent.actions.action_registry INFO   [ActionRegistry] 注册Action: echo (class=EchoAction, category=example)
12:24:26 app.services.agent.actions.action_registry INFO   [ActionRegistry] 注册Action: writing (class=WritingAction, category=content_creation)
12:24:26 app.services.agent.actions.action_registry INFO   [ActionRegistry] 注册Action: planning (class=PlanningAction, category=planning)
12:24:26 app.services.agent.actions.action_registry INFO   [ActionRegistry] 注册Action: analysis (class=AnalysisAction, category=analysis)
12:24:26 app.services.agent.actions.action_registry INFO   [ActionRegistry] 注册Action: stuck (class=StuckAction, category=writing_assistance)
12:24:26 app.services.agent.actions.action_registry INFO   [ActionRegistry] 注册Action: general_chat (class=GeneralChatAction, category=conversation)
12:24:26 app.services.agent.langgraph_agent INFO   [LangGraph] 处理一般对话（新架构）
12:24:26 Action.general_chat INFO   [general_chat] 准备一般对话，历史消息数: 1
12:24:26 app.services.agent.langgraph_agent INFO   [LangGraph] 使用system_prompt调用LLM: 你是友好的AI写作助手，以专业、简洁的方式回复用户。

【你的特点】
- 友好、专业、有耐心
- 简洁明了，避免冗长
- 善于引导用户使用功能

【你能做什么】
- 写作：帮助用户续写、创作小说内容
...
12:24:26 app.services.agent.langgraph_agent INFO   [LangGraph] 处理general场景 (use_chatgpt=True)
12:24:30 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
12:24:30 app.api.callbacks.monitoring_callback INFO   [MonitoringCallback] LLM调用成功: run_id=9c28e0c8-9dc8-4e69-b5b4-86fa5e144bbe, model=gemini-2.5-pro, duration=3.39s, tokens=704 (prompt=672, completion=32)
12:24:47 app.api.v1.agent INFO   [LangGraph Agent] User 602f5147-846a-4cde-95d3-405fa75f133f - Intent: general, Steps: 2
12:24:47 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat
INFO:     127.0.0.1:51680 - "POST /api/v1/agent/chat HTTP/1.1" 200 OK
12:24:47 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
12:24:47 app.services.ai.http_ai_service INFO   ModelSelector 已启用
12:24:47 app.services.ai.http_ai_service INFO   CostTracker 已启用
12:24:48 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
12:24:48 app.api.v1.agent INFO   [Chat Stream] Mode: planning
12:24:48 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: planning, Message: Help me write a story opening about a detective...
12:24:48 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:51793 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
12:24:48 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: Help me write a story opening about a detective...
12:25:10 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
12:25:10 app.api.callbacks.monitoring_callback INFO   [MonitoringCallback] LLM调用成功: run_id=cbf63311-6a5a-4a98-8701-023873f81e4c, model=gemini-2.5-pro, duration=21.71s, tokens=2892 (prompt=2501, completion=391)
12:25:10 app.services.agent.langgraph_agent INFO   [_generate_text] 使用ChatOpenAI生成文本，tokens=2892
12:25:10 app.services.agent.langgraph_agent INFO   [JSON解析] 方法2成功: 从```json块提取
12:25:10 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共4个任务，耗时: 21.71s
12:25:10 app.api.v1.agent INFO   [Stream] 规划生成: 4 个任务
12:25:10 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
12:25:10 app.services.agent.langgraph_agent INFO   [ParallelExecution] 任务分组: 并行=0, 串行=4
12:25:10 app.services.agent.langgraph_agent INFO   [ParallelExecution] 开始串行执行4个任务
12:25:10 app.services.agent.langgraph_agent INFO   [ParallelExecution] 串行任务1开始: 分析用户请求，明确核心创作任务是撰写一个全新的侦探故事开头。
12:25:10 app.api.v1.agent INFO   [Stream] 任务开始: 分析用户请求，明确核心创作任务是撰写一个全新的侦探故事开头。
12:25:10 app.services.agent.langgraph_agent INFO   [ParallelExecution] 串行任务1完成
12:25:10 app.api.v1.agent INFO   [Stream] 任务完成: 分析用户请求，明确核心创作任务是撰写一个全新的侦探故事开头。 (0.0s)
12:25:10 app.services.agent.langgraph_agent INFO   [ParallelExecution] 串行任务2开始: 构思故事开头的关键要素，包括侦探的性格特点、故事发生的场景氛围以及一个初始的悬念或钩子。
12:25:10 app.api.v1.agent INFO   [Stream] 任务开始: 构思故事开头的关键要素，包括侦探的性格特点、故事发生的场景氛围以及一个初始的悬念或钩子。
12:25:10 app.services.agent.langgraph_agent INFO   [ParallelExecution] 串行任务2完成
12:25:10 app.api.v1.agent INFO   [Stream] 任务完成: 构思故事开头的关键要素，包括侦探的性格特点、故事发生的场景氛围以及一个初始的悬念或钩子。 (0.0s)
12:25:10 app.services.agent.langgraph_agent INFO   [ParallelExecution] 串行任务3开始: 基于构思的要素，生成一段引人入胜的故事开头文本。
12:25:10 app.api.v1.agent INFO   [Stream] 任务开始: 基于构思的要素，生成一段引人入胜的故事开头文本。
12:25:10 app.services.agent.langgraph_agent ERROR   [ParallelExecution] 串行任务3最终失败: cannot access local variable 'asyncio' where it is not associated with a value
12:25:10 app.services.agent.langgraph_agent INFO   [ParallelExecution] 串行任务4开始: 对生成的文本进行润色，优化语言表达和节奏，使其更具悬疑感和吸引力。
12:25:10 app.api.v1.agent INFO   [Stream] 任务开始: 对生成的文本进行润色，优化语言表达和节奏，使其更具悬疑感和吸引力。
12:25:10 app.services.agent.langgraph_agent ERROR   [ParallelExecution] 串行任务4最终失败: cannot access local variable 'asyncio' where it is not associated with a value
12:25:10 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共4个任务，耗时: 0.01s
12:25:10 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
12:25:10 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=0, 输出型=4
12:25:10 app.services.agent.langgraph_agent INFO   [Response] 4个输出任务，简单拼接
12:25:10 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed
12:25:10 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
12:25:10 app.services.ai.http_ai_service INFO   ModelSelector 已启用
12:25:10 app.services.ai.http_ai_service INFO   CostTracker 已启用
12:25:11 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
12:25:11 app.api.v1.agent INFO   [Chat Stream] Mode: planning
12:25:11 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: planning, Message: Help me plan a fantasy novel outline with 5 chapte...
12:25:11 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:51858 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
12:25:11 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: Help me plan a fantasy novel outline with 5 chapte...
12:25:58 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
12:25:58 app.api.callbacks.monitoring_callback INFO   [MonitoringCallback] LLM调用成功: run_id=cbfb9dab-bc2d-40d5-8511-e3e55207d930, model=gemini-2.5-pro, duration=46.90s, tokens=5717 (prompt=4785, completion=932)
12:25:58 app.services.agent.langgraph_agent INFO   [_generate_text] 使用ChatOpenAI生成文本，tokens=5717
12:25:58 app.services.agent.langgraph_agent INFO   [JSON解析] 方法2成功: 从```json块提取
12:25:58 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共7个任务，耗时: 46.90s
12:25:58 app.api.v1.agent INFO   [Stream] 规划生成: 7 个任务
12:25:58 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
12:25:58 app.services.agent.langgraph_agent INFO   [ParallelExecution] 任务分组: 并行=1, 串行=6
12:25:58 app.services.agent.langgraph_agent INFO   [ParallelExecution] 开始并行执行1个任务
12:25:58 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务1开始: 检索奇幻小说创作的常见元素和结构，为构思故事提供灵感。
12:25:58 app.api.v1.agent INFO   [Stream] 任务开始: 检索奇幻小说创作的常见元素和结构，为构思故事提供灵感。
12:25:58 app.services.agent.langgraph_agent ERROR   [ParallelExecution] 并行任务1最终失败: 1 validation error for search_analysis_fragments_tool
work_id
  Input should be a valid string [type=string_type, input_value=None, input_type=NoneType]
    For further information visit https://errors.pydantic.dev/2.12/v/string_type
12:25:58 app.services.agent.langgraph_agent INFO   [ParallelExecution] 开始串行执行6个任务
12:25:58 app.services.agent.langgraph_agent INFO   [ParallelExecution] 串行任务2开始: 基于检索到的灵感，构思故事核心概念，并生成第一章大纲：主角介绍与激励事件。
12:25:58 app.api.v1.agent INFO   [Stream] 任务开始: 基于检索到的灵感，构思故事核心概念，并生成第一章大纲：主角介绍与激励事件。
12:25:58 app.services.agent.langgraph_agent ERROR   [ParallelExecution] 串行任务2最终失败: cannot access local variable 'asyncio' where it is not associated with a value
12:25:58 app.services.agent.langgraph_agent INFO   [ParallelExecution] 串行任务3开始: 基于第一章内容，生成第二章大纲：上升行动与初次考验。
12:25:58 app.api.v1.agent INFO   [Stream] 任务开始: 基于第一章内容，生成第二章大纲：上升行动与初次考验。
12:25:58 app.services.agent.langgraph_agent ERROR   [ParallelExecution] 串行任务3最终失败: cannot access local variable 'asyncio' where it is not associated with a value
12:25:58 app.services.agent.langgraph_agent INFO   [ParallelExecution] 串行任务4开始: 基于前两章内容，生成第三章大纲：中点转折与重大发现。
12:25:58 app.api.v1.agent INFO   [Stream] 任务开始: 基于前两章内容，生成第三章大纲：中点转折与重大发现。
12:25:58 app.services.agent.langgraph_agent ERROR   [ParallelExecution] 串行任务4最终失败: cannot access local variable 'asyncio' where it is not associated with a value
12:25:58 app.services.agent.langgraph_agent INFO   [ParallelExecution] 串行任务5开始: 基于前三章内容，生成第四章大纲：高潮前的准备。
12:25:58 app.api.v1.agent INFO   [Stream] 任务开始: 基于前三章内容，生成第四章大纲：高潮前的准备。
12:25:58 app.services.agent.langgraph_agent ERROR   [ParallelExecution] 串行任务5最终失败: cannot access local variable 'asyncio' where it is not associated with a value
12:25:58 app.services.agent.langgraph_agent INFO   [ParallelExecution] 串行任务6开始: 基于前四章内容，生成第五章大纲：高潮与结局。
12:25:58 app.api.v1.agent INFO   [Stream] 任务开始: 基于前四章内容，生成第五章大纲：高潮与结局。
12:25:58 app.services.agent.langgraph_agent ERROR   [ParallelExecution] 串行任务6最终失败: cannot access local variable 'asyncio' where it is not associated with a value
12:25:58 app.services.agent.langgraph_agent INFO   [ParallelExecution] 串行任务7开始: 整合并润色完整的五章节大纲，确保逻辑连贯，富有吸引力。
12:25:58 app.api.v1.agent INFO   [Stream] 任务开始: 整合并润色完整的五章节大纲，确保逻辑连贯，富有吸引力。
12:25:58 app.services.agent.langgraph_agent ERROR   [ParallelExecution] 串行任务7最终失败: cannot access local variable 'asyncio' where it is not associated with a value
12:25:58 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共7个任务，耗时: 0.02s
12:25:58 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
12:25:58 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=1, 输出型=6
12:25:58 app.services.agent.langgraph_agent INFO   [Response] 6个输出任务，简单拼接
12:25:58 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed
12:25:58 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
12:25:58 app.services.ai.http_ai_service INFO   ModelSelector 已启用
12:25:58 app.services.ai.http_ai_service INFO   CostTracker 已启用
12:25:58 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
12:25:58 app.api.v1.agent INFO   [LangGraph Agent] User: 602f5147-846a-4cde-95d3-405fa75f133f, Message: Say exactly: Hello World...
12:25:58 app.services.agent.langgraph_agent INFO   [LangGraph] 意图分类
12:26:05 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
12:26:05 app.api.callbacks.monitoring_callback INFO   [MonitoringCallback] LLM调用成功: run_id=013c8315-9496-48d1-860f-537b97acb918, model=gemini-2.5-pro, duration=6.92s, tokens=521 (prompt=520, completion=1)
12:26:05 app.services.agent.langgraph_agent INFO   [_generate_text] 使用ChatOpenAI生成文本，tokens=521
12:26:05 app.services.agent.langgraph_agent INFO   [LangGraph] 路由到: general
12:26:05 app.services.agent.langgraph_agent INFO   [LangGraph] 处理一般对话（新架构）
12:26:05 Action.general_chat INFO   [general_chat] 准备一般对话，历史消息数: 1
12:26:05 app.services.agent.langgraph_agent INFO   [LangGraph] 使用system_prompt调用LLM: 你是友好的AI写作助手，以专业、简洁的方式回复用户。

【你的特点】
- 友好、专业、有耐心
- 简洁明了，避免冗长
- 善于引导用户使用功能

【你能做什么】
- 写作：帮助用户续写、创作小说内容
...
12:26:05 app.services.agent.langgraph_agent INFO   [LangGraph] 处理general场景 (use_chatgpt=True)
12:26:08 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
12:26:08 app.api.callbacks.monitoring_callback INFO   [MonitoringCallback] LLM调用成功: run_id=e66c92af-d34b-4ac8-8fd3-a8290030f907, model=gemini-2.5-pro, duration=2.47s, tokens=654 (prompt=652, completion=2)
12:26:08 app.api.v1.agent INFO   [LangGraph Agent] User 602f5147-846a-4cde-95d3-405fa75f133f - Intent: general, Steps: 2
12:26:08 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat
INFO:     127.0.0.1:52117 - "POST /api/v1/agent/chat HTTP/1.1" 200 OK
12:26:08 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
12:26:08 app.services.ai.http_ai_service INFO   ModelSelector 已启用
12:26:08 app.services.ai.http_ai_service INFO   CostTracker 已启用
12:26:08 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
12:26:08 app.api.v1.agent INFO   [LangGraph Agent] User: 602f5147-846a-4cde-95d3-405fa75f133f, Message: Write a creative greeting...
12:26:08 app.services.agent.langgraph_agent INFO   [LangGraph] 意图分类
12:26:18 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
12:26:18 app.api.callbacks.monitoring_callback INFO   [MonitoringCallback] LLM调用成功: run_id=9c3f796b-8ab3-40b7-bdb4-b1863d03ce95, model=gemini-2.5-pro, duration=9.37s, tokens=915 (prompt=914, completion=1)
12:26:18 app.services.agent.langgraph_agent INFO   [_generate_text] 使用ChatOpenAI生成文本，tokens=915
12:26:18 app.services.agent.langgraph_agent INFO   [LangGraph] 路由到: writing
12:26:18 app.services.agent.langgraph_agent INFO   [LangGraph] 处理写作请求（新架构）
12:26:18 Action.writing INFO   [writing] PromptManager已初始化
12:26:18 Action.writing INFO   [writing] work_id=None, chapter_id=None, phase=None, chapter_num=None
12:26:18 app.services.agent.langgraph_agent INFO   [LangGraph] WritingAction准备完成: phase=None, chapter_num=None
12:26:18 app.services.agent.langgraph_agent INFO   [LangGraph] 处理writing场景 (use_chatgpt=True)
12:26:25 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
12:26:25 app.api.callbacks.monitoring_callback INFO   [MonitoringCallback] LLM调用成功: run_id=0748fc6f-80fd-445f-83a2-61408bc129b2, model=gemini-2.5-pro, duration=7.64s, tokens=1562 (prompt=1425, completion=137)
12:26:25 app.services.agent.langgraph_agent INFO   [LangGraph] 无需工具调用，结束流程
12:26:25 app.api.v1.agent INFO   [LangGraph Agent] User 602f5147-846a-4cde-95d3-405fa75f133f - Intent: writing, Steps: 2
12:26:25 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat
INFO:     127.0.0.1:52160 - "POST /api/v1/agent/chat HTTP/1.1" 200 OK
