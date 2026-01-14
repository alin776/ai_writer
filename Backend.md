INFO:     Started server process [56980]
INFO:     Waiting for application startup.
2026-01-14 16:37:18,574 - app.main - INFO - [STARTUP] 应用启动中...
2026-01-14 16:37:18,575 - app.core.database - INFO - 正在初始化数据库... (尝试 1/3)
2026-01-14 16:37:18,758 - app.core.database - INFO - ✅ 数据库初始化成功
2026-01-14 16:37:18,762 - app.main - INFO - [STARTUP] 开始检查并初始化官方频道...
检查官方频道...
现有官方频道: {'官方实验室', '公共酒馆', '读者茶馆', '作者酒馆'}

✓ 所有官方频道都已存在，无需创建

现有官方频道列表:
  - 作者酒馆 (ID: c4a5fcd7-7fd1-4a18-8677-a15c052c7507)
  - 读者茶馆 (ID: 2e1b9d33-1400-4a40-802b-6d212d7a2fe5)
  - 公共酒馆 (ID: 3749ebb4-a2d6-4ab8-aa14-cf6c26611fc0)
  - 官方实验室 (ID: 452cfe84-3ac4-49e1-986b-260bcc3b8a6a)
2026-01-14 16:37:18,780 - app.main - INFO - [STARTUP] ✅ 官方频道检查完成
2026-01-14 16:37:18,781 - apscheduler.scheduler - INFO - Adding job tentatively -- it will be properly scheduled when the scheduler starts
2026-01-14 16:37:18,782 - apscheduler.scheduler - INFO - Adding job tentatively -- it will be properly scheduled when the scheduler starts
2026-01-14 16:37:18,790 - apscheduler.scheduler - INFO - Added job "清理过期的去痕迹会话详情" to job store "default"
2026-01-14 16:37:18,790 - apscheduler.scheduler - INFO - Added job "清理过期的 Agent 会话" to job store "default"
2026-01-14 16:37:18,790 - apscheduler.scheduler - INFO - Scheduler started
2026-01-14 16:37:18,792 - app.tasks.cleanup_humanize_details - INFO - 定时任务调度器已启动
2026-01-14 16:37:18,794 - apscheduler.scheduler - INFO - Adding job tentatively -- it will be properly scheduled when the scheduler starts
2026-01-14 16:37:18,795 - app.services.channel_scheduler - INFO - Channel scheduler initialized
2026-01-14 16:37:18,796 - apscheduler.scheduler - INFO - Added job "检查作品频道活跃度" to job store "default"
2026-01-14 16:37:18,798 - apscheduler.scheduler - INFO - Scheduler started
2026-01-14 16:37:18,800 - app.services.channel_scheduler - INFO - Channel scheduler started
2026-01-14 16:37:18,801 - app.main - INFO - [STARTUP] 开始预初始化同步Redis连接...
2026-01-14 16:37:18,803 - app.api.v1.agent - INFO - [Redis] 全局连接池已创建
2026-01-14 16:37:20,861 - app.main - INFO - [STARTUP] ✅ 同步Redis连接池预初始化完成
2026-01-14 16:37:20,861 - app.main - INFO - [STARTUP] 开始初始化AsyncRedisSaver索引...
2026-01-14 16:37:22,903 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ setup_checkpointer Redis连接验证成功
2026-01-14 16:37:24,946 - redisvl.index.index - INFO - Index already exists, not overwriting.
2026-01-14 16:37:24,950 - redisvl.index.index - INFO - Index already exists, not overwriting.
2026-01-14 16:37:24,953 - redisvl.index.index - INFO - Index already exists, not overwriting.
2026-01-14 16:37:24,954 - langgraph.checkpoint.redis.aio - INFO - Redis client is a standalone client
2026-01-14 16:37:24,955 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ AsyncRedisSaver索引预创建成功
2026-01-14 16:37:24,955 - app.main - INFO - [STARTUP] AsyncRedisSaver索引初始化完成
2026-01-14 16:37:24,956 - app.main - INFO - [STARTUP] 开始预加载Embedding模型...
2026-01-14 16:37:24,956 - app.services.vector_store_service - INFO - 🔄 预加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
2026-01-14 16:37:36,049 - app.services.vector_store_service - INFO - ✅ Embedding模型预加载成功，耗时: 11.09秒
2026-01-14 16:37:36,049 - app.main - INFO - [STARTUP] Embedding模型预加载完成
2026-01-14 16:37:36,049 - app.main - INFO - [STARTUP] P0性能优化已暂时禁用（诊断模式）
2026-01-14 16:37:36,055 - app.main - INFO - [STARTUP] 应用启动完成
INFO:     Application startup complete.
INFO:     ('127.0.0.1', 52619) - "WebSocket /api/v1/ws/notifications/79913e7e-d5cd-4e09-bce6-ca6639bd8456" [accepted]
2026-01-14 16:37:36,118 - app.api.v1.ws - INFO - [WebSocket] 通知连接建立: user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
INFO:     ('127.0.0.1', 58477) - "WebSocket /api/v1/ws/notifications/79913e7e-d5cd-4e09-bce6-ca6639bd8456" [accepted]
2026-01-14 16:37:36,128 - app.api.v1.ws - INFO - [WebSocket] 通知连接建立: user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
INFO:     ('127.0.0.1', 52622) - "WebSocket /api/v1/ws/notifications/79913e7e-d5cd-4e09-bce6-ca6639bd8456" [accepted]
2026-01-14 16:37:36,146 - app.api.v1.ws - INFO - [WebSocket] 通知连接建立: user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
INFO:     ('127.0.0.1', 59069) - "WebSocket /api/v1/ws/notifications/79913e7e-d5cd-4e09-bce6-ca6639bd8456" [accepted]
2026-01-14 16:37:36,163 - app.api.v1.ws - INFO - [WebSocket] 通知连接建立: user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
INFO:     connection open
INFO:     connection open
INFO:     connection open
INFO:     connection open
2026-01-14 16:37:43,065 - monitoring - INFO - Registered health check: cpu_usage
2026-01-14 16:37:43,069 - monitoring - INFO - Registered health check: memory_usage
2026-01-14 16:37:43,075 - monitoring - INFO - Registered health check: disk_usage
2026-01-14 16:37:43,079 - monitoring - INFO - Registered health check: process_status
2026-01-14 16:37:43,087 - monitoring - INFO - Added alert rule: high_cpu_usage
2026-01-14 16:37:43,096 - monitoring - INFO - Added alert rule: high_memory_usage
2026-01-14 16:37:43,107 - monitoring - INFO - Added alert rule: low_disk_space
2026-01-14 16:37:43,227 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:59245 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
2026-01-14 16:37:43,291 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works
INFO:     127.0.0.1:59244 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
2026-01-14 16:37:43,354 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:62225 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
2026-01-14 16:37:43,418 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works
INFO:     127.0.0.1:53501 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
2026-01-14 16:37:49,782 - app.api.v1.import_routes - INFO - 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456 预览导入文件: 一夕千悟，从杂役弟子开始.txt, 格式: txt
2026-01-14 16:37:49,796 - app.api.v1.import_routes - INFO - 预览成功: 作品=一夕千悟，从杂役弟子开始, 章节数=5
2026-01-14 16:37:49,808 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/works/import/preview
INFO:     127.0.0.1:58209 - "POST /api/v1/works/import/preview HTTP/1.1" 200 OK
2026-01-14 16:37:52,621 - app.api.v1.import_routes - INFO - 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456 导入文件: 一夕千悟，从杂役弟子开始.txt, 格式: txt
2026-01-14 16:37:52,624 - app.api.v1.import_routes - INFO - [导入参数] auto_extract_worldview=True, format=txt, background_tasks=True
2026-01-14 16:37:52,628 - app.services.import_service - INFO - 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456 开始导入文本数据
2026-01-14 16:37:52,840 - app.services.chapter_word_stat_service - INFO - 记录字数增量: chapter_id=494a31c1-e52b-4dc7-a1d1-b53c93b9f21e, delta=3005, edit_event_id=None
2026-01-14 16:37:52,849 - app.services.chapter_word_stat_service - INFO - 记录字数增量: chapter_id=f145fb07-88fd-4fc6-a942-f9526bb5399e, delta=2674, edit_event_id=None
2026-01-14 16:37:52,862 - app.services.chapter_word_stat_service - INFO - 记录字数增量: chapter_id=ba77b261-f2dd-4466-95ba-852fbceeef19, delta=2565, edit_event_id=None
2026-01-14 16:37:52,872 - app.services.chapter_word_stat_service - INFO - 记录字数增量: chapter_id=0a8fada7-1e6d-416d-909d-5633d7320375, delta=2481, edit_event_id=None
2026-01-14 16:37:52,889 - app.services.chapter_word_stat_service - INFO - 记录字数增量: chapter_id=37e6b76b-232a-41ec-8d99-a501dffe4186, delta=2951, edit_event_id=None
2026-01-14 16:37:52,961 - app.services.import_service - INFO - 文本导入完成: 作品ID=53539551-c108-468e-b5aa-d0e20a00e989, 章节=5
2026-01-14 16:37:52,970 - app.api.v1.import_routes - INFO - [世界观提取] 已为作品 53539551-c108-468e-b5aa-d0e20a00e989 排队世界观提取任务
2026-01-14 16:37:52,984 - app.api.v1.import_routes - INFO - 导入成功: 作品ID=53539551-c108-468e-b5aa-d0e20a00e989, 章节=5, 人物=0
2026-01-14 16:37:53,000 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/works/import
INFO:     127.0.0.1:63930 - "POST /api/v1/works/import HTTP/1.1" 200 OK
2026-01-14 16:37:53,075 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-14 16:37:58,645 - app.api.v1.chapters - INFO - [GET chapters] work_id=53539551-c108-468e-b5aa-d0e20a00e989, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-14 16:37:58,694 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:settings:53539551-c108-468e-b5aa-d0e20a00e989 (expire=300s)
2026-01-14 16:37:58,709 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/53539551-c108-468e-b5aa-d0e20a00e989/settings
2026-01-14 16:37:58,719 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:guidelines:53539551-c108-468e-b5aa-d0e20a00e989 (expire=300s)
2026-01-14 16:37:58,722 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:locations:53539551-c108-468e-b5aa-d0e20a00e989 (expire=300s)
INFO:     127.0.0.1:55739 - "GET /api/v1/worldview/works/53539551-c108-468e-b5aa-d0e20a00e989/settings HTTP/1.1" 200 OK
2026-01-14 16:37:58,730 - app.api.v1.chapters - INFO - ⚠️ [GET chapters] 缓存未命中: chapters:work:53539551-c108-468e-b5aa-d0e20a00e989
2026-01-14 16:37:58,731 - app.services.chapter_service - INFO - [ChapterService] Querying chapters for work_id=53539551-c108-468e-b5aa-d0e20a00e989, type=<class 'uuid.UUID'>
2026-01-14 16:37:58,742 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/53539551-c108-468e-b5aa-d0e20a00e989/guidelines
2026-01-14 16:37:58,744 - app.services.chapter_service - INFO - [ChapterService] Found 5 chapters
2026-01-14 16:37:58,745 - app.services.chapter_service - INFO -   - Chapter: 第1章 吞噬, order=1
2026-01-14 16:37:58,745 - app.services.chapter_service - INFO -   - ... (3 more chapters)
2026-01-14 16:37:58,745 - app.services.chapter_service - INFO -   - Chapter: 第5章 太一门, order=5
2026-01-14 16:37:58,746 - app.api.v1.chapters - INFO - [GET chapters] Returning 5 chapters
2026-01-14 16:37:58,751 - app.api.v1.chapters - INFO - 💾 [GET chapters] 缓存已保存: chapters:work:53539551-c108-468e-b5aa-d0e20a00e989 (expire=60s)
2026-01-14 16:37:58,753 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/53539551-c108-468e-b5aa-d0e20a00e989/locations
2026-01-14 16:37:58,755 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works/53539551-c108-468e-b5aa-d0e20a00e989
2026-01-14 16:37:58,756 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
2026-01-14 16:37:58,759 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:characters:53539551-c108-468e-b5aa-d0e20a00e989 (expire=300s)
INFO:     127.0.0.1:55740 - "GET /api/v1/worldview/works/53539551-c108-468e-b5aa-d0e20a00e989/guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:55738 - "GET /api/v1/worldview/works/53539551-c108-468e-b5aa-d0e20a00e989/locations HTTP/1.1" 200 OK
2026-01-14 16:37:58,765 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第2章 浑圆桩 (order=2)
INFO:     127.0.0.1:55730 - "GET /api/v1/works/53539551-c108-468e-b5aa-d0e20a00e989 HTTP/1.1" 200 OK
2026-01-14 16:37:58,771 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/work/53539551-c108-468e-b5aa-d0e20a00e989
2026-01-14 16:37:58,783 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/53539551-c108-468e-b5aa-d0e20a00e989/characters
INFO:     127.0.0.1:55736 - "GET /api/v1/chapters/work/53539551-c108-468e-b5aa-d0e20a00e989 HTTP/1.1" 200 OK
INFO:     127.0.0.1:55737 - "GET /api/v1/worldview/works/53539551-c108-468e-b5aa-d0e20a00e989/characters HTTP/1.1" 200 OK
2026-01-14 16:38:00,262 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:ai-guidelines:53539551-c108-468e-b5aa-d0e20a00e989 (expire=300s)
2026-01-14 16:38:00,264 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/53539551-c108-468e-b5aa-d0e20a00e989/ai-guidelines
INFO:     127.0.0.1:60907 - "GET /api/v1/worldview/works/53539551-c108-468e-b5aa-d0e20a00e989/ai-guidelines HTTP/1.1" 200 OK
2026-01-14 16:38:00,272 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第2章 浑圆桩 (65 paragraphs)
2026-01-14 16:38:00,274 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第3章 一夕千悟 (order=3)
2026-01-14 16:38:02,016 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第3章 一夕千悟 (64 paragraphs)
2026-01-14 16:38:02,017 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第4章 家底 (order=4)
2026-01-14 16:38:03,390 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第4章 家底 (60 paragraphs)
2026-01-14 16:38:03,398 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2026-01-14 16:38:06,799 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (70 paragraphs)
2026-01-14 16:38:06,826 - app.api.v1.import_routes - INFO - [世界观提取] 开始为作品 53539551-c108-468e-b5aa-d0e20a00e989 提取世界观
2026-01-14 16:38:06,852 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 53539551-c108-468e-b5aa-d0e20a00e989, chapter_id: 494a31c1-e52b-4dc7-a1d1-b53c93b9f21e
2026-01-14 16:38:06,857 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 53539551-c108-468e-b5aa-d0e20a00e989, chapter_id: 494a31c1-e52b-4dc7-a1d1-b53c93b9f21e
2026-01-14 16:38:06,934 - app.services.worldview_sync_service - INFO - [世界观同步] 章节 1 '第1章 吞噬': 内容长度=3005
2026-01-14 16:38:06,936 - app.services.worldview_sync_service - INFO - [世界观同步] 章节 2 '第2章 浑圆桩': 内容长度=2674
2026-01-14 16:38:06,938 - app.services.worldview_sync_service - INFO - [世界观同步] 章节 3 '第3章 一夕千悟': 内容长度=2565
2026-01-14 16:38:06,939 - app.services.worldview_sync_service - INFO - [世界观同步] 章节 4 '第4章 家底': 内容长度=2481
2026-01-14 16:38:06,942 - app.services.worldview_sync_service - INFO - [世界观同步] 章节 5 '第5章 太一门': 内容长度=2951
2026-01-14 16:38:06,950 - app.services.worldview_sync_service - INFO - [世界观同步] 合并 5 个章节，总内容长度: 13755
2026-01-14 16:38:06,956 - app.services.worldview_sync_service - INFO - [世界观同步] 内容预览:

【第1章 第1章 吞噬】
<p>青州。</p><p>渊阳府，贤古县。</p><p>源顺镖局，后院偏房的一片空地内。</p><p>此处是镖局内，堆放柴炭的地方，平常少有人至，但此时，却有十多个单薄的身影，在空地上，稀稀落落地站着。</p><p>这些人都是十五六岁的少年，身体大多都还没长开，脸上都泛着长期营养不良的菜色。</p><p>这些少年都是源顺镖局，今年新招的杂役弟子。</p><p>刚进源顺镖局的时候，他们还一个个都兴奋异常。</p><p>因为源顺镖局的杂役弟子，是有机会学些粗浅的拳脚武技的。</p><p>学得好的，有机会晋升为学徒。</p><p>一旦成为学徒，就能学到真正的武功，而且可以跟随镖师，出去走镖。</p><p>假以时日，业务熟练了，自己也能成为镖师。</p><p>镖师虽说是吃江湖饭的，有些危险，但对这些贫苦出身的少年们，这已经是相当好的职业了。</p><p>起码能吃饱肚子，而且多少是可以捞些油水的。</p><p>但现在，他们已经进门两个半月了。</p><p>心绪也从兴奋，慢慢变得黯淡了。</p><p>杂役弟子能成为学徒的，一批里，最多一二个，而且经常的，是成批成批的覆...
2026-01-14 16:38:06,972 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works
INFO:     127.0.0.1:61244 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
2026-01-14 16:38:07,157 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
2026-01-14 16:38:07,165 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
2026-01-14 16:38:07,181 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
2026-01-14 16:38:07,189 - app.services.worldview_sync_service - INFO - [世界观同步] 开始AI分析，章节数: 5, 内容长度: 13755
2026-01-14 16:38:07,197 - app.services.worldview_sync_service - INFO - [世界观同步] 现有世界观: （暂无世界观数据）...
2026-01-14 16:38:07,206 - app.services.worldview_sync_service - INFO - [世界观同步] db=<sqlalchemy.ext.asyncio.session.AsyncSession object at 0x00000170FE467CE0>, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-14 16:38:07,216 - app.services.ai.prompts - INFO - Prompts loaded successfully from D:\Java\ai_writer\backend\app\services\ai\prompts\default.json
2026-01-14 16:38:07,229 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-14 16:38:07,233 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-14 16:38:07,243 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2026-01-14 16:38:09,395 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-14 16:38:09,395 - app.services.worldview_sync_service - INFO - [世界观同步] AI服务初始化完成: api_key=***57d8, base_url=https://204992.xyz/v1, model=gemini-2.5-pro
INFO:     127.0.0.1:64850 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
INFO:     127.0.0.1:64851 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
INFO:     127.0.0.1:64847 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2026-01-14 16:38:09,417 - app.core.redis - INFO - ✅ Redis connected: redis://localhost:6379/0
2026-01-14 16:38:09,420 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 未传递task_type，使用默认模型: gemini-2.5-pro
2026-01-14 16:38:09,421 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=3000, temp=0.3, task_type=None
2026-01-14 16:38:09,450 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 494a31c1-e52b-4dc7-a1d1-b53c93b9f21e
2026-01-14 16:38:09,453 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
2026-01-14 16:38:09,482 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 494a31c1-e52b-4dc7-a1d1-b53c93b9f21e
2026-01-14 16:38:09,484 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
2026-01-14 16:38:09,506 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
2026-01-14 16:38:09,510 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/analysis/works/53539551-c108-468e-b5aa-d0e20a00e989/status
INFO:     127.0.0.1:57254 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-14 16:38:09,522 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:58915 - "GET /api/v1/analysis/works/53539551-c108-468e-b5aa-d0e20a00e989/status HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:61124 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-14 16:38:09,588 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/494a31c1-e52b-4dc7-a1d1-b53c93b9f21e/revisions
INFO:     127.0.0.1:61512 - "GET /api/v1/chapters/494a31c1-e52b-4dc7-a1d1-b53c93b9f21e/revisions?status=pending HTTP/1.1" 200 OK
2026-01-14 16:38:09,642 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:locations:53539551-c108-468e-b5aa-d0e20a00e989 (expire=300s)
2026-01-14 16:38:09,645 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:guidelines:53539551-c108-468e-b5aa-d0e20a00e989
2026-01-14 16:38:09,652 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:characters:53539551-c108-468e-b5aa-d0e20a00e989 (expire=300s)
2026-01-14 16:38:09,661 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/53539551-c108-468e-b5aa-d0e20a00e989/locations
2026-01-14 16:38:09,665 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/53539551-c108-468e-b5aa-d0e20a00e989/guidelines
2026-01-14 16:38:09,670 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/53539551-c108-468e-b5aa-d0e20a00e989/characters
INFO:     127.0.0.1:62665 - "GET /api/v1/worldview/works/53539551-c108-468e-b5aa-d0e20a00e989/locations HTTP/1.1" 200 OK
2026-01-14 16:38:09,677 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:settings:53539551-c108-468e-b5aa-d0e20a00e989 (expire=300s)
INFO:     127.0.0.1:63409 - "GET /api/v1/worldview/works/53539551-c108-468e-b5aa-d0e20a00e989/guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:61773 - "GET /api/v1/worldview/works/53539551-c108-468e-b5aa-d0e20a00e989/characters HTTP/1.1" 200 OK
2026-01-14 16:38:09,703 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:ai-guidelines:53539551-c108-468e-b5aa-d0e20a00e989
2026-01-14 16:38:09,705 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/53539551-c108-468e-b5aa-d0e20a00e989/settings
INFO:     127.0.0.1:63408 - "GET /api/v1/worldview/works/53539551-c108-468e-b5aa-d0e20a00e989/settings HTTP/1.1" 200 OK
2026-01-14 16:38:09,728 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/53539551-c108-468e-b5aa-d0e20a00e989/ai-guidelines
INFO:     127.0.0.1:53740 - "GET /api/v1/worldview/works/53539551-c108-468e-b5aa-d0e20a00e989/ai-guidelines HTTP/1.1" 200 OK
2026-01-14 16:38:09,764 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/494a31c1-e52b-4dc7-a1d1-b53c93b9f21e/revisions
INFO:     127.0.0.1:63722 - "GET /api/v1/chapters/494a31c1-e52b-4dc7-a1d1-b53c93b9f21e/revisions?status=pending HTTP/1.1" 200 OK
2026-01-14 16:38:09,785 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/analysis/works/53539551-c108-468e-b5aa-d0e20a00e989/status
2026-01-14 16:38:09,789 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:53539551-c108-468e-b5aa-d0e20a00e989
INFO:     127.0.0.1:63721 - "GET /api/v1/analysis/works/53539551-c108-468e-b5aa-d0e20a00e989/status HTTP/1.1" 404 Not Found
2026-01-14 16:38:09,793 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/494a31c1-e52b-4dc7-a1d1-b53c93b9f21e
INFO:     127.0.0.1:63167 - "PUT /api/v1/chapters/494a31c1-e52b-4dc7-a1d1-b53c93b9f21e HTTP/1.1" 200 OK
2026-01-14 16:38:09,800 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-14 16:38:14,075 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 53539551-c108-468e-b5aa-d0e20a00e989, chapter_id: 37e6b76b-232a-41ec-8d99-a501dffe4186
2026-01-14 16:38:14,080 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 53539551-c108-468e-b5aa-d0e20a00e989, chapter_id: 37e6b76b-232a-41ec-8d99-a501dffe4186
2026-01-14 16:38:14,135 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
2026-01-14 16:38:14,155 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 37e6b76b-232a-41ec-8d99-a501dffe4186
2026-01-14 16:38:14,189 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 37e6b76b-232a-41ec-8d99-a501dffe4186
2026-01-14 16:38:14,218 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: 0a8fada7-1e6d-416d-909d-5633d7320375
2026-01-14 16:38:14,223 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-14 16:38:14,234 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: 0a8fada7-1e6d-416d-909d-5633d7320375
2026-01-14 16:38:14,238 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-14 16:38:14,326 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
2026-01-14 16:38:14,329 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
2026-01-14 16:38:14,341 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:64639 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
INFO:     127.0.0.1:52590 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
INFO:     127.0.0.1:64641 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2026-01-14 16:38:14,525 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/37e6b76b-232a-41ec-8d99-a501dffe4186/revisions
INFO:     127.0.0.1:50620 - "GET /api/v1/chapters/37e6b76b-232a-41ec-8d99-a501dffe4186/revisions?status=pending HTTP/1.1" 200 OK
2026-01-14 16:38:14,594 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 494a31c1-e52b-4dc7-a1d1-b53c93b9f21e 内容更新，新段落数: 88
2026-01-14 16:38:14,616 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 494a31c1-e52b-4dc7-a1d1-b53c93b9f21e 内容更新，新段落数: 88
2026-01-14 16:38:14,632 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:53539551-c108-468e-b5aa-d0e20a00e989
2026-01-14 16:38:14,650 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/494a31c1-e52b-4dc7-a1d1-b53c93b9f21e
INFO:     127.0.0.1:51237 - "PUT /api/v1/chapters/494a31c1-e52b-4dc7-a1d1-b53c93b9f21e HTTP/1.1" 200 OK
2026-01-14 16:38:14,677 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
[TaskService] Checking daily writing task for user 79913e7e-d5cd-4e09-bce6-ca6639bd8456, word_count: 1672
[TaskService] Checking daily writing task for user 79913e7e-d5cd-4e09-bce6-ca6639bd8456, word_count: 1672
2026-01-14 16:38:17,799 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/37e6b76b-232a-41ec-8d99-a501dffe4186/revisions
2026-01-14 16:38:17,800 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
INFO:     127.0.0.1:60183 - "GET /api/v1/chapters/37e6b76b-232a-41ec-8d99-a501dffe4186/revisions?status=pending HTTP/1.1" 200 OK
[TaskService] Daily writing task result: None
2026-01-14 16:38:17,835 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:53539551-c108-468e-b5aa-d0e20a00e989
2026-01-14 16:38:17,857 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:characters:53539551-c108-468e-b5aa-d0e20a00e989 (expire=300s)
2026-01-14 16:38:17,858 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:53539551-c108-468e-b5aa-d0e20a00e989
[TaskService] Daily writing task result: None
2026-01-14 16:38:17,862 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:53539551-c108-468e-b5aa-d0e20a00e989
2026-01-14 16:38:17,869 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/494a31c1-e52b-4dc7-a1d1-b53c93b9f21e
2026-01-14 16:38:17,872 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/37e6b76b-232a-41ec-8d99-a501dffe4186
2026-01-14 16:38:17,876 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:locations:53539551-c108-468e-b5aa-d0e20a00e989 (expire=300s)
INFO:     127.0.0.1:51240 - "PUT /api/v1/chapters/494a31c1-e52b-4dc7-a1d1-b53c93b9f21e HTTP/1.1" 200 OK
2026-01-14 16:38:17,889 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-14 16:38:17,895 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/53539551-c108-468e-b5aa-d0e20a00e989/characters
2026-01-14 16:38:17,899 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/494a31c1-e52b-4dc7-a1d1-b53c93b9f21e
INFO:     127.0.0.1:50621 - "PUT /api/v1/chapters/37e6b76b-232a-41ec-8d99-a501dffe4186 HTTP/1.1" 200 OK
2026-01-14 16:38:17,903 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
INFO:     127.0.0.1:60174 - "GET /api/v1/worldview/works/53539551-c108-468e-b5aa-d0e20a00e989/characters HTTP/1.1" 200 OK
INFO:     127.0.0.1:51239 - "PUT /api/v1/chapters/494a31c1-e52b-4dc7-a1d1-b53c93b9f21e HTTP/1.1" 200 OK
2026-01-14 16:38:17,911 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-14 16:38:17,920 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/53539551-c108-468e-b5aa-d0e20a00e989/locations
INFO:     127.0.0.1:60175 - "GET /api/v1/worldview/works/53539551-c108-468e-b5aa-d0e20a00e989/locations HTTP/1.1" 200 OK
2026-01-14 16:38:22,522 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:settings:53539551-c108-468e-b5aa-d0e20a00e989 (expire=300s)
2026-01-14 16:38:22,537 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/53539551-c108-468e-b5aa-d0e20a00e989/settings
2026-01-14 16:38:24,706 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
INFO:     127.0.0.1:62715 - "GET /api/v1/worldview/works/53539551-c108-468e-b5aa-d0e20a00e989/settings HTTP/1.1" 200 OK
2026-01-14 16:38:24,718 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (70 paragraphs)
2026-01-14 16:38:24,724 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:guidelines:53539551-c108-468e-b5aa-d0e20a00e989
2026-01-14 16:38:24,737 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/53539551-c108-468e-b5aa-d0e20a00e989/guidelines
2026-01-14 16:38:24,742 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:ai-guidelines:53539551-c108-468e-b5aa-d0e20a00e989
INFO:     127.0.0.1:64595 - "GET /api/v1/worldview/works/53539551-c108-468e-b5aa-d0e20a00e989/guidelines HTTP/1.1" 200 OK
2026-01-14 16:38:24,766 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/53539551-c108-468e-b5aa-d0e20a00e989/ai-guidelines
INFO:     127.0.0.1:64597 - "GET /api/v1/worldview/works/53539551-c108-468e-b5aa-d0e20a00e989/ai-guidelines HTTP/1.1" 200 OK
2026-01-14 16:38:24,802 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
2026-01-14 16:38:24,852 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 37e6b76b-232a-41ec-8d99-a501dffe4186 内容更新，新段落数: 70
2026-01-14 16:38:24,863 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 37e6b76b-232a-41ec-8d99-a501dffe4186 内容更新，新段落数: 70
2026-01-14 16:38:24,873 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:53539551-c108-468e-b5aa-d0e20a00e989
2026-01-14 16:38:24,878 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/37e6b76b-232a-41ec-8d99-a501dffe4186
INFO:     127.0.0.1:56968 - "PUT /api/v1/chapters/37e6b76b-232a-41ec-8d99-a501dffe4186 HTTP/1.1" 200 OK
2026-01-14 16:38:24,883 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
[TaskService] Checking daily writing task for user 79913e7e-d5cd-4e09-bce6-ca6639bd8456, word_count: 1330
[TaskService] Checking daily writing task for user 79913e7e-d5cd-4e09-bce6-ca6639bd8456, word_count: 1330
[TaskService] Daily writing task result: None
2026-01-14 16:38:27,156 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:53539551-c108-468e-b5aa-d0e20a00e989
2026-01-14 16:38:27,159 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/37e6b76b-232a-41ec-8d99-a501dffe4186
INFO:     127.0.0.1:56971 - "PUT /api/v1/chapters/37e6b76b-232a-41ec-8d99-a501dffe4186 HTTP/1.1" 200 OK
2026-01-14 16:38:27,167 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2026-01-14 16:38:27,171 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (70 paragraphs)
[TaskService] Daily writing task result: None
2026-01-14 16:38:27,179 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:53539551-c108-468e-b5aa-d0e20a00e989
2026-01-14 16:38:27,186 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/37e6b76b-232a-41ec-8d99-a501dffe4186
INFO:     127.0.0.1:56970 - "PUT /api/v1/chapters/37e6b76b-232a-41ec-8d99-a501dffe4186 HTTP/1.1" 200 OK
2026-01-14 16:38:27,197 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2026-01-14 16:38:31,605 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (70 paragraphs)
2026-01-14 16:38:31,670 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (70 paragraphs)
2026-01-14 16:38:36,832 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:guidelines:53539551-c108-468e-b5aa-d0e20a00e989
2026-01-14 16:38:36,835 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:characters:53539551-c108-468e-b5aa-d0e20a00e989 (expire=300s)
2026-01-14 16:38:36,838 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:settings:53539551-c108-468e-b5aa-d0e20a00e989 (expire=300s)
2026-01-14 16:38:36,841 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:ai-guidelines:53539551-c108-468e-b5aa-d0e20a00e989
2026-01-14 16:38:36,848 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:locations:53539551-c108-468e-b5aa-d0e20a00e989 (expire=300s)
2026-01-14 16:38:36,851 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/53539551-c108-468e-b5aa-d0e20a00e989/guidelines
2026-01-14 16:38:36,853 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/53539551-c108-468e-b5aa-d0e20a00e989/characters
2026-01-14 16:38:36,855 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/53539551-c108-468e-b5aa-d0e20a00e989/settings
2026-01-14 16:38:36,858 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/53539551-c108-468e-b5aa-d0e20a00e989/ai-guidelines
INFO:     127.0.0.1:63446 - "GET /api/v1/worldview/works/53539551-c108-468e-b5aa-d0e20a00e989/guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:63443 - "GET /api/v1/worldview/works/53539551-c108-468e-b5aa-d0e20a00e989/characters HTTP/1.1" 200 OK
INFO:     127.0.0.1:63445 - "GET /api/v1/worldview/works/53539551-c108-468e-b5aa-d0e20a00e989/settings HTTP/1.1" 200 OK
INFO:     127.0.0.1:63447 - "GET /api/v1/worldview/works/53539551-c108-468e-b5aa-d0e20a00e989/ai-guidelines HTTP/1.1" 200 OK
2026-01-14 16:38:36,869 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/53539551-c108-468e-b5aa-d0e20a00e989/locations
INFO:     127.0.0.1:63444 - "GET /api/v1/worldview/works/53539551-c108-468e-b5aa-d0e20a00e989/locations HTTP/1.1" 200 OK
2026-01-14 16:39:01,919 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:guidelines:53539551-c108-468e-b5aa-d0e20a00e989
2026-01-14 16:39:01,922 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:characters:53539551-c108-468e-b5aa-d0e20a00e989 (expire=300s)
2026-01-14 16:39:01,936 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/53539551-c108-468e-b5aa-d0e20a00e989/guidelines
2026-01-14 16:39:01,937 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/53539551-c108-468e-b5aa-d0e20a00e989/characters
2026-01-14 16:39:01,940 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:ai-guidelines:53539551-c108-468e-b5aa-d0e20a00e989
2026-01-14 16:39:01,946 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:locations:53539551-c108-468e-b5aa-d0e20a00e989 (expire=300s)
2026-01-14 16:39:01,950 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:settings:53539551-c108-468e-b5aa-d0e20a00e989 (expire=300s)
INFO:     127.0.0.1:63077 - "GET /api/v1/worldview/works/53539551-c108-468e-b5aa-d0e20a00e989/guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:63074 - "GET /api/v1/worldview/works/53539551-c108-468e-b5aa-d0e20a00e989/characters HTTP/1.1" 200 OK
2026-01-14 16:39:01,957 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/53539551-c108-468e-b5aa-d0e20a00e989/ai-guidelines
2026-01-14 16:39:01,959 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/53539551-c108-468e-b5aa-d0e20a00e989/locations
2026-01-14 16:39:01,961 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/53539551-c108-468e-b5aa-d0e20a00e989/settings
INFO:     127.0.0.1:63079 - "GET /api/v1/worldview/works/53539551-c108-468e-b5aa-d0e20a00e989/ai-guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:63075 - "GET /api/v1/worldview/works/53539551-c108-468e-b5aa-d0e20a00e989/locations HTTP/1.1" 200 OK
INFO:     127.0.0.1:63076 - "GET /api/v1/worldview/works/53539551-c108-468e-b5aa-d0e20a00e989/settings HTTP/1.1" 200 OK
2026-01-14 16:39:03,464 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-14 16:39:05,218 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:58098 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2026-01-14 16:39:05,239 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-14 16:39:05,240 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-14 16:39:05,241 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2026-01-14 16:39:07,264 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-14 16:39:07,268 - app.api.v1.agent - INFO - [Chat Stream] Mode: planning
2026-01-14 16:39:07,283 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:64915 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2026-01-14 16:39:07,299 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 你是资深写作研究员。完成以下严格流程：
  【工具使用规则】
  1) 只允许在“第1步”调用一次读...
