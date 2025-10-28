(venv) PS D:\Java\ai_writer\backend> python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
INFO:     Will watch for changes in these directories: ['D:\\Java\\ai_writer\\backend']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [34064] using WatchFiles
已注册策略: web_novel_11d - 网文11维度分析
INFO:     Started server process [4404]
INFO:     Waiting for application startup.
2025-10-28 15:25:34,197 - app.main - INFO - 🚀 应用启动中...
2025-10-28 15:25:34,198 - app.core.database - INFO - 正在初始化数据库... (尝试 1/3)
2025-10-28 15:25:34,589 - app.core.database - INFO - ✅ 数据库初始化成功
2025-10-28 15:25:34,592 - apscheduler.scheduler - INFO - Adding job tentatively -- it will be properly scheduled when the scheduler starts
2025-10-28 15:25:34,597 - apscheduler.scheduler - INFO - Added job "清理过期的去痕迹会话详情" to job store "default"
2025-10-28 15:25:34,597 - apscheduler.scheduler - INFO - Scheduler started
2025-10-28 15:25:34,598 - app.tasks.cleanup_humanize_details - INFO - 定时任务调度器已启动
2025-10-28 15:25:34,599 - app.main - INFO - 🔄 开始预加载Embedding模型...
2025-10-28 15:25:34,599 - app.services.vector_store_service - INFO - 🔄 预加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
2025-10-28 15:25:34,602 - sentence_transformers.SentenceTransformer - INFO - Use pytorch device_name: cpu
2025-10-28 15:25:34,602 - sentence_transformers.SentenceTransformer - INFO - Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
2025-10-28 15:25:46,847 - app.services.vector_store_service - INFO - ✅ Embedding模型预加载成功，耗时: 12.25秒
2025-10-28 15:25:46,849 - app.main - INFO - ✅ Embedding模型预加载完成
2025-10-28 15:25:46,849 - app.main - INFO - ✅ 应用启动完成
INFO:     Application startup complete.
INFO:     127.0.0.1:55334 - "POST /api/v1/auth/login HTTP/1.1" 200 OK
2025-10-28 15:25:59,548 - app.services.ai.prompts - INFO - Prompts loaded successfully from D:\Java\ai_writer\backend\app\services\ai\prompts\default.json
2025-10-28 15:26:01,037 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: qwen3-32b, Timeout: 60s
INFO:     127.0.0.1:55337 - "POST /api/v1/books/upload HTTP/1.1" 200 OK
2025-10-28 15:26:01,160 - app.api.v1.endpoints.books - INFO - 🚀 开始执行后台分析任务: job_id=015e9e24-274b-4118-9a79-013f9f6cbfcc, user_id=602f5147-846a-4cde-95d3-405fa75f133f
2025-10-28 15:26:01,160 - app.api.v1.endpoints.books - INFO - ✅ 数据库会话创建成功
2025-10-28 15:26:02,657 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: qwen3-32b, Timeout: 60s
2025-10-28 15:26:02,658 - app.api.v1.endpoints.books - INFO - ✅ AI服务初始化成功
2025-10-28 15:26:02,660 - app.api.v1.endpoints.books - INFO - ✅ 知识库服务初始化成功
2025-10-28 15:26:02,660 - app.api.v1.endpoints.books - INFO - ✅ 图书分析服务初始化成功,开始分析...
2025-10-28 15:26:02,660 - app.services.book_analysis_service - INFO - 📖 analyze_book 开始: job_id=015e9e24-274b-4118-9a79-013f9f6cbfcc, user_id=602f5147-846a-4cde-95d3-405fa75f133f
2025-10-28 15:26:02,689 - app.services.book_analysis_service - INFO - ✅ 获取到任务: test_cache_v1_1761636359.txt, file_path=uploads\books\a33fc2ee-58fe-4f36-a361-e709bab2ee5b.txt
2025-10-28 15:26:02,703 - app.services.book_analysis_service - INFO - 📄 开始解析文件: uploads\books\a33fc2ee-58fe-4f36-a361-e709bab2ee5b.txt
2025-10-28 15:26:02,705 - app.services.book_analysis.smart_sampling - INFO - 🔍 准备解析文件: uploads\books\a33fc2ee-58fe-4f36-a361-e709bab2ee5b.txt
2025-10-28 15:26:02,705 - app.services.book_analysis.smart_sampling - INFO - 📁 文件是否存在: True
2025-10-28 15:26:02,705 - app.services.book_analysis.smart_sampling - INFO - 📏 文件大小: 1132 字节
2025-10-28 15:26:02,707 - app.services.book_analysis.smart_sampling - INFO - 📖 读取内容长度: 460 字符
2025-10-28 15:26:02,707 - app.services.book_analysis.smart_sampling - INFO - 📝 内容前200字符: [测试版本: v1 | 时间戳: 1761636359 | ID: 0]

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
2025-10-28 15:26:02,707 - app.services.book_analysis.smart_sampling - INFO - 🔎 正则匹配结果: 找到 3 个章节标题
2025-10-28 15:26:02,707 - app.services.book_analysis.smart_sampling - INFO -   匹配1: '第一章 测试章节' at position 38
2025-10-28 15:26:02,709 - app.services.book_analysis.smart_sampling - INFO -   匹配2: '第二章 系统觉醒' at position 132
2025-10-28 15:26:02,709 - app.services.book_analysis.smart_sampling - INFO -   匹配3: '第三章 初试锋芒' at position 274
2025-10-28 15:26:02,709 - app.services.book_analysis.smart_sampling - INFO -   ⏭️ 跳过章节 '第一章 测试章节': 长度82字符 < 最小长度100
2025-10-28 15:26:02,709 - app.services.book_analysis.smart_sampling - INFO -   ✅ 保留章节 '第二章 系统觉醒': 130字符
2025-10-28 15:26:02,709 - app.services.book_analysis.smart_sampling - INFO -   ✅ 保留章节 '第三章 初试锋芒': 175字符
2025-10-28 15:26:02,711 - app.services.book_analysis.smart_sampling - INFO - ✨ 最终保留 2 个有效章节
2025-10-28 15:26:02,711 - app.services.book_analysis_service - INFO - 📊 解析完成,识别到 2 个章节
2025-10-28 15:26:02,713 - app.services.book_analysis_service - INFO -   章节1: 第二章 系统觉醒 (130字)
2025-10-28 15:26:02,713 - app.services.book_analysis_service - INFO -   章节2: 第三章 初试锋芒 (175字)
2025-10-28 15:26:02,753 - app.services.book_analysis_service - INFO - 📊 开始分析 2 个章节: 2个深度分析(串行), 0个增量分析(并行)
2025-10-28 15:26:02,766 - app.services.book_analysis_service - INFO - 🔍 深度分析章节 1: 第二章 系统觉醒
INFO:     127.0.0.1:55340 - "GET /api/v1/books/jobs/015e9e24-274b-4118-9a79-013f9f6cbfcc/status HTTP/1.1" 200 OK
2025-10-28 15:26:04,803 - app.services.redis_cache_service - INFO - ✓ Redis连接成功
2025-10-28 15:26:04,804 - app.services.book_analysis_service - INFO - ✅ Redis缓存服务初始化成功
2025-10-28 15:26:04,809 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=3000, temp=0.3, 尝试=1/3
INFO:     127.0.0.1:50067 - "GET /api/v1/books/jobs/015e9e24-274b-4118-9a79-013f9f6cbfcc/status HTTP/1.1" 200 OK
INFO:     127.0.0.1:62724 - "GET /api/v1/books/jobs/015e9e24-274b-4118-9a79-013f9f6cbfcc/status HTTP/1.1" 200 OK
INFO:     127.0.0.1:62727 - "GET /api/v1/books/jobs/015e9e24-274b-4118-9a79-013f9f6cbfcc/status HTTP/1.1" 200 OK
INFO:     127.0.0.1:62730 - "GET /api/v1/books/jobs/015e9e24-274b-4118-9a79-013f9f6cbfcc/status HTTP/1.1" 200 OK
INFO:     127.0.0.1:63040 - "GET /api/v1/books/jobs/015e9e24-274b-4118-9a79-013f9f6cbfcc/status HTTP/1.1" 200 OK
INFO:     127.0.0.1:54177 - "GET /api/v1/books/jobs/015e9e24-274b-4118-9a79-013f9f6cbfcc/status HTTP/1.1" 200 OK
INFO:     127.0.0.1:54180 - "GET /api/v1/books/jobs/015e9e24-274b-4118-9a79-013f9f6cbfcc/status HTTP/1.1" 200 OK
INFO:     127.0.0.1:54183 - "GET /api/v1/books/jobs/015e9e24-274b-4118-9a79-013f9f6cbfcc/status HTTP/1.1" 200 OK
INFO:     127.0.0.1:54186 - "GET /api/v1/books/jobs/015e9e24-274b-4118-9a79-013f9f6cbfcc/status HTTP/1.1" 200 OK
INFO:     127.0.0.1:54189 - "GET /api/v1/books/jobs/015e9e24-274b-4118-9a79-013f9f6cbfcc/status HTTP/1.1" 200 OK
2025-10-28 15:26:26,511 - httpx - INFO - HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
2025-10-28 15:26:26,524 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=3307, 尝试次数=1
2025-10-28 15:26:26,530 - app.services.book_analysis_service - INFO - 💾 AI响应已保存到: D:\Java\ai_writer\backend\debug_ai_responses\ch1_第二章 系统觉醒.txt
2025-10-28 15:26:26,532 - app.services.book_analysis.web_novel_strategy - INFO - 🔍 开始解析AI响应,长度=3307
2025-10-28 15:26:26,532 - app.services.book_analysis.web_novel_strategy - INFO - ✅ 预处理: 已替换中文标点符号
2025-10-28 15:26:26,533 - app.services.book_analysis.web_novel_strategy - INFO - ✅ 直接解析JSON成功
2025-10-28 15:26:26,533 - app.services.book_analysis_service - INFO - ✅ 章节1 '第二章 系统觉醒' 分析成功,获得 11 个维度
2025-10-28 15:26:26,539 - app.services.redis_cache_service - INFO - ✓ 结果已缓存: novel_analysis:book_breakdown:a6... (TTL: 604800秒)
INFO:     127.0.0.1:54192 - "GET /api/v1/books/jobs/015e9e24-274b-4118-9a79-013f9f6cbfcc/status HTTP/1.1" 200 OK
2025-10-28 15:26:27,074 - app.services.book_analysis_service - INFO - 🔍 深度分析章节 2: 第三章 初试锋芒
INFO:     127.0.0.1:54195 - "GET /api/v1/books/jobs/015e9e24-274b-4118-9a79-013f9f6cbfcc/status HTTP/1.1" 200 OK
INFO:     127.0.0.1:54198 - "GET /api/v1/books/jobs/015e9e24-274b-4118-9a79-013f9f6cbfcc/status HTTP/1.1" 200 OK
2025-10-28 15:26:32,088 - app.services.redis_cache_service - WARNING - 查询缓存失败: Timeout reading from localhost:6379
2025-10-28 15:26:32,090 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=3000, temp=0.3, 尝试=1/3
INFO:     127.0.0.1:54205 - "GET /api/v1/books/jobs/015e9e24-274b-4118-9a79-013f9f6cbfcc/status HTTP/1.1" 200 OK
INFO:     127.0.0.1:54212 - "GET /api/v1/books/jobs/015e9e24-274b-4118-9a79-013f9f6cbfcc/status HTTP/1.1" 200 OK
INFO:     127.0.0.1:54215 - "GET /api/v1/books/jobs/015e9e24-274b-4118-9a79-013f9f6cbfcc/status HTTP/1.1" 200 OK
INFO:     127.0.0.1:54218 - "GET /api/v1/books/jobs/015e9e24-274b-4118-9a79-013f9f6cbfcc/status HTTP/1.1" 200 OK
INFO:     127.0.0.1:54221 - "GET /api/v1/books/jobs/015e9e24-274b-4118-9a79-013f9f6cbfcc/status HTTP/1.1" 200 OK
INFO:     127.0.0.1:54224 - "GET /api/v1/books/jobs/015e9e24-274b-4118-9a79-013f9f6cbfcc/status HTTP/1.1" 200 OK
INFO:     127.0.0.1:54233 - "GET /api/v1/books/jobs/015e9e24-274b-4118-9a79-013f9f6cbfcc/status HTTP/1.1" 200 OK
INFO:     127.0.0.1:54236 - "GET /api/v1/books/jobs/015e9e24-274b-4118-9a79-013f9f6cbfcc/status HTTP/1.1" 200 OK
INFO:     127.0.0.1:54239 - "GET /api/v1/books/jobs/015e9e24-274b-4118-9a79-013f9f6cbfcc/status HTTP/1.1" 200 OK
2025-10-28 15:26:51,574 - httpx - INFO - HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
2025-10-28 15:26:51,579 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=3278, 尝试次数=1
2025-10-28 15:26:51,580 - app.services.book_analysis_service - INFO - 💾 AI响应已保存到: D:\Java\ai_writer\backend\debug_ai_responses\ch2_第三章 初试锋芒.txt
2025-10-28 15:26:51,582 - app.services.book_analysis.web_novel_strategy - INFO - 🔍 开始解析AI响应,长度=3278
2025-10-28 15:26:51,582 - app.services.book_analysis.web_novel_strategy - INFO - ✅ 预处理: 已替换中文标点符号
2025-10-28 15:26:51,582 - app.services.book_analysis.web_novel_strategy - INFO - ✅ 直接解析JSON成功
2025-10-28 15:26:51,582 - app.services.book_analysis_service - INFO - ✅ 章节2 '第三章 初试锋芒' 分析成功,获得 11 个维度
INFO:     127.0.0.1:54243 - "GET /api/v1/books/jobs/015e9e24-274b-4118-9a79-013f9f6cbfcc/status HTTP/1.1" 200 OK
INFO:     127.0.0.1:54247 - "GET /api/v1/books/jobs/015e9e24-274b-4118-9a79-013f9f6cbfcc/status HTTP/1.1" 200 OK
INFO:     127.0.0.1:54251 - "GET /api/v1/books/jobs/015e9e24-274b-4118-9a79-013f9f6cbfcc/status HTTP/1.1" 200 OK
2025-10-28 15:26:58,633 - app.services.redis_cache_service - WARNING - 写入缓存失败: Timeout reading from localhost:6379
2025-10-28 15:26:59,145 - app.services.book_analysis_service - INFO - ✅ 深度分析完成, 建立了 11 个维度的基础
2025-10-28 15:26:59,146 - app.services.book_analysis_service - INFO - 📊 章节分析全部完成, 共11个维度
2025-10-28 15:26:59,147 - app.services.book_analysis_service - INFO - 📚 开始提取知识点,共 11 个维度
2025-10-28 15:26:59,147 - app.services.book_analysis_service - INFO -   - 维度 'core_selling_point': dimension_type=technique
2025-10-28 15:26:59,148 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 核心卖点 (类别: technique)
2025-10-28 15:26:59,149 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=💡 核心卖点
2025-10-28 15:26:59,246 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=f93716bd-1ec1-4819-85ee-bbb4a03e5d3e
2025-10-28 15:26:59,248 - app.services.book_analysis_service - INFO -   - 维度 'protagonist_setting': dimension_type=character_template
2025-10-28 15:26:59,248 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 主角设定 (类别: character)
2025-10-28 15:26:59,249 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=👤 主角设定
2025-10-28 15:26:59,276 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=d8d87c36-c530-47f5-b331-45133c4d3676
2025-10-28 15:26:59,277 - app.services.book_analysis_service - INFO -   - 维度 'cheat_system': dimension_type=power_system
2025-10-28 15:26:59,277 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 金手指系统 (类别: worldview)
2025-10-28 15:26:59,278 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=🌍 金手指系统
2025-10-28 15:26:59,293 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=7fff280a-7504-47e5-963b-31b5126906a2
2025-10-28 15:26:59,293 - app.services.book_analysis_service - INFO -   - 维度 'world_framework': dimension_type=setting
2025-10-28 15:26:59,294 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 世界观框架 (类别: worldview)
2025-10-28 15:26:59,295 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=🌍 世界观框架
2025-10-28 15:26:59,307 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=8be97a31-98cb-492a-82bd-198779b4bed3
2025-10-28 15:26:59,308 - app.services.book_analysis_service - INFO -   - 维度 'power_system': dimension_type=power_system
2025-10-28 15:26:59,309 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 等级力量体系 (类别: worldview)
2025-10-28 15:26:59,310 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=🌍 等级力量体系
2025-10-28 15:26:59,321 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=a0785edd-9935-4a3b-b0b1-c848fda0e535
2025-10-28 15:26:59,322 - app.services.book_analysis_service - INFO -   - 维度 'antagonist_forces': dimension_type=character_template
2025-10-28 15:26:59,322 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 反派势力 (类别: character)
2025-10-28 15:26:59,323 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=👤 反派势力
2025-10-28 15:26:59,336 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=1b592b50-3e15-4ce2-be4f-f77f08f44d43
2025-10-28 15:26:59,337 - app.services.book_analysis_service - INFO -   - 维度 'romance_line': dimension_type=relationship
2025-10-28 15:26:59,337 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 情感线设定 (类别: plot)
2025-10-28 15:26:59,338 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=📖 情感线设定
2025-10-28 15:26:59,352 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=5c1806ab-6ef8-4766-acc8-a0d6c625d89b
2025-10-28 15:26:59,353 - app.services.book_analysis_service - INFO -   - 维度 'satisfaction_points': dimension_type=technique
2025-10-28 15:26:59,354 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 爽点布局 (类别: technique)
2025-10-28 15:26:59,354 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=💡 爽点布局
2025-10-28 15:26:59,366 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=245ef165-af1b-44bf-94a3-f757593a6234
2025-10-28 15:26:59,367 - app.services.book_analysis_service - INFO -   - 维度 'anticipation_hooks': dimension_type=technique
2025-10-28 15:26:59,367 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 期待感钩子 (类别: technique)
2025-10-28 15:26:59,368 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=💡 期待感钩子
2025-10-28 15:26:59,381 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=3b64436f-c384-4ad7-ae18-8d9b1c71ed95
2025-10-28 15:26:59,381 - app.services.book_analysis_service - INFO -   - 维度 'sub_plots': dimension_type=plot_structure
2025-10-28 15:26:59,381 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 支线剧情 (类别: plot)
2025-10-28 15:26:59,382 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=📖 支线剧情
2025-10-28 15:26:59,397 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=1cb976a6-8a47-4b94-a21d-61d548562093
2025-10-28 15:26:59,398 - app.services.book_analysis_service - INFO -   - 维度 'unique_features': dimension_type=technique
2025-10-28 15:26:59,398 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 特色设定 (类别: technique)
2025-10-28 15:26:59,399 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=💡 特色设定
2025-10-28 15:26:59,410 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=e6cfc6e9-5ac3-416a-94ba-5d9b20a9abb5
2025-10-28 15:26:59,410 - app.services.book_analysis_service - INFO - 🚀 开始批量向量化 11 个知识条目...
2025-10-28 15:26:59,411 - app.services.vector_store_service - INFO - 🚀 开始批量向量化 11 个知识条目
Batches: 100%|█████████████████████████████████████████████████████████████████████| 1/1 [00:01<00:00,  1.63s/it]
INFO:     127.0.0.1:54254 - "GET /api/v1/books/jobs/015e9e24-274b-4118-9a79-013f9f6cbfcc/status HTTP/1.1" 200 OK
2025-10-28 15:27:01,246 - app.services.vector_store_service - INFO - ✅ 批量向量化完成: 11个条目, 耗时: 1.83秒
2025-10-28 15:27:01,247 - app.services.book_analysis_service - INFO - ✅ 批量向量化成功
2025-10-28 15:27:01,247 - app.services.book_analysis_service - INFO - 📚 知识点提取完成,共创建 11 个知识条目
2025-10-28 15:27:01,248 - app.services.book_analysis_service - INFO -    - 相比旧策略,覆盖率提升: 从2个类型扩展到所有维度
2025-10-28 15:27:01,254 - app.services.book_analysis_service - INFO - 💡 开始生成智能建议,共 11 个维度
2025-10-28 15:27:01,254 - app.services.book_analysis.suggestion_generator - INFO - 🎯 开始生成建议,共 11 个维度
2025-10-28 15:27:01,255 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'core_selling_point': dimension_type=technique
2025-10-28 15:27:01,255 - app.services.book_analysis.suggestion_generator - INFO -     ❌ 维度类型不可关联,跳过
2025-10-28 15:27:01,256 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'protagonist_setting': dimension_type=character_template
2025-10-28 15:27:01,261 - app.services.book_analysis.suggestion_generator - INFO -     ✅ 创建建议: character, 置信度=0.75
2025-10-28 15:27:01,262 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'cheat_system': dimension_type=power_system
2025-10-28 15:27:01,264 - app.services.book_analysis.suggestion_generator - INFO -     ✅ 创建建议: power_system, 置信度=0.75
2025-10-28 15:27:01,264 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'world_framework': dimension_type=setting
2025-10-28 15:27:01,272 - app.services.book_analysis.suggestion_generator - INFO -     ✅ 创建建议: setting, 置信度=0.60
2025-10-28 15:27:01,272 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'power_system': dimension_type=power_system
2025-10-28 15:27:01,273 - app.services.book_analysis.suggestion_generator - INFO -     ✅ 创建建议: power_system, 置信度=0.60
2025-10-28 15:27:01,274 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'antagonist_forces': dimension_type=character_template
2025-10-28 15:27:01,274 - app.services.book_analysis.suggestion_generator - INFO -     ✅ 创建建议: character, 置信度=0.65
2025-10-28 15:27:01,275 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'romance_line': dimension_type=relationship
2025-10-28 15:27:01,275 - app.services.book_analysis.suggestion_generator - INFO -     ❌ 置信度不足 (0.50 < 0.6)
2025-10-28 15:27:01,276 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'satisfaction_points': dimension_type=technique
2025-10-28 15:27:01,276 - app.services.book_analysis.suggestion_generator - INFO -     ❌ 维度类型不可关联,跳过
2025-10-28 15:27:01,277 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'anticipation_hooks': dimension_type=technique
2025-10-28 15:27:01,277 - app.services.book_analysis.suggestion_generator - INFO -     ❌ 维度类型不可关联,跳过
2025-10-28 15:27:01,278 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'sub_plots': dimension_type=plot_structure
2025-10-28 15:27:01,278 - app.services.book_analysis.suggestion_generator - INFO -     ❌ 维度类型不可关联,跳过
2025-10-28 15:27:01,279 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'unique_features': dimension_type=technique
2025-10-28 15:27:01,279 - app.services.book_analysis.suggestion_generator - INFO -     ❌ 维度类型不可关联,跳过
2025-10-28 15:27:01,279 - app.services.book_analysis.suggestion_generator - INFO - 🎯 建议生成完成,共 5 个
2025-10-28 15:27:01,280 - app.services.book_analysis_service - INFO - 💡 建议生成器返回 5 个建议
2025-10-28 15:27:01,328 - app.services.book_analysis_service - INFO - 💡 智能建议生成完成,共创建 5 个建议
2025-10-28 15:27:01,352 - app.api.v1.endpoints.books - INFO - 🎉 图书分析任务完成: job_id=015e9e24-274b-4118-9a79-013f9f6cbfcc
INFO:     127.0.0.1:64133 - "GET /api/v1/books/jobs/015e9e24-274b-4118-9a79-013f9f6cbfcc/status HTTP/1.1" 200 OK
2025-10-28 15:27:04,737 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: qwen3-32b, Timeout: 60s
INFO:     127.0.0.1:64136 - "POST /api/v1/books/upload HTTP/1.1" 200 OK
2025-10-28 15:27:04,798 - app.api.v1.endpoints.books - INFO - 🚀 开始执行后台分析任务: job_id=807dd020-a35e-479c-b33b-a2324f7a2718, user_id=602f5147-846a-4cde-95d3-405fa75f133f
2025-10-28 15:27:04,798 - app.api.v1.endpoints.books - INFO - ✅ 数据库会话创建成功
2025-10-28 15:27:06,192 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: qwen3-32b, Timeout: 60s
2025-10-28 15:27:06,193 - app.api.v1.endpoints.books - INFO - ✅ AI服务初始化成功
2025-10-28 15:27:06,193 - app.api.v1.endpoints.books - INFO - ✅ 知识库服务初始化成功
2025-10-28 15:27:06,193 - app.api.v1.endpoints.books - INFO - ✅ 图书分析服务初始化成功,开始分析...
2025-10-28 15:27:06,193 - app.services.book_analysis_service - INFO - 📖 analyze_book 开始: job_id=807dd020-a35e-479c-b33b-a2324f7a2718, user_id=602f5147-846a-4cde-95d3-405fa75f133f
2025-10-28 15:27:06,203 - app.services.book_analysis_service - INFO - ✅ 获取到任务: test_cache_v1_1761636359.txt, file_path=uploads\books\814fc92e-ba02-4957-94af-0af7598afef5.txt
INFO:     127.0.0.1:64139 - "GET /api/v1/books/jobs/807dd020-a35e-479c-b33b-a2324f7a2718/status HTTP/1.1" 200 OK
2025-10-28 15:27:06,214 - app.services.book_analysis_service - INFO - 📄 开始解析文件: uploads\books\814fc92e-ba02-4957-94af-0af7598afef5.txt
2025-10-28 15:27:06,215 - app.services.book_analysis.smart_sampling - INFO - 🔍 准备解析文件: uploads\books\814fc92e-ba02-4957-94af-0af7598afef5.txt
2025-10-28 15:27:06,216 - app.services.book_analysis.smart_sampling - INFO - 📁 文件是否存在: True
2025-10-28 15:27:06,217 - app.services.book_analysis.smart_sampling - INFO - 📏 文件大小: 1135 字节
2025-10-28 15:27:06,218 - app.services.book_analysis.smart_sampling - INFO - 📖 读取内容长度: 463 字符
2025-10-28 15:27:06,218 - app.services.book_analysis.smart_sampling - INFO - 📝 内容前200字符: [测试版本: v1 | 时间戳: 1761636359 | ID: 3270]

第一章 测试章节

这是一个用于测试Redis缓存的章节内容。

林逸站在窗前,望着远方的天空。

"这一世,我一定要改变命运!"他暗暗发誓。

【系统提示: 检测到主角决心值+10】

第二章 系统觉醒

就在这时,脑海中响起了机械音。

【叮!美食评鉴系统已激活】

林逸愣住了,这是......金手指?

【系统
2025-10-28 15:27:06,220 - app.services.book_analysis.smart_sampling - INFO - 🔎 正则匹配结果: 找到 3 个章节标题
2025-10-28 15:27:06,220 - app.services.book_analysis.smart_sampling - INFO -   匹配1: '第一章 测试章节' at position 41
2025-10-28 15:27:06,221 - app.services.book_analysis.smart_sampling - INFO -   匹配2: '第二章 系统觉醒' at position 135
2025-10-28 15:27:06,221 - app.services.book_analysis.smart_sampling - INFO -   匹配3: '第三章 初试锋芒' at position 277
2025-10-28 15:27:06,222 - app.services.book_analysis.smart_sampling - INFO -   ⏭️ 跳过章节 '第一章 测试章节': 长度82字符 < 最小长度100
2025-10-28 15:27:06,222 - app.services.book_analysis.smart_sampling - INFO -   ✅ 保留章节 '第二章 系统觉醒': 130字符
2025-10-28 15:27:06,223 - app.services.book_analysis.smart_sampling - INFO -   ✅ 保留章节 '第三章 初试锋芒': 175字符
2025-10-28 15:27:06,223 - app.services.book_analysis.smart_sampling - INFO - ✨ 最终保留 2 个有效章节
2025-10-28 15:27:06,224 - app.services.book_analysis_service - INFO - 📊 解析完成,识别到 2 个章节
2025-10-28 15:27:06,225 - app.services.book_analysis_service - INFO -   章节1: 第二章 系统觉醒 (130字)
2025-10-28 15:27:06,225 - app.services.book_analysis_service - INFO -   章节2: 第三章 初试锋芒 (175字)
2025-10-28 15:27:06,249 - app.services.book_analysis_service - INFO - 📊 开始分析 2 个章节: 2个深度分析(串行), 0个增量分析(并行)
2025-10-28 15:27:06,259 - app.services.book_analysis_service - INFO - 🔍 深度分析章节 1: 第二章 系统觉醒
2025-10-28 15:27:06,259 - app.services.book_analysis_service - INFO - ✅ Redis缓存服务初始化成功
2025-10-28 15:27:08,393 - app.services.redis_cache_service - INFO - ✓ 缓存命中: novel_analysis:book_breakdown:a6...
2025-10-28 15:27:08,393 - app.services.book_analysis_service - INFO - ✅ 缓存命中! 章节1 '第二章 系统觉醒' (跳过AI调用)
2025-10-28 15:27:08,920 - app.services.book_analysis_service - INFO - 🔍 深度分析章节 2: 第三章 初试锋芒
2025-10-28 15:27:08,924 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=3000, temp=0.3, 尝试=1/3
INFO:     127.0.0.1:64144 - "GET /api/v1/books/jobs/807dd020-a35e-479c-b33b-a2324f7a2718/status HTTP/1.1" 200 OK
INFO:     127.0.0.1:64149 - "GET /api/v1/books/jobs/807dd020-a35e-479c-b33b-a2324f7a2718/status HTTP/1.1" 200 OK
INFO:     127.0.0.1:64152 - "GET /api/v1/books/jobs/807dd020-a35e-479c-b33b-a2324f7a2718/status HTTP/1.1" 200 OK
INFO:     127.0.0.1:64155 - "GET /api/v1/books/jobs/807dd020-a35e-479c-b33b-a2324f7a2718/status HTTP/1.1" 200 OK
INFO:     127.0.0.1:64158 - "GET /api/v1/books/jobs/807dd020-a35e-479c-b33b-a2324f7a2718/status HTTP/1.1" 200 OK
INFO:     127.0.0.1:64163 - "GET /api/v1/books/jobs/807dd020-a35e-479c-b33b-a2324f7a2718/status HTTP/1.1" 200 OK
INFO:     127.0.0.1:64170 - "GET /api/v1/books/jobs/807dd020-a35e-479c-b33b-a2324f7a2718/status HTTP/1.1" 200 OK
INFO:     127.0.0.1:64175 - "GET /api/v1/books/jobs/807dd020-a35e-479c-b33b-a2324f7a2718/status HTTP/1.1" 200 OK
INFO:     127.0.0.1:64180 - "GET /api/v1/books/jobs/807dd020-a35e-479c-b33b-a2324f7a2718/status HTTP/1.1" 200 OK
INFO:     127.0.0.1:64185 - "GET /api/v1/books/jobs/807dd020-a35e-479c-b33b-a2324f7a2718/status HTTP/1.1" 200 OK
INFO:     127.0.0.1:51011 - "GET /api/v1/books/jobs/807dd020-a35e-479c-b33b-a2324f7a2718/status HTTP/1.1" 200 OK
INFO:     127.0.0.1:51018 - "GET /api/v1/books/jobs/807dd020-a35e-479c-b33b-a2324f7a2718/status HTTP/1.1" 200 OK
INFO:     127.0.0.1:51023 - "GET /api/v1/books/jobs/807dd020-a35e-479c-b33b-a2324f7a2718/status HTTP/1.1" 200 OK
2025-10-28 15:27:36,111 - httpx - INFO - HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
2025-10-28 15:27:36,118 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=4534, 尝试次数=1
2025-10-28 15:27:36,122 - app.services.book_analysis_service - INFO - 💾 AI响应已保存到: D:\Java\ai_writer\backend\debug_ai_responses\ch2_第三章 初试锋芒.txt
2025-10-28 15:27:36,124 - app.services.book_analysis.web_novel_strategy - INFO - 🔍 开始解析AI响应,长度=4534
2025-10-28 15:27:36,124 - app.services.book_analysis.web_novel_strategy - INFO - ✅ 预处理: 已替换中文标点符号
2025-10-28 15:27:36,126 - app.services.book_analysis.web_novel_strategy - INFO - ✅ 直接解析JSON成功
2025-10-28 15:27:36,127 - app.services.book_analysis_service - INFO - ✅ 章节2 '第三章 初试锋芒' 分析成功,获得 11 个维度
2025-10-28 15:27:36,129 - app.services.redis_cache_service - INFO - ✓ 结果已缓存: novel_analysis:book_breakdown:da... (TTL: 604800秒)
2025-10-28 15:27:36,646 - app.services.book_analysis_service - INFO - ✅ 深度分析完成, 建立了 11 个维度的基础
2025-10-28 15:27:36,646 - app.services.book_analysis_service - INFO - 📊 章节分析全部完成, 共11个维度
2025-10-28 15:27:36,648 - app.services.book_analysis_service - INFO - 📚 开始提取知识点,共 11 个维度
2025-10-28 15:27:36,650 - app.services.book_analysis_service - INFO -   - 维度 'core_selling_point': dimension_type=technique
2025-10-28 15:27:36,650 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 核心卖点 (类别: technique)
2025-10-28 15:27:36,650 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=💡 核心卖点
2025-10-28 15:27:36,678 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=f69d5e01-eec8-4ae7-814a-85b85e31edc3
2025-10-28 15:27:36,678 - app.services.book_analysis_service - INFO -   - 维度 'protagonist_setting': dimension_type=character_template
2025-10-28 15:27:36,680 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 主角设定 (类别: character)
2025-10-28 15:27:36,680 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=👤 主角设定
2025-10-28 15:27:36,692 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=099941b1-2ec9-4d25-bf13-da5e8164ea9a
2025-10-28 15:27:36,693 - app.services.book_analysis_service - INFO -   - 维度 'cheat_system': dimension_type=power_system
2025-10-28 15:27:36,693 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 金手指系统 (类别: worldview)
2025-10-28 15:27:36,693 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=🌍 金手指系统
2025-10-28 15:27:36,706 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=48ebac8b-af22-4536-8e9f-37fcf7f16d24
2025-10-28 15:27:36,706 - app.services.book_analysis_service - INFO -   - 维度 'world_framework': dimension_type=setting
2025-10-28 15:27:36,707 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 世界观框架 (类别: worldview)
2025-10-28 15:27:36,707 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=🌍 世界观框架
2025-10-28 15:27:36,717 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=7ef36a2c-1b41-45bf-9a90-8bd1a0ea27b8
2025-10-28 15:27:36,718 - app.services.book_analysis_service - INFO -   - 维度 'power_system': dimension_type=power_system
2025-10-28 15:27:36,719 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 等级力量体系 (类别: worldview)
2025-10-28 15:27:36,719 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=🌍 等级力量体系
2025-10-28 15:27:36,731 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=cfd2894b-95ec-4294-90ba-6d1616b22c6e
2025-10-28 15:27:36,732 - app.services.book_analysis_service - INFO -   - 维度 'antagonist_forces': dimension_type=character_template
2025-10-28 15:27:36,732 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 反派势力 (类别: character)
2025-10-28 15:27:36,732 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=👤 反派势力
2025-10-28 15:27:36,744 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=13a1e633-a368-4ddd-ae65-c8e7d546fe65
2025-10-28 15:27:36,745 - app.services.book_analysis_service - INFO -   - 维度 'romance_line': dimension_type=relationship
2025-10-28 15:27:36,745 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 情感线设定 (类别: plot)
2025-10-28 15:27:36,746 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=📖 情感线设定
2025-10-28 15:27:36,760 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=82836e96-ec1c-4d92-83c2-e17d40a01a2e
2025-10-28 15:27:36,761 - app.services.book_analysis_service - INFO -   - 维度 'satisfaction_points': dimension_type=technique
2025-10-28 15:27:36,761 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 爽点布局 (类别: technique)
2025-10-28 15:27:36,762 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=💡 爽点布局
2025-10-28 15:27:36,774 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=895b118e-fad2-48e6-a637-a3f0af0434cd
2025-10-28 15:27:36,775 - app.services.book_analysis_service - INFO -   - 维度 'anticipation_hooks': dimension_type=technique
2025-10-28 15:27:36,775 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 期待感钩子 (类别: technique)
2025-10-28 15:27:36,775 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=💡 期待感钩子
2025-10-28 15:27:36,786 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=eeb6a3ba-dcec-4428-95a0-e9fe3154d067
2025-10-28 15:27:36,786 - app.services.book_analysis_service - INFO -   - 维度 'sub_plots': dimension_type=plot_structure
2025-10-28 15:27:36,787 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 支线剧情 (类别: plot)
2025-10-28 15:27:36,787 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=📖 支线剧情
2025-10-28 15:27:36,798 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=37d93f71-965b-4143-80f9-4832a75ea158
2025-10-28 15:27:36,798 - app.services.book_analysis_service - INFO -   - 维度 'unique_features': dimension_type=technique
2025-10-28 15:27:36,800 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 特色设定 (类别: technique)
2025-10-28 15:27:36,800 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=💡 特色设定
2025-10-28 15:27:36,815 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=3b6a5dbc-3067-4992-9e68-5d060c9ff599
2025-10-28 15:27:36,816 - app.services.book_analysis_service - INFO - 🚀 开始批量向量化 11 个知识条目...
2025-10-28 15:27:36,816 - app.services.vector_store_service - INFO - 🚀 开始批量向量化 11 个知识条目
Batches: 100%|█████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  1.34it/s]
2025-10-28 15:27:37,658 - app.services.vector_store_service - INFO - ✅ 批量向量化完成: 11个条目, 耗时: 0.84秒
2025-10-28 15:27:37,658 - app.services.book_analysis_service - INFO - ✅ 批量向量化成功
2025-10-28 15:27:37,660 - app.services.book_analysis_service - INFO - 📚 知识点提取完成,共创建 11 个知识条目
2025-10-28 15:27:37,660 - app.services.book_analysis_service - INFO -    - 相比旧策略,覆盖率提升: 从2个类型扩展到所有维度
2025-10-28 15:27:37,666 - app.services.book_analysis_service - INFO - 💡 开始生成智能建议,共 11 个维度
2025-10-28 15:27:37,666 - app.services.book_analysis.suggestion_generator - INFO - 🎯 开始生成建议,共 11 个维度
2025-10-28 15:27:37,666 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'core_selling_point': dimension_type=technique
2025-10-28 15:27:37,666 - app.services.book_analysis.suggestion_generator - INFO -     ❌ 维度类型不可关联,跳过
2025-10-28 15:27:37,668 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'protagonist_setting': dimension_type=character_template
2025-10-28 15:27:37,668 - app.services.book_analysis.suggestion_generator - INFO -     ✅ 创建建议: character, 置信度=0.75
2025-10-28 15:27:37,669 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'cheat_system': dimension_type=power_system
2025-10-28 15:27:37,670 - app.services.book_analysis.suggestion_generator - INFO -     ✅ 创建建议: power_system, 置信度=0.65
2025-10-28 15:27:37,670 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'world_framework': dimension_type=setting
2025-10-28 15:27:37,671 - app.services.book_analysis.suggestion_generator - INFO -     ✅ 创建建议: setting, 置信度=0.60
2025-10-28 15:27:37,671 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'power_system': dimension_type=power_system
2025-10-28 15:27:37,672 - app.services.book_analysis.suggestion_generator - INFO -     ✅ 创建建议: power_system, 置信度=0.60
2025-10-28 15:27:37,672 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'antagonist_forces': dimension_type=character_template
2025-10-28 15:27:37,673 - app.services.book_analysis.suggestion_generator - INFO -     ✅ 创建建议: character, 置信度=0.65
2025-10-28 15:27:37,673 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'romance_line': dimension_type=relationship
2025-10-28 15:27:37,674 - app.services.book_analysis.suggestion_generator - INFO -     ✅ 创建建议: relationship, 置信度=0.60
2025-10-28 15:27:37,674 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'satisfaction_points': dimension_type=technique
2025-10-28 15:27:37,675 - app.services.book_analysis.suggestion_generator - INFO -     ❌ 维度类型不可关联,跳过
2025-10-28 15:27:37,676 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'anticipation_hooks': dimension_type=technique
2025-10-28 15:27:37,676 - app.services.book_analysis.suggestion_generator - INFO -     ❌ 维度类型不可关联,跳过
2025-10-28 15:27:37,677 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'sub_plots': dimension_type=plot_structure
2025-10-28 15:27:37,677 - app.services.book_analysis.suggestion_generator - INFO -     ❌ 维度类型不可关联,跳过
2025-10-28 15:27:37,678 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'unique_features': dimension_type=technique
2025-10-28 15:27:37,678 - app.services.book_analysis.suggestion_generator - INFO -     ❌ 维度类型不可关联,跳过
2025-10-28 15:27:37,679 - app.services.book_analysis.suggestion_generator - INFO - 🎯 建议生成完成,共 6 个
2025-10-28 15:27:37,679 - app.services.book_analysis_service - INFO - 💡 建议生成器返回 6 个建议
2025-10-28 15:27:37,691 - app.services.book_analysis_service - INFO - 💡 智能建议生成完成,共创建 6 个建议
2025-10-28 15:27:37,708 - app.api.v1.endpoints.books - INFO - 🎉 图书分析任务完成: job_id=807dd020-a35e-479c-b33b-a2324f7a2718
INFO:     127.0.0.1:51026 - "GET /api/v1/books/jobs/807dd020-a35e-479c-b33b-a2324f7a2718/status HTTP/1.1" 200 OK
2025-10-28 15:27:39,417 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: qwen3-32b, Timeout: 60s
INFO:     127.0.0.1:51029 - "POST /api/v1/books/upload HTTP/1.1" 200 OK
2025-10-28 15:27:39,457 - app.api.v1.endpoints.books - INFO - 🚀 开始执行后台分析任务: job_id=f4a6520c-f6df-4f1b-a75a-da9c7f47bdd7, user_id=602f5147-846a-4cde-95d3-405fa75f133f
2025-10-28 15:27:39,459 - app.api.v1.endpoints.books - INFO - ✅ 数据库会话创建成功
2025-10-28 15:27:40,791 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: qwen3-32b, Timeout: 60s
2025-10-28 15:27:40,791 - app.api.v1.endpoints.books - INFO - ✅ AI服务初始化成功
2025-10-28 15:27:40,793 - app.api.v1.endpoints.books - INFO - ✅ 知识库服务初始化成功
2025-10-28 15:27:40,793 - app.api.v1.endpoints.books - INFO - ✅ 图书分析服务初始化成功,开始分析...
2025-10-28 15:27:40,793 - app.services.book_analysis_service - INFO - 📖 analyze_book 开始: job_id=f4a6520c-f6df-4f1b-a75a-da9c7f47bdd7, user_id=602f5147-846a-4cde-95d3-405fa75f133f
2025-10-28 15:27:40,801 - app.services.book_analysis_service - INFO - ✅ 获取到任务: test_cache_v2_1761636458.txt, file_path=uploads\books\f3c0d2b6-51ff-492f-92ca-8b94339c097a.txt
2025-10-28 15:27:40,807 - app.services.book_analysis_service - INFO - 📄 开始解析文件: uploads\books\f3c0d2b6-51ff-492f-92ca-8b94339c097a.txt
2025-10-28 15:27:40,807 - app.services.book_analysis.smart_sampling - INFO - 🔍 准备解析文件: uploads\books\f3c0d2b6-51ff-492f-92ca-8b94339c097a.txt
2025-10-28 15:27:40,808 - app.services.book_analysis.smart_sampling - INFO - 📁 文件是否存在: True
2025-10-28 15:27:40,808 - app.services.book_analysis.smart_sampling - INFO - 📏 文件大小: 1132 字节
2025-10-28 15:27:40,810 - app.services.book_analysis.smart_sampling - INFO - 📖 读取内容长度: 460 字符
2025-10-28 15:27:40,810 - app.services.book_analysis.smart_sampling - INFO - 📝 内容前200字符: [测试版本: v2 | 时间戳: 1761636458 | ID: 0]

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
2025-10-28 15:27:40,811 - app.services.book_analysis.smart_sampling - INFO - 🔎 正则匹配结果: 找到 3 个章节标题
2025-10-28 15:27:40,811 - app.services.book_analysis.smart_sampling - INFO -   匹配1: '第一章 测试章节' at position 38
2025-10-28 15:27:40,812 - app.services.book_analysis.smart_sampling - INFO -   匹配2: '第二章 系统觉醒' at position 132
2025-10-28 15:27:40,812 - app.services.book_analysis.smart_sampling - INFO -   匹配3: '第三章 初试锋芒' at position 274
2025-10-28 15:27:40,812 - app.services.book_analysis.smart_sampling - INFO -   ⏭️ 跳过章节 '第一章 测试章节': 长度82字符 < 最小长度100
2025-10-28 15:27:40,813 - app.services.book_analysis.smart_sampling - INFO -   ✅ 保留章节 '第二章 系统觉醒': 130字符
2025-10-28 15:27:40,813 - app.services.book_analysis.smart_sampling - INFO -   ✅ 保留章节 '第三章 初试锋芒': 175字符
2025-10-28 15:27:40,813 - app.services.book_analysis.smart_sampling - INFO - ✨ 最终保留 2 个有效章节
2025-10-28 15:27:40,815 - app.services.book_analysis_service - INFO - 📊 解析完成,识别到 2 个章节
2025-10-28 15:27:40,815 - app.services.book_analysis_service - INFO -   章节1: 第二章 系统觉醒 (130字)
2025-10-28 15:27:40,815 - app.services.book_analysis_service - INFO -   章节2: 第三章 初试锋芒 (175字)
2025-10-28 15:27:40,836 - app.services.book_analysis_service - INFO - 📊 开始分析 2 个章节: 2个深度分析(串行), 0个增量分析(并行)
2025-10-28 15:27:40,844 - app.services.book_analysis_service - INFO - 🔍 深度分析章节 1: 第二章 系统觉醒
2025-10-28 15:27:40,845 - app.services.book_analysis_service - INFO - ✅ Redis缓存服务初始化成功
2025-10-28 15:27:40,846 - app.services.redis_cache_service - INFO - ✓ 缓存命中: novel_analysis:book_breakdown:a6...
2025-10-28 15:27:40,847 - app.services.book_analysis_service - INFO - ✅ 缓存命中! 章节1 '第二章 系统觉醒' (跳过AI调用)
2025-10-28 15:27:41,358 - app.services.book_analysis_service - INFO - 🔍 深度分析章节 2: 第三章 初试锋芒
2025-10-28 15:27:41,360 - app.services.redis_cache_service - INFO - ✓ 缓存命中: novel_analysis:book_breakdown:da...
2025-10-28 15:27:41,361 - app.services.book_analysis_service - INFO - ✅ 缓存命中! 章节2 '第三章 初试锋芒' (跳过AI调用)
2025-10-28 15:27:41,871 - app.services.book_analysis_service - INFO - ✅ 深度分析完成, 建立了 11 个维度的基础
2025-10-28 15:27:41,873 - app.services.book_analysis_service - INFO - 📊 章节分析全部完成, 共11个维度
2025-10-28 15:27:41,875 - app.services.book_analysis_service - INFO - 📚 开始提取知识点,共 11 个维度
2025-10-28 15:27:41,875 - app.services.book_analysis_service - INFO -   - 维度 'core_selling_point': dimension_type=technique
2025-10-28 15:27:41,875 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 核心卖点 (类别: technique)
2025-10-28 15:27:41,877 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=💡 核心卖点
2025-10-28 15:27:41,902 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=ad5d2ce1-4d18-487e-ba38-3b73928de40c
2025-10-28 15:27:41,903 - app.services.book_analysis_service - INFO -   - 维度 'protagonist_setting': dimension_type=character_template
2025-10-28 15:27:41,904 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 主角设定 (类别: character)
2025-10-28 15:27:41,905 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=👤 主角设定
2025-10-28 15:27:41,919 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=b45a44f2-7582-49f4-a30a-ab3f47dcb869
2025-10-28 15:27:41,920 - app.services.book_analysis_service - INFO -   - 维度 'cheat_system': dimension_type=power_system
2025-10-28 15:27:41,921 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 金手指系统 (类别: worldview)
2025-10-28 15:27:41,921 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=🌍 金手指系统
2025-10-28 15:27:41,934 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=44dff86f-6b3f-49e0-96af-725752c7471f
2025-10-28 15:27:41,934 - app.services.book_analysis_service - INFO -   - 维度 'world_framework': dimension_type=setting
2025-10-28 15:27:41,934 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 世界观框架 (类别: worldview)
2025-10-28 15:27:41,935 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=🌍 世界观框架
2025-10-28 15:27:41,945 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=592075d9-9b37-440d-a3a8-a6852a4e0a68
2025-10-28 15:27:41,946 - app.services.book_analysis_service - INFO -   - 维度 'power_system': dimension_type=power_system
2025-10-28 15:27:41,946 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 等级力量体系 (类别: worldview)
2025-10-28 15:27:41,947 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=🌍 等级力量体系
2025-10-28 15:27:41,960 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=668a9df7-8d4a-4f84-8f03-8ff13012a613
2025-10-28 15:27:41,960 - app.services.book_analysis_service - INFO -   - 维度 'antagonist_forces': dimension_type=character_template
2025-10-28 15:27:41,961 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 反派势力 (类别: character)
2025-10-28 15:27:41,961 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=👤 反派势力
2025-10-28 15:27:41,972 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=ed495132-4e53-4736-b353-d908bc956ca7
2025-10-28 15:27:41,972 - app.services.book_analysis_service - INFO -   - 维度 'romance_line': dimension_type=relationship
2025-10-28 15:27:41,972 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 情感线设定 (类别: plot)
2025-10-28 15:27:41,974 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=📖 情感线设定
2025-10-28 15:27:41,983 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=160f4089-87e9-4692-961e-bbe53a6421ac
2025-10-28 15:27:41,984 - app.services.book_analysis_service - INFO -   - 维度 'satisfaction_points': dimension_type=technique
2025-10-28 15:27:41,985 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 爽点布局 (类别: technique)
2025-10-28 15:27:41,985 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=💡 爽点布局
2025-10-28 15:27:41,996 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=c4dd0cf8-f2b9-47e9-b96c-7016f899062d
2025-10-28 15:27:41,997 - app.services.book_analysis_service - INFO -   - 维度 'anticipation_hooks': dimension_type=technique
2025-10-28 15:27:41,997 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 期待感钩子 (类别: technique)
2025-10-28 15:27:41,997 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=💡 期待感钩子
2025-10-28 15:27:42,007 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=c31d50b5-457b-4084-9643-826c4fc6c3b3
2025-10-28 15:27:42,007 - app.services.book_analysis_service - INFO -   - 维度 'sub_plots': dimension_type=plot_structure
2025-10-28 15:27:42,007 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 支线剧情 (类别: plot)
2025-10-28 15:27:42,007 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=📖 支线剧情
2025-10-28 15:27:42,018 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=d9160f47-6349-4781-95d6-82882136c1b8
2025-10-28 15:27:42,019 - app.services.book_analysis_service - INFO -   - 维度 'unique_features': dimension_type=technique
2025-10-28 15:27:42,019 - app.services.book_analysis_service - INFO -     ✅ 创建知识点: 特色设定 (类别: technique)
2025-10-28 15:27:42,020 - app.services.knowledge_service - INFO - 创建知识条目: user_id=602f5147-846a-4cde-95d3-405fa75f133f, title=💡 特色设定
2025-10-28 15:27:42,030 - app.services.knowledge_service - INFO - 知识条目创建成功: item_id=8f5061cf-1f95-45a2-b233-efdaf3b42ef0
2025-10-28 15:27:42,030 - app.services.book_analysis_service - INFO - 🚀 开始批量向量化 11 个知识条目...
2025-10-28 15:27:42,032 - app.services.vector_store_service - INFO - 🚀 开始批量向量化 11 个知识条目
Batches: 100%|█████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  1.35it/s]
2025-10-28 15:27:42,880 - app.services.vector_store_service - INFO - ✅ 批量向量化完成: 11个条目, 耗时: 0.85秒
2025-10-28 15:27:42,881 - app.services.book_analysis_service - INFO - ✅ 批量向量化成功
2025-10-28 15:27:42,881 - app.services.book_analysis_service - INFO - 📚 知识点提取完成,共创建 11 个知识条目
2025-10-28 15:27:42,882 - app.services.book_analysis_service - INFO -    - 相比旧策略,覆盖率提升: 从2个类型扩展到所有维度
2025-10-28 15:27:42,887 - app.services.book_analysis_service - INFO - 💡 开始生成智能建议,共 11 个维度
2025-10-28 15:27:42,887 - app.services.book_analysis.suggestion_generator - INFO - 🎯 开始生成建议,共 11 个维度
2025-10-28 15:27:42,888 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'core_selling_point': dimension_type=technique
2025-10-28 15:27:42,888 - app.services.book_analysis.suggestion_generator - INFO -     ❌ 维度类型不可关联,跳过
2025-10-28 15:27:42,888 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'protagonist_setting': dimension_type=character_template
2025-10-28 15:27:42,889 - app.services.book_analysis.suggestion_generator - INFO -     ✅ 创建建议: character, 置信度=0.75
2025-10-28 15:27:42,889 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'cheat_system': dimension_type=power_system
2025-10-28 15:27:42,889 - app.services.book_analysis.suggestion_generator - INFO -     ✅ 创建建议: power_system, 置信度=0.65
2025-10-28 15:27:42,890 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'world_framework': dimension_type=setting
2025-10-28 15:27:42,890 - app.services.book_analysis.suggestion_generator - INFO -     ✅ 创建建议: setting, 置信度=0.60
2025-10-28 15:27:42,890 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'power_system': dimension_type=power_system
2025-10-28 15:27:42,891 - app.services.book_analysis.suggestion_generator - INFO -     ✅ 创建建议: power_system, 置信度=0.60
2025-10-28 15:27:42,891 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'antagonist_forces': dimension_type=character_template
2025-10-28 15:27:42,892 - app.services.book_analysis.suggestion_generator - INFO -     ✅ 创建建议: character, 置信度=0.65
2025-10-28 15:27:42,892 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'romance_line': dimension_type=relationship
2025-10-28 15:27:42,892 - app.services.book_analysis.suggestion_generator - INFO -     ✅ 创建建议: relationship, 置信度=0.60
2025-10-28 15:27:42,893 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'satisfaction_points': dimension_type=technique
2025-10-28 15:27:42,894 - app.services.book_analysis.suggestion_generator - INFO -     ❌ 维度类型不可关联,跳过
2025-10-28 15:27:42,894 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'anticipation_hooks': dimension_type=technique
2025-10-28 15:27:42,894 - app.services.book_analysis.suggestion_generator - INFO -     ❌ 维度类型不可关联,跳过
2025-10-28 15:27:42,894 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'sub_plots': dimension_type=plot_structure
2025-10-28 15:27:42,894 - app.services.book_analysis.suggestion_generator - INFO -     ❌ 维度类型不可关联,跳过
2025-10-28 15:27:42,895 - app.services.book_analysis.suggestion_generator - INFO -   - 维度 'unique_features': dimension_type=technique
2025-10-28 15:27:42,895 - app.services.book_analysis.suggestion_generator - INFO -     ❌ 维度类型不可关联,跳过
2025-10-28 15:27:42,895 - app.services.book_analysis.suggestion_generator - INFO - 🎯 建议生成完成,共 6 个
2025-10-28 15:27:42,896 - app.services.book_analysis_service - INFO - 💡 建议生成器返回 6 个建议
2025-10-28 15:27:42,926 - app.services.book_analysis_service - INFO - 💡 智能建议生成完成,共创建 6 个建议
2025-10-28 15:27:42,940 - app.api.v1.endpoints.books - INFO - 🎉 图书分析任务完成: job_id=f4a6520c-f6df-4f1b-a75a-da9c7f47bdd7
