INFO:     127.0.0.1:62110 - "OPTIONS /api/v1/chapters/ef5eb68c-32b8-4249-83a3-31d57363c0a9 HTTP/1.1" 200 OK
09:55:12 app.api.v1.novel_analysis INFO   后台任务已找到分析记录 analysis_id=930534b8-4c97-45a6-856c-e179e6b87fb6
09:55:12 app.services.ai.novel_analysis_orchestrator INFO   ============================================================
09:55:12 app.services.ai.novel_analysis_orchestrator INFO   开始分析作品: ad948837-e94e-4d0f-92a4-a75cf1301b07
09:55:12 app.services.ai.novel_analysis_orchestrator INFO   ============================================================
09:55:12 app.services.novel_analysis_service INFO   Updated analysis 930534b8-4c97-45a6-856c-e179e6b87fb6 progress: 0/5, stage: AnalysisStage.MICRO_ANALYSIS, status: AnalysisStatus.ANALYZING
09:55:12 app.services.ai.novel_analysis_orchestrator INFO   初始化AI分析服务...
09:55:12 app.services.ai.prompts INFO   Prompts loaded successfully from D:\Java\ai_writer\backend\app\services\ai\prompts\default.json
09:55:12 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
09:55:12 app.services.ai.http_ai_service INFO   ModelSelector 已启用
09:55:12 app.services.ai.http_ai_service INFO   AILogService 已启用 (用于成本追踪)
09:55:14 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
09:55:14 app.services.ai.novel_micro_analysis INFO   微观分析提示词加载成功
09:55:14 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
09:55:14 app.services.ai.http_ai_service INFO   ModelSelector 已启用
09:55:14 app.services.ai.http_ai_service INFO   AILogService 已启用 (用于成本追踪)
09:55:16 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
09:55:16 app.services.ai.novel_macro_analysis INFO   宏观分析提示词加载成功
09:55:16 app.services.ai.novel_analysis_orchestrator INFO   共获取 5 个章节，内容验证通过，开始微观分析...
09:55:16 app.services.ai.novel_analysis_orchestrator INFO   ⚡ 使用并行分析模式 (并发数: 5)
09:55:16 app.services.ai.novel_analysis_orchestrator INFO   ⚡ 启动 5 个并发分析任务...
09:55:16 app.services.ai.novel_analysis_orchestrator INFO   [1/5] 🔄 开始分析: 钢铁坟场
09:55:16 app.services.ai.novel_analysis_orchestrator INFO   [2/5] 🔄 开始分析: 归巢与低语
09:55:16 app.services.ai.novel_analysis_orchestrator INFO   [3/5] 🔄 开始分析: 遗落的星图
09:55:16 app.services.ai.novel_analysis_orchestrator INFO   [4/5] 🔄 开始分析: 天眼与土獾
09:55:16 app.services.ai.novel_analysis_orchestrator INFO   [5/5] 🔄 开始分析: 红雾下的星图
09:55:16 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:ad948837-e94e-4d0f-92a4-a75cf1301b07
09:55:16 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/ef5eb68c-32b8-4249-83a3-31d57363c0a9
09:55:16 app.services.ai.novel_micro_analysis INFO   开始AI分析章节: 298f5ac1-437c-4087-919b-5db66b1b3b14 - 天眼与土獾
09:55:16 app.services.ai.novel_micro_analysis INFO   第 1/3 次尝试调用AI分析
09:55:16 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
09:55:16 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
09:55:16 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=4000, temp=0.3, task_type=TaskType.SUMMARIZATION
09:55:16 app.services.redis_cache_service INFO   ✓ Redis连接成功 (timeout=10s, retry=enabled, pool=50)
09:55:16 app.services.ai.novel_micro_analysis INFO   开始AI分析章节: 803ee3d1-5cc6-48a7-871d-f4a53511a749 - 遗落的星图
09:55:16 app.services.ai.novel_micro_analysis INFO   第 1/3 次尝试调用AI分析
09:55:16 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
09:55:16 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
09:55:16 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=4000, temp=0.3, task_type=TaskType.SUMMARIZATION
09:55:16 app.services.ai.novel_micro_analysis INFO   开始AI分析章节: f0908bf1-bbc2-4d8e-9211-d33327dc82e7 - 归巢与低语
09:55:16 app.services.ai.novel_micro_analysis INFO   第 1/3 次尝试调用AI分析
09:55:16 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
09:55:16 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
09:55:16 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=4000, temp=0.3, task_type=TaskType.SUMMARIZATION
09:55:16 app.services.ai.novel_micro_analysis INFO   开始AI分析章节: 484090bc-6bd4-4118-8fd4-5c988e4a2c98 - 红雾下的星图
09:55:16 app.services.ai.novel_micro_analysis INFO   第 1/3 次尝试调用AI分析
09:55:16 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
09:55:16 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
09:55:16 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=4000, temp=0.3, task_type=TaskType.SUMMARIZATION
INFO:     127.0.0.1:60039 - "PUT /api/v1/chapters/ef5eb68c-32b8-4249-83a3-31d57363c0a9 HTTP/1.1" 200 OK
09:55:16 app.services.chapter_vector_service INFO   开始向量化章节: 钢铁坟场 (order=1)
09:55:16 app.services.ai.novel_micro_analysis INFO   开始AI分析章节: ef5eb68c-32b8-4249-83a3-31d57363c0a9 - 钢铁坟场
09:55:16 app.services.ai.novel_micro_analysis INFO   第 1/3 次尝试调用AI分析
09:55:16 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
09:55:16 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
09:55:16 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=4000, temp=0.3, task_type=TaskType.SUMMARIZATION
09:55:17 app.services.chapter_vector_service INFO   ✅ 章节向量存储完成: 钢铁坟场 (6段)
09:55:17 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:ad948837-e94e-4d0f-92a4-a75cf1301b07
09:55:17 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/ef5eb68c-32b8-4249-83a3-31d57363c0a9
INFO:     127.0.0.1:60039 - "PUT /api/v1/chapters/ef5eb68c-32b8-4249-83a3-31d57363c0a9 HTTP/1.1" 200 OK
09:55:17 app.services.chapter_vector_service INFO   开始向量化章节: 钢铁坟场 (order=1)
09:55:18 app.services.chapter_vector_service INFO   ✅ 章节向量存储完成: 钢铁坟场 (6段)
09:55:19 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
09:55:20 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
09:55:20 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
09:55:20 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
09:55:22 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
INFO:     127.0.0.1:54246 - "OPTIONS /api/v1/chapters/f0908bf1-bbc2-4d8e-9211-d33327dc82e7 HTTP/1.1" 200 OK
09:55:26 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:ad948837-e94e-4d0f-92a4-a75cf1301b07
09:55:26 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/f0908bf1-bbc2-4d8e-9211-d33327dc82e7
INFO:     127.0.0.1:54246 - "PUT /api/v1/chapters/f0908bf1-bbc2-4d8e-9211-d33327dc82e7 HTTP/1.1" 200 OK
09:55:26 app.services.chapter_vector_service INFO   开始向量化章节: 归巢与低语 (order=2)
09:55:27 app.services.chapter_vector_service INFO   ✅ 章节向量存储完成: 归巢与低语 (7段)
09:55:27 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:ad948837-e94e-4d0f-92a4-a75cf1301b07
09:55:27 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/f0908bf1-bbc2-4d8e-9211-d33327dc82e7
INFO:     127.0.0.1:54246 - "PUT /api/v1/chapters/f0908bf1-bbc2-4d8e-9211-d33327dc82e7 HTTP/1.1" 200 OK
09:55:27 app.services.chapter_vector_service INFO   开始向量化章节: 归巢与低语 (order=2)
09:55:28 app.services.chapter_vector_service INFO   ✅ 章节向量存储完成: 归巢与低语 (7段)
09:55:37 app.services.ai.http_ai_service INFO   API 响应完成，共接收 42 个数据块，总长度: 6747
09:55:37 app.services.ai.http_ai_service INFO   流式响应Token统计: 7294 (prompt=4545, completion=2749)
09:55:37 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:实例): tokens=7294, cost=$0.033171, time=21429ms
09:55:37 app.services.redis_cache_service INFO   ✓ 结果已缓存: novel_analysis:v2:micro:b088f948... (TTL: 604800秒)
09:55:37 app.services.ai.novel_micro_analysis INFO   章节 803ee3d1-5cc6-48a7-871d-f4a53511a749 分析成功，提取事件数: 8
09:55:37 app.services.ai.novel_analysis_orchestrator INFO   [3/5] ✓ 分析完成: 遗落的星图 (21.6秒)
INFO:     127.0.0.1:63721 - "OPTIONS /api/v1/agent/chat/stream HTTP/1.1" 200 OK
09:55:38 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
09:55:38 app.services.ai.http_ai_service INFO   ModelSelector 已启用
09:55:38 app.services.ai.http_ai_service INFO   AILogService 已启用 (用于成本追踪)
09:55:40 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
09:55:40 app.api.v1.agent INFO   [Chat Stream] Mode: planning
09:55:40 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:63721 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
09:55:40 app.core.redis INFO   ✅ Redis connected: redis://localhost:6379/0
09:55:40 app.api.v1.agent INFO   [Session] 创建新会话归属: 4e2b53a7-603f-493c-bc80-864f7ddf6713 -> 602f5147-846a-4cde-95d3-405fa75f133f
09:55:40 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: planning, Message: 这章章名是什么？...
09:55:40 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
09:55:40 app.services.ai.http_ai_service INFO   ModelSelector 已启用
09:55:40 app.services.ai.http_ai_service WARNING   成本追踪已启用，但未提供db或user_id，成本数据将不会被记录！请检查HTTPAIService初始化参数。
09:55:42 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
09:55:42 app.services.context.adaptive_budget INFO   ✅ 所有预算配置验证通过
09:55:53 app.services.context.vector_memory_store INFO   ✅ VectorMemoryStore初始化成功 | 目录=./data/chroma_db | 模型=paraphrase-multilingual-MiniLM-L12-v2 | 集合=user_memories
09:55:53 app.services.context.manager INFO   ✅ VectorMemoryStore 已初始化
09:55:53 app.services.context.manager INFO   ✅ ContextManager: 长期记忆已启用 (user_id=None)
09:55:53 app.services.context.manager INFO   ✅ ContextManager: 自适应预算已启用
09:55:53 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ ContextManager已初始化（长期记忆已启用，自适应预算已启用，总预算=16000 tokens）
成功加载模板: intent_classifier (版本 2.0.0)
成功加载模板: writing_agent (版本 2.0.0)
成功加载模板: planning_agent (版本 2.0.0)
成功加载模板: tool_agent (版本 2.0.0)
成功加载模板: query_agent (版本 2.0.0)
成功加载模板: system_agent_prompt (版本 2.0.0)
成功加载模板: creative_writing_prompt (版本 1.0.0)
09:55:53 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ PromptManager已初始化
09:55:53 app.services.agent.langgraph_agent INFO   [LangGraph] 使用 HTTPAIService 模式（手动工具调用，绕过 Cloudflare）
09:55:53 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ Redis连接验证成功
09:55:53 app.services.agent.langgraph_agent INFO   [LangGraph] OK 使用 AsyncRedisSaver（redis://localhost:6379/0，TTL=7天）
09:55:53 app.services.agent.memory.metrics INFO   [MemoryMetrics] 监控系统已初始化
09:55:53 app.services.agent.memory.long_term_store INFO   [LongTermStore] Initialized: base_dir=./data/long_term_memory, max_size=50KB, compression=True
09:55:53 app.services.agent.memory.enhanced_memory_manager INFO   EnhancedMemoryManager initialized: short=10, medium=100, threshold=0.1, long_term_backup=enabled
09:55:53 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ EnhancedMemoryManager已创建
09:55:53 app.services.agent.memory.unified_coordinator INFO   [UnifiedMemoryCoordinator] 初始化统一记忆协调器
09:55:53 app.services.agent.memory.unified_coordinator INFO   [UnifiedMemoryCoordinator] 全局实例已设置
09:55:53 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ UnifiedMemoryCoordinator已初始化 | checkpointer=AsyncRedisSaver | enhanced_memory=yes | context_manager=yes
09:55:53 app.services.agent.parallel_tool_node INFO   [ParallelToolNode] 初始化完成，最大并发数=5，并行安全工具=4个
09:55:53 app.api.v1.agent INFO   [Global Agent] 创建全局Agent实例，MemorySaver将在请求间共享
09:55:53 app.services.agent.langgraph_agent INFO   [Planning] 使用隔离的thread_id: ad948837-e94e-4d0f-92a4-a75cf1301b07:4e2b53a7-603f-493c-bc80-864f7ddf6713 (work_id=ad948837-e94e-4d0f-92a4-a75cf1301b07, conversation_id=4e2b53a7-603f-493c-bc80-864f7ddf6713)
09:55:53 app.services.ai.http_ai_service INFO   API 响应完成，共接收 34 个数据块，总长度: 5270
09:55:53 app.services.ai.http_ai_service INFO   流式响应Token统计: 6987 (prompt=4764, completion=2223)
09:55:53 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: 这章章名是什么？...
09:55:53 app.core.cache INFO   ⚠️ 缓存未命中: prompt:get_planning_static_prompt:fca6eb91156619d0
09:55:53 app.core.cache INFO   💾 缓存已保存: prompt:get_planning_static_prompt:fca6eb91156619d0 (expire=3600s)
09:55:53 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
09:55:53 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
09:55:53 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=600, temp=0.3, task_type=TaskType.SIMPLE_QA
09:55:53 app.services.ai.http_ai_service INFO   API 响应完成，共接收 40 个数据块，总长度: 6615
09:55:53 app.services.ai.http_ai_service INFO   流式响应Token统计: 8207 (prompt=5595, completion=2612)
09:55:53 app.services.ai.http_ai_service INFO   API 响应完成，共接收 41 个数据块，总长度: 6698
09:55:53 app.services.ai.http_ai_service INFO   流式响应Token统计: 8460 (prompt=5775, completion=2685)
09:55:53 app.services.ai.http_ai_service INFO   API 响应完成，共接收 45 个数据块，总长度: 7413
09:55:53 app.services.ai.http_ai_service INFO   流式响应Token统计: 7591 (prompt=4655, completion=2936)
09:55:53 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:实例): tokens=6987, cost=$0.028185, time=37258ms
09:55:53 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:实例): tokens=8460, cost=$0.034069, time=37287ms
09:55:53 app.services.redis_cache_service INFO   ✓ 结果已缓存: novel_analysis:v2:micro:afbfba55... (TTL: 604800秒)
09:55:53 app.services.ai.novel_micro_analysis INFO   章节 f0908bf1-bbc2-4d8e-9211-d33327dc82e7 分析成功，提取事件数: 7
09:55:53 app.services.ai.novel_analysis_orchestrator INFO   [2/5] ✓ 分析完成: 归巢与低语 (37.5秒)
09:55:53 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:实例): tokens=8207, cost=$0.033114, time=37315ms
09:55:53 app.services.redis_cache_service INFO   ✓ 结果已缓存: novel_analysis:v2:micro:71954b9c... (TTL: 604800秒)
09:55:53 app.services.ai.novel_micro_analysis INFO   章节 ef5eb68c-32b8-4249-83a3-31d57363c0a9 分析成功，提取事件数: 10
09:55:53 app.services.ai.novel_analysis_orchestrator INFO   [1/5] ✓ 分析完成: 钢铁坟场 (37.5秒)
09:55:53 app.services.redis_cache_service INFO   ✓ 结果已缓存: novel_analysis:v2:micro:09e220db... (TTL: 604800秒)
09:55:53 app.services.ai.novel_micro_analysis INFO   章节 298f5ac1-437c-4087-919b-5db66b1b3b14 分析成功，提取事件数: 9
09:55:53 app.services.ai.novel_analysis_orchestrator INFO   [4/5] ✓ 分析完成: 天眼与土獾 (37.5秒)
09:55:53 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:实例): tokens=7591, cost=$0.035179, time=37349ms
09:55:53 app.services.redis_cache_service INFO   ✓ 结果已缓存: novel_analysis:v2:micro:00d87f02... (TTL: 604800秒)
09:55:53 app.services.ai.novel_micro_analysis INFO   章节 484090bc-6bd4-4118-8fd4-5c988e4a2c98 分析成功，提取事件数: 9
09:55:53 app.services.ai.novel_analysis_orchestrator INFO   [5/5] ✓ 分析完成: 红雾下的星图 (37.5秒)
09:55:53 app.services.ai.novel_analysis_orchestrator INFO   ⚡ 并行分析完成: 成功 5/5 章
09:55:53 app.services.ai.novel_analysis_orchestrator INFO   💾 开始批量保存 5 个分析结果...
09:55:53 app.services.novel_analysis_service INFO   Batch saved 5 micro results for analysis 930534b8-4c97-45a6-856c-e179e6b87fb6, total: 5
09:55:53 app.services.ai.novel_analysis_orchestrator INFO   ✅ 批量保存完成: 5 个结果
09:55:53 app.services.ai.novel_analysis_orchestrator INFO   🔍 开始批量存储向量...
09:55:53 app.services.vector_store_service INFO   开始向量化章节 ef5eb68c-32b8-4249-83a3-31d57363c0a9 的微观分析数据
09:55:54 app.services.vector_store_service INFO   生成向量维度: 384
09:55:54 app.services.vector_store_service INFO   向量存储成功: vector_id=5ebf7614-b1c0-4d79-9b05-118a8bf816d1
09:55:54 app.services.vector_store_service INFO   开始向量化章节 f0908bf1-bbc2-4d8e-9211-d33327dc82e7 的微观分析数据
09:55:54 app.services.vector_store_service INFO   生成向量维度: 384
09:55:54 app.services.vector_store_service INFO   向量存储成功: vector_id=b6074ca4-7ccb-42f2-adfe-7eec9d774b61
09:55:54 app.services.vector_store_service INFO   开始向量化章节 803ee3d1-5cc6-48a7-871d-f4a53511a749 的微观分析数据
09:55:54 app.services.vector_store_service INFO   生成向量维度: 384
09:55:54 app.services.vector_store_service INFO   向量存储成功: vector_id=d0a05496-0951-47cd-9226-07b3a11d8a3e
09:55:55 app.services.vector_store_service INFO   开始向量化章节 298f5ac1-437c-4087-919b-5db66b1b3b14 的微观分析数据
09:55:55 app.services.vector_store_service INFO   生成向量维度: 384
09:55:55 app.services.vector_store_service INFO   向量存储成功: vector_id=91d119f3-899d-4a7e-a921-5bbe9616a823
09:55:55 app.services.vector_store_service INFO   开始向量化章节 484090bc-6bd4-4118-8fd4-5c988e4a2c98 的微观分析数据
09:55:55 app.services.vector_store_service INFO   生成向量维度: 384
09:55:55 app.services.vector_store_service INFO   向量存储成功: vector_id=56509eb0-1d5d-4ca6-ab90-7609c00518a7
09:55:55 app.services.ai.novel_analysis_orchestrator INFO   ✅ 批量向量存储完成
09:55:55 app.services.ai.novel_analysis_orchestrator INFO   ============================================================
09:55:55 app.services.ai.novel_analysis_orchestrator INFO   微观分析完成统计:
09:55:55 app.services.ai.novel_analysis_orchestrator INFO     成功: 5/5 章节 (100.0%)
09:55:55 app.services.ai.novel_analysis_orchestrator INFO     失败: 0 章节
09:55:55 app.services.ai.novel_analysis_orchestrator INFO     总耗时: 43.0秒 (平均 8.6秒/章)
09:55:55 app.services.ai.novel_analysis_orchestrator INFO   ============================================================
09:55:55 app.services.novel_analysis_service INFO   Updated analysis 930534b8-4c97-45a6-856c-e179e6b87fb6 progress: 5/5, stage: AnalysisStage.MACRO_ANALYSIS, status: None
09:55:55 app.services.ai.novel_analysis_orchestrator INFO   ============================================================
09:55:55 app.services.ai.novel_analysis_orchestrator INFO   开始宏观分析...
09:55:55 app.services.ai.novel_analysis_orchestrator INFO   ============================================================
09:55:55 app.services.ai.novel_macro_analysis INFO   开始宏观分析，共 5 个章节的数据，43 个事件
09:55:55 app.services.ai.novel_macro_analysis INFO   第 1/3 次尝试调用AI宏观分析
09:55:55 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
09:55:55 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
09:55:55 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=6000, temp=0.5, task_type=TaskType.SUMMARIZATION
09:55:56 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
09:55:57 app.services.ai.http_ai_service INFO   API 响应完成，共接收 3 个数据块，总长度: 259
09:55:57 app.services.ai.http_ai_service INFO   流式响应Token统计: 1162 (prompt=1043, completion=119)
09:55:57 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1162, cost=$0.002494, time=4198ms
09:55:57 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=1162
09:55:57 app.services.agent.langgraph_agent INFO   [JSON解析] 方法2成功: 从```json块提取
09:55:57 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共1个任务，耗时: 4.29s
09:55:57 app.api.v1.agent INFO   [Stream] 规划生成: 1 个任务
09:55:57 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
09:55:57 app.services.agent.parameter_resolver INFO   [ParameterResolver] 初始化完成, 严格模式: False
09:55:57 app.services.agent.langgraph_agent INFO   [ParameterResolver] 参数解析器已启用
09:55:57 app.services.agent.langgraph_agent INFO   [ParallelExecution] 任务分组: 并行=1, 串行=0
09:55:57 app.services.agent.langgraph_agent INFO   [ParallelExecution] 开始并行执行1个任务
09:55:57 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务1开始: 根据chapter_id读取章节信息
09:55:57 app.api.v1.agent INFO   [Stream] 任务开始: 根据chapter_id读取章节信息
09:55:57 app.services.agent.langgraph_agent INFO   [read_chapter_tool] ✅ 读取章节成功: 归巢与低语
09:55:57 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务1完成
09:55:57 app.api.v1.agent INFO   [Stream] 任务完成: 根据chapter_id读取章节信息 (0.0s)
09:55:57 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共1个任务，耗时: 0.05s
09:55:57 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
09:55:57 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=0, 输出型=0, 展示型=1
09:55:57 app.services.agent.langgraph_agent INFO   [Response] 纯展示型任务(1个)，直接格式化返回（跳过AI整合，节省成本）
09:55:58 app.api.v1.agent INFO   [Stream] 跳过最终响应（内容已流式发送）
09:55:58 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed
09:55:58 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
09:56:12 app.services.ai.http_ai_service INFO   API 响应完成，共接收 42 个数据块，总长度: 2732
09:56:12 app.services.ai.http_ai_service INFO   流式响应Token统计: 16318 (prompt=14285, completion=2033)
09:56:12 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:实例): tokens=16318, cost=$0.038186, time=16591ms
09:56:12 app.services.ai.novel_macro_analysis INFO   宏观分析完成，报告长度: 2732 字符
09:56:12 app.services.ai.novel_analysis_orchestrator INFO   宏观分析完成，报告长度: 2732 字符，耗时: 16.6秒
09:56:12 app.services.novel_analysis_service INFO   Saved macro result for analysis 930534b8-4c97-45a6-856c-e179e6b87fb6, marked as completed
09:56:12 app.services.ai.novel_analysis_orchestrator INFO   ============================================================
09:56:12 app.services.ai.novel_analysis_orchestrator INFO   作品 ad948837-e94e-4d0f-92a4-a75cf1301b07 分析全部完成！
09:56:12 app.services.ai.novel_analysis_orchestrator INFO   ============================================================
09:56:12 app.services.ai.novel_analysis_orchestrator INFO   📊 分析统计:
09:56:12 app.services.ai.novel_analysis_orchestrator INFO     微观分析: 5/5 章 (成功率 100.0%)
09:56:12 app.services.ai.novel_analysis_orchestrator INFO     宏观报告: 2732 字符
09:56:12 app.services.ai.novel_analysis_orchestrator INFO     总耗时: 59.7秒 (1.0分钟)
09:56:12 app.services.ai.novel_analysis_orchestrator INFO     平均速度: 11.9秒/章
09:56:12 app.services.ai.novel_analysis_orchestrator INFO     向量存储: 5 条，覆盖 5 章
09:56:12 app.services.ai.novel_analysis_orchestrator INFO   ============================================================
09:56:12 app.services.ai.novel_analysis_orchestrator INFO   AI服务资源已清理
09:56:12 app.services.ai.novel_analysis_orchestrator INFO   AI服务资源已清理
09:56:12 app.api.v1.novel_analysis INFO   后台任务完成：作品 ad948837-e94e-4d0f-92a4-a75cf1301b07 分析成功
09:56:25 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
09:56:25 app.services.ai.http_ai_service INFO   ModelSelector 已启用
09:56:25 app.services.ai.http_ai_service INFO   AILogService 已启用 (用于成本追踪)
09:56:27 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
09:56:27 app.api.v1.agent INFO   [Chat Stream] Mode: planning
09:56:27 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:64289 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
09:56:27 app.api.v1.agent INFO   [Session] 创建新会话归属: 6988a486-d876-4196-91ef-cbbf7c15a7b7 -> 602f5147-846a-4cde-95d3-405fa75f133f
09:56:27 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: planning, Message: 这章主要讲了什么内容...
09:56:27 app.services.agent.langgraph_agent INFO   [Planning] 使用隔离的thread_id: ad948837-e94e-4d0f-92a4-a75cf1301b07:6988a486-d876-4196-91ef-cbbf7c15a7b7 (work_id=ad948837-e94e-4d0f-92a4-a75cf1301b07, conversation_id=6988a486-d876-4196-91ef-cbbf7c15a7b7)
09:56:27 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: 这章主要讲了什么内容...
09:56:27 app.core.cache INFO   ✅ 缓存命中: prompt:get_planning_static_prompt:fca6eb91156619d0
09:56:27 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
09:56:27 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
09:56:27 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=600, temp=0.3, task_type=TaskType.SIMPLE_QA
09:56:29 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
09:56:31 app.services.ai.http_ai_service INFO   API 响应完成，共接收 2 个数据块，总长度: 251
09:56:31 app.services.ai.http_ai_service INFO   流式响应Token统计: 1203 (prompt=1083, completion=120)
09:56:31 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1203, cost=$0.002554, time=4319ms
09:56:31 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=1203
09:56:31 app.services.agent.langgraph_agent INFO   [JSON解析] 方法2成功: 从```json块提取
09:56:31 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共1个任务，耗时: 4.33s
09:56:31 app.api.v1.agent INFO   [Stream] 规划生成: 1 个任务
09:56:31 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
09:56:31 app.services.agent.parameter_resolver INFO   [ParameterResolver] 初始化完成, 严格模式: False
09:56:31 app.services.agent.langgraph_agent INFO   [ParameterResolver] 参数解析器已启用
09:56:31 app.services.agent.langgraph_agent INFO   [ParallelExecution] 任务分组: 并行=1, 串行=0
09:56:31 app.services.agent.langgraph_agent INFO   [ParallelExecution] 开始并行执行1个任务
09:56:31 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务1开始: 读取指定章节内容
09:56:31 app.api.v1.agent INFO   [Stream] 任务开始: 读取指定章节内容
09:56:31 app.services.agent.langgraph_agent INFO   [read_chapter_tool] ✅ 读取章节成功: 归巢与低语
09:56:31 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务1完成
09:56:31 app.api.v1.agent INFO   [Stream] 任务完成: 读取指定章节内容 (0.0s)
09:56:31 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共1个任务，耗时: 0.01s
09:56:31 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
09:56:31 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=0, 输出型=0, 展示型=1
09:56:31 app.services.agent.langgraph_agent INFO   [Response] 纯展示型任务(1个)，直接格式化返回（跳过AI整合，节省成本）
09:56:31 app.api.v1.agent INFO   [Stream] 跳过最终响应（内容已流式发送）
09:56:31 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed
09:59:56 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
09:59:56 app.services.ai.http_ai_service INFO   ModelSelector 已启用
09:59:56 app.services.ai.http_ai_service INFO   AILogService 已启用 (用于成本追踪)
09:59:58 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
09:59:58 app.api.v1.agent INFO   [Chat Stream] Mode: planning
09:59:58 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:50870 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
09:59:58 app.api.v1.agent INFO   [Session] 创建新会话归属: 210623e6-1240-4c1b-9dbc-91f5e7fce045 -> 602f5147-846a-4cde-95d3-405fa75f133f
09:59:58 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: planning, Message: 这章出现了那些人物？...
09:59:58 app.services.agent.langgraph_agent INFO   [Planning] 使用隔离的thread_id: ad948837-e94e-4d0f-92a4-a75cf1301b07:210623e6-1240-4c1b-9dbc-91f5e7fce045 (work_id=ad948837-e94e-4d0f-92a4-a75cf1301b07, conversation_id=210623e6-1240-4c1b-9dbc-91f5e7fce045)
09:59:58 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: 这章出现了那些人物？...
09:59:58 app.core.cache INFO   ✅ 缓存命中: prompt:get_planning_static_prompt:fca6eb91156619d0
09:59:58 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
09:59:58 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
09:59:58 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=600, temp=0.3, task_type=TaskType.SIMPLE_QA
10:00:00 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:00:01 app.services.ai.http_ai_service INFO   API 响应完成，共接收 3 个数据块，总长度: 437
10:00:01 app.services.ai.http_ai_service INFO   流式响应Token统计: 1158 (prompt=968, completion=190)
10:00:01 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1158, cost=$0.003110, time=3660ms
10:00:01 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=1158
10:00:01 app.services.agent.langgraph_agent INFO   [JSON解析] 方法2成功: 从```json块提取
10:00:01 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共2个任务，耗时: 3.70s
10:00:01 app.api.v1.agent INFO   [Stream] 规划生成: 2 个任务
10:00:01 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
10:00:01 app.services.agent.parameter_resolver INFO   [ParameterResolver] 初始化完成, 严格模式: False
10:00:01 app.services.agent.langgraph_agent INFO   [ParameterResolver] 参数解析器已启用
10:00:01 app.services.agent.langgraph_agent INFO   [ParallelExecution] 任务分组: 并行=1, 串行=1
10:00:01 app.services.agent.langgraph_agent INFO   [ParallelExecution] 开始并行执行1个任务
10:00:01 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务1开始: 读取指定章节内容
10:00:01 app.api.v1.agent INFO   [Stream] 任务开始: 读取指定章节内容
10:00:01 app.services.agent.langgraph_agent INFO   [read_chapter_tool] ✅ 读取章节成功: 归巢与低语
10:00:01 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务1完成
10:00:01 app.api.v1.agent INFO   [Stream] 任务完成: 读取指定章节内容 (0.0s)
10:00:01 app.services.agent.langgraph_agent INFO   [ParallelExecution] 开始串行执行1个任务
10:00:01 app.services.agent.langgraph_agent INFO   [ParallelExecution] 串行任务2开始: 分析章节中出现的人物
10:00:01 app.api.v1.agent INFO   [Stream] 任务开始: 分析章节中出现的人物
10:00:01 app.prompts.constraint_manager INFO   ✅ 已加载模板: analyze_text (v3.0.0)
10:00:01 app.prompts.constraint_manager INFO   ✅ 已加载模板: creative_writing (v1.0.0)
10:00:01 app.prompts.constraint_manager INFO   ✅ 已加载模板: intent_classifier (v2.0.0)
10:00:01 app.prompts.constraint_manager INFO   ✅ 已加载模板: planning_agent (v2.0.0)
10:00:01 app.prompts.constraint_manager INFO   ✅ 已加载模板: query_agent (v2.0.0)
10:00:01 app.prompts.constraint_manager INFO   ✅ 已加载模板: system_agent (v2.0.0)
10:00:01 app.prompts.constraint_manager INFO   ✅ 已加载模板: tool_agent (v2.0.0)
10:00:01 app.prompts.constraint_manager INFO   ✅ 已加载模板: writing_agent (v2.0.0)
10:00:01 app.prompts.constraint_manager INFO   ✅ 约束提示词管理器已初始化: 加载8个模板, 注册0个验证器
10:00:01 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
10:00:01 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
10:00:01 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
10:00:03 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:00:18 app.services.ai.http_ai_service INFO   API 响应完成，共接收 41 个数据块，总长度: 2809
10:00:18 app.services.ai.http_ai_service INFO   流式响应Token统计: 5727 (prompt=3764, completion=1963)
10:00:18 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=5727, cost=$0.024335, time=16732ms
10:00:18 app.services.agent.langgraph_agent INFO   ✅ [Agent分析] 分析完成，结果长度: 2809
10:00:18 app.services.agent.langgraph_agent INFO   [ParallelExecution] 串行任务2完成
10:00:18 app.api.v1.agent INFO   [Stream] 任务完成: 分析章节中出现的人物 (16.8s)
10:00:18 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共2个任务，耗时: 16.82s
10:00:18 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
10:00:18 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=0, 输出型=1, 展示型=1
10:00:18 app.services.agent.langgraph_agent INFO   [Response] 单个分析任务(analyze_text_tool)，使用AI格式化
10:00:18 app.services.agent.langgraph_agent INFO   [Summarization] 使用AI整合任务结果
10:00:18 app.services.agent.langgraph_agent INFO   [Summarization] 上下文压缩: 原始=6121字符, 压缩后=4089字符, 压缩率=34%
10:00:18 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
10:00:18 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
10:00:18 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
10:00:20 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:00:21 app.services.ai.http_ai_service INFO   API 响应完成，共接收 4 个数据块，总长度: 293
10:00:21 app.services.ai.http_ai_service INFO   流式响应Token统计: 3285 (prompt=3076, completion=209)
10:00:21 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=3285, cost=$0.005935, time=2925ms
10:00:21 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=3285
10:00:21 app.api.v1.agent INFO   [Stream] 跳过最终响应（内容已流式发送）
10:00:21 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed
