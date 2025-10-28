(venv) PS D:\Java\ai_writer\backend> python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
INFO:     Will watch for changes in these directories: ['D:\\Java\\ai_writer\\backend']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [31856] using WatchFiles
已注册策略: web_novel_11d - 网文11维度分析
INFO:     Started server process [14148]
INFO:     Waiting for application startup.
2025-10-28 13:35:53,747 - app.main - INFO - 🚀 应用启动中...
2025-10-28 13:35:53,747 - app.core.database - INFO - 正在初始化数据库... (尝试 1/3)
2025-10-28 13:35:53,924 - app.core.database - INFO - ✅ 数据库初始化成功
2025-10-28 13:35:53,924 - apscheduler.scheduler - INFO - Adding job tentatively -- it will be properly scheduled when the scheduler starts
2025-10-28 13:35:53,927 - apscheduler.scheduler - INFO - Added job "清理过期的去痕迹会话详情" to job store "default"
2025-10-28 13:35:53,927 - apscheduler.scheduler - INFO - Scheduler started
2025-10-28 13:35:53,928 - app.tasks.cleanup_humanize_details - INFO - 定时任务调度器已启动
2025-10-28 13:35:53,928 - app.main - INFO - 🔄 开始预加载Embedding模型...
2025-10-28 13:35:53,928 - app.services.vector_store_service - INFO - 🔄 预加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
2025-10-28 13:35:53,929 - sentence_transformers.SentenceTransformer - INFO - Use pytorch device_name: cpu
2025-10-28 13:35:53,930 - sentence_transformers.SentenceTransformer - INFO - Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
2025-10-28 13:36:01,928 - app.services.vector_store_service - INFO - ✅ Embedding模型预加载成功，耗时: 8.00秒
2025-10-28 13:36:01,928 - app.main - INFO - ✅ Embedding模型预加载完成
2025-10-28 13:36:01,928 - app.main - INFO - ✅ 应用启动完成
INFO:     Application startup complete.
INFO:     127.0.0.1:61069 - "POST /api/v1/auth/login HTTP/1.1" 200 OK
2025-10-28 13:36:07,726 - app.api.v1.ai - INFO - [AI评价] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), 操作类型: continue, 文本长度: 164
2025-10-28 13:36:07,726 - app.services.ai.evaluation_service - INFO - 开始评价文本, user_id=602f5147-846a-4cde-95d3-405fa75f133f, operation_type=continue, text_length=164
2025-10-28 13:36:07,727 - app.services.ai.prompts - INFO - Prompts loaded successfully from D:\Java\ai_writer\backend\app\services\ai\prompts\default.json
2025-10-28 13:36:08,394 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-flash, Timeout: 120s
2025-10-28 13:36:08,395 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.3
2025-10-28 13:36:12,131 - httpx - INFO - HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
2025-10-28 13:36:12,132 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-10-28 13:36:23,066 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 6 个数据块，总长度: 615
2025-10-28 13:36:23,067 - app.services.ai.evaluation_service - ERROR - JSON解析失败: Expecting value: line 1 column 1 (char 0), 原文: ```json
{
  "overall_score": 83,
  "dimensions": {
    "literary_quality": 85,
    "coherence": 90,
    "creativity": 70,
    "emotional_impact": 80,
    "pacing": 90
  },
  "highlights": [
    "意境优美,通过多感官描写营造了静谧而富有诗意的夏夜氛围。",
    "情感表达细腻,成功刻画了人物面对景物时油然而生的感慨与怀旧情愫。",
    "语言流畅自然,修辞手法运用得当,如“月光如水”、“宛如一幅水墨画”等。"
  ],
  "issues": [
    "部分意象和表达略显陈旧,如“月光如水”、“沁人心脾”、“时光荏苒,物是人非”等,缺乏新颖的视角。",
    "人物情感的“无限感慨”略显宽泛,若能稍加暗示具体的回忆或情感来源,感染力会更强。"
  ],
  "suggestions": [
    "尝试在描写中融入更具个人风格或独特视角的意象,避免使用过于常见的比喻和短语。",

2025-10-28 13:36:23,086 - app.services.ai.ai_log_middleware - INFO - AI调用日志已记录: operation=evaluate, tokens=811, cost=$0.001078, duration=14672ms, success=True
2025-10-28 13:36:23,095 - app.services.ai.evaluation_service - INFO - 评价记录已保存: d5ae4be8-9723-40ef-b21d-abcd51fa8e0d
2025-10-28 13:36:23,095 - app.services.ai.evaluation_service - INFO - 评价完成, evaluation_id=d5ae4be8-9723-40ef-b21d-abcd51fa8e0d, overall_score=83.0
2025-10-28 13:36:23,099 - app.api.v1.ai - INFO - [AI评价] 用户 testuser_new-1 评价完成, 总分: 83.0, 评价ID: d5ae4be8-9723-40ef-b21d-abcd51fa8e0d
INFO:     127.0.0.1:54746 - "POST /api/v1/ai/evaluate HTTP/1.1" 200 OK
INFO:     127.0.0.1:55597 - "GET /api/v1/ai-logs/me?skip=0&limit=1 HTTP/1.1" 200 OK