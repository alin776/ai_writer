23:04:42 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: planning, Message: 请先深度分析《一夕千悟，从杂役弟子开始》前5章的：
  1. 人物关系图谱（段融、杨震、孔斌三人组、...
23:04:42 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
23:04:42 app.services.ai.http_ai_service INFO   ModelSelector 已启用
23:04:42 app.services.ai.http_ai_service INFO   [成本追踪] 初始化未传db/user_id，将使用请求上下文按需记录成本
23:04:44 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
23:04:44 app.services.context.adaptive_budget INFO   ✅ 所有预算配置验证通过
23:04:55 app.services.context.vector_memory_store INFO   ✅ VectorMemoryStore初始化成功 | 目录=./data/chroma_db | 模型=paraphrase-multilingual-MiniLM-L12-v2 | 集合=user_memories
23:04:55 app.services.context.manager INFO   ✅ VectorMemoryStore 已初始化
23:04:55 app.services.context.manager INFO   ✅ ContextManager: 长期记忆已启用 (user_id=None)
23:04:55 app.services.context.manager INFO   ✅ ContextManager: 自适应预算已启用
23:04:55 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ ContextManager已初始化（长期记忆已启用，自适应预算已启用，总预算=16000 tokens）
成功加载模板: intent_classifier (版本 2.0.0)
成功加载模板: writing_agent (版本 2.0.0)
成功加载模板: planning_agent (版本 2.0.0)
成功加载模板: tool_agent (版本 2.0.0)
成功加载模板: query_agent (版本 2.0.0)
成功加载模板: system_agent_prompt (版本 2.0.0)
成功加载模板: creative_writing_prompt (版本 1.0.0)
23:04:55 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ PromptManager已初始化
23:04:55 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ Redis连接验证成功
23:04:55 app.services.agent.langgraph_agent INFO   [LangGraph] OK 使用 AsyncRedisSaver（redis://localhost:6379/0，TTL=7天）
23:04:55 app.services.agent.memory.metrics INFO   [MemoryMetrics] 监控系统已初始化
23:04:55 app.services.agent.memory.long_term_store INFO   [LongTermStore] Initialized: base_dir=./data/long_term_memory, max_size=50KB, compression=True
23:04:55 app.services.agent.memory.enhanced_memory_manager INFO   EnhancedMemoryManager initialized: short=10, medium=100, threshold=0.1, long_term_backup=enabled
23:04:55 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ EnhancedMemoryManager已创建
23:04:55 app.services.agent.memory.unified_coordinator INFO   [UnifiedMemoryCoordinator] 初始化统一记忆协调器
23:04:55 app.services.agent.memory.unified_coordinator INFO   [UnifiedMemoryCoordinator] 全局实例已设置
23:04:55 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ UnifiedMemoryCoordinator已初始化 | checkpointer=AsyncRedisSaver | enhanced_memory=yes | context_manager=yes
23:04:55 app.services.agent.parallel_tool_node INFO   [ParallelToolNode] 初始化完成，最大并发数=5，并行安全工具=4个
23:04:55 app.api.v1.agent INFO   [Global Agent] created global agent instance; MemorySaver shared across requests
23:04:55 app.services.agent.langgraph_agent INFO   [Planning] 使用隔离的thread_id: c9dd9cbf-fa57-447e-9605-3020bbde5350:a68498ba-165c-4ca0-9912-deba7926a8b9 (work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, conversation_id=a68498ba-165c-4ca0-9912-deba7926a8b9)
23:04:55 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: 请先深度分析《一夕千悟，从杂役弟子开始》前5章的：
  1. 人物关系图谱（段融、杨震、孔斌三人组、...
23:04:55 app.core.cache INFO   ✅ 缓存命中: prompt:get_planning_agent_mode_prompt:fca6eb91156619d0
23:04:55 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
23:04:55 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
23:04:55 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=1200, temp=0.3, task_type=TaskType.SIMPLE_QA
23:04:58 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
23:05:12 app.services.ai.http_ai_service INFO   API 响应完成，共接收 25 个数据块，总长度: 2894
23:05:12 app.services.ai.http_ai_service INFO   流式响应Token统计: 6917 (prompt=5355, completion=1562)
23:05:12 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
23:05:12 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
23:05:12 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=6917, cost=$0.022314, time=17013ms
23:05:12 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=6917
23:05:12 app.services.agent.langgraph_agent INFO   [JSON解析] 方法2成功: 从```json块提取
23:05:12 app.services.agent.langgraph_agent INFO   [Planning] 思维链: 输出=用户期望得到两部分内容：1. 对小说《一夕千悟，从杂役弟子开, 原料=需要获取《一夕千悟，从杂役弟子开始》前5, 处理=首先，使用 `get_chapter_b
23:05:12 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共6个任务，耗时: 17.12s
23:05:12 app.api.v1.agent INFO   [Stream] Plan tasks: 6 items
23:05:12 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
23:05:12 app.services.agent.langgraph_agent INFO   [DeepAgent] 启用反思模式
23:05:12 app.services.agent.parameter_resolver INFO   [ParameterResolver] 初始化完成, 严格模式: False
23:05:12 app.services.agent.langgraph_agent INFO   [DeepAgent] ParameterResolver 已启用
23:05:12 app.services.agent.deep_agent.executor INFO   DeepAgent 开始执行，共 6 个任务，反思功能已启用
23:05:12 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] AI 推断功能已启用
23:05:12 app.api.v1.agent INFO   [Stream] Task started: 获取《一夕千悟，从杂役弟子开始》第一章内容
23:05:12 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
23:05:12 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
23:05:12 app.api.v1.agent INFO   [Stream] 任务完成: 获取《一夕千悟，从杂役弟子开始》第一章内容 (0.1s)
23:05:12 app.api.v1.agent INFO   [Stream] Task started: 获取《一夕千悟，从杂役弟子开始》第二章内容
23:05:12 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
23:05:12 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第2章: 第2章 浑圆桩
23:05:12 app.api.v1.agent INFO   [Stream] 任务完成: 获取《一夕千悟，从杂役弟子开始》第二章内容 (0.0s)
23:05:12 app.api.v1.agent INFO   [Stream] Task started: 获取《一夕千悟，从杂役弟子开始》第三章内容
23:05:12 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
23:05:12 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第3章: 第3章 一夕千悟
23:05:12 app.api.v1.agent INFO   [Stream] 任务完成: 获取《一夕千悟，从杂役弟子开始》第三章内容 (0.0s)
23:05:12 app.api.v1.agent INFO   [Stream] Task started: 获取《一夕千悟，从杂役弟子开始》第四章内容
23:05:12 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
23:05:12 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第4章: 第4章 家底
23:05:12 app.api.v1.agent INFO   [Stream] 任务完成: 获取《一夕千悟，从杂役弟子开始》第四章内容 (0.0s)
23:05:12 app.api.v1.agent INFO   [Stream] Task started: 获取《一夕千悟，从杂役弟子开始》第五章内容
23:05:12 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
23:05:12 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第5章: 第5章 太一门
23:05:12 app.api.v1.agent INFO   [Stream] 任务完成: 获取《一夕千悟，从杂役弟子开始》第五章内容 (0.0s)
23:05:12 app.api.v1.agent INFO   [Stream] Task started: 深度分析前5章内容，并规划第6-10章大纲
23:05:12 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
23:05:12 app.prompts.constraint_manager INFO   ✅ 已加载模板: analyze_text (v3.1.0)
23:05:12 app.prompts.constraint_manager INFO   ✅ 已加载模板: creative_writing (v1.0.0)
23:05:12 app.prompts.constraint_manager INFO   ✅ 已加载模板: intent_classifier (v2.0.0)
23:05:12 app.prompts.constraint_manager INFO   ✅ 已加载模板: planning_agent (v2.0.0)
23:05:13 app.prompts.constraint_manager INFO   ✅ 已加载模板: query_agent (v2.0.0)
23:05:13 app.prompts.constraint_manager INFO   ✅ 已加载模板: system_agent (v2.0.0)
23:05:13 app.prompts.constraint_manager INFO   ✅ 已加载模板: tool_agent (v2.0.0)
23:05:13 app.prompts.constraint_manager INFO   ✅ 已加载模板: writing_agent (v2.0.0)
23:05:13 app.prompts.constraint_manager INFO   ✅ 约束提示词管理器已初始化: 加载8个模板, 注册0个验证器
23:05:13 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
23:05:13 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
23:05:13 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
23:05:15 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
23:06:07 app.services.ai.http_ai_service INFO   API 响应完成，共接收 139 个数据块，总长度: 9626
23:06:07 app.services.ai.http_ai_service INFO   流式响应Token统计: 22407 (prompt=15668, completion=6739)
23:06:07 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
23:06:07 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
23:06:07 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=22407, cost=$0.086975, time=54356ms
23:06:07 app.services.agent.langgraph_agent INFO   ✅ [Agent分析] 分析完成，结果长度: 9626
23:06:07 app.api.v1.agent INFO   [Stream] 任务完成: 深度分析前5章内容，并规划第6-10章大纲 (54.5s)
23:06:07 app.services.agent.deep_agent.reflection INFO   [Checkpoint] 任务 6 标记了 checkpoint，触发反思
23:06:07 app.services.agent.deep_agent.executor INFO   任务 6 触发反思检查点
23:06:07 app.services.agent.deep_agent.reflection INFO   [DeepAgent反思] 开始调用 AI，task_id=6
23:06:07 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
23:06:07 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
23:06:07 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=500, temp=0.3, task_type=TaskType.SIMPLE_QA
23:06:09 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
23:06:12 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 63
23:06:12 app.services.ai.http_ai_service INFO   流式响应Token统计: 792 (prompt=753, completion=39)
23:06:12 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
23:06:12 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
23:06:12 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=792, cost=$0.001331, time=4525ms
23:06:12 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=792
23:06:12 app.services.agent.deep_agent.reflection INFO   [Reflection] 解析结果: needs_replan=True, first_line=REPLAN:YES, raw_len=63
23:06:12 app.services.agent.deep_agent.executor INFO   反思结果需要重规划 (第 1 次)
23:06:12 app.services.agent.deep_agent.executor INFO   [DeepAgent重规划] 开始调用 AI
23:06:12 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
23:06:12 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
23:06:12 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=800, temp=0.2, task_type=TaskType.SIMPLE_QA
23:06:14 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
23:06:19 app.services.ai.http_ai_service INFO   API 响应完成，共接收 3 个数据块，总长度: 287
23:06:19 app.services.ai.http_ai_service INFO   流式响应Token统计: 1921 (prompt=1769, completion=152)
23:06:19 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
23:06:19 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
23:06:19 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1921, cost=$0.003731, time=7504ms
23:06:19 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=1921
23:06:19 app.api.v1.agent INFO   [Stream] Plan tasks: 10 items
23:06:19 app.services.agent.deep_agent.executor INFO   计划已更新，新任务数: 4
23:06:19 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=200, temp=0.1, task_type=None
23:06:23 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
23:06:29 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 96
23:06:29 app.services.ai.http_ai_service INFO   流式响应Token统计: 1143 (prompt=1100, completion=43)
23:06:29 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
23:06:29 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
23:06:29 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1143, cost=$0.001805, time=9959ms
23:06:29 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=1143
23:06:29 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] 从 1 个任务结果中提取文本，总长度: 9626 字符
23:06:29 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] AI 推断成功: '[待办] 规划《一夕千悟，从杂役弟子开始》第6-10章大纲...' → tool=analyze_text_tool
23:06:29 app.api.v1.agent INFO   [Stream] Task started: [待办] 规划《一夕千悟，从杂役弟子开始》第6-10章大纲
23:06:29 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
23:06:29 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
23:06:29 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
23:06:29 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
23:06:33 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
23:07:18 app.services.ai.http_ai_service INFO   API 响应完成，共接收 70 个数据块，总长度: 6414
23:07:18 app.services.ai.http_ai_service INFO   流式响应Token统计: 14872 (prompt=10293, completion=4579)
23:07:18 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
23:07:18 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
23:07:18 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=14872, cost=$0.058656, time=48602ms
23:07:18 app.services.agent.langgraph_agent INFO   ✅ [Agent分析] 分析完成，结果长度: 6414
23:07:18 app.api.v1.agent INFO   [Stream] 任务完成: [待办] 规划《一夕千悟，从杂役弟子开始》第6-10章大纲 (48.6s)
23:07:18 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=200, temp=0.1, task_type=None
23:07:31 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
23:07:48 app.services.agent.deep_agent.task_enricher WARNING   [TaskEnricher] AI 推断超时
23:07:48 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] 从 2 个任务结果中提取文本，总长度: 16042 字符
23:07:48 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] 规则匹配成功: '[待办] 评估第6-10章大纲规划的合理性与完整性...' → tool=analyze_text_tool
23:07:48 app.api.v1.agent INFO   [Stream] Task started: [待办] 评估第6-10章大纲规划的合理性与完整性
23:07:48 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
23:07:48 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
23:07:48 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
23:07:48 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
23:07:50 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
23:08:15 app.services.ai.http_ai_service INFO   API 响应完成，共接收 99 个数据块，总长度: 6699
23:08:15 app.services.ai.http_ai_service INFO   流式响应Token统计: 17712 (prompt=12957, completion=4755)
23:08:15 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
23:08:15 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
23:08:15 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=17712, cost=$0.063746, time=27030ms
23:08:15 app.services.agent.langgraph_agent INFO   ✅ [Agent分析] 分析完成，结果长度: 6699
23:08:15 app.api.v1.agent INFO   [Stream] 任务完成: [待办] 评估第6-10章大纲规划的合理性与完整性 (27.1s)
23:08:15 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=200, temp=0.1, task_type=None
23:08:18 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
23:08:45 app.services.agent.deep_agent.task_enricher WARNING   [TaskEnricher] AI 推断超时
23:08:45 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] 规则匹配成功: '[已完成] 获取《一夕千悟，从杂役弟子开始》第四章内容...' → tool=get_chapter_by_order_tool
23:08:45 app.api.v1.agent INFO   [Stream] Task started: [已完成] 获取《一夕千悟，从杂役弟子开始》第四章内容
23:08:45 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
23:08:45 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第4章: 第4章 家底
23:08:45 app.api.v1.agent INFO   [Stream] 任务完成: [已完成] 获取《一夕千悟，从杂役弟子开始》第四章内容 (0.0s)
23:08:45 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=200, temp=0.1, task_type=None
23:08:53 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
23:08:59 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 89
23:08:59 app.services.ai.http_ai_service INFO   流式响应Token统计: 1310 (prompt=1267, completion=43)
23:08:59 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
23:08:59 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
23:08:59 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1310, cost=$0.002014, time=13783ms
23:08:59 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=1310
23:08:59 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] AI 推断成功: '[已完成] 获取《一夕千悟，从杂役弟子开始》第五章内容...' → tool=get_chapter_by_order_tool
23:08:59 app.api.v1.agent INFO   [Stream] Task started: [已完成] 获取《一夕千悟，从杂役弟子开始》第五章内容
23:08:59 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
23:08:59 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第5章: 第5章 太一门
23:08:59 app.api.v1.agent INFO   [Stream] 任务完成: [已完成] 获取《一夕千悟，从杂役弟子开始》第五章内容 (0.0s)
23:08:59 app.services.agent.deep_agent.executor INFO   DeepAgent 执行完成: 任务=10, 反思=1, 重规划=1
23:08:59 app.services.agent.langgraph_agent INFO   [DeepAgent] 执行完成: 反思=1次, 重规划=1次
23:08:59 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共10个任务，耗时: 226.67s
23:08:59 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
23:08:59 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=0, 输出型=3, 展示型=7
23:08:59 app.services.agent.langgraph_agent INFO   [Response] 3个输出任务，简单拼接
23:08:59 app.api.v1.agent INFO   [Stream] 跳过最终响应（内容已流式发送）
23:08:59 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed