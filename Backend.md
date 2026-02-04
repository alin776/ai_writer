INFO:     127.0.0.1:64499 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
2026-02-04 11:25:19,688 - app.api.v1.import_routes - INFO - 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456 预览导入文件: 人在诸天，摆烂成帝.txt, 格式: txt
2026-02-04 11:25:19,773 - app.api.v1.import_routes - INFO - 预览成功: 作品=人在诸天，摆烂成帝, 章节数=100
INFO:     127.0.0.1:57611 - "POST /api/v1/works/import/preview HTTP/1.1" 200 OK
2026-02-04 11:25:28,719 - app.api.v1.import_routes - INFO - 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456 导入文件: 人在诸天，摆烂成帝.txt, 格式: txt
2026-02-04 11:25:28,720 - app.api.v1.import_routes - INFO - [导入参数] auto_extract_worldview=True, scan_mode=full, format=txt, background_tasks=True
2026-02-04 11:25:28,721 - app.services.import_service - INFO - 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456 开始导入文本数据
2026-02-04 11:25:32,375 - app.core.redis - INFO - ✅ Redis connected: redis://localhost:6379/0
2026-02-04 11:25:32,387 - app.services.import_service - INFO - 文本导入完成: 作品ID=24998c56-d1e1-4ffa-93a7-e86dddf98b27, 章节=100
2026-02-04 11:25:32,451 - app.api.v1.import_routes - INFO - [世界观提取] 已为作品 24998c56-d1e1-4ffa-93a7-e86dddf98b27 排队世界观提取任务
2026-02-04 11:25:32,454 - app.api.v1.import_routes - INFO - 导入成功: 作品ID=24998c56-d1e1-4ffa-93a7-e86dddf98b27, 章节=100, 人物=0
2026-02-04 11:25:32,461 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/works/import
INFO:     127.0.0.1:55354 - "POST /api/v1/works/import HTTP/1.1" 200 OK
2026-02-04 11:25:32,465 - app.services.worldview_extraction_runner - INFO - [世界观提取] 开始为作品 24998c56-d1e1-4ffa-93a7-e86dddf98b27 提取世界观
2026-02-04 11:25:32,630 - app.services.ai.prompts - INFO - Prompts loaded successfully from D:\Java\ai_writer\backend\app\services\ai\prompts\default.json
2026-02-04 11:25:32,635 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-02-04 11:25:32,636 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-02-04 11:25:32,641 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2026-02-04 11:25:35,448 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz:8443/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-02-04 11:25:35,451 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2026-02-04 11:25:37,941 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz:8443/v1, Model: gemini-2.5-flash, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: False, CostTracking: True
2026-02-04 11:25:38,157 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 未启用(model_selector=None)，使用默认模型: gemini-2.5-flash
INFO:     127.0.0.1:50115 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
INFO:     127.0.0.1:51720 - "GET /api/v1/works/24998c56-d1e1-4ffa-93a7-e86dddf98b27/worldview/scan-progress HTTP/1.1" 200 OK
2026-02-04 11:26:10,611 - app.services.worldview_sync_service - INFO - [世界观同步] 解析结果: 新人物=7, 新地点=10, 新设定=14
2026-02-04 11:26:10,717 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-02-04 11:26:10,719 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=world_building, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: world_building; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
INFO:     127.0.0.1:62551 - "GET /api/v1/works/24998c56-d1e1-4ffa-93a7-e86dddf98b27/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:54606 - "GET /api/v1/works/24998c56-d1e1-4ffa-93a7-e86dddf98b27/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:49617 - "GET /api/v1/works/24998c56-d1e1-4ffa-93a7-e86dddf98b27/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:63282 - "GET /api/v1/works/24998c56-d1e1-4ffa-93a7-e86dddf98b27/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:51002 - "GET /api/v1/works/24998c56-d1e1-4ffa-93a7-e86dddf98b27/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:59449 - "GET /api/v1/works/24998c56-d1e1-4ffa-93a7-e86dddf98b27/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:50597 - "GET /api/v1/works/24998c56-d1e1-4ffa-93a7-e86dddf98b27/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:51803 - "GET /api/v1/works/24998c56-d1e1-4ffa-93a7-e86dddf98b27/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:49390 - "GET /api/v1/works/24998c56-d1e1-4ffa-93a7-e86dddf98b27/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:62188 - "GET /api/v1/works/24998c56-d1e1-4ffa-93a7-e86dddf98b27/worldview/scan-progress HTTP/1.1" 200 OK
2026-02-04 11:27:04,483 - app.services.worldview_sync_service - INFO - [世界观同步] 解析结果: 新人物=10, 新地点=6, 新设定=8
2026-02-04 11:27:04,588 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-02-04 11:27:04,588 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=world_building, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: world_building; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
INFO:     127.0.0.1:64980 - "GET /api/v1/works/24998c56-d1e1-4ffa-93a7-e86dddf98b27/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:49454 - "GET /api/v1/works/24998c56-d1e1-4ffa-93a7-e86dddf98b27/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:64599 - "GET /api/v1/works/24998c56-d1e1-4ffa-93a7-e86dddf98b27/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:58431 - "GET /api/v1/works/24998c56-d1e1-4ffa-93a7-e86dddf98b27/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:55434 - "GET /api/v1/works/24998c56-d1e1-4ffa-93a7-e86dddf98b27/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:54658 - "GET /api/v1/works/24998c56-d1e1-4ffa-93a7-e86dddf98b27/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:64309 - "GET /api/v1/works/24998c56-d1e1-4ffa-93a7-e86dddf98b27/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:49817 - "GET /api/v1/works/24998c56-d1e1-4ffa-93a7-e86dddf98b27/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:57193 - "GET /api/v1/works/24998c56-d1e1-4ffa-93a7-e86dddf98b27/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:49515 - "GET /api/v1/works/24998c56-d1e1-4ffa-93a7-e86dddf98b27/worldview/scan-progress HTTP/1.1" 200 OK
2026-02-04 11:28:05,178 - app.services.worldview_sync_service - INFO - [世界观同步] 解析结果: 新人物=13, 新地点=5, 新设定=8
2026-02-04 11:28:05,276 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-02-04 11:28:05,276 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=world_building, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: world_building; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
INFO:     127.0.0.1:53862 - "GET /api/v1/works/24998c56-d1e1-4ffa-93a7-e86dddf98b27/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:61216 - "GET /api/v1/works/24998c56-d1e1-4ffa-93a7-e86dddf98b27/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:59599 - "GET /api/v1/works/24998c56-d1e1-4ffa-93a7-e86dddf98b27/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:58327 - "GET /api/v1/works/24998c56-d1e1-4ffa-93a7-e86dddf98b27/worldview/scan-progress HTTP/1.1" 200 OK
2026-02-04 11:29:02,771 - app.services.worldview_sync_service - INFO - [世界观同步] 解析结果: 新人物=14, 新地点=4, 新设定=7
2026-02-04 11:29:02,849 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-02-04 11:29:02,849 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=world_building, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: world_building; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
INFO:     127.0.0.1:60706 - "GET /api/v1/works/24998c56-d1e1-4ffa-93a7-e86dddf98b27/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:64337 - "GET /api/v1/works/24998c56-d1e1-4ffa-93a7-e86dddf98b27/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:51698 - "GET /api/v1/works/24998c56-d1e1-4ffa-93a7-e86dddf98b27/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:59824 - "GET /api/v1/works/24998c56-d1e1-4ffa-93a7-e86dddf98b27/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:56150 - "GET /api/v1/works/24998c56-d1e1-4ffa-93a7-e86dddf98b27/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:62820 - "GET /api/v1/works/24998c56-d1e1-4ffa-93a7-e86dddf98b27/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:56832 - "GET /api/v1/works/24998c56-d1e1-4ffa-93a7-e86dddf98b27/worldview/scan-progress HTTP/1.1" 200 OK
2026-02-04 11:30:16,052 - app.services.worldview_sync_service - INFO - [世界观同步] 解析结果: 新人物=11, 新地点=7, 新设定=6
2026-02-04 11:30:16,113 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-02-04 11:30:16,113 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=world_building, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: world_building; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-02-04 11:31:04,929 - app.services.worldview_sync_service - INFO - [世界观同步] 解析结果: 新人物=6, 新地点=6, 新设定=8
2026-02-04 11:31:05,010 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-02-04 11:31:05,010 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=world_building, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: world_building; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-02-04 11:32:15,815 - app.services.worldview_sync_service - INFO - [世界观同步] 解析结果: 新人物=12, 新地点=10, 新设定=8
2026-02-04 11:32:15,863 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-02-04 11:32:15,864 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=world_building, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: world_building; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-02-04 11:33:29,907 - app.services.worldview_sync_service - INFO - [世界观同步] 解析结果: 新人物=11, 新地点=4, 新设定=10
2026-02-04 11:33:29,996 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-02-04 11:33:29,996 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=world_building, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: world_building; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
INFO:     127.0.0.1:65305 - "GET /api/v1/works/24998c56-d1e1-4ffa-93a7-e86dddf98b27/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:53626 - "GET /api/v1/works/24998c56-d1e1-4ffa-93a7-e86dddf98b27/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:53028 - "GET /api/v1/works/24998c56-d1e1-4ffa-93a7-e86dddf98b27/worldview/scan-progress HTTP/1.1" 200 OK
2026-02-04 11:34:30,389 - app.services.ai.http_ai_service - ERROR - API 错误: 504, <!DOCTYPE html>
<!--[if lt IE 7]> <html class="no-js ie6 oldie" lang="en-US"> <![endif]-->
<!--[if IE 7]>    <html class="no-js ie7 oldie" lang="en-US"> <![endif]-->
<!--[if IE 8]>    <html class="no-js ie8 oldie" lang="en-US"> <![endif]-->
<!--[if gt IE 8]><!--> <html class="no-js" lang="en-US"> <!--<![endif]-->
<head>

<title>204992.xyz | 504: Gateway time-out</title>
<meta charset="UTF-8" />
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<meta http-equiv="X-UA-Compatibl
2026-02-04 11:34:30,389 - app.services.ai.http_ai_service - ERROR - AI API 调用错误: Exception: API 请求失败: 504, <!DOCTYPE html>
<!--[if lt IE 7]> <html class="no-js ie6 oldie" lang="en-US"> <![endif]-->
<!--[if IE 7]>    <html class="no-js ie7 oldie" lang="en-US"> <![endif]-->
<!--[if IE 8]>    <html class="no-js ie8 oldie" lang="en-US"> <![endif]-->
<!--[if gt IE 8]><!--> <html class="no-js" lang="en-US"> <!--<![endif]-->
<head>

<title>204992.xyz | 504: Gateway time-out</title>
<meta charset="UTF-8" />
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<meta http-equiv="X-UA-Compatibl
2026-02-04 11:34:30,389 - app.services.worldview_sync_service - ERROR - AI批量提取世界观变化失败: API 请求失败: 504, <!DOCTYPE html>
<!--[if lt IE 7]> <html class="no-js ie6 oldie" lang="en-US"> <![endif]-->
<!--[if IE 7]>    <html class="no-js ie7 oldie" lang="en-US"> <![endif]-->
<!--[if IE 8]>    <html class="no-js ie8 oldie" lang="en-US"> <![endif]-->
<!--[if gt IE 8]><!--> <html class="no-js" lang="en-US"> <!--<![endif]-->
<head>

<title>204992.xyz | 504: Gateway time-out</title>
<meta charset="UTF-8" />
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<meta http-equiv="X-UA-Compatibl
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\services\worldview_sync_service.py", line 931, in _ai_batch_extract_changes
    async for chunk, usage in ai_service._stream_chat(
  File "D:\Java\ai_writer\backend\app\services\ai\http_ai_service.py", line 337, in _stream_chat
    raise Exception(f"API 请求失败: {response.status_code}, {error_msg}")
Exception: API 请求失败: 504, <!DOCTYPE html>
<!--[if lt IE 7]> <html class="no-js ie6 oldie" lang="en-US"> <![endif]-->
<!--[if IE 7]>    <html class="no-js ie7 oldie" lang="en-US"> <![endif]-->
<!--[if IE 8]>    <html class="no-js ie8 oldie" lang="en-US"> <![endif]-->
<!--[if gt IE 8]><!--> <html class="no-js" lang="en-US"> <!--<![endif]-->
<head>

<title>204992.xyz | 504: Gateway time-out</title>
<meta charset="UTF-8" />
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<meta http-equiv="X-UA-Compatibl
2026-02-04 11:34:30,547 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-02-04 11:34:30,549 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=world_building, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: world_building; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
INFO:     127.0.0.1:55947 - "GET /api/v1/works/24998c56-d1e1-4ffa-93a7-e86dddf98b27/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:56283 - "GET /api/v1/works/24998c56-d1e1-4ffa-93a7-e86dddf98b27/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:62105 - "GET /api/v1/works/24998c56-d1e1-4ffa-93a7-e86dddf98b27/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:62940 - "GET /api/v1/works/24998c56-d1e1-4ffa-93a7-e86dddf98b27/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:54889 - "GET /api/v1/works/24998c56-d1e1-4ffa-93a7-e86dddf98b27/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:52743 - "GET /api/v1/works/24998c56-d1e1-4ffa-93a7-e86dddf98b27/worldview/scan-progress HTTP/1.1" 200 OK
INFO:     127.0.0.1:59414 - "GET /api/v1/works/24998c56-d1e1-4ffa-93a7-e86dddf98b27/worldview/scan-progress HTTP/1.1" 200 OK
2026-02-04 11:35:43,807 - app.services.worldview_sync_service - INFO - [世界观同步] 解析结果: 新人物=10, 新地点=6, 新设定=10
2026-02-04 11:35:43,848 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-02-04 11:35:43,851 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=world_building, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: world_building; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-02-04 11:37:00,001 - app.services.worldview_sync_service - INFO - [世界观同步] 解析结果: 新人物=14, 新地点=6, 新设定=10
2026-02-04 11:37:00,111 - app.services.worldview_extraction_runner - INFO - [世界观提取] 扫描完成: 100章, 发现 61人物, 48地点, 80设定
2026-02-04 11:37:00,177 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 林仙
2026-02-04 11:37:00,193 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 系统10086
2026-02-04 11:37:00,216 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 叶凡
2026-02-04 11:37:00,231 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 荒天帝
2026-02-04 11:37:00,238 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 庞博
2026-02-04 11:37:00,238 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 楚终极
2026-02-04 11:37:00,251 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 龙虎山老天师
2026-02-04 11:37:00,257 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 狠人大帝
2026-02-04 11:37:00,257 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 张楚岚
2026-02-04 11:37:00,269 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 冯宝宝
2026-02-04 11:37:00,276 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 周毅
2026-02-04 11:37:00,282 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 刘云志
2026-02-04 11:37:00,288 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 夏禾
2026-02-04 11:37:00,294 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 徐三
2026-02-04 11:37:00,302 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 无根生（冯曜）
2026-02-04 11:37:00,310 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 张怀义（张锡林）
2026-02-04 11:37:00,317 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 风正豪
2026-02-04 11:37:00,325 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 吕良
2026-02-04 11:37:00,331 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 徐三/徐四
2026-02-04 11:37:00,340 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 赵方旭（赵总）
2026-02-04 11:37:00,349 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 柳妍妍
2026-02-04 11:37:00,358 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 风莎燕/风星潼
2026-02-04 11:37:00,369 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 徐翔（狗娃子）
2026-02-04 11:37:00,378 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 张之维（老天师）
2026-02-04 11:37:00,387 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 赵方旭
2026-02-04 11:37:00,396 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 巴伦
2026-02-04 11:37:00,403 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 陆谨
2026-02-04 11:37:00,414 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 徐翔
2026-02-04 11:37:00,422 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 田晋中
2026-02-04 11:37:00,431 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 风天养
2026-02-04 11:37:00,440 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 王蔼/王并
2026-02-04 11:37:00,452 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 马云
2026-02-04 11:37:00,461 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 神桥老妪
2026-02-04 11:37:00,473 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 玉鼎掌教
2026-02-04 11:37:00,483 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 张道陵
2026-02-04 11:37:00,495 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 周圣
2026-02-04 11:37:00,507 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 段德
2026-02-04 11:37:00,520 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 青帝（万青）
2026-02-04 11:37:00,533 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 颜如玉
2026-02-04 11:37:00,543 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 马云长老
2026-02-04 11:37:00,554 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 老疯子
2026-02-04 11:37:00,566 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 姜婷婷
2026-02-04 11:37:00,577 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 青帝
2026-02-04 11:37:00,587 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: System 10086
2026-02-04 11:37:00,598 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 姜逸飞
2026-02-04 11:37:00,608 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 姜老头
2026-02-04 11:37:00,617 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 摇光弟子
2026-02-04 11:37:00,626 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 青帝十九代孙（药老）
2026-02-04 11:37:00,635 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 韩长老（韩立/韩易火）
2026-02-04 11:37:00,646 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 秦瑶
2026-02-04 11:37:00,652 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 化龙老妪
2026-02-04 11:37:00,661 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 姬家老圣人
2026-02-04 11:37:00,666 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 李若愚
2026-02-04 11:37:00,679 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 华云飞
2026-02-04 11:37:00,689 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 姬皓月
2026-02-04 11:37:00,699 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 姬紫月
2026-02-04 11:37:00,707 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 虚空大帝
2026-02-04 11:37:00,715 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 狠人一脉终极护道人
2026-02-04 11:37:00,724 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 摇光圣子
2026-02-04 11:37:00,729 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 星峰之主
2026-02-04 11:37:00,740 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 小婷婷
2026-02-04 11:37:00,770 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 繁华的都市
2026-02-04 11:37:00,787 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 泰山
2026-02-04 11:37:00,799 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 一人之下世界
2026-02-04 11:37:00,811 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 遮天宇宙
2026-02-04 11:37:00,817 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 星空宇宙
2026-02-04 11:37:00,826 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 仙域
2026-02-04 11:37:00,834 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 混沌海
2026-02-04 11:37:00,841 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 洪荒古星
2026-02-04 11:37:00,849 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 北斗古星
2026-02-04 11:37:00,856 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 荧惑古星
2026-02-04 11:37:00,862 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 九龙拉棺
2026-02-04 11:37:00,869 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 北斗葬帝星
2026-02-04 11:37:00,878 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 荒古禁地
2026-02-04 11:37:00,883 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 荧惑古星（火星）
2026-02-04 11:37:00,891 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 一人之下的地球
2026-02-04 11:37:00,898 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 大雷音寺
2026-02-04 11:37:00,904 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 哪都通公司
2026-02-04 11:37:00,912 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 龙虎山
2026-02-04 11:37:00,918 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 二十四节通天谷
2026-02-04 11:37:00,925 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 天下会
2026-02-04 11:37:00,931 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 林仙的别墅
2026-02-04 11:37:00,938 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 一人之下/一世之尊世界
2026-02-04 11:37:00,944 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 北斗星域（遮天世界）
2026-02-04 11:37:00,952 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 玉鼎洞天
2026-02-04 11:37:00,961 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 原始废墟
2026-02-04 11:37:00,970 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 青帝坟
2026-02-04 11:37:00,982 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 紫府圣地
2026-02-04 11:37:00,989 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 东荒
2026-02-04 11:37:00,997 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 北斗星
2026-02-04 11:37:01,002 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 生命禁区
2026-02-04 11:37:01,011 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 北斗古星/葬帝星
2026-02-04 11:37:01,018 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 天璇圣地
2026-02-04 11:37:01,027 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 紫微帝星
2026-02-04 11:37:01,035 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 摇光圣地
2026-02-04 11:37:01,042 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 飞仙星
2026-02-04 11:37:01,048 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 地球/星空彼岸
2026-02-04 11:37:01,058 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 天璇石坊
2026-02-04 11:37:01,066 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 清风小镇
2026-02-04 11:37:01,074 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 青帝一脉/玄元门
2026-02-04 11:37:01,081 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 魏国
2026-02-04 11:37:01,088 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 灵墟洞天
2026-02-04 11:37:01,095 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 太玄门
2026-02-04 11:37:01,103 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 拙峰
2026-02-04 11:37:01,111 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 星峰
2026-02-04 11:37:01,119 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 北斗
2026-02-04 11:37:01,126 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 紫山
2026-02-04 11:37:01,136 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 火域
2026-02-04 11:37:01,143 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 北域
2026-02-04 11:37:01,172 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 时空错位与系统绑定
2026-02-04 11:37:01,185 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 系统层级与运作
2026-02-04 11:37:01,197 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 林仙的“摆烂”哲学
2026-02-04 11:37:01,208 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 《遮天》宇宙世界观
2026-02-04 11:37:01,217 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 《一人之下》世界观
2026-02-04 11:37:01,227 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 遮天法/秘境法
2026-02-04 11:37:01,238 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 遮天三部曲
2026-02-04 11:37:01,250 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 仙王境
2026-02-04 11:37:01,264 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 道祖境
2026-02-04 11:37:01,277 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 祭道之上
2026-02-04 11:37:01,288 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 九龙拉棺
2026-02-04 11:37:01,300 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 八奇技：炁体源流
2026-02-04 11:37:01,312 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 轮海秘境详解
2026-02-04 11:37:01,322 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 雷劫
2026-02-04 11:37:01,331 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 遮天修炼体系
2026-02-04 11:37:01,339 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 特殊体质
2026-02-04 11:37:01,348 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 系统与穿越
2026-02-04 11:37:01,357 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 生命禁区与至尊
2026-02-04 11:37:01,366 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 一人之下异人体系
2026-02-04 11:37:01,374 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 大帝
2026-02-04 11:37:01,386 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 打卡系统
2026-02-04 11:37:01,394 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 内圣外王
2026-02-04 11:37:01,401 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 八奇技
2026-02-04 11:37:01,412 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 长生不老之谜
2026-02-04 11:37:01,421 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 跨世界修炼体系融合
2026-02-04 11:37:01,429 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 炁体源流
2026-02-04 11:37:01,437 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 异人与势力格局
2026-02-04 11:37:01,445 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 甲申之乱与三十六贼
2026-02-04 11:37:01,453 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 六库仙贼
2026-02-04 11:37:01,461 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 主角的系统
2026-02-04 11:37:01,470 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 先天一炁/先天之精
2026-02-04 11:37:01,478 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 凡体理论
2026-02-04 11:37:01,486 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 八奇技的深层解析
2026-02-04 11:37:01,496 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 异人界势力格局
2026-02-04 11:37:01,504 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 罗天大醮
2026-02-04 11:37:01,512 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 鬼仙
2026-02-04 11:37:01,520 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 双世界修炼体系差异
2026-02-04 11:37:01,527 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 八奇技的本质与应用
2026-02-04 11:37:01,535 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 系统机制
2026-02-04 11:37:01,544 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 飞升机制
2026-02-04 11:37:01,550 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 五雷正法
2026-02-04 11:37:01,560 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 《遮天》世界炼器三要素
2026-02-04 11:37:01,567 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 修炼体系
2026-02-04 11:37:01,575 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 荒古圣体
2026-02-04 11:37:01,584 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 帝兵
2026-02-04 11:37:01,592 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 源
2026-02-04 11:37:01,600 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 考古（盗墓）
2026-02-04 11:37:01,609 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 拘灵遣将
2026-02-04 11:37:01,616 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 啃之大道
2026-02-04 11:37:01,624 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 《道经》
2026-02-04 11:37:01,631 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 仙路
2026-02-04 11:37:01,639 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 寿元体系
2026-02-04 11:37:01,647 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 九秘
2026-02-04 11:37:01,655 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 天璇圣地覆灭秘闻
2026-02-04 11:37:01,663 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 荒奴
2026-02-04 11:37:01,671 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 北斗七圣
2026-02-04 11:37:01,678 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 修行五大秘境
2026-02-04 11:37:01,687 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 禁（战力衡量）
2026-02-04 11:37:01,695 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 六道轮回拳
2026-02-04 11:37:01,703 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 人皇幡
2026-02-04 11:37:01,709 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 至尊与黑暗动乱
2026-02-04 11:37:01,718 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 妖帝之心
2026-02-04 11:37:01,726 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 人族母经
2026-02-04 11:37:01,733 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 行字秘
2026-02-04 11:37:01,741 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 九秘·皆字秘
2026-02-04 11:37:01,749 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 狠人传承体系（吞天魔功/不灭天功）
2026-02-04 11:37:01,757 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 体质与道途
2026-02-04 11:37:01,764 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 神禁与八禁
2026-02-04 11:37:01,773 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 虚空大帝即黄帝
2026-02-04 11:37:01,782 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 红尘仙路
2026-02-04 11:37:01,791 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 信仰长生法
2026-02-04 11:37:01,801 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 染血的黑色纸船
2026-02-04 11:37:01,809 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 玄黄母气根
2026-02-04 11:37:01,817 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 自然大道
2026-02-04 11:37:01,826 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 帝路争锋
2026-02-04 11:37:01,835 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 狠人传承体系
2026-02-04 11:37:01,842 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 天庭/大爱仙盟
2026-02-04 11:37:01,850 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 段德的多重身份
2026-02-04 11:37:01,861 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 源与源天师
2026-02-04 11:37:01,871 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 小纸船
2026-02-04 11:37:01,906 - app.services.worldview_sync_service - INFO - [世界观同步] 创建关系: 林仙 -> 系统10086: 互相吐槽的搭档/合作者
2026-02-04 11:37:01,906 - app.services.worldview_sync_service - WARNING - [世界观同步] 无法找到人物ID: 众人（叶凡、庞博等）(None) -> 林仙(c5403d3e-2be4-4f8e-8361-f7733a11fd29)
2026-02-04 11:37:01,909 - app.services.worldview_sync_service - INFO - [世界观同步] 创建关系: 林仙 -> 叶凡: 深度绑定的商业伙伴/共犯
2026-02-04 11:37:01,911 - app.services.worldview_sync_service - INFO - [世界观同步] 创建关系: 林仙 -> 张楚岚: 强行指定的保护者/师长
2026-02-04 11:37:01,914 - app.services.worldview_sync_service - INFO - [世界观同步] 创建关系: 叶凡 -> 庞博: 同为特殊体质的修行道友
2026-02-04 11:37:01,915 - app.services.worldview_sync_service - INFO - [世界观同步] 创建关系: 林仙 -> 夏禾: 俘虏与控制者
2026-02-04 11:37:01,917 - app.services.worldview_sync_service - INFO - [世界观同步] 创建关系: 林仙 -> 风正豪: 战略盟友
2026-02-04 11:37:01,918 - app.services.worldview_sync_service - INFO - [世界观同步] 创建关系: 林仙 -> 冯宝宝: 引导者与追随者
2026-02-04 11:37:01,920 - app.services.worldview_sync_service - INFO - [世界观同步] 创建关系: 冯宝宝 -> 无根生（冯曜）: 已确认的父女关系
2026-02-04 11:37:01,921 - app.services.worldview_sync_service - WARNING - [世界观同步] 无法找到人物ID: 张楚岚(55183e5e-6e2e-4b9b-bbe8-bd52a693f857) -> 风莎燕(None)
2026-02-04 11:37:01,923 - app.services.worldview_sync_service - INFO - [世界观同步] 创建关系: 林仙 -> 吕良: 被压榨的下属
2026-02-04 11:37:01,923 - app.services.worldview_sync_service - INFO - [世界观同步] 创建关系: 林仙 -> 张之维（老天师）: 对手转为合作者
2026-02-04 11:37:01,925 - app.services.worldview_sync_service - INFO - [世界观同步] 创建关系: 林仙 -> 赵方旭: 相互试探的谈判对象
2026-02-04 11:37:01,925 - app.services.worldview_sync_service - WARNING - [世界观同步] 无法找到人物ID: 风家(None) -> 王家(None)
2026-02-04 11:37:01,927 - app.services.worldview_sync_service - INFO - [世界观同步] 创建关系: 林仙 -> 巴伦: 传道者与求道者
2026-02-04 11:37:01,927 - app.services.worldview_sync_service - WARNING - [世界观同步] 无法找到人物ID: 林仙(c5403d3e-2be4-4f8e-8361-f7733a11fd29) -> 玉鼎洞天(None)
2026-02-04 11:37:01,929 - app.services.worldview_sync_service - INFO - [世界观同步] 创建关系: 林仙 -> 神桥老妪: 敌对并将其斩杀
2026-02-04 11:37:01,929 - app.services.worldview_sync_service - WARNING - [世界观同步] 无法找到人物ID: 周圣(77fde4e7-cdb6-4c3d-98af-069352f5edce) -> 王也(None)
2026-02-04 11:37:01,931 - app.services.worldview_sync_service - INFO - [世界观同步] 创建关系: 田晋中 -> 巴伦: 师徒
2026-02-04 11:37:01,934 - app.services.worldview_sync_service - INFO - [世界观同步] 创建关系: 林仙 -> 段德: “考古”事业合伙人/互相算计的损友
2026-02-04 11:37:01,936 - app.services.worldview_sync_service - INFO - [世界观同步] 创建关系: 叶凡 -> 段德: 受害者与加害者/“考古”事业合伙人
2026-02-04 11:37:01,936 - app.services.worldview_sync_service - WARNING - [世界观同步] 无法找到人物ID: 林仙、叶凡、段德(None) -> （团队）(None)
2026-02-04 11:37:01,938 - app.services.worldview_sync_service - INFO - [世界观同步] 创建关系: 林仙 -> 姜婷婷: 师徒 / 圣主与圣女
2026-02-04 11:37:01,941 - app.services.worldview_sync_service - INFO - [世界观同步] 创建关系: 林仙 -> 老疯子: 同门后辈与前辈 / 新圣主与旧圣人
2026-02-04 11:37:01,941 - app.services.worldview_sync_service - WARNING - [世界观同步] 无法找到人物ID: 叶凡(b5d8187b-4216-406f-975e-9ea97a63c085) -> 天璇圣地(None)
2026-02-04 11:37:01,941 - app.services.worldview_sync_service - WARNING - [世界观同步] 无法找到人物ID: 姜婷婷(3c5e0f48-8a30-411b-9235-c407eb545f7c) -> 天璇圣地(None)
2026-02-04 11:37:01,945 - app.services.worldview_sync_service - INFO - [世界观同步] 创建关系: 林仙 -> 颜如玉: 盟友与名义上的未婚夫妻
2026-02-04 11:37:01,945 - app.services.worldview_sync_service - WARNING - [世界观同步] 无法找到人物ID: 天璇圣地(None) -> 青帝一脉(None)
2026-02-04 11:37:01,945 - app.services.worldview_sync_service - WARNING - [世界观同步] 无法找到人物ID: 林仙(c5403d3e-2be4-4f8e-8361-f7733a11fd29) -> 青帝十九代孙(None)
2026-02-04 11:37:01,949 - app.services.worldview_sync_service - INFO - [世界观同步] 创建关系: 老疯子 -> 姜婷婷: 类似祖孙的师徒关系
2026-02-04 11:37:01,949 - app.services.worldview_sync_service - WARNING - [世界观同步] 无法找到人物ID: 林仙(c5403d3e-2be4-4f8e-8361-f7733a11fd29) -> 姬家(None)
2026-02-04 11:37:01,949 - app.services.worldview_sync_service - WARNING - [世界观同步] 无法找到人物ID: 叶凡(b5d8187b-4216-406f-975e-9ea97a63c085) -> 姬家(None)
2026-02-04 11:37:01,950 - app.services.worldview_sync_service - WARNING - [世界观同步] 无法找到人物ID: 天璇圣地 (林仙代表)(None) -> 姬家、青帝一脉(None)
2026-02-04 11:37:01,950 - app.services.worldview_sync_service - WARNING - [世界观同步] 无法找到人物ID: 林仙(c5403d3e-2be4-4f8e-8361-f7733a11fd29) -> 李若愚 (拙峰)(None)
2026-02-04 11:37:01,950 - app.services.worldview_sync_service - WARNING - [世界观同步] 无法找到人物ID: 华云飞(34c8e550-2edc-4bde-8b95-7870ce42246c) -> 狠人一脉(None)
2026-02-04 11:37:01,953 - app.services.worldview_sync_service - INFO - [世界观同步] 创建关系: 林仙 -> 华云飞: 盟友/组织领袖与成员
2026-02-04 11:37:01,953 - app.services.worldview_sync_service - WARNING - [世界观同步] 无法找到人物ID: 林仙、叶凡(None) -> 姬家、妖族(None)
2026-02-04 11:37:01,955 - app.services.worldview_sync_service - INFO - [世界观同步] 创建关系: 林仙 -> 星峰之主: 记名弟子/受其投资的盟友
2026-02-04 11:37:02,026 - app.services.worldview_sync_service - INFO - [Worldview Sync] Cache invalidated: worldview:characters:24998c56-d1e1-4ffa-93a7-e86dddf98b27
2026-02-04 11:37:02,032 - app.services.worldview_sync_service - INFO - [Worldview Sync] Cache invalidated: worldview:locations:24998c56-d1e1-4ffa-93a7-e86dddf98b27
2026-02-04 11:37:02,036 - app.services.worldview_sync_service - INFO - [Worldview Sync] Cache invalidated: worldview:settings:24998c56-d1e1-4ffa-93a7-e86dddf98b27
2026-02-04 11:37:02,040 - app.services.worldview_sync_service - INFO - [Worldview Sync] Cache invalidated: worldview:guidelines:24998c56-d1e1-4ffa-93a7-e86dddf98b27
2026-02-04 11:37:02,042 - app.services.worldview_sync_service - INFO - [Worldview Sync] Cache invalidated: worldview:worlddata:24998c56-d1e1-4ffa-93a7-e86dddf98b27
2026-02-04 11:37:02,049 - app.services.worldview_extraction_runner - INFO - [世界观提取] 应用完成: {'characters_created': 61, 'characters_updated': 0, 'locations_created': 48, 'locations_updated': 0, 'settings_created': 80, 'settings_updated': 0, 'relationships_created': 22}
2026-02-04 11:38:57,680 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works/24998c56-d1e1-4ffa-93a7-e86dddf98b27/worldview/scan-progress
INFO:     127.0.0.1:52245 - "GET /api/v1/works/24998c56-d1e1-4ffa-93a7-e86dddf98b27/worldview/scan-progress HTTP/1.1" 200 OK