2026-01-14 16:39:07,301 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-14 16:39:07,303 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-14 16:39:07,304 - app.services.ai.http_ai_service - INFO - [成本追踪] 初始化未传db/user_id，将使用请求上下文按需记录成本
2026-01-14 16:39:11,652 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-14 16:39:11,653 - app.services.agent.tools.writing_tools - INFO - Writing tools AI service initialized
2026-01-14 16:39:11,654 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ AI Service 已同时设置到 langgraph_tools 和 writing_tools
2026-01-14 16:39:11,658 - app.services.context.adaptive_budget - INFO - ✅ 所有预算配置验证通过
2026-01-14 16:39:20,965 - app.services.context.vector_memory_store - INFO - ✅ VectorMemoryStore初始化成功 | 目录=./data/chroma_db | 模型=paraphrase-multilingual-MiniLM-L12-v2 | 集合=user_memories
2026-01-14 16:39:20,966 - app.services.context.manager - INFO - ✅ VectorMemoryStore 已初始化
2026-01-14 16:39:20,967 - app.services.context.manager - INFO - ✅ ContextManager: 长期记忆已启用 (user_id=None)
2026-01-14 16:39:20,969 - app.services.context.manager - INFO - ✅ ContextManager: 自适应预算已启用
2026-01-14 16:39:20,971 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ ContextManager已初始化（长期记忆已启用，自适应预算已启用，总预算=16000 tokens）
成功加载模板: analyze_text (版本 3.1.0)
成功加载模板: writing_agent (版本 2.0.0)
成功加载模板: system_agent_prompt (版本 2.1.0)
成功加载模板: creative_writing_prompt (版本 1.0.0)
2026-01-14 16:39:21,024 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ PromptManager已初始化
2026-01-14 16:39:23,085 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ Redis连接验证成功
2026-01-14 16:39:23,089 - app.services.agent.langgraph_agent - INFO - [LangGraph] OK 使用 AsyncRedisSaver（redis://localhost:6379/0，TTL=7天）
2026-01-14 16:39:23,092 - app.services.agent.memory.metrics - INFO - [MemoryMetrics] 监控系统已初始化
2026-01-14 16:39:23,096 - app.services.agent.memory.long_term_store - INFO - [LongTermStore] Initialized: base_dir=./data/long_term_memory, max_size=50KB, compression=True
2026-01-14 16:39:23,097 - app.services.agent.memory.enhanced_memory_manager - INFO - EnhancedMemoryManager initialized: short=10, medium=100, threshold=0.1, long_term_backup=enabled
2026-01-14 16:39:23,102 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ EnhancedMemoryManager已创建
2026-01-14 16:39:23,106 - app.services.agent.memory.unified_coordinator - INFO - [UnifiedMemoryCoordinator] 初始化统一记忆协调器
2026-01-14 16:39:23,107 - app.services.agent.memory.unified_coordinator - INFO - [UnifiedMemoryCoordinator] 全局实例已设置
2026-01-14 16:39:23,110 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ UnifiedMemoryCoordinator已初始化 | checkpointer=AsyncRedisSaver | enhanced_memory=yes | context_manager=yes
2026-01-14 16:39:23,112 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ 解耦模块已初始化 (IntentClassifier, ToolExecutor, EventParser, ResponseBuilder, ToolDispatcher, ParallelExecutor, PlanGenerator, QuickPathHandler, StreamEventHandler, SecondaryToolHandler, TaskRunner, AgentExecutor)
2026-01-14 16:39:23,133 - app.services.agent.parallel_tool_node - INFO - [ParallelToolNode] 初始化完成，最大并发数=5，并行安全工具=6个
2026-01-14 16:39:23,170 - app.api.v1.agent - INFO - [Global Agent] created global agent instance; MemorySaver shared across requests
2026-01-14 16:39:23,192 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:53539551-c108-468e-b5aa-d0e20a00e989:8efa14f9-6c6d-4f6d-b441-63b6387ed111 (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=53539551-c108-468e-b5aa-d0e20a00e989, conversation_id=8efa14f9-6c6d-4f6d-b441-63b6387ed111)
2026-01-14 16:39:23,193 - app.services.context.monitoring_integration - INFO - ✅ ContextManager监控收集器已初始化
2026-01-14 16:39:23,194 - app.services.context.store - INFO - [ContextStore] Redis连接成功
2026-01-14 16:39:23,338 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 35 个数据块，总长度: 4553
2026-01-14 16:39:23,339 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 17652 (prompt=15378, completion=2274)
2026-01-14 16:39:23,340 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 实例, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-14 16:39:23,343 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-14 16:39:23,370 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-14 16:39:23,372 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:实例): tokens=17652, cost=$0.041962, time=73921ms
2026-01-14 16:39:23,374 - app.services.worldview_sync_service - INFO - [世界观同步] AI响应长度: 4553
2026-01-14 16:39:23,374 - app.services.worldview_sync_service - INFO - [世界观同步] AI响应内容: ```json
{
  "new_characters": [
    {
      "name": "段融",
      "role": "主角",
      "description": "小说主角，从现代社会魂穿而来。现为源顺镖局的杂役弟子，身怀“吞噬器灵”的特殊能力，能吸收兵器中的经验与武技。性格坚韧、务实且有心计，正努力通过考核成为学徒以改变命运。",
      "first_appearance": "第1章",
      "importance": "高"
    },
    {
      "name": "杨震",
      "role": "配角",
      "description": "主角段融的发小，在县衙担任捕快。为人仗义但略带炫耀心理，因其二叔在生药铺工作而有些门路。他是主角在外界的重要联系人，并提供了关于太一门叛徒的关键信息。",
      "first_appearance": "第5章",
      "importance": "高"
    },
    {
      "name": "赵穆",
      "role": ...
2026-01-14 16:39:23,376 - app.services.worldview_sync_service - INFO - [世界观同步] 解析结果: 新人物=9, 新地点=8, 新设定=7
2026-01-14 16:39:23,389 - app.api.v1.import_routes - INFO - [世界观提取] 扫描完成: 5章, 发现 9人物, 8地点, 7设定
2026-01-14 16:39:23,414 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 段融
2026-01-14 16:39:23,428 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 杨震
2026-01-14 16:39:23,444 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 赵穆
2026-01-14 16:39:23,457 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 孔斌, 李充, 张征
2026-01-14 16:39:23,488 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 解道寒
2026-01-14 16:39:23,511 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 许儒虎
2026-01-14 16:39:23,535 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 萧宗庭
2026-01-14 16:39:23,557 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 孙老头
2026-01-14 16:39:23,571 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 解雷
2026-01-14 16:39:23,600 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 九州大陆
2026-01-14 16:39:23,621 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 青州
2026-01-14 16:39:23,629 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 太一门
2026-01-14 16:39:23,649 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 贤古县
2026-01-14 16:39:23,674 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 源顺镖局
2026-01-14 16:39:23,697 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 渊阳府
2026-01-14 16:39:23,705 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 县衙
2026-01-14 16:39:23,724 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 段融的家
2026-01-14 16:39:23,755 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 吞噬器灵
2026-01-14 16:39:23,777 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 器灵
2026-01-14 16:39:23,800 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 宗门统治体系
2026-01-14 16:39:23,818 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 武道修炼体系
2026-01-14 16:39:23,840 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 内息/内功
2026-01-14 16:39:23,859 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 源顺镖局晋升体系
2026-01-14 16:39:23,876 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 货币体系
2026-01-14 16:39:23,897 - app.services.worldview_sync_service - INFO - [世界观同步] 创建关系: 段融 -> 杨震: 确认并发扬了发小情谊，成为主角在外部世界的重要盟友。
2026-01-14 16:39:23,902 - app.services.worldview_sync_service - INFO - [世界观同步] 创建关系: 段融 -> 赵穆: 建立了“下属与高傲上司”的对立关系，并因吞噬事件产生了“受害者与加害者”的隐秘联系。
2026-01-14 16:39:23,905 - app.services.worldview_sync_service - INFO - [世界观同步] 创建关系: 段融 -> 孔斌, 李充, 张征: 确立为晋升学徒道路上的直接竞争对手关系。
2026-01-14 16:39:23,924 - app.services.worldview_sync_service - INFO - [Worldview Sync] Cache invalidated: worldview:characters:53539551-c108-468e-b5aa-d0e20a00e989
2026-01-14 16:39:23,926 - app.services.worldview_sync_service - INFO - [Worldview Sync] Cache invalidated: worldview:locations:53539551-c108-468e-b5aa-d0e20a00e989
2026-01-14 16:39:23,929 - app.services.worldview_sync_service - INFO - [Worldview Sync] Cache invalidated: worldview:settings:53539551-c108-468e-b5aa-d0e20a00e989
2026-01-14 16:39:23,931 - app.services.worldview_sync_service - INFO - [Worldview Sync] Cache invalidated: worldview:guidelines:53539551-c108-468e-b5aa-d0e20a00e989
2026-01-14 16:39:23,935 - app.services.worldview_sync_service - INFO - [Worldview Sync] Cache invalidated: worldview:worlddata:53539551-c108-468e-b5aa-d0e20a00e989
2026-01-14 16:39:23,936 - app.api.v1.import_routes - INFO - [世界观提取] 应用完成: {'characters_created': 9, 'characters_updated': 0, 'locations_created': 8, 'settings_created': 7, 'relationships_created': 3}
2026-01-14 16:39:25,243 - app.services.context.manager - INFO - [ContextManager] 创建新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:53539551-c108-468e-b5aa-d0e20a00e989:8efa14f9-6c6d-4f6d-b441-63b6387ed111
2026-01-14 16:39:25,780 - app.services.context.token_counter - INFO - ✅ tiktoken初始化成功，模型: gemini-2.5-pro -> cl100k_base
2026-01-14 16:39:25,789 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:53539551-c108-468e-b5aa-d0e20a00e989:8efa14f9-6c6d-4f6d-b441-63b6387ed111: 0/16000 tokens
2026-01-14 16:39:27,005 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='你是资深写作研究员。完成以下严格流程：
  【工具使用规则】...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:53539551-c108-468e-b5aa-d0e20a00e989', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=0条
2026-01-14 16:39:27,006 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=53539551-c108-468e-b5aa-d0e20a00e989 | 含用户级=True | 找到=0条
2026-01-14 16:39:27,008 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 0条消息, 0 tokens, 耗时 3813.07ms
2026-01-14 16:39:27,010 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-14 16:39:27,012 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-14 16:39:27,013 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=20, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-14 16:39:29,735 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-14 16:39:29,736 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-14 16:39:29,775 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-14 16:39:29,777 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1001, cost=$0.000100, time=2724ms
2026-01-14 16:39:29,777 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=8, 尝试次数=1
2026-01-14 16:39:29,780 - app.services.agent.intent.classifier - INFO - [Intent] AI识别结果: planning
2026-01-14 16:39:29,782 - app.services.agent.langgraph_agent - INFO - [Planning] AI意图分类: planning (置信度: 0.90)
2026-01-14 16:39:29,783 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 你是资深写作研究员。完成以下严格流程：
  【工具使用规则】
  1) 只允许在“第1步”调用一次读...
2026-01-14 16:39:29,801 - app.core.cache - INFO - ✅ 缓存命中: prompt:planning:v2.39.0:get_planning_static_prompt:fca6eb91156619d0
2026-01-14 16:39:29,806 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-14 16:39:29,807 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=story_planning, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: story_planning; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-01-14 16:39:29,808 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.3, task_type=TaskType.STORY_PLANNING
2026-01-14 16:39:42,890 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-14 16:39:46,906 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 9 个数据块，总长度: 1069
2026-01-14 16:39:46,909 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 23939 (prompt=23382, completion=557)
2026-01-14 16:39:46,911 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-14 16:39:46,916 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-14 16:39:46,938 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-14 16:39:46,939 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=23939, cost=$0.034798, time=17109ms
2026-01-14 16:39:46,940 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=23939
2026-01-14 16:39:46,942 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户要求我扮演一名资深写作研究员，并遵循一个严格的五步流程。, 原料=我需要一次性获取作品第1-5章的核心内容, 处理=1. **第1步**: 调用 `get_
2026-01-14 16:39:46,943 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共1个任务
2026-01-14 16:39:46,945 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共1个任务，耗时: 17.16s
2026-01-14 16:39:46,946 - app.api.v1.agent - INFO - [Stream] Plan tasks: 1 items
2026-01-14 16:39:46,946 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2026-01-14 16:39:46,951 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2026-01-14 16:39:46,952 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2026-01-14 16:39:46,953 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 任务分组: 第一层并行=0, 第二层并行=0, 串行=1
2026-01-14 16:39:46,955 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始串行执行1个任务
2026-01-14 16:39:46,957 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务1开始: 获取第1-5章内容，覆盖主要人物、关键事件、器灵/武技信息、地点与势力线索，作为后续分析的“原始材料”。
2026-01-14 16:39:46,959 - app.api.v1.agent - INFO - [Stream] Task started: 获取第1-5章内容，覆盖主要人物、关键事件、器灵/武技信息、地点与势力线索，作为后续分析的“原始材料”。 (icon=Wrench)
2026-01-14 16:39:46,960 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: get_writing_context
2026-01-14 16:39:46,962 - app.services.agent.tools.tool_types - INFO - [get_writing_context] 开始执行工具
2026-01-14 16:39:47,010 - app.services.agent.langgraph_tools - INFO - [get_writing_context] ✅ 获取创作上下文成功: include=chapter
2026-01-14 16:39:47,022 - app.services.agent.tools.tool_types - INFO - [get_writing_context] 执行成功 (耗时: 0.060s)
2026-01-14 16:39:47,026 - app.services.agent.tools.tool_monitor - INFO - ToolMonitor initialized with Memory storage, retention: 7 days
2026-01-14 16:39:47,031 - app.services.agent.execution.tool_executor - INFO - [StandardTool] get_writing_context 执行成功
2026-01-14 16:39:47,038 - app.services.agent.utils.chapter_cache - INFO - [ChapterCache] 📝 写入: 494a31c1... (第1章)
2026-01-14 16:39:47,041 - app.services.agent.utils.chapter_cache - INFO - [ChapterCache] 📝 写入: f145fb07... (第2章)
2026-01-14 16:39:47,046 - app.services.agent.utils.chapter_cache - INFO - [ChapterCache] 📝 写入: ba77b261... (第3章)
2026-01-14 16:39:47,049 - app.services.agent.utils.chapter_cache - INFO - [ChapterCache] 📝 写入: 0a8fada7... (第4章)
2026-01-14 16:39:47,056 - app.services.agent.utils.chapter_cache - INFO - [ChapterCache] 📝 写入: 37e6b76b... (第5章)
2026-01-14 16:39:47,059 - app.services.agent.execution.tool_executor - INFO - [ChapterCache] 📝 get_writing_context 缓存写入: 5 章
2026-01-14 16:39:47,065 - app.api.v1.agent - INFO - [Stream] 任务完成: 获取第1-5章内容，覆盖主要人物、关键事件、器灵/武技信息、地点与势力线索，作为后续分析的“原始材料”。 (0.1s)
2026-01-14 16:39:47,072 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务1完成
2026-01-14 16:39:47,076 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共1个任务，耗时: 0.13s
2026-01-14 16:39:47,081 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2026-01-14 16:39:47,085 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=1, 输出型=0, 展示型=0
2026-01-14 16:39:47,099 - app.services.agent.langgraph_agent - WARNING - [Response] 没有明确输出任务，使用AI整合
2026-01-14 16:39:47,101 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2026-01-14 16:39:47,106 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=1, 输出型=0, 展示型=0
2026-01-14 16:39:47,108 - app.services.agent.utils.context_builder - INFO - [Compress] 任务1工具'get_writing_context'，内容长度12780，保留10000字符（省略2780字符）
2026-01-14 16:39:47,110 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=13873字符, 处理后=11172字符
2026-01-14 16:39:47,116 - app.services.agent.planning.response_builder - INFO - [Summarization] 准备发送 summarization_start 事件
2026-01-14 16:39:47,119 - app.services.agent.stream.stream_event_handler - INFO - [StreamEventHandler] emit_summarization_start 被调用, _on_flow_event=True
2026-01-14 16:39:47,130 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_start 事件已发送
2026-01-14 16:39:47,139 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2026-01-14 16:39:47,155 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2026-01-14 16:39:47,299 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-14 16:39:47,303 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-14 16:39:47,308 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
2026-01-14 16:39:47,323 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:ai-guidelines:53539551-c108-468e-b5aa-d0e20a00e989
2026-01-14 16:39:47,355 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:characters:53539551-c108-468e-b5aa-d0e20a00e989 (expire=300s)
2026-01-14 16:39:47,366 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:settings:53539551-c108-468e-b5aa-d0e20a00e989 (expire=300s)
2026-01-14 16:39:47,382 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:guidelines:53539551-c108-468e-b5aa-d0e20a00e989 (expire=300s)
2026-01-14 16:39:47,398 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/53539551-c108-468e-b5aa-d0e20a00e989/ai-guidelines
2026-01-14 16:39:47,404 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/53539551-c108-468e-b5aa-d0e20a00e989/characters
2026-01-14 16:39:47,411 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:locations:53539551-c108-468e-b5aa-d0e20a00e989 (expire=300s)
2026-01-14 16:39:47,415 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/53539551-c108-468e-b5aa-d0e20a00e989/settings
INFO:     127.0.0.1:51354 - "GET /api/v1/worldview/works/53539551-c108-468e-b5aa-d0e20a00e989/ai-guidelines HTTP/1.1" 200 OK
2026-01-14 16:39:47,422 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/53539551-c108-468e-b5aa-d0e20a00e989/guidelines
INFO:     127.0.0.1:51349 - "GET /api/v1/worldview/works/53539551-c108-468e-b5aa-d0e20a00e989/characters HTTP/1.1" 200 OK
INFO:     127.0.0.1:51351 - "GET /api/v1/worldview/works/53539551-c108-468e-b5aa-d0e20a00e989/settings HTTP/1.1" 200 OK
INFO:     127.0.0.1:51353 - "GET /api/v1/worldview/works/53539551-c108-468e-b5aa-d0e20a00e989/guidelines HTTP/1.1" 200 OK
2026-01-14 16:39:47,446 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/53539551-c108-468e-b5aa-d0e20a00e989/locations
INFO:     127.0.0.1:51352 - "GET /api/v1/worldview/works/53539551-c108-468e-b5aa-d0e20a00e989/locations HTTP/1.1" 200 OK
2026-01-14 16:40:01,313 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-14 16:40:01,316 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_complete 事件已发送（第一个chunk时）
2026-01-14 16:40:01,317 - app.services.agent.planning.response_builder - INFO - [Summarization] output_ready 事件已发送（第一个chunk时）
2026-01-14 16:40:04,323 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 11 个数据块，总长度: 865
2026-01-14 16:40:04,327 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 12266 (prompt=11723, completion=543)
2026-01-14 16:40:04,331 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-14 16:40:04,337 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-14 16:40:04,379 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-14 16:40:04,385 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=12266, cost=$0.004874, time=17028ms
2026-01-14 16:40:04,389 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=865
2026-01-14 16:40:04,502 - app.services.context.vector_memory_store - INFO - 🔁 跳过重复记忆，复用ID=79913e7e-d5cd-4e09-bce6-ca6639bd8456_1768376850595_2da49c7d
2026-01-14 16:40:04,504 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:53539551-c108-468e-b5aa-d0e20a00e989 | 重要度=1.00
2026-01-14 16:40:05,679 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:53539551-c108-468e-b5aa-d0e20a00e989 | 重要度=0.60
2026-01-14 16:40:05,703 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:53539551-c108-468e-b5aa-d0e20a00e989:8efa14f9-6c6d-4f6d-b441-63b6387ed111, token=1743
2026-01-14 16:40:05,711 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:53539551-c108-468e-b5aa-d0e20a00e989:8efa14f9-6c6d-4f6d-b441-63b6387ed111, 消息数=2, 摘要长度=0, Token=1743
2026-01-14 16:40:05,716 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:53539551-c108-468e-b5aa-d0e20a00e989:8efa14f9-6c6d-4f6d-b441-63b6387ed111)
2026-01-14 16:40:05,723 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2026-01-14 16:40:05,741 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed
2026-01-14 16:40:10,111 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/8efa14f9-6c6d-4f6d-b441-63b6387ed111
INFO:     127.0.0.1:56608 - "GET /api/v1/agent/operations/8efa14f9-6c6d-4f6d-b441-63b6387ed111 HTTP/1.1" 200 OK
2026-01-14 16:40:47,431 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-14 16:40:47,431 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-14 16:40:47,433 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2026-01-14 16:40:49,638 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-14 16:40:49,641 - app.api.v1.agent - INFO - [Chat Stream] Mode: planning
2026-01-14 16:40:49,646 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:52773 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2026-01-14 16:40:49,668 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 没有要求，继续...
2026-01-14 16:40:49,686 - app.api.v1.agent - INFO - [agent_chat_stream] 📚 世界观数据已注入: 人物=9, 地点=8, 设定=7, 规范=无
2026-01-14 16:40:49,690 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:53539551-c108-468e-b5aa-d0e20a00e989:8efa14f9-6c6d-4f6d-b441-63b6387ed111 (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=53539551-c108-468e-b5aa-d0e20a00e989, conversation_id=8efa14f9-6c6d-4f6d-b441-63b6387ed111)
2026-01-14 16:40:49,703 - app.services.context.store - INFO - [ContextStore] 加载上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:53539551-c108-468e-b5aa-d0e20a00e989:8efa14f9-6c6d-4f6d-b441-63b6387ed111, 2条消息
2026-01-14 16:40:49,713 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:53539551-c108-468e-b5aa-d0e20a00e989:8efa14f9-6c6d-4f6d-b441-63b6387ed111: 1743/16000 tokens
2026-01-14 16:40:49,863 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='没有要求，继续...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:53539551-c108-468e-b5aa-d0e20a00e989', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=0条
2026-01-14 16:40:49,864 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=53539551-c108-468e-b5aa-d0e20a00e989 | 含用户级=True | 找到=0条
2026-01-14 16:40:49,870 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 2条消息, 1743 tokens, 耗时 172.14ms
2026-01-14 16:40:49,877 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 2 条历史消息 (token: 1743, has_summary: False)
2026-01-14 16:40:49,880 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-14 16:40:49,882 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-14 16:40:49,884 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=20, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-14 16:40:51,066 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-14 16:40:51,067 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-14 16:40:51,090 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-14 16:40:51,093 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=285, cost=$0.000029, time=1184ms
2026-01-14 16:40:51,095 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=7, 尝试次数=1
2026-01-14 16:40:51,101 - app.services.agent.intent.classifier - INFO - [Intent] AI识别结果: general
2026-01-14 16:40:51,103 - app.services.agent.langgraph_agent - INFO - [Planning] AI意图分类: general (置信度: 0.90)
2026-01-14 16:40:51,106 - app.services.agent.langgraph_agent - INFO - [Planning] 识别为 general 意图，但仍走 LangGraph 流程（支持工具调用）
2026-01-14 16:40:51,110 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 没有要求，继续...
2026-01-14 16:40:51,119 - app.core.cache - INFO - ✅ 缓存命中: prompt:planning:v2.39.0:get_planning_static_prompt:fca6eb91156619d0
2026-01-14 16:40:51,127 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-14 16:40:51,128 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=story_planning, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: story_planning; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-01-14 16:40:51,130 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.3, task_type=TaskType.STORY_PLANNING
2026-01-14 16:41:40,301 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-14 16:42:07,377 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 49 个数据块，总长度: 5077
2026-01-14 16:42:07,377 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 30829 (prompt=27691, completion=3138)
2026-01-14 16:42:07,378 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-14 16:42:07,379 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-14 16:42:07,406 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-14 16:42:07,407 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=30829, cost=$0.065994, time=76251ms
2026-01-14 16:42:07,408 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=30829
2026-01-14 16:42:08,427 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-14 16:42:08,429 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=story_planning, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: story_planning; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-01-14 16:42:08,430 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.4, task_type=TaskType.STORY_PLANNING
2026-01-14 16:42:24,297 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-14 16:43:01,460 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 65 个数据块，总长度: 6757
2026-01-14 16:43:01,462 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 28479 (prompt=24263, completion=4216)
2026-01-14 16:43:01,465 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-14 16:43:01,468 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-14 16:43:01,506 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-14 16:43:01,507 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=28479, cost=$0.072489, time=53039ms
2026-01-14 16:43:01,508 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=28479
2026-01-14 16:43:01,509 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共2个任务
2026-01-14 16:43:01,510 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共2个任务，耗时: 130.40s
2026-01-14 16:43:01,511 - app.api.v1.agent - INFO - [Stream] Plan tasks: 2 items
2026-01-14 16:43:01,512 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2026-01-14 16:43:01,513 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2026-01-14 16:43:01,515 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2026-01-14 16:43:01,516 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 任务分组: 第一层并行=1, 第二层并行=0, 串行=1
2026-01-14 16:43:01,517 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始第一层并行执行1个任务
2026-01-14 16:43:01,518 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务1开始: 理解用户意图并获取相关上下文
2026-01-14 16:43:01,519 - app.api.v1.agent - INFO - [Stream] Task started: 理解用户意图并获取相关上下文 (icon=BookOpen)
2026-01-14 16:43:01,520 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 ToolExecutor(get_context)
2026-01-14 16:43:01,522 - app.services.agent.tools.tool_types - INFO - [get_context] 开始执行工具
2026-01-14 16:43:01,525 - app.services.agent.langgraph_tools - WARNING - [get_context_tool] ⚠️ 此工具已废弃，请使用 get_writing_context
2026-01-14 16:43:01,547 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=53539551-c108-468e-b5aa-d0e20a00e989, current_order=5, query=作品背景、人物关系、情节发展...
2026-01-14 16:43:01,883 - app.services.chapter_vector_service - INFO - RAG retrieved 5 segments within order<=5
2026-01-14 16:43:01,892 - app.services.agent.langgraph_tools - INFO - [get_writing_context] ✅ 获取创作上下文成功: include=work,chapter,rag
2026-01-14 16:43:01,901 - app.services.agent.tools.tool_types - INFO - [get_context] 执行成功 (耗时: 0.379s)
2026-01-14 16:43:01,905 - app.services.agent.execution.tool_executor - INFO - [StandardTool] get_context 执行成功
2026-01-14 16:43:01,915 - app.services.agent.execution.task_runner - INFO - [TaskRunner] get_context 执行成功（ToolExecutor）
2026-01-14 16:43:01,917 - app.api.v1.agent - INFO - [Stream] 任务完成: 理解用户意图并获取相关上下文 (0.4s)
2026-01-14 16:43:01,920 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务1完成
2026-01-14 16:43:01,928 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始串行执行1个任务
2026-01-14 16:43:01,933 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务2开始: 基于上下文响应用户请求
2026-01-14 16:43:01,936 - app.api.v1.agent - INFO - [Stream] Task started: 基于上下文响应用户请求 (icon=FileSearch)
2026-01-14 16:43:01,941 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 解析占位符: $TASK_1.None$
2026-01-14 16:43:01,947 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 任务1结果长度: 2173
2026-01-14 16:43:01,955 - app.services.agent.utils.tool_helpers - INFO - [参数标准化] analyze_content.content → text
2026-01-14 16:43:01,960 - app.services.agent.utils.tool_helpers - INFO - [参数标准化] analyze_content.analysis_types: str → list
2026-01-14 16:43:01,965 - app.services.agent.execution.task_runner - INFO - [TaskRunner] analyze_text_tool 使用 focus: '根据用户请求进行分析或回答...'
2026-01-14 16:43:01,966 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 ToolExecutor(analyze_content)
2026-01-14 16:43:01,974 - app.services.agent.tools.tool_types - INFO - [analyze_content] 开始执行工具
2026-01-14 16:43:02,012 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-14 16:43:02,013 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-14 16:43:02,014 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=3000, temp=0.3, task_type=TaskType.SUMMARIZATION
2026-01-14 16:43:12,907 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-14 16:43:21,584 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 26 个数据块，总长度: 2393
2026-01-14 16:43:21,584 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 6495 (prompt=4798, completion=1697)
2026-01-14 16:43:21,585 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-14 16:43:21,586 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-14 16:43:21,617 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-14 16:43:21,618 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=6495, cost=$0.005682, time=19569ms
2026-01-14 16:43:21,620 - app.services.agent.tools.tool_types - INFO - [analyze_content] 执行成功 (耗时: 19.646s)
2026-01-14 16:43:21,627 - app.services.agent.execution.tool_executor - INFO - [StandardTool] analyze_content 执行成功
2026-01-14 16:43:21,628 - app.services.agent.execution.task_runner - INFO - [TaskRunner] analyze_content 执行成功（ToolExecutor）
2026-01-14 16:43:21,631 - app.api.v1.agent - INFO - [Stream] 任务完成: 基于上下文响应用户请求 (19.7s)
2026-01-14 16:43:21,634 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务2完成
2026-01-14 16:43:21,637 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共2个任务，耗时: 20.13s
2026-01-14 16:43:21,641 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2026-01-14 16:43:21,644 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=1, 输出型=1, 展示型=0
2026-01-14 16:43:21,646 - app.services.agent.langgraph_agent - INFO - [Response] 单个输出任务(analyze_content)，使用AI整合
2026-01-14 16:43:21,648 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2026-01-14 16:43:21,650 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=1, 输出型=1, 展示型=0
2026-01-14 16:43:21,651 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=4605字符, 处理后=4635字符
2026-01-14 16:43:21,651 - app.services.agent.planning.response_builder - INFO - [Summarization] 准备发送 summarization_start 事件
2026-01-14 16:43:21,652 - app.services.agent.stream.stream_event_handler - INFO - [StreamEventHandler] emit_summarization_start 被调用, _on_flow_event=True
2026-01-14 16:43:21,654 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_start 事件已发送
2026-01-14 16:43:21,655 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2026-01-14 16:43:21,661 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2026-01-14 16:43:21,681 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-14 16:43:21,684 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-14 16:43:21,690 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
2026-01-14 16:43:24,688 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-14 16:43:24,689 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_complete 事件已发送（第一个chunk时）
2026-01-14 16:43:24,690 - app.services.agent.planning.response_builder - INFO - [Summarization] output_ready 事件已发送（第一个chunk时）
2026-01-14 16:43:30,549 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 29 个数据块，总长度: 2057
2026-01-14 16:43:30,552 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 5847 (prompt=4430, completion=1417)
2026-01-14 16:43:30,555 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-14 16:43:30,558 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-14 16:43:30,601 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-14 16:43:30,603 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=5847, cost=$0.004871, time=8867ms
2026-01-14 16:43:30,604 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=2057
2026-01-14 16:43:31,457 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:53539551-c108-468e-b5aa-d0e20a00e989 | 重要度=0.72
2026-01-14 16:43:32,565 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:53539551-c108-468e-b5aa-d0e20a00e989 | 重要度=0.94
2026-01-14 16:43:32,591 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:53539551-c108-468e-b5aa-d0e20a00e989:8efa14f9-6c6d-4f6d-b441-63b6387ed111, token=3919
2026-01-14 16:43:32,601 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:53539551-c108-468e-b5aa-d0e20a00e989:8efa14f9-6c6d-4f6d-b441-63b6387ed111, 消息数=4, 摘要长度=0, Token=3919
2026-01-14 16:43:32,604 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:53539551-c108-468e-b5aa-d0e20a00e989:8efa14f9-6c6d-4f6d-b441-63b6387ed111)
2026-01-14 16:43:32,608 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2026-01-14 16:43:32,620 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed
2026-01-14 16:43:45,466 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/8efa14f9-6c6d-4f6d-b441-63b6387ed111
INFO:     127.0.0.1:59013 - "GET /api/v1/agent/operations/8efa14f9-6c6d-4f6d-b441-63b6387ed111 HTTP/1.1" 200 OK
2026-01-14 16:44:27,205 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-14 16:44:27,206 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-14 16:44:27,207 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2026-01-14 16:44:29,832 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-14 16:44:29,833 - app.api.v1.agent - INFO - [Chat Stream] Mode: planning
2026-01-14 16:44:29,838 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:52191 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2026-01-14 16:44:29,849 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 基于你上一轮输出的 MemoryPack JSON（已在上下文中），完成以下复问。严格要求：
  1...
2026-01-14 16:44:29,858 - app.api.v1.agent - INFO - [agent_chat_stream] 📚 世界观数据已注入: 人物=9, 地点=8, 设定=7, 规范=无
2026-01-14 16:44:29,860 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:53539551-c108-468e-b5aa-d0e20a00e989:8efa14f9-6c6d-4f6d-b441-63b6387ed111 (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=53539551-c108-468e-b5aa-d0e20a00e989, conversation_id=8efa14f9-6c6d-4f6d-b441-63b6387ed111)
2026-01-14 16:44:29,866 - app.services.context.store - INFO - [ContextStore] 加载上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:53539551-c108-468e-b5aa-d0e20a00e989:8efa14f9-6c6d-4f6d-b441-63b6387ed111, 4条消息
2026-01-14 16:44:29,872 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:53539551-c108-468e-b5aa-d0e20a00e989:8efa14f9-6c6d-4f6d-b441-63b6387ed111: 3919/16000 tokens
2026-01-14 16:44:30,105 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='基于你上一轮输出的 MemoryPack JSON（已在上下...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:53539551-c108-468e-b5aa-d0e20a00e989', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=2条
2026-01-14 16:44:30,110 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=53539551-c108-468e-b5aa-d0e20a00e989 | 含用户级=True | 找到=2条
2026-01-14 16:44:30,179 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 5条消息, 3919 tokens, 耗时 316.43ms
2026-01-14 16:44:30,180 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 5 条历史消息 (token: 3919, has_summary: False)
2026-01-14 16:44:30,181 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-14 16:44:30,186 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-14 16:44:30,192 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=20, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-14 16:44:31,808 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-14 16:44:31,809 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-14 16:44:31,842 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-14 16:44:31,844 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=585, cost=$0.000059, time=1620ms
2026-01-14 16:44:31,845 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=7, 尝试次数=1
2026-01-14 16:44:31,849 - app.services.agent.intent.classifier - INFO - [Intent] AI识别结果: writing
2026-01-14 16:44:31,851 - app.services.agent.langgraph_agent - INFO - [Planning] AI意图分类: writing (置信度: 0.90)
2026-01-14 16:44:31,853 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 基于你上一轮输出的 MemoryPack JSON（已在上下文中），完成以下复问。严格要求：
  1...
2026-01-14 16:44:31,861 - app.core.cache - INFO - ✅ 缓存命中: prompt:planning:v2.39.0:get_planning_static_prompt:fca6eb91156619d0
2026-01-14 16:44:31,871 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-14 16:44:31,875 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=story_planning, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: story_planning; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-01-14 16:44:31,878 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.3, task_type=TaskType.STORY_PLANNING
2026-01-14 16:44:44,275 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-14 16:44:49,842 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 11 个数据块，总长度: 1041
2026-01-14 16:44:49,843 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 26318 (prompt=25610, completion=708)
2026-01-14 16:44:49,845 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-14 16:44:49,847 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-14 16:44:49,883 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-14 16:44:49,884 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=26318, cost=$0.039093, time=17973ms
2026-01-14 16:44:49,886 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=26318
2026-01-14 16:44:49,886 - app.services.agent.planning.plan_generator - WARNING - [Planning] 第1次尝试: JSON解析失败
2026-01-14 16:44:50,893 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-14 16:44:50,895 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=story_planning, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: story_planning; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-01-14 16:44:50,896 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.4, task_type=TaskType.STORY_PLANNING
2026-01-14 16:45:08,921 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-14 16:45:14,892 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 13 个数据块，总长度: 1262
2026-01-14 16:45:14,894 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 27166 (prompt=26349, completion=817)
2026-01-14 16:45:14,896 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-14 16:45:14,898 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-14 16:45:14,917 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-14 16:45:14,919 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=27166, cost=$0.041106, time=24003ms
2026-01-14 16:45:14,920 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=27166
2026-01-14 16:45:14,922 - app.services.agent.planning.plan_generator - WARNING - [Planning] 第2次尝试: JSON解析失败
2026-01-14 16:45:14,925 - app.services.agent.planning.plan_generator - WARNING - [Planning] 无法解析规划JSON，AI返回: 好的，我将严格依据您上一轮提供的 MemoryPack JSON 内容，对复问清单进行回答。

---

**Q1: 段融在镖局的身份与日常工作是什么？**
他是源顺镖局的杂役弟子，日常负责劈柴、挑水等基础杂活。 (来源: `MemoryPack.characters[段融]`)
> 证据: “段融，源顺镖局的杂役弟子，负责劈柴、挑水等杂活。(Ch.1)”

**Q2: 赵穆的身份、对段融的态度与一次具体行为？**
赵穆是源顺镖局的实习镖师，他轻视并欺压段融，曾因段融练功慢而一脚将他踹了个趔趄。 (来源: `MemoryPack.characters[赵穆]`)
> 证据: “赵穆一脚踹在段融的屁股上，将他踹了个趔趄。(Ch.1)”

**Q3: “浑圆桩”的动作要点与赵穆强调的练法核心？**
赵穆强调“浑圆桩”的练法核心在于“浑”与“圆”二字，具体的动作要点在MemoryPack中未找到。 (来源: `MemoryPack.quotes`)
> 证据: “浑圆桩，最重要的是一个‘浑’字，一个‘圆’字。(Ch.1)”

**Q4: 段融“脑子里像塞了东西”的表现与原因？**
这是因为他
2026-01-14 16:45:14,928 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共2个任务
2026-01-14 16:45:14,934 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共2个任务，耗时: 43.08s
2026-01-14 16:45:14,939 - app.api.v1.agent - INFO - [Stream] Plan tasks: 2 items
2026-01-14 16:45:14,940 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2026-01-14 16:45:14,943 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2026-01-14 16:45:14,949 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2026-01-14 16:45:14,953 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 任务分组: 第一层并行=1, 第二层并行=0, 串行=1
2026-01-14 16:45:14,955 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始第一层并行执行1个任务
2026-01-14 16:45:14,958 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务1开始: 理解用户意图并获取相关上下文
2026-01-14 16:45:14,962 - app.api.v1.agent - INFO - [Stream] Task started: 理解用户意图并获取相关上下文 (icon=BookOpen)
2026-01-14 16:45:14,965 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 ToolExecutor(get_context)
2026-01-14 16:45:14,968 - app.services.agent.utils.tool_cache - INFO - [ToolCache] hit: tool_cache:anonymous:53539551-c108-468e-b5aa-d0e20a00e989:chapter:37e6b76b-232a-41ec-8d99-a501dffe4186:get_context:bdc4dfbe139b2a90
2026-01-14 16:45:14,970 - app.services.agent.execution.task_runner - INFO - [TaskRunner] get_context 执行成功（ToolExecutor）
2026-01-14 16:45:14,972 - app.api.v1.agent - INFO - [Stream] 任务完成: 理解用户意图并获取相关上下文 (0.0s)
2026-01-14 16:45:14,973 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务1完成
2026-01-14 16:45:14,974 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始串行执行1个任务
2026-01-14 16:45:14,978 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务2开始: 基于上下文响应用户请求
2026-01-14 16:45:14,983 - app.api.v1.agent - INFO - [Stream] Task started: 基于上下文响应用户请求 (icon=FileSearch)
2026-01-14 16:45:14,986 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 解析占位符: $TASK_1.None$
2026-01-14 16:45:14,988 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 任务1结果长度: 2173
2026-01-14 16:45:14,990 - app.services.agent.utils.tool_helpers - INFO - [参数标准化] analyze_content.content → text
2026-01-14 16:45:14,994 - app.services.agent.utils.tool_helpers - INFO - [参数标准化] analyze_content.analysis_types: str → list
2026-01-14 16:45:14,997 - app.services.agent.execution.task_runner - INFO - [TaskRunner] analyze_text_tool 使用 focus: '根据用户请求进行分析或回答...'
2026-01-14 16:45:15,002 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 ToolExecutor(analyze_content)
2026-01-14 16:45:15,006 - app.services.agent.tools.tool_types - INFO - [analyze_content] 开始执行工具
2026-01-14 16:45:15,016 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-14 16:45:15,017 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-14 16:45:15,018 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=3000, temp=0.3, task_type=TaskType.SUMMARIZATION
2026-01-14 16:45:37,851 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-14 16:45:42,409 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 17 个数据块，总长度: 1570
2026-01-14 16:45:42,410 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 7647 (prompt=6532, completion=1115)
2026-01-14 16:45:42,413 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-14 16:45:42,415 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-14 16:45:42,435 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-14 16:45:42,437 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=7647, cost=$0.004747, time=27399ms
2026-01-14 16:45:42,440 - app.services.agent.tools.tool_types - INFO - [analyze_content] 执行成功 (耗时: 27.434s)
2026-01-14 16:45:42,440 - app.services.agent.execution.tool_executor - INFO - [StandardTool] analyze_content 执行成功
2026-01-14 16:45:42,444 - app.services.agent.execution.task_runner - INFO - [TaskRunner] analyze_content 执行成功（ToolExecutor）
2026-01-14 16:45:42,446 - app.api.v1.agent - INFO - [Stream] 任务完成: 基于上下文响应用户请求 (27.5s)
2026-01-14 16:45:42,448 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务2完成
2026-01-14 16:45:42,449 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共2个任务，耗时: 27.51s
2026-01-14 16:45:42,450 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2026-01-14 16:45:42,451 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=1, 输出型=1, 展示型=0
2026-01-14 16:45:42,451 - app.services.agent.langgraph_agent - INFO - [Response] 单个输出任务(analyze_content)，使用AI整合
2026-01-14 16:45:42,452 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2026-01-14 16:45:42,453 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=1, 输出型=1, 展示型=0
2026-01-14 16:45:42,455 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=4248字符, 处理后=4278字符
2026-01-14 16:45:42,455 - app.services.agent.planning.response_builder - INFO - [Summarization] 准备发送 summarization_start 事件
2026-01-14 16:45:42,457 - app.services.agent.stream.stream_event_handler - INFO - [StreamEventHandler] emit_summarization_start 被调用, _on_flow_event=True
2026-01-14 16:45:42,458 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_start 事件已发送
2026-01-14 16:45:42,459 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2026-01-14 16:45:42,460 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2026-01-14 16:45:42,469 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-14 16:45:42,471 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-14 16:45:42,472 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
2026-01-14 16:45:57,856 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-14 16:45:57,857 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_complete 事件已发送（第一个chunk时）
2026-01-14 16:45:57,858 - app.services.agent.planning.response_builder - INFO - [Summarization] output_ready 事件已发送（第一个chunk时）
2026-01-14 16:45:59,337 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 8 个数据块，总长度: 561
2026-01-14 16:45:59,339 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 7116 (prompt=6777, completion=339)
2026-01-14 16:45:59,345 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-14 16:45:59,350 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-14 16:45:59,384 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-14 16:45:59,389 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=7116, cost=$0.002881, time=16881ms
2026-01-14 16:45:59,395 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=561
2026-01-14 16:45:59,409 - app.services.context.vector_memory_store - INFO - 🔁 跳过重复记忆，复用ID=79913e7e-d5cd-4e09-bce6-ca6639bd8456_1768377257649_eac42cef
2026-01-14 16:45:59,410 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:53539551-c108-468e-b5aa-d0e20a00e989 | 重要度=0.60
2026-01-14 16:46:00,553 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:53539551-c108-468e-b5aa-d0e20a00e989 | 重要度=0.58
2026-01-14 16:46:00,572 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:53539551-c108-468e-b5aa-d0e20a00e989:8efa14f9-6c6d-4f6d-b441-63b6387ed111, token=4816
2026-01-14 16:46:00,588 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:53539551-c108-468e-b5aa-d0e20a00e989:8efa14f9-6c6d-4f6d-b441-63b6387ed111, 消息数=6, 摘要长度=0, Token=4816
2026-01-14 16:46:00,590 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:53539551-c108-468e-b5aa-d0e20a00e989:8efa14f9-6c6d-4f6d-b441-63b6387ed111)
2026-01-14 16:46:00,593 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2026-01-14 16:46:00,602 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed
2026-01-14 16:46:03,696 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/8efa14f9-6c6d-4f6d-b441-63b6387ed111
INFO:     127.0.0.1:58004 - "GET /api/v1/agent/operations/8efa14f9-6c6d-4f6d-b441-63b6387ed111 HTTP/1.1" 200 OK
