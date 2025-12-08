13:38:24 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: planning, Message: 请先深度分析《一夕千悟，从杂役弟子开始》前5章的：
  1. 人物关系图谱（段融、杨震、孔斌三人组、...
13:38:24 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
13:38:24 app.services.ai.http_ai_service INFO   ModelSelector 已启用
13:38:24 app.services.ai.http_ai_service INFO   [成本追踪] 初始化未传db/user_id，将使用请求上下文按需记录成本
13:38:26 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
13:38:26 app.services.context.adaptive_budget INFO   ✅ 所有预算配置验证通过
13:38:37 app.services.context.vector_memory_store INFO   ✅ VectorMemoryStore初始化成功 | 目录=./data/chroma_db | 模型=paraphrase-multilingual-MiniLM-L12-v2 | 集合=user_memories
13:38:37 app.services.context.manager INFO   ✅ VectorMemoryStore 已初始化
13:38:37 app.services.context.manager INFO   ✅ ContextManager: 长期记忆已启用 (user_id=None)
13:38:37 app.services.context.manager INFO   ✅ ContextManager: 自适应预算已启用
13:38:37 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ ContextManager已初始化（长期记忆已启用，自适应预算已启用，总预算=16000 tokens）
成功加载模板: intent_classifier (版本 2.0.0)
成功加载模板: writing_agent (版本 2.0.0)
成功加载模板: planning_agent (版本 2.0.0)
成功加载模板: tool_agent (版本 2.0.0)
成功加载模板: query_agent (版本 2.0.0)
成功加载模板: system_agent_prompt (版本 2.0.0)
成功加载模板: creative_writing_prompt (版本 1.0.0)
13:38:37 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ PromptManager已初始化
13:38:37 app.services.agent.langgraph_agent INFO   [LangGraph] 使用 HTTPAIService 模式（手动工具调用，绕过 Cloudflare）
13:38:37 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ Redis连接验证成功
13:38:37 app.services.agent.langgraph_agent INFO   [LangGraph] OK 使用 AsyncRedisSaver（redis://localhost:6379/0，TTL=7天）
13:38:37 app.services.agent.memory.metrics INFO   [MemoryMetrics] 监控系统已初始化
13:38:37 app.services.agent.memory.long_term_store INFO   [LongTermStore] Initialized: base_dir=./data/long_term_memory, max_size=50KB, compression=True
13:38:37 app.services.agent.memory.enhanced_memory_manager INFO   EnhancedMemoryManager initialized: short=10, medium=100, threshold=0.1, long_term_backup=enabled
13:38:37 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ EnhancedMemoryManager已创建
13:38:37 app.services.agent.memory.unified_coordinator INFO   [UnifiedMemoryCoordinator] 初始化统一记忆协调器
13:38:37 app.services.agent.memory.unified_coordinator INFO   [UnifiedMemoryCoordinator] 全局实例已设置
13:38:37 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ UnifiedMemoryCoordinator已初始化 | checkpointer=AsyncRedisSaver | enhanced_memory=yes | context_manager=yes
13:38:37 app.services.agent.parallel_tool_node INFO   [ParallelToolNode] 初始化完成，最大并发数=5，并行安全工具=4个
13:38:37 app.api.v1.agent INFO   [Global Agent] created global agent instance; MemorySaver shared across requests
13:38:37 app.services.agent.langgraph_agent INFO   [Planning] 使用隔离的thread_id: c9dd9cbf-fa57-447e-9605-3020bbde5350:0cd1cd0d-790f-4e88-b8e4-3f7ac3fe4afe (work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, conversation_id=0cd1cd0d-790f-4e88-b8e4-3f7ac3fe4afe)
13:38:37 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: 请先深度分析《一夕千悟，从杂役弟子开始》前5章的：
  1. 人物关系图谱（段融、杨震、孔斌三人组、...
13:38:37 app.core.cache INFO   ⚠️ 缓存未命中: prompt:get_planning_agent_mode_prompt:fca6eb91156619d0
13:38:37 app.core.cache INFO   ⚠️ 缓存未命中: prompt:get_planning_static_prompt:fca6eb91156619d0
13:38:37 app.core.cache INFO   💾 缓存已保存: prompt:get_planning_static_prompt:fca6eb91156619d0 (expire=3600s)
13:38:37 app.core.cache INFO   💾 缓存已保存: prompt:get_planning_agent_mode_prompt:fca6eb91156619d0 (expire=3600s)
13:38:37 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
13:38:37 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
13:38:37 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=1200, temp=0.3, task_type=TaskType.SIMPLE_QA
13:38:40 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
13:38:47 app.services.ai.http_ai_service INFO   API 响应完成，共接收 19 个数据块，总长度: 2307
13:38:47 app.services.ai.http_ai_service INFO   流式响应Token统计: 6172 (prompt=4980, completion=1192)
13:38:47 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
13:38:47 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=6172, cost=$0.018145, time=9480ms
13:38:47 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=6172
13:38:47 app.services.agent.langgraph_agent INFO   [JSON解析] 方法2成功: 从```json块提取
13:38:47 app.services.agent.langgraph_agent INFO   [Planning] 思维链: 输出=用户期望得到两部分内容：1. 对《一夕千悟，从杂役弟子开始》, 原料=需要《一夕千悟，从杂役弟子开始》第1章至, 处理=1. 使用 `get_chapter_b
13:38:47 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共7个任务，耗时: 9.55s
13:38:47 app.api.v1.agent INFO   [Stream] Plan tasks: 7 items
13:38:47 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
13:38:47 app.services.agent.langgraph_agent INFO   [DeepAgent] 启用反思模式
13:38:47 app.services.agent.parameter_resolver INFO   [ParameterResolver] 初始化完成, 严格模式: False
13:38:47 app.services.agent.langgraph_agent INFO   [DeepAgent] ParameterResolver 已启用
13:38:47 app.services.agent.deep_agent.executor INFO   DeepAgent 开始执行，共 7 个任务，反思功能已启用
13:38:47 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] AI 推断功能已启用
13:38:47 app.api.v1.agent INFO   [Stream] Task started: 获取《一夕千悟，从杂役弟子开始》第一章内容
13:38:47 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
13:38:47 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 第1章 吞噬
13:38:47 app.api.v1.agent INFO   [Stream] 任务完成: 获取《一夕千悟，从杂役弟子开始》第一章内容 (0.0s)
13:38:47 app.api.v1.agent INFO   [Stream] Task started: 获取《一夕千悟，从杂役弟子开始》第二章内容
13:38:47 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
13:38:47 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第2章: 第2章 浑圆桩
13:38:47 app.api.v1.agent INFO   [Stream] 任务完成: 获取《一夕千悟，从杂役弟子开始》第二章内容 (0.0s)
13:38:47 app.api.v1.agent INFO   [Stream] Task started: 获取《一夕千悟，从杂役弟子开始》第三章内容
13:38:47 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
13:38:47 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第3章: 第3章 一夕千悟
13:38:47 app.api.v1.agent INFO   [Stream] 任务完成: 获取《一夕千悟，从杂役弟子开始》第三章内容 (0.0s)
13:38:47 app.api.v1.agent INFO   [Stream] Task started: 获取《一夕千悟，从杂役弟子开始》第四章内容
13:38:47 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
13:38:47 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第4章: 第4章 家底
13:38:47 app.api.v1.agent INFO   [Stream] 任务完成: 获取《一夕千悟，从杂役弟子开始》第四章内容 (0.0s)
13:38:47 app.api.v1.agent INFO   [Stream] Task started: 获取《一夕千悟，从杂役弟子开始》第五章内容
13:38:47 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
13:38:47 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第5章: 第5章 太一门
13:38:47 app.api.v1.agent INFO   [Stream] 任务完成: 获取《一夕千悟，从杂役弟子开始》第五章内容 (0.0s)
13:38:47 app.api.v1.agent INFO   [Stream] Task started: 深度分析《一夕千悟，从杂役弟子开始》前5章内容
13:38:47 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
13:38:47 app.prompts.constraint_manager INFO   ✅ 已加载模板: analyze_text (v3.1.0)
13:38:47 app.prompts.constraint_manager INFO   ✅ 已加载模板: creative_writing (v1.0.0)
13:38:47 app.prompts.constraint_manager INFO   ✅ 已加载模板: intent_classifier (v2.0.0)
13:38:47 app.prompts.constraint_manager INFO   ✅ 已加载模板: planning_agent (v2.0.0)
13:38:47 app.prompts.constraint_manager INFO   ✅ 已加载模板: query_agent (v2.0.0)
13:38:47 app.prompts.constraint_manager INFO   ✅ 已加载模板: system_agent (v2.0.0)
13:38:47 app.prompts.constraint_manager INFO   ✅ 已加载模板: tool_agent (v2.0.0)
13:38:47 app.prompts.constraint_manager INFO   ✅ 已加载模板: writing_agent (v2.0.0)
13:38:47 app.prompts.constraint_manager INFO   ✅ 约束提示词管理器已初始化: 加载8个模板, 注册0个验证器
13:38:47 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
13:38:47 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
13:38:47 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
13:38:49 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
13:39:14 app.services.ai.http_ai_service INFO   API 响应完成，共接收 41 个数据块，总长度: 3671
13:39:14 app.services.ai.http_ai_service INFO   流式响应Token统计: 17475 (prompt=14805, completion=2670)
13:39:14 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
13:39:14 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=17475, cost=$0.045206, time=27325ms
13:39:14 app.services.agent.langgraph_agent INFO   ✅ [Agent分析] 分析完成，结果长度: 3671
13:39:14 app.api.v1.agent INFO   [Stream] 任务完成: 深度分析《一夕千悟，从杂役弟子开始》前5章内容 (0.0s)
13:39:14 app.services.agent.deep_agent.reflection INFO   [Checkpoint] 任务 6 标记了 checkpoint，触发反思
13:39:14 app.services.agent.deep_agent.executor INFO   任务 6 触发反思检查点
13:39:14 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=500, temp=0.3, task_type=None
13:39:17 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
13:39:30 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 60
13:39:30 app.services.ai.http_ai_service INFO   流式响应Token统计: 1942 (prompt=1904, completion=38)
13:39:30 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
13:39:30 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1942, cost=$0.002760, time=16384ms
13:39:30 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=1942
13:39:30 app.services.agent.deep_agent.executor INFO   反思结果需要重规划 (第 1 次)
13:39:30 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=1000, temp=0.3, task_type=None
13:39:34 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
13:39:41 app.services.ai.http_ai_service INFO   API 响应完成，共接收 2 个数据块，总长度: 144
13:39:41 app.services.ai.http_ai_service INFO   流式响应Token统计: 1228 (prompt=1159, completion=69)
13:39:41 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
13:39:41 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1228, cost=$0.002139, time=10761ms
13:39:41 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=1228
13:39:41 app.api.v1.agent INFO   [Stream] Plan tasks: 8 items
13:39:41 app.services.agent.deep_agent.executor INFO   计划已更新，新任务数: 2
13:39:41 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=200, temp=0.1, task_type=None
13:39:44 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
13:39:51 app.services.agent.deep_agent.task_enricher WARNING   [TaskEnricher] AI 推断超时
13:39:51 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] 规则匹配成功: '补充主角能力设定细节与未来情节钩子...' → tool=get_context_tool
13:39:51 app.api.v1.agent INFO   [Stream] Task started: 补充主角能力设定细节与未来情节钩子
13:39:51 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
13:39:51 app.services.agent.langgraph_agent INFO   [get_context_tool] 🔥 新版本工具被调用！work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id=627feba4-2097-4f28-a3f3-7641d10f7f40
13:39:51 app.services.agent.langgraph_agent INFO   [get_context_tool] 当前章节order=1，将检索前0章
13:39:51 app.services.chapter_vector_service INFO   RAG检索: work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, current_order=1, query=作品背景、人物关系、情节发展、伏笔线索...
13:39:51 app.services.chapter_vector_service WARNING   ⚠️ 作品 c9dd9cbf-fa57-447e-9605-3020bbde5350 前0章暂无向量数据
13:39:51 app.services.agent.langgraph_agent WARNING   [get_context_tool] RAG检索为空，使用Worldview降级
13:39:52 app.services.agent.langgraph_agent INFO   [get_context_tool] ✅ 获取上下文成功: work=一夕千悟，从杂役弟子开始
13:39:52 app.api.v1.agent INFO   [Stream] 任务完成: 补充主角能力设定细节与未来情节钩子 (0.0s)
13:39:52 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=200, temp=0.1, task_type=None
13:39:54 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
13:39:59 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 94
13:39:59 app.services.ai.http_ai_service INFO   流式响应Token统计: 1057 (prompt=1015, completion=42)
13:39:59 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
13:39:59 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1057, cost=$0.001689, time=7671ms
13:39:59 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=1057
13:39:59 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] 从 3 个任务结果中提取文本，总长度: 8113 字符
13:39:59 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] AI 推断成功: '基于深化分析结果，规划第6-10章的详细大纲...' → tool=analyze_text_tool
13:39:59 app.api.v1.agent INFO   [Stream] Task started: 基于深化分析结果，规划第6-10章的详细大纲
13:39:59 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
13:39:59 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
13:39:59 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
13:39:59 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
13:40:01 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
13:40:22 app.services.ai.http_ai_service INFO   API 响应完成，共接收 44 个数据块，总长度: 4002
13:40:22 app.services.ai.http_ai_service INFO   流式响应Token统计: 11720 (prompt=8832, completion=2888)
13:40:22 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
13:40:22 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=11720, cost=$0.039920, time=23049ms
13:40:22 app.services.agent.langgraph_agent INFO   ✅ [Agent分析] 分析完成，结果长度: 4002
13:40:22 app.api.v1.agent INFO   [Stream] 任务完成: 基于深化分析结果，规划第6-10章的详细大纲 (0.0s)
13:40:22 app.services.agent.deep_agent.executor INFO   DeepAgent 执行完成: 任务=8, 反思=1, 重规划=1
13:40:22 app.services.agent.langgraph_agent INFO   [DeepAgent] 执行完成: 反思=1次, 重规划=1次
13:40:22 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共8个任务，耗时: 95.65s
13:40:22 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
13:40:22 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=1, 输出型=2, 展示型=5
13:40:22 app.services.agent.langgraph_agent INFO   [Response] 2个输出任务，简单拼接
13:40:22 app.api.v1.agent INFO   [Stream] 跳过最终响应（内容已流式发送）
13:40:22 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed