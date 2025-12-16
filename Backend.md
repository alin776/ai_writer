00:01:52 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ AI Service 已同时设置到 langgraph_tools 和 writing_tools
00:01:52 app.services.context.adaptive_budget INFO   ✅ 所有预算配置验证通过
00:02:00 app.services.context.vector_memory_store INFO   ✅ VectorMemoryStore初始化成功 | 目录=./data/chroma_db | 模型=paraphrase-multilingual-MiniLM-L12-v2 | 集合=user_memories
00:02:00 app.services.context.manager INFO   ✅ VectorMemoryStore 已初始化
00:02:00 app.services.context.manager INFO   ✅ ContextManager: 长期记忆已启用 (user_id=None)
00:02:00 app.services.context.manager INFO   ✅ ContextManager: 自适应预算已启用
00:02:00 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ ContextManager已初始化（长期记忆已启用，自适应预算已启用，总预算=16000 tokens）
成功加载模板: analyze_text (版本 3.1.0)
成功加载模板: intent_classifier (版本 2.0.0)
成功加载模板: writing_agent (版本 2.0.0)
成功加载模板: planning_agent (版本 2.0.0)
成功加载模板: tool_agent (版本 2.0.0)
成功加载模板: query_agent (版本 2.0.0)
成功加载模板: system_agent_prompt (版本 2.0.0)
成功加载模板: creative_writing_prompt (版本 1.0.0)
00:02:00 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ PromptManager已初始化
00:02:00 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ Redis连接验证成功
00:02:00 app.services.agent.langgraph_agent INFO   [LangGraph] OK 使用 AsyncRedisSaver（redis://localhost:6379/0，TTL=7天）
00:02:00 app.services.agent.memory.metrics INFO   [MemoryMetrics] 监控系统已初始化
00:02:00 app.services.agent.memory.long_term_store INFO   [LongTermStore] Initialized: base_dir=./data/long_term_memory, max_size=50KB, compression=True
00:02:00 app.services.agent.memory.enhanced_memory_manager INFO   EnhancedMemoryManager initialized: short=10, medium=100, threshold=0.1, long_term_backup=enabled
00:02:00 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ EnhancedMemoryManager已创建
00:02:00 app.services.agent.memory.unified_coordinator INFO   [UnifiedMemoryCoordinator] 初始化统一记忆协调器
00:02:00 app.services.agent.memory.unified_coordinator INFO   [UnifiedMemoryCoordinator] 全局实例已设置
00:02:00 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ UnifiedMemoryCoordinator已初始化 | checkpointer=AsyncRedisSaver | enhanced_memory=yes | context_manager=yes
00:02:00 app.services.agent.parallel_tool_node INFO   [ParallelToolNode] 初始化完成，最大并发数=5，并行安全工具=4个
00:02:00 app.api.v1.agent INFO   [Global Agent] created global agent instance; MemorySaver shared across requests
00:02:00 app.api.v1.agent INFO   [agent_chat_stream] 📥 收到的 context 字段:
00:02:00 app.api.v1.agent INFO     - selected_text: 而他，曾经的青云宗第一天才，如今却像一条死狗般躺在这里，丹田破碎，修为尽失，离死只差一步。 “呵呵……”叶尘的喉咙里发出一声沙哑的自嘲，牵动了胸口的伤势，又是一阵剧烈的咳嗽，鲜血顺着嘴角不断溢出。 三...
00:02:00 app.api.v1.agent INFO     - selection_position: {'from': 146, 'to': 311}
00:02:00 app.api.v1.agent INFO     - chapter_context: 当前章节ID: 05363a2e-cfc2-4532-b7f6-a1c61d6d44a0...
00:02:00 app.api.v1.agent INFO     - instruction_context: 用户选中了以下文本进行操作:
---
而他，曾经的青云宗第一天才，如今却像一条死狗般躺在这里，丹田破碎，修为尽失，离死只差一步。 “呵呵……”叶尘的喉咙里发出一声沙哑的自嘲，牵动了胸口的伤势，又是一阵...
00:02:00 app.services.agent.langgraph_agent INFO   [Planning] 使用隔离的thread_id: 602f5147-846a-4cde-95d3-405fa75f133f:22d5f90f-da38-4805-a5a7-4e891b62b076:7cf2dba8-d53a-4e91-a810-15c1791d6a99 (user_id=602f5147-846a-4cde-95d3-405fa75f133f, work_id=22d5f90f-da38-4805-a5a7-4e891b62b076, conversation_id=7cf2dba8-d53a-4e91-a810-15c1791d6a99)
00:02:00 app.services.context.monitoring_integration INFO   ✅ ContextManager监控收集器已初始化
00:02:00 app.services.context.store INFO   [ContextStore] Redis连接成功
00:02:00 app.services.context.store INFO   [ContextStore] 加载上下文: 602f5147-846a-4cde-95d3-405fa75f133f:22d5f90f-da38-4805-a5a7-4e891b62b076:7cf2dba8-d53a-4e91-a810-15c1791d6a99, 2条消息
00:02:00 app.services.context.token_counter INFO   ✅ tiktoken初始化成功，模型: gemini-2.5-pro -> cl100k_base
00:02:00 app.services.context.manager INFO   [ContextManager] Session 602f5147-846a-4cde-95d3-405fa75f133f:22d5f90f-da38-4805-a5a7-4e891b62b076:7cf2dba8-d53a-4e91-a810-15c1791d6a99: 724/16000 tokens
00:02:02 app.services.context.vector_memory_store INFO   🔍 检索记忆 | 查询='帮我写润色这段话...' | 隔离键=['user:602f5147-846a-4cde-95d3-405fa75f133f:work:22d5f90f-da38-4805-a5a7-4e891b62b076', 'user:602f5147-846a-4cde-95d3-405fa75f133f'] | 找到=1条
00:02:02 app.services.context.manager INFO   🔍 检索长期记忆 | 级别=work | work_id=22d5f90f-da38-4805-a5a7-4e891b62b076 | 含用户级=True | 找到=1条
00:02:02 app.services.context.monitoring_integration INFO   [Monitor] 上下文构建: 3条消息, 724 tokens, 耗时 1889.41ms
00:02:02 app.services.agent.langgraph_agent INFO   [Planning] 从 ContextManager 加载了 3 条历史消息 (token: 724)
00:02:02 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: 帮我写润色这段话...
00:02:02 app.core.cache INFO   ⚠️ 缓存未命中: prompt:planning_agent:v2.12.0:get_planning_agent_mode_prompt:fca6eb91156619d0
00:02:02 app.core.cache INFO   ✅ 缓存命中: prompt:planning:v2.12.0:get_planning_static_prompt:fca6eb91156619d0
00:02:02 app.core.cache INFO   💾 缓存已保存: prompt:planning_agent:v2.12.0:get_planning_agent_mode_prompt:fca6eb91156619d0 (expire=3600s)
00:02:02 app.services.agent.langgraph_agent INFO   [Planning] 注入选中文本到prompt: 而他，曾经的青云宗第一天才，如今却像一条死狗般躺在这里，丹田破碎，修为尽失，离死只差一步。 “呵呵…...
00:02:02 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
00:02:02 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
00:02:02 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=2000, temp=0.3, task_type=TaskType.SIMPLE_QA
00:02:04 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
00:02:06 app.services.ai.http_ai_service INFO   API 响应完成，共接收 12 个数据块，总长度: 968
00:02:06 app.services.ai.http_ai_service INFO   流式响应Token统计: 6683 (prompt=6164, completion=519)
00:02:06 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
00:02:06 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
00:02:06 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=6683, cost=$0.012895, time=3452ms
00:02:06 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=6683
00:02:06 app.services.agent.langgraph_agent INFO   [JSON解析] 方法1成功: 直接解析
00:02:06 app.services.agent.langgraph_agent INFO   [Planning] 思维链: 输出=用户希望对选中的文本进行润色，使其更具文学性和感染力，去除A, 原料=需要用户选中的文本内容，以及该文本所在的, 处理=首先读取用户选中的章节内容，然后使用an
00:02:06 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共2个任务，耗时: 3.56s
00:02:06 app.api.v1.agent INFO   [Stream] Plan tasks: 2 items
00:02:06 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
00:02:06 app.services.agent.langgraph_agent INFO   [DeepAgent] 启用反思模式
00:02:06 app.services.agent.parameter_resolver INFO   [ParameterResolver] 初始化完成, 严格模式: False
00:02:06 app.services.agent.langgraph_agent INFO   [DeepAgent] ParameterResolver 已启用
00:02:06 app.services.agent.deep_agent.executor INFO   DeepAgent 开始执行，共 2 个任务，反思功能已启用
00:02:06 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] AI 推断功能已启用
00:02:06 app.api.v1.agent INFO   [Stream] Task started: 读取当前章节内容以获取上下文
00:02:06 app.services.agent.langgraph_agent INFO   [_execute_task] 调用 registry.call_tool(read_chapter)
00:02:06 app.services.agent.tools.tool_types INFO   [read_chapter] 开始执行工具
00:02:06 app.services.agent.langgraph_tools INFO   [read_chapter_tool] ✅ 读取章节成功: 废物？神级签到系统！
00:02:06 app.services.agent.tools.tool_types INFO   [read_chapter] 执行成功 (耗时: 0.037s)
00:02:06 app.services.agent.tools.tool_monitor INFO   ToolMonitor initialized with Memory storage, retention: 7 days
00:02:06 app.services.agent.langgraph_agent INFO   [StandardTool] read_chapter 执行成功（DeepAgent模式）
00:02:06 app.api.v1.agent INFO   [Stream] 任务完成: 读取当前章节内容以获取上下文 (0.0s)
00:02:06 app.services.agent.deep_agent.reflection INFO   [Checkpoint] 首个任务 1 未标记 checkpoint，触发一次兜底反思以校验规划
00:02:06 app.services.agent.deep_agent.executor INFO   任务 1 触发反思检查点
00:02:06 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
00:02:06 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
00:02:06 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
00:02:06 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
00:02:06 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
00:02:06 app.services.ai.http_ai_service INFO   流式响应Token统计: 103 (prompt=102, completion=1)
00:02:06 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
00:02:06 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
00:02:06 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=103, cost=$0.000138, time=622ms
00:02:06 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=103
00:02:06 app.services.agent.deep_agent.reflection INFO   [DeepAgent反思] 开始调用 AI，task_id=1
00:02:06 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
00:02:06 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
00:02:06 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=500, temp=0.3, task_type=TaskType.SIMPLE_QA
00:02:07 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
00:02:08 app.services.ai.http_ai_service INFO   API 响应完成，共接收 5 个数据块，总长度: 90
00:02:08 app.services.ai.http_ai_service INFO   流式响应Token统计: 1227 (prompt=1185, completion=42)
00:02:08 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
00:02:08 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
00:02:08 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1227, cost=$0.001901, time=1180ms
00:02:08 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=1227
00:02:08 app.services.agent.deep_agent.reflection INFO   [Reflection] JSON解析成功: needs_replan=False
00:02:08 app.api.v1.agent INFO   [Stream] Task started: 分析选中的文本并给出润色建议
00:02:08 app.services.agent.langgraph_agent INFO   [_execute_task] analyze_text_tool 使用 focus: '分析文本的不足之处，并给出润色建议，使其更具文学性和感染力，去除AI痕迹。...'
00:02:08 app.services.agent.langgraph_agent INFO   [_execute_task] 调用 registry.call_tool(analyze_text)
00:02:08 app.services.agent.tools.tool_types INFO   [analyze_text] 开始执行工具
00:02:08 app.services.agent.tools.analysis_tools INFO   [analyze_text_tool] 尝试第 1 次调用，config={'temperature': 0.3, 'task_type': <TaskType.SUMMARIZATION: 'summarization'>}
00:02:08 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
00:02:08 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
00:02:08 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
00:02:16 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
00:02:20 app.services.ai.http_ai_service INFO   API 响应完成，共接收 10 个数据块，总长度: 852
00:02:20 app.services.ai.http_ai_service INFO   流式响应Token统计: 2134 (prompt=1479, completion=655)
00:02:20 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
00:02:20 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
00:02:20 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2134, cost=$0.008399, time=12084ms
00:02:20 app.services.agent.tools.analysis_tools INFO   [analyze_text_tool] 第 1 次调用成功
00:02:20 app.services.agent.tools.analysis_tools INFO   [analyze_text_tool] 分析完成，结果长度: 852
00:02:20 app.services.agent.tools.tool_types INFO   [analyze_text] 执行成功 (耗时: 12.112s)
00:02:20 app.services.agent.langgraph_agent INFO   [StandardTool] analyze_text 执行成功（DeepAgent模式）
00:02:20 app.api.v1.agent INFO   [Stream] 任务完成: 分析选中的文本并给出润色建议 (12.1s)
00:02:20 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
00:02:20 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
00:02:20 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
00:02:20 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
00:02:20 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
00:02:20 app.services.ai.http_ai_service INFO   流式响应Token统计: 105 (prompt=104, completion=1)
00:02:20 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
00:02:20 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
00:02:20 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=105, cost=$0.000140, time=644ms
00:02:20 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=105
00:02:20 app.services.agent.deep_agent.executor INFO   DeepAgent 执行完成: 任务=2, 反思=1, 重规划=0
00:02:20 app.services.agent.langgraph_agent INFO   [DeepAgent] 执行完成: 反思=1次, 重规划=0次
00:02:20 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共2个任务，耗时: 14.75s
00:02:20 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
00:02:20 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=0, 输出型=1, 展示型=1
00:02:20 app.services.agent.langgraph_agent INFO   [Response] 单个分析任务(analyze_text_tool)，使用AI格式化
00:02:20 app.services.agent.langgraph_agent INFO   [Summarization] 使用AI整合任务结果
00:02:20 app.services.agent.langgraph_agent INFO   [Summarization] 上下文处理: 原始=5604字符, 处理后=5637字符
00:02:20 app.services.agent.langgraph_agent INFO   [Summarization] 使用流式生成（_generate_text_stream）
00:02:20 app.services.agent.langgraph_agent INFO   [_generate_text_stream] 开始流式生成，buffer_size=1
00:02:20 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
00:02:20 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
00:02:20 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
00:02:33 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
00:02:46 app.services.ai.http_ai_service INFO   API 响应完成，共接收 55 个数据块，总长度: 4638
00:02:46 app.services.ai.http_ai_service INFO   流式响应Token统计: 9656 (prompt=6065, completion=3591)
00:02:46 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
00:02:46 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
00:02:46 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=9656, cost=$0.043491, time=25334ms
00:02:46 app.services.agent.langgraph_agent INFO   [_generate_text_stream] 流式生成完成，总长度=4638
00:02:47 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 隔离=work:22d5f90f-da38-4805-a5a7-4e891b62b076 | 重要度=0.65
00:02:49 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 隔离=work:22d5f90f-da38-4805-a5a7-4e891b62b076 | 重要度=0.60
00:02:49 app.services.context.store INFO   [ContextStore] 保存上下文: 602f5147-846a-4cde-95d3-405fa75f133f:22d5f90f-da38-4805-a5a7-4e891b62b076:7cf2dba8-d53a-4e91-a810-15c1791d6a99, token=6643
00:02:49 app.services.context.manager INFO   [ContextManager] 更新上下文: 602f5147-846a-4cde-95d3-405fa75f133f:22d5f90f-da38-4805-a5a7-4e891b62b076:7cf2dba8-d53a-4e91-a810-15c1791d6a99, 消息数=4, Token=6643
00:02:49 app.services.agent.langgraph_agent INFO   [Planning] 已保存对话到 ContextManager (session=602f5147-846a-4cde-95d3-405fa75f133f:22d5f90f-da38-4805-a5a7-4e891b62b076:7cf2dba8-d53a-4e91-a810-15c1791d6a99)
00:02:49 app.api.v1.agent INFO   [Stream] 跳过最终响应（内容已流式发送）
00:02:49 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed
