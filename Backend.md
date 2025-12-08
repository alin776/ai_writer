10:31:58 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: planning, Message: 根据前面的所有章节，来写出接下来的 五章 的大纲...
10:31:58 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
10:31:58 app.services.ai.http_ai_service INFO   ModelSelector 已启用
10:31:58 app.services.ai.http_ai_service INFO   [成本追踪] 初始化未传db/user_id，将使用请求上下文按需记录成本
10:32:01 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
10:32:01 app.services.context.adaptive_budget INFO   ✅ 所有预算配置验证通过
10:32:10 app.services.context.vector_memory_store INFO   ✅ VectorMemoryStore初始化成功 | 目录=./data/chroma_db | 模型=paraphrase-multilingual-MiniLM-L12-v2 | 集合=user_memories
10:32:10 app.services.context.manager INFO   ✅ VectorMemoryStore 已初始化
10:32:10 app.services.context.manager INFO   ✅ ContextManager: 长期记忆已启用 (user_id=None)
10:32:10 app.services.context.manager INFO   ✅ ContextManager: 自适应预算已启用
10:32:10 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ ContextManager已初始化（长期记忆已启用，自适应预算已启用，总预算=16000 tokens）
成功加载模板: intent_classifier (版本 2.0.0)
成功加载模板: writing_agent (版本 2.0.0)
成功加载模板: planning_agent (版本 2.0.0)
成功加载模板: tool_agent (版本 2.0.0)
成功加载模板: query_agent (版本 2.0.0)
成功加载模板: system_agent_prompt (版本 2.0.0)
成功加载模板: creative_writing_prompt (版本 1.0.0)
10:32:10 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ PromptManager已初始化
10:32:10 app.services.agent.langgraph_agent INFO   [LangGraph] 使用 HTTPAIService 模式（手动工具调用，绕过 Cloudflare）
10:32:10 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ Redis连接验证成功
10:32:10 app.services.agent.langgraph_agent INFO   [LangGraph] OK 使用 AsyncRedisSaver（redis://localhost:6379/0，TTL=7天）
10:32:10 app.services.agent.memory.metrics INFO   [MemoryMetrics] 监控系统已初始化
10:32:10 app.services.agent.memory.long_term_store INFO   [LongTermStore] Initialized: base_dir=./data/long_term_memory, max_size=50KB, compression=True
10:32:10 app.services.agent.memory.enhanced_memory_manager INFO   EnhancedMemoryManager initialized: short=10, medium=100, threshold=0.1, long_term_backup=enabled
10:32:10 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ EnhancedMemoryManager已创建
10:32:10 app.services.agent.memory.unified_coordinator INFO   [UnifiedMemoryCoordinator] 初始化统一记忆协调器
10:32:10 app.services.agent.memory.unified_coordinator INFO   [UnifiedMemoryCoordinator] 全局实例已设置
10:32:10 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ UnifiedMemoryCoordinator已初始化 | checkpointer=AsyncRedisSaver | enhanced_memory=yes | context_manager=yes
10:32:10 app.services.agent.parallel_tool_node INFO   [ParallelToolNode] 初始化完成，最大并发数=5，并行安全工具=4个
10:32:10 app.api.v1.agent INFO   [Global Agent] created global agent instance; MemorySaver shared across requests
10:32:10 app.services.agent.langgraph_agent INFO   [Planning] 使用隔离的thread_id: 9398f47b-1e74-4e1c-93dd-e837e51dbaaf:a833a199-7b1a-4610-ab64-f7beb0b947a1 (work_id=9398f47b-1e74-4e1c-93dd-e837e51dbaaf, conversation_id=a833a199-7b1a-4610-ab64-f7beb0b947a1)
10:32:10 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: 根据前面的所有章节，来写出接下来的 五章 的大纲...
10:32:10 app.core.cache INFO   ⚠️ 缓存未命中: prompt:get_planning_static_prompt:fca6eb91156619d0
10:32:10 app.core.cache INFO   💾 缓存已保存: prompt:get_planning_static_prompt:fca6eb91156619d0 (expire=3600s)
10:32:10 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
10:32:10 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
10:32:10 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=1200, temp=0.3, task_type=TaskType.SIMPLE_QA
10:32:12 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:32:19 app.services.ai.http_ai_service INFO   API 响应完成，共接收 7 个数据块，总长度: 848
10:32:19 app.services.ai.http_ai_service INFO   流式响应Token统计: 5195 (prompt=4786, completion=409)
10:32:20 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:32:20 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=5195, cost=$0.010072, time=9831ms
10:32:20 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=5195
10:32:20 app.services.agent.langgraph_agent INFO   [JSON解析] 方法2成功: 从```json块提取
10:32:20 app.services.agent.langgraph_agent INFO   [Planning] 思维链: 输出=用户期望看到一个接下来的五章内容的规划或大纲，而不是原文或摘, 原料=需要获取作品的所有历史章节内容作为规划的, 处理=获取所有历史章节内容后，使用 `anal
10:32:20 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共2个任务，耗时: 9.90s
10:32:20 app.api.v1.agent INFO   [Stream] Plan tasks: 2 items
10:32:20 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
10:32:20 app.services.agent.langgraph_agent INFO   [DeepAgent] 启用反思模式
10:32:20 app.services.agent.parameter_resolver INFO   [ParameterResolver] 初始化完成, 严格模式: False
10:32:20 app.services.agent.langgraph_agent INFO   [DeepAgent] ParameterResolver 已启用
10:32:20 app.services.agent.deep_agent.executor INFO   DeepAgent 开始执行，共 2 个任务，反思功能已启用
10:32:20 app.api.v1.agent INFO   [Stream] Task started: 获取作品的所有历史章节内容作为上下文
10:32:20 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
10:32:20 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=9398f47b-1e74-4e1c-93dd-e837e51dbaaf, chapter_id=6481bdc8-3657-4aca-a638-af31744a57cf
10:32:20 app.services.agent.langgraph_agent INFO   [get_context_tool] 当前章节order=1，将检索前0章
10:32:20 app.services.chapter_vector_service INFO   RAG检索: work_id=9398f47b-1e74-4e1c-93dd-e837e51dbaaf, current_order=1, query=作品背景、人物关系、情节发展、伏笔线索...
10:32:20 app.services.chapter_vector_service WARNING   ⚠️ 作品 9398f47b-1e74-4e1c-93dd-e837e51dbaaf 前0章暂无向量数据
10:32:20 app.services.agent.langgraph_agent WARNING   [get_context_tool] RAG检索为空，使用Worldview降级
10:32:20 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=天道一甲子：张三丰下山录
10:32:20 app.api.v1.agent INFO   [Stream] 任务完成: 获取作品的所有历史章节内容作为上下文 (0.0s)
10:32:20 app.api.v1.agent INFO   [Stream] Task started: 基于所有历史章节内容，规划接下来的五章大纲
10:32:20 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
10:32:20 app.prompts.constraint_manager INFO   ✅ 已加载模板: analyze_text (v3.1.0)
10:32:20 app.prompts.constraint_manager INFO   ✅ 已加载模板: creative_writing (v1.0.0)
10:32:20 app.prompts.constraint_manager INFO   ✅ 已加载模板: intent_classifier (v2.0.0)
10:32:20 app.prompts.constraint_manager INFO   ✅ 已加载模板: planning_agent (v2.0.0)
10:32:20 app.prompts.constraint_manager INFO   ✅ 已加载模板: query_agent (v2.0.0)
10:32:20 app.prompts.constraint_manager INFO   ✅ 已加载模板: system_agent (v2.0.0)
10:32:20 app.prompts.constraint_manager INFO   ✅ 已加载模板: tool_agent (v2.0.0)
10:32:20 app.prompts.constraint_manager INFO   ✅ 已加载模板: writing_agent (v2.0.0)
10:32:20 app.prompts.constraint_manager INFO   ✅ 约束提示词管理器已初始化: 加载8个模板, 注册0个验证器
10:32:20 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
10:32:20 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
10:32:20 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
10:32:24 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:32:56 app.services.ai.http_ai_service INFO   API 响应完成，共接收 53 个数据块，总长度: 4794
10:32:56 app.services.ai.http_ai_service INFO   流式响应Token统计: 8936 (prompt=5452, completion=3484)
10:32:56 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:32:56 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=8936, cost=$0.041655, time=36313ms
10:32:56 app.services.agent.langgraph_agent INFO   ✅ [Agent分析] 分析完成，结果长度: 4794
10:32:56 app.api.v1.agent INFO   [Stream] 任务完成: 基于所有历史章节内容，规划接下来的五章大纲 (0.0s)
10:32:56 app.services.agent.deep_agent.executor INFO   DeepAgent 执行完成: 任务=2, 反思=0, 重规划=0
10:32:56 app.services.agent.langgraph_agent INFO   [DeepAgent] 执行完成: 反思=0次, 重规划=0次
10:32:56 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共2个任务，耗时: 36.46s
10:32:56 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
10:32:56 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=1, 输出型=1, 展示型=0
10:32:56 app.services.agent.langgraph_agent INFO   [Response] 单个分析任务(analyze_text_tool)，使用AI格式化
10:32:56 app.services.agent.langgraph_agent INFO   [Summarization] 使用AI整合任务结果
10:32:56 app.services.agent.langgraph_agent INFO   [Summarization] 上下文压缩: 原始=8487字符, 压缩后=4122字符, 压缩率=52%
10:32:56 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
10:32:56 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
10:32:56 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
10:32:59 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
10:33:16 app.services.ai.http_ai_service INFO   API 响应完成，共接收 28 个数据块，总长度: 2432
10:33:16 app.services.ai.http_ai_service INFO   流式响应Token统计: 6801 (prompt=5013, completion=1788)
10:33:16 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
10:33:16 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=6801, cost=$0.024146, time=19702ms
10:33:16 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=6801
10:33:16 app.api.v1.agent INFO   [Stream] 跳过最终响应（内容已流式发送）
10:33:16 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed