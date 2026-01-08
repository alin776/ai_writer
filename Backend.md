2026-01-08 01:57:31,711 - app.services.context.manager - INFO - [ContextManager] 创建新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:d7c41457-7216-4b22-9316-ed4af8544925
2026-01-08 01:57:32,072 - app.services.context.token_counter - INFO - ✅ tiktoken初始化成功，模型: gemini-2.5-pro -> cl100k_base
2026-01-08 01:57:32,074 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:d7c41457-7216-4b22-9316-ed4af8544925: 0/16000 tokens
2026-01-08 01:57:34,160 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='查找关于"五虎群羊刀"和"浑圆桩"的所有设定信息，然后创作一...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:f141c5ed-0a75-4429-ba2a-912c74d167a3', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=3条
2026-01-08 01:57:34,172 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=f141c5ed-0a75-4429-ba2a-912c74d167a3 | 含用户级=True | 找到=3条
2026-01-08 01:57:34,188 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 1条消息, 0 tokens, 耗时 2487.54ms
2026-01-08 01:57:34,198 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 1 条历史消息 (token: 0)
2026-01-08 01:57:34,211 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-08 01:57:34,214 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-08 01:57:34,216 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=20, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-08 01:57:34,403 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:56623 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 01:57:36,274 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-08 01:57:36,274 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-08 01:57:36,309 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-08 01:57:36,310 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=330, cost=$0.000033, time=2058ms
2026-01-08 01:57:36,310 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=7, 尝试次数=1
2026-01-08 01:57:36,311 - app.services.agent.intent.classifier - INFO - [Intent] AI识别结果: writing
2026-01-08 01:57:36,311 - app.services.agent.langgraph_agent - INFO - [Planning] AI意图分类: writing (置信度: 0.90)
2026-01-08 01:57:36,311 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 查找关于"五虎群羊刀"和"浑圆桩"的所有设定信息，然后创作一段段融在深夜偷偷练功、突破瓶颈的精彩场景...
2026-01-08 01:57:36,319 - app.core.cache - INFO - ✅ 缓存命中: prompt:planning:v2.29.0:get_planning_static_prompt:fca6eb91156619d0
2026-01-08 01:57:36,324 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-08 01:57:36,324 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=story_planning, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: story_planning; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-01-08 01:57:36,325 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.3, task_type=TaskType.STORY_PLANNING
2026-01-08 01:57:49,234 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-08 01:57:55,235 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 12 个数据块，总长度: 1344
2026-01-08 01:57:55,235 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 14729 (prompt=14016, completion=713)
2026-01-08 01:57:55,236 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-08 01:57:55,236 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-08 01:57:55,247 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-08 01:57:55,248 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=14729, cost=$0.024650, time=18911ms
2026-01-08 01:57:55,248 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=14729
2026-01-08 01:57:55,248 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户需要两部分内容：1. 查找关于“五虎群羊刀”和“浑圆桩”, 原料=需要的原料是作品中所有关于“五虎群羊刀”, 处理=首先，通过两次搜索分别找到两个关键词的所
2026-01-08 01:57:55,254 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共3个任务
2026-01-08 01:57:55,255 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共3个任务，耗时: 18.94s
2026-01-08 01:57:55,255 - app.api.v1.agent - INFO - [Stream] Plan tasks: 3 items
2026-01-08 01:57:55,256 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2026-01-08 01:57:55,258 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2026-01-08 01:57:55,259 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2026-01-08 01:57:55,259 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 任务分组: 第一层并行=2, 第二层并行=0, 串行=1
2026-01-08 01:57:55,259 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始第一层并行执行2个任务
2026-01-08 01:57:55,259 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务1开始: 在作品中搜索关于“五虎群羊刀”的所有相关描述和设定信息。
2026-01-08 01:57:55,260 - app.api.v1.agent - INFO - [Stream] Task started: 在作品中搜索关于“五虎群羊刀”的所有相关描述和设定信息。 (icon=Search)
2026-01-08 01:57:55,260 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(search_analysis_fragments)
2026-01-08 01:57:55,261 - app.services.agent.tools.tool_types - INFO - [search_analysis_fragments] 开始执行工具
2026-01-08 01:57:55,262 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务2开始: 在作品中搜索关于“浑圆桩”的所有相关描述和设定信息。
2026-01-08 01:57:55,262 - app.api.v1.agent - INFO - [Stream] Task started: 在作品中搜索关于“浑圆桩”的所有相关描述和设定信息。 (icon=Search)
2026-01-08 01:57:55,262 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(search_analysis_fragments)
2026-01-08 01:57:55,264 - app.services.agent.tools.tool_types - INFO - [search_analysis_fragments] 开始执行工具
2026-01-08 01:57:56,476 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=f141c5ed-0a75-4429-ba2a-912c74d167a3, current_order=5, query=五虎群羊刀...
2026-01-08 01:57:56,693 - app.services.chapter_vector_service - INFO - RAG retrieved 10 segments within order<=7
Building prefix dict from the default dictionary ...
2026-01-08 01:57:56,695 - jieba - DEBUG - Building prefix dict from the default dictionary ...
Loading model from cache D:\Temp\jieba.cache
2026-01-08 01:57:56,695 - jieba - DEBUG - Loading model from cache D:\Temp\jieba.cache
Loading model cost 1.780 seconds.
2026-01-08 01:57:58,476 - jieba - DEBUG - Loading model cost 1.780 seconds.
Prefix dict has been built successfully.
2026-01-08 01:57:58,476 - jieba - DEBUG - Prefix dict has been built successfully.
2026-01-08 01:57:58,489 - app.services.agent.langgraph_tools - INFO - [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
2026-01-08 01:57:58,491 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=f141c5ed-0a75-4429-ba2a-912c74d167a3, current_order=5, query=浑圆桩...
2026-01-08 01:57:58,552 - app.services.agent.tools.tool_types - INFO - [search_analysis_fragments] 执行成功 (耗时: 3.290s)
2026-01-08 01:57:58,552 - app.services.agent.tools.tool_monitor - INFO - ToolMonitor initialized with Memory storage, retention: 7 days
2026-01-08 01:57:58,553 - app.services.agent.execution.task_runner - INFO - [TaskRunner] search_analysis_fragments 执行成功（DeepAgent模式）
2026-01-08 01:57:58,553 - app.api.v1.agent - INFO - [Stream] 任务完成: 在作品中搜索关于“五虎群羊刀”的所有相关描述和设定信息。 (3.3s)
2026-01-08 01:57:58,554 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务1完成
2026-01-08 01:57:58,590 - app.services.chapter_vector_service - INFO - RAG retrieved 10 segments within order<=7
2026-01-08 01:57:58,596 - app.services.agent.langgraph_tools - INFO - [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
2026-01-08 01:57:58,598 - app.services.agent.tools.tool_types - INFO - [search_analysis_fragments] 执行成功 (耗时: 3.334s)
2026-01-08 01:57:58,599 - app.services.agent.execution.task_runner - INFO - [TaskRunner] search_analysis_fragments 执行成功（DeepAgent模式）
2026-01-08 01:57:58,600 - app.api.v1.agent - INFO - [Stream] 任务完成: 在作品中搜索关于“浑圆桩”的所有相关描述和设定信息。 (3.3s)
2026-01-08 01:57:58,600 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务2完成
2026-01-08 01:57:58,602 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始串行执行1个任务
2026-01-08 01:57:58,602 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务3开始: 整合查找到的设定信息，创作一段约800字的主角深夜练功、突破瓶颈的场景，并详细描写内息流转。
2026-01-08 01:57:58,603 - app.api.v1.agent - INFO - [Stream] Task started: 整合查找到的设定信息，创作一段约800字的主角深夜练功、突破瓶颈的场景，并详细描写内息流转。 (icon=PenTool)
2026-01-08 01:57:58,603 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(continue_writing)
2026-01-08 01:57:58,604 - app.services.agent.tools.tool_types - INFO - [continue_writing] 开始执行工具
2026-01-08 01:57:58,614 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-08 01:57:58,615 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=content_creation, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: content_creation; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-01-08 01:57:58,616 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=1600, temp=0.8, task_type=TaskType.CONTENT_CREATION
2026-01-08 01:57:59,995 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:54031 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 01:58:22,201 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-08 01:58:29,951 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:50252 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 01:58:34,625 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 17 个数据块，总长度: 1274
2026-01-08 01:58:34,626 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 6923 (prompt=5854, completion=1069)
2026-01-08 01:58:34,626 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-08 01:58:34,627 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-08 01:58:34,643 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-08 01:58:34,644 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=6923, cost=$0.018008, time=36009ms
2026-01-08 01:58:34,645 - app.services.agent.tools.tool_types - INFO - [continue_writing] 执行成功 (耗时: 36.041s)
2026-01-08 01:58:34,645 - app.services.agent.execution.task_runner - INFO - [TaskRunner] continue_writing 执行成功（DeepAgent模式）
2026-01-08 01:58:34,646 - app.api.v1.agent - INFO - [Stream] 任务完成: 整合查找到的设定信息，创作一段约800字的主角深夜练功、突破瓶颈的场景，并详细描写内息流转。 (36.0s)
2026-01-08 01:58:34,646 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务3完成
2026-01-08 01:58:34,647 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共3个任务，耗时: 39.39s
2026-01-08 01:58:34,647 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2026-01-08 01:58:34,648 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=2, 输出型=1, 展示型=0
2026-01-08 01:58:34,648 - app.services.agent.langgraph_agent - INFO - [Response] 单个输出任务(continue_writing_tool)，使用AI整合
2026-01-08 01:58:34,649 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2026-01-08 01:58:34,649 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=2, 输出型=1, 展示型=0
2026-01-08 01:58:34,649 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=6691字符, 处理后=5480字符
2026-01-08 01:58:34,649 - app.services.agent.planning.response_builder - INFO - [Summarization] 准备发送 summarization_start 事件
2026-01-08 01:58:34,651 - app.services.agent.stream.stream_event_handler - INFO - [StreamEventHandler] emit_summarization_start 被调用, _on_flow_event=True
2026-01-08 01:58:34,651 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_start 事件已发送
2026-01-08 01:58:34,652 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2026-01-08 01:58:34,652 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2026-01-08 01:58:34,659 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-08 01:58:34,660 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-08 01:58:34,660 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
2026-01-08 01:58:46,930 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-08 01:58:59,988 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:60533 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-08 01:59:00,990 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 29 个数据块，总长度: 2423
2026-01-08 01:59:00,991 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 7809 (prompt=5967, completion=1842)
2026-01-08 01:59:00,993 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-08 01:59:00,993 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-08 01:59:01,015 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-08 01:59:01,021 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=7809, cost=$0.006395, time=26333ms
2026-01-08 01:59:01,023 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=2423
2026-01-08 01:59:05,505 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:f141c5ed-0a75-4429-ba2a-912c74d167a3 | 重要度=0.99
2026-01-08 01:59:09,705 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:f141c5ed-0a75-4429-ba2a-912c74d167a3 | 重要度=0.77
2026-01-08 01:59:09,724 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:d7c41457-7216-4b22-9316-ed4af8544925, token=3020
2026-01-08 01:59:09,730 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:d7c41457-7216-4b22-9316-ed4af8544925, 消息数=2, Token=3020
2026-01-08 01:59:09,732 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:d7c41457-7216-4b22-9316-ed4af8544925)
2026-01-08 01:59:09,733 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2026-01-08 01:59:09,746 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed