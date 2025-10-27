(venv) PS D:\Java\ai_writer\backend> python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
INFO:     Will watch for changes in these directories: ['D:\\Java\\ai_writer\\backend']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [27264] using WatchFiles
已注册策略: web_novel_11d - 网文11维度分析
INFO:     Started server process [27832]
INFO:     Waiting for application startup.
2025-10-27 22:38:49,497 - app.main - INFO - 🚀 应用启动中...
2025-10-27 22:38:49,497 - app.core.database - INFO - 正在初始化数据库... (尝试 1/3)
2025-10-27 22:38:49,617 - app.core.database - INFO - ✅ 数据库初始化成功
2025-10-27 22:38:49,631 - apscheduler.scheduler - INFO - Adding job tentatively -- it will be properly scheduled when the scheduler starts
2025-10-27 22:38:49,633 - apscheduler.scheduler - INFO - Added job "清理过期的去痕迹会话详情" to job store "default"
2025-10-27 22:38:49,633 - apscheduler.scheduler - INFO - Scheduler started
2025-10-27 22:38:49,633 - app.tasks.cleanup_humanize_details - INFO - 定时任务调度器已启动
2025-10-27 22:38:49,633 - app.main - INFO - 🔄 开始预加载Embedding模型...
2025-10-27 22:38:49,633 - app.services.vector_store_service - INFO - 🔄 预加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
2025-10-27 22:38:49,633 - sentence_transformers.SentenceTransformer - INFO - Use pytorch device_name: cpu
2025-10-27 22:38:49,633 - sentence_transformers.SentenceTransformer - INFO - Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
2025-10-27 22:38:57,854 - app.services.vector_store_service - INFO - ✅ Embedding模型预加载成功，耗时: 8.22秒
2025-10-27 22:38:57,854 - app.main - INFO - ✅ Embedding模型预加载完成
2025-10-27 22:38:57,854 - app.main - INFO - ✅ 应用启动完成
INFO:     Application startup complete.
INFO:     127.0.0.1:52012 - "POST /api/v1/auth/login HTTP/1.1" 200 OK
INFO:     127.0.0.1:52015 - "GET /api/v1/users/me HTTP/1.1" 200 OK
2025-10-27 22:39:03,546 - app.services.novel_analysis_service - INFO - Deleted old analysis for work ddc0183e-76f5-4187-a491-9692a341996b, creating new one
2025-10-27 22:39:03,549 - app.services.novel_analysis_service - INFO - Created analysis task for work ddc0183e-76f5-4187-a491-9692a341996b, total_chapters: 20
2025-10-27 22:39:03,549 - app.api.v1.novel_analysis - INFO - User 602f5147-846a-4cde-95d3-405fa75f133f started analysis for work ddc0183e-76f5-4187-a491-9692a341996b, analysis_id: 8dea84ef-1098-4d8b-b0ca-8ac0d354eb4a
INFO:     127.0.0.1:52018 - "POST /api/v1/analysis/works/ddc0183e-76f5-4187-a491-9692a341996b/start HTTP/1.1" 201 Created
2025-10-27 22:39:03,654 - app.api.v1.novel_analysis - INFO - 后台任务开始：分析作品 ddc0183e-76f5-4187-a491-9692a341996b
2025-10-27 22:39:03,656 - app.api.v1.novel_analysis - INFO - 后台任务已找到分析记录 analysis_id=8dea84ef-1098-4d8b-b0ca-8ac0d354eb4a
2025-10-27 22:39:03,656 - app.services.ai.novel_analysis_orchestrator - INFO - ============================================================
2025-10-27 22:39:03,656 - app.services.ai.novel_analysis_orchestrator - INFO - 开始分析作品: ddc0183e-76f5-4187-a491-9692a341996b
2025-10-27 22:39:03,656 - app.services.ai.novel_analysis_orchestrator - INFO - ============================================================
2025-10-27 22:39:03,666 - app.services.novel_analysis_service - INFO - Updated analysis 8dea84ef-1098-4d8b-b0ca-8ac0d354eb4a progress: 0/20, stage: AnalysisStage.MICRO_ANALYSIS, status: AnalysisStatus.ANALYZING
2025-10-27 22:39:03,666 - app.services.ai.novel_analysis_orchestrator - INFO - 初始化AI分析服务...
2025-10-27 22:39:03,666 - app.services.ai.prompts - INFO - Prompts loaded successfully from D:\Java\ai_writer\backend\app\services\ai\prompts\default.json
2025-10-27 22:39:04,884 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s
2025-10-27 22:39:04,884 - app.services.ai.novel_micro_analysis - INFO - 微观分析提示词加载成功
2025-10-27 22:39:05,610 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s
2025-10-27 22:39:05,610 - app.services.ai.novel_macro_analysis - INFO - 宏观分析提示词加载成功
2025-10-27 22:39:05,624 - app.services.ai.novel_analysis_orchestrator - INFO - 共获取 20 个章节，开始微观分析...
2025-10-27 22:39:05,624 - app.services.ai.novel_analysis_orchestrator - INFO - ⚡ 使用并行分析模式 (并发数: 5)
2025-10-27 22:39:05,624 - app.services.ai.novel_analysis_orchestrator - INFO - ⚡ 启动 20 个并发分析任务...
2025-10-27 22:39:05,624 - app.services.ai.novel_analysis_orchestrator - INFO - [1/20] 🔄 开始分析: 第1章 修炼之路
2025-10-27 22:39:05,631 - app.services.ai.novel_analysis_orchestrator - INFO - [2/20] 🔄 开始分析: 第2章 修炼之路
2025-10-27 22:39:05,633 - app.services.ai.novel_analysis_orchestrator - INFO - [3/20] 🔄 开始分析: 第3章 修炼之路
2025-10-27 22:39:05,633 - app.services.ai.novel_analysis_orchestrator - INFO - [4/20] 🔄 开始分析: 第4章 修炼之路
2025-10-27 22:39:05,633 - app.services.ai.novel_analysis_orchestrator - INFO - [5/20] 🔄 开始分析: 第5章 修炼之路
INFO:     127.0.0.1:50756 - "GET /api/v1/analysis/works/ddc0183e-76f5-4187-a491-9692a341996b HTTP/1.1" 200 OK
2025-10-27 22:39:07,677 - app.services.redis_cache_service - INFO - ✓ Redis连接成功
2025-10-27 22:39:07,677 - app.services.redis_cache_service - INFO - ✓ 缓存命中: novel_analysis:micro:26ef9f90a88...
2025-10-27 22:39:07,677 - app.services.ai.novel_micro_analysis - INFO - ⚡ 使用缓存结果: b1e9f52a-ab87-45a0-b924-2a89c25bb74b - 第3章 修炼之路
2025-10-27 22:39:07,677 - app.services.ai.novel_analysis_orchestrator - INFO - [3/20] ✓ 分析完成: 第3章 修炼之路 (2.0秒)
2025-10-27 22:39:07,679 - app.services.redis_cache_service - INFO - ✓ 缓存命中: novel_analysis:micro:af8a84a9203...
2025-10-27 22:39:07,679 - app.services.ai.novel_micro_analysis - INFO - ⚡ 使用缓存结果: e8f60b96-fa2b-4ce4-8e3f-7e2863cafe32 - 第5章 修炼之路
2025-10-27 22:39:07,679 - app.services.ai.novel_analysis_orchestrator - INFO - [5/20] ✓ 分析完成: 第5章 修炼之路 (2.0秒)
2025-10-27 22:39:07,679 - app.services.redis_cache_service - INFO - ✓ 缓存命中: novel_analysis:micro:969ea95d05f...
2025-10-27 22:39:07,679 - app.services.ai.novel_micro_analysis - INFO - ⚡ 使用缓存结果: bfe8ae0a-b7ed-450d-aa9e-b0a73ad3cdf1 - 第2章 修炼之路
2025-10-27 22:39:07,681 - app.services.ai.novel_analysis_orchestrator - INFO - [2/20] ✓ 分析完成: 第2章 修炼之路 (2.1秒)
2025-10-27 22:39:07,681 - app.services.redis_cache_service - INFO - ✓ 缓存命中: novel_analysis:micro:49b54fe9b9b...
2025-10-27 22:39:07,681 - app.services.ai.novel_micro_analysis - INFO - ⚡ 使用缓存结果: 7d502ad6-cb11-42e9-b5a6-02aa33a4adfe - 第4章 修炼之路
2025-10-27 22:39:07,681 - app.services.ai.novel_analysis_orchestrator - INFO - [4/20] ✓ 分析完成: 第4章 修炼之路 (2.0秒)
2025-10-27 22:39:07,681 - app.services.ai.novel_analysis_orchestrator - INFO - [6/20] 🔄 开始分析: 第6章 修炼之路
2025-10-27 22:39:07,683 - app.services.ai.novel_analysis_orchestrator - INFO - [7/20] 🔄 开始分析: 第7章 修炼之路
2025-10-27 22:39:07,683 - app.services.ai.novel_analysis_orchestrator - INFO - [8/20] 🔄 开始分析: 第8章 修炼之路
2025-10-27 22:39:07,683 - app.services.ai.novel_analysis_orchestrator - INFO - [9/20] 🔄 开始分析: 第9章 修炼之路
2025-10-27 22:39:07,683 - app.services.redis_cache_service - INFO - ✓ 缓存命中: novel_analysis:micro:7939c14c34a...
2025-10-27 22:39:07,685 - app.services.ai.novel_micro_analysis - INFO - ⚡ 使用缓存结果: 6c4da6db-4819-4003-84a4-319352f63b5e - 第1章 修炼之路
2025-10-27 22:39:07,685 - app.services.ai.novel_analysis_orchestrator - INFO - [1/20] ✓ 分析完成: 第1章 修炼之路 (2.1秒)
2025-10-27 22:39:07,685 - app.services.redis_cache_service - INFO - ✓ 缓存命中: novel_analysis:micro:3fe2a4255ec...
2025-10-27 22:39:07,685 - app.services.ai.novel_micro_analysis - INFO - ⚡ 使用缓存结果: e0e78085-852a-4285-b894-69cafb79265f - 第9章 修炼之路
2025-10-27 22:39:07,685 - app.services.ai.novel_analysis_orchestrator - INFO - [9/20] ✓ 分析完成: 第9章 修炼之路 (0.0秒)
2025-10-27 22:39:07,685 - app.services.redis_cache_service - INFO - ✓ 缓存命中: novel_analysis:micro:f97f4f1196d...
2025-10-27 22:39:07,685 - app.services.ai.novel_micro_analysis - INFO - ⚡ 使用缓存结果: 6848cf5c-2538-4569-ba99-d2c11a819495 - 第8章 修炼之路
2025-10-27 22:39:07,685 - app.services.ai.novel_analysis_orchestrator - INFO - [8/20] ✓ 分析完成: 第8章 修炼之路 (0.0秒)
2025-10-27 22:39:07,685 - app.services.redis_cache_service - INFO - ✓ 缓存命中: novel_analysis:micro:bba934595c4...
2025-10-27 22:39:07,685 - app.services.ai.novel_micro_analysis - INFO - ⚡ 使用缓存结果: 791bdf0c-3adb-40c8-bb05-120f492ee011 - 第7章 修炼之路
2025-10-27 22:39:07,685 - app.services.ai.novel_analysis_orchestrator - INFO - [7/20] ✓ 分析完成: 第7章 修炼之路 (0.0秒)
2025-10-27 22:39:07,685 - app.services.redis_cache_service - INFO - ✓ 缓存命中: novel_analysis:micro:aecef9f4c07...
2025-10-27 22:39:07,685 - app.services.ai.novel_micro_analysis - INFO - ⚡ 使用缓存结果: 8d2ed027-27bb-413d-b0f8-dab5b20e9969 - 第6章 修炼之路
2025-10-27 22:39:07,685 - app.services.ai.novel_analysis_orchestrator - INFO - [6/20] ✓ 分析完成: 第6章 修炼之路 (0.0秒)
2025-10-27 22:39:07,687 - app.services.ai.novel_analysis_orchestrator - INFO - [10/20] 🔄 开始分析: 第10章 修炼之路
2025-10-27 22:39:07,687 - app.services.ai.novel_analysis_orchestrator - INFO - [11/20] 🔄 开始分析: 第11章 修炼之路
2025-10-27 22:39:07,687 - app.services.ai.novel_analysis_orchestrator - INFO - [12/20] 🔄 开始分析: 第12章 修炼之路
2025-10-27 22:39:07,687 - app.services.ai.novel_analysis_orchestrator - INFO - [13/20] 🔄 开始分析: 第13章 修炼之路
2025-10-27 22:39:07,687 - app.services.ai.novel_analysis_orchestrator - INFO - [14/20] 🔄 开始分析: 第14章 修炼之路
2025-10-27 22:39:07,690 - app.services.redis_cache_service - INFO - ✓ 缓存命中: novel_analysis:micro:ee404f64e29...
2025-10-27 22:39:07,691 - app.services.ai.novel_micro_analysis - INFO - ⚡ 使用缓存结果: 281ea8a4-3a92-4cc9-91d4-3383688063bf - 第11章 修炼之路
2025-10-27 22:39:07,691 - app.services.ai.novel_analysis_orchestrator - INFO - [11/20] ✓ 分析完成: 第11章 修炼之路 (0.0秒)
2025-10-27 22:39:07,691 - app.services.ai.novel_analysis_orchestrator - INFO - 📊 进度更新: 10/20 章
2025-10-27 22:39:07,691 - app.services.redis_cache_service - INFO - ✓ 缓存命中: novel_analysis:micro:db2cd1858ff...
2025-10-27 22:39:07,691 - app.services.ai.novel_micro_analysis - INFO - ⚡ 使用缓存结果: a4902cfc-c29f-4a97-9b76-6e78e6d5022f - 第13章 修炼之路
2025-10-27 22:39:07,691 - app.services.ai.novel_analysis_orchestrator - INFO - [13/20] ✓ 分析完成: 第13章 修炼之路 (0.0秒)
2025-10-27 22:39:07,691 - app.services.redis_cache_service - INFO - ✓ 缓存命中: novel_analysis:micro:749f18af65e...
2025-10-27 22:39:07,691 - app.services.ai.novel_micro_analysis - INFO - ⚡ 使用缓存结果: 9bcf4602-97bf-4c2b-81a7-ea944827934f - 第10章 修炼之路
2025-10-27 22:39:07,691 - app.services.ai.novel_analysis_orchestrator - INFO - [10/20] ✓ 分析完成: 第10章 修炼之路 (0.0秒)
2025-10-27 22:39:07,691 - app.services.redis_cache_service - INFO - ✓ 缓存命中: novel_analysis:micro:99603843526...
2025-10-27 22:39:07,691 - app.services.ai.novel_micro_analysis - INFO - ⚡ 使用缓存结果: 78478422-2051-433a-b2ac-f6abe415222f - 第12章 修炼之路
2025-10-27 22:39:07,691 - app.services.ai.novel_analysis_orchestrator - INFO - [12/20] ✓ 分析完成: 第12章 修炼之路 (0.0秒)
2025-10-27 22:39:07,691 - app.services.ai.novel_analysis_orchestrator - INFO - [15/20] 🔄 开始分析: 第15章 修炼之路
2025-10-27 22:39:07,691 - app.services.ai.novel_analysis_orchestrator - INFO - [16/20] 🔄 开始分析: 第16章 修炼之路
2025-10-27 22:39:07,691 - app.services.ai.novel_analysis_orchestrator - INFO - [17/20] 🔄 开始分析: 第17章 修炼之路
2025-10-27 22:39:07,691 - app.services.ai.novel_analysis_orchestrator - INFO - [18/20] 🔄 开始分析: 第18章 修炼之路
2025-10-27 22:39:07,691 - app.services.redis_cache_service - INFO - ✓ 缓存命中: novel_analysis:micro:1f1e5685523...
2025-10-27 22:39:07,691 - app.services.ai.novel_micro_analysis - INFO - ⚡ 使用缓存结果: 197dd3bb-fc04-40aa-bdc1-054a6d99f8a0 - 第14章 修炼之路
2025-10-27 22:39:07,691 - app.services.ai.novel_analysis_orchestrator - INFO - [14/20] ✓ 分析完成: 第14章 修炼之路 (0.0秒)
2025-10-27 22:39:07,691 - app.services.ai.novel_analysis_orchestrator - INFO - [19/20] 🔄 开始分析: 第19章 修炼之路
2025-10-27 22:39:07,691 - app.services.redis_cache_service - INFO - ✓ 缓存命中: novel_analysis:micro:8d42e1c261e...
2025-10-27 22:39:07,691 - app.services.ai.novel_micro_analysis - INFO - ⚡ 使用缓存结果: c1642e9a-2c13-4a79-93cd-077a60356f14 - 第18章 修炼之路
2025-10-27 22:39:07,691 - app.services.ai.novel_analysis_orchestrator - INFO - [18/20] ✓ 分析完成: 第18章 修炼之路 (0.0秒)
2025-10-27 22:39:07,691 - app.services.redis_cache_service - INFO - ✓ 缓存命中: novel_analysis:micro:61467eb83d4...
2025-10-27 22:39:07,691 - app.services.ai.novel_micro_analysis - INFO - ⚡ 使用缓存结果: fbbdf7e1-7ece-4e5d-bff9-20a770b4477b - 第17章 修炼之路
2025-10-27 22:39:07,691 - app.services.ai.novel_analysis_orchestrator - INFO - [17/20] ✓ 分析完成: 第17章 修炼之路 (0.0秒)
2025-10-27 22:39:07,691 - app.services.redis_cache_service - INFO - ✓ 缓存命中: novel_analysis:micro:a1cdf20f896...
2025-10-27 22:39:07,691 - app.services.ai.novel_micro_analysis - INFO - ⚡ 使用缓存结果: e73d2886-817e-4eea-9c7f-02ce3f1f9f68 - 第16章 修炼之路
2025-10-27 22:39:07,691 - app.services.ai.novel_analysis_orchestrator - INFO - [16/20] ✓ 分析完成: 第16章 修炼之路 (0.0秒)
2025-10-27 22:39:07,691 - app.services.redis_cache_service - INFO - ✓ 缓存命中: novel_analysis:micro:e9394444736...
2025-10-27 22:39:07,691 - app.services.ai.novel_micro_analysis - INFO - ⚡ 使用缓存结果: 3c04f730-54b6-4b7d-832e-af1877d4be07 - 第15章 修炼之路
2025-10-27 22:39:07,691 - app.services.ai.novel_analysis_orchestrator - INFO - [15/20] ✓ 分析完成: 第15章 修炼之路 (0.0秒)
2025-10-27 22:39:07,691 - app.services.ai.novel_analysis_orchestrator - INFO - [20/20] 🔄 开始分析: 第20章 修炼之路
2025-10-27 22:39:07,691 - app.services.redis_cache_service - INFO - ✓ 缓存命中: novel_analysis:micro:99ed28183d8...
2025-10-27 22:39:07,691 - app.services.ai.novel_micro_analysis - INFO - ⚡ 使用缓存结果: 72d32a6c-c203-4739-9198-e07f29d9abd1 - 第19章 修炼之路
2025-10-27 22:39:07,691 - app.services.ai.novel_analysis_orchestrator - INFO - [19/20] ✓ 分析完成: 第19章 修炼之路 (0.0秒)
2025-10-27 22:39:07,691 - app.services.redis_cache_service - INFO - ✓ 缓存命中: novel_analysis:micro:2e6c60591db...
2025-10-27 22:39:07,691 - app.services.ai.novel_micro_analysis - INFO - ⚡ 使用缓存结果: 12c1cc22-0877-4ccb-b504-0ce4d92c7a4d - 第20章 修炼之路
2025-10-27 22:39:07,691 - app.services.ai.novel_analysis_orchestrator - INFO - [20/20] ✓ 分析完成: 第20章 修炼之路 (0.0秒)
2025-10-27 22:39:07,691 - app.services.ai.novel_analysis_orchestrator - INFO - 📊 进度更新: 20/20 章
2025-10-27 22:39:07,691 - app.services.ai.novel_analysis_orchestrator - INFO - ⚡ 并行分析完成: 成功 20/20 章
2025-10-27 22:39:07,691 - app.services.ai.novel_analysis_orchestrator - INFO - 💾 开始批量保存 20 个分析结果...
2025-10-27 22:39:07,708 - app.services.novel_analysis_service - INFO - Batch saved 20 micro results for analysis 8dea84ef-1098-4d8b-b0ca-8ac0d354eb4a, total: 20
2025-10-27 22:39:07,708 - app.services.ai.novel_analysis_orchestrator - INFO - ✅ 批量保存完成: 20 个结果
2025-10-27 22:39:07,710 - app.services.ai.novel_analysis_orchestrator - INFO - 🔍 开始批量存储向量...
2025-10-27 22:39:07,710 - app.services.vector_store_service - INFO - 开始向量化章节 6c4da6db-4819-4003-84a4-319352f63b5e 的微观分析数据
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 13.30it/s]
2025-10-27 22:39:07,787 - app.services.vector_store_service - INFO - 生成向量维度: 384
2025-10-27 22:39:07,800 - app.services.vector_store_service - INFO - 向量存储成功: vector_id=ed2d58c2-a7bd-4e39-82cc-7d98af9ae00b
2025-10-27 22:39:07,800 - app.services.vector_store_service - INFO - 开始向量化章节 bfe8ae0a-b7ed-450d-aa9e-b0a73ad3cdf1 的微观分析数据
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 21.12it/s]
2025-10-27 22:39:07,848 - app.services.vector_store_service - INFO - 生成向量维度: 384
2025-10-27 22:39:07,869 - app.services.vector_store_service - INFO - 向量存储成功: vector_id=17175bd1-c218-4859-b9d7-c557acb01a7d
2025-10-27 22:39:07,869 - app.services.vector_store_service - INFO - 开始向量化章节 b1e9f52a-ab87-45a0-b924-2a89c25bb74b 的微观分析数据
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 22.33it/s]
2025-10-27 22:39:07,917 - app.services.vector_store_service - INFO - 生成向量维度: 384
2025-10-27 22:39:07,929 - app.services.vector_store_service - INFO - 向量存储成功: vector_id=3a60ae44-8f40-4605-a03f-b567501bfb89
2025-10-27 22:39:07,929 - app.services.vector_store_service - INFO - 开始向量化章节 7d502ad6-cb11-42e9-b5a6-02aa33a4adfe 的微观分析数据
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 24.14it/s]
2025-10-27 22:39:07,973 - app.services.vector_store_service - INFO - 生成向量维度: 384
2025-10-27 22:39:07,973 - app.services.vector_store_service - INFO - 向量存储成功: vector_id=9414d649-8d21-48d7-b4d3-ec7ac8e45c2e
2025-10-27 22:39:07,973 - app.services.vector_store_service - INFO - 开始向量化章节 e8f60b96-fa2b-4ce4-8e3f-7e2863cafe32 的微观分析数据
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 15.73it/s]
2025-10-27 22:39:08,036 - app.services.vector_store_service - INFO - 生成向量维度: 384
2025-10-27 22:39:08,036 - app.services.vector_store_service - INFO - 向量存储成功: vector_id=674e3fce-ebd3-4357-b7cc-388f23bdb1d2
2025-10-27 22:39:08,036 - app.services.vector_store_service - INFO - 开始向量化章节 8d2ed027-27bb-413d-b0f8-dab5b20e9969 的微观分析数据
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 26.68it/s]
2025-10-27 22:39:08,083 - app.services.vector_store_service - INFO - 生成向量维度: 384
2025-10-27 22:39:08,098 - app.services.vector_store_service - INFO - 向量存储成功: vector_id=e0d103af-4c04-4788-86a2-5b6cdeb5008c
2025-10-27 22:39:08,098 - app.services.vector_store_service - INFO - 开始向量化章节 791bdf0c-3adb-40c8-bb05-120f492ee011 的微观分析数据
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 20.56it/s]
2025-10-27 22:39:08,151 - app.services.vector_store_service - INFO - 生成向量维度: 384
2025-10-27 22:39:08,157 - app.services.vector_store_service - INFO - 向量存储成功: vector_id=939e2329-e680-4507-8516-f048accca543
2025-10-27 22:39:08,157 - app.services.vector_store_service - INFO - 开始向量化章节 6848cf5c-2538-4569-ba99-d2c11a819495 的微观分析数据
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 17.24it/s]
2025-10-27 22:39:08,219 - app.services.vector_store_service - INFO - 生成向量维度: 384
2025-10-27 22:39:08,230 - app.services.vector_store_service - INFO - 向量存储成功: vector_id=1d4b5bc6-9e6d-4f81-9ed1-421c89b63ff2
2025-10-27 22:39:08,230 - app.services.vector_store_service - INFO - 开始向量化章节 e0e78085-852a-4285-b894-69cafb79265f 的微观分析数据
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 10.93it/s]
2025-10-27 22:39:08,322 - app.services.vector_store_service - INFO - 生成向量维度: 384
2025-10-27 22:39:08,322 - app.services.vector_store_service - INFO - 向量存储成功: vector_id=8649a4a3-0579-4a01-9c46-a0dd876e8dff
2025-10-27 22:39:08,322 - app.services.vector_store_service - INFO - 开始向量化章节 9bcf4602-97bf-4c2b-81a7-ea944827934f 的微观分析数据
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 11.68it/s]
2025-10-27 22:39:08,422 - app.services.vector_store_service - INFO - 生成向量维度: 384
2025-10-27 22:39:08,432 - app.services.vector_store_service - INFO - 向量存储成功: vector_id=571d7158-ab67-4820-8af3-13735b7c4c8d
2025-10-27 22:39:08,432 - app.services.vector_store_service - INFO - 开始向量化章节 281ea8a4-3a92-4cc9-91d4-3383688063bf 的微观分析数据
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 13.53it/s]
2025-10-27 22:39:08,511 - app.services.vector_store_service - INFO - 生成向量维度: 384
2025-10-27 22:39:08,527 - app.services.vector_store_service - INFO - 向量存储成功: vector_id=f03d44de-b1eb-478f-b9e9-f2f1a27d9762
2025-10-27 22:39:08,527 - app.services.vector_store_service - INFO - 开始向量化章节 78478422-2051-433a-b2ac-f6abe415222f 的微观分析数据
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 10.47it/s]
2025-10-27 22:39:08,622 - app.services.vector_store_service - INFO - 生成向量维度: 384
2025-10-27 22:39:08,634 - app.services.vector_store_service - INFO - 向量存储成功: vector_id=a70c5acf-6c4e-49b0-b1aa-17466b2a4be1
2025-10-27 22:39:08,634 - app.services.vector_store_service - INFO - 开始向量化章节 a4902cfc-c29f-4a97-9b76-6e78e6d5022f 的微观分析数据
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 11.95it/s]
2025-10-27 22:39:08,723 - app.services.vector_store_service - INFO - 生成向量维度: 384
2025-10-27 22:39:08,731 - app.services.vector_store_service - INFO - 向量存储成功: vector_id=f3cee9af-43fb-4587-91f6-289eab477cb4
2025-10-27 22:39:08,733 - app.services.vector_store_service - INFO - 开始向量化章节 197dd3bb-fc04-40aa-bdc1-054a6d99f8a0 的微观分析数据
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 11.06it/s]
2025-10-27 22:39:08,825 - app.services.vector_store_service - INFO - 生成向量维度: 384
2025-10-27 22:39:08,832 - app.services.vector_store_service - INFO - 向量存储成功: vector_id=a19671d1-d7b2-4507-b0d3-12bd0290555f
2025-10-27 22:39:08,832 - app.services.vector_store_service - INFO - 开始向量化章节 3c04f730-54b6-4b7d-832e-af1877d4be07 的微观分析数据
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 11.44it/s]
2025-10-27 22:39:08,925 - app.services.vector_store_service - INFO - 生成向量维度: 384
2025-10-27 22:39:08,935 - app.services.vector_store_service - INFO - 向量存储成功: vector_id=a5988532-1055-47f3-ba7b-240befd70876
2025-10-27 22:39:08,935 - app.services.vector_store_service - INFO - 开始向量化章节 e73d2886-817e-4eea-9c7f-02ce3f1f9f68 的微观分析数据
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 12.92it/s]
2025-10-27 22:39:09,017 - app.services.vector_store_service - INFO - 生成向量维度: 384
2025-10-27 22:39:09,033 - app.services.vector_store_service - INFO - 向量存储成功: vector_id=9def0fbe-1715-444c-b22c-3259ae527700
2025-10-27 22:39:09,033 - app.services.vector_store_service - INFO - 开始向量化章节 fbbdf7e1-7ece-4e5d-bff9-20a770b4477b 的微观分析数据
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  9.42it/s]
2025-10-27 22:39:09,141 - app.services.vector_store_service - INFO - 生成向量维度: 384
2025-10-27 22:39:09,150 - app.services.vector_store_service - INFO - 向量存储成功: vector_id=bb7435bc-7a0d-49fc-81ca-ab1e052d45a9
2025-10-27 22:39:09,150 - app.services.vector_store_service - INFO - 开始向量化章节 c1642e9a-2c13-4a79-93cd-077a60356f14 的微观分析数据
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 12.87it/s]
2025-10-27 22:39:09,235 - app.services.vector_store_service - INFO - 生成向量维度: 384
2025-10-27 22:39:09,250 - app.services.vector_store_service - INFO - 向量存储成功: vector_id=87202435-0135-478e-a548-f151d05bc15e
2025-10-27 22:39:09,252 - app.services.vector_store_service - INFO - 开始向量化章节 72d32a6c-c203-4739-9198-e07f29d9abd1 的微观分析数据
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 13.03it/s]
2025-10-27 22:39:09,329 - app.services.vector_store_service - INFO - 生成向量维度: 384
2025-10-27 22:39:09,347 - app.services.vector_store_service - INFO - 向量存储成功: vector_id=2ba4b7c4-829e-4880-aa88-0f1c061a11fe
2025-10-27 22:39:09,347 - app.services.vector_store_service - INFO - 开始向量化章节 12c1cc22-0877-4ccb-b504-0ce4d92c7a4d 的微观分析数据
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 11.96it/s]
2025-10-27 22:39:09,430 - app.services.vector_store_service - INFO - 生成向量维度: 384
2025-10-27 22:39:09,439 - app.services.vector_store_service - INFO - 向量存储成功: vector_id=e32766e4-f629-4742-b57d-828b2edef9e9
2025-10-27 22:39:09,440 - app.services.ai.novel_analysis_orchestrator - INFO - ✅ 批量向量存储完成
2025-10-27 22:39:09,440 - app.services.ai.novel_analysis_orchestrator - INFO - ============================================================
2025-10-27 22:39:09,440 - app.services.ai.novel_analysis_orchestrator - INFO - 微观分析完成统计:
2025-10-27 22:39:09,440 - app.services.ai.novel_analysis_orchestrator - INFO -   成功: 20/20 章节 (100.0%)
2025-10-27 22:39:09,440 - app.services.ai.novel_analysis_orchestrator - INFO -   失败: 0 章节
2025-10-27 22:39:09,440 - app.services.ai.novel_analysis_orchestrator - INFO -   总耗时: 5.8秒 (平均 0.3秒/章)
2025-10-27 22:39:09,440 - app.services.ai.novel_analysis_orchestrator - INFO - ============================================================
2025-10-27 22:39:09,452 - app.services.novel_analysis_service - INFO - Updated analysis 8dea84ef-1098-4d8b-b0ca-8ac0d354eb4a progress: 20/20, stage: AnalysisStage.MACRO_ANALYSIS, status: None
2025-10-27 22:39:09,452 - app.services.ai.novel_analysis_orchestrator - INFO - ============================================================
2025-10-27 22:39:09,454 - app.services.ai.novel_analysis_orchestrator - INFO - 开始宏观分析...
2025-10-27 22:39:09,454 - app.services.ai.novel_analysis_orchestrator - INFO - ============================================================
2025-10-27 22:39:09,455 - app.services.ai.novel_macro_analysis - INFO - 开始宏观分析，共 20 个章节的数据
2025-10-27 22:39:09,457 - app.services.ai.novel_macro_analysis - INFO - 第 1/3 次尝试调用AI宏观分析
2025-10-27 22:39:09,457 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=6000, temp=0.5
INFO:     127.0.0.1:55613 - "GET /api/v1/analysis/works/ddc0183e-76f5-4187-a491-9692a341996b HTTP/1.1" 200 OK
2025-10-27 22:39:14,147 - httpx - INFO - HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
2025-10-27 22:39:14,147 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
INFO:     127.0.0.1:53186 - "GET /api/v1/analysis/works/ddc0183e-76f5-4187-a491-9692a341996b HTTP/1.1" 200 OK
INFO:     127.0.0.1:60589 - "GET /api/v1/analysis/works/ddc0183e-76f5-4187-a491-9692a341996b HTTP/1.1" 200 OK
INFO:     127.0.0.1:61617 - "GET /api/v1/analysis/works/ddc0183e-76f5-4187-a491-9692a341996b HTTP/1.1" 200 OK
INFO:     127.0.0.1:59667 - "GET /api/v1/analysis/works/ddc0183e-76f5-4187-a491-9692a341996b HTTP/1.1" 200 OK
INFO:     127.0.0.1:57815 - "GET /api/v1/analysis/works/ddc0183e-76f5-4187-a491-9692a341996b HTTP/1.1" 200 OK
INFO:     127.0.0.1:61664 - "GET /api/v1/analysis/works/ddc0183e-76f5-4187-a491-9692a341996b HTTP/1.1" 200 OK
INFO:     127.0.0.1:62713 - "GET /api/v1/analysis/works/ddc0183e-76f5-4187-a491-9692a341996b HTTP/1.1" 200 OK
INFO:     127.0.0.1:49438 - "GET /api/v1/analysis/works/ddc0183e-76f5-4187-a491-9692a341996b HTTP/1.1" 200 OK
2025-10-27 22:39:54,549 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 19 个数据块，总长度: 1788
2025-10-27 22:39:54,550 - app.services.ai.novel_macro_analysis - INFO - 宏观分析完成，报告长度: 1788 字符
2025-10-27 22:39:54,550 - app.services.ai.novel_analysis_orchestrator - INFO - 宏观分析完成，报告长度: 1788 字符，耗时: 45.1秒
2025-10-27 22:39:54,551 - app.services.novel_analysis_service - INFO - Saved macro result for analysis 8dea84ef-1098-4d8b-b0ca-8ac0d354eb4a, marked as completed
2025-10-27 22:39:54,551 - app.services.ai.novel_analysis_orchestrator - INFO - ============================================================
2025-10-27 22:39:54,551 - app.services.ai.novel_analysis_orchestrator - INFO - 作品 ddc0183e-76f5-4187-a491-9692a341996b 分析全部完成！
2025-10-27 22:39:54,551 - app.services.ai.novel_analysis_orchestrator - INFO - ============================================================
2025-10-27 22:39:54,551 - app.services.ai.novel_analysis_orchestrator - INFO - 📊 分析统计:
2025-10-27 22:39:54,551 - app.services.ai.novel_analysis_orchestrator - INFO -   微观分析: 20/20 章 (成功率 100.0%)
2025-10-27 22:39:54,551 - app.services.ai.novel_analysis_orchestrator - INFO -   宏观报告: 1788 字符
2025-10-27 22:39:54,551 - app.services.ai.novel_analysis_orchestrator - INFO -   总耗时: 50.9秒 (0.8分钟)
2025-10-27 22:39:54,551 - app.services.ai.novel_analysis_orchestrator - INFO -   平均速度: 2.5秒/章
2025-10-27 22:39:54,551 - app.services.ai.novel_analysis_orchestrator - INFO -   向量存储: 20 条，覆盖 20 章
2025-10-27 22:39:54,551 - app.services.ai.novel_analysis_orchestrator - INFO - ============================================================
2025-10-27 22:39:54,551 - app.services.ai.novel_analysis_orchestrator - INFO - AI服务资源已清理
2025-10-27 22:39:54,551 - app.services.ai.novel_analysis_orchestrator - INFO - AI服务资源已清理
2025-10-27 22:39:54,551 - app.api.v1.novel_analysis - INFO - 后台任务完成：作品 ddc0183e-76f5-4187-a491-9692a341996b 分析成功
INFO:     127.0.0.1:54328 - "GET /api/v1/analysis/works/ddc0183e-76f5-4187-a491-9692a341996b HTTP/1.1" 200 OK
