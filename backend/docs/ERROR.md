(venv) PS D:\Java\ai_writer\backend> python -m uvicorn app.main:app --reload
INFO:     Will watch for changes in these directories: ['D:\\Java\\ai_writer\\backend']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [25232] using WatchFiles
D:\Java\ai_writer\backend\app\services\worldview_extraction_service.py:306: SyntaxWarning: invalid escape sequence '\s'
  conflict_match = re.search(f'{stage}[^：:]*[:：]\s*([^\n]{{20,200}})', conflict_section)
D:\Java\ai_writer\backend\app\services\worldview_extraction_service.py:574: SyntaxWarning: invalid escape sequence '\.'
  text = re.sub(r'[，。！？、；：""''《》（）【】\.,!?;:\'"()\[\]]+', '', text)
INFO:     Started server process [20008]
INFO:     Waiting for application startup.
2025-10-26 10:54:16,525 - apscheduler.scheduler - INFO - Adding job tentatively -- it will be properly scheduled when the scheduler starts
2025-10-26 10:54:16,529 - apscheduler.scheduler - INFO - Added job "清理过期的去痕迹会话详情" to job store "default"
2025-10-26 10:54:16,529 - apscheduler.scheduler - INFO - Scheduler started
2025-10-26 10:54:16,529 - app.tasks.cleanup_humanize_details - INFO - 定时任务调度器已启动
INFO:     Application startup complete.
INFO:     127.0.0.1:63232 - "POST /api/v1/auth/login HTTP/1.1" 200 OK
INFO:     127.0.0.1:63235 - "GET /health HTTP/1.1" 200 OK
2025-10-26 10:54:49,253 - app.services.user_profile_service - INFO - 创建新用户画像: user_id=602f5147-846a-4cde-95d3-405fa75f133f
INFO:     127.0.0.1:63238 - "GET /api/v1/humanize/profile HTTP/1.1" 200 OK
2025-10-26 10:54:49,766 - app.services.user_profile_service - INFO - 更新用户画像设置: user_id=602f5147-846a-4cde-95d3-405fa75f133f
INFO:     127.0.0.1:63241 - "PUT /api/v1/humanize/profile/settings HTTP/1.1" 200 OK
INFO:     127.0.0.1:63244 - "GET /api/v1/humanize/history?page=1&page_size=10 HTTP/1.1" 200 OK
INFO:     127.0.0.1:63247 - "GET /api/v1/humanize/stats HTTP/1.1" 200 OK
