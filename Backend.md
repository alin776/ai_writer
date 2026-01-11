(venv) PS D:\Java\ai_writer\backend> python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000 --log-level info
INFO:     Will watch for changes in these directories: ['D:\\Java\\ai_writer\\backend']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [36104] using WatchFiles
已注册策略: web_novel_11d - 网文11维度分析
2026-01-12 03:18:49,732 - app.main - INFO - [STARTUP] 监控中间件已注册: TraceMiddleware, MonitoringMiddleware
INFO:     Started server process [35596]
INFO:     Waiting for application startup.
2026-01-12 03:18:49,992 - app.main - INFO - [STARTUP] 应用启动中...
2026-01-12 03:18:49,992 - app.core.database - INFO - 正在初始化数据库... (尝试 1/3)
2026-01-12 03:18:50,144 - app.core.database - INFO - ✅ 数据库初始化成功
2026-01-12 03:18:50,144 - app.main - INFO - [STARTUP] 开始检查并初始化官方频道...
检查官方频道...
现有官方频道: {'公共酒馆', '官方实验室', '作者酒馆', '读者茶馆'}

✓ 所有官方频道都已存在，无需创建

现有官方频道列表:
  - 作者酒馆 (ID: c4a5fcd7-7fd1-4a18-8677-a15c052c7507)
  - 读者茶馆 (ID: 2e1b9d33-1400-4a40-802b-6d212d7a2fe5)
  - 公共酒馆 (ID: 3749ebb4-a2d6-4ab8-aa14-cf6c26611fc0)
  - 官方实验室 (ID: 452cfe84-3ac4-49e1-986b-260bcc3b8a6a)
2026-01-12 03:18:50,153 - app.main - INFO - [STARTUP] ✅ 官方频道检查完成
2026-01-12 03:18:50,153 - apscheduler.scheduler - INFO - Adding job tentatively -- it will be properly scheduled when the scheduler starts
2026-01-12 03:18:50,153 - apscheduler.scheduler - INFO - Adding job tentatively -- it will be properly scheduled when the scheduler starts
2026-01-12 03:18:50,153 - apscheduler.scheduler - INFO - Added job "清理过期的去痕迹会话详情" to job store "default"
2026-01-12 03:18:50,153 - apscheduler.scheduler - INFO - Added job "清理过期的 Agent 会话" to job store "default"
2026-01-12 03:18:50,153 - apscheduler.scheduler - INFO - Scheduler started
2026-01-12 03:18:50,153 - app.tasks.cleanup_humanize_details - INFO - 定时任务调度器已启动
2026-01-12 03:18:50,153 - apscheduler.scheduler - INFO - Adding job tentatively -- it will be properly scheduled when the scheduler starts
2026-01-12 03:18:50,163 - app.services.channel_scheduler - INFO - Channel scheduler initialized
2026-01-12 03:18:50,163 - apscheduler.scheduler - INFO - Added job "检查作品频道活跃度" to job store "default"
2026-01-12 03:18:50,163 - apscheduler.scheduler - INFO - Scheduler started
2026-01-12 03:18:50,163 - app.services.channel_scheduler - INFO - Channel scheduler started
2026-01-12 03:18:50,163 - app.main - INFO - [STARTUP] 开始预初始化同步Redis连接...
2026-01-12 03:18:50,163 - app.api.v1.agent - INFO - [Redis] 全局连接池已创建
2026-01-12 03:18:52,233 - app.main - INFO - [STARTUP] ✅ 同步Redis连接池预初始化完成
2026-01-12 03:18:52,233 - app.main - INFO - [STARTUP] 开始初始化AsyncRedisSaver索引...
2026-01-12 03:18:54,265 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ setup_checkpointer Redis连接验证成功
2026-01-12 03:18:56,319 - redisvl.index.index - INFO - Index already exists, not overwriting.
2026-01-12 03:18:56,319 - redisvl.index.index - INFO - Index already exists, not overwriting.
2026-01-12 03:18:56,319 - redisvl.index.index - INFO - Index already exists, not overwriting.
2026-01-12 03:18:56,319 - langgraph.checkpoint.redis.aio - INFO - Redis client is a standalone client
2026-01-12 03:18:56,325 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ AsyncRedisSaver索引预创建成功
2026-01-12 03:18:56,325 - app.main - INFO - [STARTUP] AsyncRedisSaver索引初始化完成
2026-01-12 03:18:56,326 - app.main - INFO - [STARTUP] 开始预加载Embedding模型...
2026-01-12 03:18:56,326 - app.services.vector_store_service - INFO - 🔄 预加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
2026-01-12 03:19:02,788 - app.services.vector_store_service - INFO - ✅ Embedding模型预加载成功，耗时: 6.46秒
2026-01-12 03:19:02,788 - app.main - INFO - [STARTUP] Embedding模型预加载完成
2026-01-12 03:19:02,790 - app.main - INFO - [STARTUP] P0性能优化已暂时禁用（诊断模式）
2026-01-12 03:19:02,790 - app.main - INFO - [STARTUP] 应用启动完成
INFO:     Application startup complete.