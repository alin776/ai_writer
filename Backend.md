20:23:27 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: planning, Message: 请为第二章写一篇10000字的深度分析报告...
20:23:27 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
20:23:27 app.services.ai.http_ai_service INFO   ModelSelector 已启用
20:23:27 app.services.ai.http_ai_service INFO   [成本追踪] 初始化未传db/user_id，将使用请求上下文按需记录成本
20:23:29 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
20:23:29 app.services.agent.tools.writing_tools INFO   Writing tools AI service initialized
20:23:29 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ AI Service 已同时设置到 langgraph_tools 和 writing_tools
20:23:29 app.services.context.adaptive_budget INFO   ✅ 所有预算配置验证通过
20:23:39 app.services.context.vector_memory_store INFO   ✅ VectorMemoryStore初始化成功 | 目录=./data/chroma_db | 模型=paraphrase-multilingual-MiniLM-L12-v2 | 集合=user_memories
20:23:39 app.services.context.manager INFO   ✅ VectorMemoryStore 已初始化
20:23:39 app.services.context.manager INFO   ✅ ContextManager: 长期记忆已启用 (user_id=None)
20:23:39 app.services.context.manager INFO   ✅ ContextManager: 自适应预算已启用
20:23:39 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ ContextManager已初始化（长期记忆已启用，自适应预算已启用，总预算=16000 tokens）
成功加载模板: analyze_text (版本 3.1.0)
成功加载模板: intent_classifier (版本 2.0.0)
成功加载模板: writing_agent (版本 2.0.0)
成功加载模板: planning_agent (版本 2.0.0)
成功加载模板: tool_agent (版本 2.0.0)
成功加载模板: query_agent (版本 2.0.0)
成功加载模板: system_agent_prompt (版本 2.0.0)
成功加载模板: creative_writing_prompt (版本 1.0.0)
20:23:39 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ PromptManager已初始化
20:23:39 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ Redis连接验证成功
20:23:39 app.services.agent.langgraph_agent INFO   [LangGraph] OK 使用 AsyncRedisSaver（redis://localhost:6379/0，TTL=7天）
20:23:39 app.services.agent.memory.metrics INFO   [MemoryMetrics] 监控系统已初始化
20:23:39 app.services.agent.memory.long_term_store INFO   [LongTermStore] Initialized: base_dir=./data/long_term_memory, max_size=50KB, compression=True
20:23:39 app.services.agent.memory.enhanced_memory_manager INFO   EnhancedMemoryManager initialized: short=10, medium=100, threshold=0.1, long_term_backup=enabled
20:23:39 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ EnhancedMemoryManager已创建
20:23:39 app.services.agent.memory.unified_coordinator INFO   [UnifiedMemoryCoordinator] 初始化统一记忆协调器
20:23:39 app.services.agent.memory.unified_coordinator INFO   [UnifiedMemoryCoordinator] 全局实例已设置
20:23:39 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ UnifiedMemoryCoordinator已初始化 | checkpointer=AsyncRedisSaver | enhanced_memory=yes | context_manager=yes
20:23:39 app.services.agent.parallel_tool_node INFO   [ParallelToolNode] 初始化完成，最大并发数=5，并行安全工具=4个
20:23:39 app.api.v1.agent INFO   [Global Agent] created global agent instance; MemorySaver shared across requests
20:23:39 app.api.v1.agent INFO   [agent_chat_stream] 📥 收到的 context 字段:
20:23:39 app.api.v1.agent INFO     - selected_text: N/A...
20:23:39 app.api.v1.agent INFO     - selection_position: N/A
20:23:39 app.api.v1.agent INFO     - chapter_context: 当前章节ID: 671fca0b-5c00-471e-ae49-d076c5d0c637...
20:23:39 app.api.v1.agent INFO     - instruction_context: N/A...
20:23:39 app.services.agent.langgraph_agent INFO   [Planning] 使用隔离的thread_id: 602f5147-846a-4cde-95d3-405fa75f133f:738a636e-191d-45dd-8f41-1bb7c08e8c9c:16533812-d548-4457-ae76-07252df3a548 (user_id=602f5147-846a-4cde-95d3-405fa75f133f, work_id=738a636e-191d-45dd-8f41-1bb7c08e8c9c, conversation_id=16533812-d548-4457-ae76-07252df3a548)
20:23:39 app.services.context.monitoring_integration INFO   ✅ ContextManager监控收集器已初始化
20:23:39 app.services.context.store INFO   [ContextStore] Redis连接成功
20:23:39 app.services.context.manager INFO   [ContextManager] 创建新上下文: 602f5147-846a-4cde-95d3-405fa75f133f:738a636e-191d-45dd-8f41-1bb7c08e8c9c:16533812-d548-4457-ae76-07252df3a548
20:23:39 app.services.context.token_counter INFO   ✅ tiktoken初始化成功，模型: gemini-2.5-pro -> cl100k_base
20:23:39 app.services.context.manager INFO   [ContextManager] Session 602f5147-846a-4cde-95d3-405fa75f133f:738a636e-191d-45dd-8f41-1bb7c08e8c9c:16533812-d548-4457-ae76-07252df3a548: 0/16000 tokens
20:23:41 app.services.context.vector_memory_store INFO   🔍 检索记忆 | 查询='请为第二章写一篇10000字的深度分析报告...' | 隔离键=['user:602f5147-846a-4cde-95d3-405fa75f133f:work:738a636e-191d-45dd-8f41-1bb7c08e8c9c', 'user:602f5147-846a-4cde-95d3-405fa75f133f'] | 找到=3条
20:23:41 app.services.context.manager INFO   🔍 检索长期记忆 | 级别=work | work_id=738a636e-191d-45dd-8f41-1bb7c08e8c9c | 含用户级=True | 找到=3条
20:23:41 app.services.context.monitoring_integration INFO   [Monitor] 上下文构建: 1条消息, 0 tokens, 耗时 2600.64ms
20:23:41 app.services.agent.langgraph_agent INFO   [Planning] 从 ContextManager 加载了 1 条历史消息 (token: 0)
20:23:41 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: 请为第二章写一篇10000字的深度分析报告...
20:23:41 app.core.cache INFO   ✅ 缓存命中: prompt:planning_agent:v2.12.0:get_planning_agent_mode_prompt:fca6eb91156619d0
20:23:41 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
20:23:41 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
20:23:41 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=2000, temp=0.3, task_type=TaskType.SIMPLE_QA
20:23:44 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
20:23:46 app.services.ai.http_ai_service INFO   API 响应完成，共接收 15 个数据块，总长度: 1262
20:23:46 app.services.ai.http_ai_service INFO   流式响应Token统计: 6163 (prompt=5525, completion=638)
20:23:46 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
20:23:47 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
20:23:47 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=6163, cost=$0.013286, time=4991ms
20:23:47 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=6163
20:23:47 app.services.agent.langgraph_agent INFO   [JSON解析] 方法2成功: 从```json块提取
20:23:47 app.services.agent.langgraph_agent INFO   [Planning] 思维链: 输出=用户期望看到一份关于第二章的深度分析报告，内容需要达到100, 原料=需要第二章的全部内容，以及可能需要作品的, 处理=获取第二章内容后，需要对内容进行深度分析
20:23:47 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共2个任务，耗时: 5.14s
20:23:47 app.api.v1.agent INFO   [Stream] Plan tasks: 2 items
20:23:47 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
20:23:47 app.services.agent.langgraph_agent INFO   [DeepAgent] 启用反思模式
20:23:47 app.services.agent.parameter_resolver INFO   [ParameterResolver] 初始化完成, 严格模式: False
20:23:47 app.services.agent.langgraph_agent INFO   [DeepAgent] ParameterResolver 已启用
20:23:47 app.services.agent.deep_agent.executor INFO   DeepAgent 开始执行，共 2 个任务，反思功能已启用
20:23:47 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] AI 推断功能已启用
20:23:47 app.api.v1.agent INFO   [Stream] Task started: 获取第二章的全部内容。
20:23:47 app.services.agent.langgraph_agent INFO   [_execute_task] 调用 registry.call_tool(get_chapter_by_order)
20:23:47 app.services.agent.tools.tool_types INFO   [get_chapter_by_order] 开始执行工具
20:23:47 app.services.agent.langgraph_tools INFO   [get_chapter_by_order_tool] ✅ 找到第2章: 第二章 夜航
20:23:47 app.services.agent.tools.tool_types INFO   [get_chapter_by_order] 执行成功 (耗时: 0.069s)
20:23:47 app.services.agent.tools.tool_monitor INFO   ToolMonitor initialized with Memory storage, retention: 7 days
20:23:47 app.services.agent.langgraph_agent INFO   [StandardTool] get_chapter_by_order 执行成功（DeepAgent模式）
20:23:47 app.api.v1.agent INFO   [Stream] 任务完成: 获取第二章的全部内容。 (0.1s)
20:23:47 app.services.agent.deep_agent.reflection INFO   [Checkpoint] 首个任务 1 未标记 checkpoint，触发一次兜底反思以校验规划
20:23:47 app.services.agent.deep_agent.executor INFO   任务 1 触发反思检查点
20:23:47 app.services.agent.deep_agent.reflection INFO   [DeepAgent反思] 开始调用 AI，task_id=1
20:23:47 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
20:23:47 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
20:23:47 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=500, temp=0.3, task_type=TaskType.SIMPLE_QA
20:23:47 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
20:23:47 app.services.ai.http_ai_service INFO   API 响应完成，共接收 3 个数据块，总长度: 93
20:23:47 app.services.ai.http_ai_service INFO   流式响应Token统计: 1259 (prompt=1212, completion=47)
20:23:47 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
20:23:47 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
20:23:48 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1259, cost=$0.001985, time=811ms
20:23:48 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=1259
20:23:48 app.services.agent.deep_agent.reflection INFO   [Reflection] JSON解析成功: needs_replan=False
20:23:48 app.api.v1.agent INFO   [Stream] Task started: 基于第二章的内容，撰写一份10000字的深度分析报告。
20:23:48 app.services.agent.langgraph_agent INFO   [_execute_task] 调用 registry.call_tool(continue_writing)
20:23:48 app.services.agent.tools.tool_types INFO   [continue_writing] 开始执行工具
20:23:48 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: complex
20:23:48 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=content_creation, 模型=gemini-2.5-pro, 原因=任务复杂度为 complex; 任务类型: content_creation; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
20:23:48 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=1000, temp=0.8, task_type=TaskType.CONTENT_CREATION
20:24:13 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
20:24:17 app.services.ai.http_ai_service INFO   API 响应完成，共接收 9 个数据块，总长度: 692
20:24:17 app.services.ai.http_ai_service INFO   流式响应Token统计: 6803 (prompt=6255, completion=548)
20:24:17 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
20:24:17 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
20:24:17 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=6803, cost=$0.013299, time=29731ms
20:24:17 app.services.agent.tools.tool_types INFO   [continue_writing] 执行成功 (耗时: 29.806s)
20:24:17 app.services.agent.langgraph_agent INFO   [StandardTool] continue_writing 执行成功（DeepAgent模式）
20:24:17 app.api.v1.agent INFO   [Stream] 任务完成: 基于第二章的内容，撰写一份10000字的深度分析报告。 (29.8s)
20:24:17 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
20:24:17 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
20:24:17 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=200, temp=0.1, task_type=TaskType.SIMPLE_QA
20:24:18 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
20:24:19 app.services.ai.http_ai_service INFO   API 响应完成，共接收 5 个数据块，总长度: 117
20:24:19 app.services.ai.http_ai_service INFO   流式响应Token统计: 910 (prompt=844, completion=66)
20:24:19 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
20:24:19 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
20:24:19 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=910, cost=$0.001715, time=1314ms
20:24:19 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=910
20:24:19 app.services.agent.deep_agent.executor INFO   [验收] 结果: 未通过, 摘要: 生成内容字数远低于8000字阈值，不满足深度分析报告的要求。
20:24:19 app.services.agent.deep_agent.executor INFO   [FinalCheck] 末尾校验未通过，追加补救任务
20:24:19 app.services.agent.deep_agent.reflection INFO   [DeepAgent反思] 开始调用 AI，task_id=2
20:24:19 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
20:24:19 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
20:24:19 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=500, temp=0.3, task_type=TaskType.SIMPLE_QA
20:24:19 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
20:24:20 app.services.ai.http_ai_service INFO   API 响应完成，共接收 3 个数据块，总长度: 95
20:24:20 app.services.ai.http_ai_service INFO   流式响应Token统计: 1287 (prompt=1235, completion=52)
20:24:20 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
20:24:20 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
20:24:20 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1287, cost=$0.002064, time=1024ms
20:24:20 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=1287
20:24:20 app.services.agent.deep_agent.reflection INFO   [Reflection] JSON解析成功: needs_replan=False
20:24:20 app.api.v1.agent INFO   [Stream] Plan tasks: 3 items
20:24:20 app.api.v1.agent INFO   [Stream] Task started: 补充/修正前一任务结果，确保满足：10000字
20:24:20 app.services.agent.langgraph_agent INFO   [_execute_task] 调用 registry.call_tool(continue_writing)
20:24:20 app.services.agent.tools.tool_types INFO   [continue_writing] 开始执行工具
20:24:20 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: complex
20:24:20 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=content_creation, 模型=gemini-2.5-pro, 原因=任务复杂度为 complex; 任务类型: content_creation; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
20:24:20 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=1000, temp=0.8, task_type=TaskType.CONTENT_CREATION
20:24:47 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
20:24:52 app.services.ai.http_ai_service INFO   API 响应完成，共接收 12 个数据块，总长度: 916
20:24:52 app.services.ai.http_ai_service INFO   流式响应Token统计: 7267 (prompt=6558, completion=709)
20:24:52 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
20:24:52 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
20:24:52 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=7267, cost=$0.015287, time=31975ms
20:24:52 app.services.agent.tools.tool_types INFO   [continue_writing] 执行成功 (耗时: 32.037s)
20:24:52 app.services.agent.langgraph_agent INFO   [StandardTool] continue_writing 执行成功（DeepAgent模式）
20:24:52 app.api.v1.agent INFO   [Stream] 任务完成: 补充/修正前一任务结果，确保满足：10000字 (32.0s)
20:24:52 app.services.agent.deep_agent.executor INFO   DeepAgent 执行完成: 任务=3, 反思=2, 重规划=0
20:24:52 app.services.agent.langgraph_agent INFO   [DeepAgent] 执行完成: 反思=2次, 重规划=0次
20:24:52 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共3个任务，耗时: 65.23s
20:24:52 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
20:24:52 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=0, 输出型=2, 展示型=1
20:24:52 app.services.agent.langgraph_agent INFO   [Response] 2个输出任务，简单拼接
20:24:54 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 隔离=work:738a636e-191d-45dd-8f41-1bb7c08e8c9c | 重要度=0.68
20:24:54 app.services.context.store INFO   [ContextStore] 保存上下文: 602f5147-846a-4cde-95d3-405fa75f133f:738a636e-191d-45dd-8f41-1bb7c08e8c9c:16533812-d548-4457-ae76-07252df3a548, token=2265
20:24:54 app.services.context.manager INFO   [ContextManager] 更新上下文: 602f5147-846a-4cde-95d3-405fa75f133f:738a636e-191d-45dd-8f41-1bb7c08e8c9c:16533812-d548-4457-ae76-07252df3a548, 消息数=2, Token=2265
20:24:54 app.services.agent.langgraph_agent INFO   [Planning] 已保存对话到 ContextManager (session=602f5147-846a-4cde-95d3-405fa75f133f:738a636e-191d-45dd-8f41-1bb7c08e8c9c:16533812-d548-4457-ae76-07252df3a548)
20:24:54 app.api.v1.agent INFO   [Stream] 跳过最终响应（内容已流式发送）
20:24:54 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed