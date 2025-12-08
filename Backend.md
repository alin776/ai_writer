15:51:38 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: planning, Message: 请先深度分析《一夕千悟，从杂役弟子开始》前5章的：
  1. 人物关系图谱（段融、杨震、孔斌三人组、...
15:51:38 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
15:51:38 app.services.ai.http_ai_service INFO   ModelSelector 已启用
15:51:38 app.services.ai.http_ai_service INFO   [成本追踪] 初始化未传db/user_id，将使用请求上下文按需记录成本
15:51:43 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
15:51:43 app.services.context.adaptive_budget INFO   ✅ 所有预算配置验证通过
15:51:59 app.services.context.vector_memory_store INFO   ✅ VectorMemoryStore初始化成功 | 目录=./data/chroma_db | 模型=paraphrase-multilingual-MiniLM-L12-v2 | 集合=user_memories
15:51:59 app.services.context.manager INFO   ✅ VectorMemoryStore 已初始化
15:51:59 app.services.context.manager INFO   ✅ ContextManager: 长期记忆已启用 (user_id=None)
15:51:59 app.services.context.manager INFO   ✅ ContextManager: 自适应预算已启用
15:51:59 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ ContextManager已初始化（长期记忆已启用，自适应预算已启用，总预算=16000 tokens）
成功加载模板: intent_classifier (版本 2.0.0)
成功加载模板: writing_agent (版本 2.0.0)
成功加载模板: planning_agent (版本 2.0.0)
成功加载模板: tool_agent (版本 2.0.0)
成功加载模板: query_agent (版本 2.0.0)
成功加载模板: system_agent_prompt (版本 2.0.0)
成功加载模板: creative_writing_prompt (版本 1.0.0)
15:51:59 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ PromptManager已初始化
15:51:59 app.services.agent.langgraph_agent INFO   [LangGraph] 使用 HTTPAIService 模式（手动工具调用，绕过 Cloudflare）
15:51:59 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ Redis连接验证成功
15:51:59 app.services.agent.langgraph_agent INFO   [LangGraph] OK 使用 AsyncRedisSaver（redis://localhost:6379/0，TTL=7天）
15:51:59 app.services.agent.memory.metrics INFO   [MemoryMetrics] 监控系统已初始化
15:51:59 app.services.agent.memory.long_term_store INFO   [LongTermStore] Initialized: base_dir=./data/long_term_memory, max_size=50KB, compression=True
15:51:59 app.services.agent.memory.enhanced_memory_manager INFO   EnhancedMemoryManager initialized: short=10, medium=100, threshold=0.1, long_term_backup=enabled
15:51:59 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ EnhancedMemoryManager已创建
15:51:59 app.services.agent.memory.unified_coordinator INFO   [UnifiedMemoryCoordinator] 初始化统一记忆协调器
15:51:59 app.services.agent.memory.unified_coordinator INFO   [UnifiedMemoryCoordinator] 全局实例已设置
15:51:59 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ UnifiedMemoryCoordinator已初始化 | checkpointer=AsyncRedisSaver | enhanced_memory=yes | context_manager=yes
15:51:59 app.services.agent.parallel_tool_node INFO   [ParallelToolNode] 初始化完成，最大并发数=5，并行安全工具=4个
15:51:59 app.api.v1.agent INFO   [Global Agent] created global agent instance; MemorySaver shared across requests
15:51:59 app.services.agent.langgraph_agent INFO   [Planning] 使用隔离的thread_id: 9398f47b-1e74-4e1c-93dd-e837e51dbaaf:12125a43-768f-499e-b409-1421f8875cf3 (work_id=9398f47b-1e74-4e1c-93dd-e837e51dbaaf, conversation_id=12125a43-768f-499e-b409-1421f8875cf3)
15:51:59 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: 请先深度分析《一夕千悟，从杂役弟子开始》前5章的：
  1. 人物关系图谱（段融、杨震、孔斌三人组、...
15:51:59 app.core.cache INFO   ✅ 缓存命中: prompt:get_planning_agent_mode_prompt:fca6eb91156619d0
15:51:59 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
15:51:59 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
15:51:59 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=1200, temp=0.3, task_type=TaskType.SIMPLE_QA
15:51:59 app.services.ai.http_ai_service INFO   API 响应完成，共接收 41 个数据块，总长度: 6540
15:51:59 app.services.ai.http_ai_service INFO   流式响应Token统计: 7626 (prompt=4969, completion=2657)
15:51:59 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
15:51:59 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:实例): tokens=6043, cost=$0.026060, time=17426ms
15:51:59 app.services.redis_cache_service INFO   ✓ 结果已缓存: novel_analysis:v2:micro:cc0abb0e... (TTL: 604800秒)
15:51:59 app.services.ai.novel_micro_analysis INFO   章节 6481bdc8-3657-4aca-a638-af31744a57cf 分析成功，提取事件数: 6
15:51:59 app.services.ai.novel_analysis_orchestrator INFO   [1/6] ✓ 分析完成: 百年关，天机变 (38.7秒)
15:51:59 app.services.ai.novel_analysis_orchestrator INFO   [6/6] 🔄 开始分析: 嵩山少室，魔焰滔天
15:51:59 app.services.ai.novel_micro_analysis INFO   开始AI分析章节: 340878e8-73b6-4ed7-96eb-6aee60332f87 - 嵩山少室，魔焰滔天
15:51:59 app.services.ai.novel_micro_analysis INFO   第 1/3 次尝试调用AI分析
15:51:59 app.services.ai.http_ai_service INFO   API 响应完成，共接收 38 个数据块，总长度: 6079
15:51:59 app.services.ai.http_ai_service INFO   流式响应Token统计: 7121 (prompt=4622, completion=2499)
15:52:00 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
15:52:00 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
15:52:00 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=4000, temp=0.3, task_type=TaskType.SUMMARIZATION
15:52:00 app.services.ai.http_ai_service INFO   API 响应完成，共接收 43 个数据块，总长度: 6602
15:52:00 app.services.ai.http_ai_service INFO   流式响应Token统计: 7654 (prompt=4867, completion=2787)
15:52:00 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
15:52:00 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:实例): tokens=7626, cost=$0.032781, time=38539ms
15:52:00 app.services.redis_cache_service INFO   ✓ 结果已缓存: novel_analysis:v2:micro:dd535d4d... (TTL: 604800秒)
15:52:00 app.services.ai.novel_micro_analysis INFO   章节 6c02b0db-0a67-4d6e-a27f-86e3c7ff7289 分析成功，提取事件数: 7
15:52:00 app.services.ai.novel_analysis_orchestrator INFO   [2/6] ✓ 分析完成: 道祖出关，太极震群魔 (39.1秒)
15:52:00 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
15:52:00 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:实例): tokens=7121, cost=$0.030767, time=38714ms
15:52:00 app.services.ai.http_ai_service INFO   API 响应完成，共接收 41 个数据块，总长度: 6388
15:52:00 app.services.ai.http_ai_service INFO   流式响应Token统计: 8567 (prompt=5901, completion=2666)
15:52:00 app.services.redis_cache_service INFO   ✓ 结果已缓存: novel_analysis:v2:micro:7fda3049... (TTL: 604800秒)
15:52:00 app.services.ai.novel_micro_analysis INFO   章节 04889237-7067-4527-88b1-c5232a5bd47c 分析成功，提取事件数: 8
15:52:00 app.services.ai.novel_analysis_orchestrator INFO   [5/6] ✓ 分析完成: 一饭之恩，乱世人心 (39.2秒)
15:52:00 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
15:52:00 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:实例): tokens=7654, cost=$0.033954, time=38727ms
15:52:00 app.services.redis_cache_service INFO   ✓ 结果已缓存: novel_analysis:v2:micro:09970a46... (TTL: 604800秒)
15:52:00 app.services.ai.novel_micro_analysis INFO   章节 c285feff-d240-4cfd-8bda-a05bb79af50b 分析成功，提取事件数: 7
15:52:00 app.services.ai.novel_analysis_orchestrator INFO   [3/6] ✓ 分析完成: 下山 (39.2秒)
15:52:00 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
15:52:00 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:实例): tokens=8567, cost=$0.034036, time=39091ms
15:52:00 app.services.redis_cache_service INFO   ✓ 结果已缓存: novel_analysis:v2:micro:612c6e93... (TTL: 604800秒)
15:52:00 app.services.ai.novel_micro_analysis INFO   章节 9d18cb2b-3210-4235-a6a0-635af73db118 分析成功，提取事件数: 9
15:52:00 app.services.ai.novel_analysis_orchestrator INFO   [4/6] ✓ 分析完成: 荒村孤烟，道祖传心 (39.3秒)
15:52:02 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
15:52:02 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
15:52:08 app.services.ai.http_ai_service INFO   API 响应完成，共接收 20 个数据块，总长度: 2529
15:52:08 app.services.ai.http_ai_service INFO   流式响应Token统计: 5804 (prompt=4521, completion=1283)
15:52:08 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
15:52:08 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=5804, cost=$0.018481, time=9122ms
15:52:08 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=5804
15:52:08 app.services.agent.langgraph_agent INFO   [JSON解析] 方法2成功: 从```json块提取
15:52:08 app.services.agent.langgraph_agent INFO   [Planning] 思维链: 输出=用户期望得到两部分内容：1. 对《一夕千悟，从杂役弟子开始》, 原料=需要获取《一夕千悟，从杂役弟子开始》前5, 处理=首先，获取前5章的文本内容。然后，使用
15:52:08 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共7个任务，耗时: 9.36s
15:52:08 app.api.v1.agent INFO   [Stream] Plan tasks: 7 items
15:52:08 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
15:52:08 app.services.agent.langgraph_agent INFO   [DeepAgent] 启用反思模式
15:52:08 app.services.agent.parameter_resolver INFO   [ParameterResolver] 初始化完成, 严格模式: False
15:52:08 app.services.agent.langgraph_agent INFO   [DeepAgent] ParameterResolver 已启用
15:52:08 app.services.agent.deep_agent.executor INFO   DeepAgent 开始执行，共 7 个任务，反思功能已启用
15:52:08 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] AI 推断功能已启用
15:52:08 app.api.v1.agent INFO   [Stream] Task started: 获取《一夕千悟，从杂役弟子开始》第一章内容
15:52:08 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
15:52:08 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 百年关，天机变
15:52:08 app.api.v1.agent INFO   [Stream] 任务完成: 获取《一夕千悟，从杂役弟子开始》第一章内容 (0.0s)
15:52:08 app.api.v1.agent INFO   [Stream] Task started: 获取《一夕千悟，从杂役弟子开始》第二章内容
15:52:08 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
15:52:09 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第2章: 道祖出关，太极震群魔
15:52:09 app.api.v1.agent INFO   [Stream] 任务完成: 获取《一夕千悟，从杂役弟子开始》第二章内容 (0.1s)
15:52:09 app.api.v1.agent INFO   [Stream] Task started: 获取《一夕千悟，从杂役弟子开始》第三章内容
15:52:09 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
15:52:09 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第3章: 下山
15:52:09 app.api.v1.agent INFO   [Stream] 任务完成: 获取《一夕千悟，从杂役弟子开始》第三章内容 (0.0s)
15:52:09 app.api.v1.agent INFO   [Stream] Task started: 获取《一夕千悟，从杂役弟子开始》第四章内容
15:52:09 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
15:52:09 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第4章: 荒村孤烟，道祖传心
15:52:09 app.api.v1.agent INFO   [Stream] 任务完成: 获取《一夕千悟，从杂役弟子开始》第四章内容 (0.1s)
15:52:09 app.api.v1.agent INFO   [Stream] Task started: 获取《一夕千悟，从杂役弟子开始》第五章内容
15:52:09 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
15:52:09 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第5章: 一饭之恩，乱世人心
15:52:09 app.api.v1.agent INFO   [Stream] 任务完成: 获取《一夕千悟，从杂役弟子开始》第五章内容 (0.2s)
15:52:09 app.api.v1.agent INFO   [Stream] Task started: 深度分析前5章内容：人物关系、能力体系、世界观、伏笔
15:52:09 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
15:52:09 app.prompts.constraint_manager INFO   ✅ 已加载模板: analyze_text (v3.1.0)
15:52:09 app.prompts.constraint_manager INFO   ✅ 已加载模板: creative_writing (v1.0.0)
15:52:09 app.prompts.constraint_manager INFO   ✅ 已加载模板: intent_classifier (v2.0.0)
15:52:09 app.prompts.constraint_manager INFO   ✅ 已加载模板: planning_agent (v2.0.0)
15:52:09 app.prompts.constraint_manager INFO   ✅ 已加载模板: query_agent (v2.0.0)
15:52:09 app.prompts.constraint_manager INFO   ✅ 已加载模板: system_agent (v2.0.0)
15:52:09 app.prompts.constraint_manager INFO   ✅ 已加载模板: tool_agent (v2.0.0)
15:52:09 app.prompts.constraint_manager INFO   ✅ 已加载模板: writing_agent (v2.0.0)
15:52:09 app.prompts.constraint_manager INFO   ✅ 约束提示词管理器已初始化: 加载8个模板, 注册0个验证器
15:52:09 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
15:52:09 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
15:52:09 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
15:52:13 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
15:52:21 app.services.ai.http_ai_service INFO   API 响应完成，共接收 41 个数据块，总长度: 6272
15:52:21 app.services.ai.http_ai_service INFO   流式响应Token统计: 7534 (prompt=4864, completion=2670)
15:52:21 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
15:52:21 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:实例): tokens=7534, cost=$0.032780, time=21342ms
15:52:21 app.services.redis_cache_service INFO   ✓ 结果已缓存: novel_analysis:v2:micro:a36d8e0f... (TTL: 604800秒)
15:52:21 app.services.ai.novel_micro_analysis INFO   章节 340878e8-73b6-4ed7-96eb-6aee60332f87 分析成功，提取事件数: 7
15:52:21 app.services.ai.novel_analysis_orchestrator INFO   [6/6] ✓ 分析完成: 嵩山少室，魔焰滔天 (21.6秒)
15:52:21 app.services.ai.novel_analysis_orchestrator INFO   ⚡ 并行分析完成: 成功 6/6 章
15:52:21 app.services.ai.novel_analysis_orchestrator INFO   💾 开始批量保存 6 个分析结果...
15:52:21 app.services.novel_analysis_service INFO   Batch saved 6 micro results for analysis 17960841-8343-44c6-a797-b8d076afd40a, total: 6
15:52:21 app.services.ai.novel_analysis_orchestrator INFO   ✅ 批量保存完成: 6 个结果
15:52:21 app.services.ai.novel_analysis_orchestrator INFO   🔍 开始批量存储向量...
15:52:21 app.services.vector_store_service INFO   开始向量化章节 6481bdc8-3657-4aca-a638-af31744a57cf 的微观分析数据
15:52:22 app.services.vector_store_service INFO   生成向量维度: 384
15:52:22 app.services.vector_store_service INFO   向量存储成功: vector_id=3154d820-d6e4-42ff-b7d0-3609e3052d04
15:52:22 app.services.vector_store_service INFO   开始向量化章节 6c02b0db-0a67-4d6e-a27f-86e3c7ff7289 的微观分析数据
15:52:22 app.services.vector_store_service INFO   生成向量维度: 384
15:52:22 app.services.vector_store_service INFO   向量存储成功: vector_id=49288b06-6fc7-4605-bf54-04dcbd59d12b
15:52:22 app.services.vector_store_service INFO   开始向量化章节 c285feff-d240-4cfd-8bda-a05bb79af50b 的微观分析数据
15:52:24 app.services.vector_store_service INFO   生成向量维度: 384
15:52:24 app.services.vector_store_service INFO   向量存储成功: vector_id=97fa9ff8-b66f-4ffe-bf2a-77b15dc9156c
15:52:24 app.services.vector_store_service INFO   开始向量化章节 9d18cb2b-3210-4235-a6a0-635af73db118 的微观分析数据
15:52:25 app.services.vector_store_service INFO   生成向量维度: 384
15:52:25 app.services.vector_store_service INFO   向量存储成功: vector_id=c824ad11-2834-49fd-ae43-063a9ef4dc2e
15:52:25 app.services.vector_store_service INFO   开始向量化章节 04889237-7067-4527-88b1-c5232a5bd47c 的微观分析数据
15:52:26 app.services.vector_store_service INFO   生成向量维度: 384
15:52:26 app.services.vector_store_service INFO   向量存储成功: vector_id=b76f7791-e837-4636-9893-f8c8c081fe0a
15:52:26 app.services.vector_store_service INFO   开始向量化章节 340878e8-73b6-4ed7-96eb-6aee60332f87 的微观分析数据
15:52:27 app.services.vector_store_service INFO   生成向量维度: 384
15:52:27 app.services.vector_store_service INFO   向量存储成功: vector_id=452550c6-8da4-430c-aec0-b7f57e023228
15:52:27 app.services.ai.novel_analysis_orchestrator INFO   ✅ 批量向量存储完成
15:52:27 app.services.ai.novel_analysis_orchestrator INFO   ============================================================
15:52:27 app.services.ai.novel_analysis_orchestrator INFO   微观分析完成统计:
15:52:27 app.services.ai.novel_analysis_orchestrator INFO     成功: 6/6 章节 (100.0%)
15:52:27 app.services.ai.novel_analysis_orchestrator INFO     失败: 0 章节
15:52:27 app.services.ai.novel_analysis_orchestrator INFO     总耗时: 69.4秒 (平均 11.6秒/章)
15:52:27 app.services.ai.novel_analysis_orchestrator INFO   ============================================================
15:52:27 app.services.novel_analysis_service INFO   Updated analysis 17960841-8343-44c6-a797-b8d076afd40a progress: 6/6, stage: AnalysisStage.MACRO_ANALYSIS, status: None
15:52:27 app.services.ai.novel_analysis_orchestrator INFO   ============================================================
15:52:27 app.services.ai.novel_analysis_orchestrator INFO   开始宏观分析...
15:52:27 app.services.ai.novel_analysis_orchestrator INFO   ============================================================
15:52:27 app.services.ai.novel_macro_analysis INFO   开始宏观分析，共 6 个章节的数据，44 个事件
15:52:27 app.services.ai.novel_macro_analysis INFO   第 1/3 次尝试调用AI宏观分析
15:52:27 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
15:52:27 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
15:52:27 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=6000, temp=0.5, task_type=TaskType.SUMMARIZATION
15:52:30 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
15:52:40 app.services.ai.http_ai_service INFO   API 响应完成，共接收 39 个数据块，总长度: 3312
15:52:40 app.services.ai.http_ai_service INFO   流式响应Token统计: 16725 (prompt=14218, completion=2507)
15:52:40 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
15:52:40 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=16725, cost=$0.042843, time=30254ms
15:52:40 app.services.agent.langgraph_agent INFO   ✅ [Agent分析] 分析完成，结果长度: 3312
15:52:40 app.api.v1.agent INFO   [Stream] 任务完成: 深度分析前5章内容：人物关系、能力体系、世界观、伏笔 (30.7s)
15:52:40 app.services.agent.deep_agent.reflection INFO   [Checkpoint] 任务 6 标记了 checkpoint，触发反思
15:52:40 app.services.agent.deep_agent.executor INFO   任务 6 触发反思检查点
15:52:40 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=500, temp=0.3, task_type=None
15:52:42 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
15:52:53 app.services.ai.http_ai_service INFO   API 响应完成，共接收 35 个数据块，总长度: 2851
15:52:53 app.services.ai.http_ai_service INFO   流式响应Token统计: 20439 (prompt=18128, completion=2311)
15:52:53 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
15:52:53 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:实例): tokens=20439, cost=$0.045770, time=25804ms
15:52:53 app.services.ai.novel_macro_analysis INFO   宏观分析完成，报告长度: 2851 字符
15:52:53 app.services.ai.novel_analysis_orchestrator INFO   宏观分析完成，报告长度: 2851 字符，耗时: 25.9秒
15:52:53 app.services.novel_analysis_service INFO   Saved macro result for analysis 17960841-8343-44c6-a797-b8d076afd40a, marked as completed
15:52:53 app.services.ai.novel_analysis_orchestrator INFO   ============================================================
15:52:53 app.services.ai.novel_analysis_orchestrator INFO   作品 9398f47b-1e74-4e1c-93dd-e837e51dbaaf 分析全部完成！
15:52:53 app.services.ai.novel_analysis_orchestrator INFO   ============================================================
15:52:53 app.services.ai.novel_analysis_orchestrator INFO   📊 分析统计:
15:52:53 app.services.ai.novel_analysis_orchestrator INFO     微观分析: 6/6 章 (成功率 100.0%)
15:52:53 app.services.ai.novel_analysis_orchestrator INFO     宏观报告: 2851 字符
15:52:53 app.services.ai.novel_analysis_orchestrator INFO     总耗时: 95.3秒 (1.6分钟)
15:52:53 app.services.ai.novel_analysis_orchestrator INFO     平均速度: 15.9秒/章
15:52:53 app.services.ai.novel_analysis_orchestrator INFO     向量存储: 6 条，覆盖 6 章
15:52:53 app.services.ai.novel_analysis_orchestrator INFO   ============================================================
15:52:53 app.services.ai.novel_analysis_orchestrator INFO   AI服务资源已清理
15:52:53 app.services.ai.novel_analysis_orchestrator INFO   AI服务资源已清理
15:52:53 app.api.v1.novel_analysis INFO   后台任务完成：作品 9398f47b-1e74-4e1c-93dd-e837e51dbaaf 分析成功
15:52:54 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 68
15:52:54 app.services.ai.http_ai_service INFO   流式响应Token统计: 1796 (prompt=1753, completion=43)
15:52:54 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
15:52:54 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1796, cost=$0.002621, time=13865ms
15:52:54 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=1796
15:52:54 app.services.agent.deep_agent.reflection INFO   [Reflection] 解析结果: needs_replan=True, first_line=REPLAN:YES, raw_len=68
15:52:54 app.services.agent.deep_agent.executor INFO   反思结果需要重规划 (第 1 次)
15:52:54 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=800, temp=0.2, task_type=None
15:52:57 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
15:53:06 app.services.ai.http_ai_service INFO   API 响应完成，共接收 2 个数据块，总长度: 204
15:53:06 app.services.ai.http_ai_service INFO   流式响应Token统计: 1317 (prompt=1221, completion=96)
15:53:06 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
15:53:06 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1317, cost=$0.002486, time=11962ms
15:53:06 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=1317
15:53:06 app.api.v1.agent INFO   [Stream] Plan tasks: 9 items
15:53:06 app.services.agent.deep_agent.executor INFO   计划已更新，新任务数: 3
15:53:06 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=200, temp=0.1, task_type=None
15:53:08 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
15:53:16 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 123
15:53:16 app.services.ai.http_ai_service INFO   流式响应Token统计: 1353 (prompt=1294, completion=59)
15:53:16 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
15:53:16 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1353, cost=$0.002208, time=10327ms
15:53:16 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=1353
15:53:16 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] 从 3 个任务结果中提取文本，总长度: 9743 字符
15:53:16 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] AI 推断成功: '深化前5章分析：聚焦能力体系、人物关系及伏笔...' → tool=analyze_text_tool
15:53:16 app.api.v1.agent INFO   [Stream] Task started: 深化前5章分析：聚焦能力体系、人物关系及伏笔
15:53:16 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
15:53:16 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
15:53:16 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
15:53:16 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
15:53:18 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
15:53:47 app.services.ai.http_ai_service INFO   API 响应完成，共接收 45 个数据块，总长度: 3951
15:53:47 app.services.ai.http_ai_service INFO   流式响应Token统计: 14024 (prompt=11081, completion=2943)
15:53:47 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
15:53:47 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=14024, cost=$0.043281, time=31093ms
15:53:47 app.services.agent.langgraph_agent INFO   ✅ [Agent分析] 分析完成，结果长度: 3951
15:53:47 app.api.v1.agent INFO   [Stream] 任务完成: 深化前5章分析：聚焦能力体系、人物关系及伏笔 (31.2s)
15:53:47 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=200, temp=0.1, task_type=None
15:53:50 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
15:54:07 app.services.agent.deep_agent.task_enricher WARNING   [TaskEnricher] AI 推断超时
15:54:07 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] 从 3 个任务结果中提取文本，总长度: 10090 字符
15:54:07 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] 规则匹配成功: '整合深化分析结果，构建故事核心要素文档...' → tool=analyze_text_tool
15:54:07 app.api.v1.agent INFO   [Stream] Task started: 整合深化分析结果，构建故事核心要素文档
15:54:07 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
15:54:07 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
15:54:07 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
15:54:07 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
15:54:09 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
15:54:33 app.services.ai.http_ai_service INFO   API 响应完成，共接收 39 个数据块，总长度: 3507
15:54:33 app.services.ai.http_ai_service INFO   流式响应Token统计: 13139 (prompt=10598, completion=2541)
15:54:33 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
15:54:33 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=13139, cost=$0.038657, time=25340ms
15:54:33 app.services.agent.langgraph_agent INFO   ✅ [Agent分析] 分析完成，结果长度: 3507
15:54:33 app.api.v1.agent INFO   [Stream] 任务完成: 整合深化分析结果，构建故事核心要素文档 (25.4s)
15:54:33 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=200, temp=0.1, task_type=None
15:54:35 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
15:54:40 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 94
15:54:40 app.services.ai.http_ai_service INFO   流式响应Token统计: 983 (prompt=940, completion=43)
15:54:40 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
15:54:40 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=983, cost=$0.001605, time=7618ms
15:54:40 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=983
15:54:40 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] 从 3 个任务结果中提取文本，总长度: 10774 字符
15:54:40 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] AI 推断成功: '基于新的分析结果，规划第6-10章详细大纲...' → tool=analyze_text_tool
15:54:40 app.api.v1.agent INFO   [Stream] Task started: 基于新的分析结果，规划第6-10章详细大纲
15:54:40 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
15:54:40 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
15:54:40 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
15:54:40 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
15:54:43 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
15:55:00 app.services.ai.http_ai_service INFO   API 响应完成，共接收 63 个数据块，总长度: 5477
15:55:00 app.services.ai.http_ai_service INFO   流式响应Token统计: 13640 (prompt=9505, completion=4135)
15:55:00 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
15:55:00 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=13640, cost=$0.053231, time=19939ms
15:55:00 app.services.agent.langgraph_agent INFO   ✅ [Agent分析] 分析完成，结果长度: 5477
15:55:00 app.api.v1.agent INFO   [Stream] 任务完成: 基于新的分析结果，规划第6-10章详细大纲 (20.0s)
15:55:00 app.services.agent.deep_agent.executor INFO   DeepAgent 执行完成: 任务=9, 反思=1, 重规划=1
15:55:00 app.services.agent.langgraph_agent INFO   [DeepAgent] 执行完成: 反思=1次, 重规划=1次
15:55:00 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共9个任务，耗时: 171.81s
15:55:00 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
15:55:00 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=0, 输出型=4, 展示型=5
15:55:00 app.services.agent.langgraph_agent INFO   [Response] 4个输出任务，简单拼接
15:55:01 app.api.v1.agent INFO   [Stream] 跳过最终响应（内容已流式发送）
15:55:01 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed