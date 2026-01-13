INFO:     127.0.0.1:57397 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2026-01-13 12:51:27,080 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 你现在在第5章页面，但我要修改第2章与第3章的内容，严格走跨章节定位与修订流程。请按步骤执行，不要省...
2026-01-13 12:51:27,098 - app.api.v1.agent - INFO - [agent_chat_stream] 📚 世界观数据已注入: 人物=8, 地点=6, 设定=6, 规范=无
2026-01-13 12:51:27,099 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:48e063af-6b4d-4911-817c-b5dc41d863b9:85422cf3-a26c-4dd4-a949-181434cd410b (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=48e063af-6b4d-4911-817c-b5dc41d863b9, conversation_id=85422cf3-a26c-4dd4-a949-181434cd410b)
2026-01-13 12:51:27,101 - app.services.context.manager - INFO - [ContextManager] 创建新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:48e063af-6b4d-4911-817c-b5dc41d863b9:85422cf3-a26c-4dd4-a949-181434cd410b
2026-01-13 12:51:27,102 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:48e063af-6b4d-4911-817c-b5dc41d863b9:85422cf3-a26c-4dd4-a949-181434cd410b: 0/16000 tokens
2026-01-13 12:51:27,572 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='你现在在第5章页面，但我要修改第2章与第3章的内容，严格走跨...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:48e063af-6b4d-4911-817c-b5dc41d863b9', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=3条
2026-01-13 12:51:27,573 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=48e063af-6b4d-4911-817c-b5dc41d863b9 | 含用户级=True | 找到=3条
2026-01-13 12:51:27,573 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 1条消息, 0 tokens, 耗时 472.71ms
2026-01-13 12:51:27,574 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 1 条历史消息 (token: 0, has_summary: False)
2026-01-13 12:51:27,575 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-13 12:51:27,576 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-13 12:51:27,576 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=20, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-13 12:51:29,508 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-13 12:51:29,509 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-13 12:51:29,539 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-13 12:51:29,540 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=808, cost=$0.000081, time=1933ms
2026-01-13 12:51:29,542 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=7, 尝试次数=1
2026-01-13 12:51:29,543 - app.services.agent.intent.classifier - INFO - [Intent] AI识别结果: writing
2026-01-13 12:51:29,544 - app.services.agent.langgraph_agent - INFO - [Planning] AI意图分类: writing (置信度: 0.90)
2026-01-13 12:51:29,545 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 你现在在第5章页面，但我要修改第2章与第3章的内容，严格走跨章节定位与修订流程。请按步骤执行，不要省...
2026-01-13 12:51:29,554 - app.core.cache - INFO - ✅ 缓存命中: prompt:planning:v2.39.0:get_planning_static_prompt:fca6eb91156619d0
2026-01-13 12:51:29,563 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-13 12:51:29,564 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=story_planning, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: story_planning; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-01-13 12:51:29,564 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.3, task_type=TaskType.STORY_PLANNING
2026-01-13 12:51:43,880 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-13 12:51:56,340 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 27 个数据块，总长度: 3834
2026-01-13 12:51:56,340 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 24687 (prompt=22937, completion=1750)
2026-01-13 12:51:56,340 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-13 12:51:56,340 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-13 12:51:56,344 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-13 12:51:56,344 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=24687, cost=$0.046171, time=26775ms
2026-01-13 12:51:56,344 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=24687
2026-01-13 12:51:56,344 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户要求执行一个严格的多步骤、跨章节的编辑任务。具体包括：1, 原料=1. 需要同时读取第2章和第3章的内容。, 处理=1.  **`get_writing_c
2026-01-13 12:51:56,344 - app.services.agent.planning.plan_generator - INFO - [Planning] 直接回答模式，答案长度: 101
2026-01-13 12:51:56,344 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共7个任务
2026-01-13 12:51:56,344 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共7个任务，耗时: 26.80s
2026-01-13 12:51:56,344 - app.api.v1.agent - INFO - [Stream] Plan tasks: 7 items
2026-01-13 12:51:56,344 - app.services.agent.langgraph_agent - WARNING - [Planning-Alert] AI 违反协议：同时返回 direct_answer(101字) 和 7 个 tasks，将执行 tasks 而忽略 direct_answer
2026-01-13 12:51:56,344 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2026-01-13 12:51:56,352 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2026-01-13 12:51:56,352 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2026-01-13 12:51:56,353 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 任务分组: 第一层并行=0, 第二层并行=0, 串行=7
2026-01-13 12:51:56,353 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 开始串行执行7个任务
2026-01-13 12:51:56,353 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务1开始: 获取第2章与第3章的上下文内容
2026-01-13 12:51:56,353 - app.api.v1.agent - INFO - [Stream] Task started: 获取第2章与第3章的上下文内容 (icon=Wrench)
2026-01-13 12:51:56,353 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: get_writing_context
2026-01-13 12:51:56,355 - app.services.agent.tools.tool_types - INFO - [get_writing_context] 开始执行工具
2026-01-13 12:51:56,355 - app.services.agent.langgraph_tools - INFO - [get_writing_context] ✅ 获取创作上下文成功: include=chapter
2026-01-13 12:51:56,365 - app.services.agent.tools.tool_types - INFO - [get_writing_context] 执行成功 (耗时: 0.010s)
2026-01-13 12:51:56,365 - app.services.agent.execution.tool_executor - INFO - [StandardTool] get_writing_context 执行成功
2026-01-13 12:51:56,365 - app.services.agent.utils.chapter_cache - INFO - [ChapterCache] 📝 写入: 7356bc11... (第2章)
2026-01-13 12:51:56,365 - app.services.agent.utils.chapter_cache - INFO - [ChapterCache] 📝 写入: 7f9ecac9... (第3章)
2026-01-13 12:51:56,365 - app.services.agent.execution.tool_executor - INFO - [ChapterCache] 📝 get_writing_context 缓存写入: 2 章
2026-01-13 12:51:56,365 - app.api.v1.agent - INFO - [Stream] 任务完成: 获取第2章与第3章的上下文内容 (0.0s)
2026-01-13 12:51:56,365 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务1完成
2026-01-13 12:51:56,365 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务2开始: 在第2章中定位目标句子
2026-01-13 12:51:56,365 - app.api.v1.agent - INFO - [Stream] Task started: 在第2章中定位目标句子 (icon=Wrench)
2026-01-13 12:51:56,368 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 解析占位符: $TASK_1.chapters[0].id$
2026-01-13 12:51:56,368 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 任务1结果长度: 4980
2026-01-13 12:51:56,368 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 解析路径 chapters[0].id -> tokens: ['chapters', 0, 'id']
2026-01-13 12:51:56,368 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] $TASK_1.chapters[0].id$ → str: 7356bc11-2cde-49ca-a45c-d2926ff7f4ae
2026-01-13 12:51:56,368 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: locate_content
2026-01-13 12:51:56,368 - app.services.agent.tools.locate_tools - INFO - [locate_content] 开始定位: chapter_id=7356bc11-2cde-49ca-a45c-d2926ff7f4ae, query=这怎么回事？一点也不顺手了……倒像是攥了一把新刀……
2026-01-13 12:51:56,368 - app.services.agent.tools.locate_tools - INFO - [locate_content] 收到 70 个节点信息
2026-01-13 12:51:56,368 - app.services.agent.tools.locate_tools - INFO - [locate_content] 章节共 65 个段落
2026-01-13 12:51:56,386 - app.services.agent.tools.locate_tools - INFO - [locate_content] 模糊匹配结果: None
2026-01-13 12:51:56,386 - app.services.agent.tools.locate_tools - INFO - [locate_content] 无模糊匹配结果，尝试 LLM 辅助定位
2026-01-13 12:51:56,386 - app.services.agent.tools.locate_tools - INFO - [_llm_assisted_locate] 开始调用 LLM，候选数量: 8
2026-01-13 12:51:56,386 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-13 12:51:56,386 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-13 12:51:56,386 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=10, temp=0.1, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-13 12:51:57,953 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-13 12:51:57,953 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-13 12:51:57,979 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-13 12:51:57,981 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=335, cost=$0.000034, time=1566ms
2026-01-13 12:51:57,981 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=1, 尝试次数=1
2026-01-13 12:51:57,982 - app.services.agent.tools.locate_tools - INFO - [_llm_assisted_locate] LLM 选择候选 6 → 原始第 15 段
2026-01-13 12:51:57,983 - app.services.agent.tools.locate_tools - INFO - [locate_content] LLM 辅助定位返回: (14, 0.85)
2026-01-13 12:51:57,983 - app.services.agent.tools.locate_tools - INFO - [locate_content] LLM 辅助定位成功: 第15段
2026-01-13 12:51:57,985 - app.services.agent.execution.tool_executor - INFO - [StandardTool] locate_content 执行成功
2026-01-13 12:51:57,986 - app.api.v1.agent - INFO - [Stream] 任务完成: 在第2章中定位目标句子 (1.6s)
2026-01-13 12:51:57,987 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务2完成
2026-01-13 12:51:57,987 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务3开始: 为第2章生成更细腻的替换句
2026-01-13 12:51:57,988 - app.api.v1.agent - INFO - [Stream] Task started: 为第2章生成更细腻的替换句 (icon=Edit3)
2026-01-13 12:51:57,988 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 解析占位符: $TASK_2.chapter_id$
2026-01-13 12:51:57,989 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 任务2结果长度: 473
2026-01-13 12:51:57,989 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 解析路径 chapter_id -> tokens: ['chapter_id']
2026-01-13 12:51:57,990 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] $TASK_2.chapter_id$ → str: 7356bc11-2cde-49ca-a45c-d2926ff7f4ae
2026-01-13 12:51:57,991 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 解析占位符: $TASK_2.text$
2026-01-13 12:51:57,991 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 任务2结果长度: 473
2026-01-13 12:51:57,992 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 解析路径 text -> tokens: ['text']
2026-01-13 12:51:57,992 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] $TASK_2.text$ → str: 赵穆见段融如此，心头涌起的火气，下来了一大半，他接过刀来，将手中的废刀，放在了段融手上，微怒道：“归队吧！”
2026-01-13 12:51:57,994 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: smart_rewrite
2026-01-13 12:51:57,994 - app.services.agent.tools.tool_types - INFO - [smart_rewrite] 开始执行工具
2026-01-13 12:51:58,001 - app.services.agent.tools.editor_tools - INFO - [smart_rewrite] 开始生成改写版本，原文长度: 54, 用户要求: 改写得更细腻，长度相近，保留“门道”二字，体现“意识无法介入”的无力感, 基准版本: 无
2026-01-13 12:51:58,002 - app.services.agent.tools.editor_tools - INFO - [smart_rewrite] 使用传统单Prompt架构
2026-01-13 12:51:58,002 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-13 12:51:58,002 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=content_creation, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro
2026-01-13 12:51:58,003 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=4000, temp=0.8, 尝试=1/3, task_type=TaskType.CONTENT_CREATION
2026-01-13 12:52:23,086 - app.services.knowledge_service - INFO - 查询知识条目: user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, total=4, returned=4
2026-01-13 12:52:23,090 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/knowledge
INFO:     127.0.0.1:60126 - "GET /api/v1/knowledge?skip=0&limit=20 HTTP/1.1" 200 OK
2026-01-13 12:52:25,054 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-13 12:52:25,060 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-13 12:52:25,111 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-13 12:52:25,118 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=3122, cost=$0.006720, time=27062ms
2026-01-13 12:52:25,119 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=491, 尝试次数=1
2026-01-13 12:52:25,120 - app.services.agent.tools.editor_tools - INFO - [smart_rewrite] AI返回长度: 491
2026-01-13 12:52:25,123 - app.services.agent.tools.editor_tools - INFO - [smart_rewrite] 成功生成3个改写版本
2026-01-13 12:52:25,127 - app.services.agent.tools.tool_types - INFO - [smart_rewrite] 执行成功 (耗时: 27.133s)
2026-01-13 12:52:25,129 - app.services.agent.execution.tool_executor - INFO - [StandardTool] smart_rewrite 执行成功
2026-01-13 12:52:25,131 - app.api.v1.agent - INFO - [Stream] 任务完成: 为第2章生成更细腻的替换句 (27.1s)
2026-01-13 12:52:25,133 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务3完成
2026-01-13 12:52:25,136 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务4开始: 将替换句应用到第2章编辑器
2026-01-13 12:52:25,143 - app.api.v1.agent - INFO - [Stream] Task started: 将替换句应用到第2章编辑器 (icon=Check)
2026-01-13 12:52:25,145 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 解析占位符: $TASK_2.chapter_id$
2026-01-13 12:52:25,145 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 任务2结果长度: 473
2026-01-13 12:52:25,145 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 解析路径 chapter_id -> tokens: ['chapter_id']
2026-01-13 12:52:25,150 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] $TASK_2.chapter_id$ → str: 7356bc11-2cde-49ca-a45c-d2926ff7f4ae
2026-01-13 12:52:25,151 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 解析占位符: $TASK_3.versions[0].content$
2026-01-13 12:52:25,152 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 任务3结果长度: 645
2026-01-13 12:52:25,153 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 解析路径 versions[0].content -> tokens: ['versions', 0, 'content']
2026-01-13 12:52:25,156 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] $TASK_3.versions[0].content$ → str: 段融那副模样，让赵穆心头火气一滞，意识尚未跟上，手已换过了刀。他将废刀塞入段融手中，暗忖这其中门道他还差得远，只剩一丝余怒道：“归队吧！”
2026-01-13 12:52:25,156 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 解析占位符: $TASK_2.node_id$
2026-01-13 12:52:25,158 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 任务2结果长度: 473
2026-01-13 12:52:25,160 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 解析路径 node_id -> tokens: ['node_id']
2026-01-13 12:52:25,166 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] $TASK_2.node_id$ → str: 6nf35ycf
2026-01-13 12:52:25,169 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 解析占位符: $TASK_2.paragraph_index$
2026-01-13 12:52:25,170 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 任务2结果长度: 473
2026-01-13 12:52:25,172 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 解析路径 paragraph_index -> tokens: ['paragraph_index']
2026-01-13 12:52:25,173 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] $TASK_2.paragraph_index$ → int: 14
2026-01-13 12:52:25,175 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 解析占位符: $TASK_2.before_anchor$
2026-01-13 12:52:25,178 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 任务2结果长度: 473
2026-01-13 12:52:25,179 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 解析路径 before_anchor -> tokens: ['before_anchor']
2026-01-13 12:52:25,181 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] $TASK_2.before_anchor$ → str: ，但他站了起来，将手中刀，插进刀鞘，双手捧着，献于赵穆身前。
2026-01-13 12:52:25,183 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 解析占位符: $TASK_2.after_anchor$
2026-01-13 12:52:25,187 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 任务2结果长度: 473
2026-01-13 12:52:25,190 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 解析路径 after_anchor -> tokens: ['after_anchor']
2026-01-13 12:52:25,194 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] $TASK_2.after_anchor$ → str: 段融抬头看着两手捧着的废刀，似是好一会儿才反应过来一般，拿着
2026-01-13 12:52:25,199 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 解析占位符: $TASK_2.text$
2026-01-13 12:52:25,203 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 任务2结果长度: 473
2026-01-13 12:52:25,206 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 解析路径 text -> tokens: ['text']
2026-01-13 12:52:25,210 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] $TASK_2.text$ → str: 赵穆见段融如此，心头涌起的火气，下来了一大半，他接过刀来，将手中的废刀，放在了段融手上，微怒道：“归队吧！”
2026-01-13 12:52:25,212 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: apply_chapter_edit
2026-01-13 12:52:25,215 - app.services.agent.tools.tool_types - INFO - [apply_chapter_edit] 开始执行工具
2026-01-13 12:52:25,226 - app.services.agent.tools.editor_tools - INFO - [apply_chapter_edit] 参数: chapter_id=7356bc11-2cde-49ca-a45c-d2926ff7f4ae, operation=replace, content_len=69
2026-01-13 12:52:25,329 - app.services.chapter_word_stat_service - INFO - 记录字数增量: chapter_id=7356bc11-2cde-49ca-a45c-d2926ff7f4ae, delta=15, edit_event_id=None
2026-01-13 12:52:25,337 - app.services.agent.tools.operation_log - INFO - [OperationLog] 记录操作: update_content - update content (replace)
2026-01-13 12:52:25,339 - app.services.agent.tools.tool_types - INFO - [apply_chapter_edit] 执行成功 (耗时: 0.124s)
2026-01-13 12:52:25,342 - app.services.agent.execution.tool_executor - INFO - [StandardTool] apply_chapter_edit 执行成功
2026-01-13 12:52:25,351 - app.api.v1.agent - INFO - [Stream] 任务完成: 将替换句应用到第2章编辑器 (0.2s)
2026-01-13 12:52:25,352 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务4完成
2026-01-13 12:52:25,354 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务5开始: 在第3章中定位插入位置
2026-01-13 12:52:25,355 - app.api.v1.agent - INFO - [Stream] Task started: 在第3章中定位插入位置 (icon=Wrench)
2026-01-13 12:52:25,357 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 解析占位符: $TASK_1.chapters[1].id$
2026-01-13 12:52:25,358 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 任务1结果长度: 4980
2026-01-13 12:52:25,361 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 解析路径 chapters[1].id -> tokens: ['chapters', 1, 'id']
2026-01-13 12:52:25,362 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] $TASK_1.chapters[1].id$ → str: 7f9ecac9-5dca-4340-93f8-ea58738193c3
2026-01-13 12:52:25,363 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: locate_content
2026-01-13 12:52:25,363 - app.services.agent.tools.locate_tools - INFO - [locate_content] 开始定位: chapter_id=7f9ecac9-5dca-4340-93f8-ea58738193c3, query=段融站了一会儿，周身已经开始冒热气，他能明显感到气脉在奔腾一般，但他的意识却无法介入进去。
2026-01-13 12:52:25,364 - app.services.agent.tools.locate_tools - INFO - [locate_content] 收到 70 个节点信息
2026-01-13 12:52:25,381 - app.services.agent.tools.locate_tools - INFO - [locate_content] 章节共 64 个段落
2026-01-13 12:52:25,383 - app.services.agent.tools.locate_tools - INFO - [locate_content] 定位到开头
2026-01-13 12:52:25,385 - app.services.agent.execution.tool_executor - INFO - [StandardTool] locate_content 执行成功
2026-01-13 12:52:25,387 - app.api.v1.agent - INFO - [Stream] 任务完成: 在第3章中定位插入位置 (0.0s)
2026-01-13 12:52:25,388 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务5完成
2026-01-13 12:52:25,389 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务6开始: 为第3章生成关于意识旁观的段落
2026-01-13 12:52:25,390 - app.api.v1.agent - INFO - [Stream] Task started: 为第3章生成关于意识旁观的段落 (icon=Plus)
2026-01-13 12:52:25,390 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 解析占位符: $TASK_5.chapter_id$
2026-01-13 12:52:25,393 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 任务5结果长度: 312
2026-01-13 12:52:25,396 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 解析路径 chapter_id -> tokens: ['chapter_id']
2026-01-13 12:52:25,398 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] $TASK_5.chapter_id$ → str: 7f9ecac9-5dca-4340-93f8-ea58738193c3
2026-01-13 12:52:25,400 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 解析占位符: $TASK_5.text$
2026-01-13 12:52:25,405 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 任务5结果长度: 312
2026-01-13 12:52:25,412 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 解析路径 text -> tokens: ['text']
2026-01-13 12:52:25,415 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] $TASK_5.text$ → str: 段融这一夜，仿佛一直处在梦境中……
2026-01-13 12:52:25,419 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: smart_insert
2026-01-13 12:52:25,421 - app.services.agent.tools.tool_types - INFO - [smart_insert] 开始执行工具
2026-01-13 12:52:25,443 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-13 12:52:25,445 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=content_creation, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro
2026-01-13 12:52:25,445 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=300, temp=0.8, 尝试=1/3, task_type=TaskType.CONTENT_CREATION
INFO:     127.0.0.1:60136 - "OPTIONS /api/v1/humanize/history?page=1&page_size=10 HTTP/1.1" 200 OK
INFO:     127.0.0.1:64808 - "OPTIONS /api/v1/humanize/profile HTTP/1.1" 200 OK
INFO:     127.0.0.1:54959 - "OPTIONS /api/v1/humanize/history?page=1&page_size=10 HTTP/1.1" 200 OK
INFO:     127.0.0.1:52260 - "OPTIONS /api/v1/humanize/profile HTTP/1.1" 200 OK
2026-01-13 12:52:26,273 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/humanize/profile
INFO:     127.0.0.1:64808 - "GET /api/v1/humanize/profile HTTP/1.1" 200 OK
2026-01-13 12:52:26,307 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/humanize/history
INFO:     127.0.0.1:60136 - "GET /api/v1/humanize/history?page=1&page_size=10 HTTP/1.1" 200 OK
2026-01-13 12:52:26,311 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/humanize/profile
INFO:     127.0.0.1:52260 - "GET /api/v1/humanize/profile HTTP/1.1" 200 OK
2026-01-13 12:52:26,342 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/humanize/history
INFO:     127.0.0.1:60136 - "GET /api/v1/humanize/history?page=1&page_size=10 HTTP/1.1" 200 OK
2026-01-13 12:52:32,200 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/available-channels
INFO:     127.0.0.1:64261 - "GET /api/v1/channels/available-channels?params%5Bskip%5D=0&params%5Blimit%5D=20 HTTP/1.1" 200 OK
2026-01-13 12:52:32,227 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/my-channels
INFO:     127.0.0.1:64262 - "GET /api/v1/channels/my-channels HTTP/1.1" 200 OK
2026-01-13 12:52:32,262 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/available-channels
INFO:     127.0.0.1:64264 - "GET /api/v1/channels/available-channels?params%5Bskip%5D=0&params%5Blimit%5D=20 HTTP/1.1" 200 OK
2026-01-13 12:52:32,302 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/my-channels
INFO:     127.0.0.1:64266 - "GET /api/v1/channels/my-channels HTTP/1.1" 200 OK
INFO:     ('127.0.0.1', 54140) - "WebSocket /api/v1/ws/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3OTkxM2U3ZS1kNWNkLTRlMDktYmNlNi1jYTY2MzliZDg0NTYiLCJleHAiOjE3NjgyODI5MjEsInR5cGUiOiJhY2Nlc3MifQ.BieEn6fVM9HiDvlxVC-4n0nbKZNkG-EwRE4QXcwRjl4" [accepted]
INFO:     connection open
INFO:     ('127.0.0.1', 59540) - "WebSocket /api/v1/ws/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3OTkxM2U3ZS1kNWNkLTRlMDktYmNlNi1jYTY2MzliZDg0NTYiLCJleHAiOjE3NjgyODI5MjEsInR5cGUiOiJhY2Nlc3MifQ.BieEn6fVM9HiDvlxVC-4n0nbKZNkG-EwRE4QXcwRjl4" [accepted]
INFO:     connection open
INFO:     connection closed
2026-01-13 12:52:32,531 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/friends/requests/count
INFO:     127.0.0.1:59866 - "GET /api/v1/friends/requests/count HTTP/1.1" 200 OK
2026-01-13 12:52:32,578 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9/members
2026-01-13 12:52:32,584 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/friends
INFO:     127.0.0.1:59869 - "GET /api/v1/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9/members HTTP/1.1" 200 OK
2026-01-13 12:52:32,602 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9/unread-info
INFO:     127.0.0.1:59861 - "GET /api/v1/friends?skip=0&limit=50 HTTP/1.1" 200 OK
2026-01-13 12:52:32,611 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9/pinned-messages
INFO:     127.0.0.1:59868 - "GET /api/v1/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9/unread-info HTTP/1.1" 200 OK
INFO:     127.0.0.1:59867 - "GET /api/v1/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9/pinned-messages HTTP/1.1" 200 OK
2026-01-13 12:52:32,837 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/friends/requests/count
2026-01-13 12:52:32,872 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9/latest-announcement
INFO:     127.0.0.1:57964 - "GET /api/v1/friends/requests/count HTTP/1.1" 200 OK
INFO:     127.0.0.1:50422 - "GET /api/v1/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9/latest-announcement HTTP/1.1" 200 OK
2026-01-13 12:52:32,917 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9/members
INFO:     127.0.0.1:63162 - "GET /api/v1/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9/members HTTP/1.1" 200 OK
2026-01-13 12:52:33,009 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/friends
INFO:     127.0.0.1:52622 - "GET /api/v1/friends?skip=0&limit=50 HTTP/1.1" 200 OK
2026-01-13 12:52:33,078 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9/pinned-messages
2026-01-13 12:52:33,080 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9/messages
INFO:     127.0.0.1:53302 - "GET /api/v1/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9/pinned-messages HTTP/1.1" 200 OK
INFO:     127.0.0.1:53091 - "GET /api/v1/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9/messages?params%5Bskip%5D=0&params%5Blimit%5D=50 HTTP/1.1" 200 OK
2026-01-13 12:52:33,111 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9/unread-info
INFO:     127.0.0.1:51769 - "GET /api/v1/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9/unread-info HTTP/1.1" 200 OK
2026-01-13 12:52:33,139 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9/latest-announcement
INFO:     127.0.0.1:59620 - "GET /api/v1/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9/latest-announcement HTTP/1.1" 200 OK
2026-01-13 12:52:33,150 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9/mark-read
INFO:     127.0.0.1:61437 - "POST /api/v1/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9/mark-read HTTP/1.1" 200 OK
2026-01-13 12:52:33,177 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9/members
INFO:     127.0.0.1:50159 - "GET /api/v1/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9/members HTTP/1.1" 200 OK
2026-01-13 12:52:33,194 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9/latest-announcement
INFO:     127.0.0.1:51535 - "GET /api/v1/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9/latest-announcement HTTP/1.1" 200 OK
2026-01-13 12:52:33,225 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9/latest-announcement
INFO:     127.0.0.1:63076 - "GET /api/v1/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9/latest-announcement HTTP/1.1" 200 OK
2026-01-13 12:52:33,320 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9/latest-announcement
INFO:     127.0.0.1:63917 - "GET /api/v1/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9/latest-announcement HTTP/1.1" 200 OK
2026-01-13 12:52:33,359 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/invite/UZ7CMmgT/preview
INFO:     127.0.0.1:63916 - "GET /api/v1/channels/invite/UZ7CMmgT/preview HTTP/1.1" 400 Bad Request
2026-01-13 12:52:33,452 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/invite/UZ7CMmgT/preview
INFO:     127.0.0.1:63195 - "GET /api/v1/channels/invite/UZ7CMmgT/preview HTTP/1.1" 400 Bad Request
INFO:     connection closed
INFO:     ('127.0.0.1', 63817) - "WebSocket /api/v1/ws/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3OTkxM2U3ZS1kNWNkLTRlMDktYmNlNi1jYTY2MzliZDg0NTYiLCJleHAiOjE3NjgyODI5MjEsInR5cGUiOiJhY2Nlc3MifQ.BieEn6fVM9HiDvlxVC-4n0nbKZNkG-EwRE4QXcwRjl4" [accepted]
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 62306) - "WebSocket /api/v1/ws/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3OTkxM2U3ZS1kNWNkLTRlMDktYmNlNi1jYTY2MzliZDg0NTYiLCJleHAiOjE3NjgyODI5MjEsInR5cGUiOiJhY2Nlc3MifQ.BieEn6fVM9HiDvlxVC-4n0nbKZNkG-EwRE4QXcwRjl4" [accepted]
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 57052) - "WebSocket /api/v1/ws/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3OTkxM2U3ZS1kNWNkLTRlMDktYmNlNi1jYTY2MzliZDg0NTYiLCJleHAiOjE3NjgyODI5MjEsInR5cGUiOiJhY2Nlc3MifQ.BieEn6fVM9HiDvlxVC-4n0nbKZNkG-EwRE4QXcwRjl4" [accepted]
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 55246) - "WebSocket /api/v1/ws/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3OTkxM2U3ZS1kNWNkLTRlMDktYmNlNi1jYTY2MzliZDg0NTYiLCJleHAiOjE3NjgyODI5MjEsInR5cGUiOiJhY2Nlc3MifQ.BieEn6fVM9HiDvlxVC-4n0nbKZNkG-EwRE4QXcwRjl4" [accepted]
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 64828) - "WebSocket /api/v1/ws/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3OTkxM2U3ZS1kNWNkLTRlMDktYmNlNi1jYTY2MzliZDg0NTYiLCJleHAiOjE3NjgyODI5MjEsInR5cGUiOiJhY2Nlc3MifQ.BieEn6fVM9HiDvlxVC-4n0nbKZNkG-EwRE4QXcwRjl4" [accepted]
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 51195) - "WebSocket /api/v1/ws/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3OTkxM2U3ZS1kNWNkLTRlMDktYmNlNi1jYTY2MzliZDg0NTYiLCJleHAiOjE3NjgyODI5MjEsInR5cGUiOiJhY2Nlc3MifQ.BieEn6fVM9HiDvlxVC-4n0nbKZNkG-EwRE4QXcwRjl4" [accepted]
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 53619) - "WebSocket /api/v1/ws/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3OTkxM2U3ZS1kNWNkLTRlMDktYmNlNi1jYTY2MzliZDg0NTYiLCJleHAiOjE3NjgyODI5MjEsInR5cGUiOiJhY2Nlc3MifQ.BieEn6fVM9HiDvlxVC-4n0nbKZNkG-EwRE4QXcwRjl4" [accepted]
INFO:     connection open
2026-01-13 12:52:45,867 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/stickers/my
2026-01-13 12:52:45,869 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/stickers/favorites
INFO:     127.0.0.1:50322 - "GET /api/v1/stickers/my?skip=0&limit=50 HTTP/1.1" 200 OK
INFO:     127.0.0.1:50323 - "GET /api/v1/stickers/favorites?skip=0&limit=50 HTTP/1.1" 200 OK
2026-01-13 12:52:45,934 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/stickers/my
INFO:     127.0.0.1:54725 - "GET /api/v1/stickers/my?skip=0&limit=50 HTTP/1.1" 200 OK
2026-01-13 12:52:45,950 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/stickers/favorites
INFO:     127.0.0.1:54727 - "GET /api/v1/stickers/favorites?skip=0&limit=50 HTTP/1.1" 200 OK
2026-01-13 12:52:46,659 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-13 12:52:46,661 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-13 12:52:46,671 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-13 12:52:46,673 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=3263, cost=$0.005067, time=21215ms
2026-01-13 12:52:46,673 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=137, 尝试次数=1
2026-01-13 12:52:46,676 - app.services.agent.tools.tool_types - INFO - [smart_insert] 执行成功 (耗时: 21.255s)
2026-01-13 12:52:46,676 - app.services.agent.execution.tool_executor - INFO - [StandardTool] smart_insert 执行成功
2026-01-13 12:52:46,676 - app.api.v1.agent - INFO - [Stream] 任务完成: 为第3章生成关于意识旁观的段落 (21.3s)
2026-01-13 12:52:46,676 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务6完成
2026-01-13 12:52:46,676 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务7开始: 将新段落应用到第3章编辑器
2026-01-13 12:52:46,680 - app.api.v1.agent - INFO - [Stream] Task started: 将新段落应用到第3章编辑器 (icon=Check)
2026-01-13 12:52:46,680 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 解析占位符: $TASK_5.chapter_id$
2026-01-13 12:52:46,680 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 任务5结果长度: 312
2026-01-13 12:52:46,680 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 解析路径 chapter_id -> tokens: ['chapter_id']
2026-01-13 12:52:46,680 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] $TASK_5.chapter_id$ → str: 7f9ecac9-5dca-4340-93f8-ea58738193c3
2026-01-13 12:52:46,680 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 解析占位符: $TASK_6.content$
2026-01-13 12:52:46,680 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 任务6结果长度: 303
2026-01-13 12:52:46,680 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 解析路径 content -> tokens: ['content']
2026-01-13 12:52:46,683 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] $TASK_6.content$ → str: 他“看见”一个壮硕人影在练刀，视角却无比诡异。他并非旁观，而是仿佛化作了那人身体里的内息，随着刀势在经脉中奔腾流转。他的神识只是一个渺小的浮萍，在这股洪流中身不由己，只能被动地承接着。那人毕生的苦练与
2026-01-13 12:52:46,683 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 解析占位符: $TASK_5.node_id$
2026-01-13 12:52:46,683 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 任务5结果长度: 312
2026-01-13 12:52:46,683 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 解析路径 node_id -> tokens: ['node_id']
2026-01-13 12:52:46,684 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] $TASK_5.node_id$ → str: hicij01s
2026-01-13 12:52:46,685 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 解析占位符: $TASK_5.paragraph_index$
2026-01-13 12:52:46,685 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 任务5结果长度: 312
2026-01-13 12:52:46,685 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 解析路径 paragraph_index -> tokens: ['paragraph_index']
2026-01-13 12:52:46,685 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] $TASK_5.paragraph_index$ → int: 0
2026-01-13 12:52:46,685 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 解析占位符: $TASK_5.after_anchor$
2026-01-13 12:52:46,685 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 任务5结果长度: 312
2026-01-13 12:52:46,685 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 解析路径 after_anchor -> tokens: ['after_anchor']
2026-01-13 12:52:46,685 - app.services.agent.parameter_resolver - WARNING - [ParameterResolver] 字段 after_anchor 不存在于 dict，降级返回完整结果
2026-01-13 12:52:46,685 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: apply_chapter_edit
2026-01-13 12:52:46,685 - app.services.agent.tools.tool_types - INFO - [apply_chapter_edit] 开始执行工具
2026-01-13 12:52:46,691 - app.services.agent.tools.editor_tools - INFO - [apply_chapter_edit] 参数: chapter_id=7f9ecac9-5dca-4340-93f8-ea58738193c3, operation=insert, content_len=137
2026-01-13 12:52:46,730 - app.services.chapter_word_stat_service - INFO - 记录字数增量: chapter_id=7f9ecac9-5dca-4340-93f8-ea58738193c3, delta=123, edit_event_id=None
2026-01-13 12:52:46,733 - app.services.agent.tools.operation_log - INFO - [OperationLog] 记录操作: update_content - update content (insert)
2026-01-13 12:52:46,733 - app.services.agent.tools.tool_types - INFO - [apply_chapter_edit] 执行成功 (耗时: 0.049s)
2026-01-13 12:52:46,733 - app.services.agent.execution.tool_executor - INFO - [StandardTool] apply_chapter_edit 执行成功
2026-01-13 12:52:46,736 - app.api.v1.agent - INFO - [Stream] 任务完成: 将新段落应用到第3章编辑器 (0.1s)
2026-01-13 12:52:46,736 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行任务7完成
2026-01-13 12:52:46,736 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共7个任务，耗时: 50.39s
2026-01-13 12:52:46,736 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2026-01-13 12:52:46,736 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=1, 输出型=6, 展示型=0
2026-01-13 12:52:46,741 - app.services.agent.langgraph_agent - INFO - [Response] 6个输出任务（含续写），使用AI整合
2026-01-13 12:52:46,742 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2026-01-13 12:52:46,742 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=1, 输出型=6, 展示型=0
2026-01-13 12:52:46,742 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=9374字符, 处理后=9470字符
2026-01-13 12:52:46,742 - app.services.agent.planning.response_builder - INFO - [Summarization] 准备发送 summarization_start 事件
2026-01-13 12:52:46,742 - app.services.agent.stream.stream_event_handler - INFO - [StreamEventHandler] emit_summarization_start 被调用, _on_flow_event=True
2026-01-13 12:52:46,742 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_start 事件已发送
2026-01-13 12:52:46,742 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2026-01-13 12:52:46,742 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2026-01-13 12:52:46,757 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-13 12:52:46,758 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-13 12:52:46,758 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
INFO:     connection closed
INFO:     ('127.0.0.1', 62558) - "WebSocket /api/v1/ws/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3OTkxM2U3ZS1kNWNkLTRlMDktYmNlNi1jYTY2MzliZDg0NTYiLCJleHAiOjE3NjgyODI5MjEsInR5cGUiOiJhY2Nlc3MifQ.BieEn6fVM9HiDvlxVC-4n0nbKZNkG-EwRE4QXcwRjl4" [accepted]
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 58820) - "WebSocket /api/v1/ws/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3OTkxM2U3ZS1kNWNkLTRlMDktYmNlNi1jYTY2MzliZDg0NTYiLCJleHAiOjE3NjgyODI5MjEsInR5cGUiOiJhY2Nlc3MifQ.BieEn6fVM9HiDvlxVC-4n0nbKZNkG-EwRE4QXcwRjl4" [accepted]
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 54963) - "WebSocket /api/v1/ws/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3OTkxM2U3ZS1kNWNkLTRlMDktYmNlNi1jYTY2MzliZDg0NTYiLCJleHAiOjE3NjgyODI5MjEsInR5cGUiOiJhY2Nlc3MifQ.BieEn6fVM9HiDvlxVC-4n0nbKZNkG-EwRE4QXcwRjl4" [accepted]
INFO:     connection open
2026-01-13 12:52:52,968 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/stickers/search
INFO:     127.0.0.1:54526 - "GET /api/v1/stickers/search?q=%E5%93%88%E5%93%88&limit=20 HTTP/1.1" 200 OK
INFO:     connection closed
INFO:     ('127.0.0.1', 57334) - "WebSocket /api/v1/ws/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3OTkxM2U3ZS1kNWNkLTRlMDktYmNlNi1jYTY2MzliZDg0NTYiLCJleHAiOjE3NjgyODI5MjEsInR5cGUiOiJhY2Nlc3MifQ.BieEn6fVM9HiDvlxVC-4n0nbKZNkG-EwRE4QXcwRjl4" [accepted]
INFO:     connection open
2026-01-13 12:52:56,087 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/stickers/search
INFO:     127.0.0.1:56901 - "GET /api/v1/stickers/search?q=%E5%93%88%E5%93%88&limit=20 HTTP/1.1" 200 OK
INFO:     connection closed
INFO:     ('127.0.0.1', 56773) - "WebSocket /api/v1/ws/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3OTkxM2U3ZS1kNWNkLTRlMDktYmNlNi1jYTY2MzliZDg0NTYiLCJleHAiOjE3NjgyODI5MjEsInR5cGUiOiJhY2Nlc3MifQ.BieEn6fVM9HiDvlxVC-4n0nbKZNkG-EwRE4QXcwRjl4" [accepted]
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 55537) - "WebSocket /api/v1/ws/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3OTkxM2U3ZS1kNWNkLTRlMDktYmNlNi1jYTY2MzliZDg0NTYiLCJleHAiOjE3NjgyODI5MjEsInR5cGUiOiJhY2Nlc3MifQ.BieEn6fVM9HiDvlxVC-4n0nbKZNkG-EwRE4QXcwRjl4" [accepted]
INFO:     connection open
2026-01-13 12:53:00,058 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/stickers/search
INFO:     127.0.0.1:56183 - "GET /api/v1/stickers/search?q=%E5%93%88%E5%93%88&limit=20&pos=CBQQ0t3pnNyHkgMaHgoKAD-_yvSwBW_t3xIQh124lePxaJ63P2fcAAAAADAU HTTP/1.1" 200 OK
INFO:     connection closed
2026-01-13 12:53:02,627 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/friends/requests/count
INFO:     127.0.0.1:58462 - "GET /api/v1/friends/requests/count HTTP/1.1" 200 OK
INFO:     ('127.0.0.1', 63613) - "WebSocket /api/v1/ws/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3OTkxM2U3ZS1kNWNkLTRlMDktYmNlNi1jYTY2MzliZDg0NTYiLCJleHAiOjE3NjgyODI5MjEsInR5cGUiOiJhY2Nlc3MifQ.BieEn6fVM9HiDvlxVC-4n0nbKZNkG-EwRE4QXcwRjl4" [accepted]
INFO:     connection open
2026-01-13 12:53:02,636 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9/unread-info
INFO:     127.0.0.1:58463 - "GET /api/v1/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9/unread-info HTTP/1.1" 200 OK
2026-01-13 12:53:03,234 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-13 12:53:03,235 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_complete 事件已发送（第一个chunk时）
2026-01-13 12:53:03,237 - app.services.agent.planning.response_builder - INFO - [Summarization] output_ready 事件已发送（第一个chunk时）
2026-01-13 12:53:03,318 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/stickers/search
INFO:     127.0.0.1:51425 - "GET /api/v1/stickers/search?q=%E5%93%88%E5%93%88&limit=20 HTTP/1.1" 200 OK
INFO:     connection closed
INFO:     ('127.0.0.1', 54052) - "WebSocket /api/v1/ws/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3OTkxM2U3ZS1kNWNkLTRlMDktYmNlNi1jYTY2MzliZDg0NTYiLCJleHAiOjE3NjgyODI5MjEsInR5cGUiOiJhY2Nlc3MifQ.BieEn6fVM9HiDvlxVC-4n0nbKZNkG-EwRE4QXcwRjl4" [accepted]
INFO:     connection open
2026-01-13 12:53:06,964 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/stickers/favorites
2026-01-13 12:53:06,967 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/stickers/my
INFO:     127.0.0.1:61788 - "GET /api/v1/stickers/favorites?skip=0&limit=50 HTTP/1.1" 200 OK
INFO:     127.0.0.1:61787 - "GET /api/v1/stickers/my?skip=0&limit=50 HTTP/1.1" 200 OK
2026-01-13 12:53:07,004 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/stickers/search
INFO:     127.0.0.1:50582 - "GET /api/v1/stickers/search?q=%E5%93%88%E5%93%88&limit=20 HTTP/1.1" 200 OK
2026-01-13 12:53:07,052 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/stickers/favorites
INFO:     127.0.0.1:50628 - "GET /api/v1/stickers/favorites?skip=0&limit=50 HTTP/1.1" 200 OK
2026-01-13 12:53:07,066 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/stickers/my
INFO:     127.0.0.1:50630 - "GET /api/v1/stickers/my?skip=0&limit=50 HTTP/1.1" 200 OK
2026-01-13 12:53:07,642 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/stickers/favorites
INFO:     127.0.0.1:55319 - "GET /api/v1/stickers/favorites?skip=0&limit=50 HTTP/1.1" 200 OK
INFO:     connection closed
INFO:     ('127.0.0.1', 62848) - "WebSocket /api/v1/ws/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3OTkxM2U3ZS1kNWNkLTRlMDktYmNlNi1jYTY2MzliZDg0NTYiLCJleHAiOjE3NjgyODI5MjEsInR5cGUiOiJhY2Nlc3MifQ.BieEn6fVM9HiDvlxVC-4n0nbKZNkG-EwRE4QXcwRjl4" [accepted]
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 64102) - "WebSocket /api/v1/ws/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3OTkxM2U3ZS1kNWNkLTRlMDktYmNlNi1jYTY2MzliZDg0NTYiLCJleHAiOjE3NjgyODI5MjEsInR5cGUiOiJhY2Nlc3MifQ.BieEn6fVM9HiDvlxVC-4n0nbKZNkG-EwRE4QXcwRjl4" [accepted]
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 59653) - "WebSocket /api/v1/ws/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3OTkxM2U3ZS1kNWNkLTRlMDktYmNlNi1jYTY2MzliZDg0NTYiLCJleHAiOjE3NjgyODI5MjEsInR5cGUiOiJhY2Nlc3MifQ.BieEn6fVM9HiDvlxVC-4n0nbKZNkG-EwRE4QXcwRjl4" [accepted]
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 53857) - "WebSocket /api/v1/ws/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3OTkxM2U3ZS1kNWNkLTRlMDktYmNlNi1jYTY2MzliZDg0NTYiLCJleHAiOjE3NjgyODI5MjEsInR5cGUiOiJhY2Nlc3MifQ.BieEn6fVM9HiDvlxVC-4n0nbKZNkG-EwRE4QXcwRjl4" [accepted]
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 50383) - "WebSocket /api/v1/ws/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3OTkxM2U3ZS1kNWNkLTRlMDktYmNlNi1jYTY2MzliZDg0NTYiLCJleHAiOjE3NjgyODI5MjEsInR5cGUiOiJhY2Nlc3MifQ.BieEn6fVM9HiDvlxVC-4n0nbKZNkG-EwRE4QXcwRjl4" [accepted]
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 65518) - "WebSocket /api/v1/ws/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3OTkxM2U3ZS1kNWNkLTRlMDktYmNlNi1jYTY2MzliZDg0NTYiLCJleHAiOjE3NjgyODI5MjEsInR5cGUiOiJhY2Nlc3MifQ.BieEn6fVM9HiDvlxVC-4n0nbKZNkG-EwRE4QXcwRjl4" [accepted]
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 57169) - "WebSocket /api/v1/ws/channels/b916971e-9f21-47e3-99ff-3e4535716b95?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3OTkxM2U3ZS1kNWNkLTRlMDktYmNlNi1jYTY2MzliZDg0NTYiLCJleHAiOjE3NjgyODI5MjEsInR5cGUiOiJhY2Nlc3MifQ.BieEn6fVM9HiDvlxVC-4n0nbKZNkG-EwRE4QXcwRjl4" [accepted]
INFO:     connection open
2026-01-13 12:53:18,925 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/b916971e-9f21-47e3-99ff-3e4535716b95/pinned-messages
INFO:     127.0.0.1:59157 - "GET /api/v1/channels/b916971e-9f21-47e3-99ff-3e4535716b95/pinned-messages HTTP/1.1" 200 OK
2026-01-13 12:53:18,950 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/b916971e-9f21-47e3-99ff-3e4535716b95/latest-announcement
2026-01-13 12:53:18,954 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/b916971e-9f21-47e3-99ff-3e4535716b95/members
INFO:     127.0.0.1:59162 - "GET /api/v1/channels/b916971e-9f21-47e3-99ff-3e4535716b95/latest-announcement HTTP/1.1" 200 OK
2026-01-13 12:53:18,968 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/b916971e-9f21-47e3-99ff-3e4535716b95/unread-info
INFO:     127.0.0.1:59159 - "GET /api/v1/channels/b916971e-9f21-47e3-99ff-3e4535716b95/members HTTP/1.1" 200 OK
INFO:     127.0.0.1:59158 - "GET /api/v1/channels/b916971e-9f21-47e3-99ff-3e4535716b95/unread-info HTTP/1.1" 200 OK
2026-01-13 12:53:19,025 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/b916971e-9f21-47e3-99ff-3e4535716b95/messages
INFO:     127.0.0.1:59163 - "GET /api/v1/channels/b916971e-9f21-47e3-99ff-3e4535716b95/messages?params%5Bskip%5D=0&params%5Blimit%5D=50 HTTP/1.1" 200 OK
2026-01-13 12:53:19,049 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/b916971e-9f21-47e3-99ff-3e4535716b95/members
INFO:     127.0.0.1:54554 - "GET /api/v1/channels/b916971e-9f21-47e3-99ff-3e4535716b95/members HTTP/1.1" 200 OK
2026-01-13 12:53:19,127 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/b916971e-9f21-47e3-99ff-3e4535716b95/latest-announcement
INFO:     127.0.0.1:52680 - "GET /api/v1/channels/b916971e-9f21-47e3-99ff-3e4535716b95/latest-announcement HTTP/1.1" 200 OK
2026-01-13 12:53:19,143 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/invite/kRY6JRfT/preview
INFO:     127.0.0.1:52679 - "GET /api/v1/channels/invite/kRY6JRfT/preview HTTP/1.1" 200 OK
2026-01-13 12:53:19,188 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/invite/kRY6JRfT/preview
INFO:     127.0.0.1:53536 - "GET /api/v1/channels/invite/kRY6JRfT/preview HTTP/1.1" 200 OK
2026-01-13 12:53:19,369 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/channels/b916971e-9f21-47e3-99ff-3e4535716b95/mark-read
INFO:     127.0.0.1:51481 - "POST /api/v1/channels/b916971e-9f21-47e3-99ff-3e4535716b95/mark-read HTTP/1.1" 200 OK
INFO:     connection closed
INFO:     ('127.0.0.1', 53525) - "WebSocket /api/v1/ws/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3OTkxM2U3ZS1kNWNkLTRlMDktYmNlNi1jYTY2MzliZDg0NTYiLCJleHAiOjE3NjgyODI5MjEsInR5cGUiOiJhY2Nlc3MifQ.BieEn6fVM9HiDvlxVC-4n0nbKZNkG-EwRE4QXcwRjl4" [accepted]
INFO:     connection open
2026-01-13 12:53:22,611 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9/pinned-messages
INFO:     127.0.0.1:58129 - "GET /api/v1/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9/pinned-messages HTTP/1.1" 200 OK
2026-01-13 12:53:22,626 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/invite/UZ7CMmgT/preview
2026-01-13 12:53:22,628 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9/latest-announcement
INFO:     127.0.0.1:58134 - "GET /api/v1/channels/invite/UZ7CMmgT/preview HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:58137 - "GET /api/v1/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9/latest-announcement HTTP/1.1" 200 OK
2026-01-13 12:53:22,633 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9/members
INFO:     127.0.0.1:58136 - "GET /api/v1/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9/members HTTP/1.1" 200 OK
2026-01-13 12:53:22,642 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9/unread-info
INFO:     127.0.0.1:58135 - "GET /api/v1/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9/unread-info HTTP/1.1" 200 OK
2026-01-13 12:53:22,689 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/invite/UZ7CMmgT/preview
2026-01-13 12:53:22,691 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9/members
INFO:     127.0.0.1:52461 - "GET /api/v1/channels/invite/UZ7CMmgT/preview HTTP/1.1" 400 Bad Request
INFO:     127.0.0.1:59518 - "GET /api/v1/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9/members HTTP/1.1" 200 OK
2026-01-13 12:53:23,026 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9/mark-read
INFO:     127.0.0.1:60511 - "POST /api/v1/channels/532e853c-06c9-4259-8b3b-7e517bfbadf9/mark-read HTTP/1.1" 200 OK
2026-01-13 12:53:23,053 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 100 个数据块，总长度: 9777
2026-01-13 12:53:23,053 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 17403 (prompt=10823, completion=6580)
2026-01-13 12:53:23,053 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-13 12:53:23,053 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-13 12:53:23,078 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-13 12:53:23,080 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=17403, cost=$0.019697, time=36294ms
2026-01-13 12:53:23,080 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=9777
2026-01-13 12:53:23,905 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:48e063af-6b4d-4911-817c-b5dc41d863b9 | 重要度=0.87
2026-01-13 12:53:25,771 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:48e063af-6b4d-4911-817c-b5dc41d863b9 | 重要度=0.60
2026-01-13 12:53:25,808 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:48e063af-6b4d-4911-817c-b5dc41d863b9:85422cf3-a26c-4dd4-a949-181434cd410b, token=10221
2026-01-13 12:53:25,815 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:48e063af-6b4d-4911-817c-b5dc41d863b9:85422cf3-a26c-4dd4-a949-181434cd410b, 消息数=2, 摘要长度=0, Token=10221
2026-01-13 12:53:25,815 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:48e063af-6b4d-4911-817c-b5dc41d863b9:85422cf3-a26c-4dd4-a949-181434cd410b)
2026-01-13 12:53:25,815 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2026-01-13 12:53:25,823 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed