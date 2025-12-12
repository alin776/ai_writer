10:06:33 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: 07251ab5-98b3-4df7-b5f2-2bdb75201d18, chapter_id: 0d076ac2-70fc-46ce-92a0-d9dfba43723b
10:06:33 app.core.redis INFO   ✅ Redis connected: redis://localhost:6379/0
10:06:33 app.api.v1.ai INFO   [预加载] 当前章节已加载: 0d076ac2-70fc-46ce-92a0-d9dfba43723b
10:06:33 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
10:06:33 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:62550 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
10:06:33 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: 07251ab5-98b3-4df7-b5f2-2bdb75201d18, chapter_id: 0d076ac2-70fc-46ce-92a0-d9dfba43723b
10:06:33 app.api.v1.ai INFO   [预加载] 当前章节已加载: 0d076ac2-70fc-46ce-92a0-d9dfba43723b
10:06:33 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
10:06:33 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:62551 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
10:06:34 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:07251ab5-98b3-4df7-b5f2-2bdb75201d18
10:06:34 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/0d076ac2-70fc-46ce-92a0-d9dfba43723b
INFO:     127.0.0.1:57373 - "PUT /api/v1/chapters/0d076ac2-70fc-46ce-92a0-d9dfba43723b HTTP/1.1" 200 OK
10:06:34 app.services.chapter_vector_service INFO   Vectorizing chapter: 第1章 【摆烂的宿主】 (order=1)
10:06:37 app.services.chapter_vector_service INFO   Stored chapter vectors: 第1章 【摆烂的宿主】 (8 chunks)
10:06:37 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:07251ab5-98b3-4df7-b5f2-2bdb75201d18
10:06:37 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/0d076ac2-70fc-46ce-92a0-d9dfba43723b
INFO:     127.0.0.1:55748 - "PUT /api/v1/chapters/0d076ac2-70fc-46ce-92a0-d9dfba43723b HTTP/1.1" 200 OK
10:06:37 app.services.chapter_vector_service INFO   Vectorizing chapter: 第1章 【摆烂的宿主】 (order=1)
10:06:40 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: 07251ab5-98b3-4df7-b5f2-2bdb75201d18, chapter_id: a4044c3a-34f8-45c0-a992-871db188810d
10:06:40 app.api.v1.ai INFO   [预加载] 当前章节已加载: a4044c3a-34f8-45c0-a992-871db188810d
10:06:40 app.services.chapter_vector_service INFO   Stored chapter vectors: 第1章 【摆烂的宿主】 (8 chunks)
10:06:40 app.api.v1.ai INFO   [预加载] 前一章节已加载: 0d076ac2-70fc-46ce-92a0-d9dfba43723b
10:06:40 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
10:06:40 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:49209 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
10:06:40 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: 07251ab5-98b3-4df7-b5f2-2bdb75201d18, chapter_id: a4044c3a-34f8-45c0-a992-871db188810d
10:06:40 app.api.v1.ai INFO   [预加载] 当前章节已加载: a4044c3a-34f8-45c0-a992-871db188810d
10:06:40 app.api.v1.ai INFO   [预加载] 前一章节已加载: 0d076ac2-70fc-46ce-92a0-d9dfba43723b
10:06:40 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
10:06:40 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:49211 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
10:06:40 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:07251ab5-98b3-4df7-b5f2-2bdb75201d18
10:06:40 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/a4044c3a-34f8-45c0-a992-871db188810d
INFO:     127.0.0.1:54481 - "PUT /api/v1/chapters/a4044c3a-34f8-45c0-a992-871db188810d HTTP/1.1" 200 OK
10:06:40 app.services.chapter_vector_service INFO   Vectorizing chapter: 第2章 【躺平的系统】 (order=2)
10:06:42 app.services.chapter_vector_service INFO   Stored chapter vectors: 第2章 【躺平的系统】 (8 chunks)
10:06:42 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:07251ab5-98b3-4df7-b5f2-2bdb75201d18
10:06:42 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/a4044c3a-34f8-45c0-a992-871db188810d
INFO:     127.0.0.1:56216 - "PUT /api/v1/chapters/a4044c3a-34f8-45c0-a992-871db188810d HTTP/1.1" 200 OK
10:06:42 app.services.chapter_vector_service INFO   Vectorizing chapter: 第2章 【躺平的系统】 (order=2)
10:06:44 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: 07251ab5-98b3-4df7-b5f2-2bdb75201d18, chapter_id: 0d076ac2-70fc-46ce-92a0-d9dfba43723b
10:06:44 app.services.chapter_vector_service INFO   Stored chapter vectors: 第2章 【躺平的系统】 (8 chunks)
10:06:44 app.api.v1.ai INFO   [预加载] 当前章节已加载: 0d076ac2-70fc-46ce-92a0-d9dfba43723b
10:06:44 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
10:06:44 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:52951 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
10:06:44 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: 07251ab5-98b3-4df7-b5f2-2bdb75201d18, chapter_id: 0d076ac2-70fc-46ce-92a0-d9dfba43723b
10:06:44 app.api.v1.ai INFO   [预加载] 当前章节已加载: 0d076ac2-70fc-46ce-92a0-d9dfba43723b
10:06:44 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
10:06:44 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:52953 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
10:06:44 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:07251ab5-98b3-4df7-b5f2-2bdb75201d18
10:06:44 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/0d076ac2-70fc-46ce-92a0-d9dfba43723b
INFO:     127.0.0.1:50062 - "PUT /api/v1/chapters/0d076ac2-70fc-46ce-92a0-d9dfba43723b HTTP/1.1" 200 OK
10:06:44 app.services.chapter_vector_service INFO   Vectorizing chapter: 第1章 【摆烂的宿主】 (order=1)
10:06:47 app.services.chapter_vector_service INFO   Stored chapter vectors: 第1章 【摆烂的宿主】 (8 chunks)
10:06:47 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:07251ab5-98b3-4df7-b5f2-2bdb75201d18
10:06:47 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/0d076ac2-70fc-46ce-92a0-d9dfba43723b
INFO:     127.0.0.1:55382 - "PUT /api/v1/chapters/0d076ac2-70fc-46ce-92a0-d9dfba43723b HTTP/1.1" 200 OK
10:06:47 app.services.chapter_vector_service INFO   Vectorizing chapter: 第1章 【摆烂的宿主】 (order=1)
10:06:48 app.services.chapter_vector_service INFO   Stored chapter vectors: 第1章 【摆烂的宿主】 (8 chunks)
10:06:57 app.services.ai.prompts INFO   Prompts loaded successfully from D:\Java\ai_writer\backend\app\services\ai\prompts\default.json
10:06:57 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
10:06:58 app.services.ai.http_ai_service INFO   ModelSelector 已启用
10:06:58 app.services.ai.http_ai_service INFO   AILogService 已启用 (用于成本追踪)
10:07:03 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
10:07:03 app.api.v1.agent INFO   [Chat Stream] Mode: planning
10:07:03 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:57960 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
10:07:03 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: planning, Message: 庞博是什么身份？...
10:07:03 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
10:07:03 app.services.ai.http_ai_service INFO   ModelSelector 已启用
10:07:03 app.services.ai.http_ai_service INFO   [成本追踪] 初始化未传db/user_id，将使用请求上下文按需记录成本
10:07:05 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
10:07:05 app.services.context.adaptive_budget INFO   ✅ 所有预算配置验证通过
10:07:14 app.services.context.vector_memory_store INFO   ✅ VectorMemoryStore初始化成功 | 目录=./data/chroma_db | 模型=paraphrase-multilingual-MiniLM-L12-v2 | 集合=user_memories
10:07:14 app.services.context.manager INFO   ✅ VectorMemoryStore 已初始化
10:07:14 app.services.context.manager INFO   ✅ ContextManager: 长期记忆已启用 (user_id=None)
10:07:14 app.services.context.manager INFO   ✅ ContextManager: 自适应预算已启用
10:07:14 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ ContextManager已初始化（长期记忆已启用，自适应预算已启用，总预算=16000 tokens）
成功加载模板: analyze_text (版本 3.1.0)
成功加载模板: intent_classifier (版本 2.0.0)
成功加载模板: writing_agent (版本 2.0.0)
成功加载模板: planning_agent (版本 2.0.0)
成功加载模板: tool_agent (版本 2.0.0)
成功加载模板: query_agent (版本 2.0.0)
成功加载模板: system_agent_prompt (版本 2.0.0)
成功加载模板: creative_writing_prompt (版本 1.0.0)
10:07:15 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ PromptManager已初始化
10:07:15 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ Redis连接验证成功
10:07:15 app.services.agent.langgraph_agent INFO   [LangGraph] OK 使用 AsyncRedisSaver（redis://localhost:6379/0，TTL=7天）
10:07:15 app.services.agent.memory.metrics INFO   [MemoryMetrics] 监控系统已初始化
10:07:15 app.services.agent.memory.long_term_store INFO   [LongTermStore] Initialized: base_dir=./data/long_term_memory, max_size=50KB, compression=True
10:07:15 app.services.agent.memory.enhanced_memory_manager INFO   EnhancedMemoryManager initialized: short=10, medium=100, threshold=0.1, long_term_backup=enabled
10:07:15 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ EnhancedMemoryManager已创建
10:07:15 app.services.agent.memory.unified_coordinator INFO   [UnifiedMemoryCoordinator] 初始化统一记忆协调器
10:07:15 app.services.agent.memory.unified_coordinator INFO   [UnifiedMemoryCoordinator] 全局实例已设置
10:07:15 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ UnifiedMemoryCoordinator已初始化 | checkpointer=AsyncRedisSaver | enhanced_memory=yes | context_manager=yes
10:07:15 app.services.agent.parallel_tool_node INFO   [ParallelToolNode] 初始化完成，最大并发数=5，并行安全工具=4个
10:07:15 app.api.v1.agent INFO   [Global Agent] created global agent instance; MemorySaver shared across requests
10:07:15 app.api.v1.agent INFO   [agent_chat_stream] 📥 收到的 context 字段:
10:07:15 app.api.v1.agent INFO     - selected_text: N/A...
10:07:15 app.api.v1.agent INFO     - selection_position: N/A
10:07:15 app.api.v1.agent INFO     - chapter_context: 当前章节ID: 0d076ac2-70fc-46ce-92a0-d9dfba43723b...
10:07:15 app.api.v1.agent INFO     - instruction_context: N/A...
10:07:15 app.services.agent.langgraph_agent INFO   [Planning] 使用隔离的thread_id: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:69168b23-4f90-4cab-8efa-bd09b8118280 (user_id=602f5147-846a-4cde-95d3-405fa75f133f, work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18, conversation_id=69168b23-4f90-4cab-8efa-bd09b8118280)
10:07:15 app.services.context.monitoring_integration INFO   ✅ ContextManager监控收集器已初始化
10:07:15 app.services.context.store INFO   [ContextStore] Redis连接成功
10:07:15 app.services.context.store INFO   [ContextStore] 加载上下文: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:69168b23-4f90-4cab-8efa-bd09b8118280, 10条消息
10:07:15 app.services.context.token_counter WARNING   ⚠️ tiktoken初始化失败: 'Could not automatically map gemini-2.5-pro to a tokeniser. Please use `tiktoken.get_encoding` to explicitly get the tokeniser you expect.'，将使用降级策略
10:07:15 app.services.context.manager INFO   [ContextManager] Session 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:69168b23-4f90-4cab-8efa-bd09b8118280: 3327/16000 tokens
10:07:16 app.services.context.vector_memory_store INFO   🔍 检索记忆 | 查询='庞博是什么身份？...' | 隔离键=['user:602f5147-846a-4cde-95d3-405fa75f133f:work:07251ab5-98b3-4df7-b5f2-2bdb75201d18', 'user:602f5147-846a-4cde-95d3-405fa75f133f'] | 找到=3条
10:07:16 app.services.context.manager INFO   🔍 检索长期记忆 | 级别=work | work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18 | 含用户级=True | 找到=3条
10:07:16 app.services.context.monitoring_integration INFO   [Monitor] 上下文构建: 11条消息, 3327 tokens, 耗时 1644.30ms
10:07:16 app.services.agent.langgraph_agent INFO   [Planning] 从 ContextManager 加载了 11 条历史消息 (token: 3327)
10:07:16 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: 庞博是什么身份？...
10:07:16 app.core.cache INFO   ⚠️ 缓存未命中: prompt:planning_agent:v2.9.1:get_planning_agent_mode_prompt:fca6eb91156619d0
10:07:16 app.core.cache INFO   ⚠️ 缓存未命中: prompt:planning:v2.9.1:get_planning_static_prompt:fca6eb91156619d0
10:07:16 app.core.cache INFO   💾 缓存已保存: prompt:planning:v2.9.1:get_planning_static_prompt:fca6eb91156619d0 (expire=3600s)
10:07:16 app.core.cache INFO   💾 缓存已保存: prompt:planning_agent:v2.9.1:get_planning_agent_mode_prompt:fca6eb91156619d0 (expire=3600s)
10:07:16 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:07:16 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:07:16 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=1200, temp=0.3, task_type=TaskType.SIMPLE_QA
10:07:19 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:07:31 app.services.ai.http_ai_service INFO   API 响应完成，共接收 6 个数据块，总长度: 832
10:07:31 app.services.ai.http_ai_service INFO   流式响应Token统计: 11842 (prompt=11453, completion=389)
10:07:31 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:07:31 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:07:31 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=11842, cost=$0.018206, time=15080ms
10:07:31 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=11842
10:07:31 app.services.agent.langgraph_agent INFO   [JSON解析] 方法1成功: 直接解析
10:07:31 app.services.agent.langgraph_agent INFO   [Planning] 思维链: 输出=用户期望看到关于“庞博”身份的分析报告，需要总结他的角色定位, 原料=需要检索关于“庞博”的信息片段，并基于这, 处理=1. 使用 search_analysi
10:07:31 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共2个任务，耗时: 15.17s
10:07:31 app.api.v1.agent INFO   [Stream] Plan tasks: 2 items
10:07:31 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
10:07:31 app.services.agent.langgraph_agent INFO   [DeepAgent] 启用反思模式
10:07:31 app.services.agent.parameter_resolver INFO   [ParameterResolver] 初始化完成, 严格模式: False
10:07:31 app.services.agent.langgraph_agent INFO   [DeepAgent] ParameterResolver 已启用
10:07:31 app.services.agent.deep_agent.executor INFO   DeepAgent 开始执行，共 2 个任务，反思功能已启用
10:07:31 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] AI 推断功能已启用
10:07:31 app.api.v1.agent INFO   [Stream] Task started: 检索关于“庞博”的信息片段
D:\Java\ai_writer\backend\venv\Lib\site-packages\jieba\__init__.py:44: SyntaxWarning: invalid escape sequence '\.'
  re_han_default = re.compile("([\u4E00-\u9FD5a-zA-Z0-9+#&\._%\-]+)", re.U)
D:\Java\ai_writer\backend\venv\Lib\site-packages\jieba\__init__.py:46: SyntaxWarning: invalid escape sequence '\s'
  re_skip_default = re.compile("(\r\n|\s)", re.U)
D:\Java\ai_writer\backend\venv\Lib\site-packages\jieba\finalseg\__init__.py:78: SyntaxWarning: invalid escape sequence '\.'
  re_skip = re.compile("([a-zA-Z0-9]+(?:\.\d+)?%?)")
D:\Java\ai_writer\backend\venv\Lib\site-packages\jieba\posseg\__init__.py:16: SyntaxWarning: invalid escape sequence '\.'
  re_skip_detail = re.compile("([\.0-9]+|[a-zA-Z0-9]+)")
D:\Java\ai_writer\backend\venv\Lib\site-packages\jieba\posseg\__init__.py:17: SyntaxWarning: invalid escape sequence '\.'
  re_han_internal = re.compile("([\u4E00-\u9FD5a-zA-Z0-9+#&\._]+)")
D:\Java\ai_writer\backend\venv\Lib\site-packages\jieba\posseg\__init__.py:18: SyntaxWarning: invalid escape sequence '\s'
  re_skip_internal = re.compile("(\r\n|\s)")
D:\Java\ai_writer\backend\venv\Lib\site-packages\jieba\posseg\__init__.py:21: SyntaxWarning: invalid escape sequence '\.'
  re_num = re.compile("[\.0-9]+")
10:07:38 app.services.chapter_vector_service INFO   RAG retrieve work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18, current_order=1000000, query=庞博...
10:07:38 app.services.chapter_vector_service INFO   RAG retrieved 10 segments within order<=1000002
Building prefix dict from the default dictionary ...
10:07:38 jieba DEBUG   Building prefix dict from the default dictionary ...
Loading model from cache D:\Temp\jieba.cache
10:07:38 jieba DEBUG   Loading model from cache D:\Temp\jieba.cache
Loading model cost 1.520 seconds.
10:07:40 jieba DEBUG   Loading model cost 1.520 seconds.
Prefix dict has been built successfully.
10:07:40 jieba DEBUG   Prefix dict has been built successfully.
10:07:40 app.services.agent.langgraph_tools INFO   [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
10:07:40 app.api.v1.agent INFO   [Stream] 任务完成: 检索关于“庞博”的信息片段 (8.3s)
10:07:40 app.services.agent.deep_agent.reflection INFO   [Checkpoint] 任务 1 标记了 checkpoint，触发反思
10:07:40 app.services.agent.deep_agent.executor INFO   任务 1 触发反思检查点
10:07:40 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:07:40 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:07:40 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
10:07:42 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:07:44 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
10:07:44 app.services.ai.http_ai_service INFO   流式响应Token统计: 425 (prompt=424, completion=1)
10:07:44 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:07:44 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:07:44 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=425, cost=$0.000540, time=3708ms
10:07:44 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=425
10:07:44 app.services.agent.deep_agent.reflection INFO   [DeepAgent反思] 开始调用 AI，task_id=1
10:07:44 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:07:44 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:07:44 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=500, temp=0.3, task_type=TaskType.SIMPLE_QA
10:07:45 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:07:51 app.services.ai.http_ai_service INFO   API 响应完成，共接收 2 个数据块，总长度: 129
10:07:51 app.services.ai.http_ai_service INFO   流式响应Token统计: 1974 (prompt=1905, completion=69)
10:07:51 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:07:52 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:07:52 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1974, cost=$0.003071, time=7839ms
10:07:52 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=1974
10:07:52 app.services.agent.deep_agent.reflection INFO   [Reflection] JSON提取成功: needs_replan=False
10:07:52 app.api.v1.agent INFO   [Stream] Task started: 分析检索到的片段，总结庞博的身份
10:07:52 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
10:07:52 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
10:07:52 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
10:07:54 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:08:13 app.services.ai.http_ai_service INFO   API 响应完成，共接收 27 个数据块，总长度: 2374
10:08:13 app.services.ai.http_ai_service INFO   流式响应Token统计: 6757 (prompt=5038, completion=1719)
10:08:13 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:08:13 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:08:13 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=6757, cost=$0.023488, time=21118ms
10:08:13 app.services.agent.langgraph_tools INFO   ✅ [Agent分析] 分析完成，结果长度: 2374
10:08:13 app.api.v1.agent INFO   [Stream] 任务完成: 分析检索到的片段，总结庞博的身份 (21.2s)
10:08:13 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:08:13 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:08:13 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
10:08:16 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:08:17 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
10:08:17 app.services.ai.http_ai_service INFO   流式响应Token统计: 425 (prompt=424, completion=1)
10:08:17 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:08:17 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:08:17 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=425, cost=$0.000540, time=4625ms
10:08:17 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=425
10:08:17 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:08:17 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:08:17 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
10:08:19 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:08:21 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
10:08:21 app.services.ai.http_ai_service INFO   流式响应Token统计: 544 (prompt=543, completion=1)
10:08:21 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:08:21 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:08:21 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=544, cost=$0.000689, time=3881ms
10:08:21 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=544
10:08:21 app.services.agent.deep_agent.executor INFO   DeepAgent 执行完成: 任务=2, 反思=1, 重规划=0
10:08:21 app.services.agent.langgraph_agent INFO   [DeepAgent] 执行完成: 反思=1次, 重规划=0次
10:08:21 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共2个任务，耗时: 49.84s
10:08:21 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
10:08:21 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=1, 输出型=1, 展示型=0
10:08:21 app.services.agent.langgraph_agent INFO   [Response] 单个分析任务(analyze_text_tool)，使用AI格式化
10:08:21 app.services.agent.langgraph_agent INFO   [Summarization] 使用AI整合任务结果
10:08:21 app.services.agent.langgraph_agent INFO   [Summarization] 上下文压缩: 原始=5494字符, 压缩后=2143字符, 压缩率=61%
10:08:21 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
10:08:21 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
10:08:21 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
10:08:24 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:08:25 app.services.ai.http_ai_service INFO   API 响应完成，共接收 4 个数据块，总长度: 297
10:08:25 app.services.ai.http_ai_service INFO   流式响应Token统计: 2031 (prompt=1826, completion=205)
10:08:25 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:08:25 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:08:25 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2031, cost=$0.004332, time=3240ms
10:08:25 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=2031
10:08:26 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 隔离=work:07251ab5-98b3-4df7-b5f2-2bdb75201d18 | 重要度=0.60
10:08:26 app.services.context.store INFO   [ContextStore] 保存上下文: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:69168b23-4f90-4cab-8efa-bd09b8118280, token=3495
10:08:26 app.services.context.manager INFO   [ContextManager] 更新上下文: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:69168b23-4f90-4cab-8efa-bd09b8118280, 消息数=12, Token=3495
10:08:26 app.services.agent.langgraph_agent INFO   [Planning] 已保存对话到 ContextManager (session=602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:69168b23-4f90-4cab-8efa-bd09b8118280)
10:08:26 app.api.v1.agent INFO   [Stream] 跳过最终响应（内容已流式发送）
10:08:26 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed
INFO:     connection closed
INFO:     connection closed
INFO:     ('127.0.0.1', 55159) - "WebSocket /api/v1/ws/notifications/602f5147-846a-4cde-95d3-405fa75f133f" [accepted]
10:09:28 app.api.v1.ws INFO   [WebSocket] 通知连接建立: user_id=602f5147-846a-4cde-95d3-405fa75f133f
INFO:     connection open
10:09:30 app.api.v1.chapters INFO   [GET chapters] work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:09:30 app.api.v1.chapters INFO   ⚠️ [GET chapters] 缓存未命中: chapters:work:07251ab5-98b3-4df7-b5f2-2bdb75201d18
10:09:30 app.services.chapter_service INFO   [ChapterService] Querying chapters for work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18, type=<class 'uuid.UUID'>
10:09:30 app.api.v1.worldview INFO   ✅ [Worldview] 缓存命中: worldview:guidelines:07251ab5-98b3-4df7-b5f2-2bdb75201d18
10:09:30 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:characters:07251ab5-98b3-4df7-b5f2-2bdb75201d18 (expire=300s)
10:09:30 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:locations:07251ab5-98b3-4df7-b5f2-2bdb75201d18 (expire=300s)
10:09:30 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works/07251ab5-98b3-4df7-b5f2-2bdb75201d18
10:09:30 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:settings:07251ab5-98b3-4df7-b5f2-2bdb75201d18 (expire=300s)
10:09:30 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/07251ab5-98b3-4df7-b5f2-2bdb75201d18/guidelines
INFO:     127.0.0.1:55166 - "GET /api/v1/works/07251ab5-98b3-4df7-b5f2-2bdb75201d18 HTTP/1.1" 200 OK
10:09:30 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/07251ab5-98b3-4df7-b5f2-2bdb75201d18/characters
10:09:30 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/07251ab5-98b3-4df7-b5f2-2bdb75201d18/locations
INFO:     127.0.0.1:55173 - "GET /api/v1/worldview/works/07251ab5-98b3-4df7-b5f2-2bdb75201d18/guidelines HTTP/1.1" 200 OK
10:09:30 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/07251ab5-98b3-4df7-b5f2-2bdb75201d18/settings
10:09:30 app.services.chapter_service INFO   [ChapterService] Found 77 chapters
10:09:30 app.services.chapter_service INFO     - Chapter: 第1章 【摆烂的宿主】, order=1
10:09:30 app.services.chapter_service INFO     - ... (75 more chapters)
10:09:30 app.services.chapter_service INFO     - Chapter: 第100章 【火域铸真器，两脉起冲突】, order=77
10:09:30 app.api.v1.chapters INFO   [GET chapters] Returning 77 chapters
10:09:30 app.api.v1.chapters INFO   💾 [GET chapters] 缓存已保存: chapters:work:07251ab5-98b3-4df7-b5f2-2bdb75201d18 (expire=60s)
INFO:     127.0.0.1:55169 - "GET /api/v1/worldview/works/07251ab5-98b3-4df7-b5f2-2bdb75201d18/characters HTTP/1.1" 200 OK
INFO:     127.0.0.1:55168 - "GET /api/v1/worldview/works/07251ab5-98b3-4df7-b5f2-2bdb75201d18/locations HTTP/1.1" 200 OK
INFO:     127.0.0.1:55171 - "GET /api/v1/worldview/works/07251ab5-98b3-4df7-b5f2-2bdb75201d18/settings HTTP/1.1" 200 OK
10:09:30 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/chapters/work/07251ab5-98b3-4df7-b5f2-2bdb75201d18
INFO:     127.0.0.1:55167 - "GET /api/v1/chapters/work/07251ab5-98b3-4df7-b5f2-2bdb75201d18 HTTP/1.1" 200 OK
10:09:30 app.api.v1.worldview INFO   ✅ [Worldview] 缓存命中: worldview:ai-guidelines:07251ab5-98b3-4df7-b5f2-2bdb75201d18
10:09:30 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/07251ab5-98b3-4df7-b5f2-2bdb75201d18/ai-guidelines
INFO:     127.0.0.1:56166 - "GET /api/v1/worldview/works/07251ab5-98b3-4df7-b5f2-2bdb75201d18/ai-guidelines HTTP/1.1" 200 OK
10:09:30 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works/07251ab5-98b3-4df7-b5f2-2bdb75201d18
INFO:     127.0.0.1:56171 - "GET /api/v1/works/07251ab5-98b3-4df7-b5f2-2bdb75201d18 HTTP/1.1" 200 OK
10:09:30 app.api.v1.worldview INFO   ✅ [Worldview] 缓存命中: worldview:guidelines:07251ab5-98b3-4df7-b5f2-2bdb75201d18
10:09:30 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:characters:07251ab5-98b3-4df7-b5f2-2bdb75201d18 (expire=300s)
10:09:31 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:settings:07251ab5-98b3-4df7-b5f2-2bdb75201d18 (expire=300s)
10:09:31 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/07251ab5-98b3-4df7-b5f2-2bdb75201d18/guidelines
10:09:31 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/07251ab5-98b3-4df7-b5f2-2bdb75201d18/characters
INFO:     127.0.0.1:56172 - "GET /api/v1/worldview/works/07251ab5-98b3-4df7-b5f2-2bdb75201d18/guidelines HTTP/1.1" 200 OK
10:09:31 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/07251ab5-98b3-4df7-b5f2-2bdb75201d18/settings
10:09:31 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:locations:07251ab5-98b3-4df7-b5f2-2bdb75201d18 (expire=300s)
INFO:     127.0.0.1:56173 - "GET /api/v1/worldview/works/07251ab5-98b3-4df7-b5f2-2bdb75201d18/characters HTTP/1.1" 200 OK
INFO:     127.0.0.1:56175 - "GET /api/v1/worldview/works/07251ab5-98b3-4df7-b5f2-2bdb75201d18/settings HTTP/1.1" 200 OK
10:09:31 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/07251ab5-98b3-4df7-b5f2-2bdb75201d18/locations
INFO:     127.0.0.1:56174 - "GET /api/v1/worldview/works/07251ab5-98b3-4df7-b5f2-2bdb75201d18/locations HTTP/1.1" 200 OK
10:09:31 app.api.v1.chapters INFO   [GET chapters] work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:09:31 app.api.v1.chapters INFO   ✅ [GET chapters] 缓存命中: chapters:work:07251ab5-98b3-4df7-b5f2-2bdb75201d18
10:09:31 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/chapters/work/07251ab5-98b3-4df7-b5f2-2bdb75201d18
INFO:     127.0.0.1:65162 - "GET /api/v1/chapters/work/07251ab5-98b3-4df7-b5f2-2bdb75201d18 HTTP/1.1" 200 OK
10:09:31 app.api.v1.worldview INFO   ✅ [Worldview] 缓存命中: worldview:ai-guidelines:07251ab5-98b3-4df7-b5f2-2bdb75201d18
10:09:31 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/07251ab5-98b3-4df7-b5f2-2bdb75201d18/ai-guidelines
INFO:     127.0.0.1:65163 - "GET /api/v1/worldview/works/07251ab5-98b3-4df7-b5f2-2bdb75201d18/ai-guidelines HTTP/1.1" 200 OK
10:09:31 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/analysis/works/07251ab5-98b3-4df7-b5f2-2bdb75201d18/status
INFO:     127.0.0.1:60611 - "GET /api/v1/analysis/works/07251ab5-98b3-4df7-b5f2-2bdb75201d18/status HTTP/1.1" 404 Not Found
10:09:31 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/analysis/works/07251ab5-98b3-4df7-b5f2-2bdb75201d18/status
INFO:     127.0.0.1:63593 - "GET /api/v1/analysis/works/07251ab5-98b3-4df7-b5f2-2bdb75201d18/status HTTP/1.1" 404 Not Found
10:09:31 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: 07251ab5-98b3-4df7-b5f2-2bdb75201d18, chapter_id: 0d076ac2-70fc-46ce-92a0-d9dfba43723b
10:09:31 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: 07251ab5-98b3-4df7-b5f2-2bdb75201d18, chapter_id: 0d076ac2-70fc-46ce-92a0-d9dfba43723b
10:09:31 app.api.v1.ai INFO   [预加载] 当前章节已加载: 0d076ac2-70fc-46ce-92a0-d9dfba43723b
10:09:31 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
10:09:31 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:60750 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
10:09:32 app.api.v1.ai INFO   [预加载] 当前章节已加载: 0d076ac2-70fc-46ce-92a0-d9dfba43723b
10:09:32 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
10:09:32 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:60751 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
10:09:32 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:07251ab5-98b3-4df7-b5f2-2bdb75201d18
10:09:32 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/0d076ac2-70fc-46ce-92a0-d9dfba43723b
INFO:     127.0.0.1:60580 - "PUT /api/v1/chapters/0d076ac2-70fc-46ce-92a0-d9dfba43723b HTTP/1.1" 200 OK
10:09:32 app.services.chapter_vector_service INFO   Vectorizing chapter: 第1章 【摆烂的宿主】 (order=1)
INFO:     ('127.0.0.1', 63116) - "WebSocket /api/v1/ws/notifications/602f5147-846a-4cde-95d3-405fa75f133f" [accepted]
10:09:34 app.api.v1.ws INFO   [WebSocket] 通知连接建立: user_id=602f5147-846a-4cde-95d3-405fa75f133f
INFO:     connection open
10:09:34 app.services.chapter_vector_service INFO   Stored chapter vectors: 第1章 【摆烂的宿主】 (8 chunks)
10:09:34 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:07251ab5-98b3-4df7-b5f2-2bdb75201d18
10:09:34 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/0d076ac2-70fc-46ce-92a0-d9dfba43723b
INFO:     127.0.0.1:63118 - "PUT /api/v1/chapters/0d076ac2-70fc-46ce-92a0-d9dfba43723b HTTP/1.1" 200 OK
10:09:34 app.services.chapter_vector_service INFO   Vectorizing chapter: 第1章 【摆烂的宿主】 (order=1)
10:09:36 app.services.chapter_vector_service INFO   Stored chapter vectors: 第1章 【摆烂的宿主】 (8 chunks)
10:09:36 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: 07251ab5-98b3-4df7-b5f2-2bdb75201d18, chapter_id: a4044c3a-34f8-45c0-a992-871db188810d
10:09:36 app.api.v1.ai INFO   [预加载] 当前章节已加载: a4044c3a-34f8-45c0-a992-871db188810d
10:09:36 app.api.v1.ai INFO   [预加载] 前一章节已加载: 0d076ac2-70fc-46ce-92a0-d9dfba43723b
10:09:36 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
10:09:36 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:52237 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
10:09:36 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: 07251ab5-98b3-4df7-b5f2-2bdb75201d18, chapter_id: a4044c3a-34f8-45c0-a992-871db188810d
10:09:36 app.api.v1.ai INFO   [预加载] 当前章节已加载: a4044c3a-34f8-45c0-a992-871db188810d
10:09:36 app.api.v1.ai INFO   [预加载] 前一章节已加载: 0d076ac2-70fc-46ce-92a0-d9dfba43723b
10:09:36 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
10:09:36 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:52239 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
10:09:37 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:07251ab5-98b3-4df7-b5f2-2bdb75201d18
10:09:37 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/a4044c3a-34f8-45c0-a992-871db188810d
INFO:     127.0.0.1:62765 - "PUT /api/v1/chapters/a4044c3a-34f8-45c0-a992-871db188810d HTTP/1.1" 200 OK
10:09:37 app.services.chapter_vector_service INFO   Vectorizing chapter: 第2章 【躺平的系统】 (order=2)
10:09:39 app.services.chapter_vector_service INFO   Stored chapter vectors: 第2章 【躺平的系统】 (8 chunks)
10:09:40 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:07251ab5-98b3-4df7-b5f2-2bdb75201d18
10:09:40 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/a4044c3a-34f8-45c0-a992-871db188810d
INFO:     127.0.0.1:59180 - "PUT /api/v1/chapters/a4044c3a-34f8-45c0-a992-871db188810d HTTP/1.1" 200 OK
10:09:40 app.services.chapter_vector_service INFO   Vectorizing chapter: 第2章 【躺平的系统】 (order=2)
10:09:41 app.services.chapter_vector_service INFO   Stored chapter vectors: 第2章 【躺平的系统】 (8 chunks)
10:09:46 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
10:09:46 app.services.ai.http_ai_service INFO   ModelSelector 已启用
10:09:46 app.services.ai.http_ai_service INFO   AILogService 已启用 (用于成本追踪)
10:09:51 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
10:09:51 app.api.v1.agent INFO   [Chat Stream] Mode: planning
10:09:51 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:51770 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
10:09:51 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: planning, Message: 庞博是什么身份？...
10:09:51 app.api.v1.agent INFO   [agent_chat_stream] 📥 收到的 context 字段:
10:09:51 app.api.v1.agent INFO     - selected_text: N/A...
10:09:51 app.api.v1.agent INFO     - selection_position: N/A
10:09:51 app.api.v1.agent INFO     - chapter_context: 当前章节ID: a4044c3a-34f8-45c0-a992-871db188810d...
10:09:51 app.api.v1.agent INFO     - instruction_context: N/A...
10:09:51 app.services.agent.langgraph_agent INFO   [Planning] 使用隔离的thread_id: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:ab8f921b-2735-4d92-a8cf-9c8d418d9c97 (user_id=602f5147-846a-4cde-95d3-405fa75f133f, work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18, conversation_id=ab8f921b-2735-4d92-a8cf-9c8d418d9c97)
10:09:51 app.services.context.store INFO   [ContextStore] 加载上下文: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:ab8f921b-2735-4d92-a8cf-9c8d418d9c97, 2条消息
10:09:51 app.services.context.manager INFO   [ContextManager] Session 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:ab8f921b-2735-4d92-a8cf-9c8d418d9c97: 3244/16000 tokens
10:09:51 app.services.context.vector_memory_store INFO   🔍 检索记忆 | 查询='庞博是什么身份？...' | 隔离键=['user:602f5147-846a-4cde-95d3-405fa75f133f:work:07251ab5-98b3-4df7-b5f2-2bdb75201d18', 'user:602f5147-846a-4cde-95d3-405fa75f133f'] | 找到=3条
10:09:51 app.services.context.manager INFO   🔍 检索长期记忆 | 级别=work | work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18 | 含用户级=True | 找到=3条
10:09:51 app.services.context.monitoring_integration INFO   [Monitor] 上下文构建: 3条消息, 3244 tokens, 耗时 79.46ms
10:09:51 app.services.agent.langgraph_agent INFO   [Planning] 从 ContextManager 加载了 3 条历史消息 (token: 3244)
10:09:51 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: 庞博是什么身份？...
10:09:51 app.core.cache INFO   ✅ 缓存命中: prompt:planning_agent:v2.9.1:get_planning_agent_mode_prompt:fca6eb91156619d0
10:09:51 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:09:51 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:09:51 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=1200, temp=0.3, task_type=TaskType.SIMPLE_QA
10:09:53 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:09:57 app.services.ai.http_ai_service INFO   API 响应完成，共接收 5 个数据块，总长度: 712
10:09:57 app.services.ai.http_ai_service INFO   流式响应Token统计: 9917 (prompt=9597, completion=320)
10:09:57 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:09:57 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:09:57 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=9917, cost=$0.015196, time=5756ms
10:09:57 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=9917
10:09:57 app.services.agent.langgraph_agent INFO   [JSON解析] 方法1成功: 直接解析
10:09:57 app.services.agent.langgraph_agent INFO   [Planning] 思维链: 输出=用户想了解“庞博”这个角色的身份信息，需要对相关文本进行分析, 原料=需要搜索作品中关于“庞博”的信息片段。, 处理=使用 search_analysis_f
10:09:57 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共2个任务，耗时: 5.79s
10:09:57 app.api.v1.agent INFO   [Stream] Plan tasks: 2 items
10:09:57 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
10:09:57 app.services.agent.langgraph_agent INFO   [DeepAgent] 启用反思模式
10:09:57 app.services.agent.parameter_resolver INFO   [ParameterResolver] 初始化完成, 严格模式: False
10:09:57 app.services.agent.langgraph_agent INFO   [DeepAgent] ParameterResolver 已启用
10:09:57 app.services.agent.deep_agent.executor INFO   DeepAgent 开始执行，共 2 个任务，反思功能已启用
10:09:57 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] AI 推断功能已启用
10:09:57 app.api.v1.agent INFO   [Stream] Task started: 搜索关于“庞博”的信息片段
10:09:57 app.services.chapter_vector_service INFO   RAG retrieve work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18, current_order=1000000, query=庞博...
10:09:57 app.services.chapter_vector_service INFO   RAG retrieved 10 segments within order<=1000002
10:09:57 app.services.agent.langgraph_tools INFO   [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
10:09:57 app.api.v1.agent INFO   [Stream] 任务完成: 搜索关于“庞博”的信息片段 (0.3s)
10:09:57 app.services.agent.deep_agent.reflection INFO   [Checkpoint] 任务 1 标记了 checkpoint，触发反思
10:09:57 app.services.agent.deep_agent.executor INFO   任务 1 触发反思检查点
10:09:57 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:09:57 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:09:57 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
10:10:00 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:10:01 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
10:10:01 app.services.ai.http_ai_service INFO   流式响应Token统计: 464 (prompt=463, completion=1)
10:10:01 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:10:01 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:10:01 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=464, cost=$0.000589, time=4038ms
10:10:01 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=464
10:10:01 app.services.agent.deep_agent.reflection INFO   [DeepAgent反思] 开始调用 AI，task_id=1
10:10:01 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:10:01 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:10:01 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=500, temp=0.3, task_type=TaskType.SIMPLE_QA
10:10:03 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:10:07 app.services.ai.http_ai_service INFO   API 响应完成，共接收 2 个数据块，总长度: 136
10:10:07 app.services.ai.http_ai_service INFO   流式响应Token统计: 1680 (prompt=1607, completion=73)
10:10:07 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:10:07 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:10:07 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1680, cost=$0.002739, time=5850ms
10:10:07 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=1680
10:10:07 app.services.agent.deep_agent.reflection INFO   [Reflection] JSON提取成功: needs_replan=True
10:10:07 app.services.agent.deep_agent.executor INFO   [Reflection] 前置任务不触发重规划（已有后续输出任务）
10:10:07 app.api.v1.agent INFO   [Stream] Task started: 分析“庞博”的身份信息
10:10:07 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
10:10:07 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
10:10:07 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
10:10:11 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:10:26 app.services.ai.http_ai_service INFO   API 响应完成，共接收 26 个数据块，总长度: 2242
10:10:26 app.services.ai.http_ai_service INFO   流式响应Token统计: 5254 (prompt=3606, completion=1648)
10:10:26 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:10:26 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:10:26 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=5254, cost=$0.020987, time=19025ms
10:10:26 app.services.agent.langgraph_tools INFO   ✅ [Agent分析] 分析完成，结果长度: 2242
10:10:26 app.api.v1.agent INFO   [Stream] 任务完成: 分析“庞博”的身份信息 (19.0s)
10:10:26 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:10:26 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:10:26 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
10:10:27 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:10:28 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
10:10:28 app.services.ai.http_ai_service INFO   流式响应Token统计: 513 (prompt=512, completion=1)
10:10:28 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:10:28 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:10:28 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=513, cost=$0.000650, time=2450ms
10:10:28 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=513
10:10:28 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:10:28 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:10:28 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
10:10:30 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:10:32 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
10:10:32 app.services.ai.http_ai_service INFO   流式响应Token统计: 546 (prompt=545, completion=1)
10:10:32 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:10:32 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:10:32 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=546, cost=$0.000691, time=3318ms
10:10:32 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=546
10:10:32 app.services.agent.deep_agent.executor INFO   DeepAgent 执行完成: 任务=2, 反思=1, 重规划=0
10:10:32 app.services.agent.langgraph_agent INFO   [DeepAgent] 执行完成: 反思=1次, 重规划=0次
10:10:32 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共2个任务，耗时: 35.10s
10:10:32 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
10:10:32 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=1, 输出型=1, 展示型=0
10:10:32 app.services.agent.langgraph_agent INFO   [Response] 单个分析任务(analyze_text_tool)，使用AI格式化
10:10:32 app.services.agent.langgraph_agent INFO   [Summarization] 使用AI整合任务结果
10:10:32 app.services.agent.langgraph_agent INFO   [Summarization] 上下文压缩: 原始=5362字符, 压缩后=2144字符, 压缩率=61%
10:10:32 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
10:10:32 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
10:10:32 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
10:10:34 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:10:37 app.services.ai.http_ai_service INFO   API 响应完成，共接收 3 个数据块，总长度: 248
10:10:37 app.services.ai.http_ai_service INFO   流式响应Token统计: 2441 (prompt=2268, completion=173)
10:10:37 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:10:37 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:10:37 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2441, cost=$0.004565, time=5085ms
10:10:37 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=2441
10:10:38 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 隔离=work:07251ab5-98b3-4df7-b5f2-2bdb75201d18 | 重要度=0.92
10:10:38 app.services.context.store INFO   [ContextStore] 保存上下文: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:ab8f921b-2735-4d92-a8cf-9c8d418d9c97, token=3390
10:10:38 app.services.context.manager INFO   [ContextManager] 更新上下文: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:ab8f921b-2735-4d92-a8cf-9c8d418d9c97, 消息数=4, Token=3390
10:10:38 app.services.agent.langgraph_agent INFO   [Planning] 已保存对话到 ContextManager (session=602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:ab8f921b-2735-4d92-a8cf-9c8d418d9c97)
10:10:38 app.api.v1.agent INFO   [Stream] 跳过最终响应（内容已流式发送）
10:10:38 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed
10:13:00 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
10:13:00 app.services.ai.http_ai_service INFO   ModelSelector 已启用
10:13:00 app.services.ai.http_ai_service INFO   AILogService 已启用 (用于成本追踪)
10:13:01 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
10:13:01 app.api.v1.agent INFO   [Chat Stream] Mode: planning
10:13:01 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:53329 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
10:13:01 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: planning, Message: 周毅有什么背景？...
10:13:01 app.api.v1.agent INFO   [agent_chat_stream] 📥 收到的 context 字段:
10:13:01 app.api.v1.agent INFO     - selected_text: N/A...
10:13:01 app.api.v1.agent INFO     - selection_position: N/A
10:13:01 app.api.v1.agent INFO     - chapter_context: 当前章节ID: a4044c3a-34f8-45c0-a992-871db188810d...
10:13:01 app.api.v1.agent INFO     - instruction_context: N/A...
10:13:01 app.services.agent.langgraph_agent INFO   [Planning] 使用隔离的thread_id: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:ab8f921b-2735-4d92-a8cf-9c8d418d9c97 (user_id=602f5147-846a-4cde-95d3-405fa75f133f, work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18, conversation_id=ab8f921b-2735-4d92-a8cf-9c8d418d9c97)
10:13:01 app.services.context.store INFO   [ContextStore] 加载上下文: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:ab8f921b-2735-4d92-a8cf-9c8d418d9c97, 4条消息
10:13:01 app.services.context.manager INFO   [ContextManager] Session 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:ab8f921b-2735-4d92-a8cf-9c8d418d9c97: 3390/16000 tokens
10:13:01 app.services.context.vector_memory_store INFO   🔍 检索记忆 | 查询='周毅有什么背景？...' | 隔离键=['user:602f5147-846a-4cde-95d3-405fa75f133f:work:07251ab5-98b3-4df7-b5f2-2bdb75201d18', 'user:602f5147-846a-4cde-95d3-405fa75f133f'] | 找到=3条
10:13:01 app.services.context.manager INFO   🔍 检索长期记忆 | 级别=work | work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18 | 含用户级=True | 找到=3条
10:13:01 app.services.context.monitoring_integration INFO   [Monitor] 上下文构建: 5条消息, 3390 tokens, 耗时 91.09ms
10:13:01 app.services.agent.langgraph_agent INFO   [Planning] 从 ContextManager 加载了 5 条历史消息 (token: 3390)
10:13:01 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: 周毅有什么背景？...
10:13:01 app.core.cache INFO   ✅ 缓存命中: prompt:planning_agent:v2.9.1:get_planning_agent_mode_prompt:fca6eb91156619d0
10:13:01 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:13:01 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:13:01 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=1200, temp=0.3, task_type=TaskType.SIMPLE_QA
10:13:04 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:13:07 app.services.ai.http_ai_service INFO   API 响应完成，共接收 5 个数据块，总长度: 637
10:13:07 app.services.ai.http_ai_service INFO   流式响应Token统计: 10076 (prompt=9790, completion=286)
10:13:07 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:13:07 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:13:07 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=10076, cost=$0.015097, time=5320ms
10:13:07 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=10076
10:13:07 app.services.agent.langgraph_agent INFO   [JSON解析] 方法1成功: 直接解析
10:13:07 app.services.agent.langgraph_agent INFO   [Planning] 思维链: 输出=用户期望看到关于“周毅”背景信息的分析报告。, 原料=需要搜索作品中关于“周毅”的所有相关信息, 处理=首先使用检索工具查找包含“周毅”的信息片
10:13:07 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共2个任务，耗时: 5.35s
10:13:07 app.api.v1.agent INFO   [Stream] Plan tasks: 2 items
10:13:07 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
10:13:07 app.services.agent.langgraph_agent INFO   [DeepAgent] 启用反思模式
10:13:07 app.services.agent.parameter_resolver INFO   [ParameterResolver] 初始化完成, 严格模式: False
10:13:07 app.services.agent.langgraph_agent INFO   [DeepAgent] ParameterResolver 已启用
10:13:07 app.services.agent.deep_agent.executor INFO   DeepAgent 开始执行，共 2 个任务，反思功能已启用
10:13:07 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] AI 推断功能已启用
10:13:07 app.api.v1.agent INFO   [Stream] Task started: 搜索关于“周毅”的文本片段
10:13:07 app.services.chapter_vector_service INFO   RAG retrieve work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18, current_order=1000000, query=周毅...
10:13:07 app.services.chapter_vector_service INFO   RAG retrieved 10 segments within order<=1000002
10:13:07 app.services.agent.langgraph_tools INFO   [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
10:13:07 app.api.v1.agent INFO   [Stream] 任务完成: 搜索关于“周毅”的文本片段 (0.2s)
10:13:07 app.services.agent.deep_agent.reflection INFO   [Checkpoint] 任务 1 标记了 checkpoint，触发反思
10:13:07 app.services.agent.deep_agent.executor INFO   任务 1 触发反思检查点
10:13:07 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:13:07 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:13:07 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
10:13:09 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:13:10 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
10:13:10 app.services.ai.http_ai_service INFO   流式响应Token统计: 518 (prompt=517, completion=1)
10:13:10 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:13:10 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:13:10 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=518, cost=$0.000656, time=3246ms
10:13:10 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=518
10:13:10 app.services.agent.deep_agent.reflection INFO   [DeepAgent反思] 开始调用 AI，task_id=1
10:13:10 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:13:10 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:13:10 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=500, temp=0.3, task_type=TaskType.SIMPLE_QA
10:13:12 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:13:15 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 110
10:13:15 app.services.ai.http_ai_service INFO   流式响应Token统计: 1345 (prompt=1291, completion=54)
10:13:15 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:13:15 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:13:15 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1345, cost=$0.002154, time=5248ms
10:13:15 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=1345
10:13:15 app.services.agent.deep_agent.reflection INFO   [Reflection] JSON提取成功: needs_replan=False
10:13:15 app.api.v1.agent INFO   [Stream] Task started: 分析搜索结果，总结周毅的背景信息
10:13:15 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
10:13:15 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
10:13:15 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
10:13:18 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:13:34 app.services.ai.http_ai_service INFO   API 响应完成，共接收 23 个数据块，总长度: 2042
10:13:34 app.services.ai.http_ai_service INFO   流式响应Token统计: 6176 (prompt=4716, completion=1460)
10:13:34 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:13:34 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:13:34 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=6176, cost=$0.020495, time=18442ms
10:13:34 app.services.agent.langgraph_tools INFO   ✅ [Agent分析] 分析完成，结果长度: 2042
10:13:34 app.api.v1.agent INFO   [Stream] 任务完成: 分析搜索结果，总结周毅的背景信息 (18.5s)
10:13:34 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:13:34 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:13:34 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
10:13:36 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:13:37 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
10:13:37 app.services.ai.http_ai_service INFO   流式响应Token统计: 464 (prompt=463, completion=1)
10:13:37 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:13:37 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:13:37 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=464, cost=$0.000589, time=3469ms
10:13:37 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=464
10:13:37 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:13:37 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:13:37 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
10:13:39 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:13:40 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
10:13:40 app.services.ai.http_ai_service INFO   流式响应Token统计: 451 (prompt=450, completion=1)
10:13:40 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:13:40 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:13:40 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=451, cost=$0.000572, time=2546ms
10:13:40 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=451
10:13:40 app.services.agent.deep_agent.executor INFO   DeepAgent 执行完成: 任务=2, 反思=1, 重规划=0
10:13:40 app.services.agent.langgraph_agent INFO   [DeepAgent] 执行完成: 反思=1次, 重规划=0次
10:13:40 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共2个任务，耗时: 33.24s
10:13:40 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
10:13:40 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=1, 输出型=1, 展示型=0
10:13:40 app.services.agent.langgraph_agent INFO   [Response] 单个分析任务(analyze_text_tool)，使用AI格式化
10:13:40 app.services.agent.langgraph_agent INFO   [Summarization] 使用AI整合任务结果
10:13:40 app.services.agent.langgraph_agent INFO   [Summarization] 上下文压缩: 原始=5557字符, 压缩后=2143字符, 压缩率=62%
10:13:40 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
10:13:40 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
10:13:40 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
10:13:43 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:13:44 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 63
10:13:44 app.services.ai.http_ai_service INFO   流式响应Token统计: 1912 (prompt=1873, completion=39)
10:13:44 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:13:44 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:13:44 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1912, cost=$0.002731, time=3849ms
10:13:44 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=1912
10:13:44 app.services.context.vector_memory_store INFO   🔁 跳过重复记忆，复用ID=602f5147-846a-4cde-95d3-405fa75f133f_1765503558784_d8fceede
10:13:44 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 隔离=work:07251ab5-98b3-4df7-b5f2-2bdb75201d18 | 重要度=0.89
10:13:44 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 隔离=work:07251ab5-98b3-4df7-b5f2-2bdb75201d18 | 重要度=0.79
10:13:44 app.services.context.store INFO   [ContextStore] 保存上下文: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:ab8f921b-2735-4d92-a8cf-9c8d418d9c97, token=3432
10:13:44 app.services.context.manager INFO   [ContextManager] 更新上下文: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:ab8f921b-2735-4d92-a8cf-9c8d418d9c97, 消息数=6, Token=3432
10:13:44 app.services.agent.langgraph_agent INFO   [Planning] 已保存对话到 ContextManager (session=602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:ab8f921b-2735-4d92-a8cf-9c8d418d9c97)
10:13:44 app.api.v1.agent INFO   [Stream] 跳过最终响应（内容已流式发送）
10:13:44 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed
WARNING:  WatchFiles detected changes in 'app\services\agent\langgraph_tools.py'. Reloading...
INFO:     Shutting down
INFO:     connection closed
INFO:     connection closed
INFO:     connection closed
INFO:     connection closed
INFO:     connection closed
INFO:     Waiting for application shutdown.
10:22:45 app.main INFO   [SHUTDOWN] 应用关闭中...
10:22:45 app.tasks.cleanup_humanize_details INFO   定时任务调度器已停止
10:22:45 apscheduler.scheduler INFO   Scheduler has been shut down
10:22:45 app.main INFO   [SHUTDOWN] 应用已关闭
INFO:     Application shutdown complete.
INFO:     Finished server process [37884]
WARNING:  WatchFiles detected changes in 'app\services\agent\langgraph_agent.py', 'app\services\agent\langgraph_tools.py'. Reloading...
Process SpawnProcess-22:
Traceback (most recent call last):
  File "C:\Program Files\Python312\Lib\multiprocessing\process.py", line 314, in _bootstrap
    self.run()
  File "C:\Program Files\Python312\Lib\multiprocessing\process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\uvicorn\_subprocess.py", line 72, in subprocess_started
    sys.stdin = os.fdopen(stdin_fileno)
                ^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen os>", line 1066, in fdopen
  File "<frozen codecs>", line 309, in __init__
KeyboardInterrupt
已注册策略: web_novel_11d - 网文11维度分析
10:23:12 app.utils.file_storage INFO   临时文件存储目录: D:\Temp\novelaide_exports
10:23:13 app.main INFO   [STARTUP] 监控中间件已注册: TraceMiddleware, MonitoringMiddleware
INFO:     Started server process [21808]
INFO:     Waiting for application startup.
10:23:13 app.main INFO   [STARTUP] 应用启动中...
10:23:13 app.core.database INFO   正在初始化数据库... (尝试 1/3)
10:23:13 app.core.database INFO   ✅ 数据库初始化成功
10:23:13 apscheduler.scheduler INFO   Adding job tentatively -- it will be properly scheduled when the scheduler starts
10:23:13 apscheduler.scheduler INFO   Adding job tentatively -- it will be properly scheduled when the scheduler starts
10:23:13 apscheduler.scheduler INFO   Added job "清理过期的去痕迹会话详情" to job store "default"
10:23:13 apscheduler.scheduler INFO   Added job "清理过期的 Agent 会话" to job store "default"
10:23:13 apscheduler.scheduler INFO   Scheduler started
10:23:13 app.tasks.cleanup_humanize_details INFO   定时任务调度器已启动
10:23:13 app.main INFO   [STARTUP] 开始预初始化同步Redis连接...
10:23:13 app.api.v1.agent INFO   [Redis] 全局连接池已创建
10:23:13 app.main INFO   [STARTUP] ✅ 同步Redis连接池预初始化完成
10:23:13 app.main INFO   [STARTUP] 开始初始化AsyncRedisSaver索引...
10:23:13 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ setup_checkpointer Redis连接验证成功
10:23:13 redisvl.index.index INFO   Index already exists, not overwriting.
10:23:13 redisvl.index.index INFO   Index already exists, not overwriting.
10:23:13 redisvl.index.index INFO   Index already exists, not overwriting.
10:23:13 langgraph.checkpoint.redis.aio INFO   Redis client is a standalone client
10:23:13 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ AsyncRedisSaver索引预创建成功
10:23:13 app.main INFO   [STARTUP] AsyncRedisSaver索引初始化完成
10:23:13 app.main INFO   [STARTUP] 开始预加载Embedding模型...
10:23:13 app.services.vector_store_service INFO   🔄 预加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
10:23:21 app.services.vector_store_service INFO   ✅ Embedding模型预加载成功，耗时: 7.44秒
10:23:21 app.main INFO   [STARTUP] Embedding模型预加载完成
10:23:21 app.main INFO   [STARTUP] P0性能优化已暂时禁用（诊断模式）
10:23:21 app.main INFO   [STARTUP] 应用启动完成
INFO:     Application startup complete.
INFO:     ('127.0.0.1', 61205) - "WebSocket /api/v1/ws/notifications/602f5147-846a-4cde-95d3-405fa75f133f" [accepted]
10:23:21 app.api.v1.ws INFO   [WebSocket] 通知连接建立: user_id=602f5147-846a-4cde-95d3-405fa75f133f
INFO:     ('127.0.0.1', 54642) - "WebSocket /api/v1/ws/notifications/602f5147-846a-4cde-95d3-405fa75f133f" [accepted]
10:23:21 app.api.v1.ws INFO   [WebSocket] 通知连接建立: user_id=602f5147-846a-4cde-95d3-405fa75f133f
INFO:     ('127.0.0.1', 59316) - "WebSocket /api/v1/ws/notifications/602f5147-846a-4cde-95d3-405fa75f133f" [accepted]
10:23:21 app.api.v1.ws INFO   [WebSocket] 通知连接建立: user_id=602f5147-846a-4cde-95d3-405fa75f133f
INFO:     ('127.0.0.1', 57419) - "WebSocket /api/v1/ws/notifications/602f5147-846a-4cde-95d3-405fa75f133f" [accepted]
10:23:21 app.api.v1.ws INFO   [WebSocket] 通知连接建立: user_id=602f5147-846a-4cde-95d3-405fa75f133f
INFO:     connection open
INFO:     connection open
INFO:     connection open
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 52169) - "WebSocket /api/v1/ws/notifications/602f5147-846a-4cde-95d3-405fa75f133f" [accepted]
10:23:21 app.api.v1.ws INFO   [WebSocket] 通知连接建立: user_id=602f5147-846a-4cde-95d3-405fa75f133f
INFO:     connection open
10:23:21 app.api.v1.ws ERROR   [WebSocket] 通知推送错误:
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\websockets\legacy\protocol.py", line 945, in transfer_data
    message = await self.read_message()
              ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\websockets\legacy\protocol.py", line 1015, in read_message
    frame = await self.read_data_frame(max_size=self.max_size)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\websockets\legacy\protocol.py", line 1090, in read_data_frame
    frame = await self.read_frame(max_size)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\websockets\legacy\protocol.py", line 1147, in read_frame
    frame = await Frame.read(
            ^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\websockets\legacy\framing.py", line 71, in read
    data = await reader(2)
           ^^^^^^^^^^^^^^^
  File "C:\Program Files\Python312\Lib\asyncio\streams.py", line 750, in readexactly
    raise exceptions.IncompleteReadError(incomplete, n)
asyncio.exceptions.IncompleteReadError: 0 bytes read on a total of 2 expected bytes

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\uvicorn\protocols\websockets\websockets_impl.py", line 349, in asgi_send
    await self.send(data)  # type: ignore[arg-type]
    ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\websockets\legacy\protocol.py", line 620, in send
    await self.ensure_open()
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\websockets\legacy\protocol.py", line 921, in ensure_open
    raise self.connection_closed_exc()
websockets.exceptions.ConnectionClosedError: no close frame received or sent

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\api\v1\ws.py", line 196, in notifications_stream
    await websocket.send_json({
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\websockets.py", line 173, in send_json
    await self.send({"type": "websocket.send", "text": text})
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\websockets.py", line 85, in send
    await self._send(message)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\_exception_handler.py", line 50, in sender
    await send(message)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\uvicorn\protocols\websockets\websockets_impl.py", line 365, in asgi_send
    raise ClientDisconnected from exc
uvicorn.protocols.utils.ClientDisconnected
WARNING:  WatchFiles detected changes in 'app\services\agent\langgraph_agent.py'. Reloading...
INFO:     Shutting down
INFO:     connection closed
INFO:     connection closed
INFO:     connection closed
INFO:     connection closed
INFO:     Waiting for application shutdown.
10:28:56 app.main INFO   [SHUTDOWN] 应用关闭中...
10:28:56 app.tasks.cleanup_humanize_details INFO   定时任务调度器已停止
10:28:56 apscheduler.scheduler INFO   Scheduler has been shut down
10:28:56 app.main INFO   [SHUTDOWN] 应用已关闭
INFO:     Application shutdown complete.
INFO:     Finished server process [21808]
已注册策略: web_novel_11d - 网文11维度分析
10:29:17 app.utils.file_storage INFO   临时文件存储目录: D:\Temp\novelaide_exports
10:29:18 app.main INFO   [STARTUP] 监控中间件已注册: TraceMiddleware, MonitoringMiddleware
INFO:     Started server process [45592]
INFO:     Waiting for application startup.
10:29:19 app.main INFO   [STARTUP] 应用启动中...
10:29:19 app.core.database INFO   正在初始化数据库... (尝试 1/3)
10:29:19 app.core.database INFO   ✅ 数据库初始化成功
10:29:19 apscheduler.scheduler INFO   Adding job tentatively -- it will be properly scheduled when the scheduler starts
10:29:19 apscheduler.scheduler INFO   Adding job tentatively -- it will be properly scheduled when the scheduler starts
10:29:19 apscheduler.scheduler INFO   Added job "清理过期的去痕迹会话详情" to job store "default"
10:29:19 apscheduler.scheduler INFO   Added job "清理过期的 Agent 会话" to job store "default"
10:29:19 apscheduler.scheduler INFO   Scheduler started
10:29:19 app.tasks.cleanup_humanize_details INFO   定时任务调度器已启动
10:29:19 app.main INFO   [STARTUP] 开始预初始化同步Redis连接...
10:29:19 app.api.v1.agent INFO   [Redis] 全局连接池已创建
10:29:19 app.main INFO   [STARTUP] ✅ 同步Redis连接池预初始化完成
10:29:19 app.main INFO   [STARTUP] 开始初始化AsyncRedisSaver索引...
10:29:19 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ setup_checkpointer Redis连接验证成功
10:29:19 redisvl.index.index INFO   Index already exists, not overwriting.
10:29:19 redisvl.index.index INFO   Index already exists, not overwriting.
10:29:19 redisvl.index.index INFO   Index already exists, not overwriting.
10:29:19 langgraph.checkpoint.redis.aio INFO   Redis client is a standalone client
10:29:19 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ AsyncRedisSaver索引预创建成功
10:29:19 app.main INFO   [STARTUP] AsyncRedisSaver索引初始化完成
10:29:19 app.main INFO   [STARTUP] 开始预加载Embedding模型...
10:29:19 app.services.vector_store_service INFO   🔄 预加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
10:29:26 app.services.vector_store_service INFO   ✅ Embedding模型预加载成功，耗时: 7.43秒
10:29:26 app.main INFO   [STARTUP] Embedding模型预加载完成
10:29:26 app.main INFO   [STARTUP] P0性能优化已暂时禁用（诊断模式）
10:29:26 app.main INFO   [STARTUP] 应用启动完成
INFO:     Application startup complete.
INFO:     ('127.0.0.1', 61768) - "WebSocket /api/v1/ws/notifications/602f5147-846a-4cde-95d3-405fa75f133f" [accepted]
10:29:26 app.api.v1.ws INFO   [WebSocket] 通知连接建立: user_id=602f5147-846a-4cde-95d3-405fa75f133f
INFO:     ('127.0.0.1', 52183) - "WebSocket /api/v1/ws/notifications/602f5147-846a-4cde-95d3-405fa75f133f" [accepted]
10:29:26 app.api.v1.ws INFO   [WebSocket] 通知连接建立: user_id=602f5147-846a-4cde-95d3-405fa75f133f
INFO:     ('127.0.0.1', 63351) - "WebSocket /api/v1/ws/notifications/602f5147-846a-4cde-95d3-405fa75f133f" [accepted]
10:29:26 app.api.v1.ws INFO   [WebSocket] 通知连接建立: user_id=602f5147-846a-4cde-95d3-405fa75f133f
INFO:     ('127.0.0.1', 60806) - "WebSocket /api/v1/ws/notifications/602f5147-846a-4cde-95d3-405fa75f133f" [accepted]
10:29:26 app.api.v1.ws INFO   [WebSocket] 通知连接建立: user_id=602f5147-846a-4cde-95d3-405fa75f133f
INFO:     connection open
INFO:     connection open
INFO:     connection open
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 58558) - "WebSocket /api/v1/ws/notifications/602f5147-846a-4cde-95d3-405fa75f133f" [accepted]
10:29:27 app.api.v1.ws INFO   [WebSocket] 通知连接建立: user_id=602f5147-846a-4cde-95d3-405fa75f133f
INFO:     connection open
10:29:27 app.api.v1.ws ERROR   [WebSocket] 通知推送错误:
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\websockets\legacy\protocol.py", line 945, in transfer_data
    message = await self.read_message()
              ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\websockets\legacy\protocol.py", line 1015, in read_message
    frame = await self.read_data_frame(max_size=self.max_size)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\websockets\legacy\protocol.py", line 1090, in read_data_frame
    frame = await self.read_frame(max_size)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\websockets\legacy\protocol.py", line 1147, in read_frame
    frame = await Frame.read(
            ^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\websockets\legacy\framing.py", line 71, in read
    data = await reader(2)
           ^^^^^^^^^^^^^^^
  File "C:\Program Files\Python312\Lib\asyncio\streams.py", line 750, in readexactly
    raise exceptions.IncompleteReadError(incomplete, n)
asyncio.exceptions.IncompleteReadError: 0 bytes read on a total of 2 expected bytes

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\uvicorn\protocols\websockets\websockets_impl.py", line 349, in asgi_send
    await self.send(data)  # type: ignore[arg-type]
    ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\websockets\legacy\protocol.py", line 620, in send
    await self.ensure_open()
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\websockets\legacy\protocol.py", line 921, in ensure_open
    raise self.connection_closed_exc()
websockets.exceptions.ConnectionClosedError: no close frame received or sent

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\api\v1\ws.py", line 196, in notifications_stream
    await websocket.send_json({
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\websockets.py", line 173, in send_json
    await self.send({"type": "websocket.send", "text": text})
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\websockets.py", line 85, in send
    await self._send(message)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\_exception_handler.py", line 50, in sender
    await send(message)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\uvicorn\protocols\websockets\websockets_impl.py", line 365, in asgi_send
    raise ClientDisconnected from exc
uvicorn.protocols.utils.ClientDisconnected
WARNING:  WatchFiles detected changes in 'app\services\search\hybrid_retriever.py'. Reloading...
INFO:     Shutting down
INFO:     connection closed
INFO:     connection closed
INFO:     connection closed
INFO:     connection closed
INFO:     Waiting for application shutdown.
10:33:08 app.main INFO   [SHUTDOWN] 应用关闭中...
10:33:08 app.tasks.cleanup_humanize_details INFO   定时任务调度器已停止
10:33:08 apscheduler.scheduler INFO   Scheduler has been shut down
10:33:08 app.main INFO   [SHUTDOWN] 应用已关闭
INFO:     Application shutdown complete.
INFO:     Finished server process [45592]
WARNING:  WatchFiles detected changes in 'app\services\search\hybrid_retriever.py'. Reloading...
Process SpawnProcess-25:
Traceback (most recent call last):
  File "C:\Program Files\Python312\Lib\multiprocessing\process.py", line 314, in _bootstrap
    self.run()
  File "C:\Program Files\Python312\Lib\multiprocessing\process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\uvicorn\_subprocess.py", line 72, in subprocess_started
    sys.stdin = os.fdopen(stdin_fileno)
                ^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen os>", line 1066, in fdopen
  File "<frozen codecs>", line 309, in __init__
KeyboardInterrupt
已注册策略: web_novel_11d - 网文11维度分析
10:33:28 app.utils.file_storage INFO   临时文件存储目录: D:\Temp\novelaide_exports
10:33:28 app.main INFO   [STARTUP] 监控中间件已注册: TraceMiddleware, MonitoringMiddleware
INFO:     Started server process [28332]
INFO:     Waiting for application startup.
10:33:29 app.main INFO   [STARTUP] 应用启动中...
10:33:29 app.core.database INFO   正在初始化数据库... (尝试 1/3)
10:33:29 app.core.database INFO   ✅ 数据库初始化成功
10:33:29 apscheduler.scheduler INFO   Adding job tentatively -- it will be properly scheduled when the scheduler starts
10:33:29 apscheduler.scheduler INFO   Adding job tentatively -- it will be properly scheduled when the scheduler starts
10:33:29 apscheduler.scheduler INFO   Added job "清理过期的去痕迹会话详情" to job store "default"
10:33:29 apscheduler.scheduler INFO   Added job "清理过期的 Agent 会话" to job store "default"
10:33:29 apscheduler.scheduler INFO   Scheduler started
10:33:29 app.tasks.cleanup_humanize_details INFO   定时任务调度器已启动
10:33:29 app.main INFO   [STARTUP] 开始预初始化同步Redis连接...
10:33:29 app.api.v1.agent INFO   [Redis] 全局连接池已创建
10:33:29 app.main INFO   [STARTUP] ✅ 同步Redis连接池预初始化完成
10:33:29 app.main INFO   [STARTUP] 开始初始化AsyncRedisSaver索引...
10:33:29 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ setup_checkpointer Redis连接验证成功
10:33:29 redisvl.index.index INFO   Index already exists, not overwriting.
10:33:29 redisvl.index.index INFO   Index already exists, not overwriting.
10:33:29 redisvl.index.index INFO   Index already exists, not overwriting.
10:33:29 langgraph.checkpoint.redis.aio INFO   Redis client is a standalone client
10:33:29 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ AsyncRedisSaver索引预创建成功
10:33:29 app.main INFO   [STARTUP] AsyncRedisSaver索引初始化完成
10:33:29 app.main INFO   [STARTUP] 开始预加载Embedding模型...
10:33:29 app.services.vector_store_service INFO   🔄 预加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
10:33:36 app.services.vector_store_service INFO   ✅ Embedding模型预加载成功，耗时: 7.47秒
10:33:36 app.main INFO   [STARTUP] Embedding模型预加载完成
10:33:36 app.main INFO   [STARTUP] P0性能优化已暂时禁用（诊断模式）
10:33:36 app.main INFO   [STARTUP] 应用启动完成
INFO:     Application startup complete.
INFO:     ('127.0.0.1', 61083) - "WebSocket /api/v1/ws/notifications/602f5147-846a-4cde-95d3-405fa75f133f" [accepted]
10:33:36 app.api.v1.ws INFO   [WebSocket] 通知连接建立: user_id=602f5147-846a-4cde-95d3-405fa75f133f
INFO:     ('127.0.0.1', 51236) - "WebSocket /api/v1/ws/notifications/602f5147-846a-4cde-95d3-405fa75f133f" [accepted]
10:33:36 app.api.v1.ws INFO   [WebSocket] 通知连接建立: user_id=602f5147-846a-4cde-95d3-405fa75f133f
INFO:     ('127.0.0.1', 60473) - "WebSocket /api/v1/ws/notifications/602f5147-846a-4cde-95d3-405fa75f133f" [accepted]
10:33:36 app.api.v1.ws INFO   [WebSocket] 通知连接建立: user_id=602f5147-846a-4cde-95d3-405fa75f133f
INFO:     connection open
INFO:     connection open
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 60832) - "WebSocket /api/v1/ws/notifications/602f5147-846a-4cde-95d3-405fa75f133f" [accepted]
10:33:37 app.api.v1.ws INFO   [WebSocket] 通知连接建立: user_id=602f5147-846a-4cde-95d3-405fa75f133f
INFO:     connection open
10:33:37 app.api.v1.ws ERROR   [WebSocket] 通知推送错误:
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\websockets\legacy\protocol.py", line 945, in transfer_data
    message = await self.read_message()
              ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\websockets\legacy\protocol.py", line 1015, in read_message
    frame = await self.read_data_frame(max_size=self.max_size)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\websockets\legacy\protocol.py", line 1090, in read_data_frame
    frame = await self.read_frame(max_size)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\websockets\legacy\protocol.py", line 1147, in read_frame
    frame = await Frame.read(
            ^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\websockets\legacy\framing.py", line 71, in read
    data = await reader(2)
           ^^^^^^^^^^^^^^^
  File "C:\Program Files\Python312\Lib\asyncio\streams.py", line 750, in readexactly
    raise exceptions.IncompleteReadError(incomplete, n)
asyncio.exceptions.IncompleteReadError: 0 bytes read on a total of 2 expected bytes

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\uvicorn\protocols\websockets\websockets_impl.py", line 349, in asgi_send
    await self.send(data)  # type: ignore[arg-type]
    ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\websockets\legacy\protocol.py", line 620, in send
    await self.ensure_open()
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\websockets\legacy\protocol.py", line 921, in ensure_open
    raise self.connection_closed_exc()
websockets.exceptions.ConnectionClosedError: no close frame received or sent

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\api\v1\ws.py", line 196, in notifications_stream
    await websocket.send_json({
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\websockets.py", line 173, in send_json
    await self.send({"type": "websocket.send", "text": text})
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\websockets.py", line 85, in send
    await self._send(message)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\_exception_handler.py", line 50, in sender
    await send(message)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\uvicorn\protocols\websockets\websockets_impl.py", line 365, in asgi_send
    raise ClientDisconnected from exc
uvicorn.protocols.utils.ClientDisconnected
INFO:     ('127.0.0.1', 60836) - "WebSocket /api/v1/ws/notifications/602f5147-846a-4cde-95d3-405fa75f133f" [accepted]
10:33:39 app.api.v1.ws INFO   [WebSocket] 通知连接建立: user_id=602f5147-846a-4cde-95d3-405fa75f133f
INFO:     connection open
10:35:51 monitoring INFO   Registered health check: cpu_usage
10:35:51 monitoring INFO   Registered health check: memory_usage
10:35:51 monitoring INFO   Registered health check: disk_usage
10:35:51 monitoring INFO   Registered health check: process_status
10:35:51 monitoring INFO   Added alert rule: high_cpu_usage
10:35:51 monitoring INFO   Added alert rule: high_memory_usage
10:35:51 monitoring INFO   Added alert rule: low_disk_space
10:35:51 app.api.v1.auth INFO   [LOGIN] 尝试登录: 2072855200@qq.com
10:35:52 app.api.v1.auth INFO   [LOGIN] 会话创建成功: 602f5147-846a-4cde-95d3-405fa75f133f (127.0.0.1)
10:35:52 app.api.v1.auth INFO   [LOGIN] 登录成功: testuser_new-1 (602f5147-846a-4cde-95d3-405fa75f133f) from 127.0.0.1
10:35:52 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/auth/login
INFO:     127.0.0.1:55924 - "POST /api/v1/auth/login HTTP/1.1" 200 OK
10:35:52 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/users/me
INFO:     127.0.0.1:62572 - "GET /api/v1/users/me HTTP/1.1" 200 OK
INFO:     ('127.0.0.1', 62529) - "WebSocket /api/v1/ws/notifications/602f5147-846a-4cde-95d3-405fa75f133f" [accepted]
10:35:53 app.api.v1.ws INFO   [WebSocket] 通知连接建立: user_id=602f5147-846a-4cde-95d3-405fa75f133f
INFO:     connection open
10:35:53 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works
INFO:     127.0.0.1:62531 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
10:35:53 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works
INFO:     127.0.0.1:49451 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
INFO:     ('127.0.0.1', 50341) - "WebSocket /api/v1/ws/notifications/602f5147-846a-4cde-95d3-405fa75f133f" [accepted]
10:35:58 app.api.v1.ws INFO   [WebSocket] 通知连接建立: user_id=602f5147-846a-4cde-95d3-405fa75f133f
INFO:     connection open
10:36:00 app.api.v1.chapters INFO   [GET chapters] work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:36:00 app.api.v1.chapters INFO   ⚠️ [GET chapters] 缓存未命中: chapters:work:07251ab5-98b3-4df7-b5f2-2bdb75201d18
10:36:00 app.services.chapter_service INFO   [ChapterService] Querying chapters for work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18, type=<class 'uuid.UUID'>
10:36:00 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:characters:07251ab5-98b3-4df7-b5f2-2bdb75201d18 (expire=300s)
10:36:00 app.services.chapter_service INFO   [ChapterService] Found 77 chapters
10:36:00 app.services.chapter_service INFO     - Chapter: 第1章 【摆烂的宿主】, order=1
10:36:00 app.services.chapter_service INFO     - ... (75 more chapters)
10:36:00 app.services.chapter_service INFO     - Chapter: 第100章 【火域铸真器，两脉起冲突】, order=77
10:36:00 app.api.v1.chapters INFO   [GET chapters] Returning 77 chapters
10:36:00 app.api.v1.chapters INFO   💾 [GET chapters] 缓存已保存: chapters:work:07251ab5-98b3-4df7-b5f2-2bdb75201d18 (expire=60s)
10:36:00 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/07251ab5-98b3-4df7-b5f2-2bdb75201d18/characters
10:36:00 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/chapters/work/07251ab5-98b3-4df7-b5f2-2bdb75201d18
10:36:00 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:locations:07251ab5-98b3-4df7-b5f2-2bdb75201d18 (expire=300s)
INFO:     127.0.0.1:50354 - "GET /api/v1/worldview/works/07251ab5-98b3-4df7-b5f2-2bdb75201d18/characters HTTP/1.1" 200 OK
INFO:     127.0.0.1:50353 - "GET /api/v1/chapters/work/07251ab5-98b3-4df7-b5f2-2bdb75201d18 HTTP/1.1" 200 OK
10:36:00 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works/07251ab5-98b3-4df7-b5f2-2bdb75201d18
10:36:00 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/07251ab5-98b3-4df7-b5f2-2bdb75201d18/locations
INFO:     127.0.0.1:50351 - "GET /api/v1/works/07251ab5-98b3-4df7-b5f2-2bdb75201d18 HTTP/1.1" 200 OK
INFO:     127.0.0.1:50355 - "GET /api/v1/worldview/works/07251ab5-98b3-4df7-b5f2-2bdb75201d18/locations HTTP/1.1" 200 OK
10:36:00 app.api.v1.agent WARNING   [create_agent_session] chapter_id 07251ab5-98b3-4df7-b5f2-2bdb75201d18 不存在，已忽略
10:36:00 app.api.v1.agent WARNING   [create_agent_session] chapter_id 07251ab5-98b3-4df7-b5f2-2bdb75201d18 不存在，已忽略
10:36:00 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/sessions
10:36:00 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:50352 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
INFO:     127.0.0.1:50350 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
10:36:01 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:guidelines:07251ab5-98b3-4df7-b5f2-2bdb75201d18 (expire=300s)
10:36:01 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:settings:07251ab5-98b3-4df7-b5f2-2bdb75201d18 (expire=300s)
10:36:01 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/07251ab5-98b3-4df7-b5f2-2bdb75201d18/guidelines
10:36:01 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/07251ab5-98b3-4df7-b5f2-2bdb75201d18/settings
INFO:     127.0.0.1:60104 - "GET /api/v1/worldview/works/07251ab5-98b3-4df7-b5f2-2bdb75201d18/guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:60103 - "GET /api/v1/worldview/works/07251ab5-98b3-4df7-b5f2-2bdb75201d18/settings HTTP/1.1" 200 OK
10:36:01 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:characters:07251ab5-98b3-4df7-b5f2-2bdb75201d18 (expire=300s)
10:36:01 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:ai-guidelines:07251ab5-98b3-4df7-b5f2-2bdb75201d18 (expire=300s)
10:36:01 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/07251ab5-98b3-4df7-b5f2-2bdb75201d18/characters
10:36:01 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/07251ab5-98b3-4df7-b5f2-2bdb75201d18/ai-guidelines
INFO:     127.0.0.1:60106 - "GET /api/v1/worldview/works/07251ab5-98b3-4df7-b5f2-2bdb75201d18/characters HTTP/1.1" 200 OK
INFO:     127.0.0.1:60105 - "GET /api/v1/worldview/works/07251ab5-98b3-4df7-b5f2-2bdb75201d18/ai-guidelines HTTP/1.1" 200 OK
10:36:01 app.api.v1.chapters INFO   [GET chapters] work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:36:01 app.api.v1.chapters INFO   ✅ [GET chapters] 缓存命中: chapters:work:07251ab5-98b3-4df7-b5f2-2bdb75201d18
10:36:01 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/chapters/work/07251ab5-98b3-4df7-b5f2-2bdb75201d18
10:36:01 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works/07251ab5-98b3-4df7-b5f2-2bdb75201d18
INFO:     127.0.0.1:56125 - "GET /api/v1/chapters/work/07251ab5-98b3-4df7-b5f2-2bdb75201d18 HTTP/1.1" 200 OK
INFO:     127.0.0.1:54522 - "GET /api/v1/works/07251ab5-98b3-4df7-b5f2-2bdb75201d18 HTTP/1.1" 200 OK
10:36:01 app.api.v1.worldview INFO   ✅ [Worldview] 缓存命中: worldview:guidelines:07251ab5-98b3-4df7-b5f2-2bdb75201d18
10:36:01 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:locations:07251ab5-98b3-4df7-b5f2-2bdb75201d18 (expire=300s)
10:36:01 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/07251ab5-98b3-4df7-b5f2-2bdb75201d18/guidelines
10:36:01 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/07251ab5-98b3-4df7-b5f2-2bdb75201d18/locations
INFO:     127.0.0.1:50301 - "GET /api/v1/worldview/works/07251ab5-98b3-4df7-b5f2-2bdb75201d18/guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:50300 - "GET /api/v1/worldview/works/07251ab5-98b3-4df7-b5f2-2bdb75201d18/locations HTTP/1.1" 200 OK
10:36:01 app.api.v1.worldview INFO   ✅ [Worldview] 缓存命中: worldview:ai-guidelines:07251ab5-98b3-4df7-b5f2-2bdb75201d18
10:36:01 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/07251ab5-98b3-4df7-b5f2-2bdb75201d18/ai-guidelines
INFO:     127.0.0.1:54009 - "GET /api/v1/worldview/works/07251ab5-98b3-4df7-b5f2-2bdb75201d18/ai-guidelines HTTP/1.1" 200 OK
10:36:01 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:settings:07251ab5-98b3-4df7-b5f2-2bdb75201d18 (expire=300s)
10:36:01 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/07251ab5-98b3-4df7-b5f2-2bdb75201d18/settings
INFO:     127.0.0.1:54008 - "GET /api/v1/worldview/works/07251ab5-98b3-4df7-b5f2-2bdb75201d18/settings HTTP/1.1" 200 OK
10:36:01 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/analysis/works/07251ab5-98b3-4df7-b5f2-2bdb75201d18/status
INFO:     127.0.0.1:54012 - "GET /api/v1/analysis/works/07251ab5-98b3-4df7-b5f2-2bdb75201d18/status HTTP/1.1" 404 Not Found
10:36:01 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:54013 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
10:36:01 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/analysis/works/07251ab5-98b3-4df7-b5f2-2bdb75201d18/status
INFO:     127.0.0.1:65311 - "GET /api/v1/analysis/works/07251ab5-98b3-4df7-b5f2-2bdb75201d18/status HTTP/1.1" 404 Not Found
10:36:01 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: 07251ab5-98b3-4df7-b5f2-2bdb75201d18, chapter_id: 0d076ac2-70fc-46ce-92a0-d9dfba43723b
10:36:01 app.core.redis INFO   ✅ Redis connected: redis://localhost:6379/0
10:36:01 app.api.v1.ai INFO   [预加载] 当前章节已加载: 0d076ac2-70fc-46ce-92a0-d9dfba43723b
10:36:01 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
10:36:01 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:57786 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
10:36:02 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: 07251ab5-98b3-4df7-b5f2-2bdb75201d18, chapter_id: 0d076ac2-70fc-46ce-92a0-d9dfba43723b
10:36:02 app.api.v1.ai INFO   [预加载] 当前章节已加载: 0d076ac2-70fc-46ce-92a0-d9dfba43723b
10:36:02 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
10:36:02 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:57375 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
10:36:02 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:07251ab5-98b3-4df7-b5f2-2bdb75201d18
10:36:02 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/0d076ac2-70fc-46ce-92a0-d9dfba43723b
INFO:     127.0.0.1:52083 - "PUT /api/v1/chapters/0d076ac2-70fc-46ce-92a0-d9dfba43723b HTTP/1.1" 200 OK
10:36:02 app.services.chapter_vector_service INFO   Vectorizing chapter: 第1章 【摆烂的宿主】 (order=1)
10:36:04 app.services.chapter_vector_service INFO   Stored chapter vectors: 第1章 【摆烂的宿主】 (8 chunks)
10:36:04 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:07251ab5-98b3-4df7-b5f2-2bdb75201d18
10:36:04 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/0d076ac2-70fc-46ce-92a0-d9dfba43723b
INFO:     127.0.0.1:53566 - "PUT /api/v1/chapters/0d076ac2-70fc-46ce-92a0-d9dfba43723b HTTP/1.1" 200 OK
10:36:04 app.services.chapter_vector_service INFO   Vectorizing chapter: 第1章 【摆烂的宿主】 (order=1)
10:36:06 app.services.chapter_vector_service INFO   Stored chapter vectors: 第1章 【摆烂的宿主】 (8 chunks)
10:36:33 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: 07251ab5-98b3-4df7-b5f2-2bdb75201d18, chapter_id: deae53e0-7dee-4bc7-8dc7-b122ae549845
10:36:33 app.api.v1.ai INFO   [预加载] 当前章节已加载: deae53e0-7dee-4bc7-8dc7-b122ae549845
10:36:33 app.api.v1.ai INFO   [预加载] 前一章节已加载: 407cb96c-a896-40de-b0d2-7947d54ba1fd
10:36:33 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
10:36:33 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:52510 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
10:36:33 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: 07251ab5-98b3-4df7-b5f2-2bdb75201d18, chapter_id: deae53e0-7dee-4bc7-8dc7-b122ae549845
10:36:33 app.api.v1.ai INFO   [预加载] 当前章节已加载: deae53e0-7dee-4bc7-8dc7-b122ae549845
10:36:33 app.api.v1.ai INFO   [预加载] 前一章节已加载: 407cb96c-a896-40de-b0d2-7947d54ba1fd
10:36:33 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
10:36:33 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:52512 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
10:36:33 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:52511 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
10:36:34 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:07251ab5-98b3-4df7-b5f2-2bdb75201d18
10:36:34 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/deae53e0-7dee-4bc7-8dc7-b122ae549845
INFO:     127.0.0.1:61873 - "PUT /api/v1/chapters/deae53e0-7dee-4bc7-8dc7-b122ae549845 HTTP/1.1" 200 OK
10:36:34 app.services.chapter_vector_service INFO   Vectorizing chapter: 第5章 【拳打禁区养老院，脚踢圣灵幼儿园】（4000） (order=5)
10:36:36 app.services.chapter_vector_service INFO   Stored chapter vectors: 第5章 【拳打禁区养老院，脚踢圣灵幼儿园】（4000） (10 chunks)
10:36:36 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:07251ab5-98b3-4df7-b5f2-2bdb75201d18
10:36:36 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/deae53e0-7dee-4bc7-8dc7-b122ae549845
INFO:     127.0.0.1:55894 - "PUT /api/v1/chapters/deae53e0-7dee-4bc7-8dc7-b122ae549845 HTTP/1.1" 200 OK
10:36:36 app.services.chapter_vector_service INFO   Vectorizing chapter: 第5章 【拳打禁区养老院，脚踢圣灵幼儿园】（4000） (order=5)
10:36:37 app.services.chapter_vector_service INFO   Stored chapter vectors: 第5章 【拳打禁区养老院，脚踢圣灵幼儿园】（4000） (10 chunks)
10:36:39 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:51986 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
10:36:39 app.services.ai.prompts INFO   Prompts loaded successfully from D:\Java\ai_writer\backend\app\services\ai\prompts\default.json
10:36:39 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
10:36:39 app.services.ai.http_ai_service INFO   ModelSelector 已启用
10:36:39 app.services.ai.http_ai_service INFO   AILogService 已启用 (用于成本追踪)
10:36:44 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
10:36:44 app.api.v1.agent INFO   [Chat Stream] Mode: planning
10:36:44 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:64227 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
10:36:44 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: planning, Message: 庞博的身份是什么？...
10:36:44 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
10:36:44 app.services.ai.http_ai_service INFO   ModelSelector 已启用
10:36:44 app.services.ai.http_ai_service INFO   [成本追踪] 初始化未传db/user_id，将使用请求上下文按需记录成本
10:36:47 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
10:36:47 app.services.context.adaptive_budget INFO   ✅ 所有预算配置验证通过
10:36:58 app.services.context.vector_memory_store INFO   ✅ VectorMemoryStore初始化成功 | 目录=./data/chroma_db | 模型=paraphrase-multilingual-MiniLM-L12-v2 | 集合=user_memories
10:36:58 app.services.context.manager INFO   ✅ VectorMemoryStore 已初始化
10:36:58 app.services.context.manager INFO   ✅ ContextManager: 长期记忆已启用 (user_id=None)
10:36:58 app.services.context.manager INFO   ✅ ContextManager: 自适应预算已启用
10:36:58 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ ContextManager已初始化（长期记忆已启用，自适应预算已启用，总预算=16000 tokens）
成功加载模板: analyze_text (版本 3.1.0)
成功加载模板: intent_classifier (版本 2.0.0)
成功加载模板: writing_agent (版本 2.0.0)
成功加载模板: planning_agent (版本 2.0.0)
成功加载模板: tool_agent (版本 2.0.0)
成功加载模板: query_agent (版本 2.0.0)
成功加载模板: system_agent_prompt (版本 2.0.0)
成功加载模板: creative_writing_prompt (版本 1.0.0)
10:36:58 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ PromptManager已初始化
10:36:58 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ Redis连接验证成功
10:36:58 app.services.agent.langgraph_agent INFO   [LangGraph] OK 使用 AsyncRedisSaver（redis://localhost:6379/0，TTL=7天）
10:36:58 app.services.agent.memory.metrics INFO   [MemoryMetrics] 监控系统已初始化
10:36:58 app.services.agent.memory.long_term_store INFO   [LongTermStore] Initialized: base_dir=./data/long_term_memory, max_size=50KB, compression=True
10:36:58 app.services.agent.memory.enhanced_memory_manager INFO   EnhancedMemoryManager initialized: short=10, medium=100, threshold=0.1, long_term_backup=enabled
10:36:58 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ EnhancedMemoryManager已创建
10:36:58 app.services.agent.memory.unified_coordinator INFO   [UnifiedMemoryCoordinator] 初始化统一记忆协调器
10:36:58 app.services.agent.memory.unified_coordinator INFO   [UnifiedMemoryCoordinator] 全局实例已设置
10:36:58 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ UnifiedMemoryCoordinator已初始化 | checkpointer=AsyncRedisSaver | enhanced_memory=yes | context_manager=yes
10:36:58 app.services.agent.parallel_tool_node INFO   [ParallelToolNode] 初始化完成，最大并发数=5，并行安全工具=4个
10:36:58 app.api.v1.agent INFO   [Global Agent] created global agent instance; MemorySaver shared across requests
10:36:58 app.api.v1.agent INFO   [agent_chat_stream] 📥 收到的 context 字段:
10:36:58 app.api.v1.agent INFO     - selected_text: N/A...
10:36:58 app.api.v1.agent INFO     - selection_position: N/A
10:36:58 app.api.v1.agent INFO     - chapter_context: 当前章节ID: deae53e0-7dee-4bc7-8dc7-b122ae549845...
10:36:58 app.api.v1.agent INFO     - instruction_context: N/A...
10:36:58 app.services.agent.langgraph_agent INFO   [Planning] 使用隔离的thread_id: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:d7764e19-4eef-47cd-8b18-a05515ee87f0 (user_id=602f5147-846a-4cde-95d3-405fa75f133f, work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18, conversation_id=d7764e19-4eef-47cd-8b18-a05515ee87f0)
10:36:58 app.services.context.monitoring_integration INFO   ✅ ContextManager监控收集器已初始化
10:36:58 app.services.context.store INFO   [ContextStore] Redis连接成功
10:36:58 app.services.context.manager INFO   [ContextManager] 创建新上下文: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:d7764e19-4eef-47cd-8b18-a05515ee87f0
10:36:58 app.services.context.token_counter WARNING   ⚠️ tiktoken初始化失败: 'Could not automatically map gemini-2.5-pro to a tokeniser. Please use `tiktoken.get_encoding` to explicitly get the tokeniser you expect.'，将使用降级策略
10:36:58 app.services.context.manager INFO   [ContextManager] Session 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:d7764e19-4eef-47cd-8b18-a05515ee87f0: 0/16000 tokens
10:36:59 app.services.context.vector_memory_store INFO   🔍 检索记忆 | 查询='庞博的身份是什么？...' | 隔离键=['user:602f5147-846a-4cde-95d3-405fa75f133f:work:07251ab5-98b3-4df7-b5f2-2bdb75201d18', 'user:602f5147-846a-4cde-95d3-405fa75f133f'] | 找到=3条
10:36:59 app.services.context.manager INFO   🔍 检索长期记忆 | 级别=work | work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18 | 含用户级=True | 找到=3条
10:36:59 app.services.context.monitoring_integration INFO   [Monitor] 上下文构建: 1条消息, 0 tokens, 耗时 996.86ms
10:36:59 app.services.agent.langgraph_agent INFO   [Planning] 从 ContextManager 加载了 1 条历史消息 (token: 0)
10:36:59 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: 庞博的身份是什么？...
10:36:59 app.core.cache INFO   ✅ 缓存命中: prompt:planning_agent:v2.9.1:get_planning_agent_mode_prompt:fca6eb91156619d0
10:36:59 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:36:59 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:36:59 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=1200, temp=0.3, task_type=TaskType.SIMPLE_QA
10:37:01 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:37:04 app.services.ai.http_ai_service INFO   API 响应完成，共接收 4 个数据块，总长度: 523
10:37:04 app.services.ai.http_ai_service INFO   流式响应Token统计: 5253 (prompt=4996, completion=257)
10:37:04 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:37:04 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:37:04 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=5253, cost=$0.008815, time=4880ms
10:37:04 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=5253
10:37:04 app.services.agent.langgraph_agent INFO   [JSON解析] 方法2成功: 从```json块提取
10:37:04 app.services.agent.langgraph_agent INFO   [Planning] 思维链: 输出=用户想知道“庞博”这个角色的身份信息，期望得到一个关于这个角, 原料=需要搜索作品中关于“庞博”的所有相关信息, 处理=使用搜索工具查找包含“庞博”的文本片段，
10:37:04 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共1个任务，耗时: 4.93s
10:37:04 app.api.v1.agent INFO   [Stream] Plan tasks: 1 items
10:37:04 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
10:37:04 app.services.agent.langgraph_agent INFO   [DeepAgent] 启用反思模式
10:37:04 app.services.agent.parameter_resolver INFO   [ParameterResolver] 初始化完成, 严格模式: False
10:37:04 app.services.agent.langgraph_agent INFO   [DeepAgent] ParameterResolver 已启用
10:37:04 app.services.agent.deep_agent.executor INFO   DeepAgent 开始执行，共 1 个任务，反思功能已启用
10:37:04 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] AI 推断功能已启用
10:37:04 app.api.v1.agent INFO   [Stream] Task started: 搜索作品中关于“庞博”身份的信息片段
10:37:05 app.services.chapter_vector_service INFO   RAG retrieve work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18, current_order=5, query=庞博的身份...
10:37:05 app.services.chapter_vector_service INFO   RAG retrieved 10 segments within order<=7
Building prefix dict from the default dictionary ...
10:37:05 jieba DEBUG   Building prefix dict from the default dictionary ...
Loading model from cache D:\Temp\jieba.cache
10:37:05 jieba DEBUG   Loading model from cache D:\Temp\jieba.cache
Loading model cost 0.989 seconds.
10:37:06 jieba DEBUG   Loading model cost 0.989 seconds.
Prefix dict has been built successfully.
10:37:06 jieba DEBUG   Prefix dict has been built successfully.
10:37:06 app.services.agent.langgraph_tools INFO   [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
10:37:06 app.api.v1.agent INFO   [Stream] 任务完成: 搜索作品中关于“庞博”身份的信息片段 (2.2s)
10:37:06 app.services.agent.deep_agent.reflection INFO   [Checkpoint] 任务 1 标记了 checkpoint，触发反思
10:37:06 app.services.agent.deep_agent.executor INFO   任务 1 触发反思检查点
10:37:06 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:37:06 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:37:06 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
10:37:08 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:37:10 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
10:37:10 app.services.ai.http_ai_service INFO   流式响应Token统计: 468 (prompt=467, completion=1)
10:37:10 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:37:10 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:37:10 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=468, cost=$0.000594, time=3659ms
10:37:10 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=468
10:37:10 app.services.agent.deep_agent.reflection INFO   [DeepAgent反思] 开始调用 AI，task_id=1
10:37:10 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:37:10 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:37:10 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=500, temp=0.3, task_type=TaskType.SIMPLE_QA
10:37:12 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:37:15 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 108
10:37:15 app.services.ai.http_ai_service INFO   流式响应Token统计: 1339 (prompt=1283, completion=56)
10:37:15 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:37:15 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:37:15 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1339, cost=$0.002164, time=5468ms
10:37:15 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=1339
10:37:15 app.services.agent.deep_agent.reflection INFO   [Reflection] JSON提取成功: needs_replan=False
10:37:15 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:37:15 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:37:15 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
10:37:17 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:37:19 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
10:37:19 app.services.ai.http_ai_service INFO   流式响应Token统计: 462 (prompt=461, completion=1)
10:37:19 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:37:19 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:37:19 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=462, cost=$0.000586, time=3534ms
10:37:19 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=462
10:37:19 app.services.agent.deep_agent.executor INFO   DeepAgent 执行完成: 任务=1, 反思=1, 重规划=0
10:37:19 app.services.agent.langgraph_agent INFO   [DeepAgent] 执行完成: 反思=1次, 重规划=0次
10:37:19 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共1个任务，耗时: 14.99s
10:37:19 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
10:37:19 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=1, 输出型=0, 展示型=0
10:37:19 app.services.agent.langgraph_agent WARNING   [Response] 没有明确输出任务，使用AI整合
10:37:19 app.services.agent.langgraph_agent INFO   [Summarization] 使用AI整合任务结果
10:37:19 app.services.agent.langgraph_agent INFO   [Summarization] 上下文压缩: 原始=3527字符, 压缩后=120字符, 压缩率=97%
10:37:19 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
10:37:19 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
10:37:19 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
10:37:21 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:37:22 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 69
10:37:22 app.services.ai.http_ai_service INFO   流式响应Token统计: 478 (prompt=433, completion=45)
10:37:22 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:37:22 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:37:22 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=478, cost=$0.000991, time=3683ms
10:37:22 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=478
10:37:23 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 隔离=work:07251ab5-98b3-4df7-b5f2-2bdb75201d18 | 重要度=0.54
10:37:23 app.services.context.store INFO   [ContextStore] 保存上下文: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:d7764e19-4eef-47cd-8b18-a05515ee87f0, token=47
10:37:23 app.services.context.manager INFO   [ContextManager] 更新上下文: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:d7764e19-4eef-47cd-8b18-a05515ee87f0, 消息数=2, Token=47
10:37:23 app.services.agent.langgraph_agent INFO   [Planning] 已保存对话到 ContextManager (session=602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:d7764e19-4eef-47cd-8b18-a05515ee87f0)
10:37:23 app.api.v1.agent INFO   [Stream] 跳过最终响应（内容已流式发送）
10:37:23 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed
10:37:47 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
10:37:47 app.services.ai.http_ai_service INFO   ModelSelector 已启用
10:37:47 app.services.ai.http_ai_service INFO   AILogService 已启用 (用于成本追踪)
10:37:50 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
10:37:50 app.api.v1.agent INFO   [Chat Stream] Mode: planning
10:37:50 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:54813 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
10:37:50 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: planning, Message: 林仙是谁？...
10:37:50 app.api.v1.agent INFO   [agent_chat_stream] 📥 收到的 context 字段:
10:37:50 app.api.v1.agent INFO     - selected_text: N/A...
10:37:50 app.api.v1.agent INFO     - selection_position: N/A
10:37:50 app.api.v1.agent INFO     - chapter_context: 当前章节ID: deae53e0-7dee-4bc7-8dc7-b122ae549845...
10:37:50 app.api.v1.agent INFO     - instruction_context: N/A...
10:37:50 app.services.agent.langgraph_agent INFO   [Planning] 使用隔离的thread_id: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:d7764e19-4eef-47cd-8b18-a05515ee87f0 (user_id=602f5147-846a-4cde-95d3-405fa75f133f, work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18, conversation_id=d7764e19-4eef-47cd-8b18-a05515ee87f0)
10:37:50 app.services.context.store INFO   [ContextStore] 加载上下文: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:d7764e19-4eef-47cd-8b18-a05515ee87f0, 2条消息
10:37:50 app.services.context.manager INFO   [ContextManager] Session 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:d7764e19-4eef-47cd-8b18-a05515ee87f0: 47/16000 tokens
10:37:50 app.services.context.vector_memory_store INFO   🔍 检索记忆 | 查询='林仙是谁？...' | 隔离键=['user:602f5147-846a-4cde-95d3-405fa75f133f:work:07251ab5-98b3-4df7-b5f2-2bdb75201d18', 'user:602f5147-846a-4cde-95d3-405fa75f133f'] | 找到=3条
10:37:50 app.services.context.manager INFO   🔍 检索长期记忆 | 级别=work | work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18 | 含用户级=True | 找到=3条
10:37:50 app.services.context.monitoring_integration INFO   [Monitor] 上下文构建: 3条消息, 47 tokens, 耗时 204.70ms
10:37:50 app.services.agent.langgraph_agent INFO   [Planning] 从 ContextManager 加载了 3 条历史消息 (token: 47)
10:37:50 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: 林仙是谁？...
10:37:50 app.core.cache INFO   ✅ 缓存命中: prompt:planning_agent:v2.9.1:get_planning_agent_mode_prompt:fca6eb91156619d0
10:37:50 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:37:50 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:37:50 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=1200, temp=0.3, task_type=TaskType.SIMPLE_QA
10:37:53 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:37:59 app.services.ai.http_ai_service INFO   API 响应完成，共接收 10 个数据块，总长度: 897
10:37:59 app.services.ai.http_ai_service INFO   流式响应Token统计: 6045 (prompt=5593, completion=452)
10:37:59 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:37:59 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:37:59 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=6045, cost=$0.011511, time=8735ms
10:37:59 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=6045
10:37:59 app.services.agent.langgraph_agent INFO   [JSON解析] 方法2成功: 从```json块提取
10:37:59 app.services.agent.langgraph_agent INFO   [Planning] 思维链: 输出=用户期望看到关于“林仙”身份的概括性描述，而不是原文或大纲。, 原料=需要查找包含“林仙”这个名字的文本片段，, 处理=使用检索工具查找相关片段，然后使用分析工
10:37:59 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共2个任务，耗时: 8.81s
10:37:59 app.api.v1.agent INFO   [Stream] Plan tasks: 2 items
10:37:59 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
10:37:59 app.services.agent.langgraph_agent INFO   [DeepAgent] 启用反思模式
10:37:59 app.services.agent.parameter_resolver INFO   [ParameterResolver] 初始化完成, 严格模式: False
10:37:59 app.services.agent.langgraph_agent INFO   [DeepAgent] ParameterResolver 已启用
10:37:59 app.services.agent.deep_agent.executor INFO   DeepAgent 开始执行，共 2 个任务，反思功能已启用
10:37:59 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] AI 推断功能已启用
10:37:59 app.api.v1.agent INFO   [Stream] Task started: 在指定章节和作品中搜索关于“林仙”的信息片段。
10:37:59 app.services.chapter_vector_service INFO   RAG retrieve work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18, current_order=5, query=林仙...
10:37:59 app.services.chapter_vector_service INFO   RAG retrieved 10 segments within order<=7
10:37:59 app.services.agent.langgraph_tools INFO   [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
10:37:59 app.api.v1.agent INFO   [Stream] 任务完成: 在指定章节和作品中搜索关于“林仙”的信息片段。 (0.3s)
10:37:59 app.services.agent.deep_agent.reflection INFO   [Checkpoint] 任务 1 标记了 checkpoint，触发反思
10:37:59 app.services.agent.deep_agent.executor INFO   任务 1 触发反思检查点
10:37:59 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:37:59 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:37:59 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
10:38:01 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:38:03 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
10:38:03 app.services.ai.http_ai_service INFO   流式响应Token统计: 458 (prompt=457, completion=1)
10:38:03 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:38:03 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:38:03 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=458, cost=$0.000581, time=3702ms
10:38:03 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=458
10:38:03 app.services.agent.deep_agent.reflection INFO   [DeepAgent反思] 开始调用 AI，task_id=1
10:38:03 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:38:03 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:38:03 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=500, temp=0.3, task_type=TaskType.SIMPLE_QA
10:38:05 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:38:09 app.services.ai.http_ai_service INFO   API 响应完成，共接收 2 个数据块，总长度: 143
10:38:09 app.services.ai.http_ai_service INFO   流式响应Token统计: 1452 (prompt=1377, completion=75)
10:38:09 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:38:09 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:38:09 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1452, cost=$0.002471, time=5411ms
10:38:09 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=1452
10:38:09 app.services.agent.deep_agent.reflection INFO   [Reflection] JSON提取成功: needs_replan=True
10:38:09 app.services.agent.deep_agent.executor INFO   [Reflection] 前置任务不触发重规划（已有后续输出任务）
10:38:09 app.api.v1.agent INFO   [Stream] Task started: 根据搜索到的片段，概括林仙的身份信息。
10:38:09 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
10:38:09 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
10:38:09 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
10:38:11 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:38:33 app.services.ai.http_ai_service INFO   API 响应完成，共接收 23 个数据块，总长度: 2152
10:38:33 app.services.ai.http_ai_service INFO   流式响应Token统计: 7274 (prompt=5771, completion=1503)
10:38:33 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:38:33 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:38:33 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=7274, cost=$0.022244, time=24132ms
10:38:33 app.services.agent.langgraph_tools INFO   ✅ [Agent分析] 分析完成，结果长度: 2152
10:38:33 app.api.v1.agent INFO   [Stream] 任务完成: 根据搜索到的片段，概括林仙的身份信息。 (24.2s)
10:38:33 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:38:33 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:38:33 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
10:38:34 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:38:36 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
10:38:36 app.services.ai.http_ai_service INFO   流式响应Token统计: 484 (prompt=483, completion=1)
10:38:36 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:38:36 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:38:36 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=484, cost=$0.000614, time=3090ms
10:38:36 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=484
10:38:36 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:38:36 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:38:36 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
10:38:37 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:38:38 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
10:38:38 app.services.ai.http_ai_service INFO   流式响应Token统计: 404 (prompt=403, completion=1)
10:38:38 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:38:38 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:38:38 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=404, cost=$0.000514, time=2381ms
10:38:38 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=404
10:38:38 app.services.agent.deep_agent.executor INFO   DeepAgent 执行完成: 任务=2, 反思=1, 重规划=0
10:38:38 app.services.agent.langgraph_agent INFO   [DeepAgent] 执行完成: 反思=1次, 重规划=0次
10:38:38 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共2个任务，耗时: 39.31s
10:38:38 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
10:38:38 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=1, 输出型=1, 展示型=0
10:38:38 app.services.agent.langgraph_agent INFO   [Response] 单个分析任务(analyze_text_tool)，使用AI格式化
10:38:38 app.services.agent.langgraph_agent INFO   [Summarization] 使用AI整合任务结果
10:38:38 app.services.agent.langgraph_agent INFO   [Summarization] 上下文压缩: 原始=5614字符, 压缩后=2142字符, 压缩率=62%
10:38:38 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
10:38:38 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
10:38:38 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
10:38:41 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:38:44 app.services.ai.http_ai_service INFO   API 响应完成，共接收 6 个数据块，总长度: 516
10:38:44 app.services.ai.http_ai_service INFO   流式响应Token统计: 2433 (prompt=2070, completion=363)
10:38:44 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:38:44 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:38:44 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2433, cost=$0.006217, time=5204ms
10:38:44 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=2433
10:38:45 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 隔离=work:07251ab5-98b3-4df7-b5f2-2bdb75201d18 | 重要度=0.92
10:38:45 app.services.context.store INFO   [ContextStore] 保存上下文: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:d7764e19-4eef-47cd-8b18-a05515ee87f0, token=344
10:38:45 app.services.context.manager INFO   [ContextManager] 更新上下文: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:d7764e19-4eef-47cd-8b18-a05515ee87f0, 消息数=4, Token=344
10:38:45 app.services.agent.langgraph_agent INFO   [Planning] 已保存对话到 ContextManager (session=602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:d7764e19-4eef-47cd-8b18-a05515ee87f0)
10:38:45 app.api.v1.agent INFO   [Stream] 跳过最终响应（内容已流式发送）
10:38:45 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed
10:39:19 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: 07251ab5-98b3-4df7-b5f2-2bdb75201d18, chapter_id: dc84ad42-a4ef-4beb-beb0-94d0ba54bdec
10:39:19 app.api.v1.ai INFO   [预加载] 当前章节已加载: dc84ad42-a4ef-4beb-beb0-94d0ba54bdec
10:39:19 app.api.v1.ai INFO   [预加载] 前一章节已加载: d2063c51-2364-4b9e-816c-3696cf98c28d
10:39:19 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
10:39:19 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:63107 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
10:39:20 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: 07251ab5-98b3-4df7-b5f2-2bdb75201d18, chapter_id: dc84ad42-a4ef-4beb-beb0-94d0ba54bdec
10:39:20 app.api.v1.ai INFO   [预加载] 当前章节已加载: dc84ad42-a4ef-4beb-beb0-94d0ba54bdec
10:39:20 app.api.v1.ai INFO   [预加载] 前一章节已加载: d2063c51-2364-4b9e-816c-3696cf98c28d
10:39:20 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
10:39:20 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:62254 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
10:39:20 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:62255 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
10:39:20 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:07251ab5-98b3-4df7-b5f2-2bdb75201d18
10:39:20 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/dc84ad42-a4ef-4beb-beb0-94d0ba54bdec
INFO:     127.0.0.1:56018 - "PUT /api/v1/chapters/dc84ad42-a4ef-4beb-beb0-94d0ba54bdec HTTP/1.1" 200 OK
10:39:20 app.services.chapter_vector_service INFO   Vectorizing chapter: 第8章 【系统升级，降临荒古】 (order=8)
10:39:21 app.services.chapter_vector_service INFO   Stored chapter vectors: 第8章 【系统升级，降临荒古】 (5 chunks)
10:39:22 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:07251ab5-98b3-4df7-b5f2-2bdb75201d18
10:39:22 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/dc84ad42-a4ef-4beb-beb0-94d0ba54bdec
INFO:     127.0.0.1:62508 - "PUT /api/v1/chapters/dc84ad42-a4ef-4beb-beb0-94d0ba54bdec HTTP/1.1" 200 OK
10:39:22 app.services.chapter_vector_service INFO   Vectorizing chapter: 第8章 【系统升级，降临荒古】 (order=8)
10:39:22 app.services.chapter_vector_service INFO   Stored chapter vectors: 第8章 【系统升级，降临荒古】 (5 chunks)
10:39:31 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:59121 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
10:39:31 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
10:39:31 app.services.ai.http_ai_service INFO   ModelSelector 已启用
10:39:31 app.services.ai.http_ai_service INFO   AILogService 已启用 (用于成本追踪)
10:39:34 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
10:39:34 app.api.v1.agent INFO   [Chat Stream] Mode: planning
10:39:34 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:62609 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
10:39:34 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: planning, Message: 叶凡和庞博是什么关系？...
10:39:34 app.api.v1.agent INFO   [agent_chat_stream] 📥 收到的 context 字段:
10:39:34 app.api.v1.agent INFO     - selected_text: N/A...
10:39:34 app.api.v1.agent INFO     - selection_position: N/A
10:39:34 app.api.v1.agent INFO     - chapter_context: 当前章节ID: dc84ad42-a4ef-4beb-beb0-94d0ba54bdec...
10:39:34 app.api.v1.agent INFO     - instruction_context: N/A...
10:39:34 app.services.agent.langgraph_agent INFO   [Planning] 使用隔离的thread_id: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:12153cac-f941-4dcd-9dd1-1a8ad3d94f6e (user_id=602f5147-846a-4cde-95d3-405fa75f133f, work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18, conversation_id=12153cac-f941-4dcd-9dd1-1a8ad3d94f6e)
10:39:34 app.services.context.manager INFO   [ContextManager] 创建新上下文: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:12153cac-f941-4dcd-9dd1-1a8ad3d94f6e
10:39:34 app.services.context.manager INFO   [ContextManager] Session 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:12153cac-f941-4dcd-9dd1-1a8ad3d94f6e: 0/16000 tokens
10:39:34 app.services.context.vector_memory_store INFO   🔍 检索记忆 | 查询='叶凡和庞博是什么关系？...' | 隔离键=['user:602f5147-846a-4cde-95d3-405fa75f133f:work:07251ab5-98b3-4df7-b5f2-2bdb75201d18', 'user:602f5147-846a-4cde-95d3-405fa75f133f'] | 找到=3条
10:39:34 app.services.context.manager INFO   🔍 检索长期记忆 | 级别=work | work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18 | 含用户级=True | 找到=3条
10:39:34 app.services.context.monitoring_integration INFO   [Monitor] 上下文构建: 1条消息, 0 tokens, 耗时 231.73ms
10:39:34 app.services.agent.langgraph_agent INFO   [Planning] 从 ContextManager 加载了 1 条历史消息 (token: 0)
10:39:34 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: 叶凡和庞博是什么关系？...
10:39:34 app.core.cache INFO   ✅ 缓存命中: prompt:planning_agent:v2.9.1:get_planning_agent_mode_prompt:fca6eb91156619d0
10:39:34 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:39:34 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:39:34 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=1200, temp=0.3, task_type=TaskType.SIMPLE_QA
10:39:37 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:39:40 app.services.ai.http_ai_service INFO   API 响应完成，共接收 7 个数据块，总长度: 832
10:39:40 app.services.ai.http_ai_service INFO   流式响应Token统计: 5698 (prompt=5291, completion=407)
10:39:40 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:39:40 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:39:40 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=5698, cost=$0.010684, time=5909ms
10:39:40 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=5698
10:39:40 app.services.agent.langgraph_agent INFO   [JSON解析] 方法2成功: 从```json块提取
10:39:40 app.services.agent.langgraph_agent INFO   [Planning] 思维链: 输出=用户想了解叶凡和庞博之间的关系，需要对作品内容进行分析和总结, 原料=需要查找作品中关于叶凡和庞博的互动和描述, 处理=使用 search_analysis_f
10:39:40 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共2个任务，耗时: 5.99s
10:39:40 app.api.v1.agent INFO   [Stream] Plan tasks: 2 items
10:39:40 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
10:39:40 app.services.agent.langgraph_agent INFO   [DeepAgent] 启用反思模式
10:39:40 app.services.agent.parameter_resolver INFO   [ParameterResolver] 初始化完成, 严格模式: False
10:39:40 app.services.agent.langgraph_agent INFO   [DeepAgent] ParameterResolver 已启用
10:39:40 app.services.agent.deep_agent.executor INFO   DeepAgent 开始执行，共 2 个任务，反思功能已启用
10:39:40 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] AI 推断功能已启用
10:39:40 app.api.v1.agent INFO   [Stream] Task started: 搜索叶凡和庞博的关系相关内容
10:39:40 app.services.chapter_vector_service INFO   RAG retrieve work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18, current_order=8, query=叶凡和庞博的关系...
10:39:40 app.services.chapter_vector_service INFO   RAG retrieved 10 segments within order<=10
10:39:40 app.services.agent.langgraph_tools INFO   [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
10:39:40 app.api.v1.agent INFO   [Stream] 任务完成: 搜索叶凡和庞博的关系相关内容 (0.3s)
10:39:40 app.services.agent.deep_agent.reflection INFO   [Checkpoint] 任务 1 标记了 checkpoint，触发反思
10:39:40 app.services.agent.deep_agent.executor INFO   任务 1 触发反思检查点
10:39:40 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:39:40 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:39:40 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
10:39:42 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:39:43 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
10:39:43 app.services.ai.http_ai_service INFO   流式响应Token统计: 507 (prompt=506, completion=1)
10:39:43 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:39:43 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:39:43 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=507, cost=$0.000643, time=2751ms
10:39:43 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=507
10:39:43 app.services.agent.deep_agent.reflection INFO   [DeepAgent反思] 开始调用 AI，task_id=1
10:39:43 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:39:43 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:39:43 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=500, temp=0.3, task_type=TaskType.SIMPLE_QA
10:39:45 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:39:58 app.services.ai.http_ai_service INFO   API 响应完成，共接收 2 个数据块，总长度: 151
10:39:58 app.services.ai.http_ai_service INFO   流式响应Token统计: 3384 (prompt=3302, completion=82)
10:39:58 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:39:58 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:39:58 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=3384, cost=$0.004948, time=14713ms
10:39:58 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=3384
10:39:58 app.services.agent.deep_agent.reflection INFO   [Reflection] JSON提取成功: needs_replan=True
10:39:58 app.services.agent.deep_agent.executor INFO   [Reflection] 前置任务不触发重规划（已有后续输出任务）
10:39:58 app.api.v1.agent INFO   [Stream] Task started: 分析搜索结果，概括叶凡和庞博的关系
10:39:58 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
10:39:58 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
10:39:58 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
10:40:00 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:40:24 app.services.ai.http_ai_service INFO   API 响应完成，共接收 28 个数据块，总长度: 2421
10:40:24 app.services.ai.http_ai_service INFO   流式响应Token统计: 8442 (prompt=6620, completion=1822)
10:40:24 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:40:24 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:40:24 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=8442, cost=$0.026495, time=26535ms
10:40:24 app.services.agent.langgraph_tools INFO   ✅ [Agent分析] 分析完成，结果长度: 2421
10:40:24 app.api.v1.agent INFO   [Stream] 任务完成: 分析搜索结果，概括叶凡和庞博的关系 (26.6s)
10:40:25 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:40:25 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:40:25 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
10:40:26 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:40:27 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
10:40:27 app.services.ai.http_ai_service INFO   流式响应Token统计: 508 (prompt=507, completion=1)
10:40:27 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:40:27 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:40:27 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=508, cost=$0.000644, time=2625ms
10:40:27 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=508
10:40:27 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:40:27 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:40:27 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
10:40:29 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:40:31 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
10:40:31 app.services.ai.http_ai_service INFO   流式响应Token统计: 569 (prompt=568, completion=1)
10:40:31 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:40:31 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:40:31 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=569, cost=$0.000720, time=3752ms
10:40:31 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=569
10:40:31 app.services.agent.deep_agent.executor INFO   DeepAgent 执行完成: 任务=2, 反思=1, 重规划=0
10:40:31 app.services.agent.langgraph_agent INFO   [DeepAgent] 执行完成: 反思=1次, 重规划=0次
10:40:31 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共2个任务，耗时: 50.88s
10:40:31 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
10:40:31 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=1, 输出型=1, 展示型=0
10:40:31 app.services.agent.langgraph_agent INFO   [Response] 单个分析任务(analyze_text_tool)，使用AI格式化
10:40:31 app.services.agent.langgraph_agent INFO   [Summarization] 使用AI整合任务结果
10:40:31 app.services.agent.langgraph_agent INFO   [Summarization] 上下文压缩: 原始=5984字符, 压缩后=2137字符, 压缩率=65%
10:40:31 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
10:40:31 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
10:40:31 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
10:40:33 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:40:36 app.services.ai.http_ai_service INFO   API 响应完成，共接收 5 个数据块，总长度: 434
10:40:36 app.services.ai.http_ai_service INFO   流式响应Token统计: 2271 (prompt=1957, completion=314)
10:40:36 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:40:36 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:40:36 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2271, cost=$0.005586, time=4670ms
10:40:36 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=2271
10:40:37 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 隔离=work:07251ab5-98b3-4df7-b5f2-2bdb75201d18 | 重要度=0.51
10:40:37 app.services.context.store INFO   [ContextStore] 保存上下文: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:12153cac-f941-4dcd-9dd1-1a8ad3d94f6e, token=258
10:40:37 app.services.context.manager INFO   [ContextManager] 更新上下文: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:12153cac-f941-4dcd-9dd1-1a8ad3d94f6e, 消息数=2, Token=258
10:40:37 app.services.agent.langgraph_agent INFO   [Planning] 已保存对话到 ContextManager (session=602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:12153cac-f941-4dcd-9dd1-1a8ad3d94f6e)
10:40:37 app.api.v1.agent INFO   [Stream] 跳过最终响应（内容已流式发送）
10:40:37 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed
10:41:51 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
10:41:51 app.services.ai.http_ai_service INFO   ModelSelector 已启用
10:41:51 app.services.ai.http_ai_service INFO   AILogService 已启用 (用于成本追踪)
10:41:52 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
10:41:52 app.api.v1.agent INFO   [Chat Stream] Mode: planning
10:41:52 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:63691 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
10:41:52 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: planning, Message: 系统10086有什么能力？...
10:41:52 app.api.v1.agent INFO   [agent_chat_stream] 📥 收到的 context 字段:
10:41:52 app.api.v1.agent INFO     - selected_text: N/A...
10:41:52 app.api.v1.agent INFO     - selection_position: N/A
10:41:52 app.api.v1.agent INFO     - chapter_context: 当前章节ID: dc84ad42-a4ef-4beb-beb0-94d0ba54bdec...
10:41:52 app.api.v1.agent INFO     - instruction_context: N/A...
10:41:52 app.services.agent.langgraph_agent INFO   [Planning] 使用隔离的thread_id: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:12153cac-f941-4dcd-9dd1-1a8ad3d94f6e (user_id=602f5147-846a-4cde-95d3-405fa75f133f, work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18, conversation_id=12153cac-f941-4dcd-9dd1-1a8ad3d94f6e)
10:41:52 app.services.context.store INFO   [ContextStore] 加载上下文: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:12153cac-f941-4dcd-9dd1-1a8ad3d94f6e, 2条消息
10:41:52 app.services.context.manager INFO   [ContextManager] Session 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:12153cac-f941-4dcd-9dd1-1a8ad3d94f6e: 258/16000 tokens
10:41:53 app.services.context.vector_memory_store INFO   🔍 检索记忆 | 查询='系统10086有什么能力？...' | 隔离键=['user:602f5147-846a-4cde-95d3-405fa75f133f:work:07251ab5-98b3-4df7-b5f2-2bdb75201d18', 'user:602f5147-846a-4cde-95d3-405fa75f133f'] | 找到=1条
10:41:53 app.services.context.manager INFO   🔍 检索长期记忆 | 级别=work | work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18 | 含用户级=True | 找到=1条
10:41:53 app.services.context.monitoring_integration INFO   [Monitor] 上下文构建: 3条消息, 258 tokens, 耗时 214.35ms
10:41:53 app.services.agent.langgraph_agent INFO   [Planning] 从 ContextManager 加载了 3 条历史消息 (token: 258)
10:41:53 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: 系统10086有什么能力？...
10:41:53 app.core.cache INFO   ✅ 缓存命中: prompt:planning_agent:v2.9.1:get_planning_agent_mode_prompt:fca6eb91156619d0
10:41:53 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:41:53 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:41:53 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=1200, temp=0.3, task_type=TaskType.SIMPLE_QA
10:41:55 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:41:58 app.services.ai.http_ai_service INFO   API 响应完成，共接收 7 个数据块，总长度: 847
10:41:58 app.services.ai.http_ai_service INFO   流式响应Token统计: 6178 (prompt=5770, completion=408)
10:41:58 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:41:58 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:41:58 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=6178, cost=$0.011293, time=5633ms
10:41:58 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=6178
10:41:58 app.services.agent.langgraph_agent INFO   [JSON解析] 方法2成功: 从```json块提取
10:41:58 app.services.agent.langgraph_agent INFO   [Planning] 思维链: 输出=用户期望看到关于“系统10086”能力的分析报告或概括性总结, 原料=需要找到作品中所有关于“系统10086”, 处理=首先使用 search_analysis
10:41:58 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共2个任务，耗时: 5.71s
10:41:58 app.api.v1.agent INFO   [Stream] Plan tasks: 2 items
10:41:58 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
10:41:58 app.services.agent.langgraph_agent INFO   [DeepAgent] 启用反思模式
10:41:58 app.services.agent.parameter_resolver INFO   [ParameterResolver] 初始化完成, 严格模式: False
10:41:58 app.services.agent.langgraph_agent INFO   [DeepAgent] ParameterResolver 已启用
10:41:58 app.services.agent.deep_agent.executor INFO   DeepAgent 开始执行，共 2 个任务，反思功能已启用
10:41:58 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] AI 推断功能已启用
10:41:58 app.api.v1.agent INFO   [Stream] Task started: 搜索关于“系统10086”的文本片段
10:41:58 app.services.chapter_vector_service INFO   RAG retrieve work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18, current_order=8, query=系统10086...
10:41:59 app.services.chapter_vector_service INFO   RAG retrieved 8 segments within order<=10
10:41:59 app.services.agent.langgraph_tools INFO   [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
10:41:59 app.api.v1.agent INFO   [Stream] 任务完成: 搜索关于“系统10086”的文本片段 (0.3s)
10:41:59 app.services.agent.deep_agent.reflection INFO   [Checkpoint] 任务 1 标记了 checkpoint，触发反思
10:41:59 app.services.agent.deep_agent.executor INFO   任务 1 触发反思检查点
10:41:59 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:41:59 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:41:59 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
10:42:00 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:42:02 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
10:42:02 app.services.ai.http_ai_service INFO   流式响应Token统计: 469 (prompt=468, completion=1)
10:42:02 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:42:02 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:42:02 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=469, cost=$0.000595, time=3279ms
10:42:02 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=469
10:42:02 app.services.agent.deep_agent.reflection INFO   [DeepAgent反思] 开始调用 AI，task_id=1
10:42:02 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:42:02 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:42:02 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=500, temp=0.3, task_type=TaskType.SIMPLE_QA
10:42:04 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:42:07 app.services.ai.http_ai_service INFO   API 响应完成，共接收 2 个数据块，总长度: 133
10:42:07 app.services.ai.http_ai_service INFO   流式响应Token统计: 1260 (prompt=1190, completion=70)
10:42:07 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:42:07 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:42:07 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1260, cost=$0.002188, time=5357ms
10:42:07 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=1260
10:42:07 app.services.agent.deep_agent.reflection INFO   [Reflection] JSON提取成功: needs_replan=True
10:42:07 app.services.agent.deep_agent.executor INFO   [Reflection] 前置任务不触发重规划（已有后续输出任务）
10:42:07 app.api.v1.agent INFO   [Stream] Task started: 分析搜索到的文本，总结“系统10086”的能力
10:42:07 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
10:42:07 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
10:42:07 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
10:42:09 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:42:25 app.services.ai.http_ai_service INFO   API 响应完成，共接收 19 个数据块，总长度: 1853
10:42:25 app.services.ai.http_ai_service INFO   流式响应Token统计: 3878 (prompt=2632, completion=1246)
10:42:25 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:42:25 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:42:25 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=3878, cost=$0.015750, time=17083ms
10:42:25 app.services.agent.langgraph_tools INFO   ✅ [Agent分析] 分析完成，结果长度: 1853
10:42:25 app.api.v1.agent INFO   [Stream] 任务完成: 分析搜索到的文本，总结“系统10086”的能力 (17.1s)
10:42:25 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:42:25 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:42:25 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
10:42:26 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:42:27 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
10:42:27 app.services.ai.http_ai_service INFO   流式响应Token统计: 500 (prompt=499, completion=1)
10:42:27 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:42:27 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:42:27 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=500, cost=$0.000634, time=2239ms
10:42:27 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=500
10:42:27 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:42:27 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:42:27 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
10:42:29 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:42:30 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
10:42:30 app.services.ai.http_ai_service INFO   流式响应Token统计: 470 (prompt=469, completion=1)
10:42:30 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:42:30 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:42:30 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=470, cost=$0.000596, time=3334ms
10:42:30 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=470
10:42:30 app.services.agent.deep_agent.executor INFO   DeepAgent 执行完成: 任务=2, 反思=1, 重规划=0
10:42:30 app.services.agent.langgraph_agent INFO   [DeepAgent] 执行完成: 反思=1次, 重规划=0次
10:42:30 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共2个任务，耗时: 31.78s
10:42:30 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
10:42:30 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=1, 输出型=1, 展示型=0
10:42:30 app.services.agent.langgraph_agent INFO   [Response] 单个分析任务(analyze_text_tool)，使用AI格式化
10:42:30 app.services.agent.langgraph_agent INFO   [Summarization] 使用AI整合任务结果
10:42:30 app.services.agent.langgraph_agent INFO   [Summarization] 上下文压缩: 原始=3419字符, 压缩后=3465字符, 压缩率=-1%
10:42:30 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
10:42:30 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
10:42:30 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
10:42:33 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:42:41 app.services.ai.http_ai_service INFO   API 响应完成，共接收 8 个数据块，总长度: 775
10:42:41 app.services.ai.http_ai_service INFO   流式响应Token统计: 4243 (prompt=3720, completion=523)
10:42:41 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:42:41 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:42:41 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4243, cost=$0.009880, time=11020ms
10:42:41 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=4243
10:42:42 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 隔离=work:07251ab5-98b3-4df7-b5f2-2bdb75201d18 | 重要度=0.60
10:42:42 app.services.context.store INFO   [ContextStore] 保存上下文: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:12153cac-f941-4dcd-9dd1-1a8ad3d94f6e, token=688
10:42:42 app.services.context.manager INFO   [ContextManager] 更新上下文: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:12153cac-f941-4dcd-9dd1-1a8ad3d94f6e, 消息数=4, Token=688
10:42:42 app.services.agent.langgraph_agent INFO   [Planning] 已保存对话到 ContextManager (session=602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:12153cac-f941-4dcd-9dd1-1a8ad3d94f6e)
10:42:42 app.api.v1.agent INFO   [Stream] 跳过最终响应（内容已流式发送）
10:42:42 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed
10:44:03 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
10:44:03 app.services.ai.http_ai_service INFO   ModelSelector 已启用
10:44:03 app.services.ai.http_ai_service INFO   AILogService 已启用 (用于成本追踪)
10:44:06 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
10:44:06 app.api.v1.agent INFO   [Chat Stream] Mode: planning
10:44:06 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:53020 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
10:44:06 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: planning, Message: 段德是谁？...
10:44:06 app.api.v1.agent INFO   [agent_chat_stream] 📥 收到的 context 字段:
10:44:06 app.api.v1.agent INFO     - selected_text: N/A...
10:44:06 app.api.v1.agent INFO     - selection_position: N/A
10:44:06 app.api.v1.agent INFO     - chapter_context: 当前章节ID: dc84ad42-a4ef-4beb-beb0-94d0ba54bdec...
10:44:06 app.api.v1.agent INFO     - instruction_context: N/A...
10:44:06 app.services.agent.langgraph_agent INFO   [Planning] 使用隔离的thread_id: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:12153cac-f941-4dcd-9dd1-1a8ad3d94f6e (user_id=602f5147-846a-4cde-95d3-405fa75f133f, work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18, conversation_id=12153cac-f941-4dcd-9dd1-1a8ad3d94f6e)
10:44:06 app.services.context.store INFO   [ContextStore] 加载上下文: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:12153cac-f941-4dcd-9dd1-1a8ad3d94f6e, 4条消息
10:44:06 app.services.context.manager INFO   [ContextManager] Session 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:12153cac-f941-4dcd-9dd1-1a8ad3d94f6e: 688/16000 tokens
10:44:06 app.services.context.vector_memory_store INFO   🔍 检索记忆 | 查询='段德是谁？...' | 隔离键=['user:602f5147-846a-4cde-95d3-405fa75f133f:work:07251ab5-98b3-4df7-b5f2-2bdb75201d18', 'user:602f5147-846a-4cde-95d3-405fa75f133f'] | 找到=3条
10:44:06 app.services.context.manager INFO   🔍 检索长期记忆 | 级别=work | work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18 | 含用户级=True | 找到=3条
10:44:06 app.services.context.monitoring_integration INFO   [Monitor] 上下文构建: 5条消息, 688 tokens, 耗时 229.10ms
10:44:06 app.services.agent.langgraph_agent INFO   [Planning] 从 ContextManager 加载了 5 条历史消息 (token: 688)
10:44:06 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: 段德是谁？...
10:44:06 app.core.cache INFO   ✅ 缓存命中: prompt:planning_agent:v2.9.1:get_planning_agent_mode_prompt:fca6eb91156619d0
10:44:06 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:44:06 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:44:06 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=1200, temp=0.3, task_type=TaskType.SIMPLE_QA
10:44:09 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:44:13 app.services.ai.http_ai_service INFO   API 响应完成，共接收 6 个数据块，总长度: 776
10:44:13 app.services.ai.http_ai_service INFO   流式响应Token统计: 6445 (prompt=6089, completion=356)
10:44:13 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:44:13 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:44:13 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=6445, cost=$0.011171, time=6428ms
10:44:13 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=6445
10:44:13 app.services.agent.langgraph_agent INFO   [JSON解析] 方法2成功: 从```json块提取
10:44:13 app.services.agent.langgraph_agent INFO   [Planning] 思维链: 输出=用户想了解“段德”这个人物的信息，期望得到一个关于他身份、特, 原料=需要查找作品中所有关于“段德”的信息片段, 处理=使用 search_analysis_f
10:44:13 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共2个任务，耗时: 6.51s
10:44:13 app.api.v1.agent INFO   [Stream] Plan tasks: 2 items
10:44:13 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
10:44:13 app.services.agent.langgraph_agent INFO   [DeepAgent] 启用反思模式
10:44:13 app.services.agent.parameter_resolver INFO   [ParameterResolver] 初始化完成, 严格模式: False
10:44:13 app.services.agent.langgraph_agent INFO   [DeepAgent] ParameterResolver 已启用
10:44:13 app.services.agent.deep_agent.executor INFO   DeepAgent 开始执行，共 2 个任务，反思功能已启用
10:44:13 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] AI 推断功能已启用
10:44:13 app.api.v1.agent INFO   [Stream] Task started: 搜索关于“段德”的相关内容片段
10:44:13 app.services.chapter_vector_service INFO   RAG retrieve work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18, current_order=8, query=段德...
10:44:13 app.services.chapter_vector_service INFO   RAG retrieved 10 segments within order<=10
10:44:13 app.services.agent.langgraph_tools INFO   [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
10:44:13 app.api.v1.agent INFO   [Stream] 任务完成: 搜索关于“段德”的相关内容片段 (0.2s)
10:44:13 app.services.agent.deep_agent.reflection INFO   [Checkpoint] 任务 1 标记了 checkpoint，触发反思
10:44:13 app.services.agent.deep_agent.executor INFO   任务 1 触发反思检查点
10:44:13 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:44:13 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:44:13 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
10:44:14 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:44:15 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
10:44:15 app.services.ai.http_ai_service INFO   流式响应Token统计: 362 (prompt=361, completion=1)
10:44:15 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:44:15 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:44:15 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=362, cost=$0.000461, time=2176ms
10:44:15 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=362
10:44:15 app.services.agent.deep_agent.reflection INFO   [DeepAgent反思] 开始调用 AI，task_id=1
10:44:15 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:44:15 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:44:15 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=500, temp=0.3, task_type=TaskType.SIMPLE_QA
10:44:16 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:44:19 app.services.ai.http_ai_service INFO   API 响应完成，共接收 2 个数据块，总长度: 164
10:44:19 app.services.ai.http_ai_service INFO   流式响应Token统计: 1307 (prompt=1214, completion=93)
10:44:19 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:44:19 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:44:19 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1307, cost=$0.002448, time=3923ms
10:44:19 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=1307
10:44:19 app.services.agent.deep_agent.reflection INFO   [Reflection] JSON提取成功: needs_replan=True
10:44:19 app.services.agent.deep_agent.executor INFO   [Reflection] 前置任务不触发重规划（已有后续输出任务）
10:44:19 app.api.v1.agent INFO   [Stream] Task started: 分析搜索到的内容，介绍段德是谁
10:44:19 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
10:44:19 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
10:44:19 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
10:44:21 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:44:48 app.services.ai.http_ai_service INFO   API 响应完成，共接收 36 个数据块，总长度: 3340
10:44:48 app.services.ai.http_ai_service INFO   流式响应Token统计: 8357 (prompt=6027, completion=2330)
10:44:48 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:44:48 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:44:48 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=8357, cost=$0.030834, time=29134ms
10:44:48 app.services.agent.langgraph_tools INFO   ✅ [Agent分析] 分析完成，结果长度: 3340
10:44:48 app.api.v1.agent INFO   [Stream] 任务完成: 分析搜索到的内容，介绍段德是谁 (29.2s)
10:44:48 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:44:48 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:44:48 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
10:44:51 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:44:52 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
10:44:52 app.services.ai.http_ai_service INFO   流式响应Token统计: 447 (prompt=446, completion=1)
10:44:52 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:44:52 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:44:52 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=447, cost=$0.000568, time=3702ms
10:44:52 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=447
10:44:52 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:44:52 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:44:52 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
10:44:54 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:44:55 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
10:44:55 app.services.ai.http_ai_service INFO   流式响应Token统计: 427 (prompt=426, completion=1)
10:44:55 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:44:55 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:44:55 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=427, cost=$0.000543, time=2476ms
10:44:55 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=427
10:44:55 app.services.agent.deep_agent.executor INFO   DeepAgent 执行完成: 任务=2, 反思=1, 重规划=0
10:44:55 app.services.agent.langgraph_agent INFO   [DeepAgent] 执行完成: 反思=1次, 重规划=0次
10:44:55 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共2个任务，耗时: 41.85s
10:44:55 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
10:44:55 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=1, 输出型=1, 展示型=0
10:44:55 app.services.agent.langgraph_agent INFO   [Response] 单个分析任务(analyze_text_tool)，使用AI格式化
10:44:55 app.services.agent.langgraph_agent INFO   [Summarization] 使用AI整合任务结果
10:44:55 app.services.agent.langgraph_agent INFO   [Summarization] 上下文压缩: 原始=6689字符, 压缩后=2134字符, 压缩率=69%
10:44:55 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
10:44:55 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
10:44:55 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
10:44:57 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:44:58 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 72
10:44:58 app.services.ai.http_ai_service INFO   流式响应Token统计: 1920 (prompt=1877, completion=43)
10:44:58 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:44:58 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:44:58 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1920, cost=$0.002776, time=3101ms
10:44:58 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=1920
10:44:59 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 隔离=work:07251ab5-98b3-4df7-b5f2-2bdb75201d18 | 重要度=0.51
10:44:59 app.services.context.store INFO   [ContextStore] 保存上下文: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:12153cac-f941-4dcd-9dd1-1a8ad3d94f6e, token=733
10:44:59 app.services.context.manager INFO   [ContextManager] 更新上下文: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:12153cac-f941-4dcd-9dd1-1a8ad3d94f6e, 消息数=6, Token=733
10:44:59 app.services.agent.langgraph_agent INFO   [Planning] 已保存对话到 ContextManager (session=602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:12153cac-f941-4dcd-9dd1-1a8ad3d94f6e)
10:44:59 app.api.v1.agent INFO   [Stream] 跳过最终响应（内容已流式发送）
10:44:59 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed
10:45:26 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: 07251ab5-98b3-4df7-b5f2-2bdb75201d18, chapter_id: a628af2c-98b5-44ba-b128-c8ca915861ce
10:45:26 app.api.v1.ai INFO   [预加载] 当前章节已加载: a628af2c-98b5-44ba-b128-c8ca915861ce
10:45:26 app.api.v1.ai INFO   [预加载] 前一章节已加载: bd8cdfc1-f77e-4a02-93fb-e56e214193d8
10:45:26 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
10:45:26 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:49325 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
10:45:26 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: 07251ab5-98b3-4df7-b5f2-2bdb75201d18, chapter_id: a628af2c-98b5-44ba-b128-c8ca915861ce
10:45:26 app.api.v1.ai INFO   [预加载] 当前章节已加载: a628af2c-98b5-44ba-b128-c8ca915861ce
10:45:26 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/sessions
10:45:26 app.api.v1.ai INFO   [预加载] 前一章节已加载: bd8cdfc1-f77e-4a02-93fb-e56e214193d8
10:45:26 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
INFO:     127.0.0.1:55851 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
10:45:26 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:55850 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
10:45:27 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:07251ab5-98b3-4df7-b5f2-2bdb75201d18
10:45:27 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/a628af2c-98b5-44ba-b128-c8ca915861ce
INFO:     127.0.0.1:54723 - "PUT /api/v1/chapters/a628af2c-98b5-44ba-b128-c8ca915861ce HTTP/1.1" 200 OK
10:45:27 app.services.chapter_vector_service INFO   Vectorizing chapter: 第62章 【啃老大法，启动！】 (order=51)
10:45:28 app.services.chapter_vector_service INFO   Stored chapter vectors: 第62章 【啃老大法，启动！】 (5 chunks)
10:45:28 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:07251ab5-98b3-4df7-b5f2-2bdb75201d18
10:45:28 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/a628af2c-98b5-44ba-b128-c8ca915861ce
INFO:     127.0.0.1:54926 - "PUT /api/v1/chapters/a628af2c-98b5-44ba-b128-c8ca915861ce HTTP/1.1" 200 OK
10:45:28 app.services.chapter_vector_service INFO   Vectorizing chapter: 第62章 【啃老大法，启动！】 (order=51)
10:45:29 app.services.chapter_vector_service INFO   Stored chapter vectors: 第62章 【啃老大法，启动！】 (5 chunks)
10:45:33 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:53943 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
10:45:34 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
10:45:34 app.services.ai.http_ai_service INFO   ModelSelector 已启用
10:45:34 app.services.ai.http_ai_service INFO   AILogService 已启用 (用于成本追踪)
10:45:37 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
10:45:37 app.api.v1.agent INFO   [Chat Stream] Mode: planning
10:45:37 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:61589 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
10:45:37 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: planning, Message: 段德是谁？...
10:45:37 app.api.v1.agent INFO   [agent_chat_stream] 📥 收到的 context 字段:
10:45:37 app.api.v1.agent INFO     - selected_text: N/A...
10:45:37 app.api.v1.agent INFO     - selection_position: N/A
10:45:37 app.api.v1.agent INFO     - chapter_context: 当前章节ID: a628af2c-98b5-44ba-b128-c8ca915861ce...
10:45:37 app.api.v1.agent INFO     - instruction_context: N/A...
10:45:37 app.services.agent.langgraph_agent INFO   [Planning] 使用隔离的thread_id: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:d1e4530e-2bf8-4502-a37f-deb843845a39 (user_id=602f5147-846a-4cde-95d3-405fa75f133f, work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18, conversation_id=d1e4530e-2bf8-4502-a37f-deb843845a39)
10:45:37 app.services.context.manager INFO   [ContextManager] 创建新上下文: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:d1e4530e-2bf8-4502-a37f-deb843845a39
10:45:37 app.services.context.manager INFO   [ContextManager] Session 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:d1e4530e-2bf8-4502-a37f-deb843845a39: 0/16000 tokens
10:45:37 app.services.context.vector_memory_store INFO   🔍 检索记忆 | 查询='段德是谁？...' | 隔离键=['user:602f5147-846a-4cde-95d3-405fa75f133f:work:07251ab5-98b3-4df7-b5f2-2bdb75201d18', 'user:602f5147-846a-4cde-95d3-405fa75f133f'] | 找到=3条
10:45:37 app.services.context.manager INFO   🔍 检索长期记忆 | 级别=work | work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18 | 含用户级=True | 找到=3条
10:45:37 app.services.context.monitoring_integration INFO   [Monitor] 上下文构建: 1条消息, 0 tokens, 耗时 180.10ms
10:45:37 app.services.agent.langgraph_agent INFO   [Planning] 从 ContextManager 加载了 1 条历史消息 (token: 0)
10:45:37 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: 段德是谁？...
10:45:37 app.core.cache INFO   ✅ 缓存命中: prompt:planning_agent:v2.9.1:get_planning_agent_mode_prompt:fca6eb91156619d0
10:45:37 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:45:37 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:45:37 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=1200, temp=0.3, task_type=TaskType.SIMPLE_QA
10:45:39 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:45:43 app.services.ai.http_ai_service INFO   API 响应完成，共接收 6 个数据块，总长度: 734
10:45:43 app.services.ai.http_ai_service INFO   流式响应Token统计: 5780 (prompt=5436, completion=344)
10:45:43 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:45:43 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:45:43 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=5780, cost=$0.010235, time=6158ms
10:45:43 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=5780
10:45:43 app.services.agent.langgraph_agent INFO   [JSON解析] 方法2成功: 从```json块提取
10:45:43 app.services.agent.langgraph_agent INFO   [Planning] 思维链: 输出=用户想了解“段德”这个人物的信息，期望得到一个关于这个人物的, 原料=需要搜索作品中所有关于“段德”的信息片段, 处理=使用搜索工具查找相关内容，然后使用分析工
10:45:43 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共2个任务，耗时: 6.22s
10:45:43 app.api.v1.agent INFO   [Stream] Plan tasks: 2 items
10:45:43 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
10:45:43 app.services.agent.langgraph_agent INFO   [DeepAgent] 启用反思模式
10:45:43 app.services.agent.parameter_resolver INFO   [ParameterResolver] 初始化完成, 严格模式: False
10:45:43 app.services.agent.langgraph_agent INFO   [DeepAgent] ParameterResolver 已启用
10:45:43 app.services.agent.deep_agent.executor INFO   DeepAgent 开始执行，共 2 个任务，反思功能已启用
10:45:43 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] AI 推断功能已启用
10:45:43 app.api.v1.agent INFO   [Stream] Task started: 搜索关于“段德”的信息片段
10:45:43 app.services.chapter_vector_service INFO   RAG retrieve work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18, current_order=51, query=段德...
10:45:44 app.services.chapter_vector_service INFO   RAG retrieved 10 segments within order<=53
10:45:44 app.services.agent.langgraph_tools INFO   [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
10:45:44 app.api.v1.agent INFO   [Stream] 任务完成: 搜索关于“段德”的信息片段 (0.6s)
10:45:44 app.services.agent.deep_agent.reflection INFO   [Checkpoint] 任务 1 标记了 checkpoint，触发反思
10:45:44 app.services.agent.deep_agent.executor INFO   任务 1 触发反思检查点
10:45:44 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:45:44 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:45:44 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
10:45:46 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:45:47 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
10:45:47 app.services.ai.http_ai_service INFO   流式响应Token统计: 461 (prompt=460, completion=1)
10:45:47 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:45:47 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:45:47 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=461, cost=$0.000585, time=3357ms
10:45:47 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=461
10:45:47 app.services.agent.deep_agent.reflection INFO   [DeepAgent反思] 开始调用 AI，task_id=1
10:45:47 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:45:47 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:45:47 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=500, temp=0.3, task_type=TaskType.SIMPLE_QA
10:45:49 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:45:51 app.services.ai.http_ai_service INFO   API 响应完成，共接收 2 个数据块，总长度: 149
10:45:51 app.services.ai.http_ai_service INFO   流式响应Token统计: 1282 (prompt=1201, completion=81)
10:45:51 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:45:51 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:45:51 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1282, cost=$0.002311, time=4300ms
10:45:51 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=1282
10:45:51 app.services.agent.deep_agent.reflection INFO   [Reflection] JSON提取成功: needs_replan=True
10:45:51 app.services.agent.deep_agent.executor INFO   [Reflection] 前置任务不触发重规划（已有后续输出任务）
10:45:51 app.api.v1.agent INFO   [Stream] Task started: 根据搜索结果概括“段德”的人物信息
10:45:51 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
10:45:51 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
10:45:51 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
10:45:53 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:46:17 app.services.ai.http_ai_service INFO   API 响应完成，共接收 27 个数据块，总长度: 2437
10:46:17 app.services.ai.http_ai_service INFO   流式响应Token统计: 6554 (prompt=4819, completion=1735)
10:46:17 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:46:17 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:46:17 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=6554, cost=$0.023374, time=25823ms
10:46:17 app.services.agent.langgraph_tools INFO   ✅ [Agent分析] 分析完成，结果长度: 2437
10:46:17 app.api.v1.agent INFO   [Stream] 任务完成: 根据搜索结果概括“段德”的人物信息 (25.9s)
10:46:17 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:46:17 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:46:17 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
10:46:19 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:46:20 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
10:46:20 app.services.ai.http_ai_service INFO   流式响应Token统计: 461 (prompt=460, completion=1)
10:46:20 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:46:20 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:46:20 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=461, cost=$0.000585, time=2786ms
10:46:20 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=461
10:46:20 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:46:20 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:46:20 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
10:46:22 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:46:22 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
10:46:22 app.services.ai.http_ai_service INFO   流式响应Token统计: 308 (prompt=307, completion=1)
10:46:22 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:46:22 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:46:22 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=308, cost=$0.000394, time=1979ms
10:46:22 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=308
10:46:22 app.services.agent.deep_agent.executor INFO   DeepAgent 执行完成: 任务=2, 反思=1, 重规划=0
10:46:22 app.services.agent.langgraph_agent INFO   [DeepAgent] 执行完成: 反思=1次, 重规划=0次
10:46:22 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共2个任务，耗时: 39.05s
10:46:22 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
10:46:22 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=1, 输出型=1, 展示型=0
10:46:22 app.services.agent.langgraph_agent INFO   [Response] 单个分析任务(analyze_text_tool)，使用AI格式化
10:46:22 app.services.agent.langgraph_agent INFO   [Summarization] 使用AI整合任务结果
10:46:22 app.services.agent.langgraph_agent INFO   [Summarization] 上下文压缩: 原始=4707字符, 压缩后=2141字符, 压缩率=55%
10:46:22 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
10:46:22 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
10:46:22 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
10:46:24 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:46:26 app.services.ai.http_ai_service INFO   API 响应完成，共接收 7 个数据块，总长度: 599
10:46:26 app.services.ai.http_ai_service INFO   流式响应Token统计: 2344 (prompt=1915, completion=429)
10:46:26 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:46:26 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:46:26 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2344, cost=$0.006684, time=3945ms
10:46:26 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=2344
10:46:27 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 隔离=work:07251ab5-98b3-4df7-b5f2-2bdb75201d18 | 重要度=0.92
10:46:27 app.services.context.store INFO   [ContextStore] 保存上下文: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:d1e4530e-2bf8-4502-a37f-deb843845a39, token=332
10:46:27 app.services.context.manager INFO   [ContextManager] 更新上下文: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:d1e4530e-2bf8-4502-a37f-deb843845a39, 消息数=2, Token=332
10:46:27 app.services.agent.langgraph_agent INFO   [Planning] 已保存对话到 ContextManager (session=602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:d1e4530e-2bf8-4502-a37f-deb843845a39)
10:46:27 app.api.v1.agent INFO   [Stream] 跳过最终响应（内容已流式发送）
10:46:27 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed
10:47:23 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
10:47:23 app.services.ai.http_ai_service INFO   ModelSelector 已启用
10:47:23 app.services.ai.http_ai_service INFO   AILogService 已启用 (用于成本追踪)
10:47:26 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
10:47:26 app.api.v1.agent INFO   [Chat Stream] Mode: planning
10:47:26 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:65522 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
10:47:26 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: planning, Message: 老天师有什么能力？...
10:47:26 app.api.v1.agent INFO   [agent_chat_stream] 📥 收到的 context 字段:
10:47:26 app.api.v1.agent INFO     - selected_text: N/A...
10:47:26 app.api.v1.agent INFO     - selection_position: N/A
10:47:26 app.api.v1.agent INFO     - chapter_context: 当前章节ID: a628af2c-98b5-44ba-b128-c8ca915861ce...
10:47:26 app.api.v1.agent INFO     - instruction_context: N/A...
10:47:26 app.services.agent.langgraph_agent INFO   [Planning] 使用隔离的thread_id: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:d1e4530e-2bf8-4502-a37f-deb843845a39 (user_id=602f5147-846a-4cde-95d3-405fa75f133f, work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18, conversation_id=d1e4530e-2bf8-4502-a37f-deb843845a39)
10:47:26 app.services.context.store INFO   [ContextStore] 加载上下文: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:d1e4530e-2bf8-4502-a37f-deb843845a39, 2条消息
10:47:26 app.services.context.manager INFO   [ContextManager] Session 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:d1e4530e-2bf8-4502-a37f-deb843845a39: 332/16000 tokens
10:47:26 app.services.context.vector_memory_store INFO   🔍 检索记忆 | 查询='老天师有什么能力？...' | 隔离键=['user:602f5147-846a-4cde-95d3-405fa75f133f:work:07251ab5-98b3-4df7-b5f2-2bdb75201d18', 'user:602f5147-846a-4cde-95d3-405fa75f133f'] | 找到=3条
10:47:26 app.services.context.manager INFO   🔍 检索长期记忆 | 级别=work | work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18 | 含用户级=True | 找到=3条
10:47:26 app.services.context.monitoring_integration INFO   [Monitor] 上下文构建: 3条消息, 332 tokens, 耗时 304.86ms
10:47:26 app.services.agent.langgraph_agent INFO   [Planning] 从 ContextManager 加载了 3 条历史消息 (token: 332)
10:47:26 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: 老天师有什么能力？...
10:47:26 app.core.cache INFO   ✅ 缓存命中: prompt:planning_agent:v2.9.1:get_planning_agent_mode_prompt:fca6eb91156619d0
10:47:26 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:47:26 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:47:26 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=1200, temp=0.3, task_type=TaskType.SIMPLE_QA
10:47:29 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:47:32 app.services.ai.http_ai_service INFO   API 响应完成，共接收 5 个数据块，总长度: 680
10:47:32 app.services.ai.http_ai_service INFO   流式响应Token统计: 5890 (prompt=5581, completion=309)
10:47:32 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:47:32 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:47:32 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=5890, cost=$0.010066, time=5658ms
10:47:32 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=5890
10:47:32 app.services.agent.langgraph_agent INFO   [JSON解析] 方法2成功: 从```json块提取
10:47:32 app.services.agent.langgraph_agent INFO   [Planning] 思维链: 输出=用户期望看到关于“老天师”能力的分析报告，需要对相关信息进行, 原料=需要查找作品中关于“老天师”能力的相关描, 处理=使用检索工具查找相关内容，然后使用分析工
10:47:32 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共2个任务，耗时: 5.76s
10:47:32 app.api.v1.agent INFO   [Stream] Plan tasks: 2 items
10:47:32 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
10:47:32 app.services.agent.langgraph_agent INFO   [DeepAgent] 启用反思模式
10:47:32 app.services.agent.parameter_resolver INFO   [ParameterResolver] 初始化完成, 严格模式: False
10:47:32 app.services.agent.langgraph_agent INFO   [DeepAgent] ParameterResolver 已启用
10:47:32 app.services.agent.deep_agent.executor INFO   DeepAgent 开始执行，共 2 个任务，反思功能已启用
10:47:32 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] AI 推断功能已启用
10:47:32 app.api.v1.agent INFO   [Stream] Task started: 搜索关于“老天师”能力的相关内容片段。
10:47:32 app.services.chapter_vector_service INFO   RAG retrieve work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18, current_order=51, query=老天师的能力...
10:47:33 app.services.chapter_vector_service INFO   RAG retrieved 10 segments within order<=53
10:47:33 app.services.agent.langgraph_tools INFO   [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
10:47:33 app.api.v1.agent INFO   [Stream] 任务完成: 搜索关于“老天师”能力的相关内容片段。 (0.6s)
10:47:33 app.services.agent.deep_agent.reflection INFO   [Checkpoint] 任务 1 标记了 checkpoint，触发反思
10:47:33 app.services.agent.deep_agent.executor INFO   任务 1 触发反思检查点
10:47:33 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:47:33 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:47:33 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
10:47:34 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:47:35 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
10:47:35 app.services.ai.http_ai_service INFO   流式响应Token统计: 388 (prompt=387, completion=1)
10:47:35 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:47:35 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:47:35 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=388, cost=$0.000494, time=1981ms
10:47:35 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=388
10:47:35 app.services.agent.deep_agent.reflection INFO   [DeepAgent反思] 开始调用 AI，task_id=1
10:47:35 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:47:35 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:47:35 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=500, temp=0.3, task_type=TaskType.SIMPLE_QA
10:47:36 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:47:43 app.services.ai.http_ai_service INFO   API 响应完成，共接收 2 个数据块，总长度: 142
10:47:43 app.services.ai.http_ai_service INFO   流式响应Token统计: 2338 (prompt=2257, completion=81)
10:47:43 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:47:43 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:47:43 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2338, cost=$0.003631, time=8513ms
10:47:43 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=2338
10:47:43 app.services.agent.deep_agent.reflection INFO   [Reflection] JSON提取成功: needs_replan=True
10:47:43 app.services.agent.deep_agent.executor INFO   [Reflection] 前置任务不触发重规划（已有后续输出任务）
10:47:43 app.api.v1.agent INFO   [Stream] Task started: 分析搜索到的片段，总结老天师的能力。
10:47:43 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
10:47:43 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
10:47:43 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
10:47:46 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:48:04 app.services.ai.http_ai_service INFO   API 响应完成，共接收 24 个数据块，总长度: 2085
10:48:04 app.services.ai.http_ai_service INFO   流式响应Token统计: 6614 (prompt=5093, completion=1521)
10:48:04 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:48:04 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:48:04 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=6614, cost=$0.021576, time=20907ms
10:48:04 app.services.agent.langgraph_tools INFO   ✅ [Agent分析] 分析完成，结果长度: 2085
10:48:04 app.api.v1.agent INFO   [Stream] 任务完成: 分析搜索到的片段，总结老天师的能力。 (21.0s)
10:48:04 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:48:04 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:48:04 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
10:48:06 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:48:07 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
10:48:07 app.services.ai.http_ai_service INFO   流式响应Token统计: 388 (prompt=387, completion=1)
10:48:07 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:48:07 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:48:07 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=388, cost=$0.000494, time=2903ms
10:48:07 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=388
10:48:07 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:48:07 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:48:07 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
10:48:09 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:48:11 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
10:48:11 app.services.ai.http_ai_service INFO   流式响应Token统计: 538 (prompt=537, completion=1)
10:48:11 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:48:11 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:48:11 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=538, cost=$0.000681, time=3605ms
10:48:11 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=538
10:48:11 app.services.agent.deep_agent.executor INFO   DeepAgent 执行完成: 任务=2, 反思=1, 重规划=0
10:48:11 app.services.agent.langgraph_agent INFO   [DeepAgent] 执行完成: 反思=1次, 重规划=0次
10:48:11 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共2个任务，耗时: 38.81s
10:48:11 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
10:48:11 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=1, 输出型=1, 展示型=0
10:48:11 app.services.agent.langgraph_agent INFO   [Response] 单个分析任务(analyze_text_tool)，使用AI格式化
10:48:11 app.services.agent.langgraph_agent INFO   [Summarization] 使用AI整合任务结果
10:48:11 app.services.agent.langgraph_agent INFO   [Summarization] 上下文压缩: 原始=5640字符, 压缩后=2144字符, 压缩率=62%
10:48:11 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
10:48:11 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
10:48:11 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
10:48:13 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:48:17 app.services.ai.http_ai_service INFO   API 响应完成，共接收 5 个数据块，总长度: 419
10:48:17 app.services.ai.http_ai_service INFO   流式响应Token统计: 2820 (prompt=2505, completion=315)
10:48:17 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:48:17 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:48:17 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2820, cost=$0.006281, time=6148ms
10:48:17 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=2820
10:48:18 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 隔离=work:07251ab5-98b3-4df7-b5f2-2bdb75201d18 | 重要度=0.51
10:48:18 app.services.context.store INFO   [ContextStore] 保存上下文: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:d1e4530e-2bf8-4502-a37f-deb843845a39, token=575
10:48:18 app.services.context.manager INFO   [ContextManager] 更新上下文: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:d1e4530e-2bf8-4502-a37f-deb843845a39, 消息数=4, Token=575
10:48:18 app.services.agent.langgraph_agent INFO   [Planning] 已保存对话到 ContextManager (session=602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:d1e4530e-2bf8-4502-a37f-deb843845a39)
10:48:18 app.api.v1.agent INFO   [Stream] 跳过最终响应（内容已流式发送）
10:48:18 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed
10:49:20 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
10:49:20 app.services.ai.http_ai_service INFO   ModelSelector 已启用
10:49:20 app.services.ai.http_ai_service INFO   AILogService 已启用 (用于成本追踪)
10:49:22 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
10:49:22 app.api.v1.agent INFO   [Chat Stream] Mode: planning
10:49:22 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:51207 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
10:49:22 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: planning, Message: 故事的主角是谁？...
10:49:22 app.api.v1.agent INFO   [agent_chat_stream] 📥 收到的 context 字段:
10:49:22 app.api.v1.agent INFO     - selected_text: N/A...
10:49:22 app.api.v1.agent INFO     - selection_position: N/A
10:49:22 app.api.v1.agent INFO     - chapter_context: 当前章节ID: a628af2c-98b5-44ba-b128-c8ca915861ce...
10:49:22 app.api.v1.agent INFO     - instruction_context: N/A...
10:49:22 app.services.agent.langgraph_agent INFO   [Planning] 使用隔离的thread_id: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:d1e4530e-2bf8-4502-a37f-deb843845a39 (user_id=602f5147-846a-4cde-95d3-405fa75f133f, work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18, conversation_id=d1e4530e-2bf8-4502-a37f-deb843845a39)
10:49:22 app.services.context.store INFO   [ContextStore] 加载上下文: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:d1e4530e-2bf8-4502-a37f-deb843845a39, 4条消息
10:49:22 app.services.context.manager INFO   [ContextManager] Session 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:d1e4530e-2bf8-4502-a37f-deb843845a39: 575/16000 tokens
10:49:22 app.services.context.vector_memory_store INFO   🔍 检索记忆 | 查询='故事的主角是谁？...' | 隔离键=['user:602f5147-846a-4cde-95d3-405fa75f133f:work:07251ab5-98b3-4df7-b5f2-2bdb75201d18', 'user:602f5147-846a-4cde-95d3-405fa75f133f'] | 找到=3条
10:49:22 app.services.context.manager INFO   🔍 检索长期记忆 | 级别=work | work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18 | 含用户级=True | 找到=3条
10:49:22 app.services.context.monitoring_integration INFO   [Monitor] 上下文构建: 5条消息, 575 tokens, 耗时 89.30ms
10:49:22 app.services.agent.langgraph_agent INFO   [Planning] 从 ContextManager 加载了 5 条历史消息 (token: 575)
10:49:22 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: 故事的主角是谁？...
10:49:22 app.core.cache INFO   ✅ 缓存命中: prompt:planning_agent:v2.9.1:get_planning_agent_mode_prompt:fca6eb91156619d0
10:49:22 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:49:22 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:49:22 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=1200, temp=0.3, task_type=TaskType.SIMPLE_QA
10:49:25 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:49:31 app.services.ai.http_ai_service INFO   API 响应完成，共接收 6 个数据块，总长度: 681
10:49:31 app.services.ai.http_ai_service INFO   流式响应Token统计: 6852 (prompt=6521, completion=331)
10:49:31 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:49:31 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:49:31 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=6852, cost=$0.011461, time=9064ms
10:49:31 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=6852
10:49:31 app.services.agent.langgraph_agent INFO   [JSON解析] 方法2成功: 从```json块提取
10:49:31 app.services.agent.langgraph_agent INFO   [Planning] 思维链: 输出=用户期望得到一个明确的答案，指出故事的主角是谁。这需要对现有, 原料=需要利用提供的 work_id 和 ch, 处理=使用 search_analysis_f
10:49:31 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共1个任务，耗时: 9.12s
10:49:31 app.api.v1.agent INFO   [Stream] Plan tasks: 1 items
10:49:31 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
10:49:31 app.services.agent.langgraph_agent INFO   [DeepAgent] 启用反思模式
10:49:31 app.services.agent.parameter_resolver INFO   [ParameterResolver] 初始化完成, 严格模式: False
10:49:31 app.services.agent.langgraph_agent INFO   [DeepAgent] ParameterResolver 已启用
10:49:31 app.services.agent.deep_agent.executor INFO   DeepAgent 开始执行，共 1 个任务，反思功能已启用
10:49:31 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] AI 推断功能已启用
10:49:31 app.api.v1.agent INFO   [Stream] Task started: 搜索关于故事主角的信息
10:49:31 app.services.chapter_vector_service INFO   RAG retrieve work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18, current_order=51, query=故事的主角...
10:49:32 app.services.chapter_vector_service INFO   RAG retrieved 10 segments within order<=53
10:49:32 app.services.agent.langgraph_tools INFO   [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
10:49:32 app.api.v1.agent INFO   [Stream] 任务完成: 搜索关于故事主角的信息 (0.5s)
10:49:32 app.services.agent.deep_agent.reflection INFO   [Checkpoint] 任务 1 标记了 checkpoint，触发反思
10:49:32 app.services.agent.deep_agent.executor INFO   任务 1 触发反思检查点
10:49:32 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:49:32 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:49:32 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
10:49:33 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:49:35 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
10:49:35 app.services.ai.http_ai_service INFO   流式响应Token统计: 536 (prompt=535, completion=1)
10:49:35 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:49:35 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:49:35 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=536, cost=$0.000679, time=2709ms
10:49:35 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=536
10:49:35 app.services.agent.deep_agent.reflection INFO   [DeepAgent反思] 开始调用 AI，task_id=1
10:49:35 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:49:35 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:49:35 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=500, temp=0.3, task_type=TaskType.SIMPLE_QA
10:49:36 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:49:38 app.services.ai.http_ai_service INFO   API 响应完成，共接收 2 个数据块，总长度: 145
10:49:38 app.services.ai.http_ai_service INFO   流式响应Token统计: 1149 (prompt=1070, completion=79)
10:49:38 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:49:38 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:49:38 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1149, cost=$0.002128, time=3702ms
10:49:38 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=1149
10:49:38 app.services.agent.deep_agent.reflection INFO   [Reflection] JSON提取成功: needs_replan=False
10:49:38 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:49:38 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:49:38 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
10:49:40 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:49:41 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
10:49:41 app.services.ai.http_ai_service INFO   流式响应Token统计: 532 (prompt=531, completion=1)
10:49:41 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:49:41 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:49:41 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=532, cost=$0.000674, time=3148ms
10:49:41 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=532
10:49:41 app.services.agent.deep_agent.executor INFO   DeepAgent 执行完成: 任务=1, 反思=1, 重规划=0
10:49:41 app.services.agent.langgraph_agent INFO   [DeepAgent] 执行完成: 反思=1次, 重规划=0次
10:49:41 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共1个任务，耗时: 10.15s
10:49:41 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
10:49:41 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=1, 输出型=0, 展示型=0
10:49:41 app.services.agent.langgraph_agent WARNING   [Response] 没有明确输出任务，使用AI整合
10:49:41 app.services.agent.langgraph_agent INFO   [Summarization] 使用AI整合任务结果
10:49:41 app.services.agent.langgraph_agent INFO   [Summarization] 上下文压缩: 原始=3332字符, 压缩后=107字符, 压缩率=97%
10:49:41 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
10:49:41 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
10:49:41 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
10:49:43 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:49:44 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 79
10:49:44 app.services.ai.http_ai_service INFO   流式响应Token统计: 482 (prompt=431, completion=51)
10:49:44 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:49:44 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:49:44 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=482, cost=$0.001049, time=2889ms
10:49:44 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=482
10:49:45 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 隔离=work:07251ab5-98b3-4df7-b5f2-2bdb75201d18 | 重要度=0.89
10:49:45 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 隔离=work:07251ab5-98b3-4df7-b5f2-2bdb75201d18 | 重要度=0.89
10:49:45 app.services.context.store INFO   [ContextStore] 保存上下文: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:d1e4530e-2bf8-4502-a37f-deb843845a39, token=623
10:49:45 app.services.context.manager INFO   [ContextManager] 更新上下文: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:d1e4530e-2bf8-4502-a37f-deb843845a39, 消息数=6, Token=623
10:49:45 app.services.agent.langgraph_agent INFO   [Planning] 已保存对话到 ContextManager (session=602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:d1e4530e-2bf8-4502-a37f-deb843845a39)
10:49:45 app.api.v1.agent INFO   [Stream] 跳过最终响应（内容已流式发送）
10:49:45 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed
10:50:00 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: 07251ab5-98b3-4df7-b5f2-2bdb75201d18, chapter_id: 08189013-3991-42c2-a37c-0f52bbcfe4a9
10:50:00 app.api.v1.ai INFO   [预加载] 当前章节已加载: 08189013-3991-42c2-a37c-0f52bbcfe4a9
10:50:00 app.api.v1.ai INFO   [预加载] 前一章节已加载: d9c7e7e4-532d-4b29-b149-9d8c319ef382
10:50:00 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
10:50:00 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:52445 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
10:50:01 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: 07251ab5-98b3-4df7-b5f2-2bdb75201d18, chapter_id: 08189013-3991-42c2-a37c-0f52bbcfe4a9
10:50:01 app.api.v1.ai INFO   [预加载] 当前章节已加载: 08189013-3991-42c2-a37c-0f52bbcfe4a9
10:50:01 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:54036 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
10:50:01 app.api.v1.ai INFO   [预加载] 前一章节已加载: d9c7e7e4-532d-4b29-b149-9d8c319ef382
10:50:01 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
10:50:01 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:54037 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
10:50:01 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:07251ab5-98b3-4df7-b5f2-2bdb75201d18
10:50:01 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/08189013-3991-42c2-a37c-0f52bbcfe4a9
INFO:     127.0.0.1:58654 - "PUT /api/v1/chapters/08189013-3991-42c2-a37c-0f52bbcfe4a9 HTTP/1.1" 200 OK
10:50:01 app.services.chapter_vector_service INFO   Vectorizing chapter: 第39章 【玉鼎洞天，马云长老】 (order=33)
10:50:02 app.services.chapter_vector_service INFO   Stored chapter vectors: 第39章 【玉鼎洞天，马云长老】 (5 chunks)
10:50:02 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:07251ab5-98b3-4df7-b5f2-2bdb75201d18
10:50:02 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/08189013-3991-42c2-a37c-0f52bbcfe4a9
INFO:     127.0.0.1:54516 - "PUT /api/v1/chapters/08189013-3991-42c2-a37c-0f52bbcfe4a9 HTTP/1.1" 200 OK
10:50:02 app.services.chapter_vector_service INFO   Vectorizing chapter: 第39章 【玉鼎洞天，马云长老】 (order=33)
10:50:03 app.services.chapter_vector_service INFO   Stored chapter vectors: 第39章 【玉鼎洞天，马云长老】 (5 chunks)
10:50:08 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:49385 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
10:50:08 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
10:50:08 app.services.ai.http_ai_service INFO   ModelSelector 已启用
10:50:08 app.services.ai.http_ai_service INFO   AILogService 已启用 (用于成本追踪)
10:50:12 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
10:50:12 app.api.v1.agent INFO   [Chat Stream] Mode: planning
10:50:12 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:55584 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
10:50:12 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: planning, Message: 故事的主角是谁？...
10:50:12 app.api.v1.agent INFO   [agent_chat_stream] 📥 收到的 context 字段:
10:50:12 app.api.v1.agent INFO     - selected_text: N/A...
10:50:12 app.api.v1.agent INFO     - selection_position: N/A
10:50:12 app.api.v1.agent INFO     - chapter_context: 当前章节ID: 08189013-3991-42c2-a37c-0f52bbcfe4a9...
10:50:12 app.api.v1.agent INFO     - instruction_context: N/A...
10:50:12 app.services.agent.langgraph_agent INFO   [Planning] 使用隔离的thread_id: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:055d2400-6ccd-4033-bd31-596b82e9a09a (user_id=602f5147-846a-4cde-95d3-405fa75f133f, work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18, conversation_id=055d2400-6ccd-4033-bd31-596b82e9a09a)
10:50:12 app.services.context.manager INFO   [ContextManager] 创建新上下文: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:055d2400-6ccd-4033-bd31-596b82e9a09a
10:50:12 app.services.context.manager INFO   [ContextManager] Session 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:055d2400-6ccd-4033-bd31-596b82e9a09a: 0/16000 tokens
10:50:13 app.services.context.vector_memory_store INFO   🔍 检索记忆 | 查询='故事的主角是谁？...' | 隔离键=['user:602f5147-846a-4cde-95d3-405fa75f133f:work:07251ab5-98b3-4df7-b5f2-2bdb75201d18', 'user:602f5147-846a-4cde-95d3-405fa75f133f'] | 找到=3条
10:50:13 app.services.context.manager INFO   🔍 检索长期记忆 | 级别=work | work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18 | 含用户级=True | 找到=3条
10:50:13 app.services.context.monitoring_integration INFO   [Monitor] 上下文构建: 1条消息, 0 tokens, 耗时 195.31ms
10:50:13 app.services.agent.langgraph_agent INFO   [Planning] 从 ContextManager 加载了 1 条历史消息 (token: 0)
10:50:13 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: 故事的主角是谁？...
10:50:13 app.core.cache INFO   ✅ 缓存命中: prompt:planning_agent:v2.9.1:get_planning_agent_mode_prompt:fca6eb91156619d0
10:50:13 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:50:13 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:50:13 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=1200, temp=0.3, task_type=TaskType.SIMPLE_QA
10:50:15 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:50:20 app.services.ai.http_ai_service INFO   API 响应完成，共接收 4 个数据块，总长度: 579
10:50:20 app.services.ai.http_ai_service INFO   流式响应Token统计: 5987 (prompt=5748, completion=239)
10:50:20 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:50:20 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:50:20 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=5987, cost=$0.009575, time=7612ms
10:50:20 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=5987
10:50:20 app.services.agent.langgraph_agent INFO   [JSON解析] 方法2成功: 从```json块提取
10:50:20 app.services.agent.langgraph_agent INFO   [Planning] 思维链: 输出=用户期望得到一个关于故事主角是谁的答案，这是一个分析性的输出, 原料=需要作品的上下文信息，以便识别主角。, 处理=使用get_context_tool获取
10:50:20 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共2个任务，耗时: 7.70s
10:50:20 app.api.v1.agent INFO   [Stream] Plan tasks: 2 items
10:50:20 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
10:50:20 app.services.agent.langgraph_agent INFO   [DeepAgent] 启用反思模式
10:50:20 app.services.agent.parameter_resolver INFO   [ParameterResolver] 初始化完成, 严格模式: False
10:50:20 app.services.agent.langgraph_agent INFO   [DeepAgent] ParameterResolver 已启用
10:50:20 app.services.agent.deep_agent.executor INFO   DeepAgent 开始执行，共 2 个任务，反思功能已启用
10:50:20 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] AI 推断功能已启用
10:50:20 app.api.v1.agent INFO   [Stream] Task started: 获取作品的上下文信息
10:50:20 app.services.chapter_vector_service INFO   RAG retrieve work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18, current_order=33, query=作品背景、人物关系、情节发展、伏笔线索...
10:50:21 app.services.chapter_vector_service INFO   RAG retrieved 5 segments within order<=33
10:50:21 app.services.agent.langgraph_tools INFO   [get_context_tool] ✅ 获取上下文成功
10:50:21 app.api.v1.agent INFO   [Stream] 任务完成: 获取作品的上下文信息 (0.5s)
10:50:21 app.services.agent.deep_agent.reflection INFO   [Checkpoint] 任务 1 标记了 checkpoint，触发反思
10:50:21 app.services.agent.deep_agent.executor INFO   任务 1 触发反思检查点
10:50:21 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:50:21 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:50:21 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
10:50:22 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:50:24 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
10:50:24 app.services.ai.http_ai_service INFO   流式响应Token统计: 601 (prompt=600, completion=1)
10:50:24 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:50:24 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:50:24 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=601, cost=$0.000760, time=3035ms
10:50:24 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=601
10:50:24 app.services.agent.deep_agent.reflection INFO   [DeepAgent反思] 开始调用 AI，task_id=1
10:50:24 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:50:24 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:50:24 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=500, temp=0.3, task_type=TaskType.SIMPLE_QA
10:50:26 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:50:28 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 109
10:50:28 app.services.ai.http_ai_service INFO   流式响应Token统计: 1024 (prompt=970, completion=54)
10:50:28 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:50:28 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:50:28 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1024, cost=$0.001753, time=3778ms
10:50:28 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=1024
10:50:28 app.services.agent.deep_agent.reflection INFO   [Reflection] JSON提取成功: needs_replan=False
10:50:28 app.api.v1.agent INFO   [Stream] Task started: 分析上下文，找出故事的主角
10:50:28 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
10:50:28 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
10:50:28 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
10:50:30 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:50:48 app.services.ai.http_ai_service INFO   API 响应完成，共接收 23 个数据块，总长度: 2119
10:50:48 app.services.ai.http_ai_service INFO   流式响应Token统计: 7879 (prompt=6387, completion=1492)
10:50:48 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:50:48 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:50:48 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=7879, cost=$0.022904, time=19893ms
10:50:48 app.services.agent.langgraph_tools INFO   ✅ [Agent分析] 分析完成，结果长度: 2119
10:50:48 app.api.v1.agent INFO   [Stream] 任务完成: 分析上下文，找出故事的主角 (19.9s)
10:50:48 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:50:48 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:50:48 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
10:50:49 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:50:51 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
10:50:51 app.services.ai.http_ai_service INFO   流式响应Token统计: 452 (prompt=451, completion=1)
10:50:51 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:50:51 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:50:51 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=452, cost=$0.000574, time=3332ms
10:50:51 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=452
10:50:51 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:50:51 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:50:51 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
10:50:53 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:50:54 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
10:50:54 app.services.ai.http_ai_service INFO   流式响应Token统计: 569 (prompt=568, completion=1)
10:50:54 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:50:54 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:50:54 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=569, cost=$0.000720, time=2995ms
10:50:54 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=569
10:50:54 app.services.agent.deep_agent.executor INFO   DeepAgent 执行完成: 任务=2, 反思=1, 重规划=0
10:50:54 app.services.agent.langgraph_agent INFO   [DeepAgent] 执行完成: 反思=1次, 重规划=0次
10:50:54 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共2个任务，耗时: 33.72s
10:50:54 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
10:50:54 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=1, 输出型=1, 展示型=0
10:50:54 app.services.agent.langgraph_agent INFO   [Response] 单个分析任务(analyze_text_tool)，使用AI格式化
10:50:54 app.services.agent.langgraph_agent INFO   [Summarization] 使用AI整合任务结果
10:50:54 app.services.agent.langgraph_agent INFO   [Summarization] 上下文压缩: 原始=6735字符, 压缩后=4087字符, 压缩率=40%
10:50:54 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
10:50:54 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
10:50:54 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
10:50:56 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:50:58 app.services.ai.http_ai_service INFO   API 响应完成，共接收 2 个数据块，总长度: 128
10:50:58 app.services.ai.http_ai_service INFO   流式响应Token统计: 3566 (prompt=3479, completion=87)
10:50:58 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:50:58 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:50:58 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=3566, cost=$0.005219, time=3641ms
10:50:58 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=3566
10:50:58 app.services.context.vector_memory_store INFO   🔁 跳过重复记忆，复用ID=602f5147-846a-4cde-95d3-405fa75f133f_1765507784852_367d8fb5
10:50:58 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 隔离=work:07251ab5-98b3-4df7-b5f2-2bdb75201d18 | 重要度=0.89
10:50:59 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 隔离=work:07251ab5-98b3-4df7-b5f2-2bdb75201d18 | 重要度=0.89
10:50:59 app.services.context.store INFO   [ContextStore] 保存上下文: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:055d2400-6ccd-4033-bd31-596b82e9a09a, token=78
10:50:59 app.services.context.manager INFO   [ContextManager] 更新上下文: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:055d2400-6ccd-4033-bd31-596b82e9a09a, 消息数=2, Token=78
10:50:59 app.services.agent.langgraph_agent INFO   [Planning] 已保存对话到 ContextManager (session=602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:055d2400-6ccd-4033-bd31-596b82e9a09a)
10:50:59 app.api.v1.agent INFO   [Stream] 跳过最终响应（内容已流式发送）
10:50:59 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed
10:51:33 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: 07251ab5-98b3-4df7-b5f2-2bdb75201d18, chapter_id: 029388c2-e2ac-4deb-92b0-2747e155e701
10:51:33 app.api.v1.ai INFO   [预加载] 当前章节已加载: 029388c2-e2ac-4deb-92b0-2747e155e701
10:51:33 app.api.v1.ai INFO   [预加载] 前一章节已加载: ca3e30d0-99e9-481a-8df1-56ee960f95e4
10:51:33 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
10:51:33 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:60835 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
10:51:33 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: 07251ab5-98b3-4df7-b5f2-2bdb75201d18, chapter_id: 029388c2-e2ac-4deb-92b0-2747e155e701
10:51:33 app.api.v1.ai INFO   [预加载] 当前章节已加载: 029388c2-e2ac-4deb-92b0-2747e155e701
10:51:33 app.api.v1.ai INFO   [预加载] 前一章节已加载: ca3e30d0-99e9-481a-8df1-56ee960f95e4
10:51:33 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
10:51:33 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:61720 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
10:51:33 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:61721 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
10:51:34 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:07251ab5-98b3-4df7-b5f2-2bdb75201d18
10:51:34 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/029388c2-e2ac-4deb-92b0-2747e155e701
INFO:     127.0.0.1:54828 - "PUT /api/v1/chapters/029388c2-e2ac-4deb-92b0-2747e155e701 HTTP/1.1" 200 OK
10:51:34 app.services.chapter_vector_service INFO   Vectorizing chapter: 第46章 【极道之耻，青帝后人】 (order=39)
10:51:35 app.services.chapter_vector_service INFO   Stored chapter vectors: 第46章 【极道之耻，青帝后人】 (5 chunks)
10:51:35 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:07251ab5-98b3-4df7-b5f2-2bdb75201d18
10:51:35 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/029388c2-e2ac-4deb-92b0-2747e155e701
INFO:     127.0.0.1:58575 - "PUT /api/v1/chapters/029388c2-e2ac-4deb-92b0-2747e155e701 HTTP/1.1" 200 OK
10:51:35 app.services.chapter_vector_service INFO   Vectorizing chapter: 第46章 【极道之耻，青帝后人】 (order=39)
10:51:36 app.services.chapter_vector_service INFO   Stored chapter vectors: 第46章 【极道之耻，青帝后人】 (5 chunks)
10:51:41 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:64493 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
10:51:41 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
10:51:41 app.services.ai.http_ai_service INFO   ModelSelector 已启用
10:51:41 app.services.ai.http_ai_service INFO   AILogService 已启用 (用于成本追踪)
10:51:44 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
10:51:44 app.api.v1.agent INFO   [Chat Stream] Mode: planning
10:51:44 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:54258 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
10:51:44 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: planning, Message: 马云长老是什么人？...
10:51:44 app.api.v1.agent INFO   [agent_chat_stream] 📥 收到的 context 字段:
10:51:44 app.api.v1.agent INFO     - selected_text: N/A...
10:51:44 app.api.v1.agent INFO     - selection_position: N/A
10:51:44 app.api.v1.agent INFO     - chapter_context: 当前章节ID: 029388c2-e2ac-4deb-92b0-2747e155e701...
10:51:44 app.api.v1.agent INFO     - instruction_context: N/A...
10:51:44 app.services.agent.langgraph_agent INFO   [Planning] 使用隔离的thread_id: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:3c185cff-0860-4984-8538-ad46765d7117 (user_id=602f5147-846a-4cde-95d3-405fa75f133f, work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18, conversation_id=3c185cff-0860-4984-8538-ad46765d7117)
10:51:44 app.services.context.manager INFO   [ContextManager] 创建新上下文: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:3c185cff-0860-4984-8538-ad46765d7117
10:51:44 app.services.context.manager INFO   [ContextManager] Session 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:3c185cff-0860-4984-8538-ad46765d7117: 0/16000 tokens
10:51:44 app.services.context.vector_memory_store INFO   🔍 检索记忆 | 查询='马云长老是什么人？...' | 隔离键=['user:602f5147-846a-4cde-95d3-405fa75f133f:work:07251ab5-98b3-4df7-b5f2-2bdb75201d18', 'user:602f5147-846a-4cde-95d3-405fa75f133f'] | 找到=3条
10:51:44 app.services.context.manager INFO   🔍 检索长期记忆 | 级别=work | work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18 | 含用户级=True | 找到=3条
10:51:44 app.services.context.monitoring_integration INFO   [Monitor] 上下文构建: 1条消息, 0 tokens, 耗时 219.48ms
10:51:44 app.services.agent.langgraph_agent INFO   [Planning] 从 ContextManager 加载了 1 条历史消息 (token: 0)
10:51:44 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: 马云长老是什么人？...
10:51:44 app.core.cache INFO   ✅ 缓存命中: prompt:planning_agent:v2.9.1:get_planning_agent_mode_prompt:fca6eb91156619d0
10:51:44 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:51:44 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:51:44 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=1200, temp=0.3, task_type=TaskType.SIMPLE_QA
10:51:47 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:51:51 app.services.ai.http_ai_service INFO   API 响应完成，共接收 6 个数据块，总长度: 802
10:51:51 app.services.ai.http_ai_service INFO   流式响应Token统计: 5717 (prompt=5340, completion=377)
10:51:51 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:51:51 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:51:51 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=5717, cost=$0.010445, time=6463ms
10:51:51 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=5717
10:51:51 app.services.agent.langgraph_agent INFO   [JSON解析] 方法2成功: 从```json块提取
10:51:51 app.services.agent.langgraph_agent INFO   [Planning] 思维链: 输出=用户想了解“马云长老”这个人物的身份信息，需要对作品中提及该, 原料=需要搜索作品中关于“马云长老”的描述片段, 处理=使用 search_analysis_f
10:51:51 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共2个任务，耗时: 6.53s
10:51:51 app.api.v1.agent INFO   [Stream] Plan tasks: 2 items
10:51:51 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
10:51:51 app.services.agent.langgraph_agent INFO   [DeepAgent] 启用反思模式
10:51:51 app.services.agent.parameter_resolver INFO   [ParameterResolver] 初始化完成, 严格模式: False
10:51:51 app.services.agent.langgraph_agent INFO   [DeepAgent] ParameterResolver 已启用
10:51:51 app.services.agent.deep_agent.executor INFO   DeepAgent 开始执行，共 2 个任务，反思功能已启用
10:51:51 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] AI 推断功能已启用
10:51:51 app.api.v1.agent INFO   [Stream] Task started: 搜索关于马云长老的内容
10:51:51 app.services.chapter_vector_service INFO   RAG retrieve work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18, current_order=39, query=马云长老...
10:51:51 app.services.chapter_vector_service INFO   RAG retrieved 10 segments within order<=41
10:51:51 app.services.agent.langgraph_tools INFO   [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
10:51:51 app.api.v1.agent INFO   [Stream] 任务完成: 搜索关于马云长老的内容 (0.4s)
10:51:51 app.services.agent.deep_agent.reflection INFO   [Checkpoint] 任务 1 标记了 checkpoint，触发反思
10:51:51 app.services.agent.deep_agent.executor INFO   任务 1 触发反思检查点
10:51:51 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:51:51 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:51:51 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
10:51:53 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:51:54 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
10:51:54 app.services.ai.http_ai_service INFO   流式响应Token统计: 415 (prompt=414, completion=1)
10:51:54 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:51:55 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:51:55 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=415, cost=$0.000527, time=2900ms
10:51:55 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=415
10:51:55 app.services.agent.deep_agent.reflection INFO   [DeepAgent反思] 开始调用 AI，task_id=1
10:51:55 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:51:55 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:51:55 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=500, temp=0.3, task_type=TaskType.SIMPLE_QA
10:51:57 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:52:01 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 125
10:52:01 app.services.ai.http_ai_service INFO   流式响应Token统计: 1474 (prompt=1409, completion=65)
10:52:01 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:52:01 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:52:01 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1474, cost=$0.002411, time=6546ms
10:52:01 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=1474
10:52:01 app.services.agent.deep_agent.reflection INFO   [Reflection] JSON提取成功: needs_replan=False
10:52:01 app.api.v1.agent INFO   [Stream] Task started: 概括马云长老的身份信息
10:52:01 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
10:52:01 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
10:52:01 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
10:52:03 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:52:15 app.services.ai.http_ai_service INFO   API 响应完成，共接收 22 个数据块，总长度: 2042
10:52:15 app.services.ai.http_ai_service INFO   流式响应Token统计: 4941 (prompt=3505, completion=1436)
10:52:15 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:52:15 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:52:15 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4941, cost=$0.018741, time=13701ms
10:52:15 app.services.agent.langgraph_tools INFO   ✅ [Agent分析] 分析完成，结果长度: 2042
10:52:15 app.api.v1.agent INFO   [Stream] 任务完成: 概括马云长老的身份信息 (13.8s)
10:52:15 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:52:15 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:52:15 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
10:52:17 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:52:17 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
10:52:17 app.services.ai.http_ai_service INFO   流式响应Token统计: 400 (prompt=399, completion=1)
10:52:17 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:52:17 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:52:17 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=400, cost=$0.000509, time=2242ms
10:52:17 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=400
10:52:17 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:52:17 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:52:17 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
10:52:19 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:52:21 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
10:52:21 app.services.ai.http_ai_service INFO   流式响应Token统计: 515 (prompt=514, completion=1)
10:52:21 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:52:21 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:52:21 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=515, cost=$0.000653, time=3507ms
10:52:21 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=515
10:52:21 app.services.agent.deep_agent.executor INFO   DeepAgent 执行完成: 任务=2, 反思=1, 重规划=0
10:52:21 app.services.agent.langgraph_agent INFO   [DeepAgent] 执行完成: 反思=1次, 重规划=0次
10:52:21 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共2个任务，耗时: 30.39s
10:52:21 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
10:52:21 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=1, 输出型=1, 展示型=0
10:52:21 app.services.agent.langgraph_agent INFO   [Response] 单个分析任务(analyze_text_tool)，使用AI格式化
10:52:21 app.services.agent.langgraph_agent INFO   [Summarization] 使用AI整合任务结果
10:52:21 app.services.agent.langgraph_agent INFO   [Summarization] 上下文压缩: 原始=5267字符, 压缩后=2133字符, 压缩率=60%
10:52:21 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
10:52:21 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
10:52:21 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
10:52:23 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:52:26 app.services.ai.http_ai_service INFO   API 响应完成，共接收 6 个数据块，总长度: 566
10:52:26 app.services.ai.http_ai_service INFO   流式响应Token统计: 2444 (prompt=2053, completion=391)
10:52:26 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:52:26 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:52:26 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2444, cost=$0.006476, time=4732ms
10:52:26 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=2444
10:52:27 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 隔离=work:07251ab5-98b3-4df7-b5f2-2bdb75201d18 | 重要度=0.91
10:52:27 app.services.context.store INFO   [ContextStore] 保存上下文: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:3c185cff-0860-4984-8538-ad46765d7117, token=319
10:52:27 app.services.context.manager INFO   [ContextManager] 更新上下文: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:3c185cff-0860-4984-8538-ad46765d7117, 消息数=2, Token=319
10:52:27 app.services.agent.langgraph_agent INFO   [Planning] 已保存对话到 ContextManager (session=602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:3c185cff-0860-4984-8538-ad46765d7117)
10:52:27 app.api.v1.agent INFO   [Stream] 跳过最终响应（内容已流式发送）
10:52:27 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed
10:53:42 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
10:53:42 app.services.ai.http_ai_service INFO   ModelSelector 已启用
10:53:42 app.services.ai.http_ai_service INFO   AILogService 已启用 (用于成本追踪)
10:53:44 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
10:53:44 app.api.v1.agent INFO   [Chat Stream] Mode: planning
10:53:44 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:49600 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
10:53:44 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: planning, Message: 狠人女帝出场了吗？...
10:53:44 app.api.v1.agent INFO   [agent_chat_stream] 📥 收到的 context 字段:
10:53:44 app.api.v1.agent INFO     - selected_text: N/A...
10:53:44 app.api.v1.agent INFO     - selection_position: N/A
10:53:44 app.api.v1.agent INFO     - chapter_context: 当前章节ID: 029388c2-e2ac-4deb-92b0-2747e155e701...
10:53:44 app.api.v1.agent INFO     - instruction_context: N/A...
10:53:44 app.services.agent.langgraph_agent INFO   [Planning] 使用隔离的thread_id: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:3c185cff-0860-4984-8538-ad46765d7117 (user_id=602f5147-846a-4cde-95d3-405fa75f133f, work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18, conversation_id=3c185cff-0860-4984-8538-ad46765d7117)
10:53:44 app.services.context.store INFO   [ContextStore] 加载上下文: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:3c185cff-0860-4984-8538-ad46765d7117, 2条消息
10:53:44 app.services.context.manager INFO   [ContextManager] Session 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:3c185cff-0860-4984-8538-ad46765d7117: 319/16000 tokens
10:53:44 app.services.context.vector_memory_store INFO   🔍 检索记忆 | 查询='狠人女帝出场了吗？...' | 隔离键=['user:602f5147-846a-4cde-95d3-405fa75f133f:work:07251ab5-98b3-4df7-b5f2-2bdb75201d18', 'user:602f5147-846a-4cde-95d3-405fa75f133f'] | 找到=3条
10:53:44 app.services.context.manager INFO   🔍 检索长期记忆 | 级别=work | work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18 | 含用户级=True | 找到=3条
10:53:44 app.services.context.monitoring_integration INFO   [Monitor] 上下文构建: 3条消息, 319 tokens, 耗时 219.21ms
10:53:44 app.services.agent.langgraph_agent INFO   [Planning] 从 ContextManager 加载了 3 条历史消息 (token: 319)
10:53:44 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: 狠人女帝出场了吗？...
10:53:44 app.core.cache INFO   ✅ 缓存命中: prompt:planning_agent:v2.9.1:get_planning_agent_mode_prompt:fca6eb91156619d0
10:53:44 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:53:44 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:53:44 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=1200, temp=0.3, task_type=TaskType.SIMPLE_QA
10:53:47 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:53:49 app.services.ai.http_ai_service INFO   API 响应完成，共接收 5 个数据块，总长度: 620
10:53:49 app.services.ai.http_ai_service INFO   流式响应Token统计: 5651 (prompt=5344, completion=307)
10:53:49 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:53:49 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:53:49 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=5651, cost=$0.009750, time=4958ms
10:53:49 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=5651
10:53:49 app.services.agent.langgraph_agent INFO   [JSON解析] 方法2成功: 从```json块提取
10:53:49 app.services.agent.langgraph_agent INFO   [Planning] 思维链: 输出=用户期望得到一个关于“狠人女帝”是否在故事中出场的答案，可能, 原料=需要搜索作品内容，查找“狠人女帝”这个关, 处理=使用 search_analysis_f
10:53:49 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共1个任务，耗时: 5.02s
10:53:49 app.api.v1.agent INFO   [Stream] Plan tasks: 1 items
10:53:49 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
10:53:49 app.services.agent.langgraph_agent INFO   [DeepAgent] 启用反思模式
10:53:49 app.services.agent.parameter_resolver INFO   [ParameterResolver] 初始化完成, 严格模式: False
10:53:49 app.services.agent.langgraph_agent INFO   [DeepAgent] ParameterResolver 已启用
10:53:49 app.services.agent.deep_agent.executor INFO   DeepAgent 开始执行，共 1 个任务，反思功能已启用
10:53:49 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] AI 推断功能已启用
10:53:49 app.api.v1.agent INFO   [Stream] Task started: 搜索作品中关于“狠人女帝”的内容片段
10:53:49 app.services.chapter_vector_service INFO   RAG retrieve work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18, current_order=39, query=狠人女帝...
10:53:50 app.services.chapter_vector_service INFO   RAG retrieved 10 segments within order<=41
10:53:50 app.services.agent.langgraph_tools INFO   [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
10:53:50 app.api.v1.agent INFO   [Stream] 任务完成: 搜索作品中关于“狠人女帝”的内容片段 (0.4s)
10:53:50 app.services.agent.deep_agent.reflection INFO   [Checkpoint] 任务 1 标记了 checkpoint，触发反思
10:53:50 app.services.agent.deep_agent.executor INFO   任务 1 触发反思检查点
10:53:50 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:53:50 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:53:50 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
10:53:51 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:53:53 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
10:53:53 app.services.ai.http_ai_service INFO   流式响应Token统计: 534 (prompt=533, completion=1)
10:53:53 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:53:53 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:53:53 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=534, cost=$0.000676, time=3107ms
10:53:53 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=534
10:53:53 app.services.agent.deep_agent.reflection INFO   [DeepAgent反思] 开始调用 AI，task_id=1
10:53:53 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:53:53 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:53:53 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=500, temp=0.3, task_type=TaskType.SIMPLE_QA
10:53:54 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:53:58 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 111
10:53:58 app.services.ai.http_ai_service INFO   流式响应Token统计: 1266 (prompt=1208, completion=58)
10:53:58 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:53:58 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:53:58 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1266, cost=$0.002090, time=5207ms
10:53:58 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=1266
10:53:58 app.services.agent.deep_agent.reflection INFO   [Reflection] JSON提取成功: needs_replan=False
10:53:58 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:53:58 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:53:58 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
10:54:00 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:54:01 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
10:54:01 app.services.ai.http_ai_service INFO   流式响应Token统计: 500 (prompt=499, completion=1)
10:54:01 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:54:01 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:54:01 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=500, cost=$0.000634, time=2747ms
10:54:01 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=500
10:54:01 app.services.agent.deep_agent.executor INFO   DeepAgent 执行完成: 任务=1, 反思=1, 重规划=0
10:54:01 app.services.agent.langgraph_agent INFO   [DeepAgent] 执行完成: 反思=1次, 重规划=0次
10:54:01 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共1个任务，耗时: 11.59s
10:54:01 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
10:54:01 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=1, 输出型=0, 展示型=0
10:54:01 app.services.agent.langgraph_agent WARNING   [Response] 没有明确输出任务，使用AI整合
10:54:01 app.services.agent.langgraph_agent INFO   [Summarization] 使用AI整合任务结果
10:54:01 app.services.agent.langgraph_agent INFO   [Summarization] 上下文压缩: 原始=3290字符, 压缩后=105字符, 压缩率=97%
10:54:01 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
10:54:01 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
10:54:01 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
10:54:03 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:54:05 app.services.ai.http_ai_service INFO   API 响应完成，共接收 2 个数据块，总长度: 109
10:54:05 app.services.ai.http_ai_service INFO   流式响应Token统计: 526 (prompt=454, completion=72)
10:54:05 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:54:05 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:54:05 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=526, cost=$0.001288, time=3767ms
10:54:05 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=526
10:54:06 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 隔离=work:07251ab5-98b3-4df7-b5f2-2bdb75201d18 | 重要度=0.57
10:54:06 app.services.context.store INFO   [ContextStore] 保存上下文: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:3c185cff-0860-4984-8538-ad46765d7117, token=388
10:54:06 app.services.context.manager INFO   [ContextManager] 更新上下文: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:3c185cff-0860-4984-8538-ad46765d7117, 消息数=4, Token=388
10:54:06 app.services.agent.langgraph_agent INFO   [Planning] 已保存对话到 ContextManager (session=602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:3c185cff-0860-4984-8538-ad46765d7117)
10:54:06 app.api.v1.agent INFO   [Stream] 跳过最终响应（内容已流式发送）
10:54:06 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed
10:54:45 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
10:54:45 app.services.ai.http_ai_service INFO   ModelSelector 已启用
10:54:45 app.services.ai.http_ai_service INFO   AILogService 已启用 (用于成本追踪)
10:54:47 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
10:54:47 app.api.v1.agent INFO   [Chat Stream] Mode: planning
10:54:47 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:59841 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
10:54:47 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: planning, Message: 是什么？...
10:54:47 app.api.v1.agent INFO   [agent_chat_stream] 📥 收到的 context 字段:
10:54:47 app.api.v1.agent INFO     - selected_text: N/A...
10:54:47 app.api.v1.agent INFO     - selection_position: N/A
10:54:47 app.api.v1.agent INFO     - chapter_context: 当前章节ID: 029388c2-e2ac-4deb-92b0-2747e155e701...
10:54:47 app.api.v1.agent INFO     - instruction_context: N/A...
10:54:47 app.services.agent.langgraph_agent INFO   [Planning] 使用隔离的thread_id: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:3c185cff-0860-4984-8538-ad46765d7117 (user_id=602f5147-846a-4cde-95d3-405fa75f133f, work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18, conversation_id=3c185cff-0860-4984-8538-ad46765d7117)
10:54:47 app.services.context.store INFO   [ContextStore] 加载上下文: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:3c185cff-0860-4984-8538-ad46765d7117, 4条消息
10:54:47 app.services.context.manager INFO   [ContextManager] Session 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:3c185cff-0860-4984-8538-ad46765d7117: 388/16000 tokens
10:54:47 app.services.context.vector_memory_store INFO   🔍 检索记忆 | 查询='是什么？...' | 隔离键=['user:602f5147-846a-4cde-95d3-405fa75f133f:work:07251ab5-98b3-4df7-b5f2-2bdb75201d18', 'user:602f5147-846a-4cde-95d3-405fa75f133f'] | 找到=3条
10:54:47 app.services.context.manager INFO   🔍 检索长期记忆 | 级别=work | work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18 | 含用户级=True | 找到=3条
10:54:47 app.services.context.monitoring_integration INFO   [Monitor] 上下文构建: 5条消息, 388 tokens, 耗时 89.02ms
10:54:47 app.services.agent.langgraph_agent INFO   [Planning] 从 ContextManager 加载了 5 条历史消息 (token: 388)
10:54:47 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: 是什么？...
10:54:47 app.core.cache INFO   ✅ 缓存命中: prompt:planning_agent:v2.9.1:get_planning_agent_mode_prompt:fca6eb91156619d0
10:54:47 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:54:47 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:54:47 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=1200, temp=0.3, task_type=TaskType.SIMPLE_QA
10:54:50 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:55:08 app.services.ai.http_ai_service INFO   API 响应完成，共接收 9 个数据块，总长度: 1104
10:55:08 app.services.ai.http_ai_service INFO   流式响应Token统计: 10380 (prompt=9803, completion=577)
10:55:08 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:55:08 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:55:08 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=10380, cost=$0.018024, time=21219ms
10:55:08 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=10380
10:55:08 app.services.agent.langgraph_agent INFO   [JSON解析] 方法2成功: 从```json块提取
10:55:08 app.services.agent.langgraph_agent INFO   [Planning] 思维链: 输出=用户期望看到对指定章节内容的概括或分析，以回答“是什么？”这, 原料=需要获取 work_id 为 '0725, 处理=首先使用 `read_chapter_t
10:55:08 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共2个任务，耗时: 21.24s
10:55:08 app.api.v1.agent INFO   [Stream] Plan tasks: 2 items
10:55:08 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
10:55:08 app.services.agent.langgraph_agent INFO   [DeepAgent] 启用反思模式
10:55:08 app.services.agent.parameter_resolver INFO   [ParameterResolver] 初始化完成, 严格模式: False
10:55:08 app.services.agent.langgraph_agent INFO   [DeepAgent] ParameterResolver 已启用
10:55:08 app.services.agent.deep_agent.executor INFO   DeepAgent 开始执行，共 2 个任务，反思功能已启用
10:55:08 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] AI 推断功能已启用
10:55:08 app.api.v1.agent INFO   [Stream] Task started: 获取指定章节的内容
10:55:08 app.services.agent.langgraph_tools INFO   [read_chapter_tool] ✅ 读取章节成功: 第46章 【极道之耻，青帝后人】
10:55:08 app.api.v1.agent INFO   [Stream] 任务完成: 获取指定章节的内容 (0.0s)
10:55:08 app.services.agent.deep_agent.reflection INFO   [Checkpoint] 任务 1 标记了 checkpoint，触发反思
10:55:08 app.services.agent.deep_agent.executor INFO   任务 1 触发反思检查点
10:55:08 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:55:08 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:55:08 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
10:55:10 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:55:11 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
10:55:11 app.services.ai.http_ai_service INFO   流式响应Token统计: 684 (prompt=683, completion=1)
10:55:11 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:55:11 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:55:11 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=684, cost=$0.000864, time=3362ms
10:55:11 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=684
10:55:11 app.services.agent.deep_agent.reflection INFO   [DeepAgent反思] 开始调用 AI，task_id=1
10:55:11 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:55:11 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:55:11 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=500, temp=0.3, task_type=TaskType.SIMPLE_QA
10:55:13 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:55:19 app.services.ai.http_ai_service INFO   API 响应完成，共接收 2 个数据块，总长度: 129
10:55:19 app.services.ai.http_ai_service INFO   流式响应Token统计: 1933 (prompt=1864, completion=69)
10:55:19 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:55:19 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:55:19 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1933, cost=$0.003020, time=7379ms
10:55:19 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=1933
10:55:19 app.services.agent.deep_agent.reflection INFO   [Reflection] JSON提取成功: needs_replan=True
10:55:19 app.services.agent.deep_agent.executor INFO   反思结果需要重规划 (第 1 次)
10:55:19 app.services.agent.deep_agent.executor INFO   [DeepAgent重规划] 开始调用 AI
10:55:19 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:55:19 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:55:19 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=800, temp=0.2, task_type=TaskType.SIMPLE_QA
10:55:21 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:55:27 app.services.ai.http_ai_service INFO   API 响应完成，共接收 2 个数据块，总长度: 186
10:55:27 app.services.ai.http_ai_service INFO   流式响应Token统计: 1816 (prompt=1715, completion=101)
10:55:27 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:55:27 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:55:27 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1816, cost=$0.003154, time=8297ms
10:55:27 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=1816
10:55:27 app.services.agent.deep_agent.executor INFO   [DeepAgent重规划] 成功生成 2 个新任务
10:55:27 app.api.v1.agent INFO   [Stream] Plan tasks: 3 items
10:55:27 app.services.agent.deep_agent.executor INFO   计划已更新，新任务数: 2
10:55:27 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:55:27 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:55:27 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=200, temp=0.1, task_type=TaskType.SIMPLE_QA
10:55:29 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:55:32 app.services.ai.http_ai_service INFO   API 响应完成，共接收 2 个数据块，总长度: 166
10:55:32 app.services.ai.http_ai_service INFO   流式响应Token统计: 1441 (prompt=1360, completion=81)
10:55:32 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:55:32 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:55:32 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1441, cost=$0.002510, time=4448ms
10:55:32 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=1441
10:55:32 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] 从 1 个任务结果中提取文本，总长度: 2478 字符
10:55:32 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] AI 推断成功: '概括章节（chapter_id: 029388c2-e2ac...' → tool=analyze_text_tool
10:55:32 app.api.v1.agent INFO   [Stream] Task started: 概括章节（chapter_id: 029388c2-e2ac-4deb-92b0-2747e155e701）的内容。
10:55:32 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
10:55:32 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
10:55:32 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
10:55:33 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:55:52 app.services.ai.http_ai_service INFO   API 响应完成，共接收 32 个数据块，总长度: 2821
10:55:52 app.services.ai.http_ai_service INFO   流式响应Token统计: 6377 (prompt=4285, completion=2092)
10:55:52 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:55:52 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:55:52 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=6377, cost=$0.026276, time=19853ms
10:55:52 app.services.agent.langgraph_tools INFO   ✅ [Agent分析] 分析完成，结果长度: 2821
10:55:52 app.api.v1.agent INFO   [Stream] 任务完成: 概括章节（chapter_id: 029388c2-e2ac-4deb-92b0-2747e155e701）的内容。 (19.9s)
10:55:52 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:55:52 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:55:52 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=200, temp=0.1, task_type=TaskType.SIMPLE_QA
10:55:53 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:55:55 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 131
10:55:55 app.services.ai.http_ai_service INFO   流式响应Token统计: 755 (prompt=695, completion=60)
10:55:55 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:55:55 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:55:55 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=755, cost=$0.001469, time=3297ms
10:55:55 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=755
10:55:55 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] 从 2 个任务结果中提取文本，总长度: 5301 字符
10:55:55 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] AI 推断成功: '检查章节内容是否提及“狠人女帝”，并进行关联。...' → tool=analyze_text_tool
10:55:55 app.api.v1.agent INFO   [Stream] Task started: 检查章节内容是否提及“狠人女帝”，并进行关联。
10:55:55 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
10:55:55 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
10:55:55 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
10:55:57 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:56:04 app.services.ai.http_ai_service INFO   API 响应完成，共接收 32 个数据块，总长度: 2825
10:56:04 app.services.ai.http_ai_service INFO   流式响应Token统计: 7127 (prompt=5032, completion=2095)
10:56:04 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:56:04 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:56:04 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=7127, cost=$0.027240, time=9341ms
10:56:04 app.services.agent.langgraph_tools INFO   ✅ [Agent分析] 分析完成，结果长度: 2825
10:56:04 app.api.v1.agent INFO   [Stream] 任务完成: 检查章节内容是否提及“狠人女帝”，并进行关联。 (9.4s)
10:56:04 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:56:04 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:56:04 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
10:56:06 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:56:08 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
10:56:08 app.services.ai.http_ai_service INFO   流式响应Token统计: 635 (prompt=634, completion=1)
10:56:08 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:56:08 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:56:08 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=635, cost=$0.000803, time=3473ms
10:56:08 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=635
10:56:08 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:56:08 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:56:08 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
10:56:09 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:56:10 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
10:56:10 app.services.ai.http_ai_service INFO   流式响应Token统计: 579 (prompt=578, completion=1)
10:56:10 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:56:10 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:56:10 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=579, cost=$0.000732, time=2684ms
10:56:11 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=579
10:56:11 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:56:11 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:56:11 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
10:56:12 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:56:14 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
10:56:14 app.services.ai.http_ai_service INFO   流式响应Token统计: 756 (prompt=755, completion=1)
10:56:14 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:56:14 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:56:14 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=756, cost=$0.000954, time=3876ms
10:56:14 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=756
10:56:14 app.services.agent.deep_agent.executor INFO   DeepAgent 执行完成: 任务=3, 反思=1, 重规划=1
10:56:14 app.services.agent.langgraph_agent INFO   [DeepAgent] 执行完成: 反思=1次, 重规划=1次
10:56:14 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共3个任务，耗时: 66.35s
10:56:14 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
10:56:14 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=0, 输出型=2, 展示型=1
10:56:14 app.services.agent.langgraph_agent INFO   [Response] 2个分析类任务，使用AI整合（避免冗余）
10:56:14 app.services.agent.langgraph_agent INFO   [Summarization] 使用AI整合任务结果
10:56:14 app.services.agent.langgraph_agent INFO   [Summarization] 上下文压缩: 原始=8162字符, 压缩后=4144字符, 压缩率=50%
10:56:14 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
10:56:14 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
10:56:14 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
10:56:16 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:56:22 app.services.ai.http_ai_service INFO   API 响应完成，共接收 10 个数据块，总长度: 808
10:56:22 app.services.ai.http_ai_service INFO   流式响应Token统计: 4881 (prompt=4270, completion=611)
10:56:22 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:56:22 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:56:22 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4881, cost=$0.011447, time=7447ms
10:56:22 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=4881
10:56:23 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 隔离=work:07251ab5-98b3-4df7-b5f2-2bdb75201d18 | 重要度=0.92
10:56:23 app.services.context.store INFO   [ContextStore] 保存上下文: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:3c185cff-0860-4984-8538-ad46765d7117, token=828
10:56:23 app.services.context.manager INFO   [ContextManager] 更新上下文: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:3c185cff-0860-4984-8538-ad46765d7117, 消息数=6, Token=828
10:56:23 app.services.agent.langgraph_agent INFO   [Planning] 已保存对话到 ContextManager (session=602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:3c185cff-0860-4984-8538-ad46765d7117)
10:56:23 app.api.v1.agent INFO   [Stream] 跳过最终响应（内容已流式发送）
10:56:23 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed
10:57:31 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: 07251ab5-98b3-4df7-b5f2-2bdb75201d18, chapter_id: d2063c51-2364-4b9e-816c-3696cf98c28d
10:57:31 app.api.v1.ai INFO   [预加载] 当前章节已加载: d2063c51-2364-4b9e-816c-3696cf98c28d
10:57:31 app.api.v1.ai INFO   [预加载] 前一章节已加载: 18875b96-43d7-4aae-b9f1-c77adbdb3f86
10:57:31 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
10:57:31 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:50971 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
10:57:31 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: 07251ab5-98b3-4df7-b5f2-2bdb75201d18, chapter_id: d2063c51-2364-4b9e-816c-3696cf98c28d
10:57:31 app.api.v1.ai INFO   [预加载] 当前章节已加载: d2063c51-2364-4b9e-816c-3696cf98c28d
10:57:31 app.api.v1.ai INFO   [预加载] 前一章节已加载: 18875b96-43d7-4aae-b9f1-c77adbdb3f86
10:57:31 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
10:57:31 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:65048 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
10:57:31 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:65049 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
10:57:32 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:07251ab5-98b3-4df7-b5f2-2bdb75201d18
10:57:32 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/d2063c51-2364-4b9e-816c-3696cf98c28d
INFO:     127.0.0.1:64237 - "PUT /api/v1/chapters/d2063c51-2364-4b9e-816c-3696cf98c28d HTTP/1.1" 200 OK
10:57:32 app.services.chapter_vector_service INFO   Vectorizing chapter: 第7章 【帝星飘摇荧惑高】（4400） (order=7)
10:57:33 app.services.chapter_vector_service INFO   Stored chapter vectors: 第7章 【帝星飘摇荧惑高】（4400） (10 chunks)
10:57:33 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:07251ab5-98b3-4df7-b5f2-2bdb75201d18
10:57:33 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/d2063c51-2364-4b9e-816c-3696cf98c28d
INFO:     127.0.0.1:49718 - "PUT /api/v1/chapters/d2063c51-2364-4b9e-816c-3696cf98c28d HTTP/1.1" 200 OK
10:57:33 app.services.chapter_vector_service INFO   Vectorizing chapter: 第7章 【帝星飘摇荧惑高】（4400） (order=7)
10:57:34 app.services.chapter_vector_service INFO   Stored chapter vectors: 第7章 【帝星飘摇荧惑高】（4400） (10 chunks)
10:57:45 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:64446 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
10:57:45 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
10:57:45 app.services.ai.http_ai_service INFO   ModelSelector 已启用
10:57:45 app.services.ai.http_ai_service INFO   AILogService 已启用 (用于成本追踪)
10:57:48 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
10:57:48 app.api.v1.agent INFO   [Chat Stream] Mode: planning
10:57:48 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:58955 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
10:57:48 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: planning, Message: ？？？...
10:57:48 app.api.v1.agent INFO   [agent_chat_stream] 📥 收到的 context 字段:
10:57:48 app.api.v1.agent INFO     - selected_text: N/A...
10:57:48 app.api.v1.agent INFO     - selection_position: N/A
10:57:48 app.api.v1.agent INFO     - chapter_context: 当前章节ID: d2063c51-2364-4b9e-816c-3696cf98c28d...
10:57:48 app.api.v1.agent INFO     - instruction_context: N/A...
10:57:48 app.services.agent.langgraph_agent INFO   [Planning] 使用隔离的thread_id: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:4e349d4e-2da0-4d4a-a167-8e6f5ac29981 (user_id=602f5147-846a-4cde-95d3-405fa75f133f, work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18, conversation_id=4e349d4e-2da0-4d4a-a167-8e6f5ac29981)
10:57:48 app.services.context.manager INFO   [ContextManager] 创建新上下文: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:4e349d4e-2da0-4d4a-a167-8e6f5ac29981
10:57:48 app.services.context.manager INFO   [ContextManager] Session 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:4e349d4e-2da0-4d4a-a167-8e6f5ac29981: 0/16000 tokens
10:57:48 app.services.context.vector_memory_store INFO   🔍 检索记忆 | 查询='？？？...' | 隔离键=['user:602f5147-846a-4cde-95d3-405fa75f133f:work:07251ab5-98b3-4df7-b5f2-2bdb75201d18', 'user:602f5147-846a-4cde-95d3-405fa75f133f'] | 找到=0条
10:57:48 app.services.context.manager INFO   🔍 检索长期记忆 | 级别=work | work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18 | 含用户级=True | 找到=0条
10:57:48 app.services.context.monitoring_integration INFO   [Monitor] 上下文构建: 0条消息, 0 tokens, 耗时 229.87ms
10:57:48 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: ？？？...
10:57:49 app.core.cache INFO   ✅ 缓存命中: prompt:planning_agent:v2.9.1:get_planning_agent_mode_prompt:fca6eb91156619d0
10:57:49 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:57:49 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:57:49 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=1200, temp=0.3, task_type=TaskType.SIMPLE_QA
10:57:51 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:58:00 app.services.ai.http_ai_service INFO   API 响应完成，共接收 9 个数据块，总长度: 1003
10:58:00 app.services.ai.http_ai_service INFO   流式响应Token统计: 8276 (prompt=7755, completion=521)
10:58:00 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:58:00 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:58:00 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=8276, cost=$0.014904, time=11551ms
10:58:00 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=8276
10:58:00 app.services.agent.langgraph_agent INFO   [JSON解析] 方法2成功: 从```json块提取
10:58:00 app.services.agent.langgraph_agent INFO   [Planning] 思维链: 输出=用户输入'???', 意图不明。鉴于当前用户处于特定章节（c, 原料=需要获取当前章节 `d2063c51-2, 处理=使用 `read_chapter_too
10:58:00 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共2个任务，耗时: 11.58s
10:58:00 app.api.v1.agent INFO   [Stream] Plan tasks: 2 items
10:58:00 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
10:58:00 app.services.agent.langgraph_agent INFO   [DeepAgent] 启用反思模式
10:58:00 app.services.agent.parameter_resolver INFO   [ParameterResolver] 初始化完成, 严格模式: False
10:58:00 app.services.agent.langgraph_agent INFO   [DeepAgent] ParameterResolver 已启用
10:58:00 app.services.agent.deep_agent.executor INFO   DeepAgent 开始执行，共 2 个任务，反思功能已启用
10:58:00 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] AI 推断功能已启用
10:58:00 app.api.v1.agent INFO   [Stream] Task started: 读取当前章节内容
10:58:00 app.services.agent.langgraph_tools INFO   [read_chapter_tool] ✅ 读取章节成功: 第7章 【帝星飘摇荧惑高】（4400）
10:58:00 app.api.v1.agent INFO   [Stream] 任务完成: 读取当前章节内容 (0.0s)
10:58:00 app.services.agent.deep_agent.reflection INFO   [Checkpoint] 任务 1 标记了 checkpoint，触发反思
10:58:00 app.services.agent.deep_agent.executor INFO   任务 1 触发反思检查点
10:58:00 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:58:00 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:58:00 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
10:58:01 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:58:03 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
10:58:03 app.services.ai.http_ai_service INFO   流式响应Token统计: 415 (prompt=414, completion=1)
10:58:03 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:58:03 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:58:03 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=415, cost=$0.000527, time=2694ms
10:58:03 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=415
10:58:03 app.services.agent.deep_agent.reflection INFO   [DeepAgent反思] 开始调用 AI，task_id=1
10:58:03 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:58:03 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:58:03 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=500, temp=0.3, task_type=TaskType.SIMPLE_QA
10:58:05 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:58:06 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 92
10:58:06 app.services.ai.http_ai_service INFO   流式响应Token统计: 1152 (prompt=1107, completion=45)
10:58:06 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:58:06 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:58:06 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1152, cost=$0.001834, time=3522ms
10:58:06 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=1152
10:58:06 app.services.agent.deep_agent.reflection INFO   [Reflection] JSON提取成功: needs_replan=False
10:58:06 app.api.v1.agent INFO   [Stream] Task started: 概括章节内容
10:58:06 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
10:58:06 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
10:58:06 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
10:58:09 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:58:31 app.services.ai.http_ai_service INFO   API 响应完成，共接收 28 个数据块，总长度: 2423
10:58:31 app.services.ai.http_ai_service INFO   流式响应Token统计: 8333 (prompt=6561, completion=1772)
10:58:31 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:58:31 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:58:31 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=8333, cost=$0.025921, time=24913ms
10:58:31 app.services.agent.langgraph_tools INFO   ✅ [Agent分析] 分析完成，结果长度: 2423
10:58:31 app.api.v1.agent INFO   [Stream] 任务完成: 概括章节内容 (25.0s)
10:58:31 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:58:31 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:58:31 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
10:58:33 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:58:34 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
10:58:34 app.services.ai.http_ai_service INFO   流式响应Token统计: 581 (prompt=580, completion=1)
10:58:34 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:58:34 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:58:34 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=581, cost=$0.000735, time=2923ms
10:58:34 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=581
10:58:34 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:58:34 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:58:34 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
10:58:36 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:58:37 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
10:58:37 app.services.ai.http_ai_service INFO   流式响应Token统计: 516 (prompt=515, completion=1)
10:58:37 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:58:37 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:58:37 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=516, cost=$0.000654, time=2804ms
10:58:37 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=516
10:58:37 app.services.agent.deep_agent.executor INFO   DeepAgent 执行完成: 任务=2, 反思=1, 重规划=0
10:58:37 app.services.agent.langgraph_agent INFO   [DeepAgent] 执行完成: 反思=1次, 重规划=0次
10:58:37 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共2个任务，耗时: 37.11s
10:58:37 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
10:58:37 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=0, 输出型=1, 展示型=1
10:58:37 app.services.agent.langgraph_agent INFO   [Response] 单个分析任务(analyze_text_tool)，使用AI格式化
10:58:37 app.services.agent.langgraph_agent INFO   [Summarization] 使用AI整合任务结果
10:58:37 app.services.agent.langgraph_agent INFO   [Summarization] 上下文压缩: 原始=7504字符, 压缩后=4078字符, 压缩率=46%
10:58:37 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
10:58:37 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
10:58:37 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
10:58:39 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:58:53 app.services.ai.http_ai_service INFO   API 响应完成，共接收 19 个数据块，总长度: 1633
10:58:53 app.services.ai.http_ai_service INFO   流式响应Token统计: 6234 (prompt=5014, completion=1220)
10:58:53 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
10:58:53 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:58:53 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=6234, cost=$0.018467, time=15396ms
10:58:53 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=6234
10:58:54 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 隔离=work:07251ab5-98b3-4df7-b5f2-2bdb75201d18 | 重要度=0.92
10:58:54 app.services.context.store INFO   [ContextStore] 保存上下文: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:4e349d4e-2da0-4d4a-a167-8e6f5ac29981, token=913
10:58:54 app.services.context.manager INFO   [ContextManager] 更新上下文: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:4e349d4e-2da0-4d4a-a167-8e6f5ac29981, 消息数=2, Token=913
10:58:54 app.services.agent.langgraph_agent INFO   [Planning] 已保存对话到 ContextManager (session=602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:4e349d4e-2da0-4d4a-a167-8e6f5ac29981)
10:58:54 app.api.v1.agent INFO   [Stream] 跳过最终响应（内容已流式发送）
10:58:54 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed
11:00:44 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
11:00:44 app.services.ai.http_ai_service INFO   ModelSelector 已启用
11:00:44 app.services.ai.http_ai_service INFO   AILogService 已启用 (用于成本追踪)
11:00:47 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
11:00:47 app.api.v1.agent INFO   [Chat Stream] Mode: planning
11:00:47 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:49725 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
11:00:47 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: planning, Message: 九龙拉棺是什么？出现在哪里？...
11:00:47 app.api.v1.agent INFO   [agent_chat_stream] 📥 收到的 context 字段:
11:00:47 app.api.v1.agent INFO     - selected_text: N/A...
11:00:47 app.api.v1.agent INFO     - selection_position: N/A
11:00:47 app.api.v1.agent INFO     - chapter_context: 当前章节ID: d2063c51-2364-4b9e-816c-3696cf98c28d...
11:00:47 app.api.v1.agent INFO     - instruction_context: N/A...
11:00:47 app.services.agent.langgraph_agent INFO   [Planning] 使用隔离的thread_id: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:4e349d4e-2da0-4d4a-a167-8e6f5ac29981 (user_id=602f5147-846a-4cde-95d3-405fa75f133f, work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18, conversation_id=4e349d4e-2da0-4d4a-a167-8e6f5ac29981)
11:00:47 app.services.context.store INFO   [ContextStore] 加载上下文: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:4e349d4e-2da0-4d4a-a167-8e6f5ac29981, 2条消息
11:00:47 app.services.context.manager INFO   [ContextManager] Session 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:4e349d4e-2da0-4d4a-a167-8e6f5ac29981: 913/16000 tokens
11:00:47 app.services.context.vector_memory_store INFO   🔍 检索记忆 | 查询='九龙拉棺是什么？出现在哪里？...' | 隔离键=['user:602f5147-846a-4cde-95d3-405fa75f133f:work:07251ab5-98b3-4df7-b5f2-2bdb75201d18', 'user:602f5147-846a-4cde-95d3-405fa75f133f'] | 找到=3条
11:00:47 app.services.context.manager INFO   🔍 检索长期记忆 | 级别=work | work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18 | 含用户级=True | 找到=3条
11:00:47 app.services.context.monitoring_integration INFO   [Monitor] 上下文构建: 3条消息, 913 tokens, 耗时 263.72ms
11:00:47 app.services.agent.langgraph_agent INFO   [Planning] 从 ContextManager 加载了 3 条历史消息 (token: 913)
11:00:47 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: 九龙拉棺是什么？出现在哪里？...
11:00:47 app.core.cache INFO   ✅ 缓存命中: prompt:planning_agent:v2.9.1:get_planning_agent_mode_prompt:fca6eb91156619d0
11:00:47 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
11:00:47 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
11:00:47 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=1200, temp=0.3, task_type=TaskType.SIMPLE_QA
11:00:49 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:00:52 app.services.ai.http_ai_service INFO   API 响应完成，共接收 6 个数据块，总长度: 809
11:00:52 app.services.ai.http_ai_service INFO   流式响应Token统计: 6724 (prompt=6343, completion=381)
11:00:52 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
11:00:52 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
11:00:52 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=6724, cost=$0.011739, time=5259ms
11:00:52 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=6724
11:00:52 app.services.agent.langgraph_agent INFO   [JSON解析] 方法2成功: 从```json块提取
11:00:52 app.services.agent.langgraph_agent INFO   [Planning] 思维链: 输出=用户想了解“九龙拉棺”这个概念是什么，以及它在故事中出现的情, 原料=需要检索作品中所有关于“九龙拉棺”的内容, 处理=使用 search_analysis_f
11:00:52 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共2个任务，耗时: 5.35s
11:00:52 app.api.v1.agent INFO   [Stream] Plan tasks: 2 items
11:00:52 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
11:00:52 app.services.agent.langgraph_agent INFO   [DeepAgent] 启用反思模式
11:00:52 app.services.agent.parameter_resolver INFO   [ParameterResolver] 初始化完成, 严格模式: False
11:00:52 app.services.agent.langgraph_agent INFO   [DeepAgent] ParameterResolver 已启用
11:00:52 app.services.agent.deep_agent.executor INFO   DeepAgent 开始执行，共 2 个任务，反思功能已启用
11:00:52 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] AI 推断功能已启用
11:00:52 app.api.v1.agent INFO   [Stream] Task started: 搜索作品中关于“九龙拉棺”的所有相关片段
11:00:52 app.services.chapter_vector_service INFO   RAG retrieve work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18, current_order=7, query=九龙拉棺...
11:00:52 app.services.chapter_vector_service INFO   RAG retrieved 10 segments within order<=9
11:00:53 app.services.agent.langgraph_tools INFO   [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
11:00:53 app.api.v1.agent INFO   [Stream] 任务完成: 搜索作品中关于“九龙拉棺”的所有相关片段 (0.3s)
11:00:53 app.services.agent.deep_agent.reflection INFO   [Checkpoint] 任务 1 标记了 checkpoint，触发反思
11:00:53 app.services.agent.deep_agent.executor INFO   任务 1 触发反思检查点
11:00:53 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
11:00:53 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
11:00:53 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
11:00:54 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:00:56 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
11:00:56 app.services.ai.http_ai_service INFO   流式响应Token统计: 463 (prompt=462, completion=1)
11:00:56 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
11:00:56 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
11:00:56 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=463, cost=$0.000588, time=3384ms
11:00:56 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=463
11:00:56 app.services.agent.deep_agent.reflection INFO   [DeepAgent反思] 开始调用 AI，task_id=1
11:00:56 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
11:00:56 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
11:00:56 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=500, temp=0.3, task_type=TaskType.SIMPLE_QA
11:00:58 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:01:00 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 122
11:01:00 app.services.ai.http_ai_service INFO   流式响应Token统计: 1362 (prompt=1300, completion=62)
11:01:00 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
11:01:00 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
11:01:00 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1362, cost=$0.002245, time=4135ms
11:01:00 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=1362
11:01:00 app.services.agent.deep_agent.reflection INFO   [Reflection] JSON提取成功: needs_replan=True
11:01:00 app.services.agent.deep_agent.executor INFO   [Reflection] 前置任务不触发重规划（已有后续输出任务）
11:01:00 app.api.v1.agent INFO   [Stream] Task started: 根据搜索结果，解释“九龙拉棺”的含义和出现情境
11:01:00 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
11:01:00 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
11:01:00 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
11:01:02 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:01:16 app.services.ai.http_ai_service INFO   API 响应完成，共接收 19 个数据块，总长度: 1625
11:01:16 app.services.ai.http_ai_service INFO   流式响应Token统计: 5538 (prompt=4326, completion=1212)
11:01:16 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
11:01:16 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
11:01:16 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=5538, cost=$0.017527, time=16161ms
11:01:16 app.services.agent.langgraph_tools INFO   ✅ [Agent分析] 分析完成，结果长度: 1625
11:01:16 app.api.v1.agent INFO   [Stream] 任务完成: 根据搜索结果，解释“九龙拉棺”的含义和出现情境 (16.2s)
11:01:16 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
11:01:16 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
11:01:16 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
11:01:18 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:01:20 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
11:01:20 app.services.ai.http_ai_service INFO   流式响应Token统计: 549 (prompt=548, completion=1)
11:01:20 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
11:01:20 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
11:01:20 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=549, cost=$0.000695, time=3353ms
11:01:20 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=549
11:01:20 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
11:01:20 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
11:01:20 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
11:01:21 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:01:22 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
11:01:22 app.services.ai.http_ai_service INFO   流式响应Token统计: 338 (prompt=337, completion=1)
11:01:22 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
11:01:22 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
11:01:22 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=338, cost=$0.000431, time=2201ms
11:01:22 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=338
11:01:22 app.services.agent.deep_agent.executor INFO   DeepAgent 执行完成: 任务=2, 反思=1, 重规划=0
11:01:22 app.services.agent.langgraph_agent INFO   [DeepAgent] 执行完成: 反思=1次, 重规划=0次
11:01:22 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共2个任务，耗时: 29.72s
11:01:22 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
11:01:22 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=1, 输出型=1, 展示型=0
11:01:22 app.services.agent.langgraph_agent INFO   [Response] 单个分析任务(analyze_text_tool)，使用AI格式化
11:01:22 app.services.agent.langgraph_agent INFO   [Summarization] 使用AI整合任务结果
11:01:22 app.services.agent.langgraph_agent INFO   [Summarization] 上下文压缩: 原始=5011字符, 压缩后=1767字符, 压缩率=65%
11:01:22 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
11:01:22 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
11:01:22 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
11:01:26 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:01:27 app.services.ai.http_ai_service INFO   API 响应完成，共接收 5 个数据块，总长度: 430
11:01:27 app.services.ai.http_ai_service INFO   流式响应Token统计: 2437 (prompt=2112, completion=325)
11:01:27 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
11:01:27 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
11:01:27 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2437, cost=$0.005890, time=5433ms
11:01:27 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=2437
11:01:28 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 隔离=work:07251ab5-98b3-4df7-b5f2-2bdb75201d18 | 重要度=0.60
11:01:28 app.services.context.store INFO   [ContextStore] 保存上下文: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:4e349d4e-2da0-4d4a-a167-8e6f5ac29981, token=1172
11:01:28 app.services.context.manager INFO   [ContextManager] 更新上下文: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:4e349d4e-2da0-4d4a-a167-8e6f5ac29981, 消息数=4, Token=1172
11:01:28 app.services.agent.langgraph_agent INFO   [Planning] 已保存对话到 ContextManager (session=602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:4e349d4e-2da0-4d4a-a167-8e6f5ac29981)
11:01:28 app.api.v1.agent INFO   [Stream] 跳过最终响应（内容已流式发送）
11:01:28 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed
11:02:49 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
11:02:49 app.services.ai.http_ai_service INFO   ModelSelector 已启用
11:02:49 app.services.ai.http_ai_service INFO   AILogService 已启用 (用于成本追踪)
11:02:50 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
11:02:50 app.api.v1.agent INFO   [Chat Stream] Mode: planning
11:02:50 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:60259 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
11:02:50 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: planning, Message: 遮天三部曲包括哪些？...
11:02:50 app.api.v1.agent INFO   [agent_chat_stream] 📥 收到的 context 字段:
11:02:50 app.api.v1.agent INFO     - selected_text: N/A...
11:02:50 app.api.v1.agent INFO     - selection_position: N/A
11:02:50 app.api.v1.agent INFO     - chapter_context: 当前章节ID: d2063c51-2364-4b9e-816c-3696cf98c28d...
11:02:50 app.api.v1.agent INFO     - instruction_context: N/A...
11:02:50 app.services.agent.langgraph_agent INFO   [Planning] 使用隔离的thread_id: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:4e349d4e-2da0-4d4a-a167-8e6f5ac29981 (user_id=602f5147-846a-4cde-95d3-405fa75f133f, work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18, conversation_id=4e349d4e-2da0-4d4a-a167-8e6f5ac29981)
11:02:50 app.services.context.store INFO   [ContextStore] 加载上下文: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:4e349d4e-2da0-4d4a-a167-8e6f5ac29981, 4条消息
11:02:50 app.services.context.manager INFO   [ContextManager] Session 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:4e349d4e-2da0-4d4a-a167-8e6f5ac29981: 1172/16000 tokens
11:02:51 app.services.context.vector_memory_store INFO   🔍 检索记忆 | 查询='遮天三部曲包括哪些？...' | 隔离键=['user:602f5147-846a-4cde-95d3-405fa75f133f:work:07251ab5-98b3-4df7-b5f2-2bdb75201d18', 'user:602f5147-846a-4cde-95d3-405fa75f133f'] | 找到=3条
11:02:51 app.services.context.manager INFO   🔍 检索长期记忆 | 级别=work | work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18 | 含用户级=True | 找到=3条
11:02:51 app.services.context.monitoring_integration INFO   [Monitor] 上下文构建: 5条消息, 1172 tokens, 耗时 339.03ms
11:02:51 app.services.agent.langgraph_agent INFO   [Planning] 从 ContextManager 加载了 5 条历史消息 (token: 1172)
11:02:51 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: 遮天三部曲包括哪些？...
11:02:51 app.core.cache INFO   ✅ 缓存命中: prompt:planning_agent:v2.9.1:get_planning_agent_mode_prompt:fca6eb91156619d0
11:02:51 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
11:02:51 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
11:02:51 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=1200, temp=0.3, task_type=TaskType.SIMPLE_QA
11:02:53 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:03:00 app.services.ai.http_ai_service INFO   API 响应完成，共接收 5 个数据块，总长度: 736
11:03:00 app.services.ai.http_ai_service INFO   流式响应Token统计: 8856 (prompt=8536, completion=320)
11:03:00 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
11:03:00 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
11:03:00 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=8856, cost=$0.013870, time=9265ms
11:03:00 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=8856
11:03:00 app.services.agent.langgraph_agent INFO   [JSON解析] 方法2成功: 从```json块提取
11:03:00 app.services.agent.langgraph_agent INFO   [Planning] 思维链: 输出=用户期望看到一个列表或描述，说明‘遮天三部曲’包含哪些作品。, 原料=需要作品的上下文信息，以确定‘遮天三部曲, 处理=使用 get_context_tool
11:03:00 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共2个任务，耗时: 9.35s
11:03:00 app.api.v1.agent INFO   [Stream] Plan tasks: 2 items
11:03:00 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
11:03:00 app.services.agent.langgraph_agent INFO   [DeepAgent] 启用反思模式
11:03:00 app.services.agent.parameter_resolver INFO   [ParameterResolver] 初始化完成, 严格模式: False
11:03:00 app.services.agent.langgraph_agent INFO   [DeepAgent] ParameterResolver 已启用
11:03:00 app.services.agent.deep_agent.executor INFO   DeepAgent 开始执行，共 2 个任务，反思功能已启用
11:03:00 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] AI 推断功能已启用
11:03:00 app.api.v1.agent INFO   [Stream] Task started: 获取作品上下文信息，查找遮天三部曲的其他组成部分。
11:03:00 app.services.chapter_vector_service INFO   RAG retrieve work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18, current_order=7, query=作品背景、人物关系、情节发展、伏笔线索...
11:03:00 app.services.chapter_vector_service INFO   RAG retrieved 5 segments within order<=7
11:03:00 app.services.agent.langgraph_tools INFO   [get_context_tool] ✅ 获取上下文成功
11:03:00 app.api.v1.agent INFO   [Stream] 任务完成: 获取作品上下文信息，查找遮天三部曲的其他组成部分。 (0.3s)
11:03:00 app.services.agent.deep_agent.reflection INFO   [Checkpoint] 任务 1 标记了 checkpoint，触发反思
11:03:00 app.services.agent.deep_agent.executor INFO   任务 1 触发反思检查点
11:03:01 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
11:03:01 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
11:03:01 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
11:03:03 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:03:04 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
11:03:04 app.services.ai.http_ai_service INFO   流式响应Token统计: 480 (prompt=479, completion=1)
11:03:04 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
11:03:04 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
11:03:04 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=480, cost=$0.000609, time=3802ms
11:03:04 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=480
11:03:04 app.services.agent.deep_agent.reflection INFO   [DeepAgent反思] 开始调用 AI，task_id=1
11:03:04 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
11:03:04 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
11:03:04 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=500, temp=0.3, task_type=TaskType.SIMPLE_QA
11:03:06 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:03:11 app.services.ai.http_ai_service INFO   API 响应完成，共接收 2 个数据块，总长度: 190
11:03:11 app.services.ai.http_ai_service INFO   流式响应Token统计: 1769 (prompt=1649, completion=120)
11:03:11 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
11:03:11 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
11:03:11 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1769, cost=$0.003261, time=7104ms
11:03:11 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=1769
11:03:11 app.services.agent.deep_agent.reflection INFO   [Reflection] JSON提取成功: needs_replan=True
11:03:11 app.services.agent.deep_agent.executor INFO   [Reflection] 前置任务不触发重规划（已有后续输出任务）
11:03:11 app.api.v1.agent INFO   [Stream] Task started: 根据获取的上下文信息，整理并列出遮天三部曲的作品。
11:03:11 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
11:03:11 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
11:03:11 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
11:03:14 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:03:35 app.services.ai.http_ai_service INFO   API 响应完成，共接收 21 个数据块，总长度: 1865
11:03:35 app.services.ai.http_ai_service INFO   流式响应Token统计: 7616 (prompt=6265, completion=1351)
11:03:35 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
11:03:36 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
11:03:36 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=7616, cost=$0.021341, time=23798ms
11:03:36 app.services.agent.langgraph_tools INFO   ✅ [Agent分析] 分析完成，结果长度: 1865
11:03:36 app.api.v1.agent INFO   [Stream] 任务完成: 根据获取的上下文信息，整理并列出遮天三部曲的作品。 (24.2s)
11:03:36 app.services.agent.deep_agent.reflection INFO   [Checkpoint] 任务 2 标记了 checkpoint，触发反思
11:03:36 app.services.agent.deep_agent.executor INFO   任务 2 触发反思检查点
11:03:36 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
11:03:36 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
11:03:36 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
11:03:38 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:03:40 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
11:03:40 app.services.ai.http_ai_service INFO   流式响应Token统计: 468 (prompt=467, completion=1)
11:03:40 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
11:03:41 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
11:03:41 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=468, cost=$0.000594, time=4446ms
11:03:41 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=468
11:03:41 app.services.agent.deep_agent.reflection INFO   [DeepAgent反思] 开始调用 AI，task_id=2
11:03:41 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
11:03:41 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
11:03:41 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=500, temp=0.3, task_type=TaskType.SIMPLE_QA
11:03:42 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:03:49 app.services.ai.http_ai_service INFO   API 响应完成，共接收 2 个数据块，总长度: 128
11:03:49 app.services.ai.http_ai_service INFO   流式响应Token统计: 2215 (prompt=2147, completion=68)
11:03:49 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
11:03:49 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
11:03:49 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2215, cost=$0.003364, time=8353ms
11:03:49 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=2215
11:03:49 app.services.agent.deep_agent.reflection INFO   [Reflection] JSON提取成功: needs_replan=True
11:03:49 app.services.agent.deep_agent.executor INFO   反思结果需要重规划 (第 1 次)
11:03:49 app.services.agent.deep_agent.executor INFO   [DeepAgent重规划] 开始调用 AI
11:03:49 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
11:03:49 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
11:03:49 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=800, temp=0.2, task_type=TaskType.SIMPLE_QA
11:03:51 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:03:57 app.services.ai.http_ai_service INFO   API 响应完成，共接收 2 个数据块，总长度: 151
11:03:57 app.services.ai.http_ai_service INFO   流式响应Token统计: 1704 (prompt=1631, completion=73)
11:03:57 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
11:03:57 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
11:03:57 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1704, cost=$0.002769, time=8138ms
11:03:57 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=1704
11:03:57 app.services.agent.deep_agent.executor INFO   [DeepAgent重规划] 成功生成 2 个新任务
11:03:57 app.api.v1.agent INFO   [Stream] Plan tasks: 4 items
11:03:57 app.services.agent.deep_agent.executor INFO   计划已更新，新任务数: 2
11:03:57 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
11:03:57 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
11:03:57 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=200, temp=0.1, task_type=TaskType.SIMPLE_QA
11:03:59 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:04:00 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 101
11:04:00 app.services.ai.http_ai_service INFO   流式响应Token统计: 699 (prompt=650, completion=49)
11:04:00 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
11:04:00 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
11:04:00 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=699, cost=$0.001302, time=3162ms
11:04:00 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=699
11:04:00 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] AI 推断成功: '查找并确认构成“遮天三部曲”的作品列表。...' → tool=get_context_tool
11:04:00 app.api.v1.agent INFO   [Stream] Task started: 查找并确认构成“遮天三部曲”的作品列表。
11:04:01 app.services.chapter_vector_service INFO   RAG retrieve work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18, current_order=7, query=作品背景、人物关系、情节发展、伏笔线索...
11:04:01 app.services.chapter_vector_service INFO   RAG retrieved 5 segments within order<=7
11:04:01 app.services.agent.langgraph_tools INFO   [get_context_tool] ✅ 获取上下文成功
11:04:01 app.api.v1.agent INFO   [Stream] 任务完成: 查找并确认构成“遮天三部曲”的作品列表。 (0.2s)
11:04:01 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
11:04:01 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
11:04:01 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=200, temp=0.1, task_type=TaskType.SIMPLE_QA
11:04:02 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:04:05 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 117
11:04:05 app.services.ai.http_ai_service INFO   流式响应Token统计: 1148 (prompt=1091, completion=57)
11:04:05 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
11:04:05 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
11:04:05 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1148, cost=$0.001934, time=4273ms
11:04:05 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=1148
11:04:05 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] AI 推断成功: '根据查找结果，清晰列出“遮天三部曲”包含的所有作品。...' → tool=get_context_tool
11:04:05 app.api.v1.agent INFO   [Stream] Task started: 根据查找结果，清晰列出“遮天三部曲”包含的所有作品。
11:04:05 app.services.chapter_vector_service INFO   RAG retrieve work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18, current_order=7, query=作品背景、人物关系、情节发展、伏笔线索...
11:04:05 app.services.chapter_vector_service INFO   RAG retrieved 5 segments within order<=7
11:04:05 app.services.agent.langgraph_tools INFO   [get_context_tool] ✅ 获取上下文成功
11:04:05 app.api.v1.agent INFO   [Stream] 任务完成: 根据查找结果，清晰列出“遮天三部曲”包含的所有作品。 (0.3s)
11:04:05 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
11:04:05 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
11:04:05 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
11:04:08 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:04:10 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
11:04:10 app.services.ai.http_ai_service INFO   流式响应Token统计: 552 (prompt=551, completion=1)
11:04:10 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
11:04:10 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
11:04:10 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=552, cost=$0.000699, time=4423ms
11:04:10 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=552
11:04:10 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
11:04:10 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
11:04:10 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
11:04:11 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:04:13 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
11:04:13 app.services.ai.http_ai_service INFO   流式响应Token统计: 547 (prompt=546, completion=1)
11:04:13 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
11:04:13 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
11:04:13 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=547, cost=$0.000693, time=3265ms
11:04:13 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=547
11:04:13 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
11:04:13 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
11:04:13 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
11:04:15 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:04:19 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
11:04:19 app.services.ai.http_ai_service INFO   流式响应Token统计: 937 (prompt=936, completion=1)
11:04:19 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
11:04:19 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
11:04:19 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=937, cost=$0.001180, time=5532ms
11:04:19 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=937
11:04:19 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
11:04:19 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
11:04:19 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
11:04:21 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:04:23 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
11:04:23 app.services.ai.http_ai_service INFO   流式响应Token统计: 650 (prompt=649, completion=1)
11:04:23 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
11:04:23 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
11:04:23 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=650, cost=$0.000821, time=4365ms
11:04:23 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=650
11:04:23 app.services.agent.deep_agent.executor INFO   DeepAgent 执行完成: 任务=4, 反思=2, 重规划=1
11:04:23 app.services.agent.langgraph_agent INFO   [DeepAgent] 执行完成: 反思=2次, 重规划=1次
11:04:23 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共4个任务，耗时: 82.89s
11:04:23 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
11:04:23 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=3, 输出型=1, 展示型=0
11:04:23 app.services.agent.langgraph_agent INFO   [Response] 单个分析任务(analyze_text_tool)，使用AI格式化
11:04:23 app.services.agent.langgraph_agent INFO   [Summarization] 使用AI整合任务结果
11:04:23 app.services.agent.langgraph_agent INFO   [Summarization] 上下文压缩: 原始=15022字符, 压缩后=3994字符, 压缩率=74%
11:04:23 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
11:04:23 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
11:04:23 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
11:04:25 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:04:28 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 96
11:04:28 app.services.ai.http_ai_service INFO   流式响应Token统计: 3811 (prompt=3750, completion=61)
11:04:28 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
11:04:28 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
11:04:28 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=3811, cost=$0.005298, time=5108ms
11:04:28 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=3811
11:04:28 app.services.context.store INFO   [ContextStore] 保存上下文: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:4e349d4e-2da0-4d4a-a167-8e6f5ac29981, token=1235
11:04:28 app.services.context.manager INFO   [ContextManager] 更新上下文: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:4e349d4e-2da0-4d4a-a167-8e6f5ac29981, 消息数=6, Token=1235
11:04:28 app.services.agent.langgraph_agent INFO   [Planning] 已保存对话到 ContextManager (session=602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:4e349d4e-2da0-4d4a-a167-8e6f5ac29981)
11:04:28 app.api.v1.agent INFO   [Stream] 跳过最终响应（内容已流式发送）
11:04:28 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed
11:04:55 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
11:04:55 app.services.ai.http_ai_service INFO   ModelSelector 已启用
11:04:55 app.services.ai.http_ai_service INFO   AILogService 已启用 (用于成本追踪)
11:04:57 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
11:04:57 app.api.v1.agent INFO   [Chat Stream] Mode: planning
11:04:57 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:50152 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
11:04:57 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: planning, Message: 仙王境界有什么能力？...
11:04:57 app.api.v1.agent INFO   [agent_chat_stream] 📥 收到的 context 字段:
11:04:57 app.api.v1.agent INFO     - selected_text: N/A...
11:04:57 app.api.v1.agent INFO     - selection_position: N/A
11:04:57 app.api.v1.agent INFO     - chapter_context: 当前章节ID: d2063c51-2364-4b9e-816c-3696cf98c28d...
11:04:57 app.api.v1.agent INFO     - instruction_context: N/A...
11:04:57 app.services.agent.langgraph_agent INFO   [Planning] 使用隔离的thread_id: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:4e349d4e-2da0-4d4a-a167-8e6f5ac29981 (user_id=602f5147-846a-4cde-95d3-405fa75f133f, work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18, conversation_id=4e349d4e-2da0-4d4a-a167-8e6f5ac29981)
11:04:57 app.services.context.store INFO   [ContextStore] 加载上下文: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:4e349d4e-2da0-4d4a-a167-8e6f5ac29981, 6条消息
11:04:57 app.services.context.manager INFO   [ContextManager] Session 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:4e349d4e-2da0-4d4a-a167-8e6f5ac29981: 1235/16000 tokens
11:04:57 app.services.context.vector_memory_store INFO   🔍 检索记忆 | 查询='仙王境界有什么能力？...' | 隔离键=['user:602f5147-846a-4cde-95d3-405fa75f133f:work:07251ab5-98b3-4df7-b5f2-2bdb75201d18', 'user:602f5147-846a-4cde-95d3-405fa75f133f'] | 找到=3条
11:04:57 app.services.context.manager INFO   🔍 检索长期记忆 | 级别=work | work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18 | 含用户级=True | 找到=3条
11:04:57 app.services.context.monitoring_integration INFO   [Monitor] 上下文构建: 7条消息, 1235 tokens, 耗时 361.79ms
11:04:57 app.services.agent.langgraph_agent INFO   [Planning] 从 ContextManager 加载了 7 条历史消息 (token: 1235)
11:04:57 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: 仙王境界有什么能力？...
11:04:57 app.core.cache INFO   ✅ 缓存命中: prompt:planning_agent:v2.9.1:get_planning_agent_mode_prompt:fca6eb91156619d0
11:04:57 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
11:04:57 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
11:04:57 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=1200, temp=0.3, task_type=TaskType.SIMPLE_QA
11:05:00 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:05:03 app.services.ai.http_ai_service INFO   API 响应完成，共接收 5 个数据块，总长度: 677
11:05:03 app.services.ai.http_ai_service INFO   流式响应Token统计: 7131 (prompt=6836, completion=295)
11:05:03 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
11:05:03 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
11:05:03 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=7131, cost=$0.011495, time=5484ms
11:05:03 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=7131
11:05:03 app.services.agent.langgraph_agent INFO   [JSON解析] 方法1成功: 直接解析
11:05:03 app.services.agent.langgraph_agent INFO   [Planning] 思维链: 输出=用户想了解“仙王境界”的具体能力，期望得到一个分析性的回答，, 原料=需要搜索作品中关于“仙王境界”能力的所有, 处理=首先使用搜索工具查找相关内容，然后使用分
11:05:03 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共2个任务，耗时: 5.56s
11:05:03 app.api.v1.agent INFO   [Stream] Plan tasks: 2 items
11:05:03 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
11:05:03 app.services.agent.langgraph_agent INFO   [DeepAgent] 启用反思模式
11:05:03 app.services.agent.parameter_resolver INFO   [ParameterResolver] 初始化完成, 严格模式: False
11:05:03 app.services.agent.langgraph_agent INFO   [DeepAgent] ParameterResolver 已启用
11:05:03 app.services.agent.deep_agent.executor INFO   DeepAgent 开始执行，共 2 个任务，反思功能已启用
11:05:03 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] AI 推断功能已启用
11:05:03 app.api.v1.agent INFO   [Stream] Task started: 搜索关于“仙王境界”能力的内容
11:05:03 app.services.chapter_vector_service INFO   RAG retrieve work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18, current_order=7, query=仙王境界能力...
11:05:03 app.services.chapter_vector_service INFO   RAG retrieved 10 segments within order<=9
11:05:03 app.services.agent.langgraph_tools INFO   [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
11:05:03 app.api.v1.agent INFO   [Stream] 任务完成: 搜索关于“仙王境界”能力的内容 (0.3s)
11:05:03 app.services.agent.deep_agent.reflection INFO   [Checkpoint] 任务 1 标记了 checkpoint，触发反思
11:05:03 app.services.agent.deep_agent.executor INFO   任务 1 触发反思检查点
11:05:03 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
11:05:03 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
11:05:03 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
11:05:05 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:05:06 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
11:05:06 app.services.ai.http_ai_service INFO   流式响应Token统计: 499 (prompt=498, completion=1)
11:05:06 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
11:05:06 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
11:05:06 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=499, cost=$0.000633, time=3485ms
11:05:06 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=499
11:05:06 app.services.agent.deep_agent.reflection INFO   [DeepAgent反思] 开始调用 AI，task_id=1
11:05:06 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
11:05:06 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
11:05:06 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=500, temp=0.3, task_type=TaskType.SIMPLE_QA
11:05:08 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:05:12 app.services.ai.http_ai_service INFO   API 响应完成，共接收 2 个数据块，总长度: 166
11:05:12 app.services.ai.http_ai_service INFO   流式响应Token统计: 1286 (prompt=1193, completion=93)
11:05:12 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
11:05:12 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
11:05:12 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1286, cost=$0.002421, time=5399ms
11:05:12 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=1286
11:05:12 app.services.agent.deep_agent.reflection INFO   [Reflection] JSON提取成功: needs_replan=True
11:05:12 app.services.agent.deep_agent.executor INFO   [Reflection] 前置任务不触发重规划（已有后续输出任务）
11:05:12 app.api.v1.agent INFO   [Stream] Task started: 分析搜索到的内容，总结仙王境界的能力
11:05:12 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
11:05:12 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
11:05:12 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
11:05:14 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:05:31 app.services.ai.http_ai_service INFO   API 响应完成，共接收 26 个数据块，总长度: 2424
11:05:31 app.services.ai.http_ai_service INFO   流式响应Token统计: 6107 (prompt=4418, completion=1689)
11:05:31 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
11:05:31 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
11:05:31 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=6107, cost=$0.022412, time=19213ms
11:05:31 app.services.agent.langgraph_tools INFO   ✅ [Agent分析] 分析完成，结果长度: 2424
11:05:31 app.api.v1.agent INFO   [Stream] 任务完成: 分析搜索到的内容，总结仙王境界的能力 (19.3s)
11:05:31 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
11:05:31 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
11:05:31 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
11:05:33 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:05:34 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
11:05:34 app.services.ai.http_ai_service INFO   流式响应Token统计: 461 (prompt=460, completion=1)
11:05:34 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
11:05:34 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
11:05:34 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=461, cost=$0.000585, time=3082ms
11:05:34 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=461
11:05:34 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
11:05:34 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
11:05:34 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
11:05:36 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:05:38 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
11:05:38 app.services.ai.http_ai_service INFO   流式响应Token统计: 454 (prompt=453, completion=1)
11:05:38 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
11:05:38 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
11:05:38 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=454, cost=$0.000576, time=3466ms
11:05:38 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=454
11:05:38 app.services.agent.deep_agent.executor INFO   DeepAgent 执行完成: 任务=2, 反思=1, 重规划=0
11:05:38 app.services.agent.langgraph_agent INFO   [DeepAgent] 执行完成: 反思=1次, 重规划=0次
11:05:38 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共2个任务，耗时: 35.20s
11:05:38 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
11:05:38 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=1, 输出型=1, 展示型=0
11:05:38 app.services.agent.langgraph_agent INFO   [Response] 单个分析任务(analyze_text_tool)，使用AI格式化
11:05:38 app.services.agent.langgraph_agent INFO   [Summarization] 使用AI整合任务结果
11:05:38 app.services.agent.langgraph_agent INFO   [Summarization] 上下文压缩: 原始=5939字符, 压缩后=2146字符, 压缩率=64%
11:05:38 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
11:05:38 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
11:05:38 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
11:05:40 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:05:43 app.services.ai.http_ai_service INFO   API 响应完成，共接收 6 个数据块，总长度: 556
11:05:43 app.services.ai.http_ai_service INFO   流式响应Token统计: 2299 (prompt=1941, completion=358)
11:05:43 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
11:05:43 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
11:05:43 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2299, cost=$0.006006, time=4716ms
11:05:43 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=2299
11:05:44 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 隔离=work:07251ab5-98b3-4df7-b5f2-2bdb75201d18 | 重要度=0.73
11:05:44 app.services.context.store INFO   [ContextStore] 保存上下文: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:4e349d4e-2da0-4d4a-a167-8e6f5ac29981, token=1536
11:05:44 app.services.context.manager INFO   [ContextManager] 更新上下文: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:4e349d4e-2da0-4d4a-a167-8e6f5ac29981, 消息数=8, Token=1536
11:05:44 app.services.agent.langgraph_agent INFO   [Planning] 已保存对话到 ContextManager (session=602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:4e349d4e-2da0-4d4a-a167-8e6f5ac29981)
11:05:44 app.api.v1.agent INFO   [Stream] 跳过最终响应（内容已流式发送）
11:05:44 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed
11:06:52 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: 07251ab5-98b3-4df7-b5f2-2bdb75201d18, chapter_id: a4044c3a-34f8-45c0-a992-871db188810d
11:06:52 app.api.v1.ai INFO   [预加载] 当前章节已加载: a4044c3a-34f8-45c0-a992-871db188810d
11:06:52 app.api.v1.ai INFO   [预加载] 前一章节已加载: 0d076ac2-70fc-46ce-92a0-d9dfba43723b
11:06:52 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
11:06:52 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:55986 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
11:06:53 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:62059 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
11:06:53 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: 07251ab5-98b3-4df7-b5f2-2bdb75201d18, chapter_id: a4044c3a-34f8-45c0-a992-871db188810d
11:06:53 app.api.v1.ai INFO   [预加载] 当前章节已加载: a4044c3a-34f8-45c0-a992-871db188810d
11:06:53 app.api.v1.ai INFO   [预加载] 前一章节已加载: 0d076ac2-70fc-46ce-92a0-d9dfba43723b
11:06:53 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
11:06:53 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:62058 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
11:06:54 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:07251ab5-98b3-4df7-b5f2-2bdb75201d18
11:06:54 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/a4044c3a-34f8-45c0-a992-871db188810d
INFO:     127.0.0.1:61180 - "PUT /api/v1/chapters/a4044c3a-34f8-45c0-a992-871db188810d HTTP/1.1" 200 OK
11:06:54 app.services.chapter_vector_service INFO   Vectorizing chapter: 第2章 【躺平的系统】 (order=2)
11:06:55 app.services.chapter_vector_service INFO   Stored chapter vectors: 第2章 【躺平的系统】 (8 chunks)
11:06:55 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:07251ab5-98b3-4df7-b5f2-2bdb75201d18
11:06:55 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/a4044c3a-34f8-45c0-a992-871db188810d
INFO:     127.0.0.1:63133 - "PUT /api/v1/chapters/a4044c3a-34f8-45c0-a992-871db188810d HTTP/1.1" 200 OK
11:06:55 app.services.chapter_vector_service INFO   Vectorizing chapter: 第2章 【躺平的系统】 (order=2)
11:06:56 app.services.chapter_vector_service INFO   Stored chapter vectors: 第2章 【躺平的系统】 (8 chunks)
11:07:02 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:61528 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
11:07:02 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
11:07:02 app.services.ai.http_ai_service INFO   ModelSelector 已启用
11:07:02 app.services.ai.http_ai_service INFO   AILogService 已启用 (用于成本追踪)
11:07:05 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
11:07:05 app.api.v1.agent INFO   [Chat Stream] Mode: planning
11:07:05 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:56248 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
11:07:05 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: planning, Message: 仙王境界有什么能力？...
11:07:05 app.api.v1.agent INFO   [agent_chat_stream] 📥 收到的 context 字段:
11:07:05 app.api.v1.agent INFO     - selected_text: N/A...
11:07:05 app.api.v1.agent INFO     - selection_position: N/A
11:07:05 app.api.v1.agent INFO     - chapter_context: 当前章节ID: a4044c3a-34f8-45c0-a992-871db188810d...
11:07:05 app.api.v1.agent INFO     - instruction_context: N/A...
11:07:05 app.services.agent.langgraph_agent INFO   [Planning] 使用隔离的thread_id: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:798360bd-2759-4752-b699-76b9890c58dd (user_id=602f5147-846a-4cde-95d3-405fa75f133f, work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18, conversation_id=798360bd-2759-4752-b699-76b9890c58dd)
11:07:05 app.services.context.manager INFO   [ContextManager] 创建新上下文: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:798360bd-2759-4752-b699-76b9890c58dd
11:07:05 app.services.context.manager INFO   [ContextManager] Session 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:798360bd-2759-4752-b699-76b9890c58dd: 0/16000 tokens
11:07:05 app.services.context.vector_memory_store INFO   🔍 检索记忆 | 查询='仙王境界有什么能力？...' | 隔离键=['user:602f5147-846a-4cde-95d3-405fa75f133f:work:07251ab5-98b3-4df7-b5f2-2bdb75201d18', 'user:602f5147-846a-4cde-95d3-405fa75f133f'] | 找到=3条
11:07:05 app.services.context.manager INFO   🔍 检索长期记忆 | 级别=work | work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18 | 含用户级=True | 找到=3条
11:07:05 app.services.context.monitoring_integration INFO   [Monitor] 上下文构建: 1条消息, 0 tokens, 耗时 198.97ms
11:07:05 app.services.agent.langgraph_agent INFO   [Planning] 从 ContextManager 加载了 1 条历史消息 (token: 0)
11:07:05 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: 仙王境界有什么能力？...
11:07:05 app.core.cache INFO   ✅ 缓存命中: prompt:planning_agent:v2.9.1:get_planning_agent_mode_prompt:fca6eb91156619d0
11:07:05 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
11:07:05 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
11:07:05 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=1200, temp=0.3, task_type=TaskType.SIMPLE_QA
11:07:08 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:07:11 app.services.ai.http_ai_service INFO   API 响应完成，共接收 5 个数据块，总长度: 691
11:07:11 app.services.ai.http_ai_service INFO   流式响应Token统计: 5519 (prompt=5219, completion=300)
11:07:11 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
11:07:11 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
11:07:11 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=5519, cost=$0.009524, time=5670ms
11:07:11 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=5519
11:07:11 app.services.agent.langgraph_agent INFO   [JSON解析] 方法2成功: 从```json块提取
11:07:11 app.services.agent.langgraph_agent INFO   [Planning] 思维链: 输出=用户想了解“仙王境界”所具备的能力，期望得到一个解释或总结性, 原料=需要搜索作品中关于“仙王境界”的描述和能, 处理=使用搜索工具查找相关内容，然后使用分析工
11:07:11 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共2个任务，耗时: 5.76s
11:07:11 app.api.v1.agent INFO   [Stream] Plan tasks: 2 items
11:07:11 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
11:07:11 app.services.agent.langgraph_agent INFO   [DeepAgent] 启用反思模式
11:07:11 app.services.agent.parameter_resolver INFO   [ParameterResolver] 初始化完成, 严格模式: False
11:07:11 app.services.agent.langgraph_agent INFO   [DeepAgent] ParameterResolver 已启用
11:07:11 app.services.agent.deep_agent.executor INFO   DeepAgent 开始执行，共 2 个任务，反思功能已启用
11:07:11 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] AI 推断功能已启用
11:07:11 app.api.v1.agent INFO   [Stream] Task started: 搜索关于“仙王境界”能力的信息
11:07:11 app.services.chapter_vector_service INFO   RAG retrieve work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18, current_order=2, query=仙王境界的能力...
11:07:11 app.services.chapter_vector_service INFO   RAG retrieved 10 segments within order<=4
11:07:11 app.services.agent.langgraph_tools INFO   [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
11:07:11 app.api.v1.agent INFO   [Stream] 任务完成: 搜索关于“仙王境界”能力的信息 (0.3s)
11:07:11 app.services.agent.deep_agent.reflection INFO   [Checkpoint] 任务 1 标记了 checkpoint，触发反思
11:07:11 app.services.agent.deep_agent.executor INFO   任务 1 触发反思检查点
11:07:11 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
11:07:11 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
11:07:11 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
11:07:13 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:07:14 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
11:07:14 app.services.ai.http_ai_service INFO   流式响应Token统计: 373 (prompt=372, completion=1)
11:07:14 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
11:07:14 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
11:07:14 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=373, cost=$0.000475, time=2655ms
11:07:14 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=373
11:07:14 app.services.agent.deep_agent.reflection INFO   [DeepAgent反思] 开始调用 AI，task_id=1
11:07:14 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
11:07:14 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
11:07:14 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=500, temp=0.3, task_type=TaskType.SIMPLE_QA
11:07:18 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:07:21 app.services.ai.http_ai_service INFO   API 响应完成，共接收 2 个数据块，总长度: 131
11:07:21 app.services.ai.http_ai_service INFO   流式响应Token统计: 1263 (prompt=1197, completion=66)
11:07:21 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
11:07:21 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
11:07:21 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1263, cost=$0.002156, time=7096ms
11:07:21 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=1263
11:07:21 app.services.agent.deep_agent.reflection INFO   [Reflection] JSON提取成功: needs_replan=True
11:07:21 app.services.agent.deep_agent.executor INFO   [Reflection] 前置任务不触发重规划（已有后续输出任务）
11:07:21 app.api.v1.agent INFO   [Stream] Task started: 分析搜索结果，总结仙王境界的能力
11:07:21 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
11:07:21 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
11:07:21 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
11:07:23 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:07:44 app.services.ai.http_ai_service INFO   API 响应完成，共接收 23 个数据块，总长度: 1989
11:07:44 app.services.ai.http_ai_service INFO   流式响应Token统计: 7027 (prompt=5565, completion=1462)
11:07:44 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
11:07:44 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
11:07:44 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=7027, cost=$0.021576, time=23500ms
11:07:44 app.services.agent.langgraph_tools INFO   ✅ [Agent分析] 分析完成，结果长度: 1989
11:07:44 app.api.v1.agent INFO   [Stream] 任务完成: 分析搜索结果，总结仙王境界的能力 (23.6s)
11:07:44 app.services.agent.deep_agent.reflection INFO   [Checkpoint] 任务 2 标记了 checkpoint，触发反思
11:07:44 app.services.agent.deep_agent.executor INFO   任务 2 触发反思检查点
11:07:44 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
11:07:44 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
11:07:44 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
11:07:46 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:07:48 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
11:07:48 app.services.ai.http_ai_service INFO   流式响应Token统计: 446 (prompt=445, completion=1)
11:07:48 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
11:07:48 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
11:07:48 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=446, cost=$0.000566, time=3442ms
11:07:48 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=446
11:07:48 app.services.agent.deep_agent.reflection INFO   [DeepAgent反思] 开始调用 AI，task_id=2
11:07:48 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
11:07:48 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
11:07:48 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=500, temp=0.3, task_type=TaskType.SIMPLE_QA
11:07:50 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:07:54 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 115
11:07:54 app.services.ai.http_ai_service INFO   流式响应Token统计: 1369 (prompt=1313, completion=56)
11:07:54 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
11:07:54 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
11:07:54 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1369, cost=$0.002201, time=6027ms
11:07:54 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=1369
11:07:54 app.services.agent.deep_agent.reflection INFO   [Reflection] JSON提取成功: needs_replan=True
11:07:54 app.services.agent.deep_agent.executor INFO   反思结果需要重规划 (第 1 次)
11:07:54 app.services.agent.deep_agent.executor INFO   [DeepAgent重规划] 开始调用 AI
11:07:54 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
11:07:54 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
11:07:54 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=800, temp=0.2, task_type=TaskType.SIMPLE_QA
11:07:56 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:08:01 app.services.ai.http_ai_service INFO   API 响应完成，共接收 3 个数据块，总长度: 292
11:08:01 app.services.ai.http_ai_service INFO   流式响应Token统计: 1803 (prompt=1664, completion=139)
11:08:01 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
11:08:01 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
11:08:01 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1803, cost=$0.003470, time=7342ms
11:08:01 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=1803
11:08:01 app.services.agent.deep_agent.executor INFO   [DeepAgent重规划] 成功生成 4 个新任务
11:08:01 app.api.v1.agent INFO   [Stream] Plan tasks: 6 items
11:08:01 app.services.agent.deep_agent.executor INFO   计划已更新，新任务数: 4
11:08:01 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
11:08:01 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
11:08:01 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=200, temp=0.1, task_type=TaskType.SIMPLE_QA
11:08:03 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:08:05 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 117
11:08:05 app.services.ai.http_ai_service INFO   流式响应Token统计: 844 (prompt=790, completion=54)
11:08:05 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
11:08:05 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
11:08:05 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=844, cost=$0.001528, time=3144ms
11:08:05 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=844
11:08:05 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] AI 推断成功: '[已完成] 搜索关于“仙王境界”的具体能力信息。...' → tool=get_context_tool
11:08:05 app.api.v1.agent INFO   [Stream] Task started: [已完成] 搜索关于“仙王境界”的具体能力信息。
11:08:05 app.services.chapter_vector_service INFO   RAG retrieve work_id=07251ab5-98b3-4df7-b5f2-2bdb75201d18, current_order=2, query=作品背景、人物关系、情节发展、伏笔线索...
11:08:05 app.services.chapter_vector_service INFO   RAG retrieved 3 segments within order<=2
11:08:05 app.services.agent.langgraph_tools INFO   [get_context_tool] ✅ 获取上下文成功
11:08:05 app.api.v1.agent INFO   [Stream] 任务完成: [已完成] 搜索关于“仙王境界”的具体能力信息。 (0.1s)
11:08:05 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
11:08:05 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
11:08:05 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=200, temp=0.1, task_type=TaskType.SIMPLE_QA
11:08:07 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:08:08 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 120
11:08:08 app.services.ai.http_ai_service INFO   流式响应Token统计: 889 (prompt=836, completion=53)
11:08:08 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
11:08:08 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
11:08:08 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=889, cost=$0.001575, time=3611ms
11:08:08 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=889
11:08:08 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] 从 3 个任务结果中提取文本，总长度: 8550 字符
11:08:08 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] AI 推断成功: '[调整] 深入分析搜索结果，重点提炼仙王境界的各项具体能力。...' → tool=analyze_text_tool
11:08:08 app.api.v1.agent INFO   [Stream] Task started: [调整] 深入分析搜索结果，重点提炼仙王境界的各项具体能力。
11:08:08 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
11:08:08 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
11:08:08 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
11:08:10 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:08:42 app.services.ai.http_ai_service INFO   API 响应完成，共接收 27 个数据块，总长度: 2366
11:08:42 app.services.ai.http_ai_service INFO   流式响应Token统计: 14152 (prompt=12407, completion=1745)
11:08:42 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
11:08:42 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
11:08:42 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=14152, cost=$0.032959, time=34087ms
11:08:42 app.services.agent.langgraph_tools INFO   ✅ [Agent分析] 分析完成，结果长度: 2366
11:08:42 app.api.v1.agent INFO   [Stream] 任务完成: [调整] 深入分析搜索结果，重点提炼仙王境界的各项具体能力。 (34.2s)
11:08:42 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
11:08:42 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
11:08:42 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=200, temp=0.1, task_type=TaskType.SIMPLE_QA
11:08:44 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:08:46 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 122
11:08:46 app.services.ai.http_ai_service INFO   流式响应Token统计: 849 (prompt=792, completion=57)
11:08:46 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
11:08:46 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
11:08:46 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=849, cost=$0.001560, time=3297ms
11:08:46 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=849
11:08:46 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] 从 4 个任务结果中提取文本，总长度: 10918 字符
11:08:46 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] AI 推断成功: '[新增] 详细阐述已提炼出的仙王境界能力，解释其含义和表现形...' → tool=analyze_text_tool
11:08:46 app.api.v1.agent INFO   [Stream] Task started: [新增] 详细阐述已提炼出的仙王境界能力，解释其含义和表现形式。
11:08:46 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
11:08:46 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
11:08:46 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
11:08:48 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:09:04 app.services.ai.http_ai_service INFO   API 响应完成，共接收 38 个数据块，总长度: 2426
11:09:04 app.services.ai.http_ai_service INFO   流式响应Token统计: 12732 (prompt=10954, completion=1778)
11:09:04 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
11:09:04 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
11:09:04 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=12732, cost=$0.031473, time=18023ms
11:09:04 app.services.agent.langgraph_tools INFO   ✅ [Agent分析] 分析完成，结果长度: 2426
11:09:04 app.api.v1.agent INFO   [Stream] 任务完成: [新增] 详细阐述已提炼出的仙王境界能力，解释其含义和表现形式。 (18.1s)
11:09:04 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
11:09:04 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
11:09:04 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=200, temp=0.1, task_type=TaskType.SIMPLE_QA
11:09:05 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:09:07 app.services.ai.http_ai_service INFO   API 响应完成，共接收 2 个数据块，总长度: 165
11:09:07 app.services.ai.http_ai_service INFO   流式响应Token统计: 922 (prompt=844, completion=78)
11:09:07 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
11:09:07 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
11:09:07 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=922, cost=$0.001835, time=3314ms
11:09:07 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=922
11:09:07 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] 从 4 个任务结果中提取文本，总长度: 9955 字符
11:09:07 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] AI 推断成功: '[新增] 整合信息，生成对“仙王境界能力”的全面解释。...' → tool=analyze_text_tool
11:09:07 app.api.v1.agent INFO   [Stream] Task started: [新增] 整合信息，生成对“仙王境界能力”的全面解释。
11:09:07 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
11:09:07 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
11:09:07 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
11:09:10 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:09:24 app.services.ai.http_ai_service INFO   API 响应完成，共接收 23 个数据块，总长度: 1989
11:09:24 app.services.ai.http_ai_service INFO   流式响应Token统计: 10872 (prompt=9410, completion=1462)
11:09:24 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
11:09:25 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
11:09:25 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=10872, cost=$0.026382, time=17225ms
11:09:25 app.services.agent.langgraph_tools INFO   ✅ [Agent分析] 分析完成，结果长度: 1989
11:09:25 app.api.v1.agent INFO   [Stream] 任务完成: [新增] 整合信息，生成对“仙王境界能力”的全面解释。 (17.3s)
11:09:25 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
11:09:25 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
11:09:25 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
11:09:30 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:09:32 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
11:09:32 app.services.ai.http_ai_service INFO   流式响应Token统计: 451 (prompt=450, completion=1)
11:09:32 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
11:09:32 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
11:09:32 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=451, cost=$0.000572, time=7129ms
11:09:32 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=451
11:09:32 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
11:09:32 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
11:09:32 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
11:09:33 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:09:35 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
11:09:35 app.services.ai.http_ai_service INFO   流式响应Token统计: 455 (prompt=454, completion=1)
11:09:35 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
11:09:35 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
11:09:35 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=455, cost=$0.000577, time=3276ms
11:09:35 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=455
11:09:35 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
11:09:35 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
11:09:35 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
11:09:37 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:09:38 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
11:09:38 app.services.ai.http_ai_service INFO   流式响应Token统计: 481 (prompt=480, completion=1)
11:09:38 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
11:09:38 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
11:09:38 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=481, cost=$0.000610, time=2829ms
11:09:38 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=481
11:09:38 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
11:09:38 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
11:09:38 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
11:09:39 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:09:42 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
11:09:42 app.services.ai.http_ai_service INFO   流式响应Token统计: 643 (prompt=642, completion=1)
11:09:42 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
11:09:42 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
11:09:42 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=643, cost=$0.000813, time=3891ms
11:09:42 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=643
11:09:42 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
11:09:42 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
11:09:42 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
11:09:44 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:09:45 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
11:09:45 app.services.ai.http_ai_service INFO   流式响应Token统计: 394 (prompt=393, completion=1)
11:09:45 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
11:09:45 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
11:09:45 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=394, cost=$0.000501, time=2770ms
11:09:45 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=394
11:09:45 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
11:09:45 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
11:09:45 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
11:09:47 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:09:48 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
11:09:48 app.services.ai.http_ai_service INFO   流式响应Token统计: 481 (prompt=480, completion=1)
11:09:48 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
11:09:48 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
11:09:48 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=481, cost=$0.000610, time=3705ms
11:09:48 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=481
11:09:48 app.services.agent.deep_agent.executor INFO   DeepAgent 执行完成: 任务=6, 反思=2, 重规划=1
11:09:48 app.services.agent.langgraph_agent INFO   [DeepAgent] 执行完成: 反思=2次, 重规划=1次
11:09:48 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共6个任务，耗时: 157.57s
11:09:48 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
11:09:48 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=2, 输出型=4, 展示型=0
11:09:48 app.services.agent.langgraph_agent INFO   [Response] 4个分析类任务，使用AI整合（避免冗余）
11:09:48 app.services.agent.langgraph_agent INFO   [Summarization] 使用AI整合任务结果
11:09:48 app.services.agent.langgraph_agent INFO   [Summarization] 上下文压缩: 原始=15398字符, 压缩后=4201字符, 压缩率=73%
11:09:48 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
11:09:48 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
11:09:48 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
11:09:50 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
11:09:53 app.services.ai.http_ai_service INFO   API 响应完成，共接收 6 个数据块，总长度: 395
11:09:53 app.services.ai.http_ai_service INFO   流式响应Token统计: 4236 (prompt=3954, completion=282)
11:09:53 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
11:09:53 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
11:09:53 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4236, cost=$0.007763, time=4825ms
11:09:53 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=4236
11:09:54 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 隔离=work:07251ab5-98b3-4df7-b5f2-2bdb75201d18 | 重要度=0.92
11:09:54 app.services.context.store INFO   [ContextStore] 保存上下文: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:798360bd-2759-4752-b699-76b9890c58dd, token=239
11:09:54 app.services.context.manager INFO   [ContextManager] 更新上下文: 602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:798360bd-2759-4752-b699-76b9890c58dd, 消息数=2, Token=239
11:09:54 app.services.agent.langgraph_agent INFO   [Planning] 已保存对话到 ContextManager (session=602f5147-846a-4cde-95d3-405fa75f133f:07251ab5-98b3-4df7-b5f2-2bdb75201d18:798360bd-2759-4752-b699-76b9890c58dd)
11:09:54 app.api.v1.agent INFO   [Stream] 跳过最终响应（内容已流式发送）
11:09:54 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed