已注册策略: web_novel_11d - 网文11维度分析
INFO:     Started server process [36408]
INFO:     Waiting for application startup.
2025-11-01 21:49:32,479 - app.main - INFO - [STARTUP] 应用启动中...
2025-11-01 21:49:32,487 - app.core.database - INFO - 正在初始化数据库... (尝试 1/3)
2025-11-01 21:49:32,581 - app.core.database - INFO - ✅ 数据库初始化成功
2025-11-01 21:49:32,581 - apscheduler.scheduler - INFO - Adding job tentatively -- it will be properly scheduled when the scheduler starts
2025-11-01 21:49:32,583 - apscheduler.scheduler - INFO - Added job "清理过期的去痕迹会话详情" to job store "default"
2025-11-01 21:49:32,584 - apscheduler.scheduler - INFO - Scheduler started
2025-11-01 21:49:32,584 - app.tasks.cleanup_humanize_details - INFO - 定时任务调度器已启动
2025-11-01 21:49:32,585 - app.main - INFO - [STARTUP] 开始预加载Embedding模型...
2025-11-01 21:49:32,585 - app.services.vector_store_service - INFO - 🔄 预加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
2025-11-01 21:49:32,585 - sentence_transformers.SentenceTransformer - INFO - Use pytorch device_name: cpu
2025-11-01 21:49:32,586 - sentence_transformers.SentenceTransformer - INFO - Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
2025-11-01 21:49:40,293 - app.services.vector_store_service - INFO - ✅ Embedding模型预加载成功，耗时: 7.71秒
2025-11-01 21:49:40,293 - app.main - INFO - [STARTUP] Embedding模型预加载完成
2025-11-01 21:49:40,293 - app.main - INFO - [STARTUP] 应用启动完成
INFO:     Application startup complete.
INFO:     127.0.0.1:57424 - "OPTIONS /api/v1/worldview/works/527ad0eb-67de-428d-ae61-45cfac74933a/characters HTTP/1.1" 200 OK
INFO:     127.0.0.1:59364 - "OPTIONS /api/v1/worldview/works/527ad0eb-67de-428d-ae61-45cfac74933a/locations HTTP/1.1" 200 OK
INFO:     127.0.0.1:57556 - "OPTIONS /api/v1/worldview/works/527ad0eb-67de-428d-ae61-45cfac74933a/settings HTTP/1.1" 200 OK
INFO:     127.0.0.1:63672 - "OPTIONS /api/v1/works/527ad0eb-67de-428d-ae61-45cfac74933a HTTP/1.1" 200 OK
INFO:     127.0.0.1:65293 - "OPTIONS /api/v1/chapters/work/527ad0eb-67de-428d-ae61-45cfac74933a HTTP/1.1" 200 OK
INFO:     127.0.0.1:57424 - "OPTIONS /api/v1/worldview/works/527ad0eb-67de-428d-ae61-45cfac74933a/ai-guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:59364 - "OPTIONS /api/v1/works/527ad0eb-67de-428d-ae61-45cfac74933a HTTP/1.1" 200 OK
INFO:     127.0.0.1:57556 - "OPTIONS /api/v1/chapters/work/527ad0eb-67de-428d-ae61-45cfac74933a HTTP/1.1" 200 OK
INFO:     127.0.0.1:63672 - "OPTIONS /api/v1/worldview/works/527ad0eb-67de-428d-ae61-45cfac74933a/characters HTTP/1.1" 200 OK
INFO:     127.0.0.1:59543 - "OPTIONS /api/v1/worldview/works/527ad0eb-67de-428d-ae61-45cfac74933a/guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:65293 - "OPTIONS /api/v1/worldview/works/527ad0eb-67de-428d-ae61-45cfac74933a/locations HTTP/1.1" 200 OK
INFO:     127.0.0.1:57556 - "OPTIONS /api/v1/worldview/works/527ad0eb-67de-428d-ae61-45cfac74933a/ai-guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:59364 - "OPTIONS /api/v1/worldview/works/527ad0eb-67de-428d-ae61-45cfac74933a/guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:57424 - "OPTIONS /api/v1/worldview/works/527ad0eb-67de-428d-ae61-45cfac74933a/settings HTTP/1.1" 200 OK
2025-11-01 21:49:55,662 - app.api.v1.chapters - INFO - [GET chapters] work_id=527ad0eb-67de-428d-ae61-45cfac74933a, user_id=602f5147-846a-4cde-95d3-405fa75f133f
INFO:     127.0.0.1:63672 - "GET /api/v1/worldview/works/527ad0eb-67de-428d-ae61-45cfac74933a/characters HTTP/1.1" 200 OK
2025-11-01 21:49:55,700 - app.services.chapter_service - INFO - [ChapterService] Querying chapters for work_id=527ad0eb-67de-428d-ae61-45cfac74933a, type=<class 'uuid.UUID'>
2025-11-01 21:49:55,714 - app.services.chapter_service - INFO - [ChapterService] Found 0 chapters
2025-11-01 21:49:55,714 - app.api.v1.chapters - INFO - [GET chapters] Returning 0 chapters
INFO:     127.0.0.1:57556 - "GET /api/v1/works/527ad0eb-67de-428d-ae61-45cfac74933a HTTP/1.1" 200 OK
INFO:     127.0.0.1:59364 - "GET /api/v1/chapters/work/527ad0eb-67de-428d-ae61-45cfac74933a HTTP/1.1" 200 OK
INFO:     127.0.0.1:57424 - "GET /api/v1/worldview/works/527ad0eb-67de-428d-ae61-45cfac74933a/ai-guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:63672 - "GET /api/v1/worldview/works/527ad0eb-67de-428d-ae61-45cfac74933a/guidelines HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:59543 - "GET /api/v1/worldview/works/527ad0eb-67de-428d-ae61-45cfac74933a/locations HTTP/1.1" 200 OK
INFO:     127.0.0.1:65293 - "GET /api/v1/worldview/works/527ad0eb-67de-428d-ae61-45cfac74933a/settings HTTP/1.1" 200 OK
2025-11-01 21:49:55,734 - app.api.v1.chapters - INFO - [GET chapters] work_id=527ad0eb-67de-428d-ae61-45cfac74933a, user_id=602f5147-846a-4cde-95d3-405fa75f133f
2025-11-01 21:49:55,744 - app.services.chapter_service - INFO - [ChapterService] Querying chapters for work_id=527ad0eb-67de-428d-ae61-45cfac74933a, type=<class 'uuid.UUID'>
INFO:     127.0.0.1:59364 - "GET /api/v1/works/527ad0eb-67de-428d-ae61-45cfac74933a HTTP/1.1" 200 OK
2025-11-01 21:49:55,750 - app.services.chapter_service - INFO - [ChapterService] Found 0 chapters
2025-11-01 21:49:55,750 - app.api.v1.chapters - INFO - [GET chapters] Returning 0 chapters
INFO:     127.0.0.1:57424 - "GET /api/v1/chapters/work/527ad0eb-67de-428d-ae61-45cfac74933a HTTP/1.1" 200 OK
INFO:     127.0.0.1:57556 - "GET /api/v1/worldview/works/527ad0eb-67de-428d-ae61-45cfac74933a/characters HTTP/1.1" 200 OK
INFO:     127.0.0.1:63672 - "GET /api/v1/worldview/works/527ad0eb-67de-428d-ae61-45cfac74933a/ai-guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:59543 - "GET /api/v1/worldview/works/527ad0eb-67de-428d-ae61-45cfac74933a/guidelines HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:65293 - "GET /api/v1/worldview/works/527ad0eb-67de-428d-ae61-45cfac74933a/locations HTTP/1.1" 200 OK
INFO:     127.0.0.1:59364 - "GET /api/v1/worldview/works/527ad0eb-67de-428d-ae61-45cfac74933a/settings HTTP/1.1" 200 OK
INFO:     127.0.0.1:55811 - "OPTIONS /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2025-11-01 21:50:06,794 - app.services.ai.prompts - INFO - Prompts loaded successfully from D:\Java\ai_writer\backend\app\services\ai\prompts\default.json
2025-11-01 21:50:06,794 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2025-11-01 21:50:06,794 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2025-11-01 21:50:06,794 - app.services.agent.cost_tracker - INFO - CostTracker 初始化完成, 持久化: False
2025-11-01 21:50:06,794 - app.services.ai.http_ai_service - INFO - CostTracker 已启用
2025-11-01 21:50:08,252 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, ModelSelector: True, CostTracking: True
INFO:     127.0.0.1:55811 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2025-11-01 21:50:08,267 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User: 602f5147-846a-4cde-95d3-405fa75f133f, Message: 你好...
2025-11-01 21:50:10,307 - app.services.agent.langgraph_agent - INFO - [LangGraph] 使用 ChatOpenAI 模式（原生工具调用）
2025-11-01 21:50:14,919 - app.services.agent.langgraph_agent - INFO - [Planning] 开始规划: 你好...
2025-11-01 21:50:14,925 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=1000, temp=0.3, task_type=None
2025-11-01 21:50:18,498 - httpx - INFO - HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
2025-11-01 21:50:18,500 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-11-01 21:50:37,316 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 6 个数据块，总长度: 302
2025-11-01 21:50:37,316 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 3057 (prompt=2931, completion=126)
2025-11-01 21:50:37,316 - app.services.agent.cost_tracker - INFO - [CostTracker] 记录API调用: gemini-2.5-pro, tokens: 2931+126=3057, cost: $0.000103
2025-11-01 21:50:37,316 - app.services.ai.http_ai_service - INFO - [CostTracker] API调用已记录: tokens=2931+126, cost=$0.000103, time=22.39s
2025-11-01 21:50:37,320 - app.services.agent.langgraph_agent - INFO - [JSON解析] 方法2成功: 从```json块提取
2025-11-01 21:50:37,321 - app.services.agent.langgraph_agent - INFO - [Planning] 规划生成成功，共1个任务
2025-11-01 21:50:37,321 - app.api.v1.agent - INFO - [Stream] 规划生成: 1 个任务
2025-11-01 21:50:37,321 - app.services.agent.langgraph_agent - INFO - [Execution] 开始任务1: 由于用户只是打招呼，没有提出具体写作要求，因此首先调用 get_context_tool 获取作品的整体背景信息（如简介、大纲、章节列表等），为理解用户后续可能提出的具体指令做准备。
2025-11-01 21:50:37,321 - app.api.v1.agent - INFO - [Stream] 任务开始: 由于用户只是打招呼，没有提出具体写作要求，因此首先调用 get_context_tool 获取作品的整体背景信息（如简介、大纲、章节列表等），为理解用户后续可能提出的具体指令做准备。
2025-11-01 21:50:37,321 - app.services.agent.langgraph_agent - ERROR - [Execution] 任务1失败: 1 validation error for get_context_tool
chapter_id
  Input should be a valid string [type=string_type, input_value=None, input_type=NoneType]
    For further information visit https://errors.pydantic.dev/2.12/v/string_type
2025-11-01 21:50:37,321 - app.services.agent.langgraph_agent - INFO - [Summarization] 生成最终响应
2025-11-01 21:50:37,321 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.7, task_type=None
2025-11-01 21:50:40,719 - httpx - INFO - HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
2025-11-01 21:50:40,720 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-11-01 21:51:01,537 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 8 个数据块，总长度: 798
2025-11-01 21:51:01,537 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 2365 (prompt=1916, completion=449)
2025-11-01 21:51:01,537 - app.services.agent.cost_tracker - INFO - [CostTracker] 记录API调用: gemini-2.5-pro, tokens: 1916+449=2365, cost: $0.000111
2025-11-01 21:51:01,539 - app.services.ai.http_ai_service - INFO - [CostTracker] API调用已记录: tokens=1916+449, cost=$0.000111, time=24.22s
2025-11-01 21:51:01,541 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Stream completed
