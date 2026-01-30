(venv) PS D:\Java\ai_writer\backend> python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
INFO:     Will watch for changes in these directories: ['D:\\Java\\ai_writer\\backend']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [27296] using WatchFiles
已注册策略: web_novel_11d - 网文11维度分析
2026-01-30 14:47:21,977 - app.main - INFO - [STARTUP] 监控中间件已注册: TraceMiddleware, MonitoringMiddleware
INFO:     Started server process [22244]
INFO:     Waiting for application startup.
2026-01-30 14:47:22,439 - app.main - INFO - [STARTUP] 应用启动中...
2026-01-30 14:47:22,440 - app.core.database - INFO - 正在初始化数据库... (尝试 1/3)
2026-01-30 14:47:22,586 - app.core.database - INFO - ✅ 数据库初始化成功
2026-01-30 14:47:22,586 - app.main - INFO - [STARTUP] 开始检查并初始化官方频道...
检查官方频道...
现有官方频道: {'公共酒馆', '读者茶馆', '官方实验室', '作者酒馆'}

✓ 所有官方频道都已存在，无需创建

现有官方频道列表:
  - 作者酒馆 (ID: c4a5fcd7-7fd1-4a18-8677-a15c052c7507)
  - 读者茶馆 (ID: 2e1b9d33-1400-4a40-802b-6d212d7a2fe5)
  - 公共酒馆 (ID: 3749ebb4-a2d6-4ab8-aa14-cf6c26611fc0)
  - 官方实验室 (ID: 452cfe84-3ac4-49e1-986b-260bcc3b8a6a)
2026-01-30 14:47:22,602 - app.main - INFO - [STARTUP] ✅ 官方频道检查完成
2026-01-30 14:47:22,605 - app.tasks.cleanup_humanize_details - INFO - 定时任务调度器已启动
2026-01-30 14:47:22,605 - app.services.channel_scheduler - INFO - Channel scheduler initialized
2026-01-30 14:47:22,605 - app.services.channel_scheduler - INFO - Channel scheduler started
2026-01-30 14:47:22,606 - app.main - INFO - [STARTUP] 开始预初始化同步Redis连接...
2026-01-30 14:47:22,606 - app.api.v1.agent - INFO - [Redis] 全局连接池已创建
2026-01-30 14:47:22,619 - app.main - INFO - [STARTUP] ✅ 同步Redis连接池预初始化完成
2026-01-30 14:47:22,619 - app.main - INFO - [STARTUP] 开始初始化AsyncRedisSaver索引...
2026-01-30 14:47:22,631 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ setup_checkpointer Redis连接验证成功
2026-01-30 14:47:22,643 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ AsyncRedisSaver索引预创建成功
2026-01-30 14:47:22,643 - app.main - INFO - [STARTUP] AsyncRedisSaver索引初始化完成
2026-01-30 14:47:22,643 - app.main - INFO - [STARTUP] 开始预加载Embedding模型...
2026-01-30 14:47:22,643 - app.services.vector_store_service - INFO - 🔄 预加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
2026-01-30 14:47:29,107 - app.services.vector_store_service - INFO - ✅ Embedding模型预加载成功，耗时: 6.46秒
2026-01-30 14:47:29,109 - app.main - INFO - [STARTUP] Embedding模型预加载完成
2026-01-30 14:47:29,109 - app.main - INFO - [STARTUP] P0性能优化已暂时禁用（诊断模式）
2026-01-30 14:47:29,111 - app.main - INFO - [STARTUP] 应用启动完成
INFO:     Application startup complete.
INFO:     ('127.0.0.1', 57975) - "WebSocket /api/v1/ws/notifications/79913e7e-d5cd-4e09-bce6-ca6639bd8456" [accepted]
2026-01-30 14:47:32,031 - app.api.v1.ws - INFO - [WebSocket] 通知连接建立: user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
INFO:     connection open
2026-01-30 14:49:26,722 - monitoring - INFO - Registered health check: cpu_usage
2026-01-30 14:49:26,724 - monitoring - INFO - Registered health check: memory_usage
2026-01-30 14:49:26,724 - monitoring - INFO - Registered health check: disk_usage
2026-01-30 14:49:26,725 - monitoring - INFO - Registered health check: process_status
2026-01-30 14:49:26,725 - monitoring - INFO - Added alert rule: high_cpu_usage
2026-01-30 14:49:26,726 - monitoring - INFO - Added alert rule: high_memory_usage
2026-01-30 14:49:26,726 - monitoring - INFO - Added alert rule: low_disk_space
2026-01-30 14:49:27,144 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 b0994445-fba2-42c5-8fd2-a2216828183b 内容更新，新段落数: 88
INFO:     127.0.0.1:63591 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
INFO:     127.0.0.1:63590 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
2026-01-30 14:49:27,244 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:7692a7f2-19ce-49e3-977f-aad9c77bc4d1
2026-01-30 14:49:27,249 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/b0994445-fba2-42c5-8fd2-a2216828183b
INFO:     127.0.0.1:63585 - "PUT /api/v1/chapters/b0994445-fba2-42c5-8fd2-a2216828183b HTTP/1.1" 200 OK
2026-01-30 14:49:29,868 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:62663 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
2026-01-30 14:49:29,886 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works
INFO:     127.0.0.1:63434 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
2026-01-30 14:49:33,557 - app.api.v1.import_routes - INFO - 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456 预览导入文件: 一夕千悟，从杂役弟子开始.txt, 格式: txt
2026-01-30 14:49:33,566 - app.api.v1.import_routes - INFO - 预览成功: 作品=一夕千悟，从杂役弟子开始, 章节数=5
INFO:     127.0.0.1:54116 - "POST /api/v1/works/import/preview HTTP/1.1" 200 OK
2026-01-30 14:49:35,143 - app.api.v1.import_routes - INFO - 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456 导入文件: 一夕千悟，从杂役弟子开始.txt, 格式: txt
2026-01-30 14:49:35,145 - app.api.v1.import_routes - INFO - [导入参数] auto_extract_worldview=True, format=txt, background_tasks=True
2026-01-30 14:49:35,147 - app.services.import_service - INFO - 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456 开始导入文本数据
2026-01-30 14:49:35,292 - app.services.import_service - INFO - 文本导入完成: 作品ID=57b6b0cc-2832-412c-ad2c-1ec0d8ff637d, 章节=5
2026-01-30 14:49:35,292 - app.api.v1.import_routes - INFO - [世界观提取] 已为作品 57b6b0cc-2832-412c-ad2c-1ec0d8ff637d 排队世界观提取任务
2026-01-30 14:49:35,297 - app.api.v1.import_routes - INFO - 导入成功: 作品ID=57b6b0cc-2832-412c-ad2c-1ec0d8ff637d, 章节=5, 人物=0
INFO:     127.0.0.1:60480 - "POST /api/v1/works/import HTTP/1.1" 200 OK
2026-01-30 14:49:37,381 - app.api.v1.chapters - INFO - [GET chapters] work_id=57b6b0cc-2832-412c-ad2c-1ec0d8ff637d, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 14:49:37,406 - app.api.v1.chapters - INFO - ⚠️ [GET chapters] 缓存未命中: chapters:work:57b6b0cc-2832-412c-ad2c-1ec0d8ff637d
2026-01-30 14:49:37,406 - app.services.chapter_service - INFO - [ChapterService] Querying chapters for work_id=57b6b0cc-2832-412c-ad2c-1ec0d8ff637d, type=<class 'uuid.UUID'>
2026-01-30 14:49:37,412 - app.services.chapter_service - INFO - [ChapterService] Found 5 chapters
2026-01-30 14:49:37,413 - app.services.chapter_service - INFO -   - Chapter: 第1章 吞噬, order=1
2026-01-30 14:49:37,415 - app.services.chapter_service - INFO -   - ... (3 more chapters)
2026-01-30 14:49:37,415 - app.services.chapter_service - INFO -   - Chapter: 第5章 太一门, order=5
2026-01-30 14:49:37,458 - app.api.v1.chapters - INFO - [GET chapters] Returning 5 chapters
2026-01-30 14:49:37,468 - app.api.v1.chapters - INFO - 💾 [GET chapters] 缓存已保存: chapters:work:57b6b0cc-2832-412c-ad2c-1ec0d8ff637d (expire=60s)
INFO:     127.0.0.1:50292 - "GET /api/v1/chapters/work/57b6b0cc-2832-412c-ad2c-1ec0d8ff637d HTTP/1.1" 200 OK
INFO:     127.0.0.1:50291 - "GET /api/v1/works/57b6b0cc-2832-412c-ad2c-1ec0d8ff637d HTTP/1.1" 200 OK
2026-01-30 14:49:39,567 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/57b6b0cc-2832-412c-ad2c-1ec0d8ff637d/characters
INFO:     127.0.0.1:50293 - "GET /api/v1/worldview/works/57b6b0cc-2832-412c-ad2c-1ec0d8ff637d/characters HTTP/1.1" 200 OK
2026-01-30 14:49:39,586 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/57b6b0cc-2832-412c-ad2c-1ec0d8ff637d/guidelines
INFO:     127.0.0.1:50297 - "GET /api/v1/worldview/works/57b6b0cc-2832-412c-ad2c-1ec0d8ff637d/guidelines HTTP/1.1" 200 OK
2026-01-30 14:49:39,618 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/57b6b0cc-2832-412c-ad2c-1ec0d8ff637d/ai-guidelines
INFO:     127.0.0.1:50527 - "GET /api/v1/worldview/works/57b6b0cc-2832-412c-ad2c-1ec0d8ff637d/ai-guidelines HTTP/1.1" 200 OK
2026-01-30 14:49:41,773 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/57b6b0cc-2832-412c-ad2c-1ec0d8ff637d/locations
INFO:     127.0.0.1:50294 - "GET /api/v1/worldview/works/57b6b0cc-2832-412c-ad2c-1ec0d8ff637d/locations HTTP/1.1" 200 OK
2026-01-30 14:49:41,783 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/57b6b0cc-2832-412c-ad2c-1ec0d8ff637d/settings
INFO:     127.0.0.1:50296 - "GET /api/v1/worldview/works/57b6b0cc-2832-412c-ad2c-1ec0d8ff637d/settings HTTP/1.1" 200 OK
2026-01-30 14:49:43,911 - app.core.redis - INFO - ✅ Redis connected: redis://localhost:6379/0
INFO:     127.0.0.1:60047 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
INFO:     127.0.0.1:49342 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-30 14:49:46,777 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:57159 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
INFO:     127.0.0.1:62114 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2026-01-30 14:49:46,810 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
2026-01-30 14:49:46,814 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:62113 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
INFO:     127.0.0.1:62115 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2026-01-30 14:49:46,854 - app.api.v1.import_routes - INFO - [世界观提取] 开始为作品 57b6b0cc-2832-412c-ad2c-1ec0d8ff637d 提取世界观
2026-01-30 14:49:46,924 - app.api.middleware.monitoring_middleware - WARNING - API请求完成: GET /api/v1/analysis/works/57b6b0cc-2832-412c-ad2c-1ec0d8ff637d/status
2026-01-30 14:49:46,930 - app.services.ai.prompts - INFO - Prompts loaded successfully from D:\Java\ai_writer\backend\app\services\ai\prompts\default.json
2026-01-30 14:49:46,930 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-30 14:49:46,939 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-30 14:49:46,939 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2026-01-30 14:49:48,583 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz:8443/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-30 14:49:48,586 - app.services.worldview_sync_service - INFO - [世界观同步] AI服务初始化完成: api_key=***KFzr, base_url=https://204992.xyz:8443/v1, model=gemini-2.5-pro
INFO:     127.0.0.1:52109 - "GET /api/v1/analysis/works/57b6b0cc-2832-412c-ad2c-1ec0d8ff637d/status HTTP/1.1" 404 Not Found
2026-01-30 14:49:48,586 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/57b6b0cc-2832-412c-ad2c-1ec0d8ff637d/characters
2026-01-30 14:49:48,589 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/57b6b0cc-2832-412c-ad2c-1ec0d8ff637d/locations
INFO:     127.0.0.1:56611 - "GET /api/v1/worldview/works/57b6b0cc-2832-412c-ad2c-1ec0d8ff637d/characters HTTP/1.1" 200 OK
INFO:     127.0.0.1:56612 - "GET /api/v1/worldview/works/57b6b0cc-2832-412c-ad2c-1ec0d8ff637d/locations HTTP/1.1" 200 OK
2026-01-30 14:49:48,597 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/5c482e16-09c7-4575-888c-3f818971e36f/revisions
INFO:     127.0.0.1:50064 - "GET /api/v1/chapters/5c482e16-09c7-4575-888c-3f818971e36f/revisions?status=pending HTTP/1.1" 200 OK
2026-01-30 14:49:48,616 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 未传递task_type，使用默认模型: gemini-2.5-pro
2026-01-30 14:49:48,626 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=3000, temp=0.3, task_type=None
INFO:     127.0.0.1:61358 - "GET /api/v1/worldview/works/57b6b0cc-2832-412c-ad2c-1ec0d8ff637d/guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:49888 - "GET /api/v1/worldview/works/57b6b0cc-2832-412c-ad2c-1ec0d8ff637d/ai-guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:56705 - "GET /api/v1/worldview/works/57b6b0cc-2832-412c-ad2c-1ec0d8ff637d/settings HTTP/1.1" 200 OK
2026-01-30 14:49:48,760 - app.api.middleware.monitoring_middleware - WARNING - API请求完成: GET /api/v1/analysis/works/57b6b0cc-2832-412c-ad2c-1ec0d8ff637d/status
INFO:     127.0.0.1:54920 - "GET /api/v1/analysis/works/57b6b0cc-2832-412c-ad2c-1ec0d8ff637d/status HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:52951 - "GET /api/v1/chapters/5c482e16-09c7-4575-888c-3f818971e36f/revisions?status=pending HTTP/1.1" 200 OK
2026-01-30 14:49:48,858 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:57b6b0cc-2832-412c-ad2c-1ec0d8ff637d
2026-01-30 14:49:51,012 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/5c482e16-09c7-4575-888c-3f818971e36f
INFO:     127.0.0.1:64355 - "PUT /api/v1/chapters/5c482e16-09c7-4575-888c-3f818971e36f HTTP/1.1" 200 OK
2026-01-30 14:49:53,414 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 5c482e16-09c7-4575-888c-3f818971e36f 内容更新，新段落数: 88
2026-01-30 14:49:53,430 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:57b6b0cc-2832-412c-ad2c-1ec0d8ff637d
2026-01-30 14:49:53,430 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 5c482e16-09c7-4575-888c-3f818971e36f 内容更新，新段落数: 88
2026-01-30 14:49:53,430 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/5c482e16-09c7-4575-888c-3f818971e36f
2026-01-30 14:49:53,435 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 5c482e16-09c7-4575-888c-3f818971e36f 内容更新，新段落数: 88
INFO:     127.0.0.1:63894 - "PUT /api/v1/chapters/5c482e16-09c7-4575-888c-3f818971e36f HTTP/1.1" 200 OK
2026-01-30 14:49:57,896 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:57b6b0cc-2832-412c-ad2c-1ec0d8ff637d
2026-01-30 14:49:57,896 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/5c482e16-09c7-4575-888c-3f818971e36f
INFO:     127.0.0.1:63892 - "PUT /api/v1/chapters/5c482e16-09c7-4575-888c-3f818971e36f HTTP/1.1" 200 OK
2026-01-30 14:49:57,934 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:57b6b0cc-2832-412c-ad2c-1ec0d8ff637d
2026-01-30 14:49:57,944 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/5c482e16-09c7-4575-888c-3f818971e36f
INFO:     127.0.0.1:52872 - "GET /api/v1/worldview/works/57b6b0cc-2832-412c-ad2c-1ec0d8ff637d/guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:63893 - "PUT /api/v1/chapters/5c482e16-09c7-4575-888c-3f818971e36f HTTP/1.1" 200 OK
INFO:     127.0.0.1:52868 - "GET /api/v1/worldview/works/57b6b0cc-2832-412c-ad2c-1ec0d8ff637d/locations HTTP/1.1" 200 OK
INFO:     127.0.0.1:52867 - "GET /api/v1/worldview/works/57b6b0cc-2832-412c-ad2c-1ec0d8ff637d/characters HTTP/1.1" 200 OK
INFO:     127.0.0.1:53702 - "GET /api/v1/worldview/works/57b6b0cc-2832-412c-ad2c-1ec0d8ff637d/ai-guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:52871 - "GET /api/v1/worldview/works/57b6b0cc-2832-412c-ad2c-1ec0d8ff637d/settings HTTP/1.1" 200 OK
INFO:     127.0.0.1:64197 - "GET /api/v1/worldview/works/57b6b0cc-2832-412c-ad2c-1ec0d8ff637d/locations HTTP/1.1" 200 OK
INFO:     127.0.0.1:64196 - "GET /api/v1/worldview/works/57b6b0cc-2832-412c-ad2c-1ec0d8ff637d/characters HTTP/1.1" 200 OK
INFO:     127.0.0.1:64202 - "GET /api/v1/worldview/works/57b6b0cc-2832-412c-ad2c-1ec0d8ff637d/ai-guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:64201 - "GET /api/v1/worldview/works/57b6b0cc-2832-412c-ad2c-1ec0d8ff637d/guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:64199 - "GET /api/v1/worldview/works/57b6b0cc-2832-412c-ad2c-1ec0d8ff637d/settings HTTP/1.1" 200 OK
2026-01-30 14:50:28,049 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
INFO:     127.0.0.1:62349 - "GET /api/v1/worldview/works/57b6b0cc-2832-412c-ad2c-1ec0d8ff637d/guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:62346 - "GET /api/v1/worldview/works/57b6b0cc-2832-412c-ad2c-1ec0d8ff637d/characters HTTP/1.1" 200 OK
INFO:     127.0.0.1:62350 - "GET /api/v1/worldview/works/57b6b0cc-2832-412c-ad2c-1ec0d8ff637d/ai-guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:62348 - "GET /api/v1/worldview/works/57b6b0cc-2832-412c-ad2c-1ec0d8ff637d/settings HTTP/1.1" 200 OK
INFO:     127.0.0.1:62347 - "GET /api/v1/worldview/works/57b6b0cc-2832-412c-ad2c-1ec0d8ff637d/locations HTTP/1.1" 200 OK
2026-01-30 14:50:48,152 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 35 个数据块，总长度: 4580
2026-01-30 14:50:48,152 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 16350 (prompt=14117, completion=2233)
2026-01-30 14:50:48,152 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 实例, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 14:50:48,152 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-30 14:50:48,174 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 14:50:48,175 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:实例): tokens=16350, cost=$0.039976, time=59528ms
2026-01-30 14:50:48,176 - app.services.worldview_sync_service - INFO - [世界观同步] 解析结果: 新人物=11, 新地点=8, 新设定=6
2026-01-30 14:50:48,179 - app.api.v1.import_routes - INFO - [世界观提取] 扫描完成: 5章, 发现 11人物, 8地点, 6设定
2026-01-30 14:50:48,205 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 段融
2026-01-30 14:50:48,220 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 杨震
2026-01-30 14:50:48,243 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 赵穆
2026-01-30 14:50:48,263 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 许儒虎
2026-01-30 14:50:48,278 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 孔斌
2026-01-30 14:50:48,296 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 解道寒
2026-01-30 14:50:48,309 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 萧宗庭
2026-01-30 14:50:48,334 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 李充
2026-01-30 14:50:48,348 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 张征
2026-01-30 14:50:48,359 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 孙老头
2026-01-30 14:50:48,367 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 解雷
2026-01-30 14:50:48,385 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 九州大陆
2026-01-30 14:50:48,399 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 太一门
2026-01-30 14:50:48,411 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 青州
2026-01-30 14:50:48,420 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 源顺镖局
2026-01-30 14:50:48,428 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 贤古县
2026-01-30 14:50:48,439 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 县衙
2026-01-30 14:50:48,448 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 渊阳府
2026-01-30 14:50:48,458 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 段融的家
2026-01-30 14:50:48,473 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 吞噬器灵
2026-01-30 14:50:48,485 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 宗门统治体系
2026-01-30 14:50:48,498 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 器灵理论
2026-01-30 14:50:48,509 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 武学修炼体系
2026-01-30 14:50:48,523 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 职业晋升路径
2026-01-30 14:50:48,535 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 货币体系
2026-01-30 14:50:48,548 - app.services.worldview_sync_service - INFO - [世界观同步] 创建关系: 段融 -> 杨震: 发小/挚友
2026-01-30 14:50:48,551 - app.services.worldview_sync_service - INFO - [世界观同步] 创建关系: 段融 -> 赵穆: 上下级与初期冲突
2026-01-30 14:50:48,551 - app.services.worldview_sync_service - INFO - [世界观同步] 创建关系: 段融 -> 孔斌: 同期竞争对手
2026-01-30 14:50:48,556 - app.services.worldview_sync_service - INFO - [世界观同步] 创建关系: 段融 -> 李充: 敌视与被挑衅
2026-01-30 14:50:48,576 - app.services.worldview_sync_service - INFO - [Worldview Sync] Cache invalidated: worldview:characters:57b6b0cc-2832-412c-ad2c-1ec0d8ff637d
2026-01-30 14:50:48,582 - app.services.worldview_sync_service - INFO - [Worldview Sync] Cache invalidated: worldview:locations:57b6b0cc-2832-412c-ad2c-1ec0d8ff637d
2026-01-30 14:50:48,586 - app.services.worldview_sync_service - INFO - [Worldview Sync] Cache invalidated: worldview:settings:57b6b0cc-2832-412c-ad2c-1ec0d8ff637d
2026-01-30 14:50:48,591 - app.services.worldview_sync_service - INFO - [Worldview Sync] Cache invalidated: worldview:guidelines:57b6b0cc-2832-412c-ad2c-1ec0d8ff637d
2026-01-30 14:50:48,596 - app.services.worldview_sync_service - INFO - [Worldview Sync] Cache invalidated: worldview:worlddata:57b6b0cc-2832-412c-ad2c-1ec0d8ff637d
2026-01-30 14:50:48,597 - app.api.v1.import_routes - INFO - [世界观提取] 应用完成: {'characters_created': 11, 'characters_updated': 0, 'locations_created': 8, 'settings_created': 6, 'relationships_created': 4}
INFO:     127.0.0.1:58490 - "GET /api/v1/worldview/works/57b6b0cc-2832-412c-ad2c-1ec0d8ff637d/characters HTTP/1.1" 200 OK
INFO:     127.0.0.1:58492 - "GET /api/v1/worldview/works/57b6b0cc-2832-412c-ad2c-1ec0d8ff637d/locations HTTP/1.1" 200 OK
INFO:     127.0.0.1:61819 - "GET /api/v1/worldview/works/57b6b0cc-2832-412c-ad2c-1ec0d8ff637d/ai-guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:54664 - "GET /api/v1/worldview/works/57b6b0cc-2832-412c-ad2c-1ec0d8ff637d/settings HTTP/1.1" 200 OK
INFO:     127.0.0.1:54666 - "GET /api/v1/worldview/works/57b6b0cc-2832-412c-ad2c-1ec0d8ff637d/guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:58822 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2026-01-30 14:51:35,080 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-30 14:51:35,080 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-30 14:51:35,080 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2026-01-30 14:51:36,917 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz:8443/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-30 14:51:36,917 - app.api.v1.agent - INFO - [Chat Stream] Mode: planning
2026-01-30 14:51:36,929 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:57487 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2026-01-30 14:51:36,947 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 仅限第1–3章。请找出所有包含“器灵/吞噬/器物/等阶/吞噬要求/吞噬效果”的段落，必须逐条读取原文...
2026-01-30 14:51:36,948 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-30 14:51:36,949 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-30 14:51:36,949 - app.services.ai.http_ai_service - INFO - [成本追踪] 初始化未传db/user_id，将使用请求上下文按需记录成本
2026-01-30 14:51:38,475 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz:8443/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-30 14:51:38,475 - app.services.agent.tools.writing_tools - INFO - Writing tools AI service initialized
2026-01-30 14:51:38,475 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ AI Service 已同时设置到 langgraph_tools 和 writing_tools
2026-01-30 14:51:38,475 - app.services.context.adaptive_budget - INFO - ✅ 所有预算配置验证通过
2026-01-30 14:51:46,745 - app.services.context.vector_memory_store - INFO - ✅ VectorMemoryStore初始化成功 | 目录=./data/chroma_db | 模型=paraphrase-multilingual-MiniLM-L12-v2 | 集合=user_memories
2026-01-30 14:51:46,745 - app.services.context.manager - INFO - ✅ VectorMemoryStore 已初始化
2026-01-30 14:51:46,745 - app.services.context.manager - INFO - ✅ ContextManager: 长期记忆已启用 (user_id=None)
2026-01-30 14:51:46,745 - app.services.context.manager - INFO - ✅ ContextManager: 自适应预算已启用
2026-01-30 14:51:46,745 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ ContextManager已初始化（长期记忆已启用，自适应预算已启用，总预算=16000 tokens）
成功加载模板: analyze_text (版本 3.1.0)
成功加载模板: writing_agent (版本 2.0.0)
成功加载模板: system_agent_prompt (版本 2.1.0)
成功加载模板: creative_writing_prompt (版本 1.0.0)
2026-01-30 14:51:46,790 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ PromptManager已初始化
2026-01-30 14:51:46,810 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ Redis连接验证成功
2026-01-30 14:51:46,813 - app.services.agent.langgraph_agent - INFO - [LangGraph] OK 使用 AsyncRedisSaver（redis://localhost:6379/0，TTL=7天）
2026-01-30 14:51:46,814 - app.services.agent.memory.metrics - INFO - [MemoryMetrics] 监控系统已初始化
2026-01-30 14:51:46,815 - app.services.agent.memory.long_term_store - INFO - [LongTermStore] Initialized: base_dir=./data/long_term_memory, max_size=50KB, compression=True
2026-01-30 14:51:46,816 - app.services.agent.memory.enhanced_memory_manager - INFO - EnhancedMemoryManager initialized: short=10, medium=100, threshold=0.1, long_term_backup=enabled
2026-01-30 14:51:46,817 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ EnhancedMemoryManager已创建
2026-01-30 14:51:46,818 - app.services.agent.memory.unified_coordinator - INFO - [UnifiedMemoryCoordinator] 初始化统一记忆协调器
2026-01-30 14:51:46,820 - app.services.agent.memory.unified_coordinator - INFO - [UnifiedMemoryCoordinator] 全局实例已设置
2026-01-30 14:51:46,820 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ UnifiedMemoryCoordinator已初始化 | checkpointer=AsyncRedisSaver | enhanced_memory=yes | context_manager=yes
2026-01-30 14:51:46,820 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ 解耦模块已初始化 (IntentClassifier, ToolExecutor, EventParser, ResponseBuilder, ToolDispatcher, ParallelExecutor, PlanGenerator, QuickPathHandler, StreamEventHandler, SecondaryToolHandler, TaskRunner, AgentExecutor)
2026-01-30 14:51:46,825 - app.services.agent.parallel_tool_node - INFO - [ParallelToolNode] 初始化完成，最大并发数=5，并行安全工具=6个
2026-01-30 14:51:46,845 - app.api.v1.agent - INFO - [Global Agent] created global agent instance; MemorySaver shared across requests
2026-01-30 14:51:46,870 - app.api.v1.agent - INFO - [agent_chat_stream] 📚 世界观数据已注入: 人物=11, 地点=8, 设定=6, 规范=无
2026-01-30 14:51:46,870 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:57b6b0cc-2832-412c-ad2c-1ec0d8ff637d:ee47fc57-5bea-4a83-8013-d9134672a763 (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=57b6b0cc-2832-412c-ad2c-1ec0d8ff637d, conversation_id=ee47fc57-5bea-4a83-8013-d9134672a763)
2026-01-30 14:51:46,870 - app.services.context.monitoring_integration - INFO - ✅ ContextManager监控收集器已初始化
2026-01-30 14:51:46,870 - app.services.context.store - INFO - [ContextStore] Redis连接成功
2026-01-30 14:51:46,884 - app.services.context.manager - INFO - [ContextManager] 创建新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:57b6b0cc-2832-412c-ad2c-1ec0d8ff637d:ee47fc57-5bea-4a83-8013-d9134672a763
2026-01-30 14:51:47,248 - app.services.context.token_counter - INFO - ✅ tiktoken初始化成功，模型: gemini-2.5-pro -> cl100k_base
2026-01-30 14:51:47,249 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:57b6b0cc-2832-412c-ad2c-1ec0d8ff637d:ee47fc57-5bea-4a83-8013-d9134672a763: 0/16000 tokens
2026-01-30 14:51:49,174 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='仅限第1–3章。请找出所有包含“器灵/吞噬/器物/等阶/吞噬...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:57b6b0cc-2832-412c-ad2c-1ec0d8ff637d', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=0条
2026-01-30 14:51:49,179 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=57b6b0cc-2832-412c-ad2c-1ec0d8ff637d | 含用户级=True | 找到=0条
2026-01-30 14:51:49,261 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 0条消息, 0 tokens, 耗时 2391.49ms
2026-01-30 14:51:49,261 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-30 14:51:49,269 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-30 14:51:49,270 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=200, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-30 14:51:51,181 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 14:51:51,185 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-30 14:51:51,231 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 14:51:51,240 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=481, cost=$0.000053, time=1917ms
2026-01-30 14:51:51,240 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=39, 尝试次数=1
2026-01-30 14:51:51,245 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-30 14:51:51,245 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-30 14:51:51,245 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=20, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-30 14:51:53,769 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 14:51:53,769 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-30 14:51:53,806 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 14:51:53,808 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=406, cost=$0.000041, time=2524ms
2026-01-30 14:51:53,808 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=8, 尝试次数=1
2026-01-30 14:51:53,808 - app.services.agent.intent.classifier - INFO - [Intent] AI识别结果: analysis
2026-01-30 14:51:53,808 - app.services.agent.langgraph_agent - INFO - [Planning] AI意图分类: analysis (置信度: 0.90)
2026-01-30 14:51:53,808 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 仅限第1–3章。请找出所有包含“器灵/吞噬/器物/等阶/吞噬要求/吞噬效果”的段落，必须逐条读取原文...
2026-01-30 14:51:53,823 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-30 14:51:53,824 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=story_planning, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: story_planning; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-01-30 14:51:53,824 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.3, task_type=TaskType.STORY_PLANNING
2026-01-30 14:52:06,271 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-30 14:52:09,741 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 9 个数据块，总长度: 941
2026-01-30 14:52:09,741 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 21876 (prompt=21398, completion=478)
2026-01-30 14:52:09,745 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 14:52:09,746 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-30 14:52:09,778 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 14:52:09,787 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=21876, cost=$0.031527, time=15921ms
2026-01-30 14:52:09,787 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=21876
2026-01-30 14:52:09,789 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户需要一个表格，其中包含第1-3章中所有提及特定关键词（器, 原料=需要读取作品第1章、第2章和第3章的全部, 处理=使用`explore_content`工
2026-01-30 14:52:09,811 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共1个任务
2026-01-30 14:52:09,811 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共1个任务，耗时: 16.00s
2026-01-30 14:52:09,811 - app.api.v1.agent - INFO - [Stream] Plan tasks: 1 items
2026-01-30 14:52:09,811 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2026-01-30 14:52:09,811 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2026-01-30 14:52:09,811 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2026-01-30 14:52:09,811 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] DAG 调度启用，任务数=1, 有依赖任务=0
2026-01-30 14:52:09,811 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1开始: 读取作品的第1、2、3章，以查找包含“器灵”、“吞噬”、“器物”、“等阶”、“吞噬要求”、“吞噬效果”等关键词的段落。
2026-01-30 14:52:09,811 - app.api.v1.agent - INFO - [Stream] Task started: 读取作品的第1、2、3章，以查找包含“器灵”、“吞噬”、“器物”、“等阶”、“吞噬要求”、“吞噬效果”等关键词的段落。 (icon=Wrench)
2026-01-30 14:52:09,811 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: explore_content
2026-01-30 14:52:09,811 - app.services.agent.tools.explore_tools - INFO - [explore_content] 开始: work_id=57b6b0cc-2832-412c-ad2c-1ec0d8ff637d, target=读取第1-3章，找出所有包含“器灵/吞噬/器物/等阶/吞噬要求/吞噬效果”的段落
约束：章节范围：第...
2026-01-30 14:52:09,821 - app.services.agent.tools.explore_tools - INFO - [explore_content] 规划传入关键词: ['器灵', '吞噬', '器物', '等阶', '吞噬要求', '吞噬效果']
2026-01-30 14:52:09,824 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 启用严格段落号模式
2026-01-30 14:52:09,824 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 章节范围锁定: 第1-3章
2026-01-30 14:52:09,824 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 任务禁止整章阅读
2026-01-30 14:52:09,824 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 开始探索 V5: work_id=57b6b0cc-2832-412c-ad2c-1ec0d8ff637d, target=读取第1-3章，找出所有包含“器灵/吞噬/器物/等阶/吞噬要求/吞噬效果”的段落
约束：章节范围：第...
2026-01-30 14:52:09,824 - app.services.chapter_service - INFO - [ChapterService] Querying chapters for work_id=57b6b0cc-2832-412c-ad2c-1ec0d8ff637d, type=<class 'uuid.UUID'>
2026-01-30 14:52:09,837 - app.services.chapter_service - INFO - [ChapterService] Found 5 chapters
2026-01-30 14:52:09,837 - app.services.chapter_service - INFO -   - Chapter: 第1章 吞噬, order=1
2026-01-30 14:52:09,837 - app.services.chapter_service - INFO -   - ... (3 more chapters)
2026-01-30 14:52:09,837 - app.services.chapter_service - INFO -   - Chapter: 第5章 太一门, order=5
2026-01-30 14:52:09,875 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 章节范围映射: 第1-3章 -> 第1-3章
2026-01-30 14:52:09,884 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 自动获取世界观...
2026-01-30 14:52:09,890 - app.services.agent.langgraph_tools - INFO - [get_writing_context] ✅ 获取创作上下文成功: include=worldview
2026-01-30 14:52:09,893 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 世界观获取完成: 25 条
2026-01-30 14:52:09,893 - app.services.ai.http_ai_service - INFO - [成本追踪] 初始化未传db/user_id，将使用请求上下文按需记录成本
2026-01-30 14:52:11,496 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz:8443/v1, Model: gemini-2.5-flash, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: False, CostTracking: True
2026-01-30 14:52:11,504 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 14:52:11,504 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=80, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 14:52:18,665 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 14:52:18,665 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 14:52:18,705 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 14:52:18,705 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=967, cost=$0.000316, time=7160ms
2026-01-30 14:52:18,713 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=17, 尝试次数=1
2026-01-30 14:52:18,713 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 强制流程步骤: list_chapters
2026-01-30 14:52:18,713 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=list_chapters params={"work_id": "57b6b0cc-2832-412c-ad2c-1ec0d8ff637d"}
2026-01-30 14:52:18,713 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=list_chapters success=True count=3
2026-01-30 14:52:18,713 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 14:52:18,713 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=80, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 14:52:22,826 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 14:52:22,826 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 14:52:22,841 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 14:52:22,847 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=800, cost=$0.000258, time=4113ms
2026-01-30 14:52:22,849 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=10, 尝试次数=1
2026-01-30 14:52:22,849 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 强制流程步骤: list_paragraphs
2026-01-30 14:52:22,851 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=list_paragraphs params={"chapter_order": 1, "offset": 0, "limit": 50, "preview_len": 80, "work_id": "57b6b0cc-2832-412c-ad2c-1ec0d8ff637d"}
2026-01-30 14:52:22,866 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=list_paragraphs success=True chapter=1 offset=0 limit=50 approximate=None
2026-01-30 14:52:22,866 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 14:52:22,871 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 14:52:25,358 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 14:52:25,358 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 14:52:25,373 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 14:52:25,380 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1646, cost=$0.000822, time=2486ms
2026-01-30 14:52:25,381 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=313, 尝试次数=1
2026-01-30 14:52:25,383 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"keywords": ["器灵", "吞噬", "器物", "等阶", "吞噬要求", "吞噬效果"], "match_mode": "any", "limit": 100, "chapter_order": 1, "work_id": "57b6b0cc-2832-412c-ad2c-1ec0d8ff637d"}
2026-01-30 14:52:25,384 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 世界观匹配: 4 条
2026-01-30 14:52:25,463 - app.services.chapter_vector_service - INFO - [exact_search] work=57b6b0cc-2832-412c-ad2c-1ec0d8ff637d, keywords=['器灵', '吞噬', '器物']..., mode=any, range=(1, 1), hits=63
2026-01-30 14:52:25,480 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=33 corrected=False final=33
2026-01-30 14:52:25,480 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第33段
2026-01-30 14:52:25,490 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=35 corrected=False final=35
2026-01-30 14:52:25,490 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第35段
2026-01-30 14:52:25,505 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=36 corrected=False final=36
2026-01-30 14:52:25,505 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第36段
2026-01-30 14:52:25,513 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=37 corrected=False final=37
2026-01-30 14:52:25,513 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第37段
2026-01-30 14:52:25,522 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=38 corrected=False final=38
2026-01-30 14:52:25,522 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第38段
2026-01-30 14:52:25,536 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=39 corrected=False final=39
2026-01-30 14:52:25,538 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第39段
2026-01-30 14:52:25,548 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=41 corrected=False final=41
2026-01-30 14:52:25,548 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第41段
2026-01-30 14:52:25,558 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=42 corrected=False final=42
2026-01-30 14:52:25,558 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第42段
2026-01-30 14:52:25,572 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=69 corrected=False final=69
2026-01-30 14:52:25,580 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第69段
2026-01-30 14:52:25,592 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=70 corrected=False final=70
2026-01-30 14:52:25,592 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第70段
2026-01-30 14:52:25,605 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=72 corrected=False final=72
2026-01-30 14:52:25,605 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第72段
2026-01-30 14:52:25,621 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=73 corrected=False final=73
2026-01-30 14:52:25,622 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第73段
2026-01-30 14:52:25,630 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=74 corrected=False final=74
2026-01-30 14:52:25,630 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第74段
2026-01-30 14:52:25,644 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=75 corrected=False final=75
2026-01-30 14:52:25,644 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第75段
2026-01-30 14:52:25,653 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=76 corrected=False final=76
2026-01-30 14:52:25,653 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第76段
2026-01-30 14:52:25,656 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=78 corrected=False final=78
2026-01-30 14:52:25,656 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第78段
2026-01-30 14:52:25,671 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=79 corrected=False final=79
2026-01-30 14:52:25,671 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第79段
2026-01-30 14:52:25,680 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=81 corrected=False final=81
2026-01-30 14:52:25,680 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第81段
2026-01-30 14:52:25,685 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=21 (chapter=21, worldview=4) keywords=器灵,吞噬,器物,等阶,吞噬要求,吞噬效果
2026-01-30 14:52:25,685 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 14:52:25,688 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 14:52:32,630 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 14:52:32,630 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 14:52:32,647 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 14:52:32,647 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4368, cost=$0.001546, time=6942ms
2026-01-30 14:52:32,654 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=161, 尝试次数=1
2026-01-30 14:52:32,655 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 14:52:32,657 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=200, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 14:52:37,605 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 14:52:37,612 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 14:52:37,638 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 14:52:37,638 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1120, cost=$0.000481, time=4955ms
2026-01-30 14:52:37,638 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=93, 尝试次数=1
2026-01-30 14:52:37,646 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 探索完成(工具循环): 3轮, 原因=已完成目标任务。在第1-3章范围内，所有包含关键词“器灵/吞噬/器物/等阶/吞噬要求/吞噬效果”的段落均已通过上一次精确搜索找到并收集。搜索结果显示所有命中段落均在第1章，且第1章已全部读取。第2章和第3章未发现相关段落。
2026-01-30 14:52:37,646 - app.services.agent.execution.tool_executor - INFO - [StandardTool] explore_content 执行成功
2026-01-30 14:52:37,655 - app.api.v1.agent - INFO - [Stream] 任务完成: 读取作品的第1、2、3章，以查找包含“器灵”、“吞噬”、“器物”、“等阶”、“吞噬要求”、“吞噬效果”等关键词的段落。 (27.8s)
2026-01-30 14:52:37,657 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1完成
2026-01-30 14:52:37,657 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共1个任务，耗时: 27.85s
2026-01-30 14:52:37,657 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2026-01-30 14:52:37,657 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=1, 展示型=0
2026-01-30 14:52:37,657 - app.services.agent.langgraph_agent - INFO - [Response] 单个输出任务(explore_content)，使用AI整合
2026-01-30 14:52:37,657 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2026-01-30 14:52:37,657 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=1, 展示型=0
2026-01-30 14:52:37,657 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=1758字符, 处理后=1822字符
2026-01-30 14:52:37,657 - app.services.agent.planning.response_builder - INFO - [Summarization] 准备发送 summarization_start 事件
2026-01-30 14:52:37,657 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-30 14:52:37,663 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-30 14:52:37,663 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=60, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 14:52:39,126 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 14:52:39,132 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-30 14:52:39,169 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 14:52:39,175 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=328, cost=$0.000045, time=1468ms
2026-01-30 14:52:39,175 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=58, 尝试次数=1
2026-01-30 14:52:39,175 - app.services.agent.planning.response_builder - INFO - [Summarization] reason生成: len=58 content=已完成对第1-3章的探索，共找到18条包含“器灵”、“吞噬”、“器物”、“等阶”、“吞噬要求”、“吞噬效果”的段落。
2026-01-30 14:52:39,175 - app.services.agent.stream.stream_event_handler - INFO - [StreamEventHandler] emit_summarization_start 被调用, _on_flow_event=True, reason_len=58, reason=已完成对第1-3章的探索，共找到18条包含“器灵”、“吞噬”、“器物”、“等阶”、“吞噬要求”、“吞噬效果”的段落。
2026-01-30 14:52:39,175 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_start 事件已发送
2026-01-30 14:52:39,179 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2026-01-30 14:52:39,179 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2026-01-30 14:52:39,185 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-30 14:52:39,185 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-30 14:52:39,188 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=20000, temp=0.7, task_type=TaskType.SUMMARIZATION
2026-01-30 14:52:57,050 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-30 14:52:57,050 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_complete 事件已发送（第一个chunk时）
2026-01-30 14:52:57,055 - app.services.agent.planning.response_builder - INFO - [Summarization] output_ready 事件已发送（第一个chunk时）
2026-01-30 14:52:58,958 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 9 个数据块，总长度: 754
2026-01-30 14:52:58,959 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 7981 (prompt=7437, completion=544)
2026-01-30 14:52:58,960 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 14:52:58,960 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-30 14:52:58,978 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 14:52:58,981 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=7981, cost=$0.003591, time=19772ms
2026-01-30 14:52:58,982 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=754
2026-01-30 14:52:59,110 - app.services.context.vector_memory_store - INFO - 🔁 跳过重复记忆，复用ID=79913e7e-d5cd-4e09-bce6-ca6639bd8456_1769696287283_02f23afe
2026-01-30 14:52:59,111 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:57b6b0cc-2832-412c-ad2c-1ec0d8ff637d | 重要度=0.87
2026-01-30 14:53:00,447 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:57b6b0cc-2832-412c-ad2c-1ec0d8ff637d | 重要度=0.77
2026-01-30 14:53:00,458 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:57b6b0cc-2832-412c-ad2c-1ec0d8ff637d:ee47fc57-5bea-4a83-8013-d9134672a763, token=974
2026-01-30 14:53:00,459 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:57b6b0cc-2832-412c-ad2c-1ec0d8ff637d:ee47fc57-5bea-4a83-8013-d9134672a763, 消息数=2, 摘要长度=0, Token=974
2026-01-30 14:53:00,459 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:57b6b0cc-2832-412c-ad2c-1ec0d8ff637d:ee47fc57-5bea-4a83-8013-d9134672a763)
2026-01-30 14:53:00,460 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2026-01-30 14:53:00,474 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed
INFO:     127.0.0.1:65057 - "GET /api/v1/agent/operations/ee47fc57-5bea-4a83-8013-d9134672a763 HTTP/1.1" 200 OK
2026-01-30 14:54:04,515 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-30 14:54:04,515 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-30 14:54:04,516 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2026-01-30 14:54:06,104 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz:8443/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-30 14:54:06,104 - app.api.v1.agent - INFO - [Chat Stream] Mode: planning
2026-01-30 14:54:06,110 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:56433 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2026-01-30 14:54:06,137 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 仅第2章。完整复原赵穆讲解“羚羊献食”动作要点的顺序。
  - 不允许跳段或合并概括
  限定第1–...
2026-01-30 14:54:06,154 - app.api.v1.agent - INFO - [agent_chat_stream] 📚 世界观数据已注入: 人物=11, 地点=8, 设定=6, 规范=无
2026-01-30 14:54:06,158 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:57b6b0cc-2832-412c-ad2c-1ec0d8ff637d:ee47fc57-5bea-4a83-8013-d9134672a763 (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=57b6b0cc-2832-412c-ad2c-1ec0d8ff637d, conversation_id=ee47fc57-5bea-4a83-8013-d9134672a763)
2026-01-30 14:54:06,165 - app.services.context.store - INFO - [ContextStore] 加载上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:57b6b0cc-2832-412c-ad2c-1ec0d8ff637d:ee47fc57-5bea-4a83-8013-d9134672a763, 2条消息
2026-01-30 14:54:06,170 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:57b6b0cc-2832-412c-ad2c-1ec0d8ff637d:ee47fc57-5bea-4a83-8013-d9134672a763: 974/16000 tokens
2026-01-30 14:54:06,413 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='仅第2章。完整复原赵穆讲解“羚羊献食”动作要点的顺序。
  ...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:57b6b0cc-2832-412c-ad2c-1ec0d8ff637d', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=1条
2026-01-30 14:54:06,418 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=57b6b0cc-2832-412c-ad2c-1ec0d8ff637d | 含用户级=True | 找到=1条
2026-01-30 14:54:06,426 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 3条消息, 974 tokens, 耗时 268.38ms
2026-01-30 14:54:06,428 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 3 条历史消息 (token: 974, has_summary: False)
2026-01-30 14:54:06,429 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-30 14:54:06,430 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-30 14:54:06,430 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=200, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-30 14:54:08,496 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 14:54:08,499 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-30 14:54:08,528 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 14:54:08,529 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1181, cost=$0.000124, time=2069ms
2026-01-30 14:54:08,531 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=42, 尝试次数=1
2026-01-30 14:54:08,531 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-30 14:54:08,534 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-30 14:54:08,534 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=20, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-30 14:54:09,347 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 14:54:09,350 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-30 14:54:09,377 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 14:54:09,379 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=422, cost=$0.000043, time=816ms
2026-01-30 14:54:09,379 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=7, 尝试次数=1
2026-01-30 14:54:09,379 - app.services.agent.intent.classifier - INFO - [Intent] AI识别结果: writing
2026-01-30 14:54:09,379 - app.services.agent.langgraph_agent - INFO - [Planning] AI意图分类: writing (置信度: 0.90)
2026-01-30 14:54:09,382 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 仅第2章。完整复原赵穆讲解“羚羊献食”动作要点的顺序。
  - 不允许跳段或合并概括
  限定第1–...
2026-01-30 14:54:09,394 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-30 14:54:09,396 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=story_planning, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: story_planning; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-01-30 14:54:09,396 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.3, task_type=TaskType.STORY_PLANNING
2026-01-30 14:54:25,118 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-30 14:54:31,143 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 13 个数据块，总长度: 1500
2026-01-30 14:54:31,143 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 23213 (prompt=22451, completion=762)
2026-01-30 14:54:31,143 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 14:54:31,145 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-30 14:54:31,168 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 14:54:31,172 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=23213, cost=$0.035684, time=21750ms
2026-01-30 14:54:31,172 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=23213
2026-01-30 14:54:31,172 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户需要完成两个独立的查询任务：1. 完整复原第2章中“羚羊, 原料=完成这两个任务需要读取并检索第1、2、3, 处理=使用 explore_content 工
2026-01-30 14:54:31,172 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共2个任务
2026-01-30 14:54:31,177 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共2个任务，耗时: 21.80s
2026-01-30 14:54:31,178 - app.api.v1.agent - INFO - [Stream] Plan tasks: 2 items
2026-01-30 14:54:31,178 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2026-01-30 14:54:31,179 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2026-01-30 14:54:31,180 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2026-01-30 14:54:31,180 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] DAG 调度启用，任务数=2, 有依赖任务=0
2026-01-30 14:54:31,180 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1开始: 在第2章中，查找所有关于赵穆讲解“羚羊献食”动作要点的段落，用于复原其讲解顺序。
2026-01-30 14:54:31,180 - app.api.v1.agent - INFO - [Stream] Task started: 在第2章中，查找所有关于赵穆讲解“羚羊献食”动作要点的段落，用于复原其讲解顺序。 (icon=Wrench)
2026-01-30 14:54:31,180 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: explore_content
2026-01-30 14:54:31,188 - app.services.agent.tools.explore_tools - INFO - [explore_content] 开始: work_id=57b6b0cc-2832-412c-ad2c-1ec0d8ff637d, target=仅第2章。完整复原赵穆讲解“羚羊献食”动作要点的顺序。
约束：章节范围：第1–3章、1–3章、第2章...
2026-01-30 14:54:31,189 - app.services.agent.tools.explore_tools - INFO - [explore_content] 规划传入关键词: ['羚羊献食', '赵穆', '动作要点', '右腿', '左腿', '腰腹']
2026-01-30 14:54:31,190 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 启用严格段落号模式
2026-01-30 14:54:31,190 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 章节范围锁定: 第1-3章
2026-01-30 14:54:31,190 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 任务禁止整章阅读
2026-01-30 14:54:31,190 - app.services.agent.tools.explore_tools - INFO - [explore_content] 复用共享状态: searched=6, read_paragraphs=18, read_chapters=0
2026-01-30 14:54:31,190 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 开始探索 V5: work_id=57b6b0cc-2832-412c-ad2c-1ec0d8ff637d, target=仅第2章。完整复原赵穆讲解“羚羊献食”动作要点的顺序。
约束：章节范围：第1–3章、1–3章、第2章...
2026-01-30 14:54:31,190 - app.services.chapter_service - INFO - [ChapterService] Querying chapters for work_id=57b6b0cc-2832-412c-ad2c-1ec0d8ff637d, type=<class 'uuid.UUID'>
2026-01-30 14:54:31,210 - app.services.chapter_service - INFO - [ChapterService] Found 5 chapters
2026-01-30 14:54:31,212 - app.services.chapter_service - INFO -   - Chapter: 第1章 吞噬, order=1
2026-01-30 14:54:31,213 - app.services.chapter_service - INFO -   - ... (3 more chapters)
2026-01-30 14:54:31,213 - app.services.chapter_service - INFO -   - Chapter: 第5章 太一门, order=5
2026-01-30 14:54:31,213 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 章节范围映射: 第1-3章 -> 第1-3章
2026-01-30 14:54:31,224 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 自动获取世界观...
2026-01-30 14:54:31,232 - app.services.agent.langgraph_tools - INFO - [get_writing_context] ✅ 获取创作上下文成功: include=worldview
2026-01-30 14:54:31,234 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 世界观获取完成: 25 条
2026-01-30 14:54:31,234 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 14:54:31,234 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=80, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 14:54:37,633 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 14:54:37,636 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 14:54:37,664 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 14:54:37,664 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1014, cost=$0.000315, time=6402ms
2026-01-30 14:54:37,664 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=9, 尝试次数=1
2026-01-30 14:54:37,664 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 强制流程步骤: list_chapters
2026-01-30 14:54:37,664 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=list_chapters params={"work_id": "57b6b0cc-2832-412c-ad2c-1ec0d8ff637d"}
2026-01-30 14:54:37,669 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=list_chapters success=True count=3
2026-01-30 14:54:37,670 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 14:54:37,670 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=80, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 14:54:48,687 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 14:54:48,688 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 14:54:48,706 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 14:54:48,709 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1775, cost=$0.000559, time=11018ms
2026-01-30 14:54:48,709 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=17, 尝试次数=1
2026-01-30 14:54:48,709 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 强制流程步骤: list_paragraphs
2026-01-30 14:54:48,712 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=list_paragraphs params={"chapter_order": 1, "offset": 0, "limit": 50, "preview_len": 80, "work_id": "57b6b0cc-2832-412c-ad2c-1ec0d8ff637d"}
2026-01-30 14:54:48,722 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=list_paragraphs success=True chapter=1 offset=0 limit=50 approximate=None
2026-01-30 14:54:48,723 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 14:54:48,723 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 14:54:51,186 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 14:54:51,187 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 14:54:51,212 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 14:54:51,216 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1697, cost=$0.000749, time=2465ms
2026-01-30 14:54:51,216 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=210, 尝试次数=1
2026-01-30 14:54:51,216 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=list_paragraphs params={"chapter_order": 2, "offset": 0, "limit": 50, "work_id": "57b6b0cc-2832-412c-ad2c-1ec0d8ff637d"}
2026-01-30 14:54:51,229 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=list_paragraphs success=True chapter=2 offset=0 limit=50 approximate=None
2026-01-30 14:54:51,229 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 14:54:51,229 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 14:54:57,404 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 14:54:57,407 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 14:54:57,417 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 14:54:57,420 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2401, cost=$0.000945, time=6177ms
2026-01-30 14:54:57,420 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=199, 尝试次数=1
2026-01-30 14:54:57,423 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=read_paragraphs params={"chapter_order": 2, "offset": 5, "limit": 15, "work_id": "57b6b0cc-2832-412c-ad2c-1ec0d8ff637d"}
2026-01-30 14:54:57,433 - app.services.agent.langgraph_tools - INFO - [read_paragraphs] start items=13 index_base=zero
2026-01-30 14:54:57,442 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=5 corrected=False final=5
2026-01-30 14:54:57,451 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第5段
2026-01-30 14:54:57,462 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=6 corrected=False final=6
2026-01-30 14:54:57,462 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第6段
2026-01-30 14:54:57,471 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=7 corrected=False final=7
2026-01-30 14:54:57,471 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第7段
2026-01-30 14:54:57,480 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=8 corrected=False final=8
2026-01-30 14:54:57,485 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第8段
2026-01-30 14:54:57,488 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=9 corrected=False final=9
2026-01-30 14:54:57,495 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第9段
2026-01-30 14:54:57,504 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=10 corrected=False final=10
2026-01-30 14:54:57,504 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第10段
2026-01-30 14:54:57,513 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=11 corrected=False final=11
2026-01-30 14:54:57,513 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第11段
2026-01-30 14:54:57,522 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=12 corrected=False final=12
2026-01-30 14:54:57,522 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第12段
2026-01-30 14:54:57,530 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=13 corrected=False final=13
2026-01-30 14:54:57,530 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第13段
2026-01-30 14:54:57,540 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=14 corrected=False final=14
2026-01-30 14:54:57,540 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第14段
2026-01-30 14:54:57,545 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=15 corrected=False final=15
2026-01-30 14:54:57,545 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第15段
2026-01-30 14:54:57,554 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=16 corrected=False final=16
2026-01-30 14:54:57,554 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第16段
2026-01-30 14:54:57,562 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=17 corrected=False final=17
2026-01-30 14:54:57,570 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第17段
2026-01-30 14:54:57,573 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=read_paragraphs success=True count=13 index_base=None
2026-01-30 14:54:57,575 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 14:54:57,575 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 14:55:03,202 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 14:55:03,202 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 14:55:03,221 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 14:55:03,224 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2879, cost=$0.001123, time=5628ms
2026-01-30 14:55:03,226 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=172, 尝试次数=1
2026-01-30 14:55:03,226 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 14:55:03,226 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=200, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 14:55:14,736 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 14:55:14,737 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 14:55:14,754 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 14:55:14,755 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2782, cost=$0.001006, time=11511ms
2026-01-30 14:55:14,755 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=103, 尝试次数=1
2026-01-30 14:55:14,755 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 探索完成(工具循环): 4轮, 原因=已完整复原赵穆在第2章讲解“羚羊献食”动作要点的顺序。根据已读取的段落，动作要点包括：1. 右脚上前落在左脚前方，抬左脚向前弹踢；2. 同时，右手刀由前向右下方，划弧抡撩，然后挑于前方，刀刃向上，刀尖向前。第7段为省略号，第8段表明讲解已结束。
2026-01-30 14:55:14,762 - app.services.agent.execution.tool_executor - INFO - [StandardTool] explore_content 执行成功
2026-01-30 14:55:14,762 - app.api.v1.agent - INFO - [Stream] 任务完成: 在第2章中，查找所有关于赵穆讲解“羚羊献食”动作要点的段落，用于复原其讲解顺序。 (43.6s)
2026-01-30 14:55:14,770 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1完成
2026-01-30 14:55:14,771 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务2开始: 在第1至3章中，查找与时间线（进入镖局→考核前半个月→傍晚练武→晚饭后→夜里练刀/梦境→醒后练功）相关的原文证据。
2026-01-30 14:55:14,771 - app.api.v1.agent - INFO - [Stream] Task started: 在第1至3章中，查找与时间线（进入镖局→考核前半个月→傍晚练武→晚饭后→夜里练刀/梦境→醒后练功）相关的原文证据。 (icon=Wrench)
2026-01-30 14:55:14,771 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: explore_content
2026-01-30 14:55:14,771 - app.services.agent.tools.explore_tools - INFO - [explore_content] 开始: work_id=57b6b0cc-2832-412c-ad2c-1ec0d8ff637d, target=限定第1–3章，构建“时间线”：进入镖局 → 考核前半个月 → 傍晚练武 → 晚饭后 → 夜里练刀/...
2026-01-30 14:55:14,771 - app.services.agent.tools.explore_tools - INFO - [explore_content] 规划传入关键词: ['进入镖局', '考核', '半个月', '傍晚', '晚饭后', '夜里', '梦境', '醒后', '练功', '练刀']
2026-01-30 14:55:14,771 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 启用严格段落号模式
2026-01-30 14:55:14,771 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 章节范围锁定: 第1-3章
2026-01-30 14:55:14,771 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 任务禁止整章阅读
2026-01-30 14:55:14,779 - app.services.agent.tools.explore_tools - INFO - [explore_content] 复用共享状态: searched=6, read_paragraphs=31, read_chapters=0
2026-01-30 14:55:14,780 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 开始探索 V5: work_id=57b6b0cc-2832-412c-ad2c-1ec0d8ff637d, target=限定第1–3章，构建“时间线”：进入镖局 → 考核前半个月 → 傍晚练武 → 晚饭后 → 夜里练刀/...
2026-01-30 14:55:14,780 - app.services.chapter_service - INFO - [ChapterService] Querying chapters for work_id=57b6b0cc-2832-412c-ad2c-1ec0d8ff637d, type=<class 'uuid.UUID'>
2026-01-30 14:55:14,793 - app.services.chapter_service - INFO - [ChapterService] Found 5 chapters
2026-01-30 14:55:14,794 - app.services.chapter_service - INFO -   - Chapter: 第1章 吞噬, order=1
2026-01-30 14:55:14,794 - app.services.chapter_service - INFO -   - ... (3 more chapters)
2026-01-30 14:55:14,794 - app.services.chapter_service - INFO -   - Chapter: 第5章 太一门, order=5
2026-01-30 14:55:14,798 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 章节范围映射: 第1-3章 -> 第1-3章
2026-01-30 14:55:14,820 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 自动获取世界观...
2026-01-30 14:55:14,829 - app.services.agent.langgraph_tools - INFO - [get_writing_context] ✅ 获取创作上下文成功: include=worldview
2026-01-30 14:55:14,833 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 世界观获取完成: 25 条
2026-01-30 14:55:14,834 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 14:55:14,835 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=80, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 14:55:19,913 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 14:55:19,916 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 14:55:19,929 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 14:55:19,929 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=833, cost=$0.000270, time=5081ms
2026-01-30 14:55:19,929 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=15, 尝试次数=1
2026-01-30 14:55:19,929 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 强制流程步骤: list_chapters
2026-01-30 14:55:19,929 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=list_chapters params={"work_id": "57b6b0cc-2832-412c-ad2c-1ec0d8ff637d"}
2026-01-30 14:55:19,929 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=list_chapters success=True count=3
2026-01-30 14:55:19,929 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 14:55:19,937 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=80, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 14:55:23,645 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 14:55:23,646 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 14:55:23,665 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 14:55:23,667 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=753, cost=$0.000252, time=3710ms
2026-01-30 14:55:23,669 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=17, 尝试次数=1
2026-01-30 14:55:23,670 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 强制流程步骤: list_paragraphs
2026-01-30 14:55:23,670 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=list_paragraphs params={"chapter_order": 1, "offset": 0, "limit": 50, "preview_len": 80, "work_id": "57b6b0cc-2832-412c-ad2c-1ec0d8ff637d"}
2026-01-30 14:55:23,679 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=list_paragraphs success=True chapter=1 offset=0 limit=50 approximate=None
2026-01-30 14:55:23,679 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 14:55:23,679 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 14:55:31,214 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 14:55:31,214 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 14:55:31,235 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 14:55:31,237 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2782, cost=$0.001030, time=7534ms
2026-01-30 14:55:31,237 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=202, 尝试次数=1
2026-01-30 14:55:31,237 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"keywords": "考核", "match_mode": "exact", "limit": 50, "work_id": "57b6b0cc-2832-412c-ad2c-1ec0d8ff637d"}
2026-01-30 14:55:31,237 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 世界观匹配: 2 条
2026-01-30 14:55:31,281 - app.services.chapter_vector_service - INFO - [exact_search] work=57b6b0cc-2832-412c-ad2c-1ec0d8ff637d, keywords=['考核']..., mode=any, range=(1, 3), hits=8
2026-01-30 14:55:31,297 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=48 corrected=False final=48
2026-01-30 14:55:31,297 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第48段
2026-01-30 14:55:31,308 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=56 corrected=False final=56
2026-01-30 14:55:31,308 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第56段
2026-01-30 14:55:31,312 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=6 (chapter=4, worldview=2) keywords=考核
2026-01-30 14:55:31,312 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 14:55:31,312 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 14:55:34,838 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 14:55:34,838 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 14:55:34,856 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 14:55:34,862 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2334, cost=$0.000927, time=3526ms
2026-01-30 14:55:34,862 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=230, 尝试次数=1
2026-01-30 14:55:34,862 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"keywords": ["进入镖局", "来到镖局", "加入镖局"], "match_mode": "any", "limit": 50, "work_id": "57b6b0cc-2832-412c-ad2c-1ec0d8ff637d"}
2026-01-30 14:55:34,891 - app.services.chapter_vector_service - INFO - [exact_search] work=57b6b0cc-2832-412c-ad2c-1ec0d8ff637d, keywords=['进入镖局', '来到镖局', '加入镖局']..., mode=any, range=(1, 3), hits=1
2026-01-30 14:55:34,904 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=37 corrected=False final=37
2026-01-30 14:55:34,904 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第37段
2026-01-30 14:55:34,904 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=1 (chapter=1, worldview=0) keywords=进入镖局,来到镖局,加入镖局
2026-01-30 14:55:34,904 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 14:55:34,904 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 14:55:39,011 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 14:55:39,012 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 14:55:39,029 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 14:55:39,034 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1943, cost=$0.000821, time=4108ms
2026-01-30 14:55:39,034 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=231, 尝试次数=1
2026-01-30 14:55:39,034 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"keywords": ["前半个月"], "match_mode": "all", "limit": 10, "work_id": "57b6b0cc-2832-412c-ad2c-1ec0d8ff637d"}
2026-01-30 14:55:39,053 - app.services.chapter_vector_service - INFO - [exact_search] work=57b6b0cc-2832-412c-ad2c-1ec0d8ff637d, keywords=['前半个月']..., mode=all, range=(1, 3), hits=0
2026-01-30 14:55:39,054 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=0 (chapter=0, worldview=0) keywords=前半个月
2026-01-30 14:55:39,057 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 14:55:39,057 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 14:55:41,027 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 14:55:41,032 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 14:55:41,054 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 14:55:41,054 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1589, cost=$0.000710, time=1975ms
2026-01-30 14:55:41,054 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=229, 尝试次数=1
2026-01-30 14:55:41,054 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"keywords": ["傍晚练武", "傍晚", "练武"], "match_mode": "any", "limit": 100, "work_id": "57b6b0cc-2832-412c-ad2c-1ec0d8ff637d"}
2026-01-30 14:55:41,079 - app.services.chapter_vector_service - INFO - [exact_search] work=57b6b0cc-2832-412c-ad2c-1ec0d8ff637d, keywords=['傍晚练武', '傍晚', '练武']..., mode=any, range=(1, 3), hits=9
2026-01-30 14:55:41,087 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=38 corrected=False final=38
2026-01-30 14:55:41,087 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第38段
2026-01-30 14:55:41,096 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=63 corrected=False final=63
2026-01-30 14:55:41,096 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第63段
2026-01-30 14:55:41,096 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=5 (chapter=5, worldview=0) keywords=傍晚练武,傍晚,练武
2026-01-30 14:55:41,096 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 14:55:41,096 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 14:55:45,904 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 14:55:45,908 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 14:55:45,929 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 14:55:45,932 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2824, cost=$0.001089, time=4815ms
2026-01-30 14:55:45,932 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=237, 尝试次数=1
2026-01-30 14:55:45,932 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"keywords": ["晚饭后", "晚饭", "饭后"], "match_mode": "any", "limit": 50, "work_id": "57b6b0cc-2832-412c-ad2c-1ec0d8ff637d"}
2026-01-30 14:55:45,970 - app.services.chapter_vector_service - INFO - [exact_search] work=57b6b0cc-2832-412c-ad2c-1ec0d8ff637d, keywords=['晚饭后', '晚饭', '饭后']..., mode=any, range=(1, 3), hits=2
2026-01-30 14:55:45,970 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=2 (chapter=2, worldview=0) keywords=晚饭后,晚饭,饭后
2026-01-30 14:55:45,970 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 14:55:45,970 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 14:55:49,156 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 14:55:49,156 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 14:55:49,170 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 14:55:49,171 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2122, cost=$0.000903, time=3186ms
2026-01-30 14:55:49,171 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=257, 尝试次数=1
2026-01-30 14:55:49,171 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"keywords": ["夜里练刀", "夜里", "练刀", "梦境"], "match_mode": "any", "limit": 100, "work_id": "57b6b0cc-2832-412c-ad2c-1ec0d8ff637d"}
2026-01-30 14:55:49,189 - app.services.chapter_vector_service - INFO - [exact_search] work=57b6b0cc-2832-412c-ad2c-1ec0d8ff637d, keywords=['夜里练刀', '夜里', '练刀']..., mode=any, range=(1, 3), hits=2
2026-01-30 14:55:49,196 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=0 corrected=False final=0
2026-01-30 14:55:49,199 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第0段
2026-01-30 14:55:49,204 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=1 corrected=False final=1
2026-01-30 14:55:49,204 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第1段
2026-01-30 14:55:49,204 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=2 (chapter=2, worldview=0) keywords=夜里练刀,夜里,练刀,梦境
2026-01-30 14:55:49,210 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 14:55:49,210 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 14:55:59,018 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 14:55:59,019 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 14:55:59,029 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 14:55:59,029 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=3604, cost=$0.001259, time=9809ms
2026-01-30 14:55:59,029 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=145, 尝试次数=1
2026-01-30 14:55:59,029 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=list_chapters params={"work_id": "57b6b0cc-2832-412c-ad2c-1ec0d8ff637d"}
2026-01-30 14:55:59,029 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=list_chapters success=True count=3
2026-01-30 14:55:59,029 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 14:55:59,029 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 14:56:05,729 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 14:56:05,736 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 14:56:05,746 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 14:56:05,746 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=3173, cost=$0.001172, time=6706ms
2026-01-30 14:56:05,746 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=207, 尝试次数=1
2026-01-30 14:56:05,746 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"keywords": "醒后练功,醒后", "match_mode": "any", "limit": 10, "work_id": "57b6b0cc-2832-412c-ad2c-1ec0d8ff637d"}
2026-01-30 14:56:05,768 - app.services.chapter_vector_service - INFO - [exact_search] work=57b6b0cc-2832-412c-ad2c-1ec0d8ff637d, keywords=['醒后练功', '醒后']..., mode=any, range=(1, 3), hits=0
2026-01-30 14:56:05,775 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=0 (chapter=0, worldview=0) keywords=醒后练功,醒后
2026-01-30 14:56:05,776 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 14:56:05,776 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 14:56:31,437 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 14:56:31,439 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 14:56:31,458 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 14:56:31,459 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=6892, cost=$0.002373, time=25662ms
2026-01-30 14:56:31,459 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=313, 尝试次数=1
2026-01-30 14:56:31,459 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=read_paragraphs params={"items": [{"chapter_order": 1, "paragraph_index": 19}, {"chapter_order": 2, "paragraph_index": 50}], "work_id": "57b6b0cc-2832-412c-ad2c-1ec0d8ff637d"}
2026-01-30 14:56:31,459 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=read_paragraphs success=False count=0 index_base=None
2026-01-30 14:56:31,461 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] read_paragraphs failed details: empty_reason=None error=没有可读取的段落（可能超出范围） invalid_items=None index_base=None
2026-01-30 14:56:31,461 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 14:56:31,462 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 14:56:40,080 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 14:56:40,080 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 14:56:40,096 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 14:56:40,099 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=3184, cost=$0.001329, time=8617ms
2026-01-30 14:56:40,099 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=377, 尝试次数=1
2026-01-30 14:56:40,099 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=read_paragraphs params={"items": [{"chapter_order": 2, "paragraph_index": 50}, {"chapter_order": 1, "paragraph_index": 19}], "context_before": 0, "context_after": 0, "work_id": "57b6b0cc-2832-412c-ad2c-1ec0d8ff637d"}
2026-01-30 14:56:40,099 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=read_paragraphs success=False count=0 index_base=None
2026-01-30 14:56:40,099 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] read_paragraphs failed details: empty_reason=None error=没有可读取的段落（可能超出范围） invalid_items=None index_base=None
2026-01-30 14:56:40,099 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 14:56:40,099 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 14:56:53,978 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 14:56:53,981 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 14:56:54,003 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 14:56:54,006 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4346, cost=$0.001563, time=13882ms
2026-01-30 14:56:54,007 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=244, 尝试次数=1
2026-01-30 14:56:54,008 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=read_paragraphs params={"chapter_order": 2, "offset": 50, "limit": 3, "context_before": 0, "context_after": 0, "work_id": "57b6b0cc-2832-412c-ad2c-1ec0d8ff637d"}
2026-01-30 14:56:54,008 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=read_paragraphs success=False count=3 index_base=None
2026-01-30 14:56:54,008 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] read_paragraphs failed details: empty_reason=None error=该章节读取预算已用尽 invalid_items=None index_base=None
2026-01-30 14:56:54,008 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 14:56:54,010 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 14:57:03,455 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 14:57:03,455 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 14:57:03,470 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 14:57:03,470 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=3451, cost=$0.001315, time=9445ms
2026-01-30 14:57:03,470 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=297, 尝试次数=1
2026-01-30 14:57:03,470 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=read_paragraphs params={"items": [{"chapter_order": 1, "paragraph_index": 19}, {"chapter_order": 2, "paragraph_index": 50}], "work_id": "57b6b0cc-2832-412c-ad2c-1ec0d8ff637d"}
2026-01-30 14:57:03,470 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=read_paragraphs success=False count=0 index_base=None
2026-01-30 14:57:03,470 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] read_paragraphs failed details: empty_reason=None error=没有可读取的段落（可能超出范围） invalid_items=None index_base=None
2026-01-30 14:57:03,470 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 14:57:03,470 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 14:57:11,188 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 14:57:11,188 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 14:57:11,205 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 14:57:11,212 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2993, cost=$0.001127, time=7718ms
2026-01-30 14:57:11,212 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=225, 尝试次数=1
2026-01-30 14:57:11,212 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=read_paragraph params={"chapter_order": 2, "paragraph_index": 50, "context_before": 2, "context_after": 2, "work_id": "57b6b0cc-2832-412c-ad2c-1ec0d8ff637d"}
2026-01-30 14:57:11,215 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=read_paragraph success=False chapter=2 paragraph=50 index_base=None
2026-01-30 14:57:11,216 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 14:57:11,216 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 14:57:26,403 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 14:57:26,405 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 14:57:26,422 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 14:57:26,422 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4663, cost=$0.001645, time=15189ms
2026-01-30 14:57:26,422 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=228, 尝试次数=1
2026-01-30 14:57:26,422 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"keywords": ["醒后", "练功"], "match_mode": "all", "limit": 10, "work_id": "57b6b0cc-2832-412c-ad2c-1ec0d8ff637d"}
2026-01-30 14:57:26,451 - app.services.chapter_vector_service - INFO - [exact_search] work=57b6b0cc-2832-412c-ad2c-1ec0d8ff637d, keywords=['练功']..., mode=all, range=(1, 3), hits=10
2026-01-30 14:57:26,462 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=4 corrected=False final=4
2026-01-30 14:57:26,462 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第4段
2026-01-30 14:57:26,472 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=20 corrected=False final=20
2026-01-30 14:57:26,474 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第20段
2026-01-30 14:57:26,474 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=6 (chapter=6, worldview=0) keywords=练功
2026-01-30 14:57:26,474 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 14:57:26,474 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 14:57:35,796 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 14:57:35,796 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 14:57:35,820 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 14:57:35,825 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4136, cost=$0.001498, time=9321ms
2026-01-30 14:57:35,825 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=242, 尝试次数=1
2026-01-30 14:57:35,825 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"keywords": ["进入镖局"], "match_mode": "any", "limit": 10, "work_id": "57b6b0cc-2832-412c-ad2c-1ec0d8ff637d"}
2026-01-30 14:57:35,841 - app.services.chapter_vector_service - INFO - [exact_search] work=57b6b0cc-2832-412c-ad2c-1ec0d8ff637d, keywords=['进入镖局']..., mode=any, range=(1, 3), hits=1
2026-01-30 14:57:35,842 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=1 (chapter=1, worldview=0) keywords=进入镖局
2026-01-30 14:57:35,843 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 14:57:35,844 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 14:57:43,307 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 14:57:43,311 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 14:57:43,321 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 14:57:43,321 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=3503, cost=$0.001313, time=7468ms
2026-01-30 14:57:43,321 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=257, 尝试次数=1
2026-01-30 14:57:43,328 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"keywords": ["考核前", "临近考核", "将近考核"], "match_mode": "any", "limit": 5, "work_id": "57b6b0cc-2832-412c-ad2c-1ec0d8ff637d"}
2026-01-30 14:57:43,328 - app.services.agent.tools.explore_tools - INFO - [ExploreState] 搜索词与已有词相似，跳过: '考核前' ~ '考核'
2026-01-30 14:57:43,350 - app.services.chapter_vector_service - INFO - [exact_search] work=57b6b0cc-2832-412c-ad2c-1ec0d8ff637d, keywords=['临近考核', '将近考核']..., mode=any, range=(1, 3), hits=0
2026-01-30 14:57:43,351 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=0 (chapter=0, worldview=0) keywords=临近考核,将近考核
2026-01-30 14:57:43,352 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 14:57:43,353 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 14:57:57,147 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 14:57:57,147 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 14:57:57,163 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 14:57:57,168 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4544, cost=$0.001647, time=13793ms
2026-01-30 14:57:57,169 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=284, 尝试次数=1
2026-01-30 14:57:57,170 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=read_paragraphs params={"items": [{"chapter_order": 2, "paragraph_index": 50}], "context_before": 0, "context_after": 1, "work_id": "57b6b0cc-2832-412c-ad2c-1ec0d8ff637d"}
2026-01-30 14:57:57,172 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=read_paragraphs success=False count=0 index_base=None
2026-01-30 14:57:57,172 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] read_paragraphs failed details: empty_reason=None error=没有可读取的段落（可能超出范围） invalid_items=None index_base=None
2026-01-30 14:57:57,172 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 14:57:57,172 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 14:58:04,320 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 14:58:04,320 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 14:58:04,337 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 14:58:04,337 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=3255, cost=$0.001196, time=7148ms
2026-01-30 14:58:04,337 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=219, 尝试次数=1
2026-01-30 14:58:04,337 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=read_paragraph params={"chapter_order": 2, "paragraph_index": 50, "context_before": 1, "context_after": 1, "work_id": "57b6b0cc-2832-412c-ad2c-1ec0d8ff637d"}
2026-01-30 14:58:04,337 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=read_paragraph success=False chapter=2 paragraph=50 index_base=None
2026-01-30 14:58:04,343 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 14:58:04,344 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 14:58:24,838 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 14:58:24,839 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 14:58:24,854 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 14:58:24,857 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=5768, cost=$0.002049, time=20495ms
2026-01-30 14:58:24,857 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=278, 尝试次数=1
2026-01-30 14:58:24,857 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=list_paragraphs params={"chapter_order": 3, "offset": 0, "limit": 20, "preview_len": 50, "work_id": "57b6b0cc-2832-412c-ad2c-1ec0d8ff637d"}
2026-01-30 14:58:24,869 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=list_paragraphs success=True chapter=3 offset=0 limit=20 approximate=None
2026-01-30 14:58:24,871 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 14:58:24,872 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 14:58:33,898 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 14:58:33,903 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 14:58:33,920 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 14:58:33,920 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4151, cost=$0.001476, time=9031ms
2026-01-30 14:58:33,920 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=216, 尝试次数=1
2026-01-30 14:58:33,920 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"keywords": "晚饭后", "match_mode": "any", "limit": 5, "work_id": "57b6b0cc-2832-412c-ad2c-1ec0d8ff637d"}
2026-01-30 14:58:33,945 - app.services.chapter_vector_service - INFO - [exact_search] work=57b6b0cc-2832-412c-ad2c-1ec0d8ff637d, keywords=['晚饭后']..., mode=any, range=(1, 3), hits=1
2026-01-30 14:58:33,948 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=1 (chapter=1, worldview=0) keywords=晚饭后
2026-01-30 14:58:33,948 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 14:58:33,948 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 14:58:47,094 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 14:58:47,095 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 14:58:47,109 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 14:58:47,110 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4647, cost=$0.001568, time=13147ms
2026-01-30 14:58:47,110 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=169, 尝试次数=1
2026-01-30 14:58:47,111 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=read_paragraph params={"chapter_order": 2, "paragraph_index": 56, "work_id": "57b6b0cc-2832-412c-ad2c-1ec0d8ff637d"}
2026-01-30 14:58:47,111 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=read_paragraph success=False chapter=2 paragraph=56 index_base=None
2026-01-30 14:58:47,112 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 14:58:47,114 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 14:58:56,690 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 14:58:56,690 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 14:58:56,711 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 14:58:56,711 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4018, cost=$0.001447, time=9576ms
2026-01-30 14:58:56,711 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=233, 尝试次数=1
2026-01-30 14:58:56,711 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=read_paragraph params={"chapter_order": 2, "paragraph_index": 56, "context_before": 0, "context_after": 0, "work_id": "57b6b0cc-2832-412c-ad2c-1ec0d8ff637d"}
2026-01-30 14:58:56,711 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=read_paragraph success=False chapter=2 paragraph=56 index_base=None
2026-01-30 14:58:56,711 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 14:58:56,711 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 14:59:09,386 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 14:59:09,388 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 14:59:09,403 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 14:59:09,403 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4308, cost=$0.001636, time=12677ms
2026-01-30 14:59:09,403 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=357, 尝试次数=1
2026-01-30 14:59:09,403 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=read_paragraphs params={"items": [{"chapter_order": 3, "paragraph_index": 2}, {"chapter_order": 3, "paragraph_index": 3}], "context_before": 0, "context_after": 0, "work_id": "57b6b0cc-2832-412c-ad2c-1ec0d8ff637d"}
2026-01-30 14:59:09,412 - app.services.agent.langgraph_tools - INFO - [read_paragraphs] start items=2 index_base=zero
2026-01-30 14:59:09,422 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=2 corrected=False final=2
2026-01-30 14:59:09,422 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第2段
2026-01-30 14:59:09,433 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=3 corrected=False final=3
2026-01-30 14:59:09,433 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第3段
2026-01-30 14:59:09,436 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=read_paragraphs success=True count=2 index_base=zero
2026-01-30 14:59:09,437 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 14:59:09,437 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 14:59:19,617 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 14:59:19,619 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 14:59:19,644 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 14:59:19,645 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4648, cost=$0.001555, time=10182ms
2026-01-30 14:59:19,650 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=155, 尝试次数=1
2026-01-30 14:59:19,650 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=read_paragraph params={"chapter_order": 2, "paragraph_index": 56, "work_id": "57b6b0cc-2832-412c-ad2c-1ec0d8ff637d"}
2026-01-30 14:59:19,650 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=read_paragraph success=False chapter=2 paragraph=56 index_base=None
2026-01-30 14:59:19,653 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 14:59:19,653 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 14:59:26,402 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 14:59:26,402 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 14:59:26,420 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 14:59:26,420 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=3447, cost=$0.001324, time=6752ms
2026-01-30 14:59:26,420 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=302, 尝试次数=1
2026-01-30 14:59:26,420 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=read_paragraphs params={"items": [{"chapter_order": 2, "paragraph_index": 56}, {"chapter_order": 2, "paragraph_index": 57}], "work_id": "57b6b0cc-2832-412c-ad2c-1ec0d8ff637d"}
2026-01-30 14:59:26,427 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=read_paragraphs success=False count=0 index_base=None
2026-01-30 14:59:26,428 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] read_paragraphs failed details: empty_reason=None error=没有可读取的段落（可能超出范围） invalid_items=None index_base=None
2026-01-30 14:59:26,428 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 14:59:26,428 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 14:59:32,795 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 14:59:32,796 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 14:59:32,816 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 14:59:32,819 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=3194, cost=$0.001209, time=6368ms
2026-01-30 14:59:32,819 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=242, 尝试次数=1
2026-01-30 14:59:32,819 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=read_paragraph params={"chapter_order": 2, "paragraph_index": 56, "context_before": 0, "context_after": 0, "work_id": "57b6b0cc-2832-412c-ad2c-1ec0d8ff637d"}
2026-01-30 14:59:32,819 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=read_paragraph success=False chapter=2 paragraph=56 index_base=None
2026-01-30 14:59:32,819 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 14:59:32,819 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 14:59:46,665 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 14:59:46,668 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 14:59:46,686 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 14:59:46,688 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4596, cost=$0.001605, time=13849ms
2026-01-30 14:59:46,688 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=159, 尝试次数=1
2026-01-30 14:59:46,688 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 14:59:46,693 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=200, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 14:59:53,275 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 14:59:53,277 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 14:59:53,297 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 14:59:53,300 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2010, cost=$0.000783, time=6584ms
2026-01-30 14:59:53,303 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=107, 尝试次数=1
2026-01-30 14:59:53,305 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 探索完成(工具循环): 28轮, 原因=已收集到足够证据来构建目标时间线中的所有事件：进入镖局、考核前半个月、傍晚练武、晚饭后、夜里练刀/梦境、醒后练功。尽管“考核前半个月”没有精确匹配的段落，但“眼见都要考核了”和“马上要考核了”的证据已足以表示该时间点。
2026-01-30 14:59:53,312 - app.services.agent.execution.tool_executor - INFO - [StandardTool] explore_content 执行成功
2026-01-30 14:59:53,312 - app.api.v1.agent - INFO - [Stream] 任务完成: 在第1至3章中，查找与时间线（进入镖局→考核前半个月→傍晚练武→晚饭后→夜里练刀/梦境→醒后练功）相关的原文证据。 (278.5s)
2026-01-30 14:59:53,312 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务2完成
2026-01-30 14:59:53,319 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共2个任务，耗时: 322.14s
2026-01-30 14:59:53,320 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2026-01-30 14:59:53,320 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=2, 展示型=0
2026-01-30 14:59:53,320 - app.services.agent.langgraph_agent - INFO - [Response] 2个输出任务（含续写），使用AI整合
2026-01-30 14:59:53,321 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2026-01-30 14:59:53,321 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=2, 展示型=0
2026-01-30 14:59:53,322 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=3598字符, 处理后=3700字符
2026-01-30 14:59:53,322 - app.services.agent.planning.response_builder - INFO - [Summarization] 准备发送 summarization_start 事件
2026-01-30 14:59:53,322 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-30 14:59:53,322 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-30 14:59:53,323 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=60, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 14:59:54,828 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 14:59:54,828 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-30 14:59:54,852 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 14:59:54,852 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=415, cost=$0.000049, time=1505ms
2026-01-30 14:59:54,852 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=32, 尝试次数=1
2026-01-30 14:59:54,858 - app.services.agent.planning.response_builder - INFO - [Summarization] reason生成: len=32 content=赵穆在第二章详细讲解了“羚羊献食”的动作要点，复原了其讲解顺序。
2026-01-30 14:59:54,859 - app.services.agent.stream.stream_event_handler - INFO - [StreamEventHandler] emit_summarization_start 被调用, _on_flow_event=True, reason_len=32, reason=赵穆在第二章详细讲解了“羚羊献食”的动作要点，复原了其讲解顺序。
2026-01-30 14:59:54,859 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_start 事件已发送
2026-01-30 14:59:54,859 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2026-01-30 14:59:54,859 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2026-01-30 14:59:54,870 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-30 14:59:54,871 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-30 14:59:54,872 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=20000, temp=0.7, task_type=TaskType.SUMMARIZATION
2026-01-30 15:00:01,926 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-30 15:00:01,928 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_complete 事件已发送（第一个chunk时）
2026-01-30 15:00:01,930 - app.services.agent.planning.response_builder - INFO - [Summarization] output_ready 事件已发送（第一个chunk时）
2026-01-30 15:00:04,813 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 13 个数据块，总长度: 1163
2026-01-30 15:00:04,814 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 8850 (prompt=8031, completion=819)
2026-01-30 15:00:04,814 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 15:00:04,814 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-30 15:00:04,834 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 15:00:04,835 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=8850, cost=$0.004457, time=9942ms
2026-01-30 15:00:04,836 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=1163
2026-01-30 15:00:04,840 - app.services.context.vector_memory_store - INFO - 🔁 跳过重复记忆，复用ID=79913e7e-d5cd-4e09-bce6-ca6639bd8456_1769698570739_ee3e8190
2026-01-30 15:00:04,840 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:57b6b0cc-2832-412c-ad2c-1ec0d8ff637d | 重要度=0.87
2026-01-30 15:00:06,222 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:57b6b0cc-2832-412c-ad2c-1ec0d8ff637d | 重要度=0.60
2026-01-30 15:00:06,232 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:57b6b0cc-2832-412c-ad2c-1ec0d8ff637d:ee47fc57-5bea-4a83-8013-d9134672a763, token=2355
2026-01-30 15:00:06,235 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:57b6b0cc-2832-412c-ad2c-1ec0d8ff637d:ee47fc57-5bea-4a83-8013-d9134672a763, 消息数=4, 摘要长度=0, Token=2355
2026-01-30 15:00:06,236 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:57b6b0cc-2832-412c-ad2c-1ec0d8ff637d:ee47fc57-5bea-4a83-8013-d9134672a763)
2026-01-30 15:00:06,238 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2026-01-30 15:00:06,248 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed
INFO:     127.0.0.1:58606 - "GET /api/v1/agent/operations/ee47fc57-5bea-4a83-8013-d9134672a763 HTTP/1.1" 200 OK
INFO:     127.0.0.1:62703 - "POST /api/v1/auth/refresh HTTP/1.1" 200 OK
2026-01-30 15:02:59,408 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-30 15:02:59,408 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-30 15:02:59,409 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2026-01-30 15:03:01,153 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz:8443/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-30 15:03:01,155 - app.api.v1.agent - INFO - [Chat Stream] Mode: planning
2026-01-30 15:03:01,155 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:51486 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2026-01-30 15:03:01,168 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 仅第1–2章，分析赵穆对段融的态度与原因，并对孔斌/李充/张征的“区别对待”做证据支撑。
  要求：...
