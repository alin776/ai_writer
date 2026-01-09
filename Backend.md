2026-01-10 02:15:20,586 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 我需要对小说进行一次改版，请按顺序完成以下操作：

  1. 首先，创建一个新章节"第四章 暗流涌动...
2026-01-10 02:15:20,597 - app.api.v1.agent - INFO - [agent_chat_stream] 📚 世界观数据已注入: 人物=10, 地点=6, 设定=6, 规范=无
2026-01-10 02:15:20,597 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:008150f0-1fc8-46ca-b1a7-facc70b16da6:671e74fa-e2d8-476f-9e8d-2043edf79a27 (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=008150f0-1fc8-46ca-b1a7-facc70b16da6, conversation_id=671e74fa-e2d8-476f-9e8d-2043edf79a27)
2026-01-10 02:15:20,600 - app.services.context.manager - INFO - [ContextManager] 创建新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:008150f0-1fc8-46ca-b1a7-facc70b16da6:671e74fa-e2d8-476f-9e8d-2043edf79a27
2026-01-10 02:15:20,601 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:008150f0-1fc8-46ca-b1a7-facc70b16da6:671e74fa-e2d8-476f-9e8d-2043edf79a27: 0/16000 tokens
2026-01-10 02:15:20,820 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='我需要对小说进行一次改版，请按顺序完成以下操作：

  1....' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:008150f0-1fc8-46ca-b1a7-facc70b16da6', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=3条
2026-01-10 02:15:20,820 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=008150f0-1fc8-46ca-b1a7-facc70b16da6 | 含用户级=True | 找到=3条
2026-01-10 02:15:20,820 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 1条消息, 0 tokens, 耗时 223.32ms
2026-01-10 02:15:20,824 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 1 条历史消息 (token: 0)
2026-01-10 02:15:20,825 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-10 02:15:20,825 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-10 02:15:20,826 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=20, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-10 02:15:22,126 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-10 02:15:22,128 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-10 02:15:22,144 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-10 02:15:22,146 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=443, cost=$0.000045, time=1301ms
2026-01-10 02:15:22,147 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=7, 尝试次数=1
2026-01-10 02:15:22,147 - app.services.agent.intent.classifier - INFO - [Intent] AI识别结果: writing
2026-01-10 02:15:22,147 - app.services.agent.langgraph_agent - INFO - [Planning] AI意图分类: writing (置信度: 0.90)
2026-01-10 02:15:22,147 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 我需要对小说进行一次改版，请按顺序完成以下操作：

  1. 首先，创建一个新章节"第四章 暗流涌动...
2026-01-10 02:15:22,159 - app.core.cache - INFO - ✅ 缓存命中: prompt:planning:v2.37.0:get_planning_static_prompt:fca6eb91156619d0
2026-01-10 02:15:22,166 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-10 02:15:22,166 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=story_planning, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: story_planning; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-01-10 02:15:22,168 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.3, task_type=TaskType.STORY_PLANNING
2026-01-10 02:15:24,567 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:61574 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-10 02:15:54,575 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:64571 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-10 02:16:19,508 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-10 02:16:24,577 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:63976 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-10 02:16:28,485 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 19 个数据块，总长度: 2443
2026-01-10 02:16:28,485 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 20163 (prompt=18980, completion=1183)
2026-01-10 02:16:28,485 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-10 02:16:28,485 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-10 02:16:28,506 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-10 02:16:28,509 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=20163, cost=$0.035555, time=66319ms
2026-01-10 02:16:28,509 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=20163
2026-01-10 02:16:28,509 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户希望对小说进行一系列有序的修改操作，包括创建新章节、修改, 原料=为了完成这些操作，我需要：
1. 获取现, 处理=我将按顺序规划一系列任务来完成用户的请求
2026-01-10 02:16:28,513 - app.services.agent.planning.plan_generator - INFO - [PlanValidator] 检测到人物查询'一段环境'但未指定章节，自动插入搜索任务
2026-01-10 02:16:28,513 - app.services.agent.planning.plan_generator - INFO - [PlanOptimizer] 合并 2 个章节读取任务为批量读取: 1-2
2026-01-10 02:16:28,513 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共6个任务
2026-01-10 02:16:28,513 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共6个任务，耗时: 66.37s
2026-01-10 02:16:28,513 - app.api.v1.agent - INFO - [Stream] Plan tasks: 6 items
2026-01-10 02:16:28,513 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2026-01-10 02:16:28,513 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2026-01-10 02:16:28,513 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2026-01-10 02:16:28,513 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 任务分组: 第一层并行=2, 第二层并行=0, 串行=4
2026-01-10 02:16:28,513 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始第一层并行执行2个任务
2026-01-10 02:16:28,513 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务1开始: 批量读取第1-2章
2026-01-10 02:16:28,513 - app.api.v1.agent - INFO - [Stream] Task started: 批量读取第1-2章 (icon=FileText)
2026-01-10 02:16:28,513 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(get_chapter_by_order)
2026-01-10 02:16:28,513 - app.services.agent.tools.tool_types - INFO - [get_chapter_by_order] 开始执行工具
2026-01-10 02:16:28,520 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务2开始: 搜索'一段环境'出现位置
2026-01-10 02:16:28,521 - app.api.v1.agent - INFO - [Stream] Task started: 搜索'一段环境'出现位置 (icon=Search)
2026-01-10 02:16:28,521 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(search_analysis_fragments)
2026-01-10 02:16:28,524 - app.services.agent.tools.tool_types - INFO - [search_analysis_fragments] 开始执行工具
2026-01-10 02:16:29,511 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=008150f0-1fc8-46ca-b1a7-facc70b16da6, current_order=3, query=一段环境...
2026-01-10 02:16:29,543 - app.services.agent.langgraph_tools - INFO - [get_chapter_by_order_tool] ✅ 批量读取成功: 共 2 章
2026-01-10 02:16:29,546 - app.services.agent.tools.tool_types - INFO - [get_chapter_by_order] 执行成功 (耗时: 1.033s)
2026-01-10 02:16:29,546 - app.services.agent.execution.task_runner - INFO - [TaskRunner] get_chapter_by_order 执行成功（DeepAgent模式）
2026-01-10 02:16:29,547 - app.api.v1.agent - INFO - [Stream] 任务完成: 批量读取第1-2章 (1.0s)
2026-01-10 02:16:29,547 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务1完成
2026-01-10 02:16:29,568 - app.services.chapter_vector_service - INFO - RAG retrieved 8 segments within order<=5
Building prefix dict from the default dictionary ...
2026-01-10 02:16:29,568 - jieba - DEBUG - Building prefix dict from the default dictionary ...
Loading model from cache D:\Temp\jieba.cache
2026-01-10 02:16:29,568 - jieba - DEBUG - Loading model from cache D:\Temp\jieba.cache
Loading model cost 0.393 seconds.
2026-01-10 02:16:29,961 - jieba - DEBUG - Loading model cost 0.393 seconds.
Prefix dict has been built successfully.
2026-01-10 02:16:29,961 - jieba - DEBUG - Prefix dict has been built successfully.
2026-01-10 02:16:29,970 - app.services.agent.langgraph_tools - INFO - [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
2026-01-10 02:16:29,970 - app.services.agent.tools.tool_types - INFO - [search_analysis_fragments] 执行成功 (耗时: 1.446s)
2026-01-10 02:16:29,972 - app.services.agent.execution.task_runner - INFO - [TaskRunner] search_analysis_fragments 执行成功（DeepAgent模式）
2026-01-10 02:16:29,972 - app.api.v1.agent - INFO - [Stream] 任务完成: 搜索'一段环境'出现位置 (1.5s)
2026-01-10 02:16:29,972 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 第一层任务2完成
2026-01-10 02:16:29,973 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始串行执行4个任务
2026-01-10 02:16:29,974 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务3开始: 根据用户要求，生成“第四章 暗流涌动”的章节内容
2026-01-10 02:16:29,974 - app.api.v1.agent - INFO - [Stream] Task started: 根据用户要求，生成“第四章 暗流涌动”的章节内容 (icon=PenTool)
2026-01-10 02:16:29,974 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 registry.call_tool(smart_continue)
2026-01-10 02:16:29,974 - app.services.agent.tools.tool_types - INFO - [smart_continue] 开始执行工具
2026-01-10 02:16:29,975 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-10 02:16:29,975 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=content_creation, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro
2026-01-10 02:16:29,975 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=1000, temp=0.8, 尝试=1/3, task_type=TaskType.CONTENT_CREATION
2026-01-10 02:16:54,728 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/unread-summary
INFO:     127.0.0.1:54042 - "GET /api/v1/channels/unread-summary HTTP/1.1" 200 OK
2026-01-10 02:17:00,817 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-10 02:17:00,817 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-10 02:17:00,832 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-10 02:17:00,833 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=3416, cost=$0.009634, time=30842ms
2026-01-10 02:17:00,833 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=787, 尝试次数=1
2026-01-10 02:17:00,835 - app.services.agent.tools.tool_types - INFO - [smart_continue] 执行成功 (耗时: 30.861s)
2026-01-10 02:17:00,835 - app.services.agent.execution.task_runner - INFO - [TaskRunner] smart_continue 执行成功（DeepAgent模式）
2026-01-10 02:17:00,837 - app.api.v1.agent - INFO - [Stream] 任务完成: 根据用户要求，生成“第四章 暗流涌动”的章节内容 (30.9s)
2026-01-10 02:17:00,837 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务3完成
2026-01-10 02:17:00,838 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务4开始: 创建“第四章 暗流涌动”
2026-01-10 02:17:00,838 - app.api.v1.agent - INFO - [Stream] Task started: 创建“第四章 暗流涌动” (icon=Wrench)
2026-01-10 02:17:00,840 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: create_chapter
2026-01-10 02:17:00,841 - app.services.agent.execution.tool_executor - WARNING - [StandardTool] 'create_chapter' 不存在，降级到 @tool: 工具 'create_chapter' 不存在
可用的 StandardTool: ['expand_text', 'analyze_content', 'analyze_text', 'evaluate_quality', 'smart_rewrite', 'smart_continue', 'smart_insert', 'apply_chapter_edit', 'get_context', 'read_chapter', 'get_chapter_by_order', 'search_analysis_fragments', 'get_worldview_summary', 'check_story_consistency']
可用的 DynamicTool: []
2026-01-10 02:17:00,841 - app.services.agent.execution.tool_executor - INFO - [LegacyTool] 使用 @tool 版本: create_chapter
2026-01-10 02:17:00,858 - app.api.v1.agent - INFO - [Stream] 任务完成: 创建“第四章 暗流涌动” (0.0s)
2026-01-10 02:17:00,859 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务4完成
2026-01-10 02:17:00,859 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务5开始: 将第一章“吞噬”的标题修改为“魂穿异域，器灵觉醒”
2026-01-10 02:17:00,860 - app.api.v1.agent - INFO - [Stream] Task started: 将第一章“吞噬”的标题修改为“魂穿异域，器灵觉醒” (icon=Wrench)
2026-01-10 02:17:00,860 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: update_chapter_title
2026-01-10 02:17:00,860 - app.services.agent.execution.tool_executor - WARNING - [StandardTool] 'update_chapter_title' 不存在，降级到 @tool: 工具 'update_chapter_title' 不存在
可用的 StandardTool: ['expand_text', 'analyze_content', 'analyze_text', 'evaluate_quality', 'smart_rewrite', 'smart_continue', 'smart_insert', 'apply_chapter_edit', 'get_context', 'read_chapter', 'get_chapter_by_order', 'search_analysis_fragments', 'get_worldview_summary', 'check_story_consistency']
可用的 DynamicTool: []
2026-01-10 02:17:00,860 - app.services.agent.execution.tool_executor - INFO - [LegacyTool] 使用 @tool 版本: update_chapter_title
2026-01-10 02:17:00,887 - app.api.v1.agent - INFO - [Stream] 任务完成: 将第一章“吞噬”的标题修改为“魂穿异域，器灵觉醒” (0.0s)
2026-01-10 02:17:00,887 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务5完成
2026-01-10 02:17:00,887 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务6开始: 在第二章“浑圆桩”的开头插入一段环境描写
2026-01-10 02:17:00,888 - app.api.v1.agent - INFO - [Stream] Task started: 在第二章“浑圆桩”的开头插入一段环境描写 (icon=Check)
2026-01-10 02:17:00,889 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: apply_chapter_edit
2026-01-10 02:17:00,900 - app.services.agent.execution.tool_executor - WARNING - [StandardTool] 'apply_chapter_edit' 不存在，降级到 @tool: StandardTool 执行失败: 1 validation error for ApplyChapterEditInput
operation
  String should match pattern '^(append|replace|insert)$' [type=string_pattern_mismatch, input_value='insert_at_start', input_type=str]
    For further information visit https://errors.pydantic.dev/2.12/v/string_pattern_mismatch
2026-01-10 02:17:00,900 - app.services.agent.execution.tool_executor - INFO - [LegacyTool] 使用 @tool 版本: apply_chapter_edit
2026-01-10 02:17:00,906 - app.api.v1.agent - INFO - [Stream] 任务完成: 在第二章“浑圆桩”的开头插入一段环境描写 (0.0s)
2026-01-10 02:17:00,906 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务6完成
2026-01-10 02:17:00,907 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共6个任务，耗时: 32.39s
2026-01-10 02:17:00,907 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2026-01-10 02:17:00,907 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=2, 输出型=4, 展示型=0
2026-01-10 02:17:00,909 - app.services.agent.langgraph_agent - INFO - [Response] 4个输出任务（含续写），使用AI整合
2026-01-10 02:17:00,909 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2026-01-10 02:17:00,910 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=2, 输出型=4, 展示型=0
2026-01-10 02:17:00,910 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=17519字符, 处理后=5144字符
2026-01-10 02:17:00,910 - app.services.agent.planning.response_builder - INFO - [Summarization] 准备发送 summarization_start 事件
2026-01-10 02:17:00,911 - app.services.agent.stream.stream_event_handler - INFO - [StreamEventHandler] emit_summarization_start 被调用, _on_flow_event=True
2026-01-10 02:17:00,911 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_start 事件已发送
2026-01-10 02:17:00,912 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2026-01-10 02:17:00,912 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2026-01-10 02:17:00,920 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-10 02:17:00,921 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-10 02:17:00,922 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
2026-01-10 02:17:06,663 - app.api.v1.agent - INFO - [Approval] 章节标题已修改: chapter_id=5ebe6c74-ed96-4573-8bf2-98a460aeef7d, new_title=魂穿异域，器灵觉醒
2026-01-10 02:17:06,667 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/approval-response
INFO:     127.0.0.1:61222 - "POST /api/v1/agent/chat/approval-response HTTP/1.1" 200 OK
2026-01-10 02:17:06,684 - app.api.v1.chapters - INFO - [GET chapters] work_id=008150f0-1fc8-46ca-b1a7-facc70b16da6, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-10 02:17:06,689 - app.api.v1.chapters - INFO - ⚠️ [GET chapters] 缓存未命中: chapters:work:008150f0-1fc8-46ca-b1a7-facc70b16da6
2026-01-10 02:17:06,689 - app.services.chapter_service - INFO - [ChapterService] Querying chapters for work_id=008150f0-1fc8-46ca-b1a7-facc70b16da6, type=<class 'uuid.UUID'>
2026-01-10 02:17:06,692 - app.services.chapter_service - INFO - [ChapterService] Found 3 chapters
2026-01-10 02:17:06,692 - app.services.chapter_service - INFO -   - Chapter: 第1章 吞噬, order=1
2026-01-10 02:17:06,692 - app.services.chapter_service - INFO -   - ... (1 more chapters)
2026-01-10 02:17:06,693 - app.services.chapter_service - INFO -   - Chapter: 魂穿异域，器灵觉醒, order=3
2026-01-10 02:17:06,693 - app.api.v1.chapters - INFO - [GET chapters] Returning 3 chapters
2026-01-10 02:17:06,696 - app.api.v1.chapters - INFO - 💾 [GET chapters] 缓存已保存: chapters:work:008150f0-1fc8-46ca-b1a7-facc70b16da6 (expire=60s)
2026-01-10 02:17:06,697 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/work/008150f0-1fc8-46ca-b1a7-facc70b16da6
INFO:     127.0.0.1:61225 - "GET /api/v1/chapters/work/008150f0-1fc8-46ca-b1a7-facc70b16da6 HTTP/1.1" 200 OK
2026-01-10 02:17:09,763 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:008150f0-1fc8-46ca-b1a7-facc70b16da6
2026-01-10 02:17:09,763 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/5ebe6c74-ed96-4573-8bf2-98a460aeef7d
INFO:     127.0.0.1:59615 - "PUT /api/v1/chapters/5ebe6c74-ed96-4573-8bf2-98a460aeef7d HTTP/1.1" 200 OK
2026-01-10 02:17:09,763 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 魂穿异域，器灵觉醒 (order=3)
2026-01-10 02:17:10,239 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 魂穿异域，器灵觉醒 (5 chunks)
2026-01-10 02:17:10,272 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:008150f0-1fc8-46ca-b1a7-facc70b16da6
2026-01-10 02:17:10,273 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/5ebe6c74-ed96-4573-8bf2-98a460aeef7d
INFO:     127.0.0.1:59618 - "PUT /api/v1/chapters/5ebe6c74-ed96-4573-8bf2-98a460aeef7d HTTP/1.1" 200 OK
2026-01-10 02:17:10,276 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 魂穿异域，器灵觉醒 (order=3)
2026-01-10 02:17:10,742 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 魂穿异域，器灵觉醒 (5 chunks)
2026-01-10 02:17:16,851 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-10 02:17:16,853 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_complete 事件已发送（第一个chunk时）
2026-01-10 02:17:16,854 - app.services.agent.planning.response_builder - INFO - [Summarization] output_ready 事件已发送（第一个chunk时）
2026-01-10 02:17:22,312 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 18 个数据块，总长度: 1733
2026-01-10 02:17:22,314 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 7347 (prompt=6162, completion=1185)
2026-01-10 02:17:22,315 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-10 02:17:22,317 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-10 02:17:22,339 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-10 02:17:22,342 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=7347, cost=$0.004811, time=21394ms
2026-01-10 02:17:22,346 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=1733
2026-01-10 02:17:27,089 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:008150f0-1fc8-46ca-b1a7-facc70b16da6 | 重要度=0.84
2026-01-10 02:17:31,932 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:008150f0-1fc8-46ca-b1a7-facc70b16da6 | 重要度=0.77
2026-01-10 02:17:31,973 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:008150f0-1fc8-46ca-b1a7-facc70b16da6:671e74fa-e2d8-476f-9e8d-2043edf79a27, token=2110
2026-01-10 02:17:31,979 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:008150f0-1fc8-46ca-b1a7-facc70b16da6:671e74fa-e2d8-476f-9e8d-2043edf79a27, 消息数=2, Token=2110
2026-01-10 02:17:31,981 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:008150f0-1fc8-46ca-b1a7-facc70b16da6:671e74fa-e2d8-476f-9e8d-2043edf79a27)
2026-01-10 02:17:31,982 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2026-01-10 02:17:32,002 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream complete