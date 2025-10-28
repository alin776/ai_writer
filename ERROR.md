(venv) PS D:\Java\ai_writer\backend> python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
INFO:     Will watch for changes in these directories: ['D:\\Java\\ai_writer\\backend']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [32976] using WatchFiles
已注册策略: web_novel_11d - 网文11维度分析
INFO:     Started server process [25836]
INFO:     Waiting for application startup.
2025-10-28 08:14:33,050 - app.main - INFO - 🚀 应用启动中...
2025-10-28 08:14:33,050 - app.core.database - INFO - 正在初始化数据库... (尝试 1/3)
2025-10-28 08:14:33,154 - app.core.database - INFO - ✅ 数据库初始化成功
2025-10-28 08:14:33,154 - apscheduler.scheduler - INFO - Adding job tentatively -- it will be properly scheduled when the scheduler starts
2025-10-28 08:14:33,154 - apscheduler.scheduler - INFO - Added job "清理过期的去痕迹会话详情" to job store "default"
2025-10-28 08:14:33,154 - apscheduler.scheduler - INFO - Scheduler started
2025-10-28 08:14:33,154 - app.tasks.cleanup_humanize_details - INFO - 定时任务调度器已启动
2025-10-28 08:14:33,154 - app.main - INFO - 🔄 开始预加载Embedding模型...
2025-10-28 08:14:33,154 - app.services.vector_store_service - INFO - 🔄 预加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
2025-10-28 08:14:33,154 - sentence_transformers.SentenceTransformer - INFO - Use pytorch device_name: cpu
2025-10-28 08:14:33,154 - sentence_transformers.SentenceTransformer - INFO - Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
2025-10-28 08:14:40,523 - app.services.vector_store_service - INFO - ✅ Embedding模型预加载成功，耗时: 7.37秒
2025-10-28 08:14:40,523 - app.main - INFO - ✅ Embedding模型预加载完成
2025-10-28 08:14:40,523 - app.main - INFO - ✅ 应用启动完成
INFO:     Application startup complete.
INFO:     127.0.0.1:59228 - "POST /api/v1/auth/login HTTP/1.1" 200 OK
INFO:     127.0.0.1:59232 - "GET /api/v1/works?skip=0&limit=10 HTTP/1.1" 200 OK
2025-10-28 08:14:42,897 - app.api.v1.chapters - INFO - [GET chapters] work_id=ddc0183e-76f5-4187-a491-9692a341996b, user_id=602f5147-846a-4cde-95d3-405fa75f133f
2025-10-28 08:14:42,907 - app.services.chapter_service - INFO - [ChapterService] Querying chapters for work_id=ddc0183e-76f5-4187-a491-9692a341996b, type=<class 'uuid.UUID'>
2025-10-28 08:14:42,918 - app.services.chapter_service - INFO - [ChapterService] Found 20 chapters
2025-10-28 08:14:42,918 - app.services.chapter_service - INFO -   - Chapter: 第1章 修炼之路, order=1
2025-10-28 08:14:42,919 - app.services.chapter_service - INFO -   - Chapter: 第2章 修炼之路, order=2
2025-10-28 08:14:42,919 - app.services.chapter_service - INFO -   - Chapter: 第3章 修炼之路, order=3
2025-10-28 08:14:42,919 - app.services.chapter_service - INFO -   - Chapter: 第4章 修炼之路, order=4
2025-10-28 08:14:42,919 - app.services.chapter_service - INFO -   - Chapter: 第5章 修炼之路, order=5
2025-10-28 08:14:42,919 - app.services.chapter_service - INFO -   - Chapter: 第6章 修炼之路, order=6
2025-10-28 08:14:42,919 - app.services.chapter_service - INFO -   - Chapter: 第7章 修炼之路, order=7
2025-10-28 08:14:42,919 - app.services.chapter_service - INFO -   - Chapter: 第8章 修炼之路, order=8
2025-10-28 08:14:42,919 - app.services.chapter_service - INFO -   - Chapter: 第9章 修炼之路, order=9
2025-10-28 08:14:42,919 - app.services.chapter_service - INFO -   - Chapter: 第10章 修炼之路, order=10
2025-10-28 08:14:42,919 - app.services.chapter_service - INFO -   - Chapter: 第11章 修炼之路, order=11
2025-10-28 08:14:42,919 - app.services.chapter_service - INFO -   - Chapter: 第12章 修炼之路, order=12
2025-10-28 08:14:42,919 - app.services.chapter_service - INFO -   - Chapter: 第13章 修炼之路, order=13
2025-10-28 08:14:42,919 - app.services.chapter_service - INFO -   - Chapter: 第14章 修炼之路, order=14
2025-10-28 08:14:42,919 - app.services.chapter_service - INFO -   - Chapter: 第15章 修炼之路, order=15
2025-10-28 08:14:42,919 - app.services.chapter_service - INFO -   - Chapter: 第16章 修炼之路, order=16
2025-10-28 08:14:42,919 - app.services.chapter_service - INFO -   - Chapter: 第17章 修炼之路, order=17
2025-10-28 08:14:42,919 - app.services.chapter_service - INFO -   - Chapter: 第18章 修炼之路, order=18
2025-10-28 08:14:42,919 - app.services.chapter_service - INFO -   - Chapter: 第19章 修炼之路, order=19
2025-10-28 08:14:42,919 - app.services.chapter_service - INFO -   - Chapter: 第20章 修炼之路, order=20
2025-10-28 08:14:42,919 - app.api.v1.chapters - INFO - [GET chapters] Returning 20 chapters
INFO:     127.0.0.1:59236 - "GET /api/v1/chapters/work/ddc0183e-76f5-4187-a491-9692a341996b HTTP/1.1" 200 OK
2025-10-28 08:14:42,935 - app.api.v1.review - INFO - [POST /review/books] user_id=602f5147-846a-4cde-95d3-405fa75f133f, novel_id=ddc0183e-76f5-4187-a491-9692a341996b, chapters=5, quick_mode=False
2025-10-28 08:14:42,938 - app.services.ai.prompts - INFO - Prompts loaded successfully from D:\Java\ai_writer\backend\app\services\ai\prompts\default.json
2025-10-28 08:14:43,655 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-flash, Timeout: 60s
2025-10-28 08:14:43,655 - app.services.review.book_review_analyzer - INFO - [BookReviewAnalyzer] 初始化完成, 使用模型: gemini-2.5-flash, 超时: 60秒
2025-10-28 08:14:43,668 - app.services.review.book_review_service - INFO - [BookReviewService] 开始评审作品: 测试作品 (5章), 章节数=5
2025-10-28 08:14:43,669 - app.services.review.book_review_service - INFO - ⚠️ 缓存未命中: book_review:review_book:9df7c9a6c9f4ee63
2025-10-28 08:14:43,669 - app.services.review.book_review_analyzer - INFO - [BookReviewAnalyzer] 开始分析作品: 测试作品 (5章), 章节数=5
2025-10-28 08:14:43,669 - app.services.review.book_review_analyzer - INFO - [BookReviewAnalyzer] 并发执行4个维度分析...
2025-10-28 08:14:43,669 - app.services.review.book_review_analyzer - INFO - [BookReviewAnalyzer] 开始情节结构分析
2025-10-28 08:14:43,669 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=2000, temp=0.7, 尝试=1/3
2025-10-28 08:14:43,671 - app.services.review.book_review_analyzer - INFO - [BookReviewAnalyzer] 开始人物分析
2025-10-28 08:14:43,671 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=2000, temp=0.7, 尝试=1/3
2025-10-28 08:14:43,671 - app.services.review.book_review_analyzer - INFO - [BookReviewAnalyzer] 开始世界观分析
2025-10-28 08:14:43,671 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=1500, temp=0.7, 尝试=1/3
2025-10-28 08:14:43,671 - app.services.review.book_review_analyzer - INFO - [BookReviewAnalyzer] 开始文风分析
2025-10-28 08:14:43,673 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=1500, temp=0.7, 尝试=1/3
2025-10-28 08:14:57,842 - httpx - INFO - HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
2025-10-28 08:14:57,848 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=1099, 尝试次数=1
2025-10-28 08:14:57,848 - app.utils.json_parser - INFO - [BookReviewAnalyzer] 🔍 开始解析AI响应, 长度=1099
2025-10-28 08:14:57,848 - app.utils.json_parser - INFO - [BookReviewAnalyzer] ✅ 预处理: 已替换中文标点符号
2025-10-28 08:14:57,851 - app.utils.json_parser - INFO - [BookReviewAnalyzer] 🔍 方法2: 从markdown代码块提取JSON, 长度=1087
2025-10-28 08:14:57,851 - app.utils.json_parser - INFO - [BookReviewAnalyzer] ✅ 方法2成功: markdown代码块解析
2025-10-28 08:15:04,742 - httpx - INFO - HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
2025-10-28 08:15:04,744 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=1912, 尝试次数=1
2025-10-28 08:15:04,744 - app.utils.json_parser - INFO - [BookReviewAnalyzer] 🔍 开始解析AI响应, 长度=1912
2025-10-28 08:15:04,744 - app.utils.json_parser - INFO - [BookReviewAnalyzer] ✅ 预处理: 已替换中文标点符号
2025-10-28 08:15:04,744 - app.utils.json_parser - INFO - [BookReviewAnalyzer] 🔍 方法2: 从markdown代码块提取JSON, 长度=1900
2025-10-28 08:15:04,744 - app.utils.json_parser - INFO - [BookReviewAnalyzer] ✅ 方法2成功: markdown代码块解析
2025-10-28 08:15:05,411 - httpx - INFO - HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
2025-10-28 08:15:05,413 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=928, 尝试次数=1
2025-10-28 08:15:05,413 - app.utils.json_parser - INFO - [BookReviewAnalyzer] 🔍 开始解析AI响应, 长度=928
2025-10-28 08:15:05,413 - app.utils.json_parser - INFO - [BookReviewAnalyzer] 🔍 方法2: 从markdown代码块提取JSON, 长度=916
2025-10-28 08:15:05,413 - app.utils.json_parser - INFO - [BookReviewAnalyzer] ✅ 方法2成功: markdown代码块解析
2025-10-28 08:15:06,088 - httpx - INFO - HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
2025-10-28 08:15:06,090 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=968, 尝试次数=1
2025-10-28 08:15:06,090 - app.utils.json_parser - INFO - [BookReviewAnalyzer] 🔍 开始解析AI响应, 长度=968
2025-10-28 08:15:06,090 - app.utils.json_parser - INFO - [BookReviewAnalyzer] ✅ 预处理: 已替换中文标点符号
2025-10-28 08:15:06,090 - app.utils.json_parser - INFO - [BookReviewAnalyzer] 🔍 方法2: 从markdown代码块提取JSON, 长度=956
2025-10-28 08:15:06,090 - app.utils.json_parser - INFO - [BookReviewAnalyzer] ✅ 方法2成功: markdown代码块解析
2025-10-28 08:15:06,090 - app.services.review.book_review_analyzer - INFO - [BookReviewAnalyzer] 4个维度分析完成,开始计算评分和建议
2025-10-28 08:15:06,090 - app.services.review.book_review_analyzer - INFO - [BookReviewAnalyzer] 生成综合建议
2025-10-28 08:15:06,090 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=1500, temp=0.8, 尝试=1/3
2025-10-28 08:15:27,514 - httpx - INFO - HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
2025-10-28 08:15:27,515 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=2288, 尝试次数=1
2025-10-28 08:15:27,515 - app.utils.json_parser - INFO - [BookReviewAnalyzer] 🔍 开始解析AI响应, 长度=2288
2025-10-28 08:15:27,515 - app.utils.json_parser - INFO - [BookReviewAnalyzer] ✅ 预处理: 已替换中文标点符号
2025-10-28 08:15:27,515 - app.utils.json_parser - INFO - [BookReviewAnalyzer] 🔍 方法2: 从markdown代码块提取JSON, 长度=2276
2025-10-28 08:15:27,515 - app.utils.json_parser - INFO - [BookReviewAnalyzer] ✅ 方法2成功: markdown代码块解析
2025-10-28 08:15:27,515 - app.services.review.book_review_analyzer - INFO - [BookReviewAnalyzer] 分析完成, 总分=39.9
2025-10-28 08:15:27,515 - app.services.review.book_review_service - INFO - 💾 缓存已保存: book_review:review_book:9df7c9a6c9f4ee63 (expire=7200s)
2025-10-28 08:15:27,515 - app.services.review.book_review_service - INFO - [BookReviewService] 评审完成, 总分=39.9
2025-10-28 08:15:27,515 - app.api.v1.review - INFO - [POST /review/books] 评审完成, novel_id=ddc0183e-76f5-4187-a491-9692a341996b, overall_score=39.9
INFO:     127.0.0.1:59239 - "POST /api/v1/review/books HTTP/1.1" 200 OK
2025-10-28 08:15:29,554 - app.api.v1.review - INFO - [POST /review/books] user_id=602f5147-846a-4cde-95d3-405fa75f133f, novel_id=ddc0183e-76f5-4187-a491-9692a341996b, chapters=5, quick_mode=False
2025-10-28 08:15:30,141 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-flash, Timeout: 60s
2025-10-28 08:15:30,141 - app.services.review.book_review_analyzer - INFO - [BookReviewAnalyzer] 初始化完成, 使用模型: gemini-2.5-flash, 超时: 60秒
2025-10-28 08:15:30,141 - app.services.review.book_review_service - INFO - [BookReviewService] 开始评审作品: 测试作品 (5章), 章节数=5
2025-10-28 08:15:30,145 - app.services.review.book_review_service - INFO - ✅ 缓存命中: book_review:review_book:9df7c9a6c9f4ee63
2025-10-28 08:15:30,145 - app.api.v1.review - INFO - [POST /review/books] 评审完成, novel_id=ddc0183e-76f5-4187-a491-9692a341996b, overall_score=39.9
INFO:     127.0.0.1:56032 - "POST /api/v1/review/books HTTP/1.1" 200 OK
2025-10-28 08:15:33,196 - app.api.v1.review - INFO - [POST /review/books] user_id=602f5147-846a-4cde-95d3-405fa75f133f, novel_id=ddc0183e-76f5-4187-a491-9692a341996b, chapters=10, quick_mode=False
2025-10-28 08:15:33,692 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-flash, Timeout: 60s
2025-10-28 08:15:33,692 - app.services.review.book_review_analyzer - INFO - [BookReviewAnalyzer] 初始化完成, 使用模型: gemini-2.5-flash, 超时: 60秒
2025-10-28 08:15:33,692 - app.services.review.book_review_service - INFO - [BookReviewService] 开始评审作品: 测试作品 (10章), 章节数=10
2025-10-28 08:15:33,695 - app.services.review.book_review_service - INFO - ⚠️ 缓存未命中: book_review:review_book:18a7d94e2f7d0bf7
2025-10-28 08:15:33,695 - app.services.review.book_review_analyzer - INFO - [BookReviewAnalyzer] 开始分析作品: 测试作品 (10章), 章节数=10
2025-10-28 08:15:33,695 - app.services.review.book_review_analyzer - INFO - [BookReviewAnalyzer] 并发执行4个维度分析...
2025-10-28 08:15:33,695 - app.services.review.book_review_analyzer - INFO - [BookReviewAnalyzer] 开始情节结构分析
2025-10-28 08:15:33,695 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=2000, temp=0.7, 尝试=1/3
2025-10-28 08:15:33,695 - app.services.review.book_review_analyzer - INFO - [BookReviewAnalyzer] 开始人物分析
2025-10-28 08:15:33,695 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=2000, temp=0.7, 尝试=1/3
2025-10-28 08:15:33,695 - app.services.review.book_review_analyzer - INFO - [BookReviewAnalyzer] 开始世界观分析
2025-10-28 08:15:33,695 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=1500, temp=0.7, 尝试=1/3
2025-10-28 08:15:33,695 - app.services.review.book_review_analyzer - INFO - [BookReviewAnalyzer] 开始文风分析
2025-10-28 08:15:33,695 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=1500, temp=0.7, 尝试=1/3
2025-10-28 08:15:48,581 - httpx - INFO - HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
2025-10-28 08:15:48,583 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=1791, 尝试次数=1
2025-10-28 08:15:48,583 - app.utils.json_parser - INFO - [BookReviewAnalyzer] 🔍 开始解析AI响应, 长度=1791
2025-10-28 08:15:48,583 - app.utils.json_parser - INFO - [BookReviewAnalyzer] ✅ 预处理: 已替换中文标点符号
2025-10-28 08:15:48,585 - app.utils.json_parser - INFO - [BookReviewAnalyzer] 🔍 方法2: 从markdown代码块提取JSON, 长度=1779
2025-10-28 08:15:48,586 - app.utils.json_parser - INFO - [BookReviewAnalyzer] ✅ 方法2成功: markdown代码块解析
2025-10-28 08:15:50,747 - httpx - INFO - HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
2025-10-28 08:15:50,748 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=1168, 尝试次数=1
2025-10-28 08:15:50,748 - app.utils.json_parser - INFO - [BookReviewAnalyzer] 🔍 开始解析AI响应, 长度=1168
2025-10-28 08:15:50,748 - app.utils.json_parser - INFO - [BookReviewAnalyzer] ✅ 预处理: 已替换中文标点符号
2025-10-28 08:15:50,748 - app.utils.json_parser - INFO - [BookReviewAnalyzer] 🔍 方法2: 从markdown代码块提取JSON, 长度=1156
2025-10-28 08:15:50,748 - app.utils.json_parser - INFO - [BookReviewAnalyzer] ✅ 方法2成功: markdown代码块解析
2025-10-28 08:15:56,541 - httpx - INFO - HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
2025-10-28 08:15:56,543 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=1256, 尝试次数=1
2025-10-28 08:15:56,544 - app.utils.json_parser - INFO - [BookReviewAnalyzer] 🔍 开始解析AI响应, 长度=1256
2025-10-28 08:15:56,544 - app.utils.json_parser - INFO - [BookReviewAnalyzer] ✅ 预处理: 已替换中文标点符号
2025-10-28 08:15:56,544 - app.utils.json_parser - INFO - [BookReviewAnalyzer] 🔍 方法2: 从markdown代码块提取JSON, 长度=1244
2025-10-28 08:15:56,544 - app.utils.json_parser - INFO - [BookReviewAnalyzer] ✅ 方法2成功: markdown代码块解析
2025-10-28 08:15:59,500 - httpx - INFO - HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
2025-10-28 08:15:59,502 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=954, 尝试次数=1
2025-10-28 08:15:59,502 - app.utils.json_parser - INFO - [BookReviewAnalyzer] 🔍 开始解析AI响应, 长度=954
2025-10-28 08:15:59,502 - app.utils.json_parser - INFO - [BookReviewAnalyzer] 🔍 方法2: 从markdown代码块提取JSON, 长度=942
2025-10-28 08:15:59,503 - app.utils.json_parser - INFO - [BookReviewAnalyzer] ✅ 方法2成功: markdown代码块解析
2025-10-28 08:15:59,503 - app.services.review.book_review_analyzer - INFO - [BookReviewAnalyzer] 4个维度分析完成,开始计算评分和建议
2025-10-28 08:15:59,504 - app.services.review.book_review_analyzer - INFO - [BookReviewAnalyzer] 生成综合建议
2025-10-28 08:15:59,505 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=1500, temp=0.8, 尝试=1/3
2025-10-28 08:16:25,766 - httpx - INFO - HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
2025-10-28 08:16:25,769 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=1949, 尝试次数=1
2025-10-28 08:16:25,770 - app.utils.json_parser - INFO - [BookReviewAnalyzer] 🔍 开始解析AI响应, 长度=1949
2025-10-28 08:16:25,770 - app.utils.json_parser - INFO - [BookReviewAnalyzer] ✅ 预处理: 已替换中文标点符号
2025-10-28 08:16:25,770 - app.utils.json_parser - INFO - [BookReviewAnalyzer] 🔍 方法2: 从markdown代码块提取JSON, 长度=1937
2025-10-28 08:16:25,771 - app.utils.json_parser - INFO - [BookReviewAnalyzer] ✅ 方法2成功: markdown代码块解析
2025-10-28 08:16:25,771 - app.services.review.book_review_analyzer - INFO - [BookReviewAnalyzer] 分析完成, 总分=39.8
2025-10-28 08:16:25,771 - app.services.review.book_review_service - INFO - 💾 缓存已保存: book_review:review_book:18a7d94e2f7d0bf7 (expire=7200s)
2025-10-28 08:16:25,771 - app.services.review.book_review_service - INFO - [BookReviewService] 评审完成, 总分=39.8
2025-10-28 08:16:25,773 - app.api.v1.review - INFO - [POST /review/books] 评审完成, novel_id=ddc0183e-76f5-4187-a491-9692a341996b, overall_score=39.8
INFO:     127.0.0.1:56066 - "POST /api/v1/review/books HTTP/1.1" 200 OK
2025-10-28 08:16:27,826 - app.api.v1.review - INFO - [POST /review/books] user_id=602f5147-846a-4cde-95d3-405fa75f133f, novel_id=ddc0183e-76f5-4187-a491-9692a341996b, chapters=10, quick_mode=False
2025-10-28 08:16:28,319 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-flash, Timeout: 60s
2025-10-28 08:16:28,319 - app.services.review.book_review_analyzer - INFO - [BookReviewAnalyzer] 初始化完成, 使用模型: gemini-2.5-flash, 超时: 60秒
2025-10-28 08:16:28,319 - app.services.review.book_review_service - INFO - [BookReviewService] 开始评审作品: 测试作品 (10章), 章节数=10
2025-10-28 08:16:28,319 - app.services.review.book_review_service - INFO - ✅ 缓存命中: book_review:review_book:18a7d94e2f7d0bf7
2025-10-28 08:16:28,319 - app.api.v1.review - INFO - [POST /review/books] 评审完成, novel_id=ddc0183e-76f5-4187-a491-9692a341996b, overall_score=39.8
INFO:     127.0.0.1:57457 - "POST /api/v1/review/books HTTP/1.1" 200 OK
2025-10-28 08:16:31,350 - app.api.v1.review - INFO - [POST /review/books] user_id=602f5147-846a-4cde-95d3-405fa75f133f, novel_id=ddc0183e-76f5-4187-a491-9692a341996b, chapters=20, quick_mode=False
2025-10-28 08:16:31,832 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-flash, Timeout: 60s
2025-10-28 08:16:31,832 - app.services.review.book_review_analyzer - INFO - [BookReviewAnalyzer] 初始化完成, 使用模型: gemini-2.5-flash, 超时: 60秒
2025-10-28 08:16:31,832 - app.services.review.book_review_service - INFO - [BookReviewService] 开始评审作品: 测试作品 (20章), 章节数=20
2025-10-28 08:16:31,832 - app.services.review.book_review_service - INFO - ⚠️ 缓存未命中: book_review:review_book:4f0a3011d61559d6
2025-10-28 08:16:31,832 - app.services.review.book_review_analyzer - INFO - [BookReviewAnalyzer] 开始分析作品: 测试作品 (20章), 章节数=20
2025-10-28 08:16:31,832 - app.services.review.book_review_analyzer - INFO - [BookReviewAnalyzer] 并发执行4个维度分析...
2025-10-28 08:16:31,832 - app.services.review.book_review_analyzer - INFO - [BookReviewAnalyzer] 开始情节结构分析
2025-10-28 08:16:31,832 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=2000, temp=0.7, 尝试=1/3
2025-10-28 08:16:31,832 - app.services.review.book_review_analyzer - INFO - [BookReviewAnalyzer] 开始人物分析
2025-10-28 08:16:31,832 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=2000, temp=0.7, 尝试=1/3
2025-10-28 08:16:31,832 - app.services.review.book_review_analyzer - INFO - [BookReviewAnalyzer] 开始世界观分析
2025-10-28 08:16:31,832 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=1500, temp=0.7, 尝试=1/3
2025-10-28 08:16:31,832 - app.services.review.book_review_analyzer - INFO - [BookReviewAnalyzer] 开始文风分析
2025-10-28 08:16:31,837 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=1500, temp=0.7, 尝试=1/3
2025-10-28 08:16:45,213 - httpx - INFO - HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
2025-10-28 08:16:45,213 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=1602, 尝试次数=1
2025-10-28 08:16:45,213 - app.utils.json_parser - INFO - [BookReviewAnalyzer] 🔍 开始解析AI响应, 长度=1602
2025-10-28 08:16:45,213 - app.utils.json_parser - INFO - [BookReviewAnalyzer] 🔍 方法2: 从markdown代码块提取JSON, 长度=1590
2025-10-28 08:16:45,213 - app.utils.json_parser - INFO - [BookReviewAnalyzer] ✅ 方法2成功: markdown代码块解析
2025-10-28 08:16:52,321 - httpx - INFO - HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
2025-10-28 08:16:52,323 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=1035, 尝试次数=1
2025-10-28 08:16:52,323 - app.utils.json_parser - INFO - [BookReviewAnalyzer] 🔍 开始解析AI响应, 长度=1035
2025-10-28 08:16:52,324 - app.utils.json_parser - INFO - [BookReviewAnalyzer] ✅ 预处理: 已替换中文标点符号
2025-10-28 08:16:52,324 - app.utils.json_parser - INFO - [BookReviewAnalyzer] 🔍 方法2: 从markdown代码块提取JSON, 长度=1023
2025-10-28 08:16:52,324 - app.utils.json_parser - INFO - [BookReviewAnalyzer] ✅ 方法2成功: markdown代码块解析
2025-10-28 08:16:55,712 - httpx - INFO - HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
2025-10-28 08:16:55,720 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=1041, 尝试次数=1
2025-10-28 08:16:55,720 - app.utils.json_parser - INFO - [BookReviewAnalyzer] 🔍 开始解析AI响应, 长度=1041
2025-10-28 08:16:55,720 - app.utils.json_parser - INFO - [BookReviewAnalyzer] ✅ 预处理: 已替换中文标点符号
2025-10-28 08:16:55,720 - app.utils.json_parser - INFO - [BookReviewAnalyzer] 🔍 方法2: 从markdown代码块提取JSON, 长度=1029
2025-10-28 08:16:55,720 - app.utils.json_parser - INFO - [BookReviewAnalyzer] ✅ 方法2成功: markdown代码块解析
2025-10-28 08:16:59,597 - httpx - INFO - HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
2025-10-28 08:16:59,599 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=926, 尝试次数=1
2025-10-28 08:16:59,600 - app.utils.json_parser - INFO - [BookReviewAnalyzer] 🔍 开始解析AI响应, 长度=926
2025-10-28 08:16:59,600 - app.utils.json_parser - INFO - [BookReviewAnalyzer] ✅ 预处理: 已替换中文标点符号
2025-10-28 08:16:59,600 - app.utils.json_parser - INFO - [BookReviewAnalyzer] 🔍 方法2: 从markdown代码块提取JSON, 长度=914
2025-10-28 08:16:59,600 - app.utils.json_parser - INFO - [BookReviewAnalyzer] ✅ 方法2成功: markdown代码块解析
2025-10-28 08:16:59,602 - app.services.review.book_review_analyzer - INFO - [BookReviewAnalyzer] 4个维度分析完成,开始计算评分和建议
2025-10-28 08:16:59,602 - app.services.review.book_review_analyzer - INFO - [BookReviewAnalyzer] 生成综合建议
2025-10-28 08:16:59,602 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=1500, temp=0.8, 尝试=1/3
2025-10-28 08:17:21,199 - httpx - INFO - HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
2025-10-28 08:17:21,204 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=1905, 尝试次数=1
2025-10-28 08:17:21,204 - app.utils.json_parser - INFO - [BookReviewAnalyzer] 🔍 开始解析AI响应, 长度=1905
2025-10-28 08:17:21,205 - app.utils.json_parser - INFO - [BookReviewAnalyzer] 🔍 方法2: 从markdown代码块提取JSON, 长度=1893
2025-10-28 08:17:21,205 - app.utils.json_parser - INFO - [BookReviewAnalyzer] ✅ 方法2成功: markdown代码块解析
2025-10-28 08:17:21,205 - app.services.review.book_review_analyzer - INFO - [BookReviewAnalyzer] 分析完成, 总分=37.1
2025-10-28 08:17:21,205 - app.services.review.book_review_service - INFO - 💾 缓存已保存: book_review:review_book:4f0a3011d61559d6 (expire=7200s)
2025-10-28 08:17:21,205 - app.services.review.book_review_service - INFO - [BookReviewService] 评审完成, 总分=37.1
2025-10-28 08:17:21,205 - app.api.v1.review - INFO - [POST /review/books] 评审完成, novel_id=ddc0183e-76f5-4187-a491-9692a341996b, overall_score=37.1
INFO:     127.0.0.1:57460 - "POST /api/v1/review/books HTTP/1.1" 200 OK
2025-10-28 08:17:23,243 - app.api.v1.review - INFO - [POST /review/books] user_id=602f5147-846a-4cde-95d3-405fa75f133f, novel_id=ddc0183e-76f5-4187-a491-9692a341996b, chapters=20, quick_mode=False
2025-10-28 08:17:23,758 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-flash, Timeout: 60s
2025-10-28 08:17:23,758 - app.services.review.book_review_analyzer - INFO - [BookReviewAnalyzer] 初始化完成, 使用模型: gemini-2.5-flash, 超时: 60秒
2025-10-28 08:17:23,758 - app.services.review.book_review_service - INFO - [BookReviewService] 开始评审作品: 测试作品 (20章), 章节数=20
2025-10-28 08:17:23,760 - app.services.review.book_review_service - INFO - ✅ 缓存命中: book_review:review_book:4f0a3011d61559d6
2025-10-28 08:17:23,760 - app.api.v1.review - INFO - [POST /review/books] 评审完成, novel_id=ddc0183e-76f5-4187-a491-9692a341996b, overall_score=37.1
INFO:     127.0.0.1:55972 - "POST /api/v1/review/books HTTP/1.1" 200 OK
