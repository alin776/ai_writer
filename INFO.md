17:09:31 app.services.chapter_service INFO     - Chapter: 第34章 书生的疑惑, order=34
17:09:31 app.api.v1.chapters INFO   [GET chapters] Returning 34 chapters
INFO:     127.0.0.1:65023 - "GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/ai-guidelines HTTP/1.1" 200 OK
17:09:31 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/locations
17:09:31 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/chapters/work/c9dd9cbf-fa57-447e-9605-3020bbde5350
INFO:     127.0.0.1:65024 - "GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/locations HTTP/1.1" 200 OK
17:09:31 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/settings
INFO:     127.0.0.1:65026 - "GET /api/v1/chapters/work/c9dd9cbf-fa57-447e-9605-3020bbde5350 HTTP/1.1" 200 OK
INFO:     127.0.0.1:65025 - "GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/settings HTTP/1.1" 200 OK
17:09:31 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/guidelines
INFO:     127.0.0.1:65028 - "GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/guidelines HTTP/1.1" 200 OK
17:09:31 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/analysis/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/status
INFO:     127.0.0.1:65023 - "GET /api/v1/analysis/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/status HTTP/1.1" 200 OK
17:09:31 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/ai-guidelines
INFO:     127.0.0.1:65027 - "GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/ai-guidelines HTTP/1.1" 200 OK
17:09:31 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/627feba4-2097-4f28-a3f3-7641d10f7f40
17:09:31 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/627feba4-2097-4f28-a3f3-7641d10f7f40
INFO:     127.0.0.1:65026 - "PUT /api/v1/chapters/627feba4-2097-4f28-a3f3-7641d10f7f40 HTTP/1.1" 200 OK
INFO:     127.0.0.1:65024 - "PUT /api/v1/chapters/627feba4-2097-4f28-a3f3-7641d10f7f40 HTTP/1.1" 200 OK
17:09:31 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/analysis/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/status
INFO:     127.0.0.1:65023 - "GET /api/v1/analysis/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/status HTTP/1.1" 200 OK
17:09:37 app.api.middleware.monitoring_middleware INFO   API请求完成: OPTIONS /api/v1/agent/chat/stream
INFO:     127.0.0.1:60197 - "OPTIONS /api/v1/agent/chat/stream HTTP/1.1" 200 OK
17:09:37 app.services.ai.prompts INFO   Prompts loaded successfully from D:\Java\ai_writer\backend\app\services\ai\prompts\default.json
17:09:37 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
17:09:37 app.services.ai.http_ai_service INFO   ModelSelector 已启用
17:09:37 app.services.agent.cost_tracker INFO   CostTracker 初始化完成, 持久化: False
17:09:37 app.services.ai.http_ai_service INFO   CostTracker 已启用
17:09:38 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
17:09:38 app.api.v1.agent INFO   [Chat Stream] Mode: planning
17:09:38 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: planning, Message: 段融的金手指能力是什么？具体有什么效果？...
17:09:38 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:60197 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
17:09:38 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
17:09:38 app.services.ai.http_ai_service INFO   ModelSelector 已启用
17:09:38 app.services.ai.http_ai_service INFO   CostTracker 已启用
17:09:40 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
17:09:40 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ ContextManager已初始化
成功加载模板: intent_classifier (版本 2.0.0)
成功加载模板: writing_agent (版本 2.0.0)
成功加载模板: planning_agent (版本 2.0.0)
成功加载模板: tool_agent (版本 2.0.0)
成功加载模板: query_agent (版本 2.0.0)
17:09:40 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ PromptManager已初始化
17:09:40 app.services.agent.langgraph_agent INFO   [LangGraph] 使用 ChatOpenAI 模式（原生工具调用）
17:09:41 app.api.callbacks.monitoring_callback INFO   [MonitoringCallback] 已初始化
17:09:41 app.services.agent.langgraph_agent INFO   [LangGraph] 已创建MonitoringCallbackHandler
17:10:02 app.services.agent.langgraph_agent INFO   [LangGraph] OK 使用 AsyncRedisSaver（redis://localhost:6379/0，TTL=7天）
17:10:02 app.api.v1.agent INFO   [Global Agent] 创建全局Agent实例，MemorySaver将在请求间共享
17:10:23 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: 段融的金手指能力是什么？具体有什么效果？...
17:10:46 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
17:10:46 app.api.callbacks.monitoring_callback INFO   [MonitoringCallback] LLM调用成功: run_id=12fc3c94-047e-4a08-8c26-7d91013b2b6c, model=gemini-2.5-pro, duration=22.24s, tokens=2661 (prompt=2345, completion=316)
17:10:46 app.services.agent.langgraph_agent INFO   [_generate_text] 使用ChatOpenAI生成文本，tokens=2661
17:10:46 app.services.agent.langgraph_agent INFO   [JSON解析] 方法2成功: 从```json块提取
17:10:46 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共3个任务，耗时: 22.26s
17:10:46 app.api.v1.agent INFO   [Stream] 规划生成: 3 个任务
17:10:46 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
17:10:46 app.services.agent.langgraph_agent INFO   [ParallelExecution] 任务分组: 并行=2, 串行=1
17:10:46 app.services.agent.langgraph_agent INFO   [ParallelExecution] 开始并行执行2个任务
17:10:46 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务1开始: 使用关键词检索关于“段融”金手指能力和效果的核心信息。
17:10:46 app.api.v1.agent INFO   [Stream] 任务开始: 使用关键词检索关于“段融”金手指能力和效果的核心信息。
17:10:46 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务2开始: 读取当前章节内容，以防金手指的相关信息在本章被首次提及或有关键补充说明。
17:10:46 app.api.v1.agent INFO   [Stream] 任务开始: 读取当前章节内容，以防金手指的相关信息在本章被首次提及或有关键补充说明。
17:10:46 app.services.vector_store_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, query=段融 金手指能力 效果...
Batches: 100%|█████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  4.79it/s]
17:10:46 app.services.agent.langgraph_agent INFO   [read_chapter_tool] 读取章节成功: 第1章 吞噬
17:10:46 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务2完成
17:10:46 app.api.v1.agent INFO   [Stream] 任务完成: 读取当前章节内容，以防金手指的相关信息在本章被首次提及或有关键补充说明。 (0.0s)
17:10:46 app.services.vector_store_service INFO   检索到 1 个相关结果（阈值=0.3）
17:10:46 app.services.agent.langgraph_agent INFO   [search_analysis_fragments_tool] RAG检索成功: 找到1个相关片段
17:10:46 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务1完成
17:10:46 app.api.v1.agent INFO   [Stream] 任务完成: 使用关键词检索关于“段融”金手指能力和效果的核心信息。 (0.0s)
17:10:46 app.services.agent.langgraph_agent INFO   [ParallelExecution] 开始串行执行1个任务
17:10:46 app.services.agent.langgraph_agent INFO   [ParallelExecution] 串行任务3开始: 综合步骤1和2获取的信息，整理并生成关于段融金手指能力和具体效果的详细回答。
17:10:46 app.api.v1.agent INFO   [Stream] 任务开始: 综合步骤1和2获取的信息，整理并生成关于段融金手指能力和具体效果的详细回答。
17:10:46 app.services.agent.langgraph_agent INFO   [ParallelExecution] 串行任务3完成
17:10:46 app.api.v1.agent INFO   [Stream] 任务完成: 综合步骤1和2获取的信息，整理并生成关于段融金手指能力和具体效果的详细回答。 (0.0s)
17:10:46 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共3个任务
17:10:46 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
17:10:46 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=2, 输出型=1
17:10:46 app.services.agent.langgraph_agent INFO   [Response] 单个分析任务(None)，使用AI格式化
17:10:46 app.services.agent.langgraph_agent INFO   [Summarization] 使用AI整合任务结果
17:10:46 app.services.agent.langgraph_agent INFO   [Summarization] 上下文压缩: 原始=5155字符, 压缩后=3905字符, 压缩率=25%
17:10:46 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
17:10:46 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.075/$0.3 per 1M tokens)
17:10:46 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
17:10:49 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/2 200 OK"
17:10:49 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
17:10:56 app.services.ai.http_ai_service INFO   API 响应完成，共接收 5 个数据块，总长度: 438
17:10:56 app.services.ai.http_ai_service INFO   流式响应Token统计: 3961 (prompt=3652, completion=309)
17:10:56 app.services.agent.cost_tracker INFO   [CostTracker] 记录API调用: gemini-2.5-pro, tokens: 3652+309=3961, cost: $0.000147
17:10:56 app.services.ai.http_ai_service INFO   [CostTracker] API调用已记录: tokens=3652+309, cost=$0.000147, time=9.80s
17:10:56 app.services.agent.langgraph_agent INFO   [Planning] 已保存 2 条新消息到checkpointer (总计: 2)
17:10:56 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed
