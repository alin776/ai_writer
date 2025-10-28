(venv) PS D:\Java\ai_writer\backend> python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
INFO:     Will watch for changes in these directories: ['D:\\Java\\ai_writer\\backend']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [26972] using WatchFiles
已注册策略: web_novel_11d - 网文11维度分析
INFO:     Started server process [25100]
INFO:     Waiting for application startup.
2025-10-28 19:09:38,498 - app.main - INFO - 🚀 应用启动中...
2025-10-28 19:09:38,498 - app.core.database - INFO - 正在初始化数据库... (尝试 1/3)
2025-10-28 19:09:38,615 - app.core.database - INFO - ✅ 数据库初始化成功
2025-10-28 19:09:38,615 - apscheduler.scheduler - INFO - Adding job tentatively -- it will be properly scheduled when the scheduler starts
2025-10-28 19:09:38,617 - apscheduler.scheduler - INFO - Added job "清理过期的去痕迹会话详情" to job store "default"
2025-10-28 19:09:38,617 - apscheduler.scheduler - INFO - Scheduler started
2025-10-28 19:09:38,617 - app.tasks.cleanup_humanize_details - INFO - 定时任务调度器已启动
2025-10-28 19:09:38,617 - app.main - INFO - 🔄 开始预加载Embedding模型...
2025-10-28 19:09:38,618 - app.services.vector_store_service - INFO - 🔄 预加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
2025-10-28 19:09:38,618 - sentence_transformers.SentenceTransformer - INFO - Use pytorch device_name: cpu
2025-10-28 19:09:38,619 - sentence_transformers.SentenceTransformer - INFO - Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
2025-10-28 19:09:46,501 - app.services.vector_store_service - INFO - ✅ Embedding模型预加载成功，耗时: 7.88秒
2025-10-28 19:09:46,502 - app.main - INFO - ✅ Embedding模型预加载完成
2025-10-28 19:09:46,502 - app.main - INFO - ✅ 应用启动完成
INFO:     Application startup complete.
INFO:     127.0.0.1:60624 - "POST /api/v1/auth/login HTTP/1.1" 200 OK
2025-10-28 19:09:51,488 - app.api.v1.ai - INFO - [多模型改写] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), 文本长度: 16, 模式: RewriteMode.EXPAND
2025-10-28 19:09:51,488 - app.api.v1.ai - INFO - [多模型改写] 使用模型: ['gemini-2.5-pro', 'gpt-5']
2025-10-28 19:09:52,101 - app.services.ai.rewrite_arena_service - INFO - RewriteArenaService 初始化成功 (最大并发: 3, 超时时间: 30s)
2025-10-28 19:09:52,101 - app.services.ai.rewrite_arena_service - INFO - 开始多模型改写 - 模型数量: 2, 最大并发: 3, 超时限制: 30s
2025-10-28 19:09:52,102 - app.services.ai.rewrite_arena_service - INFO - [gemini-2.5-pro] 开始改写
2025-10-28 19:09:52,102 - app.services.ai.rewrite_arena_service - INFO - [gpt-5] 开始改写
2025-10-28 19:10:03,458 - httpx - INFO - HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
2025-10-28 19:10:03,459 - app.services.ai.rewrite_arena_service - INFO - [gpt-5] 改写完成，耗时: 11.36s, 字数: 240
2025-10-28 19:10:17,928 - httpx - INFO - HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
2025-10-28 19:10:17,930 - app.services.ai.rewrite_arena_service - INFO - [gemini-2.5-pro] 改写完成，耗时: 25.83s, 字数: 298
2025-10-28 19:10:17,931 - app.services.ai.rewrite_arena_service - INFO - 多模型改写完成 - 总耗时: 25.83s, 成功: 2/2, 超时: 0/2
2025-10-28 19:10:17,931 - app.api.v1.ai - INFO - [多模型改写] 用户 testuser_new-1 改写完成，成功: 2/2
INFO:     127.0.0.1:60627 - "POST /api/v1/ai/rewrite-arena/rewrite HTTP/1.1" 200 OK
