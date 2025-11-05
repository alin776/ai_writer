18:56:40 app.services.ai.prompts INFO   Prompts loaded successfully from D:\Java\ai_writer\backend\app\services\ai\prompts\default.json
18:56:40 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
18:56:40 app.services.ai.http_ai_service INFO   ModelSelector 已启用
18:56:40 app.services.agent.cost_tracker INFO   CostTracker 初始化完成, 持久化: False
18:56:40 app.services.ai.http_ai_service INFO   CostTracker 已启用
18:56:41 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
INFO:     127.0.0.1:65141 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
18:56:41 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Message: 段融的金手指能力是什么？具体有什么效果？...
18:57:02 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 记忆上下文加载完成，耗时: 21.03s
18:57:02 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
18:57:02 app.services.ai.http_ai_service INFO   ModelSelector 已启用
18:57:02 app.services.ai.http_ai_service INFO   CostTracker 已启用
18:57:04 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
18:57:04 app.services.agent.langgraph_agent INFO   [LangGraph] 使用 HTTPAIService 模式（手动工具调用，绕过 Cloudflare）
18:57:25 app.services.agent.langgraph_agent INFO   [LangGraph] OK 使用 AsyncRedisSaver（redis://localhost:6379/0，TTL=7天）
18:57:25 app.api.v1.agent INFO   [Global Agent] 创建全局Agent实例，MemorySaver将在请求间共享
18:57:25 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ Agent实例获取完成，耗时: 22.31s
18:57:25 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 初始化总耗时: 43.35s
18:57:25 app.services.agent.langgraph_agent INFO   [Planning] ⏱️ chat_with_planning方法开始
18:57:46 app.services.agent.langgraph_agent INFO   [Planning] ⏱️ 无历史checkpoint，耗时: 21.08s
18:57:46 app.services.agent.langgraph_agent INFO   [Planning] ⏱️ 规划前准备完成，总耗时: 21.08s
18:57:46 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: 段融的金手指能力是什么？具体有什么效果？...
18:57:46 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
18:57:46 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.03/$0.12 per 1M tokens)
18:57:46 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=1000, temp=0.3, task_type=TaskType.SIMPLE_QA
18:57:48 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/2 200 OK"
18:57:48 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:57:52 app.services.ai.http_ai_service INFO   API 响应完成，共接收 4 个数据块，总长度: 544
18:57:52 app.services.ai.http_ai_service INFO   流式响应Token统计: 2518 (prompt=2290, completion=228)
18:57:52 app.services.agent.cost_tracker INFO   [CostTracker] 记录API调用: gemini-2.5-pro, tokens: 2290+228=2518, cost: $0.000096
18:57:52 app.services.ai.http_ai_service INFO   [CostTracker] API调用已记录: tokens=2290+228, cost=$0.000096, time=5.94s
18:57:52 app.services.agent.langgraph_agent INFO   [JSON解析] 方法2成功: 从```json块提取
18:57:52 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共2个任务，耗时: 5.94s
18:57:52 app.services.agent.langgraph_agent INFO   [Planning] ⏱️ 从方法开始到规划完成总耗时: 27.02s
18:57:52 app.api.v1.agent INFO   [Stream] 规划生成: 2 个任务
18:57:52 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
18:57:52 app.services.agent.langgraph_agent INFO   [ParallelExecution] 任务分组: 并行=1, 串行=1
18:57:52 app.services.agent.langgraph_agent INFO   [ParallelExecution] 开始并行执行1个任务
18:57:52 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务1开始: 搜索关于“段融”的金手指能力和效果的相关信息片段
18:57:52 app.api.v1.agent INFO   [Stream] 任务开始: 搜索关于“段融”的金手指能力和效果的相关信息片段
18:57:52 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=段融 金手指 能力 效果...
18:57:52 app.services.vector_store_service INFO   正在加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
18:57:52 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
18:57:52 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
18:57:59 app.services.vector_store_service INFO   Embedding模型加载成功
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 25.69it/s]
18:57:59 app.services.vector_store_service INFO   检索到 5 个相关结果（阈值=0.3）
18:57:59 app.services.agent.langgraph_agent INFO   [search_analysis_fragments_tool] RAG检索成功: 找到5个相关片段
18:57:59 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务1完成
18:57:59 app.api.v1.agent INFO   [Stream] 任务完成: 搜索关于“段融”的金手指能力和效果的相关信息片段 (0.0s)
18:57:59 app.services.agent.langgraph_agent INFO   [ParallelExecution] 开始串行执行1个任务
18:57:59 app.services.agent.langgraph_agent INFO   [ParallelExecution] 串行任务2开始: 分析搜索到的片段，明确段融的金手指能力是什么，以及其具体效果
18:57:59 app.api.v1.agent INFO   [Stream] 任务开始: 分析搜索到的片段，明确段融的金手指能力是什么，以及其具体效果
18:57:59 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
18:57:59 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.075/$0.3 per 1M tokens)
18:57:59 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
18:58:02 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/2 200 OK"
18:58:02 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:58:09 app.services.ai.http_ai_service INFO   API 响应完成，共接收 11 个数据块，总长度: 836
18:58:09 app.services.ai.http_ai_service INFO   流式响应Token统计: 1587 (prompt=1068, completion=519)
18:58:09 app.services.agent.cost_tracker INFO   [CostTracker] 记录API调用: gemini-2.5-pro, tokens: 1068+519=1587, cost: $0.000094
18:58:09 app.services.ai.http_ai_service INFO   [CostTracker] API调用已记录: tokens=1068+519, cost=$0.000094, time=10.07s
18:58:09 app.services.agent.langgraph_agent INFO   [ParallelExecution] 串行任务2完成
18:58:09 app.api.v1.agent INFO   [Stream] 任务完成: 分析搜索到的片段，明确段融的金手指能力是什么，以及其具体效果 (0.0s)
18:58:09 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共2个任务
18:58:09 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
18:58:09 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=1, 输出型=1
18:58:09 app.services.agent.langgraph_agent INFO   [Response] 单个分析任务(analyze_text_tool)，使用AI格式化
18:58:09 app.services.agent.langgraph_agent INFO   [Summarization] 使用AI整合任务结果
18:58:09 app.services.agent.langgraph_agent INFO   [Summarization] 上下文压缩: 原始=7590字符, 压缩后=2949字符, 压缩率=62%
18:58:09 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
18:58:09 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.075/$0.3 per 1M tokens)
18:58:09 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
18:58:11 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/2 200 OK"
18:58:11 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:58:18 app.services.ai.http_ai_service INFO   API 响应完成，共接收 8 个数据块，总长度: 752
18:58:18 app.services.ai.http_ai_service INFO   流式响应Token统计: 3622 (prompt=3165, completion=457)
18:58:18 app.services.agent.cost_tracker INFO   [CostTracker] 记录API调用: gemini-2.5-pro, tokens: 3165+457=3622, cost: $0.000150
18:58:18 app.services.ai.http_ai_service INFO   [CostTracker] API调用已记录: tokens=3165+457, cost=$0.000150, time=8.54s
18:58:18 app.services.agent.langgraph_agent INFO   [Planning] 已保存 2 条新消息到checkpointer (总计: 2)
18:58:18 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Stream completed
INFO:     127.0.0.1:58569 - "OPTIONS /api/v1/ai/complete HTTP/1.1" 200 OK
18:58:21 app.api.v1.ai INFO   [AI续写] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), 上下文长度: 106, 风格: 默认
18:58:21 app.api.v1.ai INFO   [AI续写] context内容: '青州。 　　渊阳府，贤古县。 源顺镖局，后院偏房的一片空地内。 此处是镖局内，堆放柴炭的地方，平常少有人至，但此时，却有十多个单薄的身影，在空地上，稀稀落落地站着。 　　这些人都是十五六岁的少年，身体大多都还没长'
18:58:21 app.api.v1.ai INFO   [AI续写] prompt: '续写', max_tokens: 100
18:58:21 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
18:58:21 app.services.ai.http_ai_service INFO   ModelSelector 已启用
18:58:21 app.services.ai.http_ai_service INFO   CostTracker 已启用
18:58:23 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
INFO:     127.0.0.1:58569 - "POST /api/v1/ai/complete HTTP/1.1" 200 OK
18:58:23 app.services.ai.http_ai_service INFO   AI自动补全请求 - 上下文长度: 106
18:58:23 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=100, temp=0.7, task_type=None
18:58:25 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/2 200 OK"
18:58:25 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:58:26 app.services.ai.http_ai_service INFO   API 响应完成，共接收 4 个数据块，总长度: 32
18:58:26 app.services.ai.http_ai_service INFO   流式响应Token统计: 218 (prompt=192, completion=26)
18:58:26 app.services.agent.cost_tracker INFO   [CostTracker] 记录API调用: gemini-2.5-pro, tokens: 192+26=218, cost: $0.000009
18:58:26 app.services.ai.http_ai_service INFO   [CostTracker] API调用已记录: tokens=192+26, cost=$0.000009, time=2.80s
18:58:26 app.services.ai.ai_log_middleware INFO   AI调用日志已记录: operation=continue, tokens=80, cost=$0.000171, duration=2805ms, success=True
18:58:26 app.api.v1.ai INFO   [AI续写] 用户 testuser_new-1 请求完成，生成字数: 32
18:58:35 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
18:58:35 app.services.ai.http_ai_service INFO   ModelSelector 已启用
18:58:35 app.services.ai.http_ai_service INFO   CostTracker 已启用
18:58:37 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
INFO:     127.0.0.1:54082 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
18:58:37 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Message: 帮我总结一下前两章的主要内容，包括：1）主角设定 2）当前处境 3）主要冲突...
18:58:58 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 记忆上下文加载完成，耗时: 21.04s
18:58:58 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ Agent实例获取完成，耗时: 0.00s
18:58:58 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 初始化总耗时: 21.04s
18:58:58 app.services.agent.langgraph_agent INFO   [Planning] ⏱️ chat_with_planning方法开始
18:58:58 app.api.v1.ai INFO   [AI续写] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), 上下文长度: 106, 风格: 默认
18:58:58 app.api.v1.ai INFO   [AI续写] context内容: '青州。 　　渊阳府，贤古县。 源顺镖局，后院偏房的一片空地内。 此处是镖局内，堆放柴炭的地方，平常少有人至，但此时，却有十多个单薄的身影，在空地上，稀稀落落地站着。 　　这些人都是十五六岁的少年，身体大多都还没长'
18:58:58 app.api.v1.ai INFO   [AI续写] prompt: '续写', max_tokens: 100
18:58:58 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
18:58:58 app.services.ai.http_ai_service INFO   ModelSelector 已启用
18:58:58 app.services.ai.http_ai_service INFO   CostTracker 已启用
18:58:59 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
INFO:     127.0.0.1:55937 - "POST /api/v1/ai/complete HTTP/1.1" 200 OK
18:58:59 app.services.ai.http_ai_service INFO   AI自动补全请求 - 上下文长度: 106
18:58:59 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=100, temp=0.7, task_type=None
18:59:02 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/2 200 OK"
18:59:02 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:59:02 app.services.ai.http_ai_service INFO   API 响应完成，共接收 2 个数据块，总长度: 20
18:59:02 app.services.ai.http_ai_service INFO   流式响应Token统计: 224 (prompt=207, completion=17)
18:59:02 app.services.agent.cost_tracker INFO   [CostTracker] 记录API调用: gemini-2.5-pro, tokens: 207+17=224, cost: $0.000008
18:59:02 app.services.ai.http_ai_service INFO   [CostTracker] API调用已记录: tokens=207+17, cost=$0.000008, time=2.56s
18:59:02 app.services.ai.ai_log_middleware INFO   AI调用日志已记录: operation=continue, tokens=73, cost=$0.000136, duration=2556ms, success=True
18:59:02 app.api.v1.ai INFO   [AI续写] 用户 testuser_new-1 请求完成，生成字数: 20
18:59:20 app.services.agent.langgraph_agent INFO   [Planning] 从checkpointer加载了 2 条历史消息，耗时: 22.50s
18:59:20 app.services.agent.langgraph_agent INFO   [Planning] ⏱️ 规划前准备完成，总耗时: 22.50s
18:59:20 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: 帮我总结一下前两章的主要内容，包括：1）主角设定 2）当前处境 3）主要冲突...
18:59:20 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
18:59:20 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.03/$0.12 per 1M tokens)
18:59:20 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=1000, temp=0.3, task_type=TaskType.SIMPLE_QA
INFO:     127.0.0.1:56990 - "PUT /api/v1/chapters/627feba4-2097-4f28-a3f3-7641d10f7f40 HTTP/1.1" 200 OK
18:59:22 app.api.v1.ai INFO   [AI续写] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), 上下文长度: 126, 风格: 默认
18:59:22 app.api.v1.ai INFO   [AI续写] context内容: '青州。 　　渊阳府，贤古县。 源顺镖局，后院偏房的一片空地内。 此处是镖局内，堆放柴炭的地方，平常少有人至，但此时，却有十多个单薄的身影，在空地上，稀稀落落地站着。 　　这些人都是十五六岁的少年，身体大多都还没长开，面黄肌瘦，一看便知是穷苦人家的孩子。'
18:59:22 app.api.v1.ai INFO   [AI续写] prompt: '续写', max_tokens: 100
18:59:22 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
18:59:22 app.services.ai.http_ai_service INFO   ModelSelector 已启用
18:59:22 app.services.ai.http_ai_service INFO   CostTracker 已启用
18:59:23 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
18:59:23 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/2 200 OK"
18:59:23 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
INFO:     127.0.0.1:56991 - "POST /api/v1/ai/complete HTTP/1.1" 200 OK
18:59:23 app.services.ai.http_ai_service INFO   AI自动补全请求 - 上下文长度: 126
18:59:23 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=100, temp=0.7, task_type=None
INFO:     127.0.0.1:56990 - "PUT /api/v1/chapters/627feba4-2097-4f28-a3f3-7641d10f7f40 HTTP/1.1" 200 OK
18:59:26 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/2 200 OK"
18:59:26 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:59:26 app.services.ai.http_ai_service INFO   API 响应完成，共接收 3 个数据块，总长度: 28
18:59:26 app.services.ai.http_ai_service INFO   流式响应Token统计: 230 (prompt=209, completion=21)
18:59:26 app.services.agent.cost_tracker INFO   [CostTracker] 记录API调用: gemini-2.5-pro, tokens: 209+21=230, cost: $0.000009
18:59:26 app.services.ai.http_ai_service INFO   [CostTracker] API调用已记录: tokens=209+21, cost=$0.000009, time=3.03s
18:59:26 app.services.ai.ai_log_middleware INFO   AI调用日志已记录: operation=continue, tokens=91, cost=$0.000178, duration=3026ms, success=True
18:59:26 app.api.v1.ai INFO   [AI续写] 用户 testuser_new-1 请求完成，生成字数: 28
18:59:27 app.services.ai.http_ai_service INFO   API 响应完成，共接收 7 个数据块，总长度: 748
18:59:27 app.services.ai.http_ai_service INFO   流式响应Token统计: 2970 (prompt=2683, completion=287)
18:59:27 app.services.agent.cost_tracker INFO   [CostTracker] 记录API调用: gemini-2.5-pro, tokens: 2683+287=2970, cost: $0.000115
18:59:27 app.services.ai.http_ai_service INFO   [CostTracker] API调用已记录: tokens=2683+287, cost=$0.000115, time=6.98s
18:59:27 app.services.agent.langgraph_agent INFO   [JSON解析] 方法2成功: 从```json块提取
18:59:27 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共3个任务，耗时: 6.98s
18:59:27 app.services.agent.langgraph_agent INFO   [Planning] ⏱️ 从方法开始到规划完成总耗时: 29.48s
18:59:27 app.api.v1.agent INFO   [Stream] 规划生成: 3 个任务
18:59:27 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
18:59:27 app.services.agent.langgraph_agent INFO   [ParallelExecution] 任务分组: 并行=2, 串行=1
18:59:27 app.services.agent.langgraph_agent INFO   [ParallelExecution] 开始并行执行2个任务
18:59:27 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务1开始: 获取作品第一章的内容
18:59:27 app.api.v1.agent INFO   [Stream] 任务开始: 获取作品第一章的内容
18:59:27 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务2开始: 获取作品第二章的内容
18:59:27 app.api.v1.agent INFO   [Stream] 任务开始: 获取作品第二章的内容
18:59:27 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] 找到第2章: 第2章 浑圆桩
18:59:27 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务2完成
18:59:27 app.api.v1.agent INFO   [Stream] 任务完成: 获取作品第二章的内容 (0.0s)
18:59:27 sqlalchemy.pool.impl.AsyncAdaptedQueuePool ERROR   The garbage collector is trying to clean up non-checked-in connection <AdaptedConnection <asyncpg.connection.Connection object at 0x000001E2575B4C80>>, which will be terminated.  Please ensure that SQLAlchemy pooled connections are returned to the pool explicitly, either by calling ``close()`` or by using appropriate context managers to manage their lifecycle.
sys:1: SAWarning: The garbage collector is trying to clean up non-checked-in connection <AdaptedConnection <asyncpg.connection.Connection object at 0x000001E2575B4C80>>, which will be terminated.  Please ensure that SQLAlchemy pooled connections are returned to the pool explicitly, either by calling ``close()`` or by using appropriate context managers to manage their lifecycle.
18:59:27 sqlalchemy.pool.impl.AsyncAdaptedQueuePool ERROR   The garbage collector is trying to clean up non-checked-in connection <AdaptedConnection <asyncpg.connection.Connection object at 0x000001E2575B4B90>>, which will be terminated.  Please ensure that SQLAlchemy pooled connections are returned to the pool explicitly, either by calling ``close()`` or by using appropriate context managers to manage their lifecycle.
sys:1: SAWarning: The garbage collector is trying to clean up non-checked-in connection <AdaptedConnection <asyncpg.connection.Connection object at 0x000001E2575B4B90>>, which will be terminated.  Please ensure that SQLAlchemy pooled connections are returned to the pool explicitly, either by calling ``close()`` or by using appropriate context managers to manage their lifecycle.
18:59:27 sqlalchemy.pool.impl.AsyncAdaptedQueuePool ERROR   The garbage collector is trying to clean up non-checked-in connection <AdaptedConnection <asyncpg.connection.Connection object at 0x000001E257294230>>, which will be terminated.  Please ensure that SQLAlchemy pooled connections are returned to the pool explicitly, either by calling ``close()`` or by using appropriate context managers to manage their lifecycle.
sys:1: SAWarning: The garbage collector is trying to clean up non-checked-in connection <AdaptedConnection <asyncpg.connection.Connection object at 0x000001E257294230>>, which will be terminated.  Please ensure that SQLAlchemy pooled connections are returned to the pool explicitly, either by calling ``close()`` or by using appropriate context managers to manage their lifecycle.
18:59:27 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] 找到第1章: 第1章 吞噬
18:59:27 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务1完成
18:59:27 app.api.v1.agent INFO   [Stream] 任务完成: 获取作品第一章的内容 (0.0s)
18:59:27 app.services.agent.langgraph_agent INFO   [ParallelExecution] 开始串行执行1个任务
18:59:27 app.services.agent.langgraph_agent INFO   [ParallelExecution] 串行任务3开始: 分析合并后的前两章内容，提取主角设定、当前处境和主要冲突
18:59:27 app.api.v1.agent INFO   [Stream] 任务开始: 分析合并后的前两章内容，提取主角设定、当前处境和主要冲突
18:59:27 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
18:59:27 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.075/$0.3 per 1M tokens)
18:59:27 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
18:59:29 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/2 200 OK"
18:59:29 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:59:34 app.api.v1.ai INFO   [AI续写] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), 上下文长度: 126, 风格: 默认
18:59:34 app.api.v1.ai INFO   [AI续写] context内容: '青州。 　　渊阳府，贤古县。 源顺镖局，后院偏房的一片空地内。 此处是镖局内，堆放柴炭的地方，平常少有人至，但此时，却有十多个单薄的身影，在空地上，稀稀落落地站着。 　　这些人都是十五六岁的少年，身体大多都还没长开，面黄肌瘦，一看便知是穷苦人家的孩子。'
18:59:34 app.api.v1.ai INFO   [AI续写] prompt: '续写', max_tokens: 100
18:59:34 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
18:59:34 app.services.ai.http_ai_service INFO   ModelSelector 已启用
18:59:34 app.services.ai.http_ai_service INFO   CostTracker 已启用
18:59:36 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
INFO:     127.0.0.1:60535 - "POST /api/v1/ai/complete HTTP/1.1" 200 OK
18:59:36 app.services.ai.http_ai_service INFO   AI自动补全请求 - 上下文长度: 126
18:59:36 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=100, temp=0.7, task_type=None
18:59:38 app.services.ai.http_ai_service INFO   API 响应完成，共接收 21 个数据块，总长度: 1858
18:59:38 app.services.ai.http_ai_service INFO   流式响应Token统计: 2032 (prompt=1035, completion=997)
18:59:38 app.services.agent.cost_tracker INFO   [CostTracker] 记录API调用: gemini-2.5-pro, tokens: 1035+997=2032, cost: $0.000151
18:59:38 app.services.ai.http_ai_service INFO   [CostTracker] API调用已记录: tokens=1035+997, cost=$0.000151, time=11.06s
18:59:38 app.services.agent.langgraph_agent INFO   [ParallelExecution] 串行任务3完成
18:59:38 app.api.v1.agent INFO   [Stream] 任务完成: 分析合并后的前两章内容，提取主角设定、当前处境和主要冲突 (0.0s)
18:59:38 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共3个任务
18:59:38 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
18:59:38 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=2, 输出型=1
18:59:38 app.services.agent.langgraph_agent INFO   [Response] 单个分析任务(analyze_text_tool)，使用AI格式化
18:59:38 app.services.agent.langgraph_agent INFO   [Summarization] 使用AI整合任务结果
18:59:38 app.services.agent.langgraph_agent INFO   [Summarization] 上下文压缩: 原始=8286字符, 压缩后=6014字符, 压缩率=28%
18:59:38 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
18:59:38 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.075/$0.3 per 1M tokens)
18:59:38 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
18:59:38 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/2 200 OK"
18:59:38 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:59:39 app.services.ai.http_ai_service INFO   API 响应完成，共接收 3 个数据块，总长度: 24
18:59:39 app.services.ai.http_ai_service INFO   流式响应Token统计: 245 (prompt=224, completion=21)
18:59:39 app.services.agent.cost_tracker INFO   [CostTracker] 记录API调用: gemini-2.5-pro, tokens: 224+21=245, cost: $0.000009
18:59:39 app.services.ai.http_ai_service INFO   [CostTracker] API调用已记录: tokens=224+21, cost=$0.000009, time=3.07s
18:59:39 app.services.ai.ai_log_middleware INFO   AI调用日志已记录: operation=continue, tokens=89, cost=$0.000168, duration=3072ms, success=True
18:59:39 app.api.v1.ai INFO   [AI续写] 用户 testuser_new-1 请求完成，生成字数: 24
18:59:41 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/2 200 OK"
18:59:41 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:59:56 app.services.ai.http_ai_service INFO   API 响应完成，共接收 13 个数据块，总长度: 1191
18:59:56 app.services.ai.http_ai_service INFO   流式响应Token统计: 6433 (prompt=5634, completion=799)
18:59:56 app.services.agent.cost_tracker INFO   [CostTracker] 记录API调用: gemini-2.5-pro, tokens: 5634+799=6433, cost: $0.000265
18:59:56 app.services.ai.http_ai_service INFO   [CostTracker] API调用已记录: tokens=5634+799, cost=$0.000265, time=17.45s
18:59:56 app.services.agent.langgraph_agent INFO   [Planning] 已保存 2 条新消息到checkpointer (总计: 4)
18:59:56 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Stream completed
INFO:     127.0.0.1:60952 - "OPTIONS /api/v1/agent/chat/stream HTTP/1.1" 200 OK
19:00:17 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
19:00:17 app.services.ai.http_ai_service INFO   ModelSelector 已启用
19:00:17 app.services.ai.http_ai_service INFO   CostTracker 已启用
19:00:19 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
INFO:     127.0.0.1:60952 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
19:00:19 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Message: 上次问了你什么？...
19:00:40 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 记忆上下文加载完成，耗时: 21.06s
19:00:40 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ Agent实例获取完成，耗时: 0.00s
19:00:40 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 初始化总耗时: 21.06s
19:00:40 app.services.agent.langgraph_agent INFO   [Planning] ⏱️ chat_with_planning方法开始
19:00:40 app.services.agent.langgraph_agent INFO   [Planning] 从checkpointer加载了 4 条历史消息，耗时: 0.00s
19:00:40 app.services.agent.langgraph_agent INFO   [Planning] ⏱️ 规划前准备完成，总耗时: 0.00s
19:00:40 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: 上次问了你什么？...
19:00:40 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
19:00:40 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.03/$0.12 per 1M tokens)
19:00:40 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=1000, temp=0.3, task_type=TaskType.SIMPLE_QA
19:00:42 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/2 200 OK"
19:00:42 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
19:00:42 sqlalchemy.pool.impl.AsyncAdaptedQueuePool ERROR   The garbage collector is trying to clean up non-checked-in connection <AdaptedConnection <asyncpg.connection.Connection object at 0x000001E2572E8E60>>, which will be terminated.  Please ensure that SQLAlchemy pooled connections are returned to the pool explicitly, either by calling ``close()`` or by using appropriate context managers to manage their lifecycle.
C:\Program Files\Python312\Lib\selectors.py:298: SAWarning: The garbage collector is trying to clean up non-checked-in connection <AdaptedConnection <asyncpg.connection.Connection object at 0x000001E2572E8E60>>, which will be terminated.  Please ensure that SQLAlchemy pooled connections are returned to the pool explicitly, either by calling ``close()`` or by using appropriate context managers to manage their lifecycle.
  def register(self, fileobj, events, data=None):
19:00:51 app.services.ai.http_ai_service INFO   API 响应完成，共接收 24 个数据块，总长度: 2446
19:00:51 app.services.ai.http_ai_service INFO   流式响应Token统计: 6310 (prompt=4812, completion=1498)
19:00:51 app.services.agent.cost_tracker INFO   [CostTracker] 记录API调用: gemini-2.5-pro, tokens: 4812+1498=6310, cost: $0.000324
19:00:51 app.services.ai.http_ai_service INFO   [CostTracker] API调用已记录: tokens=4812+1498, cost=$0.000324, time=11.24s
19:00:51 app.services.agent.langgraph_agent INFO   [JSON解析] 方法2成功: 从```json块提取
19:00:51 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共1个任务，耗时: 11.25s
19:00:51 app.services.agent.langgraph_agent INFO   [Planning] ⏱️ 从方法开始到规划完成总耗时: 11.25s
19:00:51 app.api.v1.agent INFO   [Stream] 规划生成: 1 个任务
19:00:51 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
19:00:51 app.services.agent.langgraph_agent INFO   [ParallelExecution] 任务分组: 并行=0, 串行=1
19:00:51 app.services.agent.langgraph_agent INFO   [ParallelExecution] 开始串行执行1个任务
19:00:51 app.services.agent.langgraph_agent INFO   [ParallelExecution] 串行任务1开始: Analyze the provided conversation history to identify the last user query.
19:00:51 app.api.v1.agent INFO   [Stream] 任务开始: Analyze the provided conversation history to identify the last user query.
19:00:51 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
19:00:51 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.075/$0.3 per 1M tokens)
19:00:51 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
19:00:53 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/2 200 OK"
19:00:53 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
19:01:07 app.services.ai.http_ai_service INFO   API 响应完成，共接收 27 个数据块，总长度: 2287
19:01:07 app.services.ai.http_ai_service INFO   流式响应Token统计: 4110 (prompt=2809, completion=1301)
19:01:07 app.services.agent.cost_tracker INFO   [CostTracker] 记录API调用: gemini-2.5-pro, tokens: 2809+1301=4110, cost: $0.000240
19:01:07 app.services.ai.http_ai_service INFO   [CostTracker] API调用已记录: tokens=2809+1301, cost=$0.000240, time=16.36s
19:01:07 app.services.agent.langgraph_agent INFO   [ParallelExecution] 串行任务1完成
19:01:07 app.api.v1.agent INFO   [Stream] 任务完成: Analyze the provided conversation history to identify the last user query. (0.0s)
19:01:07 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共1个任务
19:01:07 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
19:01:07 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=0, 输出型=1
19:01:07 app.services.agent.langgraph_agent INFO   [Response] 单个分析任务(analyze_text_tool)，使用AI格式化
19:01:07 app.services.agent.langgraph_agent INFO   [Summarization] 使用AI整合任务结果
19:01:07 app.services.agent.langgraph_agent INFO   [Summarization] 上下文压缩: 原始=2311字符, 压缩后=234字符, 压缩率=90%
19:01:07 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
19:01:07 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.075/$0.3 per 1M tokens)
19:01:07 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
19:01:10 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/2 200 OK"
19:01:10 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
19:01:11 app.services.ai.http_ai_service INFO   API 响应完成，共接收 2 个数据块，总长度: 105
19:01:11 app.services.ai.http_ai_service INFO   流式响应Token统计: 455 (prompt=387, completion=68)
19:01:11 app.services.agent.cost_tracker INFO   [CostTracker] 记录API调用: gemini-2.5-pro, tokens: 387+68=455, cost: $0.000020
19:01:11 app.services.ai.http_ai_service INFO   [CostTracker] API调用已记录: tokens=387+68, cost=$0.000020, time=3.61s
19:01:11 app.services.agent.langgraph_agent INFO   [Planning] 已保存 2 条新消息到checkpointer (总计: 6)
19:01:11 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Stream completed
