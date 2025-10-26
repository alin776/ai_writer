(venv) PS D:\Java\ai_writer\backend> python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
INFO:     Will watch for changes in these directories: ['D:\\Java\\ai_writer\\backend']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [28028] using WatchFiles
INFO:     Started server process [28580]
INFO:     Waiting for application startup.
2025-10-26 17:21:12,484 - apscheduler.scheduler - INFO - Adding job tentatively -- it will be properly scheduled when the scheduler starts
2025-10-26 17:21:12,488 - apscheduler.scheduler - INFO - Added job "清理过期的去痕迹会话详情" to job store "default"
2025-10-26 17:21:12,488 - apscheduler.scheduler - INFO - Scheduler started
2025-10-26 17:21:12,488 - app.tasks.cleanup_humanize_details - INFO - 定时任务调度器已启动
INFO:     Application startup complete.
INFO:     127.0.0.1:51895 - "POST /api/v1/auth/login HTTP/1.1" 200 OK
INFO:     127.0.0.1:51900 - "GET /api/v1/works?skip=0&limit=10 HTTP/1.1" 200 OK
2025-10-26 17:21:15,447 - app.api.v1.chapters - INFO - [GET chapters] work_id=1a14bf0c-8c1c-42b9-9d9e-6107cd84c75f, user_id=602f5147-846a-4cde-95d3-405fa75f133f
2025-10-26 17:21:15,463 - app.services.chapter_service - INFO - [ChapterService] Querying chapters for work_id=1a14bf0c-8c1c-42b9-9d9e-6107cd84c75f, type=<class 'uuid.UUID'>
2025-10-26 17:21:15,463 - app.services.chapter_service - INFO - [ChapterService] Found 2 chapters
2025-10-26 17:21:15,463 - app.services.chapter_service - INFO -   - Chapter: 武松开飞机打老鼠, order=1
2025-10-26 17:21:15,463 - app.services.chapter_service - INFO -   - Chapter: 你好, order=2
2025-10-26 17:21:15,463 - app.api.v1.chapters - INFO - [GET chapters] Returning 2 chapters
INFO:     127.0.0.1:51903 - "GET /api/v1/chapters/work/1a14bf0c-8c1c-42b9-9d9e-6107cd84c75f HTTP/1.1" 200 OK
2025-10-26 17:21:16,514 - app.api.v1.review - INFO - [POST /review/chapters/a29b721e-4657-49f4-bcf0-f0367f32a56e] user_id=602f5147-846a-4cde-95d3-405fa75f133f, review_type=ReviewTypeEnum.STANDARD
2025-10-26 17:21:16,514 - app.services.ai.prompts - INFO - Prompts loaded successfully from D:\Java\ai_writer\backend\app\services\ai\prompts\default.json
2025-10-26 17:21:17,396 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro
2025-10-26 17:21:17,400 - app.services.review.novel_review_service - INFO - [NovelReviewService] 开始评审章节: chapter_id=a29b721e-4657-49f4-bcf0-f0367f32a56e, user_id=602f5147-846a-4cde-95d3-405fa75f133f, review_type=ReviewTypeEnum.STANDARD
2025-10-26 17:21:17,409 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=3000, temp=0.7
2025-10-26 17:21:20,671 - httpx - INFO - HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
2025-10-26 17:21:20,672 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-10-26 17:21:50,751 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 15 个数据块，总长度: 1784
2025-10-26 17:21:50,752 - app.services.review.novel_review_service - INFO - [NovelReviewService] AI 响应长度: 1784 字符
2025-10-26 17:21:50,752 - app.services.review.novel_review_service - INFO - [NovelReviewService] JSON 解析成功,总分: 0.0
2025-10-26 17:21:50,792 - app.services.review.novel_review_service - INFO - [NovelReviewService] 章节评审完成: session_id=29a4ace2-5bb7-4ce6-afe8-18aec9e7ff28, overall_score=0.0
2025-10-26 17:21:51,899 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro
2025-10-26 17:21:51,904 - app.services.review.task_generator_service - INFO - [TaskGeneratorService] 开始生成任务: session_id=29a4ace2-5bb7-4ce6-afe8-18aec9e7ff28, overall_score=0.0
2025-10-26 17:21:51,909 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=3000, temp=0.7
2025-10-26 17:21:55,052 - httpx - INFO - HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
2025-10-26 17:21:55,052 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-10-26 17:22:27,887 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 66 个数据块，总长度: 3818
2025-10-26 17:22:27,888 - app.services.review.task_generator_service - INFO - [TaskGeneratorService] AI 响应长度: 3818 字符
2025-10-26 17:22:27,888 - app.services.review.task_generator_service - INFO - [TaskGeneratorService] 成功生成 7 个任务
2025-10-26 17:22:27,935 - app.services.review.task_generator_service - INFO - [TaskGeneratorService] 任务生成完成: 共生成 7 个任务
2025-10-26 17:22:27,966 - app.services.review.version_manager_service - INFO - [VersionManagerService] 版本创建成功: version_id=3f3d5860-271c-4ebc-af1e-a34ad748528f, version_number=8, is_milestone=False
2025-10-26 17:22:27,966 - app.api.v1.review - INFO - [POST /review/chapters/a29b721e-4657-49f4-bcf0-f0367f32a56e] 评审完成: session_id=29a4ace2-5bb7-4ce6-afe8-18aec9e7ff28, tasks=7, version=3f3d5860-271c-4ebc-af1e-a34ad748528f
INFO:     127.0.0.1:49616 - "POST /api/v1/review/chapters/a29b721e-4657-49f4-bcf0-f0367f32a56e/review HTTP/1.1" 200 OK
2025-10-26 17:22:30,098 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro
INFO:     127.0.0.1:50890 - "GET /api/v1/review/chapters/a29b721e-4657-49f4-bcf0-f0367f32a56e/tasks HTTP/1.1" 200 OK
2025-10-26 17:22:31,101 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro
2025-10-26 17:22:31,110 - app.services.review.task_generator_service - INFO - [TaskGeneratorService] 手动创建任务: task_id=5212a994-0100-41a7-adb4-ac4719a07bb1
2025-10-26 17:22:31,110 - app.api.v1.review - INFO - [POST /tasks] 手动创建任务: task_id=5212a994-0100-41a7-adb4-ac4719a07bb1
INFO:     127.0.0.1:53414 - "POST /api/v1/review/tasks HTTP/1.1" 201 Created
2025-10-26 17:22:32,389 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro
2025-10-26 17:22:32,400 - app.services.review.task_generator_service - INFO - [TaskGeneratorService] 任务状态更新: task_id=0a966109-9ef5-40dc-b3f4-922da8b70588, status=TaskStatusEnum.IN_PROGRESS
INFO:     127.0.0.1:53417 - "PATCH /api/v1/review/tasks/0a966109-9ef5-40dc-b3f4-922da8b70588/status HTTP/1.1" 200 OK
2025-10-26 17:22:33,629 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro
INFO:     127.0.0.1:50736 - "GET /api/v1/review/tasks/stats?chapter_id=a29b721e-4657-49f4-bcf0-f0367f32a56e HTTP/1.1" 200 OK
2025-10-26 17:22:34,687 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro
2025-10-26 17:22:34,699 - app.services.review.task_generator_service - INFO - [TaskGeneratorService] 任务状态更新: task_id=0a966109-9ef5-40dc-b3f4-922da8b70588, status=TaskStatusEnum.COMPLETED
2025-10-26 17:22:34,715 - app.services.review.task_generator_service - INFO - [TaskGeneratorService] 任务状态更新: task_id=9b43eda4-be97-4b8f-8bb4-39dfb952662c, status=TaskStatusEnum.COMPLETED
2025-10-26 17:22:34,715 - app.services.review.task_generator_service - INFO - [TaskGeneratorService] 批量操作完成: action=complete, success=2, failed=0
2025-10-26 17:22:34,715 - app.api.v1.review - INFO - [POST /tasks/batch-operations] action=complete, success=2, failed=0
INFO:     127.0.0.1:51815 - "POST /api/v1/review/tasks/batch-operations HTTP/1.1" 200 OK
2025-10-26 17:22:35,776 - app.services.review.version_manager_service - INFO - [VersionManagerService] 版本创建成功: version_id=cbf7d82f-44a3-4683-a0f1-b2457fb731ed, version_number=9, is_milestone=False
2025-10-26 17:22:35,776 - app.api.v1.review - INFO - [POST /chapters/a29b721e-4657-49f4-bcf0-f0367f32a56e/versions] 版本创建成功: version_id=cbf7d82f-44a3-4683-a0f1-b2457fb731ed, version_number=9
INFO:     127.0.0.1:54109 - "POST /api/v1/review/chapters/a29b721e-4657-49f4-bcf0-f0367f32a56e/versions HTTP/1.1" 201 Created
INFO:     127.0.0.1:54112 - "GET /api/v1/review/chapters/a29b721e-4657-49f4-bcf0-f0367f32a56e/versions HTTP/1.1" 200 OK
2025-10-26 17:22:35,839 - app.services.review.version_manager_service - INFO - [VersionManagerService] 里程碑状态更新: version_id=3f3d5860-271c-4ebc-af1e-a34ad748528f, is_milestone=True
INFO:     127.0.0.1:54115 - "PATCH /api/v1/review/versions/3f3d5860-271c-4ebc-af1e-a34ad748528f/milestone HTTP/1.1" 200 OK
