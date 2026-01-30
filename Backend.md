2026-01-30 12:07:54,977 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
2026-01-30 12:07:54,977 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
2026-01-30 12:07:54,981 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (70 paragraphs)
2026-01-30 12:07:54,988 - app.api.v1.import_routes - INFO - [世界观提取] 开始为作品 832d8d96-080d-4d14-bcc6-80a23ffafa0e 提取世界观
INFO:     127.0.0.1:51005 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
INFO:     127.0.0.1:52300 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-30 12:07:55,259 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works
2026-01-30 12:07:55,260 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
2026-01-30 12:07:55,262 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
2026-01-30 12:07:55,266 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:50583 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
INFO:     127.0.0.1:51051 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
INFO:     127.0.0.1:51052 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
INFO:     127.0.0.1:51050 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2026-01-30 12:07:55,267 - app.services.worldview_sync_service - INFO - [世界观同步] 章节 1 '第1章 吞噬': 内容长度=3005
2026-01-30 12:07:55,267 - app.services.worldview_sync_service - INFO - [世界观同步] 章节 2 '第2章 浑圆桩': 内容长度=2674
2026-01-30 12:07:55,274 - app.services.worldview_sync_service - INFO - [世界观同步] 章节 3 '第3章 一夕千悟': 内容长度=2565
2026-01-30 12:07:55,275 - app.services.worldview_sync_service - INFO - [世界观同步] 章节 4 '第4章 家底': 内容长度=2481
2026-01-30 12:07:55,275 - app.services.worldview_sync_service - INFO - [世界观同步] 章节 5 '第5章 太一门': 内容长度=2951
2026-01-30 12:07:55,275 - app.services.worldview_sync_service - INFO - [世界观同步] 合并 5 个章节，总内容长度: 13755
2026-01-30 12:07:55,275 - app.services.worldview_sync_service - INFO - [世界观同步] 内容预览:

【第1章 第1章 吞噬】
<p>青州。</p><p>渊阳府，贤古县。</p><p>源顺镖局，后院偏房的一片空地内。</p><p>此处是镖局内，堆放柴炭的地方，平常少有人至，但此时，却有十多个单薄的身影，在空地上，稀稀落落地站着。</p><p>这些人都是十五六岁的少年，身体大多都还没长开，脸上都泛着长期营养不良的菜色。</p><p>这些少年都是源顺镖局，今年新招的杂役弟子。</p><p>刚进源顺镖局的时候，他们还一个个都兴奋异常。</p><p>因为源顺镖局的杂役弟子，是有机会学些粗浅的拳脚武技的。</p><p>学得好的，有机会晋升为学徒。</p><p>一旦成为学徒，就能学到真正的武功，而且可以跟随镖师，出去走镖。</p><p>假以时日，业务熟练了，自己也能成为镖师。</p><p>镖师虽说是吃江湖饭的，有些危险，但对这些贫苦出身的少年们，这已经是相当好的职业了。</p><p>起码能吃饱肚子，而且多少是可以捞些油水的。</p><p>但现在，他们已经进门两个半月了。</p><p>心绪也从兴奋，慢慢变得黯淡了。</p><p>杂役弟子能成为学徒的，一批里，最多一二个，而且经常的，是成批成批的覆...
2026-01-30 12:07:55,291 - app.services.worldview_sync_service - INFO - [世界观同步] 开始AI分析，章节数: 5, 内容长度: 13755
2026-01-30 12:07:55,291 - app.services.worldview_sync_service - INFO - [世界观同步] 现有世界观: （暂无世界观数据）...
2026-01-30 12:07:55,291 - app.services.worldview_sync_service - INFO - [世界观同步] db=<sqlalchemy.ext.asyncio.session.AsyncSession object at 0x000001D8C782DC10>, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:07:55,309 - app.services.ai.prompts - INFO - Prompts loaded successfully from D:\Java\ai_writer\backend\app\services\ai\prompts\default.json
2026-01-30 12:07:55,309 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-30 12:07:55,309 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-30 12:07:55,309 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2026-01-30 12:07:56,089 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz:8443/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-30 12:07:56,100 - app.services.worldview_sync_service - INFO - [世界观同步] AI服务初始化完成: api_key=***KFzr, base_url=https://204992.xyz:8443/v1, model=gemini-2.5-pro
2026-01-30 12:07:56,122 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 未传递task_type，使用默认模型: gemini-2.5-pro
2026-01-30 12:07:56,123 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=3000, temp=0.3, task_type=None
2026-01-30 12:07:56,123 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/analysis/works/832d8d96-080d-4d14-bcc6-80a23ffafa0e/status
INFO:     127.0.0.1:51334 - "GET /api/v1/analysis/works/832d8d96-080d-4d14-bcc6-80a23ffafa0e/status HTTP/1.1" 404 Not Found
2026-01-30 12:07:56,142 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/07352d22-b4c9-4aa0-90ab-2408baca9e29/revisions
INFO:     127.0.0.1:50230 - "GET /api/v1/chapters/07352d22-b4c9-4aa0-90ab-2408baca9e29/revisions?status=pending HTTP/1.1" 200 OK
2026-01-30 12:07:56,155 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-30 12:07:57,221 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
2026-01-30 12:07:57,235 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:locations:832d8d96-080d-4d14-bcc6-80a23ffafa0e (expire=300s)
2026-01-30 12:07:57,236 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/analysis/works/832d8d96-080d-4d14-bcc6-80a23ffafa0e/status
2026-01-30 12:07:57,237 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/07352d22-b4c9-4aa0-90ab-2408baca9e29/revisions
2026-01-30 12:07:57,241 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:settings:832d8d96-080d-4d14-bcc6-80a23ffafa0e (expire=300s)
INFO:     127.0.0.1:58608 - "GET /api/v1/analysis/works/832d8d96-080d-4d14-bcc6-80a23ffafa0e/status HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:58610 - "GET /api/v1/chapters/07352d22-b4c9-4aa0-90ab-2408baca9e29/revisions?status=pending HTTP/1.1" 200 OK
2026-01-30 12:07:57,245 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/832d8d96-080d-4d14-bcc6-80a23ffafa0e/locations
2026-01-30 12:07:57,246 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/832d8d96-080d-4d14-bcc6-80a23ffafa0e/settings
INFO:     127.0.0.1:59436 - "GET /api/v1/worldview/works/832d8d96-080d-4d14-bcc6-80a23ffafa0e/locations HTTP/1.1" 200 OK
INFO:     127.0.0.1:54021 - "GET /api/v1/worldview/works/832d8d96-080d-4d14-bcc6-80a23ffafa0e/settings HTTP/1.1" 200 OK
2026-01-30 12:07:57,305 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:ai-guidelines:832d8d96-080d-4d14-bcc6-80a23ffafa0e
2026-01-30 12:07:57,310 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:guidelines:832d8d96-080d-4d14-bcc6-80a23ffafa0e
2026-01-30 12:07:57,312 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/832d8d96-080d-4d14-bcc6-80a23ffafa0e/ai-guidelines
2026-01-30 12:07:57,315 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:832d8d96-080d-4d14-bcc6-80a23ffafa0e
2026-01-30 12:07:57,316 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/832d8d96-080d-4d14-bcc6-80a23ffafa0e/guidelines
INFO:     127.0.0.1:54195 - "GET /api/v1/worldview/works/832d8d96-080d-4d14-bcc6-80a23ffafa0e/ai-guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:54194 - "GET /api/v1/worldview/works/832d8d96-080d-4d14-bcc6-80a23ffafa0e/guidelines HTTP/1.1" 200 OK
2026-01-30 12:07:57,319 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/07352d22-b4c9-4aa0-90ab-2408baca9e29
INFO:     127.0.0.1:50231 - "PUT /api/v1/chapters/07352d22-b4c9-4aa0-90ab-2408baca9e29 HTTP/1.1" 200 OK
2026-01-30 12:07:57,384 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-30 12:07:57,388 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:characters:832d8d96-080d-4d14-bcc6-80a23ffafa0e (expire=300s)
2026-01-30 12:07:58,438 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/832d8d96-080d-4d14-bcc6-80a23ffafa0e/characters
INFO:     127.0.0.1:54095 - "GET /api/v1/worldview/works/832d8d96-080d-4d14-bcc6-80a23ffafa0e/characters HTTP/1.1" 200 OK
2026-01-30 12:07:58,467 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 07352d22-b4c9-4aa0-90ab-2408baca9e29 内容更新，新段落数: 88
2026-01-30 12:07:58,497 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:832d8d96-080d-4d14-bcc6-80a23ffafa0e
2026-01-30 12:07:58,499 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/07352d22-b4c9-4aa0-90ab-2408baca9e29
INFO:     127.0.0.1:54975 - "PUT /api/v1/chapters/07352d22-b4c9-4aa0-90ab-2408baca9e29 HTTP/1.1" 200 OK
2026-01-30 12:07:58,502 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
2026-01-30 12:07:58,583 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-30 12:07:59,660 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-30 12:07:59,682 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 07352d22-b4c9-4aa0-90ab-2408baca9e29 内容更新，新段落数: 88
2026-01-30 12:07:59,691 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
2026-01-30 12:08:00,842 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 07352d22-b4c9-4aa0-90ab-2408baca9e29 内容更新，新段落数: 88
2026-01-30 12:08:00,858 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:832d8d96-080d-4d14-bcc6-80a23ffafa0e
2026-01-30 12:08:00,861 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/07352d22-b4c9-4aa0-90ab-2408baca9e29
INFO:     127.0.0.1:57144 - "PUT /api/v1/chapters/07352d22-b4c9-4aa0-90ab-2408baca9e29 HTTP/1.1" 200 OK
2026-01-30 12:08:00,877 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:832d8d96-080d-4d14-bcc6-80a23ffafa0e
2026-01-30 12:08:00,879 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/07352d22-b4c9-4aa0-90ab-2408baca9e29
INFO:     127.0.0.1:57146 - "PUT /api/v1/chapters/07352d22-b4c9-4aa0-90ab-2408baca9e29 HTTP/1.1" 200 OK
2026-01-30 12:08:00,888 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
2026-01-30 12:08:05,045 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:characters:832d8d96-080d-4d14-bcc6-80a23ffafa0e (expire=300s)
2026-01-30 12:08:05,057 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/832d8d96-080d-4d14-bcc6-80a23ffafa0e/characters
INFO:     127.0.0.1:64327 - "GET /api/v1/worldview/works/832d8d96-080d-4d14-bcc6-80a23ffafa0e/characters HTTP/1.1" 200 OK
2026-01-30 12:08:05,091 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:guidelines:832d8d96-080d-4d14-bcc6-80a23ffafa0e
2026-01-30 12:08:05,097 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:settings:832d8d96-080d-4d14-bcc6-80a23ffafa0e (expire=300s)
2026-01-30 12:08:05,108 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:ai-guidelines:832d8d96-080d-4d14-bcc6-80a23ffafa0e
2026-01-30 12:08:05,109 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/832d8d96-080d-4d14-bcc6-80a23ffafa0e/guidelines
2026-01-30 12:08:05,118 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:locations:832d8d96-080d-4d14-bcc6-80a23ffafa0e (expire=300s)
2026-01-30 12:08:05,120 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/832d8d96-080d-4d14-bcc6-80a23ffafa0e/settings
INFO:     127.0.0.1:51079 - "GET /api/v1/worldview/works/832d8d96-080d-4d14-bcc6-80a23ffafa0e/guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:63070 - "GET /api/v1/worldview/works/832d8d96-080d-4d14-bcc6-80a23ffafa0e/settings HTTP/1.1" 200 OK
2026-01-30 12:08:05,126 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/832d8d96-080d-4d14-bcc6-80a23ffafa0e/ai-guidelines
2026-01-30 12:08:05,128 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/832d8d96-080d-4d14-bcc6-80a23ffafa0e/locations
INFO:     127.0.0.1:51081 - "GET /api/v1/worldview/works/832d8d96-080d-4d14-bcc6-80a23ffafa0e/ai-guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:51078 - "GET /api/v1/worldview/works/832d8d96-080d-4d14-bcc6-80a23ffafa0e/locations HTTP/1.1" 200 OK
2026-01-30 12:08:17,290 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:51010 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2026-01-30 12:08:17,317 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:ai-guidelines:832d8d96-080d-4d14-bcc6-80a23ffafa0e
2026-01-30 12:08:17,326 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:guidelines:832d8d96-080d-4d14-bcc6-80a23ffafa0e
2026-01-30 12:08:17,345 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:characters:832d8d96-080d-4d14-bcc6-80a23ffafa0e (expire=300s)
2026-01-30 12:08:17,348 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/832d8d96-080d-4d14-bcc6-80a23ffafa0e/ai-guidelines
2026-01-30 12:08:17,349 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/832d8d96-080d-4d14-bcc6-80a23ffafa0e/guidelines
2026-01-30 12:08:17,353 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:settings:832d8d96-080d-4d14-bcc6-80a23ffafa0e (expire=300s)
2026-01-30 12:08:17,355 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:locations:832d8d96-080d-4d14-bcc6-80a23ffafa0e (expire=300s)
INFO:     127.0.0.1:56480 - "GET /api/v1/worldview/works/832d8d96-080d-4d14-bcc6-80a23ffafa0e/ai-guidelines HTTP/1.1" 200 OK
2026-01-30 12:08:17,360 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/832d8d96-080d-4d14-bcc6-80a23ffafa0e/characters
INFO:     127.0.0.1:56479 - "GET /api/v1/worldview/works/832d8d96-080d-4d14-bcc6-80a23ffafa0e/guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:56474 - "GET /api/v1/worldview/works/832d8d96-080d-4d14-bcc6-80a23ffafa0e/characters HTTP/1.1" 200 OK
2026-01-30 12:08:17,370 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/832d8d96-080d-4d14-bcc6-80a23ffafa0e/settings
2026-01-30 12:08:17,372 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/832d8d96-080d-4d14-bcc6-80a23ffafa0e/locations
INFO:     127.0.0.1:56478 - "GET /api/v1/worldview/works/832d8d96-080d-4d14-bcc6-80a23ffafa0e/settings HTTP/1.1" 200 OK
INFO:     127.0.0.1:56477 - "GET /api/v1/worldview/works/832d8d96-080d-4d14-bcc6-80a23ffafa0e/locations HTTP/1.1" 200 OK
2026-01-30 12:08:17,382 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-30 12:08:17,382 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-30 12:08:17,383 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2026-01-30 12:08:19,165 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz:8443/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-30 12:08:19,167 - app.api.v1.agent - INFO - [Chat Stream] Mode: planning
2026-01-30 12:08:19,175 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:49172 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2026-01-30 12:08:19,188 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 仅限第1–3章。请找出所有包含“器灵/吞噬/器物/等阶/吞噬要求/吞噬效果”的段落，必须逐条读取原文...
2026-01-30 12:08:19,191 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-30 12:08:19,191 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-30 12:08:19,193 - app.services.ai.http_ai_service - INFO - [成本追踪] 初始化未传db/user_id，将使用请求上下文按需记录成本
2026-01-30 12:08:20,844 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz:8443/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-30 12:08:20,844 - app.services.agent.tools.writing_tools - INFO - Writing tools AI service initialized
2026-01-30 12:08:20,844 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ AI Service 已同时设置到 langgraph_tools 和 writing_tools
2026-01-30 12:08:20,844 - app.services.context.adaptive_budget - INFO - ✅ 所有预算配置验证通过
2026-01-30 12:08:27,854 - app.services.context.vector_memory_store - INFO - ✅ VectorMemoryStore初始化成功 | 目录=./data/chroma_db | 模型=paraphrase-multilingual-MiniLM-L12-v2 | 集合=user_memories
2026-01-30 12:08:27,859 - app.services.context.manager - INFO - ✅ VectorMemoryStore 已初始化
2026-01-30 12:08:27,859 - app.services.context.manager - INFO - ✅ ContextManager: 长期记忆已启用 (user_id=None)
2026-01-30 12:08:27,859 - app.services.context.manager - INFO - ✅ ContextManager: 自适应预算已启用
2026-01-30 12:08:27,859 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ ContextManager已初始化（长期记忆已启用，自适应预算已启用，总预算=16000 tokens）
成功加载模板: analyze_text (版本 3.1.0)
成功加载模板: writing_agent (版本 2.0.0)
成功加载模板: system_agent_prompt (版本 2.1.0)
成功加载模板: creative_writing_prompt (版本 1.0.0)
2026-01-30 12:08:27,911 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ PromptManager已初始化
2026-01-30 12:08:27,917 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ Redis连接验证成功
2026-01-30 12:08:27,917 - app.services.agent.langgraph_agent - INFO - [LangGraph] OK 使用 AsyncRedisSaver（redis://localhost:6379/0，TTL=7天）
2026-01-30 12:08:27,921 - app.services.agent.memory.metrics - INFO - [MemoryMetrics] 监控系统已初始化
2026-01-30 12:08:27,921 - app.services.agent.memory.long_term_store - INFO - [LongTermStore] Initialized: base_dir=./data/long_term_memory, max_size=50KB, compression=True
2026-01-30 12:08:27,921 - app.services.agent.memory.enhanced_memory_manager - INFO - EnhancedMemoryManager initialized: short=10, medium=100, threshold=0.1, long_term_backup=enabled
2026-01-30 12:08:27,921 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ EnhancedMemoryManager已创建
2026-01-30 12:08:27,921 - app.services.agent.memory.unified_coordinator - INFO - [UnifiedMemoryCoordinator] 初始化统一记忆协调器
2026-01-30 12:08:27,925 - app.services.agent.memory.unified_coordinator - INFO - [UnifiedMemoryCoordinator] 全局实例已设置
2026-01-30 12:08:27,925 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ UnifiedMemoryCoordinator已初始化 | checkpointer=AsyncRedisSaver | enhanced_memory=yes | context_manager=yes
2026-01-30 12:08:27,925 - app.services.agent.langgraph_agent - INFO - [LangGraph] ✅ 解耦模块已初始化 (IntentClassifier, ToolExecutor, EventParser, ResponseBuilder, ToolDispatcher, ParallelExecutor, PlanGenerator, QuickPathHandler, StreamEventHandler, SecondaryToolHandler, TaskRunner, AgentExecutor)
2026-01-30 12:08:27,936 - app.services.agent.parallel_tool_node - INFO - [ParallelToolNode] 初始化完成，最大并发数=5，并行安全工具=6个
2026-01-30 12:08:28,100 - app.api.v1.agent - INFO - [Global Agent] created global agent instance; MemorySaver shared across requests
2026-01-30 12:08:28,110 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-30 12:08:28,127 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:832d8d96-080d-4d14-bcc6-80a23ffafa0e:2edba307-74c5-40ab-aa48-84396f47c759 (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=832d8d96-080d-4d14-bcc6-80a23ffafa0e, conversation_id=2edba307-74c5-40ab-aa48-84396f47c759)
2026-01-30 12:08:28,128 - app.services.context.monitoring_integration - INFO - ✅ ContextManager监控收集器已初始化
2026-01-30 12:08:28,128 - app.services.context.store - INFO - [ContextStore] Redis连接成功
2026-01-30 12:08:28,134 - app.services.context.manager - INFO - [ContextManager] 创建新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:832d8d96-080d-4d14-bcc6-80a23ffafa0e:2edba307-74c5-40ab-aa48-84396f47c759
2026-01-30 12:08:28,442 - app.services.context.token_counter - INFO - ✅ tiktoken初始化成功，模型: gemini-2.5-pro -> cl100k_base
2026-01-30 12:08:28,442 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:832d8d96-080d-4d14-bcc6-80a23ffafa0e:2edba307-74c5-40ab-aa48-84396f47c759: 0/16000 tokens
2026-01-30 12:08:30,166 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='仅限第1–3章。请找出所有包含“器灵/吞噬/器物/等阶/吞噬...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:832d8d96-080d-4d14-bcc6-80a23ffafa0e', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=0条
2026-01-30 12:08:30,166 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=832d8d96-080d-4d14-bcc6-80a23ffafa0e | 含用户级=True | 找到=0条
2026-01-30 12:08:30,247 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 0条消息, 0 tokens, 耗时 2119.08ms
2026-01-30 12:08:30,251 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-30 12:08:30,253 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-30 12:08:30,255 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=20, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-30 12:08:31,738 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:08:31,738 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-30 12:08:31,798 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:08:31,798 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=408, cost=$0.000041, time=1484ms
2026-01-30 12:08:31,798 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=8, 尝试次数=1
2026-01-30 12:08:31,798 - app.services.agent.intent.classifier - INFO - [Intent] AI识别结果: analysis
2026-01-30 12:08:31,798 - app.services.agent.langgraph_agent - INFO - [Planning] AI意图分类: analysis (置信度: 0.90)
2026-01-30 12:08:31,798 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 仅限第1–3章。请找出所有包含“器灵/吞噬/器物/等阶/吞噬要求/吞噬效果”的段落，必须逐条读取原文...
2026-01-30 12:08:31,806 - app.core.cache - INFO - ⚠️ 缓存未命中: prompt:planning:v2.41.0:get_planning_static_prompt:fca6eb91156619d0
2026-01-30 12:08:31,812 - app.core.cache - INFO - 💾 缓存已保存: prompt:planning:v2.41.0:get_planning_static_prompt:fca6eb91156619d0 (expire=3600s)
2026-01-30 12:08:31,819 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-30 12:08:31,819 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=story_planning, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: story_planning; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-01-30 12:08:31,819 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.3, task_type=TaskType.STORY_PLANNING
2026-01-30 12:08:42,441 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:guidelines:832d8d96-080d-4d14-bcc6-80a23ffafa0e
2026-01-30 12:08:42,446 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:ai-guidelines:832d8d96-080d-4d14-bcc6-80a23ffafa0e
2026-01-30 12:08:42,457 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:settings:832d8d96-080d-4d14-bcc6-80a23ffafa0e (expire=300s)
2026-01-30 12:08:42,461 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/832d8d96-080d-4d14-bcc6-80a23ffafa0e/guidelines
2026-01-30 12:08:42,463 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/832d8d96-080d-4d14-bcc6-80a23ffafa0e/ai-guidelines
2026-01-30 12:08:42,464 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/832d8d96-080d-4d14-bcc6-80a23ffafa0e/settings
2026-01-30 12:08:42,470 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:characters:832d8d96-080d-4d14-bcc6-80a23ffafa0e (expire=300s)
2026-01-30 12:08:42,477 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:locations:832d8d96-080d-4d14-bcc6-80a23ffafa0e (expire=300s)
INFO:     127.0.0.1:62515 - "GET /api/v1/worldview/works/832d8d96-080d-4d14-bcc6-80a23ffafa0e/guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:62516 - "GET /api/v1/worldview/works/832d8d96-080d-4d14-bcc6-80a23ffafa0e/ai-guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:62514 - "GET /api/v1/worldview/works/832d8d96-080d-4d14-bcc6-80a23ffafa0e/settings HTTP/1.1" 200 OK
2026-01-30 12:08:42,491 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/832d8d96-080d-4d14-bcc6-80a23ffafa0e/locations
2026-01-30 12:08:42,491 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/832d8d96-080d-4d14-bcc6-80a23ffafa0e/characters
INFO:     127.0.0.1:62513 - "GET /api/v1/worldview/works/832d8d96-080d-4d14-bcc6-80a23ffafa0e/locations HTTP/1.1" 200 OK
INFO:     127.0.0.1:62512 - "GET /api/v1/worldview/works/832d8d96-080d-4d14-bcc6-80a23ffafa0e/characters HTTP/1.1" 200 OK
2026-01-30 12:08:44,550 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-30 12:08:46,682 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 33 个数据块，总长度: 4121
2026-01-30 12:08:46,687 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 15759 (prompt=13689, completion=2070)
2026-01-30 12:08:46,689 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 实例, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:08:46,690 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-30 12:08:46,708 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:08:46,708 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:实例): tokens=15759, cost=$0.037811, time=50569ms
2026-01-30 12:08:46,708 - app.services.worldview_sync_service - INFO - [世界观同步] AI响应长度: 4121
2026-01-30 12:08:46,714 - app.services.worldview_sync_service - INFO - [世界观同步] AI响应内容: 好的，作为专业的小说世界观分析师，我已经综合分析了您提供的五个章节。由于【现有世界观】为空，以下所有内容均为本次分析的新增发现。

