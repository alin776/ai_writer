(venv) PS D:\Java\ai_writer\backend> python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
INFO:     Will watch for changes in these directories: ['D:\\Java\\ai_writer\\backend']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [35408] using WatchFiles
已注册策略: web_novel_11d - 网文11维度分析
INFO:     Started server process [36840]
INFO:     Waiting for application startup.
2025-10-28 15:47:26,103 - app.main - INFO - 🚀 应用启动中...
2025-10-28 15:47:26,103 - app.core.database - INFO - 正在初始化数据库... (尝试 1/3)
2025-10-28 15:47:26,316 - app.core.database - INFO - ✅ 数据库初始化成功
2025-10-28 15:47:26,316 - apscheduler.scheduler - INFO - Adding job tentatively -- it will be properly scheduled when the scheduler starts
2025-10-28 15:47:26,322 - apscheduler.scheduler - INFO - Added job "清理过期的去痕迹会话详情" to job store "default"
2025-10-28 15:47:26,322 - apscheduler.scheduler - INFO - Scheduler started
2025-10-28 15:47:26,323 - app.tasks.cleanup_humanize_details - INFO - 定时任务调度器已启动
2025-10-28 15:47:26,323 - app.main - INFO - 🔄 开始预加载Embedding模型...
2025-10-28 15:47:26,324 - app.services.vector_store_service - INFO - 🔄 预加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
2025-10-28 15:47:26,326 - sentence_transformers.SentenceTransformer - INFO - Use pytorch device_name: cpu
2025-10-28 15:47:26,326 - sentence_transformers.SentenceTransformer - INFO - Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
2025-10-28 15:47:36,166 - app.services.vector_store_service - INFO - ✅ Embedding模型预加载成功，耗时: 9.84秒
2025-10-28 15:47:36,168 - app.main - INFO - ✅ Embedding模型预加载完成
2025-10-28 15:47:36,168 - app.main - INFO - ✅ 应用启动完成
INFO:     Application startup complete.
INFO:     127.0.0.1:55997 - "POST /api/v1/auth/login HTTP/1.1" 200 OK
2025-10-28 15:48:13,926 - app.services.ai.prompts - INFO - Prompts loaded successfully from D:\Java\ai_writer\backend\app\services\ai\prompts\default.json
2025-10-28 15:48:14,559 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: qwen3-32b, Timeout: 60s
INFO:     127.0.0.1:56000 - "POST /api/v1/books/upload HTTP/1.1" 200 OK
2025-10-28 15:48:14,606 - app.api.v1.endpoints.books - INFO - 🚀 开始执行后台分析任务: job_id=ae8288d2-2c18-4a95-938a-703be6360e7a, user_id=602f5147-846a-4cde-95d3-405fa75f133f
2025-10-28 15:48:14,606 - app.api.v1.endpoints.books - INFO - ✅ 数据库会话创建成功
2025-10-28 15:48:15,350 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: qwen3-32b, Timeout: 60s
2025-10-28 15:48:15,351 - app.api.v1.endpoints.books - INFO - ✅ AI服务初始化成功
2025-10-28 15:48:15,351 - app.api.v1.endpoints.books - INFO - ✅ 知识库服务初始化成功
2025-10-28 15:48:15,351 - app.api.v1.endpoints.books - INFO - ✅ 图书分析服务初始化成功,开始分析...
2025-10-28 15:48:15,351 - app.services.book_analysis_service - INFO - 📖 analyze_book 开始: job_id=ae8288d2-2c18-4a95-938a-703be6360e7a, user_id=602f5147-846a-4cde-95d3-405fa75f133f
2025-10-28 15:48:15,382 - app.services.book_analysis_service - INFO - ✅ 获取到任务: test_cache_v1_1761637693.txt, file_path=uploads\books\5e6b6176-508b-460f-9fd5-8931ce8f33ba.txt
2025-10-28 15:48:15,388 - app.services.book_analysis_service - INFO - 📄 开始解析文件: uploads\books\5e6b6176-508b-460f-9fd5-8931ce8f33ba.txt
2025-10-28 15:48:15,388 - app.services.book_analysis.smart_sampling - INFO - 🔍 准备解析文件: uploads\books\5e6b6176-508b-460f-9fd5-8931ce8f33ba.txt
2025-10-28 15:48:15,388 - app.services.book_analysis.smart_sampling - INFO - 📁 文件是否存在: True
2025-10-28 15:48:15,390 - app.services.book_analysis.smart_sampling - INFO - 📏 文件大小: 1132 字节
2025-10-28 15:48:15,390 - app.services.book_analysis.smart_sampling - INFO - 📖 读取内容长度: 460 字符
2025-10-28 15:48:15,390 - app.services.book_analysis.smart_sampling - INFO - 📝 内容前200字符: [测试版本: v1 | 时间戳: 1761637693 | ID: 0]

第一章 测试章节

这是一个用于测试Redis缓存的章节内容。

林逸站在窗前,望着远方的天空。

"这一世,我一定要改变命运!"他暗暗发誓。

【系统提示: 检测到主角决心值+10】

第二章 系统觉醒

就在这时,脑海中响起了机械音。

【叮!美食评鉴系统已激活】

林逸愣住了,这是......金手指?

【系统功能说
2025-10-28 15:48:15,390 - app.services.book_analysis.smart_sampling - INFO - 🔎 正则匹配结果: 找到 3 个章节标题
2025-10-28 15:48:15,392 - app.services.book_analysis.smart_sampling - INFO -   匹配1: '第一章 测试章节' at position 38
2025-10-28 15:48:15,392 - app.services.book_analysis.smart_sampling - INFO -   匹配2: '第二章 系统觉醒' at position 132
2025-10-28 15:48:15,392 - app.services.book_analysis.smart_sampling - INFO -   匹配3: '第三章 初试锋芒' at position 274
2025-10-28 15:48:15,392 - app.services.book_analysis.smart_sampling - INFO -   ⏭️ 跳过章节 '第一章 测试章节': 长度82字符 < 最小长度100
2025-10-28 15:48:15,392 - app.services.book_analysis.smart_sampling - INFO -   ✅ 保留章节 '第二章 系统觉醒': 130字符
2025-10-28 15:48:15,392 - app.services.book_analysis.smart_sampling - INFO -   ✅ 保留章节 '第三章 初试锋芒': 175字符
2025-10-28 15:48:15,392 - app.services.book_analysis.smart_sampling - INFO - ✨ 最终保留 2 个有效章节
2025-10-28 15:48:15,394 - app.services.book_analysis_service - INFO - 📊 解析完成,识别到 2 个章节
2025-10-28 15:48:15,394 - app.services.book_analysis_service - INFO -   章节1: 第二章 系统觉醒 (130字)
2025-10-28 15:48:15,394 - app.services.book_analysis_service - INFO -   章节2: 第三章 初试锋芒 (175字)
2025-10-28 15:48:15,403 - app.services.book_analysis_service - INFO - 📊 开始分析 2 个章节: 2个深度分析(串行), 0个增量分析(并行)
2025-10-28 15:48:15,441 - app.services.book_analysis_service - INFO - 🔍 深度分析章节 1: 第二章 系统觉醒
INFO:     127.0.0.1:56003 - "GET /api/v1/books/jobs/ae8288d2-2c18-4a95-938a-703be6360e7a/status HTTP/1.1" 200 OK
2025-10-28 15:48:17,483 - app.services.redis_cache_service - INFO - ✓ Redis连接成功 (timeout=10s, retry=enabled, pool=50)
2025-10-28 15:48:17,484 - app.services.book_analysis_service - INFO - ✅ Redis缓存服务初始化成功
2025-10-28 15:48:17,485 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=3000, temp=0.3, 尝试=1/3
INFO:     127.0.0.1:58823 - "GET /api/v1/books/jobs/ae8288d2-2c18-4a95-938a-703be6360e7a/status HTTP/1.1" 200 OK
INFO:     127.0.0.1:63964 - "GET /api/v1/books/jobs/ae8288d2-2c18-4a95-938a-703be6360e7a/status HTTP/1.1" 200 OK
INFO:     127.0.0.1:63967 - "GET /api/v1/books/jobs/ae8288d2-2c18-4a95-938a-703be6360e7a/status HTTP/1.1" 200 OK
INFO:     127.0.0.1:64936 - "GET /api/v1/books/jobs/ae8288d2-2c18-4a95-938a-703be6360e7a/status HTTP/1.1" 200 OK
INFO:     127.0.0.1:64124 - "GET /api/v1/books/jobs/ae8288d2-2c18-4a95-938a-703be6360e7a/status HTTP/1.1" 200 OK
INFO:     127.0.0.1:64127 - "GET /api/v1/books/jobs/ae8288d2-2c18-4a95-938a-703be6360e7a/status HTTP/1.1" 200 OK
INFO:     127.0.0.1:64130 - "GET /api/v1/books/jobs/ae8288d2-2c18-4a95-938a-703be6360e7a/status HTTP/1.1" 200 OK
INFO:     127.0.0.1:64133 - "GET /api/v1/books/jobs/ae8288d2-2c18-4a95-938a-703be6360e7a/status HTTP/1.1" 200 OK
INFO:     127.0.0.1:64136 - "GET /api/v1/books/jobs/ae8288d2-2c18-4a95-938a-703be6360e7a/status HTTP/1.1" 200 OK
INFO:     127.0.0.1:64139 - "GET /api/v1/books/jobs/ae8288d2-2c18-4a95-938a-703be6360e7a/status HTTP/1.1" 200 OK
2025-10-28 15:48:37,668 - httpx - INFO - HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
2025-10-28 15:48:37,668 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=3296, 尝试次数=1
2025-10-28 15:48:37,668 - app.services.book_analysis_service - INFO - 💾 AI响应已保存到: D:\Java\ai_writer\backend\debug_ai_responses\ch1_第二章 系统觉醒.txt
2025-10-28 15:48:37,668 - app.services.book_analysis.web_novel_strategy - INFO - 🔍 开始解析AI响应,长度=3296
2025-10-28 15:48:37,668 - app.services.book_analysis.web_novel_strategy - INFO - ✅ 预处理: 已替换中文标点符号
2025-10-28 15:48:37,675 - app.services.book_analysis.web_novel_strategy - INFO - ✅ 直接解析JSON成功
2025-10-28 15:48:37,675 - app.services.book_analysis_service - INFO - ✅ 章节1 '第二章 系统觉醒' 分析成功,获得 11 个维度
2025-10-28 15:48:37,675 - app.services.redis_cache_service - INFO - ✓ 结果已缓存: novel_analysis:v2:book_breakdown... (TTL: 604800秒)
INFO:     127.0.0.1:55448 - "GET /api/v1/books/jobs/ae8288d2-2c18-4a95-938a-703be6360e7a/status HTTP/1.1" 200 OK
2025-10-28 15:48:38,183 - app.services.book_analysis_service - INFO - 🔍 深度分析章节 2: 第三章 初试锋芒
2025-10-28 15:48:38,183 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=3000, temp=0.3, 尝试=1/3
INFO:     127.0.0.1:56462 - "GET /api/v1/books/jobs/ae8288d2-2c18-4a95-938a-703be6360e7a/status HTTP/1.1" 200 OK
INFO:     127.0.0.1:56465 - "GET /api/v1/books/jobs/ae8288d2-2c18-4a95-938a-703be6360e7a/status HTTP/1.1" 200 OK
INFO:     127.0.0.1:56468 - "GET /api/v1/books/jobs/ae8288d2-2c18-4a95-938a-703be6360e7a/status HTTP/1.1" 200 OK
INFO:     127.0.0.1:59396 - "GET /api/v1/books/jobs/ae8288d2-2c18-4a95-938a-703be6360e7a/status HTTP/1.1" 200 OK
INFO:     127.0.0.1:59421 - "GET /api/v1/books/jobs/ae8288d2-2c18-4a95-938a-703be6360e7a/status HTTP/1.1" 200 OK
INFO:     127.0.0.1:58514 - "GET /api/v1/books/jobs/ae8288d2-2c18-4a95-938a-703be6360e7a/status HTTP/1.1" 200 OK
INFO:     127.0.0.1:61646 - "GET /api/v1/books/jobs/ae8288d2-2c18-4a95-938a-703be6360e7a/status HTTP/1.1" 200 OK
INFO:     127.0.0.1:55890 - "GET /api/v1/books/jobs/ae8288d2-2c18-4a95-938a-703be6360e7a/status HTTP/1.1" 200 OK
INFO:     127.0.0.1:55893 - "GET /api/v1/books/jobs/ae8288d2-2c18-4a95-938a-703be6360e7a/status HTTP/1.1" 200 OK
INFO:     127.0.0.1:55484 - "GET /api/v1/books/jobs/ae8288d2-2c18-4a95-938a-703be6360e7a/status HTTP/1.1" 200 OK
2025-10-28 15:48:58,422 - httpx - INFO - HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
2025-10-28 15:48:58,422 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=3630, 尝试次数=1
2025-10-28 15:48:58,425 - app.services.book_analysis_service - INFO - 💾 AI响应已保存到: D:\Java\ai_writer\backend\debug_ai_responses\ch2_第三章 初试锋芒.txt
2025-10-28 15:48:58,425 - app.services.book_analysis.web_novel_strategy - INFO - 🔍 开始解析AI响应,长度=3630
2025-10-28 15:48:58,425 - app.services.book_analysis.web_novel_strategy - INFO - ✅ 预处理: 已替换中文标点符号
2025-10-28 15:48:58,425 - app.services.book_analysis.web_novel_strategy - INFO - ✅ 直接解析JSON成功
2025-10-28 15:48:58,425 - app.services.book_analysis_service - INFO - ✅ 章节2 '第三章 初试锋芒' 分析成功,获得 11 个维度
2025-10-28 15:48:58,427 - app.services.redis_cache_service - INFO - ✓ 结果已缓存: novel_analysis:v2:book_breakdown... (TTL: 604800秒)
2025-10-28 15:48:58,926 - app.services.book_analysis_service - INFO - ✅ 深度分析完成, 建立了 11 个维度的基础
2025-10-28 15:48:58,926 - app.services.book_analysis_service - INFO - 📊 章节分析全部完成, 共11个维度
2025-10-28 15:48:58,926 - app.services.book_analysis_service - INFO - 📚 开始提取知识点,共 11 个维度
2025-10-28 15:48:58,926 - app.services.book_analysis_service - INFO -   - 维度 'core_selling_point': dimension_type=technique
2025-10-28 15:48:58,928 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 核心卖点 (类别: technique)
2025-10-28 15:48:58,928 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=💡 核心卖点
2025-10-28 15:48:58,960 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=25ae6f29-bc1f-425e-a6c8-2fe8a1841a80
2025-10-28 15:48:58,960 - app.services.book_analysis_service - INFO -   - 维度 'protagonist_setting': dimension_type=character_template
2025-10-28 15:48:58,960 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 主角设定 (类别: character)
2025-10-28 15:48:58,960 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=👤 主角设定
2025-10-28 15:48:58,975 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=4a4e17ba-2236-45e4-b850-70f0da20646e
2025-10-28 15:48:58,975 - app.services.book_analysis_service - INFO -   - 维度 'cheat_system': dimension_type=power_system
2025-10-28 15:48:58,975 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 金手指系统 (类别: worldview)
2025-10-28 15:48:58,975 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=🌍 金手指系统
2025-10-28 15:48:58,984 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=b8bd79a6-62b0-407b-8b66-7bd0d0421f5b
2025-10-28 15:48:58,984 - app.services.book_analysis_service - INFO -   - 维度 'world_framework': dimension_type=setting
2025-10-28 15:48:58,984 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 世界观框架 (类别: worldview)
2025-10-28 15:48:58,984 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=🌍 世界观框架
2025-10-28 15:48:58,987 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=bdfb5554-85af-4d32-bb13-9b120b8c851b
2025-10-28 15:48:58,990 - app.services.book_analysis_service - INFO -   - 维度 'power_system': dimension_type=power_system
2025-10-28 15:48:58,990 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 等级力量体系 (类别: worldview)
2025-10-28 15:48:58,990 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=🌍 等级力量体系
2025-10-28 15:48:58,991 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=38e05a99-0c82-41aa-a4ff-fcb259d67429
2025-10-28 15:48:58,991 - app.services.book_analysis_service - INFO -   - 维度 'antagonist_forces': dimension_type=character_template
2025-10-28 15:48:58,991 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 反派势力 (类别: character)
2025-10-28 15:48:58,991 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=👤 反派势力
2025-10-28 15:48:58,991 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=6746678a-4e07-41a4-b4fa-a0cb154d3631
2025-10-28 15:48:58,991 - app.services.book_analysis_service - INFO -   - 维度 'romance_line': dimension_type=relationship
2025-10-28 15:48:58,991 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 情感线设定 (类别: plot)
2025-10-28 15:48:58,991 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=📖 情感线设定
2025-10-28 15:48:59,012 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=f17288bc-73c8-477e-8346-400878246f56
2025-10-28 15:48:59,012 - app.services.book_analysis_service - INFO -   - 维度 'satisfaction_points': dimension_type=technique
2025-10-28 15:48:59,012 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 爽点布局 (类别: technique)
2025-10-28 15:48:59,012 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=💡 爽点布局
2025-10-28 15:48:59,018 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=ac1fdeba-08ba-4c68-b3c6-26780ea23bcb
2025-10-28 15:48:59,019 - app.services.book_analysis_service - INFO -   - 维度 'anticipation_hooks': dimension_type=technique
2025-10-28 15:48:59,019 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 期待感钩子 (类别: technique)
2025-10-28 15:48:59,019 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=💡 期待感钩子
2025-10-28 15:48:59,026 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=add443fc-d645-4a3c-98b9-89f9fcdbed5e
2025-10-28 15:48:59,026 - app.services.book_analysis_service - INFO -   - 维度 'sub_plots': dimension_type=plot_structure
2025-10-28 15:48:59,026 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 支线剧情 (类别: plot)
2025-10-28 15:48:59,028 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=📖 支线剧情
2025-10-28 15:48:59,034 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=576e7bc2-c4c7-4963-93b4-6afc0e14f6fb
2025-10-28 15:48:59,034 - app.services.book_analysis_service - INFO -   - 维度 'unique_features': dimension_type=technique
2025-10-28 15:48:59,035 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 特色设定 (类别: technique)
2025-10-28 15:48:59,035 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=💡 特色设定
2025-10-28 15:48:59,043 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=971051bf-e4b6-4062-96d7-a2dfda08afe9
2025-10-28 15:48:59,043 - app.services.book_analysis_service - INFO - 🚀 开始批量向量化 11 个知识条目...
2025-10-28 15:48:59,043 - app.services.vector_store_service - INFO - 🚀 开始批量向量化 11 个知识条目
2025-10-28 15:48:59,047 - app.services.vector_store_service - INFO - 🔄 缓存未命中,计算全部 11 个向量
Batches: 100%|█████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  3.68it/s]
2025-10-28 15:48:59,337 - app.services.redis_cache_service - INFO - ✓ 向量缓存成功: 11 个向量 (TTL: 604800秒)
2025-10-28 15:48:59,401 - app.services.vector_store_service - INFO - ✅ 批量向量化完成: 11个条目, 耗时: 0.36秒
2025-10-28 15:48:59,401 - app.services.book_analysis_service - INFO - ✅ 批量向量化成功
2025-10-28 15:48:59,401 - app.services.book_analysis_service - INFO - 📚 知识点提取完成,共创建 11 个知识条目
2025-10-28 15:48:59,401 - app.services.book_analysis_service - INFO -    - 相比旧策略,覆盖率提升: 从2个类型扩展到所有维度
2025-10-28 15:48:59,401 - app.services.book_analysis_service - INFO - 💡 开始生成智能建议,共 11 个维度
2025-10-28 15:48:59,401 - app.services.book_analysis.suggestion_generator - INFO - 🎯 开始生成建议,共 11 个维度
2025-10-28 15:48:59,401 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'core_selling_point': dimension_type=technique
2025-10-28 15:48:59,401 - app.services.book_analysis.suggestion_generator - INFO -     ❌ 维度类型不可关联,跳过
2025-10-28 15:48:59,401 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'protagonist_setting': dimension_type=character_template
2025-10-28 15:48:59,401 - app.services.book_analysis.suggestion_generator - INFO -     ✅ 创建建议: character, 置信度=0.75
2025-10-28 15:48:59,401 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'cheat_system': dimension_type=power_system
2025-10-28 15:48:59,401 - app.services.book_analysis.suggestion_generator - INFO -     ✅ 创建建议: power_system, 置信度=0.75
2025-10-28 15:48:59,401 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'world_framework': dimension_type=setting
2025-10-28 15:48:59,401 - app.services.book_analysis.suggestion_generator - INFO -     ✅ 创建建议: setting, 置信度=0.60
2025-10-28 15:48:59,401 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'power_system': dimension_type=power_system
2025-10-28 15:48:59,401 - app.services.book_analysis.suggestion_generator - INFO -     ✅ 创建建议: power_system, 置信度=0.65
2025-10-28 15:48:59,401 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'antagonist_forces': dimension_type=character_template
2025-10-28 15:48:59,401 - app.services.book_analysis.suggestion_generator - INFO -     ✅ 创建建议: character, 置信度=0.65
2025-10-28 15:48:59,401 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'romance_line': dimension_type=relationship
2025-10-28 15:48:59,401 - app.services.book_analysis.suggestion_generator - INFO -     ✅ 创建建议: relationship, 置信度=0.60
2025-10-28 15:48:59,401 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'satisfaction_points': dimension_type=technique
2025-10-28 15:48:59,401 - app.services.book_analysis.suggestion_generator - INFO -     ❌ 维度类型不可关联,跳过
2025-10-28 15:48:59,401 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'anticipation_hooks': dimension_type=technique
2025-10-28 15:48:59,401 - app.services.book_analysis.suggestion_generator - INFO -     ❌ 维度类型不可关联,跳过
2025-10-28 15:48:59,401 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'sub_plots': dimension_type=plot_structure
2025-10-28 15:48:59,401 - app.services.book_analysis.suggestion_generator - INFO -     ❌ 维度类型不可关联,跳过
2025-10-28 15:48:59,401 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'unique_features': dimension_type=technique
2025-10-28 15:48:59,401 - app.services.book_analysis.suggestion_generator - INFO -     ❌ 维度类型不可关联,跳过
2025-10-28 15:48:59,401 - app.services.book_analysis.suggestion_generator - INFO - 🎯 建议生成完成,共 6 个
2025-10-28 15:48:59,401 - app.services.book_analysis_service - INFO - 💡 建议生成器返回 6 个建议
2025-10-28 15:48:59,422 - app.services.book_analysis_service - INFO - 💡 智能建议生成完成,共创建 6 个建议
2025-10-28 15:48:59,444 - app.services.redis_cache_service - INFO -
📊 缓存统计:
  - 总请求: 13
  - 命中: 0
  - 未命中: 13
  - 错误: 0
  - 命中率: 0.0%
  - 节省时间: 0.0秒

2025-10-28 15:48:59,444 - app.api.v1.endpoints.books - INFO - 🎉 图书分析任务完成: job_id=ae8288d2-2c18-4a95-938a-703be6360e7a
INFO:     127.0.0.1:55487 - "GET /api/v1/books/jobs/ae8288d2-2c18-4a95-938a-703be6360e7a/status HTTP/1.1" 200 OK
2025-10-28 15:49:00,503 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: qwen3-32b, Timeout: 60s
INFO:     127.0.0.1:55490 - "POST /api/v1/books/upload HTTP/1.1" 200 OK
2025-10-28 15:49:00,515 - app.api.v1.endpoints.books - INFO - 🚀 开始执行后台分析任务: job_id=20a4260a-09c6-4b00-8ebe-045ab62f7b41, user_id=602f5147-846a-4cde-95d3-405fa75f133f
2025-10-28 15:49:00,517 - app.api.v1.endpoints.books - INFO - ✅ 数据库会话创建成功
2025-10-28 15:49:01,183 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: qwen3-32b, Timeout: 60s
2025-10-28 15:49:01,183 - app.api.v1.endpoints.books - INFO - ✅ AI服务初始化成功
2025-10-28 15:49:01,183 - app.api.v1.endpoints.books - INFO - ✅ 知识库服务初始化成功
2025-10-28 15:49:01,185 - app.api.v1.endpoints.books - INFO - ✅ 图书分析服务初始化成功,开始分析...
2025-10-28 15:49:01,185 - app.services.book_analysis_service - INFO - 📖 analyze_book 开始: job_id=20a4260a-09c6-4b00-8ebe-045ab62f7b41, user_id=602f5147-846a-4cde-95d3-405fa75f133f
2025-10-28 15:49:01,188 - app.services.book_analysis_service - INFO - ✅ 获取到任务: test_cache_v1_1761637693.txt, file_path=uploads\books\1df29960-b501-4ece-a724-225b59906d7e.txt
INFO:     127.0.0.1:50632 - "GET /api/v1/books/jobs/20a4260a-09c6-4b00-8ebe-045ab62f7b41/status HTTP/1.1" 200 OK
2025-10-28 15:49:01,198 - app.services.book_analysis_service - INFO - 📄 开始解析文件: uploads\books\1df29960-b501-4ece-a724-225b59906d7e.txt
2025-10-28 15:49:01,198 - app.services.book_analysis.smart_sampling - INFO - 🔍 准备解析文件: uploads\books\1df29960-b501-4ece-a724-225b59906d7e.txt
2025-10-28 15:49:01,199 - app.services.book_analysis.smart_sampling - INFO - 📁 文件是否存在: True
2025-10-28 15:49:01,199 - app.services.book_analysis.smart_sampling - INFO - 📏 文件大小: 1132 字节
2025-10-28 15:49:01,199 - app.services.book_analysis.smart_sampling - INFO - 📖 读取内容长度: 460 字符
2025-10-28 15:49:01,199 - app.services.book_analysis.smart_sampling - INFO - 📝 内容前200字符: [测试版本: v1 | 时间戳: 1761637693 | ID: 1]

第一章 测试章节

这是一个用于测试Redis缓存的章节内容。

林逸站在窗前,望着远方的天空。

"这一世,我一定要改变命运!"他暗暗发誓。

【系统提示: 检测到主角决心值+10】

第二章 系统觉醒

就在这时,脑海中响起了机械音。

【叮!美食评鉴系统已激活】

林逸愣住了,这是......金手指?

【系统功能说
2025-10-28 15:49:01,199 - app.services.book_analysis.smart_sampling - INFO - 🔎 正则匹配结果: 找到 3 个章节标题
2025-10-28 15:49:01,201 - app.services.book_analysis.smart_sampling - INFO -   匹配1: '第一章 测试章节' at position 38
2025-10-28 15:49:01,201 - app.services.book_analysis.smart_sampling - INFO -   匹配2: '第二章 系统觉醒' at position 132
2025-10-28 15:49:01,201 - app.services.book_analysis.smart_sampling - INFO -   匹配3: '第三章 初试锋芒' at position 274
2025-10-28 15:49:01,201 - app.services.book_analysis.smart_sampling - INFO -   ⏭️ 跳过章节 '第一章 测试章节': 长度82字符 < 最小长度100
2025-10-28 15:49:01,201 - app.services.book_analysis.smart_sampling - INFO -   ✅ 保留章节 '第二章 系统觉醒': 130字符
2025-10-28 15:49:01,201 - app.services.book_analysis.smart_sampling - INFO -   ✅ 保留章节 '第三章 初试锋芒': 175字符
2025-10-28 15:49:01,201 - app.services.book_analysis.smart_sampling - INFO - ✨ 最终保留 2 个有效章节
2025-10-28 15:49:01,202 - app.services.book_analysis_service - INFO - 📊 解析完成,识别到 2 个章节
2025-10-28 15:49:01,202 - app.services.book_analysis_service - INFO -   章节1: 第二章 系统觉醒 (130字)
2025-10-28 15:49:01,202 - app.services.book_analysis_service - INFO -   章节2: 第三章 初试锋芒 (175字)
2025-10-28 15:49:01,215 - app.services.book_analysis_service - INFO - 📊 开始分析 2 个章节: 2个深度分析(串行), 0个增量分析(并行)
2025-10-28 15:49:01,220 - app.services.book_analysis_service - INFO - 🔍 深度分析章节 1: 第二章 系统觉醒
2025-10-28 15:49:01,220 - app.services.book_analysis_service - INFO - ✅ Redis缓存服务初始化成功
2025-10-28 15:49:01,223 - app.services.redis_cache_service - INFO - ✓ 缓存命中: novel_analysis:v2:book_breakdown...
2025-10-28 15:49:01,223 - app.services.book_analysis_service - INFO - ✅ 缓存命中! 章节1 '第二章 系统觉醒' (跳过AI调用)
2025-10-28 15:49:01,725 - app.services.book_analysis_service - INFO - 🔍 深度分析章节 2: 第三章 初试锋芒
2025-10-28 15:49:01,725 - app.services.redis_cache_service - INFO - ✓ 缓存命中: novel_analysis:v2:book_breakdown...
2025-10-28 15:49:01,725 - app.services.book_analysis_service - INFO - ✅ 缓存命中! 章节2 '第三章 初试锋芒' (跳过AI调用)
2025-10-28 15:49:02,229 - app.services.book_analysis_service - INFO - ✅ 深度分析完成, 建立了 11 个维度的基础
2025-10-28 15:49:02,230 - app.services.book_analysis_service - INFO - 📊 章节分析全部完成, 共11个维度
2025-10-28 15:49:02,230 - app.services.book_analysis_service - INFO - 📚 开始提取知识点,共 11 个维度
2025-10-28 15:49:02,231 - app.services.book_analysis_service - INFO -   - 维度 'core_selling_point': dimension_type=technique
2025-10-28 15:49:02,231 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 核心卖点 (类别: technique)
2025-10-28 15:49:02,232 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=💡 核心卖点
2025-10-28 15:49:02,233 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=b30331fb-3a8a-48b7-9954-679df9d7dabc
2025-10-28 15:49:02,233 - app.services.book_analysis_service - INFO -   - 维度 'protagonist_setting': dimension_type=character_template
2025-10-28 15:49:02,233 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 主角设定 (类别: character)
2025-10-28 15:49:02,233 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=👤 主角设定
2025-10-28 15:49:02,248 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=b444b197-f015-4ed0-8adb-b79a86a8c392
2025-10-28 15:49:02,248 - app.services.book_analysis_service - INFO -   - 维度 'cheat_system': dimension_type=power_system
2025-10-28 15:49:02,248 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 金手指系统 (类别: worldview)
2025-10-28 15:49:02,248 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=🌍 金手指系统
2025-10-28 15:49:02,260 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=59af0b78-1ef2-4fb9-88fc-85d4df00ef3c
2025-10-28 15:49:02,260 - app.services.book_analysis_service - INFO -   - 维度 'world_framework': dimension_type=setting
2025-10-28 15:49:02,260 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 世界观框架 (类别: worldview)
2025-10-28 15:49:02,260 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=🌍 世界观框架
2025-10-28 15:49:02,264 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=99ca095e-d5a4-4d9a-9702-ebd202b1a64c
2025-10-28 15:49:02,264 - app.services.book_analysis_service - INFO -   - 维度 'power_system': dimension_type=power_system
2025-10-28 15:49:02,264 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 等级力量体系 (类别: worldview)
2025-10-28 15:49:02,264 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=🌍 等级力量体系
2025-10-28 15:49:02,278 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=325825ec-d162-452e-b259-c0692c1d4fab
2025-10-28 15:49:02,278 - app.services.book_analysis_service - INFO -   - 维度 'antagonist_forces': dimension_type=character_template
2025-10-28 15:49:02,278 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 反派势力 (类别: character)
2025-10-28 15:49:02,278 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=👤 反派势力
2025-10-28 15:49:02,286 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=7f86e5bb-2b1f-4745-bf79-d45279ef50aa
2025-10-28 15:49:02,286 - app.services.book_analysis_service - INFO -   - 维度 'romance_line': dimension_type=relationship
2025-10-28 15:49:02,286 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 情感线设定 (类别: plot)
2025-10-28 15:49:02,286 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=📖 情感线设定
2025-10-28 15:49:02,294 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=98d397e9-4509-418e-b8d2-cd5f3e78a9fc
2025-10-28 15:49:02,294 - app.services.book_analysis_service - INFO -   - 维度 'satisfaction_points': dimension_type=technique
2025-10-28 15:49:02,294 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 爽点布局 (类别: technique)
2025-10-28 15:49:02,294 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=💡 爽点布局
2025-10-28 15:49:02,302 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=5ab75dda-2d90-4f8d-b085-9b13ad2e0803
2025-10-28 15:49:02,302 - app.services.book_analysis_service - INFO -   - 维度 'anticipation_hooks': dimension_type=technique
2025-10-28 15:49:02,302 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 期待感钩子 (类别: technique)
2025-10-28 15:49:02,302 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=💡 期待感钩子
2025-10-28 15:49:02,311 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=9ee6704b-7f33-4120-84ce-96572103865f
2025-10-28 15:49:02,311 - app.services.book_analysis_service - INFO -   - 维度 'sub_plots': dimension_type=plot_structure
2025-10-28 15:49:02,311 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 支线剧情 (类别: plot)
2025-10-28 15:49:02,311 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=📖 支线剧情
2025-10-28 15:49:02,317 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=fc491e44-3689-4b31-96bb-a1450bc0bd30
2025-10-28 15:49:02,317 - app.services.book_analysis_service - INFO -   - 维度 'unique_features': dimension_type=technique
2025-10-28 15:49:02,317 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 特色设定 (类别: technique)
2025-10-28 15:49:02,317 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=💡 特色设定
2025-10-28 15:49:02,324 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=e72589bf-4108-405f-89b5-7bba4ebc5399
2025-10-28 15:49:02,324 - app.services.book_analysis_service - INFO - 🚀 开始批量向量化 11 个知识条目...
2025-10-28 15:49:02,324 - app.services.vector_store_service - INFO - 🚀 开始批量向量化 11 个知识条目
2025-10-28 15:49:02,333 - app.services.redis_cache_service - INFO - ✓ 向量缓存部分命中: 11/11 个向量
2025-10-28 15:49:02,334 - app.services.vector_store_service - INFO - ⚡ 100%缓存命中,跳过所有向量计算
2025-10-28 15:49:02,379 - app.services.vector_store_service - INFO - ✅ 批量向量化完成: 11个条目, 耗时: 0.06秒
2025-10-28 15:49:02,379 - app.services.book_analysis_service - INFO - ✅ 批量向量化成功
2025-10-28 15:49:02,379 - app.services.book_analysis_service - INFO - 📚 知识点提取完成,共创建 11 个知识条目
2025-10-28 15:49:02,379 - app.services.book_analysis_service - INFO -    - 相比旧策略,覆盖率提升: 从2个类型扩展到所有维度
2025-10-28 15:49:02,387 - app.services.book_analysis_service - INFO - 💡 开始生成智能建议,共 11 个维度
2025-10-28 15:49:02,388 - app.services.book_analysis.suggestion_generator - INFO - 🎯 开始生成建议,共 11 个维度
2025-10-28 15:49:02,388 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'core_selling_point': dimension_type=technique
2025-10-28 15:49:02,388 - app.services.book_analysis.suggestion_generator - INFO -     ❌ 维度类型不可关联,跳过
2025-10-28 15:49:02,388 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'protagonist_setting': dimension_type=character_template
2025-10-28 15:49:02,389 - app.services.book_analysis.suggestion_generator - INFO -     ✅ 创建建议: character, 置信度=0.75
2025-10-28 15:49:02,389 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'cheat_system': dimension_type=power_system
2025-10-28 15:49:02,389 - app.services.book_analysis.suggestion_generator - INFO -     ✅ 创建建议: power_system, 置信度=0.75
2025-10-28 15:49:02,390 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'world_framework': dimension_type=setting
2025-10-28 15:49:02,390 - app.services.book_analysis.suggestion_generator - INFO -     ✅ 创建建议: setting, 置信度=0.60
2025-10-28 15:49:02,390 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'power_system': dimension_type=power_system
2025-10-28 15:49:02,390 - app.services.book_analysis.suggestion_generator - INFO -     ✅ 创建建议: power_system, 置信度=0.65
2025-10-28 15:49:02,390 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'antagonist_forces': dimension_type=character_template
2025-10-28 15:49:02,390 - app.services.book_analysis.suggestion_generator - INFO -     ✅ 创建建议: character, 置信度=0.65
2025-10-28 15:49:02,390 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'romance_line': dimension_type=relationship
2025-10-28 15:49:02,390 - app.services.book_analysis.suggestion_generator - INFO -     ✅ 创建建议: relationship, 置信度=0.60
2025-10-28 15:49:02,390 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'satisfaction_points': dimension_type=technique
2025-10-28 15:49:02,390 - app.services.book_analysis.suggestion_generator - INFO -     ❌ 维度类型不可关联,跳过
2025-10-28 15:49:02,390 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'anticipation_hooks': dimension_type=technique
2025-10-28 15:49:02,390 - app.services.book_analysis.suggestion_generator - INFO -     ❌ 维度类型不可关联,跳过
2025-10-28 15:49:02,390 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'sub_plots': dimension_type=plot_structure
2025-10-28 15:49:02,390 - app.services.book_analysis.suggestion_generator - INFO -     ❌ 维度类型不可关联,跳过
2025-10-28 15:49:02,390 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'unique_features': dimension_type=technique
2025-10-28 15:49:02,390 - app.services.book_analysis.suggestion_generator - INFO -     ❌ 维度类型不可关联,跳过
2025-10-28 15:49:02,393 - app.services.book_analysis.suggestion_generator - INFO - 🎯 建议生成完成,共 6 个
2025-10-28 15:49:02,393 - app.services.book_analysis_service - INFO - 💡 建议生成器返回 6 个建议
2025-10-28 15:49:02,415 - app.services.book_analysis_service - INFO - 💡 智能建议生成完成,共创建 6 个建议
2025-10-28 15:49:02,426 - app.services.redis_cache_service - INFO -
📊 缓存统计:
  - 总请求: 26
  - 命中: 13
  - 未命中: 13
  - 错误: 0
  - 命中率: 50.0%
  - 节省时间: 0.0秒

2025-10-28 15:49:02,426 - app.api.v1.endpoints.books - INFO - 🎉 图书分析任务完成: job_id=20a4260a-09c6-4b00-8ebe-045ab62f7b41
INFO:     127.0.0.1:51069 - "GET /api/v1/books/jobs/20a4260a-09c6-4b00-8ebe-045ab62f7b41/status HTTP/1.1" 200 OK
2025-10-28 15:49:04,038 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: qwen3-32b, Timeout: 60s
INFO:     127.0.0.1:51074 - "POST /api/v1/books/upload HTTP/1.1" 200 OK
2025-10-28 15:49:04,056 - app.api.v1.endpoints.books - INFO - 🚀 开始执行后台分析任务: job_id=73891fef-3346-4aa5-a1c8-a6d369cee8e3, user_id=602f5147-846a-4cde-95d3-405fa75f133f
2025-10-28 15:49:04,060 - app.api.v1.endpoints.books - INFO - ✅ 数据库会话创建成功
2025-10-28 15:49:04,870 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: qwen3-32b, Timeout: 60s
2025-10-28 15:49:04,871 - app.api.v1.endpoints.books - INFO - ✅ AI服务初始化成功
2025-10-28 15:49:04,871 - app.api.v1.endpoints.books - INFO - ✅ 知识库服务初始化成功
2025-10-28 15:49:04,871 - app.api.v1.endpoints.books - INFO - ✅ 图书分析服务初始化成功,开始分析...
2025-10-28 15:49:04,871 - app.services.book_analysis_service - INFO - 📖 analyze_book 开始: job_id=73891fef-3346-4aa5-a1c8-a6d369cee8e3, user_id=602f5147-846a-4cde-95d3-405fa75f133f
2025-10-28 15:49:04,875 - app.services.book_analysis_service - INFO - ✅ 获取到任务: test_cache_v2_1761637743.txt, file_path=uploads\books\cddc24ad-f5d6-45c2-ad35-479560ec6848.txt
INFO:     127.0.0.1:56535 - "GET /api/v1/books/jobs/73891fef-3346-4aa5-a1c8-a6d369cee8e3/status HTTP/1.1" 200 OK
2025-10-28 15:49:04,880 - app.services.book_analysis_service - INFO - 📄 开始解析文件: uploads\books\cddc24ad-f5d6-45c2-ad35-479560ec6848.txt
2025-10-28 15:49:04,880 - app.services.book_analysis.smart_sampling - INFO - 🔍 准备解析文件: uploads\books\cddc24ad-f5d6-45c2-ad35-479560ec6848.txt
2025-10-28 15:49:04,880 - app.services.book_analysis.smart_sampling - INFO - 📁 文件是否存在: True
2025-10-28 15:49:04,881 - app.services.book_analysis.smart_sampling - INFO - 📏 文件大小: 1132 字节
2025-10-28 15:49:04,882 - app.services.book_analysis.smart_sampling - INFO - 📖 读取内容长度: 460 字符
2025-10-28 15:49:04,882 - app.services.book_analysis.smart_sampling - INFO - 📝 内容前200字符: [测试版本: v2 | 时间戳: 1761637743 | ID: 0]

第一章 测试章节

这是一个用于测试Redis缓存的章节内容。

林逸站在窗前,望着远方的天空。

"这一世,我一定要改变命运!"他暗暗发誓。

【系统提示: 检测到主角决心值+10】

第二章 系统觉醒

就在这时,脑海中响起了机械音。

【叮!美食评鉴系统已激活】

林逸愣住了,这是......金手指?

【系统功能说
2025-10-28 15:49:04,882 - app.services.book_analysis.smart_sampling - INFO - 🔎 正则匹配结果: 找到 3 个章节标题
2025-10-28 15:49:04,882 - app.services.book_analysis.smart_sampling - INFO -   匹配1: '第一章 测试章节' at position 38
2025-10-28 15:49:04,882 - app.services.book_analysis.smart_sampling - INFO -   匹配2: '第二章 系统觉醒' at position 132
2025-10-28 15:49:04,883 - app.services.book_analysis.smart_sampling - INFO -   匹配3: '第三章 初试锋芒' at position 274
2025-10-28 15:49:04,883 - app.services.book_analysis.smart_sampling - INFO -   ⏭️ 跳过章节 '第一章 测试章节': 长度82字符 < 最小长度100
2025-10-28 15:49:04,883 - app.services.book_analysis.smart_sampling - INFO -   ✅ 保留章节 '第二章 系统觉醒': 130字符
2025-10-28 15:49:04,884 - app.services.book_analysis.smart_sampling - INFO -   ✅ 保留章节 '第三章 初试锋芒': 175字符
2025-10-28 15:49:04,884 - app.services.book_analysis.smart_sampling - INFO - ✨ 最终保留 2 个有效章节
2025-10-28 15:49:04,884 - app.services.book_analysis_service - INFO - 📊 解析完成,识别到 2 个章节
2025-10-28 15:49:04,885 - app.services.book_analysis_service - INFO -   章节1: 第二章 系统觉醒 (130字)
2025-10-28 15:49:04,885 - app.services.book_analysis_service - INFO -   章节2: 第三章 初试锋芒 (175字)
2025-10-28 15:49:04,894 - app.services.book_analysis_service - INFO - 📊 开始分析 2 个章节: 2个深度分析(串行), 0个增量分析(并行)
2025-10-28 15:49:04,896 - app.services.book_analysis_service - INFO - 🔍 深度分析章节 1: 第二章 系统觉醒
2025-10-28 15:49:04,896 - app.services.book_analysis_service - INFO - ✅ Redis缓存服务初始化成功
2025-10-28 15:49:04,896 - app.services.redis_cache_service - INFO - ✓ 缓存命中: novel_analysis:v2:book_breakdown...
2025-10-28 15:49:04,898 - app.services.book_analysis_service - INFO - ✅ 缓存命中! 章节1 '第二章 系统觉醒' (跳过AI调用)
2025-10-28 15:49:05,393 - app.services.book_analysis_service - INFO - 🔍 深度分析章节 2: 第三章 初试锋芒
2025-10-28 15:49:05,393 - app.services.redis_cache_service - INFO - ✓ 缓存命中: novel_analysis:v2:book_breakdown...
2025-10-28 15:49:05,393 - app.services.book_analysis_service - INFO - ✅ 缓存命中! 章节2 '第三章 初试锋芒' (跳过AI调用)
2025-10-28 15:49:05,899 - app.services.book_analysis_service - INFO - ✅ 深度分析完成, 建立了 11 个维度的基础
2025-10-28 15:49:05,899 - app.services.book_analysis_service - INFO - 📊 章节分析全部完成, 共11个维度
2025-10-28 15:49:05,900 - app.services.book_analysis_service - INFO - 📚 开始提取知识点,共 11 个维度
2025-10-28 15:49:05,900 - app.services.book_analysis_service - INFO -   - 维度 'core_selling_point': dimension_type=technique
2025-10-28 15:49:05,900 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 核心卖点 (类别: technique)
2025-10-28 15:49:05,900 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=💡 核心卖点
2025-10-28 15:49:05,907 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=44dc4ca8-45dc-4e39-846a-7d35ba10cb33
2025-10-28 15:49:05,907 - app.services.book_analysis_service - INFO -   - 维度 'protagonist_setting': dimension_type=character_template
2025-10-28 15:49:05,907 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 主角设定 (类别: character)
2025-10-28 15:49:05,907 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=👤 主角设定
2025-10-28 15:49:05,916 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=f5539cad-c4f3-4b55-bcb7-0fc486638e1f
2025-10-28 15:49:05,916 - app.services.book_analysis_service - INFO -   - 维度 'cheat_system': dimension_type=power_system
2025-10-28 15:49:05,916 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 金手指系统 (类别: worldview)
2025-10-28 15:49:05,916 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=🌍 金手指系统
2025-10-28 15:49:05,916 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=54956701-808d-48c9-8cb4-8db53f364b71
2025-10-28 15:49:05,925 - app.services.book_analysis_service - INFO -   - 维度 'world_framework': dimension_type=setting
2025-10-28 15:49:05,925 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 世界观框架 (类别: worldview)
2025-10-28 15:49:05,925 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=🌍 世界观框架
2025-10-28 15:49:05,930 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=ac03b063-d111-4ec9-b3a8-013a2be63293
2025-10-28 15:49:05,930 - app.services.book_analysis_service - INFO -   - 维度 'power_system': dimension_type=power_system
2025-10-28 15:49:05,930 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 等级力量体系 (类别: worldview)
2025-10-28 15:49:05,930 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=🌍 等级力量体系
2025-10-28 15:49:05,939 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=dcfd58ea-fab8-4c61-b6d8-8bae3cb37e3b
2025-10-28 15:49:05,939 - app.services.book_analysis_service - INFO -   - 维度 'antagonist_forces': dimension_type=character_template
2025-10-28 15:49:05,939 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 反派势力 (类别: character)
2025-10-28 15:49:05,939 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=👤 反派势力
2025-10-28 15:49:05,944 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=795bda93-919b-4a10-ae80-8041eca6c88a
2025-10-28 15:49:05,944 - app.services.book_analysis_service - INFO -   - 维度 'romance_line': dimension_type=relationship
2025-10-28 15:49:05,944 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 情感线设定 (类别: plot)
2025-10-28 15:49:05,944 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=📖 情感线设定
2025-10-28 15:49:05,949 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=27243488-3522-4720-a93f-5ed5b734c96f
2025-10-28 15:49:05,949 - app.services.book_analysis_service - INFO -   - 维度 'satisfaction_points': dimension_type=technique
2025-10-28 15:49:05,949 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 爽点布局 (类别: technique)
2025-10-28 15:49:05,949 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=💡 爽点布局
2025-10-28 15:49:05,957 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=b88ebb78-3759-4c56-8dc2-8c822841e87a
2025-10-28 15:49:05,957 - app.services.book_analysis_service - INFO -   - 维度 'anticipation_hooks': dimension_type=technique
2025-10-28 15:49:05,957 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 期待感钩子 (类别: technique)
2025-10-28 15:49:05,957 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=💡 期待感钩子
2025-10-28 15:49:05,957 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=79d57eb2-b2ed-40f1-9245-5b23e6f5fa9b
2025-10-28 15:49:05,962 - app.services.book_analysis_service - INFO -   - 维度 'sub_plots': dimension_type=plot_structure
2025-10-28 15:49:05,962 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 支线剧情 (类别: plot)
2025-10-28 15:49:05,962 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=📖 支线剧情
2025-10-28 15:49:05,965 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=d15b2143-998e-4c1f-a9f9-9f346c2040d4
2025-10-28 15:49:05,965 - app.services.book_analysis_service - INFO -   - 维度 'unique_features': dimension_type=technique
2025-10-28 15:49:05,965 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 特色设定 (类别: technique)
2025-10-28 15:49:05,965 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=💡 特色设定
2025-10-28 15:49:05,965 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=1257bfc6-8e2d-462c-9037-582972a4d9d8
2025-10-28 15:49:05,965 - app.services.book_analysis_service - INFO - 🚀 开始批量向量化 11 个知识条目...
2025-10-28 15:49:05,965 - app.services.vector_store_service - INFO - 🚀 开始批量向量化 11 个知识条目
2025-10-28 15:49:05,975 - app.services.vector_store_service - INFO - 🔄 缓存未命中,计算全部 11 个向量
Batches: 100%|█████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  2.65it/s]
2025-10-28 15:49:06,377 - app.services.redis_cache_service - INFO - ✓ 向量缓存成功: 11 个向量 (TTL: 604800秒)
2025-10-28 15:49:06,427 - app.services.vector_store_service - INFO - ✅ 批量向量化完成: 11个条目, 耗时: 0.46秒
2025-10-28 15:49:06,427 - app.services.book_analysis_service - INFO - ✅ 批量向量化成功
2025-10-28 15:49:06,427 - app.services.book_analysis_service - INFO - 📚 知识点提取完成,共创建 11 个知识条目
2025-10-28 15:49:06,427 - app.services.book_analysis_service - INFO -    - 相比旧策略,覆盖率提升: 从2个类型扩展到所有维度
2025-10-28 15:49:06,427 - app.services.book_analysis_service - INFO - 💡 开始生成智能建议,共 11 个维度
2025-10-28 15:49:06,427 - app.services.book_analysis.suggestion_generator - INFO - 🎯 开始生成建议,共 11 个维度
2025-10-28 15:49:06,427 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'core_selling_point': dimension_type=technique
2025-10-28 15:49:06,427 - app.services.book_analysis.suggestion_generator - INFO -     ❌ 维度类型不可关联,跳过
2025-10-28 15:49:06,427 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'protagonist_setting': dimension_type=character_template
2025-10-28 15:49:06,427 - app.services.book_analysis.suggestion_generator - INFO -     ✅ 创建建议: character, 置信度=0.75
2025-10-28 15:49:06,427 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'cheat_system': dimension_type=power_system
2025-10-28 15:49:06,427 - app.services.book_analysis.suggestion_generator - INFO -     ✅ 创建建议: power_system, 置信度=0.75
2025-10-28 15:49:06,427 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'world_framework': dimension_type=setting
2025-10-28 15:49:06,427 - app.services.book_analysis.suggestion_generator - INFO -     ✅ 创建建议: setting, 置信度=0.60
2025-10-28 15:49:06,427 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'power_system': dimension_type=power_system
2025-10-28 15:49:06,427 - app.services.book_analysis.suggestion_generator - INFO -     ✅ 创建建议: power_system, 置信度=0.65
2025-10-28 15:49:06,427 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'antagonist_forces': dimension_type=character_template
2025-10-28 15:49:06,427 - app.services.book_analysis.suggestion_generator - INFO -     ✅ 创建建议: character, 置信度=0.65
2025-10-28 15:49:06,427 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'romance_line': dimension_type=relationship
2025-10-28 15:49:06,427 - app.services.book_analysis.suggestion_generator - INFO -     ✅ 创建建议: relationship, 置信度=0.60
2025-10-28 15:49:06,439 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'satisfaction_points': dimension_type=technique
2025-10-28 15:49:06,439 - app.services.book_analysis.suggestion_generator - INFO -     ❌ 维度类型不可关联,跳过
2025-10-28 15:49:06,439 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'anticipation_hooks': dimension_type=technique
2025-10-28 15:49:06,439 - app.services.book_analysis.suggestion_generator - INFO -     ❌ 维度类型不可关联,跳过
2025-10-28 15:49:06,439 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'sub_plots': dimension_type=plot_structure
2025-10-28 15:49:06,439 - app.services.book_analysis.suggestion_generator - INFO -     ❌ 维度类型不可关联,跳过
2025-10-28 15:49:06,439 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'unique_features': dimension_type=technique
2025-10-28 15:49:06,440 - app.services.book_analysis.suggestion_generator - INFO -     ❌ 维度类型不可关联,跳过
2025-10-28 15:49:06,440 - app.services.book_analysis.suggestion_generator - INFO - 🎯 建议生成完成,共 6 个
2025-10-28 15:49:06,440 - app.services.book_analysis_service - INFO - 💡 建议生成器返回 6 个建议
2025-10-28 15:49:06,448 - app.services.book_analysis_service - INFO - 💡 智能建议生成完成,共创建 6 个建议
2025-10-28 15:49:06,456 - app.services.redis_cache_service - INFO -
📊 缓存统计:
  - 总请求: 39
  - 命中: 15
  - 未命中: 24
  - 错误: 0
  - 命中率: 38.5%
  - 节省时间: 0.0秒

2025-10-28 15:49:06,456 - app.api.v1.endpoints.books - INFO - 🎉 图书分析任务完成: job_id=73891fef-3346-4aa5-a1c8-a6d369cee8e3
INFO:     127.0.0.1:56539 - "GET /api/v1/books/jobs/73891fef-3346-4aa5-a1c8-a6d369cee8e3/status HTTP/1.1" 200 OK
INFO:     127.0.0.1:56542 - "DELETE /api/v1/books/jobs/ae8288d2-2c18-4a95-938a-703be6360e7a HTTP/1.1" 200 OK
INFO:     127.0.0.1:56545 - "DELETE /api/v1/books/jobs/20a4260a-09c6-4b00-8ebe-045ab62f7b41 HTTP/1.1" 200 OK
INFO:     127.0.0.1:56548 - "DELETE /api/v1/books/jobs/73891fef-3346-4aa5-a1c8-a6d369cee8e3 HTTP/1.1" 200 OK
