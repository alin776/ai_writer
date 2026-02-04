INFO:     127.0.0.1:57583 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
INFO:     127.0.0.1:57584 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
INFO:     127.0.0.1:57595 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
INFO:     127.0.0.1:56174 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
INFO:     ('127.0.0.1', 52534) - "WebSocket /api/v1/ws/notifications/79913e7e-d5cd-4e09-bce6-ca6639bd8456" [accepted]
2026-02-04 10:11:26,001 - app.api.v1.ws - INFO - [WebSocket] 通知连接建立: user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
INFO:     connection open
2026-02-04 10:11:42,287 - app.api.v1.import_routes - INFO - 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456 预览导入文件: 人在诸天，摆烂成帝.txt, 格式: txt
2026-02-04 10:11:42,329 - app.api.v1.import_routes - INFO - 预览成功: 作品=人在诸天，摆烂成帝, 章节数=100
INFO:     127.0.0.1:61748 - "POST /api/v1/works/import/preview HTTP/1.1" 200 OK
2026-02-04 10:11:50,399 - app.api.v1.import_routes - INFO - 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456 导入文件: 人在诸天，摆烂成帝.txt, 格式: txt
2026-02-04 10:11:50,399 - app.api.v1.import_routes - INFO - [导入参数] auto_extract_worldview=True, scan_mode=incremental, format=txt, background_tasks=True
2026-02-04 10:11:50,399 - app.services.import_service - INFO - 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456 开始导入文本数据
2026-02-04 10:11:51,726 - app.core.redis - INFO - ✅ Redis connected: redis://localhost:6379/0
2026-02-04 10:11:51,732 - app.services.import_service - INFO - 文本导入完成: 作品ID=26cfcf99-9e77-4686-b21d-b82d1881e56d, 章节=100
2026-02-04 10:11:51,735 - app.api.v1.import_routes - INFO - [世界观提取] 已为作品 26cfcf99-9e77-4686-b21d-b82d1881e56d 排队世界观提取任务
2026-02-04 10:11:51,736 - app.api.v1.import_routes - INFO - 导入成功: 作品ID=26cfcf99-9e77-4686-b21d-b82d1881e56d, 章节=100, 人物=0
2026-02-04 10:11:51,739 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/works/import
INFO:     127.0.0.1:53518 - "POST /api/v1/works/import HTTP/1.1" 200 OK
INFO:     127.0.0.1:59640 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:53393 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
INFO:     127.0.0.1:59486 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:62745 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:61270 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
2026-02-04 10:12:15,323 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress
INFO:     127.0.0.1:50567 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:58818 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
2026-02-04 10:12:24,580 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress
INFO:     127.0.0.1:61714 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:57775 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:58682 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:59959 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:56266 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:55734 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:51851 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:61135 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:65023 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:63691 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:65291 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:50183 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:62362 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:53907 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:59017 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:60932 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:52601 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:60431 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:61687 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:60406 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:54859 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:63814 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:55701 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:59605 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:65136 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:59283 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
2026-02-04 10:14:11,216 - app.api.v1.import_routes - INFO - [世界观提取] 开始为作品 26cfcf99-9e77-4686-b21d-b82d1881e56d 提取世界观
2026-02-04 10:14:13,372 - app.services.ai.prompts - INFO - Prompts loaded successfully from D:\Java\ai_writer\backend\app\services\ai\prompts\default.json
2026-02-04 10:14:13,372 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-02-04 10:14:13,381 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-02-04 10:14:13,381 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2026-02-04 10:14:14,008 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz:8443/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-02-04 10:14:14,008 - app.services.worldview_sync_service - INFO - [世界观同步] AI服务初始化完成: api_key=***KFzr, base_url=https://204992.xyz:8443/v1, model=gemini-2.5-pro
2026-02-04 10:14:14,019 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 未传递task_type，使用默认模型: gemini-2.5-pro
INFO:     127.0.0.1:54630 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:60039 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:58760 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:62130 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:57596 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:55276 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:50951 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:58765 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:51315 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:58847 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:58098 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:63682 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:61362 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:64513 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:60386 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:56550 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:59782 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:60351 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:50418 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:52888 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:50237 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:64083 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:50482 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:51583 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
2026-02-04 10:15:25,319 - app.services.worldview_sync_service - INFO - [世界观同步] 解析结果: 新人物=9, 新地点=7, 新设定=7
2026-02-04 10:15:25,323 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-02-04 10:15:25,323 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-02-04 10:15:25,323 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2026-02-04 10:15:25,769 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz:8443/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-02-04 10:15:25,772 - app.services.worldview_sync_service - INFO - [世界观同步] AI服务初始化完成: api_key=***KFzr, base_url=https://204992.xyz:8443/v1, model=gemini-2.5-pro
2026-02-04 10:15:25,775 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 未传递task_type，使用默认模型: gemini-2.5-pro
INFO:     127.0.0.1:57740 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:50767 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:49990 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:56898 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:64667 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:53742 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:59075 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:50951 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:64137 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:54972 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:51474 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:56330 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:58984 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:62823 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:62716 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:57910 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:61866 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 
OK
INFO:     127.0.0.1:64431 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:61464 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:65532 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:53061 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
2026-02-04 10:16:36,920 - app.services.worldview_sync_service - INFO - [世界观同步] 解析结果: 新人物=14, 新地点=5, 新设定=9
2026-02-04 10:16:36,933 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-02-04 10:16:36,933 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-02-04 10:16:36,933 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2026-02-04 10:16:38,368 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz:8443/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-02-04 10:16:38,368 - app.services.worldview_sync_service - INFO - [世界观同步] AI服务初始化完成: api_key=***KFzr, base_url=https://204992.xyz:8443/v1, model=gemini-2.5-pro
2026-02-04 10:16:38,376 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 未传递task_type，使用默认模型: gemini-2.5-pro
INFO:     127.0.0.1:58907 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:51751 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:57035 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:57535 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:59899 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:56143 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:62816 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:64646 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:55755 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:51094 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:63303 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:63524 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:64763 - "GET /api/v1/works/26cfcf99-9e77-4686-b21d-b82d1881e56d/worldview/scan-progress HTTP/1.1" 200 OK