2026-01-30 15:03:01,179 - app.api.v1.agent - INFO - [agent_chat_stream] 📚 世界观数据已注入: 人物=11, 地点=8, 设定=6, 规范=无
2026-01-30 15:03:01,182 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:57b6b0cc-2832-412c-ad2c-1ec0d8ff637d:ee47fc57-5bea-4a83-8013-d9134672a763 (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=57b6b0cc-2832-412c-ad2c-1ec0d8ff637d, conversation_id=ee47fc57-5bea-4a83-8013-d9134672a763)
2026-01-30 15:03:01,188 - app.services.context.store - INFO - [ContextStore] 加载上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:57b6b0cc-2832-412c-ad2c-1ec0d8ff637d:ee47fc57-5bea-4a83-8013-d9134672a763, 4条消息
2026-01-30 15:03:01,190 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:57b6b0cc-2832-412c-ad2c-1ec0d8ff637d:ee47fc57-5bea-4a83-8013-d9134672a763: 2355/16000 tokens
2026-01-30 15:03:01,389 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='仅第1–2章，分析赵穆对段融的态度与原因，并对孔斌/李充/张...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:57b6b0cc-2832-412c-ad2c-1ec0d8ff637d', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=2条
2026-01-30 15:03:01,393 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=57b6b0cc-2832-412c-ad2c-1ec0d8ff637d | 含用户级=True | 找到=2条
2026-01-30 15:03:01,426 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 5条消息, 2355 tokens, 耗时 243.73ms
2026-01-30 15:03:01,428 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 5 条历史消息 (token: 2355, has_summary: False)
2026-01-30 15:03:01,428 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-30 15:03:01,428 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-30 15:03:01,428 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=200, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-30 15:03:02,877 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 15:03:02,878 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-30 15:03:02,898 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 15:03:02,898 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1850, cost=$0.000191, time=1451ms
2026-01-30 15:03:02,901 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=42, 尝试次数=1
2026-01-30 15:03:02,903 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-30 15:03:02,904 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-30 15:03:02,904 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=20, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-30 15:03:03,813 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 15:03:03,816 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-30 15:03:03,831 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 15:03:03,837 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=373, cost=$0.000038, time=911ms
2026-01-30 15:03:03,838 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=8, 尝试次数=1
2026-01-30 15:03:03,838 - app.services.agent.intent.classifier - INFO - [Intent] AI识别结果: analysis
2026-01-30 15:03:03,838 - app.services.agent.langgraph_agent - INFO - [Planning] AI意图分类: analysis (置信度: 0.90)
2026-01-30 15:03:03,838 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 仅第1–2章，分析赵穆对段融的态度与原因，并对孔斌/李充/张征的“区别对待”做证据支撑。
  要求：...
