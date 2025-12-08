14:08:09 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: planning, Message: 请先深度分析《一夕千悟，从杂役弟子开始》前5章的：
  1. 人物关系图谱（段融、杨震、孔斌三人组、...
14:08:09 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
14:08:09 app.services.ai.http_ai_service INFO   ModelSelector 已启用
14:08:09 app.services.ai.http_ai_service INFO   [成本追踪] 初始化未传db/user_id，将使用请求上下文按需记录成本
14:08:13 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
14:08:13 app.services.context.adaptive_budget INFO   ✅ 所有预算配置验证通过
14:08:28 app.services.context.vector_memory_store INFO   ✅ VectorMemoryStore初始化成功 | 目录=./data/chroma_db | 模型=paraphrase-multilingual-MiniLM-L12-v2 | 集合=user_memories
14:08:28 app.services.context.manager INFO   ✅ VectorMemoryStore 已初始化
14:08:28 app.services.context.manager INFO   ✅ ContextManager: 长期记忆已启用 (user_id=None)
14:08:28 app.services.context.manager INFO   ✅ ContextManager: 自适应预算已启用
14:08:28 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ ContextManager已初始化（长期记忆已启用，自适应预算已启用，总预算=16000 tokens）
成功加载模板: intent_classifier (版本 2.0.0)
成功加载模板: writing_agent (版本 2.0.0)
成功加载模板: planning_agent (版本 2.0.0)
成功加载模板: tool_agent (版本 2.0.0)
成功加载模板: query_agent (版本 2.0.0)
成功加载模板: system_agent_prompt (版本 2.0.0)
成功加载模板: creative_writing_prompt (版本 1.0.0)
14:08:28 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ PromptManager已初始化
14:08:28 app.services.agent.langgraph_agent INFO   [LangGraph] 使用 HTTPAIService 模式（手动工具调用，绕过 Cloudflare）
14:08:28 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ Redis连接验证成功
14:08:28 app.services.agent.langgraph_agent INFO   [LangGraph] OK 使用 AsyncRedisSaver（redis://localhost:6379/0，TTL=7天）
14:08:28 app.services.agent.memory.metrics INFO   [MemoryMetrics] 监控系统已初始化
14:08:28 app.services.agent.memory.long_term_store INFO   [LongTermStore] Initialized: base_dir=./data/long_term_memory, max_size=50KB, compression=True
14:08:28 app.services.agent.memory.enhanced_memory_manager INFO   EnhancedMemoryManager initialized: short=10, medium=100, threshold=0.1, long_term_backup=enabled
14:08:28 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ EnhancedMemoryManager已创建
14:08:28 app.services.agent.memory.unified_coordinator INFO   [UnifiedMemoryCoordinator] 初始化统一记忆协调器
14:08:28 app.services.agent.memory.unified_coordinator INFO   [UnifiedMemoryCoordinator] 全局实例已设置
14:08:28 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ UnifiedMemoryCoordinator已初始化 | checkpointer=AsyncRedisSaver | enhanced_memory=yes | context_manager=yes
14:08:28 app.services.agent.parallel_tool_node INFO   [ParallelToolNode] 初始化完成，最大并发数=5，并行安全工具=4个
14:08:28 app.api.v1.agent INFO   [Global Agent] created global agent instance; MemorySaver shared across requests
14:08:28 app.services.agent.langgraph_agent INFO   [Planning] 使用隔离的thread_id: c9dd9cbf-fa57-447e-9605-3020bbde5350:0aa1c0e3-04c8-4225-81a8-260076143dc3 (work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, conversation_id=0aa1c0e3-04c8-4225-81a8-260076143dc3)
14:08:28 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: 请先深度分析《一夕千悟，从杂役弟子开始》前5章的：
  1. 人物关系图谱（段融、杨震、孔斌三人组、...
14:08:28 app.core.cache INFO   ✅ 缓存命中: prompt:get_planning_agent_mode_prompt:fca6eb91156619d0
14:08:28 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
14:08:28 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
14:08:28 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=1200, temp=0.3, task_type=TaskType.SIMPLE_QA
14:08:31 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
14:08:40 app.services.ai.http_ai_service INFO   API 响应完成，共接收 19 个数据块，总长度: 2225
14:08:40 app.services.ai.http_ai_service INFO   流式响应Token统计: 6685 (prompt=5507, completion=1178)
14:08:40 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
14:08:40 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=6685, cost=$0.018664, time=11751ms
14:08:40 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=6685
14:08:40 app.services.agent.langgraph_agent INFO   [JSON解析] 方法2成功: 从```json块提取
14:08:40 app.services.agent.langgraph_agent INFO   [Planning] 思维链: 输出=用户期望得到一份深度分析报告（包含人物关系、能力体系、世界观, 原料=需要《一夕千悟，从杂役弟子开始》前5章的, 处理=获取前5章内容，然后使用analyze_
14:08:40 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共6个任务，耗时: 11.92s
14:08:40 app.api.v1.agent INFO   [Stream] Plan tasks: 6 items
14:08:40 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
14:08:40 app.services.agent.langgraph_agent INFO   [DeepAgent] 启用反思模式
14:08:40 app.services.agent.parameter_resolver INFO   [ParameterResolver] 初始化完成, 严格模式: False
14:08:40 app.services.agent.langgraph_agent INFO   [DeepAgent] ParameterResolver 已启用
14:08:40 app.services.agent.deep_agent.executor INFO   DeepAgent 开始执行，共 6 个任务，反思功能已启用
14:08:40 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] AI 推断功能已启用
14:08:40 app.api.v1.agent INFO   [Stream] Task started: 获取《一夕千悟，从杂役弟子开始》第一章内容
14:08:40 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
14:08:40 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
14:08:40 app.api.v1.agent INFO   [Stream] 任务完成: 获取《一夕千悟，从杂役弟子开始》第一章内容 (0.1s)
14:08:40 app.api.v1.agent INFO   [Stream] Task started: 获取《一夕千悟，从杂役弟子开始》第二章内容
14:08:40 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
14:08:40 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第2章: 第2章 浑圆桩
14:08:40 app.api.v1.agent INFO   [Stream] 任务完成: 获取《一夕千悟，从杂役弟子开始》第二章内容 (0.1s)
14:08:40 app.api.v1.agent INFO   [Stream] Task started: 获取《一夕千悟，从杂役弟子开始》第三章内容
14:08:40 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
14:08:40 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第3章: 第3章 一夕千悟
14:08:40 app.api.v1.agent INFO   [Stream] 任务完成: 获取《一夕千悟，从杂役弟子开始》第三章内容 (0.1s)
14:08:40 app.api.v1.agent INFO   [Stream] Task started: 获取《一夕千悟，从杂役弟子开始》第四章内容
14:08:40 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
14:08:40 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第4章: 第4章 家底
14:08:40 app.api.v1.agent INFO   [Stream] 任务完成: 获取《一夕千悟，从杂役弟子开始》第四章内容 (0.1s)
14:08:40 app.api.v1.agent INFO   [Stream] Task started: 获取《一夕千悟，从杂役弟子开始》第五章内容
14:08:40 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
14:08:41 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第5章: 第5章 太一门
14:08:41 app.api.v1.agent INFO   [Stream] 任务完成: 获取《一夕千悟，从杂役弟子开始》第五章内容 (0.1s)
14:08:41 app.api.v1.agent INFO   [Stream] Task started: 深度分析前5章内容，并规划第6-10章大纲
14:08:41 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
14:08:41 app.prompts.constraint_manager INFO   ✅ 已加载模板: analyze_text (v3.1.0)
14:08:41 app.prompts.constraint_manager INFO   ✅ 已加载模板: creative_writing (v1.0.0)
14:08:41 app.prompts.constraint_manager INFO   ✅ 已加载模板: intent_classifier (v2.0.0)
14:08:41 app.prompts.constraint_manager INFO   ✅ 已加载模板: planning_agent (v2.0.0)
14:08:41 app.prompts.constraint_manager INFO   ✅ 已加载模板: query_agent (v2.0.0)
14:08:41 app.prompts.constraint_manager INFO   ✅ 已加载模板: system_agent (v2.0.0)
14:08:41 app.prompts.constraint_manager INFO   ✅ 已加载模板: tool_agent (v2.0.0)
14:08:41 app.prompts.constraint_manager INFO   ✅ 已加载模板: writing_agent (v2.0.0)
14:08:41 app.prompts.constraint_manager INFO   ✅ 约束提示词管理器已初始化: 加载8个模板, 注册0个验证器
14:08:41 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
14:08:41 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
14:08:41 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
14:08:43 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
14:09:21 app.services.ai.http_ai_service INFO   API 响应完成，共接收 69 个数据块，总长度: 6248
14:09:21 app.services.ai.http_ai_service INFO   流式响应Token统计: 19137 (prompt=14656, completion=4481)
14:09:21 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
14:09:21 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=19137, cost=$0.063130, time=40338ms
14:09:21 app.services.agent.langgraph_agent INFO   ✅ [Agent分析] 分析完成，结果长度: 6248
14:09:21 app.api.v1.agent INFO   [Stream] 任务完成: 深度分析前5章内容，并规划第6-10章大纲 (40.6s)
14:09:21 app.services.agent.deep_agent.reflection INFO   [Checkpoint] 任务 6 标记了 checkpoint，触发反思
14:09:21 app.services.agent.deep_agent.executor INFO   任务 6 触发反思检查点
14:09:21 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=500, temp=0.3, task_type=None
14:09:24 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
14:09:39 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 52
14:09:39 app.services.ai.http_ai_service INFO   流式响应Token统计: 2176 (prompt=2144, completion=32)
14:09:39 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
14:09:39 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2176, cost=$0.003000, time=18159ms
14:09:39 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=2176
14:09:39 app.services.agent.deep_agent.executor INFO   DeepAgent 执行完成: 任务=6, 反思=1, 重规划=0
14:09:39 app.services.agent.langgraph_agent INFO   [DeepAgent] 执行完成: 反思=1次, 重规划=0次
14:09:39 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共6个任务，耗时: 59.12s
14:09:39 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
14:09:39 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=0, 输出型=1, 展示型=5
14:09:39 app.services.agent.langgraph_agent INFO   [Response] 单个分析任务(analyze_text_tool)，使用AI格式化
14:09:39 app.services.agent.langgraph_agent INFO   [Summarization] 使用AI整合任务结果
14:09:39 app.services.agent.langgraph_agent INFO   [Summarization] 上下文压缩: 原始=20236字符, 压缩后=4441字符, 压缩率=79%
14:09:39 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
14:09:39 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
14:09:39 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
14:09:42 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
14:10:22 app.services.ai.http_ai_service INFO   API 响应完成，共接收 59 个数据块，总长度: 5803
14:10:22 app.services.ai.http_ai_service INFO   流式响应Token统计: 11445 (prompt=7616, completion=3829)
14:10:22 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
14:10:22 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=11445, cost=$0.047810, time=42913ms
14:10:22 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=11445
14:10:22 app.api.v1.agent INFO   [Stream] 跳过最终响应（内容已流式发送）
14:10:22 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed