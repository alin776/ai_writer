17:15:54 app.utils.file_storage INFO   临时文件存储目录: D:\Temp\novelaide_exports
17:15:55 app.main INFO   [STARTUP] 监控中间件已注册: TraceMiddleware, MonitoringMiddleware
INFO:     Started server process [7244]
INFO:     Waiting for application startup.
17:15:55 app.main INFO   [STARTUP] 应用启动中...
17:15:55 app.core.database INFO   正在初始化数据库... (尝试 1/3)
17:15:55 app.core.database INFO   ✅ 数据库初始化成功
17:15:55 apscheduler.scheduler INFO   Adding job tentatively -- it will be properly scheduled when the scheduler starts
17:15:55 apscheduler.scheduler INFO   Added job "清理过期的去痕迹会话详情" to job store "default"
17:15:55 apscheduler.scheduler INFO   Scheduler started
17:15:55 app.tasks.cleanup_humanize_details INFO   定时任务调度器已启动
17:15:55 app.main INFO   [STARTUP] 开始预初始化同步Redis连接...
17:15:55 app.api.v1.agent INFO   [Redis] 全局连接池已创建
17:16:00 app.main INFO   [STARTUP] ✅ 同步Redis连接池预初始化完成
17:16:00 app.main INFO   [STARTUP] 开始初始化AsyncRedisSaver索引...
17:16:21 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ setup_checkpointer Redis连接验证成功
17:16:42 redisvl.index.index INFO   Index already exists, not overwriting.
17:16:42 redisvl.index.index INFO   Index already exists, not overwriting.
17:16:42 redisvl.index.index INFO   Index already exists, not overwriting.
17:16:42 langgraph.checkpoint.redis.aio INFO   Redis client is a standalone client
17:16:42 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ AsyncRedisSaver索引预创建成功
17:16:42 app.main INFO   [STARTUP] AsyncRedisSaver索引初始化完成
17:16:42 app.main INFO   [STARTUP] 开始预加载Embedding模型...
17:16:42 app.services.vector_store_service INFO   🔄 预加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
17:16:42 sentence_transformers.SentenceTransformer INFO   Use pytorch device_name: cpu
17:16:42 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
17:16:50 app.services.vector_store_service INFO   ✅ Embedding模型预加载成功，耗时: 7.38秒
17:16:50 app.main INFO   [STARTUP] Embedding模型预加载完成
17:16:50 app.main INFO   [STARTUP] P0性能优化已暂时禁用（诊断模式）
17:16:50 app.main INFO   [STARTUP] 应用启动完成
INFO:     Application startup complete.
17:18:09 monitoring INFO   Registered health check: cpu_usage
17:18:09 monitoring INFO   Registered health check: memory_usage
17:18:09 monitoring INFO   Registered health check: disk_usage
17:18:09 monitoring INFO   Registered health check: process_status
17:18:09 monitoring INFO   Added alert rule: high_cpu_usage
17:18:09 monitoring INFO   Added alert rule: high_memory_usage
17:18:09 monitoring INFO   Added alert rule: low_disk_space
17:18:09 app.api.v1.auth INFO   [LOGIN] 尝试登录: 2072855200@qq.com
17:18:09 app.api.v1.auth INFO   [LOGIN] 会话创建成功: 602f5147-846a-4cde-95d3-405fa75f133f (127.0.0.1)
17:18:09 app.api.v1.auth INFO   [LOGIN] 登录成功: testuser_new-1 (602f5147-846a-4cde-95d3-405fa75f133f) from 127.0.0.1
17:18:09 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/auth/login
INFO:     127.0.0.1:56319 - "POST /api/v1/auth/login HTTP/1.1" 200 OK
17:18:09 app.services.ai.prompts INFO   Prompts loaded successfully from D:\Java\ai_writer\backend\app\services\ai\prompts\default.json
17:18:09 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
17:18:09 app.services.ai.http_ai_service INFO   ModelSelector 已启用
17:18:09 app.services.agent.cost_tracker INFO   CostTracker 初始化完成, 持久化: False
17:18:09 app.services.ai.http_ai_service INFO   CostTracker 已启用
17:18:11 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
17:18:12 app.services.ai.fast_ai_service INFO   Fast AI Service 初始化成功，Model: gemini-2.5-flash-lite, Timeout: 15s (专用于检测/验证)
17:18:12 app.services.ai.nlp_preprocessor INFO   ✅ NLP预处理器初始化完成，规则库包含 31 条替换规则
17:18:12 app.services.ai.humanize_service INFO   HumanizeService 初始化成功 - 双AI架构 + NLP预处理 (标准模型: gemini-2.5-pro, 快速模型: gemini-2.5-flash-lite) (检测: True, 验证: False)
17:18:12 app.services.ai.humanize_service INFO   开始检测AI痕迹 (使用快速模型: gemini-2.5-flash-lite),文本长度: 40
17:18:12 app.services.ai.fast_ai_service INFO   开始快速AI痕迹检测: 文本长度=40
17:18:21 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
17:18:21 app.services.ai.fast_ai_service INFO   快速AI响应成功: tokens=2736 (prompt=2446, completion=290)
17:18:21 app.utils.json_parser INFO   [AI痕迹检测] 🔍 开始解析AI响应, 长度=802
17:18:21 app.utils.json_parser INFO   [AI痕迹检测] 🔍 方法2: 从markdown代码块提取JSON, 长度=790
17:18:21 app.utils.json_parser INFO   [AI痕迹检测] ✅ 方法2成功: markdown代码块解析
17:18:21 app.services.ai.humanize_service INFO   AI痕迹检测完成 (快速模型): overall_score=10.0, needs_humanization=False, tokens=2736, 耗时: 8.90秒
17:18:21 app.services.ai.humanize_service INFO   AI特征分数较低 (10.0 < 60.0),无需去痕迹
17:18:21 app.api.v1.humanize INFO   Token统计 - 总计: 2736 (检测:2736, 改写:0, 验证:0), 成本: $0.000547
17:18:21 app.services.user_profile_service INFO   记录去痕迹使用: user_id=602f5147-846a-4cde-95d3-405fa75f133f, total_uses=7, intensity=medium, improvement=-40.0
17:18:21 app.api.v1.humanize INFO   去痕迹会话已保存: session_id=9618b519-a38c-4fcf-9a40-05120de7cb36, improvement=-40.0, tokens=2736
17:18:21 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/humanize/rewrite
INFO:     127.0.0.1:56322 - "POST /api/v1/humanize/rewrite HTTP/1.1" 200 OK
17:19:22 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
17:19:22 app.services.ai.http_ai_service INFO   ModelSelector 已启用
17:19:22 app.services.ai.http_ai_service INFO   CostTracker 已启用
17:19:23 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
17:19:24 app.services.ai.fast_ai_service INFO   Fast AI Service 初始化成功，Model: gemini-2.5-flash-lite, Timeout: 15s (专用于检测/验证)
17:19:24 app.services.ai.nlp_preprocessor INFO   ✅ NLP预处理器初始化完成，规则库包含 31 条替换规则
17:19:24 app.services.ai.humanize_service INFO   HumanizeService 初始化成功 - 双AI架构 + NLP预处理 (标准模型: gemini-2.5-pro, 快速模型: gemini-2.5-flash-lite) (检测: True, 验证: False)
17:19:24 app.services.ai.humanize_service INFO   开始检测AI痕迹 (使用快速模型: gemini-2.5-flash-lite),文本长度: 42
17:19:24 app.services.ai.fast_ai_service INFO   开始快速AI痕迹检测: 文本长度=42
17:19:36 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
17:19:36 app.services.ai.fast_ai_service INFO   快速AI响应成功: tokens=2954 (prompt=2621, completion=333)
17:19:36 app.utils.json_parser INFO   [AI痕迹检测] 🔍 开始解析AI响应, 长度=907
17:19:36 app.utils.json_parser INFO   [AI痕迹检测] 🔍 方法2: 从markdown代码块提取JSON, 长度=895
17:19:36 app.utils.json_parser INFO   [AI痕迹检测] ✅ 方法2成功: markdown代码块解析
17:19:36 app.services.ai.humanize_service INFO   AI痕迹检测完成 (快速模型): overall_score=15.0, needs_humanization=False, tokens=2954, 耗时: 11.74秒
17:19:36 app.services.ai.humanize_service INFO   AI特征分数较低 (15.0 < 60.0),无需去痕迹
17:19:36 app.api.v1.humanize INFO   Token统计 - 总计: 2954 (检测:2954, 改写:0, 验证:0), 成本: $0.000591
17:19:36 app.services.user_profile_service INFO   记录去痕迹使用: user_id=602f5147-846a-4cde-95d3-405fa75f133f, total_uses=8, intensity=light, improvement=-35.0
17:19:36 app.api.v1.humanize INFO   去痕迹会话已保存: session_id=d919dcfc-918f-4c0b-a8be-14784509b71c, improvement=-35.0, tokens=2954
17:19:36 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/humanize/rewrite
INFO:     127.0.0.1:63730 - "POST /api/v1/humanize/rewrite HTTP/1.1" 200 OK
17:19:36 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
17:19:36 app.services.ai.http_ai_service INFO   ModelSelector 已启用
17:19:36 app.services.ai.http_ai_service INFO   CostTracker 已启用
17:19:38 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
17:19:39 app.services.ai.fast_ai_service INFO   Fast AI Service 初始化成功，Model: gemini-2.5-flash-lite, Timeout: 15s (专用于检测/验证)
17:19:39 app.services.ai.nlp_preprocessor INFO   ✅ NLP预处理器初始化完成，规则库包含 31 条替换规则
17:19:39 app.services.ai.humanize_service INFO   HumanizeService 初始化成功 - 双AI架构 + NLP预处理 (标准模型: gemini-2.5-pro, 快速模型: gemini-2.5-flash-lite) (检测: True, 验证: False)
17:19:39 app.services.ai.humanize_service INFO   开始检测AI痕迹 (使用快速模型: gemini-2.5-flash-lite),文本长度: 42
17:19:39 app.services.ai.fast_ai_service INFO   开始快速AI痕迹检测: 文本长度=42
17:19:48 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
17:19:48 app.services.ai.fast_ai_service INFO   快速AI响应成功: tokens=2928 (prompt=2616, completion=312)
17:19:48 app.utils.json_parser INFO   [AI痕迹检测] 🔍 开始解析AI响应, 长度=852
17:19:48 app.utils.json_parser INFO   [AI痕迹检测] 🔍 方法2: 从markdown代码块提取JSON, 长度=840
17:19:48 app.utils.json_parser INFO   [AI痕迹检测] ✅ 方法2成功: markdown代码块解析
17:19:48 app.services.ai.humanize_service INFO   AI痕迹检测完成 (快速模型): overall_score=18.0, needs_humanization=False, tokens=2928, 耗时: 8.90秒
17:19:48 app.services.ai.humanize_service INFO   AI特征分数较低 (18.0 < 60.0),无需去痕迹
17:19:48 app.api.v1.humanize INFO   Token统计 - 总计: 2928 (检测:2928, 改写:0, 验证:0), 成本: $0.000586
17:19:48 app.services.user_profile_service INFO   记录去痕迹使用: user_id=602f5147-846a-4cde-95d3-405fa75f133f, total_uses=9, intensity=light, improvement=-32.0
17:19:48 app.api.v1.humanize INFO   去痕迹会话已保存: session_id=c9e26dc9-aee2-41a0-b7d8-c2cd93224294, improvement=-32.0, tokens=2928
17:19:48 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/humanize/rewrite
INFO:     127.0.0.1:62016 - "POST /api/v1/humanize/rewrite HTTP/1.1" 200 OK
17:19:48 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
17:19:48 app.services.ai.http_ai_service INFO   ModelSelector 已启用
17:19:48 app.services.ai.http_ai_service INFO   CostTracker 已启用
17:19:49 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
17:19:51 app.services.ai.fast_ai_service INFO   Fast AI Service 初始化成功，Model: gemini-2.5-flash-lite, Timeout: 15s (专用于检测/验证)
17:19:51 app.services.ai.nlp_preprocessor INFO   ✅ NLP预处理器初始化完成，规则库包含 31 条替换规则
17:19:51 app.services.ai.humanize_service INFO   HumanizeService 初始化成功 - 双AI架构 + NLP预处理 (标准模型: gemini-2.5-pro, 快速模型: gemini-2.5-flash-lite) (检测: True, 验证: False)
17:19:51 app.services.ai.humanize_service INFO   开始检测AI痕迹 (使用快速模型: gemini-2.5-flash-lite),文本长度: 42
17:19:51 app.services.ai.fast_ai_service INFO   开始快速AI痕迹检测: 文本长度=42
17:20:05 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
17:20:05 app.services.ai.fast_ai_service INFO   快速AI响应成功: tokens=3079 (prompt=2720, completion=359)
17:20:05 app.utils.json_parser INFO   [AI痕迹检测] 🔍 开始解析AI响应, 长度=937
17:20:05 app.utils.json_parser INFO   [AI痕迹检测] 🔍 方法2: 从markdown代码块提取JSON, 长度=925
17:20:05 app.utils.json_parser INFO   [AI痕迹检测] ✅ 方法2成功: markdown代码块解析
17:20:05 app.services.ai.humanize_service INFO   AI痕迹检测完成 (快速模型): overall_score=15.0, needs_humanization=False, tokens=3079, 耗时: 14.38秒
17:20:05 app.services.ai.humanize_service INFO   AI特征分数较低 (15.0 < 60.0),无需去痕迹
17:20:05 app.api.v1.humanize INFO   Token统计 - 总计: 3079 (检测:3079, 改写:0, 验证:0), 成本: $0.000616
17:20:05 app.services.user_profile_service INFO   记录去痕迹使用: user_id=602f5147-846a-4cde-95d3-405fa75f133f, total_uses=10, intensity=light, improvement=-35.0
17:20:05 app.api.v1.humanize INFO   去痕迹会话已保存: session_id=69831f09-8c15-424b-b3d9-74f6cea8d0c2, improvement=-35.0, tokens=3079
17:20:05 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/humanize/rewrite
INFO:     127.0.0.1:62023 - "POST /api/v1/humanize/rewrite HTTP/1.1" 200 OK
17:20:05 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
17:20:05 app.services.ai.http_ai_service INFO   ModelSelector 已启用
17:20:05 app.services.ai.http_ai_service INFO   CostTracker 已启用
17:20:06 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
17:20:08 app.services.ai.fast_ai_service INFO   Fast AI Service 初始化成功，Model: gemini-2.5-flash-lite, Timeout: 15s (专用于检测/验证)
17:20:08 app.services.ai.nlp_preprocessor INFO   ✅ NLP预处理器初始化完成，规则库包含 31 条替换规则
17:20:08 app.services.ai.humanize_service INFO   HumanizeService 初始化成功 - 双AI架构 + NLP预处理 (标准模型: gemini-2.5-pro, 快速模型: gemini-2.5-flash-lite) (检测: True, 验证: False)
17:20:08 app.services.ai.humanize_service INFO   开始检测AI痕迹 (使用快速模型: gemini-2.5-flash-lite),文本长度: 42
17:20:08 app.services.ai.fast_ai_service INFO   开始快速AI痕迹检测: 文本长度=42
17:20:23 app.services.ai.fast_ai_service ERROR   快速AI调用超时 (>15秒)
17:20:23 app.services.ai.humanize_service ERROR   快速AI检测失败: API超时 (>15秒)
17:20:23 app.services.ai.humanize_service INFO   检测到AI特征 (分数=70.0 >= 60.0),开始去痕迹
17:20:23 app.services.ai.humanize_service INFO   ✅ NLP预处理完成: 未发现AI痕迹
17:20:23 app.services.ai.humanize_service INFO   开始人性化改写: intensity=light, 文本长度=42
17:20:23 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=500, temp=0.5, task_type=None
17:20:40 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/2 200 OK"
17:20:40 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
17:20:52 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 42
17:20:52 app.services.ai.http_ai_service INFO   流式响应Token统计: 1519 (prompt=1509, completion=10)
17:20:52 app.services.agent.cost_tracker INFO   [CostTracker] 记录API调用: gemini-2.5-pro, tokens: 1509+10=1519, cost: $0.000046
17:20:52 app.services.ai.http_ai_service INFO   [CostTracker] API调用已记录: tokens=1509+10, cost=$0.000046, time=28.62s
17:20:52 app.services.ai.humanize_service INFO   人性化改写完成: 输出了 2 个片段, 耗时: 28.62秒
17:20:52 app.services.ai.humanize_service INFO   ⏭️  已跳过验证阶段 (根据配置)
17:20:52 app.services.ai.humanize_service INFO   完整去痕迹流程完成,总耗时: 44.28秒, 总Token: 1519 (检测:0, 改写:1519, 验证:0)
17:20:52 app.api.v1.humanize INFO   Token统计 - 总计: 1519 (检测:0, 改写:1519, 验证:0), 成本: $0.003038
17:20:52 app.services.user_profile_service INFO   记录去痕迹使用: user_id=602f5147-846a-4cde-95d3-405fa75f133f, total_uses=11, intensity=light, improvement=20.0
17:20:52 app.api.v1.humanize INFO   去痕迹会话已保存: session_id=a2cd9152-6e60-4452-b91b-ac3dee17ff69, improvement=20.0, tokens=1519
17:20:52 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/humanize/rewrite
INFO:     127.0.0.1:49570 - "POST /api/v1/humanize/rewrite HTTP/1.1" 200 OK
17:20:52 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
17:20:52 app.services.ai.http_ai_service INFO   ModelSelector 已启用
17:20:52 app.services.ai.http_ai_service INFO   CostTracker 已启用
17:20:52 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
17:20:53 app.services.ai.fast_ai_service INFO   Fast AI Service 初始化成功，Model: gemini-2.5-flash-lite, Timeout: 15s (专用于检测/验证)
17:20:53 app.services.ai.nlp_preprocessor INFO   ✅ NLP预处理器初始化完成，规则库包含 31 条替换规则
17:20:53 app.services.ai.humanize_service INFO   HumanizeService 初始化成功 - 双AI架构 + NLP预处理 (标准模型: gemini-2.5-pro, 快速模型: gemini-2.5-flash-lite) (检测: True, 验证: False)
17:20:53 app.services.ai.humanize_service INFO   开始检测AI痕迹 (使用快速模型: gemini-2.5-flash-lite),文本长度: 42
17:20:53 app.services.ai.fast_ai_service INFO   开始快速AI痕迹检测: 文本长度=42
17:21:09 app.services.ai.fast_ai_service ERROR   快速AI调用超时 (>15秒)
17:21:09 app.services.ai.humanize_service ERROR   快速AI检测失败: API超时 (>15秒)
17:21:09 app.services.ai.humanize_service INFO   检测到AI特征 (分数=70.0 >= 60.0),开始去痕迹
17:21:09 app.services.ai.humanize_service INFO   ✅ NLP预处理完成: 未发现AI痕迹
17:21:09 app.services.ai.humanize_service INFO   开始人性化改写: intensity=light, 文本长度=42
17:21:09 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=500, temp=0.5, task_type=None
17:21:18 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/2 200 OK"
17:21:18 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
17:21:31 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 42
17:21:31 app.services.ai.http_ai_service INFO   流式响应Token统计: 1464 (prompt=1454, completion=10)
17:21:31 app.services.agent.cost_tracker INFO   [CostTracker] 记录API调用: gemini-2.5-pro, tokens: 1454+10=1464, cost: $0.000045
17:21:31 app.services.ai.http_ai_service INFO   [CostTracker] API调用已记录: tokens=1454+10, cost=$0.000045, time=22.00s
17:21:31 app.services.ai.humanize_service INFO   人性化改写完成: 输出了 2 个片段, 耗时: 22.00秒
17:21:31 app.services.ai.humanize_service INFO   ⏭️  已跳过验证阶段 (根据配置)
17:21:31 app.services.ai.humanize_service INFO   完整去痕迹流程完成,总耗时: 37.66秒, 总Token: 1464 (检测:0, 改写:1464, 验证:0)
17:21:31 app.api.v1.humanize INFO   Token统计 - 总计: 1464 (检测:0, 改写:1464, 验证:0), 成本: $0.002928
17:21:31 app.services.user_profile_service INFO   记录去痕迹使用: user_id=602f5147-846a-4cde-95d3-405fa75f133f, total_uses=12, intensity=light, improvement=20.0
17:21:31 app.api.v1.humanize INFO   去痕迹会话已保存: session_id=caac8242-b35c-4f03-8350-fae6e4bcc0b7, improvement=20.0, tokens=1464
17:21:31 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/humanize/rewrite
INFO:     127.0.0.1:52721 - "POST /api/v1/humanize/rewrite HTTP/1.1" 200 OK
17:21:31 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
17:21:31 app.services.ai.http_ai_service INFO   ModelSelector 已启用
17:21:31 app.services.ai.http_ai_service INFO   CostTracker 已启用
17:21:31 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
17:21:32 app.services.ai.fast_ai_service INFO   Fast AI Service 初始化成功，Model: gemini-2.5-flash-lite, Timeout: 15s (专用于检测/验证)
17:21:32 app.services.ai.nlp_preprocessor INFO   ✅ NLP预处理器初始化完成，规则库包含 31 条替换规则
17:21:32 app.services.ai.humanize_service INFO   HumanizeService 初始化成功 - 双AI架构 + NLP预处理 (标准模型: gemini-2.5-pro, 快速模型: gemini-2.5-flash-lite) (检测: True, 验证: False)
17:21:32 app.services.ai.humanize_service INFO   开始检测AI痕迹 (使用快速模型: gemini-2.5-flash-lite),文本长度: 42
17:21:32 app.services.ai.fast_ai_service INFO   开始快速AI痕迹检测: 文本长度=42
17:21:41 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
17:21:41 app.services.ai.fast_ai_service INFO   快速AI响应成功: tokens=2681 (prompt=2397, completion=284)
17:21:41 app.utils.json_parser INFO   [AI痕迹检测] 🔍 开始解析AI响应, 长度=797
17:21:41 app.utils.json_parser INFO   [AI痕迹检测] 🔍 方法2: 从markdown代码块提取JSON, 长度=785
17:21:41 app.utils.json_parser INFO   [AI痕迹检测] ✅ 方法2成功: markdown代码块解析
17:21:41 app.services.ai.humanize_service INFO   AI痕迹检测完成 (快速模型): overall_score=5.0, needs_humanization=False, tokens=2681, 耗时: 9.44秒
17:21:41 app.services.ai.humanize_service INFO   AI特征分数较低 (5.0 < 60.0),无需去痕迹
17:21:41 app.api.v1.humanize INFO   Token统计 - 总计: 2681 (检测:2681, 改写:0, 验证:0), 成本: $0.000536
17:21:41 app.services.user_profile_service INFO   记录去痕迹使用: user_id=602f5147-846a-4cde-95d3-405fa75f133f, total_uses=13, intensity=light, improvement=-45.0
17:21:41 app.api.v1.humanize INFO   去痕迹会话已保存: session_id=a4ce86b1-8aef-46c9-bd8a-984d1194d54f, improvement=-45.0, tokens=2681
17:21:41 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/humanize/rewrite
INFO:     127.0.0.1:64741 - "POST /api/v1/humanize/rewrite HTTP/1.1" 200 OK
17:21:41 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
17:21:41 app.services.ai.http_ai_service INFO   ModelSelector 已启用
17:21:41 app.services.ai.http_ai_service INFO   CostTracker 已启用
17:21:42 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
17:21:42 app.services.ai.fast_ai_service INFO   Fast AI Service 初始化成功，Model: gemini-2.5-flash-lite, Timeout: 15s (专用于检测/验证)
17:21:42 app.services.ai.nlp_preprocessor INFO   ✅ NLP预处理器初始化完成，规则库包含 31 条替换规则
17:21:42 app.services.ai.humanize_service INFO   HumanizeService 初始化成功 - 双AI架构 + NLP预处理 (标准模型: gemini-2.5-pro, 快速模型: gemini-2.5-flash-lite) (检测: True, 验证: False)
17:21:42 app.services.ai.humanize_service INFO   开始检测AI痕迹 (使用快速模型: gemini-2.5-flash-lite),文本长度: 42
17:21:42 app.services.ai.fast_ai_service INFO   开始快速AI痕迹检测: 文本长度=42
17:21:54 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
17:21:54 app.services.ai.fast_ai_service INFO   快速AI响应成功: tokens=2942 (prompt=2639, completion=303)
17:21:54 app.utils.json_parser INFO   [AI痕迹检测] 🔍 开始解析AI响应, 长度=832
17:21:54 app.utils.json_parser INFO   [AI痕迹检测] 🔍 方法2: 从markdown代码块提取JSON, 长度=820
17:21:54 app.utils.json_parser INFO   [AI痕迹检测] ✅ 方法2成功: markdown代码块解析
17:21:54 app.services.ai.humanize_service INFO   AI痕迹检测完成 (快速模型): overall_score=10.0, needs_humanization=False, tokens=2942, 耗时: 12.13秒
17:21:54 app.services.ai.humanize_service INFO   AI特征分数较低 (10.0 < 60.0),无需去痕迹
17:21:54 app.api.v1.humanize INFO   Token统计 - 总计: 2942 (检测:2942, 改写:0, 验证:0), 成本: $0.000588
17:21:54 app.services.user_profile_service INFO   记录去痕迹使用: user_id=602f5147-846a-4cde-95d3-405fa75f133f, total_uses=14, intensity=light, improvement=-40.0
17:21:54 app.api.v1.humanize INFO   去痕迹会话已保存: session_id=2bd388bb-5d9b-4786-8caf-e5140d5e48f9, improvement=-40.0, tokens=2942
17:21:54 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/humanize/rewrite
INFO:     127.0.0.1:62645 - "POST /api/v1/humanize/rewrite HTTP/1.1" 200 OK
17:21:54 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
17:21:54 app.services.ai.http_ai_service INFO   ModelSelector 已启用
17:21:54 app.services.ai.http_ai_service INFO   CostTracker 已启用
17:21:55 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
17:21:55 app.services.ai.fast_ai_service INFO   Fast AI Service 初始化成功，Model: gemini-2.5-flash-lite, Timeout: 15s (专用于检测/验证)
17:21:55 app.services.ai.nlp_preprocessor INFO   ✅ NLP预处理器初始化完成，规则库包含 31 条替换规则
17:21:55 app.services.ai.humanize_service INFO   HumanizeService 初始化成功 - 双AI架构 + NLP预处理 (标准模型: gemini-2.5-pro, 快速模型: gemini-2.5-flash-lite) (检测: True, 验证: False)
17:21:55 app.services.ai.humanize_service INFO   开始检测AI痕迹 (使用快速模型: gemini-2.5-flash-lite),文本长度: 42
17:21:55 app.services.ai.fast_ai_service INFO   开始快速AI痕迹检测: 文本长度=42
17:22:11 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
17:22:11 app.services.ai.fast_ai_service INFO   快速AI响应成功: tokens=4089 (prompt=3836, completion=253)
17:22:11 app.utils.json_parser INFO   [AI痕迹检测] 🔍 开始解析AI响应, 长度=683
17:22:11 app.utils.json_parser INFO   [AI痕迹检测] 🔍 方法2: 从markdown代码块提取JSON, 长度=671
17:22:11 app.utils.json_parser INFO   [AI痕迹检测] ✅ 方法2成功: markdown代码块解析
17:22:11 app.services.ai.humanize_service INFO   AI痕迹检测完成 (快速模型): overall_score=10.0, needs_humanization=False, tokens=4089, 耗时: 15.29秒
17:22:11 app.services.ai.humanize_service INFO   AI特征分数较低 (10.0 < 60.0),无需去痕迹
17:22:11 app.api.v1.humanize INFO   Token统计 - 总计: 4089 (检测:4089, 改写:0, 验证:0), 成本: $0.000818
17:22:11 app.services.user_profile_service INFO   记录去痕迹使用: user_id=602f5147-846a-4cde-95d3-405fa75f133f, total_uses=15, intensity=light, improvement=-40.0
17:22:11 app.api.v1.humanize INFO   去痕迹会话已保存: session_id=c99e317e-8d04-401f-8c44-d94922152428, improvement=-40.0, tokens=4089
17:22:11 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/humanize/rewrite
INFO:     127.0.0.1:50344 - "POST /api/v1/humanize/rewrite HTTP/1.1" 200 OK
17:22:11 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
17:22:11 app.services.ai.http_ai_service INFO   ModelSelector 已启用
17:22:11 app.services.ai.http_ai_service INFO   CostTracker 已启用
17:22:11 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
17:22:12 app.services.ai.fast_ai_service INFO   Fast AI Service 初始化成功，Model: gemini-2.5-flash-lite, Timeout: 15s (专用于检测/验证)
17:22:12 app.services.ai.nlp_preprocessor INFO   ✅ NLP预处理器初始化完成，规则库包含 31 条替换规则
17:22:12 app.services.ai.humanize_service INFO   HumanizeService 初始化成功 - 双AI架构 + NLP预处理 (标准模型: gemini-2.5-pro, 快速模型: gemini-2.5-flash-lite) (检测: True, 验证: False)
17:22:12 app.services.ai.humanize_service INFO   开始检测AI痕迹 (使用快速模型: gemini-2.5-flash-lite),文本长度: 42
17:22:12 app.services.ai.fast_ai_service INFO   开始快速AI痕迹检测: 文本长度=42
17:22:22 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
17:22:22 app.services.ai.fast_ai_service INFO   快速AI响应成功: tokens=2749 (prompt=2460, completion=289)
17:22:22 app.utils.json_parser INFO   [AI痕迹检测] 🔍 开始解析AI响应, 长度=801
17:22:22 app.utils.json_parser INFO   [AI痕迹检测] 🔍 方法2: 从markdown代码块提取JSON, 长度=789
17:22:22 app.utils.json_parser INFO   [AI痕迹检测] ✅ 方法2成功: markdown代码块解析
17:22:22 app.services.ai.humanize_service INFO   AI痕迹检测完成 (快速模型): overall_score=10.0, needs_humanization=False, tokens=2749, 耗时: 10.51秒
17:22:22 app.services.ai.humanize_service INFO   AI特征分数较低 (10.0 < 60.0),无需去痕迹
17:22:22 app.api.v1.humanize INFO   Token统计 - 总计: 2749 (检测:2749, 改写:0, 验证:0), 成本: $0.000550
17:22:22 app.services.user_profile_service INFO   记录去痕迹使用: user_id=602f5147-846a-4cde-95d3-405fa75f133f, total_uses=16, intensity=light, improvement=-40.0
17:22:22 app.api.v1.humanize INFO   去痕迹会话已保存: session_id=d722438d-682d-4712-8a30-de0d2f4419b1, improvement=-40.0, tokens=2749
17:22:22 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/humanize/rewrite
INFO:     127.0.0.1:63430 - "POST /api/v1/humanize/rewrite HTTP/1.1" 200 OK
17:22:22 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
17:22:22 app.services.ai.http_ai_service INFO   ModelSelector 已启用
17:22:22 app.services.ai.http_ai_service INFO   CostTracker 已启用
17:22:23 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
17:22:23 app.services.ai.fast_ai_service INFO   Fast AI Service 初始化成功，Model: gemini-2.5-flash-lite, Timeout: 15s (专用于检测/验证)
17:22:23 app.services.ai.nlp_preprocessor INFO   ✅ NLP预处理器初始化完成，规则库包含 31 条替换规则
17:22:23 app.services.ai.humanize_service INFO   HumanizeService 初始化成功 - 双AI架构 + NLP预处理 (标准模型: gemini-2.5-pro, 快速模型: gemini-2.5-flash-lite) (检测: True, 验证: False)
17:22:23 app.services.ai.humanize_service INFO   开始检测AI痕迹 (使用快速模型: gemini-2.5-flash-lite),文本长度: 43
17:22:23 app.services.ai.fast_ai_service INFO   开始快速AI痕迹检测: 文本长度=43
17:22:39 app.services.ai.fast_ai_service ERROR   快速AI调用超时 (>15秒)
17:22:39 app.services.ai.humanize_service ERROR   快速AI检测失败: API超时 (>15秒)
17:22:39 app.services.ai.humanize_service INFO   检测到AI特征 (分数=70.0 >= 60.0),开始去痕迹
17:22:39 app.services.ai.humanize_service INFO   ✅ NLP预处理完成: 未发现AI痕迹
17:22:39 app.services.ai.humanize_service INFO   开始人性化改写: intensity=light, 文本长度=43
17:22:39 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=500, temp=0.5, task_type=None
17:22:43 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/2 200 OK"
17:22:43 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
17:22:55 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 43
17:22:55 app.services.ai.http_ai_service INFO   流式响应Token统计: 1599 (prompt=1588, completion=11)
17:22:55 app.services.agent.cost_tracker INFO   [CostTracker] 记录API调用: gemini-2.5-pro, tokens: 1588+11=1599, cost: $0.000049
17:22:55 app.services.ai.http_ai_service INFO   [CostTracker] API调用已记录: tokens=1588+11, cost=$0.000049, time=16.00s
17:22:55 app.services.ai.humanize_service INFO   人性化改写完成: 输出了 2 个片段, 耗时: 16.00秒
17:22:55 app.services.ai.humanize_service INFO   ⏭️  已跳过验证阶段 (根据配置)
17:22:55 app.services.ai.humanize_service INFO   完整去痕迹流程完成,总耗时: 31.81秒, 总Token: 1599 (检测:0, 改写:1599, 验证:0)
17:22:55 app.api.v1.humanize INFO   Token统计 - 总计: 1599 (检测:0, 改写:1599, 验证:0), 成本: $0.003198
17:22:55 app.services.user_profile_service INFO   记录去痕迹使用: user_id=602f5147-846a-4cde-95d3-405fa75f133f, total_uses=17, intensity=light, improvement=20.0
17:22:55 app.api.v1.humanize INFO   去痕迹会话已保存: session_id=a3fbc8db-44fd-44e2-b036-a5b5e862f469, improvement=20.0, tokens=1599
17:22:55 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/humanize/rewrite
INFO:     127.0.0.1:58598 - "POST /api/v1/humanize/rewrite HTTP/1.1" 200 OK
17:22:55 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
17:22:55 app.services.ai.http_ai_service INFO   ModelSelector 已启用
17:22:55 app.services.ai.http_ai_service INFO   CostTracker 已启用
17:22:56 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
17:22:58 app.services.ai.fast_ai_service INFO   Fast AI Service 初始化成功，Model: gemini-2.5-flash-lite, Timeout: 15s (专用于检测/验证)
17:22:58 app.services.ai.nlp_preprocessor INFO   ✅ NLP预处理器初始化完成，规则库包含 31 条替换规则
17:22:58 app.services.ai.humanize_service INFO   HumanizeService 初始化成功 - 双AI架构 + NLP预处理 (标准模型: gemini-2.5-pro, 快速模型: gemini-2.5-flash-lite) (检测: True, 验证: False)
17:22:58 app.services.ai.humanize_service INFO   开始检测AI痕迹 (使用快速模型: gemini-2.5-flash-lite),文本长度: 43
17:22:58 app.services.ai.fast_ai_service INFO   开始快速AI痕迹检测: 文本长度=43
17:23:11 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
17:23:11 app.services.ai.fast_ai_service INFO   快速AI响应成功: tokens=4311 (prompt=3975, completion=336)
17:23:11 app.utils.json_parser INFO   [AI痕迹检测] 🔍 开始解析AI响应, 长度=877
17:23:11 app.utils.json_parser INFO   [AI痕迹检测] 🔍 方法2: 从markdown代码块提取JSON, 长度=865
17:23:11 app.utils.json_parser INFO   [AI痕迹检测] ✅ 方法2成功: markdown代码块解析
17:23:11 app.services.ai.humanize_service INFO   AI痕迹检测完成 (快速模型): overall_score=15.0, needs_humanization=False, tokens=4311, 耗时: 13.14秒
17:23:11 app.services.ai.humanize_service INFO   AI特征分数较低 (15.0 < 60.0),无需去痕迹
17:23:11 app.api.v1.humanize INFO   Token统计 - 总计: 4311 (检测:4311, 改写:0, 验证:0), 成本: $0.000862
17:23:11 app.services.user_profile_service INFO   记录去痕迹使用: user_id=602f5147-846a-4cde-95d3-405fa75f133f, total_uses=18, intensity=light, improvement=-35.0
17:23:11 app.api.v1.humanize INFO   去痕迹会话已保存: session_id=717a519e-7ea2-4b86-a743-e6d2bc36ee2f, improvement=-35.0, tokens=4311
17:23:11 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/humanize/rewrite
INFO:     127.0.0.1:54987 - "POST /api/v1/humanize/rewrite HTTP/1.1" 200 OK
17:23:11 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
17:23:11 app.services.ai.http_ai_service INFO   ModelSelector 已启用
17:23:11 app.services.ai.http_ai_service INFO   CostTracker 已启用
17:23:12 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
17:23:14 app.services.ai.fast_ai_service INFO   Fast AI Service 初始化成功，Model: gemini-2.5-flash-lite, Timeout: 15s (专用于检测/验证)
17:23:14 app.services.ai.nlp_preprocessor INFO   ✅ NLP预处理器初始化完成，规则库包含 31 条替换规则
17:23:14 app.services.ai.humanize_service INFO   HumanizeService 初始化成功 - 双AI架构 + NLP预处理 (标准模型: gemini-2.5-pro, 快速模型: gemini-2.5-flash-lite) (检测: True, 验证: False)
17:23:14 app.services.ai.humanize_service INFO   开始检测AI痕迹 (使用快速模型: gemini-2.5-flash-lite),文本长度: 43
17:23:14 app.services.ai.fast_ai_service INFO   开始快速AI痕迹检测: 文本长度=43
17:23:29 app.services.ai.fast_ai_service ERROR   快速AI调用超时 (>15秒)
17:23:29 app.services.ai.humanize_service ERROR   快速AI检测失败: API超时 (>15秒)
17:23:29 app.services.ai.humanize_service INFO   检测到AI特征 (分数=70.0 >= 60.0),开始去痕迹
17:23:29 app.services.ai.humanize_service INFO   ✅ NLP预处理完成: 未发现AI痕迹
17:23:29 app.services.ai.humanize_service INFO   开始人性化改写: intensity=light, 文本长度=43
17:23:29 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=500, temp=0.5, task_type=None
17:23:33 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/2 200 OK"
17:23:33 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
17:23:42 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 43
17:23:42 app.services.ai.http_ai_service INFO   流式响应Token统计: 1281 (prompt=1270, completion=11)
17:23:42 app.services.agent.cost_tracker INFO   [CostTracker] 记录API调用: gemini-2.5-pro, tokens: 1270+11=1281, cost: $0.000039
17:23:42 app.services.ai.http_ai_service INFO   [CostTracker] API调用已记录: tokens=1270+11, cost=$0.000039, time=12.53s
17:23:42 app.services.ai.humanize_service INFO   人性化改写完成: 输出了 2 个片段, 耗时: 12.54秒
17:23:42 app.services.ai.humanize_service INFO   ⏭️  已跳过验证阶段 (根据配置)
17:23:42 app.services.ai.humanize_service INFO   完整去痕迹流程完成,总耗时: 28.24秒, 总Token: 1281 (检测:0, 改写:1281, 验证:0)
17:23:42 app.api.v1.humanize INFO   Token统计 - 总计: 1281 (检测:0, 改写:1281, 验证:0), 成本: $0.002562
17:23:42 app.services.user_profile_service INFO   记录去痕迹使用: user_id=602f5147-846a-4cde-95d3-405fa75f133f, total_uses=19, intensity=light, improvement=20.0
17:23:42 app.api.v1.humanize INFO   去痕迹会话已保存: session_id=e7b618ba-bc63-4c2f-b15c-1beb66cd4ad0, improvement=20.0, tokens=1281
17:23:42 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/humanize/rewrite
INFO:     127.0.0.1:59157 - "POST /api/v1/humanize/rewrite HTTP/1.1" 200 OK
17:23:42 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
17:23:42 app.services.ai.http_ai_service INFO   ModelSelector 已启用
17:23:42 app.services.ai.http_ai_service INFO   CostTracker 已启用
17:23:43 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
17:23:45 app.services.ai.fast_ai_service INFO   Fast AI Service 初始化成功，Model: gemini-2.5-flash-lite, Timeout: 15s (专用于检测/验证)
17:23:45 app.services.ai.nlp_preprocessor INFO   ✅ NLP预处理器初始化完成，规则库包含 31 条替换规则
17:23:45 app.services.ai.humanize_service INFO   HumanizeService 初始化成功 - 双AI架构 + NLP预处理 (标准模型: gemini-2.5-pro, 快速模型: gemini-2.5-flash-lite) (检测: True, 验证: False)
17:23:45 app.services.ai.humanize_service INFO   开始检测AI痕迹 (使用快速模型: gemini-2.5-flash-lite),文本长度: 43
17:23:45 app.services.ai.fast_ai_service INFO   开始快速AI痕迹检测: 文本长度=43
17:24:00 app.services.ai.fast_ai_service ERROR   快速AI调用超时 (>15秒)
17:24:00 app.services.ai.humanize_service ERROR   快速AI检测失败: API超时 (>15秒)
17:24:00 app.services.ai.humanize_service INFO   检测到AI特征 (分数=70.0 >= 60.0),开始去痕迹
17:24:00 app.services.ai.humanize_service INFO   ✅ NLP预处理完成: 未发现AI痕迹
17:24:00 app.services.ai.humanize_service INFO   开始人性化改写: intensity=light, 文本长度=43
17:24:00 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=500, temp=0.5, task_type=None
17:24:11 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/2 200 OK"
17:24:11 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
17:24:16 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 43
17:24:16 app.services.ai.http_ai_service INFO   流式响应Token统计: 1133 (prompt=1126, completion=7)
17:24:16 app.services.agent.cost_tracker INFO   [CostTracker] 记录API调用: gemini-2.5-pro, tokens: 1126+7=1133, cost: $0.000035
17:24:16 app.services.ai.http_ai_service INFO   [CostTracker] API调用已记录: tokens=1126+7, cost=$0.000035, time=16.04s
17:24:16 app.services.ai.humanize_service INFO   人性化改写完成: 输出了 2 个片段, 耗时: 16.05秒
17:24:16 app.services.ai.humanize_service INFO   ⏭️  已跳过验证阶段 (根据配置)
17:24:16 app.services.ai.humanize_service INFO   完整去痕迹流程完成,总耗时: 31.92秒, 总Token: 1133 (检测:0, 改写:1133, 验证:0)
17:24:16 app.api.v1.humanize INFO   Token统计 - 总计: 1133 (检测:0, 改写:1133, 验证:0), 成本: $0.002266
17:24:16 app.services.user_profile_service INFO   记录去痕迹使用: user_id=602f5147-846a-4cde-95d3-405fa75f133f, total_uses=20, intensity=light, improvement=20.0
17:24:16 app.api.v1.humanize INFO   去痕迹会话已保存: session_id=16bfae09-e93b-4407-96c7-48d55265657e, improvement=20.0, tokens=1133
17:24:17 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/humanize/rewrite
INFO:     127.0.0.1:57000 - "POST /api/v1/humanize/rewrite HTTP/1.1" 200 OK
17:24:17 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
17:24:17 app.services.ai.http_ai_service INFO   ModelSelector 已启用
17:24:17 app.services.ai.http_ai_service INFO   CostTracker 已启用
17:24:18 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
17:24:19 app.services.ai.fast_ai_service INFO   Fast AI Service 初始化成功，Model: gemini-2.5-flash-lite, Timeout: 15s (专用于检测/验证)
17:24:19 app.services.ai.nlp_preprocessor INFO   ✅ NLP预处理器初始化完成，规则库包含 31 条替换规则
17:24:19 app.services.ai.humanize_service INFO   HumanizeService 初始化成功 - 双AI架构 + NLP预处理 (标准模型: gemini-2.5-pro, 快速模型: gemini-2.5-flash-lite) (检测: True, 验证: False)
17:24:19 app.services.ai.humanize_service INFO   开始检测AI痕迹 (使用快速模型: gemini-2.5-flash-lite),文本长度: 43
17:24:19 app.services.ai.fast_ai_service INFO   开始快速AI痕迹检测: 文本长度=43
17:24:31 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
17:24:31 app.services.ai.fast_ai_service INFO   快速AI响应成功: tokens=2919 (prompt=2555, completion=364)
17:24:31 app.utils.json_parser INFO   [AI痕迹检测] 🔍 开始解析AI响应, 长度=946
17:24:31 app.utils.json_parser INFO   [AI痕迹检测] 🔍 方法2: 从markdown代码块提取JSON, 长度=934
17:24:31 app.utils.json_parser INFO   [AI痕迹检测] ✅ 方法2成功: markdown代码块解析
17:24:31 app.services.ai.humanize_service INFO   AI痕迹检测完成 (快速模型): overall_score=15.0, needs_humanization=False, tokens=2919, 耗时: 11.37秒
17:24:31 app.services.ai.humanize_service INFO   AI特征分数较低 (15.0 < 60.0),无需去痕迹
17:24:31 app.api.v1.humanize INFO   Token统计 - 总计: 2919 (检测:2919, 改写:0, 验证:0), 成本: $0.000584
17:24:31 app.services.user_profile_service INFO   记录去痕迹使用: user_id=602f5147-846a-4cde-95d3-405fa75f133f, total_uses=21, intensity=light, improvement=-35.0
17:24:31 app.api.v1.humanize INFO   去痕迹会话已保存: session_id=d787d931-c858-4538-bd6d-b6585141fa81, improvement=-35.0, tokens=2919
17:24:31 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/humanize/rewrite
INFO:     127.0.0.1:59048 - "POST /api/v1/humanize/rewrite HTTP/1.1" 200 OK
17:24:31 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
17:24:31 app.services.ai.http_ai_service INFO   ModelSelector 已启用
17:24:31 app.services.ai.http_ai_service INFO   CostTracker 已启用
17:24:32 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
17:24:33 app.services.ai.fast_ai_service INFO   Fast AI Service 初始化成功，Model: gemini-2.5-flash-lite, Timeout: 15s (专用于检测/验证)
17:24:33 app.services.ai.nlp_preprocessor INFO   ✅ NLP预处理器初始化完成，规则库包含 31 条替换规则
17:24:33 app.services.ai.humanize_service INFO   HumanizeService 初始化成功 - 双AI架构 + NLP预处理 (标准模型: gemini-2.5-pro, 快速模型: gemini-2.5-flash-lite) (检测: True, 验证: False)
17:24:33 app.services.ai.humanize_service INFO   开始检测AI痕迹 (使用快速模型: gemini-2.5-flash-lite),文本长度: 43
17:24:33 app.services.ai.fast_ai_service INFO   开始快速AI痕迹检测: 文本长度=43
17:24:46 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
17:24:46 app.services.ai.fast_ai_service INFO   快速AI响应成功: tokens=3170 (prompt=2818, completion=352)
17:24:46 app.utils.json_parser INFO   [AI痕迹检测] 🔍 开始解析AI响应, 长度=929
17:24:46 app.utils.json_parser INFO   [AI痕迹检测] 🔍 方法2: 从markdown代码块提取JSON, 长度=917
17:24:46 app.utils.json_parser INFO   [AI痕迹检测] ✅ 方法2成功: markdown代码块解析
17:24:46 app.services.ai.humanize_service INFO   AI痕迹检测完成 (快速模型): overall_score=10.0, needs_humanization=False, tokens=3170, 耗时: 12.08秒
17:24:46 app.services.ai.humanize_service INFO   AI特征分数较低 (10.0 < 60.0),无需去痕迹
17:24:46 app.api.v1.humanize INFO   Token统计 - 总计: 3170 (检测:3170, 改写:0, 验证:0), 成本: $0.000634
17:24:46 app.services.user_profile_service INFO   记录去痕迹使用: user_id=602f5147-846a-4cde-95d3-405fa75f133f, total_uses=22, intensity=light, improvement=-40.0
17:24:46 app.api.v1.humanize INFO   去痕迹会话已保存: session_id=e8b86783-ef2c-4c44-8adf-577591a42e7f, improvement=-40.0, tokens=3170
17:24:46 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/humanize/rewrite
INFO:     127.0.0.1:65303 - "POST /api/v1/humanize/rewrite HTTP/1.1" 200 OK
17:24:46 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
17:24:46 app.services.ai.http_ai_service INFO   ModelSelector 已启用
17:24:46 app.services.ai.http_ai_service INFO   CostTracker 已启用
17:24:46 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
17:24:47 app.services.ai.fast_ai_service INFO   Fast AI Service 初始化成功，Model: gemini-2.5-flash-lite, Timeout: 15s (专用于检测/验证)
17:24:47 app.services.ai.nlp_preprocessor INFO   ✅ NLP预处理器初始化完成，规则库包含 31 条替换规则
17:24:47 app.services.ai.humanize_service INFO   HumanizeService 初始化成功 - 双AI架构 + NLP预处理 (标准模型: gemini-2.5-pro, 快速模型: gemini-2.5-flash-lite) (检测: True, 验证: False)
17:24:47 app.services.ai.humanize_service INFO   开始检测AI痕迹 (使用快速模型: gemini-2.5-flash-lite),文本长度: 43
17:24:47 app.services.ai.fast_ai_service INFO   开始快速AI痕迹检测: 文本长度=43
17:24:58 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
17:24:58 app.services.ai.fast_ai_service INFO   快速AI响应成功: tokens=2841 (prompt=2502, completion=339)
17:24:58 app.utils.json_parser INFO   [AI痕迹检测] 🔍 开始解析AI响应, 长度=899
17:24:58 app.utils.json_parser INFO   [AI痕迹检测] 🔍 方法2: 从markdown代码块提取JSON, 长度=887
17:24:58 app.utils.json_parser INFO   [AI痕迹检测] ✅ 方法2成功: markdown代码块解析
17:24:58 app.services.ai.humanize_service INFO   AI痕迹检测完成 (快速模型): overall_score=10.0, needs_humanization=False, tokens=2841, 耗时: 10.97秒
17:24:58 app.services.ai.humanize_service INFO   AI特征分数较低 (10.0 < 60.0),无需去痕迹
17:24:58 app.api.v1.humanize INFO   Token统计 - 总计: 2841 (检测:2841, 改写:0, 验证:0), 成本: $0.000568
17:24:58 app.services.user_profile_service INFO   记录去痕迹使用: user_id=602f5147-846a-4cde-95d3-405fa75f133f, total_uses=23, intensity=light, improvement=-40.0
17:24:58 app.api.v1.humanize INFO   去痕迹会话已保存: session_id=11fe8b28-471f-4f7a-9de1-a020fef0b036, improvement=-40.0, tokens=2841
17:24:58 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/humanize/rewrite
INFO:     127.0.0.1:56149 - "POST /api/v1/humanize/rewrite HTTP/1.1" 200 OK
17:24:58 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
17:24:58 app.services.ai.http_ai_service INFO   ModelSelector 已启用
17:24:58 app.services.ai.http_ai_service INFO   CostTracker 已启用
17:24:59 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
17:25:01 app.services.ai.fast_ai_service INFO   Fast AI Service 初始化成功，Model: gemini-2.5-flash-lite, Timeout: 15s (专用于检测/验证)
17:25:01 app.services.ai.nlp_preprocessor INFO   ✅ NLP预处理器初始化完成，规则库包含 31 条替换规则
17:25:01 app.services.ai.humanize_service INFO   HumanizeService 初始化成功 - 双AI架构 + NLP预处理 (标准模型: gemini-2.5-pro, 快速模型: gemini-2.5-flash-lite) (检测: True, 验证: False)
17:25:01 app.services.ai.humanize_service INFO   开始检测AI痕迹 (使用快速模型: gemini-2.5-flash-lite),文本长度: 43
17:25:01 app.services.ai.fast_ai_service INFO   开始快速AI痕迹检测: 文本长度=43
17:25:13 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
17:25:13 app.services.ai.fast_ai_service INFO   快速AI响应成功: tokens=3123 (prompt=2803, completion=320)
17:25:13 app.utils.json_parser INFO   [AI痕迹检测] 🔍 开始解析AI响应, 长度=866
17:25:13 app.utils.json_parser INFO   [AI痕迹检测] 🔍 方法2: 从markdown代码块提取JSON, 长度=854
17:25:13 app.utils.json_parser INFO   [AI痕迹检测] ✅ 方法2成功: markdown代码块解析
17:25:13 app.services.ai.humanize_service INFO   AI痕迹检测完成 (快速模型): overall_score=10.0, needs_humanization=False, tokens=3123, 耗时: 11.94秒
17:25:13 app.services.ai.humanize_service INFO   AI特征分数较低 (10.0 < 60.0),无需去痕迹
17:25:13 app.api.v1.humanize INFO   Token统计 - 总计: 3123 (检测:3123, 改写:0, 验证:0), 成本: $0.000625
17:25:13 app.services.user_profile_service INFO   记录去痕迹使用: user_id=602f5147-846a-4cde-95d3-405fa75f133f, total_uses=24, intensity=light, improvement=-40.0
17:25:13 app.api.v1.humanize INFO   去痕迹会话已保存: session_id=3f17f4d4-916e-4d63-9d53-402924c32e79, improvement=-40.0, tokens=3123
17:25:13 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/humanize/rewrite
INFO:     127.0.0.1:57739 - "POST /api/v1/humanize/rewrite HTTP/1.1" 200 OK
17:25:13 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
17:25:13 app.services.ai.http_ai_service INFO   ModelSelector 已启用
17:25:13 app.services.ai.http_ai_service INFO   CostTracker 已启用
17:25:15 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
17:25:16 app.services.ai.fast_ai_service INFO   Fast AI Service 初始化成功，Model: gemini-2.5-flash-lite, Timeout: 15s (专用于检测/验证)
17:25:16 app.services.ai.nlp_preprocessor INFO   ✅ NLP预处理器初始化完成，规则库包含 31 条替换规则
17:25:16 app.services.ai.humanize_service INFO   HumanizeService 初始化成功 - 双AI架构 + NLP预处理 (标准模型: gemini-2.5-pro, 快速模型: gemini-2.5-flash-lite) (检测: True, 验证: False)
17:25:16 app.services.ai.humanize_service INFO   开始检测AI痕迹 (使用快速模型: gemini-2.5-flash-lite),文本长度: 43
17:25:16 app.services.ai.fast_ai_service INFO   开始快速AI痕迹检测: 文本长度=43
17:25:32 app.services.ai.fast_ai_service ERROR   快速AI调用超时 (>15秒)
17:25:32 app.services.ai.humanize_service ERROR   快速AI检测失败: API超时 (>15秒)
17:25:32 app.services.ai.humanize_service INFO   检测到AI特征 (分数=70.0 >= 60.0),开始去痕迹
17:25:32 app.services.ai.humanize_service INFO   ✅ NLP预处理完成: 未发现AI痕迹
17:25:32 app.services.ai.humanize_service INFO   开始人性化改写: intensity=light, 文本长度=43
17:25:32 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=500, temp=0.5, task_type=None
17:25:35 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/2 200 OK"
17:25:35 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
17:25:45 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 43
17:25:45 app.services.ai.http_ai_service INFO   流式响应Token统计: 1345 (prompt=1334, completion=11)
17:25:45 app.services.agent.cost_tracker INFO   [CostTracker] 记录API调用: gemini-2.5-pro, tokens: 1334+11=1345, cost: $0.000041
17:25:45 app.services.ai.http_ai_service INFO   [CostTracker] API调用已记录: tokens=1334+11, cost=$0.000041, time=13.15s
17:25:45 app.services.ai.humanize_service INFO   人性化改写完成: 输出了 2 个片段, 耗时: 13.15秒
17:25:45 app.services.ai.humanize_service INFO   ⏭️  已跳过验证阶段 (根据配置)
17:25:45 app.services.ai.humanize_service INFO   完整去痕迹流程完成,总耗时: 28.82秒, 总Token: 1345 (检测:0, 改写:1345, 验证:0)
17:25:45 app.api.v1.humanize INFO   Token统计 - 总计: 1345 (检测:0, 改写:1345, 验证:0), 成本: $0.002690
17:25:45 app.services.user_profile_service INFO   记录去痕迹使用: user_id=602f5147-846a-4cde-95d3-405fa75f133f, total_uses=25, intensity=light, improvement=20.0
17:25:45 app.api.v1.humanize INFO   去痕迹会话已保存: session_id=e313c1d3-45a9-4aad-a910-ea02e85996b4, improvement=20.0, tokens=1345
17:25:45 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/humanize/rewrite
INFO:     127.0.0.1:63902 - "POST /api/v1/humanize/rewrite HTTP/1.1" 200 OK
17:25:45 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
17:25:45 app.services.ai.http_ai_service INFO   ModelSelector 已启用
17:25:45 app.services.ai.http_ai_service INFO   CostTracker 已启用
17:25:47 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
17:25:48 app.services.ai.fast_ai_service INFO   Fast AI Service 初始化成功，Model: gemini-2.5-flash-lite, Timeout: 15s (专用于检测/验证)
17:25:48 app.services.ai.nlp_preprocessor INFO   ✅ NLP预处理器初始化完成，规则库包含 31 条替换规则
17:25:48 app.services.ai.humanize_service INFO   HumanizeService 初始化成功 - 双AI架构 + NLP预处理 (标准模型: gemini-2.5-pro, 快速模型: gemini-2.5-flash-lite) (检测: True, 验证: False)
17:25:48 app.services.ai.humanize_service INFO   开始检测AI痕迹 (使用快速模型: gemini-2.5-flash-lite),文本长度: 43
17:25:48 app.services.ai.fast_ai_service INFO   开始快速AI痕迹检测: 文本长度=43
17:25:59 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
17:25:59 app.services.ai.fast_ai_service INFO   快速AI响应成功: tokens=2920 (prompt=2648, completion=272)
17:25:59 app.utils.json_parser INFO   [AI痕迹检测] 🔍 开始解析AI响应, 长度=711
17:25:59 app.utils.json_parser INFO   [AI痕迹检测] 🔍 方法2: 从markdown代码块提取JSON, 长度=699
17:25:59 app.utils.json_parser INFO   [AI痕迹检测] ✅ 方法2成功: markdown代码块解析
17:25:59 app.services.ai.humanize_service INFO   AI痕迹检测完成 (快速模型): overall_score=15.0, needs_humanization=False, tokens=2920, 耗时: 10.61秒
17:25:59 app.services.ai.humanize_service INFO   AI特征分数较低 (15.0 < 60.0),无需去痕迹
17:25:59 app.api.v1.humanize INFO   Token统计 - 总计: 2920 (检测:2920, 改写:0, 验证:0), 成本: $0.000584
17:25:59 app.services.user_profile_service INFO   记录去痕迹使用: user_id=602f5147-846a-4cde-95d3-405fa75f133f, total_uses=26, intensity=light, improvement=-35.0
17:25:59 app.api.v1.humanize INFO   去痕迹会话已保存: session_id=af587abb-9854-41d2-9ecb-134e72726848, improvement=-35.0, tokens=2920
17:25:59 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/humanize/rewrite
INFO:     127.0.0.1:62369 - "POST /api/v1/humanize/rewrite HTTP/1.1" 200 OK
17:25:59 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
17:25:59 app.services.ai.http_ai_service INFO   ModelSelector 已启用
17:25:59 app.services.ai.http_ai_service INFO   CostTracker 已启用
17:26:01 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
17:26:02 app.services.ai.fast_ai_service INFO   Fast AI Service 初始化成功，Model: gemini-2.5-flash-lite, Timeout: 15s (专用于检测/验证)
17:26:02 app.services.ai.nlp_preprocessor INFO   ✅ NLP预处理器初始化完成，规则库包含 31 条替换规则
17:26:02 app.services.ai.humanize_service INFO   HumanizeService 初始化成功 - 双AI架构 + NLP预处理 (标准模型: gemini-2.5-pro, 快速模型: gemini-2.5-flash-lite) (检测: True, 验证: False)
17:26:02 app.services.ai.humanize_service INFO   开始检测AI痕迹 (使用快速模型: gemini-2.5-flash-lite),文本长度: 43
17:26:02 app.services.ai.fast_ai_service INFO   开始快速AI痕迹检测: 文本长度=43
17:26:18 app.services.ai.fast_ai_service ERROR   快速AI调用超时 (>15秒)
17:26:18 app.services.ai.humanize_service ERROR   快速AI检测失败: API超时 (>15秒)
17:26:18 app.services.ai.humanize_service INFO   检测到AI特征 (分数=70.0 >= 60.0),开始去痕迹
17:26:18 app.services.ai.humanize_service INFO   ✅ NLP预处理完成: 未发现AI痕迹
17:26:18 app.services.ai.humanize_service INFO   开始人性化改写: intensity=light, 文本长度=43
17:26:18 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=500, temp=0.5, task_type=None
17:26:24 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/2 200 OK"
17:26:24 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
17:26:35 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 43
17:26:35 app.services.ai.http_ai_service INFO   流式响应Token统计: 1303 (prompt=1292, completion=11)
17:26:35 app.services.agent.cost_tracker INFO   [CostTracker] 记录API调用: gemini-2.5-pro, tokens: 1292+11=1303, cost: $0.000040
17:26:35 app.services.ai.http_ai_service INFO   [CostTracker] API调用已记录: tokens=1292+11, cost=$0.000040, time=17.24s
17:26:35 app.services.ai.humanize_service INFO   人性化改写完成: 输出了 2 个片段, 耗时: 17.24秒
17:26:35 app.services.ai.humanize_service INFO   ⏭️  已跳过验证阶段 (根据配置)
17:26:35 app.services.ai.humanize_service INFO   完整去痕迹流程完成,总耗时: 32.97秒, 总Token: 1303 (检测:0, 改写:1303, 验证:0)
17:26:35 app.api.v1.humanize INFO   Token统计 - 总计: 1303 (检测:0, 改写:1303, 验证:0), 成本: $0.002606
17:26:35 app.services.user_profile_service INFO   记录去痕迹使用: user_id=602f5147-846a-4cde-95d3-405fa75f133f, total_uses=27, intensity=light, improvement=20.0
17:26:35 app.api.v1.humanize INFO   去痕迹会话已保存: session_id=d46d3c0c-5504-4dfe-97ec-fbc9a13e208d, improvement=20.0, tokens=1303
17:26:35 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/humanize/rewrite
INFO:     127.0.0.1:51874 - "POST /api/v1/humanize/rewrite HTTP/1.1" 200 OK
17:26:35 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
17:26:35 app.services.ai.http_ai_service INFO   ModelSelector 已启用
17:26:35 app.services.ai.http_ai_service INFO   CostTracker 已启用
17:26:37 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
17:26:38 app.services.ai.fast_ai_service INFO   Fast AI Service 初始化成功，Model: gemini-2.5-flash-lite, Timeout: 15s (专用于检测/验证)
17:26:38 app.services.ai.nlp_preprocessor INFO   ✅ NLP预处理器初始化完成，规则库包含 31 条替换规则
17:26:38 app.services.ai.humanize_service INFO   HumanizeService 初始化成功 - 双AI架构 + NLP预处理 (标准模型: gemini-2.5-pro, 快速模型: gemini-2.5-flash-lite) (检测: True, 验证: False)
17:26:38 app.services.ai.humanize_service INFO   开始检测AI痕迹 (使用快速模型: gemini-2.5-flash-lite),文本长度: 43
17:26:38 app.services.ai.fast_ai_service INFO   开始快速AI痕迹检测: 文本长度=43
17:26:52 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
17:26:52 app.services.ai.fast_ai_service INFO   快速AI响应成功: tokens=2492 (prompt=2208, completion=284)
17:26:52 app.utils.json_parser INFO   [AI痕迹检测] 🔍 开始解析AI响应, 长度=797
17:26:52 app.utils.json_parser INFO   [AI痕迹检测] 🔍 方法2: 从markdown代码块提取JSON, 长度=785
17:26:52 app.utils.json_parser INFO   [AI痕迹检测] ✅ 方法2成功: markdown代码块解析
17:26:52 app.services.ai.humanize_service INFO   AI痕迹检测完成 (快速模型): overall_score=5.0, needs_humanization=False, tokens=2492, 耗时: 14.22秒
17:26:52 app.services.ai.humanize_service INFO   AI特征分数较低 (5.0 < 60.0),无需去痕迹
17:26:52 app.api.v1.humanize INFO   Token统计 - 总计: 2492 (检测:2492, 改写:0, 验证:0), 成本: $0.000498
17:26:52 app.services.user_profile_service INFO   记录去痕迹使用: user_id=602f5147-846a-4cde-95d3-405fa75f133f, total_uses=28, intensity=light, improvement=-45.0
17:26:52 app.api.v1.humanize INFO   去痕迹会话已保存: session_id=a5fdf90c-054d-43fa-9522-de6553f07dd6, improvement=-45.0, tokens=2492
17:26:52 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/humanize/rewrite
INFO:     127.0.0.1:58945 - "POST /api/v1/humanize/rewrite HTTP/1.1" 200 OK
17:26:52 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
17:26:52 app.services.ai.http_ai_service INFO   ModelSelector 已启用
17:26:52 app.services.ai.http_ai_service INFO   CostTracker 已启用
17:26:53 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
17:26:53 app.services.ai.fast_ai_service INFO   Fast AI Service 初始化成功，Model: gemini-2.5-flash-lite, Timeout: 15s (专用于检测/验证)
17:26:53 app.services.ai.nlp_preprocessor INFO   ✅ NLP预处理器初始化完成，规则库包含 31 条替换规则
17:26:53 app.services.ai.humanize_service INFO   HumanizeService 初始化成功 - 双AI架构 + NLP预处理 (标准模型: gemini-2.5-pro, 快速模型: gemini-2.5-flash-lite) (检测: True, 验证: False)
17:26:53 app.services.ai.humanize_service INFO   开始检测AI痕迹 (使用快速模型: gemini-2.5-flash-lite),文本长度: 43
17:26:53 app.services.ai.fast_ai_service INFO   开始快速AI痕迹检测: 文本长度=43
17:27:08 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
17:27:08 app.services.ai.fast_ai_service INFO   快速AI响应成功: tokens=4027 (prompt=3712, completion=315)
17:27:08 app.utils.json_parser INFO   [AI痕迹检测] 🔍 开始解析AI响应, 长度=843
17:27:08 app.utils.json_parser INFO   [AI痕迹检测] 🔍 方法2: 从markdown代码块提取JSON, 长度=831
17:27:08 app.utils.json_parser INFO   [AI痕迹检测] ✅ 方法2成功: markdown代码块解析
17:27:08 app.services.ai.humanize_service INFO   AI痕迹检测完成 (快速模型): overall_score=20.0, needs_humanization=False, tokens=4027, 耗时: 14.62秒
17:27:08 app.services.ai.humanize_service INFO   AI特征分数较低 (20.0 < 60.0),无需去痕迹
17:27:08 app.api.v1.humanize INFO   Token统计 - 总计: 4027 (检测:4027, 改写:0, 验证:0), 成本: $0.000805
17:27:08 app.services.user_profile_service INFO   记录去痕迹使用: user_id=602f5147-846a-4cde-95d3-405fa75f133f, total_uses=29, intensity=light, improvement=-30.0
17:27:08 app.api.v1.humanize INFO   去痕迹会话已保存: session_id=21af068f-44d8-449c-915d-3756ce0ac9f6, improvement=-30.0, tokens=4027
17:27:08 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/humanize/rewrite
INFO:     127.0.0.1:60038 - "POST /api/v1/humanize/rewrite HTTP/1.1" 200 OK
17:27:08 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
17:27:08 app.services.ai.http_ai_service INFO   ModelSelector 已启用
17:27:08 app.services.ai.http_ai_service INFO   CostTracker 已启用
17:27:09 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
17:27:09 app.services.ai.fast_ai_service INFO   Fast AI Service 初始化成功，Model: gemini-2.5-flash-lite, Timeout: 15s (专用于检测/验证)
17:27:09 app.services.ai.nlp_preprocessor INFO   ✅ NLP预处理器初始化完成，规则库包含 31 条替换规则
17:27:09 app.services.ai.humanize_service INFO   HumanizeService 初始化成功 - 双AI架构 + NLP预处理 (标准模型: gemini-2.5-pro, 快速模型: gemini-2.5-flash-lite) (检测: True, 验证: False)
17:27:09 app.services.ai.humanize_service INFO   开始检测AI痕迹 (使用快速模型: gemini-2.5-flash-lite),文本长度: 43
17:27:09 app.services.ai.fast_ai_service INFO   开始快速AI痕迹检测: 文本长度=43
17:27:21 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
17:27:21 app.services.ai.fast_ai_service INFO   快速AI响应成功: tokens=2415 (prompt=2186, completion=229)
17:27:21 app.utils.json_parser INFO   [AI痕迹检测] 🔍 开始解析AI响应, 长度=637
17:27:21 app.utils.json_parser INFO   [AI痕迹检测] 🔍 方法2: 从markdown代码块提取JSON, 长度=625
17:27:21 app.utils.json_parser INFO   [AI痕迹检测] ✅ 方法2成功: markdown代码块解析
17:27:21 app.services.ai.humanize_service INFO   AI痕迹检测完成 (快速模型): overall_score=15.0, needs_humanization=False, tokens=2415, 耗时: 11.67秒
17:27:21 app.services.ai.humanize_service INFO   AI特征分数较低 (15.0 < 60.0),无需去痕迹
17:27:21 app.api.v1.humanize INFO   Token统计 - 总计: 2415 (检测:2415, 改写:0, 验证:0), 成本: $0.000483
17:27:21 app.services.user_profile_service INFO   记录去痕迹使用: user_id=602f5147-846a-4cde-95d3-405fa75f133f, total_uses=30, intensity=light, improvement=-35.0
17:27:21 app.api.v1.humanize INFO   去痕迹会话已保存: session_id=5af58b0e-3bd4-463a-bd09-418ada794219, improvement=-35.0, tokens=2415
17:27:21 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/humanize/rewrite
INFO:     127.0.0.1:65340 - "POST /api/v1/humanize/rewrite HTTP/1.1" 200 OK
17:27:21 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
17:27:21 app.services.ai.http_ai_service INFO   ModelSelector 已启用
17:27:21 app.services.ai.http_ai_service INFO   CostTracker 已启用
17:27:21 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
17:27:22 app.services.ai.fast_ai_service INFO   Fast AI Service 初始化成功，Model: gemini-2.5-flash-lite, Timeout: 15s (专用于检测/验证)
17:27:22 app.services.ai.nlp_preprocessor INFO   ✅ NLP预处理器初始化完成，规则库包含 31 条替换规则
17:27:22 app.services.ai.humanize_service INFO   HumanizeService 初始化成功 - 双AI架构 + NLP预处理 (标准模型: gemini-2.5-pro, 快速模型: gemini-2.5-flash-lite) (检测: True, 验证: False)
17:27:22 app.services.ai.humanize_service INFO   开始检测AI痕迹 (使用快速模型: gemini-2.5-flash-lite),文本长度: 43
17:27:22 app.services.ai.fast_ai_service INFO   开始快速AI痕迹检测: 文本长度=43
17:27:38 app.services.ai.fast_ai_service ERROR   快速AI调用超时 (>15秒)
17:27:38 app.services.ai.humanize_service ERROR   快速AI检测失败: API超时 (>15秒)
17:27:38 app.services.ai.humanize_service INFO   检测到AI特征 (分数=70.0 >= 60.0),开始去痕迹
17:27:38 app.services.ai.humanize_service INFO   ✅ NLP预处理完成: 未发现AI痕迹
17:27:38 app.services.ai.humanize_service INFO   开始人性化改写: intensity=light, 文本长度=43
17:27:38 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=500, temp=0.5, task_type=None
17:27:41 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/2 200 OK"
17:27:41 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
17:27:54 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 43
17:27:54 app.services.ai.http_ai_service INFO   流式响应Token统计: 1490 (prompt=1479, completion=11)
17:27:54 app.services.agent.cost_tracker INFO   [CostTracker] 记录API调用: gemini-2.5-pro, tokens: 1479+11=1490, cost: $0.000046
17:27:54 app.services.ai.http_ai_service INFO   [CostTracker] API调用已记录: tokens=1479+11, cost=$0.000046, time=16.09s
17:27:54 app.services.ai.humanize_service INFO   人性化改写完成: 输出了 2 个片段, 耗时: 16.09秒
17:27:54 app.services.ai.humanize_service INFO   ⏭️  已跳过验证阶段 (根据配置)
17:27:54 app.services.ai.humanize_service INFO   完整去痕迹流程完成,总耗时: 31.79秒, 总Token: 1490 (检测:0, 改写:1490, 验证:0)
17:27:54 app.api.v1.humanize INFO   Token统计 - 总计: 1490 (检测:0, 改写:1490, 验证:0), 成本: $0.002980
17:27:54 app.services.user_profile_service INFO   记录去痕迹使用: user_id=602f5147-846a-4cde-95d3-405fa75f133f, total_uses=31, intensity=light, improvement=20.0
17:27:54 app.api.v1.humanize INFO   去痕迹会话已保存: session_id=6d8e4a27-adc4-46c9-b02c-29840cdf9055, improvement=20.0, tokens=1490
17:27:54 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/humanize/rewrite
INFO:     127.0.0.1:63927 - "POST /api/v1/humanize/rewrite HTTP/1.1" 200 OK
17:27:54 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
17:27:54 app.services.ai.http_ai_service INFO   ModelSelector 已启用
17:27:54 app.services.ai.http_ai_service INFO   CostTracker 已启用
17:27:55 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
17:27:57 app.services.ai.fast_ai_service INFO   Fast AI Service 初始化成功，Model: gemini-2.5-flash-lite, Timeout: 15s (专用于检测/验证)
17:27:57 app.services.ai.nlp_preprocessor INFO   ✅ NLP预处理器初始化完成，规则库包含 31 条替换规则
17:27:57 app.services.ai.humanize_service INFO   HumanizeService 初始化成功 - 双AI架构 + NLP预处理 (标准模型: gemini-2.5-pro, 快速模型: gemini-2.5-flash-lite) (检测: True, 验证: False)
17:27:57 app.services.ai.humanize_service INFO   开始检测AI痕迹 (使用快速模型: gemini-2.5-flash-lite),文本长度: 43
17:27:57 app.services.ai.fast_ai_service INFO   开始快速AI痕迹检测: 文本长度=43
17:28:06 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
17:28:06 app.services.ai.fast_ai_service INFO   快速AI响应成功: tokens=2102 (prompt=1876, completion=226)
17:28:06 app.utils.json_parser INFO   [AI痕迹检测] 🔍 开始解析AI响应, 长度=637
17:28:06 app.utils.json_parser INFO   [AI痕迹检测] 🔍 方法2: 从markdown代码块提取JSON, 长度=625
17:28:06 app.utils.json_parser INFO   [AI痕迹检测] ✅ 方法2成功: markdown代码块解析
17:28:06 app.services.ai.humanize_service INFO   AI痕迹检测完成 (快速模型): overall_score=10.0, needs_humanization=False, tokens=2102, 耗时: 8.99秒
17:28:06 app.services.ai.humanize_service INFO   AI特征分数较低 (10.0 < 60.0),无需去痕迹
17:28:06 app.api.v1.humanize INFO   Token统计 - 总计: 2102 (检测:2102, 改写:0, 验证:0), 成本: $0.000420
17:28:06 app.services.user_profile_service INFO   记录去痕迹使用: user_id=602f5147-846a-4cde-95d3-405fa75f133f, total_uses=32, intensity=light, improvement=-40.0
17:28:06 app.api.v1.humanize INFO   去痕迹会话已保存: session_id=512da90c-e618-4b51-94c6-e9f4d6fa71fa, improvement=-40.0, tokens=2102
17:28:06 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/humanize/rewrite
INFO:     127.0.0.1:56266 - "POST /api/v1/humanize/rewrite HTTP/1.1" 200 OK
17:28:06 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/humanize/rewrite/stream
INFO:     127.0.0.1:61561 - "POST /api/v1/humanize/rewrite/stream HTTP/1.1" 200 OK
17:28:06 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
17:28:06 app.services.ai.http_ai_service INFO   ModelSelector 已启用
17:28:06 app.services.ai.http_ai_service INFO   CostTracker 已启用
17:28:07 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
17:28:09 app.services.ai.fast_ai_service INFO   Fast AI Service 初始化成功，Model: gemini-2.5-flash-lite, Timeout: 15s (专用于检测/验证)
17:28:09 app.services.ai.nlp_preprocessor INFO   ✅ NLP预处理器初始化完成，规则库包含 31 条替换规则
17:28:09 app.services.ai.humanize_service INFO   HumanizeService 初始化成功 - 双AI架构 + NLP预处理 (标准模型: gemini-2.5-pro, 快速模型: gemini-2.5-flash-lite) (检测: True, 验证: False)
17:28:09 app.services.ai.humanize_service INFO   开始检测AI痕迹 (使用快速模型: gemini-2.5-flash-lite),文本长度: 33
17:28:09 app.services.ai.fast_ai_service INFO   开始快速AI痕迹检测: 文本长度=33
17:28:19 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
17:28:19 app.services.ai.fast_ai_service INFO   快速AI响应成功: tokens=2835 (prompt=2521, completion=314)
17:28:19 app.utils.json_parser INFO   [AI痕迹检测] 🔍 开始解析AI响应, 长度=854
17:28:19 app.utils.json_parser INFO   [AI痕迹检测] 🔍 方法2: 从markdown代码块提取JSON, 长度=842
17:28:19 app.utils.json_parser INFO   [AI痕迹检测] ✅ 方法2成功: markdown代码块解析
17:28:19 app.services.ai.humanize_service INFO   AI痕迹检测完成 (快速模型): overall_score=20.0, needs_humanization=False, tokens=2835, 耗时: 10.52秒