2026-01-30 15:03:03,870 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-30 15:03:03,873 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=story_planning, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: story_planning; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-01-30 15:03:03,873 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.3, task_type=TaskType.STORY_PLANNING
2026-01-30 15:03:30,739 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-30 15:03:36,597 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 11 个数据块，总长度: 1150
2026-01-30 15:03:36,598 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 25061 (prompt=24420, completion=641)
2026-01-30 15:03:36,598 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 15:03:36,598 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-30 15:03:36,618 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 15:03:36,620 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=25061, cost=$0.036935, time=32724ms
2026-01-30 15:03:36,620 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=25061
2026-01-30 15:03:36,620 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户需要一份关于角色关系的分析报告。具体来说，报告需要包含两, 原料=为了完成这个分析，我需要获取第1章和第2, 处理=1. 使用 `explore_conte
2026-01-30 15:03:36,620 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共1个任务
2026-01-30 15:03:36,626 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共1个任务，耗时: 32.79s
2026-01-30 15:03:36,626 - app.api.v1.agent - INFO - [Stream] Plan tasks: 1 items
2026-01-30 15:03:36,627 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2026-01-30 15:03:36,627 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2026-01-30 15:03:36,629 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2026-01-30 15:03:36,629 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] DAG 调度启用，任务数=1, 有依赖任务=0
2026-01-30 15:03:36,629 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1开始: 在第1-2章中，查找所有关于赵穆、段融、孔斌、李充、张征之间互动的段落，以分析赵穆的态度和是否存在区别对待。
2026-01-30 15:03:36,629 - app.api.v1.agent - INFO - [Stream] Task started: 在第1-2章中，查找所有关于赵穆、段融、孔斌、李充、张征之间互动的段落，以分析赵穆的态度和是否存在区别对待。 (icon=Wrench)
2026-01-30 15:03:36,629 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: explore_content
2026-01-30 15:03:36,629 - app.services.agent.tools.explore_tools - INFO - [explore_content] 开始: work_id=57b6b0cc-2832-412c-ad2c-1ec0d8ff637d, target=在第1-2章中，分析赵穆对段融的态度与原因，并对孔斌/李充/张征的“区别对待”做证据支撑。
约束：章...
2026-01-30 15:03:36,629 - app.services.agent.tools.explore_tools - INFO - [explore_content] 规划传入关键词: ['赵穆', '段融', '孔斌', '李充', '张征']
2026-01-30 15:03:36,629 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 章节范围锁定: 第1-2章
2026-01-30 15:03:36,629 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 开始探索 V5: work_id=57b6b0cc-2832-412c-ad2c-1ec0d8ff637d, target=在第1-2章中，分析赵穆对段融的态度与原因，并对孔斌/李充/张征的“区别对待”做证据支撑。
约束：章...
2026-01-30 15:03:36,636 - app.services.chapter_service - INFO - [ChapterService] Querying chapters for work_id=57b6b0cc-2832-412c-ad2c-1ec0d8ff637d, type=<class 'uuid.UUID'>
2026-01-30 15:03:36,643 - app.services.chapter_service - INFO - [ChapterService] Found 5 chapters
2026-01-30 15:03:36,643 - app.services.chapter_service - INFO -   - Chapter: 第1章 吞噬, order=1
2026-01-30 15:03:36,643 - app.services.chapter_service - INFO -   - ... (3 more chapters)
2026-01-30 15:03:36,643 - app.services.chapter_service - INFO -   - Chapter: 第5章 太一门, order=5
2026-01-30 15:03:36,660 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 章节范围映射: 第1-2章 -> 第1-2章
2026-01-30 15:03:36,671 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 自动获取世界观...
2026-01-30 15:03:36,687 - app.services.agent.langgraph_tools - INFO - [get_writing_context] ✅ 获取创作上下文成功: include=worldview
2026-01-30 15:03:36,688 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 世界观获取完成: 25 条
2026-01-30 15:03:36,688 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 15:03:36,688 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=80, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 15:03:39,118 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 15:03:39,118 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 15:03:39,138 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 15:03:39,143 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=330, cost=$0.000110, time=2430ms
2026-01-30 15:03:39,144 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=9, 尝试次数=1
2026-01-30 15:03:39,144 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 强制流程步骤: list_chapters
2026-01-30 15:03:39,144 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=list_chapters params={"work_id": "57b6b0cc-2832-412c-ad2c-1ec0d8ff637d"}
2026-01-30 15:03:39,144 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=list_chapters success=True count=2
2026-01-30 15:03:39,144 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 15:03:39,148 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=80, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 15:03:41,654 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 15:03:41,654 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 15:03:41,676 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 15:03:41,680 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=503, cost=$0.000173, time=2509ms
2026-01-30 15:03:41,680 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=15, 尝试次数=1
2026-01-30 15:03:41,680 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 强制流程步骤: list_paragraphs
2026-01-30 15:03:41,682 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=list_paragraphs params={"chapter_order": 1, "offset": 0, "limit": 50, "preview_len": 80, "work_id": "57b6b0cc-2832-412c-ad2c-1ec0d8ff637d"}
2026-01-30 15:03:41,693 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=list_paragraphs success=True chapter=1 offset=0 limit=50 approximate=None
2026-01-30 15:03:41,693 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 15:03:41,693 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 15:03:43,504 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 15:03:43,508 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 15:03:43,526 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 15:03:43,532 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1609, cost=$0.000679, time=1815ms
2026-01-30 15:03:43,532 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=198, 尝试次数=1
2026-01-30 15:03:43,532 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"keywords": "赵穆", "match_mode": "keywords", "limit": 50, "work_id": "57b6b0cc-2832-412c-ad2c-1ec0d8ff637d"}
2026-01-30 15:03:43,532 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 世界观匹配: 1 条
2026-01-30 15:03:43,573 - app.services.chapter_vector_service - INFO - [exact_search] work=57b6b0cc-2832-412c-ad2c-1ec0d8ff637d, keywords=['赵穆']..., mode=any, range=(1, 2), hits=46
2026-01-30 15:03:43,585 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=55 corrected=False final=55
2026-01-30 15:03:43,585 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第55段
2026-01-30 15:03:43,596 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=57 corrected=False final=57
2026-01-30 15:03:43,597 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第57段
2026-01-30 15:03:43,602 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=59 corrected=False final=59
2026-01-30 15:03:43,608 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第59段
2026-01-30 15:03:43,610 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=60 corrected=False final=60
2026-01-30 15:03:43,610 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第60段
2026-01-30 15:03:43,627 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=61 corrected=False final=61
2026-01-30 15:03:43,629 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第61段
2026-01-30 15:03:43,636 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=63 corrected=False final=63
2026-01-30 15:03:43,640 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第63段
2026-01-30 15:03:43,643 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=66 corrected=False final=66
2026-01-30 15:03:43,651 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第66段
2026-01-30 15:03:43,660 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=0 corrected=False final=0
2026-01-30 15:03:43,665 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第0段
2026-01-30 15:03:43,668 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=1 corrected=False final=1
2026-01-30 15:03:43,668 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第1段
2026-01-30 15:03:43,687 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=2 corrected=False final=2
2026-01-30 15:03:43,687 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第2段
2026-01-30 15:03:43,696 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=4 corrected=False final=4
2026-01-30 15:03:43,702 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第4段
2026-01-30 15:03:43,710 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=8 corrected=False final=8
2026-01-30 15:03:43,710 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第8段
2026-01-30 15:03:43,731 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=9 corrected=False final=9
2026-01-30 15:03:43,736 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第9段
2026-01-30 15:03:43,744 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=10 corrected=False final=10
2026-01-30 15:03:43,754 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第10段
2026-01-30 15:03:43,769 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=11 corrected=False final=11
2026-01-30 15:03:43,769 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第11段
2026-01-30 15:03:43,786 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=12 corrected=False final=12
2026-01-30 15:03:43,786 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第12段
2026-01-30 15:03:43,794 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=13 corrected=False final=13
2026-01-30 15:03:43,801 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第13段
2026-01-30 15:03:43,812 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=14 corrected=False final=14
2026-01-30 15:03:43,812 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第14段
2026-01-30 15:03:43,819 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=16 corrected=False final=16
2026-01-30 15:03:43,819 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第16段
2026-01-30 15:03:43,826 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=18 corrected=False final=18
2026-01-30 15:03:43,826 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第18段
2026-01-30 15:03:43,826 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=33 (chapter=32, worldview=1) keywords=赵穆
2026-01-30 15:03:43,826 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 15:03:43,826 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 15:04:02,010 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 15:04:02,012 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 15:04:02,030 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 15:04:02,033 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=8168, cost=$0.002604, time=18185ms
2026-01-30 15:04:02,037 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=115, 尝试次数=1
2026-01-30 15:04:02,037 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 15:04:02,037 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=200, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 15:04:06,921 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 15:04:06,921 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 15:04:06,935 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 15:04:06,942 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1430, cost=$0.000629, time=4883ms
2026-01-30 15:04:06,943 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=126, 尝试次数=1
2026-01-30 15:04:06,943 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 探索完成(工具循环): 3轮, 原因=已收集到所有关于赵穆对段融态度的证据，以及赵穆对孔斌/李充/张征区别对待的证据。所有提及赵穆的段落都已阅读，无需进一步搜索或阅读。
2026-01-30 15:04:06,952 - app.services.agent.execution.tool_executor - INFO - [StandardTool] explore_content 执行成功
2026-01-30 15:04:06,952 - app.api.v1.agent - INFO - [Stream] 任务完成: 在第1-2章中，查找所有关于赵穆、段融、孔斌、李充、张征之间互动的段落，以分析赵穆的态度和是否存在区别对待。 (30.3s)
2026-01-30 15:04:06,952 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1完成
2026-01-30 15:04:06,952 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共1个任务，耗时: 30.32s
2026-01-30 15:04:06,952 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2026-01-30 15:04:06,958 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=1, 展示型=0
2026-01-30 15:04:06,958 - app.services.agent.langgraph_agent - INFO - [Response] 单个输出任务(explore_content)，使用AI整合
2026-01-30 15:04:06,959 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2026-01-30 15:04:06,959 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=1, 展示型=0
2026-01-30 15:04:06,959 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=2166字符, 处理后=2225字符
2026-01-30 15:04:06,963 - app.services.agent.planning.response_builder - INFO - [Summarization] 准备发送 summarization_start 事件
2026-01-30 15:04:06,964 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-30 15:04:06,965 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-30 15:04:06,965 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=60, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 15:04:08,506 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 15:04:08,506 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-30 15:04:08,523 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 15:04:08,526 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=284, cost=$0.000038, time=1540ms
2026-01-30 15:04:08,526 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=36, 尝试次数=1
2026-01-30 15:04:08,526 - app.services.agent.planning.response_builder - INFO - [Summarization] reason生成: len=36 content=赵穆对段融态度温和，对孔斌、李充、张征则区别对待，体现在其言语和行动上。
2026-01-30 15:04:08,526 - app.services.agent.stream.stream_event_handler - INFO - [StreamEventHandler] emit_summarization_start 被调用, _on_flow_event=True, reason_len=36, reason=赵穆对段融态度温和，对孔斌、李充、张征则区别对待，体现在其言语和行动上。
2026-01-30 15:04:08,526 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_start 事件已发送
2026-01-30 15:04:08,526 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2026-01-30 15:04:08,526 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2026-01-30 15:04:08,536 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-30 15:04:08,536 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-30 15:04:08,536 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=20000, temp=0.7, task_type=TaskType.SUMMARIZATION
2026-01-30 15:04:12,852 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-30 15:04:12,852 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_complete 事件已发送（第一个chunk时）
2026-01-30 15:04:12,852 - app.services.agent.planning.response_builder - INFO - [Summarization] output_ready 事件已发送（第一个chunk时）
2026-01-30 15:04:15,834 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 10 个数据块，总长度: 785
2026-01-30 15:04:15,837 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 5572 (prompt=4998, completion=574)
2026-01-30 15:04:15,837 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 15:04:15,837 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-30 15:04:15,857 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 15:04:15,858 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=5572, cost=$0.002934, time=7302ms
2026-01-30 15:04:15,860 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=785
2026-01-30 15:04:15,866 - app.services.context.vector_memory_store - INFO - 🔁 跳过重复记忆，复用ID=79913e7e-d5cd-4e09-bce6-ca6639bd8456_1769698913413_aaa0d9e3
2026-01-30 15:04:15,867 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:57b6b0cc-2832-412c-ad2c-1ec0d8ff637d | 重要度=0.82
2026-01-30 15:04:17,249 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:57b6b0cc-2832-412c-ad2c-1ec0d8ff637d | 重要度=0.67
2026-01-30 15:04:17,260 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:57b6b0cc-2832-412c-ad2c-1ec0d8ff637d:ee47fc57-5bea-4a83-8013-d9134672a763, token=3383
2026-01-30 15:04:17,262 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:57b6b0cc-2832-412c-ad2c-1ec0d8ff637d:ee47fc57-5bea-4a83-8013-d9134672a763, 消息数=6, 摘要长度=0, Token=3383
2026-01-30 15:04:17,263 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:57b6b0cc-2832-412c-ad2c-1ec0d8ff637d:ee47fc57-5bea-4a83-8013-d9134672a763)
2026-01-30 15:04:17,264 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2026-01-30 15:04:17,272 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed
INFO:     127.0.0.1:60728 - "GET /api/v1/agent/operations/ee47fc57-5bea-4a83-8013-d9134672a763 HTTP/1.1" 200 OK
2026-01-30 15:08:56,365 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-30 15:08:56,366 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-30 15:08:56,366 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2026-01-30 15:08:57,971 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz:8443/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-30 15:08:57,974 - app.api.v1.agent - INFO - [Chat Stream] Mode: planning
2026-01-30 15:08:57,977 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:53012 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2026-01-30 15:08:57,988 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 限定第2–3章，梳理因果链：
  “脑子被塞进一团东西”→“梦中悟刀”→“醒后练刀”→“身体限制”→...
2026-01-30 15:08:57,999 - app.api.v1.agent - INFO - [agent_chat_stream] 📚 世界观数据已注入: 人物=11, 地点=8, 设定=6, 规范=无
2026-01-30 15:08:58,000 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:57b6b0cc-2832-412c-ad2c-1ec0d8ff637d:ee47fc57-5bea-4a83-8013-d9134672a763 (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=57b6b0cc-2832-412c-ad2c-1ec0d8ff637d, conversation_id=ee47fc57-5bea-4a83-8013-d9134672a763)
2026-01-30 15:08:58,005 - app.services.context.store - INFO - [ContextStore] 加载上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:57b6b0cc-2832-412c-ad2c-1ec0d8ff637d:ee47fc57-5bea-4a83-8013-d9134672a763, 6条消息
2026-01-30 15:08:58,008 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:57b6b0cc-2832-412c-ad2c-1ec0d8ff637d:ee47fc57-5bea-4a83-8013-d9134672a763: 3383/16000 tokens
2026-01-30 15:08:58,202 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='限定第2–3章，梳理因果链：
  “脑子被塞进一团东西”→“...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:57b6b0cc-2832-412c-ad2c-1ec0d8ff637d', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=3条
2026-01-30 15:08:58,202 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=57b6b0cc-2832-412c-ad2c-1ec0d8ff637d | 含用户级=True | 找到=3条
2026-01-30 15:08:58,310 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 7条消息, 3383 tokens, 耗时 308.45ms
2026-01-30 15:08:58,310 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 7 条历史消息 (token: 3383, has_summary: False)
2026-01-30 15:08:58,311 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-30 15:08:58,311 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-30 15:08:58,311 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=200, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-30 15:09:00,038 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 15:09:00,040 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-30 15:09:00,050 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 15:09:00,055 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1893, cost=$0.000195, time=1728ms
2026-01-30 15:09:00,055 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=42, 尝试次数=1
2026-01-30 15:09:00,055 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-30 15:09:00,055 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-30 15:09:00,055 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=20, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-30 15:09:01,640 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 15:09:01,640 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-30 15:09:01,651 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 15:09:01,651 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=390, cost=$0.000039, time=1585ms
2026-01-30 15:09:01,651 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=8, 尝试次数=1
2026-01-30 15:09:01,651 - app.services.agent.intent.classifier - INFO - [Intent] AI识别结果: analysis
2026-01-30 15:09:01,651 - app.services.agent.langgraph_agent - INFO - [Planning] AI意图分类: analysis (置信度: 0.90)
2026-01-30 15:09:01,651 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 限定第2–3章，梳理因果链：
  “脑子被塞进一团东西”→“梦中悟刀”→“醒后练刀”→“身体限制”→...
2026-01-30 15:09:01,663 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-30 15:09:01,664 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=story_planning, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: story_planning; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-01-30 15:09:01,664 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.3, task_type=TaskType.STORY_PLANNING
2026-01-30 15:09:13,683 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-30 15:09:17,745 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 9 个数据块，总长度: 954
2026-01-30 15:09:17,745 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 24341 (prompt=23835, completion=506)
2026-01-30 15:09:17,745 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 15:09:17,745 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-30 15:09:17,760 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 15:09:17,760 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=24341, cost=$0.034854, time=16080ms
2026-01-30 15:09:17,760 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=24341
2026-01-30 15:09:17,760 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户想要梳理一个跨越第2章和第3章的特定因果链，并要求为链条, 原料=需要从第2章和第3章中，根据因果链的五个, 处理=使用 explore_content 工
2026-01-30 15:09:17,760 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共1个任务
2026-01-30 15:09:17,760 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共1个任务，耗时: 16.11s
2026-01-30 15:09:17,760 - app.api.v1.agent - INFO - [Stream] Plan tasks: 1 items
2026-01-30 15:09:17,760 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2026-01-30 15:09:17,760 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2026-01-30 15:09:17,760 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2026-01-30 15:09:17,770 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] DAG 调度启用，任务数=1, 有依赖任务=0
2026-01-30 15:09:17,770 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1开始: 在第2-3章中，为因果链“脑子被塞进一团东西→梦中悟刀→醒后练刀→身体限制→改用站桩尝试内息”的每一步寻找原文证据。
2026-01-30 15:09:17,770 - app.api.v1.agent - INFO - [Stream] Task started: 在第2-3章中，为因果链“脑子被塞进一团东西→梦中悟刀→醒后练刀→身体限制→改用站桩尝试内息”的每一步寻找原文证据。 (icon=Wrench)
2026-01-30 15:09:17,770 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: explore_content
2026-01-30 15:09:17,770 - app.services.agent.tools.explore_tools - INFO - [explore_content] 开始: work_id=57b6b0cc-2832-412c-ad2c-1ec0d8ff637d, target=限定第2-3章，梳理因果链：“脑子被塞进一团东西”→“梦中悟刀”→“醒后练刀”→“身体限制”→“改用...
2026-01-30 15:09:17,770 - app.services.agent.tools.explore_tools - INFO - [explore_content] 规划传入关键词: ['塞进', '脑子', '梦境', '练刀', '醒后', '身体', '酸疼', '站桩', '内息']
2026-01-30 15:09:17,773 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 启用严格段落号模式
2026-01-30 15:09:17,773 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 章节范围锁定: 第2-3章
2026-01-30 15:09:17,773 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 任务禁止整章阅读
2026-01-30 15:09:17,773 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 开始探索 V5: work_id=57b6b0cc-2832-412c-ad2c-1ec0d8ff637d, target=限定第2-3章，梳理因果链：“脑子被塞进一团东西”→“梦中悟刀”→“醒后练刀”→“身体限制”→“改用...
2026-01-30 15:09:17,773 - app.services.chapter_service - INFO - [ChapterService] Querying chapters for work_id=57b6b0cc-2832-412c-ad2c-1ec0d8ff637d, type=<class 'uuid.UUID'>
2026-01-30 15:09:17,780 - app.services.chapter_service - INFO - [ChapterService] Found 5 chapters
2026-01-30 15:09:17,780 - app.services.chapter_service - INFO -   - Chapter: 第1章 吞噬, order=1
2026-01-30 15:09:17,780 - app.services.chapter_service - INFO -   - ... (3 more chapters)
2026-01-30 15:09:17,780 - app.services.chapter_service - INFO -   - Chapter: 第5章 太一门, order=5
2026-01-30 15:09:17,783 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 章节范围映射: 第2-3章 -> 第2-3章
2026-01-30 15:09:17,788 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 自动获取世界观...
2026-01-30 15:09:17,793 - app.services.agent.langgraph_tools - INFO - [get_writing_context] ✅ 获取创作上下文成功: include=worldview
2026-01-30 15:09:17,793 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 世界观获取完成: 25 条
2026-01-30 15:09:17,793 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 15:09:17,793 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=80, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 15:09:22,097 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 15:09:22,097 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 15:09:22,111 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 15:09:22,111 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=734, cost=$0.000240, time=4304ms
2026-01-30 15:09:22,111 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=12, 尝试次数=1
2026-01-30 15:09:22,111 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 强制流程步骤: list_chapters
2026-01-30 15:09:22,111 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=list_chapters params={"work_id": "57b6b0cc-2832-412c-ad2c-1ec0d8ff637d"}
2026-01-30 15:09:22,111 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=list_chapters success=True count=2
2026-01-30 15:09:22,111 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 15:09:22,119 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=80, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 15:09:23,707 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 15:09:23,707 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 15:09:23,722 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 15:09:23,722 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=313, cost=$0.000120, time=1588ms
2026-01-30 15:09:23,722 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=20, 尝试次数=1
2026-01-30 15:09:23,722 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 强制流程步骤: list_paragraphs
2026-01-30 15:09:23,726 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=list_paragraphs params={"chapter_order": 2, "offset": 0, "limit": 50, "preview_len": 80, "work_id": "57b6b0cc-2832-412c-ad2c-1ec0d8ff637d"}
2026-01-30 15:09:23,739 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=list_paragraphs success=True chapter=2 offset=0 limit=50 approximate=None
2026-01-30 15:09:23,739 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 15:09:23,739 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 15:09:25,748 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 15:09:25,750 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 15:09:25,760 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 15:09:25,764 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1596, cost=$0.000725, time=2010ms
2026-01-30 15:09:25,764 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=236, 尝试次数=1
2026-01-30 15:09:25,766 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"keywords": "脑子被塞进一团东西", "match_mode": "keywords", "limit": 10, "chapter_order": 2, "work_id": "57b6b0cc-2832-412c-ad2c-1ec0d8ff637d"}
2026-01-30 15:09:25,778 - app.services.chapter_vector_service - INFO - [exact_search] work=57b6b0cc-2832-412c-ad2c-1ec0d8ff637d, keywords=['脑子被塞进一团东西']..., mode=any, range=(2, 2), hits=0
2026-01-30 15:09:25,778 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=0 (chapter=0, worldview=0) keywords=脑子被塞进一团东西
2026-01-30 15:09:25,778 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 15:09:25,783 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 15:09:31,751 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 15:09:31,751 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 15:09:31,761 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 15:09:31,761 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1743, cost=$0.000639, time=5972ms
2026-01-30 15:09:31,761 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=115, 尝试次数=1
2026-01-30 15:09:31,761 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=list_chapters params={"work_id": "57b6b0cc-2832-412c-ad2c-1ec0d8ff637d"}
2026-01-30 15:09:31,761 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=list_chapters success=True count=2
2026-01-30 15:09:31,761 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 15:09:31,761 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 15:09:35,511 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 15:09:35,513 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 15:09:35,520 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 15:09:35,524 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1591, cost=$0.000682, time=3751ms
2026-01-30 15:09:35,524 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=199, 尝试次数=1
2026-01-30 15:09:35,524 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"keywords": "梦中悟刀", "match_mode": "all", "limit": 100, "work_id": "57b6b0cc-2832-412c-ad2c-1ec0d8ff637d"}
2026-01-30 15:09:35,528 - app.services.chapter_vector_service - INFO - [exact_search] work=57b6b0cc-2832-412c-ad2c-1ec0d8ff637d, keywords=['梦中悟刀']..., mode=all, range=(2, 3), hits=0
2026-01-30 15:09:35,528 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=0 (chapter=0, worldview=0) keywords=梦中悟刀
2026-01-30 15:09:35,528 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 15:09:35,528 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 15:09:37,505 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 15:09:37,505 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 15:09:37,513 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 15:09:37,513 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1051, cost=$0.000531, time=1976ms
2026-01-30 15:09:37,513 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=214, 尝试次数=1
2026-01-30 15:09:37,513 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"keywords": ["醒后练刀"], "match_mode": "all", "limit": 10, "work_id": "57b6b0cc-2832-412c-ad2c-1ec0d8ff637d"}
2026-01-30 15:09:37,521 - app.services.chapter_vector_service - INFO - [exact_search] work=57b6b0cc-2832-412c-ad2c-1ec0d8ff637d, keywords=['醒后练刀']..., mode=all, range=(2, 3), hits=0
2026-01-30 15:09:37,524 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=0 (chapter=0, worldview=0) keywords=醒后练刀
2026-01-30 15:09:37,524 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 15:09:37,524 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 15:09:40,235 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 15:09:40,236 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 15:09:40,242 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 15:09:40,242 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1177, cost=$0.000628, time=2711ms
2026-01-30 15:09:40,247 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=274, 尝试次数=1
2026-01-30 15:09:40,247 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"keywords": ["身体限制"], "match_mode": "all", "limit": 100, "chapter_orders": [2, 3], "work_id": "57b6b0cc-2832-412c-ad2c-1ec0d8ff637d"}
2026-01-30 15:09:40,248 - app.services.chapter_vector_service - INFO - [exact_search] work=57b6b0cc-2832-412c-ad2c-1ec0d8ff637d, keywords=['身体限制']..., mode=all, range=(2, 3), hits=0
2026-01-30 15:09:40,248 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=0 (chapter=0, worldview=0) keywords=身体限制
2026-01-30 15:09:40,248 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 15:09:40,248 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 15:09:57,018 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 15:09:57,021 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 15:09:57,041 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 15:09:57,043 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=3539, cost=$0.001381, time=16773ms
2026-01-30 15:09:57,047 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=286, 尝试次数=1
2026-01-30 15:09:57,047 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=list_paragraphs params={"chapter_order": 2, "offset": 0, "limit": 13, "preview_len": 100, "work_id": "57b6b0cc-2832-412c-ad2c-1ec0d8ff637d"}
2026-01-30 15:09:57,062 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=list_paragraphs success=True chapter=2 offset=0 limit=13 approximate=None
2026-01-30 15:09:57,062 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 15:09:57,066 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 15:09:59,399 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 15:09:59,400 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 15:09:59,417 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 15:09:59,417 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1722, cost=$0.000697, time=2333ms
2026-01-30 15:09:59,417 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=193, 尝试次数=1
2026-01-30 15:09:59,417 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"keywords": "身体限制", "match_mode": "keywords", "limit": 10, "work_id": "57b6b0cc-2832-412c-ad2c-1ec0d8ff637d"}
2026-01-30 15:09:59,425 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 拦截搜索: 关键词'身体限制'在第2-3章范围内已搜索过，0命中
2026-01-30 15:09:59,426 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs blocked=True keywords=身体限制
2026-01-30 15:09:59,426 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 15:09:59,426 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 15:10:05,895 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 15:10:05,897 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 15:10:05,913 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 15:10:05,916 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1889, cost=$0.000837, time=6471ms
2026-01-30 15:10:05,917 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=258, 尝试次数=1
2026-01-30 15:10:05,917 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=read_paragraphs params={"chapter_order": 2, "offset": 0, "limit": 13, "context_before": 0, "context_after": 0, "work_id": "57b6b0cc-2832-412c-ad2c-1ec0d8ff637d"}
2026-01-30 15:10:05,935 - app.services.agent.langgraph_tools - INFO - [read_paragraphs] start items=13 index_base=zero
2026-01-30 15:10:05,946 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=1 corrected=False final=1
2026-01-30 15:10:05,949 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第1段
2026-01-30 15:10:05,961 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=2 corrected=False final=2
2026-01-30 15:10:05,963 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第2段
2026-01-30 15:10:05,975 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=3 corrected=False final=3
2026-01-30 15:10:05,975 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第3段
2026-01-30 15:10:05,991 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=4 corrected=False final=4
2026-01-30 15:10:05,992 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第4段
2026-01-30 15:10:06,008 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=5 corrected=False final=5
2026-01-30 15:10:06,009 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第5段
2026-01-30 15:10:06,017 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=6 corrected=False final=6
2026-01-30 15:10:06,019 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第6段
2026-01-30 15:10:06,025 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=7 corrected=False final=7
2026-01-30 15:10:06,025 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第7段
2026-01-30 15:10:06,033 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=8 corrected=False final=8
2026-01-30 15:10:06,033 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第8段
2026-01-30 15:10:06,044 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=9 corrected=False final=9
2026-01-30 15:10:06,050 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第9段
2026-01-30 15:10:06,058 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=10 corrected=False final=10
2026-01-30 15:10:06,058 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第10段
2026-01-30 15:10:06,068 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=11 corrected=False final=11
2026-01-30 15:10:06,068 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第11段
2026-01-30 15:10:06,075 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=12 corrected=False final=12
2026-01-30 15:10:06,075 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第12段
2026-01-30 15:10:06,078 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=read_paragraphs success=True count=13 index_base=None
2026-01-30 15:10:06,078 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 15:10:06,078 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 15:10:08,733 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 15:10:08,735 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 15:10:08,750 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 15:10:08,758 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2325, cost=$0.000935, time=2657ms
2026-01-30 15:10:08,758 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=206, 尝试次数=1
2026-01-30 15:10:08,758 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=read_paragraphs params={"chapter_order": 2, "offset": 12, "limit": 10, "work_id": "57b6b0cc-2832-412c-ad2c-1ec0d8ff637d"}
2026-01-30 15:10:08,775 - app.services.agent.langgraph_tools - INFO - [read_paragraphs] start items=1 index_base=zero
2026-01-30 15:10:08,786 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=12 corrected=False final=12
2026-01-30 15:10:08,788 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第12段
2026-01-30 15:10:08,789 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=read_paragraphs success=True count=1 index_base=None
2026-01-30 15:10:08,792 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 15:10:08,792 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 15:10:15,012 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 15:10:15,014 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 15:10:15,028 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 15:10:15,031 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2963, cost=$0.001118, time=6223ms
2026-01-30 15:10:15,031 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=203, 尝试次数=1
2026-01-30 15:10:15,031 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=read_paragraphs params={"chapter_order": 2, "offset": 13, "limit": 10, "work_id": "57b6b0cc-2832-412c-ad2c-1ec0d8ff637d"}
2026-01-30 15:10:15,044 - app.services.agent.langgraph_tools - INFO - [read_paragraphs] start items=1 index_base=zero
2026-01-30 15:10:15,052 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=13 corrected=False final=13
2026-01-30 15:10:15,053 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第13段
2026-01-30 15:10:15,054 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=read_paragraphs success=True count=1 index_base=None
2026-01-30 15:10:15,056 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 15:10:15,056 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 15:10:17,317 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 15:10:17,317 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 15:10:17,339 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 15:10:17,341 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2295, cost=$0.000933, time=2261ms
2026-01-30 15:10:17,341 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=220, 尝试次数=1
2026-01-30 15:10:17,343 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=list_paragraphs params={"chapter_order": 3, "offset": 0, "limit": 10, "preview_len": 50, "work_id": "57b6b0cc-2832-412c-ad2c-1ec0d8ff637d"}
2026-01-30 15:10:17,353 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=list_paragraphs success=True chapter=3 offset=0 limit=10 approximate=None
2026-01-30 15:10:17,353 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 15:10:17,353 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 15:10:22,184 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 15:10:22,191 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 15:10:22,212 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 15:10:22,212 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2921, cost=$0.001112, time=4838ms
2026-01-30 15:10:22,212 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=199, 尝试次数=1
2026-01-30 15:10:22,217 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=read_paragraphs params={"chapter_order": 3, "offset": 0, "limit": 8, "work_id": "57b6b0cc-2832-412c-ad2c-1ec0d8ff637d"}
2026-01-30 15:10:22,225 - app.services.agent.langgraph_tools - INFO - [read_paragraphs] start items=8 index_base=zero
2026-01-30 15:10:22,244 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=1 corrected=False final=1
2026-01-30 15:10:22,245 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第1段
2026-01-30 15:10:22,257 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=2 corrected=False final=2
2026-01-30 15:10:22,258 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第2段
2026-01-30 15:10:22,274 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=3 corrected=False final=3
2026-01-30 15:10:22,276 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第3段
2026-01-30 15:10:22,284 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=4 corrected=False final=4
2026-01-30 15:10:22,287 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第4段
2026-01-30 15:10:22,295 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=5 corrected=False final=5
2026-01-30 15:10:22,295 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第5段
2026-01-30 15:10:22,307 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=6 corrected=False final=6
2026-01-30 15:10:22,308 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第6段
2026-01-30 15:10:22,316 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=7 corrected=False final=7
2026-01-30 15:10:22,320 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第7段
2026-01-30 15:10:22,325 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=read_paragraphs success=True count=8 index_base=None
2026-01-30 15:10:22,326 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 15:10:22,328 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 15:10:28,905 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 15:10:28,906 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 15:10:28,926 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 15:10:28,928 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=3434, cost=$0.001285, time=6577ms
2026-01-30 15:10:28,928 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=213, 尝试次数=1
2026-01-30 15:10:28,928 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=read_paragraphs params={"chapter_order": 3, "offset": 7, "limit": 10, "work_id": "57b6b0cc-2832-412c-ad2c-1ec0d8ff637d"}
2026-01-30 15:10:28,950 - app.services.agent.langgraph_tools - INFO - [read_paragraphs] start items=6 index_base=zero
2026-01-30 15:10:28,959 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=7 corrected=False final=7
2026-01-30 15:10:28,963 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第7段
2026-01-30 15:10:28,975 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=8 corrected=False final=8
2026-01-30 15:10:28,976 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第8段
2026-01-30 15:10:28,983 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=9 corrected=False final=9
2026-01-30 15:10:28,990 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第9段
2026-01-30 15:10:29,001 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=10 corrected=False final=10
2026-01-30 15:10:29,001 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第10段
2026-01-30 15:10:29,008 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=11 corrected=False final=11
2026-01-30 15:10:29,011 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第11段
2026-01-30 15:10:29,017 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=12 corrected=False final=12
2026-01-30 15:10:29,017 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第12段
2026-01-30 15:10:29,022 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=read_paragraphs success=True count=6 index_base=None
2026-01-30 15:10:29,024 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 15:10:29,025 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 15:10:32,241 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 15:10:32,241 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 15:10:32,261 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 15:10:32,261 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2927, cost=$0.001107, time=3217ms
2026-01-30 15:10:32,261 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=224, 尝试次数=1
2026-01-30 15:10:32,261 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=read_paragraph params={"chapter_order": 3, "paragraph_index": 12, "context_before": 0, "context_after": 0, "work_id": "57b6b0cc-2832-412c-ad2c-1ec0d8ff637d"}
2026-01-30 15:10:32,261 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=read_paragraph success=True chapter=3 paragraph=12 index_base=None
2026-01-30 15:10:32,267 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 15:10:32,269 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 15:10:43,122 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 15:10:43,124 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 15:10:43,143 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 15:10:43,147 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=3740, cost=$0.001333, time=10857ms
2026-01-30 15:10:43,147 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=192, 尝试次数=1
2026-01-30 15:10:43,149 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=read_paragraph params={"chapter_order": 3, "paragraph_index": 13, "work_id": "57b6b0cc-2832-412c-ad2c-1ec0d8ff637d"}
2026-01-30 15:10:43,158 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=13 corrected=False final=13
2026-01-30 15:10:43,158 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第13段
2026-01-30 15:10:43,159 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=read_paragraph success=True chapter=3 paragraph=13 index_base=zero
2026-01-30 15:10:43,159 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 15:10:43,159 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 15:10:54,625 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 15:10:54,627 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 15:10:54,641 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 15:10:54,642 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4625, cost=$0.001652, time=11467ms
2026-01-30 15:10:54,642 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=229, 尝试次数=1
2026-01-30 15:10:54,642 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=list_paragraphs params={"chapter_order": 3, "offset": 15, "limit": 10, "preview_len": 100, "work_id": "57b6b0cc-2832-412c-ad2c-1ec0d8ff637d"}
2026-01-30 15:10:54,655 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=list_paragraphs success=True chapter=3 offset=15 limit=10 approximate=None
2026-01-30 15:10:54,655 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 15:10:54,655 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 15:11:13,452 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 15:11:13,452 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 15:11:13,469 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 15:11:13,469 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=6785, cost=$0.005333, time=18800ms
2026-01-30 15:11:13,474 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=3222, 尝试次数=1
2026-01-30 15:11:13,476 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 15:11:13,476 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=200, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 15:11:18,475 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 15:11:18,483 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 15:11:18,499 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 15:11:18,501 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1491, cost=$0.000562, time=5007ms
2026-01-30 15:11:18,501 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=74, 尝试次数=1
2026-01-30 15:11:18,504 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 探索完成(工具循环): 18轮, 原因=已在第2-3章内找到所有因果链环节的原文证据，任务完成。
2026-01-30 15:11:18,515 - app.services.agent.execution.tool_executor - INFO - [StandardTool] explore_content 执行成功
2026-01-30 15:11:18,516 - app.api.v1.agent - INFO - [Stream] 任务完成: 在第2-3章中，为因果链“脑子被塞进一团东西→梦中悟刀→醒后练刀→身体限制→改用站桩尝试内息”的每一步寻找原文证据。 (120.7s)
2026-01-30 15:11:18,516 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1完成
2026-01-30 15:11:18,516 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共1个任务，耗时: 120.76s
2026-01-30 15:11:18,516 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2026-01-30 15:11:18,516 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=1, 展示型=0
2026-01-30 15:11:18,516 - app.services.agent.langgraph_agent - INFO - [Response] 单个输出任务(explore_content)，使用AI整合
2026-01-30 15:11:18,516 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2026-01-30 15:11:18,524 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=1, 展示型=0
2026-01-30 15:11:18,527 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=2072字符, 处理后=2135字符
2026-01-30 15:11:18,527 - app.services.agent.planning.response_builder - INFO - [Summarization] 准备发送 summarization_start 事件
2026-01-30 15:11:18,527 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-30 15:11:18,527 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-30 15:11:18,527 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=60, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 15:11:20,107 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 15:11:20,107 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-30 15:11:20,125 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 15:11:20,128 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=331, cost=$0.000049, time=1580ms
2026-01-30 15:11:20,128 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=61, 尝试次数=1
2026-01-30 15:11:20,128 - app.services.agent.planning.response_builder - INFO - [Summarization] reason生成: len=61 content=因果链梳理完成，第2章“脑子被塞进一团东西”引出“梦中悟刀”，第3章“醒后练刀”遇“身体限制”，最终“改用站桩尝试内息”。
2026-01-30 15:11:20,128 - app.services.agent.stream.stream_event_handler - INFO - [StreamEventHandler] emit_summarization_start 被调用, _on_flow_event=True, reason_len=61, reason=因果链梳理完成，第2章“脑子被塞进一团东西”引出“梦中悟刀”，第3章“醒后练刀”遇“身体限制”，最终“改用站桩尝试内息”。
2026-01-30 15:11:20,128 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_start 事件已发送
2026-01-30 15:11:20,128 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2026-01-30 15:11:20,135 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2026-01-30 15:11:20,146 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-30 15:11:20,146 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-30 15:11:20,150 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=20000, temp=0.7, task_type=TaskType.SUMMARIZATION
2026-01-30 15:11:49,062 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-30 15:11:49,073 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_complete 事件已发送（第一个chunk时）
2026-01-30 15:11:49,075 - app.services.agent.planning.response_builder - INFO - [Summarization] output_ready 事件已发送（第一个chunk时）
2026-01-30 15:11:51,684 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 13 个数据块，总长度: 1072
2026-01-30 15:11:51,685 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 10771 (prompt=9950, completion=821)
2026-01-30 15:11:51,687 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 15:11:51,688 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-30 15:11:51,706 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 15:11:51,708 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=10771, cost=$0.005038, time=31536ms
2026-01-30 15:11:51,710 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=1072
2026-01-30 15:11:51,715 - app.services.context.vector_memory_store - INFO - 🔁 跳过重复记忆，复用ID=79913e7e-d5cd-4e09-bce6-ca6639bd8456_1769699172336_fc1f7e1d
2026-01-30 15:11:51,716 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:57b6b0cc-2832-412c-ad2c-1ec0d8ff637d | 重要度=0.87
2026-01-30 15:11:53,158 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:57b6b0cc-2832-412c-ad2c-1ec0d8ff637d | 重要度=0.73
2026-01-30 15:11:53,169 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:57b6b0cc-2832-412c-ad2c-1ec0d8ff637d:ee47fc57-5bea-4a83-8013-d9134672a763, token=4711
2026-01-30 15:11:53,174 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:57b6b0cc-2832-412c-ad2c-1ec0d8ff637d:ee47fc57-5bea-4a83-8013-d9134672a763, 消息数=8, 摘要长度=0, Token=4711
2026-01-30 15:11:53,174 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:57b6b0cc-2832-412c-ad2c-1ec0d8ff637d:ee47fc57-5bea-4a83-8013-d9134672a763)
2026-01-30 15:11:53,175 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2026-01-30 15:11:53,183 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed
INFO:     127.0.0.1:58982 - "GET /api/v1/agent/operations/ee47fc57-5bea-4a83-8013-d9134672a763 HTTP/1.1" 200 OK