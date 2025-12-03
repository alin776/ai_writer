13:12:58 app.api.v1.agent INFO   [Redis] 全局连接池已创建
已注册策略: web_novel_11d - 网文11维度分析
13:12:58 app.utils.file_storage INFO   临时文件存储目录: D:\Temp\novelaide_exports
13:12:59 app.main INFO   [STARTUP] 监控中间件已注册: TraceMiddleware, MonitoringMiddleware
INFO:     Started server process [21728]
INFO:     Waiting for application startup.
13:13:00 app.main INFO   [STARTUP] 应用启动中...
13:13:00 app.core.database INFO   正在初始化数据库... (尝试 1/3)
13:13:00 app.core.database INFO   ✅ 数据库初始化成功
13:13:00 apscheduler.scheduler INFO   Adding job tentatively -- it will be properly scheduled when the scheduler starts
13:13:00 apscheduler.scheduler INFO   Added job "清理过期的去痕迹会话详情" to job store "default"
13:13:00 apscheduler.scheduler INFO   Scheduler started
13:13:00 app.tasks.cleanup_humanize_details INFO   定时任务调度器已启动
13:13:00 app.main INFO   [STARTUP] 开始预初始化同步Redis连接...
13:13:00 app.main INFO   [STARTUP] ✅ 同步Redis连接池预初始化完成
13:13:00 app.main INFO   [STARTUP] 开始初始化AsyncRedisSaver索引...
13:13:00 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ setup_checkpointer Redis连接验证成功
13:13:00 redisvl.index.index INFO   Index already exists, not overwriting.
13:13:00 redisvl.index.index INFO   Index already exists, not overwriting.
13:13:00 redisvl.index.index INFO   Index already exists, not overwriting.
13:13:00 langgraph.checkpoint.redis.aio INFO   Redis client is a standalone client
13:13:00 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ AsyncRedisSaver索引预创建成功
13:13:00 app.main INFO   [STARTUP] AsyncRedisSaver索引初始化完成
13:13:00 app.main INFO   [STARTUP] 开始预加载Embedding模型...
13:13:00 app.services.vector_store_service INFO   🔄 预加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
13:13:08 app.services.vector_store_service INFO   ✅ Embedding模型预加载成功，耗时: 7.61秒
13:13:08 app.main INFO   [STARTUP] Embedding模型预加载完成
13:13:08 app.main INFO   [STARTUP] P0性能优化已暂时禁用（诊断模式）
13:13:08 app.main INFO   [STARTUP] 应用启动完成
INFO:     Application startup complete.
13:14:17 monitoring INFO   Registered health check: cpu_usage
13:14:17 monitoring INFO   Registered health check: memory_usage
13:14:17 monitoring INFO   Registered health check: disk_usage
13:14:17 monitoring INFO   Registered health check: process_status
13:14:17 monitoring INFO   Added alert rule: high_cpu_usage
13:14:17 monitoring INFO   Added alert rule: high_memory_usage
13:14:17 monitoring INFO   Added alert rule: low_disk_space
13:14:17 app.api.v1.auth INFO   [LOGIN] 尝试登录: 2072855200@qq.com
sys:1: SAWarning: relationship 'User.credit_transactions' will copy column users.id to column credit_transactions.user_id, which conflicts with relationship(s): 'UserCredits.transactions' (copies user_credits.user_id to credit_transactions.user_id). If this is not the intention, consider if these relationships should be linked with back_populates, or if viewonly=True should be applied to one or more if they are read-only. For the less common case that foreign key constraints are partially overlapping, the orm.foreign() annotation can be used to isolate the columns that should be written towards.   To silence this warning, add the parameter 'overlaps="transactions"' to the 'User.credit_transactions' relationship. (Background on this warning at: https://sqlalche.me/e/20/qzyx) (This warning originated from the `configure_mappers()` process, which was invoked automatically in response to a user-initiated operation.)
sys:1: SAWarning: relationship 'CreditTransaction.user' will copy column users.id to column credit_transactions.user_id, which conflicts with relationship(s): 'UserCredits.transactions' (copies user_credits.user_id to credit_transactions.user_id). If this is not the intention, consider if these relationships should be linked with back_populates, or if viewonly=True should be applied to one or more if they are read-only. For the less common case that foreign key constraints are partially overlapping, the orm.foreign() annotation can be used to isolate the columns that should be written towards.   To silence this warning, add the parameter 'overlaps="transactions"' to the 'CreditTransaction.user' relationship. (Background on this warning at: https://sqlalche.me/e/20/qzyx) (This warning originated from the `configure_mappers()` process, which was invoked automatically in response to a user-initiated operation.)
sys:1: SAWarning: relationship 'CreditTransaction.user_credits' will copy column user_credits.user_id to column credit_transactions.user_id, which conflicts with relationship(s): 'CreditTransaction.user' (copies users.id to credit_transactions.user_id), 'User.credit_transactions' (copies users.id to credit_transactions.user_id). If this is not the intention, consider if these relationships should be linked with back_populates, or if viewonly=True should be applied to one or more if they are read-only. For the less common case that foreign key constraints are partially overlapping, the orm.foreign() annotation can be used to isolate the columns that should be written towards.   To silence this warning, add the parameter 'overlaps="credit_transactions,user"' to the 'CreditTransaction.user_credits' relationship. (Background on this warning at: https://sqlalche.me/e/20/qzyx) (This warning originated from the `configure_mappers()` process, which was invoked automatically in response to a user-initiated operation.)
13:14:18 app.api.v1.auth INFO   [LOGIN] 会话创建成功: 602f5147-846a-4cde-95d3-405fa75f133f (127.0.0.1)
13:14:18 app.api.v1.auth INFO   [LOGIN] 登录成功: testuser_new-1 (602f5147-846a-4cde-95d3-405fa75f133f) from 127.0.0.1
13:14:18 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/auth/login
INFO:     127.0.0.1:58017 - "POST /api/v1/auth/login HTTP/1.1" 200 OK
INFO:     127.0.0.1:58017 - "OPTIONS /api/v1/users/me HTTP/1.1" 200 OK
13:14:18 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/users/me
INFO:     127.0.0.1:58017 - "GET /api/v1/users/me HTTP/1.1" 200 OK
INFO:     127.0.0.1:58017 - "OPTIONS /api/v1/works HTTP/1.1" 200 OK
INFO:     127.0.0.1:63160 - "OPTIONS /api/v1/works HTTP/1.1" 200 OK
13:14:18 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works
INFO:     127.0.0.1:63160 - "GET /api/v1/works HTTP/1.1" 200 OK
13:14:18 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works
INFO:     127.0.0.1:58017 - "GET /api/v1/works HTTP/1.1" 200 OK