```json
{
  "new_characters": [
    {
      "name": "段融",
      "role": "主角",
      "description": "魂穿者，性格现实、功利。拥有吞噬器灵获得技能和经验的独特能力。为了在残酷的世界中生存和变强，他行事果断，善于投资自身。目前是源顺镖局的杂役弟子，目标是通过考核成为学徒。",
      "first_appearance": "第1章",
      "importance": "高"
    },
    {
      "name": "杨震",
      "role": "配角",
      "description": "主角段融的发小，在县衙担任捕快，为人热情，有些爱显摆。因二叔在生药铺当账房而有些门路，是主角在世界上为数不多的熟人。他无意中为主角提供了关于太一门和逃犯许儒虎的重要情报。",
      "first_appearance": "...
2026-01-30 12:08:46,714 - app.services.worldview_sync_service - INFO - [世界观同步] 解析结果: 新人物=9, 新地点=6, 新设定=5
2026-01-30 12:08:46,714 - app.api.v1.import_routes - INFO - [世界观提取] 扫描完成: 5章, 发现 9人物, 6地点, 5设定
2026-01-30 12:08:46,758 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 段融
2026-01-30 12:08:46,780 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 杨震
2026-01-30 12:08:46,790 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 赵穆
2026-01-30 12:08:46,803 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 许儒虎
2026-01-30 12:08:46,818 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 孔斌
2026-01-30 12:08:46,834 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 李充
2026-01-30 12:08:46,850 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 张征
2026-01-30 12:08:46,864 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 孙老头
2026-01-30 12:08:46,872 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 解捕头
2026-01-30 12:08:46,898 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 太一门
2026-01-30 12:08:46,918 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 源顺镖局
2026-01-30 12:08:46,930 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 青州
2026-01-30 12:08:46,944 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 贤古县
2026-01-30 12:08:46,969 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 九州大陆
2026-01-30 12:08:46,980 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 县衙
2026-01-30 12:08:47,008 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 吞噬器灵
2026-01-30 12:08:47,025 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 器灵
2026-01-30 12:08:47,044 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 世界构架：宗门统治
2026-01-30 12:08:47,058 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 武学修炼体系
2026-01-30 12:08:47,078 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 镖局晋升体系
2026-01-30 12:08:47,099 - app.services.worldview_sync_service - INFO - [世界观同步] 创建关系: 段融 -> 杨震: 发小/朋友
2026-01-30 12:08:47,108 - app.services.worldview_sync_service - INFO - [世界观同步] 创建关系: 段融 -> 赵穆: 临时的指导者与被指导者（有轻微冲突）
2026-01-30 12:08:47,110 - app.services.worldview_sync_service - INFO - [世界观同步] 创建关系: 段融 -> 孔斌: 同门/竞争对手
2026-01-30 12:08:47,110 - app.services.worldview_sync_service - INFO - [世界观同步] 创建关系: 杨震 -> 解捕头: 被赏识的下属与上司
2026-01-30 12:08:47,130 - app.services.worldview_sync_service - INFO - [Worldview Sync] Cache invalidated: worldview:characters:832d8d96-080d-4d14-bcc6-80a23ffafa0e
2026-01-30 12:08:47,134 - app.services.worldview_sync_service - INFO - [Worldview Sync] Cache invalidated: worldview:locations:832d8d96-080d-4d14-bcc6-80a23ffafa0e
2026-01-30 12:08:47,136 - app.services.worldview_sync_service - INFO - [Worldview Sync] Cache invalidated: worldview:settings:832d8d96-080d-4d14-bcc6-80a23ffafa0e
2026-01-30 12:08:47,139 - app.services.worldview_sync_service - INFO - [Worldview Sync] Cache invalidated: worldview:guidelines:832d8d96-080d-4d14-bcc6-80a23ffafa0e
2026-01-30 12:08:47,142 - app.services.worldview_sync_service - INFO - [Worldview Sync] Cache invalidated: worldview:worlddata:832d8d96-080d-4d14-bcc6-80a23ffafa0e
2026-01-30 12:08:47,142 - app.api.v1.import_routes - INFO - [世界观提取] 应用完成: {'characters_created': 9, 'characters_updated': 0, 'locations_created': 6, 'settings_created': 5, 'relationships_created': 4}
2026-01-30 12:08:48,465 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 8 个数据块，总长度: 1003
2026-01-30 12:08:48,466 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 21977 (prompt=21480, completion=497)
2026-01-30 12:08:48,467 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:08:48,467 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-30 12:08:48,500 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:08:48,504 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=21977, cost=$0.031820, time=16648ms
2026-01-30 12:08:48,504 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=21977
2026-01-30 12:08:48,504 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户需要一个表格，其中包含第1-3章中所有提及特定关键词（器, 原料=需要读取并检索第1章、第2章和第3章的全, 处理=使用 `explore_content`
2026-01-30 12:08:48,537 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共1个任务
2026-01-30 12:08:48,537 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共1个任务，耗时: 16.74s
2026-01-30 12:08:48,537 - app.api.v1.agent - INFO - [Stream] Plan tasks: 1 items
2026-01-30 12:08:48,537 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2026-01-30 12:08:48,537 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2026-01-30 12:08:48,537 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2026-01-30 12:08:48,537 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] DAG 调度启用，任务数=1, 有依赖任务=0
2026-01-30 12:08:48,542 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1开始: 在第1章至第3章范围内，找出所有包含关键词“器灵”、“吞噬”、“器物”、“等阶”、“吞噬要求”、“吞噬效果”的段落原文。
2026-01-30 12:08:48,542 - app.api.v1.agent - INFO - [Stream] Task started: 在第1章至第3章范围内，找出所有包含关键词“器灵”、“吞噬”、“器物”、“等阶”、“吞噬要求”、“吞噬效果”的段落原文。 (icon=Wrench)
2026-01-30 12:08:48,542 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: explore_content
2026-01-30 12:08:48,542 - app.services.agent.tools.explore_tools - INFO - [explore_content] 开始: work_id=832d8d96-080d-4d14-bcc6-80a23ffafa0e, target=在第1章至第3章范围内，找出所有包含关键词“器灵”、“吞噬”、“器物”、“等阶”、“吞噬要求”、“吞...
2026-01-30 12:08:48,542 - app.services.agent.tools.explore_tools - INFO - [explore_content] 规划传入关键词: ['器灵', '吞噬', '器物', '等阶', '吞噬要求', '吞噬效果']
2026-01-30 12:08:48,549 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 启用严格段落号模式
2026-01-30 12:08:48,549 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 章节范围锁定: 第1-3章
2026-01-30 12:08:48,549 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 任务禁止整章阅读
2026-01-30 12:08:48,549 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 开始探索 V5: work_id=832d8d96-080d-4d14-bcc6-80a23ffafa0e, target=在第1章至第3章范围内，找出所有包含关键词“器灵”、“吞噬”、“器物”、“等阶”、“吞噬要求”、“吞...
2026-01-30 12:08:48,549 - app.services.chapter_service - INFO - [ChapterService] Querying chapters for work_id=832d8d96-080d-4d14-bcc6-80a23ffafa0e, type=<class 'uuid.UUID'>
2026-01-30 12:08:48,561 - app.services.chapter_service - INFO - [ChapterService] Found 5 chapters
2026-01-30 12:08:48,561 - app.services.chapter_service - INFO -   - Chapter: 第1章 吞噬, order=1
2026-01-30 12:08:48,561 - app.services.chapter_service - INFO -   - ... (3 more chapters)
2026-01-30 12:08:48,561 - app.services.chapter_service - INFO -   - Chapter: 第5章 太一门, order=5
2026-01-30 12:08:48,604 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 章节范围映射: 第1-3章 -> 第1-3章
2026-01-30 12:08:48,616 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 自动获取世界观...
2026-01-30 12:08:48,627 - app.services.agent.langgraph_tools - INFO - [get_writing_context] ✅ 获取创作上下文成功: include=worldview
2026-01-30 12:08:48,627 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 世界观获取完成: 20 条
2026-01-30 12:08:48,627 - app.services.ai.http_ai_service - INFO - [成本追踪] 初始化未传db/user_id，将使用请求上下文按需记录成本
2026-01-30 12:08:50,158 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz:8443/v1, Model: gemini-2.5-flash, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: False, CostTracking: True
2026-01-30 12:08:50,158 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:08:50,158 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=80, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:08:52,578 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:08:52,578 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:08:52,615 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:08:52,615 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=247, cost=$0.000090, time=2420ms
2026-01-30 12:08:52,615 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=11, 尝试次数=1
2026-01-30 12:08:52,615 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 强制流程步骤: list_chapters
2026-01-30 12:08:52,615 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=list_chapters params={"work_id": "832d8d96-080d-4d14-bcc6-80a23ffafa0e"}
2026-01-30 12:08:52,615 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=list_chapters success=True count=3
2026-01-30 12:08:52,620 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:08:52,620 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=80, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:08:56,963 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:08:56,965 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:08:56,984 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:08:56,986 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=779, cost=$0.000256, time=4345ms
2026-01-30 12:08:56,988 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=16, 尝试次数=1
2026-01-30 12:08:56,988 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 强制流程步骤: list_paragraphs
2026-01-30 12:08:56,988 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=list_paragraphs params={"chapter_order": 1, "offset": 0, "limit": 50, "preview_len": 80, "work_id": "832d8d96-080d-4d14-bcc6-80a23ffafa0e"}
2026-01-30 12:08:57,003 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=list_paragraphs success=True chapter=1 offset=0 limit=50 approximate=None
2026-01-30 12:08:57,003 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:08:57,003 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:09:00,331 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:09:00,332 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:09:00,351 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:09:00,352 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1788, cost=$0.000899, time=3328ms
2026-01-30 12:09:00,353 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=353, 尝试次数=1
2026-01-30 12:09:00,353 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"keywords": ["器灵", "吞噬", "器物", "等阶", "吞噬要求", "吞噬效果"], "match_mode": "any", "limit": 100, "work_id": "832d8d96-080d-4d14-bcc6-80a23ffafa0e"}
2026-01-30 12:09:00,354 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 世界观匹配: 4 条
2026-01-30 12:09:00,397 - app.services.chapter_vector_service - INFO - [exact_search] work=832d8d96-080d-4d14-bcc6-80a23ffafa0e, keywords=['器灵', '吞噬', '器物']..., mode=any, range=(1, 3), hits=43
2026-01-30 12:09:00,405 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=33 corrected=False final=33
2026-01-30 12:09:00,406 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第33段
2026-01-30 12:09:00,413 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=35 corrected=False final=35
2026-01-30 12:09:00,414 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第35段
2026-01-30 12:09:00,417 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=36 corrected=False final=36
2026-01-30 12:09:00,421 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第36段
2026-01-30 12:09:00,426 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=37 corrected=False final=37
2026-01-30 12:09:00,426 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第37段
2026-01-30 12:09:00,434 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=38 corrected=False final=38
2026-01-30 12:09:00,434 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第38段
2026-01-30 12:09:00,443 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=39 corrected=False final=39
2026-01-30 12:09:00,443 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第39段
2026-01-30 12:09:00,450 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=41 corrected=False final=41
2026-01-30 12:09:00,450 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第41段
2026-01-30 12:09:00,459 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=42 corrected=False final=42
2026-01-30 12:09:00,459 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第42段
2026-01-30 12:09:00,468 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=69 corrected=False final=69
2026-01-30 12:09:00,468 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第69段
2026-01-30 12:09:00,475 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=70 corrected=False final=70
2026-01-30 12:09:00,475 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第70段
2026-01-30 12:09:00,484 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=72 corrected=False final=72
2026-01-30 12:09:00,485 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第72段
2026-01-30 12:09:00,492 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=73 corrected=False final=73
2026-01-30 12:09:00,492 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第73段
2026-01-30 12:09:00,501 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=74 corrected=False final=74
2026-01-30 12:09:00,501 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第74段
2026-01-30 12:09:00,512 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=75 corrected=False final=75
2026-01-30 12:09:00,522 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第75段
2026-01-30 12:09:00,528 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=76 corrected=False final=76
2026-01-30 12:09:00,534 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第76段
2026-01-30 12:09:00,543 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=78 corrected=False final=78
2026-01-30 12:09:00,544 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第78段
2026-01-30 12:09:00,551 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=79 corrected=False final=79
2026-01-30 12:09:00,552 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第79段
2026-01-30 12:09:00,559 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=81 corrected=False final=81
2026-01-30 12:09:00,559 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第81段
2026-01-30 12:09:00,567 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=17 corrected=False final=17
2026-01-30 12:09:00,570 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第17段
2026-01-30 12:09:00,572 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=26 (chapter=22, worldview=4) keywords=器灵,吞噬,器物,等阶,吞噬要求,吞噬效果
2026-01-30 12:09:00,572 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:09:00,572 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:09:07,881 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:09:07,881 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:09:07,900 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:09:07,900 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4760, cost=$0.001776, time=7311ms
2026-01-30 12:09:07,900 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=388, 尝试次数=1
2026-01-30 12:09:07,900 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=read_paragraphs params={"items": [{"chapter_order": 1, "paragraph_index": 82}, {"chapter_order": 1, "paragraph_index": 83}, {"chapter_order": 1, "paragraph_index": 87}], "work_id": "832d8d96-080d-4d14-bcc6-80a23ffafa0e"}
2026-01-30 12:09:07,900 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=read_paragraphs success=False count=0 index_base=None
2026-01-30 12:09:07,900 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:09:07,905 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:09:12,823 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:09:12,826 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:09:12,843 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:09:12,848 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4195, cost=$0.001562, time=4920ms
2026-01-30 12:09:12,848 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=285, 尝试次数=1
2026-01-30 12:09:12,848 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"keywords": ["等阶", "吞噬要求", "吞噬效果"], "match_mode": "any", "limit": 100, "chapter_range": "1-3", "work_id": "832d8d96-080d-4d14-bcc6-80a23ffafa0e"}
2026-01-30 12:09:12,848 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 世界观匹配: 2 条
2026-01-30 12:09:12,897 - app.services.chapter_vector_service - INFO - [exact_search] work=832d8d96-080d-4d14-bcc6-80a23ffafa0e, keywords=['等阶', '吞噬要求', '吞噬效果']..., mode=any, range=(1, 3), hits=20
2026-01-30 12:09:12,901 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=12 (chapter=10, worldview=2) keywords=等阶,吞噬要求,吞噬效果
2026-01-30 12:09:12,901 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:09:12,901 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:09:26,621 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:09:26,621 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:09:26,643 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:09:26,645 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=6493, cost=$0.002285, time=13722ms
2026-01-30 12:09:26,645 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=374, 尝试次数=1
2026-01-30 12:09:26,645 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=read_paragraphs params={"items": [{"chapter_order": 1, "paragraph_index": 82}, {"chapter_order": 1, "paragraph_index": 83}, {"chapter_order": 1, "paragraph_index": 87}], "work_id": "832d8d96-080d-4d14-bcc6-80a23ffafa0e"}
2026-01-30 12:09:26,645 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=read_paragraphs success=False count=0 index_base=None
2026-01-30 12:09:26,645 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:09:26,645 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:09:27,556 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:characters:832d8d96-080d-4d14-bcc6-80a23ffafa0e (expire=300s)
2026-01-30 12:09:27,567 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/832d8d96-080d-4d14-bcc6-80a23ffafa0e/characters
INFO:     127.0.0.1:53363 - "GET /api/v1/worldview/works/832d8d96-080d-4d14-bcc6-80a23ffafa0e/characters HTTP/1.1" 200 OK
2026-01-30 12:09:27,591 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:locations:832d8d96-080d-4d14-bcc6-80a23ffafa0e (expire=300s)
2026-01-30 12:09:27,604 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:ai-guidelines:832d8d96-080d-4d14-bcc6-80a23ffafa0e
2026-01-30 12:09:27,618 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/832d8d96-080d-4d14-bcc6-80a23ffafa0e/locations
2026-01-30 12:09:27,623 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:settings:832d8d96-080d-4d14-bcc6-80a23ffafa0e (expire=300s)
2026-01-30 12:09:27,627 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/832d8d96-080d-4d14-bcc6-80a23ffafa0e/ai-guidelines
INFO:     127.0.0.1:53364 - "GET /api/v1/worldview/works/832d8d96-080d-4d14-bcc6-80a23ffafa0e/locations HTTP/1.1" 200 OK
INFO:     127.0.0.1:53370 - "GET /api/v1/worldview/works/832d8d96-080d-4d14-bcc6-80a23ffafa0e/ai-guidelines HTTP/1.1" 200 OK
2026-01-30 12:09:27,640 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:guidelines:832d8d96-080d-4d14-bcc6-80a23ffafa0e (expire=300s)
2026-01-30 12:09:27,642 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/832d8d96-080d-4d14-bcc6-80a23ffafa0e/settings
INFO:     127.0.0.1:53367 - "GET /api/v1/worldview/works/832d8d96-080d-4d14-bcc6-80a23ffafa0e/settings HTTP/1.1" 200 OK
2026-01-30 12:09:27,649 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/832d8d96-080d-4d14-bcc6-80a23ffafa0e/guidelines
INFO:     127.0.0.1:53368 - "GET /api/v1/worldview/works/832d8d96-080d-4d14-bcc6-80a23ffafa0e/guidelines HTTP/1.1" 200 OK
2026-01-30 12:09:54,350 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:09:54,351 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:09:54,367 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:09:54,367 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=8521, cost=$0.002891, time=27705ms
2026-01-30 12:09:54,367 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=378, 尝试次数=1
2026-01-30 12:09:54,370 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=read_paragraphs params={"items": [{"chapter_order": 1, "paragraph_index": 82}, {"chapter_order": 1, "paragraph_index": 83}, {"chapter_order": 1, "paragraph_index": 87}], "work_id": "832d8d96-080d-4d14-bcc6-80a23ffafa0e"}
2026-01-30 12:09:54,370 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=read_paragraphs success=False count=0 index_base=None
2026-01-30 12:09:54,370 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:09:54,370 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:09:58,515 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:09:58,517 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:09:58,544 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:09:58,545 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=3963, cost=$0.001506, time=4148ms
2026-01-30 12:09:58,545 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=306, 尝试次数=1
2026-01-30 12:09:58,545 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"keywords": ["等阶", "吞噬要求", "吞噬效果"], "match_mode": "any", "limit": 100, "chapter_orders": [2, 3], "work_id": "832d8d96-080d-4d14-bcc6-80a23ffafa0e"}
2026-01-30 12:09:58,545 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 世界观匹配: 2 条
2026-01-30 12:09:58,586 - app.services.chapter_vector_service - INFO - [exact_search] work=832d8d96-080d-4d14-bcc6-80a23ffafa0e, keywords=['等阶', '吞噬要求', '吞噬效果']..., mode=any, range=(1, 3), hits=20
2026-01-30 12:09:58,586 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=12 (chapter=10, worldview=2) keywords=等阶,吞噬要求,吞噬效果
2026-01-30 12:09:58,586 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:09:58,586 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:10:15,109 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:10:15,109 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:10:15,136 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:10:15,136 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=7197, cost=$0.002505, time=16523ms
2026-01-30 12:10:15,136 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=380, 尝试次数=1
2026-01-30 12:10:15,136 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=read_paragraphs params={"items": [{"chapter_order": 1, "paragraph_index": 82}, {"chapter_order": 1, "paragraph_index": 83}, {"chapter_order": 1, "paragraph_index": 87}], "work_id": "832d8d96-080d-4d14-bcc6-80a23ffafa0e"}
2026-01-30 12:10:15,136 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=read_paragraphs success=False count=0 index_base=None
2026-01-30 12:10:15,147 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:10:15,147 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:10:28,714 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:10:28,715 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:10:28,746 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:10:28,747 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=6199, cost=$0.002185, time=13569ms
2026-01-30 12:10:28,748 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=372, 尝试次数=1
2026-01-30 12:10:28,748 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=read_paragraphs params={"items": [{"chapter_order": 1, "paragraph_index": 82}, {"chapter_order": 1, "paragraph_index": 83}, {"chapter_order": 1, "paragraph_index": 87}], "work_id": "832d8d96-080d-4d14-bcc6-80a23ffafa0e"}
2026-01-30 12:10:28,749 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=read_paragraphs success=False count=0 index_base=None
2026-01-30 12:10:28,751 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:10:28,753 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:10:35,191 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:10:35,192 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:10:35,209 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:10:35,213 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4373, cost=$0.001622, time=6438ms
2026-01-30 12:10:35,214 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=314, 尝试次数=1
2026-01-30 12:10:35,215 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"keywords": ["器灵", "吞噬", "器物", "等阶", "吞噬要求", "吞噬效果"], "match_mode": "any", "chapter_orders": [2], "limit": 100, "work_id": "832d8d96-080d-4d14-bcc6-80a23ffafa0e"}
2026-01-30 12:10:35,215 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 世界观匹配: 4 条
2026-01-30 12:10:35,262 - app.services.chapter_vector_service - INFO - [exact_search] work=832d8d96-080d-4d14-bcc6-80a23ffafa0e, keywords=['器灵', '吞噬', '器物']..., mode=any, range=(1, 3), hits=43
2026-01-30 12:10:35,263 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=26 (chapter=22, worldview=4) keywords=器灵,吞噬,器物,等阶,吞噬要求,吞噬效果
2026-01-30 12:10:35,265 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:10:35,265 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:10:43,483 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:10:43,484 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:10:43,502 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:10:43,504 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=5937, cost=$0.002118, time=8218ms
2026-01-30 12:10:43,505 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=380, 尝试次数=1
2026-01-30 12:10:43,505 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=read_paragraphs params={"items": [{"chapter_order": 1, "paragraph_index": 82}, {"chapter_order": 1, "paragraph_index": 83}, {"chapter_order": 1, "paragraph_index": 87}], "work_id": "832d8d96-080d-4d14-bcc6-80a23ffafa0e"}
2026-01-30 12:10:43,506 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=read_paragraphs success=False count=0 index_base=None
2026-01-30 12:10:43,507 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:10:43,509 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:10:46,075 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:10:46,076 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:10:46,090 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:10:46,092 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=3848, cost=$0.001469, time=2568ms
2026-01-30 12:10:46,092 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=304, 尝试次数=1
2026-01-30 12:10:46,094 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"keywords": ["器灵", "吞噬", "器物", "等阶", "吞噬要求", "吞噬效果"], "match_mode": "any", "limit": 100, "chapter_range": "2-2", "work_id": "832d8d96-080d-4d14-bcc6-80a23ffafa0e"}
2026-01-30 12:10:46,095 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 世界观匹配: 4 条
2026-01-30 12:10:46,150 - app.services.chapter_vector_service - INFO - [exact_search] work=832d8d96-080d-4d14-bcc6-80a23ffafa0e, keywords=['器灵', '吞噬', '器物']..., mode=any, range=(1, 3), hits=43
2026-01-30 12:10:46,152 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=26 (chapter=22, worldview=4) keywords=器灵,吞噬,器物,等阶,吞噬要求,吞噬效果
2026-01-30 12:10:46,153 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:10:46,154 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:10:59,990 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:10:59,990 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:11:00,012 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:11:00,015 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=6640, cost=$0.002364, time=13836ms
2026-01-30 12:11:00,019 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=400, 尝试次数=1
2026-01-30 12:11:00,020 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=read_paragraphs params={"items": [{"chapter_order": 1, "paragraph_index": 82}, {"chapter_order": 1, "paragraph_index": 83}, {"chapter_order": 1, "paragraph_index": 87}], "work_id": "832d8d96-080d-4d14-bcc6-80a23ffafa0e"}
2026-01-30 12:11:00,023 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=read_paragraphs success=False count=0 index_base=None
2026-01-30 12:11:00,025 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:11:00,027 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:11:13,287 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:11:13,287 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:11:13,298 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:11:13,299 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=5776, cost=$0.002102, time=13259ms
2026-01-30 12:11:13,300 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=340, 尝试次数=1
2026-01-30 12:11:13,300 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"keywords": ["器灵", "吞噬", "器物", "等阶", "吞噬要求", "吞噬效果"], "match_mode": "any", "limit": 100, "work_id": "832d8d96-080d-4d14-bcc6-80a23ffafa0e"}
2026-01-30 12:11:13,301 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 世界观匹配: 4 条
2026-01-30 12:11:13,349 - app.services.chapter_vector_service - INFO - [exact_search] work=832d8d96-080d-4d14-bcc6-80a23ffafa0e, keywords=['器灵', '吞噬', '器物']..., mode=any, range=(1, 3), hits=43
2026-01-30 12:11:13,352 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=26 (chapter=22, worldview=4) keywords=器灵,吞噬,器物,等阶,吞噬要求,吞噬效果
2026-01-30 12:11:13,354 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:11:13,355 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:11:19,568 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:11:19,568 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:11:19,588 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:11:19,590 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=5211, cost=$0.001935, time=6214ms
2026-01-30 12:11:19,591 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=400, 尝试次数=1
2026-01-30 12:11:19,593 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=read_paragraphs params={"items": [{"chapter_order": 1, "paragraph_index": 82}, {"chapter_order": 1, "paragraph_index": 83}, {"chapter_order": 1, "paragraph_index": 87}], "work_id": "832d8d96-080d-4d14-bcc6-80a23ffafa0e"}
2026-01-30 12:11:19,593 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=read_paragraphs success=False count=0 index_base=None
2026-01-30 12:11:19,595 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:11:19,596 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:11:41,128 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:11:41,129 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:11:41,151 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:11:41,155 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=7541, cost=$0.002627, time=21534ms
2026-01-30 12:11:41,156 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=339, 尝试次数=1
2026-01-30 12:11:41,156 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"keywords": ["等阶", "吞噬要求", "吞噬效果"], "match_mode": "any", "limit": 100, "work_id": "832d8d96-080d-4d14-bcc6-80a23ffafa0e"}
2026-01-30 12:11:41,157 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 世界观匹配: 2 条
2026-01-30 12:11:41,182 - app.services.chapter_vector_service - INFO - [exact_search] work=832d8d96-080d-4d14-bcc6-80a23ffafa0e, keywords=['等阶', '吞噬要求', '吞噬效果']..., mode=any, range=(1, 3), hits=20
2026-01-30 12:11:41,185 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=12 (chapter=10, worldview=2) keywords=等阶,吞噬要求,吞噬效果
2026-01-30 12:11:41,187 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:11:41,187 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:11:58,772 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:11:58,773 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:11:58,796 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:11:58,797 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=7692, cost=$0.002653, time=17589ms
2026-01-30 12:11:58,798 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=385, 尝试次数=1
2026-01-30 12:11:58,798 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=read_paragraphs params={"items": [{"chapter_order": 1, "paragraph_index": 82}, {"chapter_order": 1, "paragraph_index": 83}, {"chapter_order": 1, "paragraph_index": 87}], "work_id": "832d8d96-080d-4d14-bcc6-80a23ffafa0e"}
2026-01-30 12:11:58,799 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=read_paragraphs success=False count=0 index_base=None
2026-01-30 12:11:58,800 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:11:58,800 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:12:07,711 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:12:07,711 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:12:07,725 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:12:07,728 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=5076, cost=$0.001846, time=8911ms
2026-01-30 12:12:07,729 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=300, 尝试次数=1
2026-01-30 12:12:07,730 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"keywords": ["等阶", "吞噬要求", "吞噬效果"], "match_mode": "any", "limit": 100, "work_id": "832d8d96-080d-4d14-bcc6-80a23ffafa0e"}
2026-01-30 12:12:07,731 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 世界观匹配: 2 条
2026-01-30 12:12:07,776 - app.services.chapter_vector_service - INFO - [exact_search] work=832d8d96-080d-4d14-bcc6-80a23ffafa0e, keywords=['等阶', '吞噬要求', '吞噬效果']..., mode=any, range=(1, 3), hits=20
2026-01-30 12:12:07,778 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=12 (chapter=10, worldview=2) keywords=等阶,吞噬要求,吞噬效果
2026-01-30 12:12:07,780 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:12:07,780 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:12:26,109 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:12:26,111 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:12:26,131 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:12:26,133 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=7111, cost=$0.002498, time=18333ms
2026-01-30 12:12:26,134 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=333, 尝试次数=1
2026-01-30 12:12:26,135 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"keywords": ["器灵", "吞噬", "器物", "等阶", "吞噬要求", "吞噬效果"], "match_mode": "any", "limit": 100, "work_id": "832d8d96-080d-4d14-bcc6-80a23ffafa0e"}
2026-01-30 12:12:26,139 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 世界观匹配: 4 条
2026-01-30 12:12:26,178 - app.services.chapter_vector_service - INFO - [exact_search] work=832d8d96-080d-4d14-bcc6-80a23ffafa0e, keywords=['器灵', '吞噬', '器物']..., mode=any, range=(1, 3), hits=43
2026-01-30 12:12:26,181 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=26 (chapter=22, worldview=4) keywords=器灵,吞噬,器物,等阶,吞噬要求,吞噬效果
2026-01-30 12:12:26,183 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:12:26,184 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:12:53,276 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:12:53,282 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:12:53,293 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:12:53,299 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=9329, cost=$0.003177, time=27098ms
2026-01-30 12:12:53,303 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=401, 尝试次数=1
2026-01-30 12:12:53,303 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=read_paragraphs params={"items": [{"chapter_order": 1, "paragraph_index": 82}, {"chapter_order": 1, "paragraph_index": 83}, {"chapter_order": 1, "paragraph_index": 87}], "work_id": "832d8d96-080d-4d14-bcc6-80a23ffafa0e"}
2026-01-30 12:12:53,305 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=read_paragraphs success=False count=0 index_base=None
2026-01-30 12:12:53,305 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:12:53,305 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:12:56,699 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:12:56,700 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:12:56,718 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:12:56,724 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4099, cost=$0.001538, time=3394ms
2026-01-30 12:12:56,725 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=302, 尝试次数=1
2026-01-30 12:12:56,726 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"keywords": ["器灵", "吞噬", "器物", "等阶", "吞噬要求", "吞噬效果"], "match_mode": "any", "limit": 100, "chapter_range": "2-2", "work_id": "832d8d96-080d-4d14-bcc6-80a23ffafa0e"}
2026-01-30 12:12:56,726 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 世界观匹配: 4 条
2026-01-30 12:12:56,785 - app.services.chapter_vector_service - INFO - [exact_search] work=832d8d96-080d-4d14-bcc6-80a23ffafa0e, keywords=['器灵', '吞噬', '器物']..., mode=any, range=(1, 3), hits=43
2026-01-30 12:12:56,791 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=26 (chapter=22, worldview=4) keywords=器灵,吞噬,器物,等阶,吞噬要求,吞噬效果
2026-01-30 12:12:56,793 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:12:56,793 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:13:03,257 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:13:03,258 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:13:03,268 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:13:03,268 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4943, cost=$0.001837, time=6465ms
2026-01-30 12:13:03,273 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=392, 尝试次数=1
2026-01-30 12:13:03,274 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=read_paragraphs params={"items": [{"chapter_order": 1, "paragraph_index": 82}, {"chapter_order": 1, "paragraph_index": 83}, {"chapter_order": 1, "paragraph_index": 87}], "work_id": "832d8d96-080d-4d14-bcc6-80a23ffafa0e"}
2026-01-30 12:13:03,274 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=read_paragraphs success=False count=0 index_base=None
2026-01-30 12:13:03,274 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:13:03,274 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:13:12,420 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:13:12,421 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:13:12,442 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:13:12,442 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=5049, cost=$0.001768, time=9147ms
2026-01-30 12:13:12,443 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=246, 尝试次数=1
2026-01-30 12:13:12,444 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"keywords": "等阶,吞噬要求,吞噬效果", "match_mode": "any", "chapter_order": 2, "limit": -1, "work_id": "832d8d96-080d-4d14-bcc6-80a23ffafa0e"}
2026-01-30 12:13:12,444 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 世界观匹配: 2 条
2026-01-30 12:13:12,493 - app.services.chapter_vector_service - ERROR - [exact_search] 精确搜索失败: (sqlalchemy.dialects.postgresql.asyncpg.Error) <class 'asyncpg.exceptions.InvalidRowCountInLimitClauseError'>: LIMIT后的值不能为负数
[SQL: SELECT novel_chapter_vectors.id, novel_chapter_vectors.work_id, novel_chapter_vectors.chapter_id, novel_chapter_vectors.chapter_order, novel_chapter_vectors.chapter_title, novel_chapter_vectors.chunk_index, novel_chapter_vectors.chunk_text, novel_chapter_vectors.node_id, novel_chapter_vectors.embedding, novel_chapter_vectors.created_at, novel_chapter_vectors.updated_at
FROM novel_chapter_vectors
WHERE novel_chapter_vectors.work_id = $1::UUID AND novel_chapter_vectors.chapter_order >= $2::INTEGER AND novel_chapter_vectors.chapter_order <= $3::INTEGER AND (novel_chapter_vectors.chunk_text ILIKE $4::VARCHAR OR novel_chapter_vectors.chunk_text ILIKE $5::VARCHAR OR novel_chapter_vectors.chunk_text ILIKE $6::VARCHAR) ORDER BY novel_chapter_vectors.chapter_order, novel_chapter_vectors.chunk_index
 LIMIT $7::INTEGER]
[parameters: (UUID('832d8d96-080d-4d14-bcc6-80a23ffafa0e'), 1, 3, '%等阶%', '%吞噬要求%', '%吞噬效果%', -1)]
(Background on this error at: https://sqlalche.me/e/20/dbapi)
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 546, in _prepare_and_execute
    self._rows = await prepared_stmt.fetch(*parameters)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\prepared_stmt.py", line 176, in fetch
    data = await self.__bind_execute(args, 0, timeout)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\prepared_stmt.py", line 241, in __bind_execute
    data, status, _ = await self.__do_execute(
                      ^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\asyncpg\prepared_stmt.py", line 230, in __do_execute
    return await executor(protocol)
           ^^^^^^^^^^^^^^^^^^^^^^^^
  File "asyncpg\protocol\protocol.pyx", line 207, in bind_execute
asyncpg.exceptions.InvalidRowCountInLimitClauseError: LIMIT后的值不能为负数

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1969, in _exec_single_context
    self.dialect.do_execute(
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\default.py", line 922, in do_execute
    cursor.execute(statement, parameters)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 580, in execute
    self._adapt_connection.await_(
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 130, in await_only
    return current.driver.switch(awaitable)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 195, in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 558, in _prepare_and_execute
    self._handle_exception(error)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 509, in _handle_exception
    self._adapt_connection._handle_exception(error)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 797, in _handle_exception
    raise translated_error from error
sqlalchemy.dialects.postgresql.asyncpg.AsyncAdapt_asyncpg_dbapi.Error: <class 'asyncpg.exceptions.InvalidRowCountInLimitClauseError'>: LIMIT后的值不能为负数

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\services\chapter_vector_service.py", line 555, in exact_search_paragraphs
    result = await self.db.execute(stmt)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\ext\asyncio\session.py", line 455, in execute
    result = await greenlet_spawn(
             ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 200, in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2308, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2190, in _execute_internal
    result: Result[Any] = compile_state_cls.orm_execute_statement(
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\orm\context.py", line 293, in orm_execute_statement
    result = conn.execute(
             ^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1416, in execute
    return meth(
           ^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\sql\elements.py", line 517, in _execute_on_connection
    return connection._execute_clauseelement(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1639, in _execute_clauseelement
    ret = self._execute_context(
          ^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1848, in _execute_context
    return self._exec_single_context(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1988, in _exec_single_context
    self._handle_dbapi_exception(
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 2344, in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1969, in _exec_single_context
    self.dialect.do_execute(
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\engine\default.py", line 922, in do_execute
    cursor.execute(statement, parameters)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 580, in execute
    self._adapt_connection.await_(
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 130, in await_only
    return current.driver.switch(awaitable)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py", line 195, in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 558, in _prepare_and_execute
    self._handle_exception(error)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 509, in _handle_exception
    self._adapt_connection._handle_exception(error)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py", line 797, in _handle_exception
    raise translated_error from error
sqlalchemy.exc.DBAPIError: (sqlalchemy.dialects.postgresql.asyncpg.Error) <class 'asyncpg.exceptions.InvalidRowCountInLimitClauseError'>: LIMIT后的值不能为负数
[SQL: SELECT novel_chapter_vectors.id, novel_chapter_vectors.work_id, novel_chapter_vectors.chapter_id, novel_chapter_vectors.chapter_order, novel_chapter_vectors.chapter_title, novel_chapter_vectors.chunk_index, novel_chapter_vectors.chunk_text, novel_chapter_vectors.node_id, novel_chapter_vectors.embedding, novel_chapter_vectors.created_at, novel_chapter_vectors.updated_at
FROM novel_chapter_vectors
WHERE novel_chapter_vectors.work_id = $1::UUID AND novel_chapter_vectors.chapter_order >= $2::INTEGER AND novel_chapter_vectors.chapter_order <= $3::INTEGER AND (novel_chapter_vectors.chunk_text ILIKE $4::VARCHAR OR novel_chapter_vectors.chunk_text ILIKE $5::VARCHAR OR novel_chapter_vectors.chunk_text ILIKE $6::VARCHAR) ORDER BY novel_chapter_vectors.chapter_order, novel_chapter_vectors.chunk_index
 LIMIT $7::INTEGER]
[parameters: (UUID('832d8d96-080d-4d14-bcc6-80a23ffafa0e'), 1, 3, '%等阶%', '%吞噬要求%', '%吞噬效果%', -1)]
(Background on this error at: https://sqlalche.me/e/20/dbapi)
2026-01-30 12:13:12,997 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=2 (chapter=0, worldview=2) keywords=等阶,吞噬要求,吞噬效果
2026-01-30 12:13:12,999 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:13:13,000 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:13:28,797 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:13:28,797 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:13:28,810 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:13:28,810 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=6669, cost=$0.002326, time=15796ms
2026-01-30 12:13:28,810 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=308, 尝试次数=1
2026-01-30 12:13:28,810 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"keywords": ["器灵", "吞噬", "器物", "等阶", "吞噬要求", "吞噬效果"], "match_mode": "any", "limit": 100, "work_id": "832d8d96-080d-4d14-bcc6-80a23ffafa0e"}
2026-01-30 12:13:28,810 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 世界观匹配: 4 条
2026-01-30 12:13:28,858 - app.services.chapter_vector_service - INFO - [exact_search] work=832d8d96-080d-4d14-bcc6-80a23ffafa0e, keywords=['器灵', '吞噬', '器物']..., mode=any, range=(1, 3), hits=43
2026-01-30 12:13:28,859 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=26 (chapter=22, worldview=4) keywords=器灵,吞噬,器物,等阶,吞噬要求,吞噬效果
2026-01-30 12:13:28,859 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:13:28,859 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:13:40,187 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:13:40,187 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:13:40,202 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:13:40,204 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=6475, cost=$0.002277, time=11328ms
2026-01-30 12:13:40,207 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=321, 尝试次数=1
2026-01-30 12:13:40,211 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"keywords": ["器灵", "吞噬", "器物", "等阶", "吞噬要求", "吞噬效果"], "match_mode": "any", "limit": 50, "work_id": "832d8d96-080d-4d14-bcc6-80a23ffafa0e"}
2026-01-30 12:13:40,213 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 世界观匹配: 4 条
2026-01-30 12:13:40,257 - app.services.chapter_vector_service - INFO - [exact_search] work=832d8d96-080d-4d14-bcc6-80a23ffafa0e, keywords=['器灵', '吞噬', '器物']..., mode=any, range=(1, 3), hits=43
2026-01-30 12:13:40,258 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=26 (chapter=22, worldview=4) keywords=器灵,吞噬,器物,等阶,吞噬要求,吞噬效果
2026-01-30 12:13:40,258 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:13:40,258 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:13:45,140 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:13:45,145 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:13:45,158 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:13:45,158 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4920, cost=$0.001865, time=4886ms
2026-01-30 12:13:45,158 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=417, 尝试次数=1
2026-01-30 12:13:45,158 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=read_paragraphs params={"items": [{"chapter_order": 1, "paragraph_index": 82}, {"chapter_order": 1, "paragraph_index": 83}, {"chapter_order": 1, "paragraph_index": 87}], "work_id": "832d8d96-080d-4d14-bcc6-80a23ffafa0e"}
2026-01-30 12:13:45,158 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=read_paragraphs success=False count=0 index_base=None
2026-01-30 12:13:45,158 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:13:45,158 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:13:52,653 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:13:52,653 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:13:52,666 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:13:52,666 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=5011, cost=$0.001818, time=7497ms
2026-01-30 12:13:52,666 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=361, 尝试次数=1
2026-01-30 12:13:52,666 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=read_paragraphs params={"items": [{"chapter_order": 1, "paragraph_index": 82}, {"chapter_order": 1, "paragraph_index": 83}, {"chapter_order": 1, "paragraph_index": 87}], "work_id": "832d8d96-080d-4d14-bcc6-80a23ffafa0e"}
2026-01-30 12:13:52,666 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=read_paragraphs success=False count=0 index_base=None
2026-01-30 12:13:52,672 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:13:52,672 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:14:00,204 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:14:00,204 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:14:00,220 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:14:00,226 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4830, cost=$0.001574, time=7532ms
2026-01-30 12:14:00,226 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=119, 尝试次数=1
2026-01-30 12:14:00,230 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=list_chapters params={"work_id": "832d8d96-080d-4d14-bcc6-80a23ffafa0e"}
2026-01-30 12:14:00,230 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=list_chapters success=True count=3
2026-01-30 12:14:00,232 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:14:00,232 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:14:36,424 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:14:36,425 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:14:36,433 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:14:36,436 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=11095, cost=$0.003724, time=36192ms
2026-01-30 12:14:36,436 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=455, 尝试次数=1
2026-01-30 12:14:36,437 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=read_paragraphs params={"items": [{"chapter_order": 1, "paragraph_index": 70}, {"chapter_order": 1, "paragraph_index": 82}, {"chapter_order": 1, "paragraph_index": 83}, {"chapter_order": 1, "paragraph_index": 87}], "work_id": "832d8d96-080d-4d14-bcc6-80a23ffafa0e"}
2026-01-30 12:14:36,438 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=read_paragraphs success=False count=0 index_base=None
2026-01-30 12:14:36,439 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:14:36,439 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:14:43,018 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:14:43,018 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:14:43,040 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:14:43,044 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4591, cost=$0.001703, time=6582ms
2026-01-30 12:14:43,045 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=312, 尝试次数=1
2026-01-30 12:14:43,045 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"keywords": ["器灵", "吞噬", "器物", "等阶", "吞噬要求", "吞噬效果"], "match_mode": "any", "chapter_order": 2, "limit": 100, "work_id": "832d8d96-080d-4d14-bcc6-80a23ffafa0e"}
2026-01-30 12:14:43,045 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 世界观匹配: 4 条
2026-01-30 12:14:43,083 - app.services.chapter_vector_service - INFO - [exact_search] work=832d8d96-080d-4d14-bcc6-80a23ffafa0e, keywords=['器灵', '吞噬', '器物']..., mode=any, range=(1, 3), hits=43
2026-01-30 12:14:43,090 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=26 (chapter=22, worldview=4) keywords=器灵,吞噬,器物,等阶,吞噬要求,吞噬效果
2026-01-30 12:14:43,092 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:14:43,094 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:14:49,249 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:14:49,250 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:14:49,265 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:14:49,267 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=5279, cost=$0.001909, time=6155ms
2026-01-30 12:14:49,273 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=370, 尝试次数=1
2026-01-30 12:14:49,274 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=read_paragraphs params={"items": [{"chapter_order": 1, "paragraph_index": 82}, {"chapter_order": 1, "paragraph_index": 83}, {"chapter_order": 1, "paragraph_index": 87}], "work_id": "832d8d96-080d-4d14-bcc6-80a23ffafa0e"}
2026-01-30 12:14:49,276 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=read_paragraphs success=False count=0 index_base=None
2026-01-30 12:14:49,278 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:14:49,278 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:15:00,724 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:15:00,724 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:15:00,740 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:15:00,740 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=5280, cost=$0.001925, time=11446ms
2026-01-30 12:15:00,740 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=322, 尝试次数=1
2026-01-30 12:15:00,740 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"keywords": ["器灵", "吞噬", "器物", "等阶", "吞噬要求", "吞噬效果"], "match_mode": "any", "limit": 100, "work_id": "832d8d96-080d-4d14-bcc6-80a23ffafa0e"}
2026-01-30 12:15:00,740 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 世界观匹配: 4 条
2026-01-30 12:15:00,788 - app.services.chapter_vector_service - INFO - [exact_search] work=832d8d96-080d-4d14-bcc6-80a23ffafa0e, keywords=['器灵', '吞噬', '器物']..., mode=any, range=(1, 3), hits=43
2026-01-30 12:15:00,793 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=26 (chapter=22, worldview=4) keywords=器灵,吞噬,器物,等阶,吞噬要求,吞噬效果
2026-01-30 12:15:00,793 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:15:00,793 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:15:09,946 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:15:09,946 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:15:09,957 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:15:09,960 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=6045, cost=$0.002183, time=9153ms
2026-01-30 12:15:09,960 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=394, 尝试次数=1
2026-01-30 12:15:09,960 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=read_paragraphs params={"items": [{"chapter_order": 1, "paragraph_index": 82}, {"chapter_order": 1, "paragraph_index": 83}, {"chapter_order": 1, "paragraph_index": 87}], "work_id": "832d8d96-080d-4d14-bcc6-80a23ffafa0e"}
2026-01-30 12:15:09,960 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=read_paragraphs success=False count=0 index_base=None
2026-01-30 12:15:09,960 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:15:09,960 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:15:21,946 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:15:21,946 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:15:21,961 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:15:21,966 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=6138, cost=$0.002209, time=11986ms
2026-01-30 12:15:21,966 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=383, 尝试次数=1
2026-01-30 12:15:21,971 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"keywords": ["器灵", "吞噬", "器物", "等阶", "吞噬要求", "吞噬效果"], "match_mode": "any", "limit": 100, "chapter_ranges": [{"chapter_order_start": 2, "chapter_order_end": 2}], "work_id": "832d8d96-080d-4d14-bcc6-80a23ffafa0e"}
2026-01-30 12:15:21,971 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 世界观匹配: 4 条
2026-01-30 12:15:22,017 - app.services.chapter_vector_service - INFO - [exact_search] work=832d8d96-080d-4d14-bcc6-80a23ffafa0e, keywords=['器灵', '吞噬', '器物']..., mode=any, range=(1, 3), hits=43
2026-01-30 12:15:22,017 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=26 (chapter=22, worldview=4) keywords=器灵,吞噬,器物,等阶,吞噬要求,吞噬效果
2026-01-30 12:15:22,023 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:15:22,024 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:15:33,261 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:15:33,265 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:15:33,282 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:15:33,287 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=6497, cost=$0.002303, time=11241ms
2026-01-30 12:15:33,290 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=388, 尝试次数=1
2026-01-30 12:15:33,290 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=read_paragraphs params={"items": [{"chapter_order": 1, "paragraph_index": 82}, {"chapter_order": 1, "paragraph_index": 83}, {"chapter_order": 1, "paragraph_index": 87}], "work_id": "832d8d96-080d-4d14-bcc6-80a23ffafa0e"}
2026-01-30 12:15:33,290 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=read_paragraphs success=False count=0 index_base=None
2026-01-30 12:15:33,290 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:15:33,290 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:16:00,985 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:16:00,990 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:16:01,007 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:16:01,010 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=9307, cost=$0.003135, time=27700ms
2026-01-30 12:16:01,011 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=386, 尝试次数=1
2026-01-30 12:16:01,013 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=read_paragraphs params={"items": [{"chapter_order": 1, "paragraph_index": 82}, {"chapter_order": 1, "paragraph_index": 83}, {"chapter_order": 1, "paragraph_index": 87}], "work_id": "832d8d96-080d-4d14-bcc6-80a23ffafa0e"}
2026-01-30 12:16:01,013 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=read_paragraphs success=False count=0 index_base=None
2026-01-30 12:16:01,015 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:16:01,016 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:16:07,708 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:16:07,708 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:16:07,726 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:16:07,726 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4623, cost=$0.001508, time=6691ms
2026-01-30 12:16:07,726 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=94, 尝试次数=1
2026-01-30 12:16:07,731 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:16:07,731 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=200, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:16:11,583 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:16:11,583 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:16:11,603 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:16:11,606 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1373, cost=$0.000575, time=3851ms
2026-01-30 12:16:11,606 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=108, 尝试次数=1
2026-01-30 12:16:11,608 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 探索完成(工具循环): 37轮, 原因=已在第1章和第3章找到所有包含关键词的段落，且第2章未发现相关段落。所有相关证据已收集。
2026-01-30 12:16:11,626 - app.services.agent.execution.tool_executor - INFO - [StandardTool] explore_content 执行成功
2026-01-30 12:16:11,631 - app.api.v1.agent - INFO - [Stream] 任务完成: 在第1章至第3章范围内，找出所有包含关键词“器灵”、“吞噬”、“器物”、“等阶”、“吞噬要求”、“吞噬效果”的段落原文。 (443.1s)
2026-01-30 12:16:11,632 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1完成
2026-01-30 12:16:11,634 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共1个任务，耗时: 443.10s
2026-01-30 12:16:11,634 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2026-01-30 12:16:11,634 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=1, 展示型=0
2026-01-30 12:16:11,634 - app.services.agent.langgraph_agent - INFO - [Response] 单个输出任务(explore_content)，使用AI整合
2026-01-30 12:16:11,640 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2026-01-30 12:16:11,641 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=1, 展示型=0
2026-01-30 12:16:11,641 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=1959字符, 处理后=2024字符
2026-01-30 12:16:11,644 - app.services.agent.planning.response_builder - INFO - [Summarization] 准备发送 summarization_start 事件
2026-01-30 12:16:11,644 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-30 12:16:11,650 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-30 12:16:11,652 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=60, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:16:14,380 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:16:14,380 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-30 12:16:14,388 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:16:14,396 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=321, cost=$0.000043, time=2728ms
2026-01-30 12:16:14,396 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=50, 尝试次数=1
2026-01-30 12:16:14,399 - app.services.agent.planning.response_builder - INFO - [Summarization] reason生成: len=50 content=在第1-3章中，未找到包含“器灵”、“吞噬”、“器物”、“等阶”、“吞噬要求”、“吞噬效果”的段落。
2026-01-30 12:16:14,399 - app.services.agent.stream.stream_event_handler - INFO - [StreamEventHandler] emit_summarization_start 被调用, _on_flow_event=True, reason_len=50, reason=在第1-3章中，未找到包含“器灵”、“吞噬”、“器物”、“等阶”、“吞噬要求”、“吞噬效果”的段落。
2026-01-30 12:16:14,399 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_start 事件已发送
2026-01-30 12:16:14,399 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2026-01-30 12:16:14,399 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2026-01-30 12:16:14,409 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-30 12:16:14,411 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-30 12:16:14,411 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=20000, temp=0.7, task_type=TaskType.SUMMARIZATION
2026-01-30 12:16:21,911 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-30 12:16:21,912 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_complete 事件已发送（第一个chunk时）
2026-01-30 12:16:21,912 - app.services.agent.planning.response_builder - INFO - [Summarization] output_ready 事件已发送（第一个chunk时）
2026-01-30 12:16:23,840 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 9 个数据块，总长度: 807
2026-01-30 12:16:23,841 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 5938 (prompt=5359, completion=579)
2026-01-30 12:16:23,842 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:16:23,843 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-30 12:16:23,861 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:16:23,863 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=5938, cost=$0.003055, time=9432ms
2026-01-30 12:16:23,864 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=807
2026-01-30 12:16:24,062 - app.services.context.vector_memory_store - INFO - 🔁 跳过重复记忆，复用ID=79913e7e-d5cd-4e09-bce6-ca6639bd8456_1769696287283_02f23afe
2026-01-30 12:16:24,062 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:832d8d96-080d-4d14-bcc6-80a23ffafa0e | 重要度=0.87
2026-01-30 12:16:25,432 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:832d8d96-080d-4d14-bcc6-80a23ffafa0e | 重要度=0.77
2026-01-30 12:16:25,450 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:832d8d96-080d-4d14-bcc6-80a23ffafa0e:2edba307-74c5-40ab-aa48-84396f47c759, token=1036
2026-01-30 12:16:25,452 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:832d8d96-080d-4d14-bcc6-80a23ffafa0e:2edba307-74c5-40ab-aa48-84396f47c759, 消息数=2, 摘要长度=0, Token=1036
2026-01-30 12:16:25,452 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:832d8d96-080d-4d14-bcc6-80a23ffafa0e:2edba307-74c5-40ab-aa48-84396f47c759)
2026-01-30 12:16:25,453 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2026-01-30 12:16:25,467 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed
2026-01-30 12:16:35,496 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/2edba307-74c5-40ab-aa48-84396f47c759
INFO:     127.0.0.1:61228 - "GET /api/v1/agent/operations/2edba307-74c5-40ab-aa48-84396f47c759 HTTP/1.1" 200 OK
2026-01-30 12:20:08,956 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-30 12:20:08,957 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-30 12:20:08,957 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2026-01-30 12:20:10,611 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz:8443/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-30 12:20:10,613 - app.api.v1.agent - INFO - [Chat Stream] Mode: planning
2026-01-30 12:20:10,613 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:51037 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2026-01-30 12:20:10,631 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 仅第2章。完整复原赵穆讲解“羚羊献食”动作要点的顺序。
  - 不允许跳段或合并概括
  限定第1–...
2026-01-30 12:20:10,639 - app.api.v1.agent - INFO - [agent_chat_stream] 📚 世界观数据已注入: 人物=9, 地点=6, 设定=5, 规范=无
2026-01-30 12:20:10,639 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:832d8d96-080d-4d14-bcc6-80a23ffafa0e:2edba307-74c5-40ab-aa48-84396f47c759 (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=832d8d96-080d-4d14-bcc6-80a23ffafa0e, conversation_id=2edba307-74c5-40ab-aa48-84396f47c759)
2026-01-30 12:20:10,648 - app.services.context.store - INFO - [ContextStore] 加载上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:832d8d96-080d-4d14-bcc6-80a23ffafa0e:2edba307-74c5-40ab-aa48-84396f47c759, 2条消息
2026-01-30 12:20:10,649 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:832d8d96-080d-4d14-bcc6-80a23ffafa0e:2edba307-74c5-40ab-aa48-84396f47c759: 1036/16000 tokens
2026-01-30 12:20:10,972 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='仅第2章。完整复原赵穆讲解“羚羊献食”动作要点的顺序。
  ...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:832d8d96-080d-4d14-bcc6-80a23ffafa0e', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=1条
2026-01-30 12:20:10,974 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=832d8d96-080d-4d14-bcc6-80a23ffafa0e | 含用户级=True | 找到=1条
2026-01-30 12:20:10,995 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 3条消息, 1036 tokens, 耗时 350.79ms
2026-01-30 12:20:10,997 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 3 条历史消息 (token: 1036, has_summary: False)
2026-01-30 12:20:10,999 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-30 12:20:10,999 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-30 12:20:11,000 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=200, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-30 12:20:12,464 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:20:12,465 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-30 12:20:12,482 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:20:12,486 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1214, cost=$0.000127, time=1465ms
2026-01-30 12:20:12,486 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=39, 尝试次数=1
2026-01-30 12:20:12,489 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-30 12:20:12,491 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-30 12:20:12,491 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=20, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-30 12:20:13,687 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:20:13,692 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-30 12:20:13,701 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:20:13,709 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=424, cost=$0.000043, time=1201ms
2026-01-30 12:20:13,709 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=7, 尝试次数=1
2026-01-30 12:20:13,709 - app.services.agent.intent.classifier - INFO - [Intent] AI识别结果: writing
2026-01-30 12:20:13,709 - app.services.agent.langgraph_agent - INFO - [Planning] AI意图分类: writing (置信度: 0.90)
2026-01-30 12:20:13,709 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 仅第2章。完整复原赵穆讲解“羚羊献食”动作要点的顺序。
  - 不允许跳段或合并概括
  限定第1–...
2026-01-30 12:20:13,725 - app.core.cache - INFO - ✅ 缓存命中: prompt:planning:v2.41.0:get_planning_static_prompt:fca6eb91156619d0
2026-01-30 12:20:13,734 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-30 12:20:13,734 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=story_planning, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: story_planning; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-01-30 12:20:13,735 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.3, task_type=TaskType.STORY_PLANNING
2026-01-30 12:20:35,084 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-30 12:20:40,739 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 12 个数据块，总长度: 1509
2026-01-30 12:20:40,739 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 23930 (prompt=23188, completion=742)
2026-01-30 12:20:40,740 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:20:40,741 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-30 12:20:40,756 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:20:40,758 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=23930, cost=$0.036405, time=27005ms
2026-01-30 12:20:40,759 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=23930
2026-01-30 12:20:40,760 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户有两个明确的查询请求：1. 完整复原第2章中“羚羊献食”, 原料=完成这两个任务需要读取第1、2、3章的原, 处理=创建两个并行的 explore_cont
2026-01-30 12:20:40,763 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共2个任务
2026-01-30 12:20:40,764 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共2个任务，耗时: 27.06s
2026-01-30 12:20:40,764 - app.api.v1.agent - INFO - [Stream] Plan tasks: 2 items
2026-01-30 12:20:40,766 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2026-01-30 12:20:40,766 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2026-01-30 12:20:40,767 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2026-01-30 12:20:40,768 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] DAG 调度启用，任务数=2, 有依赖任务=0
2026-01-30 12:20:40,769 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1开始: 在第2章中，查找赵穆讲解“羚羊献食”动作要点的所有段落，并按原文顺序排列。
2026-01-30 12:20:40,769 - app.api.v1.agent - INFO - [Stream] Task started: 在第2章中，查找赵穆讲解“羚羊献食”动作要点的所有段落，并按原文顺序排列。 (icon=Wrench)
2026-01-30 12:20:40,770 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: explore_content
2026-01-30 12:20:40,773 - app.services.agent.tools.explore_tools - INFO - [explore_content] 开始: work_id=832d8d96-080d-4d14-bcc6-80a23ffafa0e, target=仅限第2章。完整复原赵穆讲解“羚羊献食”动作要点的顺序。
约束：章节范围：第1–3章、1–3章、第2...
2026-01-30 12:20:40,774 - app.services.agent.tools.explore_tools - INFO - [explore_content] 规划传入关键词: ['羚羊献食', '赵穆', '动作要点', '讲解', '第2章']
2026-01-30 12:20:40,776 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 启用严格段落号模式
2026-01-30 12:20:40,777 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 章节范围锁定: 第1-3章
2026-01-30 12:20:40,777 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 任务禁止整章阅读
2026-01-30 12:20:40,777 - app.services.agent.tools.explore_tools - INFO - [explore_content] 复用共享状态: searched=6, read_paragraphs=19, read_chapters=0
2026-01-30 12:20:40,778 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 开始探索 V5: work_id=832d8d96-080d-4d14-bcc6-80a23ffafa0e, target=仅限第2章。完整复原赵穆讲解“羚羊献食”动作要点的顺序。
约束：章节范围：第1–3章、1–3章、第2...
2026-01-30 12:20:40,781 - app.services.chapter_service - INFO - [ChapterService] Querying chapters for work_id=832d8d96-080d-4d14-bcc6-80a23ffafa0e, type=<class 'uuid.UUID'>
2026-01-30 12:20:40,793 - app.services.chapter_service - INFO - [ChapterService] Found 5 chapters
2026-01-30 12:20:40,794 - app.services.chapter_service - INFO -   - Chapter: 第1章 吞噬, order=1
2026-01-30 12:20:40,795 - app.services.chapter_service - INFO -   - ... (3 more chapters)
2026-01-30 12:20:40,796 - app.services.chapter_service - INFO -   - Chapter: 第5章 太一门, order=5
2026-01-30 12:20:40,806 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 章节范围映射: 第1-3章 -> 第1-3章
2026-01-30 12:20:40,817 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 自动获取世界观...
2026-01-30 12:20:40,839 - app.services.agent.langgraph_tools - INFO - [get_writing_context] ✅ 获取创作上下文成功: include=worldview
2026-01-30 12:20:40,846 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 世界观获取完成: 20 条
2026-01-30 12:20:40,850 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:20:40,855 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=80, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:20:43,932 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:20:43,933 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:20:43,965 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:20:43,970 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=460, cost=$0.000149, time=3077ms
2026-01-30 12:20:43,972 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=9, 尝试次数=1
2026-01-30 12:20:43,972 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 强制流程步骤: list_chapters
2026-01-30 12:20:43,972 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=list_chapters params={"work_id": "832d8d96-080d-4d14-bcc6-80a23ffafa0e"}
2026-01-30 12:20:43,973 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=list_chapters success=True count=3
2026-01-30 12:20:43,974 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:20:43,974 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=80, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:20:54,703 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:20:54,704 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:20:54,716 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:20:54,719 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2042, cost=$0.000637, time=10730ms
2026-01-30 12:20:54,720 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=18, 尝试次数=1
2026-01-30 12:20:54,721 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 强制流程步骤: list_paragraphs
2026-01-30 12:20:54,721 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=list_paragraphs params={"chapter_order": 1, "offset": 0, "limit": 50, "preview_len": 80, "work_id": "832d8d96-080d-4d14-bcc6-80a23ffafa0e"}
2026-01-30 12:20:54,730 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=list_paragraphs success=True chapter=1 offset=0 limit=50 approximate=None
2026-01-30 12:20:54,731 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:20:54,732 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:20:57,202 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:20:57,204 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:20:57,221 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:20:57,223 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2025, cost=$0.000810, time=2472ms
2026-01-30 12:20:57,224 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=186, 尝试次数=1
2026-01-30 12:20:57,225 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=list_paragraphs params={"chapter_order": 2, "offset": 0, "limit": 50, "work_id": "832d8d96-080d-4d14-bcc6-80a23ffafa0e"}
2026-01-30 12:20:57,236 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=list_paragraphs success=True chapter=2 offset=0 limit=50 approximate=None
2026-01-30 12:20:57,237 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:20:57,237 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:21:00,550 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:21:00,551 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:21:00,563 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:21:00,564 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2309, cost=$0.000957, time=3313ms
2026-01-30 12:21:00,565 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=243, 尝试次数=1
2026-01-30 12:21:00,566 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=read_paragraphs params={"chapter_order": 2, "offset": 4, "limit": 20, "context_before": 0, "context_after": 0, "work_id": "832d8d96-080d-4d14-bcc6-80a23ffafa0e"}
2026-01-30 12:21:00,578 - app.services.agent.langgraph_tools - INFO - [read_paragraphs] start items=13 index_base=zero
2026-01-30 12:21:00,587 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=4 corrected=False final=4
2026-01-30 12:21:00,589 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第4段
2026-01-30 12:21:00,596 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=5 corrected=False final=5
2026-01-30 12:21:00,597 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第5段
2026-01-30 12:21:00,605 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=6 corrected=False final=6
2026-01-30 12:21:00,605 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第6段
2026-01-30 12:21:00,612 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=7 corrected=False final=7
2026-01-30 12:21:00,613 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第7段
2026-01-30 12:21:00,620 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=8 corrected=False final=8
2026-01-30 12:21:00,621 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第8段
2026-01-30 12:21:00,628 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=9 corrected=False final=9
2026-01-30 12:21:00,629 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第9段
2026-01-30 12:21:00,636 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=10 corrected=False final=10
2026-01-30 12:21:00,637 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第10段
2026-01-30 12:21:00,644 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=11 corrected=False final=11
2026-01-30 12:21:00,644 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第11段
2026-01-30 12:21:00,651 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=12 corrected=False final=12
2026-01-30 12:21:00,652 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第12段
2026-01-30 12:21:00,659 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=13 corrected=False final=13
2026-01-30 12:21:00,660 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第13段
2026-01-30 12:21:00,667 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=14 corrected=False final=14
2026-01-30 12:21:00,668 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第14段
2026-01-30 12:21:00,675 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=15 corrected=False final=15
2026-01-30 12:21:00,675 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第15段
2026-01-30 12:21:00,685 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=16 corrected=False final=16
2026-01-30 12:21:00,686 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第16段
2026-01-30 12:21:00,687 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=read_paragraphs success=True count=13 index_base=None
2026-01-30 12:21:00,689 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:21:00,689 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:21:06,244 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:21:06,246 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:21:06,260 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:21:06,262 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=3381, cost=$0.001267, time=5556ms
2026-01-30 12:21:06,263 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=166, 尝试次数=1
2026-01-30 12:21:06,263 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:21:06,264 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=200, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:21:11,449 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:21:11,450 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:21:11,459 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:21:11,460 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1655, cost=$0.000646, time=5186ms
2026-01-30 12:21:11,461 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=92, 尝试次数=1
2026-01-30 12:21:11,462 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 探索完成(工具循环): 4轮, 原因=已完整复原赵穆讲解“羚羊献食”动作要点的顺序。根据第2章第5段和第6段，动作要点为：1. 右脚上前落在左脚前方，抬左脚向前弹踢！2. 同时，右手刀由前向右下方，划弧抡撩，然后挑于前方，刀刃向上，刀尖向前！第7段内容为“……”，表示没有进一步的详细动作描述。
2026-01-30 12:21:11,465 - app.services.agent.execution.tool_executor - INFO - [StandardTool] explore_content 执行成功
2026-01-30 12:21:11,468 - app.api.v1.agent - INFO - [Stream] 任务完成: 在第2章中，查找赵穆讲解“羚羊献食”动作要点的所有段落，并按原文顺序排列。 (30.7s)
2026-01-30 12:21:11,468 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1完成
2026-01-30 12:21:11,469 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务2开始: 在第1-3章中，为指定时间点（进入镖局、考核前半个月、傍晚练武、晚饭后、夜里练刀/梦境、醒后练功）查找原文证据。
2026-01-30 12:21:11,470 - app.api.v1.agent - INFO - [Stream] Task started: 在第1-3章中，为指定时间点（进入镖局、考核前半个月、傍晚练武、晚饭后、夜里练刀/梦境、醒后练功）查找原文证据。 (icon=Wrench)
2026-01-30 12:21:11,470 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: explore_content
2026-01-30 12:21:11,471 - app.services.agent.tools.explore_tools - INFO - [explore_content] 开始: work_id=832d8d96-080d-4d14-bcc6-80a23ffafa0e, target=限定第1–3章，构建时间线：进入镖局 → 考核前半个月 → 傍晚练武 → 晚饭后 → 夜里练刀/梦境...
2026-01-30 12:21:11,472 - app.services.agent.tools.explore_tools - INFO - [explore_content] 规划传入关键词: ['进入镖局', '考核', '半个月', '傍晚', '练武', '晚饭后', '夜里', '练刀', '梦境', '醒后']
2026-01-30 12:21:11,472 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 启用严格段落号模式
2026-01-30 12:21:11,472 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 章节范围锁定: 第1-3章
2026-01-30 12:21:11,472 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 任务禁止整章阅读
2026-01-30 12:21:11,472 - app.services.agent.tools.explore_tools - INFO - [explore_content] 复用共享状态: searched=6, read_paragraphs=32, read_chapters=0
2026-01-30 12:21:11,473 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 开始探索 V5: work_id=832d8d96-080d-4d14-bcc6-80a23ffafa0e, target=限定第1–3章，构建时间线：进入镖局 → 考核前半个月 → 傍晚练武 → 晚饭后 → 夜里练刀/梦境...
2026-01-30 12:21:11,474 - app.services.chapter_service - INFO - [ChapterService] Querying chapters for work_id=832d8d96-080d-4d14-bcc6-80a23ffafa0e, type=<class 'uuid.UUID'>
2026-01-30 12:21:11,479 - app.services.chapter_service - INFO - [ChapterService] Found 5 chapters
2026-01-30 12:21:11,479 - app.services.chapter_service - INFO -   - Chapter: 第1章 吞噬, order=1
2026-01-30 12:21:11,480 - app.services.chapter_service - INFO -   - ... (3 more chapters)
2026-01-30 12:21:11,480 - app.services.chapter_service - INFO -   - Chapter: 第5章 太一门, order=5
2026-01-30 12:21:11,486 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 章节范围映射: 第1-3章 -> 第1-3章
2026-01-30 12:21:11,494 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 自动获取世界观...
2026-01-30 12:21:11,503 - app.services.agent.langgraph_tools - INFO - [get_writing_context] ✅ 获取创作上下文成功: include=worldview
2026-01-30 12:21:11,505 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 世界观获取完成: 20 条
2026-01-30 12:21:11,506 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:21:11,506 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=80, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:21:14,585 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:21:14,586 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:21:14,596 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:21:14,598 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=659, cost=$0.000220, time=3081ms
2026-01-30 12:21:14,598 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=17, 尝试次数=1
2026-01-30 12:21:14,599 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 强制流程步骤: list_chapters
2026-01-30 12:21:14,599 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=list_chapters params={"work_id": "832d8d96-080d-4d14-bcc6-80a23ffafa0e"}
2026-01-30 12:21:14,599 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=list_chapters success=True count=3
2026-01-30 12:21:14,600 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:21:14,601 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=80, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:21:23,429 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:21:23,430 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:21:23,447 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:21:23,450 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=706, cost=$0.000236, time=8829ms
2026-01-30 12:21:23,451 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=16, 尝试次数=1
2026-01-30 12:21:23,452 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 强制流程步骤: list_paragraphs
2026-01-30 12:21:23,452 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=list_paragraphs params={"chapter_order": 1, "offset": 0, "limit": 50, "preview_len": 80, "work_id": "832d8d96-080d-4d14-bcc6-80a23ffafa0e"}
2026-01-30 12:21:23,467 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=list_paragraphs success=True chapter=1 offset=0 limit=50 approximate=None
2026-01-30 12:21:23,469 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:21:23,469 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:21:31,043 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:21:31,043 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:21:31,055 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:21:31,056 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=3599, cost=$0.001546, time=7575ms
2026-01-30 12:21:31,057 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=522, 尝试次数=1
2026-01-30 12:21:31,057 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=read_paragraphs params={"items": [{"chapter_order": 1, "paragraph_index": 2}, {"chapter_order": 1, "paragraph_index": 5}, {"chapter_order": 1, "paragraph_index": 6}, {"chapter_order": 1, "paragraph_index": 7}], "context_before": 0, "context_after": 0, "work_id": "832d8d96-080d-4d14-bcc6-80a23ffafa0e"}
2026-01-30 12:21:31,058 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=read_paragraphs success=False count=0 index_base=None
2026-01-30 12:21:31,058 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:21:31,058 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:21:33,411 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:21:33,412 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:21:33,426 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:21:33,429 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1535, cost=$0.000698, time=2353ms
2026-01-30 12:21:33,430 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=237, 尝试次数=1
2026-01-30 12:21:33,431 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"keywords": "镖局", "match_mode": "all", "limit": 100, "chapter_ranges": [[1, 3]], "work_id": "832d8d96-080d-4d14-bcc6-80a23ffafa0e"}
2026-01-30 12:21:33,432 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 世界观匹配: 8 条
2026-01-30 12:21:33,452 - app.services.chapter_vector_service - INFO - [exact_search] work=832d8d96-080d-4d14-bcc6-80a23ffafa0e, keywords=['镖局']..., mode=all, range=(1, 3), hits=20
2026-01-30 12:21:33,463 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=25 corrected=False final=25
2026-01-30 12:21:33,465 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第25段
2026-01-30 12:21:33,477 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=37 corrected=False final=37
2026-01-30 12:21:33,478 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第37段
2026-01-30 12:21:33,485 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=50 corrected=False final=50
2026-01-30 12:21:33,486 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第50段
2026-01-30 12:21:33,487 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=20 (chapter=12, worldview=8) keywords=镖局
2026-01-30 12:21:33,488 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:21:33,489 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:21:36,423 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:21:36,425 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:21:36,439 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:21:36,440 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=3133, cost=$0.001162, time=2935ms
2026-01-30 12:21:36,441 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=217, 尝试次数=1
2026-01-30 12:21:36,441 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"keywords": "考核,半个月", "match_mode": "and", "limit": 50, "work_id": "832d8d96-080d-4d14-bcc6-80a23ffafa0e"}
2026-01-30 12:21:36,442 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 世界观匹配: 2 条
2026-01-30 12:21:36,457 - app.services.chapter_vector_service - INFO - [exact_search] work=832d8d96-080d-4d14-bcc6-80a23ffafa0e, keywords=['考核', '半个月']..., mode=any, range=(1, 3), hits=6
2026-01-30 12:21:36,465 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=48 corrected=False final=48
2026-01-30 12:21:36,465 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第48段
2026-01-30 12:21:36,477 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=56 corrected=False final=56
2026-01-30 12:21:36,478 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第56段
2026-01-30 12:21:36,479 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=6 (chapter=4, worldview=2) keywords=考核,半个月
2026-01-30 12:21:36,480 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:21:36,480 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:21:40,727 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:21:40,729 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:21:40,743 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:21:40,745 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2942, cost=$0.001136, time=4249ms
2026-01-30 12:21:40,745 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=240, 尝试次数=1
2026-01-30 12:21:40,747 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"keywords": ["傍晚", "练武", "练功"], "match_mode": "any", "limit": 20, "work_id": "832d8d96-080d-4d14-bcc6-80a23ffafa0e"}
2026-01-30 12:21:40,764 - app.services.chapter_vector_service - INFO - [exact_search] work=832d8d96-080d-4d14-bcc6-80a23ffafa0e, keywords=['傍晚', '练武', '练功']..., mode=any, range=(1, 3), hits=16
2026-01-30 12:21:40,776 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=4 corrected=False final=4
2026-01-30 12:21:40,779 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第4段
2026-01-30 12:21:40,791 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=20 corrected=False final=20
2026-01-30 12:21:40,792 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第20段
2026-01-30 12:21:40,802 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=26 corrected=False final=26
2026-01-30 12:21:40,807 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第26段
2026-01-30 12:21:40,815 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=38 corrected=False final=38
2026-01-30 12:21:40,818 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第38段
2026-01-30 12:21:40,828 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=59 corrected=False final=59
2026-01-30 12:21:40,829 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第59段
2026-01-30 12:21:40,837 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=63 corrected=False final=63
2026-01-30 12:21:40,838 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第63段
2026-01-30 12:21:40,842 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=13 (chapter=13, worldview=0) keywords=傍晚,练武,练功
2026-01-30 12:21:40,843 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:21:40,843 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:21:53,827 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:21:53,830 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:21:53,846 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:21:53,848 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=6307, cost=$0.002112, time=12987ms
2026-01-30 12:21:53,849 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=222, 尝试次数=1
2026-01-30 12:21:53,850 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"keywords": ["晚饭", "饭后", "晚餐"], "match_mode": "any", "limit": 100, "work_id": "832d8d96-080d-4d14-bcc6-80a23ffafa0e"}
2026-01-30 12:21:53,874 - app.services.chapter_vector_service - INFO - [exact_search] work=832d8d96-080d-4d14-bcc6-80a23ffafa0e, keywords=['晚饭', '饭后', '晚餐']..., mode=any, range=(1, 3), hits=2
2026-01-30 12:21:53,877 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=2 (chapter=2, worldview=0) keywords=晚饭,饭后,晚餐
2026-01-30 12:21:53,878 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:21:53,879 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:21:59,556 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:21:59,556 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:21:59,580 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:21:59,580 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=3204, cost=$0.001192, time=5677ms
2026-01-30 12:21:59,580 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=215, 尝试次数=1
2026-01-30 12:21:59,580 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"keywords": ["夜里", "练刀", "梦境"], "match_mode": "any", "limit": 10, "work_id": "832d8d96-080d-4d14-bcc6-80a23ffafa0e"}
2026-01-30 12:21:59,597 - app.services.chapter_vector_service - INFO - [exact_search] work=832d8d96-080d-4d14-bcc6-80a23ffafa0e, keywords=['夜里', '练刀', '梦境']..., mode=any, range=(1, 3), hits=2
2026-01-30 12:21:59,608 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=0 corrected=False final=0
2026-01-30 12:21:59,609 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第3章第0段
2026-01-30 12:21:59,609 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=2 (chapter=2, worldview=0) keywords=夜里,练刀,梦境
2026-01-30 12:21:59,609 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:21:59,609 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:22:14,299 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:22:14,299 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:22:14,318 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:22:14,322 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=3357, cost=$0.001405, time=14692ms
2026-01-30 12:22:14,322 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=438, 尝试次数=1
2026-01-30 12:22:14,323 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=read_paragraphs params={"items": [{"chapter_order": 1, "paragraph_index": 16}, {"chapter_order": 1, "paragraph_index": 19}, {"chapter_order": 2, "paragraph_index": 50}], "context_before": 0, "context_after": 0, "work_id": "832d8d96-080d-4d14-bcc6-80a23ffafa0e"}
2026-01-30 12:22:14,324 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=read_paragraphs success=False count=0 index_base=None
2026-01-30 12:22:14,325 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:22:14,326 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:22:24,124 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:22:24,124 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:22:24,143 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:22:24,147 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4151, cost=$0.001481, time=9798ms
2026-01-30 12:22:24,147 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=234, 尝试次数=1
2026-01-30 12:22:24,147 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=read_paragraph params={"chapter_order": 1, "paragraph_index": 16, "context_before": 0, "context_after": 0, "work_id": "832d8d96-080d-4d14-bcc6-80a23ffafa0e"}
2026-01-30 12:22:24,147 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=read_paragraph success=False chapter=1 paragraph=16 index_base=None
2026-01-30 12:22:24,152 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:22:24,152 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:22:45,256 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:22:45,256 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:22:45,272 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:22:45,272 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=6965, cost=$0.002272, time=21104ms
2026-01-30 12:22:45,277 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=143, 尝试次数=1
2026-01-30 12:22:45,278 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:22:45,278 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=200, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:22:51,089 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:22:51,091 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:22:51,104 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:22:51,105 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1853, cost=$0.000809, time=5813ms
2026-01-30 12:22:51,105 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=153, 尝试次数=1
2026-01-30 12:22:51,105 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 探索完成(工具循环): 10轮, 原因=已在限定章节范围内，收集了所有时间点的原文证据。其中“晚饭后”的证据为领取晚饭，而非晚饭后具体活动，但由于所有章节已达读取上限，无法进一步搜索或读取新的段落。因此，任务已完成到最大程度。
2026-01-30 12:22:51,109 - app.services.agent.execution.tool_executor - INFO - [StandardTool] explore_content 执行成功
2026-01-30 12:22:51,111 - app.api.v1.agent - INFO - [Stream] 任务完成: 在第1-3章中，为指定时间点（进入镖局、考核前半个月、傍晚练武、晚饭后、夜里练刀/梦境、醒后练功）查找原文证据。 (99.6s)
2026-01-30 12:22:51,112 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务2完成
2026-01-30 12:22:51,112 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共2个任务，耗时: 130.35s
2026-01-30 12:22:51,113 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2026-01-30 12:22:51,113 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=2, 展示型=0
2026-01-30 12:22:51,113 - app.services.agent.langgraph_agent - INFO - [Response] 2个输出任务（含续写），使用AI整合
2026-01-30 12:22:51,114 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2026-01-30 12:22:51,114 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=2, 展示型=0
2026-01-30 12:22:51,114 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=4016字符, 处理后=4114字符
2026-01-30 12:22:51,114 - app.services.agent.planning.response_builder - INFO - [Summarization] 准备发送 summarization_start 事件
2026-01-30 12:22:51,115 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-30 12:22:51,116 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-30 12:22:51,116 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=60, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:22:53,252 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:22:53,252 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-30 12:22:53,263 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:22:53,263 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=414, cost=$0.000049, time=2136ms
2026-01-30 12:22:53,269 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=33, 尝试次数=1
2026-01-30 12:22:53,269 - app.services.agent.planning.response_builder - INFO - [Summarization] reason生成: len=33 content=赵穆在第2章详细讲解了“羚羊献食”的动作要点，并按顺序进行了复原。
2026-01-30 12:22:53,269 - app.services.agent.stream.stream_event_handler - INFO - [StreamEventHandler] emit_summarization_start 被调用, _on_flow_event=True, reason_len=33, reason=赵穆在第2章详细讲解了“羚羊献食”的动作要点，并按顺序进行了复原。
2026-01-30 12:22:53,269 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_start 事件已发送
2026-01-30 12:22:53,269 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2026-01-30 12:22:53,269 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2026-01-30 12:22:53,275 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-30 12:22:53,275 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-30 12:22:53,280 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=20000, temp=0.7, task_type=TaskType.SUMMARIZATION
2026-01-30 12:23:06,621 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-30 12:23:06,623 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_complete 事件已发送（第一个chunk时）
2026-01-30 12:23:06,623 - app.services.agent.planning.response_builder - INFO - [Summarization] output_ready 事件已发送（第一个chunk时）
2026-01-30 12:23:09,571 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 14 个数据块，总长度: 1250
2026-01-30 12:23:09,571 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 10975 (prompt=10082, completion=893)
2026-01-30 12:23:09,572 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:23:09,572 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-30 12:23:09,586 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:23:09,588 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=10975, cost=$0.005257, time=16293ms
2026-01-30 12:23:09,590 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=1250
2026-01-30 12:23:09,593 - app.services.context.vector_memory_store - INFO - 🔁 跳过重复记忆，复用ID=79913e7e-d5cd-4e09-bce6-ca6639bd8456_1769698570739_ee3e8190
2026-01-30 12:23:09,593 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:832d8d96-080d-4d14-bcc6-80a23ffafa0e | 重要度=0.87
2026-01-30 12:23:10,881 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:832d8d96-080d-4d14-bcc6-80a23ffafa0e | 重要度=0.60
2026-01-30 12:23:10,898 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:832d8d96-080d-4d14-bcc6-80a23ffafa0e:2edba307-74c5-40ab-aa48-84396f47c759, token=2516
2026-01-30 12:23:10,901 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:832d8d96-080d-4d14-bcc6-80a23ffafa0e:2edba307-74c5-40ab-aa48-84396f47c759, 消息数=4, 摘要长度=0, Token=2516
2026-01-30 12:23:10,902 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:832d8d96-080d-4d14-bcc6-80a23ffafa0e:2edba307-74c5-40ab-aa48-84396f47c759)
2026-01-30 12:23:10,902 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2026-01-30 12:23:10,908 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed
2026-01-30 12:23:19,358 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/2edba307-74c5-40ab-aa48-84396f47c759
INFO:     127.0.0.1:61675 - "GET /api/v1/agent/operations/2edba307-74c5-40ab-aa48-84396f47c759 HTTP/1.1" 200 OK
2026-01-30 12:25:34,469 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 832d8d96-080d-4d14-bcc6-80a23ffafa0e, chapter_id: 4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469
2026-01-30 12:25:34,483 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469
2026-01-30 12:25:34,494 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: 011f4c78-04f0-40f6-99e5-97de0582c58f
2026-01-30 12:25:34,495 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-30 12:25:34,506 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:53534 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-30 12:25:34,522 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 832d8d96-080d-4d14-bcc6-80a23ffafa0e, chapter_id: 4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469
2026-01-30 12:25:34,540 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469
2026-01-30 12:25:34,540 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: 011f4c78-04f0-40f6-99e5-97de0582c58f
2026-01-30 12:25:34,540 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-30 12:25:34,546 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:63270 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-30 12:25:34,637 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
2026-01-30 12:25:34,638 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469/revisions
INFO:     127.0.0.1:55926 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
INFO:     127.0.0.1:55927 - "GET /api/v1/chapters/4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469/revisions?status=pending HTTP/1.1" 200 OK
2026-01-30 12:25:34,683 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469/revisions
INFO:     127.0.0.1:59096 - "GET /api/v1/chapters/4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469/revisions?status=pending HTTP/1.1" 200 OK
2026-01-30 12:25:34,728 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第3章 一夕千悟 (order=3)
2026-01-30 12:25:36,970 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第3章 一夕千悟 (64 paragraphs)
2026-01-30 12:25:36,991 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:832d8d96-080d-4d14-bcc6-80a23ffafa0e
2026-01-30 12:25:36,993 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469
INFO:     127.0.0.1:55131 - "PUT /api/v1/chapters/4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469 HTTP/1.1" 200 OK
2026-01-30 12:25:37,085 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第3章 一夕千悟 (order=3)
2026-01-30 12:25:39,272 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第3章 一夕千悟 (64 paragraphs)
2026-01-30 12:25:39,275 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469 内容更新，新段落数: 64
2026-01-30 12:25:39,288 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:832d8d96-080d-4d14-bcc6-80a23ffafa0e
2026-01-30 12:25:39,289 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469
INFO:     127.0.0.1:63172 - "PUT /api/v1/chapters/4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469 HTTP/1.1" 200 OK
2026-01-30 12:25:39,387 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第3章 一夕千悟 (order=3)
2026-01-30 12:25:39,396 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第3章 一夕千悟 (order=3)
2026-01-30 12:25:41,664 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469 内容更新，新段落数: 64
2026-01-30 12:25:41,668 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469 内容更新，新段落数: 64
2026-01-30 12:25:41,672 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第3章 一夕千悟 (64 paragraphs)
2026-01-30 12:25:43,897 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:832d8d96-080d-4d14-bcc6-80a23ffafa0e
2026-01-30 12:25:43,900 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469
INFO:     127.0.0.1:63486 - "PUT /api/v1/chapters/4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469 HTTP/1.1" 200 OK
2026-01-30 12:25:43,920 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:832d8d96-080d-4d14-bcc6-80a23ffafa0e
2026-01-30 12:25:43,923 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469
2026-01-30 12:25:43,925 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第3章 一夕千悟 (64 paragraphs)
INFO:     127.0.0.1:63487 - "PUT /api/v1/chapters/4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469 HTTP/1.1" 200 OK
2026-01-30 12:26:29,916 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 832d8d96-080d-4d14-bcc6-80a23ffafa0e, chapter_id: 07352d22-b4c9-4aa0-90ab-2408baca9e29
2026-01-30 12:26:29,922 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 07352d22-b4c9-4aa0-90ab-2408baca9e29
2026-01-30 12:26:29,922 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
2026-01-30 12:26:29,923 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:64910 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-30 12:26:29,951 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 832d8d96-080d-4d14-bcc6-80a23ffafa0e, chapter_id: 07352d22-b4c9-4aa0-90ab-2408baca9e29
2026-01-30 12:26:29,962 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 07352d22-b4c9-4aa0-90ab-2408baca9e29
2026-01-30 12:26:29,962 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
2026-01-30 12:26:29,963 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:60242 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-30 12:26:29,974 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/07352d22-b4c9-4aa0-90ab-2408baca9e29/revisions
INFO:     127.0.0.1:60244 - "GET /api/v1/chapters/07352d22-b4c9-4aa0-90ab-2408baca9e29/revisions?status=pending HTTP/1.1" 200 OK
2026-01-30 12:26:29,989 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/07352d22-b4c9-4aa0-90ab-2408baca9e29/revisions
INFO:     127.0.0.1:50062 - "GET /api/v1/chapters/07352d22-b4c9-4aa0-90ab-2408baca9e29/revisions?status=pending HTTP/1.1" 200 OK
2026-01-30 12:26:30,198 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/2edba307-74c5-40ab-aa48-84396f47c759
INFO:     127.0.0.1:58803 - "GET /api/v1/agent/operations/2edba307-74c5-40ab-aa48-84396f47c759 HTTP/1.1" 200 OK
2026-01-30 12:26:30,222 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/2edba307-74c5-40ab-aa48-84396f47c759
INFO:     127.0.0.1:65130 - "GET /api/v1/agent/operations/2edba307-74c5-40ab-aa48-84396f47c759 HTTP/1.1" 200 OK
2026-01-30 12:26:30,242 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-30 12:26:32,442 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:832d8d96-080d-4d14-bcc6-80a23ffafa0e
2026-01-30 12:26:32,445 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/07352d22-b4c9-4aa0-90ab-2408baca9e29
INFO:     127.0.0.1:58805 - "PUT /api/v1/chapters/07352d22-b4c9-4aa0-90ab-2408baca9e29 HTTP/1.1" 200 OK
2026-01-30 12:26:32,455 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
2026-01-30 12:26:32,519 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-30 12:26:34,558 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:832d8d96-080d-4d14-bcc6-80a23ffafa0e
2026-01-30 12:26:34,560 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/07352d22-b4c9-4aa0-90ab-2408baca9e29
INFO:     127.0.0.1:63920 - "PUT /api/v1/chapters/07352d22-b4c9-4aa0-90ab-2408baca9e29 HTTP/1.1" 200 OK
2026-01-30 12:26:34,574 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
2026-01-30 12:29:49,466 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 832d8d96-080d-4d14-bcc6-80a23ffafa0e, chapter_id: 4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469
2026-01-30 12:29:49,476 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469
2026-01-30 12:29:49,482 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: 011f4c78-04f0-40f6-99e5-97de0582c58f
2026-01-30 12:29:49,482 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-30 12:29:49,487 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:56079 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-30 12:29:49,537 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 832d8d96-080d-4d14-bcc6-80a23ffafa0e, chapter_id: 4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469
2026-01-30 12:29:49,557 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469
2026-01-30 12:29:49,560 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469/revisions
INFO:     127.0.0.1:64096 - "GET /api/v1/chapters/4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469/revisions?status=pending HTTP/1.1" 200 OK
2026-01-30 12:29:49,565 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: 011f4c78-04f0-40f6-99e5-97de0582c58f
2026-01-30 12:29:49,566 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-30 12:29:49,572 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:64095 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-30 12:29:49,614 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第3章 一夕千悟 (order=3)
2026-01-30 12:29:51,668 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469/revisions
INFO:     127.0.0.1:49861 - "GET /api/v1/chapters/4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469/revisions?status=pending HTTP/1.1" 200 OK
2026-01-30 12:29:51,681 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:832d8d96-080d-4d14-bcc6-80a23ffafa0e
2026-01-30 12:29:51,683 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469
INFO:     127.0.0.1:53269 - "PUT /api/v1/chapters/4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469 HTTP/1.1" 200 OK
2026-01-30 12:29:51,700 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第3章 一夕千悟 (64 paragraphs)
2026-01-30 12:29:51,732 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第3章 一夕千悟 (order=3)
2026-01-30 12:29:53,719 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:832d8d96-080d-4d14-bcc6-80a23ffafa0e
2026-01-30 12:29:53,721 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469
2026-01-30 12:29:53,723 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第3章 一夕千悟 (64 paragraphs)
INFO:     127.0.0.1:56025 - "PUT /api/v1/chapters/4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469 HTTP/1.1" 200 OK
2026-01-30 12:29:59,772 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 832d8d96-080d-4d14-bcc6-80a23ffafa0e, chapter_id: 07352d22-b4c9-4aa0-90ab-2408baca9e29
2026-01-30 12:29:59,780 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 07352d22-b4c9-4aa0-90ab-2408baca9e29
2026-01-30 12:29:59,781 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
2026-01-30 12:29:59,789 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:59969 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-30 12:29:59,824 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 832d8d96-080d-4d14-bcc6-80a23ffafa0e, chapter_id: 07352d22-b4c9-4aa0-90ab-2408baca9e29
2026-01-30 12:29:59,833 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 07352d22-b4c9-4aa0-90ab-2408baca9e29
2026-01-30 12:29:59,833 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
2026-01-30 12:29:59,834 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:56069 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-30 12:29:59,841 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/07352d22-b4c9-4aa0-90ab-2408baca9e29/revisions
INFO:     127.0.0.1:56070 - "GET /api/v1/chapters/07352d22-b4c9-4aa0-90ab-2408baca9e29/revisions?status=pending HTTP/1.1" 200 OK
2026-01-30 12:29:59,875 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/07352d22-b4c9-4aa0-90ab-2408baca9e29/revisions
INFO:     127.0.0.1:57329 - "GET /api/v1/chapters/07352d22-b4c9-4aa0-90ab-2408baca9e29/revisions?status=pending HTTP/1.1" 200 OK
2026-01-30 12:30:00,056 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/2edba307-74c5-40ab-aa48-84396f47c759
INFO:     127.0.0.1:59160 - "GET /api/v1/agent/operations/2edba307-74c5-40ab-aa48-84396f47c759 HTTP/1.1" 200 OK
2026-01-30 12:30:00,077 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/2edba307-74c5-40ab-aa48-84396f47c759
INFO:     127.0.0.1:53433 - "GET /api/v1/agent/operations/2edba307-74c5-40ab-aa48-84396f47c759 HTTP/1.1" 200 OK
2026-01-30 12:30:00,101 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-30 12:30:02,226 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:832d8d96-080d-4d14-bcc6-80a23ffafa0e
2026-01-30 12:30:02,227 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/07352d22-b4c9-4aa0-90ab-2408baca9e29
INFO:     127.0.0.1:59161 - "PUT /api/v1/chapters/07352d22-b4c9-4aa0-90ab-2408baca9e29 HTTP/1.1" 200 OK
2026-01-30 12:30:02,234 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
2026-01-30 12:30:02,305 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-30 12:30:04,336 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:832d8d96-080d-4d14-bcc6-80a23ffafa0e
2026-01-30 12:30:04,338 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/07352d22-b4c9-4aa0-90ab-2408baca9e29
INFO:     127.0.0.1:56352 - "PUT /api/v1/chapters/07352d22-b4c9-4aa0-90ab-2408baca9e29 HTTP/1.1" 200 OK
2026-01-30 12:30:04,344 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
2026-01-30 12:30:16,020 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 832d8d96-080d-4d14-bcc6-80a23ffafa0e, chapter_id: 4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469
2026-01-30 12:30:16,025 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469
2026-01-30 12:30:16,027 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: 011f4c78-04f0-40f6-99e5-97de0582c58f
2026-01-30 12:30:16,029 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-30 12:30:16,035 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:50372 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-30 12:30:16,051 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 832d8d96-080d-4d14-bcc6-80a23ffafa0e, chapter_id: 4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469
2026-01-30 12:30:16,057 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469
2026-01-30 12:30:16,059 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469/revisions
2026-01-30 12:30:16,061 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: 011f4c78-04f0-40f6-99e5-97de0582c58f
2026-01-30 12:30:16,063 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
INFO:     127.0.0.1:56633 - "GET /api/v1/chapters/4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469/revisions?status=pending HTTP/1.1" 200 OK
2026-01-30 12:30:16,069 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:56631 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-30 12:30:16,086 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469/revisions
INFO:     127.0.0.1:53680 - "GET /api/v1/chapters/4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469/revisions?status=pending HTTP/1.1" 200 OK
2026-01-30 12:30:16,137 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第3章 一夕千悟 (order=3)
2026-01-30 12:30:18,347 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:832d8d96-080d-4d14-bcc6-80a23ffafa0e
2026-01-30 12:30:18,349 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第3章 一夕千悟 (64 paragraphs)
2026-01-30 12:30:18,351 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469
INFO:     127.0.0.1:52074 - "PUT /api/v1/chapters/4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469 HTTP/1.1" 200 OK
2026-01-30 12:30:18,399 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第3章 一夕千悟 (order=3)
2026-01-30 12:30:20,548 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:832d8d96-080d-4d14-bcc6-80a23ffafa0e
2026-01-30 12:30:20,549 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469
INFO:     127.0.0.1:57237 - "PUT /api/v1/chapters/4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469 HTTP/1.1" 200 OK
2026-01-30 12:30:20,557 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第3章 一夕千悟 (64 paragraphs)
2026-01-30 12:31:43,470 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 832d8d96-080d-4d14-bcc6-80a23ffafa0e, chapter_id: 07352d22-b4c9-4aa0-90ab-2408baca9e29
2026-01-30 12:31:43,479 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 07352d22-b4c9-4aa0-90ab-2408baca9e29
2026-01-30 12:31:43,481 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
2026-01-30 12:31:43,491 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:62800 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-30 12:31:43,525 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 832d8d96-080d-4d14-bcc6-80a23ffafa0e, chapter_id: 07352d22-b4c9-4aa0-90ab-2408baca9e29
2026-01-30 12:31:43,533 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 07352d22-b4c9-4aa0-90ab-2408baca9e29
2026-01-30 12:31:43,533 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
2026-01-30 12:31:43,535 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:54415 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-30 12:31:43,539 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/07352d22-b4c9-4aa0-90ab-2408baca9e29/revisions
INFO:     127.0.0.1:54416 - "GET /api/v1/chapters/07352d22-b4c9-4aa0-90ab-2408baca9e29/revisions?status=pending HTTP/1.1" 200 OK
2026-01-30 12:31:43,561 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/07352d22-b4c9-4aa0-90ab-2408baca9e29/revisions
INFO:     127.0.0.1:60024 - "GET /api/v1/chapters/07352d22-b4c9-4aa0-90ab-2408baca9e29/revisions?status=pending HTTP/1.1" 200 OK
2026-01-30 12:31:43,771 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/2edba307-74c5-40ab-aa48-84396f47c759
INFO:     127.0.0.1:59387 - "GET /api/v1/agent/operations/2edba307-74c5-40ab-aa48-84396f47c759 HTTP/1.1" 200 OK
2026-01-30 12:31:43,793 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/2edba307-74c5-40ab-aa48-84396f47c759
INFO:     127.0.0.1:61577 - "GET /api/v1/agent/operations/2edba307-74c5-40ab-aa48-84396f47c759 HTTP/1.1" 200 OK
2026-01-30 12:31:43,821 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-30 12:31:45,822 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:832d8d96-080d-4d14-bcc6-80a23ffafa0e
2026-01-30 12:31:45,826 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/07352d22-b4c9-4aa0-90ab-2408baca9e29
INFO:     127.0.0.1:59388 - "PUT /api/v1/chapters/07352d22-b4c9-4aa0-90ab-2408baca9e29 HTTP/1.1" 200 OK
2026-01-30 12:31:45,831 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
2026-01-30 12:31:45,899 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-30 12:31:48,132 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:832d8d96-080d-4d14-bcc6-80a23ffafa0e
2026-01-30 12:31:48,139 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/07352d22-b4c9-4aa0-90ab-2408baca9e29
2026-01-30 12:31:48,140 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
INFO:     127.0.0.1:50404 - "PUT /api/v1/chapters/07352d22-b4c9-4aa0-90ab-2408baca9e29 HTTP/1.1" 200 OK
2026-01-30 12:32:02,442 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 832d8d96-080d-4d14-bcc6-80a23ffafa0e, chapter_id: 4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469
2026-01-30 12:32:02,452 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469
2026-01-30 12:32:02,455 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: 011f4c78-04f0-40f6-99e5-97de0582c58f
2026-01-30 12:32:02,456 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-30 12:32:02,462 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:61235 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-30 12:32:02,479 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 832d8d96-080d-4d14-bcc6-80a23ffafa0e, chapter_id: 4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469
2026-01-30 12:32:02,499 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469
2026-01-30 12:32:02,504 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: 011f4c78-04f0-40f6-99e5-97de0582c58f
2026-01-30 12:32:02,504 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-30 12:32:02,506 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469/revisions
2026-01-30 12:32:02,509 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:53650 - "GET /api/v1/chapters/4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469/revisions?status=pending HTTP/1.1" 200 OK
INFO:     127.0.0.1:53649 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-30 12:32:02,528 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469/revisions
INFO:     127.0.0.1:49862 - "GET /api/v1/chapters/4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469/revisions?status=pending HTTP/1.1" 200 OK
2026-01-30 12:32:02,580 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第3章 一夕千悟 (order=3)
2026-01-30 12:32:04,570 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第3章 一夕千悟 (64 paragraphs)
2026-01-30 12:32:04,580 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:832d8d96-080d-4d14-bcc6-80a23ffafa0e
2026-01-30 12:32:04,580 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469
INFO:     127.0.0.1:50606 - "PUT /api/v1/chapters/4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469 HTTP/1.1" 200 OK
2026-01-30 12:32:04,634 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第3章 一夕千悟 (order=3)
2026-01-30 12:32:06,628 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第3章 一夕千悟 (64 paragraphs)
2026-01-30 12:32:06,638 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:832d8d96-080d-4d14-bcc6-80a23ffafa0e
2026-01-30 12:32:06,643 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469
INFO:     127.0.0.1:61300 - "PUT /api/v1/chapters/4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469 HTTP/1.1" 200 OK
2026-01-30 12:33:27,520 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 832d8d96-080d-4d14-bcc6-80a23ffafa0e, chapter_id: 07352d22-b4c9-4aa0-90ab-2408baca9e29
2026-01-30 12:33:27,540 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 07352d22-b4c9-4aa0-90ab-2408baca9e29
2026-01-30 12:33:27,541 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
2026-01-30 12:33:27,545 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:50624 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-30 12:33:27,555 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 832d8d96-080d-4d14-bcc6-80a23ffafa0e, chapter_id: 07352d22-b4c9-4aa0-90ab-2408baca9e29
2026-01-30 12:33:27,589 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 07352d22-b4c9-4aa0-90ab-2408baca9e29
2026-01-30 12:33:27,590 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
2026-01-30 12:33:27,592 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
2026-01-30 12:33:27,593 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/07352d22-b4c9-4aa0-90ab-2408baca9e29/revisions
INFO:     127.0.0.1:52807 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
INFO:     127.0.0.1:49415 - "GET /api/v1/chapters/07352d22-b4c9-4aa0-90ab-2408baca9e29/revisions?status=pending HTTP/1.1" 200 OK
2026-01-30 12:33:27,610 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/07352d22-b4c9-4aa0-90ab-2408baca9e29/revisions
INFO:     127.0.0.1:58233 - "GET /api/v1/chapters/07352d22-b4c9-4aa0-90ab-2408baca9e29/revisions?status=pending HTTP/1.1" 200 OK
2026-01-30 12:33:27,847 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/2edba307-74c5-40ab-aa48-84396f47c759
INFO:     127.0.0.1:50806 - "GET /api/v1/agent/operations/2edba307-74c5-40ab-aa48-84396f47c759 HTTP/1.1" 200 OK
2026-01-30 12:33:27,888 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/2edba307-74c5-40ab-aa48-84396f47c759
INFO:     127.0.0.1:64258 - "GET /api/v1/agent/operations/2edba307-74c5-40ab-aa48-84396f47c759 HTTP/1.1" 200 OK
2026-01-30 12:33:27,901 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-30 12:33:30,079 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:832d8d96-080d-4d14-bcc6-80a23ffafa0e
2026-01-30 12:33:30,084 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/07352d22-b4c9-4aa0-90ab-2408baca9e29
2026-01-30 12:33:30,087 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
INFO:     127.0.0.1:50807 - "PUT /api/v1/chapters/07352d22-b4c9-4aa0-90ab-2408baca9e29 HTTP/1.1" 200 OK
2026-01-30 12:33:30,181 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-30 12:33:32,324 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:832d8d96-080d-4d14-bcc6-80a23ffafa0e
2026-01-30 12:33:32,325 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/07352d22-b4c9-4aa0-90ab-2408baca9e29
INFO:     127.0.0.1:59277 - "PUT /api/v1/chapters/07352d22-b4c9-4aa0-90ab-2408baca9e29 HTTP/1.1" 200 OK
2026-01-30 12:33:32,336 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
2026-01-30 12:34:08,694 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 832d8d96-080d-4d14-bcc6-80a23ffafa0e, chapter_id: 4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469
2026-01-30 12:34:08,700 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469
2026-01-30 12:34:08,703 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: 011f4c78-04f0-40f6-99e5-97de0582c58f
2026-01-30 12:34:08,704 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-30 12:34:08,712 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:56348 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-30 12:34:08,726 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 832d8d96-080d-4d14-bcc6-80a23ffafa0e, chapter_id: 4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469
2026-01-30 12:34:08,735 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469
2026-01-30 12:34:08,737 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469/revisions
2026-01-30 12:34:08,739 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: 011f4c78-04f0-40f6-99e5-97de0582c58f
2026-01-30 12:34:08,739 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
INFO:     127.0.0.1:60141 - "GET /api/v1/chapters/4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469/revisions?status=pending HTTP/1.1" 200 OK
2026-01-30 12:34:08,745 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:60139 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-30 12:34:08,760 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469/revisions
INFO:     127.0.0.1:64983 - "GET /api/v1/chapters/4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469/revisions?status=pending HTTP/1.1" 200 OK
2026-01-30 12:34:08,802 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第3章 一夕千悟 (order=3)
2026-01-30 12:34:10,833 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:832d8d96-080d-4d14-bcc6-80a23ffafa0e
2026-01-30 12:34:10,843 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469
2026-01-30 12:34:10,843 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第3章 一夕千悟 (64 paragraphs)
INFO:     127.0.0.1:63315 - "PUT /api/v1/chapters/4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469 HTTP/1.1" 200 OK
2026-01-30 12:34:10,913 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第3章 一夕千悟 (order=3)
2026-01-30 12:34:12,995 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:832d8d96-080d-4d14-bcc6-80a23ffafa0e
2026-01-30 12:34:12,995 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第3章 一夕千悟 (64 paragraphs)
2026-01-30 12:34:12,996 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469
INFO:     127.0.0.1:59594 - "PUT /api/v1/chapters/4ae9c329-1fd0-4abc-b1d5-8ff0b4f3d469 HTTP/1.1" 200 OK
2026-01-30 12:34:13,467 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 832d8d96-080d-4d14-bcc6-80a23ffafa0e, chapter_id: 011f4c78-04f0-40f6-99e5-97de0582c58f
2026-01-30 12:34:13,482 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 011f4c78-04f0-40f6-99e5-97de0582c58f
2026-01-30 12:34:13,487 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: 07352d22-b4c9-4aa0-90ab-2408baca9e29
2026-01-30 12:34:13,489 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-30 12:34:13,496 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 832d8d96-080d-4d14-bcc6-80a23ffafa0e, chapter_id: 011f4c78-04f0-40f6-99e5-97de0582c58f
2026-01-30 12:34:13,498 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:58776 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-30 12:34:13,509 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 011f4c78-04f0-40f6-99e5-97de0582c58f
2026-01-30 12:34:13,512 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: 07352d22-b4c9-4aa0-90ab-2408baca9e29
2026-01-30 12:34:13,514 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-30 12:34:13,518 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:57522 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-30 12:34:13,519 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/011f4c78-04f0-40f6-99e5-97de0582c58f/revisions
INFO:     127.0.0.1:62075 - "GET /api/v1/chapters/011f4c78-04f0-40f6-99e5-97de0582c58f/revisions?status=pending HTTP/1.1" 200 OK
2026-01-30 12:34:13,597 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:62073 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2026-01-30 12:34:13,650 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/011f4c78-04f0-40f6-99e5-97de0582c58f/revisions
INFO:     127.0.0.1:52689 - "GET /api/v1/chapters/011f4c78-04f0-40f6-99e5-97de0582c58f/revisions?status=pending HTTP/1.1" 200 OK
2026-01-30 12:34:13,656 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第2章 浑圆桩 (order=2)
2026-01-30 12:34:15,490 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第2章 浑圆桩 (65 paragraphs)
2026-01-30 12:34:15,512 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 832d8d96-080d-4d14-bcc6-80a23ffafa0e, chapter_id: 07352d22-b4c9-4aa0-90ab-2408baca9e29
2026-01-30 12:34:15,515 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 832d8d96-080d-4d14-bcc6-80a23ffafa0e, chapter_id: 07352d22-b4c9-4aa0-90ab-2408baca9e29
2026-01-30 12:34:15,521 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/2edba307-74c5-40ab-aa48-84396f47c759
INFO:     127.0.0.1:60661 - "GET /api/v1/agent/operations/2edba307-74c5-40ab-aa48-84396f47c759 HTTP/1.1" 200 OK
2026-01-30 12:34:15,535 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 07352d22-b4c9-4aa0-90ab-2408baca9e29
2026-01-30 12:34:15,535 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
2026-01-30 12:34:15,535 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 07352d22-b4c9-4aa0-90ab-2408baca9e29
2026-01-30 12:34:15,535 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
2026-01-30 12:34:15,538 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/07352d22-b4c9-4aa0-90ab-2408baca9e29/revisions
2026-01-30 12:34:15,546 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:60328 - "GET /api/v1/chapters/07352d22-b4c9-4aa0-90ab-2408baca9e29/revisions?status=pending HTTP/1.1" 200 OK
2026-01-30 12:34:15,548 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:64822 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
INFO:     127.0.0.1:60327 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-30 12:34:15,557 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:832d8d96-080d-4d14-bcc6-80a23ffafa0e
2026-01-30 12:34:15,572 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/011f4c78-04f0-40f6-99e5-97de0582c58f
INFO:     127.0.0.1:57586 - "PUT /api/v1/chapters/011f4c78-04f0-40f6-99e5-97de0582c58f HTTP/1.1" 200 OK
2026-01-30 12:34:15,589 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/2edba307-74c5-40ab-aa48-84396f47c759
2026-01-30 12:34:15,591 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
INFO:     127.0.0.1:58861 - "GET /api/v1/agent/operations/2edba307-74c5-40ab-aa48-84396f47c759 HTTP/1.1" 200 OK
2026-01-30 12:34:17,762 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/07352d22-b4c9-4aa0-90ab-2408baca9e29/revisions
INFO:     127.0.0.1:57385 - "GET /api/v1/chapters/07352d22-b4c9-4aa0-90ab-2408baca9e29/revisions?status=pending HTTP/1.1" 200 OK
2026-01-30 12:34:17,806 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
2026-01-30 12:34:17,816 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:832d8d96-080d-4d14-bcc6-80a23ffafa0e
2026-01-30 12:34:17,820 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/07352d22-b4c9-4aa0-90ab-2408baca9e29
INFO:     127.0.0.1:60662 - "PUT /api/v1/chapters/07352d22-b4c9-4aa0-90ab-2408baca9e29 HTTP/1.1" 200 OK
2026-01-30 12:34:17,851 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第2章 浑圆桩 (order=2)
2026-01-30 12:34:19,792 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第2章 浑圆桩 (65 paragraphs)
2026-01-30 12:34:19,795 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 011f4c78-04f0-40f6-99e5-97de0582c58f 内容更新，新段落数: 65
2026-01-30 12:34:19,827 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-30 12:34:22,552 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:832d8d96-080d-4d14-bcc6-80a23ffafa0e
2026-01-30 12:34:22,555 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/011f4c78-04f0-40f6-99e5-97de0582c58f
INFO:     127.0.0.1:56620 - "PUT /api/v1/chapters/011f4c78-04f0-40f6-99e5-97de0582c58f HTTP/1.1" 200 OK
2026-01-30 12:34:22,563 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
2026-01-30 12:34:22,570 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:832d8d96-080d-4d14-bcc6-80a23ffafa0e
2026-01-30 12:34:22,573 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/07352d22-b4c9-4aa0-90ab-2408baca9e29
INFO:     127.0.0.1:54253 - "PUT /api/v1/chapters/07352d22-b4c9-4aa0-90ab-2408baca9e29 HTTP/1.1" 200 OK
2026-01-30 12:35:24,287 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-30 12:35:24,287 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-30 12:35:24,288 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2026-01-30 12:35:25,895 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz:8443/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-30 12:35:25,895 - app.api.v1.agent - INFO - [Chat Stream] Mode: planning
2026-01-30 12:35:25,895 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:56537 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2026-01-30 12:35:25,910 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 仅第1–2章，分析赵穆对段融的态度与原因，并对孔斌/李充/张征的“区别对待”做证据支撑。
  要求：...
2026-01-30 12:35:25,918 - app.api.v1.agent - INFO - [agent_chat_stream] 📚 世界观数据已注入: 人物=9, 地点=6, 设定=5, 规范=无
2026-01-30 12:35:25,921 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:832d8d96-080d-4d14-bcc6-80a23ffafa0e:2edba307-74c5-40ab-aa48-84396f47c759 (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=832d8d96-080d-4d14-bcc6-80a23ffafa0e, conversation_id=2edba307-74c5-40ab-aa48-84396f47c759)
2026-01-30 12:35:25,928 - app.services.context.store - INFO - [ContextStore] 加载上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:832d8d96-080d-4d14-bcc6-80a23ffafa0e:2edba307-74c5-40ab-aa48-84396f47c759, 4条消息
2026-01-30 12:35:25,930 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:832d8d96-080d-4d14-bcc6-80a23ffafa0e:2edba307-74c5-40ab-aa48-84396f47c759: 2516/16000 tokens
2026-01-30 12:35:26,094 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='仅第1–2章，分析赵穆对段融的态度与原因，并对孔斌/李充/张...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:832d8d96-080d-4d14-bcc6-80a23ffafa0e', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=2条
2026-01-30 12:35:26,094 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=832d8d96-080d-4d14-bcc6-80a23ffafa0e | 含用户级=True | 找到=2条
2026-01-30 12:35:26,135 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 5条消息, 2516 tokens, 耗时 212.74ms
2026-01-30 12:35:26,136 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 5 条历史消息 (token: 2516, has_summary: False)
2026-01-30 12:35:26,136 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-30 12:35:26,136 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-30 12:35:26,136 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=200, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-30 12:35:28,112 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:35:28,112 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-30 12:35:28,130 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:35:28,130 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1854, cost=$0.000191, time=1975ms
2026-01-30 12:35:28,130 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=42, 尝试次数=1
2026-01-30 12:35:28,130 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-30 12:35:28,130 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-30 12:35:28,130 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=20, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-30 12:35:29,097 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:35:29,097 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-30 12:35:29,114 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:35:29,114 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=371, cost=$0.000037, time=967ms
2026-01-30 12:35:29,114 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=8, 尝试次数=1
2026-01-30 12:35:29,114 - app.services.agent.intent.classifier - INFO - [Intent] AI识别结果: analysis
2026-01-30 12:35:29,114 - app.services.agent.langgraph_agent - INFO - [Planning] AI意图分类: analysis (置信度: 0.90)
2026-01-30 12:35:29,114 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 仅第1–2章，分析赵穆对段融的态度与原因，并对孔斌/李充/张征的“区别对待”做证据支撑。
  要求：...
2026-01-30 12:35:29,133 - app.core.cache - INFO - ✅ 缓存命中: prompt:planning:v2.41.0:get_planning_static_prompt:fca6eb91156619d0
2026-01-30 12:35:29,143 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-30 12:35:29,143 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=story_planning, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: story_planning; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-01-30 12:35:29,143 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.3, task_type=TaskType.STORY_PLANNING
2026-01-30 12:35:43,610 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-30 12:35:47,753 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 9 个数据块，总长度: 942
2026-01-30 12:35:47,753 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 23852 (prompt=23369, completion=483)
2026-01-30 12:35:47,753 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:35:47,753 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-30 12:35:47,767 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:35:47,778 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=23852, cost=$0.034041, time=18613ms
2026-01-30 12:35:47,778 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=23852
2026-01-30 12:35:47,778 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户需要一份关于角色态度的分析报告，限定在第1-2章。报告需, 原料=需要读取第1章和第2章中所有涉及“赵穆”, 处理=使用 explore_content 工
2026-01-30 12:35:47,778 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共1个任务
2026-01-30 12:35:47,778 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共1个任务，耗时: 18.66s
2026-01-30 12:35:47,778 - app.api.v1.agent - INFO - [Stream] Plan tasks: 1 items
2026-01-30 12:35:47,778 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2026-01-30 12:35:47,785 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2026-01-30 12:35:47,785 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2026-01-30 12:35:47,787 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] DAG 调度启用，任务数=1, 有依赖任务=0
2026-01-30 12:35:47,787 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1开始: 在第1-2章中，检索所有关于赵穆、段融、孔斌、李充、张征的互动及态度描写的段落。
2026-01-30 12:35:47,787 - app.api.v1.agent - INFO - [Stream] Task started: 在第1-2章中，检索所有关于赵穆、段融、孔斌、李充、张征的互动及态度描写的段落。 (icon=Wrench)
2026-01-30 12:35:47,787 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: explore_content
2026-01-30 12:35:47,787 - app.services.agent.tools.explore_tools - INFO - [explore_content] 开始: work_id=832d8d96-080d-4d14-bcc6-80a23ffafa0e, target=分析赵穆对段融、孔斌、李充、张征的态度及区别对待，限定第1-2章
约束：章节范围：第1–2章、1–2...
2026-01-30 12:35:47,787 - app.services.agent.tools.explore_tools - INFO - [explore_content] 规划传入关键词: ['赵穆', '段融', '孔斌', '李充', '张征']
2026-01-30 12:35:47,787 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 章节范围锁定: 第1-2章
2026-01-30 12:35:47,787 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 开始探索 V5: work_id=832d8d96-080d-4d14-bcc6-80a23ffafa0e, target=分析赵穆对段融、孔斌、李充、张征的态度及区别对待，限定第1-2章
约束：章节范围：第1–2章、1–2...
2026-01-30 12:35:47,793 - app.services.chapter_service - INFO - [ChapterService] Querying chapters for work_id=832d8d96-080d-4d14-bcc6-80a23ffafa0e, type=<class 'uuid.UUID'>
2026-01-30 12:35:47,798 - app.services.chapter_service - INFO - [ChapterService] Found 5 chapters
2026-01-30 12:35:47,798 - app.services.chapter_service - INFO -   - Chapter: 第1章 吞噬, order=1
2026-01-30 12:35:47,798 - app.services.chapter_service - INFO -   - ... (3 more chapters)
2026-01-30 12:35:47,798 - app.services.chapter_service - INFO -   - Chapter: 第5章 太一门, order=5
2026-01-30 12:35:47,863 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 章节范围映射: 第1-2章 -> 第1-2章
2026-01-30 12:35:47,869 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 自动获取世界观...
2026-01-30 12:35:47,880 - app.services.agent.langgraph_tools - INFO - [get_writing_context] ✅ 获取创作上下文成功: include=worldview
2026-01-30 12:35:47,882 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 世界观获取完成: 20 条
2026-01-30 12:35:47,882 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:35:47,883 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=80, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:35:50,479 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:35:50,479 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:35:50,498 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:35:50,501 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=278, cost=$0.000123, time=2595ms
2026-01-30 12:35:50,502 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=24, 尝试次数=1
2026-01-30 12:35:50,503 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 强制流程步骤: list_chapters
2026-01-30 12:35:50,503 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=list_chapters params={"work_id": "832d8d96-080d-4d14-bcc6-80a23ffafa0e"}
2026-01-30 12:35:50,503 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=list_chapters success=True count=2
2026-01-30 12:35:50,503 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:35:50,503 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=80, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:35:54,161 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:35:54,162 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:35:54,180 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:35:54,185 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=531, cost=$0.000188, time=3660ms
2026-01-30 12:35:54,186 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=19, 尝试次数=1
2026-01-30 12:35:54,186 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 强制流程步骤: list_paragraphs
2026-01-30 12:35:54,186 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=list_paragraphs params={"chapter_order": 1, "offset": 0, "limit": 50, "preview_len": 80, "work_id": "832d8d96-080d-4d14-bcc6-80a23ffafa0e"}
2026-01-30 12:35:54,219 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=list_paragraphs success=True chapter=1 offset=0 limit=50 approximate=None
2026-01-30 12:35:54,223 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:35:54,223 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:35:56,716 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:35:56,716 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:35:56,734 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:35:56,741 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1621, cost=$0.000706, time=2495ms
2026-01-30 12:35:56,741 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=214, 尝试次数=1
2026-01-30 12:35:56,742 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"keywords": "赵穆", "match_mode": "keywords", "limit": 50, "work_id": "832d8d96-080d-4d14-bcc6-80a23ffafa0e"}
2026-01-30 12:35:56,743 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 世界观匹配: 1 条
2026-01-30 12:35:56,774 - app.services.chapter_vector_service - INFO - [exact_search] work=832d8d96-080d-4d14-bcc6-80a23ffafa0e, keywords=['赵穆']..., mode=any, range=(1, 2), hits=32
2026-01-30 12:35:56,784 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=55 corrected=False final=55
2026-01-30 12:35:56,786 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第55段
2026-01-30 12:35:56,797 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=57 corrected=False final=57
2026-01-30 12:35:56,797 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第57段
2026-01-30 12:35:56,802 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=59 corrected=False final=59
2026-01-30 12:35:56,802 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第59段
2026-01-30 12:35:56,817 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=60 corrected=False final=60
2026-01-30 12:35:56,818 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第60段
2026-01-30 12:35:56,828 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=61 corrected=False final=61
2026-01-30 12:35:56,828 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第61段
2026-01-30 12:35:56,835 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=63 corrected=False final=63
2026-01-30 12:35:56,835 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第63段
2026-01-30 12:35:56,842 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=66 corrected=False final=66
2026-01-30 12:35:56,842 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第66段
2026-01-30 12:35:56,856 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=0 corrected=False final=0
2026-01-30 12:35:56,856 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第0段
2026-01-30 12:35:56,862 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=1 corrected=False final=1
2026-01-30 12:35:56,867 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第1段
2026-01-30 12:35:56,871 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=2 corrected=False final=2
2026-01-30 12:35:56,876 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第2段
2026-01-30 12:35:56,885 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=4 corrected=False final=4
2026-01-30 12:35:56,886 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第4段
2026-01-30 12:35:56,896 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=8 corrected=False final=8
2026-01-30 12:35:56,897 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第8段
2026-01-30 12:35:56,903 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=9 corrected=False final=9
2026-01-30 12:35:56,903 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第9段
2026-01-30 12:35:56,914 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=10 corrected=False final=10
2026-01-30 12:35:56,914 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第10段
2026-01-30 12:35:56,924 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=11 corrected=False final=11
2026-01-30 12:35:56,925 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第11段
2026-01-30 12:35:56,934 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=12 corrected=False final=12
2026-01-30 12:35:56,936 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第12段
2026-01-30 12:35:56,943 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=13 corrected=False final=13
2026-01-30 12:35:56,943 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第13段
2026-01-30 12:35:56,951 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=14 corrected=False final=14
2026-01-30 12:35:56,956 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第14段
2026-01-30 12:35:56,965 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=16 corrected=False final=16
2026-01-30 12:35:56,965 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第16段
2026-01-30 12:35:56,972 - app.services.agent.langgraph_tools - INFO - [read_paragraph] index_base=zero assumed=zero original=18 corrected=False final=18
2026-01-30 12:35:56,972 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第18段
2026-01-30 12:35:56,976 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=33 (chapter=32, worldview=1) keywords=赵穆
2026-01-30 12:35:56,976 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:35:56,977 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:36:03,579 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:36:03,581 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:36:03,589 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:36:03,597 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=6164, cost=$0.002034, time=6604ms
2026-01-30 12:36:03,597 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=128, 尝试次数=1
2026-01-30 12:36:03,599 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:36:03,599 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=200, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:36:08,933 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:36:08,933 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:36:08,951 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:36:08,951 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1569, cost=$0.000651, time=5335ms
2026-01-30 12:36:08,951 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=106, 尝试次数=1
2026-01-30 12:36:08,951 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 探索完成(工具循环): 3轮, 原因=已收集到足够信息来分析赵穆对段融、孔斌、李充、张征的态度及区别对待。证据表明赵穆对段融态度恶劣、轻视且带有偏见，而对孔斌、李充、张征则表现出重视和重点培养。
2026-01-30 12:36:08,958 - app.services.agent.execution.tool_executor - INFO - [StandardTool] explore_content 执行成功
2026-01-30 12:36:08,961 - app.api.v1.agent - INFO - [Stream] 任务完成: 在第1-2章中，检索所有关于赵穆、段融、孔斌、李充、张征的互动及态度描写的段落。 (21.2s)
2026-01-30 12:36:08,961 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1完成
2026-01-30 12:36:08,961 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共1个任务，耗时: 21.18s
2026-01-30 12:36:08,961 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2026-01-30 12:36:08,961 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=1, 展示型=0
2026-01-30 12:36:08,966 - app.services.agent.langgraph_agent - INFO - [Response] 单个输出任务(explore_content)，使用AI整合
2026-01-30 12:36:08,966 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2026-01-30 12:36:08,967 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=1, 展示型=0
2026-01-30 12:36:08,968 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=2368字符, 处理后=2413字符
2026-01-30 12:36:08,968 - app.services.agent.planning.response_builder - INFO - [Summarization] 准备发送 summarization_start 事件
2026-01-30 12:36:08,968 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-30 12:36:08,968 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-30 12:36:08,968 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=60, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:36:10,699 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:36:10,702 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-30 12:36:10,715 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:36:10,720 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=279, cost=$0.000038, time=1733ms
2026-01-30 12:36:10,721 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=43, 尝试次数=1
2026-01-30 12:36:10,721 - app.services.agent.planning.response_builder - INFO - [Summarization] reason生成: len=43 content=赵穆对段融态度温和，因其是“自己人”，而对孔斌、李充、张征则区别对待，显示出等级差异。
2026-01-30 12:36:10,722 - app.services.agent.stream.stream_event_handler - INFO - [StreamEventHandler] emit_summarization_start 被调用, _on_flow_event=True, reason_len=43, reason=赵穆对段融态度温和，因其是“自己人”，而对孔斌、李充、张征则区别对待，显示出等级差异。
2026-01-30 12:36:10,722 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_start 事件已发送
2026-01-30 12:36:10,722 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2026-01-30 12:36:10,722 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2026-01-30 12:36:10,730 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-30 12:36:10,730 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-30 12:36:10,730 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=20000, temp=0.7, task_type=TaskType.SUMMARIZATION
2026-01-30 12:36:28,698 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-30 12:36:28,698 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_complete 事件已发送（第一个chunk时）
2026-01-30 12:36:28,698 - app.services.agent.planning.response_builder - INFO - [Summarization] output_ready 事件已发送（第一个chunk时）
2026-01-30 12:36:30,729 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 9 个数据块，总长度: 685
2026-01-30 12:36:30,729 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 8328 (prompt=7833, completion=495)
2026-01-30 12:36:30,729 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:36:30,729 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-30 12:36:30,743 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:36:30,747 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=8328, cost=$0.003587, time=20001ms
2026-01-30 12:36:30,749 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=685
2026-01-30 12:36:30,754 - app.services.context.vector_memory_store - INFO - 🔁 跳过重复记忆，复用ID=79913e7e-d5cd-4e09-bce6-ca6639bd8456_1769698913413_aaa0d9e3
2026-01-30 12:36:30,754 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:832d8d96-080d-4d14-bcc6-80a23ffafa0e | 重要度=0.82
2026-01-30 12:36:31,319 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:832d8d96-080d-4d14-bcc6-80a23ffafa0e | 重要度=0.68
2026-01-30 12:36:31,330 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:832d8d96-080d-4d14-bcc6-80a23ffafa0e:2edba307-74c5-40ab-aa48-84396f47c759, token=3400
2026-01-30 12:36:31,332 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:832d8d96-080d-4d14-bcc6-80a23ffafa0e:2edba307-74c5-40ab-aa48-84396f47c759, 消息数=6, 摘要长度=0, Token=3400
2026-01-30 12:36:31,332 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:832d8d96-080d-4d14-bcc6-80a23ffafa0e:2edba307-74c5-40ab-aa48-84396f47c759)
2026-01-30 12:36:31,332 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2026-01-30 12:36:31,341 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed
2026-01-30 12:36:40,580 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/2edba307-74c5-40ab-aa48-84396f47c759
INFO:     127.0.0.1:59931 - "GET /api/v1/agent/operations/2edba307-74c5-40ab-aa48-84396f47c759 HTTP/1.1" 200 OK
2026-01-30 12:38:36,843 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 832d8d96-080d-4d14-bcc6-80a23ffafa0e, chapter_id: 011f4c78-04f0-40f6-99e5-97de0582c58f
2026-01-30 12:38:36,854 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 832d8d96-080d-4d14-bcc6-80a23ffafa0e, chapter_id: 011f4c78-04f0-40f6-99e5-97de0582c58f
2026-01-30 12:38:36,878 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 011f4c78-04f0-40f6-99e5-97de0582c58f
2026-01-30 12:38:36,881 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: 07352d22-b4c9-4aa0-90ab-2408baca9e29
2026-01-30 12:38:36,881 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-30 12:38:36,884 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
2026-01-30 12:38:36,885 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 011f4c78-04f0-40f6-99e5-97de0582c58f
INFO:     127.0.0.1:59664 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-30 12:38:36,892 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: 07352d22-b4c9-4aa0-90ab-2408baca9e29
2026-01-30 12:38:36,892 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-30 12:38:36,892 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:57344 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-30 12:38:36,909 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/011f4c78-04f0-40f6-99e5-97de0582c58f/revisions
INFO:     127.0.0.1:59665 - "GET /api/v1/chapters/011f4c78-04f0-40f6-99e5-97de0582c58f/revisions?status=pending HTTP/1.1" 200 OK
2026-01-30 12:38:37,197 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第2章 浑圆桩 (order=2)
2026-01-30 12:38:39,022 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/011f4c78-04f0-40f6-99e5-97de0582c58f/revisions
INFO:     127.0.0.1:51531 - "GET /api/v1/chapters/011f4c78-04f0-40f6-99e5-97de0582c58f/revisions?status=pending HTTP/1.1" 200 OK
2026-01-30 12:38:39,048 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:832d8d96-080d-4d14-bcc6-80a23ffafa0e
2026-01-30 12:38:39,049 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第2章 浑圆桩 (65 paragraphs)
2026-01-30 12:38:39,052 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/011f4c78-04f0-40f6-99e5-97de0582c58f
INFO:     127.0.0.1:65129 - "PUT /api/v1/chapters/011f4c78-04f0-40f6-99e5-97de0582c58f HTTP/1.1" 200 OK
2026-01-30 12:38:39,118 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第2章 浑圆桩 (order=2)
2026-01-30 12:38:41,105 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第2章 浑圆桩 (65 paragraphs)
2026-01-30 12:38:41,113 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:832d8d96-080d-4d14-bcc6-80a23ffafa0e
2026-01-30 12:38:41,123 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/011f4c78-04f0-40f6-99e5-97de0582c58f
INFO:     127.0.0.1:58968 - "PUT /api/v1/chapters/011f4c78-04f0-40f6-99e5-97de0582c58f HTTP/1.1" 200 OK
2026-01-30 12:39:27,306 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 832d8d96-080d-4d14-bcc6-80a23ffafa0e, chapter_id: 07352d22-b4c9-4aa0-90ab-2408baca9e29
2026-01-30 12:39:27,337 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 07352d22-b4c9-4aa0-90ab-2408baca9e29
2026-01-30 12:39:27,337 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
2026-01-30 12:39:27,345 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 832d8d96-080d-4d14-bcc6-80a23ffafa0e, chapter_id: 07352d22-b4c9-4aa0-90ab-2408baca9e29
2026-01-30 12:39:27,349 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:60337 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-30 12:39:27,367 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 07352d22-b4c9-4aa0-90ab-2408baca9e29
2026-01-30 12:39:27,367 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
2026-01-30 12:39:27,372 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:62920 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-30 12:39:27,378 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/07352d22-b4c9-4aa0-90ab-2408baca9e29/revisions
INFO:     127.0.0.1:62921 - "GET /api/v1/chapters/07352d22-b4c9-4aa0-90ab-2408baca9e29/revisions?status=pending HTTP/1.1" 200 OK
2026-01-30 12:39:27,426 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/07352d22-b4c9-4aa0-90ab-2408baca9e29/revisions
INFO:     127.0.0.1:62678 - "GET /api/v1/chapters/07352d22-b4c9-4aa0-90ab-2408baca9e29/revisions?status=pending HTTP/1.1" 200 OK
2026-01-30 12:39:27,666 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/2edba307-74c5-40ab-aa48-84396f47c759
INFO:     127.0.0.1:62211 - "GET /api/v1/agent/operations/2edba307-74c5-40ab-aa48-84396f47c759 HTTP/1.1" 200 OK
2026-01-30 12:39:27,693 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/2edba307-74c5-40ab-aa48-84396f47c759
INFO:     127.0.0.1:52928 - "GET /api/v1/agent/operations/2edba307-74c5-40ab-aa48-84396f47c759 HTTP/1.1" 200 OK
2026-01-30 12:39:27,718 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-30 12:39:29,784 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
2026-01-30 12:39:29,799 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:832d8d96-080d-4d14-bcc6-80a23ffafa0e
2026-01-30 12:39:29,802 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/07352d22-b4c9-4aa0-90ab-2408baca9e29
INFO:     127.0.0.1:62213 - "PUT /api/v1/chapters/07352d22-b4c9-4aa0-90ab-2408baca9e29 HTTP/1.1" 200 OK
2026-01-30 12:39:29,883 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-30 12:39:32,053 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:832d8d96-080d-4d14-bcc6-80a23ffafa0e
2026-01-30 12:39:32,055 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/07352d22-b4c9-4aa0-90ab-2408baca9e29
INFO:     127.0.0.1:63303 - "PUT /api/v1/chapters/07352d22-b4c9-4aa0-90ab-2408baca9e29 HTTP/1.1" 200 OK
2026-01-30 12:39:32,075 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
2026-01-30 12:40:15,541 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-30 12:40:15,542 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-30 12:40:15,542 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2026-01-30 12:40:17,112 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz:8443/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-30 12:40:17,112 - app.api.v1.agent - INFO - [Chat Stream] Mode: planning
2026-01-30 12:40:17,119 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:54037 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2026-01-30 12:40:17,129 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 限定第2–3章，梳理因果链：
  “脑子被塞进一团东西”→“梦中悟刀”→“醒后练刀”→“身体限制”→...
2026-01-30 12:40:17,146 - app.api.v1.agent - INFO - [agent_chat_stream] 📚 世界观数据已注入: 人物=9, 地点=6, 设定=5, 规范=无
2026-01-30 12:40:17,146 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:832d8d96-080d-4d14-bcc6-80a23ffafa0e:2edba307-74c5-40ab-aa48-84396f47c759 (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=832d8d96-080d-4d14-bcc6-80a23ffafa0e, conversation_id=2edba307-74c5-40ab-aa48-84396f47c759)
2026-01-30 12:40:17,150 - app.services.context.store - INFO - [ContextStore] 加载上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:832d8d96-080d-4d14-bcc6-80a23ffafa0e:2edba307-74c5-40ab-aa48-84396f47c759, 6条消息
2026-01-30 12:40:17,156 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:832d8d96-080d-4d14-bcc6-80a23ffafa0e:2edba307-74c5-40ab-aa48-84396f47c759: 3400/16000 tokens
2026-01-30 12:40:17,328 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='限定第2–3章，梳理因果链：
  “脑子被塞进一团东西”→“...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:832d8d96-080d-4d14-bcc6-80a23ffafa0e', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=3条
2026-01-30 12:40:17,329 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=832d8d96-080d-4d14-bcc6-80a23ffafa0e | 含用户级=True | 找到=3条
2026-01-30 12:40:17,418 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 7条消息, 3400 tokens, 耗时 272.29ms
2026-01-30 12:40:17,418 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 7 条历史消息 (token: 3400, has_summary: False)
2026-01-30 12:40:17,419 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-30 12:40:17,419 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-30 12:40:17,420 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=200, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-30 12:40:19,105 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:40:19,107 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-30 12:40:19,130 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:40:19,132 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1878, cost=$0.000193, time=1687ms
2026-01-30 12:40:19,133 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=39, 尝试次数=1
2026-01-30 12:40:19,133 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-30 12:40:19,135 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-30 12:40:19,135 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=20, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-30 12:40:20,527 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:40:20,528 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-30 12:40:20,558 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:40:20,563 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=390, cost=$0.000039, time=1393ms
2026-01-30 12:40:20,563 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=8, 尝试次数=1
2026-01-30 12:40:20,564 - app.services.agent.intent.classifier - INFO - [Intent] AI识别结果: analysis
2026-01-30 12:40:20,564 - app.services.agent.langgraph_agent - INFO - [Planning] AI意图分类: analysis (置信度: 0.90)
2026-01-30 12:40:20,564 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 限定第2–3章，梳理因果链：
  “脑子被塞进一团东西”→“梦中悟刀”→“醒后练刀”→“身体限制”→...
2026-01-30 12:40:20,577 - app.core.cache - INFO - ✅ 缓存命中: prompt:planning:v2.41.0:get_planning_static_prompt:fca6eb91156619d0
2026-01-30 12:40:20,583 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-30 12:40:20,584 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=story_planning, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: story_planning; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-01-30 12:40:20,584 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.3, task_type=TaskType.STORY_PLANNING
2026-01-30 12:40:43,140 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-30 12:40:47,462 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 9 个数据块，总长度: 996
2026-01-30 12:40:47,462 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 25411 (prompt=24866, completion=545)
2026-01-30 12:40:47,462 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:40:47,462 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-30 12:40:47,488 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:40:47,488 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=25411, cost=$0.036532, time=26880ms
2026-01-30 12:40:47,488 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=25411
2026-01-30 12:40:47,488 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户要求梳理一个跨越第2章和第3章的完整因果链，并为链条中的, 原料=需要读取第2章和第3章中与因果链各环节相, 处理=使用 explore_content 工
2026-01-30 12:40:47,498 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共1个任务
2026-01-30 12:40:47,498 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共1个任务，耗时: 26.93s
2026-01-30 12:40:47,498 - app.api.v1.agent - INFO - [Stream] Plan tasks: 1 items
2026-01-30 12:40:47,498 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2026-01-30 12:40:47,500 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2026-01-30 12:40:47,500 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2026-01-30 12:40:47,500 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] DAG 调度启用，任务数=1, 有依赖任务=0
2026-01-30 12:40:47,500 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1开始: 在第2章和第3章中，检索与因果链“‘脑子被塞进一团东西’→‘梦中悟刀’→‘醒后练刀’→‘身体限制’→‘改用站桩尝试内息’”相关的原文段落。
2026-01-30 12:40:47,502 - app.api.v1.agent - INFO - [Stream] Task started: 在第2章和第3章中，检索与因果链“‘脑子被塞进一团东西’→‘梦中悟刀’→‘醒后练刀’→‘身体限制’→‘改用站桩尝试内息’”相关的原文段落。 (icon=Wrench)
2026-01-30 12:40:47,502 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: explore_content
2026-01-30 12:40:47,502 - app.services.agent.tools.explore_tools - INFO - [explore_content] 开始: work_id=832d8d96-080d-4d14-bcc6-80a23ffafa0e, target=在第2章和第3章中，检索与因果链“‘脑子被塞进一团东西’→‘梦中悟刀’→‘醒后练刀’→‘身体限制’→...
2026-01-30 12:40:47,502 - app.services.agent.tools.explore_tools - INFO - [explore_content] 规划传入关键词: ['塞进', '一夕千悟', '演练', '身体素质', '身体跟不上', '站桩', '内息']
2026-01-30 12:40:47,502 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 启用严格段落号模式
2026-01-30 12:40:47,502 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 章节范围锁定: 第2-3章
2026-01-30 12:40:47,502 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 任务禁止整章阅读
2026-01-30 12:40:47,502 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 开始探索 V5: work_id=832d8d96-080d-4d14-bcc6-80a23ffafa0e, target=在第2章和第3章中，检索与因果链“‘脑子被塞进一团东西’→‘梦中悟刀’→‘醒后练刀’→‘身体限制’→...
2026-01-30 12:40:47,502 - app.services.chapter_service - INFO - [ChapterService] Querying chapters for work_id=832d8d96-080d-4d14-bcc6-80a23ffafa0e, type=<class 'uuid.UUID'>
2026-01-30 12:40:47,511 - app.services.chapter_service - INFO - [ChapterService] Found 5 chapters
2026-01-30 12:40:47,511 - app.services.chapter_service - INFO -   - Chapter: 第1章 吞噬, order=1
2026-01-30 12:40:47,511 - app.services.chapter_service - INFO -   - ... (3 more chapters)
2026-01-30 12:40:47,511 - app.services.chapter_service - INFO -   - Chapter: 第5章 太一门, order=5
2026-01-30 12:40:47,550 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 章节范围映射: 第2-3章 -> 第2-3章
2026-01-30 12:40:47,564 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 自动获取世界观...
2026-01-30 12:40:47,585 - app.services.agent.langgraph_tools - INFO - [get_writing_context] ✅ 获取创作上下文成功: include=worldview
2026-01-30 12:40:47,585 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 世界观获取完成: 20 条
2026-01-30 12:40:47,585 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:40:47,585 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=80, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:40:52,702 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:40:52,702 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:40:52,716 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:40:52,718 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=660, cost=$0.000209, time=5118ms
2026-01-30 12:40:52,718 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=9, 尝试次数=1
2026-01-30 12:40:52,720 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 强制流程步骤: list_chapters
2026-01-30 12:40:52,720 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=list_chapters params={"work_id": "832d8d96-080d-4d14-bcc6-80a23ffafa0e"}
2026-01-30 12:40:52,722 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=list_chapters success=True count=2
2026-01-30 12:40:52,723 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:40:52,723 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=80, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:40:58,254 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:40:58,254 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:40:58,263 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:40:58,265 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1054, cost=$0.000343, time=5531ms
2026-01-30 12:40:58,266 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=15, 尝试次数=1
2026-01-30 12:40:58,266 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 强制流程步骤: list_paragraphs
2026-01-30 12:40:58,266 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=list_paragraphs params={"chapter_order": 2, "offset": 0, "limit": 50, "preview_len": 80, "work_id": "832d8d96-080d-4d14-bcc6-80a23ffafa0e"}
2026-01-30 12:40:58,271 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=list_paragraphs success=True chapter=2 offset=0 limit=50 approximate=None
2026-01-30 12:40:58,271 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:40:58,271 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:41:02,743 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:41:02,743 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:41:02,764 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:41:02,764 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2028, cost=$0.000846, time=4471ms
2026-01-30 12:41:02,764 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=218, 尝试次数=1
2026-01-30 12:41:02,764 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"keywords": "脑子被塞", "match_mode": "all", "limit": 100, "work_id": "832d8d96-080d-4d14-bcc6-80a23ffafa0e"}
2026-01-30 12:41:02,798 - app.services.chapter_vector_service - INFO - [exact_search] work=832d8d96-080d-4d14-bcc6-80a23ffafa0e, keywords=['脑子被塞']..., mode=all, range=(2, 3), hits=0
2026-01-30 12:41:02,800 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=0 (chapter=0, worldview=0) keywords=脑子被塞
2026-01-30 12:41:02,800 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:41:02,800 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:41:05,212 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:41:05,212 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:41:05,222 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:41:05,222 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1137, cost=$0.000559, time=2412ms
2026-01-30 12:41:05,222 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=209, 尝试次数=1
2026-01-30 12:41:05,222 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"keywords": ["梦中悟刀"], "match_mode": "all", "limit": 50, "work_id": "832d8d96-080d-4d14-bcc6-80a23ffafa0e"}
2026-01-30 12:41:05,237 - app.services.chapter_vector_service - INFO - [exact_search] work=832d8d96-080d-4d14-bcc6-80a23ffafa0e, keywords=['梦中悟刀']..., mode=all, range=(2, 3), hits=0
2026-01-30 12:41:05,239 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=0 (chapter=0, worldview=0) keywords=梦中悟刀
2026-01-30 12:41:05,239 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:41:05,239 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:41:09,497 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:41:09,497 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:41:09,506 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:41:09,506 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1270, cost=$0.000636, time=4259ms
2026-01-30 12:41:09,507 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=234, 尝试次数=1
2026-01-30 12:41:09,507 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"keywords": ["醒后练刀"], "match_mode": "all", "limit": 10, "work_id": "832d8d96-080d-4d14-bcc6-80a23ffafa0e"}
2026-01-30 12:41:09,508 - app.services.chapter_vector_service - INFO - [exact_search] work=832d8d96-080d-4d14-bcc6-80a23ffafa0e, keywords=['醒后练刀']..., mode=all, range=(2, 3), hits=0
2026-01-30 12:41:09,513 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=0 (chapter=0, worldview=0) keywords=醒后练刀
2026-01-30 12:41:09,513 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:41:09,513 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:41:11,147 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:41:11,147 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:41:11,173 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:41:11,173 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1071, cost=$0.000517, time=1636ms
2026-01-30 12:41:11,176 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=202, 尝试次数=1
2026-01-30 12:41:11,176 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"keywords": ["身体限制"], "match_mode": "all", "limit": 100, "work_id": "832d8d96-080d-4d14-bcc6-80a23ffafa0e"}
2026-01-30 12:41:11,185 - app.services.chapter_vector_service - INFO - [exact_search] work=832d8d96-080d-4d14-bcc6-80a23ffafa0e, keywords=['身体限制']..., mode=all, range=(2, 3), hits=0
2026-01-30 12:41:11,185 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=0 (chapter=0, worldview=0) keywords=身体限制
2026-01-30 12:41:11,194 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:41:11,194 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:41:13,258 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:41:13,258 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:41:13,275 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:41:13,275 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1159, cost=$0.000587, time=2063ms
2026-01-30 12:41:13,275 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=221, 尝试次数=1
2026-01-30 12:41:13,282 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] call=exact_search_paragraphs params={"keywords": ["改用站桩尝试内息"], "match_mode": "exact", "limit": 100, "work_id": "832d8d96-080d-4d14-bcc6-80a23ffafa0e"}
2026-01-30 12:41:13,308 - app.services.chapter_vector_service - INFO - [exact_search] work=832d8d96-080d-4d14-bcc6-80a23ffafa0e, keywords=['改用站桩尝试内息']..., mode=any, range=(2, 3), hits=0
2026-01-30 12:41:13,311 - app.services.agent.tools.explore_tools - INFO - [ExploreTool] done=exact_search_paragraphs success=True hits=0 (chapter=0, worldview=0) keywords=改用站桩尝试内息
2026-01-30 12:41:13,311 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:41:13,311 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:41:20,676 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:41:20,676 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:41:20,695 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:41:20,695 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1985, cost=$0.000743, time=7365ms
2026-01-30 12:41:20,695 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=123, 尝试次数=1
2026-01-30 12:41:20,695 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: gemini-2.5-flash
2026-01-30 12:41:20,705 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=200, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:41:24,221 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:41:24,222 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-flash)
2026-01-30 12:41:24,230 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:41:24,232 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=679, cost=$0.000287, time=3517ms
2026-01-30 12:41:24,232 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=57, 尝试次数=1
2026-01-30 12:41:24,232 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 探索完成(工具循环): 7轮, 原因=已对因果链中的所有关键词进行了精确搜索，但均未命中任何段落。由于禁止使用语义搜索且不能重复搜索已用关键词，当前工具和约束下无法进一步找到相关段落。
2026-01-30 12:41:24,232 - app.services.agent.execution.tool_executor - INFO - [StandardTool] explore_content 执行成功
2026-01-30 12:41:24,232 - app.api.v1.agent - INFO - [Stream] 任务完成: 在第2章和第3章中，检索与因果链“‘脑子被塞进一团东西’→‘梦中悟刀’→‘醒后练刀’→‘身体限制’→‘改用站桩尝试内息’”相关的原文段落。 (36.7s)
2026-01-30 12:41:24,232 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1完成
2026-01-30 12:41:24,232 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共1个任务，耗时: 36.73s
2026-01-30 12:41:24,232 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2026-01-30 12:41:24,232 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=1, 展示型=0
2026-01-30 12:41:24,232 - app.services.agent.langgraph_agent - INFO - [Response] 单个输出任务(explore_content)，使用AI整合
2026-01-30 12:41:24,232 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2026-01-30 12:41:24,232 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=1, 展示型=0
2026-01-30 12:41:24,232 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=1444字符, 处理后=1518字符
2026-01-30 12:41:24,232 - app.services.agent.planning.response_builder - INFO - [Summarization] 准备发送 summarization_start 事件
2026-01-30 12:41:24,232 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-30 12:41:24,232 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-30 12:41:24,232 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=60, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-30 12:41:25,762 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:41:25,762 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-30 12:41:25,765 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:41:25,765 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=350, cost=$0.000053, time=1532ms
2026-01-30 12:41:25,765 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=72, 尝试次数=1
2026-01-30 12:41:25,775 - app.services.agent.planning.response_builder - INFO - [Summarization] reason生成: len=72 content=因果链梳理显示，“脑子被塞进一团东西”及“梦中悟刀”在第2、3章未找到直接证据，但“醒后练刀”、“身体限制”及“改用站桩尝试内息”均有原文支持。
2026-01-30 12:41:25,775 - app.services.agent.stream.stream_event_handler - INFO - [StreamEventHandler] emit_summarization_start 被调用, _on_flow_event=True, reason_len=72, reason=因果链梳理显示，“脑子被塞进一团东西”及“梦中悟刀”在第2、3章未找到直接证据，但“醒后练刀”、“身体限制”及“改用站桩尝试内息”均有原文支持。
2026-01-30 12:41:25,775 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_start 事件已发送
2026-01-30 12:41:25,775 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2026-01-30 12:41:25,775 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2026-01-30 12:41:25,780 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-30 12:41:25,781 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-30 12:41:25,781 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=20000, temp=0.7, task_type=TaskType.SUMMARIZATION
2026-01-30 12:41:32,493 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-30 12:41:32,494 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_complete 事件已发送（第一个chunk时）
2026-01-30 12:41:32,494 - app.services.agent.planning.response_builder - INFO - [Summarization] output_ready 事件已发送（第一个chunk时）
2026-01-30 12:41:35,353 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 11 个数据块，总长度: 1009
2026-01-30 12:41:35,354 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 4891 (prompt=4195, completion=696)
2026-01-30 12:41:35,354 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-30 12:41:35,355 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-30 12:41:35,366 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-30 12:41:35,366 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4891, cost=$0.002998, time=9573ms
2026-01-30 12:41:35,366 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=1009
2026-01-30 12:41:35,373 - app.services.context.vector_memory_store - INFO - 🔁 跳过重复记忆，复用ID=79913e7e-d5cd-4e09-bce6-ca6639bd8456_1769699172336_fc1f7e1d
2026-01-30 12:41:35,374 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:832d8d96-080d-4d14-bcc6-80a23ffafa0e | 重要度=0.87
2026-01-30 12:41:36,045 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:832d8d96-080d-4d14-bcc6-80a23ffafa0e | 重要度=0.60
2026-01-30 12:41:36,056 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:832d8d96-080d-4d14-bcc6-80a23ffafa0e:2edba307-74c5-40ab-aa48-84396f47c759, token=4635
2026-01-30 12:41:36,059 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:832d8d96-080d-4d14-bcc6-80a23ffafa0e:2edba307-74c5-40ab-aa48-84396f47c759, 消息数=8, 摘要长度=0, Token=4635
2026-01-30 12:41:36,059 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:832d8d96-080d-4d14-bcc6-80a23ffafa0e:2edba307-74c5-40ab-aa48-84396f47c759)
2026-01-30 12:41:36,060 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2026-01-30 12:41:36,066 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed